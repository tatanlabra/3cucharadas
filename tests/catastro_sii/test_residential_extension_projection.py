"""Contract tests for the removable Avalúos II explanatory extension."""

import csv
import difflib
import hashlib
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/catastro_sii"))
from project_residential_extension import (  # noqa: E402
    POSTS,
    PROTECTED_REFERENCE_PATTERN,
    PUBLIC_FILES,
    baseline_post,
    check_projection,
    front_matter,
)

HISTORICAL_BASELINE = ROOT.parent / "catastros_sii/v5_brecha/artifacts/avaluos_ii_extension/baseline.json"
RELEASE_BASELINE = ROOT / "tests/catastro_sii/fixtures/avaluos_ii_release_baseline.json"


class ResidentialExtensionProjectionTest(unittest.TestCase):
    def test_projection_is_bound_and_protected_post_surfaces_remain(self):
        result = check_projection(
            ROOT / "assets/data/avaluos-ii-extension",
            ROOT / "_includes",
            RELEASE_BASELINE,
        )
        self.assertEqual(result["status"], "passed")
        self.assertEqual(set(result["public_data_sha256"]), set(PUBLIC_FILES))
        self.assertTrue(all(front_matter((ROOT / relative).read_text(encoding="utf-8")) for relative in result["posts_sha256"]))

    def test_release_anchor_preserves_historical_identity_and_references(self):
        release = json.loads(RELEASE_BASELINE.read_text(encoding="utf-8"))
        historical = json.loads(HISTORICAL_BASELINE.read_text(encoding="utf-8"))
        self.assertEqual(
            hashlib.sha256(HISTORICAL_BASELINE.read_bytes()).hexdigest(),
            release["historical_baseline_sha256"],
        )
        self.assertEqual(historical["blog_head"], release["historical_blog_head"])
        self.assertEqual(
            set(release["approved_front_matter_delta_sha256"]),
            {str(post.relative_to(ROOT)) for post in POSTS},
        )
        for post in POSTS:
            relative = str(post.relative_to(ROOT))
            original = baseline_post(historical["blog_head"], relative)
            approved = baseline_post(release["blog_head"], relative)
            original_front = front_matter(original)
            approved_front = front_matter(approved)
            delta = "".join(
                difflib.unified_diff(
                    original_front.splitlines(keepends=True),
                    approved_front.splitlines(keepends=True),
                    fromfile="historical",
                    tofile="approved",
                )
            )
            self.assertEqual(
                hashlib.sha256(delta.encode("utf-8")).hexdigest(),
                release["approved_front_matter_delta_sha256"][relative],
                relative,
            )
            for key in ("title", "date", "lang", "ref", "permalink"):
                pattern = rf"^{re.escape(key)}:.*$"
                self.assertEqual(
                    re.search(pattern, original_front, re.MULTILINE).group(),
                    re.search(pattern, approved_front, re.MULTILINE).group(),
                    f"{relative}: {key}",
                )
            self.assertEqual(
                sorted(PROTECTED_REFERENCE_PATTERN.findall(original)),
                sorted(PROTECTED_REFERENCE_PATTERN.findall(approved)),
                relative,
            )

    def test_public_projection_contains_only_selected_casen_aggregates(self):
        data = ROOT / "assets/data/avaluos-ii-extension"
        with (data / "casen-quantities.csv").open(encoding="utf-8", newline="") as source:
            rows = list(csv.DictReader(source))
        self.assertEqual([row["territory_code"] for row in rows], ["CL", "5101", "5109"])
        self.assertEqual(
            [
                (row["expanded_households"], row["expanded_residents"], row["sample_households"], row["sample_residents"])
                for row in rows
            ],
            [("77705", "200238", "787", "2020"), ("11359", "26410", "106", "249"), ("12251", "28558", "119", "280")],
        )
        public_text = "\n".join((data / name).read_text(encoding="utf-8") for name in PUBLIC_FILES)
        self.assertNotIn("/home/", public_text)
        self.assertNotIn("id_persona", public_text)
        self.assertNotIn("id_vivienda", public_text)
        self.assertNotIn("folio", public_text)
        provenance = json.loads((data / "provenance.json").read_text(encoding="utf-8"))
        self.assertFalse(provenance["private_paths_exported"])
        self.assertFalse(provenance["raw_rows_exported"])

    def test_editorial_claims_keep_units_and_original_rates_separate(self):
        es = (ROOT / "_includes/avaluos-ii-extension-es.html").read_text(encoding="utf-8")
        en = (ROOT / "_includes/avaluos-ii-extension-en.html").read_text(encoding="utf-8")
        for expected in ("77.705", "200.238", "76.493", "1,09 %", "9,27 %", "8,60 %"):
            self.assertIn(expected, es)
        for expected in ("77,705", "200,238", "76,493", "1.09%", "9.27%", "8.60%"):
            self.assertIn(expected, en)
        self.assertIn("no demuestra viviendas omitidas", es)
        self.assertIn("does not establish omitted dwellings", en)
        self.assertIn("Qué puede combinarse", es)
        self.assertIn("What can be combined", en)

    def test_hash_tampering_fails_closed(self):
        with tempfile.TemporaryDirectory() as temporary:
            scratch = Path(temporary)
            output = scratch / "data"
            includes = scratch / "includes"
            shutil.copytree(ROOT / "assets/data/avaluos-ii-extension", output)
            includes.mkdir()
            for lang in ("es", "en"):
                shutil.copyfile(ROOT / "_includes" / f"avaluos-ii-extension-{lang}.html", includes / f"avaluos-ii-extension-{lang}.html")
            (output / "method.md").write_text((output / "method.md").read_text(encoding="utf-8") + "altered\n", encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "hash mismatch"):
                check_projection(output, includes, RELEASE_BASELINE)

    def test_front_matter_tampering_fails_closed(self):
        original_read = Path.read_text

        def tampered_read(path, *args, **kwargs):
            source = original_read(path, *args, **kwargs)
            if path == POSTS[0]:
                return source.replace('title: "Avalúos en 3 cucharadas II:', 'title: "Alterado en 3 cucharadas II:', 1)
            return source

        with patch.object(Path, "read_text", tampered_read):
            with self.assertRaisesRegex(ValueError, "protected front matter changed"):
                check_projection(
                    ROOT / "assets/data/avaluos-ii-extension",
                    ROOT / "_includes",
                    RELEASE_BASELINE,
                )


if __name__ == "__main__":
    unittest.main()
