#!/usr/bin/env bash
set -euo pipefail

# Copy only the two tested PMTiles plus the two small manifests needed for a
# localhost cartographic review. It never transfers the canonical GeoParquet,
# FGB intermediates, reports or any R2 credentials.
run_id="${1:?Uso: sync_local_preview_from_stata01.sh RUN_ID}"
[[ "${run_id}" =~ ^[0-9]{8}T[0-9]{6}Z$ ]] || { printf 'RUN_ID inválido: %s\n' "${run_id}" >&2; exit 2; }

: "${REMOTE_STATA01_HOST:=stata01}"
: "${REMOTE_TILES_ROOT:=/mnt/nas05/proyecto_catastral_sii/outputs/maps/catastro_sii_brechas_maps/tiles}"
: "${PYTHON_BIN:=python3}"

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
local_root="${repo_root}/assets/data/catastro_sii/local/${run_id}"
remote_root="${REMOTE_STATA01_HOST}:${REMOTE_TILES_ROOT}/${run_id}"
mkdir -p "${local_root}"

for file in \
  "chile_comunas_brechas_${run_id}.pmtiles" \
  "predios_region_03_${run_id}.pmtiles" \
  "territories_${run_id}.json" \
  "tiles_manifest_${run_id}.json"; do
  rsync --archive --checksum --protect-args "${remote_root}/${file}" "${local_root}/${file}"
done

"${PYTHON_BIN}" "$(dirname "$0")/write_local_preview_manifest.py" \
  --tiles-manifest "${local_root}/tiles_manifest_${run_id}.json" \
  --output "${local_root}/manifest.json" \
  --current-output "${repo_root}/assets/data/catastro_sii/local/manifest.json" \
  --tiles-base "/assets/data/catastro_sii/local/${run_id}" \
  --territories-output "${repo_root}/assets/data/catastro_sii/local/territories.json"

sha256sum \
  "${local_root}/chile_comunas_brechas_${run_id}.pmtiles" \
  "${local_root}/predios_region_03_${run_id}.pmtiles" \
  "${local_root}/territories_${run_id}.json" \
  "${local_root}/tiles_manifest_${run_id}.json"
printf '%s\n' "Preview local listo: /catastro_sii_brecha/ (última corrida)"
printf '%s\n' "Corrida fijada: /catastro_sii_brecha/?catastroPreview=local&run=${run_id}"
