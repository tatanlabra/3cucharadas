require 'minitest/autorun'
require 'tmpdir'
require 'fileutils'
require 'open3'
require 'yaml'

class PolyglotDoctorTest < Minitest::Test
  ROOT = File.expand_path('..', __dir__)

  def doctor(compatibility: true, conflict: false)
    Dir.mktmpdir('polyglot-doctor-') do |dir|
      FileUtils.mkdir_p(File.join(dir, '_plugins'))
      FileUtils.cp(File.join(ROOT, '_plugins/polyglot_doctor.rb'), File.join(dir, '_plugins')) if compatibility
      File.write(File.join(dir, 'index.md'), "---\nlang: es\n---\n# Prueba ágil\n")
      if conflict
        # Polyglot intentionally deduplicates pages sharing a URL. A static file
        # colliding with a rendered page survives coordination and must fail.
        File.write(File.join(dir, 'index.html'), 'conflicting static output')
      end
      config = { 'source' => dir, 'destination' => File.join(dir, '_site'), 'plugins_dir' => File.join(dir, '_plugins'),
                 'url' => 'https://3cucharadas.cl', 'languages' => %w[es en], 'default_lang' => 'es', 'parallel_localization' => false }
      path = File.join(dir, '_config.yml')
      File.write(path, YAML.dump(config))
      Open3.capture2e({ 'BUNDLE_GEMFILE' => File.join(ROOT, 'Gemfile') }, 'bundle', 'exec', 'jekyll', 'doctor', '--config', path, chdir: ROOT)
    end
  end

  def test_original_failure
    out, status = doctor(compatibility: false)
    refute status.success?, out
    assert_match(/nil into Array/, out)
  end

  def test_prepared_languages_pass
    out, status = doctor
    assert status.success?, out
    assert_match(/Everything looks fine/, out)
  end

  def test_real_conflict_still_fails
    out, status = doctor(conflict: true)
    refute status.success?, out
    assert_match(/Conflict/, out)
    refute_match(/nil into Array/, out)
  end

  def test_missing_stringex_is_rejected_then_accented_anchors_recover
    program = <<~'RUBY'
      require 'yaml'
      if ENV['SIMULATE_MISSING_STRINGEX'] == '1'
        Kernel.prepend(Module.new do
          def gem(name, *args)
            raise Gem::LoadError, 'stringex unavailable in fixture bundle' if name == 'stringex'
            super
          end
        end)
      end
      require 'kramdown'
      # The Kramdown converter uses stringex; GFM's default ID generation
      # deliberately retains Unicode and bypasses this transliteration path.
      puts Kramdown::Document.new("# Prueba ágil\n\n## Niño y acción\n", input: 'Kramdown', auto_ids: true, transliterated_header_ids: true).to_html
    RUBY
    run = ->(missing) { Open3.capture2e({ 'BUNDLE_GEMFILE' => File.join(ROOT, 'Gemfile'), 'SIMULATE_MISSING_STRINGEX' => missing }, 'bundle', 'exec', 'ruby', '-e', program, chdir: ROOT) }
    rejected, status = run.call('1')
    refute status.success?, rejected
    assert_match(/stringex unavailable/, rejected)
    recovered, status = run.call('0')
    assert status.success?, recovered
    assert_includes recovered, 'id="prueba-agil"'
    assert_includes recovered, 'id="nino-y-accion"'
  end

  def build_anchors(compatibility:)
    Dir.mktmpdir('polyglot-anchor-parity-') do |dir|
      FileUtils.mkdir_p(File.join(dir, '_plugins'))
      FileUtils.cp(File.join(ROOT, '_plugins/polyglot_doctor.rb'), File.join(dir, '_plugins')) if compatibility
      File.write(File.join(dir, 'index.md'), "---\nlang: es\n---\n# Prueba ágil\n\n## Niño y acción\n")
      config = { 'source' => dir, 'destination' => File.join(dir, '_site'), 'plugins_dir' => File.join(dir, '_plugins'),
                 'url' => 'https://3cucharadas.cl', 'languages' => %w[es en], 'default_lang' => 'es', 'parallel_localization' => false,
                 'kramdown' => { 'input' => 'GFM', 'auto_ids' => true, 'transliterated_header_ids' => true } }
      path = File.join(dir, '_config.yml')
      File.write(path, YAML.dump(config))
      output, status = Open3.capture2e({ 'BUNDLE_GEMFILE' => File.join(ROOT, 'Gemfile') }, 'bundle', 'exec', 'jekyll', 'build', '--config', path, chdir: ROOT)
      assert status.success?, output
      %w[index.html en/index.html].to_h do |relative|
        html = File.read(File.join(dir, '_site', relative))
        # Freeze actual production GFM anchors, not hypothetical ASCII IDs.
        assert_includes html, 'id="prueba-ágil"'
        assert_includes html, 'id="niño-y-acción"'
        [relative, html]
      end
    end
  end

  def test_doctor_hook_preserves_both_rendered_languages_and_anchors
    baseline = build_anchors(compatibility: false)
    candidate = build_anchors(compatibility: true)
    assert_equal baseline, candidate
  end
end
