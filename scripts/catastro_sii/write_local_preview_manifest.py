#!/usr/bin/env python3
"""Create an ignored localhost-only manifest from an audited build run.

This is a cartographic review aid.  It never uploads data, never changes the
versioned production manifest and is only read by the browser on localhost when
the loopback preview is opened. A run id can still pin a specific audited run.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from pathlib import Path
from typing import Any


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def atomic_write(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            json.dump(payload, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def tile_entry(result: dict[str, Any]) -> dict[str, Any]:
    entry = {
        "available": True,
        "url": result["url"],
        "source_layer": result["source_layer"],
        "minzoom": result["minzoom"],
        "maxzoom": result["maxzoom"],
    }
    if isinstance(result.get("commune_focus_bounds"), dict):
        entry["commune_focus_bounds"] = result["commune_focus_bounds"]
    return entry


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tiles-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--current-output", type=Path)
    parser.add_argument("--tiles-base", required=True)
    parser.add_argument("--territories-output", type=Path, required=True)
    parser.add_argument("--basemap-file", required=True)
    parser.add_argument("--basemap-style", required=True)
    parser.add_argument("--basemap-fonts-dir", type=Path, required=True)
    args = parser.parse_args()

    built = read(args.tiles_manifest)
    communes = built.get("results", {}).get("communes")
    pilot = built.get("results", {}).get("parcel_regions", {}).get("03")
    if not communes or not pilot:
        raise RuntimeError("El preview local requiere capa comunal y piloto Atacama validados")
    territories_name = communes.get("territories_file")
    if not isinstance(territories_name, str) or not territories_name:
        raise RuntimeError("El manifest del build no declara el índice territorial")
    territories = args.tiles_manifest.parent / territories_name
    if not territories.is_file():
        raise FileNotFoundError(f"Índice territorial ausente: {territories}")
    basemap = args.tiles_manifest.parent / args.basemap_file
    style = args.tiles_manifest.parent / args.basemap_style
    latin_font = args.basemap_fonts_dir / "Noto Sans Regular" / "0-255.pbf"
    for asset in (basemap, style, latin_font):
        if not asset.is_file():
            raise FileNotFoundError(f"Activo de base cartográfica ausente: {asset}")

    # This status activates only a localhost-only manifest generated under an
    # ignored path. It is deliberately not a declaration of an R2 deployment.
    payload = {
        "schema_version": 1,
        "deployment_scope": "localhost-cartographic-review",
        "source_legal_publication_status": built.get("legal_publication_status"),
        "legal_publication_status": "AUTHORIZED_VECTOR",
        "tiles_base": args.tiles_base.rstrip("/"),
        "basemap": {
            "available": True,
            "url": args.basemap_file,
            "style_url": args.basemap_style,
            "attribution": "© OpenStreetMap contributors",
        },
        "communes": {
            **tile_entry(communes),
            "territories_url": "/assets/data/catastro_sii/local/territories.json",
            "excluded_communes": communes.get("excluded_communes", []),
        },
        "parcel_regions": {
            "03": {
                **tile_entry(pilot),
                "pilot": True,
                "scope": "Caldera (03102) y Diego de Almagro (03202)",
                "communes": pilot.get("communes", []),
                "attribution": "Fuente predial: Servicio de Impuestos Internos. Cartografía referencial.",
            }
        },
    }
    atomic_write(args.output, payload)
    if args.current_output:
        atomic_write(args.current_output, payload)
    args.territories_output.parent.mkdir(parents=True, exist_ok=True)
    args.territories_output.write_bytes(territories.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
