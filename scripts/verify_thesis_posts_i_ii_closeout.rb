#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "cgi"
require "json"
require "kramdown"
require "optparse"
require "open3"
require "yaml"

class CloseoutError < StandardError; end

ROOT = File.expand_path("..", __dir__)
DECISIONS = File.join(ROOT, "docs/contracts/thesis-posts-i-ii-editorial-decisions.yml")
POSTS = {
  i_es: File.join(ROOT, "_posts/2026-08-29-replica-tesis-establecimientos-educacionales.md"),
  i_en: File.join(ROOT, "_posts/2026-08-29-replica-tesis-establecimientos-educacionales-en.md"),
  ii_es: File.join(ROOT, "_posts/2026-10-11-extender-tesis-no-es-agregar-anos.md"),
  ii_en: File.join(ROOT, "_posts/2026-10-11-extender-tesis-no-es-agregar-anos-en.md")
}.freeze
ANNEXES = {
  es: File.join(ROOT, "_pages/auditoria-coordenadas-rbd.md"),
  en: File.join(ROOT, "_pages/rbd-coordinate-audit-en.md")
}.freeze

def assert(condition, message)
  raise CloseoutError, message unless condition
end

def read_post(path)
  text = File.read(path, encoding: "UTF-8")
  match = text.match(/\A---\s*\n(.*?)\n---\s*\n(.*)\z/m)
  raise CloseoutError, "front matter inválido: #{path}" unless match
  front = YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: false)
  [front, match[2]]
end

def word_count(body)
  markdown = body.gsub(/\{%.*?%\}/m, " ")
  html = Kramdown::Document.new(markdown).to_html
  alternatives = html.scan(/<img\b[^>]*\balt="([^"]*)"/im).flatten.join(" ")
  renderable = CGI.unescapeHTML(html.gsub(/<[^>]+>/m, " "))
  "#{renderable} #{alternatives}".split(/\s+/).reject(&:empty?).length
end

def require_fragments(body, fragments, label)
  lower = body.downcase
  fragments.each { |fragment| assert(lower.include?(fragment.downcase), "#{label}: falta #{fragment}") }
end

def forbid_fragments(body, fragments, label)
  lower = body.downcase
  fragments.each { |fragment| assert(!lower.include?(fragment.downcase), "#{label}: conserva #{fragment}") }
end

def verify(posts, decisions, annexes)
  i_es_front, i_es = posts.fetch(:i_es)
  i_en_front, i_en = posts.fetch(:i_en)
  ii_es_front, ii_es = posts.fetch(:ii_es)
  ii_en_front, ii_en = posts.fetch(:ii_en)
  annex_es = annexes.fetch(:es)
  annex_en = annexes.fetch(:en)

  expected_titles = {
    i_es: decisions.dig("posts", "post_i", "title"),
    i_en: "Replicating my thesis in three spoonfuls (part I): what survived and what the evidence corrected",
    ii_es: decisions.dig("posts", "post_ii", "title"),
    ii_en: "Extending my thesis in three spoonfuls (part II): what school turnover still cannot tell us"
  }
  { i_es: i_es_front, i_en: i_en_front, ii_es: ii_es_front, ii_en: ii_en_front }.each do |key, front|
    assert(front.fetch("title") == expected_titles.fetch(key), "#{key}: título derivó")
    assert(front.fetch("last_modified_at").to_s.start_with?("2026-10-17"), "#{key}: fecha de modificación derivó")
  end
  assert(ii_es_front.fetch("subtitle") == decisions.dig("posts", "post_ii", "subtitle"), "ii_es: subtítulo derivó")
  assert(ii_es_front.fetch("ref") == ii_en_front.fetch("ref") && ii_es_front.fetch("permalink") == ii_en_front.fetch("permalink"), "post II: ref o permalink ES/EN difiere")
  assert(i_es_front.fetch("ref") == i_en_front.fetch("ref") && i_es_front.fetch("permalink") == i_en_front.fetch("permalink"), "post I: ref o permalink ES/EN difiere")
  [i_es_front, i_en_front, ii_es_front, ii_en_front].each do |front|
    assert(front.fetch("table_contract") == "explicit-v1", "contrato responsivo de tablas ausente")
  end

  i_range = decisions.dig("posts", "post_i", "spanish_word_range")
  ii_range = decisions.dig("posts", "post_ii", "spanish_word_range")
  i_es_words = word_count(i_es)
  ii_es_words = word_count(ii_es)
  assert((i_range[0]..i_range[1]).cover?(i_es_words), "post I ES: extensión #{i_es_words} fuera de #{i_range}")
  assert((ii_range[0]..ii_range[1]).cover?(ii_es_words), "post II ES: extensión #{ii_es_words} fuera de #{ii_range}")
  assert((word_count(i_en) - i_es_words).abs <= 180, "post I: extensión ES/EN perdió paridad")
  assert((word_count(ii_en) - ii_es_words).abs <= 180, "post II: extensión ES/EN perdió paridad")

  require_fragments(i_es, [
    "## Cucharada 1: qué sobrevivió", "## Cucharada 2: quién se equivocó",
    "## Cucharada 3: qué quedó listo", "## Cierre: de replicar a extender",
    "50 hipótesis técnicas", "34 juicios editoriales", "Tabla 1.", "Tabla 2.", "Tabla 3.",
    "cara-a-cara-movilidad.webp", "cara-a-cara-ihh.webp", "sombra-de-la-muerte.webp",
    "parte II]", "retoma estas tres preguntas"
  ], "post I ES")
  require_fragments(i_en, [
    "## Spoonful 1: what survived", "## Spoonful 2: who was wrong",
    "## Spoonful 3: what is ready", "## Closing: from replication to extension",
    "50 technical hypotheses", "34 editorial judgements", "Table 1.", "Table 2.", "Table 3.",
    "cara-a-cara-movilidad.webp", "cara-a-cara-ihh.webp", "sombra-de-la-muerte.webp",
    "Part II]", "revisits these three questions"
  ], "post I EN")
  forbid_fragments(i_es + i_en, ["AI at least publishes", "notas de versión", "do_058", "do_059", "do_060", ".d2"], "post I")

  require_fragments(ii_es, [
    "## Cucharada 1: antes de evaluar el recambio, hay que saber qué cambió realmente",
    "## Cucharada 2:", "## Cucharada 3:",
    "## Cierre: evaluar la transición, no celebrar el movimiento",
    "«no estimable» no significa cero", "regresión a la media", "Ley 20.529",
    "capacidad docente", "artículo", "auditoria-coordenadas-rbd",
    "{% include thesis-extension-stylized-evidence.html %}",
    "ninguna de las 25 combinaciones", "cuatro regiones tratadas y diez de control",
    "artículo 31", "0,5341", "cobertura nominal de 95 % es aproximada"
  ], "post II ES")
  require_fragments(ii_en, [
    "## Spoonful 1: before evaluating turnover, establish what actually changed",
    "## Spoonful 2:", "## Spoonful 3:",
    "## Closing: evaluate the transition, do not celebrate movement",
    "“not estimable” does not mean zero", "regression to the mean", "Law 20,529",
    "teaching capacity", "article", "auditoria-coordenadas-rbd",
    "{% include thesis-extension-stylized-evidence.html %}",
    "none of the 25 territory-horizon combinations", "four treated and ten control regions",
    "Article 31", "0.5341", "nominal 95% coverage is approximate"
  ], "post II EN")
  forbid_fragments(ii_es + ii_en, [
    "Lo Barnechea", "Lo Prado", "NOT_ESTIMABLE", "`999`", "112 celdas", "112 cells",
    "Abrir lámina", "Open static", "estilizada-mapa-el-salvador", "parte III", "part III",
    "0,45 km", "0.45 km", "826 m", "825,551 m", "825.551 m",
    "0,448903 km", "0.448903 km", "1,272025 km", "1.272025 km"
  ], "post II")
  assert(ii_es.scan("{% include thesis-extension-stylized-evidence.html %}").length == 1, "post II ES: visor ausente o duplicado")
  assert(ii_en.scan("{% include thesis-extension-stylized-evidence.html %}").length == 1, "post II EN: visor ausente o duplicado")
  assert(ii_es.scan(/^\| SLEP \|/).length == 1 && ii_es.scan(/^\| SAE \|/).length == 1, "post II ES: tabla SLEP/SAE derivó")
  assert(ii_en.scan(/^\| SLEP \|/).length == 1 && ii_en.scan(/^\| SAE \|/).length == 1, "post II EN: tabla SLEP/SAE derivó")

  required_numbers = ["900", "330", "665", "21", "8", "0.029", "0.0035", "0.0042", "391", "390"]
  es_normalized = ii_es.tr("−,", "-.")
  en_normalized = ii_en.tr("−", "-")
  required_numbers.each do |number|
    assert(es_normalized.include?(number) && en_normalized.include?(number), "post II: cifra bilingüe ausente #{number}")
  end

  require_fragments(annex_es, [
    "## Auditoría específica del caso El Salvador", "| Puntos oficiales conservados | 2 |",
    "| Candidatos OSM retenidos para contraste | 2 |", "825,551 m", "1,272025 km", "0,448903 km",
    "GeoJSON del contraste de El Salvador"
  ], "anexo ES")
  require_fragments(annex_en, [
    "## Audit of the El Salvador case", "| Official points retained | 2 |",
    "| OSM candidates retained for comparison | 2 |", "825.551 m", "1.272025 km", "0.448903 km",
    "El Salvador contrast GeoJSON"
  ], "anexo EN")
  forbid_fragments(annex_en, ["six points", "six-point contrast"], "anexo EN")
  require_fragments(i_es, ["Tasas 6,3; 4,5; 1,6"], "post I ES")
  require_fragments(i_en, ["Rates 6.3, 4.5, and 1.6", "<strong>Figure 2</strong> —"], "post I EN")

  {
    post_i_es_words: i_es_words,
    post_i_en_words: word_count(i_en),
    post_ii_es_words: ii_es_words,
    post_ii_en_words: word_count(ii_en)
  }
end

def verify_research_root(path)
  freeze_path = File.join(path, "audit/scientific_release_freeze.json")
  author_case_path = File.join(path, "research/article_post2/el_salvador_author_case.yaml")
  assert(File.file?(freeze_path), "freeze científico ausente: #{freeze_path}")
  assert(File.file?(author_case_path), "caso autoral ausente: #{author_case_path}")

  freeze = JSON.parse(File.read(freeze_path, encoding: "UTF-8"))
  author_case = YAML.safe_load(File.read(author_case_path, encoding: "UTF-8"), aliases: false)
  assert(freeze.fetch("freeze_revision") == 10, "freeze científico no está en revisión 10")
  assert(freeze.dig("snapshot_semantics", "cross_environment_byte_identity_established") == false,
         "freeze promovió identidad byte a byte entre entornos")
  assert(author_case.dig("selection", "systematic_sample_member") == false,
         "El Salvador fue promovido a la muestra sistemática")
  assert(author_case.dig("selection", "uses_outcomes") == false,
         "El Salvador fue seleccionado usando resultados")
  assert(author_case.dig("schools", "geodesic_distance_km") == 1.272025,
         "distancia cartográfica del caso autoral derivó")
  assert(author_case.dig("schools", "official_coordinate_distance_km") == 0.448903,
         "distancia oficial del caso autoral derivó")
end

def clean_tree?(path)
  output, status = Open3.capture2("git", "status", "--porcelain", chdir: path)
  status.success? && output.empty?
end

options = { self_test: false, final_commit_audit: false, research_root: nil }
OptionParser.new do |parser|
  parser.on("--self-test") { options[:self_test] = true }
  parser.on("--final-commit-audit") { options[:final_commit_audit] = true }
  parser.on("--research-root PATH") { |value| options[:research_root] = File.expand_path(value, ROOT) }
end.parse!

begin
  decisions = YAML.safe_load(File.read(DECISIONS, encoding: "UTF-8"), aliases: false)
  posts = POSTS.transform_values { |path| read_post(path) }
  annexes = ANNEXES.transform_values { |path| File.read(path, encoding: "UTF-8") }
  if options[:self_test]
    probes = [
      ["retired-territorial-case", lambda { |mutant_posts, _mutant_annexes| mutant_posts[:ii_es][1] << "\nLo Prado\n" }, "post II: conserva Lo Prado"],
      ["body-distance-leak", lambda { |mutant_posts, _mutant_annexes| mutant_posts[:ii_es][1] << "\n0,448903 km\n" }, "post II: conserva 0,448903 km"],
      ["annex-en-six-point-regression", lambda { |_mutant_posts, mutant_annexes| mutant_annexes[:en] << "\nsix points\n" }, "anexo EN: conserva six points"]
    ]
    observed = probes.map do |name, mutation, expected|
      mutant_posts = Marshal.load(Marshal.dump(posts))
      mutant_annexes = Marshal.load(Marshal.dump(annexes))
      mutation.call(mutant_posts, mutant_annexes)
      begin
        verify(mutant_posts, decisions, mutant_annexes)
      rescue CloseoutError => error
        raise unless error.message == expected
        { probe: name, error: error.message }
      else
        raise CloseoutError, "self-test no observó #{name}"
      end
    end
    warn JSON.generate(result: "EXPECTED_FAIL", probes: observed)
    exit 1
  end
  counts = verify(posts, decisions, annexes)
  verify_research_root(options[:research_root]) if options[:research_root]
  if options[:final_commit_audit]
    research_root = options[:research_root] || File.expand_path("../../incubadora/tesis_mae_mejorada", ROOT)
    assert(clean_tree?(ROOT), "commit final: árbol del blog no está limpio")
    assert(clean_tree?(research_root), "commit final: árbol científico no está limpio")
  end
  puts JSON.generate({ result: "PASS", final_commit_audit: options[:final_commit_audit] }.merge(counts))
rescue CloseoutError, KeyError, Psych::SyntaxError => error
  warn JSON.generate(result: "FAIL", error: error.message)
  exit 1
end
