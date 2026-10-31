---
layout: single
classes:
  - post-editorial-hero-v2
  - post3-evidence
title: "Multi-agent work in three spoonfuls (part IV): from a terminal trident to an autopoietic loop"
subtitle: "Agent governance, 70-millisecond hybrid memory, and a local laboratory that rehearses its own improvements without burning quota"
description: "Fourth entry in the penta-agent multi-agent series: quota-governed routing, 70 ms hybrid memory, MCP tools, and a zero-token local autopoiesis loop in Harness2."
excerpt: "In part III I built a trident of agents in the terminal; months later I realized that coordinating calls is not enough if the system forgets, burns quota blindly, or breaks in silence. Here I show how I moved to a governed autopoietic architecture and why a standalone language model could never achieve it on its own."
date: 2026-10-31 12:00:00 -0300
last_modified_at: 2026-10-31 18:30:00 -0300
author: clabra
author_profile: true
comments: true
published: true
math: false
lang: en
ref: multiagente-penta-agent-autopoiesis-parte-iv
permalink: /ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/
categories: [ai, productivity, development, multi-agent]
tags: [ai, agents, cli, automation, linux, architecture, memory, autopoiesis]
distribution:
  social: true
  republish: [dev, medium]
repo: https://github.com/tatanlabra/penta-agent
entorno: "Arch Linux, KDE Plasma, kitty + tmux + Starship, local services (Qdrant + FTS5 + Qwen3-Embedding-0.6B), and the deterministic Harness2 laboratory"
en_abstract: >
  Fourth entry in the penta-agent multi-agent series. Having three CLI agents
  talking in the terminal does not produce a system that learns: without
  governed memory, quota-aware routing, and falsifiable verification gates, each
  new session repeats past failures or burns quota blindly. Drawing on systems
  theory and autopoiesis (Maturana and Varela 1987; Luhmann 1995, 1998;
  Spencer-Brown 1969; Esposito 2017, 2024; Zönnchen, Dzhimova, and Socher 2025),
  this post shows why a standalone large language model lacks genuine re-entry
  and internal resistance, and how an engineered socio-technical harness supplies
  both across three layers: quota-governed agent routing with a live plan-board
  in kitty and tmux; a 70 ms hybrid memory coupling SQLite FTS5 with Qdrant
  dense vectors alongside modular skills and MCP servers; and a zero-token
  autopoiesis loop in Harness2 that converts real friction signals into holdout
  cases and rejects regressive candidates before human promotion.
toc: true
toc_sticky: true
visual_id: multiagente-penta-agent-autopoiesis-parte-iv
visual_ref: multiagente-penta-agent-autopoiesis-parte-iv
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
header:
  overlay_image: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/teaser-1280x720.webp
  teaser_mobile: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/teaser-mobile-640x360.webp
  og_image: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/og-1200x630.webp
  og_image_alt: "Network sphere with three agent nodes inside a Harness2 orbital ring that halts a regressive pulse at an internal resistance threshold while feeding the verified flow back into the structure."
---

After benchmarking the models in [part I]({{ '/ia/productividad/desarrollo/multiagente-penta-agent-modelos/' | relative_url }}), auditing retrieval in [part II]({{ '/ia/productividad/desarrollo/multiagente-penta-agent-memoria/' | relative_url }}), and tracing provenance in [part III of this series]({{ '/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/' | relative_url }}), I closed my laptop with a sense of victory: I had a trident of agents running from the terminal on Arch Linux. With a couple of `zsh` aliases, I could invoke [Claude Code](https://github.com/anthropics/claude-code) for architectural reasoning, hand off a task to [Codex CLI](https://github.com/openai/codex) to edit code, or ask [Gemini CLI](https://github.com/google-gemini/gemini-cli) and Antigravity for a quick second opinion. On paper, orchestration looked solved.
{: .text-justify}

Yet after using that setup every day on real projects inside [`penta-agent`](https://github.com/tatanlabra/penta-agent), I hit a silent wall: **having three agents talking does not equal having a system that learns**. Every time I opened a fresh session, the trident suffered from partial amnesia, repeated commands that had already failed the previous week, burned the quota of the most expensive provider on routine tasks, or marked tests as "verified" when they had never had a chance to fail.
{: .text-justify}

To understand what was missing, it helped to change the question. In a recent systems-theory analysis of artificial intelligence, Benedikt Zönnchen, Mariya Dzhimova, and Gudrun Socher (2025[^zonnchen2025], 2–4) propose setting aside whether a language model "thinks like a human" and asking instead the question posed by Humberto Maturana and Francisco Varela (1987[^maturana1987] [1984]) and extended by Niklas Luhmann (1998[^luhmann1998], 60–69): **can the system draw its own boundary with the environment, observe its own failures, and sustain itself through its own operations?** In other words, moving from the vague notion of "intelligence" to the concrete mechanism of **autopoiesis**.
{: .text-justify}

As Zönnchen, Dzhimova, and Socher (2025[^zonnchen2025], 8–10) show, an isolated language model in a chat window **neither is nor can be an autopoietic, sense-making system**: it lacks what George Spencer-Brown (1969[^spencerbrown1969]) called *re-entry*—the capacity to re-introduce the distinction between system and environment (self-reference vs. other-reference) inside its own operations—because it only computes which token is statistically plausible after another, without internal resistance against error. If I want a system that improves without degrading, I have to build a **socio-technical harness** around the models that couples the probabilistic flexibility of neural networks with the strict coupling and binary code (`works / does not work`, `work / fail`) of deterministic technology described by Luhmann (1998[^luhmann1998], 517–525) and André Reichel (2011[^reichel2011], 105–118).
{: .text-justify}

### The starting point: what I measured and discarded before making this leap

Before diving into the three spoonfuls of this fourth installment, here is the experiment that forced me to adopt that discipline. When I tried to give the system long-term memory, the obvious temptation was to install the most elaborate architecture available: temporal graphs, heavy extractors, or an `8B`-parameter neural judge running on CPU. Instead of following intuition, I built a reproducible benchmark over my real work logs—comparing open alternatives such as [GraphRAG](https://github.com/microsoft/graphrag), [Graphiti](https://github.com/getzep/graphiti), [Hindsight](https://github.com/vectorize-io/hindsight), [Letta](https://github.com/letta-ai/letta), [Mem0](https://github.com/mem0ai/mem0), and [deja-vu](https://github.com/vshulcz/deja-vu)—and set a falsification contract upfront: any candidate exceeding `0.10 s` in `p95` latency or failing to improve recall by at least `10%` would be discarded.
{: .text-justify}

| What I tested in the laboratory | Measured result | Operational decision |
|---|---|---|
| **Hybrid memory (`v3.1`)** (`FTS5` lexical index + semantic neighbors in [Qdrant](https://github.com/qdrant/qdrant) with [`Qwen3-Embedding-0.6B`](https://github.com/QwenLM/Qwen3-Embedding)) | Latency `p95 = 0.07 s` (`< 0.10 s`), `96%` overall recall, rescuing `1 in 3` zero-lexical-overlap queries | **Promoted to production** as the engine behind `experience-memory` and `recall-context` |
| **In-memory relational graph (`v3.2`)** for multi-hop entity expansion | Exact tie in accuracy with `v3.1`, but nearly double the latency (`p95 = 0.13 s > 0.10 s`) | **Frozen in the lab**; the extra complexity did not earn its keep |
| **CPU neural judges (`4B` and `8B`)** for live answer auditing | Between `69 s` and `197 s` per verdict, hitting `180 s` timeouts in `2` of `3` runs | **Discarded from the critical path**; pruned `36.3 GiB` from disk |
| **Deterministic checks + bounded `0.6B` judge** for local validation | Millisecond latency, `0` remote calls, and `100%` reproducibility | **Adopted as the standard** for control gates and evaluation |

**Table 1.** Summary of the prior local memory and evaluation laboratory in [`penta-agent`](https://github.com/tatanlabra/penta-agent): what survived the `0.10 s` threshold and why I pruned `36.3 GiB` of local models that added no operational value.
{: .text-justify}

With that foundation in place, I organized this fourth part into three progressive spoonfuls: in the **first**, I show how I moved from launching standalone agents by hand to governing them with quota budgets, auditable bridges, and a live board in [`kitty`](https://github.com/kovidgoyal/kitty) and [`tmux`](https://github.com/tmux/tmux); in the **second**, how the nervous system of hybrid memory, [MCP](https://github.com/modelcontextprotocol/servers) tools, and [skills](https://github.com/anthropics/skills) works under the hood; and in the **third**, how I closed the local autopoiesis loop with `Harness2` and where both my metrics and systems theory draw the boundary today.
{: .text-justify}

---

## Spoonful 1: From invoking agents by hand to governing agents and models

In plain terms: when I first wired the three agents together, I acted like a traffic officer waving my arms in the middle of an intersection. If I wanted [Codex CLI](https://github.com/openai/codex) to review a patch written by [Claude Code](https://github.com/anthropics/claude-code), I copied file paths, opened another tab, and hoped for the best. That works for a five-minute demo, but it falls apart when a task runs for two hours and touches twenty files.
{: .text-justify}

### Quota-aware routing and security boundaries

My first **deductive** inference came from a hard constraint: model subscriptions and APIs have usage limits, different context windows, and credential boundaries that must never blur. By definition, if I delegate a heavy task to an agent whose quota is at `98%`, the session will die mid-flight and leave the repository in an inconsistent state.
{: .text-justify}

So I replaced intuitive provider selection with an explicit policy in `routing.yaml` and a pre-flight sentinel (`quota_status.sh`, governed by the `quota-guard` skill). Before launching any expensive job, the system reads cached pressure across every lane without spending tokens:
{: .text-justify}

- **🔍 [Claude Code](https://github.com/anthropics/claude-code) (`Opus` / `Sonnet`):** handles architectural design, delicate editing, and long-horizon synthesis when its quota is clear (`exit 0`).
- **🛠️ [Codex CLI](https://github.com/openai/codex) (`gpt-5.4`):** steps in as an implementation peer, deep refactoring engine, session rescuer (`codex-rescue`), and cross-validator.
- **🌐 [Gemini CLI](https://github.com/google-gemini/gemini-cli) and Antigravity (`gemini-3-pro` / `flash`):** in a direct session (`penta-agy`) it acts as the primary integrator; when invoked from outside via `agy-bridge`, it runs inside a strict sandbox over sanitized public context as an explorer, reviewer, or validator, never inheriting private keys or `.env` files.

Instead of calling a raw binary and depending on whatever it prints to stdout, every cross-agent handoff goes through `agy-bridge`. The bridge requires declaring who is calling (`--caller`), in what mode (`plan`, `review`, `patch`, `test`, or `explain`), and with what time limit (`--timeout`), leaving an immutable receipt in `.agents/runs/<run_id>/` with `request.md`, `result.md`, `status.json`, and `diff.patch`.
{: .text-justify}

### The live board (`plan-board`) and decision gates

My second inference was **inductive**: reviewing dozens of past sessions showed that the biggest waste of time happened at two extremes. Either an agent interrupted me every two minutes to ask permission for trivial, reversible steps, or it silently made a delicate architectural choice and I only discovered at the end that it had gone down the wrong path.
{: .text-justify}

To eliminate both extremes without filling this post with abstract flowcharts, here is how my actual [`kitty`](https://github.com/kovidgoyal/kitty) terminal—or minimalist Wayland alternatives like [`foot` on Codeberg](https://codeberg.org/dnkl/foot)—looks today when split into two panes with [`tmux`](https://github.com/tmux/tmux) during a live task:
{: .text-justify}

<figure class="align-center" style="width: 100%;">
  <video width="1280" height="800" style="width: 100%; height: auto; border-radius: 12px; display: block; cursor: pointer;" autoplay loop muted playsinline preload="metadata" onclick="this.paused ? this.play() : this.pause()" title="Click or tap to pause or resume the terminal" poster="{{ '/assets/images/multiagente-penta-agent-autopoiesis/kitty-tmux-plan-board-poster-1280x800.webp' | relative_url }}" aria-label="Demonstration in a Kitty terminal split with tmux where the top pane runs multi-agent delegation, passes through a decision-gate, and validates a falsifiable gate, while the bottom pane updates the plan-board live until closing 4 of 4 steps.">
    <source src="{{ '/assets/videos/kitty-tmux-plan-board-1280x800.webm' | relative_url }}" type="video/webm">
    Your browser does not support WebM video. You can <a href="{{ '/assets/videos/kitty-tmux-plan-board-1280x800.webm' | relative_url }}">open the demonstration directly</a>.
  </video>
  <figcaption><strong>Figure 1.</strong> Daily workflow in my <a href="https://github.com/kovidgoyal/kitty"><code>kitty</code></a> + <a href="https://github.com/tmux/tmux"><code>tmux</code></a> terminal with the <a href="https://github.com/starship/starship"><code>Starship</code></a> prompt: the top pane runs multi-agent delegation via <code>agy-bridge</code>, the <code>decision-gate</code> brake, and <code>pytest</code>; the bottom pane (<code>watch.mjs</code>) updates each step live (<code>[ ]</code> &rarr; <code>[~]</code> &rarr; <code>[!]</code> &rarr; <code>[x]</code>), along with binding decisions and drift.</figcaption>
</figure>

What appears in the bottom pane of **Figure 1** is the contract that changed how I work:
{: .text-justify}

1. **Local autonomy with visual traceability (`plan-board`):** every reversible, in-scope step proceeds without asking permission, but must be reflected in real time in the bottom table. And no item can be closed as verified (`[x]`) unless the agent attaches the concrete test, command, or observation reference that backs it.
2. **Decision gate (`decision-gate`):** when an irreversible or architectural fork appears (state `[!]`), the agent halts only that branch and presents the question with the **recommended option first**, marked `(Recommended)` and justified with deductive, inductive, and abductive evidence.
3. **A gate that has never been seen red is not a gate (`gates-falsables`):** before accepting any new verifier, I require running it against a synthetic failure (`--fixture`) and proving that it returns a non-zero exit code (`exit 1`). If a check passes even when I break its input on purpose, it is not a safety net—it is compliance theater.

---

## Spoonful 2: The nervous system — hybrid memory, skills, and MCP tools

If the first spoonful orders who does what and under which rules, the second solves how the system remembers what it has already learned and how it picks the exact tool without bloating the context window.
{: .text-justify}

Here the diagnosis by Zönnchen, Dzhimova, and Socher (2025[^zonnchen2025], 6–7, 9) is decisive again: a neural network maintains a **loose coupling** with human communication that behaves like a *"contingent index-card system (Zettelkasten)"* (pp. 7, 9) of semantic associations in vector space, giving rise to what Elena Esposito (2017[^esposito2017], 249–265; 2022[^esposito2022]) calls *"virtual double contingency"* and *"artificial communication."* That flexibility lets it connect ideas phrased in very different words, but also makes its outputs inherently probabilistic and devoid of autonomous decision-making. If I want reliable memory and precise execution, I have to couple that vector *Zettelkasten* with exact indices and deterministic scripts.
{: .text-justify}

### Experience memory (`experience-memory`): the hybrid *Zettelkasten* in `0.07 s`

When I first started keeping logs, my memory was essentially a folder of Markdown files that I read or searched with [`ripgrep`](https://github.com/BurntSushi/ripgrep). The obvious problem is that if a month ago I solved a cold-boot screen freeze under the title `"Webview failure on autostart"` and today I search for `"Panel fails to load at login"`, a purely lexical search can miss it entirely, whereas a purely vector search can bury the exact name of a script like `verify_boot_contract.sh`.
{: .text-justify}

The solution I validated in **Table 1** combines both worlds behind the `experience-memory` [MCP](https://github.com/modelcontextprotocol/servers) server and the `recall-context` skill:
{: .text-justify}

- **Exact lexical lane (`SQLite FTS5`):** instantly catches flag names, error codes, file paths, and invariants (`INV-005`).
- **Dense semantic lane ([Qdrant](https://github.com/qdrant/qdrant) + [`Qwen3-Embedding-0.6B`](https://github.com/QwenLM/Qwen3-Embedding)):** indexes architectural decisions, handoffs, and operational lessons (`penta_context_v2`) to retrieve conceptual neighbors even when they share zero keywords.

Before designing any non-trivial strategy, the agent queries `recall_experience` in `70 milliseconds` (`p95 = 0.07 s`). That is how it discovers which command worked previously, which hypothesis was already refuted, and which environment trap to avoid (for instance, knowing that in my shell `cp`, `mv`, and `rm` are aliased to interactive `-i`, which hangs a headless process unless invoked via `command mv -f`).
{: .text-justify}

### Skills as living procedures and proactive MCP selection

To avoid saturating the initial prompt with thousands of lines of instructions, I adopted the modular pattern of [Anthropic Skills](https://github.com/anthropics/skills) enriched with local contracts. In [`penta-agent`](https://github.com/tatanlabra/penta-agent), each skill is a self-contained package with four parts: a concise contract in `SKILL.md` defining when to activate and **when not to use it**; on-demand deep documentation in `references/` (such as the editorial corpus extracted with [Docling](https://github.com/docling-project/docling) or diagramming rules with [D2](https://github.com/terrastruct/d2)); deterministic executables in `scripts/` (such as typed pipelines in [Nushell](https://github.com/nushell/nushell), visual automation with [Playwright](https://github.com/microsoft/playwright), or forge integration via [`glab` on GitLab](https://gitlab.com/gitlab-org/cli)); and a telemetry trail.
{: .text-justify}

Similarly, the fleet of [MCP](https://github.com/modelcontextprotocol/servers) servers (`plan-board`, `experience-memory`, `ideas-rag`, `paper-search`, `bibliography-apa`, `PLAYWRIGHT_LOCAL`) is cataloged in `specs/mcp-capabilities.json`. When a task arrives, triage evaluates which capabilities provide real evidence and records both hits and justified abstentions. And when I found that two older servers (quota status and remote SSH infrastructure) were faster, clearer, and easier to audit as direct scripts (`quota_status.sh` and `remote_exec.sh`), I decommissioned them as MCP servers and turned them into lightweight skills. Fewer resident daemons mean a smaller failure surface.
{: .text-justify}

---

## Spoonful 3: The autopoiesis loop (`Harness2`) — how the system rehearses its own improvements

Here I reach the core of this fourth installment. Having capable agents (Spoonful 1) and fast hybrid memory with skills (Spoonful 2) still leaves a critical question open: **what happens when a delegation route ages, a skill starts inducing errors, or a memory tweak degrades accuracy on edge cases?** If I rely solely on noticing by eye weeks later, the system degrades through silent drift.
{: .text-justify}

### Why a standalone LLM lacks *re-entry* and internal resistance

In their study on autopoiesis and artificial intelligence, Zönnchen, Dzhimova, and Socher (2025[^zonnchen2025], 8–9) explain with surgical precision why asking a model to "reflect on its own errors" via *chain-of-thought* (`CoT`) is not enough. When a model generates intermediate tokens like *"Is this step correct?"*, it exhibits only rudimentary **processual self-referentiality** (p. 8)—producing the most statistically plausible continuation inside its training distribution—while lacking **reflective self-reference** and genuine *re-entry* (Spencer-Brown 1969[^spencerbrown1969]). If a model takes itself as its sole reference without external contrast, it quickly falls into infinite recursion or collapse; if it depends entirely on a human retraining its weights from outside (`RLHF` or delayed fine-tuning), it remains an *allopoietic* artifact determined from the outside (Zönnchen, Dzhimova, and Socher 2025[^zonnchen2025], 4, 8–9).
{: .text-justify}

To escape that trap, Zönnchen, Dzhimova, and Socher (2025[^zonnchen2025], 7) recover a decisive formulation from Niklas Luhmann (1995[^luhmann1995]) on how operational constructivism relocates Kant's "resistance of reality" inside a system:
{: .text-justify}

> "I think we should not abandon [Kant's] idea of resistance, but we should relocate it into the system. It is the result of resolving an internal conflict—the result of the system's operations resisting the operations of the same system" (Luhmann 1995[^luhmann1995], quoted in Zönnchen, Dzhimova, and Socher 2025[^zonnchen2025], 7).

That sentence describes, piece by piece, what I built in [`penta-agent`](https://github.com/tatanlabra/penta-agent) by adapting and integrating the proactive loop of [**`Harness²`**](https://github.com/google-research/harness2) proposed by Ruiyao Xu, Yanfei Chen, Zhongying CuiZhu, et al. (2026[^xu2026]): making **the system's own deterministic verification operations resist and filter change proposals generated from its own operational friction**.
{: .text-justify}

<details markdown="1">
<summary><strong>In plain terms (ELI5): what is Google's original Harness² and how did I adapt it to my machine?</strong></summary>

Imagine your AI agents are very creative chefs, but the recipe book they follow (their rules, memory, and tools) sometimes has confusing steps that make them burn the rice. The [original `Harness²` from Google Research](https://github.com/google-research/harness2) (Xu et al. 2026[^xu2026]) proposes a clever loop called *Propose–Probe–Compose*: instead of swapping out the chef's brain, it puts several assistants to work rewriting the recipe book, asks them to cook test dishes in the cloud, and keeps the winning recipe. For my daily workflow, the factory setup had two catches: it is designed to burn hundreds of paid cloud model calls (`Vertex AI`), and when driving CLI agents it unbuckles their seatbelt (`--dangerously-bypass-approvals-and-sandbox`) with open internet access.
{: .text-justify}

To adapt it to [`penta-agent`](https://github.com/tatanlabra/penta-agent) without spending an extra cent or opening security holes, I took its recursive search engine (`commit 1cfe254e`) and locked it inside a "test kitchen" completely unplugged from the internet (`unshare -Urn`), with a disposable home folder and zero access to my API keys or model CLIs (`model_calls = 0`). Instead of running cloud benchmarks, my wrapper (`penta-harness2` and `local-cycle`) feeds that test kitchen with the real stumbles my agents suffered during the week (`CSI`), requires any recipe tweak to first fail the test when broken (red) and then pass every historical case without breaking anything else (green), and finally stages the winning recipe across all three agents (`Claude`, `Codex`, and `Gemini/Antigravity`) with a one-step undo button (`rollback-local`) in case I do not approve it.
{: .text-justify}

</details>

<figure class="d2-responsive" style="width: 100%;">
  <picture style="display: block; width: 100%;">
    <source media="(max-width: 640px)" srcset="{{ '/assets/images/multiagente-penta-agent-autopoiesis/circuito-autopoiesis-h2-mobile.svg' | relative_url }}" type="image/svg+xml">
    <img src="{{ '/assets/images/multiagente-penta-agent-autopoiesis/circuito-autopoiesis-h2.svg' | relative_url }}" width="1001" height="954" style="width: 100%; height: auto; display: block; border-radius: 12px;" alt="Diagram of the closed local autopoiesis loop in Penta Agent with Harness2: CSI friction signals feed the case generator and the local cycle across routing, memory, and skills; a deterministic judge evaluates against holdout cases with zero model calls, discarding regressions and keeping only verified improvements for human promotion.">
  </picture>
  <figcaption><strong>Figure 2.</strong> Governed autopoiesis loop in <code>penta-agent</code> + <code>Harness2</code>: relocating internal resistance (Luhmann 1995; Zönnchen, Dzhimova, and Socher 2025) through <code>holdout</code> evaluation with <code>model_calls = 0</code> prior to any human promotion.</figcaption>
</figure>

### How the closed loop operates across my three domains (`routing`, `memory`, `skills`)

As **Figure 2** shows (adapting into a three-column horizontal layout on desktop and a vertical flow on mobile), the loop operates in four strict stages:
{: .text-justify}

1. **Observing real friction (`CSI` — *Continuous Self-Improvement*):** while I use the system, a collector logs objective friction signals: a task that had to switch agents after a timeout, an `experience-memory` query that returned too few useful neighbors, or a skill where the user had to correct a command.
2. **Bridging evidence into reproducible cases (`--from-csi latest`):** the `local_cycle.py` module takes that friction report and automatically translates it into a test specification (`CaseSpec`) inside an isolated environment, without touching my active configuration.
3. **Internal resistance without spending tokens (`eval_harness` with `model_calls = 0`):** the harness runs the full suite (`--profile autopoiesis-all`, currently covering `9/9` baseline cases across `routing`, `memory`, and `skills`), enforcing two hard conditions: every control case (`holdout`) must pass (`holdout_passed = true`), and external API calls must equal zero (`model_calls = 0`).
4. **Auditable decision (`KEEP` vs. `DISCARD`) and human promotion:** if a candidate degrades even a single `holdout` case or fails to beat the baseline, the deterministic judge discards it (`DISCARD`). Only when it improves the score with zero regressions does it receive a `KEEP` verdict and leave a signed receipt for me to review before promoting it to the main repository.

So this does not remain a theoretical promise, the next mini-video shows `penta-harness2-shadow local-cycle --profile autopoiesis-all` running in my [`kitty`](https://github.com/kovidgoyal/kitty) + [`tmux`](https://github.com/tmux/tmux) terminal, including what happens when I inject a regressive candidate (`--fixture`) alongside a healthy improvement:
{: .text-justify}

<figure class="align-center" style="width: 100%;">
  <video width="1280" height="800" style="width: 100%; height: auto; border-radius: 12px; display: block; cursor: pointer;" autoplay loop muted playsinline preload="metadata" onclick="this.paused ? this.play() : this.pause()" title="Click or tap to pause or resume the terminal" poster="{{ '/assets/images/multiagente-penta-agent-autopoiesis/kitty-harness2-autopoiesis-poster-1280x800.webp' | relative_url }}" aria-label="Demonstration in a Kitty terminal split with tmux running penta-harness2-shadow local-cycle across 9 of 9 cases in routing, memory, and skills with zero model calls, applying internal resistance to discard a regressor and keep the healthy candidate.">
    <source src="{{ '/assets/videos/kitty-harness2-autopoiesis-1280x800.webm' | relative_url }}" type="video/webm">
    Your browser does not support WebM video. You can <a href="{{ '/assets/videos/kitty-harness2-autopoiesis-1280x800.webm' | relative_url }}">open the demonstration directly</a>.
  </video>
  <figcaption><strong>Figure 3.</strong> Execution in my <a href="https://github.com/kovidgoyal/kitty"><code>kitty</code></a> + <a href="https://github.com/tmux/tmux"><code>tmux</code></a> terminal of the local autopoiesis loop (<code>local-cycle --profile autopoiesis-all</code>): it evaluates all <code>9/9</code> cases in <code>routing</code>, <code>memory</code>, and <code>skills</code> with <code>model_calls = 0</code>, applies internal resistance to reject the regressor (<code>DISCARD</code>), and preserves the verified improvement (<code>KEEP +0.250</code>) with all <code>82</code> harness tests green.</figcaption>
</figure>

---

## Closing: what my architecture achieves today and where its limits lie

Looking back at the path from [part I]({{ '/ia/productividad/desarrollo/multiagente-penta-agent-modelos/' | relative_url }}), [part II]({{ '/ia/productividad/desarrollo/multiagente-penta-agent-memoria/' | relative_url }}), and [part III]({{ '/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/' | relative_url }}), the main difference is no longer which model writes the prettiest reply to an isolated prompt, but the structure that holds the whole system together when I am not watching every line.
{: .text-justify}

Following the rigorous distinction drawn by Zönnchen, Dzhimova, and Socher (2025[^zonnchen2025], 5, 9–10) and by Elena Esposito (2017[^esposito2017]; 2022[^esposito2022]; 2024[^esposito2024]), it would be an epistemic mistake to claim that a language model or a bundle of scripts has on its own achieved the biological autopoiesis of a living cell (Maturana and Varela 1987[^maturana1987] [1984]) or the reflective sense-making (*Sinn*) of human consciousness (Luhmann 1998[^luhmann1998], 50–69). As Zönnchen, Dzhimova, and Socher (2025[^zonnchen2025], 5, 10) caution when critiquing merely metaphorical invocations of technological autopoiesis, language models remain statistical engines that compute distributions without mental states of their own. Yet—and this is my engineering synthesis for the socio-technical system as a whole—when I couple their capacity for contingent variation with verified hybrid memory, strict delegation contracts, a binary internal-resistance harness (`work / fail`; Reichel 2011[^reichel2011]) that filters its own proposals before touching production, and deliberative human oversight, I obtain in practice a loop of **governed operational autopoiesis**.
{: .text-justify}

To close with full transparency, **Table 2** summarizes what is running and measured on my machine today, where the next step points, and under what objective condition I would discard each component if it stopped earning its keep:
{: .text-justify}

| System pillar | What it achieves today (verified in production) | What it aims to achieve next & falsification condition |
|---|---|---|
| **1. Agent and model routing** (`routing.yaml`, `quota-guard`, `agy-bridge`) | Routes tasks across [Claude Code](https://github.com/anthropics/claude-code), [Codex CLI](https://github.com/openai/codex), and [Gemini CLI](https://github.com/google-gemini/gemini-cli) / Antigravity based on cached quota pressure; isolates handoffs in `.agents/runs/` under a strict sandbox and displays live progress in `plan-board` (**Figure 1**). | **Goal:** reweight routing priorities from historical domain success rates.<br>**Discard if:** the bridge introduces spurious failures or bureaucratic latency exceeding quota savings. |
| **2. Hybrid memory** (`experience-memory`, [Qdrant](https://github.com/qdrant/qdrant) + `FTS5`) | Resolves lexical and semantic queries in `p95 = 0.07 s` (`< 0.10 s`), rescues `33%` of zero-keyword-overlap pairs, and saves `36.3 GiB` after pruning slow CPU judges (**Table 1**). | **Goal:** add automatic decay for obsolete lessons when a contract changes.<br>**Discard if:** `p95` latency exceeds `0.10 s` or semantic noise degrades top-3 precision. |
| **3. Skills and MCP governance** (`mcp-fleet`, `gates-falsables`) | Maintains declarative parity across agents (`24/24` checks green), measures MCP usage and abstention, and requires every new gate to fail first against a red canary (`--fixture -> exit 1`). | **Goal:** semi-automatic pruning of skills that accumulate repeated friction in `CSI` telemetry.<br>**Discard if:** maintaining a skill's contract takes longer than running the direct command. |
| **4. Local autopoiesis (`Harness2`)** (`local-cycle`, `eval_harness`) | Converts real `CSI` friction into reproducible `Cases` and evaluates candidates across `routing`, `memory`, and `skills` (`9/9` cases, `82/82` tests) with `model_calls = 0`, applying internal resistance (`KEEP` / `DISCARD`, **Figures 2 and 3**). | **Goal:** expand the bank of real cases extracted from failed sessions without losing millisecond evaluation.<br>**Hard boundary (`INV-004`):** blind *auto-merge* is forbidden; final promotion to production always requires human review. |

**Table 2.** Balance between verified production results in [`penta-agent`](https://github.com/tatanlabra/penta-agent) today, the design horizon, and the falsification thresholds that keep the system under human control.
{: .text-justify}

If building this fourth stage made one thing clear to me, it is that the maturity of a multi-agent system is not measured by how many new pieces I bolt onto it each week, but by how much unnecessary complexity I can prune and how many of its own mistakes the system can catch before asking for my help.
{: .text-justify}

---

## References

[^esposito2017]: Esposito, Elena. 2017. ["Artificial Communication? The Production of Contingency by Algorithms."](https://doi.org/10.1515/zfsoz-2017-1014) *Zeitschrift für Soziologie* 46 (4): 249–265. [Scholar](https://scholar.google.com/scholar_lookup?title=Artificial+Communication%3F+The+Production+of+Contingency+by+Algorithms&doi=10.1515%2Fzfsoz-2017-1014)

[^esposito2022]: Esposito, Elena. 2022. [*Artificial Communication: How Algorithms Produce Social Intelligence*](https://doi.org/10.7551/mitpress/14189.001.0001). Cambridge, MA: The MIT Press. [Scholar](https://scholar.google.com/scholar_lookup?title=Artificial+Communication&doi=10.7551%2Fmitpress%2F14189.001.0001)

[^esposito2024]: Esposito, Elena. 2024. *Kommunikation mit unverständlichen Maschinen*. Salzburg and Vienna: [Residenz Verlag](https://www.residenzverlag.com/buch/kommunikation-mit-unverstaendlichen-maschinen). [Review of *Kommunikation mit unverständlichen Maschinen*](https://www.merz-zeitschrift.de/article/download/2950/2744) by Eric Van der Beek in *merz \| medien + erziehung*: [DOI](https://doi.org/10.21240/merz/2024.4.20) · [Scholar](https://scholar.google.com/scholar_lookup?title=Esposito%2C+Elena+%282024%29.+Kommunikation+mit+unverst%C3%A4ndlichen+Maschinen+%28Unruhe+bewahren%29.+Wien%2C+Salzburg%3A+Residenz+Verlag%2C+96+S.%2C+20%2C00+%E2%82%AC.&doi=10.21240%2Fmerz%2F2024.4.20)

[^luhmann1995]: Luhmann, Niklas. 1995. "Systems Theory and Postmodernism." University lecture, London. Quoted in Zönnchen, Dzhimova, and Socher, [*From Intelligence to Autopoiesis*](https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2025.1585321/pdf) (2025, 7): [DOI](https://doi.org/10.3389/fcomm.2025.1585321) · [Scholar](https://scholar.google.com/scholar_lookup?title=From+intelligence+to+autopoiesis%3A+rethinking+artificial+intelligence+through+systems+theory&doi=10.3389%2Ffcomm.2025.1585321)

[^luhmann1998]: Luhmann, Niklas. 1998. [*Die Gesellschaft der Gesellschaft*](https://search.worldcat.org/title/37906965). Frankfurt am Main: Suhrkamp Verlag. <https://search.worldcat.org/title/37906965>.

[^maturana1987]: Maturana, Humberto R., and Francisco J. Varela. 1987 [1984]. [*El árbol del conocimiento: las bases biológicas del entendimiento humano*](https://search.worldcat.org/title/12314331). Santiago de Chile: Editorial Universitaria. 1st Chilean ed. 1984; 1987 international ed. cited in Zönnchen, Dzhimova, and Socher, [*From Intelligence to Autopoiesis*](https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2025.1585321/pdf) (2025, 3): [DOI](https://doi.org/10.3389/fcomm.2025.1585321) · [Scholar](https://scholar.google.com/scholar_lookup?title=From+intelligence+to+autopoiesis%3A+rethinking+artificial+intelligence+through+systems+theory&doi=10.3389%2Ffcomm.2025.1585321)

[^reichel2011]: Reichel, André. 2011. ["Technology as System: Towards an Autopoietic Theory of Technology."](https://doi.org/10.1504/IJISD.2011.043070) *International Journal of Innovation and Sustainable Development* 5 (2–3): 105–118. [Scholar](https://scholar.google.com/scholar_lookup?title=Technology+as+system%3A+towards+an+autopoietic+theory+of+technology&doi=10.1504%2FIJISD.2011.043070)

[^spencerbrown1969]: Spencer-Brown, George. 1969. [*Laws of Form*](https://archive.org/details/lawsofform00spen). London: Allen & Unwin. <https://archive.org/details/lawsofform00spen>.

[^xu2026]: Xu, Ruiyao, Yanfei Chen, Zhongying CuiZhu, Bhavana Dalvi Mishra, Yifei Ming, Han Yu, Rujun Han, Chen-Yu Lee, and Tomas Pfister. 2026. ["Harness²: Recursive Agent Harnessing for an Open World."](https://arxiv.org/pdf/2610.14224) *arXiv preprint* `arXiv:2610.14224` (open source at <https://github.com/google-research/harness2>). [arXiv](https://arxiv.org/abs/2610.14224) · [Scholar](https://scholar.google.com/scholar_lookup?title=Harness%5E2%3A+Recursive+Agent+Harnessing+for+an+Open+World)

[^zonnchen2025]: Zönnchen, Benedikt, Mariya Dzhimova, and Gudrun Socher. 2025. ["From Intelligence to Autopoiesis: Rethinking Artificial Intelligence through Systems Theory."](https://www.frontiersin.org/journals/communication/articles/10.3389/fcomm.2025.1585321/pdf) *Frontiers in Communication* 10:1585321. [DOI](https://doi.org/10.3389/fcomm.2025.1585321) · [Scholar](https://scholar.google.com/scholar_lookup?title=From+intelligence+to+autopoiesis%3A+rethinking+artificial+intelligence+through+systems+theory&doi=10.3389%2Ffcomm.2025.1585321)

<style>
.post3-evidence .page__content > p,
.post3-evidence .page__content > ul > li,
.post3-evidence .page__content > ol > li,
.post3-evidence .page__content blockquote p {
  text-align: justify;
  hyphens: auto;
}
@media (max-width: 47.99em) {
  .post3-evidence .tabla-desliza {
    overflow-x: visible;
  }
  .post3-evidence .tabla-desliza table,
  .post3-evidence .tabla-desliza[data-perfil="narrativa"] table {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    table-layout: fixed;
    font-size: 13.5px;
    line-height: 1.35;
  }
  .post3-evidence .tabla-desliza table :is(th, td) {
    padding: 0.42rem 0.32rem;
    overflow-wrap: anywhere;
    word-break: normal;
  }
  .post3-evidence .tabla-desliza table code {
    font-size: 0.85em;
    word-break: break-word;
  }
}
</style>
