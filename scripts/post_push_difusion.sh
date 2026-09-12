#!/usr/bin/env bash
# Ejecutar tras verificar Pages. No es un hook nativo de Git; sin --live no envía.
set -euo pipefail
repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
if [ "$#" -eq 0 ]; then
  printf 'Uso: %s REF [--live] [--confirm "PUBLICAR REF"]\n' "$0" >&2
  exit 2
fi
python_bin="${DIFUSION_PYTHON:-/opt/entornos/3cucharadas-difusion/bin/python}"
if [ ! -x "$python_bin" ]; then
  printf 'Entorno de difusión no disponible. Fija DIFUSION_PYTHON al Python del entorno aprobado.\n' >&2
  exit 2
fi
export PYTHONPATH="$repo_root/difusion/src${PYTHONPATH:+:$PYTHONPATH}"
exec "$python_bin" -m cucharadas_difusion.cli --repo "$repo_root" closeout "$@"
