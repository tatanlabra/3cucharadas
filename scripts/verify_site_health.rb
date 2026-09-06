#!/usr/bin/env ruby
# frozen_string_literal: true
require 'optparse'
require 'open3'
require 'tmpdir'
require 'fileutils'
require 'digest'
require 'net/http'
require 'time'
require_relative 'lib/site_health'

options = { profile: 'source', root: File.expand_path('..', __dir__) }
OptionParser.new do |p|
  p.on('--profile PROFILE', SiteHealth::PROFILES) { |v| options[:profile] = v }
  p.on('--root PATH') { |v| options[:root] = File.expand_path(v) }
  p.on('--report PATH') { |v| options[:report] = File.expand_path(v) }
end.parse!
abort 'Unexpected arguments' unless ARGV.empty?
root = options[:root]
report_path = options[:report] || File.join(Dir.mktmpdir('3c-health-'), 'report.json')
log_dir = File.join(File.dirname(report_path), 'logs')
FileUtils.mkdir_p(log_dir)
checks = []
record = lambda do |id, status, detail|
  checks << { id: id, status: status, detail: detail }
  puts "#{status} #{id}: #{detail}"
end
run = lambda do |id, command, env = {}|
  output, status = Open3.capture2e(env, *command, chdir: root)
  log = File.join(log_dir, "#{id}.log")
  File.write(log, output)
  checks << { id: id, status: status.success? ? 'PASS' : 'FAIL', command: command, exit_code: status.exitstatus, log: log }
  puts "#{checks.last[:status]} #{id} (#{status.exitstatus})"
  status.success?
rescue Errno::ENOENT => error
  record.call(id, 'NO_CONCLUYENTE', error.message)
  false
end
get_json = lambda do |url|
  uri = URI(url)
  response = Net::HTTP.start(uri.host, uri.port, use_ssl: true, open_timeout: 10, read_timeout: 25) { |http| http.get(uri.request_uri) }
  raise "HTTP #{response.code}: #{uri.host}" unless response.is_a?(Net::HTTPSuccess)
  JSON.parse(response.body)
end

begin
  contract = SiteHealth.validate_contract(YAML.safe_load_file(File.join(root, 'docs/contracts/site-health.yaml')))
  record.call('contract', 'PASS', 'Nonempty invariants and seven complete phase contracts')
  begin
    count = SiteHealth.validate_workflows(root)
    record.call('workflow-yaml', 'PASS', "#{count} workflows parse and have jobs")
  rescue Psych::Exception, RuntimeError => error
    record.call('workflow-yaml', 'FAIL', error.message)
  end
  errors = SiteHealth.runtime_violations(root, contract)
  record.call('runtime-declarations', errors.empty? ? 'PASS' : 'FAIL', errors.empty? ? 'Node/Bundler declarations agree' : errors.join('; '))
  run.call('git-integrity', %w[git fsck --full --no-dangling])
  run.call('whitespace', %w[git diff --check])
  run.call('governance', %w[ruby scripts/verify_repo_governance.rb --strict])
  run.call('visual-assets', %w[ruby scripts/verify_visual_assets.rb --strict])
  run.call('diffusion-coherence', %w[ruby scripts/verify_difusion_coherente.rb])
  %w[site_health polyglot_doctor math_keyboard jekyll_to_devto verify_distribution_done verify_repo_governance devto_draft_policy].each do |test|
    run.call("test-#{test}", ['ruby', "tests/test_#{test}.rb"])
  end
  run.call('test-notification', %w[python3 -m unittest tests/test_notify_telegram_publication.py], { 'PYTHONDONTWRITEBYTECODE' => '1' })
  run.call('test-accessible-regions', %w[python3 -m unittest discover -s tests/catastro_sii -p test_accessible_regions.py], { 'PYTHONDONTWRITEBYTECODE' => '1' })

  unless options[:profile] == 'source'
    version, status = Open3.capture2e('node', '--version')
    record.call('node-runtime', status.success? && version.strip == "v#{contract.dig('runtime', 'node')}" ? 'PASS' : 'FAIL', version.strip)
    version, status = Open3.capture2e('bundle', '--version', chdir: root)
    record.call('bundler-runtime', status.success? && version.include?(contract.dig('runtime', 'bundler')) ? 'PASS' : 'FAIL', version.strip)
    record.call('ruby-runtime', contract.dig('runtime', 'ruby_matrix').include?(RUBY_VERSION.split('.')[0, 2].join('.')) ? 'PASS' : 'FAIL', RUBY_VERSION)
    bundle_ok = run.call('bundle-check', %w[bundle check], { 'BUNDLE_FROZEN' => 'true' })
    run.call('doctor', %w[bundle exec jekyll doctor], { 'BUNDLE_FROZEN' => 'true' }) if bundle_ok
    %w[check:catastro check:catastro:static-css test:catastro test:memoria-gobernada].each { |task| run.call(task.tr(':', '-'), ['npm', 'run', task]) }
    run.call('test-geospatial', %w[python3 -m unittest discover -s tests/catastro_sii -p test_*.py], { 'PYTHONDONTWRITEBYTECODE' => '1' })
    geo = File.read(File.join(log_dir, 'test-geospatial.log'))
    skipped = geo[/skipped=(\d+)/, 1].to_i
    ran = geo[/Ran (\d+) tests/, 1].to_i
    record.call('geospatial-coverage', ran >= 43 && skipped <= 7 ? 'PASS' : 'NO_CONCLUYENTE', "#{ran} discovered, #{skipped} skipped; declared geospatial exception, not executed coverage")
    catastro = run.call('build-catastro', %w[npm run build:catastro])
    memory = run.call('build-memory', %w[npm run build:memoria-gobernada])
    run.call('graph-budget', %w[npm run check:memoria-gobernada:assets]) if memory
    if bundle_ok && catastro && memory
      %w[production future drafts].each do |mode|
        dest = File.join(File.dirname(report_path), "site-#{mode}")
        command = %w[bundle exec jekyll build --disable-disk-cache] + ['--destination', dest]
        command << '--future' unless mode == 'production'
        command << '--drafts' if mode == 'drafts'
        built = run.call("build-#{mode}", command, { 'JEKYLL_ENV' => 'production', 'BUNDLE_FROZEN' => 'true' })
        next unless built
        run.call("artifact-#{mode}", ['ruby', 'scripts/verify_site_artifact.rb', dest], { 'VERIFY_MATH_DRAFTS' => mode == 'drafts' ? '1' : nil })
        run.call('distribution-readiness', ['ruby', 'scripts/verify_distribution_readiness.rb', dest]) if mode == 'production'
      end
    else
      record.call('builds', 'NO_CONCLUYENTE', 'Build prerequisites failed')
    end
  end

  sha, sha_status = Open3.capture2e('git', 'rev-parse', 'HEAD', chdir: root)
  raise 'Cannot identify HEAD' unless sha_status.success?
  sha = sha.strip
  if options[:profile] == 'release'
    dirty, status = Open3.capture2e('git', 'status', '--porcelain=v1', '--untracked-files=all', chdir: root)
    record.call('clean-checkout', status.success? && dirty.empty? ? 'PASS' : 'FAIL', dirty.empty? ? 'Clean Git checkout; ignored installed dependencies allowed' : dirty)
    %w[gitlab.com github.com].each do |host|
      output, status = Open3.capture2e('git', 'ls-remote', "https://#{host}/tatanlabra/3cucharadas.git", 'refs/heads/main', chdir: root)
      record.call("remote-#{host}", status.success? && output.split.first == sha ? 'PASS' : 'FAIL', output.strip)
    end
    pipelines = get_json.call("https://gitlab.com/api/v4/projects/57339918/pipelines?sha=#{sha}&ref=main&per_page=20")
    success = pipelines.select { |p| p['sha'] == sha && p['status'] == 'success' }
    jobs = success.flat_map { |p| get_json.call("https://gitlab.com/api/v4/projects/57339918/pipelines/#{p.fetch('id')}/jobs?per_page=100") }
    valid = %w[build_site pages].all? { |name| jobs.any? { |job| job['name'] == name && job['status'] == 'success' } }
    record.call('gitlab-release', valid ? 'PASS' : 'FAIL', success.map { |p| p['web_url'] }.join(', '))
    ['/', '/en/', '/feed.xml', '/feed-julia.xml', '/catastro_sii_brecha/'].each_with_index do |path, index|
      run.call("public-http-#{index}", ['curl', '--fail', '--silent', '--show-error', '--max-time', '25', '--output', File.join(log_dir, "public-#{index}.html"), "https://3cucharadas.cl#{path}"])
    end
    css = File.join(log_dir, 'public-main.css')
    if run.call('public-css-http', ['curl', '--fail', '--silent', '--show-error', '--max-time', '25', '--output', css, 'https://3cucharadas.cl/assets/css/main.css'])
      expected = File.join(File.dirname(report_path), 'site-production/assets/css/main.css')
      equal = File.file?(expected) && Digest::SHA256.file(expected).hexdigest == Digest::SHA256.file(css).hexdigest
      record.call('public-css-parity', equal ? 'PASS' : 'FAIL', Digest::SHA256.file(css).hexdigest)
    end
  end
rescue StandardError => error
  record.call('execution', 'NO_CONCLUYENTE', "#{error.class}: #{error.message}")
end

paths, status = Open3.capture2e('git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard', chdir: root)
digest = Digest::SHA256.new
if status.success?
  paths.split("\0").uniq.sort.each do |path|
    full = File.join(root, path)
    digest << path << "\0"
    digest << (File.symlink?(full) ? File.readlink(full) : File.file?(full) ? File.binread(full) : 'MISSING')
  end
end
verdict = if checks.any? { |c| c[:status] == 'FAIL' }
            'FAIL'
          elsif checks.empty? || checks.any? { |c| c[:status] == 'NO_CONCLUYENTE' }
            'NO_CONCLUYENTE'
          else
            'PASS'
          end
report = { version: 1, timestamp: Time.now.utc.iso8601, profile: options[:profile], sha: sha, source_digest: digest.hexdigest,
           status: verdict, checks: checks, coverage_exceptions: contract && contract['coverage_exceptions'] }
File.write(report_path, JSON.pretty_generate(report) + "\n")
puts "#{verdict}: #{report_path}"
exit({ 'PASS' => 0, 'FAIL' => 1, 'NO_CONCLUYENTE' => 2 }.fetch(verdict))
