from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonschema import Draft7Validator
from jsonschema.validators import validator_for


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/build_post3_visual_tokens.py"
TOKENS = ROOT / "assets/data/tesis-post3/visual_identity_tokens_v1.json"
OUTPUT = ROOT / "_sass/_post3-data-viz-tokens.scss"
MANIFEST = ROOT / "assets/images/tesis-post3/manifest.json"
CSS = ROOT / "assets/css/main.scss"


def run_gate(
    tokens: Path = TOKENS,
    output: Path = OUTPUT,
    manifest: Path = MANIFEST,
    css: Path = CSS,
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--check",
            "--tokens",
            str(tokens),
            "--output",
            str(output),
            "--manifest",
            str(manifest),
            "--css-source",
            str(css),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


class Post3VisualTokensTest(unittest.TestCase):
    def test_checked_in_sass_is_current(self) -> None:
        result = run_gate()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("POST3_VISUAL_TOKENS_CURRENT", result.stdout)

    def test_changed_token_rejects_stale_sass(self) -> None:
        with tempfile.TemporaryDirectory(prefix="post3-viz-token-") as directory:
            fixture = Path(directory)
            tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
            original = tokens["color"]["light"]["accent"]["$value"]
            tokens["color"]["light"]["accent"]["$value"] = {
                "colorSpace": "srgb", "components": [1.0, 1.0, 1.0],
                "alpha": 1, "hex": "#ffffff",
            }
            self.assertNotEqual(tokens["color"]["light"]["accent"]["$value"], original)
            mutated = fixture / "tokens.json"
            mutated.write_text(json.dumps(tokens), encoding="utf-8")
            stale = fixture / "stale.scss"
            stale.write_bytes(OUTPUT.read_bytes())
            result = run_gate(mutated, stale)
            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("POST3_VISUAL_TOKENS_STALE", result.stderr)

    def test_remote_runtime_dependency_fails_closed(self) -> None:
        with tempfile.TemporaryDirectory(prefix="post3-viz-remote-") as directory:
            fixture = Path(directory)
            tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
            tokens["$extensions"]["org.3cucharadas"]["runtimeRemoteDependencies"] = ["https://example.invalid/theme.css"]
            invalid = fixture / "tokens.json"
            invalid.write_text(json.dumps(tokens), encoding="utf-8")
            result = run_gate(invalid, fixture / "missing.scss")
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("runtimeRemoteDependencies debe ser []", result.stderr)

    def test_root_meta_is_rejected_by_official_schema(self) -> None:
        with tempfile.TemporaryDirectory(prefix="post3-viz-meta-") as directory:
            tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
            tokens["meta"] = tokens.pop("$extensions")["org.3cucharadas"]
            invalid = Path(directory) / "tokens.json"
            invalid.write_text(json.dumps(tokens), encoding="utf-8")
            result = run_gate(invalid)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("schema DTCG 2025.10", result.stderr)

    def test_official_schema_uses_its_declared_dialect_and_offline_refs(self) -> None:
        skill = ROOT.parents[1] / "penta-agent/skills/3cucharadas-visualizacion-datos"
        sys.path.insert(0, str(skill / "scripts"))
        from dtcg_format import _schema_validator  # noqa: PLC0415

        schema = json.loads((skill / "assets/dtcg/2025.10/format.json").read_text(encoding="utf-8"))
        self.assertEqual(schema["$schema"], "http://json-schema.org/draft-07/schema#")
        self.assertIs(validator_for(schema), Draft7Validator)
        self.assertIsInstance(_schema_validator(), Draft7Validator)

    def test_hex_component_disagreement_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="post3-viz-color-semantic-") as directory:
            tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
            tokens["color"]["light"]["accent"]["$value"]["components"][0] = 0.1
            invalid = Path(directory) / "tokens.json"
            invalid.write_text(json.dumps(tokens), encoding="utf-8")
            result = run_gate(invalid)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("difiere de hex", result.stderr)

    def test_string_color_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="post3-viz-string-") as directory:
            tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
            tokens["color"]["light"]["accent"]["$value"] = "#176b7b"
            invalid = Path(directory) / "tokens.json"
            invalid.write_text(json.dumps(tokens), encoding="utf-8")
            result = run_gate(invalid)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("schema DTCG 2025.10", result.stderr)

    def test_invalid_srgb_components_are_rejected(self) -> None:
        with tempfile.TemporaryDirectory(prefix="post3-viz-components-") as directory:
            tokens = json.loads(TOKENS.read_text(encoding="utf-8"))
            tokens["color"]["light"]["accent"]["$value"]["components"][0] = 2
            invalid = Path(directory) / "tokens.json"
            invalid.write_text(json.dumps(tokens), encoding="utf-8")
            result = run_gate(invalid)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("schema DTCG 2025.10", result.stderr)

    def test_css_mixin_binding_is_falsable(self) -> None:
        with tempfile.TemporaryDirectory(prefix="post3-viz-css-") as directory:
            css = Path(directory) / "main.scss"
            source = CSS.read_text(encoding="utf-8")
            self.assertIn("@include post3-viz.dark-theme;", source)
            css.write_text(source.replace("@include post3-viz.dark-theme;", "", 1), encoding="utf-8")
            result = run_gate(css=css)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("CSS Post III desacoplado", result.stderr)

    def test_focus_binding_uses_global_ring_contract(self) -> None:
        with tempfile.TemporaryDirectory(prefix="post3-viz-focus-") as directory:
            css = Path(directory) / "main.scss"
            source = CSS.read_text(encoding="utf-8")
            anchor = "--focus-ring: var(--c3-viz-focus);"
            self.assertIn(anchor, source)
            css.write_text(source.replace(anchor, "", 1), encoding="utf-8")
            result = run_gate(css=css)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn("CSS Post III desacoplado", result.stderr)

    def test_aggregate_manifest_rejects_stale_visual_identity_hash(self) -> None:
        with tempfile.TemporaryDirectory(prefix="post3-viz-manifest-") as directory:
            fixture = Path(directory) / "manifest.json"
            manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
            manifest["visual_identity"]["sha256"] = "0" * 64
            fixture.write_text(json.dumps(manifest), encoding="utf-8")

            result = run_gate(manifest=fixture)

            self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
            self.assertIn("POST3_VISUAL_TOKENS_MANIFEST_STALE", result.stderr)


if __name__ == "__main__":
    unittest.main()
