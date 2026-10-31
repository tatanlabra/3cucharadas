TÍTULO PROVISIONAL:
From a terminal CLI trident to a zero-token autopoietic loop: hybrid 70 ms memory, negative benchmarks (why regex beat an ONNX classifier), and adapting Google's Harness2 in shadow mode

URL PROPUESTA:
https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/

PRIMER COMENTARIO PROPUESTO:
I wrote up Part IV of my engineering log on `penta-agent` (an open-source multi-agent harness on Arch Linux coordinating Claude Code, Codex CLI, and Gemini CLI / Antigravity inside `kitty` + `tmux`).

Key technical takeaways and negative results from the post:
- **Why standalone LLMs lack internal resistance:** Drawing on Zönnchen, Dzhimova, and Socher (2025) and Luhmann (1998), an isolated LLM only computes next-token plausibility without Spencer-Brown *re-entry* or a binary `work / fail` boundary.
- **Two negative benchmarks:** I purged dozens of gigabytes of local models that had 0 real routing calls over 60 days, and archived a local ONNX neural prompt classifier after deterministic lexical rules achieved perfect accuracy in sub-millisecond latency.
- **70 ms hybrid memory + modular skills + 7 MCP servers:** Coupling SQLite FTS5 lexical search with Qdrant dense vectors (`Qwen3-Embedding-0.6B`).
- **Adapting Google's `Harness²` (Xu et al. 2026) with `model_calls = 0`:** Running recursive harness evaluation offline in shadow mode across 9 seed cases (`routing`, `memory`, `skills`) and 82 deterministic tests so regressions are discarded before human promotion.

Code repository: https://github.com/tatanlabra/penta-agent
