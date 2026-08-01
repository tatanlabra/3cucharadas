# Multiagente II - targeting social

Estado: actualizado despues de seguir el lote recomendado el 2026-07-24. No publicar mensajes sin aprobacion.

## Regla de uso

- Usar menciones solo si la cuenta esta directamente vinculada con una tecnologia usada en el post.
- Mantener maximo una mencion fuerte en la raiz de Mastodon/Bluesky; una mencion complementaria en respuesta si agrega contexto.
- En LinkedIn, resolver las menciones manualmente con el typeahead de la plataforma; no dejar `@Nombre` como texto plano si LinkedIn no lo convierte en entidad.
- En Mastodon, preferir hashtags y cuentas curatoriales; mencionar cuentas remotas solo si el hilo lo justifica.

## Cuentas y plataformas

| Prioridad | Plataforma | Cuenta o entidad | Uso recomendado | Evidencia |
| --- | --- | --- | --- | --- |
| Alta | Bluesky | `@qdrant.bsky.social` | Mencionar en la raiz ES/EN cuando el post trate retrieval, vector DB, BM25, hybrid search o agent memory. | <https://bsky.app/profile/qdrant.bsky.social> |
| Media | Bluesky | `@mcp-community.bsky.social` | Mencionar en respuesta o hilo cuando MCP sea parte central del flujo. Es comunidad/protocolo, no proveedor del stack. | <https://bsky.app/profile/mcp-community.bsky.social> |
| Alta | LinkedIn | Qdrant | Mencion manual recomendada si se habla de Qdrant, vector search, BM25 o memoria de agentes. | <https://www.linkedin.com/company/qdrant> |
| Alta | LinkedIn | Ollama | Mencion manual recomendada si se destaca ejecucion local o modelos servidos por Ollama. | <https://www.linkedin.com/company/ollama> |
| Media | LinkedIn | Beijing Academy of Artificial Intelligence (BAAI) | Mencion manual opcional si se enfatiza BGE-M3. Mejor usar una sola vez, no junto a demasiadas marcas. | <https://www.linkedin.com/company/beijingbaai> |
| Media | LinkedIn | Hugging Face | Mencion manual opcional si el post remite al ecosistema/model card, no si solo se uso Ollama local. | <https://www.linkedin.com/company/huggingface> |
| Media | Bluesky | `@langchain.bsky.social` | Seguir e interactuar por RAG/agentes; mencionar solo si el texto habla de apps context-aware o agentes sobre herramientas. | <https://bsky.app/profile/langchain.bsky.social> |
| Media | Bluesky | `@llamaindex.bsky.social` | Seguir e interactuar por agentes sobre documentos; mencion solo si el texto conecta con retrieval/documentos. | <https://bsky.app/profile/llamaindex.bsky.social> |
| Media | Bluesky | `@hamel.bsky.social` | Seguir por evaluacion de LLMs; mejor como comunidad/referencia que como mencion directa en esta publicacion. | <https://bsky.app/profile/hamel.bsky.social> |
| Media | Mastodon | `@llamaindex@fosstodon.org` | Seguir por RAG/agentes; evitar mencionarlo en esta publicacion porque no es componente usado directamente. | <https://fosstodon.org/@llamaindex> |
| Media | Mastodon | `@FediFollows@social.growyourown.services` | Seguir para discovery continuo de comunidades Fediverse. No mencionar en posts tecnicos. | <https://social.growyourown.services/@FediFollows> |
| Baja | Bluesky/Mastodon | Bots mirror de Ollama/OpenAI/Anthropic | No usar como mencion de difusion: son espejos no oficiales y pueden verse como ruido. | Verificar caso a caso antes de usar. |
| Baja | LinkedIn/Bluesky | OpenAI, Anthropic, Google DeepMind | No mencionar por defecto en este post: Codex/Claude/Gemini aparecen como consumidores del flujo, pero el articulo no evalua sus productos. | Usar solo si el texto futuro los discute directamente. |

## X / Twitter

| Prioridad | Cuenta | Uso recomendado |
| --- | --- | --- |
| Alta | `@qdrant_engine` | Seguir y mencionar si el post habla de Qdrant, vector search, hybrid search, BM25 o memoria de agentes. |
| Alta | `@ollama` | Seguir y mencionar si se destaca ejecucion local o modelos servidos por Ollama. |
| Media | `@huggingface` | Seguir; mencionar solo si se enfatiza BGE-M3 como modelo o el ecosistema de modelos abiertos. |
| Media | `@llama_index` | Seguir por RAG/agentes sobre documentos; no mencionar en este post salvo que el texto conecte con LlamaIndex. |
| Media | `@LangChain` | Seguir por agentes y context engineering; no mencionar en este post salvo comparacion directa. |
| Media | `@deepset_ai` | Seguir por Haystack/RAG; no mencionar en este post salvo referencia directa a Haystack. |
| Media | `@weaviate_io` | Seguir por vector search/RAG; no mencionar en este post salvo comparacion directa. |
| Media | `@pinecone` | Seguir por vector DB/RAG; no mencionar en este post salvo comparacion directa. |
| Media | `@elastic` | Seguir por search/BM25/hybrid retrieval; mencionar solo si el texto habla de busqueda lexical o Elastic. |
| Baja | `@BAAIBeijing` | Posible cuenta de BAAI; verificar manualmente antes de seguir o mencionar. |

## Hashtags recomendados

| Plataforma | Set base | Alternativas |
| --- | --- | --- |
| Mastodon ES | `#RAG #IA #AIAgents #MLOps` | `#VectorSearch`, `#OpenSource`, `#OpenData` |
| Mastodon EN | `#RAG #AIAgents #VectorSearch #MLOps` | `#AIEngineering`, `#OpenSource` |
| Bluesky ES/EN | `#RAG #AIAgents` | `#VectorSearch`, `#MLOps` si queda espacio |
| LinkedIn | `#RAG #AIAgents #VectorSearch #LocalAI #MLOps` | `#ContextEngineering`, `#OpenSourceAI` |

## Copy note

Para LinkedIn, el foco debe seguir siendo primera persona y evidencia concreta. Las menciones son secundarias: primero el hallazgo, luego el stack, luego la invitacion a comparar experiencias.
