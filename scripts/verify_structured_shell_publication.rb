#!/usr/bin/env ruby
# frozen_string_literal: true

# Gate específico del post Nushell. Los verificadores genéricos no inspeccionan
# drafts y posts; bloquea que un corpus congelado, su versión EN o sus activos
# sociales diverjan durante la preparación y después de mover el par a _posts/.
# falsified_by: fecha ES/EN distinta, una de las seis tablas sin acceso por teclado,
# un SVG localizado sin title/desc o un activo que exponga una ruta local.

require "date"
require "json"
require "open3"
require "yaml"
require_relative "lib/image_dimensions"

ROOT = File.expand_path("..", __dir__)
SLUG = "2026-08-29-nushell-coprocesador-estructurado"

def assert!(condition, message)
  raise message unless condition
end

def publication_entry(slug)
  candidates = %w[_posts _drafts].map { |directory| File.join(ROOT, directory, "#{slug}.md") }
  found = candidates.select { |path| File.file?(path) }
  assert!(found.length == 1, "#{slug}: debe existir exactamente una vez, en _posts o _drafts")
  found.first
end

ES = publication_entry(SLUG)
EN = publication_entry("#{SLUG}-en")
DATA = File.join(ROOT, "assets", "data", "structured-shell", "datos.json")
CASE_DATA = File.join(ROOT, "assets", "data", "structured-shell", "tesis-case.json")
VIEWER = File.join(ROOT, "assets", "visores", "structured-shell", "index.html")
GENERATOR = File.join(ROOT, "scripts", "render_structured_shell_og.py")
D2_GENERATOR = File.join(ROOT, "scripts", "render_structured_shell_d2_locales.py")
OG_MASTER = File.join(ROOT, "assets", "images", "structured-shell", "routing-og-master.webp")
TEASER_MASTER = File.join(ROOT, "assets", "images", "structured-shell", "routing-teaser-master.webp")
CASE_GENERATOR = File.join(ROOT, "scripts", "export_structured_shell_thesis_case_public.py")
CASE_SUMMARY = File.join(ROOT, "research", "structured-shell-thesis-case", "results", "summary.json")
CASE_FIXTURE = File.join(ROOT, "research", "structured-shell-thesis-case", "fixtures", "tesis_temporal_activity.json")

def front_matter(path)
  body = File.read(path, encoding: "UTF-8")
  match = body.match(/\A---\s*\n(.*?)\n---\s*\n/m)
  assert!(!match.nil?, "#{path}: front matter ausente")
  [YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: false), body]
end

def prop(data, indicator, arm)
  index = data.fetch("prop").fetch("ind").each_index.find do |i|
    data["prop"]["ind"][i] == indicator && data["prop"]["brazo"][i] == arm
  end
  raise "datos.json: falta #{indicator}/#{arm}" if index.nil?

  [data["prop"]["ex"][index], data["prop"]["n"][index]]
end

def median(data, section, metric, group)
  result = data.fetch(section).fetch(metric)
  index = result.fetch("g").index(group)
  raise "datos.json: falta #{section}/#{metric}/#{group}" if index.nil?

  result.fetch("est")[index]
end

def require_holdout_claims!(body, label)
  %w[14/15 10/15 4/15 5/10 6/10].each do |claim|
    assert!(body.include?(claim), "#{label}: falta claim holdout #{claim}")
  end
end

def require_case_contract!(data, label)
  assert!(data["schema_version"] == 1, "#{label}: schema de caso inválido")
  assert!(data.dig("design", "records") == 30, "#{label}: no hay 30 observaciones")
  assert!(data.dig("design", "tasks") == 3 && data.dig("design", "repetitions_per_task_arm") == 5, "#{label}: diseño A/B inválido")
  assert!(data.dig("source_shape", "annual_aggregate_rows") == 21, "#{label}: filas anuales inválidas")
  assert!(data.dig("source_shape", "rows") == 306_768 && data.dig("source_shape", "columns") == 263, "#{label}: forma de fuente inválida")
  assert!(data["source_dataset_sha256"] == "854f47c641261cc0d92c21f18a11e12b26f9faaeec1b0d81bc4344e947157304", "#{label}: hash de fuente inválido")
  assert!(data["tasks"].length == 3, "#{label}: tareas de caso incompletas")
  expected = {
    "R1_valid_aggregate" => { "without_nushell" => [0, 30_641, 445], "policy_nushell" => [5, 42_038, 580] },
    "R2_corrupt_aggregate" => { "without_nushell" => [0, 31_432, 358], "policy_nushell" => [5, 31_956, 410] },
    "R3_epistemic_boundary" => { "without_nushell" => [0, 14_976, 88], "policy_nushell" => [0, 11_355, 62] }
  }
  expected.each do |task_id, arms|
    task = data["tasks"].find { |item| item["id"] == task_id }
    assert!(!task.nil?, "#{label}: falta #{task_id}")
    arms.each do |arm_id, values|
      arm = task["arms"].find { |item| item["arm"] == arm_id }
      assert!(!arm.nil?, "#{label}: falta #{task_id}/#{arm_id}")
      assert!(arm["runs"] == 5 && arm["correct"] == 5, "#{label}: acierto inválido #{task_id}/#{arm_id}")
      assert!([arm["used_nushell"], arm["median_elapsed_ms"], arm["median_output_tokens"]] == values, "#{label}: métricas inválidas #{task_id}/#{arm_id}")
    end
  end
end

def public_json_safe!(data, label)
  assert!(!JSON.generate(data).include?("/home/"), "#{label}: contiene una ruta local")
  stack = [data]
  until stack.empty?
    item = stack.pop
    case item
    when Hash
      assert!(item.keys.none? { |key| key.to_s.match?(%r{(?:^|_)(?:rbd|cod_ine)(?:_|$)|relative_path}i) }, "#{label}: contiene una clave identificadora")
      stack.concat(item.values)
    when Array
      stack.concat(item)
    end
  end
end

def accessible_svg!(content, label)
  assert!(content.include?("<title") && content.include?("<desc"), "#{label}: SVG sin nombre o descripción")
  assert!(!content.include?("/home/") && !content.include?("file:"), "#{label}: SVG contiene ruta local")
end

def self_test!
  sample = "14/15 con skill; 10/15 sin skill; 4/15 activaciones; 5/10; 6/10"
  require_holdout_claims!(sample, "fixture sano")
  begin
    require_holdout_claims!(sample.gsub("4/15", "4/14"), "fixture negativo")
    raise "fixture negativo aprobó"
  rescue RuntimeError => e
    raise e if e.message == "fixture negativo aprobó"
  end
  case_sample = { "schema_version" => 1, "design" => { "records" => 30, "tasks" => 3, "repetitions_per_task_arm" => 5 }, "source_shape" => { "annual_aggregate_rows" => 21, "rows" => 306_768, "columns" => 263 }, "source_dataset_sha256" => "854f47c641261cc0d92c21f18a11e12b26f9faaeec1b0d81bc4344e947157304", "tasks" => [] }
  begin
    require_case_contract!(case_sample, "fixture negativo")
    raise "fixture de caso negativo aprobó"
  rescue RuntimeError => e
    raise e if e.message == "fixture de caso negativo aprobó"
  end
  begin
    accessible_svg!("<svg><title>Only a title</title></svg>", "fixture SVG negativo")
    raise "fixture SVG negativo aprobó"
  rescue RuntimeError => e
    raise e if e.message == "fixture SVG negativo aprobó"
  end
  puts "SELF-TEST: observó fixture negativo"
end

if ARGV.delete("--self-test")
  self_test!
  exit 0
end

failures = []
begin
  [ES, EN, DATA, CASE_DATA, VIEWER, GENERATOR, D2_GENERATOR, OG_MASTER, TEASER_MASTER, CASE_GENERATOR, CASE_SUMMARY, CASE_FIXTURE].each { |path| assert!(File.file?(path), "falta #{path.delete_prefix("#{ROOT}/")}") }
  es_fm, es_body = front_matter(ES)
  en_fm, en_body = front_matter(EN)
  assert!(es_fm["lang"] == "es" && en_fm["lang"] == "en", "lang ES/EN inválido")
  %w[ref permalink date].each { |key| assert!(es_fm[key] == en_fm[key], "par ES/EN diverge en #{key}") }
  assert!(es_fm.dig("header", "og_image") == "/assets/images/structured-shell/og-1200.webp", "OG ES inesperado")
  assert!(en_fm.dig("header", "og_image") == "/assets/images/structured-shell/og-1200-en.webp", "OG EN inesperado")
  assert!(en_fm.dig("header", "teaser") == "/assets/images/teasers/teaser-structured-shell-en.webp", "teaser EN inesperado")

  data = JSON.parse(File.read(DATA, encoding: "UTF-8"))
  case_data = JSON.parse(File.read(CASE_DATA, encoding: "UTF-8"))
  case_summary = JSON.parse(File.read(CASE_SUMMARY, encoding: "UTF-8"))
  assert!(data.dig("meta", "n_micro") == 200 && data.dig("meta", "n_ab") == 100, "corpus congelado no es 200 + 100")
  assert!(prop(data, "acierto", "sin la skill") == [23, 30], "acierto sin skill no coincide")
  assert!(prop(data, "acierto", "con la skill") == [30, 30], "acierto con skill no coincide")
  assert!(prop(data, "activo", "con la skill") == [28, 30], "activación afinada no coincide")
  assert!(median(data, "micro", "res_ms", "T1 · archivos >1 MB, 30 días|tradicional") == 389, "microbenchmark T1 tradicional no coincide")
  assert!(median(data, "micro", "res_ms", "T1 · archivos >1 MB, 30 días|Nushell") == 1315, "microbenchmark T1 Nushell no coincide")
  require_case_contract!(case_data, "activo público")
  assert!(case_summary["records"] == 30 && case_summary["errors"] == 0, "resumen A/B no está cerrado")
  assert!(case_summary.fetch("by_task_arm").all? { |row| row["condition_conformant"] == 5 && row["correct"] == 5 }, "A/B contiene una observación no conforme")
  public_json_safe!(case_data, "activo público")
  public_json_safe!(JSON.parse(File.read(CASE_FIXTURE, encoding: "UTF-8")), "fixture público")
  public_json_safe!(case_summary, "resumen A/B")

  require_holdout_claims!(es_body, "ES")
  require_holdout_claims!(en_body, "EN")
  %w[306.768 30\ observaciones 10/10 presencia=0].each { |claim| assert!(es_body.include?(claim), "ES: falta claim de caso #{claim}") }
  ["306,768", "30 observations", "10/10", "presence=0"].each { |claim| assert!(en_body.include?(claim), "EN: missing case claim #{claim}") }
  assert!(es_body.match?(%r{<iframe[^>]+loading="eager"}m), "ES: iframe debe cargar sin depender del umbral lazy")
  assert!(en_body.match?(%r{<iframe[^>]+loading="eager"}m), "EN: iframe must not depend on lazy-load threshold")
  assert!(es_body.scan('{: tabindex="0" aria-label=').length == 6, "ES: las seis tablas deben tener acceso por teclado")
  assert!(en_body.scan('{: tabindex="0" aria-label=').length == 6, "EN: all six tables must support keyboard access")
  assert!(!es_body.include?("317 ms") && !en_body.include?("317 ms"), "tabla micro usa la cifra obsoleta 317 ms")
  assert!(!es_body.include?("unas sesenta líneas"), "wrapper con longitud obsoleta")

  viewer = File.read(VIEWER, encoding: "UTF-8")
  viewer_script = viewer[/<script>(.*?)<\/script>/m, 1]
  assert!(!viewer_script.nil?, "visor sin script embebido")
  _stdout, stderr, node_status = Open3.capture3("node", "--check", "-", stdin_data: viewer_script)
  assert!(node_status.success?, "visor: JavaScript inválido: #{stderr.lines.first.to_s.strip}")
  assert!(viewer.include?("new URLSearchParams(location.search).get(\"lang\")") && viewer.include?("===\"en\""), "visor sin localización por query")
  assert!(viewer.include?("function fallback") && viewer.include?("fig-microbenchmark.svg"), "visor sin fallback estático")
  assert!(!viewer.include?("/opt/entornos/") && !viewer.include?("/home/"), "visor contiene ruta local")
  %w[14/15 10/15 4/15].each { |claim| assert!(viewer.include?(claim), "visor: falta resumen holdout #{claim}") }
  %w[tesis-case.json Thesis\ case Caso\ de\ tesis].each { |claim| assert!(viewer.include?(claim), "visor: falta caso real #{claim}") }
  generator = File.read(GENERATOR, encoding: "UTF-8")
  assert!(generator.include?("OG_MASTER") && generator.include?("TEASER_MASTER") && generator.include?("DERIVATIVES"), "generador social no declara sus masters y derivados")
  assert!(!generator.include?("25/25 acierto") && !generator.include?("120 corridas después"), "generador conserva copy obsoleto")
  d2_generator = File.read(D2_GENERATOR, encoding: "UTF-8")
  assert!(d2_generator.include?("fig-d2-shell-families-en.svg") && d2_generator.include?("fig-d2-shell-families-mobile-en.svg"), "generador D2 no declara ambas variantes EN")
  case_generator = File.read(CASE_GENERATOR, encoding: "UTF-8")
  assert!(case_generator.include?("ensure_safe") && case_generator.include?("OUT_SVG_EN"), "generador de caso no protege ni localiza activos")
  assert!(!case_generator.include?("fixtures/tesis_temporal_activity_corrupt"), "generador público incluye fixture corrupto")

  {
    "assets/images/structured-shell/og-1200.webp" => [1200, 630],
    "assets/images/structured-shell/og-1200-en.webp" => [1200, 630],
    "assets/images/teasers/teaser-structured-shell.webp" => [1280, 720],
    "assets/images/teasers/teaser-structured-shell-en.webp" => [1280, 720]
  }.each do |relative, expected|
    dimensions = image_dimensions(File.join(ROOT, relative))
    assert!(dimensions == expected, "#{relative}: dimensiones #{dimensions.inspect}, esperaba #{expected.inspect}")
  end
  [
    "assets/images/structured-shell/fig-d2-familias-shell.svg",
    "assets/images/structured-shell/fig-d2-familias-shell-mobile.svg",
    "assets/images/structured-shell/fig-d2-shell-families-en.svg",
    "assets/images/structured-shell/fig-d2-shell-families-mobile-en.svg",
    "assets/images/structured-shell/fig-tesis-caso-real.svg",
    "assets/images/structured-shell/fig-tesis-caso-real-en.svg"
  ].each do |relative|
    content = File.read(File.join(ROOT, relative), encoding: "UTF-8")
    accessible_svg!(content, relative)
  end
rescue StandardError => e
  failures << e.message
end

if failures.empty?
  puts "PASS structured-shell publication contract"
else
  failures.each { |failure| warn "FAIL #{failure}" }
  exit 1
end
