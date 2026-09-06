import contextlib
import importlib.util
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"


def _load_module(name: str, filename: str):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS_DIR / filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


publication = _load_module("notify_telegram_publication_under_test", "notify_telegram_publication.py")
local_commit = _load_module("notify_telegram_commit_under_test", "notify_telegram_commit.py")


class PublicationNotifierTests(unittest.TestCase):
    def test_accepts_only_canonical_https_publication_urls(self):
        self.assertEqual(
            publication._validate_publication_url("https://3cucharadas.cl/articulo/"),
            "https://3cucharadas.cl/articulo/",
        )
        for invalid_url in (
            "http://3cucharadas.cl/articulo/",
            "https://example.test/articulo/",
            "https://3cucharadas.cl:444/articulo/",
            "https://3cucharadas.cl",
        ):
            with self.assertRaises(publication.VerificationError):
                publication._validate_publication_url(invalid_url)

    def test_rejects_redirect_to_noncanonical_host(self):
        handler = publication._CanonicalPublicationRedirectHandler()

        with self.assertRaisesRegex(publication.VerificationError, "HTTPS de 3cucharadas.cl"):
            handler.redirect_request(None, None, 302, "Found", {}, "https://example.test/phishing")

    def test_remote_gate_fails_when_github_has_another_commit(self):
        expected = "a" * 40
        with mock.patch.object(
            publication.subprocess,
            "check_output",
            side_effect=[f"{expected}\trefs/heads/main\n", f"{'b' * 40}\trefs/heads/main\n"],
        ):
            with self.assertRaisesRegex(publication.VerificationError, "GitHub"):
                publication._verify_remote_ref(Path("/repo"), "main", expected)

    def test_pipeline_gate_rejects_pending_pipeline(self):
        with (
            mock.patch.object(publication, "_origin_gitlab_project", return_value="owner/project"),
            mock.patch.object(
                publication,
                "_get_json",
                return_value=[{"id": 42, "sha": "a" * 40, "status": "running"}],
            ),
        ):
            with self.assertRaisesRegex(publication.VerificationError, "aún no registra"):
                publication._verify_gitlab_pipeline(Path("/repo"), "main", "a" * 40)

    def test_public_page_gate_requires_expected_text(self):
        class Response:
            def __enter__(self):
                return self

            def __exit__(self, *_args):
                return False

            def geturl(self):
                return "https://3cucharadas.cl/articulo/"

            def read(self, _limit):
                return "Contenido distinto".encode()

        opener = mock.Mock()
        opener.open.return_value = Response()
        with mock.patch.object(publication.urllib.request, "build_opener", return_value=opener):
            with self.assertRaisesRegex(publication.VerificationError, "texto esperado"):
                publication._verify_public_page("https://3cucharadas.cl/articulo/", "Título esperado")

    def test_message_is_compact_and_html_escapes_subject(self):
        message = publication._build_message(
            publication.ReleaseEvidence(
                commit="a" * 40,
                publication_url="https://3cucharadas.cl/articulo/",
                pipeline_id=42,
            ),
            "Título <verificado>",
        )
        self.assertIn("3cucharadas publicada", message)
        self.assertIn("Título &lt;verificado&gt;", message)
        self.assertIn("<code>aaaaaaaaaaaa</code>", message)
        self.assertIn("https://3cucharadas.cl/articulo/", message)
        self.assertIn("build · remoto · CI · página", message)

    def test_dry_run_never_sends_telegram(self):
        evidence = publication.ReleaseEvidence("b" * 40, "https://3cucharadas.cl/articulo/", 7)
        with (
            mock.patch.object(publication, "_resolve_repo_root", return_value=Path("/repo")),
            mock.patch.object(publication, "verify_release", return_value=evidence) as verify_release,
            mock.patch.object(publication, "_send_message") as send_message,
            contextlib.redirect_stdout(io.StringIO()) as stdout,
        ):
            result = publication.main(
                [
                    "--publication-url", "https://3cucharadas.cl/articulo/",
                    "--expect-text", "Artículo",
                    "--dry-run",
                ]
            )

        self.assertEqual(result, 0)
        self.assertEqual(stdout.getvalue().strip(), "publication-dry-run-ok")
        verify_release.assert_called_once()
        send_message.assert_not_called()

    def test_failed_gate_never_sends_telegram(self):
        with (
            mock.patch.object(publication, "_resolve_repo_root", return_value=Path("/repo")),
            mock.patch.object(
                publication,
                "verify_release",
                side_effect=publication.VerificationError("CI pendiente"),
            ),
            mock.patch.object(publication, "_send_message") as send_message,
            contextlib.redirect_stderr(io.StringIO()) as stderr,
        ):
            result = publication.main(
                ["--publication-url", "https://3cucharadas.cl/articulo/", "--expect-text", "Artículo"]
            )

        self.assertEqual(result, 1)
        self.assertIn("publication-not-verified: CI pendiente", stderr.getvalue())
        send_message.assert_not_called()

    def test_legacy_local_commit_entry_point_is_silent(self):
        with contextlib.redirect_stdout(io.StringIO()) as stdout:
            result = local_commit.main(["--dry-run"])

        self.assertEqual(result, 0)
        self.assertEqual(stdout.getvalue().strip(), "telegram-suppressed-local-commit")

    def test_hook_installer_is_idempotent(self):
        with tempfile.TemporaryDirectory(prefix="hooks-fixture-") as temporary:
            root = Path(temporary)
            hooks_source = root / "scripts" / "git-hooks"
            hooks_source.mkdir(parents=True)
            shutil.copy2(SCRIPTS_DIR / "install_git_hooks.sh", root / "scripts" / "install_git_hooks.sh")
            shutil.copy2(SCRIPTS_DIR / "git-hooks" / "post-commit", hooks_source / "post-commit")
            shutil.copy2(
                SCRIPTS_DIR / "git-hooks" / "post-commit-difusion",
                hooks_source / "post-commit-difusion",
            )
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            installer = root / "scripts" / "install_git_hooks.sh"

            subprocess.run(["bash", str(installer)], cwd=root, check=True, capture_output=True, text=True)
            second = subprocess.run(
                ["bash", str(installer)], cwd=root, check=True, capture_output=True, text=True
            )

            self.assertIn("already installed", second.stdout)
            self.assertEqual([], list((root / ".git" / "hooks").glob("post-commit.backup-*")))


if __name__ == "__main__":
    unittest.main()
