# Implementación editorial III–IV

Plan aprobado el 2026-11-07. Cierre local; sin publicación, commit, push ni envío.

## Contrato de lectura

- Público adulto no especialista; yo, comillas dobles, números regionalizados. Chicago-Deusto ES y CMOS18 EN con excepciones del blog; bibliografía conserva formato.
- Preámbulo 180–250 palabras: motivación, hallazgo, comparación decisiva, límite. Un notice--primary.
- Tres cucharadas: pregunta, evidencia, interpretación, límite y transición. Cierre 200–250 palabras con recapitulación y tres desafíos verificables.
- III 2.500–3.200 palabras; IV 2.800–3.500, sin referencias ni anexos. ES se consolida antes de adaptar EN.
- III receptoras −3,35 pp descriptivo sin intervalo propio; 2016–2019 inconcluso por faltantes. IV: −12,26 y −0,26 corresponden a quintiles G1 reestimados bajo especificaciones distintas, no al mismo grupo de estudiantes; IP/CFT −2,09 pp es contracción del canal, sustitución no identificada.
- Títulos, fechas, ref y permalink de artículos invariantes. Ref de cada anexo distinto al artículo; pareja ES/EN comparte ref de anexo.

## Mapa de traslado

| Superficie | Principal | Anexo independiente |
|---|---|---|
| III | Figuras originales 2/3, tabla original 6 | Figuras 1/4; tablas 1–5/7; especificaciones y notas extensas |
| IV | Figura original 1 | Figuras 2/3; tablas 1–6; depuración, especificaciones y sensibilidad |

Conservar IDs de figuras, CSV, fuentes y enlaces de retorno; numeración visible independiente. Los límites necesarios para leer una conclusión permanecen en el principal.

## Responsabilidad y custodia

Un escritor por archivo: editor ES; adaptador EN tras F2; implementador de sitio/gates; productor de figuras/PDF; integrador para hero, contrato y revisión. Máximo tres trabajadores simultáneos más integrador. Baseline en evidence/baseline.json; respuestas y receipts en evidence/. El tablero persistido es pb-20261107T230204755Z-19e1bf67.

HANDOFF-TRACE: usuario → Codex integrador → editorial_hilo / implement_site / figures_pdf vía collaboration; revisión Claude mediante puente canónico.

## Derivas observadas

- Solicitud humana adicional: abrir tablero. El pane %42 no resultó visible para el usuario; se abrió una ventana Kitty independiente. Proceso confirmado; usuario confirmó visibilidad de la ventana independiente. Se corrigió después NO_COLOR=1 heredado para restaurar colores y énfasis ANSI en vista completa.
- Corrección técnica de interfaz: los anexos necesitan ref propio para evitar colisión Polyglot. Cumple la arquitectura aprobada, no amplía alcance.
- QA real detectó que el plugin de tablas solo procesaba posts: ampliar únicamente a los anexos III/IV por ref para conservar desplazamiento y encabezados accesibles.
- Las pruebas negativas web se amplían a HTTP y DOM reales; mutar una fila ya clasificada no basta para verificar el detector.
- Primer intento Claude inconcluso por DNS en sandbox, sin tokens procesados; respuesta original preservada y reintento por el mismo puente fuera del sandbox.
- Revisión adversarial corrigió definiciones, intervalos, atribución de perfiles G1 recalculados y referencias; r4 APPROVE confirmado tras delta menor por r5.
- QA del PDF detectó anclas HTML, fórmulas y Markdown literales, además de encabezados estrechos/vacíos; corrección acotada al renderizador, sin cambiar las fuentes ES aprobadas.
- Alineación natural limitada a la combinación de clases III/IV para conservar otras páginas.
- QA bilingüe de navegador rechazó 8/32 combinaciones de IV por una leyenda EN que omitía el límite jurídico D1/D2; la revisión manual detectó además un alt heredado que afirmaba efecto nulo. Corregir traducción, sin debilitar detector ni alterar ES aprobado.

<!-- contract:thesis-editorial-iii-iv:begin -->
```yaml
plan_contract_version: 1
plan:
  id: thesis-editorial-iii-iv
  title: 'III-IV: relato adulto, anexos y cierre local'
  source: 'Conversacion: plan aprobado con Implement the plan'
  accepted_at: '2026-11-07'
  revision: 1
task:
  id: editorial-iii-iv
  objective: Implementar plan aprobado y verificar evidencia sin publicacion
  scope: Dos articulos ES/EN, cuatro anexos, navegacion, hero IV, figuras IV, PDF IV, gates y evidencia local
parameters:
  post3_min: 2500
  post3_max: 3200
  post4_min: 2800
  post4_max: 3500
  board: pb-20261107T230204755Z-19e1bf67
requirements:
- id: R0
  source: Plan aprobado, fase F0
  description: Baseline e identidad
- id: R1
  source: Plan aprobado, fase F1
  description: ES condensado, anexos y evidencia
- id: R2
  source: Plan aprobado, fase F2
  description: Revision adversarial ES vigente
- id: R3
  source: Plan aprobado, fase F3
  description: Paridad ES/EN y PDF integrado
- id: R4
  source: Plan aprobado, fase F4
  description: Ocho rutas responsive y navegables
- id: R5
  source: Plan aprobado, fase F5
  description: Integridad final y cierre local
invariants:
- id: I0
  source: Plan aprobado
  description: Sin commit/push/publicacion/envios; preservar identidad, datos, limites inferenciales y cambios concurrentes.
phases:
- id: F0
  status: done
  objective: Baseline e identidad
  depends_on: []
  invariants:
  - I0
  entry_gate: Plan humano aprobado y baseline inspeccionado
  exit_gate: AC-F0
  rollback: Restaurar solo hunks propios desde baseline; no reset ni limpieza global
  mandatory: true
- id: F1
  status: done
  objective: ES condensado, anexos y evidencia
  depends_on:
  - F0
  invariants:
  - I0
  entry_gate: Fase anterior aceptada; trabajo independiente puede adelantarse
  exit_gate: AC-F1
  rollback: Restaurar solo hunks propios desde baseline; no reset ni limpieza global
  mandatory: true
- id: F2
  status: done
  objective: Revision adversarial ES vigente
  depends_on:
  - F1
  invariants:
  - I0
  entry_gate: Fase anterior aceptada; trabajo independiente puede adelantarse
  exit_gate: AC-F2
  rollback: Restaurar solo hunks propios desde baseline; no reset ni limpieza global
  mandatory: true
- id: F3
  status: done
  objective: Paridad ES/EN y PDF integrado
  depends_on:
  - F2
  invariants:
  - I0
  entry_gate: Fase anterior aceptada; trabajo independiente puede adelantarse
  exit_gate: AC-F3
  rollback: Restaurar solo hunks propios desde baseline; no reset ni limpieza global
  mandatory: true
- id: F4
  status: done
  objective: Ocho rutas responsive y navegables
  depends_on:
  - F3
  invariants:
  - I0
  entry_gate: Fase anterior aceptada; trabajo independiente puede adelantarse
  exit_gate: AC-F4
  rollback: Restaurar solo hunks propios desde baseline; no reset ni limpieza global
  mandatory: true
- id: F5
  status: done
  objective: Integridad final y cierre local
  depends_on:
  - F4
  invariants:
  - I0
  entry_gate: Fase anterior aceptada; trabajo independiente puede adelantarse
  exit_gate: AC-F5
  rollback: Restaurar solo hunks propios desde baseline; no reset ni limpieza global
  mandatory: true
tasks:
- id: T0
  phase: F0
  requirements:
  - R0
  owner: Codex
  allowed_paths:
  - activos/3cucharadas/_posts/*
  - activos/3cucharadas/_pages/tesis-post*-anexo-metodologico*
  - activos/3cucharadas/scripts/*thesis*
  - activos/3cucharadas/_plugins/tabla_desplazable.rb
  - activos/3cucharadas/tests/test_verify_thesis*
  - activos/3cucharadas/_includes/thesis-series-nav.html
  - activos/3cucharadas/assets/images/tesis-post4/*
  - activos/3cucharadas/assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/*
  - activos/3cucharadas/_data/visuales/cierre-escolar-educacion-superior-causal-ml.yml
  - activos/3cucharadas/assets/css/main.scss
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/*
  - activos/3cucharadas/docs/style-manual-corpus.md
  - incubadora/tesis_mae_mejorada/scripts/352_post4_visuals.py
  - incubadora/tesis_mae_mejorada/scripts/353_render_and_send_post4_pdf.py
  - incubadora/tesis_mae_mejorada/tests/*post4*
  - incubadora/tesis_mae_mejorada/milestones/STATUS.md
  - activos/3cucharadas/scripts/build_thesis_post4_hero.py
  - incubadora/tesis_mae_mejorada/outputs/post4_visuals/*
  - incubadora/tesis_mae_mejorada/outputs/post4_delivery/*
  deliverable: Baseline e identidad
  status: done
  acceptance:
  - AC-F0
  mandatory: true
- id: T1
  phase: F1
  requirements:
  - R1
  owner: editorial_hilo + implement_site + figures_pdf
  allowed_paths:
  - activos/3cucharadas/_posts/*
  - activos/3cucharadas/_pages/tesis-post*-anexo-metodologico*
  - activos/3cucharadas/scripts/*thesis*
  - activos/3cucharadas/_plugins/tabla_desplazable.rb
  - activos/3cucharadas/tests/test_verify_thesis*
  - activos/3cucharadas/_includes/thesis-series-nav.html
  - activos/3cucharadas/assets/images/tesis-post4/*
  - activos/3cucharadas/assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/*
  - activos/3cucharadas/_data/visuales/cierre-escolar-educacion-superior-causal-ml.yml
  - activos/3cucharadas/assets/css/main.scss
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/*
  - activos/3cucharadas/docs/style-manual-corpus.md
  - incubadora/tesis_mae_mejorada/scripts/352_post4_visuals.py
  - incubadora/tesis_mae_mejorada/scripts/353_render_and_send_post4_pdf.py
  - incubadora/tesis_mae_mejorada/tests/*post4*
  - incubadora/tesis_mae_mejorada/milestones/STATUS.md
  - activos/3cucharadas/scripts/build_thesis_post4_hero.py
  - incubadora/tesis_mae_mejorada/outputs/post4_visuals/*
  - incubadora/tesis_mae_mejorada/outputs/post4_delivery/*
  deliverable: ES condensado, anexos y evidencia
  status: done
  acceptance:
  - AC-F1
  mandatory: true
- id: T2
  phase: F2
  requirements:
  - R2
  owner: Claude via claude-bridge; Codex integra
  allowed_paths:
  - activos/3cucharadas/_posts/*
  - activos/3cucharadas/_pages/tesis-post*-anexo-metodologico*
  - activos/3cucharadas/scripts/*thesis*
  - activos/3cucharadas/_plugins/tabla_desplazable.rb
  - activos/3cucharadas/tests/test_verify_thesis*
  - activos/3cucharadas/_includes/thesis-series-nav.html
  - activos/3cucharadas/assets/images/tesis-post4/*
  - activos/3cucharadas/assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/*
  - activos/3cucharadas/_data/visuales/cierre-escolar-educacion-superior-causal-ml.yml
  - activos/3cucharadas/assets/css/main.scss
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/*
  - activos/3cucharadas/docs/style-manual-corpus.md
  - incubadora/tesis_mae_mejorada/scripts/352_post4_visuals.py
  - incubadora/tesis_mae_mejorada/scripts/353_render_and_send_post4_pdf.py
  - incubadora/tesis_mae_mejorada/tests/*post4*
  - incubadora/tesis_mae_mejorada/milestones/STATUS.md
  - activos/3cucharadas/scripts/build_thesis_post4_hero.py
  - incubadora/tesis_mae_mejorada/outputs/post4_visuals/*
  - incubadora/tesis_mae_mejorada/outputs/post4_delivery/*
  deliverable: Revision adversarial ES vigente
  status: done
  acceptance:
  - AC-F2
  mandatory: true
- id: T3
  phase: F3
  requirements:
  - R3
  owner: Adaptador EN + figures_pdf
  allowed_paths:
  - activos/3cucharadas/_posts/*
  - activos/3cucharadas/_pages/tesis-post*-anexo-metodologico*
  - activos/3cucharadas/scripts/*thesis*
  - activos/3cucharadas/_plugins/tabla_desplazable.rb
  - activos/3cucharadas/tests/test_verify_thesis*
  - activos/3cucharadas/_includes/thesis-series-nav.html
  - activos/3cucharadas/assets/images/tesis-post4/*
  - activos/3cucharadas/assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/*
  - activos/3cucharadas/_data/visuales/cierre-escolar-educacion-superior-causal-ml.yml
  - activos/3cucharadas/assets/css/main.scss
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/*
  - activos/3cucharadas/docs/style-manual-corpus.md
  - incubadora/tesis_mae_mejorada/scripts/352_post4_visuals.py
  - incubadora/tesis_mae_mejorada/scripts/353_render_and_send_post4_pdf.py
  - incubadora/tesis_mae_mejorada/tests/*post4*
  - incubadora/tesis_mae_mejorada/milestones/STATUS.md
  - activos/3cucharadas/scripts/build_thesis_post4_hero.py
  - incubadora/tesis_mae_mejorada/outputs/post4_visuals/*
  - incubadora/tesis_mae_mejorada/outputs/post4_delivery/*
  deliverable: Paridad ES/EN y PDF integrado
  status: done
  acceptance:
  - AC-F3
  mandatory: true
- id: T4
  phase: F4
  requirements:
  - R4
  owner: implement_site + Codex
  allowed_paths:
  - activos/3cucharadas/_posts/*
  - activos/3cucharadas/_pages/tesis-post*-anexo-metodologico*
  - activos/3cucharadas/scripts/*thesis*
  - activos/3cucharadas/_plugins/tabla_desplazable.rb
  - activos/3cucharadas/tests/test_verify_thesis*
  - activos/3cucharadas/_includes/thesis-series-nav.html
  - activos/3cucharadas/assets/images/tesis-post4/*
  - activos/3cucharadas/assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/*
  - activos/3cucharadas/_data/visuales/cierre-escolar-educacion-superior-causal-ml.yml
  - activos/3cucharadas/assets/css/main.scss
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/*
  - activos/3cucharadas/docs/style-manual-corpus.md
  - incubadora/tesis_mae_mejorada/scripts/352_post4_visuals.py
  - incubadora/tesis_mae_mejorada/scripts/353_render_and_send_post4_pdf.py
  - incubadora/tesis_mae_mejorada/tests/*post4*
  - incubadora/tesis_mae_mejorada/milestones/STATUS.md
  - activos/3cucharadas/scripts/build_thesis_post4_hero.py
  - incubadora/tesis_mae_mejorada/outputs/post4_visuals/*
  - incubadora/tesis_mae_mejorada/outputs/post4_delivery/*
  deliverable: Ocho rutas responsive y navegables
  status: done
  acceptance:
  - AC-F4
  mandatory: true
- id: T5
  phase: F5
  requirements:
  - R5
  owner: Codex
  allowed_paths:
  - activos/3cucharadas/_posts/*
  - activos/3cucharadas/_pages/tesis-post*-anexo-metodologico*
  - activos/3cucharadas/scripts/*thesis*
  - activos/3cucharadas/_plugins/tabla_desplazable.rb
  - activos/3cucharadas/tests/test_verify_thesis*
  - activos/3cucharadas/_includes/thesis-series-nav.html
  - activos/3cucharadas/assets/images/tesis-post4/*
  - activos/3cucharadas/assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/*
  - activos/3cucharadas/_data/visuales/cierre-escolar-educacion-superior-causal-ml.yml
  - activos/3cucharadas/assets/css/main.scss
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/*
  - activos/3cucharadas/docs/style-manual-corpus.md
  - incubadora/tesis_mae_mejorada/scripts/352_post4_visuals.py
  - incubadora/tesis_mae_mejorada/scripts/353_render_and_send_post4_pdf.py
  - incubadora/tesis_mae_mejorada/tests/*post4*
  - incubadora/tesis_mae_mejorada/milestones/STATUS.md
  - activos/3cucharadas/scripts/build_thesis_post4_hero.py
  - incubadora/tesis_mae_mejorada/outputs/post4_visuals/*
  - incubadora/tesis_mae_mejorada/outputs/post4_delivery/*
  deliverable: Integridad final y cierre local
  status: done
  acceptance:
  - AC-F5
  mandatory: true
acceptance:
- id: AC-F0
  phase: F0
  task: T0
  description: Baseline e identidad
  command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py --check baseline
  scope: tree
  input_paths: &id001
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/baseline.json
  - activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias.md
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml-en.md
  - activos/3cucharadas/assets/images/tesis-post3/*.csv
  - activos/3cucharadas/assets/images/tesis-post4/*.csv
  falsification:
    red_command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py --check baseline
      --fixture identity-drift
    green_command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py --check baseline
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id001
    green_input_paths: *id001
    fixture_path: activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T00:11:48Z'
    fixture_sha256: 09370e38d5caba168dafef9f08dd77f6dee873dd5bac0b0a999b411f1baaf65f
    red_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F0-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F0-green.json
- id: AC-F1
  phase: F1
  task: T1
  description: ES condensado, anexos y evidencia
  command: cd activos/3cucharadas && ruby scripts/verify_thesis_post3.rb --lang es && ruby scripts/verify_thesis_post4.rb
    --lang es
  scope: tree
  input_paths: &id002
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias.md
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml-en.md
  - activos/3cucharadas/_pages/tesis-post3-anexo-metodologico.md
  - activos/3cucharadas/_pages/tesis-post3-anexo-metodologico-en.md
  - activos/3cucharadas/_pages/tesis-post4-anexo-metodologico.md
  - activos/3cucharadas/_pages/tesis-post4-anexo-metodologico-en.md
  - activos/3cucharadas/scripts/verify_thesis_post3.rb
  - activos/3cucharadas/scripts/verify_thesis_post4.rb
  - activos/3cucharadas/scripts/*thesis*editorial*
  - activos/3cucharadas/assets/images/tesis-post3/*.csv
  - activos/3cucharadas/assets/images/tesis-post4/*.csv
  falsification:
    red_command: cd activos/3cucharadas && ruby scripts/verify_thesis_post4.rb --lang es --fixture annex-removed
    green_command: cd activos/3cucharadas && ruby scripts/verify_thesis_post3.rb --lang es && ruby scripts/verify_thesis_post4.rb
      --lang es
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id002
    green_input_paths: *id002
    fixture_path: activos/3cucharadas/scripts/verify_thesis_post4.rb
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T00:11:49Z'
    fixture_sha256: 3b8f9b09b7c648d5ce577ccf4e987a92ce9f0584b866825618db0266843647c7
    red_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F1-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F1-green.json
- id: AC-F2
  phase: F2
  task: T2
  description: Revision adversarial ES vigente
  command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py --check review
  scope: tree
  input_paths: &id003
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md
  - activos/3cucharadas/_pages/tesis-post3-anexo-metodologico.md
  - activos/3cucharadas/_pages/tesis-post4-anexo-metodologico.md
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/claude/*.json
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/claude/result*.md
  - activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  - activos/3cucharadas/assets/data/tesis-post4/post4_higher_education_causal_ml_v1.json
  - activos/3cucharadas/assets/data/tesis-post4/post4_retrospective_post3_audit.json
  falsification:
    red_command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py --check review --fixture
      review-stale
    green_command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py --check review
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id003
    green_input_paths: *id003
    fixture_path: activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T00:11:50Z'
    fixture_sha256: 09370e38d5caba168dafef9f08dd77f6dee873dd5bac0b0a999b411f1baaf65f
    red_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F2-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F2-green.json
- id: AC-F3
  phase: F3
  task: T3
  description: Paridad ES/EN y PDF integrado
  command: cd activos/3cucharadas && ruby scripts/verify_thesis_post3.rb && ruby scripts/verify_thesis_post4.rb
    && python3 scripts/verify_thesis_editorial_delivery.py --check pdf
  scope: tree
  input_paths: &id004
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias.md
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml-en.md
  - activos/3cucharadas/_pages/tesis-post3-anexo-metodologico.md
  - activos/3cucharadas/_pages/tesis-post3-anexo-metodologico-en.md
  - activos/3cucharadas/_pages/tesis-post4-anexo-metodologico.md
  - activos/3cucharadas/_pages/tesis-post4-anexo-metodologico-en.md
  - activos/3cucharadas/scripts/verify_thesis_post3.rb
  - activos/3cucharadas/scripts/verify_thesis_post4.rb
  - activos/3cucharadas/scripts/*thesis*editorial*
  - activos/3cucharadas/assets/images/tesis-post3/*.csv
  - activos/3cucharadas/assets/images/tesis-post4/*.csv
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/pdf-delivery.json
  - activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  - activos/3cucharadas/assets/images/tesis-post4/*-es-light.png
  - incubadora/tesis_mae_mejorada/scripts/353_render_and_send_post4_pdf.py
  - incubadora/tesis_mae_mejorada/outputs/post4_delivery/post4_borrador_educacion_superior_causal_ml.pdf
  - incubadora/tesis_mae_mejorada/outputs/post4_delivery/post4_borrador_educacion_superior_causal_ml.manifest.json
  falsification:
    red_command: cd activos/3cucharadas && python3 scripts/verify_thesis_editorial_delivery.py --check pdf --fixture
      pdf-stale
    green_command: cd activos/3cucharadas && ruby scripts/verify_thesis_post3.rb && ruby scripts/verify_thesis_post4.rb
      && python3 scripts/verify_thesis_editorial_delivery.py --check pdf
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id004
    green_input_paths: *id004
    fixture_path: activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T00:11:51Z'
    fixture_sha256: 09370e38d5caba168dafef9f08dd77f6dee873dd5bac0b0a999b411f1baaf65f
    red_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F3-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F3-green.json
- id: AC-F4
  phase: F4
  task: T4
  description: Ocho rutas responsive y navegables
  command: cd activos/3cucharadas && node scripts/verify_thesis_post3_browser.mjs --base-url http://127.0.0.1:4004
    --artifact-root /tmp/codex-thesis-editorial-site && node scripts/verify_thesis_post4_browser.mjs --base-url
    http://127.0.0.1:4004 --artifact-root /tmp/codex-thesis-editorial-site && python3 scripts/verify_thesis_editorial_delivery.py
    --check links --artifact-root /tmp/codex-thesis-editorial-site
  scope: live
  input_paths: &id005
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias.md
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml-en.md
  - activos/3cucharadas/_pages/tesis-post3-anexo-metodologico.md
  - activos/3cucharadas/_pages/tesis-post3-anexo-metodologico-en.md
  - activos/3cucharadas/_pages/tesis-post4-anexo-metodologico.md
  - activos/3cucharadas/_pages/tesis-post4-anexo-metodologico-en.md
  - activos/3cucharadas/scripts/verify_thesis_post*_browser.mjs
  - activos/3cucharadas/scripts/verify_thesis_series_browser.mjs
  - activos/3cucharadas/_plugins/tabla_desplazable.rb
  - activos/3cucharadas/_includes/thesis-series-nav.html
  - activos/3cucharadas/assets/css/main.scss
  - activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  - activos/3cucharadas/_config.yml
  - activos/3cucharadas/assets/images/tesis-post3/manifest.json
  - activos/3cucharadas/assets/images/tesis-post4/manifest.json
  falsification:
    red_command: cd activos/3cucharadas && node scripts/verify_thesis_post4_browser.mjs --base-url http://127.0.0.1:4004
      --artifact-root /tmp/codex-thesis-editorial-site --live-fixture missing-annex
    green_command: cd activos/3cucharadas && node scripts/verify_thesis_post3_browser.mjs --base-url http://127.0.0.1:4004
      --artifact-root /tmp/codex-thesis-editorial-site && node scripts/verify_thesis_post4_browser.mjs --base-url
      http://127.0.0.1:4004 --artifact-root /tmp/codex-thesis-editorial-site && python3 scripts/verify_thesis_editorial_delivery.py
      --check links --artifact-root /tmp/codex-thesis-editorial-site
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id005
    green_input_paths: *id005
    fixture_path: activos/3cucharadas/scripts/verify_thesis_series_browser.mjs
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T00:13:46Z'
    fixture_sha256: e05a76007e37cd923e831afd8666e16e8221e877f7a097d67a9cf9d58d9dc4c4
    red_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F4-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F4-green.json
- id: AC-F5
  phase: F5
  task: T5
  description: Integridad final y cierre local
  command: cd activos/3cucharadas && ruby scripts/verify_thesis_post3.rb && ruby scripts/verify_thesis_post4.rb
    && python3 scripts/verify_thesis_editorial_delivery.py --check baseline && git diff --check
  scope: tree
  input_paths: &id006
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias.md
  - activos/3cucharadas/_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md
  - activos/3cucharadas/_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml-en.md
  - activos/3cucharadas/_pages/tesis-post3-anexo-metodologico.md
  - activos/3cucharadas/_pages/tesis-post3-anexo-metodologico-en.md
  - activos/3cucharadas/_pages/tesis-post4-anexo-metodologico.md
  - activos/3cucharadas/_pages/tesis-post4-anexo-metodologico-en.md
  - activos/3cucharadas/scripts/verify_thesis_post3.rb
  - activos/3cucharadas/scripts/verify_thesis_post4.rb
  - activos/3cucharadas/scripts/*thesis*editorial*
  - activos/3cucharadas/assets/images/tesis-post3/*.csv
  - activos/3cucharadas/assets/images/tesis-post4/*.csv
  - activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/baseline.json
  - activos/3cucharadas/scripts/verify_thesis_editorial_delivery.py
  falsification:
    red_command: cd activos/3cucharadas && ruby scripts/verify_thesis_post4.rb --fixture primary-number-drift
    green_command: cd activos/3cucharadas && ruby scripts/verify_thesis_post3.rb && ruby scripts/verify_thesis_post4.rb
      && python3 scripts/verify_thesis_editorial_delivery.py --check baseline && git diff --check
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths: *id006
    green_input_paths: *id006
    fixture_path: activos/3cucharadas/scripts/verify_thesis_post4.rb
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-08T00:11:51Z'
    fixture_sha256: 3b8f9b09b7c648d5ce577ccf4e987a92ce9f0584b866825618db0266843647c7
    red_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F5-red.json
    green_receipt: activos/3cucharadas/docs/plans/20261107-thesis-editorial-iii-iv/evidence/contract/AC-F5-green.json
changes: []
emergent_tasks: []
completion:
  status: complete
  require_all_mandatory_tasks_done: true
  require_all_acceptance_passed: true
  allow_authorized_deferred_exclusions: true
```
<!-- contract:thesis-editorial-iii-iv:end -->
