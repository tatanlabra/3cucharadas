#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  scripts/difusion-review-url.sh [ref]

Starts or reuses the local diffusion review UI and prints the review URL.
If ref is omitted, the most recently modified draft in difusion/state/drafts is used.

Environment:
  CUCHARADAS_DIFUSION_STATE_DIR  Override the local state dir.
  CUCHARADAS_DIFUSION_PYTHON     Override the Python executable.
USAGE
}

repo_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
state_dir="${CUCHARADAS_DIFUSION_STATE_DIR:-$repo_root/difusion/state}"
python_bin="${CUCHARADAS_DIFUSION_PYTHON:-/opt/entornos/3cucharadas-difusion/bin/python}"
ref="${1:-}"

if [[ "${ref:-}" == "-h" || "${ref:-}" == "--help" ]]; then
  usage
  exit 0
fi

if [[ -z "$ref" ]]; then
  drafts_dir="$state_dir/drafts"
  if [[ ! -d "$drafts_dir" ]]; then
    echo "No existe $drafts_dir; prepara primero un borrador de difusion." >&2
    exit 1
  fi
  latest="$(
    find "$drafts_dir" -maxdepth 1 -type f -name '*.json' -printf '%T@ %f\n' |
      sort -rn |
      head -n 1 |
      sed -E 's/^[^ ]+ //; s/\.json$//'
  )"
  if [[ -z "$latest" ]]; then
    echo "No hay borradores en $drafts_dir." >&2
    exit 1
  fi
  ref="$latest"
fi

if [[ ! -x "$python_bin" ]]; then
  echo "No encuentro Python ejecutable: $python_bin" >&2
  exit 1
fi

if ! command -v tmux >/dev/null 2>&1; then
  echo "tmux no esta disponible; ejecuta manualmente:" >&2
  echo "PYTHONPATH=difusion/src $python_bin -m cucharadas_difusion.cli --state-dir '$state_dir' review '$ref' --no-open" >&2
  exit 1
fi

if ! command -v curl >/dev/null 2>&1; then
  echo "curl no esta disponible; no puedo validar la URL local del visor." >&2
  exit 1
fi

safe_ref="$(printf '%s' "$ref" | tr -c 'A-Za-z0-9_.-' '-')"
session="3cucharadas-difusion-review-$safe_ref"

capture_url() {
  tmux capture-pane -t "$session" -J -p 2>/dev/null |
    grep -Eo 'http://127\.0\.0\.1:[0-9]+/#token=[A-Za-z0-9_-]+' |
    tail -n 1
}

url_ok() {
  local candidate="$1"
  local endpoint="${candidate%%#*}"
  [[ -n "$endpoint" ]] || return 1
  curl -fsS -o /dev/null "$endpoint"
}

if tmux has-session -t "$session" 2>/dev/null; then
  url="$(capture_url || true)"
  if [[ -n "$url" ]] && url_ok "$url"; then
    printf '%s\n' "$url"
    exit 0
  fi
  tmux kill-session -t "$session"
fi

printf -v command \
  'PYTHONPATH=%q %q -m cucharadas_difusion.cli --state-dir %q review %q --no-open' \
  "$repo_root/difusion/src" \
  "$python_bin" \
  "$state_dir" \
  "$ref"

tmux new-session -d -s "$session" -c "$repo_root" "$command"

url=""
for _ in {1..80}; do
  url="$(capture_url || true)"
  if [[ -n "$url" ]] && url_ok "$url"; then
    printf '%s\n' "$url"
    exit 0
  fi
  sleep 0.1
done

echo "El visor no entrego una URL valida. Revisa con:" >&2
echo "tmux capture-pane -t '$session' -J -p" >&2
exit 1
