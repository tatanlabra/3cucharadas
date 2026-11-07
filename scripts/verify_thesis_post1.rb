#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "digest"
require "json"
require "pathname"
require "yaml"

class ThesisPost1Error < StandardError; end

Post1Document = Data.define(:path, :front_matter, :body)

class ThesisPost1Verifier
  FILES = {
    "es" => "_posts/2026-08-29-replica-tesis-establecimientos-educacionales.md",
    "en" => "_posts/2026-08-29-replica-tesis-establecimientos-educacionales-en.md"
  }.freeze
  UPGRADES_ARTIFACT = "assets/data/tesis-post4/trilogy_econometric_upgrades_v1.json"
  CAROUSEL_DATA = "_data/thesis_recreation_face_to_face.yml"
  MAIN_WORD_RANGE = (3_500..6_500).freeze
  PUBLIC_METADATA_KEYS = %w[title subtitle description excerpt tags categories].freeze
  PRIVATE_PATH_PATTERN = %r{/(?:home|mnt|opt|run|tmp)/}i

  FORBIDDEN_CAUSAL_PROMOTIONS = {
    "es" => [
      /\bla tesis demuestra causalmente que la competencia\b/i,
      /\bel modelo cloglog identifica el efecto causal\b/i,
      /\b1\.677\s+cierres\b/i,
      /\b295\s+en\s+2016[–-]2025\b/i
    ],
    "en" => [
      /\bthe thesis causally demonstrates that competition\b/i,
      /\bthe cloglog model identifies the causal effect\b/i,
      /\b1,677\s+clean\b/i,
      /\b295\s+in\s+2016[–-]2025\b/i
    ]
  }.freeze

  def initialize(root:)
    @root = Pathname(root).expand_path
    @upgrades = load_json(UPGRADES_ARTIFACT)
    @carousel = YAML.safe_load(@root.join(CAROUSEL_DATA).read(encoding: "UTF-8"), permitted_classes: [Date, Time], aliases: true)
    validate_artifacts!
  end

  def verify(fixture: nil)
    documents = FILES.transform_values { |relative| read_document(@root.join(relative)) }
    inject_fixture!(documents, fixture) if fixture
    verify_identity(documents)
    documents.each { |lang, document| verify_document(lang, document) }
    verify_pair(documents)
    true
  end

  private

  def load_json(relative)
    path = @root.join(relative)
    raise ThesisPost1Error, "artefacto científico ausente: #{path}" unless path.file?

    JSON.parse(path.read(encoding: "UTF-8"))
  rescue JSON::ParserError => e
    raise ThesisPost1Error, "JSON inválido en #{relative}: #{e.message}"
  end

  def validate_artifacts!
    unless @upgrades["schema_version"] == "trilogy-econometric-upgrades-v1" &&
           @upgrades.dig("privacy", "contains_student_identifiers") == false
      raise ThesisPost1Error, "contrato de artefacto trilogy_econometric_upgrades_v1 inválido"
    end
    unless @carousel.dig("technical", "causal_boundary") == "ASSOCIATIONAL_ONLY"
      raise ThesisPost1Error, "contrato de carrusel Post I inválido"
    end
  end

  def read_document(path)
    raise ThesisPost1Error, "post ausente: #{path}" unless path.file?

    source = path.read(encoding: "UTF-8")
    match = source.match(/\A---\s*\n(.*?)\n---\s*\n(.*)\z/m)
    raise ThesisPost1Error, "front matter ausente: #{path}" unless match

    front = YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: true)
    Post1Document.new(path:, front_matter: front, body: match[2])
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
    raise ThesisPost1Error, message unless body.match?(pattern)
  end

  def verify_identity(documents)
    fronts = documents.values.map(&:front_matter)
    unless fronts.map { |front| front["lang"] }.sort == %w[en es]
      raise ThesisPost1Error, "par de idiomas incompleto"
    end
    unless fronts.map { |front| front["ref"] }.uniq == ["replica-tesis-establecimientos-educacionales"]
      raise ThesisPost1Error, "ref bilingüe divergente"
    end
    raise ThesisPost1Error, "fecha bilingüe divergente" unless fronts.map { |front| front["date"] }.uniq.length == 1
    unless fronts.map { |front| front["permalink"] }.uniq ==
           ["/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/"]
      raise ThesisPost1Error, "permalink bilingüe divergente"
    end
  end

  def verify_document(lang, document)
    front = document.front_matter
    body = document.body

    verify_front_matter(lang, front)
    verify_didactic_structure(lang, body)
    verify_core_numbers(lang, body)
    verify_references(lang, body)
    verify_forbidden_content(lang, body, front)
    verify_visible_length(lang, body)
  end

  def verify_front_matter(lang, front)
    unless front.dig("distribution", "social") == true && front.dig("distribution", "republish") == []
      raise ThesisPost1Error, "estado de distribución inesperado #{lang}"
    end
    unless front["editorial_contract"] == "societal-contribution-v1"
      raise ThesisPost1Error, "contrato editorial societal-contribution-v1 ausente #{lang}"
    end
    unless front["table_contract"] == "explicit-v1"
      raise ThesisPost1Error, "contrato de tablas explicit-v1 ausente #{lang}"
    end
    unless front["math"] == true
      raise ThesisPost1Error, "math: true obligatorio para KaTeX en #{lang}"
    end
    unless Array(front["classes"]).include?("thesis-recreation-post")
      raise ThesisPost1Error, "clase thesis-recreation-post obligatoria en #{lang}"
    end
    unless front.dig("ai_disclosure", "level") == "some_ai"
      raise ThesisPost1Error, "ai_disclosure ausente o inválido #{lang}"
    end
  end

  def verify_didactic_structure(lang, body)
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

    callout_notes = body.scan(/<aside class="notice--info" markdown="1">/).length
    raise ThesisPost1Error, "notas metodológicas destacadas (<aside class=\"notice--info\">) insuficientes #{lang}: #{callout_notes}" if callout_notes < 2

    assert_match!(body, /\{%\s*include\s+evidence-carousel\.html\s*%\}/, "include evidence-carousel.html ausente #{lang}")

    inline_backticks = body.scan(/`[^`\n]+`/).length
    raise ThesisPost1Error, "uso de código inline (`...`) en prosa/tablas contamina el tema claro #{lang}: #{inline_backticks} ocurrencias" if inline_backticks > 0

    guillemets = body.scan(/[«»]/).length
    raise ThesisPost1Error, "uso de comillas angulares (« ») prohibido #{lang}: #{guillemets}" if guillemets > 0

    brace_decimals = body.scan(/\d+\{[.,]\}\d+/).length
    raise ThesisPost1Error, "uso de llaves {, } en decimales KaTeX prohibido #{lang}: #{brace_decimals}" if brace_decimals > 0

    katex_blocks = body.scan(/\$\$(.*?)\$\$/m).flatten
    katex_violations = katex_blocks.select { |expr| expr.include?(",") || expr.match?(/\\text\{\s*%/) || expr.include?("%") }
    raise ThesisPost1Error, "uso de comas o % dentro de $$...$$ prohibido #{lang}: #{katex_violations.inspect}" unless katex_violations.empty?
  end

  def verify_core_numbers(lang, body)
    m7 = @upgrades.dig("post_i_upgrades", "m7_mundlak_cre_and_cluster_inference")
    m8 = @upgrades.dig("post_i_upgrades", "m8_out_of_sample_hazard_calibration", "post1_cuadro10_forward_validation_2009_2011")

    mun_between = localized_decimal(m7.dig("cuadro3_sombra_de_la_muerte", "municipal", "between_school_permanent_gap").abs, lang, decimals: 2)
    ps_between = localized_decimal(m7.dig("cuadro3_sombra_de_la_muerte", "private_subsidized", "between_school_permanent_gap").abs, lang, decimals: 2)
    mun_within = localized_decimal(m7.dig("cuadro3_sombra_de_la_muerte", "municipal", "excess_within_contraction_per_yr").abs, lang, decimals: 3)
    ps_within = localized_decimal(m7.dig("cuadro3_sombra_de_la_muerte", "private_subsidized", "excess_within_contraction_per_yr").abs, lang, decimals: 3)
    c3_total_obs = localized_integer(
      m7.dig("cuadro3_sombra_de_la_muerte", "municipal", "n_obs") +
      m7.dig("cuadro3_sombra_de_la_muerte", "private_subsidized", "n_obs"),
      lang
    )
    c7_static_between = localized_decimal(m7.dig("cuadro7_hlm_mundlak", "static_mundlak_cre", "terms", "lagged_simce_mate4im_bar", "beta"), lang, decimals: 6)
    c7_static_within = localized_signed(m7.dig("cuadro7_hlm_mundlak", "static_mundlak_cre", "terms", "lagged_simce_mate4im_within", "beta"), lang, decimals: 6)

    auc_str = localized_decimal(m8.fetch("roc_auc"), lang, decimals: 4)
    brier_str = localized_decimal(m8.fetch("brier_score"), lang, decimals: 6)
    brier_null_str = localized_decimal(m8.fetch("brier_null"), lang, decimals: 6)
    top_decile = localized_decimal(m8.fetch("top_decile_capture_pct"), lang, decimals: 1)

    required_tokens = [
      mun_between,
      ps_between,
      mun_within,
      ps_within,
      c3_total_obs,
      c7_static_between,
      c7_static_within,
      auc_str,
      brier_str,
      brier_null_str,
      top_decile,
      localized_integer(14_704, lang),
      localized_integer(2_640, lang),
      localized_integer(30_484, lang),
      localized_integer(7_460, lang),
      localized_integer(1_981, lang),
      localized_integer(1_807, lang),
      localized_integer(1_678, lang),
      localized_integer(1_648, lang),
      localized_integer(1_382, lang),
      "296",
      "266"
    ]

    missing = required_tokens.reject { |token| body.include?(token) }
    raise ThesisPost1Error, "cifras gobernadas ausentes #{lang}: #{missing.join(', ')}" unless missing.empty?
  end

  def footnote_parts(body)
    heading = body.match(/^## (?:Referencias|References)\s*$/)
    raise ThesisPost1Error, "sección de referencias ausente" unless heading

    text = body[0...heading.begin(0)]
    refs = body[heading.end(0)..]
    definitions = refs.scan(/^\[\^([^\]]+)\]:\s*(.+)$/)
    [text.scan(/\[\^([^\]]+)\](?!:)/).flatten, definitions]
  end

  def verify_references(lang, body)
    marks, definitions = footnote_parts(body)
    keys = definitions.map(&:first)
    raise ThesisPost1Error, "referencias sin formato de nota #{lang}" if keys.empty?
    raise ThesisPost1Error, "clave de nota duplicada #{lang}" unless keys.uniq.length == keys.length

    orphans = keys - marks
    raise ThesisPost1Error, "nota sin cita en el texto #{lang}: #{orphans.join(', ')}" unless orphans.empty?
    missing = marks.uniq - keys
    raise ThesisPost1Error, "cita sin nota #{lang}: #{missing.join(', ')}" unless missing.empty?

    responsive_tables = body.scan("{: .table--compact .table--scroll}").length
    raise ThesisPost1Error, "tablas responsivas insuficientes #{lang}: #{responsive_tables}" if responsive_tables < 3
  end

  def verify_forbidden_content(lang, body, front)
    public_text = "#{public_metadata(front)}\n#{body}"
    FORBIDDEN_CAUSAL_PROMOTIONS.fetch(lang).each do |pattern|
      if public_text.match?(pattern)
        raise ThesisPost1Error, "promoción causal prohibida o discrepancia D2 #{lang}: #{pattern.inspect}"
      end
    end

    identifier_pattern = /\b(?:MRUN|RUN|RUT|RBD)\s*(?:N[.º°o]?\s*)?\d{2,}\b/i
    raise ThesisPost1Error, "identificador individual/escolar prohibido #{lang}" if public_text.match?(identifier_pattern)
    raise ThesisPost1Error, "ruta privada prohibida #{lang}" if public_text.match?(PRIVATE_PATH_PATTERN)
  end

  def public_metadata(front)
    PUBLIC_METADATA_KEYS.flat_map { |key| Array(front[key]) }.compact.join("\n")
  end

  def verify_visible_length(lang, body)
    article = body.sub(/\n## (?:Referencias|References)\n.*/m, "")
    words = article.scan(/[[:alnum:]ÁÉÍÓÚÜÑáéíóúüñ]+/).length
    unless MAIN_WORD_RANGE.cover?(words)
      raise ThesisPost1Error, "longitud visible fuera de rango #{lang}: #{words} palabras"
    end
  end

  def verify_pair(documents)
    es_body = documents.fetch("es").body
    en_body = documents.fetch("en").body

    es_tables = es_body.scan("{: .table--compact .table--scroll}").length
    en_tables = en_body.scan("{: .table--compact .table--scroll}").length
    raise ThesisPost1Error, "paridad de tablas ES/EN divergente (#{es_tables} vs #{en_tables})" unless es_tables == en_tables

    es_notes = es_body.scan(/<aside class="notice--info" markdown="1">/).length
    en_notes = en_body.scan(/<aside class="notice--info" markdown="1">/).length
    raise ThesisPost1Error, "paridad de notas metodológicas ES/EN divergente (#{es_notes} vs #{en_notes})" unless es_notes == en_notes
  end

  def inject_fixture!(documents, fixture)
    case fixture
    when "missing_m7_m8"
      documents["es"] = Post1Document.new(
        path: documents["es"].path,
        front_matter: documents["es"].front_matter,
        body: documents["es"].body.gsub("0,8517", "0,5000")
      )
    when "rcid_d2_typo"
      documents["es"] = Post1Document.new(
        path: documents["es"].path,
        front_matter: documents["es"].front_matter,
        body: documents["es"].body + "\n1.677 cierres y 295 en 2016–2025.\n"
      )
    when "inline_backtick"
      documents["es"] = Post1Document.new(
        path: documents["es"].path,
        front_matter: documents["es"].front_matter,
        body: documents["es"].body + "\nTexto con `codigo_inline` prohibido.\n"
      )
    when "causal_promotion"
      documents["es"] = Post1Document.new(
        path: documents["es"].path,
        front_matter: documents["es"].front_matter,
        body: documents["es"].body + "\nLa tesis demuestra causalmente que la competencia cierra escuelas.\n"
      )
    when "orphan_footnote"
      documents["en"] = Post1Document.new(
        path: documents["en"].path,
        front_matter: documents["en"].front_matter,
        body: documents["en"].body + "\n[^orphan999]: Autor. 2025. Test.\n"
      )
    when "katex_comma_or_pct"
      documents["es"] = Post1Document.new(
        path: documents["es"].path,
        front_matter: documents["es"].front_matter,
        body: documents["es"].body + "\n$$0,84\\text{ %}$$\n"
      )
    else
      raise ThesisPost1Error, "fixture desconocida: #{fixture}"
    end
  end
end

if $PROGRAM_NAME == __FILE__
  root = File.expand_path("..", __dir__)
  fixture = nil
  ARGV.each_with_index do |arg, idx|
    fixture = ARGV[idx + 1] if arg == "--fixture"
  end

  begin
    verifier = ThesisPost1Verifier.new(root:)
    verifier.verify(fixture:)
    puts "THESIS_POST1_VERIFICATION_OK"
  rescue ThesisPost1Error => e
    warn "THESIS_POST1_VERIFICATION_FAILED: #{e.message}"
    exit 1
  end
end
