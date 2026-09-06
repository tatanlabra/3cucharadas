#!/usr/bin/env python3
"""Notify Telegram only after a 3cucharadas release is verifiably public."""

from __future__ import annotations

import argparse
import html
import io
import json
import os
import subprocess
import sys
import tarfile
import tempfile
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path


ALLOWED_PUBLICATION_HOSTS = {"3cucharadas.cl", "www.3cucharadas.cl"}
HTTP_TIMEOUT_SECONDS = 20
MAX_PUBLIC_PAGE_BYTES = 2_000_000


class VerificationError(RuntimeError):
    """A publication condition could not be proven."""


class _CanonicalPublicationRedirectHandler(urllib.request.HTTPRedirectHandler):
    """Do not follow a publication-page redirect outside the canonical hosts."""

    def redirect_request(self, request, fp, code, msg, headers, new_url):
        _validate_publication_url(new_url)
        return super().redirect_request(request, fp, code, msg, headers, new_url)


@dataclass(frozen=True)
class ReleaseEvidence:
    commit: str
    publication_url: str
    pipeline_id: int | str


def _run_git(repo_root: Path, *args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=repo_root,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError) as exc:
        raise VerificationError("no se pudo consultar git") from exc


def _resolve_repo_root(path: Path) -> Path:
    return Path(_run_git(path, "rev-parse", "--show-toplevel"))


def _resolve_commit(repo_root: Path, revision: str) -> str:
    return _run_git(repo_root, "rev-parse", "--verify", f"{revision}^{{commit}}")


def _validate_publication_url(value: str) -> str:
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_PUBLICATION_HOSTS:
        raise VerificationError("la URL pública debe ser HTTPS de 3cucharadas.cl")
    try:
        port = parsed.port
    except ValueError as exc:
        raise VerificationError("la URL pública no tiene una forma permitida") from exc
    if parsed.username or parsed.password or port or not parsed.path:
        raise VerificationError("la URL pública no tiene una forma permitida")
    return value


def _safe_extract(archive: tarfile.TarFile, destination: Path) -> None:
    destination_resolved = destination.resolve()
    for member in archive.getmembers():
        member_path = (destination / member.name).resolve()
        if not member_path.is_relative_to(destination_resolved):
            raise VerificationError("el archivo del commit contiene una ruta no segura")
        if not (member.isfile() or member.isdir()):
            raise VerificationError("el archivo del commit contiene enlaces no permitidos")
    for member in archive.getmembers():
        archive.extract(member, destination)


def _verify_local_gates(repo_root: Path, commit: str) -> None:
    try:
        archive_bytes = subprocess.check_output(
            ["git", "archive", "--format=tar", commit],
            cwd=repo_root,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as exc:
        raise VerificationError("no se pudo aislar el commit para sus gates locales") from exc

    with tempfile.TemporaryDirectory(prefix="3cucharadas-release-") as temporary:
        source = Path(temporary)
        try:
            with tarfile.open(fileobj=io.BytesIO(archive_bytes), mode="r:") as archive:
                _safe_extract(archive, source)
            env = {**os.environ, "JEKYLL_ENV": "production"}
            commands = (
                ("bundle", "exec", "jekyll", "build", "-d", "public"),
                ("ruby", "scripts/verify_site_artifact.rb", "public"),
                ("ruby", "scripts/verify_distribution_readiness.rb", "public"),
            )
            for command in commands:
                try:
                    subprocess.run(
                        command,
                        cwd=source,
                        env=env,
                        check=True,
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                    )
                except subprocess.CalledProcessError as exc:
                    raise VerificationError(f"falló gate local: {' '.join(command)}") from exc
        except (OSError, subprocess.CalledProcessError, tarfile.TarError) as exc:
            raise VerificationError("falló un gate local del commit") from exc


def _origin_gitlab_project(repo_root: Path) -> str:
    remote = _run_git(repo_root, "remote", "get-url", "origin")
    parsed = urllib.parse.urlparse(remote)
    if parsed.scheme in {"http", "https", "ssh"} and parsed.hostname == "gitlab.com":
        project = parsed.path.lstrip("/")
    elif remote.startswith("git@gitlab.com:"):
        project = remote.removeprefix("git@gitlab.com:")
    else:
        raise VerificationError("origin no apunta a GitLab")
    if not project.endswith(".git"):
        raise VerificationError("origin de GitLab inválido")
    return project.removesuffix(".git")


def _verify_remote_ref(repo_root: Path, ref: str, commit: str) -> None:
    for label, remote in (("GitLab", "origin"), ("GitHub", "github")):
        try:
            output = subprocess.check_output(
                ["git", "ls-remote", "--exit-code", remote, f"refs/heads/{ref}"],
                cwd=repo_root,
                stderr=subprocess.DEVNULL,
                text=True,
                timeout=HTTP_TIMEOUT_SECONDS,
            )
        except (OSError, subprocess.CalledProcessError, subprocess.TimeoutExpired) as exc:
            raise VerificationError(f"{label} no confirma la referencia publicada") from exc
        remote_commit = output.split()[0] if output.split() else ""
        if remote_commit != commit:
            raise VerificationError(f"{label} no contiene exactamente el commit solicitado")


def _get_json(url: str) -> object:
    request = urllib.request.Request(url, headers={"User-Agent": "3cucharadas-release-verifier/1"})
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
            return json.loads(response.read().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise VerificationError("no se pudo verificar GitLab CI") from exc


def _verify_gitlab_pipeline(repo_root: Path, ref: str, commit: str) -> int | str:
    project = urllib.parse.quote(_origin_gitlab_project(repo_root), safe="")
    query = urllib.parse.urlencode({"sha": commit, "ref": ref, "status": "success", "per_page": "20"})
    payload = _get_json(f"https://gitlab.com/api/v4/projects/{project}/pipelines?{query}")
    if not isinstance(payload, list):
        raise VerificationError("GitLab CI devolvió una respuesta inesperada")
    for pipeline in payload:
        if isinstance(pipeline, dict) and pipeline.get("sha") == commit and pipeline.get("status") == "success":
            pipeline_id = pipeline.get("id")
            if isinstance(pipeline_id, (int, str)):
                return pipeline_id
    raise VerificationError("GitLab CI aún no registra un pipeline exitoso para el commit")


def _verify_public_page(publication_url: str, expected_text: str) -> None:
    request = urllib.request.Request(publication_url, headers={"User-Agent": "3cucharadas-release-verifier/1"})
    try:
        opener = urllib.request.build_opener(_CanonicalPublicationRedirectHandler())
        with opener.open(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
            final_url = _validate_publication_url(response.geturl())
            body = response.read(MAX_PUBLIC_PAGE_BYTES + 1)
    except (OSError, ValueError) as exc:
        raise VerificationError("no se pudo leer la página pública") from exc
    if len(body) > MAX_PUBLIC_PAGE_BYTES:
        raise VerificationError("la página pública excede el límite de verificación")
    if expected_text not in body.decode("utf-8", errors="replace"):
        raise VerificationError("la página pública no contiene el texto esperado")
    if not final_url:
        raise VerificationError("la página pública no terminó en un destino permitido")


def verify_release(repo_root: Path, ref: str, revision: str, publication_url: str, expected_text: str) -> ReleaseEvidence:
    if not expected_text.strip():
        raise VerificationError("se requiere texto esperado de la publicación")
    verified_url = _validate_publication_url(publication_url)
    commit = _resolve_commit(repo_root, revision)
    _verify_local_gates(repo_root, commit)
    _verify_remote_ref(repo_root, ref, commit)
    pipeline_id = _verify_gitlab_pipeline(repo_root, ref, commit)
    _verify_public_page(verified_url, expected_text)
    return ReleaseEvidence(commit=commit, publication_url=verified_url, pipeline_id=pipeline_id)


def _build_message(evidence: ReleaseEvidence, subject: str) -> str:
    safe_subject = html.escape(subject.strip() or "Publicación verificada")
    return "\n".join(
        (
            "✅ <b>3cucharadas publicada</b>",
            safe_subject,
            f"Commit: <code>{html.escape(evidence.commit[:12])}</code>",
            evidence.publication_url,
            "Gate: build · remoto · CI · página",
        )
    )


def _send_message(token: str, chat_id: str, text: str) -> bool:
    request = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=urllib.parse.urlencode(
            {
                "chat_id": chat_id,
                "text": text,
                "parse_mode": "HTML",
                "disable_web_page_preview": "false",
            }
        ).encode("utf-8"),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_SECONDS) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False
    return bool(response_payload.get("ok"))


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Notify after a verified 3cucharadas publication.")
    parser.add_argument("--repo-root", default=".", help="Repository root or a path inside it.")
    parser.add_argument("--ref", default="main", help="Remote branch expected to contain the commit.")
    parser.add_argument("--commit", default="HEAD", help="Commit that must be publicly available.")
    parser.add_argument("--publication-url", required=True, help="HTTPS URL expected to contain the publication.")
    parser.add_argument("--expect-text", required=True, help="Exact visible text expected on the public page.")
    parser.add_argument("--subject", default="", help="Short title for the local notification.")
    parser.add_argument("--dry-run", action="store_true", help="Run all gates without sending Telegram.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        repo_root = _resolve_repo_root(Path(args.repo_root).resolve())
        evidence = verify_release(repo_root, args.ref, args.commit, args.publication_url, args.expect_text)
    except VerificationError as exc:
        print(f"publication-not-verified: {exc}", file=sys.stderr)
        return 1

    if args.dry_run:
        print("publication-dry-run-ok")
        return 0

    token = os.environ.get("EPUB_CURATOR_TG_TOKEN", "").strip()
    chat_id = os.environ.get("EPUB_CURATOR_TG_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("publication-telegram-missing-env", file=sys.stderr)
        return 2
    if _send_message(token, chat_id, _build_message(evidence, args.subject)):
        print("publication-telegram-sent")
        return 0
    print("publication-telegram-send-failed", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
