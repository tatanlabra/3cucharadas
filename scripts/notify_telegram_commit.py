#!/usr/bin/env python3
"""Send a Telegram notification for the latest successful local commit."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from pathlib import Path


TIMEOUT_SECONDS = 10


def _git_output(args: list[str], cwd: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            cwd=cwd,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError):
        return ""


def _repo_root(cwd: Path) -> Path:
    root = _git_output(["rev-parse", "--show-toplevel"], cwd)
    return Path(root) if root else cwd.resolve()


def _first_line(value: str) -> str:
    return value.splitlines()[0].strip() if value else ""


def _build_message(repo_root: Path) -> str:
    repo = repo_root.name
    branch = _git_output(["branch", "--show-current"], repo_root) or "detached"
    short_hash = _git_output(["rev-parse", "--short", "HEAD"], repo_root) or "unknown"
    subject = _first_line(_git_output(["log", "-1", "--pretty=%s"], repo_root))
    subject_part = f" {subject}" if subject else ""

    return "\n".join(
        [
            "3cucharadas: commit local",
            f"Repo: {repo}",
            f"Branch: {branch}",
            f"Commit: {short_hash}{subject_part}",
            "Hook: post-commit",
        ]
    )


def _send_message(token: str, chat_id: str, text: str) -> bool:
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = urllib.parse.urlencode(
        {
            "chat_id": chat_id,
            "text": text,
            "disable_web_page_preview": "true",
        }
    ).encode("utf-8")

    request = urllib.request.Request(url, data=payload, method="POST")
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            body = response.read().decode("utf-8")
    except Exception:
        return False

    try:
        parsed = json.loads(body)
    except json.JSONDecodeError:
        return False

    return bool(parsed.get("ok"))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Notify a Telegram chat about the latest local commit.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root or any path inside the repository.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate environment and build the message without sending it.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    token = os.environ.get("EPUB_CURATOR_TG_TOKEN", "").strip()
    chat_id = os.environ.get("EPUB_CURATOR_TG_CHAT_ID", "").strip()
    if not token or not chat_id:
        print("telegram-missing-env")
        return 2

    repo_root = _repo_root(Path(args.repo_root).resolve())
    message = _build_message(repo_root)
    if args.dry_run:
        print("telegram-dry-run-ok")
        return 0

    if _send_message(token, chat_id, message):
        print("telegram-sent")
        return 0

    print("telegram-send-failed")
    return 1


if __name__ == "__main__":
    sys.exit(main())
