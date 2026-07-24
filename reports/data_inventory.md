# Inventario de insumos cartográficos

Fecha de diagnóstico: 2026-07-18.

## Fuente maestra inmutable

La fuente canónica local está en
`activos/catastros_sii/storage/source_safe/tienda/v46_20260627/parquet/` y contiene
346 GeoParquet. No se escribe, simplifica ni repara esa fuente.

| Piloto | Archivo fuente | Filas | Predios `H` | `H` con geometría no nula | Tamaño |
| --- | --- | ---: | ---: | ---: | ---: |
| Caldera | `caldera_3202.parquet` | 11.287 | 8.477 | 8.475 | 6,44 MB |
| Diego de Almagro | `diego_de_almagro_3102.parquet` | 5.120 | 2.878 | 2.422 | 1,21 MB |

Las geometrías declaradas son WKB, EPSG:4326, de tipo `Polygon`/`MultiPolygon`.
Sus bounding boxes GeoParquet son respectivamente
`[-70.978809, -27.833521, -70.244801, -26.644673]` y
`[-70.210973, -26.921486, -68.366938, -25.285839]`.

## Datos públicos ya presentes

| Producto | Tamaño | Uso |
| --- | ---: | --- |
| `data/comunas.json` | 564 KB | Fichas y catálogo de 346 comunas. |
| `data/metricas_comunales.parquet` | 100 KB | Descarga de métricas agregadas. |
| `data/comunas/*.json` | 89.796 bytes en total | Celdas agregadas por comuna. |
| `data/capas_prediales/manifest.json` | 1 archivo | Declara que ningún polígono está disponible hoy. |

## Límite comunal a incorporar

La fuente candidata es la **División Política Administrativa 2023** publicada por
la IDE Chile/SUBDERE: entrega capas separadas de comunas, provincias y regiones, en
SIRGAS Chile y a escala de representación 1:50.000. Antes de construir se debe
descargar de esa fuente, guardar hash y metadatos, y comprobar el cruce de códigos.
La ficha advierte que no incluye el polígono de Antártica; ese caso se declara en el
manifest hasta contar con una geometría autorizada, en vez de inventarlo o usar OSM
como reemplazo.

## Campos y clasificación de publicación

Los dos GeoParquet piloto contienen identificadores prediales, direcciones y atributos
operativos. Son **prohibidos** en cualquier salida web:

- `rol`, componentes `predioPublicado_*`, `dc_bc*`, `dc_padre_*`, `_poly_idx` y
  cualquier identificador fuente;
- `direccion_sii`, `dc_direccion`, `ubicacion` y cualquier dirección;
- coordenadas auxiliares, métodos de emparejamiento, errores y atributos de proceso.

**Actualización 2026-07-23.** Los **valores de avalúo y superficie dejaron de estar
prohibidos**. El visor publica avalúo fiscal por predio, avalúo por m² agregado por unidad
vecinal (`avm2`) y superficie, además de las clases derivadas. El límite que se mantiene es
la **identificación**, no el valor: puede mostrarse cuánto vale un predio, no quién es su
titular ni su dirección exacta.

El extracto público admite geometría, clases no identificables y los valores señalados:
`destino_clase`, `superficie_clase`, `avaluo_m2_clase`, `brecha_clase`,
`calidad_geometrica`, `cod_region`, `cod_comuna`, `version_datos`, `id_publico`
aleatorio/salteado y los valores de avalúo/superficie descritos arriba. La construcción
falla si detecta un identificador fuente o una dirección.

## Validación pendiente de entorno de build

El diagnóstico no encontró Tippecanoe, PMTiles CLI ni GDAL en `stata01`; por ello no
es honesto afirmar todavía conteos de geometrías inválidas, distribución de tamaños
de teselas o PMTiles válidos. El pipeline nuevo ejecuta esas pruebas antes de habilitar
un manifest publicable y conserva el reporte por versión.
