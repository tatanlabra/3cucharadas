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
end
