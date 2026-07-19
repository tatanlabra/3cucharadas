# Runbook de despliegue R2 — Catastro SII

Este runbook publica una capa comunal nacional de **345 comunas** y el piloto
predial de Atacama. No generaliza los predios a otras regiones, no sube fuentes
GeoParquet/FlatGeobuf y no modifica geometrías.

## Alcance de la corrida aprobada

| Activo | Corrida | Rol |
| --- | --- | --- |
| `chile_comunas_brechas_20260718T212932Z.pmtiles` | `20260718T212932Z` | capa nacional agregada: 345 comunas |
| `basemap_chile_20260718T212932Z.pmtiles` | `20260718T212932Z` | base Protomaps/OSM autoalojada |
| `predios_region_03_20260718T212932Z.pmtiles` | `20260718T212932Z` | piloto Caldera y Diego de Almagro |

Los cinco objetos públicos de la corrida ocupan aproximadamente 654 MB. El
directorio `assets/data/catastro_sii/local/` está ignorado por Git: se usa como
origen de publicación, pero nunca se incorpora al sitio ni a un commit.

## 1. Provisión manual en Cloudflare

1. Crear el bucket R2 `3cucharadas-tiles` en clase **Standard**.
2. Adjuntar el dominio personalizado `tiles.3cucharadas.cl` y habilitar lectura
   pública mediante ese dominio.
3. Aplicar `scripts/catastro_sii/r2-cors.json` como política CORS del bucket.
4. Crear un token R2 `Object Read & Write`, limitado exclusivamente al bucket.
5. Guardar el Access Key ID, Secret Access Key y endpoint S3 en el gestor local
   de secretos. El secreto se muestra una sola vez y no se copia al repositorio,
   a `stata01` ni a CI.

Cloudflare recomienda un dominio personalizado para producción; `r2.dev` queda
para pruebas. La política CORS debe exponer `Accept-Ranges` y `Content-Range`
para que PMTiles funcione desde `3cucharadas.cl`.

## 2. Configuración local de rclone

Configurar en la laptop, no en `stata01`:

```bash
rclone config
```

Crear el remoto `r2-3cucharadas` como S3/Cloudflare R2 usando el endpoint del
paso anterior. La configuración reside fuera del repositorio, normalmente en
`~/.config/rclone/rclone.conf`. Verificar sin mostrar configuración ni secretos:

```bash
rclone lsd r2-3cucharadas:
```

## 3. Variables locales de despliegue

En una sesión local, cargar los valores no versionados:

```bash
export R2_REMOTE='r2-3cucharadas'
export R2_BUCKET='3cucharadas-tiles'
export R2_PREFIX='catastro-sii'
export PUBLIC_TILES_BASE='https://tiles.3cucharadas.cl/catastro-sii'
export LEGAL_PUBLICATION_STATUS='AUTHORIZED_VECTOR'

run='20260718T212932Z'
assets="assets/data/catastro_sii/local/${run}"
```

No incluir las exportaciones en `.zshrc`, archivos versionados, historial
compartido o mensajes. Si se usa un archivo local, debe quedar fuera de Git y
con permisos de usuario.

## 4. Preflight y upload

Primero ejecutar el preflight sin red de escritura. Debe confirmar variables,
remoto rclone, CORS, manifest autorizado y allowlist de assets. Después, subir
únicamente los objetos versionados:

```bash
bash scripts/catastro_sii/preflight_r2.sh --run-dir "$assets"

bash scripts/catastro_sii/upload_r2.sh \
  "$assets/basemap_chile_${run}.pmtiles" \
  "$assets/basemap_chile_${run}.style.json" \
  "$assets/fonts/Noto Sans Regular/0-255.pbf" \
  "$assets/chile_comunas_brechas_${run}.pmtiles" \
  "$assets/predios_region_03_${run}.pmtiles"
```

`upload_r2.sh` usa nombres inmutables, `--checksum` y `--immutable`; rechaza
los insumos fuente y exige `GET Range` con CORS para cada PMTiles. Ante cualquier
fallo, detenerse: no promover el manifest ni hacer push del sitio.

## 5. Promoción del manifest del sitio

Sólo después del PASS de upload:

```bash
python3 scripts/catastro_sii/promote_manifest.py \
  --tiles-manifest "$assets/tiles_manifest_${run}_authorized.json" \
  --output assets/data/catastro_sii/manifest.json \
  --tiles-base "$PUBLIC_TILES_BASE" \
  --basemap-file "basemap_chile_${run}.pmtiles" \
  --basemap-style "basemap_chile_${run}.style.json" \
  --territories-output assets/data/catastro_sii/territories.json
```

El resultado versionado habilita las 345 comunas y conserva el piloto de
Atacama. Los PMTiles no entran al commit.

## 6. Build, revisión y publicación del sitio

```bash
bash scripts/catastro_sii/validate_build.sh
git add assets/data/catastro_sii/manifest.json assets/data/catastro_sii/territories.json
git commit --author='tatan <tatanlabra@gmail.com>' -m 'feat(catastro): publica capa comunal nacional'
```

Integrar y publicar por el flujo normal de GitLab Pages. En el sitio público,
confirmar: capa nacional visible, 345 comunas disponibles, Caldera/Diego cargan
predios, y una comuna fuera de Atacama no inicia un PMTiles predial.

Luego ejecutar el guard post-release, que compara manifest e índice público
contra el candidato local y prueba HTTP Range/CORS para basemap, fuente, comunas
y piloto Atacama:

```bash
bash scripts/catastro_sii/verify_public_tiles.sh \
  --tiles-base "$PUBLIC_TILES_BASE"
```

## 7. Rollback

Los objetos R2 son inmutables y permanecen disponibles. Para revertir el sitio,
restaurar el commit anterior de `assets/data/catastro_sii/manifest.json` y
`territories.json`, reconstruir y publicar. No borrar PMTiles para recuperar
servicio: el rollback debe ser de manifest, reversible y rápido.
