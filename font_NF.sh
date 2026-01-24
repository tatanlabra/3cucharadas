#!/usr/bin/env bash
set -euo pipefail

# Script para copiar Fira Sans y FiraCode Nerd Font desde el sistema
# y generar WOFF2 para usarlas en el sitio Jekyll "3cucharadas".
#
# Uso:
#   ./font_NF.sh
#
# Requisitos:
#   - fc-list (fontconfig)
#   - woff2_compress (paquete woff2)

# --- Utilidades básicas ---

need_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "Error: falta el comando requerido: $1" >&2
    exit 1
  fi
}

need_cmd fc-list
need_cmd woff2_compress

# Directorio raíz del repositorio (donde vive este script)
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

FONTS_DIR="$ROOT_DIR/assets/fonts"
FIRA_SANS_DIR="$FONTS_DIR/fira-sans"
FIRACODE_NF_DIR="$FONTS_DIR/firacode-nerd"

mkdir -p "$FIRA_SANS_DIR" "$FIRACODE_NF_DIR"

echo "Raíz del proyecto:        $ROOT_DIR"
echo "Destino Fira Sans:        $FIRA_SANS_DIR"
echo "Destino FiraCode Nerd:    $FIRACODE_NF_DIR"
echo

# --- Funciones auxiliares ---

# Obtiene la ruta de un archivo de fuente usando fc-match (preferido) y,
# si falla, fc-list. Acepta un patrón completo, ej: "Fira Sans:style=Italic".
pick_font() {
  local pattern="$1"
  local match

  match="$(fc-match --format='%{file}\n' "$pattern" 2>/dev/null || true)"
  if [[ -n "$match" ]]; then
    echo "$match"
    return 0
  fi

  match="$(fc-list -f '%{file}\n' "$pattern" 2>/dev/null | head -n1 || true)"
  echo "$match"
}

# Copia y convierte a woff2 (si es TTF/OTF). Si se pasa un nombre destino,
# se fuerza ese basename (sin extensión) para homogeneizar los .woff2.
copy_and_woff2() {
  local src="$1"
  local dest_dir="$2"
  local dest_base="${3:-}"

  if [[ -z "${src:-}" ]]; then
    echo "Aviso: no se encontró la fuente solicitada; se omite." >&2
    return 0
  fi

  mkdir -p "$dest_dir"

  local base ext dest_font
  base="$(basename "$src")"
  ext="${base##*.}"
  if [[ -n "$dest_base" ]]; then
    base="${dest_base}.${ext}"
  fi
  dest_font="$dest_dir/$base"

  echo "  - Copiando: $src"
  cp "$src" "$dest_font"

  # Si es TTF u OTF, convertir a WOFF2 y eliminar el original
  if [[ "$ext" == "ttf" || "$ext" == "otf" ]]; then
    echo "    > Generando WOFF2 desde $base"
    local woff2_path="${dest_font%.*}.woff2"
    rm -f "$woff2_path"
    woff2_compress "$dest_font"

    echo "    > Generado: $(basename "$woff2_path")"

    # Eliminamos el TTF/OTF de trabajo y dejamos solo el WOFF2
    rm -f "$dest_font"
  else
    echo "    > Aviso: extensión $ext no es TTF/OTF, no se comprime."
  fi
}

# --- Fira Sans: Regular + Light, Italic, Medium, Bold ---

echo "Buscando Fira Sans (familia principal para texto)..."

declare -A FIRA_SANS_PATTERNS=(
  [Light]="Fira Sans:style=Light"
  [Regular]="Fira Sans:style=Regular"
  [Italic]="Fira Sans:style=Italic"
  [Medium]="Fira Sans:style=Medium"
  [Bold]="Fira Sans:style=Bold"
)

for variant in Light Regular Italic Medium Bold; do
  src_path="$(pick_font "${FIRA_SANS_PATTERNS[$variant]}")"
  echo "Fira Sans ${variant}: ${src_path:-no encontrada}"
  copy_and_woff2 "${src_path:-}" "$FIRA_SANS_DIR" "FiraSans-${variant}"
done

echo

# --- FiraCode Nerd Font: Regular "a secas" ---

echo "Buscando FiraCode Nerd Font (para código y símbolos Nerd)..."

src_nf="$(pick_font 'FiraCode Nerd Font:style=Regular')"
echo "FiraCode Nerd Font (Regular por defecto): ${src_nf:-no encontrada}"
copy_and_woff2 "${src_nf:-}" "$FIRACODE_NF_DIR" "FiraCodeNerdFont-Regular"

echo
echo "Fuentes preparadas en assets/fonts:"
find "$FONTS_DIR" -maxdepth 2 -type f -printf '  %P\n' || true

echo
echo "Listo. Ahora puedes referenciar estas fuentes desde tu main.scss."
