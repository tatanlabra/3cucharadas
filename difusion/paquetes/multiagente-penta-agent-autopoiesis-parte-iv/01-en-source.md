# Source (EN) — Multi-agent work in three spoonfuls (part IV): from a terminal trident to an autopoietic loop

Canonical URL: https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/
Repository: https://github.com/tatanlabra/penta-agent

## Core summary

Having three CLI agents (Claude Code, Codex CLI, and Gemini CLI / Antigravity) collaborating in a terminal does not produce a system that learns: without governed memory, quota-aware routing, and falsifiable verification gates, each new session repeats past failures or burns quota blindly.

Drawing on systems theory and autopoiesis (Maturana and Varela 1987 [1984]; Luhmann 1995, 1998; Spencer-Brown 1969; Esposito 2017, 2024; Zönnchen, Dzhimova, and Socher 2025), this article explains why an isolated large language model lacks genuine *re-entry* and internal resistance against error, and how an engineered socio-technical harness supplies both across three layers:

1. **Spoonful 1 — Quota-governed routing (`quota-guard`), structured trade-off gates (`decision-gate`), and a live `plan-board` in `kitty` and `tmux`:**
   - Before adding new layers, two empirical negative results pruned complexity: purging dozens of gigabytes of unused local model weights (`0` real invocations over `60` days), and archiving a local ONNX neural prompt classifier after deterministic lexical rules achieved perfect accuracy in sub-millisecond latency.
2. **Spoonful 2 — 70 ms hybrid memory (`experience-memory`), modular on-demand skills, and 7 MCP servers:**
   - Coupling SQLite FTS5 lexical search with Qdrant dense vectors (`Qwen3-Embedding-0.6B`) in `70 ms`, keeping long-term operational lessons separate from procedural skills and Model Context Protocol (MCP) tools.
3. **Spoonful 3 — A zero-token local autopoiesis loop in `Harness²` (Xu et al. 2026):**
   - Adapting Google Research's `Harness²` in offline shadow mode (`model_calls = 0`, no `--dangerously-skip-permissions`) over `9` seed cases across `3` domains (`routing`, `memory`, `skills`) backed by `82` deterministic unit tests. Real operational friction becomes holdout test cases, and internal resistance discards regressive candidates before human review.
