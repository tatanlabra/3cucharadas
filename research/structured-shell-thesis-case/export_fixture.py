#!/usr/bin/env python3
"""Export a public-safe aggregate fixture from the governed thesis audit."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
FORBIDDEN_VALUE = re.compile(r"/home/|\\", re.IGNORECASE)
FORBIDDEN_KEY = re.compile(r"(?:^|_)(?:rbd|cod_ine)(?:_|$)|relative_path", re.IGNORECASE)
COUNTS = ("input_rows", "valid_year_rows", "presence_one", "presence_zero", "entrada_one", "salida_one")
YEAR_FIELDS = ("year", "rows", "presence_one", "presence_zero", "entrada_one", "salida_one")


class FixtureSafetyError(ValueError):
    """Raised when a fixture would expose a local or identifying marker."""


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_public_fixture(payload: dict[str, Any]) -> None:
    if FORBIDDEN_VALUE.search(canonical(payload)):
        raise FixtureSafetyError("fixture contiene una ruta local")
    stack: list[Any] = [payload]
    while stack:
        current = stack.pop()
        if isinstance(current, dict):
            if any(FORBIDDEN_KEY.search(str(key)) for key in current):
                raise FixtureSafetyError("fixture contiene una clave identificadora")
            stack.extend(current.values())
        elif isinstance(current, list):
            stack.extend(current)
    if payload.get("fixture_kind") not in {"real_aggregated_audit", "synthetic_counterfactual"}:
        raise FixtureSafetyError("fixture_kind inválido")
    source = payload.get("source", {})
    if not re.fullmatch(r"[0-9a-f]{64}", str(source.get("dataset_sha256", ""))):
        raise FixtureSafetyError("hash de fuente inválido")
    aggregate = payload.get("aggregate", {})
    if set(aggregate.get("row_counts", {})) != set(COUNTS):
        raise FixtureSafetyError("conteos agregados incompletos")
    for row in aggregate.get("by_year", []):
        if set(row) != set(YEAR_FIELDS):
            raise FixtureSafetyError("fila anual expone o pierde campos")


def audit_payload(tesis_root: Path, python: str) -> dict[str, Any]:
    command = [python, "scripts/54_audit_temporal_activity.py"]
    result = subprocess.run(command, cwd=tesis_root, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError("la auditoría temporal canónica no terminó correctamente")
    payload = json.loads(result.stdout)
    if payload.get("state") != "TEMPORAL_ACTIVITY_AUDIT":
        raise RuntimeError("la auditoría no devolvió el estado temporal esperado")
    return payload


def build_fixture(audit: dict[str, Any]) -> dict[str, Any]:
    counts = audit["row_counts"]
    fixture = {
        "schema_version": 1,
        "case_id": "tesis-temporal-activity-aggregate-v1",
        "fixture_kind": "real_aggregated_audit",
        "source": {
            "dataset_sha256": audit["input"]["input_sha256"],
            "input_rows": audit["input"]["input_rows"],
            "input_columns_count": audit["input"]["input_columns_count"],
            "audit_schema_version": audit["schema_version"],
            "interpretation_status": audit["interpretation_status"],
        },
        "aggregate": {
            "row_counts": {key: int(counts[key]) for key in COUNTS},
            "by_year": [{key: int(row[key]) for key in YEAR_FIELDS} for row in audit["by_year"]],
        },
        "declared_invariants": {
            "input_rows_equals_valid_year_rows": int(counts["input_rows"]) == int(counts["valid_year_rows"]),
            "sum_by_year_rows_equals_valid_year_rows": sum(int(row["rows"]) for row in audit["by_year"]) == int(counts["valid_year_rows"]),
            "presence_counts_do_not_exceed_annual_rows": all(
                int(row["presence_one"]) + int(row["presence_zero"]) <= int(row["rows"])
                for row in audit["by_year"]
            ),
        },
        "epistemic_limits": list(audit["limits"]),
    }
    validate_public_fixture(fixture)
    return fixture


def corrupt_fixture(fixture: dict[str, Any]) -> dict[str, Any]:
    corrupt = json.loads(canonical(fixture))
    corrupt["fixture_kind"] = "synthetic_counterfactual"
    corrupt["case_id"] = "tesis-temporal-activity-aggregate-corrupt-v1"
    corrupt["aggregate"]["by_year"][0]["rows"] += 1
    validate_public_fixture(corrupt)
    return corrupt


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tesis-root", type=Path, required=True)
    parser.add_argument("--python", default="/opt/entornos/mamba312/bin/python")
    parser.add_argument("--out-dir", type=Path, default=HERE / "fixtures")
    args = parser.parse_args()
    audit = audit_payload(args.tesis_root.expanduser().resolve(), args.python)
    fixture = build_fixture(audit)
    corrupt = corrupt_fixture(fixture)
    output = args.out_dir.expanduser().resolve()
    write_json(output / "tesis_temporal_activity.json", fixture)
    write_json(output / "tesis_temporal_activity_corrupt.json", corrupt)
    manifest = {
        "schema_version": 1,
        "case_id": fixture["case_id"],
        "fixture_sha256": sha256(output / "tesis_temporal_activity.json"),
        "corrupt_fixture_sha256": sha256(output / "tesis_temporal_activity_corrupt.json"),
        "source_dataset_sha256": fixture["source"]["dataset_sha256"],
        "public_safe": True,
    }
    write_json(output / "fixture_manifest.json", manifest)
    print(json.dumps({"status": "PASS", "fixture_sha256": manifest["fixture_sha256"]}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
