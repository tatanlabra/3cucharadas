# Distribution source — Nushell as a selective route

## Central claim

A structured shell helped a coding agent on some task families, but it also increased latency and output tokens, and it made no accuracy difference in a real aggregate case. The defensible result is a bounded routing rule, not a general claim that Nushell is better than a text shell.

## Evidence that every adaptation must preserve

- The full corpus contains 380 runs: 200 pipeline microbenchmarks, 100 tuned agent A/B runs, 50 held-out runs, and 30 observations from an aggregate thesis case.
- In the tuned positive tasks, observed accuracy was 30/30 with the skill and 23/30 without it; median time rose from 6,239 ms to 9,537 ms and median output from 152 to 368 tokens.
- In the held-out positive tasks, observed accuracy was 14/15 with the skill and 10/15 without it; only 4/15 treatment runs activated Nushell.
- Nushell was slower in every timed microbenchmark; it materially reduced output only in the aggregation task, from 3,353 to 566 bytes.
- In the aggregate thesis case, both arms were correct in all 30 observations. The policy used Nu in 10/10 structured treatment observations and 0/5 conceptual ones, but did not improve accuracy.
- The recurring `fd -I` error omitted hidden files; `-H -I` or `-u` was required.
- A Bash-to-Nu pipeline returned `null` with exit code 0 until `nu --stdin -c` was used.

## Limits that every adaptation must preserve

- The task families are few, repeated, and partly tuned during development.
- Runs within a family are not independent problem types; the reported Fisher test is exploratory.
- The thesis case uses public aggregates only and does not support institutional claims from `presence=0`.
- Measurements describe EndeavourOS/Arch, zsh, Nushell 0.115.1, Claude Code, and Codex on one machine.
- The project that implemented the skill also produced the measurements.

## Routing rule retained after measurement

Use Nushell when a task combines structured data, multiple transformations, and a concrete risk of silent parsing failure. Prefer a native command or specialised utility for simpler operations, and an analytical engine for larger or more complex analysis.

## Canonical evidence

- English article: https://3cucharadas.cl/en/ia/productividad/desarrollo/nushell-coprocesador-estructurado/
- Spanish article: https://3cucharadas.cl/ia/productividad/desarrollo/nushell-coprocesador-estructurado/
- Reproducible aggregate case: https://github.com/tatanlabra/3cucharadas/tree/main/research/structured-shell-thesis-case
