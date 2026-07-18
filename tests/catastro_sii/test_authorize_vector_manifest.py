from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "catastro_sii" / "authorize_vector_manifest.py"


def manifest() -> dict[str, object]:
    return {
        "schema_version": 1,
        "generated_at": "2026-07-18T21:29:32+00:00",
        "legal_publication_status": "PENDING",
        "build_scope": "local-predeployment-validation",
        "results": {
            "communes": {"available": True, "url": "chile_comunas_brechas_20260718.pmtiles"},
            "parcel_regions": {
                "03": {
                    "available": False,
                    "url": "predios_region_03_20260718T212932Z.pmtiles",
                    "source_layer": "predios",
                    "minzoom": 13,
                    "maxzoom": 18,
                    "feature_count": 10892,
                    "bytes": 22050380,
                    "source_sha256": "abc123",
                }
            },
        },
    }


class AuthorizeVectorManifestTests(unittest.TestCase):
    def call(self, source: Path, output: Path, *, confirmed: bool) -> subprocess.CompletedProcess[str]:
        command = [sys.executable, str(SCRIPT), "--tiles-manifest", str(source), "--output", str(output)]
        if confirmed:
            command.append("--confirm-public-vector")
        return subprocess.run(command, text=True, capture_output=True, check=False)

    def test_authorization_writes_a_new_metadata_only_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "tiles_manifest.json"
            contents = json.dumps(manifest(), ensure_ascii=False, indent=2).encode("utf-8")
            source.write_bytes(contents)
            output = directory / "authorized.json"

            result = self.call(source, output, confirmed=True)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(source.read_bytes(), contents)
            authorized = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(authorized["legal_publication_status"], "AUTHORIZED_VECTOR")
            self.assertEqual(authorized["build_scope"], "authorized-existing-artifact")
            self.assertTrue(authorized["results"]["parcel_regions"]["03"]["available"])
            audit = authorized["publication_authorization"]
            self.assertEqual(audit["source_manifest"], source.name)
            self.assertEqual(audit["source_manifest_sha256"], hashlib.sha256(contents).hexdigest())
            self.assertEqual(audit["pilot_asset"], "predios_region_03_20260718T212932Z.pmtiles")

    def test_confirmation_is_required_and_does_not_replace_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "tiles_manifest.json"
            source.write_text(json.dumps(manifest()), encoding="utf-8")
            output = directory / "authorized.json"
            output.write_text('{"previous": true}\n', encoding="utf-8")

            result = self.call(source, output, confirmed=False)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("--confirm-public-vector", result.stderr)
            self.assertEqual(output.read_text(encoding="utf-8"), '{"previous": true}\n')

    def test_rejects_a_manifest_without_audited_pilot_evidence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            invalid = manifest()
            invalid["results"]["parcel_regions"]["03"].pop("source_sha256")  # type: ignore[index]
            source = directory / "tiles_manifest.json"
            source.write_text(json.dumps(invalid), encoding="utf-8")
            output = directory / "authorized.json"

            result = self.call(source, output, confirmed=True)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source_sha256", result.stderr)
            self.assertFalse(output.exists())

    def test_rejects_an_output_outside_the_audited_run_directory(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "run" / "tiles_manifest.json"
            source.parent.mkdir()
            source.write_text(json.dumps(manifest()), encoding="utf-8")
            output = directory / "other" / "authorized.json"

            result = self.call(source, output, confirmed=True)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("junto al manifest auditado", result.stderr)
            self.assertFalse(output.exists())


if __name__ == "__main__":
    unittest.main()
