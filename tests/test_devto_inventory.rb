# frozen_string_literal: true
require 'minitest/autorun'
require 'tmpdir'
require 'fileutils'
require 'open3'
require 'json'

class DevtoInventoryTest < Minitest::Test
  ROOT = File.expand_path('..', __dir__)
  def fixture
    Dir.mktmpdir('devto-inventory-test-') do |dir|
      %w[scripts/lib _posts _data].each { |path| FileUtils.mkdir_p(File.join(dir, path)) }
      %w[scripts/syndicate_devto.rb scripts/jekyll_to_devto.rb scripts/lib/devto_draft_policy.rb].each do |path|
        FileUtils.cp(File.join(ROOT, path), File.join(dir, path))
      end
      File.write(File.join(dir, '_posts/2026-09-06-example-en.md'), "---\ntitle: Example\npermalink: /example/\ndistribution:\n  republish: [dev]\n---\nPublic example.\n")
      File.write(File.join(dir, '_data/distribucion.yml'), "[]\n")
      File.write(File.join(dir, 'fake.rb'), <<~'RUBY')
        require 'net/http'
        require 'json'
        class FakeHTTP
          attr_accessor :use_ssl, :open_timeout, :read_timeout
          def request(request)
            File.open(ENV.fetch('REQUEST_LOG'), 'a') { |f| f.puts(request.method) }
            abort 'FORBIDDEN WRITE' unless request.method == 'GET'
            unpublished = request.path.include?('/unpublished?')
            article = { 'id' => unpublished ? 42 : 41, 'canonical_url' => 'https://3cucharadas.cl/en/example/', 'title' => 'PRIVATE-TITLE', 'body_markdown' => 'PRIVATE-BODY' }
            Struct.new(:code, :body).new(ENV.fetch('FAKE_HTTP_CODE', '200'), [article].to_json)
          end
        end
        Net::HTTP.define_singleton_method(:new) { |*| FakeHTTP.new }
      RUBY
      yield dir
    end
  end

  def invoke(dir, extra = [], env = {})
    Open3.capture3({ 'DEV_TO_API_KEY' => 'TEST-SECRET', 'REQUEST_LOG' => File.join(dir, 'requests'), 'DEVTO_DRY_RUN' => nil, 'DEVTO_INVENTORY_ONLY' => nil }.merge(env),
                  'ruby', '-r', File.join(dir, 'fake.rb'), File.join(dir, 'scripts/syndicate_devto.rb'), '--inventory-only', *extra)
  end

  def test_real_cli_only_gets_and_does_not_disclose_or_write
    fixture do |dir|
      stdout, stderr, status = invoke(dir)
      assert status.success?, stderr
      report = JSON.parse(stdout)
      assert_equal 0, report.fetch('writes')
      assert_equal [{ 'id' => 41, 'published' => true }, { 'id' => 42, 'published' => false }], report.fetch('inventory').first.fetch('articles')
      %w[PRIVATE-TITLE PRIVATE-BODY TEST-SECRET].each { |secret| refute_includes stdout + stderr, secret }
      assert_equal %w[GET GET], File.readlines(File.join(dir, 'requests'), chomp: true)
      assert_equal "[]\n", File.read(File.join(dir, '_data/distribucion.yml'))
    end
  end

  def test_conflicting_modes_and_missing_key_stop_before_network
    fixture do |dir|
      assert_equal 2, invoke(dir, ['--dry-run']).last.exitstatus
      assert_equal 2, invoke(dir, [], { 'DEV_TO_API_KEY' => nil }).last.exitstatus
      refute File.exist?(File.join(dir, 'requests'))
    end
  end

  def test_http_failure_is_not_a_successful_inventory
    fixture do |dir|
      assert_equal 1, invoke(dir, [], { 'FAKE_HTTP_CODE' => '429' }).last.exitstatus
      assert_equal ['GET'], File.readlines(File.join(dir, 'requests'), chomp: true)
      assert invoke(dir).last.success?
    end
  end
end
