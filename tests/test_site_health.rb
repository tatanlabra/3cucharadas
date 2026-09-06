require 'minitest/autorun'
require 'tmpdir'
require 'fileutils'
require_relative '../scripts/lib/site_health'

class SiteHealthTest < Minitest::Test
  ROOT = File.expand_path('..', __dir__)
  def contract
    YAML.safe_load_file(File.join(ROOT, 'docs/contracts/site-health.yaml'))
  end
  def test_contract_has_real_phases
    assert SiteHealth.validate_contract(contract)
    broken = contract
    broken['phases'] = []
    assert_raises(RuntimeError) { SiteHealth.validate_contract(broken) }
    broken = contract
    broken['phases'][2]['falsified_by'] = ''
    assert_raises(RuntimeError) { SiteHealth.validate_contract(broken) }
  end
  def test_runtime_drift_red_then_green
    Dir.mktmpdir do |dir|
      %w[.nvmrc package.json package-lock.json Gemfile.lock .gitlab-ci.yml].each { |file| FileUtils.cp(File.join(ROOT, file), dir) }
      assert_empty SiteHealth.runtime_violations(dir, contract)
      path = File.join(dir, '.gitlab-ci.yml')
      original = File.read(path)
      File.write(path, original.sub('NODE_VERSION: "26.8.1"', 'NODE_VERSION: "24.18.0"'))
      assert_includes SiteHealth.runtime_violations(dir, contract), 'node CI drift'
      File.write(path, original)
      assert_empty SiteHealth.runtime_violations(dir, contract)
    end
  end

  def test_workflow_yaml_rejects_empty_and_unquoted_colon_then_recovers
    assert_operator SiteHealth.validate_workflows(ROOT), :>, 0
    Dir.mktmpdir do |dir|
      assert_raises(RuntimeError) { SiteHealth.validate_workflows(dir) }
      FileUtils.mkdir_p(File.join(dir, '.github/workflows'))
      path = File.join(dir, '.github/workflows/check.yml')
      File.write(path, "jobs:\n  check:\n    env:\n      MODE: expression('maintenance: drafts-only')\n")
      assert_raises(Psych::SyntaxError) { SiteHealth.validate_workflows(dir) }
      File.write(path, "jobs:\n  check:\n    env:\n      MODE: \"expression('maintenance: drafts-only')\"\n")
      assert_equal 1, SiteHealth.validate_workflows(dir)
    end
  end

  def test_public_css_uses_the_live_version_and_rejects_missing_evidence
    assert_raises(RuntimeError) { SiteHealth.public_css_url('<html></html>') }
    assert_raises(RuntimeError) { SiteHealth.public_css_url('<link href="/assets/css/main.css?v=1"><link href="/assets/css/main.css?v=2">') }
    assert_equal 'https://3cucharadas.cl/assets/css/main.css?v=42', SiteHealth.public_css_url('<link rel="stylesheet" href="/assets/css/main.css?v=42">')
  end
end
