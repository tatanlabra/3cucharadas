#!/usr/bin/env ruby
# frozen_string_literal: true

require "fileutils"
require "digest"
require "json"
require "open3"
require "optparse"
require "pathname"
require "tmpdir"
require "yaml"

def options
  result = { root: Pathname.pwd, staged: false, external_papers: nil, thesis_root: nil, self_test: false }
  OptionParser.new do |parser|
    parser.banner = "Usage: verify_thesis_recreation_post_i_ready_review.rb [options]"
    parser.on("--root PATH") { |value| result[:root] = Pathname(value) }
    parser.on("--staged") { result[:staged] = true }
    parser.on("--external-papers PATH") { |value| result[:external_papers] = Pathname(value).expand_path }
    parser.on("--thesis-root PATH") { |value| result[:thesis_root] = Pathname(value).expand_path }
    parser.on("--self-test") { result[:self_test] = true }
  end.parse!
  result
end

def yaml(path)
  YAML.safe_load(path.read, permitted_classes: [Date, Time], aliases: false)
end

def document(path)
  text = path.read
  match = text.match(/\A---\s*\n(.*?)\n---\s*\n/m)
  raise "Front matter missing: #{path}" unless match

  [YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: false), text[match.end(0)..]]
end

def add(errors, control, condition, message)
  errors[control] << message unless condition
end

def resolve_evidence(specification, repository)
  if specification.fetch("commit") == "WORKTREE"
    path = repository.join(specification.fetch("path"))
    return { available: false } unless path.file?

    head, head_status = Open3.capture2e("git", "-C", repository.to_s, "rev-parse", "HEAD")
    blob, blob_status = Open3.capture2e(
      "git", "-C", repository.to_s, "hash-object", specification.fetch("path")
    )
    return {
      available: true,
      payload: path.binread,
      blob: blob.strip,
      blob_ok: blob_status.success?,
      base_ok: head_status.success? && head.strip == specification.fetch("base_commit")
    }
  end

  revision = "#{specification.fetch('commit')}:#{specification.fetch('path')}"
  blob, blob_status = Open3.capture2e("git", "-C", repository.to_s, "rev-parse", revision)
  payload, payload_status = Open3.capture2e("git", "-C", repository.to_s, "show", revision)
  {
    available: payload_status.success?,
    payload: payload,
    blob: blob.strip,
    blob_ok: blob_status.success?,
    base_ok: true
  }
end

def staged_paths(root)
  output, status = Open3.capture2e("git", "-C", root.to_s, "diff", "--cached", "--name-only", "-z")
  raise "Cannot inspect staged paths: #{output.strip}" unless status.success?

  output.split("\0").reject(&:empty?).sort
end

def validate(root, staged:, external_papers:, thesis_root:)
  errors = Hash.new { |hash, key| hash[key] = [] }
  contract_path = root.join("docs/contracts/thesis-recreation-post-i-ready-review.yaml")
  add(errors, "C0", contract_path.file?, "contract file is missing")
  return errors unless contract_path.file?

  contract = yaml(contract_path)
  required = %w[id version authorization status_target scope evidence commit required_front_matter controls final_contract]
  add(errors, "C0", required.all? { |key| contract.key?(key) }, "contract schema is incomplete")
  return errors unless errors.empty?
  add(errors, "C0", contract["version"] == 10, "contract version must be 10")
  add(errors, "C0", contract["status_target"] == "READY_FOR_PUBLICATION_NO_DISTRIBUTION", "contract status target drifted")
  add(errors, "C0", contract.fetch("controls").map { |row| row.fetch("id") } == (0..14).map { |number| "C#{number}" }, "contract controls must be exactly C0-C14 in order")
  add(errors, "C0", contract.dig("final_contract", "requirement").to_s.include?("C0–C14"), "final contract does not bind all controls")

  expected_paths = contract.dig("commit", "paths").sort
  expected_deletions = Array(contract.dig("commit", "deletions")).sort
  expected_paths.each { |path| add(errors, "C0", root.join(path).file?, "required path is missing: #{path}") }
  expected_deletions.each { |path| add(errors, "C0", !root.join(path).exist?, "required deletion is still present: #{path}") }
  add(errors, "C0", contract.dig("scope", "excluded").include?("penta-agent"), "penta-agent is not excluded")

  documents = contract.dig("scope", "documents")
  headers = {}
  bodies = {}
  documents.each do |language, relative|
    path = root.join(relative)
    if path.file?
      headers[language], bodies[language] = document(path)
    else
      add(errors, "C5", false, "publication source missing: #{relative}")
    end
  end
  contract.dig("required_front_matter").each do |language, expected|
    expected.each { |key, value| add(errors, "C5", headers.dig(language, key) == value, "#{language} front matter drifted: #{key}") }
  end
  add(errors, "C5", headers.dig("es", "title").to_s != "" && headers.dig("en", "title").to_s != "", "a title is missing")
  add(errors, "C5", headers.dig("es", "date") == headers.dig("en", "date"), "dates diverged")
  reduction = contract.dig("evidence", "editorial_reduction")
  hard_reduction = {
    "baseline_commit" => "fac3b3f6d9d6cb919061653199b1f7bdd7b057fa",
    "unit" => "Unicode characters including front matter",
    "maximum_after_per_draft" => 30_000,
    "before" => { "es" => 50_589, "en" => 50_562 }
  }
  add(errors, "C5", reduction == hard_reduction, "editorial reduction baseline or limit drifted")
  documents.each do |language, relative|
    next unless root.join(relative).file?

    add(errors, "C5", root.join(relative).read.length <= 30_000, "#{language} draft exceeds the 30,000-character limit")
  end

  headings = {
    "es" => ["## Cucharada 1", "## Cucharada 2", "## Cucharada 3", "## Cierre"],
    "en" => ["## Spoonful 1", "## Spoonful 2", "## Spoonful 3", "## Closing"]
  }
  headings.each { |language, list| list.each { |needle| add(errors, "C5", bodies.fetch(language, "").include?(needle), "#{language} heading missing: #{needle}") } }

  checks = {
    "es" => {
      "C2" => ["El mercado mutó muy rápido", "La IA al menos publica notas de versión", "[^regimenes]"],
      "C3" => ["Python", "invocó Stata 17 mediante `stata-mp`", "14 rutas activas", "reejecución actual trazable", "Nada de lo que sigue es causal", "Con datos de 2002 a 2012", "dos comunidades rurales del sur", "Mi panel (datos que siguen", "La tesis es mía y la auditoría también: no es una réplica independiente"],
      "C4" => ["50 hipótesis", "37 quedaron refutadas, 11 sostenidas, 1 parcial y 1 refutada para once de catorce términos", "34 juicios", "quince juicios quedaron correctamente respaldados", "ninguno permanece como error conocido en la salida canónica de 2026", "doce convergencias, diez divergencias explicadas y cuatro sin prueba numérica", "Fórmulas productoras: 80/80 y 40/40 puntos", "Planilla y gráfico incrustado: 80/80 puntos", "salida canónica de 2026 sin errores conocidos"],
      "C8" => ["Todo el itinerario computacional disponible volvió a ejecutarse; eso no hizo que todos los resultados fueran iguales.", "10 de 20 coeficientes", "4 de 12 coinciden", "| Coincidencia | 3 |", "| Diferencia | 2 |", "| No comparable por diseño | 4 |"],
      "C10" => ["`do_058`", "`do_059`", "`do_060`", "recuperación gobernada", "[^harvest]:"],
      "C11" => ["para que una reparación técnica no reescriba la evidencia histórica", "reejecutable no significa recreable; recreable no significa coincidente; coincidente no significa correcto; correcto no significa causal", "### De describir el cierre a identificar una política", "no crea el contrafactual que falta", "**Alerta descriptiva/predictiva**", "**Reforma escalonada**", "**Consecuencias del cierre**"],
      "C12" => ["10 de los 11 efectos fijos publicados", "12 coeficientes en el archivo, 11 efectos en el cuadro y 10 coincidencias", "solo para el universo reconstruido del Gran Santiago", "visible retrospectivamente durante los siete años previos", "mayor consecuencia interpretativa para la política pública", "**Tabla 4** — Qué uso público resiste y dónde termina la evidencia", "Lo que no autoriza"],
      "C14" => ["invocó Stata 17 mediante `stata-mp`", "14 rutas activas", "reejecución actual trazable", "[^stata17]: Recibo técnico fijado", "15/15 roles", "`c(MP)=1`", "`c(flavor)=IC`", "[^harvest]: Cosecha de salidas fijada"]
    },
    "en" => {
      "C2" => ["school market changed rules faster than AI", "[^regimenes]"],
      "C3" => ["Python", "invoked Stata 17 through `stata-mp`", "14 active routes", "traceable present-day rerun", "Nothing below is causal", "With data from 2002 to 2012", "two rural communities in southern Chile", "My panel (data that follow", "The thesis is mine and so is the audit: this is not an independent replication"],
      "C4" => ["50 hypotheses", "37 were refuted, 11 sustained, 1 partial, and 1 refuted for eleven of fourteen terms", "34 judgements", "fifteen judgements were correctly supported", "none remains as a known error in the canonical 2026 output", "twelve converge, ten have explained divergences, and four lack a numerical test", "Producer formulas: 80/80 and 40/40 points", "Workbook and embedded chart: 80/80 points", "canonical 2026 output with no known errors"],
      "C8" => ["Every available computational route ran again; that did not make every result equal.", "10 of 20 coefficients", "4 of 12 match", "| Match | 3 |", "| Mismatch | 2 |", "| Not comparable by design | 4 |"],
      "C10" => ["`do_058`", "`do_059`", "`do_060`", "governed recovery", "[^harvest]:"],
      "C11" => ["so a repair cannot rewrite historical evidence", "rerunnable does not mean rebuildable; rebuildable does not mean matching; matching does not mean correct; correct does not mean causal", "### From describing closure to identifying a policy", "do not create the missing counterfactual", "**Descriptive/predictive warning**", "**Staggered reform**", "**Consequences of closure**"],
      "C12" => ["10 of the 11 published fixed effects", "12 coefficients in the file, 11 effects in the table, and 10 matches", "only for the reconstructed Greater Santiago universe", "visible retrospectively across the previous seven years", "largest interpretive consequence for public policy", "**Table 4** — What public use survives, and where the evidence ends", "What it does not authorise"],
      "C14" => ["invoked Stata 17 through `stata-mp`", "14 active routes", "traceable present-day rerun", "[^stata17]: Technical receipt pinned", "15/15 roles", "`c(MP)=1`", "`c(flavor)=IC`", "[^harvest]: Output harvest pinned"]
    }
  }
  checks.each { |language, controls| controls.each { |control, needles| needles.each { |needle| add(errors, control, bodies.fetch(language, "").include?(needle), "#{language} missing: #{needle}") } } }
  unverified_attribution = /(?:no he logrado verificar|have not managed to verify)/i
  bodies.each { |language, body| add(errors, "C3", !body.match?(unverified_attribution), "#{language} retains an unverified attribution") }
  policy_locations = {
    "es" => ["La primera conclusión sí resistió", "Con datos de 2002 a 2012", "También sobrevivieron varios resultados más pequeños"],
    "en" => ["The first conclusion held", "With data from 2002 to 2012", "Several smaller results survived too"]
  }
  policy_locations.each do |language, (flow, policy, next_object)|
    body = bodies.fetch(language, "")
    add(errors, "C3", body.index(flow) && body.index(policy) && body.index(next_object) && body.index(flow) < body.index(policy) && body.index(policy) < body.index(next_object), "#{language} policy bridge is not between the flow and second object")
  end
  %w[regimenes christensen2018 clemens2015 herndon2013 hamermesh2007 paredes2018 nunez2014].each do |note|
    bodies.each { |language, body| add(errors, "C1", body.include?("[^#{note}]:"), "#{language} note missing: #{note}") }
  end

  literature_path = root.join("research/replica-tesis/literature.yml")
  accounting_path = root.join("research/replica-tesis/hypothesis-accounting.md")
  if literature_path.file?
    literature = yaml(literature_path)
    sources = literature.fetch("sources")
    expected_dois = %w[10.1257/jel.20171350 10.1111/joes.12139 10.1093/cje/bet075 10.1111/j.1365-2966.2007.00428.x]
    add(errors, "C1", sources.map { |source| source["doi"] }.sort == expected_dois.sort, "literature DOI set drifted")
    sources.each do |source|
      add(errors, "C1", source["apa"].to_s.include?(source["doi"].to_s), "APA lacks DOI: #{source["key"]}")
      add(errors, "C1", source["abstract_source"].to_s != "", "abstract source missing: #{source["key"]}")
      add(errors, "C1", %w[resolved unavailable].include?(source["oa_status"]), "invalid OA status: #{source["key"]}")
    end
    regimes = literature.fetch("historical_regimes")
    add(errors, "C2", regimes.map { |row| row["period"] } == %w[1980s 1990s 2000s 2010s 2020s], "historical periods drifted")
    add(errors, "C2", regimes.all? { |row| row["source"].to_s.start_with?("https://www.bcn.cl/") }, "regime sources must be BCN")
    contextual_sources = literature.fetch("contextual_sources")
    add(errors, "C1", contextual_sources.map { |source| source["key"] }.sort == %w[nunez2014 paredes2018], "contextual source set drifted")
    nunez = contextual_sources.find { |source| source["key"] == "nunez2014" }
    add(errors, "C1", nunez&.fetch("doi", nil) == "10.11144/Javeriana.UPSY13-2.qscc", "Núñez DOI drifted")
    christensen = sources.find { |source| source["key"] == "christensen2018" }
    add(errors, "C1", christensen&.fetch("oa_status", nil) == "resolved", "Christensen OA resolution missing")
    paper_sources = sources + contextual_sources
    paper_sources.each do |source|
      external = source["external_pdf"]
      add(errors, "C1", external.is_a?(Hash) && external["filename"].to_s != "" && external["sha256"].to_s.match?(/\A[0-9a-f]{64}\z/), "external PDF record is incomplete: #{source["key"]}")
    end
    repository_pdfs = Dir.glob(root.join("research/replica-tesis/**/*.pdf").to_s)
    add(errors, "C1", repository_pdfs.empty?, "repository contains PDF(s): #{repository_pdfs.join(', ')}")
    if external_papers
      add(errors, "C1", external_papers.directory?, "external paper directory is absent: #{external_papers}")
      if external_papers.directory?
        paper_sources.each do |source|
          external = source.fetch("external_pdf")
          cache = external_papers.join(external.fetch("filename"))
          add(errors, "C1", cache.file?, "external PDF is absent: #{external.fetch("filename")}")
          add(errors, "C1", File.binread(cache, 5) == "%PDF-", "external PDF is not a PDF: #{external.fetch("filename")}") if cache.file?
          add(errors, "C1", Digest::SHA256.file(cache).hexdigest == external.fetch("sha256"), "external PDF digest drifted: #{external.fetch("filename")}") if cache.file?
        end
      end
    end
  else
    add(errors, "C1", false, "literature metadata is missing")
  end

  source = contract.dig("evidence", "primary_hypothesis_registry")
  source_keys = %w[repository commit path git_blob sha256 hypotheses_tested outcomes]
  add(errors, "C4", source.is_a?(Hash) && source_keys.all? { |key| source.key?(key) }, "primary F4 registry specification is incomplete")
  if source.is_a?(Hash) && source_keys.all? { |key| source.key?(key) }
    expected_outcomes = source.fetch("outcomes")
    expected_outcomes = expected_outcomes.transform_values(&:to_i) if expected_outcomes.is_a?(Hash)
    add(errors, "C4", expected_outcomes == { "REFUTADA" => 37, "SOSTENIDA" => 11, "PARCIAL" => 1, "REFUTADA_PARA_ONCE_TERMINOS" => 1 }, "primary F4 expected outcomes drifted")
    if thesis_root.nil?
      add(errors, "C4", false, "--thesis-root is required to verify the primary F4 registry")
    elsif !thesis_root.directory?
      add(errors, "C4", false, "thesis root is absent: #{thesis_root}")
    else
      resolved = resolve_evidence(source, thesis_root)
      add(errors, "C4", resolved[:available], "primary F4 evidence is unavailable")
      add(errors, "C4", resolved[:base_ok], "primary F4 worktree base commit drifted")
      add(errors, "C4", resolved[:blob_ok] && resolved[:blob] == source.fetch("git_blob"), "primary F4 Git blob drifted")
      if resolved[:available]
        payload = resolved.fetch(:payload)
        add(errors, "C4", Digest::SHA256.hexdigest(payload) == source.fetch("sha256"), "primary F4 SHA-256 drifted")
        begin
          registry = JSON.parse(payload)
          add(errors, "C4", registry.dig("summary", "hypotheses_tested") == source.fetch("hypotheses_tested"), "primary F4 hypothesis total drifted")
          add(errors, "C4", registry.fetch("hypotheses").length == source.fetch("hypotheses_tested"), "primary F4 row count drifted")
          add(errors, "C4", registry.dig("summary", "by_outcome") == expected_outcomes, "primary F4 outcome counts drifted")
        rescue JSON::ParserError
          add(errors, "C4", false, "primary F4 evidence is not valid JSON")
        end
      end
    end
    accounting_complete = accounting_path.file? && [source.fetch("commit"), source.fetch("git_blob"), source.fetch("sha256"), "50 filas", "REFUTADA", "SOSTENIDA", "PARCIAL", "REFUTADA_PARA_ONCE_TERMINOS", "34 juicios"].all? { |needle| accounting_path.read.include?(needle) }
    add(errors, "C4", accounting_complete, "hypothesis accounting record is incomplete")
  end

  judgments = contract.dig("evidence", "editorial_judgment_registry")
  judgment_keys = %w[repository commit path git_blob sha256 judgments verdict_counts expected_verdicts]
  add(errors, "C4", judgments.is_a?(Hash) && judgment_keys.all? { |key| judgments.key?(key) }, "F5 judgment registry specification is incomplete")
  if judgments.is_a?(Hash) && judgment_keys.all? { |key| judgments.key?(key) }
    hard_verdicts = {
      "J-017" => "CALCE_CORRECTO",
      "J-010" => "CALCE_CORRECTO",
      "J-011" => "CALCE_CORRECTO",
      "J-016" => "CALCE_CORRECTO",
      "J-026" => "CALCE_CORRECTO"
    }
    hard_counts = {
      "CALCE_CORRECTO" => 15,
      "DESCALCE_ERROR_PASADO" => 10,
      "DESCALCE_AMBOS_MAL" => 1,
      "CALCE_HEREDADO" => 1,
      "LIMITE_DECLARADO" => 2,
      "NO_NUMERICO_ESTRUCTURAL" => 3,
      "PROCEDENCIA_VERIFICADA" => 2
    }
    add(errors, "C4", judgments.fetch("judgments") == 34, "F5 judgment total drifted")
    add(errors, "C4", judgments.fetch("verdict_counts") == hard_counts, "F5 verdict counts drifted")
    add(errors, "C4", judgments.fetch("expected_verdicts") == hard_verdicts, "F5 expected verdicts drifted")
    if thesis_root.nil?
      add(errors, "C4", false, "--thesis-root is required to verify the F5 judgment registry")
    elsif !thesis_root.directory?
      add(errors, "C4", false, "thesis root is absent: #{thesis_root}")
    else
      resolved = resolve_evidence(judgments, thesis_root)
      add(errors, "C4", resolved[:available], "F5 judgment evidence is unavailable")
      add(errors, "C4", resolved[:base_ok], "F5 judgment worktree base commit drifted")
      add(errors, "C4", resolved[:blob_ok] && resolved[:blob] == judgments.fetch("git_blob"), "F5 judgment Git blob drifted")
      if resolved[:available]
        payload = resolved.fetch(:payload)
        add(errors, "C4", Digest::SHA256.hexdigest(payload) == judgments.fetch("sha256"), "F5 judgment SHA-256 drifted")
        begin
          registry = JSON.parse(payload)
          rows = registry.fetch("judgments")
          verdicts = rows.to_h { |row| [row.fetch("id"), row.fetch("veredicto")] }
          add(errors, "C4", registry.dig("summary", "judgments") == judgments.fetch("judgments"), "F5 judgment summary drifted")
          add(errors, "C4", rows.length == judgments.fetch("judgments"), "F5 judgment row count drifted")
          add(errors, "C4", registry.dig("summary", "by_verdict") == hard_counts, "F5 registry counts drifted")
          hard_verdicts.each do |id, verdict|
            add(errors, "C4", verdicts[id] == verdict, "F5 verdict drifted: #{id}")
          end
        rescue JSON::ParserError, KeyError
          add(errors, "C4", false, "F5 judgment evidence is not a valid complete JSON registry")
        end
      end
    end
    table_rows = {
      "es" => [
        "| Alumnos por docente | 48 celdas | Hoja `rad`: 48/48; cálculo alternativo separado | Vector productor verificado |",
        "| Brecha SIMCE, subvencionados que cierran | −4,3 | Hoja productora: −4,3 | Valor productor verificado |",
        "| Movilidad bruta y tasas | 6,3; 4,5; 1,6 | Fórmulas productoras: 80/80 y 40/40 puntos | Calce final correcto |",
        "| Movilidad neta | Entradas − salidas | Planilla y gráfico incrustado: 80/80 puntos | Calce final correcto; interpretación causal no probada |",
        "| Brecha PSU | ≈ 10 | Resultado final: 10,40, no 11,25 | Calce final correcto |"
      ],
      "en" => [
        "| Pupils per teacher | 48 cells | `rad`: 48/48; alternative calculation separated | Producer vector verified |",
        "| SIMCE gap, closing subsidised schools | −4.3 | Producer sheet: −4.3 | Producer value verified |",
        "| Gross mobility and rates | 6.3; 4.5; 1.6 | Producer formulas: 80/80 and 40/40 points | Correct final match |",
        "| Net mobility | Entries − exits | Workbook and embedded chart: 80/80 points | Correct final match; causal interpretation unproven |",
        "| PSU gap | ≈ 10 | Final result: 10.40, not 11.25 | Correct final match |"
      ]
    }
    table_rows.each do |language, rows|
      rows.each { |row| add(errors, "C4", bodies.fetch(language, "").include?(row), "#{language} F5 table mapping drifted: #{row}") }
    end
  end

  comparison = contract.dig("evidence", "result_comparison")
  comparison_keys = %w[repository commit path git_blob sha256 expected]
  add(errors, "C8", comparison.is_a?(Hash) && comparison_keys.all? { |key| comparison.key?(key) }, "result comparison specification is incomplete")
  if comparison.is_a?(Hash) && comparison_keys.all? { |key| comparison.key?(key) }
    expected = comparison.fetch("expected")
    hard_expected = {
      "status" => "COMPLETE_WITH_CLASSIFIED_LIMITS",
      "reopened_cases" => 9,
      "execution_terminal" => 9,
      "comparison_terminal" => 9,
      "matches" => 3,
      "mismatches" => 2,
      "not_comparable_by_design" => 4,
      "inferential_models" => 4,
      "central_claim" => "Todo el itinerario computacional disponible volvió a ejecutarse; eso no hizo que todos los resultados fueran iguales."
    }
    add(errors, "C8", expected == hard_expected, "result comparison expectations drifted")
    if thesis_root.nil?
      add(errors, "C8", false, "--thesis-root is required to verify the result comparison")
    elsif !thesis_root.directory?
      add(errors, "C8", false, "thesis root is absent: #{thesis_root}")
    else
      resolved = resolve_evidence(comparison, thesis_root)
      add(errors, "C8", resolved[:available], "result comparison evidence is unavailable")
      add(errors, "C8", resolved[:base_ok], "result comparison worktree base commit drifted")
      add(errors, "C8", resolved[:blob_ok] && resolved[:blob] == comparison.fetch("git_blob"), "result comparison Git blob drifted")
      if resolved[:available]
        payload = resolved.fetch(:payload)
        add(errors, "C8", Digest::SHA256.hexdigest(payload) == comparison.fetch("sha256"), "result comparison SHA-256 drifted")
        begin
          result = JSON.parse(payload)
          summary = result.fetch("summary")
          cases = result.fetch("reopened_cases")
          models = result.fetch("inferential_audit")
          add(errors, "C8", result.fetch("status") == expected.fetch("status"), "result comparison status drifted")
          %w[reopened_cases execution_terminal comparison_terminal matches mismatches not_comparable_by_design inferential_models].each do |key|
            add(errors, "C8", summary.fetch(key) == expected.fetch(key), "result comparison count drifted: #{key}")
          end
          add(errors, "C8", cases.length == 9, "result comparison case rows drifted")
          add(errors, "C8", cases.all? { |row| %w[REEXECUTED REGENERATED TRACE_ONLY].include?(row["execution_status"]) }, "a result comparison execution is non-terminal")
          add(errors, "C8", cases.all? { |row| %w[MATCH MISMATCH NOT_COMPARABLE_BY_DESIGN].include?(row["comparison_status"]) }, "a result comparison is non-terminal")
          add(errors, "C8", cases.all? { |row| row["attribution_status"] != "PENDING" }, "an attribution remains pending")
          add(errors, "C8", models.map { |row| row["display_id"] } == %w[TABLE-05 TABLE-06 TABLE-07 TABLE-08], "inferential model set drifted")
          add(errors, "C8", models.all? { |row| row["causal_boundary"] == "ASSOCIATIONAL_ONLY" }, "a model crossed the causal boundary")
          add(errors, "C8", models.find { |row| row["display_id"] == "TABLE-05" }&.fetch("strict_display_matches", nil) == "10/20 coefficients; 11/20 SE", "Table 5 strict match drifted")
          add(errors, "C8", models.find { |row| row["display_id"] == "TABLE-08" }&.fetch("strict_display_matches", nil) == "4/12 parameters", "Table 8 strict match drifted")
          add(errors, "C8", result.dig("claims_boundary", "authorized_claims").include?(expected.fetch("central_claim")), "central result claim drifted")
        rescue JSON::ParserError, KeyError
          add(errors, "C8", false, "result comparison evidence is not valid complete JSON")
        end
      end
    end
  end

  carousel = contract.dig("evidence", "face_to_face_carousel")
  carousel_keys = %w[repository commit path git_blob sha256 expected]
  add(errors, "C9", carousel.is_a?(Hash) && carousel_keys.all? { |key| carousel.key?(key) }, "carousel evidence specification is incomplete")
  carousel_data_path = root.join("_data/thesis_recreation_face_to_face.yml")
  carousel_include_path = root.join("_includes/evidence-carousel.html")
  carousel_script_path = root.join("assets/js/evidence-carousel.js")
  carousel_css_path = root.join("assets/css/main.scss")
  [carousel_data_path, carousel_include_path, carousel_script_path, carousel_css_path].each do |path|
    add(errors, "C9", path.file?, "carousel component file is missing: #{path.relative_path_from(root)}")
  end
  if carousel.is_a?(Hash) && carousel_keys.all? { |key| carousel.key?(key) }
    hard_carousel_expected = {
      "status" => "READY_FOR_BLOG_INTEGRATION",
      "slides" => 6,
      "assets" => 18,
      "historical_execution" => "HISTORICAL_EXECUTION_NOT_VERIFIED",
      "causal_boundary" => "ASSOCIATIONAL_ONLY",
      "slide_order" => %w[table-04-exact figure-01-pattern figure-11-hhi figure-02-rates table-08-rounding figure-04-net-mobility]
    }
    add(errors, "C9", carousel.fetch("expected") == hard_carousel_expected, "carousel expectations drifted")
    technical_manifest = nil
    if thesis_root.nil?
      add(errors, "C9", false, "--thesis-root is required to verify carousel provenance")
    elsif !thesis_root.directory?
      add(errors, "C9", false, "thesis root is absent: #{thesis_root}")
    else
      resolved = resolve_evidence(carousel, thesis_root)
      add(errors, "C9", resolved[:available], "carousel evidence is unavailable")
      add(errors, "C9", resolved[:base_ok], "carousel worktree base commit drifted")
      add(errors, "C9", resolved[:blob_ok] && resolved[:blob] == carousel.fetch("git_blob"), "carousel Git blob drifted")
      if resolved[:available]
        payload = resolved.fetch(:payload)
        add(errors, "C9", Digest::SHA256.hexdigest(payload) == carousel.fetch("sha256"), "carousel manifest SHA-256 drifted")
        begin
          technical_manifest = JSON.parse(payload)
          add(errors, "C9", technical_manifest["status"] == hard_carousel_expected["status"], "carousel technical status drifted")
          add(errors, "C9", technical_manifest["slide_order"] == hard_carousel_expected["slide_order"], "carousel technical order drifted")
          add(errors, "C9", technical_manifest.fetch("slides").length == hard_carousel_expected["slides"], "carousel technical slide count drifted")
          add(errors, "C9", technical_manifest.fetch("assets").length == hard_carousel_expected["assets"], "carousel technical asset count drifted")
          add(errors, "C9", technical_manifest.dig("claims", "historical_execution") == hard_carousel_expected["historical_execution"], "carousel historical boundary drifted")
          add(errors, "C9", technical_manifest.dig("claims", "causal_boundary") == hard_carousel_expected["causal_boundary"], "carousel causal boundary drifted")
        rescue JSON::ParserError, KeyError
          add(errors, "C9", false, "carousel evidence is not a valid complete manifest")
        end
      end
    end

    if carousel_data_path.file?
      begin
        data = yaml(carousel_data_path)
        add(errors, "C9", data.dig("technical", "commit") == carousel.fetch("commit"), "carousel data technical commit drifted")
        add(errors, "C9", data.dig("technical", "manifest") == carousel.fetch("path"), "carousel data manifest path drifted")
        add(errors, "C9", data.dig("technical", "manifest_sha256") == carousel.fetch("sha256"), "carousel data manifest digest drifted")
        add(errors, "C9", data.dig("technical", "historical_execution") == "HISTORICAL_EXECUTION_NOT_VERIFIED", "carousel data promotes historical execution")
        add(errors, "C9", data.dig("technical", "causal_boundary") == "ASSOCIATIONAL_ONLY", "carousel data crosses the causal boundary")
        expected_verdicts = {
          "es" => ["Acerté: 12 de 12", "La conclusión sobrevivió", "Me equivoqué en 2014", "Recreación exacta", "Parece que truncé ocho valores", "Recreación exacta"],
          "en" => ["I got it right: 12 of 12", "The conclusion survived", "I was wrong in 2014", "Exact reconstruction", "I appear to have truncated eight values", "Exact reconstruction"]
        }
        referenced_assets = []
        expected_verdicts.each do |language, verdicts|
          slides = data.dig("locales", language, "slides") || []
          add(errors, "C9", slides.map { |slide| slide["id"] } == hard_carousel_expected["slide_order"], "#{language} carousel order drifted")
          add(errors, "C9", slides.map { |slide| slide["verdict"] } == verdicts, "#{language} carousel verdicts drifted")
          add(errors, "C9", slides.all? { |slide| slide["original_alt"].to_s != "" && slide["recreated_alt"].to_s != "" }, "#{language} carousel alt text is incomplete")
          referenced_assets.concat(slides.flat_map { |slide| [slide["original_asset"], slide["recreated_asset"]] })
        end
        assets = data.fetch("assets", {})
        add(errors, "C9", assets.length == 18, "carousel data must declare 18 assets")
        add(errors, "C9", referenced_assets.uniq.sort == assets.keys.sort, "carousel slides do not reference the exact asset set")
        if technical_manifest
          by_file = technical_manifest.fetch("assets").to_h { |asset| [asset.fetch("file"), asset] }
          assets.each do |key, asset|
            technical_asset = by_file[asset["file"]]
            add(errors, "C9", !technical_asset.nil?, "carousel asset is absent from technical manifest: #{key}")
            next unless technical_asset

            %w[sha256 width height].each do |field|
              add(errors, "C9", asset[field] == technical_asset[field], "carousel asset #{field} drifted: #{key}")
            end
            relative = asset.fetch("path").sub(%r{\A/}, "")
            file = root.join(relative)
            add(errors, "C9", file.file?, "carousel asset file is missing: #{relative}")
            add(errors, "C9", Digest::SHA256.file(file).hexdigest == asset["sha256"], "carousel asset file digest drifted: #{relative}") if file.file?
          end
          add(errors, "C9", assets.values.map { |asset| asset["file"] }.sort == by_file.keys.sort, "carousel technical and editorial asset sets diverged")
        end
      rescue KeyError, Psych::SyntaxError
        add(errors, "C9", false, "carousel data is not valid complete YAML")
      end
    end

    include_call = "{% include evidence-carousel.html %}"
    insertion_anchors = {
      "es" => ["## Cucharada 3:", "**Tabla 3**"],
      "en" => ["## Spoonful 3:", "**Table 3**"]
    }
    insertion_anchors.each do |language, (section_heading, table)|
      body = bodies.fetch(language, "")
      section_at = body.index(section_heading)
      include_at = body.index(include_call)
      table_at = body.index(table)
      next_section_at = section_at ? body.index("\n## ", section_at + section_heading.length) : nil
      prefix = section_at && include_at && section_at < include_at ? body[section_at...include_at] : ""
      add(errors, "C9", body.scan(include_call).length == 1, "#{language} must include the carousel exactly once")
      add(errors, "C9", section_at && include_at && table_at && next_section_at && section_at < include_at && include_at < table_at && table_at < next_section_at && !prefix.include?("\n### "), "#{language} carousel is not at the start of Spoonful 3")
    end

    if carousel_include_path.file?
      markup = carousel_include_path.read
      required_markup = ['role="region"', 'aria-roledescription="carousel"', 'role="group"', 'aria-roledescription="slide"', 'data-carousel-previous', 'data-carousel-next', 'data-carousel-dot', 'aria-live="polite"', 'tabindex="0"', 'loading="lazy"', 'image-popup', 'data-carousel-popup', 'data-carousel-hd-link', 'target="_blank"', 'rel="noopener"']
      required_markup.each { |needle| add(errors, "C9", markup.include?(needle), "carousel markup missing: #{needle}") }
    end
    if carousel_script_path.file?
      script = carousel_script_path.read
      %w[ArrowLeft ArrowRight Home End scrollTo ResizeObserver].each { |needle| add(errors, "C9", script.include?(needle), "carousel controller missing: #{needle}") }
      %w[setInterval autoplay data-ride new\ Swiper slick Glide].each { |needle| add(errors, "C9", !script.include?(needle.gsub("\\ ", " ")), "carousel controller contains prohibited automation/library token: #{needle}") }
    end
    if carousel_css_path.file?
      css = carousel_css_path.read
      %w[.evidence-carousel scroll-snap-type .evidence-carousel__panels prefers-reduced-motion academic-night].each { |needle| add(errors, "C9", css.include?(needle), "carousel CSS missing: #{needle}") }
    end
  end

  pipeline = contract.dig("evidence", "reconstruction_pipeline")
  pipeline_keys = %w[renderer expected artifacts]
  add(errors, "C11", pipeline.is_a?(Hash) && pipeline_keys.all? { |key| pipeline.key?(key) }, "reconstruction pipeline specification is incomplete")
  if pipeline.is_a?(Hash) && pipeline_keys.all? { |key| pipeline.key?(key) }
    hard_renderer = {
      "name" => "d2",
      "version" => "v0.7.1",
      "layout" => "elk",
      "theme" => 200,
      "command" => "DEBUG=0 d2 --theme=200 --layout=elk --elk-nodeNodeBetweenLayers=20 --elk-edgeNodeBetweenLayers=12 --pad=6 SOURCE.d2 OUTPUT.svg",
      "annotation_command" => "python3 annotate_svg.py OUTPUT.svg --title TITLE --description DESCRIPTION"
    }
    hard_pipeline_expected = {
      "inputs" => 3,
      "gates" => 4,
      "gate_chain" => "shared_once",
      "outcomes" => %w[matches differs not_comparable declared_limit],
      "placement" => "spoonful_2_before_first_subheading",
      "causal_boundary_es" => "reejecutable no significa recreable; recreable no significa coincidente; coincidente no significa correcto; correcto no significa causal",
      "causal_boundary_en" => "rerunnable does not mean rebuildable; rebuildable does not mean matching; matching does not mean correct; correct does not mean causal"
    }
    hard_artifacts = [
      {
        "language" => "es", "surface" => "desktop",
        "source" => "assets/images/replica-tesis-establecimientos/pipeline-recreacion-es.d2",
        "source_sha256" => "0fb223471c608417883f0e6364c056a9d45af22f72263cebcee4385580788a1d",
        "svg" => "assets/images/replica-tesis-establecimientos/pipeline-recreacion-es.svg",
        "svg_sha256" => "a78e14ec33ba5eec57d35c6bea645380a62a569e185a8a411fc2c5459fa8f3ec"
      },
      {
        "language" => "es", "surface" => "mobile",
        "source" => "assets/images/replica-tesis-establecimientos/pipeline-recreacion-es-mobile.d2",
        "source_sha256" => "52e3d2040d38aabb91b7d08a93e7364d58cf5be16f62983578113c96acff9b4f",
        "svg" => "assets/images/replica-tesis-establecimientos/pipeline-recreacion-es-mobile.svg",
        "svg_sha256" => "0523f36d22aa4608151593d076c496a8f3191502bb0b27d5dcbc5c6aee876593"
      },
      {
        "language" => "en", "surface" => "desktop",
        "source" => "assets/images/replica-tesis-establecimientos/pipeline-recreacion-en.d2",
        "source_sha256" => "f165e5240c47db011c8dd6e95afe1cf22e7b4e68f2ad4a8e7c2875330fa4213e",
        "svg" => "assets/images/replica-tesis-establecimientos/pipeline-recreacion-en.svg",
        "svg_sha256" => "fe1224e2762849a8583365ae06ecb93697a742372c5aec4c3abc7237f9f26ade"
      },
      {
        "language" => "en", "surface" => "mobile",
        "source" => "assets/images/replica-tesis-establecimientos/pipeline-recreacion-en-mobile.d2",
        "source_sha256" => "0f6140ea10e096fe7837fd56201f6a26a07645d7f9a1611f0a820c2eac9a50f3",
        "svg" => "assets/images/replica-tesis-establecimientos/pipeline-recreacion-en-mobile.svg",
        "svg_sha256" => "20bb6a12b8986f17fc13cd10e27c88dbb74b99b818f02263d1bc4b28f747c5e9"
      }
    ]
    add(errors, "C11", pipeline.fetch("renderer") == hard_renderer, "D2 renderer specification drifted")
    add(errors, "C11", pipeline.fetch("expected") == hard_pipeline_expected, "pipeline semantic expectations drifted")
    add(errors, "C11", pipeline.fetch("artifacts") == hard_artifacts, "pipeline artifact manifest drifted")

    hard_artifacts.each do |artifact|
      source_path = root.join(artifact.fetch("source"))
      svg_path = root.join(artifact.fetch("svg"))
      add(errors, "C11", source_path.file?, "D2 source is missing: #{artifact.fetch('source')}")
      add(errors, "C11", svg_path.file?, "D2 SVG is missing: #{artifact.fetch('svg')}")
      if source_path.file?
        source_text = source_path.read
        add(errors, "C11", Digest::SHA256.file(source_path).hexdigest == artifact.fetch("source_sha256"), "D2 source digest drifted: #{artifact.fetch('source')}")
        %w[data_lane stats_lane econ_lane].each { |lane| add(errors, "C11", source_text.include?(lane), "D2 lane is missing in #{artifact.fetch('source')}: #{lane}") }
        (1..4).each { |gate| add(errors, "C11", source_text.scan(/^\s*g#{gate}:/).length == 1, "D2 shared gate G#{gate} must occur exactly once in #{artifact.fetch('source')}") }
        causal_token = "≠ causal"
        add(errors, "C11", source_text.include?(causal_token), "D2 causal boundary is absent: #{artifact.fetch('source')}")
        add(errors, "C11", !source_text.match?(%r{(?:file:|/home/|\\home\\|/Users/)}i), "D2 source leaks a local absolute path: #{artifact.fetch('source')}")
      end
      next unless svg_path.file?

      svg = svg_path.read
      add(errors, "C11", Digest::SHA256.file(svg_path).hexdigest == artifact.fetch("svg_sha256"), "D2 SVG digest drifted: #{artifact.fetch('svg')}")
      required_svg = ['data-d2-version="v0.7.1"', 'role="img"', 'aria-labelledby="d2-title d2-desc"', '<title id="d2-title">', '<desc id="d2-desc">', 'viewBox="0 0 ']
      required_svg.each { |needle| add(errors, "C11", svg.include?(needle), "D2 SVG accessibility metadata is missing in #{artifact.fetch('svg')}: #{needle}") }
      title = artifact.fetch("language") == "es" ? "Pipeline de recreación de la tesis" : "Thesis reconstruction pipeline"
      title += artifact.fetch("language") == "es" ? ", versión móvil" : ", mobile version" if artifact.fetch("surface") == "mobile"
      add(errors, "C11", svg.include?(%(<title id="d2-title">#{title}</title>)), "D2 SVG title drifted: #{artifact.fetch('svg')}")
      description = svg[/<desc id="d2-desc">(.*?)<\/desc>/m, 1].to_s
      description_tokens = artifact.fetch("language") == "es" ? %w[custodia causal] : %w[custody causal]
      description_tokens.each { |token| add(errors, "C11", description.downcase.include?(token), "D2 SVG description lacks #{token}: #{artifact.fetch('svg')}") }
      add(errors, "C11", !svg.match?(%r{(?:file:|/home/|\\home\\|/Users/)}i), "D2 SVG leaks a local absolute path: #{artifact.fetch('svg')}")
      view_box = svg.match(/viewBox="0 0 ([0-9.]+) ([0-9.]+)"/)
      add(errors, "C11", !view_box.nil?, "D2 SVG root viewBox is absent: #{artifact.fetch('svg')}")
      if view_box
        width = view_box[1].to_f
        ratio = width / view_box[2].to_f
        expected_shape = artifact.fetch("surface") == "mobile" ? width <= 450 && ratio.between?(0.25, 0.45) : width >= 650 && ratio.between?(1.35, 1.65)
        add(errors, "C11", expected_shape, "D2 SVG surface shape drifted: #{artifact.fetch('svg')}")
      end
    end

    figure_paths = {
      "es" => {
        "desktop" => "pipeline-recreacion-es.svg", "mobile" => "pipeline-recreacion-es-mobile.svg",
        "desktop_source" => "pipeline-recreacion-es.d2", "mobile_source" => "pipeline-recreacion-es-mobile.d2",
        "spoon" => "## Cucharada 2: quién se equivocó", "first_subheading" => "### Donde me equivoqué en 2014",
        "section" => "### De describir el cierre a identificar una política", "section_end" => "La ironía final",
        "route_class" => 'class="causal-routes causal-routes--es"',
        "routes" => ["**Alerta descriptiva/predictiva**", "**Reforma escalonada**", "**Consecuencias del cierre**"]
      },
      "en" => {
        "desktop" => "pipeline-recreacion-en.svg", "mobile" => "pipeline-recreacion-en-mobile.svg",
        "desktop_source" => "pipeline-recreacion-en.d2", "mobile_source" => "pipeline-recreacion-en-mobile.d2",
        "spoon" => "## Spoonful 2: who was wrong", "first_subheading" => "### Where my 2014 self was wrong",
        "section" => "### From describing closure to identifying a policy", "section_end" => "The final irony",
        "route_class" => 'class="causal-routes causal-routes--en"',
        "routes" => ["**Descriptive/predictive warning**", "**Staggered reform**", "**Consequences of closure**"]
      }
    }
    figure_paths.each do |language, spec|
      body = bodies.fetch(language, "")
      add(errors, "C11", body.scan('class="recreation-pipeline-figure"').length == 1, "#{language} must embed the pipeline figure exactly once")
      %w[desktop mobile desktop_source mobile_source].each { |key| add(errors, "C11", body.include?(spec.fetch(key)), "#{language} pipeline markup is missing #{spec.fetch(key)}") }
      figure_at = body.index('class="recreation-pipeline-figure"')
      add(errors, "C11", body.index(spec.fetch("spoon")) && figure_at && body.index(spec.fetch("first_subheading")) && body.index(spec.fetch("spoon")) < figure_at && figure_at < body.index(spec.fetch("first_subheading")), "#{language} pipeline figure is not before the first Spoonful 2 subheading")
      section_start = body.index(spec.fetch("section"))
      section_end = body.index(spec.fetch("section_end"))
      section = section_start && section_end && section_start < section_end ? body[section_start...section_end] : ""
      add(errors, "C11", !section.empty?, "#{language} causal bridge is missing or misplaced")
      add(errors, "C11", section.include?(spec.fetch("route_class")), "#{language} causal routes lack their responsive wrapper")
      spec.fetch("routes").each { |route| add(errors, "C11", section.scan(route).length == 1, "#{language} causal bridge must contain route exactly once: #{route}") }
      add(errors, "C11", section.include?("[^grau2018]"), "#{language} causal bridge does not retain the Grau–Hojman–Mizala citation")
    end
    css = carousel_css_path.file? ? carousel_css_path.read : ""
    required_pipeline_css = [
      ".recreation-pipeline-figure",
      '.causal-routes .tabla-desliza[data-perfil="narrativa"] table',
      "max-height: min(640px, calc(100vh - 6rem))",
      ".causal-routes--es td:nth-child(3)::before",
      ".causal-routes--en td:nth-child(3)::before",
      'html[data-theme="academic-night"] .causal-routes td:nth-child(n + 2)::before'
    ]
    required_pipeline_css.each { |needle| add(errors, "C11", css.include?(needle), "pipeline or route CSS is missing: #{needle}") }
    prohibited_causal_claims = [
      "La reejecución demuestra un efecto causal.",
      "The rerun demonstrates a causal effect.",
      "Los modelos identifican causalmente el efecto.",
      "The models causally identify the effect."
    ]
    bodies.each do |language, body|
      prohibited_causal_claims.each { |claim| add(errors, "C11", !body.include?(claim), "#{language} contains a prohibited causal overclaim: #{claim}") }
    end
  end

  browser_gate_path = root.join("scripts/verify_thesis_recreation_post_i_browser.mjs")
  add(errors, "C13", browser_gate_path.file?, "browser gate is missing")
  if browser_gate_path.file?
    browser_gate = browser_gate_path.read
    browser_tokens = [
      "390, height: 844", "768, height: 1024", "1366, height: 768", "1440, height: 900",
      "academic-night", "carousel-left-overflow", "carousel-title-too-large", "slide-title-too-large",
      "target-too-small", "pipeline-too-tall", "pipeline-misplaced", "carousel-interaction",
      "carousel-popup-link-count", "carousel-full-size-link", "carousel-image-cropped", "carousel-popup-missing",
      "controlMin: 44", "dotMin: 24", "desktopPipelineViewportRatioMax: 1.0", "mobilePipelineViewportRatioMax: 1.5",
      "page.keyboard.press('End')", "page.keyboard.press('Home')", "[data-carousel-next]", "[data-carousel-popup]", "[data-carousel-hd-link]"
    ]
    browser_tokens.each { |needle| add(errors, "C13", browser_gate.include?(needle), "browser gate is missing: #{needle}") }
  end
  if carousel_css_path.file?
    carousel_css = carousel_css_path.read
    carousel_css_tokens = [
      "box-sizing: border-box", "width: 100%", "max-width: 100%", "font-size: 24px",
      "font-size: 20px", "width: 2.75rem", "height: 2.75rem", "width: 1.5rem", "height: 1.5rem",
      ".evidence-carousel__zoom-cue", ".evidence-carousel__full-size-link", "cursor: zoom-in", "width: auto"
    ]
    carousel_css_tokens.each { |needle| add(errors, "C13", carousel_css.include?(needle), "responsive carousel CSS is missing: #{needle}") }
  end
  technical = contract.dig("evidence", "stata17_traceable_rerun")
  technical_keys = %w[repository commit path git_blob sha256 expected]
  add(errors, "C7", technical.is_a?(Hash) && technical_keys.all? { |key| technical.key?(key) }, "Stata receipt specification is incomplete")
  if technical.is_a?(Hash) && technical_keys.all? { |key| technical.key?(key) }
    expected = technical.fetch("expected")
    hard_expected = {
      "status" => "TRACEABLE_PRESENT_DAY_RERUN_COMPLETED",
      "successful_roles" => 15,
      "active_routes" => 14,
      "documented_inactive_routes" => 1,
      "receipt_count" => 15,
      "route_verdict" => "TRACEABLE_PRESENT_DAY_ROUTE_COMPLETED",
      "runtime_status" => "STATA_17_C_MP_EQ_1_CONFIRMED",
      "isolation_status" => "READ_ONLY_ROOTS_INTACT",
      "prohibited_claims" => %w[HISTORICAL_EXECUTION_OBSERVED LITERAL_HISTORICAL_EQUIVALENCE ALL_HISTORICAL_COMMANDS_EXECUTED_UNMODIFIED]
    }
    add(errors, "C7", expected == hard_expected, "Stata receipt expectations were weakened or drifted")
    if thesis_root.nil?
      add(errors, "C7", false, "--thesis-root is required to verify the Stata receipt")
    elsif !thesis_root.directory?
      add(errors, "C7", false, "thesis root is absent: #{thesis_root}")
    else
      revision = "#{technical.fetch('commit')}:#{technical.fetch('path')}"
      technical_blob, blob_status = Open3.capture2e("git", "-C", thesis_root.to_s, "rev-parse", revision)
      add(errors, "C7", blob_status.success? && technical_blob.strip == technical.fetch("git_blob"), "Stata receipt Git blob drifted")
      technical_payload, payload_status = Open3.capture2e("git", "-C", thesis_root.to_s, "show", revision)
      add(errors, "C7", payload_status.success?, "Stata receipt Git object is unavailable")
      if payload_status.success?
        add(errors, "C7", Digest::SHA256.hexdigest(technical_payload) == technical.fetch("sha256"), "Stata receipt SHA-256 drifted")
        begin
          receipt = JSON.parse(technical_payload)
          suite = receipt.fetch("suite")
          routes = receipt.fetch("receipts")
          expected_order = %w[do_056 do_057 do_058 do_070 do_071 do_068 do_060 do_063 do_065 do_036 do_066 do_067 do_059 do_069 do_064]
          add(errors, "C7", suite["status"] == expected["status"], "Stata suite status drifted")
          add(errors, "C7", suite["successful_roles"] == expected["successful_roles"], "Stata successful-role count drifted")
          add(errors, "C7", suite["active_routes"] == expected["active_routes"], "Stata active-route count drifted")
          add(errors, "C7", suite["documented_inactive_routes"] == expected["documented_inactive_routes"], "Stata documentary-route count drifted")
          add(errors, "C7", suite["prohibited_claims"] == expected["prohibited_claims"], "Stata prohibited claims drifted")
          add(errors, "C7", routes.length == expected["receipt_count"], "Stata receipt count drifted")
          add(errors, "C7", routes.map { |row| row["do_id"] } == expected_order, "Stata role order drifted")
          add(errors, "C7", routes.all? { |row| row.dig("execution", "verdict") == expected["route_verdict"] }, "a Stata route is not green")
          add(errors, "C7", routes.all? { |row| row.dig("execution", "error_count") == 0 }, "a Stata route contains errors")
          add(errors, "C7", routes.all? { |row| row.dig("execution", "runtime_identity", "status") == expected["runtime_status"] }, "a Stata runtime identity drifted")
          add(errors, "C7", routes.all? { |row| row.dig("isolation", "status") == expected["isolation_status"] }, "a Stata route lost isolation")
          add(errors, "C7", receipt.dig("isolation", "status") == expected["isolation_status"], "Stata suite isolation drifted")
        rescue JSON::ParserError, KeyError
          add(errors, "C7", false, "Stata receipt Git object is not a valid complete JSON receipt")
        end
      end
    end
  end

  harvest = contract.dig("evidence", "stata17_output_harvest")
  harvest_keys = %w[repository commit path git_blob sha256 expected]
  add(errors, "C10", harvest.is_a?(Hash) && harvest_keys.all? { |key| harvest.key?(key) }, "Stata output harvest specification is incomplete")
  if harvest.is_a?(Hash) && harvest_keys.all? { |key| harvest.key?(key) }
    expected = harvest.fetch("expected")
    hard_expected = {
      "status" => "COMPLETE_WITH_DECLARED_LIMITS",
      "routes" => 3,
      "outputs" => 4,
      "literal_source_status" => "NO_EJECUTABLE",
      "governed_rerun_status" => "TRACEABLE_PRESENT_DAY_ROUTE_COMPLETED",
      "panel_rows" => 234_284,
      "schools" => 16_048,
      "years" => [1992, 2012],
      "communes" => 346,
      "coordinate_rows" => 2_934_033,
      "multilevel_models" => 4,
      "observations_per_model" => [816, 816, 816, 816],
      "persisted_graph_files" => 0
    }
    add(errors, "C10", expected == hard_expected, "Stata output harvest expectations drifted")
    if thesis_root.nil?
      add(errors, "C10", false, "--thesis-root is required to verify the Stata output harvest")
    elsif !thesis_root.directory?
      add(errors, "C10", false, "thesis root is absent: #{thesis_root}")
    else
      revision = "#{harvest.fetch('commit')}:#{harvest.fetch('path')}"
      harvest_blob, blob_status = Open3.capture2e("git", "-C", thesis_root.to_s, "rev-parse", revision)
      add(errors, "C10", blob_status.success? && harvest_blob.strip == harvest.fetch("git_blob"), "Stata output harvest Git blob drifted")
      harvest_payload, payload_status = Open3.capture2e("git", "-C", thesis_root.to_s, "show", revision)
      add(errors, "C10", payload_status.success?, "Stata output harvest Git object is unavailable")
      if payload_status.success?
        add(errors, "C10", Digest::SHA256.hexdigest(harvest_payload) == harvest.fetch("sha256"), "Stata output harvest SHA-256 drifted")
        begin
          result = JSON.parse(harvest_payload)
          routes = result.fetch("routes")
          route58 = routes.fetch("do_058")
          route59 = routes.fetch("do_059")
          route60 = routes.fetch("do_060")
          add(errors, "C10", result.fetch("status") == expected.fetch("status"), "Stata output harvest status drifted")
          add(errors, "C10", routes.keys.sort == %w[do_058 do_059 do_060], "Stata output harvest route set drifted")
          add(errors, "C10", routes.values.all? { |row| row["literal_source_status"] == expected["literal_source_status"] }, "a literal source status drifted")
          add(errors, "C10", routes.values.all? { |row| row["governed_rerun_status"] == expected["governed_rerun_status"] }, "a governed rerun status drifted")
          add(errors, "C10", routes.values.sum { |row| row.fetch("output_count") } == expected["outputs"], "Stata output count drifted")
          add(errors, "C10", routes.values.flat_map { |row| row.fetch("outputs") }.all? { |output| output["sha256"].to_s.match?(/\A[0-9a-f]{64}\z/) }, "a harvested output lacks a SHA-256")
          add(errors, "C10", route58.dig("qa", "rows") == expected["panel_rows"], "do_058 row count drifted")
          add(errors, "C10", route58.dig("qa", "unique_schools") == expected["schools"], "do_058 school count drifted")
          add(errors, "C10", route58.dig("qa", "years") == expected["years"], "do_058 year range drifted")
          add(errors, "C10", route58.dig("qa", "duplicate_school_year_rows") == 0, "do_058 duplicate keys appeared")
          add(errors, "C10", route58.dig("qa", "missing_commune_code_rows") == 0, "do_058 missing commune codes appeared")
          add(errors, "C10", route60.dig("qa", "communes") == expected["communes"], "do_060 commune count drifted")
          add(errors, "C10", route60.dig("qa", "coordinate_rows") == expected["coordinate_rows"], "do_060 coordinate count drifted")
          add(errors, "C10", route60.dig("qa", "communes_without_coordinates") == 0, "do_060 lost commune geometry")
          add(errors, "C10", route60.dig("graph_evidence", "persisted_graph_files") == expected["persisted_graph_files"], "do_060 graph persistence drifted")
          add(errors, "C10", route59["model_blocks"] == expected["multilevel_models"], "do_059 model count drifted")
          add(errors, "C10", route59["observations_per_model"] == expected["observations_per_model"], "do_059 observation counts drifted")
          add(errors, "C10", route59["substantive_thesis_evidence"] == false, "do_059 was promoted to thesis evidence")
          add(errors, "C10", result.dig("claims_boundary", "historical_execution") == "NOT_VERIFIED", "harvest promotes historical execution")
          add(errors, "C10", result.dig("claims_boundary", "prohibited_claims") == %w[HISTORICAL_EXECUTION_OBSERVED LITERAL_HISTORICAL_EQUIVALENCE DO_059_AS_SUBSTANTIVE_THESIS_EVIDENCE DO_060_PERSISTED_MAPS], "harvest prohibited claims drifted")
        rescue JSON::ParserError, KeyError
          add(errors, "C10", false, "Stata output harvest Git object is not valid complete JSON")
        end
      end
    end
  end
  add(errors, "C1", root.join("_config.yml").read.include?("- research/replica-tesis"), "research metadata is not excluded from Jekyll")

  if staged
    actual = staged_paths(root)
    allowed_paths = expected_paths + expected_deletions
    add(errors, "C6", !actual.empty? && actual.all? { |path| allowed_paths.include?(path) }, "staged paths are empty or outside allowlist: #{actual.join(', ')}")
    publication_paths = contract.dig("scope", "documents").values
    add(errors, "C6", publication_paths.all? { |path| actual.include?(path) }, "bilingual publication pair is not fully staged")
    draft_paths = expected_deletions.select { |path| path.start_with?("_drafts/") }
    add(errors, "C6", draft_paths.none? { |path| root.join(path).exist? }, "a promoted source still exists under _drafts")
  end
  errors
end

def self_test(root, thesis_root:)
  raise "self-test requires --thesis-root" if thesis_root.nil?

  Dir.mktmpdir("thesis-post-contract-") do |directory|
    fixture = Pathname(directory)
    contract = yaml(root.join("docs/contracts/thesis-recreation-post-i-ready-review.yaml"))
    fixture_paths = (contract.dig("commit", "paths") + ["_config.yml", "research/replica-tesis/literature.yml"]).uniq
    fixture_paths.each do |relative|
      target = fixture.join(relative)
      FileUtils.mkdir_p(target.dirname)
      FileUtils.cp(root.join(relative), target)
    end
    validate_options = { staged: false, external_papers: nil, thesis_root: thesis_root }
    raise "baseline failed: #{validate(fixture, **validate_options)}" unless validate(fixture, **validate_options).empty?
    deleted_fixture = fixture.join(contract.dig("commit", "deletions").first)
    FileUtils.mkdir_p(deleted_fixture.dirname)
    deleted_fixture.write("stale asset\n")
    raise "C0 required deletion did not fail" if validate(fixture, **validate_options).fetch("C0", []).empty?
    FileUtils.rm(deleted_fixture)
    accounting = fixture.join("research/replica-tesis/hypothesis-accounting.md")
    FileUtils.rm(accounting)
    raise "C0 did not fail" if validate(fixture, **validate_options).fetch("C0", []).empty?
    FileUtils.cp(root.join("research/replica-tesis/hypothesis-accounting.md"), accounting)
    es = fixture.join(contract.dig("scope", "documents", "es")); es_original = es.read
    es.write(es_original.sub("El mercado mutó muy rápido", "El mercado dejó de cambiar"))
    raise "C2 did not fail" if validate(fixture, **validate_options).fetch("C2", []).empty?
    es.write(es_original)
    literature = fixture.join("research/replica-tesis/literature.yml"); literature_original = literature.read
    literature.write(literature_original.sub("10.1111/joes.12139", "10.1111/invalid"))
    raise "C1 did not fail" if validate(fixture, **validate_options).fetch("C1", []).empty?
    literature.write(literature_original)
    stray_pdf = fixture.join("research/replica-tesis/unwanted.pdf")
    stray_pdf.binwrite("%PDF- stray\n")
    raise "C1 repository PDF did not fail" if validate(fixture, **validate_options).fetch("C1", []).empty?
    FileUtils.rm(stray_pdf)
    en = fixture.join(contract.dig("scope", "documents", "en")); en_original = en.read
    en.write(en_original.sub("traceable present-day rerun", "literal historical equivalence"))
    raise "C3 present-day-rerun boundary did not fail" if validate(fixture, **validate_options).fetch("C3", []).empty?
    en.write(en_original)
    es.write(es_original.sub("Con datos de 2002 a 2012", "Datos de otro periodo"))
    raise "C3 policy bridge did not fail" if validate(fixture, **validate_options).fetch("C3", []).empty?
    es.write(es_original)
    es.write(es_original + "\nNo he logrado verificar una atribución.\n")
    raise "C3 unverified attribution did not fail" if validate(fixture, **validate_options).fetch("C3", []).empty?
    es.write(es_original)
    contract_path = fixture.join("docs/contracts/thesis-recreation-post-i-ready-review.yaml"); contract_original = contract_path.read
    contract_path.write(contract_original.sub("REFUTADA: 37", "REFUTADA: 36"))
    raise "C4 source outcome did not fail" if validate(fixture, **validate_options).fetch("C4", []).empty?
    contract_path.write(contract_original)
    en.write(en_original.sub("1 partial", "0 partial"))
    raise "C4 draft outcome did not fail" if validate(fixture, **validate_options).fetch("C4", []).empty?
    en.write(en_original)
    es.write(es_original.gsub("salida canónica de 2026 sin errores conocidos", "salida canónica de 2026 sin revisar"))
    raise "C4 corrected-current-route closing did not fail" if validate(fixture, **validate_options).fetch("C4", []).empty?
    es.write(es_original)
    es.write(es_original.sub("| Movilidad bruta y tasas |", "| Tasa omitida |"))
    raise "C4 mobility mapping did not fail" if validate(fixture, **validate_options).fetch("C4", []).empty?
    es.write(es_original)
    en.write(en_original.sub("| PSU gap | ≈ 10 | Final result: 10.40, not 11.25 | Correct final match |", "| PSU gap | ≈ 10 | Final result: 11.25 | Unresolved |"))
    raise "C4 PSU final-match mapping did not fail" if validate(fixture, **validate_options).fetch("C4", []).empty?
    en.write(en_original)
    technical_sha = contract.dig("evidence", "stata17_traceable_rerun", "sha256")
    contract_path.write(contract_original.sub(technical_sha, "0" * 64))
    raise "C7 technical receipt did not fail" if validate(fixture, **validate_options).fetch("C7", []).empty?
    contract_path.write(contract_original)
    comparison_sha = contract.dig("evidence", "result_comparison", "sha256")
    contract_path.write(contract_original.sub(comparison_sha, "0" * 64))
    raise "C8 comparison receipt did not fail" if validate(fixture, **validate_options).fetch("C8", []).empty?
    contract_path.write(contract_original)
    es.write(es_original.sub("Todo el itinerario computacional disponible volvió a ejecutarse", "La ruta no volvió a ejecutarse"))
    raise "C8 central claim did not fail" if validate(fixture, **validate_options).fetch("C8", []).empty?
    es.write(es_original)
    es.write(es_original.sub("| Coincidencia | 3 |", "| Coincidencia | 1 |"))
    raise "C8 corrected comparison counts did not fail" if validate(fixture, **validate_options).fetch("C8", []).empty?
    es.write(es_original)
    carousel_data = fixture.join("_data/thesis_recreation_face_to_face.yml"); carousel_data_original = carousel_data.read
    carousel_data.write(carousel_data_original.sub("      - id: figure-04-net-mobility", "      - id: figure-04-removed"))
    raise "C9 missing slide did not fail" if validate(fixture, **validate_options).fetch("C9", []).empty?
    carousel_data.write(carousel_data_original)
    carousel_digest = "ab67c3adccf3bd4a3c9594fcdd26a2382daed7031a12bdb74738921a9af1c8fb"
    carousel_data.write(carousel_data_original.sub(carousel_digest, "0" * 64))
    raise "C9 asset digest did not fail" if validate(fixture, **validate_options).fetch("C9", []).empty?
    carousel_data.write(carousel_data_original)
    carousel_include = fixture.join("_includes/evidence-carousel.html"); carousel_include_original = carousel_include.read
    carousel_include.write(carousel_include_original.sub('aria-roledescription="carousel"', ""))
    raise "C9 ARIA did not fail" if validate(fixture, **validate_options).fetch("C9", []).empty?
    carousel_include.write(carousel_include_original)
    carousel_include.write(carousel_include_original.gsub("data-carousel-hd-link", "data-carousel-link-removed"))
    raise "C9 full-size link did not fail" if validate(fixture, **validate_options).fetch("C9", []).empty?
    carousel_include.write(carousel_include_original)
    carousel_script = fixture.join("assets/js/evidence-carousel.js"); carousel_script_original = carousel_script.read
    carousel_script.write(carousel_script_original + "\nsetInterval(function () {}, 1000);\n")
    raise "C9 automation did not fail" if validate(fixture, **validate_options).fetch("C9", []).empty?
    carousel_script.write(carousel_script_original)
    carousel_include_call = "{% include evidence-carousel.html %}"
    es.write(es_original.sub(carousel_include_call, "").sub("**Tabla 3**", "**Tabla 3**\n\n#{carousel_include_call}"))
    raise "C9 placement did not fail" if validate(fixture, **validate_options).fetch("C9", []).empty?
    es.write(es_original)
    harvest_sha = contract.dig("evidence", "stata17_output_harvest", "sha256")
    contract_path.write(contract_original.sub(harvest_sha, "0" * 64))
    raise "C10 output harvest did not fail" if validate(fixture, **validate_options).fetch("C10", []).empty?
    contract_path.write(contract_original)
    es.write(es_original.gsub("`do_059`", "`do_999`"))
    raise "C10 smoke-test promotion did not fail" if validate(fixture, **validate_options).fetch("C10", []).empty?
    es.write(es_original)
    pipeline_mobile = fixture.join("assets/images/replica-tesis-establecimientos/pipeline-recreacion-es-mobile.svg")
    FileUtils.rm(pipeline_mobile)
    raise "C11 missing mobile SVG did not fail" if validate(fixture, **validate_options).fetch("C11", []).empty?
    FileUtils.cp(root.join("assets/images/replica-tesis-establecimientos/pipeline-recreacion-es-mobile.svg"), pipeline_mobile)
    pipeline_svg = fixture.join("assets/images/replica-tesis-establecimientos/pipeline-recreacion-es.svg"); pipeline_svg_original = pipeline_svg.read
    pipeline_svg.write(pipeline_svg_original.sub(' role="img"', ""))
    raise "C11 SVG accessibility did not fail" if validate(fixture, **validate_options).fetch("C11", []).empty?
    pipeline_svg.write(pipeline_svg_original)
    es.write(es_original.sub("reejecutable no significa recreable; recreable no significa coincidente; coincidente no significa correcto; correcto no significa causal", "La reejecución demuestra un efecto causal."))
    raise "C11 causal overclaim did not fail" if validate(fixture, **validate_options).fetch("C11", []).empty?
    es.write(es_original)
    es.write(es_original.sub("12 coeficientes en el archivo, 11 efectos en el cuadro y 10 coincidencias", "once efectos sin denominador"))
    raise "C12 denominator boundary did not fail" if validate(fixture, **validate_options).fetch("C12", []).empty?
    es.write(es_original)
    browser_gate = fixture.join("scripts/verify_thesis_recreation_post_i_browser.mjs"); browser_gate_original = browser_gate.read
    browser_gate.write(browser_gate_original.sub("carousel-left-overflow", "overflow-check-removed"))
    raise "C13 browser geometry gate did not fail" if validate(fixture, **validate_options).fetch("C13", []).empty?
    browser_gate.write(browser_gate_original)
    browser_gate.write(browser_gate_original.sub("carousel-popup-missing", "popup-check-removed"))
    raise "C13 popup gate did not fail" if validate(fixture, **validate_options).fetch("C13", []).empty?
    browser_gate.write(browser_gate_original)
    en.write(en_original.sub("[^stata17]: Technical receipt pinned", "[^stata17]: Receipt removed"))
    raise "C14 runtime provenance did not fail" if validate(fixture, **validate_options).fetch("C14", []).empty?
    en.write(en_original)
    en.write(en_original.sub("## Closing", "## Removed closing"))
    raise "C5 did not fail" if validate(fixture, **validate_options).fetch("C5", []).empty?
    en.write(en_original)
    output, status = Open3.capture2e("git", "-C", fixture.to_s, "init", "-q"); raise output unless status.success?
    staged_options = validate_options.merge(staged: true)
    raise "C6 empty index did not fail" if validate(fixture, **staged_options).fetch("C6", []).empty?
    output, status = Open3.capture2e("git", "-C", fixture.to_s, "add", *contract.dig("commit", "paths")); raise output unless status.success?
    raise "C6 baseline failed" unless validate(fixture, **staged_options).empty?
    fixture.join("unrelated.txt").write("must not enter commit\n")
    output, status = Open3.capture2e("git", "-C", fixture.to_s, "add", "unrelated.txt"); raise output unless status.success?
    raise "C6 did not fail" if validate(fixture, **staged_options).fetch("C6", []).empty?
  end
  { "self_test" => "pass", "observed_red_controls" => %w[C0 C1 C2 C3 C4 C5 C6 C7 C8 C9 C10 C11 C12 C13 C14] }
end

def with_staged_snapshot(root)
  Dir.mktmpdir("thesis-post-i-staged-") do |directory|
    snapshot = Pathname(directory)
    output, status = Open3.capture2e(
      "git", "-C", root.to_s, "checkout-index", "--all", "--prefix=#{snapshot}/"
    )
    raise "Cannot materialize staged snapshot: #{output.strip}" unless status.success?
    yield snapshot
  end
end

def validate_staged_snapshot(root, external_papers:, thesis_root:)
  actual = staged_paths(root)
  with_staged_snapshot(root) do |snapshot|
    errors = validate(snapshot, staged: false, external_papers: external_papers, thesis_root: thesis_root)
    contract_path = snapshot.join("docs/contracts/thesis-recreation-post-i-ready-review.yaml")
    if contract_path.file?
      staged_contract = yaml(contract_path)
      expected = (staged_contract.dig("commit", "paths") + Array(staged_contract.dig("commit", "deletions"))).sort
      add(errors, "C6", !actual.empty? && actual.all? { |path| expected.include?(path) }, "staged paths are empty or outside allowlist: #{actual.join(', ')}")
    else
      add(errors, "C6", false, "staged snapshot is missing the ready-review contract")
    end
    errors
  end
end

settings = options
root = settings.fetch(:root).expand_path
if settings.fetch(:self_test)
  result = if settings.fetch(:staged)
    with_staged_snapshot(root) { |snapshot| self_test(snapshot, thesis_root: settings.fetch(:thesis_root)) }
  else
    self_test(root, thesis_root: settings.fetch(:thesis_root))
  end
  puts JSON.pretty_generate(result)
  exit 0
end
errors = if settings.fetch(:staged)
  validate_staged_snapshot(root, external_papers: settings.fetch(:external_papers), thesis_root: settings.fetch(:thesis_root))
else
  validate(root, staged: false, external_papers: settings.fetch(:external_papers), thesis_root: settings.fetch(:thesis_root))
end
puts JSON.pretty_generate({ "contract" => "docs/contracts/thesis-recreation-post-i-ready-review.yaml", "status" => errors.empty? ? "pass" : "fail", "controls" => errors })
exit(errors.empty? ? 0 : 1)
