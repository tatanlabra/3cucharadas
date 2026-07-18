#!/usr/bin/env bash
set -euo pipefail

node --version
npm --version
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
