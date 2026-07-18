#!/usr/bin/env bash
set -euo pipefail

# Copy only versioned PMTiles/style/font assets needed for a localhost
# cartographic review. It never transfers canonical GeoParquet, FGB
# intermediates, reports or R2 credentials.
run_id="${1:?Uso: sync_local_preview_from_stata01.sh RUN_ID}"
[[ "${run_id}" =~ ^[0-9]{8}T[0-9]{6}Z$ ]] || { printf 'RUN_ID inválido: %s\n' "${run_id}" >&2; exit 2; }

: "${REMOTE_STATA01_HOST:=stata01}"
: "${REMOTE_TILES_ROOT:=/mnt/nas05/proyecto_catastral_sii/outputs/maps/catastro_sii_brechas_maps/tiles}"
: "${PYTHON_BIN:=python3}"

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
local_root="${repo_root}/assets/data/catastro_sii/local/${run_id}"
remote_root="${REMOTE_STATA01_HOST}:${REMOTE_TILES_ROOT}/${run_id}"
mkdir -p "${local_root}"
partial_dir="${local_root}/.rsync-partial"
mkdir -p "${partial_dir}"

sync_file() {
  local file="$1"
  rsync --archive --checksum --partial --partial-dir="${partial_dir}" --protect-args \
    "${remote_root}/${file}" "${local_root}/${file}"
}

for file in \
  "chile_comunas_brechas_${run_id}.pmtiles" \
  "predios_region_03_${run_id}.pmtiles" \
  "basemap_chile_${run_id}.pmtiles" \
  "basemap_chile_${run_id}.style.json" \
  "territories_${run_id}.json" \
  "tiles_manifest_${run_id}.json"; do
  sync_file "${file}"
done

mkdir -p "${local_root}/fonts/Noto Sans Regular"
sync_file "fonts/Noto Sans Regular/0-255.pbf"

"${PYTHON_BIN}" "$(dirname "$0")/write_local_preview_manifest.py" \
  --tiles-manifest "${local_root}/tiles_manifest_${run_id}.json" \
  --output "${local_root}/manifest.json" \
  --current-output "${repo_root}/assets/data/catastro_sii/local/manifest.json" \
  --tiles-base "/assets/data/catastro_sii/local/${run_id}" \
  --territories-output "${repo_root}/assets/data/catastro_sii/local/territories.json" \
  --basemap-file "basemap_chile_${run_id}.pmtiles" \
  --basemap-style "basemap_chile_${run_id}.style.json" \
  --basemap-fonts-dir "${local_root}/fonts"

sha256sum \
  "${local_root}/chile_comunas_brechas_${run_id}.pmtiles" \
  "${local_root}/predios_region_03_${run_id}.pmtiles" \
  "${local_root}/basemap_chile_${run_id}.pmtiles" \
  "${local_root}/basemap_chile_${run_id}.style.json" \
  "${local_root}/fonts/Noto Sans Regular/0-255.pbf" \
  "${local_root}/territories_${run_id}.json" \
  "${local_root}/tiles_manifest_${run_id}.json"
printf '%s\n' "Preview local listo: /catastro_sii_brecha/ (última corrida)"
printf '%s\n' "Corrida fijada: /catastro_sii_brecha/?catastroPreview=local&run=${run_id}"
