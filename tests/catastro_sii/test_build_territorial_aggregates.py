from __future__ import annotations

import importlib.util
import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "catastro_sii" / "build_territorial_aggregates.py"
SPEC = importlib.util.spec_from_file_location("build_territorial_aggregates", MODULE_PATH)
assert SPEC is not None and SPEC.loader is not None
BUILD = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = BUILD
SPEC.loader.exec_module(BUILD)


class TerritorialAggregatesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.payload = BUILD.aggregate()

    def test_contract_counts_and_null_communes(self) -> None:
        national = self.payload["national"]
        self.assertEqual(national["n_comunas"], 346)
        self.assertEqual(national["n_regiones"], 16)
        self.assertEqual(national["n_comunas_con_avm2"], 340)
        self.assertEqual(
            national["comunas_sin_avm2"],
            ["05201", "11303", "12102", "12103", "12104", "12202"],
        )
        self.assertEqual(len(self.payload["communes"]), 346)
        self.assertEqual(len(self.payload["regions"]), 16)

    def test_preserves_valparaiso_and_uses_canonical_commune_labels(self) -> None:
        self.assertIn("Valparaíso", self.payload["regions"])
        valparaiso = self.payload["communes"]["05101"]
        self.assertEqual(valparaiso["comuna"], "Valparaíso")
        self.assertEqual(valparaiso["region"], "Valparaíso")

    def test_positive_avm2_communes_receive_quartile_and_regional_median(self) -> None:
        diego = self.payload["communes"]["03202"]
        self.assertEqual(diego["codigo_comuna_dato"], "3202")
        self.assertEqual(diego["cuartil_nacional_avm2"], 3)
        self.assertIsNotNone(diego["avm2_mediana"])
        self.assertIsNotNone(diego["mediana_regional_avm2"])
        self.assertIs(diego["sobre_mediana_regional"], False)

    def test_reconciles_tabular_and_published_uv_universes(self) -> None:
        note = self.payload["technical_notes"]["uv_universe_reconciliation"]
        self.assertEqual(note["insights_v1_uv"], 6891)
        self.assertEqual(note["published_uv_features"], 6888)
        self.assertEqual(note["difference"], 3)
        self.assertEqual(
            [row["uv_rsh"] for row in note["not_navigable_uv"]],
            [43018092, 101054603, 162037323],
        )

    def test_no_predial_rows_or_geometry_are_serialized(self) -> None:
        BUILD.assert_contract(self.payload)
        rendered = json.dumps(self.payload, ensure_ascii=False)
        for forbidden in ("predio", "pred_uid", "rol", "rut", "run", "direccion", "geometry", "coordinates", "avaluo_fiscal_clp"):
            self.assertNotIn(f'"{forbidden}"', rendered)


if __name__ == "__main__":
    unittest.main()
