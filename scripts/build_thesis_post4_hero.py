#!/usr/bin/env python3
"""Export the approved Post IV illustration; never generate measured graphics."""
import argparse
import hashlib
import json
from pathlib import Path

from PIL import Image, ImageOps
import yaml

ROOT = Path(__file__).resolve().parents[1]
SLUG = "cierre-escolar-educacion-superior-causal-ml"
VARIANTS = (
    ("hero-1600x900.webp", (1600, 900), 250000, False),
    ("hero-mobile-800x450.webp", (800, 450), 100000, False),
    ("teaser-1280x720.webp", (1280, 720), 180000, True),
    ("teaser-mobile-640x360.webp", (640, 360), 70000, True),
    ("og-1200x630.webp", (1200, 630), 180000, True),
)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    args = parser.parse_args()
    source = args.source.resolve()
    picture = ImageOps.exif_transpose(Image.open(source)).convert("RGB")
    destination = ROOT / "assets/images/heroes-v2" / SLUG
    catalogue_path = ROOT / "_data/visuales" / f"{SLUG}.yml"
    catalogue = yaml.safe_load(catalogue_path.read_text())
    records = []
    for name, size, budget, compact in VARIANTS:
        frame = picture
        if compact:
            # The hero reserves its left 45% for HTML. Social variants keep the
            # students and both destinations while reducing that empty margin.
            frame = picture.crop((round(picture.width * .22), 0, picture.width, picture.height))
        frame = ImageOps.fit(frame, size, Image.Resampling.LANCZOS, centering=(.65, .5))
        target = destination / name
        for quality in (88, 84, 80, 76, 72):
            frame.save(target, "WEBP", quality=quality, method=6)
            if target.stat().st_size <= budget:
                break
        else:
            raise RuntimeError(f"Image budget exceeded: {target}")
        piece = next(p for p in catalogue["piezas"] if Path(p["archivo"]).name == name)
        piece.update(ancho=size[0], alto=size[1], bytes=target.stat().st_size, sha256=sha(target))
        piece["alt"] = {
            "es": "Ilustración conceptual nocturna de estudiantes ante caminos abiertos hacia un instituto técnico y un campus universitario; al fondo queda su liceo.",
            "en": "Conceptual night-time illustration of students facing open paths towards a technical institute and a university campus, with their secondary school behind them.",
        }
        piece["provenance"] = {
            "status": "generated_this_revision",
            "source_sha256": sha(source),
            "source_file": str(source.relative_to(ROOT)),
            "tool": "image_gen",
            "interface": "Codex built-in image generation",
            "note": {
                "es": "Ilustración conceptual generada con ImageGen mediante Codex; no representa instituciones específicas ni un efecto causal demostrado.",
                "en": "Conceptual illustration generated with ImageGen through Codex; it does not depict specific institutions or an established causal effect.",
            },
            "encoding": f"WebP quality={quality}; Lanczos; compact_crop={compact}",
        }
        records.append({"file": str(target.relative_to(ROOT)), "bytes": target.stat().st_size, "size": list(size), "sha256": sha(target), "quality": quality})
    catalogue_path.write_text(yaml.safe_dump(catalogue, allow_unicode=True, sort_keys=False))
    print(json.dumps({"source_sha256": sha(source), "variants": records}, indent=2))


if __name__ == "__main__":
    main()
