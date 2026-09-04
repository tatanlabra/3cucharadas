# Multiagentes III — targeting social

Estado: preparado, sin publicar. No enviar mensajes sin aprobación humana explícita.

Derivado del targeting del Post II, con la diferencia de stack que impone este post: aquí
**no hay Ollama ni bge-m3**. El stack de recuperación cambió a Qwen3-Embedding-0.6B servido
por Sentence Transformers sobre CPU, y Qdrant sigue siendo el índice.

## Regla de uso

- Mencionar solo cuentas directamente vinculadas a una tecnología usada en el post.
- Máximo una mención fuerte en la raíz de Mastodon/Bluesky; una complementaria en la respuesta si aporta contexto.
- En LinkedIn, resolver las menciones con el typeahead. Si no convierte en entidad, dejar texto plano.
- **No mencionar a ningún proveedor de modelos de agente** (OpenAI, Anthropic, Google): Codex, Claude y Gemini aparecen como consumidores del flujo, no como objeto de evaluación. Mencionarlos convertiría una bitácora en algo que parece marketing comparativo.

## Cambio respecto al Post II

| Cuenta del Post II | Qué hacer ahora | Por qué |
| --- | --- | --- |
| `@ollama` / Ollama (LinkedIn) | **No mencionar** | Ollama no interviene en este post. El embedding corre por Sentence Transformers en CPU. |
| BAAI (bge-m3) | **No mencionar** | El modelo cambió a Qwen3-Embedding-0.6B. |
| `@qdrant.bsky.social` / Qdrant | **Mantener, prioridad alta** | Sigue siendo el índice, y el post discute vector nombrado `dense` y reindexación selectiva. |

## Cuentas y plataformas

| Prioridad | Plataforma | Cuenta o entidad | Uso recomendado | Evidencia |
| --- | --- | --- | --- | --- |
| Alta | Bluesky | `@qdrant.bsky.social` | Mencionar en la raíz ES/EN. El post trata recuperación híbrida, vector nombrado y reindexación. | <https://bsky.app/profile/qdrant.bsky.social> |
| Alta | LinkedIn | Qdrant | Mención manual en el cuerpo, donde ya está marcada como `@Qdrant`. | <https://www.linkedin.com/company/qdrant> |
| Media | LinkedIn | Hugging Face | Opcional, una sola vez, si se quiere apuntar a la tarjeta del modelo Qwen3-Embedding. No combinar con otras marcas en el mismo párrafo. | <https://www.linkedin.com/company/huggingface> |
| Media | Bluesky | `@llamaindex.bsky.social` | Seguir e interactuar. Mención solo si el hilo deriva hacia procedencia de documentos. | <https://bsky.app/profile/llamaindex.bsky.social> |
| Media | Bluesky | `@hamel.bsky.social` | Seguir por evaluación de LLM. Este post encaja bien con esa comunidad porque rechaza cuatro hipótesis con medición. | <https://bsky.app/profile/hamel.bsky.social> |
| Media | Mastodon | hashtags `#RAG` `#AIAgents` `#KnowledgeGraph` | Vía principal en Mastodon. Preferir hashtags sobre menciones remotas. | — |
| Baja | LinkedIn/Bluesky | Alibaba / Qwen | **No mencionar como marca.** El modelo se cita por nombre técnico. Mencionar a la empresa sugiere una relación que no existe. | — |
| Baja | Cualquiera | Bots espejo de proveedores de LLM | No usar: son espejos no oficiales y se leen como ruido. | — |

## Comunidades donde este post encaja de verdad

Este post tiene un ángulo que el II no tenía: **publica una compuerta en rojo a propósito**.
Eso lo hace pertinente en comunidades de ingeniería de evaluación y de gobernanza de datos,
no solo en las de RAG.

| Comunidad | Plataforma | Encaje |
| --- | --- | --- |
| r/LocalLLaMA | Reddit | Alto: stack local, CPU, medición de latencia real. Publicar el texto, no el enlace solo. |
| r/MachineLearning | Reddit | Medio: exige rigor; el rechazo del reordenador con números es lo que le interesa. |
| Hacker News | HN | Medio-alto: el ángulo «publico el gate en rojo» es el gancho, no el visor 3D. |
| dev.to | dev.to | Automático vía `feed-dev-en.xml` al pushear el post EN. |

## Hashtags

- LinkedIn: `#RAG #AIAgents #KnowledgeGraph #ContextEngineering #MLOps`
- Mastodon y Bluesky: `#RAG #AIAgents #KnowledgeGraph` (tres bastan; más se lee como spam en el Fediverso)
