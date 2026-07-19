---
layout: single
# Retirado de publicación: se reescribe antes de volver a salir.
published: false
title: "Un catastro no es un censo: medir la brecha residencial con Python y OSM"
subtitle: "Predios H, Parquet, celdas neón y una regla simple para no inventar habitantes"
date: 2026-07-17 15:00:00 -0400
categories: [datos, python, openstreetmap]
tags: [python, openstreetmap, osm, maplibre, parquet, catastro-sii, censo-2024, datos-abiertos, geodata]
description: "Cómo construí un visor Python + OpenStreetMap que compara la cobertura residencial equivalente del Catastro SII con el Censo 2024, sin convertir registros en personas imaginarias."
excerpt: "Casi seis millones de predios H no son casi seis millones de hogares. La diferencia importa y ahora tiene visor."
author: clabra
lang: es
ref: catastro-sii-brecha-python-osm
permalink: /datos/python/openstreetmap/catastro-sii-brecha/
distribution:
  social: true
  republish: []
toc: true
toc_sticky: true
comments: true
author_profile: true
---

El Catastro SII es una fuente fantástica para mirar territorio. También es una fuente peligrosa si uno hace la conversión mental demasiado rápido: “hay N predios, entonces viven N hogares, entonces viven N personas”. No.
{: .text-justify}

Publiqué el visor [Brecha residencial del Catastro SII](/catastro_sii_brecha/). Parte con los predios de destino habitacional (`H`) y pregunta algo más modesto: ¿qué porcentaje de la población censada 2024 quedaría cubierto si esos registros siguieran la relación comunal de personas por vivienda ocupada?
{: .text-justify}

No responde dónde vive una persona. No diagnostica informalidad, vacancia, mala clasificación ni subregistro. Es una medida de cobertura equivalente. Ese límite es el producto.
{: .text-justify}

## La fórmula cabe en una línea

Para cada comuna calculé:

```python
poblacion_equivalente = predios_H * (poblacion_censo_2024 / viviendas_con_moradores_presentes)
cobertura = poblacion_equivalente / poblacion_censo_2024
```

Es deliberadamente auditable. También puede descomponerse en personas por hogar y hogares por vivienda, pero el resultado principal termina siendo personas por vivienda con moradores presentes. El visor muestra esa cobertura frente al Censo 2024 y, como contexto histórico separado, frente a la proyección INE 2024 cuya base es el Censo 2017.
{: .text-justify}

CASEN 2024 aparece sólo como sensibilidad. La base permite construir una aritmética comunal con factores, pero MDSF no recomienda usarla como estimación comunal representativa. Por eso no ordena comunas, no pinta el mapa y no escribe el titular.
{: .text-justify}

## Python para el dato, OSM para no dejarlo en una tabla

El pipeline es Python-first: lee el corte canónico del Catastro SII por columnas, normaliza Censo, INE y CASEN a Parquet con compresión Zstandard y genera una tabla comunal reproducible. Nada de cargar seis millones de filas al navegador para descubrir que una pestaña no es un cluster HPC.
{: .text-justify}

Para el mapa transformé sólo las coordenadas válidas de predios H en celdas Web Mercator agregadas. El resultado son puntos de concentración neón sobre un fondo oscuro de OpenStreetMap: útiles para mirar patrón territorial, pero sin pretender que cada brillo es una casa concreta. La carga inicial trae los 346 indicadores comunales; la capa de celdas se pide recién al elegir comuna.
{: .text-justify}

Hubo además una pequeña lección de geografía de datos. El corte SII divide Santiago en tres extractos, mientras que Censo lo entrega como una comuna; Trehuaco y Antártica no traen extracto SII en este corte. El build no los “arregla”: documenta el cruce, agrega sólo lo justificable y muestra la ausencia cuando corresponde.
{: .text-justify}

## Qué se puede hacer con esto

El visor permite elegir región y comuna, revisar población Censo, predios H, cobertura de coordenadas, superficie, avalúo y percentiles. La descarga incluye las métricas comunales en Parquet para usarla desde Python; el detalle de fuentes, supuestos y excepciones está en [la metodología](/catastro_sii_brecha/metodologia.html).
{: .text-justify}

La interpretación responsable empieza por una pregunta menos sexy que “¿cuánta gente vive ahí?”: ¿qué parte de la población logra representar este registro si le damos reglas explícitas? Desde ahí se puede investigar lo demás. Antes, es sólo un mapa con demasiada seguridad en sí mismo.
{: .text-justify}

Fuentes: [Censo 2024 INE](https://censo2024.ine.gob.cl/estadisticas/), [códigos de destino SII](https://www.sii.cl/servicios_online/1048-Anexo_6-2573.html), [nota de uso CASEN 2024](https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf) y [política de teselas OSM](https://operations.osmfoundation.org/policies/tiles/).
{: .small}
