---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extender mi tesis en 3 cucharadas (parte III): qué muestran las trayectorias después del cierre de una escuela"
subtitle: "Seguir a los estudiantes permite observar la transición, pero todavía no separa con certeza el cierre de las trayectorias que ya venían cambiando."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-10-28 04:00:00 -0300
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

Cuando una escuela cierra, la pregunta pública no termina al encontrar otro colegio en el mapa. Importa saber si sus estudiantes siguieron matriculados, pasaron de curso y mantuvieron una asistencia regular. Y, sobre todo, importa distinguir qué parte de un tropiezo posterior se debe al cierre y qué parte venía gestándose desde antes.
{: .text-justify}

La comparación principal estima que el cambio entre antes y después en la **proporción observada sin matrícula o con avance inferior al curso esperado al año siguiente —indicador resumido como «falla de progresión o rezago»— fue 5,29 puntos porcentuales mayor entre los estudiantes expuestos que en el grupo de comparación**, con un intervalo de confianza conservador del 95 % de **2,08 a 8,51 puntos**. Sin embargo, como no todos los estudiantes tienen ese registro al año siguiente, al calcular cotas sin supuestos para los datos faltantes (Manski 2003) el rango posible va de **−1,15 a 10,98 puntos porcentuales**. Como ese intervalo cruza cero, el resultado de la ventana principal es **inconcluso**: no demuestra por sí solo daño, beneficio ni ausencia de efecto.
{: .text-justify}

Este ejercicio presenta una **reestimación posterior al piloto** sobre **79.709.054 registros de matrícula** y **73.873.835 de rendimiento** entre 2004 y 2025. La escala del panel permite reconstruir trayectorias individuales que los promedios por escuela ocultan, pero no fabrica el contrafactual —qué habría pasado con esos mismos niños, niñas y adolescentes (NNA) si su escuela hubiese seguido abierta— necesario para proclamar causalidad.
{: .text-justify}

<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->
<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->

La [parte I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) reconstruyó la evidencia histórica y separó qué hallazgos resistían. La [parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) verificó qué establecimientos cerraron en la década reciente y mostró que la escuela más cercana rara vez es el destino principal. Esta tercera entrega pasa de los edificios a las trayectorias estudiantiles en tres pasos: **qué cerró realmente**, **qué ocurrió después con los estudiantes** y **cómo proteger una transición escolar en la práctica**.
{: .text-justify}

## Cucharada 1: ¿qué cerró y quién quedó expuesto?

### Un flujo estudiantil es una señal, no un acto administrativo

En el período reciente (2016–2025) existen **346 episodios** donde una escuela con matrícula dejó de operar. Al descontar anexos, cambios administrativos y continuidades probables, la [parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) identificó **330 cierres estrictos** de oferta educativa. Seguir a sus estudiantes al año siguiente permite detectar cuándo casi todo el alumnado se traslada en bloque a un único colegio receptor: eso puede reflejar una fusión, un cambio de código o simplemente una alternativa vecina capaz de recibirlos, pero el flujo por sí solo no reemplaza un acto administrativo.
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

Cada uno de los 346 episodios entra en una sola fila de la tabla 1. Las **45 alertas por destino concentrado** son un corte transversal que se superpone con esas categorías y no se suma a ellas; existen **cero confirmaciones institucionales independientes** en esta etapa, por lo que los 330 cierres estrictos se mantienen como base de referencia.
{: .text-justify}

### De la certeza documental a la Regla de Cierre Escolar Inferido desde los Datos (RCID v1)

En un panel de veinte años sin expediente físico para cada colegio, necesitamos una regla explícita y falsable que separe una baja administrativa en el directorio de un cierre con dispersión real de estudiantes. Esa es la **Regla de Cierre Escolar Inferido desde los Datos (`RCID v1`)**, organizada en tres niveles anidados (D0 ⊃ D1 ⊃ D2):
{: .text-justify}

- **D0 (salida administrativa bruta):** matrícula positiva en t−1, caída a cero en t y sin actividad docente posterior.
- **D1 (cierre estricto de oferta):** depura de D0 las reaperturas, los cambios de código Rol Base de Datos (RBD) en el mismo local y las continuidades administrativas.
- **D2 = RCID v1 (cierre depurado por flujo estudiantil):** exige al menos 5 estudiantes seguibles en t−1 y aparta las absorciones concentradas donde un único colegio receptor recibe al menos el **70 %** de los trasladados y al menos **15 alumnos** en t.

{: .table-caption}
**Tabla 2.** Jerarquía de la Regla de Cierre Escolar Inferido desde los Datos (`RCID v1`, D0 ⊃ D1 ⊃ D2) en las tres entregas (2005–2025)

| Estrato de la regla | Ventana histórica (2005–2015) | Ventana reciente (2016–2025) | Serie longitudinal (2005–2025) | Qué depura y cómo se usa en las partes I, II y III |
|---|---:|---:|---:|---|
| D0: salida administrativa o de actividad bruta | 1.635 | 346 | 1.981 | Cese de matrícula en t; contrasta con las 2.069 salidas brutas de directorio de 1992–2012 en la parte I. |
| D1: cierre estricto de oferta educativa | 1.477 | 330 | 1.807 | Depura 158 reaperturas o continuidades históricas y 16 continuidades candidatas o anexos recientes (base de la parte II). |
| D2 = RCID v1 (conservador, incluye censurados de 2025) | 1.382 | 296 | 1.678 | Depura además 95 absorciones históricas y 34 absorciones o alertas de flujo concentradas recientes (≥ 70 % y ≥ 15 alumnos). |
| D2 = RCID v1 (limpio con ventana t+1 observada) | 1.382 | 266 | 1.648 | Exige además observar el año t+1 completo (excluye los 30 episodios de 2025 censurados a la derecha); base principal de la parte III. |
{: .table--compact .table--scroll}

En simple: no es lo mismo que un curso entero se mude junto a otro edificio a que cada familia deba buscar cupo por su cuenta. Aplicar `RCID v1` (D2) deja **1.648 cierres limpios** con ventana posterior observada en toda la serie 2005–2025 (**266** en la ventana reciente) y constituye el punto de partida para evaluar trayectorias sin mezclar fusiones de facto con cierres dispersos.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-1">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }} 1600w" alt="Dos carriles resumen el soporte de la reestimación post-piloto de 2016 a 2019. De 64 episodios históricos antes del soporte, 63 conservan al menos un estrato comparable y uno queda completamente fuera. De 6.581 observaciones estudiante-cohorte expuestas, 391 se excluyen y 6.190 permanecen. El universo de soporte contiene 82.753 observaciones estudiante-cohorte de control; las muestras finales cambian según el desenlace." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 1</strong> — Cómo se forma la muestra comparable de la reestimación post-piloto (2016–2019). Los conteos agregados preceden la elegibilidad específica de cada resultado y sus unidades no deben sumarse. <span class="figure-source">Fuente: elaboración propia a partir de la reestimación post-piloto.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/sample-flow-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

La figura 1 distingue entre episodios escolares y observaciones «estudiante-cohorte» (un alumno contado dentro de una cohorte de cierre). Además, la salida pública es estrictamente agregada: no expone nombres, direcciones ni identificadores individuales o de establecimientos.
{: .text-justify}

## Cucharada 2: ¿qué ocurrió después del cierre?

### Dos resultados primarios y una conclusión incómoda

Para medir qué pasó después del cierre en la ventana principal **2016–2019**, seguimos a los estudiantes de los **63 episodios con soporte comparable** de la figura 1 (de los cuales **62 episodios** tienen ventana observable para los dos resultados primarios y **58** para asistencia y notas). El primer resultado primario mira cuántos estudiantes quedan **sin matrícula durante dos años seguidos**: no lo llamamos «deserción» porque salir del registro administrativo chileno no aclara el motivo ni el destino. Allí el cambio del grupo expuesto supera en **+0,63 puntos porcentuales** al del grupo de comparación, con un intervalo conservador del 95 % de **−0,77 a 2,03 puntos** (sobre **3.666** observaciones expuestas y **49.944** controles).
{: .text-justify}

El segundo resultado primario mide la proporción **sin matrícula o bajo el curso esperado al año siguiente**, resumida como **falla de progresión o rezago**. Aquí la brecha antes-después sube en **+5,29 puntos porcentuales** entre los expuestos frente a sus controles (intervalo conservador de **2,08 a 8,51 puntos**, sobre **4.815** observaciones expuestas y **65.538** controles). El problema es qué ocurre con los registros donde la progresión no quedó observada: cuando aplicamos cotas de Manski para esos datos faltantes sin imponer supuestos optimistas, el rango va de **−1,15 a 10,98 puntos porcentuales**. Como incluye tanto una leve mejora como un rezago de casi once puntos, la estimación puntual no basta para adjudicar un efecto causal.
{: .text-justify}

{: .table-caption}
**Tabla 3.** Reestimación posterior al piloto (2016–2019): diferencias observadas, no efectos causales

| Resultado | Diferencia estimada | Intervalo conservador del 95 % | Condición decisiva |
|---|---:|---:|---|
| No matrícula persistente por dos años | +0,63 pp | [−0,77; 2,03] | No equivale a deserción; la tendencia previa estimable se apoya en pocos episodios. |
| Falla de progresión o rezago: sin matrícula o bajo el curso esperado al año siguiente | +5,29 pp | [2,08; 8,51] | Cotas por datos faltantes: [−1,15; 10,98] pp. |
| Asistencia | −1,15 puntos | [−2,40; 0,10] | Exploratoria y condicionada; exige asistencia válida y estado final promovido/reprobado observable. |
| Promedio de notas | −0,06 | [−0,14; 0,01] | Exploratorio y condicionado; solo entre quienes tienen rendimiento observable. |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-2">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }} 1600w" alt="Reestimación post-piloto inconclusa de dos resultados primarios. La no matrícula persistente se estima en 0,63 puntos porcentuales, con IC de menos 0,77 a 2,03; en la muestra distinta que incluye escuelas receptoras, 0,71, con IC de menos 0,69 a 2,12. La falla de progresión o rezago se estima en 5,29 puntos, con IC de 2,08 a 8,51; en la muestra distinta con receptoras, 5,09, con IC de 1,94 a 8,23. Sus límites por datos faltantes abarcan de menos 1,15 a 10,98 puntos. No son efectos causales confirmados." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 2</strong> — Reestimación post-piloto inconclusa, no efectos causales. El intervalo de progresión no cruza cero, pero sus cotas por datos faltantes sí; el solapamiento con el piloto y los supuestos no observados impiden atribuir causalidad. <span class="figure-source">Fuente: elaboración propia a partir de la reestimación post-piloto.</span> <span class="figure-data">Datos tabulares accesibles: <a href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-data.csv' | relative_url }}">estimaciones</a> y <a href="{{ '/assets/images/tesis-post3/missingness-bounds-data.csv' | relative_url }}">cotas por datos faltantes</a>.</span></figcaption>
</figure>

La asistencia y el promedio de notas en la tabla 3 son **exploratorias y condicionadas**: solo pueden medirse entre quienes tienen acta anual válida en ambos períodos (**3.871** observaciones expuestas en **58 episodios**, equivalentes al **62,5 %** del soporte expuesto frente al **76,8 %** de los controles, con **63.591** y **63.596** observaciones de comparación). En la figura 2, además, la barra alternativa que incluye a las escuelas receptoras en el grupo de control entrega **+0,71 puntos porcentuales** en no matrícula ([−0,69; 2,12], con 3.670 expuestos y 59.613 controles) y **+5,09 puntos** en falla de progresión ([1,94; 8,23], con 4.822 expuestos y 79.058 controles): cambiar qué escuelas entran al control modifica la muestra, pero no despeja las cotas de **−1,15 a 10,98 puntos** asociadas al +5,29 pp principal.
{: .text-justify}

Hay un límite estadístico adicional que conviene explicar como una **sala de reuniones**. Aunque la estimación principal reúne 62 escuelas cerradas, unas pocas concentran gran parte del alumnado. Escuchar esos 62 cierres se parece menos a oír 62 voces independientes del mismo volumen y más a oír unas **21,1 episodios efectivos** en no matrícula, **21,9** en progresión y apenas **17,7** en asistencia y notas. Del mismo modo, la exploración entre zonas urbanas y rurales descansa en aún menos episodios rurales, por lo que no permite hacer recomendaciones territoriales sin incorporar antes tiempos de viaje por red vial y transporte escolar.
{: .text-justify}

### ¿Estamos comparando peras con peras?

El diseño utiliza **diferencias en diferencias**: mide cuánto cambió el grupo expuesto antes y después del cierre y le resta el cambio de estudiantes de control emparejados exactamente un año antes del evento (G−1) por año, sexo, región, dependencia, ruralidad, nivel y curso. En simple: buscamos comparar peras con peras en todo lo que el registro permite ver.
{: .text-justify}

{: .table-caption}
**Tabla 4.** Similitud observada antes del cierre en la muestra ponderada (2016–2019)

| Característica previa | Estudiantes expuestos | Grupo de comparación | Lectura |
|---|---:|---:|---|
| Edad promedio | 11,70 años | 11,70 años | Diferencia estandarizada: 0,000. |
| Asistencia promedio | 90,93 % | 91,68 % | Diferencia estandarizada: −0,079. |
| Promedio de notas | 5,62 | 5,67 | Diferencia estandarizada: −0,072. |
| Registro válido de asistencia y notas | 76,8 % | 96,2 % | Brecha de cobertura: −19,4 pp. |
{: .table--compact .table--scroll}

La edad se observa en toda la muestra. La asistencia y las notas, en cambio, solo pueden compararse entre quienes tienen esos registros; allí la cobertura es 76,8 % entre los expuestos y 96,2 % en el grupo de comparación (una brecha de −19,4 puntos porcentuales). Por eso la tabla 4 no certifica aleatorización ni comparabilidad sociodemográfica completa: muestra equilibrio en el promedio observable, pero también una pérdida selectiva de actas entre quienes vivirán el cierre.
{: .text-justify}

¿Qué pasa si abrimos el foco hacia la vulnerabilidad social y la historia escolar previa entre G−3 y G−1? La tabla 5 resume ocho descriptores clave de los niños, niñas y adolescentes (NNA) y de sus escuelas de origen.
{: .text-justify}

{: .table-caption}
**Tabla 5.** Caracterización ampliada de niños, niñas y adolescentes (NNA) en G−1 (cohortes 2016–2019, 6.190 expuestos y 82.753 controles)

| Descriptor previo en G−1 | Estudiantes expuestos | Grupo de comparación | Brecha (pp) | Lectura sustantiva para la identificación |
|---|---:|---:|---:|---|
| Estudiante prioritario SEP (`PRIORITARIO_ALU`) | 30,68 % | 32,32 % | −1,64 | Equilibrio cercano en pobreza y vulnerabilidad prioritaria tras el pareo. |
| Elegibilidad SEP total (prioritario o preferente) | 54,51 % | 55,58 % | −1,07 | Composición socioeconómica individual equivalente en G−1. |
| Beneficiario efectivo SEP (`BEN_SEP`) | 37,63 % | 48,58 % | −10,95 | Pese a igual elegibilidad individual, los expuestos reciben menor cobertura SEP efectiva. |
| Escuela de origen con convenio SEP (`CONVENIO_SEP`) | 45,17 % | 55,23 % | −10,06 | Los cierres se concentran en sostenedores con menor adscripción a la SEP. |
| Escuela de origen con Jornada Escolar Completa (JEC) | 53,97 % | 72,51 % | −18,54 | Menor dotación de jornada completa en las escuelas que cerrarán. |
| Conmutación intercomunal (residencia ≠ comuna escolar) | 38,59 % | 29,99 % | +8,60 | Mayor proporción de NNA que ya viajaban fuera de su comuna antes del cierre. |
| Sobreedad ≥ 1 año respecto de la norma del curso | 33,86 % | 33,86 % | 0,00 | Equilibrio exacto por construcción del emparejamiento en G−1. |
| Al menos un cambio de escuela entre G−3 y G−1 | 47,04 % | 30,52 % | +16,52 | Casi la mitad de los expuestos ya venía rotando de colegio antes del cierre. |
{: .table--compact .table--scroll}

La radiografía de la tabla 5 explica por qué hay que ser cautelosos: los estudiantes expuestos y sus controles tienen la misma edad, el mismo rezago previo (33,86 %) y prácticamente la misma vulnerabilidad individual elegible para la Subvención Escolar Preferencial (54,51 % frente a 55,58 %, con **30,68 %** de alumnos prioritarios), pero asistían a colegios más precarios institucionalmente —con menos convenio SEP (−10,06 pp) y menos Jornada Escolar Completa (−18,54 pp)— y casi la mitad (**47,04 %** frente a 30,52 %) ya había cambiado de colegio en los dos años previos. Una parte del deterioro o la rotación antecedía al cierre.
{: .text-justify}

### ¿Por qué se eligió 2016–2019 y qué muestra la serie completa 2005–2024?

Concentrar el corte principal en **2016–2019** no fue una elección arbitraria: responde a que el estado oficial del directorio (`ESTADO_ESTAB`) se estandarizó desde 2015, a que observar tendencias previas largas dentro de un panel iniciado en 2004 empuja hacia esa década, a que **2020–2022** estuvo distorsionado por la pandemia de COVID-19 y la promoción flexible, y a que **2024–2025** está censurado a la derecha para medir dos años de no matrícula.
{: .text-justify}

Aun así, aplicando los estimadores modernos de diferencias en diferencias escalonadas para múltiples períodos (Callaway y Sant'Anna 2021; Sun y Abraham 2021; Roth et al. 2023) junto con cotas de sensibilidad (Manski 2003; Rambachan y Roth 2023), estimamos cada una de las **20 cohortes anuales entre 2005 y 2024** bajo la regla `RCID v1` (D2) frente a controles aún no tratados. La serie completa abarca **1.141 episodios con soporte empírico**, **78.972 observaciones expuestas** y **734.472 controles**; el detalle año a año está disponible en el [CSV abierto de la figura 3]({{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}), y la tabla 6 sintetiza los cinco regímenes institucionales, el rango anual y los tres agregados de la serie.
{: .text-justify}

{: .table-caption}
**Tabla 6.** Síntesis de la serie completa 2005–2024 por régimen institucional, rango anual y esquemas de agregación (`RCID v1`)

| Régimen institucional / Rango / Agregado | Episodios con soporte | Expuestos (N) | Controles (N) | Falla de progresión o rezago (pp) | IC 95 % progresión (pp) | No matrícula persistente 2 años (pp) | IC 95 % no matrícula (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Subagregado 2005–2010 (régimen LOCE e inicio SEP) | 521 | 36.984 | 334.062 | +12,15 | [+3,78; +20,52] | +1,21 | [+0,53; +1,90] |
| Subagregado 2011–2015 (puesta en marcha LGE y SAC) | 502 | 31.512 | 260.740 | +7,82 | [+6,20; +9,41] | +1,85 | [+1,10; +2,59] |
| Subagregado 2016–2019 (ventana principal; cotas [−1,15; 10,98] pp) | 63 | 6.190 | 82.753 | +5,29 | [+2,08; +8,51] | +0,63 | [−0,77; +2,03] |
| Subagregado 2020–2022 (pandemia COVID-19 y promoción flexible) | 33 | 3.272 | 42.457 | +2,70 | [−0,63; +6,03] | −0,28 | [−1,37; +0,81] |
| Subagregado 2023–2024 (reactivación post-pandemia; 2024 censurado en 2 años) | 22 | 1.014 | 14.460 | +2,59 | [−1,55; +6,73] | −0,93 | [−2,64; +0,78] |
| **Rango anual (19 cohortes en progresión; 17 en no matrícula)** | **7 a 129** | **357 a 10.261** | **5.566 a 71.248** | **+0,94 a +28,22 (mediana: +7,18)** | **[+3,15; +9,62] (RIQ)** | **−0,93 a +4,56 (mediana: +0,92)** | **[+0,22; +2,11] (RIQ)** |
| **Agregado serie 2005–2024 (Callaway y Sant'Anna, ponderado por expuestos)** | **1.141** | **78.972** | **734.472** | **+9,11** | **[+5,34; +12,88]** | **+1,38** | **[+0,92; +1,85]** |
| **Agregado serie 2005–2024 (pesos iguales por cohorte anual)** | **1.141** | **78.972** | **734.472** | **+7,55** | **[+5,52; +9,57]** | **+1,03** | **[+0,56; +1,50]** |
| **Agregado serie 2005–2024 (precisión por varianza inversa; I² = 76,48 %)** | **1.141** | **78.972** | **734.472** | **+5,14** | **[+4,34; +5,95]** | **+0,54** | **[+0,29; +0,79]** |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-4">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }} 1600w" alt="Infografía en tres paneles bajo la regla RCID v1 con 1.141 episodios con soporte entre 2005 y 2024. El panel A muestra las 19 cohortes anuales estimables de falla de progresión o rezago entre 2006 y 2024: las 19 son positivas, con rango de 0,94 a 28,22 puntos porcentuales, mediana de 7,18 y agregado ponderado de Callaway y Sant'Anna de +9,11 puntos (intervalo de 5,34 a 12,88 y cotas de Manski de +0,43 a +16,21 puntos). El panel B resume la atenuación por régimen institucional desde 12,15 puntos en 2005–2010 y 7,82 en 2011–2015 hasta 5,29 en 2016–2019 (con cotas por datos faltantes de menos 1,15 a 10,98 puntos), 2,70 en 2020–2022 y 2,59 en 2023–2024. El panel C muestra las brechas basales en G menos 1 tras el pareo exacto: la elegibilidad SEP es similar (−1,07 puntos), pero los expuestos asisten a escuelas con menos convenio SEP (−10,06 puntos), menos JEC (−18,54 puntos), menor cobertura de acta (−19,24 puntos) y mayor rotación previa (+16,52 puntos)." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 3</strong> — Auditoría de la serie completa 2005–2024 bajo <code>RCID v1</code>: estimaciones anuales (2006–2024), atenuación por régimen institucional y brechas de caracterización de NNA en G−1. <span class="figure-source">Fuente: elaboración propia a partir del panel 2004–2025 y el artefacto auditado de serie completa v1.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

La serie larga de la tabla 6 y la figura 3 deja tres lecciones claras:
{: .text-justify}

- **La ventana 2016–2019 no fue elegida para inflar el resultado:** de hecho, muestra una atenuación progresiva de la brecha de progresión a medida que se desplegaron la SEP, el Sistema de Aseguramiento de la Calidad (SAC) y la Ley de Inclusión, bajando desde **+12,15 puntos porcentuales** en 2005–2010 y **+7,82 puntos** en 2011–2015 hasta **+5,29 puntos porcentuales** en 2016–2019 (con sus cotas de **−1,15 a 10,98 puntos**), **+2,70 puntos** en 2020–2022 y **+2,59 puntos** en 2023–2024.
- **En la serie completa las 19 cohortes estimables de progresión son positivas:** el agregado ponderado de Callaway y Sant'Anna alcanza **+9,11 puntos porcentuales** ([+5,34; +12,88]) y sus cotas de Manski (**+0,43 a +16,21 puntos**) no cruzan cero, mientras que el ponderador por varianza inversa —que descuenta la dispersión entre períodos (I² = 76,48 %)— converge a **+5,14 puntos** ([+4,34; +5,95]).
- **Mayor volumen no reemplaza un experimento aleatorio:** como muestran la alta rotación previa en G−1 (47,04 %) y una pequeña desviación pre-tendencia media en G−2 de −1,49 puntos en la serie larga, cualquier lectura causal estricta requiere evaluar cuánto cambiaría la conclusión ante desvíos moderados de tendencias paralelas (Rambachan y Roth 2023).

¿Podríamos resolver esa endogeneidad usando una variable instrumental, como la entrada en operación de los Servicios Locales de Educación Pública (SLEP), el Sistema de Admisión Escolar (SAE) o los shocks demográficos comunales? No en este diseño: esas reformas y caídas de matrícula afectan directamente los recursos, las vacantes disponibles y las decisiones de cambio de colegio de las familias, incumpliendo la restricción de exclusión (que el instrumento actúe únicamente a través del cierre). Sin un sorteo o umbral administrativo externo que supere relevancia y exclusión, forzar un modelo instrumental solo crearía falsa precisión. Por eso no se ejecuta una regresión instrumental en esta versión.
{: .text-justify}

### Qué agrega —y qué no agrega— la literatura

La evidencia internacional coincide en que el impacto de cerrar una escuela depende crítica y conjuntamente del proceso de transición y de la calidad del establecimiento receptor: suele haber pérdidas durante el anuncio y el primer año, seguidas de recuperación parcial cuando los estudiantes acceden a escuelas de mayor valor agregado, pero con costos duraderos en asistencia o graduación secundaria cuando la reubicación ocurre hacia planteles congestionados o de desempeño similar (Engberg et al. 2012; Brummet 2014; Beuchert et al. 2018; Steinberg y MacDonald 2019; Larsen 2020; Taghizadeh 2020; Bross, Harris y Liu 2023; Kim 2024; Abdulkadiroğlu, Pathak y Walters 2026). En Chile, Grau, Hojman y Mizala (2018) estimaron aumentos en repitencia y deserción en un período anterior, mientras que Iocco (2024), en un preprint sobre cierres planificados, reporta efectos promedio nulos en puntajes con heterogeneidad según la escuela de destino. Por diferencias de período, definición de tratamiento y variable dependiente, la estimación de 5,29 puntos —con cotas de −1,15 a 10,98 puntos— complementa pero no replica ni refuta mecánicamente esos trabajos.
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

Que el efecto causal exacto sea inconcluso en la ventana reciente no justifica quedarse de brazos cruzados cuando una escuela cierra. Al contrario: el diagnóstico longitudinal muestra exactamente dónde se pierde el rastro de los estudiantes y qué garantías operativas deben exigirse antes, durante y después de reorganizar una red escolar.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-3">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }} 1600w" alt="De 346 episodios, 339 tienen tres años preevento completos y 323 tienen cinco. La clasificación contiene 266 sin señal contradictoria, 15 candidatos de continuidad, 35 alertas no resueltas y 30 censurados. Hay 45 alertas posevento y cero confirmaciones institucionales; el procesamiento automático solo permite observación." loading="lazy" decoding="async">
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

La figura 4 y la tabla 7 invierten la carga de la prueba: la autoridad no puede dar por garantizada la continuidad educativa solo porque existe otro establecimiento a pocos kilómetros o porque un grupo de alumnos reapareció matriculado. Debe acreditar de antemano vacantes efectivas, transporte seguro, convenio SEP activo y soporte pedagógico en las escuelas receptoras, y monitorear nominalmente qué pasa con cada estudiante durante al menos dos años.
{: .text-justify}

## Cierre: seguir trayectorias cambia la pregunta pública

La parte I reconstruyó los cimientos históricos; la parte II depuró qué escuelas cerraron y qué oferta existía alrededor; esta tercera parte siguió las trayectorias estudiantiles y demostró por qué el mapa no bastaba. El resultado principal de la ventana reciente —un aumento de **5,29 puntos porcentuales** en falla de progresión o rezago— debe leerse siempre junto a sus cotas por datos faltantes de **−1,15 a 10,98 puntos**, y la brecha acumulada de la serie larga (+9,11 puntos en Callaway y Sant'Anna; +5,14 puntos por varianza inversa) debe leerse junto a la mayor movilidad y precariedad institucional previa de las escuelas que cierran.
{: .text-justify}

Un resultado inconcluso sí permite fijar resguardos prudenciales hoy: no tratar la cercanía como continuidad, no reorganizar una red sin verificar cupos y apoyos, y seguir a cada estudiante durante la transición. Estos resguardos no son efectos estimados de esas decisiones. Son el estándar mínimo de cuidado público mientras se construyen mejores datos sobre fechas de anuncio, capacidad receptora y seguimiento completo de actas.
{: .text-justify}

### Transparencia y alcance de las fuentes

La tesis original y esta serie de extensión son de mi autoría, al igual que la coautoría del documento de trabajo de 2014; por ello no constituyen una réplica externa independiente y mantienen separadas la reconstrucción histórica y la reestimación actual. No recibí financiamiento externo y declaro no tener conflictos de interés. Mi única afiliación institucional es el Ministerio de Desarrollo Social y Familia de Chile, que no financió, encargó ni revisó este análisis; las opiniones y conclusiones son de mi exclusiva responsabilidad. Utilicé asistentes de inteligencia artificial para apoyar programación reproducible, búsqueda bibliográfica, validación estadística y edición; toda decisión metodológica y verificación factual es propia.
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

Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). New York: Springer.

Rambachan, Ashesh, and Jonathan Roth. 2023. [“A More Credible Approach to Parallel Trends.”](https://doi.org/10.1093/restud/rdad018) *The Review of Economic Studies* 90 (5): 2555–91.

Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://doi.org/10.1016/j.jeconom.2023.03.008) *Journal of Econometrics* 235 (2): 2218–44.

Steinberg, Matthew P., and John M. MacDonald. 2019. [“The Effects of Closing Urban Schools on Students’ Academic and Behavioral Outcomes: Evidence from Philadelphia.”](https://doi.org/10.1016/j.econedurev.2018.12.005) *Economics of Education Review* 69: 25–60.

Sun, Liyang, and Sarah Abraham. 2021. [“Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects.”](https://doi.org/10.1016/j.jeconom.2020.09.006) *Journal of Econometrics* 225 (2): 175–99.

Taghizadeh, Jonas Larsson. 2020. [“Are Students in Receiving Schools Hurt by the Closing of Low-Performing Schools? Effects of School Closures on Receiving Schools in Sweden 2000–2016.”](https://doi.org/10.1016/j.econedurev.2020.102020) *Economics of Education Review* 78: 102020.

</div>
