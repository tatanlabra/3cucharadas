# frozen_string_literal: true
require 'minitest/autorun'
require 'tmpdir'
require 'fileutils'
require 'open3'
require 'json'

class VerifyDiffusionCoherenceTest < Minitest::Test
  def setup
    @root = Dir.mktmpdir('diffusion-coherence-')
    %w[_posts scripts difusion/paquetes/fixture difusion/linkedin].each { |dir| FileUtils.mkdir_p(File.join(@root, dir)) }
    source = ENV.fetch('COHERENCE_TEST_SCRIPT', File.expand_path('../scripts/verify_difusion_coherente.rb', __dir__))
    FileUtils.cp(source, File.join(@root, 'scripts', 'verify_difusion_coherente.rb'))
    File.write(File.join(@root, 'difusion/paquetes/fixture/00-metadata.json'), JSON.generate(language: 'es'))
  end

  def teardown
    FileUtils.remove_entry(@root)
  end

  def post(lang, body, ref = 'fixture')
    File.write(File.join(@root, "_posts/#{ref}-#{lang}.md"), "---\nref: #{ref}\nlang: #{lang}\ntitle: Fixture\n---\n#{body}\n")
  end

  def copy(name, text)
    File.write(File.join(@root, 'difusion/paquetes/fixture', name), text)
  end

  def gate(*args)
    out, err, status = Open3.capture3('ruby', File.join(@root, 'scripts/verify_difusion_coherente.rb'), *args)
    [out + err, status]
  end

  def test_equivalent_tex_and_locale_values_with_txt_and_json_coverage
    post('es', 'Tasa 0{,}00893 y 0{,}20; 16.955 viviendas.')
    post('en', 'Rate 0.00893 and 0.20; 16,955 dwellings.')
    copy('linkedin.txt', 'Tasa 0,00893 y 16.955 viviendas.')
    copy('social.json', JSON.generate(es: 'Tasa 0,20', en: 'Rate 0.20'))
    out, status = gate('fixture')
    assert status.success?, out
    assert_includes out, 'COPY difusion/paquetes/fixture/linkedin.txt'
    assert_includes out, 'COPY difusion/paquetes/fixture/social.json'
  end

  def test_changed_decimal_in_txt_is_rejected
    post('es', 'Tasa 0,00893')
    copy('linkedin.txt', 'Tasa 0,0893')
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, '0.0893'
  end

  def test_changed_decimal_in_json_is_rejected
    post('es', 'Tasa 0,00893')
    copy('social.json', JSON.generate(en: 'Rate 0.0893'))
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, 'social.json'
  end

  def test_body_reference_to_another_post_does_not_grant_coverage
    post('es', 'fixture: 7654 viviendas.', 'different')
    copy('linkedin.txt', '7654 viviendas.')
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, 'sin cobertura'
  end

  def test_missing_pieces_and_empty_declared_scope_fail
    post('es', '7654 viviendas.')
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, 'sin cobertura'
    FileUtils.rm(File.join(@root, 'difusion/paquetes/fixture/00-metadata.json'))
    out, status = gate('--all-declared')
    refute status.success?, out
  end

  def test_legacy_html_visible_text_is_checked_but_css_is_not
    post('es', '7654 viviendas.')
    legacy = File.join(@root, 'difusion/linkedin/fixture-carrusel.html')
    File.write(legacy, '<style>.x{width:98765px}</style><p>7654 viviendas</p>')
    out, status = gate('fixture')
    assert status.success?, out
    File.write(legacy, '<p>7655 viviendas</p>')
    out, status = gate('fixture')
    refute status.success?, out
  end

  def test_metadata_numbers_do_not_pollute_copy
    post('es', '7654 viviendas.')
    copy('linkedin.txt', '7654 viviendas.')
    copy('00-metadata.json', JSON.generate(language: 'es', characters: 98765))
    out, status = gate('--all-declared')
    assert status.success?, out
  end

  def test_translation_changes_are_rejected_even_if_union_would_cover_copy
    post('es', 'Tasa 0,00893')
    post('en', 'Rate 0.0893')
    copy('linkedin.txt', 'Tasa 0,00893')
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, 'paridad'
  end
  def test_decimal_is_not_equivalent_to_integer_and_other_locale_is_explicit
    post('es', 'Tasa 0,20')
    copy('social.json', JSON.generate(en: 'Rate 20'))
    out, status = gate('fixture')
    refute status.success?, out
    copy('social.json', JSON.generate(en: 'Rate 0,20'))
    out, status = gate('fixture')
    assert status.success?, out
    assert_includes out, 'NORMALIZE decimal 0,20 (en)'
  end

  def test_milliseconds_rounding_requires_time_units_and_correct_rounding
    post('es', 'Mediana 6.239 ms y 9.537 ms.')
    copy('linkedin.txt', 'De 6,2 a 9,5 segundos.')
    out, status = gate('fixture')
    assert status.success?, out
    assert_includes out, 'EQUIVALENCE'
    copy('linkedin.txt', 'De 6,3 a 9,5 segundos.')
    out, status = gate('fixture')
    refute status.success?, out
    copy('linkedin.txt', 'Tasa 6,2 y 9,5 pesos.')
    out, status = gate('fixture')
    refute status.success?, out
  end

  def test_reddit_operational_notes_excluded_but_public_title_checked
    post('en', 'There were 7654 cases.')
    text = "REGLAS DEL SUB VERIFICADAS:\nHTTP 403\n\nTÍTULO PROVISIONAL:\n7654 cases\n\nURL PROPUESTA:\nhttps://example.invalid/\n\nPRIMER COMENTARIO PROPUESTO:\n7654 cases\n\nRECORDATORIO DE CONDUCTA:\nNever send\n"
    copy('reddit-target.md', text)
    out, status = gate('fixture')
    assert status.success?, out
    copy('reddit-target.md', text.sub('7654 cases', '7655 cases'))
    out, status = gate('fixture')
    refute status.success?, out
  end

  def test_unknown_json_structure_fails_instead_of_claiming_coverage
    post('en', 'There were 7654 cases.')
    copy('social.json', JSON.generate(posts: [{text: '7654 cases'}]))
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, 'JSON de copy no reconocido'
  end

  def test_versions_keep_their_identity_and_public_environment_is_included
    post('en', 'There were 7654 cases.')
    path = File.join(@root, '_posts/fixture-en.md')
    File.write(path, File.read(path).sub('title: Fixture', 'title: Fixture\nentorno: Tool 0.115.1'.gsub('\\n', "\n")))
    copy('social.json', JSON.generate(en: 'Tool 0.115.1; 7654 cases'))
    out, status = gate('fixture')
    assert status.success?, out
    copy('social.json', JSON.generate(en: 'Tool 0.115.2; 7654 cases'))
    out, status = gate('fixture')
    refute status.success?, out
  end

  def test_two_component_rss_versions_are_identifiers_not_locale_decimals
    post('es', 'El protocolo RSS 2.0 sigue disponible.')
    post('en', 'The RSS 2.0 protocol remains available.')
    copy('social.json', JSON.generate(es: 'RSS 2.0', en: 'RSS 2.0'))
    out, status = gate('fixture')
    assert status.success?, out
    post('en', 'The RSS 2.1 protocol remains available.')
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, 'paridad'
  end

  def test_empty_copy_and_empty_json_fail
    post('en', 'There were 7654 cases.')
    copy('social.json', '{}')
    out, status = gate('fixture')
    refute status.success?, out
    copy('social.json', ' ')
    out, status = gate('fixture')
    refute status.success?, out
  end

  def test_legacy_exact_basename_and_yaml_language_remain_supported
    post('en', '16,955 dwellings.')
    FileUtils.rm(File.join(@root, 'difusion/paquetes/fixture/00-metadata.json'))
    copy('00-metadata.yaml', "language: en\n")
    copy('linkedin.txt', '16,955 dwellings.')
    File.write(File.join(@root, 'difusion/linkedin/fixture.md'), '16955 dwellings.')
    out, status = gate('fixture')
    assert status.success?, out
    assert_includes out, 'COPY difusion/linkedin/fixture.md'
    File.write(File.join(@root, 'difusion/linkedin/fixture.md'), '16956 dwellings.')
    out, status = gate('fixture')
    refute status.success?, out
  end

  def test_legacy_lookup_does_not_read_ledger_json_as_copy
    post('es', '7654 viviendas.')
    File.write(File.join(@root, 'difusion/linkedin/fixture.md'), '7654 viviendas.')
    state = File.join(@root, 'difusion/state')
    FileUtils.mkdir_p(state)
    File.write(File.join(state, 'fixture.json'), JSON.generate(id: 998877))
    out, status = gate('fixture')
    assert status.success?, out
    refute_includes out, 'COPY difusion/state'
  end

  def test_rounding_respects_explicit_trailing_decimal_zero
    post('es', 'Mediana 6.239 ms.')
    copy('linkedin.txt', 'Mediana 6,20 segundos.')
    out, status = gate('fixture')
    refute status.success?, out
    copy('linkedin.txt', 'Mediana 6,24 segundos.')
    out, status = gate('fixture')
    assert status.success?, out
    assert_includes out, '(2 decimales)'
  end

  def test_heading_only_markdown_has_no_extracted_copy
    post('es', '7654 viviendas.')
    copy('linkedin.md', "# Encabezado editorial\n")
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, 'copy extraído vacío'
  end

  def test_html_with_only_style_and_markup_has_no_extracted_copy
    post('es', '7654 viviendas.')
    copy('linkedin.html', '<style>.x{width:98765px}</style><div> </div>')
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, 'copy extraído vacío'
  end

  def test_empty_reddit_public_section_is_rejected
    post('en', '7654 cases.')
    copy('reddit-target.md', "TÍTULO PROVISIONAL:\n \nURL PROPUESTA:\nhttps://example.invalid/\n\nPRIMER COMENTARIO PROPUESTO:\n7654 cases\n\nRECORDATORIO DE CONDUCTA:\nNever send\n")
    out, status = gate('fixture')
    refute status.success?, out
    assert_includes out, 'sección publicable vacía'
  end

end
