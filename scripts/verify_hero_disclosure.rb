#!/usr/bin/env ruby
# frozen_string_literal: true
# Source validation always runs. Passing an artifact also verifies each expected
# post, rather than accepting an empty/stale subset found by a glob.
require 'date'
require 'yaml'
require 'cgi'
require 'digest'
require 'uri'
require_relative 'lib/ai_disclosure'
require_relative 'lib/image_dimensions'

module HeroDisclosureCheck
  module_function
  def attributes(tag)
    tag.to_s.scan(/([\w:-]+)\s*=\s*["']([^"']*)["']/).to_h.transform_values { |v| CGI.unescapeHTML(v) }
  end

  # Public responsive derivatives have a fixed size/role/byte contract.
  def variant_errors(piece, root)
    path = piece['archivo'].to_s
    return [] unless path.start_with?('assets/images/heroes-v2/')
    return ['invalid variant path'] if path.include?('..')
    file = File.join(root, path)
    return ["variant missing: #{path}"] unless File.file?(file)
    errors = []
    signature = File.binread(file, 12)
    errors << "variant is not WebP: #{path}" unless File.extname(file) == '.webp' && signature.start_with?('RIFF') && signature[8, 4] == 'WEBP'
    contracts = {[1600, 900] => ['hero', 250_000], [800, 450] => ['hero', 100_000], [1280, 720] => ['teaser', 180_000], [640, 360] => ['teaser', 70_000], [1200, 630] => ['og', 180_000]}
    dimensions = image_dimensions(file)
    contract = contracts[dimensions]
    if contract
      errors << "variant role mismatch: #{path}" unless piece['rol'] == contract.first
      errors << "variant exceeds #{contract.last} bytes: #{path}" if File.size(file) > contract.last
    else
      errors << "variant dimensions outside contract: #{path}"
    end
    errors << "variant declared dimensions mismatch: #{path}" unless dimensions && [piece['ancho'], piece['alto']] == dimensions
    errors << "variant must be publicable: #{path}" unless piece['estado'] == 'publicable'
    expected_hash = piece['sha256'].to_s
    errors << "variant SHA256 missing/mismatch: #{path}" unless expected_hash.match?(/\A[0-9a-f]{64}\z/) && Digest::SHA256.file(file).hexdigest == expected_hash
    errors
  end

  def source_errors(front, root)
    errors = []
    begin
      disclosure = AiDisclosure.resolve(front)
    rescue ArgumentError => e
      return [e.message]
    end
    header = front['header'] || {}
    hero, mobile = header.values_at('overlay_image', 'overlay_image_mobile')
    {'overlay_image' => [hero, [1600, 900], 250_000], 'overlay_image_mobile' => [mobile, [800, 450], 100_000]}.each do |key, (path, dims, budget)|
      unless path.is_a?(String) && path.start_with?('/assets/images/') && !path.include?('..')
        errors << "header.#{key}: missing or invalid local hero"
        next
      end
      actual = File.join(root, path.delete_prefix('/'))
      errors << "header.#{key}: missing file #{path}" unless File.file?(actual)
      errors << "header.#{key}: expected #{dims.join('x')}" unless image_dimensions(actual) == dims
      errors << "header.#{key}: exceeds #{budget} bytes" if File.file?(actual) && File.size(actual) > budget
    end
    visual_id = front['visual_id'].to_s
    unless visual_id.match?(/\A[a-z0-9_-]+\z/)
      return errors + ['missing/invalid visual_id']
    end
    catalog_path = File.join(root, '_data', 'visuales', "#{visual_id}.yml")
    return errors + ['visual_id catalog missing'] unless File.file?(catalog_path)
    catalog = YAML.safe_load_file(catalog_path, permitted_classes: [Date, Time], aliases: true)
    pieces = Array(catalog['piezas'])
    [hero, mobile].each do |path|
      piece = pieces.find { |p| p['archivo'] == path.to_s.delete_prefix('/') }
      unless piece && piece['estado'] == 'publicable' && piece['rol'] == 'hero'
        errors << "hero not a publicable catalog hero: #{path}"
        next
      end
      errors.concat(variant_errors(piece, root))
      %w[es en].each { |lang| errors << "hero missing #{lang} description" if piece.dig('alt', lang).to_s.strip.empty? }
      component = disclosure.dig('components', 'hero')
      ai_origin = %w[ia ia-integrada ai ai-generated].include?(piece['origen'])
      errors << 'hero AI attribution contradicts catalog origin' if (component == 'generated') != ai_origin
      errors << 'human hero attribution lacks human catalog origin' if component == 'human' && !%w[human humano].include?(piece['origen'])
      errors << 'no_ai contradicts catalog AI hero' if disclosure['level'] == 'no_ai' && ai_origin
      if piece['sha256']
        actual = File.join(root, path.to_s.delete_prefix('/'))
        errors << "hero sha256 mismatch: #{path}" unless File.file?(actual) && Digest::SHA256.file(actual).hexdigest == piece['sha256']
      end
    end
    errors
  rescue Psych::Exception => e
    errors + ["invalid catalog YAML: #{e.message}"]
  end

  def artifact_errors(front, html, site_dir)
    errors = []
    expected = AiDisclosure.resolve(front)
    errors << 'expected exactly one h1' unless html.scan(/<h1\b/i).size == 1
    images = html.scan(/<img\b[^>]*>/i).select { |tag| attributes(tag)['fetchpriority'] == 'high' }
    if images.size != 1
      errors << 'expected one high-priority hero image'
    else
      img = attributes(images.first)
      errors << 'hero image must have decorative picture wrapper' unless html.match?(%r{<picture\b[^>]*aria-hidden="true"[^>]*>\s*#{Regexp.escape(images.first)}}m)
      errors << 'hero must be eager and decorative with fixed dimensions' unless img.values_at('loading', 'alt', 'width', 'height') == ['eager', '', '1600', '900']
      header = front.fetch('header')
      expected_srcset = "#{header['overlay_image_mobile']} 800w, #{header['overlay_image']} 1600w"
      errors << 'hero src differs from source' unless img['src'] == header['overlay_image']
      errors << 'hero responsive candidates differ from source' unless img['srcset'] == expected_srcset && img['sizes'] == '100vw'
      preloads = html.scan(/<link\b[^>]*>/i).map { |tag| attributes(tag) }.select { |a| a['rel'] == 'preload' && a['as'] == 'image' }
      errors << 'preload differs from effective image' unless preloads.size == 1 && preloads.first.values_at('href', 'imagesrcset', 'imagesizes') == img.values_at('src', 'srcset', 'sizes')
      [img['src'], *img.fetch('srcset', '').split(',').map { |c| c.strip.split.first }].compact.each do |path|
        errors << "missing built hero #{path}" unless File.file?(File.join(site_dir, path.delete_prefix('/')))
      end
    end
    notes = html.scan(/<p\b[^>]*>/i).map { |tag| attributes(tag) }.select { |a| a['id'] == 'ai-disclosure' }
    errors << 'missing/incorrect disclosure level' unless notes.size == 1 && notes.first['data-ai-level'] == expected['level']
    expected['components'].each do |component, origin|
      errors << "incorrect rendered #{component} provenance" unless notes.size == 1 && notes.first["data-ai-#{component}-origin"] == origin
    end
    language = front.fetch('lang', 'es')
    prefix = language == 'es' ? '' : "/#{language}"
    canonical = "https://3cucharadas.cl#{prefix}#{front['permalink']}"
    links = html.scan(/<link\b[^>]*>/i).map { |tag| attributes(tag) }
    errors << 'canonical differs from source permalink/lang' unless links.select { |a| a['rel'] == 'canonical' }.map { |a| a['href'] } == [canonical]
    %w[es en].each do |lang|
      href = "https://3cucharadas.cl#{lang == 'es' ? '' : '/en'}#{front['permalink']}"
      errors << "missing #{lang} hreflang" unless links.any? { |a| a['hreflang'] == lang && a['href'] == href }
    end
    published = html.scan(/<meta\b[^>]*>/i).map { |tag| attributes(tag) }.find { |a| a['itemprop'] == 'datePublished' }
    source_date = front.fetch('date').to_s
    rendered_date = published && published['content'].to_s
    # Explicit timestamps preserve an instant, even when Jekyll converts midnight
    # UTC to the preceding calendar date in Chile. Date-only posts preserve a day.
    same_date = if source_date.match?(/\d{2}:\d{2}/)
      rendered_date && DateTime.parse(rendered_date) == DateTime.parse(source_date)
    else
      rendered_date && Date.parse(rendered_date) == Date.parse(source_date)
    end
    errors << 'publication date differs from source' unless same_date
    policy = "#{prefix}/ai-transparency/"
    errors << 'missing localized policy link' unless html.include?(%(href="#{policy}"))
    errors << 'missing built policy' unless File.file?(File.join(site_dir, policy.delete_prefix('/'), 'index.html'))
    errors
  end

  def run(root:, artifact: nil)
    posts = Dir.glob(File.join(root, '_posts', '*.md')).sort
    return ['empty post inventory'] if posts.empty?
    posts.flat_map do |path|
      front = YAML.safe_load(File.read(path).split(/^---\s*$/, 3)[1], permitted_classes: [Date, Time], aliases: true)
      errors = source_errors(front, root)
      if artifact
        prefix = front['lang'] == 'en' ? 'en/' : ''
        target = File.join(artifact, prefix, front.fetch('permalink').delete_prefix('/'), 'index.html')
        if File.file?(target)
          errors.concat(artifact_errors(front, File.read(target), artifact)) if errors.empty?
        else
          errors << 'expected built post missing'
        end
      end
      errors.map { |e| "#{File.basename(path)}: #{e}" }
    rescue StandardError => e
      ["#{File.basename(path)}: #{e.class}: #{e.message}"]
    end
  end
end

if $PROGRAM_NAME == __FILE__
  root = File.expand_path('..', __dir__)
  artifact = ARGV[0] && File.expand_path(ARGV[0])
  errors = HeroDisclosureCheck.run(root: root, artifact: artifact)
  abort errors.join("\n") unless errors.empty?
  puts "Hero/disclosure OK: #{Dir.glob(File.join(root, '_posts', '*.md')).size} source posts#{artifact ? ' and built pages' : ''}"
end
