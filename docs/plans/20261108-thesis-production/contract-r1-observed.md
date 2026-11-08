> Histórico: observaciones individuales aprobadas; ejecución integral interrumpida por nuevas correcciones humanas. No constituye cierre integral.

# Producción III–IV

Autorización humana: dejar todo en productivo, hacer push y verificar con Playwright gráficos, visualizaciones y colores; difusión pendiente.

PLAN_STATE v2: pb-20261108T003705315Z-fc127547. Contrato editorial anterior cerrado localmente; esta fase agrega publicación y medición pública.
HANDOFF-TRACE: usuario → Codex integrador → implement_site / figures_pdf / editorial_critica vía collaboration.

Las cuatro aceptaciones tienen observaciones rojas y verdes reales, vinculadas a sus entradas. El cierre integral depende además de ejecutar el contrato completo sin filtros. Las fases ejecutables P2 y P3 reúnen, respectivamente, publicación/CI y calidad pública del tablero P2–P4.

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

- Referencias trasladadas: productor y gate incluyen cuatro anexos explícitos; reindexación conserva metadatos bibliográficos cacheados.
- Gate de promoción requería justificación local: reconoce alineación natural solo para refs y clases III–IV, con comprobación del CSS y prueba negativa.
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
  revision: 1
task:
  id: thesis-production
  objective: Publicar III-IV y verificar experiencia publica con Playwright
  scope: Blog ES/EN, anexos, visuales, custodia local research, gates y evidencia;
    sin difusion
parameters:
  board: pb-20261108T003705315Z-fc127547
requirements:
- id: R0
  source: Objetivo humano de produccion
  description: Custodia e invariantes
- id: R1
  source: Objetivo humano de produccion
  description: Calidad local y gates
- id: R2
  source: Objetivo humano de produccion
  description: Remotos y despliegue actual
- id: R3
  source: Objetivo humano de produccion
  description: Playwright publico
invariants:
- id: I0
  source: Usuario
  description: Sin difusion; datos y limites cientificos preservados; push sin force;
    cambios selectivos
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
  status: done
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
  status: done
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
  deliverable: Calidad local y gates
  status: done
  acceptance:
  - AC-P1
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
  deliverable: Remotos y despliegue actual
  status: done
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
  deliverable: Playwright publico
  status: done
  acceptance:
  - AC-P3
  mandatory: true
acceptance:
- id: AC-P0
  phase: P0
  task: T0
  description: Custodia e invariantes
  command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py
    --check baseline && python3 scripts/verify_thesis_editorial_delivery.py --check
    review && python3 scripts/verify_thesis_editorial_delivery.py --check pdf
  scope: tree
  input_paths: &id001
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias*.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml*.md
  - activos/3cucharadas/_pages/tesis-post*-anexo-metodologico*.md
  - activos/3cucharadas/scripts/verify_thesis*.py
  - activos/3cucharadas/scripts/verify_thesis*.mjs
  - activos/3cucharadas/assets/images/tesis-post*/manifest.json
  falsification:
    red_command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py
      --check baseline --fixture identity-drift
    green_command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py
      --check baseline && python3 scripts/verify_thesis_editorial_delivery.py --check
      review && python3 scripts/verify_thesis_editorial_delivery.py --check pdf
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T01:11:25Z'
    fixture_sha256: 09370e38d5caba168dafef9f08dd77f6dee873dd5bac0b0a999b411f1baaf65f
    red_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract/AC-P0-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract/AC-P0-green.json
- id: AC-P1
  phase: P1
  task: T1
  description: Calidad local y gates
  command: cd activos/3cucharadas && ruby scripts/verify_site_health.rb --profile
    source --report /tmp/thesis-production-contract-source.json && ruby scripts/verify_reference_links.rb
    && node scripts/verify_thesis_visual_quality.mjs --base-url http://127.0.0.1:4005
    --report /tmp/thesis-production-contract-local.json
  scope: tree
  input_paths: *id001
  falsification:
    red_command: cd activos/3cucharadas && node scripts/verify_thesis_visual_quality.mjs
      --base-url http://127.0.0.1:4005 --fixture low-contrast
    green_command: cd activos/3cucharadas && ruby scripts/verify_site_health.rb --profile
      source --report /tmp/thesis-production-contract-source.json && ruby scripts/verify_reference_links.rb
      && node scripts/verify_thesis_visual_quality.mjs --base-url http://127.0.0.1:4005
      --report /tmp/thesis-production-contract-local.json
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: activos/3cucharadas/scripts/verify_thesis_visual_quality.mjs
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T01:11:33Z'
    fixture_sha256: 88466bb24820e335a2c10f29c399f6dd2acd6c91fa3df9480789bac3020ce1a0
    red_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract/AC-P1-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract/AC-P1-green.json
- id: AC-P2
  phase: P2
  task: T2
  description: Remotos y despliegue actual
  command: cd activos/3cucharadas && python3 scripts/verify_thesis_production.py --artifact-root
    /tmp/codex-thesis-ci-artifact/public --receipt /tmp/thesis-production-contract-deployed.json
  scope: tree
  input_paths: *id001
  falsification:
    red_command: cd activos/3cucharadas && python3 scripts/verify_thesis_production.py
      --artifact-root /tmp/codex-thesis-production-site --expected-sha 0000000000000000000000000000000000000000
      --receipt /tmp/thesis-production-contract-wrong-sha.json
    green_command: cd activos/3cucharadas && python3 scripts/verify_thesis_production.py
      --artifact-root /tmp/codex-thesis-ci-artifact/public --receipt /tmp/thesis-production-contract-deployed.json
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: activos/3cucharadas/scripts/verify_thesis_production.py
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T01:11:29Z'
    fixture_sha256: 72d8fac26f54447ac0b95890ed3a125f5ffdacc73a5812bf1f2981df438883e4
    red_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract/AC-P2-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract/AC-P2-green.json
- id: AC-P3
  phase: P3
  task: T3
  description: Playwright publico
  command: cd activos/3cucharadas && node scripts/verify_thesis_visual_quality.mjs
    --base-url https://3cucharadas.cl --report /tmp/thesis-production-contract-visual-public.json
  scope: tree
  input_paths: *id001
  falsification:
    red_command: cd activos/3cucharadas && node scripts/verify_thesis_visual_quality.mjs
      --base-url https://3cucharadas.cl --fixture low-contrast
    green_command: cd activos/3cucharadas && node scripts/verify_thesis_visual_quality.mjs
      --base-url https://3cucharadas.cl --report /tmp/thesis-production-contract-visual-public.json
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: activos/3cucharadas/scripts/verify_thesis_visual_quality.mjs
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T01:13:25Z'
    fixture_sha256: 88466bb24820e335a2c10f29c399f6dd2acd6c91fa3df9480789bac3020ce1a0
    red_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract/AC-P3-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261108-thesis-production/evidence/contract/AC-P3-green.json
changes: []
emergent_tasks: []
completion:
  status: complete
  require_all_mandatory_tasks_done: true
  require_all_acceptance_passed: true
  allow_authorized_deferred_exclusions: true
```
<!-- contract:thesis-production:end -->
