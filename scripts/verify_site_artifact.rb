#!/usr/bin/env ruby
# frozen_string_literal: true

require "cgi"
require "find"

site_dir = File.expand_path(ARGV.fetch(0, "public"))
max_bytes = Integer(ENV.fetch("SITE_ARTIFACT_MAX_BYTES", "21000000"))

abort "Artifact directory does not exist: #{site_dir}" unless Dir.exist?(site_dir)

required_files = %w[
  assets/css/main.css
  assets/js/main.min.js
  assets/js/theme-toggle.js
  assets/js/lunr/lunr-en.js
  assets/js/lunr/lunr-store.js
  assets/js/lunr/lunr.min.js
  assets/images/clabra2026-320.webp
  assets/images/teasers/teaser-ai-quota-hud-640.webp
  assets/images/teasers/teaser-bayes-hiperparametros-640.webp
  assets/images/teasers/teaser-casen-2024-640.webp
  assets/images/teasers/teaser-multiagentes-vscode-640.webp
  assets/images/teasers/teaser-rss-soberania-digital-640.webp
].freeze

pruned_files = %w[
  assets/images/catppuccin_latte-skin-archive-large.png
  assets/images/catppuccin_mocha-skin-archive-large.png
  assets/images/favicons/favicon.svg
  assets/js/_main.js
  assets/js/lunr/lunr-gr.js
  assets/js/lunr/lunr.js
  assets/js/main.min.js.map
  assets/js/plugins/gumshoe.js
  assets/js/vendor/jquery/jquery-3.6.0.js
].freeze

required_files.each do |relative|
  abort "Required runtime asset is missing: #{relative}" unless File.file?(File.join(site_dir, relative))
end

pruned_files.each do |relative|
  abort "Pruned asset is present: #{relative}" if File.exist?(File.join(site_dir, relative))
end

source_maps = Dir.glob(File.join(site_dir, "**", "*.map"))
abort "Source maps are public: #{source_maps.join(', ')}" unless source_maps.empty?

missing_references = []
extract_references = lambda do |body|
  values = body.scan(/\b(?:src|href|poster|content)=["']([^"']+)["']/i).flatten
  values.concat(body.scan(/\bsrcset=["']([^"']+)["']/i).flatten.flat_map { |srcset| srcset.split(",").map { |entry| entry.strip.split(/\s+/, 2).first } })
  values
end

Dir.glob(File.join(site_dir, "**", "*.{html,css}")).each do |document|
  extract_references.call(File.read(document)).each do |raw_value|
    value = CGI.unescapeHTML(raw_value)
    value = value.sub(%r{\Ahttps://3cucharadas\.cl}, "")
    next unless value.match?(%r{\A/(?:assets/|favicon\.ico)})

    relative = value.split(/[?#]/, 2).first.delete_prefix("/")
    missing_references << [document.delete_prefix("#{site_dir}/"), relative] unless File.file?(File.join(site_dir, relative))
  end
end

unless missing_references.empty?
  missing_references.uniq.each { |document, relative| warn "Missing #{relative} referenced by #{document}" }
  abort "Rendered internal asset references are broken"
end

home = File.read(File.join(site_dir, "index.html"))
abort "Home LCP card is not eager" unless home.include?('loading="eager"') && home.include?('fetchpriority="high"')
abort "Home responsive teaser sources are absent" unless home.include?('teaser-ai-quota-hud-640.webp')

artifact_bytes = 0
Find.find(site_dir) { |entry| artifact_bytes += File.size(entry) if File.file?(entry) }
abort "Artifact exceeds #{max_bytes} bytes: #{artifact_bytes}" if artifact_bytes > max_bytes

puts "Artifact verification passed: #{artifact_bytes} bytes"
