from __future__ import annotations

from cucharadas_difusion.posts import extract_hashtags
from cucharadas_difusion.storage import Storage
from cucharadas_difusion.verification import verify_publication


def _facets(text: str):
    return [
        {
            "$type": "app.bsky.richtext.facet",
            "features": [{"$type": "app.bsky.richtext.facet#tag", "tag": tag[1:]}],
            "index": {"byteStart": 0, "byteEnd": 1},
        }
        for tag in extract_hashtags(text)
    ]


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
