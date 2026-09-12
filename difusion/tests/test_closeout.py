import json
import subprocess
from types import SimpleNamespace

from cucharadas_difusion import cli
from cucharadas_difusion.storage import Storage


def setup_draft(tmp_path, draft):
    Storage(tmp_path / "state").save_draft(draft)
    return ["--state-dir", str(tmp_path / "state"), "closeout", draft.ref]


def test_dry_run_never_calls_live_checks_or_reconciliation(tmp_path, draft, monkeypatch):
    args = setup_draft(tmp_path, draft)
    monkeypatch.setattr(cli, "_publish", lambda args: 0 if not args.live else 99)
    monkeypatch.setattr(cli.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("unexpected reconciliation")))
    monkeypatch.setattr(cli, "check_public_urls", lambda *a: (_ for _ in ()).throw(AssertionError("unexpected HTTP")))
    assert cli.main(args) == 0


def test_failed_publish_does_not_reconcile(tmp_path, draft, monkeypatch):
    args = setup_draft(tmp_path, draft)
    monkeypatch.setattr(cli, "check_public_urls", lambda *a: {})
    monkeypatch.setattr(cli, "_publish", lambda args: 1)
    monkeypatch.setattr(cli.subprocess, "run", lambda *a, **k: (_ for _ in ()).throw(AssertionError("reconciled failed publication")))
    assert cli.main(args + ["--live"]) == 1


def test_verified_publish_reconciles_exact_ref_and_state_then_audits(tmp_path, draft, monkeypatch):
    args = setup_draft(tmp_path, draft)
    calls = []
    monkeypatch.setattr(cli, "check_public_urls", lambda *a: {})
    monkeypatch.setattr(cli, "_publish", lambda args: 0)
    def run(command, **kwargs):
        calls.append((command, kwargs))
        return SimpleNamespace(returncode=0)
    monkeypatch.setattr(cli.subprocess, "run", run)
    assert cli.main(args + ["--live"]) == 0
    assert len(calls) == 2
    assert "--aplicar" in calls[0][0]
    assert "--social-only" in calls[1][0] and "--strict" in calls[1][0]
    for command, kwargs in calls:
        assert command[command.index("--ref") + 1] == draft.ref
        assert kwargs["env"]["CUCHARADAS_DIFUSION_STATE_DIR"] == str(tmp_path / "state")


def test_reconciliation_failure_is_not_a_success(tmp_path, draft, monkeypatch):
    args = setup_draft(tmp_path, draft)
    monkeypatch.setattr(cli, "check_public_urls", lambda *a: {})
    monkeypatch.setattr(cli, "_publish", lambda args: 0)
    monkeypatch.setattr(cli.subprocess, "run", lambda *a, **k: SimpleNamespace(returncode=1))
    assert cli.main(args + ["--live"]) == 1


def test_changed_policy_blocks_before_publish(tmp_path, draft, monkeypatch):
    args = setup_draft(tmp_path, draft)
    draft.posts["es"].distribution["social"] = False
    monkeypatch.setattr(cli, "find_pair", lambda *a: draft.posts)
    monkeypatch.setattr(cli, "_publish", lambda *a: (_ for _ in ()).throw(AssertionError("unexpected publish")))
    assert cli.main(args + ["--live"]) == 1
