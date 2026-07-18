from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "catastro_sii" / "extract_pmtiles_bbox.py"
SPEC = importlib.util.spec_from_file_location("extract_pmtiles_bbox", SCRIPT)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class TileBoundsTests(unittest.TestCase):
    def test_tile_bounds_at_world_origin(self) -> None:
        west, south, east, north = MODULE.tile_bounds(0, 0, 0)
        self.assertEqual((west, east), (-180.0, 180.0))
        self.assertLess(south, -85)
        self.assertGreater(north, 85)

    def test_intersection_is_inclusive_at_the_tile_edge(self) -> None:
        self.assertTrue(MODULE.tile_intersects_bbox(2, 1, 1, (-91, 0, -89, 2)))
        self.assertFalse(MODULE.tile_intersects_bbox(2, 3, 3, (-91, 0, -89, 2)))


try:
    import pmtiles  # type: ignore[import-not-found]  # noqa: F401
except ModuleNotFoundError:
    PMTILES_AVAILABLE = False
else:
    PMTILES_AVAILABLE = True


@unittest.skipUnless(PMTILES_AVAILABLE, "PMTiles se valida en python_base de stata01")
class ExtractArchiveTests(unittest.TestCase):
    def make_source(self, path: Path) -> None:
        from pmtiles.tile import Compression, TileType, zxy_to_tileid
        from pmtiles.writer import write

        header = {
            "root_offset": 0,
            "root_length": 0,
            "metadata_offset": 0,
            "metadata_length": 0,
            "tile_data_offset": 0,
            "tile_data_length": 0,
            "clustered": True,
            "internal_compression": Compression.GZIP,
            "tile_compression": Compression.GZIP,
            "tile_type": TileType.MVT,
            "min_zoom": 0,
            "max_zoom": 2,
        }
        with write(path) as writer:
            writer.write_tile(zxy_to_tileid(0, 0, 0), b"world")
            writer.write_tile(zxy_to_tileid(2, 1, 1), b"north-west")
            writer.write_tile(zxy_to_tileid(2, 3, 3), b"south-east")
            writer.finalize(header, {"name": "fixture", "vector_layers": []})

    def test_extract_copies_selected_payloads_and_keeps_source_hash(self) -> None:
        from pmtiles.reader import MmapSource, Reader

        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "source.pmtiles"
            output = directory / "output.pmtiles"
            self.make_source(source)
            source_hash = MODULE.sha256(source)

            report = MODULE.extract(source, output, (-100, 1, -1, 70), maxzoom=2)

            self.assertEqual(MODULE.sha256(source), source_hash)
            self.assertEqual(report["tiles_seen"], 3)
            self.assertEqual(report["tiles_copied"], 2)
            self.assertEqual(report["output_bytes"], output.stat().st_size)
            with output.open("rb") as handle:
                reader = Reader(MmapSource(handle))
                self.assertEqual(reader.get(0, 0, 0), b"world")
                self.assertEqual(reader.get(2, 1, 1), b"north-west")
                self.assertIsNone(reader.get(2, 3, 3))
                self.assertEqual(json.loads(json.dumps(reader.metadata()))["name"], "fixture")


if __name__ == "__main__":
    unittest.main()
