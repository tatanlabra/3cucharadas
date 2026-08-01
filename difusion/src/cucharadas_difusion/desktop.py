from __future__ import annotations

import shutil
import subprocess
import threading


def open_url(url: str) -> bool:
    executable = shutil.which("xdg-open")
    if not executable:
        return False
    try:
        subprocess.Popen(
            [executable, url],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError:
        return False
    return True


def notify_ready(ref: str, url: str) -> bool:
    executable = shutil.which("notify-send")
    if not executable:
        return False
    try:
        process = subprocess.Popen(
            [
                executable,
                "--app-name=3cucharadas-difusion",
                "--icon=mail-send",
                "--urgency=normal",
                "--action=open=Ver revisión",
                "3cucharadas · Difusión",
                f"{ref}: previsualización lista (4 publicaciones)",
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            start_new_session=True,
        )
    except OSError:
        return False

    def wait_for_action() -> None:
        output = process.stdout.read().strip() if process.stdout else ""
        if output == "open":
            open_url(url)

    threading.Thread(target=wait_for_action, daemon=True).start()
    return True


def notify_status(ref: str, status: str, detail: str = "") -> bool:
    executable = shutil.which("notify-send")
    if not executable:
        return False
    urgency = "critical" if status in {"failed", "partial"} else "normal"
    body = f"{ref}: {status}"
    if detail:
        body += f" — {detail}"
    try:
        subprocess.Popen(
            [
                executable,
                "--app-name=3cucharadas-difusion",
                f"--urgency={urgency}",
                "3cucharadas · Difusión",
                body,
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )
    except OSError:
        return False
    return True
