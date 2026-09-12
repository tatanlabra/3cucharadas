# R1 round2: resolve manifest coverage without pretending a product change
Read-only, requested sonnet. No need to re-read the first entire packet. Return JSON task_id R1, source_digest 3b27cb4149399559e7fd942f4bdff03e263f26a50bc7e484bf528025f413a79b, provider, requested_model, effective_identity_evidence, findings with explicit dispositions of F1/F2/F3, open_p0_p1 boolean,verdict,limitations. No tools/mutations needed beyond Read of this supplied packet. Do not claim to run tests/hash data yourself.

F1: The fixture EXISTS in the unchanged baseline bf1ff5ac; previous manifest explicitly covered changed product files plus selected build outputs, not every file in baseline. Its omission was a review-packet coverage gap, not a missing runtime dependency. Added it and the unchanged image_dimensions.rb to this extended manifest. Source/build files have NOT changed. Below actual Git-blob/current SHA byte equality and real13-test run log include the executed fixture test. Determine if this resolves your unverifiedP1.
F3: verify_visual_assets.rb owns every catalog piece's variant_errors, dimensions/hash/budget validation and frontmatter/reference validation. Supplied full checker and real --strict greenlog below. Current teaser_mobile values are also exercised in the recorded archive browser check; do not claim a future pointer mutation is universally covered.
F2: Retain as P2 residual implementation risk if warranted. The precise JSON digest is pinned to the D2-reviewed output, so an added JSON row key would fail that guard; CSV/parquet/audit/provenance are not independently guarded within this publisher. Current exported five files were byte-compared to D2-reviewed outputs and a separate bounded privacy pass found aggregate territorial tables/no original identifiers (summary below). This is evidence for current export, not a universal future guarantee. The code field raw_records_exported=false is a declaration of this intended/reviewed export, not an independent privacy detector. The plan's D2/current-manifest checker additionally binds all reviewed files; future modified/unreviewed sources require renewed review, not an arbitrary newly-computed hash. We choose to leave this P2 documented for current scope, not silently claim the CLI alone enforces all privacy properties.

New UI80+8 browser cases are now complete but Q1 performance still running; those are separate Q1 acceptance. Original policy/scientific content unchanged. Current source source-before-build digest remains238221099b11ca45bc387d65fe90450397084927173ef75e808dfa36bc848b2a; extended R1 digest differs only by added baseline dependency coverage.

## Prior review
```json
{
  "task_id": "R1",
  "source_digest": "918f6c4edda5d6ed0bef4075dbd63816c9cce8bb6af4dd41812f40160998dded",
  "provider": "anthropic",
  "requested_model": "sonnet",
  "effective_identity_evidence": {
    "self_report": "claude-sonnet-5 (Sonnet 5), Anthropic — per this session's harness system-reminder",
    "runtime_evidence": "none independent of the harness string; no API/header introspection available in this sandbox",
    "note": "identical caveat as the D2 report consumed here; this round adds no independent attestation"
  },
  "findings": [
    {
      "id": "F1",
      "severity": "P1",
      "status": "open, unverified hypothesis",
      "claim": "tests/test_ai_disclosure.rb (test_real_webp_derivative_requires_digest_role_and_byte_budget) does `FileUtils.cp(File.expand_path('../assets/images/avaluos-ii/hero-brecha-residencial-tokyo-night-1600x900.webp', __dir__), target)`, but that exact path is absent from source-freeze.json's manifest, even though every other file under assets/images/avaluos-ii/ (all casen-shared-site-*, gap-top15-*, monetary-top15-* variants, 24 entries) is listed there.",
      "evidence": "source-freeze.json manifest keys under 'assets/images/avaluos-ii/' enumerate only casen-shared-site-*, gap-top15-*, monetary-top15-* files; 'hero-brecha-residencial-tokyo-night-1600x900.webp' does not appear in that block or anywhere else in the manifest.",
      "remedy": "Confirm the fixture's presence and hash at digest 918f6c4e... before trusting this suite as green (e.g. re-derive the manifest with this path included, or check the file directly against the frozen tree). If absent, FileUtils.cp raises before any assertion runs, so this specific test cannot currently pass, and the suite is not verifiably green against this candidate's frozen source."
    },
    {
      "id": "F2",
      "severity": "P2",
      "status": "open, design-gap hypothesis",
      "claim": "scripts/catastro_sii/project_casen_shared_site.py copies estimates.json/csv/parquet/audit.json/provenance.json verbatim into the public output directory and writes `'raw_records_exported': False` into its own receipt, but the only row-level checks it performs are scope counts, `unit == 'household'`, and null CI for commune rows — there is no allowlist check on row keys, so an upstream aggregate accidentally carrying an extra per-record field would be copied and published while the receipt still asserts no raw records were exported.",
      "evidence": "project_casen_shared_site.py:801-835 — `main()` validates `len(national)`, `len(regional)`, `r['unit']`, and commune `ci_low`/`ci_high`, then unconditionally `shutil.copyfile`s the five source files and writes `raw_records_exported: False` without inspecting `row.keys()`.",
      "remedy": "Add an explicit allowlist assertion on row schema (e.g. `set(row) <= {expected fields}`) before copy, so the 'no raw records' claim in the receipt is enforced rather than asserted."
    },
    {
      "id": "F3",
      "severity": "P3",
      "status": "open, scope-coverage gap",
      "claim": "scripts/verify_hero_disclosure.rb#source_errors only validates `header.overlay_image` and `header.overlay_image_mobile` against the visual catalog (dimensions, byte budget, sha256, AI-origin match); `header.teaser`, `header.teaser_mobile`, and `header.og_image` — all present in this post's front matter — are never checked by this script.",
      "evidence": "source_errors iterates a literal two-key hash (`'overlay_image'`, `'overlay_image_mobile'`); no analogous loop exists for teaser/og fields in the supplied file.",
      "remedy": "Either extend this checker's coverage or confirm (not asserted anywhere in this packet) that scripts/verify_visual_assets.rb, referenced only by hash in source-freeze.json and not included here, owns that gate — otherwise those three variants ship with no automated dimension/hash/disclosure check."
    }
  ],
  "open_p0_p1": true,
  "verdict": "Editorial/scientific content passes adversarial spot-checks: the p_v algebra, the g(A) tax formula (cross-checked numerically against the Iquique and Lo Barnechea worked examples), the CASEN regional sample sizes (sum exactly to the reported national n=78,654), the residuo/escenario-aceptable ordering in both tables, and the causality/representativeness/geographic-evidence guardrails from the brief are all respected in both the ES and EN posts, which read as faithful translations of each other. Acceptance is nonetheless blocked: F1 is an open, unverified P1 (a test fixture the suite depends on is not visible in this round's own frozen manifest, so the 'tests pass' claim for that file cannot be taken as reproducible from what was supplied). F2 is a real but unconfirmed P2 residual-risk gap in the CASEN publish path. Per the brief, I am not certifying the pending Q1 checks (80-case AI-UI browser matrix, 5 paired performance runs) — those remain explicitly outside this packet's approval boundary regardless of F1/F2.",
  "limitations": [
    "No command execution was available in this sandbox (Bash calls required approval that did not resolve), so no sha256/test re-run was actually performed; all findings above are derived from static reading and cross-arithmetic, not from executing the referenced scripts or hashing the referenced assets myself.",
    "D1/D2 (source_digest 14eaab8598...) was consumed as accepted per the brief and not re-verified; rdata.py/core.py referenced in the D2 findings are not present in this round's source-freeze.json manifest, consistent with D1 being out of this round's diff scope.",
    "Axe/keyboard/performance evidence in editorial-browser/receipt.json is reported, not independently reproduced by me; I read it for internal consistency only (case/check counts reconcile: 8 cases x 46 = 368; 8+8=16 axe audits).",
    "image_dimensions.rb (required by verify_hero_disclosure.rb) was not supplied in this packet, so its correctness could not be reviewed.",
    "P2 residual limitation staying visible per the brief: F2 (unenforced raw-export guarantee) remains an open, unconfirmed risk even if F1 resolves cleanly."
  ]
}
```

## Baseline fixture and helper proof
```json
[
  {
    "file": "assets/images/avaluos-ii/hero-brecha-residencial-tokyo-night-1600x900.webp",
    "current_sha256": "31f508f8317beb602ed04e5c3fcd974569d308d712ec5f7f707d447196ca0808",
    "baseline_sha256": "31f508f8317beb602ed04e5c3fcd974569d308d712ec5f7f707d447196ca0808",
    "unchanged_from_baseline": true,
    "bytes": 156080
  },
  {
    "file": "scripts/lib/image_dimensions.rb",
    "current_sha256": "c94fb013aaa3f691eb791b3a5112a0583b220f1d3b7a59af353f2034f887c584",
    "baseline_sha256": "c94fb013aaa3f691eb791b3a5112a0583b220f1d3b7a59af353f2034f887c584",
    "unchanged_from_baseline": true,
    "bytes": 2577
  }
]
```

## Executed checks/logs
```json
[
  {
    "id": "U1-first-person-green",
    "task_id": "U1",
    "command": [
      "ruby",
      "tests/test_ai_disclosure.rb"
    ],
    "cwd": "/home/ende/Descargas/programaciones/activos/3cucharadas",
    "started_at": "2026-09-12T11:55:15.864922+00:00",
    "seconds": 0.6530756020001718,
    "exit_code": 0,
    "log": "evidence/checks/U1-first-person-green.log",
    "log_sha256": "2fa98cefe131d2f4ab7ee0904c6d474dbd267530259fce225745d6d0e3fdcec5"
  },
  {
    "reported_log": "Run options: --seed 21376\n\n# Running:\n\n............/home/ende/.local/share/gem/ruby/3.4.0/gems/liquid-4.0.4/lib/liquid/tags/case.rb:51: warning: literal string will be frozen in the future (run with --debug-frozen-string-literal for more information)\n/home/ende/.local/share/gem/ruby/3.4.0/gems/liquid-4.0.4/lib/liquid/tags/case.rb:51: warning: literal string will be frozen in the future (run with --debug-frozen-string-literal for more information)\n/home/ende/.local/share/gem/ruby/3.4.0/gems/liquid-4.0.4/lib/liquid/tags/case.rb:51: warning: literal string will be frozen in the future (run with --debug-frozen-string-literal for more information)\n/home/ende/.local/share/gem/ruby/3.4.0/gems/liquid-4.0.4/lib/liquid/tags/case.rb:51: warning: literal string will be frozen in the future (run with --debug-frozen-string-literal for more information)\n/home/ende/.local/share/gem/ruby/3.4.0/gems/liquid-4.0.4/lib/liquid/tags/case.rb:51: warning: literal string will be frozen in the future (run with --debug-frozen-string-literal for more information)\n/home/ende/.local/share/gem/ruby/3.4.0/gems/liquid-4.0.4/lib/liquid/tags/case.rb:51: warning: literal string will be frozen in the future (run with --debug-frozen-string-literal for more information)\n.\n\nFinished in 0.427439s, 30.4137 runs/s, 339.2300 assertions/s.\n\n13 runs, 145 assertions, 0 failures, 0 errors, 0 skips\n"
  },
  {
    "id": "H1-first-person-strict",
    "task_id": "H1",
    "command": [
      "ruby",
      "scripts/verify_visual_assets.rb",
      "--strict"
    ],
    "cwd": "/home/ende/Descargas/programaciones/activos/3cucharadas",
    "started_at": "2026-09-12T11:56:50.390765+00:00",
    "seconds": 0.5010663270004443,
    "exit_code": 0,
    "log": "evidence/checks/H1-first-person-strict.log",
    "log_sha256": "95d5248e4ecafcb431301b8e6c7c88a61b1ab711488c2c22ff3265c4e5878de5"
  },
  {
    "reported_log": "Gate de activos visuales OK: 12 manifest(s), 162 activo(s) referenciados desde 20 posts, 0 aviso(s).\n"
  }
]
```

## Current public projection equality
```json
{
  "estimates.json": {
    "reviewed_source_sha256": "b192b57607badd8fac36f42f4e5bc3132b4239ecb05ed7a0904998f91121a9ce",
    "public_sha256": "b192b57607badd8fac36f42f4e5bc3132b4239ecb05ed7a0904998f91121a9ce"
  },
  "estimates.csv": {
    "reviewed_source_sha256": "c6c7e9ca08f0b12325ed3f8144df00dd27e6906b7e1ecad4f3ba7b8b8b41e1e3",
    "public_sha256": "c6c7e9ca08f0b12325ed3f8144df00dd27e6906b7e1ecad4f3ba7b8b8b41e1e3"
  },
  "estimates.parquet": {
    "reviewed_source_sha256": "5802ad1a03c929ad68b617849c842e65c119add571be5c7e82da8cc549479b02",
    "public_sha256": "5802ad1a03c929ad68b617849c842e65c119add571be5c7e82da8cc549479b02"
  },
  "audit.json": {
    "reviewed_source_sha256": "89c0516199a7bda371cdfd42572917ff92b5551084fb69ee86093a2baafbfd31",
    "public_sha256": "89c0516199a7bda371cdfd42572917ff92b5551084fb69ee86093a2baafbfd31"
  },
  "provenance.json": {
    "reviewed_source_sha256": "12286c253b021a9b9a83381e8d5ad1cb46964f312e396f7474582501b61c2df0",
    "public_sha256": "12286c253b021a9b9a83381e8d5ad1cb46964f312e396f7474582501b61c2df0"
  }
}
```

## Bounded privacy review
```json
{
  "task_id": "closure-privacy-package-review",
  "recorded_at": "2026-09-12T12:14:17.136355+00:00",
  "status": "bounded_review_complete_package_streams_sanitized",
  "scope": {
    "3cucharadas": [
      "docs/plans/20260912-heroes-casen",
      "catastro_sii_brecha/data/casen-shared-site"
    ],
    "catastros_sii": [
      "v5_brecha/artifacts/casen_shared_site"
    ]
  },
  "selection": "Only Git-added or untracked files under requested scopes at this snapshot; existing modified files and private archive excluded.",
  "snapshot": {
    "new_files": 686,
    "total_bytes": 112364830,
    "text_bytes_scanned": 12369795,
    "files_changed_during_own_read": []
  },
  "observations": {
    "credential_pattern_candidates": [],
    "json_original_identifier_record_candidates": [],
    "remaining_raw_initialization_stream_candidates": [],
    "aggregate_tables": {
      "files_inspected": 6,
      "rows_per_file": 363,
      "scope_values": [
        "national",
        "region",
        "commune"
      ],
      "unique_territorial_keys": true,
      "original_identifier_columns": [],
      "locations": [
        "blog public CASEN projection",
        "analytical current aggregates",
        "analytical preserved historical aggregates"
      ]
    },
    "documents": {
      "official_CASEN_PDFs_text_inspected": 2,
      "original_RData_DTA_read": false,
      "questionnaire_field_names_are_not_filled_respondent_records": true
    },
    "images": {
      "metadata_headers_inspected": 165,
      "GPS_EXIF_observed": false,
      "plot_description_metadata_inspected": 8,
      "credential_or_home_path_patterns_in_plot_descriptions": false,
      "pixels_or_OCR_exhaustively_inspected": false
    },
    "browser_jsonl": {
      "files_inspected": 4,
      "classification": "Browser command receipts, not model-session transcripts"
    },
    "claude_identity_metadata": {
      "path": "docs/plans/20260912-heroes-casen/evidence/claude-science/round1/runtime-identity.json",
      "record_count": 2,
      "allowed_record_keys": [
        "line",
        "type",
        "model",
        "timestamp"
      ],
      "raw_message_content_present": false
    },
    "fixtures": "Synthetic RData values and fixture code are explicitly labelled; column names in audited class metadata are distinct from original observation values.",
    "operational_local_paths": {
      "files": [
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/G1/agy-20260912T104837Z-241965/status.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/G1/receipt.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/U1/3c-u1-ai-green.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/U1/3c-u1-build.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/U1/3c-u1-red.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/V0-portability/old-svg-red.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/V0-portability/prior-acceptance-receipt.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/V0/missing-residual.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/V0/nested-invalid.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/baseline.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/D1-root-r-boundary-tests.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/D1-root-tests.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/D2-binding-final.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/D2-current-review-binding.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-bound-build.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-bound-build.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-candidate-build.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-candidate-build.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-casen-projection-green.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-first-person-build.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-first-person-build.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-first-person-hero.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-first-person-offline-dev.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-hero-integrated.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-hero-timezone-green.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-offline-dev.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-visual-assets.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-wrong-casen-digest-red.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/E1-wrong-casen-digest-red.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/H1-cardfix-current-assets.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/H1-final-strict-green.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/H1-final-strict.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/H1-first-person-strict.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/H1-visual-assets-integrated.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/H1-visual-assets-recovery.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/H1-visual-assets.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/P0-source-inventory.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/Q1-catastro-types.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/Q1-distribution.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/Q1-first-person-artifact.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/Q1-first-person-distribution.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/Q1-fiscal-invariants.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/Q1-fiscal-invariants.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/Q1-runtime-gate-assurance.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/Q1-site-artifact.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-first-person-green.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-first-person-green.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-first-person-red.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-first-person-red.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-root-ai-tests.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-root-ai-tests.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-root-dev-tests.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-timezone-fixture-red.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-timezone-fixture-red.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-timezone-green.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-timezone-green.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-timezone-red.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/U1-timezone-red.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/V0-portable-root-tests.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/V0-tests-root.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/checks/V1-root-tests.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/claude-final/bridge-argument-limit-failed.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/claude-science/round1/D1-prior-acceptance.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/claude-science/round1/bridge-retry.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/claude-science/round1/bridge.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/claude-science/round2/binding-negative-recovery.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/claude-science/round2/bridge.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/editorial-browser/run-fiscal-tables-qa.py",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/editorial-browser/run-qa.py",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/editorial/baseline-inputs-current.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/hero-browser/cardfix-build.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/hero-browser/matrix-build.log",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/images/selected-sources.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/performance/doctor-after-init-command.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/performance/formal-candidate-freeze.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/performance/formal-tools/run_performance.py",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/performance/pilot-valid/harness-used.py",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/performance/run_performance.py",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/receipts/D1.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/receipts/D2.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/receipts/E1.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/receipts/H1.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/receipts/P0.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/receipts/U1.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/receipts/V0.json",
        "3cucharadas/docs/plans/20260912-heroes-casen/evidence/receipts/V1.json"
      ],
      "classification": "Local execution paths in planning receipts/logs; no recognized credentials; not a certification that all planning evidence is suitable for external publication."
    },
    "small_aggregate_cells": {
      "area_cells_with_positive_n_below_5": 2,
      "minimum_positive_n": 3,
      "classification": "Aggregates without original IDs; no formal statistical disclosure-control certification."
    }
  },
  "resolved_finding": {
    "id": "PR-01",
    "type": "unsanitized_Qwen_session_stream_in_versionable_package",
    "before": "27 complete objects including local initialization and conversation records; original stdout truncated at 65536 bytes.",
    "action": "Two original streams archived byte-identically outside versionable package; package copies removed; explicit public allowlist replacement written.",
    "originals": [
      {
        "original_package_path": "docs/plans/20260912-heroes-casen/evidence/G1/qwen-20260912T105710Z-263862/stdout.json",
        "sha256": "3d3c49ee0ab5614430a156b510696f90f35503786d14af499220aee7a317c367",
        "bytes": 65536,
        "private_copy_matches": true,
        "package_copy_absent": true
      },
      {
        "original_package_path": "docs/plans/20260912-heroes-casen/evidence/G1/qwen-20260912T105710Z-263862/complete-prefix-objects.json",
        "sha256": "b21c18f53c37fcba737311a1e2b1b96d48c105c965920e1d8592082b9f005585",
        "bytes": 66854,
        "private_copy_matches": true,
        "package_copy_absent": true
      }
    ],
    "replacement": "docs/plans/20260912-heroes-casen/evidence/G1/qwen-20260912T105710Z-263862/sanitized-review-evidence.json",
    "replacement_sha256": "b589c0ea516310eb91dbc92d1ade19e5eb667259521b9a408a3398ff02b170d4",
    "reference_updates": [
      {
        "path": "evidence/G1/receipt.json",
        "references": [
          "excluded original hashes with explicit exclusion",
          "replacement file with current SHA-256"
        ]
      },
      {
        "path": "evidence/G1/qwen-20260912T105710Z-263862/recovery.json",
        "references": [
          "original hashes retained as historical evidence",
          "sanitized replacement and SHA-256"
        ]
      },
      {
        "path": "evidence/G1/qwen-20260912T105710Z-263862/result.md",
        "references": [
          "replacement/recovery/stderr instead of unavailable raw stdout"
        ]
      },
      {
        "path": "evidence/G1/qwen-launch-escalated.log",
        "references": [
          "replacement/recovery/stderr instead of unavailable raw stdout"
        ]
      },
      {
        "path": "evidence/G1/disposition.md",
        "references": [
          "reason for exclusion and unchanged partial status"
        ]
      }
    ],
    "receipt_hash_bindings_valid": true,
    "G1_status": "partial_optional",
    "approved_external_review": false,
    "Gemini_rejection_unchanged": true
  },
  "limits": [
    "Pattern scans do not prove absence of every possible credential encoding or indirect identifying information.",
    "No original CASEN microdata read and no statistical/scientific re-estimation performed.",
    "No exhaustive image-pixel/OCR review; image metadata and bounded documentary/structured surfaces inspected.",
    "Snapshot only: concurrent or later new/modified files need renewed checking before relying on this result.",
    "Existing modified files outside the new-file selection, other repositories/scopes, Git history and external publication state not audited."
  ],
  "writes": [
    "G1 authorized receipt/disposition/log and selected Qwen run subtree",
    "this privacy-review.json",
    "private nonversionable archive of preserved originals"
  ],
  "D1_freeze_modified": false,
  "no_commits": true,
  "no_publication": true
}
```

## scripts/verify_visual_assets.rb
```ruby
#!/usr/bin/env ruby
# frozen_string_literal: true

# Gate de activos visuales. Corre sobre el ÁRBOL FUENTE (_posts/, assets/,
# _config.yml), no sobre el artefacto construido, así que puede ejecutarse antes
# de `jekyll build` y también como pre-commit local.
#
# Cubre dos cosas que ningún otro verificador del repo mira:
#
#   1. Que todo <img src> de un post resuelva a un archivo real (V9). Hoy una
#      imagen excluida del build pero referenciada desde un post sale rota a
#      producción y el CI pasa en verde.
#   2. Que los manifests _data/visuales/<slug>.yml se cumplan: dimensiones
#      declaradas == reales, cifras citadas presentes en el post, y coherencia
#      entre el estado de cada pieza y el `exclude` de _config.yml.
#
# V9 no depende de que exista manifest: funciona para todos los posts desde ya.
#
# Uso:
#   ruby scripts/verify_visual_assets.rb            # warnings no fallan
#   ruby scripts/verify_visual_assets.rb --strict   # warnings fallan

require "date"
require "yaml"
require_relative "lib/image_dimensions"
require_relative "verify_hero_disclosure"

ROOT = File.expand_path("..", __dir__)
STRICT = ARGV.include?("--strict")
MIN_OG_IMAGE_WIDTH = 1200
ROLES_CON_ALT = %w[hero figura og].freeze

errors = []
warnings = []

def rel(path)
  path.delete_prefix("#{ROOT}/")
end

# --- Carga del exclude de _config.yml -------------------------------------

config = YAML.safe_load_file(File.join(ROOT, "_config.yml"), permitted_classes: [Date, Time], aliases: true)
excludes = Array(config["exclude"]).map { |e| e.to_s.chomp("/") }

# Una ruta está excluida si coincide exactamente o cuelga de un prefijo excluido.
def excluded?(path, excludes)
  excludes.any? { |e| path == e || path.start_with?("#{e}/") }
end

# Quita separadores de miles y decimales para comparar cifras entre idiomas:
# "10.343.893" (ES) y "10,343,893" (EN) colapsan al mismo "10343893".
def normaliza_cifra(str)
  str.gsub(/[., \s]/, "")
end

# No reutiliza posts.py::_numbers() del paquete de difusión a propósito: aquel
# compara contra title+description (metadatos públicos) y su regex parte
# "10.343.893" en fragmentos. Acá el corpus es el cuerpo completo del post.
def cifra_presente?(cifra, cuerpo)
  return true if cuerpo.include?(cifra)

  objetivo = normaliza_cifra(cifra)
  return false if objetivo.empty?

  # Compara token completo, no subcadena: evita que "94" case dentro de "1945".
  cuerpo.scan(/\d[\d.,]*%?/).any? { |token| normaliza_cifra(token) == objetivo }
end

# --- Índice de referencias desde los posts --------------------------------

post_paths = Dir.glob(File.join(ROOT, "_posts", "*.md")).sort
abort "No se encontraron posts en _posts/" if post_paths.empty?

# ruta_de_asset => [[post_relativo, alt], ...]
referencias = Hash.new { |h, k| h[k] = [] }
post_bodies = {}

post_paths.each do |path|
  body = File.read(path)
  post_bodies[rel(path)] = body

  # <img src="..."> y srcset, con o sin filtro Liquid alrededor.
  tags = body.scan(/<img\s[^>]*>/i)
  tags.each do |tag|
    alt = tag[/\balt\s*=\s*"([^"]*)"/i, 1]
    srcs = tag.scan(/\b(?:src|srcset)\s*=\s*"([^"]*)"/i).flatten
    srcs.each do |raw|
      # Desenvuelve {{ '/ruta' | relative_url }} y limpia descriptores de srcset.
      raw.scan(%r{/assets/[^"'\s,|\}]+}).each do |asset|
        referencias[asset.delete_prefix("/")] << [rel(path), alt]
      end
    end
  end

  # Front matter: teaser y og_image.
  next unless body.start_with?("---")

  fm_raw = body.split(/^---\s*$/, 3)[1]
  next if fm_raw.nil?

  begin
    fm = YAML.safe_load(fm_raw, permitted_classes: [Date, Time], aliases: true)
  rescue StandardError
    next
  end
  header = fm.is_a?(Hash) ? fm["header"] : nil
  next unless header.is_a?(Hash)

  %w[teaser og_image overlay_image overlay_image_mobile image].each do |key|
    value = header[key]
    next unless value.is_a?(String) && value.start_with?("/assets/")

    referencias[value.delete_prefix("/")] << [rel(path), nil]
  end
end

# --- V9: toda referencia resuelve a un archivo real ------------------------

referencias.each do |asset, usos|
  next if File.file?(File.join(ROOT, asset))

  usos.map(&:first).uniq.each do |post|
    errors << "V9 #{post}: referencia a #{asset}, que no existe en el repo"
  end
end

# --- Manifests -------------------------------------------------------------

manifest_paths = Dir.glob(File.join(ROOT, "_data", "visuales", "*.yml")).sort
declared_assets = []
slugs_con_manifest = manifest_paths.map { |p| File.basename(p, ".yml") }

manifest_paths.each do |manifest_path|
  manifest_rel = rel(manifest_path)
  manifest = YAML.safe_load_file(manifest_path, permitted_classes: [Date, Time], aliases: true)

  unless manifest.is_a?(Hash) && manifest["piezas"].is_a?(Array)
    errors << "#{manifest_rel}: no tiene una lista `piezas`"
    next
  end

  # Cuerpo de los posts declarados, para contrastar cifras.
  cuerpos = Array(manifest["posts"]).filter_map { |p| post_bodies[p] }
  if cuerpos.empty? && manifest["posts"]
    errors << "#{manifest_rel}: ningún post de `posts` existe en _posts/"
  end
  cuerpo_unido = cuerpos.join("\n")

  manifest["piezas"].each do |pieza|
    id = pieza["id"] || "(sin id)"
    etiqueta = "#{manifest_rel}[#{id}]"
    estado = pieza["estado"]
    archivo = pieza["archivo"]

    unless %w[publicable solo-difusion bloqueado].include?(estado)
      errors << "#{etiqueta}: estado inválido #{estado.inspect}"
      next
    end

    if archivo.nil?
      # Solo una pieza bloqueada puede no tener archivo: se eliminó del repo y
      # la entrada se conserva por el catálogo de errores.
      errors << "#{etiqueta}: sin `archivo` y no está bloqueada" unless estado == "bloqueado"
      next
    end

    declared_assets << archivo
    errors.concat(HeroDisclosureCheck.variant_errors(pieza, ROOT))
    ruta = File.join(ROOT, archivo)
    existe = File.file?(ruta)

    # V1: el archivo declarado existe (salvo pieza bloqueada ya eliminada).
    if !existe
      if estado == "bloqueado"
        next
      end
      errors << "V1 #{etiqueta}: #{archivo} no existe"
      next
    end

    # V2 y V3: dimensiones declaradas vs reales vs nombre.
    declarado_w = pieza["ancho"]
    declarado_h = pieza["alto"]
    reales = image_dimensions(ruta)

    if reales.nil?
      # SVG y formatos sin encabezado binario: no verificable, no es error.
      if declarado_w || declarado_h
        warnings << "V2 #{etiqueta}: declara dimensiones pero #{File.extname(archivo)} no es verificable; se ignoran"
      end
    elsif declarado_w.nil? || declarado_h.nil?
      warnings << "V2 #{etiqueta}: sin ancho/alto declarados (reales #{reales[0]}x#{reales[1]})"
    elsif [declarado_w, declarado_h] != reales
      errors << "V2 #{etiqueta}: declara #{declarado_w}x#{declarado_h} pero #{archivo} mide #{reales[0]}x#{reales[1]}"
    end

    # Anclado antes de la extensión: un nombre como
    # bivariado-clasificacion-4x2-1200x1685.webp lleva "4x2" en el nombre y las
    # dimensiones al final. Sin anclar, el "4x2" gana.
    if (m = File.basename(archivo).match(/(\d+)x(\d+)\.\w+\z/)) && declarado_w && declarado_h
      nombre = [m[1].to_i, m[2].to_i]
      if nombre != [declarado_w, declarado_h]
        errors << "V3 #{etiqueta}: el nombre dice #{nombre[0]}x#{nombre[1]} pero declara #{declarado_w}x#{declarado_h}"
      end
    end

    # V4: convención de nombres. Solo aviso, y solo para activos editoriales
    # colocados a mano: los generados desde los datos siguen el naming de su
    # pipeline (sankey-pipeline.webp, violin-denominadores.webp) y renombrarlos
    # en masa rompería los posts sin ganar nada.
    nombre_legacy = pieza["nombre_legacy"] == true
    if nombre_legacy && pieza["motivo_nombre"].to_s.strip.empty?
      errors << "V4 #{etiqueta}: `nombre_legacy` exige `motivo_nombre`"
    elsif pieza["origen"] != "datos" && File.extname(archivo) != ".svg" &&
          !File.basename(archivo).match?(/\d+x\d+\.\w+\z/) && !nombre_legacy
      warnings << "V4 #{etiqueta}: #{File.basename(archivo)} no sigue la convención <nombre>-<ancho>x<alto>.<ext>"
    end

    usos = referencias[archivo] || []

    # V5: las cifras declaradas aparecen en el cuerpo del post.
    Array(pieza["cifras"]).each do |cifra|
      next if cuerpo_unido.empty?
      next if cifra_presente?(cifra, cuerpo_unido)

      errors << "V5 #{etiqueta}: la cifra #{cifra.inspect} no aparece en el cuerpo del post"
    end

    case estado
    when "publicable"
      # V7: una pieza publicable no puede estar excluida del build.
      if excluded?(archivo, excludes)
        errors << "V7 #{etiqueta}: es publicable pero #{archivo} está en el `exclude` de _config.yml"
      end

      # V11: og real >= 1200px de ancho.
      if pieza["rol"] == "og" && reales && reales[0] < MIN_OG_IMAGE_WIDTH
        errors << "V11 #{etiqueta}: og de #{reales[0]}px, mínimo #{MIN_OG_IMAGE_WIDTH}px"
      end

      # V12: alt no vacío en los roles que lo exigen.
      # Los .svg suelen ser el acompañante vectorial de un .webp que ya lleva el
      # alt en su <img>; exigirles alt propio duplicaría el texto.
      if ROLES_CON_ALT.include?(pieza["rol"]) && File.extname(archivo) != ".svg"
        alt = pieza["alt"]
        vacio = !alt.is_a?(Hash) || alt.values.all? { |v| v.to_s.strip.empty? }
        warnings << "V12 #{etiqueta}: rol #{pieza["rol"]} sin `alt`" if vacio
      end

      # V12b: el alt real del <img> en el post tampoco puede estar vacío.
      usos.each do |post, alt_real|
        next if alt_real.nil? # front matter, no lleva alt
        next unless alt_real.strip.empty?

        errors << "V12 #{post}: <img> de #{archivo} sin alt"
      end

    when "solo-difusion", "bloqueado"
      # V6: no puede estar referenciada desde ningún post.
      usos.map(&:first).uniq.each do |post|
        errors << "V6 #{etiqueta}: es #{estado} pero #{post} la referencia"
      end

      # V8: debe estar cubierta por el `exclude` de _config.yml.
      if existe && !excluded?(archivo, excludes)
        errors << "V8 #{etiqueta}: es #{estado} pero #{archivo} no está en el `exclude` de _config.yml"
      end
    end
  end

  # V10: teaser y og_image del front matter apuntan a piezas publicables.
  publicables = manifest["piezas"]
                .select { |p| p["estado"] == "publicable" && p["archivo"] }
                .map { |p| p["archivo"] }

  Array(manifest["posts"]).each do |post_rel|
    body = post_bodies[post_rel]
    next unless body&.start_with?("---")

    fm_raw = body.split(/^---\s*$/, 3)[1]
    next if fm_raw.nil?

    fm = begin
      YAML.safe_load(fm_raw, permitted_classes: [Date, Time], aliases: true)
    rescue StandardError
      nil
    end
    header = fm.is_a?(Hash) ? fm["header"] : nil
    next unless header.is_a?(Hash)

    %w[teaser og_image overlay_image overlay_image_mobile].each do |key|
      value = header[key]
      next unless value.is_a?(String) && value.start_with?("/assets/")

      asset = value.delete_prefix("/")
      next if publicables.include?(asset)

      errors << "V10 #{post_rel}: header.#{key} apunta a #{asset}, que no es una pieza publicable de #{manifest_rel}"
    end
  end
end

# --- V13: posts con carpeta de activos propia deberían tener manifest ------

Dir.glob(File.join(ROOT, "assets", "images", "*")).each do |dir|
  next unless File.directory?(dir)

  slug = File.basename(dir)
  # Carpetas de infraestructura del sitio, no activos de un post.
  next if %w[teasers home favicons 404].include?(slug)
  next if slugs_con_manifest.include?(slug)
  # A shared directory can be covered by multiple topic catalogs, without a
  # duplicate directory-level catalog becoming a second source of truth.
  files = Dir.glob(File.join(dir, "**", "*")).select { |f| File.file?(f) }.map { |f| rel(f) }
  next if !files.empty? && (files - declared_assets).empty?

  warnings << "V13 assets/images/#{slug}/ no tiene manifest en _data/visuales/"
end

# --- Salida ----------------------------------------------------------------

warnings.uniq.each { |w| warn "- aviso: #{w}" }
errors.uniq.each { |e| warn "- #{e}" }

if !errors.empty?
  abort "Gate de activos visuales falló (#{errors.uniq.length} problema(s))"
elsif STRICT && !warnings.empty?
  abort "Gate de activos visuales falló en modo --strict (#{warnings.uniq.length} aviso(s))"
end

referenciados = referencias.keys.length
puts "Gate de activos visuales OK: #{manifest_paths.length} manifest(s), " \
     "#{referenciados} activo(s) referenciados desde #{post_paths.length} posts, " \
     "#{warnings.uniq.length} aviso(s)."

```

## scripts/lib/image_dimensions.rb
```ruby
# frozen_string_literal: true

# Lectura de dimensiones de imagen sin dependencias: parsea encabezados
# WebP (VP8/VP8L/VP8X), PNG y JPEG con solo stdlib de Ruby.
#
# Extraído de verify_distribution_readiness.rb, que solo necesitaba el ancho.
# verify_visual_assets.rb necesita también el alto para contrastar las
# dimensiones declaradas en _data/visuales/<slug>.yml contra el archivo real.
#
# No cubre SVG a propósito: no tiene encabezado binario y sus dimensiones
# dependen de width/height o viewBox, que pueden estar en unidades relativas.
# Quien lo llame debe tratar el nil de un .svg como "no verificable", no como error.

# Devuelve [ancho, alto] o nil si el formato no se reconoce o el archivo no existe.
def image_dimensions(path)
  return nil unless File.file?(path)

  bytes = File.open(path, "rb") { |f| f.read(64) }
  return nil unless bytes

  if bytes[0, 4] == "RIFF" && bytes[8, 4] == "WEBP"
    webp_dimensions(bytes)
  elsif bytes[0, 8] == "\x89PNG\r\n\x1a\n".b
    [bytes[16, 4].unpack1("N"), bytes[20, 4].unpack1("N")]
  elsif bytes[0, 2] == "\xFF\xD8".b
    jpeg_dimensions(path)
  end
rescue StandardError
  nil
end

# Compatibilidad con el uso original en verify_distribution_readiness.rb.
def image_width(path)
  image_dimensions(path)&.first
end

def webp_dimensions(bytes)
  case bytes[12, 4]
  when "VP8 "
    # Lossy: ancho y alto son little-endian 14-bit en los bytes 26-29.
    w = bytes[26, 2].unpack1("v") & 0x3FFF
    h = bytes[28, 2].unpack1("v") & 0x3FFF
    (w.positive? && h.positive?) ? [w, h] : nil
  when "VP8L"
    # Lossless: 14 bits de ancho y 14 de alto, menos uno, empaquetados en 32 bits.
    b = bytes[21, 4].unpack1("V")
    [(b & 0x3FFF) + 1, ((b >> 14) & 0x3FFF) + 1]
  when "VP8X"
    # Extendido: canvas menos uno, 24-bit little-endian (ancho en 24-26, alto en 27-29).
    [le24(bytes[24, 3]) + 1, le24(bytes[27, 3]) + 1]
  end
end

def le24(chunk)
  chunk.bytes.reverse.inject(0) { |acc, b| (acc << 8) | b }
end

def jpeg_dimensions(path)
  File.open(path, "rb") do |f|
    f.read(2)
    loop do
      marker = f.read(2)
      break unless marker && marker[0] == "\xFF".b

      code = marker[1].unpack1("C")
      break if code == 0xD9

      length = f.read(2)&.unpack1("n")
      break unless length

      # SOFn lleva las dimensiones, salvo DHT (C4), JPG (C8) y DAC (CC).
      if (0xC0..0xCF).cover?(code) && ![0xC4, 0xC8, 0xCC].include?(code)
        f.read(1)
        height, width = f.read(4).unpack("nn")
        return [width, height]
      else
        f.read(length - 2)
      end
    end
  end
  nil
end

```
