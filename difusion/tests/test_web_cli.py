from __future__ import annotations

import asyncio

import httpx

from cucharadas_difusion.cli import main
from cucharadas_difusion.models import PublishResult
from cucharadas_difusion.storage import Storage
from cucharadas_difusion.web import create_app


def ui_payload(draft, *, approvals=True):
    return {
        "expected_revision": draft.draft_revision,
        "approvals": {"mastodon": approvals, "bluesky": approvals},
        "base_copy": dict(draft.base_copy),
    }


def test_gui_auth_revision_and_publish_gate(tmp_path, draft):
    storage = Storage(tmp_path)
    storage.save_draft(draft)
    app = create_app(draft.ref, storage, "test-token")
    headers = {"X-Review-Token": "test-token"}

    async def scenario():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            index = await client.get("/")
            assert index.status_code == 200
            assert index.headers["x-frame-options"] == "DENY"
            assert index.text.count('class="message-card') == 4
            assert (await client.get("/api/draft")).status_code == 403

            current = (await client.get("/api/draft", headers=headers)).json()
            response = await client.put("/api/draft", headers=headers, json=ui_payload(draft))
            assert response.status_code == 200
            saved = response.json()
            assert saved["draft_revision"] == current["draft_revision"] + 1
            assert saved["approvals"] == {"mastodon": True, "bluesky": True}

            stale = await client.put("/api/draft", headers=headers, json=ui_payload(draft))
            assert stale.status_code == 409
            wrong = await client.post(
                "/api/publish",
                headers=headers,
                json={"expected_revision": saved["draft_revision"], "confirmation": "PUBLICAR otra-cosa"},
            )
            assert wrong.status_code == 400

    asyncio.run(scenario())


def test_cli_manual_prepare_and_preview(tmp_path, repo, capsys):
    post = "_posts/2026-03-15-casen2024-julia-waffles-politica-publica.md"
    common = ["--repo", str(repo), "--state-dir", str(tmp_path)]
    assert main(common + ["prepare", post, "--provider", "manual", "--skip-url-check", "--no-review"]) == 0
    prepared = capsys.readouterr()
    assert "Borrador:" in prepared.out
    assert main(common + ["preview", "casen2024-julia-waffles", "--format", "json"]) == 0
    preview = capsys.readouterr().out
    assert '"provider": "manual"' in preview
    assert '"schema_version": 2' in preview


def test_cli_destinations(tmp_path, repo, capsys):
    code = main(
        [
            "--repo",
            str(repo),
            "--state-dir",
            str(tmp_path),
            "destinations",
            "status",
            "casen2024-julia-waffles",
        ]
    )
    assert code == 0
    output = capsys.readouterr().out
    assert "dev" in output and "ready" in output
    assert "juliabloggers" in output and "monitoring" in output


def test_gui_async_publish_progress_and_verification(tmp_path, draft, monkeypatch):
    storage = Storage(tmp_path)
    storage.save_draft(draft)

    class FakePublisher:
        def __init__(self, target_storage):
            self.storage = target_storage

        def publish(self, current, *, live, progress):
            for step in ("mastodon_es", "mastodon_en", "bluesky_es", "bluesky_en"):
                progress(step, "success", "ok", f"https://example.test/{step}")
            current.status = "published"
            self.storage.save_draft(current, expected_revision=current.draft_revision)
            return [
                PublishResult(network="mastodon", status="published"),
                PublishResult(network="bluesky", status="published"),
            ]

    def fake_verify(target_storage, ref, *, progress):
        progress("verification", "success", "confirmado", "")
        current = target_storage.load_draft(ref)
        current.status = "published_verified"
        saved = target_storage.save_draft(current, expected_revision=current.draft_revision)
        return {"status": "published_verified", "draft_revision": saved.draft_revision, "errors": []}

    monkeypatch.setattr("cucharadas_difusion.web.Publisher", FakePublisher)
    monkeypatch.setattr("cucharadas_difusion.web.verify_publication", fake_verify)
    app = create_app(draft.ref, storage, "test-token")
    headers = {"X-Review-Token": "test-token"}

    async def scenario():
        transport = httpx.ASGITransport(app=app)
        async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
            saved = (await client.put("/api/draft", headers=headers, json=ui_payload(draft))).json()
            response = await client.post(
                "/api/publish",
                headers=headers,
                json={
                    "expected_revision": saved["draft_revision"],
                    "confirmation": f"PUBLICAR {draft.ref}",
                },
            )
            assert response.status_code == 202
            job = response.json()
            for _ in range(100):
                job = (await client.get(f"/api/publish/{job['job_id']}", headers=headers)).json()
                if job["state"] == "done":
                    break
                await asyncio.sleep(0.01)
            assert job["status"] == "published_verified"
            assert all(value["status"] == "success" for value in job["steps"].values())
            assert storage.load_draft(draft.ref).status == "published_verified"

    asyncio.run(scenario())


def test_doctor_auth_reports_accounts(tmp_path, repo, capsys, monkeypatch):
    secrets_file = tmp_path / "secrets.env"
    secrets_file.write_text(
        "MASTODON_TOKEN=m-token\nBSKY_HANDLE=example.test\nBSKY_APP_PASSWORD=b-password\n",
        encoding="utf-8",
    )
    secrets_file.chmod(0o600)
    monkeypatch.setattr(
        "cucharadas_difusion.cli.authenticate_accounts",
        lambda _: {"mastodon": "asiole", "bluesky": "labra.bsky.social"},
    )
    code = main(["--repo", str(repo), "--secrets", str(secrets_file), "doctor", "--auth"])
    output = capsys.readouterr().out
    assert code == 0
    assert "social-auth" in output and "mastodon=asiole" in output
    assert "m-token" not in output and "b-password" not in output
