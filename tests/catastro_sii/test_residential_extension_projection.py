"""Contract tests for the removable Avalúos II explanatory extension."""

import csv
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "scripts/catastro_sii"))
from project_residential_extension import (  # noqa: E402
    PUBLIC_FILES,
    check_projection,
    front_matter,
)

BASELINE = ROOT.parent / "catastros_sii/v5_brecha/artifacts/avaluos_ii_extension/baseline.json"


class ResidentialExtensionProjectionTest(unittest.TestCase):
    def test_projection_is_bound_and_protected_post_surfaces_remain(self):
        result = check_projection(
            ROOT / "assets/data/avaluos-ii-extension",
            ROOT / "_includes",
            BASELINE,
        )
        self.assertEqual(result["status"], "passed")
        self.assertEqual(set(result["public_data_sha256"]), set(PUBLIC_FILES))
        self.assertTrue(all(front_matter((ROOT / relative).read_text(encoding="utf-8")) for relative in result["posts_sha256"]))

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
                check_projection(output, includes, BASELINE)


if __name__ == "__main__":
    unittest.main()
