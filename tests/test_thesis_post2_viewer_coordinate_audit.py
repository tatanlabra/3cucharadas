import copy
import importlib.util
import json
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location(
    "viewer_coordinate_audit", ROOT / "scripts/build_thesis_post2_viewer_coordinate_audit.py"
)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC.loader
SPEC.loader.exec_module(MODULE)


@pytest.fixture()
def inputs():
    contract = yaml.safe_load(MODULE.CONTRACT.read_text(encoding="utf-8"))
    cases = json.loads(MODULE.CASES.read_text(encoding="utf-8"))
    return contract, cases


def test_all_primary_case_points_have_a_decision(inputs):
    geojson, manifest = MODULE.build(*inputs)
    assert manifest["coverage"]["expected_rbds"] == [391, 390]
    assert manifest["counts"] == {"official": 2, "accepted_candidates": 2, "rejected_candidates": 1, "not_found": 0}
    assert len(geojson["features"]) == 5


def test_only_reviewed_and_flagged_primary_case_is_public(inputs):
    geojson, _ = MODULE.build(*inputs)
    assert {f["properties"]["rbd"] for f in geojson["features"]} == {390, 391}
    assert {f["properties"]["final_status"] for f in geojson["features"]} == {"PLAUSIBLE", "DISCREPANCY"}


def test_school_14_is_not_silently_overwritten(inputs):
    geojson, manifest = MODULE.build(*inputs)
    rows = [f for f in geojson["features"] if f["properties"]["rbd"] == 391]
    assert {r["properties"]["observation_kind"] for r in rows} == {
        "OFFICIAL_MINEDUC", "OSM_CANDIDATE", "OSM_REJECTED_CANDIDATE"
    }
    accepted = next(r for r in rows if r["properties"]["observation_kind"] == "OSM_CANDIDATE")
    official = next(r for r in rows if r["properties"]["observation_kind"] == "OFFICIAL_MINEDUC")
    assert accepted["properties"]["osm_id"] == 1122520465
    assert accepted["properties"]["identity_status"] == "PLAUSIBLE"
    assert accepted["properties"]["temporal_status"] == "RETROSPECTIVE_UNVERIFIED"
    assert accepted["properties"]["used_as_viewer_point"] is True
    assert official["geometry"]["coordinates"] == [-69.627083, -26.244385]
    assert official["properties"]["coordinate_year"] == 2015
    assert official["properties"]["source_url"].startswith("https://datosabiertos.mineduc.cl/")
    assert official["geometry"] != accepted["geometry"]
    assert manifest["epistemic_status"]["official_coordinates_overwritten"] is False
    assert manifest["epistemic_status"]["dual_source_observations_preserved"] == 1


def test_distant_homonym_is_rejected(inputs):
    geojson, _ = MODULE.build(*inputs)
    rejected = next(f["properties"] for f in geojson["features"] if f["properties"].get("osm_id") == 991314175)
    assert rejected["candidate_disposition"] == "REJECTED_DISTANT_HOMONYM"
    assert rejected["official_distance_m"] > 45_000


def test_red_canary_missing_rbd_391_fails(inputs):
    contract, cases = copy.deepcopy(inputs)
    contract["decisions"] = [row for row in contract["decisions"] if row["rbd"] != 391]
    with pytest.raises(ValueError, match="every viewer point"):
        MODULE.build(contract, cases)


def test_red_canary_missing_osm_attribution_fails(inputs):
    contract, cases = copy.deepcopy(inputs)
    contract["sources"]["osm_attribution"] = ""
    with pytest.raises(ValueError, match="attribution"):
        MODULE.build(contract, cases)


def test_red_canary_near_homonym_fails(inputs):
    contract, cases = copy.deepcopy(inputs)
    school_14 = next(row for row in contract["decisions"] if row["rbd"] == 391)
    school_14["rejected_candidates"][0]["official_distance_m"] = 100
    with pytest.raises(ValueError, match="homonym"):
        MODULE.build(contract, cases)


def test_red_canary_school_14_official_point_collision_fails(inputs):
    contract, cases = copy.deepcopy(inputs)
    school_14 = next(point for case in cases["cases"] for point in case["points"] if point["rbd"] == 391)
    school_14["official_latitude"] = school_14["latitude"]
    school_14["official_longitude"] = school_14["longitude"]
    with pytest.raises(ValueError, match="collides"):
        MODULE.build(contract, cases)
