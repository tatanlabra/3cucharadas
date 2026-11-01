# Reddit: hilos del Post IV (en inglés)

Texto redactado por el autor y enviado como post de texto con el formulario prellenado de
old.reddit, abierto en su navegador. El título es la primera frase del texto. En r/LocalLLaMA se
cambió una frase a pedido del autor para no sugerir inferencia local: los agentes son CLIs en la
nube y lo local es la memoria. Las reglas de los subreddits no se pudieron leer de forma
automática. Los cuerpos tienen varios párrafos, así que `reddit_prefill_urls.py` no los
reabriría bien; las dos secciones llevan la marca de publicado y el script las omite.

## r/AI_Agents

Publicado por el autor el 1 de noviembre de 2026:
https://www.reddit.com/r/AI_Agents/comments/1xleo4g/

**Título:** Is anyone else experimenting with something resembling autopoiesis in their AI agents?

**Texto:**

I've been exploring this with a small local multi-agent setup (Claude Code, Codex, and Gemini). The idea is to move beyond agents that simply execute tasks toward a system that learns from its own operational failures.

My experiment combines hybrid memory, failure detection, and a local adaptation of Google's Harness². It turns recurring problems into reproducible tests, evaluates changes to routing, memory, and skills, and rejects regressions before any human-approved deployment.

Still very early: 9 baseline cases, 82 tests, and plenty of limitations. I'm certainly not claiming genuine biological autopoiesis or autonomous intelligence.

I documented the experiment, including a terminal demo, here:

https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/

**Is anyone building something similar?** Particularly interested in how others prevent self-improvement loops from reinforcing their own mistakes or simply overfitting to past failures.

## r/LocalLLaMA

Publicado por el autor el 1 de noviembre de 2026:
https://www.reddit.com/r/LocalLLaMA/comments/1xlepxp/

**Título:** Is anyone else experimenting with something resembling autopoiesis in their AI agents?

**Texto:** igual al de r/AI_Agents, salvo la primera frase, que dice:

I've been exploring this with a multi-agent setup that runs on my own machine: the agents are cloud CLIs (Claude Code, Codex, and Gemini), but memory is local (SQLite FTS5 + Qdrant with Qwen3-Embedding-0.6B).
