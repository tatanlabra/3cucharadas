# Handoff: saneamiento y paleta nocturna

**Estado documental:** `draft`
**Fecha de estado:** 2026-09-06
**Evidencia de estado:** Codex emite resultados medidos y una decisión DEV pendiente.

**Estado de implementación:** `no-implementado`
**Evidencia de implementación:** la tarea del receptor es resolver la revisión de duplicados; el saneamiento técnico ya fue implementado según el informe enlazado.

## Metadata

- Task ID: site-health-20260906.
- From → To: Codex → humano.
- Vía: sesión Codex del workspace.
- Modelo origen: unknown; identificador exacto no expuesto en el contexto utilizable.
- Modelo destino: no aplica, humano.
- Skill: handoff-protocol.
- Fecha: 2026-09-06, America/Santiago.

HANDOFF-TRACE: Codex entrega a humano la validación pendiente de DEV (model: no aplica) vía sesión Codex.

MODEL-REPORT: {"agent":"Codex","provider":"OpenAI","model":"unknown","source":"unknown"}

DECISION: human_validation

## Decisiones inmutables

- Preservar historia y cambios previos; nada de force push ni reaplicar versiones antiguas del stash sobre main saneado.
- Ambos videos aprobados quedan archivados fuera del sitio, recuperables por hash.
- DEV sólo permite borradores existentes: no crear, publicar, despublicar ni tocar publicados.
- No Telegram ni difusión en otras redes; los compromisos editoriales vencidos siguen visibles.
- Paleta conservada con dos acentos teal leves; no rediseño ni cambio del tema claro.

## Artefactos

- `docs/evidence/site-health-20260906.md`: fases, pruebas, incidentes, producción y límites.
- `docs/evidence/night-palette-20260906.md`: baseline, dos candidatas y aceptación visual.
- `docs/contracts/site-health.yaml`: contrato ejecutable por `scripts/verify_site_health.rb`.
- `docs/contracts/devto-draft-maintenance.md`: permisos, cifrado y rollback de borradores.
- Custodia original: `~/.local/state/3cucharadas/git-backups/site-health-20260906T221857Z`.
- Videos: `~/.local/state/3cucharadas/source-masters/penta-rag-video-20260906`.
- Evidencia de ejecución: `/tmp/3c-health-run-LCLqKQ`, con copia durable bajo `~/.local/state/3cucharadas/site-health/20260906` al cierre.

## Contexto y tarea del receptor

DEV devolvió más de un artículo para el canonical EN de Avalúo. El preflight global
detuvo la corrida antes de escribir. Resolver la pregunta nativa pendiente: mantener
DEV pausado (menor riesgo), excluir Avalúo y procesar sólo los demás inequívocos,
o revisar IDs y escoger uno explícitamente. No hay autorización implícita para
eliminar duplicados ni para actualizar todos indiscriminadamente.

Hecho para esta revisión: decisión explícita registrada; si se continúa, inventario
autenticado actual, selección inequívoca, custodia cifrada y comprobación del estado
posterior. No introducir claves API en el chat ni en argumentos de comandos.

## Verificación y riesgos

- `ruby scripts/verify_site_health.rb --profile release --report /tmp/site-health-resume/report.json` desde el checkout operativo; exige herramientas instaladas, remotos, CI y CSS público real.
- Los informes incluyen SHA, digest fuente, comandos, logs y cobertura; un FAIL no se convierte en PASS por proximidad al cierre.
- Siete pruebas geoespaciales y navegadores heredados quedan fuera de cobertura ejecutada; axe no sustituye lectores de pantalla.
- No se acreditó mejora de velocidad: siete pares exploratorios no cumplieron la condición de promoción; CLS de laboratorio alto en ambas variantes, requiere experimento controlado.
- La API DEV no ofrece atomicidad entre relectura y PUT; no editar simultáneamente los borradores durante una eventual corrida autorizada.
- Riesgo residual técnico bajo para los cambios probados; pendiente operativo DEV y validación perceptual humana de la preferencia estética.
