---
layout: single
title: "Avalúo fiscal e IGVUST por unidad vecinal: el denominador cambia el mapa"
subtitle: "Una lectura descriptiva de 9,4 millones de predios SII agregados a unidades vecinales, con foco en superficie, hogares RSH, fuga territorial y escala"
date: 2026-07-23 10:00:00 -0400
categories: [datos, python, territorio]
tags: [catastro-sii, igvust, unidad-vecinal, desigualdad, gini, theil, duckdb, geoespacial, datos-abiertos]
description: "Cruce descriptivo entre avalúo fiscal SII e IGVUST por unidad vecinal. El resultado estable no es una paradoja social: es la sensibilidad al denominador, al universo RSH, a la geometría disponible y a la escala territorial."
excerpt: "Un catastro registra predios, no personas. Para compararlo con vulnerabilidad territorial hay que declarar qué se suma, por qué se divide, qué superficie se observa y qué queda fuera."
author: clabra
lang: es
ref: avaluo-vulnerabilidad-uv
permalink: /datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/
header:
  teaser: /assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-teaser-640.webp
  og_image: /assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-social-1200x630.webp
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

Un mapa de datos no empieza en los colores. Empieza antes, en cuatro decisiones menos fotogénicas: **qué se suma, entre qué se divide, sobre qué territorio se agrega y qué casos quedan fuera**. Si cualquiera de esas decisiones cambia, el mapa también puede cambiar aunque el catastro original sea el mismo.
{: .text-justify}

La fracción mínima es esta:
{: .text-justify}

$$
\text{indicador territorial}
=
\frac{\text{total que se quiere describir}}
{\text{unidad con que se lo compara}}
$$

El total de avalúo fiscal de una unidad vecinal responde cuánto valor administrativo fue asignado allí. Dividir ese mismo total por hogares, personas o metros cuadrados responde preguntas distintas. Ninguna es "la correcta" por naturaleza; el error aparece cuando se las usa como si fueran equivalentes.
{: .text-justify}

## Contrato de lectura

Cruzo dos registros administrativos chilenos. El primero es el catastro de bienes raíces del Servicio de Impuestos Internos (SII). El segundo es el Índice Global de Vulnerabilidad Socioterritorial (IGVUST) del Ministerio de Desarrollo Social y Familia. La unidad de análisis es la **unidad vecinal (UV)**, no el predio, el hogar ni la persona.
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

El punto del RSH es importante. A escala nacional su universo es amplio, pero no reemplaza la proyección censal ni tiene igual cobertura en todas las comunas. En comunas con baja presencia relativa en RSH, como puede ocurrir en Vitacura, un indicador "por hogar RSH" puede amplificar el avalúo por un denominador estrecho. El visor SIVUST que aún no está público trabaja esa comparación contra proyecciones censales y RSH con disclaimers explícitos; aquí mantengo la misma cautela.
{: .text-justify}

El avalúo fiscal tampoco es precio de mercado. El SII lo construye con características del bien y su área homogénea. Puede ser una señal territorial útil, siempre que conserve su apellido: **fiscal**. La teoría de precios hedónicos de [Rosen (1974)](https://doi.org/10.1086/260169) ayuda a entender por qué el entorno importa en la valoración de bienes diferenciados, pero este post no observa transacciones ni patrimonio familiar.
{: .text-justify}

**Corte de datos:** 19 de julio de 2026. **Fecha editorial:** 23 de julio de 2026. Todas las relaciones son descriptivas y dependen de la malla UV utilizada.
{: .small}

## Pregunta

Agregué el avalúo fiscal de predios SII a escala UV y lo comparé con el orden nacional de vulnerabilidad del IGVUST. Mantengo fijo el numerador y cambio la lente:
{: .text-justify}

| Medida | Pregunta que responde |
|---|---|
| Avalúo total | ¿Cuánto avalúo fiscal fue asignado a esta UV? |
| Avalúo por hogar RSH | ¿Cuánto avalúo asignado corresponde por hogar registrado en la UV? |
| Avalúo por persona RSH | ¿Cuánto corresponde por persona registrada? |
| Avalúo por m² predial | ¿Cuánto avalúo corresponde por superficie predial asignada? |

La respuesta corta: por hogar y por persona casi no hay relación con vulnerabilidad. Por metro cuadrado aparece una relación nacional fuerte, pero al mirar sólo UV mayoritariamente urbanas esa relación se diluye. El hallazgo no es una paradoja glamorosa entre riqueza y vulnerabilidad. Es más sobrio, y por eso más útil: **denominador, universo y escala forman parte del resultado**.
{: .text-justify}

Este análisis no permite saber cuánto ganan los habitantes, cuánto vale una vivienda en el mercado ni quién vive en un predio. Convertir una asociación territorial en afirmación sobre individuos sería la inferencia ecológica que [Robinson (1950)](https://doi.org/10.2307/2087176) dejó advertida hace rato.
{: .text-justify}

## Cucharada 1: construir el numerador sin cerrar la fuga

El corte original trae **10.343.893 registros**. Registro no equivale a predio único. Después de deduplicar la clave catastral —comuna, manzana y número predial— quedan **9.401.277 predios**. El objetivo es repartir su avalúo sobre **6.891 UV** antes de probar denominadores.
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

**No renormalizo.** Si $$\sum_u f_{p,u} < 1$$, una parte del predio quedó fuera de toda UV. Redistribuir ese resto entre las UV que sí tocó produciría una suma perfecta y una medición peor: escondería que la UV no fue diseñada para teselar Chile.
{: .text-justify}

El residuo es concreto: **271.150 predios**, **2,884%** de los deduplicados, no quedaron en ninguna UV. La fuga mediana comunal es **0,644%**, pero no es homogénea. En Antofagasta, 2.325 predios fuera de UV concentran **32,6%** del avalúo fiscal comunal; en Tortel, Timaukel, San Gregorio, Laguna Blanca y Río Verde la fuga llega a 100%, porque las UV cubren el poblado y los predios catastrados quedan fuera de esa malla.
{: .text-justify}

Ese sesgo se declara, no se barre debajo de la alfombra. En comunas con muchos predios sin polígono o mucha fuga fuera de UV, el cruce UV subrepresenta parte del catastro. La lectura pública debe mirar esos indicadores antes de interpretar colores.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline.webp' | relative_url }}" title="Figura 1 — Del registro original al universo espacial" aria-label="Abrir la Figura 1 ampliada">
    <picture>
      <source srcset="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline.svg' | relative_url }}" type="image/svg+xml">
      <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline.webp' | relative_url }}" alt="Diagrama de flujo: 10.343.893 registros originales se separan en 942.616 duplicados y 9.401.277 predios únicos; de estos últimos, 9.130.127 tocan al menos una unidad vecinal y 271.150 no tocan ninguna." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 1</strong> — Del registro original al universo espacial. «Toca al menos una UV» no significa asignación completa: un predio puede intersectar una UV y conservar parte de su superficie fuera de la malla. Fuente: elaboración propia, corte 19/07/2026. Haz clic para ampliar.</figcaption>
</figure>

## Antes del IGVUST: tamaño del avalúo observado

Antes de cruzar vulnerabilidad conviene saber de qué magnitud hablamos. En las 346 comunas, el avalúo fiscal asignado suma **587,4 billones de pesos**. La Región Metropolitana concentra **286,7 billones** (**48,8%**); Valparaíso, **56,2 billones** (**9,6%**); Biobío, **39,4 billones** (**6,7%**). La concentración no es un detalle: define el tamaño del numerador que luego se divide.
{: .text-justify}

Por comuna, las mayores sumas asignadas son Las Condes (**38,2 billones**), Santiago (**27,1**), Providencia (**16,3**), Lo Barnechea (**16,0**) y Vitacura (**15,2**). Antofagasta también aparece arriba (**15,1 billones**), pero con una fuga UV comunal muy alta; ese es precisamente el tipo de caso donde el total, el denominador y el universo deben leerse juntos.
{: .text-justify}

El visor incorpora esta lectura pura en la pestaña **Avalúos**. Primero el numerador; después la historia.
{: .text-justify}

<figure class="avaluo-bars" aria-labelledby="avaluo-bars-title">
  <figcaption id="avaluo-bars-title"><strong>Gráfico 1</strong> — Avalúo fiscal total asignado antes de normalizar. Las barras regionales muestran participación sobre el total nacional asignado; las comunales, monto total en billones de pesos.</figcaption>
  <div class="avaluo-bars__grid">
    <section class="avaluo-bars__panel" aria-label="Participación regional del avalúo fiscal asignado">
      <h3>Regiones</h3>
      <div class="avaluo-bars__row"><span>Metropolitana</span><div class="avaluo-bars__track"><span style="--w: 100%"></span></div><strong>48,8%</strong></div>
      <div class="avaluo-bars__row"><span>Valparaíso</span><div class="avaluo-bars__track"><span style="--w: 19.7%"></span></div><strong>9,6%</strong></div>
      <div class="avaluo-bars__row"><span>Biobío</span><div class="avaluo-bars__track"><span style="--w: 13.7%"></span></div><strong>6,7%</strong></div>
      <div class="avaluo-bars__row"><span>La Araucanía</span><div class="avaluo-bars__track"><span style="--w: 9.8%"></span></div><strong>4,8%</strong></div>
      <div class="avaluo-bars__row"><span>Maule</span><div class="avaluo-bars__track"><span style="--w: 9.2%"></span></div><strong>4,5%</strong></div>
    </section>
    <section class="avaluo-bars__panel" aria-label="Comunas con mayor avalúo fiscal asignado">
      <h3>Comunas</h3>
      <div class="avaluo-bars__row"><span>Las Condes</span><div class="avaluo-bars__track"><span style="--w: 100%"></span></div><strong>38,2</strong></div>
      <div class="avaluo-bars__row"><span>Santiago</span><div class="avaluo-bars__track"><span style="--w: 71.0%"></span></div><strong>27,1</strong></div>
      <div class="avaluo-bars__row"><span>Providencia</span><div class="avaluo-bars__track"><span style="--w: 42.7%"></span></div><strong>16,3</strong></div>
      <div class="avaluo-bars__row"><span>Lo Barnechea</span><div class="avaluo-bars__track"><span style="--w: 41.9%"></span></div><strong>16,0</strong></div>
      <div class="avaluo-bars__row"><span>Vitacura</span><div class="avaluo-bars__track"><span style="--w: 39.8%"></span></div><strong>15,2</strong></div>
    </section>
  </div>
  <p class="avaluo-bars__note">Total nacional asignado: 587,4 billones CLP. En comunas con fuga UV o baja cobertura relativa del denominador RSH, este tamaño no debe confundirse con una lectura completa del territorio ni de sus residentes.</p>
</figure>

## Cucharada 2: cuartiles, bivariado y denominadores

El IGVUST ordena unidades vecinales según vulnerabilidad socioterritorial. Mantengo sus cuatro cuartiles oficiales porque son el contrato analítico de esa fuente. En el mapa, sólo compacto visualmente el eje de avalúo en tres tramos: bajo, medio y alto. El resultado es una matriz 3×4 más legible: tres columnas de avalúo por cuatro filas IGVUST. Una partición más fina volvería el bivariado más difícil de leer y, en territorios con pocas comunas como Arica y Parinacota, podría sugerir una precisión que los datos agregados no entregan. Un cuartil indica orden relativo, no distancia.
{: .text-justify}

En el mapa bivariado la lectura principal usa **avalúo por m² predial**. Es la señal más clara para poner atención donde alto avalúo unitario coincide con alta vulnerabilidad territorial. En la paleta, esas celdas quedan más oscuras, con una capa transparente para no tapar el fondo ni convertir el mapa en alarma cromática. Lo contraintuitivo debe llamar la atención; lo evidente no necesita megáfono. El indicador sigue siendo descriptivo y nacional; al restringir a UV con $$p_\text{urbano} > 50$$ la asociación por m² se atenúa fuertemente.
{: .text-justify}

En el visor separé la lectura en dos mapas. El primero es geométrico: OSM, predios SII piloto y UV transparentes, con bordes distintos para revisar límites antes de leer colores. El segundo es analítico: sólo UV, selector gráfico de Chile, selector de región/comuna como respaldo, hover con datos de la UV y leyenda 3×4. La selección tomada en ese bloque se mantiene en las tablas y en el ranking territorial cuando corresponde. Esa separación evita mezclar la inspección de geometría predial con la clasificación bivariada.
{: .text-justify}

### 1. Por hogar, la celda llamativa es una pista

Si se divide por hogares RSH, el cuartil de mayor vulnerabilidad (`q1` IGVUST) contiene 530 UV en el cuartil más alto de avalúo por hogar. Ese número puede parecer una contradicción social. Todavía no lo es.
{: .text-justify}

{: .table-caption}
**Tabla 1** — Unidades vecinales por cuartil nacional de vulnerabilidad y avalúo por hogar

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
**Tabla 2** — Mecanismo del cuartil más vulnerable (`q1` IGVUST)

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
**Tabla 3** — Sensibilidad de la asociación al denominador

| Medida de avalúo | Pearson | Spearman | UV |
|---|---:|---:|---:|
| Total asignado | -0,371 | -0,382 | 6.857 |
| Por hogar RSH | -0,061 | -0,047 | 6.849 |
| Por persona RSH | -0,079 | -0,072 | 6.849 |
| Por m² predial asignado | -0,582 | -0,575 | 6.851 |
| Por m², sólo UV mayoritariamente urbanas | +0,079 | +0,081 | 3.221 |

Por hogar y por persona, la asociación es casi nula. Por m², el patrón nacional parece fuerte. Al restringir a UV predominantemente urbanas cambia a aproximadamente +0,08. La lectura prudente es que el resultado nacional por m² contiene mucho contraste urbano-rural; no que se haya identificado un mecanismo de barrio.
{: .text-justify}

Los violines de la Figura 2 muestran la distribución completa. Su ancho indica dónde se concentran más UV; las líneas internas muestran mediana y rango intercuartílico. Son densidades suavizadas, no siluetas literales del territorio.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores.webp' | relative_url }}" title="Figura 2 — Sensibilidad al denominador y al universo" aria-label="Abrir la Figura 2 ampliada">
    <picture>
      <source srcset="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores.svg' | relative_url }}" type="image/svg+xml">
      <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores.webp' | relative_url }}" alt="Tres gráficos de violín comparan las distribuciones de avalúo por hogar, avalúo por metro cuadrado nacional y avalúo por metro cuadrado en unidades vecinales mayoritariamente urbanas, para los cuatro cuartiles nacionales de vulnerabilidad." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 2</strong> — El mismo avalúo produce distribuciones distintas al cambiar el denominador y el universo. Los violines muestran densidades estimadas; su forma depende del ancho de banda y no prueba grupos naturales ni causalidad. Las líneas internas resumen mediana y rango intercuartílico. Fuente: elaboración propia, corte 19/07/2026. Haz clic para ampliar.</figcaption>
</figure>

### 4. Lo robusto es la sensibilidad

Entre las **6.843 UV** con cuartil disponible tanto por hogar como por m², sólo **1.362 (19,9%)** permanecen en el mismo cuartil y **3.132 (45,8%)** se desplazan dos o más. No cambiaron los predios. Cambió la pregunta.
{: .text-justify}

## Cucharada 3: escala y concentración

Entre las **6.857 UV con avalúo asignado positivo**, el Gini es **0,7265**. Describe una base tributaria territorial muy concentrada; no es un Gini de ingresos ni de patrimonio de personas.
{: .text-justify}

El Gini resume concentración, pero no separa cuánto ocurre dentro y entre grupos. Para eso sirve el índice de **Theil**, que sí se descompone. Con $$x_i$$ como avalúo asignado a la UV $$i$$, $$\mu$$ como su media y $$w_g$$ como la participación del grupo $$g$$ en el avalúo total:
{: .text-justify}

$$
T = \frac{1}{n}\sum_{i=1}^{n} \frac{x_i}{\mu} \ln\!\left(\frac{x_i}{\mu}\right)
= \underbrace{\sum_{g} w_g T_g}_{\text{intra}} + \underbrace{\sum_{g} w_g \ln\!\left(\frac{\mu_g}{\mu}\right)}_{\text{entre}}
$$

Agrupando por región, $$T = 1{,}2042$$ y 81,0% queda dentro de las regiones. Al reagrupar por comuna, la parte entre-grupos llega a 56,9%. La comuna no "revela" segregación por arte de magia: al refinar una partición, parte de la desigualdad se desplaza desde el componente intra al componente entre por construcción ([Shorrocks, 1984](https://doi.org/10.2307/1913511)).
{: .text-justify}

Ese es el problema de la unidad areal modificable, o MAUP ([Fotheringham & Wong, 1991](https://doi.org/10.1068/a231025)). Los mismos predios pueden producir estadísticas distintas si se agrupan en regiones, comunas o UV. La escala no adorna el resultado: lo define.
{: .text-justify}

Segundo freno: los cuartiles IGVUST ordenan UV, no personas. El cuartil de mayor vulnerabilidad reúne 25% de las unidades, pero **2.032.893 de 15.978.644 personas RSH (12,7%)**. Una coropleta puede sobrerrepresentar territorio rural disperso aunque sus colores estén perfectamente calculados.
{: .text-justify}

Tercer freno: la literatura de *assessment ratio* muestra que la valoración fiscal puede apartarse sistemáticamente de valores de mercado y que el patrón depende del contexto institucional. [Hodge, McMillen, Sands y Skidmore (2017)](https://doi.org/10.1111/1540-6229.12126) estudian ese problema en otro mercado; no prueban que el SII tenga el mismo sesgo. Lo que sí impiden es usar avalúo fiscal como sinónimo de precio de mercado.
{: .text-justify}

## Cierre: brechas que sí importan

La conclusión pública no es que el cruce "descubre" una paradoja. La conclusión útil es más práctica: identifica brechas que deben cerrarse antes de usar el mapa como evidencia fuerte.
{: .text-justify}

**Brecha 1: universo del denominador.** El RSH cubre cerca de 85% de la población del país, pero no con igual intensidad comunal. Cualquier indicador por hogar o persona RSH debe declarar esa cobertura y, cuando corresponda, contrastarla con proyecciones censales.
{: .text-justify}

**Brecha 2: geometría y superficie.** El prorrateo requiere polígonos. La superficie declarada no reemplaza una geometría faltante sin una regla espacial adicional. Comunas con muchos predios sin polígono necesitan alerta antes de interpretar su color.
{: .text-justify}

**Brecha 3: fuga fuera de UV.** La UV no cubre todo el territorio catastral. Si una comuna concentra mucho avalúo fuera de UV, el cruce UV describe un subconjunto, no el total comunal.
{: .text-justify}

**Brecha 4: urbano-rural.** El avalúo por m² tiene una señal nacional fuerte, pero esa señal cambia al restringir a UV urbanas. El indicador requiere filtro de universo, no sólo una paleta intensa.
{: .text-justify}

**Brecha 5: escala.** Región, comuna y UV no son versiones ampliadas de la misma pregunta. Cambiar la unidad territorial cambia la estadística.
{: .text-justify}

El visor permite explorar esas brechas con dos mapas separados —capas geométricas primero, bivariado UV después—, la vista de avalúos, las distribuciones, la sensibilidad y la vista comunal. La invitación es simple: mirar más, concluir menos rápido.
{: .text-justify}

<a class="btn btn--primary" href="{{ '/catastro_sii_brecha/?vista=avaluos' | relative_url }}">Explorar el mapa y el laboratorio de denominadores</a>

---

## Fuentes

**Método y teoría**

- Rosen, S. (1974). *Hedonic Prices and Implicit Markets*. Journal of Political Economy, 82(1), 34-55. [10.1086/260169](https://doi.org/10.1086/260169).
- Goodchild, M. F., Anselin, L. & Deichmann, U. (1993). *A Framework for the Areal Interpolation of Socioeconomic Data*. Environment and Planning A, 25(3), 383-397. [10.1068/a250383](https://doi.org/10.1068/a250383).
- Robinson, W. S. (1950). *Ecological Correlations and the Behavior of Individuals*. American Sociological Review, 15(3), 351-357. [10.2307/2087176](https://doi.org/10.2307/2087176).
- Shorrocks, A. F. (1984). *Inequality Decomposition by Population Subgroups*. Econometrica, 52(6), 1369-1385. [10.2307/1913511](https://doi.org/10.2307/1913511).
- Fotheringham, A. S. & Wong, D. W. S. (1991). *The Modifiable Areal Unit Problem in Multivariate Statistical Analysis*. Environment and Planning A, 23(7), 1025-1044. [10.1068/a231025](https://doi.org/10.1068/a231025).
- Hodge, T. R., McMillen, D. P., Sands, G. & Skidmore, M. (2017). *Assessment Inequity in a Declining Housing Market: The Case of Detroit*. Real Estate Economics, 45(2), 237-258. [10.1111/1540-6229.12126](https://doi.org/10.1111/1540-6229.12126).
