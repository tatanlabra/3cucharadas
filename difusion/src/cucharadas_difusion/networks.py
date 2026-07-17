from __future__ import annotations

import hashlib
import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any, Callable, Protocol

from .models import Draft, PublishResult
from .posts import SUPPORTED_NETWORKS, validate_draft
from .storage import Storage


class PublishError(RuntimeError):
    pass


class PartialPublishError(PublishError):
    def __init__(self, result: PublishResult, cause: Exception) -> None:
        super().__init__(str(cause))
        self.result = result
        self.cause = cause


ProgressCallback = Callable[[str, str, str, str], None]


def _emit(
    progress: ProgressCallback | None,
    step: str,
    status: str,
    detail: str = "",
    url: str = "",
) -> None:
    if progress is not None:
        progress(step, status, detail, url)


def secrets_path() -> Path:
    override = os.environ.get("CUCHARADAS_DIFUSION_SECRETS")
    if override:
        return Path(override).expanduser()
    return Path.home() / ".config" / "3cucharadas-difusion" / "secrets.env"


def load_secrets(path: Path | None = None) -> dict[str, str]:
    target = path or secrets_path()
    values = dict(os.environ)
    if not target.exists():
        return values
    for raw_line in target.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values.setdefault(key.strip(), value.strip().strip("'\""))
    return values


def _required(values: dict[str, str], *keys: str) -> None:
    missing = [key for key in keys if not values.get(key)]
    if missing:
        raise PublishError("Faltan credenciales: " + ", ".join(missing))


def authenticate_accounts(values: dict[str, str]) -> dict[str, str]:
    """Authenticate without creating or modifying social records."""
    _required(values, "MASTODON_TOKEN", "BSKY_HANDLE", "BSKY_APP_PASSWORD")
    instance = values.get("MASTODON_INSTANCE", "https://mastodon.social").rstrip("/")
    request = urllib.request.Request(
        f"{instance}/api/v1/accounts/verify_credentials",
        headers={
            "Authorization": f"Bearer {values['MASTODON_TOKEN']}",
            "User-Agent": "3cucharadas-difusion/0.2",
        },
    )
    with urllib.request.urlopen(request, timeout=15) as response:
        mastodon = json.loads(response.read().decode("utf-8"))
    client = BlueskyClient(values)._client()
    profile = client.get_profile(values["BSKY_HANDLE"])
    return {
        "mastodon": str(mastodon.get("acct", "")),
        "bluesky": str(profile.handle),
    }


def _safe_error(exc: Exception, secrets: dict[str, str]) -> str:
    text = f"{type(exc).__name__}: {exc}"
    for key in ("MASTODON_TOKEN", "BSKY_APP_PASSWORD"):
        value = secrets.get(key, "")
        if value:
            text = text.replace(value, "[REDACTED]")
    return text[:500]


class NetworkClient(Protocol):
    network: str

    def publish_thread(
        self, draft: Draft, dry_run: bool, progress: ProgressCallback | None = None
    ) -> PublishResult: ...

    def resume_thread(
        self, draft: Draft, event: dict[str, Any], progress: ProgressCallback | None = None
    ) -> PublishResult: ...

    def rollback(self, event: dict[str, Any], dry_run: bool) -> PublishResult: ...


class MastodonClient:
    network = "mastodon"

    def __init__(self, secrets: dict[str, str]) -> None:
        self.secrets = secrets
        self.instance = secrets.get("MASTODON_INSTANCE", "https://mastodon.social").rstrip("/")

    def discover_limit(self, timeout: float = 5.0) -> int:
        request = urllib.request.Request(
            f"{self.instance}/api/v2/instance",
            headers={"User-Agent": "3cucharadas-difusion/0.1"},
        )
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                payload = json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
            return 500
        statuses = payload.get("configuration", {}).get("statuses", {})
        return int(statuses.get("max_characters") or payload.get("max_toot_chars") or 500)

    def _post(self, message: str, lang: str, idem: str, reply_to: str = "") -> dict[str, Any]:
        _required(self.secrets, "MASTODON_TOKEN")
        form = {"status": message, "language": lang}
        if reply_to:
            form["in_reply_to_id"] = reply_to
        request = urllib.request.Request(
            f"{self.instance}/api/v1/statuses",
            data=urllib.parse.urlencode(form).encode("utf-8"),
            method="POST",
            headers={
                "Authorization": f"Bearer {self.secrets['MASTODON_TOKEN']}",
                "Idempotency-Key": idem,
                "User-Agent": "3cucharadas-difusion/0.1",
            },
        )
        with urllib.request.urlopen(request, timeout=20) as response:
            return json.loads(response.read().decode("utf-8"))

    def publish_thread(
        self, draft: Draft, dry_run: bool, progress: ProgressCallback | None = None
    ) -> PublishResult:
        es = draft.messages["mastodon"]["es"]
        en = draft.messages["mastodon"]["en"]
        if dry_run:
            _emit(progress, "mastodon_es", "success", "simulacion", es.target_url)
            _emit(progress, "mastodon_en", "success", "simulacion", en.target_url)
            return PublishResult(
                network="mastodon",
                status="dry_run",
                root_id="dry-run-es",
                root_url=es.target_url,
                reply_id="dry-run-en",
                reply_url=en.target_url,
            )
        root_key = hashlib.sha256(f"{draft.ref}:mastodon:es:{es.text}".encode()).hexdigest()
        _emit(progress, "mastodon_es", "in_progress")
        try:
            root = self._post(es.text, "es", root_key)
        except Exception as exc:
            _emit(progress, "mastodon_es", "failed", _safe_error(exc, self.secrets))
            raise
        _emit(progress, "mastodon_es", "success", url=str(root.get("url", "")))
        reply_key = hashlib.sha256(f"{draft.ref}:mastodon:en:{en.text}".encode()).hexdigest()
        _emit(progress, "mastodon_en", "in_progress")
        try:
            reply = self._post(en.text, "en", reply_key, str(root["id"]))
        except Exception as exc:
            _emit(progress, "mastodon_en", "failed", _safe_error(exc, self.secrets))
            raise PartialPublishError(
                PublishResult(
                    network="mastodon",
                    status="partial",
                    root_id=str(root["id"]),
                    root_url=str(root.get("url", "")),
                    error=_safe_error(exc, self.secrets),
                ),
                exc,
            ) from exc
        _emit(progress, "mastodon_en", "success", url=str(reply.get("url", "")))
        return PublishResult(
            network="mastodon",
            status="published",
            root_id=str(root["id"]),
            root_url=str(root.get("url", "")),
            reply_id=str(reply["id"]),
            reply_url=str(reply.get("url", "")),
        )

    def resume_thread(
        self, draft: Draft, event: dict[str, Any], progress: ProgressCallback | None = None
    ) -> PublishResult:
        previous = event.get("result", {})
        root_id = str(previous.get("root_id", ""))
        if not root_id:
            raise PublishError("El estado parcial de Mastodon no tiene root_id")
        _emit(progress, "mastodon_es", "skipped", "raiz ya publicada", str(previous.get("root_url", "")))
        en = draft.messages["mastodon"]["en"]
        reply_key = hashlib.sha256(f"{draft.ref}:mastodon:en:{en.text}".encode()).hexdigest()
        _emit(progress, "mastodon_en", "in_progress")
        try:
            reply = self._post(en.text, "en", reply_key, root_id)
        except Exception as exc:
            _emit(progress, "mastodon_en", "failed", _safe_error(exc, self.secrets))
            raise
        _emit(progress, "mastodon_en", "success", url=str(reply.get("url", "")))
        return PublishResult(
            network="mastodon",
            status="published",
            root_id=root_id,
            root_url=str(previous.get("root_url", "")),
            reply_id=str(reply["id"]),
            reply_url=str(reply.get("url", "")),
        )

    def _delete(self, status_id: str) -> None:
        _required(self.secrets, "MASTODON_TOKEN")
        request = urllib.request.Request(
            f"{self.instance}/api/v1/statuses/{urllib.parse.quote(status_id)}",
            method="DELETE",
            headers={"Authorization": f"Bearer {self.secrets['MASTODON_TOKEN']}"},
        )
        with urllib.request.urlopen(request, timeout=20):
            return

    def rollback(self, event: dict[str, Any], dry_run: bool) -> PublishResult:
        result = event.get("result", {})
        if dry_run:
            return PublishResult(network="mastodon", status="dry_run")
        if result.get("reply_id"):
            self._delete(str(result["reply_id"]))
        if result.get("root_id"):
            self._delete(str(result["root_id"]))
        return PublishResult(network="mastodon", status="published")


class BlueskyClient:
    network = "bluesky"

    def __init__(self, secrets: dict[str, str]) -> None:
        self.secrets = secrets

    def _client(self) -> Any:
        _required(self.secrets, "BSKY_HANDLE", "BSKY_APP_PASSWORD")
        try:
            from atproto import Client
        except ImportError as exc:
            raise PublishError("Falta atproto==0.0.69 en el entorno") from exc
        client = Client()
        client.login(self.secrets["BSKY_HANDLE"], self.secrets["BSKY_APP_PASSWORD"])
        return client

    @staticmethod
    def _hashtag_facets(text: str, models: Any) -> list[Any]:
        """Build AT Protocol byte-indexed facets for every hashtag."""
        facets: list[Any] = []
        for match in re.finditer(r"(?<!\w)#([\w-]+)", text, flags=re.UNICODE):
            byte_start = len(text[: match.start()].encode("utf-8"))
            byte_end = len(text[: match.end()].encode("utf-8"))
            facets.append(
                models.AppBskyRichtextFacet.Main(
                    index=models.AppBskyRichtextFacet.ByteSlice(
                        byte_start=byte_start,
                        byte_end=byte_end,
                    ),
                    features=[models.AppBskyRichtextFacet.Tag(tag=match.group(1))],
                )
            )
        return facets

    @staticmethod
    def _download_card_image(url: str, timeout: float = 15.0) -> bytes:
        if not url.startswith("https://"):
            raise PublishError("La tarjeta de Bluesky requiere una imagen OG https")
        request = urllib.request.Request(url, headers={"User-Agent": "3cucharadas-difusion/0.1"})
        with urllib.request.urlopen(request, timeout=timeout) as response:
            content_type = response.headers.get_content_type()
            if not content_type.startswith("image/"):
                raise PublishError(f"La imagen OG devolvio {content_type}, no image/*")
            data = response.read(2_000_001)
        if not data:
            raise PublishError("La imagen OG de Bluesky esta vacia")
        if len(data) > 2_000_000:
            raise PublishError("La imagen OG supera el limite de 2 MB de Bluesky")
        return data

    def _external_embed(self, client: Any, models: Any, draft: Draft, lang: str) -> Any:
        post = draft.posts[lang]
        message = draft.messages["bluesky"][lang]
        if not post.image_url:
            raise PublishError(f"Falta imagen OG para la tarjeta Bluesky {lang}")
        thumb = client.upload_blob(self._download_card_image(post.image_url))
        return models.AppBskyEmbedExternal.Main(
            external=models.AppBskyEmbedExternal.External(
                uri=message.target_url,
                title=post.title,
                description=post.description[:280],
                thumb=thumb.blob,
            )
        )

    @staticmethod
    def _web_url(handle: str, uri: str) -> str:
        rkey = uri.rsplit("/", 1)[-1]
        return f"https://bsky.app/profile/{handle}/post/{rkey}"

    def publish_thread(
        self, draft: Draft, dry_run: bool, progress: ProgressCallback | None = None
    ) -> PublishResult:
        es = draft.messages["bluesky"]["es"]
        en = draft.messages["bluesky"]["en"]
        if dry_run:
            _emit(progress, "bluesky_es", "success", "simulacion", es.target_url)
            _emit(progress, "bluesky_en", "success", "simulacion", en.target_url)
            return PublishResult(
                network="bluesky",
                status="dry_run",
                root_id="at://dry-run/es",
                root_url=es.target_url,
                reply_id="at://dry-run/en",
                reply_url=en.target_url,
            )
        try:
            from atproto import models
        except ImportError as exc:
            raise PublishError("Falta atproto==0.0.69 en el entorno") from exc
        client = self._client()

        _emit(progress, "bluesky_es", "in_progress")
        try:
            root = client.send_post(
                text=es.text,
                langs=["es"],
                facets=self._hashtag_facets(es.text, models),
                embed=self._external_embed(client, models, draft, "es"),
            )
        except Exception as exc:
            _emit(progress, "bluesky_es", "failed", _safe_error(exc, self.secrets))
            raise
        root_ref = models.ComAtprotoRepoStrongRef.Main(cid=root.cid, uri=root.uri)
        reply_ref = models.AppBskyFeedPost.ReplyRef(root=root_ref, parent=root_ref)
        handle = self.secrets["BSKY_HANDLE"]
        root_url = self._web_url(handle, str(root.uri))
        _emit(progress, "bluesky_es", "success", url=root_url)
        _emit(progress, "bluesky_en", "in_progress")
        try:
            reply = client.send_post(
                text=en.text,
                langs=["en"],
                facets=self._hashtag_facets(en.text, models),
                embed=self._external_embed(client, models, draft, "en"),
                reply_to=reply_ref,
            )
        except Exception as exc:
            _emit(progress, "bluesky_en", "failed", _safe_error(exc, self.secrets))
            raise PartialPublishError(
                PublishResult(
                    network="bluesky",
                    status="partial",
                    root_id=str(root.uri),
                    root_url=self._web_url(handle, str(root.uri)),
                    error=_safe_error(exc, self.secrets),
                ),
                exc,
            ) from exc
        reply_url = self._web_url(handle, str(reply.uri))
        _emit(progress, "bluesky_en", "success", url=reply_url)
        return PublishResult(
            network="bluesky",
            status="published",
            root_id=str(root.uri),
            root_url=root_url,
            reply_id=str(reply.uri),
            reply_url=reply_url,
        )

    def resume_thread(
        self, draft: Draft, event: dict[str, Any], progress: ProgressCallback | None = None
    ) -> PublishResult:
        try:
            from atproto import models
        except ImportError as exc:
            raise PublishError("Falta atproto==0.0.69 en el entorno") from exc
        previous = event.get("result", {})
        root_uri = str(previous.get("root_id", ""))
        if not root_uri:
            raise PublishError("El estado parcial de Bluesky no tiene root URI")
        _emit(progress, "bluesky_es", "skipped", "raiz ya publicada", str(previous.get("root_url", "")))
        client = self._client()
        response = client.app.bsky.feed.get_posts({"uris": [root_uri]})
        if not response.posts:
            raise PublishError("No se pudo recuperar la raiz parcial de Bluesky")
        root_ref = models.ComAtprotoRepoStrongRef.Main(cid=response.posts[0].cid, uri=root_uri)
        reply_ref = models.AppBskyFeedPost.ReplyRef(root=root_ref, parent=root_ref)
        message = draft.messages["bluesky"]["en"]
        _emit(progress, "bluesky_en", "in_progress")
        try:
            reply = client.send_post(
                text=message.text,
                langs=["en"],
                facets=self._hashtag_facets(message.text, models),
                embed=self._external_embed(client, models, draft, "en"),
                reply_to=reply_ref,
            )
        except Exception as exc:
            _emit(progress, "bluesky_en", "failed", _safe_error(exc, self.secrets))
            raise
        handle = self.secrets["BSKY_HANDLE"]
        reply_url = self._web_url(handle, str(reply.uri))
        _emit(progress, "bluesky_en", "success", url=reply_url)
        return PublishResult(
            network="bluesky",
            status="published",
            root_id=root_uri,
            root_url=str(previous.get("root_url", self._web_url(handle, root_uri))),
            reply_id=str(reply.uri),
            reply_url=reply_url,
        )

    def rollback(self, event: dict[str, Any], dry_run: bool) -> PublishResult:
        if dry_run:
            return PublishResult(network="bluesky", status="dry_run")
        client = self._client()
        result = event.get("result", {})
        if result.get("reply_id"):
            client.delete_post(str(result["reply_id"]))
        if result.get("root_id"):
            client.delete_post(str(result["root_id"]))
        return PublishResult(network="bluesky", status="published")


class Publisher:
    def __init__(self, storage: Storage, secrets: dict[str, str] | None = None) -> None:
        self.storage = storage
        self.secrets = secrets or load_secrets()
        self.clients: dict[str, NetworkClient] = {
            "mastodon": MastodonClient(self.secrets),
            "bluesky": BlueskyClient(self.secrets),
        }

    def publish(
        self,
        draft: Draft,
        *,
        live: bool,
        networks: list[str] | None = None,
        progress: ProgressCallback | None = None,
    ) -> list[PublishResult]:
        errors = validate_draft(draft)
        if errors:
            raise PublishError("Borrador invalido: " + "; ".join(errors))
        if live and not all(draft.approvals.get(network) for network in SUPPORTED_NETWORKS):
            raise PublishError("La publicacion live exige aprobar ambas cadenas")

        selected = networks or list(SUPPORTED_NETWORKS)
        already = self.storage.published_networks(draft.ref) if live else set()
        results: list[PublishResult] = []

        def report(step: str, status: str, detail: str = "", url: str = "") -> None:
            if live:
                self.storage.append_event(
                    {
                        "event": "publication_step",
                        "ref": draft.ref,
                        "step": step,
                        "status": status,
                        "detail": detail,
                        "url": url,
                    }
                )
            _emit(progress, step, status, detail, url)

        for network in selected:
            if network not in self.clients:
                raise PublishError(f"Red desconocida: {network}")
            if network in already:
                event = self.storage.latest_publish_event(draft.ref, network) or {}
                previous = event.get("result", {})
                for lang, key in (("es", "root_url"), ("en", "reply_url")):
                    report(f"{network}_{lang}", "skipped", "ya publicado", str(previous.get(key, "")))
                results.append(
                    PublishResult(
                        network=network,  # type: ignore[arg-type]
                        status="skipped",
                        root_id=str(previous.get("root_id", "")),
                        root_url=str(previous.get("root_url", "")),
                        reply_id=str(previous.get("reply_id", "")),
                        reply_url=str(previous.get("reply_url", "")),
                    )
                )
                continue
            self.storage.append_event(
                {"event": "network_publish_started", "ref": draft.ref, "network": network, "live": live}
            )
            try:
                partial = self.storage.latest_partial_event(draft.ref, network) if live else None
                if partial is not None:
                    result = self.clients[network].resume_thread(draft, partial, report)
                else:
                    result = self.clients[network].publish_thread(draft, dry_run=not live, progress=report)
            except PartialPublishError as exc:
                result = exc.result
                self.storage.append_event(
                    {
                        "event": "network_publish_partial",
                        "ref": draft.ref,
                        "network": network,
                        "result": result.to_dict(),
                        "error": result.error,
                    }
                )
            except Exception as exc:  # la frontera de red debe convertir cualquier SDK/HTTP error
                result = PublishResult(
                    network=network,  # type: ignore[arg-type]
                    status="failed",
                    error=_safe_error(exc, self.secrets),
                )
                self.storage.append_event(
                    {
                        "event": "network_publish_failed",
                        "ref": draft.ref,
                        "network": network,
                        "error": result.error,
                    }
                )
            else:
                self.storage.append_event(
                    {
                        "event": "network_published" if live else "network_dry_run",
                        "ref": draft.ref,
                        "network": network,
                        "result": result.to_dict(),
                    }
                )
            results.append(result)

        if live:
            statuses = {result.status for result in results}
            if statuses <= {"published", "skipped"}:
                draft.status = "published"
            elif statuses <= {"failed"}:
                draft.status = "failed"
            else:
                draft.status = "partial"
            self.storage.save_draft(draft, expected_revision=draft.draft_revision)
        return results

    def rollback(self, ref: str, network: str, *, live: bool) -> PublishResult:
        if network not in self.clients:
            raise PublishError(f"Red desconocida: {network}")
        event = self.storage.latest_publish_event(ref, network)
        if event is None:
            raise PublishError(f"No hay publicacion registrada para {ref}/{network}")
        result = self.clients[network].rollback(event, dry_run=not live)
        self.storage.append_event(
            {
                "event": "network_rolled_back" if live else "network_rollback_dry_run",
                "ref": ref,
                "network": network,
            }
        )
        return result
