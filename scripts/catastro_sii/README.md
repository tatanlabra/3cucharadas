# Operación de tiles Catastro SII

1. Obtener la DPA 2023 de fuente oficial y registrar fecha, licencia y SHA-256.
2. Elegir una ruta existente con uso menor a 90% para `TILES_OUTPUT_ROOT`.
   No usar el árbol canónico ni un NFS ya saturado para artefactos temporales.
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
   para un artefacto privado de validación. Revisar `pmtiles-show`, conteos,
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
