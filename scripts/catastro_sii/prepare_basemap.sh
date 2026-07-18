#!/usr/bin/env bash
set -euo pipefail

# Produce a Chile-only Protomaps/OSM PMTiles copy for static hosting. The source
# archive is never edited; this is a bounded derivative used only by the web map.
: "${PROTOMAPS_SOURCE:?Definir PROTOMAPS_SOURCE}"
output_dir="${1:?Uso: prepare_basemap.sh /ruta/salida version}"
version="${2:?Uso: prepare_basemap.sh /ruta/salida version}"
: "${PYTHON_BIN:=/opt/conda/envs/python_base/bin/python}"
: "${BASEMAP_MAXZOOM:=14}"

test -r "${PROTOMAPS_SOURCE}"
test -x "${PYTHON_BIN}"
"${PYTHON_BIN}" -c 'import pmtiles'
mkdir -p "${output_dir}"
tile="${output_dir}/basemap_chile_${version}.pmtiles"

# Bounds include Chile continental and archipelagos; the selected source must carry
# its own licensing/attribution compatible with OSM and the published style.
"${PYTHON_BIN}" "$(dirname "$0")/extract_pmtiles_bbox.py" \
  --input "${PROTOMAPS_SOURCE}" \
  --output "${tile}" \
  --bbox "-112,-57,-66,-17" \
  --maxzoom "${BASEMAP_MAXZOOM}" \
  --report "${output_dir}/basemap_chile_${version}.report.json"

sed "s/__BASEMAP_PM_TILES__/basemap_chile_${version}.pmtiles/g" \
  "$(dirname "$0")/protomaps-basemap-style.template.json" \
  > "${output_dir}/basemap_chile_${version}.style.json"

printf '%s\n' "Basemap listo: ${tile}"
