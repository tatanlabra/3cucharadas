from __future__ import annotations

import hashlib
import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "catastro_sii" / "preflight_r2.sh"


class PreflightR2Tests(unittest.TestCase):
    version = "20260718T212932Z"
    public_base = "https://tiles.example.test/catastro-sii"

    def prepare_rclone(self, directory: Path) -> tuple[Path, Path]:
        binary = directory / "bin"
        binary.mkdir()
        log = directory / "rclone.log"
        (binary / "rclone").write_text(
            "#!/usr/bin/env bash\n"
            "set -euo pipefail\n"
            "printf '%s\\n' \"$*\" >> \"$RCLONE_LOG\"\n"
            "if [[ \"${1:-}\" == listremotes ]]; then\n"
            "  printf '%s\\n' \"${RCLONE_REMOTES:-}\"\n"
            "elif [[ \"${1:-}\" == config && \"${2:-}\" == file ]]; then\n"
            "  printf '%s\\n' 'Configuration file is stored at:' \"$RCLONE_CONFIG_PATH\"\n"
            "fi\n",
            encoding="utf-8",
        )
        os.chmod(binary / "rclone", 0o755)
        return binary, log

    def environment(self, binary: Path, log: Path, remotes: str = "r2:") -> dict[str, str]:
        config = log.parent / "rclone.conf"
        config.write_text(
            "[r2]\n"
            "type = s3\n"
            "provider = Cloudflare\n"
            "access_key_id = fixture-not-a-secret\n"
            "secret_access_key = fixture-not-a-secret\n",
            encoding="utf-8",
        )
        return {
            **os.environ,
            "PATH": f"{binary}:{os.environ['PATH']}",
            "RCLONE_LOG": str(log),
            "RCLONE_REMOTES": remotes,
            "RCLONE_CONFIG_PATH": str(config),
            "R2_REMOTE": "r2",
            "R2_BUCKET": "private-bucket-value",
            "R2_PREFIX": "private-prefix-value",
            "PUBLIC_TILES_BASE": self.public_base,
        }

    def write_cors(self, path: Path, *, valid: bool) -> None:
        policy = [
            {
                "AllowedOrigins": ["https://3cucharadas.cl", "https://www.3cucharadas.cl"],
                "AllowedMethods": ["GET", "HEAD"],
                "AllowedHeaders": ["Range", "If-None-Match"],
                "ExposeHeaders": ["Accept-Ranges", "Content-Length", "Content-Range", "ETag"],
                "MaxAgeSeconds": 7200,
            }
        ]
        if not valid:
            policy[0]["ExposeHeaders"] = ["ETag"]
        path.write_text(json.dumps(policy), encoding="utf-8")

    def write_valid_run(self, directory: Path) -> Path:
        run = directory / self.version
        run.mkdir()
        commune = f"chile_comunas_brechas_{self.version}.pmtiles"
        pilot = f"predios_region_03_{self.version}.pmtiles"
        territories = f"territories_{self.version}.json"
        source_name = f"tiles_manifest_{self.version}.json"
        source = {
            "legal_publication_status": "PENDING",
            "tiles_base": self.public_base,
            "results": {
                "communes": {
                    "available": True,
                    "url": commune,
                    "territories_file": territories,
                },
                "parcel_regions": {
                    "03": {
                        "available": False,
                        "pilot": True,
                        "url": pilot,
                        "source_layer": "predios",
                        "minzoom": 13,
                        "maxzoom": 18,
                        "feature_count": 2,
                        "bytes": 10,
                        "source_sha256": {"fixture": "abc"},
                    }
                },
            },
        }
        source_path = run / source_name
        source_path.write_text(json.dumps(source), encoding="utf-8")
        authorized = json.loads(json.dumps(source))
        authorized["legal_publication_status"] = "AUTHORIZED_VECTOR"
        authorized["build_scope"] = "authorized-existing-artifact"
        authorized["results"]["parcel_regions"]["03"]["available"] = True
        authorized["publication_authorization"] = {
            "kind": "project-owner-public-vector-confirmation",
            "source_manifest": source_name,
            "source_manifest_sha256": hashlib.sha256(source_path.read_bytes()).hexdigest(),
            "pilot_asset": pilot,
        }
        (run / f"tiles_manifest_{self.version}_authorized.json").write_text(
            json.dumps(authorized), encoding="utf-8"
        )
        for filename in (
            commune,
            pilot,
            f"basemap_chile_{self.version}.pmtiles",
            f"basemap_chile_{self.version}.style.json",
            territories,
        ):
            (run / filename).write_bytes(b"fixture")
        font = run / "fonts" / "Noto Sans Regular" / "0-255.pbf"
        font.parent.mkdir(parents=True)
        font.write_bytes(b"fixture")
        return run

    def run_preflight(
        self, run: Path, environment: dict[str, str], cors: Path | None = None
    ) -> subprocess.CompletedProcess[str]:
        command = ["bash", str(SCRIPT), "--run-dir", str(run)]
        if cors is not None:
            command.extend(["--cors-file", str(cors)])
        return subprocess.run(
            command,
            text=True,
            capture_output=True,
            env=environment,
            check=False,
        )

    def test_valid_run_checks_only_local_rclone_configuration_without_secrets(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            binary, log = self.prepare_rclone(directory)
            result = self.run_preflight(self.write_valid_run(directory), self.environment(binary, log))

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(log.read_text(encoding="utf-8").splitlines(), ["listremotes", "config file"])
            self.assertNotIn("private-bucket-value", result.stdout + result.stderr)
            self.assertNotIn("private-prefix-value", result.stdout + result.stderr)
            self.assertIn("no se realizaron uploads ni solicitudes de red", result.stdout)

    def test_accumulates_environment_remote_cors_and_asset_errors(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            binary, log = self.prepare_rclone(directory)
            cors = directory / "r2-cors.json"
            self.write_cors(cors, valid=False)
            run = self.write_valid_run(directory)
            (run / f"basemap_chile_{self.version}.pmtiles").unlink()
            (run / "unexpected.pmtiles").write_bytes(b"fixture")
            environment = self.environment(binary, log, remotes="different:")
            environment.pop("R2_BUCKET")

            result = self.run_preflight(run, environment, cors)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Falta variable de entorno R2_BUCKET", result.stderr)
            self.assertIn("R2_REMOTE no existe", result.stderr)
            self.assertIn("CORS:", result.stderr)
            self.assertIn("Activo versionado requerido ausente", result.stderr)
            self.assertIn("activo con nombre no permitido", result.stderr)
            self.assertEqual(log.read_text(encoding="utf-8").splitlines(), ["listremotes"])

    def test_requires_the_authorized_manifest_and_its_provenance(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            binary, log = self.prepare_rclone(directory)
            cors = directory / "r2-cors.json"
            self.write_cors(cors, valid=True)
            run = self.write_valid_run(directory)
            authorized = run / f"tiles_manifest_{self.version}_authorized.json"
            document = json.loads(authorized.read_text(encoding="utf-8"))
            document["publication_authorization"]["source_manifest_sha256"] = "invalid"
            authorized.write_text(json.dumps(document), encoding="utf-8")

            result = self.run_preflight(run, self.environment(binary, log), cors)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("source_manifest_sha256 no permitido", result.stderr)
            self.assertEqual(log.read_text(encoding="utf-8").splitlines(), ["listremotes", "config file"])

    def test_rejects_an_existing_remote_that_is_not_cloudflare_r2(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            binary, log = self.prepare_rclone(directory)
            environment = self.environment(binary, log)
            config = Path(environment["RCLONE_CONFIG_PATH"])
            config.write_text("[r2]\ntype = drive\n", encoding="utf-8")

            result = self.run_preflight(self.write_valid_run(directory), environment)

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("S3 con proveedor Cloudflare", result.stderr)
            self.assertEqual(log.read_text(encoding="utf-8").splitlines(), ["listremotes", "config file"])


if __name__ == "__main__":
    unittest.main()
