#!/usr/bin/env python3
"""Copy a bounded PMTiles derivative without modifying the source archive or tiles.

The maintained ``python_base`` Conda environment has the PMTiles Python library,
but not the separate Go ``pmtiles extract`` binary.  This adapter copies the exact
tile payloads selected by a geographic bounding box, so it keeps the source
archive read-only and avoids a second package manager or a hand-installed binary.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import tempfile
from pathlib import Path
from typing import Any


Bounds = tuple[float, float, float, float]


def parse_bbox(raw: str) -> Bounds:
    try:
        west, south, east, north = (float(value) for value in raw.split(","))
    except ValueError as error:
        raise argparse.ArgumentTypeError("bbox debe ser oeste,sur,este,norte") from error
    if not -180 <= west < east <= 180 or not -85.051129 <= south < north <= 85.051129:
        raise argparse.ArgumentTypeError("bbox fuera de los límites Web Mercator o con orden inválido")
    return west, south, east, north


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tile_bounds(z: int, x: int, y: int) -> Bounds:
    """Return WGS84 bounds for a Web Mercator XYZ tile."""

    tiles = 1 << z
    west = x / tiles * 360.0 - 180.0
    east = (x + 1) / tiles * 360.0 - 180.0
    north = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / tiles))))
    south = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * (y + 1) / tiles))))
    return west, south, east, north


def tile_intersects_bbox(z: int, x: int, y: int, bounds: Bounds) -> bool:
    west, south, east, north = tile_bounds(z, x, y)
    requested_west, requested_south, requested_east, requested_north = bounds
    return not (
        east < requested_west
        or west > requested_east
        or north < requested_south
        or south > requested_north
    )


def archive_metadata(metadata: dict[str, Any], bounds: Bounds, maxzoom: int | None) -> dict[str, Any]:
    west, south, east, north = bounds
    output = dict(metadata)
    output["bounds"] = f"{west},{south},{east},{north}"
    if maxzoom is not None:
        output["maxzoom"] = maxzoom
    output["center"] = f"{(west + east) / 2},{(south + north) / 2},{maxzoom if maxzoom is not None else 4}"
    return output


def extract(input_path: Path, output_path: Path, bounds: Bounds, maxzoom: int | None) -> dict[str, Any]:
    """Write an atomic derivative with byte-identical copied tile payloads."""

    if input_path.resolve() == output_path.resolve():
        raise ValueError("La salida debe ser distinta del archivo fuente")
    if not input_path.is_file():
        raise FileNotFoundError(f"PMTiles fuente ausente: {input_path}")
    if maxzoom is not None and not 0 <= maxzoom <= 30:
        raise ValueError("maxzoom debe estar entre 0 y 30")

    from pmtiles.reader import MmapSource, Reader, all_tiles
    from pmtiles.tile import zxy_to_tileid
    from pmtiles.writer import write

    source_before = sha256(input_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{output_path.name}.", dir=output_path.parent)
    os.close(descriptor)
    temporary = Path(temporary_name)
    tiles_seen = 0
    tiles_copied = 0
    try:
        with input_path.open("rb") as input_handle:
            reader = Reader(MmapSource(input_handle))
            header = dict(reader.header())
            metadata = archive_metadata(reader.metadata(), bounds, maxzoom)
            with write(temporary) as writer:
                for (z, x, y), payload in all_tiles(MmapSource(input_handle)):
                    tiles_seen += 1
                    if (maxzoom is not None and z > maxzoom) or not tile_intersects_bbox(z, x, y, bounds):
                        continue
                    writer.write_tile(zxy_to_tileid(z, x, y), payload)
                    tiles_copied += 1
                if not tiles_copied:
                    raise RuntimeError("El bbox no seleccionó teselas; no se crea una base vacía")
                west, south, east, north = bounds
                header.update(
                    min_lon_e7=round(west * 10_000_000),
                    min_lat_e7=round(south * 10_000_000),
                    max_lon_e7=round(east * 10_000_000),
                    max_lat_e7=round(north * 10_000_000),
                    center_lon_e7=round((west + east) / 2 * 10_000_000),
                    center_lat_e7=round((south + north) / 2 * 10_000_000),
                )
                if maxzoom is not None:
                    header["max_zoom"] = min(header["max_zoom"], maxzoom)
                    header["center_zoom"] = min(maxzoom, max(header["min_zoom"], 4))
                writer.finalize(header, metadata)
        if sha256(input_path) != source_before:
            raise RuntimeError("La fuente PMTiles cambió durante la extracción; se aborta")
        os.replace(temporary, output_path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise

    return {
        "input": input_path.name,
        "input_sha256": source_before,
        "input_bytes": input_path.stat().st_size,
        "output": output_path.name,
        "output_sha256": sha256(output_path),
        "output_bytes": output_path.stat().st_size,
        "bounds": list(bounds),
        "maxzoom": maxzoom,
        "tiles_seen": tiles_seen,
        "tiles_copied": tiles_copied,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--bbox", type=parse_bbox, required=True)
    parser.add_argument("--maxzoom", type=int)
    parser.add_argument("--report", type=Path, required=True)
    args = parser.parse_args()
    report = extract(args.input, args.output, args.bbox, args.maxzoom)
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
