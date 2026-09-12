require "fileutils"
require "json"
require "minitest/autorun"
require "open3"
require "tmpdir"
require "yaml"
require "date"

class ReconciliarDistribucionTest < Minitest::Test
  def setup
    @root = Dir.mktmpdir
    FileUtils.mkdir_p("#{@root}/_data")
    FileUtils.mkdir_p("#{@root}/state")
    @file = "#{@root}/_data/distribucion.yml"
    File.write(@file, "# preserve this comment\n- slug: fixture\n  ref_interno: fixture\n  publicaciones: []\n- slug: other\n  ref_interno: other\n  publicaciones: []\n")
  end

  def teardown
    FileUtils.remove_entry(@root)
  end

  def event(ref = "fixture", kind = "network_published")
    { event: kind, ref: ref, network: "mastodon", timestamp: "2026-09-12T12:00:00Z",
      result: { root_url: "https://example.org/#{ref}/es", reply_url: "https://example.org/#{ref}/en" } }
  end

  def ledger(*events)
    File.write("#{@root}/state/ledger.jsonl", events.map { |e| JSON.generate(e) }.join("\n") + "\n")
  end

  def run_script(*args)
    Open3.capture3({ "DISTRIBUCION_ROOT" => @root, "CUCHARADAS_DIFUSION_STATE_DIR" => "#{@root}/state" },
      "ruby", File.expand_path("../scripts/reconciliar_distribucion.rb", __dir__), *args)
  end

  def test_scoped_reconciliation_is_idempotent_and_preserves_comments
    ledger(event, event, event("other"))
    _out, _err, status = run_script("--ref", "fixture", "--check")
    refute status.success?
    _out, err, status = run_script("--ref", "fixture", "--aplicar")
    assert status.success?, err
    first = File.read(@file)
    data = YAML.safe_load(first, permitted_classes: [Date])
    assert_equal 1, data[0]["publicaciones"].length
    assert_equal [], data[1]["publicaciones"]
    assert_includes first, "# preserve this comment"
    _out, err, status = run_script("--ref", "fixture", "--aplicar")
    assert status.success?, err
    assert_equal first, File.read(@file)
  end

  def test_missing_explicit_ledger_does_not_use_another_ledger
    _out, _err, status = run_script("--ref", "fixture", "--aplicar")
    refute status.success?
  end

  def test_rolled_back_publication_cannot_close_ref
    ledger(event, event("fixture", "network_rolled_back"))
    _out, _err, status = run_script("--ref", "fixture", "--aplicar")
    refute status.success?
    assert_includes File.read(@file), "publicaciones: []"
  end

  def test_corrupt_ledger_does_not_silently_skip_events
    ledger(event)
    File.open("#{@root}/state/ledger.jsonl", "a") { |f| f.puts("{broken") }
    before = File.read(@file)
    _out, _err, status = run_script("--ref", "fixture", "--aplicar")
    refute status.success?
    assert_equal before, File.read(@file)
  end

  def test_missing_english_reply_is_repaired_without_duplicate_platform
    ledger(event)
    File.write(@file, "# comment\n- slug: fixture\n  ref_interno: fixture\n  publicaciones:\n  - plataforma: mastodon\n    url_publicada: https://example.org/fixture/es\n")
    _out, err, status = run_script("--ref", "fixture", "--aplicar")
    assert status.success?, err
    pubs = YAML.safe_load_file(@file)[0]["publicaciones"]
    assert_equal 1, pubs.length
    assert_equal "https://example.org/fixture/en", pubs[0]["url_publicada_en"]
  end
end
