# QA visual local: posts III y IV

Estado: **PASS local**, artefacto `/tmp/codex-thesis-production-site`, preview `http://127.0.0.1:4005`. La comprobación pública queda pendiente del despliegue.

## Método y resultado

- Matriz: 8 rutas (artículo y anexo III/IV, ES/EN) × 2 temas × 4 anchos (320, 390, 768, 1440 px) = **64 observaciones**.
- Resultado: **64/64 PASS**, HTTP 200 en 64/64; 0 desbordes de documento, 0 elementos principales recortados, 0 imágenes o variantes fallidas, 0 errores de consola/red, 0 fuentes Fira Sans sin cargar.
- Contraste CSS: **16.088 muestras de texto directo**; mínimo **5,73:1**. El fondo efectivo se compone desde `background-color` de los ancestros; 0 muestras con fondo incierto.
- Figuras SVG activas: contraste mínimo de etiquetas frente al lienzo declarado **4,67:1**; texto renderizado mínimo **10,28 px**. La métrica del lienzo no demuestra contraste sobre cada subpanel coloreado: cuatro capturas representativas se inspeccionaron visualmente.
- Capturas: **96 PNG** con fuentes e imágenes cargadas, movimiento reducido y animaciones/transiciones desactivadas; originales en `/tmp/codex-thesis-visual-production`.

## Falsación observada

- `node scripts/verify_thesis_visual_quality.mjs --base-url http://127.0.0.1:4004 --fixture low-contrast --report docs/plans/20261108-thesis-production/visual-falsification.json` → exit **1**, `EXPECTED_FAIL`; baseline sin fallos (104 muestras, mínimo 5,73:1), párrafo perturbado blanco sobre blanco **1:1**, único fallo `text-contrast`. El fixture modificó el DOM en una sesión efímera; no cambió archivos del sitio.
- `node scripts/verify_thesis_post4_browser.mjs --artifact-root /tmp/codex-thesis-production-site --manifest-fixture missing-csv` → exit **1**, `EXPECTED_FAIL`; baseline de 51 entradas válido, copia efímera sin `selection-ladder-data.csv` detectada como `artifactMismatches`.
- Verdes tras falsación: Post III **32/32** en `visual-manifest-post3-green.json`; Post IV ES **16/16** en `visual-manifest-green.json`, ambos con manifest enlazado al artefacto, SHA y bytes correctos.

## Capturas inspeccionadas

- [III, artículo ES, oscuro, móvil](visual-iii-article-es-dark-mobile.png).
- [III, anexo EN, claro, figura](visual-iii-annex-en-light-figure.png).
- [IV, artículo EN, claro, escritorio](visual-iv-article-en-light-desktop.png).
- [IV, anexo ES, oscuro, figura móvil](visual-iv-annex-es-dark-figure-mobile.png).

Datos completos: [visual-production-local.json](visual-production-local.json). El script audita el resultado renderizado y no reemplaza la revisión científica, editorial ni una comprobación del dominio público después de publicar.
