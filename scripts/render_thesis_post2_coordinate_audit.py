#!/usr/bin/env python3
"""Publica solo la superficie agregada de la auditoría MINEDUC--OSM."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RESEARCH_ROOT = ROOT / "../../incubadora/tesis_mae_mejorada"
AUDIT_RELATIVE = Path("audit/school_coordinate_osm_audit_v1.json")
CSV_RELATIVE = Path("figures/school_coordinate_osm_audit/public_summary.csv")
OUTPUT_RELATIVE = Path(
    "assets/data/thesis-extension-post2/coordinate-audit-summary.json"
)
PUBLIC_RECORD_FIELDS = {
    "region_code",
    "signal",
    "confidence",
    "case_status",
    "distance_band_m",
    "source_year",
    "count",
}
FORBIDDEN_KEYS = {
    "rbd",
    "name",
    "latitude",
    "longitude",
    "address",
    "osm_id",
    "osm_type",
    "mrun",
    "rut",
    "rut_sostenedor",
    "student_id",
}


class CoordinateAuditPublicationError(ValueError):
    """La superficie pública intentó exceder el contrato agregado."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def load_public_records(path: Path) -> list[dict[str, Any]]:
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if set(reader.fieldnames or []) != PUBLIC_RECORD_FIELDS:
            raise CoordinateAuditPublicationError("esquema CSV público divergente")
        records = []
        for row in reader:
            records.append(
                {
                    "region_code": int(row["region_code"]),
                    "signal": row["signal"],
                    "confidence": row["confidence"],
                    "case_status": row["case_status"],
                    "distance_band_m": row["distance_band_m"],
                    "source_year": int(row["source_year"]),
                    "count": int(row["count"]),
                }
            )
    return records


def build_payload(research_root: Path) -> dict[str, Any]:
    audit_path = research_root / AUDIT_RELATIVE
    csv_path = research_root / CSV_RELATIVE
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    records = load_public_records(csv_path)

    if audit["license"] != {
        "attribution": "© OpenStreetMap contributors",
        "combined_row_level_csv_published": False,
        "mineduc_portal_license_observed": None,
        "mineduc_republication_assumed": False,
        "odbl": "https://opendatacommons.org/licenses/odbl/1-0/",
        "public_surface": "aggregate_only",
    }:
        raise CoordinateAuditPublicationError("límite de licencia divergente")
    if sha256(csv_path) != audit["outputs"]["public_summary_csv_sha256"]:
        raise CoordinateAuditPublicationError("hash del resumen CSV divergente")
    if records != audit["public_records"]:
        raise CoordinateAuditPublicationError("CSV agregado no reconcilia con audit JSON")
    scope = audit["scope"]
    matching = audit["osm_matching"]
    total = int(scope["official_rows_audited"])
    if (
        int(scope["operating_establishments"])
        + int(scope["authorized_without_enrollment"])
        != total
        or int(matching["official_rows_with_candidate"])
        + int(matching["official_rows_without_candidate"])
        != total
    ):
        raise CoordinateAuditPublicationError("denominador de auditoría divergente")

    payload = {
        "schema_version": 1,
        "status": audit["status"],
        "frozen_on": audit["frozen_on"],
        "scope": audit["scope"],
        "coordinate_status": audit["coordinate_status"],
        "matching": audit["osm_matching"],
        "commune_signals": audit["commune_signals"],
        "adjudication": audit["adjudication"],
        "license": audit["license"],
        "sources": {
            "audit_sha256": sha256(audit_path),
            "public_summary_csv_sha256": sha256(csv_path),
            "directory_2025_sha256": audit["sources"]["directory_2025_sha256"],
            "commune_archive_sha256": audit["sources"]["commune_archive_sha256"],
            "osm_snapshot_date": audit["sources"]["osm_snapshot_date"],
        },
        "aggregated_records": records,
    }
    serialized_keys = {
        str(key).casefold()
        for item in records
        for key in item
    }
    leaked = sorted(serialized_keys.intersection(FORBIDDEN_KEYS))
    if leaked:
        raise CoordinateAuditPublicationError(
            f"campos por establecimiento en superficie pública: {leaked}"
        )
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--research-root", type=Path, default=DEFAULT_RESEARCH_ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / OUTPUT_RELATIVE)
    parser.add_argument("--check", action="store_true")
    arguments = parser.parse_args()

    payload = build_payload(arguments.research_root.resolve())
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    output = arguments.output.resolve()
    if arguments.check:
        if not output.is_file() or output.read_text(encoding="utf-8") != rendered:
            raise CoordinateAuditPublicationError("resumen público ausente u obsoleto")
        print(
            "THESIS_POST2_COORDINATE_AUDIT_VALID "
            f"records={len(payload['aggregated_records'])}"
        )
        return 0
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(rendered, encoding="utf-8")
    print(
        "THESIS_POST2_COORDINATE_AUDIT_RENDERED "
        f"records={len(payload['aggregated_records'])} output={output}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
