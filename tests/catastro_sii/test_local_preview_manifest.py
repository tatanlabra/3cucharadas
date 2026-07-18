from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "catastro_sii" / "write_local_preview_manifest.py"


def build_manifest() -> dict[str, object]:
    return {
        "legal_publication_status": "PENDING",
        "results": {
            "communes": {
                "available": True,
                "url": "chile_comunas_brechas_20260718T194751Z.pmtiles",
                "source_layer": "comunas",
                "minzoom": 4,
                "maxzoom": 12,
                "territories_file": "territories_20260718T194751Z.json",
                "excluded_communes": ["12202"],
            },
            "parcel_regions": {
                "03": {
                    "available": False,
                    "url": "predios_region_03_20260718T194751Z.pmtiles",
                    "source_layer": "predios",
                    "minzoom": 13,
                    "maxzoom": 18,
                    "communes": ["03102", "03202"],
                }
            },
        },
    }


class LocalPreviewManifestTests(unittest.TestCase):
    def test_generates_localhost_review_manifest_without_changing_source_gate(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "tiles_manifest.json"
            source.write_text(json.dumps(build_manifest()), encoding="utf-8")
            territories = directory / "territories_20260718T194751Z.json"
            territories.write_text('{"communes": {}}\n', encoding="utf-8")
            output = directory / "local" / "manifest.json"
            copied_territories = directory / "local" / "territories.json"

            result = subprocess.run(
                [
                    sys.executable, str(SCRIPT),
                    "--tiles-manifest", str(source),
                    "--output", str(output),
                    "--tiles-base", "/assets/data/catastro_sii/local/20260718T194751Z",
                    "--territories-output", str(copied_territories),
                ],
                text=True,
                capture_output=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(source.read_text(encoding="utf-8"))["legal_publication_status"], "PENDING")
            preview = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(preview["deployment_scope"], "localhost-cartographic-review")
            self.assertEqual(preview["source_legal_publication_status"], "PENDING")
            self.assertEqual(preview["legal_publication_status"], "AUTHORIZED_VECTOR")
            self.assertTrue(preview["parcel_regions"]["03"]["available"])
            self.assertEqual(copied_territories.read_text(encoding="utf-8"), territories.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
