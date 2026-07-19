from __future__ import annotations

import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "catastro_sii" / "upload_r2.sh"


class UploadR2Tests(unittest.TestCase):
    def prepare_mocks(self, directory: Path) -> tuple[Path, Path]:
        binary = directory / "bin"
        binary.mkdir()
        log = directory / "rclone.log"
        (binary / "rclone").write_text(
            "#!/usr/bin/env bash\nprintf '%s\\n' \"$*\" >> \"$RCLONE_LOG\"\n",
            encoding="utf-8",
        )
        (binary / "curl").write_text(
            "#!/usr/bin/env bash\nset -euo pipefail\nwhile [[ $# -gt 0 ]]; do\n"
            "  case \"$1\" in\n    --dump-header) headers=\"$2\"; shift 2 ;;\n    *) shift ;;\n  esac\ndone\n"
            "printf '%s\\n' 'HTTP/1.1 206 Partial Content' 'Accept-Ranges: bytes' "
            "'Content-Range: bytes 0-126/999' 'Access-Control-Allow-Origin: https://3cucharadas.cl' "
            "'Access-Control-Expose-Headers: Accept-Ranges, Content-Range' > \"$headers\"\n",
            encoding="utf-8",
        )
        os.chmod(binary / "rclone", 0o755)
        os.chmod(binary / "curl", 0o755)
        return binary, log

    def environment(self, binary: Path, log: Path, legal: str) -> dict[str, str]:
        return {
            **os.environ,
            "PATH": f"{binary}:{os.environ['PATH']}",
            "RCLONE_LOG": str(log),
            "LEGAL_PUBLICATION_STATUS": legal,
            "R2_REMOTE": "r2",
            "R2_BUCKET": "tiles",
            "R2_PREFIX": "catastro-sii",
            "PUBLIC_TILES_BASE": "https://tiles.example.test/catastro-sii",
        }

    def test_pending_can_upload_communal_asset_after_range_cors_pass(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            binary, log = self.prepare_mocks(directory)
            asset = directory / "chile_comunas_brechas_20260718.pmtiles"
            asset.write_bytes(b"fixture")

            result = subprocess.run(
                ["bash", str(SCRIPT), str(asset)],
                text=True,
                capture_output=True,
                env=self.environment(binary, log, "PENDING"),
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("copyto", log.read_text(encoding="utf-8"))

    def test_pending_rejects_predial_asset_before_upload(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            binary, log = self.prepare_mocks(directory)
            asset = directory / "predios_region_03_20260718.pmtiles"
            asset.write_bytes(b"fixture")

            result = subprocess.run(
                ["bash", str(SCRIPT), str(asset)],
                text=True,
                capture_output=True,
                env=self.environment(binary, log, "PENDING"),
                check=False,
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("AUTHORIZED_VECTOR", result.stderr)
            self.assertFalse(log.exists())


if __name__ == "__main__":
    unittest.main()
