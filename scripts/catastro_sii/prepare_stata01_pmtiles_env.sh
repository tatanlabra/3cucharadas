#!/usr/bin/env bash
set -euo pipefail

# Provision a dedicated PMTiles environment without mutating the shared Conda env.
# The caller must choose an executable workspace on a filesystem below 90% usage.
: "${ENV_WORK_ROOT:?Definir ENV_WORK_ROOT en un volumen ejecutable y verificado}"
: "${CONDA_BIN:=conda}"
: "${SOURCE_ENV_PREFIX:=/opt/conda/envs/py_3_12_geopandas_jc}"

test -d "${ENV_WORK_ROOT}" || { printf 'ENV_WORK_ROOT no existe: %s\n' "${ENV_WORK_ROOT}" >&2; exit 2; }
test -x "${SOURCE_ENV_PREFIX}/bin/python" || { printf 'Entorno fuente inválido: %s\n' "${SOURCE_ENV_PREFIX}" >&2; exit 2; }
command -v "${CONDA_BIN}" >/dev/null || { printf 'Conda no está disponible: %s\n' "${CONDA_BIN}" >&2; exit 2; }

usage_pct="$(df -P "${ENV_WORK_ROOT}" | awk 'NR == 2 {gsub(/%/, "", $5); print $5}')"
if [[ -z "${usage_pct}" || "${usage_pct}" -ge 90 ]]; then
  printf 'ABORTADO: %s está a %s%% de uso; elegir un volumen bajo 90%%.\n' "${ENV_WORK_ROOT}" "${usage_pct:-desconocido}" >&2
  exit 2
fi

target_env="${ENV_WORK_ROOT}/conda-env"
export CONDA_PKGS_DIRS="${ENV_WORK_ROOT}/conda-pkgs"
mkdir -p "${CONDA_PKGS_DIRS}" "${ENV_WORK_ROOT}/logs"

if [[ ! -x "${target_env}/bin/python" ]]; then
  "${CONDA_BIN}" create --yes --prefix "${target_env}" --clone "${SOURCE_ENV_PREFIX}"
fi

# First choice: conda-forge for native binaries and the PMTiles CLI package.
for package in tippecanoe rclone; do
  if [[ ! -x "${target_env}/bin/${package}" ]]; then
    "${CONDA_BIN}" install --yes --override-channels -c conda-forge --prefix "${target_env}" "${package}"
  fi
done

if [[ ! -x "${target_env}/bin/pmtiles" ]]; then
  if ! "${CONDA_BIN}" install --yes --override-channels -c conda-forge --prefix "${target_env}" pmtiles; then
    # PyPI is an explicit last resort only for the Python PMTiles CLI.
    "${target_env}/bin/python" -m pip install --upgrade pmtiles
  fi
fi

"${target_env}/bin/python" -c 'import geopandas, pandas, pyarrow, shapely, fiona, pyogrio'
"${target_env}/bin/ogrinfo" --version
"${target_env}/bin/tippecanoe" --version
"${target_env}/bin/pmtiles" --help >/dev/null
"${target_env}/bin/rclone" version
printf 'PYTHON_BIN=%s\n' "${target_env}/bin/python"
