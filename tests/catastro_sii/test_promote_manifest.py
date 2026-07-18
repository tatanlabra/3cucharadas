from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "catastro_sii" / "promote_manifest.py"


def tiles_manifest(territories_file: str = "territories.json") -> dict[str, object]:
    return {
        "legal_publication_status": "PENDING",
        "results": {
            "communes": {
                "available": True,
                "url": "chile_comunas_brechas_20260718.pmtiles",
                "source_layer": "comunas",
                "minzoom": 4,
                "maxzoom": 12,
                "territories_file": territories_file,
                "excluded_communes": ["12202"],
            },
            "parcel_regions": {
                "03": {
                    "available": False,
                    "url": "predios_region_03_20260718.pmtiles",
                    "source_layer": "predios",
                    "minzoom": 13,
                    "maxzoom": 18,
                }
            },
        },
    }


class PromoteManifestTests(unittest.TestCase):
    def run_promotion(self, directory: Path, manifest: Path, output: Path, territories: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable, str(SCRIPT),
                "--tiles-manifest", str(manifest),
                "--output", str(output),
                "--tiles-base", "https://tiles.example.test/catastro-sii",
                "--basemap-file", "basemap_chile_20260718.pmtiles",
                "--basemap-style", "basemap_chile_20260718.style.json",
                "--territories-output", str(territories),
            ],
            cwd=directory,
            text=True,
            capture_output=True,
            check=False,
        )

    def test_promotes_private_pilot_without_exposing_predios(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            manifest = directory / "tiles_manifest.json"
            manifest.write_text(json.dumps(tiles_manifest()), encoding="utf-8")
            source_territories = directory / "territories.json"
            source_territories.write_text('{"communes": {}}\n', encoding="utf-8")
            output = directory / "site" / "manifest.json"
            territories = directory / "site" / "territories.json"

            result = self.run_promotion(directory, manifest, output, territories)

            self.assertEqual(result.returncode, 0, result.stderr)
            promoted = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(promoted["legal_publication_status"], "PENDING")
            self.assertEqual(promoted["communes"]["excluded_communes"], ["12202"])
            self.assertFalse(promoted["parcel_regions"]["03"]["available"])
            self.assertEqual(territories.read_text(encoding="utf-8"), source_territories.read_text(encoding="utf-8"))

    def test_missing_territories_does_not_replace_existing_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            manifest = directory / "tiles_manifest.json"
            manifest.write_text(json.dumps(tiles_manifest("missing.json")), encoding="utf-8")
            output = directory / "site" / "manifest.json"
            output.parent.mkdir()
            output.write_text('{"previous": true}\n', encoding="utf-8")
            territories = directory / "site" / "territories.json"

            result = self.run_promotion(directory, manifest, output, territories)

            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(output.read_text(encoding="utf-8"), '{"previous": true}\n')
            self.assertFalse(territories.exists())


if __name__ == "__main__":
    unittest.main()
