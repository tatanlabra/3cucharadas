# Contract evidence assurance — observed red and green

The original verifier accepted 27 forbidden fixtures. Its complete 49-case suite exited 1: six valid fixtures accepted, 16 invalid fixtures already rejected, and 27 invalid fixtures incorrectly accepted. The integrator patched `verify_execution.py`; the same final suite now exits 0 with all 49 expectations met (six accepts, 43 rejects). No actual receipt, source manifest, contract, D1 artifact or product output was perturbed by these tests.

| Defect observed in original CLI | Required correction, applied by integrator | Current observation |
|---|---|---|
| Missing or foreign check task binding; absent, empty, unknown, string-valued or incomplete acceptance coverage; no declared acceptance | Require matching `checks[].task_id`, a nonempty list `acceptance_ids`, no unknown IDs, and exact union of covered contractual IDs; require nonempty unique contractual criteria | Invalid cases rejected; one check covering several criteria and repeated valid coverage both accepted |
| Verified task with missing/pending dependency; dependency cycle | Validate dependency graph existence and acyclicity; verified tasks require verified dependencies except an explicitly optional task | Missing, pending mandatory and cyclic dependencies rejected; verified and explicitly optional pending dependencies accepted |
| Empty task list or duplicate task IDs | Require nonempty task collection, unique IDs and TODO/task agreement | Invalid collections rejected |
| Stale manual digest, changed reviewed source, missing or empty manifest | Require a nonempty manifest, recompute canonical digest and compare against both frozen and receipt digests; rehash each source file | All stale/absent/empty/changed source cases rejected |
| Changing receipt `kind` to bypass the review checks | Derive need for manual review from contractual acceptance, then require manual receipt kind and provenance | Bypass rejected; current valid manual fixture accepted |
| Absolute paths, lexical traversal or symlinks escaping artifact/log/source roots | Resolve relative paths through a containment check; disallow absolute paths and `..`; enforce containment after symlink resolution | All path escape fixtures rejected |
| JSON boolean `false` accepted as exit code zero | Require exact integer type and value zero | Boolean false rejected |

Existing rejection controls were retained for failed/missing checks, missing command, empty/missing artifact collections, altered/missing logs or artifacts, wrong top-level receipt task, missing receipt, inconsistent TODO, open critical findings and missing review identity.

## Frozen interface

- `checks[].acceptance_ids` is a nonempty string list. Its union must equal the task's contractual acceptance IDs. Overlap between checks is allowed; pertinence remains a review obligation.
- Review receipts have `source_manifest` and `source_root`, both relative to the workspace.
- The manifest JSON contains `manifest: {path_relative_to_source_root: sha256}` and `source_digest`.
- The digest is SHA-256 of UTF-8 `json.dumps(manifest, sort_keys=True, separators=(',', ':'))`. Each referenced source hash must still match.
- `open_p0_p1` must explicitly be Boolean false; absence is not evidence of closed findings.
- Fixture commands and review identity statements are synthetic. These tests never represent an actual model review or execution of the fixture's declared check command.

## Reproduction

```sh
python -m unittest discover -s docs/plans/20260912-heroes-casen \
  -p test_execution_evidence.py -v
EXECUTION_VERIFIER_SOURCE=docs/plans/20260912-heroes-casen/evidence/contract-assurance/verify_execution.before.py \
  python docs/plans/20260912-heroes-casen/test_execution_evidence.py
```

The second command is expected to fail: it replays the known original defects. The test module copies one pinned verifier version into a temporary workspace-shaped tree and exercises its real CLI. `observations-before.json` and `observations-after.json` record every return code and sanitized stdout/stderr; each includes verifier and test-suite hashes. Log paths in test tracebacks were normalized to `<plan>` or `<isolated-fixture>`; no substantive diagnostic was removed.

## Limits and disposition

All 27 reproduced receipt-integrity/binding defects are addressed by the frozen patched verifier. This is not a guarantee of global correctness. Receipt hashes and acceptance IDs do not establish that a check is substantively relevant, that a claimed command really ran, that model identity evidence is authentic, or that scientific, visual, accessibility and performance criteria are satisfied. Those still require their actual evidence and designated review. The suite does not certify live publication or empirical optimality.

Existing real receipts need explicit, evidence-backed coverage migration by the integrator; this suite does not silently add IDs to them. An incomplete acceptance or changed source keeps the affected task pending regardless of the verifier's fixture pass.

Ownership: assurance worker wrote only `test_execution_evidence.py` and `evidence/contract-assurance/**`. The integrator alone patched `verify_execution.py` and migrates contract/real receipts. D1 remained frozen. No commits or publication were performed by the assurance worker.
