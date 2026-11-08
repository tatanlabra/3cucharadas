REVIEW_VERDICT: APPROVE

Aprobación técnica acotada a lo que pude observar. Los tres hallazgos ALTA quedaron resueltos con margen visible en las capturas y en el código. Persisten cuatro debilidades menores, ninguna bloqueante (ver más abajo). No ejecuté Playwright, el generador, pytest ni los mutantes: todo lo que sigue es lectura de código, recibos, hashes y capturas.

## Hallazgos previos

| Hallazgo previo | Estado | Evidencia |
|---|---|---|
| [ALTA] Título del peldaño 1 de Fig. 1 cruza el borde superior | Resuelto | `352_post4_visuals.py:445` pone el título en `y+2,15 = 15,75` con `ylim` superior de `17,25` (`:465`), es decir 1,5 unidades de holgura. Las capturas `iv-article-{es-light-320, es-academic-night-1440, en-light-1440, en-academic-night-320}` y `pdf-figure1-r4.png` muestran el título bajo el marco en ambos paneles. |
| [ALTA] `−0,1` causal pegado al borde superior | Resuelto | `352_post4_visuals.py:831,850` pone el rótulo en `6,3` con `ylim` superior de `9,0` (antes `7,5`). Las capturas `iv-annex-es-academic-night-1440-fig-post4-3` e `iv-annex-en-light-320-fig-post4-3` lo muestran dentro del marco. |
| [ALTA] El marco de los ejes no era una marca registrada | Resuelto | Productor: `_register_spines` (`:260-268`) registra 4 espinas por panel, con cobertura exigida `(20,38)`, `(…,…)` y `(27,20)` en `:474,643,865`. Falla cerrado ante conteo distinto (`:236-239`). DOM: `verify_thesis_visual_quality.mjs:192,198,206` exige 8 espinas por familia y devuelve `unmeasured` si faltan IDs. |
| [MEDIA] Fixture de barra propia no discriminaba | Resuelto | `r2-final-fixture-svg-own-bar-overlap.json`: una sola falla (`longitudinal-value-1-2` / `longitudinal-bar-1-2`, solape 28,86×17 px), `isolatedCollision=true`, `EXPECTED_FAIL`. Antes eran 1,93 px y además disparaba una barra vecina. |
| [MEDIA] API `allowed` muerta y docstring engañoso | Resuelto | `rg allowed` y `rg 'may sit inside'` sobre 352, 336 y los tests no devuelven nada relevante. El docstring actual (`:235`) dice que falla ante cruces con etiquetas, marcas o marcos. |
| [MEDIA] Asociación de lectura dependiente del color | Parcial | G1 `−12,3` / `−11,5` ahora están separados en horizontal y vertical en las capturas a 320 y 1440 px. PAES: los ámbar siguen flotando en un carril superior (`:831`), lejos de barras casi nulas, y se atribuyen solo por color y leyenda. Fig. 1: el título del peldaño siguiente queda a 26–30 px del IC anterior, contra 18–22 px de su propio valor. Es legible, con margen estrecho a 320 px. |
| [BAJA] Guards con tolerancias distintas | Persiste, declarado | Productor: relleno de 8 px a la espina. DOM: 1,5 px y 2 px. No lo cambiaron. |
| [BAJA] Recibo funcional no vinculaba el SVG final | Resuelto | `r4-post4-browser-local.json`: 32/32, `manifestBound`, sha `d3f354f8…`, igual al manifiesto actual. `/tmp/codex-thesis-production-site` es byte-idéntico a `assets/images/tesis-post4` (51 archivos) y `tesis-post3` (69 archivos). |
| [BAJA] Espacio antes del punto en `(CSV).` | Resuelto | El texto del PDF dice `(CSV).` en las 3 figuras. `test_post4_pdf_composition.py:115-116` lo asegura. |
| [BAJA] Prosa IV ES: `−2,64` sin intervalo; figura 2 solo en el anexo | No revisado | Es contenido editorial, fuera de este encargo. |

## Falsaciones

1. **Marcos.** Las espinas están registradas en el productor y en el DOM. Cada uno de los cuatro bordes de ambos paneles se prueba con relleno de 8 px en el productor y 1,5 px en el DOM. La inspección visual de las ocho capturas coincide con eso. No medí bboxes por mi cuenta.
2. **Fixtures.**
   - Los seis recibos `r2-final-fixture-svg-*` salen `EXPECTED_FAIL` con línea base limpia.
   - El del marco y el de barra propia tienen exactamente 1 falla, `isolatedCollision=true` y `wouldPassWithoutTargetMark=true`.
   - En el productor, `verify_post4_visual_geometry.py` solo sale 1 si el mensaje coincide con el esperado (`:173`). Setup devuelve 3 y mutante sobreviviente devuelve 2.
   - `generator-validation-r3.json` registra los 6 rojos con exit 1 y el verde de 24 variantes. `r4` repite el verde de 24.
3. **Excepciones.** No hay API `allowed` ni lista blanca en `verify_thesis_visual_quality.mjs`. Hay tolerancias numéricas explícitas (`hit.x>2 && hit.y>1.5`, `>2 && >2`, 1,5 px). Si falta cobertura, devuelve `unmeasured`; si los conteos no calzan, no pasa.
4. **Fig. 1.** Título, valor e IC del mismo peldaño se leen juntos. PAES y G1 se atribuyen a su serie sin tocar barra, línea ni marco.
5. **Ancho y PDF.**
   - CSS: `#fig-post4-1 {width:100%}` (`main.scss:2217`).
   - PDF, sha `d866c2d2…`: 24 páginas. `pdfimages` muestra una imagen a página completa (p. 5) y otras en p. 14 y 17, o sea tres figuras.
   - `test_post4_pdf_composition.py:136-171` cubre el salto de página dedicado.
   - Las seis tablas y el sha del anexo vienen del manifiesto, que el snapshot final verifica. Las tablas no las conté en el PDF.
6. **III.** `outputs/post3_visuals` y `assets/images/tesis-post3` son byte-idénticos (78 archivos), y el sitio servido también (69). El fixture `effective-clusters-drift` (`verify_thesis_post3.rb:951`) muta todas las apariciones de `21.1` en el artículo y el anexo EN. `r3-effective-clusters-receipt.json` da rojo con `POST3_INVALID: clusters efectivos ausentes en: 21.1` y verde 3 runs / 393 assertions. No se superpone con la cobertura de IV.
7. **Matriz, recibos y rótulos longitudinales.**
   - `r4-final-visual-local.json`: PASS, 64/64, 128 capturas, contraste mínimo de texto 5,73, SVG 4,67, texto SVG mínimo 10,28 px.
   - III: el primer run `r4-post3-browser-local.json` quedó FAIL por `ERR_NETWORK_CHANGED`, con `groupFailures` vacío y 32 filas sin falla propia. El retry da PASS 32/32 con manifiesto `3c207de3…`, igual al actual.
   - Rótulos longitudinales: ES y EN usan «composición», «depurados» / «screened», y el pie dice que la figura «no verifica el estado jurídico». No encontré «sesgo» ni «bias» en los SVG longitudinales ni en `manifest.json`, y ninguna variante afirma cierres jurídicos ni validación de la regla.

## Límites y debilidades que persisten

- **Mutantes no repetidos tras la última edición de 352.** El gate DOM tiene el mismo sha (`c74e8a24…`) que cuando se corrieron los 6 mutantes r2. `352_post4_visuals.py` se tocó a las 23:41, después de los mutantes del productor (23:35). Lo cubre pytest (19 passed, 23:45), que llama directamente a `_assert_visual_geometry`, pero los `--inject-*` de punta a punta no se volvieron a correr. No puedo comprobar sin diff que el guard no cambió.
- **`wouldPassWithoutTargetMark` es un alias de `isolatedCollision`.** Se deduce de «falla única», no de una corrida contrafactual sin la marca (`verify_thesis_visual_quality.mjs:458-475`). La deducción es razonable, pero no es una prueba independiente.
- **Fixture `21.1` solo muta EN.** ES (`21,1`) queda cubierto por el predicado (`verify_thesis_post3.rb:561`), pero no por el fixture. Además `body.include?("21.1")` acepta subcadenas como `121.1`.
- **Aprobación solo de lectura:** no abrí Playwright, no generé figuras. Los pares de texto sin rol, la rejilla y la semántica científica no equivalen a geometría; el gate compara etiquetas con texto sin ID (`otherText`), pero no texto sin ID contra texto sin ID.
- **Sin verificar:** justificación con `hyphens:auto` a 320, 390, 768 y 1440 px en los párrafos del artículo (solo vi capturas de figuras), fuentes incrustadas en el SVG frente a Playwright, y la paridad numérica ES/EN de tablas.

## Epistémico

- **HECHO:** 135/135 hashes de `inputs-final.json` vigentes, PDF y manifiestos con los sha citados, sitio servido idéntico a los assets, ocho capturas curadas y `pdf-figure1-r4.png` abiertos.
- **DEDUCTIVO:** el gate DOM tiene el mismo sha que en los mutantes r2 ⊢ esos rojos siguen valiendo para él. Exit 1 en el verificador del productor solo ocurre con el mensaje esperado ⊢ los 6 rojos son específicos.
- **INDUCTIVO:** los tres defectos previos nacieron de marcas no registradas; las tres familias ahora registran espinas y las cuatro capturas de Fig. 1 más las dos causales las muestran con margen.
- **ABDUCTIVO:** la causa previa fue `ylim` fijado sin margen para el texto agrandado por `_readable_text`. Evidencia discriminante: las capturas finales y los nuevos `ylim` (17,25 y 9,0). Se descarta si algún tema o idioma muestra el rótulo tocando el marco en una variante que no vi (por ejemplo 768 px).

Capturas abiertas: `iv-article-es-light-320`, `iv-article-es-academic-night-1440`, `iv-article-en-light-1440`, `iv-article-en-academic-night-320` (Fig. 1), `iv-annex-es-academic-night-1440-fig-post4-3`, `iv-annex-en-light-320-fig-post4-3` (causal), `iv-annex-en-academic-night-1440-fig-post4-2`, `iv-annex-es-light-320-fig-post4-2` (longitudinal), más el raster `pdf-figure1-r4.png`.

PLAN_STATE v2: pb-20261108T003705315Z-fc127547 rev17; D9 revisión técnica visual: APPROVE de solo lectura. No se editó ningún archivo, no hubo commit, push, envío ni difusión. La publicación sigue bajo custodia del agente raíz, que debe ejecutar el source-health actual antes del push.
HANDOFF-TRACE: Claude Code (`claude-bridge`, solo lectura) → Codex integrador; revisión de `../claude-correction/result.md`, sin escrituras.
MODEL-REPORT: sonnet (claude-sonnet-5-5), modo plan de solo lectura, sin subagentes.
