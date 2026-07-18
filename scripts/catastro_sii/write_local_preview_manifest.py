#!/usr/bin/env python3
"""Create an ignored localhost-only manifest from an audited private build run.

This is a cartographic review aid.  It never uploads data, never changes the
versioned production manifest and is only read by the browser on localhost when
``?catastroPreview=local&run=<run-id>`` is present.
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
    return {
        "available": True,
        "url": result["url"],
        "source_layer": result["source_layer"],
        "minzoom": result["minzoom"],
        "maxzoom": result["maxzoom"],
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tiles-manifest", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--tiles-base", required=True)
    parser.add_argument("--territories-output", type=Path, required=True)
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

    # This status activates only a localhost-only manifest generated under an
    # ignored path. It is deliberately not a declaration of public authorization.
    payload = {
        "schema_version": 1,
        "deployment_scope": "localhost-cartographic-review",
        "source_legal_publication_status": built.get("legal_publication_status"),
        "legal_publication_status": "AUTHORIZED_VECTOR",
        "tiles_base": args.tiles_base.rstrip("/"),
        "basemap": {
            "available": False,
            "url": "basemap_chile_PENDING.pmtiles",
            "style_url": "basemap_chile_PENDING.style.json",
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
    args.territories_output.parent.mkdir(parents=True, exist_ok=True)
    args.territories_output.write_bytes(territories.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
