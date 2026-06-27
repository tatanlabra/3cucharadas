#!/usr/bin/env python3
"""Render codera-style El Salvador hero backgrounds for 3 Cucharadas."""

from __future__ import annotations

import json
import math
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parents[1]
OSM_CACHE = (
    ROOT.parent
    / "catastros_sii"
    / "data"
    / "interim"
    / "osm_cache"
    / "el_salvador_overpass.json"
)
OUT_DIR = ROOT / "assets" / "images" / "home"

BG = "#080d10"
URBAN = "#10252b"
ROAD_MAJOR = "#f7fbff"
ROAD_LOCAL = "#dfe8ef"
ROAD_MINOR = "#b7c7d3"
ACCENT = "#5dd6ff"

# Editorial crop around El Salvador's urban grid. The Overpass cache includes
# long access roads; fitting to all of them makes the city unreadably small.
FOCUS_BBOX = (-69.6380, -26.2705, -69.5955, -26.2375)


@dataclass(frozen=True)
class CanvasSpec:
    filename: str
    width: int
    height: int
    map_rect: tuple[float, float, float, float]
    line_scale: float
    label: bool = False


SPECS = [
    CanvasSpec(
        filename="el-salvador-codera-hero-2400x720.webp",
        width=2400,
        height=720,
        map_rect=(0.42, 0.05, 0.985, 0.95),
        line_scale=1.00,
        label=True,
    ),
    CanvasSpec(
        filename="el-salvador-codera-hero-1600x524.webp",
        width=1600,
        height=524,
        map_rect=(0.42, 0.05, 0.985, 0.95),
        line_scale=0.74,
        label=True,
    ),
    CanvasSpec(
        filename="el-salvador-codera-hero-mobile-1200x720.webp",
        width=1200,
        height=720,
        map_rect=(0.20, 0.08, 1.08, 0.94),
        line_scale=1.08,
        label=False,
    ),
]

MAJOR_HIGHWAYS = {
    "motorway",
    "trunk",
    "primary",
    "secondary",
    "tertiary",
    "motorway_link",
    "trunk_link",
    "primary_link",
    "secondary_link",
    "tertiary_link",
}
LOCAL_HIGHWAYS = {"residential", "living_street", "unclassified"}


def mercator(lon: float, lat: float) -> tuple[float, float]:
    lat = max(min(lat, 85.05112878), -85.05112878)
    x = lon
    y = math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))
    return x, y


def load_roads() -> list[dict[str, object]]:
    if not OSM_CACHE.exists():
        raise FileNotFoundError(f"Missing OSM cache: {OSM_CACHE}")
    payload = json.loads(OSM_CACHE.read_text(encoding="utf-8"))
    roads: list[dict[str, object]] = []
    nodes: dict[int, tuple[float, float]] = {}

    for element in payload.get("elements", []):
        if element.get("type") == "node" and {"id", "lon", "lat"} <= set(element):
            nodes[int(element["id"])] = (float(element["lon"]), float(element["lat"]))

    for element in payload.get("elements", []):
        if element.get("type") != "way":
            continue
        tags = element.get("tags") or {}
        highway = tags.get("highway")
        if not highway:
            continue
        if "geometry" in element:
            coords = [(float(pt["lon"]), float(pt["lat"])) for pt in element["geometry"]]
        else:
            coords = [nodes[nid] for nid in element.get("nodes", []) if nid in nodes]
        if len(coords) < 2:
            continue
        roads.append({"highway": str(highway), "coords": coords})
    if not roads:
        raise RuntimeError(f"No highway geometry found in {OSM_CACHE}")
    return roads


def projected_focus_bounds() -> tuple[float, float, float, float]:
    lon_min, lat_min, lon_max, lat_max = FOCUS_BBOX
    x0, y0 = mercator(lon_min, lat_min)
    x1, y1 = mercator(lon_max, lat_max)
    pad_x = abs(x1 - x0) * 0.06
    pad_y = abs(y1 - y0) * 0.06
    return min(x0, x1) - pad_x, min(y0, y1) - pad_y, max(x0, x1) + pad_x, max(y0, y1) + pad_y


def transformer(
    src_bounds: tuple[float, float, float, float],
    dst_rect: tuple[int, int, int, int],
) -> callable:
    sx0, sy0, sx1, sy1 = src_bounds
    dx0, dy0, dx1, dy1 = dst_rect
    scale = min((dx1 - dx0) / (sx1 - sx0), (dy1 - dy0) / (sy1 - sy0))
    cx_src = (sx0 + sx1) / 2
    cy_src = (sy0 + sy1) / 2
    cx_dst = (dx0 + dx1) / 2
    cy_dst = (dy0 + dy1) / 2

    def convert(lon: float, lat: float) -> tuple[float, float]:
        x, y = mercator(lon, lat)
        px = cx_dst + (x - cx_src) * scale
        py = cy_dst - (y - cy_src) * scale
        return px, py

    return convert


def draw_gradient(img: Image.Image) -> None:
    overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    width, height = img.size
    for x in range(width):
        t = x / max(1, width - 1)
        if t < 0.43:
            alpha = 230
        elif t < 0.70:
            alpha = int(230 * (1 - (t - 0.43) / 0.27) + 42 * ((t - 0.43) / 0.27))
        else:
            alpha = 42
        draw.line([(x, 0), (x, height)], fill=(2, 7, 9, alpha))
    img.alpha_composite(overlay)


def add_texture(img: Image.Image) -> None:
    noise = Image.effect_noise(img.size, 18).convert("L")
    tint = Image.new("RGBA", img.size, (93, 214, 255, 0))
    tint.putalpha(noise.point(lambda p: max(0, min(14, int((p - 126) / 8)))))
    img.alpha_composite(tint)


def draw_roads(img: Image.Image, roads: list[dict[str, object]], spec: CanvasSpec) -> None:
    width, height = img.size
    rect = (
        int(spec.map_rect[0] * width),
        int(spec.map_rect[1] * height),
        int(spec.map_rect[2] * width),
        int(spec.map_rect[3] * height),
    )
    convert = transformer(projected_focus_bounds(), rect)

    glow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)
    wash = Image.new("RGBA", img.size, (0, 0, 0, 0))
    wash_draw = ImageDraw.Draw(wash)
    road_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
    road_draw = ImageDraw.Draw(road_layer)

    for road in roads:
        highway = str(road["highway"])
        pts = [convert(lon, lat) for lon, lat in road["coords"]]  # type: ignore[index]
        if len(pts) < 2:
            continue
        if highway in MAJOR_HIGHWAYS:
            glow_w = int(20 * spec.line_scale)
            wash_w = int(10 * spec.line_scale)
            road_w = max(2, int(3.8 * spec.line_scale))
            color = ROAD_MAJOR
            alpha = 252
        elif highway in LOCAL_HIGHWAYS:
            glow_w = int(13 * spec.line_scale)
            wash_w = int(7 * spec.line_scale)
            road_w = max(1, int(2.2 * spec.line_scale))
            color = ROAD_LOCAL
            alpha = 235
        else:
            glow_w = int(8 * spec.line_scale)
            wash_w = int(5 * spec.line_scale)
            road_w = max(1, int(1.35 * spec.line_scale))
            color = ROAD_MINOR
            alpha = 205

        glow_draw.line(pts, fill=(93, 214, 255, 70), width=max(1, glow_w), joint="curve")
        wash_draw.line(pts, fill=(16, 37, 43, 165), width=max(1, wash_w), joint="curve")
        road_draw.line(pts, fill=color + f"{alpha:02x}", width=road_w, joint="curve")

    img.alpha_composite(glow.filter(ImageFilter.GaussianBlur(radius=max(4, int(7 * spec.line_scale)))))
    img.alpha_composite(wash.filter(ImageFilter.GaussianBlur(radius=max(2, int(2 * spec.line_scale)))))
    img.alpha_composite(road_layer)

    if spec.label:
        label = Image.new("RGBA", img.size, (0, 0, 0, 0))
        label_draw = ImageDraw.Draw(label)
        label_draw.text(
            (int(width * 0.765), int(height * 0.82)),
            "EL SALVADOR",
            fill=ACCENT + "b8",
            anchor="mm",
            spacing=4,
        )
        img.alpha_composite(label)


def render(spec: CanvasSpec, roads: list[dict[str, object]]) -> Path:
    img = Image.new("RGBA", (spec.width, spec.height), BG)
    add_texture(img)
    draw_roads(img, roads, spec)
    draw_gradient(img)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    out = OUT_DIR / spec.filename
    img.convert("RGB").save(out, format="WEBP", quality=86, method=6)
    return out


def main() -> None:
    roads = load_roads()
    for spec in SPECS:
        out = render(spec, roads)
        print(f"rendered {out}")


if __name__ == "__main__":
    main()
