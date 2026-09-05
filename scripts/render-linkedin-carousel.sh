#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage:
  scripts/render-linkedin-carousel.sh path/to/post-carrusel.html

Renders a LinkedIn carousel HTML into:
  - path/to/post-carrusel.pdf
  - path/to/post-preview-N-slides.png

The HTML must contain one <section class="slide"> per page.

Environment:
  LINKEDIN_CAROUSEL_WIDTH         Slide width in pixels. Default: 1080
  LINKEDIN_CAROUSEL_HEIGHT        Slide height in pixels. Default: 1350
  LINKEDIN_CAROUSEL_FIREFOX       Firefox executable. Default: firefox
  LINKEDIN_CAROUSEL_TIMEOUT       Seconds per slide render. Default: 30
  LINKEDIN_CAROUSEL_PDF           Override PDF output path.
  LINKEDIN_CAROUSEL_PREVIEW       Override preview output path.
  LINKEDIN_CAROUSEL_PREVIEW_COLS  Preview columns. Default: 3 for <=6 slides, 4 otherwise.
  CAROUSEL_SLIDES_DIR             Keep each slide as its own PNG in this directory.
                                  LinkedIn consumes the PDF; X consumes one PNG
                                  per post, and those died in the temp dir.
USAGE
}

if [[ "${1:-}" == "-h" || "${1:-}" == "--help" || $# -ne 1 ]]; then
  usage
  [[ $# -eq 1 ]] && exit 0
  exit 1
fi

html_path="$1"
if [[ ! -f "$html_path" ]]; then
  echo "No existe el HTML: $html_path" >&2
  exit 1
fi

for required in python3 montage; do
  if ! command -v "$required" >/dev/null 2>&1; then
    echo "No encuentro '$required' en PATH." >&2
    exit 1
  fi
done

if command -v magick >/dev/null 2>&1; then
  image_cmd=(magick)
elif command -v convert >/dev/null 2>&1; then
  image_cmd=(convert)
else
  echo "No encuentro ImageMagick: falta 'magick' o 'convert'." >&2
  exit 1
fi

firefox_bin="${LINKEDIN_CAROUSEL_FIREFOX:-firefox}"
if ! command -v "$firefox_bin" >/dev/null 2>&1; then
  echo "No encuentro Firefox ejecutable: $firefox_bin" >&2
  exit 1
fi

width="${LINKEDIN_CAROUSEL_WIDTH:-1080}"
height="${LINKEDIN_CAROUSEL_HEIGHT:-1350}"
timeout_s="${LINKEDIN_CAROUSEL_TIMEOUT:-30}"
html_abs="$(realpath "$html_path")"
stem="${html_abs%.html}"
base="$stem"
if [[ "$base" == *-carrusel ]]; then
  base="${base%-carrusel}"
fi

workdir="$(mktemp -d "${TMPDIR:-/tmp}/linkedin-carousel.XXXXXX")"
cleanup() {
  rm -rf "$workdir"
}
trap cleanup EXIT

slide_count="$(
  python3 - "$html_abs" "$workdir" "$width" "$height" <<'PY'
from pathlib import Path
import re
import sys

html_path = Path(sys.argv[1])
out_dir = Path(sys.argv[2])
width = int(sys.argv[3])
height = int(sys.argv[4])

html = html_path.read_text(encoding="utf-8")

# Cada lamina se rasteriza como HTML autonomo en un directorio temporal, asi que
# el CSS tiene que viajar dentro: un <link> relativo apuntaria a un fichero que
# ahi no existe. Se inlinea el contenido de cada hoja enlazada, en el orden en
# que aparece, y despues los <style> propios del documento --que asi siguen
# ganando como overrides--.
#
# Antes solo se admitia <style>: un carrusel con la hoja externa abortaba con
# "El HTML no contiene un bloque <style>". Se aborto la lectura, no se ignoro en
# silencio, pero igual bloqueaba deduplicar los 909 renglones de CSS repetido.
partes = []
for href in re.findall(r'<link[^>]+rel=["\']?stylesheet["\']?[^>]*>', html, re.I):
    m = re.search(r'href=["\']([^"\']+)["\']', href, re.I)
    if not m:
        continue
    ruta = (html_path.parent / m.group(1)).resolve()
    if not ruta.is_file():
        raise SystemExit(f"Hoja enlazada inexistente: {m.group(1)}")
    partes.append(ruta.read_text(encoding="utf-8"))

partes += re.findall(r"<style>(.*?)</style>", html, re.S | re.I)
if not partes:
    raise SystemExit("El HTML no trae CSS: ni <style> ni <link rel=stylesheet>.")

# La clase del <body> original tenia que viajar a cada lamina. Sin esto, un
# carrusel que declara `<body class="formato-x">` se renderizaba con la
# tipografia vertical dentro de la caja apaisada: el titulo salia a 83px en vez
# de 62, la cita ocupaba los 1600px enteros y se escribia encima del glifo de
# fondo. Y no fallaba nada: las imagenes salian 1600x900 porque ese tamano lo
# impone el override de abajo, no la hoja. Una comprobacion de geometria en
# verde que no probaba nada.
m_body = re.search(r'<body([^>]*)>', html, re.I)
body_attrs = m_body.group(1) if m_body else ""

sections = re.findall(r'<section class="slide">.*?</section>', html, re.S)
if not sections:
    raise SystemExit('El HTML no contiene <section class="slide">.')

style = "\n".join(partes)
base_href = html_path.parent.as_uri() + "/"
override = f"""
html,body{{background:#101116;margin:0;padding:0;width:{width}px;height:{height}px;overflow:hidden}}
body{{display:block}}
.hint{{display:none!important}}
.slide{{width:{width}px;height:{height}px;max-width:none;border:0;border-radius:0;box-shadow:none;aspect-ratio:auto}}
"""

for index, section in enumerate(sections, 1):
    rendered = f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<base href="{base_href}">
<title>{html_path.stem} - slide {index:02d}</title>
<style>{style}
{override}</style>
</head>
<body{body_attrs}>
{section}
</body>
</html>
"""
    (out_dir / f"slide-{index:02d}.html").write_text(rendered, encoding="utf-8")

print(len(sections))
PY
)"

pdf_path="${LINKEDIN_CAROUSEL_PDF:-$stem.pdf}"
preview_path="${LINKEDIN_CAROUSEL_PREVIEW:-${base}-preview-${slide_count}-slides.png}"

if [[ -n "${LINKEDIN_CAROUSEL_PREVIEW_COLS:-}" ]]; then
  preview_cols="$LINKEDIN_CAROUSEL_PREVIEW_COLS"
elif (( slide_count <= 6 )); then
  preview_cols=3
else
  preview_cols=4
fi

slides=()
for n in $(seq 1 "$slide_count"); do
  i="$(printf "%02d" "$n")"
  slide_html="$workdir/slide-$i.html"
  slide_png="$workdir/slide-$i.png"
  log="$workdir/firefox-$i.log"
  if ! timeout "$timeout_s" "$firefox_bin" \
      --headless \
      --screenshot "$slide_png" \
      --window-size "$width,$height" \
      "file://$slide_html" >"$log" 2>&1; then
    echo "Fallo el render del slide $i. Log:" >&2
    sed -n '1,120p' "$log" >&2
    exit 1
  fi
  slides+=("$slide_png")
done

"${image_cmd[@]}" "${slides[@]}" "$pdf_path"
# La miniatura estaba fijada a 500x625, que es la proporcion de la lamina
# vertical. Con una apaisada de 1600x900 ImageMagick no la deforma --respeta el
# aspecto-- pero deja cada celda con 200 px de banda muerta arriba y abajo, y el
# contacto se vuelve ilegible. Se deriva del tamano real de la lamina.
thumb_w=500
thumb_h="$(( 500 * height / width ))"
montage "${slides[@]}" \
  -thumbnail "${thumb_w}x${thumb_h}" \
  -tile "${preview_cols}x" \
  -geometry "${thumb_w}x${thumb_h}+24+24" \
  -background '#0c0d12' \
  "$preview_path"

if [[ -n "${CAROUSEL_SLIDES_DIR:-}" ]]; then
  mkdir -p "$CAROUSEL_SLIDES_DIR"
  for n in $(seq 1 "$slide_count"); do
    i="$(printf "%02d" "$n")"
    command cp -f "$workdir/slide-$i.png" "$CAROUSEL_SLIDES_DIR/$(basename "$stem")-$i.png"
  done
  printf 'slides_dir=%s\n' "$CAROUSEL_SLIDES_DIR"
fi

printf 'slides=%s\n' "$slide_count"
printf 'pdf=%s\n' "$pdf_path"
printf 'preview=%s\n' "$preview_path"
