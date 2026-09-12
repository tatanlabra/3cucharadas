#!/usr/bin/env python3
"""Prepare two isolated, instrumented historical builds; never edit the site."""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import tarfile

REVISIONS = ("e986f238", "6b46731e")
SOURCE_FILES = (
    "assets/src/catastro_sii", "package.json", "package-lock.json",
    "vite.catastro.config.ts", "catastro_sii_brecha/index.html",
    "catastro_sii_brecha/style.css", "catastro_sii_brecha/app.js",
    "catastro_sii_brecha/assets",
)
MAP_HOOK = '''    // Symmetric read-only benchmark observer; isolated copies only.
    (window as unknown as { __catastroBenchmark?: { registerMap?:
      (map: unknown, container: HTMLElement, style: unknown, manifest: unknown) => void
    } }).__catastroBenchmark?.registerMap?.(map, container, style, manifest);
'''


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare(repo: Path, root: Path, revision: str) -> dict:
    dest = root / "source" / revision
    if dest.exists():
        raise RuntimeError(f"No sobrescribir un build previo: {dest}")
    dest.mkdir(parents=True)
    payload = subprocess.check_output(["git", "archive", revision, *SOURCE_FILES], cwd=repo)
    with tarfile.open(fileobj=io.BytesIO(payload)) as archive:
        archive.extractall(dest, filter="data")
    (dest / "node_modules").symlink_to(repo / "node_modules", target_is_directory=True)
    source = dest / "assets/src/catastro_sii/map.ts"
    original_hash = sha256(source)
    text = source.read_text()
    needle = "    configureMapCanvasAccessibility(map.getCanvas(), describedBy);"
    if text.count(needle) != 1:
        raise RuntimeError("No se encontró un único punto de observación MapLibre")
    source.write_text(text.replace(needle, MAP_HOOK + needle))
    prefix = f"/__catastro_benchmark/{revision}/assets/dist/catastro_sii/"
    result = subprocess.run([
        "node", str(repo / "node_modules/vite/bin/vite.js"), "build",
        "--config", "vite.catastro.config.ts", "--base", prefix,
    ], cwd=dest, text=True, capture_output=True)
    (root / f"build-{revision}.log").write_text(result.stdout + result.stderr)
    result.check_returncode()
    web = root / "web" / revision
    web.mkdir(parents=True)
    shutil.copytree(dest / "catastro_sii_brecha", web, dirs_exist_ok=True)
    shutil.copytree(dest / "assets/dist", web / "assets/dist")
    loader = web / "assets/map-app-loader.js"
    loader_text = loader.read_text()
    if loader_text.count('"/assets/dist/catastro_sii/"') != 1:
        raise RuntimeError("El cargador no tiene una única base conocida")
    loader.write_text(loader_text.replace('"/assets/dist/catastro_sii/"', json.dumps(prefix)))
    page = web / "index.html"
    html = page.read_text()
    if html.count("</head>") != 1:
        raise RuntimeError("HTML sin cabecera única")
    html = html.replace("</head>", '<style data-benchmark-fixture>\n'
                        '#bivariate-map { width:750px!important; height:558px!important; }\n'
                        '</style>\n</head>')
    page.write_text(html)
    return {
        "revision": subprocess.check_output(["git", "rev-parse", revision], cwd=repo, text=True).strip(),
        "source_map_sha256": original_hash,
        "instrumented_map_sha256": sha256(source),
        "package_lock_sha256": sha256(dest / "package-lock.json"),
        "bundle_base": prefix,
        "artifacts": {str(f.relative_to(web)): sha256(f) for f in sorted(web.rglob("*")) if f.is_file()},
    }


def project(root: Path, destination: Path) -> None:
    target = destination / "__catastro_benchmark"
    if target.exists() or target.is_symlink():
        raise RuntimeError(f"No sobrescribir ruta del servidor: {target}")
    data = destination / "catastro_sii_brecha/data"
    if not data.is_dir():
        raise RuntimeError(f"Datos compartidos ausentes: {data}")
    for revision in REVISIONS:
        link = root / "web" / revision / "data"
        if not link.exists():
            link.symlink_to(data, target_is_directory=True)
    target.symlink_to(root / "web", target_is_directory=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--project-only", type=Path, metavar="EXISTING_JEKYLL_DESTINATION")
    args = parser.parse_args()
    root = args.root.resolve()
    repo = Path(__file__).resolve().parents[2]
    if args.project_only:
        project(root, args.project_only.resolve())
        print(f"Proyectado en servidor existente: {args.project_only}")
        return
    root.mkdir(parents=True, exist_ok=True)
    evidence = {"variants": [prepare(repo, root, revision) for revision in REVISIONS]}
    if len({variant["package_lock_sha256"] for variant in evidence["variants"]}) != 1:
        raise RuntimeError("Lockfiles diferentes: comparación no preparada")
    (root / "preparation.json").write_text(json.dumps(evidence, indent=2) + "\n")
    print(f"Preparado sin publicar rutas ni navegar: {root}")


if __name__ == "__main__":
    main()
