---
layout: single
title: "Multiagentes en 3 cucharadas II: una memoria que se puede auditar"
subtitle: "De los handoffs a una recuperación compartida: qué está implementado, cómo se mide y qué falta validar"
date: 2026-07-23 00:00:00 +0000
last_modified_at: 2026-07-23 00:00:00 +0000
categories: [ia, productividad, desarrollo, multiagente]
tags: [multiagente, rag, embeddings, memoria-agentes, qdrant, bm25, mcp, context-engineering, arch-linux]
description: "Segunda bitácora de penta-agent: cómo evolucionó su memoria operativa, qué arquitectura está realmente implementada y cómo evaluar la recuperación sin confundir una coincidencia plausible con evidencia."
excerpt: "El sistema ya conservaba handoffs y decisiones. El paso siguiente fue comprobar qué recuperaba, con qué arquitectura y cuándo debía reconocer que no tenía evidencia suficiente."
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

Al cerrar esa primera publicación ya existían mecanismos de continuidad: handoffs, reglas de routing, bitácoras append-only, una memoria experiencial en JSONL/YAML, una colección vectorial reconstruible y la skill `recall-context`. El problema no era una amnesia absoluta. Era menos vistoso y bastante más peligroso: no estaba suficientemente demostrado qué recuperaba el sistema, cuándo confundía una coincidencia con evidencia y cuándo debía reconocer que no tenía respuesta.
{: .text-justify}

Esta segunda parte no trata, por tanto, de inventar una memoria desde cero. Trata de convertir una continuidad operativa todavía frágil en un mecanismo **trazable, evaluable y reconstruible**.
{: .text-justify}

## Cucharada 1: el problema no era guardar, sino recuperar bien

Guardar información es fácil. Lo difícil es recuperar la pieza correcta cuando existen decisiones sucesivas, nombres parecidos, versiones contradictorias y explicaciones repartidas entre varios archivos.
{: .text-justify}

Para no llamar «memoria» a cualquier cosa, separé sus capas operativas:
{: .text-justify}

{: .table-caption}
**Tabla 1** — Capas de memoria del sistema

| Capa | Pregunta que responde | Implementación efectiva |
|---|---|---|
| Registro canónico | ¿Qué ocurrió y qué se decidió? | `memory/experience-events.jsonl`, `memory/experience-lessons.yaml`, `memory/interaction-metrics.jsonl` y eventos `context` curados. |
| Índice de recuperación | ¿Dónde está la evidencia pertinente? | Qdrant con `penta_context_v2` para contexto curado y `penta_experience_v1` para memoria operacional; ambos son derivados. |
| Historial episódico | ¿Cómo se desarrolló una sesión? | Handoffs Markdown seleccionados, eventos compactos de contexto y logs operacionales; las sesiones completas no se indexan crudas. |
| Contexto de trabajo | ¿Qué necesita saber el agente ahora? | MCP `experience-memory` (`experience_status`, `recall_experience`) consumido por la skill `recall-context`. |

La distinción importa. Un resultado recuperado no es todavía una decisión comprobada. Es una pista que debe conservar procedencia, fecha y vínculo con su fuente. En el contrato actual, los JSONL/YAML locales son la fuente de verdad; Qdrant se reconstruye desde ellos. Si el índice contradice un archivo vigente, gana el archivo y corresponde reindexar o corregir la ingesta, no publicar la vecindad vectorial como si fuera evidencia final.
{: .text-justify}

El flujo real quedó así:

```text
handoffs curados + eventos de hooks + métricas locales
        |
record-context / import-context-handoffs
        |
saneamiento, compactación y metadatos de procedencia
        |
experience-events.jsonl + curated-context-manifest.jsonl
        |
Ollama /api/embed con bge-m3  +  FastEmbed Qdrant/bm25
        |
Qdrant: penta_context_v2 y penta_experience_v1
        |
hybrid_context_hits: denso + JSONL léxico + BM25 + recencia + ciclo de vida
        |
MCP experience-memory / skill recall-context
        |
Codex, Claude o Gemini reciben contexto; el humano conserva el cierre
```

### RAG, sin convertirlo en magia

Un modelo de lenguaje guarda parte de lo aprendido durante el entrenamiento en sus parámetros. Esa memoria no incluye necesariamente lo que decidí ayer en un repositorio local. La *Retrieval-Augmented Generation* o RAG agrega una memoria externa: antes de responder, un recuperador busca pasajes pertinentes y se los entrega al modelo generativo como contexto.[^rag]
{: .text-justify}

En esta implementación, el recuperador es `experience-memory`: consulta Qdrant, fusiona señales con los registros canónicos y entrega candidatos mediante MCP. La respuesta final la genera el agente activo —Codex, Claude o Gemini según el flujo— usando ese contexto. Por eso prefiero describirlo como **recuperación aumentada para agentes** antes que como un «RAG autónomo»: almacenar y ordenar fragmentos no equivale a razonar sobre ellos.
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

El sistema actual combina cinco señales:
{: .text-justify}

- búsqueda densa en Qdrant con embeddings de `bge-m3`;
- fallback léxico sobre los eventos canónicos `context`;
- vector sparse BM25 con `Qdrant/bm25`;
- recencia del evento;
- tipo de ciclo de vida: `outcome`, `review`, `decision` o `handoff`.

No usa RRF en la versión evaluada. La fusión es una fórmula ponderada en `hybrid_context_hits`: cuando hay señal semántica, pesa 0,60 para similitud densa, 0,28 para léxico, 0,07 para recencia y 0,05 para ciclo de vida. Cuando no hay señal semántica, el fallback pesa principalmente el léxico. BM25 suma como reordenamiento adicional, pero no basta por sí solo para rescatar un resultado.
{: .text-justify}

Falta una virtud menos vistosa: saber callarse. Una consulta sin respuesta en el corpus no debería recibir un fragmento solo porque parece cercano. En esta versión se mide **rechazo del recuperador**: un candidato califica si supera alguno de estos criterios en la corrida del gate, `lexical_score >= 0.34`, `semantic_score >= 0.44` o `hybrid_score >= 0.61`. No hay todavía una métrica automatizada de abstención del generador final. Si un modelo recibe contexto y aun así inventa, esta evaluación no lo detecta.
{: .text-justify}

## Cucharada 2: de un índice útil a una recuperación evaluada

La implementación efectiva usa estas piezas, verificadas el 23 de julio de 2026 contra el repo local y los servicios activos:
{: .text-justify}

{: .table-caption}
**Tabla 2** — Componentes activos

| Función | Componente | Configuración comprobada |
|---|---|---|
| Fuente canónica | `memory/*.jsonl` y `memory/*.yaml` | Registros locales regenerables; al revisar había 1.829 líneas en `experience-events.jsonl` y 904 en `interaction-metrics.jsonl`. |
| Vectorización densa | Ollama + `bge-m3:latest` | Modelo `bert`, 566,70M parámetros, F16, contexto 8192, embedding 1024, digest local `790764642607...`. |
| Base vectorial | Qdrant local | Colecciones `penta_context_v2` y `penta_experience_v1`; el MCP reportó estado `green`, 14 contextos canónicos y 1.769 puntos operacionales. |
| Recuperación léxica | JSONL canónico + FastEmbed BM25 | `context_fallback_hits` calcula coincidencia léxica; `SparseTextEmbedding("Qdrant/bm25")` alimenta el vector sparse `bm25`. |
| Fusión | `hybrid_context_hits` | Fusiona denso, léxico, BM25, recencia y ciclo de vida; deduplica por `handoff_id` o `source_document`. |
| Reranking | No activo en la corrida publicada | Existe un reranker opt-in con `PENTA_AGENT_RERANK=1`, pero el gate validado no lo usa. |
| Interfaz para agentes | MCP `experience-memory` | `experience_status` y `recall_experience`; la skill `recall-context` lo usa como ruta primaria. |
| Automatización de pruebas | `evaluate_context_retrieval.py` y `rag_regression_gate.py` | El timer `penta-agent-rag-gate.timer` está habilitado semanalmente; el gate registra histórico en `memory/retrieval-metrics.jsonl`. |

Todo corre en una estación local con Arch Linux/KDE. Ollama y Qdrant se consultan por loopback; los timers son de `systemd --user`. Ese detalle no es cosmético: si el sandbox bloquea sockets locales o falta el entorno del gate, la recuperación puede degradar a vector hash. Por eso el servicio del gate fija explícitamente `PENTA_AGENT_EMBED_BACKEND=ollama`, `PENTA_AGENT_OLLAMA_MODEL=bge-m3` y `PENTA_AGENT_CONTEXT_SEM_THRESHOLD=0.44`.
{: .text-justify}

### El modelo de embeddings realmente usado

El modelo BGE-M3, en su implementación original, admite representaciones densas, dispersas y multivectoriales, trabaja con más de cien idiomas y acepta secuencias extensas.[^bge-m3] Pero esas capacidades del modelo no prueban que todas estén expuestas en mi *stack*.
{: .text-justify}

El embedding activo es `bge-m3:latest`, servido por Ollama mediante `/api/embed`.[^ollama-embed] En la práctica se usa **solo la representación densa** que entrega Ollama: vectores de 1024 dimensiones en la instalación local. La rama sparse del sistema no viene de BGE-M3; viene de BM25 con FastEmbed y Qdrant.[^qdrant-vectors][^qdrant-bm25] Pooling, tokenización y normalización quedan encapsulados en el runtime de Ollama, no en código propio del repo.
{: .text-justify}

Tampoco hay una fragmentación general de todo el workspace. La ingesta `context` trabaja con documentos seleccionados: handoffs Markdown saneados y eventos compactos. Al importar handoffs, el extractor toma secciones como objetivo/contexto, decisión y resultado, las compacta, conserva `source_document`, `source_hash`, `source_type`, `handoff_id`, `workspace_entry`, `repo_scope`, rama y fecha, y limita los textos a campos cortos. No vuelca conversaciones completas ni archivos privados en bruto.
{: .text-justify}

### Un conjunto de preguntas que incomode al sistema

La evaluación usa un golden set local de 40 preguntas: 32 positivas y 8 negativas. Las positivas apuntan a documentos esperados mediante sufijos relativos al workspace; el evaluador no abre ni emite el contenido fuente. Las etiquetas de dificultad no son mutuamente excluyentes: hay 10 casos de keyword exacto, 9 de paráfrasis, 7 entre idiomas, 3 coloquiales y 4 multi-documento. Los negativos incluyen consultas de cocina, deportes, finanzas, ciencia y tecnología no relacionada.
{: .text-justify}

Las respuestas esperadas fueron anotadas manualmente contra handoffs seleccionados y rutas relativas. Eso lo hace útil como conjunto de desarrollo y regresión, no como benchmark independiente. Si uso el mismo archivo para calibrar umbrales y luego celebrar el resultado, no puedo fingir independencia estadística.
{: .text-justify}

### Resultados: lo que pasó en la corrida validada

La corrida trazable fue:
{: .text-justify}

```bash
env PENTA_AGENT_EMBED_BACKEND=ollama \
    PENTA_AGENT_OLLAMA_MODEL=bge-m3 \
    PENTA_AGENT_CONTEXT_SEM_THRESHOLD=0.44 \
    /opt/entornos/mamba312/bin/python scripts/evaluate_context_retrieval.py --strict
```

El modo estricto salió con código 1 porque hubo un caso parcial. El gate, en cambio, pasó porque evalúa umbrales agregados: recall mínimo 0,95, MRR mínimo 0,85, precisión mínima 0,40 y abstención negativa perfecta.
{: .text-justify}

{: .table-caption}
**Tabla 3** — Resultado local validado

| Configuración | Recall@5 | MRR | Precision@5 | Rechazo de negativos | Latencia |
|---|---:|---:|---:|---:|---:|
| `bge-m3` + Qdrant denso + JSONL léxico + BM25 sparse | 0,9896 | 0,9479 | 0,4448 | 8/8 | p50 401 ms; máximo 4.250 ms |

La lectura prudente es:
{: .text-justify}

1. La recuperación actual encuentra casi toda la evidencia anotada en este corpus chico y curado.
2. Los negativos son el mejor resultado: ocho de ocho fueron rechazados.
3. La precisión@5 es baja a propósito: el sistema prefiere traer contexto de más antes que perder el documento esperado.
4. El error que queda es multi-documento: `catastro_multi_sii` recuperó parte, no toda, la evidencia esperada.
5. La métrica no prueba que la respuesta final sea fiel; prueba solo que el recuperador trajo o rechazó candidatos.

También apareció un hallazgo práctico: ejecutar el evaluador sin el entorno del gate puede degradar a hash y bajar el recall agregado a 0,8177. Ese no es un resultado del stack elegido, sino una señal de que la configuración de evaluación debe ser explícita.
{: .text-justify}

### Fusión y reranking, sin venderlos como otra cosa

La fusión actual no compara puntajes crudos de modelos distintos como si fueran la misma escala. Primero reúne candidatos desde Qdrant denso, JSONL léxico y BM25 sparse. Luego calcula un puntaje híbrido con umbrales de admisión. Después deduplica por ciclo de vida: si existe un `outcome` y un handoff pendiente con el mismo `handoff_id`, el resultado completo gana.
{: .text-justify}

Hay código para reordenar candidatos con `jinaai/jina-reranker-v2-base-multilingual`, pero está detrás de `PENTA_AGENT_RERANK=1`. No formó parte del gate publicado, así que no lo cuento como componente activo ni atribuyo mejoras al reranking.
{: .text-justify}

### Un gate de regresión

La evaluación se ejecuta manualmente y también está instalada como timer semanal de usuario: `penta-agent-rag-gate.timer`, con `OnCalendar=weekly`, `Persistent=true` y retardo aleatorio de hasta 30 minutos. El servicio ejecuta `scripts/rag_regression_gate.py` con Ollama, `bge-m3` y umbral semántico 0,44. Registra métricas agregadas en `memory/retrieval-metrics.jsonl` y falla si cae bajo los umbrales configurados.
{: .text-justify}

Debe llamarse **gate de regresión** porque comprueba casos conocidos. Detectar deriva de verdad exige observar cambios en consultas, documentos, versiones o distribuciones de puntajes. Un RAG sin pruebas difíciles no necesariamente funciona bien. A veces solo funciona sin testigos.
{: .text-justify}

## Cucharada 3: lo que esta memoria todavía no resuelve

El índice puede recuperar mejor sin convertirse en un «segundo yo». Esa metáfora ayuda a presentar la intuición —Bush imaginó el *memex* y Clark y Chalmers discutieron una mente extendida mediante herramientas externas—, pero no debe tomarse literalmente.[^bush][^extended-mind]
{: .text-justify}

El sistema conserva documentos, calcula similitudes, ordena candidatos y entrega evidencia a modelos que todavía pueden interpretarla mal.
{: .text-justify}

### 1. Vigencia temporal

Hay fechas, recencia y estados `stale` para lecciones operacionales. También hay deduplicación por `handoff_id` y preferencia por `outcome`. Lo que no existe todavía es una relación semántica general de «este documento reemplaza a este otro» ni una política completa para retirar conocimiento obsoleto cuando cambia una decisión.
{: .text-justify}

### 2. Contradicciones

El sistema puede contar lecciones contradictorias en el tablero y puede preferir evidencia más reciente o más completa en casos simples. No hay, sin embargo, un detector de contradicciones entre documentos curados ni una resolución automática de conflictos. Si dos handoffs dicen cosas opuestas y no comparten identidad, todavía hace falta revisión humana.
{: .text-justify}

### 3. Sesiones completas

Las sesiones completas no se ingieren crudas. Se preservan handoffs, eventos compactos, métricas y lecciones derivadas. La skill `recall-context` puede buscar sesiones de Claude o Codex como fallback para evidencia exacta, pero eso no convierte cada conversación en memoria semántica permanente. Es una decisión deliberada de privacidad y ruido: antes de indexar, hay que destilar.
{: .text-justify}

### 4. Respuestas que requieren varios documentos

El gold set ya incluye casos multi-documento, y eso fue útil porque dejó un fallo visible. La arquitectura puede devolver varios documentos, pero todavía no garantiza una síntesis multi-hop completa. El caso parcial muestra el límite: recuperar algo correcto no basta cuando la respuesta depende de varias piezas.
{: .text-justify}

### 5. Evaluación de la respuesta final

Recall, MRR y precisión evalúan recuperación, no verdad. El nivel siguiente consiste en medir si el generador:

- cita el fragmento correcto;
- distingue evidencia de inferencia;
- respeta la versión vigente;
- se abstiene cuando el contexto no basta;
- evita contradecir o deformar la fuente.

Actualmente esa capa está pendiente como evaluación automatizada. Hay revisión humana y roles de reviewer en el flujo multiagente, pero no un juez de fidelidad de respuestas finales. Benchmarks como BEIR muestran además que ningún recuperador domina de forma uniforme en todos los dominios.[^beir] Un corpus personal, pequeño y curado no autoriza a generalizar resultados a repositorios institucionales o heterogéneos.
{: .text-justify}

### Lo que sigue

Los próximos pasos comprobables son:

1. Corregir el modo `--skip-qdrant` del evaluador para que mida realmente el fallback canónico sin consulta semántica. Termina cuando el resumen reporte ese modo sin hits densos.
2. Agregar ablations reproducibles: denso solo, JSONL léxico, BM25, híbrido y reranking opt-in. Termina cuando cada fila salga de una corrida y no de una impresión subjetiva.
3. Incorporar vigencia y fidelidad: metadatos de reemplazo entre contextos y una prueba de respuesta final con citas. Termina cuando una contradicción conocida active abstención o revisión.

La conclusión sigue conectada con la primera entrega. Un multiagente útil no es abrir más chats. Es imponer contratos, permisos, fuentes de verdad, trazas y pruebas. La memoria agrega una regla más: **recuperar no basta; hay que demostrar cuándo la evidencia es pertinente y reconocer cuándo no está**.
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
