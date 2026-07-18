#!/usr/bin/env bash
set -euo pipefail

# Produce a Chile-only Protomaps/OSM PMTiles copy for static hosting. The source
# archive is never edited; this is a bounded derivative used only by the web map.
: "${PROTOMAPS_SOURCE:?Definir PROTOMAPS_SOURCE}"
output_dir="${1:?Uso: prepare_basemap.sh /ruta/salida version}"
version="${2:?Uso: prepare_basemap.sh /ruta/salida version}"

command -v pmtiles >/dev/null
mkdir -p "${output_dir}"
tile="${output_dir}/basemap_chile_${version}.pmtiles"

# Bounds include Chile continental and archipelagos; the selected source must carry
# its own licensing/attribution compatible with OSM and the published style.
pmtiles extract "${PROTOMAPS_SOURCE}" "${tile}" --bbox "-112,-57,-66,-17"
pmtiles verify "${tile}"
pmtiles show "${tile}" > "${output_dir}/basemap_chile_${version}.show.txt"

sed "s/__BASEMAP_PM_TILES__/basemap_chile_${version}.pmtiles/g" \
  "$(dirname "$0")/protomaps-basemap-style.template.json" \
  > "${output_dir}/basemap_chile_${version}.style.json"

printf '%s\n' "Basemap listo: ${tile}"
