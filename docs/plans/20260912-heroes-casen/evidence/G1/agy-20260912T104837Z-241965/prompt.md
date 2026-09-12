HANDOFF-TRACE: codex le solicita apoyo a gemini-antigravity (model: __default__) via CLI
MODEL-REPORT: {"agent":"gemini-antigravity","provider":"google","model":"gemini-3.7-flash-medium","source":"agy_bridge"}

# AGY BRIDGE REQUEST

## Contract
- You are Gemini/Antigravity acting as a sidecar, not the primary agent.
- Caller: codex
- Mode: review
- Repo/CWD: public-export-redacted
- Public export mode: true
- Do not read, copy, print or modify secrets, credentials, tokens, keys, .env files or SSH material.
- Do not use --dangerously-skip-permissions.
- If critical information is missing, return status: blocked.
- End your response with exactly one final AGY_RESULT block.

## Mode rules
- plan/review/explain: do not modify files.
- test: only run bounded validation and avoid source edits except unavoidable test outputs.
- patch: implement only the requested minimal change.

## Required final block

# AGY_RESULT

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

# Public review brief: CASEN shared-site claims and AI disclosure

Review only the public propositions below. No code changes or publication.
Independent source verification is the objective, not agreement with another model.

1. CASEN 2024 v9 categories 3 and 4 describe household ownership of a site shared with other dwellings, not the number of dwellings per site.
2. A defensible indicator is the weighted share of households declaring those categories among all households with valid responses.
3. expr supports national/regional analysis; expc does not establish commune representativeness.
4. v28 is conditional on multi-household dwellings; a global v28 filter would lose single-household dwellings.
5. The algebra 1/(1-p/2) assumes p is a dwelling share in complete pairs; a household tenure share cannot be inserted without new assumptions.
6. An article-level AI disclosure should distinguish generated images from authorial text and allow unknown provenance.
7. SVG text in the downloaded file does not itself create selectable text or an accessible table in a web img element.

Check official sources; report counterexamples, exact pages, uncertainty and what would refute each proposition. Do not infer observations from mathematical identities. No raw records are needed.

Sources:
- https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf
- https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf
- https://raw.githubusercontent.com/forem/forem/main/app/models/article.rb
- https://matplotlib.org/stable/users/explain/figure/backends.html

Return a section headed AGY_RESULT with status, caller: codex, mode: review, numbered findings and source URLs/pages.
Also supply MODEL-REPORT with agent, provider, model if known, source: self_report; say unknown when unavailable.
