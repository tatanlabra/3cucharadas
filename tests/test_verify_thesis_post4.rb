# frozen_string_literal: true

require "minitest/autorun"
require "open3"

class VerifyThesisPost4Test < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  SCRIPT = File.join(ROOT, "scripts/verify_thesis_post4.rb")
  NEGATIVES = {
    "annex-removed" => "anexo metodológico ausente es",
    "annex-table-contract-drop" => "contrato explícito de tablas ausente en anexo es",
    "primary-number-drift" => "cifras gobernadas ausentes es: −2,09",
    "footnote-orphan" => "nota sin cita en el texto es: manski2003",
    "net-access-promotion" => "promoción causal ingenua o violación normativa es",
    "inline-code-article" => "uso de código inline (`...`) en prosa/tablas contamina el tema claro es",
    "inline-code-unscoped-annex" => "uso de código inline (`...`) en prosa/tablas contamina el tema claro es",
    "inline-code-fake-json-key" => "uso de código inline (`...`) en prosa/tablas contamina el tema claro es",
    "eli5-label-annex" => "rótulo ELI5 o En simple expuesto es",
    "orphan-details-close" => "etiquetas details desbalanceadas es en anexo",
    "colon-citation-missing-definition" => "cita sin nota es: guard_colon_missing"
  }.freeze

  def run_gate(*arguments)
    Open3.capture2e("ruby", SCRIPT, *arguments, chdir: ROOT)
  end

  def test_spanish_post_and_annex_pass_before_english_adaptation
    output, status = run_gate("--lang", "es")
    assert_equal 0, status.exitstatus, output
    assert_includes output, "THESIS_POST4_VERIFIED lang=es fixture=none"
  end

  def test_bilingual_fixture_cannot_claim_red_in_spanish_only_mode
    output, status = run_gate("--lang", "es", "--fixture", "table-parity-drift")
    assert_equal 2, status.exitstatus, output
    assert_includes output, "THESIS_POST4_USAGE_ERROR: fixture requiere comparación bilingüe"
  end

  def test_each_negative_exercises_its_named_guard
    NEGATIVES.each do |fixture, reason|
      output, status = run_gate("--lang", "es", "--fixture", fixture)
      assert_equal 1, status.exitstatus, "#{fixture}: #{output}"
      assert_includes output, "THESIS_POST4_INVALID: #{reason}", fixture
      refute_includes output, "fixture no pudo aplicarse", fixture
    end
  end
end
