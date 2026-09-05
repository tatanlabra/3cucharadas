#!/usr/bin/env python3
"""Publish the minimal, public-safe summary of the governed thesis case."""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CASE = ROOT / "research" / "structured-shell-thesis-case"
FIXTURE = CASE / "fixtures" / "tesis_temporal_activity.json"
MANIFEST = CASE / "fixtures" / "fixture_manifest.json"
SUMMARY = CASE / "results" / "summary.json"
OUT_DATA = ROOT / "assets" / "data" / "structured-shell" / "tesis-case.json"
OUT_SVG_ES = ROOT / "assets" / "images" / "structured-shell" / "fig-tesis-caso-real.svg"
OUT_SVG_EN = ROOT / "assets" / "images" / "structured-shell" / "fig-tesis-caso-real-en.svg"
LOCAL_PATH = re.compile(r"/home/|\\\\")


def read(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def ensure_safe(value: Any) -> None:
    text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    if LOCAL_PATH.search(text):
        raise ValueError("el activo público contendría una ruta local")


def index(summary: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    rows = summary.get("by_task_arm", [])
    keyed = {(row["task"], row["arm"]): row for row in rows}
    if len(keyed) != 6 or len(rows) != 6 or summary.get("records") != 30 or summary.get("errors") != 0:
        raise ValueError("el resumen no contiene las seis celdas sanas de 30 observaciones")
    for row in keyed.values():
        if row["runs"] != 5 or row["valid_runs"] != 5 or row["correct"] != 5 or row["condition_conformant"] != 5:
            raise ValueError("la celda A/B no cumple el contrato de cinco corridas")
    return keyed


def public_payload(fixture: dict[str, Any], manifest: dict[str, Any], summary: dict[str, Any]) -> dict[str, Any]:
    rows = index(summary)
    tasks = []
    labels = {
        "R1_valid_aggregate": {
            "es": "R1 · ranking sobre agregados válidos",
            "en": "R1 · ranking from valid aggregates",
            "expected_policy_nushell": True,
        },
        "R2_corrupt_aggregate": {
            "es": "R2 · fixture corrupto: bloquear ranking",
            "en": "R2 · corrupt fixture: block ranking",
            "expected_policy_nushell": True,
        },
        "R3_epistemic_boundary": {
            "es": "R3 · límite conceptual: no inferir cierre",
            "en": "R3 · epistemic boundary: do not infer closure",
            "expected_policy_nushell": False,
        },
    }
    for task, label in labels.items():
        arms = []
        for arm in ("without_nushell", "policy_nushell"):
            row = rows[(task, arm)]
            arms.append({
                "arm": arm,
                "runs": row["runs"],
                "correct": row["correct"],
                "used_nushell": row["used_nushell"],
                "median_elapsed_ms": row["median_elapsed_ms"],
                "median_output_tokens": row["median_output_tokens"],
            })
        tasks.append({"id": task, **label, "arms": arms})
    payload = {
        "schema_version": 1,
        "case_id": fixture["case_id"],
        "fixture_sha256": manifest["fixture_sha256"],
        "source_dataset_sha256": fixture["source"]["dataset_sha256"],
        "source_shape": {
            "rows": fixture["source"]["input_rows"],
            "columns": fixture["source"]["input_columns_count"],
            "annual_aggregate_rows": len(fixture["aggregate"]["by_year"]),
        },
        "design": {
            "arms": ["without_nushell", "policy_nushell"],
            "tasks": 3,
            "repetitions_per_task_arm": 5,
            "records": summary["records"],
            "reasoning_effort": "low",
            "intervention": "El control prohíbe Nu; la política congelada lo exige solo para R1 y R2.",
        },
        "tasks": tasks,
        "limits": {
            "es": "Caso único con agregados públicos; sin inferencia poblacional, p-valor ni afirmación de superioridad general. presencia=0 no prueba cierre institucional.",
            "en": "Single case with public aggregates; no population inference, p-value, or general-superiority claim. presence=0 does not prove institutional closure.",
        },
    }
    ensure_safe(payload)
    return payload


def svg(payload: dict[str, Any], locale: str) -> str:
    labels = {
        "es": {
            "eyebrow": "CASO REAL · AGREGADOS PÚBLICOS · 30 EJECUCIONES",
            "title": "La política cumple la ruta; no prueba que Nushell gane",
            "sub": "Codex read-only · razonamiento low · 3 tareas × 2 brazos × 5 repeticiones",
            "task": "TAREA", "arm": "BRAZO", "correct": "ACIERTO", "nu": "USÓ NU", "median": "MEDIANA",
            "without": "Sin Nu", "policy": "Política Nu", "token": "tok",
            "note_one": "R1/R2: la política pidió Nu y se observó 5/5. R3: no lo pidió y se observó 0/5.",
            "note_two": "Caso único; sin inferencia poblacional, p-valor ni claim de rendimiento general.",
            "title_alt": "Caso real agregado de tesis: A/B Codex con y sin política Nushell",
            "desc": "Treinta ejecuciones. Ambos brazos acertaron cinco de cinco en cada una de tres tareas. La política activó Nushell cinco de cinco veces en las dos tareas estructuradas y cero de cinco veces en el límite conceptual.",
        },
        "en": {
            "eyebrow": "REAL CASE · PUBLIC AGGREGATES · 30 RUNS",
            "title": "The policy follows its route; it does not prove Nushell wins",
            "sub": "Codex read-only · low reasoning · 3 tasks × 2 arms × 5 repetitions",
            "task": "TASK", "arm": "ARM", "correct": "CORRECT", "nu": "USED NU", "median": "MEDIAN",
            "without": "No Nu", "policy": "Nu policy", "token": "tok",
            "note_one": "R1/R2: policy required Nu and observed 5/5. R3: policy did not require it and observed 0/5.",
            "note_two": "Single case; no population inference, p-value, or general-performance claim.",
            "title_alt": "Real aggregated thesis case: Codex A/B with and without a Nushell policy",
            "desc": "Thirty runs. Both arms were correct in five of five repetitions for three tasks. The policy activated Nushell five of five times in two structured tasks and zero of five in the conceptual boundary.",
        },
    }[locale]
    rows = []
    y = 234
    for task in payload["tasks"]:
        for arm in task["arms"]:
            arm_label = labels["policy"] if arm["arm"] == "policy_nushell" else labels["without"]
            nu = f"{arm['used_nushell']}/{arm['runs']}"
            rows.append(
                f'<text x="72" y="{y}" class="task">{task[locale] if arm["arm"] == "without_nushell" else ""}</text>'
                f'<text x="500" y="{y}" class="arm">{arm_label}</text>'
                f'<text x="660" y="{y}" class="ok">{arm["correct"]}/{arm["runs"]}</text>'
                f'<text x="790" y="{y}" class="nu">{nu}</text>'
                f'<text x="920" y="{y}" class="metric">{arm["median_elapsed_ms"] / 1000:.1f} s · {arm["median_output_tokens"]:.0f} {labels["token"]}</text>'
            )
            y += 60
        y += 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 700" role="img" aria-labelledby="title desc">
  <title id="title">{labels["title_alt"]}</title>
  <desc id="desc">{labels["desc"]}</desc>
  <style>
    .bg{{fill:#121521}} .panel{{fill:#1b2032;stroke:#2a3041;stroke-width:2}} text{{font-family:system-ui,-apple-system,Segoe UI,sans-serif;fill:#e8ecf5}} .eyebrow{{font-size:18px;letter-spacing:2px;fill:#37e7ff;font-weight:700}} .title{{font-size:31px;font-weight:700}} .sub{{font-size:17px;fill:#aeb8ca}} .head{{font-size:15px;fill:#aeb8ca;font-weight:700}} .task{{font-size:16px;font-weight:650}} .arm{{font-size:16px}} .ok{{font-size:18px;fill:#b8ff3c;font-weight:700}} .nu{{font-size:18px;fill:#37e7ff;font-weight:700}} .metric{{font-size:16px;fill:#aeb8ca}} .note{{font-size:15px;fill:#aeb8ca}} .rule{{stroke:#2a3041;stroke-width:1}}
  </style>
  <rect class="bg" width="1200" height="700" rx="20"/>
  <text x="72" y="72" class="eyebrow">{labels["eyebrow"]}</text>
  <text x="72" y="120" class="title">{labels["title"]}</text>
  <text x="72" y="154" class="sub">{labels["sub"]}</text>
  <rect x="52" y="188" width="1096" height="414" rx="14" class="panel"/>
  <text x="72" y="214" class="head">{labels["task"]}</text><text x="500" y="214" class="head">{labels["arm"]}</text><text x="660" y="214" class="head">{labels["correct"]}</text><text x="790" y="214" class="head">{labels["nu"]}</text><text x="920" y="214" class="head">{labels["median"]}</text>
  <line x1="72" x2="1128" y1="226" y2="226" class="rule"/>
  {''.join(rows)}
  <text x="72" y="648" class="note">{labels["note_one"]}</text>
  <text x="72" y="675" class="note">{labels["note_two"]}</text>
</svg>
'''


def main() -> int:
    payload = public_payload(read(FIXTURE), read(MANIFEST), read(SUMMARY))
    OUT_DATA.parent.mkdir(parents=True, exist_ok=True)
    OUT_SVG_ES.parent.mkdir(parents=True, exist_ok=True)
    OUT_DATA.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    OUT_SVG_ES.write_text(svg(payload, "es"), encoding="utf-8")
    OUT_SVG_EN.write_text(svg(payload, "en"), encoding="utf-8")
    print(json.dumps({"status": "PASS", "data": str(OUT_DATA.relative_to(ROOT)), "svg_es": str(OUT_SVG_ES.relative_to(ROOT)), "svg_en": str(OUT_SVG_EN.relative_to(ROOT))}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
