#!/usr/bin/env bash
set -euo pipefail

: "${LEGAL_PUBLICATION_STATUS:?Definir gate legal}"
: "${R2_REMOTE:?Definir remoto rclone ya autenticado}"
: "${R2_BUCKET:?Definir bucket R2}"
: "${R2_PREFIX:?Definir prefijo R2}"
: "${PUBLIC_TILES_BASE:?Definir origen público de tiles}"

if [[ "${LEGAL_PUBLICATION_STATUS}" != "AUTHORIZED_VECTOR" ]]; then
  printf '%s\n' 'ABORTADO: los PMTiles prediales sólo se publican con LEGAL_PUBLICATION_STATUS=AUTHORIZED_VECTOR.' >&2
  exit 2
fi

source_dir="${1:?Uso: upload_r2.sh /ruta/a/tiles-versionados}"
test -d "${source_dir}"
command -v rclone >/dev/null
command -v curl >/dev/null

rclone copy "${source_dir}" "${R2_REMOTE}:${R2_BUCKET}/${R2_PREFIX}/" \
  --include "*.pmtiles" --include "*.json" --checksum --immutable --progress

first_tile="$(fd -t f -e pmtiles . "${source_dir}" | head -n 1)"
test -n "${first_tile}"
tile_name="$(basename "${first_tile}")"
curl --fail --silent --show-error --head \
  --header 'Origin: https://3cucharadas.cl' \
  --header 'Range: bytes=0-126' \
  "${PUBLIC_TILES_BASE%/}/${tile_name}" | rg -i '^(HTTP/.* 206|accept-ranges: bytes|content-range:)'
