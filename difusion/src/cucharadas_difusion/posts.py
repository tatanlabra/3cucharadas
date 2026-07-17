from __future__ import annotations

import re
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlencode, urlsplit, urlunsplit

import yaml

from .models import Draft, Message, PostMetadata, utc_now

SUPPORTED_LANGS = ("es", "en")
SUPPORTED_NETWORKS = ("mastodon", "bluesky")


class PostError(RuntimeError):
    pass


def _front_matter(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---\n"):
        raise PostError(f"Front matter ausente en {path}")
    try:
        header, body = raw[4:].split("\n---\n", 1)
    except ValueError as exc:
        raise PostError(f"Front matter incompleto en {path}") from exc
    data = yaml.safe_load(header) or {}
    if not isinstance(data, dict):
        raise PostError(f"Front matter invalido en {path}")
    return data, body


def load_site_config(repo: Path) -> dict[str, Any]:
    config = yaml.safe_load((repo / "_config.yml").read_text(encoding="utf-8")) or {}
    if not isinstance(config, dict):
        raise PostError("_config.yml no es un mapping YAML")
    return config


def _absolute(root: str, path: str) -> str:
    return f"{root.rstrip('/')}/{path.lstrip('/')}"


def parse_post(path: Path, repo: Path) -> PostMetadata:
    data, _ = _front_matter(path)
    required = ("ref", "lang", "title", "description", "permalink")
    missing = [key for key in required if not data.get(key)]
    if missing:
        raise PostError(f"Faltan campos {missing} en {path}")
    lang = str(data["lang"])
    if lang not in SUPPORTED_LANGS:
        raise PostError(f"Idioma no soportado en {path}: {lang}")

    config = load_site_config(repo)
    site_root = f"{config.get('url', '')}{config.get('baseurl', '')}".rstrip("/")
    if not site_root.startswith("https://"):
        raise PostError("El sitio canonico debe usar https://")
    permalink = str(data["permalink"])
    localized = permalink if lang == config.get("default_lang", "es") else f"/{lang}{permalink}"
    header = data.get("header") if isinstance(data.get("header"), dict) else {}
    image = str(header.get("og_image") or config.get("og_image") or "")
    distribution = data.get("distribution") if isinstance(data.get("distribution"), dict) else {}
    return PostMetadata(
        path=str(path.resolve()),
        ref=str(data["ref"]),
        lang=lang,  # type: ignore[arg-type]
        title=str(data["title"]),
        description=str(data["description"]),
        tags=[str(item) for item in data.get("tags", [])],
        categories=[str(item) for item in data.get("categories", [])],
        canonical_url=_absolute(site_root, localized),
        image_url=_absolute(site_root, image) if image else "",
        distribution=distribution,
    )


def find_pair(repo: Path, source_path: Path) -> dict[str, PostMetadata]:
    source = parse_post(source_path, repo)
    posts: dict[str, PostMetadata] = {source.lang: source}
    for candidate in sorted((repo / "_posts").glob("*.md")):
        if candidate.resolve() == source_path.resolve():
            continue
        try:
            post = parse_post(candidate, repo)
        except PostError:
            continue
        if post.ref == source.ref:
            posts[post.lang] = post
    missing = [lang for lang in SUPPORTED_LANGS if lang not in posts]
    if missing:
        raise PostError(f"Falta el par {missing} para ref={source.ref}")
    if not bool(posts["es"].distribution.get("social")):
        raise PostError("El post ES no tiene distribution.social: true")
    return posts


def add_utm(url: str, network: str, ref: str, lang: str) -> str:
    parsed = urlsplit(url)
    params = urlencode(
        {
            "utm_source": network,
            "utm_medium": "social",
            "utm_campaign": ref,
            "utm_content": lang,
        }
    )
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, params, ""))


def public_prompt_context(posts: dict[str, PostMetadata]) -> dict[str, Any]:
    return {
        "ref": posts["es"].ref,
        "es": {
            "title": posts["es"].title,
            "description": posts["es"].description,
            "tags": posts["es"].tags,
            "url": posts["es"].canonical_url,
            "mastodon_url": add_utm(posts["es"].canonical_url, "mastodon", posts["es"].ref, "es"),
            "bluesky_card_url": add_utm(posts["es"].canonical_url, "bluesky", posts["es"].ref, "es"),
        },
        "en": {
            "title": posts["en"].title,
            "description": posts["en"].description,
            "tags": posts["en"].tags,
            "url": posts["en"].canonical_url,
            "mastodon_url": add_utm(posts["en"].canonical_url, "mastodon", posts["en"].ref, "en"),
            "bluesky_card_url": add_utm(posts["en"].canonical_url, "bluesky", posts["en"].ref, "en"),
        },
    }


def create_draft(
    posts: dict[str, PostMetadata],
    provider: str,
    payload: dict[str, Any] | None,
    attempts: list[dict[str, Any]],
    mastodon_limit: int = 500,
) -> Draft:
    now = utc_now()
    base_copy = _payload_base_copy(payload)
    messages: dict[str, dict[str, Message]] = {}
    for network in SUPPORTED_NETWORKS:
        messages[network] = {}
        for lang in SUPPORTED_LANGS:
            target_url = add_utm(posts[lang].canonical_url, network, posts[lang].ref, lang)
            text = _derived_text(base_copy.get(lang, ""), network, target_url)
            messages[network][lang] = Message(
                network=network,  # type: ignore[arg-type]
                lang=lang,  # type: ignore[arg-type]
                role="root" if lang == "es" else "reply",
                text=text,
                target_url=target_url,
            )
    draft = Draft(
        schema_version=2,
        ref=posts["es"].ref,
        provider=provider,
        draft_revision=1,
        created_at=now,
        updated_at=now,
        status="prepared",
        posts=posts,
        messages=messages,
        base_copy=base_copy,
        approvals={network: False for network in SUPPORTED_NETWORKS},
        limits={"mastodon": mastodon_limit, "bluesky": 300},
        provider_attempts=attempts,
    )
    validate_draft(draft)
    return draft


def _payload_base_copy(payload: dict[str, Any] | None) -> dict[str, str]:
    if payload is None:
        return {lang: "" for lang in SUPPORTED_LANGS}
    candidate: Any = payload.get("base_copy") if isinstance(payload.get("base_copy"), dict) else payload
    if all(isinstance(candidate.get(lang), str) for lang in SUPPORTED_LANGS):
        return {lang: str(candidate[lang]).strip() for lang in SUPPORTED_LANGS}
    # Compatibilidad con resultados de proveedores v1.
    bluesky = payload.get("bluesky")
    if isinstance(bluesky, dict) and all(isinstance(bluesky.get(lang), str) for lang in SUPPORTED_LANGS):
        return {lang: str(bluesky[lang]).strip() for lang in SUPPORTED_LANGS}
    return {lang: "" for lang in SUPPORTED_LANGS}


def _derived_text(base: str, network: str, target_url: str) -> str:
    clean = base.strip()
    return f"{clean} {target_url}".strip() if network == "mastodon" and clean else clean


def derive_messages(draft: Draft) -> None:
    for network in SUPPORTED_NETWORKS:
        for lang in SUPPORTED_LANGS:
            message = draft.messages[network][lang]
            message.text = _derived_text(draft.base_copy.get(lang, ""), network, message.target_url)


def _grapheme_count(text: str) -> int:
    try:
        import regex  # type: ignore[import-not-found]

        return len(regex.findall(r"\X", text))
    except ImportError:
        return len(text)


def extract_hashtags(text: str) -> list[str]:
    return re.findall(r"(?<!\w)#[\w-]+", text, flags=re.UNICODE)


def _numbers(text: str) -> set[str]:
    return set(re.findall(r"(?<!\w)\d+(?:[.,]\d+)?%?", text))


def validate_message(message: Message, draft: Draft) -> list[str]:
    warnings: list[str] = []
    text = message.text.strip()
    if not text:
        return ["error: el texto esta vacio"]
    limit = draft.limits[message.network]
    count = _grapheme_count(text)
    if count > limit:
        warnings.append(f"error: {count} caracteres; limite {limit}")
    if message.network == "mastodon" and message.target_url not in text:
        warnings.append("error: Mastodon debe incluir la URL UTM")
    if message.network == "bluesky" and re.search(r"https?://", text, flags=re.IGNORECASE):
        warnings.append("error: Bluesky usa la tarjeta externa; elimina la URL del mensaje base")

    post = draft.posts[message.lang]
    allowed_numbers = _numbers(f"{post.title} {post.description} {post.canonical_url}")
    introduced = sorted(_numbers(text) - allowed_numbers)
    if introduced:
        warnings.append("error: cifras no presentes en metadatos publicos: " + ", ".join(introduced))
    if len(extract_hashtags(text)) > 4:
        warnings.append("advertencia: mas de 4 hashtags")
    temporal = re.search(r"\b(new|recent|recently|today|nuevo|nueva|reciente|hoy)\b", text, flags=re.IGNORECASE)
    if temporal:
        warnings.append(f"error: expresion temporal no estable: {temporal.group(0)}")
    return warnings


def validate_draft(draft: Draft) -> list[str]:
    errors: list[str] = []
    for network in SUPPORTED_NETWORKS:
        for lang in SUPPORTED_LANGS:
            message = draft.messages[network][lang]
            message.warnings = validate_message(message, draft)
            errors.extend(
                f"{network}.{lang}: {warning}"
                for warning in message.warnings
                if warning.startswith("error:")
            )
    return errors


def update_draft_from_ui(draft: Draft, raw: dict[str, Any]) -> Draft:
    incoming_base = raw.get("base_copy")
    if not isinstance(incoming_base, dict):
        # Compatibilidad temporal con clientes v1: se toma la variante Bluesky.
        incoming_messages = raw.get("messages")
        if not isinstance(incoming_messages, dict) or not isinstance(incoming_messages.get("bluesky"), dict):
            raise PostError("base_copy debe ser un objeto")
        incoming_base = {
            lang: incoming_messages["bluesky"].get(lang, {}).get("text")
            for lang in SUPPORTED_LANGS
        }
    clean_base: dict[str, str] = {}
    for lang in SUPPORTED_LANGS:
        value = incoming_base.get(lang)
        if not isinstance(value, str):
            raise PostError(f"Falta base_copy.{lang}")
        clean_base[lang] = value.strip()
    changed = any(clean_base[lang] != draft.base_copy.get(lang, "") for lang in SUPPORTED_LANGS)
    if changed and draft.status in {"published", "published_verified", "published_unverified"}:
        raise PostError("Una publicacion finalizada es de solo lectura; prepara un borrador nuevo")
    if changed:
        draft.base_copy = clean_base
        derive_messages(draft)
        for network in SUPPORTED_NETWORKS:
            draft.approvals[network] = False
            for lang in SUPPORTED_LANGS:
                draft.messages[network][lang].approved = False

    approvals = raw.get("approvals", {})
    if not isinstance(approvals, dict):
        raise PostError("approvals debe ser un objeto")
    validate_draft(draft)
    for network in SUPPORTED_NETWORKS:
        requested = approvals.get(network) is True and not changed
        has_errors = any(
            warning.startswith("error:")
            for lang in SUPPORTED_LANGS
            for warning in draft.messages[network][lang].warnings
        )
        draft.approvals[network] = requested and not has_errors
        for lang in SUPPORTED_LANGS:
            draft.messages[network][lang].approved = draft.approvals[network]
    return draft


def check_public_urls(posts: dict[str, PostMetadata], timeout: float = 10.0) -> dict[str, str]:
    results: dict[str, str] = {}
    for lang, post in posts.items():
        request = urllib.request.Request(post.canonical_url, method="HEAD", headers={"User-Agent": "3cucharadas-difusion/0.1"})
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                status = int(response.status)
        except urllib.error.HTTPError as exc:
            status = exc.code
        except (urllib.error.URLError, TimeoutError) as exc:
            raise PostError(f"No se pudo verificar {post.canonical_url}: {exc}") from exc
        if status != 200:
            raise PostError(f"URL {lang} no disponible: HTTP {status}")
        results[lang] = f"HTTP {status}"
    return results
