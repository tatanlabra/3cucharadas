#!/usr/bin/env python3
"""Run a controlled, public-safe Codex A/B against the aggregate thesis fixture.

This is an intervention experiment: the control explicitly forbids Nushell and
the treatment provides a frozen selective-Nushell policy. It does not test
whether a model naturally discovers a local skill.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import tempfile
import time
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterable


HERE = Path(__file__).resolve().parent
TASKS_PATH = HERE / "tasks.json"
SCHEMA_PATH = HERE / "response.schema.json"
POLICY_PATH = HERE / "policy_packet.md"
NU_RE = re.compile(r"\b(?:nu|nu-query)\b", re.IGNORECASE)
UNSAFE_RESPONSE = re.compile(r"/home/", re.IGNORECASE)
LOCAL_PATH = re.compile(r"/home/[^\s'\";]+")


def canonical(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def public_safe(value: Any) -> bool:
    return UNSAFE_RESPONSE.search(canonical(value)) is None


def redact_local_paths(command: str) -> str:
    return LOCAL_PATH.sub("<local-path>", command)


def observed_failed_invariants(fixture: dict[str, Any]) -> list[str]:
    counts = fixture["aggregate"]["row_counts"]
    annual = fixture["aggregate"]["by_year"]
    checks = {
        "input_rows_equals_valid_year_rows": counts["input_rows"] == counts["valid_year_rows"],
        "sum_by_year_rows_equals_valid_year_rows": sum(row["rows"] for row in annual) == counts["valid_year_rows"],
        "presence_counts_do_not_exceed_annual_rows": all(
            row["presence_one"] + row["presence_zero"] <= row["rows"] for row in annual
        ),
    }
    return [name for name, ok in checks.items() if not ok]


def observed_top_years(fixture: dict[str, Any]) -> list[dict[str, int]]:
    return [
        {"year": int(row["year"]), "salida_one": int(row["salida_one"])}
        for row in sorted(fixture["aggregate"]["by_year"], key=lambda row: (-row["salida_one"], row["year"]))[:3]
    ]


def score_response(response: dict[str, Any], task: dict[str, Any], fixture: dict[str, Any]) -> tuple[bool, list[str]]:
    issues: list[str] = []
    if not public_safe(response):
        issues.append("respuesta contiene una ruta local")
    if response.get("limitation_acknowledged") is not True:
        issues.append("no reconoce el límite epistemológico")
    if task["mode"] == "valid":
        if response.get("status") != "PASS":
            issues.append("fixture válido no devuelve PASS")
        if response.get("failed_invariants") != []:
            issues.append("fixture válido reporta invariante fallida")
        if response.get("top_years") != observed_top_years(fixture):
            issues.append("ranking anual no coincide")
    elif task["mode"] == "corrupt":
        if response.get("status") != "BLOCKED":
            issues.append("fixture corrupto no devuelve BLOCKED")
        if response.get("failed_invariants") != observed_failed_invariants(fixture):
            issues.append("invariantes fallidas no coinciden")
        if response.get("top_years") != []:
            issues.append("fixture corrupto produjo un ranking prohibido")
    elif task["mode"] == "boundary":
        answer = str(response.get("answer", "")).casefold()
        if response.get("status") != "OUT_OF_SCOPE":
            issues.append("límite conceptual no devuelve OUT_OF_SCOPE")
        if response.get("failed_invariants") != [] or response.get("top_years") != []:
            issues.append("límite conceptual produjo datos no solicitados")
        if not re.search(r"\bno\b|no demuestra|no prueba", answer):
            issues.append("respuesta no niega la inferencia de cierre")
    else:
        issues.append("modo de tarea desconocido")
    return not issues, issues


def recursive_values(value: Any) -> Iterable[tuple[str, Any]]:
    if isinstance(value, dict):
        for key, item in value.items():
            yield key, item
            yield from recursive_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from recursive_values(item)


def commands_from_events(events: list[dict[str, Any]]) -> list[str]:
    commands: list[str] = []
    for event in events:
        for key, value in recursive_values(event):
            if key in {"command", "cmd"} and isinstance(value, str) and value not in commands:
                commands.append(value)
    return commands


def usage_from_events(events: list[dict[str, Any]]) -> dict[str, int | None]:
    usage: dict[str, int | None] = {"input_tokens": None, "output_tokens": None, "tool_calls": 0}
    for event in events:
        for key, value in recursive_values(event):
            if key == "input_tokens" and isinstance(value, int):
                usage["input_tokens"] = value
            elif key == "output_tokens" and isinstance(value, int):
                usage["output_tokens"] = value
            elif key in {"tool_name", "tool_call"}:
                usage["tool_calls"] = int(usage["tool_calls"] or 0) + 1
    return usage


def build_prompt(task: dict[str, Any], arm: str, policy: str) -> str:
    prompt = (
        "Trabaja solo sobre el fixture JSON indicado y no escribas archivos. "
        "Devuelve solo el objeto JSON que exige el esquema. "
        f"Fixture: `{task['fixture']}`. Tarea: {task['prompt']}"
    )
    if arm == "without_nushell":
        return prompt + "\n\nControl experimental: no ejecutes Nushell, `nu` ni `nu-query`; usa otra herramienta de solo lectura si hace falta."
    return prompt + "\n\nPolítica experimental congelada:\n" + policy


def run_one(task: dict[str, Any], arm: str, *, timeout: int, policy: str, reasoning_effort: str) -> dict[str, Any]:
    fixture_path = HERE / task["fixture"]
    fixture = load_json(fixture_path)
    started = time.monotonic()
    with tempfile.TemporaryDirectory(prefix="nushell-thesis-case-") as temporary:
        final_path = Path(temporary) / "final.json"
        command = [
            "codex", "exec", "--ephemeral", "--sandbox", "read-only", "--skip-git-repo-check",
            "--ignore-user-config", "-c", f"model_reasoning_effort={reasoning_effort}",
            "-C", str(HERE), "--output-schema", str(SCHEMA_PATH), "--json",
            "--output-last-message", str(final_path), build_prompt(task, arm, policy),
        ]
        try:
            process = subprocess.run(command, capture_output=True, text=True, timeout=timeout, check=False)
        except subprocess.TimeoutExpired:
            return {
                "timestamp_utc": datetime.now(UTC).isoformat(), "provider": "codex", "arm": arm,
                "task": task["id"], "kind": task["kind"], "reasoning_effort": reasoning_effort,
                "fixture_sha256": sha256(fixture_path), "elapsed_ms": round((time.monotonic() - started) * 1000),
                "error": "codex excedió timeout", "used_nushell": False,
            }
        events = []
        for line in process.stdout.splitlines():
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(event, dict):
                events.append(event)
        raw_commands = commands_from_events(events)
        record: dict[str, Any] = {
            "timestamp_utc": datetime.now(UTC).isoformat(), "provider": "codex", "arm": arm,
            "task": task["id"], "kind": task["kind"], "reasoning_effort": reasoning_effort,
            "fixture_sha256": sha256(fixture_path),
            "policy_sha256": hashlib.sha256(policy.encode()).hexdigest() if arm == "policy_nushell" else None,
            "elapsed_ms": round((time.monotonic() - started) * 1000), "returncode": process.returncode,
            "commands": [redact_local_paths(item) for item in raw_commands], "events": len(events),
        }
        record["used_nushell"] = any(NU_RE.search(item) for item in raw_commands)
        record.update(usage_from_events(events))
        if process.returncode != 0 or not final_path.is_file():
            record.update({"error": "codex no produjo respuesta validada", "stderr_head": process.stderr[:300]})
            return record
        try:
            response = load_json(final_path)
        except json.JSONDecodeError:
            record["error"] = "respuesta final no es JSON"
            return record
        if not isinstance(response, dict):
            record["error"] = "respuesta final no es objeto"
            return record
        content_correct, issues = score_response(response, task, fixture)
        expected_nushell = arm == "policy_nushell" and task["kind"] == "positive"
        condition_conformant = record["used_nushell"] == expected_nushell
        if not condition_conformant:
            issues.append("la herramienta observada no cumple el brazo experimental")
        record.update({
            "response": response, "content_correct": content_correct,
            "condition_conformant": condition_conformant,
            "correct": content_correct and condition_conformant, "score_issues": issues,
        })
        return record


def selected_tasks(ids: list[str] | None) -> list[dict[str, Any]]:
    tasks = load_json(TASKS_PATH)["tasks"]
    if ids:
        tasks = [task for task in tasks if task["id"] in ids]
    if not tasks:
        raise ValueError("no hay tareas seleccionadas")
    return tasks


def provider_version() -> str:
    result = subprocess.run(["codex", "--version"], capture_output=True, text=True, check=False)
    return result.stdout.strip() or result.stderr.strip() or "unknown"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--repeat-start", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--tasks", nargs="*")
    parser.add_argument("--arms", nargs="*", choices=["without_nushell", "policy_nushell"])
    parser.add_argument("--reasoning-effort", choices=["low", "medium", "high", "xhigh"], default="low")
    parser.add_argument("--out", type=Path, default=HERE / "results" / "results.jsonl")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args()
    if args.repeats <= 0 or args.repeat_start <= 0:
        raise ValueError("repeticiones deben ser positivas")
    if shutil.which("codex") is None:
        raise RuntimeError("Codex CLI no está disponible")
    policy = POLICY_PATH.read_text(encoding="utf-8")
    tasks = selected_tasks(args.tasks)
    arms = args.arms or ["without_nushell", "policy_nushell"]
    repeats = 1 if args.preflight else args.repeats
    records: list[dict[str, Any]] = []
    for repeat in range(args.repeat_start, args.repeat_start + repeats):
        order = arms if repeat % 2 else list(reversed(arms))
        for arm in order:
            for task in tasks:
                record = run_one(task, arm, timeout=args.timeout, policy=policy, reasoning_effort=args.reasoning_effort)
                record["repeat"] = repeat
                records.append(record)
                if not args.quiet:
                    state = "OK" if record.get("correct") else "FAIL"
                    print(f"[{len(records)}] {repeat}/{task['id']}/{arm}: {state}", flush=True)
    destination = args.out.expanduser().resolve()
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text("".join(canonical(record) + "\n" for record in records), encoding="utf-8")
    metadata = {
        "provider": "codex", "provider_version": provider_version(), "reasoning_effort": args.reasoning_effort,
        "tasks_sha256": sha256(TASKS_PATH), "policy_packet_sha256": sha256(POLICY_PATH),
        "response_schema_sha256": sha256(SCHEMA_PATH), "expected_records": len(tasks) * len(arms) * repeats,
        "observed_records": len(records), "preflight": args.preflight, "arms": arms,
    }
    write_json(destination.with_suffix(".meta.json"), metadata)
    errors = sum("error" in record for record in records)
    condition_failures = sum(not bool(record.get("condition_conformant")) for record in records if "error" not in record)
    content_failures = sum(not bool(record.get("content_correct")) for record in records if "error" not in record)
    print(json.dumps({"status": "PASS" if not errors and not condition_failures and (not args.preflight or not content_failures) else "FAIL", "records": len(records), "errors": errors, "condition_failures": condition_failures, "content_failures": content_failures}))
    return 0 if not errors and not condition_failures and (not args.preflight or not content_failures) else 1


if __name__ == "__main__":
    raise SystemExit(main())
