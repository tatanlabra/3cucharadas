#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "$0")/../.." && pwd)"
required_node="$(tr -d '[:space:]' < "${repo_root}/.nvmrc")"
current_node="$(node --version 2>/dev/null || true)"
if [[ "${current_node}" != "v${required_node}" ]]; then
  workspace_root="$(cd "${repo_root}/../.." && pwd)"
  node_home="${NODE24_HOME:-${workspace_root}/herramientas/local-config/runtimes/node-v${required_node}-linux-x64}"
  if [[ ! -x "${node_home}/bin/node" ]]; then
    printf 'Node %s requerido; define NODE24_HOME o instala el runtime en %s\n' \
      "${required_node}" "${node_home}" >&2
    exit 2
  fi
  export PATH="${node_home}/bin:${PATH}"
fi

node --version
npm --version
[[ "$(node --version)" == "v${required_node}" ]] || {
  printf 'Runtime Node inesperado; se esperaba v%s\n' "${required_node}" >&2
  exit 2
}
npm ci
npm run check:catastro
npm run check:catastro:static-css
npm run test:catastro
python3 -m unittest discover -s tests/catastro_sii -p 'test_*.py'
npm run build:catastro
output_dir="$(mktemp -d "${TMPDIR:-/tmp}/3cucharadas-catastro-check.XXXXXX")"
trap 'rm -rf "${output_dir}"' EXIT
JEKYLL_ENV=production bundle exec jekyll build -d "${output_dir}"
test -f "${output_dir}/catastro_sii_brecha/index.html"
test -f "${output_dir}/assets/data/catastro_sii/manifest.json"
test -f "${output_dir}/assets/dist/catastro_sii/manifest.json"
ruby scripts/verify_site_artifact.rb "${output_dir}"
