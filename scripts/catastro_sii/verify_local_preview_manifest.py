#!/usr/bin/env python3
"""Validate the ignored same-origin cartographic preview before local review.

The deploy artifact deliberately excludes ``assets/data/catastro_sii/local``.
When that overlay exists on a developer machine, however, every manifest
reference must resolve locally; otherwise MapLibre falls back to an empty style
and a broken preview can look like a cartographic design problem.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
from typing import Any


def read_json(path: Path, label: str) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"{label} inválido: {path}: {error}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"{label} debe ser un objeto JSON: {path}")
    return value


def safe_web_path(value: object, label: str) -> str:
    if not isinstance(value, str) or not value:
        raise RuntimeError(f"{label} ausente")
    if "://" in value or value.startswith("//") or ".." in Path(value).parts:
        raise RuntimeError(f"{label} no es una ruta local segura: {value}")
    return value


def require_file(path: Path, label: str) -> None:
    if not path.is_file():
        raise RuntimeError(f"{label} ausente: {path}")


def default_local_root() -> Path:
    configured = os.environ.get("CATASTRO_SII_LOCAL_ROOT")
    if configured:
        return Path(configured).expanduser()
    state_root = Path(os.environ.get("XDG_STATE_HOME", Path.home() / ".local" / "state"))
    return state_root / "3cucharadas" / "catastro_sii" / "local"


def validate(local_root: Path, manifest_path: Path) -> None:
    manifest = read_json(manifest_path, "Manifest local")
    if manifest.get("deployment_scope") != "localhost-cartographic-review":
        raise RuntimeError("El manifest local no declara deployment_scope=localhost-cartographic-review")

    tiles_base = safe_web_path(manifest.get("tiles_base"), "tiles_base")
    expected_prefix = "/assets/data/catastro_sii/local/"
    if not tiles_base.startswith(expected_prefix):
        raise RuntimeError(f"tiles_base debe permanecer bajo {expected_prefix}: {tiles_base}")
    relative_tiles = tiles_base.removeprefix(expected_prefix)
    tile_root = local_root / relative_tiles
    if not tile_root.is_dir():
        raise RuntimeError(f"Directorio de teselas local ausente: {tile_root}")

    basemap = manifest.get("basemap")
    if not isinstance(basemap, dict) or basemap.get("available") is not True:
        raise RuntimeError("El preview local requiere basemap disponible")
    basemap_name = safe_web_path(basemap.get("url"), "basemap.url")
    style_name = safe_web_path(basemap.get("style_url"), "basemap.style_url")
    basemap_path = tile_root / basemap_name
    style_path = tile_root / style_name
    require_file(basemap_path, "PMTiles base")
    require_file(style_path, "Estilo base")

    style = read_json(style_path, "Estilo base")
    source_url = style.get("sources", {}).get("protomaps", {}).get("url")
    if source_url != basemap_name:
        raise RuntimeError(
            f"El estilo base referencia {source_url!r}; se esperaba {basemap_name!r}"
        )
    glyphs = safe_web_path(style.get("glyphs"), "style.glyphs")
    if glyphs != "fonts/{fontstack}/{range}.pbf":
        raise RuntimeError(f"Ruta de fuentes inesperada en el estilo: {glyphs}")
    require_file(tile_root / "fonts" / "Noto Sans Regular" / "0-255.pbf", "Fuente Noto Sans")

    communes = manifest.get("communes")
    if not isinstance(communes, dict) or communes.get("available") is not True:
        raise RuntimeError("El preview local requiere capa comunal disponible")
    require_file(
        tile_root / safe_web_path(communes.get("url"), "communes.url"),
        "PMTiles comunal",
    )
    territories_url = safe_web_path(communes.get("territories_url"), "communes.territories_url")
    if territories_url.startswith(expected_prefix):
        territories_path = local_root / territories_url.removeprefix(expected_prefix)
    elif territories_url.startswith("/"):
        raise RuntimeError(f"Índice territorial fuera del overlay local: {territories_url}")
    else:
        territories_path = tile_root / territories_url
    require_file(territories_path, "Índice territorial")

    parcel_regions = manifest.get("parcel_regions")
    if not isinstance(parcel_regions, dict):
        raise RuntimeError("parcel_regions ausente")
    for region, entry in parcel_regions.items():
        if not isinstance(entry, dict) or entry.get("available") is not True:
            continue
        require_file(
            tile_root / safe_web_path(entry.get("url"), f"parcel_regions.{region}.url"),
            f"PMTiles predial región {region}",
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local-root", type=Path, default=default_local_root())
    parser.add_argument(
        "--manifest",
        type=Path,
        default=None,
    )
    args = parser.parse_args()
    local_root = args.local_root.expanduser().resolve()
    manifest_path = args.manifest or (local_root / "manifest.json")
    manifest_path = manifest_path.expanduser().resolve()
    if not manifest_path.exists():
        print(f"Preview local omitido: no existe {manifest_path}")
        return 0
    try:
        validate(local_root, manifest_path)
    except RuntimeError as error:
        print(f"Preview local inválido: {error}")
        return 1
    print(f"Preview local válido: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
