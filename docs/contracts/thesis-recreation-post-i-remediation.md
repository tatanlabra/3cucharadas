# Remediación final del Post I de recreación de tesis

<!-- contract:thesis-recreation-post-i-remediation:begin -->
```yaml
plan_contract_version: 1
plan:
  id: thesis-recreation-post-i-remediation
  title: Remediación editorial, metodológica y visual del Post I
  source: "Plan aprobado por la persona autora el 2026-09-27, ampliado por su instrucción de avanzar con lo faltante."
  accepted_at: "2026-09-27T10:21:54-03:00"
  revision: 3
task:
  id: thesis-recreation-post-i-remediation
  objective: Dejar los drafts ES/EN listos para revisión humana detallada, con evidencia F5 coherente, UX responsiva y dos commits locales verificables.
  scope: Dos repositorios locales; sin modificar fuentes históricas, incorporar PDFs, mover drafts a posts, publicar, desplegar ni hacer push.
parameters:
  preview_url: http://127.0.0.1:4004
  thesis_repository: incubadora/tesis_mae_mejorada
  blog_repository: activos/3cucharadas
  target_state: READY_FOR_DETAILED_REVIEW_V2
requirements:
  - {id: REQ-CUSTODY, source: user:plan, description: Fijar baseline y preservar cambios concurrentes antes de editar.}
  - {id: REQ-SOURCE, source: user:source-and-post, description: Distinguir los 12 coeficientes del productor de los 11 efectos publicados y de sus 10 coincidencias.}
  - {id: REQ-PRODUCER-MOBILITY, source: user:advance-missing, description: "Recuperar las fórmulas productoras de las Figuras 2–4, corregir la salida canónica y conservar como sensibilidad las rutas alternativas."}
  - {id: REQ-EDITORIAL, source: user:critical-audit, description: "Corregir alcance, temporalidad y utilidad pública con paridad ES/EN."}
  - {id: REQ-VISUAL, source: user:ux-review, description: Reubicar y compactar el D2 y contener el carrusel con tipografía proporcionada.}
  - {id: REQ-CLOSE, source: user:implement-plan, description: "Demostrar rojo y recuperación verde, construir el sitio y crear commits locales selectivos."}
invariants:
  - {id: INV-CONCURRENT, source: git:baseline, description: "No revertir, sobreescribir ni incluir cambios ajenos de ninguno de los dos worktrees."}
  - {id: INV-HISTORICAL-SOURCE, source: thesis:AGENTS.md, description: La fuente histórica externa y sus datos permanecen de solo lectura.}
  - {id: INV-BILINGUAL, source: jekyll-post, description: "Título, fecha, ref, permalink, estructura y contenido sustantivo conservan paridad ES/EN."}
  - {id: INV-INFERENCE, source: estadistica, description: Ninguna asociación descriptiva se promueve a efecto causal ni alerta prospectiva validada.}
  - {id: INV-FALSIFIABLE, source: gates-falsables, description: Todo criterio nuevo debe observar un rojo pertinente y la recuperación verde sobre la misma definición.}
  - {id: INV-LOCAL-ONLY, source: user:scope, description: "No mover a posts, publicar, desplegar, hacer push ni versionar PDFs."}
phases:
  - {id: F0, status: done, objective: "Fijar custodia, baseline y contrato ejecutable.", depends_on: [], invariants: [INV-CONCURRENT, INV-HISTORICAL-SOURCE, INV-FALSIFIABLE], entry_gate: Worktrees y preview inspeccionados., exit_gate: Contrato estructuralmente válido y baseline registrado., rollback: Retirar solo contrato y recibos propios., mandatory: true}
  - {id: F1, status: done, objective: Reconciliar el Cuadro 7 y recuperar los productores de movilidad en F4/F5., depends_on: [F0], invariants: [INV-HISTORICAL-SOURCE, INV-FALSIFIABLE], entry_gate: "Productores, cuadros y gráficos incrustados comparados término a término y punto a punto.", exit_gate: "12 productor, 11 cuadro, 10 coincidencias; Figuras 2–4 en 80/80, 40/40 y 80/80; cero errores presentes conocidos.", rollback: "Revertir el commit científico local e4c8d924 sin tocar corridas ni figuras espaciales ajenas.", mandatory: true}
  - {id: F2, status: done, objective: Corregir el relato público y la progresión editorial bilingüe., depends_on: [F1], invariants: [INV-BILINGUAL, INV-INFERENCE, INV-FALSIFIABLE], entry_gate: Nuevo commit F5 fijado por hash., exit_gate: Claims acotados y matriz de uso público presentes en ES/EN., rollback: Restaurar juntos ambos drafts y el manifiesto editorial., mandatory: true}
  - {id: F3, status: done, objective: "Corregir D2, carrusel, jerarquía y accesibilidad responsiva.", depends_on: [F2], invariants: [INV-BILINGUAL, INV-FALSIFIABLE], entry_gate: Baseline visual rojo capturado., exit_gate: Matriz de viewports y temas sin desborde ni violaciones de accesibilidad., rollback: "Restaurar fuentes D2, SVG y CSS del commit previo.", mandatory: true}
  - {id: F4, status: done, objective: "Cerrar gates, build, auditoría y commits locales selectivos.", depends_on: [F3], invariants: [INV-CONCURRENT, INV-LOCAL-ONLY, INV-FALSIFIABLE], entry_gate: F0-F3 verdes sobre los mismos bytes., exit_gate: READY_FOR_DETAILED_REVIEW_V2 ligado a dos commits locales y preview 4004., rollback: Revertir selectivamente los dos commits locales; no tocar cambios ajenos., mandatory: true}
tasks:
  - id: TASK-F0
    phase: F0
    requirements: [REQ-CUSTODY]
    owner: codex-principal
    allowed_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-remediation.md, activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation]
    deliverable: Contrato validado y baseline de custodia.
    status: done
    acceptance: [AC-F0]
    mandatory: true
  - id: TASK-F1
    phase: F1
    requirements: [REQ-SOURCE]
    owner: codex-principal
    allowed_paths: [incubadora/tesis_mae_mejorada/.agent/contracts, incubadora/tesis_mae_mejorada/.agent/evidence, incubadora/tesis_mae_mejorada/audit, incubadora/tesis_mae_mejorada/editorial/full_audit_pdf, incubadora/tesis_mae_mejorada/reports, incubadora/tesis_mae_mejorada/src/school_exit, incubadora/tesis_mae_mejorada/tests, incubadora/tesis_mae_mejorada/DECISIONS.md, incubadora/tesis_mae_mejorada/milestones/STATUS.md]
    deliverable: Productores F4/F5, reconciliaciones y cierre regenerados en el commit local e4c8d924.
    status: done
    acceptance: [AC-F1]
    mandatory: true
  - id: TASK-F2
    phase: F2
    requirements: [REQ-EDITORIAL]
    owner: codex-principal
    allowed_paths: [activos/3cucharadas/_drafts/2026-08-29-replica-tesis-establecimientos-educacionales.md, activos/3cucharadas/_drafts/2026-08-29-replica-tesis-establecimientos-educacionales-en.md, activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml, activos/3cucharadas/scripts/verify_thesis_recreation_post_i_ready_review.rb]
    deliverable: Relato bilingüe corregido y evidencia editorial repineada.
    status: done
    acceptance: [AC-F2]
    mandatory: true
  - id: TASK-F3
    phase: F3
    requirements: [REQ-VISUAL]
    owner: codex-principal
    allowed_paths: [activos/3cucharadas/_drafts/2026-08-29-replica-tesis-establecimientos-educacionales.md, activos/3cucharadas/_drafts/2026-08-29-replica-tesis-establecimientos-educacionales-en.md, activos/3cucharadas/assets/css/main.scss, activos/3cucharadas/assets/images/replica-tesis-establecimientos, activos/3cucharadas/scripts/verify_thesis_recreation_post_i_browser.mjs, activos/3cucharadas/scripts/verify_thesis_recreation_post_i_ready_review.rb]
    deliverable: D2 compacto y carrusel responsivo validados en navegador real.
    status: done
    acceptance: [AC-F3]
    mandatory: true
  - id: TASK-F4
    phase: F4
    requirements: [REQ-CLOSE]
    owner: codex-principal
    allowed_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-remediation.md, activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation, activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml]
    deliverable: Recibos, build, auditoría y commit local del blog.
    status: done
    acceptance: [AC-F4]
    mandatory: true
acceptance:
  - id: AC-F0
    phase: F0
    task: TASK-F0
    description: El contrato cubre fases, tareas, dependencias, alcance y cierre sin ejecutar trabajo todavía.
    command: bash scripts/verify_handoff_governance_contract.sh --require-plan-profile --contract activos/3cucharadas/docs/contracts/thesis-recreation-post-i-remediation.md --contract-id thesis-recreation-post-i-remediation --validate-only --json
    scope: tree
    input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-remediation.md, penta-agent/specs/plan-contract.schema.json]
    falsification: {red_command: "bash scripts/verify_handoff_governance_contract.sh --require-plan-profile --contract activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f0-invalid.md --contract-id thesis-recreation-post-i-remediation --validate-only --json | jq -e '.result != \"ERROR\"'", green_command: 'python3 -c "from pathlib import Path; from scripts.plan_contract import extract_contract, validate_contract; y,c=extract_contract(Path(\"activos/3cucharadas/docs/contracts/thesis-recreation-post-i-remediation.md\"),\"thesis-recreation-post-i-remediation\"); validate_contract(c,yaml_text=y,require_evidence_files=False); print(\"VALID\")"', red_setup_status: fixture_loaded, green_setup_status: stable_tree, red_input_paths: [activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f0-invalid.md, penta-agent/specs/plan-contract.schema.json], green_input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-remediation.md, penta-agent/specs/plan-contract.schema.json], fixture_path: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f0-invalid.md}
    falsified_by: {status: observed, method: fixture, observed_at: "2026-09-27T12:43:57-03:00", red_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F0-red.json, green_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F0-green.json, fixture_sha256: 29b57d42f0feda130494cb6e6cd3cc97ab9db4ba941787b272b020fc43fec0b4}
  - id: AC-F1
    phase: F1
    task: TASK-F1
    description: F5 distingue 12 coeficientes del productor, 11 efectos publicados y 10 coincidencias sin cambiar el inventario de 34 juicios.
    command: "git -C incubadora/tesis_mae_mejorada show e4c8d924691bf40763897fd61ad6df7459fab82c:audit/f5_judgment_registry.json | jq -e '.summary.judgments == 34 and ([.judgments[] | select(.id == \"J-012\")][0].mecanismo | contains(\"once efectos\") and contains(\"otros diez\") and contains(\"doce coeficientes\"))'"
    scope: tree
    input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml]
    falsification: {red_command: "jq -e '.producer_coefficients == 12 and .published_fixed_effects == 11 and .matching_fixed_effects == 10' activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-baseline.json", green_command: "git -C incubadora/tesis_mae_mejorada show e4c8d924691bf40763897fd61ad6df7459fab82c:audit/f5_judgment_registry.json | jq -e '.summary.judgments == 34 and ([.judgments[] | select(.id == \"J-012\")][0].mecanismo | contains(\"once efectos\") and contains(\"otros diez\") and contains(\"doce coeficientes\"))'", red_setup_status: fixture_loaded, green_setup_status: restored, red_input_paths: [activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-baseline.json], green_input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml], fixture_path: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-baseline.json}
    falsified_by: {status: observed, method: fixture, observed_at: "2026-09-27T12:43:58-03:00", red_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F1-red.json, green_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F1-green.json, fixture_sha256: ce17ae105474ee2e73c3aeda6d8187c6b687ef584c44040f32834238ba228753}
  - id: AC-F2
    phase: F2
    task: TASK-F2
    description: ES/EN acotan temporalidad, territorio, uso público y causalidad y conservan paridad editorial.
    command: cd activos/3cucharadas && ruby scripts/verify_thesis_recreation_post_i_ready_review.rb --thesis-root ../../incubadora/tesis_mae_mejorada --external-papers /home/ende/Descargas/investigacion/tesis-recreacion-educacion/papers --staged
    scope: tree
    input_paths: [activos/3cucharadas/_drafts/2026-08-29-replica-tesis-establecimientos-educacionales.md, activos/3cucharadas/_drafts/2026-08-29-replica-tesis-establecimientos-educacionales-en.md, activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml]
    falsification: {red_command: "cd activos/3cucharadas && ruby scripts/verify_thesis_recreation_post_i_ready_review.rb --self-test --staged --thesis-root ../../incubadora/tesis_mae_mejorada | jq -e '(.observed_red_controls | index(\"C12\")) == null'", green_command: cd activos/3cucharadas && ruby scripts/verify_thesis_recreation_post_i_ready_review.rb --thesis-root ../../incubadora/tesis_mae_mejorada --external-papers /home/ende/Descargas/investigacion/tesis-recreacion-educacion/papers --staged, red_setup_status: fixture_loaded, green_setup_status: restored, red_input_paths: [activos/3cucharadas/scripts/verify_thesis_recreation_post_i_ready_review.rb, activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml], green_input_paths: [activos/3cucharadas/_drafts/2026-08-29-replica-tesis-establecimientos-educacionales.md, activos/3cucharadas/_drafts/2026-08-29-replica-tesis-establecimientos-educacionales-en.md, activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml], fixture_path: activos/3cucharadas/scripts/verify_thesis_recreation_post_i_ready_review.rb}
    falsified_by: {status: observed, method: fixture, observed_at: "2026-09-27T12:45:30-03:00", red_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F2-red.json, green_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F2-green.json, fixture_sha256: 8385ba1ac371d7afa60d366b965af4c17bbc937b84288cd431c62d51b2f2c82c}
  - id: AC-F3
    phase: F3
    task: TASK-F3
    description: Carrusel y D2 pasan geometría, interacción, legibilidad y accesibilidad en la matriz responsiva.
    command: node activos/3cucharadas/scripts/verify_thesis_recreation_post_i_browser.mjs --base-url http://127.0.0.1:4004
    scope: live
    input_paths: [activos/3cucharadas/assets/css/main.scss, activos/3cucharadas/assets/images/replica-tesis-establecimientos, activos/3cucharadas/scripts/verify_thesis_recreation_post_i_browser.mjs]
    falsification: {red_command: node activos/3cucharadas/scripts/verify_thesis_recreation_post_i_browser.mjs --fixture baseline, green_command: node activos/3cucharadas/scripts/verify_thesis_recreation_post_i_browser.mjs --base-url http://127.0.0.1:4004, red_setup_status: historical_loaded, green_setup_status: stable_tree, red_input_paths: [activos/3cucharadas/assets/css/main.scss, activos/3cucharadas/assets/images/replica-tesis-establecimientos, activos/3cucharadas/scripts/verify_thesis_recreation_post_i_browser.mjs], green_input_paths: [activos/3cucharadas/assets/css/main.scss, activos/3cucharadas/assets/images/replica-tesis-establecimientos, activos/3cucharadas/scripts/verify_thesis_recreation_post_i_browser.mjs], fixture_path: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f3-baseline.json}
    falsified_by: {status: observed, method: historical_artifact, observed_at: "2026-09-27T12:45:00-03:00", red_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F3-red.json, green_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F3-green.json}
  - id: AC-F4
    phase: F4
    task: TASK-F4
    description: El cierre liga verificadores, build, commits selectivos y preview sin publicación externa.
    command: cd activos/3cucharadas && ruby scripts/verify_thesis_recreation_post_i_ready_review.rb --thesis-root ../../incubadora/tesis_mae_mejorada --external-papers /home/ende/Descargas/investigacion/tesis-recreacion-educacion/papers --staged
    scope: tree
    input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-remediation.md, activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml, activos/3cucharadas/scripts/verify_thesis_recreation_post_i_ready_review.rb]
    falsification: {red_command: "cd activos/3cucharadas && ruby scripts/verify_thesis_recreation_post_i_ready_review.rb --self-test --staged --thesis-root ../../incubadora/tesis_mae_mejorada | jq -e '(.observed_red_controls | index(\"C6\")) == null'", green_command: cd activos/3cucharadas && ruby scripts/verify_thesis_recreation_post_i_ready_review.rb --thesis-root ../../incubadora/tesis_mae_mejorada --external-papers /home/ende/Descargas/investigacion/tesis-recreacion-educacion/papers --staged, red_setup_status: fixture_loaded, green_setup_status: stable_tree, red_input_paths: [activos/3cucharadas/scripts/verify_thesis_recreation_post_i_ready_review.rb, activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml], green_input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-remediation.md, activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml, activos/3cucharadas/scripts/verify_thesis_recreation_post_i_ready_review.rb], fixture_path: activos/3cucharadas/scripts/verify_thesis_recreation_post_i_ready_review.rb}
    falsified_by: {status: observed, method: fixture, observed_at: "2026-09-27T12:45:34-03:00", red_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F4-red.json, green_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F4-green.json, fixture_sha256: 8385ba1ac371d7afa60d366b965af4c17bbc937b84288cd431c62d51b2f2c82c}
  - id: AC-F1-MOBILITY
    phase: F1
    task: EM-F1-PRODUCER-MOBILITY
    description: Las fórmulas productoras recomputan las Figuras 2–4 punto a punto y eliminan los errores conocidos de la salida canónica sin cruzar la frontera causal.
    command: "git -C incubadora/tesis_mae_mejorada show e4c8d924691bf40763897fd61ad6df7459fab82c:audit/f4_divergence_adjudication.json | jq -e '.displays[\"FIGURE-02\"].producer_workbook.formula_cells_verified == 400 and .displays[\"FIGURE-02\"].producer_workbook.embedded_chart_comparisons[\"FIGURE-02\"].points == 80 and .displays[\"FIGURE-02\"].producer_workbook.embedded_chart_comparisons[\"FIGURE-03\"].points == 40 and .displays[\"FIGURE-02\"].producer_workbook.embedded_chart_comparisons[\"FIGURE-04\"].points == 80 and .displays[\"FIGURE-02\"].producer_workbook.all_embedded_series_match == true'"
    scope: tree
    input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml, activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-mobility-baseline.json]
    falsification: {red_command: "jq -e '.formula_cells_verified == 400 and .figure_02_matching_points == 80 and .figure_03_matching_points == 40 and .figure_04_matching_points == 80 and .known_present_errors == 0' activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-mobility-baseline.json", green_command: "git -C incubadora/tesis_mae_mejorada show e4c8d924691bf40763897fd61ad6df7459fab82c:audit/f4_divergence_adjudication.json | jq -e '.displays[\"FIGURE-02\"].producer_workbook.formula_cells_verified == 400 and .displays[\"FIGURE-02\"].producer_workbook.embedded_chart_comparisons[\"FIGURE-02\"].points == 80 and .displays[\"FIGURE-02\"].producer_workbook.embedded_chart_comparisons[\"FIGURE-03\"].points == 40 and .displays[\"FIGURE-02\"].producer_workbook.embedded_chart_comparisons[\"FIGURE-04\"].points == 80 and .displays[\"FIGURE-02\"].producer_workbook.all_embedded_series_match == true'", red_setup_status: fixture_loaded, green_setup_status: stable_tree, red_input_paths: [activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-mobility-baseline.json], green_input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml, activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-mobility-baseline.json], fixture_path: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-mobility-baseline.json}
    falsified_by: {status: observed, method: fixture, observed_at: "2026-09-27T12:43:58-03:00", red_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F1-MOBILITY-red.json, green_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F1-MOBILITY-green.json, fixture_sha256: d987ce896ea5fc6cad8d7044aa125663ba1ea582467328b14e3d62792fe401fe}
  - id: AC-F1-HYGIENE
    phase: F1
    task: EM-F1-HYGIENE
    description: La higiene contractual refleja el contrato F5 vigente sin ciclos ni referencias stale.
    command: "git -C incubadora/tesis_mae_mejorada show e4c8d924691bf40763897fd61ad6df7459fab82c:audit/contract_hygiene.json | jq -e '([.provenance.entries[] | select(.status == \"STALE\")] | length) == 0 and (.provenance.cycles | length) == 0'"
    scope: tree
    input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml]
    falsification: {red_command: "jq -e '(.provenance.cycles | length) == 0' activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-hygiene-cycle.json", green_command: "git -C incubadora/tesis_mae_mejorada show e4c8d924691bf40763897fd61ad6df7459fab82c:audit/contract_hygiene.json | jq -e '([.provenance.entries[] | select(.status == \"STALE\")] | length) == 0 and (.provenance.cycles | length) == 0'", red_setup_status: fixture_loaded, green_setup_status: stable_tree, red_input_paths: [activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-hygiene-cycle.json], green_input_paths: [activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml], fixture_path: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/ac-f1-hygiene-cycle.json}
    falsified_by: {status: observed, method: fixture, observed_at: "2026-09-27T12:43:58-03:00", red_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F1-HYGIENE-red.json, green_receipt: activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/AC-F1-HYGIENE-green.json, fixture_sha256: 459b1afd0568b92af2f734034762c03e944f2ce0985ed7aed3ff9d7499194c5e}
changes:
  - {id: CHG-SOURCE-SCOPE, description: Corregir la fuente F5 y repinear el post., reason: La persona autora eligió fuente y post después de distinguir los universos 12/11/10., material: true, approval_refs: ["Respuesta usuario 2026-09-27: Fuente y post; valida en profundidad."]}
  - {id: CHG-D2-PLACEMENT, description: Mover y compactar el D2 en Cucharada 2., reason: La persona autora observó que el diagrama domina Cucharada 3 y no explica el método en su lugar natural., material: true, approval_refs: ["Mensaje usuario 2026-09-27: D2 mejor en cucharada 2."]}
  - {id: CHG-CAROUSEL-GEOMETRY, description: Contener carrusel y reducir jerarquía tipográfica desktop., reason: La medición confirmó solapamiento con la columna izquierda y títulos desproporcionados., material: true, approval_refs: ["Mensaje usuario 2026-09-27: carrusel se desborda y letra muy grande."]}
  - {id: CHG-PRODUCER-MOBILITY, description: Sustituir las aproximaciones provisionales por las fórmulas productoras de las Figuras 2–4., reason: La planilla TESIS.xlsx y los vectores del manuscrito permiten una comparación punto a punto que discrimina la ruta canónica., material: true, approval_refs: ["Mensaje usuario 2026-09-27: avanza con lo faltante."]}
emergent_tasks:
  - id: EM-F1-HYGIENE
    phase: F1
    requirements: [REQ-CUSTODY, REQ-SOURCE]
    owner: codex-principal
    allowed_paths: [incubadora/tesis_mae_mejorada/audit/contract_hygiene.json, incubadora/tesis_mae_mejorada/reports/194_contract_hygiene.md]
    deliverable: Derivados de higiene coherentes con el contrato F5 reabierto y cerrado.
    status: done
    acceptance: [AC-F1-HYGIENE]
    mandatory: true
    reason: El cierre obligatorio de higiene regeneró conteos contractuales y de falsabilidad después de añadir AC-004.
    material: false
    approval_refs: []
  - id: EM-F1-PRODUCER-MOBILITY
    phase: F1
    requirements: [REQ-SOURCE, REQ-PRODUCER-MOBILITY]
    owner: codex-principal
    allowed_paths: [incubadora/tesis_mae_mejorada/audit/f4_divergence_adjudication.json, incubadora/tesis_mae_mejorada/audit/f5_judgment_registry.json, incubadora/tesis_mae_mejorada/audit/recreation_result_comparison_v2.json, incubadora/tesis_mae_mejorada/audit/post_face_to_face_carousel.json, activos/3cucharadas/_data/thesis_recreation_face_to_face.yml, activos/3cucharadas/assets/images/replica-tesis-establecimientos/face-to-face]
    deliverable: "Figuras 2–4 recreadas desde fórmulas productoras, carrusel repineado y cero errores presentes conocidos."
    status: done
    acceptance: [AC-F1-MOBILITY]
    mandatory: true
    reason: La inspección de TESIS.xlsx recuperó el productor que la búsqueda por valores sueltos había pasado por alto.
    material: true
    approval_refs: ["Mensaje usuario 2026-09-27: avanza con lo faltante."]
completion:
  status: complete
  require_all_mandatory_tasks_done: true
  require_all_acceptance_passed: true
  allow_authorized_deferred_exclusions: true
  evidence_refs:
    - activos/3cucharadas/docs/contracts/evidence/thesis-recreation-post-i-remediation/remediation-closeout.json
    - activos/3cucharadas/docs/contracts/thesis-recreation-post-i-ready-review.yaml
```
<!-- contract:thesis-recreation-post-i-remediation:end -->
