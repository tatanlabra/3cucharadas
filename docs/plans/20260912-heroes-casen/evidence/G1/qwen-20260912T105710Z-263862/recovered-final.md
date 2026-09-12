Review complete. Here is my independent documentary countercheck.

## 1. Source retrieval outcomes

| # | Source | Outcome | Verdict |
|---|--------|---------|---------|
| 1 | CASEN 2024 questionnaire PDF | Fetched (HTTP 200, 1.30 MB, `application/pdf`), saved as binary; **text extraction failed** (`pdftotext` not installed; shell denied; installs forbidden) | **NOT VERIFIED** by me — supplied-only |
| 2 | CASEN 2024 use-note PDF | Fetched (HTTP 200, 227.5 KB), saved as binary; same extraction failure | **NOT VERIFIED** by me — supplied-only |
| 3 | Forem `article.rb` | Retrieved (HTTP 200, raw GitHub, 73.9 KB) and read verbatim | **VERIFIED** |
| 4 | MDN "SVG as an image" | Retrieved (HTTP 200, HTML) and read | **VERIFIED** (with a nuance, see P5) |
| 5 | matplotlib `text_props.html` | Retrieved (HTTP 200, HTML) and read | **VERIFIED** (not relevant to the SVG claim) |

I did not read, print, or inspect any secrets, `.env`, SSH material, local repository files, environment variables, or private config. No files were written or modified.

## 2. Findings by proposition

### P1 — estimand definition (weighted share, v9∈{3,4} / v9∈1..11, expr national/regional, expc communal-only)
- **Severity:** LOW–MEDIUM (plausible, but instrument content not independently verified)
- **Conclusion:** The definition is internally coherent and consistent with the supplied instrument evidence. The denominator `1..11` correctly includes all valid tenure categories (the caller's evidence already flags that a `1..4` denominator would be wrong; this proposition avoids that error). "Own shared-site tenure" is the right scoping for `Propio compartido … con otras viviendas del sitio` — it is a *tenure* category, not a count of co-located dwellings, dwellings-per-site, or census dwellings.
- **Source actually checked:** none by me (PDF unreadable). Supplied-only: questionnaire printed p.79 / PDF idx 78 (v9); use-note printed pp.2–3 (expr/expc).
- **Limitations:** I could not independently confirm the v9 category text, the `1..11` range, or the exact semantics of `expc` (whether it is a communal expansion factor and whether "nonrepresentative" is the precise status). The "deduplicate to one head per household" step is an analytic design choice, not an instrument claim — it must be defended by the pipeline logic, not by the questionnaire.

### P2 — v28 principal household is auxiliary, not a universal filter, no dwelling weight
- **Severity:** LOW (sound, supplied-only)
- **Conclusion:** Internally correct and matches supplied evidence: v28 asks whether the responding household is the dwelling's *principal* household, gated on `p10=2` (multi-household dwellings). A one-household dwelling (p10≠2) stays in; a multi-household dwelling needs exactly one principal. A global v28 filter would wrongly drop single-household dwellings. Selecting a principal household does **not** manufacture an official dwelling weight.
- **Source actually checked:** none by me (PDF unreadable). Supplied-only: questionnaire printed p.83 / PDF idx 82 (v28).
- **Limitations / discard condition:** The "one-household stays in" step collapses if v28 is actually administered to single-household dwellings too (i.e., not truly gated on p10=2). I could not confirm the gating from the instrument.

### P3 — `1/(1-p/2)` is algebra, not observed evidence
- **Severity:** MEDIUM (valid methodological flag, unverifiable from any public source)
- **Conclusion:** Correct as a critique. A *household* share cannot be substituted into a formula whose `p` is a *dwelling* share over complete pairs of dwellings per site without an explicit, verified household↔dwelling↔site-pair mapping. The expression is arithmetic; nothing retrieved or supplied establishes it as an observed quantity or a fiscal adjustment.
- **Source actually checked:** none — this is an internal-consistency/mathematical critique, not a source-checkable fact.
- **Limitations:** I am evaluating the *form* of the claim (units mismatch / unverified mapping), not adjudicating the intended meaning of the formula, which was not supplied.

### P4 — AI disclosure mapping to Forem
- **Severity:** SUPPORTED (verified directly)
- **Conclusion:** The enum `ai_disclosure_level` exists in Forem's `article.rb` with exactly `{ not_disclosed: 0, no_ai: 1, some_ai: 3, fully_autonomous: 5 }`, so the proposed mapping matches. It is **article-level only** — there is no per-component (text vs hero/image) field. `some_ai` therefore does not establish *text* assistance specifically. A missing declaration leaves the default `not_disclosed` (0). All three sub-claims hold.
- **Source actually checked:** `https://raw.githubusercontent.com/forem/forem/main/app/models/article.rb` (HTTP 200). Verbatim: `enum :ai_disclosure_level, { not_disclosed: 0, no_ai: 1, some_ai: 3, fully_autonomous: 5 }`. Also confirmed `set_ai_disclosure_from_front_matter`, `ai_disclosed?`, `ai_disclosure_label`.
- **Limitations:** None material. Minor note: `set_ai_disclosure_from_front_matter` only executes when `Settings::General.enable_ai_disclosure` is enabled; the "stays not_disclosed" default still holds via the enum default.

### P5 — SVG text via `<img>` is not selectable/semantic; `<object>` does not auto-supply table semantics
- **Severity:** LOW–MEDIUM (correct in practice; the cited MDN page does not state it verbatim)
- **Conclusion:** The proposition is true as a matter of web-platform behavior, but the retrieved MDN page supports it only *indirectly*: it says JavaScript is disabled and external resources are blocked "when it's being used as an image," and that these restrictions "don't apply when SVG content is viewed directly, or when it's embedded as a document via the `<iframe>`, `<object>`, or `<embed>` elements." It does **not** literally state "text is not selectable," nor does it discuss `<object>` supplying *table* semantics. So the "don't claim an object auto-supplies table semantics" and "supply alt/description/tables separately" parts are correct, but the "text not selectable" part is an inference, not a direct quotation.
- **Source actually checked:** `https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image` (HTTP 200). The matplotlib page (`text_props.html`) is about `matplotlib.text.Text` properties/layout only — it neither supports nor contradicts the SVG claim and should not be cited as evidence for it.
- **Limitations:** If the writeup needs a *verbatim* authoritative statement on text selectability, this MDN page is insufficient; a spec reference (e.g., SVG integration / HTML `<img>` rendering of SVG) would be required.

## MODEL-REPORT

MODEL-REPORT: {"agent":"qwen","provider":"deepseek","model":"deepseek-v4-pro","source":"self_report"}

*(This is the requested self-reported identity; it is not an introspective verification of underlying weights, and it is separate from the harness metadata already present in the handoff trace.)*

# QWEN_RESULT

status: partial
caller: codex
mode: review
summary: "P4 fully verified verbatim against Forem's article.rb (enum ai_disclosure_level = not_disclosed/no_ai/some_ai/fully_autonomous, article-level only). P1/P2/P3/P5 are internally sound and consistent with caller-supplied evidence, but the two CASEN PDFs could not be text-extracted (pdftotext missing, installs forbidden), so instrument-level claims remain NOT VERIFIED by independent retrieval; P5's 'text not selectable' is inference, not a verbatim MDN statement."
files_read: "Forem article.rb (verbatim); MDN SVG_as_an_image (HTML); matplotlib text_props (HTML). CASEN questionnaire + use-note PDFs fetched but unreadable (binary, no text extraction)."
files_changed: "none"
commands_run: "none (shell denied)"
risks: "Instrument facts (v9 categories, 1..11 range, v28/p10 gating, expr/expc semantics) rest on caller-supplied evidence only; if that evidence is itself stale or miscited, P1/P2 weight and filter claims would change. The 1/(1-p/2) formula remains an unverified construct."
validation: "Forem enum confirmed verbatim; web sources retrieved 200 OK. CASEN PDFs not independently text-verified due to missing pdftotext and a denied shell; no dependencies installed."
next_action: "If independent verification of the CASEN instrument is required, re-run with PDF text extraction available (e.g. poppler-utils installed) or provide the questionnaire/use-note as extractable text/HTML; otherwise treat P1/P2 as contingent on the caller's own direct check."
