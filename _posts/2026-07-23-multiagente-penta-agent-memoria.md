---
layout: single
title: "Multiagentes en 3 cucharadas II: una memoria que se puede auditar"
subtitle: "De los handoffs a una recuperación compartida: qué implementé, cómo lo medí y qué falta validar"
date: 2026-07-23 00:00:00 +0000
last_modified_at: 2026-07-24 00:00:00 +0000
categories: [ia, productividad, desarrollo, multiagente]
tags: [multiagente, rag, embeddings, memoria-agentes, qdrant, bm25, mcp, context-engineering, arch-linux]
description: "Segunda bitácora de penta-agent: cómo convertí su memoria operativa en un mecanismo evaluable, qué arquitectura quedó realmente implementada y cómo evité confundir una coincidencia plausible con evidencia."
excerpt: "Ya tenía handoffs y decisiones. El paso siguiente fue comprobar qué recuperaba, con qué arquitectura y cuándo debía reconocer que no tenía evidencia suficiente."
author: clabra
lang: es
ref: multiagente-penta-agent-memoria
permalink: /ia/productividad/desarrollo/multiagente-penta-agent-memoria/
toc: true
toc_sticky: true
comments: true
author_profile: true
math: true
published: true
header:
  teaser: /assets/images/teasers/teaser-multiagentes-memoria.webp
---

En el [primer post](/ia/productividad/desarrollo/multiagente-penta-agent-modelos/) conté cómo ordené `penta-agent`: Codex ejecuta, Claude revisa, otros agentes entran de manera acotada y el humano conserva el cierre. También dejé planteado que la memoria operativa no debía depender de una conversación aislada ni confundirse con el índice vectorial.
{: .text-justify}

Al cerrar esa primera publicación ya tenía mecanismos de continuidad: handoffs, reglas de routing, bitácoras append-only, una memoria experiencial en JSONL/YAML, una colección vectorial reconstruible y la skill `recall-context`. Mi problema no era una amnesia absoluta. Era que todavía no podía demostrar qué recuperaba, cuándo confundía una coincidencia con evidencia y cuándo debía reconocer que no tenía respuesta.
{: .text-justify}

Esta segunda parte no trata, por tanto, de inventar una memoria desde cero. Trata de convertir una continuidad operativa todavía frágil en un mecanismo **trazable, evaluable y reconstruible**.
{: .text-justify}

## Cucharada 1: el problema no era guardar, sino recuperar bien

Guardar información es fácil. Lo difícil, creo, es recuperar la pieza correcta cuando existen decisiones sucesivas, nombres parecidos, versiones contradictorias y explicaciones repartidas entre varios archivos.
{: .text-justify}

Para ordenar esa "memoria" en mi caso, separé sus capas operativas:
{: .text-justify}

{: .table-caption}
**Tabla 1** — Capas de memoria del sistema

| Capa | Pregunta que responde | Implementación efectiva |
|---|---|---|
| Registro canónico | ¿Qué ocurrió y qué se decidió? | `memory/experience-events.jsonl`, `memory/experience-lessons.yaml`, `memory/interaction-metrics.jsonl` y eventos `context` curados. |
| Índice de recuperación | ¿Dónde está la evidencia pertinente? | Qdrant con `penta_context_v2` para contexto curado y `penta_experience_v1` para memoria operacional; ambos son derivados. |
| Historial episódico | ¿Cómo se desarrolló una sesión? | Handoffs Markdown seleccionados, eventos compactos de contexto y logs operacionales; las sesiones completas no se indexan crudas. |
| Contexto de trabajo | ¿Qué contexto necesito entregar ahora? | MCP `experience-memory` (`experience_status`, `recall_experience`) consumido por la skill `recall-context`. |

La distinción importa. Un resultado recuperado no es todavía una decisión comprobada. Es una pista que debe conservar procedencia, fecha y vínculo con su fuente. En el contrato actual, los JSONL/YAML locales son la fuente de verdad; Qdrant se reconstruye desde ellos. Si el índice contradice un archivo vigente, gana el archivo y corresponde reindexar o corregir la ingesta, no publicar la vecindad vectorial como si fuera evidencia final.
{: .text-justify}

El flujo real quedó así:
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/multiagente-penta-agent-memoria/flujo-memoria-penta-agent.svg' | relative_url }}" alt="Diagrama de flujo de la memoria de penta-agent: trazas curadas, ingesta selectiva, fuente canónica, representación con embeddings y BM25, Qdrant derivado, recuperación híbrida, MCP y uso por Codex, Claude o Gemini con cierre humano." loading="lazy" decoding="async">
  <figcaption><strong>Figura 1</strong> — Flujo operativo de la memoria validable de <code>penta-agent</code>. Nota: los JSONL/YAML locales son la fuente de verdad; Qdrant y BM25 son índices derivados para recuperación, no evidencia final.</figcaption>
</figure>

### RAG, sin convertirlo en magia

Un modelo de lenguaje guarda parte de lo aprendido durante el entrenamiento en sus parámetros. Esa memoria no incluye necesariamente lo que decidí ayer en un repositorio local. La *Retrieval-Augmented Generation* o RAG agrega una memoria externa: antes de responder, un recuperador busca pasajes pertinentes y se los entrega al modelo generativo como contexto.[^rag]
{: .text-justify}

En mi implementación, `experience-memory` hace de recuperador: consulta Qdrant, fusiona señales con los registros canónicos y entrega candidatos mediante MCP. Después Codex, Claude o Gemini usan ese contexto según el flujo. Por eso prefiero describirlo como **recuperación aumentada para agentes** antes que como un «RAG autónomo»: almacenar y ordenar fragmentos no equivale a razonar sobre ellos.
{: .text-justify}

### Buscar por significado y por palabras

La búsqueda semántica transforma cada fragmento en un vector. La consulta se representa con el mismo modelo y luego se compara su orientación mediante similitud coseno:
{: .text-justify}

$$
\operatorname{sim}(q,d)=
\frac{\mathbf{q}\cdot\mathbf{d}}
{\lVert\mathbf{q}\rVert\,\lVert\mathbf{d}\rVert}
$$

Si la consulta y el documento apuntan en direcciones parecidas, su similitud aumenta. Esto permite encontrar paráfrasis aunque no compartan exactamente las mismas palabras.
{: .text-justify}

Una búsqueda léxica cubre el problema complementario: identificadores, siglas, rutas, nombres propios y términos exactos. BM25 no se limita a contar coincidencias; pondera la rareza y frecuencia de los términos, satura repeticiones y corrige parcialmente por la longitud documental.[^bm25]
{: .text-justify}

Hoy combino cinco señales:
{: .text-justify}

- búsqueda densa en Qdrant con embeddings de `bge-m3`;
- fallback léxico sobre los eventos canónicos `context`;
- vector sparse BM25 con `Qdrant/bm25`;
- recencia del evento;
- tipo de ciclo de vida: `outcome`, `review`, `decision` o `handoff`.

Todavía no uso RRF en la versión evaluada. La fusión que dejé activa es una fórmula ponderada en `hybrid_context_hits`: cuando hay señal semántica, pesa 0,60 para similitud densa, 0,28 para léxico, 0,07 para recencia y 0,05 para ciclo de vida. Cuando no hay señal semántica, el fallback pesa principalmente el léxico. BM25 suma como reordenamiento adicional, pero no basta por sí solo para rescatar un resultado.
{: .text-justify}

Me falta una virtud menos vistosa: saber callar al sistema. Una consulta sin respuesta en el corpus no debería recibir un fragmento solo porque parece cercano. En esta versión mido **rechazo del recuperador**: un candidato califica si supera alguno de estos criterios en la corrida del gate, `lexical_score >= 0.34`, `semantic_score >= 0.44` o `hybrid_score >= 0.61`. Todavía no tengo una métrica automatizada de abstención del generador final. Si un modelo recibe contexto y aun así inventa, esta evaluación no lo detecta.
{: .text-justify}

## Cucharada 2: de un índice útil a una recuperación evaluada

Lo que dejé funcionando usa estas piezas, verificadas contra el repo local y los servicios activos:
{: .text-justify}

{: .table-caption}
**Tabla 2** — Componentes activos

| Función | Componente | Configuración comprobada |
|---|---|---|
| Fuente canónica | `memory/*.jsonl` y `memory/*.yaml` | Registros locales regenerables; al revisar había 1.829 líneas en `experience-events.jsonl` y 904 en `interaction-metrics.jsonl`. |
| Vectorización densa | Ollama + `bge-m3:latest` | Modelo `bert`, 566,70M parámetros, F16, contexto 8192, embedding 1024. |
| Base vectorial | Qdrant local | Colecciones `penta_context_v2` y `penta_experience_v1`; el MCP reportó estado `green`, 14 contextos canónicos y 1.769 puntos operacionales. |
| Recuperación léxica | JSONL canónico + FastEmbed BM25 | `context_fallback_hits` calcula coincidencia léxica; `SparseTextEmbedding("Qdrant/bm25")` alimenta el vector sparse `bm25`. |
| Fusión | `hybrid_context_hits` | Fusiona denso, léxico, BM25, recencia y ciclo de vida; deduplica por `handoff_id` o `source_document`. |
| Reranking | No activo en la corrida publicada | Existe un reranker opt-in con `PENTA_AGENT_RERANK=1`, pero el gate validado no lo usa. |
| Interfaz para agentes | MCP `experience-memory` | `experience_status` y `recall_experience`; la skill `recall-context` lo usa como ruta primaria. |
| Automatización de pruebas | `evaluate_context_retrieval.py` y `rag_regression_gate.py` | El timer `penta-agent-rag-gate.timer` está habilitado semanalmente; el gate registra histórico en `memory/retrieval-metrics.jsonl`. |

Lo corro en una estación local con Arch Linux/KDE. Ollama y Qdrant se consultan por loopback; los timers son de `systemd --user`. Ese detalle no es cosmético: si aíslo el fallback canónico o falta el entorno del gate, la recuperación cambia materialmente. Por eso el servicio del gate fija explícitamente `PENTA_AGENT_EMBED_BACKEND=ollama`, `PENTA_AGENT_OLLAMA_MODEL=bge-m3` y `PENTA_AGENT_CONTEXT_SEM_THRESHOLD=0.44`.
{: .text-justify}

### El modelo de embeddings realmente usado

El modelo BGE-M3, en su implementación original, admite representaciones densas, dispersas y multivectoriales, trabaja con más de cien idiomas y acepta secuencias extensas.[^bge-m3] Pero esas capacidades del modelo no prueban que todas estén expuestas en mi *stack*.
{: .text-justify}

Estoy usando `bge-m3:latest`, servido por Ollama mediante `/api/embed`.[^ollama-embed] En la práctica uso **solo la representación densa** que entrega Ollama: vectores de 1024 dimensiones en la instalación local. La rama sparse del sistema no viene de BGE-M3; viene de BM25 con FastEmbed y Qdrant.[^qdrant-vectors][^qdrant-bm25] Pooling, tokenización y normalización quedan encapsulados en el runtime de Ollama, no en código propio del repo.
{: .text-justify}

Tampoco hice una fragmentación general de todo el workspace. La ingesta `context` trabaja con documentos seleccionados: handoffs Markdown saneados y eventos compactos. Al importar handoffs, el extractor toma secciones como objetivo/contexto, decisión y resultado, las compacta, conserva `source_document`, `source_hash`, `source_type`, `handoff_id`, `workspace_entry`, `repo_scope`, rama y fecha, y limita los textos a campos cortos. No vuelco conversaciones completas ni archivos privados en bruto.
{: .text-justify}

### Un conjunto de preguntas que incomode al sistema

Evalué con un golden set local de 40 preguntas: 32 positivas y 8 negativas. Las positivas apuntan a documentos esperados mediante sufijos relativos al workspace; el evaluador no abre ni emite el contenido fuente. Las etiquetas de dificultad no son mutuamente excluyentes: hay 10 casos de keyword exacto, 9 de paráfrasis, 7 entre idiomas, 3 coloquiales y 4 multi-documento. Los negativos incluyen consultas de cocina, deportes, finanzas, ciencia y tecnología no relacionada.
{: .text-justify}

Anoté las respuestas esperadas manualmente contra handoffs seleccionados y rutas relativas. Eso lo hace útil como conjunto de desarrollo y regresión, no como benchmark independiente. Si uso el mismo archivo para calibrar umbrales y luego celebrar el resultado, no puedo tratarlo como evidencia independiente.
{: .text-justify}

### Resultados: lo que pasó en la corrida validada

La corrida que dejé trazable fue:
{: .text-justify}

```bash
env PENTA_AGENT_EMBED_BACKEND=ollama \
    PENTA_AGENT_OLLAMA_MODEL=bge-m3 \
    PENTA_AGENT_CONTEXT_SEM_THRESHOLD=0.44 \
    /opt/entornos/mamba312/bin/python scripts/evaluate_context_retrieval.py --strict
```

La corrí en modo estricto y salió con código 1 porque hubo un caso parcial. El gate, en cambio, pasó porque evalúa umbrales agregados: recall mínimo 0,95, MRR mínimo 0,85, precisión mínima 0,40 y abstención negativa perfecta.
{: .text-justify}

{: .table-caption}
**Tabla 3** — Resultado local validado

| Configuración | Recall@5 | MRR | Precision@5 | Rechazo de negativos | Latencia |
|---|---:|---:|---:|---:|---:|
| `bge-m3` + Qdrant denso + JSONL léxico + BM25 sparse | 0,9896 | 0,9479 | 0,4448 | 8/8 | p50 401 ms; máximo 4.250 ms |

Mi lectura prudente es:
{: .text-justify}

1. La recuperación que dejé activa encuentra casi toda la evidencia anotada en este corpus chico y curado.
2. Los negativos son el mejor resultado: ocho de ocho fueron rechazados.
3. La precisión@5 es baja a propósito: prefiero traer contexto de más antes que perder el documento esperado.
4. El error que queda es multi-documento: `catastro_multi_sii` recuperó parte, no toda, la evidencia esperada.
5. La métrica no prueba que la respuesta final sea fiel; prueba solo que el recuperador trajo o rechazó candidatos.

También encontré una señal práctica: al aislar el fallback canónico sin Qdrant, el recall agregado baja a 0,8177. Ese no es el resultado del stack elegido; es la comparación que necesitaba para saber cuánto aporta la recuperación semántica y por qué la configuración de evaluación debe ser explícita.
{: .text-justify}

### Fusión y reranking

Hoy no comparo puntajes crudos de modelos distintos como si fueran la misma escala. Primero reúno candidatos desde Qdrant denso, JSONL léxico y BM25 sparse. Luego calculo un puntaje híbrido con umbrales de admisión. Después deduplico por ciclo de vida: si existe un `outcome` y un handoff pendiente con el mismo `handoff_id`, el resultado completo gana.
{: .text-justify}

### Un gate de regresión

Puedo ejecutar la evaluación a mano y también la dejé instalada como timer semanal de usuario: `penta-agent-rag-gate.timer`, con `OnCalendar=weekly`, `Persistent=true` y retardo aleatorio de hasta 30 minutos. El servicio ejecuta `scripts/rag_regression_gate.py` con Ollama, `bge-m3` y umbral semántico 0,44. Registra métricas agregadas en `memory/retrieval-metrics.jsonl` y falla si cae bajo los umbrales configurados.
{: .text-justify}

Lo llamo **gate de regresión** porque comprueba casos conocidos. Detectar deriva de verdad exige observar cambios en consultas, documentos, versiones o distribuciones de puntajes.
{: .text-justify}

## Cucharada 3: lo que esta memoria todavía no resuelve

La memoria ya recupera mejor, pero sigue teniendo límites claros: no resuelve bien la vigencia entre documentos, no detecta contradicciones de forma general, no convierte sesiones completas en memoria permanente y todavía falla en algunas respuestas que requieren unir varias fuentes.
{: .text-justify}

Tampoco evalúo aún la fidelidad de la respuesta final. Recall, MRR y precisión indican si apareció la evidencia correcta, no si Claude o Codex la interpretaron bien, respetaron su vigencia o supieron abstenerse. Benchmarks como BEIR muestran además que ningún recuperador domina de forma uniforme en todos los dominios.[^beir]
{: .text-justify}

Lo próximo es comparar, de forma reproducible, cada capa del sistema: búsqueda densa, JSONL léxico, BM25, híbrido, RRF y reranking opt-in. Después quiero agregar vigencia entre documentos y evaluación de respuestas con citas, para medir no solo si recupero evidencia, sino si la respuesta la usa con fidelidad.
{: .text-justify}

Si estás construyendo algo parecido —un multiagente, un RAG local, un *second brain* o una memoria de trabajo para no repetir contexto— me interesa leer qué te funcionó, dónde falló y cómo decidiste cuándo abstenerte. Esa comparación entre bitácoras honestas vale más que una arquitectura perfecta.
{: .text-justify}

---

## Referencias

[^bush]: Vannevar Bush, «As We May Think», *The Atlantic*, julio de 1945. <https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/>

[^extended-mind]: Andy Clark y David Chalmers, «The Extended Mind», *Analysis* 58, n.º 1 (1998): 7-19. <https://doi.org/10.1111/1467-8284.00096>

[^rag]: Patrick Lewis et al., «Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks», *Advances in Neural Information Processing Systems* 33 (2020). <https://arxiv.org/abs/2005.11401>

[^bge-m3]: Jianlv Chen et al., «BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation», 2024. <https://arxiv.org/abs/2402.03216>

[^ollama-embed]: Ollama, «Generate embeddings», documentación de `/api/embed`, consultada el 23 de julio de 2026. <https://docs.ollama.com/api/embed>

[^qdrant-vectors]: Qdrant, «Vectors», documentación sobre named vectors y sparse vectors, consultada el 23 de julio de 2026. <https://qdrant.tech/documentation/manage-data/vectors/>

[^qdrant-bm25]: Qdrant, «Full-Text Search: BM25», documentación sobre BM25 y sparse vectors, consultada el 23 de julio de 2026. <https://qdrant.tech/documentation/search/text-search/full-text-search/>

[^bm25]: Stephen Robertson y Hugo Zaragoza, «The Probabilistic Relevance Framework: BM25 and Beyond», *Foundations and Trends in Information Retrieval* 3, n.º 4 (2009): 333-389. <https://doi.org/10.1561/1500000019>

[^beir]: Nandan Thakur et al., «BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models», 2021. <https://arxiv.org/abs/2104.08663>
