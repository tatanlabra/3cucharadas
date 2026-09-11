---
layout: single
title: "Avalúos II: dónde la brecha residencial merece una revisión tributaria"
subtitle: "Campamentos, materialidad y avalúos para distinguir las comunas que conviene revisar primero"
date: 2026-09-09 20:00:00 -0400
categories: [datos, territorio]
tags: [catastro-sii, censo-2024, contribuciones, datos-abiertos, desigualdad]
author: clabra
lang: es
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: false
editorial_status: pendiente-conciliacion-fiscal
description: "Una lectura de la brecha Censo–SII con campamentos, escenarios de materialidad y avalúos habitacionales para orientar la revisión del catastro."
excerpt: "Una diferencia persistente, acompañada de avalúos altos en los predios registrados, da motivos para revisar. Falta identificar cada inmueble para hablar de contribuciones omitidas."
header:
  teaser: /assets/images/avaluos-ii/gap-top15-es.png
math: true
toc: true
toc_sticky: true
comments: true
---

**Cómo leer este análisis.** Las barras ayudan a elegir dónde investigar. Combinan una diferencia observada entre registros con escenarios explícitos; todavía no cuentan propiedades omitidas ni pesos sin cobrar.
{: .notice--info}

En el [primer post de avalúos](/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/) cambiábamos el denominador para mirar el territorio de otra manera. Ahora interesa una pregunta de administración pública: **si las viviendas censadas superan a los roles habitacionales, ¿por dónde conviene empezar a revisar?**

La diferencia adquiere otro interés cuando persiste al considerar campamentos y coincide con avalúos altos en los predios que sí están registrados. Si una revisión encuentra allí inmuebles omitidos, comparables a ese stock y con una obligación tributaria exigible, podría descubrir contribuciones que debieron girarse. La secuencia importa: primero encontrar y verificar el inmueble; después determinar el impuesto.

Ese es el propósito de este ejercicio: pasar de una cifra nacional llamativa a una selección territorial argumentada. La comparación puede orientar una revisión; cada conclusión tributaria requiere una comprobación predial.

## Primera cucharada: leer la barra en tres pasos

La base compara **todas las viviendas particulares del Censo 2024**, ocupadas y desocupadas, con los **roles habitacionales del primer semestre de 2026**, identificados por el código de destino **H**. Son unidades distintas: el Censo cuenta viviendas; el SII identifica bienes raíces. Un predio puede contener varias viviendas, y una vivienda puede estar en un rol agrícola excluido por el filtro habitacional. Por eso la resta no se puede llamar «viviendas sin rol».

| Paso | Operación | Qué permite leer |
|---|---|---|
| Diferencia inicial | Viviendas censadas menos roles habitacionales | Dónde los dos recuentos se alejan más |
| Campamentos | Descontar hogares con dato en la capa MINVU, bajo un supuesto uno a uno | Cuánto cambia la diferencia si esos hogares se asignan a ella |
| Materialidad | Aplicar al residuo la proporción comunal de viviendas de tipo y materiales aceptables | Qué tamaño tendría esa parte si el residuo se pareciera al parque observado |

**El largo total conserva la diferencia inicial.** Sus partes muestran el descuento supuesto por campamentos, el escenario de materialidad aceptable y el resto. Las comunas se ordenan por el residuo posterior al descuento de campamentos; el color de materialidad no cambia ese criterio.

![Quince comunas con mayor residuo tras el supuesto por campamentos; cada barra distingue el descuento supuesto y la composición hipotética del resto por materialidad.](/assets/images/avaluos-ii/gap-top15-es.svg)

{% include avaluos-ii-top-es.html %}

En el [visor puedes seleccionar una comuna, explorar la barra y consultar la tabla completa](/catastro_sii_brecha/#brecha-contribuciones). El [anexo cartográfico de Valparaíso y Puerto Montt](/catastro_sii_brecha/#catastro-anexo) superpone predios habitacionales, unidades vecinales y campamentos: permite observar sus relaciones espaciales, sin identificar por sí mismo viviendas omitidas.

### Campamentos: una prueba que cambia mucho algunas comunas

Pensemos en Alto Hospicio: la diferencia inicial es 15.368 y la capa MINVU contiene 9.136 hogares censados en campamentos con dato. Al restarlos queda un residuo de 6.232. El ejercicio reduce la diferencia un 59,4%; **no ha localizado 9.136 viviendas sin rol ni ha determinado su situación tributaria**.

| Comuna | Diferencia inicial | Hogares en campamentos con dato | Residuo del escenario | Reducción |
|---|---:|---:|---:|---:|
| Alto Hospicio | 15.368 | 9.136 | 6.232 | 59,4% |
| Antofagasta | 21.755 | 7.537 | 14.218 | 34,6% |
| Viña del Mar | 24.030 | 8.014 | 16.016 | 33,3% |
| Valparaíso | 32.533 | 2.572 | 29.961 | 7,9% |
| Puerto Montt | 29.036 | 632 | 28.404 | 2,2% |

La suma nacional de diferencias positivas pasa de **1.588.449 a 1.516.689**, una reducción del **4,52%**. El efecto desigual es el hallazgo: este supuesto cambia mucho la lectura de algunas comunas y deja buena parte de la diferencia en otras.

El [MINVU publicó un cruce geográfico entre campamentos y el Censo 2024](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/vivienda-y-deficit/): su fotografía de 2024 contiene 1.373 campamentos, 81.993 viviendas ocupadas y 77.399 hogares. La capa CNC 2026 utilizada aquí es otra fotografía: 1.345 polígonos y 71.760 hogares en el campo de conteo censal, con 222 polígonos sin ese dato. El registro cambia; hogares y viviendas tampoco son intercambiables. En comunas con conteos faltantes, el descuento es parcial.

El supuesto es deliberadamente sencillo: asignar cada hogar contado en un campamento a una unidad de la diferencia. Puede fallar porque varios hogares compartan vivienda, porque el terreno ya tenga un rol matriz o porque las fechas no coincidan. Estar en un campamento no establece una exención automática. De hecho, el SII contempla antecedentes para revisar construcciones no regularizadas, y la ley prevé asignar roles separados a sitios de determinados loteos una vez regularizados. [Documentos requeridos por el SII](https://www.sii.cl/servicios_online/1048-doctos_requeridos-2573.html), [Ley 20.234, artículo 16](https://www.bcn.cl/leychile/Navegar/imprimir?idNorma=268116&idParte=0).

### Materialidad: mirar más allá de la vivienda precaria

El Censo permite distinguir viviendas de **tipo aceptable y con materiales aceptables en paredes, techo y piso simultáneamente**. Es una señal más exigente que simplemente «no irrecuperable». Describe componentes constructivos; no mide lujo, conservación integral, superficie, legalidad ni valor fiscal. La clasificación sigue el código del [manual de microdatos INE, indicadores viv04–viv06, pp. 103–106](https://censo2024.ine.gob.cl/wp-content/uploads/2025/12/manual_uso_microdatos_censo2024.pdf).

En la base pública, de 6.408.172 viviendas particulares ocupadas con moradores presentes, **5.774.146 cumplen ese criterio**. Para explorar la composición del residuo usamos la proporción de cada comuna sobre todas sus viviendas de ese universo. Los datos faltantes quedan fuera del grupo aceptable.

Un ejemplo ilustrativo: si después del supuesto por campamentos quedaran 9.000 unidades y el 80% del parque observado tuviera materialidad aceptable, la barra asignaría **7.200 al escenario aceptable y 1.800 al resto**. No significa que se hayan encontrado 7.200 viviendas aceptables sin catastro: proyecta una composición conocida sobre una diferencia cuyo contenido todavía no conocemos.

Esta extrapolación puede sobrestimar la proporción si las viviendas efectivamente omitidas son más precarias que las observadas; también podría subestimarla si predominan construcciones nuevas con materiales aceptables. Además, el residuo usa viviendas ocupadas y vacantes, mientras la materialidad se observa en viviendas ocupadas con moradores presentes. El método conserva alternativas con materiales completos y con la categoría más amplia de no irrecuperables para mostrar cuánto depende el resultado de esas decisiones. **No multiplicamos materialidad por la proporción de roles sobre el umbral tributario:** pertenecen a registros distintos y desconocemos su distribución conjunta.

No sumamos otro descuento por vivienda irrecuperable: desconocemos cuánto se superpone con campamentos. La base histórica innominada 2011–2021 tampoco alimenta el cálculo actual.

## Segunda cucharada: por qué importan los avalúos de lo que sí vemos

Una brecha grande y una brecha con interés tributario pueden estar en lugares diferentes. Para distinguirlas, el visor incorpora tres referencias de los **predios habitacionales observados en cada comuna**: avalúo medio, avalúo mediano y proporción que supera el monto exento general.

El monto exento habitacional era **$60.030.710 en el primer semestre de 2026**, el mismo período del extracto. Se compara el avalúo de cada predio con ese valor; no se aplica una tasa tributaria al promedio comunal. Superarlo identifica una característica del avalúo observado, pero otros beneficios o exenciones pueden afectar el giro. [Ejemplo oficial SII para 2026S1](https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf).

Tampoco estamos comparando precios de venta. El [SII distingue expresamente avalúo fiscal y valor comercial](https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_8124.htm), y su metodología considera terreno, construcción, localización, superficie y otras características. Una casa de materiales aceptables en suelo de poco valor puede quedar bajo el monto exento; una construcción modesta en suelo caro puede situarse sobre él. [Cómo se forma el avalúo fiscal](https://www.sii.cl/destacados/impuesto_territorial/avaluo_fiscal.html).

La media resume el valor total por rol, pero unas pocas propiedades muy caras pueden elevarla. La mediana ubica el centro de la distribución, y la proporción sobre el monto exento muestra qué tan extendida está esa condición. Las tres lecturas se complementan.

**El criterio de revisión es condicional:** una diferencia que persiste, un escenario de materialidad aceptable de tamaño relevante y una distribución de avalúos habitacionales desplazada sobre el monto exento justifican examinar el territorio con mayor detalle. Si aparecen predios omitidos comparables a los registrados, aumenta el interés de verificar su incorporación y su avalúo. Esta es una prioridad de investigación, no una probabilidad de omisión estimada.

### Quince comunas con dos señales que conviene contrastar

Un filtro transparente selecciona comunas con **residuo positivo y mediana de avalúos habitacionales superior a $60.030.710**. Cumplen estas 15, ordenadas por residuo. Es un punto de partida reproducible: no un ranking de deuda ni de probabilidad de evasión.

| Comuna | Residuo | Escenario de tipo y materiales aceptables | Avalúo mediano habitacional, millones de pesos | Roles habitacionales sobre monto exento |
|---|---:|---:|---:|---:|
| Iquique | 18.949 | 16.964 | $60,24 | 50,4% |
| Pucón | 13.707 | 12.205 | $63,71 | 53,4% |
| Puerto Varas | 8.693 | 7.997 | $61,61 | 51,1% |
| Pirque | 4.883 | 4.090 | $91,85 | 62,2% |
| Algarrobo | 3.201 | 2.876 | $79,72 | 71,1% |
| Santo Domingo | 2.765 | 2.516 | $112,00 | 75,9% |
| Lo Barnechea | 2.300 | 2.202 | $290,03 | 85,6% |
| Huechuraba | 2.297 | 2.118 | $69,73 | 52,5% |
| Concón | 2.005 | 1.888 | $91,82 | 73,3% |
| San Miguel | 1.984 | 1.927 | $63,62 | 55,2% |
| Zapallar | 1.948 | 1.723 | $182,98 | 75,0% |
| La Reina | 1.532 | 1.488 | $122,56 | 83,3% |
| Papudo | 1.213 | 1.092 | $69,05 | 58,1% |
| Providencia | 918 | 908 | $100,40 | 82,6% |
| Las Condes | 542 | 538 | $139,18 | 92,0% |

El escenario se redondea a unidades y los avalúos corresponden exclusivamente a predios registrados. En Iquique, por ejemplo, la media es $73,84 millones y la mediana $60,24 millones, apenas sobre el monto exento: un promedio alto no significa que la mayor parte del stock esté muy lejos del umbral.

Lo Barnechea ilustra otra combinación: un residuo de 2.300, menor que el de las primeras comunas, junto con una mediana de avalúos habitacionales de $290,03 millones y un 85,6% de roles sobre el monto exento. Zapallar también combina un residuo más pequeño con una mediana elevada. **Estos contrastes permiten buscar dónde una eventual omisión tendría mayor interés tributario, si los inmuebles que se encuentren son comparables a los registrados.** El tamaño de la diferencia y el perfil de avalúos deben leerse juntos.

La principal objeción es el sesgo de selección. Lo que falta en un registro puede diferir sistemáticamente de lo que sí entró: viviendas más pequeñas, predios agrícolas, roles matrices, construcciones recientes o tenencias distintas. Trasladar la media, mediana o proporción del stock registrado a los posibles ausentes exige una semejanza que todavía debe probarse.

### Por qué aún no hay una barra en pesos

El campo semestral del extracto no separa todos los componentes necesarios para obtener contribución neta habitacional. Los cuadros comunales oficiales disponibles sí distinguen componentes, pero incluyen otros destinos no agrícolas además del habitacional. Dividir ese total por roles habitacionales fabricaría una media residencial. La [auditoría de fuentes](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) conserva el problema.

El monto que podría girarse, el monto efectivamente girado y el monto pagado son etapas distintas. En Chile, el SII determina avalúos y giros, y [la TGR recauda](https://ayuda.tgr.gob.cl/ayuda/impuestos/impuestos-y-tipos-de-impuestos); además, la distribución por el Fondo Común Municipal impide equiparar impuesto asociado a una comuna con ingreso retenido íntegramente por su municipio. [SII: contribuciones y distribución](https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html).

La literatura ayuda a ordenar esa secuencia. Grote y Wen separan cobertura, valoración y cobro como componentes de la administración del impuesto; su guía propone contrastar cartografía, datos de terreno y registros para identificar discrepancias. Es un fundamento para verificar inmuebles, no un coeficiente que podamos aplicar a Chile. [Guía del FMI, 2024, pp. 16–18](https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf).

## Tercera cucharada: qué revisión resolvería la pregunta

Para que la hipótesis de contribuciones omitidas gane respaldo, la siguiente etapa debe enlazar construcciones y predios, revisar su situación tributaria y reconstruir fechas. El resultado puede ser una nueva incorporación, la actualización de un rol existente o la constatación de que el registro ya era correcto.

| Hipótesis | Evidencia que la distinguiría | Qué la debilitaría o descartaría |
|---|---|---|
| Construcción o predio omitido del catastro | Ubicación identificable, antecedentes de terreno y construcción, búsqueda de roles y expediente de incorporación | El inmueble ya figura correctamente, incluso bajo otro rol o destino |
| Avalúo desactualizado en un rol existente | Superficie o características actuales comparadas con el detalle catastral y las fechas de actualización | El avalúo ya incorpora esas características o la diferencia no corresponde al período |
| Diferencia entre unidades o fechas | Enlace con rol matriz, predio agrícola, copropiedad y cortes temporales comparables | Un cruce individual confirma unidades y fechas equivalentes y la diferencia persiste |
| Error de la fuente o del cruce | Extracto oficial íntegro, claves territoriales conciliadas y contraste independiente | Fuentes independientes reproducen el resultado con las mismas definiciones |

El SII dispone de procedimientos de [inclusión de bienes raíces](https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_1947.htm) y de modificación del avalúo de construcciones. Enrolar y actualizar son respuestas diferentes: una ampliación puede aumentar el avalúo de un rol existente sin crear un rol nuevo.

Hay evidencia experimental de que mejorar la localización de contribuyentes puede cambiar la recaudación: Dzansi y coautores estudian una herramienta geoespacial para entregar giros en Ghana. Su resultado respalda estudiar el mecanismo administrativo; no permite importar una tasa de recuperación para estas comunas. [NBER, documento 29923, revisión 2025](https://www.nber.org/system/files/working_papers/w29923/w29923.pdf).

También hay evidencia que frena una conclusión automática. D'Arcy, Nistotskaya y Olsson, en un panel histórico de países, no encuentran un efecto sobre impuestos a la propiedad en su análisis de mecanismos. Mejorar un catastro no garantiza por sí solo mayor recaudación predial. [Journal of Political Economy, 2024, sección IV](https://www.journals.uchicago.edu/doi/full/10.1086/730551).

La inferencia que interesa conservar es concreta: **donde la discrepancia persiste y los predios observados tienen avalúos altos, conviene exigir una explicación verificable y revisar la eventual necesidad de enrolar o actualizar**. Si las diferencias se resuelven con roles existentes, destinos o fechas, la hipótesis tributaria pierde fuerza. Si se identifican omisiones con obligación exigible, recién entonces habrá base para cuantificar giros faltantes y examinar responsabilidades.

El próximo post incorporará el **Continuo de Construcciones Urbanas (CCU)** para observar expansión y densificación. La huella física puede ayudar a localizar cambios; para hablar de demora del SII habrá que añadir fechas de construcción, avisos y actualización administrativa, y comprobar cuánto depende el CCU de insumos censales.

<details markdown="1">
<summary>Fuentes, cortes y correcciones que afectan la lectura</summary>

El espejo catastral fue descargado el 24 de julio de 2026 y corresponde a 2026S1; no es una descarga directa del SII ni un corte de septiembre. Antártica y Trehuaco carecen de extracto y quedan como faltantes. El control nacional SII por destino informa 6.056.150 predios habitacionales; el extracto reúne 6.054.808. Las planillas MINVU 2026S1 informan 6.057.949, incluidos 1.342 de Trehuaco: no se mezclan silenciosamente esos cortes. [SII por destino](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html), [MINVU parque habitacional](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/).

La revisión corrigió la homologación territorial de Coyhaique, Aysén y Chile Chico. También corrigió el indicador de vivienda irrecuperable: el borrador anterior informaba 73.338; al aplicar primero la exclusión de no respuesta del código oficial, quedan **72.642**, es decir, 696 menos. Esta corrección no cambia la diferencia viviendas–roles ni el descuento por campamentos. La definición de materialidad aceptable sigue el código del manual INE, que no coincide completamente con su descripción en prosa; la decisión y su sensibilidad están documentadas.

La capa CNC no incluye un diccionario para su campo `HOGARESCEN`: interpretarlo como hogares censales se apoya en su nombre y en la documentación MINVU, y deberá revisarse si aparece una definición oficial diferente. En materialidad hay 4.388 viviendas ocupadas con información incompleta; las variantes documentadas modifican su tratamiento, sin presentarse como intervalos de confianza.

El [método reproducible](/catastro_sii_brecha/data/fiscal-gap/method.md), la [auditoría de fuentes](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) y el [archivo de datos](/catastro_sii_brecha/data/fiscal-gap/communes.json) conservan definiciones, faltantes, reglas y erratas. Sólo se publican agregados comunales.

</details>

## Referencias para seguir la inferencia

- Grote, M., & Wen, J.-F. (2024). *How to Design and Implement Property Tax Reforms* (How to Note 2024/006). Fondo Monetario Internacional. [Texto completo](https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf).
- Dzansi, J., Jensen, A., Lagakos, D., & Telli, H. (2022; revisión de febrero de 2025). *Technology and Tax Capacity: Evidence from Local Governments in Ghana* (Working Paper 29923). National Bureau of Economic Research. [DOI](https://doi.org/10.3386/w29923).
- D'Arcy, M., Nistotskaya, M., & Olsson, O. (2024). Cadasters and economic growth: A long-run cross-country panel. *Journal of Political Economy, 132*(11), 3785–3826. [DOI](https://doi.org/10.1086/730551).

[Explorar el diagnóstico](/catastro_sii_brecha/#brecha-contribuciones) · [Descargar CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv) · [Método, fuentes y erratas](/catastro_sii_brecha/data/fiscal-gap/method.md).
