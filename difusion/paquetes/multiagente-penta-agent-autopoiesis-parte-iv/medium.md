# Multi-agent work in three spoonfuls (part IV): from a terminal trident to an autopoietic loop

*Originally published at [3cucharadas.cl](https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/). When importing into Medium, set the canonical link to `https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/`.*

Having three CLI agents—Claude Code, Codex CLI, and Gemini CLI / Antigravity—collaborating in a terminal does not produce a system that learns. Without governed memory, quota-aware routing, and falsifiable verification gates, every fresh session suffers from partial amnesia, repeats failed commands, or burns quota blindly.

In Part IV of my `penta-agent` engineering log, I turn to systems theory and **autopoiesis** (Maturana and Varela 1987 [1984]; Luhmann 1995, 1998; Spencer-Brown 1969; Esposito 2017, 2024; Zönnchen, Dzhimova, and Socher 2025) to explain why a standalone large language model lacks genuine *re-entry* and **internal resistance**—and how I built a deterministic socio-technical harness around the models across three layers:

- **Quota-governed routing (`quota-guard`), trade-off gates (`decision-gate`), and a live `plan-board` in `kitty` and `tmux`:** grounded in two negative benchmarks where measurement beat hype (reclaiming unused local model weights after `60` days with `0` invocations, and archiving an ONNX neural classifier after deterministic lexical rules achieved perfect accuracy in sub-millisecond time).
- **A `70 ms` hybrid memory (`experience-memory`)** coupling SQLite FTS5 lexical search with Qdrant dense vectors (`Qwen3-Embedding-0.6B`), paired with modular skills and `7` MCP servers.
- **A zero-token autopoiesis loop adapted from Google Research's `Harness²` (Xu et al. 2026):** running offline in shadow mode (`model_calls = 0`) across `9` seed cases in `3` domains (`routing`, `memory`, `skills`) and `82` deterministic tests so regressive candidates are discarded by internal resistance before human review.

Read the complete article with real `kitty` + `tmux` videos, responsive architecture diagrams, and full citations at:
https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/
