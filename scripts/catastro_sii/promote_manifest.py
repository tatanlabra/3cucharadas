#!/usr/bin/env python3
"""Promote validated local tile metadata into the small site manifest.

Promotion does not upload files.  It only makes a validated, versioned tile filename
available to the browser.  The preceding R2 upload and Range/CORS check are separate
operations, so a failed storage deployment cannot silently expose stale metadata.
"""

from __future__ import annotations

import argparse
import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def tile_entry(result: dict[str, Any]) -> dict[str, Any]:
    return {
        "available": bool(result["available"]),
        "url": result["url"],
        "source_layer": result["source_layer"],
        "minzoom": result["minzoom"],
        "maxzoom": result["maxzoom"],
    }


def atomic_write(path: Path, contents: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(contents)
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tiles-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tiles-base", required=True)
    parser.add_argument("--basemap-file", required=True)
    parser.add_argument("--basemap-style", required=True)
    parser.add_argument("--territories-output", type=Path, required=True)
    args = parser.parse_args()

    built = read(args.tiles_manifest)
    legal = built["legal_publication_status"]
    communes = built.get("results", {}).get("communes")
    pilot = built.get("results", {}).get("parcel_regions", {}).get("03")
    if not communes:
        raise RuntimeError("No se puede promover un manifest sin capa comunal validada")
    if pilot and pilot["available"] and legal != "AUTHORIZED_VECTOR":
        raise RuntimeError("Manifest intenta exponer predios sin autorización vectorial")
    territories_name = communes.get("territories_file")
    if not isinstance(territories_name, str) or not territories_name:
        raise RuntimeError("Manifest de tiles sin índice de bounding boxes comunales")
    territories_file = args.tiles_manifest.parent / territories_name
    if not territories_file.is_file():
        raise RuntimeError(f"Índice de bounding boxes ausente: {territories_file}")

    parcels: dict[str, Any] = {}
    if pilot:
        parcels["03"] = {
            **tile_entry(pilot),
            "pilot": True,
            "scope": "Caldera (03102) y Diego de Almagro (03202)",
            "communes": pilot.get("communes", []),
            "attribution": "Fuente predial: Servicio de Impuestos Internos. Cartografía referencial."
        }
    payload = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "legal_publication_status": legal,
        "tiles_base": args.tiles_base.rstrip("/"),
        "basemap": {
            "available": True,
            "url": args.basemap_file,
            "style_url": args.basemap_style,
            "attribution": "© OpenStreetMap contributors"
        },
        "communes": {
            **tile_entry(communes),
            "territories_url": "/assets/data/catastro_sii/territories.json",
            "excluded_communes": communes.get("excluded_communes", []),
        },
        "parcel_regions": parcels,
    }
    atomic_write(args.territories_output, territories_file.read_bytes())
    atomic_write(args.output, (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
