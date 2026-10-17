# frozen_string_literal: true

require 'minitest/autorun'
require 'yaml'

class SeriesTitleConventionTest < Minitest::Test
  ROOT = File.expand_path(ENV.fetch('SERIES_TITLE_ROOT', '..'), __dir__)
  EXPECTED = {
    '_posts/2026-06-27-multiagente-penta-agent-modelos-v2.md' =>
      'Multiagentes en 3 cucharadas (parte I): lo que me funcionó y lo que no',
    '_posts/2026-06-27-multiagente-penta-agent-modelos-v2-en.md' =>
      'Multi-agent work in three spoonfuls (part I): what worked for me and what did not',
    '_posts/2026-07-23-multiagente-penta-agent-memoria.md' =>
      'Multiagentes en 3 cucharadas (parte II): una memoria que se puede auditar',
    '_posts/2026-07-23-multiagente-penta-agent-memoria-en.md' =>
      'Multi-agent work in three spoonfuls (part II): auditable memory',
    '_posts/2026-09-03-multiagente-penta-agent-memoria-gobernada-poc.md' =>
      'Multiagentes en 3 cucharadas (parte III): una memoria que deja huellas',
    '_posts/2026-09-03-multiagente-penta-agent-memoria-gobernada-poc-en.md' =>
      'Multi-agent work in three spoonfuls (part III): a memory that leaves traces',
    '_posts/2026-07-26-avaluo-vulnerabilidad-unidad-vecinal.md' =>
      'Avalúo y vulnerabilidad en 3 cucharadas (parte I): cambie el denominador, cambie el mapa',
    '_posts/2026-07-26-avaluo-vulnerabilidad-unidad-vecinal-en.md' =>
      'Appraisal and vulnerability in 3 spoonfuls (part I): change the denominator, change the map',
    '_posts/2026-09-11-avaluos-ii-brecha-residencial.md' =>
      'Avalúos en 3 cucharadas (parte II): dónde revisar la brecha residencial',
    '_posts/2026-09-11-avaluos-ii-brecha-residencial-en.md' =>
      'Property assessments in 3 spoonfuls (part II): where to review the residential gap',
    '_posts/2026-08-29-replica-tesis-establecimientos-educacionales.md' =>
      'Replicar mi tesis en 3 cucharadas (parte I): qué sobrevivió y qué corrigió la evidencia',
    '_posts/2026-08-29-replica-tesis-establecimientos-educacionales-en.md' =>
      'Replicating my thesis in three spoonfuls (part I): what survived and what the evidence corrected',
    '_posts/2026-10-11-extender-tesis-no-es-agregar-anos.md' =>
      'Extender mi tesis en 3 cucharadas (parte II): lo que el recambio escolar todavía no permite concluir',
    '_posts/2026-10-11-extender-tesis-no-es-agregar-anos-en.md' =>
      'Extending my thesis in three spoonfuls (part II): what school turnover still cannot tell us'
  }.freeze
  BARE_ROMAN = /(?:3 cucharadas|(?:3|three) spoonfuls)\s+[IVX]+:/i

  def front_title(relative)
    source = File.read(File.join(ROOT, relative), encoding: 'UTF-8')
    front = source.match(/\A---\s*\n(.*?)\n---\s*\n/m)&.[](1)
    refute_nil front, "#{relative}: front matter ausente"
    line = front.lines.find { |candidate| candidate.start_with?('title:') }
    refute_nil line, "#{relative}: title ausente"
    YAML.safe_load(line).fetch('title')
  end

  def actual_titles
    titles = EXPECTED.to_h { |relative, _title| [relative, front_title(relative)] }
    case ENV['SERIES_TITLE_NEGATIVE_FIXTURE']
    when nil, ''
      titles
    when 'bare-roman'
      titles.merge(EXPECTED.keys.first => titles.fetch(EXPECTED.keys.first).sub('(parte I)', 'I'))
    when 'missing-part-i'
      titles.merge(EXPECTED.keys.first => titles.fetch(EXPECTED.keys.first).sub(' (parte I)', ''))
    when 'wrong-language'
      titles.merge(EXPECTED.keys.first => titles.fetch(EXPECTED.keys.first).sub('(parte I)', '(part I)'))
    else
      flunk "fixture negativo desconocido: #{ENV['SERIES_TITLE_NEGATIVE_FIXTURE']}"
    end
  end

  def test_known_series_use_the_exact_bilingual_part_labels
    titles = actual_titles
    EXPECTED.each do |relative, expected|
      assert_equal expected, titles.fetch(relative), relative
    end
  end

  def test_no_published_title_uses_a_bare_roman_after_the_spoonfuls_signature
    Dir.glob(File.join(ROOT, '_posts', '*.md')).sort.each do |path|
      relative = path.delete_prefix("#{ROOT}/")
      refute_match BARE_ROMAN, front_title(relative), relative
    end
  end
end
