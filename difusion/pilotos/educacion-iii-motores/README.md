# Educación III — piloto de composición nativa

Estado: piloto cerrado. Elección delegada por el usuario: HTML/CSS + Chromium, promovido a `difusion/paquetes/costos-cierre-escolar-trayectorias/linkedin/`. PDF final entregado por Telegram; sin publicación en LinkedIn ni certificación «HIGH END». La primera ronda fue rechazada por semejanza excesiva y defectos de diagramación; permanece en `out/revision-01/`.

## Abrir

- Galería: `out/native/index.html` (selector de página, cuatro PDF, notas descargables, tecnologías identificadas explícitamente).
- PDF: `out/native/Typst.pdf`, `Beamer.pdf`, `HTML-CSS.pdf`, `Scribus.pdf`. Los identificadores internos A–D permanecen en fuentes y receipts.
- Fuentes editables: `A.typ`, `B.tex`, `C.html`, `D.sla` en el mismo directorio.
- El tablero de Kitty lee `state.json`; su panel queda abierto.

## Qué se está comparando

| Código | Motor | Composición implementada | Edición |
|---|---|---|---|
| A | Typst 0.15.1 | Stack/grid, espacio fraccional, párrafos e intervalos vectoriales | Fuente declarativa `.typ`; generador `native_typst.py` |
| B | Beamer + LuaLaTeX | Minipages, párrafos TeX y gráficos TikZ; cifras en columnas | `.tex`; generador `native_beamer.py` |
| C | HTML/CSS + Chromium | Grid/Flex, tarjetas, SVG y exportación PDF directa | `.html`; generador `native_html.py` |
| D | Scribus 1.6.6 | Marcos, párrafos nativos, estilos y fondo maestro; texto y gráfico en columnas | `.sla` editable en Scribus; `native_scribus.py` |

Las cuatro usan el mismo contenido, Fira Sans y paleta oscura. El estilo visual se puede portar entre herramientas: preferir una composición no prueba que su motor sea superior. La segunda ronda ya no utiliza `render.py`, `Scene` ni saltos de línea calculados por PIL. El antiguo generador queda para explicar/reproducir la ronda rechazada.

## Fuente y alcance

`content.json` contiene las nueve láminas; `source-lock.json` congela contenido, hero, logo y post. El post vigente es `_posts/2026-10-23-costos-cierre-escolar-trayectorias.md`, SHA-256 `bad473d666d7e60fe2ea231adddf5c78e054fe28339380a2896293c9455b9c3e`.

Se reconcilió un cambio concurrente limitado al front matter de audio; el cuerpo científico permanece idéntico. Evidencia: `out/native/source-metadata-refresh.json`.

Se preservan las diferencias descriptivas, los niveles de confianza, la exclusión de 2024 en el seguimiento de dos años, los contraejemplos y los límites causales. La primera persona corresponde al autor del artículo. El carrusel antiguo archivado no es fuente científica vigente. El piloto no modifica el post, no incluye audio ni añade una versión inglesa.

## Reproducir en este equipo

Desde este directorio:

```sh
python3 native_build.py all
python3 native_verify.py --receipt out/native/qa.json
python3 native_previews.py
python3 negative_probes.py
python3 build_gallery.py
```

Para editar contenido: modificar `content.json`, contrastar el cambio con el post y ejecutar `python3 freeze.py` solo después de esa revisión; luego regenerar. Para cambiar diseño: editar el generador del motor correspondiente. Los archivos generados pueden editarse directamente, pero una regeneración los sobrescribe; guardar una copia si se desea conservar una edición manual de `.sla`, `.tex`, `.typ` o `.html`.

Prueba realizada: al título de la lámina 4 se añadió ` en las trayectorias escolares` en una copia aislada:

```sh
python3 native_build.py all --content out/native/stress/long-title.json --output out/native/stress
python3 native_verify.py --root out/native/stress --content out/native/stress/long-title.json --receipt out/native/stress/qa.json
```

No se ajustó el diseño para esa copia. Los cuatro pasan ese caso. Un ejemplo no demuestra robustez frente a textos arbitrarios; Scribus utiliza marcos de altura fija y requiere revisar desbordamientos. HTML tiene alto fijo por lámina y también puede recortar contenido excesivo.

## Dependencias y portabilidad

Este piloto es reproducible en el equipo actual, no un paquete autosuficiente para cualquier sistema. Necesita Python con Pillow/pypdf, Poppler, LuaLaTeX/Beamer/fontspec/TikZ, Node y Playwright, Fira Sans y Bubblewrap. Chromium se toma del navegador instalado para agent-browser. `html_render.mjs` utiliza el módulo Playwright local de penta-agent, bloquea solicitudes HTTP(S) y no usa un perfil del usuario.

Typst y Scribus fueron extraídos de paquetes oficiales Arch a `.tools/root`, con firmas verificadas contra el keyring local; los paquetes y firmas quedan en `.tools/packages`. No se instaló software global. Scribus utiliza un overlay de `/usr` de solo lectura dentro de Bubblewrap, más cachés aisladas. LuaLaTeX usa `.tools/tex-cache-ready` con la caché de nombres de fuentes previamente disponible.

`out/` y `.tools/` están ignorados por Git. No eliminar esos directorios si se necesitan los PDF o dependencias locales. Para trasladar el piloto deben prepararse dependencias equivalentes y adaptar las rutas del navegador, fuentes y Playwright. No se afirma portabilidad probada.

## Evidencia y límites

- `out/native/qa.json`: 36 páginas, contenido esperado, cifras, fuentes incrustadas, enlaces y límites de página.
- `out/native/probes/summary.json`: cifra 9,58→9,59, página omitida y PDF solo imagen rechazados; salida roja real `1`, retorno verde `0`.
- `out/native/stress/qa.json`: prueba común de título más largo.
- `out/native/*.receipt.json`: hashes, comandos y tiempos de generación. Una ejecución con cachés; no es un benchmark de productividad.
- `out/native/visual-review.json`: revisión visual y sus límites.

El detector de colisiones es una heurística sobre la región central de cajas de palabras PDF; no certifica ausencia total de choques ni verifica semánticamente la ciencia. Los criterios numéricos y anchors se contrastan con el archivo congelado, pero no reemplazan la lectura editorial. Typst y Chromium producen estructura etiquetada; eso no acredita orden de lectura accesible ni conformidad PDF/UA. Beamer y Scribus no están etiquetados en esta configuración.

Los fondos maestros de Scribus están implementados. La API fallaba después de cerrar la maestra hasta ejecutar explícitamente `gotoPage(1)`; el encabezado se mantiene en marcos normales. Quedan advertencias de plugins OSG opcionales no usados por este carrusel. No se midió edición humana en la interfaz de Scribus ni se probó carga real en LinkedIn.

## Referencias de la selección

- [Matthew Butterick: máximas de composición](https://practicaltypography.com/maxims-of-page-layout.html): referencia tipográfica; no aval de estos PDF ni recomendación de motor.
- [Creative Bloq: alternativas a InDesign](https://www.creativebloq.com/features/indesign-alternatives): fuente editorial para incluir Scribus como alternativa de autoedición; no benchmark de este piloto.
- [Typst: configuración de página](https://typst.app/docs/guides/page-setup/): documentación del motor.
- [Playwright: exportación PDF](https://playwright.dev/docs/api/class-page#page-pdf): documentación del flujo HTML nativo.

## Decisión final y rollback

Se revisaron legibilidad a 390 px, jerarquía, densidad, cortes, diagramas y acabado. Se eligió HTML/CSS por control editorial y reutilización del flujo existente. No se midieron horas de edición humana: menor costo de migración es una inferencia, no un benchmark. El título largo no discrimina entre candidatos. La justificación y condiciones para reabrir la decisión están en la referencia nativa de publicacion-externa.

Rollback: volver a los artefactos de revisión 1 para inspección histórica, o retirar únicamente esta carpeta del piloto. No restaurar el carrusel histórico como contenido vigente ni tocar fuentes canónicas. Los commits locales fueron autorizados posteriormente; push y publicación en LinkedIn permanecen fuera del alcance.
