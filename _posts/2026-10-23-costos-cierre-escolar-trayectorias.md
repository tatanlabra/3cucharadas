---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extender mi tesis en 3 cucharadas (parte III): qué muestran las trayectorias después del cierre de una escuela"
subtitle: "En las 19 cohortes medibles, la estimación puntual del rezago o la salida del registro de quienes perdieron su escuela fue mayor que la de sus pares. Todavía no puedo atribuir esa brecha al cierre."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-11-06 09:00:00 -0300
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

Cuando una escuela cierra, la pregunta pública no termina al encontrar otro colegio en el mapa. Importa saber si sus estudiantes siguieron matriculados, pasaron de curso y mantuvieron una asistencia regular. Y, sobre todo, importa distinguir qué parte de un tropiezo posterior se debe al cierre y qué parte venía gestándose desde antes.
{: .text-justify}

Para responderlo reconstruí veinte años de historia escolar sobre **79.709.054 registros de matrícula** y **73.873.835 de rendimiento** entre 2004 y 2025, y seguí **78.972 trayectorias estudiantiles** en **1.141 escuelas regulares** que cerraron entre 2005 y 2024 frente a **734.472 controles** de escuelas que seguían abiertas. La ventana larga admite dos lecturas que conviene sostener juntas. La primera: en las **19 cohortes anuales** que se pueden medir (2006–2024), la estimación puntual de la **proporción sin matrícula o con avance inferior al curso esperado al año siguiente —lo que llamo "falla de progresión o rezago"—** aumentó más entre quienes perdieron su escuela que entre sus pares, y esa brecha es positiva en las 19 (entre **+0,94 y +28,22 puntos porcentuales**, con mediana de **+7,18**). Al agregar la serie completa ponderando por los alumnos expuestos (Callaway y Sant'Anna), la brecha media es de **+9,11 puntos porcentuales** (intervalo de confianza del 95 % de **+5,34 a +12,88** y cotas de peor caso para datos faltantes de **+0,43 a +16,21 puntos**, que se mantienen sobre cero), acompañada de **+6,29 puntos** bajo un modelo de efectos aleatorios (**+4,49 a +8,09**, I² = 76,5 %) y, con la misma ponderación por expuestos, de **+1,38 puntos** en la no matrícula persistente por dos años. La segunda lectura: todavía no puedo atribuir esa brecha al cierre por sí solo, porque esas escuelas ya venían institucionalmente más frágiles y casi la mitad de sus estudiantes ya rotaba de colegio antes del evento.
{: .text-justify}

Al dividir las dos décadas en sus **cinco etapas institucionales**, aparece además un hallazgo estructural que una ventana corta no deja ver: el volumen de cierres se concentra en la primera mitad de la serie y la magnitud de la brecha se atenúa después. En **2005–2010** (régimen LOCE e inicio de la SEP; **521 cierres** y **36.984 alumnos expuestos**), la falla de progresión o rezago subió **+12,15 puntos porcentuales** —el único régimen donde el intervalo de confianza (**+3,78 a +20,52**) y las cotas de peor caso para datos faltantes (**+3,49 a +18,83**) excluyen el cero al mismo tiempo— y la no matrícula a dos años aumentó **+1,21 puntos**. En **2011–2015** (instalación de la LGE y del Sistema de Aseguramiento de la Calidad; **502 cierres** y **31.512 expuestos**), la brecha de progresión fue de **+7,82 puntos** y la no matrícula por dos años alcanzó su máximo de **+1,85 puntos**: juntas, esas dos primeras etapas concentran el **89,7 % de los cierres regulares** y el **86,7 % de los estudiantes expuestos** de toda la serie. Luego la brecha baja a **+5,29 puntos porcentuales** en **2016–2019** (implementación gradual de la Ley de Inclusión; **63 cierres** y **6.190 expuestos**, con cotas de **−1,15 a 10,98 puntos**), a **+2,70 puntos** en **2020–2022** (pandemia y promoción flexible; **33 cierres** y **3.272 expuestos**) y a **+2,59 puntos** en **2023–2024** (pospandemia; **22 cierres** y **1.014 expuestos**).
{: .text-justify}

Frente a esa serie de veinte años, la subventana **2016–2019** —el corte que fijé como ventana principal antes de mirar la serie completa, y cuyas cifras provienen de la **reestimación posterior al piloto**, es decir, de volver a estimar con el diseño ya fijado lo que un piloto exploratorio había tanteado antes— representa apenas el **5,5 % de los cierres con soporte** (63 de 1.141) y el **7,8 % de los estudiantes expuestos** (6.190 de 78.972), y por la concentración del alumnado en pocos colegios pesa estadísticamente como unas **21 o 22 escuelas independientes**. En ese zoom reciente, la falla de progresión o rezago subió **5,29 puntos porcentuales** más entre los expuestos que en sus controles (intervalo conservador del 95 % de **2,08 a 8,51 puntos**; la tasa pasó de 2,2 % a 15,8 % cuando lo esperable según sus controles era 10,6 %), pero las cotas sin supuestos para los datos faltantes (Manski 2003[^manski2003]) van de **−1,15 a 10,98 puntos porcentuales**. Como ese intervalo cruza cero, la subventana 2016–2019 entrega por sí sola **evidencia parcial e inconclusa**: no demuestra daño, beneficio ni ausencia de efecto, pero funciona como un laboratorio exigente para someter los resultados a pruebas de estrés sobre tendencias previas, cobertura de actas y escuela receptora sin fabricar el contrafactual de qué habría pasado con esos mismos niños, niñas y adolescentes (NNA) si su escuela hubiese seguido abierta.
{: .text-justify}

<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->
<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->

La [parte I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) reconstruyó la evidencia histórica y separó qué hallazgos resistían. La [parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) verificó qué establecimientos cerraron en la década reciente y mostró que la escuela más cercana rara vez es el destino principal. Esta tercera entrega pasa de los edificios a las trayectorias estudiantiles en tres pasos: **qué cerró realmente en veinte años**, **qué ocurrió después con los estudiantes en la serie larga y en sus cinco etapas** y **cómo proteger una transición escolar en la práctica**.
{: .text-justify}

**Guía rápida.** Llamo **G** al primer año en que la escuela ya no tiene matrícula; **G−1** es su último año abierto y **G+1**, el siguiente. En la progresión de curso, el "antes" se mide dos años antes del cierre (G−2) y el "después", en G+1. **pp** son puntos porcentuales; **RBD** es el código de cada escuela; **SEP**, la Subvención Escolar Preferencial; **JEC**, la Jornada Escolar Completa; **RCID**, la regla de cierre que construí desde los datos. Las **cotas de Manski** (o cotas por datos faltantes) son el rango que seguiría siendo posible si a los alumnos sin dato les hubiera ido, a todos, lo peor o lo mejor: si ese rango cruza el cero, los datos faltantes bastan para cambiar el signo del resultado.
{: .notice--info .text-justify}

## Cucharada 1: ¿qué cerró y quién quedó expuesto en veinte años?

### Veinte años de cierres bajo tres coladores sucesivos (RCID v1, 2005–2025)

En Chile, el cierre jurídico de un colegio exige una resolución exenta de la SEREMI de Educación, pero no existe un registro público y completo de esas resoluciones: lo comprobé en Transparencia Activa (detalle en las notas metodológicas al final). Por eso construí una regla empírica y falsable, la **Regla de Cierre Escolar Inferido desde los Datos (RCID v1)**, que funciona como tres coladores sucesivos (**D0 ⊃ D1 ⊃ D2**) sobre veinte años de datos administrativos. El primero (**D0**) detecta la matrícula que desaparece; el segundo (**D1**) descarta anexos y cambios de código; el tercero (**D2**) aparta los traslados en bloque a un solo colegio. En simple: no es lo mismo que un curso entero se mude junto a otro edificio a que cada familia deba buscar cupo por su cuenta.
{: .text-justify}

{: .table-caption}
**Tabla 1.** Jerarquía de la Regla de Cierre Escolar Inferido desde los Datos (RCID v1, D0 ⊃ D1 ⊃ D2) en las tres entregas (2005–2025)

| Estrato de la regla | Ventana histórica (2005–2015) | Ventana reciente (2016–2025) | Serie longitudinal (2005–2025) | Qué depura y cómo se usa en las partes I, II y III |
|---|---:|---:|---:|---|
| D0: salida administrativa o de actividad bruta | 1.635 | 346 | 1.981 | Cese de matrícula en t; contrasta con las 2.069 salidas brutas de directorio de 1992–2012 en la parte I. |
| D1: cierre estricto de oferta educativa | 1.477 | 330 | 1.807 | Depura 158 anexos, sedes o sucesores de RBD históricos y 16 continuidades de directorio recientes (base de la parte II). |
| D2 = RCID v1 (conservador, incluye censurados de 2025) | 1.382 | 296 | 1.678 | Depura además 95 absorciones históricas y 34 absorciones o alertas de flujo concentradas recientes (≥ 10 estudiantes de base y asignados, ≥ 70 % al destino principal y HHI ≥ 0,50). |
| D2 = RCID v1 (limpio con ventana t+1 observada) | 1.382 | 266 | 1.648 | Exige además observar el año t+1 completo (excluye los 30 episodios de 2025 censurados a la derecha); base principal de la parte III. |
{: .table--compact .table--scroll}

Como muestra la tabla 1, aplicar RCID v1 (D2) deja **1.648 cierres limpios** con ventana posterior observada en toda la serie 2005–2025 —**1.382** en la ventana histórica 2005–2015 y **266** en la ventana reciente 2016–2024— y constituye el punto de partida para evaluar trayectorias sin mezclar fusiones de hecho con cierres dispersos. No todos esos cierres pueden seguirse con trayectorias de curso: solo **1.177** tenían estudiantes de educación regular (básica de 1.º a 8.º o media de 1.º a 3.º) y **1.141** encontraron controles comparables (**78.972 estudiantes expuestos** y **734.472 controles**). En la ventana reciente, **145 de los 266** cierres eran escuelas solo de párvulos (69), solo de educación especial (57), solo de adultos (13) o solo de cuarto medio (1), o tenían predominio de esas ofertas (5). Allí no se puede medir la progresión de curso, así que los resultados de esta entrega hablan de escuelas regulares, no de todo cierre.
{: .text-justify}

### Un flujo estudiantil es una señal, no un acto administrativo: el corte 2016–2025

En el período reciente (2016–2025) existen **346 episodios** donde una escuela con matrícula dejó de operar. Al descontar anexos, cambios administrativos y continuidades probables, la [parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) identificó **330 cierres estrictos** (D1) de oferta educativa. Seguir a sus estudiantes al año siguiente permite detectar cuándo casi todo el alumnado se traslada en bloque a un único colegio receptor: eso puede reflejar una fusión, un cambio de código o simplemente una alternativa vecina capaz de recibirlos, pero el flujo por sí solo no reemplaza un acto administrativo.
{: .text-justify}

{: .table-caption}
**Tabla 2.** Lectura diagnóstica de los 346 episodios registrados como cierres en el período reciente (2016–2025)

| Estado | Episodios | Lectura permitida |
|---|---:|---|
| Sin señal contradictoria | 266 | La trayectoria no contradice el cierre estricto; no constituye corroboración externa. |
| Continuidad candidata | 15 | Nombre, nivel o modalidad, o actividad posterior justifican una revisión documental. |
| Alerta no resuelta | 35 | La categoría no cambia mientras falte evidencia independiente. |
| Seguimiento incompleto | 30 | Son cierres de 2025 y todavía no se observa el año siguiente. |
{: .table--compact .table--scroll}

Cada uno de los 346 episodios entra en una sola fila de la tabla 2. Las **45 alertas por destino concentrado** son un corte transversal que se superpone con esas categorías y no se suma a ellas; sin contar aún con **confirmaciones institucionales independientes** (**cero** en este corte), los 330 cierres estrictos se mantienen como base de referencia de la parte II, mientras esta entrega trabaja sobre los cierres D2 de la tabla 1.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-1">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-es-dark.svg' | relative_url }} 1600w" alt="Dos carriles resumen el soporte de la reestimación post-piloto de 2016 a 2019. De 64 episodios históricos antes del soporte, 63 conservan al menos un estrato comparable y uno queda completamente fuera. De 6.581 observaciones estudiante-cohorte expuestas, 391 se excluyen y 6.190 permanecen. El universo de soporte contiene 82.753 observaciones estudiante-cohorte de control; las muestras finales cambian según el desenlace." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 1</strong> — Cómo se forma la muestra comparable en el zoom pre-registrado (2016–2019). Los conteos agregados preceden la elegibilidad específica de cada resultado y sus unidades no deben sumarse. <span class="figure-source">Fuente: elaboración propia a partir de la reestimación post-piloto.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/sample-flow-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

La figura 1 distingue entre escuelas cerradas (episodios) y observaciones "estudiante-cohorte" (cada alumno contado dentro de su cohorte de cierre). Además, la información publicada es estrictamente agregada: por resguardo de privacidad, no expone nombres, direcciones ni códigos individuales de estudiantes o establecimientos.
{: .text-justify}

### Quiénes eran los estudiantes expuestos

Antes de mirar qué les pasó, conviene saber quiénes eran. La tabla 3 resume ocho características de los niños, niñas y adolescentes (NNA) y de sus escuelas de origen, medidas un año antes del cierre (G−1); solo la última fila mira más atrás, desde G−3, para capturar la rotación previa.
{: .text-justify}

{: .table-caption}
**Tabla 3.** Caracterización ampliada de niños, niñas y adolescentes (NNA) en G−1 (cohortes 2016–2019, 6.190 expuestos y 82.753 controles)

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

La radiografía de la tabla 3 explica por qué hay que ser cautelosos tanto en la serie larga como en el corte reciente: los estudiantes expuestos y sus controles tienen la misma edad, el mismo rezago previo (33,86 %) y prácticamente la misma vulnerabilidad individual elegible para la Subvención Escolar Preferencial (54,51 % frente a 55,58 %, con **30,68 %** de alumnos prioritarios), pero asistían a colegios institucionalmente más frágiles —con menos convenio SEP (−10,06 pp) y menos Jornada Escolar Completa (−18,54 pp)— y casi la mitad (**47,04 %** frente a 30,52 %) ya había cambiado de colegio en los dos años previos. Una parte del desgaste escolar y de la rotación familiar ya estaba en marcha antes del cierre. Además, solo cuento como expuestos a quienes seguían matriculados en G−1: si las familias con más recursos se fueron antes del cierre, el grupo expuesto ya llega seleccionado.
{: .text-justify}

## Cucharada 2: ¿qué ocurrió después del cierre en la ventana grande y en sus cinco etapas?

### La serie completa 2005–2024 y sus cinco etapas institucionales

El corazón empírico de esta entrega está en las veinte cohortes anuales entre **2005 y 2024**. Cuando los colegios cierran en años distintos, mezclarlos en un promedio simple cometería el error de usar escuelas recién cerradas como si fueran controles estables de las que cierran después. Los estimadores modernos de **diferencias en diferencias escalonadas** (Callaway y Sant'Anna 2021[^callaway2021]; Sun y Abraham 2021[^sun2021]; Roth et al. 2023[^roth2023]) evitan esa distorsión comparando cada cohorte anual únicamente contra establecimientos que aún no han cerrado. Aquí calculo además cotas por datos faltantes (Manski 2003[^manski2003]) y evalúo la sensibilidad a tendencias previas no paralelas con una versión simplificada de la idea de Rambachan y Roth (2023[^rambachan2023]). Bajo la regla RCID v1 (D2), la serie completa abarca **20 cohortes anuales**, **1.141 episodios con soporte empírico**, **78.972 observaciones expuestas** y **734.472 controles**. De esas 20 cohortes, 19 son estimables en progresión y 17 en no matrícula persistente: las que caen en el borde del panel 2004–2025 no tienen el año "antes" (G−2) o el segundo año "después" dentro de los datos. El detalle año a año está disponible en el [CSV abierto de la figura 2]({{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}), y la tabla 4 sintetiza los cinco períodos institucionales, el rango anual y tres formas distintas de agregar las dos décadas.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-2">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-es-dark.svg' | relative_url }} 1600w" alt="Infografía en tres paneles bajo la regla RCID v1 con 1.141 episodios con soporte entre 2005 y 2024. El panel A muestra las 19 cohortes anuales estimables de falla de progresión o rezago entre 2006 y 2024: las 19 son positivas, con rango de 0,94 a 28,22 puntos porcentuales, mediana de 7,18 y agregado ponderado de Callaway y Sant'Anna de +9,11 puntos (intervalo de 5,34 a 12,88 y cotas de Manski de +0,43 a +16,21 puntos). El panel B resume la atenuación por régimen institucional desde 12,15 puntos en 2005–2010 y 7,82 en 2011–2015 hasta 5,29 en 2016–2019 (con cotas por datos faltantes de menos 1,15 a 10,98 puntos), 2,70 en 2020–2022 y 2,59 en 2023–2024. El panel C muestra las brechas basales en G menos 1 tras el pareo exacto: la elegibilidad SEP es similar (−1,07 puntos), pero los expuestos asisten a escuelas con menos convenio SEP (−10,06 puntos), menos JEC (−18,54 puntos), menor cobertura de acta (−19,24 puntos) y mayor rotación previa (+16,52 puntos)." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 2</strong> — Serie completa 2005–2024 bajo la regla RCID v1: estimaciones anuales (2006–2024), atenuación en las cinco etapas institucionales y brechas de caracterización de NNA en G−1. <span class="figure-source">Fuente: elaboración propia a partir del panel longitudinal 2004–2025 del MINEDUC.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

{: .table-caption}
**Tabla 4.** Síntesis de la serie completa 2005–2024 por régimen institucional, rango anual y esquemas de agregación (RCID v1)

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

Los N de la tabla 4 corresponden al soporte; cada estimación usa el subconjunto con desenlace observable (por ejemplo, 4.815 expuestos en progresión 2016–2019). Las cotas de Manski no incluyen error muestral. El agregado de efectos aleatorios (Paule-Mandel, con intervalo de Hartung-Knapp) reemplaza al de varianza inversa de la versión anterior; aquel suponía un efecto común a todas las cohortes, lo que con una heterogeneidad de 76,5 % produce un intervalo artificialmente estrecho. Como las cohortes comparten controles, incluso estos intervalos pueden quedar algo cortos.
{: .text-justify}

La serie de veinte años y sus cinco divisiones institucionales (figura 2 y tabla 4) entregan cuatro hallazgos principales:
{: .text-justify}

- **Las 19 cohortes estimables de progresión son positivas, y el agregado se mantiene sobre cero bajo los tres esquemas de ponderación, aunque con alta heterogeneidad entre épocas:** al ponderar por el volumen de alumnos afectados (Callaway y Sant'Anna), la diferencia media es de **+9,11 puntos porcentuales** ([+5,34; +12,88]) y sus cotas de Manski (**+0,43 a +16,21**) se mantienen sobre cero, junto con **+1,38 puntos** ([+0,92; +1,85]) en la no matrícula persistente por dos años. Con pesos iguales por cohorte anual es de **+7,55 puntos** ([+5,52; +9,57]) en progresión y **+1,03 puntos** ([+0,56; +1,50]) en no matrícula. Y bajo un modelo de efectos aleatorios (I² = 76,5 %, τ = 2,81 pp), la media es de **+6,29 puntos** ([+4,49; +8,09]), con un intervalo de predicción de **+0,09 a +12,49 puntos** que indica dónde podría ubicarse la brecha de una cohorte nueva.
- **2005–2010 (régimen LOCE e inicio de la SEP) y 2011–2015 (instalación de la LGE y del SAC) concentran casi nueve de cada diez cierres y las mayores brechas:** en **2005–2010** (**521 episodios**, **36.984 expuestos** y **334.062 controles**), la falla de progresión subió **+12,15 puntos porcentuales** ([+3,78; +20,52]) y tanto su intervalo de confianza como sus cotas de Manski (**+3,49 a +18,83**) excluyen el cero a la vez, mientras la no matrícula por dos años subió **+1,21 puntos** ([+0,53; +1,90]). En **2011–2015** (**502 episodios**, **31.512 expuestos** y **260.740 controles**), la brecha de progresión fue de **+7,82 puntos** ([+6,20; +9,41]; cotas [−2,11; +16,18]) y la no matrícula por dos años alcanzó su máximo de toda la serie con **+1,85 puntos porcentuales** ([+1,10; +2,59]). En conjunto, ambas etapas reúnen **1.023 de los 1.141 cierres** (89,7 %) y **68.496 de los 78.972 estudiantes expuestos** (86,7 %).
- **Desde 2016 el número de cierres cae abruptamente y la brecha se atenúa a través de las tres etapas recientes:** en **2016–2019** (implementación gradual de la Ley de Inclusión; **63 episodios** y **6.190 expuestos**), la brecha baja a **+5,29 puntos porcentuales** ([+2,08; +8,51], con cotas de **−1,15 a 10,98 puntos**) y **+0,63 puntos** en no matrícula. En **2020–2022** (pandemia y promoción flexible; **33 episodios** y **3.272 expuestos**), se comprime a **+2,70 puntos** ([−0,63; +6,03]; cotas [+0,18; +4,95]) y **−0,28 puntos** en no matrícula. Y en **2023–2024** (reactivación pospandemia; **22 episodios** y **1.014 expuestos**), se sitúa en **+2,59 puntos** ([−1,55; +6,73]; cotas [−1,70; +6,07]) y **−0,93 puntos** en no matrícula.
- **La atenuación entre regímenes es un hecho descriptivo robusto, pero no el efecto aislado de una ley:** esa caída coincide en el tiempo con la SEP, el Sistema de Aseguramiento de la Calidad (SAC) y la Ley de Inclusión, pero no se les puede atribuir de forma directa, porque también cambiaron el tipo de escuelas que cierran y la forma de registrar el estado de los colegios en 2015, la promoción flexible de 2020–2022 reduce el rezago de forma mecánica y las muestras recientes son mucho más pequeñas.

### El zoom pre-registrado 2016–2019: evidencia parcial y dos resultados primarios

Visto ese panorama de veinte años, la ventana **2016–2019** cobra su sentido exacto: fue el corte que fijé antes de estimar la serie larga porque desde 2015 se estandarizó el directorio oficial, permitía observar varios años previos sin chocar con el inicio del panel en 2004 y evitaba la distorsión de la pandemia de 2020–2022. Pero como solo reúne **63 de los 1.141 episodios con soporte** (el 5,5 % de la serie, de los cuales **62 episodios** tienen ventana observable para los dos resultados primarios y **58** para asistencia y notas), sus resultados deben leerse como **evidencia parcial**.
{: .text-justify}

En este zoom 2016–2019, el primer resultado primario mira cuántos estudiantes quedan **sin matrícula durante dos años seguidos**: no lo llamo "deserción" porque salir del registro administrativo chileno no aclara si el alumno abandonó los estudios, salió del país o pasó a una modalidad no cubierta. Allí el cambio del grupo expuesto supera en **+0,63 puntos porcentuales** al del grupo de comparación, con un intervalo conservador del 95 % de **−0,77 a 2,03 puntos** (sobre **3.666** observaciones expuestas y **49.944** controles).
{: .text-justify}

El segundo resultado primario mide la proporción **sin matrícula o bajo el curso esperado al año siguiente**, resumida como **falla de progresión o rezago**. En 2016–2019 la brecha antes-después sube en **+5,29 puntos porcentuales** entre los expuestos frente a sus controles (intervalo conservador de **2,08 a 8,51 puntos**, sobre **4.815** observaciones expuestas y **65.538** controles). Pero el dato falta para el **3,60 %** de los expuestos y el **2,15 %** de los controles, y las **cotas de Manski** (Manski 2003[^manski2003]) van de **−1,15 a 10,98 puntos porcentuales** —una prueba de esfuerzo sin optimismo que asigna a los alumnos sin dato el peor desenlace en un grupo y el mejor en el otro, y luego al revés—. Por eso el resultado de este subperíodo es **inconcluso** por sí solo: entre los expuestos la falla pasa de **2,2 %** dos años antes del cierre a **15,8 %** el año siguiente frente al **10,6 %** esperable según sus controles (un **50 %** más que ese contrafactual y, solo si fuese causal, unos **255 estudiantes**), sin que el indicador separe salida del registro y repitencia. Las cotas solo excluyen el cero dentro de este subperíodo en los cierres con al menos 90 % de actas válidas el año previo (un 38 % de los expuestos).
{: .text-justify}

{: .table-caption}
**Tabla 5.** Reestimación posterior al piloto en el zoom pre-registrado (2016–2019): diferencias observadas, no efectos causales

| Resultado | Diferencia estimada | Intervalo conservador del 95 % | Condición decisiva |
|---|---:|---:|---|
| No matrícula persistente por dos años | +0,63 pp | [−0,77; 2,03] | No equivale a deserción; la tendencia previa estimable se apoya en pocos episodios. |
| Falla de progresión o rezago: sin matrícula o bajo el curso esperado al año siguiente | +5,29 pp | [2,08; 8,51] | Cotas por datos faltantes: [−1,15; 10,98] pp en el total; [0,09; 7,84] pp en cierres con ≥ 90 % de actas válidas en G−1 (38 % de los expuestos). Sin error muestral. |
| Asistencia | −1,15 puntos | [−2,40; 0,10] | Exploratoria y condicionada; exige asistencia válida y estado final promovido/reprobado observable. |
| Promedio de notas | −0,06 | [−0,14; 0,01] | Exploratorio y condicionado; solo entre quienes tienen rendimiento observable. |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-3">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-es-dark.svg' | relative_url }} 1600w" alt="Reestimación post-piloto inconclusa de dos resultados primarios. La no matrícula persistente se estima en 0,63 puntos porcentuales, con IC de menos 0,77 a 2,03; en la muestra distinta que incluye escuelas receptoras, 0,71, con IC de menos 0,69 a 2,12. La falla de progresión o rezago se estima en 5,29 puntos, con IC de 2,08 a 8,51; en la muestra distinta con receptoras, 5,09, con IC de 1,94 a 8,23. Sus límites por datos faltantes abarcan de menos 1,15 a 10,98 puntos. No son efectos causales confirmados." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 3</strong> — Zoom pre-registrado 2016–2019: reestimación post-piloto inconclusa, no efectos causales. El intervalo de progresión no cruza cero, pero sus cotas por datos faltantes sí; el solapamiento con el piloto y los supuestos no observados impiden atribuir causalidad. <span class="figure-source">Fuente: elaboración propia a partir de la reestimación post-piloto.</span> <span class="figure-data">Datos tabulares accesibles: <a href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-data.csv' | relative_url }}">estimaciones</a> y <a href="{{ '/assets/images/tesis-post3/missingness-bounds-data.csv' | relative_url }}">cotas por datos faltantes</a>.</span></figcaption>
</figure>

La asistencia y el promedio de notas en la tabla 5 son **exploratorias y condicionadas**: solo pueden medirse entre quienes tienen acta anual válida en ambos períodos. Eso deja **3.871** observaciones expuestas en **58 episodios**, el **62,5 %** del soporte expuesto, frente a **63.591** de los **82.753** controles en asistencia (63.596 en notas). En la figura 3, además, la barra alternativa que incluye a las escuelas receptoras en el grupo de control entrega **+0,71 puntos porcentuales** en no matrícula ([−0,69; 2,12], con 3.670 expuestos y 59.613 controles) y **+5,09 puntos** en falla de progresión ([1,94; 8,23], con 4.822 expuestos y 79.058 controles): cambiar qué escuelas entran al control modifica la muestra, pero no despeja las cotas de **−1,15 a 10,98 puntos** asociadas al +5,29 pp principal.
{: .text-justify}

El tamaño efectivo de este subperíodo se entiende mejor como una **sala de reuniones**. Aunque la estimación 2016–2019 reúne 62 escuelas cerradas, unas pocas concentran gran parte del alumnado. Escuchar esos 62 cierres se parece menos a oír 62 voces independientes del mismo volumen y más a oír unos **21,1 episodios efectivos** en no matrícula, **21,9** en progresión y apenas **17,7** en asistencia y notas. Del mismo modo, la exploración entre zonas urbanas y rurales descansa en aún menos episodios rurales, por lo que no permite hacer recomendaciones territoriales sin incorporar antes tiempos de viaje por red vial y transporte escolar.
{: .text-justify}

### ¿Se comparan peras con peras? Tendencias previas y cobertura de actas

Tanto en la serie larga como en el zoom 2016–2019, el diseño utiliza **diferencias en diferencias**, que compara dos películas en lugar de dos fotografías sueltas: primero empareja a cada alumno de una escuela que cerrará con estudiantes de control idénticos un año antes del cierre (G−1) en año calendario, sexo, edad, región, dependencia del sostenedor, ruralidad, nivel de enseñanza y curso, y luego mide cuánto cambió la trayectoria del primer grupo antes y después del evento frente al cambio de sus pares. En simple: busco comparar peras con peras en todo lo que el registro permite ver, midiendo su cercanía mediante la **diferencia estandarizada** (distancia en unidades de dispersión donde cero equivale a igualdad).
{: .text-justify}

En lo observable, los grupos quedan casi idénticos en edad, asistencia y notas, con diferencias estandarizadas menores a 0,08. Pero los expuestos tienen muchas menos actas anuales válidas el año previo al cierre: 76,8 % frente a 96,2 %. A la vez, tres pruebas placebo anteriores al cierre en 2016–2019 dan diferencias de +0,16, +0,30 y +0,40 puntos en progresión: el intervalo de la estimación de +5,29 pp (con cotas de −1,15 a 10,98 puntos) deja de excluir el cero si un sesgo posterior al cierre alcanza 2,07 puntos, unas 2,54 veces la cota superior al 95 % del mayor placebo (0,81 puntos), sin combinar ese cálculo con las cotas por datos faltantes. Y al separar a los alumnos estables en la misma escuela entre G−2 y G−1 —3.556, el 77,5 % de los expuestos con curso observado en G−2 y G−1 (70,6 % del total)— de los entrantes tardíos (1.033), la falla de progresión sube **+3,87 puntos porcentuales** ([+1,04; +6,69]) entre los estables y **+9,58 puntos** ([+5,06; +14,10]) entre los entrantes tardíos: cerca de tres cuartas partes de la brecha se mantiene entre quienes llevaban al menos dos años en la escuela.
{: .text-justify}

<aside class="notice--info" markdown="1">
**Nota metodológica — Qué cambia según la cobertura de actas y cuánto sesgo anularía el intervalo:** Las cotas de peor caso de Manski (2003[^manski2003]) no suponen nada sobre los alumnos sin dato, así que su amplitud depende de cuántos faltan. El artículo 27 del Decreto Supremo n.º 315 exige al sostenedor entregar las actas de promoción antes de que la SEREMI resuelva el cierre; no observo esa entrega, sino la proporción de estudiantes con acta válida en el panel. En los cierres de 2016–2019 donde esa proporción llega al 90 % (1.822 expuestos con desenlace), los faltantes casi se igualan entre grupos (2,31 % frente a 2,15 %), la diferencia es de +4,26 puntos y las cotas van de +0,09 a +7,84 puntos; excluir solo los cierres con menos de la mitad de actas deja las cotas entre −0,90 y +12,18 puntos. Por su parte, el umbral de 2,07 puntos de sesgo posterior al cierre (2,54 veces la cota superior de 0,81 puntos del mayor placebo) aplica una versión lineal y simplificada de la idea de Rambachan y Roth (2023[^rambachan2023]), no su estimador formal, y ninguna de estas dos pruebas incorpora simultáneamente el error muestral de las cotas.
</aside>

### Qué agrega —y qué no agrega— la literatura

Buena parte de la evidencia internacional sugiere que el impacto de cerrar una escuela depende conjuntamente del proceso de transición y de la calidad del establecimiento receptor: suele haber pérdidas durante el anuncio y el primer año, seguidas de recuperación parcial cuando los estudiantes acceden a escuelas de mayor valor agregado, pero con costos duraderos en asistencia o graduación secundaria cuando la reubicación ocurre hacia planteles congestionados o de desempeño similar (Engberg et al. 2012[^engberg2012]; Brummet 2014[^brummet2014]; Beuchert et al. 2018[^beuchert2018]; Steinberg y MacDonald 2019[^steinberg2019]; Larsen 2020[^larsen2020]; Taghizadeh 2020[^taghizadeh2020]; Bross, Harris y Liu 2023[^bross2023]; Kim 2024[^kim2024]), en línea con la literatura sobre asignación escolar y calidad del establecimiento de destino (Abdulkadiroğlu, Pathak y Walters 2026[^abdulkadiroglu2026]). En Chile, Grau, Hojman y Mizala (2018[^grau2018]) estimaron aumentos en repitencia y deserción en un período anterior, mientras que Iocco (2024[^iocco2024]), en un preprint sobre cierres planificados, reporta efectos promedio nulos en puntajes con heterogeneidad según la escuela de destino. Por diferencias de período, definición de tratamiento y variable dependiente, tanto la serie completa 2005–2024 (+9,11 puntos en Callaway y Sant'Anna; +6,29 en efectos aleatorios) como la estimación 2016–2019 de 5,29 puntos porcentuales —con cotas de −1,15 a 10,98 puntos— complementan pero no replican ni refutan mecánicamente esos trabajos.
{: .text-justify}

### ¿Importa a qué escuela llegan?

En mi panel 2016–2019 exploré una pieza de ese mecanismo. Entre los 4.362 estudiantes expuestos que se matricularon en otra escuela el año del cierre (G), quienes llegaron a un establecimiento con mayor tasa de aprobación previa (en G−1) que su colegio cerrado (2.099) muestran una brecha de +2,03 puntos porcentuales, frente a +5,38 puntos entre quienes llegaron a uno de igual o menor aprobación (2.263). El patrón va en la dirección que sugiere la literatura, pero es descriptivo: las familias eligen el destino, la muestra deja fuera a quienes no se matricularon y la diferencia entre ambos grupos (−3,35 puntos) todavía no tiene un intervalo que la separe del azar.
{: .text-justify}

<aside class="notice--info" markdown="1">
**Nota metodológica — Cómo comparé la calidad previa de la escuela receptora ($$\Delta Q_i$$):** Para evitar circularidad mecánica, definí la calidad de cada establecimiento estrictamente con su desempeño histórico previo al cierre (en G−1, antes de recibir a los alumnos desplazados) y calculé para cada estudiante reubicado la diferencia entre su escuela receptora y su escuela de origen en G−1 en tasa de aprobación, asistencia media y promedio de notas. Como las familias eligen el colegio de destino, este contraste es una heterogeneidad descriptiva y su diferencia todavía no tiene intervalo propio.
</aside>

### Educación superior: una pregunta que queda abierta

<!-- higher-education-agenda:start -->
Para quienes cursaban enseñanza media, la trayectoria no termina en la última matrícula escolar: todavía importa saber si el cierre se relaciona con el ingreso oportuno a la educación superior, el tipo de institución y la selectividad del destino. Esa pregunta queda para una entrega posterior. Requiere microdatos individuales del SIES con procedencia oficial y, para distinguir rendición, postulación, admisión y matrícula, un enlace validado con datos del DEMRE. Como esos insumos no están acreditados para este ejercicio, aquí no se estiman ni se sugieren efectos postsecundarios. La agenda futura no condiciona la publicación de los resultados escolares de esta parte.
{: .notice--info .text-justify}
<!-- higher-education-agenda:end -->

## Cucharada 3: ¿cómo se protege una transición escolar?

### La evidencia sirve antes de resolver la causalidad

Que el efecto causal exacto tenga límites de identificación en la serie larga y sea inconcluso en la subventana reciente no justifica quedarse de brazos cruzados cuando una escuela cierra. Al contrario: el diagnóstico longitudinal muestra exactamente dónde se pierde el rastro de los estudiantes y qué garantías operativas deben exigirse antes, durante y después de reorganizar una red escolar.
{: .text-justify}

{: .table-caption}
**Tabla 6.** Información mínima para decidir y evaluar una transición

| Antes de decidir | Durante la transición | Después del cambio |
|---|---|---|
| Distinguir establecimiento, sede, nivel, fusión y cambio de Rol Base de Datos (RBD). | Asignar vacantes reales y apoyos a cada estudiante. | Seguir matrícula, asistencia, progresión, notas y bienestar. |
| Registrar fecha de anuncio y participación de la comunidad. | Medir tiempo de viaje, accesibilidad y continuidad de compañeros. | Observar también a estudiantes y equipos de las receptoras. |
| Verificar capacidad, dotación y calidad previa de los destinos. | Financiar la carga receptora y la continuidad pedagógica. | Publicar alertas, correcciones y responsabilidades con plazos. |
{: .table--compact .table--scroll}

La tabla 6 invierte la carga de la prueba frente a un vacío procedimental concreto: cuando la Biblioteca del Congreso Nacional consultó a la Unidad de Reconocimiento Oficial de la SEREMI Metropolitana en qué consistía la "constancia de reubicación de los alumnos" exigida en la pauta administrativa de cierre voluntario, la autoridad precisó que dicho requisito —ausente de la ley y del Decreto Supremo n.º 315 de 2010— consistía únicamente en "haber informado a los alumnos alternativas de reubicación de su matrícula", sin verificar si esos establecimientos contaban con vacantes reales ni si los estudiantes lograban matricularse en ellos (Castro Paredes 2013[^castroparedes2013], p. 2, n. 1). La autoridad no puede dar por garantizada la continuidad educativa solo porque el sostenedor saliente entregó una lista de colegios cercanos o porque parte del alumnado reapareció matriculado: debe acreditar de antemano vacantes efectivas, transporte seguro, apoyos para estudiantes prioritarios y soporte pedagógico en las escuelas receptoras, y monitorear nominalmente qué pasa con cada estudiante durante al menos dos años.
{: .text-justify}

## Cierre: seguir trayectorias cambia la pregunta pública

La parte I reconstruyó los cimientos históricos; la parte II depuró qué escuelas cerraron y qué oferta existía alrededor; esta tercera parte siguió a **78.972 estudiantes en 1.141 cierres regulares** a lo largo de veinte años. Mirar la ventana grande (2005–2024) cambia la perspectiva: las 19 cohortes anuales estimables son positivas, el agregado de Callaway y Sant'Anna alcanza **+9,11 puntos porcentuales** (con cotas de Manski de **+0,43 a +16,21 puntos** sobre cero; **+6,29 puntos** bajo efectos aleatorios) y las cinco etapas institucionales muestran una caída desde **+12,15 puntos** en 2005–2010 y **+7,82** en 2011–2015 hasta **+5,29 puntos porcentuales** en la subventana pre-registrada 2016–2019 —que siempre debe leerse junto a sus cotas por datos faltantes de **−1,15 a 10,98 puntos**—, **+2,70** en 2020–2022 y **+2,59** en 2023–2024, todo ello condicionado por la mayor fragilidad institucional y rotación previa de las escuelas que cierran.
{: .text-justify}

Un resultado con límites causales sí permite fijar resguardos prudenciales hoy: no tratar la cercanía ni una constancia meramente informativa como continuidad, no reorganizar una red sin verificar cupos y apoyos, y seguir a cada estudiante durante la transición. Estos resguardos no son efectos estimados de esas decisiones. Son el estándar mínimo de cuidado público mientras se consolidan las Resoluciones Exentas de término del Reconocimiento Oficial, las fechas de anuncio, la capacidad receptora y la entrega íntegra de las actas de evaluación y promoción escolar.
{: .text-justify}


<details markdown="1" class="post3-methods">
<summary>Notas metodológicas: regla de cierre, comparabilidad, serie completa y fuentes</summary>

### Cómo se define un cierre: de la certeza documental a la RCID v1

En la normativa educacional chilena no existe una figura normativa llamada "acta de cierre" que decrete el fin de un colegio. Que un establecimiento quede jurídicamente cerrado —en lenguaje legal, a través de un acto firme y ejecutoriado, es decir, una decisión oficial definitiva contra la cual ya no caben recursos— exige una **Resolución Exenta** dictada por la Secretaría Regional Ministerial (SEREMI) de Educación respectiva que extinga o suspenda su permiso para funcionar (el Reconocimiento Oficial). Esa resolución opera bajo cuatro figuras: receso temporal por un año lectivo, renuncia tácita al Reconocimiento Oficial si el plantel no retoma sus clases tras ese receso, renuncia voluntaria total o parcial al Reconocimiento Oficial (**artículos 25 y 26 del Decreto Supremo n.º 315 de 2010 del MINEDUC**; Castro Paredes 2013[^castroparedes2013]) o ejecución de la sanción de revocación del Reconocimiento Oficial ordenada por la Superintendencia de Educación (**artículo 73, letra f), de la [Ley n.º 20.529](https://www.bcn.cl/leychile/navegar?idNorma=1028635)**).
{: .text-justify}

¿Están publicadas esas resoluciones para cada colegio del país? Para comprobarlo empíricamente, revisé, en octubre de 2026, el [Portal de Transparencia Activa](https://www.portaltransparencia.cl/PortalPdT/directorio-de-organismos-regulados/?org=AJ001) de la Subsecretaría de Educación (organismo AJ001, sección "Actos y resoluciones con efectos sobre terceras personas"). Entre las **12.509 resoluciones administrativas** y **4.735 resoluciones sancionatorias** disponibles, el repositorio histórico previo a 2018 se encuentra fuera de servicio y, entre 2018 y 2025, las 16 secretarías regionales solo registran **22 resoluciones administrativas** sobre renuncia, receso o cierre de establecimientos —varias de ellas declarando inadmisibles las solicitudes por falta de documentación o regularizando "cierres tácitos" años después de que el colegio dejó de funcionar— y **21 resoluciones sancionatorias únicas** que revocan el Reconocimiento Oficial. Mientras ese catastro nacional no se consolide mediante una solicitud de acceso a la información pública (**Ley n.º 20.285**), analizar veinte años de historia escolar exige una regla empírica transparente y falsable —la **Regla de Cierre Escolar Inferido desde los Datos (RCID v1)** presentada en la tabla 1 del cuerpo principal— que funciona como tres coladores sucesivos (D0 ⊃ D1 ⊃ D2):
{: .text-justify}

- **D0 (salida administrativa bruta):** el primer colador detecta toda escuela con matrícula positiva en un año (t−1) que deja de tener matrícula desde t, no reabre hasta 2025 y figura como cerrada en el directorio oficial.
- **D1 (cierre estricto de oferta):** el segundo colador retira de D0 los anexos o sedes secundarias y los cambios de código identificador —el Rol Base de Datos (RBD)— registrados como sucesores: es decir, las continuidades de directorio.
- **D2 = RCID v1 (cierre depurado por flujo estudiantil):** el tercer colador aparta los traslados concentrados: escuelas con al menos **10 estudiantes** de base y **10** seguidos al año siguiente, donde un único colegio receptor recibe al menos el **70 %** de los trasladados, con un índice de concentración de destinos (HHI) de al menos **0,50** y el mismo destino principal en t y t+1. Son candidatos a fusión de hecho que piden revisión documental, no pruebas de fusión.

La figura 4 resume la cobertura de la auditoría territorial de los 346 episodios de la tabla 2: cuántos tienen historia previa suficiente y cuántas alertas de flujo quedan sin confirmación institucional.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-4">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-es-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-es-dark.svg' | relative_url }} 1600w" alt="De 346 episodios, 339 tienen tres años preevento completos y 323 tienen cinco. La clasificación contiene 266 sin señal contradictoria, 15 candidatos de continuidad, 35 alertas no resueltas y 30 censurados. Hay 45 alertas posevento y cero confirmaciones institucionales; el procesamiento automático solo permite observación." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 4</strong> — Cobertura y límites de la auditoría territorial. Seguimiento longitudinal y alertas de flujo no sustituyen evidencia sobre capacidad, acceso, demografía o decisiones institucionales. <span class="figure-source">Fuente: elaboración propia a partir de directorios MINEDUC y la auditoría longitudinal.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/territorial-audit-data.csv' | relative_url }}">Datos tabulares accesibles (CSV)</a>.</span></figcaption>
</figure>

### Comparabilidad antes del cierre

{: .table-caption}
**Tabla 7.** Similitud observada antes del cierre en la muestra ponderada (2016–2019)

| Característica previa | Estudiantes expuestos | Grupo de comparación | Lectura |
|---|---:|---:|---|
| Edad promedio | 11,70 años | 11,70 años | Diferencia estandarizada: 0,000. |
| Asistencia promedio | 90,93 % | 91,68 % | Diferencia estandarizada: −0,079. |
| Promedio de notas | 5,62 | 5,67 | Diferencia estandarizada: −0,072. |
| Registro válido de asistencia y notas | 76,8 % | 96,2 % | Brecha de cobertura: −19,4 pp (proporción observada, sin ponderar). |
{: .table--compact .table--scroll}

La edad se observa en toda la muestra y coincide por construcción, porque forma parte del pareo exacto. La asistencia y las notas, en cambio, solo pueden compararse entre quienes tienen esos registros; allí la cobertura es 76,8 % entre los expuestos y 96,2 % en el grupo de comparación (una brecha de −19,4 puntos porcentuales; con los controles reponderados al pareo, la brecha es de −19,2, la cifra que usa la figura 2). Aquí aparece un vínculo directo con la norma: el **artículo 27, inciso segundo, del Decreto Supremo n.º 315 de 2010** (y el numeral noveno de la Circular n.º 1 de 2013 de la Superintendencia de Educación; Castro Paredes 2013[^castroparedes2013]) establece que la SEREMI *solo podrá pronunciarse* sobre una solicitud de receso o renuncia al Reconocimiento Oficial una vez que el sostenedor entregue las **actas de evaluación y promoción escolar de todos los alumnos y alumnas**, es decir, la planilla oficial de cierre de año que certifica las notas, la asistencia y quién pasó de curso. Casi uno de cada cuatro estudiantes expuestos (23,2 % frente a 3,8 % en los controles) carece de esa planilla en el año previo al cierre. Es tentador leer ahí un sostenedor que abandona el trámite, pero el patrón no lo confirma por sí solo. El **17 %** de los estudiantes sin acta está en 4 escuelas que no entregaron ninguna, y el **35 %**, en 3 escuelas que entregaron menos de la mitad. Eso es compatible con un cierre administrativo desordenado, como los "cierres tácitos" de Transparencia Activa. El **48 %** restante está disperso en escuelas que sí entregaron la mayoría de sus actas, lo que calza mejor con traslados o retiros a mitad de año. Ninguna de las dos explicaciones está probada, y la tabla 7 no certifica aleatorización ni comparabilidad sociodemográfica completa.
{: .text-justify}

### Por qué se pre-registró el zoom 2016–2019 y cómo se articula con la serie 2005–2024

Concentrar el corte pre-registrado en **2016–2019** no fue una elección arbitraria: responde a que el estado de funcionamiento del directorio oficial se estandarizó desde 2015, a que observar varios años de historia previa dentro de un panel iniciado en 2004 empuja hacia mediados de la década de 2010, a que **2020–2022** estuvo distorsionado por la pandemia de COVID-19 y la promoción flexible, y a que **2024–2025** aún no cuenta con dos años posteriores completos para medir la ausencia persistente de matrícula. Por eso la lectura íntegra exige combinar ambos niveles: la tabla 4 del cuerpo principal entrega la magnitud histórica de las veinte cohortes y sus cinco regímenes institucionales (donde el 89,7 % de los cierres ocurrió entre 2005 y 2015), mientras el zoom 2016–2019 documenta con máxima granularidad las pruebas de sensibilidad.
{: .text-justify}

### Por qué no uso una variable instrumental

¿Podría resolverse esa selección previa usando una **variable instrumental** —es decir, un empujón externo parecido a un sorteo, como la entrada en operación de los Servicios Locales de Educación Pública (SLEP), el Sistema de Admisión Escolar (SAE) o las caídas demográficas comunales—? No en este diseño: para que un instrumento sea válido debe cumplir la llamada **restricción de exclusión**, que exige que ese factor externo afecte la progresión del alumno *únicamente* porque gatilló el cierre de su escuela y por ninguna otra vía. Esas reformas y cambios demográficos alteran al mismo tiempo los recursos locales, las vacantes disponibles y las decisiones cotidianas de las familias, incumpliendo esa condición. Sin un sorteo o umbral administrativo externo que supere relevancia y exclusión, forzar un modelo instrumental solo fabricaría falsa precisión. Por eso no ejecuto una regresión instrumental en esta versión.
{: .text-justify}

### Tres verificaciones sobre tendencias previas, cobertura de actas y escuela receptora

Tres verificaciones adicionales sobre los microdatos precisan el alcance de la ventana 2016–2019:
{: .text-justify}

1. **Sensibilidad a tendencias previas (versión lineal simplificada de Rambachan y Roth 2023) y alumnos estables desde G−2:** Los tres placebos previos al cierre en progresión son +0,16, +0,30 y +0,40 pp (mayor placebo: 0,40 pp; cota superior al 95 %: 0,81 pp). En la estimación de +5,29 pp (IC [2,08; 8,51]; cotas de −1,15 a 10,98 pp), el margen del intervalo hasta cero es 2,07 pp, equivalente a 2,54 veces esa cota superior de 0,81 pp (sin combinar con las cotas por datos faltantes). Entre los **alumnos estables en la misma escuela desde G−2** —3.556, el 77,5 % de los expuestos con curso observado en G−2 y G−1 (70,6 % del total)—, la falla de progresión sube **+3,87 pp** ([+1,04; +6,69]), frente a **+9,58 pp** ([+5,06; +14,10]) en los **entrantes tardíos entre G−2 y G−1** (1.033): cerca de tres cuartas partes de la brecha persiste entre los alumnos estables.
2. **Cotas por datos faltantes según cobertura de actas en G−1:** Faltan desenlaces para el 3,60 % de los expuestos y el 2,15 % de los controles; la proporción de recorte es (3,60 − 2,15)/(100 − 3,60) = 1,51 %. Con 90 % o más de actas válidas (1.822 expuestos con desenlace), la diferencia es +4,26 pp y las cotas de peor caso van de +0,09 a +7,84 pp, por lo que el cero queda fuera del rango de mezclas posibles (λ* = 1,0114 > 1); sin los 7 cierres con menos de 50 % de actas siguen en −0,90 a +12,18 pp; sin los 4 sin ninguna acta, en −0,87 a +11,48 pp. Ninguna incluye error muestral.
3. **Calidad previa de la escuela receptora ($$\Delta Q_i$$):** Entre 4.362 expuestos matriculados en otra escuela en G, quienes llegaron a una con mayor aprobación en G−1 que su escuela cerrada (2.099) muestran +2,03 pp, frente a +5,38 pp cuando la receptora tenía igual o menor aprobación (2.263). La diferencia descriptiva es −3,35 pp, sin intervalo propio; al definir la calidad por asistencia media o por promedio de notas, la diferencia es −2,05 y −2,43 pp. La muestra excluye a quienes no se matricularon en G.

### Fuentes de datos y herramientas

Las bases provienen de los datos abiertos del MINEDUC: [directorio de establecimientos](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/), [matrícula por estudiante](https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/) y [rendimiento por estudiante](https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/). Las procesé con [DuckDB](https://duckdb.org/) sobre archivos [Apache Parquet/Arrow](https://arrow.apache.org/), y estimé en Python con [pandas](https://pandas.pydata.org/), [SciPy](https://scipy.org/) y [statsmodels](https://www.statsmodels.org/stable/index.html), incluido el meta-análisis de efectos aleatorios. El marco legal de la SEP y de la Ley de Inclusión está en las leyes [n.º 20.248](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=269001&idVersion=) y [n.º 20.845](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=1078172&idParte=9605200&idVersion=2222-02-02).
{: .text-justify}

</details>

**Transparencia y alcance de las fuentes.** La tesis original y esta serie de extensión son de mi autoría, al igual que la coautoría del [documento de trabajo de 2014]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }})[^grau2014]; por ello no constituyen una réplica externa independiente y mantienen separadas la reconstrucción histórica y la reestimación actual. No recibí financiamiento externo y declaro no tener conflictos de interés. Mi única afiliación institucional es el Ministerio de Desarrollo Social y Familia de Chile, que no financió, encargó ni revisó este análisis; las opiniones y conclusiones son de mi exclusiva responsabilidad. Utilicé asistentes de inteligencia artificial para apoyar programación reproducible, búsqueda bibliográfica, validación estadística y edición; toda decisión metodológica y verificación factual es propia. El código del análisis vive en un repositorio privado de la tesis y todavía no es público; las cifras agregadas de cada figura están en los CSV abiertos que acompañan a cada una.
{: .notice--info .text-justify}

---

## Referencias

[^abdulkadiroglu2026]: Abdulkadiroğlu, Atila, Parag A. Pathak, and Christopher R. Walters. 2026. [“Who Gets What in Education: Can School Matching Improve Student Achievement?”](https://doi.org/10.3386/w34936) NBER Working Paper 34936. [Scholar](https://scholar.google.com/scholar_lookup?title=Who+Gets+What+in+Education%3A+Can+School+Matching+Improve+Student+Achievement%3F&doi=10.3386%2Fw34936)

[^beuchert2018]: Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen, and Nina Smith. 2018. [“The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?”](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47. [Scholar](https://scholar.google.com/scholar_lookup?title=The+short-term+effects+of+school+consolidation+on+student+achievement%3A+Evidence+of+disruption%3F&doi=10.1016%2Fj.econedurev.2018.05.004)

[^bross2023]: Bross, Whitney, Douglas N. Harris, and Lihan Liu. 2023. [“The Effects of Performance-Based School Closure and Restart on Student Performance.”](https://doi.org/10.1016/j.econedurev.2023.102368) *Economics of Education Review* 94: 102368. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effects+of+performance-based+school+closure+and+restart+on+student+performance&doi=10.1016%2Fj.econedurev.2023.102368)

[^brummet2014]: Brummet, Quentin. 2014. [“The Effect of School Closings on Student Achievement.”](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–24. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effect+of+school+closings+on+student+achievement&doi=10.1016%2Fj.jpubeco.2014.06.010)

[^callaway2021]: Callaway, Brantly, and Pedro H. C. Sant'Anna. 2021. [“Difference-in-Differences with Multiple Time Periods.”](http://arxiv.org/pdf/1803.09015) *Journal of Econometrics* 225 (2): 200–230. [DOI](https://doi.org/10.1016/j.jeconom.2020.12.001) · [Scholar](https://scholar.google.com/scholar_lookup?title=Difference-in-Differences+with+multiple+time+periods&doi=10.1016%2Fj.jeconom.2020.12.001)

[^castroparedes2013]: Castro Paredes, Luis. 2013. [*Cierre voluntario de Establecimientos Educacionales*](https://obtienearchivo.bcn.cl/obtienearchivo?id=repositorio/10221/20674/5/Cierre%20voluntario%20de%20Establecimientos%20Educacionales_v2.pdf). Asesoría Técnica Parlamentaria, Biblioteca del Congreso Nacional de Chile (BCN), 12 de diciembre de 2013.

[^engberg2012]: Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. [“Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?”](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203. [Scholar](https://scholar.google.com/scholar_lookup?title=Closing+schools+in+a+shrinking+district%3A+Do+student+outcomes+depend+on+which+schools+are+closed%3F&doi=10.1016%2Fj.jue.2011.10.001)

[^grau2014]: Grau, Nicolás, Daniel A. Hojman, Cristián Labra, and Alejandra Mizala. 2014. [“Destructive Creation: School Turnover and Educational Attainment.”]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}) Documento de Trabajo 396, Universidad de Chile.

[^grau2018]: Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. [“School Closure and Educational Attainment: Evidence from a Market-Based System.”](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf) *Economics of Education Review* 65: 1–17. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)

[^iocco2024]: Iocco, Maria Pia. 2024. [“Impact of Planned School Closures on Academic Performance: Evidence from Chile.”](https://doi.org/10.2139/ssrn.4808834) SSRN preprint. [Scholar](https://scholar.google.com/scholar_lookup?title=Impact+of+Planned+School+Closures+on+Academic+Performance%3A+Evidence+from+Chile&doi=10.2139%2Fssrn.4808834)

[^kim2024]: Kim, Jeonghyeok. 2024. [“The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes.”](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963. [Scholar](https://scholar.google.com/scholar_lookup?title=The+Long+Shadow+of+School+Closures%3A+Impacts+on+Students%27+Educational+and+Labor+Market+Outcomes&doi=10.26300%2FAX4M-3Z14)

[^larsen2020]: Larsen, Matthew F. 2020. [“Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment.”](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980. [Scholar](https://scholar.google.com/scholar_lookup?title=Does+closing+schools+close+doors%3F+The+effect+of+high+school+closings+on+achievement+and+attainment&doi=10.1016%2Fj.econedurev.2020.101980)

[^manski2003]: Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). New York: Springer. [Scholar](https://scholar.google.com/scholar_lookup?title=Partial+Identification+of+Probability+Distributions&doi=10.1007%2Fb97478)

[^rambachan2023]: Rambachan, Ashesh, and Jonathan Roth. 2023. [“A More Credible Approach to Parallel Trends.”](https://doi.org/10.1093/restud/rdad018) *The Review of Economic Studies* 90 (5): 2555–91. [Scholar](https://scholar.google.com/scholar_lookup?title=A+More+Credible+Approach+to+Parallel+Trends&doi=10.1093%2Frestud%2Frdad018)

[^roth2023]: Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–44. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)

[^steinberg2019]: Steinberg, Matthew P., and John M. MacDonald. 2019. [“The Effects of Closing Urban Schools on Students’ Academic and Behavioral Outcomes: Evidence from Philadelphia.”](https://doi.org/10.1016/j.econedurev.2018.12.005) *Economics of Education Review* 69: 25–60. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effects+of+closing+urban+schools+on+students%E2%80%99+academic+and+behavioral+outcomes%3A+Evidence+from+Philadelphia&doi=10.1016%2Fj.econedurev.2018.12.005)

[^sun2021]: Sun, Liyang, and Sarah Abraham. 2021. [“Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects.”](https://doi.org/10.1016/j.jeconom.2020.09.006) *Journal of Econometrics* 225 (2): 175–99. [Scholar](https://scholar.google.com/scholar_lookup?title=Estimating+dynamic+treatment+effects+in+event+studies+with+heterogeneous+treatment+effects&doi=10.1016%2Fj.jeconom.2020.09.006)

[^taghizadeh2020]: Taghizadeh, Jonas Larsson. 2020. [“Are Students in Receiving Schools Hurt by the Closing of Low-Performing Schools? Effects of School Closures on Receiving Schools in Sweden 2000–2016.”](https://doi.org/10.1016/j.econedurev.2020.102020) *Economics of Education Review* 78: 102020. [Scholar](https://scholar.google.com/scholar_lookup?title=Are+students+in+receiving+schools+hurt+by+the+closing+of+low-Performing+schools%3F+Effects+of+school+closures+on+receiving+schools+in+Sweden+2000%E2%80%932016&doi=10.1016%2Fj.econedurev.2020.102020)
