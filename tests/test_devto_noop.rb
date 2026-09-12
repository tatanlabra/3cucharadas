# frozen_string_literal: true
require 'minitest/autorun'
require 'tmpdir'
require 'fileutils'
require 'open3'
require 'json'

class DevtoNoopTest < Minitest::Test
  def run_fixture(mode)
    Dir.mktmpdir('devto-noop-') do |root|
      %w[scripts/lib _posts _data].each { |dir| FileUtils.mkdir_p(File.join(root, dir)) }
      %w[scripts/syndicate_devto.rb scripts/jekyll_to_devto.rb scripts/lib/devto_draft_policy.rb scripts/lib/ai_disclosure.rb].each do |path|
        FileUtils.cp(File.expand_path("../#{path}", __dir__), File.join(root, path))
      end
      File.write(File.join(root, '_posts/example-en.md'), "---\ntitle: Example\npermalink: /example/\ndistribution:\n  republish: [dev]\n---\nExisting public text.\n")
      File.write(File.join(root, '_data/distribucion.yml'), "[]\n")
      stub = File.join(root, 'http_stub.rb')
      File.write(stub, <<~'RUBY')
        require 'net/http'
        require 'json'
        Net::HTTP.prepend(Module.new do
          def request(request)
            abort 'WRITE FORBIDDEN IN NO-OP TEST' unless request.is_a?(Net::HTTP::Get)
            abort 'unexpected API path' unless request.path.start_with?('/api/articles/me/')
            article = {'id'=>42, 'canonical_url'=>'https://3cucharadas.cl/en/example/', 'title'=>'Example', 'body_markdown'=>'Existing public text.'}
            body = request.path.include?('/published?') ? [article] : []
            body = [] if ENV['FIXTURE_MODE'] == 'empty'
            body << article.merge('id'=>43) if ENV['FIXTURE_MODE'] == 'duplicate' && !body.empty?
            code = ENV['FIXTURE_MODE'] == 'rate-limit' ? '429' : '200'
            Struct.new(:code, :body).new(code, JSON.generate(body))
          end
        end)
      RUBY
      env = {'DEV_TO_API_KEY'=>'fixture-not-a-secret', 'RUBYOPT'=>"-r#{stub}", 'FIXTURE_MODE'=>mode,
             'DEVTO_BACKUP_DIR'=>File.join(root, 'custody'), 'DEVTO_DRY_RUN'=>nil, 'DEVTO_INVENTORY_ONLY'=>nil}
      results = 2.times.map { Open3.capture2e(env, 'ruby', 'scripts/syndicate_devto.rb', '--existing-drafts-only', chdir:root) }
      assert_equal "[]\n", File.read(File.join(root, '_data/distribucion.yml'))
      refute File.exist?(File.join(root, 'custody')), 'A verified no-op must not create misleading draft custody'
      yield results
    end
  end

  def test_all_published_is_a_verified_repeatable_noop
    run_fixture('published') do |results|
      results.each do |output, status|
        assert status.success?, output
        assert_includes output, 'NO_OP: 1 canonical(es) verificados publicados; 0 borradores, 0 escrituras'
      end
    end
  end

  def test_empty_duplicate_and_rate_limited_inventory_cannot_pass
    %w[empty duplicate rate-limit].each do |mode|
      run_fixture(mode) do |results|
        results.each do |output, status|
          refute status.success?, "#{mode}: #{output}"
          refute_includes output, 'NO_OP:'
        end
      end
    end
  end
end
