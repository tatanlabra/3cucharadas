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
    "reference-drift" => "referencia contradictoria en: callaway2021",
    "pilot-number" => "cifra piloto obsoleta",
    "hmg-capsule-reintroduced" => "contenido retirado reintroducido es",
    "hmg-effect-reintroduced" => "contenido retirado reintroducido en: efecto HMG table_7",
    "update-note-reintroduced" => "contenido retirado reintroducido en",
    "transparency-capsule-drop" => "transparencia sin cita o PDF de 2014 es",
    "he-blocker-reintroduced" => "bloqueo de educación superior reintroducido",
    "he-blocker-paraphrase" => "bloqueo de educación superior reintroducido",
    "he-effect-outside-agenda" => "efecto postsecundario no autorizado",
    "he-effect-invented" => "efecto postsecundario no autorizado es",
    "he-scope-drop" => "límite de alcance postsecundario ausente es",
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
    "series-regime-drift" => "evidencia RCID v1 o serie 2005-2024 ausente",
    "random-effects-drift" => "agregado de efectos aleatorios ausente",
    "fixed-effect-reintroduced" => "agregado de efecto fijo reintroducido",
    "appendix-removed" => "anexo metodológico ausente es",
    "annex-table-contract-drop" => "contrato explícito de tablas ausente en anexo es",
    "appendix-overflow" => "apéndice metodológico fuera de extensión",
    "eli5-label-annex" => "rótulo ELI5 o En simple expuesto es",
    "orphan-details-close" => "etiquetas details desbalanceadas es en anexo",
    "colon-citation-missing-definition" => "cita sin nota es: guard_colon_missing",
    "footnote-orphan" => "nota sin cita en el texto es: manski2003",
    "footnote-missing-definition" => "cita sin nota en: brummet2015",
    "footnote-parity-drift" => "notas bilingües divergentes",
    "math-katex-percent-comment" => "porcentaje sin escapar en bloque matemático KaTeX es",
    "math-comma-number" => "número con coma en bloque matemático KaTeX es"
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

  def test_bilingual_fixture_cannot_claim_red_in_spanish_only_mode
    output, status = Open3.capture2e("ruby", SCRIPT, "--lang", "es", "--fixture", "table-number-parity-drift", chdir: ROOT)
    assert_equal 2, status.exitstatus, output
    assert_includes output, "POST3_USAGE_ERROR: fixture requiere comparación bilingüe"
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
