# frozen_string_literal: true

require "minitest/autorun"
require "open3"

class VerifyThesisPost4BrowserTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  SCRIPT = File.join(ROOT, "scripts/verify_thesis_post4_browser.mjs")
  FIXTURES = %w[overflow missing-figure wrong-figure-limit wrong-theme private-content missing-table
                missing-series-link missing-annex stale-build].freeze

  def test_each_fixture_reaches_its_expected_red
    FIXTURES.each do |fixture|
      output, status = Open3.capture2e("node", SCRIPT, "--fixture", fixture, chdir: ROOT)
      assert_equal 1, status.exitstatus, "#{fixture}: #{output}"
      assert_includes output, '"status":"EXPECTED_FAIL"', fixture
    end
  end

  def test_live_gate_requires_an_artifact_root
    output, status = Open3.capture2e("node", SCRIPT, chdir: ROOT)
    assert_equal 2, status.exitstatus, output
    assert_includes output, "--artifact-root is required"
  end
end
