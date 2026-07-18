#!/usr/bin/env bash
set -euo pipefail

: "${LEGAL_PUBLICATION_STATUS:?Definir gate legal predial}"
: "${R2_REMOTE:?Definir remoto rclone ya autenticado}"
: "${R2_BUCKET:?Definir bucket R2}"
: "${R2_PREFIX:?Definir prefijo R2}"
: "${PUBLIC_TILES_BASE:?Definir origen público de tiles}"

[[ "$#" -gt 0 ]] || { printf '%s\n' 'Uso: upload_r2.sh <activo-publico> [activo-publico...]' >&2; exit 2; }
command -v rclone >/dev/null
command -v curl >/dev/null

remote="${R2_REMOTE}:${R2_BUCKET}/${R2_PREFIX%/}"
range_check() {
  local tile_name="$1" headers passed=0
  headers="$(mktemp "${TMPDIR:-/tmp}/catastro-r2-range.XXXXXX")"
  if curl --fail --silent --show-error --dump-header "${headers}" --output /dev/null \
      --header 'Origin: https://3cucharadas.cl' \
      --range 0-126 \
      "${PUBLIC_TILES_BASE%/}/${tile_name}" \
    && rg -qi '^HTTP/[0-9.]+ 206' "${headers}" \
    && rg -qi '^accept-ranges: bytes' "${headers}" \
    && rg -qi '^content-range: bytes 0-126/' "${headers}" \
    && rg -qi '^access-control-allow-origin: https://3cucharadas\.cl' "${headers}" \
    && rg -qi '^access-control-expose-headers:.*(accept-ranges|content-range)' "${headers}"; then
    passed=1
  fi
  rm -f "${headers}"
  [[ "${passed}" -eq 1 ]]
}

for asset in "$@"; do
  test -f "${asset}" || { printf 'Activo ausente: %s\n' "${asset}" >&2; exit 2; }
  name="$(basename "${asset}")"
  case "${name}" in
    chile_comunas_brechas_*.pmtiles|basemap_chile_*.pmtiles|basemap_chile_*.style.json) ;;
    predios_region_*.pmtiles)
      [[ "${LEGAL_PUBLICATION_STATUS}" == "AUTHORIZED_VECTOR" ]] || {
        printf '%s\n' 'ABORTADO: un PMTiles predial exige LEGAL_PUBLICATION_STATUS=AUTHORIZED_VECTOR.' >&2
        exit 2
      }
      ;;
    *)
      printf 'Activo no permitido para R2: %s\n' "${name}" >&2
      exit 2
      ;;
  esac
  rclone copyto "${asset}" "${remote}/${name}" --checksum --immutable --progress
  [[ "${name}" == *.pmtiles ]] && range_check "${name}"
done

printf '%s\n' 'Activos versionados copiados y cada PMTiles verificó GET Range/CORS. Promueve el manifest sólo después de este PASS.'
