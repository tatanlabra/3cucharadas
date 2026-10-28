# frozen_string_literal: true

require "minitest/autorun"
require "open3"

class VerifyThesisPost3Test < Minitest::Test
  ROOT = File.expand_path("..", __dir__)
  SCRIPT = File.join(ROOT, "scripts/verify_thesis_post3.rb")
  NEGATIVE_FIXTURES = {
    "causal-promotion" => "promoción causal no autorizada",
    "en-causal-promotion" => "promoción causal no autorizada en",
    "null-promotion" => "promoción causal no autorizada es",
    "privacy-path" => "ruta privada prohibida",
    "school-identifier" => "identificador público prohibido",
    "state-drift" => "estado científico v3.1 ausente o duplicado",
    "readiness-marker-drift" => "estado de publicación ausente o duplicado",
    "readiness-marker-duplicate" => "marcador científico o editorial contradictorio",
    "scientific-state-duplicate" => "marcador científico o editorial contradictorio",
    "primary-number-drift" => "estimación principal v3.1 faltante",
    "missingness-drift" => "cotas de datos faltantes ausentes",
    "missingness-unpaired" => "cada mención de progresión debe conservar sus dos cotas",
    "bounds-drop" => "cotas de datos faltantes ausentes",
    "bounds-unpaired-extra" => "cada mención de progresión debe conservar sus dos cotas",
    "bounds-unpaired-no-sign" => "cada mención de progresión debe conservar sus dos cotas",
    "bounds-unpaired-rounded" => "cada mención de progresión debe conservar sus dos cotas",
    "secondary-label-drop" => "etiqueta exploratoria secundaria ausente",
    "figure-path-drift" => "figura canónica no referenciada",
    "figure-contract-drift" => "contrato visual de figura incompleto",
    "reference-drift" => "referencias bilingües divergentes",
    "pilot-number" => "cifra piloto obsoleta",
    "hmg-number-drift" => "cápsula HMG sin efecto o muestra publicados",
    "he-blocker-reintroduced" => "bloqueo de educación superior reintroducido",
    "he-blocker-paraphrase" => "bloqueo de educación superior reintroducido",
    "he-effect-outside-agenda" => "efecto postsecundario no autorizado",
    "he-effect-invented" => "agenda de educación superior contiene una cifra estimada",
    "he-agenda-duplicate" => "agenda de educación superior ausente o duplicada",
    "front-matter-causal-promotion" => "promoción causal no autorizada",
    "front-matter-tags-causal-promotion" => "promoción causal no autorizada",
    "strong-policy-promotion" => "promoción causal no autorizada",
    "table-number-parity-drift" => "cifras de tablas bilingües divergentes",
    "figure-number-parity-drift" => "cifras de figuras bilingües divergentes",
    "comparability-coverage-drift" => "comparabilidad observada divergente",
    "progression-definition-narrowing" => "definición pública de progresión incompleta",
    "comparability-age-coverage" => "alcance de cobertura comparativa impreciso",
    "safeguards-causal-promotion" => "resguardos prudenciales promovidos a efecto",
    "effective-clusters-drift" => "clusters efectivos ausentes",
    "iv-promotion" => "rechazo editorial de IV ausente",
    "series-regime-drift" => "evidencia RCID v1 o serie 2005-2024 ausente"
  }.freeze

  def run_gate(fixture = nil)
    env = fixture ? { "POST3_NEGATIVE_FIXTURE" => fixture } : {}
    Open3.capture2e(env, "ruby", SCRIPT, chdir: ROOT)
  end

  def test_current_bilingual_posts_pass
    output, status = run_gate
    assert status.success?, output
    assert_includes output, "POST3_VALID"
    assert_includes output, "upstream_custody=UNCOMMITTED_FILE_HASHES"
  end

  def test_each_negative_fixture_reaches_its_specific_red
    NEGATIVE_FIXTURES.each do |fixture, reason|
      output, status = run_gate(fixture)
      refute status.success?, "#{fixture} should fail:\n#{output}"
      assert_includes output, "POST3_INVALID", fixture
      assert_includes output, reason, "#{fixture} failed for the wrong reason:\n#{output}"
      refute_includes output, "fixture no pudo aplicarse", fixture
    end
  end
end
