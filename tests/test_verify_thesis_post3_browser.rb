# frozen_string_literal: true

require "minitest/autorun"
require "open3"

class VerifyThesisPost3BrowserTest < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  SCRIPT = File.join(ROOT, "scripts/verify_thesis_post3_browser.mjs")
  FIXTURES = %w[
    overflow
    missing-figure
    wrong-theme
    zero-size
    private-content
    missing-table
    missing-visual-identity
    mismatched-editorial-width
    off-theme-panel
    missing-he-agenda
    he-blocker
  ].freeze

  def test_each_fixture_reaches_its_expected_red
    FIXTURES.each do |fixture|
      output, status = Open3.capture2e("node", SCRIPT, "--fixture", fixture, chdir: ROOT)
      assert_equal 1, status.exitstatus, "#{fixture}:\n#{output}"
      assert_includes output, '"status":"EXPECTED_FAIL"', fixture
      assert_includes output, %Q{"fixture":"#{fixture}"}, fixture
    end
  end

  def test_live_gate_requires_an_artifact_root
    output, status = Open3.capture2e("node", SCRIPT, chdir: ROOT)
    assert_equal 2, status.exitstatus, output
    assert_includes output, "--artifact-root is required"
  end
end
