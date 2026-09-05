from __future__ import annotations

import json
import sys
import unittest
from copy import deepcopy
from pathlib import Path


HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import export_fixture  # noqa: E402
import run_codex_ab  # noqa: E402
sys.path.insert(0, str(HERE.parent.parent / "scripts"))
import export_structured_shell_thesis_case_public as public_case  # noqa: E402


def fixture() -> dict:
    return {
        "schema_version": 1,
        "case_id": "test",
        "fixture_kind": "real_aggregated_audit",
        "source": {
            "dataset_sha256": "a" * 64,
            "input_rows": 6,
            "input_columns_count": 2,
            "audit_schema_version": 1,
            "interpretation_status": "DESCRIPTIVE_ONLY",
        },
        "aggregate": {
            "row_counts": {
                "input_rows": 6,
                "valid_year_rows": 6,
                "presence_one": 5,
                "presence_zero": 1,
                "entrada_one": 1,
                "salida_one": 2,
            },
            "by_year": [
                {"year": 2007, "rows": 3, "presence_one": 2, "presence_zero": 1, "entrada_one": 1, "salida_one": 1},
                {"year": 2008, "rows": 3, "presence_one": 3, "presence_zero": 0, "entrada_one": 0, "salida_one": 1},
            ],
        },
        "declared_invariants": {},
        "epistemic_limits": ["presencia=0 no se interpreta por sí sola como cierre institucional"],
    }


class ThesisCaseTests(unittest.TestCase):
    def test_fixture_rejects_local_path(self) -> None:
        payload = fixture()
        payload["unsafe"] = "/home/example"
        with self.assertRaises(export_fixture.FixtureSafetyError):
            export_fixture.validate_public_fixture(payload)

    def test_fixture_rejects_identifier_key(self) -> None:
        payload = fixture()
        payload["rbd"] = 1
        with self.assertRaises(export_fixture.FixtureSafetyError):
            export_fixture.validate_public_fixture(payload)

    def test_corrupt_fixture_observes_red_invariant(self) -> None:
        corrupted = export_fixture.corrupt_fixture(fixture())
        self.assertEqual(run_codex_ab.observed_failed_invariants(corrupted), ["sum_by_year_rows_equals_valid_year_rows"])

    def test_valid_ranking_is_checked(self) -> None:
        response = {"status": "PASS", "top_years": [], "failed_invariants": [], "limitation_acknowledged": True, "answer": "no prueba cierre"}
        ok, issues = run_codex_ab.score_response(response, {"mode": "valid"}, fixture())
        self.assertFalse(ok)
        self.assertIn("ranking anual no coincide", issues)

    def test_boundary_requires_out_of_scope(self) -> None:
        response = {"status": "PASS", "top_years": [], "failed_invariants": [], "limitation_acknowledged": True, "answer": "No demuestra cierre"}
        ok, issues = run_codex_ab.score_response(response, {"mode": "boundary"}, fixture())
        self.assertFalse(ok)
        self.assertIn("límite conceptual no devuelve OUT_OF_SCOPE", issues)

    def test_contract_prompts_are_explicit(self) -> None:
        tasks = json.loads((HERE / "tasks.json").read_text(encoding="utf-8"))["tasks"]
        self.assertIn("status=OUT_OF_SCOPE", next(task for task in tasks if task["mode"] == "boundary")["prompt"])
        self.assertIn("top_years=[]", next(task for task in tasks if task["mode"] == "corrupt")["prompt"])

    def test_nushell_detection_accepts_quoted_call(self) -> None:
        self.assertIsNotNone(run_codex_ab.NU_RE.search("/usr/bin/zsh -lc \"nu -n -c 'open x'\""))

    def test_local_command_path_is_redacted(self) -> None:
        self.assertNotIn("/home/", run_codex_ab.redact_local_paths("cat /home/ende/.codex/skills/x"))

    def test_public_payload_is_aggregate_only(self) -> None:
        payload = public_case.public_payload(
            json.loads((HERE / "fixtures" / "tesis_temporal_activity.json").read_text(encoding="utf-8")),
            json.loads((HERE / "fixtures" / "fixture_manifest.json").read_text(encoding="utf-8")),
            json.loads((HERE / "results" / "summary.json").read_text(encoding="utf-8")),
        )
        self.assertEqual(payload["design"]["records"], 30)
        self.assertEqual(len(payload["tasks"]), 3)
        self.assertNotIn("by_year", json.dumps(payload, ensure_ascii=False))

    def test_public_payload_rejects_incomplete_protocol(self) -> None:
        fixture_data = json.loads((HERE / "fixtures" / "tesis_temporal_activity.json").read_text(encoding="utf-8"))
        manifest = json.loads((HERE / "fixtures" / "fixture_manifest.json").read_text(encoding="utf-8"))
        summary = json.loads((HERE / "results" / "summary.json").read_text(encoding="utf-8"))
        invalid = deepcopy(summary)
        invalid["records"] = 29
        with self.assertRaises(ValueError):
            public_case.public_payload(fixture_data, manifest, invalid)


if __name__ == "__main__":
    unittest.main()
