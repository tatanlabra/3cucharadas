# Diagnóstico de imagegen para Avalúos II

> **Adenda del 12-09-2026.** La herramienta funcionó, pero la revisión humana posterior rechazó la dirección artística. Por tanto, la aceptación visual Q2 de este diagnóstico queda refutada para el par inicial. La [corrección vigente](avaluos-ii-title-visual-correction-20260912.md) recupera Tokyo Night, los tamaños editoriales y la convención del título; este informe sólo conserva evidencia operacional de la primera ejecución.

Fecha local: 2026-09-11. Responsable: subagente `imagegen_diagnosis`; integración y generación a cargo del agente principal. Alcance: hero editorial y teaser bilingües para el borrador de Avalúos II; sin publicación, llamadas API adicionales ni modificación de la skill global.

## Dictamen

**La vía incorporada funcionó para los fines solicitados: produjo un hero y un teaser coherentes, integrables y legibles en las superficies inspeccionadas. No está demostrada la optimalidad global de la skill.** El peso de entrega móvil sigue siendo una mejora parcial; el esquema de la herramienta no ofrece controles estructurados de resolución, formato, compresión o modelo.

Hay una desalineación concreta entre la descripción de edición de la skill y la herramienta actual: esta última admite `referenced_image_paths`. Se resuelve aplicando la instrucción de mayor prioridad —inspeccionar primero con `view_image`, después editar mediante la ruta local—, sin derivar a CLI por esa sola necesidad.

## Evidencia y límites

| Nivel | Comprobación actual | Lo que permite concluir |
|---|---|---|
| Configuración | Leídos `SKILL.md`, `references/prompting.md`, plantilla web de `references/sample-prompts.md`, referencia CLI y constantes del script; herramienta `image_gen__imagegen` efectivamente expuesta | Existe una vía incorporada apta para generación y edición; no demuestra que haya completado una llamada |
| Plantilla consumidora | Inspeccionados `_includes/page__hero.html`, `_includes/archive-single.html`, `_includes/seo.html`, `assets/css/main.scss` y verificadores | Se conocen mecanismos reales de título, recorte, teaser responsivo e imagen social |
| Ejecución | Ambos archivos confirmados por `file`, `stat` y SHA-256; el agente principal reporta llamadas terminadas en 23,0 y 27,4 s | Se confirma el output del par; duraciones son evidencia transmitida por el ejecutor, no un benchmark independiente |
| Calidad visual | Hero y teaser inspeccionados con `view_image`; revisadas capturas estables del hero ES/EN a 390 px, ES a 1440 px y EN oscuro a 1440 px, más tarjeta real de ~334 px | Se acepta la composición en esas muestras; no equivale a cobertura de todas las combinaciones de idioma, tema y dispositivo |
| Comparación entre proveedores/superficies | No ejecutada; CLI no autorizado y ChatGPT web no inspeccionado | No se declara superioridad de calidad, costo o latencia frente a alternativas |

Huellas de los recursos auditados, sin modificaciones:

- `SKILL.md`: `681ddb4ad6d06a2acc78a3535b583f8d0c1ea800ecda3d56370d3310fd2cd4ba`.
- `scripts/image_gen.py`: `b4345cf835e5b593b97df6bb2b70bda493b8a97eee4cabbc99b2fa57dba9b448`.
- La herramienta disponible expone solamente `prompt`, `referenced_image_paths` y `num_last_images_to_include`; el modelo interno, costo y parámetros de codificación no son observables en ese esquema.

## Rúbrica fijada antes de recibir imágenes

Esta rúbrica es un protocolo de revisión, no un verificador nuevo ni una prueba ya aprobada. Los contraejemplos describen condiciones de rechazo; no se registran como rojos observados hasta inspeccionar un caso real.

| ID | Restricción o criterio | Evidencia de aceptación | Contraejemplo que impide aprobar |
|---|---|---|---|
| H1 | Honestidad editorial | Ciudad y registro aparecen como una ilustración conceptual; caption lo declara; no hay datos, mapas identificables, leyendas fiscales o cifras inventadas | Una imagen parece cartografía real o identifica una vivienda como omisión tributaria comprobada |
| H2 | Dos entregables conservados | Hero y teaser son archivos reales dentro del repositorio, con rutas, dimensiones y procedencia documentadas | Enlace a archivo temporal/inaccesible o un único montaje que no entrega ambas piezas |
| H3 | Legibilidad bilingüe | Sin texto rasterizado; título nativo ES/EN sin recortes ni solapamientos a 390 y 1440 px | Título incorporado solo en español, glifos ficticios o recorte del título HTML |
| H4 | Accesibilidad e integración | La imagen es decorativa cuando su información está en texto; imagen social tiene descripción cuando la plantilla la expone; no hay información esencial solo en color | Datos necesarios escondidos en un background o distinciones solo cromáticas que el texto no explica |
| H5 | Restricciones operativas | Built-in, una llamada por pieza/variante; edición local tras `view_image`; sin llamadas duplicadas por timeout de observación | Cambiar silenciosamente a CLI, reiniciar una llamada todavía viva o sobrescribir imágenes ajenas |
| H6 | Integridad técnica | Dimensiones reales coinciden con manifest/nombre; referencias locales existen; OG ≥1200 px; build y verificación visual actuales | Un sufijo `1280x720` encubre otra resolución o el `srcset` apunta a un sibling inexistente |
| Q1 | Claridad a tamaño de uso | Teaser mantiene un motivo principal reconocible a unos 320–384 px; el hero admite el título sobre zonas tranquilas | Microdetalle que desaparece en la tarjeta o un motivo esencial perdido por `cover` |
| Q2 | Coherencia del par y del visor | Familia visual común: teal, slate, ámbar y base oscura; luz, geometría y materialidad coherentes | Teaser con estilo/composición ajenos al hero o colores que parecen una escala de datos inexistente |
| Q3 | Peso de entrega | Registrar bytes y resolución por archivo y contrastarlos con el baseline; separar master y entrega si la optimización está autorizada | Dar por eficiente un PNG de varios MB únicamente porque el build queda bajo 1 GB |
| Q4 | Robustez de recorte | Inspección real de tarjeta 16:9 y hero en escritorio/móvil, incluyendo caption y cambio de idioma | La evidencia solo muestra el master completo o una captura de escritorio |
| Q5 | Trazabilidad y costo de operación | Prompt final y llamadas/variantes documentadas; originales preservados; ningún servicio nuevo requerido | Repetir generaciones sin objetivo discriminante ni conservar cuál se integró |

Meta ideal: dos imágenes reconocibles, coherentes y ligeras, sin fallos a cualquier tamaño. Óptimo factible para este alcance: satisfacer H1–H6 y revisar Q1–Q5 en las dos superficies acordadas, con el menor número de iteraciones útil. Resultado medido: dos piezas producidas e inspeccionadas, entrega recodificada sin cambios de píxeles; dos muestras permiten evaluar estas piezas, no estimar la fiabilidad general de la skill.

## Hallazgos priorizados

| ID / gravedad | Hallazgo reproducible | Consecuencia | Recomendación |
|---|---|---|---|
| I1 / media | `SKILL.md:76–80` describe edición visible y deriva a CLI para control directo de ruta; el esquema vigente sí admite `referenced_image_paths` | Un agente que obedezca esa frase aisladamente puede pedir autorización innecesaria o escoger otra vía | Usar `view_image` y `referenced_image_paths` conforme a la herramienta; reportar desalineación sin editar la skill global |
| I2 / media | El esquema built-in no contiene `size`, `output_format`, `quality`, `seed`, `out` ni `model` | Un prompt que pide 16:9/PNG no garantiza el formato/resolución del archivo | Inspeccionar encabezado, MIME, bytes y dimensiones reales; no inventar argumentos ni prometer medidas exactas antes de recibir el archivo |
| I3 / media | `_includes/archive-single.html:13–22,35–38` construye automáticamente un sibling móvil cuando encuentra `/assets/images/teasers/*.webp` | Un solo WebP con esa ruta crea una referencia adicional aunque ese archivo no exista | Integrar la pareja real conforme al patrón; si el output es PNG, conservar inicialmente el PNG con medidas reales y registrar la deuda de entrega responsiva |
| I4 / media | `_includes/page__hero.html:24–26` utiliza CSS background y `assets/css/main.scss:212–240` impone un título/párrafo sobre la imagen | El master aislado puede ser legible, pero el título puede caer sobre edificios/retícula al recortar | Composición con zona tranquila y filtro oscuro; revisar ES/EN y móvil/escritorio; no aumentar detalle detrás del título |
| I5 / media | El presupuesto del artefacto es global: `scripts/verify_site_artifact.rb:17–20`; no impone un presupuesto específico por hero/teaser | Un resultado pesado puede pasar todos los checks existentes | Medir tamaño de archivo y transferencia del recurso; el éxito del build no prueba eficiencia de carga |
| I6 / baja, resuelto por agente principal | `_includes/seo.html` inicialmente no renderizaba `og_image_alt` ni `twitter:image:alt`; el diff actual y el HTML construido ES/EN ya incluyen ambos | El campo dejó de ser una declaración inerte y llega al artefacto servido | Mantener el campo localizado y escapado; comprobado directamente en `/tmp/avaluos-ii-hero-20260911/` |
| I7 / límite operativo | La herramienta requiere esperar una operación que puede durar minutos; la skill no detalla recuperación del handle | Un timeout de observación puede confundirse con fracaso y duplicar producción/costo | Conservar la celda devuelta, esperar esa misma celda y reintentar generación solo tras fallo terminal comprobado |
| I8 / media, resuelto por agente principal | Las primeras capturas mantenían el caption apagado; el tema fija `opacity: 0.5` en `vendor/bundle/ruby/3.4.0/gems/minimal-mistakes-jekyll-*/_sass/minimal-mistakes/_page.scss:255` | Cambiar solo el color no eliminaba la atenuación heredada | Agente principal añadió `opacity: 1` únicamente al selector `.avaluos-ii-editorial .page__hero-caption`; valor computado final reportado igual a 1 y captura móvil corregida reinspeccionada |

No se encontró evidencia de que la skill esté rota, de que el modelo incorporado sea inferior a ChatGPT web, o de que usar CLI mejore la calidad de estas ilustraciones. Tampoco se han probado esos enunciados contrarios.

### Baseline de peso observado

Medido con `stat` sobre archivos locales reales; no es una comparación de latencia ni de calidad entre imágenes distintas.

| Archivo de referencia | Bytes | Uso |
|---|---:|---|
| `assets/images/avaluos-ii/gap-top15-es.png` | 212.817 | Teaser anterior de Avalúos II; gráfico factual que permanece en el cuerpo |
| `assets/images/teasers/teaser-avaluo-vulnerabilidad-1280x720.webp` | 64.702 | Teaser de Avalúos I |
| `assets/images/teasers/teaser-avaluo-vulnerabilidad-640x360.webp` | 31.810 | Teaser móvil de Avalúos I |
| `assets/images/home/el-salvador-codera-hero-1600x524.webp` | 28.790 | Hero de inicio, composición distinta |
| `assets/images/home/el-salvador-codera-hero-mobile-1200x720.webp` | 32.736 | Hero móvil de inicio, composición distinta |

Los archivos existentes demuestran que el sitio tiene una vía de entrega WebP responsiva. No fijan un límite universal: una ilustración con otra complejidad puede pesar más. Un master nuevo de varios MB requeriría atender la entrega antes de declararla eficiente; no se debe sustituir ese trabajo por el mero cumplimiento del límite global.

## Comparación bajo los mismos criterios

| Criterio | Built-in incorporado | Prompt en ChatGPT web | CLI de la skill |
|---|---|---|---|
| Autorización actual | Sí; preferido por skill y herramienta | El usuario acepta recibir prompts; no exige operar su sesión web | No autorizada una llamada API de fallback |
| Ajuste al proyecto | Puede devolver un artefacto para copiar e integrar en esta sesión | Exige transferencia manual posterior del archivo al repo | Puede escribir una ruta explícita, si se autoriza |
| Controles observables aquí | Prompt y mecanismos de referencia; modelo/formato no configurables en el esquema | Superficie/modelo/opciones actuales no inspeccionados | Script local ofrece tamaño/formato/calidad/modelo; servicio no ejecutado ni validado aquí |
| Acceso y secretos | Según la skill no requiere `OPENAI_API_KEY`; no se inspeccionaron secretos | Depende de la cuenta del usuario; no se accedió | La skill requiere API key y red; no se buscaron ni usaron credenciales |
| Coherencia entre piezas | Referencia visual explícita y edición con invariantes | Prompt más imagen de referencia entregados al usuario | Referencias admitidas por el código local; calidad no ensayada |
| Calidad, latencia y costo reales | Par inspeccionado; tiempos reportados de 23,0 y 27,4 s; costo no observable | Desconocidos | Desconocidos; leer constantes o hacer `dry-run` no los demostraría |
| Juicio actual | Recomendado por menor trabajo adicional y compatibilidad con la autorización | Alternativa útil para iteración humana directa y prompt reutilizable | Reservado para elección explícita; no hay evidencia de ventaja suficiente para cambiar |

Esta comparación evalúa viabilidad y control observable, no establece un ranking de calidad entre modelos. El diagnóstico y la producción pertenecen a agentes del mismo sistema; no constituyen validación independiente entre proveedores.

## Deducción, inducción y abducción

| Tipo | Conclusión | Evidencia discriminante o límite |
|---|---|---|
| Hecho | La herramienta admite rutas de referencias locales y la edición del teaser por esa vía funcionó según el ejecutor, con archivo real inspeccionado | Esquema efectivo y dos archivos; la skill `SKILL.md:76–80` no refleja completamente esa capacidad |
| Deducción | Un tamaño escrito en el prompt no equivale a una garantía estructurada del output | El esquema carece de ese control; las dimensiones recibidas pueden cumplir o incumplir el deseo |
| Deducción | No debe representarse una deuda ni una omisión predial como un hecho en la ilustración | El propio post distingue diferencia entre recuentos de omisión comprobada; el hero no puede contradecirlo |
| Inducción acotada | En cinco assets locales de referencia, la entrega existente tiene pesos entre 28.790 y 212.817 bytes | Solo describe esos cinco archivos; no prueba que una nueva ilustración alcance igual peso con igual calidad |
| Abducción provisional | Una composición con dos capas urbanas por conciliar comunica mejor el tema que dinero o una acusación visual | Preferida porque coincide con el relato verificable; descartar si las piezas se leen como un mapa de propiedades efectivamente omitidas o como un antes/después engañoso |
| Abducción provisional | Derivar el teaser del hero favorece una identidad visual común con menos iteraciones que dos generaciones sin referencia | Inspeccionar geometría, paleta y motivo del par; descartar si la edición pierde legibilidad a tamaño de tarjeta y una composición independiente resuelve ese defecto |
| Incertidumbre | Fiabilidad de generación, ratio final, nitidez, costos, tiempos y calidad comparada | Solo se resolverán parcialmente con los archivos reales; una comparación de rutas requeriría autorización y ensayos bajo condiciones equivalentes |

## Recepción de resultados

Recepción del par: inspeccionado el 2026-09-11. Falta evaluar el render final; la rúbrica anterior no se cambia para acomodar el resultado.

| Campo | Hero recibido |
|---|---|
| Archivo final original | `assets/images/avaluos-ii/hero-catastro-residencial-v1-1942x809.png` |
| Formato real | PNG RGB de 8 bits, sin entrelazado |
| Dimensiones | 1942 × 809 px; relación 2,40049:1 frente a aproximadamente 2,4:1 solicitada |
| Peso | 2.042.870 bytes, 9,60 veces el teaser anterior de 212.817 bytes; son piezas con usos distintos, no una regresión de latencia medida |
| SHA-256 | `57d2e84e1eb1eb4f8e4632faaaf086683b4504958146c013729268043564ae5f` |
| Prompt | `docs/avaluos-ii-imagegen-prompts-20260911.md`, sección Hero |
| Ejecución reportada | Built-in terminado con éxito en 23,0 s según agente principal |
| Inspección directa | Diorama de viviendas y edificios sobre base oscura, plano catastral abstracto translúcido, líneas teal y ámbar escaso; sin texto ni geografía identificable |
| Favorable | Zona izquierda tranquila para título HTML; composición coherente con el encargo conceptual y con la familia cromática |
| Contrario / pendiente | Peso alto para entrega; caption debe evitar que los contornos incompletos se interpreten como omisiones comprobadas; falta prueba de recorte con título real |

| Campo | Teaser recibido |
|---|---|
| Archivo final original | `assets/images/avaluos-ii/teaser-catastro-residencial-v1-1672x941.png` |
| Formato y dimensiones | PNG RGB de 8 bits, 1672 × 941 px; relación 1,77683:1, muy cercana a 16:9 pero no exacta |
| Peso | 2.049.992 bytes |
| SHA-256 original | `3aa42647ea65f6e79ba7bed3cdeb98fce302a62fe998ad22c28fd8f34f43948f` |
| Prompt | `docs/avaluos-ii-imagegen-prompts-20260911.md`, sección Teaser |
| Ejecución reportada | Built-in terminado con éxito en 27,4 s; referencia local al hero inspeccionado |
| Inspección directa | Conjunto más compacto y centrado de viviendas y plano translúcido; conserva materiales, luz y familia cromática del hero |
| Favorable | Motivo principal completo, sin texto ni elementos nuevos acusatorios; elimina el gran vacío lateral del hero |
| Contrario / límite | El microdetalle de ventanas disminuye en tarjeta, pero la captura real de ~334 px conserva el conjunto de viviendas, el plano y la relación entre ambos |

### Recodificación de entrega observada

El agente principal recodificó ambos archivos con ImageMagick a WebP lossless, conservando los originales. Es una conversión de formato sin retoque, recorte, remuestreo o variación generativa. La distinción es verificable: esta auditoría volvió a decodificar **RGBA de 8 bits** de ambas versiones y obtuvo hashes idénticos por pieza; los cuatro archivos son opacos y conservan sus dimensiones, espacio sRGB y gamma 0,454545.

| Pieza | Bytes PNG | Bytes WebP | Reducción | SHA-256 de RGBA decodificado, idéntico en ambos formatos |
|---|---:|---:|---:|---|
| Hero | 2.042.870 | 1.449.082 | 29,07 % | `aefdbc68b2220d62cb341ac707e59908daa7f5816cdedae7b0d52753b8e32372` |
| Teaser | 2.049.992 | 1.495.992 | 27,02 % | `b3a066ea4e1e088bc3f9d95492c968d50962696e6e1b26763cbf7062bccdb29b` |

Comprobaciones de lectura: `file`, `magick identify -format '%f %wx%h %[channels] opaque=%[opaque]\n'` y `magick <archivo> -depth 8 rgba:- | sha256sum`. Ninguna de estas comprobaciones modifica los archivos. `file` etiquetó inicialmente el contenedor del teaser WebP como «with alpha»; la decodificación confirmó opacidad total y RGBA idéntico, por lo que no se infiere transparencia real de esa etiqueta aislada.

Los nombres finales incluyen las dimensiones reales y evitan una declaración engañosa de 1280 × 720. La conversión reduce el transporte de bytes sin pérdida visual; **no demuestra que el peso final de ~1,5 MB sea óptimo para una tarjeta pequeña**. Recomiendo entregar estos archivos como versión fiel y mantener visible la oportunidad de una variante responsiva más ligera, que requeriría comprobar sus píxeles, resolución y calidad a tamaño de uso bajo el mecanismo autorizado. No cambiar a CLI ni regenerar el arte para aparentar una conversión exacta.

Incidencia de observabilidad transmitida por el agente principal: el selector MCP informó `MCP observation unavailable; calls continue unmeasured`; `recall` respondió con abstención. Esto limita la telemetría de selección de capacidades, no invalida el archivo raster comprobado ni demuestra un fallo de imagegen.

### Integración comprobada

| Evidencia | Resultado | Límite |
|---|---|---|
| HTML ES/EN de `/tmp/avaluos-ii-hero-20260911/`, leído directamente | Caption conceptual localizado, preload del hero y etiquetas `og:image:alt` / `twitter:image:alt` presentes en ambos idiomas | Presencia de preload no cuantifica una mejora de LCP |
| `/tmp/avaluos-hero-es-390-final.png` y `/tmp/avaluos-hero-en-390-final.png`, inspección visual | Títulos completos en tres líneas, escena reconocible y contenido dentro del ancho; el ejecutor mide `scrollWidth=390` en viewport 390 | La revisión previa permitió detectar `opacity:0.5` heredada; valor computado corregido a 1 y captura ES reinspeccionada con texto visible, sin truncamiento |
| `/tmp/avaluos-hero-es-1440-final.png` y `/tmp/avaluos-hero-en-1440-dark-final.png`, inspección visual | Composición y paleta estables, títulos completos sobre base oscura, sin solapamientos apreciables; el hero funciona junto al tema claro y al oscuro | La primera captura `/tmp/avaluos-hero-es-1440.png`, con velo de transición, se conserva como antecedente excluido del juicio de color |
| `/tmp/avaluos-teaser-card-390-final.png`, inspección visual | La tarjeta real conserva el conjunto de viviendas y el plano superior; no corta el motivo principal ni depende de texto rasterizado | Tamaño comunicado 333,625 × 187,656 px; referencia eager por ser primera tarjeta; usa el archivo grande, sin variante móvil |
| Build y verificadores comunicados por el agente principal | Artefacto final 77.923.263 bytes, distribución 24 posts y registro visual 99 assets sin warnings | Son evidencias transmitidas; esta auditoría no duplicó esos comandos ni los usa como prueba de optimalidad visual |
| Build normal de producción comunicado por el agente principal | 77.011.354 bytes, 18 posts; los borradores, docs y overlay local quedan ausentes | No hubo publicación remota |

La descarga local del hero reportó 1.449.082 bytes y 15,3 ms en una observación. Confirma la entrega del recurso, **no** un percentil de producción, una ventaja causal del preload ni una medida de acceso móvil. Una evaluación que esperaba `decode()` de todas las imágenes —incluidas las diferidas— agotó `Runtime.evaluate`; se sustituyó por DOM, entradas de recursos y captura estable. No se atribuye ese timeout al generador ni al archivo.

Cierre del caption: el agente principal reportó `captionOpacity="1"`, color `rgb(232,237,242)` y fondo `rgba(16,18,29,0.92)` en viewport 390 sin overflow. La captura ES final se volvió a inspeccionar tras ese cambio y muestra texto visible sin truncamiento. No hizo falta otra generación: el defecto estaba en el CSS del tema.

### Estado de los criterios

| Criterios | Resultado |
|---|---|
| H1–H3 | Cumplidos en archivos, texto e imágenes observadas: honestidad conceptual, dos piezas locales y títulos nativos bilingües |
| H4 | Cumplido en el alcance inspeccionado: imagen decorativa, caption conceptual localizado, alt social efectivo y opacidad corregida comprobada; no es una auditoría WCAG exhaustiva |
| H5–H6 | Cumplidos en el alcance observado: dos llamadas built-in reportadas, referencia local efectiva, originales preservados, rutas y medidas reales, OG ≥1200 px y builds verificados por ejecutor |
| Q1–Q2 y Q4 | Favorables en las muestras inspeccionadas: motivo reconocible, coherencia cromática y recortes adecuados |
| Q3 | Parcial: reducción fiel de 27–29 % frente a PNG; los ~1,5 MB por pieza y la falta de derivado móvil impiden afirmar entrega óptima |
| Q5 | Cumplido en trazabilidad disponible: prompts, archivos, medidas y hashes; latencia solo reportada y costo interno desconocido |

| Estado | Alcance |
|---|---|
| Implementado | Auditoría local de skill, herramientas y plantillas; rúbrica y recomendaciones registradas antes de evaluar outputs |
| Parcial | Peso de entrega móvil; no se afirma optimalidad global |
| No implementado | Generación duplicada, llamadas CLI/API, edición global de skill, publicación y comparación experimental entre superficies |
