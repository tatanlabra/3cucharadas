from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path

try:
    import geopandas as gpd
    from shapely.geometry import GeometryCollection, Polygon
except ModuleNotFoundError:
    gpd = None


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = ROOT / "scripts" / "catastro_sii" / "build_pmtiles.py"
BUILD = None
if gpd is not None:
    SPEC = importlib.util.spec_from_file_location("build_pmtiles", MODULE_PATH)
    assert SPEC is not None and SPEC.loader is not None
    BUILD = importlib.util.module_from_spec(SPEC)
    sys.modules[SPEC.name] = BUILD
    SPEC.loader.exec_module(BUILD)


@unittest.skipUnless(gpd is not None, "La prueba geoespacial se ejecuta en python_base de stata01")
class PublicResidentialGeometryTests(unittest.TestCase):
    def test_nearest_rank_uses_a_conservative_index(self) -> None:
        assert BUILD is not None
        self.assertEqual(BUILD.nearest_rank([1, 2, 3, 4], 0.50), 2)
        self.assertEqual(BUILD.nearest_rank([1, 2, 3, 4], 0.95), 4)

    def test_empty_and_null_residential_geometries_are_audited_not_repaired(self) -> None:
        raw = gpd.GeoDataFrame(
            {"dc_cod_destino": ["H", "H", "H", "C"]},
            geometry=[
                Polygon([(0, 0), (1, 0), (1, 1), (0, 0)]),
                GeometryCollection(),
                None,
                Polygon([(2, 0), (3, 0), (3, 1), (2, 0)]),
            ],
            crs=4326,
        )

        assert BUILD is not None
        selected, counts = BUILD.select_public_residential_geometries(raw, "pilot")

        self.assertEqual(len(selected), 1)
        self.assertEqual(counts["residential_input"], 3)
        self.assertEqual(counts["excluded_empty_geometries"], 1)
        self.assertEqual(counts["excluded_null_geometries"], 1)

    def test_public_derivative_preserves_non_contiguous_selected_index(self) -> None:
        residential = gpd.GeoDataFrame(
            {"geometry": [Polygon([(0, 0), (1, 0), (1, 1), (0, 0)])]},
            index=[7],
            crs=4326,
        )

        assert BUILD is not None
        public = BUILD.public_parcel_frame(residential, "03102", "pilot", residential.crs)

        self.assertEqual(list(public.index), [7])
        self.assertEqual(set(public.columns), BUILD.PUBLIC_PARCEL_FIELDS)
        self.assertEqual(public.iloc[0].cod_comuna, "03102")

    def test_non_empty_invalid_residential_geometry_stops_build(self) -> None:
        raw = gpd.GeoDataFrame(
            {"dc_cod_destino": ["H"]},
            geometry=[Polygon([(0, 0), (1, 1), (1, 0), (0, 1), (0, 0)])],
            crs=4326,
        )

        with self.assertRaisesRegex(RuntimeError, "inválidas"):
            assert BUILD is not None
            BUILD.select_public_residential_geometries(raw, "pilot")
