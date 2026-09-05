---
layout: single
title: "Nushell in three spoonfuls: when does a structured shell actually help an agent?"
subtitle: "R, microbenchmarks, and 380 runs to separate improvement, regression, and no material difference"
date: 2026-08-29 00:00:00 -0400
last_modified_at: 2026-09-05 00:00:00 -0400
categories: [ai, productivity, development, multi-agent]
tags: [nushell, shell, agents, claude-code, codex, routing, context-engineering, docker, arch-linux, benchmark, r]
description: "I tested whether selectively routing coding-agent tasks through Nushell helps: it improved accuracy on some tasks, increased latency and output tokens, and made no accuracy difference in a real aggregate case."
excerpt: "A tuned corpus, a holdout, and an aggregate reconstruction of my master's thesis show when Nushell helps, when it hurts, and when it changes nothing that matters."
author: clabra
lang: en
ref: nushell-coprocesador-estructurado
permalink: /ia/productividad/desarrollo/nushell-coprocesador-estructurado/
distribution:
  social: true
  republish: [dev, medium]
toc: true
toc_sticky: true
comments: true
author_profile: true
repo: https://github.com/tatanlabra/penta-agent
entorno: "EndeavourOS (Arch), zsh, Nushell 0.115.1, and Claude Code + Codex on the same workspace"
header:
  teaser: /assets/images/teasers/teaser-structured-shell-en.webp
  og_image: /assets/images/structured-shell/og-1200-en.webp
  og_image_alt: "A data stream enters a processing core and splits into three structured routes shown in blue, magenta, and grey"
en_abstract: >
  I tested whether a selective Nushell route makes sense for coding agents instead
  of assuming that a typed shell must be better. The evidence comprises 380 runs:
  a 200-run pipeline microbenchmark, a tuned 100-run agent A/B test, a 50-run
  holdout, and a 30-run aggregate case based on a governed reconstruction of my
  master's thesis. Nushell improved accuracy in some task families, increased
  latency and output tokens, and produced no accuracy advantage in the real
  aggregate case. The defensible result is therefore a bounded routing rule, not
  a claim that Nushell is generally superior.
---

## Prelude — Does structure actually help?

In late August 2026, I heard Lorenzo Carbonell of [atareao.es](https://atareao.es/) discuss Nushell and its advantage when working with structured data. One question stayed with me: **could that structure genuinely improve my workflow?**

The Unix shell works well, but many of its pipelines depend on text, column positions, and options whose behaviour can differ across implementations.[^greenberg-2020] Nushell takes a different approach: it preserves tables and typed values—dates, numbers, or file sizes, for example—throughout the pipeline.[^nushell]

I did not want to replace `zsh`. I used Nushell as a selective route instead, then tested the decision against three possible outcomes:

- **improvement**, if accuracy rises enough to justify the cost;
- **regression**, if it adds time, tokens, or complexity without compensating benefits;
- **no material difference**, if the technical route changes but the relevant outcome does not.

To test this, I wrote a *skill* (a rule that guides an agent on when to use a tool) and collected **380 runs**: 200 pipeline comparisons, 100 A/B runs on a tuned corpus, 50 runs on held-out tasks, and 30 observations from a real aggregate case inspired by the reconstruction of my master's thesis.

That is a large number of repetitions across only a few task families. Part of the integration was also tuned during the process. The results are therefore **bounded exploratory evidence, not a universal test**.

The question is not whether Nushell is better than Bash:

> **When does a structured route improve an agent's work, when does it make it worse, and when does it make no material difference?**

---

## Route before you replace

The policy uses the least complex tool that can solve the task robustly.

| Level | Preferred tool | Preferred use |
|---|---|---|
| 1 | `git`, `systemctl`, `pacman`, `ssh`, `rsync` | The operation already has a direct interface. |
| 2 | `rg`, `jq`, `yq`, `awk`, `fd` | A specialised utility handles the transformation. |
| 3 | Nushell | Several transformations over tabular or typed data. |
| 4 | DuckDB, Python, Polars, or R | The volume or logic calls for an analytical engine. |
{: tabindex="0" aria-label="Tool-routing policy"}

Before comparing results, it helps to locate the shell families. Sharing the word *shell* does not mean they carry the same kind of information: `zsh` usually orchestrates text and commands, while Nushell preserves structured values. This is an orientation map, not a ranking.

<figure>
  <picture>
    <source media="(max-width: 40em)" srcset="/assets/images/structured-shell/fig-d2-shell-families-mobile-en.svg">
    <img src="/assets/images/structured-shell/fig-d2-shell-families-en.svg"
         alt="D2 diagram. Text shells sh, Bash, and zsh pass text between programs; fish is an interactive non-POSIX shell; Nushell carries records, columns, numbers, and dates; PowerShell pipes .NET objects. The experiment compares only selective routing between zsh and Nushell."
         loading="lazy">
  </picture>
  <figcaption><strong>D2 — Where Nushell fits.</strong> A conceptual map for reading the routing rule, not a ranking of shells or a comparison with fish or PowerShell.</figcaption>
</figure>

The practical rule is simple: **if Nushell merely runs, inside another shell, a command that already works well, it is unnecessary**.

The integration consists of a *skill*, narrow activation rules, and a small wrapper named `nu-query`, which returns JSON, enforces a timeout, and states whether it truncated rows. I did not add it to the auto-approved permission list: `nu -c` can modify the system.

The failures that surfaced before measurement were more useful than any benchmark. In the tested environment, `ls **/*` omitted hidden paths, Claude Code substituted some commands with different implementations, and localised output made parsing harder. In that tree, `ls **/*` found roughly 46,400 files while `ls -a **/*` found about 127,900: omitting `-a` excluded close to 64%. This is not a general property of Nushell; it is a dated warning about a silent failure observed in that environment.

---

## Measure with R, not impressions

### First level: pipeline against pipeline

The first experiment was a **microbenchmark** (a repeated comparison of small, tightly scoped tasks): four tasks, two variants, and 25 repetitions per variant, for **200 runs** in total. I analysed the results with R 4.5.3.

| Task | Variant | Median time | Output |
|---|---|---:|---:|
| Files > 1 MB, modified in the last 30 days | `find + sort + head` | **389 ms** | **648 B** |
| | Nushell | 1,315 ms | 1,060 B |
| Five processes using the most memory | `ps + awk` | **22 ms** | **113 B** |
| | Nushell | 233 ms | 366 B |
| Containers grouped by image | `docker + sort + uniq` | **19 ms** | **339 B** |
| | Nushell | 40 ms | 603 B |
| Context from `docker ps -a` | Unreduced | **17 ms** | 3,353 B |
| | Aggregated in Nushell | 39 ms | **566 B** |
{: tabindex="0" aria-label="Frozen pipeline microbenchmark"}

<figure>
  <iframe src="/assets/visores/structured-shell/index.html?lang=en"
          title="Interactive viewer for the Nushell benchmark corpus"
          loading="eager"
          style="width:100%;height:clamp(470px,78vw,660px);border:1px solid #2a3041;border-radius:6px"></iframe>
  <figcaption style="font-size:.85em;opacity:.75;margin-top:.4em">
    The analysis ran in R. The viewer renders precomputed data from the frozen corpus and does not query the reader's machine.
  </figcaption>
</figure>

The result was uncomfortable, as useful measurements often are: **Nushell was slower on every timed task**. It did not always reduce context either. The advantage appeared only when there was real aggregation: the container summary fell from 3,353 to 566 bytes, about 83%.

The potential gain was semantic. Comparing sizes or dates as typed values leaves fewer implicit assumptions than manufacturing text columns and deciding how to sort them. But the microbenchmark measured pipelines I had written. I still needed to observe the agent.

### Second level: agent against agent

The tuned corpus used five task families in Spanish: three where the policy favoured Nushell and two where it should avoid it. Each family was repeated ten times per arm: **100 runs**. The agent was headless Claude Code using a model from the Sonnet family; ground truth was recomputed before every run, and the command came from the transcript rather than the agent's account of what it had done.

| Subset | Arm | Correct | Activation | Median time | Median tokens |
|---|---|---:|---:|---:|---:|
| Positive | Without *skill* | 23/30 | 0/30 | **6,239 ms** | **152** |
| Positive | With *skill* | **30/30** | **28/30** | 9,537 ms | 368 |
| Negative | Without *skill* | 20/20 | 0/20 | 5,220 ms | 91 |
| Negative | With *skill* | 20/20 | **0/20** | 5,107 ms | 99 |
{: tabindex="0" aria-label="A/B results from the tuned corpus"}

On positive tasks, observed accuracy rose from 23/30 to 30/30. If the 60 runs are treated as independent observations, Fisher's exact test gives *p* = 0.0105.[^r-fisher] That assumption is not defensible for generalisation: the substantive unit is the task family, and there were only three positive families, all reused during tuning. I therefore report the value as an **exploratory description of the tuned corpus**, not as confirmation at the 5% level.

The exact Clopper–Pearson interval (a range compatible with a binomial proportion) was [88.4%; 100%] for 30/30 and [57.7%; 90.1%] for 23/30.[^clopper-1934][^r-binom] Median time increased 1.53× and median output tokens increased 2.43×: **higher accuracy on that corpus, at a cost**. I estimated the medians and their uncertainty by *bootstrap* (resampling the observations to construct intervals).[^efron-1993]

The task that separated the arms most strongly asked for the three files larger than 1 MB modified during the previous 30 days. Without the *skill*, the agent succeeded 3/10 times; with it, 10/10. The recurring failure used `fd -I`: that option ignores exclusion rules, but does not include hidden files on its own; that requires `-H -I` or `-u`.[^fd]

The transcript also exposed a `stdin` (standard input) trap. Bash piped into `nu -c`, which returned `null` with exit code 0, and the agent entered a 77-second search. The documentation requires `--stdin` for that route.[^nushell-stdin] After the correction, that case fell from 70,901 to 7,852 ms and from 3,287 to 303 tokens. This is a causal observation for that task, not a general estimator.

---

## Counter-tests before the verdict

### The holdout that corrected the story

The earlier corpus was both tuned and evaluated on the same five families. I also expanded the sample after seeing preliminary results. To test what survived outside that set, I froze the *skill* description and wrote five held-out tasks (*holdout*: cases kept out of tuning), three positive and two negative. Five repetitions per arm produced **50 runs**.

| Held-out subset | Arm | Correct | Activation | Median time | Median tokens |
|---|---|---:|---:|---:|---:|
| Positive | Without *skill* | 10/15 | 0/15 | **6,449 ms** | **178** |
| Positive | With *skill* | **14/15** | **4/15** | 8,019 ms | 282 |
| Negative | Without *skill* | **6/10** | 0/10 | **5,227 ms** | **143** |
| Negative | With *skill* | 5/10 | 0/10 | 5,476 ms | 160 |
{: tabindex="0" aria-label="Results from the later holdout"}

All four positive activations occurred in one family, at 4/5. The other two achieved 5/5 correct answers without activating the *skill*. The holdout is small, and its negative tasks produced weak results in both arms. It does not prove a general advantage or show that the *skill* harms negative tasks. It does refute one concrete extrapolation: **28/30 described the tuned corpus, not the integration in general**.

### A real aggregate case from my thesis

The second counter-test reused the governed temporal audit from a reconstruction of my master's thesis, but only as a *fixture* (a small, frozen dataset used to test a contract) of public aggregates: a source with 306,768 rows and 263 columns summarised into 21 annual rows, with no microdata or identifiers. The source hash, invariants, export process, and results are available in the [reproducible case package](https://github.com/tatanlabra/3cucharadas/tree/main/research/structured-shell-thesis-case).

The control arm was forbidden from using Nu; the frozen policy required it only for the two structured tasks. With Codex in read-only mode and low reasoning effort, three tasks across two arms and five repetitions produced **30 observations**:

- R1 requested a ranking of valid aggregates;
- R2 received the same corrupted *fixture* and had to block the ranking;
- R3 asked whether `presence=0` proved institutional closure and had to answer that the claim was out of scope.

| Task | Without Nu | Nu policy | Strict reading |
|---|---:|---:|---|
| R1 · valid ranking | 5/5; Nu 0/5; 30.6 s; 445 tokens | 5/5; Nu 5/5; 42.0 s; 580 tokens | The policy activated the route but did not improve accuracy. |
| R2 · corrupted *fixture* | 5/5; Nu 0/5; 31.4 s; 358 tokens | 5/5; Nu 5/5; 32.0 s; 410 tokens | Both blocked the ranking; the expected activation occurred 5/5 times. |
| R3 · epistemic boundary | 5/5; Nu 0/5; 15.0 s; 88 tokens | 5/5; Nu 0/5; 11.4 s; 62 tokens | The policy did not route a conceptual question through Nu. |
{: tabindex="0" aria-label="Real aggregate thesis case, A/B with Codex"}

Both arms achieved 5/5 on all three tasks. The case demonstrates policy conformity—Nu in 10/10 structured observations and 0/5 conceptual observations within that arm—but **no difference in accuracy**. I did not calculate a *p*-value: five repetitions of the same case are not five independent problem types. Nor does this alter the boundary of the data: `presence=0` does not prove institutional closure.

### A verdict for each outcome

| Outcome | Where it appears | Defensible interpretation |
|---|---|---|
| Improvement | Tuned corpus: 30/30 versus 23/30; holdout: 14/15 versus 10/15 | Some task families show an accuracy signal, but not a generalisable rate. |
| Regression | Microbenchmark, tuned corpus, and holdout | The structured route added latency and, in the agent experiments, more tokens. |
| No material difference | Real aggregate case and tasks that did not activate the *skill* | Changing the route did not improve accuracy when both arms already satisfied the contract. |
{: tabindex="0" aria-label="Verdict on improvement, regression, and no material difference"}

This is the rule I kept after measuring:

> **Nushell is worth testing when a query combines structured data, several transformations, and a concrete risk of silent failure.** For a native operation, a single transformation, or analysis at larger scale, a simpler or more appropriate tool usually exists.

I do not want to make it my primary shell or tell the agent to use it “whenever possible.” The objective is the opposite: **it should be able to justify both entering and avoiding that route**.

I also see no reason yet to turn this route into an MCP server. A query would merit promotion to a dedicated tool if it recurred, had a stable interface, accepted typed parameters, could be reused across agents, and measurably improved safety or observability. These cases do not yet meet all those conditions.

## Closing — A shell is not a religion

The result is not that Nushell wins. It improved accuracy on the tuned corpus; it added time in the microbenchmark and agent experiments, plus output tokens in the latter; and it did not change correctness in the real aggregate case. The reasonable decision depends on the task and on the cost of being wrong.

The most interesting finding was not Nushell either. It was discovering that a *skill* might never activate, that a rule about hidden files might be incomplete, and that a pipeline could return `null` with apparent success. The benchmark ended up testing both the tool and my assumptions.

There are probably better routes. If you use Nushell, DuckDB, `jq`, Python, MCP, *skills*, or another strategy that gives an agent a concrete advantage, I would like to know **what problem it solves, what baseline you compared it against, and how you verified that it actually improved the workflow**. Rather than collecting tools, we should start collecting evidence about when they are worth using and what they measurably improve.

## References and notes

> **Conflicts of interest and provenance.** The `penta-agent` metrics and the thesis case were produced by the same project that implemented the *skill*. The Nushell documentation also comes from the tool's developers. I use it to document the declared contract and behaviour, not as independent evidence of superiority.
{: .notice--info}

[^greenberg-2020]: Greenberg, Michael, and Austin J. Blatt. 2020. “Executable Formal Semantics for the POSIX Shell.” *Proceedings of the ACM on Programming Languages* 4 (POPL), article 43, 1–30. <https://doi.org/10.1145/3371111>.

[^nushell]: Nushell. n.d. “Nushell: A New Type of Shell.” Accessed September 5, 2026. <https://www.nushell.sh/>.

[^r-fisher]: R Core Team. n.d. “Fisher's Exact Test for Count Data.” *R Documentation*. Accessed September 5, 2026. <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/fisher.test.html>.

[^clopper-1934]: Clopper, C. J., and E. S. Pearson. 1934. “The Use of Confidence or Fiducial Limits Illustrated in the Case of the Binomial.” *Biometrika* 26, no. 4: 404–413. <https://doi.org/10.1093/biomet/26.4.404>.

[^r-binom]: R Core Team. n.d. “Exact Binomial Test.” *R Documentation*. Accessed September 5, 2026. <https://stat.ethz.ch/R-manual/R-devel/library/stats/html/binom.test.html>.

[^efron-1993]: Efron, Bradley, and Robert J. Tibshirani. 1993. *An Introduction to the Bootstrap*. New York: Chapman & Hall. <https://www.routledge.com/An-Introduction-to-the-Bootstrap/Efron-Tibshirani/p/book/9780412042317>.

[^fd]: sharkdp. n.d. “fd: A Simple, Fast and User-Friendly Alternative to `find`.” GitHub repository. Accessed September 5, 2026. <https://github.com/sharkdp/fd>.

[^nushell-stdin]: Nushell. n.d. “Scripts.” *The Nushell Book*. Accessed September 5, 2026. <https://www.nushell.sh/book/scripts.html>.
