from __future__ import annotations

import json

import pytest

from cucharadas_difusion.destinations import destination_status
from cucharadas_difusion.posts import PostError, add_utm, update_draft_from_ui, validate_draft
from cucharadas_difusion.providers import ProviderError, _parse_json, _prompt
from cucharadas_difusion.storage import StaleRevisionError, Storage


def test_pair_and_localized_urls(posts):
    assert set(posts) == {"es", "en"}
    assert posts["es"].canonical_url.startswith("https://3cucharadas.cl/")
    assert posts["en"].canonical_url.startswith("https://3cucharadas.cl/en/")
    assert posts["es"].distribution["social"] is True
    assert posts["en"].distribution["republish"] == ["dev", "medium"]


def test_utm_contract(posts):
    url = add_utm(posts["es"].canonical_url, "mastodon", posts["es"].ref, "es")
    assert "utm_source=mastodon" in url
    assert "utm_medium=social" in url
    assert "utm_campaign=casen2024-julia-waffles" in url
    assert "utm_content=es" in url


def test_validation_and_approval_reset(draft):
    assert validate_draft(draft) == []
    raw = {
        "base_copy": dict(draft.base_copy),
        "approvals": {"mastodon": True, "bluesky": True},
    }
    update_draft_from_ui(draft, raw)
    assert draft.approvals == {"mastodon": True, "bluesky": True}
    raw["base_copy"]["es"] += " cambio"
    update_draft_from_ui(draft, raw)
    assert draft.approvals["bluesky"] is False
    assert draft.approvals["mastodon"] is False
    assert draft.messages["bluesky"]["es"].text == draft.base_copy["es"]
    assert draft.messages["mastodon"]["es"].text.startswith(draft.base_copy["es"])
    assert draft.messages["mastodon"]["es"].target_url in draft.messages["mastodon"]["es"].text


def test_unbacked_number_is_blocking(draft):
    draft.messages["bluesky"]["es"].text += " 999%"
    errors = validate_draft(draft)
    assert any("cifras no presentes" in error for error in errors)


def test_temporal_claim_is_blocking(draft):
    draft.messages["bluesky"]["en"].text = "New CASEN 2024 analysis with Julia. #CASEN2024"
    errors = validate_draft(draft)
    assert any("expresion temporal" in error for error in errors)


def test_base_copy_cannot_duplicate_url_in_bluesky(draft):
    draft.messages["bluesky"]["es"].text += " https://example.test"
    errors = validate_draft(draft)
    assert any("tarjeta externa" in error for error in errors)


def test_atomic_revision_and_ledger(tmp_path, draft):
    storage = Storage(tmp_path)
    first = storage.save_draft(draft)
    assert first.draft_revision == 1
    loaded = storage.load_draft(draft.ref)
    loaded.status = "edited"
    second = storage.save_draft(loaded, expected_revision=1)
    assert second.draft_revision == 2
    with pytest.raises(StaleRevisionError):
        storage.save_draft(loaded, expected_revision=1)
    storage.append_event({"event": "network_published", "ref": draft.ref, "network": "mastodon"})
    assert storage.published_networks(draft.ref) == {"mastodon"}
    storage.append_event({"event": "network_rolled_back", "ref": draft.ref, "network": "mastodon"})
    assert storage.published_networks(draft.ref) == set()
    storage.append_event({"event": "network_published", "ref": draft.ref, "network": "mastodon"})
    assert storage.published_networks(draft.ref) == {"mastodon"}
    assert json.loads(storage.ledger_path.read_text().splitlines()[0])["ref"] == draft.ref


def test_provider_result_parser(valid_payload):
    compact = json.dumps(valid_payload, ensure_ascii=False, separators=(",", ":"))
    parsed = _parse_json(f"# AGY_RESULT\nstatus: success\ncopy_payload_json: {compact}\n")
    assert parsed == valid_payload
    with pytest.raises(ProviderError):
        _parse_json("status: success but no payload")


def test_provider_prompt_requires_first_person_without_generic_cta():
    prompt = _prompt({"title_es": "Un HUD de cuotas", "title_en": "An AI quota HUD"})
    assert "author's first person" in prompt
    assert "Do not address the reader with imperatives" in prompt
    assert "stay informed" in prompt


def test_provider_parser_decodes_only_whole_percent_encoded_messages(valid_payload):
    import urllib.parse

    encoded = {lang: urllib.parse.quote(text, safe="/:?&=#_-") for lang, text in valid_payload.items()}
    parsed = _parse_json(json.dumps(encoded, ensure_ascii=False))
    assert parsed == valid_payload


def test_v1_draft_loads_with_bluesky_as_base(draft):
    raw = draft.to_dict()
    raw.pop("base_copy")
    raw["schema_version"] = 1
    from cucharadas_difusion.models import Draft

    migrated = Draft.from_dict(raw)
    assert migrated.schema_version == 1
    assert migrated.base_copy["es"] == migrated.messages["bluesky"]["es"].text


def test_published_draft_is_read_only(draft):
    draft.status = "published_verified"
    raw = {"base_copy": dict(draft.base_copy), "approvals": dict(draft.approvals)}
    raw["base_copy"]["es"] += " cambio"
    with pytest.raises(PostError, match="solo lectura"):
        update_draft_from_ui(draft, raw)


def test_destinations_are_content_gated(repo):
    rows = {row["destination"]: row for row in destination_status(repo, "casen2024-julia-waffles")}
    assert rows["dev"]["status"] == "ready"
    assert rows["medium"]["status"] == "ready"
    assert rows["juliabloggers"]["status"] == "monitoring"
    assert rows["r-bloggers"]["status"] == "blocked"
