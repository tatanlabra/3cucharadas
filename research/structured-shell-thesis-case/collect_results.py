#!/usr/bin/env python3
"""Validate and merge independently executed thesis-case observations."""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
ARMS = {"without_nushell", "policy_nushell"}
UNSAFE = re.compile(r"/home/", re.IGNORECASE)


def load_one(path: Path) -> dict[str, Any]:
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    if len(rows) != 1 or not isinstance(rows[0], dict):
        raise ValueError(f"{path.name}: se esperaba exactamente un objeto JSON")
    return rows[0]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, default=HERE / "results" / "individual")
    parser.add_argument("--out", type=Path, default=HERE / "results" / "results.jsonl")
    parser.add_argument("--repeats", type=int, default=5)
    args = parser.parse_args()
    task_ids = [task["id"] for task in json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))["tasks"]]
    expected = {(repeat, task, arm) for repeat in range(1, args.repeats + 1) for task in task_ids for arm in ARMS}
    rows = [load_one(path) for path in sorted(args.input_dir.glob("*.jsonl"))]
    keys = [(int(row.get("repeat", -1)), row.get("task"), row.get("arm")) for row in rows]
    observed = set(keys)
    errors: list[str] = []
    if len(observed) != len(rows):
        errors.append("hay observaciones duplicadas")
    if expected - observed:
        errors.append(f"faltan {len(expected - observed)} observaciones")
    if observed - expected:
        errors.append(f"sobran {len(observed - expected)} observaciones")
    if any("error" in row for row in rows):
        errors.append("hay observaciones sin respuesta validada")
    if any(not bool(row.get("condition_conformant")) for row in rows):
        errors.append("hay incumplimiento del brazo experimental")
    if any(UNSAFE.search(json.dumps(row, ensure_ascii=False)) for row in rows):
        errors.append("una observación contiene metadato local no publicable")
    if len({row.get("reasoning_effort") for row in rows}) != 1:
        errors.append("reasoning_effort no es constante")
    by_task: dict[str, set[str]] = defaultdict(set)
    for row in rows:
        by_task[str(row.get("task"))].add(str(row.get("fixture_sha256")))
    if any(len(hashes) != 1 for hashes in by_task.values()):
        errors.append("un fixture cambió entre réplicas del mismo task")
    ordered = sorted(rows, key=lambda row: (int(row["repeat"]), row["task"], row["arm"]))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text("".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in ordered), encoding="utf-8")
    manifest = {
        "status": "PASS" if not errors else "FAIL", "expected_records": len(expected), "observed_records": len(rows),
        "reasoning_effort": next(iter({row.get("reasoning_effort") for row in rows}), None),
        "errors": errors,
    }
    args.out.with_suffix(".collection.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": manifest["status"], "records": len(rows), "errors": len(errors)}))
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
