from __future__ import annotations

import json
import os
import shutil
import subprocess
import time
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


class ProviderError(RuntimeError):
    pass


@dataclass(slots=True)
class ProviderOutcome:
    provider: str
    payload: dict[str, Any] | None
    attempts: list[dict[str, Any]]


def penta_root() -> Path:
    configured = os.environ.get("PENTA_AGENT_ROOT")
    if configured:
        return Path(configured).expanduser()
    return Path.home() / "Descargas" / "programaciones" / "penta-agent"


def _prompt(context: dict[str, Any]) -> str:
    public_json = json.dumps(context, ensure_ascii=False, sort_keys=True)
    return f"""Create one shared social-media message per language from the public metadata below.

Rules:
- Return no factual number that is absent from the supplied title or description.
- Spanish drafts must be natural Spanish; English drafts must be natural English.
- Write in the author's first person, as a brief note about something they built.
- Prefer this arc when the metadata supports it: concrete problem, what I built, and the practical difficulty or lesson.
- Do not address the reader with imperatives and do not add generic calls to action such as stay informed, take control, discover, or learn more.
- Each message must fit in 190 characters, including at most 2 hashtags.
- Do not include a URL. The local application derives the Mastodon URL variant and Bluesky card.
- Use the same editorial idea in Spanish and English, translated naturally.
- Use equivalent hashtags in both languages and keep product/project capitalization consistent.
- Avoid time-sensitive words such as new, recent, today, nuevo, reciente or hoy.
- Do not claim impact, causality, official endorsement, or statistical significance beyond the metadata.
- Return exactly one compact JSON object with this shape:
  {{"es":"...","en":"..."}}

Public metadata:
{public_json}
"""


def _normalize_text(value: Any, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ProviderError(f"Falta {field}")
    normalized = value.strip()
    if "%20" in normalized and " " not in normalized:
        normalized = urllib.parse.unquote(normalized)
    return normalized


def _validate_payload(payload: Any) -> dict[str, Any]:
    if not isinstance(payload, dict):
        raise ProviderError("La respuesta no es un objeto JSON")
    candidate = payload.get("base_copy") if isinstance(payload.get("base_copy"), dict) else payload
    if all(lang in candidate for lang in ("es", "en")):
        return {lang: _normalize_text(candidate.get(lang), lang) for lang in ("es", "en")}
    # Los runs previos de Antigravity pueden devolver el contrato v1.
    legacy = payload.get("bluesky")
    if isinstance(legacy, dict):
        return {lang: _normalize_text(legacy.get(lang), f"bluesky.{lang}") for lang in ("es", "en")}
    raise ProviderError("Faltan los mensajes base es/en")


def _parse_json(text: str) -> dict[str, Any]:
    marker = "copy_payload_json:"
    candidates: list[str] = []
    for line in text.splitlines():
        if marker in line:
            candidates.append(line.split(marker, 1)[1].strip())
    candidates.append(text.strip())
    decoder = json.JSONDecoder()
    for candidate in candidates:
        for index, char in enumerate(candidate):
            if char != "{":
                continue
            try:
                payload, _ = decoder.raw_decode(candidate[index:])
                return _validate_payload(payload)
            except (json.JSONDecodeError, ProviderError):
                continue
    raise ProviderError("No se encontro copy_payload_json valido")


def _attempt(provider: str, status: str, started: float, reason: str = "") -> dict[str, Any]:
    return {
        "provider": provider,
        "status": status,
        "latency_ms": int((time.monotonic() - started) * 1000),
        "reason": reason[:300],
    }


def _find_agy_run(task_path: Path, started_epoch: float) -> tuple[dict[str, Any], Path]:
    state_root = penta_root().parent / ".agents" / "runs"
    matches: list[tuple[float, dict[str, Any], Path]] = []
    if not state_root.exists():
        raise ProviderError("agy-bridge no dejo runs en el state dir canonico")
    for status_path in state_root.glob("agy-*/status.json"):
        try:
            status = json.loads(status_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if Path(str(status.get("task_file", ""))) != task_path.resolve():
            continue
        mtime = status_path.stat().st_mtime
        if mtime + 2 >= started_epoch:
            matches.append((mtime, status, status_path.parent))
    if not matches:
        raise ProviderError("No se encontro status.json para la tarea de agy-bridge")
    _, status, run_dir = max(matches, key=lambda item: item[0])
    return status, run_dir


def run_antigravity(context: dict[str, Any], timeout_seconds: int = 100) -> dict[str, Any]:
    root = penta_root()
    bridge = root / "scripts" / "agent" / "agy-bridge"
    if not bridge.is_file():
        raise ProviderError(f"Falta wrapper canonico: {bridge}")
    queue = root.parent / ".agents" / "queue"
    queue.mkdir(parents=True, exist_ok=True)
    task_path = queue / f"difusion-copy-{context['ref']}-{int(time.time())}.md"
    prompt = _prompt(context)
    task_text = """# Public social-copy task

Use only the public metadata in this request. Do not browse or modify files.
Return the required AGY_RESULT block and add one extra single-line field:
copy_payload_json: <the exact compact JSON object requested below>

""" + prompt
    task_path.write_text(task_text, encoding="utf-8")
    started_epoch = time.time()
    process = subprocess.run(
        [
            str(bridge),
            "run",
            "--caller",
            "human",
            "--mode",
            "explain",
            "--timeout",
            f"{timeout_seconds}s",
            "--public-export",
            str(task_path),
        ],
        cwd=root,
        text=True,
        capture_output=True,
        timeout=timeout_seconds + 20,
        check=False,
    )
    status, run_dir = _find_agy_run(task_path, started_epoch)
    result_path = run_dir / "result.md"
    if process.returncode != 0 or status.get("status") != "success":
        raise ProviderError(f"agy-bridge: {status.get('status', 'failed')} (exit {process.returncode})")
    return _parse_json(result_path.read_text(encoding="utf-8"))


def _litellm_ready(timeout: float = 2.0) -> bool:
    try:
        with urllib.request.urlopen("http://127.0.0.1:4000/health/readiness", timeout=timeout) as response:
            return 200 <= response.status < 300
    except (urllib.error.URLError, TimeoutError):
        return False


def run_deepseek(context: dict[str, Any], timeout_seconds: int = 70) -> dict[str, Any]:
    if not _litellm_ready():
        raise ProviderError("LiteLLM no esta listo en 127.0.0.1:4000")
    delegate = penta_root() / "ai-sidecars" / "litellm" / "scripts" / "ai-delegate"
    if not delegate.is_file():
        raise ProviderError(f"Falta wrapper canonico: {delegate}")
    process = subprocess.run(
        [str(delegate), "cheap-code"],
        input=_prompt(context),
        cwd=penta_root(),
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    if process.returncode != 0:
        raise ProviderError(f"DeepSeek wrapper fallo (exit {process.returncode})")
    return _parse_json(process.stdout)


def run_claude(context: dict[str, Any], timeout_seconds: int = 100) -> dict[str, Any]:
    executable = shutil.which("claude")
    if not executable:
        raise ProviderError("Claude Code CLI no esta en PATH")
    handoff = (
        "HANDOFF-TRACE: human le solicita apoyo a claude (model: sonnet) via CLI\n"
        'MODEL-REPORT: {"agent":"claude","provider":"anthropic","model":"sonnet","source":"expected"}\n\n'
        + _prompt(context)
    )
    process = subprocess.run(
        [
            executable,
            "-p",
            "--permission-mode",
            "dontAsk",
            "--tools",
            "",
            "--output-format",
            "text",
            "--max-turns",
            "1",
            "--model",
            "sonnet",
            handoff,
        ],
        text=True,
        capture_output=True,
        timeout=timeout_seconds,
        check=False,
    )
    if process.returncode != 0:
        raise ProviderError(f"Claude Code CLI fallo (exit {process.returncode})")
    return _parse_json(process.stdout)


PROVIDERS = {
    "antigravity": run_antigravity,
    "deepseek": run_deepseek,
    "claude": run_claude,
}


def generate_copies(context: dict[str, Any], provider: str = "auto") -> ProviderOutcome:
    if provider == "manual":
        return ProviderOutcome("manual", None, [])
    order = list(PROVIDERS) if provider == "auto" else [provider]
    unknown = [name for name in order if name not in PROVIDERS]
    if unknown:
        raise ProviderError(f"Proveedor desconocido: {unknown[0]}")
    attempts: list[dict[str, Any]] = []
    for name in order:
        started = time.monotonic()
        try:
            payload = PROVIDERS[name](context)
        except (OSError, subprocess.SubprocessError, ProviderError) as exc:
            attempts.append(_attempt(name, "failed", started, str(exc)))
            continue
        attempts.append(_attempt(name, "success", started))
        return ProviderOutcome(name, payload, attempts)
    return ProviderOutcome("manual", None, attempts)
