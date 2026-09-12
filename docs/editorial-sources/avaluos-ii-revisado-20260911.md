---
layout: single
title: "Avalúos II: dónde conviene revisar el catastro residencial"
subtitle: "Campamentos, materialidad y avalúos para pasar de una diferencia comunal a una revisión predial"
date: 2026-09-09 20:00:00 -0400
categories: [datos, territorio]
tags: [catastro-sii, censo-2024, contribuciones, datos-abiertos, desigualdad]
author: clabra
lang: es
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: false
editorial_status: pendiente-conciliacion-fiscal
description: "Una comparación entre viviendas del Censo 2024 y roles habitacionales del SII, con escenarios de campamentos y materialidad, para orientar la revisión del catastro."
excerpt: "Una diferencia entre registros puede justificar una revisión. Para hablar de contribuciones omitidas, primero hay que identificar los inmuebles y comprobar su situación tributaria."
header:
  teaser: /assets/images/avaluos-ii/gap-top15-es.png
math: true
toc: true
toc_sticky: true
comments: true
---

En el [primer post de avalúos](/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/), cambiar el denominador cambiaba el mapa. Ahora me interesa una pregunta anterior al impuesto: **si el Censo cuenta más viviendas que los roles habitacionales del SII, ¿por dónde conviene empezar a revisar?**

Cruzo esa diferencia con campamentos, materialidad y avalúos para ordenar la búsqueda. El recorrido tiene tres pasos: entender qué estamos restando, distinguir dónde podría haber interés tributario y precisar qué evidencia permitiría comprobarlo.

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

El contraste sirve para formular una pregunta: **si se encontraran inmuebles omitidos y fueran comparables a los registrados, ¿qué implicaría incorporarlos o actualizar su avalúo?** No estima cuántos aparecerán ni cuánto deberían pagar.

La condición de semejanza es la más difícil. Lo que falta en un registro puede diferir sistemáticamente de lo que entró: construcciones más pequeñas, viviendas en predios agrícolas o inmuebles bajo un rol matriz. Trasladarles el perfil de avalúos observado introduciría un sesgo de selección. Este filtro tampoco mide la discrepancia proporcional ni el costo de investigar cada comuna; es un punto de partida, no una priorización óptima demostrada.

## Tercera cucharada: comprobar el inmueble antes de calcular el impuesto

La comparación comunal permite elegir dónde mirar. Para resolver la pregunta tributaria hay que bajar al predio: **identificar la construcción, encontrar su relación con uno o más roles y reconstruir sus fechas**. La revisión debe admitir tanto una omisión como una explicación que la descarte.

| Posible explicación | Qué habría que contrastar | Qué debilitaría esa explicación |
|---|---|---|
| Predio o construcción omitidos | Ubicación, antecedentes de terreno y construcción, roles y expediente catastral | El inmueble ya está incorporado correctamente, incluso bajo otro rol o destino |
| Avalúo desactualizado | Superficie y características construidas frente al detalle catastral y sus fechas | El avalúo ya incorpora esas características |
| Diferencia de unidades o períodos | Viviendas por predio, roles matrices, destinos agrícolas, copropiedad y fechas comparables | La discrepancia persiste después de conciliar unidades y períodos |
| Error de fuente o procesamiento | Integridad del extracto, claves territoriales y reproducción independiente | El resultado se reproduce con fuentes y cruces independientes |

**Incorporar un predio y actualizar una construcción no son lo mismo.** El SII dispone de un [procedimiento de inclusión de bienes raíces][sii-inclusion]. También contempla modificaciones del avalúo. Una ampliación puede aumentar el valor de un rol existente sin crear otro: la diferencia entre viviendas y roles no detecta por sí sola toda desactualización del catastro.

### Por qué todavía no hay una cifra en pesos

Antes de calcularla faltan dos comprobaciones: identificar qué inmuebles requieren una modificación y determinar qué obligación tributaria corresponde a cada uno, con sus fechas y exenciones.

También hay una limitación de las fuentes utilizadas. El campo semestral del extracto no permite separar todos los componentes de la contribución neta habitacional. Los cuadros comunales oficiales revisados distinguen componentes, pero abarcan otros destinos no agrícolas. **Dividir ese total por roles habitacionales produciría un promedio de universos incompatibles.** La [auditoría de fuentes](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) registra ese pendiente.

Determinar un impuesto, girarlo y recaudarlo son etapas distintas. El SII determina los avalúos y giros; la [Tesorería General de la República recauda][tgr-impuestos]. Además, la distribución mediante el [Fondo Común Municipal][sii-fcm] impide equiparar el impuesto asociado a una comuna con ingresos retenidos íntegramente por su municipio.

La guía de Grote y Wen (2024, 16–18) ayuda a ordenar el problema: distingue cobertura, valoración y cobro, y propone contrastar cartografía, terreno y registros. Sirve para diseñar una verificación, no para importar un coeficiente de recaudación a estas comunas.

## Cierre: que la diferencia tenga una explicación

Una brecha entre registros merece una explicación, no una deuda inventada. Si se resuelve con roles existentes, destinos o fechas, la hipótesis de omisión pierde fuerza. Si aparecen inmuebles que debieron incorporarse o actualizarse, habrá que determinar sus efectos tributarios caso a caso.

En la próxima entrega exploraré el **Continuo de Construcciones Urbanas (CCU)** para contrastar la huella construida. Antes de atribuir un atraso administrativo, habrá que verificar sus fuentes y reconstruir cuándo ocurrió cada cambio.

[Explorar el diagnóstico](/catastro_sii_brecha/#brecha-contribuciones) · [Descargar CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv).

<details markdown="1">
<summary>Notas metodológicas: fuentes, cortes y límites pendientes</summary>

**Procedencia y cobertura.** El espejo catastral se descargó el 24 de julio de 2026 y corresponde al primer semestre de ese año. No es una descarga directa del SII ni un corte de septiembre. Antártica y Trehuaco carecen de extracto y se mantienen como faltantes, no como comunas sin predios habitacionales.

**Totales todavía no conciliados.** El control [SII por destino][sii-destino] citado informa 6.056.150 predios habitacionales; el extracto reúne 6.054.808. Las [planillas MINVU de parque habitacional][minvu-parque] citadas para 2026S1 informan 6.057.949, incluidos 1.342 de Trehuaco. La diferencia entre el SII y el extracto es de 1.342, pero entre MINVU y el extracto alcanza 3.141. Incorporar los 1.342 de Trehuaco no concilia ambos controles: todavía quedan 1.799 predios de diferencia respecto del total MINVU. No se atribuye esta discrepancia a una causa no comprobada ni se sustituyen silenciosamente los totales.

**Dos cortes de campamentos.** El informe [MINVU publicado el 8 de julio de 2026][minvu-campamentos], con información referida a 2024, registra 1.373 campamentos, 81.993 viviendas ocupadas y 77.399 hogares. La capa CNC 2026 utilizada en este procesamiento contiene 1.345 polígonos y suma 71.760 en el campo `HOGARESCEN`, con 222 polígonos sin dato. Son universos y cortes diferentes. Interpretar ese campo como hogares censales es una decisión provisional, apoyada en su nombre y la documentación disponible, no en un diccionario específico de la capa. El descuento depende de ella.

**Definición de materialidad.** Se utiliza el código del manual INE, cuya clasificación no coincide por completo con la descripción en prosa: para materialidad aceptable, esta última admite algunas paredes recuperables, mientras el código exige materiales aceptables en los tres componentes. El escenario combina ese criterio con el tipo aceptable de vivienda. Se conservan variantes con materiales completos y con la categoría más amplia de no irrecuperables; son análisis de sensibilidad, no intervalos de confianza. El procesamiento registra 4.388 viviendas ocupadas con información incompleta.

**Correcciones del procesamiento documentadas en el borrador.** Se corrigió la homologación territorial de Coyhaique, Aysén y Chile Chico. El conteo de viviendas irrecuperables pasó de 73.338 a 72.642 —696 menos— al aplicar primero la exclusión de no respuesta del código oficial. Esa corrección no modifica la diferencia viviendas–roles ni el descuento por campamentos. La base histórica innominada 2011–2021 no interviene en el cálculo actual.

**Trazabilidad.** El [método](/catastro_sii_brecha/data/fiscal-gap/method.md), la [auditoría](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) y los [datos comunales](/catastro_sii_brecha/data/fiscal-gap/communes.json) son las referencias del procesamiento. Solo se publican agregados comunales.

</details>

## Fuentes y referencias

Grote, Martin, y Jean-François Wen. 2024. *How to Design and Implement Property Tax Reforms*. How to Note 2024/006. Fondo Monetario Internacional, septiembre. [Texto completo][fmi-guia].

Instituto Nacional de Estadísticas (INE). 2025. *Manual de uso de microdatos censales: Censo de Población y Vivienda 2024*. Indicadores viv04–viv06, 103–106. [Manual][ine-manual].

Ministerio de Vivienda y Urbanismo (MINVU), Centro de Estudios de Ciudad y Territorio. 2026. *Caracterización de campamentos en Censo 2024*. Publicado el 8 de julio. Véanse los resultados generales y la tabla 1, 4–5. [Informe][minvu-campamentos].

Servicio de Impuestos Internos (SII). «De avalúo fiscal a contribuciones: paso a paso», ejemplo del primer semestre de 2026; «¿Qué es un avalúo fiscal?»; «¿El avalúo fiscal corresponde a una tasación comercial de la propiedad?», actualización del 8 de abril de 2026; «¿Cómo regularizo una propiedad que no tiene rol de avalúo?», actualización del 7 de abril de 2026; y «¿Para qué sirve el pago del impuesto territorial?». [Cálculo][sii-ejemplo], [avalúo][sii-avaluo], [distinción del valor comercial][sii-comercial], [inclusión][sii-inclusion] y [distribución municipal][sii-fcm].

Tesorería General de la República (TGR). S. f. «Impuestos y tipos de impuestos». Centro de Ayuda TGR. [Fuente][tgr-impuestos].

*Fuentes externas anteriores consultadas el 11 de septiembre de 2026. Los resultados del procesamiento y sus correcciones deben leerse junto con las notas metodológicas.*

[ine-manual]: https://censo2024.ine.gob.cl/wp-content/uploads/2025/12/manual_uso_microdatos_censo2024.pdf
[minvu-campamentos]: https://catalogo.minvu.cl/cgi-bin/koha/opac-retrieve-file.pl?id=7e816aa9c26af8904eab01badfbfc6e6
[minvu-parque]: https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/
[sii-ejemplo]: https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf
[sii-comercial]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_8124.htm
[sii-avaluo]: https://www.sii.cl/destacados/impuesto_territorial/avaluo_fiscal.html
[sii-inclusion]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_1947.htm
[sii-fcm]: https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html
[sii-destino]: https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html
[tgr-impuestos]: https://ayuda.tgr.gob.cl/ayuda/impuestos/impuestos-y-tipos-de-impuestos
[fmi-guia]: https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf
