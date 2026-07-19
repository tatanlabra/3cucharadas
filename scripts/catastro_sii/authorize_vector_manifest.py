#!/usr/bin/env python3
"""Record explicit public-vector confirmation for an audited tile manifest.

This utility is deliberately metadata-only: it never reads, rewrites, copies,
or uploads a PMTiles file.  It preserves the source manifest and writes a new
manifest that references the same versioned assets, records the source SHA-256,
and enables the already-validated Atacama pilot for the deployment workflow.

The confirmation is a project publication decision, not a legal opinion.  The
separate R2 upload and HTTP Range/CORS checks remain mandatory before the
versioned site manifest can be promoted.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


PENDING = "PENDING"
AUTHORIZED_VECTOR = "AUTHORIZED_VECTOR"


def read_json(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise RuntimeError(f"Manifest JSON inválido: {path}") from error
    if not isinstance(payload, dict):
        raise RuntimeError("El manifest debe ser un objeto JSON")
    return payload


def required_mapping(value: object, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise RuntimeError(f"Manifest inválido: falta objeto {label}")
    return value


def validate_audited_pilot(manifest: dict[str, Any]) -> dict[str, Any]:
    status = manifest.get("legal_publication_status")
    if status not in {PENDING, AUTHORIZED_VECTOR}:
        raise RuntimeError(f"Estado de publicación no promovible: {status!r}")

    results = required_mapping(manifest.get("results"), "results")
    communes = required_mapping(results.get("communes"), "results.communes")
    if communes.get("available") is not True:
        raise RuntimeError("No se puede autorizar sin capa comunal validada")
    parcels = required_mapping(results.get("parcel_regions"), "results.parcel_regions")
    pilot = required_mapping(parcels.get("03"), "results.parcel_regions.03")
    if pilot.get("source_layer") != "predios":
        raise RuntimeError("El piloto Atacama no declara source_layer=predios")
    url = pilot.get("url")
    if not isinstance(url, str) or not url.startswith("predios_region_03_") or not url.endswith(".pmtiles"):
        raise RuntimeError("El piloto Atacama no referencia un PMTiles regional versionado")
    for key in ("minzoom", "maxzoom", "feature_count", "bytes", "source_sha256"):
        if key not in pilot:
            raise RuntimeError(f"El piloto Atacama no contiene evidencia auditada: {key}")
    return pilot


def atomic_write(path: Path, contents: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(contents)
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--tiles-manifest", type=Path, required=True)
    command.add_argument("--output", type=Path, required=True)
    command.add_argument(
        "--confirm-public-vector",
        action="store_true",
        help="Confirma expresamente la promoción de este piloto vectorial público.",
    )
    return command


def main() -> int:
    args = parser().parse_args()
    if not args.confirm_public_vector:
        raise RuntimeError("Falta --confirm-public-vector; no se modifica el estado de publicación")
    source = args.tiles_manifest.resolve()
    if not source.is_file():
        raise FileNotFoundError(f"Manifest de tiles ausente: {source}")
    output = args.output.resolve()
    if output.parent != source.parent:
        raise RuntimeError(
            "El manifest autorizado debe escribirse junto al manifest auditado; "
            "así conserva las referencias relativas a territories y los PMTiles versionados"
        )
    source_bytes = source.read_bytes()
    manifest = read_json(source)
    pilot = validate_audited_pilot(manifest)

    promoted = json.loads(json.dumps(manifest))
    promoted["legal_publication_status"] = AUTHORIZED_VECTOR
    promoted["build_scope"] = "authorized-existing-artifact"
    promoted["generated_at"] = datetime.now(UTC).isoformat()
    promoted_results = required_mapping(promoted.get("results"), "results")
    promoted_pilot = required_mapping(
        required_mapping(promoted_results.get("parcel_regions"), "results.parcel_regions").get("03"),
        "results.parcel_regions.03",
    )
    promoted_pilot["available"] = True
    promoted["publication_authorization"] = {
        "kind": "project-owner-public-vector-confirmation",
        "confirmed_at": promoted["generated_at"],
        "source_manifest": source.name,
        "source_manifest_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "pilot_asset": pilot["url"],
        "note": "Estado promovido sin reprocesar datos ni modificar PMTiles o geometrías.",
    }
    atomic_write(output, (json.dumps(promoted, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (FileNotFoundError, RuntimeError, ValueError) as error:
        print(f"ERROR: {error}", file=os.sys.stderr)
        raise SystemExit(1)
