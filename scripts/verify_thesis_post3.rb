#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "digest"
require "json"
require "pathname"
require "yaml"

class ThesisPost3Error < StandardError; end

Post3Document = Data.define(:path, :front_matter, :body)

class ThesisPost3Verifier
  attr_reader :upstream_custody

  FILES = {
    "es" => "_posts/2026-10-23-costos-cierre-escolar-trayectorias.md",
    "en" => "_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md"
  }.freeze
  RECEIPT = "docs/contracts/evidence/post3-scientific-release-v3_1.json"
  CANONICAL_FIGURES = %w[sample-flow post-pilot-reestimation territorial-audit].freeze
  FIGURE_VARIANTS = %w[light dark light-mobile dark-mobile].freeze
  FIGURE_FORMATS = %w[svg png].freeze
  REQUIRED_ANALYSIS_STAGE = "POST_PILOT_REESTIMATION_V3"
  REQUIRED_RESULT_STATE = "INCONCLUSIVE"
  REQUIRED_ANALYSIS_REVISION = "ATTENDANCE_AND_RURALITY_SEMANTICS_V3_1"
  REQUIRED_READINESS = "READY_SCHOOL_OUTCOMES_HE_DEFERRED"
  REQUIRED_UPSTREAM_CUSTODY = "UNCOMMITTED_FILE_HASHES"
  PUBLIC_METADATA_KEYS = %w[title subtitle description excerpt tags categories].freeze
  PRIVATE_PATH_PATTERN = %r{/(?:home|mnt|opt|run|tmp)/}i
  PILOT_NUMBER_PATTERNS = [
    /\+0[,.]98\s*(?:pp|puntos? porcentuales?|percentage points?)/i,
    /[−-]0[,.]57\s+(?:a|to)\s+\+2[,.]54/i,
    /\+3[,.]91\s*(?:pp|puntos? porcentuales?|percentage points?)/i,
    /\+1[,.]53\s+(?:a|to)\s+\+6[,.]29/i,
    /[−-]6[,.]99\s+(?:a|to)\s+\+14[,.]51/i
  ].freeze
  FORBIDDEN_PROMOTIONS = {
    "es" => [
      /\b(?:los cierres(?:\s+escolares)?|cerrar escuelas|el cierre de escuelas?)\s+(?:causan?|provocan?|generan?|reducen?|aumentan?|disminuyen?|empeoran?|mejoran?|deterioran?|perjudican?|dañan?)\b/i,
      /\b(?:los cierres(?:\s+escolares)?|el cierre de escuelas?)\s+(?:causaron?|provocaron?|generaron?|redujeron?|aumentaron?|disminuyeron?|empeoraron?|mejoraron?|deterioraron?|perjudicaron?|dañaron?)\b/i,
      /\b(?:estimamos|identificamos|demostramos|encontramos)\s+(?:un|el)\s+(?:efecto|impacto|costo)\s+causal\b/i,
      /\bla evidencia\s+(?:demuestra|prueba|confirma)\s+que\s+los cierres\b/i,
      /\b(?:el cierre|los cierres)\s+(?:no tuvo|no tuvieron)\s+(?:efecto|impacto|costo)\b/i,
      /\b(?:efecto|impacto|costo)\s+(?:nulo|causal (?:confirmado|demostrado|identificado))\b/i,
      /\b(?:el cierre escolar|cerrar una escuela)\s+(?:perjudica|daña|deteriora|reduce|aumenta|mejora)\b/i,
      /\b(?:el Estado|la autoridad)\s+debe\s+(?:suspender|detener|frenar|prohibir)\s+(?:todo|cualquier|los?)\s+cierre\b/i
    ],
    "en" => [
      /\b(?:school closures|closing schools|the closure of schools?)\s+(?:causes?|produces?|generates?|reduces?|increases?|worsens?|improves?|harms?|damages?)\b/i,
      /\b(?:school closures|closing schools|the closure of schools?)\s+(?:caused|produced|generated|reduced|increased|worsened|improved|harmed|damaged)\b/i,
      /\bwe\s+(?:estimate|identify|demonstrate|find)\s+(?:an?|the)\s+causal\s+(?:effect|impact|cost)\b/i,
      /\bthe evidence\s+(?:demonstrates|proves|confirms)\s+that\s+school closures\b/i,
      /\b(?:the closure|school closures)\s+(?:had|have)\s+no\s+(?:effect|impact|cost)\b/i,
      /\b(?:null|confirmed|demonstrated|identified)\s+causal\s+(?:effect|impact|cost)\b/i,
      /\bclosing a school\s+(?:harms?|damages?|worsens?|reduces?|increases?|improves?)\b/i,
      /\b(?:the state|the authority)\s+(?:must|should)\s+(?:suspend|stop|halt|ban)\s+(?:all|any|the)\s+(?:school )?closures?\b/i
    ]
  }.freeze

  def initialize(root:)
    @root = Pathname(root).expand_path
    @evidence = load_evidence
    validate_evidence!
    verify_optional_upstream!
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

  def read_document(path)
    source = path.read(encoding: "UTF-8")
    match = source.match(/\A---\s*\n(.*?)\n---\s*\n(.*)\z/m)
    raise ThesisPost3Error, "front matter ausente: #{path}" unless match

    front = YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: true)
    Post3Document.new(path:, front_matter: front, body: match[2])
  end

  def load_evidence
    path = @root.join(RECEIPT)
    raise ThesisPost3Error, "recibo científico ausente: #{path}" unless path.file?

    receipt = JSON.parse(path.read(encoding: "UTF-8"))
    unless receipt["schema"] == "3cucharadas-post3-scientific-release-v1" &&
           receipt.dig("publication_scope", "higher_education") == "DEFERRED_NOT_ESTIMATED_NOT_A_PUBLICATION_GATE" &&
           receipt.dig("publication_scope", "new_analysis_performed_for_blog_release") == false
      raise ThesisPost3Error, "alcance del recibo científico divergente"
    end
    @upstream_custody = receipt.dig("source_worktree", "upstream_custody")
    unless @upstream_custody == REQUIRED_UPSTREAM_CUSTODY
      raise ThesisPost3Error, "custodia científica upstream no declarada"
    end
    receipt.fetch("evidence")
  rescue JSON::ParserError => e
    raise ThesisPost3Error, "recibo científico inválido: #{e.message}"
  end

  def verify_optional_upstream!
    root_value = ENV["POST3_RESEARCH_ROOT"]
    return if root_value.nil? || root_value.empty?

    receipt = JSON.parse(@root.join(RECEIPT).read(encoding: "UTF-8"))
    research_root = Pathname(root_value).expand_path
    receipt.fetch("source_worktree").fetch("files").each do |relative, expected|
      path = research_root.join(relative)
      raise ThesisPost3Error, "artefacto científico upstream ausente: #{path}" unless path.file?
      actual = Digest::SHA256.file(path).hexdigest
      raise ThesisPost3Error, "hash upstream divergente: #{relative}" unless actual == expected
    end
  end

  def validate_evidence!
    database = @evidence.fetch("database")
    identity = @evidence.fetch("identity")
    hmg = @evidence.fetch("hmg")
    comparability = @evidence.fetch("comparability")
    identification = @evidence.fetch("identification")
    modern = @evidence.fetch("modern")
    modern_database = @evidence.fetch("modern_database")
    territorial = @evidence.fetch("territorial")

    unless database["status"] == "IMMUTABLE_FOUNDATION_RELEASE_READY_NOT_CAUSAL"
      raise ThesisPost3Error, "release científica fundacional no está cerrada"
    end
    unless identity.dig("interpretation", "causal_effect_identified") == false
      raise ThesisPost3Error, "auditoría de identidad autoriza causalidad"
    end
    unless hmg.dig("counts", "NO_COMPARABLE") == 5
      raise ThesisPost3Error, "ruta histórica no conserva cinco NO_COMPARABLE"
    end
    unless modern["analysis_stage"] == REQUIRED_ANALYSIS_STAGE &&
           modern_database["analysis_stage"] == REQUIRED_ANALYSIS_STAGE
      raise ThesisPost3Error, "etapa científica v3.1 divergente"
    end
    unless modern["analysis_revision"] == REQUIRED_ANALYSIS_REVISION &&
           modern_database["analysis_revision"] == REQUIRED_ANALYSIS_REVISION
      raise ThesisPost3Error, "revisión científica v3.1 divergente"
    end
    unless modern["status"] == REQUIRED_RESULT_STATE &&
           modern.dig("promotion", "causal_language_authorized") == false &&
           modern.dig("promotion", "effect_null_claim_authorized") == false &&
           modern.dig("promotion", "material_harm_claim_authorized") == false
      raise ThesisPost3Error, "resultado v3.1 promovió una conclusión no autorizada"
    end
    unless modern_database["status"] == "ANALYSIS_READY_CAUSAL_MARTS_V3_1"
      raise ThesisPost3Error, "base analítica v3.1 no está lista"
    end
    unless territorial["status"] == "PARTIAL_COVERAGE_GAP" &&
           territorial.dig("adjudication", "closure_supported") == false
      raise ThesisPost3Error, "señal territorial excede su cobertura o autorizó cierre"
    end
    unless comparability["status"] == "OBSERVED_BALANCE_PARTIAL_DIFFERENTIAL_PRE_EVENT_COVERAGE" &&
           comparability["causal_certificate"] == false &&
           comparability.dig("interpretation", "full_sociodemographic_balance") == false
      raise ThesisPost3Error, "auditoría de comparabilidad promovió un certificado causal"
    end
    unless identification["status"] == "DID_EXPLORATORY_NO_DEFENSIBLE_IV_CURRENT_RELEASE" &&
           identification.dig("decision", "estimate_new_iv_now") == false &&
           identification.dig("instrumental_variables", "candidate_passing_all_requirements") == false &&
           identification.dig("instrumental_variables", "iv_estimated") == false
      raise ThesisPost3Error, "auditoría de identificación autorizó una IV no defendible"
    end
  end

  def estimate(outcome_id)
    @evidence.fetch("modern").fetch("estimates").find do |row|
      row.fetch("outcome_id") == outcome_id
    end || raise(ThesisPost3Error, "estimación v3.1 ausente: #{outcome_id}")
  end

  def source_rows(source)
    row = @evidence.fetch("database").fetch("source_views").find { |item| item["source"] == source }
    raise ThesisPost3Error, "fuente científica ausente: #{source}" unless row

    Integer(row.fetch("rows"))
  end

  def localized_integer(value, lang)
    value.to_i.to_s.reverse.scan(/.{1,3}/).join(lang == "es" ? "." : ",").reverse
  end

  def localized_signed(value, lang, scale: 1, decimals: 2)
    number = format("%+.#{decimals}f", Float(value) * scale).tr("-", "−")
    lang == "es" ? number.tr(".", ",") : number
  end

  def numeric_pattern(value, lang, scale: 1, decimals: 2, positive_sign: :required)
    formatted = localized_signed(value, lang, scale:, decimals:)
    if positive_sign == :optional && formatted.start_with?("+")
      "\\+?#{Regexp.escape(formatted.delete_prefix('+'))}"
    else
      Regexp.escape(formatted).sub("−", "[−-]")
    end
  end

  def assert_match!(body, pattern, message)
    raise ThesisPost3Error, message unless body.match?(pattern)
  end

  def positions(body, pattern)
    body.to_enum(:scan, pattern).map { Regexp.last_match.begin(0) }
  end

  def assert_near!(body, left_pattern, right_pattern, max_distance:, message:)
    left = positions(body, left_pattern)
    right = positions(body, right_pattern)
    paired = left.product(right).any? { |a, b| (a - b).abs <= max_distance }
    raise ThesisPost3Error, message unless paired
  end

  def verify_identity(documents)
    fronts = documents.values.map(&:front_matter)
    unless fronts.map { |front| front["lang"] }.sort == %w[en es]
      raise ThesisPost3Error, "par de idiomas incompleto"
    end
    unless fronts.map { |front| front["ref"] }.uniq == ["costos-cierre-escolar-trayectorias"]
      raise ThesisPost3Error, "ref bilingüe divergente"
    end
    raise ThesisPost3Error, "fecha bilingüe divergente" unless fronts.map { |front| front["date"] }.uniq.length == 1
    unless fronts.map { |front| front["permalink"] }.uniq ==
           ["/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/"]
      raise ThesisPost3Error, "permalink bilingüe divergente"
    end

    FILES.each_value do |relative|
      draft = @root.join(relative.sub("_posts/", "_drafts/"))
      raise ThesisPost3Error, "identidad duplicada en _drafts: #{draft}" if draft.exist?
    end
  end

  def verify_document(lang, document)
    front = document.front_matter
    body = document.body

    verify_front_matter(lang, front)
    verify_scientific_state(lang, body)
    verify_core_evidence(lang, body)
    verify_historical_capsule(lang, body)
    verify_higher_education_agenda(lang, body)
    verify_primary_results(lang, body, front)
    verify_comparability_and_identification(lang, body)
    verify_policy_safeguards(lang, body)
    verify_secondary_labels(lang, body)
    verify_figures(lang, body)
    verify_references(lang, body)
    verify_forbidden_content(lang, body, front)
    verify_visible_length(lang, body)
  end

  def verify_front_matter(lang, front)
    unless front.dig("distribution", "social") == false && front.dig("distribution", "republish") == []
      raise ThesisPost3Error, "distribución externa habilitada #{lang}"
    end
    unless front["editorial_contract"] == "societal-contribution-v1"
      raise ThesisPost3Error, "contrato editorial ausente #{lang}"
    end
    unless front["table_contract"] == "explicit-v1"
      raise ThesisPost3Error, "contrato de tablas ausente #{lang}"
    end
  end

  def verify_scientific_state(lang, body)
    state_marker = "<!-- scientific-state: #{REQUIRED_ANALYSIS_STAGE}; result: #{REQUIRED_RESULT_STATE} -->"
    readiness_marker = "<!-- publication-readiness: #{REQUIRED_READINESS} -->"
    raise ThesisPost3Error, "estado científico v3.1 ausente o duplicado #{lang}" unless body.scan(state_marker).length == 1
    raise ThesisPost3Error, "estado de publicación ausente o duplicado #{lang}" unless body.scan(readiness_marker).length == 1
    state_comments = body.scan(/<!--\s*scientific-state:.*?-->/m)
    readiness_comments = body.scan(/<!--\s*publication-readiness:.*?-->/m)
    unless state_comments == [state_marker] && readiness_comments == [readiness_marker]
      raise ThesisPost3Error, "marcador científico o editorial contradictorio #{lang}"
    end
    revision_words = if lang == "es"
                       /reestimaci[oó]n\s+(?:v3\.1\s+)?posterior al piloto|posterior al piloto\s+v3\.1/i
                     else
                       /v3\.1\s+post-pilot re-estimation|post-pilot\s+v3\.1\s+re-estimation/i
                     end
    assert_match!(body, revision_words, "lectura posterior al piloto ausente #{lang}")
  end

  def verify_core_evidence(lang, body)
    required_numbers = [
      localized_integer(source_rows("enrollment"), lang),
      localized_integer(source_rows("performance"), lang),
      localized_integer(@evidence.fetch("identity").dig("universe", "activity_closure_episodes"), lang),
      localized_integer(@evidence.fetch("identity").dig("universe", "post2_strict_baseline_episodes"), lang)
    ]
    missing = required_numbers.reject { |number| body.include?(number) }
    raise ThesisPost3Error, "evidencia estructural faltante #{lang}: #{missing.join(', ')}" unless missing.empty?

    historical_label = if lang == "es"
                         /tablas?.{0,80}\b5\b.{0,30}\b6\b.{0,30}\b7\b.{0,30}\b8\b.{0,30}\b14\b.{0,180}no comparables?/im
                       else
                         /tables?.{0,80}\b5\b.{0,30}\b6\b.{0,30}\b7\b.{0,30}\b8\b.{0,30}\b14\b.{0,180}not comparable/im
                       end
    assert_match!(body, historical_label, "límite histórico HMG ausente #{lang}")
  end

  def verify_primary_results(lang, body, front)
    persistent = estimate("persistent_nonenrollment_two_years")
    progression = estimate("grade_progression_or_lag")
    missingness = @evidence.fetch("modern").dig("sensitivity", "informative_missingness")
    pp = lang == "es" ? /(?:pp|puntos?(?: porcentuales?)?)/i : /(?:pp|(?:percentage )?points?)/i

    {
      "persistent_nonenrollment_two_years" => persistent,
      "grade_progression_or_lag" => progression
    }.each do |outcome, row|
      estimate_pattern = /#{numeric_pattern(row.fetch('estimate'), lang, scale: 100)}\s*#{pp}/i
      ci_pattern = /#{numeric_pattern(row.fetch('ci_lower'), lang, scale: 100, positive_sign: :optional)}\s*(?:a|to|;|,|–|—)\s*#{numeric_pattern(row.fetch('ci_upper'), lang, scale: 100, positive_sign: :optional)}\]?\s*#{pp}?/i
      assert_match!(body, estimate_pattern, "estimación principal v3.1 faltante #{lang}: #{outcome}")
      assert_match!(body, ci_pattern, "intervalo principal v3.1 faltante #{lang}: #{outcome}")

      treated = localized_integer(row.fetch("n_treated_students"), lang)
      control = localized_integer(row.fetch("n_control_students"), lang)
      assert_match!(body, /#{Regexp.escape(treated)}.{0,160}#{Regexp.escape(control)}/m, "muestra principal v3.1 faltante #{lang}: #{outcome}")
    end

    progression_pattern = /#{numeric_pattern(progression.fetch('estimate'), lang, scale: 100)}\s*#{pp}/i
    progression_mentions = progression_mentions_pattern(lang, progression.fetch("estimate"))
    bounds_pattern = /#{numeric_pattern(missingness.fetch('effect_lower'), lang, scale: 100, positive_sign: :optional)}\s*(?:a|to|;|,|–|—)\s*#{numeric_pattern(missingness.fetch('effect_upper'), lang, scale: 100, positive_sign: :optional)}\]?\s*#{pp}?/i
    assert_match!(body, bounds_pattern, "cotas de datos faltantes ausentes #{lang}")
    outcome_definition = if lang == "es"
                           /sin matrícula o (?:con avance inferior|bajo) al? curso esperado al año siguiente.{0,180}falla de progresión o rezago/im
                         else
                           /no enrolment or (?:enrolment )?below the expected grade one year later.{0,180}progression failure or grade lag/im
                         end
    assert_match!(body, outcome_definition, "definición pública de progresión incompleta #{lang}")
    verify_progression_pairing(lang, "#{public_metadata(front)}\n\n#{body}", progression_mentions)
  end

  def semantic_blocks(body)
    figures = body.scan(/<figure\b.*?<\/figure>/mi)
    remainder = body.gsub(/<figure\b.*?<\/figure>/mi, "\n\n")
    prose_and_tables = remainder.split(/\n{2,}/).flat_map do |block|
      rows = block.lines.select { |line| line.start_with?("|") }
      rows.empty? ? [block] : rows
    end
    figures + prose_and_tables
  end

  def verify_progression_pairing(lang, body, progression_pattern)
    lower = lang == "es" ? /(?:[−-]1,15|menos\s+1,15)/i : /(?:[−-]1\.15|minus\s+1\.15)/i
    upper = lang == "es" ? /10,98/i : /10\.98/i
    total = body.scan(progression_pattern).length
    blocks = semantic_blocks(body).select { |block| block.match?(progression_pattern) }
    represented = blocks.sum { |block| block.scan(progression_pattern).length }
    paired = blocks.all? do |block|
      claims = positions(block, progression_pattern)
      lows = positions(block, lower)
      highs = positions(block, upper)
      claims.all? do |claim|
        lows.any? { |position| (claim - position).abs <= 420 } &&
          highs.any? { |position| (claim - position).abs <= 420 }
      end
    end
    unless total.positive? && represented == total && paired
      raise ThesisPost3Error, "cada mención de progresión debe conservar sus dos cotas #{lang}"
    end
  end

  def progression_mentions_pattern(lang, estimate)
    exact = localized_signed(estimate, lang, scale: 100).delete_prefix("+")
    rounded = localized_decimal(Float(estimate) * 100, lang, decimals: 1)
    /(?<![[:alnum:]])\+?(?:#{Regexp.escape(exact)}|#{Regexp.escape(rounded)})(?!\d)/i
  end

  def hmg_table(table_id)
    @evidence.fetch("hmg_spec").fetch("tables").find do |row|
      row.fetch("table_id") == table_id
    end || raise(ThesisPost3Error, "tabla HMG ausente: #{table_id}")
  end

  def verify_historical_capsule(lang, body)
    %w[table_7 table_8 table_14].each do |table_id|
      row = hmg_table(table_id)
      effect = numeric_pattern(
        row.fetch("parameters").fetch("school_exit").fetch("coefficient"),
        lang,
        scale: 100,
        positive_sign: :optional
      )
      sample = Regexp.escape(localized_integer(row.fetch("sample_n"), lang))
      assert_near!(
        body,
        /#{effect}\s*(?:puntos?(?: porcentuales?)?|percentage[- ]points?|points?)/i,
        /#{sample}/,
        max_distance: 420,
        message: "cápsula HMG sin efecto o muestra publicados #{lang}: #{table_id}"
      )
    end
    label = lang == "es" ? /cifras describen lo publicado/i : /figures therefore describe the paper/i
    assert_match!(body, label, "cápsula HMG no separa publicación y reconstrucción #{lang}")
  end

  def verify_higher_education_agenda(lang, body)
    blocks = body.scan(/<!-- higher-education-agenda:start -->(.*?)<!-- higher-education-agenda:end -->/m).flatten
    raise ThesisPost3Error, "agenda de educación superior ausente o duplicada #{lang}" unless blocks.length == 1

    agenda = blocks.first
    words = agenda.gsub(/<[^>]+>|\{:[^}]+\}/, " ").scan(/[[:alpha:]À-ÿ]+/).length
    raise ThesisPost3Error, "agenda de educación superior fuera de extensión #{lang}" unless (60..130).cover?(words)
    raise ThesisPost3Error, "agenda de educación superior contiene una cifra estimada #{lang}" if agenda.match?(/\d/)

    required = if lang == "es"
                 [/educación superior/i, /entrega posterior/i, /SIES/i, /DEMRE/i, /aquí no se estiman ni se sugieren efectos postsecundarios/i, /no condiciona la publicación/i]
               else
                 [/higher education/i, /later instalment/i, /SIES/i, /DEMRE/i, /neither estimates nor suggests postsecondary effects/i, /does not condition publication/i]
               end
    required.each { |pattern| assert_match!(agenda, pattern, "agenda de educación superior incompleta #{lang}") }
    forbidden = /BLOCKED_MISSING_INDIVIDUAL_SIES|no está listo para publicación|not publication-ready|required outcome|resultado obligatorio|(?:publicación|publication).{0,120}(?:bloquead|blocked).{0,200}(?:SIES|DEMRE)|(?:SIES|DEMRE).{0,200}(?:bloquead|blocked)/im
    raise ThesisPost3Error, "bloqueo de educación superior reintroducido #{lang}" if body.match?(forbidden)

    outside_agenda = body.gsub(/<!-- higher-education-agenda:start -->.*?<!-- higher-education-agenda:end -->/m, "")
    he_effect = if lang == "es"
                  /\b(?:el cierre|los cierres)\b.{0,80}\b(?:reduce|aumenta|afecta|perjudica|mejora)\b.{0,100}\b(?:ingreso|acceso)\b.{0,40}\beducación superior\b/im
                else
                  /\b(?:a school closure|school closures)\b.{0,80}\b(?:reduces?|increases?|affects?|harms?|improves?)\b.{0,100}\b(?:entry|access)\b.{0,40}\bhigher education\b/im
                end
    raise ThesisPost3Error, "efecto postsecundario no autorizado #{lang}" if outside_agenda.match?(he_effect)
  end

  def verify_secondary_labels(lang, body)
    if lang == "es"
      outcome = /(?:asistencia|promedio de notas|notas)/i
      exploratory = /exploratori[oa]s?/i
      conditional = /condicionad[oa]s?|condicional(?:es)?/i
    else
      outcome = /(?:attendance|average marks?|marks?|grades?)/i
      exploratory = /exploratory/i
      conditional = /conditional(?:ly)?|conditioned/i
    end
    assert_near!(body, outcome, exploratory, max_distance: 650, message: "etiqueta exploratoria secundaria ausente #{lang}")
    assert_near!(body, outcome, conditional, max_distance: 650, message: "etiqueta condicional secundaria ausente #{lang}")
  end

  def localized_decimal(value, lang, decimals:)
    formatted = format("%.#{decimals}f", Float(value))
    lang == "es" ? formatted.tr(".", ",") : formatted
  end

  def verify_comparability_and_identification(lang, body)
    comparability = @evidence.fetch("comparability")
    identification = @evidence.fetch("identification")
    balance = comparability.fetch("continuous_balance").to_h { |row| [row.fetch("variable"), row] }

    age = balance.fetch("age")
    attendance = balance.fetch("baseline_attendance")
    grades = balance.fetch("baseline_grade_average")
    expected_values = [
      localized_decimal(age.fetch("treated_weighted_mean"), lang, decimals: 2),
      localized_decimal(age.fetch("control_weighted_mean"), lang, decimals: 2),
      localized_decimal(attendance.fetch("treated_weighted_mean"), lang, decimals: 2),
      localized_decimal(attendance.fetch("control_weighted_mean"), lang, decimals: 2),
      localized_decimal(grades.fetch("treated_weighted_mean"), lang, decimals: 2),
      localized_decimal(grades.fetch("control_weighted_mean"), lang, decimals: 2),
      localized_decimal(comparability.dig("summary", "maximum_continuous_observation_share_gap") * 100, lang, decimals: 1)
    ]
    missing = expected_values.reject { |value| body.include?(value) }
    unless missing.empty?
      raise ThesisPost3Error, "comparabilidad observada divergente #{lang}: #{missing.join(', ')}"
    end

    df_rows = identification.dig("degrees_of_freedom", "estimates")
    effective_clusters = df_rows.map { |row| row.fetch("effective_treated_clusters") }.uniq
    effective_clusters.each do |value|
      rendered = localized_decimal(value, lang, decimals: 1)
      raise ThesisPost3Error, "clusters efectivos ausentes #{lang}: #{rendered}" unless body.include?(rendered)
    end

    balance_limit = if lang == "es"
                      /no certifica aleatorización ni comparabilidad sociodemográfica completa/i
                    else
                      /certifies neither random assignment nor full sociodemographic comparability/i
                    end
    no_iv = if lang == "es"
              /no se ejecuta una regresión instrumental en esta versión/i
            else
              /no instrumental-variable regression is therefore run in this version/i
            end
    assert_match!(body, balance_limit, "límite de comparabilidad ausente #{lang}")
    coverage_scope = if lang == "es"
                       /la edad se observa en toda la muestra.{0,260}asistencia y las notas.{0,180}76,8\s*%.{0,100}96,2\s*%/im
                     else
                       /age is observed for the full sample.{0,260}attendance and marks.{0,180}76\.8%.{0,100}96\.2%/im
                     end
    assert_match!(body, coverage_scope, "alcance de cobertura comparativa impreciso #{lang}")
    assert_match!(body, no_iv, "rechazo editorial de IV ausente #{lang}")
  end

  def verify_policy_safeguards(lang, body)
    safeguard = if lang == "es"
                  /resguardos prudenciales.{0,500}no son efectos estimados de esas decisiones/im
                else
                  /precautionary safeguards.{0,500}not estimated effects of those decisions/im
                end
    assert_match!(body, safeguard, "resguardos prudenciales promovidos a efecto #{lang}")
  end

  def verify_figures(lang, body)
    CANONICAL_FIGURES.each do |family|
      reference = %r{/assets/images/tesis-post3/#{Regexp.escape(family)}-#{lang}-(?:light|dark)}
      assert_match!(body, reference, "figura canónica no referenciada #{lang}: #{family}")

      figure = body.scan(/<figure\b.*?<\/figure>/mi).find { |block| block.match?(reference) }
      raise ThesisPost3Error, "bloque de figura canónica ausente #{lang}: #{family}" unless figure

      visual_contract = [
        /<img\b[^>]*class="[^"]*\bpost3-theme-image\b[^"]*"/i,
        /<a\b[^>]*data-light-href="[^"]*#{Regexp.escape(family)}-#{lang}-light\.svg/i,
        /<a\b[^>]*data-dark-href="[^"]*#{Regexp.escape(family)}-#{lang}-dark\.svg/i,
        /data-light-src="[^"]*#{Regexp.escape(family)}-#{lang}-light\.svg/i,
        /data-dark-src="[^"]*#{Regexp.escape(family)}-#{lang}-dark\.svg/i,
        /data-light-srcset="[^"]*#{Regexp.escape(family)}-#{lang}-light-mobile\.svg/i,
        /data-dark-srcset="[^"]*#{Regexp.escape(family)}-#{lang}-dark-mobile\.svg/i,
        lang == "es" ? /<figcaption>.*\bFuente:/mi : /<figcaption>.*\bSource:/mi
      ]
      unless visual_contract.all? { |pattern| figure.match?(pattern) }
        raise ThesisPost3Error, "contrato visual de figura incompleto #{lang}: #{family}"
      end

      FIGURE_VARIANTS.product(FIGURE_FORMATS).each do |variant, format|
        relative = "assets/images/tesis-post3/#{family}-#{lang}-#{variant}.#{format}"
        raise ThesisPost3Error, "variante de figura ausente: #{relative}" unless @root.join(relative).file?
      end
    end
  end

  def verify_references(lang, body)
    unless body.include?('<div class="post-references" markdown="1">')
      raise ThesisPost3Error, "contenedor de referencias ausente #{lang}"
    end
    dois = body.scan(%r{https://doi\.org/([^\s)\]"<]+)}i).flatten.map(&:downcase).uniq
    raise ThesisPost3Error, "bibliografía insuficiente #{lang}: #{dois.length} DOI" if dois.length < 9

    responsive_tables = body.scan("{: .table--compact .table--scroll}").length
    raise ThesisPost3Error, "tablas responsivas insuficientes #{lang}" if responsive_tables < 2
  end

  def verify_forbidden_content(lang, body, front)
    public_text = "#{public_metadata(front)}\n#{body}"
    FORBIDDEN_PROMOTIONS.fetch(lang).each do |pattern|
      if public_text.match?(pattern)
        raise ThesisPost3Error, "promoción causal no autorizada #{lang}: #{pattern.inspect}"
      end
    end
    PILOT_NUMBER_PATTERNS.each do |pattern|
      raise ThesisPost3Error, "cifra piloto obsoleta #{lang}: #{pattern.inspect}" if public_text.match?(pattern)
    end

    identifier_pattern = /\b(?:MRUN|RUN|RUT|RBD)\s*(?:N[.º°o]?\s*)?\d{2,}\b/i
    raise ThesisPost3Error, "identificador público prohibido #{lang}" if public_text.match?(identifier_pattern)
    raise ThesisPost3Error, "ruta privada prohibida #{lang}" if public_text.match?(PRIVATE_PATH_PATTERN)
  end

  def public_metadata(front)
    PUBLIC_METADATA_KEYS.flat_map { |key| Array(front[key]) }.compact.join("\n")
  end

  def verify_visible_length(lang, body)
    return unless lang == "es"

    article = body.sub(/\n## Referencias\n.*/m, "")
    article = article.gsub(/<!--.*?-->/m, " ").gsub(/<[^>]+>/, " ")
                     .gsub(/\{:[^}]+\}/, " ").gsub(/\{\{.*?\}\}/, " ")
                     .gsub(/[|#*_>`~-]/, " ")
    words = article.scan(/[[:alpha:]À-ÿ0-9]+/).length
    raise ThesisPost3Error, "extensión visible ES fuera de 3.000–3.500 palabras: #{words}" unless (3_000..3_500).cover?(words)
  end

  def verify_pair(documents)
    spanish = documents.fetch("es").body
    english = documents.fetch("en").body
    es_tables = spanish.scan(/^\|/).length
    en_tables = english.scan(/^\|/).length
    raise ThesisPost3Error, "número de filas de tablas divergente" unless es_tables == en_tables

    es_dois = spanish.scan(%r{https://doi\.org/([^\s)\]"<]+)}i).flatten.map(&:downcase).uniq.sort
    en_dois = english.scan(%r{https://doi\.org/([^\s)\]"<]+)}i).flatten.map(&:downcase).uniq.sort
    raise ThesisPost3Error, "referencias bilingües divergentes" unless es_dois == en_dois

    figure_families = lambda do |body|
      body.scan(%r{/assets/images/tesis-post3/([a-z0-9-]+)-(?:es|en)-(?:light|dark)}).flatten.uniq.sort
    end
    unless figure_families.call(spanish) == figure_families.call(english)
      raise ThesisPost3Error, "familias de figuras bilingües divergentes"
    end

    verify_numeric_pairing(spanish, english)
  end

  def localized_numeric_tokens(text, lang)
    text.scan(/(?<![[:alnum:]])[+−-]?(?:\d{1,3}(?:[.,]\d{3})+|\d+)(?:[.,]\d+)?(?![[:alnum:]])/).map do |token|
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
    unless es_tables.length == en_tables.length && es_tables.zip(en_tables).all? { |es, en| localized_numeric_tokens(es, "es") == localized_numeric_tokens(en, "en") }
      raise ThesisPost3Error, "cifras de tablas bilingües divergentes"
    end

    figure_blocks = lambda { |body| body.scan(/<figure\b.*?<\/figure>/mi) }
    es_figures = figure_blocks.call(spanish)
    en_figures = figure_blocks.call(english)
    unless es_figures.length == en_figures.length && es_figures.zip(en_figures).all? { |es, en| localized_numeric_tokens(es, "es") == localized_numeric_tokens(en, "en") }
      raise ThesisPost3Error, "cifras de figuras bilingües divergentes"
    end
  end

  def replace_once!(documents, lang, pattern, replacement, fixture)
    document = documents.fetch(lang)
    changed = document.body.sub(pattern, replacement)
    if changed == document.body
      raise ThesisPost3Error, "fixture no pudo aplicarse: #{fixture}"
    end

    documents[lang] = document.with(body: changed)
  end

  def replace_all!(documents, lang, pattern, replacement, fixture)
    document = documents.fetch(lang)
    changed = document.body.gsub(pattern, replacement)
    if changed == document.body
      raise ThesisPost3Error, "fixture no pudo aplicarse: #{fixture}"
    end

    documents[lang] = document.with(body: changed)
  end

  def inject_fixture!(documents, fixture)
    case fixture
    when "causal-promotion"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nLos cierres causan una pérdida comprobada.\n")
    when "en-causal-promotion"
      document = documents.fetch("en")
      documents["en"] = document.with(body: "#{document.body}\nSchool closures reduced achievement.\n")
    when "null-promotion"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nLos cierres no tuvieron impacto.\n")
    when "privacy-path"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nFuente local: /home/private/post3.parquet\n")
    when "school-identifier"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nEl RBD 123 requiere revisión.\n")
    when "state-drift"
      replace_all!(documents, "es", REQUIRED_RESULT_STATE, "CONCLUSIVE", fixture)
    when "readiness-marker-drift"
      replace_all!(documents, "es", REQUIRED_READINESS, "READY_UNSCOPED", fixture)
    when "readiness-marker-duplicate"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\n<!-- publication-readiness: READY_UNSCOPED -->\n")
    when "scientific-state-duplicate"
      document = documents.fetch("en")
      documents["en"] = document.with(body: "#{document.body}\n<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: CONCLUSIVE -->\n")
    when "primary-number-drift"
      progression = estimate("grade_progression_or_lag")
      pattern = /#{numeric_pattern(progression.fetch('estimate'), 'es', scale: 100)}\s*(?:pp|puntos porcentuales?)/i
      replace_all!(documents, "es", pattern, "+5,30 pp", fixture)
    when "missingness-drift"
      missingness = @evidence.fetch("modern").dig("sensitivity", "informative_missingness")
      pattern = /#{numeric_pattern(missingness.fetch('effect_upper'), 'es', scale: 100, positive_sign: :optional)}/i
      replace_all!(documents, "es", pattern, "10,99", fixture)
    when "missingness-unpaired"
      missingness = @evidence.fetch("modern").dig("sensitivity", "informative_missingness")
      low = /#{numeric_pattern(missingness.fetch('effect_lower'), 'es', scale: 100, positive_sign: :optional)}/i
      high = /#{numeric_pattern(missingness.fetch('effect_upper'), 'es', scale: 100, positive_sign: :optional)}/i
      replace_all!(documents, "es", low, "−1,14", fixture)
      replace_all!(documents, "es", high, "10,99", fixture)
      document = documents.fetch("es")
      moved = "#{document.body}\n#{'x' * 2_200}\nCotas de datos faltantes: −1,15 a 10,98 pp.\n"
      documents["es"] = document.with(body: moved)
    when "bounds-drop"
      replace_all!(documents, "en", /[−-]1\.15/, "−1.14", fixture)
      replace_all!(documents, "en", /10\.98/, "10.99", fixture)
    when "bounds-unpaired-extra"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nResultado adicional: +5,29 pp.\n")
    when "bounds-unpaired-no-sign"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nResultado adicional: 5,29 puntos porcentuales.\n")
    when "bounds-unpaired-rounded"
      document = documents.fetch("en")
      documents["en"] = document.with(body: "#{document.body}\nAdditional result: 5.3 percentage points.\n")
    when "secondary-label-drop"
      replace_all!(documents, "es", /exploratori[oa]s?/i, "descriptivos", fixture)
    when "figure-path-drift"
      replace_all!(documents, "en", /post-pilot-reestimation-en-(?=light|dark)/, "pilot-estimates-en-", fixture)
    when "figure-contract-drift"
      replace_all!(documents, "en", /data-dark-srcset=/, "data-dark-srcset-broken=", fixture)
    when "reference-drift"
      replace_once!(documents, "en", %r{https://doi\.org/[^\s)\]"<]+}i, "https://doi.org/10.0000/drift", fixture)
    when "pilot-number"
      document = documents.fetch("en")
      documents["en"] = document.with(body: "#{document.body}\nLegacy estimate: +3.91 pp.\n")
    when "hmg-number-drift"
      replace_all!(documents, "es", /\+1,46\s+puntos porcentuales/i, "+1,47 puntos porcentuales", fixture)
    when "he-blocker-reintroduced"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nEl borrador no está listo para publicación.\n")
    when "he-blocker-paraphrase"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nLa publicación queda bloqueada hasta contar con microdatos SIES.\n")
    when "he-effect-outside-agenda"
      document = documents.fetch("en")
      documents["en"] = document.with(body: "#{document.body}\nSchool closures reduce access to higher education.\n")
    when "he-effect-invented"
      replace_once!(documents, "es", "<!-- higher-education-agenda:end -->", "Se estima un efecto postsecundario de 4,2 puntos.\n<!-- higher-education-agenda:end -->", fixture)
    when "he-agenda-duplicate"
      document = documents.fetch("en")
      duplicate = "<!-- higher-education-agenda:start -->Future higher education agenda.<!-- higher-education-agenda:end -->"
      documents["en"] = document.with(body: "#{document.body}\n#{duplicate}\n")
    when "front-matter-causal-promotion"
      document = documents.fetch("es")
      changed = document.front_matter.merge("excerpt" => "Los cierres causan daño educativo.")
      documents["es"] = document.with(front_matter: changed)
    when "front-matter-tags-causal-promotion"
      document = documents.fetch("en")
      changed = document.front_matter.merge("tags" => ["closing a school harms students"])
      documents["en"] = document.with(front_matter: changed)
    when "strong-policy-promotion"
      document = documents.fetch("es")
      documents["es"] = document.with(body: "#{document.body}\nEl Estado debe suspender todo cierre.\n")
    when "table-number-parity-drift"
      replace_once!(documents, "es", "| Sin señal contradictoria | 266 |", "| Sin señal contradictoria | 267 |", fixture)
    when "figure-number-parity-drift"
      replace_once!(documents, "es", "391 se excluyen y 6.190 permanecen", "391 se excluyen y 6.191 permanecen", fixture)
    when "comparability-coverage-drift"
      replace_all!(documents, "es", /19,4(?:\s+pp|\s+puntos porcentuales)/, "19,5 pp", fixture)
    when "progression-definition-narrowing"
      replace_all!(documents, "es", /sin matrícula o (?:con avance inferior|bajo) al? curso esperado al año siguiente/i, "no promoción o rezago escolar", fixture)
    when "comparability-age-coverage"
      replace_all!(documents, "en", /Age is observed for the full sample\./i, "Age is observed only for students with performance records.", fixture)
    when "safeguards-causal-promotion"
      replace_all!(documents, "es", /Estos resguardos no son efectos estimados de esas decisiones\./i, "Estas decisiones reducen los efectos del cierre.", fixture)
    when "effective-clusters-drift"
      replace_all!(documents, "en", "21.1 effective episodes", "22.1 effective episodes", fixture)
    when "iv-promotion"
      replace_all!(documents, "es", "no se ejecuta una regresión instrumental en esta versión", "se ejecuta una regresión instrumental en esta versión", fixture)
    else
      raise ThesisPost3Error, "fixture desconocido: #{fixture}"
    end
  end
end

if $PROGRAM_NAME == __FILE__
  root = Pathname(__dir__).parent
  fixture = ENV["POST3_NEGATIVE_FIXTURE"]

  begin
    verifier = ThesisPost3Verifier.new(root:)
    verifier.verify(fixture: fixture)
    warn "POST3_WARNING: upstream_custody=#{verifier.upstream_custody}; el recibo prueba post↔proyección, no custodia científica en un commit upstream"
    puts "POST3_VALID"
    exit 0
  rescue ThesisPost3Error => e
    warn "POST3_INVALID: #{e.message}"
    exit 1
  end
end
