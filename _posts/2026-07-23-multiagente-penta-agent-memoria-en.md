---
layout: single
title: "Multi-agent work in three spoonfuls II: auditable memory"
subtitle: "From handoffs to shared retrieval: what I implemented, how I measured it, and what still needs validation"
date: 2026-07-23 00:00:00 +0000
last_modified_at: 2026-07-24 00:00:00 +0000
categories: [ai, productivity, development, multi-agent]
tags: [multi-agent, rag, embeddings, agent-memory, qdrant, bm25, mcp, context-engineering, arch-linux]
description: "The second penta-agent log: how I turned operational memory into a testable mechanism, what architecture actually shipped, and how I avoided treating a plausible match as evidence."
excerpt: "I already had handoffs and decisions. The next step was to prove what the system retrieved, with which architecture, and when it had to admit it lacked enough evidence."
author: clabra
lang: en
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

In the [first post]({{ "/ia/productividad/desarrollo/multiagente-penta-agent-modelos/" | relative_url }}) I described how I organized `penta-agent`: Codex executes, Claude reviews, other agents enter in bounded ways, and the human keeps closure authority. I also argued that operational memory should not depend on a single conversation or be confused with the vector index.
{: .text-justify}

By the time I closed that first post, I already had continuity mechanisms: handoffs, routing rules, append-only logs, experiential memory in JSONL/YAML, a rebuildable vector collection, and the `recall-context` skill. My problem was not absolute amnesia. It was that I still could not prove what the system retrieved, when it confused a coincidence with evidence, and when it should admit that it did not have an answer.
{: .text-justify}

This second part, then, is not about inventing memory from scratch. It is about turning still-fragile operational continuity into a **traceable, testable, and rebuildable** mechanism.
{: .text-justify}

The idea of an external working memory is not new. It echoes Bush's old ambition of augmenting recall through a personal archive and the extended-mind intuition that notes and tools can become part of cognition.[^bush][^extended-mind] My claim here is narrower: local traces are useful only if I can retrieve them with provenance and audit how they were used.
{: .text-justify}

## Spoonful 1: the problem was not storing, but retrieving well

Storing information is easy. The difficult part, I think, is retrieving the right piece when there are successive decisions, similar names, contradictory versions, and explanations spread across several files.
{: .text-justify}

To organize that "memory" in my own setup, I separated its operational layers:
{: .text-justify}

{: .table-caption}
**Table 1** - System memory layers

| Layer | Question it answers | Effective implementation |
|---|---|---|
| Canonical record | What happened, and what was decided? | `memory/experience-events.jsonl`, `memory/experience-lessons.yaml`, `memory/interaction-metrics.jsonl`, and curated `context` events. |
| Retrieval index | Where is the relevant evidence? | Qdrant with `penta_context_v2` for curated context and `penta_experience_v1` for operational memory; both are derived. |
| Episodic history | How did a session unfold? | Selected Markdown handoffs, compact context events, and operational logs; full sessions are not indexed raw. |
| Working context | What context do I need to provide now? | MCP `experience-memory` (`experience_status`, `recall_experience`) consumed by the `recall-context` skill. |

The distinction matters. A retrieved result is not yet a verified decision. It is a clue that must preserve provenance, date, and a link to its source. In the current contract, local JSONL/YAML files are the source of truth; Qdrant is rebuilt from them. If the index contradicts a current file, the file wins, and the right fix is to reindex or correct ingestion, not to publish vector proximity as if it were final evidence.
{: .text-justify}

The actual flow ended up like this:
{: .text-justify}

<figure class="align-center memory-flow-figure">
  <img src="{{ '/assets/images/multiagente-penta-agent-memoria/flujo-memoria-penta-agent-en.svg' | relative_url }}" alt="Flow diagram of penta-agent memory: curated traces, selective ingestion, canonical source, embeddings and BM25 representation, derived Qdrant index, hybrid retrieval, MCP, and use by Codex, Claude, or Gemini with human closure." loading="lazy" decoding="async">
  <figcaption><strong>Figure 1</strong> - Operational flow of the auditable memory in <code>penta-agent</code>. Note: local JSONL/YAML files are the source of truth; Qdrant and BM25 are derived retrieval indexes, not final evidence.</figcaption>
</figure>

### RAG, without turning it into magic

A language model stores part of what it learned during training in its parameters. That memory does not necessarily include what I decided yesterday in a local repository. Retrieval-Augmented Generation, or RAG, adds an external memory: before answering, a retriever searches for relevant passages and gives them to the generative model as context.[^rag]
{: .text-justify}

In my implementation, `experience-memory` acts as the retriever: it queries Qdrant, fuses signals with the canonical records, and returns candidates through MCP. Codex, Claude, or Gemini then use that context according to the workflow. That is why I prefer to describe this as **retrieval-augmented agents** rather than as an "autonomous RAG": storing and ordering fragments is not the same as reasoning over them.
{: .text-justify}

### Searching by meaning and by words

Semantic search transforms each fragment into a vector. The query is represented with the same model and then compared by orientation through cosine similarity:
{: .text-justify}

$$
\operatorname{sim}(q,d)=
\frac{\mathbf{q}\cdot\mathbf{d}}
{\lVert\mathbf{q}\rVert\,\lVert\mathbf{d}\rVert}
$$

If the query and the document point in similar directions, their similarity increases. This makes it possible to find paraphrases even when they do not share the exact same words.
{: .text-justify}

Lexical search covers the complementary problem: identifiers, acronyms, paths, proper names, and exact terms. BM25 does more than count matches; it weighs term rarity and frequency, saturates repetitions, and partially adjusts for document length.[^bm25]
{: .text-justify}

Today I combine five signals:
{: .text-justify}

- dense search in Qdrant with `bge-m3` embeddings;
- lexical fallback over canonical `context` events;
- BM25 sparse vector with `Qdrant/bm25`;
- event recency;
- lifecycle type: `outcome`, `review`, `decision`, or `handoff`.

I still do not use RRF in the evaluated version. The active fusion is a weighted formula in `hybrid_context_hits`: when there is a semantic signal, it assigns 0.60 to dense similarity, 0.28 to lexical evidence, 0.07 to recency, and 0.05 to lifecycle type. When there is no semantic signal, the fallback mostly weights lexical evidence. BM25 contributes as an additional reordering signal, but it is not enough by itself to rescue a result.
{: .text-justify}

One less flashy virtue is still missing: teaching the system to stay quiet. A query with no answer in the corpus should not receive a fragment only because it looks nearby. In this version I measure **retriever rejection**: a candidate qualifies if it passes any of these criteria in the gate run, `lexical_score >= 0.34`, `semantic_score >= 0.44`, or `hybrid_score >= 0.61`. I still do not have an automated abstention metric for the final generator. If a model receives context and invents anyway, this evaluation will not catch it.
{: .text-justify}

## Spoonful 2: from a useful index to evaluated retrieval

What I left working uses these pieces, verified against the local repo and active services:
{: .text-justify}

{: .table-caption}
**Table 2** - Active components

| Function | Component | Verified configuration |
|---|---|---|
| Canonical source | `memory/*.jsonl` and `memory/*.yaml` | Rebuildable local records; at review time, `experience-events.jsonl` had 1,829 lines and `interaction-metrics.jsonl` had 904. |
| Dense vectorization | Ollama + `bge-m3:latest` | `bert` model, 566.70M parameters, F16, 8192 context, 1024-dimensional embeddings. |
| Vector database | Local Qdrant | Collections `penta_context_v2` and `penta_experience_v1`; the MCP reported `green` status, 14 canonical contexts, and 1,769 operational points. |
| Lexical retrieval | Canonical JSONL + FastEmbed BM25 | `context_fallback_hits` computes lexical matching; `SparseTextEmbedding("Qdrant/bm25")` feeds the `bm25` sparse vector. |
| Fusion | `hybrid_context_hits` | Fuses dense, lexical, BM25, recency, and lifecycle signals; deduplicates by `handoff_id` or `source_document`. |
| Reranking | Not active in the published run | An opt-in reranker exists with `PENTA_AGENT_RERANK=1`, but the validated gate does not use it. |
| Agent interface | MCP `experience-memory` | `experience_status` and `recall_experience`; the `recall-context` skill uses it as its primary path. |
| Test automation | `evaluate_context_retrieval.py` and `rag_regression_gate.py` | The `penta-agent-rag-gate.timer` is enabled weekly; the gate records history in `memory/retrieval-metrics.jsonl`. |

I run this on a local Arch Linux/KDE workstation. Ollama and Qdrant are queried over loopback; the timers are `systemd --user` timers. That detail is not cosmetic: if I isolate the canonical fallback or the gate environment is missing, retrieval changes materially. That is why the gate service explicitly sets `PENTA_AGENT_EMBED_BACKEND=ollama`, `PENTA_AGENT_OLLAMA_MODEL=bge-m3`, and `PENTA_AGENT_CONTEXT_SEM_THRESHOLD=0.44`.
{: .text-justify}

### The embedding model I actually used

BGE-M3, in its original implementation, supports dense, sparse, and multivector representations, works with more than one hundred languages, and accepts long sequences.[^bge-m3] But those model capabilities do not prove that all of them are exposed in my stack.
{: .text-justify}

I use `bge-m3:latest`, served by Ollama through `/api/embed`.[^ollama-embed] In practice I use **only the dense representation** returned by Ollama: 1024-dimensional vectors in the local installation. The sparse branch of the system does not come from BGE-M3; it comes from BM25 with FastEmbed and Qdrant.[^qdrant-vectors][^qdrant-bm25] Pooling, tokenization, and normalization are encapsulated in the Ollama runtime, not in custom repo code.
{: .text-justify}

I also did not chunk the whole workspace indiscriminately. The `context` ingestion works with selected documents: sanitized Markdown handoffs and compact events. When importing handoffs, the extractor takes sections such as goal/context, decision, and outcome; compacts them; preserves `source_document`, `source_hash`, `source_type`, `handoff_id`, `workspace_entry`, `repo_scope`, branch, and date; and limits text to short fields. I do not dump full conversations or raw private files into the index.
{: .text-justify}

### A question set that makes the system uncomfortable

I evaluated with a local golden set of 40 questions: 32 positives and 8 negatives. Positive cases point to expected documents through suffixes relative to the workspace; the evaluator does not open or emit the source content. Difficulty labels are not mutually exclusive: there are 10 exact-keyword cases, 9 paraphrase cases, 7 cross-language cases, 3 colloquial cases, and 4 multi-document cases. Negatives include cooking, sports, finance, science, and unrelated technology queries.
{: .text-justify}

I annotated expected answers manually against selected handoffs and relative paths. That makes the set useful for development and regression, not as an independent benchmark. If I use the same file to calibrate thresholds and then celebrate the result, I cannot treat it as independent evidence.
{: .text-justify}

### Results: what happened in the validated run

The traceable run was:
{: .text-justify}

```bash
env PENTA_AGENT_EMBED_BACKEND=ollama \
    PENTA_AGENT_OLLAMA_MODEL=bge-m3 \
    PENTA_AGENT_CONTEXT_SEM_THRESHOLD=0.44 \
    /opt/entornos/mamba312/bin/python scripts/evaluate_context_retrieval.py --strict
```

I ran it in strict mode, and it exited with code 1 because there was one partial case. The gate itself passed because it evaluates aggregate thresholds: minimum recall 0.95, minimum MRR 0.85, minimum precision 0.40, and perfect negative abstention.
{: .text-justify}

{: .table-caption}
**Table 3** - Validated local result

| Configuration | Recall@5 | MRR | Precision@5 | Negative rejection | Latency |
|---|---:|---:|---:|---:|---:|
| `bge-m3` + dense Qdrant + lexical JSONL + sparse BM25 | 0.9896 | 0.9479 | 0.4448 | 8/8 | p50 401 ms; max 4,250 ms |

My cautious reading is:
{: .text-justify}

1. The active retrieval setup finds almost all annotated evidence in this small, curated corpus.
2. The negative cases are the strongest result: all eight were rejected.
3. Precision@5 is low by design: I prefer bringing extra context over missing the expected document.
4. The remaining error is multi-document: `catastro_multi_sii` recovered part of the expected evidence, not all of it.
5. The metric does not prove that the final answer is faithful; it only proves that the retriever brought or rejected candidates.

I also found a practical signal: when I isolate the canonical fallback without Qdrant, aggregate recall drops to 0.8177. That is not the result of the chosen stack; it is the comparison I needed to understand how much semantic retrieval contributes and why the evaluation configuration must be explicit.
{: .text-justify}

### Fusion and reranking

I do not compare raw scores from different models as if they lived on the same scale. First I gather candidates from dense Qdrant, lexical JSONL, and sparse BM25. Then I compute a hybrid score with admission thresholds. After that I deduplicate by lifecycle: if an `outcome` and a pending handoff share the same `handoff_id`, the completed result wins.
{: .text-justify}

### A regression gate

I can run the evaluation by hand, and I also installed it as a weekly user timer: `penta-agent-rag-gate.timer`, with `OnCalendar=weekly`, `Persistent=true`, and a randomized delay of up to 30 minutes. The service runs `scripts/rag_regression_gate.py` with Ollama, `bge-m3`, and semantic threshold 0.44. It records aggregate metrics in `memory/retrieval-metrics.jsonl` and fails if they fall below the configured thresholds.
{: .text-justify}

I call it a **regression gate** because it checks known cases. Detecting real drift requires observing changes in queries, documents, versions, or score distributions.
{: .text-justify}

## Spoonful 3: what this memory still does not solve

The memory now retrieves better, but it still has clear limits: it does not handle document validity over time very well, it does not detect contradictions in a general way, it does not turn full sessions into permanent memory, and it still fails on some answers that require combining several sources.
{: .text-justify}

I also do not yet evaluate the faithfulness of the final answer. Recall, MRR, and precision indicate whether the right evidence appeared, not whether Claude or Codex interpreted it correctly, respected its validity, or knew when to abstain. Benchmarks such as BEIR also show that no retriever dominates uniformly across all domains.[^beir]
{: .text-justify}

Next, I want to compare each layer of the system reproducibly: dense search, lexical JSONL, BM25, hybrid retrieval, RRF, and opt-in reranking. After that I want to add document-validity handling and answer evaluation with citations, so I can measure not only whether I retrieve evidence, but whether the answer uses it faithfully.
{: .text-justify}

If you are building something similar - a multi-agent setup, a local RAG, a second brain, or working memory to avoid repeating context - I would like to read what worked for you, where it failed, and how you decided when to abstain. That comparison between honest logs is worth more than a perfect architecture.
{: .text-justify}

---

## References

[^bush]: Vannevar Bush, "As We May Think", *The Atlantic*, July 1945. <https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/>

[^extended-mind]: Andy Clark and David Chalmers, "The Extended Mind", *Analysis* 58, no. 1 (1998): 7-19. <https://doi.org/10.1111/1467-8284.00096>

[^rag]: Patrick Lewis et al., "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks", *Advances in Neural Information Processing Systems* 33 (2020). <https://arxiv.org/abs/2005.11401>

[^bge-m3]: Jianlv Chen et al., "BGE M3-Embedding: Multi-Lingual, Multi-Functionality, Multi-Granularity Text Embeddings Through Self-Knowledge Distillation", 2024. <https://arxiv.org/abs/2402.03216>

[^ollama-embed]: Ollama, "Generate embeddings", `/api/embed` documentation, accessed July 23, 2026. <https://docs.ollama.com/api/embed>

[^qdrant-vectors]: Qdrant, "Vectors", documentation on named vectors and sparse vectors, accessed July 23, 2026. <https://qdrant.tech/documentation/manage-data/vectors/>

[^qdrant-bm25]: Qdrant, "Full-Text Search: BM25", documentation on BM25 and sparse vectors, accessed July 23, 2026. <https://qdrant.tech/documentation/search/text-search/full-text-search/>

[^bm25]: Stephen Robertson and Hugo Zaragoza, "The Probabilistic Relevance Framework: BM25 and Beyond", *Foundations and Trends in Information Retrieval* 3, no. 4 (2009): 333-389. <https://doi.org/10.1561/1500000019>

[^beir]: Nandan Thakur et al., "BEIR: A Heterogeneous Benchmark for Zero-shot Evaluation of Information Retrieval Models", 2021. <https://arxiv.org/abs/2104.08663>
