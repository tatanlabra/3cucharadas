**Multiagentes II: memoria auditable**

Segunda parte: más y mejor memoria para los agentes.

Cómo recuperar evidencia desde historiales, hacerla persistente y auditar cuándo el sistema debe abstenerse.

En esta segunda bitácora de mi sistema multiagente cuento el ajuste más útil hasta ahora: tratar @Qdrant, bge-m3 y BM25 como índices derivados, no como verdad; conservar JSONL/YAML como fuente canónica; y probar la recuperación con un gate semanal que también sabe decir "no hay evidencia suficiente".

La parte menos glamorosa es la más importante: el agente puede traer una pista convincente y aun así estar equivocado. La memoria útil no es la que siempre responde, sino la que deja rastro de por qué respondió, de dónde salió la evidencia y qué parte todavía no puede sostener.

Lo corrí en local con @Ollama, Qdrant, bge-m3, BM25/FastEmbed y un gate de regresión. No es una arquitectura universal; es una forma concreta de evitar que una memoria de agente se convierta en continuidad inventada.

Me interesa especialmente leer otras estrategias de RAG que les hayan funcionado en producción o en uso sostenido: qué guardan, qué descartan, cómo fusionan señales, cuándo usan reranking/RRF y cómo prueban que la recuperación no está inventando continuidad.

#RAG #AIAgents #VectorSearch #ContextEngineering #MLOps


## Primer comentario

La historia completa está aquí:

https://3cucharadas.cl/ia/productividad/desarrollo/multiagente-penta-agent-memoria/?utm_source=linkedin&utm_medium=social&utm_campaign=multiagente_penta_agent_memoria

## Nota de publicación

En LinkedIn, convertir manualmente `@Qdrant` y `@Ollama` en menciones reales usando el typeahead de la plataforma. Si no se resuelven como entidades, dejar solo `Qdrant` y `Ollama`.
