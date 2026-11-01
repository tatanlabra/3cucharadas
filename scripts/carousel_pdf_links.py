#!/usr/bin/env python3
"""Agrega anotaciones /Link al PDF de un carrusel a partir de las cajas medidas en el navegador.

render-linkedin-carousel.sh arma el PDF con capturas PNG (ImageMagick), así que los <a href>
del HTML no sobreviven. Este paso los repone sobre la misma geometría, sin tocar la imagen.
El visor de documentos de LinkedIn puede no hacerlos clicables; en el PDF descargado sí lo son.

Uso: carousel_pdf_links.py PDF RECTS.json ANCHO_PX ALTO_PX
"""
import json
import sys

from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link


def main() -> int:
    pdf, rects_path, width, height = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    with open(rects_path, encoding="utf-8") as fh:
        rects = json.load(fh)
    writer = PdfWriter(clone_from=PdfReader(pdf))
    for rect in rects:
        if not rect["href"].startswith("https://"):
            raise SystemExit(f"enlace no absoluto ni https: {rect['href']}")
        if not 0 <= rect["page"] < len(writer.pages):
            raise SystemExit(f"lámina {rect['page'] + 1} fuera del PDF ({len(writer.pages)} páginas)")
        if rect["w"] <= 0 or rect["h"] <= 0:
            raise SystemExit(f"caja vacía para {rect['href']}")
        box = writer.pages[rect["page"]].mediabox
        sx, sy = float(box.width) / width, float(box.height) / height
        top = float(box.height) - rect["y"] * sy
        writer.add_annotation(
            page_number=rect["page"],
            annotation=Link(rect=(rect["x"] * sx, top - rect["h"] * sy, (rect["x"] + rect["w"]) * sx, top),
                            url=rect["href"], border=[0, 0, 0]),
        )
    writer.write(pdf)
    print(f"links={len(rects)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
