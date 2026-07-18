# Operación de tiles Catastro SII

1. Obtener la DPA 2023 de fuente oficial y registrar fecha, licencia y SHA-256.
2. Elegir rutas existentes bajo `MAX_VOLUME_USAGE_PCT` para `BUILD_WORK_ROOT` y
   `TILES_OUTPUT_ROOT`. La primera debe ser disco local ejecutable: Tippecanoe
   requiere locks SQLite y no puede construir sobre CIFS/NFS. El resultado se
   copia al segundo directorio sólo después de sus validaciones no publicadas.
   No usar el árbol canónico ni un NFS ya saturado para artefactos temporales.
   El máximo normal es 90%; un override debe residir sólo en la configuración
   no versionada, dejar registrado el espacio libre y tener rollback probado.
3. Instalar sólo las herramientas faltantes en el entorno mantenido de `stata01`:

   ```bash
   PYTHON_BIN=/opt/conda/envs/python_base/bin/python \
   scripts/catastro_sii/prepare_stata01_pmtiles_env.sh
   ```

   El script no crea ni clona entornos Conda: instala únicamente Tippecanoe,
   PMTiles y rclone que no estén ya presentes en `python_base`, desde conda-forge.
4. Sincronizar sólo el código versionado del sitio, la DPA autorizada y las dos fuentes
   piloto a `stata01`. No copiar ni exponer credenciales R2 en ese paso.
5. Ejecutar `run_atacama_pilot_stata01.sh` con `LEGAL_PUBLICATION_STATUS=PENDING`
   para un artefacto de validación aún no desplegado. El piloto Atacama deriva sólo
   `predio` y `dc_avaluo_fiscal` como `avaluo_fiscal_clp`; no incluye rol, dirección,
   propietario, superficie ni `valorTotal`. Revisar `pmtiles-show`, conteos,
   geometrías, atributos y presupuesto antes de cualquier promoción.
   Declarar `COMUNAS_SOURCE_CODE_FIELD=CUT_COM` y
   `COMUNAS_EXCLUDED_CODES=12202`: la DPA 2023 tiene 345 geometrías y la exclusión
   antártica debe ser explícita, nunca implícita.
6. Para la revisión local, copiar sólo los PMTiles, estilo PBF y los índices auditados
   desde `stata01`; nunca el GeoParquet ni los intermedios:

   ```bash
   scripts/catastro_sii/sync_local_preview_from_stata01.sh 20260718T212932Z
   ```

   El resultado queda ignorado por Git bajo `assets/data/catastro_sii/local/` y se
   abre en `http://127.0.0.1:4001/catastro_sii_brecha/`. Para fijar una corrida
   específica, usa `?catastroPreview=local&run=20260718T212932Z`.
   Su manifest sólo funciona en localhost y no modifica el manifest versionado.
7. Preparar la base Protomaps/OSM desde una fuente con licencia compatible. El script
   llama al extractor oficial `pmtiles` en el contenedor Protomaps fijado por digest,
   con artefactos finales bajo el directorio de salida en `nas05` y caché/runroot
   efímeros sólo bajo `/tmp` (el almacenamiento interno de Podman no bloquea sobre
   CIFS/NFS). Divide Chile continental e islas para no extraer el Pacífico
   completo, autoalberga la fuente PBF usada por las etiquetas y no modifica la fuente:

   ```bash
   PROTOMAPS_SOURCE=https://build.protomaps.com/AAAAMMDD.pmtiles \
   scripts/catastro_sii/prepare_basemap.sh /ruta/a/salida 20260718
   ```

8. Tras los PASS de datos, cartografía y configuración de despliegue,
   actualizar el manifest público versionado y ejecutar `upload_r2.sh` con una
   lista explícita de activos. La capa comunal y el basemap pueden comprobarse con
   `PENDING`; un archivo `predios_region_*.pmtiles` exige
   `AUTHORIZED_VECTOR`. `promote_manifest.py` copia además el pequeño índice de
   bounding boxes de la capa comunal a `assets/data/catastro_sii/territories.json`.
9. Aplicar `r2-cors.json` al bucket/dominio. `upload_r2.sh` exige para cada PMTiles
   una petición **GET** `Range` desde `https://3cucharadas.cl` con `206`,
   `Accept-Ranges`, `Content-Range` y los encabezados CORS expuestos antes de
   permitir promover el manifest.

`build_pmtiles.py` nunca escribe sobre la fuente GeoParquet. Rechaza geometrías
inválidas; no aplica `MakeValid` ni publica los atributos fuente.
