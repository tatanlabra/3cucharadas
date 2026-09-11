---
layout: single
title: "Avalúos II: ¿cuánto podría representar la brecha residencial en contribuciones?"
subtitle: "Qué parte cambia al descontar hogares censados en campamentos y qué evidencia falta para ponerle pesos"
date: 2026-09-09 20:00:00 -0400
categories: [datos, territorio]
tags: [catastro-sii, censo-2024, contribuciones, datos-abiertos, desigualdad]
author: clabra
lang: es
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: false
editorial_status: pendiente-conciliacion-fiscal
description: "Diagnóstico comunal Censo 2024–SII 2026S1 con sensibilidad por campamentos. La diferencia física no identifica impuestos omitidos."
excerpt: "Los campamentos explican una parte desigual de la brecha residencial; aun después del ajuste quedan diferencias que requieren investigación."
header:
  teaser: /assets/images/avaluos-ii/gap-top15-es.png
math: true
toc: true
toc_sticky: true
comments: true
---

**Borrador de investigación: el ranking monetario sigue pendiente de conciliación.** El gráfico compara la brecha original con una sensibilidad que descuenta hogares censados en campamentos. Ninguna barra muestra recaudación perdida ni identifica negligencia del SII.
{: .notice--warning}

En el [primer post de avalúos](/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/) cambiábamos el denominador para examinar cómo cambia la lectura territorial. Aquí la pregunta es más incómoda: cuando una comuna tiene más viviendas censadas que roles habitacionales, ¿qué parte de esa diferencia podría tener consecuencias tributarias?

Hay una inquietud pública atendible: una construcción que reúne las condiciones para tributar debería quedar correctamente incorporada al catastro. Pero una resta entre dos totales no identifica esa construcción, su obligación ni un peso sin cobrar. Para problematizar la situación con evidencia, hay que conservar esa distinción hasta el final.

## Primera cucharada: una diferencia que merece explicación

Comparo todas las viviendas particulares del **Censo 2024**, ocupadas y desocupadas, con los roles de destino habitacional **H del primer semestre de 2026**. La fuente catastral es un espejo descargado el 24 de julio de 2026, contrastado con estadísticas oficiales: no una descarga directa del SII ni un catastro de septiembre. La [tabla completa y sus fuentes](/catastro_sii_brecha/data/fiscal-gap/communes.json) conservan período, extracción y faltantes.

Una vivienda es una unidad del censo. Un rol es una identificación catastral de un bien raíz. Un hogar es un grupo de personas. Un edificio puede contener muchas viviendas; un predio rural de destino agrícola puede contener viviendas que no aparecen al filtrar exclusivamente destino H. Las subdivisiones y los roles matrices agregan otras diferencias. Por eso **viviendas menos roles H** es un diagnóstico de compatibilidad entre registros, no un conteo de viviendas sin rol.

![Quince comunas con mayor brecha residual; cada comuna compara la diferencia original con el resultado de descontar hogares censados en campamentos.](/assets/images/avaluos-ii/gap-top15-es.svg)

{% include avaluos-ii-top-es.html %}

Orden descendente del residuo positivo después de la sensibilidad, desempate por CUT. Las barras comienzan en cero. Antártica y Trehuaco carecen de extracto en este conjunto y quedan fuera del ranking; permanecen como faltantes en la tabla completa. Una brecha negativa también se conserva: no prueba que todos los inmuebles estén correctamente registrados.

## Campamentos: cuánto cambia y cuánto no

El [MINVU cruzó geográficamente su catastro con el Censo 2024](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/vivienda-y-deficit/). En la foto de 2024 identificó 1.373 campamentos con viviendas ocupadas, 81.993 viviendas y 77.399 hogares. La capa CNC 2026 que acompaña este análisis contiene 1.345 polígonos vigentes y un campo `HOGARESCEN`: suma 71.760 hogares en los polígonos con dato; 222 polígonos permanecen como `S/I` o vacíos.

La sensibilidad resta esos hogares observados a la brecha comunal bajo una hipótesis fuerte: **un hogar censado en campamento explica una vivienda que no requiere un rol H separado**. No es un enlace vivienda–predio–rol ni una corrección observada. En las comunas con polígonos sin conteo, descuenta sólo lo conocido y marca el resultado como parcial.

| Comuna | Brecha original | Hogares Censo en campamentos observados | Residuo de sensibilidad | Parte absorbida |
|---|---:|---:|---:|---:|
| Alto Hospicio | 15.368 | 9.136 | 6.232 | 59,4% |
| Antofagasta | 21.755 | 7.537 | 14.218 | 34,6% |
| Viña del Mar | 24.030 | 8.014 | 16.016 | 33,3% |
| Valparaíso | 32.533 | 2.572 | 29.961 | 7,9% |
| Puerto Montt | 29.036 | 632 | 28.404 | 2,2% |

A escala nacional, la suma de brechas positivas baja de 1.588.449 a 1.516.689: una reducción de 71.760 unidades, o 4,52%. El contraste es informativo precisamente porque no produce el mismo relato en todas partes: los campamentos alteran mucho algunas posiciones, pero explican poco de varias brechas líderes.

El Censo también permite identificar viviendas irrecuperables por tipo o materialidad. Aplicando el algoritmo oficial a viviendas particulares ocupadas con moradores presentes aparecen 73.338. No las resto: materialidad precaria no prueba tenencia irregular ni ausencia de rol, y parte de esas viviendas ya puede estar dentro de los polígonos de campamentos. Sumarlas duplicaría casos sin conocer su superposición.

La base innominada histórica de campamentos tampoco entra al descuento. Contiene observaciones de personas y hogares asociadas a levantamientos 2011–2021, incluidos hogares que pueden haber salido del registro vigente. Usarla como stock 2026 mezclaría períodos y unidades; sus filas individuales no se publican.

El [INE define el universo censal](https://censo2024.ine.gob.cl/resultados/) y el [SII clasifica los bienes raíces por destino](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html). Entre ambas fechas pueden existir nuevas construcciones, cambios de destino y actualizaciones administrativas. Este contraste no mide crecimiento entre 2024 y 2026: sus unidades tampoco son iguales.

La revisión de las [planillas oficiales MINVU 2026S1](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/) aporta un control adicional: Trehuaco tiene 1.342 roles H y Antártica, cero. Sin embargo, su total nacional es 6.057.949, superior en 1.799 al cuadro SII. En las comunas cubiertas por el espejo, esos 1.799 adicionales se distribuyen en 208 comunas. La [conciliación completa](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) conserva ambas fuentes; no reemplazamos silenciosamente el corte del gráfico. Una revisión posterior es una hipótesis, no una fecha de alta ni prueba de omisión tributaria.

## Segunda cucharada: cómo pasar a pesos sin inventar recaudación

El escenario propuesto es:

$$
B_c(q)=\max(V_{c,2024}-H_{c,2026S1},0)\;q\;\overline{T}_{c,anual\ equivalente}
$$

La media —o promedio, que es lo mismo— se calculará sobre **todos los roles H, incluidos los ceros**, usando contribución neta semestral verificable y duplicándola para expresar un equivalente anual a condiciones del mismo semestre. No será un monto anual efectivamente girado o pagado.

q tomará 0, 0,25, 0,5 y 1. Permite preguntar qué representaría una fracción hipotética de la diferencia si se le asignara la contribución media del stock observado. **q = 1 no es una probabilidad de omisión estimada ni un límite superior demostrado.** Las viviendas realmente omitidas podrían tener una distribución tributaria diferente. Un q común positivo cambia el tamaño de las barras, no su orden; supuestos diferentes por comuna sí pueden cambiarlo.

La mediana de todos los roles puede ser cero si los ceros predominan. Por eso acompañará a la media, la proporción positiva y la media y mediana entre casos positivos. Multiplicar una media que ya incluye ceros nuevamente por la proporción positiva descontaría dos veces esos ceros. Usar proporción positiva por mediana positiva sería otro escenario, de caso típico, no el valor esperado.

El obstáculo actual es verificable: la [definición histórica del producto catastral](https://www.sii.cl/documentos/resoluciones/2010/2010-5.pdf) incorpora componentes como aseo y sobretasas en el campo semestral. El extracto disponible no los separa. El control nacional tampoco coincide exactamente. La [auditoría y el método](/catastro_sii_brecha/data/fiscal-gap/method.md) muestran la discrepancia y las fuentes consultadas.

Los [CSV comunales vigentes del SII](https://www.sii.cl/sobre_el_sii/estadisticas/estadisticas_bienes_raices_por_comuna.html) sí ofrecen componentes para 2026S1. Pero su contribución neta reúne todos los destinos no agrícolas, incluidos comercio y oficinas. Dividir ese monto por los roles H no produciría una media habitacional.

No basta cambiar el nombre de la columna, aplicar una tasa al avalúo promedio o escalar los montos para que coincidan. La exención, la progresión y los beneficios impiden esas sustituciones. Necesitamos suma neta y total H por comuna del mismo semestre; para las medianas, una distribución o estadísticos oficiales. Hasta entonces, **no hay un top de comunas por pesos publicable**.

## Tercera cucharada: qué evidencia permitiría hablar de responsabilidad

| Explicación provisional | Qué la distinguiría de las alternativas |
|---|---|
| Rezago del catastro | Un inmueble identificable, fecha de construcción, obligación exigible y fecha posterior de incorporación o actualización |
| Viviendas incluidas en otra unidad o destino | Enlace documental y espacial con rol matriz, agrícola u otra configuración existente |
| Incompatibilidad de fechas o clasificación | Reconstrucción de ambos universos en fechas comparables y revisión de las reglas de cada registro |
| Error del extracto o de la homologación | Recuperar la fuente oficial y corregir claves, faltantes o duplicados |
| Error censal o cartográfico | Evidencia independiente que contradiga conteo, localización o clasificación censal |

Estas hipótesis tienen condiciones de descarte. La explicación de rezago pierde fuerza si el rol ya existía o si no había una obligación exigible. La explicación de error del espejo se debilita si un extracto íntegro concilia con el SII. La diferencia de unidades se debilita cuando un enlace individual valida una correspondencia uno a uno. Ninguna de esas verificaciones está contenida en la resta comunal.

«Campamento» tampoco significa «predio que el SII jamás tendrá». La [Ley 17.235](https://www.bcn.cl/leychile/navegar?i=128563) aplica el impuesto a bienes raíces y el rol identifica un predio; una ocupación puede estar dentro de un rol matriz. Además, el [artículo 16 de la Ley 20.234](https://www.bcn.cl/leychile/Navegar/imprimir?idNorma=268116&idParte=0) ordena asignar rol y avalúo separado a cada sitio de ciertos loteos irregulares una vez regularizados, recibidas las obras y otorgadas las escrituras. La informalidad actual no permite deducir ausencia catastral permanente ni obligación tributaria actual.

La revisión encontró un ejemplo concreto de error de homologación: el espejo intercambiaba nombres asociados a los códigos de Coyhaique, Aysén y Chile Chico. Se corrigieron el cruce y sus indicadores; la [errata conserva los valores anteriores y corregidos](/catastro_sii_brecha/data/fiscal-gap/method.md). Corregir ese error cambia la lectura territorial sin descubrir una sola deuda tributaria.

También importa quién hace qué: el SII determina avalúos y giros; la TGR recauda. Girar no equivale a cobrar. El [Fondo Común Municipal participa de la distribución del impuesto territorial](https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html): el escenario bruto asociado a una comuna no sería automáticamente dinero retenido por su municipio.

El siguiente post estudiará el **Continuo de Construcciones Urbanas (CCU)**: dónde crece físicamente la ciudad y si ese crecimiento tiene un patrón compatible con las discrepancias. Primero habrá que distinguir expansión de densificación y revisar cuánto depende el CCU de insumos censales. Una ampliación puede actualizar el avalúo de un rol existente sin crear otro. Sin fechas administrativas no mediremos demora; sin obligación tributaria no mediremos recursos perdidos.

[Explorar el diagnóstico en el mismo visor](/catastro_sii_brecha/#brecha-contribuciones) · [Descargar CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv) · [Método, fuentes y errata](/catastro_sii_brecha/data/fiscal-gap/method.md).
