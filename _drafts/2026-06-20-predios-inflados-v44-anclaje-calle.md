---
layout: single
title: "Predios desde una coordenada en 3 cucharadas: anclar la forma a la calle"
subtitle: "Reconstrucción geométrica de predios del SII para análisis territorial, probada en Diego de Almagro y Caldera"
date: 2026-06-20
categories: [datos, geoespacial, sii]
tags: [sii, catastro, georreferenciacion, reconstruccion-predial, cctpr, diego-de-almagro, caldera, openstreetmap, r, voronoi, sivust, igvust]
description: "Cómo reconstruir polígonos prediales inferidos cuando el SII entrega coordenadas, superficies y avalúos, pero no siempre disemina geometrías vectoriales masivas: anclaje a calle, validación topológica y cruces con vulnerabilidad socioterritorial."
author: "3 Cucharadas"
toc: true
toc_sticky: true
comments: true
author_profile: true
header:
  og_image: /assets/img/predios_3102_diego_centro_face2face_v44.png

gallery_v44:
  - url: /assets/img/predios_3102_diego_centro_face2face_v44.png
    image_path: /assets/img/predios_3102_diego_centro_face2face_v44.png
    alt: "Face-to-face de Diego de Almagro (3102): a la izquierda la trama vial observada de OpenStreetMap; a la derecha los predios reconstruidos v4.4 como rectángulos anclados a la calle, color por clase."
    title: "Diego de Almagro (3102) — observado (trama vial) vs. inferido (predios reconstruidos v4.4)"
  - url: /assets/img/predios_3202_caldera_face2face_v44.png
    image_path: /assets/img/predios_3202_caldera_face2face_v44.png
    alt: "Face-to-face de Caldera (3202): a la izquierda la trama vial observada de OpenStreetMap; a la derecha los predios reconstruidos v4.4 como rectángulos con frente a la calle, color por clase."
    title: "Caldera (3202) — observado (trama vial) vs. inferido (predios reconstruidos v4.4)"
---

Hay datos públicos que parecen pequeños hasta que se cruzan con otros. El catastro predial es uno de ellos. Una coordenada, una superficie y un avalúo fiscal no dicen demasiado si se miran de a un predio; pero, cuando se ordenan territorialmente, permiten observar patrones de valorización del suelo, accesibilidad, centralidades, bordes urbanos, zonas de expansión, discontinuidades de inversión y brechas socioterritoriales.
{: .text-justify}

Ahí está el problema: el Servicio de Impuestos Internos (SII) administra una de las bases territoriales más valiosas del Estado, pero su diseminación masiva sigue siendo más difícil de lo que debería ser para investigación, política pública y análisis territorial. Los resguardos de privacidad y seguridad importan, sobre todo cuando existen atributos identificables o riesgos de uso indebido; sin embargo, resguardar no debería equivaler a impedir el uso analítico, agregado y reproducible de información de alto valor público. Una cosa es proteger personas; otra, muy distinta, es dejar subutilizada la infraestructura de datos que permitiría entender mejor el territorio.
{: .text-justify}

Este post muestra un ejercicio concreto: reconstruir geometría predial inferida cuando se dispone de un punto, una superficie y una red vial. La prueba se hizo en **Diego de Almagro** y **Caldera**, usando datos prediales del SII procesados y distribuidos por **Cristóbal Hernández / Tremen** a través de [Catastral.cl](https://catastral.cl/) y la trama vial de [OpenStreetMap](https://www.openstreetmap.org/). El mérito de Tremen no es menor: convirtió una información formalmente pública, pero técnicamente difícil de usar a escala, en una base explotable para análisis territorial. Su repositorio describe el propósito como producir un conjunto georreferenciado de millones de predios con geometría vectorial y atributos catastrales para las comunas del país.
{: .text-justify}

La hipótesis es deliberadamente modesta: **un punto no es un polígono**, pero puede transformarse en una hipótesis geométrica útil si se respeta la superficie, la calle, la manzana y la topología. Esta no es una mensura ni una cartografía oficial de deslindes. Es una capa analítica para preguntar mejor.
{: .text-justify}

---

## Tolerancia al contraste: ¿qué tan sano es el resultado?

Antes de mirar mapas, conviene mirar controles. La versión v4.4 no busca exactitud catastral plena; busca geometría plausible, trazable, útil y honesta respecto de su incertidumbre.

{: .table-caption}
**Tabla 1** — Cobertura y precisión de la reconstrucción v4.4, por piloto (fuente interna: `predios_inflados_class_summary.csv`)

| Piloto | Predios | Con polígono | Cobertura | Sin soporte | Error de superficie mediano | Geometrías inválidas | Avalúo representado |
|--------|--------:|-------------:|:---------:|------------:|:----------------------------:|:--------------------:|-------------------:|
| Diego de Almagro (3102, centro) | 3.050 | 3.041 | **99,7 %** | 9 | 21 % | **0** | $74.548 MM |
| Caldera (3202) | 5.753 | 5.708 | **99,2 %** | 45 | 24 % | **0** | $187.622 MM |
| **Total** | **8.803** | **8.749** | **99,4 %** | **54** | — | **0** | **$262.170 MM** |

Dos lecturas son importantes.

Primero, la cobertura es alta, pero no total. **54 predios quedaron sin polígono**. Eso no es un fracaso; es una regla de prudencia. Cuando no hay soporte suficiente, por ejemplo, sin calle cercana o sin espacio geométrico razonable en la manzana, el predio se conserva como registro, pero no se dibuja.
{: .text-justify}

Segundo, el error mediano de superficie no debe leerse mecánicamente como defecto. La reconstrucción recupera aproximadamente tres cuartas partes de la superficie declarada. Parte de la diferencia proviene del recorte contra la vialidad y del carácter conservador de la forma. En esta etapa preferimos un polígono bien ubicado, trazable y algo más pequeño, antes que una figura inflada que invada calle, espacio público o predios vecinos.
{: .text-justify}

Esta decisión es coherente con una regla metodológica básica: **degradar antes que sobrerrepresentar**. Cuando una geometría inferida no puede justificarse, se etiqueta como baja confianza o sin soporte.

---

## Cucharada 1 — Una base pública no es todavía una infraestructura pública

El SII permite consultar avalúos, roles, superficies y características de bienes raíces. También dispone de cartografía digital. Pero la consulta predio a predio no alcanza para preguntas territoriales: ¿dónde se concentra el valor del suelo?, ¿qué zonas vulnerables tienen alta presión inmobiliaria?, ¿qué barrios combinan baja inversión privada con alta vulnerabilidad socioterritorial?, ¿dónde la inversión pública y privada podrían complementarse mejor?
{: .text-justify}

La diferencia entre consulta unitaria y uso masivo no es menor. Las infraestructuras de datos espaciales sirven cuando permiten reutilización, cruce y trazabilidad. En el lenguaje de datos abiertos, los conjuntos de alto valor no son solo los que existen, sino aquellos que pueden reutilizarse de manera efectiva. La literatura reciente sobre *high-value datasets* insiste en que los datos deben ser reutilizables y transformables en productos o servicios de valor público, no solo estar nominalmente disponibles.
{: .text-justify}

> “data must be reused and transformed into value-added products or services”.  
> — Nikiforova et al., 2023, revisión sistemática sobre *high-value datasets*.

En Chile, el valor de esta apertura sería muy concreto. Un catastro predial explotable permitiría cruzar **avalúo por metro cuadrado**, destino del predio, superficie, densidad y localización con indicadores territoriales de vulnerabilidad. Ese cruce se vuelve especialmente potente cuando se lleva a Unidades Vecinales (UV) y se combina con el **SIVUST/IGVUST**. Para quienes no lo conocen, el [Banco Integrado de Datos, BIDAT](https://bidat.gob.cl/directorio/SIVUST%20-%20Vulnerabilidad%20Socioterritorial), publica mapas y bases del Índice Global de Vulnerabilidad Socioterritorial (IGVUST) en cuartiles y ranking para UV, comunas y regiones.
{: .text-justify}

El propio BIDAT presenta el SIVUST como un avance para incorporar el enfoque territorial en políticas sociales y como insumo para la asignación, diseño y evaluación de programas basados en evidencia. La cita es clara:

> “insumos cruciales para la asignación, diseño y evaluación de programas sociales basados en evidencia”.  
> — BIDAT, directorio SIVUST.

La tensión, entonces, no es entre privacidad y apertura. La tensión real es entre una apertura diseñada para el uso público responsable y una disponibilidad fragmentada que termina favoreciendo a quienes tienen recursos técnicos para sortear barreras. En el caso predial, la pregunta pública no debería ser solo quién puede consultar un rol, sino qué capacidades colectivas se pierden cuando no existe una diseminación masiva, documentada y apta para análisis.
{: .text-justify}

Esto exige cautela. El SII advierte que sus mapas son referenciales. La Resolución Exenta N.° 51 de 2026 señala que los servicios de interoperabilidad de SII-Mapas tienen carácter referencial en localización y dimensiones, y que no acreditan delimitaciones de manzanas o predios. Dicho de otro modo: son datos muy valiosos, pero no equivalen a un deslinde jurídico.
{: .text-justify}

> “son de carácter referencial, tanto en su localización como en sus dimensiones”.  
> — SII, Resolución Exenta N.° 51 de 2026.

Esa frase no debilita el ejercicio; lo ordena. Lo que sigue no pretende reemplazar al catastro jurídico ni a la mensura oficial. Pretende construir una **capa analítica inferida**, útil para describir patrones territoriales y abrir preguntas de política pública.

---

## Cucharada 2 — De punto a polígono: anclar la forma a la calle

La versión v4.4 parte de una regla urbana simple: un predio no flota en el centro de la manzana; normalmente tiene **frente a una vía**. Por eso, para cada punto predial con superficie conocida, el método construye un rectángulo orientado por la calle más cercana.

El procedimiento es el siguiente:

1. se identifica la vía más cercana al punto predial;
2. se proyecta el punto hacia esa vía para aproximar el frente;
3. se orienta el lado largo del rectángulo en paralelo a la calle;
4. se extiende la profundidad hacia el interior de la manzana;
5. se recorta contra la calzada y barreras duras;
6. se evita inventar polígonos cuando no hay soporte geométrico suficiente;
7. se clasifica cada resultado según su origen y confianza.

El corazón de la iteración v4.4 es una función deliberadamente simple:

```r
# Rectángulo anclado: frente paralelo a la calle, profundidad hacia el interior del bloque
build_anchored_rect <- function(point_m, area_m2, road_geom, aspect_ratio = 1.8, setback = 2) {
  xy      <- sf::st_coordinates(point_m)[1, c("X", "Y")]
  road_pt <- tail(sf::st_coordinates(sf::st_nearest_points(point_m, road_geom)), 1)
  inward  <- (xy - road_pt) / sqrt(sum((xy - road_pt)^2))   # normal a la calle, hacia el interior
  along   <- c(-inward[2], inward[1])                        # tangente: paralela a la calle
  width   <- sqrt(area_m2 * aspect_ratio)                    # frente aproximado
  depth   <- area_m2 / width                                 # fondo aproximado
  front   <- road_pt + inward * setback
  coords  <- rbind(front - along*width/2, front + along*width/2,
                   front + along*width/2 + inward*depth, front - along*width/2 + inward*depth,
                   front - along*width/2)
  sf::st_sfc(sf::st_polygon(list(coords)), crs = sf::st_crs(point_m))
}
```

La mejora respecto de versiones anteriores es conceptual. Hasta la v4.3, el recorte tipo *packing* hacía que cada predio dependiera del orden de colocación: si un lote entraba antes, deformaba el espacio de los siguientes. El resultado eran triángulos, astillas y retazos. La v4.4 evita ese problema: no busca llenar todo a cualquier costo, sino construir una forma urbana plausible con frente, fondo y restricción vial.
{: .text-justify}

Este enfoque se puede leer como una primera forma de **teselación restringida**. En geometría espacial, las teselaciones dividen el plano en regiones asociadas a objetos o semillas. Los diagramas de Voronoi y sus variantes ponderadas son herramientas clásicas para esta familia de problemas, y siguen siendo relevantes cuando se requiere pasar de puntos a celdas, asignar vecindad o dividir un contenedor espacial. En el futuro, esta línea debería evolucionar hacia una teselación por manzana, con celdas no superpuestas y pesos asociados a la superficie declarada.
{: .text-justify}

La literatura geomática reciente también justifica la cautela. Grift, Persello y Koeva (2023) revisan la extracción de límites catastrales con aprendizaje profundo e imágenes remotas, y advierten que los estudios disponibles siguen siendo limitados, con problemas de generalización entre territorios. Su diagnóstico es útil para este post: usar imágenes, calles y puntos puede ayudar, pero ningún modelo debería confundirse con verdad catastral.

> “small study areas and small data sets”.  
> — Grift, Persello y Koeva, 2023.

Hong et al. (2021), al trabajar límites parcelarios desde imágenes aéreas, muestran que es preferible extraer límites como polígonos conectados y no solo agrupar píxeles similares. Ese punto dialoga directamente con este ejercicio: no basta con pintar superficies; hay que producir geometrías topológicamente sanas.

> “extract boundaries of polygon type over the pixel aggregation”.  
> — Hong et al., 2021.

Crommelinck et al. (2019), por su parte, muestran que los métodos asistidos por aprendizaje profundo pueden reducir el esfuerzo de delineación cuando los límites son visibles, especialmente en escenas rurales. Pero esa promesa tiene una condición: se trata de límites visibles, no necesariamente jurídicos.

> “38% less time and 80% fewer clicks”.  
> — Crommelinck et al., 2019.

Por eso, el uso de OpenStreetMap en esta versión es acotado: la red vial opera como **restricción geométrica**, no como verdad catastral. La imagen y la calle ayudan a ordenar la hipótesis; no la transforman en deslinde.

---

## Cucharada 2,5 — Qué falta para completar metodológicamente los polígonos

La v4.4 mejora la forma, pero todavía no resuelve todo. El paso siguiente no debería ser “más IA” de inmediato, sino mejor topología.

La hoja de ruta metodológica debería avanzar en cuatro capas:

1. **Teselación restringida por manzana.** Cada manzana debe dividirse como una cobertura planar: sin solapes, sin huecos injustificados y con bordes compartidos. La unidad de optimización no debe ser el predio aislado, sino el conjunto de predios de la manzana.
2. **Voronoi ponderado o diagrama de potencia.** Cuando existe superficie declarada, la distancia a cada semilla puede ponderarse para aproximar áreas relativas. Esto no garantiza exactitud, pero mejora la coherencia cuando predios grandes y pequeños conviven en la misma manzana.
3. **Restricciones morfológicas.** En áreas urbanas regulares, las particiones deberían favorecer frentes a calle, fondos razonables, orientación dominante y compacidad. En áreas rurales, deben pesar más caminos, canales, cercos, cambios de cultivo y pendientes.
4. **Validación topológica y clasificación de confianza.** Cada geometría debe quedar etiquetada: observada, inferida desde punto, inferida por manzana, degradada o sin soporte. La ausencia de solapes y de geometrías inválidas es condición mínima, no prueba de veracidad catastral.

Esta distinción es importante porque una cobertura visualmente atractiva puede ser metodológicamente débil si no respeta la estructura común de bordes. Para análisis público, la belleza del mapa no basta; debe haber trazabilidad, métricas y límites explícitos de uso.

---

## Cucharada 3 — Evidencia: El Salvador, Caldera y el valor de caracterizar bien el territorio

A la izquierda, lo observado: la trama vial de OpenStreetMap. A la derecha, lo inferido: los predios reconstruidos v4.4, coloreados por clase. En Diego de Almagro y Caldera, el cambio visual es claro: se pasa de puntos o manchas poco interpretables a hileras de lotes con frente a calle.

{% include gallery id="gallery_v44" layout="half" caption="**Face-to-face v4.4** — Diego de Almagro (3102) y Caldera (3202): capa observada (trama vial OSM) versus predios reconstruidos. Base vial: OpenStreetMap (cache local). Fuente predial: SII vía Catastral.cl/Tremen. Cartografía analítica, no constituye deslinde legal. Clic para ampliar." %}

La extracción de Cristóbal Hernández / Tremen permite llegar a esta pregunta porque resolvió un paso que normalmente queda oculto: transformar datos prediales públicos, dispersos y técnicamente ásperos en una base masiva, consultable y cruzable. El ejercicio de este post no reemplaza esa extracción; la usa como punto de partida para otro problema: cómo representar territorialmente predios cuando la geometría completa falta, es incompleta o no está disponible para uso masivo.
{: .text-justify}

La diferencia entre urbano y rural debe tratarse con seriedad. En urbano, la calle organiza gran parte de la forma predial: frente, fondo, línea de edificación, pasaje, manzana. En rural, en cambio, la geometría puede depender de caminos interiores, canales, quebradas, deslindes históricos, cambios de cultivo, cercos vivos o subdivisiones no visibles desde una sola fuente. Por eso, una metodología razonable no debería imponer el mismo molde en ambos territorios.
{: .text-justify}

En urbano, el anclaje a calle puede ser una buena primera aproximación. En rural, el método debe ser más prudente y apoyarse en segmentación de linderos visibles, imágenes de alta resolución, hidrografía, caminos, pendientes, límites agrícolas y revisión humana. Incluso allí, lo correcto es hablar de **linderos visibles o hipótesis parcelarias**, no de deslindes jurídicos.
{: .text-justify}

La razón de fondo no es inflar puntos por inflarlos. La razón es que **caracterizar bien el territorio mejora las decisiones**. Un predio representado como punto sirve para ubicar; un predio representado como polígono inferido, con cautelas, permite estimar entorno, densidad, vecindad, exposición, accesibilidad y relación con inversión pública o privada. Si ese mapa se cruza con IGVUST, se pueden observar desigualdades que no aparecen al mirar solo comunas o promedios.
{: .text-justify}

Por ejemplo:

- UV con alta vulnerabilidad y bajo avalúo por metro cuadrado pueden indicar territorios donde la inversión pública debe actuar como palanca de equidad territorial.
- UV con alta vulnerabilidad y alza de avalúo pueden indicar presión inmobiliaria, riesgo de desplazamiento o necesidad de regulación y provisión de servicios.
- Zonas con baja vulnerabilidad, alto avalúo y baja inversión pública pueden ayudar a reorientar recursos hacia territorios más rezagados.
- Áreas con equipamientos, inversión privada y baja vulnerabilidad pueden servir para estudiar polos de oportunidad, no solo carencias.

La contribución del SIVUST/IGVUST es precisamente permitir que esas lecturas no queden atrapadas en intuiciones. BIDAT ya disponibiliza información territorial para Unidades Vecinales, comunas y regiones. La agenda siguiente es cruzarla con capas económicas, urbanas y prediales de alta resolución, siempre cuidando privacidad y evitando usos individualizantes.
{: .text-justify}

En ese punto, el catastro deja de ser solo tributario. Se convierte en infraestructura para coordinar inversión, evitar duplicidades, identificar sinergias y anticipar efectos territoriales. Una mejor caracterización predial puede ayudar a que las prestaciones sociales se asignen con más pertinencia y a que la inversión pública y privada no opere a ciegas ni se solape de forma ineficiente.

---

## Cierre — No es el polígono perfecto; es una mejor pregunta territorial

Este ejercicio no prueba que podamos reconstruir el catastro legal desde puntos. Prueba algo más acotado y, a mi juicio, más útil: que podemos construir una **hipótesis geométrica controlada** para enriquecer el análisis territorial.

La regla es simple:

1. **No llamar oficial a lo inferido.** Un polígono reconstruido es una hipótesis espacial, no un deslinde.
2. **No sacrificar topología por cobertura.** Si una forma cruza calles, se superpone o no tiene soporte, debe degradarse.
3. **No confundir privacidad con inutilización del dato.** La protección de personas y riesgos patrimoniales puede convivir con datos agregados, anonimizados, trazables y reutilizables.
4. **No aplicar la misma lógica a lo urbano y lo rural.** La calle organiza mucho en ciudad; en rural pesan más linderos visibles, agua, caminos, usos de suelo e historia predial.
5. **No perder el objetivo público.** La finalidad no es dibujar lotes bonitos, sino mejorar la comprensión territorial para orientar prestaciones sociales, inversión y coordinación institucional.

La v4.4 muestra que anclar a la calle produce una mejora evidente frente al punto desnudo y frente al recorte por orden de colocación. La próxima etapa debería ser una teselación restringida por manzana, idealmente con Voronoi ponderado por superficie, validación topológica y medición de incertidumbre. Después de eso, recién tiene sentido incorporar modelos de segmentación visual como evidencia auxiliar.
{: .text-justify}

La promesa pública está en el cruce: catastro, avalúo por metro cuadrado, vulnerabilidad socioterritorial, inversión, servicios y equipamientos. Ahí aparece la pregunta que importa: no solo dónde están los predios, sino qué nos dicen sobre las oportunidades, brechas y prioridades del territorio.

> **Nota metodológica.** Esta cartografía es analítica. OpenStreetMap se usa como contexto y restricción espacial. La inferencia predial se valida por encaje a la vía, topología y superficie, pero no sustituye mensura oficial ni acredita deslindes legales.

> **Nota de privacidad.** La publicación minimiza atributos identificables: se muestran formas y clases agregadas, no rol predial, dirección exacta, propietario ni coordenadas crudas asociadas a atributos sensibles.

> **Nota de uso público.** El propósito del ejercicio es fortalecer análisis territorial agregado: vulnerabilidad, inversión, accesibilidad, valorización relativa del suelo y coordinación pública. No se recomienda usar esta capa para decisiones individuales que afecten derechos patrimoniales.

---

## Referencias comentadas

- [Servicio de Impuestos Internos, Resolución Exenta N.° 51 de 2026](https://www.sii.cl/normativa_legislacion/resoluciones/2026/reso51.pdf). Autoriza acceso a servicios de interoperabilidad cartográfica SII-Mapas y advierte el carácter referencial de su localización y dimensiones.
- [SII, estructura de archivo para Detalle Catastral de Bienes Raíces](https://www.sii.cl/bbrr/descargas/estructura_detalle_catastral.pdf). Documenta campos como código de comuna, manzana, predial, dirección, avalúo, destino y superficie de terreno.
- [ChileAtiende, consulta de avalúos y certificados de bienes raíces](https://www.chileatiende.gob.cl/fichas/3160-consulta-de-avaluos-y-certificados-de-bienes-raices). Recuerda que el certificado de avalúo es tasación fiscal y no acredita dominio.
- [Catastral.cl](https://catastral.cl/) y [repositorio de metodología de Catastral.cl](https://github.com/crishernandezmaps/catastral.cl). Plataforma y pipeline de extracción, vectorización y distribución de datos catastrales del SII.
- [BIDAT, SIVUST - Vulnerabilidad Socioterritorial](https://bidat.gob.cl/directorio/SIVUST%20-%20Vulnerabilidad%20Socioterritorial). Portal para descargar mapas y bases del IGVUST en UV, comunas y regiones.
- Aurenhammer, F. (1991). [“Voronoi Diagrams — A Survey of a Fundamental Geometric Data Structure”](https://doi.org/10.1145/116873.116880). *ACM Computing Surveys*, 23(3), 345–405. Referencia clásica sobre diagramas de Voronoi.
- Okabe, A., Boots, B., Sugihara, K., & Chiu, S. N. (2000). *Spatial Tessellations: Concepts and Applications of Voronoi Diagrams*. Wiley. Obra de referencia sobre teselaciones espaciales.
- Crommelinck, S., Koeva, M., Yang, M. Y., & Vosselman, G. (2019). [“Application of Deep Learning for Delineation of Visible Cadastral Boundaries from Remote Sensing Imagery”](https://www.mdpi.com/2072-4292/11/21/2505). *Remote Sensing*, 11(21), 2505.
- Hong, R., Park, S., Jang, D., et al. (2021). [“Development of a Parcel-Level Land Boundary Extraction Algorithm for Aerial Imagery of Regularly Arranged Agricultural Areas”](https://www.mdpi.com/2072-4292/13/6/1167). *Remote Sensing*, 13(6), 1167.
- Grift, J., Persello, C., & Koeva, M. N. (2023). [“Cadastral Boundary Delineation using Deep Learning and Remote Sensing Imagery: State of the Art and Future Developments”](https://research.utwente.nl/en/publications/cadastral-boundary-delineation-using-deep-learning-and-remote-sen/). FIG Working Week 2023.
- Chen, J. et al. (2026). [“Artificial Intelligence in Cadastre: A Systematic Review of Methods, Applications, and Trends”](https://www.mdpi.com/2073-445X/15/3/411). *Land*, 15(3), 411.
- Nikiforova, A., Rizun, N., Ciesielska, M., Alexopoulos, C., & Miletić, A. (2023). [“Towards High-Value Datasets Determination for Data-Driven Development: A Systematic Literature Review”](https://arxiv.org/abs/2305.10234). Preprint.
