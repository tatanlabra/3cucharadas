# PLAN_STATE v2 · Educación III

Entrega final implementada. Usuario delegó elección y autorizó envío por Telegram; HTML/CSS nativo elegido, mensaje 2322 verificado mediante descarga y hash.

HANDOFF-TRACE: Codex → humano · galería local y PDF · sin consulta a pares IA.

Estado documental: fuentes y resultados bajo custodia en esta carpeta. El entrypoint canónico `scripts/verify_handoff_governance_contract.sh` indicado por agent-plan-flow.md no existe en el checkout actual de penta-agent. Se validó el esquema con jsonschema; no se declara cierre integral mediante ese runner.

<!-- contract:educacion-iii-motores:begin -->
```yaml
plan_contract_version: 1
plan:
  id: educacion-iii-motores
  title: Cuatro composiciones nativas para Educación III
  source: 'Usuario: Implement the plan; decisión posterior Composición nativa (Recomendado)'
  accepted_at: '2026-11-10'
  revision: 3
task:
  id: pilot-native
  objective: Entregar cuatro PDF editables y comparables, con evidencia; elegir versión de producción por delegación del usuario
  scope: Piloto, generador nativo, paquete LinkedIn y skill publicacion-externa; envío Telegram autorizado; sin publicación ni cambios al post canónico
parameters:
  pages: 9
  engines: 4
  human_choice_pending: false
requirements:
- id: R1
  source: usuario
  description: Cuatro propuestas de composición nativa con idéntico contenido vigente
- id: R2
  source: usuario y gates-falsables
  description: Corregir solapamientos, revisar páginas y probar detección de artefactos
    defectuosos
- id: R3
  source: usuario
  description: Abrir PDF y mantener tablero de plan visible
invariants:
- id: I1
  source: scope autorizado
  description: Sin editar post canónico ni publicar; preservar límites y cifras del
    contenido congelado
phases:
- id: C1
  status: done
  objective: Prototipos locales y comparación técnica
  depends_on: []
  invariants:
  - I1
  entry_gate: Decisión explícita de composición nativa registrada
  exit_gate: Cuatro PDF y galería entregados; QA técnico y visual documentados; preferencia
    no simulada
  rollback: Conservar ronda 1 como antecedente rechazado; retirar solo esta carpeta
    si se descarta el piloto
  mandatory: true
tasks:
- id: T1
  phase: C1
  requirements:
  - R1
  - R2
  - R3
  owner: Codex
  allowed_paths:
  - .
  deliverable: out/native/{A,B,C,D}.pdf, fuentes, index.html, qa.json, probes y tablero
  status: done
  acceptance:
  - AC1
  mandatory: true
acceptance:
- id: AC1
  phase: C1
  task: T1
  description: Integridad técnica de PDF; la preferencia estética se mantiene como
    decisión humana independiente
  command: python3 native_verify.py --receipt out/native/qa.json
  scope: tree
  input_paths:
  - content.json
  - source-lock.json
  - native_verify.py
  - out/native/A.pdf
  - out/native/B.pdf
  - out/native/C.pdf
  - out/native/D.pdf
  falsification:
    red_command: python3 native_verify.py --engine typst --pdf out/native/probes/missing-page.pdf
    green_command: python3 native_verify.py
    red_setup_status: fixture_loaded
    green_setup_status: stable_tree
    red_input_paths:
    - out/native/probes/missing-page.pdf
    green_input_paths:
    - out/native/A.pdf
    - out/native/B.pdf
    - out/native/C.pdf
    - out/native/D.pdf
    fixture_path: out/native/probes/missing-page.pdf
  falsified_by:
    status: observed
    method: fixture
    observed_at: '2026-11-10T22:48:55.972937'
    red_receipt: out/native/probes/missing-page.json
    green_receipt: out/native/probes/green.json
changes:
- id: D2
  description: Sustituir maquetador común por composición propia de cada motor
  reason: Usuario rechazó similitud excesiva y defectos de diagramación de ronda 1
  material: true
  approval_refs:
  - 'request_user_input: Composición nativa (Recomendado)'
emergent_tasks: []
completion:
  status: complete
  require_all_mandatory_tasks_done: true
  require_all_acceptance_passed: true
  allow_authorized_deferred_exclusions: true
  evidence_refs:
  - out/native/qa.json
  - out/native/visual-review.json
  - out/native/probes/summary.json
  - out/native/stress/qa.json
```
<!-- contract:educacion-iii-motores:end -->

## Cierre de producción · 2026-11-10

- D3: usuario delegó elección heurística y ejecución desatendida; no queda preferencia pendiente como bloqueo.
- Motor elegido: HTML/CSS + Chromium. Razón, alternativas y límites en el README del paquete y referencia de la skill.
- Producción: `../../paquetes/costos-cierre-escolar-trayectorias/linkedin/` (desde raíz del repositorio: `difusion/paquetes/costos-cierre-escolar-trayectorias/linkedin/`).
- Generador: `scripts/render_linkedin_native.py`; prueba: `scripts/probe_linkedin_native.py` desde raíz del repositorio.
- Evidencia: `out/build.json`, `out/qa.json`, `out/visual-review.json`, `out/probes/summary.json`, `out/telegram-delivery.json` dentro del paquete de producción.
- Telegram: mensaje 2322; descarga idéntica al PDF local; lectura humana no observada.
- Skill: `penta-agent/skills/publicacion-externa/references/carrusel-linkedin-nativo.md`.
- Tablero: panel inferior de `codex_1`; ninguna segunda instancia Codex lanzada por esta ejecución.
- Sin commit, push ni publicación LinkedIn. El runner de gobernanza ausente no se presenta como ejecutado.
