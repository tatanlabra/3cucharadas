---
layout: single
classes: [thesis-extension-post, thesis-coordinate-audit-annex]
title: "Auditoría nacional de coordenadas escolares MINEDUC–OSM"
subtitle: "Método, resultados agregados y límites del control usado en el Post II."
date: 2026-10-11 19:10:00 -0300
last_modified_at: 2026-10-17 17:15:00 -0300
categories: [datos, educacion, metodologia]
tags: [educacion, mineduc, openstreetmap, coordenadas, calidad-de-datos]
description: "Anexo técnico reproducible de la auditoría agregada de coordenadas de establecimientos educacionales chilenos con señales de OpenStreetMap."
excerpt: "Una auditoría de calidad geográfica distingue coordenadas oficiales, candidatos OSM y casos no resueltos sin corregir automáticamente la fuente institucional."
author: clabra
lang: es
ref: auditoria-coordenadas-rbd
permalink: /datos/educacion/auditoria-coordenadas-rbd/
header:
  teaser: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/og-1200x630.webp
  og_image_alt: "Puntos y contornos escolares superpuestos como metáfora de una auditoría de coordenadas."
distribution:
  social: false
---

Este anexo documenta el control geográfico usado en el Post II. La comparación **no identifica el efecto causal** de abrir o cerrar escuelas y tampoco convierte OpenStreetMap (OSM) en una ubicación verdadera automática. Su propósito es más acotado: detectar señales que merecen revisión antes de medir distancias.

[Read this technical annex in English](/en/datos/educacion/auditoria-coordenadas-rbd/).

## Universo y fuentes

- El universo principal contiene **12.038 establecimientos funcionando** en el Directorio Oficial MINEDUC 2025, de todas las dependencias y regiones.
- Otros **78 establecimientos autorizados sin matrícula** se informan por separado. Ambos estados forman las **12.116 filas oficiales auditadas**; no se mezclan para describir el universo principal de establecimientos funcionando.
- El contraste usa **18.588 objetos educacionales candidatos** del snapshot OSM fechado el 27 de agosto de 2026.
- La división comunal proviene de la DPA 2023: 345 geometrías válidas; la comuna Antártica (CUT 12202) queda como no evaluable porque el archivo oficial no contiene su polígono.

La unidad oficial es el establecimiento por año de directorio. OSM aporta objetos cartográficos: un punto puede representar un acceso, un edificio, un campus o el centroide interno de un polígono. Por eso, cercanía no equivale a identidad.

## Reglas de matching

| Nivel | Regla | Resultado permitido |
|---|---|---|
| A | Referencia OSM explícita al mismo RBD | Candidato de mayor confianza |
| B | Nombre normalizado exacto, misma comuna y candidato único | Candidato fuerte |
| C | Similitud nominal de al menos 0,90, misma comuna y señal adicional | Revisión obligatoria |
| D | Solo cercanía espacial | Diagnóstico; nunca match por sí solo |

Los empates conservan todas sus alternativas. El matching no usa matrícula, SIMCE, admisión ni otro resultado educativo y nunca imputa o sobrescribe una coordenada MINEDUC.

## Resultados agregados

| Indicador | Conteo |
|---|---:|
| Filas oficiales con al menos un candidato A–C | 6.601 |
| Filas oficiales sin candidato OSM | 5.515 |
| Matches ambiguos conservados | 237 |
| Coordenadas oficiales válidas | 11.864 |
| Coordenadas oficiales faltantes | 250 |
| Latitud y longitud aparentemente invertidas | 2 |
| Señales de comuna incompatible | 48 |
| Casos dentro del buffer comunal de 250 m | 31 |
| Candidatos de campus compartido | 207 |
| Saltos temporales candidatos | 750 |
| Filas de muestra adjudicadas por reglas | 126 |
| Errores oficiales confirmados | **0** |

Entre los establecimientos con candidato y distancia calculable, los conteos acumulados son 5.230 hasta 100 m; 5.745 hasta 250 m; 6.013 hasta 500 m; 6.184 hasta 1 km; 6.324 hasta 2 km; y 6.465 hasta 5 km. Estos umbrales priorizan revisión: no son una escala de verdad.

Dos enlaces OSM declaran una posible fuente MINEDUC. Se conservan como riesgo de dependencia entre fuentes y no cuentan como corroboración independiente.

## Adjudicación e interpretación

Una muestra estratificada con semilla `20261011`, más filas obligatorias, reunió 126 filas con referencias explícitas compatibles o divergentes, coincidencias nominales y candidatos de duplicado. Luego se adjudicó por reglas. El repositorio **no documenta una revisión humana independiente de las 126 filas**, por lo que no corresponde llamarlas «revisadas manualmente». El resultado automatizado fue deliberadamente conservador: **ninguna señal se elevó a error oficial confirmado**.

- Una coordenada inválida es un problema observable del snapshot oficial, pero OSM por sí solo no acredita el punto correcto.
- Un punto fuera de la comuna puede reflejar borde, acceso, traslado o error; el buffer de 250 m evita convertir precisión cartográfica en una conclusión administrativa.
- Dos RBD separados por 10 m o menos pueden compartir campus.
- Un salto de al menos 1 km entre años puede corresponder a traslado, fusión, corrección o error.
- La ausencia en OSM significa falta de contraste, no validación de MINEDUC.

## Superficie pública, licencia y reproducibilidad

La auditoría nacional publica únicamente agregados por región, señal, confianza y banda de distancia. El cruce nacional por establecimiento no se publica: el portal MINEDUC no mostró una licencia adjunta a los archivos durante esta revisión y esa ausencia no se interpreta como permiso de redistribución.

- [Descargar el resumen agregado en JSON](/assets/data/thesis-extension-post2/coordinate-audit-summary.json).
- Fuente oficial: [Directorio de establecimientos educacionales MINEDUC](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/).
- Cartografía: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), bajo [ODbL](https://opendatacommons.org/licenses/odbl/1-0/).

El JSON nacional fija hashes de las fuentes agregadas y el snapshot OSM. No contiene nombres, RBD individuales, direcciones, coordenadas ni identificadores personales.

## Auditoría específica del caso El Salvador

La auditoría nacional 2025 no bastaba para validar el caso mostrado en el visor: el RBD 391 estaba cerrado y quedaba fuera de ese universo. Por eso se ejecutó un control específico para los dos establecimientos de El Salvador, conservando por separado las observaciones oficiales y los candidatos OSM.

| Resultado del contraste | Casos |
|---|---:|
| Puntos oficiales conservados | 2 |
| Candidatos OSM retenidos para contraste | 2 |
| Homónimos rechazados | 1 |
| Errores oficiales confirmados | **0** |
{: .table--compact .table--scroll}

La Escuela N° 14 (RBD 391) queda como **discrepancia no resuelta**: los directorios MINEDUC 2008–2011 registran Diego Portales 500 y el objeto OSM homónimo es compatible con esa sede, pero fue creado en 2022 y no declara RBD. El candidato está a **825,551 m** del punto oficial 2015. Medida desde ese candidato, la Escuela N° 1 queda a **1,272025 km**; con las dos coordenadas oficiales, a **0,448903 km**. El visor conserva ambas observaciones y no afirma que OSM haya corregido a MINEDUC.

- [Descargar el GeoJSON del contraste de El Salvador](/assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.geojson).
- [Descargar su manifiesto reproducible](/assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.manifest.json).

Este archivo de alcance acotado contiene RBD, nombres y coordenadas que ya se muestran en el Post II, además de identificadores y enlaces OSM. No contiene datos de estudiantes ni identificadores personales.

## Qué permite concluir

La auditoría permite afirmar que la medición territorial tiene controles reproducibles y que existen señales que requieren revisión. No permite afirmar que OSM corrigió a MINEDUC, que una discrepancia sea un error institucional, ni que la cercanía entre establecimientos pruebe sustitución, calidad o causalidad.
