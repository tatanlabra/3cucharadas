#!/usr/bin/env python3
"""Custody check for archived Post III/IV diffusion packages, not scientific QA."""

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys


SOURCE_COMMIT = "f45d34f355636a41b1ac514c8115517b0b394d0d"
ARCHIVE = "difusion/historico/scientific-reset-20261108"
SLUGS = (
    "costos-cierre-escolar-trayectorias",
    "cierre-escolar-educacion-superior-causal-ml",
)
SOURCES = (
    "_posts/2026-10-23-costos-cierre-escolar-trayectorias.md",
    "_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md",
    "_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md",
    "_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml-en.md",
    "_pages/tesis-post3-anexo-metodologico.md",
    "_pages/tesis-post3-anexo-metodologico-en.md",
    "_pages/tesis-post4-anexo-metodologico.md",
    "_pages/tesis-post4-anexo-metodologico-en.md",
)
DERIVATIVES = tuple(
    f"difusion/linkedin/{slug}{language}-carrusel.{extension}"
    for slug in SLUGS
    for language in ("", "-en")
    for extension in ("html", "json")
)
CURRENT_RECEIPT = "docs/contracts/thesis-current-diffusion.json"


def git(repo: Path, *args: str) -> bytes:
    return subprocess.check_output(["git", *args], cwd=repo, stderr=subprocess.PIPE)


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def expected_archive(raw: bytes, slug: str, name: str) -> bytes:
    if name != "podcast/origen.yaml":
        return raw
    old = f"difusion/paquetes/{slug}/".encode()
    new = f"{ARCHIVE}/{slug}/".encode()
    if old not in raw:
        raise ValueError(f"referencia histórica ausente: {slug}/{name}")
    return raw.replace(old, new)


def check_current_package(repo: Path, slug: str, package: Path, historical: dict) -> None:
    """Admit a separately inventoried current campaign, never a restored archive."""
    receipt = repo / CURRENT_RECEIPT
    if not receipt.is_file() or receipt.is_symlink():
        raise ValueError(f"paquete activo sin revisión vigente: {slug}")
    data = json.loads(receipt.read_text(encoding="utf-8"))
    entry = data.get("packages", {}).get(slug, {})
    if data.get("schema_version") != 1 or data.get("archived_source_commit") != SOURCE_COMMIT:
        raise ValueError("recibo de campaña vigente inválido")
    expected_sources = {name for name in SOURCES if name.startswith("_posts/") and slug in name}
    if set(entry.get("sources", {})) != expected_sources:
        raise ValueError(f"fuentes vigentes incompletas: {slug}")
    for name in expected_sources:
        if entry["sources"][name] != sha((repo / name).read_bytes()):
            raise ValueError(f"fuente vigente modificada: {name}")
    if package.is_symlink() or any(p.is_symlink() for p in package.rglob("*")):
        raise ValueError(f"paquete vigente enlazado: {slug}")
    actual = {p.relative_to(package).as_posix(): sha(p.read_bytes()) for p in package.rglob("*") if p.is_file()}
    if not actual or entry.get("artifacts") != actual:
        raise ValueError(f"inventario vigente vacío o modificado: {slug}")
    old_hashes = {h for item in historical.values() for h in (item["source_sha256"], item["archive_sha256"])}
    if old_hashes.intersection(actual.values()):
        raise ValueError(f"pieza histórica restaurada como vigente: {slug}")


def check(repo: Path, archive_root: Path, receipt: Path) -> str:
    data = json.loads(receipt.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("source_commit") != SOURCE_COMMIT:
        raise ValueError("commit fuente incorrecto")
    if data.get("diffusion_deferred") is not True or data.get("status") != "historical_not_current":
        raise ValueError("marcador de difusión diferida ausente")
    if git(repo, "cat-file", "-t", SOURCE_COMMIT).strip() != b"commit":
        raise ValueError("commit fuente irresoluble")
    if set(data.get("sources", {})) != set(SOURCES):
        raise ValueError("inventario de fuentes incompleto")
    for name in SOURCES:
        raw = git(repo, "show", f"{SOURCE_COMMIT}:{name}")
        if data["sources"][name] != sha(raw):
            raise ValueError(f"hash fuente inválido: {name}")
    if set(data.get("derivatives", {})) != set(DERIVATIVES):
        raise ValueError("inventario de carruseles incompleto")
    derivative_dir = archive_root / "linkedin"
    if not derivative_dir.is_dir() or derivative_dir.is_symlink():
        raise ValueError("directorio de carruseles ausente o enlazado")
    actual_derivatives = {p.name for p in derivative_dir.iterdir() if p.is_file()}
    if any(p.is_symlink() for p in derivative_dir.iterdir()) or actual_derivatives != {Path(name).name for name in DERIVATIVES}:
        raise ValueError("carrusel faltante, extra o enlazado")
    for name in DERIVATIVES:
        if (repo / name).exists():
            raise ValueError(f"carrusel obsoleto activo: {name}")
        raw = git(repo, "show", f"{SOURCE_COMMIT}:{name}")
        archived = (derivative_dir / Path(name).name).read_bytes()
        entry = data["derivatives"][name]
        if not isinstance(entry, dict) or entry.get("source_sha256") != sha(raw):
            raise ValueError(f"hash de carrusel inválido: {name}")
        if archived != raw:
            raise ValueError(f"carrusel histórico alterado: {name}")
        if entry.get("archive_sha256") != sha(archived):
            raise ValueError(f"hash de carrusel inválido: {name}")
    if set(data.get("packages", {})) != set(SLUGS):
        raise ValueError("inventario de paquetes incompleto")
    checked = 0
    for slug in SLUGS:
        old_prefix = f"difusion/paquetes/{slug}/"
        current_package = repo / old_prefix
        package = archive_root / slug
        if not package.is_dir() or package.is_symlink():
            raise ValueError(f"paquete histórico ausente o enlazado: {slug}")
        source_names = {
            name.removeprefix(old_prefix)
            for name in git(repo, "ls-tree", "-r", "--name-only", SOURCE_COMMIT, old_prefix).decode().splitlines()
        }
        files = data["packages"][slug]
        if not isinstance(files, dict) or len(source_names) < 10 or set(files) != source_names:
            raise ValueError(f"manifiesto vacío o incompleto: {slug}")
        if current_package.exists():
            check_current_package(repo, slug, current_package, files)
        actual = {p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file()}
        if actual != source_names:
            raise ValueError(f"archivo faltante o extra: {slug}")
        if any(p.is_symlink() for p in package.rglob("*")):
            raise ValueError(f"enlace simbólico en paquete: {slug}")
        for name in sorted(source_names):
            entry = files[name]
            if not isinstance(entry, dict) or not re.fullmatch(r"[a-f0-9]{64}", entry.get("source_sha256", "")) or not re.fullmatch(r"[a-f0-9]{64}", entry.get("archive_sha256", "")):
                raise ValueError(f"hash inválido: {slug}/{name}")
            source = git(repo, "show", f"{SOURCE_COMMIT}:{old_prefix}{name}")
            archived = (package / name).read_bytes()
            if entry["source_sha256"] != sha(source):
                raise ValueError(f"hash fuente inválido: {slug}/{name}")
            if archived != expected_archive(source, slug, name):
                raise ValueError(f"contenido histórico alterado: {slug}/{name}")
            if entry["archive_sha256"] != sha(archived):
                raise ValueError(f"hash archivo inválido: {slug}/{name}")
            checked += 1
    return f"PASS historical-diffusion: {len(SLUGS)} paquetes, {checked} archivos, {len(SOURCES)} fuentes, {len(DERIVATIVES)} carruseles; custodia, no validez científica"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--archive-root", type=Path)
    parser.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    repo = args.repo.resolve()
    archive_root = args.archive_root or repo / ARCHIVE
    receipt = args.receipt or archive_root / "receipt.json"
    try:
        print(check(repo, archive_root, receipt))
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError, json.JSONDecodeError) as error:
        print(f"FAIL historical-diffusion: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
