---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Anexo metodológico de la parte III: cierres y trayectorias escolares"
description: "Definiciones, tablas, sensibilidades y fuentes de la parte III de la serie de extensión de tesis."
permalink: /datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/
ref: tesis-post3-anexo-metodologico
lang: es
author: clabra
author_profile: true
math: true
toc: true
toc_sticky: true
table_contract: explicit-v1
last_modified_at: 2026-11-07 21:00:00 -0300
---

{% include thesis-series-nav.html current=3 %}

Este anexo conserva definiciones, universos, tablas, figuras complementarias y pruebas de sensibilidad que sostienen el [relato principal]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/' | relative_url }}). La numeración A corresponde solo a este anexo; los identificadores de las figuras se mantienen para conservar enlaces existentes. Las brechas escolares no equivalen automáticamente a efectos causales del cierre.
## Clasificación y población observada

### Veinte años de cierres bajo tres coladores sucesivos (RCID v1, 2005–2025)

En Chile, el cierre jurídico de un colegio exige una resolución exenta de la SEREMI de Educación, pero no existe un registro público y completo de esas resoluciones: lo comprobé en Transparencia Activa (detalle en las notas metodológicas al final). Por eso construí una regla empírica y falsable, la **Regla de Cierre Escolar Inferido desde los Datos (RCID v1)**, que funciona como tres coladores sucesivos (**D0 ⊃ D1 ⊃ D2**) sobre veinte años de datos administrativos. El primero (**D0**) detecta la matrícula que desaparece; el segundo (**D1**) descarta anexos y cambios de código; el tercero (**D2**) aparta los traslados en bloque a un solo colegio. La distinción importa: no es lo mismo que un curso entero se mude junto a otro edificio a que cada familia deba buscar cupo por su cuenta.

{: .table-caption}
<span id="tabla-post3-a1"></span>
**Tabla A1.** Jerarquía de la Regla de Cierre Escolar Inferido desde los Datos (RCID v1, D0 ⊃ D1 ⊃ D2) en las tres entregas (2005–2025)

| Estrato de la regla | Ventana histórica (2005–2015) | Ventana reciente (2016–2025) | Serie longitudinal (2005–2025) | Qué depura y cómo se usa en las partes I, II y III |
|---|---:|---:|---:|---|
| D0: salida administrativa o de actividad bruta | 1.635 | 346 | 1.981 | Cese de matrícula en t; contrasta con las 2.069 salidas brutas de directorio de 1992–2012 en la parte I. |
| D1: cierre estricto de oferta educativa | 1.477 | 330 | 1.807 | Depura 158 anexos, sedes o sucesores de RBD históricos y 16 continuidades de directorio recientes (base de la parte II). |
| D2 = RCID v1 (conservador, incluye censurados de 2025) | 1.382 | 296 | 1.678 | Depura además 95 absorciones históricas y 34 absorciones o alertas de flujo concentradas recientes (≥ 10 estudiantes de base y asignados, ≥ 70 % al destino principal y HHI ≥ 0,50). |
| D2 = RCID v1 (limpio con ventana t+1 observada) | 1.382 | 266 | 1.648 | Exige además observar el año t+1 completo (excluye los 30 episodios de 2025 censurados a la derecha); base principal de la parte III. |
{: .table--compact .table--scroll}

Como muestra la tabla A1, aplicar RCID v1 (D2) deja **1.648 cierres limpios** con ventana posterior observada en toda la serie 2005–2025 —**1.382** en la ventana histórica 2005–2015 y **266** en la ventana reciente 2016–2024— y constituye el punto de partida para evaluar trayectorias sin mezclar fusiones de hecho con cierres dispersos. No todos esos cierres pueden seguirse con trayectorias de curso: solo **1.177** tenían estudiantes de educación regular (básica de 1.º a 8.º o media de 1.º a 3.º) y **1.141** encontraron controles comparables (**78.972 estudiantes expuestos** y **734.472 controles**). En la ventana reciente, **145 de los 266** cierres eran escuelas solo de párvulos (69), solo de educación especial (57), solo de adultos (13) o solo de cuarto medio (1), o tenían predominio de esas ofertas (5). Allí no se puede medir la progresión de curso, así que los resultados de esta entrega hablan de escuelas regulares, no de todo cierre.

### Un flujo estudiantil es una señal, no un acto administrativo: el corte 2016–2025

En el período reciente (2016–2025) existen **346 episodios** donde una escuela con matrícula dejó de operar. Al descontar anexos, cambios administrativos y continuidades probables, la [parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) identificó **330 cierres estrictos** (D1) de oferta educativa. Seguir a sus estudiantes al año siguiente permite detectar cuándo casi todo el alumnado se traslada en bloque a un único colegio receptor: eso puede reflejar una fusión, un cambio de código o simplemente una alternativa vecina capaz de recibirlos, pero el flujo por sí solo no reemplaza un acto administrativo.

{: .table-caption}
<span id="tabla-post3-a2"></span>
**Tabla A2.** Lectura diagnóstica de los 346 episodios registrados como cierres en el período reciente (2016–2025)

| Estado | Episodios | Lectura permitida |
|---|---:|---|
| Sin señal contradictoria | 266 | La trayectoria no contradice el cierre estricto; no constituye corroboración externa. |
| Continuidad candidata | 15 | Nombre, nivel o modalidad, o actividad posterior justifican una revisión documental. |
| Alerta no resuelta | 35 | La categoría no cambia mientras falte evidencia independiente. |
| Seguimiento incompleto | 30 | Son cierres de 2025 y todavía no se observa el año siguiente. |
{: .table--compact .table--scroll}

Cada uno de los 346 episodios entra en una sola fila de la tabla A2. Las **45 alertas por destino concentrado** son un corte transversal que se superpone con esas categorías y no se suma a ellas; sin contar aún con **confirmaciones institucionales independientes** (**cero** en este corte), los 330 cierres estrictos se mantienen como base de referencia de la parte II, mientras esta entrega trabaja sobre los cierres D2 de la tabla A1.

<figure class="post3-figure data-visualization" id="fig-post3-1">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }} 1600w" alt="Dos carriles resumen el soporte de la reestimación post-piloto de 2016 a 2019. De 64 episodios históricos antes del soporte, 63 conservan al menos un estrato comparable y uno queda completamente fuera. De 6.581 observaciones estudiante-cohorte expuestas, 391 se excluyen y 6.190 permanecen. El universo de soporte contiene 82.753 observaciones estudiante-cohorte de control; las muestras finales cambian según el desenlace." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura A1</strong> — Cómo se forma la muestra comparable en el zoom pre-registrado (2016–2019). Los conteos agregados preceden la elegibilidad específica de cada resultado y sus unidades no deben sumarse. <span class="figure-source">Fuente: elaboración propia a partir de la reestimación post-piloto.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/sample-flow-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

La figura A1 distingue entre escuelas cerradas (episodios) y observaciones "estudiante-cohorte" (cada alumno contado dentro de su cohorte de cierre). Además, la información publicada es estrictamente agregada: por resguardo de privacidad, no expone nombres, direcciones ni códigos individuales de estudiantes o establecimientos.

### Quiénes eran los estudiantes expuestos

Antes de mirar qué les pasó, conviene saber quiénes eran. La tabla A3 resume ocho características de los niños, niñas y adolescentes (NNA) y de sus escuelas de origen, medidas un año antes del cierre (G−1); solo la última fila mira más atrás, desde G−3, para capturar la rotación previa.

{: .table-caption}
<span id="tabla-post3-a3"></span>
**Tabla A3.** Caracterización ampliada de niños, niñas y adolescentes (NNA) en G−1 (cohortes 2016–2019, 6.190 expuestos y 82.753 controles)

| Descriptor previo en G−1 | Estudiantes expuestos | Grupo de comparación | Brecha (pp) | Lectura sustantiva para la identificación |
|---|---:|---:|---:|---|
| Estudiante prioritario SEP | 30,68 % | 32,32 % | −1,64 | Equilibrio cercano en pobreza y vulnerabilidad prioritaria tras el pareo. |
| Elegibilidad SEP total (prioritario o preferente) | 54,51 % | 55,58 % | −1,07 | Composición similar en esta medida binaria de vulnerabilidad. |
| Beneficiario efectivo SEP | 37,63 % | 48,58 % | −10,95 | Es coherente con el menor convenio SEP de la escuela (fila siguiente). |
| Escuela de origen con convenio SEP | 45,17 % | 55,23 % | −10,06 | Los cierres se concentran en sostenedores con menor adscripción a la SEP. |
| Escuela de origen con Jornada Escolar Completa (JEC) | 53,97 % | 72,51 % | −18,54 | Menor dotación de jornada completa en las escuelas que cerrarán. |
| Conmutación intercomunal (residencia ≠ comuna escolar) | 38,59 % | 29,99 % | +8,60 | Mayor proporción de NNA que ya viajaban fuera de su comuna antes del cierre. |
| Sobreedad ≥ 1 año respecto de la norma del curso | 33,86 % | 33,86 % | 0,00 | Equilibrio exacto por construcción del emparejamiento en G−1. |
| Al menos un cambio de escuela entre G−3 y G−1 | 47,04 % | 30,52 % | +16,52 | Casi la mitad de los expuestos ya venía rotando de colegio antes del cierre. |
{: .table--compact .table--scroll}

La radiografía de la tabla A3 explica por qué hay que ser cautelosos tanto en la serie larga como en el corte reciente: los estudiantes expuestos y sus controles tienen la misma edad, el mismo rezago previo (33,86 %) y prácticamente la misma vulnerabilidad individual elegible para la Subvención Escolar Preferencial (54,51 % frente a 55,58 %, con **30,68 %** de alumnos prioritarios), pero asistían a colegios institucionalmente más frágiles —con menos convenio SEP (−10,06 pp) y menos Jornada Escolar Completa (−18,54 pp)— y casi la mitad (**47,04 %** frente a 30,52 %) ya había cambiado de colegio en los dos años previos. Una parte del desgaste escolar y de la rotación familiar ya estaba en marcha antes del cierre. Además, solo cuento como expuestos a quienes seguían matriculados en G−1: si las familias con más recursos se fueron antes del cierre, el grupo expuesto ya llega seleccionado.
## Serie, sensibilidad y receptoras

{: .table-caption}
<span id="tabla-post3-a4"></span>
**Tabla A4.** Síntesis de la serie completa 2005–2024 por régimen institucional, rango anual y esquemas de agregación (RCID v1)

| Régimen institucional / Rango / Agregado | Episodios con soporte | Expuestos (N) | Controles (N) | Falla de progresión o rezago (pp) | IC 95 % progresión (pp) | Cotas Manski progresión (pp) | No matrícula persistente 2 años (pp) | IC 95 % no matrícula (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Subagregado 2005–2010 (régimen LOCE e inicio SEP) | 521 | 36.984 | 334.062 | +12,15 | [+3,78; +20,52] | [+3,49; +18,83] | +1,21 | [+0,53; +1,90] |
| Subagregado 2011–2015 (puesta en marcha LGE y SAC) | 502 | 31.512 | 260.740 | +7,82 | [+6,20; +9,41] | [−2,11; +16,18] | +1,85 | [+1,10; +2,59] |
| Subagregado 2016–2019 (ventana principal; cotas [−1,15; 10,98] pp) | 63 | 6.190 | 82.753 | +5,29 | [+2,08; +8,51] | [−1,15; +10,98] | +0,63 | [−0,77; +2,03] |
| Subagregado 2020–2022 (pandemia COVID-19 y promoción flexible) | 33 | 3.272 | 42.457 | +2,70 | [−0,63; +6,03] | [+0,18; +4,95] | −0,28 | [−1,37; +0,81] |
| Subagregado 2023–2024 (reactivación post-pandemia; 2024 censurado en 2 años) | 22 | 1.014 | 14.460 | +2,59 | [−1,55; +6,73] | [−1,70; +6,07] | −0,93 | [−2,64; +0,78] |
| **Rango anual (19 cohortes en progresión; 17 en no matrícula)** | **7 a 129** | **357 a 10.261** | **5.566 a 71.248** | **+0,94 a +28,22 (mediana: +7,18)** | **RIQ: +3,15 a +9,62** | **—** | **−0,93 a +4,56 (mediana: +0,92)** | **RIQ: +0,22 a +2,11** |
| **Agregado serie 2005–2024 (Callaway y Sant'Anna, ponderado por expuestos)** | **1.141** | **78.972** | **734.472** | **+9,11** | **[+5,34; +12,88]** | **[+0,43; +16,21]** | **+1,38** | **[+0,92; +1,85]** |
| **Agregado serie 2005–2024 (pesos iguales por cohorte anual)** | **1.141** | **78.972** | **734.472** | **+7,55** | **[+5,52; +9,57]** | **—** | **+1,03** | **[+0,56; +1,50]** |
| **Agregado serie 2005–2024 (efectos aleatorios; I² = 76,5 %, τ = 2,81 pp)** | **1.141** | **78.972** | **734.472** | **+6,29** | **[+4,49; +8,09]; predicción [+0,09; +12,49]** | **—** | **+0,79** | **[+0,16; +1,42]; predicción [−1,34; +2,92]** |
{: .table--compact .table--scroll}

Los N de la tabla A4 corresponden al soporte; cada estimación usa el subconjunto con desenlace observable (por ejemplo, 4.815 expuestos en progresión 2016–2019). Las cotas de Manski no incluyen error muestral. El agregado de efectos aleatorios (Paule-Mandel, con intervalo de Hartung-Knapp) reemplaza al de varianza inversa de la versión anterior; aquel suponía un efecto común a todas las cohortes, lo que con una heterogeneidad de 76,5 % produce un intervalo artificialmente estrecho. Como las cohortes comparten controles, incluso estos intervalos pueden quedar algo cortos.
### El zoom pre-registrado 2016–2019: evidencia parcial y dos resultados primarios

Visto ese panorama de veinte años, la ventana **2016–2019** cobra su sentido exacto: fue el corte que fijé antes de estimar la serie larga porque desde 2015 se estandarizó el directorio oficial, permitía observar varios años previos sin chocar con el inicio del panel en 2004 y evitaba la distorsión de la pandemia de 2020–2022. Pero como solo reúne **63 de los 1.141 episodios con soporte** (el 5,5 % de la serie, de los cuales **62 episodios** tienen ventana observable para los dos resultados primarios y **58** para asistencia y notas), sus resultados deben leerse como **evidencia parcial**.

En este zoom 2016–2019, el primer resultado primario mira cuántos estudiantes quedan **sin matrícula durante dos años seguidos**: no lo llamo "deserción" porque salir del registro administrativo chileno no aclara si el alumno abandonó los estudios, salió del país o pasó a una modalidad no cubierta. Allí el cambio del grupo expuesto supera en **+0,63 puntos porcentuales** al del grupo de comparación, con un intervalo conservador del 95 % de **−0,77 a 2,03 puntos** (sobre **3.666** observaciones expuestas y **49.944** controles).

El segundo resultado primario mide la proporción **sin matrícula o bajo el curso esperado al año siguiente**, resumida como **falla de progresión o rezago**. En 2016–2019 la brecha antes-después sube en **+5,29 puntos porcentuales** entre los expuestos frente a sus controles (intervalo conservador de **2,08 a 8,51 puntos**, sobre **4.815** observaciones expuestas y **65.538** controles). Pero el dato falta para el **3,60 %** de los expuestos y el **2,15 %** de los controles, y las **cotas de Manski** (Manski 2003[^manski2003]) van de **−1,15 a 10,98 puntos porcentuales** —una prueba de esfuerzo sin optimismo que asigna a los alumnos sin dato el peor desenlace en un grupo y el mejor en el otro, y luego al revés—. Por eso el resultado de este subperíodo es **inconcluso** por sí solo: entre los expuestos la falla pasa de **2,2 %** dos años antes del cierre a **15,8 %** el año siguiente frente al **10,6 %** esperable según sus controles (un **50 %** más que ese contrafactual y, solo si fuese causal, unos **255 estudiantes**), sin que el indicador separe salida del registro y repitencia. Las cotas solo excluyen el cero dentro de este subperíodo en los cierres con al menos 90 % de actas válidas el año previo (un 38 % de los expuestos).

{: .table-caption}
<span id="tabla-post3-a5"></span>
**Tabla A5.** Reestimación posterior al piloto en el zoom pre-registrado (2016–2019): diferencias observadas, no efectos causales

| Resultado | Diferencia estimada | Intervalo conservador del 95 % | Condición decisiva |
|---|---:|---:|---|
| No matrícula persistente por dos años | +0,63 pp | [−0,77; 2,03] | No equivale a deserción; la tendencia previa estimable se apoya en pocos episodios. |
| Falla de progresión o rezago: sin matrícula o bajo el curso esperado al año siguiente | +5,29 pp | [2,08; 8,51] | Cotas por datos faltantes: [−1,15; 10,98] pp en el total; [0,09; 7,84] pp en cierres con ≥ 90 % de actas válidas en G−1 (38 % de los expuestos). Sin error muestral. |
| Asistencia | −1,15 puntos | [−2,40; 0,10] | Exploratoria y condicionada; exige asistencia válida y estado final promovido/reprobado observable. |
| Promedio de notas | −0,06 | [−0,14; 0,01] | Exploratorio y condicionado; solo entre quienes tienen rendimiento observable. |
{: .table--compact .table--scroll}

La asistencia y el promedio de notas en la tabla A5 son **exploratorias y condicionadas**: solo pueden medirse entre quienes tienen acta anual válida en ambos períodos. Eso deja **3.871** observaciones expuestas en **58 episodios**, el **62,5 %** del soporte expuesto, frente a **63.591** de los **82.753** controles en asistencia (63.596 en notas). En la figura 2 del artículo principal, además, la barra alternativa que incluye a las escuelas receptoras en el grupo de control entrega **+0,71 puntos porcentuales** en no matrícula ([−0,69; 2,12], con 3.670 expuestos y 59.613 controles) y **+5,09 puntos** en falla de progresión ([1,94; 8,23], con 4.822 expuestos y 79.058 controles): cambiar qué escuelas entran al control modifica la muestra, pero no despeja las cotas de **−1,15 a 10,98 puntos** asociadas al +5,29 pp principal.

El tamaño efectivo de este subperíodo se entiende mejor como una **sala de reuniones**. Aunque la estimación 2016–2019 reúne 62 escuelas cerradas, unas pocas concentran gran parte del alumnado. Escuchar esos 62 cierres se parece menos a oír 62 voces independientes del mismo volumen y más a oír unos **21,1 episodios efectivos** en no matrícula, **21,9** en progresión y apenas **17,7** en asistencia y notas. Del mismo modo, la exploración entre zonas urbanas y rurales descansa en aún menos episodios rurales, por lo que no permite hacer recomendaciones territoriales sin incorporar antes tiempos de viaje por red vial y transporte escolar.

<span id="tendencias-y-datos-faltantes"></span>
### ¿Se comparan peras con peras? Tendencias previas y cobertura de actas

Tanto en la serie larga como en el zoom 2016–2019, el diseño utiliza **diferencias en diferencias**, que compara dos películas en lugar de dos fotografías sueltas: primero empareja a cada alumno de una escuela que cerrará con estudiantes de control idénticos un año antes del cierre (G−1) en año calendario, sexo, edad, región, dependencia del sostenedor, ruralidad, nivel de enseñanza y curso, y luego mide cuánto cambió la trayectoria del primer grupo antes y después del evento frente al cambio de sus pares. Comparo las variables observables del registro, midiendo su cercanía mediante la **diferencia estandarizada** (distancia en unidades de dispersión donde cero equivale a igualdad).

En lo observable, los grupos quedan casi idénticos en edad, asistencia y notas, con diferencias estandarizadas menores a 0,08. Pero los expuestos tienen muchas menos actas anuales válidas el año previo al cierre: 76,8 % frente a 96,2 %. A la vez, tres pruebas placebo anteriores al cierre en 2016–2019 dan diferencias de +0,16, +0,30 y +0,40 puntos en progresión: el intervalo de la estimación de +5,29 pp (con cotas de −1,15 a 10,98 puntos) deja de excluir el cero si un sesgo posterior al cierre alcanza 2,07 puntos, unas 2,54 veces la cota superior al 95 % del mayor placebo (0,81 puntos), sin combinar ese cálculo con las cotas por datos faltantes. Antes de restringir por soporte y desenlace, el 70,58 % de las 6.581 observaciones expuestas corresponde a alumnos estables en la misma escuela entre G−2 y G−1. Para la estimación de progresión, la submuestra con soporte contiene 3.556 estables y 1.033 entrantes tardíos; sus brechas son **+3,87 puntos porcentuales** ([+1,04; +6,69]) y **+9,58 puntos** ([+5,06; +14,10]), respectivamente. Cerca de tres cuartas partes de la brecha puntual de la muestra completa se mantiene entre quienes llevaban al menos dos años en la escuela; no es una proporción causal atribuible a la permanencia.

<aside class="notice--info" markdown="1">
**Nota metodológica — Qué cambia según la cobertura de actas y cuánto sesgo anularía el intervalo:** Las cotas de peor caso de Manski (2003[^manski2003]) no suponen nada sobre los alumnos sin dato, así que su amplitud depende de cuántos faltan. El artículo 27 del Decreto Supremo n.º 315 exige al sostenedor entregar las actas de promoción antes de que la SEREMI resuelva el cierre; no observo esa entrega, sino la proporción de estudiantes con acta válida en el panel. En los cierres de 2016–2019 donde esa proporción llega al 90 % (1.822 expuestos con desenlace), los faltantes casi se igualan entre grupos (2,31 % frente a 2,15 %), la diferencia es de +4,26 puntos y las cotas van de +0,09 a +7,84 puntos; excluir solo los cierres con menos de la mitad de actas deja las cotas entre −0,90 y +12,18 puntos. Por su parte, el umbral de 2,07 puntos de sesgo posterior al cierre (2,54 veces la cota superior de 0,81 puntos del mayor placebo) aplica una versión lineal y simplificada de la idea de Rambachan y Roth (2023[^rambachan2023]), no su estimador formal, y ninguna de estas dos pruebas incorpora simultáneamente el error muestral de las cotas.
</aside>

### Qué agrega —y qué no agrega— la literatura

La evidencia internacional sugiere que los resultados posteriores a un cierre pueden depender conjuntamente del proceso de transición y de la calidad del establecimiento receptor: suele haber pérdidas durante el anuncio y el primer año, seguidas de recuperación parcial cuando los estudiantes acceden a escuelas de mayor valor agregado, pero con costos duraderos en asistencia o graduación secundaria cuando la reubicación ocurre hacia planteles congestionados o de desempeño similar (Engberg et al. 2012[^engberg2012]; Brummet 2014[^brummet2014]; Beuchert et al. 2018[^beuchert2018]; Steinberg y MacDonald 2019[^steinberg2019]; Larsen 2020[^larsen2020]; Taghizadeh 2020[^taghizadeh2020]; Bross, Harris y Liu 2023[^bross2023]; Kim 2024[^kim2024]), en línea con la literatura sobre asignación escolar y calidad del establecimiento de destino (Abdulkadiroğlu, Pathak y Walters 2026[^abdulkadiroglu2026]). En Chile, Grau, Hojman y Mizala (2018[^grau2018]) estimaron aumentos en repitencia y deserción en un período anterior, mientras que Iocco (2024[^iocco2024]), en un preprint sobre cierres planificados, reporta efectos promedio nulos en puntajes con heterogeneidad según la escuela de destino. Por diferencias de período, definición de tratamiento y variable dependiente, tanto la serie completa 2005–2024 (+9,11 puntos en Callaway y Sant'Anna; +6,29 en efectos aleatorios) como la estimación 2016–2019 de 5,29 puntos porcentuales —con cotas de −1,15 a 10,98 puntos— complementan pero no replican ni refutan mecánicamente esos trabajos.

<span id="calidad-de-la-receptora"></span>
### ¿Importa a qué escuela llegan?

En mi panel 2016–2019 exploré una pieza de ese mecanismo. Entre los 4.362 estudiantes expuestos que se matricularon en otra escuela el año del cierre (G), quienes llegaron a un establecimiento con mayor tasa de aprobación previa (en G−1) que su colegio cerrado (2.099) muestran una brecha de +2,03 puntos porcentuales, frente a +5,38 puntos entre quienes llegaron a uno de igual o menor aprobación (2.263). El patrón va en la dirección que sugiere la literatura, pero es descriptivo: las familias eligen el destino, la muestra deja fuera a quienes no se matricularon y la diferencia entre ambos grupos (−3,35 puntos) todavía no tiene un intervalo que la separe del azar.

<aside class="notice--info" markdown="1">
**Nota metodológica — Cómo comparé la calidad previa de la escuela receptora ($$\Delta Q_i$$):** Para evitar circularidad mecánica, definí la calidad de cada establecimiento estrictamente con su desempeño histórico previo al cierre (en G−1, antes de recibir a los alumnos desplazados) y calculé para cada estudiante reubicado la diferencia entre su escuela receptora y su escuela de origen en G−1 en tasa de aprobación, asistencia media y promedio de notas. Como las familias eligen el colegio de destino, este contraste es una heterogeneidad descriptiva y su diferencia todavía no tiene intervalo propio.
</aside>

### Educación superior: continuación de la serie

<!-- higher-education-agenda:start -->
Para quienes cursaban enseñanza media, la trayectoria no termina en la última matrícula escolar: todavía importa saber si el cierre se relaciona con el ingreso oportuno a la educación superior, el tipo de institución y la selectividad del destino. Esa pregunta no se estimó en esta parte escolar. La [parte IV]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/' | relative_url }}) utiliza registros individuales SIES y PAES/PDT con procedencia documentada; sus resultados y límites se leen allí, sin extrapolarlos a los desenlaces escolares de esta parte.
{: .notice--info}
<!-- higher-education-agenda:end -->
## Definición documental, comparabilidad y fuentes

<span id="certeza-documental-y-regla-empirica"></span>
### Cómo se define un cierre: de la certeza documental a la RCID v1

En la normativa educacional chilena no existe una figura normativa llamada "acta de cierre" que decrete el fin de un colegio. Que un establecimiento quede jurídicamente cerrado —en lenguaje legal, a través de un acto firme y ejecutoriado, es decir, una decisión oficial definitiva contra la cual ya no caben recursos— exige una **Resolución Exenta** dictada por la Secretaría Regional Ministerial (SEREMI) de Educación respectiva que extinga o suspenda su permiso para funcionar (el Reconocimiento Oficial). Esa resolución opera bajo cuatro figuras: receso temporal por un año lectivo, renuncia tácita al Reconocimiento Oficial si el plantel no retoma sus clases tras ese receso, renuncia voluntaria total o parcial al Reconocimiento Oficial (**artículos 25 y 26 del Decreto Supremo n.º 315 de 2010 del MINEDUC**; Castro Paredes 2013[^castroparedes2013]) o ejecución de la sanción de revocación del Reconocimiento Oficial ordenada por la Superintendencia de Educación (**artículo 73, letra f), de la [Ley n.º 20.529](https://www.bcn.cl/leychile/navegar?idNorma=1028635)**).

¿Están publicadas esas resoluciones para cada colegio del país? Para comprobarlo empíricamente, revisé, en octubre de 2026, el [Portal de Transparencia Activa](https://www.portaltransparencia.cl/PortalPdT/directorio-de-organismos-regulados/?org=AJ001) de la Subsecretaría de Educación (organismo AJ001, sección "Actos y resoluciones con efectos sobre terceras personas"). Entre las **12.509 resoluciones administrativas** y **4.735 resoluciones sancionatorias** disponibles, el repositorio histórico previo a 2018 se encuentra fuera de servicio y, entre 2018 y 2025, las 16 secretarías regionales solo registran **22 resoluciones administrativas** sobre renuncia, receso o cierre de establecimientos —varias de ellas declarando inadmisibles las solicitudes por falta de documentación o regularizando "cierres tácitos" años después de que el colegio dejó de funcionar— y **21 resoluciones sancionatorias únicas** que revocan el Reconocimiento Oficial. Mientras ese catastro nacional no se consolide mediante una solicitud de acceso a la información pública (**Ley n.º 20.285**), analizar veinte años de historia escolar exige una regla empírica transparente y falsable —la **Regla de Cierre Escolar Inferido desde los Datos (RCID v1)** presentada en la tabla A1 de este anexo— que funciona como tres coladores sucesivos (D0 ⊃ D1 ⊃ D2):

- **D0 (salida administrativa bruta):** el primer colador detecta toda escuela con matrícula positiva en un año (t−1) que deja de tener matrícula desde t, no reabre hasta 2025 y figura como cerrada en el directorio oficial.
- **D1 (cierre estricto de oferta):** el segundo colador retira de D0 los anexos o sedes secundarias y los cambios de código identificador —el Rol Base de Datos (RBD)— registrados como sucesores: es decir, las continuidades de directorio.
- **D2 = RCID v1 (cierre depurado por flujo estudiantil):** el tercer colador aparta los traslados concentrados: escuelas con al menos **10 estudiantes** de base y **10** seguidos al año siguiente, donde un único colegio receptor recibe al menos el **70 %** de los trasladados, con un índice de concentración de destinos (HHI) de al menos **0,50** y el mismo destino principal en t y t+1. Son candidatos a fusión de hecho que piden revisión documental, no pruebas de fusión.

La figura A2 resume la cobertura de la auditoría territorial de los 346 episodios de la tabla A2: cuántos tienen historia previa suficiente y cuántas alertas de flujo quedan sin confirmación institucional.

<figure class="post3-figure data-visualization" id="fig-post3-4">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }} 1600w" alt="De 346 episodios, 339 tienen tres años preevento completos y 323 tienen cinco. La clasificación contiene 266 sin señal contradictoria, 15 candidatos de continuidad, 35 alertas no resueltas y 30 censurados. Hay 45 alertas posevento y cero confirmaciones institucionales; el procesamiento automático solo permite observación." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura A2</strong> — Cobertura y límites de la auditoría territorial. Seguimiento longitudinal y alertas de flujo no sustituyen evidencia sobre capacidad, acceso, demografía o decisiones institucionales. <span class="figure-source">Fuente: elaboración propia a partir de directorios MINEDUC y la auditoría longitudinal.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/territorial-audit-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

### Comparabilidad antes del cierre

{: .table-caption}
<span id="tabla-post3-a6"></span>
**Tabla A6.** Similitud observada antes del cierre en la muestra ponderada (2016–2019)

| Característica previa | Estudiantes expuestos | Grupo de comparación | Lectura |
|---|---:|---:|---|
| Edad promedio | 11,70 años | 11,70 años | Diferencia estandarizada: 0,000. |
| Asistencia promedio | 90,93 % | 91,68 % | Diferencia estandarizada: −0,079. |
| Promedio de notas | 5,62 | 5,67 | Diferencia estandarizada: −0,072. |
| Registro válido de asistencia y notas | 76,8 % | 96,2 % | Brecha de cobertura: −19,4 pp (proporción observada, sin ponderar). |
{: .table--compact .table--scroll}

La edad se observa en toda la muestra y coincide por construcción, porque forma parte del pareo exacto. La asistencia y las notas, en cambio, solo pueden compararse entre quienes tienen esos registros; allí la cobertura es 76,8 % entre los expuestos y 96,2 % en el grupo de comparación (una brecha de −19,4 puntos porcentuales; con los controles reponderados al pareo, la brecha es de −19,2, la cifra que usa la figura 1 del artículo principal). Aquí aparece un vínculo directo con la norma: el **artículo 27, inciso segundo, del Decreto Supremo n.º 315 de 2010** (y el numeral noveno de la Circular n.º 1 de 2013 de la Superintendencia de Educación; Castro Paredes 2013[^castroparedes2013]) establece que la SEREMI *solo podrá pronunciarse* sobre una solicitud de receso o renuncia al Reconocimiento Oficial una vez que el sostenedor entregue las **actas de evaluación y promoción escolar de todos los alumnos y alumnas**, es decir, la planilla oficial de cierre de año que certifica las notas, la asistencia y quién pasó de curso. Casi uno de cada cuatro estudiantes expuestos (23,2 % frente a 3,8 % en los controles) carece de esa planilla en el año previo al cierre. Es tentador leer ahí un sostenedor que abandona el trámite, pero el patrón no lo confirma por sí solo. El **17 %** de los estudiantes sin acta está en 4 escuelas que no entregaron ninguna, y el **35 %**, en 3 escuelas que entregaron menos de la mitad. Eso es compatible con un cierre administrativo desordenado, como los "cierres tácitos" de Transparencia Activa. El **48 %** restante está disperso en escuelas que sí entregaron la mayoría de sus actas, lo que calza mejor con traslados o retiros a mitad de año. Ninguna de las dos explicaciones está probada, y la tabla A6 no certifica aleatorización ni comparabilidad sociodemográfica completa.

### Por qué se pre-registró el zoom 2016–2019 y cómo se articula con la serie 2005–2024

Concentrar el corte pre-registrado en **2016–2019** no fue una elección arbitraria: responde a que el estado de funcionamiento del directorio oficial se estandarizó desde 2015, a que observar varios años de historia previa dentro de un panel iniciado en 2004 empuja hacia mediados de la década de 2010, a que **2020–2022** estuvo distorsionado por la pandemia de COVID-19 y la promoción flexible, y a que **2024–2025** aún no cuenta con dos años posteriores completos para medir la ausencia persistente de matrícula. Por eso la lectura íntegra exige combinar ambos niveles: la tabla A4 de este anexo entrega la magnitud histórica de las veinte cohortes y sus cinco regímenes institucionales (donde el 89,7 % de los cierres ocurrió entre 2005 y 2015), mientras el zoom 2016–2019 documenta con máxima granularidad las pruebas de sensibilidad.

### Por qué no uso una variable instrumental

¿Podría resolverse esa selección previa usando una **variable instrumental** —es decir, un empujón externo parecido a un sorteo, como la entrada en operación de los Servicios Locales de Educación Pública (SLEP), el Sistema de Admisión Escolar (SAE) o las caídas demográficas comunales—? No en este diseño: para que un instrumento sea válido debe cumplir la llamada **restricción de exclusión**, que exige que ese factor externo afecte la progresión del alumno *únicamente* porque gatilló el cierre de su escuela y por ninguna otra vía. Esas reformas y cambios demográficos alteran al mismo tiempo los recursos locales, las vacantes disponibles y las decisiones cotidianas de las familias, incumpliendo esa condición. Sin un sorteo o umbral administrativo externo que supere relevancia y exclusión, forzar un modelo instrumental solo fabricaría falsa precisión. Por eso no ejecuto una regresión instrumental en esta versión.

### Tres verificaciones sobre tendencias previas, cobertura de actas y escuela receptora

Tres verificaciones adicionales sobre los microdatos precisan el alcance de la ventana 2016–2019:

1. **Sensibilidad a tendencias previas (versión lineal simplificada de Rambachan y Roth 2023) y alumnos estables desde G−2:** Los tres placebos previos al cierre en progresión son +0,16, +0,30 y +0,40 pp (mayor placebo: 0,40 pp; cota superior al 95 %: 0,81 pp). En la estimación de +5,29 pp (IC [2,08; 8,51]; cotas de −1,15 a 10,98 pp), el margen del intervalo hasta cero es 2,07 pp, equivalente a 2,54 veces esa cota superior de 0,81 pp (sin combinar con las cotas por datos faltantes). El **70,58 % de los 6.581 expuestos del universo descriptivo** era estable desde G−2; la estimación de progresión usa otra submuestra con soporte, de **3.556 estables** y **1.033 entrantes tardíos**. Sus brechas son **+3,87 pp** ([+1,04; +6,69]) y **+9,58 pp** ([+5,06; +14,10]), respectivamente: cerca de tres cuartas partes de la brecha puntual completa persiste entre los estables, sin identificar la causa de la diferencia entre grupos.
2. **Cotas por datos faltantes según cobertura de actas en G−1:** Faltan desenlaces para el 3,60 % de los expuestos y el 2,15 % de los controles; la proporción de recorte es (3,60 − 2,15)/(100 − 3,60) = 1,51 %. Con 90 % o más de actas válidas (1.822 expuestos con desenlace), la diferencia es +4,26 pp y las cotas de peor caso van de +0,09 a +7,84 pp, por lo que el cero queda fuera del rango de mezclas posibles (λ* = 1,0114 > 1); sin los 7 cierres con menos de 50 % de actas siguen en −0,90 a +12,18 pp; sin los 4 sin ninguna acta, en −0,87 a +11,48 pp. Ninguna incluye error muestral.
3. **Calidad previa de la escuela receptora ($$\Delta Q_i$$):** Entre 4.362 expuestos matriculados en otra escuela en G, quienes llegaron a una con mayor aprobación en G−1 que su escuela cerrada (2.099) muestran +2,03 pp, frente a +5,38 pp cuando la receptora tenía igual o menor aprobación (2.263). La diferencia descriptiva es −3,35 pp, sin intervalo propio; al definir la calidad por asistencia media o por promedio de notas, la diferencia es −2,05 y −2,43 pp. La muestra excluye a quienes no se matricularon en G.

### Fuentes de datos y herramientas

Las bases provienen de los datos abiertos del MINEDUC: [directorio de establecimientos](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/), [matrícula por estudiante](https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/) y [rendimiento por estudiante](https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/). Las procesé con [DuckDB](https://duckdb.org/) sobre archivos [Apache Parquet/Arrow](https://arrow.apache.org/), y estimé en Python con [pandas](https://pandas.pydata.org/), [SciPy](https://scipy.org/) y [statsmodels](https://www.statsmodels.org/stable/index.html), incluido el meta-análisis de efectos aleatorios. El marco legal de la SEP y de la Ley de Inclusión está en las leyes [n.º 20.248](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=269001&idVersion=) y [n.º 20.845](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=1078172&idParte=9605200&idVersion=2222-02-02).

**Transparencia y alcance de las fuentes.** La tesis original y esta serie de extensión son de mi autoría, al igual que la coautoría del [documento de trabajo de 2014]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }})[^grau2014]; por ello no constituyen una réplica externa independiente y mantienen separadas la reconstrucción histórica y la reestimación actual. No recibí financiamiento externo y declaro no tener conflictos de interés. Mi única afiliación institucional es el Ministerio de Desarrollo Social y Familia de Chile, que no financió, encargó ni revisó este análisis; las opiniones y conclusiones son de mi exclusiva responsabilidad. Utilicé asistentes de inteligencia artificial para apoyar programación reproducible, búsqueda bibliográfica, validación estadística y edición; toda decisión metodológica y verificación factual es propia. El código del análisis vive en un repositorio privado de la tesis y todavía no es público; las cifras agregadas de cada figura están en los CSV abiertos que acompañan a cada una.
{: .notice--info}

---
## Referencias

[^abdulkadiroglu2026]: Abdulkadiroğlu, Atila, Parag A. Pathak, and Christopher R. Walters. 2026. [“Who Gets What in Education: Can School Matching Improve Student Achievement?”](https://doi.org/10.3386/w34936) NBER Working Paper 34936. [Scholar](https://scholar.google.com/scholar_lookup?title=Who+Gets+What+in+Education%3A+Can+School+Matching+Improve+Student+Achievement%3F&doi=10.3386%2Fw34936)

[^beuchert2018]: Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen, and Nina Smith. 2018. [“The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?”](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47. [Scholar](https://scholar.google.com/scholar_lookup?title=The+short-term+effects+of+school+consolidation+on+student+achievement%3A+Evidence+of+disruption%3F&doi=10.1016%2Fj.econedurev.2018.05.004)

[^bross2023]: Bross, Whitney, Douglas N. Harris, and Lihan Liu. 2023. [“The Effects of Performance-Based School Closure and Restart on Student Performance.”](https://doi.org/10.1016/j.econedurev.2023.102368) *Economics of Education Review* 94: 102368. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effects+of+performance-based+school+closure+and+restart+on+student+performance&doi=10.1016%2Fj.econedurev.2023.102368)

[^brummet2014]: Brummet, Quentin. 2014. [“The Effect of School Closings on Student Achievement.”](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–24. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effect+of+school+closings+on+student+achievement&doi=10.1016%2Fj.jpubeco.2014.06.010)

[^castroparedes2013]: Castro Paredes, Luis. 2013. [*Cierre voluntario de Establecimientos Educacionales*](https://obtienearchivo.bcn.cl/obtienearchivo?id=repositorio/10221/20674/5/Cierre%20voluntario%20de%20Establecimientos%20Educacionales_v2.pdf). Asesoría Técnica Parlamentaria, Biblioteca del Congreso Nacional de Chile (BCN), 12 de diciembre de 2013.

[^engberg2012]: Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. [“Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?”](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203. [Scholar](https://scholar.google.com/scholar_lookup?title=Closing+schools+in+a+shrinking+district%3A+Do+student+outcomes+depend+on+which+schools+are+closed%3F&doi=10.1016%2Fj.jue.2011.10.001)

[^grau2014]: Grau, Nicolás, Daniel A. Hojman, Cristián Labra, and Alejandra Mizala. 2014. [“Destructive Creation: School Turnover and Educational Attainment.”]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}) Documento de Trabajo 396, Universidad de Chile.

[^grau2018]: Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. [“School Closure and Educational Attainment: Evidence from a Market-Based System.”](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf) *Economics of Education Review* 65: 1–17. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)

[^iocco2024]: Iocco, Maria Pia. 2024. [“Impact of Planned School Closures on Academic Performance: Evidence from Chile.”](https://doi.org/10.2139/ssrn.4808834) SSRN preprint. [Scholar](https://scholar.google.com/scholar_lookup?title=Impact+of+Planned+School+Closures+on+Academic+Performance%3A+Evidence+from+Chile&doi=10.2139%2Fssrn.4808834)

[^kim2024]: Kim, Jeonghyeok. 2024. [“The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes.”](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963. [Scholar](https://scholar.google.com/scholar_lookup?title=The+Long+Shadow+of+School+Closures%3A+Impacts+on+Students%27+Educational+and+Labor+Market+Outcomes&doi=10.26300%2FAX4M-3Z14)

[^larsen2020]: Larsen, Matthew F. 2020. [“Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment.”](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980. [Scholar](https://scholar.google.com/scholar_lookup?title=Does+closing+schools+close+doors%3F+The+effect+of+high+school+closings+on+achievement+and+attainment&doi=10.1016%2Fj.econedurev.2020.101980)

[^manski2003]: Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). New York: Springer. [Scholar](https://scholar.google.com/scholar_lookup?title=Partial+Identification+of+Probability+Distributions&doi=10.1007%2Fb97478)

[^rambachan2023]: Rambachan, Ashesh, and Jonathan Roth. 2023. [“A More Credible Approach to Parallel Trends.”](https://doi.org/10.1093/restud/rdad018) *The Review of Economic Studies* 90 (5): 2555–91. [Scholar](https://scholar.google.com/scholar_lookup?title=A+More+Credible+Approach+to+Parallel+Trends&doi=10.1093%2Frestud%2Frdad018)

[^steinberg2019]: Steinberg, Matthew P., and John M. MacDonald. 2019. [“The Effects of Closing Urban Schools on Students’ Academic and Behavioral Outcomes: Evidence from Philadelphia.”](https://doi.org/10.1016/j.econedurev.2018.12.005) *Economics of Education Review* 69: 25–60. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effects+of+closing+urban+schools+on+students%E2%80%99+academic+and+behavioral+outcomes%3A+Evidence+from+Philadelphia&doi=10.1016%2Fj.econedurev.2018.12.005)

[^taghizadeh2020]: Taghizadeh, Jonas Larsson. 2020. [“Are Students in Receiving Schools Hurt by the Closing of Low-Performing Schools? Effects of School Closures on Receiving Schools in Sweden 2000–2016.”](https://doi.org/10.1016/j.econedurev.2020.102020) *Economics of Education Review* 78: 102020. [Scholar](https://scholar.google.com/scholar_lookup?title=Are+students+in+receiving+schools+hurt+by+the+closing+of+low-Performing+schools%3F+Effects+of+school+closures+on+receiving+schools+in+Sweden+2000%E2%80%932016&doi=10.1016%2Fj.econedurev.2020.102020)
