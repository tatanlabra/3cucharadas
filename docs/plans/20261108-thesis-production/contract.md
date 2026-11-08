# Producción III–IV

Autorización humana: dejar todo en productivo, hacer push y verificar con Playwright gráficos, visualizaciones y colores; difusión pendiente.

PLAN_STATE v2: pb-20261108T003705315Z-fc127547. Contrato editorial anterior cerrado localmente; esta fase agrega publicación y medición pública.
HANDOFF-TRACE: usuario → Codex integrador → implement_site / figures_pdf / editorial_critica vía collaboration.

Revisión 2 abierta por corrección humana: párrafos justificados, figura 1 amplia y sin cruces, guardas geométricas en generador y Playwright, y revisión adversarial Claude antes de publicar. Los recibos de revisión 1 son históricos y no aprueban esta revisión. La ejecución integral anterior fue interrumpida (exit 130). Las fases ejecutables P2 y P3 reúnen publicación/CI y calidad pública del tablero P2–P4.

## Fases y aceptación

| Fase | Resultado exigido | Evidencia discriminante | Rollback |
|---|---|---|---|
| P0 | Custodia, hooks y destinos comprobados | HEAD y ambos remotos iguales antes de publicar; cambios selectivos; cero envíos sociales | Conservar árbol local y no empujar |
| P1 | Build, gates fuente y Playwright local | 8 rutas ES/EN; temas claro/oscuro; móvil/escritorio; contraste, clipping, carga y tamaño efectivos; detector falsado | Corregir archivos afectados y repetir |
| P2 | Commit y push explícito a ambos destinos | SHA remoto igual a SHA entregado, hooks sin bypass | Commit correctivo; nunca force push |
| P3 | CI y Pages con bytes actuales | Pipeline y pages exitosos; rutas y activos públicos coincidentes | Corregir o revertir entrega con nuevo commit |
| P4 | Calidad visual pública y cierre | Playwright público con capturas, cifras de contraste/tamaño, ausencia de roturas; inventario de limitaciones | Mantener abierto ante cualquier fallo material |

## Rúbrica

HIGH END se evalúa como calidad editorial medida: jerarquía legible, gráficos y tablas sin recortes, paleta consistente entre temas, texto contrastado, variantes responsivas correctas y navegación accesible. No se afirmará perfección global. La matriz y límites numéricos quedan en el reporte visual reproducible; cada incumplimiento requiere corrección o justificación explícita sin convertirlo en aprobado.

## Invariantes

- Preservar datos, intervalos, límites inferenciales, títulos, fechas, refs y permalinks.
- Publicación del sitio autorizada. Difusión y sindicación externa pendientes.
- GitLab sirve producción; GitHub conserva espejo y redirector. Push explícito y sin force.
- Custodia PDF local preservada; no inventar enlace público inexistente.
- Advertencia histórica Post III UNCOMMITTED_FILE_HASHES permanece explícita: no demuestra ausencia de custodia de esta entrega ni autoriza modificar freeze científico.

## Derivas

- Claude editorial B1–B8: sincronizar límites ES/EN, recuperar cautelas omitidas, retirar metáforas/etiquetas y corregir referencias a un preregistro independiente o estimadores no implementados. La evidencia del productor RCID identifica controles sin cierres registrados y agregación ponderada por expuestos. Se corrigen prosa, alt y etiquetas de la figura III desde su generador; cifras y CSV intactos.

- Corrección humana posterior: restaurar justificación de párrafos; retirar excepción anterior de alineación natural.
- Figura 1: límite externo de 620 px y geometría interna insuficiente; exigir detección de cruces texto/marcas y texto/texto en generación y navegador.
- Panorama longitudinal 2009–2022 al inicio ES/EN; 2016–2019 queda delimitado como análisis detallado, sin extrapolar sus modelos a toda la serie.
- Nueva revisión Claude del conjunto; preservar revisión previa como histórica.

- Referencias trasladadas: productor y gate incluyen cuatro anexos explícitos; reindexación conserva metadatos bibliográficos cacheados.
- Deriva histórica D6 reemplazada por D7: el gate exige ahora justificación en III–IV; la excepción anterior de alineación natural queda retirada.
- Se corrigió paridad numérica EN según mismo hecho y denominador ES; revisión científica ES permanece vigente.
- Cinco piezas locales de difusión se alinearon a fuentes actuales para no conservar cifras huérfanas; siguen pendientes de revisión y envío humano.

- Push EN dispara DEV.to: agregar exclusión por marcador de commit `3c-release: diffusion-deferred`, limitada a esa entrega.
- Preflight de CI detectó manifiesto IV incompleto: faltaban tres CSV existentes; registrar hashes y tamaños sin tocar bytes.
- Preflight de difusión usa artículo sin anexos: adaptar corpus canónico y conservar visibles las piezas realmente desfasadas; no publicar difusión.

<!-- contract:thesis-production:begin -->
```yaml
plan_contract_version: 1
plan:
  id: thesis-production
  title: III-IV produccion y calidad visual
  source: Autorizacion humana de push y produccion; difusion pendiente
  accepted_at: '2026-11-07'
  revision: 2
task:
  id: thesis-production
  objective: Publicar III-IV y verificar experiencia publica con Playwright
  scope: Blog ES/EN, anexos, visuales, custodia local research, gates y evidencia; sin difusion
parameters:
  board: pb-20261108T003705315Z-fc127547
requirements:
- id: R0
  source: Objetivo humano de produccion
  description: Custodia, invariantes y revision adversarial Claude vigente
- id: R1
  source: Objetivo humano de produccion
  description: Justificacion, amplitud, geometria de las tres familias de figuras, calidad local
    y gates
- id: R2
  source: Objetivo humano de produccion
  description: Remotos y despliegue actual
- id: R3
  source: Objetivo humano de produccion
  description: Playwright publico
invariants:
- id: I0
  source: Usuario
  description: Sin difusion; datos y limites cientificos preservados; push sin force; cambios
    selectivos
phases:
- id: P0
  status: done
  objective: Custodia e invariantes
  depends_on: []
  invariants:
  - I0
  entry_gate: Autorizacion humana y fase anterior verificada
  exit_gate: AC-P0
  rollback: Corregir archivos propios o commit correctivo; nunca force push
  mandatory: true
- id: P1
  status: done
  objective: Calidad local y gates
  depends_on:
  - P0
  invariants:
  - I0
  entry_gate: Autorizacion humana y fase anterior verificada
  exit_gate: AC-P1
  rollback: Corregir archivos propios o commit correctivo; nunca force push
  mandatory: true
- id: P2
  status: pending
  objective: Remotos y despliegue actual
  depends_on:
  - P1
  invariants:
  - I0
  entry_gate: Autorizacion humana y fase anterior verificada
  exit_gate: AC-P2
  rollback: Corregir archivos propios o commit correctivo; nunca force push
  mandatory: true
- id: P3
  status: pending
  objective: Playwright publico
  depends_on:
  - P2
  invariants:
  - I0
  entry_gate: Autorizacion humana y fase anterior verificada
  exit_gate: AC-P3
  rollback: Corregir archivos propios o commit correctivo; nunca force push
  mandatory: true
tasks:
- id: T0
  phase: P0
  requirements:
  - R0
  owner: Codex integrador y pares delimitados
  allowed_paths:
  - activos/3cucharadas/**
  - incubadora/tesis_mae_mejorada/outputs/post4*/*
  - incubadora/tesis_mae_mejorada/scripts/35*.py
  - incubadora/tesis_mae_mejorada/scripts/336_post3_visuals.py
  - incubadora/tesis_mae_mejorada/outputs/post3_visuals/**
  - incubadora/tesis_mae_mejorada/tests/*post4_visual_geometry.py
  - incubadora/tesis_mae_mejorada/tests/test_post4_pdf_composition.py
  deliverable: Custodia e invariantes
  status: done
  acceptance:
  - AC-P0
  mandatory: true
- id: T1
  phase: P1
  requirements:
  - R1
  owner: Codex integrador y pares delimitados
  allowed_paths:
  - activos/3cucharadas/**
  - incubadora/tesis_mae_mejorada/outputs/post4*/*
  - incubadora/tesis_mae_mejorada/scripts/35*.py
  - incubadora/tesis_mae_mejorada/scripts/336_post3_visuals.py
  - incubadora/tesis_mae_mejorada/outputs/post3_visuals/**
  - incubadora/tesis_mae_mejorada/tests/*post4_visual_geometry.py
  - incubadora/tesis_mae_mejorada/tests/test_post4_pdf_composition.py
  deliverable: Calidad local y gates
  status: done
  acceptance:
  - AC-P1
  - AC-GEN
  mandatory: true
- id: T2
  phase: P2
  requirements:
  - R2
  owner: Codex integrador y pares delimitados
  allowed_paths:
  - activos/3cucharadas/**
  - incubadora/tesis_mae_mejorada/outputs/post4*/*
  - incubadora/tesis_mae_mejorada/scripts/35*.py
  - incubadora/tesis_mae_mejorada/scripts/336_post3_visuals.py
  - incubadora/tesis_mae_mejorada/outputs/post3_visuals/**
  - incubadora/tesis_mae_mejorada/tests/*post4_visual_geometry.py
  - incubadora/tesis_mae_mejorada/tests/test_post4_pdf_composition.py
  deliverable: Remotos y despliegue actual
  status: pending
  acceptance:
  - AC-P2
  mandatory: true
- id: T3
  phase: P3
  requirements:
  - R3
  owner: Codex integrador y pares delimitados
  allowed_paths:
  - activos/3cucharadas/**
  - incubadora/tesis_mae_mejorada/outputs/post4*/*
  - incubadora/tesis_mae_mejorada/scripts/35*.py
  - incubadora/tesis_mae_mejorada/scripts/336_post3_visuals.py
  - incubadora/tesis_mae_mejorada/outputs/post3_visuals/**
  - incubadora/tesis_mae_mejorada/tests/*post4_visual_geometry.py
  - incubadora/tesis_mae_mejorada/tests/test_post4_pdf_composition.py
  deliverable: Playwright publico
  status: pending
  acceptance:
  - AC-P3
  mandatory: true
acceptance:
- id: AC-P0
  phase: P0
  task: T0
  description: Custodia e invariantes
  command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py --check
    baseline && python3 scripts/verify_thesis_editorial_delivery.py --check review && python3
    scripts/verify_thesis_editorial_delivery.py --check pdf
  scope: tree
  input_paths: &id001
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias*.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml*.md
  - activos/3cucharadas/_pages/tesis-post*-anexo-metodologico*.md
  - activos/3cucharadas/scripts/verify_thesis*.py
  - activos/3cucharadas/scripts/verify_thesis*.mjs
  - activos/3cucharadas/assets/images/tesis-post*/manifest.json
  - activos/3cucharadas/assets/css/main.scss
  - activos/3cucharadas/scripts/verify_draft_promotion.rb
  - activos/3cucharadas/scripts/verify_thesis_post3.rb
  - incubadora/tesis_mae_mejorada/scripts/336_post3_visuals.py
  - incubadora/tesis_mae_mejorada/scripts/352_post4_visuals.py
  - incubadora/tesis_mae_mejorada/tests/verify_post4_visual_geometry.py
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/baseline.json
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/claude/decision.json
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/pdf-delivery.json
  falsification:
    red_command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py
      --check baseline --fixture identity-drift
    green_command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py
      --check baseline && python3 scripts/verify_thesis_editorial_delivery.py --check review
      && python3 scripts/verify_thesis_editorial_delivery.py --check pdf
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T02:52:56Z'
    fixture_sha256: 09370e38d5caba168dafef9f08dd77f6dee873dd5bac0b0a999b411f1baaf65f
    red_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract-r2/AC-P0-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract-r2/AC-P0-green.json
- id: AC-P1
  phase: P1
  task: T1
  description: Calidad local y gates
  command: cd activos/3cucharadas && ruby scripts/verify_site_health.rb --profile source --report
    /tmp/thesis-production-contract-source.json && ruby scripts/verify_reference_links.rb &&
    node scripts/verify_thesis_visual_quality.mjs --base-url http://127.0.0.1:4005 --report
    /tmp/thesis-production-contract-local.json
  scope: tree
  input_paths: *id001
  falsification:
    red_command: cd activos/3cucharadas && node scripts/verify_thesis_visual_quality.mjs --base-url
      http://127.0.0.1:4005 --fixture svg-value-overlap
    green_command: cd activos/3cucharadas && ruby scripts/verify_site_health.rb --profile source
      --report /tmp/thesis-production-contract-source.json && ruby scripts/verify_reference_links.rb
      && node scripts/verify_thesis_visual_quality.mjs --base-url http://127.0.0.1:4005 --report
      /tmp/thesis-production-contract-local.json
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: activos/3cucharadas/scripts/verify_thesis_visual_quality.mjs
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T02:53:02Z'
    fixture_sha256: c74e8a248776d56bd97e33abcdc0a1292c0ee3c7f3b4a3eee03d72d7200a929c
    red_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract-r2/AC-P1-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract-r2/AC-P1-green.json
- id: AC-P2
  phase: P2
  task: T2
  description: Remotos y despliegue actual
  command: cd activos/3cucharadas && python3 scripts/verify_thesis_production.py --artifact-root
    /tmp/codex-thesis-correction-ci-artifact/public --receipt /tmp/thesis-production-contract-deployed.json
  scope: tree
  input_paths: *id001
  falsification:
    red_command: cd activos/3cucharadas && python3 scripts/verify_thesis_production.py --artifact-root
      /tmp/codex-thesis-production-site --expected-sha 0000000000000000000000000000000000000000
      --receipt /tmp/thesis-production-contract-wrong-sha.json
    green_command: cd activos/3cucharadas && python3 scripts/verify_thesis_production.py --artifact-root
      /tmp/codex-thesis-correction-ci-artifact/public --receipt /tmp/thesis-production-contract-deployed.json
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: activos/3cucharadas/scripts/verify_thesis_production.py
  falsified_by: null
- id: AC-P3
  phase: P3
  task: T3
  description: Playwright publico
  command: cd activos/3cucharadas && node scripts/verify_thesis_visual_quality.mjs --base-url
    https://3cucharadas.cl --report /tmp/thesis-production-contract-visual-public.json
  scope: tree
  input_paths: *id001
  falsification:
    red_command: cd activos/3cucharadas && node scripts/verify_thesis_visual_quality.mjs --base-url
      https://3cucharadas.cl --fixture low-contrast
    green_command: cd activos/3cucharadas && node scripts/verify_thesis_visual_quality.mjs --base-url
      https://3cucharadas.cl --report /tmp/thesis-production-contract-visual-public.json
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: activos/3cucharadas/scripts/verify_thesis_visual_quality.mjs
  falsified_by: null
- id: AC-GEN
  phase: P1
  task: T1
  description: Generador rechaza cruces geometricos en todas las variantes IV
  command: /opt/entornos/mamba312/bin/python incubadora/tesis_mae_mejorada/tests/verify_post4_visual_geometry.py
  scope: tree
  input_paths: *id001
  falsification:
    red_command: /opt/entornos/mamba312/bin/python incubadora/tesis_mae_mejorada/tests/verify_post4_visual_geometry.py
      --inject-selection-overlap
    green_command: /opt/entornos/mamba312/bin/python incubadora/tesis_mae_mejorada/tests/verify_post4_visual_geometry.py
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: incubadora/tesis_mae_mejorada/tests/verify_post4_visual_geometry.py
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T02:52:58Z'
    fixture_sha256: d9d25817e4df00ecc840fa48c237f0cc1d698985838fecbab6e4f999d5b4618d
    red_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract-r2/AC-GEN-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract-r2/AC-GEN-green.json
changes:
- id: CH1
  description: Justificacion, panorama temporal y geometria corregidos; nueva revision Claude
    antes de push
  reason: El usuario detecto parrafos sin justificar y figura1 estrecha con cruces; el verde
    anterior no media solapamientos
  material: true
  approval_refs:
  - user-chat:corregir-integralmente-revision-claude-y-productivo
emergent_tasks: []
completion:
  status: in_progress
  require_all_mandatory_tasks_done: true
  require_all_acceptance_passed: true
  allow_authorized_deferred_exclusions: true
```
<!-- contract:thesis-production:end -->
