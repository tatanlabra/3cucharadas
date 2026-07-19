# Validación de PMTiles

Estado: **no iniciado como artefacto publicable**.

No hay PMTiles ni upload R2 que validar todavía. Es la consecuencia intencional de
dos gates comprobados: `LEGAL_PUBLICATION_STATUS=PENDING` y `stata01` sin el árbol de
build ni Tippecanoe/PMTiles/GDAL.

Antes de promoción, el pipeline exige por versión:

1. `pmtiles verify` y `pmtiles show` con capa, bounds y zoom esperados;
2. allowlist exacta de atributos prediales (`cod_region`, `cod_comuna`,
   `destino_clase`, `calidad_geometrica`, `version_datos`);
3. cero geometrías inválidas o vacías en la copia pública;
4. conteo de entidades por Caldera y Diego de Almagro conciliado con el extracto H;
5. muestra de tamaños p50/p95/máximo de tesela; objetivo p95 < 500 KB y máximo < 1 MB;
6. petición HTTP `Range` contra R2 con `206`, `Accept-Ranges` y `Content-Range`.

El manifiesto web se mantiene en `PENDING`, con `available: false`, para impedir que
el navegador intente descargar predios o presente una capa inexistente como publicada.
