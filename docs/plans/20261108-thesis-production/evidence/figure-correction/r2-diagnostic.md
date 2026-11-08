# QA visual local IV tras REQUEST_CHANGES de Claude

PLAN_STATE v2: `pb-20261108T003705315Z-fc127547`; D9 revisión definitiva de Claude pendiente sobre el conjunto corregido.
HANDOFF-TRACE: Claude Code → Codex integrador → adaptador EN vía collaboration; `figures_pdf` produjo SVG y guard Matplotlib, `implement_site` conserva QA funcional.

| Etapa | Hecho medido | Recibo |
|---|---|---|
| Antes de r2 | 64/64 PASS era compatible con rótulos que tocaban el marco porque no se registraban espinas. | `visual-local-final.json`; `diagnostic.md`. |
| Primer render con espinas | 60/64 PASS; cuatro variantes EN no superaron el margen de 1,5 px entre `longitudinal-value-0-1` y `longitudinal-spine-1-left`. Bboxes DOM a 620 px: etiqueta izquierda `−9689,3408`, espina `−9690,6631`; separación positiva 1,3223 px, sin intersección estricta. | `r2-visual-local.json`; `/tmp/codex-visual-r2-shots/iv-annex-en-light-1440-fig-post4-2.png`. |
| Render corregido final | Playwright exit 0: 64/64 filas PASS, 128 capturas; contraste mínimo texto 5,73:1, SVG 4,67:1; texto SVG mínimo 10,28 px. Misma holgura DOM EN clara a 620 px: 6,7109 px tras desplazar el valor. | `r2-final-visual-local.json`; `/tmp/codex-visual-r2-final-shots/`. |
| Falsación final | Seis fixtures exit 1 `EXPECTED_FAIL`; baseline limpio. Marco y barra propia producen **una sola** falla `label-mark` cada uno, con `isolatedCollision=true` y `wouldPassWithoutTargetMark=true`. | `r2-final-fixture-svg-*.json`. |

El gate exige ocho IDs de espinas por familia (`selection`, `longitudinal`, `causal`; dos paneles × cuatro bordes) y mide sus trayectorias SVG en coordenadas del navegador, junto con IC, puntos, barras y líneas GATE. La ausencia de IDs causa fallo de cobertura; no cuenta como falsación geométrica. La fixture de marco traslada `selection-value-a-1` sobre `selection-spine-a-top` sin tocar otra marca o texto. La de barra propia traslada `longitudinal-value-1-2` dentro de `longitudinal-bar-1-2` sin tocar barra vecina; solape medido 28,86 × 17 px. Los cuatro fixtures previos (IC/punto, barra vecina longitudinal, barra vecina PAES y línea GATE) mantienen `EXPECTED_FAIL`.

Límites: el detector geométrico no compara entre sí títulos, ticks y leyendas sin IDs, ni registra rejilla o trazos sin IDs; tampoco verifica contenido científico ni proximidad editorial sin intersección. Las ocho capturas en `curated-r2/` cubren cuatro variantes de Figura 1 y dos por cada figura del anexo, con ES/EN, claro/oscuro y 320/1.440 px. Las otras 120 capturas permanecen en `/tmp/codex-visual-r2-final-shots/`. Inspección visual puntual de Figura 1 EN clara 1.440, causal EN clara 320 y longitudinal EN oscura 1.440: el rótulo superior queda dentro del marco, los valores G1 están separados y `56.6%` tiene espacio visible frente al marco. Esa inspección no sustituye la revisión adversarial de Claude.

SHA-256 del manifiesto final `assets/images/tesis-post4/manifest.json`: `a29020d552c24eb42bff845dc090629befd86e7bd06a728d492493a543e972d8`. SHA-256 del gate `scripts/verify_thesis_visual_quality.mjs`: `c74e8a248776d56bd97e33abcdc0a1292c0ee3c7f3b4a3eee03d72d7200a929c`. `node --check` y `git diff --check`: exit 0. Sin commit, push ni publicación.
