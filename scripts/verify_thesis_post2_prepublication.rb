#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "json"
require "optparse"
require "pathname"
require "tmpdir"
require "yaml"

class Post2GateError < StandardError
  attr_reader :code

  def initialize(code, message)
    @code = code
    super("#{code}: #{message}")
  end
end

Document = Data.define(:path, :front_matter, :body)

class ThesisPost2PrepublicationVerifier
  LEAKS = {
    "PLACEHOLDER" => /\bPLACEHOLDER\b/,
    "PH marker" => /\bPH-\d{2}\b/i,
    "Nota de edición" => /Nota de edici[oó]n/i,
    "editorial comment" => /<!--(?:(?!-->).)*(?:VERSI[ÓO]N DE TRABAJO|NOTA (?:DE )?EDICI[ÓO]N|EDITORIAL|PLACEHOLDER|PH-\d{2})(?:(?!-->).)*-->/im
  }.freeze
  CAUSAL_BOUNDARY = /(?:no (?:identifican?|estima|permite identificar|demuestra).{0,50}causal|no sabemos.{0,50}(?:efecto|mejor[oó])|asociaci[oó]n.{0,50}no.{0,30}causal|(?:none of this|do(?:es)? not) identif(?:y|ies).{0,50}causal|association.{0,50}not.{0,30}causal)/i
  ANNEX_REF = "auditoria-coordenadas-rbd"
  ANNEX_SOURCE_PERMALINK = "/datos/educacion/auditoria-coordenadas-rbd/"
  ANNEX_RENDERED_PATHS = {
    "es" => "/datos/educacion/auditoria-coordenadas-rbd/",
    "en" => "/en/datos/educacion/auditoria-coordenadas-rbd/"
  }.freeze
  PUBLIC_DATA_PATH = "assets/data/thesis-extension-post2/coordinate-audit-summary.json"
  PUBLIC_RECORD_FIELDS = %w[case_status confidence count distance_band_m region_code signal source_year].freeze

  def initialize(root:)
    @root = Pathname(root).expand_path
  end

  def verify(stage:, site_dir: nil)
    documents = source_documents
    if stage == "annex"
      annexes = documents.select { |document| document.front_matter["ref"] == ANNEX_REF }
      verify_hygiene(annexes.map(&:path))
      verify_annex_sources(annexes)
      verify_public_data
      return true
    end
    verify_hygiene(documents.map(&:path))
    verify_unique_identity(documents)
    post2 = documents.select { |document| document.front_matter["ref"] == "extender-tesis-no-es-agregar-anos" }
    post2.each { |document| verify_first_screen(document) }
    if stage == "h1"
      verify_annex_sources(documents)
      verify_public_data
    end
    verify_built_site(Pathname(site_dir)) if site_dir
    true
  end

  def verify_hygiene(paths)
    paths.each do |path|
      content = path.read
      LEAKS.each do |label, pattern|
        next unless content.match?(pattern)

        raise Post2GateError.new("public-editorial-leak", "#{label} in #{path}")
      end
    end
  end

  def verify_unique_identity(documents)
    grouped = documents.group_by do |document|
      front = document.front_matter
      [front["lang"], front["ref"], front["permalink"]]
    end
    duplicates = grouped.select do |identity, entries|
      identity.none?(&:nil?) && entries.length > 1
    end
    return if duplicates.empty?

    identity, entries = duplicates.first
    raise Post2GateError.new(
      "duplicate-jekyll-identity",
      "#{identity.inspect}: #{entries.map { |entry| entry.path.to_s }.join(', ')}"
    )
  end

  def verify_first_screen(document)
    body_before_h2 = document.body.split(/^##\s+/, 2).first
    visible = body_before_h2
      .gsub(/<!--.*?-->/m, " ")
      .gsub(/\{%.*?%\}/m, " ")
      .gsub(/<[^>]+>/, " ")
      .gsub(/!\[[^\]]*\]\([^)]*\)/, " ")
      .gsub(/\[([^\]]+)\]\([^)]*\)/, "\\1")
      .gsub(/[#*_>`~-]/, " ")
      .split
    first_words = visible.first(120).join(" ")
    return if first_words.match?(CAUSAL_BOUNDARY)

    raise Post2GateError.new("causal-boundary-too-late", document.path.to_s)
  end

  def verify_annex_sources(documents)
    annexes = documents.select { |document| document.front_matter["ref"] == ANNEX_REF }
    languages = annexes.map { |document| document.front_matter["lang"] }.sort
    unless languages == %w[en es]
      raise Post2GateError.new("annex-language-pair-missing", languages.inspect)
    end
    refs = annexes.map { |document| document.front_matter["ref"] }.uniq
    raise Post2GateError.new("annex-ref-mismatch", refs.inspect) unless refs.length == 1 && refs.first
    permalinks = annexes.map { |document| document.front_matter["permalink"] }.uniq
    unless permalinks == [ANNEX_SOURCE_PERMALINK]
      raise Post2GateError.new("annex-permalink-mismatch", permalinks.inspect)
    end

    annexes.each do |document|
      front = document.front_matter
      og_image = front.dig("header", "og_image")
      if front["description"].to_s.strip.empty? || og_image.to_s.strip.empty?
        raise Post2GateError.new("annex-metadata-missing", document.path.to_s)
      end
      unless document.body.include?("OpenStreetMap") && document.body.match?(/ODbL/i)
        raise Post2GateError.new("annex-attribution-missing", document.path.to_s)
      end
      other_language = front["lang"] == "es" ? "en" : "es"
      unless document.body.include?(ANNEX_RENDERED_PATHS.fetch(other_language))
        raise Post2GateError.new("annex-language-link-missing", document.path.to_s)
      end
      required = if front["lang"] == "es"
                   ["12.038", "78", "18.588", "6.601", "5.515", "126", "Errores oficiales confirmados", "agregados"]
                 else
                   ["12,038", "78", "18,588", "6,601", "5,515", "126", "Confirmed official errors", "aggregates"]
                 end
      missing = required.reject { |fragment| document.body.include?(fragment) }
      unless missing.empty?
        raise Post2GateError.new("annex-evidence-missing", "#{document.path}: #{missing.join(', ')}")
      end
      unless document.body.include?("/assets/data/thesis-extension-post2/coordinate-audit-summary.json")
        raise Post2GateError.new("annex-data-link-missing", document.path.to_s)
      end
    end
  end

  def verify_public_data(payload = nil)
    payload ||= JSON.parse(@root.join(PUBLIC_DATA_PATH).read)
    expected = {
      "schema_version" => 1,
      "scope.official_rows_audited" => 12_116,
      "scope.operating_establishments" => 12_038,
      "scope.authorized_without_enrollment" => 78,
      "matching.official_rows_with_candidate" => 6_601,
      "matching.official_rows_without_candidate" => 5_515,
      "adjudication.manual_review_rows" => 126,
      "adjudication.official_errors_confirmed" => 0,
      "license.public_surface" => "aggregate_only",
      "license.combined_row_level_csv_published" => false,
      "license.mineduc_republication_assumed" => false
    }
    expected.each do |path, value|
      observed = path.split(".").reduce(payload) { |node, key| node.fetch(key) }
      raise Post2GateError.new("public-data-boundary", "#{path}=#{observed.inspect}") unless observed == value
    end
    scope = payload.fetch("scope")
    matching = payload.fetch("matching")
    total = scope.fetch("official_rows_audited")
    unless scope.fetch("operating_establishments") + scope.fetch("authorized_without_enrollment") == total &&
           matching.fetch("official_rows_with_candidate") + matching.fetch("official_rows_without_candidate") == total
      raise Post2GateError.new("public-data-denominator-mismatch", total.to_s)
    end
    records = payload.fetch("aggregated_records")
    raise Post2GateError.new("public-data-empty", PUBLIC_DATA_PATH) if records.empty?
    records.each do |record|
      unless record.keys.sort == PUBLIC_RECORD_FIELDS
        raise Post2GateError.new("public-data-row-level-field", record.keys.sort.inspect)
      end
    end
    attribution = payload.dig("license", "attribution").to_s
    odbl = payload.dig("license", "odbl").to_s
    unless attribution.include?("OpenStreetMap") && odbl.match?(/odbl/i)
      raise Post2GateError.new("public-data-attribution-missing", PUBLIC_DATA_PATH)
    end
  end

  def verify_built_site(site_dir)
    raise Post2GateError.new("built-site-missing", site_dir.to_s) unless site_dir.directory?

    files = ANNEX_RENDERED_PATHS.transform_values do |permalink|
      site_dir.join(permalink.sub(%r{\A/}, ""), "index.html")
    end
    verify_hygiene(files.values)
    files.each do |page_language, path|
      raise Post2GateError.new("annex-built-page-missing", path.to_s) unless path.file?

      html = path.read
      raise Post2GateError.new("annex-canonical-missing", path.to_s) unless html.match?(/rel=["']canonical["']/i)
      ANNEX_RENDERED_PATHS.each do |language, permalink|
        expected_href = "https://3cucharadas.cl#{permalink}"
        next if html.match?(/rel=["']alternate["'][^>]*hreflang=["']#{language}["'][^>]*href=["']#{Regexp.escape(expected_href)}["']/i)

        raise Post2GateError.new("annex-hreflang-mismatch", "#{path}: #{page_language}->#{language}")
      end
    end
  end

  def parse_document(path)
    content = path.read
    match = content.match(/\A---\s*\n(.*?)\n---\s*\n(.*)\z/m)
    raise Post2GateError.new("front-matter-missing", path.to_s) unless match

    front = YAML.safe_load(match[1], permitted_classes: [Date, Time], aliases: true) || {}
    Document.new(path:, front_matter: front, body: match[2])
  end

  private

  def source_documents
    %w[_drafts _posts _pages].flat_map do |directory|
      @root.join(directory).glob("**/*.{md,markdown,html}").map { |path| parse_document(path) }
    end
  end
end

SELF_TESTS = {
  "hygiene" => "public-editorial-leak",
  "duplicate-identity" => "duplicate-jekyll-identity",
  "causal-first-screen" => "causal-boundary-too-late",
  "annex-metadata" => "annex-metadata-missing",
  "public-data-boundary" => "public-data-boundary"
}.freeze

def run_self_test(name, verifier)
  expected = SELF_TESTS.fetch(name)
  Dir.mktmpdir("post2-prepublication-") do |directory|
    root = Pathname(directory)
    case name
    when "hygiene"
      path = root.join("source.md")
      path.write("PLACEHOLDER PH-11")
      verifier.verify_hygiene([path])
    when "duplicate-identity"
      front = { "lang" => "es", "ref" => "same", "permalink" => "/same/" }
      documents = [
        Document.new(path: root.join("a.md"), front_matter: front, body: ""),
        Document.new(path: root.join("b.md"), front_matter: front, body: "")
      ]
      verifier.verify_unique_identity(documents)
    when "causal-first-screen"
      document = Document.new(
        path: root.join("post.md"),
        front_matter: {},
        body: "Los datos describen aperturas y cierres.\n\n## Resultado\nNo identifica causalidad."
      )
      verifier.verify_first_screen(document)
    when "annex-metadata"
      base = {
        "ref" => ThesisPost2PrepublicationVerifier::ANNEX_REF,
        "description" => "",
        "header" => {},
      }
      documents = %w[es en].map do |language|
      front = base.merge(
        "lang" => language,
        "permalink" => ThesisPost2PrepublicationVerifier::ANNEX_SOURCE_PERMALINK
      )
        other = ThesisPost2PrepublicationVerifier::ANNEX_RENDERED_PATHS.fetch(
          language == "es" ? "en" : "es"
        )
        Document.new(
          path: root.join("#{language}.md"),
          front_matter: front,
          body: "© OpenStreetMap contributors ODbL #{other}"
        )
      end
      verifier.verify_annex_sources(documents)
    when "public-data-boundary"
      payload = JSON.parse(
        Pathname(__dir__).parent.join(
          ThesisPost2PrepublicationVerifier::PUBLIC_DATA_PATH
        ).read
      )
      payload["license"]["combined_row_level_csv_published"] = true
      verifier.verify_public_data(payload)
    end
  end
  warn "SELF_TEST_WRONG_RESULT #{name}: expected #{expected}, gate passed"
  2
rescue Post2GateError => error
  if error.code == expected
    warn "EXPECTED_FAIL #{name}: #{error.message}"
    1
  else
    warn "SELF_TEST_WRONG_FAILURE #{name}: expected #{expected}, got #{error.code}"
    2
  end
end

begin
  options = { stage: "source" }
  parser = OptionParser.new do |opts|
    opts.on("--stage STAGE", %w[source annex h1]) { |value| options[:stage] = value }
    opts.on("--site-dir PATH") { |value| options[:site_dir] = value }
    opts.on("--self-test RULE", SELF_TESTS.keys) { |value| options[:self_test] = value }
    opts.on("--list-self-tests") { options[:list] = true }
  end
  parser.parse!
  if options[:list]
    puts SELF_TESTS.keys
    exit 0
  end
  verifier = ThesisPost2PrepublicationVerifier.new(root: Pathname(__dir__).parent)
  exit run_self_test(options[:self_test], verifier) if options[:self_test]

  verifier.verify(stage: options[:stage], site_dir: options[:site_dir])
  puts "POST2_PREPUBLICATION_OK stage=#{options[:stage]}"
rescue OptionParser::ParseError, Psych::Exception, Errno::ENOENT, Post2GateError => error
  warn "POST2_PREPUBLICATION_FAIL #{error.message}"
  exit 1
end
