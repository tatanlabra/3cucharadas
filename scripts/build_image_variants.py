#!/usr/bin/env python3
"""Genera variantes WebP de 800 y 1280 px para figuras grandes (C3, auditoría UX 2026-10-17).

Las figuras se servían a tamaño completo aunque su espacio en pantalla fuera mucho
menor: rss-governance-hero.jpg pesaba 288 KB a 1439 px, cara-a-cara-ihh.webp medía
2562 px para un hueco de 731. Este script escribe <nombre>-w800.webp y -w1280.webp
junto al original (solo anchos menores que el original) y _data/image_variants.json.
_plugins/responsive_images.rb agrega srcset/sizes a toda <img> cuyo src esté en ese
JSON, sin tocar los posts; el enlace a la imagen completa (zoom) no cambia.

    python3 scripts/build_image_variants.py

Agregar una figura: sumarla a SOURCES y volver a correr. El CI comprueba el JSON
desde tests/test_ux_transversal_contract.py (imagenes-responsivas).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "_data" / "image_variants.json"
WIDTHS = (800, 1280)
QUALITY = 88  # figuras con texto: se privilegia la legibilidad sobre unos pocos KB

SOURCES = [
    "assets/images/rss-governance-hero.jpg",
    "assets/images/multiagente-penta-agent-memoria-gobernada/cerebro-20-por-ciento-1600x1000.webp",
    "assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp",
    "assets/images/replica-tesis-establecimientos/cara-a-cara-ihh-en.webp",
    "assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp",
    "assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad-en.webp",
    "assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp",
    "assets/images/replica-tesis-establecimientos/face-to-face/s05-table08-original.png",
    "assets/images/replica-tesis-establecimientos/face-to-face/s01-table04-original.png",
] + [
    f"assets/images/replica-tesis-establecimientos/face-to-face/{name}-rerun-{lang}.webp"
    for name in ("s01-table-04-exact", "s02-figure-01-pattern", "s03-figure-11-hhi",
                 "s04-figure-02-rates", "s05-table-08-rounding", "s06-figure-04-net-mobility")
    for lang in ("es", "en")
]


def main() -> int:
    variants = {}
    before = after = 0
    for rel in SOURCES:
        source = ROOT / rel
        if not source.is_file():
            print(f"no existe: {rel}", file=sys.stderr)
            return 1
        image = Image.open(source)
        width, height = image.size
        entries = []
        for target_width in WIDTHS:
            if target_width >= width:
                continue
            target = source.with_name(f"{source.stem}-w{target_width}.webp")
            resized = image.convert("RGBA" if image.mode in ("RGBA", "LA", "P") else "RGB").resize(
                (target_width, round(height * target_width / width)), Image.LANCZOS)
            resized.save(target, "WEBP", quality=QUALITY, method=6)
            entries.append({"src": "/" + target.relative_to(ROOT).as_posix(), "w": target_width,
                            "bytes": target.stat().st_size})
        if not entries:
            continue
        variants["/" + rel] = {"w": width, "bytes": source.stat().st_size, "variants": entries}
        before += source.stat().st_size
        after += min(e["bytes"] for e in entries)
    payload = {
        "schema": "image-variants-v1",
        "generated_by": "scripts/build_image_variants.py",
        "sizes": "(max-width: 48em) calc(100vw - 2rem), 845px",
        "images": variants,
    }
    DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{len(variants)} figuras; original {before} B -> variante más chica {after} B")
    return 0


if __name__ == "__main__":
    sys.exit(main())
