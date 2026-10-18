#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "digest"
require "json"
require "optparse"
require "pathname"
require "rexml/document"
require "yaml"

class VerificationError < StandardError; end

ROOT = File.expand_path("..", __dir__)
ES_DRAFT_PATH = File.join(ROOT, "_drafts/2026-10-11-tesis-continuacion-post-II.md")
EN_DRAFT_PATH = File.join(ROOT, "_drafts/2026-10-11-tesis-continuacion-post-II-en.md")
ES_POST_PATH = File.join(ROOT, "_posts/2026-10-11-extender-tesis-no-es-agregar-anos.md")
EN_POST_PATH = File.join(ROOT, "_posts/2026-10-11-extender-tesis-no-es-agregar-anos-en.md")
RESULTS_DATA_PATH = File.join(ROOT, "_data/thesis_extension_results.yml")
STYLIZED_DATA_PATH = File.join(ROOT, "_data/thesis_extension_stylized.yml")
STYLIZED_INCLUDE_PATH = File.join(ROOT, "_includes/thesis-extension-stylized-evidence.html")
EDITORIAL_CLAIMS_PATH = File.join(ROOT, "docs/contracts/thesis-post-ii-editorial-claims.yml")
MAP_DATA_PATH = File.join(ROOT, "assets/data/thesis-extension-post2/cases.json")
MAP_AUDIT_PATH = File.join(ROOT, "assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.geojson")
MAP_AUDIT_MANIFEST_PATH = File.join(ROOT, "assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.manifest.json")
MAP_SOURCE_PATH = File.join(ROOT, "assets/src/thesis_post2_map/main.ts")
MAP_STYLE_PATH = File.join(ROOT, "assets/src/thesis_post2_map/styles.scss")
RESULTS_DIR = File.join(ROOT, "assets/images/extender-tesis-no-es-agregar-anos")
RESULTS_MANIFEST_PATH = File.join(RESULTS_DIR, "resultados-manifest.json")
STYLIZED_MANIFEST_PATH = File.join(RESULTS_DIR, "estilizada-manifest.json")
RESULTS_MANIFEST_SHA256 = "846d9d104205b72d2959e690a252ab86869348eacebcb4546d56a13afc22f8cf"
STYLIZED_MANIFEST_SHA256 = "0d51cddcd083d95f889286c781b55780ac79399613ec2e5a00229465348ef607"
FREEZE_RELATIVE_PATH = "audit/scientific_release_freeze.json"
FREEZE_SHA256 = "0a498a7f2294938013751758daf59f72e57d3317e9dcb9cb289ee6f144b92903"
EXPECTED_VISUAL_KEYS = %w[v3 v5 v6 v7 v8 v10].freeze
EXPECTED_LANGUAGES = %w[es en].freeze
EDITORIAL_WORD_TARGET = 4_200
EXPECTED_STYLIZED_COMMUNES = ["Lo Barnechea", "Lo Prado"].freeze
STYLIZED_MAP_ITEM_FIELDS = %w[
  commune tab_label asset alt caption paired_closures nearby_entries same_commune_pairs event_period
  median_distance_km education_segment segment_family schools
].freeze
STYLIZED_SCHOOL_FIELDS = %w[marker role rbd name event_year].freeze
MAP_ROOT_FIELDS = %w[schema_version generated_by basemap_manifest selection_rule cases].freeze
MAP_CASE_FIELDS = %w[
  id case case_kind selection_rank selection_note_es selection_note_en commune event_period
  education_segment segment_family distance_km distance_band same_commune poster_es poster_en
  points links trajectories
].freeze
MAP_POINT_FIELDS = %w[
  role rbd name event_year coordinate_year location_lag_years latitude longitude source_url market_segment
  coordinate_source_kind coordinate_source_label_es coordinate_source_label_en address_evidence
  official_coordinate_year official_latitude official_longitude official_distance_m audit_url
].freeze
MAP_LINK_FIELDS = %w[
  closure_rbd entry_rbd receiver_rbd closure_year entry_year receiver_year distance_km
  entry_coordinate_year location_lag_years market_segment relationship
].freeze
MAP_TRAJECTORY_FIELDS = %w[
  branch outcome relative_year calendar_year status estimate units minimum_units regime
].freeze
EXPECTED_STYLIZED_FILES = %w[
  estilizada-demografia-en.svg
  estilizada-demografia-es.svg
  estilizada-mapa-lo-barnechea-en.svg
  estilizada-mapa-lo-barnechea-es.svg
  estilizada-mapa-el-salvador-en.svg
  estilizada-mapa-el-salvador-es.svg
  estilizada-mapa-lo-prado-en.svg
  estilizada-mapa-lo-prado-es.svg
  estilizada-trayectoria-admission-en.svg
  estilizada-trayectoria-admission-es.svg
  estilizada-trayectoria-simce-en.svg
  estilizada-trayectoria-simce-es.svg
].freeze
AUTHOR_CASE_RELATIVE_PATH = "research/article_post2/el_salvador_author_case.yaml"
EXPECTED_CLAIMS = {
  "SRF-001" => "VERIFIED_WITH_CAVEATS",
  "SRF-004" => "PARTLY_NOT_ESTIMABLE",
  "SRF-005" => "NOT_ESTIMABLE",
  "SRF-006" => "MIXED_SIGNS_ONE_INTERVAL_EXCLUDES_ZERO",
  "SRF-007" => "PARTLY_NOT_ESTIMABLE",
  "SRF-008" => "NOT_SUPPORTED",
  "SRF-013" => "NOT_GRANTED",
  "SRF-014" => "NOT_IDENTIFIED",
  "SRF-015" => "DESCRIPTIVE_AUDIT_WITH_CANDIDATE_LIMITS",
  "SRF-016" => "DESIGN_REJECTED_NO_SYNTHETIC_SUPPORT",
  "SRF-017" => "EXPLORATORY_ONLY",
  "SRF-018" => "EXPLORATORY_DDD_CAUSAL_BLOCKED"
}.freeze
EXPECTED_MR_CLAIM_STATEMENTS = {
  "SRF-004" => "MR1 estima SIMCE en +0,029 DE con un intervalo que cruza cero; admisión queda NOT_ESTIMABLE con ocho cierres.",
  "SRF-006" => "MR3 entrega contribuciones oficiales pequeñas y de signos opuestos: SIMCE es negativa con un intervalo que cruza cero y admisión es positiva con un intervalo que excluye cero."
}.freeze
EXPECTED_WEIGHTED_RAW = [
  ["admission_core", -0.05859441, nil, nil, 8, "NOT_ESTIMABLE"],
  ["simce_relative", 0.03382697, -0.22475448, 0.28894332, 21, "ESTIMATED"]
].freeze
EXPECTED_MR2_POINTS = [
  ["admission_core", 1, -0.02950929, "NOT_ESTIMABLE", 1],
  ["admission_core", 2, -0.32206913, "NOT_ESTIMABLE", 1],
  ["admission_core", 3, -0.25046366, "NOT_ESTIMABLE", 2],
  ["simce_relative", 1, -0.1236597, "NOT_ESTIMABLE", 4],
  ["simce_relative", 2, -0.5117083, "NOT_ESTIMABLE", 6],
  ["simce_relative", 3, -0.2835065, "NOT_ESTIMABLE", 8]
].freeze
POST_IDENTITY = {
  "ref" => "extender-tesis-no-es-agregar-anos",
  "permalink" => "/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/",
  "date" => "2026-10-11 10:00:00 -0300"
}.freeze
FORBIDDEN_PRIVATE = %r{(?:/home/|/Users/|Descargas/|student_id|person_id|dvrut|rut_sostenedor|\b(?:RUN|RUT|MRUN)\s*[:=#]?\s*\d{4,})}i

def fail_unless(condition, message)
  raise VerificationError, message unless condition
end

# Dos niveles (2026-10-17, pedido de la persona usuaria: editar el Post II sin dañar
# nada). Las prohibiciones —promoción causal, fugas privadas, identificadores y puntos
# MR2, estructura del componente— fallan siempre. La redacción exigida —frases de
# evidencia, anclas visibles, etapas en prosa, paridad ES/EN— es un aviso por defecto
# y vuelve a ser error con --strict y en las sondas (--self-test), que es como se
# audita antes de una revisión científica.
$strict = false
$wording_warnings = []

def fail_wording(condition, message)
  return true if condition
  raise VerificationError, message if $strict

  $wording_warnings << message unless $wording_warnings.include?(message)
  false
end

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def read_json(path)
  JSON.parse(File.read(path, encoding: "UTF-8"))
end

def verify_pinned_sha!(path, expected, label)
  fail_unless(File.file?(path), "#{label} ausente")
  fail_unless(sha256(path) == expected, "#{label} hash obsoleto o derivado")
end

def read_post(path)
  text = File.read(path, encoding: "UTF-8")
  match = text.match(/\A---\s*\n(.*?)\n---\s*\n(.*)\z/m)
  raise VerificationError, "front matter inválido: #{path}" unless match

  [YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: false), match[2]]
end

def post_path(lang)
  draft = lang == "es" ? ES_DRAFT_PATH : EN_DRAFT_PATH
  published = lang == "es" ? ES_POST_PATH : EN_POST_PATH
  candidates = [draft, published].select { |path| File.file?(path) }
  fail_unless(candidates.length == 1, "#{lang}: debe existir exactamente una fuente entre draft y post")
  candidates.first
end

def visible_text(markdown)
  markdown.gsub(/<img\b[^>]*>/mi, "").gsub(/\{%.+?%\}/m, "")
end

def public_and_technical(body, required: true)
  match = body.match(/<details\b[^>]*class=["'][^"']*technical-disclosure[^"']*["'][^>]*>.*?<\/details>/mi)
  # El redline aprobado del 2026-10-17 (human-redline.md:38) llevó la nota técnica
  # a «Alcance y reproducibilidad» en lenguaje llano: en societal-contribution-v1
  # el cuerpo entero es relato público.
  return [body, ""] if match.nil? && !required
  fail_unless(match, "nota técnica separada ausente")
  [body.sub(match[0], ""), match[0]]
end

def editorial_claim_ids
  fail_unless(File.file?(EDITORIAL_CLAIMS_PATH), "contrato editorial de claims ausente")
  contract = YAML.safe_load(File.read(EDITORIAL_CLAIMS_PATH, encoding: "UTF-8"), permitted_classes: [], aliases: false)
  fail_unless(contract.fetch("schema") == "thesis-post-ii-editorial-claims-v1", "schema editorial de claims derivó")
  fail_unless(contract.fetch("post_ref") == "extender-tesis-no-es-agregar-anos", "ref editorial de claims derivó")
  fail_unless(contract.fetch("locales") == %w[es en], "locales editoriales de claims derivaron")
  claims = contract.fetch("claims")
  ids = claims.map { |claim| claim.fetch("id") }
  fail_unless(ids.length == ids.uniq.length && ids.length == 12, "claims editoriales deben ser doce y únicos")
  fail_unless(claims.all? { |claim| !claim.fetch("class").empty? && !claim.fetch("requirement").empty? }, "claim editorial incompleto")
  ids
end

def visible_word_count(markdown)
  visible_text(markdown)
    .gsub(/<[^>]+>/m, " ")
    .scan(/[\p{L}\p{N}]+(?:[.,][\p{L}\p{N}]+)*/u)
    .length
end

def estimability_mentions(lower, lang)
  lower.scan(lang == "es" ? /\bno estimable\b/ : /\bnot estimable\b/).length
end

def normalized_text(text)
  text.tr("−", "-").gsub(/(?<=\d),(?=\d)/, ".")
end

def safe_source_path!(root, relative)
  canonical = Pathname.new(File.realpath(root))
  candidate = canonical.join(relative).cleanpath
  fail_unless(candidate.to_s.start_with?("#{canonical}/"), "ruta fuente escapa raíz: #{relative}")
  resolved = Pathname.new(File.realpath(candidate))
  fail_unless(resolved.to_s.start_with?("#{canonical}/"), "ruta fuente escapa raíz: #{relative}")
  resolved.to_s
end

def frozen_artifact_map(freeze)
  freeze.fetch("artifacts").to_h { |row| [row.fetch("path"), row] }
end

def check_freeze!(freeze)
  fail_unless(freeze.fetch("status") == "TECHNICAL_SNAPSHOT_WITH_OPEN_GATES", "estado del freeze científico derivó")
  fail_unless(freeze.fetch("freeze_revision") == 10, "revisión del freeze científico derivó")
  current = freeze.fetch("revision_history").find { |row| row.fetch("revision") == 10 }
  fail_unless(current && current.fetch("supersedes") == 9 && current.fetch("change").include?("RBD 391") && current.fetch("change").include?("mismo entorno visual"), "transición a revisión 10 ausente")
  editorial = freeze.fetch("revision_history").find { |row| row.fetch("revision") == 9 }
  fail_unless(editorial && editorial.fetch("supersedes") == 8 && editorial.fetch("change").include?("no distinguible del azar") && editorial.fetch("change").include?("cambios de calendario posteriores"), "transición a revisión 9 ausente")
  historical_rollout = freeze.fetch("revision_history").find { |row| row.fetch("revision") == 8 }
  fail_unless(historical_rollout && historical_rollout.fetch("supersedes") == 7 && historical_rollout.fetch("change").include?("14 clusters históricos") && historical_rollout.fetch("change").include?("Ñuble con Biobío"), "transición a revisión 8 ausente")
  identification = freeze.fetch("revision_history").find { |row| row.fetch("revision") == 7 }
  fail_unless(identification && identification.fetch("supersedes") == 6 && identification.fetch("change").include?("SLEP v2") && identification.fetch("change").include?("triple diferencia SAE"), "transición a revisión 7 ausente")
  mr_transition = freeze.fetch("revision_history").find { |row| row.fetch("revision") == 6 }
  fail_unless(mr_transition && mr_transition.fetch("supersedes") == 5 && mr_transition.fetch("change").include?("claims MR1 y MR3"), "transición a revisión 6 ausente")
  geographic = freeze.fetch("revision_history").find { |row| row.fetch("revision") == 5 }
  fail_unless(geographic && geographic.fetch("supersedes") == 4 && geographic.fetch("change").include?("Lo Barnechea y Lo Prado"), "transición a revisión 5 ausente")
  transition = freeze.fetch("revision_history").find { |row| row.fetch("revision") == 4 }
  fail_unless(transition && transition.fetch("supersedes") == 3 && transition.fetch("change").include?("tres a dos"), "transición 3→2 del freeze científico ausente")
  authority = freeze.fetch("release_authority")
  %w[publication_authorized submission_authorized diffusion_authorized].each do |key|
    fail_unless(authority.fetch(key) == false, "el freeze concedió autoridad externa: #{key}")
  end
  fail_unless(authority.fetch("human_approval") == "NOT_GRANTED", "el freeze inventó aprobación humana")
  boundaries = freeze.fetch("scientific_boundaries")
  fail_unless(boundaries.fetch("causal_effect_identified") == false, "el freeze promovió causalidad")
  fail_unless(boundaries.fetch("creative_destruction_proven") == false, "el freeze promovió destrucción creadora")
  fail_unless(boundaries.fetch("mr2_global_status").values.all? { |value| value == "NOT_ESTIMABLE" }, "MR2 dejó de ser NOT_ESTIMABLE")
  fail_unless(boundaries.fetch("slep_identification_status") == "DESIGN_REJECTED_NO_SYNTHETIC_SUPPORT", "SLEP v2 fue promovido pese al rechazo")
  fail_unless(boundaries.fetch("slep_exploratory_status") == "EXPLORATORY_RESULTS_REPRODUCED_CAUSAL_BLOCKED", "SLEP v3 fue promovido a efecto")
  fail_unless(boundaries.fetch("sae_ddd_status") == "EXPLORATORY_DDD_ESTIMATED_CAUSAL_BLOCKED", "SAE DDD fue promovido a efecto")
  claims = freeze.fetch("claims").to_h { |row| [row.fetch("claim_id"), row] }
  EXPECTED_CLAIMS.each do |claim_id, status|
    row = claims.fetch(claim_id)
    fail_unless(row.fetch("status") == status, "#{claim_id} derivó de #{status}")
    fail_unless(row.fetch("causal_scope") == "NOT_CAUSAL", "#{claim_id} promovió causalidad")
    fail_unless(row.fetch("consumer_product").split(";").include?("post_ii"), "#{claim_id} no enlaza post_ii")
  end
  EXPECTED_MR_CLAIM_STATEMENTS.each do |claim_id, statement|
    fail_unless(claims.fetch(claim_id).fetch("statement") == statement, "#{claim_id} derivó de la evidencia MR")
  end
end

def check_frozen_files!(freeze, research_root)
  required = %w[
    research/article_post2/el_salvador_author_case.yaml
    audit/post2_stylized_evidence.json
    audit/article_school_market_renewal_estimation.json
    audit/slep_identification_v2.json
    audit/slep_discovery_v3.json
    audit/sae_entry_grade_ddd_v1.json
    reports/275_slep_identification_v2.md
    reports/276_slep_discovery_v3.md
    reports/317_sae_entry_grade_ddd_v1.md
    research/article_post2/sae_entry_grade_ddd_v1.yaml
    audit/release_visuals_h1_h3.json
    audit/release_visuals_mr.json
    figures/post2_stylized_evidence/case_trajectory.csv
    figures/post2_stylized_evidence/comparable_trajectory.csv
    figures/post2_stylized_evidence/demographic_pressure.csv
    figures/post2_stylized_evidence/spatial_school_links.csv
    figures/post2_stylized_evidence/spatial_school_points.csv
    figures/post2_stylized_evidence/spatial_case_summary.csv
    audit/school_coordinate_osm_audit_v1.json
    reports/323_school_coordinate_osm_audit_v1.md
    figures/school_coordinate_osm_audit/public_summary.csv
  ]
  artifacts = frozen_artifact_map(freeze)
  required.each do |relative|
    row = artifacts.fetch(relative) { raise VerificationError, "artefacto no congelado: #{relative}" }
    path = safe_source_path!(research_root, relative)
    verify_pinned_sha!(path, row.fetch("sha256"), "artefacto congelado #{relative}")
    fail_unless(File.size(path) == row.fetch("bytes"), "bytes del artefacto congelado derivaron: #{relative}")
  end
end

def check_science!(research_root, estimation_override: nil)
  estimation = estimation_override || read_json(File.join(research_root, "audit/article_school_market_renewal_estimation.json"))
  mr = read_json(File.join(research_root, "audit/release_visuals_mr.json"))
  interpretation = estimation.fetch("interpretation")
  fail_unless(interpretation.fetch("empirical_verdict") == "SCHUMPETERIAN_CONSISTENCY_NOT_SUPPORTED", "veredicto conjunto derivó")
  fail_unless(interpretation.fetch("causal_effect_identified") == false, "estimación promovió causalidad")
  fail_unless(estimation.fetch("favorable_secondary_sensitivities").empty?, "reaparecieron sensibilidades favorables sin soporte")
  execution = estimation.fetch("execution")
  fail_unless(execution.fetch("primary_engine") == "R" && execution.fetch("bootstrap_reps") == 999 && execution.fetch("result_cells") == 112, "ejecución R 999/112 derivó")
  fail_unless(estimation.dig("method_disclosure", "exact_matching_variables").include?("market_segment"), "el emparejamiento dejó de exigir segmento exacto")

  weighted = estimation.fetch("results").select do |row|
    row["estimand"] == "MR1" && row["variant"] == "weighted_raw" && row["modality"] == "ALL"
  end.sort_by { |row| row.fetch("outcome") }.map do |row|
    [row.fetch("outcome"), row.fetch("estimate"), row["ci95_low"], row["ci95_high"], row.fetch("units"), row.fetch("status")]
  end
  fail_unless(weighted == EXPECTED_WEIGHTED_RAW, "MR1 weighted_raw científico derivó")

  mr2 = estimation.fetch("results").select do |row|
    row["estimand"] == "MR2" && row["variant"] == "primary_shrunk_precision" && row["modality"] == "ALL"
  end.sort_by { |row| [row.fetch("outcome"), row.fetch("cohort_order")] }.map do |row|
    [row.fetch("outcome"), row.fetch("cohort_order"), row.fetch("estimate"), row.fetch("status"), row.fetch("units")]
  end
  fail_unless(mr2 == EXPECTED_MR2_POINTS, "seis puntos MR2 científicos derivaron")
  fail_unless(mr2.all? { |row| row[3] == "NOT_ESTIMABLE" }, "MR2 publicó inferencia sin soporte")

  v5 = mr.dig("visuals", "v5_mr1_forest")
  fail_unless(v5.fetch("not_estimable_visible") && v5.fetch("intervals_cross_zero"), "V5 oculta incertidumbre o no estimabilidad")
  v6 = mr.dig("visuals", "v6_mr2_support")
  fail_unless(v6.fetch("global_status") == "NOT_ESTIMABLE", "V6 promovió MR2")
  fail_unless(v6.fetch("support").map { |row| row.fetch("strict_supported") } == [4, 6, 8, 1, 1, 2], "soporte V6 derivó")
  v7 = mr.dig("visuals", "v7_mr3_fhk")
  fail_unless(v7.dig("identity", "exact_within_tolerance"), "identidad FHK rota")
  turnover = v7.fetch("official_turnover").to_h { |row| [row.fetch("outcome"), row.fetch("estimate")] }
  fail_unless(turnover == { "simce_relative" => -0.00010523, "admission_core" => 0.00011268 }, "rotación oficial derivó")
  v8 = mr.dig("visuals", "v8_mr4_modality")
  fail_unless(v8.fetch("tp_estimates_published") == false, "V8 publicó TP sin soporte")
  fail_unless(v8.fetch("hc_exit_estimates").all? { |row| row.fetch("status") == "NOT_ESTIMABLE" }, "V8 promovió HC sin soporte")
end

def check_svg_accessibility!(path)
  text = File.read(path, encoding: "UTF-8")
  fail_unless(!text.match?(FORBIDDEN_PRIVATE), "SVG expone ruta o identificador privado: #{File.basename(path)}")
  root = REXML::Document.new(text).root
  fail_unless(root&.name == "svg" && root.attributes["role"] == "img", "SVG sin role=img: #{File.basename(path)}")
  title = root.elements["title"]
  desc = root.elements["desc"]
  fail_unless(title && desc && !title.text.to_s.strip.empty? && !desc.text.to_s.strip.empty?, "SVG sin title/desc: #{File.basename(path)}")
end

def check_results!(data, manifest, freeze, research_root)
  fail_unless(manifest.fetch("status") == "BILINGUAL_THESIS_EXTENSION_RESULTS_READY", "estado del manifiesto visual derivó")
  fail_unless(manifest.fetch("languages") == EXPECTED_LANGUAGES, "idiomas del manifiesto visual derivaron")
  figures = manifest.fetch("figures")
  fail_unless(figures.map { |row| row.fetch("key") } == EXPECTED_VISUAL_KEYS, "inventario visual derivó")
  frozen = frozen_artifact_map(freeze)
  outputs = []
  figures.each do |figure|
    source_csv = figure.fetch("source_csv")
    verify_pinned_sha!(safe_source_path!(research_root, source_csv), figure.fetch("source_csv_sha256"), "CSV visual #{figure.fetch('key')}")
    fail_unless(frozen.fetch(source_csv).fetch("sha256") == figure.fetch("source_csv_sha256"), "CSV visual no coincide con freeze")
    EXPECTED_LANGUAGES.each do |lang|
      output = figure.dig("outputs", lang)
      path = File.join(RESULTS_DIR, output.fetch("filename"))
      verify_pinned_sha!(path, output.fetch("sha256"), "visual blog #{output.fetch('filename')}")
      check_svg_accessibility!(path)
      outputs << output.fetch("filename")
    end
  end
  physical = Dir.glob(File.join(RESULTS_DIR, "resultados-*.svg")).map { |path| File.basename(path) }.sort
  fail_unless(physical == outputs.sort, "archivos resultados-*.svg no coinciden con manifiesto")
  fail_unless(data.fetch("schema_version") == 1, "schema de resultados derivó")
  EXPECTED_LANGUAGES.each do |lang|
    slides = data.dig("locales", lang, "slides")
    ids = %w[market-sensitivity exit-selection entry-support market-recomposition modality-support causal-ladder]
    fail_unless(slides.map { |slide| slide.fetch("id") } == ids, "#{lang}: orden semántico derivó")
    slides.each do |slide|
      %w[title verdict metric alt evidence limit].each { |field| fail_unless(!slide.fetch(field).strip.empty?, "#{lang}: #{field} vacío") }
    end
  end
  combined = normalized_text(data.fetch("locales").values.join(" "))
  %w[+0.029 -0.095 +0.158 4/6/8 1/1/2 -0.000105 +0.000113].each do |token|
    fail_unless(combined.include?(token), "dato material ausente del carrusel: #{token}")
  end
  fail_unless(combined.include?("NOT_ESTIMABLE"), "el carrusel oculta NOT_ESTIMABLE")
end

def check_stylized!(audit, data, manifest, freeze, research_root, workspace_root)
  fail_unless(audit.fetch("status") == "POST2_STYLIZED_EVIDENCE_READY_WITH_DESCRIPTIVE_LIMITS", "evidencia estilizada no está lista")
  governance = audit.fetch("data_governance")
  %w[personal_identifiers_serialized student_rows_serialized third_party_restricted_rows_serialized raw_directory_serialized].each do |key|
    fail_unless(governance.fetch(key) == false, "evidencia estilizada expone #{key}")
  end
  fail_unless(audit.fetch("school_points").length == 4 && audit.fetch("school_links").length == 2, "inventario de casos estilizados derivó")
  selection = audit.fetch("selection")
  fail_unless(
    selection.fetch("uses_outcome_values") == false &&
      selection.fetch("uses_outcome_availability") == false &&
      selection.fetch("selected_cases") == 2,
    "selección de casos no divulga valor versus disponibilidad del resultado"
  )
  spatial = audit.fetch("spatial")
  expected_spatial = {
    "administrative_closure_events_total" => 346,
    "eligible_closure_events_total" => 330,
    "eligible_closure_schools_total" => 329,
    "eligible_closures_with_coordinates" => 320,
    "eligible_entry_events_total" => 414,
    "eligible_entry_schools_total" => 414,
    "eligible_entries_with_coordinates" => 389,
    "entries_excluded_for_location_instability" => 9,
    "entries_with_delayed_coordinates" => 259,
    "nonoverlapping_offerings_excluded" => 420,
    "cross_segment_candidates_excluded" => 420,
    "identity_candidates_excluded_count" => 6,
    "same_site_identity_candidates_excluded_count" => 6,
    "paired_closures" => 38,
    "unique_nearby_entries" => 29
  }
  expected_spatial.each { |key, value| fail_unless(spatial.fetch(key) == value, "métrica espacial derivó: #{key}") }
  fail_unless(spatial.fetch("exact_market_segment_required") == true, "mapa dejó de exigir segmento exacto")
  fail_unless(spatial.fetch("same_site_identity_guard_km") == 0.1, "guarda de misma sede derivó")
  cases = audit.fetch("spatial_cases")
  fail_unless(cases.map { |row| row.fetch("commune") } == EXPECTED_STYLIZED_COMMUNES, "casos comunales derivaron")
  fail_unless(cases.map { |row| row.fetch("same_commune_pairs") } == [1, 0], "pares dentro de comuna derivaron")
  fail_unless(cases.map { |row| row.fetch("segment_family") } == %w[initial basic], "familias educativas derivaron")
  demography = audit.fetch("demography")
  fail_unless(demography.fetch("population_age_6_17_2025") == 3_081_791 && demography.fetch("population_age_6_17_2050") == 1_366_155, "serie demográfica derivó")
  fail_unless(audit.fetch("interpretation").values.all? { |value| value == false }, "evidencia estilizada promovió interpretación prohibida")

  fail_unless(manifest.fetch("schema_version") == 2, "schema del manifiesto estilizado derivó")
  generator = manifest.fetch("generator")
  verify_pinned_sha!(File.join(ROOT, generator.fetch("path")), generator.fetch("sha256"), "generador estilizado")
  frozen = frozen_artifact_map(freeze)
  manifest.fetch("inputs").each do |relative, expected_sha|
    path = if relative.start_with?("incubadora/tesis_mae_mejorada/")
      safe_source_path!(research_root, relative.sub(%r{\Aincubadora/tesis_mae_mejorada/}, ""))
    else
      safe_source_path!(workspace_root, relative)
    end
    verify_pinned_sha!(path, expected_sha, "fuente estilizada #{relative}")
    research_relative = relative.sub(%r{\Aincubadora/tesis_mae_mejorada/}, "")
    next if research_relative == AUTHOR_CASE_RELATIVE_PATH
    fail_unless(frozen.fetch(research_relative).fetch("sha256") == expected_sha, "fuente estilizada no coincide con freeze")
  end
  expected_outputs = ["_data/thesis_extension_stylized.yml", "assets/data/thesis-extension-post2/cases.json"] + EXPECTED_STYLIZED_FILES.map do |name|
    "assets/images/extender-tesis-no-es-agregar-anos/#{name}"
  end
  fail_unless(manifest.fetch("outputs").keys.sort == expected_outputs.sort, "salidas del manifiesto estilizado derivaron")
  manifest.fetch("outputs").each do |relative, metadata|
    path = File.join(ROOT, relative)
    verify_pinned_sha!(path, metadata.fetch("sha256"), "salida estilizada #{relative}")
    check_svg_accessibility!(path) if path.end_with?(".svg")
  end
  fail_unless(manifest.dig("visual_lineage", "reference") == "assets/src/catastro_sii/chart-theme.ts", "linaje visual de Avalúos derivó")

  fail_unless(data.fetch("schema_version") == 3, "schema de datos estilizados derivó")
  fail_unless(data.fetch("assets").map { |path| File.basename(path) }.sort == EXPECTED_STYLIZED_FILES.sort, "inventario estilizado declarado derivó")
  check_stylized_public_fields!(data)
  EXPECTED_LANGUAGES.each do |lang|
    items = data.dig("locales", lang, "maps", "items")
    fail_unless(items.map { |row| row.fetch("commune") } == EXPECTED_STYLIZED_COMMUNES, "#{lang}: comunas estilizadas derivaron")
    fail_unless(items.map { |row| row.fetch("event_period") } == %w[2016 2016], "#{lang}: periodos de casos derivaron")
    fail_unless(items.map { |row| row.fetch("education_segment") } == ["initial:transicion", "basic"], "#{lang}: segmentos de casos derivaron")
  end
end

def check_stylized_public_fields!(data)
  EXPECTED_LANGUAGES.each do |lang|
    data.dig("locales", lang, "maps", "items").each do |row|
      fail_unless((row.keys - STYLIZED_MAP_ITEM_FIELDS).empty?, "#{lang}: caso cartográfico contiene campos no autorizados")
      row.fetch("schools").each do |school|
        fail_unless((school.keys - STYLIZED_SCHOOL_FIELDS).empty?, "#{lang}: establecimiento contiene campos no autorizados")
      end
    end
  end
end

def check_map_public_fields!(map_data)
  fail_unless((map_data.keys - MAP_ROOT_FIELDS).empty?, "JSON cartográfico contiene campos no autorizados: raíz")
  fail_unless(!JSON.generate(map_data).match?(FORBIDDEN_PRIVATE), "JSON cartográfico expone ruta o identificador privado")
  map_data.fetch("cases").each do |case_row|
    fail_unless((case_row.keys - MAP_CASE_FIELDS).empty?, "JSON cartográfico contiene campos no autorizados: case")
    case_row.fetch("points").each do |point|
      fail_unless((point.keys - MAP_POINT_FIELDS).empty?, "JSON cartográfico contiene campos no autorizados: point")
    end
    case_row.fetch("links").each do |link|
      fail_unless((link.keys - MAP_LINK_FIELDS).empty?, "JSON cartográfico contiene campos no autorizados: link")
    end
    case_row.fetch("trajectories").each do |trajectory|
      fail_unless((trajectory.keys - MAP_TRAJECTORY_FIELDS).empty?, "JSON cartográfico contiene campos no autorizados: trajectory")
    end
  end
end

def check_author_svg_marker!(text)
  fail_unless(text.include?('class="receiver-marker">R</text>'), "mapa autoral no distingue escuela receptora")
  fail_unless(!text.include?('M562 244h24M574 232v24'), "mapa autoral conserva símbolo de apertura para receptora")
end

def check_author_case!(author_case, map_data, data, manifest, research_root)
  check_map_public_fields!(map_data)
  fail_unless(author_case.fetch("status") == "documented_descriptive_case", "El Salvador dejó de ser caso descriptivo documentado")
  selection = author_case.fetch("selection")
  fail_unless(
    selection.fetch("systematic_sample_member") == false &&
      selection.fetch("selected_on_event") == true &&
      selection.fetch("uses_measured_performance_outcomes") == false,
    "El Salvador contaminó la selección sistemática"
  )
  event = author_case.fetch("event")
  fail_unless(event.fetch("type") == "documented_closure_and_merger" && event.fetch("school_year") == 2014, "evento de El Salvador derivó")
  schools = author_case.fetch("schools")
  closure = schools.fetch("closure")
  receiver = schools.fetch("receiver")
  fail_unless(closure.fetch("rbd") == 391 && receiver.fetch("rbd") == 390, "RBD del caso El Salvador derivaron")
  fail_unless(receiver.fetch("coordinate_reference_year") == 2020 && receiver.fetch("address").include?("Diego Portales 1510"), "coordenada receptora de El Salvador no conserva el contraste 2020")
  fail_unless((schools.fetch("geodesic_distance_km") - 1.272025).abs < 0.000001, "distancia de El Salvador derivó")
  fail_unless((schools.fetch("official_coordinate_distance_km") - 0.448903).abs < 0.000001, "contraste oficial de El Salvador derivó")
  closure_display = closure.fetch("display_coordinate")
  fail_unless(
    closure.fetch("address").include?("Diego Portales 500") &&
      closure_display.fetch("source_kind") == "osm_historical_site_candidate" &&
      closure_display.fetch("osm_id") == 1_122_520_465 &&
      closure_display.fetch("temporal_status") == "RETROSPECTIVE_UNVERIFIED" &&
      closure_display.fetch("final_status") == "DISCREPANCY",
    "auditoría de sede histórica de Escuela N° 14 derivó"
  )
  rows = author_case.dig("enrollment", "rows").to_h { |row| [row.fetch("year"), row] }
  fail_unless(rows.dig(2004, "combined") == 1399 && rows.dig(2013, "combined") == 977, "trayectoria histórica de El Salvador derivó")
  fail_unless(rows.dig(2013, "receiver_rbd_390") == 432 && rows.dig(2014, "receiver_rbd_390") == 738, "salto receptor de El Salvador derivó")
  fail_unless((author_case.dig("enrollment", "summaries", "combined_change_2004_2013_percent") + 30.164403).abs < 0.000001, "cambio demográfico de El Salvador derivó")
  source_ids = author_case.fetch("documentary_sources").map { |row| row.fetch("id") }
  fail_unless(%w[bcn_2014 fees_regulation_2019 fees_bulletin_2020 mineduc_open_data].all? { |id| source_ids.include?(id) }, "fuentes de El Salvador incompletas")
  not_verified = author_case.dig("epistemic_register", "not_verified").join(" ").downcase
  fail_unless(not_verified.include?("razón administrativa") && not_verified.include?("cada estudiante"), "límites epistémicos de El Salvador incompletos")

  fail_unless(map_data.fetch("schema_version") == 4, "schema cartográfico no incorpora la procedencia auditada")
  cases = map_data.fetch("cases")
  systematic = cases.select { |row| row.fetch("case_kind") == "systematic" }
  authored = cases.select { |row| row.fetch("case_kind") == "author_documented" }
  fail_unless(systematic.empty?, "el visor principal conserva casos sistemáticos retirados")
  fail_unless(authored.length == 1 && authored.first.fetch("commune") == "El Salvador", "caso autoral ausente o duplicado")
  author_map = authored.first
  fail_unless(author_map.fetch("selection_rank").nil?, "El Salvador recibió ranking sistemático")
  role_by_rbd = author_map.fetch("points").to_h { |row| [row.fetch("rbd"), row.fetch("role")] }
  fail_unless(role_by_rbd == {391 => "closure", 390 => "receiver"}, "la escuela receptora fue rotulada como apertura")
  receiver_map = author_map.fetch("points").find { |row| row.fetch("rbd") == 390 }
  fail_unless(receiver_map.fetch("coordinate_year") == 2020 && receiver_map.fetch("latitude") == -26.243219 && receiver_map.fetch("longitude") == -69.62278, "el render no usa la coordenada 2020 de RBD 390")
  closure_map = author_map.fetch("points").find { |row| row.fetch("rbd") == 391 }
  fail_unless(
    closure_map.fetch("coordinate_source_kind") == "osm_historical_site_candidate" &&
      closure_map.fetch("coordinate_year") == 2026 &&
      closure_map.fetch("official_coordinate_year") == 2015 &&
      closure_map.fetch("official_distance_m") == 825.551 &&
      closure_map.fetch("source_url").end_with?("/way/1122520465"),
    "el visor no conserva la procedencia dual de Escuela N° 14"
  )
  fail_unless(author_map.fetch("trajectories").map { |row| row.fetch("calendar_year") } == [2004, 2013, 2014, 2025], "años calendario de El Salvador derivaron")

  %w[es en].each do |lang|
    authored_locale = data.dig("locales", lang, "authored_case")
    fail_unless(authored_locale.fetch("commune") == "El Salvador", "#{lang}: recuadro autoral ausente")
    fail_unless(authored_locale.fetch("combined_2004") == 1399 && authored_locale.fetch("combined_2013") == 977, "#{lang}: cifras autorales derivaron")
    fail_unless(authored_locale.fetch("asset").end_with?("estilizada-mapa-el-salvador-#{lang}.svg"), "#{lang}: fallback autoral derivó")
    author_svg = File.read(File.join(RESULTS_DIR, "estilizada-mapa-el-salvador-#{lang}.svg"), encoding: "UTF-8")
    check_author_svg_marker!(author_svg)
  end

  author_path = safe_source_path!(research_root, AUTHOR_CASE_RELATIVE_PATH)
  manifest_key = "incubadora/tesis_mae_mejorada/#{AUTHOR_CASE_RELATIVE_PATH}"
  fail_unless(manifest.dig("inputs", manifest_key) == sha256(author_path), "expediente El Salvador no está ligado al manifiesto")
end

def check_include!(text)
  required = %w[
    data-thesis-market-map data-market-map-canvas data-market-map-aside
    data-market-map-panel data-market-map-fallback-grid thesis-post2-map-loader.js
    territorial-evidence territorial-evidence__fallback-grid documented-summary
  ]
  required.each { |token| fail_unless(text.include?(token), "include estilizado sin selector requerido: #{token}") }
  retired = %w[evidence-carousel--stylized data-evidence-carousel thesis-author-case]
  fail_unless(retired.none? { |token| text.include?(token) }, "include conserva componentes territoriales retirados")
  fail_unless(text.include?("target=\"_blank\"") && text.include?("rel=\"noopener\""), "enlace externo sin custodia de pestaña")
  fail_unless(!text.include?("data-market-map-poster"), "el include conserva enlace visible a la lámina estática")
end

def check_release_boundaries!(body, lang, societal: false)
  public_body, technical_body = public_and_technical(body, required: !societal)
  public_text = normalized_text(visible_text(public_body)).gsub(/[*`]/, "")
  technical_text = normalized_text(visible_text(technical_body)).gsub(/[*`]/, "")
  public_lower = public_text.downcase
  claim_ids = editorial_claim_ids
  public_source = public_body.to_s
  claim_ids.each do |claim_id|
    count = public_source.scan(%(id="#{claim_id}")).length
    fail_unless(count <= 1, "#{lang}: claim visible duplicado: #{claim_id}")
    societal ? fail_wording(count == 1, "#{lang}: claim visible ausente: #{claim_id}") : fail_unless(count == 1, "#{lang}: claim visible ausente o duplicado: #{claim_id}")
  end
  selection_fragments = if societal
                          # El redline retiró la frase sobre selección ciega a resultados; quedan el
                          # criterio de coordenada, las exclusiones y el conteo vinculado.
                          if lang == "es"
                            ["primera coordenada oficial válida entre el año de entrada y 2025", "nueve trayectorias inestables", "38 cierres vinculados por proximidad con 29 aperturas únicas"]
                          else
                            ["first valid official coordinate between the entry year and 2025", "nine unstable trajectories", "38 closures remain linked by proximity to 29 unique openings"]
                          end
                        elsif lang == "es"
                          ["ni los valores ni la disponibilidad de resultados participaron en la selección", "primera coordenada oficial válida entre el año de entrada y 2025", "nueve trayectorias inestables", "38 cierres emparejados con 29 aperturas únicas"]
                        else
                          ["neither outcome values nor outcome availability enter the selection", "first valid official coordinate between the entry year and 2025", "nine unstable trajectories", "38 matched closures and 29 unique openings"]
                        end
  selection_ok = selection_fragments.all? { |fragment| public_lower.include?(fragment) }
  societal ? fail_wording(selection_ok, "selección territorial incompletamente divulgada #{lang}") : fail_unless(selection_ok, "selección territorial incompletamente divulgada #{lang}")
  leaked = %w[weighted_raw MR1 MR2].select { |token| public_text.include?(token) }
  fail_unless(leaked.empty?, "relato público expone identificadores de auditoría #{lang}: #{leaked.join(', ')}")
  # Sin nota técnica, MR1/MR2 viven en el registro y el freeze (--claims-only); los
  # puntos MR2 sin soporte no pueden aparecer en ninguna parte del post.
  fail_unless(%w[MR1 MR2].all? { |token| technical_text.include?(token) }, "nota técnica perdió identificadores auditables #{lang}") unless societal
  mr2_point_tokens = %w[-0.124 -0.512 -0.284 -0.030 -0.322 -0.250]
  scanned = societal ? public_text : technical_text
  leaked_mr2_points = mr2_point_tokens.select { |token| scanned.include?(token) }
  fail_unless(leaked_mr2_points.empty?, "nota técnica expone puntos MR2 subsoportados #{lang}: #{leaked_mr2_points.join(', ')}")
end

def check_policy_prose!(section, lower, lang)
  text = normalized_text(visible_text(section)).gsub(/[*`]/, "").downcase
  stages = if lang == "es"
             ["validar el evento", "diagnosticar la trayectoria", "comprobar vacantes reales", "evaluar resultados con seguimiento estudiantil"]
           else
             ["the event must first be validated", "diagnosis then needs", "verify actual vacancies", "evaluation with student follow-up"]
           end
  positions = stages.map { |stage| text.index(stage) }
  fail_wording(positions.none?(&:nil?), "#{lang}: etapa de decisión ausente en la política")
  fail_wording(positions == positions.sort, "#{lang}: etapas de decisión fuera de orden")
  required = if lang == "es"
               [
                 "apoyo a la decisión", "observación → diagnóstico → decisión",
                 "no bastan para decidir un cierre",
                 "un slep planifica y gestiona su propia red", "no los establecimientos de otros sostenedores",
                 "nada de ello entrega autoridad sobre otros sostenedores",
                 "un falso positivo declararía inviable una escuela", "un falso negativo omitiría una transición riesgosa",
                 "ive-sinae describe composición escolar agregada", "la teoría de cambio enlaza",
                 "este post propone evaluar esa cadena; no acredita que funcione"
               ]
             else
               [
                 "decision support", "observation → diagnosis → decision",
                 "a slep plans and manages its own network", "not establishments run by other providers",
                 "none of this grants authority over other providers",
                 "a false positive would deem unviable a school", "a false negative would miss a risky transition",
                 "ive-sinae describes aggregate school composition", "the theory of change links",
                 "this post proposes the chain for evaluation; it does not establish that it works"
               ]
             end
  required.each { |fragment| fail_wording(lower.include?(fragment), "#{lang}: frontera de uso público ausente: #{fragment}") }
end

def check_policy_boundaries!(body, lang)
  lower = normalized_text(visible_text(body)).gsub(/[*`]/, "").downcase
  heading = lang == "es" ? "Qué puede usar la política pública" : "What public policy can use"
  section = body.match(/^## #{Regexp.escape(heading)}\s*$\n(.*?)(?=^## )/m)
  fail_unless(section, "#{lang}: sección de política ausente")
  if body.include?('id="claim-policy-use"')
    check_policy_prose!(section[1], lower, lang)
    return
  end
  table_lines = section[1].lines.map(&:strip).select { |line| line.start_with?("|") }
  fail_unless(table_lines.length == 6, "#{lang}: matriz de política debe tener cuatro filas")
  rows = table_lines.drop(2).map do |line|
    line.delete_prefix("|").delete_suffix("|").split("|").map(&:strip)
  end
  fail_unless(rows.all? { |row| row.length == 4 && row.none?(&:empty?) }, "#{lang}: matriz de política incompleta")
  expected_stages = if lang == "es"
                      ["Validar el evento", "Diagnosticar matrícula decreciente", "Planificar la transición o la red", "Evaluar resultados"]
                    else
                      ["Validate the event", "Diagnose falling enrolment", "Plan a transition or network", "Evaluate results"]
                    end
  fail_unless(rows.map(&:first) == expected_stages, "#{lang}: etapas de decisión divergentes")
  action_guard = lang == "es" ? "; no " : "; do not "
  fail_unless(rows.all? { |row| row[3].downcase.include?(action_guard) }, "#{lang}: matriz perdió una salvaguarda de acción")
  fail_unless(
    rows.all? { |row| row[3].downcase.split(action_guard, 2).last.to_s.strip.length >= 15 },
    "#{lang}: matriz conserva una salvaguarda vacía o trivial"
  )
  if body.include?('id="claim-policy-use"')
    required = if lang == "es"
                 [
                   "apoyo a la decisión", "observación → diagnóstico → decisión",
                   "un slep planifica y gestiona su propia red", "no los establecimientos de otros sostenedores",
                   "un falso positivo señalaría como inviable una escuela", "un falso negativo omitiría una transición riesgosa",
                   "ive-sinae ayuda a describir composición agregada", "la teoría de cambio distingue",
                   "este post propone evaluar esa cadena; no acredita que ya funcione"
                 ]
               else
                 [
                   "decision support", "observation → diagnosis → decision",
                   "a slep plans and manages its own network", "not establishments run by other providers",
                   "a false positive would flag a school as unviable", "a false negative would miss a risky transition",
                   "ive-sinae helps describe aggregate school composition", "an evaluable theory of change",
                   "this post proposes the chain for evaluation; it does not establish that it already works"
                 ]
               end
    required.each { |fragment| fail_unless(lower.include?(fragment), "#{lang}: frontera de uso público ausente: #{fragment}") }
    return
  end
  required = if lang == "es"
               [
                 "apoyo a la decisión",
                 "ordenar escuelas en un ranking",
                 "observación → diagnóstico → decisión",
                 "una baja de matrícula o la cercanía de otra escuela justifican un diagnóstico",
                 "solicitar la corrección a quien mantiene el registro",
                 "no usar un umbral de matrícula como regla de cierre",
                 "un slep planifica y gestiona su propia red",
                 "no los establecimientos de otros sostenedores",
                 "ninguna de esas funciones entrega autoridad sobre otros sostenedores",
                 "desarrollar la oferta pública, velar por la cobertura",
                 "mineduc ejerce la rectoría del sistema educativo",
                 "la dirección de educación pública coordina y conduce estratégicamente el sistema de educación pública",
                 "planifica apoyo técnico, infraestructura y dotaciones a partir del número de cursos y la matrícula",
                 "un falso positivo señalaría como inviable una escuela",
                 "un falso negativo omitiría una transición riesgosa",
                 "ive-sinae ayuda a describir composición agregada de la escuela",
                 "no identifica pobreza individual ni decide por sí solo dónde intervenir",
                 "una teoría de cambio evaluable",
                 "insumos:",
                 "actividades:",
                 "productos:",
                 "resultados intermedios:",
                 "impactos:",
                 "la cadena supone vacantes reales",
                 "traslados aceptables y participación de las comunidades",
                 "no acredita que ya funcione"
               ]
             else
               [
                 "decision support",
                 "ranking schools",
                 "observation → diagnosis → decision",
                 "falling enrolment or a nearby school justify diagnosis",
                 "ask the register's custodian to correct it",
                 "do not use an enrolment threshold as a closure rule",
                 "a slep plans and manages its own network",
                 "not establishments run by other providers",
                 "none of these functions grants authority over other providers",
                 "develop public provision, safeguard coverage",
                 "mineduc is the governing authority for the education system",
                 "the directorate of public education coordinates and strategically steers the public education system",
                 "plans technical support, infrastructure, and staffing on the basis of course numbers and enrolment",
                 "a false positive would flag a school as unviable",
                 "a false negative would miss a risky transition",
                 "ive-sinae helps describe aggregate school composition",
                 "does not identify individual poverty or decide by itself where to intervene",
                 "an evaluable theory of change",
                 "inputs:",
                 "activities:",
                 "outputs:",
                 "intermediate outcomes:",
                 "impacts:",
                 "the chain assumes actual vacancies",
                 "acceptable transfers, and community participation",
                 "does not establish that it already works"
               ]
             end
  required.each do |fragment|
    fail_unless(lower.include?(fragment), "#{lang}: frontera de uso público ausente: #{fragment}")
  end
end

def check_identity!(front, lang)
  POST_IDENTITY.each { |key, value| fail_unless(front.fetch(key).to_s == value, "#{lang}: #{key} derivó") }
  fail_unless(front.fetch("lang") == lang, "#{lang}: lang derivó")
  fail_unless(front.fetch("title").include?(lang == "es" ? "3 cucharadas (parte II)" : "three spoonfuls (part II)"), "#{lang}: título de serie derivó")
  fail_unless(front.fetch("editorial_contract") == "societal-contribution-v1", "#{lang}: contrato editorial ausente")
  fail_unless(front.fetch("table_contract") == "explicit-v1", "#{lang}: contrato explícito de tablas ausente")
  fail_unless(front.dig("ai_disclosure", "components", "text") == "assisted", "#{lang}: divulgación de asistencia derivó")
end

def check_language!(front, body, lang, enforce_length: true, soft_warnings: [])
  check_identity!(front, lang)
  text = visible_text(body)
  normalized = normalized_text(text).gsub(/[*`]/, "")
  lower = normalized.downcase
  if front["editorial_contract"] == "societal-contribution-v1"
    fail_unless(body.scan("{% include thesis-extension-stylized-evidence.html %}").length == 1, "#{lang}: evidencia territorial ausente o duplicada")
    fail_unless(!body.include?("{% include thesis-post2-coordinate-audit-box.html %}"), "#{lang}: auditoría geográfica duplicada fuera del componente unificado")
    fail_unless(!body.include?("{% include thesis-extension-results-carousel.html %}"), "#{lang}: carrusel redundante sigue montado")
    fail_unless(!text.match?(FORBIDDEN_PRIVATE), "#{lang}: ruta o identificador privado expuesto")
    # El redline aprobado reemplaza la jerga `NOT_ESTIMABLE` por «no estimable» /
    # «not estimable» (human-redline.md:38); lo que se exige es que el estado se
    # nombre y se distinga de cero, no el literal técnico.
    fail_unless(estimability_mentions(lower, lang) >= 1, "#{lang}: «no estimable» ausente")
    fail_wording(estimability_mentions(lower, lang) >= 2, "#{lang}: «no estimable» ausente o insuficiente")
    not_zero = lang == "es" ? "«no estimable» no significa cero" : "“not estimable” does not mean zero"
    fail_wording(lower.include?(not_zero), "#{lang}: «no estimable» no se distingue de cero")
    required = if lang == "es"
                 [
                   "900 cierres oficiales", "330 cierres estrictos", "28 → 23 → 1", "21 y 8",
                   "+0.029", "[-0.095; +0.158]", "4/6/8", "1/1/2",
                   "38 cierres vinculados por proximidad con 29 aperturas únicas",
                   "rbd 391", "rbd 390", "1.399", "977", "432 a 738",
                   "ninguna de las 25", "auc con validación cruzada 0.5341", "ihh +0.0035",
                   "estos resultados no permiten concluir que los slep y el sae no tuvieron efectos",
                   "observación → diagnóstico → decisión", "no como una regla para cerrar",
                   "sobre los 684 cierres desde actividad", "no identifica pobreza individual ni decide dónde intervenir",
                   "el diagnóstico basal no mostró capacidad predictiva distinguible del azar",
                   "los resultados son diagnósticos del diseño, no impactos",
                   "el mínimo de diez es una regla retrospectiva", "ihh +0.0035 [-0.0104; +0.0174]"
                 ]
               else
                 [
                   "900 official closures", "330 strict closures", "28 → 23 → 1", "21 and 8",
                   "+0.029", "[-0.095, +0.158]", "4/6/8", "1/1/2",
                   "38 closures remain linked by proximity to 29 unique openings",
                   "rbd 391", "rbd 390", "1.399", "977", "432 to 738",
                   "none of the 25", "cross-validated auc 0.5341", "hhi +0.0035",
                   "these results do not allow me to conclude that sleps and sae had no effects",
                   "observation → diagnosis → decision", "not a rule for closing",
                   "of the 684 closures from active status", "neither identifies individual poverty nor decides where",
                   "the baseline diagnostic showed no predictive ability distinguishable from chance",
                   "these findings diagnose the designs; they are not impacts",
                   "the minimum of ten is a retrospective rule", "hhi +0.0035 [-0.0104, +0.0174]"
                 ]
               end
    required.each { |fragment| fail_wording(lower.include?(fragment), "#{lang}: evidencia o cautela ausente: #{fragment}") }
    forbidden = if lang == "es"
                  ["los cierres mejoraron", "efecto causal está identificado", "deberían cerrar primero",
                   "la baja de matrícula causó el cierre", "también toda la oferta de una comuna"]
                else
                  ["closures improved", "causal effect is identified", "should close first",
                   "falling enrolment caused the closure", "and every school in the commune"]
                end
    forbidden.each { |fragment| fail_unless(!lower.include?(fragment), "#{lang}: promoción causal prohibida: #{fragment}") }
    check_release_boundaries!(body, lang, societal: true)
    check_policy_boundaries!(body, lang)
    if enforce_length
      public_body, = public_and_technical(body, required: false)
      word_count = visible_word_count(public_body)
      fail_unless(word_count >= 3_000, "#{lang}: relato visible demasiado breve (#{word_count})")
      if word_count > EDITORIAL_WORD_TARGET
        soft_warnings << { code: "post-above-soft-word-target", lang: lang, observed_words: word_count, target_words: EDITORIAL_WORD_TARGET }
      end
    end
    return soft_warnings
  end
  fail_unless(body.scan("{% include thesis-extension-stylized-evidence.html %}").length == 1, "#{lang}: evidencia estilizada ausente o duplicada")
  fail_unless(body.scan("{% include thesis-post2-coordinate-audit-box.html %}").length == 1, "#{lang}: recuadro de auditoría geográfica ausente o duplicado")
  fail_unless(!body.include?("{% include thesis-extension-results-carousel.html %}"), "#{lang}: carrusel redundante sigue montado")
  fail_unless(!text.match?(FORBIDDEN_PRIVATE), "#{lang}: ruta o identificador privado expuesto")
  fail_unless(text.scan("NOT_ESTIMABLE").length >= 2, "#{lang}: NOT_ESTIMABLE traducido o ausente")
  not_zero = lang == "es" ? "not_estimable no significa cero" : "not_estimable does not mean zero"
  fail_unless(lower.include?(not_zero), "#{lang}: NOT_ESTIMABLE no se distingue de cero")
  required = if lang == "es"
               [
                 "330 cierres estrictos", "los otros 16", "sede o anexo", "sala cuna", "segmento educativo exacto",
                 "21 y 8", "+0.029", "[-0.095; +0.158]", "4/6/8", "1/1/2", "38 cierres emparejados con 29 aperturas únicas",
                 "lo barnechea", "lo prado", "-0.000105", "+0.000113", "estos resultados no respaldan la hipótesis de destrucción creativa",
                 "contrafactual", "no identifica el efecto de una modalidad de gestión", "este análisis no identifica efectos causales", "3.081.791", "1.366.155", "55.7 %",
                 "el salvador", "rbd 391", "rbd 390", "1.399", "977", "-30.2 %", "432 a 738", "no prueba que haya sido el motivo administrativo",
                 "ninguna de las 25", "regla de soporte fijada en la especificación", "no mostraron capacidad predictiva distinguible del azar",
                 "auc exacta fue 0.5341 con p=0.2195 de permutación", "53 de 70 territorios", "20 %",
                 "hhi +0.0035", "log del número efectivo de escuelas -0.0042",
                 "[-0.010368; +0.017395]", "[-0.026491; +0.018106]", "ñuble se agrupa con biobío",
                 "magallanes se excluye", "solo dos de cuatro", "no acota el efecto de la política",
                 "para cambios de calendario posteriores", "superan incluso los extremos de los intervalos de 2018",
                 "fortalecerían, sin garantizar, una lectura causal de estos diseños",
                 "estos resultados no permiten concluir que los slep y el sae no tuvieron efectos", "la base permite diagnosticar los límites del diseño"
               ]
             else
               [
                 "330 strict closures", "the other 16", "annex", "nursery", "exact education segment",
                 "21 and 8", "+0.029", "[-0.095, +0.158]", "4/6/8", "1/1/2", "38 matched closures and 29 unique openings",
                 "lo barnechea", "lo prado", "-0.000105", "+0.000113", "do not support the creative-destruction hypothesis",
                 "counterfactual", "this analysis does not identify causal effects", "not causal effects", "3.081.791", "1.366.155", "55.7%",
                 "el salvador", "rbd 391", "rbd 390", "1.399", "977", "-30.2%", "432 to 738", "does not prove it was the administrative motive",
                 "none of the 25", "support rule fixed in the analysis specification", "showed no predictive ability distinguishable from chance",
                 "exact auc was 0.5341 with permutation p=0.2195", "53 of 70 territories", "20%",
                 "hhi +0.0035", "log effective number of schools -0.0042",
                 "[-0.010368, +0.017395]", "[-0.026491, +0.018106]", "ñuble is pooled with biobío",
                 "magallanes is excluded", "only two of four", "do not bound the policy effect",
                 "for later schedule changes", "exceed even the bounds of the 2018 intervals",
                 "would strengthen, not guarantee, a causal reading of these designs",
                 "these results do not allow me to conclude that sleps and sae had no effects", "the data let me diagnose the design's limits"
               ]
             end
  required.each { |fragment| fail_unless(lower.include?(fragment), "#{lang}: evidencia o cautela ausente: #{fragment}") }
  forbidden = if lang == "es"
                ["los cierres mejoraron", "destrucción creadora funcionó", "efecto causal está identificado", "la baja de matrícula causó el cierre", "primer estudio", "rancagua", "la reina", "deberían cerrar primero", "base administrativa suficiente", "saltar a un cierre es razonable", "gestiona toda la oferta comunal", "también toda la oferta de una comuna", "coordina la de los demás sostenedores de la comuna", "impactos ya observados", "soporte preregistrado", "regla de soporte preespecificada", "no predijeron mejor que el azar"]
              else
                ["closures improved", "creative destruction worked", "causal effect is identified", "enrolment decline caused the closure", "first study", "rancagua", "la reina", "should close first", "sufficient administrative basis", "jumping to closure is reasonable", "manages every school in the commune", "and every school in the commune", "impacts already observed", "preregistered support", "prespecified support rule", "predicted no better than chance"]
              end
  forbidden.each { |fragment| fail_unless(!lower.include?(fragment), "#{lang}: promoción causal prohibida: #{fragment}") }
  check_release_boundaries!(body, lang)
  check_policy_boundaries!(body, lang)
  fail_unless(!enforce_length || body.length >= 9_000, "#{lang}: extensión inferior a 9k caracteres")
  if enforce_length
    word_count = visible_word_count(body)
    if word_count > EDITORIAL_WORD_TARGET
      soft_warnings << {
        code: "post-above-soft-word-target",
        lang: lang,
        observed_words: word_count,
        target_words: EDITORIAL_WORD_TARGET
      }
    end
  end
  soft_warnings
end

def check_parity!(es_front, es_body, en_front, en_body)
  check_identity!(es_front, "es")
  check_identity!(en_front, "en")
  fail_wording(es_body.scan(/^## /).length == en_body.scan(/^## /).length, "cantidad de secciones ES/EN difiere")
  es_lower = normalized_text(visible_text(es_body)).downcase
  en_lower = normalized_text(visible_text(en_body)).downcase
  fail_unless(es_body.scan("NOT_ESTIMABLE").length == en_body.scan("NOT_ESTIMABLE").length, "cantidad NOT_ESTIMABLE ES/EN difiere")
  fail_wording(estimability_mentions(es_lower, "es") == estimability_mentions(en_lower, "en"), "cantidad de «no estimable» ES/EN difiere")
  numeric_tokens = lambda do |body|
    normalized_text(visible_text(body).gsub(/\]\([^)]+\)/, "]"))
      .scan(/[+-]?\d+(?:\.\d+)*(?:e[+-]?\d+)?(?:\/\d+)*(?:\s*%)?/i)
      .map { |token| token.gsub(/\s+/, "") }
      .tally
  end
  fail_wording(numeric_tokens.call(es_body) == numeric_tokens.call(en_body), "paridad numérica ES/EN difiere")
end

def check_custody!
  posts = [ES_POST_PATH, EN_POST_PATH].select { |path| File.file?(path) }
  drafts = [ES_DRAFT_PATH, EN_DRAFT_PATH].select { |path| File.file?(path) }
  fail_unless(posts.sort == [ES_POST_PATH, EN_POST_PATH].sort, "custodia: faltan posts ES/EN")
  fail_unless(drafts.empty?, "custodia: persisten drafts ES/EN")
end

def check_closeout_map!(freeze, author_case, map_data, data, manifest, include_text, es_body, en_body, research_root)
  check_freeze!(freeze)
  check_author_case!(author_case, map_data, data, manifest, research_root)
  check_include!(include_text)
  cases = map_data.fetch("cases")
  fail_unless(cases.length == 1 && cases.first.fetch("id") == "el-salvador", "el visor no contiene exclusivamente El Salvador")
  fail_unless((cases.first.fetch("distance_km") - 1.272025).abs < 0.000001, "distancia visible de El Salvador derivó")
  fail_unless(cases.first.fetch("points").map { |row| row.fetch("rbd") }.sort == [390, 391], "puntos del visor El Salvador derivaron")
  [es_body, en_body].each do |body|
    fail_unless(!body.match?(/Lo Barnechea|Lo Prado/i), "el relato conserva casos territoriales retirados")
    fail_unless(!body.include?("estilizada-mapa-el-salvador"), "el post conserva un enlace visible a la lámina estática")
    fail_unless(body.include?("auditoria-coordenadas-rbd"), "el enlace a la auditoría territorial está ausente")
  end

  audit = read_json(MAP_AUDIT_PATH)
  audit_manifest = read_json(MAP_AUDIT_MANIFEST_PATH)
  fail_unless(audit.fetch("metadata").fetch("schema_version") == 2, "GeoJSON territorial conserva esquema obsoleto")
  fail_unless(audit.fetch("features").map { |row| row.dig("properties", "rbd") }.uniq.sort == [390, 391], "GeoJSON publica casos fuera del alcance acordado")
  school_14 = audit.fetch("features").select { |row| row.dig("properties", "rbd") == 391 }
  fail_unless(school_14.all? { |row| row.dig("properties", "identity_status") == "PLAUSIBLE" }, "GeoJSON sobredeclara identidad de la Escuela N° 14")
  fail_unless(audit.dig("metadata", "sources", "osm_attribution").to_s.include?("OpenStreetMap contributors"), "GeoJSON perdió atribución OSM")
  fail_unless(audit_manifest.dig("coverage", "expected_rbds") == [391, 390], "manifiesto territorial derivó de los dos RBD visibles")
  fail_unless(audit_manifest.dig("epistemic_status", "official_coordinates_overwritten") == false, "manifiesto sobrescribe la observación oficial")
  audit_manifest.fetch("inputs").each do |relative, expected_sha|
    verify_pinned_sha!(File.join(ROOT, relative), expected_sha, "entrada de auditoría #{relative}")
  end

  source = File.read(MAP_SOURCE_PATH, encoding: "UTF-8")
  style = File.read(MAP_STYLE_PATH, encoding: "UTF-8")
  fail_unless(source.include?("attributionControl: false") && source.scan("new maplibregl.AttributionControl").length == 1, "el mapa no contiene una única atribución controlada")
  fail_unless(source.include?("compact: false"), "la atribución OSM no permanece visible como línea compacta")
  fail_unless(!source.include?("data-market-map-poster"), "el bundle conserva la lámina estática como enlace")
  fail_unless(style.include?("@media (max-width: 52rem)") && style.include?("grid-template-columns: 1fr"), "el mapa perdió el contrato responsivo")
end

# Sondas retiradas el 2026-10-17 al alinear el contrato societal-contribution-v1 con el
# redline aprobado (human-redline.md); su objeto ya no existe en el Post II:
#   - accessible-localization: el include ya no publica la tabla de distancias (body-distance-leak del cierre).
#   - entry-series-scope: el redline retiró la nota técnica que distinguía la cohorte.
#   - policy-design-specificity: el texto aprobado ya no dice «would strengthen, not guarantee».
#   - policy-sae-margin-scope: el texto aprobado ya no compara con los intervalos de 2018.
#   - policy-slep-source-scope: el texto aprobado ya no acota la fuente SLEP a cambios posteriores de calendario.
def run_self_test!(name, freeze, audit, data, include_text, es_front, es_body, en_front, en_body, research_root, author_case, map_data, stylized_manifest)
  expected = nil
  begin
    case name
    when "claims"
      mutant = Marshal.load(Marshal.dump(freeze))
      mutant.fetch("claims").find { |row| row["claim_id"] == "SRF-005" }["status"] = "ESTIMATED"
      expected = "SRF-005 derivó de NOT_ESTIMABLE"
      check_freeze!(mutant)
    when "mr-claim-alignment"
      mutant = Marshal.load(Marshal.dump(freeze))
      mutant.fetch("claims").find { |row| row["claim_id"] == "SRF-006" }["statement"] = "MR3 entrega contribuciones positivas."
      expected = "SRF-006 derivó de la evidencia MR"
      check_freeze!(mutant)
    when "policy-identification"
      mutant = Marshal.load(Marshal.dump(freeze))
      mutant.fetch("claims").find { |row| row["claim_id"] == "SRF-016" }["status"] = "NOT_IDENTIFIED"
      expected = "SRF-016 derivó de DESIGN_REJECTED_NO_SYNTHETIC_SUPPORT"
      check_freeze!(mutant)
    when "policy-slep-predictive-null"
      expected = "es: evidencia o cautela ausente: el diagnóstico basal no mostró capacidad predictiva distinguible del azar"
      mutant = es_body.gsub("no mostró capacidad predictiva distinguible del azar", "predijo qué territorios se traspasaron antes")
      check_language!(es_front, mutant, "es", enforce_length: false)
    when "policy-sae-interval-parity"
      expected = "en: evidencia o cautela ausente: hhi +0.0035 [-0.0104, +0.0174]"
      mutant = en_body.gsub("[−0.0104, +0.0174]", "[−0.0099, +0.0169]")
      check_language!(en_front, mutant, "en", enforce_length: false)
    when "policy-prespecified"
      expected = "en: evidencia o cautela ausente: the minimum of ten is a retrospective rule"
      mutant = en_body.gsub("The minimum of ten is a retrospective rule", "The minimum of ten is a prespecified rule")
      check_language!(en_front, mutant, "en", enforce_length: false)
    when "policy-null-interpretation"
      expected = "en: evidencia o cautela ausente: these results do not allow me to conclude that sleps and sae had no effects"
      mutant = en_body.gsub(
        "These results do not allow me to conclude that SLEPs and SAE had no effects",
        "These results show that SLEPs and SAE had no effects"
      )
      check_language!(en_front, mutant, "en", enforce_length: false)
    when "segment-closure"
      mutant = Marshal.load(Marshal.dump(audit))
      mutant.fetch("spatial")["exact_market_segment_required"] = false
      expected = "mapa dejó de exigir segmento exacto"
      workspace_root = File.expand_path("../..", ROOT)
      check_stylized!(mutant, data, read_json(STYLIZED_MANIFEST_PATH), freeze, research_root, workspace_root)
    when "map-wiring"
      expected = "include estilizado sin selector requerido: data-market-map-canvas"
      check_include!(include_text.gsub("data-market-map-canvas", "data-map-canvas-disabled"))
    when "editorial-es"
      expected = "es: promoción causal prohibida: los cierres mejoraron"
      check_language!(es_front, "#{es_body}\nLos cierres mejoraron.\n", "es", enforce_length: false)
    when "parity"
      expected = "paridad numérica ES/EN difiere"
      check_parity!(es_front, es_body, en_front, en_body.sub("665", "664"))
    when "scientific-mr2"
      mutant = read_json(File.join(research_root, "audit/article_school_market_renewal_estimation.json"))
      mutant.fetch("results").find { |row| row["estimand"] == "MR2" }["status"] = "ESTIMATED"
      expected = "seis puntos MR2 científicos derivaron"
      check_science!(research_root, estimation_override: mutant)
    when "stale-hash"
      expected = "freeze científico hash obsoleto o derivado"
      verify_pinned_sha!(File.join(research_root, FREEZE_RELATIVE_PATH), "0" * 64, "freeze científico")
    when "author-separation"
      mutant = Marshal.load(Marshal.dump(map_data))
      mutant.fetch("cases").last["case_kind"] = "systematic"
      expected = "el visor principal conserva casos sistemáticos retirados"
      check_author_case!(author_case, mutant, data, stylized_manifest, research_root)
    when "author-role"
      mutant = Marshal.load(Marshal.dump(map_data))
      mutant.fetch("cases").last.fetch("points").find { |row| row["rbd"] == 390 }["role"] = "entry"
      expected = "la escuela receptora fue rotulada como apertura"
      check_author_case!(author_case, mutant, data, stylized_manifest, research_root)
    when "author-coordinate"
      mutant = Marshal.load(Marshal.dump(map_data))
      mutant.fetch("cases").last.fetch("points").find { |row| row["rbd"] == 390 }["coordinate_year"] = 2019
      expected = "el render no usa la coordenada 2020 de RBD 390"
      check_author_case!(author_case, mutant, data, stylized_manifest, research_root)
    when "author-cause"
      expected = "es: promoción causal prohibida: la baja de matrícula causó el cierre"
      check_language!(es_front, "#{es_body}\nLa baja de matrícula causó el cierre.\n", "es", enforce_length: false)
    when "policy-auto-close"
      expected = "es: frontera de uso público ausente: no bastan para decidir un cierre"
      mutant = es_body.gsub("no bastan para decidir un cierre", "bastan para decidir un cierre")
      check_language!(es_front, mutant, "es", enforce_length: false)
    when "policy-slep-scope"
      expected = "es: promoción causal prohibida: también toda la oferta de una comuna"
      mutant = es_body.gsub(
        "**su propia red**",
        "**su propia red y también toda la oferta de una comuna**"
      )
      check_language!(es_front, mutant, "es", enforce_length: false)
    when "policy-slep-scope-en"
      expected = "en: promoción causal prohibida: and every school in the commune"
      mutant = en_body.gsub(
        "**its own network**",
        "**its own network and every school in the commune**"
      )
      check_language!(en_front, mutant, "en", enforce_length: false)
    when "policy-matrix-row"
      expected = "en: etapa de decisión ausente en la política"
      mutant = en_body.gsub("evaluation with student follow-up", "evaluation")
      check_language!(en_front, mutant, "en", enforce_length: false)
    when "policy-en-causal-safeguard"
      expected = "en: evidencia o cautela ausente: these findings diagnose the designs; they are not impacts"
      mutant = en_body.gsub("these findings diagnose the designs; they are not impacts", "these findings are impacts")
      check_language!(en_front, mutant, "en", enforce_length: false)
    when "policy-ive-sufficient"
      expected = "es: evidencia o cautela ausente: no identifica pobreza individual ni decide dónde intervenir"
      mutant = es_body.gsub("no identifica pobreza individual ni decide dónde intervenir", "basta para decidir dónde intervenir")
      check_language!(es_front, mutant, "es", enforce_length: false)
    when "policy-ranking"
      expected = "en: promoción causal prohibida: should close first"
      check_language!(en_front, "#{en_body}\nSchools should close first according to this ranking.\n", "en", enforce_length: false)
    when "public-technical-leak"
      expected = "relato público expone identificadores de auditoría es: MR2"
      check_language!(es_front, "MR2.\n#{es_body}", "es", enforce_length: false)
    when "mr2-points-technical"
      expected = "nota técnica expone puntos MR2 subsoportados es: -0.124"
      mutant = es_body.sub("### Alcance y reproducibilidad\n", "### Alcance y reproducibilidad\n\nUn punto de `−0,124`.\n")
      check_language!(es_front, mutant, "es", enforce_length: false)
    when "denominators"
      expected = "es: evidencia o cautela ausente: sobre los 684 cierres desde actividad"
      mutant = es_body.gsub("sobre los 684 cierres desde actividad", "sobre los cierres")
      check_language!(es_front, mutant, "es", enforce_length: false)
    when "stylized-privacy-leak"
      expected = "es: caso cartográfico contiene campos no autorizados"
      mutant = Marshal.load(Marshal.dump(data))
      mutant.dig("locales", "es", "maps", "items", 0)["student_id"] = 123
      check_stylized_public_fields!(mutant)
    when "map-json-privacy-leak"
      expected = "JSON cartográfico contiene campos no autorizados: point"
      mutant = Marshal.load(Marshal.dump(map_data))
      mutant.dig("cases", 0, "points", 0)["internal_note"] = "no publicable"
      check_map_public_fields!(mutant)
    when "same-site-guard"
      expected = "guarda de misma sede derivó"
      mutant = Marshal.load(Marshal.dump(audit))
      mutant.fetch("spatial")["same_site_identity_guard_km"] = 0.0
      workspace_root = File.expand_path("../..", ROOT)
      check_stylized!(mutant, data, read_json(STYLIZED_MANIFEST_PATH), freeze, research_root, workspace_root)
    when "author-receiver-marker"
      expected = "mapa autoral no distingue escuela receptora"
      svg = File.read(File.join(RESULTS_DIR, "estilizada-mapa-el-salvador-es.svg"), encoding: "UTF-8")
      check_author_svg_marker!(svg.gsub("receiver-marker", "entry-marker"))
    when "long-body-soft"
      expected = "extensión larga aceptada con advertencia blanda"
      warnings = []
      check_language!(es_front, "#{es_body}\n#{'contenido trazable ' * 3_000}\n", "es", soft_warnings: warnings)
      fail_unless(warnings.any? { |row| row[:code] == "post-above-soft-word-target" }, "extensión larga no produjo advertencia blanda")
      raise VerificationError, expected
    else
      raise VerificationError, "self-test desconocido: #{name}"
    end
    warn JSON.generate(result: "SELF_TEST_DID_NOT_FAIL", self_test: name, expected_error: expected)
    exit 2
  rescue VerificationError => e
    if e.message == expected
      warn JSON.generate(result: "EXPECTED_FAIL", self_test: name, error: e.message)
      exit 1
    end
    warn JSON.generate(result: "SELF_TEST_WRONG_FAILURE", self_test: name, error: e.message, expected_error: expected)
    exit 2
  end
end

options = { research_root: nil, workspace_root: nil, mode: nil, lang: nil, self_test: nil }
OptionParser.new do |parser|
  parser.on("--research-root PATH") { |value| options[:research_root] = File.expand_path(value, ROOT) }
  parser.on("--workspace-root PATH") { |value| options[:workspace_root] = File.expand_path(value, ROOT) }
  parser.on("--claims-only") { options[:mode] = "claims" }
  parser.on("--lang LANG") { |value| options[:mode] = "lang"; options[:lang] = value }
  parser.on("--parity") { options[:mode] = "parity" }
  parser.on("--causal-language") { options[:mode] = "causal" }
  parser.on("--custody") { options[:mode] = "custody" }
  parser.on("--editorial-only") { options[:mode] = "editorial" }
  parser.on("--all") { options[:mode] = "all" }
  parser.on("--closeout") { options[:mode] = "closeout" }
  parser.on("--self-test NAME") { |value| options[:self_test] = value }
  parser.on("--strict", "la redacción exigida también falla (auditoría científica)") { $strict = true }
end.parse!
$strict = true if options[:self_test]

if options[:mode] == "editorial"
  begin
    warnings = []
    include_text = File.read(STYLIZED_INCLUDE_PATH, encoding: "UTF-8")
    es_front, es_body = read_post(post_path("es"))
    en_front, en_body = read_post(post_path("en"))
    check_include!(include_text)
    check_language!(es_front, es_body, "es", soft_warnings: warnings)
    check_language!(en_front, en_body, "en", soft_warnings: warnings)
    check_parity!(es_front, es_body, en_front, en_body)
    check_custody!
    puts JSON.generate(result: "PASS", mode: "editorial", strict: $strict, soft_warnings: warnings, wording_warnings: $wording_warnings)
    exit 0
  rescue VerificationError, KeyError, JSON::ParserError, Psych::SyntaxError, REXML::ParseException => e
    warn JSON.generate(result: "FAIL", mode: "editorial", error: e.message)
    exit 1
  end
end

begin
  soft_warnings = []
  research_root = options[:research_root] || File.expand_path("../../incubadora/tesis_mae_mejorada", ROOT)
  workspace_root = options[:workspace_root] || File.expand_path("../..", ROOT)
  freeze_path = File.join(research_root, FREEZE_RELATIVE_PATH)
  verify_pinned_sha!(freeze_path, FREEZE_SHA256, "freeze científico")
  verify_pinned_sha!(RESULTS_MANIFEST_PATH, RESULTS_MANIFEST_SHA256, "manifiesto visual")
  verify_pinned_sha!(STYLIZED_MANIFEST_PATH, STYLIZED_MANIFEST_SHA256, "manifiesto estilizado")
  freeze = read_json(freeze_path)
  results_manifest = read_json(RESULTS_MANIFEST_PATH)
  stylized_manifest = read_json(STYLIZED_MANIFEST_PATH)
  results_data = YAML.safe_load(File.read(RESULTS_DATA_PATH, encoding: "UTF-8"), aliases: false)
  stylized_data = YAML.safe_load(File.read(STYLIZED_DATA_PATH, encoding: "UTF-8"), aliases: false)
  map_data = read_json(MAP_DATA_PATH)
  author_case = YAML.safe_load(File.read(File.join(research_root, AUTHOR_CASE_RELATIVE_PATH), encoding: "UTF-8"), aliases: false)
  stylized_audit = read_json(File.join(research_root, "audit/post2_stylized_evidence.json"))
  include_text = File.read(STYLIZED_INCLUDE_PATH, encoding: "UTF-8")
  es_front, es_body = read_post(post_path("es"))
  en_front, en_body = read_post(post_path("en"))

  if options[:self_test]
    run_self_test!(options[:self_test], freeze, stylized_audit, stylized_data, include_text, es_front, es_body, en_front, en_body, research_root, author_case, map_data, stylized_manifest)
  end

  if %w[claims all].include?(options[:mode])
    check_freeze!(freeze)
    check_frozen_files!(freeze, research_root)
    check_science!(research_root)
    check_results!(results_data, results_manifest, freeze, research_root)
    check_stylized!(stylized_audit, stylized_data, stylized_manifest, freeze, research_root, workspace_root)
    check_author_case!(author_case, map_data, stylized_data, stylized_manifest, research_root)
    check_include!(include_text)
  end
  case options[:mode]
  when "lang"
    fail_unless(EXPECTED_LANGUAGES.include?(options[:lang]), "--lang debe ser es o en")
    front, body, lang = options[:lang] == "es" ? [es_front, es_body, "es"] : [en_front, en_body, "en"]
    check_language!(front, body, lang, soft_warnings: soft_warnings)
  when "parity"
    check_parity!(es_front, es_body, en_front, en_body)
  when "causal"
    check_language!(es_front, es_body, "es", soft_warnings: soft_warnings)
    check_language!(en_front, en_body, "en", soft_warnings: soft_warnings)
  when "custody"
    check_custody!
  when "all"
    check_language!(es_front, es_body, "es", soft_warnings: soft_warnings)
    check_language!(en_front, en_body, "en", soft_warnings: soft_warnings)
    check_parity!(es_front, es_body, en_front, en_body)
    check_custody!
  when "closeout"
    check_closeout_map!(freeze, author_case, map_data, stylized_data, stylized_manifest, include_text, es_body, en_body, research_root)
    check_custody!
  when "claims"
    nil
  else
    raise VerificationError, "seleccione --claims-only, --lang es|en, --parity, --causal-language, --custody, --closeout o --all"
  end
  puts JSON.generate(result: "PASS", mode: options[:mode], strict: $strict, freeze_sha256: FREEZE_SHA256, visuals: 6, stylized_visuals: 6, soft_warnings: soft_warnings, wording_warnings: $wording_warnings)
rescue VerificationError, KeyError, JSON::ParserError, Psych::SyntaxError, REXML::ParseException => e
  warn JSON.generate(result: "FAIL", error: e.message, self_test: options[:self_test])
  exit 1
end
