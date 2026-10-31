#!/usr/bin/env python3
"""Recompute every metric cited in the local CPU judges committee post from archived v2 receipts."""

from __future__ import annotations

import json
import math
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
REPORT_DIR = WORKSPACE_ROOT / "penta-agent" / "reports" / "simil-jev-panel"
RECEIPTS_DIR = REPORT_DIR / "receipts"


def wilson_ci_95(successes: int, total: int) -> tuple[float, float]:
    if total == 0:
        return (0.0, 0.0)
    z = 1.959963984540054
    phat = successes / total
    denom = 1.0 + (z * z) / total
    center = (phat + (z * z) / (2.0 * total)) / denom
    half = (z * math.sqrt((phat * (1.0 - phat) + (z * z) / (4.0 * total)) / total)) / denom
    return (center - half, center + half)


def vote(row: dict, threshold: float) -> str:
    if row.get("intrinsic_abstain"):
        return "indefinite"
    label = row["class_at_0_5"]
    conf = float(row["confidence"])
    if label in ("yes", "no") and conf >= threshold:
        return label
    return "indefinite"


def quorum(votes: list[str]) -> str:
    yes_count = sum(1 for v in votes if v == "yes")
    no_count = sum(1 for v in votes if v == "no")
    if yes_count >= 2:
        return "yes"
    if no_count >= 2:
        return "no"
    return "indefinite"


def main() -> int:
    eval_v2 = json.loads((RECEIPTS_DIR / "panel-evaluation-v2.json").read_text(encoding="utf-8"))
    cases_v2 = {
        c["id"]: c
        for c in json.loads((REPORT_DIR / "cases-v2.json").read_text(encoding="utf-8"))
    }
    laya_v2 = json.loads((RECEIPTS_DIR / "candidate-laya-v2.json").read_text(encoding="utf-8"))
    vega_v2 = json.loads((RECEIPTS_DIR / "candidate-vega-v2.json").read_text(encoding="utf-8"))
    arc_v2 = json.loads((RECEIPTS_DIR / "candidate-arc-v2.json").read_text(encoding="utf-8"))

    laya_preds = {r["id"]: r for r in laya_v2["rows"] if r["split"] == "test"}
    vega_preds = {r["id"]: r for r in vega_v2["rows"] if r["split"] == "test"}
    arc_preds = {r["id"]: r for r in arc_v2["rows"] if r["split"] == "test"}

    panel_th = eval_v2["thresholds"]["panel"]
    test_ids = sorted(laya_preds.keys())
    assert len(test_ids) == 160, f"Expected 160 test cases, got {len(test_ids)}"

    laya_panel_votes = {cid: vote(laya_preds[cid], panel_th["laya"]) for cid in test_ids}
    vega_panel_votes = {cid: vote(vega_preds[cid], panel_th["vega"]) for cid in test_ids}
    arc_panel_votes = {cid: vote(arc_preds[cid], panel_th["arc"]) for cid in test_ids}

    laya_yes = sum(1 for v in laya_panel_votes.values() if v == "yes")
    laya_yes_on_neg = sum(
        1 for cid, v in laya_panel_votes.items() if v == "yes" and cases_v2[cid]["expected"] == "no"
    )
    vega_no = sum(1 for v in vega_panel_votes.values() if v == "no")
    vega_yes = sum(1 for v in vega_panel_votes.values() if v == "yes")
    arc_decided = sum(1 for v in arc_panel_votes.values() if v in ("yes", "no"))
    arc_no = sum(1 for v in arc_panel_votes.values() if v == "no")

    opposite_laya_vega = sum(
        1
        for cid in test_ids
        if {laya_panel_votes[cid], vega_panel_votes[cid]} == {"yes", "no"}
    )

    neg_ids = [cid for cid in test_ids if cases_v2[cid]["expected"] == "no"]
    neg_vega_no = sum(1 for cid in neg_ids if vega_panel_votes[cid] == "no")
    neg_laya_no = sum(1 for cid in neg_ids if laya_panel_votes[cid] == "no")
    neg_arc_no = sum(1 for cid in neg_ids if arc_panel_votes[cid] == "no")
    neg_two_no = sum(
        1
        for cid in neg_ids
        if sum(1 for v in (laya_panel_votes[cid], vega_panel_votes[cid], arc_panel_votes[cid]) if v == "no") >= 2
    )

    panel_decisions = {
        cid: quorum([laya_panel_votes[cid], vega_panel_votes[cid], arc_panel_votes[cid]])
        for cid in test_ids
    }
    panel_correct_decided = [
        cid
        for cid, dec in panel_decisions.items()
        if dec in ("yes", "no") and dec == cases_v2[cid]["expected"]
    ]
    panel_decided_all = [cid for cid, dec in panel_decisions.items() if dec in ("yes", "no")]
    hit_families = {cases_v2[cid]["family_id"] for cid in panel_correct_decided}
    all_test_families = {cases_v2[cid]["family_id"] for cid in test_ids}

    ci_low, ci_high = wilson_ci_95(len(panel_correct_decided), len(panel_decided_all))
    always_indef_acc = sum(1 for cid in test_ids if cases_v2[cid]["expected"] == "indefinite") / len(test_ids)

    summary = {
        "test_cases": len(test_ids),
        "panel_votes": {
            "laya_yes_of_160": laya_yes,
            "laya_yes_on_60_negatives": laya_yes_on_neg,
            "vega_no_of_160": vega_no,
            "vega_yes_of_160": vega_yes,
            "arc_decided_of_160": arc_decided,
            "arc_no_of_160": arc_no,
            "laya_vs_vega_opposite_of_160": opposite_laya_vega,
        },
        "negative_class_60": {
            "vega_no": neg_vega_no,
            "laya_no": neg_laya_no,
            "arc_no": neg_arc_no,
            "cases_with_at_least_two_no_votes": neg_two_no,
        },
        "panel_quorum": {
            "decided": len(panel_decided_all),
            "correct": len(panel_correct_decided),
            "selective_accuracy": round(len(panel_correct_decided) / len(panel_decided_all), 4),
            "wilson_95_ci_pct": [round(ci_low * 100, 1), round(ci_high * 100, 1)],
            "hit_families_count": len(hit_families),
            "total_test_families": len(all_test_families),
            "always_indefinite_three_way_pct": round(always_indef_acc * 100, 2),
        },
        "resources": {
            "laya_gib": round(laya_v2["resource"]["peak_rss_bytes"] / (1024**3), 2),
            "laya_cold_s": round(laya_v2["latency_seconds"]["cold_end_to_end_first_result"], 2),
            "laya_warm_p95_ms": round(laya_v2["latency_seconds"]["p95"] * 1000),
            "vega_gib": round(vega_v2["resource"]["peak_rss_bytes"] / (1024**3), 2),
            "vega_cold_s": round(vega_v2["latency_seconds"]["cold_end_to_end_first_result"], 2),
            "vega_warm_p95_ms": round(vega_v2["latency_seconds"]["p95"] * 1000),
            "arc_gib": round(arc_v2["resource"]["peak_rss_bytes"] / (1024**3), 2),
            "arc_cold_s": round(arc_v2["latency_seconds"]["cold_end_to_end_first_result"], 2),
            "arc_warm_p95_ms": round(arc_v2["latency_seconds"]["p95"] * 1000),
        },
    }

    assert laya_yes == 125 and laya_yes_on_neg == 48
    assert vega_no == 131 and vega_yes == 4
    assert arc_decided == 12 and arc_no == 0
    assert opposite_laya_vega == 101
    assert (neg_vega_no, neg_laya_no, neg_arc_no, neg_two_no) == (53, 1, 0, 0)
    assert len(hit_families) == 4 and len(all_test_families) == 40
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
