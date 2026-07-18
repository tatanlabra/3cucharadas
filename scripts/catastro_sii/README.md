# Operación de tiles Catastro SII

1. Obtener la DPA 2023 de fuente oficial y registrar fecha, licencia y SHA-256.
2. Elegir un `TILES_WORK_ROOT` existente en un filesystem con uso menor a 90%.
   No usar el árbol canónico ni un NFS ya saturado para artefactos temporales.
3. Preparar un entorno aislado desde el Conda geoespacial existente:

   ```bash
   TILES_WORK_ROOT=/ruta/en/volumen-verificado \
   scripts/catastro_sii/prepare_stata01_pmtiles_env.sh
   ```

   El script clona `py_3_12_geopandas_jc`, instala Tippecanoe y rclone desde
   conda-forge y usa `pip` sólo si no existe un paquete Conda para la CLI PMTiles.
4. Sincronizar sólo el código versionado del sitio, la DPA autorizada y las dos fuentes
   piloto a `stata01`. No copiar ni exponer credenciales R2 en ese paso.
5. Ejecutar `run_atacama_pilot_stata01.sh` con `LEGAL_PUBLICATION_STATUS=PENDING`
   para un artefacto privado de validación. Revisar `pmtiles show`, conteos,
   geometrías, atributos y presupuesto antes de cualquier promoción.
   Declarar `COMUNAS_SOURCE_CODE_FIELD=CUT_COM` y
   `COMUNAS_EXCLUDED_CODES=12202`: la DPA 2023 tiene 345 geometrías y la exclusión
   antártica debe ser explícita, nunca implícita.
6. Cambiar el gate sólo con aprobación documentada. Reejecutar con
   `AUTHORIZED_VECTOR`, actualizar el manifest público versionado y recién entonces
   ejecutar `upload_r2.sh`. `promote_manifest.py` copia además el pequeño índice de
   bounding boxes de la capa comunal a `assets/data/catastro_sii/territories.json`.
7. Aplicar `r2-cors.json` al bucket/dominio y confirmar que una petición `Range`
   desde `https://3cucharadas.cl` recibe `206`, `Accept-Ranges` y `Content-Range`.

`build_pmtiles.py` nunca escribe sobre la fuente GeoParquet. Rechaza geometrías
inválidas; no aplica `MakeValid` ni publica los atributos fuente.
