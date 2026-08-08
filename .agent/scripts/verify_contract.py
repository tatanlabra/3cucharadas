#!/usr/bin/env python3
"""Verificador de contrato.

Ejecuta los criterios de aceptación declarados en `.agent/contract.yaml`,
guarda la salida real de cada uno como evidencia y devuelve un veredicto
determinista.

El agente produce claims. Este script produce evidencia.

Exit codes
----------
0   contrato cumplido (todos los criterios requeridos del alcance pasaron)
1   contrato incumplido
2   contrato o esquema inválido
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: falta PyYAML. Instalar con: pip install --user pyyaml", file=sys.stderr)
    raise SystemExit(2)

REPO = Path(__file__).resolve().parents[2]
AGENT_DIR = REPO / ".agent"
CONTRACT = AGENT_DIR / "contract.yaml"
EVIDENCE = AGENT_DIR / "evidence"

REQUIRED_TOP_LEVEL = ("contract_version", "task", "goal", "acceptance")

PASS, FAIL, SKIP = "PASS", "FAIL", "SKIP"


class ContractError(Exception):
    """El contrato no es válido. Se traduce a exit code 2."""


def load_contract() -> dict:
    if not CONTRACT.exists():
        raise ContractError(f"no existe {CONTRACT.relative_to(REPO)}")
    try:
        data = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ContractError(f"YAML inválido: {exc}") from exc
    if not isinstance(data, dict):
        raise ContractError("la raíz del contrato debe ser un mapping")
    for key in REQUIRED_TOP_LEVEL:
        if key not in data:
            raise ContractError(f"falta la clave obligatoria '{key}'")
    if not isinstance(data.get("acceptance"), list) or not data["acceptance"]:
        raise ContractError("'acceptance' debe ser una lista no vacía")

    seen: set[str] = set()
    for item in data["acceptance"]:
        if not isinstance(item, dict):
            raise ContractError("cada criterio de aceptación debe ser un mapping")
        for key in ("id", "description", "command"):
            if not item.get(key):
                raise ContractError(f"criterio sin '{key}': {item!r}")
        if item["id"] in seen:
            raise ContractError(f"id de criterio duplicado: {item['id']}")
        seen.add(item["id"])
    return data


def check_deliverables(contract: dict) -> list[tuple[str, str, str]]:
    rows = []
    for item in contract.get("deliverables") or []:
        path = REPO / item["path"]
        ok = path.exists()
        if not ok and not item.get("required", True):
            rows.append((item["id"], SKIP, f"{item['path']} (opcional, ausente)"))
            continue
        rows.append((item["id"], PASS if ok else FAIL, item["path"]))
    return rows


def run_criterion(item: dict, artifact: str, timeout: int) -> tuple[str, str, int, float]:
    """Ejecuta un criterio. Devuelve (estado, salida, exit_code, duración)."""
    command = item["command"].replace("{artifact}", artifact)
    started = time.monotonic()
    try:
        proc = subprocess.run(
            command,
            shell=True,
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        code = proc.returncode
        output = proc.stdout + (("\n[stderr]\n" + proc.stderr) if proc.stderr else "")
    except subprocess.TimeoutExpired:
        code = 124
        output = f"TIMEOUT tras {timeout}s"
    duration = time.monotonic() - started
    return (PASS if code == 0 else FAIL), output, code, duration


def write_evidence(item: dict, command: str, output: str, code: int, duration: float) -> Path:
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    phase = item.get("phase", "NA")
    path = EVIDENCE / f"{phase}-{item['id']}.txt"
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    path.write_text(
        f"criterio:  {item['id']}\n"
        f"fase:      {phase}\n"
        f"objetivo:  {item['description']}\n"
        f"comando:   {command}\n"
        f"timestamp: {stamp}\n"
        f"duracion:  {duration:.1f}s\n"
        f"exit_code: {code}\n"
        f"{'-' * 70}\n{output}\n",
        encoding="utf-8",
    )
    return path


def main() -> int:
    parser = argparse.ArgumentParser(description="Verifica el contrato de la tarea.")
    parser.add_argument(
        "--phase",
        action="append",
        dest="phases",
        metavar="ID",
        help="limita a una fase (repetible). Por defecto, todas.",
    )
    parser.add_argument("--only", action="append", metavar="AC-ID", help="ejecuta solo estos criterios.")
    parser.add_argument("--artifact", help="directorio del artefacto (por defecto, el del contrato).")
    parser.add_argument("--timeout", type=int, default=900, help="timeout por criterio en segundos.")
    parser.add_argument("--list", action="store_true", help="lista los criterios y sale.")
    parser.add_argument("--keep-artifact", action="store_true", help="no borra el artefacto al terminar.")
    args = parser.parse_args()

    try:
        contract = load_contract()
    except ContractError as exc:
        print(f"CONTRATO INVÁLIDO: {exc}", file=sys.stderr)
        return 2

    artifact = args.artifact or contract.get("artifact") or "_site_check"
    criteria = contract["acceptance"]

    if args.phases:
        wanted = {p.upper() for p in args.phases}
        criteria = [c for c in criteria if str(c.get("phase", "")).upper() in wanted]
    if args.only:
        wanted = {o.upper() for o in args.only}
        criteria = [c for c in criteria if c["id"].upper() in wanted]

    if args.list:
        for c in contract["acceptance"]:
            print(f"{c.get('phase', 'NA'):<4} {c['id']:<14} {c['description']}")
        return 0

    if not criteria:
        print("Ningún criterio coincide con el filtro.", file=sys.stderr)
        return 2

    task_id = contract["task"].get("id", "sin-id")
    print(f"\nVERIFICACIÓN DE CONTRATO — {task_id}")
    print(f"artefacto: {artifact}    criterios: {len(criteria)}\n")

    rows: list[tuple[str, str, str]] = []

    for item in check_deliverables(contract):
        rows.append(item)
        print(f"[{item[1]}] {item[0]:<14} {item[2]}")

    if rows:
        print()

    for item in criteria:
        command = item["command"].replace("{artifact}", artifact)
        status, output, code, duration = run_criterion(item, artifact, args.timeout)
        evidence = write_evidence(item, command, output, code, duration)
        detail = item["description"]
        if status == FAIL:
            first = next(
                (ln for ln in output.splitlines() if ln.strip()),
                f"exit {code}",
            )
            detail = f"{detail}\n{'':<22}└─ {first.strip()[:110]}"
        print(f"[{status}] {item['id']:<14} {detail}  ({duration:.1f}s)")
        rows.append((item["id"], status, str(evidence.relative_to(REPO))))

    manual = contract.get("manual_acceptance") or []
    if manual:
        print("\nVerificaciones manuales pendientes de evidencia (no bloquean):")
        for item in manual:
            summary = " ".join(str(item["description"]).split())
            print(f"  · {item['id']:<12} {summary[:100]}")

    failed = [r for r in rows if r[1] == FAIL]
    print(f"\n{'=' * 70}")
    if failed:
        print(f"RESULTADO: NOT COMPLETE — {len(failed)} de {len(rows)} fallaron")
        print(f"Evidencia en {EVIDENCE.relative_to(REPO)}/")
        for fid, _, where in failed:
            print(f"  FAIL {fid:<14} {where}")
        result = 1
    else:
        print(f"RESULTADO: COMPLETE — {len(rows)} criterios con evidencia")
        result = 0
    print(f"{'=' * 70}\n")

    if not args.keep_artifact and args.artifact is None:
        target = REPO / artifact
        if target.is_dir() and target.name.startswith("_site_"):
            shutil.rmtree(target, ignore_errors=True)

    return result


if __name__ == "__main__":
    os.environ.setdefault("LC_ALL", "C")
    sys.exit(main())
