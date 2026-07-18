# Geometry repair report — piloto Atacama

Fecha: 2026-07-18
Estado: sin reparación aplicada.

La regla implementada no ejecuta `ST_MakeValid`, simplificación ni escritura sobre
los GeoParquet canónicos. Antes de teselar, `build_pmtiles.py` descarta geometrías
nulas del extracto de trabajo y aborta si encuentra geometrías vacías o inválidas.

| Fuente | H totales | H con geometría no nula | Acción |
| --- | ---: | ---: | --- |
| Caldera (`caldera_3202.parquet`) | 8.477 | 8.475 | Validar en entorno de build; no reparar. |
| Diego de Almagro (`diego_de_almagro_3102.parquet`) | 2.878 | 2.422 | Validar en entorno de build; no reparar. |

Los conteos de validez topológica, multipolígonos y área cero están pendientes de
`stata01`, que todavía no tiene GeoPandas/GDAL/Tippecanoe ni la fuente sincronizada.
No se promueve un PMTiles hasta registrar esos conteos como cero para la salida.
