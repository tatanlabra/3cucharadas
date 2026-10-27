---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extender mi tesis en 3 cucharadas (parte III): qué muestran las trayectorias después del cierre de una escuela"
subtitle: "Seguir a los estudiantes permite observar la transición, pero todavía no separa con certeza el cierre de las trayectorias que ya venían cambiando."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-10-27 04:00:00 -0300
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

### De la certeza documental a la Regla de Cierre Escolar Inferido desde los Datos (RCID v1)

Confirmar un cierre jurídico-administrativo exige revisar actas, resoluciones exentas de reconocimiento oficial y registros del sostenedor. Pero cuando se analizan veinte años de paneles masivos sin expediente físico por establecimiento, es indispensable transparentar un supuesto empírico falsable y reproducible que distinga una salida bruta de directorio de un cese real de oferta con desplazamiento estudiantil. Esa es la **Regla de Cierre Escolar Inferido desde los Datos (`RCID v1`)**, aplicada de manera uniforme en las tres entregas de esta serie mediante tres estratos anidados (D0 ⊃ D1 ⊃ D2):
{: .text-justify}

- **D0 (salida administrativa o de actividad bruta):** el establecimiento registra matrícula positiva en t−1, pasa a matrícula cero en t y no vuelve a registrar actividad docente en t+1 ni en años posteriores (o figura con estado de cierre en el directorio oficial).
- **D1 (cierre estricto de oferta educativa):** subconjunto de D0 que depura falsos cierres a nivel de establecimiento —reaperturas posteriores, cambios de código RBD con continuidad de local, anexos o sedes parciales y continuidades administrativas candidatas—.
- **D2 = RCID v1 (cierre inferido desde los datos depurado por flujo estudiantil):** subconjunto de D1 que exige observar al menos 5 estudiantes seguibles en t−1 y descarta las absorciones concentradas o fusiones de facto en las que un único establecimiento receptor concentra al menos el **70 %** de los estudiantes reubicados y al menos **15 alumnos** en t (con variante limpia en t+1 cuando la ventana posterior está completamente observada).

{: .table-caption}
**Tabla 2.** Jerarquía de la Regla de Cierre Escolar Inferido desde los Datos (`RCID v1`, D0 ⊃ D1 ⊃ D2) en las tres entregas (2005–2025)

| Estrato de la regla | Ventana histórica (2005–2015) | Ventana reciente (2016–2025) | Serie longitudinal (2005–2025) | Qué depura y cómo se usa en las partes I, II y III |
|---|---:|---:|---:|---|
| D0: salida administrativa o de actividad bruta | 1.635 | 346 | 1.981 | Cese de matrícula en t; contrasta con las 2.069 salidas brutas de directorio de 1992–2012 en la parte I. |
| D1: cierre estricto de oferta educativa | 1.477 | 330 | 1.807 | Depura 158 reaperturas o continuidades históricas y 16 continuidades candidatas o anexos recientes (base de la parte II). |
| D2 = RCID v1 (conservador, incluye censurados de 2025) | 1.382 | 296 | 1.678 | Depura además 95 absorciones históricas y 34 absorciones o alertas de flujo concentradas recientes (≥ 70 % y ≥ 15 alumnos). |
| D2 = RCID v1 (limpio con ventana t+1 observada) | 1.382 | 266 | 1.648 | Exige además observar el año t+1 completo (excluye los 30 episodios de 2025 censurados a la derecha); base principal de la parte III. |
{: .table--compact .table--scroll}

Separar D1 y D2 evita confundir una reorganización o absorción completa en un receptor único con la dispersión forzada del alumnado. En la parte II, pasar de los 330 cierres estrictos (D1) a los 296 de `RCID v1` (D2) reduce la mediana de matrícula previa de 44 a 39 estudiantes en t−2 y de 34 a 31 en t−1 (36 y 27 en la variante limpia de 266 cierres) y deja la diferencia ajustada de SIMCE en +0,017 desviaciones estándar (17 cierres con soporte, intervalo del 95 % que cruza cero). En esta parte III, la estimación principal excluye las alertas de flujo concentrado (trabajando sobre el estrato D2 limpio) y contrasta explícitamente su sensibilidad frente a incluir o excluir escuelas receptoras.
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
**Tabla 3.** Similitud observada antes del cierre en la muestra ponderada

| Característica previa | Estudiantes expuestos | Grupo de comparación | Lectura |
|---|---:|---:|---|
| Edad promedio | 11,70 años | 11,70 años | Diferencia estandarizada: 0,000. |
| Asistencia promedio | 90,93 % | 91,68 % | Diferencia estandarizada: −0,079. |
| Promedio de notas | 5,62 | 5,67 | Diferencia estandarizada: −0,072. |
| Registro válido de asistencia y notas | 76,8 % | 96,2 % | Brecha de cobertura: −19,4 pp. |
{: .table--compact .table--scroll}

Las diferencias observadas son pequeñas después de ponderar, pero la disponibilidad del registro de rendimiento no lo es: falta con mucha mayor frecuencia entre los expuestos. La edad se observa en toda la muestra. La asistencia y las notas, en cambio, solo pueden compararse entre quienes tienen esos registros; allí la cobertura es 76,8 % entre los expuestos y 96,2 % en el grupo de comparación. Esta brecha advierte que una parte relevante de los expuestos queda menos visible. Por eso la tabla no certifica aleatorización ni comparabilidad sociodemográfica completa: muestra semejanza en lo observado y, al mismo tiempo, una selección de registros capaz de cambiar la conclusión.
{: .text-justify}

Para auditar más a fondo si el emparejamiento exacto en G−1 compara trayectorias verdaderamente equivalentes, incorporamos once descriptores adicionales de caracterización de niños, niñas y adolescentes (NNA) y de su entorno institucional previo a partir de los registros de Subvención Escolar Preferencial (SEP), directorio, matrícula y rendimiento entre G−3 y G−1. El diagnóstico muestra dos caras simultáneas: mientras la elegibilidad socioeconómica individual (`PRIORITARIO_ALU` y `PREFERENTE_ALU`) y la sobreedad quedan prácticamente equilibradas tras estratificar por nivel y curso, la adscripción efectiva de la escuela a la SEP, la Jornada Escolar Completa (JEC), la conmutación intercomunal y la rotación escolar previa exhiben asimetrías estructurales que el emparejamiento demográfico básico no corrige.
{: .text-justify}

{: .table-caption}
**Tabla 4.** Caracterización ampliada de niños, niñas y adolescentes (NNA) en G−1 (cohortes 2016–2019, 6.190 expuestos y 82.753 controles)

| Descriptor previo en G−1 | Estudiantes expuestos | Grupo de comparación | Brecha (pp) | Lectura sustantiva para la identificación |
|---|---:|---:|---:|---|
| Estudiante prioritario SEP (`PRIORITARIO_ALU`) | 30,68 % | 32,32 % | −1,64 | Equilibrio cercano en vulnerabilidad socioeconómica prioritaria tras estratificar. |
| Estudiante preferente SEP (`PREFERENTE_ALU`) | 23,83 % | 23,26 % | +0,57 | Similitud en el segundo tramo de elegibilidad SEP. |
| Elegibilidad SEP total (prioritario o preferente) | 54,51 % | 55,58 % | −1,07 | La composición socioeconómica elegible individual es comparable en G−1. |
| Beneficiario efectivo SEP (`BEN_SEP`) | 37,63 % | 48,58 % | −10,95 | Pese a igual elegibilidad, los expuestos reciben menos cobertura efectiva SEP. |
| Escuela de origen con convenio SEP (`CONVENIO_SEP`) | 45,17 % | 55,23 % | −10,06 | Los cierres se concentran en sostenedores con menor adscripción institucional a SEP. |
| Escuela de origen con Jornada Escolar Completa (JEC) | 53,97 % | 72,51 % | −18,54 | Asimetría de oferta previa: menor dotación de jornada completa antes del cierre. |
| Conmutación intercomunal (residencia ≠ comuna escolar) | 38,59 % | 29,99 % | +8,60 | Mayor proporción de estudiantes que ya viajaban entre comunas antes del cierre. |
| Sobreedad ≥ 1 año respecto de la norma del curso | 33,86 % | 33,86 % | 0,00 | Equilibrio exacto inducido por el emparejamiento por edad, nivel y curso en G−1. |
| Sobreedad severa ≥ 2 años respecto del curso | 8,32 % | 8,32 % | 0,00 | Sin diferencia previa en rezago acumulado de dos o más años. |
| Inasistencia grave (< 85 % entre registros con acta) | 13,99 % | 11,14 % | +2,85 | Mayor fragilidad de asistencia previa entre quienes sí registran acta en G−1. |
| Repitencia previa en G−1 (entre registros con acta) | 5,49 % | 4,48 % | +1,01 | Ligeramente mayor reprobación en el año inmediatamente anterior al cierre. |
| Cambio de escuela entre G−2 y G−1 | 26,57 % | 16,53 % | +10,04 | Más de un cuarto de los expuestos ya venía rotando de establecimiento antes del cierre. |
| Al menos un cambio de escuela entre G−3 y G−1 | 47,04 % | 30,52 % | +16,52 | Casi la mitad de los expuestos experimentó movilidad previa: señal de fragilidad preexistente. |
{: .table--compact .table--scroll}

Esta radiografía ampliada refuerza por qué una diferencia ajustada no debe leerse de forma mecánica como efecto puro del cierre: aunque los NNA expuestos y sus controles tienen la misma edad, el mismo rezago acumulado previo y una proporción casi idéntica de alumnos prioritarios y preferentes (54,51 % frente a 55,58 %), los expuestos asistían a establecimientos con menor cobertura de convenio SEP (−10,06 pp) y de Jornada Escolar Completa (−18,54 pp), y casi la mitad (47,04 % frente a 30,52 %) ya había cambiado de establecimiento al menos una vez entre G−3 y G−1. Parte de las trayectorias ya venía tensionada antes de que el establecimiento saliera del registro.
{: .text-justify}

De los 63 episodios que conservan soporte general en la figura 1, cada resultado utiliza solo las cohortes donde su ventana de seguimiento y su registro anual son observables: 62 episodios en los dos resultados primarios y 58 en asistencia y notas. El primer resultado compara, antes y después, la proporción de estudiantes sin matrícula durante dos años consecutivos. No lo llamo deserción: la ausencia del registro escolar no revela por sí sola la razón ni el destino. El cambio del grupo expuesto supera en **+0,63 puntos porcentuales** al del grupo de comparación, con un intervalo conservador del 95 % de **−0,77 a 2,03 puntos**. La estimación reúne 3.666 observaciones expuestas y 49.944 de comparación, provenientes de 62 episodios de cierre.
{: .text-justify}

El segundo resultado compara, antes y después, la proporción sin matrícula o con avance inferior al curso esperado al año siguiente, resumida como **falla de progresión o rezago**. El cambio del grupo expuesto supera en **+5,29 puntos porcentuales** al del grupo de comparación y su intervalo conservador va de **2,08 a 8,51 puntos**. La estimación reúne 4.815 observaciones expuestas y 65.538 de comparación en 62 episodios de cierre. Pero la progresión no se observa para todos. Bajo escenarios extremos para esos datos faltantes, las cotas de **−1,15 a 10,98 puntos porcentuales** cruzan cero. Esa es la incertidumbre que decide la lectura pública.
{: .text-justify}

{: .table-caption}
**Tabla 5.** Reestimación posterior al piloto: diferencias observadas, no efectos causales

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

### ¿Por qué se eligió 2016–2019 y qué muestra la serie completa 2005–2024?

Una pregunta legítima al leer el corte principal es por qué la estimación se concentró en las cohortes **2016–2019** y no en cada año disponible entre **2004 y 2025**. La elección original no fue arbitraria ni respondió a buscar un signo particular: obedeció a cuatro restricciones simultáneas de los datos administrativos. Primero, el campo oficial de estado del establecimiento (`ESTADO_ESTAB`) recién se incorporó al directorio MINEDUC en el corte 2015, de modo que **2016** es la primera cohorte donde la transición contemporánea a estado de cierre se observa directamente año contra año. Segundo, exigir hasta nueve años de historia previa (G−9 a G−1) dentro de un panel que parte en 2004 empuja mecánicamente las cohortes con horizonte pre-evento completo hacia mediados de la década de 2010. Tercero, las cohortes **2020–2022** coinciden con el cierre sanitario y las reglas excepcionales de promoción durante la pandemia de COVID-19. Cuarto, las cohortes **2024–2025** sufren censura a la derecha para observar la no matrícula persistente de dos años (G+1 necesita al menos dos años posteriores al cierre).
{: .text-justify}

Sin embargo, la literatura moderna de diferencias en diferencias escalonadas con adopción en múltiples períodos (Callaway y Sant'Anna 2021; Sun y Abraham 2021; Roth et al. 2023) demuestra que podemos y debemos estimar cada cohorte anual G = 2005…2024 por separado frente a controles limpios aún no tratados, evitando las ponderaciones negativas de una regresión bidireccional de efectos fijos tradicional, y luego explicitar los rangos anuales, los subagregados por régimen institucional y el agregado de toda la serie bajo distintos esquemas de ponderación. Combinando el registro histórico de cierres de los directorios 2015 y 2025 con la regla `RCID v1` (D2), reconstruimos las **20 cohortes anuales de cierre entre 2005 y 2024**, que abarcan **1.141 episodios con soporte empírico**, **78.972 observaciones estudiante-cohorte expuestas** y **734.472 observaciones de comparación** en estratos exactamente emparejados.
{: .text-justify}

{: .table-caption}
**Tabla 6.** Estimaciones por cohorte anual (G = 2005–2024), rangos, subagregados por régimen y agregado de la serie completa

| Cohorte / Régimen / Agregado | Episodios con soporte | Expuestos (N) | Controles (N) | Falla de progresión o rezago (pp) | IC 95 % progresión (pp) | No matrícula persistente 2 años (pp) | IC 95 % no matrícula (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cohorte 2005 (borde inicial; sin pre-tendencia en G−2) | 46 | 1.981 | 48.273 | +3,99 | [−1,38; +9,36] | +2,62 | [−0,09; +5,33] |
| Cohorte 2006 (régimen pre-SEP) | 60 | 2.666 | 51.310 | +7,37 | [+3,16; +11,57] | +2,71 | [+0,11; +5,32] |
| Cohorte 2007 (régimen pre-SEP) | 65 | 3.747 | 50.114 | +5,22 | [+2,29; +8,15] | +2,18 | [+0,45; +3,92] |
| Cohorte 2008 (inicio de la SEP) | 59 | 3.164 | 53.788 | +5,07 | [+1,71; +8,43] | +1,93 | [−0,20; +4,05] |
| Cohorte 2009 (implementación temprana SEP) | 63 | 3.633 | 47.492 | +7,19 | [+2,82; +11,56] | +0,92 | [−0,87; +2,71] |
| Cohorte 2010 (terremoto 27F y ajuste de red) | 88 | 4.864 | 62.719 | +5,46 | [+2,15; +8,77] | −0,41 | [−1,29; +0,46] |
| Cohorte 2011 (movilización estudiantil y ajuste privado-subvencionado) | 98 | 6.809 | 69.927 | +4,16 | [+2,14; +6,19] | +0,62 | [−0,68; +1,91] |
| Cohorte 2012 (puesta en marcha del SAC) | 115 | 7.674 | 67.272 | +5,41 | [+2,72; +8,09] | +0,39 | [−0,30; +1,08] |
| Cohorte 2013 (régimen SAC) | 109 | 5.190 | 53.681 | +7,94 | [+5,42; +10,46] | +1,45 | [−0,01; +2,91] |
| Cohorte 2014 (antesala de la Ley de Inclusión) | 100 | 5.260 | 57.152 | +3,91 | [+1,76; +6,05] | +0,82 | [−0,02; +1,66] |
| Cohorte 2015 (promulgación Ley N.º 20.845 de Inclusión) | 105 | 7.018 | 51.073 | +7,62 | [+5,02; +10,23] | +1,62 | [+0,53; +2,71] |
| Cohorte 2016 (ventana principal post-piloto) | 17 | 1.074 | 13.798 | +3,27 | [−3,51; +10,05] | −0,29 | [−1,44; +0,86] |
| Cohorte 2017 (ventana principal post-piloto) | 14 | 540 | 12.690 | +4,79 | [−2,61; +12,18] | +0,12 | [−3,19; +3,43] |
| Cohorte 2018 (ventana principal post-piloto) | 14 | 1.842 | 19.729 | +5,78 | [+2,37; +9,19] | +1,33 | [−1,84; +4,50] |
| Cohorte 2019 (ventana principal post-piloto) | 17 | 1.359 | 19.321 | +6,44 | [−0,68; +13,57] | +0,62 | [−1,89; +3,12] |
| Cohorte 2020 (pandemia COVID-19; cierre presencial) | 40 | 7.839 | 20.694 | +10,64 | [−6,81; +28,09] | +1,00 | [−1,07; +3,06] |
| Cohorte 2021 (pandemia COVID-19; promoción flexible) | 18 | 661 | 8.590 | −1,18 | [−8,45; +6,08] | +2,18 | [−1,38; +5,73] |
| Cohorte 2022 (retorno presencial post-pandemia) | 12 | 509 | 6.530 | +22,55 | [−4,07; +49,17] | +2,23 | [−2,41; +6,87] |
| Cohorte 2023 (post-pandemia con ventana completa) | 18 | 932 | 9.546 | +15,72 | [+2,70; +28,74] | +1,52 | [−1,47; +4,51] |
| Cohorte 2024 (progresión 1 año observada; 2 años censurado en 2025) | 78 | 12.208 | 10.773 | +19,92 | [−3,83; +43,66] | 0,00 | [0,00; 0,00] |
| **Rango anual (mínimo a máximo; RIQ P25–P75)** | **12 a 115** | **509 a 12.208** | **6.530 a 69.927** | **−1,18 a +22,55 (RIQ: +4,63 a +7,70)** | **[−8,45; +49,17]** | **−0,41 a +2,71 (RIQ: +0,62 a +2,05)** | **[−3,19; +6,87]** |
| **Subagregado 2006–2010 (pre-SEP e inicio SEP)** | **335** | **18.074** | **265.423** | **+5,97** | **[+4,32; +7,62]** | **+1,24** | **[+0,47; +2,01]** |
| **Subagregado 2011–2015 (SAC y antesala Inclusión)** | **527** | **31.951** | **299.105** | **+5,75** | **[+4,64; +6,85]** | **+0,90** | **[+0,44; +1,36]** |
| **Subagregado 2016–2019 (ventana principal; cotas [−1,15; 10,98] pp)** | **62** | **4.815** | **65.538** | **+5,29** | **[+2,08; +8,51]** | **+0,63** | **[−0,77; +2,03]** |
| **Subagregado 2020–2022 (shock pandémico COVID-19)** | **70** | **9.009** | **35.814** | **+10,44** | **[−4,85; +25,74]** | **+1,16** | **[−0,68; +3,01]** |
| **Subagregado 2023–2024 (reactivación post-pandemia)** | **96** | **13.140** | **20.319** | **+19,62** | **[−2,46; +41,70]** | **+1,52** | **[−1,47; +4,51]** |
| **Agregado serie 2005–2024 (Callaway y Sant'Anna, ponderado por expuestos)** | **1.141** | **78.972** | **734.472** | **+9,11** | **[+5,34; +12,88]** | **+1,09** | **[+0,65; +1,53]** |
| **Agregado serie 2005–2024 (pesos iguales por cohorte anual)** | **1.141** | **78.972** | **734.472** | **+7,55** | **[+5,52; +9,57]** | **+1,24** | **[+0,75; +1,73]** |
| **Agregado serie 2005–2024 (precisión por varianza inversa; I² = 76,48 %)** | **1.141** | **78.972** | **734.472** | **+5,14** | **[+4,34; +5,95]** | **+0,67** | **[+0,33; +1,00]** |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-4">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }} 1600w" alt="Infografía de la serie escalonada 2005 a 2024 bajo la regla RCID v1 con 1.677 cierres entre 2005 y 2024 y 1.141 episodios con soporte. En las 20 cohortes anuales, la falla de progresión o rezago varía entre menos 1,18 y más 22,55 puntos porcentuales, con 5,29 puntos en la ventana 2016 a 2019 y cotas de datos faltantes de menos 1,15 a 10,98 puntos. El agregado de Callaway y Sant'Anna ponderado por expuestos es +9,11 puntos, con intervalo de 5,34 a 12,88 y cotas de Manski de +0,43 a +16,21 puntos." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 3</strong> — Auditoría de la serie completa 2005–2024 por cohorte anual, subagregados por régimen, agregación escalonada de Callaway y Sant'Anna y caracterización ampliada de NNA en G−1. En la última fila de la tabla 6, la cohorte 2024 registra 0,00 en la columna de dos años solo como marcador de celda censurada a la derecha (requiere 2026). <span class="figure-source">Fuente: elaboración propia a partir del panel 2004–2025 y el artefacto auditado de serie completa v1.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

La tabla 6 y la figura 3 despejan cualquier sospecha de selección oportunista de la ventana **2016–2019** y muestran tres regularidades de primer orden. Primero, entre **2006 y 2019** —catorce cohortes consecutivas previas a la pandemia— la diferencia ajustada en falla de progresión o rezago es sistemáticamente positiva y muy estable entre regímenes institucionales: **+5,97 puntos porcentuales** en **2006–2010** ([+4,32; +7,62]), **+5,75 puntos** en **2011–2015** ([+4,64; +6,85]) y **+5,29 puntos porcentuales** en **2016–2019** ([+2,08; +8,51], con cotas por datos faltantes de **−1,15 a 10,98 puntos**). De hecho, la ventana 2016–2019 tiene una estimación puntual **más conservadora** que los dos quinquenios anteriores, pero menor precisión muestral porque hubo menos cierres por año (62 episodios frente a 335 y 527). Segundo, en toda la serie **2005–2024** el agregado escalonado de Callaway y Sant'Anna ponderado por estudiantes expuestos alcanza **+9,11 puntos porcentuales** ([+5,34; +12,88]) y sus cotas de Manski para datos faltantes (**[+0,43; +16,21] puntos**) **no cruzan cero**, mientras que la ponderación por varianza inversa —que penaliza la alta dispersión de los años pandémicos y post-pandémicos (I² = 76,48 %)— converge a **+5,14 puntos** ([+4,34; +5,95]). Tercero, para la no matrícula persistente de dos años (19 cohortes evaluables entre 2005 y 2023, con 66.764 expuestos y 723.699 controles), el agregado ponderado por expuestos es **+1,09 puntos porcentuales** ([+0,65; +1,53]), en línea con el orden de magnitud histórico. Aun así, como demuestra la tabla 4 de caracterización NNA y una diferencia media previa en G−2 de −1,49 puntos ([−2,27; −0,71]) en la serie larga, estas diferencias agregadas describen una **brecha ajustada antes y después** en presencia de fragilidad y movilidad preexistentes, no un experimento aleatorio.
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
  <figcaption><strong>Figura 4</strong> — Cobertura y límites de la auditoría territorial. Seguimiento longitudinal y alertas de flujo no sustituyen evidencia sobre capacidad, acceso, demografía o decisiones institucionales. <span class="figure-source">Fuente: elaboración propia a partir de directorios MINEDUC y la auditoría longitudinal.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/territorial-audit-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

{: .table-caption}
**Tabla 7.** Información mínima para decidir y evaluar una transición

| Antes de decidir | Durante la transición | Después del cambio |
|---|---|---|
| Distinguir establecimiento, sede, nivel, fusión y cambio de Rol Base de Datos (RBD). | Asignar vacantes reales y apoyos a cada estudiante. | Seguir matrícula, asistencia, progresión, notas y bienestar. |
| Registrar fecha de anuncio y participación de la comunidad. | Medir tiempo de viaje, accesibilidad y continuidad de compañeros. | Observar también a estudiantes y equipos de las receptoras. |
| Verificar capacidad, dotación y calidad previa de los destinos. | Financiar la carga receptora y la continuidad pedagógica. | Publicar alertas, correcciones y responsabilidades con plazos. |
{: .table--compact .table--scroll}

El cuadro y la figura 4 —donde los 30 cierres de 2025 con seguimiento incompleto aparecen rotulados como censurados a la derecha porque aún no transcurre su año siguiente— cambian la carga de la prueba. Una autoridad no debería suponer que existe continuidad porque hay otra escuela cerca o porque varios estudiantes llegaron al mismo lugar. Debe demostrar que existen cupos, acceso seguro, recursos receptores y apoyos suficientes; luego, observar si la transición funcionó para estudiantes desplazados y para quienes ya estaban en la escuela receptora.
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

Callaway, Brantly, and Pedro H. C. Sant'Anna. 2021. [“Difference-in-Differences with Multiple Time Periods.”](https://doi.org/10.1016/j.jeconom.2020.12.001) *Journal of Econometrics* 225 (2): 200–230.

Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. [“Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?”](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203.

Grau, Nicolás, Daniel A. Hojman, Cristián Labra, and Alejandra Mizala. 2014. [“Destructive Creation: School Turnover and Educational Attainment.”]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}) Documento de Trabajo 396, Universidad de Chile.

Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. [“School Closure and Educational Attainment: Evidence from a Market-Based System.”](https://doi.org/10.1016/j.econedurev.2018.05.003) *Economics of Education Review* 65: 1–17.

Iocco, Maria Pia. 2024. [“Impact of Planned School Closures on Academic Performance: Evidence from Chile.”](https://doi.org/10.2139/ssrn.4808834) SSRN preprint.

Kim, Jeonghyeok. 2024. [“The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes.”](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963.

Larsen, Matthew F. 2020. [“Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment.”](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980.

Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://doi.org/10.1016/j.jeconom.2023.03.008) *Journal of Econometrics* 235 (2): 2218–44.

Steinberg, Matthew P., and John M. MacDonald. 2019. [“The Effects of Closing Urban Schools on Students’ Academic and Behavioral Outcomes: Evidence from Philadelphia.”](https://doi.org/10.1016/j.econedurev.2018.12.005) *Economics of Education Review* 69: 25–60.

Sun, Liyang, and Sarah Abraham. 2021. [“Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects.”](https://doi.org/10.1016/j.jeconom.2020.09.006) *Journal of Econometrics* 225 (2): 175–99.

Taghizadeh, Jonas Larsson. 2020. [“Are Students in Receiving Schools Hurt by the Closing of Low-Performing Schools? Effects of School Closures on Receiving Schools in Sweden 2000–2016.”](https://doi.org/10.1016/j.econedurev.2020.102020) *Economics of Education Review* 78: 102020.

</div>
