#!/usr/bin/env python3
"""Autohospeda Font Awesome Free 6.7.2 reducido a los íconos que usa el sitio (C2, auditoría UX 2026-10-17).

Antes se cargaba completo desde cdnjs (~315 KB entre CSS y fuentes) para 27 íconos.
La fuente de verdad es _vendor-src/fontawesome-6.7.2/ (no se publica): el CSS
coincide con el integrity sha512 que usaba head.html. Este script:
  1. lee las clases fa-* usadas en el sitio construido;
  2. conserva del CSS el núcleo (familias, tamaños, animaciones) y SOLO las reglas
     de íconos usados; descarta las caras de compatibilidad v4/v5;
  3. reduce las tres fuentes a los codepoints de esos íconos;
  4. escribe assets/vendor/fontawesome/{fa-subset.css,webfonts/,subset-manifest.json}.

    python3 scripts/build_fontawesome_subset.py --site _site

Requiere fontTools en local. El CI lee el manifiesto desde
tests/test_ux_transversal_contract.py (iconos-autohospedados) y reprueba si una
página usa un ícono que el subconjunto no trae.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "_vendor-src" / "fontawesome-6.7.2"
OUT = ROOT / "assets" / "vendor" / "fontawesome"
FONTS = {"fa-solid-900": "solid", "fa-regular-400": "regular", "fa-brands-400": "brands"}
MODIFIERS = {"fa-fw", "fa-lg", "fa-xs", "fa-sm", "fa-1x", "fa-2x", "fa-3x", "fa-4x", "fa-5x",
             "fa-solid", "fa-regular", "fa-brands", "fa-spin", "fa-pulse", "fa-border", "fa-inverse"}


def used_icon_classes(site: Path) -> set[str]:
    """Íconos en el HTML construido y los que el JS inserta en tiempo de ejecución
    (main.min.js del tema agrega fa-copy, fa-check y fa-link al copiar código)."""
    classes: set[str] = set()
    for page in site.rglob("*.html"):
        for attr in re.findall(r'class="([^"]*\bfa[sbr]?\b[^"]*)"', page.read_text(encoding="utf-8", errors="ignore")):
            classes.update(c for c in attr.split() if c.startswith("fa-") and c not in MODIFIERS)
    for script in site.joinpath("assets", "js").rglob("*.js"):
        classes.update(c for c in re.findall(r"\bfa-[a-z0-9-]+", script.read_text(encoding="utf-8", errors="ignore"))
                       if c not in MODIFIERS)
    return classes


def split_rules(css: str) -> list[str]:
    """Reglas de nivel superior del CSS minificado (respeta @keyframes/@media anidados)."""
    rules, depth, start = [], 0, 0
    for index, char in enumerate(css):
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                rules.append(css[start:index + 1])
                start = index + 1
    return rules


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n", 1)[0])
    parser.add_argument("--site", type=Path, default=ROOT / "_site")
    args = parser.parse_args()
    css = (SOURCE / "css" / "all.min.css").read_text(encoding="utf-8")
    banner = css[: css.index("*/") + 2]
    used = used_icon_classes(args.site)
    if not used:
        print(f"no encontré íconos en {args.site}", file=sys.stderr)
        return 2
    kept, codepoints, found = [], {}, set()
    for rule in split_rules(css[len(banner):]):
        head = rule[: rule.index("{")]
        icon = re.fullmatch(r"\s*((?:\.fa-[a-z0-9-]+,?)+)\{--fa:\"\\([0-9a-f]+)\"\}\s*", rule)
        if icon:
            names = {n.lstrip(".") for n in icon.group(1).split(",")}
            if names & used:
                kept.append(rule.strip())
                for name in names & used:
                    codepoints[name] = int(icon.group(2), 16)
                found |= names & used
            continue
        if head.lstrip().startswith("@font-face"):
            family = re.search(r'font-family:"([^"]+)"', rule).group(1)
            if family not in ("Font Awesome 6 Free", "Font Awesome 6 Brands"):
                continue  # caras de compatibilidad v4/v5: el sitio no las usa
            font = re.search(r"webfonts/(fa-[a-z]+-\d+)\.woff2", rule).group(1)
            rule = re.sub(r"src:[^;}]+", f'src:url(webfonts/{font}-sub.woff2) format("woff2")', rule)
            rule = rule.replace("font-display:block", "font-display:swap")
        kept.append(rule.strip())
    missing = sorted(used - found)
    if missing:
        print(f"íconos usados sin regla en Font Awesome 6.7.2: {missing}", file=sys.stderr)
        return 1
    (OUT / "webfonts").mkdir(parents=True, exist_ok=True)
    unicodes = ",".join(f"U+{cp:04X}" for cp in sorted(set(codepoints.values())))
    files = {}
    for stem in FONTS:
        target = OUT / "webfonts" / f"{stem}-sub.woff2"
        subprocess.run(["pyftsubset", str(SOURCE / "webfonts" / f"{stem}.woff2"), f"--unicodes={unicodes}",
                        "--flavor=woff2", f"--output-file={target}"], check=True)
        files[target.relative_to(ROOT).as_posix()] = {
            "sha256": hashlib.sha256(target.read_bytes()).hexdigest(), "bytes": target.stat().st_size,
            "source_bytes": (SOURCE / "webfonts" / f"{stem}.woff2").stat().st_size}
    subset_css = banner + "\n/* Subconjunto generado por scripts/build_fontawesome_subset.py; no editar a mano. */\n" + "\n".join(kept) + "\n"
    (OUT / "fa-subset.css").write_text(subset_css, encoding="utf-8")
    css_rel = (OUT / "fa-subset.css").relative_to(ROOT).as_posix()
    manifest = {
        "schema": "fontawesome-subset-v1",
        "source": "Font Awesome Free 6.7.2 (cdnjs, css sha512 = integrity previo de head.html)",
        "license": "https://fontawesome.com/license/free (Icons: CC BY 4.0, Fonts: SIL OFL 1.1, Code: MIT)",
        "icons": {name: f"{cp:04x}" for name, cp in sorted(codepoints.items())},
        "files": {**files, css_rel: {"sha256": hashlib.sha256(subset_css.encode()).hexdigest(), "bytes": len(subset_css.encode())}},
    }
    (OUT / "subset-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    before = (SOURCE / "css" / "all.min.css").stat().st_size + sum(f["source_bytes"] for f in files.values())
    after = sum(f["bytes"] for f in manifest["files"].values())
    print(f"{len(codepoints)} íconos; {before} -> {after} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
