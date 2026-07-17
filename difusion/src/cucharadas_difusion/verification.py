from __future__ import annotations

import json
import time
import urllib.parse
import urllib.request
from typing import Any, Callable

from .networks import ProgressCallback
from .posts import extract_hashtags
from .storage import Storage


class VerificationError(RuntimeError):
    pass


JsonFetcher = Callable[[str], dict[str, Any]]


def _fetch_json(url: str, timeout: float = 15.0) -> dict[str, Any]:
    request = urllib.request.Request(url, headers={"User-Agent": "3cucharadas-difusion/0.2"})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))
    if not isinstance(payload, dict):
        raise VerificationError(f"Respuesta JSON invalida desde {urllib.parse.urlsplit(url).netloc}")
    return payload


def _latest_result(storage: Storage, ref: str, network: str) -> dict[str, Any]:
    event = storage.latest_publish_event(ref, network)
    if event is None or not isinstance(event.get("result"), dict):
        raise VerificationError(f"Falta publicacion registrada para {network}")
    return event["result"]


def _verify_mastodon(storage: Storage, ref: str, draft: Any, fetch: JsonFetcher) -> dict[str, Any]:
    result = _latest_result(storage, ref, "mastodon")
    root_id = str(result.get("root_id", ""))
    reply_id = str(result.get("reply_id", ""))
    if not root_id or not reply_id:
        raise VerificationError("Mastodon no tiene los dos IDs del hilo")
    instance = str(result.get("root_url", "https://mastodon.social")).split("/@", 1)[0]
    root = fetch(f"{instance}/api/v1/statuses/{urllib.parse.quote(root_id)}")
    reply = fetch(f"{instance}/api/v1/statuses/{urllib.parse.quote(reply_id)}")
    checks = {
        "root_language": root.get("language") == "es",
        "reply_language": reply.get("language") == "en",
        "root_position": root.get("in_reply_to_id") is None,
        "reply_position": str(reply.get("in_reply_to_id", "")) == root_id,
        "root_card": (root.get("card") or {}).get("url") == draft.messages["mastodon"]["es"].target_url,
        "reply_card": (reply.get("card") or {}).get("url") == draft.messages["mastodon"]["en"].target_url,
        "root_image": bool((root.get("card") or {}).get("image")),
        "reply_image": bool((reply.get("card") or {}).get("image")),
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise VerificationError("Mastodon no confirmo: " + ", ".join(failed))
    return {
        "status": "verified",
        "root_url": str(root.get("url", result.get("root_url", ""))),
        "reply_url": str(reply.get("url", result.get("reply_url", ""))),
        "checks": checks,
    }


def _bsky_post(uri: str, fetch: JsonFetcher) -> dict[str, Any]:
    endpoint = "https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts?uris="
    payload = fetch(endpoint + urllib.parse.quote(uri, safe=""))
    posts = payload.get("posts")
    if not isinstance(posts, list) or not posts:
        raise VerificationError(f"Bluesky no devolvio {uri}")
    return posts[0]


def _verify_bluesky(storage: Storage, ref: str, draft: Any, fetch: JsonFetcher) -> dict[str, Any]:
    result = _latest_result(storage, ref, "bluesky")
    root_uri = str(result.get("root_id", ""))
    reply_uri = str(result.get("reply_id", ""))
    if not root_uri or not reply_uri:
        raise VerificationError("Bluesky no tiene los dos URI del hilo")
    root = _bsky_post(root_uri, fetch)
    reply = _bsky_post(reply_uri, fetch)
    root_record = root.get("record") or {}
    reply_record = reply.get("record") or {}
    reply_ref = reply_record.get("reply") or {}

    def embed(record: dict[str, Any]) -> dict[str, Any]:
        return (record.get("embed") or {}).get("external") or {}

    def tags(record: dict[str, Any]) -> list[str]:
        return [
            str(feature.get("tag"))
            for facet in record.get("facets") or []
            for feature in facet.get("features") or []
            if feature.get("$type") == "app.bsky.richtext.facet#tag"
        ]

    expected_root_tags = [tag[1:] for tag in extract_hashtags(draft.messages["bluesky"]["es"].text)]
    expected_reply_tags = [tag[1:] for tag in extract_hashtags(draft.messages["bluesky"]["en"].text)]
    checks = {
        "root_text": root_record.get("text") == draft.messages["bluesky"]["es"].text,
        "reply_text": reply_record.get("text") == draft.messages["bluesky"]["en"].text,
        "root_language": root_record.get("langs") == ["es"],
        "reply_language": reply_record.get("langs") == ["en"],
        "root_position": root_record.get("reply") is None,
        "reply_parent": (reply_ref.get("parent") or {}).get("uri") == root_uri,
        "reply_root": (reply_ref.get("root") or {}).get("uri") == root_uri,
        "root_card": embed(root_record).get("uri") == draft.messages["bluesky"]["es"].target_url,
        "reply_card": embed(reply_record).get("uri") == draft.messages["bluesky"]["en"].target_url,
        "root_image": bool(embed(root_record).get("thumb")),
        "reply_image": bool(embed(reply_record).get("thumb")),
        "root_facets": tags(root_record) == expected_root_tags,
        "reply_facets": tags(reply_record) == expected_reply_tags,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise VerificationError("Bluesky no confirmo: " + ", ".join(failed))
    return {
        "status": "verified",
        "root_url": str(result.get("root_url", "")),
        "reply_url": str(result.get("reply_url", "")),
        "checks": checks,
    }


def verify_publication(
    storage: Storage,
    ref: str,
    *,
    progress: ProgressCallback | None = None,
    fetch: JsonFetcher = _fetch_json,
    attempts: int = 3,
    sleeper: Callable[[float], None] = time.sleep,
) -> dict[str, Any]:
    if progress:
        progress("verification", "in_progress", "consultando APIs publicas", "")
    draft = storage.load_draft(ref)
    errors: list[str] = []
    networks: dict[str, Any] = {}
    for attempt in range(max(1, attempts)):
        errors = []
        networks = {}
        for network, verifier in (("mastodon", _verify_mastodon), ("bluesky", _verify_bluesky)):
            try:
                networks[network] = verifier(storage, ref, draft, fetch)
            except Exception as exc:
                errors.append(f"{network}: {type(exc).__name__}: {exc}")
        if not errors:
            break
        if attempt + 1 < attempts:
            sleeper(2.0 * (attempt + 1))

    verified = not errors
    status = "published_verified" if verified else "published_unverified"
    refreshed = storage.load_draft(ref)
    refreshed.status = status
    saved = storage.save_draft(refreshed, expected_revision=refreshed.draft_revision)
    event = {
        "event": "publication_verified" if verified else "publication_verification_failed",
        "ref": ref,
        "revision": saved.draft_revision,
        "status": status,
        "networks": networks,
        "errors": errors,
    }
    storage.append_event(event)
    if progress:
        progress(
            "verification",
            "success" if verified else "failed",
            "publicacion publica confirmada" if verified else "; ".join(errors)[:500],
            "",
        )
    return {
        "status": status,
        "draft_revision": saved.draft_revision,
        "networks": networks,
        "errors": errors,
    }
