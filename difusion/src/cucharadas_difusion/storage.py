from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

from .models import Draft, utc_now


class StorageError(RuntimeError):
    pass


class StaleRevisionError(StorageError):
    pass


def default_state_dir() -> Path:
    override = os.environ.get("CUCHARADAS_DIFUSION_STATE_DIR")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".local" / "state" / "3cucharadas-difusion"


class Storage:
    def __init__(self, root: Path | None = None) -> None:
        self.root = (root or default_state_dir()).expanduser()
        self.drafts_dir = self.root / "drafts"
        self.ledger_path = self.root / "ledger.jsonl"
        self._ensure_dirs()

    def _ensure_dirs(self) -> None:
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        self.drafts_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        for directory in (self.root, self.drafts_dir):
            try:
                os.chmod(directory, 0o700)
            except OSError:
                # Los comandos estrictamente read-only (preview/doctor) deben
                # seguir funcionando en sandboxes que montan $HOME sin escritura.
                pass

    @staticmethod
    def _safe_ref(ref: str) -> str:
        safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", ref).strip("-.")
        if not safe or safe != ref:
            raise StorageError(f"ref no seguro: {ref!r}")
        return safe

    def draft_path(self, ref: str) -> Path:
        return self.drafts_dir / f"{self._safe_ref(ref)}.json"

    def load_draft(self, ref: str) -> Draft:
        path = self.draft_path(ref)
        if not path.exists():
            raise StorageError(f"No existe borrador para {ref}")
        return Draft.from_dict(json.loads(path.read_text(encoding="utf-8")))

    def save_draft(self, draft: Draft, expected_revision: int | None = None) -> Draft:
        path = self.draft_path(draft.ref)
        if path.exists() and expected_revision is not None:
            current = Draft.from_dict(json.loads(path.read_text(encoding="utf-8")))
            if current.draft_revision != expected_revision:
                raise StaleRevisionError(
                    f"Revision obsoleta: esperada {expected_revision}, actual {current.draft_revision}"
                )
            draft.draft_revision = current.draft_revision + 1
        elif path.exists():
            current = Draft.from_dict(json.loads(path.read_text(encoding="utf-8")))
            draft.draft_revision = current.draft_revision + 1
        else:
            draft.draft_revision = max(1, draft.draft_revision)

        draft.updated_at = utc_now()
        payload = json.dumps(draft.to_dict(), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        tmp = path.with_suffix(".json.tmp")
        with tmp.open("w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(tmp, 0o600)
        os.replace(tmp, path)
        return draft

    def append_event(self, event: dict[str, Any]) -> None:
        record = {"timestamp": utc_now(), **event}
        line = json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n"
        fd = os.open(self.ledger_path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
        try:
            os.write(fd, line.encode("utf-8"))
            os.fsync(fd)
        finally:
            os.close(fd)

    def events(self, ref: str | None = None) -> list[dict[str, Any]]:
        if not self.ledger_path.exists():
            return []
        rows: list[dict[str, Any]] = []
        for line in self.ledger_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if ref is None or row.get("ref") == ref:
                rows.append(row)
        return rows

    def published_networks(self, ref: str) -> set[str]:
        published: set[str] = set()
        for row in self.events(ref):
            network = str(row.get("network", ""))
            if row.get("event") == "network_published":
                published.add(network)
            elif row.get("event") == "network_rolled_back":
                published.discard(network)
        return published

    def latest_publish_event(self, ref: str, network: str) -> dict[str, Any] | None:
        for row in reversed(self.events(ref)):
            if row.get("network") != network:
                continue
            if row.get("event") == "network_rolled_back":
                return None
            if row.get("event") in {"network_published", "network_publish_partial"}:
                return row
        return None

    def latest_partial_event(self, ref: str, network: str) -> dict[str, Any] | None:
        for row in reversed(self.events(ref)):
            if row.get("network") != network:
                continue
            if row.get("event") == "network_published":
                return None
            if row.get("event") == "network_rolled_back":
                return None
            if row.get("event") == "network_publish_partial":
                return row
        return None
