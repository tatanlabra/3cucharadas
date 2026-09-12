# QA local de héroes y tarjetas

- Alcance: 20 posts bilingües, héroe, título, metadatos, procedencia y tarjetas; no certifica figuras del cuerpo, rendimiento ni conformidad WCAG de la página completa.
- Matriz final: 80/80 casos en 390 y 1440 px CSS, DPR 1, temas reales `light` (academic-day) y `academic-night`, activados mediante el botón del sitio.
- Cada caso: un h1, imagen cargada y responsive correcta (800/1600), preload idéntico, pie y declaración presentes, procedencia conforme al catálogo sin atribuir herramientas desconocidas, sin desborde y apertura por teclado del detalle con foco visible. Axe 4.12.1: cero violaciones y cero incomplete en los componentes incluidos.
- Adicionales: ocho casos de títulos CASEN ES/EN a 320 px o reflujo equivalente al 200%, ambos temas; sin desborde y axe cero violaciones/incomplete.
- Control falsable: duplicar h1 solo en DOM detectó 2; retirar la mutación restauró 1 y SHA idéntico (`negative-control.json`).
- Revisión visual: cuatro hojas de contacto con los 80 encabezados, títulos completos; capturas individuales de títulos largos y archivo estable legibles. Se conservan 113 capturas individuales y cuatro hojas PNG.

## Tarjetas: rojo y recuperación

| Evidencia | Resultado |
|---|---|
| Build original, inicio ES/EN y relacionadas ES | `srcset` ausente para imágenes heroes-v2; `cards-before-red.json` conserva el rojo. |
| Build nuevo tras corrección del agente raíz | 24 vistas ES/EN, 390/1440, claro/oscuro: imagen/título/desborde correctos; inicio y relacionadas cargan realmente teaser-mobile-640x360.webp con srcset 640/1280. |
| Axe inicial de tarjetas | 23/24 vistas verdes; archivo ES 1440 oscuro produjo contraste transitorio en diez metadatos de tiempo de lectura. Se conserva el rojo en `cards-after.json`. |
| Revisión focal estable del archivo | Cero violaciones e incomplete; `archive-es-night-settled-axe.json` y captura `screenshots/archive-es-1440-night-settled.png`. No se repitió la matriz completa después. |

## P2 conservado: contraste durante cambio de tema

- Observado: axe detectó contraste 2,38:1 en metadatos, color #545454 sobre #161616, umbral 4,5:1. La lectura estable posterior pasó.
- La muestra de transición registra cambios entre 0 y 387 ms; CSS declara 0,2 s, pero la muestra no permite afirmar que todo quedó estable a los 200 ms ni determinar duración total del defecto.
- La regla de metadatos nocturnos y el archivo theme-toggle.js son idénticos frente al baseline Git bf1ff5ac (`transition-baseline-comparison.json`). Esas fuentes preexistían; no se reprodujo el runtime del baseline y la equivalencia del defecto histórico permanece sin medir.
- Disposición: deuda P2 de transición global, conservada con evidencia; no se amplió la modificación de CSS. La comprobación estable y la carga responsive correcta satisfacen el alcance focal de tarjetas. No se afirma ausencia de defectos transitorios.

## Límites y vínculo de evidencia

- Zoom: Control+0 y cinco Control+Equal no cambiaron viewport/DPR/escala (`native-zoom-probe.json`). Se verificó reflujo equivalente con 720×450 px CSS y DPR 2 (1440×900 físicos), aceptado para este criterio; no se afirma zoom nativo del navegador.
- Matriz de héroes sobre `/tmp/3c-heroes-integrated-site` (build 11,326 s); tarjetas sobre `/tmp/3c-heroes-cardfix-site` (17,852 s), con `--disable-disk-cache`. Avisos Sass permanecen en logs.
- `freeze.json` vincula fuentes, selectores HTML, metadatos, piezas del catálogo y bytes de imágenes. CSS entre ambos builds es idéntico. Reutilizar solo si esas entradas y fragmentos permanecen iguales; cambios posteriores en figuras del cuerpo no están cubiertos.
- `commands.jsonl` conserva invocaciones exploratorias y finales; la matriz autoritativa es `matrix.json`. El intento preliminar con nombre de tema inyectado fue reemplazado por la matriz con botón real; archivos preliminares `.superseded` quedaron solo en /tmp.
- Las verificaciones axe son acotadas y no sustituyen evaluación manual integral. No se hicieron mediciones de rendimiento en esta tarea.
- Sesión propia `heroes-all` y servidor local 4038 cerrados; no se modificó producto durante QA.
