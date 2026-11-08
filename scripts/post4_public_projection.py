"""Bounded public projection of frozen Post IV descriptive aggregates.

The private aggregate files remain inputs only. This module has no microdata
dependency and the validator can be copied to a public build environment.
Passing validation closes documented arithmetic disclosure channels for this
exact pair of source hashes; it does not certify anonymity against external data.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import os
import re
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal
from pathlib import Path
from typing import Any

PRIMARY_SHA256 = "8d53186740353a50bf6af82254356ffc2fea39bf2f76c9bfb810700d1189f763"
SENSITIVITY_SHA256 = "3bb9129e31a2ff1143c86b8b7b9af34c7da96542578c6c00e440f547eb2088a7"
PROTOCOL_SHA256 = "099afeec717ba08f0d962cfbdc44acd444ba5224f714a0391cdee7c057edf07f"
STATUS = "PUBLIC_POST4_DESCRIPTIVE_PROJECTION"
POLICY = "POST4_COMBINED_PRIVACY_REVIEW_R1_ALLOWLIST"
EXPECTED_COUNTS = {
    "results": 2075,
    "primary_results": 138,
    "sensitivity_results": 1937,
    "coverage": 5040,
    "primary_coverage": 48,
    "sensitivity_coverage": 4992,
    "outcome_coverage": 384,
    "result_key_status": 2200,
    "heterogeneity_contrasts": 800,
    "placebo_coverage": 768,
    "temporal_window_metadata": 144,
}
SOURCE_SHA256 = {
    "primary_aggregate": PRIMARY_SHA256,
    "sensitivity_aggregate": SENSITIVITY_SHA256,
}
EXPECTED_CANONICAL_PUBLIC_SHA256: str | None = (
    "c06aaae2dd8ddf7165e826f10e2f5d39140b1bf19da46cd9dc9fc985f33e99c0"
)
EXCLUDED_FIELDS = (
    "results[*].rates except primary pooled any_he_2yr historical/modern",
    "results[*].n_treated except primary pooled any_he_2yr historical/modern",
    "results[*].n_control except primary pooled any_he_2yr historical/modern",
    "results[*].student_clusters",
    "coverage[*].*_rows",
    "exclusion_qa[*].excluded_records",
    "variant_quality[*].retained_future_student_cohort_rows",
    "future_baseline_quality.future_student_cohort_rows",
    "all other QA person counts and private metadata",
)
REDACTIONS = {
    "arm_rates": "null_except_two_primary_pooled_any_he_2yr_rows",
    "exact_person_denominators": "null_except_two_primary_pooled_any_he_2yr_rows",
    "qa_person_counts": "omitted_by_allowlist",
    "school_counts": "retained_for_precision_not_person_privacy",
}
LIMITATION = (
    "Descriptive estimates only; temporal and selection diagnostics do not "
    "identify a causal effect. This projection closes measured arithmetic "
    "small-cell channels for the pinned sources, not global reidentification risk."
)
OUTCOMES = frozenset({
    "any_he_2yr", "any_he_exact", "university_only_2yr",
    "ip_cft_only_2yr", "both_2yr", "none_2yr",
    "persistence_3yr", "graduation_6yr",
})
ARM_RATE_KEYS = frozenset({
    "treated_post", "treated_pre", "control_post", "control_pre",
})
RESULT_FIELDS = frozenset({
    "variant", "outcome", "era", "cohort", "cohort_range",
    "candidate_range", "estimand", "estimate_pp", "ci_low_pp",
    "ci_high_pp", "se_pp", "confidence_level", "estimation_status",
    "identification_status", "flags", "limitation", "data_status",
    "treated_schools", "control_schools", "school_clusters", "strata",
    "effective_treated_schools", "max_treated_school_share",
    "variance_ratio_to_school_CR0", "axis", "value", "calendar_rule",
    "causal_diagnostic_status", "cohort_generation_label",
    "contrast_cohorts", "pre_post_slot_semantics", "linkage_bounds",
    "bootstrap",
    "rates", "n_treated", "n_control",
})
COVERAGE_FIELDS = frozenset({
    "variant", "outcome", "taxonomy", "cohort", "g", "grade",
    "status", "calendar_primary_mature", "calendar_mature",
    "treated_schools", "control_schools", "window_end_rel_G_older",
    "window_end_rel_G_newer", "both_windows_strictly_before_G",
    "exact_supported_strata", "has_future_control_contribution",
})
OUTCOME_COVERAGE_FIELDS = frozenset({
    "outcome", "g", "grade", "taxonomy", "status", "calendar_mature",
    "treated_schools", "control_schools",
})
STATUS_FIELDS = frozenset({
    "variant", "outcome", "taxonomy", "cohort", "axis", "value",
    "estimation_status", "result_present",
})
CONTRAST_FIELDS = frozenset({
    "outcome", "era", "axis", "left_value", "right_value", "family",
    "family_size_prespecified", "estimate_difference_pp",
    "ci_low_pp_unadjusted", "ci_high_pp_unadjusted",
    "p_value_unadjusted", "p_value_holm", "estimation_status",
    "identification_status",
})
PLACEBO_COVERAGE_FIELDS = frozenset({
    "comparison", "era", "g", "grade", "outcome", "status",
    "treated_schools", "control_schools", "window_end_rel_G_older",
    "window_end_rel_G_newer", "both_windows_strictly_before_G",
})
TEMPORAL_FIELDS = frozenset({
    "outcome", "grade", "comparison", "slot", "baseline_year_rel_G",
    "window_start_rel_G", "window_end_rel_G", "crosses_G",
    "ends_at_or_after_G", "slot_semantics",
})
LINKAGE_FIELDS = frozenset({
    "low_pp", "high_pp", "vacuous_source_capacity", "capacity_scope",
})
BOOTSTRAP_FIELDS = frozenset({
    "method", "repetitions", "seed", "shared_school_weights",
})
TOP_LEVEL_FIELDS = frozenset({
    "schema_version", "status", "metadata", "source_sha256",
    "projection", "excluded_fields", "redactions", "limitation",
    "results", "coverage", "outcome_coverage", "result_key_status",
    "heterogeneity_contrasts", "placebo_coverage",
    "temporal_window_metadata", "not_run",
})
PRIVATE_TEXT_PATTERN = re.compile(
    r"(?i)(?:/(?:home|tmp|mnt|media)/|\.(?:csv|parquet|duckdb)(?:\b|$)"
    r"|\b\d+\s+(?:students?|persons?|alumnos?|personas|rows?|records?)\b"
    r"|\b(?:n|rows?|students?|persons?|alumnos?|personas|records?)"
    r"\s*[:=]\s*\d+\b)"
)


class PublicProjectionError(ValueError):
    """The requested export violates the frozen public projection contract."""


def _require(condition: bool, reason: str) -> None:
    if not condition:
        raise PublicProjectionError(reason)


def _public_figure_row(row: dict[str, Any]) -> bool:
    return (
        row.get("variant") == "primary"
        and row.get("outcome") == "any_he_2yr"
        and row.get("cohort") is None
        and row.get("era") in ("historical", "modern")
    )


def _copy_fields(row: dict[str, Any], allowed: frozenset[str]) -> dict[str, Any]:
    return {key: value for key, value in row.items() if key in allowed}


def _project_result(row: dict[str, Any], *, primary: bool) -> dict[str, Any]:
    projected = _copy_fields(row, RESULT_FIELDS - {"rates", "n_treated", "n_control"})
    projected["variant"] = "primary" if primary else row["variant"]
    if _public_figure_row(projected):
        projected["rates"] = _copy_fields(row["rates"], ARM_RATE_KEYS)
        projected["n_treated"] = row["n_treated"]
        projected["n_control"] = row["n_control"]
    else:
        projected["rates"] = None
        projected["n_treated"] = None
        projected["n_control"] = None
    if "linkage_bounds" in projected and projected["linkage_bounds"] is not None:
        projected["linkage_bounds"] = _copy_fields(
            projected["linkage_bounds"], LINKAGE_FIELDS
        )
    if "bootstrap" in projected and projected["bootstrap"] is not None:
        projected["bootstrap"] = _copy_fields(
            projected["bootstrap"], BOOTSTRAP_FIELDS
        )
    return projected


def _check_input_counts(primary: dict[str, Any], sensitivity: dict[str, Any]) -> None:
    for label, section, key in (
        ("primary_results", primary, "results"),
        ("sensitivity_results", sensitivity, "results"),
        ("primary_coverage", primary, "coverage"),
        ("sensitivity_coverage", sensitivity, "coverage"),
        ("outcome_coverage", primary, "outcome_coverage"),
        ("result_key_status", sensitivity, "result_key_status"),
        ("heterogeneity_contrasts", sensitivity, "heterogeneity_contrasts"),
        ("placebo_coverage", sensitivity, "placebo_coverage"),
        ("temporal_window_metadata", sensitivity, "temporal_window_metadata"),
    ):
        _require(isinstance(section.get(key), list), f"Input {label} is not a list")
        _require(len(section[key]) == EXPECTED_COUNTS[label], f"Input {label} count drift")
    for section in (primary, sensitivity):
        _require(
            section.get("metadata", {}).get("protocol_sha256") == PROTOCOL_SHA256,
            "Input protocol binding drift",
        )


def project_public(
    primary: dict[str, Any], sensitivity: dict[str, Any],
    *, source_sha256: dict[str, str],
) -> dict[str, Any]:
    """Project parsed aggregates; callers must authenticate bytes separately.

    Use :func:`project_files` for a provenance-bound production call.
    """
    _require(source_sha256 == SOURCE_SHA256, "Unreviewed aggregate source hashes")
    _check_input_counts(primary, sensitivity)
    results = [
        *(_project_result(row, primary=True) for row in primary["results"]),
        *(_project_result(row, primary=False) for row in sensitivity["results"]),
    ]
    coverage = [
        *({"variant": "primary", **_copy_fields(row, COVERAGE_FIELDS)}
          for row in primary["coverage"]),
        *(_copy_fields(row, COVERAGE_FIELDS) for row in sensitivity["coverage"]),
    ]
    payload = {
        "schema_version": 1,
        "status": STATUS,
        "metadata": {"protocol_sha256": PROTOCOL_SHA256},
        "source_sha256": dict(SOURCE_SHA256),
        "projection": {
            "policy": POLICY,
            "source_sha256": dict(SOURCE_SHA256),
        },
        "excluded_fields": list(EXCLUDED_FIELDS),
        "redactions": dict(REDACTIONS),
        "limitation": LIMITATION,
        "results": results,
        "coverage": coverage,
        "outcome_coverage": [
            _copy_fields(row, OUTCOME_COVERAGE_FIELDS)
            for row in primary["outcome_coverage"]
        ],
        "result_key_status": [
            _copy_fields(row, STATUS_FIELDS)
            for row in sensitivity["result_key_status"]
        ],
        "heterogeneity_contrasts": [
            _copy_fields(row, CONTRAST_FIELDS)
            for row in sensitivity["heterogeneity_contrasts"]
        ],
        "placebo_coverage": [
            _copy_fields(row, PLACEBO_COVERAGE_FIELDS)
            for row in sensitivity["placebo_coverage"]
        ],
        "temporal_window_metadata": [
            _copy_fields(row, TEMPORAL_FIELDS)
            for row in sensitivity["temporal_window_metadata"]
        ],
        "not_run": _copy_fields(sensitivity["not_run"], frozenset({"blp_gate_clan"})),
    }
    validate_public_projection(payload)
    return payload


def project_files(primary_path: Path, sensitivity_path: Path) -> dict[str, Any]:
    """Authenticate exact frozen file bytes and return an in-memory projection."""
    sources = {}
    for label, path in (
        ("primary_aggregate", Path(primary_path)),
        ("sensitivity_aggregate", Path(sensitivity_path)),
    ):
        sources[label] = hashlib.sha256(path.read_bytes()).hexdigest()
    _require(sources == SOURCE_SHA256, "Unreviewed aggregate source bytes")
    primary = json.loads(Path(primary_path).read_text())
    sensitivity = json.loads(Path(sensitivity_path).read_text())
    return project_public(primary, sensitivity, source_sha256=sources)


def _safe_rounded_successes(
    n: int, rate: float, *, require_integer: bool = False,
) -> None:
    """Reject a 1–9 numerator or complement under the published rate interval."""
    _require(type(n) is int and n >= 10, "Figure denominator is not a safe integer")
    _require(
        type(rate) in (int, float) and math.isfinite(rate) and 0 <= rate <= 100,
        "Figure arm rate invalid",
    )
    percentage = Decimal(str(rate))
    delta = Decimal("0.000005")
    lower = Decimal(n) * (percentage - delta) / Decimal(100)
    upper = Decimal(n) * (percentage + delta) / Decimal(100)
    first = int(lower.to_integral_value(rounding=ROUND_CEILING))
    last = int(upper.to_integral_value(rounding=ROUND_FLOOR))
    if require_integer:
        _require(first <= last, "Figure treated-post rate lacks an integer numerator")
    for numerator in range(first, last + 1):
        _require(
            not (1 <= numerator <= 9 or 1 <= n - numerator <= 9),
            "Figure arm rate reconstructs a protected small outcome",
        )


def _canonical_sha256(payload: dict[str, Any]) -> str:
    encoded = json.dumps(
        payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"),
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def _validate_public_scalars(value: Any) -> None:
    if isinstance(value, dict):
        _require(all(isinstance(key, str) for key in value),
                 "Public object key is not text")
        for member in value.values():
            _validate_public_scalars(member)
    elif isinstance(value, list):
        for member in value:
            _validate_public_scalars(member)
    elif isinstance(value, str):
        _require(not PRIVATE_TEXT_PATTERN.search(value),
                 "Public free text contains a private path or person count")
    elif isinstance(value, float):
        _require(math.isfinite(value), "Public numeric value is not finite")
    else:
        _require(value is None or type(value) in (bool, int),
                 "Public scalar has unsupported type")


def _validate_rows(rows: Any, count: int, allowed: frozenset[str], name: str) -> None:
    _require(isinstance(rows, list) and len(rows) == count, f"{name} count drift")
    for row in rows:
        _require(isinstance(row, dict), f"{name} row is not an object")
        _require(set(row) <= allowed, f"{name} contains unreviewed fields")


def validate_public_projection(payload: dict[str, Any]) -> None:
    """Fail closed on the entire flat public projection, with no private input."""
    _require(isinstance(payload, dict), "Public projection is not an object")
    _validate_public_scalars(payload)
    _require(set(payload) == TOP_LEVEL_FIELDS, "Public top-level fields drift")
    _require(payload["schema_version"] == 1 and payload["status"] == STATUS,
             "Public projection status drift")
    _require(payload["metadata"] == {"protocol_sha256": PROTOCOL_SHA256},
             "Public protocol binding drift")
    _require(payload["source_sha256"] == SOURCE_SHA256, "Public source hash drift")
    _require(payload["projection"] == {
        "policy": POLICY, "source_sha256": SOURCE_SHA256,
    }, "Public projection policy drift")
    _require(payload["excluded_fields"] == list(EXCLUDED_FIELDS),
             "Public exclusion manifest drift")
    _require(payload["redactions"] == REDACTIONS,
             "Public redaction manifest drift")
    _require(payload["limitation"] == LIMITATION,
             "Public limitation drift")
    _validate_rows(payload["results"], EXPECTED_COUNTS["results"],
                   RESULT_FIELDS, "results")
    _validate_rows(payload["coverage"], EXPECTED_COUNTS["coverage"],
                   COVERAGE_FIELDS, "coverage")
    _validate_rows(payload["outcome_coverage"], EXPECTED_COUNTS["outcome_coverage"],
                   OUTCOME_COVERAGE_FIELDS, "outcome_coverage")
    _validate_rows(payload["result_key_status"], EXPECTED_COUNTS["result_key_status"],
                   STATUS_FIELDS, "result_key_status")
    _validate_rows(payload["heterogeneity_contrasts"],
                   EXPECTED_COUNTS["heterogeneity_contrasts"],
                   CONTRAST_FIELDS, "heterogeneity_contrasts")
    _validate_rows(payload["placebo_coverage"], EXPECTED_COUNTS["placebo_coverage"],
                   PLACEBO_COVERAGE_FIELDS, "placebo_coverage")
    _validate_rows(payload["temporal_window_metadata"],
                   EXPECTED_COUNTS["temporal_window_metadata"],
                   TEMPORAL_FIELDS, "temporal_window_metadata")
    _require(isinstance(payload["not_run"], dict)
             and set(payload["not_run"]) <= {"blp_gate_clan"},
             "Public not-run fields drift")

    figure_eras = []
    primary_results = 0
    sensitivity_results = 0
    for row in payload["results"]:
        _require(row.get("outcome") in OUTCOMES
                 and isinstance(row.get("variant"), str)
                 and isinstance(row.get("estimation_status"), str),
                 "Result analytic key/status missing")
        if row["variant"] == "primary":
            primary_results += 1
        else:
            sensitivity_results += 1
        for key in ("rates", "n_treated", "n_control"):
            _require(key in row, f"Result {key} missing from projection schema")
        if row["estimation_status"] != "NOT_ESTIMABLE_TEMPORAL_OVERLAP":
            _require({"estimate_pp", "ci_low_pp", "ci_high_pp"} <= set(row),
                     "Result estimate or interval fields missing")
        if _public_figure_row(row):
            figure_eras.append(row["era"])
            rates = row["rates"]
            _require(isinstance(rates, dict) and set(rates) == ARM_RATE_KEYS,
                     "Figure four arm rates missing or changed")
            _require(type(row["n_control"]) is int and row["n_control"] >= 10,
                     "Figure control denominator invalid")
            for rate in rates.values():
                _require(type(rate) in (int, float) and math.isfinite(rate)
                         and 0 <= rate <= 100, "Figure arm rate invalid")
            for arm, denominator in (
                ("treated_post", row["n_treated"]),
                ("treated_pre", row["n_treated"]),
                ("control_post", row["n_control"]),
                ("control_pre", row["n_control"]),
            ):
                _safe_rounded_successes(
                    denominator, rates[arm], require_integer=arm == "treated_post",
                )
        else:
            _require(
                row["rates"] is None and row["n_treated"] is None
                and row["n_control"] is None,
                "Nonfigure row exposes arm rates or exact person counts",
            )
        bounds = row.get("linkage_bounds")
        _require(bounds is None or (isinstance(bounds, dict)
                 and set(bounds) <= LINKAGE_FIELDS),
                 "Unreviewed linkage bounds fields")
        bootstrap = row.get("bootstrap")
        _require(bootstrap is None or (isinstance(bootstrap, dict)
                 and set(bootstrap) <= BOOTSTRAP_FIELDS),
                 "Unreviewed bootstrap fields")
    _require(primary_results == EXPECTED_COUNTS["primary_results"]
             and sensitivity_results == EXPECTED_COUNTS["sensitivity_results"],
             "Result family counts drift")
    _require(sorted(figure_eras) == ["historical", "modern"],
             "Exactly two pooled access figure rows required")

    primary_coverage = payload["coverage"][:EXPECTED_COUNTS["primary_coverage"]]
    sensitivity_coverage = payload["coverage"][EXPECTED_COUNTS["primary_coverage"]:]
    _require(all(row.get("variant") == "primary" for row in primary_coverage),
             "Primary coverage source order drift")
    _require(len(sensitivity_coverage) == EXPECTED_COUNTS["sensitivity_coverage"],
             "Sensitivity coverage count drift")
    for row in payload["coverage"]:
        _require("variant" in row and ("g" in row or "cohort" in row)
                 and "grade" in row
                 and "status" in row, "Coverage analytic key/status missing")
    for row in payload["outcome_coverage"]:
        _require("outcome" in row and "g" in row and "grade" in row
                 and "status" in row, "Outcome coverage key/status missing")
    for row in payload["result_key_status"]:
        _require(set(STATUS_FIELDS) <= set(row),
                 "Result inventory key/status missing")
    for row in payload["heterogeneity_contrasts"]:
        _require(set(CONTRAST_FIELDS) <= set(row),
                 "Heterogeneity contrast fields missing")
    for row in payload["temporal_window_metadata"]:
        _require(set(TEMPORAL_FIELDS) <= set(row),
                 "Temporal window metadata missing")
    if EXPECTED_CANONICAL_PUBLIC_SHA256 is not None:
        _require(_canonical_sha256(payload) == EXPECTED_CANONICAL_PUBLIC_SHA256,
                 "Public projection exact-content digest drift")


def split_public_projection(payload: dict[str, Any]) -> dict[str, dict[str, Any]]:
    """Return the two consumer-shaped views of one validated combined object."""
    validate_public_projection(payload)
    common = {
        "schema_version": 1,
        "status": STATUS,
        "metadata": dict(payload["metadata"]),
        "excluded_fields": list(payload["excluded_fields"]),
        "redactions": dict(payload["redactions"]),
        "limitation": payload["limitation"],
    }
    primary = {
        **common,
        "source_sha256": PRIMARY_SHA256,
        "projection": {
            "policy": POLICY, "source_sha256": PRIMARY_SHA256,
        },
        "results": [row for row in payload["results"]
                    if row["variant"] == "primary"],
        "coverage": payload["coverage"][:EXPECTED_COUNTS["primary_coverage"]],
        "outcome_coverage": payload["outcome_coverage"],
    }
    sensitivity = {
        **common,
        "source_sha256": SENSITIVITY_SHA256,
        "projection": {
            "policy": POLICY, "source_sha256": SENSITIVITY_SHA256,
        },
        "results": [row for row in payload["results"]
                    if row["variant"] != "primary"],
        "coverage": payload["coverage"][EXPECTED_COUNTS["primary_coverage"]:],
        "result_key_status": payload["result_key_status"],
        "heterogeneity_contrasts": payload["heterogeneity_contrasts"],
        "placebo_coverage": payload["placebo_coverage"],
        "temporal_window_metadata": payload["temporal_window_metadata"],
        "not_run": payload["not_run"],
    }
    parts = copy.deepcopy({"primary": primary, "sensitivity": sensitivity})
    validate_split_public_projection(parts)
    return parts


def validate_split_public_projection(parts: dict[str, Any]) -> None:
    """Check both consumer views together; neither view gets a weaker gate."""
    _require(isinstance(parts, dict) and set(parts) == {"primary", "sensitivity"},
             "Split public projection sections drift")
    primary, sensitivity = parts["primary"], parts["sensitivity"]
    _require(isinstance(primary, dict) and isinstance(sensitivity, dict),
             "Split public projection section invalid")
    common_fields = {
        "schema_version", "status", "metadata", "excluded_fields",
        "redactions", "limitation", "source_sha256", "projection",
        "results", "coverage",
    }
    _require(set(primary) == common_fields | {"outcome_coverage"},
             "Split primary fields drift")
    _require(set(sensitivity) == common_fields | {
        "result_key_status", "heterogeneity_contrasts", "placebo_coverage",
        "temporal_window_metadata", "not_run",
    }, "Split sensitivity fields drift")
    _require(
        all(isinstance(part[key], list)
            for part in (primary, sensitivity)
            for key in ("results", "coverage")),
        "Split result or coverage section invalid",
    )
    _require(
        len(primary["results"]) == EXPECTED_COUNTS["primary_results"]
        and len(sensitivity["results"]) == EXPECTED_COUNTS["sensitivity_results"]
        and len(primary["coverage"]) == EXPECTED_COUNTS["primary_coverage"]
        and len(sensitivity["coverage"]) == EXPECTED_COUNTS["sensitivity_coverage"],
        "Split source cardinality drift",
    )
    _require(
        all(isinstance(row, dict) and row.get("variant") == "primary"
            for row in primary["results"])
        and all(isinstance(row, dict) and row.get("variant") != "primary"
                for row in sensitivity["results"]),
        "Split result source assignment drift",
    )
    for name, source in (("primary", PRIMARY_SHA256),
                         ("sensitivity", SENSITIVITY_SHA256)):
        part = parts[name]
        _require(part["source_sha256"] == source
                 and part["projection"] == {
                     "policy": POLICY, "source_sha256": source,
                 }, f"Split {name} source binding drift")
    for key in ("schema_version", "status", "metadata", "excluded_fields",
                "redactions", "limitation"):
        _require(primary[key] == sensitivity[key], "Split shared fields diverge")
    validate_public_projection({
        "schema_version": primary["schema_version"],
        "status": primary["status"],
        "metadata": primary["metadata"],
        "source_sha256": dict(SOURCE_SHA256),
        "projection": {"policy": POLICY, "source_sha256": dict(SOURCE_SHA256)},
        "excluded_fields": primary["excluded_fields"],
        "redactions": primary["redactions"],
        "limitation": primary["limitation"],
        "results": primary["results"] + sensitivity["results"],
        "coverage": primary["coverage"] + sensitivity["coverage"],
        "outcome_coverage": primary["outcome_coverage"],
        "result_key_status": sensitivity["result_key_status"],
        "heterogeneity_contrasts": sensitivity["heterogeneity_contrasts"],
        "placebo_coverage": sensitivity["placebo_coverage"],
        "temporal_window_metadata": sensitivity["temporal_window_metadata"],
        "not_run": sensitivity["not_run"],
    })


def _write_new(path: Path, payload: dict[str, Any]) -> None:
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    fd = os.open(path, flags, 0o600)
    with os.fdopen(fd, "w") as stream:
        json.dump(payload, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    project = commands.add_parser("project", help="Project exact frozen private aggregates")
    project.add_argument("--primary", required=True, type=Path)
    project.add_argument("--sensitivities", required=True, type=Path)
    project.add_argument("--output", required=True, type=Path)
    validate = commands.add_parser("validate", help="Validate a public projection")
    validate.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    if args.command == "project":
        payload = project_files(args.primary, args.sensitivities)
        _write_new(args.output, payload)
    else:
        validate_public_projection(json.loads(args.input.read_text()))
    print(json.dumps({"status": "PUBLIC_PROJECTION_VALIDATED",
                      "policy": POLICY, "expected_counts": EXPECTED_COUNTS}))


if __name__ == "__main__":
    main()
