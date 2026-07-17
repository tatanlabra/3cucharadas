from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from typing import Any, Literal

Network = Literal["mastodon", "bluesky"]
Language = Literal["es", "en"]


def utc_now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


@dataclass(slots=True)
class PostMetadata:
    path: str
    ref: str
    lang: Language
    title: str
    description: str
    tags: list[str]
    categories: list[str]
    canonical_url: str
    image_url: str
    distribution: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Message:
    network: Network
    lang: Language
    role: Literal["root", "reply"]
    text: str
    target_url: str
    approved: bool = False
    warnings: list[str] = field(default_factory=list)


@dataclass(slots=True)
class Draft:
    schema_version: int
    ref: str
    provider: str
    draft_revision: int
    created_at: str
    updated_at: str
    status: str
    posts: dict[str, PostMetadata]
    messages: dict[str, dict[str, Message]]
    base_copy: dict[str, str]
    approvals: dict[str, bool]
    limits: dict[str, int]
    provider_attempts: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, raw: dict[str, Any]) -> "Draft":
        posts = {lang: PostMetadata(**value) for lang, value in raw["posts"].items()}
        messages = {
            network: {lang: Message(**value) for lang, value in localized.items()}
            for network, localized in raw["messages"].items()
        }
        base_copy = raw.get("base_copy")
        if not isinstance(base_copy, dict):
            # Compatibilidad con borradores v1: Bluesky contenia la variante
            # sin URL y es la mejor aproximacion al mensaje editorial base.
            base_copy = {
                lang: messages["bluesky"][lang].text
                for lang in ("es", "en")
            }
        return cls(
            schema_version=int(raw["schema_version"]),
            ref=str(raw["ref"]),
            provider=str(raw["provider"]),
            draft_revision=int(raw["draft_revision"]),
            created_at=str(raw["created_at"]),
            updated_at=str(raw["updated_at"]),
            status=str(raw["status"]),
            posts=posts,
            messages=messages,
            base_copy={lang: str(base_copy.get(lang, "")) for lang in ("es", "en")},
            approvals={key: bool(value) for key, value in raw["approvals"].items()},
            limits={key: int(value) for key, value in raw["limits"].items()},
            provider_attempts=list(raw.get("provider_attempts", [])),
        )


@dataclass(slots=True)
class PublishResult:
    network: Network
    status: Literal["published", "partial", "dry_run", "failed", "skipped"]
    root_id: str = ""
    root_url: str = ""
    reply_id: str = ""
    reply_url: str = ""
    error: str = ""

    def to_dict(self) -> dict[str, str]:
        return asdict(self)
