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
  overlay_image: /assets/images/avaluos-ii/hero-brecha-residencial-tokyo-night-1600x900.webp
  overlay_filter: "linear-gradient(90deg, rgba(9,11,24,0.96) 0%, rgba(9,11,24,0.72) 42%, rgba(9,11,24,0.10) 72%, rgba(9,11,24,0.08) 100%)"
  show_overlay_excerpt: false
  caption: "Ilustración conceptual con IA · no es un mapa real."
  teaser: /assets/images/teasers/teaser-avaluos-ii-brecha-residencial-1280x720.webp
  og_image: /assets/images/avaluos-ii/og-avaluos-ii-brecha-residencial-1200x630.webp
  og_image_alt: "Ciudad residencial nocturna atravesada por una capa conceptual de polígonos catastrales por revisar."
math: true
toc: true
toc_sticky: true
comments: true
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

![Quince comunas con mayor residuo bajo el supuesto de campamentos. La barra conserva la diferencia inicial y separa el descuento supuesto, el escenario de tipo y materiales aceptables y el resto.](/assets/images/avaluos-ii/gap-top15-es.svg)

{% include avaluos-ii-top-es.html %}

**Cómo leer el gráfico.** El largo total conserva la diferencia inicial; sus segmentos distinguen el descuento supuesto por campamentos y la composición hipotética del residuo. Las quince comunas se ordenan por ese residuo, no por materialidad ni por avalúos. La selección tributaria de la segunda cucharada aplica un filtro diferente.

El [visor permite explorar cada comuna y consultar la tabla completa](/catastro_sii_brecha/#brecha-contribuciones). El [anexo de Valparaíso y Puerto Montt](/catastro_sii_brecha/#catastro-anexo) superpone predios, unidades vecinales y campamentos: ayuda a observar relaciones espaciales, pero no identifica por sí solo viviendas omitidas.

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

<figure>
  <img class="avaluos-ii-monetary-light" width="792" height="612" src="/assets/images/avaluos-ii/monetary-top15-es.svg" alt="Escenarios de impuesto general teórico anual equivalente para las quince comunas con residuo positivo y avalúo mediano sobre el monto exento; comparación de media y mediana." loading="lazy">
  <img class="avaluos-ii-monetary-dark" width="792" height="612" src="/assets/images/avaluos-ii/monetary-top15-es-dark.svg" alt="Escenarios de impuesto general teórico anual equivalente para las quince comunas con residuo positivo y avalúo mediano sobre el monto exento; comparación de media y mediana." loading="lazy">
  <figcaption>Millones de pesos bajo el supuesto de que cada unidad del residuo correspondiera a un nuevo predio comparable. Los montos son hipotéticos; no son deuda constatada ni ingresos municipales retenidos.</figcaption>
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
