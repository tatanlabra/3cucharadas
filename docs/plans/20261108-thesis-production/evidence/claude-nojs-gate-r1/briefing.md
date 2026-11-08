# Revisión dirigida: espera de imágenes con JavaScript desactivado

Estado documental: LISTO para revisión de solo lectura; el gate público completo corre en paralelo bajo custodia del integrador.
PLAN_STATE v2: pb-20261108T003705315Z-fc127547 rev24; D9/P4 abiertos solo por este gate. La aprobación previa visual/editorial III–IV y PDF no se reabre aquí.
HANDOFF-TRACE: Codex integrador → figures_pdf (Codex) por collaboration → Claude Code por `claude-bridge` CLI, modelo `sonnet`, modo `review`.

## Decisiones y alcance

- [Inmutable] Revisa solo `scripts/verify_thesis_series_browser.mjs` en el cambio de `inspectNoJs` y su prueba; no reaudites figuras, artículos, PDF ni publicación.
- [Inmutable] La comprobación final sin JavaScript debe seguir exigiendo HTTP 200, ausencia de overflow, navegación y que cada imagen use `-light-mobile.svg`, esté `complete` y tenga `naturalWidth > 0`.
- [Inmutable] Este handoff no autoriza editar, hacer commit, push, publicar, ni relajar umbrales. La publicación autorizada sigue bajo custodia del integrador tras sus gates.

## Artefactos de lectura

- `scripts/verify_thesis_series_browser.mjs:69,540-574,779-803` → helper actual, llamada desde `inspectNoJs`, predicado final y agregación del veredicto.
- `docs/plans/20261108-thesis-production/evidence/claude-nojs-gate-r1/gate-before.mjs` y `gate.diff` → versión anterior y diff acotado desde HEAD; no sustituyen al archivo actual.
- `docs/plans/20261108-thesis-production/evidence/figure-correction/test-nojs-host-poll.mjs` → fixture Playwright real con `javaScriptEnabled: false`, SVG de 800 ms y otro de 2.000 ms.
- `docs/plans/20261108-thesis-production/evidence/figure-correction/r4-nojs-host-poll-falsification.json` → resultado del fixture: iniciales incompletas; imagen lenta lista en 810 ms; otra no lista en 350 ms; exit 0.
- `docs/plans/20261108-thesis-production/evidence/figure-correction/r4-post3-browser-public-incomplete.json` y `verify-thesis-post3-browser-debug.log` → observación de bloqueo anterior: ocho filas sin fallas, `image.complete=false`, sin salida después de entrar al `evaluate` de la promesa; interrupción externa SIGINT exit 130. Esto **no** es un rojo propio del gate; es un bloqueo observado, sin recibo final.
- `inputs.json` → hashes SHA-256 de los archivos exactos anteriores, briefing y cualquier recibo congelado incluido. Comprueba vigencia; un cambio invalida este dictamen.

## Preguntas adversariales

1. ¿El nuevo helper sondea `image.complete` desde Node y termina en 15.000 ms aun si la imagen no completa, sin depender de callbacks `load`/`error` o `setTimeout` ejecutados dentro de la página con JavaScript apagado?
2. ¿El `Promise.race` de `bounded` cubre una llamada `image.evaluate` estancada? Examina efectos de promesa pendiente, cierre de contexto y costo máximo por imagen. Una excepción debe producir `false`, y el predicado final debe reprobar una imagen rota o incompleta.
3. ¿La prueba distingue la corrección de un helper trivial que devuelve siempre true o siempre false? Contrasta el caso retrasado listo con el caso que no está listo al vencimiento y la verificación `naturalWidth`. Distingue el bloqueo previo exit 130 de un mutante rojo específico; si falta falsación decisiva, marca `REQUEST_CHANGES` o límite explícito según severidad.
4. ¿El diff conserva exactamente el predicado final y los demás gates, sin alterar rutas, figuras, hashes ni cobertura? Revisa que el nuevo export no abra una vía productiva o un efecto lateral no previsto.
5. Los gates públicos III/IV completos aún no eran recibos finales al fijar este snapshot. Dictamina solo el mecanismo y la prueba disponibles; no afirmes aprobación de salud pública actual desde esta evidencia. El integrador verificará 32/32 de cada post por separado.

## Salida requerida

Primera línea `REVIEW_VERDICT: APPROVE` o `REVIEW_VERDICT: REQUEST_CHANGES` para **este cambio acotado**. Hallazgos en una línea: `[SEV] archivo:línea → problema → corrección (evidencia)`. Separa hechos observados, deducciones, inducciones e hipótesis; para una hipótesis material aporta evidencia discriminante y condición de descarte. Declara qué leíste, qué no ejecutaste, hashes del snapshot comprobados, alcance de la aprobación y riesgos residuales. Cierra con `PLAN_STATE v2:`, `HANDOFF-TRACE:` y `MODEL-REPORT:`. No edites archivos.
