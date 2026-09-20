from __future__ import annotations

import re

from cucharadas_difusion.posts import extract_hashtags
from cucharadas_difusion.storage import Storage
from cucharadas_difusion.verification import verify_publication


def _facets(text: str):
    tags = [
        {
            "$type": "app.bsky.richtext.facet",
            "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": tag[1:]}],
            "index": {"byteStart": 0, "byteEnd": 1},
        }
        for tag in extract_hashtags(text)
    ]
    links = [
        {
            "$type": "app.bsky.richtext.facet",
            "features": [{"$type": "app.bsky.richtext.facet#link", "uri": url}],
            "index": {"byteStart": 0, "byteEnd": 1},
        }
        for url in re.findall(r"https?://[^\s<>()]+", text)
    ]
    return [*tags, *links]


def test_public_verification_persists_verified_status(tmp_path, draft):
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    root_uri = "at://did:plc:test/app.bsky.feed.post/root"
    reply_uri = "at://did:plc:test/app.bsky.feed.post/reply"
    storage.append_event(
        {
            "event": "network_published",
            "ref": draft.ref,
            "network": "mastodon",
            "result": {
                "root_id": "m-root",
                "reply_id": "m-reply",
                "root_url": "https://mastodon.social/@test/m-root",
                "reply_url": "https://mastodon.social/@test/m-reply",
            },
        }
    )
    storage.append_event(
        {
            "event": "network_published",
            "ref": draft.ref,
            "network": "bluesky",
            "result": {
                "root_id": root_uri,
                "reply_id": reply_uri,
                "root_url": "https://bsky.app/profile/test/post/root",
                "reply_url": "https://bsky.app/profile/test/post/reply",
            },
        }
    )

    def bsky_record(lang: str, uri: str, reply=False):
        message = draft.messages["bluesky"][lang]
        record = {
            "text": message.text,
            "langs": [lang],
            "embed": {"external": {"uri": message.target_url, "thumb": {"ref": "blob"}}},
            "facets": _facets(message.text),
        }
        if reply:
            record["reply"] = {"parent": {"uri": root_uri}, "root": {"uri": root_uri}}
        return {"uri": uri, "record": record}

    responses = {
        "https://mastodon.social/api/v1/statuses/m-root": {
            "url": "https://mastodon.social/@test/m-root",
            "language": "es",
            "in_reply_to_id": None,
            "card": {"url": draft.messages["mastodon"]["es"].target_url, "image": "image"},
        },
        "https://mastodon.social/api/v1/statuses/m-reply": {
            "url": "https://mastodon.social/@test/m-reply",
            "language": "en",
            "in_reply_to_id": "m-root",
            "card": {"url": draft.messages["mastodon"]["en"].target_url, "image": "image"},
        },
    }

    def fetch(url: str):
        if url in responses:
            return responses[url]
        if "root" in url:
            return {"posts": [bsky_record("es", root_uri)]}
        return {"posts": [bsky_record("en", reply_uri, reply=True)]}

    progress = []
    result = verify_publication(
        storage,
        draft.ref,
        fetch=fetch,
        attempts=1,
        progress=lambda *values: progress.append(values),
    )
    assert result["status"] == "published_verified"
    assert storage.load_draft(draft.ref).status == "published_verified"
    assert storage.events(draft.ref)[-1]["event"] == "publication_verified"
    assert progress[0][0:2] == ("verification", "in_progress")
    assert progress[-1][0:2] == ("verification", "success")


def test_public_verification_marks_unverified_without_losing_publication(tmp_path, draft):
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    result = verify_publication(
        storage,
        draft.ref,
        fetch=lambda _: {},
        attempts=1,
    )
    assert result["status"] == "published_unverified"
    assert result["errors"]
    assert storage.load_draft(draft.ref).status == "published_unverified"


def test_public_verification_accepts_a_declared_audio_card_on_mastodon_root(tmp_path, draft):
    spotify = "https://open.spotify.com/episode/0gHdvYkrUomRP5vizqkgtW"
    draft.posts["es"].audio_urls = [spotify]
    draft.messages["mastodon"]["es"].text = f"{draft.messages['mastodon']['es'].text} {spotify}"
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    root_uri = "at://did:plc:test/app.bsky.feed.post/root"
    reply_uri = "at://did:plc:test/app.bsky.feed.post/reply"
    storage.append_event({"event": "network_published", "ref": draft.ref, "network": "mastodon", "result": {"root_id": "m-root", "reply_id": "m-reply", "root_url": "https://mastodon.social/@test/m-root", "reply_url": "https://mastodon.social/@test/m-reply"}})
    storage.append_event({"event": "network_published", "ref": draft.ref, "network": "bluesky", "result": {"root_id": root_uri, "reply_id": reply_uri, "root_url": "https://bsky.app/profile/test/post/root", "reply_url": "https://bsky.app/profile/test/post/reply"}})

    def fetch(url: str):
        if "mastodon.social" in url:
            is_root = "m-root" in url
            return {
                "url": url,
                "language": "es" if is_root else "en",
                "in_reply_to_id": None if is_root else "m-root",
                "card": {"url": spotify if is_root else draft.messages["mastodon"]["en"].target_url, "image": "image"},
            }
        lang = "es" if "root" in url else "en"
        record = {"text": draft.messages["bluesky"][lang].text, "langs": [lang], "embed": {"external": {"uri": draft.messages["bluesky"][lang].target_url, "thumb": {"ref": "blob"}}}, "facets": _facets(draft.messages["bluesky"][lang].text)}
        if lang == "en":
            record["reply"] = {"parent": {"uri": root_uri}, "root": {"uri": root_uri}}
        return {"posts": [{"uri": root_uri if lang == "es" else reply_uri, "record": record}]}

    result = verify_publication(storage, draft.ref, fetch=fetch, attempts=1)
    assert result["status"] == "published_verified"
    assert result["networks"]["mastodon"]["checks"]["root_card"] is True


def test_public_verification_rejects_an_incorrect_secondary_bluesky_link(tmp_path, draft):
    spotify = "https://open.spotify.com/episode/0gHdvYkrUomRP5vizqkgtW"
    draft.posts["es"].audio_urls = [spotify]
    draft.messages["bluesky"]["es"].text += f" {spotify}"
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    root_uri = "at://did:plc:test/app.bsky.feed.post/root"
    reply_uri = "at://did:plc:test/app.bsky.feed.post/reply"
    storage.append_event({"event": "network_published", "ref": draft.ref, "network": "mastodon", "result": {"root_id": "m-root", "reply_id": "m-reply", "root_url": "https://mastodon.social/@test/m-root", "reply_url": "https://mastodon.social/@test/m-reply"}})
    storage.append_event({"event": "network_published", "ref": draft.ref, "network": "bluesky", "result": {"root_id": root_uri, "reply_id": reply_uri, "root_url": "https://bsky.app/profile/test/post/root", "reply_url": "https://bsky.app/profile/test/post/reply"}})

    def fetch(url: str):
        if "mastodon.social" in url:
            return {"url": url, "language": "es" if "m-root" in url else "en", "in_reply_to_id": None if "m-root" in url else "m-root", "card": {"url": draft.messages["mastodon"]["es" if "m-root" in url else "en"].target_url, "image": "image"}}
        lang = "es" if "root" in url else "en"
        record = {"text": draft.messages["bluesky"][lang].text, "langs": [lang], "embed": {"external": {"uri": draft.messages["bluesky"][lang].target_url, "thumb": {"ref": "blob"}}}, "facets": _facets(draft.messages["bluesky"][lang].text)}
        if lang == "es":
            record["facets"][-1]["features"][0]["uri"] = "https://example.invalid/not-spotify"
        else:
            record["reply"] = {"parent": {"uri": root_uri}, "root": {"uri": root_uri}}
        return {"posts": [{"uri": root_uri if lang == "es" else reply_uri, "record": record}]}

    result = verify_publication(storage, draft.ref, fetch=fetch, attempts=1)
    assert result["status"] == "published_unverified"
    assert "root_links" in result["errors"][0]
