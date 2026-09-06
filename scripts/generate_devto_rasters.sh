#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for command_name in rsvg-convert magick identify; do
  if ! command -v "$command_name" >/dev/null 2>&1; then
    echo "Falta dependencia para rásteres DEV.to: $command_name" >&2
    exit 1
  fi
done

render_svg() {
  local source_path="$1"
  local width="$2"
  local expected_dimensions="$3"
  local target_path="$4"
  local full_source="$ROOT/$source_path"
  local full_target="$ROOT/$target_path"
  local rendered
  local optimized
  local actual_dimensions

  rendered="$(mktemp "${TMPDIR:-/tmp}/devto-svg.XXXXXX.png")"
  optimized="$(mktemp "${TMPDIR:-/tmp}/devto-png.XXXXXX.png")"
  trap 'command rm -f "$rendered" "$optimized"' RETURN

  rsvg-convert --width "$width" --output "$rendered" "$full_source"
  magick "$rendered" -strip -colors 128 -define png:compression-level=9 "PNG8:$optimized"

  actual_dimensions="$(identify -format '%wx%h' "$optimized")"
  if [[ "$actual_dimensions" != "$expected_dimensions" ]]; then
    echo "Dimensiones inesperadas para $target_path: $actual_dimensions (esperadas $expected_dimensions)" >&2
    exit 1
  fi

  command mv -f "$optimized" "$full_target"
  command rm -f "$rendered"
  trap - RETURN
  printf '%s -> %s (%s)\n' "$source_path" "$target_path" "$actual_dimensions"
}

render_svg \
  "assets/images/multiagente-penta-agent-memoria/flujo-memoria-penta-agent-en.svg" \
  1200 \
  "1200x2172" \
  "assets/images/multiagente-penta-agent-memoria/flujo-memoria-penta-agent-en-devto-1200x2172.png"

render_svg \
  "assets/images/structured-shell/fig-d2-shell-families-mobile-en.svg" \
  1080 \
  "1080x2710" \
  "assets/images/structured-shell/fig-d2-shell-families-mobile-en-devto-1080x2710.png"

render_svg \
  "assets/images/structured-shell/fig-d2-shell-families-en.svg" \
  1600 \
  "1600x1360" \
  "assets/images/structured-shell/fig-d2-shell-families-en-devto-1600x1360.png"

render_svg \
  "assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources.svg" \
  1600 \
  "1600x1169" \
  "assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources-devto-1600x1169.png"
