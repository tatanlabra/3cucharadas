---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extender mi tesis en 3 cucharadas (parte III): qué muestran las trayectorias después del cierre de una escuela"
subtitle: "En las 19 cohortes medibles, el aumento estimado del rezago o la salida del registro fue mayor entre quienes perdieron su escuela que entre sus pares. Todavía no puedo atribuir esa diferencia al cierre."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-11-07 20:30:00 -0300
categories: [datos, educacion, politica-publica]
tags: [educacion, cierre-escolar, trayectorias, causalidad, mineduc, datos-administrativos, duckdb, politica-publica]
description: "Trayectorias estudiantiles y cierres escolares en Chile: resultados post-piloto, límites causales y condiciones mínimas para una transición educativa responsable."
excerpt: "En todas las cohortes medibles, la brecha de progresión es positiva; en la ventana principal, las cotas para los datos faltantes abarcan ambos signos. La evidencia sirve para diseñar transiciones; aún no para atribuir daños o beneficios al cierre."
author: clabra
lang: es
ref: costos-cierre-escolar-trayectorias
permalink: /datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/
audio:
  duracion_s: 591
  fecha: "2026-11-01"
  generador: NotebookLM (Google)
  voces: 2
  idioma: es
  plataformas:
    - nombre: Spotify
      url: https://open.spotify.com/episode/4VIIXt7nDk8RwrtkqEVVZ7
    - nombre: Apple Podcasts
      url: https://podcasts.apple.com/cl/podcast/id6811713988
header:
  teaser: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/og-1200x630.webp
  og_image_alt: "Estudiantes y pupitres recorren caminos ramificados desde una escuela cerrada hacia distintas escuelas, como metáfora de una transición educativa incierta."
  overlay_image: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/teaser-mobile-640x360.webp
visual_id: costos-cierre-escolar-trayectorias
editorial_contract: societal-contribution-v1
table_contract: explicit-v1
math: true
toc: true
toc_sticky: true
comments: true
author_profile: true
distribution:
  social: true
  republish: []
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
    audio: generated
---

Cuando una escuela cierra, encontrar otro edificio no basta. Una familia necesita saber si habrá una vacante real, si el traslado es posible y si su hijo o hija seguirá matriculado y avanzará de curso. En la [parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) mostré por qué la escuela más cercana rara vez describe por sí sola el destino de los estudiantes. Aquí sigo la trayectoria escolar después del cierre, con una pregunta más exigente: ¿qué cambió frente a alumnos comparables y qué parte de esa diferencia ya venía de antes?

<aside class="notice--primary" markdown="1">
**Hallazgo.** En 19 cohortes medibles, la brecha estimada —diferencia entre el cambio de expuestos y el de controles— fue positiva; el agregado ponderado por expuestos alcanzó **+9,11 puntos porcentuales** y sus cotas por faltantes tampoco cruzan cero, sin error muestral incorporado.

**Comparación.** Seguí **78.972 observaciones estudiante-cohorte** vinculadas a **1.141 cierres regulares** con soporte, frente a **734.472 controles**.

**Límite.** La fragilidad previa impide atribuir toda la brecha al cierre. En 2016–2019, las cotas por datos faltantes abarcan **−1,15 a +10,98 puntos**.
</aside>

Reconstruí la historia con matrícula y rendimiento del MINEDUC entre 2004 y 2025. Primero separo cierres de posibles continuidades administrativas; después comparo las trayectorias; finalmente traduzco lo aprendido en resguardos que podrían verificarse antes, durante y después de una transición. Son tres preguntas distintas: qué unidad salió del sistema, qué les ocurrió a sus estudiantes y qué debe comprobar una autoridad para no perderles el rastro. La [nota metodológica y sus tablas completas]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}) conserva reglas, sensibilidad y fuentes.

<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->
<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->

{% include thesis-series-nav.html current=3 %}
## Cucharada 1: ¿qué cerró y quién quedó expuesto?

Una escuela puede dejar de figurar bajo su código oficial sin que sus alumnos pierdan la misma oferta educativa. Una sede puede pasar a otro identificador; un establecimiento completo puede trasladarse en bloque. Contar esos casos como cierres dispersos alteraría la comparación posterior. Por eso construí la Regla de Cierre Escolar Inferido desde los Datos, **RCID v1**, como tres filtros: D0 detecta salidas administrativas; D1 aparta anexos y continuidades de código; D2 aparta traslados muy concentrados hacia un único receptor. El flujo es una señal para revisar, no una resolución jurídica ni prueba de fusión. <span id="fig-post3-1"></span>Los [criterios exactos y el diagrama de cobertura]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#fig-post3-1) están en el anexo.

El filtro D2 deja **1.648 cierres limpios** con año posterior observado en 2005–2025. Para medir avance de curso uso un universo más acotado: **1.177** cierres incluían estudiantes de educación regular en grados observables y **1.141** hallaron controles comparables. De ahí provienen las **78.972 observaciones estudiante-cohorte expuestas** y las **734.472 de control**: son registros en cohortes, no necesariamente personas distintas. Las escuelas solo de párvulos, educación especial, adultos o cuarto medio no responden esta pregunta de progresión; su ausencia del análisis no equivale a ausencia de costo. El [desglose D0/D1/D2 y los universos]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a1) permite seguir cada exclusión.

La comparación tampoco parte de dos grupos idénticos. En 2016–2019, la proporción de estudiantes con al menos un cambio de escuela entre G−3 y G−1 era **47,04 %** entre los expuestos y **30,52 %** en los controles. Las escuelas que cerrarían tenían menos convenio SEP y menos Jornada Escolar Completa. En cambio, edad y rezago previo estaban prácticamente equilibrados por el emparejamiento. Esta mezcla importa: una diferencia posterior puede recoger tanto el cierre como procesos de desgaste que ya estaban activos. Si familias con más recursos salieron antes del último año abierto, el grupo observado también llega seleccionado. La [tabla de características previas]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a3) muestra el contraste completo y la cobertura de cada variable.

El período reciente permite comprobar por qué esa clasificación no es una simple limpieza de planilla. Entre 2016 y 2025 aparecieron **346 episodios** de salida con matrícula previa; D1 dejó **330 cierres estrictos de oferta**, mientras D2 apartó los flujos altamente concentrados antes de medir trayectorias. Había **45 alertas por destino concentrado** que se superponían con otras categorías, sin confirmación institucional independiente en ese corte. No las sumé como una clase nueva de cierre ni convertí su flujo en una resolución de la SEREMI. Si más adelante llega un documento de continuidad, el caso puede reclasificarse y cambiar el universo. La [lectura diagnóstica de los 346 episodios]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a2) deja visible esa incertidumbre.

Con ese universo definido, la segunda pregunta deja de ser cuántos códigos desaparecieron y pasa a ser qué trayectorias siguieron quienes estaban matriculados antes del cierre.
## Cucharada 2: ¿qué ocurrió después del cierre?

Llamo **G** al primer año sin matrícula en la escuela de origen y **G−1** a su último año abierto. Para la progresión comparo el curso observado dos años antes (G−2) con el que correspondería al año siguiente del cierre (G+1). Sin matrícula o con avance inferior al curso esperado al año siguiente es lo que llamo **falla de progresión o rezago**: el indicador reúne dos situaciones que el registro no siempre separa. Salir del registro no es automáticamente deserción. El análisis compara el cambio de estudiantes expuestos y controles antes y después, cohorte por cohorte; no reduce veinte años a una sola fotografía. Las especificaciones y las [tablas por régimen]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a4) quedan disponibles para inspección.

El seguimiento proviene de **79.709.054 registros de matrícula** y **73.873.835 de rendimiento** entre 2004 y 2025. Para cada año de cierre formé controles de escuelas sin cierre registrado en el universo del cálculo y excluí a estudiantes expuestos alguna vez; después estimé contrastes por cohorte y los agregué con pesos explícitos. La literatura sobre diferencias en diferencias escalonadas orienta esa separación[^callaway2021][^sun2021][^roth2023], pero el cálculo no reproduce exactamente un estimador de autoría nombrada. La comparación todavía requiere supuestos sobre las trayectorias que habrían seguido los alumnos sin cierre y sobre la ausencia selectiva de datos. Por eso leo los intervalos junto a las cotas y a las características previas, no como confirmaciones independientes de una misma causa.

La figura 1 muestra la serie completa. En **19 cohortes estimables** de progresión, todas las estimaciones puntuales fueron positivas. La media ponderada por estudiantes expuestos alcanzó **+9,11 puntos porcentuales** (intervalo de confianza del 95 %: **+5,34 a +12,88**; cotas de peor caso por datos faltantes: **+0,43 a +16,21**). Con igual peso por cohorte fue **+7,55 puntos**; el modelo de efectos aleatorios entregó **+6,29** y una heterogeneidad alta (**I² = 76,5 %**). Son resúmenes de brechas bajo distintos pesos, no tres efectos independientes. La no matrícula persistente por dos años mostró **+1,38 puntos** en el agregado ponderado por expuestos. Las 20 cohortes de cierres no tienen el mismo seguimiento: 19 permiten progresión y 17 no matrícula por dos años, por los bordes del panel.
<figure class="post3-figure data-visualization" id="fig-post3-2">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }} 1600w" alt="Infografía en tres paneles bajo la regla RCID v1 con 1.141 episodios con soporte entre 2005 y 2024. El panel A muestra las 19 cohortes anuales estimables de falla de progresión o rezago entre 2006 y 2024: las 19 son positivas, con rango de 0,94 a 28,22 puntos porcentuales, mediana de 7,18 y agregado ponderado por expuestos de +9,11 puntos (intervalo de 5,34 a 12,88 y cotas de Manski de +0,43 a +16,21 puntos). El panel B resume la atenuación por régimen institucional desde 12,15 puntos en 2005–2010 y 7,82 en 2011–2015 hasta 5,29 en 2016–2019 (con cotas por datos faltantes de menos 1,15 a 10,98 puntos), 2,70 en 2020–2022 y 2,59 en 2023–2024. El panel C muestra las brechas basales en G menos 1 tras el pareo exacto: la elegibilidad SEP es similar (−1,07 puntos), pero los expuestos asisten a escuelas con menos convenio SEP (−10,06 puntos), menos JEC (−18,54 puntos), menor cobertura de acta (−19,24 puntos) y mayor rotación previa (+16,52 puntos)." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 1</strong> — Serie completa 2005–2024 bajo la regla RCID v1: estimaciones anuales (2006–2024), atenuación en las cinco etapas institucionales y brechas de caracterización de NNA en G−1. <span class="figure-source">Fuente: elaboración propia a partir del panel longitudinal 2004–2025 del MINEDUC.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

La perspectiva histórica cambia la interpretación del zoom reciente. Entre **2005 y 2010** hubo **521 cierres** con soporte y **36.984 observaciones expuestas**: la brecha de progresión fue **+12,15 puntos porcentuales**, con intervalo **+3,78 a +20,52** y cotas **+3,49 a +18,83**. En **2011–2015** hubo **502 cierres** y **31.512 observaciones expuestas**, con brecha **+7,82 puntos** y cotas **−2,11 a +16,18**. Ambos períodos reúnen **89,7 %** de los cierres regulares y **86,7 %** de las observaciones expuestas. Después, las estimaciones puntuales se atenúan: **+2,70** en 2020–2022 y **+2,59** en 2023–2024. Esto describe épocas distintas; no identifica el efecto aislado de la SEP, la Ley de Inclusión ni la pandemia. Cambiaron también los establecimientos que cerraban, los registros, la promoción y el tamaño de las muestras.

El corte **2016–2019** se especificó después de observar un piloto con estudiantes y desenlaces solapados, pero antes de ejecutar la reestimación v3 completa; **no fue un prerregistro independiente**. La elección aprovechó el directorio estandarizado desde 2015, años previos observables y un período anterior a la pandemia. Representa **63 de los 1.141 episodios con soporte** y **6.190 de las 78.972 observaciones expuestas**. Es un zoom con medición y sensibilidad más exigentes, no un sustituto de las dos décadas. En él, la no matrícula por dos años fue **+0,63 puntos porcentuales** frente a controles (intervalo conservador **−0,77 a +2,03**); el rango incluye cero y el indicador tampoco aclara dónde estudia quien salió del registro. La figura 2 de esta página concentra las dos lecturas primarias; las [tablas detalladas]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a5) conservan denominadores y resultados exploratorios.

La falla de progresión o rezago en ese corte fue **+5,29 puntos porcentuales** (intervalo conservador **+2,08 a +8,51**), pero las cotas sin supuestos para desenlaces faltantes[^manski2003] van de **−1,15 a +10,98 puntos**. El cero queda dentro de las cotas: el resultado reciente es **inconcluso por sí solo**, aunque su estimación puntual sea positiva. El dato falta para **3,60 %** de los expuestos y **2,15 %** de los controles. En los cierres con al menos 90 % de actas válidas, las cotas pasan a **+0,09 a +7,84**, pero esa submuestra cubre solo **38 %** de las observaciones expuestas con desenlace y sus cotas no incorporan error muestral. Seleccionar establecimientos por cobertura puede introducir otras diferencias; no transforma la lectura del conjunto.
<figure class="post3-figure data-visualization" id="fig-post3-3">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }} 1600w" alt="Reestimación post-piloto inconclusa de dos resultados primarios. La no matrícula persistente se estima en 0,63 puntos porcentuales, con IC de menos 0,77 a 2,03; en la muestra distinta que incluye escuelas receptoras, 0,71, con IC de menos 0,69 a 2,12. La falla de progresión o rezago se estima en 5,29 puntos, con IC de 2,08 a 8,51; en la muestra distinta con receptoras, 5,09, con IC de 1,94 a 8,23. Sus límites por datos faltantes abarcan de menos 1,15 a 10,98 puntos. No son efectos causales confirmados." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 2</strong> — Corte 2016–2019 especificado después del piloto: reestimación inconclusa, no efectos causales. El intervalo de progresión no cruza cero, pero sus cotas por datos faltantes sí; el solapamiento con el piloto y los supuestos no observados impiden atribuir causalidad. <span class="figure-source">Fuente: elaboración propia a partir de la reestimación post-piloto.</span> <span class="figure-data">Datos tabulares accesibles: <a href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-data.csv' | relative_url }}">estimaciones</a> y <a href="{{ '/assets/images/tesis-post3/missingness-bounds-data.csv' | relative_url }}">cotas por datos faltantes</a>.</span></figcaption>
</figure>

El tamaño de la ventana reciente también importa. Aunque **62 cierres** tienen ventana observable para los dos resultados primarios, unos pocos concentran muchos alumnos. Por ese desequilibrio, la información pesa como **21,1 episodios efectivos** para no matrícula y **21,9** para progresión; asistencia y notas bajan a **17,7**. Sus diferencias son exploratorias porque requieren actas válidas en ambos períodos: solo **3.871 observaciones expuestas**, el **62,5 %** del soporte expuesto, las conservan. Una estimación precisa entre alumnos con acta no representa necesariamente a quienes carecen de ella. El anexo muestra [cobertura, comparabilidad y resultados secundarios]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a6).

Ni las pruebas de tendencias previas ni los ajustes de muestra resuelven los datos faltantes. Tres placebos previos al cierre en 2016–2019 fueron **+0,16, +0,30 y +0,40 puntos**; una sensibilidad lineal simplificada indica que un sesgo posterior de **2,07 puntos** anularía la exclusión de cero del intervalo convencional. Es una prueba distinta de las cotas de faltantes y no se combina automáticamente con ellas. Entre alumnos estables desde G−2, la brecha de progresión fue **+3,87 puntos**; entre entrantes tardíos, **+9,58**. La diferencia entre esos grupos advierte sobre selección previa, aunque ninguno ofrece un contrafactual perfecto. Los [supuestos y cálculos de sensibilidad]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tendencias-y-datos-faltantes) siguen en el anexo.

También examiné a qué escuelas llegaron **4.362** observaciones expuestas que reaparecieron matriculadas en G. Si la receptora tenía mayor tasa de aprobación previa que el origen, la brecha de progresión fue **+2,03 puntos**; con aprobación igual o menor, **+5,38**. La diferencia entre ambos grupos, **−3,35 puntos**, es descriptiva y carece de intervalo propio. Las familias eligen destino y el contraste excluye a quienes no reaparecieron; no estima el efecto de asignar una receptora de mayor calidad. La [comparación de receptoras]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#calidad-de-la-receptora) documenta la definición previa de calidad.

La figura histórica y el zoom responden preguntas relacionadas con grados de respaldo distintos. La primera revela una brecha extendida y muy heterogénea; el segundo deja visible cómo faltantes y selección limitan la atribución. Esa distinción prepara la pregunta pública: qué garantías exigir aun cuando el tamaño causal exacto siga abierto.
## Cucharada 3: ¿cómo proteger una transición escolar?

Una brecha observada con atribución causal incierta permite detectar dónde un procedimiento público debe producir evidencia, pero no demuestra que una medida específica vaya a reducirla. Antes de cerrar, una autoridad necesita saber si el episodio es una salida de oferta o una continuidad de código, sede o nivel; cuándo se anunció; y cuántos cupos reales, accesibles y adecuados existen. Durante el cambio importan traslado, apoyos y continuidad pedagógica. Después debe seguir matrícula, asistencia, curso y bienestar en las escuelas receptoras. La tabla ordena esas tareas como información exigible, no como efectos ya estimados.
{: .table-caption}
**Tabla 1.** Información mínima para decidir y evaluar una transición

| Antes de decidir | Durante la transición | Después del cambio |
|---|---|---|
| Distinguir establecimiento, sede, nivel, fusión y cambio de Rol Base de Datos (RBD). | Asignar vacantes reales y apoyos a cada estudiante. | Seguir matrícula, asistencia, progresión, notas y bienestar. |
| Registrar fecha de anuncio y participación de la comunidad. | Medir tiempo de viaje, accesibilidad y continuidad de compañeros. | Observar también a estudiantes y equipos de las receptoras. |
| Verificar capacidad, dotación y calidad previa de los destinos. | Financiar la carga receptora y la continuidad pedagógica. | Publicar alertas, correcciones y responsabilidades con plazos. |
{: .table--compact .table--scroll}

La propuesta se puede convertir en una evaluación concreta. Antes de decidir, habría que guardar una línea de base de los estudiantes y de las receptoras, además de fechas de anuncio, cupos y tiempos de viaje. Durante la reubicación, se registrarían apoyos efectivamente entregados, continuidad de curso y cambios de escuela. Después se seguiría a toda la cohorte, incluida la que desaparece del registro regular, con reglas claras de privacidad y cobertura. Con esa información sería posible distinguir implementación de resultado: que un cupo exista no dice si fue aceptado, que una matrícula aparezca no dice si hubo progresión, y un cambio posterior no demuestra por sí mismo qué lo causó.

Una constancia de alternativas no equivale a matrícula asegurada. La referencia sobre cierre voluntario de Castro Paredes (2013[^castroparedes2013]) da contexto administrativo, pero este análisis no verifica vacantes ni llegada efectiva. Por eso recomiendo confirmar cupos, transporte y apoyos antes de reorganizar, y dar seguimiento nominal durante al menos dos años con resguardo de privacidad. Estos **resguardos prudenciales no son efectos estimados de esas decisiones**; evaluarlos requiere registrar su implementación y comparar resultados. La cercanía por mapa, por sí sola, tampoco mide tiempo de viaje, admisión ni calidad de la receptora.

Este artículo no estima resultados de educación superior. La [parte IV]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/' | relative_url }}) extiende la pregunta con registros SIES y PAES/PDT. <span id="fig-post3-4"></span>La [figura de auditoría territorial]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#fig-post3-4) conserva el soporte de clasificación. Ese horizonte no reemplaza el seguimiento escolar inmediato: una transición puede mantener matrícula hoy y alterar opciones años después, o reflejar desventajas que ya existían antes del cierre.
## Cierre: seguir la trayectoria cambia la decisión

El recorrido comenzó por una distinción: una escuela que desaparece del directorio puede ser un cierre de oferta o una continuidad bajo otra forma. Al depurar esos episodios, seguí **78.972 observaciones estudiante-cohorte expuestas** en **1.141 cierres regulares**. La serie larga muestra una brecha positiva de falla de progresión o rezago en 19 cohortes medibles, con **+9,11 puntos porcentuales** al ponderar por expuestos; su magnitud varía entre épocas. En la ventana principal 2016–2019, la diferencia estimada es **+5,29 puntos**, pero las cotas por faltantes **−1,15 a +10,98** cruzan cero. La fragilidad de las escuelas y la rotación estudiantil previas siguen impidiendo llamar efecto del cierre a toda la brecha.

Esa incertidumbre no elimina la obligación práctica de comprobar continuidad. Verificar vacantes, traslados y apoyos, y seguir a quienes llegan a una receptora, es una respuesta prudencial a lo que el registro deja incompleto; no es una intervención cuya eficacia haya medido aquí. Para pasar de diagnóstico a decisión evaluable quedan **tres desafíos**:

1. **Acreditar el cierre.** Reunir resoluciones exentas y fechas de anuncio para distinguir jurídicamente cierres, recesos y reorganizaciones.
2. **Completar trayectorias.** Recuperar actas y desenlaces faltantes e integrar incertidumbre muestral, tendencias y selección en la sensibilidad del corte reciente.
3. **Medir la transición.** Registrar cupos, tiempos de viaje, apoyos y resultados en receptoras, incluida la situación de quienes no reaparecen matriculados.

La [parte IV]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/' | relative_url }}) sigue la trayectoria postsecundaria; conserva esta misma exigencia de separar lo observado de lo atribuible.

## Referencias

[^callaway2021]: Callaway, Brantly, and Pedro H. C. Sant'Anna. 2021. [“Difference-in-Differences with Multiple Time Periods.”](http://arxiv.org/pdf/1803.09015) *Journal of Econometrics* 225 (2): 200–230. [DOI](https://doi.org/10.1016/j.jeconom.2020.12.001) · [Scholar](https://scholar.google.com/scholar_lookup?title=Difference-in-Differences+with+multiple+time+periods&doi=10.1016%2Fj.jeconom.2020.12.001)

[^castroparedes2013]: Castro Paredes, Luis. 2013. [*Cierre voluntario de Establecimientos Educacionales*](https://obtienearchivo.bcn.cl/obtienearchivo?id=repositorio/10221/20674/5/Cierre%20voluntario%20de%20Establecimientos%20Educacionales_v2.pdf). Asesoría Técnica Parlamentaria, Biblioteca del Congreso Nacional de Chile (BCN), 12 de diciembre de 2013.

[^manski2003]: Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). New York: Springer. [Scholar](https://scholar.google.com/scholar_lookup?title=Partial+Identification+of+Probability+Distributions&doi=10.1007%2Fb97478)

[^roth2023]: Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–44. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)

[^sun2021]: Sun, Liyang, and Sarah Abraham. 2021. [“Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects.”](https://doi.org/10.1016/j.jeconom.2020.09.006) *Journal of Econometrics* 225 (2): 175–99. [Scholar](https://scholar.google.com/scholar_lookup?title=Estimating+dynamic+treatment+effects+in+event+studies+with+heterogeneous+treatment+effects&doi=10.1016%2Fj.jeconom.2020.09.006)
