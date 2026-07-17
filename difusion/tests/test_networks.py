from __future__ import annotations

from typing import Any

import pytest

from cucharadas_difusion.models import PublishResult
from cucharadas_difusion.networks import BlueskyClient, PartialPublishError, PublishError, Publisher
from cucharadas_difusion.storage import Storage


class FakeClient:
    def __init__(self, network: str, partial_once: bool = False, fail_with: str = "") -> None:
        self.network = network
        self.partial_once = partial_once
        self.fail_with = fail_with
        self.publish_calls = 0
        self.resume_calls = 0
        self.rollback_calls: list[dict[str, Any]] = []

    def publish_thread(self, draft, dry_run: bool, progress=None):
        self.publish_calls += 1
        if self.fail_with:
            raise RuntimeError(self.fail_with)
        if dry_run:
            if progress:
                progress(f"{self.network}_es", "success", "simulacion", "")
                progress(f"{self.network}_en", "success", "simulacion", "")
            return PublishResult(network=self.network, status="dry_run")
        if self.partial_once:
            self.partial_once = False
            raise PartialPublishError(
                PublishResult(
                    network=self.network,
                    status="partial",
                    root_id=f"{self.network}-root",
                    root_url=f"https://example.test/{self.network}/root",
                ),
                RuntimeError("reply failed"),
            )
        return PublishResult(
            network=self.network,
            status="published",
            root_id=f"{self.network}-root",
            root_url=f"https://example.test/{self.network}/root",
            reply_id=f"{self.network}-reply",
            reply_url=f"https://example.test/{self.network}/reply",
        )

    def resume_thread(self, draft, event, progress=None):
        self.resume_calls += 1
        return PublishResult(
            network=self.network,
            status="published",
            root_id=event["result"]["root_id"],
            root_url=event["result"]["root_url"],
            reply_id=f"{self.network}-reply",
            reply_url=f"https://example.test/{self.network}/reply",
        )

    def rollback(self, event, dry_run: bool):
        self.rollback_calls.append(event)
        return PublishResult(network=self.network, status="dry_run" if dry_run else "published")


def approved(draft):
    draft.approvals = {"mastodon": True, "bluesky": True}
    for network in draft.messages.values():
        for message in network.values():
            message.approved = True
    return draft


def test_dry_run_has_no_published_marker(tmp_path, draft):
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    publisher = Publisher(storage, {})
    publisher.clients = {name: FakeClient(name) for name in ("mastodon", "bluesky")}
    results = publisher.publish(draft, live=False)
    assert {item.status for item in results} == {"dry_run"}
    assert storage.published_networks(draft.ref) == set()


def test_progress_reports_four_pieces(tmp_path, draft):
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    publisher = Publisher(storage, {})
    publisher.clients = {name: FakeClient(name) for name in ("mastodon", "bluesky")}
    seen = []
    publisher.publish(draft, live=False, progress=lambda step, status, detail, url: seen.append((step, status)))
    assert seen == [
        ("mastodon_es", "success"),
        ("mastodon_en", "success"),
        ("bluesky_es", "success"),
        ("bluesky_en", "success"),
    ]


def test_idempotence_and_partial_resume(tmp_path, draft):
    draft = approved(draft)
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    mastodon = FakeClient("mastodon", partial_once=True)
    bluesky = FakeClient("bluesky")
    publisher = Publisher(storage, {})
    publisher.clients = {"mastodon": mastodon, "bluesky": bluesky}

    first = publisher.publish(draft, live=True)
    assert [item.status for item in first] == ["partial", "published"]
    assert storage.load_draft(draft.ref).status == "partial"

    resumed = publisher.publish(storage.load_draft(draft.ref), live=True)
    assert [item.status for item in resumed] == ["published", "skipped"]
    assert mastodon.publish_calls == 1
    assert mastodon.resume_calls == 1
    assert storage.published_networks(draft.ref) == {"mastodon", "bluesky"}

    repeated = publisher.publish(storage.load_draft(draft.ref), live=True)
    assert [item.status for item in repeated] == ["skipped", "skipped"]


def test_secret_is_redacted_from_failure_ledger(tmp_path, draft):
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    publisher = Publisher(storage, {"MASTODON_TOKEN": "top-secret-token"})
    publisher.clients = {
        "mastodon": FakeClient("mastodon", fail_with="bad top-secret-token"),
        "bluesky": FakeClient("bluesky"),
    }
    publisher.publish(draft, live=False)
    assert "top-secret-token" not in storage.ledger_path.read_text(encoding="utf-8")


def test_bluesky_hashtag_facets_use_utf8_byte_offsets():
    from atproto import models

    text = "Análisis útil #casen2024 y #política-pública"
    facets = BlueskyClient._hashtag_facets(text, models)

    assert [facet.features[0].tag for facet in facets] == ["casen2024", "política-pública"]
    for facet, hashtag in zip(facets, ["#casen2024", "#política-pública"], strict=True):
        encoded = text.encode("utf-8")
        start = facet.index.byte_start
        end = facet.index.byte_end
        assert encoded[start:end].decode("utf-8") == hashtag


def test_bluesky_card_rejects_non_https_image():
    client = BlueskyClient({})

    with pytest.raises(PublishError, match="imagen OG https"):
        client._download_card_image("http://example.test/card.jpg")


def test_total_live_failure_is_not_reported_as_partial(tmp_path, draft):
    draft = approved(draft)
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    publisher = Publisher(storage, {})
    publisher.clients = {
        "mastodon": FakeClient("mastodon", fail_with="offline"),
        "bluesky": FakeClient("bluesky", fail_with="offline"),
    }
    results = publisher.publish(draft, live=True)
    assert {item.status for item in results} == {"failed"}
    assert storage.load_draft(draft.ref).status == "failed"


def test_rollback_uses_latest_ids(tmp_path, draft):
    storage = Storage(tmp_path)
    storage.append_event(
        {
            "event": "network_published",
            "ref": draft.ref,
            "network": "mastodon",
            "result": {"root_id": "root", "reply_id": "reply"},
        }
    )
    fake = FakeClient("mastodon")
    publisher = Publisher(storage, {})
    publisher.clients["mastodon"] = fake
    result = publisher.rollback(draft.ref, "mastodon", live=False)
    assert result.status == "dry_run"
    assert fake.rollback_calls[0]["result"]["reply_id"] == "reply"
