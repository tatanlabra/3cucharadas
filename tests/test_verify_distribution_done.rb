# frozen_string_literal: true

require "fileutils"
require "minitest/autorun"
require "open3"
require "tmpdir"
require "yaml"

class VerifyDistributionDoneTest < Minitest::Test
  TODAY = "2026-09-06"

  def setup
    @root = Dir.mktmpdir("distribution-done")
    FileUtils.mkdir_p(File.join(@root, "_posts"))
    FileUtils.mkdir_p(File.join(@root, "_data"))
  end

  def teardown
    FileUtils.remove_entry(@root)
  end

  def write_post(distribution:, lang: "es", date: "2026-08-20")
    front = {
      "title" => "Fixture",
      "ref" => "fixture",
      "date" => date,
      "lang" => lang,
      "permalink" => "/fixture/",
      "distribution" => distribution
    }
    File.write(File.join(@root, "_posts", "#{date}-fixture.md"), "---\n#{front.to_yaml.sub(/\A---\s*\n/, '')}---\nBody\n")
  end

  def write_publications(publications)
    data = [{ "slug" => "fixture", "publicaciones" => publications }]
    File.write(File.join(@root, "_data", "distribucion.yml"), data.to_yaml)
  end

  def run_gate(*arguments)
    script = File.expand_path("../scripts/verify_distribution_done.rb", __dir__)
    Open3.capture3(
      { "DISTRIBUCION_ROOT" => @root, "DISTRIBUCION_HOY" => TODAY },
      "ruby", script, *arguments
    )
  end

  def test_social_requires_bluesky_even_when_mastodon_exists
    write_post(distribution: { "social" => true })
    write_publications([
      { "plataforma" => "mastodon", "url_publicada" => "https://mastodon.example/post/1" }
    ])

    _stdout, stderr, status = run_gate

    refute status.success?
    assert_includes stderr, "bluesky/es"
    refute_includes stderr, "mastodon/es"
  end

  def test_english_social_requires_reply_url_for_each_platform
    write_post(distribution: { "social" => true }, lang: "en")
    write_publications([
      { "plataforma" => "mastodon", "url_publicada" => "https://mastodon.example/post/1" },
      { "plataforma" => "bluesky", "url_publicada" => "https://bsky.example/post/1" }
    ])

    _stdout, stderr, status = run_gate

    refute status.success?
    assert_includes stderr, "mastodon/en"
    assert_includes stderr, "bluesky/en"
  end

  def test_dev_draft_does_not_close_the_channel
    write_post(distribution: { "republish" => ["dev"] }, lang: "en")
    write_publications([
      {
        "plataforma" => "devto",
        "estado" => "borrador",
        "devto_article_id" => 123,
        "url_publicada" => "https://dev.to/example/temp"
      }
    ])

    _stdout, stderr, status = run_gate

    refute status.success?
    assert_includes stderr, "devto/en"
  end

  def test_all_declared_artifacts_close_the_contract
    write_post(distribution: { "social" => true, "republish" => %w[dev medium] }, lang: "en")
    write_publications([
      {
        "plataforma" => "mastodon",
        "url_publicada" => "https://mastodon.example/post/1",
        "url_publicada_en" => "https://mastodon.example/post/2"
      },
      {
        "plataforma" => "bluesky",
        "url_publicada" => "https://bsky.example/post/1",
        "url_publicada_en" => "https://bsky.example/post/2"
      },
      {
        "plataforma" => "devto",
        "estado" => "publicado",
        "devto_article_id" => 123,
        "url_publicada" => "https://dev.to/example/published"
      },
      { "plataforma" => "medium", "url_publicada" => "https://medium.example/published" }
    ])

    stdout, stderr, status = run_gate("--strict")

    assert status.success?, stderr
    assert_includes stdout, "Gate de difusion cumplida OK"
  end

  def test_window_reports_old_debt_without_failing_daily_gate
    write_post(distribution: { "republish" => ["medium"] }, lang: "en", date: "2026-03-01")
    write_publications([])

    _stdout, stderr, status = run_gate("--ventana", "30")

    assert status.success?, stderr
    assert_includes stderr, "atraso historico"
    assert_includes stderr, "medium/en"

    _stdout, _stderr, full_status = run_gate
    refute full_status.success?
  end

  def test_linkedin_and_x_are_individual_required_channels
    write_post(distribution: { "channels" => %w[linkedin x] })
    write_publications([{ "plataforma" => "linkedin", "url_publicada" => "https://www.linkedin.com/feed/update/example" }])
    _stdout, stderr, status = run_gate
    refute status.success?
    assert_includes stderr, "x/es"
    refute_includes stderr, "linkedin/es"
  end

  def test_scheduled_x_is_pending_until_it_has_a_public_url
    write_post(distribution: { "channels" => ["x"] })
    write_publications([{ "plataforma" => "x", "estado" => "programado", "scheduled_at" => "2026-09-07" }])
    _stdout, stderr, status = run_gate
    refute status.success?
    assert_includes stderr, "x/es"
  end

  def test_explicit_channels_close_only_with_each_language_url
    write_post(distribution: { "channels" => %w[linkedin x] }, lang: "en")
    write_publications(%w[linkedin x].map { |p| { "plataforma" => p, "url_publicada_en" => "https://example.org/#{p}/en" } })
    stdout, stderr, status = run_gate("--strict")
    assert status.success?, stderr
    assert_includes stdout, "Gate de difusion cumplida OK"
  end

  def test_unknown_explicit_channel_is_not_silently_ignored
    write_post(distribution: { "channels" => %w[linkedin typo], "skip_reason" => "cannot hide an unknown channel" })
    _stdout, stderr, status = run_gate
    refute status.success?
    assert_includes stderr, "canal desconocido"
  end

  def test_social_opt_out_needs_reason_even_with_linkedin_and_x
    write_post(distribution: { "social" => false, "channels" => %w[linkedin x] })
    _out, err, status = run_gate("--policy-only")
    refute status.success?
    assert_includes err, "skip_reason"
  end

  def test_policy_only_does_not_claim_publication_or_ignore_bad_policy
    write_post(distribution: { "social" => true })
    out, err, status = run_gate("--policy-only")
    assert status.success?, err
    assert_includes out, "Política de difusión OK"
    refute_includes out, "difusion cumplida OK"
    _out, _err, status = run_gate("--strict", "--ref", "fixture", "--social-only")
    refute status.success?
  end

  def test_ref_scope_cannot_pass_without_matching_posts
    write_post(distribution: { "social" => true })
    _out, err, status = run_gate("--ref", "does-not-exist")
    refute status.success?
    assert_includes err, "ningún post"
  end

  def test_social_scope_keeps_other_channels_out_of_its_closeout
    write_post(distribution: { "social" => true, "channels" => ["x"] })
    write_publications(%w[mastodon bluesky].map { |p| { "plataforma" => p, "url_publicada" => "https://example.org/#{p}" } })
    _out, err, status = run_gate("--ref", "fixture", "--social-only", "--strict")
    assert status.success?, err
    _out, _err, status = run_gate("--ref", "fixture", "--strict")
    refute status.success?
  end
end
