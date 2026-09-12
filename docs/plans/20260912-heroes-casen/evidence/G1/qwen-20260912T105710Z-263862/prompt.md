HANDOFF-TRACE: codex le solicita apoyo a qwen (model: deepseek-v4-pro) via CLI
MODEL-REPORT: {"agent":"qwen","provider":"deepseek","model":"deepseek-v4-pro","source":"qwen_bridge"}

# QWEN BRIDGE REQUEST

## Contract
- You are Qwen Code acting as a sidecar, not the primary agent.
- Caller: codex
- Mode: review
- Repo/CWD: public-export-redacted
- Public export mode: true
- Do not read, copy, print or modify secrets, credentials, tokens, keys, .env files or SSH material.
- If critical information is missing, return status: blocked.
- End your response with exactly one final QWEN_RESULT block.

## Mode rules
- plan/review/explain: do not modify files.
- test: only run bounded validation and avoid source edits except unavoidable test outputs.
- patch: implement only the requested minimal change.

## Improvement review rubric
When evaluating improvements or drift, act as an impartial contest judge. Apply
the same criteria to every author and provider. Establish the baseline, seek
reproducible counterexamples, weigh supporting and contrary evidence, and report
regressions, cost and uncertainty. Distinguish the unconstrained ideal, feasible
optimum and measured result. Do not claim perfection or empirical improvement
from a static check or consensus. This is the portable summary of the shared
improvement-judge policy; no additional access or authority is granted.

## Required final block

# QWEN_RESULT

status: success | partial | blocked | failed
caller: codex
mode: review
summary:
files_read:
files_changed:
commands_run:
risks:
validation:
next_action:

## Task

# Public review brief: documentary countercheck of CASEN and disclosure

HANDOFF-TRACE: Codex requests bounded review through Qwen Code with requested model deepseek-v4-pro. Report actual retrieval and uncertainty, never fabricated source access. This is public-source review only; no code edits, no publication, no microdata, no local repository access is needed. Do not inspect any files outside this isolated public task workspace. Do not inspect environment variables or private configuration.

The prior reviewer said all propositions were supported but invented CASEN labels and pages. Your task is independent documentary review, not consensus. You may fetch the public URLs below using available read-only web tools. If retrieval is unavailable, say NOT VERIFIED; do not claim to have checked a PDF from memory. Do not write downloaded files in review mode. Do not repair tools or install dependencies. Prefer URL/page/short source excerpt plus your inference. Use at most 25 quoted words from each source; paraphrase the rest. Distinguish supplied public evidence from sources you actually retrieve.

Primary sources:
- https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf
- https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf
- https://raw.githubusercontent.com/forem/forem/main/app/models/article.rb
- https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image
- https://matplotlib.org/stable/users/explain/text/text_props.html

Evidence already checked by the caller directly against the public questionnaire, supplied here as evidence to crosscheck, not as your own retrieval:
- Questionnaire printed page79, PDF index78, v9: category3 is 'Propio compartido (pagado) con otras viviendas del sitio'; category4 is 'Propio compartido (pagándose) con otras viviendas del sitio'. Both are own-site tenure. Categories1..11 are listed; categories5..11 include renting, ceded tenure, usufruct and irregular occupation. Thus a denominator limited to1..4 is not all valid responses.
- Questionnaire printed page83, PDF index82, v28 asks whether the responding household is the dwelling's principal household, and is enabled for dwellings with more than one household (p10=2). It is not a kitchen-use question. A global v28 filter would exclude structurally skipped single-household dwellings; no percentage loss is established from this instrument.
- Official use-note printed pages2–3 says that expr supports national, national urban/rural and regional estimation, subject to precision checks. Its table says the survey design does not assure provincial or communal representativeness; expc does not fix that. The PDF has6pages, not7.

Review these propositions and supply concrete counterexamples and discard conditions:
1. The estimand can be the weighted share of households declaring v9=3 or4 among households with valid v9=1..11, deduplicating to one head per household, weights expr for national/regional and expc only for explicitly nonrepresentative communal descriptive outputs. It describes own shared-site tenure, not all co-location, dwellings per site or census dwellings.
2. Principal-household identification is auxiliary: one-household dwelling stays in; multi-household dwelling requires exactly one principal. v28 is not a universal filter. This does not produce an official dwelling weight.
3. A household share cannot be plugged into 1/(1-p/2), whose p is a hypothetical dwelling share on complete pairs of dwellings per site, without additional unverified mappings. The equation is algebra only, not observed evidence or a fiscal adjustment.
4. Site-level AI disclosure levels no_ai/some_ai/fully_autonomous/not_disclosed can map to Forem's article field if the source enum matches. That field alone does not document components. Separate text/hero component provenance is our editorial design, not necessarily Forem's schema. Historical author declaration some_ai does not establish text assistance; missing future declaration stays not_disclosed.
5. Text nodes in a downloaded SVG do not automatically become selectable text or a semantic data table when the SVG is embedded with HTML img. Supporting tables/alt/descriptions must be supplied separately; don't claim an object element automatically supplies table semantics.

Required response: list source retrieval outcomes first (retrieved via tool vs supplied-only vs unavailable); then numbered findings with severity, conclusion, source URL/page where actually checked, and limitations. Include MODEL-REPORT with agent, provider, model, source:self_report separately from harness metadata. End with exactly one '# QWEN_RESULT' block and required fields status/caller:codex/mode:review/summary/files_read/files_changed/commands_run/risks/validation/next_action. Return partial rather than success if documentary verification is incomplete. This optional review must not block other work.
