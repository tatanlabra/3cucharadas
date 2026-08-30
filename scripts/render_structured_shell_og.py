#!/usr/bin/env python3
"""Genera la imagen social y los teasers del post structured-shell-nushell.

Reproducible a proposito: las cifras del cuadro salen del benchmark medido
(penta-agent/reports/structured-shell-benchmark.md), no se escriben a mano en un editor
de imagenes. Si el benchmark cambia, se regenera la imagen corriendo este script.

Uso: python3 scripts/render_structured_shell_og.py
"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OG_DIR = ROOT / "assets" / "images" / "structured-shell"
TEASER_DIR = ROOT / "assets" / "images" / "teasers"

BG = "#121521"
PANEL = "#1b2032"
FG = "#e8ecf5"
DIM = "#8b97ad"
ACCENT = "#37e7ff"
WARN = "#ff4fd8"
LINE = "#2a3041"

MONO = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Regular.ttf"
MONO_BOLD = "/usr/share/fonts/TTF/JetBrainsMonoNerdFont-Bold.ttf"

# Los tres brazos del A/B de agente, con su resultado medido en 45 corridas.
LANES = [
    ("sin la skill", "21/25 acierto · 0 activaciones", DIM),
    ("con la skill afinada", "25/25 acierto · 14/15 en positivas", ACCENT),
    ("sobreactivación", "0 de 10 · no cuesta donde no toca", DIM),
    ("la tarea que decide", "1/5 sin skill  →  5/5 con skill", DIM),
]

# Cifra titular: el resultado del A/B, no el microbenchmark.
HEADLINE = ("0/15", "14/15", "activación, tras dos rondas de afinado")


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def render(width: int, height: int) -> Image.Image:
    img = Image.new("RGB", (width, height), BG)
    d = ImageDraw.Draw(img)
    s = width / 1200  # factor de escala respecto al diseno base

    f_title = font(MONO_BOLD, int(46 * s))
    f_sub = font(MONO, int(23 * s))
    f_lane = font(MONO_BOLD, int(24 * s))
    f_lane_sm = font(MONO, int(18 * s))
    f_big = font(MONO_BOLD, int(58 * s))
    f_small = font(MONO, int(19 * s))

    pad = int(64 * s)
    d.text((pad, int(52 * s)), "La escribí, la medí,", font=f_title, fill=FG)
    d.text((pad, int(108 * s)), "y no se activaba nunca", font=f_title, fill=FG)
    d.text((pad, int(178 * s)),
           "120 corridas después: qué cambió y qué cuesta",
           font=f_sub, fill=DIM)

    # Las cuatro vias
    top = int(232 * s)
    row_h = int(80 * s)
    lane_w = int(640 * s)
    for i, (name, detail, color) in enumerate(LANES):
        y = top + i * row_h
        active = color is ACCENT
        d.rounded_rectangle(
            [pad, y, pad + lane_w, y + int(66 * s)],
            radius=int(8 * s),
            fill=PANEL if active else BG,
            outline=color if active else LINE,
            width=int(2 * s) if active else int(1 * s),
        )
        d.text((pad + int(18 * s), y + int(10 * s)), name, font=f_lane, fill=color if active else FG)
        d.text((pad + int(18 * s), y + int(40 * s)), detail, font=f_lane_sm, fill=DIM)

    # Panel de la cifra titular
    px = pad + lane_w + int(40 * s)
    pw = width - px - pad
    py = top
    ph = row_h * len(LANES) - int(14 * s)
    d.rounded_rectangle([px, py, px + pw, py + ph], radius=int(10 * s),
                        fill=PANEL, outline=LINE, width=int(1 * s))
    cx = px + int(24 * s)
    d.text((cx, py + int(26 * s)), "veces que se activó", font=f_small, fill=DIM)
    d.text((cx, py + int(62 * s)), HEADLINE[0], font=f_big, fill=WARN)
    d.text((cx, py + int(136 * s)), "↓", font=f_big, fill=DIM)
    d.text((cx, py + int(206 * s)), HEADLINE[1], font=f_big, fill=ACCENT)
    d.text((cx, py + int(276 * s)), HEADLINE[2], font=font(MONO, int(15 * s)), fill=DIM)

    footer = "Claude Code headless · Sonnet · nushell 0.115.1 · 3cucharadas.cl"
    d.text((pad, height - int(46 * s)), footer, font=f_small, fill=DIM)
    return img


def main() -> None:
    OG_DIR.mkdir(parents=True, exist_ok=True)
    TEASER_DIR.mkdir(parents=True, exist_ok=True)

    og = render(1200, 630)
    og_path = OG_DIR / "og-1200.webp"
    og.save(og_path, "WEBP", quality=90, method=6)

    teaser = render(1280, 720)
    teaser.save(TEASER_DIR / "teaser-structured-shell.webp", "WEBP", quality=88, method=6)
    teaser.resize((640, 360), Image.LANCZOS).save(
        TEASER_DIR / "teaser-structured-shell-640.webp", "WEBP", quality=85, method=6
    )

    for p in (og_path,
              TEASER_DIR / "teaser-structured-shell.webp",
              TEASER_DIR / "teaser-structured-shell-640.webp"):
        print(f"{p.relative_to(ROOT)}  {Image.open(p).size}  {p.stat().st_size // 1024} KB")


if __name__ == "__main__":
    main()
