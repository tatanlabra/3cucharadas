# frozen_string_literal: true

require 'minitest/autorun'
require 'tmpdir'
require 'fileutils'
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
end
