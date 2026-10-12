#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
site_root="$(dirname -- "$script_dir")"
workspace_root="${THESIS_WORKSPACE_ROOT:-$(cd -- "$site_root/../.." && pwd)}"
research_root="${THESIS_RESEARCH_ROOT:-$workspace_root/incubadora/tesis_mae_mejorada}"
playwright_module_path="${PLAYWRIGHT_MODULE_PATH:-$workspace_root/penta-agent/tools/playwright-local-mcp/node_modules/playwright}"
research_python="${THESIS_RESEARCH_PYTHON:-/opt/entornos/mamba312/bin/python}"

if (( $# != 0 )); then
  printf 'Uso: %s\n' "$0" >&2
  exit 2
fi

build_dir="$(mktemp -d /tmp/3c-post2-build.XXXXXX)"
preview_pid=""
cleanup() {
  if [[ -n "$preview_pid" ]]; then
    kill "$preview_pid" 2>/dev/null || true
    wait "$preview_pid" 2>/dev/null || true
  fi
  command rm -rf -- "$build_dir"
}
trap cleanup EXIT

cd -- "$site_root"
PYTHONPATH="$research_root/src" "$research_python" \
  "$research_root/scripts/316_build_scientific_release_freeze.py" --validate
PYTHONPATH="$research_root/src" "$research_python" \
  "$research_root/scripts/254_validate_article_claims.py" --validate
ruby scripts/verify_thesis_extension_post_ii.rb \
  --research-root "$research_root" \
  --workspace-root "$workspace_root" \
  --all
npm run build:catastro
npm run build:thesis-post2-map
npm run build:memoria-gobernada
BUNDLE_FROZEN=true JEKYLL_ENV=production bundle exec jekyll build \
  --disable-disk-cache \
  --future \
  --destination "$build_dir"
ruby scripts/verify_site_artifact.rb "$build_dir"

preview_port="$(ruby -rsocket -e 'server = TCPServer.new("127.0.0.1", 0); puts server.addr[1]; server.close')"
base_url="http://127.0.0.1:$preview_port"
python3 -m http.server "$preview_port" --bind 127.0.0.1 --directory "$build_dir" >/dev/null 2>&1 &
preview_pid="$!"
for _ in {1..50}; do
  if curl -fsS "$base_url/" >/dev/null 2>&1; then
    break
  fi
  sleep 0.1
done
curl -fsS "$base_url/" >/dev/null

PLAYWRIGHT_MODULE_PATH="$playwright_module_path" \
  node scripts/verify_thesis_extension_post_ii_browser.mjs --summary --base-url "$base_url"
