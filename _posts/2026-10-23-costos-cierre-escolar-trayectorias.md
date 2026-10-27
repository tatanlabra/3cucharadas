---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extender mi tesis en 3 cucharadas (parte III): qué muestran las trayectorias después del cierre de una escuela"
subtitle: "Seguir a los estudiantes permite observar la transición, pero todavía no separa con certeza el cierre de las trayectorias que ya venían cambiando."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-10-26 23:20:00 -0300
categories: [datos, educacion, politica-publica]
tags: [educacion, cierre-escolar, trayectorias, causalidad, mineduc, datos-administrativos, duckdb, politica-publica]
description: "Trayectorias estudiantiles y cierres escolares en Chile: resultados post-piloto, límites causales y condiciones mínimas para una transición educativa responsable."
excerpt: "La comparación encuentra una diferencia en progresión, pero las cotas para los datos faltantes abarcan ambos signos. La evidencia sirve para diseñar transiciones; aún no para atribuir daños o beneficios al cierre."
author: clabra
lang: es
ref: costos-cierre-escolar-trayectorias
permalink: /datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/
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
math: false
toc: true
toc_sticky: true
comments: true
author_profile: true
distribution:
  social: false
  republish: []
  skip_reason: "Candidata local: la difusión se habilita solo después del check editorial humano y de la publicación canónica."
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
---

Cuando una escuela cierra, la pregunta pública no termina al encontrar otra en el mapa. Importa saber si sus estudiantes continuaron matriculados, avanzaron de curso y mantuvieron una asistencia regular. También importa distinguir lo ocurrido después del cierre de lo que habría ocurrido si la escuela hubiese seguido abierta.
{: .text-justify}

La comparación más reciente estima que el cambio entre antes y después en la **proporción observada sin matrícula o con avance inferior al curso esperado al año siguiente —indicador resumido como «falla de progresión o rezago»— fue 5,29 puntos porcentuales mayor entre los estudiantes expuestos que en el grupo de comparación**. El intervalo de confianza conservador del 95 % —el rango de incertidumbre producido por el procedimiento— va de **2,08 a 8,51 puntos**. Sin embargo, al incorporar escenarios para los registros de progresión que faltan, las cotas van de **−1,15 a 10,98 puntos porcentuales**. Ese rango abarca ambos signos. El resultado es, por tanto, **inconcluso**: no demuestra daño, beneficio ni ausencia de efecto.
{: .text-justify}

El ejercicio presenta una **reestimación posterior al piloto**; no constituye una confirmación independiente. La base enlaza **79.709.054 registros de matrícula** y **73.873.835 de rendimiento** entre 2004 y 2025. Su escala permite seguir trayectorias y detectar problemas que un agregado escolar oculta, pero no crea por sí sola el contrafactual —lo que habría sucedido sin el cierre— que exige una afirmación causal.
{: .text-justify}

<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->
<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->

La [parte I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) reconstruyó la evidencia histórica y separó los resultados que resistían de los que debían corregirse. La [parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) verificó qué cerró en el período reciente y mostró que una escuela cercana no es necesariamente el destino de los estudiantes.
{: .text-justify}

Esta tercera parte cambia la unidad de análisis: de establecimientos y mapas a trayectorias estudiantiles. Compara a estudiantes expuestos con otros de características observables parecidas, estima resultados escolares y convierte los límites encontrados en exigencias concretas para una transición. Tres preguntas ordenan el relato: qué cerró, qué ocurrió después y qué debería exigir la política pública.
{: .text-justify}

## Cucharada 1: ¿qué cerró y quién quedó expuesto?

### Un flujo estudiantil es una señal, no un acto administrativo

El punto de partida son 346 episodios registrados administrativamente como cierres de establecimientos que antes tenían matrícula. La definición estricta de la parte II conserva 330 cierres de una oferta educativa y aparta anexos, continuidades posibles y cambios administrativos. El seguimiento estudia a quienes estaban matriculados el año anterior y observa sus registros posteriores cuando el período lo permite.
{: .text-justify}

El destino de los estudiantes ayuda a revisar esa clasificación. Una transferencia muy concentrada hacia otro establecimiento puede ser compatible con una fusión, una continuidad institucional, una alternativa accesible o decisiones coincidentes de las familias. Ninguna de esas explicaciones queda demostrada por el flujo. Cambiar la identidad del episodio requiere un directorio, un acto del sostenedor u otra fuente institucional independiente.
{: .text-justify}

{: .table-caption}
**Tabla 1.** Lectura diagnóstica de los 346 episodios registrados como cierres

| Estado | Episodios | Lectura permitida |
|---|---:|---|
| Sin señal contradictoria | 266 | La trayectoria no contradice el cierre estricto; no constituye corroboración externa. |
| Continuidad candidata | 15 | Nombre, nivel o modalidad, o actividad posterior justifican una revisión documental. |
| Alerta no resuelta | 35 | La categoría no cambia mientras falte evidencia independiente. |
| Seguimiento incompleto | 30 | Son cierres de 2025 y todavía no se observa el año siguiente. |
{: .table--compact .table--scroll}

La tabla clasifica una sola vez cada uno de los 346 episodios. Las **45 alertas por destino concentrado** son un corte distinto y se superponen con esas categorías; no deben sumarse a ellas. Tampoco se convirtieron en cambios automáticos: hay **cero confirmaciones institucionales independientes** en esta fase y los 330 cierres estrictos continúan como referencia.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-1">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }} 1600w" alt="Dos carriles resumen el soporte de la reestimación post-piloto de 2016 a 2019. De 64 episodios históricos antes del soporte, 63 conservan al menos un estrato comparable y uno queda completamente fuera. De 6.581 observaciones estudiante-cohorte expuestas, 391 se excluyen y 6.190 permanecen. El universo de soporte contiene 82.753 observaciones estudiante-cohorte de comparación; las muestras finales cambian según el resultado." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 1</strong> — Cómo se forma la muestra comparable de la reestimación post-piloto. Los conteos agregados preceden la elegibilidad específica de cada resultado y sus unidades no deben sumarse. <span class="figure-source">Fuente: elaboración propia a partir de la reestimación post-piloto v3.1.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/sample-flow-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

La figura separa universo, episodios y observaciones. Una «observación estudiante-cohorte» cuenta a un estudiante dentro de una cohorte de cierre; no equivale necesariamente a una persona distinta en todo el conjunto. Esta precisión evita que el volumen aparente sea confundido con más casos independientes de los que realmente hay.
{: .text-justify}

La auditoría tampoco convierte el flujo en una lista de escuelas para cerrar o fusionar. La salida pública permanece agregada: no contiene identificadores, nombres, direcciones ni coordenadas de candidatos. Si una revisión futura corrige un episodio de la parte II, deberá dejar visible la fuente y la versión que justifican el cambio.
{: .text-justify}

## Cucharada 2: ¿qué ocurrió después del cierre?

### Dos resultados primarios y una conclusión incómoda

La reestimación se concentra en cierres de 2016 a 2019 y compara trayectorias antes y después del episodio. Se excluyen alertas de identidad y escuelas receptoras de la comparación principal. Para calcular la incertidumbre, se reconoce que los estudiantes de un mismo cierre comparten condiciones; una verificación adicional considera que el mismo estudiante puede reaparecer en los registros.
{: .text-justify}

### ¿Estamos comparando peras con peras?

La comparación usa diferencias en diferencias: calcula cuánto cambió cada grupo y luego resta ambos cambios. Antes de esa doble resta, reúne grupos de estudiantes con el mismo año, sexo, región, dependencia, ruralidad, nivel educativo y curso inicial. En simple: intentamos comparar peras con peras usando las características que sí observamos. Eso ayuda, pero no revela lo que nunca entró a la base, como ingreso familiar, educación de los padres, necesidades educativas especiales o fecha de anuncio del cierre.
{: .text-justify}

{: .table-caption}
**Tabla 2.** Similitud observada antes del cierre en la muestra ponderada

| Característica previa | Estudiantes expuestos | Grupo de comparación | Lectura |
|---|---:|---:|---|
| Edad promedio | 11,70 años | 11,70 años | Diferencia estandarizada: 0,000. |
| Asistencia promedio | 90,93 % | 91,68 % | Diferencia estandarizada: −0,079. |
| Promedio de notas | 5,62 | 5,67 | Diferencia estandarizada: −0,072. |
| Registro válido de asistencia y notas | 76,8 % | 96,2 % | Brecha de cobertura: −19,4 pp. |
{: .table--compact .table--scroll}

Las diferencias observadas son pequeñas después de ponderar, pero la disponibilidad del registro de rendimiento no lo es: falta con mucha mayor frecuencia entre los expuestos. La edad se observa en toda la muestra. La asistencia y las notas, en cambio, solo pueden compararse entre quienes tienen esos registros; allí la cobertura es 76,8 % entre los expuestos y 96,2 % en el grupo de comparación. Esta brecha advierte que una parte relevante de los expuestos queda menos visible. Por eso la tabla no certifica aleatorización ni comparabilidad sociodemográfica completa: muestra semejanza en lo observado y, al mismo tiempo, una selección de registros capaz de cambiar la conclusión.
{: .text-justify}

De los 63 episodios que conservan soporte general en la figura 1, cada resultado utiliza solo las cohortes donde su ventana de seguimiento y su registro anual son observables: 62 episodios en los dos resultados primarios y 58 en asistencia y notas. El primer resultado compara, antes y después, la proporción de estudiantes sin matrícula durante dos años consecutivos. No lo llamo deserción: la ausencia del registro escolar no revela por sí sola la razón ni el destino. El cambio del grupo expuesto supera en **+0,63 puntos porcentuales** al del grupo de comparación, con un intervalo conservador del 95 % de **−0,77 a 2,03 puntos**. La estimación reúne 3.666 observaciones expuestas y 49.944 de comparación, provenientes de 62 episodios de cierre.
{: .text-justify}

El segundo resultado compara, antes y después, la proporción sin matrícula o con avance inferior al curso esperado al año siguiente, resumida como **falla de progresión o rezago**. El cambio del grupo expuesto supera en **+5,29 puntos porcentuales** al del grupo de comparación y su intervalo conservador va de **2,08 a 8,51 puntos**. La estimación reúne 4.815 observaciones expuestas y 65.538 de comparación en 62 episodios de cierre. Pero la progresión no se observa para todos. Bajo escenarios extremos para esos datos faltantes, las cotas de **−1,15 a 10,98 puntos porcentuales** cruzan cero. Esa es la incertidumbre que decide la lectura pública.
{: .text-justify}

{: .table-caption}
**Tabla 3.** Reestimación posterior al piloto: diferencias observadas, no efectos causales

| Resultado | Diferencia estimada | Intervalo conservador del 95 % | Condición decisiva |
|---|---:|---:|---|
| No matrícula persistente por dos años | +0,63 pp | [−0,77; 2,03] | No equivale a deserción; la tendencia previa estimable se apoya en pocos episodios. |
| Falla de progresión o rezago: sin matrícula o bajo el curso esperado al año siguiente | +5,29 pp | [2,08; 8,51] | Cotas por datos faltantes: [−1,15; 10,98] pp. |
| Asistencia | −1,15 puntos | [−2,40; 0,10] | Exploratoria; exige asistencia válida y estado final promovido/reprobado observable. |
| Promedio de notas | −0,06 | [−0,14; 0,01] | Exploratorio; solo entre quienes tienen rendimiento observable. |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-2">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }} 1600w" alt="Reestimación post-piloto inconclusa de dos resultados primarios. La no matrícula persistente se estima en 0,63 puntos porcentuales, con un intervalo de menos 0,77 a 2,03; en la muestra distinta que incluye escuelas receptoras, en 0,71, con un intervalo de menos 0,69 a 2,12. La falla de progresión o rezago se estima en 5,29 puntos, con un intervalo de 2,08 a 8,51; en la muestra distinta con receptoras, en 5,09, con un intervalo de 1,94 a 8,23. Sus cotas por datos faltantes abarcan de menos 1,15 a 10,98 puntos. No son efectos causales confirmados." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 2</strong> — Reestimación post-piloto inconclusa, no efectos causales. El intervalo de progresión no cruza cero, pero sus cotas por datos faltantes sí; el solapamiento con el piloto y los supuestos no observados impiden atribuir causalidad. <span class="figure-source">Fuente: elaboración propia a partir de la reestimación post-piloto v3.1.</span> <span class="figure-data">Datos tabulares accesibles: <a href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-data.csv' | relative_url }}">estimaciones</a> y <a href="{{ '/assets/images/tesis-post3/missingness-bounds-data.csv' | relative_url }}">cotas por datos faltantes</a>.</span></figcaption>
</figure>

Asistencia y notas sirven para contextualizar; no cambian la conclusión principal. Se observan solo cuando existe un registro anual válido: en asistencia, además, el valor debe estar entre 1 y 100 y el estado final debe ser promovido o reprobado en ambos períodos. Esa exigencia reduce la muestra analítica a **3.871 observaciones expuestas** en **58 episodios** (frente a 63.591 de comparación en asistencia y 63.596 en notas), lo que cubre el **62,5 %** del soporte expuesto frente al **76,8 %** del grupo de comparación. Por eso esas filas son **exploratorias y condicionadas**; no describen a toda la población expuesta. Las cotas por datos faltantes se calcularon solo para progresión y no incorporan incertidumbre muestral. Para asistencia y notas no se estimaron cotas equivalentes, de modo que su incertidumbre por selección sigue abierta.
{: .text-justify}

Los 62 episodios de los dos resultados primarios entregan 61 grados de libertad nominales, pero su aporte es desigual. Al descontar esa concentración, equivalen aproximadamente a **21,1 episodios efectivos** para no matrícula y **21,9** para progresión; en los 58 episodios con rendimiento válido, asistencia y notas bajan a **17,7**. Los intervalos agrupados y la verificación *wild cluster* protegen mejor la incertidumbre, pero no crean episodios independientes ni reparan la selección o la falta de contrafactual.
{: .text-justify}

La idea de «episodios efectivos» puede entenderse con una sala de reuniones. Aunque haya 62 escuelas, unas pocas aportan una parte desproporcionada de los estudiantes y pesan más en el promedio. La conversación se parece entonces menos a escuchar 62 voces independientes y más a escuchar unas 21 con un volumen equilibrado. El cálculo no elimina escuelas ni cambia la estimación; hace visible cuánta información independiente sostiene el intervalo. En los resultados exploratorios esa base es todavía menor, una razón adicional para no convertir asistencia o notas en titulares causales.
{: .text-justify}

Tampoco basta con que los grupos se parezcan en las columnas disponibles. La doble resta sería causal solo si, sin cierre, ambos hubieran seguido trayectorias comparables. Esa trayectoria alternativa no se observa. La similitud previa, los intervalos agrupados y las pruebas de sensibilidad reducen explicaciones rivales específicas, pero no descartan que una decisión anticipada, un deterioro anterior o una pérdida selectiva de registros expliquen parte de la diferencia.
{: .text-justify}

El resultado sigue siendo inconcluso. Las reglas del análisis se fijaron después de observar el piloto, no existe una fecha de anuncio que permita separar anticipación y operación, y algunas pruebas previas descansan en pocos episodios. En la figura 2, la barra que incluye a las escuelas receptoras dentro del grupo de comparación entrega **+0,71 puntos porcentuales** en no matrícula ([−0,69; 2,12]) y **+5,09 puntos** en falla de progresión o rezago ([1,94; 8,23]), sobre muestras distintas (3.670 observaciones expuestas frente a 59.613 controles, y 4.822 frente a 79.058): las variantes que incluyen receptoras o mercados locales cambian la composición de la muestra y no son variaciones mecánicas de una misma comparación ni eliminan las cotas por datos faltantes de **−1,15 a 10,98 puntos**.
{: .text-justify}

¿Qué evidencia podría cambiar esta lectura? Una evaluación más firme necesitaría fijar el análisis antes de observar sus resultados, confirmar cada cierre con una fuente institucional y medir el mismo resultado antes y después del episodio. También tendría que mostrar que las conclusiones sobreviven a distintas definiciones de receptora, dependencia entre estudiantes y episodios, y pérdidas de seguimiento. En sentido contrario, afirmar que no existe un costo exigiría definir de antemano qué diferencia sería socialmente irrelevante y estimarla con precisión suficiente; que un intervalo incluya cero no cumple esa tarea.
{: .text-justify}

La separación entre zonas urbanas y rurales queda como exploración. La muestra rural es mucho menor y la comparación simultánea de varios grupos aumenta la posibilidad de destacar una diferencia fortuita. Antes de convertir esa señal en una recomendación territorial se necesitan más episodios, tiempos de viaje por red y datos de transporte, porque la misma distancia puede significar condiciones de acceso muy distintas.
{: .text-justify}

### Qué agrega —y qué no agrega— la literatura

La revisión dirigida utilizada aquí no encontró un signo universal. Los estudios incluidos describen disrupciones iniciales, recuperación posterior, pérdidas persistentes en algunos grupos y mejores resultados cuando el destino ofrece condiciones superiores (Engberg et al. 2012; Brummet 2014; Beuchert et al. 2018; Steinberg y MacDonald 2019). En las escuelas receptoras, además, una caída del promedio agregado puede reflejar cambio en la composición del alumnado antes que deterioro de quienes ya estudiaban allí (Taghizadeh 2020), mientras que la escasez de vacantes en establecimientos eficaces acota cuánto puede mejorar una reasignación (Abdulkadiroğlu, Pathak y Walters 2026). En secundaria, algunos trabajos encuentran riesgos en graduación o acceso postsecundario incluso cuando los puntajes se recuperan (Larsen 2020; Bross, Harris y Liu 2023; Kim 2024).
{: .text-justify}

Chile tampoco admite un traslado mecánico de resultados. Grau, Hojman y Mizala (2018) estiman aumentos en repitencia y deserción para otro período y diseño; Iocco (2024), en un preprint, encuentra un promedio de logro cercano a cero con heterogeneidad según el destino. Diferencias de resultado, cohorte, tratamiento y método impiden leer la cifra de 5,29 puntos —cuyas cotas por datos faltantes van de −1,15 a 10,98 puntos— como una réplica o una refutación de esos estudios.
{: .text-justify}

**Cápsula de reconstrucción histórica.** El antecedente chileno más cercano es [*Destructive Creation* (Documento de Trabajo 396, 2014)]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}), del que fui coautor. Su tabla 7 reportó una diferencia de **+1,46 puntos porcentuales** en ausencia del registro oficial por al menos dos años, sobre 682.217 estudiantes. La tabla 8 informó +1,74 puntos en una comparación restringida de 2.361 estudiantes y la tabla 14, +1,08 puntos en una muestra ampliada de 906.629. Son efectos marginales publicados de modelos probit, no resultados de la reestimación actual. Las tablas causales 5, 6, 7, 8 y 14 siguen **no comparables**: no se recuperaron el archivo original de estimación, el insumo analítico exacto ni la regla completa de transformaciones; además, la ecuación y las notas discrepan sobre los efectos fijos. Por eso estas cifras describen lo publicado, pero hoy no confirman ni corrigen su ejecución.
{: .notice--info .text-justify}

### Educación superior: una pregunta que queda abierta

<!-- higher-education-agenda:start -->
Para quienes cursaban enseñanza media, la trayectoria no termina en la última matrícula escolar: todavía importa saber si el cierre se relaciona con el ingreso oportuno a la educación superior, el tipo de institución y la selectividad del destino. Esa pregunta queda para una entrega posterior. Requiere microdatos individuales del SIES con procedencia oficial y, para distinguir rendición, postulación, admisión y matrícula, un enlace validado con datos del DEMRE. Como esos insumos no están acreditados para este ejercicio, aquí no se estiman ni se sugieren efectos postsecundarios. La agenda futura no condiciona la publicación de los resultados escolares de esta parte.
{: .notice--info .text-justify}
<!-- higher-education-agenda:end -->

## Cucharada 3: ¿cómo se protege una transición escolar?

### La evidencia sirve antes de resolver la causalidad

Un resultado inconcluso no obliga a esperar con los brazos cruzados. Ya permite identificar qué información falta antes de reorganizar una red y qué debería seguirse después. La caída de matrícula puede abrir un diagnóstico; por sí sola no recomienda una fusión ni un cierre.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-3">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }} 1600w" alt="De 346 episodios, 339 tienen tres años preevento completos y 323 tienen cinco. La clasificación contiene 266 sin señal contradictoria, 15 candidatos de continuidad, 35 alertas no resueltas y 30 episodios sin seguimiento posterior completo. Hay 45 alertas posteriores al cierre y cero confirmaciones institucionales; el procesamiento automático solo permite observación." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 3</strong> — Cobertura y límites de la auditoría territorial. Seguimiento longitudinal y alertas de flujo no sustituyen evidencia sobre capacidad, acceso, demografía o decisiones institucionales. <span class="figure-source">Fuente: elaboración propia a partir de directorios MINEDUC y la auditoría longitudinal.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/territorial-audit-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

{: .table-caption}
**Tabla 4.** Información mínima para decidir y evaluar una transición

| Antes de decidir | Durante la transición | Después del cambio |
|---|---|---|
| Distinguir establecimiento, sede, nivel, fusión y cambio de Rol Base de Datos (RBD). | Asignar vacantes reales y apoyos a cada estudiante. | Seguir matrícula, asistencia, progresión, notas y bienestar. |
| Registrar fecha de anuncio y participación de la comunidad. | Medir tiempo de viaje, accesibilidad y continuidad de compañeros. | Observar también a estudiantes y equipos de las receptoras. |
| Verificar capacidad, dotación y calidad previa de los destinos. | Financiar la carga receptora y la continuidad pedagógica. | Publicar alertas, correcciones y responsabilidades con plazos. |
{: .table--compact .table--scroll}

El cuadro y la figura 3 —donde los 30 cierres de 2025 con seguimiento incompleto aparecen rotulados como censurados a la derecha porque aún no transcurre su año siguiente— cambian la carga de la prueba. Una autoridad no debería suponer que existe continuidad porque hay otra escuela cerca o porque varios estudiantes llegaron al mismo lugar. Debe demostrar que existen cupos, acceso seguro, recursos receptores y apoyos suficientes; luego, observar si la transición funcionó para estudiantes desplazados y para quienes ya estaban en la escuela receptora.
{: .text-justify}

Los Servicios Locales de Educación Pública (SLEP) y el Sistema de Admisión Escolar (SAE) tampoco son instrumentos causales automáticos. Podrían modificar coordinación, destinos o carga receptora, pero también afectan directamente recursos, vacantes y trayectorias: eso rompe la condición de que un instrumento opere solo mediante el cierre. La caída de matrícula, el tamaño escolar y las perturbaciones locales fallan por razones parecidas; predicen el cierre, pero también pueden afectar los resultados. Sin una regla administrativa o un sorteo documentado que supere relevancia, exclusión, monotonicidad, anticipación e interferencia, estimar una variable instrumental produciría precisión aparente, no identificación. Por eso no se ejecuta una regresión instrumental en esta versión.
{: .text-justify}

## Cierre: seguir trayectorias cambia la pregunta pública

La parte I reconstruyó qué sabíamos; la parte II precisó qué establecimientos cerraron y qué oferta apareció cerca. Esta tercera parte sigue a los estudiantes y muestra por qué el mapa era insuficiente: destino no es continuidad, y continuidad observada no es un contrafactual.
{: .text-justify}

El hallazgo más visible —un cambio 5,29 puntos porcentuales mayor entre los estudiantes expuestos que en el grupo de comparación— debe permanecer junto a sus cotas de **−1,15 a 10,98 puntos**. Separarlos produciría una certeza que el análisis no tiene. El aporte de esta entrega es más exigente: convertir registros masivos en un sistema de preguntas verificables para proteger transiciones sin fabricar una respuesta causal.
{: .text-justify}

Un resultado inconcluso sí permite fijar resguardos prudenciales hoy: no tratar la cercanía como continuidad, no reorganizar una red sin verificar cupos y apoyos, y seguir a cada estudiante durante la transición. Estos resguardos no son efectos estimados de esas decisiones. También obligan a publicar qué información falta y a corregir la decisión si las alertas muestran que el destino no estaba preparado.
{: .text-justify}

El siguiente paso analítico no es buscar otro modelo hasta obtener una cifra atractiva. Es conseguir fechas de anuncio, evidencia institucional, capacidad y accesibilidad de las receptoras, observación menos selectiva y una evaluación independiente. Solo entonces será posible distinguir mejor entre el costo de cerrar, el deterioro que precedió al cierre y las condiciones del destino.
{: .text-justify}

### Transparencia y alcance de las fuentes

La tesis y esta extensión son de mi autoría; no constituyen una réplica independiente. También fui coautor del documento de trabajo de 2014. Esa relación puede favorecer hipótesis heredadas, por lo que la reconstrucción histórica y el reanálisis actual se mantienen separados y sus discrepancias deben permanecer visibles.
{: .text-justify}

No recibí financiamiento para este trabajo y declaro no tener conflictos de interés. Mi única afiliación institucional es el Ministerio de Desarrollo Social y Familia de Chile, que no financió, encargó, supervisó ni revisó este trabajo; sus posiciones no están representadas por estas conclusiones. Utilicé asistentes de inteligencia artificial para apoyar programación, búsqueda bibliográfica, control de calidad, revisión de prosa y revisión adversarial. Las decisiones metodológicas y editoriales, la verificación de fuentes y la responsabilidad por las afirmaciones y resultados son mías.
{: .text-justify}

---

## Referencias

<div class="post-references" markdown="1">

Abdulkadiroğlu, Atila, Parag A. Pathak, and Christopher R. Walters. 2026. [“Who Gets What in Education: Can School Matching Improve Student Achievement?”](https://doi.org/10.3386/w34936) NBER Working Paper 34936.

Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen, and Nina Smith. 2018. [“The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?”](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47.

Bross, Whitney, Douglas N. Harris, and Lihan Liu. 2023. [“The Effects of Performance-Based School Closure and Restart on Student Performance.”](https://doi.org/10.1016/j.econedurev.2023.102368) *Economics of Education Review* 94: 102368.

Brummet, Quentin. 2014. [“The Effect of School Closings on Student Achievement.”](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–24.

Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. [“Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?”](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203.

Grau, Nicolás, Daniel A. Hojman, Cristián Labra, and Alejandra Mizala. 2014. [“Destructive Creation: School Turnover and Educational Attainment.”]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}) Documento de Trabajo 396, Universidad de Chile.

Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. [“School Closure and Educational Attainment: Evidence from a Market-Based System.”](https://doi.org/10.1016/j.econedurev.2018.05.003) *Economics of Education Review* 65: 1–17.

Iocco, Maria Pia. 2024. [“Impact of Planned School Closures on Academic Performance: Evidence from Chile.”](https://doi.org/10.2139/ssrn.4808834) SSRN preprint.

Kim, Jeonghyeok. 2024. [“The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes.”](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963.

Larsen, Matthew F. 2020. [“Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment.”](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980.

Steinberg, Matthew P., and John M. MacDonald. 2019. [“The Effects of Closing Urban Schools on Students’ Academic and Behavioral Outcomes: Evidence from Philadelphia.”](https://doi.org/10.1016/j.econedurev.2018.12.005) *Economics of Education Review* 69: 25–60.

Taghizadeh, Jonas Larsson. 2020. [“Are Students in Receiving Schools Hurt by the Closing of Low-Performing Schools? Effects of School Closures on Receiving Schools in Sweden 2000–2016.”](https://doi.org/10.1016/j.econedurev.2020.102020) *Economics of Education Review* 78: 102020.

</div>
