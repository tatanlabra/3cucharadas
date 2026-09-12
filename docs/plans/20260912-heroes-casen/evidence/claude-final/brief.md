# R1: Independent adversarial review of the integrated local candidate

Task R1, requested model sonnet via canonical Claude CLI; provider independence must be explicit, no simulated execution. Read-only. No raw records, credentials or personal configuration are provided. Do not change product files or run network writes. Return a single JSON object in your final response, no markdown fence: task_id, source_digest, provider, requested_model, effective_identity_evidence, findings (id/severity/status/claim/evidence/remedy), open_p0_p1 (boolean false only if no unresolved critical finding), verdict, limitations.

Exact candidate source_digest: 918f6c4edda5d6ed0bef4075dbd63816c9cce8bb6af4dd41812f40160998dded. The digest binds current product sources plus built posts/assets in source-freeze.json. Baseline blog HEAD bf1ff5ac. D1 scientific module already independently reviewed by Anthropic and accepted with source digest14eaab859814dda0d89066b79c7b395b8e1cbb3e90aa7e65f5f080fe3dddec80; consume D2 rather than invent recomputation. 13 original inputs/aggregates and 20 original titles/dates/routes rehashed unchanged. No push/publication authorized. New AI UI is explicitly user-requested: brief first person ES/EN, details on separate policy, only documented tools named. Historical some_ai is user declaration, component unknown allowed. New outputs are all aggregate-only.

Review the faithful scientific/editorial integration, competing explanations, inferential units, monetary counterfactuals vs actual taxation/revenue, ES/EN equivalence, AI provenance and UI code, complete table alternatives, test negative controls and remaining risk. Do not treat rendered figure decoration as geographic evidence, household p_h as dwellings/site, commune expc as representativeness, or a successful receipt as causality/benchmark/global optimum. Regional CI approximate, communal CI absent, eleven communes without sample missing notzero. r2 is algebra for hypothetical dwelling-share p_v; NEVER plug p_h or modify fiscal bars. Existing model taxes are theoretical annual equivalents, not observed bills or revenue. Python/geomatics sidebar must not claim a performed HPC run.

Runtime acceptance boundary: 8 bilingual/width/theme chart combinations have368/368 checks and16 scoped axe audits without detected violations; contrast incomplete preserved and bounded via effective colors. This evidence covers unchanged chart/table selectors, NOT the newest AI UI. The new80-case hero/AI UI browser matrix and5 paired cold/warm performance runs are still executing under Q1 and are NOT accepted in this packet. The performance contract remains median LCP<=2500ms and <=10% regression, CLS<=0.1, same setup. Do not certify these pending checks; identify code/content findings now, and state final release acceptance is separate and pending Q1. Previous performance pilot under high CPU contention was inconclusive/RED, no threshold relaxed. No claim of physical Safari/iPhone or global WCAG compliance.

You may read source-freeze.json from this isolated directory if needed; the code/content below is inline. Hash validation over actual current files is root's separate check, not something you should assert you executed. If a finding is a hypothesis, state discriminating evidence and discard condition. Prioritize actual material defects, not invented mandatory tools. A residual P2 limitation must stay visible; any substantive P0/P1 blocks acceptance.


## _posts/2026-09-11-avaluos-ii-brecha-residencial.md
```
---
layout: single
classes: [avaluos-ii-editorial]
title: "Avalúos en 3 cucharadas II: dónde revisar la brecha residencial"
subtitle: "Campamentos, materialidad y avalúos para pasar de una diferencia comunal a una revisión predial"
date: 2026-09-11 00:00:00 -0300
categories: [datos, territorio]
tags: [catastro-sii, censo-2024, contribuciones, datos-abiertos, desigualdad]
author: clabra
lang: es
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: true
editorial_status: escenario-tributario-hipotetico
description: "Brecha Censo–SII, campamentos y avalúos habitacionales: escenarios de impuesto teórico en pesos para orientar una revisión predial, con supuestos explícitos."
excerpt: "Una diferencia persistente junto a avalúos altos en los predios registrados justifica revisar el catastro. Comprobar omisiones y sus efectos tributarios requiere identificar los inmuebles."
header:
  overlay_image: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/hero-1600x900.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/og-1200x630.webp
  og_image_alt: Ciudad residencial nocturna y polígonos catastrales conceptuales por conciliar.
  overlay_image_mobile: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/hero-mobile-800x450.webp
  teaser_mobile: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/teaser-mobile-640x360.webp
math: true
toc: true
toc_sticky: true
comments: true
visual_id: avaluos-ii
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
---

En el [primer post de avalúos](/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/), cambiar el denominador cambiaba el mapa. Ahora me interesa una pregunta anterior al impuesto: **si el Censo cuenta más viviendas que los roles habitacionales del SII, ¿por dónde conviene empezar a revisar?**

El interés tributario aumenta cuando la discrepancia persiste en comunas cuyos predios registrados presentan avalúos altos. Si una revisión encontrara inmuebles omitidos comparables a ellos, correspondería comprobar si su incorporación o actualización genera una obligación tributaria.

Cruzo esa diferencia con campamentos, materialidad y avalúos para ordenar la búsqueda. El recorrido tiene tres pasos: entender qué estamos restando, dimensionar su posible interés tributario mediante escenarios en pesos y precisar qué evidencia permitiría comprobarlo.

**Cómo leer las barras.** Orientan una revisión; no cuentan inmuebles omitidos ni contribuciones adeudadas.
{: .notice--info}

## Primera cucharada: medir la diferencia sin convertirla en omisión

Comparo **todas las viviendas particulares del Censo 2024**, ocupadas y desocupadas, con los **roles de destino habitacional —código H— del primer semestre de 2026**. El primer recuento corresponde a viviendas; el segundo, a bienes raíces registrados para fines tributarios.

No hay una equivalencia uno a uno. Un predio puede contener varias viviendas y una vivienda puede estar en un predio agrícola, excluido por el filtro habitacional. Tampoco coinciden las fechas. Por eso, viviendas menos roles es una **diferencia entre recuentos**, no un conteo de «viviendas sin rol».

La barra se construye en tres pasos:

| Paso | Operación | Qué representa |
|---|---|---|
| Diferencia inicial | Viviendas censadas menos roles habitacionales | Separación entre ambos recuentos |
| Escenario de campamentos | Descontar el conteo disponible de hogares, suponiendo una unidad de diferencia por hogar | Residuo bajo ese supuesto |
| Escenario de materialidad | Aplicar al residuo la proporción comunal de viviendas de tipo y materiales aceptables | Composición hipotética del residuo |

### Campamentos: cuánto cambia la diferencia bajo un supuesto

En Alto Hospicio, la diferencia inicial es de **15.368**. Si se descuentan los **9.136** hogares que el procesamiento atribuye a los campamentos con dato, quedan **6.232** unidades: una reducción del **59,4 %**. En Puerto Montt, el mismo ejercicio reduce la diferencia apenas un **2,2 %**.

| Comuna | Diferencia inicial | Hogares con dato | Residuo | Reducción |
|---|---:|---:|---:|---:|
| Alto Hospicio | 15.368 | 9.136 | 6.232 | 59,4 % |
| Antofagasta | 21.755 | 7.537 | 14.218 | 34,6 % |
| Viña del Mar | 24.030 | 8.014 | 16.016 | 33,3 % |
| Valparaíso | 32.533 | 2.572 | 29.961 | 7,9 % |
| Puerto Montt | 29.036 | 632 | 28.404 | 2,2 % |

Este descuento es una prueba de sensibilidad, no una explicación demostrada. Varios hogares pueden compartir vivienda, el terreno puede tener un rol matriz y las fechas pueden diferir. Además, la capa utilizada tiene **222 polígonos sin conteo**: dato faltante no significa ausencia de hogares. La interpretación de su campo `HOGARESCEN` se detalla en las notas metodológicas.

El descuento tampoco representa una exención tributaria: es un supuesto analítico. El SII contempla la [tasación de construcciones no regularizadas][sii-no-regularizadas]; la situación de cada inmueble debe verificarse.

En el agregado, la suma de las diferencias comunales positivas pasa de **1.588.449 a 1.516.689**, un descenso del **4,52 %**. No es la diferencia nacional neta: las comunas con saldo negativo no compensan las positivas. El resultado muestra que el supuesto altera mucho algunas comunas y poco otras; no demuestra qué proporción de la discrepancia explican los campamentos.

### Materialidad: describir un escenario, no tasar viviendas

El segundo supuesto pregunta cómo se repartiría el residuo si tuviera la misma composición que las viviendas observadas en la comuna. Para ello uso un criterio de **tipo de vivienda aceptable y materiales aceptables en paredes, techo y piso simultáneamente**, siguiendo el código del [manual de microdatos del INE, indicadores viv04 y viv05, pp. 103–105][ine-manual].

En el procesamiento, **5.774.146 de 6.408.172** viviendas particulares ocupadas con moradores presentes cumplen ese criterio. La proporción se calcula por comuna, manteniendo los datos incompletos en el denominador, pero fuera del grupo aceptable.

Por ejemplo, un residuo de 9.000 unidades y una proporción aceptable del 80 % producirían **7.200 unidades en ese escenario y 1.800 en el resto**. No se han localizado 7.200 viviendas: se ha aplicado una proporción conocida a una diferencia de composición desconocida.

La extrapolación tiene dos límites. La materialidad se observa en viviendas ocupadas con moradores presentes, mientras la diferencia inicial incluye también viviendas desocupadas y con moradores ausentes. Además, las viviendas que eventualmente faltaran del catastro podrían ser distintas de las observadas. **«Resto» tampoco equivale a viviendas irrecuperables**: incluye lo que no cumple el criterio y los datos incompletos.

No agrego otro descuento por viviendas irrecuperables, porque desconozco su superposición con campamentos. Tampoco multiplico este escenario por la proporción de roles sobre el monto exento: no conocemos la distribución conjunta de ambas características.

<figure style="width:100%">
  <div role="region" aria-label="Quince comunas con mayor residuo bajo el supuesto de campamentos. La barra conserva la diferencia inicial y separa el descuento supuesto, el escenario de tipo y materiales aceptables y el resto." tabindex="0" style="max-width:100%;overflow-x:auto;border:1px solid currentColor;border-radius:.4rem">
    <img class="avaluos-ii-monetary-light" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/gap-top15-es.svg" alt="Quince comunas con mayor residuo bajo el supuesto de campamentos. La barra conserva la diferencia inicial y separa el descuento supuesto, el escenario de tipo y materiales aceptables y el resto." loading="lazy">
    <img class="avaluos-ii-monetary-dark" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/gap-top15-es-dark.svg" alt="Quince comunas con mayor residuo bajo el supuesto de campamentos. La barra conserva la diferencia inicial y separa el descuento supuesto, el escenario de tipo y materiales aceptables y el resto." loading="lazy">
  </div>
  <figcaption>Escenarios de composición de la diferencia; no son viviendas omitidas identificadas. Desplaza horizontalmente o abre el SVG para ampliar; los valores están en la tabla siguiente. <a href="/assets/images/avaluos-ii/gap-top15-es.svg">SVG</a> · <a href="/assets/images/avaluos-ii/gap-top15-es-dark.svg">SVG oscuro</a>.</figcaption>
</figure>

{% include avaluos-ii-top-es.html %}

**Cómo leer el gráfico.** El largo total conserva la diferencia inicial; sus segmentos distinguen el descuento supuesto por campamentos y la composición hipotética del residuo. Las quince comunas se ordenan por ese residuo, no por materialidad ni por avalúos. La selección tributaria de la segunda cucharada aplica un filtro diferente.

El [visor permite explorar cada comuna y consultar la tabla completa](/catastro_sii_brecha/#brecha-contribuciones). El [anexo de Valparaíso y Puerto Montt](/catastro_sii_brecha/#catastro-anexo) superpone predios, unidades vecinales y campamentos: ayuda a observar relaciones espaciales, pero no identifica por sí solo viviendas omitidas.

### Varias viviendas en un sitio: una explicación adicional que sí merece contrastarse

Dos viviendas pueden compartir un terreno y estar consideradas en un mismo rol. En ese caso, el Censo cuenta dos viviendas sin que necesariamente falte un predio en el registro tributario. Este mecanismo puede contribuir a la diferencia; demostrar cuánto aporta exige vincular **vivienda, sitio y rol**. El diccionario público examinado y el [manual de microdatos del Censo, pp. 17–20][ine-manual], permiten enlazar vivienda, hogar y persona, pero no proporcionan un identificador común de sitio o rol para esta conciliación. Varios hogares dentro de una vivienda tampoco equivalen a varias viviendas dentro de un sitio.

CASEN 2024 permite observar una señal más acotada. En su pregunta de tenencia, las categorías 3 y 4 identifican hogares que declaran **sitio propio compartido con otras viviendas**, pagado o pagándose. No preguntan cuántas viviendas hay en el sitio. Calculo su proporción entre **todos los hogares con respuesta válida**, incluidos arrendatarios y otras tenencias, usando una jefatura por hogar. La pregunta sobre hogar principal es condicional; filtrarla en toda la base eliminaría indebidamente hogares de viviendas unihogar. Véase el [cuestionario oficial, pp. 79 y 83][casen-cuestionario].

El resultado nacional es **1,09 % de los hogares**, con un intervalo aproximado del 95 % de **0,97 % a 1,21 %**. Procede de 78.654 hogares muestrales, sin respuestas faltantes en esa pregunta. La estimación nacional y las regionales usan `expr` y linealización de Taylor con estratos y conglomerados; el intervalo expresa incertidumbre muestral, no todos los posibles errores de medición. La [nota oficial de uso de CASEN][casen-nota] distingue estos dominios del uso descriptivo comunal.

<figure style="width:100%">
  <div role="region" aria-label="Proporción de hogares que declaran sitio propio compartido: Chile y 16 regiones con intervalos aproximados; Valparaíso y Viña del Mar como casos exploratorios sin IC." tabindex="0" style="max-width:100%;overflow-x:auto;border:1px solid currentColor;border-radius:.4rem">
    <img class="avaluos-ii-monetary-light" width="1152" height="1286" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/casen-shared-site-es.svg" alt="Proporción de hogares que declaran sitio propio compartido: Chile y 16 regiones con intervalos aproximados; Valparaíso y Viña del Mar como casos exploratorios sin IC." loading="lazy">
    <img class="avaluos-ii-monetary-dark" width="1152" height="1286" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/casen-shared-site-es-dark.svg" alt="Proporción de hogares que declaran sitio propio compartido: Chile y 16 regiones con intervalos aproximados; Valparaíso y Viña del Mar como casos exploratorios sin IC." loading="lazy">
  </div>
  <figcaption>CASEN 2024. Los porcentajes describen hogares, no viviendas por sitio. Los dos casos comunales no son representativos. Desplaza horizontalmente o abre el SVG para ampliar; los valores están en la tabla siguiente. <a href="/assets/images/avaluos-ii/casen-shared-site-es.svg">SVG</a> · <a href="/assets/images/avaluos-ii/casen-shared-site-es-dark.svg">SVG oscuro</a>.</figcaption>
</figure>

{% include casen-shared-site-table.html lang='es' %}

Valparaíso y Viña del Mar muestran **9,27 % y 8,60 %**, respectivamente, en el cálculo comunal ponderado con `expc`. Son señales exploratorias: las elegí después de observar su discrepancia y estos resultados **no son estimaciones representativas de cada comuna**. La presencia de un factor comunal no les confiere esa propiedad. La tabla conserva tamaños muestrales y faltantes; las once comunas sin muestra se registran como dato ausente, nunca como cero.

La deducción es limitada pero útil: contar viviendas y contar roles puede producir diferencias aun con un registro correcto. El patrón observado en estas dos comunas vuelve pertinente examinar los sitios compartidos. La hipótesis es que expliquen una parte de su discrepancia, junto con campamentos, destinos agrícolas, fechas y eventuales omisiones. La evidencia que permitiría distinguir estas explicaciones es una muestra representativa que enlace viviendas con sitios y roles; la hipótesis perdería fuerza como explicación material si ese cruce mostrara que su aporte es pequeño bajo un criterio fijado antes de medirlo.

**No descuento este porcentaje de las barras ni de los escenarios en pesos.** Describe una tenencia de hogares, no la proporción de viviendas que sobran en el recuento. Además, no cubre todas las formas de compartir sitio y podría superponerse con campamentos. Restarlo ahora produciría una precisión aparente y podría contar dos veces la misma explicación.
{: .notice--info}

<details markdown="1">
<summary>Por qué no convertir directamente el porcentaje CASEN en viviendas por sitio</summary>

En un ejemplo puramente hipotético, si una proporción $$p_v$$ de las **viviendas** perteneciera a sitios con exactamente dos viviendas y las restantes ocuparan sitios individuales, habría $$V(1-p_v/2)$$ sitios. La razón roles/sitios sería $$R_2=R_1/(1-p_v/2)$$, con $$R_1=\text{roles}/V$$. Por ejemplo, un $$p_v=0{,}20$$ supuesto equivaldría a 90 sitios por cada 100 viviendas. La proporción CASEN de **hogares** no es ese parámetro: la fórmula ilustra el mecanismo, pero no estima un ajuste fiscal.

</details>

## Segunda cucharada: distinguir una brecha grande de una revisión con interés tributario

El tamaño de la diferencia no basta para anticipar su relevancia tributaria. Para añadir contexto, observo los avalúos de los **predios habitacionales que sí están registrados**: su media, su mediana y la proporción que supera el monto exento general.

En el primer semestre de 2026, ese monto era de **60.030.710 pesos**, según el [ejemplo oficial del SII][sii-ejemplo]. Comparo cada avalúo con el umbral del mismo período. Superarlo no basta para determinar una contribución exigible: deben revisarse los beneficios y las exenciones aplicables.

El avalúo fiscal [no es el precio de venta][sii-comercial]. Considera tanto el terreno como la construcción y sus características. Por eso, **materiales aceptables no significan avalúo alto**: una vivienda de buena materialidad en suelo de menor valor puede quedar bajo el monto exento, mientras otra más modesta en suelo caro puede superarlo. El SII explica los componentes de esta valoración en su [guía de avalúo fiscal][sii-avaluo].

La media puede subir por unos pocos valores muy altos. La mediana muestra el centro de la distribución, y el porcentaje sobre el umbral indica qué tan extendida está esa condición. Son resúmenes complementarios de los mismos predios, no pruebas independientes de omisión.

### Un filtro explícito: residuo positivo y mediana sobre el monto exento

En la base analizada, estas **15 comunas** cumplen ambas condiciones. Están ordenadas por residuo, de mayor a menor. **La materialidad se muestra como escenario, pero no interviene en la selección.**

| Comuna | Residuo | Escenario aceptable | Avalúo mediano, millones de pesos | Roles sobre el umbral |
|---|---:|---:|---:|---:|
| Iquique | 18.949 | 16.964 | 60,24 | 50,4 % |
| Pucón | 13.707 | 12.205 | 63,71 | 53,4 % |
| Puerto Varas | 8.693 | 7.997 | 61,61 | 51,1 % |
| Pirque | 4.883 | 4.090 | 91,85 | 62,2 % |
| Algarrobo | 3.201 | 2.876 | 79,72 | 71,1 % |
| Santo Domingo | 2.765 | 2.516 | 112,00 | 75,9 % |
| Lo Barnechea | 2.300 | 2.202 | 290,03 | 85,6 % |
| Huechuraba | 2.297 | 2.118 | 69,73 | 52,5 % |
| Concón | 2.005 | 1.888 | 91,82 | 73,3 % |
| San Miguel | 1.984 | 1.927 | 63,62 | 55,2 % |
| Zapallar | 1.948 | 1.723 | 182,98 | 75,0 % |
| La Reina | 1.532 | 1.488 | 122,56 | 83,3 % |
| Papudo | 1.213 | 1.092 | 69,05 | 58,1 % |
| Providencia | 918 | 908 | 100,40 | 82,6 % |
| Las Condes | 542 | 538 | 139,18 | 92,0 % |

*El escenario aceptable combina tipo y materiales, con resultados redondeados a unidades. Los avalúos y porcentajes corresponden exclusivamente a roles habitacionales registrados.*

Iquique combina un residuo elevado con una mediana apenas sobre el umbral: **60,24 millones de pesos**. Su media, de **73,84 millones**, no describe la situación de todos sus predios. Lo Barnechea muestra otra combinación: un residuo menor, de **2.300**, pero una mediana de **290,03 millones** y un **85,6 %** de roles sobre el monto exento.

El contraste sirve para formular una pregunta: **si se encontraran inmuebles omitidos y fueran comparables a los registrados, ¿qué orden de magnitud tendría el impuesto asociado?** Para responderla construyo dos escenarios; ninguno estima cuántos inmuebles aparecerán.

La condición de semejanza es la más difícil. Lo que falta en un registro puede diferir sistemáticamente de lo que entró: construcciones más pequeñas, viviendas en predios agrícolas o inmuebles bajo un rol matriz. Trasladarles el perfil de avalúos observado podría introducir un sesgo si los inmuebles ausentes tienen un perfil distinto. Este filtro tampoco mide la discrepancia proporcional ni el costo de investigar cada comuna; es un punto de partida, no una priorización óptima demostrada.

### Dar escala al problema: dos escenarios de impuesto teórico

Primero calculo, **predio por predio**, el impuesto general que resultaría de aplicar a su avalúo los tramos del primer semestre de 2026. Después obtengo la media y la mediana comunales de esos resultados, **incluidos los ceros bajo el monto exento**. Aplicar una tasa al avalúo promedio no daría necesariamente el mismo resultado: las exenciones y los tramos cambian el cálculo.

El modelo sigue los parámetros del [ejemplo oficial del SII][sii-ejemplo]: monto exento de **$60.030.710**, cambio de tramo en **$214.395.361** y tasas anuales de **0,893 % y 1,042 %**, respectivamente. Es un **impuesto general teórico anual equivalente**, manteniendo fijos los parámetros de ese semestre. Excluye aseo, sobretasas y beneficios individuales; no reproduce los giros efectivos ni la recaudación de todo 2026.

Luego multiplico el residuo bajo el supuesto de campamentos por cada estadístico:

| Escenario | Operación | Lectura |
|---|---|---|
| Con la mediana | Residuo × impuesto teórico mediano por predio | Aplica a cada unidad el valor central del impuesto modelado |
| Con la media | Residuo × impuesto teórico medio por predio | Aplica el promedio, sensible a los avalúos altos |

**Son dos referencias de escala, no un intervalo de confianza ni límites inferior y superior garantizados.** La mediana no es un impuesto mínimo: si más de la mitad de los predios queda bajo el monto exento, puede ser cero aunque la media sea positiva. Aquí se conservan las quince comunas del filtro anterior y se ordenan por el escenario con la media.

<figure style="width:100%">
  <div role="region" aria-label="Escenarios de impuesto general teórico anual equivalente para las quince comunas con residuo positivo y avalúo mediano sobre el monto exento; comparación de media y mediana." tabindex="0" style="max-width:100%;overflow-x:auto;border:1px solid currentColor;border-radius:.4rem">
    <img class="avaluos-ii-monetary-light" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/monetary-top15-es.svg" alt="Escenarios de impuesto general teórico anual equivalente para las quince comunas con residuo positivo y avalúo mediano sobre el monto exento; comparación de media y mediana." loading="lazy">
    <img class="avaluos-ii-monetary-dark" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/monetary-top15-es-dark.svg" alt="Escenarios de impuesto general teórico anual equivalente para las quince comunas con residuo positivo y avalúo mediano sobre el monto exento; comparación de media y mediana." loading="lazy">
  </div>
  <figcaption>Millones de pesos bajo el supuesto de que cada unidad del residuo correspondiera a un nuevo predio comparable. Los montos son hipotéticos; no son deuda constatada ni ingresos municipales retenidos. Desplaza horizontalmente o abre el SVG para ampliar; los valores están en la tabla siguiente. <a href="/assets/images/avaluos-ii/monetary-top15-es.svg">SVG</a> · <a href="/assets/images/avaluos-ii/monetary-top15-es-dark.svg">SVG oscuro</a>.</figcaption>
</figure>

{% include avaluos-ii-monetary-es.html %}

Iquique ilustra por qué conviene mostrar ambas referencias. Con sus **18.949** unidades residuales, el escenario con la mediana alcanza **$36 millones** anuales equivalentes; con la media, **$4.309 millones**. La separación es grande: el avalúo mediano apenas supera el monto exento y genera un impuesto teórico de unos **$1.912 por predio**, mientras la media incorpora el aporte de avalúos más altos. Presentar solo uno de los dos ocultaría esa diferencia de perfil.

En Lo Barnechea, las **2.300** unidades residuales producen **$4.983 millones con la mediana y $6.669 millones con la media**. Bajo este modelo, encabeza el orden monetario pese a tener una brecha física mucho menor que Iquique. No se ha descubierto esa recaudación faltante: se ha mostrado qué escala tendría el impuesto si se confirmaran nuevos predios comparables. Ese contraste vuelve concreta la razón para revisar las comunas donde coinciden una discrepancia pendiente y avalúos elevados.

La comparación completa supone **un nuevo predio comparable por cada unidad residual**: llamo $$q=1$$ a ese supuesto. El visor permite reducirlo a $$q=0{,}5$$ o $$q=0{,}25$$, con lo que los montos caen a la mitad o a un cuarto. Este factor representa la fracción hipotética del residuo que daría lugar a nuevos predios comparables; **no es una probabilidad estimada, una tasa de cobro ni la proporción de predios que paga contribuciones**. Los ceros tributarios ya están incluidos en ambos estadísticos. Tampoco se vuelve a descontar la materialidad.

## Tercera cucharada: del escenario comunal a la comprobación predial

La comparación comunal permite elegir dónde mirar. Para comprobar una omisión con efectos tributarios hay que bajar al predio: **identificar la construcción, encontrar su relación con uno o más roles y reconstruir sus fechas**. La revisión debe admitir tanto una omisión como una explicación que la descarte.

| Posible explicación | Qué habría que contrastar | Qué debilitaría esa explicación |
|---|---|---|
| Predio o construcción omitidos | Ubicación, antecedentes de terreno y construcción, roles y expediente catastral | El inmueble ya está incorporado correctamente, incluso bajo otro rol o destino |
| Avalúo desactualizado | Superficie y características construidas frente al detalle catastral y sus fechas | El avalúo ya incorpora esas características |
| Diferencia de unidades o períodos | Viviendas por predio, roles matrices, destinos agrícolas, copropiedad y fechas comparables | La discrepancia persiste después de conciliar unidades y períodos |
| Error de fuente o procesamiento | Integridad del extracto, claves territoriales y reproducción independiente | El resultado se reproduce con fuentes y cruces independientes |

**Incorporar un predio y actualizar una construcción no son lo mismo.** El SII dispone de un [procedimiento de inclusión de bienes raíces][sii-inclusion]. También contempla modificaciones del avalúo. Una ampliación puede aumentar el valor de un rol existente sin crear otro: la diferencia entre viviendas y roles no detecta por sí sola toda desactualización del catastro.

### Qué falta para pasar del escenario a una obligación comprobada

Los escenarios anteriores dan escala al supuesto, pero para cuantificar obligaciones efectivamente omitidas hay que identificar los predios, verificar sus fechas y avalúos, y aplicar los beneficios y exenciones que les correspondan. También se necesita información compatible y conciliada de los giros para contrastar el impuesto teórico con el efectivo.

El [diccionario catastral del SII][sii-estructura] define el campo semestral disponible como contribución **con aseo**. No se lo usa como impuesto neto. Los cuadros comunales oficiales revisados distinguen componentes, pero abarcan otros destinos no agrícolas: **dividir ese total por roles habitacionales produciría un promedio de universos incompatibles**. La [auditoría de fuentes](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) conserva este límite; el cálculo normativo no lo concilia ni lo elimina.

Determinar un impuesto, girarlo y recaudarlo son etapas distintas. El SII determina los avalúos y giros; la [Tesorería General de la República recauda][tgr-impuestos]. Además, la distribución mediante el [Fondo Común Municipal][sii-fcm] impide equiparar el impuesto asociado a una comuna con ingresos retenidos íntegramente por su municipio.

La [guía de Grote y Wen (2024, pp. 16–18)][fmi-guia] ayuda a ordenar el problema: distingue cobertura, valoración y cobro, y propone contrastar cartografía, terreno y registros. Sirve para diseñar una verificación, no para importar un coeficiente de recaudación a estas comunas.

<aside class="notice--info" markdown="1">
**Detrás del análisis: Python y geomática reproducible**

Python conecta los agregados catastrales, censales y territoriales; Parquet conserva las tablas en formato columnar y Matplotlib produce estas figuras en SVG y PNG, con tipografía y paletas para ambos modos de lectura. Cada gráfico parte de una tabla verificable: la imagen sirve para leer el patrón y la tabla para examinar los valores. El visor mantiene ECharts para la exploración interactiva y las capas cartográficas para revisar el territorio.

Para CASEN, R abre la base original y entrega a Python las columnas necesarias mediante una tubería en memoria. Python calcula las estimaciones y la varianza de diseño; fixtures algebraicos y una comparación acotada con Julia contrastan la implementación. Separar extracción, cálculo, representación y controles facilita llevar trabajo semejante a flujos de cómputo de mayor escala. **Esta ejecución es local: no constituye un benchmark ni una ejecución demostrada en un clúster HPC.** El [método y la procedencia](/catastro_sii_brecha/data/casen-shared-site/method.md) permiten revisar qué se hizo efectivamente.
</aside>

## Cierre: que la diferencia tenga una explicación

Las comunas donde persiste la diferencia y los predios registrados presentan avalúos altos ofrecen un punto de partida para revisar el catastro. Los escenarios en pesos muestran por qué una brecha más pequeña puede merecer atención tributaria. Si se confirman inmuebles comparables omitidos, corresponde determinar sus efectos; si la diferencia se resuelve con roles existentes, destinos o fechas, la hipótesis de omisión pierde fuerza. El resultado justifica investigar, pero no permite atribuir negligencia ni falta de cobro a un organismo.

En la próxima entrega exploraré el **Continuo de Construcciones Urbanas (CCU)** para contrastar la huella construida. Antes de atribuir un atraso administrativo, habrá que verificar sus fuentes y reconstruir cuándo ocurrió cada cambio.

[Explorar el diagnóstico](/catastro_sii_brecha/#brecha-contribuciones) · [Descargar CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv).

<details markdown="1">
<summary>Notas metodológicas: fuentes, cortes y límites pendientes</summary>

**Procedencia y cobertura.** El espejo catastral se descargó el 24 de julio de 2026 y corresponde al primer semestre de ese año. No es una descarga directa del SII ni un corte de septiembre. Antártica y Trehuaco carecen de extracto y se mantienen como faltantes, no como comunas sin predios habitacionales.

**Totales todavía no conciliados.** El control [SII por destino][sii-destino] citado informa 6.056.150 predios habitacionales; el extracto reúne 6.054.808. Las [planillas MINVU de parque habitacional][minvu-parque] citadas para 2026S1 informan 6.057.949, incluidos 1.342 de Trehuaco. La diferencia entre el SII y el extracto es de 1.342, pero entre MINVU y el extracto alcanza 3.141. Incorporar los 1.342 de Trehuaco no concilia ambos controles: todavía quedan 1.799 predios de diferencia respecto del total MINVU. No se atribuye esta discrepancia a una causa no comprobada ni se sustituyen silenciosamente los totales.

**Dos cortes de campamentos.** El informe [MINVU publicado el 8 de julio de 2026][minvu-campamentos], con información referida a 2024, registra 1.373 campamentos, 81.993 viviendas ocupadas y 77.399 hogares. La capa CNC 2026 utilizada en este procesamiento contiene 1.345 polígonos y suma 71.760 en el campo `HOGARESCEN`, con 222 polígonos sin dato. Son universos y cortes diferentes. Interpretar ese campo como hogares censales es una decisión provisional, apoyada en su nombre y la documentación disponible, no en un diccionario específico de la capa. El descuento depende de ella.

**Definición de materialidad.** Se utiliza el código del manual INE, cuya clasificación no coincide por completo con la descripción en prosa: para materialidad aceptable, esta última admite algunas paredes recuperables, mientras el código exige materiales aceptables en los tres componentes. El escenario combina ese criterio con el tipo aceptable de vivienda. Se conservan variantes con materiales completos y con la categoría más amplia de no irrecuperables; son análisis de sensibilidad, no intervalos de confianza. El procesamiento registra 4.388 viviendas ocupadas con información incompleta.

**Fórmula monetaria y unidad.** Para un avalúo $$A$$, monto exento $$E=60\,030\,710$$ y cambio de tramo $$T=214\,395\,361$$, se calcula:

$$
\begin{aligned}
g(A)={}&0{,}00893\max(\min(A,T)-E,0)\\
       &+0{,}01042\max(A-T,0).
\end{aligned}
$$

Se agregan los resultados por comuna, incluidos los ceros, antes de multiplicar cada estadístico por el residuo positivo y por $$q$$. No se aplica el impuesto al avalúo medio, no se filtran solo los predios afectos y no se anualiza otra vez una tasa que ya es anual. El avalúo exento individual del extracto no sustituye al monto exento general en este modelo. Por ello el cálculo no representa beneficios particulares ni pretende reconstruir el giro de cada predio. La media y la mediana describen los predios registrados; extrapolarlas al residuo requiere el supuesto de comparabilidad.

**Correcciones del procesamiento.** Se corrigió la homologación territorial de Coyhaique, Aysén y Chile Chico. El conteo de viviendas irrecuperables pasó de 73.338 a 72.642 —696 menos— al aplicar primero la exclusión de no respuesta del código oficial. Esa corrección no modifica la diferencia viviendas–roles ni el descuento por campamentos. La base histórica innominada 2011–2021 no interviene en el cálculo actual.

**Trazabilidad.** El [método](/catastro_sii_brecha/data/fiscal-gap/method.md), la [auditoría](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) y los [datos comunales](/catastro_sii_brecha/data/fiscal-gap/communes.json) son las referencias del procesamiento. Solo se publican agregados comunales.

</details>

## Fuentes y referencias

Ministerio de Desarrollo Social y Familia. 2026. *CASEN 2024: cuestionario y nota de uso de bases de datos*. Tenencia y hogar principal, pp. 79 y 83 del [cuestionario][casen-cuestionario]; factores de expansión y dominios en la [nota de uso][casen-nota]. Consultados el 12 de septiembre de 2026.

Grote, Martin, y Jean-François Wen. 2024. *How to Design and Implement Property Tax Reforms*. How to Note 2024/006. Fondo Monetario Internacional, septiembre. [Texto completo][fmi-guia].

Instituto Nacional de Estadísticas (INE). 2025. *Manual de uso de microdatos censales: Censo de Población y Vivienda 2024*. Indicadores viv04–viv06, 103–106. [Manual][ine-manual].

Ministerio de Vivienda y Urbanismo (MINVU), Centro de Estudios de Ciudad y Territorio. 2026. *Caracterización de campamentos en Censo 2024*. Publicado el 8 de julio. Véanse los resultados generales y la tabla 1, 4–5. [Informe][minvu-campamentos].

Servicio de Impuestos Internos (SII). «De avalúo fiscal a contribuciones: paso a paso», ejemplo del primer semestre de 2026; «¿Qué es un avalúo fiscal?»; «¿El avalúo fiscal corresponde a una tasación comercial de la propiedad?», actualización del 8 de abril de 2026; «¿Cómo regularizo una propiedad que no tiene rol de avalúo?», actualización del 7 de abril de 2026; y «¿Para qué sirve el pago del impuesto territorial?». [Cálculo][sii-ejemplo], [avalúo][sii-avaluo], [distinción del valor comercial][sii-comercial], [inclusión][sii-inclusion] y [distribución municipal][sii-fcm]. Para construcciones no regularizadas, véanse los [documentos requeridos para tasación][sii-no-regularizadas].

Servicio de Impuestos Internos (SII). S. f. *Estructura de archivo para Detalle Catastral de Bienes Raíces*. Información básica de la serie no agrícola, campos 5–8 y tabla de destinos, p. 1. [Diccionario][sii-estructura].

Tesorería General de la República (TGR). S. f. «Impuestos y tipos de impuestos». Centro de Ayuda TGR. [Fuente][tgr-impuestos].

*Fuentes externas anteriores consultadas el 11 de septiembre de 2026. Los resultados del procesamiento y sus correcciones deben leerse junto con las notas metodológicas.*

[ine-manual]: https://censo2024.ine.gob.cl/wp-content/uploads/2025/12/manual_uso_microdatos_censo2024.pdf
[minvu-campamentos]: https://catalogo.minvu.cl/cgi-bin/koha/opac-retrieve-file.pl?id=7e816aa9c26af8904eab01badfbfc6e6
[minvu-parque]: https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/
[sii-ejemplo]: https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf
[sii-estructura]: https://www.sii.cl/bbrr/descargas/estructura_detalle_catastral.pdf
[sii-comercial]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_8124.htm
[sii-avaluo]: https://www.sii.cl/destacados/impuesto_territorial/avaluo_fiscal.html
[sii-inclusion]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_1947.htm
[sii-fcm]: https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html
[sii-no-regularizadas]: https://www.sii.cl/servicios_online/1048-doctos_requeridos-2573.html
[sii-destino]: https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html
[tgr-impuestos]: https://ayuda.tgr.gob.cl/ayuda/impuestos/impuestos-y-tipos-de-impuestos
[fmi-guia]: https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf

[casen-cuestionario]: https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf
[casen-nota]: https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf

```


## _posts/2026-09-11-avaluos-ii-brecha-residencial-en.md
```
---
layout: single
classes: [avaluos-ii-editorial]
title: "Property assessments in 3 spoonfuls II: where to review the residential gap"
subtitle: "Informal settlements, construction materials and assessed values: from differences by commune to a property-level review"
date: 2026-09-11 00:00:00 -0300
categories: [datos, territorio]
tags: [catastro-sii, census-2024, property-tax, open-data, inequality]
author: clabra
lang: en
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: true
editorial_status: hypothetical-property-tax-scenario
description: "The Census–SII gap, informal settlements and residential assessments: theoretical tax scenarios in Chilean pesos to guide property-level review, with explicit assumptions."
excerpt: "A persistent discrepancy alongside high assessed values in registered properties warrants a cadastral review. Establishing omissions and their tax implications requires identifying the properties."
header:
  overlay_image: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/hero-1600x900.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/og-1200x630.webp
  og_image_alt: Residential city at night and conceptual cadastral polygons to reconcile.
  overlay_image_mobile: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/hero-mobile-800x450.webp
  teaser_mobile: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/teaser-mobile-640x360.webp
math: true
toc: true
toc_sticky: true
comments: true
visual_id: avaluos-ii
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
---

In the [first property-assessment post](/en/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/), changing the denominator changed the map. Now I am interested in a question that comes before calculating tax: **if the Census counts more dwellings than the SII's residential cadastral records, where should a review begin?**

The tax implications deserve closer attention when the discrepancy persists in communes whose registered properties have high assessed values. If a review found omitted properties comparable to them, the next step would be to establish whether registering them or updating their assessments creates a tax liability.

I examine that difference alongside informal settlements, construction materials and assessed values to guide the search. There are three steps: understand what we are subtracting, gauge its possible tax significance through scenarios in pesos, and specify the evidence needed to establish it.

**How to read the bars.** They guide a review; they do not count omitted properties or outstanding property-tax liabilities.
{: .notice--info}

## First spoonful: measure the difference without treating it as an omission

I compare **all private dwellings in the 2024 Census**, occupied and vacant, with **residential cadastral records—property-use code H—for the first half of 2026**. The first count concerns dwellings; the second concerns properties registered for tax purposes. SII is Chile's tax authority, and a commune is a local administrative area.

There is no one-to-one correspondence. A property may contain several dwellings, and a dwelling may be on an agricultural property excluded by the residential filter. The dates also differ. Dwellings minus records is therefore a **difference between counts**, not a count of “dwellings without a cadastral record.”

The bar is constructed in three steps:

| Step | Calculation | What it represents |
|---|---|---|
| Initial difference | Census dwellings minus residential cadastral records | The gap between the two counts |
| Informal-settlement scenario | Subtract the available household count, assuming one unit of the difference per household | The residual under that assumption |
| Construction-materials scenario | Apply the commune's share of dwellings with acceptable type and materials to the residual | A hypothetical composition of the residual |

### Informal settlements: how much the difference changes under an assumption

In Alto Hospicio, the initial difference is **15,368**. Subtracting the **9,136** households that the processing assigns to settlements with available data leaves **6,232** units: a **59.4%** reduction. In Puerto Montt, the same exercise reduces the difference by just **2.2%**.

| Commune | Initial difference | Households with data | Residual | Reduction |
|---|---:|---:|---:|---:|
| Alto Hospicio | 15,368 | 9,136 | 6,232 | 59.4% |
| Antofagasta | 21,755 | 7,537 | 14,218 | 34.6% |
| Viña del Mar | 24,030 | 8,014 | 16,016 | 33.3% |
| Valparaíso | 32,533 | 2,572 | 29,961 | 7.9% |
| Puerto Montt | 29,036 | 632 | 28,404 | 2.2% |

This deduction is a sensitivity test, not an established explanation. Several households may share a dwelling, the land may have a parent property record, and dates may differ. The layer also contains **222 polygons without a count**: missing data do not mean an absence of households. The interpretation of its `HOGARESCEN` field is detailed in the methodological notes.

The deduction does not represent a tax exemption either: it is an analytical assumption. The SII provides for [the assessment of buildings whose legal status has not been regularised][sii-no-regularizadas]; each property's circumstances must be checked.

In aggregate, the sum of positive differences across communes falls from **1,588,449 to 1,516,689**, a **4.52%** reduction. This is not the net national difference: communes with negative balances do not offset those with positive ones. The result shows that the assumption changes some communes substantially and others very little; it does not establish what share of the discrepancy informal settlements explain.

### Construction materials: describe a scenario, not assess property values

The second assumption asks how the residual would be distributed if it had the same composition as the dwellings observed in the commune. I use a criterion requiring **an acceptable dwelling type and acceptable wall, roof and floor materials simultaneously**, following the code in the [INE microdata manual, indicators viv04 and viv05, pp. 103–105][ine-manual].

In the processed data, **5,774,146 of 6,408,172** occupied private dwellings with residents present meet this criterion. The proportion is calculated for each commune, retaining incomplete observations in the denominator but outside the acceptable group.

For example, a residual of 9,000 units and an acceptable share of 80% would yield **7,200 units in that scenario and 1,800 in the remainder**. This has not located 7,200 dwellings: it has applied a known proportion to a difference of unknown composition.

The extrapolation has two limitations. Construction materials are observed in occupied dwellings with residents present, whereas the initial difference also includes vacant dwellings and those whose residents were absent. In addition, any dwellings missing from the cadastre could differ from those observed. **The “remainder” is not equivalent to irrecoverable dwellings either**: it includes both those that do not meet the criterion and incomplete observations.

I do not add another deduction for irrecoverable dwellings, because their overlap with informal settlements is unknown. Nor do I multiply this scenario by the share of records above the exemption threshold: we do not know the joint distribution of the two characteristics.

<figure style="width:100%">
  <div role="region" aria-label="Fifteen communes with the largest residual under the informal-settlement assumption. Each bar preserves the initial difference and separates the assumed deduction, the acceptable-type-and-materials scenario and the remainder." tabindex="0" style="max-width:100%;overflow-x:auto;border:1px solid currentColor;border-radius:.4rem">
    <img class="avaluos-ii-monetary-light" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/gap-top15-en.svg" alt="Fifteen communes with the largest residual under the informal-settlement assumption. Each bar preserves the initial difference and separates the assumed deduction, the acceptable-type-and-materials scenario and the remainder." loading="lazy">
    <img class="avaluos-ii-monetary-dark" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/gap-top15-en-dark.svg" alt="Fifteen communes with the largest residual under the informal-settlement assumption. Each bar preserves the initial difference and separates the assumed deduction, the acceptable-type-and-materials scenario and the remainder." loading="lazy">
  </div>
  <figcaption>Scenarios for the composition of the difference; these are not identified omitted dwellings. Scroll horizontally or open the SVG to zoom; values appear in the following table. <a href="/assets/images/avaluos-ii/gap-top15-en.svg">SVG</a> · <a href="/assets/images/avaluos-ii/gap-top15-en-dark.svg">SVG dark</a>.</figcaption>
</figure>

{% include avaluos-ii-top-en.html %}

**How to read the chart.** The total length preserves the initial difference; its segments distinguish the assumed settlement deduction and the hypothetical composition of the residual. The fifteen communes are ranked by that residual, not by construction materials or assessed values. The tax-related selection in the second spoonful uses a different filter.

The [viewer lets you explore each commune and consult the complete table](/catastro_sii_brecha/#brecha-contribuciones). The [Valparaíso and Puerto Montt annex](/catastro_sii_brecha/#catastro-anexo) overlays properties, neighbourhood units and informal settlements: it helps reveal spatial relationships, but does not by itself identify omitted dwellings.

### Several dwellings on one site: another explanation worth testing

Two dwellings can share a plot and be covered by one property-tax record. The Census would then count two dwellings without a property necessarily being absent from the tax register. This mechanism may contribute to the difference; measuring its contribution requires linking **dwellings, sites and property records**. The public dictionary examined and the [Census microdata manual, pp. 17–20][ine-manual], link dwellings, households and people, but do not provide a shared site or property-record identifier for this reconciliation. Several households within one dwelling are not the same as several dwellings on one site.

CASEN 2024 provides a narrower signal. Categories 3 and 4 of its tenure question identify households reporting **an owned site shared with other dwellings**, either fully paid or being paid for. They do not ask how many dwellings occupy the site. I calculate their share among **all households with valid answers**, including renters and other tenure arrangements, using one household head per household. The principal-household question is conditional; applying it as a filter to the entire dataset would incorrectly remove households in single-household dwellings. See the [official questionnaire, pp. 79 and 83][casen-cuestionario].

The national result is **1.09% of households**, with an approximate 95% interval of **0.97% to 1.21%**. It comes from 78,654 sampled households, with no missing answers to this question. National and regional estimates use `expr` and Taylor linearization with strata and clusters; the interval expresses sampling uncertainty, rather than every possible measurement error. The [official CASEN data-use note][casen-nota] distinguishes these domains from descriptive use at commune level.

<figure style="width:100%">
  <div role="region" aria-label="Share of households reporting an owned shared site: Chile and 16 regions with approximate intervals; Valparaíso and Viña del Mar as exploratory cases without confidence intervals." tabindex="0" style="max-width:100%;overflow-x:auto;border:1px solid currentColor;border-radius:.4rem">
    <img class="avaluos-ii-monetary-light" width="1152" height="1286" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/casen-shared-site-en.svg" alt="Share of households reporting an owned shared site: Chile and 16 regions with approximate intervals; Valparaíso and Viña del Mar as exploratory cases without confidence intervals." loading="lazy">
    <img class="avaluos-ii-monetary-dark" width="1152" height="1286" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/casen-shared-site-en-dark.svg" alt="Share of households reporting an owned shared site: Chile and 16 regions with approximate intervals; Valparaíso and Viña del Mar as exploratory cases without confidence intervals." loading="lazy">
  </div>
  <figcaption>CASEN 2024. Percentages describe households, not dwellings per site. The two commune cases are not representative. Scroll horizontally or open the SVG to zoom; values appear in the following table. <a href="/assets/images/avaluos-ii/casen-shared-site-en.svg">SVG</a> · <a href="/assets/images/avaluos-ii/casen-shared-site-en-dark.svg">SVG dark</a>.</figcaption>
</figure>

{% include casen-shared-site-table.html lang='en' %}

Valparaíso and Viña del Mar show **9.27% and 8.60%**, respectively, in the commune calculation weighted by `expc`. These are exploratory signals: I selected the two communes after observing their discrepancy, and these results **are not representative estimates for each commune**. A commune weight does not confer that property. The table retains sample sizes and missingness; the eleven communes outside the sample are recorded as missing data, never zero.

The deduction is limited but useful: dwelling and property-record counts may differ even with an accurate register. The observed pattern in these two communes makes shared sites worth investigating. The hypothesis is that they explain part of the discrepancy, alongside informal settlements, agricultural land uses, timing and possible omissions. A representative sample linking dwellings to sites and property records would discriminate between these explanations; the hypothesis would weaken as a material explanation if this linkage showed a small contribution against a criterion set before measurement.

**I do not subtract this percentage from the bars or monetary scenarios.** It describes household tenure, not the share of excess dwellings in a count. It also misses other ways of sharing sites and may overlap with informal settlements. Subtracting it now would introduce apparent precision and could count the same explanation twice.
{: .notice--info}

<details markdown="1">
<summary>Why the CASEN percentage cannot directly become dwellings per site</summary>

In a purely hypothetical example, if a share $$p_v$$ of **dwellings** belonged to sites with exactly two dwellings and all remaining dwellings occupied individual sites, there would be $$V(1-p_v/2)$$ sites. The property-records/sites ratio would be $$R_2=R_1/(1-p_v/2)$$, where $$R_1=\text{property records}/V$$. For example, an assumed $$p_v=0.20$$ would mean 90 sites for every 100 dwellings. The CASEN **household** share is not that parameter: the formula illustrates the mechanism but does not estimate a fiscal adjustment.

</details>

## Second spoonful: distinguish a large gap from a review with tax implications

The size of the difference alone does not establish its potential tax significance. For context, I examine the assessed values of **residential properties that are already registered**: their mean, median and the share above the general exemption threshold.

In the first half of 2026, that threshold was **60,030,710 Chilean pesos**, according to the [SII's official example][sii-ejemplo]. I compare each assessed value with the threshold for the same period. Exceeding it is not enough to establish an enforceable property-tax liability: applicable benefits and exemptions must also be checked.

A property's assessed value for tax purposes [is not its sale price][sii-comercial]. It takes account of both the land and the building and their characteristics. Therefore, **acceptable materials do not imply a high assessed value**: a dwelling with good construction materials on less valuable land may fall below the exemption threshold, while a more modest one on expensive land may exceed it. The SII explains the components of this valuation in its [guide to assessed values][sii-avaluo].

A few very high values can raise the mean. The median shows the centre of the distribution, while the share above the threshold indicates how widespread that condition is. These are complementary summaries of the same properties, not independent evidence of omission.

### An explicit filter: a positive residual and a median above the exemption threshold

In the dataset analysed, these **15 communes** meet both conditions. They are ranked by residual, from largest to smallest. **Construction materials are shown as a scenario, but do not determine the selection.**

| Commune | Residual | Acceptable scenario | Median assessed value, million Chilean pesos | Records above the threshold |
|---|---:|---:|---:|---:|
| Iquique | 18,949 | 16,964 | 60.24 | 50.4% |
| Pucón | 13,707 | 12,205 | 63.71 | 53.4% |
| Puerto Varas | 8,693 | 7,997 | 61.61 | 51.1% |
| Pirque | 4,883 | 4,090 | 91.85 | 62.2% |
| Algarrobo | 3,201 | 2,876 | 79.72 | 71.1% |
| Santo Domingo | 2,765 | 2,516 | 112.00 | 75.9% |
| Lo Barnechea | 2,300 | 2,202 | 290.03 | 85.6% |
| Huechuraba | 2,297 | 2,118 | 69.73 | 52.5% |
| Concón | 2,005 | 1,888 | 91.82 | 73.3% |
| San Miguel | 1,984 | 1,927 | 63.62 | 55.2% |
| Zapallar | 1,948 | 1,723 | 182.98 | 75.0% |
| La Reina | 1,532 | 1,488 | 122.56 | 83.3% |
| Papudo | 1,213 | 1,092 | 69.05 | 58.1% |
| Providencia | 918 | 908 | 100.40 | 82.6% |
| Las Condes | 542 | 538 | 139.18 | 92.0% |

*The acceptable scenario combines dwelling type and materials, with results rounded to whole units. Assessed values and percentages refer exclusively to registered residential properties.*

Iquique combines a large residual with a median just above the threshold: **60.24 million Chilean pesos**. Its mean of **73.84 million** does not describe every property's circumstances. Lo Barnechea shows a different combination: a smaller residual of **2,300**, but a median of **290.03 million** and **85.6%** of records above the exemption threshold.

The contrast helps frame a question: **if omitted properties were found and were comparable to registered ones, what order of magnitude would the associated tax have?** I construct two scenarios to address that question; neither estimates how many properties would be found.

Comparability is the hardest condition to establish. What is missing from a register may differ systematically from what entered it: smaller buildings, dwellings on agricultural properties or properties covered by a parent record. Applying the observed assessment profile to them could introduce bias if the absent properties have a different profile. This filter does not measure the proportional discrepancy or the cost of investigating each commune either; it is a starting point, not a demonstrably optimal prioritisation.

### Giving the problem a scale: two theoretical tax scenarios

First, I calculate, **property by property**, the general tax that would result from applying the first-half 2026 brackets to each assessed value. I then calculate the mean and median of those results within each commune, **including zeros below the exemption threshold**. Applying a rate to the mean assessed value would not necessarily give the same result: exemptions and brackets change the calculation.

The model uses the parameters in the [SII's official example][sii-ejemplo]: an exemption threshold of **CLP 60,030,710**, a bracket change at **CLP 214,395,361**, and annual rates of **0.893% and 1.042%**, respectively. It is a **theoretical annual-equivalent general property tax**, holding that half-year's parameters fixed. It excludes refuse charges, surtaxes and individual benefits; it does not reproduce actual tax bills or collections for the whole of 2026.

I then multiply the residual under the informal-settlement assumption by each statistic:

| Scenario | Calculation | Interpretation |
|---|---|---|
| Using the median | Residual × median theoretical tax per property | Applies the central value of the modelled tax to each unit |
| Using the mean | Residual × mean theoretical tax per property | Applies the average, which is sensitive to high assessments |

**These are two references for scale, not a confidence interval or guaranteed lower and upper bounds.** The median is not a minimum tax: if more than half the properties fall below the exemption threshold, it can be zero while the mean is positive. The same fifteen communes selected above are retained here and ranked by the scenario using the mean.

<figure style="width:100%">
  <div role="region" aria-label="Theoretical annual-equivalent general property-tax scenarios for the fifteen communes with a positive residual and a median assessment above the exemption threshold; comparison of mean and median." tabindex="0" style="max-width:100%;overflow-x:auto;border:1px solid currentColor;border-radius:.4rem">
    <img class="avaluos-ii-monetary-light" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/monetary-top15-en.svg" alt="Theoretical annual-equivalent general property-tax scenarios for the fifteen communes with a positive residual and a median assessment above the exemption threshold; comparison of mean and median." loading="lazy">
    <img class="avaluos-ii-monetary-dark" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/monetary-top15-en-dark.svg" alt="Theoretical annual-equivalent general property-tax scenarios for the fifteen communes with a positive residual and a median assessment above the exemption threshold; comparison of mean and median." loading="lazy">
  </div>
  <figcaption>Million Chilean pesos, assuming that each residual unit corresponded to a new comparable property. Amounts are hypothetical; they are neither established tax debt nor revenue retained by municipalities. Scroll horizontally or open the SVG to zoom; values appear in the following table. <a href="/assets/images/avaluos-ii/monetary-top15-en.svg">SVG</a> · <a href="/assets/images/avaluos-ii/monetary-top15-en-dark.svg">SVG dark</a>.</figcaption>
</figure>

{% include avaluos-ii-monetary-en.html %}

Iquique illustrates why both references are useful. With **18,949** residual units, the scenario using the median reaches **CLP 36 million** in annual-equivalent tax; using the mean, it reaches **CLP 4,309 million**. The difference is large: the median assessment barely exceeds the exemption threshold and yields theoretical tax of about **CLP 1,912 per property**, while the mean includes the contribution of higher assessments. Showing only one statistic would hide that difference in the profile.

In Lo Barnechea, **2,300** residual units produce **CLP 4,983 million using the median and CLP 6,669 million using the mean**. Under this model, it leads the monetary ranking despite having a much smaller physical gap than Iquique. This has not discovered missing revenue: it shows the scale of tax if new comparable properties were confirmed. The contrast makes the case for reviewing communes where an unresolved discrepancy coincides with high assessed values more concrete.

The full comparison assumes **one new comparable property for every residual unit**: I call this assumption $$q=1$$. The viewer allows it to be reduced to $$q=0.5$$ or $$q=0.25$$, halving or quartering the amounts. This factor represents the hypothetical share of the residual that would result in new comparable properties; **it is not an estimated probability, a collection rate or the share of properties paying tax**. Tax zeros are already included in both statistics. No additional construction-materials deduction is applied.

## Third spoonful: from a scenario for a commune to verification at property level

Comparing communes helps choose where to look. Establishing an omission with tax implications requires examining individual properties: **identify the building, establish its relationship to one or more cadastral records, and reconstruct the relevant dates**. The review must allow for both an omission and an explanation that rules it out.

| Possible explanation | What would need to be checked | What would weaken that explanation |
|---|---|---|
| Omitted property or building | Location, land and building information, property records and the cadastral file | The property is already correctly registered, including under another record or property-use category |
| Outdated assessed value | Built floor area and characteristics against cadastral details and their dates | The assessment already incorporates those characteristics |
| Differences in units or periods | Dwellings per property, parent records, agricultural uses, co-ownership and comparable dates | The discrepancy persists after reconciling units and periods |
| Source or processing error | Completeness of the extract, territorial identifiers and independent reproduction | The result is reproduced using independent sources and cross-checks |

**Registering a property and updating a building's assessment are different actions.** The SII has a [procedure for adding properties to the cadastre][sii-inclusion]. It also provides for changes to assessed values. An extension can increase the assessed value of an existing property without creating another record: the difference between dwellings and records cannot, by itself, detect every outdated cadastral assessment.

### What is missing before a scenario becomes an established liability

The scenarios above give the assumption a scale, but quantifying liabilities that were actually omitted requires identifying the properties, checking their dates and assessed values, and applying the relevant benefits and exemptions. Compatible, reconciled tax-billing data are also needed to compare theoretical tax with actual bills.

The [SII cadastral dictionary][sii-estructura] defines the available half-yearly field as a contribution **including refuse charges**. It is not used as net tax. The official commune-level tables reviewed distinguish components but include other non-agricultural uses: **dividing that total by residential records would produce an average drawn from incompatible populations**. The [source audit](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) retains this limitation; the rule-based calculation neither reconciles nor removes it.

Determining a tax liability, issuing a tax bill and collecting payment are different stages. The SII determines assessed values and issues property-tax bills; the [General Treasury of the Republic collects payment][tgr-impuestos]. Distribution through the [Municipal Common Fund][sii-fcm] also means that tax associated with a commune cannot be equated with revenue retained entirely by its municipality.

The [guide by Grote and Wen (2024, pp. 16–18)][fmi-guia] helps organise the problem: it distinguishes coverage, valuation and collection, and proposes cross-checking maps, field observations and records. It informs the design of a verification exercise; it does not supply a revenue coefficient that can be transferred to these communes.

<aside class="notice--info" markdown="1">
**Behind the analysis: Python and reproducible geomatics**

Python connects cadastral, census and territorial aggregates; Parquet stores columnar tables, and Matplotlib produces these figures in SVG and PNG with typography and palettes for both reading modes. Each chart comes from a verifiable table: the image helps readers see the pattern, while the table exposes the values. The viewer retains ECharts for interactive exploration and map layers for examining territory.

For CASEN, R opens the original dataset and passes the required columns to Python through an in-memory pipe. Python computes estimates and design variance; algebraic fixtures and a bounded comparison with Julia check the implementation. Separating extraction, computation, presentation and checks makes similar work easier to carry into larger computing workflows. **This execution is local: it is neither a benchmark nor a demonstrated HPC-cluster run.** The [method and provenance](/catastro_sii_brecha/data/casen-shared-site/method.md) document what was actually done.
</aside>

## Closing: the difference needs an explanation

Communes where the difference persists and registered properties have high assessed values offer a starting point for cadastral review. The scenarios in pesos show why a smaller gap may deserve tax-related attention. If comparable omitted properties are confirmed, their tax implications must be determined; if existing records, property-use categories or dates resolve the difference, the omission hypothesis becomes less compelling. The result warrants investigation but does not establish negligence or a failure to collect tax by any agency.

In the next instalment, I will explore the **Continuo de Construcciones Urbanas (CCU)** to examine the built footprint. Before attributing a discrepancy to administrative delay, its sources must be verified and the timing of each change reconstructed.

[Explore the analysis](/catastro_sii_brecha/#brecha-contribuciones) · [Download CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv).

<details markdown="1">
<summary>Methodological notes: sources, snapshots and unresolved limitations</summary>

**Provenance and coverage.** The cadastral mirror was downloaded on 24 July 2026 and corresponds to the first half of that year. It is neither a direct SII download nor a September snapshot. Antártica and Trehuaco have no extract and remain missing, rather than being treated as communes with no residential properties.

**Totals still awaiting reconciliation.** The cited [SII control by property-use category][sii-destino] reports 6,056,150 residential properties; the extract contains 6,054,808. The cited [MINVU housing-stock spreadsheets][minvu-parque] for the first half of 2026 report 6,057,949, including 1,342 in Trehuaco. The difference between the SII and the extract is 1,342, but between MINVU and the extract it reaches 3,141. Adding Trehuaco's 1,342 does not reconcile both controls: a difference of 1,799 properties remains against the MINVU total. This discrepancy is not attributed to an unproven cause, and totals are not silently replaced.

**Two informal-settlement snapshots.** The [MINVU report published on 8 July 2026][minvu-campamentos], using information referring to 2024, records 1,373 settlements, 81,993 occupied dwellings and 77,399 households. The CNC 2026 layer used in this processing contains 1,345 polygons and a total of 71,760 in the `HOGARESCEN` field, with 222 polygons missing that value. These are different populations and snapshots. Interpreting the field as census households is a provisional decision supported by its name and the available documentation, rather than by a dictionary specific to the layer. The deduction depends on it.

**Definition of construction materials.** The analysis uses the code in the INE manual, whose classification does not fully match its prose description: for acceptable materials, the latter allows some recoverable wall materials, whereas the code requires acceptable materials in all three components. The scenario combines that criterion with an acceptable dwelling type. Variants using complete materials responses and the broader non-irrecoverable category are retained; these are sensitivity analyses, not confidence intervals. The processing records 4,388 occupied dwellings with incomplete information.

**Monetary formula and unit.** For an assessed value $$A$$, exemption threshold $$E=60\,030\,710$$ and bracket change $$T=214\,395\,361$$, the calculation is:

$$
\begin{aligned}
g(A)={}&0.00893\max(\min(A,T)-E,0)\\
       &+0.01042\max(A-T,0).
\end{aligned}
$$

Results are aggregated by commune, including zeros, before multiplying each statistic by the positive residual and by $$q$$. Tax is not applied to the mean assessment, properties with zero theoretical tax are not filtered out, and a rate that is already annual is not annualised again. The individual exempt assessment in the extract does not replace the general exemption threshold in this model. The calculation therefore does not represent individual benefits or seek to reconstruct each property's tax bill. The mean and median describe registered properties; extrapolating them to the residual requires the comparability assumption.

**Processing corrections.** Territorial harmonisation was corrected for Coyhaique, Aysén and Chile Chico. The count of irrecoverable dwellings fell from 73,338 to 72,642—696 fewer—after first applying the official code's non-response exclusion. That correction does not change the dwellings–records difference or the settlement deduction. The historical anonymised 2011–2021 dataset is not used in the current calculation.

**Traceability.** The [method](/catastro_sii_brecha/data/fiscal-gap/method.md), [audit](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) and [data by commune](/catastro_sii_brecha/data/fiscal-gap/communes.json) document the processing. Only aggregates by commune are published.

</details>

## Sources and references

Ministerio de Desarrollo Social y Familia. 2026. *CASEN 2024: questionnaire and data-use note*. Tenure and principal household, pp. 79 and 83 of the [questionnaire][casen-cuestionario]; expansion factors and domains in the [data-use note][casen-nota]. Accessed September 12, 2026.

Grote, Martin, and Jean-François Wen. 2024. *How to Design and Implement Property Tax Reforms*. How to Note 2024/006. International Monetary Fund, September. [Full text][fmi-guia].

Instituto Nacional de Estadísticas (INE). 2025. *Manual de uso de microdatos censales: Censo de Población y Vivienda 2024*. Indicators viv04–viv06, pp. 103–106. [Manual][ine-manual].

Ministerio de Vivienda y Urbanismo (MINVU), Centro de Estudios de Ciudad y Territorio. 2026. *Caracterización de campamentos en Censo 2024*. Published on 8 July. See the general results and table 1, pp. 4–5. [Report][minvu-campamentos].

Servicio de Impuestos Internos (SII). “De avalúo fiscal a contribuciones: paso a paso,” example for the first half of 2026; “¿Qué es un avalúo fiscal?”; “¿El avalúo fiscal corresponde a una tasación comercial de la propiedad?”, updated 8 April 2026; “¿Cómo regularizo una propiedad que no tiene rol de avalúo?”, updated 7 April 2026; and “¿Para qué sirve el pago del impuesto territorial?”. [Calculation][sii-ejemplo], [assessed value][sii-avaluo], [distinction from market value][sii-comercial], [registration][sii-inclusion] and [municipal distribution][sii-fcm]. For buildings whose legal status has not been regularised, see the [documentation required for assessment][sii-no-regularizadas].

Servicio de Impuestos Internos (SII). N.d. *Estructura de archivo para Detalle Catastral de Bienes Raíces*. Basic information for non-agricultural properties, fields 5–8 and the property-use table, p. 1. [Dictionary][sii-estructura].

Tesorería General de la República (TGR). N.d. “Impuestos y tipos de impuestos.” TGR Help Centre. [Source][tgr-impuestos].

*The external sources above were accessed on 11 September 2026. Processing results and corrections should be read alongside the methodological notes.*

[ine-manual]: https://censo2024.ine.gob.cl/wp-content/uploads/2025/12/manual_uso_microdatos_censo2024.pdf
[minvu-campamentos]: https://catalogo.minvu.cl/cgi-bin/koha/opac-retrieve-file.pl?id=7e816aa9c26af8904eab01badfbfc6e6
[minvu-parque]: https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/
[sii-ejemplo]: https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf
[sii-estructura]: https://www.sii.cl/bbrr/descargas/estructura_detalle_catastral.pdf
[sii-comercial]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_8124.htm
[sii-avaluo]: https://www.sii.cl/destacados/impuesto_territorial/avaluo_fiscal.html
[sii-inclusion]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_1947.htm
[sii-fcm]: https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html
[sii-no-regularizadas]: https://www.sii.cl/servicios_online/1048-doctos_requeridos-2573.html
[sii-destino]: https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html
[tgr-impuestos]: https://ayuda.tgr.gob.cl/ayuda/impuestos/impuestos-y-tipos-de-impuestos
[fmi-guia]: https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf

[casen-cuestionario]: https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf
[casen-nota]: https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf

```


## _includes/ai-disclosure.html
```
{%- assign ai_lang = site.active_lang | default: page.lang | default: 'es' -%}
{%- assign ai_level = page.ai_disclosure.level | default: page.devto_ai_disclosure_level | default: 'not_disclosed' -%}
{%- assign ai_text = page.ai_disclosure.components.text | default: 'unknown' -%}
{%- assign ai_hero_origin = page.ai_disclosure.components.hero | default: 'unknown' -%}
<p id="ai-disclosure" class="ai-disclosure" data-ai-level="{{ ai_level | escape }}" data-ai-text-origin="{{ ai_text | escape }}" data-ai-hero-origin="{{ ai_hero_origin | escape }}">
  {% case ai_level %}{% when 'no_ai' %}{% if ai_lang == 'en' %}I made this article without AI.{% else %}Preparé este artículo sin IA.{% endif %}{% when 'some_ai' %}{% if ai_lang == 'en' %}I used AI to help prepare this article.{% else %}Preparé este artículo con ayuda de IA.{% endif %}{% when 'fully_autonomous' %}{% if ai_lang == 'en' %}I generated this article entirely with AI.{% else %}Generé este artículo íntegramente con IA.{% endif %}{% else %}{% if ai_lang == 'en' %}I have not declared my AI use here yet.{% else %}Aún no he declarado aquí mi uso de IA.{% endif %}{% endcase %}
  <a href="{{ '/ai-transparency/' | relative_url }}">{% if ai_lang == 'en' %}How I use AI{% else %}Cómo uso la IA{% endif %}</a>.
</p>

```


## _includes/ai-provenance-list.html
```
{% assign provenance_lang = site.active_lang | default: page.lang | default: 'es' %}
{% assign provenance_posts = site.posts | where: 'lang', provenance_lang %}
{% for article in provenance_posts %}
{% assign visual = site.data.visuales[article.visual_id] %}
{% assign hero_path = article.header.overlay_image | remove_first: '/' %}
{% assign hero = visual.piezas | where: 'archivo', hero_path | first %}
<details id="{{ article.ref | escape }}">
  <summary>{{ article.title | escape }}</summary>
  <dl>
    <dt>{% if provenance_lang == 'en' %}Text{% else %}Texto{% endif %}</dt>
    <dd data-ai-component="text" data-ai-origin="{{ article.ai_disclosure.components.text | default: 'unknown' | escape }}">{% case article.ai_disclosure.components.text %}{% when 'assisted' %}{% if provenance_lang == 'en' %}I worked on this text with AI assistance.{% else %}Trabajé este texto con ayuda de IA.{% endif %}{% when 'generated' %}{% if provenance_lang == 'en' %}I generated this text with AI.{% else %}Generé este texto con IA.{% endif %}{% when 'human' %}{% if provenance_lang == 'en' %}I wrote this text without AI.{% else %}Escribí este texto sin IA.{% endif %}{% else %}{% if provenance_lang == 'en' %}I do not have a documented record of AI involvement in this text.{% else %}No tengo documentada la intervención de IA en este texto.{% endif %}{% endcase %}</dd>
    <dt>{% if provenance_lang == 'en' %}Cover{% else %}Portada{% endif %}</dt>
    <dd data-ai-component="hero" data-ai-origin="{{ article.ai_disclosure.components.hero | default: 'unknown' | escape }}">{% case article.ai_disclosure.components.hero %}{% when 'generated' %}{% if provenance_lang == 'en' %}I created this conceptual illustration with AI.{% else %}Creé esta ilustración conceptual con IA.{% endif %}{% when 'human' %}{% if provenance_lang == 'en' %}I use a human-created cover.{% else %}Uso una portada de autoría humana.{% endif %}{% else %}{% if provenance_lang == 'en' %}I have not documented this cover’s origin.{% else %}No tengo documentado el origen de esta portada.{% endif %}{% endcase %}
    {% if hero.provenance.tool %}<p>{% if provenance_lang == 'en' %}I used{% else %}Usé{% endif %} {{ hero.provenance.tool | escape }}.</p>{% elsif article.ai_disclosure.components.hero == 'generated' %}<p>{% if provenance_lang == 'en' %}I have not documented the specific tool.{% else %}No tengo documentada la herramienta concreta.{% endif %}</p>{% endif %}
    {% if hero.alt[provenance_lang] %}<p>{{ hero.alt[provenance_lang] | escape }}</p>{% endif %}
    </dd>
  </dl>
  <p><a href="{{ article.url | relative_url }}">{% if provenance_lang == 'en' %}Read the article{% else %}Leer el artículo{% endif %}</a></p>
</details>
{% endfor %}

```


## _pages/ai-transparency.md
```
---
title: "Cómo uso la inteligencia artificial"
permalink: /ai-transparency/
lang: es
ref: ai-transparency
toc: false
---

Uso IA como una herramienta de trabajo y quiero que sepas cuándo interviene en lo que publico. En cada artículo dejo una nota breve; aquí explico mi criterio y detallo lo que tengo documentado de sus textos y portadas.

| Mi declaración | Qué quiero decir |
|---|---|
| Preparé este artículo sin IA | No usé IA generativa en su texto ni en sus imágenes. |
| Preparé este artículo con ayuda de IA | Usé IA en alguna parte del trabajo; no necesariamente en todos sus componentes. |
| Generé este artículo íntegramente con IA | Encargué a la IA la producción completa. Esta etiqueta no afirma que haya revisado cada resultado. |
| Aún no he declarado aquí mi uso de IA | Todavía no he incorporado una declaración suficiente; no equivale a afirmar que no usé IA. |

Identifico los artículos anteriores a esta política como trabajos con ayuda de IA, de acuerdo con mi declaración sobre su elaboración. Cuando no tengo documentado el detalle de un texto o una imagen, lo digo: prefiero reconocer ese límite antes que reconstruir un historial que no puedo respaldar.

## Imágenes, datos y responsabilidad

Uso las portadas generadas con IA como ilustraciones conceptuales. No las presento como fotografías, mapas reales ni evidencia de mis resultados. Indico la herramienta cuando consta en el registro: escribo «Hecho con ChatGPT» si ese fue el origen documentado, y distingo ImageGen de OpenAI mediante Codex cuando usé esa vía.

Para los gráficos estadísticos empleo datos y herramientas de análisis —por ejemplo, Python y Matplotlib—. Una ilustración generada y un gráfico calculado tienen funciones distintas; documento el método y las fuentes del segundo para que puedas examinarlo.

Soy responsable de lo que publico. Esta declaración te cuenta cómo lo elaboré; la solidez de cada análisis depende de sus fuentes, métodos, comprobaciones y límites. Corrijo el contenido cuando encuentro un error y explico las correcciones pertinentes.

Mantengo el mismo criterio en las traducciones y en mis publicaciones en redes. La nota breve acompaña al contenido y remite aquí cuando hace falta más detalle.

## Lo que tengo documentado por artículo

{% include ai-provenance-list.html %}

```


## _pages/ai-transparency-en.md
```
---
title: "How I use artificial intelligence"
permalink: /ai-transparency/
lang: en
ref: ai-transparency
toc: false
---

I use AI as a working tool, and I want you to know when it contributes to what I publish. I leave a brief note in each article; here I explain my approach and record what I know about its text and cover.

| My declaration | What I mean |
|---|---|
| I made this article without AI | I used no generative AI in its text or images. |
| I used AI to help prepare this article | I used AI in some part of the work, not necessarily in every component. |
| I generated this article entirely with AI | I entrusted the complete production to AI. This label does not claim that I reviewed every result. |
| I have not declared my AI use here yet | I have not added a sufficient declaration yet; this does not mean I used no AI. |

I identify articles predating this policy as work prepared with AI assistance, based on my declaration about how I made them. Where I have not documented the history of a text or image, I say so: I prefer to acknowledge that limit rather than reconstruct a history I cannot substantiate.

## Images, data and responsibility

I use AI-generated covers as conceptual illustrations. I do not present them as photographs, real maps or evidence of my findings. I name the tool when it is recorded: I write “Made with ChatGPT” when that is the documented origin, and distinguish OpenAI ImageGen through Codex when I used that route.

For statistical charts, I use data and analytical tools such as Python and Matplotlib. A generated illustration and a calculated chart serve different purposes; I document the latter’s methods and sources so you can examine them.

I am responsible for what I publish. This declaration tells you how I made it; the strength of each analysis depends on its sources, methods, checks and limitations. I correct the content when I find an error and explain relevant corrections.

I keep the same approach in translations and social posts. The brief note accompanies the content and points here when more detail is needed.

## What I have documented for each article

{% include ai-provenance-list.html %}

```


## scripts/catastro_sii/project_casen_shared_site.py
```
#!/usr/bin/env python3
"""Publish only reviewed CASEN aggregates and a bilingual equivalent HTML table."""
import argparse
import hashlib
import html
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def number(value, lang, digits=0):
    if value is None:
        return 'Sin dato' if lang == 'es' else 'No data'
    value = f'{value:,.{digits}f}'
    return value.translate(str.maketrans(',.', '.,')) if lang == 'es' else value

def percent(value, lang):
    return number(value * 100, lang, 2) + (' %' if lang == 'es' else '%') if value is not None else number(None, lang)

def table(rows, lang, exploratory=False):
    es = lang == 'es'
    caption = ('Casos comunales exploratorios; expc; sin representatividad ni IC comunales.' if es else
               'Exploratory commune cases; expc; no commune representativeness or confidence intervals.') if exploratory else (
               'Hogares que declaran sitio propio compartido; expr; IC normal aproximado del 95 %.' if es else
               'Households reporting an owned shared site; expr; approximate normal 95% confidence intervals.')
    headings = ['Territorio', 'Hogares muestrales', 'Sin respuesta', 'Proporción', 'IC 95 %'] if es else ['Territory', 'Sample households', 'Missing answers', 'Share', '95% CI']
    out = ['<div role="region" tabindex="0" style="max-width:100%;overflow-x:auto" aria-label="'+html.escape(caption)+'">',
           '<table><caption>'+html.escape(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+h+'</th>' for h in headings)+'</tr></thead><tbody>']
    for row in rows:
        interval = (percent(row['ci_low'],lang)+'–'+percent(row['ci_high'],lang)) if row['ci_low'] is not None else (
            ('No corresponde' if es else 'Not applicable') if exploratory else ('No estimable' if es else 'Not estimable'))
        name = ('Chile' if row['scope']=='national' else row['territory_name'])
        cells = [number(row['n_households'],lang), number(row['n_missing'],lang), percent(row['estimate'],lang),interval]
        out.append('<tr data-territory="'+html.escape(row['territory_code'])+'"><th scope="row">'+html.escape(name)+'</th>'+''.join('<td>'+html.escape(c)+'</td>' for c in cells)+'</tr>')
    out.append('</tbody></table></div>')
    return '\n'.join(out)

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir',type=Path,required=True)
    parser.add_argument('--expected-sha256',required=True)
    args=parser.parse_args()
    source=args.source_dir/'estimates.json'
    if sha(source)!=args.expected_sha256:
        raise ValueError('Reviewed aggregate digest mismatch; no projection written')
    data=json.loads(source.read_text());rows=data['rows']
    national=[r for r in rows if r['scope']=='national']
    regional=[r for r in rows if r['scope']=='region']
    cases=[next(r for r in rows if r['scope']=='commune' and r['territory_code']==c) for c in ['5101','5109']]
    if len(national)!=1 or len(regional)!=16 or any(r['unit']!='household' for r in rows):
        raise ValueError('Unexpected territorial coverage or unit')
    if any(r['ci_low'] is not None or r['ci_high'] is not None for r in rows if r['scope']=='commune'):
        raise ValueError('A commune interval would contradict the approved estimand')
    output=ROOT/'catastro_sii_brecha/data/casen-shared-site';output.mkdir(parents=True,exist_ok=True)
    for name in ['estimates.json','estimates.csv','estimates.parquet','audit.json','provenance.json']:
        shutil.copyfile(args.source_dir/name,output/name)
    method=args.source_dir.parents[1]/'docs/casen-shared-site-method.md'
    (output/'method.md').write_text(method.read_text().replace('/opt/entornos/mamba312/bin/python','python3'))
    pieces=[]
    for lang in ['es','en']:
        pieces.append("{% if include.lang == '"+lang+"' %}")
        summary='Tabla nacional y regional: proporción, muestra e incertidumbre' if lang=='es' else 'National and regional table: share, sample and uncertainty'
        pieces += ['<details><summary>'+summary+'</summary>',table(national+regional,lang),'</details>',table(cases,lang,True)]
        pieces.append('<p><a href="/catastro_sii_brecha/data/casen-shared-site/estimates.csv">'+('Descargar las 346 comunas (CSV); 11 sin muestra conservadas como dato ausente.' if lang=='es' else 'Download all 346 communes (CSV); 11 outside the sample remain missing data.')+'</a></p>')
        pieces.append('{% endif %}')
    include=ROOT/'_includes/casen-shared-site-table.html';include.write_text('\n'.join(pieces)+'\n')
    receipt={'source_estimates_sha256':args.expected_sha256,'unit':'household','rows':len(rows),
             'national_regional_table_rows':17,'exploratory_cases':['5101','5109'],
             'projection_script_sha256':sha(Path(__file__)), 'outputs_sha256':{p.name:sha(p) for p in output.iterdir() if p.is_file() and p.name!='projection.json'},
             'table_sha256':sha(include),'raw_records_exported':False}
    (output/'projection.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(receipt))

if __name__=='__main__':
    main()

```


## _includes/casen-shared-site-table.html
```
{% if include.lang == 'es' %}
<details><summary>Tabla nacional y regional: proporción, muestra e incertidumbre</summary>
<div role="region" tabindex="0" style="max-width:100%;overflow-x:auto" aria-label="Hogares que declaran sitio propio compartido; expr; IC normal aproximado del 95 %.">
<table><caption>Hogares que declaran sitio propio compartido; expr; IC normal aproximado del 95 %.</caption><thead><tr><th scope="col">Territorio</th><th scope="col">Hogares muestrales</th><th scope="col">Sin respuesta</th><th scope="col">Proporción</th><th scope="col">IC 95 %</th></tr></thead><tbody>
<tr data-territory="CL"><th scope="row">Chile</th><td>78.654</td><td>0</td><td>1,09 %</td><td>0,97 %–1,21 %</td></tr>
<tr data-territory="1"><th scope="row">Región de Tarapacá</th><td>3.093</td><td>0</td><td>0,24 %</td><td>0,06 %–0,42 %</td></tr>
<tr data-territory="2"><th scope="row">Región de Antofagasta</th><td>3.505</td><td>0</td><td>0,67 %</td><td>0,38 %–0,97 %</td></tr>
<tr data-territory="3"><th scope="row">Región de Atacama</th><td>3.257</td><td>0</td><td>0,18 %</td><td>0,02 %–0,35 %</td></tr>
<tr data-territory="4"><th scope="row">Región de Coquimbo</th><td>3.638</td><td>0</td><td>0,57 %</td><td>0,11 %–1,03 %</td></tr>
<tr data-territory="5"><th scope="row">Región de Valparaíso</th><td>8.415</td><td>0</td><td>4,59 %</td><td>3,73 %–5,44 %</td></tr>
<tr data-territory="6"><th scope="row">Región del Libertador Gral. Bernardo O&#x27;Higgins</th><td>5.324</td><td>0</td><td>0,60 %</td><td>0,32 %–0,89 %</td></tr>
<tr data-territory="7"><th scope="row">Región del Maule</th><td>5.578</td><td>0</td><td>0,27 %</td><td>0,07 %–0,47 %</td></tr>
<tr data-territory="8"><th scope="row">Región del Biobío</th><td>8.124</td><td>0</td><td>0,70 %</td><td>0,48 %–0,91 %</td></tr>
<tr data-territory="9"><th scope="row">Región de La Araucanía</th><td>5.458</td><td>0</td><td>1,07 %</td><td>0,77 %–1,38 %</td></tr>
<tr data-territory="10"><th scope="row">Región de Los Lagos</th><td>4.280</td><td>0</td><td>0,68 %</td><td>0,43 %–0,94 %</td></tr>
<tr data-territory="11"><th scope="row">Región de Aysén del Gral. Carlos Ibáñez del Campo</th><td>1.753</td><td>0</td><td>0,16 %</td><td>0,00 %–0,34 %</td></tr>
<tr data-territory="12"><th scope="row">Región de Magallanes y de la Antártica Chilena</th><td>2.354</td><td>0</td><td>0,16 %</td><td>0,00 %–0,33 %</td></tr>
<tr data-territory="13"><th scope="row">Región Metropolitana de Santiago</th><td>14.151</td><td>0</td><td>0,78 %</td><td>0,63 %–0,94 %</td></tr>
<tr data-territory="14"><th scope="row">Región de Los Ríos</th><td>3.433</td><td>0</td><td>0,79 %</td><td>0,48 %–1,10 %</td></tr>
<tr data-territory="15"><th scope="row">Región de Arica y Parinacota</th><td>2.795</td><td>0</td><td>0,38 %</td><td>0,15 %–0,60 %</td></tr>
<tr data-territory="16"><th scope="row">Región de Ñuble</th><td>3.496</td><td>0</td><td>0,64 %</td><td>0,37 %–0,91 %</td></tr>
</tbody></table></div>
</details>
<div role="region" tabindex="0" style="max-width:100%;overflow-x:auto" aria-label="Casos comunales exploratorios; expc; sin representatividad ni IC comunales.">
<table><caption>Casos comunales exploratorios; expc; sin representatividad ni IC comunales.</caption><thead><tr><th scope="col">Territorio</th><th scope="col">Hogares muestrales</th><th scope="col">Sin respuesta</th><th scope="col">Proporción</th><th scope="col">IC 95 %</th></tr></thead><tbody>
<tr data-territory="5101"><th scope="row">Valparaíso</th><td>1.329</td><td>0</td><td>9,27 %</td><td>No corresponde</td></tr>
<tr data-territory="5109"><th scope="row">Viña del Mar</th><td>1.608</td><td>0</td><td>8,60 %</td><td>No corresponde</td></tr>
</tbody></table></div>
<p><a href="/catastro_sii_brecha/data/casen-shared-site/estimates.csv">Descargar las 346 comunas (CSV); 11 sin muestra conservadas como dato ausente.</a></p>
{% endif %}
{% if include.lang == 'en' %}
<details><summary>National and regional table: share, sample and uncertainty</summary>
<div role="region" tabindex="0" style="max-width:100%;overflow-x:auto" aria-label="Households reporting an owned shared site; expr; approximate normal 95% confidence intervals.">
<table><caption>Households reporting an owned shared site; expr; approximate normal 95% confidence intervals.</caption><thead><tr><th scope="col">Territory</th><th scope="col">Sample households</th><th scope="col">Missing answers</th><th scope="col">Share</th><th scope="col">95% CI</th></tr></thead><tbody>
<tr data-territory="CL"><th scope="row">Chile</th><td>78,654</td><td>0</td><td>1.09%</td><td>0.97%–1.21%</td></tr>
<tr data-territory="1"><th scope="row">Región de Tarapacá</th><td>3,093</td><td>0</td><td>0.24%</td><td>0.06%–0.42%</td></tr>
<tr data-territory="2"><th scope="row">Región de Antofagasta</th><td>3,505</td><td>0</td><td>0.67%</td><td>0.38%–0.97%</td></tr>
<tr data-territory="3"><th scope="row">Región de Atacama</th><td>3,257</td><td>0</td><td>0.18%</td><td>0.02%–0.35%</td></tr>
<tr data-territory="4"><th scope="row">Región de Coquimbo</th><td>3,638</td><td>0</td><td>0.57%</td><td>0.11%–1.03%</td></tr>
<tr data-territory="5"><th scope="row">Región de Valparaíso</th><td>8,415</td><td>0</td><td>4.59%</td><td>3.73%–5.44%</td></tr>
<tr data-territory="6"><th scope="row">Región del Libertador Gral. Bernardo O&#x27;Higgins</th><td>5,324</td><td>0</td><td>0.60%</td><td>0.32%–0.89%</td></tr>
<tr data-territory="7"><th scope="row">Región del Maule</th><td>5,578</td><td>0</td><td>0.27%</td><td>0.07%–0.47%</td></tr>
<tr data-territory="8"><th scope="row">Región del Biobío</th><td>8,124</td><td>0</td><td>0.70%</td><td>0.48%–0.91%</td></tr>
<tr data-territory="9"><th scope="row">Región de La Araucanía</th><td>5,458</td><td>0</td><td>1.07%</td><td>0.77%–1.38%</td></tr>
<tr data-territory="10"><th scope="row">Región de Los Lagos</th><td>4,280</td><td>0</td><td>0.68%</td><td>0.43%–0.94%</td></tr>
<tr data-territory="11"><th scope="row">Región de Aysén del Gral. Carlos Ibáñez del Campo</th><td>1,753</td><td>0</td><td>0.16%</td><td>0.00%–0.34%</td></tr>
<tr data-territory="12"><th scope="row">Región de Magallanes y de la Antártica Chilena</th><td>2,354</td><td>0</td><td>0.16%</td><td>0.00%–0.33%</td></tr>
<tr data-territory="13"><th scope="row">Región Metropolitana de Santiago</th><td>14,151</td><td>0</td><td>0.78%</td><td>0.63%–0.94%</td></tr>
<tr data-territory="14"><th scope="row">Región de Los Ríos</th><td>3,433</td><td>0</td><td>0.79%</td><td>0.48%–1.10%</td></tr>
<tr data-territory="15"><th scope="row">Región de Arica y Parinacota</th><td>2,795</td><td>0</td><td>0.38%</td><td>0.15%–0.60%</td></tr>
<tr data-territory="16"><th scope="row">Región de Ñuble</th><td>3,496</td><td>0</td><td>0.64%</td><td>0.37%–0.91%</td></tr>
</tbody></table></div>
</details>
<div role="region" tabindex="0" style="max-width:100%;overflow-x:auto" aria-label="Exploratory commune cases; expc; no commune representativeness or confidence intervals.">
<table><caption>Exploratory commune cases; expc; no commune representativeness or confidence intervals.</caption><thead><tr><th scope="col">Territory</th><th scope="col">Sample households</th><th scope="col">Missing answers</th><th scope="col">Share</th><th scope="col">95% CI</th></tr></thead><tbody>
<tr data-territory="5101"><th scope="row">Valparaíso</th><td>1,329</td><td>0</td><td>9.27%</td><td>Not applicable</td></tr>
<tr data-territory="5109"><th scope="row">Viña del Mar</th><td>1,608</td><td>0</td><td>8.60%</td><td>Not applicable</td></tr>
</tbody></table></div>
<p><a href="/catastro_sii_brecha/data/casen-shared-site/estimates.csv">Download all 346 communes (CSV); 11 outside the sample remain missing data.</a></p>
{% endif %}

```


## scripts/lib/ai_disclosure.rb
```
# frozen_string_literal: true
require 'uri'

# Canonical declaration for source checks and offline DEV exports. A global
# declaration never invents the component history or a human review.
module AiDisclosure
  LEVELS = %w[no_ai some_ai fully_autonomous not_disclosed].freeze
  COMPONENTS = {'text' => %w[assisted human generated unknown], 'hero' => %w[generated human unknown]}.freeze
  module_function

  def resolve(front)
    canonical = front['ai_disclosure']
    legacy = front['devto_ai_disclosure_level']
    if front.key?('ai_disclosure')
      raise ArgumentError, 'ai_disclosure must be a mapping with level' unless canonical.is_a?(Hash) && canonical.key?('level')
      level = canonical['level']
      if front.key?('devto_ai_disclosure_level') && legacy != level
        raise ArgumentError, 'ai_disclosure.level conflicts with devto_ai_disclosure_level'
      end
    else
      level = front.key?('devto_ai_disclosure_level') ? legacy : 'not_disclosed'
      canonical = {}
    end
    raise ArgumentError, "invalid ai_disclosure.level: #{level.inspect}" unless LEVELS.include?(level)
    components = canonical.fetch('components', {})
    raise ArgumentError, 'ai_disclosure.components must be a mapping' unless components.is_a?(Hash)
    raise ArgumentError, 'unknown disclosure component' unless (components.keys - COMPONENTS.keys).empty?
    normalized = COMPONENTS.to_h do |component, levels|
      value = components.fetch(component, 'unknown')
      raise ArgumentError, "invalid #{component}: #{value.inspect}" unless levels.include?(value)
      [component, value]
    end
    if level == 'no_ai' && normalized.values.any? { |v| %w[generated assisted].include?(v) }
      raise ArgumentError, 'no_ai contradicts AI component'
    end
    if level == 'fully_autonomous' && normalized.values.any? { |v| %w[human assisted].include?(v) }
      raise ArgumentError, 'fully_autonomous contradicts human component'
    end
    validate_public_link!(canonical['evidence_url']) if canonical.key?('evidence_url')
    {'level' => level, 'components' => normalized, 'explicit' => front.key?('ai_disclosure') || front.key?('devto_ai_disclosure_level')}
  end

  def validate_public_link!(value)
    uri = URI.parse(value.to_s)
    unless uri.is_a?(URI::HTTPS) && uri.host && !uri.userinfo && !uri.query
      raise ArgumentError, 'evidence_url must be a public HTTPS URL without credentials or query parameters'
    end
    true
  rescue URI::InvalidURIError
    raise ArgumentError, 'invalid evidence_url'
  end
end

```


## scripts/verify_hero_disclosure.rb
```
#!/usr/bin/env ruby
# frozen_string_literal: true
# Source validation always runs. Passing an artifact also verifies each expected
# post, rather than accepting an empty/stale subset found by a glob.
require 'date'
require 'yaml'
require 'cgi'
require 'digest'
require 'uri'
require_relative 'lib/ai_disclosure'
require_relative 'lib/image_dimensions'

module HeroDisclosureCheck
  module_function
  def attributes(tag)
    tag.to_s.scan(/([\w:-]+)\s*=\s*["']([^"']*)["']/).to_h.transform_values { |v| CGI.unescapeHTML(v) }
  end

  # Public responsive derivatives have a fixed size/role/byte contract.
  def variant_errors(piece, root)
    path = piece['archivo'].to_s
    return [] unless path.start_with?('assets/images/heroes-v2/')
    return ['invalid variant path'] if path.include?('..')
    file = File.join(root, path)
    return ["variant missing: #{path}"] unless File.file?(file)
    errors = []
    signature = File.binread(file, 12)
    errors << "variant is not WebP: #{path}" unless File.extname(file) == '.webp' && signature.start_with?('RIFF') && signature[8, 4] == 'WEBP'
    contracts = {[1600, 900] => ['hero', 250_000], [800, 450] => ['hero', 100_000], [1280, 720] => ['teaser', 180_000], [640, 360] => ['teaser', 70_000], [1200, 630] => ['og', 180_000]}
    dimensions = image_dimensions(file)
    contract = contracts[dimensions]
    if contract
      errors << "variant role mismatch: #{path}" unless piece['rol'] == contract.first
      errors << "variant exceeds #{contract.last} bytes: #{path}" if File.size(file) > contract.last
    else
      errors << "variant dimensions outside contract: #{path}"
    end
    errors << "variant declared dimensions mismatch: #{path}" unless dimensions && [piece['ancho'], piece['alto']] == dimensions
    errors << "variant must be publicable: #{path}" unless piece['estado'] == 'publicable'
    expected_hash = piece['sha256'].to_s
    errors << "variant SHA256 missing/mismatch: #{path}" unless expected_hash.match?(/\A[0-9a-f]{64}\z/) && Digest::SHA256.file(file).hexdigest == expected_hash
    errors
  end

  def source_errors(front, root)
    errors = []
    begin
      disclosure = AiDisclosure.resolve(front)
    rescue ArgumentError => e
      return [e.message]
    end
    header = front['header'] || {}
    hero, mobile = header.values_at('overlay_image', 'overlay_image_mobile')
    {'overlay_image' => [hero, [1600, 900], 250_000], 'overlay_image_mobile' => [mobile, [800, 450], 100_000]}.each do |key, (path, dims, budget)|
      unless path.is_a?(String) && path.start_with?('/assets/images/') && !path.include?('..')
        errors << "header.#{key}: missing or invalid local hero"
        next
      end
      actual = File.join(root, path.delete_prefix('/'))
      errors << "header.#{key}: missing file #{path}" unless File.file?(actual)
      errors << "header.#{key}: expected #{dims.join('x')}" unless image_dimensions(actual) == dims
      errors << "header.#{key}: exceeds #{budget} bytes" if File.file?(actual) && File.size(actual) > budget
    end
    visual_id = front['visual_id'].to_s
    unless visual_id.match?(/\A[a-z0-9_-]+\z/)
      return errors + ['missing/invalid visual_id']
    end
    catalog_path = File.join(root, '_data', 'visuales', "#{visual_id}.yml")
    return errors + ['visual_id catalog missing'] unless File.file?(catalog_path)
    catalog = YAML.safe_load_file(catalog_path, permitted_classes: [Date, Time], aliases: true)
    pieces = Array(catalog['piezas'])
    [hero, mobile].each do |path|
      piece = pieces.find { |p| p['archivo'] == path.to_s.delete_prefix('/') }
      unless piece && piece['estado'] == 'publicable' && piece['rol'] == 'hero'
        errors << "hero not a publicable catalog hero: #{path}"
        next
      end
      errors.concat(variant_errors(piece, root))
      %w[es en].each { |lang| errors << "hero missing #{lang} description" if piece.dig('alt', lang).to_s.strip.empty? }
      component = disclosure.dig('components', 'hero')
      ai_origin = %w[ia ia-integrada ai ai-generated].include?(piece['origen'])
      errors << 'hero AI attribution contradicts catalog origin' if (component == 'generated') != ai_origin
      errors << 'human hero attribution lacks human catalog origin' if component == 'human' && !%w[human humano].include?(piece['origen'])
      errors << 'no_ai contradicts catalog AI hero' if disclosure['level'] == 'no_ai' && ai_origin
      if piece['sha256']
        actual = File.join(root, path.to_s.delete_prefix('/'))
        errors << "hero sha256 mismatch: #{path}" unless File.file?(actual) && Digest::SHA256.file(actual).hexdigest == piece['sha256']
      end
    end
    errors
  rescue Psych::Exception => e
    errors + ["invalid catalog YAML: #{e.message}"]
  end

  def artifact_errors(front, html, site_dir)
    errors = []
    expected = AiDisclosure.resolve(front)
    errors << 'expected exactly one h1' unless html.scan(/<h1\b/i).size == 1
    images = html.scan(/<img\b[^>]*>/i).select { |tag| attributes(tag)['fetchpriority'] == 'high' }
    if images.size != 1
      errors << 'expected one high-priority hero image'
    else
      img = attributes(images.first)
      errors << 'hero image must have decorative picture wrapper' unless html.match?(%r{<picture\b[^>]*aria-hidden="true"[^>]*>\s*#{Regexp.escape(images.first)}}m)
      errors << 'hero must be eager and decorative with fixed dimensions' unless img.values_at('loading', 'alt', 'width', 'height') == ['eager', '', '1600', '900']
      header = front.fetch('header')
      expected_srcset = "#{header['overlay_image_mobile']} 800w, #{header['overlay_image']} 1600w"
      errors << 'hero src differs from source' unless img['src'] == header['overlay_image']
      errors << 'hero responsive candidates differ from source' unless img['srcset'] == expected_srcset && img['sizes'] == '100vw'
      preloads = html.scan(/<link\b[^>]*>/i).map { |tag| attributes(tag) }.select { |a| a['rel'] == 'preload' && a['as'] == 'image' }
      errors << 'preload differs from effective image' unless preloads.size == 1 && preloads.first.values_at('href', 'imagesrcset', 'imagesizes') == img.values_at('src', 'srcset', 'sizes')
      [img['src'], *img.fetch('srcset', '').split(',').map { |c| c.strip.split.first }].compact.each do |path|
        errors << "missing built hero #{path}" unless File.file?(File.join(site_dir, path.delete_prefix('/')))
      end
    end
    notes = html.scan(/<p\b[^>]*>/i).map { |tag| attributes(tag) }.select { |a| a['id'] == 'ai-disclosure' }
    errors << 'missing/incorrect disclosure level' unless notes.size == 1 && notes.first['data-ai-level'] == expected['level']
    expected['components'].each do |component, origin|
      errors << "incorrect rendered #{component} provenance" unless notes.size == 1 && notes.first["data-ai-#{component}-origin"] == origin
    end
    language = front.fetch('lang', 'es')
    prefix = language == 'es' ? '' : "/#{language}"
    canonical = "https://3cucharadas.cl#{prefix}#{front['permalink']}"
    links = html.scan(/<link\b[^>]*>/i).map { |tag| attributes(tag) }
    errors << 'canonical differs from source permalink/lang' unless links.select { |a| a['rel'] == 'canonical' }.map { |a| a['href'] } == [canonical]
    %w[es en].each do |lang|
      href = "https://3cucharadas.cl#{lang == 'es' ? '' : '/en'}#{front['permalink']}"
      errors << "missing #{lang} hreflang" unless links.any? { |a| a['hreflang'] == lang && a['href'] == href }
    end
    published = html.scan(/<meta\b[^>]*>/i).map { |tag| attributes(tag) }.find { |a| a['itemprop'] == 'datePublished' }
    source_date = front.fetch('date').to_s
    rendered_date = published && published['content'].to_s
    # Explicit timestamps preserve an instant, even when Jekyll converts midnight
    # UTC to the preceding calendar date in Chile. Date-only posts preserve a day.
    same_date = if source_date.match?(/\d{2}:\d{2}/)
      rendered_date && DateTime.parse(rendered_date) == DateTime.parse(source_date)
    else
      rendered_date && Date.parse(rendered_date) == Date.parse(source_date)
    end
    errors << 'publication date differs from source' unless same_date
    policy = "#{prefix}/ai-transparency/"
    errors << 'missing localized policy link' unless html.include?(%(href="#{policy}"))
    errors << 'missing built policy' unless File.file?(File.join(site_dir, policy.delete_prefix('/'), 'index.html'))
    errors
  end

  def run(root:, artifact: nil)
    posts = Dir.glob(File.join(root, '_posts', '*.md')).sort
    return ['empty post inventory'] if posts.empty?
    posts.flat_map do |path|
      front = YAML.safe_load(File.read(path).split(/^---\s*$/, 3)[1], permitted_classes: [Date, Time], aliases: true)
      errors = source_errors(front, root)
      if artifact
        prefix = front['lang'] == 'en' ? 'en/' : ''
        target = File.join(artifact, prefix, front.fetch('permalink').delete_prefix('/'), 'index.html')
        if File.file?(target)
          errors.concat(artifact_errors(front, File.read(target), artifact)) if errors.empty?
        else
          errors << 'expected built post missing'
        end
      end
      errors.map { |e| "#{File.basename(path)}: #{e}" }
    rescue StandardError => e
      ["#{File.basename(path)}: #{e.class}: #{e.message}"]
    end
  end
end

if $PROGRAM_NAME == __FILE__
  root = File.expand_path('..', __dir__)
  artifact = ARGV[0] && File.expand_path(ARGV[0])
  errors = HeroDisclosureCheck.run(root: root, artifact: artifact)
  abort errors.join("\n") unless errors.empty?
  puts "Hero/disclosure OK: #{Dir.glob(File.join(root, '_posts', '*.md')).size} source posts#{artifact ? ' and built pages' : ''}"
end

```


## tests/test_ai_disclosure.rb
```
# frozen_string_literal: true
require 'minitest/autorun'
require 'time'
require_relative '../scripts/lib/ai_disclosure'

class AiDisclosureTest < Minitest::Test
  def declaration(level, text: 'unknown', hero: 'unknown')
    {'ai_disclosure' => {'level' => level, 'components' => {'text' => text, 'hero' => hero}}}
  end

  def test_four_levels_are_preserved
    %w[no_ai some_ai fully_autonomous not_disclosed].each do |level|
      assert_equal level, AiDisclosure.resolve(declaration(level))['level']
    end
  end

  def test_absence_is_not_a_claim_of_ai_assistance
    assert_equal 'not_disclosed', AiDisclosure.resolve({})['level']
    assert_equal 'unknown', AiDisclosure.resolve(declaration('some_ai'))['components']['text']
    refute AiDisclosure.resolve({})['explicit']
    assert AiDisclosure.resolve(declaration('not_disclosed'))['explicit']
  end

  def test_liquid_renderer_preserves_levels_and_unknown_component_history
    require 'liquid'
    template = Liquid::Template.parse(File.read(File.expand_path('../_includes/ai-disclosure.html', __dir__)))
    %w[no_ai some_ai fully_autonomous not_disclosed].each do |level|
      %w[es en].each do |lang|
        html = template.render!({'site' => {'active_lang' => lang}, 'page' => declaration(level), 'include' => {'mode' => 'details'}})
        assert_includes html, %(data-ai-level="#{level}")
        assert_includes html, %(data-ai-text-origin="unknown")
        refute_includes html, '<details'
        assert_operator html.gsub(/<[^>]+>/, '').split.size, :<, 32
        assert_includes html, lang == 'en' ? 'I ' : (level == 'not_disclosed' ? 'Aún no he' : (level == 'fully_autonomous' ? 'Generé' : 'Preparé'))
        refute_includes html, 'Documented tool:'
      end
    end
    html = template.render!({'site' => {'active_lang' => 'en'}, 'page' => {}, 'include' => {'mode' => 'badge'}})
    assert_includes html, 'I have not declared my AI use here yet.'
  end

  def test_legacy_matching_and_conflicts
    assert_equal 'some_ai', AiDisclosure.resolve({'devto_ai_disclosure_level' => 'some_ai'})['level']
    assert_equal 'some_ai', AiDisclosure.resolve(declaration('some_ai').merge('devto_ai_disclosure_level' => 'some_ai'))['level']
    assert_raises(ArgumentError) { AiDisclosure.resolve(declaration('no_ai').merge('devto_ai_disclosure_level' => 'some_ai')) }
  end

  def test_invalid_shape_and_contradictions_fail_closed
    [{'ai_disclosure' => 'some_ai'}, {'ai_disclosure' => {}}, declaration('invented'), declaration('some_ai', hero: 'assisted'), declaration('no_ai', hero: 'generated'), declaration('no_ai', text: 'assisted'), declaration('fully_autonomous', text: 'human')].each do |front|
      assert_raises(ArgumentError, front.inspect) { AiDisclosure.resolve(front) }
    end
  end

  def test_provenance_links_cannot_execute_or_leak_local_paths
    %w[javascript:alert(1) file:///home/private /home/private https://user:secret@example.com https://example.com/?token=secret //example.com].each do |link|
      front = declaration('some_ai')
      front['ai_disclosure']['evidence_url'] = link
      assert_raises(ArgumentError, link) { AiDisclosure.resolve(front) }
    end
    front = declaration('some_ai')
    front['ai_disclosure']['evidence_url'] = 'https://example.com/public-receipt'
    assert_equal 'some_ai', AiDisclosure.resolve(front)['level']
  end
end

require 'tmpdir'
require 'fileutils'
require 'zlib'
require_relative '../scripts/verify_hero_disclosure'

class HeroDisclosureCheckTest < Minitest::Test
  def png(path, width, height)
    chunk = ->(kind, data) { [data.bytesize].pack('N') + kind + data + [Zlib.crc32(kind + data)].pack('N') }
    File.binwrite(path, "\x89PNG\r\n\x1a\n".b + chunk.call('IHDR', [width, height, 8, 2, 0, 0, 0].pack('NNCCCCC')) + chunk.call('IDAT', Zlib.deflate(("\0".b * (width * 3 + 1)) * height)) + chunk.call('IEND', ''.b))
  end

  def setup
    @dir = Dir.mktmpdir('hero-disclosure-test')
    FileUtils.mkdir_p(File.join(@dir, 'assets/images'))
    FileUtils.mkdir_p(File.join(@dir, '_data/visuales'))
    FileUtils.mkdir_p(File.join(@dir, 'ai-transparency'))
    File.write(File.join(@dir, 'ai-transparency/index.html'), 'policy')
    png(File.join(@dir, 'assets/images/hero.png'), 1600, 900)
    png(File.join(@dir, 'assets/images/mobile.png'), 800, 450)
    @front = {'title' => 'Test', 'date' => '2026-09-12', 'lang' => 'es', 'permalink' => '/test/', 'visual_id' => 'test', 'header' => {'overlay_image' => '/assets/images/hero.png', 'overlay_image_mobile' => '/assets/images/mobile.png'}, 'ai_disclosure' => {'level' => 'some_ai', 'components' => {'text' => 'unknown', 'hero' => 'generated'}}}
    @catalog = {'piezas' => %w[hero mobile].map { |name| {'archivo' => "assets/images/#{name}.png", 'estado' => 'publicable', 'rol' => 'hero', 'origen' => 'ia-integrada', 'alt' => {'es' => 'Ilustración', 'en' => 'Illustration'}} }}
    write_catalog
    @html = <<~HTML
      <h1>Test</h1>
      <link rel="canonical" href="https://3cucharadas.cl/test/">
      <link rel="alternate" hreflang="es" href="https://3cucharadas.cl/test/">
      <link rel="alternate" hreflang="en" href="https://3cucharadas.cl/en/test/">
      <meta itemprop="datePublished" content="2026-09-12T00:00:00-04:00">
      <link rel="preload" as="image" href="/assets/images/hero.png" imagesrcset="/assets/images/mobile.png 800w, /assets/images/hero.png 1600w" imagesizes="100vw">
      <picture aria-hidden="true"><img src="/assets/images/hero.png" srcset="/assets/images/mobile.png 800w, /assets/images/hero.png 1600w" sizes="100vw" width="1600" height="900" alt="" fetchpriority="high" loading="eager"></picture>
      <p id="ai-disclosure" data-ai-level="some_ai" data-ai-text-origin="unknown" data-ai-hero-origin="generated">Preparé este artículo con ayuda de IA.</p>
      <a href="/ai-transparency/">Policy</a>
    HTML
  end

  def teardown
    FileUtils.remove_entry(@dir)
  end

  def write_catalog
    File.write(File.join(@dir, '_data/visuales/test.yml'), @catalog.to_yaml)
  end

  def test_valid_source_and_artifact_recover_green
    assert_empty HeroDisclosureCheck.source_errors(@front, @dir)
    assert_empty HeroDisclosureCheck.artifact_errors(@front, @html, @dir)
  end

  def test_explicit_timestamp_is_compared_as_an_instant_across_timezones
    @front['date'] = Time.iso8601('2026-07-15T00:00:00Z')
    html = @html.sub('2026-09-12T00:00:00-04:00', '2026-07-14T20:00:00-04:00')
    assert_empty HeroDisclosureCheck.artifact_errors(@front, html, @dir)
    wrong = html.sub('2026-07-14T20:00:00-04:00', '2026-07-15T20:00:00-04:00')
    assert HeroDisclosureCheck.artifact_errors(@front, wrong, @dir).any? { |e| e.include?('publication date differs') }
    @front['date'] = '2026-07-15 00:00:00 +0000'
    assert_empty HeroDisclosureCheck.artifact_errors(@front, html, @dir)
  end

  def test_empty_inventory_is_a_failure
    assert_includes HeroDisclosureCheck.run(root: @dir), 'empty post inventory'
  end

  def test_missing_mobile_and_unknown_catalog_origin_reject
    File.unlink(File.join(@dir, 'assets/images/mobile.png'))
    assert HeroDisclosureCheck.source_errors(@front, @dir).any? { |e| e.include?('missing file') }
    @catalog['piezas'].first['origen'] = 'unknown'
    write_catalog
    assert_includes HeroDisclosureCheck.source_errors(@front, @dir), 'hero AI attribution contradicts catalog origin'
  end

  def test_wrong_dimensions_hash_and_unpublished_catalog_reject
    png(File.join(@dir, 'assets/images/mobile.png'), 640, 360)
    assert HeroDisclosureCheck.source_errors(@front, @dir).any? { |e| e.include?('800x450') }
    @catalog['piezas'].first['sha256'] = '0' * 64
    write_catalog
    assert HeroDisclosureCheck.source_errors(@front, @dir).any? { |e| e.include?('sha256 mismatch') }
    @catalog['piezas'].first['estado'] = 'bloqueado'
    write_catalog
    assert HeroDisclosureCheck.source_errors(@front, @dir).any? { |e| e.include?('not a publicable') }
  end

  def test_real_webp_derivative_requires_digest_role_and_byte_budget
    relative = 'assets/images/heroes-v2/test/hero.webp'
    target = File.join(@dir, relative)
    FileUtils.mkdir_p(File.dirname(target))
    FileUtils.cp(File.expand_path('../assets/images/avaluos-ii/hero-brecha-residencial-tokyo-night-1600x900.webp', __dir__), target)
    piece = {'archivo' => relative, 'rol' => 'hero', 'estado' => 'publicable', 'ancho' => 1600, 'alto' => 900, 'sha256' => Digest::SHA256.file(target).hexdigest}
    assert_empty HeroDisclosureCheck.variant_errors(piece, @dir)
    assert HeroDisclosureCheck.variant_errors(piece.merge('sha256' => nil), @dir).any? { |e| e.include?('SHA256') }
    assert HeroDisclosureCheck.variant_errors(piece.merge('rol' => 'teaser'), @dir).any? { |e| e.include?('role mismatch') }
    File.open(target, 'ab') { |f| f.write('x' * 250_001) }
    assert HeroDisclosureCheck.variant_errors(piece, @dir).any? { |e| e.include?('exceeds 250000') }
  end

  def test_preload_disclosure_duplicate_title_and_date_mutations_reject
    mutations = {
      'preload differs' => @html.sub('imagesizes="100vw"', 'imagesizes="50vw"'),
      'exactly one h1' => @html + '<h1>Duplicate</h1>',
      'incorrect disclosure level' => @html.sub('data-ai-level="some_ai"', 'data-ai-level="no_ai"'),
      'publication date differs' => @html.sub('2026-09-12T', '2026-09-11T'),
      'canonical differs' => @html.sub('rel="canonical" href="https://3cucharadas.cl/test/"', 'rel="canonical" href="https://3cucharadas.cl/wrong/"'),
      'incorrect rendered text provenance' => @html.sub('data-ai-text-origin="unknown"', 'data-ai-text-origin="assisted"')
    }
    mutations.each do |message, html|
      assert HeroDisclosureCheck.artifact_errors(@front, html, @dir).any? { |e| e.include?(message) }, message
    end
    assert_empty HeroDisclosureCheck.artifact_errors(@front, @html, @dir)
  end
end

```


## Reported evidence claude-science/round2/science-findings.json
```json
{
  "task_id": "D2",
  "source_digest": "14eaab859814dda0d89066b79c7b395b8e1cbb3e90aa7e65f5f080fe3dddec80",
  "provider": "anthropic",
  "requested_model": "sonnet",
  "effective_identity_evidence": {
    "self_report": "claude-sonnet-5 (Sonnet 5), Anthropic — per this session's harness system-reminder",
    "runtime_evidence": "none independent of the harness string; no API/header introspection available",
    "note": "same source as round 1, not a second confirmation"
  },
  "findings": [
    {
      "id": "F1",
      "severity": "P1->resolved",
      "status": "resolved",
      "file": "src/casen_shared_site/rdata.py:16-38",
      "claim": "R_READER now validates !is.factor(x) && is.numeric(x) && typeof(x) in {integer,double} && !inherits(x,'integer64') && all(class(x) %in% allowlist) for every selected column BEFORE the 'data' branch runs as.numeric(). A rejected column aborts with UNSUPPORTED_R_COLUMN and Python raises before any coercion — the original silent-corruption path is unreachable.",
      "verification_performed": "Read the R_READER source and traced control flow: the safety loop runs unconditionally in both 'metadata' and 'data' modes, so a factor can never reach the coercion branch. Cross-checked test_factor_codes_fail_closed_before_level_index_conversion / test_character_codes_fail_closed_before_numeric_coercion / test_integer64_class_rejected_before_silent_precision_change: these build a REAL R factor/character/integer64 via an actual Rscript subprocess and assert ValueError — this is genuine boundary-level verification, not a Python-side mock, and directly answers the remedy the prior review requested ('add an integration test that exercises the actual R subprocess path').",
      "residual": "The claim that the real 2024 source has 0 factor columns (D2-F1-real-column-metadata.json: 5 haven_labelled + 6 numeric, double storage) is self-reported by the same inspection code path being verified here — not independently re-derived from the raw RData by a second reader. This no longer matters for safety (the guard fails closed regardless of what the real file contains), only for the narrower claim 'this specific file was never at risk.'",
      "remedy": "none required; optional: if the real file becomes available in a future review, re-run inspect_rdata_columns as a second, independent check against a fresh copy of the source file rather than trusting the persisted json alone."
    },
    {
      "id": "F1-secondary",
      "severity": "P3",
      "status": "resolved, correctly scoped",
      "file": "src/casen_shared_site/rdata.py:73 (read_csv skip_blank_lines=False)",
      "claim": "pandas silently dropped a blank CSV line for a single-column NA fixture (write.table with na=''). Fixed with skip_blank_lines=False, red/green evidence retained (D2-F1-r-tests-initial-failure.log / D2-F1-r-tests-green.log).",
      "note": "This was a test-fixture artifact of isolated single-column tests, not a production risk: main() always requests all 11 FIELDS, so a fully-empty output row would need every column NA simultaneously, which write.table renders as ',,,,,,,,,,' (not a blank line). Correctly fixed regardless.",
      "remedy": "none"
    },
    {
      "id": "F2",
      "severity": "P2",
      "status": "unchanged by design, acceptable",
      "claim": "Global (not domain-scoped) singleton-stratum policy retained intentionally; docs/method.md and core.py comments confirm this is a deliberate fail-closed choice, not an oversight, and that no official singleton correction exists to adopt instead.",
      "remedy": "none"
    },
    {
      "id": "F3",
      "severity": "P2->resolved",
      "status": "resolved",
      "file": "docs/casen-shared-site-method.md (Fuentes… section) + D2 disposition",
      "claim": "n_flagged=0 is now explicitly documented as a tautological success sentinel ('Ese cero no constituye una medición independiente ni evidencia positiva de calidad'), matching the prior remedy verbatim.",
      "remedy": "none"
    }
  ],
  "open_p0_p1": [],
  "verdict": "F1 resolved: accept D1 under source_digest 14eaab8598... — the fix is structural (fail-closed at the R/Python boundary, independent of what any given source file contains) and verified through actual Rscript subprocess execution against synthetic factor/character/integer64 fixtures, not merely asserted. F3 resolved via documentation. F2 remains an intentional, correctly-labeled conservative policy, not a defect. No open P0/P1.",
  "limitations": [
    "No raw microdata access, as in round 1; the 'real source has no factor columns' claim rests on the pipeline's own self-reported inspection output, not a second independent reader.",
    "Did not byte-verify the pasted code/test blocks against the frozen manifest hashes in round2/source-freeze.json — Write was denied and a heredoc was blocked by a quoting filter; verified instead by reading source-freeze.json directly and cross-checking its rdata.py/core.py hashes against verification.json, and by manually counting the 31 tests in the pasted suite (7+12+7+5), which matched the disposition.json claim.",
    "R execution, Julia parity, and aggregate-hash reproduction are taken from the pasted receipts, not re-run in this session (task was scoped read-only)."
  ]
}

```


## Reported evidence editorial-browser/receipt.json
```json
{
  "task_id": "E1-editorial-browser",
  "status": "scoped_checks_pass_with_documented_limits",
  "surface": "local preview http://127.0.0.1:4004; fresh E1 build completed at 2026-09-12T11:45Z",
  "scope": "Avalúos II ES/EN gap/CASEN/monetary figures plus two CASEN tables and two fiscal/monetary tables; excludes attribution UI.",
  "matrix": {
    "cases": 8,
    "checks": 368,
    "passed": 368,
    "failed": 0,
    "widths": [
      390,
      1440
    ],
    "themes": [
      "light",
      "academic-night"
    ]
  },
  "source_estimates_sha256": "b192b57607badd8fac36f42f4e5bc3132b4239ecb05ed7a0904998f91121a9ce",
  "fetched_svg_sha256": {
    "/assets/images/avaluos-ii/gap-top15-es.svg": "b4b04d89659d8761a6188a9e075d3fe1e12163ee3c36b782a097b5ec5c52e454",
    "/assets/images/avaluos-ii/casen-shared-site-es.svg": "a07067dd96040364c361f52ef5f3c02e91f646a086051e7ad26ac1b39a7107c5",
    "/assets/images/avaluos-ii/monetary-top15-es.svg": "39329925152b791a93622958ba6509390671bd43c803cff06861f38818a48d46",
    "/assets/images/avaluos-ii/gap-top15-es-dark.svg": "45caff806cc17477a6ece053c5ced08332c89c53fee8c21fb7c554d5f583199e",
    "/assets/images/avaluos-ii/casen-shared-site-es-dark.svg": "1bcbe6130fb5f120c1068f4d62e313d6173e4040d3e5ae6422033b3c6e4f9387",
    "/assets/images/avaluos-ii/monetary-top15-es-dark.svg": "bcc3fea5479ae668729b401a776c43fdda56b92b1a5c511fd4437fd8c9555461",
    "/assets/images/avaluos-ii/gap-top15-en.svg": "fc584c2a855debcdcef7c2ddd9464ea218f883235f9c90ef2aa2735a8c957c3d",
    "/assets/images/avaluos-ii/casen-shared-site-en.svg": "82dfb42a57697b6fdab66819209ab28b265057f6f92d1cacaac55f09a2db656c",
    "/assets/images/avaluos-ii/monetary-top15-en.svg": "2805ee1a09fb2fdb1eeeb9f7090dec05d582320bbe97ebed5021b8a9ae101402",
    "/assets/images/avaluos-ii/gap-top15-en-dark.svg": "29c7b0bb710a52113af73d4d4cafb7632fea472be12d6df62f80fb10eddbd6ef",
    "/assets/images/avaluos-ii/casen-shared-site-en-dark.svg": "3ad629729eb39746c4fcb8defcacd8057e4a80a50942f5202c8e1e6820198c09",
    "/assets/images/avaluos-ii/monetary-top15-en-dark.svg": "47c845ceeb206ef99c52d97aa3b64a120d971b6d2fbc85a8397d62a610636060"
  },
  "source_fragments_sha256": {
    "_includes/casen-shared-site-table.html": "fb724a62271361b91e2fca95d396779f1e6ff4ea92d4bf36cad81bb456592bb4"
  },
  "axe": {
    "en-1440-academic-night": {
      "counts": {
        "inapplicable": 64,
        "incomplete": 1,
        "passes": 24,
        "violations": 0
      },
      "incomplete_node_counts": {
        "color-contrast": 2
      }
    },
    "es-390-light": {
      "counts": {
        "inapplicable": 64,
        "incomplete": 1,
        "passes": 24,
        "violations": 0
      },
      "incomplete_node_counts": {
        "color-contrast": 52
      }
    },
    "en-1440-light": {
      "counts": {
        "inapplicable": 64,
        "incomplete": 1,
        "passes": 24,
        "violations": 0
      },
      "incomplete_node_counts": {
        "color-contrast": 52
      }
    },
    "en-390-light": {
      "counts": {
        "inapplicable": 64,
        "incomplete": 1,
        "passes": 24,
        "violations": 0
      },
      "incomplete_node_counts": {
        "color-contrast": 52
      }
    },
    "es-1440-light": {
      "counts": {
        "inapplicable": 64,
        "incomplete": 1,
        "passes": 24,
        "violations": 0
      },
      "incomplete_node_counts": {
        "color-contrast": 52
      }
    },
    "es-1440-academic-night": {
      "counts": {
        "inapplicable": 64,
        "incomplete": 1,
        "passes": 24,
        "violations": 0
      },
      "incomplete_node_counts": {
        "color-contrast": 2
      }
    },
    "es-390-academic-night": {
      "counts": {
        "inapplicable": 64,
        "incomplete": 1,
        "passes": 24,
        "violations": 0
      },
      "incomplete_node_counts": {
        "color-contrast": 2
      }
    },
    "en-390-academic-night": {
      "counts": {
        "inapplicable": 64,
        "incomplete": 1,
        "passes": 24,
        "violations": 0
      },
      "incomplete_node_counts": {
        "color-contrast": 2
      }
    }
  },
  "axe_interpretation": "Zero detected violations; color-contrast incomplete retained. Scoped computed-color bounds are independently above4.5, not an axe pass or global WCAG certification.",
  "contrast_resolution": {
    "method": "WCAG relative luminance on observed computed colors, bounding all CSS gradient alpha compositions; not a pixel-level audit.",
    "light": {
      "text": "#000000",
      "base": "#faf7f0",
      "white_overlay": "#fdfdfd",
      "max_black_shadow_alpha_each": 0.16,
      "shadow_layers": 2,
      "conservative_darkest_background": "#b0aea9",
      "minimum_ratio": 9.473356565663606
    },
    "dark_caption": {
      "text": "#f4f4f4",
      "lightest_background": "#161616",
      "minimum_ratio": 16.45309617193269
    },
    "dark_cells": {
      "text": "#e5eaf1",
      "background": "#202838",
      "ratio": 12.215510841329912
    },
    "caveats": [
      "Captured stable theme colors; immediate post-toggle light measurement was transitional and excluded.",
      "Applies to the scoped table text/gradients only; image text contrast separately verified by V0/V1.",
      "Axe incomplete results preserved, not rewritten as passes."
    ]
  },
  "keyboard": {
    "before": {
      "before": 0,
      "focused": true,
      "outline": "rgb(16, 16, 16) auto 1px"
    },
    "after": {
      "after": 40,
      "outline": "rgb(16, 16, 16) auto 1px",
      "tag": "DIV"
    },
    "method": "Actual agent-browser press ArrowRight after focusing figure scroll region"
  },
  "screenshots_inspected": [
    "es-390-light-casen-shared-site.png",
    "es-390-academic-night-casen-right-bottom.png",
    "es-1440-light-monetary-top15.png",
    "en-390-light-casen-table.png",
    "es-1440-academic-night-casen-shared-site.png",
    "en-390-light-monetary-top15.png",
    "en-390-academic-night-casen-right-bottom.png",
    "en-1440-light-casen-shared-site.png",
    "en-1440-academic-night-monetary-top15.png"
  ],
  "limitations": [
    "At390px the1000px figure is intentionally clipped inside its scroll container, keeping labels legible; right-hand numeric columns require horizontal scroll or SVG opening.",
    "At1440px the article column is roughly730px because sidebars remain visible; horizontal figure scroll still needed. Allowed by current embedding contract, residual UX cost.",
    "The table uses14.4px text in the390px case; long official territory names wrap into multiple lines.",
    "No physical Safari/iPhone validation; local Chromium151.",
    "No performance metrics; another agent owns them.",
    "Upcoming first-person AI attribution UI change is excluded; no global final-site approval asserted."
  ],
  "findings": [],
  "browser_session_closed": true,
  "server4004_untouched": true,
  "evidence_manifest": {
    "en-390-light-casen-shared-site.png": "027833893726a8075671c02d0f2b90bbb6c05f3aebdde00819775071a36956bf",
    "editorial-keyboard-before.json": "d5901d6e7420d19774d8b334c7a6107f39d2161f2565d4201c463b71904f78bf",
    "en-390-academic-night-monetary-top15.png": "2232c3189671268752d10306cce5e0d110737238ec1cc3afacadd1d2f7e779b8",
    "en-1440-academic-night-fiscal-tables-axe.json": "1e2ed847ff1c44a6e1a08c2e66231b502135f8176800b6a184becc6b4e447cd5",
    "editorial-table-mobile.json": "310cfe2bdf04656fd51ccc355af9131c9a70bc04b9ee1c38c55dda80f1addd11",
    "es-390-academic-night-casen-right-bottom.png": "2150a9db4e046e4d7778fdd0b62463537aa597cde0a0d9a956dee9437801f111",
    "en-1440-academic-night-axe.json": "92209af87581d64efac191481455bc6608470957e3f44eb80f4e9b1ecb651a83",
    "run-qa.py": "6f6fdf5b473d3b6cc4f012dabba55081025aa25d5d48f810fb6bc8ce91c597fc",
    "en-390-academic-night-fiscal-tables-axe.json": "1e2ed847ff1c44a6e1a08c2e66231b502135f8176800b6a184becc6b4e447cd5",
    "en-1440-light.json": "fdfc713383d43f48c4b3729cb14d82c22cc305f7b849e15697e0b66b7e322bb5",
    "matrix.json": "0a6e6b8a404cd003b3d777900fada9358ea796f12aba8c26d459495f59c5e85b",
    "es-1440-light-fiscal-tables-axe.json": "ea35138f9c939d272d64c1fb0b77f6814fe7b024ef9cc9f7d43eadf3640322b2",
    "es-390-academic-night-fiscal-tables-axe.json": "956439c796012c3b6a5e152199ba814df54108b5b27c3e6bc03887ec12765128",
    "en-390-light-casen-table.png": "93e252e0dab5b9e2d30b4ef2b5b779712e272be0fbaf33067a55eb45176c265e",
    "es-390-light-axe.json": "d7a54f1f837f6bfffb6e9e5535a54ce2a1e92e828466ab0f683b042ef2919c72",
    "es-1440-light-monetary-top15.png": "3382b92541441848cba37f23f788303c075024876b2ed5f2c8bc6d510583b603",
    "editorial-contrast-light-stable.json": "e155af69dcdea7b5cad4ab45e2b4727a825db9e05666088471912b3089365a44",
    "es-390-light-casen-shared-site.png": "84b37d79e60866623318fa6229e160edf295737e70c376e72d40b21f79cd14d2",
    "editorial-contrast-night.json": "7c8f80a9055940b632773a3707bc49f6788ee1485fb967bfcdc8bc3d4b8e0f7a",
    "en-1440-light-axe.json": "e318bb06fe7d37fbf63a6234195572c68736726cd8304f08c88d79b9de691d9f",
    "es-1440-academic-night.json": "cd59e4d5a4c783dab6e469ff5096eda8419d9677512ac93e31dd6ca0fabf43a7",
    "en-1440-light-monetary-top15.png": "2d28d1815be7dab00c9efce3f37bc542f90313de7c8aaca18d3d5050a839e796",
    "en-390-light-axe.json": "e318bb06fe7d37fbf63a6234195572c68736726cd8304f08c88d79b9de691d9f",
    "es-1440-light-axe.json": "d7a54f1f837f6bfffb6e9e5535a54ce2a1e92e828466ab0f683b042ef2919c72",
    "editorial-keyboard-after.json": "fd590965239958ebcdaccbbb86e514e0c135225e4c75f201d45d067d43039900",
    "en-1440-light-casen-shared-site.png": "5dd09d8d294e1c2f7c2ddfa0d8965d5cd82154ea76e105aee54dded4731ff859",
    "es-390-light-fiscal-tables-axe.json": "ea35138f9c939d272d64c1fb0b77f6814fe7b024ef9cc9f7d43eadf3640322b2",
    "es-1440-light-casen-shared-site.png": "716a4afa419da0eac51b54e3beb0f1ed0a39c27cfedd41adc1780ac56ed318dd",
    "es-390-light-casen-right-bottom.png": "67b80471c56c7cca314e397cf79b042c3b34ba1b66a44e60d7a8d69538d741e8",
    "en-390-academic-night-casen-shared-site.png": "0c73730b35b6f287f41ac99d884cdfba030b8018b2cf1a049b4ace2153c8dcfa",
    "es-1440-academic-night-monetary-top15.png": "a0deeadc66781607591176267ff27094e8feec8b0a4d7bc790aff34d954e8417",
    "contrast-bounds.json": "d75e92fe0af9310446f6723c467b6308b7f924320f4037eee516c68b0dc12503",
    "es-390-academic-night-casen-shared-site.png": "0007bc81a7edaf66c6faf882d24068629bd5ce297fbc369ae02e571837e47e6e",
    "es-1440-academic-night-axe.json": "8cb96fc634e2c8cee1a2b4306a31c84d9cd83720a36e7c8d22fdb065852de63c",
    "es-390-academic-night.json": "a733976fe330d7aee75284c693ee8046e10de826306954e901258022b3a5d87f",
    "es-390-academic-night-monetary-top15.png": "8f549117a8b45f5a1761e90264148d7e95d6c9cf5219829edc5641aed59af823",
    "en-390-academic-night.json": "9531a4c372141cba96c5464bdac8a56d7727c4354bbe75add0081e8ab7a72afa",
    "fiscal-tables-matrix.json": "d179ca757584ab340fa75baf27fd360f8f0aabf036a694b90e084550ba5cd7ed",
    "es-390-light-monetary-top15.png": "3525b12201bd2f410d1c3f8b25cfa2aa9a263cb07db94566844db3eb4ae2f612",
    "run-fiscal-tables-qa.py": "865599c58b5fbd9b3ad826bcfad0eb2999507a344a84d2e7777c3bb64e982f91",
    "es-390-academic-night-axe.json": "8cb96fc634e2c8cee1a2b4306a31c84d9cd83720a36e7c8d22fdb065852de63c",
    "en-1440-light-fiscal-tables-axe.json": "d7474a73da16f2abaddca56c00d2da867defe22dcaf3dcd2d1ff36bc1e2b97c6",
    "en-390-academic-night-axe.json": "92209af87581d64efac191481455bc6608470957e3f44eb80f4e9b1ecb651a83",
    "en-390-light.json": "e37c678aeb6aa21c45c254121582f11134771ab60cab31b49ba5ebd4c7f9a7d7",
    "en-1440-academic-night-monetary-top15.png": "6043438b4a210eee511b87ddbdb56014581d3de70b141a43899e94b39d0d6af5",
    "en-390-light-monetary-top15.png": "fcba944926a2af6d3a4f6e2c5b6109cd20fd85d14cf1e8eda57bd19e8adb43f0",
    "en-390-light-fiscal-tables-axe.json": "d7474a73da16f2abaddca56c00d2da867defe22dcaf3dcd2d1ff36bc1e2b97c6",
    "es-1440-light.json": "9e025b58543f10919b1763d5d3c867af9642f8ece34ae8641c87d18017933ae4",
    "es-1440-academic-night-fiscal-tables-axe.json": "956439c796012c3b6a5e152199ba814df54108b5b27c3e6bc03887ec12765128",
    "en-1440-academic-night.json": "0a3eab816beafc28bbb941fcfc1489cbc39dbd39d362a9907effd86bc8023647",
    "en-390-light-casen-right-bottom.png": "43348d036581d24c5b28a505872c76b030fbfe1e2bb3fecbe82f994e40d48832",
    "es-390-light.json": "024d40c2ed3a33f6718b6205ed6bb48fe6797fe6459ad282efd82cec212e2152",
    "es-1440-academic-night-casen-shared-site.png": "166066ed6cd7d74136c1a0e0bcb5ba068adc56b6ef8a5a988d0c25dc122a551c",
    "en-1440-academic-night-casen-shared-site.png": "d416293c0e1ea8a16eacee7d02c7bda440dac4b61e5e52310ca9f2b317580396",
    "en-390-academic-night-casen-right-bottom.png": "3ef3141980db9c3ff792ac848040588429e0af9e44e2ef1ff8744fdfa277ddcd"
  },
  "fiscal_tables_additional_scope": {
    "cases": 8,
    "tables_per_case": 2,
    "rows_per_table": 15,
    "tabindex": 0,
    "body_overflow": false,
    "matrix": "fiscal-tables-matrix.json",
    "axe_counts": {
      "es-390-light": {
        "inapplicable": 69,
        "incomplete": 1,
        "passes": 19,
        "violations": 0
      },
      "es-390-academic-night": {
        "inapplicable": 69,
        "incomplete": 1,
        "passes": 19,
        "violations": 0
      },
      "es-1440-light": {
        "inapplicable": 69,
        "incomplete": 1,
        "passes": 19,
        "violations": 0
      },
      "es-1440-academic-night": {
        "inapplicable": 69,
        "incomplete": 1,
        "passes": 19,
        "violations": 0
      },
      "en-390-light": {
        "inapplicable": 69,
        "incomplete": 1,
        "passes": 19,
        "violations": 0
      },
      "en-390-academic-night": {
        "inapplicable": 69,
        "incomplete": 1,
        "passes": 19,
        "violations": 0
      },
      "en-1440-light": {
        "inapplicable": 69,
        "incomplete": 1,
        "passes": 19,
        "violations": 0
      },
      "en-1440-academic-night": {
        "inapplicable": 69,
        "incomplete": 1,
        "passes": 19,
        "violations": 0
      }
    }
  },
  "axe_audit_total": 16,
  "science_label_check": {
    "status": "pass",
    "method": "Rendered HTML CASEN alt/caption/table and explanatory paragraphs inspected in ES/EN",
    "observed": "Explicit household denominator and own-site-sharing declaration; explicit distinction from dwelling/site proportion; communal cases marked exploratory without CI."
  }
}
```


## Reported evidence V1/receipt.json
```json
{
  "task_id": "V1",
  "status": "implemented_and_verified",
  "source_sha256": "b192b57607badd8fac36f42f4e5bc3132b4239ecb05ed7a0904998f91121a9ce",
  "accepted_review_digest": "14eaab859814dda0d89066b79c7b395b8e1cbb3e90aa7e65f5f080fe3dddec80",
  "code_sha256": {
    "scripts/catastro_sii/render_casen_shared_site.py": "2d230ff53406d7375f28bf59cda7c055b04697a874b5c624b578271f45bf36ea",
    "tests/catastro_sii/test_casen_shared_site_figure.py": "a05b08d3ef7895a1afab34eb7dc1cd162fb2ceeb3024f86b00cda4854e127179"
  },
  "artifacts": [
    {
      "file": "casen-shared-site-es.svg",
      "sha256": "a07067dd96040364c361f52ef5f3c02e91f646a086051e7ad26ac1b39a7107c5",
      "bytes": 93408
    },
    {
      "file": "casen-shared-site-es.png",
      "sha256": "b840fe7d44b1a41b172d2a4554242d7d1c243b957ad23c0115e590de38da2e0a",
      "bytes": 436727
    },
    {
      "file": "casen-shared-site-es-dark.svg",
      "sha256": "1bcbe6130fb5f120c1068f4d62e313d6173e4040d3e5ae6422033b3c6e4f9387",
      "bytes": 93408
    },
    {
      "file": "casen-shared-site-es-dark.png",
      "sha256": "6843d14c83ae801c2ef6598b9b31941b4705185ed9e9be2e300fbc95ec353c7c",
      "bytes": 425915
    },
    {
      "file": "casen-shared-site-en.svg",
      "sha256": "82dfb42a57697b6fdab66819209ab28b265057f6f92d1cacaac55f09a2db656c",
      "bytes": 92934
    },
    {
      "file": "casen-shared-site-en.png",
      "sha256": "370fa28ca634cf41026f9b6419291e039f3a67734e068fffc10f16b4101e87b6",
      "bytes": 430462
    },
    {
      "file": "casen-shared-site-en-dark.svg",
      "sha256": "3ad629729eb39746c4fcb8defcacd8057e4a80a50942f5202c8e1e6820198c09",
      "bytes": 92934
    },
    {
      "file": "casen-shared-site-en-dark.png",
      "sha256": "b323e886f367cf43e82516313a5b28820d51e575a34e9ad69a09fc224a571b94",
      "bytes": 420929
    },
    {
      "file": "casen-shared-site-data.json",
      "sha256": "07607fa341918c3b65e9cb68e7574fe6ba50d3b06ced6876cd9e44fc4ca864a9",
      "bytes": 15537
    },
    {
      "file": "casen-shared-site-data.csv",
      "sha256": "5cc27edc9e5be7e645037fdf6814dc60b2f916a04eca2c52758618cd00665eb9",
      "bytes": 7346
    },
    {
      "file": "casen-shared-site-provenance.json",
      "sha256": "3b1960bae36e089e2415dc1bcced298adcbdd9ea901a3597f8e7d22fb59f1094",
      "bytes": 2956
    }
  ],
  "commands": [
    {
      "command": "/opt/entornos/mamba312/bin/python -m unittest discover -s tests/catastro_sii -p test_casen_shared_site_figure.py -v",
      "exit_code": 0,
      "tests": 12
    },
    {
      "command": "/opt/entornos/mamba312/bin/python scripts/catastro_sii/render_casen_shared_site.py --expected-sha256 b192b57607badd8fac36f42f4e5bc3132b4239ecb05ed7a0904998f91121a9ce",
      "exit_code": 0
    }
  ],
  "falsified_by": [
    {
      "case": "bad-ci",
      "exit_code": 1,
      "no_outputs": true,
      "error": "ValueError: Invalid confidence interval: ('national', 'CL')"
    },
    {
      "case": "missing-is-zero",
      "exit_code": 1,
      "no_outputs": true,
      "error": "ValueError: Invalid estimate/denominator: ('commune', '5101')"
    },
    {
      "case": "forged-communal-ci",
      "exit_code": 1,
      "no_outputs": true,
      "error": "ValueError: Unavailable CI must remain null: ('commune', '5101')"
    }
  ],
  "green_recovery": "render-recovery.json",
  "repeated_render_all_11_artifacts_identical": true,
  "fiscal_aggregate_hashes_unchanged": 9,
  "exact_exported_source_rows": 19,
  "dimensions": {
    "inches": [
      12,
      13.4
    ],
    "svg_points": [
      864,
      964.8
    ],
    "intrinsic_css_px": [
      1152,
      1286.4
    ],
    "png_px": [
      2160,
      2412
    ],
    "minimum_display_width_css_px": 1000
  },
  "inspected_with_view_image": [
    "casen-shared-site-es.png",
    "casen-shared-site-en-dark.png"
  ],
  "fonts": "Embedded subsets through unchanged editorial_style.py; source SVG text retained",
  "limits": [
    "Regional Taylor intervals remain approximate, not causal effects.",
    "Two communes selected after prior exploration; no communal representativeness or CI.",
    "The estimand is households, not dwellings/sites; never applied as a fiscal adjustment.",
    "No browser integration test here; E1/Q1 owns actual scroll/zoom/table embedding.",
    "Physical iPhone/Safari not verified.",
    "No original data, V0, shared style, posts or catalog changes."
  ]
}
```


## Reported evidence V1/red-controls.json
```json
[
  {
    "case": "bad-ci",
    "exit_code": 1,
    "no_outputs": true,
    "error": "ValueError: Invalid confidence interval: ('national', 'CL')"
  },
  {
    "case": "missing-is-zero",
    "exit_code": 1,
    "no_outputs": true,
    "error": "ValueError: Invalid estimate/denominator: ('commune', '5101')"
  },
  {
    "case": "forged-communal-ci",
    "exit_code": 1,
    "no_outputs": true,
    "error": "ValueError: Unavailable CI must remain null: ('commune', '5101')"
  }
]
```


## Reported evidence V0-portability/receipt.json
```json
{
  "task_id": "V0-portability",
  "status": "implemented_and_verified",
  "source_sha256": "c21b29389e3a3f0c3d90d7383ac5d19c41851a67d308261a6db841d70e6badfc",
  "code_sha256": {
    "scripts/catastro_sii/editorial_style.py": "0f415f9675ec51ce2716a0225560754064b176020df2a7030300c1fb2328d35e",
    "scripts/catastro_sii/render_gap_figures.py": "1aa579cb8c59e5d7dc21cb17b1f48ca30fd44b6a9a0cd8bf0b4a690aad8aa4ff",
    "scripts/catastro_sii/modeled_fiscal_projection.py": "7ac0f9ecf7287cb2d988c210eae0a483bd5bfb8331d01e5a2e73b0d8f9b2ed5b",
    "tests/catastro_sii/test_editorial_figures.py": "d3b3cf93e4f5d360625834d92094ca86c5c942f9ceb7bbf6a7854f2adf003407"
  },
  "artifacts": [
    {
      "file": "gap-top15-es.svg",
      "sha256": "b4b04d89659d8761a6188a9e075d3fe1e12163ee3c36b782a097b5ec5c52e454",
      "bytes": 76205
    },
    {
      "file": "gap-top15-es.png",
      "sha256": "ad75af1a165a52ec6b615135c3a1f0b8e7adc451bce121546d82a51ae80999ac",
      "bytes": 306888
    },
    {
      "file": "gap-top15-es-dark.svg",
      "sha256": "45caff806cc17477a6ece053c5ced08332c89c53fee8c21fb7c554d5f583199e",
      "bytes": 76205
    },
    {
      "file": "gap-top15-es-dark.png",
      "sha256": "3354171dc80f79cd42fbd164673ed9f4ee27c75844e7b20c1bf136b51a89de4a",
      "bytes": 298551
    },
    {
      "file": "gap-top15-en.svg",
      "sha256": "fc584c2a855debcdcef7c2ddd9464ea218f883235f9c90ef2aa2735a8c957c3d",
      "bytes": 76310
    },
    {
      "file": "gap-top15-en.png",
      "sha256": "b668f681f4d13cd97b077c235ff778c465d85f299d883d6397b72d35830126aa",
      "bytes": 313543
    },
    {
      "file": "gap-top15-en-dark.svg",
      "sha256": "29c7b0bb710a52113af73d4d4cafb7632fea472be12d6df62f80fb10eddbd6ef",
      "bytes": 76310
    },
    {
      "file": "gap-top15-en-dark.png",
      "sha256": "7beb95a6e2662ab4f74d61a0eca0a318e41a23ef788f2bfe1ff3fe943d0b868e",
      "bytes": 304415
    },
    {
      "file": "monetary-top15-es.svg",
      "sha256": "39329925152b791a93622958ba6509390671bd43c803cff06861f38818a48d46",
      "bytes": 67174
    },
    {
      "file": "monetary-top15-es.png",
      "sha256": "cd7a1538f9879561a4f895c06f682496f3ec4978578af3ac7e2b5130564929aa",
      "bytes": 267328
    },
    {
      "file": "monetary-top15-es-dark.svg",
      "sha256": "bcc3fea5479ae668729b401a776c43fdda56b92b1a5c511fd4437fd8c9555461",
      "bytes": 67174
    },
    {
      "file": "monetary-top15-es-dark.png",
      "sha256": "f3f52ee25797989430d9f4b9f52d46f32fbbdc1971836a13759955f4ba666fda",
      "bytes": 259094
    },
    {
      "file": "monetary-top15-en.svg",
      "sha256": "2805ee1a09fb2fdb1eeeb9f7090dec05d582320bbe97ebed5021b8a9ae101402",
      "bytes": 67674
    },
    {
      "file": "monetary-top15-en.png",
      "sha256": "f2ae6abbdf69f89bed6f833953b39337f8321376639f984bee2efd547edb8a14",
      "bytes": 261438
    },
    {
      "file": "monetary-top15-en-dark.svg",
      "sha256": "47c845ceeb206ef99c52d97aa3b64a120d971b6d2fbc85a8397d62a610636060",
      "bytes": 67674
    },
    {
      "file": "monetary-top15-en-dark.png",
      "sha256": "fd1e48a4c9f0e6b683700d80adadc6a8049dfc41fe6f5eef8c8a2842277b1cad",
      "bytes": 253477
    }
  ],
  "commands": [
    {
      "command": "/opt/entornos/mamba312/bin/python -m unittest discover -s tests/catastro_sii -p test_editorial_figures.py -v",
      "exit_code": 0,
      "tests": 15
    },
    {
      "command": "/opt/entornos/mamba312/bin/python scripts/catastro_sii/render_gap_figures.py --expected-sha256 c21b29389e3a3f0c3d90d7383ac5d19c41851a67d308261a6db841d70e6badfc",
      "exit_code": 0,
      "runs": 2
    }
  ],
  "falsified_by": [
    {
      "fixture": "before/gap-top15-es.svg",
      "criterion": "assert_embedded_font_contract",
      "exit_code": 1,
      "evidence": "old-svg-red.log"
    },
    {
      "fixture": "valid embedded SVG with subset reduced to character A",
      "criterion": "glyph coverage",
      "result": "AssertionError caught by test_font_gate_rejects_missing_embedding_and_missing_glyphs"
    }
  ],
  "font_subset": {
    "family": "Cucharadas Figure",
    "weights": [
      400,
      700
    ],
    "source": "existing FiraSans Regular/Bold WOFF2",
    "preserved": "copyright, OFL license, source links, selectable text",
    "renamed": "internal family and PostScript names avoid reserved Fira name",
    "no_external_font_request": true
  },
  "observed_browser": {
    "img": {
      "all_pixels": 1183104,
      "embedded_vs_fallback_changed_pixels": 56848,
      "file_vs_data_uri_changed_pixels": 0,
      "ua": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) HeadlessChrome/151.0.0.0 Safari/537.36"
    },
    "standalone": {
      "loadedFonts": [
        {
          "family": "Cucharadas Figure",
          "status": "loaded",
          "weight": "400"
        },
        {
          "family": "Cucharadas Figure",
          "status": "loaded",
          "weight": "700"
        }
      ],
      "resources": [],
      "selectableTextNodes": 80,
      "url": "http://127.0.0.1:4087/gap-top15-es.svg"
    },
    "screenshot": "browser-standalone-full.png"
  },
  "repeated_render_identical_16": true,
  "all_png_unchanged_8": true,
  "fiscal_source_hashes_unchanged_9": true,
  "max_svg_bytes": 76310,
  "documents": [
    "https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image",
    "https://openfontlicense.org/webfonts-and-reserved-font-names/"
  ],
  "limits": [
    "Chromium151 Linux measured; no physical iPhone/Safari verification.",
    "Existing fonts and glyph outlines reused; PNGs unchanged.",
    "SVG-as-img selectable text requires opening standalone SVG; image embedding still requires equivalent HTML table.",
    "Previous evidence preserved in /tmp/avaluos-v0-evidence and before/.",
    "Temporary HTTP server and isolated browser closed."
  ]
}
```


## Current hero and disclosure styles
```scss
/* Shared article hero. The image is decorative; its description and provenance
   remain available in the linked transparency policy. Home keeps its own art direction. */
.page__hero--overlay.page__hero--editorial {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  min-height: 16rem;
  display: grid;
  align-content: center;
  padding: 2rem 0 3.1rem;
  background: #090b18;
  color: #f4f6ff;
  .page__hero-media, .page__hero-shade { position: absolute; inset: 0; z-index: -1; }
  .page__hero-media img { width: 100%; height: 100%; object-fit: cover; }
  .page__hero-shade { background: linear-gradient(90deg, rgba(9,11,24,.96), rgba(9,11,24,.72) 45%, rgba(9,11,24,.18)); }
  .wrapper { width: 100%; }
  .page__title {
    max-width: 25ch;
    font-size: clamp(1.6rem, 3vw, 2.4rem);
    font-weight: 500;
    line-height: 1.18;
    letter-spacing: -.02em;
    text-transform: none;
    overflow-wrap: anywhere;
    color: #f4f6ff;
    text-shadow: 0 1px 3px #090b18;
  }
  .page__meta, .page__lead { color: #f4f6ff; opacity: 1; }
  .page__lead { max-width: 42ch; }
  .page__hero-caption { max-width: 100%; padding: .4em .8em; background: #10121d; color: #f4f6ff; opacity: 1; font-size: .7rem; line-height: 1.5; }
  .page__hero-caption a { color: inherit; text-decoration: underline; }
  a:focus-visible { outline: 3px solid #ffdb7d; outline-offset: 3px; }
}
.ai-disclosure { margin: 0 0 1rem; font-size: .72rem; line-height: 1.6; color: #4c5668; }
.ai-disclosure a { color: #174d8c; text-decoration: underline; text-underline-offset: .15em; }
.ai-disclosure a:focus-visible { outline: 3px solid #1662a8; outline-offset: 3px; }
html[data-theme="academic-night"] .ai-disclosure { color: #bdc5d8; }
html[data-theme="academic-night"] .ai-disclosure a { color: #a8ccff; }
html[data-theme="academic-night"] .ai-disclosure :focus-visible { outline-color: #ffdb7d; }
@media (max-width: 1023px) {
  .page__hero--overlay.page__hero--editorial {
    min-height: 0;
    padding-top: 1.5rem;
    .page__hero-shade { background: rgba(9,11,24,.83) !important; }
    .page__title { max-width: 100%; font-size: 1.6rem; }
    .page__hero-caption { position: static; margin-top: 1rem; justify-self: start; }
  }
}

```


## Current hero template
```liquid
{% assign active_lang = site.active_lang | default: page.lang | default: site.default_lang | default: "es" %}
{% assign ui_text = site.data.ui-text[active_lang] | default: site.data.ui-text[site.locale] %}
{% assign brand = site.data.brand[active_lang] | default: site.data.brand[site.default_lang] %}
{% assign editorial_hero = false %}
{% if page.id and page.header.overlay_image %}{% assign editorial_hero = true %}{% endif %}
{% capture overlay_img_path %}{{ page.header.overlay_image | relative_url }}{% endcapture %}

{% if page.header.overlay_filter contains "gradient" %}
  {% capture overlay_filter %}{{ page.header.overlay_filter }}{% endcapture %}
{% elsif page.header.overlay_filter contains "rgba" %}
  {% capture overlay_filter %}{{ page.header.overlay_filter }}{% endcapture %}
  {% capture overlay_filter %}linear-gradient({{ overlay_filter }}, {{ overlay_filter }}){% endcapture %}
{% elsif page.header.overlay_filter %}
  {% capture overlay_filter %}rgba(0, 0, 0, {{ page.header.overlay_filter }}){% endcapture %}
  {% capture overlay_filter %}linear-gradient({{ overlay_filter }}, {{ overlay_filter }}){% endcapture %}
{% endif %}

{% if page.header.image_description %}
  {% assign image_description = page.header.image_description %}
{% else %}
  {% assign image_description = page.title %}
{% endif %}

{% assign image_description = image_description | markdownify | strip_html | strip_newlines | escape_once %}

<div class="page__hero{% if page.header.overlay_color or page.header.overlay_image %}--overlay{% endif %}{% if editorial_hero %} page__hero--editorial{% endif %}"
  style="{% if page.header.overlay_color %}background-color: {{ page.header.overlay_color | default: 'transparent' }};{% endif %} {% if page.header.overlay_image and editorial_hero == false %}background-image: {% if overlay_filter %}{{ overlay_filter }}, {% endif %}url('{{ overlay_img_path }}');{% endif %}"
>
  {% if editorial_hero %}
    <picture class="page__hero-media" aria-hidden="true">
      <img src="{{ page.header.overlay_image | relative_url }}"{% if page.header.overlay_image_mobile %} srcset="{{ page.header.overlay_image_mobile | relative_url }} 800w, {{ page.header.overlay_image | relative_url }} 1600w" sizes="100vw"{% endif %} width="1600" height="900" alt="" fetchpriority="high" loading="eager" style="object-position: {{ page.header.focal_point | default: '65% center' | escape }};">
    </picture>
    <span class="page__hero-shade" aria-hidden="true"{% if overlay_filter %} style="background-image: {{ overlay_filter | escape }};"{% endif %}></span>
  {% endif %}
  {% if page.header.overlay_color or page.header.overlay_image %}
    <div class="wrapper">
      <h1 id="page-title" class="page__title" itemprop="headline">
        {% if paginator and site.paginate_show_page_num %}
          {{ site.title }}{% unless paginator.page == 1 %} {{ ui_text.page | default: "Page" }} {{ paginator.page }}{% endunless %}
        {% else %}
          {{ page.title | default: site.title | markdownify | remove: "<p>" | remove: "</p>" }}
        {% endif %}
      </h1>
      {% if page.ref == "home" %}
        <p class="page__lead">{{ brand.description }}</p>
      {% elsif page.tagline %}
        <p class="page__lead">{{ page.tagline | markdownify | remove: "<p>" | remove: "</p>" }}</p>
      {% elsif page.header.show_overlay_excerpt != false and page.excerpt %}
        <p class="page__lead">{{ page.excerpt | markdownify | remove: "<p>" | remove: "</p>" }}</p>
      {% endif %}
      {% include page__meta.html %}
      {% if page.header.actions %}
        <p>
        {% for action in page.header.actions %}
          {% assign action_label = action.label %}
          {% if active_lang == "en" and action.label_en %}
            {% assign action_label = action.label_en %}
          {% elsif active_lang == "es" and action.label_es %}
            {% assign action_label = action.label_es %}
          {% endif %}
          <a href="{{ action.url | relative_url }}" class="btn btn--light-outline btn--large">{{ action_label | default: ui_text.more_label | default: "Learn More" }}</a>
        {% endfor %}
        </p>
      {% endif %}
    </div>
  {% else %}
    <img src="{{ page.header.image | relative_url }}" alt="{{ image_description }}" class="page__hero-image">
  {% endif %}
  {% if editorial_hero %}
    <span class="page__hero-caption"><a href="{{ '/ai-transparency/' | relative_url }}#{{ page.ref | escape }}">{% if page.ai_disclosure.components.hero == 'generated' %}{% if active_lang == 'en' %}I created this cover with AI{% else %}Creé esta portada con IA{% endif %}{% elsif page.ai_disclosure.components.hero == 'human' %}{% if active_lang == 'en' %}I use a human-created cover{% else %}Uso una portada de autoría humana{% endif %}{% else %}{% if active_lang == 'en' %}I have not documented this cover’s origin{% else %}No tengo documentado el origen de esta portada{% endif %}{% endif %}</a></span>
  {% elsif page.header.caption %}
    <span class="page__hero-caption">{{ page.header.caption | markdownify | remove: "<p>" | remove: "</p>" }}</span>
  {% endif %}
</div>

```


## First CASEN post correction (both languages)

CASEN 2024 tiene diseño **estratificado bietápico probabilístico** ([nota metodológica BIDAT](https://bidat.gob.cl/url/69b71c77197db)). El factor `expr` corresponde a estimaciones nacionales y regionales. El factor complementario `expc` permite cálculos descriptivos comunales, pero **no vuelve representativas las estimaciones de cada comuna**, según la [nota oficial de uso de CASEN 2024](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf). Este análisis usa `expr` y reporta estimaciones por región con IC 95 % calculados por **Taylor linearization** sobre el diseño complejo (estratos, UPM/PSU y pesos/factores).
2. **¿Estás usando el factor de expansión correcto?** `expr` corresponde a los dominios nacional y regional; disponer de `expc` no garantiza representatividad comunal. Los factores no son intercambiables y deben acompañarse del dominio y alcance de la inferencia.
CASEN 2024 has a **probabilistic stratified two-stage** design ([BIDAT methodological note](https://bidat.gob.cl/url/69b71c77197db)). The `expr` factor applies to national and regional estimates. The complementary `expc` factor supports descriptive commune calculations, but **does not make estimates representative of each commune**, according to the [official CASEN 2024 data-use note](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf). This analysis uses `expr` and reports estimates by region with 95% CIs computed by **Taylor linearization** over the complex design (strata, PSU/UPM and weights/factors).
2. **Are you using the correct expansion factor?** `expr` applies to national and regional domains; having `expc` does not guarantee commune representativeness. The factors are not interchangeable, and the domain and scope of inference must be stated.