#!/usr/bin/env bash
set -euo pipefail

# Produce a Chile-only Protomaps/OSM PMTiles derivative for static hosting.
# The source archive is read through HTTP Range requests or from a local path;
# it is never copied in full, edited or mounted writable.
: "${PROTOMAPS_SOURCE:?Definir PROTOMAPS_SOURCE (URL PMTiles o ruta local)}"
output_dir="${1:?Uso: prepare_basemap.sh /ruta/salida version}"
version="${2:?Uso: prepare_basemap.sh /ruta/salida version}"
: "${BASEMAP_MAXZOOM:=14}"
: "${BASEMAP_BBOXES:=-76,-56,-66,-17;-110.5,-28.5,-108.5,-26.5;-81,-34.5,-78,-32}"
: "${PMTILES_IMAGE:=docker.io/protomaps/go-pmtiles@sha256:dcec7fe1bdd371e28289f2e7cef419a0a402289e02640c094570d54beb29fa8a}"
: "${CONTAINER_RUNTIME:=podman}"
# Vacías por defecto: se resuelven con mktemp dentro de run_pmtiles. Una ruta fija y
# predecible en /tmp permitiría a otro usuario del host pre-crear el storage root.
: "${CONTAINER_RUNROOT:=}"
: "${CONTAINER_STORAGE_ROOT:=}"
: "${FONT_BASE_URL:=https://protomaps.github.io/basemaps-assets/fonts}"
# Hash esperado del glifo Noto. Se publica en R2, así que una fuente alterada aguas
# arriba llegaría a producción sin este pin. Vacío = registrar sin verificar.
: "${FONT_PBF_SHA256:=}"

# `version` compone nombres de archivo y el patrón de sed que inyecta el estilo.
[[ "${version}" =~ ^[0-9]{8}T[0-9]{6}Z$ ]] || {
  printf 'version inválida: %s (se espera AAAAMMDDTHHMMSSZ)\n' "${version}" >&2
  exit 2
}

[[ "${BASEMAP_MAXZOOM}" =~ ^[0-9]+$ ]] && (( BASEMAP_MAXZOOM >= 0 && BASEMAP_MAXZOOM <= 15 )) || {
  printf 'BASEMAP_MAXZOOM inválido: %s\n' "${BASEMAP_MAXZOOM}" >&2
  exit 2
}
mkdir -p "${output_dir}"
tile="${output_dir}/basemap_chile_${version}.pmtiles"
style="${output_dir}/basemap_chile_${version}.style.json"
report="${output_dir}/basemap_chile_${version}.report.json"

run_pmtiles() {
  if [[ -n "${PMTILES_BIN:-}" ]]; then
    "${PMTILES_BIN}" "$@"
    return
  fi
  command -v "${CONTAINER_RUNTIME}" >/dev/null || {
    printf 'Falta PMTILES_BIN o runtime de contenedor: %s\n' "${CONTAINER_RUNTIME}" >&2
    exit 2
  }
  [[ -n "${CONTAINER_STORAGE_ROOT}" ]] || CONTAINER_STORAGE_ROOT="$(mktemp -d -t catastro-sii-storage-XXXXXXXXXX)"
  [[ -n "${CONTAINER_RUNROOT}" ]] || CONTAINER_RUNROOT="$(mktemp -d -t catastro-sii-runroot-XXXXXXXXXX)"
  mkdir -p "${CONTAINER_STORAGE_ROOT}" "${CONTAINER_RUNROOT}"
  "${CONTAINER_RUNTIME}" \
    --root "${CONTAINER_STORAGE_ROOT}" \
    --runroot "${CONTAINER_RUNROOT}" \
    --storage-driver vfs \
    run --rm \
    --volume "${output_dir}:/data:rw" \
    "${PMTILES_IMAGE}" "$@"
}

IFS=';' read -r -a requested_bboxes <<< "${BASEMAP_BBOXES}"
for bbox in "${requested_bboxes[@]}"; do
  [[ "${bbox}" =~ ^-?[0-9]+(\.[0-9]+)?,-?[0-9]+(\.[0-9]+)?,-?[0-9]+(\.[0-9]+)?,-?[0-9]+(\.[0-9]+)?$ ]] || {
    printf 'BBOX inválido: %s\n' "${bbox}" >&2
    exit 2
  }
done

region="${output_dir}/basemap_chile_${version}.region.geojson"
python3 - "${region}" "${BASEMAP_BBOXES}" <<'PY'
from __future__ import annotations
import json
import sys
from pathlib import Path

output, raw = sys.argv[1:]
coordinates = []
for text in raw.split(";"):
    west, south, east, north = (float(value) for value in text.split(","))
    coordinates.append([[
        [west, south], [east, south], [east, north], [west, north], [west, south],
    ]])
Path(output).write_text(json.dumps({"type": "MultiPolygon", "coordinates": coordinates}) + "\n", encoding="utf-8")
PY

rm -f "${tile}"
run_pmtiles extract "${PROTOMAPS_SOURCE}" "/data/$(basename "${tile}")" \
  "--region=/data/$(basename "${region}")" "--maxzoom=${BASEMAP_MAXZOOM}" \
  --download-threads=8 --overfetch=0.1
test -s "${tile}"
run_pmtiles verify "/data/$(basename "${tile}")"

mkdir -p "${output_dir}/fonts/Noto Sans Regular"
font_pbf="${output_dir}/fonts/Noto Sans Regular/0-255.pbf"
curl --fail --location --silent --show-error \
  "${FONT_BASE_URL}/Noto%20Sans%20Regular/0-255.pbf" \
  --output "${font_pbf}"
test -s "${font_pbf}"
font_sha256="$(sha256sum "${font_pbf}" | cut -d' ' -f1)"
if [[ -n "${FONT_PBF_SHA256}" && "${font_sha256}" != "${FONT_PBF_SHA256}" ]]; then
  printf 'Glifo Noto no coincide con el hash pinneado.\n  esperado: %s\n  obtenido: %s\n' \
    "${FONT_PBF_SHA256}" "${font_sha256}" >&2
  rm -f "${font_pbf}"
  exit 3
fi
[[ -n "${FONT_PBF_SHA256}" ]] \
  || printf 'Aviso: glifo Noto sin pin. Fijar FONT_PBF_SHA256=%s para verificarlo.\n' "${font_sha256}" >&2

sed "s/__BASEMAP_PM_TILES__/$(basename "${tile}")/g" \
  "$(dirname "$0")/protomaps-basemap-style.template.json" > "${style}"

python3 - "${report}" "${tile}" "${style}" "${PROTOMAPS_SOURCE}" "${PMTILES_IMAGE}" "${BASEMAP_MAXZOOM}" "${BASEMAP_BBOXES}" "${font_sha256}" <<'PY'
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

report, tile, style, source, image, maxzoom, bboxes, font_sha256 = sys.argv[1:]
def sha256(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()
Path(report).write_text(json.dumps({
    "source": source,
    "container_image": image,
    "maxzoom": int(maxzoom),
    "bboxes": bboxes.split(";"),
    "tile": {"file": Path(tile).name, "bytes": Path(tile).stat().st_size, "sha256": sha256(tile)},
    "style": {"file": Path(style).name, "sha256": sha256(style)},
    "font": {"file": "fonts/Noto Sans Regular/0-255.pbf", "sha256": font_sha256},
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
PY

rm -f "${region}" "${output_dir}"/basemap_chile_"${version}"_part_*.pmtiles
printf '%s\n' "Basemap listo: ${tile}"
