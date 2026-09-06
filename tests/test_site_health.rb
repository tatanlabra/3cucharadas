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
end
