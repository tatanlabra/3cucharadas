from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "catastro_sii" / "verify_local_preview_manifest.py"


class LocalPreviewVerificationTests(unittest.TestCase):
    def fixture(self, root: Path) -> Path:
        run = root / "assets" / "data" / "catastro_sii" / "local" / "20260718T212932Z"
        run.mkdir(parents=True)
        for name in ("base.pmtiles", "communes.pmtiles", "parcels.pmtiles"):
            (run / name).write_bytes(b"fixture")
        font = run / "fonts" / "Noto Sans Regular" / "0-255.pbf"
        font.parent.mkdir(parents=True)
        font.write_bytes(b"font")
        style = {
            "version": 8,
            "glyphs": "fonts/{fontstack}/{range}.pbf",
            "sources": {"protomaps": {"type": "vector", "url": "base.pmtiles"}},
            "layers": [],
        }
        (run / "style.json").write_text(json.dumps(style), encoding="utf-8")
        local = root / "assets" / "data" / "catastro_sii" / "local"
        (local / "territories.json").write_text('{"communes": {}}\n', encoding="utf-8")
        manifest = {
            "deployment_scope": "localhost-cartographic-review",
            "tiles_base": "/assets/data/catastro_sii/local/20260718T212932Z",
            "basemap": {
                "available": True,
                "url": "base.pmtiles",
                "style_url": "style.json",
            },
            "communes": {
                "available": True,
                "url": "communes.pmtiles",
                "territories_url": "/assets/data/catastro_sii/local/territories.json",
            },
            "parcel_regions": {
                "03": {"available": True, "url": "parcels.pmtiles"}
            },
        }
        manifest_path = local / "manifest.json"
        manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
        return manifest_path

    def run_verifier(self, root: Path, manifest: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--repo-root",
                str(root),
                "--manifest",
                str(manifest),
            ],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_accepts_a_complete_same_origin_overlay(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = self.fixture(root)
            result = self.run_verifier(root, manifest)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("Preview local válido", result.stdout)

    def test_rejects_a_missing_style_instead_of_allowing_a_silent_fallback(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            manifest = self.fixture(root)
            payload = json.loads(manifest.read_text(encoding="utf-8"))
            payload["basemap"]["style_url"] = "missing.style.json"
            manifest.write_text(json.dumps(payload), encoding="utf-8")
            result = self.run_verifier(root, manifest)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Estilo base ausente", result.stdout)


if __name__ == "__main__":
    unittest.main()
