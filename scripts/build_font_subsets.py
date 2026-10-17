#!/usr/bin/env python3
"""Genera los subconjuntos de Fira Sans y FiraCode que sirve el sitio (C1, auditoría UX 2026-10-17).

Los .woff2 completos quedan como fuente (scripts/catastro_sii/editorial_style.py los
usa para figuras); el CSS solo carga los *-sub.woff2. Antes pesaban 1.915.036 bytes
y FiraCode Nerd sola 1.138.228, aunque el código del sitio no usa ningún glifo Nerd.

    python3 scripts/build_font_subsets.py --site _site

Requiere fontTools (pyftsubset) en local; el CI no lo necesita: lee el manifiesto
assets/fonts/subset-manifest.json desde tests/test_ux_transversal_contract.py y
reprueba si el sitio usa un carácter que el subconjunto no cubre. Si eso pasa,
basta volver a correr este script y commitear las fuentes y el manifiesto.
"""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

from fontTools.ttLib import TTFont

ROOT = Path(__file__).resolve().parents[1]
FONTS = ROOT / "assets" / "fonts"
MANIFEST = FONTS / "subset-manifest.json"

# Rangos amplios a propósito: un carácter nuevo dentro de un bloque ya cubierto no
# obliga a regenerar. Son los mismos que declara `unicode-range` en main.scss.
TEXT_RANGES = ("U+0000-00FF,U+0100-017F,U+0131,U+0152-0153,U+02B0-02FF,U+0300-036F,"
               "U+0370-03FF,U+2000-206F,U+2070-209F,U+20AC,U+2100-214F,U+2190-21FF,"
               "U+2200-22FF,U+2300-23FF,U+25A0-25FF,U+2600-26FF,U+2700-27BF,U+2900-297F")
CODE_RANGES = ("U+0000-00FF,U+0100-017F,U+0300-036F,U+2000-206F,U+2190-21FF,U+2200-22FF,"
               "U+2500-257F,U+2580-259F,U+25A0-25FF")

JOBS = [
    ("fira-sans", f"FiraSans-{cut}", TEXT_RANGES) for cut in ("Light", "Regular", "Italic", "Medium", "Bold")
] + [("firacode-nerd", "FiraCodeNerdFont-Regular", CODE_RANGES)]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def cmap(path: Path) -> set[int]:
    return set(TTFont(path).getBestCmap() or {})


def used_codepoints(site: Path) -> tuple[set[int], set[int]]:
    text: set[int] = set()
    code: set[int] = set()
    for page in site.rglob("*.html"):
        raw = page.read_text(encoding="utf-8", errors="ignore")
        raw = re.sub(r"<(script|style)\b.*?</\1>", " ", raw, flags=re.S | re.I)
        raw = re.sub(r'<span class="katex.*?</span>\s*</span>\s*</span>', " ", raw, flags=re.S)  # KaTeX usa sus fuentes
        for block in re.findall(r"<(?:code|pre)\b[^>]*>(.*?)</(?:code|pre)>", raw, flags=re.S | re.I):
            code.update(ord(c) for c in html.unescape(re.sub(r"<[^>]+>", "", block)))
        attrs = " ".join(re.findall(r'(?:alt|title|aria-label|placeholder)="([^"]*)"', raw))
        text.update(ord(c) for c in html.unescape(re.sub(r"<[^>]+>", " ", raw) + " " + attrs))
    keep = lambda cps: {c for c in cps if c > 31}
    return keep(text), keep(code)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--site", type=Path, default=ROOT / "_site", help="sitio ya construido")
    args = parser.parse_args()
    if not args.site.is_dir():
        print(f"no existe el sitio construido: {args.site}", file=sys.stderr)
        return 2
    files, covered = {}, {}
    for folder, stem, ranges in JOBS:
        source = FONTS / folder / f"{stem}.woff2"
        target = FONTS / folder / f"{stem}-sub.woff2"
        subprocess.run(["pyftsubset", str(source), f"--unicodes={ranges}", "--layout-features=*",
                        "--flavor=woff2", f"--output-file={target}"], check=True)
        rel = target.relative_to(ROOT).as_posix()
        files[rel] = {"sha256": sha256(target), "bytes": target.stat().st_size,
                      "source_bytes": source.stat().st_size}
        covered.setdefault(folder, set()).update(cmap(target))
    text, code = used_codepoints(args.site)
    original_sans = cmap(FONTS / "fira-sans" / "FiraSans-Regular.woff2")
    original_code = cmap(FONTS / "firacode-nerd" / "FiraCodeNerdFont-Regular.woff2")
    manifest = {
        "schema": "font-subsets-v1",
        "generated_by": "scripts/build_font_subsets.py",
        "text_ranges": TEXT_RANGES,
        "code_ranges": CODE_RANGES,
        "files": files,
        "covered": {k: sorted(v) for k, v in covered.items()},
        # Usados por el sitio pero ausentes también en la fuente completa (emoji, etc.):
        # el navegador ya los tomaba de otra fuente; el subconjunto no cambia eso.
        "uncovered_by_original": {
            "fira-sans": sorted(text - original_sans),
            "firacode-nerd": sorted(code - original_code),
        },
    }
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    before = sum(v["source_bytes"] for v in files.values())
    after = sum(v["bytes"] for v in files.values())
    print(f"subconjuntos: {before} -> {after} bytes ({100 * (before - after) / before:.0f} % menos)")
    lost = (text - covered["fira-sans"]) & original_sans, (code - covered["firacode-nerd"]) & original_code
    if any(lost):
        print(f"FALTAN en el subconjunto (texto, código): {sorted(map(hex, lost[0]))} {sorted(map(hex, lost[1]))}",
              file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
