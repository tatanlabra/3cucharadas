#!/usr/bin/env python3
"""Render language-neutral social derivatives for the Nushell publication.

The master illustrations deliberately contain no prose or metrics. The post and
its distribution copy supply those claims in the reader's language, while these
assets communicate the bounded routing idea: one incoming text stream, a decision
point, and three possible outcomes. Keeping the two source masters in-repository
prevents a future render from restoring the superseded numeric-card artwork.
"""

from __future__ import annotations

from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
OG_DIR = ROOT / "assets" / "images" / "structured-shell"
TEASER_DIR = ROOT / "assets" / "images" / "teasers"
OG_MASTER = OG_DIR / "routing-og-master.webp"
TEASER_MASTER = OG_DIR / "routing-teaser-master.webp"

DERIVATIVES = (
    (OG_MASTER, (1200, 630), OG_DIR / "og-1200.webp", 90),
    (OG_MASTER, (1200, 630), OG_DIR / "og-1200-en.webp", 90),
    (TEASER_MASTER, (1280, 720), TEASER_DIR / "teaser-structured-shell.webp", 88),
    (TEASER_MASTER, (1280, 720), TEASER_DIR / "teaser-structured-shell-en.webp", 88),
    (TEASER_MASTER, (640, 360), TEASER_DIR / "teaser-structured-shell-640.webp", 85),
    (TEASER_MASTER, (640, 360), TEASER_DIR / "teaser-structured-shell-en-640.webp", 85),
)


def cover(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    """Resize proportionally and centre-crop, never distort the illustration."""
    width, height = size
    scale = max(width / image.width, height / image.height)
    resized = image.resize(
        (round(image.width * scale), round(image.height * scale)), Image.Resampling.LANCZOS
    )
    left = (resized.width - width) // 2
    top = (resized.height - height) // 2
    return resized.crop((left, top, left + width, top + height))


def render(source: Path, size: tuple[int, int], destination: Path, quality: int) -> None:
    if not source.is_file():
        raise FileNotFoundError(f"missing curated master: {source.relative_to(ROOT)}")
    with Image.open(source) as raw:
        image = cover(raw.convert("RGB"), size)
    destination.parent.mkdir(parents=True, exist_ok=True)
    image.save(destination, "WEBP", quality=quality, method=6)


def main() -> None:
    for source, size, destination, quality in DERIVATIVES:
        render(source, size, destination, quality)
        print(f"{destination.relative_to(ROOT)}  {size[0]}x{size[1]}")


if __name__ == "__main__":
    main()
