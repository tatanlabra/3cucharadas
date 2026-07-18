#!/usr/bin/env bash
set -euo pipefail

# Se ejecuta en stata01, después de sincronizar código e insumos autorizados.
: "${SITE_SOURCE_DIR:?Definir SITE_SOURCE_DIR con la copia versionada del sitio}"
: "${TILES_OUTPUT_ROOT:?Definir TILES_OUTPUT_ROOT en un filesystem verificado}"
: "${PREDIOS_SOURCE_DIR:?Definir PREDIOS_SOURCE_DIR en stata01}"
: "${COMUNAS_SOURCE:?Definir COMUNAS_SOURCE en stata01}"
: "${METRICAS_COMUNALES_SOURCE:?Definir METRICAS_COMUNALES_SOURCE en stata01}"
: "${COMUNAS_EXCLUDED_CODES:?Declarar las comunas métricas sin geometría autorizada}"
: "${LEGAL_PUBLICATION_STATUS:=PENDING}"
: "${PYTHON_BIN:=/opt/conda/envs/python_base/bin/python}"

test -x "${PYTHON_BIN}" || { printf 'PYTHON_BIN no es ejecutable: %s\n' "${PYTHON_BIN}" >&2; exit 2; }
test -d "${SITE_SOURCE_DIR}" || { printf 'SITE_SOURCE_DIR no existe: %s\n' "${SITE_SOURCE_DIR}" >&2; exit 2; }
test -d "${TILES_OUTPUT_ROOT}" || { printf 'TILES_OUTPUT_ROOT no existe: %s\n' "${TILES_OUTPUT_ROOT}" >&2; exit 2; }

# Nunca escribir PMTiles en un volumen que ya está en zona de riesgo.
usage_pct="$(df -P "${TILES_OUTPUT_ROOT}" | awk 'NR == 2 {gsub(/%/, "", $5); print $5}')"
if [[ -z "${usage_pct}" || "${usage_pct}" -ge 90 ]]; then
  printf 'ABORTADO: %s está a %s%% de uso; elegir un volumen bajo 90%%.\n' "${TILES_OUTPUT_ROOT}" "${usage_pct:-desconocido}" >&2
  exit 2
fi

tool_dir="$(dirname "${PYTHON_BIN}")"
env_prefix="$(cd "${tool_dir}/.." && pwd)"
export PATH="${tool_dir}:${PATH}"
# Keep GDAL/pyproj bound to the same Conda prefix even when the SSH shell was
# not activated with `conda activate`.
test -d "${env_prefix}/share/proj" || { printf 'Datos PROJ no disponibles: %s\n' "${env_prefix}/share/proj" >&2; exit 2; }
export PROJ_DATA="${env_prefix}/share/proj"
run_id="$(date -u +%Y%m%dT%H%M%SZ)"
output_dir="${TILES_OUTPUT_ROOT}/${run_id}"
IFS=',' read -r -a excluded_codes <<< "${COMUNAS_EXCLUDED_CODES}"
excluded_args=()
for code in "${excluded_codes[@]}"; do
  code="${code//[[:space:]]/}"
  [[ -n "${code}" ]] && excluded_args+=(--excluded-commune-code "${code}")
done
[[ "${#excluded_args[@]}" -gt 0 ]] || { printf 'No hay exclusiones comunales declaradas.\n' >&2; exit 2; }

command -v tippecanoe >/dev/null
command -v pmtiles-show >/dev/null
"${PYTHON_BIN}" -c 'import geopandas, pandas, pyarrow'

mkdir -p "${output_dir}"
"${PYTHON_BIN}" "${SITE_SOURCE_DIR}/scripts/catastro_sii/build_pmtiles.py" \
  --output-dir "${output_dir}" \
  --version "${run_id}" \
  --legal-status "${LEGAL_PUBLICATION_STATUS}" \
  --build-communes \
  --comunas-source "${COMUNAS_SOURCE}" \
  --metrics-source "${METRICAS_COMUNALES_SOURCE}" \
  --build-atacama-pilot \
  --predios-source-dir "${PREDIOS_SOURCE_DIR}" \
  "${excluded_args[@]}"

printf 'Piloto privado generado en %s\n' "${output_dir}"
