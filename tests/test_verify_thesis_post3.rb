# frozen_string_literal: true
require "minitest/autorun"
require "open3"
require "tmpdir"
class VerifyThesisPost3Test < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  SCRIPT = File.join(ROOT, "scripts/verify_thesis_post3.rb")
  def test_missing_contract_fails_closed
    Dir.mktmpdir do |dir|
      output, status = Open3.capture2e("ruby", SCRIPT, "--contract", File.join(dir, "absent.json"), chdir: ROOT)
      assert_equal 1, status.exitstatus, output
      assert_includes output, "publication contract missing"
    end
  end
  def test_legacy_fixture_is_rejected_before_gate
    output, status = Open3.capture2e("ruby", SCRIPT, "--fixture", "primary-number-drift", chdir: ROOT)
    assert_equal 2, status.exitstatus, output
    assert_includes output, "POST3_USAGE_ERROR"
  end
  def test_language_mode_cannot_bypass_missing_contract
    Dir.mktmpdir do |dir|
      output, status = Open3.capture2e("ruby", SCRIPT, "--lang", "es", "--contract", File.join(dir, "absent.json"), chdir: ROOT)
      assert_equal 1, status.exitstatus, output
    end
  end
end
