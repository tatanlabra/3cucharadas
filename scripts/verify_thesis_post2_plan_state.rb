#!/usr/bin/env ruby
# frozen_string_literal: true

require "date"
require "digest"
require "optparse"
require "pathname"
require "tmpdir"
require "yaml"

class PlanStateError < StandardError
  attr_reader :code

  def initialize(code, message)
    @code = code
    super("#{code}: #{message}")
  end
end

class ThesisPost2PlanStateVerifier
  REQUIRED_PLACEHOLDERS = (1..18).map { |number| format("PH-%02d", number) }.freeze
  PLACEHOLDER_FIELDS = %w[
    id target_status requires_additional_research emergent_task_id
    publication_blocking evidence_paths claim_action unblock_condition
  ].freeze
  EMERGENT_FIELDS = %w[cause impact acceptance authority status].freeze
  CLOSED_TASK_STATUSES = %w[done complete completed closed].freeze
  RENDERED_PUBLIC_PATHS = %w[
    datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/index.html
    en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/index.html
    datos/educacion/auditoria-coordenadas-rbd/index.html
    en/datos/educacion/auditoria-coordenadas-rbd/index.html
  ].freeze
  PUBLIC_LEAKS = {
    "PLACEHOLDER" => /\bPLACEHOLDER\b/,
    "PH marker" => /\bPH-\d{2}\b/i,
    "Nota de edición" => /Nota de edici[oó]n/i,
    "editorial HTML comment" => /<!--(?:(?!-->).)*(?:VERSI[ÓO]N DE TRABAJO|NOTA (?:DE )?EDICI[ÓO]N|EDITORIAL|PLACEHOLDER|PH-\d{2})(?:(?!-->).)*-->/im
  }.freeze
  DEGRADING_ACTION = /(retirar|degradar|deferir|no afirmar|no atribuir|mantener .*limit|tratar .*contexto|hacer visibles?|declarar|evitar atribuci[oó]n)/i

  attr_reader :root, :state, :contract

  def initialize(root:, state:, contract:)
    @root = Pathname(root).expand_path
    @state = state
    @contract = contract
  end

  def verify(stage:, site_dir: nil)
    verify_registry
    verify_emergent_tasks
    verify_h1(site_dir:) if stage == "h1"
    true
  end

  def verify_registry
    registry = array_at(state, "placeholder_registry", "registry-missing")
    ids = registry.map { |entry| entry.fetch("id", nil) }
    missing = REQUIRED_PLACEHOLDERS - ids
    duplicates = ids.tally.select { |_id, count| count > 1 }.keys
    raise PlanStateError.new("registry-missing-ph", missing.join(", ")) unless missing.empty?
    raise PlanStateError.new("registry-duplicate-ph", duplicates.join(", ")) unless duplicates.empty?

    registry.each do |entry|
      missing_fields = PLACEHOLDER_FIELDS.reject { |field| entry.key?(field) }
      unless missing_fields.empty?
        raise PlanStateError.new("registry-missing-field", "#{entry['id']}: #{missing_fields.join(', ')}")
      end

      if entry["requires_additional_research"] && blank?(entry["emergent_task_id"])
        raise PlanStateError.new("registry-missing-task", entry["id"])
      end
      unless [true, false].include?(entry["publication_blocking"])
        raise PlanStateError.new("registry-invalid-blocking", entry["id"])
      end
      unless entry["evidence_paths"].is_a?(Array)
        raise PlanStateError.new("registry-invalid-evidence", entry["id"])
      end
    end
  end

  def verify_emergent_tasks
    tasks = array_at(state, "emergent_tasks", "tasks-missing")
    task_index = tasks.to_h { |task| [task["id"], task] }

    state.fetch("placeholder_registry").each do |entry|
      next unless entry["requires_additional_research"]

      task = task_index[entry["emergent_task_id"]]
      raise PlanStateError.new("registry-unknown-task", "#{entry['id']}: #{entry['emergent_task_id']}") unless task

      if CLOSED_TASK_STATUSES.include?(task["status"].to_s.downcase) && blank?(task["evidence"])
        raise PlanStateError.new("task-done-without-evidence", task["id"])
      end
    end

    tasks.select { |task| task["id"].to_s.match?(/\AE-(?:2[1-9]|3[0-4])\z/) }.each do |task|
      missing_fields = EMERGENT_FIELDS.reject { |field| !blank?(task[field]) }
      unless missing_fields.empty?
        raise PlanStateError.new("task-missing-field", "#{task['id']}: #{missing_fields.join(', ')}")
      end
      next unless %w[blocked deferred].include?(task["status"].to_s.downcase)
      next unless blank?(task["blocker"]) || blank?(task["unblock_condition"])

      raise PlanStateError.new("task-missing-unblock", task["id"])
    end
  end

  def verify_h1(site_dir: nil)
    registry = state.fetch("placeholder_registry")
    registry.each do |entry|
      closed = entry["status"] == entry["target_status"]
      if entry["publication_blocking"] && !closed
        raise PlanStateError.new("h1-blocking-placeholder-open", entry["id"])
      end
      if !entry["publication_blocking"] && !closed && entry["claim_action"].to_s !~ DEGRADING_ACTION
        raise PlanStateError.new("h1-nonblocking-claim-live", entry["id"])
      end
      next unless entry["publication_blocking"]

      missing = entry["evidence_paths"].reject { |path| resolve(path).file? }
      raise PlanStateError.new("h1-missing-evidence", "#{entry['id']}: #{missing.join(', ')}") unless missing.empty?
    end

    public_files = public_source_files
    public_files.concat(rendered_public_files(site_dir)) if site_dir
    verify_public_hygiene(public_files)
    verify_hashes
  end

  def verify_public_hygiene(files)
    files.uniq.each do |path|
      content = path.read
      PUBLIC_LEAKS.each do |label, pattern|
        next unless content.match?(pattern)

        raise PlanStateError.new("public-editorial-leak", "#{label} in #{path}")
      end
    end
  end

  def verify_hashes
    hashes = contract.fetch("content_hashes", {})
    path_index = contract.fetch("hash_path_index", {})
    raise PlanStateError.new("hash-index-empty", "hash_path_index") if path_index.empty?

    path_index.each do |key, relative_path|
      expected = hashes[key]
      raise PlanStateError.new("hash-value-missing", key) if blank?(expected)

      path = resolve(relative_path)
      raise PlanStateError.new("hash-path-missing", "#{key}: #{path}") unless path.file?

      actual = Digest::SHA256.file(path).hexdigest
      next if actual == expected

      raise PlanStateError.new("hash-mismatch", "#{key}: expected #{expected}, got #{actual}")
    end
  end

  private

  def array_at(document, key, error_code)
    value = document[key]
    raise PlanStateError.new(error_code, key) unless value.is_a?(Array)

    value
  end

  def blank?(value)
    value.nil? || value == "" || (value.respond_to?(:empty?) && value.empty?)
  end

  def resolve(path)
    root.join(path).cleanpath
  end

  def public_source_files
    candidates = []
    %w[_posts _pages].each do |directory|
      root.join(directory).glob("**/*.{md,markdown,html}").each do |path|
        content = path.read
        candidates << path if content.include?("ref: extender-tesis-no-es-agregar-anos") ||
                              content.include?("/datos/educacion/auditoria-coordenadas-rbd/") ||
                              content.include?("/en/datos/educacion/auditoria-coordenadas-rbd/")
      end
    end
    candidates
  end

  def rendered_public_files(site_dir)
    rendered_root = Pathname(site_dir)
    RENDERED_PUBLIC_PATHS.map do |relative_path|
      path = rendered_root.join(relative_path)
      raise PlanStateError.new("h1-rendered-surface-missing", path.to_s) unless path.file?

      path
    end
  end
end

SELF_TESTS = {
  "missing-ph" => "registry-missing-ph",
  "missing-task" => "registry-missing-task",
  "done-without-evidence" => "task-done-without-evidence",
  "blocking-open" => "h1-blocking-placeholder-open",
  "public-placeholder" => "public-editorial-leak",
  "hash-mismatch" => "hash-mismatch"
}.freeze

def deep_copy(value)
  Marshal.load(Marshal.dump(value))
end

def run_self_test(name, root, state, contract)
  expected_code = SELF_TESTS.fetch(name)
  test_state = deep_copy(state)
  test_contract = deep_copy(contract)
  verifier = ThesisPost2PlanStateVerifier.new(root:, state: test_state, contract: test_contract)

  case name
  when "missing-ph"
    test_state["placeholder_registry"].reject! { |entry| entry["id"] == "PH-18" }
    verifier.verify_registry
  when "missing-task"
    test_state["placeholder_registry"].find { |entry| entry["id"] == "PH-02" }["emergent_task_id"] = nil
    verifier.verify_registry
  when "done-without-evidence"
    test_state["emergent_tasks"].find { |task| task["id"] == "E-24" }["status"] = "done"
    verifier.verify_emergent_tasks
  when "blocking-open"
    test_state["placeholder_registry"].find { |entry| entry["id"] == "PH-01" }["status"] = "PENDIENTE"
    verifier.verify_h1
  when "public-placeholder"
    Dir.mktmpdir("post2-plan-state-") do |directory|
      path = Pathname(directory).join("leak.html")
      path.write("<p>PLACEHOLDER PH-11</p>")
      verifier.verify_public_hygiene([path])
    end
  when "hash-mismatch"
    Dir.mktmpdir("post2-plan-state-") do |directory|
      path = Pathname(directory).join("artifact.txt")
      path.write("current")
      test_contract["content_hashes"] = { "probe" => Digest::SHA256.hexdigest("other") }
      test_contract["hash_path_index"] = { "probe" => path.to_s }
      verifier.verify_hashes
    end
  end

  warn "SELF_TEST_WRONG_RESULT #{name}: expected #{expected_code}, gate passed"
  2
rescue PlanStateError => error
  if error.code == expected_code
    warn "EXPECTED_FAIL #{name}: #{error.message}"
    1
  else
    warn "SELF_TEST_WRONG_FAILURE #{name}: expected #{expected_code}, got #{error.code}: #{error.message}"
    2
  end
end

begin
options = {
  stage: "draft",
  state: "docs/plans/20261011-thesis-post2-closeout/PLAN_STATE.yml",
  contract: "docs/contracts/thesis-extension-post-ii-publication.yml"
}

parser = OptionParser.new do |opts|
  opts.banner = "Usage: ruby scripts/verify_thesis_post2_plan_state.rb [options]"
  opts.on("--stage STAGE", %w[draft h1]) { |value| options[:stage] = value }
  opts.on("--state PATH") { |value| options[:state] = value }
  opts.on("--contract PATH") { |value| options[:contract] = value }
  opts.on("--site-dir PATH") { |value| options[:site_dir] = value }
  opts.on("--self-test RULE", SELF_TESTS.keys) { |value| options[:self_test] = value }
  opts.on("--list-self-tests") { options[:list_self_tests] = true }
end
parser.parse!

if options[:list_self_tests]
  puts SELF_TESTS.keys
  exit 0
end

root = Pathname(__dir__).parent
state = YAML.safe_load(root.join(options[:state]).read, permitted_classes: [Date, Time], aliases: true)
contract = YAML.safe_load(root.join(options[:contract]).read, permitted_classes: [Date, Time], aliases: true)

if options[:self_test]
  exit run_self_test(options[:self_test], root, state, contract)
end

verifier = ThesisPost2PlanStateVerifier.new(root:, state:, contract:)
verifier.verify(stage: options[:stage], site_dir: options[:site_dir])
puts "PLAN_STATE_OK stage=#{options[:stage]} placeholders=#{state.fetch('placeholder_registry').length} emergent_tasks=#{state.fetch('emergent_tasks').length}"
exit 0
rescue OptionParser::ParseError, Psych::Exception, Errno::ENOENT, PlanStateError => error
  warn "PLAN_STATE_FAIL #{error.message}"
  exit 1
end
