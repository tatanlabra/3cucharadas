# frozen_string_literal: true
require 'minitest/autorun'
require 'time'
require_relative '../scripts/lib/ai_disclosure'

class AiDisclosureTest < Minitest::Test
  def declaration(level, text: 'unknown', hero: 'unknown')
    {'ai_disclosure' => {'level' => level, 'components' => {'text' => text, 'hero' => hero}}}
  end

  def test_four_levels_are_preserved
    %w[no_ai some_ai fully_autonomous not_disclosed].each do |level|
      assert_equal level, AiDisclosure.resolve(declaration(level))['level']
    end
  end

  def test_absence_is_not_a_claim_of_ai_assistance
    assert_equal 'not_disclosed', AiDisclosure.resolve({})['level']
    assert_equal 'unknown', AiDisclosure.resolve(declaration('some_ai'))['components']['text']
    refute AiDisclosure.resolve({})['explicit']
    assert AiDisclosure.resolve(declaration('not_disclosed'))['explicit']
  end

  def test_liquid_renderer_preserves_levels_and_unknown_component_history
    require 'liquid'
    template = Liquid::Template.parse(File.read(File.expand_path('../_includes/ai-disclosure.html', __dir__)))
    %w[no_ai some_ai fully_autonomous not_disclosed].each do |level|
      %w[es en].each do |lang|
        html = template.render!({'site' => {'active_lang' => lang}, 'page' => declaration(level), 'include' => {'mode' => 'details'}})
        assert_includes html, %(data-ai-level="#{level}")
        assert_includes html, %(data-ai-text-origin="unknown")
        refute_includes html, '<details'
        assert_operator html.gsub(/<[^>]+>/, '').split.size, :<, 32
        assert_includes html, lang == 'en' ? 'I ' : (level == 'not_disclosed' ? 'Aún no he' : (level == 'fully_autonomous' ? 'Generé' : 'Preparé'))
        refute_includes html, 'Documented tool:'
      end
    end
    html = template.render!({'site' => {'active_lang' => 'en'}, 'page' => {}, 'include' => {'mode' => 'badge'}})
    assert_includes html, 'I have not declared my AI use here yet.'
  end

  def test_legacy_matching_and_conflicts
    assert_equal 'some_ai', AiDisclosure.resolve({'devto_ai_disclosure_level' => 'some_ai'})['level']
    assert_equal 'some_ai', AiDisclosure.resolve(declaration('some_ai').merge('devto_ai_disclosure_level' => 'some_ai'))['level']
    assert_raises(ArgumentError) { AiDisclosure.resolve(declaration('no_ai').merge('devto_ai_disclosure_level' => 'some_ai')) }
  end

  def test_invalid_shape_and_contradictions_fail_closed
    [{'ai_disclosure' => 'some_ai'}, {'ai_disclosure' => {}}, declaration('invented'), declaration('some_ai', hero: 'assisted'), declaration('no_ai', hero: 'generated'), declaration('no_ai', text: 'assisted'), declaration('fully_autonomous', text: 'human')].each do |front|
      assert_raises(ArgumentError, front.inspect) { AiDisclosure.resolve(front) }
    end
  end

  def test_provenance_links_cannot_execute_or_leak_local_paths
    %w[javascript:alert(1) file:///home/private /home/private https://user:secret@example.com https://example.com/?token=secret //example.com].each do |link|
      front = declaration('some_ai')
      front['ai_disclosure']['evidence_url'] = link
      assert_raises(ArgumentError, link) { AiDisclosure.resolve(front) }
    end
    front = declaration('some_ai')
    front['ai_disclosure']['evidence_url'] = 'https://example.com/public-receipt'
    assert_equal 'some_ai', AiDisclosure.resolve(front)['level']
  end
end

require 'tmpdir'
require 'fileutils'
require 'zlib'
require_relative '../scripts/verify_hero_disclosure'

class HeroDisclosureCheckTest < Minitest::Test
  def png(path, width, height)
    chunk = ->(kind, data) { [data.bytesize].pack('N') + kind + data + [Zlib.crc32(kind + data)].pack('N') }
    File.binwrite(path, "\x89PNG\r\n\x1a\n".b + chunk.call('IHDR', [width, height, 8, 2, 0, 0, 0].pack('NNCCCCC')) + chunk.call('IDAT', Zlib.deflate(("\0".b * (width * 3 + 1)) * height)) + chunk.call('IEND', ''.b))
  end

  def setup
    @dir = Dir.mktmpdir('hero-disclosure-test')
    FileUtils.mkdir_p(File.join(@dir, 'assets/images'))
    FileUtils.mkdir_p(File.join(@dir, '_data/visuales'))
    FileUtils.mkdir_p(File.join(@dir, 'ai-transparency'))
    File.write(File.join(@dir, 'ai-transparency/index.html'), 'policy')
    png(File.join(@dir, 'assets/images/hero.png'), 1600, 900)
    png(File.join(@dir, 'assets/images/mobile.png'), 800, 450)
    @front = {'title' => 'Test', 'date' => '2026-09-12', 'lang' => 'es', 'permalink' => '/test/', 'visual_id' => 'test', 'header' => {'overlay_image' => '/assets/images/hero.png', 'overlay_image_mobile' => '/assets/images/mobile.png'}, 'ai_disclosure' => {'level' => 'some_ai', 'components' => {'text' => 'unknown', 'hero' => 'generated'}}}
    @catalog = {'piezas' => %w[hero mobile].map { |name| {'archivo' => "assets/images/#{name}.png", 'estado' => 'publicable', 'rol' => 'hero', 'origen' => 'ia-integrada', 'alt' => {'es' => 'Ilustración', 'en' => 'Illustration'}} }}
    write_catalog
    @html = <<~HTML
      <h1>Test</h1>
      <link rel="canonical" href="https://3cucharadas.cl/test/">
      <link rel="alternate" hreflang="es" href="https://3cucharadas.cl/test/">
      <link rel="alternate" hreflang="en" href="https://3cucharadas.cl/en/test/">
      <meta itemprop="datePublished" content="2026-09-12T00:00:00-04:00">
      <link rel="preload" as="image" href="/assets/images/hero.png" imagesrcset="/assets/images/mobile.png 800w, /assets/images/hero.png 1600w" imagesizes="100vw">
      <picture aria-hidden="true"><img src="/assets/images/hero.png" srcset="/assets/images/mobile.png 800w, /assets/images/hero.png 1600w" sizes="100vw" width="1600" height="900" alt="" fetchpriority="high" loading="eager"></picture>
      <p id="ai-disclosure" data-ai-level="some_ai" data-ai-text-origin="unknown" data-ai-hero-origin="generated">Preparé este artículo con ayuda de IA.</p>
      <a href="/ai-transparency/">Policy</a>
    HTML
  end

  def teardown
    FileUtils.remove_entry(@dir)
  end

  def write_catalog
    File.write(File.join(@dir, '_data/visuales/test.yml'), @catalog.to_yaml)
  end

  def test_valid_source_and_artifact_recover_green
    assert_empty HeroDisclosureCheck.source_errors(@front, @dir)
    assert_empty HeroDisclosureCheck.artifact_errors(@front, @html, @dir)
  end

  def test_explicit_timestamp_is_compared_as_an_instant_across_timezones
    @front['date'] = Time.iso8601('2026-07-15T00:00:00Z')
    html = @html.sub('2026-09-12T00:00:00-04:00', '2026-07-14T20:00:00-04:00')
    assert_empty HeroDisclosureCheck.artifact_errors(@front, html, @dir)
    wrong = html.sub('2026-07-14T20:00:00-04:00', '2026-07-15T20:00:00-04:00')
    assert HeroDisclosureCheck.artifact_errors(@front, wrong, @dir).any? { |e| e.include?('publication date differs') }
    @front['date'] = '2026-07-15 00:00:00 +0000'
    assert_empty HeroDisclosureCheck.artifact_errors(@front, html, @dir)
  end

  def test_empty_inventory_is_a_failure
    assert_includes HeroDisclosureCheck.run(root: @dir), 'empty post inventory'
  end

  def test_missing_mobile_and_unknown_catalog_origin_reject
    File.unlink(File.join(@dir, 'assets/images/mobile.png'))
    assert HeroDisclosureCheck.source_errors(@front, @dir).any? { |e| e.include?('missing file') }
    @catalog['piezas'].first['origen'] = 'unknown'
    write_catalog
    assert_includes HeroDisclosureCheck.source_errors(@front, @dir), 'hero AI attribution contradicts catalog origin'
  end

  def test_wrong_dimensions_hash_and_unpublished_catalog_reject
    png(File.join(@dir, 'assets/images/mobile.png'), 640, 360)
    assert HeroDisclosureCheck.source_errors(@front, @dir).any? { |e| e.include?('800x450') }
    @catalog['piezas'].first['sha256'] = '0' * 64
    write_catalog
    assert HeroDisclosureCheck.source_errors(@front, @dir).any? { |e| e.include?('sha256 mismatch') }
    @catalog['piezas'].first['estado'] = 'bloqueado'
    write_catalog
    assert HeroDisclosureCheck.source_errors(@front, @dir).any? { |e| e.include?('not a publicable') }
  end

  def test_real_webp_derivative_requires_digest_role_and_byte_budget
    relative = 'assets/images/heroes-v2/test/hero.webp'
    target = File.join(@dir, relative)
    FileUtils.mkdir_p(File.dirname(target))
    FileUtils.cp(File.expand_path('../assets/images/avaluos-ii/hero-brecha-residencial-tokyo-night-1600x900.webp', __dir__), target)
    piece = {'archivo' => relative, 'rol' => 'hero', 'estado' => 'publicable', 'ancho' => 1600, 'alto' => 900, 'sha256' => Digest::SHA256.file(target).hexdigest}
    assert_empty HeroDisclosureCheck.variant_errors(piece, @dir)
    assert HeroDisclosureCheck.variant_errors(piece.merge('sha256' => nil), @dir).any? { |e| e.include?('SHA256') }
    assert HeroDisclosureCheck.variant_errors(piece.merge('rol' => 'teaser'), @dir).any? { |e| e.include?('role mismatch') }
    File.open(target, 'ab') { |f| f.write('x' * 250_001) }
    assert HeroDisclosureCheck.variant_errors(piece, @dir).any? { |e| e.include?('exceeds 250000') }
  end

  def test_preload_disclosure_duplicate_title_and_date_mutations_reject
    mutations = {
      'preload differs' => @html.sub('imagesizes="100vw"', 'imagesizes="50vw"'),
      'exactly one h1' => @html + '<h1>Duplicate</h1>',
      'incorrect disclosure level' => @html.sub('data-ai-level="some_ai"', 'data-ai-level="no_ai"'),
      'publication date differs' => @html.sub('2026-09-12T', '2026-09-11T'),
      'canonical differs' => @html.sub('rel="canonical" href="https://3cucharadas.cl/test/"', 'rel="canonical" href="https://3cucharadas.cl/wrong/"'),
      'incorrect rendered text provenance' => @html.sub('data-ai-text-origin="unknown"', 'data-ai-text-origin="assisted"')
    }
    mutations.each do |message, html|
      assert HeroDisclosureCheck.artifact_errors(@front, html, @dir).any? { |e| e.include?(message) }, message
    end
    assert_empty HeroDisclosureCheck.artifact_errors(@front, @html, @dir)
  end
end
