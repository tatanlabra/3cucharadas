---
layout: single
title: "Nushell in three spoonfuls: a structured coprocessor, not a new shell"
subtitle: "From why text pipelines are brittle to whether one concrete skill fixes anything: 120 runs to find out"
date: 2026-08-29 00:00:00 +0000
categories: [ai, productivity, development, multi-agent]
tags: [nushell, shell, agents, claude-code, codex, routing, context-engineering, docker, arch-linux, benchmark]
description: "I added Nushell as a selective routing lane and measured whether it helps: microbenchmark, agent-level A/B, and statistical analysis in R with bootstrap and Clopper-Pearson. Each level of evidence contradicted the previous."
excerpt: "300 runs, three levels of evidence and a viewer in R. Each level contradicted the previous: the skill never activated, and two of the three effects I treated as established were not claimable."
author: clabra
lang: en
ref: nushell-coprocesador-estructurado
permalink: /ia/productividad/desarrollo/nushell-coprocesador-estructurado/
distribution:
  social: true
  republish: []
toc: true
toc_sticky: true
comments: true
author_profile: true
repo: https://github.com/tatanlabra/penta-agent
entorno: "EndeavourOS (Arch), zsh, nushell 0.115.1, Claude Code + Codex on the same workspace"
header:
  teaser: /assets/images/teasers/teaser-structured-shell.webp
  og_image: /assets/images/structured-shell/og-1200.webp
  og_image_alt: "A/B results: skill activation went from 0/15 to 14/15 over two tuning rounds, with no over-activation"
---

A coding agent lives on text. Ask it which processes use the most memory, it gets four hundred lines
of space-aligned columns, and it has to work out with `awk` where the column it cares about starts.
Every one of those steps is a place where the answer can come out wrong **without an error**: one
`2>/dev/null` too many, a date format the local implementation rejects, a flag that silently excludes
half the tree.

This post is about whether it is worth putting a typed shell into that gap. It starts with the
general problem, moves to what I built, and ends in 120 runs measuring whether it helps. The
uncomfortable part up front: the first version of what I built **never activated**, and I would have
found out late had I stopped at the benchmark people usually publish.

## The problem is not the shell: it is the text

The brittleness of text pipelines was documented long before agents existed. Greenberg and Blatt
built an executable formal semantics for the POSIX shell and describe their object of study bluntly:
*"Its power and its subtlety are a dangerous combination."* Their experiment is the hard data: they
compared their semantics against **seven shells that aim for POSIX compliance** — bash, dash, zsh,
OSH, mksh, ksh93 and yash — across three test suites. The operational conclusion is that standard
conformance is something to measure, not assume[^smoosh].

It is not that the pipeline lacks structure: it has one, just implicitly. Handa and colleagues
formalised an *order-aware* dataflow model for Unix pipelines, proved the parallelising
transformations correct, and evaluated them on 47 pipelines[^dataflow]. The data model exists —
it just lives in the head of whoever wrote the command, not in the tool.

For a human at a terminal, that is manageable. For an agent chaining commands without seeing the
intermediate output, every implicit assumption is a silent failure waiting its turn.

## Why I did not replace the shell

The obvious temptation is to switch shells. The literature suggests that is a bad idea. Greenberg,
Kallas and Vasilakis, reviewing fifty years of the shell, put it in one sentence: *"While many
replacement shells have been proposed, the Unix shell persists."*[^next50] It persists because it is
critical infrastructure and because almost everything else assumes its semantics.

Nushell promises the opposite of text. Its own site puts it this way: *"Nu pipelines use structured
data so you can safely select, filter, and sort the same way every time. Stop parsing strings and
start solving problems."*[^nushell] That is a promise, not a result — and the rest of this post is
the attempt to check it.

So I treated it as a **routing problem**, not a language one. `zsh` is still the shell. There are
four lanes, and the lowest one that solves the task robustly always wins:

```text
1. native command          git · systemctl · pacman · ssh · rsync
2. specialised tool        rg · jq · yq · awk
3. Nushell                 typed data, several transformations
4. analytical engine       DuckDB · Python · Polars · R
```

The success criterion, which is counter-intuitive and worth fixing before measuring anything:

> Success is not the agent using Nushell a lot. It is using it **rarely**, and precisely when typed
> structures reduce parsing, errors, or context. Frequent activation is a routing defect, not an
> achievement.

The closing question, before writing `nu`: *am I exploiting typed structured data, or just running a
command through another shell?* If it is the latter, don't use it.

## What I built

Little, on purpose. Nushell was already installed via `pacman`, so nothing had to be touched.

- **A skill** carrying the routing policy, projected by symlink to Claude Code and Codex, and by
  transformation to Copilot.
- **A router rule** with deliberately narrow terms. A bare `json` is **not** among them.
- **A sixty-line wrapper**, `nu-query`: `nu -n -c` with no personal config, a timeout, an enforced
  JSON contract, a row cap that **states how many rows it dropped** instead of truncating silently,
  and one log line with shape and cost — never the query text.

```json
{"rows_total": 462, "rows_shown": 2, "truncated": true, "data": [ … ]}
```

- **Two gates**: positive and negative routing cases, and a smoke test that runs the skill's real
  examples against the installed Nushell.

One decision worth writing down: **the wrapper is not on the auto-approved permission list, on
purpose.** `nu -c` can mutate the system; authorising it by pattern would be an escape hatch around
the permission manager. I considered a denylist of dangerous commands and dropped it: a guarantee
based on string matching is not a guarantee. That is friction I chose to pay.

### The gate went red on day one, and that was right

I wrote eleven negative cases, one per category the policy forbids routing to Nushell. Ten passed.
The eleventh did not:

```text
"Install nushell following the project's official documentation."
  → structured_shell rule → skill activated
```

The routing term was a bare `nushell`, so any phrase naming the tool activated it, including an
installation — which the policy itself forbids. The fix was replacing it with usage phrases.

Then I broke the gate on purpose in both directions, because **a gate that has never been seen red is
not a gate**: I removed a positive term and the positive case failed; I added `json` to the terms and
the `jq` negative case failed. Restored, green.

## Five traps that showed up before I wrote the first pipeline

I diagnosed the environment before touching it. That phase produced more value than the integration
itself.

### 1. `ls **/*` skips hidden entries, silently

Nushell's glob does not descend into `.git`, `.venv-*`, or anything starting with a dot. No error: it
just returns fewer rows.

```bash
nu -n -c 'ls   **/* | where type == file | length'   # ≈ 46,400
nu -n -c 'ls -a **/* | where type == file | length'  # ≈ 127,900
```

**64% of the tree is invisible by default.** It mirrors a trap I already had documented for `fd` and
`rg`, which honour `.gitignore` even when you think they don't. Different criterion, same symptom.

### 2. Claude Code shadows `find` and `grep` inside its own Bash tool

I did not see this one coming. The shell snapshot Claude Code injects into every session contains,
verbatim:

```bash
# Shadow find/grep with embedded bfs/ugrep
unalias find 2>/dev/null || true
function find { … ARGV0=bfs "$_cc_bin" -S dfs -regextype findutils-default … }
```

Inside the agent's Bash tool, `find` **is `bfs`**, not GNU findutils. And `bfs` rejects the relative
syntax GNU accepts:

```bash
find . -type f -newermt '-30 days' -size +1M -printf '%s\t%p\n'
# bfs: error: Invalid timestamp.
```

The real failure was what came next: with `2>/dev/null` inside a pipeline, that returned **0 bytes
with exit code 0, in 14 ms**. A silent false negative that reads as "there are no large files". It is
exactly the kind of cross-implementation divergence Greenberg and Blatt measured across seven
shells[^smoosh], happening two layers up.

### 3. The default output is localised, which makes it unparseable

```text
╭───┬───────────────┬──────┬─────────┬──────────────╮
│ # │     name      │ type │  size   │   modified   │
├───┼───────────────┼──────┼─────────┼──────────────┤
│ 0 │ AGENTS.md     │ file │ 15,5 kB │ an hour ago  │
```

Box-drawing characters, wrapped lines, relative dates, and an **`es_CL` decimal comma**: `15,5 kB`.
The contract towards an agent is always `| to json`. The pretty table is for the human.

### 4. `from ndjson` does not exist in 0.115.1

Docker and several other CLIs emit **NDJSON**: one object per line, not an array. `from json` fails,
and `from nuon` gives `error when loading nuon text`, which is quite misleading. The correct pattern:

```nu
docker ps -a --format json | lines | each {|l| $l | from json} | group-by Image
```

### 5. `ps | get cpu` is not the `%CPU` of `ps aux`

Nushell samples CPU instantaneously; `ps` averages over the process lifetime. Measured seconds apart
on the same PIDs:

| PID | process | `nu ps` cpu | `ps -eo pcpu` |
|---|---|---|---|
| 1146712 | llama-server | 0.00 | 18.2 |
| 1124940 | chrome | 281.25 | 500 |

Memory is comparable. CPU answers different questions.

## First level of evidence: pipeline against pipeline

The kind usually published. Three tasks where the skill claims Nushell helps, plus a fourth measuring
the central claim about reducing context. Median of three runs; no `hyperfine` on this machine, so I
do not interpret differences under ~50 ms.

| Task | Variant | Steps | Time | Bytes |
|---|---|---|---|---|
| files >1 MB, last 30 days | `find+sort+head` | 3 | **317 ms** | 588 |
| files >1 MB, last 30 days | nushell | 1 | 1,137 ms | 971 |
| top 5 processes by memory | `ps+awk` | 3 | **17 ms** | 103 |
| top 5 processes by memory | nushell | 1 | 225 ms | 356 |
| containers by image | `docker+sort+uniq` | 3 | **16 ms** | 339 |
| containers by image | nushell | 1 | 33 ms | 603 |
| how much context enters | raw `docker ps -a` dump | 1 | 16 ms | **3,353** |
| how much context enters | nushell, reduced | 1 | 32 ms | **566** |

<figure>
  <img src="/assets/images/structured-shell/fig-microbenchmark.svg"
       alt="Four panels showing the time distribution per task; each point is one of the 25 runs, with median and confidence interval" loading="lazy">
</figure>

<figure>
  <iframe src="/assets/visores/structured-shell/index.html" title="Interactive benchmark viewer"
          loading="lazy" style="width:100%;height:660px;border:1px solid #2a3041;border-radius:6px"></iframe>
  <figcaption style="font-size:.85em;opacity:.75;margin-top:.4em">
    Interactive viewer: switch task and metric, and jump to the agent A/B and the verdict.
    The data is precomputed in R; the page only draws. It weighs 28 KB.
  </figcaption>
</figure>

The table summarises; the figure shows what the table hides. Each point is a real run. With 25 per
variant the intervals are tight and the verdict is not up for debate: the ratio of medians is
**3.49×** on the files task (95 % CI [3.41; 3.57]) and **11.80×** on the process one ([11.00; 12.15]).
Nushell does not lose narrowly.

**Nushell loses on time, every time.** Up to 3.6× slower on the tree sweep: it starts an interpreter
and walks without `find`'s optimisations. Anyone choosing it for speed picked the wrong reason.

**On small results it also loses on bytes.** Five rows of indented JSON weigh more than five lines of
plain text. The "less output" promise only holds when there is something to reduce: in the last row
the question is answered with 566 bytes instead of a 3,353-byte dump — and the summary carries *more*
information, because it includes how many containers of each image are running.

Where it wins is steps and semantics: `size > 1mb` and `modified > ((date now) - 30day)` are typed
comparisons; the Bash version needs `-printf`, an absolute date computed separately, and a `sort -rn`
on the right column. Three places to be silently wrong, against zero.

And there was one concrete payoff. This query, while testing the third task:

```nu
docker ps -a --format json | lines | each {|l| $l | from json}
  | where Image =~ "paper-search" | select ID State Status
```

returned **between 7 and 10 containers of the same MCP server running at once**, the oldest at
`Up 16 hours`. Orphaned stdio containers: every editor session starts its own and nobody recycles
them. The information had been sitting in `docker ps -a` all along, in a format nobody looks at.

**But none of this answers the question that matters.** It compares pipelines I wrote, so it measures
my pipeline-writing. The real question is whether *the agent* solves a natural-language request better
with the skill. That needs a different experiment.

## Second level: agent against agent

Five tasks in Spanish — three where the policy says Nushell helps, two where it forbids it — asked of
headless Claude Code (`claude -p --output-format json`, Sonnet). The only thing that changes between
arms is whether the skill is available. Each task's ground truth is computed by an independent command
**immediately before** each run, so environment volatility is not mistaken for accuracy. The commands
the agent actually ran come from the session transcript, not from what it claims to have done.

### The first version never activated

**Zero out of fifteen.** With the skill available, the agent never invoked it, and the with-skill arm
was statistically indistinguishable from the one without: same accuracy, same commands, same shape.
The skill was **inert**.

The fix was not intuition. The Claude Code docs state three concrete things I was not doing: the
`description` should **put the key use case first**, there is a `when_to_use` field meant exactly for
*"trigger phrases or example requests"*, and the combined text is **truncated at 1,536 characters** —
from the end, which is where the negative examples live. My description opened with routing philosophy
and had no `when_to_use`.

**Round 1.** I rewrote the description to open with what it answers, and added 18 literal request and
rejection phrasings. Activation: **0/9 → 5/9** on positive tasks.

Better, but half-done. Looking at where it failed produced the useful data point: the failures were
spread across all three tasks **with the exact same prompt**. Not a vocabulary gap — variance. Even so
there was a concrete misalignment on the worst task: I wrote "use the most memory" and the prompt says
"the 3 processes using the most **resident memory**".

**Round 2.** I added 7 more phrasings aimed at the actual wording, plus a clause neutralising a
counter-signal I suspected: all three prompts end in *"Answer ONLY… No explanations"*, so I wrote that
asking for a short answer **constrains how to present the data, not how to obtain it**.

Activation: **5/9 → 28/30** (93 %). That leaves 32 characters of headroom under the cap; more
phrasings now means removing others.

### What it wins and what it costs

Final state: **100 runs** across two separately measured batches, 30 per arm on positive tasks and
20 on negative ones.

| Subset | Arm | Correct | Fired the skill | Median time | Output tokens |
|---|---|---|---|---|---|
| positive | `no_skill` | 23/30 | 0/30 | **6,239 ms** | **152** |
| positive | `with_skill` | **30/30** | **28/30** | 9,537 ms | 368 |
| negative | `no_skill` | 20/20 | 0/20 | 5,220 ms | 91 |
| negative | `with_skill` | 20/20 | **0/20** | 5,107 ms | 99 |

<figure>
  <img src="/assets/images/structured-shell/fig-ab-tiempo.svg"
       alt="Time distribution per arm on positive tasks, with one outlier run at 87 seconds" loading="lazy">
</figure>

That lone point at the top is an **86,852 ms** run, the first one, cold. It is the reason I read
medians and not means throughout: the with-skill arm's mean is 14,428 ms against a median of 9,537,
inflated 1.5× by that single value. With means I would say "2.3× slower"; the ratio of medians is
**1.53×**, interval [1.26; 2.22].

<figure>
  <img src="/assets/images/structured-shell/fig-ab-tokens.svg"
       alt="Output token distribution per arm on positive tasks" loading="lazy">
</figure>

On tokens the ratio is **2.43×** [1.22; 3.82]. That interval matters: with half the sample it was
[0.92; 4.18] — it **included 1**, and therefore did not allow claiming any difference at all.
Doubling the runs is what turned an impression into a result.

<figure>
  <img src="/assets/images/structured-shell/fig-ab-proporciones.svg"
       alt="Accuracy and activation per arm with exact Clopper-Pearson intervals" loading="lazy">
</figure>

And the breakdown I liked most: **on tasks where the skill should not fire, it costs nothing.**
5,220 ms against 5,107, 91 tokens against 99. Differences below the noise, and **0 activations out
of 20**. Taking activation to 93 % dragged along not a single improper one.

### Efficiency, where the skill does not come out well

Separate medians for accuracy and cost hide the question that actually matters: *how much does an
answer that works cost?* That metric combines both axes and penalises the cheap arm that gets it
wrong.

<figure>
  <img src="/assets/images/structured-shell/fig-eficiencia.svg"
       alt="Cost per correct answer in tokens and seconds, with overlapping intervals" loading="lazy">
</figure>

**It does not pay off.** 458 tokens per correct answer with the skill against 300 without; 14.4
seconds against 9.3. The extra accuracy does not cover its own cost. The intervals overlap, so there
is no evidence of a difference — and overlap is a conservative test, not an acquittal.

If your criterion is "minimise tokens per useful answer", this result says do not enable the skill.
If it is "do not be wrong on metadata queries", it says the opposite. Measurement does not choose
for you; it only stops you choosing while believing something false.

### The task that decides it, and why it fails without the skill

The discriminating task is *"the 3 largest files over 1 MB modified in the last 30 days"*. Without the
skill: **3 of 10**. With it: **10 of 10**.

The reason has nothing to do with Nushell. **Most no-skill runs solved it with
`fd -I … --changed-within 30d`**, and lost a 434 MB file living inside `.venv-qwen-staging`. `fd -I`
lifts `.gitignore` **but still skips hidden entries**: that needs `-H`, a different flag. The ones that got it right used `find`.

With the skill active, all ten runs used `ls -a **/*` and all ten were correct. The mechanism is
verifiable in the transcripts, not inferred: the skill documents that trap on the first page of its
gotchas, the agent reads it, and applies the `-a`.

And preferring `fd` over `find` is a rule imposed by my own global instructions file, together with
the note about `-I`. The note is incomplete, and that instruction is producing wrong answers across a
whole class of tasks. I found it while measuring something else.

### The sixth trap, which only the experiment could find

Looking at the outliers produced the best finding of the work. One run burned **77 seconds, 15 turns
and 3,714 output tokens**, against a median of 15 seconds for that task. I went to read what it had
done:

```text
docker ps -a --format json | nu -n -c 'lines | each {|l| $l | from json} | group-by image …'
docker ps -a --format json | head -c 300      # what is actually arriving?
echo hello | nu -n -c '$in'; echo "exit:$?"   # does anything come in on stdin?
nu --help 2>&1 | rg -i "stdin|--commands"
cat penta-agent/scripts/agent/nu-query | head -60   # it started reading my wrapper
```

It was fighting this, and the fault was mine:

```bash
printf 'a\nb\n' | nu -n -c 'lines | to json --raw'
# null
# exit=0
```

**`nu -n -c` does not read stdin.** A Bash pipe into it is ignored, the pipeline receives `nothing`,
and it returns `null` **with exit code 0**. It does not fail: it lies. For an agent that is far worse
than an error, because it looks like an answer.

The source was my own examples. The skill wrote `docker ps -a --format json | lines | each {...}`,
which is a **Nushell-internal** pipeline but reads exactly like a Bash one. The agent did the
reasonable thing and hit a silent failure.

```bash
# put the external command INSIDE, in parentheses  ← preferred
nu -n -c '(docker ps -a --format json) | lines | each {|l| $l | from json} | group-by Image'

# or, if the data already comes down a Bash pipe, you need --stdin
docker ps -a --format json | nu -n --stdin -c 'lines | each {|l| $l | from json}'
```

`nu-query` now detects stdin and adds `--stdin` only when needed, and the smoke test watches all
three things. The effect, measuring just that task before and after:

| | Time | Output tokens | Turns | Tool calls |
|---|---|---|---|---|
| before | 70,901 ms | 3,287 | 14 | 12 |
| after | **7,852 ms** | **303** | 4 | 2 |

**9× faster and 10.8× fewer tokens, without touching a line of Nushell.** Just clarifying the skill's
documentation and giving the wrapper stdin.

### What this experiment does not prove

Five tasks, five repeats, one model, one machine. At low n, a difference of 1/3 against 0/3 is noise:
the first repeat of one round suggested the skill won 3/3 on the hard task, and the following ones
dissolved it. I also discarded the cost and *new token* columns: they depend on whether a run hit the
API prompt cache, and the same task in the same arm gave 26,293 tokens in one run and 188 in another.

And a caveat about the tuning: **I measured, changed the description, and measured again on the same
five tasks.** That risks fitting the test rather than the problem. The phrasings I added are generic
and do not copy the prompts, but the only way to rule it out is a fresh task set the description has
never seen. I did not do that.

## How the numbers were read, and why a viewer was needed

The first version of this post reported medians in tables. A median without its distribution invites
you to read sampling noise as signal, and here that was not hypothetical: the microbenchmark **kept
only the median and threw every run away**. You could not see dispersion, spot an outlier, or put an
interval on anything. The first fix was making it emit one line per run; that is where the 200 runs
of the first level and the 100 of the second come from.

The analysis runs in R on an isolated conda environment (`/opt/entornos/r-geo`, R 4.5.3), and the
viewer is a four-tab Shiny app you start locally:

```bash
/opt/entornos/r-geo/bin/Rscript -e 'shiny::runApp("app.R", port = 4005)'
```

Five statistical decisions, and the reason for each:

**Median, never mean.** An 87-second run inflates the mean 1.5×. The outlier is not discarded —
throwing away inconvenient data is how you manufacture a result — it is shown, and estimated with
something that does not get dragged by it.

**Percentile bootstrap, not a t-test.** With 5 runs per cell and right-skewed distributions, the
normality assumption does not hold. Ten thousand resamples give the median's interval without
assuming any shape.

**Exact Clopper-Pearson for proportions.** With 30 correct out of 30, the normal method gives a
zero-width interval, [1; 1], claiming absolute certainty from 30 observations. The exact one gives
[0.88; 1], which is what the evidence supports.

**Ratio of medians as the effect size.** "How many times more" compares across tasks; a difference
in milliseconds does not. And it has a useful property: **if the interval crosses 1, there is no
result.** That is a stopping rule, not decoration.

**Fisher's exact test for the 2×2** accuracy table, which is what low counts call for.

None of this required installing anything: `boot` and `binom` are not in that environment, and both
the bootstrap and Clopper-Pearson come out of base R in twenty lines.

### What the rigour changed, and it was not cosmetic

With the first half of the sample, this is what I had:

| Effect | n = 15 per arm | n = 30 per arm |
|---|---|---|
| Time | 1.70× [1.19; 3.11] · conclusive | **1.53× [1.26; 2.22]** · conclusive |
| Tokens | 2.39× **[0.92; 4.18]** · CI crosses 1 | **2.43× [1.22; 3.82]** · conclusive |
| Accuracy | Fisher **p = 0.0996** | Fisher **p = 0.0105** |

Two of the three effects I was treating as established **were not claimable** with the sample I had.
I did not know until I computed the intervals, and the right answer was not to soften the headline:
it was to run fifty more. I also checked the two batches do not differ before pooling them — medians
of 5,660 and 6,381 ms without the skill, 9,650 and 9,424 with it — because pooling data from
different moments without looking is another way to manufacture a result.

That is the whole case for statistical tooling in a technical post: it does not decorate the
conclusion, it **changes** it. And it is cheap: the viewer and the metrics are about three hundred
lines of R over data that already existed.

## Verdict

The gates pass, the skill reaches both agents, and routing holds in both directions. Measured at
agent level across 100 runs, with the effects that **are** claimable:

- **Task success:** wins. 30/30 against 23/30 on positive tasks, Fisher exact **p = 0.0105**. On the
  hard task, 10/10 against 3/10.
- **Activation:** from 0 % to **93 %** (28 of 30), over two description tuning rounds.
- **Over-activation:** none. **0 of 20**, with the most aggressive wording.
- **Cost where it should not fire:** zero. 5,220 ms against 5,107, below the noise.
- **Cost where it should:** **1.53×** the time [1.26; 2.22] and **2.43×** the tokens [1.22; 3.82].
- **Efficiency:** **it does not pay off**. 458 tokens per correct answer against 300. The extra
  accuracy does not cover its cost, though the intervals overlap so that is not conclusive.

That profile is defensible on one condition: that you know what you are optimising. It stays out of
the way where it does not apply, it is right where it does, and it costs more per useful answer. If
your bottleneck is tokens, do not enable it; if it is being wrong on metadata queries, do.

I did not implement an MCP, and the path is right there: `nu 0.115.1` ships an MCP server mode in the
binary itself. That is precisely why the answer is no, for now: an operation gets promoted to a
dedicated tool only if it recurs, has a stable interface, can be defined with typed parameters, would
be reused by several agents, and offers a real security or observability advantage. I have two
candidates noted and neither meets all five.

What I take from this is not about Nushell. It is that there were **three levels of evidence and each
one contradicted the previous**. The microbenchmark said Nushell was slower and little else. The
agent-level A/B found that the skill never activated — and that fixing it changed the result
entirely. And the robust metrics showed that two of the three effects I treated as established were
not claimable with the sample I had.

None of the three came from reading code. They came from measuring, from looking at the distribution
instead of the summary, and from accepting that "cannot conclude" is a conclusion.

## References

[^smoosh]: Michael Greenberg and Austin J. Blatt, "Executable formal semantics for the POSIX shell", *Proceedings of the ACM on Programming Languages* 4, no. POPL (2019): 1-30. <https://doi.org/10.1145/3371111>

[^next50]: Michael Greenberg, Konstantinos Kallas and Nikos Vasilakis, "Unix shell programming", *Proceedings of the Workshop on Hot Topics in Operating Systems* (HotOS '21), 104-111. <https://doi.org/10.1145/3458336.3465294>

[^dataflow]: Shivam Handa, Konstantinos Kallas, Nikos Vasilakis and Martin C. Rinard, "An order-aware dataflow model for parallel Unix pipelines", *Proceedings of the ACM on Programming Languages* 5, no. ICFP (2021): 1-28. <https://doi.org/10.1145/3473570>

[^nushell]: Nushell, "A new type of shell", official project site, accessed 29 August 2026. <https://www.nushell.sh/>
