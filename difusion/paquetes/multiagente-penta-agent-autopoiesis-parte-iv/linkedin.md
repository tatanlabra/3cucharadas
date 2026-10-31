# LinkedIn — ES nativo + variante EN

## Cuerpo principal (ES — el enlace con UTM va en el primer comentario)

En la parte III de esta serie dejé funcionando en mi terminal un tridente de agentes (Claude Code, Codex CLI y Gemini CLI / Antigravity). Meses después de usarlo todos los días en `penta-agent`, choqué con una verdad incómoda: tener tres agentes conversando no equivale a tener un sistema que aprende.

Sin memoria gobernada ni compuertas falsables, cada sesión nueva sufría de amnesia parcial, repetía comandos fallidos o gastaba cuota del modelo más caro en tareas rutinarias. Para resolverlo dejé de preguntarme si un modelo «piensa» y pasé a una pregunta de teoría de sistemas (Maturana y Varela 1984; Luhmann 1995, 1998; Zönnchen, Dzhimova y Socher 2025): ¿puede el sistema trazar su propia frontera, observar sus propios fallos y sostenerse mediante sus propias operaciones? Es decir, **autopoiesis**.

Un modelo de lenguaje suelto en una ventana de chat carece de *re-entry* (Spencer-Brown 1969) y de resistencia interna: calcula qué palabra es plausible tras otra, pero no choca contra sus propios errores. En esta cuarta entrega muestro cómo construí un arnés socio-técnico alrededor de los modelos en tres capas:

- **Gobernanza y decisiones auditables en consola (`kitty` + `tmux`):** ruteo por cuota real (`quota-guard`), compuertas deductivas/inductivas/abductivas (`decision-gate`) y un tablero vivo (`plan-board` v2) que bloquea el cierre si un paso no tiene evidencia verificada. Antes de llegar ahí descarté con datos dos ideas tentadoras: purgué decenas de gigabytes de modelos locales tras 60 días con 0 invocaciones reales y archivé un clasificador neuronal ONNX donde reglas léxicas deterministas lograban precisión perfecta en fracciones de milisegundo.
- **Memoria híbrida en 70 ms, skills modulares y 7 servidores MCP:** acople de búsqueda léxica SQLite FTS5 con vectores densos en Qdrant (`Qwen3-Embedding-0.6B`), separando la memoria de largo plazo de las capacidades activadas bajo demanda.
- **Un circuito cerrado de autopoiesis local en `Harness²` (Xu et al. 2026):** adaptado en modo sombra sobre mi propio arnés, sin red, sin `--dangerously-skip-permissions` y con `model_calls = 0`. La telemetría real alimenta 9 casos semilla en 3 dominios (`routing`, `memory`, `skills`) respaldados por 82 pruebas deterministas: cuando un candidato introduce una regresión, la resistencia interna del banco lo descarta antes de llegar a mi revisión.

Dejo el artículo completo (con diagramas, videos reales de mi terminal y todas las referencias científicas enlazadas) en el primer comentario. ¿Qué mecanismos usan ustedes para evitar que sus flujos con agentes repitan errores entre sesiones?

### Primer comentario (ES)
Artículo completo y repositorio en: https://3cucharadas.cl/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/?utm_source=linkedin&utm_medium=social&utm_campaign=multiagente_parte_iv

---

## English variant (LinkedIn EN)

In Part III of this series, I had three CLI agents (Claude Code, Codex CLI, and Gemini CLI / Antigravity) collaborating in my Arch Linux terminal. Months of daily use inside `penta-agent` taught me an uncomfortable lesson: having three agents talking does not equal having a system that learns.

Drawing on systems theory and autopoiesis (Maturana and Varela 1984; Luhmann 1995, 1998; Zönnchen, Dzhimova, and Socher 2025), Part IV shows why a standalone LLM lacks genuine *re-entry* (Spencer-Brown 1969) and internal resistance—and how I built a deterministic socio-technical harness around the models across three layers:

- **Quota-governed routing and a live `plan-board` in `kitty` + `tmux`:** including two negative experiments where measurement beat hype (reclaiming unused local model weights after 60 days with 0 invocations, and archiving a local ONNX neural classifier after deterministic lexical rules achieved perfect accuracy in sub-millisecond latency).
- **70 ms hybrid memory (SQLite FTS5 + Qdrant) coupled with modular skills and 7 MCP servers.**
- **A zero-token autopoiesis loop adapted from Google's `Harness²` (Xu et al. 2026):** running offline in shadow mode (`model_calls = 0`) across 9 seed cases and 82 deterministic tests to filter out regressive candidates before human review.

Full article in the first comment: https://3cucharadas.cl/en/ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/?utm_source=linkedin&utm_medium=social&utm_campaign=multiagente_parte_iv
