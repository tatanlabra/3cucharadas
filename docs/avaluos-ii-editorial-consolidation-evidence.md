# Avalúos II — consolidación editorial y arte de portada

Corte: 11-09-2026, America/Santiago. Cumplimiento editorial F10 y producción visual F11; preparación local. Las dependencias fiscales F3/F4 y el benchmark cartográfico F9_2 permanecen abiertos.

## Resultado editorial comprobado

- La nueva base del usuario se conserva byte a byte en `docs/editorial-sources/avaluos-ii-revisado-20260911.md`; SHA-256 `e1c1a376390a44d5f08ae521668ea05fbc7a2f09af58f782c04682cbb6edce2c`.
- Solo hay un borrador por idioma para el ref canónico; ambos mantienen `published: false` y fecha `2026-09-11 00:00:00 -0300`.
- Se consolidaron los siete ajustes de la revisión: escenario/deuda, motivación tributaria, campamento/exención, sesgo condicional, bibliografía, fuente única y fecha.
- El inglés traduce esta versión completa. Comparación actual: 20 filas numéricas, 80 valores y 12 referencias coinciden entre ES/EN; cambia el formato de miles/decimales.
- El manuscrito no convierte materialidad en tasación, diferencia de recuentos en inmuebles omitidos ni prioridad de revisión en negligencia probada.

## Producción y entrega visual

Dos llamadas a `image_gen` integrado: hero nuevo en 23,0 s y teaser derivado por referencia local en 27,4 s. La edición usó `referenced_image_paths` después de `view_image`. Son tiempos de dos llamadas, no un benchmark ni una garantía de fiabilidad. No se usó API key ni CLI de generación.

| Pieza | Dimensiones reales | PNG original | WebP sin pérdida | Reducción de bytes |
|---|---|---:|---:|---:|
| Hero | 1942 × 809 | 2.042.870 | 1.449.082 | 29,07 % |
| Teaser | 1672 × 941 | 2.049.992 | 1.495.992 | 27,02 % |

La recodificación con `magick entrada.png -define webp:lossless=true salida.webp` modifica únicamente el formato. Comparación del contenido RGB decodificado con `magick archivo RGB:- | sha256sum`: hero `b1e254d9fe1e27ab6a88279d587f9009403387c2f65471751a381beca4c18517`; teaser `b617d867a44483a1894d0d68296cdb01ce42241c0542c193a97575d04135be94`, idénticos en sus dos formatos. El subagente confirmó además igualdad RGBA y opacidad completa. No hubo recorte, remuestreo ni retoque en la conversión.

La web consume WebP y la imagen social PNG; los originales se conservan. El hero tiene precarga de alta prioridad, título nativo y pie conceptual ES/EN. Se conectó `og_image_alt`, antes inerte en la plantilla, a `og:image:alt` y `twitter:image:alt`. Los gráficos y mapas analíticos permanecen independientes. [Prompts completos](avaluos-ii-imagegen-prompts-20260911.md) y [diagnóstico delegado](avaluos-ii-imagegen-diagnosis-20260911.md).

## Validación y límites observados

| Comprobación | Resultado |
|---|---|
| `JEKYLL_ENV=production bundle exec jekyll build --drafts --unpublished --destination /tmp/avaluos-ii-hero-20260911` | Exit 0; solo avisos conocidos de deprecación Sass |
| `VERIFY_MATH_DRAFTS=1 ruby scripts/verify_site_artifact.rb /tmp/avaluos-ii-hero-20260911` | Aprobado, dentro de presupuestos de tamaño y entradas |
| `ruby scripts/verify_distribution_readiness.rb /tmp/avaluos-ii-hero-20260911` | 24 posts; imágenes sociales, descripciones, canonicals y enlaces internos correctos |
| `ruby scripts/verify_visual_assets.rb --strict` | 9 manifiestos, 99 assets, cero avisos; dimensiones reales comprobadas |
| HTML de ambos artículos | Un h1, fecha correcta, canonical por idioma, precarga y descripción social presentes |
| Build normal sin flags de borrador | Aprobado; artículos aún ausentes, igual que el manuscrito archivado y el overlay local |
| ES/EN móvil y escritorio | Título completo, encuadre conceptual reconocible y documento sin desbordamiento a 390 px; capturas estables conservadas en `editorial-qa/` |
| Tarjeta real en portada móvil | Teaser visible a 333,625 × 187,656 px, composición legible y sin texto incrustado |
| Evaluador de carga cartográfica | 11 pruebas aprobadas; no convierte el ensayo incompleto por foco en mejora demostrada |

La primera captura de escritorio coincidió con la transición de entrada y mostraba un velo gris; se repitió en estado estable. El pie permanecía apagado porque el tema imponía `opacity: 0.5`: se corrigió a `1` solo en este artículo. Una sonda que esperaba decodificar todas las imágenes, incluidas las de carga diferida, agotó `Runtime.evaluate`; se sustituyó por lectura de DOM y del recurso del hero. Ese timeout de la sonda no prueba un fallo del asset.

El primer intento de usar `%[signature]` en ImageMagick no devolvió esa propiedad; la equivalencia se comprobó después sobre los bytes RGB decodificados, no sobre una firma vacía. El registro del selector MCP emitió `MCP observation unavailable`; la consulta de memoria sí respondió con abstención. No se presenta como telemetría registrada.

Los WebP siguen alrededor de 1,5 MB: hay una reducción medida, pero no evidencia de entrega óptima en redes móviles ni comparación de calidad entre proveedores. La precarga no demuestra una mejora de LCP por sí sola. La cifra local de 15,3 ms para recibir el hero es una observación de localhost y no representa producción.

## Preview y continuidad

En esta continuación el servidor 4004 había terminado: comprobación host de puerto, proceso y HTTP negativa; no se reinició por un simple timeout. Se restauró Jekyll con el mismo destino y un complemento temporal `/tmp/avaluos-jekyll-4004-local.yml` que conserva `assets/data/catastro_sii/local` al regenerar. Se proyectaron siete enlaces a datos locales preexistentes; no se duplicaron los datos ni se incluyeron en el build normal.

El benchmark emparejado previo conserva sus cinco observaciones y exclusiones en sus propios documentos; no se reanudó ni se atribuyó la interferencia de foco a una versión del visor. F9_2 sigue parcial. El ranking monetario sigue pendiente de contribuciones netas habitacionales compatibles. No hubo push, publicación ni solicitud institucional enviada.
