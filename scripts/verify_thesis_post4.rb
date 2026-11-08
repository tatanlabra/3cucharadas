#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "digest"
require "json"
require "pathname"
require "yaml"

class ThesisPost4Error < StandardError; end
class ThesisPost4UsageError < ThesisPost4Error; end

Post4Document = Data.define(:path, :front_matter, :body)

class ThesisPost4Verifier
  FILES = {
    "es" => "_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md",
    "en" => "_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml-en.md"
  }.freeze
  ANNEXES = {
    "es" => "_pages/tesis-post4-anexo-metodologico.md",
    "en" => "_pages/tesis-post4-anexo-metodologico-en.md"
  }.freeze
  BILINGUAL_ONLY_FIXTURES = %w[table-parity-drift].freeze
  EN_ONLY_FIXTURES = %w[figure-contract-drift first-person-plural].freeze
  CAUSAL_ARTIFACT = "assets/data/tesis-post4/post4_higher_education_causal_ml_v1.json"
  RETRO_ARTIFACT = "assets/data/tesis-post4/post4_retrospective_post3_audit.json"
  APPENDIX_WORD_RANGE = (800..15_000).freeze
  MAIN_WORD_RANGE = (2_800..3_500).freeze
  CANONICAL_FIGURES = %w[selection-ladder longitudinal-regimes causal-ml-heterogeneity-paes].freeze
  FIGURE_VARIANTS = %w[light dark light-mobile dark-mobile].freeze
  FIGURE_FORMATS = %w[svg png].freeze
  REQUIRED_ANALYSIS_STAGE = "POST4_HIGHER_EDUCATION_CAUSAL_ML_V1"
  REQUIRED_RESULT_STATE = "SELECTION_DOMINATES_AVERAGE_IPCFT_AND_G1_VULNERABLE_HARMED"
  REQUIRED_READINESS = "READY_INDIVIDUAL_SIES_AND_PAES_VERIFIED"
  PUBLIC_METADATA_KEYS = %w[title subtitle description excerpt tags categories].freeze
  PRIVATE_PATH_PATTERN = %r{/(?:home|mnt|opt|run|tmp)/}i

  FORBIDDEN_NAIVE_PROMOTIONS = {
    "es" => [
      /\b(?:cerrar un liceo|el cierre escolar|los cierres escolares)\s+(?:destruye|reduce|resta)\s+causalmente\s+13[,.]24\b/i,
      /\bel efecto causal promedio general\s+es\s+de\s+[−-]13[,.]24\b/i,
      /\bse utilizaron microdatos\s+DEMRE\s+2014[–-]2020\b/i,
      /[−-]1,43\b/,
      /[−-]2,85\b/,
      /\b0,0038\b/,
      /\b126\s+celdas\b/i,
      /\b(?:la ca[ií]da|el descenso)\s+en\s+IP\/CFT\s+(?:demuestra|prueba|confirma)\s+(?:una\s+)?p[eé]rdida\s+neta\s+de\s+acceso\b/i,
      /\b(?:vemos|dejamos|entremos|detengámonos|separamos|llegamos|nuestro|nuestra|nuestros|nuestras)\b|\bnos\s+(?:da|queda)\b/i
    ],
    "en" => [
      /\b(?:closing a high school|school closure|school closures)\s+causally\s+(?:destroys?|reduces?|cuts?)\s+13[,.]24\b/i,
      /\bthe overall average causal effect\s+is\s+[−-]13[,.]24\b/i,
      /\bused\s+DEMRE\s+2014[–-]2020\s+microdata\b/i,
      /[−-]1\.43\b/,
      /[−-]2\.85\b/,
      /\b0\.0038\b/,
      /\b126\s+cells\b/i,
      /\b(?:the\s+)?(?:fall|decline)\s+in\s+IP\/CFT\s+(?:proves|shows|confirms)\s+(?:a\s+)?net\s+loss\s+of\s+access\b/i,
      /\b(?:we|our|us)\b/i
    ]
  }.freeze

  def initialize(root:)
    @root = Pathname(root).expand_path
    @causal = load_json(CAUSAL_ARTIFACT)
    @retro = load_json(RETRO_ARTIFACT)
    validate_artifacts!
  end

  def verify(fixture: nil, lang: nil)
    raise ThesisPost4UsageError, "idioma inválido: #{lang}" if lang && !FILES.key?(lang)
    validate_fixture_scope!(fixture, lang)
    languages = lang ? [lang] : FILES.keys
    documents = FILES.slice(*languages).transform_values { |relative| read_document(@root.join(relative)) }
    annexes = ANNEXES.slice(*languages).transform_values { |relative| read_document(@root.join(relative)) }
    inject_fixture!(documents, annexes, fixture) if fixture
    lang ? verify_identity_single(lang, documents.fetch(lang)) : verify_identity(documents)
    languages.each { |locale| raise ThesisPost4Error, "anexo metodológico ausente #{locale}" unless annexes.key?(locale) }
    documents.each { |lang, document| verify_document(lang, document, annexes.fetch(lang)) }
    verify_pair(documents, annexes) unless lang
    true
  end

  private

  def validate_fixture_scope!(fixture, lang)
    return unless fixture && lang

    if BILINGUAL_ONLY_FIXTURES.include?(fixture)
      raise ThesisPost4UsageError, "fixture requiere comparación bilingüe: #{fixture}"
    end
    expected_lang = EN_ONLY_FIXTURES.include?(fixture) ? "en" : "es"
    return if expected_lang == lang

    raise ThesisPost4UsageError, "fixture #{fixture} requiere --lang #{expected_lang} o modo bilingüe"
  end

  def load_json(relative)
    path = @root.join(relative)
    raise ThesisPost4Error, "artefacto científico ausente: #{path}" unless path.file?

    JSON.parse(path.read(encoding: "UTF-8"))
  rescue JSON::ParserError => e
    raise ThesisPost4Error, "JSON inválido en #{relative}: #{e.message}"
  end

  def validate_artifacts!
    unless @causal["status"] == "ESTIMATED_ECONOMETRICS_AND_CAUSAL_ML_VERIFIED" &&
           @causal["schema_version"] == "post4-higher-education-causal-ml-v1.0"
      raise ThesisPost4Error, "contrato de artefacto causal Post IV inválido"
    end
    rv_row = @causal.dig("track_c_causal_ml", "orthogonal_r_learner_heterogeneity", "full_student_and_school_g5_controls", "ipcft_two_year", "cinelli_hazlett_ovb")
    unless rv_row && rv_row["robustness_value_q1_pct"] > rv_row["robustness_value_q1_alpha05_pct"]
      raise ThesisPost4Error, "RV_q1 y RV_alpha05 invertidos en artefacto causal Post IV"
    end
    unless @retro["schema_version"] == "post4-retrospective-post3-v1" &&
           @retro.dig("privacy", "contains_student_identifiers") == false
      raise ThesisPost4Error, "contrato de auditoría retrospectiva Post III inválido"
    end
  end

  def read_document(path)
    raise ThesisPost4Error, "borrador ausente: #{path}" unless path.file?

    source = path.read(encoding: "UTF-8")
    match = source.match(/\A---\s*\n(.*?)\n---\s*\n(.*)\z/m)
    raise ThesisPost4Error, "front matter ausente: #{path}" unless match

    front = YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: true)
    Post4Document.new(path:, front_matter: front, body: match[2])
  end

  def localized_integer(value, lang)
    value.to_i.to_s.reverse.scan(/.{1,3}/).join(lang == "es" ? "." : ",").reverse
  end

  def localized_decimal(value, lang, decimals: 2)
    v = Float(value)
    adj = v >= 0 ? v + 1e-9 : v - 1e-9
    formatted = format("%.#{decimals}f", adj)
    lang == "es" ? formatted.tr(".", ",") : formatted
  end

  def localized_signed(value, lang, scale: 1, decimals: 2)
    v = Float(value) * scale
    adj = v >= 0 ? v + 1e-9 : v - 1e-9
    number = format("%+.#{decimals}f", adj).tr("-", "−")
    lang == "es" ? number.tr(".", ",") : number
  end

  def assert_match!(body, pattern, message)
    raise ThesisPost4Error, message unless body.match?(pattern)
  end

  def verify_identity(documents)
    fronts = documents.values.map(&:front_matter)
    unless fronts.map { |front| front["lang"] }.sort == %w[en es]
      raise ThesisPost4Error, "par de idiomas incompleto"
    end
    unless fronts.map { |front| front["ref"] }.uniq == ["cierre-escolar-educacion-superior-causal-ml"]
      raise ThesisPost4Error, "ref bilingüe divergente"
    end
    raise ThesisPost4Error, "fecha bilingüe divergente" unless fronts.map { |front| front["date"] }.uniq.length == 1
    unless fronts.map { |front| front["permalink"] }.uniq ==
           ["/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/"]
      raise ThesisPost4Error, "permalink bilingüe divergente"
    end
  end

  def verify_identity_single(lang, document)
    front = document.front_matter
    unless front["lang"] == lang && front["ref"] == "cierre-escolar-educacion-superior-causal-ml" &&
           front["permalink"] == "/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/"
      raise ThesisPost4Error, "identidad de artículo inválida #{lang}"
    end
  end

  def verify_document(lang, document, annex)
    front = document.front_matter
    main = document.body
    appendix = annex.body
    body = "#{main}\n\n#{appendix}"

    verify_front_matter(lang, front)
    verify_annex_identity(lang, front, annex.front_matter)
    verify_scientific_state(lang, main)
    verify_didactic_structure(lang, main, appendix)
    verify_core_numbers(lang, body)
    verify_figures(lang, body)
    verify_references(lang, main, appendix)
    verify_forbidden_content(lang, body, front)
    verify_visible_length(lang, main, appendix)
  end

  def verify_annex_identity(lang, post, annex)
    expected_ref = "tesis-post4-anexo-metodologico"
    expected_route = "#{post.fetch('permalink')}anexo-metodologico/"
    unless annex["layout"] == "single" && annex["lang"] == lang &&
           annex["ref"] == expected_ref && annex["ref"] != post["ref"] &&
           annex["permalink"] == expected_route
      raise ThesisPost4Error, "identidad o ruta del anexo inválida #{lang}"
    end
    raise ThesisPost4Error, "anexo sin clase de evidencia #{lang}" unless Array(annex["classes"]).include?("post3-evidence")
    raise ThesisPost4Error, "contrato explícito de tablas ausente en anexo #{lang}" unless annex["table_contract"] == "explicit-v1"
  end

  def verify_front_matter(lang, front)
    unless front.dig("distribution", "social") == true && front.dig("distribution", "republish") == []
      raise ThesisPost4Error, "estado de distribución inesperado #{lang}"
    end
    unless front["editorial_contract"] == "societal-contribution-v1"
      raise ThesisPost4Error, "contrato editorial ausente #{lang}"
    end
    unless front["table_contract"] == "explicit-v1"
      raise ThesisPost4Error, "contrato de tablas ausente #{lang}"
    end
    unless front["math"] == true
      raise ThesisPost4Error, "math: true obligatorio para KaTeX en #{lang}"
    end
    unless Array(front["classes"]).include?("post3-evidence")
      raise ThesisPost4Error, "clase post3-evidence obligatoria en #{lang}"
    end
    unless front.dig("ai_disclosure", "level") == "some_ai"
      raise ThesisPost4Error, "ai_disclosure ausente o inválido #{lang}"
    end
  end

  def verify_scientific_state(lang, body)
    state_marker = "<!-- scientific-state: #{REQUIRED_ANALYSIS_STAGE}; result: #{REQUIRED_RESULT_STATE} -->"
    readiness_marker = "<!-- publication-readiness: #{REQUIRED_READINESS} -->"
    raise ThesisPost4Error, "estado científico Post IV ausente o duplicado #{lang}" unless body.scan(state_marker).length == 1
    raise ThesisPost4Error, "estado de publicación Post IV ausente o duplicado #{lang}" unless body.scan(readiness_marker).length == 1

    state_comments = body.scan(/<!--\s*scientific-state:.*?-->/m)
    readiness_comments = body.scan(/<!--\s*publication-readiness:.*?-->/m)
    unless state_comments == [state_marker] && readiness_comments == [readiness_marker]
      raise ThesisPost4Error, "marcador científico o editorial contradictorio #{lang}"
    end
  end

  def verify_didactic_structure(lang, body, appendix)
    headings = if lang == "es"
                 [
                   /^## Cucharada 1:/,
                   /^## Cucharada 2:/,
                   /^## Cucharada 3:/,
                   /^## Cierre:/,
                   /^## Referencias\s*$/
                 ]
               else
                 [
                   /^## Spoonful 1:/,
                   /^## Spoonful 2:/,
                   /^## Spoonful 3:/,
                   /^## Closing:/,
                   /^## References\s*$/
                 ]
               end
    headings.each do |pattern|
      assert_match!(body, pattern, "estructura de 3 cucharadas + cierre incompleta #{lang}: #{pattern.inspect}")
    end

    reader_label = /\bELI5\b|\b(?:En simple|In simple terms|Simply put|Put simply)\s*:/i
    raise ThesisPost4Error, "rótulo ELI5 o En simple expuesto #{lang}" if "#{body}\n#{appendix}".match?(reader_label)
    raise ThesisPost4Error, "detalle metodológico embebido #{lang}" if body.match?(/<details\b[^>]*class="post3-methods"/i)
    primary = body.scan(/<aside\b[^>]*class="notice--primary"[^>]*markdown="1"/i).length
    raise ThesisPost4Error, "resumen editorial único ausente #{lang}" unless primary == 1 && body.scan(/<aside\b/i).length == 1
    raise ThesisPost4Error, "navegación de serie ausente #{lang}" unless body.include?("{% include thesis-series-nav.html current=4 %}")
    raise ThesisPost4Error, "navegación de anexo ausente #{lang}" unless appendix.include?("{% include thesis-series-nav.html current=4 %}")
    { "artículo" => body, "anexo" => appendix }.each do |part, text|
      raise ThesisPost4Error, "etiquetas details desbalanceadas #{lang} en #{part}" unless details_balanced?(text)
    end

    display_math_blocks = appendix.scan(/^\s*\$\$\n.+?\n\s*\$\$/m).length
    raise ThesisPost4Error, "ecuaciones metodológicas en anexo insuficientes #{lang}: #{display_math_blocks}" if display_math_blocks < 4

    math_spans = "#{body}\n#{appendix}".scan(/\$\$(.+?)\$\$/m).flatten
    if math_spans.any? { |span| span.include?(",") || span.include?("\\text{ %}") }
      raise ThesisPost4Error, "coma o \\text{ %} dentro de $$...$$ en #{lang}"
    end

    raise ThesisPost4Error, "símbolo de grado (°) en lugar de ordinal (º) en #{lang}" if "#{body}\n#{appendix}".include?("°")

    if "#{body}\n#{appendix}".scan(/<figcaption>.*?<\/figcaption>/mi).any? { |cap| cap.include?("$$") }
      raise ThesisPost4Error, "no usar $$ dentro de <figcaption> HTML crudo (Kramdown no lo procesa) #{lang}"
    end

    # El artículo y las tablas/leyendas deben leerse como prosa. El anexo puede
    # mostrar identificadores del JSON público para que una cifra sea rastreable;
    # cada identificador queda limitado a su párrafo de enlace público.
    inline_backticks = body.scan(/`[^`\n]+`/).length
    appendix.lines.each do |line|
      codes = line.scan(/`([^`\n]+)`/).flatten
      next if codes.empty?

      authorized = line.match?(/\bJSON\b/i) && line.include?("post4_higher_education_causal_ml_v1.json") &&
                   !line.lstrip.start_with?("|") && !line.include?("<figcaption") &&
                   codes.all? { |code| code.match?(/\A[a-z][a-z0-9_.]*\z/i) && public_json_path_exists?(code) }
      inline_backticks += codes.length unless authorized
    end
    raise ThesisPost4Error, "uso de código inline (`...`) en prosa/tablas contamina el tema claro #{lang}: #{inline_backticks} ocurrencias" if inline_backticks.positive?

    adr_compliance = /ADR-188/
    assert_match!(appendix, adr_compliance, "declaración de cumplimiento ADR-188 ausente del anexo #{lang}")
  end

  def details_balanced?(text)
    depth = 0
    text.scan(%r{</?details\b[^>]*>}i).each do |tag|
      depth += tag.start_with?("</") ? -1 : 1
      return false if depth.negative?
    end
    depth.zero?
  end

  def public_json_path_exists?(path)
    parts = path.split(".")
    walk = lambda do |node, remaining|
      return true if remaining.empty?
      case node
      when Hash
        return true if node.key?(remaining.first) && walk.call(node.fetch(remaining.first), remaining.drop(1))

        node.values.any? { |value| walk.call(value, remaining) }
      when Array
        node.any? { |value| walk.call(value, remaining) }
      else
        false
      end
    end
    walk.call(@causal, parts)
  end

  def verify_core_numbers(lang, body)
    c_mod = @causal.fetch("track_c_causal_ml")
    ab_mod = @causal.fetch("track_a_and_b_econometrics")

    sec_rung1 = localized_signed(c_mod.dig("selection_purging_ladder", "secondary", "steps", "step1_demographics_only", "plr_hgb_pp"), lang, scale: 1)
    sec_rung2 = localized_signed(c_mod.dig("selection_purging_ladder", "secondary", "steps", "step2_plus_student_academic_g1_g2", "plr_hgb_pp"), lang, scale: 1)
    sec_did = localized_signed(ab_mod.dig("primary_2016_2019_repeated_cohort_did", "secondary", "outcomes", "any_he_two_year", "estimate_pp"), lang, scale: 1)
    sec_rung3b = localized_signed(c_mod.dig("selection_purging_ladder", "secondary", "steps", "step3_plus_school_pre_g5_history", "plr_hgb_pp"), lang, scale: 1)
    sec_ipcft = localized_signed(c_mod.dig("orthogonal_r_learner_heterogeneity", "full_student_and_school_g5_controls", "ipcft_two_year", "blp", "ate_beta1_pp"), lang, scale: 1)
    ub_did = localized_signed(ab_mod.dig("primary_2016_2019_repeated_cohort_did", "basic", "outcomes", "any_he_two_year", "estimate_pp"), lang, scale: 1)
    ub_dml = localized_signed(c_mod.dig("selection_purging_ladder", "basic", "steps", "step3_plus_school_pre_g5_history", "plr_hgb_pp"), lang, scale: 1)

    gate_g1_he = localized_signed(c_mod.dig("orthogonal_r_learner_heterogeneity", "student_academic_baseline_controls", "any_he_two_year", "gates_by_quintile", "G1_most_harmed", "gate_pp"), lang, scale: 1)
    gate_g1_ipcft = localized_signed(c_mod.dig("orthogonal_r_learner_heterogeneity", "student_academic_baseline_controls", "ipcft_two_year", "gates_by_quintile", "G1_most_harmed", "gate_pp"), lang, scale: 1)
    gate_g1_pers = localized_signed(c_mod.dig("orthogonal_r_learner_heterogeneity", "student_academic_baseline_controls", "persist_2yr", "gates_by_quintile", "G1_most_harmed", "gate_pp"), lang, scale: 1)

    m_star_point = localized_decimal(@retro.dig("honest_did_rambachan_roth_2023", "grade_progression_or_lag", "breakdown_m_star", "rm_point_zero"), lang, decimals: 2)
    m_star_ci = localized_decimal(@retro.dig("honest_did_rambachan_roth_2023", "grade_progression_or_lag", "breakdown_m_star", "rm_honest_upper95_zero"), lang, decimals: 2)
    stayer_est = localized_signed(@retro.dig("g_minus_2_anticipation_anchor", "outcomes", "grade_progression_or_lag", "anchored_g_minus_2_stayers", "estimate"), lang, scale: 100)
    switcher_est = localized_signed(@retro.dig("g_minus_2_anticipation_anchor", "outcomes", "grade_progression_or_lag", "late_entrants_switched_m2_to_m1", "estimate"), lang, scale: 100)

    d1_not_d2_rate = localized_decimal(ab_mod.dig("pooled_2009_2022_d2_vs_d1", "secondary", "d1_minus_d2_flow_alert_absorptions", "treated_post_he_2yr_pct"), lang, decimals: 2)
    ub_cells = localized_integer(ab_mod.dig("primary_2016_2019_repeated_cohort_did", "basic", "supported_cells"), lang)
    pre_grad_did = localized_signed(ab_mod.dig("longitudinal_2009_2022_by_regime", 0, "did_graduation_by_2025", "estimate_pp"), lang, scale: 1)

    required_tokens = [
      sec_rung1,
      sec_rung2,
      sec_did,
      sec_rung3b,
      sec_ipcft,
      ub_did,
      ub_dml,
      gate_g1_he,
      gate_g1_ipcft,
      gate_g1_pers,
      m_star_point,
      m_star_ci,
      stayer_est,
      switcher_est,
      d1_not_d2_rate,
      ub_cells,
      pre_grad_did,
      localized_integer(1_678, lang),
      localized_integer(38_525, lang),
      localized_integer(29_218, lang),
      localized_integer(79_709_054, lang),
      localized_integer(73_873_835, lang)
    ]

    missing = required_tokens.reject { |token| body.include?(token) }
    raise ThesisPost4Error, "cifras gobernadas ausentes #{lang}: #{missing.join(', ')}" unless missing.empty?
  end

  def verify_figures(lang, body)
    CANONICAL_FIGURES.each do |family|
      reference = %r{/assets/images/tesis-post4/#{Regexp.escape(family)}-#{lang}-(?:light|dark)}
      assert_match!(body, reference, "figura canónica no referenciada #{lang}: #{family}")

      figure = body.scan(/<figure\b.*?<\/figure>/mi).find { |block| block.match?(reference) }
      raise ThesisPost4Error, "bloque de figura canónica ausente #{lang}: #{family}" unless figure

      visual_contract = [
        /<img\b[^>]*class="[^"]*\bpost3-theme-image\b[^"]*"/i,
        /<a\b[^>]*data-light-href="[^"]*#{Regexp.escape(family)}-#{lang}-light\.svg/i,
        /<a\b[^>]*data-dark-href="[^"]*#{Regexp.escape(family)}-#{lang}-dark\.svg/i,
        /data-light-src="[^"]*#{Regexp.escape(family)}-#{lang}-light\.svg/i,
        /data-dark-src="[^"]*#{Regexp.escape(family)}-#{lang}-dark\.svg/i,
        /data-light-srcset="[^"]*#{Regexp.escape(family)}-#{lang}-light-mobile\.svg/i,
        /data-dark-srcset="[^"]*#{Regexp.escape(family)}-#{lang}-dark-mobile\.svg/i,
        %r{/assets/images/tesis-post4/#{Regexp.escape(family)}-data\.csv},
        lang == "es" ? /<figcaption>.*\bFuente:/mi : /<figcaption>.*\bSource:/mi
      ]
      unless visual_contract.all? { |pattern| figure.match?(pattern) }
        raise ThesisPost4Error, "contrato visual de figura incompleto #{lang}: #{family}"
      end

      FIGURE_VARIANTS.product(FIGURE_FORMATS).each do |variant, format|
        relative = "assets/images/tesis-post4/#{family}-#{lang}-#{variant}.#{format}"
        raise ThesisPost4Error, "variante de figura ausente: #{relative}" unless @root.join(relative).file?
      end
      csv_relative = "assets/images/tesis-post4/#{family}-data.csv"
      raise ThesisPost4Error, "CSV accesible de figura ausente: #{csv_relative}" unless @root.join(csv_relative).file?
    end
  end

  def footnote_parts(body)
    heading = body.match(/^## (?:Referencias|References)\s*$/)
    raise ThesisPost4Error, "sección de referencias ausente" unless heading

    text = body[0...heading.begin(0)]
    refs = body[heading.end(0)..]
    definitions = refs.scan(/^\[\^([^\]]+)\]:\s*(.+)$/)
    # Una cita inline seguida de dos puntos sigue siendo uso; solo una línea
    # anclada al inicio bajo Referencias puede definir la nota.
    [text.scan(/\[\^([^\]]+)\]/).flatten, definitions]
  end

  def verify_references(lang, main, appendix)
    all_definitions = [main, appendix].flat_map do |part|
      marks, definitions = footnote_parts(part)
      keys = definitions.map(&:first)
      raise ThesisPost4Error, "referencias sin formato de nota #{lang}" if keys.empty?
      raise ThesisPost4Error, "clave de nota duplicada #{lang}" unless keys.uniq.length == keys.length
      orphans = keys - marks
      raise ThesisPost4Error, "nota sin cita en el texto #{lang}: #{orphans.join(', ')}" unless orphans.empty?
      missing = marks.uniq - keys
      raise ThesisPost4Error, "cita sin nota #{lang}: #{missing.join(', ')}" unless missing.empty?
      definitions
    end
    definitions_by_key = all_definitions.group_by(&:first)
    raise ThesisPost4Error, "conjunto bibliográfico incompleto #{lang}: #{definitions_by_key.length}" unless definitions_by_key.length == 27
    definitions_by_key.each do |key, entries|
      raise ThesisPost4Error, "referencia contradictoria #{lang}: #{key}" unless entries.map(&:last).uniq.length == 1
    end
    dois = all_definitions.map(&:last).join("\n").scan(%r{https://doi\.org/([^\s)\]"<]+)}i).flatten.map(&:downcase).uniq
    raise ThesisPost4Error, "bibliografía insuficiente #{lang}: #{dois.length} DOI" if dois.length < 12

    responsive_tables = [main, appendix].sum { |part| part.scan("{: .table--compact .table--scroll}").length }
    raise ThesisPost4Error, "tablas responsivas incompletas #{lang}: #{responsive_tables}" unless responsive_tables == 6
  end

  def verify_forbidden_content(lang, body, front)
    public_text = "#{public_metadata(front)}\n#{body}"
    FORBIDDEN_NAIVE_PROMOTIONS.fetch(lang).each do |pattern|
      if public_text.match?(pattern)
        raise ThesisPost4Error, "promoción causal ingenua o violación normativa #{lang}: #{pattern.inspect}"
      end
    end

    identifier_pattern = /\b(?:MRUN|RUN|RUT|RBD)\s*(?:N[.º°o]?\s*)?\d{2,}\b/i
    raise ThesisPost4Error, "identificador individual/escolar prohibido #{lang}" if public_text.match?(identifier_pattern)
    raise ThesisPost4Error, "ruta privada prohibida #{lang}" if public_text.match?(PRIVATE_PATH_PATTERN)
  end

  def public_metadata(front)
    PUBLIC_METADATA_KEYS.flat_map { |key| Array(front[key]) }.compact.join("\n")
  end

  def verify_visible_length(lang, main, appendix)
    article = main.sub(/\n## (?:Referencias|References)\n.*/m, "")
    words = visible_word_count(article)
    unless MAIN_WORD_RANGE.cover?(words)
      raise ThesisPost4Error, "extensión visible #{lang.upcase} fuera de #{MAIN_WORD_RANGE}: #{words}"
    end

    appendix_words = visible_word_count(appendix.sub(/\n## (?:Referencias|References)\n.*/m, ""))
    unless APPENDIX_WORD_RANGE.cover?(appendix_words)
      raise ThesisPost4Error, "apéndice metodológico fuera de #{APPENDIX_WORD_RANGE} #{lang}: #{appendix_words}"
    end
  end

  def visible_word_count(text)
    text.gsub(/<!--.*?-->/m, " ").gsub(/<[^>]+>/, " ").gsub(/\[\^[^\]]+\]/, " ")
        .gsub(/\{:[^}]+\}/, " ").gsub(/\{\{.*?\}\}/, " ")
        .gsub(/[|#*_>`~-]/, " ")
        .scan(/[[:alpha:]À-ÿ0-9]+/).length
  end

  def verify_pair(documents, annexes)
    spanish = "#{documents.fetch('es').body}\n#{annexes.fetch('es').body}"
    english = "#{documents.fetch('en').body}\n#{annexes.fetch('en').body}"
    es_tables = spanish.scan(/^\|/).length
    en_tables = english.scan(/^\|/).length
    raise ThesisPost4Error, "número de filas de tablas divergente (#{es_tables} vs #{en_tables})" unless es_tables == en_tables

    es_dois = spanish.scan(%r{https://doi\.org/([^\s)\]"<]+)}i).flatten.map(&:downcase).uniq.sort
    en_dois = english.scan(%r{https://doi\.org/([^\s)\]"<]+)}i).flatten.map(&:downcase).uniq.sort
    raise ThesisPost4Error, "referencias bilingües divergentes" unless es_dois == en_dois

    es_marks = [documents.fetch('es'), annexes.fetch('es')].flat_map { |doc| footnote_parts(doc.body).first }
    en_marks = [documents.fetch('en'), annexes.fetch('en')].flat_map { |doc| footnote_parts(doc.body).first }
    es_definitions = [documents.fetch('es'), annexes.fetch('es')].flat_map { |doc| footnote_parts(doc.body).last }
    en_definitions = [documents.fetch('en'), annexes.fetch('en')].flat_map { |doc| footnote_parts(doc.body).last }
    unless es_definitions.map(&:first).uniq.sort == en_definitions.map(&:first).uniq.sort && es_marks.uniq.sort == en_marks.uniq.sort
      raise ThesisPost4Error, "notas bilingües divergentes"
    end

    figure_families = lambda do |body|
      body.scan(%r{/assets/images/tesis-post4/([a-z0-9-]+)-(?:es|en)-(?:light|dark)}).flatten.uniq.sort
    end
    unless figure_families.call(spanish) == figure_families.call(english)
      raise ThesisPost4Error, "familias de figuras bilingües divergentes"
    end

    verify_numeric_pairing(spanish, english)
  end

  def localized_numeric_tokens(text, lang)
    cleaned = text.gsub("{,}", lang == "es" ? "," : ".")
    cleaned.scan(/(?<![[:alnum:]])[+−-]?(?:\d{1,3}(?:[.,]\d{3})+|\d+)(?:[.,]\d+)?(?![[:alnum:]])/).map do |token|
      normalized = token.tr("−", "-").delete_prefix("+")
      normalized = lang == "es" ? normalized.delete(".").tr(",", ".") : normalized.delete(",")
      integer, decimal = normalized.split(".", 2)
      decimal = decimal&.sub(/0+\z/, "")
      decimal.nil? || decimal.empty? ? integer.to_i.to_s : "#{integer.to_i}.#{decimal}"
    end
  end

  def verify_numeric_pairing(spanish, english)
    table_blocks = lambda { |body| body.scan(/(?:^\|.*(?:\n|\z))+/) }
    es_tables = table_blocks.call(spanish)
    en_tables = table_blocks.call(english)
    unless es_tables.length == en_tables.length
      raise ThesisPost4Error, "cantidad de tablas bilingües divergente"
    end
    es_tables.zip(en_tables).each_with_index do |(es, en), idx|
      es_tok = localized_numeric_tokens(es, "es")
      en_tok = localized_numeric_tokens(en, "en")
      unless es_tok == en_tok
        raise ThesisPost4Error, "cifras de tabla #{idx + 1} bilingües divergentes: ES=#{es_tok.inspect} vs EN=#{en_tok.inspect}"
      end
    end

    figure_blocks = lambda { |body| body.scan(/<figure\b.*?<\/figure>/mi) }
    es_figures = figure_blocks.call(spanish)
    en_figures = figure_blocks.call(english)
    unless es_figures.length == en_figures.length
      raise ThesisPost4Error, "cantidad de figuras bilingües divergente"
    end
    es_figures.zip(en_figures).each_with_index do |(es, en), idx|
      es_tok = localized_numeric_tokens(es, "es")
      en_tok = localized_numeric_tokens(en, "en")
      unless es_tok == en_tok
        raise ThesisPost4Error, "cifras de figura #{idx + 1} bilingües divergentes: ES=#{es_tok.inspect} vs EN=#{en_tok.inspect}"
      end
    end
  end

  def replace_all!(documents, lang, pattern, replacement, fixture)
    document = documents.fetch(lang)
    changed = document.body.gsub(pattern, replacement)
    raise ThesisPost4Error, "fixture no pudo aplicarse: #{fixture}" if changed == document.body

    documents[lang] = document.with(body: changed)
  end

  def replace_all_across!(documents, annexes, lang, pattern, replacement, fixture)
    changed_any = false
    [documents, annexes].each do |collection|
      document = collection.fetch(lang)
      changed = document.body.gsub(pattern, replacement)
      next if changed == document.body
      changed_any = true
      collection[lang] = document.with(body: changed)
    end
    raise ThesisPost4Error, "fixture no pudo aplicarse: #{fixture}" unless changed_any
  end

  def inject_fixture!(documents, annexes, fixture)
    case fixture
    when "annex-removed"
      annexes.delete("es")
    when "annex-table-contract-drop"
      document = annexes.fetch("es")
      annexes["es"] = document.with(front_matter: document.front_matter.reject { |key, _| key == "table_contract" })
    when "net-access-promotion"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nLa caída en IP/CFT demuestra una pérdida neta de acceso.\n")
    when "causal-naive-promotion"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nCerrar un liceo destruye causalmente 13,24 puntos.\n")
    when "privacy-path"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nRuta privada: /home/ende/secret.parquet\n")
    when "school-identifier"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nEl colegio RBD 8512 cerró.\n")
    when "state-drift"
      replace_all!(documents, "es", REQUIRED_RESULT_STATE, "UNVERIFIED_STATE", fixture)
    when "primary-number-drift"
      replace_all_across!(documents, annexes, "es", /−2,09/, "−9,99", fixture)
    when "figure-contract-drift"
      replace_all!(documents, "en", /data-dark-srcset=/, "data-dark-srcset-broken=", fixture)
    when "footnote-orphan"
      replace_all_across!(documents, annexes, "es", /\[\^manski2003\](?!:)/, "", fixture)
    when "table-parity-drift"
      replace_all!(documents, "en", /\+0\.634/, "+0.999", fixture)
    when "demre-2014-violation"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nSe utilizaron microdatos DEMRE 2014-2020.\n")
    when "math-comma-or-percent"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\n$$43,7\\text{ %}$$\n")
    when "first-person-plural"
      document = documents.fetch("en")
      documents["en"] = document.with(body: "#{document.body}\nHere we see our main result.\n")
    when "unbacked-number-drift"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nLa caída fue de −2,85 pp con p = 0,0038 en 126 celdas.\n")
    when "inline-code-article"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nEl `resultado` tiene una interpretación prudente.\n")
    when "inline-code-unscoped-annex"
      document = annexes.fetch("es")
      annexes["es"] = document.with(body: "#{document.body}\nLa ruta `resultado_no_publicado` queda sin respaldo público.\n")
    when "inline-code-fake-json-key"
      document = annexes.fetch("es")
      annexes["es"] = document.with(body: "#{document.body}\nEl JSON público [JSON]({{ '/assets/data/tesis-post4/post4_higher_education_causal_ml_v1.json' | relative_url }}) declara `nonexistent_key`.\n")
    when "eli5-label-annex"
      document = annexes.fetch("es")
      annexes["es"] = document.with(body: "#{document.body}\nEn simple: explicación del resultado.\n")
    when "orphan-details-close"
      document = annexes.fetch("es")
      annexes["es"] = document.with(body: "#{document.body}\n</details>\n")
    when "colon-citation-missing-definition"
      document = documents.fetch("es")
      marker = "\n## Referencias\n"
      raise ThesisPost4Error, "fixture no pudo aplicarse: #{fixture}" unless document.body.include?(marker)

      documents["es"] = document.with(body: document.body.sub(marker, "\nCita pendiente[^guard_colon_missing]: contexto.\n#{marker}"))
    else
      raise ThesisPost4UsageError, "fixture desconocida: #{fixture}"
    end
  end
end

if $PROGRAM_NAME == __FILE__
  begin
    fixture = nil
    lang = nil
    ARGV.each_slice(2) do |flag, value|
      raise ThesisPost4UsageError, "argumento inválido: #{flag}" unless %w[--fixture --lang].include?(flag) && value
      flag == "--fixture" ? fixture = value : lang = value
    end

    root = Pathname(__dir__).parent
    verifier = ThesisPost4Verifier.new(root:)
    verifier.verify(fixture:, lang:)
    puts "THESIS_POST4_VERIFIED lang=#{lang || 'both'} fixture=#{fixture || 'none'}"
  rescue ThesisPost4UsageError => e
    warn "THESIS_POST4_USAGE_ERROR: #{e.message}"
    exit 2
  rescue ThesisPost4Error => e
    warn "THESIS_POST4_INVALID: #{e.message}"
    exit 1
  end
end
