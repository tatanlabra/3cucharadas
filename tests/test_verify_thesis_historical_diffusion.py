"""Red/green custody probes for the archived III/IV diffusion packages."""

import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import importlib.util


REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts/verify_thesis_historical_diffusion.py"
ARCHIVE = REPO / "difusion/historico/scientific-reset-20261108"
spec = importlib.util.spec_from_file_location("historical_diffusion", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CurrentPackageTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.slug = module.SLUGS[0]
        self.package = self.root / "difusion/paquetes" / self.slug
        self.package.mkdir(parents=True)
        (self.package / "linkedin.md").write_text("Current descriptive campaign")
        sources = {}
        for name in module.SOURCES:
            if name.startswith("_posts/") and self.slug in name:
                path = self.root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("Current source " + name)
                sources[name] = module.sha(path.read_bytes())
        self.data = {"schema_version": 1, "archived_source_commit": module.SOURCE_COMMIT,
                     "packages": {self.slug: {"sources": sources, "artifacts": {
                         "linkedin.md": module.sha((self.package / "linkedin.md").read_bytes())}}}}
        self.receipt = self.root / module.CURRENT_RECEIPT
        self.receipt.parent.mkdir(parents=True)
        self.receipt.write_text(json.dumps(self.data))
        self.historical = {"old.md": {"source_sha256": module.sha(b"Old claim"), "archive_sha256": module.sha(b"Old claim")}}

    def check(self):
        module.check_current_package(self.root, self.slug, self.package, self.historical)

    def test_current_bound_package_is_admitted(self):
        self.check()

    def test_missing_receipt_is_rejected(self):
        self.receipt.unlink()
        with self.assertRaisesRegex(ValueError, "sin revisión vigente"):
            self.check()

    def test_changed_piece_is_rejected(self):
        (self.package / "linkedin.md").write_text("Unreviewed change")
        with self.assertRaisesRegex(ValueError, "inventario vigente"):
            self.check()

    def test_changed_source_is_rejected(self):
        source = next(iter(self.data["packages"][self.slug]["sources"]))
        (self.root / source).write_text("New source")
        with self.assertRaisesRegex(ValueError, "fuente vigente modificada"):
            self.check()

    def test_restored_old_piece_rejected_even_when_inventoried(self):
        (self.package / "linkedin.md").write_bytes(b"Old claim")
        self.data["packages"][self.slug]["artifacts"]["linkedin.md"] = module.sha(b"Old claim")
        self.receipt.write_text(json.dumps(self.data))
        with self.assertRaisesRegex(ValueError, "pieza histórica restaurada"):
            self.check()

    def test_empty_package_is_rejected(self):
        (self.package / "linkedin.md").unlink()
        self.data["packages"][self.slug]["artifacts"] = {}
        self.receipt.write_text(json.dumps(self.data))
        with self.assertRaisesRegex(ValueError, "inventario vigente vacío"):
            self.check()


class HistoricalDiffusionTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex-historical-diffusion-")
        self.addCleanup(self.temp.cleanup)
        self.archive = Path(self.temp.name) / "archive"
        shutil.copytree(ARCHIVE, self.archive)

    def run_gate(self):
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(REPO), "--archive-root", str(self.archive)],
            text=True,
            capture_output=True,
            check=False,
        )

    def test_valid_archive_is_green(self):
        result = self.run_gate()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("42 archivos, 8 fuentes", result.stdout)

    def test_changed_piece_is_red(self):
        piece = self.archive / "costos-cierre-escolar-trayectorias/README.md"
        piece.write_bytes(piece.read_bytes() + b"\nmodified fixture\n")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("contenido histórico alterado", result.stderr)

    def test_missing_piece_is_red(self):
        (self.archive / "cierre-escolar-educacion-superior-causal-ml/README.md").unlink()
        result = self.run_gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("archivo faltante o extra", result.stderr)

    def test_changed_derivative_is_red(self):
        derivative = self.archive / "linkedin/costos-cierre-escolar-trayectorias-carrusel.html"
        derivative.write_bytes(derivative.read_bytes() + b"\nmodified fixture\n")
        result = self.run_gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("carrusel histórico alterado", result.stderr)

    def test_missing_derivative_is_red(self):
        (self.archive / "linkedin/cierre-escolar-educacion-superior-causal-ml-en-carrusel.json").unlink()
        result = self.run_gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("carrusel faltante", result.stderr)

    def test_empty_manifest_is_red(self):
        receipt = self.archive / "receipt.json"
        data = json.loads(receipt.read_text())
        data["packages"] = {}
        receipt.write_text(json.dumps(data))
        result = self.run_gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("inventario de paquetes incompleto", result.stderr)

    def test_tampered_receipt_hash_is_red(self):
        receipt = self.archive / "receipt.json"
        data = json.loads(receipt.read_text())
        data["packages"]["costos-cierre-escolar-trayectorias"]["README.md"]["archive_sha256"] = "0" * 64
        receipt.write_text(json.dumps(data))
        result = self.run_gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("hash archivo inválido", result.stderr)

    def test_wrong_source_commit_is_red(self):
        receipt = self.archive / "receipt.json"
        data = json.loads(receipt.read_text())
        data["source_commit"] = "0" * 40
        receipt.write_text(json.dumps(data))
        result = self.run_gate()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("commit fuente incorrecto", result.stderr)

    def test_unresolvable_source_commit_is_red(self):
        empty_repo = Path(self.temp.name) / "empty-repo"
        empty_repo.mkdir()
        subprocess.run(["git", "init", "-q", str(empty_repo)], check=True)
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "--repo", str(empty_repo), "--archive-root", str(self.archive)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("cat-file", result.stderr)


if __name__ == "__main__":
    unittest.main()
