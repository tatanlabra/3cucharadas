#!/usr/bin/env python3
"""Summarise the thesis case without treating repetitions as independent tasks."""
from __future__ import annotations

import argparse
import json
import statistics
from collections import defaultdict
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent


def median(values: list[float]) -> float | None:
    return statistics.median(values) if values else None


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def summarise(rows: list[dict[str, Any]]) -> dict[str, Any]:
    groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[(row["task"], row["arm"])].append(row)
    summary_rows = []
    for (task, arm), group in sorted(groups.items()):
        valid = [row for row in group if "error" not in row]
        elapsed = [float(row["elapsed_ms"]) for row in valid]
        summary_rows.append({
            "task": task,
            "arm": arm,
            "runs": len(group),
            "valid_runs": len(valid),
            "correct": sum(bool(row.get("correct")) for row in valid),
            "content_correct": sum(bool(row.get("content_correct")) for row in valid),
            "condition_conformant": sum(bool(row.get("condition_conformant")) for row in valid),
            "used_nushell": sum(bool(row.get("used_nushell")) for row in valid),
            "median_elapsed_ms": median(elapsed),
            "elapsed_range_ms": [min(elapsed, default=None), max(elapsed, default=None)],
            "median_output_tokens": median([float(row["output_tokens"]) for row in valid if row.get("output_tokens") is not None]),
        })
    return {
        "schema_version": 1,
        "interpretation": "descriptive_single_case_intervention_only",
        "records": len(rows),
        "errors": sum("error" in row for row in rows),
        "by_task_arm": summary_rows,
    }


def markdown(summary: dict[str, Any]) -> str:
    lines = [
        "# Caso agregado de tesis · A/B Codex",
        "",
        "Las cinco repeticiones son observaciones operativas del mismo caso; no son tareas independientes ni justifican inferencia poblacional.",
        "",
        "| Tarea | Brazo | Contenido | Política | Acierto | Uso Nu | Mediana ms (rango) | Tokens salida |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in summary["by_task_arm"]:
        elapsed = "—" if row["median_elapsed_ms"] is None else f"{row['median_elapsed_ms']:.0f} ({row['elapsed_range_ms'][0]:.0f}–{row['elapsed_range_ms'][1]:.0f})"
        tokens = "—" if row["median_output_tokens"] is None else f"{row['median_output_tokens']:.0f}"
        lines.append(
            f"| {row['task']} | `{row['arm']}` | {row['content_correct']}/{row['valid_runs']} | "
            f"{row['condition_conformant']}/{row['valid_runs']} | {row['correct']}/{row['valid_runs']} | "
            f"{row['used_nushell']}/{row['valid_runs']} | {elapsed} | {tokens} |"
        )
    lines.extend(["", "No se calcula p-valor ni intervalo poblacional.", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=HERE / "results" / "results.jsonl")
    parser.add_argument("--out-dir", type=Path, default=HERE / "results")
    args = parser.parse_args()
    summary = summarise(load_jsonl(args.results))
    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    (args.out_dir / "report.md").write_text(markdown(summary), encoding="utf-8")
    print(json.dumps({"status": "PASS" if summary["errors"] == 0 else "FAIL", "records": summary["records"], "errors": summary["errors"]}))
    return 0 if summary["errors"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
