# Revisión adversarial visual y técnica III–IV, ronda r2

Estado documental: LISTO tras snapshot `inputs-before.json` y PDF r4.
PLAN_STATE v2: pb-20261108T003705315Z-fc127547 rev17; D8 corrección técnica congelada, D9 revisión Claude pendiente; integración y publicación bajo custodia del agente raíz.
HANDOFF-TRACE: Codex integrador → figures_pdf (Codex) por collaboration → Claude Code por `claude-bridge` CLI, modelo `sonnet`, revisión de solo lectura. La revisión editorial de ocho textos ES/EN corre por separado.

## Encargo y autoridad

Lee completo `../claude-correction/result.md` y resuelve **cada** hallazgo visual/técnico de su `REQUEST_CHANGES`. Examina código y artefactos, no solo recibos. Devuelve dictamen independiente. No edites archivos ni hagas commit, push, envío, despliegue o difusión. La aprobación técnica no autoriza publicación. El snapshot final `inputs-final.json` fija hashes de los insumos; comprueba vigencia antes de dictaminar. `inputs-before.json` es el borrador previo a corregir rutas y adjuntar browser funcional r4.

La revisión editorial completa de las ocho fuentes ES/EN se lleva por separado y obtuvo APPROVE en r4. Aquí revisa el vínculo técnico entre texto IV, figuras y PDF, incluidos los rótulos de procedencia del gráfico longitudinal corregidos después de ese dictamen. El PDF r4 contiene ES IV final; las ocho capturas curadas reflejan las figuras y CSS finales.

## Insumos obligatorios

- Investigación: `../../incubadora/tesis_mae_mejorada/scripts/336_post3_visuals.py`, `352_post4_visuals.py`, `353_render_and_send_post4_pdf.py`, `tests/test_post3_visuals.py`, `tests/test_post4_visual_geometry.py`, `tests/verify_post4_visual_geometry.py` y `tests/test_post4_pdf_composition.py`. Las claves `../../incubadora/tesis_mae_mejorada/…` del snapshot resuelven desde la raíz del blog.
- Figura III: `assets/images/tesis-post3/cohort-series-infographic-*`, incluidos 16 SVG/PNG, CSV y dos `.visual-manifest.json`, más `assets/images/tesis-post3/manifest.json`. Confirma que etiquetas corregidas provienen del productor 336 y coinciden con los derivados; revisa pruebas blog III y el fixture específico de `21.1` en ambas fuentes.
- Figuras IV: `assets/images/tesis-post4/manifest.json` y familias `selection-ladder-*`, `longitudinal-regimes-*`, `causal-ml-heterogeneity-paes-*`; 24 SVG, 24 PNG, tres CSV. Contrasta ES/EN, claro/oscuro y móvil/escritorio sin cambiar cifras, intervalos, ejes, muestras ni CSV científicos.
- Sitio/guardas: `assets/css/main.scss`, `scripts/verify_thesis_visual_quality.mjs`, `scripts/verify_thesis_series_browser.mjs`, `scripts/verify_thesis_post3_browser.mjs`, `scripts/verify_thesis_post4_browser.mjs`, `scripts/verify_visual_assets.rb`, `scripts/verify_thesis_post3.rb`, `scripts/verify_thesis_editorial_delivery.py` y pruebas. CSS abre `#fig-post4-1` al ancho de columna sin invadir TOC; examina la justificación solicitada y legibilidad a 320/390/768/1440 px, no solo la declaración CSS.
- Recibos: `../figure-correction/generator-validation-r4.json`, `r3-source-final.json`, `r3-effective-clusters-receipt.json`, `r4-final-visual-local.json`, seis `r2-final-fixture-svg-*.json`, `r4-post3-browser-local-retry.json`, `r4-post4-browser-local.json` y entrega PDF vigente. El source-health r3 es histórico y root ejecuta el actual antes del push. El primer browser III r4 falló por `ERR_NETWORK_CHANGED`; el retry final dio 32/32. Browser IV dio 32/32. Confirma exits y hashes; recibos históricos no prueban salud actual. Los mutantes r2 prueban guardas cuyo código no cambió en r4; comprueba esa premisa.
- Inspección visual **obligatoria**: abre los ocho PNG de `../figure-correction/curated-r4/` y `../figure-correction/pdf-figure1-r4.png`. Son cuatro Fig. 1 IV, dos longitudinal y dos causal, con móvil/escritorio y temas/idiomas. Abre PDF final si hace falta comprobar paginación, caption o tablas. No sustituyas observación por JSON.

## Falsaciones concretas

1. Los dos fallos altos previos (título del primer peldaño de Fig. 1 y `−0,1` causal frente al borde superior) ¿quedaron dentro de los marcos con margen medido? Comprueba las cuatro espinas de ambos paneles en cada familia, SVG productor y DOM. Un `64/64 PASS` aislado no acredita esos objetos.
2. ¿El fixture del marco falla **por ese marco** y el de barra propia **por su barra**? Exige `isolatedCollision=true`, `wouldPassWithoutTargetMark=true`, `EXPECTED_FAIL` exit 1. Revisa los otros cuatro mutantes: valor/CI, barra longitudinal vecina, barra causal y línea GATE. Verifica el guard productor: verde 24 y seis rojos específicos, con error de setup distinto.
3. ¿Desapareció la API `allowed` muerta y el docstring que permitía rótulos dentro de barra? ¿Hay excepciones amplias de solape? Comprueba que el guard registra marcas y falla cerrado ante conteos/errores.
4. ¿Fig. 1 asocia título, valor e IC del mismo peldaño por proximidad? ¿PAES ámbar/verde y G1 `−12,3`/`−11,5` se atribuyen a su serie sin tocar barra, línea ni marco? Cero colisiones geométricas no prueba legibilidad: juzga capturas a 320 y 1440 px.
5. ¿Fig. 1 usa ancho disponible en web y página dedicada en PDF? ¿PDF conserva tres figuras, seis tablas, anexo, hashes del post/anexo y tres PNG, y `(CSV).` sin espacio antes del punto? Comprueba el raster final.
6. ¿Productor III 336, assets y gate III comparten contenido? El fixture `21.1` debe mutar ambas menciones para rechazar específicamente; separa esa cobertura de IV.
7. ¿La matriz visual y los recibos funcionales r4 vinculan manifiesto SVG actual? Valida cobertura explícita de texto frente a CI/puntos/barras/líneas/espinas, contraste, fuentes y ancho. Distingue el fallo de red transitorio III del retry verde. Inspecciona los rótulos longitudinales ES/EN: ninguna variante debe afirmar sesgo identificado, cierres jurídicamente reales ni validación de la regla de cierre a partir de mera comparación de composición. Señala sin exagerar límites: pares de texto sin rol, rejilla y semántica científica no equivalen a geometría.

## Salida

Primera línea: `REVIEW_VERDICT: APPROVE` o `REVIEW_VERDICT: REQUEST_CHANGES`. Para **cada** hallazgo previo, marca resuelto/parcial/persiste con `archivo:línea` y captura/objeto/recibo discriminante. Separa hechos, deducciones, inducciones e hipótesis; para hipótesis materiales da evidencia discriminante y condición de descarte. Declara cuáles ocho PNG y raster PDF abriste, hashes de snapshot comprobados y límites. Si no puedes leer insumo, déjalo sin verificar. Cierra con `PLAN_STATE v2:`, `HANDOFF-TRACE:`, `MODEL-REPORT:` (modelo real y modo). Solo lectura; no aprobación propia de Codex ni claim de perfección global.
