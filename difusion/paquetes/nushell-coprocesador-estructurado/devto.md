---
title: "When should a coding agent use Nushell? Evidence from 380 runs"
published: false
description: "A selective Nushell route improved accuracy on some agent tasks, but cost time and tokens and made no accuracy difference in a real aggregate case."
tags: nushell, ai, productivity, testing
canonical_url: "https://3cucharadas.cl/en/ia/productividad/desarrollo/nushell-coprocesador-estructurado/"
cover_image: "https://3cucharadas.cl/assets/images/structured-shell/og-1200-en.webp"
---

I did not replace my shell with Nushell. I added it as one route in a tool-selection policy for coding agents, then measured whether that route earned its place.

The answer was conditional. It improved observed accuracy on some task families, but it was slower in every timed pipeline benchmark, increased agent output tokens, and made no accuracy difference in an aggregate case based on a governed reconstruction of my master's thesis.

## The routing rule

The agent receives four lanes, ordered by complexity:

1. Use a native interface for `git`, `systemctl`, `pacman`, `ssh`, or `rsync`.
2. Use a specialised utility such as `rg`, `jq`, `yq`, `awk`, or `fd` for one focused transformation.
3. Use Nushell for several transformations over tabular or typed data.
4. Use DuckDB, Python, Polars, or R when the volume or analytical logic calls for an engine.

The success criterion is not frequent activation. The route is successful only when it enters for a concrete structural reason and stays out when a simpler tool is sufficient.

The wrapper around Nu returns a bounded JSON envelope instead of a display table. Its fields report the total row count, the number of rows returned, whether truncation occurred, and the bounded data payload.

It runs without personal configuration, applies a timeout, caps rows, and reports truncation explicitly. It is deliberately not auto-approved: `nu -c` can mutate the system.

## What the small benchmarks said

I compared four tasks, two implementations per task, and 25 repetitions per implementation: 200 pipeline runs.

| Task | Text-oriented route | Nushell route |
|---|---:|---:|
| Files over 1 MB, modified in 30 days | 389 ms | 1,315 ms |
| Five processes using the most memory | 22 ms | 233 ms |
| Containers grouped by image | 19 ms | 40 ms |
| Reduce `docker ps -a` context | 17 ms; 3,353 B | 39 ms; 566 B |

Nushell was slower every time. It materially reduced output only when the task actually aggregated data: 3,353 bytes became 566 bytes.

That result is useful because it rules out a common shortcut: typed pipelines are not automatically faster or smaller.

## What changed when an agent chose the command

The tuned A/B corpus contained three positive task families and two negative ones, repeated ten times per arm: 100 runs.

- Positive tasks without the skill: 23/30 correct, 6,239 ms median, 152 median output tokens.
- Positive tasks with the skill: 30/30 correct, 9,537 ms median, 368 median output tokens.
- Negative tasks: 20/20 correct in both arms, with 0/20 Nushell activations in the treatment arm.

The accuracy signal came with 1.53× median time and 2.43× median output tokens. Those figures describe the tuned corpus, not a general performance rate.

A later 50-run holdout reduced the apparent reach of the policy. Positive accuracy was 14/15 with the skill and 10/15 without it, but Nushell activated in only 4/15 treatment runs, all from one family. Two other positive families were solved correctly without invoking it.

## Two failures worth keeping

The most informative results were implementation failures.

First, `fd -I` ignores exclusion rules but does not include hidden files. The correct route for that task required `-H -I` or `-u`. A command can look intentionally broad and still omit the files that decide the answer.

Second, piping Bash into `nu -c` returned `null` with exit code 0 in the tested case. The route needed `nu --stdin -c`. After that correction, one run fell from 70,901 to 7,852 ms and from 3,287 to 303 output tokens. This is a causal observation for one task, not a general benchmark.

## A real aggregate counter-test

The final case used public aggregates derived from a reconstruction of my master's thesis: a 306,768-row, 263-column source reduced to 21 annual rows. No microdata or identifiers entered the repository.

Three tasks, two arms, and five repetitions produced 30 observations. Both arms were correct in all tasks. Within the treatment arm, Nu appeared in 10/10 structured observations and 0/5 conceptual ones, but it did not improve accuracy.

That is the boundary I wanted the experiment to find. A routing policy can behave exactly as designed and still make no material difference to the outcome.

## The rule I kept

Use Nushell when all three conditions hold:

- the input is genuinely structured;
- the answer requires several transformations;
- text parsing creates a concrete risk of silent failure.

Otherwise, prefer the lower-complexity lane. For larger analysis, move up to an analytical engine instead of stretching a shell into one.

The measurements come from EndeavourOS/Arch, zsh, Nushell 0.115.1, Claude Code, and Codex on one machine. The task families are few and partly tuned, so this is bounded evidence, not a universal shell ranking.

The full article, interactive R viewer, data, and reproducible aggregate case are available at the canonical source.
