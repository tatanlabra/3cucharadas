# frozen_string_literal: true

require 'minitest/autorun'
require 'tmpdir'
require 'fileutils'
require 'digest'
require 'json'
require 'open3'
require 'yaml'
require 'rbconfig'

# Exercise the real CLI in a disposable source tree; no live posts or assets change.
class VerifyVisualAssetsMobileTest < Minitest::Test
  def setup
    @root = Dir.mktmpdir('visual-mobile-')
    %w[scripts/lib _posts _data/visuales assets].each { |dir| FileUtils.mkdir_p(File.join(@root, dir)) }
    %w[verify_visual_assets.rb verify_hero_disclosure.rb lib/ai_disclosure.rb lib/image_dimensions.rb].each do |path|
      FileUtils.cp(File.expand_path("../scripts/#{path}", __dir__), File.join(@root, 'scripts', path))
    end
    File.write(File.join(@root, '_config.yml'), { 'exclude' => [] }.to_yaml)
    @asset = 'assets/mobile.svg'
    @post = '_posts/2026-09-12-fixture.md'
    @piece = { 'id' => 'mobile', 'archivo' => @asset, 'estado' => 'publicable', 'rol' => 'teaser', 'origen' => 'datos' }
    File.write(File.join(@root, @asset), '<svg xmlns="http://www.w3.org/2000/svg"/>')
    File.write(File.join(@root, @post), { 'header' => { 'teaser_mobile' => "/#{@asset}" } }.to_yaml + "---\nFixture.\n")
    catalog([@piece])
  end

  def teardown
    FileUtils.remove_entry(@root)
  end

  def catalog(pieces)
    File.write(File.join(@root, '_data/visuales/fixture.yml'), { 'posts' => [@post], 'piezas' => pieces }.to_yaml)
  end

  def run_gate
    output, status = Open3.capture2e(RbConfig.ruby, File.join(@root, 'scripts/verify_visual_assets.rb'), '--strict')
    [output, status.success?]
  end

  def write_embedded_manifest(dir, entries)
    File.write(File.join(dir, 'manifest.json'), JSON.pretty_generate({ 'files' => entries }))
  end

  def manifest_entry(path)
    absolute = File.join(@root, 'assets/images/generated', path)
    {
      'path' => path,
      'bytes' => File.size(absolute),
      'sha256' => Digest::SHA256.file(absolute).hexdigest
    }
  end

  def scientific_package_fixture(slug)
    root = File.join(@root, 'assets/images', slug)
    FileUtils.mkdir_p(root)
    legacy = File.join(root, 'legacy.svg')
    File.write(legacy, '<svg>legacy</svg>')
    write_embedded_manifest(root, [{ 'path' => 'legacy.svg', 'bytes' => File.size(legacy),
      'sha256' => Digest::SHA256.file(legacy).hexdigest }])
    package_paths = slug == 'tesis-post3' ? %w[
      scientific-reset/manifest.json scientific-reset/anticipation/manifest.json
      scientific-reset/sensitivity/manifest.json
    ] : %w[scientific-reset/manifest.json scientific-reset/sensitivity/manifest.json]
    package_paths.each do |relative|
      dir = File.dirname(File.join(root, relative))
      FileUtils.mkdir_p(dir)
      figure = File.join(dir, 'figure.svg')
      File.write(figure, "<svg>#{relative}</svg>")
      File.write(File.join(root, relative), JSON.pretty_generate({ 'files' => [
        { 'name' => 'figure.svg', 'sha256' => Digest::SHA256.file(figure).hexdigest }
      ] }))
    end
    root
  end

  def test_publicable_mobile_passes
    output, success = run_gate
    assert success, output
    assert_includes output, '1 activo(s) referenciados'
  end

  def test_missing_mobile_without_catalog_fails_and_restoring_recovers
    File.unlink(File.join(@root, '_data/visuales/fixture.yml'))
    File.unlink(File.join(@root, @asset))
    output, success = run_gate
    refute success, output
    assert_includes output, "V9 #{@post}: referencia a #{@asset}"
    File.write(File.join(@root, @asset), '<svg/>')
    output, success = run_gate
    assert success, output
  end

  def test_existing_mobile_omitted_from_manifest_fails_then_recovers
    catalog([])
    output, success = run_gate
    refute success, output
    assert_includes output, 'V10'
    assert_includes output, 'header.teaser_mobile'
    catalog([@piece])
    output, success = run_gate
    assert success, output
  end

  def test_existing_mobile_marked_for_diffusion_fails
    catalog([@piece.merge('estado' => 'solo-difusion')])
    File.write(File.join(@root, '_config.yml'), { 'exclude' => [@asset] }.to_yaml)
    output, success = run_gate
    refute success, output
    assert_includes output, 'V6'
    assert_includes output, 'V10'
  end

  def test_complete_embedded_manifest_satisfies_v13
    dir = File.join(@root, 'assets/images/generated')
    FileUtils.mkdir_p(dir)
    File.write(File.join(dir, 'figure.svg'), '<svg xmlns="http://www.w3.org/2000/svg"/>')
    write_embedded_manifest(dir, [manifest_entry('figure.svg')])

    output, success = run_gate

    assert success, output
    refute_includes output, 'V13'
  end

  def test_embedded_manifest_with_stale_hash_fails_then_recovers
    dir = File.join(@root, 'assets/images/generated')
    FileUtils.mkdir_p(dir)
    File.write(File.join(dir, 'figure.svg'), '<svg xmlns="http://www.w3.org/2000/svg"/>')
    write_embedded_manifest(dir, [manifest_entry('figure.svg')])
    File.write(File.join(dir, 'figure.svg'), '<svg xmlns="http://www.w3.org/2000/svg"><title>mutated</title></svg>')

    output, success = run_gate
    refute success, output
    assert_includes output, 'V13 assets/images/generated/manifest.json[figure.svg]: sha256'

    write_embedded_manifest(dir, [manifest_entry('figure.svg')])
    output, success = run_gate
    assert success, output
  end

  def test_embedded_manifest_that_omits_existing_file_fails
    dir = File.join(@root, 'assets/images/generated')
    FileUtils.mkdir_p(dir)
    File.write(File.join(dir, 'figure.svg'), '<svg xmlns="http://www.w3.org/2000/svg"/>')
    File.write(File.join(dir, 'orphan.svg'), '<svg xmlns="http://www.w3.org/2000/svg"/>')
    write_embedded_manifest(dir, [manifest_entry('figure.svg')])

    output, success = run_gate

    refute success, output
    assert_includes output, 'V13 assets/images/generated/manifest.json: archivos no declarados: orphan.svg'
  end

  def test_scientific_subpackages_are_exact_and_do_not_change_legacy_manifest
    post3 = scientific_package_fixture('tesis-post3')
    scientific_package_fixture('tesis-post4')
    legacy_sha = Digest::SHA256.file(File.join(post3, 'manifest.json')).hexdigest
    output, success = run_gate
    assert success, output

    orphan = File.join(post3, 'scientific-reset/sensitivity/orphan.svg')
    File.write(orphan, '<svg>new unlisted file</svg>')
    output, success = run_gate
    refute success, output
    assert_includes output, 'archivos no declarados: scientific-reset/sensitivity/orphan.svg'
    File.unlink(orphan)

    hidden = File.join(post3, 'scientific-reset/sensitivity/.hidden.svg')
    File.write(hidden, '<svg>unlisted hidden file</svg>')
    output, success = run_gate
    refute success, output
    assert_includes output, 'archivos no declarados: scientific-reset/sensitivity/.hidden.svg'
    File.unlink(hidden)

    figure = File.join(post3, 'scientific-reset/sensitivity/figure.svg')
    original = File.read(figure)
    File.write(figure, '<svg>changed</svg>')
    output, success = run_gate
    refute success, output
    assert_includes output, 'scientific-reset/sensitivity/manifest.json[figure.svg]: sha256'
    File.write(figure, original)

    manifest = File.join(post3, 'scientific-reset/anticipation/manifest.json')
    manifest_bytes = File.read(manifest)
    File.unlink(manifest)
    output, success = run_gate
    refute success, output
    assert_includes output, 'manifest obligatorio ausente'
    File.write(manifest, manifest_bytes)

    File.unlink(figure)
    File.symlink(File.join(@root, @asset), figure)
    output, success = run_gate
    refute success, output
    assert_includes output, 'enlace simbólico'
    File.unlink(figure)
    File.write(figure, original)

    parent_manifest = File.join(post3, 'manifest.json')
    parent_bytes = File.read(parent_manifest)
    duplicate = JSON.parse(parent_bytes)
    duplicate['files'] << { 'path' => 'scientific-reset/sensitivity/figure.svg',
      'bytes' => File.size(figure), 'sha256' => Digest::SHA256.file(figure).hexdigest }
    File.write(parent_manifest, JSON.pretty_generate(duplicate))
    output, success = run_gate
    refute success, output
    assert_includes output, 'rutas reclamadas por más de un manifest'
    File.write(parent_manifest, parent_bytes)

    output, success = run_gate
    assert success, output
    assert_equal legacy_sha, Digest::SHA256.file(File.join(post3, 'manifest.json')).hexdigest
  end
end
