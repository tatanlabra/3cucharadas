#!/usr/bin/env python3
"""Build the six-point public coordinate audit used by thesis Post II."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/contracts/thesis-post-ii-viewer-coordinate-audit.yml"
CASES = ROOT / "assets/data/thesis-extension-post2/cases.json"
OUTPUT = ROOT / "assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.geojson"
MANIFEST = ROOT / "assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.manifest.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def osm_url(candidate: dict[str, Any]) -> str:
    return f"https://www.openstreetmap.org/{candidate['osm_type']}/{candidate['osm_id']}"


def point_feature(*, coordinates: list[float], properties: dict[str, Any]) -> dict[str, Any]:
    return {
        "type": "Feature",
        "geometry": {"type": "Point", "coordinates": coordinates},
        "properties": properties,
    }


def build(contract: dict[str, Any], cases: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    points = [point for case in cases["cases"] for point in case["points"]]
    by_rbd = {int(point["rbd"]): point for point in points}
    expected = [int(rbd) for rbd in contract["scope"]["expected_rbds"]]
    if len(points) != len(expected) or sorted(by_rbd) != sorted(expected):
        raise ValueError("the viewer no longer exposes exactly the six audited RBDs")
    decisions = {int(row["rbd"]): row for row in contract["decisions"]}
    if sorted(decisions) != sorted(expected):
        raise ValueError("every viewer point must have one audit decision")
    attribution = contract["sources"].get("osm_attribution", "")
    if "OpenStreetMap contributors" not in attribution:
        raise ValueError("OSM attribution is required")

    features: list[dict[str, Any]] = []
    counts = {"official": 0, "accepted_candidates": 0, "rejected_candidates": 0, "not_found": 0}
    preserved_dual_sources = 0
    for rbd in expected:
        official = by_rbd[rbd]
        decision = decisions[rbd]
        uses_candidate_in_viewer = official.get("coordinate_source_kind") == "osm_historical_site_candidate"
        if uses_candidate_in_viewer:
            required = ("official_latitude", "official_longitude", "official_coordinate_year")
            missing = [field for field in required if field not in official]
            if missing:
                raise ValueError(f"viewer candidate for RBD {rbd} lost official fields: {missing}")
            official_latitude = float(official["official_latitude"])
            official_longitude = float(official["official_longitude"])
            official_year = int(official["official_coordinate_year"])
            if (
                official_latitude == float(official["latitude"])
                and official_longitude == float(official["longitude"])
            ):
                raise ValueError(f"official observation for RBD {rbd} collides with the viewer candidate")
            preserved_dual_sources += 1
        else:
            official_latitude = float(official["latitude"])
            official_longitude = float(official["longitude"])
            official_year = int(official["coordinate_year"])
        shared = {
            "rbd": rbd,
            "role": official["role"],
            "school_name": official["name"],
            "event_year": int(official["event_year"]),
            "identity_status": decision["identity_status"],
            "spatial_status": decision["spatial_status"],
            "temporal_status": decision["temporal_status"],
            "final_status": decision["final_status"],
            "rationale_es": decision["rationale_es"],
            "rationale_en": decision["rationale_en"],
            "audit_observed_on": contract["observed_on"],
        }
        features.append(point_feature(
            coordinates=[official_longitude, official_latitude],
            properties={
                **shared,
                "observation_kind": "OFFICIAL_MINEDUC",
                "coordinate_year": official_year,
                "source_url": contract["sources"]["mineduc_directory_url"],
                "candidate_available": decision["candidate"] is not None,
                "used_as_viewer_point": not uses_candidate_in_viewer,
            },
        ))
        counts["official"] += 1
        candidate = decision["candidate"]
        if candidate is None:
            counts["not_found"] += 1
        else:
            features.append(point_feature(
                coordinates=[float(candidate["longitude"]), float(candidate["latitude"])],
                properties={
                    **shared,
                    "observation_kind": "OSM_CANDIDATE",
                    "osm_type": candidate["osm_type"],
                    "osm_id": int(candidate["osm_id"]),
                    "osm_url": osm_url(candidate),
                    "osm_name": candidate["name"],
                    "address_evidence": candidate["address"],
                    "official_distance_m": float(candidate["official_distance_m"]),
                    "candidate_disposition": "RETAINED_FOR_CONTRAST",
                    "used_as_viewer_point": uses_candidate_in_viewer,
                },
            ))
            counts["accepted_candidates"] += 1
        for rejected in decision.get("rejected_candidates", []):
            if float(rejected["official_distance_m"]) < 5_000:
                raise ValueError("a distant-homonym canary must remain at least 5 km away")
            features.append(point_feature(
                coordinates=[float(rejected["longitude"]), float(rejected["latitude"])],
                properties={
                    **shared,
                    "observation_kind": "OSM_REJECTED_CANDIDATE",
                    "osm_type": rejected["osm_type"],
                    "osm_id": int(rejected["osm_id"]),
                    "osm_url": osm_url(rejected),
                    "osm_name": rejected["name"],
                    "address_evidence": rejected["address"],
                    "official_distance_m": float(rejected["official_distance_m"]),
                    "candidate_disposition": rejected["disposition"],
                    "rejection_reason_es": rejected["reason_es"],
                    "rejection_reason_en": rejected["reason_en"],
                },
            ))
            counts["rejected_candidates"] += 1

    geojson = {
        "type": "FeatureCollection",
        "name": contract["audit_id"],
        "features": features,
        "metadata": {
            "schema_version": contract["schema_version"],
            "observed_on": contract["observed_on"],
            "method": contract["scope"]["method"],
            "limitations": contract["scope"]["limitations"],
            "sources": contract["sources"],
            "counts": counts,
        },
    }
    manifest = {
        "schema_version": 1,
        "audit_id": contract["audit_id"],
        "generated_by": "scripts/build_thesis_post2_viewer_coordinate_audit.py",
        "inputs": {
            str(CONTRACT.relative_to(ROOT)): sha256(CONTRACT),
            str(CASES.relative_to(ROOT)): sha256(CASES),
        },
        "counts": counts,
        "coverage": {"expected_rbds": expected, "audited_rbds": sorted(decisions)},
        "epistemic_status": {
            "official_coordinates_overwritten": preserved_dual_sources != 1,
            "dual_source_observations_preserved": preserved_dual_sources,
            "confirmed_official_errors": 0,
            "rbd_391": "high-confidence historical-site candidate with unresolved official-coordinate discrepancy",
        },
    }
    return geojson, manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    contract = yaml.safe_load(CONTRACT.read_text(encoding="utf-8"))
    cases = json.loads(CASES.read_text(encoding="utf-8"))
    geojson, manifest = build(contract, cases)
    payloads = {
        OUTPUT: json.dumps(geojson, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        MANIFEST: json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
    }
    if args.check:
        stale = [str(path.relative_to(ROOT)) for path, text in payloads.items() if not path.exists() or path.read_text(encoding="utf-8") != text]
        if stale:
            raise SystemExit("stale coordinate audit outputs: " + ", ".join(stale))
        return 0
    for path, text in payloads.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
