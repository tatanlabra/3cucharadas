---
layout: single
classes: [thesis-recreation-post]
title: "Replicar mi tesis en 3 cucharadas (parte I): qué sobrevivió y qué corrigió la evidencia"
subtitle: "Volví a medir mi tesis de 2014 sobre entrada y salida de colegios. La historia general resistió, varias cifras no, y los archivos de cálculo permitieron entender por qué."
date: 2026-08-29 09:30:00 -0400
last_modified_at: 2026-11-06 09:00:00 -0300
categories: [datos, educacion, politica-publica]
tags: [replicabilidad, educacion, mercado-escolar, voucher, mineduc, analisis-de-duracion, vulnerabilidad, auditoria]
description: "Recreé los resultados de mi tesis de 2014 sobre establecimientos educacionales en Chile y audité 34 afirmaciones: qué se sostuvo, qué estaba mal entonces y qué todavía no puede saberse."
excerpt: "La tesis no salió intacta, pero tampoco se derrumbó. Los archivos productores permitieron separar resultados recreados, errores de 2014, sensibilidades y límites de la evidencia."
author: clabra
lang: es
ref: replica-tesis-establecimientos-educacionales
permalink: /datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/
audio:
  duracion_s: 1188
  fecha: "2026-10-17"
  generador: NotebookLM (Google)
  voces: 2
  idioma: es
  plataformas:
    - nombre: Spotify
      url: https://open.spotify.com/episode/7ho9naqSgAotsTfcsBmOwc
    - nombre: Apple Podcasts
      url: https://podcasts.apple.com/cl/podcast/id6811713988
header:
  teaser: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/og-1200x630.webp
  og_image_alt: Tesis archivada y modelos escolares reconstruidos como metáfora de una réplica que corrige su original.
  overlay_image: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/teaser-mobile-640x360.webp
visual_id: replica-tesis-establecimientos
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

En abril de 2014 defendí y entregué mi tesis de magíster sobre entrada y salida de establecimientos educacionales en Chile entre 1992 y 2012.[^tesis] Doce años después estoy tratando de recrearla y extenderla hasta 2025.
{: .text-justify}

En ese intervalo cambiaron las reglas: municipalización en los ochenta; financiamiento compartido en los noventa; Subvención Escolar Preferencial (SEP) en los dos mil; Inclusión y Nueva Educación Pública en los diez; y otra arquitectura estatal en los veinte.[^regimenes] El mercado mutó y también cambiaron las relaciones que podrían explicar los cierres.
{: .text-justify}

Antes de sumar trece años había que responder una pregunta más modesta: **¿qué resultados de 2014 podía volver a producir con exactitud?** En síntesis, 15 juicios quedaron respaldados y 10 errores provenían de 2014. Ninguno de esos errores pasó a la versión de 2026 que uso como referencia. De los 9 restantes, 1 fallaba a ambos lados, 1 era una coincidencia engañosa y 7 no permiten atribuir con claridad dónde estuvo el error.
{: .text-justify}

No quería convertir esto en una pelea entre herramientas: la historia no es que Python derrotara a Stata ni que mi antiguo MacBook perdiera ante el Lenovo actual. Es qué sobrevivió al contraste, con más evidencia y experiencia —y el sesgo inevitable de auditarse a uno mismo—. La tesis es mía y la auditoría también: no es una réplica independiente.
{: .text-justify}

Nada de lo que sigue es causal. "Entrada" y "salida" significan aparecer o desaparecer del registro, no observar la decisión de abrir, cerrar o quebrar. "IVE" es vulnerabilidad escolar agregada, no pobreza ni vulnerabilidad individual. Y "recreado" significa producido otra vez desde los datos y el código disponible, no haber recuperado la sesión exacta de 2014. RBD es el identificador oficial de cada establecimiento, y SIMCE, la prueba nacional estandarizada de aprendizaje. Serie completa: **Parte I** · [Parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) · [Parte III]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/' | relative_url }}).
{: .small}

## Cucharada 1: qué sobrevivió

La primera conclusión sí resistió: entre 1992 y 2012 no hubo simplemente más o menos colegios; hubo una **reasignación entre dependencias** (tipos de administración escolar). Mi reconstrucción suma 2.168 entradas y 2.069 salidas. El sector municipal registra 346 entradas y 1.135 salidas; el particular subvencionado, 1.468 y 597; el particular pagado, 354 y 337.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp' | relative_url }}" title="Figura 1 — Movilidad por dependencia" aria-label="Abrir la Figura 1 ampliada">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp' | relative_url }}" alt="A la izquierda, la figura de movilidad total por dependencia administrativa publicada en 2014. A la derecha, la réplica de 2026: municipal 346 entradas y 1.135 salidas, particular subvencionado 1.468 y 597, particular pagado 354 y 337." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figura 1</strong> — Movilidad por dependencia. La reconstrucción totaliza 2.168 entradas y 2.069 salidas; la planilla de 2014, 2.160 y 2.065. El patrón —salida municipal y entrada subvencionada— sobrevive. Fuente: Labra Olivares (2014), tesis de magíster (izquierda), y recreación propia de 2026 sobre el directorio de establecimientos 1992–2012 (derecha).</figcaption>
</figure>

Los totales no son idénticos, pero cuentan la misma historia. En el Cuadro 1 de 2012, la distancia agregada de participaciones respecto de la corrida previa de mi planilla de 2014 es de 3,05 puntos porcentuales, mientras que la suma de diferencias absolutas en puntos porcentuales entre las seis participaciones del texto publicado y la planilla llega a 13,41 puntos (4,50 puntos en municipal, 2,42 en particular subvencionado sin cobro y 4,27 en cobro alto): la recreación se parece más al archivo productor que a la prosa que firmé.
{: .text-justify}

La segunda conclusión que resistió es distributiva. En el Gran Santiago (Cuadro 8), los establecimientos que después salen del registro atendían una matrícula más vulnerable: 87,4 % frente a 78,3 % en municipales y 72,2 % frente a 62,8 % en particulares subvencionados. Las 42 celdas reconstruidas son compatibles con el margen de redondeo publicado, aunque el número efectivo de observaciones no coincide con el impreso. La magnitud sobrevive; el universo exacto, no.
{: .text-justify}

Esto describe selección (quiénes integran cada grupo), no efectos. Con datos de 2002 a 2012, Paredes y Fresard asocian menor matrícula con mayor probabilidad de cierre y estudian el destino posterior de los alumnos.[^paredes2018] Núñez, Solís y Soto examinan dos comunidades rurales del sur tras el terremoto de 2010 y muestran que el modo de cerrar una escuela importa para la cohesión social.[^nunez2014] Mis datos siguen las mismas unidades en el tiempo, pero no alcanzan para sostener esas conclusiones: observan flujos administrativos, no motivos, trayectorias ni vida comunitaria.
{: .text-justify}

También sobrevivieron varios resultados más pequeños: **10 de los 11 efectos fijos publicados** (coeficientes promedio del modelo), la brecha SIMCE de los subvencionados que cierran, siete comunas sobre un umbral de movilidad y el signo negativo entre concentración y movilidad. Con la constante, son 12 coeficientes en el archivo, 11 efectos en el cuadro y 10 coincidencias.
{: .text-justify}

{: .table-caption}
**Tabla 1.** Balance de la auditoría y diferencias que cambian la lectura

| Nivel | Resultado | Evidencia | Veredicto |
|---|---|---|---|
| Balance | 15 calces; 10 errores de 2014; 0 errores conocidos en la salida 2026 | Los archivos productores y las nuevas ejecuciones distinguen un error publicado de uno de reconstrucción. | La historia general resiste, pero no todas sus cifras. |
| Límite | 1 error a ambos lados; 1 coincidencia engañosa; 7 casos de procedencia o sin ganador | La evidencia explica por qué no hay una comparación válida, aunque no permita nombrar un ganador. | No se fuerza una tasa de acierto. |
| Rezago SIMCE | Publicado: 0,003; salida productora y dos motores: 0,001 | 0,000533 redondea a 0,001. | Error de transcripción de 2014. |
| Varianzas del modelo | Publicado: 3,82 y 2,791 | Eran log-desviaciones cruzadas | Error de interpretación de 2014. |
| IHH comunal | Santiago ≈ 1.534 | Escala canónica ≈ 152 | Error de escala de 2014. |
| Ciudades menores | Publicado: cerca de 80 % | Capital/no capital: 78,3 %; población: 11 % | La cifra describía otra partición. |
| Brecha SIMCE | Publicado: −4,3 % | Hoja productora: −4,3 % | Valor productor verificado. |
| Movilidad | Tasas 6,3; 4,5; 1,6 | Fórmulas productoras recuperan todos los puntos | Calce final correcto; lectura causal no probada. |
| Descomposición entre/dentro (Cuadros 3 y 7) | ln(matrícula) y SIMCE rezagado: asociación entre colegios (0,012131; *t* = 16,27), no distinguible de cero dentro de cada colegio (−0,000048; *t* = −0,53). Alumnos/docente: brecha media de 5,90 y 6,23; caída adicional de 0,216 y 0,148 por año, sin errores estándar | Cuadro 7: MCO agrupados con promedios de Mundlak y errores agrupados por RBD; sustituye la pendiente aleatoria que colapsaba (2,1 × 10⁻¹⁵). Cuadro 3: descomposición descriptiva. | La asociación SIMCE–matrícula refleja selección entre colegios; el vaciamiento previo es descriptivo. |
| Alerta predictiva fuera de muestra (Cuadro 10) | Entrenamiento 2007–2008 y prueba 2009–2011: AUC = 0,8517; Brier = 0,008196 frente a 0,008324 sin modelo | El decil superior de riesgo captura el 43,7 % de los 151 cierres (69,5 % en el quintil); riesgo medio predicho de 0,60 % frente a 0,84 % observado. | Ordena bien el riesgo fuera de muestra; subestima su nivel y no identifica causas. |
{: .table--compact .table--scroll}

El recuento por figura responde otra pregunta. De 26 objetos, hay doce convergencias, diez divergencias explicadas y cuatro sin prueba numérica; no queda ninguna divergencia inexplicada. No convierto ese inventario en "porcentaje de acierto": una desigualdad, un redondeo y una igualdad literal no son la misma prueba.
{: .small}

## Cucharada 2: quién se equivocó

Una discrepancia entre 2014 y 2026 no identifica por sí sola al equivocado. Puede nacer en una transcripción, el código, la muestra o un cambio del estimando; con solo "publicado" y "reconstruido", esas explicaciones se inventan después de conocer el resultado.
{: .text-justify}

Clemens propone una regla conservadora: “follow-up studies should be considered robustness checks until proven to be replications” (p. 327).[^clemens2015] En castellano: un seguimiento es una prueba de robustez hasta demostrar que es una réplica. No es semántica: Herndon, Ash y Pollin solo aislaron exclusiones, errores de código y ponderaciones al obtener la planilla de trabajo de Reinhart y Rogoff.[^herndon2013] Para Christensen y Miguel, abrir datos y materiales permite someter la credibilidad de la evidencia a examen.[^christensen2018] Hamermesh distingue la réplica pura, que revisa un trabajo publicado con sus propios datos, de la réplica científica, que prueba el resultado con otra población, y advierte que ambas escasean en economía: es una actividad que casi todos aplauden y pocos practican.[^hamermesh2007]
{: .text-justify}

Por eso incorporé una tercera fuente: archivos de 2014 que conservan rastros del cálculo, como salidas de Stata, planillas y gráficos, y, cuando fue posible, una nueva ejecución. Antes de atribuir una diferencia, verifiqué de dónde provenía cada archivo, dejé constancia y definí la comparación. Las tres fuentes permanecen separadas para que una reparación técnica no reescriba la evidencia histórica. La tercera no siempre favoreció al presente.
{: .text-justify}

<figure class="recreation-pipeline-figure">
  <a href="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-es.svg' | relative_url }}" target="_blank" rel="noopener">
    <picture>
      <source media="(max-width: 47.99em)" srcset="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-es-mobile.svg' | relative_url }}">
      <img src="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-es.svg' | relative_url }}" alt="Tres clases de insumos —piezas y datos, estadística descriptiva y econometría asociacional— atraviesan una cadena compartida de custodia, ejecución, comparación y atribución antes de clasificar el resultado y declarar la frontera causal." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 2</strong> — Cadena de recreación y control. Si una comprobación falla, la afirmación se detiene; una coincidencia aparente no reemplaza la evidencia que falta. Fuente: elaboración propia.</figcaption>
</figure>

La secuencia importa para política pública. Si cambia la definición de salida, la muestra o la precisión, un flujo administrativo puede parecer una caída del sistema. Si el modelo se ejecuta sin conservar la misma lista ordenada de valores, solo sé que pudo correr. El diagrama lo resume en una sola frontera: **reejecutable no significa recreable; recreable no significa coincidente; coincidente no significa correcto; correcto no significa causal**.
{: .text-justify}

### Donde me equivoqué en 2014

El caso más limpio está en el modelo jerárquico. El cuadro publica **0,003** para el rezago del SIMCE de matemáticas; la salida de Stata que produjo la tabla imprime **0,001**. Una reestimación da 0,000533 en Stata y Python, que redondea a 0,001. Siete explicaciones alternativas quedaron refutadas. No fue traducción ni precisión: fue transcripción.
{: .text-justify}

En la misma familia de modelos (Cuadro 6), dos filas rotuladas como varianzas (medidas de dispersión) eran los logaritmos de desviaciones estándar que Stata imprime, sin transformar y además cruzados en la tabla RTF original de 2014. El cuadro publicó 3,82 como "varianza del intercepto" y 2,791 como "varianza residual"; en realidad, la varianza entre comunas (intercepto aleatorio) es 265,6 y la varianza residual es 2.079,7.[^fn3] En otra celda, 0,4142 se convirtió en 1,4142.
{: .text-justify}

El modelo jerárquico del Gran Santiago (Cuadro 7, *N* = 14.704 observaciones en 2.640 establecimientos) tenía un problema distinto, no de copia sino de especificación: la varianza de su pendiente aleatoria colapsaba en el borde numérico (2,1 × 10⁻¹⁵), y tres covariables tomadas del corte transversal de 2006 no variaban en el tiempo dentro de cada colegio. Su variable explicada no es la proporción vulnerable del Cuadro 8, sino el logaritmo de la matrícula, ln(matrícula). Reestimé esa especificación por MCO agrupados con la descomposición de Mundlak y Chamberlain, que separa el promedio histórico de cada colegio de sus desviaciones anuales, y con errores estándar agrupados por RBD.[^mundlak1978][^chamberlain1982] El resultado reparte la asociación en dos partes que el modelo original fundía en un solo número. La asociación positiva con el SIMCE de matemáticas rezagado proviene de diferencias permanentes *entre* establecimientos ($$\hat{\beta}_{\text{entre}}$$ = 0,012131; *t* = 16,27); dentro de un mismo colegio, los cambios anuales del SIMCE no se asocian con cambios de matrícula ($$\hat{\beta}_{\text{dentro}}$$ = −0,000048; *t* = −0,53). En palabras simples: los colegios con mejor SIMCE histórico tienen más matrícula, pero un colegio que mejora su SIMCE un año no gana matrícula al siguiente de forma detectable. Para esta separación encabezo con la versión estática. La dinámica agrega como regresores la matrícula rezagada y su promedio por colegio; en un panel corto, ese promedio queda correlacionado por construcción con el término de error (el sesgo de Nickell), así que sus coeficientes van solo en la nota metodológica. A veces la arqueología encuentra un mecanismo estadístico de fondo; otras, un triste error al copiar y pegar.
{: .text-justify}

El índice de concentración produjo el error con mayor consecuencia interpretativa para la política pública. El Herfindahl-Hirschman (IHH, una medida de cuán concentrada está la oferta) va de 0 a 10.000 y usa 2.500 como umbral de alta concentración según las directrices de fusiones de EE. UU. de 2010 (las de 2023 lo bajaron a 1.800). Mi planilla guardó el índice por cien; el texto lo leyó como si estuviera por mil. Así, Santiago aparece con 1.534 cuando la escala correcta es aproximadamente 152.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" title="Figura 3 — Concentración y movilidad" aria-label="Abrir la Figura 3 ampliada">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" alt="A la izquierda, la figura publicada en 2014 con un índice de concentración entre 0 y 100. A la derecha, la recreación sobre la escala canónica de 0 a 10.000, con pendiente negativa y p igual a 0,084." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figura 3</strong> — Concentración y movilidad. El signo negativo sobrevive, pero la pendiente deja de distinguirse de cero al 5 % (p = 0,084; el valor p resume, bajo el modelo, cuán incompatibles son los datos con una pendiente nula). En el panel reconstruido con dato en ambos cortes, la escala publicada habría clasificado 318 de 337 comunas como altamente concentradas; la canónica clasifica 66. Fuente: Labra Olivares (2014), tesis de magíster (izquierda), y recreación propia de 2026 (derecha).</figcaption>
</figure>

En la hoja hhi2 de TESIS.xlsx, la planilla incluso dejó escrita la fórmula del umbral: "=C2>2,5". En su escala eso equivale a 250 puntos canónicos, no 2.500, y selecciona 330 de 346 comunas en 2006 y 326 en 2016 (mientras el panel reconstruido para las figuras cubre 318 de 337 comunas con dato en ambos cortes). Un filtro que aprueba al 95 % de los casos no está filtrando mucho.
{: .text-justify}

Otro resultado casi correcto escondía una definición distinta. El texto decía que ciudades intermedias y menores de 15.000 habitantes concentraban cerca del 80 % de la movilidad de seis regiones. La receta de la figura separaba capitales regionales del resto y daba 78,3 %. Aplicado literalmente, el umbral de población daba 11 %. El número estaba cerca; la frase describía otra partición.
{: .text-justify}

El hallazgo nuevo más sugerente no estaba cuantificado en la tesis. La razón alumnos por docente de los establecimientos que salen cae de 17,95 a 12,22 durante los siete años previos, frente a 20,31 en los establecimientos que permanecen en el registro. Para separar nivel y tendencia en el Cuadro 3, comparé municipales y particulares subvencionados entre 2004 y 2011 (59.808 observaciones = 36.493 municipales + 23.315 subvencionadas). En promedio, los establecimientos que después salen operaron con 5,90 alumnos por docente menos en el sector municipal y con 6,23 menos en el subvencionado. Su razón también cayó más rápido: 0,849 alumnos por docente al año frente a 0,632 entre los municipales que permanecen, y 0,565 frente a 0,417 entre los subvencionados. Esa diferencia adicional, de 0,216 y 0,148 por año, es descriptiva: no calculé errores estándar para la diferencia. La mayor parte de la caída la comparte todo el sistema; lo que distingue a quienes salen es, sobre todo, una escala menor visible retrospectivamente durante los siete años previos. La etiqueta es retrospectiva: marca toda la historia previa de un establecimiento que después desaparece.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" title="Figura 4 — La sombra de la muerte" aria-label="Abrir la Figura 4 ampliada">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" alt="Serie con intervalos de confianza de la razón alumnos por docente de establecimientos que salen: cae de 17,95 a 12,22 durante los siete años previos, frente a 20,31 entre incumbentes." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figura 4</strong> — La "sombra de la muerte": menos alumnos por docente durante los siete años anteriores a la salida. Es un patrón descriptivo condicionado por el problema del marcador temporal, no una estimación causal. Fuente: elaboración propia con la recreación de 2026 de los datos de la tesis (1992–2012).</figcaption>
</figure>

Esa figura es útil para política pública precisamente porque no promete lo que no observa. Un deterioro gradual abre preguntas sobre alertas tempranas, matrícula, dotación y respuesta institucional; no demuestra que una intervención específica evite el cierre ni que el cierre cause el deterioro.
{: .text-justify}

<aside class="notice--info" markdown="1">
**Nota metodológica — Cómo separé la diferencia entre colegios del cambio dentro de cada colegio (efectos aleatorios correlacionados de Mundlak y Chamberlain, CRE por su sigla en inglés):** Un modelo lineal mixto estándar supone que los rasgos permanentes no observados de cada escuela no se correlacionan con sus variables explicativas; cuando ese supuesto falla, mezcla en un solo número la diferencia *entre* escuelas distintas con el cambio *dentro* de una misma escuela a lo largo del tiempo. Para evitar esa mezcla en el Cuadro 7, incluí el promedio histórico de cada covariable variante en el tiempo por establecimiento ($$\bar{X}_i$$, descomposición de Mundlak 1978 y Chamberlain 1982) y agrupé los errores estándar por RBD.[^mundlak1978][^chamberlain1982] Así, el coeficiente de la desviación anual $$X_{it} - \bar{X}_i$$ aísla la variación *dentro* del colegio, mientras que el coeficiente de $$\bar{X}_i$$ captura la selección estructural *entre* establecimientos distintos. La parte *dentro* conserva dos límites: sigue expuesta a factores que cambian en el tiempo, y los años intermedios sin medición del SIMCE se imputaron por crecimiento anual antes de rezagar la serie. La especificación dinámica ($$\hat{\beta}_{\text{entre}}$$ = 0,000543, *t* = 7,26; $$\hat{\beta}_{\text{dentro}}$$ = 0,000174, *t* = 2,44) agrega el rezago de la matrícula y su media por escuela; en un panel con pocos años por colegio, esa media queda correlacionada por construcción con el error y sesga el coeficiente del rezago (sesgo de Nickell), por lo que encabezo con la versión estática y reporto la dinámica solo como contraste.
</aside>

## Cucharada 3: qué quedó listo para extender hasta 2025

**Esta era la prueba que necesitaba antes de sumar trece años: no que cada cifra de 2014 sobreviviera, sino saber exactamente qué estaba extendiendo.** Todo el código disponible volvió a ejecutarse, pero no siempre produjo el mismo resultado. Reejecutable quiere decir que el código termina; recreable, que vuelve a producir algo comparable; y coincidente, que supera el criterio fijado antes de mirar el resultado. Son afirmaciones distintas.
{: .text-justify}

{% include evidence-carousel.html %}

Al reabrir los nueve casos que la introducción dejó sin atribución clara con otra pregunta —si existía una base común para compararlos—, tres la tenían y coincidieron, dos la tenían y mantuvieron diferencias, y cuatro no la tenían. Esa segunda clasificación no cambia su veredicto editorial: la reejecución actual completó las rutas recuperables y reprodujo tablas y gráficos, pero no demuestra cuál fue la sesión efectiva de 2014. En el registro quedaron 50 hipótesis técnicas y 34 juicios editoriales: las primeras contrastan explicaciones; los segundos clasifican afirmaciones publicadas. Ninguno funciona como tasa de acierto del otro.
{: .text-justify}

Una comparación solo informa si ambas rutas responden la misma pregunta: muestra, definición, orden y precisión forman parte del resultado. Una cifra cercana puede ocultar una discrepancia real y dos cifras idénticas pueden heredar la misma definición errónea; importa qué evidencia distingue un acierto de una coincidencia.
{: .text-justify}

En los tres casos que coincidieron, las tablas o series conservaron una base común y superaron una regla fijada antes de compararlas. En los dos que mantuvieron diferencias, volver a ejecutar el análisis no borró la discrepancia: mostró con mayor precisión dónde empezaba. Herramientas distintas reprodujeron los resultados recuperables, lo que reduce la posibilidad de que el hallazgo dependa de un programa particular. Aun así, esa convergencia acredita el cálculo actual, no reconstruye por sí sola la ejecución histórica.
{: .text-justify}

Los cuatro casos restantes enseñan otra cosa. Cuando no sobrevive una lista común de valores, una serie o una salida suficientemente detallada, comparar solo el aspecto de dos figuras respondería una pregunta nueva. Declararlos no comparables es menos vistoso que anunciar una réplica, pero protege la interpretación. La ausencia de una prueba válida no convierte la publicación original en falsa ni la recreación en correcta; deja una deuda de evidencia que no corresponde llenar con confianza retrospectiva.
{: .text-justify}

Esta separación importa fuera de la tesis. Una administración podría usar una cifra recreada para describir un período histórico, formular una alerta o justificar una intervención. Esos usos exigen respaldos distintos. Un patrón descriptivo puede abrir una pregunta de monitoreo; una alerta necesita validación fuera de muestra y costos de error explícitos; una intervención requiere un contraste capaz de aproximar el contrafactual. Si se confunden esos usos, la capacidad predictiva o la trazabilidad técnica terminan prestando una autoridad causal que el diseño nunca obtuvo.
{: .text-justify}

La alerta de la tesis es el caso de prueba. En 2014 el modelo de duración en tiempo discreto (*cloglog* sobre 2007–2011, Cuadro 10: 30.484 observaciones colegio-año en 7.460 RBD y 237 cierres) solo se había evaluado dentro de la misma muestra. Ahora lo entrené con las transiciones de 2007–2008 (12.495 filas y 86 cierres) y lo evalué en 2009–2011 (17.989 filas y 151 cierres), años que no usó para estimarse. Ordena bien el riesgo: el 10 % de los registros colegio-año con mayor riesgo predicho concentra el 43,7 % de los cierres (66 de 151) y el 20 % concentra el 69,5 % (AUC = 0,8517; intervalo de referencia aproximado de Hanley-McNeil de 0,81–0,89 en este único corte temporal). Pero no acierta el nivel: predijo un riesgo medio de 0,60 % cuando el observado fue de 0,84 %, una brecha compatible con que la tasa de cierre subió entre el período de entrenamiento (86 de 12.495) y el de prueba (151 de 17.989). Su puntaje de Brier (0,008196) mejora apenas en 1,5 % el de asignar a todos la tasa observada (0,008324). Sirve para ordenar prioridades de monitoreo, no para leer probabilidades absolutas.
{: .text-justify}

<aside class="notice--info" markdown="1">
**Nota metodológica — Validación temporal fuera de muestra (Cuadro 10):** Evaluar un modelo de riesgo en los mismos años en que fue estimado suele exagerar su puntería, porque el algoritmo ya "conoce" qué escuelas cerraron. Por eso lo estimé con 2007–2008 y lo evalué en 2009–2011. Dos medidas responden preguntas distintas. El AUC mide si ordena bien: la probabilidad de que un registro que termina en cierre reciba más riesgo que uno que no; con 0,8517, acierta ese orden en cerca del 85 % de los pares. El puntaje de Brier (0,008196) mide el error cuadrático medio entre la probabilidad predicha y el cierre efectivo; frente a la tasa base de 0,84 % por colegio-año en 2009–2011, cualquier modelo queda cerca de cero, así que se compara con el de asignar a todos esa tasa (0,008324). La mejora relativa de 1,5 % es el puntaje de habilidad de Brier, y mide calibración y discriminación a la vez: un modelo puede ordenar bien y aun así ganar poco en Brier si subestima el nivel, como ocurre aquí. Las covariables se estandarizaron con medias de todo 2007–2011 y la estimación incluye una penalización *ridge*; ninguna de las dos usa los cierres de 2009–2011, pero la primera sí usa sus covariables, una fuga menor que conviene declarar. Focalizar diagnósticos en el 10 % o el 20 % de los registros colegio-año con mayor riesgo concentra entre dos quintas partes y siete décimas de las salidas reales, sin atribuirles causalidad.
</aside>

La extensión hasta 2025 no hereda cada variable ni cada interpretación, sino definiciones sostenibles y preguntas abiertas. En 1992–2012 el directorio agregado solo permitía contar salidas brutas de RBD (2.069) sin seguir a los alumnos. Desde 2004, los registros longitudinales permiten una **Regla de Cierre Escolar Inferido desde los Datos (RCID v1)** con tres niveles anidados. D0 reúne los cierres permanentes con matrícula previa: 1.981 entre 2005 y 2025. D1 descuenta las continuidades de directorio, los anexos y los reemplazos, y deja 1.807. D2 descuenta además las absorciones —cuando al menos el 70 % de los alumnos reasignados llega a un único receptor estable el año del cierre y el siguiente, con una concentración de destinos IHH ≥ 5.000 en la escala 0–10.000— y deja **1.678 cierres inferidos** en versión conservadora sobre la serie completa: 1.382 en 2005–2015 y 296 en 2016–2025. Si además se exige observar completo el año siguiente al cierre, quedan **1.648** (1.382 y 266 en 2016–2025): los 30 que se descuentan están todos en 2016–2025 y son cierres cuyo año siguiente no está observado completo. Las dos cifras no compiten: la primera cuenta la serie entera y la segunda solo los cierres cuyo destino ya puede verificarse. Es una inferencia empírica, no la certeza documental de una resolución o un acta de cierre.
{: .text-justify}

No hice esta arqueología para absolver o condenar mi trabajo de 2014. Antes de construir 2013–2025 necesitaba separar qué podía producir de nuevo, qué estaba mal, qué era una sensibilidad (un resultado alternativo bajo otra decisión) y qué no podía compararse.
{: .text-justify}

Lo importante no es reivindicar el original, sino llegar a la [parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) con una base 1992–2012 auditable, errores conocidos corregidos y límites visibles. Ahora sí tiene sentido añadir trece años: no para prolongar una serie, sino para averiguar qué cambió con las reglas y qué significa que un establecimiento entre o salga del registro.
{: .text-justify}

## Cierre: de replicar a extender

La tesis quedó organizada en cuatro grupos: resultados que sobreviven, errores de 2014, una versión de 2026 sin errores conocidos y casos sin comparación válida. Esa separación muestra qué conservar y qué no llevar a 1992–2025.
{: .text-justify}

Sobrevive la reasignación de 1992–2012: pérdida municipal y expansión subvencionada. También sobrevive, **solo para el universo reconstruido del Gran Santiago**, la mayor vulnerabilidad de quienes después salen del registro. No sobreviven la escala del IHH, la lectura de "menos de 15.000 habitantes", dos varianzas, varios rótulos ni una definición temporal clave. Las discrepancias de la ruta actual se corrigieron hasta dejar una salida canónica de 2026 sin errores conocidos; las alternativas siguen visibles como sensibilidades, no como recreación.
{: .text-justify}

{: .table-caption}
**Tabla 2.** Qué uso público resiste y dónde termina la evidencia

| Resultado | Uso público razonable | Lo que no autoriza |
|---|---|---|
| Reasignación entre dependencias, 1992–2012 | Diagnóstico histórico del cambio sectorial | Atribuirlo causalmente a una reforma |
| Vulnerabilidad en el Gran Santiago reconstruido | Preguntar por protección y continuidad educativa (separando brecha permanente entre escuelas de variación interna) | Generalizar a Chile o atribuir efectos del cierre |
| Razón alumnos/docente y peligro *cloglog* antes de la salida | Focalizar monitoreo preventivo (AUC fuera de muestra = 0,8517; 43,7 % de cierres en el decil superior de riesgo; ordena el riesgo, pero no calibra su nivel) | Presentarlos como regla automática de cierre o efecto causal |
| IHH corregido | Describir concentración en la escala correcta | Inferir el efecto de la competencia sobre cierres o movilidad |
{: .table--compact .table--scroll}

La segunda parte no podrá sumar trece filas y fingir continuidad. Un establecimiento de los ochenta, uno de los noventa, uno posterior a la SEP, uno bajo Inclusión y uno traspasado a un Servicio Local no enfrentan el mismo mercado ni el mismo Estado. Una serie puede estar impecablemente calculada y, aun así, responder otra pregunta. Esa es una falsa señal de éxito especialmente peligrosa en política pública.
{: .text-justify}

### De describir el cierre a identificar una política

La recreación deja un panel capaz de describir flujos, reconocer señales de riesgo y reestimar asociaciones. No observa por qué cerró cada establecimiento, qué habría ocurrido sin una reforma ni la trayectoria individual de sus alumnos. Agregar controles, efectos fijos, errores estándar más sofisticados o más capacidad de cálculo puede reducir algunos sesgos; **no crea el contrafactual que falta** (qué habría ocurrido sin la reforma o el cierre).
{: .text-justify}

La [parte II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) retoma estas tres preguntas sin tratarlas como intercambiables:
{: .text-justify}

{: .table-caption}
**Tabla 3.** Rutas causales y condiciones mínimas

<div class="causal-routes causal-routes--es" markdown="1">

| Ruta | Pregunta y diseño | Condición mínima para interpretarla |
|---|---|---|
| **Alerta descriptiva/predictiva** | Modelar transiciones entre activo, matrícula cero, receso, cierre oficial y ausencia del registro; estimar riesgo fuera de muestra (en años o casos no usados para ajustar el modelo). | Validación temporal, calibración (que el riesgo predicho se parezca a la frecuencia observada), umbrales de decisión y auditoría distributiva. Puede orientar monitoreo; no estima efectos. |
| **Reforma escalonada** | Evaluar cambios asociados al traspaso a Servicios Locales con diferencias en diferencias (comparar cambios entre grupos afectados y no afectados) y estudio de eventos por cohortes. | Fechas y exposición verificadas; tendencias paralelas (evolución previa semejante), anticipación, composición y derrames plausibles. Si el calendario respondió al riesgo, el diseño no es causal por decreto. |
| **Consecuencias del cierre** | Vincular trayectorias de estudiantes y comparar continuidad, distancia, asistencia, logro y abandono mediante estudio de eventos o diferencias en diferencias emparejadas. | Causa del cierre, controles realmente comparables y variación plausiblemente exógena (no determinada por el resultado); emparejar por sí solo no elimina la selección. |
{: .table--compact .table--scroll}

</div>

Hay, sin embargo, una pregunta anterior al diseño econométrico. En un sistema donde abren y cierran establecimientos, la llamada **"destrucción creativa"** (reemplazo de quienes salen por establecimientos nuevos) puede renovar la oferta, desplazar escuelas de menor desempeño o llevar estudiantes hacia alternativas mejores. Pero el balance no puede hacerse mirando solo qué establecimiento desaparece y cuál ocupa su lugar. En Chile existe también evidencia de costos del cierre sobre repitencia y abandono, y de efectos comunitarios que difícilmente caben en una cuenta de matrícula.[^grau2018][^nunez2014]
{: .text-justify}

Eso cambia la pregunta de política pública. No se trata de impedir cualquier cierre ni de conservar todo establecimiento. Se trata de saber **quién absorbe el costo de la transición**: quién debe cambiarse, adónde llega, cuánto más se desplaza, qué ocurre con su asistencia, aprendizaje y permanencia, y qué pierde la comunidad. Que existan cupos es necesario; no agota esos costos.
{: .text-justify}

La parte II precisa los eventos administrativos, examina comparaciones institucionales que no permiten atribuir efectos y deja pendiente el seguimiento individual; la [parte III]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/' | relative_url }}) lo aborda con trayectorias de estudiantes. Esa frontera importa porque una base más larga no reemplaza las trayectorias de estudiantes que la tesis de 2014 casi no podía observar.
{: .text-justify}

La pregunta que queda abierta no es contar nuevamente entradas y salidas, sino **¿cuándo la destrucción creativa renueva efectivamente la oferta educativa y cuándo solo desplaza sus costos hacia estudiantes, familias y territorios con menor capacidad para absorberlos?**
{: .text-justify}

Un RBD —el identificador oficial del establecimiento— puede desaparecer del registro. **La trayectoria de un estudiante no se reinicia cuando eso ocurre.**
{: .text-justify}

---

## Referencias

[^tesis]: Labra Olivares, Cristián A. *Patrones de entrada y salida de establecimientos educacionales en Chile (1992-2012)*, tesis de magíster, Universidad de Chile, 2014. Profesor guía: Daniel Hojman T.

[^fn3]: En la salida de Stata del Cuadro 6, los parámetros impresos corresponden a logaritmos de desviaciones estándar: la varianza entre comunas (intercepto aleatorio) es 265,6 —esto es, e^(2 * 2,791)— y la varianza residual es 2.079,7 —esto es, e^(2 * 3,82)—, que quedaron sin exponenciar y cruzadas en la tabla RTF original de 2014.

[^grau2018]: Grau, Nicolás; Hojman, Daniel; Labra, Cristián; Mizala, Alejandra. [Destructive Creation: School Turnover and Educational Attainment]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}), documento de trabajo SDT 396, Departamento de Economía, Universidad de Chile, 2014; Grau, Nicolás; Hojman, Daniel; Mizala, Alejandra. [School closure and educational attainment: Evidence from a market-based system](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf), *Economics of Education Review* 65, 1–17, 2018. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)

[^paredes2018]: Paredes, Ricardo D.; Fresard, Matías. Voucher y cierre de escuelas en Chile, *Estudios Públicos* 151, 7–27, 2018.

[^nunez2014]: Núñez, Carmen Gloria; Solís, Camila; Soto, Rodrigo. [¿Qué sucede en las comunidades cuando se cierra la escuela rural?](https://revistas.javeriana.edu.co/index.php/revPsycho/article/download/3602/8527), *Universitas Psychologica* 13(2), 615–625, 2014. [DOI](https://doi.org/10.11144/Javeriana.UPSY13-2.qscc) · [Scholar](https://scholar.google.com/scholar_lookup?title=%C2%BFQu%C3%A9+sucede+en+las+comunidades+cuando+se+cierra+la+escuela+rural%3F+Un+An%C3%A1lisis+Psicosocial+de+la+Pol%C3%ADtica+de+Cierre+de+las+Escuelas+Rurales+en+Chile&doi=10.11144%2FJaveriana.UPSY13-2.qscc)

[^regimenes]: Biblioteca del Congreso Nacional de Chile. [Historia del Decreto Ley N.º 3.063](https://www.bcn.cl/historiadelaley/historia-de-la-ley/vista-expandida/8363/); [Ley N.º 19.247](https://www.bcn.cl/leychile/navegar?idNorma=127911); [Ley N.º 20.248](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=269001&idVersion=); [Ley N.º 20.845](https://www.bcn.cl/leychile/Navegar?idNorma=1078172&idParte=9605200&idVersion=2222-02-02); [Ley N.º 21.040](https://www.bcn.cl/leychile/Navegar?idNorma=1111237&idParte=9853075).

[^christensen2018]: Christensen, Garret; Miguel, Edward. [Transparency, Reproducibility, and the Credibility of Economics Research](https://doi.org/10.1257/jel.20171350), *Journal of Economic Literature* 56(3), 920–980, 2018. [Scholar](https://scholar.google.com/scholar_lookup?title=Transparency%2C+Reproducibility%2C+and+the+Credibility+of+Economics+Research&doi=10.1257%2Fjel.20171350)

[^clemens2015]: Clemens, Michael A. [The Meaning of Failed Replications: A Review and Proposal](https://doi.org/10.1111/joes.12139), *Journal of Economic Surveys* 31(1), 326–342, 2017 (en línea en 2015). [Scholar](https://scholar.google.com/scholar_lookup?title=THE+MEANING+OF+FAILED+REPLICATIONS%3A+A+REVIEW+AND+PROPOSAL&doi=10.1111%2Fjoes.12139)

[^herndon2013]: Herndon, Thomas; Ash, Michael; Pollin, Robert. [Does high public debt consistently stifle economic growth?](https://doi.org/10.1093/cje/bet075), *Cambridge Journal of Economics* 38(2), 257–279, 2014 (en línea en 2013). [Scholar](https://scholar.google.com/scholar_lookup?title=Does+high+public+debt+consistently+stifle+economic+growth%3F+A+critique+of+Reinhart+and+Rogoff&doi=10.1093%2Fcje%2Fbet075)

[^hamermesh2007]: Hamermesh, Daniel S. [Viewpoint: Replication in economics](https://doi.org/10.1111/j.1365-2966.2007.00428.x), *Canadian Journal of Economics* 40(3), 715–733, 2007. [Scholar](https://scholar.google.com/scholar_lookup?title=Viewpoint%3A+Replication+in+economics&doi=10.1111%2Fj.1365-2966.2007.00428.x)

[^mundlak1978]: Mundlak, Yair. [On the Pooling of Time Series and Cross Section Data](https://doi.org/10.2307/1913646), *Econometrica* 46(1), 69–85, 1978. [Scholar](https://scholar.google.com/scholar_lookup?title=On+the+Pooling+of+Time+Series+and+Cross+Section+Data&doi=10.2307%2F1913646)

[^chamberlain1982]: Chamberlain, Gary. [Multivariate Regression Models for Panel Data](https://doi.org/10.1016/0304-4076(82)90094-X), *Journal of Econometrics* 18(1), 5–46, 1982. [Scholar](https://scholar.google.com/scholar_lookup?title=Multivariate+regression+models+for+panel+data&doi=10.1016%2F0304-4076%2882%2990094-X)
