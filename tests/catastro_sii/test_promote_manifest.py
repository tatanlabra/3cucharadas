from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "catastro_sii" / "promote_manifest.py"
AUTHORIZE_SCRIPT = ROOT / "scripts" / "catastro_sii" / "authorize_vector_manifest.py"
DEFAULT_VIEWS = ROOT / "scripts" / "catastro_sii" / "commune_default_views.json"


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
                    "feature_count": 10892,
                    "bytes": 22050380,
                    "source_sha256": "fixture-source-sha256",
                }
            },
        },
    }


class PromoteManifestTests(unittest.TestCase):
    def run_promotion(
        self,
        directory: Path,
        manifest: Path,
        output: Path,
        territories: Path,
        commune_views: Path | None = None,
    ) -> subprocess.CompletedProcess[str]:
        arguments = [
            sys.executable, str(SCRIPT),
            "--tiles-manifest", str(manifest),
            "--output", str(output),
            "--tiles-base", "https://tiles.example.test/catastro-sii",
            "--basemap-file", "basemap_chile_20260718.pmtiles",
            "--basemap-style", "basemap_chile_20260718.style.json",
            "--territories-output", str(territories),
        ]
        if commune_views is not None:
            arguments += ["--commune-views", str(commune_views)]
        return subprocess.run(
            arguments,
            cwd=directory,
            text=True,
            capture_output=True,
            check=False,
        )

    def authorize(self, manifest: Path, output: Path) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable, str(AUTHORIZE_SCRIPT),
                "--tiles-manifest", str(manifest),
                "--output", str(output),
                "--confirm-public-vector",
            ],
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

    def test_authorized_existing_artifact_promotes_the_same_vector_pilot(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            source = directory / "tiles_manifest.json"
            source.write_text(json.dumps(tiles_manifest()), encoding="utf-8")
            (directory / "territories.json").write_text('{"communes": {}}\n', encoding="utf-8")
            authorized = directory / "tiles_manifest_authorized.json"

            authorization = self.authorize(source, authorized)
            self.assertEqual(authorization.returncode, 0, authorization.stderr)
            site_manifest = directory / "site" / "manifest.json"
            site_territories = directory / "site" / "territories.json"

            promotion = self.run_promotion(directory, authorized, site_manifest, site_territories)

            self.assertEqual(promotion.returncode, 0, promotion.stderr)
            promoted = json.loads(site_manifest.read_text(encoding="utf-8"))
            self.assertEqual(promoted["legal_publication_status"], "AUTHORIZED_VECTOR")
            self.assertTrue(promoted["parcel_regions"]["03"]["available"])
            self.assertEqual(
                promoted["parcel_regions"]["03"]["url"],
                "predios_region_03_20260718.pmtiles",
            )

    def test_promotion_preserves_commune_default_views(self) -> None:
        """Una promoción no puede degradar la cámara inicial de las comunas piloto.

        El campo se editó a mano una vez y una re-ejecución del runbook lo borraba en
        silencio, dejando ambos pilotos abriendo en una vista regional inútil.
        """
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            manifest = directory / "tiles_manifest.json"
            built = tiles_manifest()
            built["results"]["parcel_regions"]["03"]["communes"] = ["03102", "03202"]
            manifest.write_text(json.dumps(built), encoding="utf-8")
            (directory / "territories.json").write_text('{"communes": {}}\n', encoding="utf-8")
            views = directory / "views.json"
            views.write_text(
                json.dumps({"03": {"03102": {"center": [-70.8267, -27.0674], "zoom": 15.4}}}),
                encoding="utf-8",
            )
            output = directory / "site" / "manifest.json"

            result = self.run_promotion(
                directory, manifest, output, directory / "site" / "territories.json", views
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            promoted = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                promoted["parcel_regions"]["03"]["commune_default_views"],
                {"03102": {"center": [-70.8267, -27.0674], "zoom": 15.4}},
            )

    def test_promotion_drops_views_for_unauthorized_communes(self) -> None:
        """Una cámara de configuración no puede filtrar una comuna fuera del piloto."""
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            manifest = directory / "tiles_manifest.json"
            built = tiles_manifest()
            built["results"]["parcel_regions"]["03"]["communes"] = ["03102"]
            manifest.write_text(json.dumps(built), encoding="utf-8")
            (directory / "territories.json").write_text('{"communes": {}}\n', encoding="utf-8")
            views = directory / "views.json"
            views.write_text(
                json.dumps({
                    "03": {
                        "03102": {"center": [-70.8267, -27.0674], "zoom": 15.4},
                        "03101": {"center": [-70.3314, -27.3665], "zoom": 15.0},
                    }
                }),
                encoding="utf-8",
            )
            output = directory / "site" / "manifest.json"

            result = self.run_promotion(
                directory, manifest, output, directory / "site" / "territories.json", views
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            promoted = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(
                list(promoted["parcel_regions"]["03"]["commune_default_views"]), ["03102"]
            )

    def test_versioned_views_cover_every_pilot_commune(self) -> None:
        """La configuración versionada debe cubrir el piloto vigente de Atacama."""
        self.assertTrue(DEFAULT_VIEWS.is_file(), f"Falta la configuración de cámaras: {DEFAULT_VIEWS}")
        configured = json.loads(DEFAULT_VIEWS.read_text(encoding="utf-8"))
        for commune in ("03102", "03202"):
            view = configured.get("03", {}).get(commune)
            self.assertIsInstance(view, dict, f"Sin cámara configurada para {commune}")
            self.assertEqual(len(view["center"]), 2)
            self.assertIsInstance(view["zoom"], (int, float))


if __name__ == "__main__":
    unittest.main()
