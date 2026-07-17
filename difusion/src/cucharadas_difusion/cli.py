from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import sys
from pathlib import Path
from typing import Any

from .destinations import destination_checklist, destination_status
from .models import Draft
from .networks import (
    MastodonClient,
    PublishError,
    Publisher,
    authenticate_accounts,
    load_secrets,
    secrets_path,
)
from .posts import (
    PostError,
    check_public_urls,
    create_draft,
    find_pair,
    public_prompt_context,
    validate_draft,
)
from .providers import generate_copies, penta_root
from .storage import Storage, StorageError
from .web import run_review
from .verification import verify_publication


def resolve_repo(value: str | None = None) -> Path:
    if value:
        candidate = Path(value).expanduser().resolve()
        if (candidate / "_config.yml").is_file() and (candidate / "_posts").is_dir():
            return candidate
        raise PostError(f"No parece un repo 3cucharadas: {candidate}")
    env_value = os.environ.get("CUCHARADAS_REPO")
    if env_value:
        return resolve_repo(env_value)
    for start in (Path.cwd(), Path(__file__).resolve().parents[3]):
        for candidate in (start, *start.parents):
            if (candidate / "_config.yml").is_file() and (candidate / "_posts").is_dir():
                return candidate
    raise PostError("No se pudo localizar el repo de 3cucharadas; usa --repo")


def _storage(args: argparse.Namespace) -> Storage:
    return Storage(Path(args.state_dir).expanduser() if args.state_dir else None)


def _secrets(args: argparse.Namespace) -> dict[str, str]:
    return load_secrets(Path(args.secrets).expanduser() if args.secrets else None)


def cmd_doctor(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    values = _secrets(args)
    checks: list[tuple[str, str, str]] = []

    version_ok = (3, 12) <= sys.version_info[:2] < (3, 14)
    checks.append(("python", "ok" if version_ok else "error", sys.version.split()[0]))
    checks.append(("repo", "ok", str(repo)))
    checks.append(("penta-agent", "ok" if penta_root().is_dir() else "error", str(penta_root())))
    for command in ("agy", "claude", "notify-send", "xdg-open"):
        checks.append((command, "ok" if shutil.which(command) else "warning", shutil.which(command) or "no disponible"))
    bridge = penta_root() / "scripts" / "agent" / "agy-bridge"
    delegate = penta_root() / "ai-sidecars" / "litellm" / "scripts" / "ai-delegate"
    checks.append(("agy-bridge", "ok" if bridge.is_file() else "error", str(bridge)))
    checks.append(("ai-delegate", "ok" if delegate.is_file() else "error", str(delegate)))

    try:
        import fastapi  # noqa: F401
        import uvicorn  # noqa: F401
        import yaml  # noqa: F401
    except ImportError as exc:
        checks.append(("python-deps", "error", str(exc)))
    else:
        checks.append(("python-deps", "ok", "FastAPI, Uvicorn, PyYAML"))
    try:
        import atproto  # noqa: F401
    except ImportError:
        checks.append(("atproto", "warning", "necesario solo para publicacion live"))
    else:
        checks.append(("atproto", "ok", "instalado"))

    secret_file = Path(args.secrets).expanduser() if args.secrets else secrets_path()
    if secret_file.exists():
        mode = stat.S_IMODE(secret_file.stat().st_mode)
        checks.append(("secrets-mode", "ok" if mode == 0o600 else "error", oct(mode)))
    else:
        checks.append(("secrets", "warning", f"crear {secret_file}"))
    for key in ("MASTODON_TOKEN", "BSKY_HANDLE", "BSKY_APP_PASSWORD"):
        checks.append((key, "ok" if values.get(key) else "warning", "configurado" if values.get(key) else "ausente"))
    if args.auth:
        try:
            accounts = authenticate_accounts(values)
        except Exception as exc:
            detail = f"{type(exc).__name__}: {exc}"
            for key in ("MASTODON_TOKEN", "BSKY_APP_PASSWORD"):
                if values.get(key):
                    detail = detail.replace(values[key], "[REDACTED]")
            checks.append(("social-auth", "error", detail[:300]))
        else:
            checks.append(
                (
                    "social-auth",
                    "ok",
                    f"mastodon={accounts['mastodon']} bluesky={accounts['bluesky']}",
                )
            )

    mastodon = MastodonClient(values)
    checks.append(("mastodon-limit", "ok", str(mastodon.discover_limit())))
    try:
        import urllib.request

        with urllib.request.urlopen("http://127.0.0.1:4000/health/readiness", timeout=1.5) as response:
            ready = 200 <= response.status < 300
    except Exception:
        ready = False
    checks.append(("litellm", "ok" if ready else "warning", "listo" if ready else "detenido; se omitira DeepSeek"))

    width = max(len(name) for name, _, _ in checks)
    for name, status, detail in checks:
        print(f"{name:<{width}}  {status:<7}  {detail}")
    return 1 if any(status == "error" for _, status, _ in checks) else 0


def cmd_prepare(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    storage = _storage(args)
    source = Path(args.post)
    if not source.is_absolute():
        source = repo / source
    posts = find_pair(repo, source.resolve())
    if not args.skip_url_check:
        results = check_public_urls(posts)
        print("URLs publicas:", ", ".join(f"{key}={value}" for key, value in results.items()))
    existing = storage.draft_path(posts["es"].ref)
    if existing.exists() and not args.force:
        raise StorageError(f"Ya existe {existing}; usa review o prepare --force")
    limit = MastodonClient(_secrets(args)).discover_limit()
    outcome = generate_copies(public_prompt_context(posts), args.provider)
    draft = create_draft(posts, outcome.provider, outcome.payload, outcome.attempts, mastodon_limit=limit)
    saved = storage.save_draft(draft)
    storage.append_event(
        {
            "event": "draft_prepared",
            "ref": saved.ref,
            "revision": saved.draft_revision,
            "provider": saved.provider,
            "attempts": saved.provider_attempts,
        }
    )
    print(f"Borrador: {storage.draft_path(saved.ref)}")
    if saved.provider == "manual":
        print("Los proveedores no entregaron un payload valido; completa los textos en la GUI.", file=sys.stderr)
    if not args.no_review:
        run_review(saved.ref, storage, open_browser=not args.no_open)
    return 0


def cmd_review(args: argparse.Namespace) -> int:
    storage = _storage(args)
    storage.load_draft(args.ref)
    run_review(args.ref, storage, open_browser=not args.no_open)
    return 0


def _preview_text(draft: Draft) -> str:
    lines = [f"ref={draft.ref} provider={draft.provider} revision={draft.draft_revision}"]
    for network in ("mastodon", "bluesky"):
        lines.append(f"\n[{network.upper()}]")
        for lang in ("es", "en"):
            message = draft.messages[network][lang]
            lines.extend([f"{lang.upper()} {message.role}:", message.text, f"CARD: {message.target_url}"])
            for warning in message.warnings:
                lines.append(f"WARN: {warning}")
    return "\n".join(lines) + "\n"


def cmd_preview(args: argparse.Namespace) -> int:
    draft = _storage(args).load_draft(args.ref)
    validate_draft(draft)
    if args.format == "json":
        print(json.dumps(draft.to_dict(), ensure_ascii=False, indent=2))
    else:
        print(_preview_text(draft), end="")
    return 0


def _confirm_live(ref: str, supplied: str | None = None) -> None:
    confirmation = supplied
    if confirmation is None:
        confirmation = input(f"Escribe PUBLICAR {ref}: ")
    if confirmation != f"PUBLICAR {ref}":
        raise PublishError("Confirmacion incorrecta")


def _publish(args: argparse.Namespace) -> int:
    storage = _storage(args)
    draft = storage.load_draft(args.ref)
    if args.live:
        _confirm_live(args.ref, args.confirm)
    results = Publisher(storage, _secrets(args)).publish(draft, live=args.live)
    failed = any(result.status in {"failed", "partial"} for result in results)
    if args.live and not failed:
        verification = verify_publication(storage, args.ref)
        print(
            json.dumps(
                {"results": [result.to_dict() for result in results], "verification": verification},
                ensure_ascii=False,
                indent=2,
            )
        )
        return 0 if verification["status"] == "published_verified" else 1
    print(json.dumps([result.to_dict() for result in results], ensure_ascii=False, indent=2))
    return 1 if failed else 0


def cmd_verify(args: argparse.Namespace) -> int:
    result = verify_publication(_storage(args), args.ref)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "published_verified" else 1


def cmd_rollback(args: argparse.Namespace) -> int:
    storage = _storage(args)
    if args.live:
        expected = f"BORRAR {args.ref} {args.network}"
        confirmation = args.confirm or input(f"Escribe {expected}: ")
        if confirmation != expected:
            raise PublishError("Confirmacion incorrecta")
    result = Publisher(storage, _secrets(args)).rollback(args.ref, args.network, live=args.live)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    return 0


def cmd_destinations(args: argparse.Namespace) -> int:
    repo = resolve_repo(args.repo)
    if args.destination_command == "checklist":
        print(destination_checklist(repo, args.ref), end="")
    else:
        rows = destination_status(repo, args.ref)
        print(json.dumps(rows, ensure_ascii=False, indent=2) if args.json else "\n".join(
            f"{row['destination']:<18} {row['status']:<10} {row['reason']}" for row in rows
        ))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="cucharadas-difusion")
    parser.add_argument("--repo", help="Ruta al repo 3cucharadas")
    parser.add_argument("--state-dir", help="Sobrescribe el state dir XDG")
    parser.add_argument("--secrets", help="Sobrescribe el archivo secrets.env")
    commands = parser.add_subparsers(dest="command", required=True)

    doctor = commands.add_parser("doctor", help="Diagnostico sin mostrar secretos")
    doctor.add_argument("--auth", action="store_true", help="Autentica ambas cuentas sin publicar")
    doctor.set_defaults(func=cmd_doctor)

    prepare = commands.add_parser("prepare", help="Genera borrador y abre la revision")
    prepare.add_argument("post")
    prepare.add_argument("--provider", choices=["auto", "antigravity", "deepseek", "claude", "manual"], default="auto")
    prepare.add_argument("--skip-url-check", action="store_true")
    prepare.add_argument("--force", action="store_true")
    prepare.add_argument("--no-open", action="store_true")
    prepare.add_argument("--no-review", action="store_true", help="Solo genera el borrador")
    prepare.set_defaults(func=cmd_prepare)

    review = commands.add_parser("review", help="Reabre la GUI de un borrador")
    review.add_argument("ref")
    review.add_argument("--no-open", action="store_true")
    review.set_defaults(func=cmd_review)

    preview = commands.add_parser("preview", help="Previsualizacion en terminal")
    preview.add_argument("ref")
    preview.add_argument("--format", choices=["text", "json"], default="text")
    preview.set_defaults(func=cmd_preview)

    verify = commands.add_parser("verify", help="Confirma hilo, idioma, tarjetas y facets publicados")
    verify.add_argument("ref")
    verify.set_defaults(func=cmd_verify)

    for name in ("publish", "resume"):
        publish = commands.add_parser(name, help="Dry-run por defecto; --live escribe en redes")
        publish.add_argument("ref")
        publish.add_argument("--live", action="store_true")
        publish.add_argument("--confirm", help=argparse.SUPPRESS)
        publish.set_defaults(func=_publish)

    rollback = commands.add_parser("rollback", help="Dry-run por defecto")
    rollback.add_argument("ref")
    rollback.add_argument("--network", choices=["mastodon", "bluesky"], required=True)
    rollback.add_argument("--live", action="store_true")
    rollback.add_argument("--confirm", help=argparse.SUPPRESS)
    rollback.set_defaults(func=cmd_rollback)

    destinations = commands.add_parser("destinations")
    dest_commands = destinations.add_subparsers(dest="destination_command", required=True)
    status_cmd = dest_commands.add_parser("status")
    status_cmd.add_argument("ref")
    status_cmd.add_argument("--json", action="store_true")
    status_cmd.set_defaults(func=cmd_destinations)
    checklist = dest_commands.add_parser("checklist")
    checklist.add_argument("ref")
    checklist.set_defaults(func=cmd_destinations)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except KeyboardInterrupt:
        print("\nRevision cerrada; el borrador local permanece guardado.", file=sys.stderr)
        return 130
    except (OSError, PostError, PublishError, StorageError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
