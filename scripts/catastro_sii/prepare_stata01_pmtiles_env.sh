#!/usr/bin/env bash
set -euo pipefail

# Install only the missing PMTiles tools in the maintained environment on stata01.
# It deliberately never creates or clones a Conda environment outside /opt/conda.
: "${PYTHON_BIN:=/opt/conda/envs/python_base/bin/python}"
: "${CONDA_BIN:=/usr/bin/conda}"

target_env="$(cd "$(dirname "${PYTHON_BIN}")/.." && pwd)"
test "${target_env}" = "/opt/conda/envs/python_base" || {
  printf 'ABORTADO: PYTHON_BIN debe pertenecer a /opt/conda/envs/python_base, recibió %s\n' "${PYTHON_BIN}" >&2
  exit 2
}
test -x "${PYTHON_BIN}" || { printf 'Python no ejecutable: %s\n' "${PYTHON_BIN}" >&2; exit 2; }
test -x "${CONDA_BIN}" || { printf 'Conda no ejecutable: %s\n' "${CONDA_BIN}" >&2; exit 2; }

missing=()
for tool in tippecanoe pmtiles-show rclone; do
  [[ -x "${target_env}/bin/${tool}" ]] && continue
  case "${tool}" in
    pmtiles-show) missing+=("pmtiles") ;;
    *) missing+=("${tool}") ;;
  esac
done

if [[ "${#missing[@]}" -gt 0 ]]; then
  # python_base is administrated under /opt/conda; sudo is needed for ordinary SSH users.
  sudo -n "${CONDA_BIN}" install --yes --override-channels -c conda-forge \
    --prefix "${target_env}" "${missing[@]}"
fi

"${PYTHON_BIN}" -c 'import geopandas, pandas, pyarrow, shapely, fiona, pyogrio'
"${target_env}/bin/ogrinfo" --version
"${target_env}/bin/tippecanoe" --version
test -x "${target_env}/bin/pmtiles-show"
"${target_env}/bin/rclone" version
printf 'PYTHON_BIN=%s\n' "${PYTHON_BIN}"
