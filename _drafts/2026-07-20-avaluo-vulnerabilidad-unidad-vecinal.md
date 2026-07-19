---
layout: single
title: "Lo que el catastro sabe del barrio: avalúo fiscal contra vulnerabilidad oficial"
subtitle: "10,3 millones de predios repartidos en 6.891 unidades vecinales, y las tres veces que el dato se contradice a sí mismo"
date: 2026-07-20 10:00:00 -0400
categories: [datos, python, territorio]
tags: [catastro-sii, igvust, unidad-vecinal, desigualdad, gini, theil, duckdb, geoespacial, datos-abiertos]
description: "Agregamos el avalúo fiscal de todos los predios del SII a las unidades vecinales del IGVUST para preguntar dónde el valor del suelo y la vulnerabilidad oficial se contradicen. Gini 0,73, y tres advertencias que el propio dato obliga a declarar."
excerpt: "El avalúo fiscal es lo que el Estado cree que vale tu barrio. El IGVUST es lo que el Estado cree que le falta. Cruzarlos a escala de unidad vecinal es más incómodo de lo que parece."
author: clabra
lang: es
ref: avaluo-vulnerabilidad-uv
permalink: /datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/
math: true
distribution:
  social: true
  republish: []
toc: true
toc_sticky: true
comments: true
author_profile: true
---

El Estado tiene dos formas de mirar un barrio. Una es el **avalúo fiscal**: cuánto vale ese suelo para efectos de contribuciones. La otra es el **IGVUST**, el índice de vulnerabilidad socioterritorial con que el Ministerio de Desarrollo Social prioriza dónde llegar primero.
{: .text-justify}

Nunca se miran entre sí. Este post los cruza a escala de **unidad vecinal**, que es la escala en que la gente efectivamente vive, y no la comuna, que es donde suele terminar todo análisis territorial en Chile.
{: .text-justify}

Spoiler: el cruce funciona, pero el dato se contradice a sí mismo tres veces. Esas contradicciones son lo interesante.
{: .text-justify}

## Antes de las cucharadas: por qué el avalúo dice algo

El avalúo no es precio de mercado. Pero tampoco es un número inventado: el SII lo construye a partir de superficie, materialidad, destino y **área homogénea** —una zona de valores unitarios similares—. Es decir, incorpora atributos del entorno.
{: .text-justify}

Eso conecta con la teoría de precios hedónicos de [Rosen (1974)](https://doi.org/10.1086/260169): el precio de un bien diferenciado es la suma de lo que el mercado paga por cada uno de sus atributos. Aplicado a suelo, el precio absorbe seguridad, conectividad, equipamiento y calidad ambiental sin nombrarlos.
{: .text-justify}

Con una diferencia crítica: el avalúo **persigue** al mercado, no lo iguala. Y persigue mal. Volveremos a eso en la tercera cucharada, porque es la parte que puede tumbar todo el análisis.
{: .text-justify}

## Cucharada 1: repartir 10 millones de predios sin inventar nada

El problema técnico es simple de enunciar: los predios son polígonos, las unidades vecinales también, y no coinciden. Un predio puede caer entero dentro de una UV, cruzar el límite de dos, o quedar fuera de todas.
{: .text-justify}

La regla que usé es prorrateo por área de intersección. Para un predio $p$ y una unidad vecinal $u$:
{: .text-justify}

$$
f_{p,u} = \frac{\text{área}(p \cap u)}{\text{área}(p)}
\qquad
A_u = \sum_{p} a_p \cdot f_{p,u}
$$

donde $a_p$ es el avalúo del predio. Si el predio está entero dentro, $f = 1$ y aporta todo. Si lo cruza a medias, aporta la mitad.
{: .text-justify}

Dos decisiones que parecen menores y no lo son.
{: .text-justify}

**Uso el área geométrica, no la superficie declarada.** El catastro trae `dc_sup_terreno`, que suena a la variable correcta. Pero tiene 12,8% de nulos, mientras la geometría del polígono tiene 2,6%. Prorratear con el dato que falta menos no es pereza: es no fabricar supuestos donde ya hay medición.
{: .text-justify}

**No renormalizo.** Si $\sum_u f_{p,u} < 1$, parte del predio quedó fuera de toda unidad vecinal. La tentación es repartir ese resto entre las UV que sí lo tocan, para que todo cuadre. No lo hice, y ese residuo resultó ser el hallazgo más interesante del ejercicio.
{: .text-justify}

Todo corre en DuckDB con la extensión espacial, leyendo GeoParquet y shapefile directo desde el zip. 10.343.893 predios, 6.891 unidades vecinales, unos 45 minutos de una laptop.
{: .text-justify}

## Cucharada 2: el 2,88% que no cabe en ningún barrio

Al terminar el reparto, **271.150 predios no cayeron en ninguna unidad vecinal**. Un 2,88%.
{: .text-justify}

Mi primera reacción fue buscar el bug. No había. La Ley 19.418 define la unidad vecinal como *el territorio jurisdiccional de una junta de vecinos*: se dibuja donde hay vecinos organizados, no para cubrir el mapa. **Las UV no teselan Chile.** Nada obliga a que un yacimiento, un fundo o un paño industrial pertenezcan a alguna.
{: .text-justify}

Y la fuga no se reparte al azar. En Antofagasta, apenas 1,3% de los predios queda fuera, pero se llevan el **32,6% del avalúo comunal**: 2.325 predios que concentran 7.260 mil millones de pesos en 1.030 km². En Tortel, Timaukel, San Gregorio, Laguna Blanca y Río Verde la fuga es del **100%**: sus unidades vecinales existen, cubren el poblado —entre 168 y 525 personas— y todos los predios catastrados son estancias fuera de él.
{: .text-justify}

Dicho de otro modo: **hay riqueza registrada en territorio que la vulnerabilidad oficial no puede ver**, porque la vulnerabilidad se mide donde hay gente organizada y el valor está donde no la hay.
{: .text-justify}

Si hubiera renormalizado, ese número no existiría. Habría repartido esos 7.260 mil millones entre las UV vecinas y el mapa se vería más limpio y diría algo falso.
{: .text-justify}

## Cucharada 3: la desigualdad, y las tres veces que hay que frenar

Sobre las 6.891 unidades vecinales con avalúo asignado, el Gini es **0,7265**. Alto, y era esperable: el valor del suelo se concentra mucho más que el ingreso.
{: .text-justify}

Para saber *dónde* se concentra hace falta descomponer, y el Gini no se deja: no es aditivamente descomponible. El índice de Theil sí. Con $x_i$ el avalúo de la UV $i$ y $\mu$ la media:
{: .text-justify}

$$
T = \frac{1}{n}\sum_{i=1}^{n} \frac{x_i}{\mu} \ln\!\left(\frac{x_i}{\mu}\right)
= \underbrace{\sum_{g} w_g T_g}_{\text{intra}} \;+\; \underbrace{\sum_{g} w_g \ln\!\left(\frac{\mu_g}{\mu}\right)}_{\text{entre}}
$$

Agrupando por región: $T = 1{,}2042$, con **81,0% intra-regional**. La desigualdad del valor del suelo está *dentro* de cada región, no entre regiones. Que Antofagasta sea más rica que La Araucanía explica menos de un quinto del total.
{: .text-justify}

Aquí viene el primer freno, y es a mí mismo. Al reagrupar por comuna el componente entre-grupos sube a 56,9%, y mi primera lectura fue que "el territorio segrega a escala comunal". **Es una sobreinterpretación.** Con particiones anidadas —las comunas están dentro de las regiones— refinar la partición aumenta el componente inter-grupo casi por construcción ([Shorrocks, 1984](https://doi.org/10.2307/1913511)): la desigualdad entre comunas de una misma región se reclasifica de intra a entre. Buena parte del salto es álgebra, no evidencia.
{: .text-justify}

Sirve igual, pero como otra cosa: es una demostración limpia del **problema de la unidad areal modificable** ([Openshaw & Taylor, 1979](https://www.researchgate.net/publication/244957000)). El mismo dato, agregado a distinta escala, cuenta distinta historia. Ninguna de las dos miente; la pregunta es cuál escala corresponde a la decisión que quieres tomar.
{: .text-justify}

**Segundo freno: los cuartiles del IGVUST no cuentan personas.** Cada cuartil agrupa un cuarto de las *unidades vecinales*, no de la población. El cuartil más vulnerable reúne el 25% de las UV y solo el **12,5% de las personas**: son unidades rurales y pequeñas. Cualquier mapa coroplético de UV sobrerrepresenta territorio disperso por construcción. Y el propio Ministerio lo advierte por escrito: sus cuartiles "son válidos exclusivamente para la región analizada".
{: .text-justify}

**Tercer freno, y es el serio.** El avalúo no persigue al mercado de forma pareja: la literatura de *assessment ratio* documenta que las propiedades baratas tienden a estar **sobretasadas** respecto de su valor real, y las caras subtasadas. [Hodge, McMillen, Sands y Skidmore (2017)](https://doi.org/10.1111/1540-6229.12179) muestran además que esa regresividad **empeora en mercados deprimidos**.
{: .text-justify}

Léelo dos veces, porque es incómodo: el sesgo del avalúo va en la misma dirección que la variable que estoy cruzando. No es ruido aleatorio que se lave con el tamaño de muestra. **Donde el IGVUST marca más vulnerabilidad, el avalúo tiende a estar relativamente inflado.** Eso comprime artificialmente la brecha que el análisis busca medir, y significa que la desigualdad real de valor de suelo es probablemente **mayor** que el 0,73 que reporté.
{: .text-justify}

Sumemos que en Chile el reavalúo se ha pospuesto por ley al menos nueve veces desde 1990, y el avalúo no solo es sesgado: además está viejo.
{: .text-justify}

## La papa

El cruce se puede hacer, da resultados coherentes, y el pipeline es reproducible en una laptop. Tres cosas que me llevo:
{: .text-justify}

**Uno.** El residuo es información. El 2,88% que no cabía en ninguna unidad vecinal terminó siendo el hallazgo más nítido del ejercicio, y solo existe porque no lo normalicé para que cuadrara.
{: .text-justify}

**Dos.** La escala no es un detalle de implementación, es parte del resultado. Cambiarla cambió el número y casi me hace publicar como hallazgo lo que era una identidad algebraica.
{: .text-justify}

**Tres.** Cuando el sesgo de tu medición está correlacionado con lo que quieres medir, no basta con declararlo al final en letra chica. Es lo primero que hay que decir.
{: .text-justify}

Nada de esto invalida usar el avalúo para mirar territorio. Lo que invalida es usarlo sin decir estas tres cosas.
{: .text-justify}

---

## Fuentes

**Método y teoría**

- Rosen, S. (1974). *Hedonic Prices and Implicit Markets*. Journal of Political Economy, 82(1), 34–55. [10.1086/260169](https://doi.org/10.1086/260169) — por qué el precio del suelo absorbe atributos del entorno.
- Shorrocks, A. F. (1984). *Inequality Decomposition by Population Subgroups*. Econometrica, 52(6), 1369–1385. [10.2307/1913511](https://doi.org/10.2307/1913511) — por qué refinar la partición sube el componente entre-grupos.
- Openshaw, S. & Taylor, P. J. (1979). *A million or so correlation coefficients*. En *Statistical Applications in the Spatial Sciences* — el problema de la unidad areal modificable.
- Hodge, T. R., McMillen, D. P., Sands, G. & Skidmore, M. (2017). *Assessment Inequity in a Declining Housing Market*. Real Estate Economics, 45(2), 237–258. [10.1111/1540-6229.12179](https://doi.org/10.1111/1540-6229.12179) — la regresividad del avalúo y su relación con mercados deprimidos.
- Meyer, M. A., Broome, F. R. & Schweitzer, R. H. (1975). *Color statistical mapping by the U.S. Bureau of the Census* — origen de la coropleta bivariada.

**Datos y normativa**

- Servicio de Impuestos Internos — catastro de bienes raíces, primer semestre 2026.
- Ministerio de Desarrollo Social y Familia — Índice Global de Vulnerabilidad Socioterritorial (IGVUST), corte junio 2026: 18 indicadores en 7 dimensiones, ponderados por análisis factorial.
- Ley N° 19.418 sobre Juntas de Vecinos y demás Organizaciones Comunitarias — define la unidad vecinal como territorio jurisdiccional de una junta de vecinos.
- Ley N° 17.235 sobre Impuesto Territorial (DFL N° 1 de 1998).
- SUBDERE — División Político Administrativa 2023.

La bibliografía completa, con 31 referencias verificadas contra CrossRef, está en el repositorio del sitio.
{: .small}
