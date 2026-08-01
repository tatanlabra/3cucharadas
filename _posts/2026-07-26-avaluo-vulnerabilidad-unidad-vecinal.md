---
layout: single
title: "Avalúo y vulnerabilidad en 3 cucharadas: cambie el denominador, cambie el mapa"
subtitle: "Qué ocurre al repartir el avalúo fiscal de 9,4 millones de predios entre unidades vecinales y cambiar la unidad de comparación"
date: 2026-07-26 19:20:00 -0400
categories: [datos, python, territorio]
tags: [catastro-sii, igvust, unidad-vecinal, desigualdad, gini, theil, duckdb, geoespacial, datos-abiertos]
description: "Cruce descriptivo entre avalúo fiscal SII e IGVUST por unidad vecinal. El resultado central no es una paradoja social: es la sensibilidad al denominador, al universo RSH, a la geometría y a la escala territorial."
excerpt: "El catastro registra predios, no personas. Cambiar el denominador cambia el mapa; omitirlo cambia la historia."
author: clabra
lang: es
ref: avaluo-vulnerabilidad-uv
permalink: /datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/
header:
  teaser: /assets/images/teasers/teaser-avaluo-vulnerabilidad.webp
  og_image: /assets/images/avaluo-vulnerabilidad-unidad-vecinal/og-avaluo-vulnerabilidad-1200x630.webp
math: true
distribution:
  social: true
  republish: []
toc: true
toc_sticky: true
comments: true
author_profile: true
classes: [avaluo-vulnerabilidad-post]
---

<figure class="align-center">
  <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/hero-avaluo-vulnerabilidad-1600x900.webp' | relative_url }}" alt="Un mismo avalúo fiscal de 9,4 millones de predios se divide por hogares, personas y metros cuadrados, y produce tres lecturas territoriales distintas; junto a las cifras 19,9% de unidades vecinales que conservan cuartil y 45,8% que se desplazan dos o más." width="1600" height="900" loading="eager" decoding="async">
  <figcaption>Apertura conceptual del argumento. Las cifras —9,4 millones de predios únicos, 19,9% que conserva cuartil, 45,8% que se desplaza dos o más— son las del procesamiento y se detallan más abajo. Los tres paneles ilustran la idea de que el patrón cambia con el denominador; no son un resultado del cruce.</figcaption>
</figure>

Chile mantiene un catastro capaz de seguir millones de predios y, aun así, suele reducir toda la conversación a una cuota trimestral. El dato no nació del entusiasmo estatal por dibujar polígonos: existe porque el impuesto territorial necesita saber **qué hay, dónde está, para qué se usa y cuánto vale fiscalmente**.
{: .text-justify}

Un avalúo fiscal no es sólo una cifra en el recibo de contribuciones. Es la vara administrativa con que el Estado mide el valor de la propiedad, y esa vara importa: parte de la desigualdad urbana se juega en el valor del suelo, en quién capitaliza la plusvalía y en quién queda fuera de ella ([Sabatini, Cáceres y Cerda, 2001](https://doi.org/10.4067/S0250-71612001008200002); [López-Morales, Sanhueza, Espinoza y Órdenes, 2019](https://doi.org/10.4067/S0250-71612019000300113)).
{: .text-justify}

Este post cruza ese número administrativo —el avalúo fiscal del SII— con un índice oficial de vulnerabilidad territorial, unidad vecinal por unidad vecinal. El resultado no es una revelación dramática. Depende de decisiones que casi nunca llegan al titular: **qué se suma, entre qué se divide, sobre qué territorio se agrega y qué casos quedan fuera**. Aquí quedan escritas antes de mirar el mapa.
{: .text-justify}

La pregunta cabe en una fracción mínima:
{: .text-justify}

$$
\text{indicador territorial}
=
\frac{\text{total que se quiere describir}}
{\text{unidad con que se lo compara}}
$$

Sumar el avalúo de una unidad vecinal responde cuánto valor administrativo fue asignado allí. Dividir ese mismo total por hogares, personas o metros cuadrados responde preguntas distintas. Ninguna es «la correcta» por naturaleza; el error aparece cuando una se presenta con el nombre de otra. La aritmética suele ser inocente. El relato, no siempre.
{: .text-justify}

## Contrato de lectura

Cruzo dos registros administrativos chilenos: el catastro de bienes raíces del Servicio de Impuestos Internos (SII) y el Índice Global de Vulnerabilidad Socioterritorial (IGVUST) del Ministerio de Desarrollo Social y Familia. La unidad de análisis es la **unidad vecinal (UV)**, no el predio, el hogar ni la persona.
{: .text-justify}

| Concepto | Qué significa aquí | Qué no significa |
|---|---|---|
| **Catastro SII** | Registro administrativo de bienes raíces y sus características. | Censo de población ni registro de residentes. |
| **Predio** | Unidad catastral identificada por comuna, manzana y número predial. | Vivienda, hogar, propietario o persona. |
| **Avalúo fiscal** | Valoración administrativa usada como base del impuesto territorial. | Precio de compraventa, ingreso o riqueza de residentes. |
| **IGVUST** | Ordenamiento de unidades vecinales según vulnerabilidad socioterritorial. | Diagnóstico individual ni mecanismo causal. |
| **RSH** | Fuente de hogares y personas usados como denominadores. En este procesamiento suma 15.978.644 personas, cerca de 85% de la población del país. | Censo completo ni universo homogéneo por comuna. |
| **Unidad vecinal** | Territorio definido para organización y participación vecinal. | Malla exhaustiva que cubra todo Chile predio por predio. |
| **Denominador** | Magnitud por la que se divide el avalúo asignado. | Letra chica posterior: define la pregunta. |

El RSH importa porque es la fuente de hogares y personas que uso como denominador. A escala nacional es amplio —cerca de 85% de la población—, pero no cubre todas las comunas por igual. En comunas con baja presencia relativa en RSH, como puede ocurrir en Vitacura, un indicador "por hogar RSH" puede inflarse por un denominador angosto, no por más avalúo real. El visor SIVUST, aún no público, trata esa misma comparación con igual cautela.
{: .text-justify}

El avalúo fiscal tampoco es precio de mercado: el SII lo construye a partir de las características del bien y su área homogénea, no de una transacción real. Puede ser una señal territorial útil si conserva su apellido, **fiscal** — la teoría de precios hedónicos de [Rosen (1974)](https://doi.org/10.1086/260169) explica por qué el entorno pesa en la valoración de un bien diferenciado como una vivienda, pero este post no observa transacciones ni patrimonio de los hogares.
{: .text-justify}

**Corte de datos:** 19 de julio de 2026. **Fecha editorial:** 26 de julio de 2026. Todas las relaciones son descriptivas y dependen de la malla UV utilizada.
{: .small}

## Pregunta

Agregué el avalúo fiscal de predios SII a escala UV y lo comparé con el orden nacional de vulnerabilidad del IGVUST, manteniendo fijo el numerador y cambiando la lente:
{: .text-justify}

| Medida | Pregunta que responde |
|---|---|
| Avalúo total | ¿Cuánto avalúo fiscal fue asignado a esta UV? |
| Avalúo por hogar RSH | ¿Cuánto avalúo asignado corresponde por hogar registrado en la UV? |
| Avalúo por persona RSH | ¿Cuánto corresponde por persona registrada? |
| Avalúo por m² predial | ¿Cuánto avalúo corresponde por superficie predial asignada? |

<figure class="align-center">
  <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/figures/numerador-tres-denominadores-1200x900.webp' | relative_url }}" alt="Un mismo avalúo fiscal total se divide por hogares, personas y metros cuadrados, produciendo tres patrones territoriales distintos." width="1200" height="900" loading="lazy" decoding="async">
  <figcaption><strong>Figura 1</strong> — Un numerador, tres historias. El total asignado no cambia; cambia la pregunta que se le hace. Esquema conceptual, no un resultado del procesamiento. Elaboración propia.</figcaption>
</figure>

La respuesta corta: por hogar y por persona casi no hay relación con vulnerabilidad. Por metro cuadrado aparece una relación nacional fuerte, pero se diluye al mirar sólo UV mayoritariamente urbanas. No es una paradoja glamorosa entre riqueza y vulnerabilidad. Es más sobrio, y por eso más útil: **el denominador, el universo y la escala forman parte del resultado**.
{: .text-justify}

Una advertencia antes de seguir: nada de esto dice cuánto gana quien vive ahí, cuánto vale su casa en el mercado ni quién es su dueño. Convertir una asociación territorial en una afirmación sobre personas es exactamente la inferencia ecológica que [Robinson (1950)](https://doi.org/10.2307/2087176) advirtió hace más de setenta años.
{: .text-justify}

## Antes de las cucharadas: por qué se grava lo que no se mueve

El impuesto territorial tiene una lógica menos exótica que su reputación pública. La propiedad es una base visible, inmóvil y vinculada al territorio donde se prestan servicios. En Chile, las contribuciones son de beneficio municipal: una parte queda en la comuna de origen y otra alimenta el Fondo Común Municipal, que redistribuye recursos para alumbrado, áreas verdes, infraestructura y programas sociales ([SII, *Impuesto Territorial*](https://www.sii.cl/destacados/impuesto_territorial/index.html)). Sin catastro, avalúos y localización predial, esa arquitectura simplemente no funciona.
{: .text-justify}

Tampoco es una rareza chilena. El impuesto recurrente sobre bienes inmuebles ocupa un lugar relevante en las finanzas locales de numerosos países. La comparación reunida por el Banco Mundial muestra recaudaciones cercanas a 2%–3% del PIB en Estados Unidos, Canadá y Reino Unido, y participaciones importantes en los ingresos locales. No son copias del sistema chileno, pero comparten la misma intuición: parte del valor que se acumula en el territorio ayuda a financiar el territorio ([Banco Mundial, 2020](https://openknowledge.worldbank.org/handle/10986/34793)).
{: .text-justify}

La evidencia comparada no dice que cualquier impuesto a la propiedad sea justo por definición. Dice algo más incómodo: **el diseño manda**. La OCDE y el FMI destacan su base poco móvil, su potencial recaudatorio y su vínculo con los servicios locales, pero recomiendan avalúos actualizados, tasas moderadas y alivios focalizados o diferidos para propietarios con baja liquidez. El propio FMI usa el *Council Tax* británico como ejemplo de cómo bandas demasiado comprimidas pueden producir un resultado regresivo ([OCDE, 2022](https://doi.org/10.1787/03dfe007-en); [FMI, 2024](https://doi.org/10.5089/9798400288753.061)). El instrumento no trae progresividad de fábrica.
{: .text-justify}

Hay, por supuesto, una vía más vistosa: borrar una línea del recibo y reconstruir el costo en otra planilla. La suma puede cerrar; la distribución no necesariamente. Cuando una exención deja de mirar ingresos o valor y la compensación reproduce la recaudación previa, el impuesto no desaparece: cambia de bolsillo, de fondo o de código postal. La contabilidad conserva la calma. El territorio quizá no.
{: .text-justify}

Con esa perspectiva, el catastro deja de ser una colección de roles y pasa a ser lo que realmente es: la infraestructura que permite medir la base, repartirla y discutir quién se beneficia de cada regla. Ahora sí, las tres cucharadas.
{: .text-justify}

## Cucharada 1: construir el numerador sin cerrar la fuga

El corte original trae **10.343.893 registros**. Registro no equivale a predio único; las bases administrativas también tienen eco. Después de deduplicar la clave catastral —comuna, manzana y número predial— quedan **9.401.277 predios**. El objetivo es repartir su avalúo sobre **6.891 UV** antes de probar denominadores.
{: .text-justify}

Predios y UV son polígonos, pero sus límites no coinciden. Un predio puede caer entero en una UV, cruzar varias o no tocar ninguna. Uso prorrateo por área de intersección, una forma de interpolación areal ([Goodchild, Anselin & Deichmann, 1993](https://doi.org/10.1068/a250383)):
{: .text-justify}

$$
f_{p,u} = \frac{\text{área}(p \cap u)}{\text{área}(p)}
\qquad
A_u = \sum_{p} a_p \cdot f_{p,u}
$$

donde $$a_p$$ es el avalúo fiscal del predio y $$A_u$$ el total asignado a la unidad vecinal. Si queda entero dentro de una UV, aporta todo; si cruza el límite a medias, aporta la mitad.
{: .text-justify}

Dos decisiones metodológicas importan.
{: .text-justify}

**Uso área geométrica para prorratear.** Entre los predios únicos, 10,7% no tiene superficie declarada utilizable y 2,8% no tiene geometría. La superficie declarada puede servir para auditoría o sensibilidad, pero no basta para ubicar espacialmente un predio sin polígono. Por eso no imputo asignación UV sólo con metros cuadrados reportados. Si más adelante se implementa un fallback, debe entrar primero al pipeline analítico con regla de localización explícita y después al post y al visor. El mapa bonito no es licencia para inventar geometría.
{: .text-justify}

**No renormalizo.** Si $$\sum_u f_{p,u} < 1$$, una parte del predio quedó fuera de toda UV. Redistribuir ese resto entre las UV que sí tocó produciría una suma perfecta —muy cómoda para la lámina— y una medición peor: escondería que la UV no fue diseñada para teselar Chile.
{: .text-justify}

El residuo es concreto: **271.150 predios**, **2,884%** de los deduplicados, no quedaron en ninguna UV. La fuga mediana comunal es **0,644%**, pero no es homogénea. En Antofagasta, 2.325 predios fuera de UV concentran **32,6%** del avalúo fiscal comunal; en Tortel, Timaukel, San Gregorio, Laguna Blanca y Río Verde la fuga llega a 100%, porque las UV cubren el poblado y los predios catastrados quedan fuera de esa malla.
{: .text-justify}

Ese sesgo se declara, no se barre debajo de la alfombra. En comunas con muchos predios sin polígono o mucha fuga fuera de UV, el cruce UV subrepresenta parte del catastro. La lectura pública debe mirar esos indicadores antes de interpretar colores.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline.webp' | relative_url }}" title="Figura 2 — Del registro original al universo espacial" aria-label="Abrir la Figura 2 ampliada">
    <picture>
      <source srcset="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline.svg' | relative_url }}" type="image/svg+xml">
      <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline.webp' | relative_url }}" alt="Diagrama de flujo: 10.343.893 registros originales se separan en 942.616 duplicados y 9.401.277 predios únicos; de estos últimos, 9.130.127 tocan al menos una unidad vecinal y 271.150 no tocan ninguna." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 2</strong> — Del registro original al universo espacial. «Toca al menos una UV» no significa asignación completa: un predio puede intersectar una UV y conservar parte de su superficie fuera de la malla. Fuente: elaboración propia, corte 19/07/2026. Haz clic para ampliar.</figcaption>
</figure>

## Antes del IGVUST: tamaño del avalúo observado

Antes de cruzar vulnerabilidad conviene saber de qué magnitud hablamos. En las 346 comunas, el avalúo fiscal asignado suma **587,4 billones de pesos**. La Región Metropolitana concentra **286,7 billones** (**48,8%**); Valparaíso, **56,2 billones** (**9,6%**); Biobío, **39,4 billones** (**6,7%**). La concentración no es un detalle: define el tamaño del numerador que luego se divide.
{: .text-justify}

Por comuna, las mayores sumas asignadas son Las Condes (**38,2 billones**), Santiago (**27,1**), Providencia (**16,3**), Lo Barnechea (**16,0**) y Vitacura (**15,2**). Antofagasta también aparece arriba (**15,1 billones**), pero con una fuga UV comunal muy alta; ese es precisamente el tipo de caso donde el total, el denominador y el universo deben leerse juntos.
{: .text-justify}

El visor incorpora esta lectura pura en la pestaña **Avalúos** de su laboratorio de denominadores. Primero el numerador; después la historia.
{: .text-justify}

{: .table-caption}
**Tabla 1** — Avalúo fiscal asignado antes de normalizar

| Nivel | Territorio | Avalúo asignado (billones CLP) | Participación nacional |
|---|---|---:|---:|
| Región | Metropolitana | 286,7 | 48,8% |
| Región | Valparaíso | 56,2 | 9,6% |
| Región | Biobío | 39,4 | 6,7% |
| Región | La Araucanía | 28,2 | 4,8% |
| Región | Maule | 26,4 | 4,5% |
| Comuna | Las Condes | 38,2 | 6,5% |
| Comuna | Santiago | 27,1 | 4,6% |
| Comuna | Providencia | 16,3 | 2,8% |
| Comuna | Lo Barnechea | 16,0 | 2,7% |
| Comuna | Vitacura | 15,2 | 2,6% |

Participación calculada sobre el total nacional asignado de 587,4 billones. Los montos de La Araucanía y Maule se derivan de esa participación publicada, no de una cifra medida aparte. En comunas con fuga UV o baja cobertura relativa del denominador RSH, este tamaño no debe confundirse con una lectura completa del territorio ni de sus residentes.
{: .small}

Las cinco comunas de la tabla suman **112,8 billones**: **19,2% de toda la base asignada del país** en cinco de 346 comunas, todas del sector oriente de Santiago. Esa es la concentración que después queda escondida cuando se divide por hogares o por metros cuadrados.
{: .text-justify}

## Cucharada 2: cuartiles, bivariado y denominadores

El IGVUST ordena unidades vecinales según vulnerabilidad socioterritorial. Mantengo sus cuatro cuartiles oficiales porque son el contrato analítico de esa fuente. En el eje de avalúo por m², cada UV se compara contra la mediana de su propia región, no contra un corte nacional fijo: queda bajo o sobre esa mediana regional. El resultado es una matriz 4×2 —cuatro filas IGVUST por dos columnas de avalúo— que evita dos problemas a la vez: una partición más fina volvería el bivariado difícil de leer y, en regiones con pocas UV como Arica y Parinacota, sugeriría una precisión que los datos agregados no entregan; y un corte nacional fijo ignoraría que el nivel de avalúo típico difiere mucho entre regiones. Un cuartil indica orden relativo, no distancia.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/figures/bivariado-clasificacion-4x2-1200x1623.webp' | relative_url }}" alt="Matriz de cuatro filas por dos columnas: las filas son los cuartiles nacionales de vulnerabilidad IGVUST, desde q1 como mayor vulnerabilidad hasta q4 como menor; las columnas separan avalúo fiscal por metro cuadrado bajo y alto." width="1200" height="1623" loading="lazy" decoding="async">
  <figcaption><strong>Figura 3</strong> — La clasificación 4×2, sin colores todavía. Cuatro filas de cuartil IGVUST por dos columnas de avalúo por m². Cada celda nombra la combinación que le corresponde por definición; no informa cuántas UV caen en ella ni qué tan frecuente es. En el visor, la columna separa por la mediana de la propia región, no por un corte nacional. Elaboración propia.</figcaption>
</figure>

En el mapa bivariado la lectura principal usa **avalúo por m² predial**. Es la señal más clara para poner atención donde alto avalúo unitario coincide con alta vulnerabilidad territorial. En la paleta, esas celdas quedan más oscuras, con una capa transparente para no tapar el fondo ni convertir el mapa en alarma cromática. Lo contraintuitivo debe llamar la atención; lo evidente no necesita megáfono. El indicador sigue siendo descriptivo y nacional; al restringir a UV con $$p_\text{urbano} > 50$$ la asociación por m² se atenúa fuertemente.
{: .text-justify}

En el visor, este cruce vive en un mapa analítico: sólo UV, selector gráfico de Chile, hover con datos de la unidad vecinal y leyenda 4×2. Un único buscador de región y comuna manda sobre todo el recorrido, y la selección que fijes ahí se mantiene en fichas, tablas y en el ranking territorial cuando corresponde. La inspección de geometría predial queda deliberadamente aparte, como anexo documentado al final: mezclarla con la clasificación bivariada invita a leer un borde catastral como si fuera un resultado.
{: .text-justify}

### 1. Por hogar, la celda llamativa es una pista

Si se divide por hogares RSH, el cuartil de mayor vulnerabilidad (`q1` IGVUST) contiene 530 UV en el cuartil más alto de avalúo por hogar. Ese número puede parecer una contradicción social. Todavía no lo es.
{: .text-justify}

{: .table-caption}
**Tabla 2** — Unidades vecinales por cuartil nacional de vulnerabilidad y avalúo por hogar

| Cuartil IGVUST | Avalúo/hogar q1 | q2 | q3 | q4 |
|---|---:|---:|---:|---:|
| q1 · mayor vulnerabilidad | 399 | 344 | 446 | **530** |
| q2 | 564 | 451 | 385 | 321 |
| q3 | 467 | 509 | 429 | 316 |
| q4 · menor vulnerabilidad | 293 | 419 | 463 | 546 |

La palabra correcta es **pista**, no conclusión. La razón combina avalúo territorial con hogares RSH. Si el denominador es bajo o el territorio es grande, el cociente sube sin que eso demuestre mayor riqueza de quienes viven allí.
{: .text-justify}

### 2. El cuadrante llamativo tiene menos hogares y mucha más superficie

Las UV vulnerables con mayor avalúo por hogar tienen mediana de **120,5 hogares** y **78,2 km²**. Las vulnerables con menor avalúo por hogar tienen **265 hogares** y **3,36 km²**. La razón crece porque el denominador se achica y el territorio se agranda. La planilla hace su trabajo; la interpretación tiene que hacer el suyo.
{: .text-justify}

{: .table-caption}
**Tabla 3** — Mecanismo del cuartil más vulnerable (`q1` IGVUST)

| Avalúo/hogar | UV | Hogares mediana | Superficie mediana (km²) | Avalúo/hogar mediano (millones CLP) |
|---|---:|---:|---:|---:|
| q1 | 399 | 265,0 | 3,36 | 10,2 |
| q2 | 344 | 368,5 | 15,21 | 26,2 |
| q3 | 446 | 274,5 | 45,59 | 57,6 |
| q4 | 530 | 120,5 | 78,22 | 185,6 |

La tabla no invalida el cruce. Delimita qué mide: avalúo fiscal asignado a una UV dividido por hogares RSH, no bienestar de sus residentes.
{: .text-justify}

### 3. La asociación cambia con la normalización

La siguiente tabla usa dos resúmenes entre -1 y +1. **Pearson** resume una relación lineal sobre logaritmo del avalúo positivo; **Spearman** resume si el orden de las UV cambia de manera monotónica. Cerca de cero hay poca relación lineal o monotónica. Ninguna columna estima un efecto causal.
{: .text-justify}

{: .table-caption}
**Tabla 4** — Sensibilidad de la asociación al denominador

| Medida de avalúo | Pearson | Spearman | UV |
|---|---:|---:|---:|
| Total asignado | -0,371 | -0,382 | 6.857 |
| Por hogar RSH | -0,061 | -0,047 | 6.849 |
| Por persona RSH | -0,079 | -0,072 | 6.849 |
| Por m² predial asignado | -0,582 | -0,575 | 6.851 |
| Por m², sólo UV mayoritariamente urbanas | +0,079 | +0,081 | 3.221 |

Por hogar y por persona, la asociación es casi nula. Por m², el patrón nacional parece fuerte. Al restringir a UV predominantemente urbanas cambia a aproximadamente +0,08. La lectura prudente es que el resultado nacional por m² contiene mucho contraste urbano-rural; no que se haya identificado un mecanismo de barrio.
{: .text-justify}

Los violines de la Figura 4 muestran la distribución completa. Su ancho indica dónde se concentran más UV; las líneas internas muestran mediana y rango intercuartílico. Son densidades suavizadas, no siluetas literales del territorio.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores.webp' | relative_url }}" title="Figura 4 — Sensibilidad al denominador y al universo" aria-label="Abrir la Figura 4 ampliada">
    <picture>
      <source srcset="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores.svg' | relative_url }}" type="image/svg+xml">
      <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores.webp' | relative_url }}" alt="Tres gráficos de violín comparan las distribuciones de avalúo por hogar, avalúo por metro cuadrado nacional y avalúo por metro cuadrado en unidades vecinales mayoritariamente urbanas, para los cuatro cuartiles nacionales de vulnerabilidad." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 4</strong> — El mismo avalúo produce distribuciones distintas al cambiar el denominador y el universo. Los violines muestran densidades estimadas; su forma depende del ancho de banda y no prueba grupos naturales ni causalidad. Las líneas internas resumen mediana y rango intercuartílico. Fuente: elaboración propia, corte 19/07/2026. Haz clic para ampliar.</figcaption>
</figure>

### 4. Lo robusto es la sensibilidad

Entre las **6.843 UV** con cuartil disponible tanto por hogar como por m², sólo **1.362 (19,9%)** permanecen en el mismo cuartil y **3.132 (45,8%)** se desplazan dos o más. No cambiaron los predios. Cambió la pregunta.
{: .text-justify}

## Cucharada 3: escala y concentración

Entre las **6.857 UV con avalúo asignado positivo**, el Gini es **0,7265**. Describe una base tributaria territorial muy concentrada; no es un Gini de ingresos ni de patrimonio de personas.
{: .text-justify}

Este dato importa fuera del ejercicio estadístico. En una base tan concentrada, cualquier exención también redistribuye: no sólo decide quién deja de pagar, sino qué comuna, fondo o impuesto deberá reconstruir el monto. El beneficio cabe en una línea; la incidencia completa suele necesitar otra planilla.
{: .text-justify}

El Gini resume concentración, pero no separa cuánto ocurre dentro y entre grupos. Para eso sirve el índice de **Theil**, que sí se descompone. Con $$x_i$$ como avalúo asignado a la UV $$i$$, $$\mu$$ como su media y $$w_g$$ como la participación del grupo $$g$$ en el avalúo total:
{: .text-justify}

$$
T = \frac{1}{n}\sum_{i=1}^{n} \frac{x_i}{\mu} \ln\!\left(\frac{x_i}{\mu}\right)
= \underbrace{\sum_{g} w_g T_g}_{\text{intra}} + \underbrace{\sum_{g} w_g \ln\!\left(\frac{\mu_g}{\mu}\right)}_{\text{entre}}
$$

Agrupando por región, $$T = 1{,}2042$$ y 81,0% queda dentro de las regiones. Al reagrupar por comuna, la parte entre-grupos llega a 56,9%. La comuna no "revela" segregación por arte de magia: al refinar una partición, parte de la desigualdad se desplaza desde el componente intra al componente entre por construcción ([Shorrocks, 1984](https://doi.org/10.2307/1913511)).
{: .text-justify}

Ese es el problema de la unidad areal modificable, o MAUP ([Fotheringham & Wong, 1991](https://doi.org/10.1068/a231025)). Los mismos predios pueden producir estadísticas distintas si se agrupan en regiones, comunas o UV. La escala no adorna el resultado: lo define. Por eso importa qué es la UV antes de usarla como contenedor: si la unidad no corresponde a un territorio con sentido propio, la estadística que produce hereda ese desajuste.
{: .text-justify}

Segundo freno: los cuartiles IGVUST ordenan UV, no personas. El cuartil de mayor vulnerabilidad reúne 25% de las unidades, pero **2.032.893 de 15.978.644 personas RSH (12,7%)**. Una coropleta puede sobrerrepresentar territorio rural disperso aunque sus colores estén perfectamente calculados.
{: .text-justify}

Tercer freno: la literatura de *assessment ratio* muestra que la valoración fiscal puede apartarse sistemáticamente de valores de mercado y que el patrón depende del contexto institucional. [Hodge, McMillen, Sands y Skidmore (2017)](https://doi.org/10.1111/1540-6229.12126) estudian ese problema en otro mercado; no prueban que el SII tenga el mismo sesgo. Lo que sí evidencian es que usar avalúo fiscal como sinónimo de precio de mercado requiere de factores de ajuste importantes, pese a eso, los gradientes o tendencias territoriales no deberían distar tanto.
{: .text-justify}

## Cierre: las brechas también pagan contribuciones

El mapa no dicta una política tributaria. Sí impide fingir que la base es homogénea, que todas las comunas parten del mismo lugar o que una exención carece de geografía. El cruce identifica cinco brechas que deben cerrarse antes de usar sus colores como evidencia fuerte.
{: .text-justify}

**Brecha 1: universo del denominador.** El RSH cubre cerca de 85% de la población del país, pero no con igual intensidad comunal. Cualquier indicador por hogar o persona RSH debe declarar esa cobertura y, cuando corresponda, contrastarla con datos censales. Ese contraste es justamente con lo que abre el visor: antes de cualquier cruce, mide qué fracción de las viviendas particulares del Censo 2024 alcanza el registro residencial del SII, comuna por comuna. Es la misma advertencia de este post en su forma más simple — declarar el universo antes de dividir por él.
{: .text-justify}

**Brecha 2: geometría y superficie.** El prorrateo requiere polígonos. La superficie declarada no reemplaza una geometría faltante sin una regla espacial adicional. Comunas con muchos predios sin polígono necesitan una alerta antes de interpretar su color.
{: .text-justify}

**Brecha 3: fuga fuera de UV.** La UV no cubre todo el territorio catastral. Si una comuna concentra mucho avalúo fuera de UV, el cruce describe un subconjunto, no su total comunal. Las UVs requieren de trabajo local para ajustarse mejor a la realidad.
{: .text-justify}

**Brecha 4: urbano-rural.** El avalúo por m² tiene una señal nacional fuerte, pero cambia al restringir el universo a UV urbanas. El indicador requiere un filtro de universo, no sólo una paleta intensa.
{: .text-justify}

**Brecha 5: escala.** Región, comuna y UV no son versiones ampliadas de la misma pregunta. Cambiar la unidad territorial cambia la estadística.
{: .text-justify}

Estas brechas tampoco son una defensa automática de cada avalúo, tasa o cobro vigente. Aliviar a una persona con poca liquidez y una vivienda valorizada es un problema real. La evidencia comparada ofrece instrumentos más precisos: rebajas según ingreso, topes de carga, diferimientos hasta la venta o herencia y reavalúos transparentes. No hace falta pedirle al catastro que finja que el activo dejó de existir.
{: .text-justify}

Se puede, desde luego, retirar la obligación de una columna y reponerla con transferencias desde otra. El alivio queda visible; su financiamiento se muda. Antes de celebrar que la cuenta desapareció, conviene revisar la segunda planilla y preguntar qué territorios terminan pagando la "cortesía".
{: .text-justify}

El visor permite explorar estas brechas de lo general a lo particular: el país completo, la comuna que elijas, sus unidades vecinales en el bivariado y un laboratorio que vuelve a subir de escala para probar denominadores, con vista de avalúos, distribuciones, sensibilidad y lectura comunal. Una exención no deja de ser distributiva porque se llame beneficio: también tiene numerador, denominador y geografía.
{: .text-justify}

<a class="btn btn--primary" href="{{ '/catastro_sii_brecha/' | relative_url }}">Explorar el mapa y el laboratorio de denominadores</a>

---

## Fuentes

**Impuesto territorial y comparación internacional**

- Servicio de Impuestos Internos (SII). *Impuesto Territorial*. Base de cálculo, exenciones, reavalúo y cartografía predial. [sii.cl](https://www.sii.cl/destacados/impuesto_territorial/index.html).
- Servicio de Impuestos Internos (SII). *¿Para qué sirve el pago del impuesto territorial?* Destino municipal y Fondo Común Municipal. [sii.cl](https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html).
- OCDE (2022). *Housing Taxation in OECD Countries*. OECD Tax Policy Studies, N.º 29. [10.1787/03dfe007-en](https://doi.org/10.1787/03dfe007-en).
- Grote, M. & Wen, J.-F. (2024). *How to Design and Implement Property Tax Reforms*. IMF How-To Notes, 2024/006. [10.5089/9798400288753.061](https://doi.org/10.5089/9798400288753.061).
- Banco Mundial (2020). *Property Tax Diagnostic Manual*. [Repositorio institucional](https://openknowledge.worldbank.org/handle/10986/34793).
- Senado de la República de Chile (15 de julio de 2026). *Reconstrucción nacional: ¿cuáles fueron los aspectos centrales aprobados?* Antecedente legislativo del Boletín N.º 18.216-05, consultado el 26 de julio de 2026. [senado.cl](https://www.senado.cl/comunicaciones/noticias/reconstruccion-nacional-cuales-fueron-los-aspectos-centrales-aprobados).
- Cooperativa (22 de julio de 2026). *Megarreforma: comisión mixta aprobó compensación a municipios por exención de contribuciones*. Fórmula aprobada por la comisión mixta y estado de tramitación, consultados el 26 de julio de 2026. [cooperativa.cl](https://www.cooperativa.cl/noticias/pais/politica/agenda-legislativa/megarreforma-comision-mixta-aprobo-compensacion-a-municipios-por/2026-07-22/171256.html).

**Método y teoría**

- Sabatini, F., Cáceres, G. & Cerda, J. (2001). *Segregación residencial en las principales ciudades chilenas: Tendencias de las tres últimas décadas y posibles cursos de acción*. EURE, 27(82), 21-42. [10.4067/S0250-71612001008200002](https://doi.org/10.4067/S0250-71612001008200002).
- López-Morales, E., Sanhueza, C., Espinoza, S. & Órdenes, F. (2019). *Verticalización inmobiliaria y valorización de renta de suelo por infraestructura pública: un análisis econométrico del Gran Santiago, 2008-2011*. EURE, 45(136), 113-134. [10.4067/S0250-71612019000300113](https://doi.org/10.4067/S0250-71612019000300113).
- Rosen, S. (1974). *Hedonic Prices and Implicit Markets*. Journal of Political Economy, 82(1), 34-55. [10.1086/260169](https://doi.org/10.1086/260169).
- Goodchild, M. F., Anselin, L. & Deichmann, U. (1993). *A Framework for the Areal Interpolation of Socioeconomic Data*. Environment and Planning A, 25(3), 383-397. [10.1068/a250383](https://doi.org/10.1068/a250383).
- Robinson, W. S. (1950). *Ecological Correlations and the Behavior of Individuals*. American Sociological Review, 15(3), 351-357. [10.2307/2087176](https://doi.org/10.2307/2087176).
- Shorrocks, A. F. (1984). *Inequality Decomposition by Population Subgroups*. Econometrica, 52(6), 1369-1385. [10.2307/1913511](https://doi.org/10.2307/1913511).
- Fotheringham, A. S. & Wong, D. W. S. (1991). *The Modifiable Areal Unit Problem in Multivariate Statistical Analysis*. Environment and Planning A, 23(7), 1025-1044. [10.1068/a231025](https://doi.org/10.1068/a231025).
- Hodge, T. R., McMillen, D. P., Sands, G. & Skidmore, M. (2017). *Assessment Inequity in a Declining Housing Market: The Case of Detroit*. Real Estate Economics, 45(2), 237-258. [10.1111/1540-6229.12126](https://doi.org/10.1111/1540-6229.12126).
