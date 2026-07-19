from __future__ import annotations

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "catastro_sii" / "verify_public_tiles.sh"
MANIFEST_URL = "https://site.example.test/assets/data/catastro_sii/manifest.json"
TERRITORIES_URL = "https://site.example.test/assets/data/catastro_sii/territories.json"


def manifest(
    *,
    status: str = "AUTHORIZED_VECTOR",
    communes_url: str = "chile_comunas_brechas_20260718T212932Z.pmtiles",
    basemap_available: bool = True,
) -> dict[str, object]:
    return {
        "schema_version": 1,
        "generated_at": "2026-07-18T21:29:32+00:00",
        "legal_publication_status": status,
        "tiles_base": "https://tiles.example.test/catastro-sii",
        "basemap": {
            "available": basemap_available,
            "url": "basemap_chile_20260718T212932Z.pmtiles",
            "style_url": "basemap_chile_20260718T212932Z.style.json",
            "attribution": "© OpenStreetMap contributors",
        },
        "communes": {
            "available": True,
            "url": communes_url,
            "source_layer": "comunas",
            "minzoom": 4,
            "maxzoom": 12,
            "territories_url": TERRITORIES_URL,
            "excluded_communes": ["12202"],
        },
        "parcel_regions": {
            "03": {
                "available": True,
                "pilot": True,
                "url": "predios_region_03_20260718T212932Z.pmtiles",
                "source_layer": "predios",
                "minzoom": 13,
                "maxzoom": 18,
                "communes": ["03102", "03202"],
            }
        },
    }


def territories(count: int = 345) -> dict[str, object]:
    # The verifier checks the release invariant (345 declared DPA communes),
    # not geography; tiny deterministic bounds keep the network-free fixture small.
    return {
        "schema_version": 1,
        "communes": {
            f"{index:05d}": {"bounds": [-70.0, -30.0, -69.0, -29.0]}
            for index in range(1, count + 1)
        },
    }


class VerifyPublicTilesTests(unittest.TestCase):
    def write_mock_curl(self, directory: Path) -> Path:
        binary = directory / "bin"
        binary.mkdir()
        curl = binary / "curl"
        curl.write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "output=''\nheaders=''\nurl=''\n"
            "while [[ $# -gt 0 ]]; do\n"
            "  case \"$1\" in\n"
            "    --output|--dump-header)\n"
            "      if [[ \"$1\" == --output ]]; then output=\"$2\"; else headers=\"$2\"; fi\n"
            "      shift 2 ;;\n"
            "    --header|--range) shift 2 ;;\n"
            "    *) url=\"$1\"; shift ;;\n"
            "  esac\n"
            "done\n"
            "printf '%s\\n' \"$url\" >> \"$MOCK_CURL_LOG\"\n"
            "case \"$url\" in\n"
            "  *manifest.json) cp \"$MOCK_MANIFEST\" \"$output\" ;;\n"
            "  *territories.json) cp \"$MOCK_TERRITORIES\" \"$output\" ;;\n"
            "  *.style.json)\n"
            "    cp \"$MOCK_STYLE\" \"$output\"\n"
            "    if [[ -n \"$headers\" ]]; then\n"
            "      if [[ \"${MOCK_CORS_MODE:-ok}\" == missing ]]; then\n"
            "        printf '%s\\n' 'HTTP/1.1 200 OK' > \"$headers\"\n"
            "      else\n"
            "        printf '%s\\n' 'HTTP/1.1 200 OK' 'Access-Control-Allow-Origin: https://3cucharadas.cl' > \"$headers\"\n"
            "      fi\n"
            "    fi ;;\n"
            "  *.pbf)\n"
            "    if [[ \"${MOCK_CORS_MODE:-ok}\" == missing ]]; then\n"
            "      printf '%s\\n' 'HTTP/1.1 200 OK' > \"$headers\"\n"
            "    else\n"
            "      printf '%s\\n' 'HTTP/1.1 200 OK' 'Access-Control-Allow-Origin: https://3cucharadas.cl' > \"$headers\"\n"
            "    fi ;;\n"
            "  *.pmtiles)\n"
            "    if [[ \"${MOCK_CORS_MODE:-ok}\" == missing ]]; then\n"
            "      printf '%s\\n' 'HTTP/1.1 206 Partial Content' 'Accept-Ranges: bytes' 'Content-Range: bytes 0-126/999' > \"$headers\"\n"
            "    else\n"
            "      printf '%s\\n' 'HTTP/1.1 206 Partial Content' 'Accept-Ranges: bytes' 'Content-Range: bytes 0-126/999' 'Access-Control-Allow-Origin: https://3cucharadas.cl' 'Access-Control-Expose-Headers: Accept-Ranges, Content-Range' > \"$headers\"\n"
            "    fi ;;\n"
            "  *) printf 'unexpected curl URL: %s\\n' \"$url\" >&2; exit 88 ;;\n"
            "esac\n",
            encoding="utf-8",
        )
        os.chmod(curl, 0o755)
        return curl

    def run_verifier(
        self,
        directory: Path,
        public: dict[str, object],
        public_territories: dict[str, object],
        *,
        cors_mode: str = "ok",
    ) -> tuple[subprocess.CompletedProcess[str], Path, Path, Path]:
        local_manifest = directory / "manifest.local.json"
        local_territories = directory / "territories.local.json"
        remote_manifest = directory / "manifest.remote.json"
        remote_territories = directory / "territories.remote.json"
        style = directory / "basemap.style.json"
        local_manifest.write_text(json.dumps(public, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        remote_manifest.write_text(json.dumps(public, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        local_territories.write_text(json.dumps(public_territories, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        remote_territories.write_text(json.dumps(public_territories, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        style.write_text(
            json.dumps(
                {
                    "version": 8,
                    "glyphs": "fonts/{fontstack}/{range}.pbf",
                    "sources": {
                        "protomaps": {
                            "type": "vector",
                            "url": "basemap_chile_20260718T212932Z.pmtiles",
                        }
                    },
                }
            ),
            encoding="utf-8",
        )
        curl = self.write_mock_curl(directory)
        curl_log = directory / "curl.log"
        environment = {
            **os.environ,
            "MOCK_MANIFEST": str(remote_manifest),
            "MOCK_TERRITORIES": str(remote_territories),
            "MOCK_STYLE": str(style),
            "MOCK_CURL_LOG": str(curl_log),
            "MOCK_CORS_MODE": cors_mode,
        }
        result = subprocess.run(
            [
                "bash", str(SCRIPT),
                "--manifest-url", MANIFEST_URL,
                "--local-manifest", str(local_manifest),
                "--local-territories", str(local_territories),
                "--tiles-base", "https://tiles.example.test/catastro-sii",
                "--curl-bin", str(curl),
            ],
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )
        return result, local_manifest, local_territories, curl_log

    def test_passes_for_matching_authorized_release_with_range_and_cors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            expected_manifest = manifest()
            expected_territories = territories()
            result, local_manifest, local_territories, curl_log = self.run_verifier(
                directory, expected_manifest, expected_territories
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("PASS manifest público, 345 comunas", result.stdout)
            self.assertEqual(json.loads(local_manifest.read_text(encoding="utf-8")), expected_manifest)
            self.assertEqual(json.loads(local_territories.read_text(encoding="utf-8")), expected_territories)
            calls = curl_log.read_text(encoding="utf-8")
            self.assertIn("basemap_chile_20260718T212932Z.pmtiles", calls)
            self.assertIn("chile_comunas_brechas_20260718T212932Z.pmtiles", calls)
            self.assertIn("predios_region_03_20260718T212932Z.pmtiles", calls)

    def test_rejects_pending_manifest(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, *_ = self.run_verifier(Path(temporary), manifest(status="PENDING"), territories())

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("PENDING", result.stderr)

    def test_rejects_unversioned_pmtiles_url(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, *_ = self.run_verifier(
                Path(temporary), manifest(communes_url="chile_comunas_brechas_latest.pmtiles"), territories()
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("versionado", result.stderr)

    def test_rejects_missing_cors_headers(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, *_ = self.run_verifier(Path(temporary), manifest(), territories(), cors_mode="missing")

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("CORS", result.stderr)

    def test_rejects_a_release_without_the_self_hosted_basemap(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, *_ = self.run_verifier(
                Path(temporary), manifest(basemap_available=False), territories()
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("basemap autoalojado", result.stderr)

    def test_rejects_territory_index_without_345_communes(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            result, *_ = self.run_verifier(Path(temporary), manifest(), territories(344))

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("345 comunas", result.stderr)


if __name__ == "__main__":
    unittest.main()
