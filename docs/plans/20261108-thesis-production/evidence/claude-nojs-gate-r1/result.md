REVIEW_VERDICT: APPROVE

Alcance: solo el mecanismo y la prueba de `inspectNoJs`. La aprobación vale con dos límites explícitos (L1 y L2, abajo). No acredita la salud pública actual de III ni de IV.

## Hallazgos

- `[LOW]` `test-nojs-host-poll.mjs:41` → el control rojo se limita a un snapshot del bloqueo anterior (exit 130). No hay mutante ejecutado del helper nuevo (`return true` o `return false`) → opcional: correr los dos mutantes y registrar que el fixture reprueba (L1).
- `[LOW]` `verify_thesis_series_browser.mjs:546-548` → `bounded` rechaza la promesa pero no cancela el `evaluate` pendiente. Ese `evaluate` queda huérfano hasta que `context.close()` lo rechaza en el `finally` de `inspectNoJs:576`, y ese rechazo no queda sin manejar porque `Promise.race` ya está enlazada → sin cambio requerido; coste residual acotado (L2).
- `[INFO]` `verify_thesis_series_browser.mjs:540` → `export` nuevo, sin efecto lateral. `main` ya estaba exportado, y los wrappers `verify_thesis_post3_browser.mjs:2` y `verify_thesis_post4_browser.mjs:2` solo importan `main`. Importar el módulo no ejecuta nada.

## Respuestas

| # | Pregunta | Veredicto | Evidencia |
|---|---|---|---|
| 1 | ¿Polling desde Node, con tope de 15.000 ms, sin callbacks dentro de la página? | Sí | `:540-553`; `evaluate((node) => node.complete)` es síncrono, sin `load`, `error` ni `setTimeout` en la página. El bucle usa `deadline` y `Date.now()` del lado Node. |
| 2 | ¿`Promise.race` cubre un `evaluate` estancado? | Sí | `:546-548` rechaza a los `remaining` ms y el `catch` devuelve `false`. |
| 3 | ¿La prueba distingue la corrección de un helper trivial? | Sí, con L1 | Ver abajo. |
| 4 | ¿Se conservan el predicado final y los demás gates? | Sí | Ver abajo. |
| 5 | ¿Se afirma salud pública? | No | Fuera de alcance, como pidió el briefing. |

**P2, coste por imagen.** El peor caso es ≈15.000 ms más el tiempo de `scrollIntoViewIfNeeded` y del `evaluate` de `loading = 'eager'`. Esos dos `evaluate` no están acotados por `bounded`, pero Playwright aplica sus propios timeouts a las acciones de locator y el contexto sigue acotado por el cierre.

**P3, qué distingue el fixture.**
- Un helper que devuelve siempre `true` falla: `slowInitial=false` y `neverReadyWithin350Ms` saldría `true`.
- Un helper que devuelve siempre `false` falla: `slowReady` saldría `false`.
- Un helper sin espera real falla por `slowElapsedMs >= 500` (810 ms observado).
- `naturalWidth === 100` verifica que la imagen cargó de verdad.

**P4, diff acotado.** `gate.diff` toca solo el bloque de espera. El predicado `page.evaluate(...)` con `-light-mobile.svg`, `complete`, `naturalWidth > 0` queda idéntico, y lo mismo vale para `noJsFailures` (`:779-780`) y `status` (`:789-790`). No cambian rutas, figuras, hashes ni cobertura.

## Epistemología

- **HECHO:** el fixture da PASS con `slowElapsedMs=810` y `neverElapsedMs=351`, y el archivo actual tiene el sha del `inputs.json`.
- **HECHO:** el log de depuración muestra 8/8 filas sin fallas y luego `evaluate start 0` sin salida posterior.
- **DEDUCTIVO:** el predicado final sigue evaluando `complete && naturalWidth > 0`. Una imagen incompleta o rota reprueba el gate, y el helper solo retrasa ese juicio y nunca lo fuerza a `true`.
- **INDUCTIVO:** n=1 corrida del fixture, ya que el repositorio solo registra una. Una espera de 810 ms contra un tope de 3.000 ms deja margen suficiente, pero no se midió la varianza.
- **ABDUCTIVO:** el cuelgue anterior se debe a que la promesa `load`/`error` dentro de la página nunca se resolvía con JS desactivado y sin evento.
  - Evidencia discriminante: la traza se detiene exactamente al entrar al `evaluate` de la promesa.
  - Condición de descarte: que el polling Node-side también se estanque en el gate público completo.
  - La hipótesis es plausible, pero no está probada contra el sitio real, porque el rojo es un snapshot del bloqueo y no un mutante ejecutado.

## Límites y riesgos residuales

- **L1.** No hay falsación con mutantes ejecutados del helper. Lo cubre el razonamiento sobre el fixture (P3), pero no una corrida.
- **L2.** El `evaluate` huérfano tras un timeout depende de `context.close()` para liberarse.
- **L3.** El PASS del fixture es una corrida única y usa `/usr/bin/brave` con rutas absolutas, así que no es portable a CI.
- **L4.** El gate público 32/32 de cada post sigue pendiente de recibo del integrador.

## Revisado y no ejecutado

- **Leí:** el helper (`:540-553`), `inspectNoJs` (`:555-577`), el agregado (`:779-806`), el wrapper `main` (`:612-616`), `gate.diff`, el fixture, el JSON de falsación y el log de depuración.
- **No ejecuté:** el fixture, el gate público ni mutantes.
- **Hashes comprobados:**
  - Coinciden: el script actual `a575bcc1…`, los tres archivos de `claude-nojs-gate-r1/` (gate-before, gate.diff, briefing) y los cuatro de `figure-correction/` (test, JSON de falsación, JSON incompleto, log).
  - Sin recibo congelado incluido.
  - El snapshot está vigente.

PLAN_STATE v2: pb-20261108T003705315Z-fc127547 rev24; D9/P4 siguen abiertos solo por el gate público; sin cambios de estado desde esta revisión.
HANDOFF-TRACE: Codex integrador → figures_pdf (Codex) → Claude Code (`claude-bridge`, `sonnet`, modo `review`); dictamen devuelto al integrador, solo lectura, sin ediciones.
MODEL-REPORT: claude-sonnet-5-5 (alias `sonnet`), solo herramientas de lectura; sin archivos modificados.
