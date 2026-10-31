---
title: "Multi-agent work in three spoonfuls (part IV): from a terminal trident to an autopoietic loop"
published: false
description: "Why a standalone LLM lacks re-entry and internal resistance (Zönnchen et al. 2025), and how I built a governed autopoiesis loop in penta-agent with 70 ms hybrid memory and Harness2."
tags: ai, agents, linux, architecture
canonical_url: https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/
---

After benchmarking models in Part I, auditing retrieval in Part II, and tracing provenance in Part III of this series, I had three CLI agents—Claude Code, Codex CLI, and Gemini CLI / Antigravity—running in my Arch Linux terminal (`kitty` + `tmux`). Yet months of daily work inside [`penta-agent`](https://github.com/tatanlabra/penta-agent) exposed a structural limit: **having three agents talking does not equal having a system that learns**.

In a recent systems-theory paper, Benedikt Zönnchen, Mariya Dzhimova, and Gudrun Socher ([2025](https://doi.org/10.3389/fcomm.2025.1585321)) build on Humberto Maturana and Francisco Varela ([1987 [1984]](https://search.worldcat.org/title/12314331)), Niklas Luhmann ([1995](https://search.worldcat.org/title/31436404), [1998](https://search.worldcat.org/title/37906965)), and George Spencer-Brown ([1969](https://archive.org/details/lawsofform00spen)) to show why a standalone LLM cannot be an autopoietic, sense-making system: it lacks *re-entry* and **internal resistance** against error. To improve without degrading, the probabilistic model must be wrapped in a deterministic socio-technical harness with strict `work / fail` boundaries.

## 1. Two negative benchmarks before adding complexity

Before building the autopoietic loop, I audited two components that sounded attractive on paper:
- **Purging unused local weights:** Over `60` days of telemetry, heavy local coder and reasoning models had `0` real routing invocations. Only `Qwen3-Embedding-0.6B` earned its keep.
- **Why regex beat an ONNX neural classifier:** I benchmarked a quantized local neural classifier against deterministic lexical rules in `triage.py`. Deterministic lexical rules achieved perfect accuracy on our golden benchmark in sub-millisecond time while the neural classifier missed edge cases and ran dozens of times slower.

## 2. Three layers of governed autopoiesis

1. **Spoonful 1 — Governance in `kitty` + `tmux`:** `quota-guard` routes tasks by real quota pressure, `decision-gate` structures material trade-offs, and `plan-board` enforces falsifiable verification before closing any task.
2. **Spoonful 2 — `70 ms` hybrid memory + modular skills + `7` MCP servers:** `experience-memory` couples SQLite FTS5 with Qdrant dense vectors (`Qwen3-Embedding-0.6B`) in `70 ms`.
3. **Spoonful 3 — Zero-token local autopoiesis with `Harness²` ([Xu et al. 2026](https://github.com/google-research/harness2)):** Adapted in offline shadow mode (`model_calls = 0`, no `--dangerously-skip-permissions`) across `9` seed cases in `3` domains (`routing`, `memory`, `skills`) and `82` deterministic tests. When a candidate patch introduces a regression, internal resistance discards it automatically before human promotion.

Read the full interactive article (with terminal videos, D2 diagrams, and full references) at the canonical URL:
https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/
