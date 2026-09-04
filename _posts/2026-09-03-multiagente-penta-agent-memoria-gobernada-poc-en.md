---
layout: single
title: "Multi-agent work in three spoonfuls III: a memory that leaves traces"
subtitle: "From auditable RAG to governed memory: why it still is not a digital clone"
date: 2026-09-03 00:00:00 -0400
last_modified_at: 2026-09-03 00:00:00 -0400
categories: [ai, productivity, development, multi-agent]
tags: [multi-agent, rag, agent-memory, provenance, privacy, governance, knowledge-graph, rag-evaluation, threejs]
description: "Third penta-agent log: provenance, currency, evaluation, and a sanitized 3D projection of its operational memory."
excerpt: "The system already retrieves and visualizes traces. The problem now is governing what persists, what expires, and what must never leave its scope."
author: clabra
lang: en
ref: multiagente-penta-agent-memoria-gobernada-poc
permalink: /ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/
distribution:
  social: true
  republish: []
repo: https://github.com/tatanlabra/penta-agent
entorno: "Arch Linux, KDE Plasma, local services (Qdrant and Sentence Transformers over loopback, systemd --user timers), Qdrant with the named `dense` vector"
en_abstract: >
  Third log of a local multi-agent setup. The previous entry made its shared
  memory measurable; this one asks a harder question: what should persist,
  what should expire, and what must never leave its scope. Four sources are
  kept apart by contract rather than merged — curated operational memory,
  a private and reversible personal-mail pilot, authorized process metadata
  from a thesis project, and the sanitized public projection built from them.
  A frozen 319-context staging collection, embedded with Qwen3-Embedding-0.6B
  on CPU, was used to test five retrieval changes against 40 queries with 8
  negatives; only one was promoted (dropping the BM25 boost from 0.10 to 0.00,
  38 complete / 2 partial / 0 failed, recall@5 0.9635, MRR 0.8396). A reranker
  scored better on MRR (0.9010) and was still rejected: median latency went
  from 2.37 s to 15.83 s, with a 91.10 s worst case. The 3D viewer is a static,
  regenerable export with a text fallback — a map of recorded strategies, not
  a mind. What this does not show is equally explicit: retrieval quality is not
  answer fidelity, two multi-source cases remain partial, and none of this
  amounts to a digital clone.
math: false
published: true
toc: true
toc_sticky: true
comments: true
author_profile: true
header:
  teaser: /assets/images/teasers/teaser-multiagentes-memoria-gobernada.webp
  og_image: /assets/images/multiagente-penta-agent-memoria-gobernada/og-memoria-gobernada-1200x630.webp
  og_image_alt: "Four governed sources on separate platforms—operational memory, personal mail sealed under glass, thesis index, and the public projection—with a membrane that lets only three permitted outputs through."
---

> **Status of the demo.** The viewer was regenerated on August 29, 2026 from a sanitized public projection. The artifact contains no mail bodies, attachments, addresses, absolute paths, tokens, credentials, or microdata. The canonical index and the private sources stay off the site.
{: .notice--warning}

> **Reading convention.** **LOCAL FACT** marks a dated measurement, reproducible from the project's own artifacts; **DESIGN INFERENCE**, a conclusion drawn from those measurements; and **UNVERIFIED**, a capability the system does not claim for itself. A count, an edge, or an infrastructure test proves neither understanding, nor identity, nor general answer fidelity.
{: .notice--info}

## Preamble: remembering is not enough

The [second part]({{ "/ia/productividad/desarrollo/multiagente-penta-agent-memoria/" | relative_url }}) went after a narrow problem: getting `penta-agent`'s memory to retrieve evidence and to recognize when it had found none. That piece exists. The question in this third part is less comfortable: **what happens once that memory starts to grow?**

An index can pile up fragments without any trouble. A useful memory, by contrast, has to carry provenance, currency, permissions, contradictions, and deletion criteria. It also has to tell finding a source apart from answering correctly from it. Recent literature insists on separating RAG, context management, and agent memory, because they do different jobs and call for different evaluations (Hu et al. 2025).

This post also corrects two shortcuts from the first draft. The first reduced the system to a handful of decorative nodes: safe, but uninformative. The second confused fidelity with saturation — a graph can be derived from real data and still be an unreadable hairball. The fix is neither to invent an allegory nor to publish every trace, but to build a projection that is bounded, reproducible, and recognizably tied to the evidence.

What follows has three movements: what changed since part II; which experiments survived an evaluation that was allowed to fail; and how to show a memory without passing it off as a mind.

---

## Spoonful 1: from retrieving fragments to governing evidence

In this architecture, RAG retrieves information; the memory layer adds rules for keeping it, updating it, discarding it, and using it again. None of those functions amounts, on its own, to identity. Every source has to travel with its origin, its transformation, its access scope, its currency, and its allowed output. PROV-O supplies an interoperable vocabulary for the provenance half — entities, activities, and agents; permissions and currency need rules of their own (Lebo, Sahoo, and McGuinness 2013).

### What changed since part II

| Open commitment | Evidence added in this version | Limit that stays open |
|---|---|---|
| Compare dense retrieval, lexical retrieval, and reranking without disturbing production. | The `penta_context_qwen3_staging` collection, a frozen cut of 319 contexts, and 40 queries evaluated at `k=5`. | The best run still stands at 38 complete cases and 2 partials; the strict gate stays shut. |
| Evaluate whether an answer uses the retrieved sources and knows when to abstain. | The `context-answer-v1` contract, with 12 positive and 6 negative cases, all sanitized. | The end-to-end test of a local model and the human review of the withheld cases are still unfinished. |
| Add currency without erasing history. | A sandbox that admits `supersedes` only from a later date and rejects competing successors. | There is still no temporal reasoner wired into live memory. |
| Make growth visible without mistaking topology for truth. | A static 3D viewer, regenerable from sanitized JSON, with a text alternative when WebGL is unavailable. | The viewer does not query Qdrant, does not validate edges, and does not represent a mind. |

### What memory actually exists

| Layer | Local cut as of August 29, 2026 | What it supports | What it does not support |
|---|---|---|---|
| `penta-agent` experience | 16,955 indexed points, 1,432 strategies, 3,949 relations, 12 communities, and 8 task families. | Operational traces, semantic neighborhoods, corrections, and failures exist and can be explored. | An edge is not, on its own, a causal relation or a true claim. |
| Curated context | 319 canonical contexts in `penta_context_v2`; the local check returned `green`. | A curated handoff or decision can be retrieved with its provenance. | The index does not replace the canonical record, and it does not cover the whole history. |
| Research process | Public snapshot with 796 derived artifacts, 533 links, and 7 open leads; FTS5 and TF-IDF search. | The thesis work chain can be inspected without publishing documents or microdata. | It proves neither historical execution, nor replication, nor substantive results. |
| Personal mail | Private inventory of 12,072 unique messages, 8,559 duplicates, covering 2011–2026. | Inventory-only reading works within an authorized scope. | Mail is not a public corpus and not a personality model. |
| Local personal memory | Separate prototype with `mbox`, SQLite/FTS, explicit scopes, purge, and synthetic evaluation. | A reversible technical route exists for retrieving private material. | No generative workflow over sensitive mail is authorized. |

Provenance has to record the pipeline's own failures too. The historical exporter expected a plain unnamed vector, while the current index uses the named `dense` vector. The first regeneration produced a degraded graph with no semantic edges. A run against the real index exposed the incompatibility; once the exporter was adapted, 3,658 semantic edges came back. The episode leaves a practical rule: **an auditable visualization has to show when its data chain degraded, why it happened, and how it was put back together**.

### From command to task

The index's atomic unit is still an observed strategy. Many strategies are command-shaped, because that is how the actions were recorded. To make them readable without inventing intent, I added a deterministic classification over strategy, tool, transport, and project.

| Derived task family | Strategies | Question it helps to ask |
|---|---:|---|
| Coordinate agents and decisions | 399 | What was learned while delegating a task or leaving a handoff? |
| Research and analyze data | 396 | Which tactics recur while examining data, thesis material, and sources? |
| Read and trace evidence | 385 | Which antecedents were inspected before deciding? |
| Execute and automate | 118 | Which steps implemented a change that had already been reviewed? |
| Version and compare changes | 76 | Which checks were applied before keeping a modification? |
| Test and verify | 28 | What was actually checked instead of declared done? |
| Operate tools and services | 18 | Which infrastructure enabled or blocked the workflow? |
| Edit and communicate | 12 | What turned technical evidence into documentation or publication? |

This layer is a teaching lens, not an ontology of the author. A strategy can belong to more than one family, but today it lands in the first matching rule. That makes it useful for getting oriented, not for measuring productivity or attributing human capacities to the system.

---

## Spoonful 2: experimenting without blending or promoting

The architecture has layers with different jobs: the ledger and the source files are canonical; Qdrant is a regenerable index; the viewer is a public projection; and the private adapters stay outside Git. That separation is what keeps a vector match from turning, unreviewed, into a durable fact.

### The proof of concept is not a source blender

Mail, thesis material, and operational memory are not interchangeable nodes. At this stage, only the curated context feeds cross-agent retrieval and the public projection. Mail keeps a private, reversible, vetoable route; the thesis contributes authorized process metadata. The arrows in the diagram describe allowed outputs, not automatic transfers or inferences about people. The gap between technical access and a legitimate information flow is exactly the problem contextual integrity is meant to capture (Nissenbaum 2004).

<figure class="align-center">
  <a href="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources.svg' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources.svg' | relative_url }}" alt="Three governed sources: operational memory allows retrieval with provenance; personal mail allows only private, reversible review; thesis material and documents allow citations and verification status. A boundary blocks publishing mail bodies, attachments, addresses, absolute paths, microdata, and inferences about identity." loading="lazy" decoding="async">
  </a>
  <figcaption>Figure 1. The current integration is an architecture of permissions: the source determines its allowed output.</figcaption>
</figure>

The thesis enters this way: as a [public snapshot of the research index]({{ '/assets/data/memoria_gobernada/thesis-research-index-snapshot.json' | relative_url }}), not as an open corpus. The card exposes 796 derived textual artifacts — 316 audits, 244 reports, 133 contracts, 71 pseudocode files, and 32 inventory, replication, or documentation pieces — plus 533 links and 7 open leads. It excludes historical sources, DTA, Parquet, PDF, images, paths, text, and microdata. Its search is lexical; it claims no neural understanding.

It is worth saying what state that snapshot is in, because it is the test case for the argument itself. Its figures belong to the index built on August 29 and are faithful to that cut: the manifest fingerprint matches the published one byte for byte. But the corpus kept growing — it holds 817 documents today, twenty-one more, all from later phases — and the index was not regenerated. The result is that the currency gate is red: `check-research-index` exits 2, with `document_count` and `source_fingerprint` at `false`, and the contract that groups it exits 2 as well.

That does not invalidate the snapshot; it dates it. And that is exactly what a governed memory has to do: not keep the world from changing, but refuse to claim it stayed the same. A gate that had stayed green while the corpus grew by 2.6% would have been worse than no gate at all, because it would have certified as current an artifact that no longer was. The publishable status of this piece is not "verified", it is "dated, with its gate open".
{: .notice--warning}

### What is worth reusing — and under what contract

| Need | Local asset | Project worth a contrast | Adoption rule |
|---|---|---|---|
| Recover decisions across coding sessions | Handoffs, events, and curated context. | [`deja-vu`](https://github.com/vshulcz/deja-vu), which indexes local agent sessions and offers retrieval through CLI and MCP. | It must improve real historical lookups without replacing curated notes with raw transcripts. |
| Keep an agent's state explicit | Evaluated RAG and curated context; not a general execution runtime. | [Letta Code](https://github.com/letta-ai/letta-code), the current harness of the project that grew out of MemGPT (Packer et al. 2023). | Compare its memory blocks and rewrite mechanisms against the existing contracts before adding another runtime. |
| Extract memories from conversations | Ingestion and human curation; private mail with a veto. | [Mem0](https://github.com/mem0ai/mem0) and [Hindsight](https://github.com/vectorize-io/hindsight). | Measure precision, false positives, revocation, and purge on synthetic data before touching real mail. |
| Represent currency and contradiction | A sandbox with `supersedes`. | [Graphiti](https://github.com/getzep/graphiti), the open core of the temporal architecture described by Rasmussen et al. (2025). | Move dated decisions into a pilot without losing source, currency, or human review. |
| Connect concepts, documents, and citations | Allowlisted FTS5/TF-IDF process index. | [Microsoft GraphRAG](https://github.com/microsoft/graphrag) over a bounded scientific corpus (Edge et al. 2024). | Compare cost, traceability, and retrieval against the lexical baseline; start small, because the project is in maintenance mode and its documentation warns about indexing cost. |
| Visualize a reproducible projection | Local generator and sanitized JSON artifact. | [`3d-force-graph`](https://github.com/vasturiano/3d-force-graph), already vendored. | Keep the text alternative, and do not read visual distance as human affinity. |

The priority is not to install everything. It is to try, under the same contract, whatever might cut friction without degrading provenance, privacy, or reversibility. Product descriptions tell you what each project promises; they do not establish that it is better on this corpus. An open core is not enough either: the models, external services, and data flows needed to run it have to be documented.

### A retrieval experiment that was allowed to fail

The `Qwen3-Embedding-0.6B` trial ran through Sentence Transformers on an isolated collection: 319 frozen contexts, 1,024-dimensional vectors, CPU, and 319/319 persisted. It did not touch `penta_context_v2`. The test set kept 40 queries, 8 negatives, and `k=5`; the notation **38/2/0** means 38 complete passes, 2 partials, and no outright miss.

The model card recommends task-specific instructions, but a vendor recommendation is not a substitute for local evaluation. This is what came out (Zhang et al. 2025):

| Hypothesis | Isolated change | Local result | Decision |
|---|---|---|---|
| The lexical component displaces correct dense evidence. | BM25 boost from `0.10` to `0.00`, in `staging` only. | From 36/3/1 to **38/2/0**; all 8/8 negatives kept abstaining; recall@5 0.9635 and MRR 0.8396. | Kept as an experimental starting point; it does not prove an improvement over production. |
| A generic instruction improves citability. | Explicit instruction to favor complete, citable sources. | **33/3/4**; negative abstentions 6/8. | Rejected: it degraded coverage and abstention alike. |
| A reranker recovers complementary sources. | `Qwen3-Reranker-0.6B` over already-admitted candidates. | **38/2/0**; recall@5 0.9688 and MRR 0.9010; median 15.83 s and 91.10 s worst case, against 2.37 s for the base ordering. | Offline analysis only; the cost does not justify promoting it. |
| The repository is a good proxy for the document family. | `repo_scope` diversification within a window of 20. | **38/2/0**; recall@5 0.9740; one partial was resolved and another appeared in a different task. | Rejected: provenance is not document intent. |
| Agreement between two orderings keeps the error from moving. | Reciprocal rank fusion (RRF) of the base and reranked orderings (Cormack, Clarke, and Büttcher 2009). | **38/2/0**; recall@5 0.9635; median 20.06 s. | Rejected: it neither closed the gate nor paid for its cost. |

The two partials are always multi-source cases: the selection cannot cover distinct document families within five positions. Here I have to declare a limit instead of a measurement. The diagnostic that would have located what rank the missing documents landed at never ran: it required an evidence-taxonomy file that does not exist in the repository, and the single attempt was recorded as `failed`. I know the partials exist and which cases they are, because that much is in every run; I do not know how far off they landed, and I am not going to write down a number I cannot reproduce. Raising `k` until a case passes would change the evaluation question, so that is no way out either.

The next hypothesis is harder and less photogenic: human lineage or document-intent metadata, bound to the fingerprint of the cut and of the query, with no access to the gold set while it is being written. Until those labels exist and the strict test stops being red, the collection stays in `staging`.

---

## Spoonful 3: a map that does not pass itself off as a mind

The visualization is generated from a sanitized cut of the experience memory. It queries neither Qdrant nor any external service when it opens: it receives a static, regenerable, auditable artifact. The [public JSON export]({{ '/assets/data/rag_knowledge_graph/public-graph.json' | relative_url }}) makes this run inspectable, and the HTML has to be reproducible from that file without rereading private sources.

> **Guided reading.** The viewer's interface is in Spanish. Open **Tareas** (tasks) first and pick a family — "Investigar y analizar datos", research and analyze data, for instance. Then use **Proy** (projects) to tell where the work happened. Only at the end open **Errores** (errors) or diagnostic mode to inspect a concrete point of friction. The viewer should start from a question, not from a cloud of points.
{: .notice--primary}

<section class="rag-knowledge-graph" aria-labelledby="rag-knowledge-graph-title">
  <div class="rag-knowledge-graph__header">
    <div>
      <p class="rag-knowledge-graph__eyebrow">Public projection · 2026-08-29</p>
      <h3 id="rag-knowledge-graph-title">Map of strategies recorded by penta-agent</h3>
      <p>August 29 cut: 1,432 strategies · 3,949 relations · 8 task families · 16,955 indexed points</p>
    </div>
    <a class="rag-knowledge-graph__open" href="{{ '/assets/visualizations/penta-rag-knowledge-graph/index.html' | relative_url }}" target="_blank" rel="noopener">Open full viewer<span class="screen-reader-text"> in a new tab</span></a>
  </div>
  <iframe class="rag-knowledge-graph__frame" title="Navigable 3D map of penta-agent task families and strategies" src="{{ '/assets/visualizations/penta-rag-knowledge-graph/index.html' | relative_url }}" loading="lazy" sandbox="allow-scripts" referrerpolicy="no-referrer"></iframe>
</section>

The numbers belong to that cut, not to a live counter. Updating the viewer means regenerating the projection, sanitizing it again, and reviewing the differences before the public artifact is replaced.
{: .notice--info}

| Visible component | Derivation | Correct reading |
|---|---|---|
| Task families | Deterministic rules over strategy, tool, transport, and project. | They orient exploration; they do not classify the author's psychology. |
| Strategy nodes | Experience lessons with observed evidence. | They stand for a recorded strategy, not a belief. |
| Semantic edges | Neighborhood between vector representations in the derived index. | They indicate operational similarity, not causality. |
| Structural and correction edges | Shared tools, repositories, transports, or sequences. | They are clues that require opening their provenance. |
| Communities and panels | Deterministic aggregations over the export. | They help decide what to ask and where to verify. |
| Mail and thesis | They do not appear as content nodes. | Only capabilities, scopes, and authorized metadata are published. |

The composition does not try to show all 3,949 relations with equal weight. It starts from task families, lets projects and errors be isolated, and holds detail back for interaction. That is the trade-off between a real base — too large for an illustration — and a public reading — too important for an opaque hairball.

### From a retrieved source to an attributed answer

Finding the right document does not guarantee a right answer. A model can leave out the decisive condition, cite a different source, or answer when it should abstain. LongMemEval separates extraction, cross-session reasoning, temporality, knowledge updating, and abstention; LongMemEval-V2 — still presented as work in progress — moves the focus toward agent trajectories, workflow knowledge, state changes, recurring failures, and invalid premises (Wu et al. 2024; Wu et al. 2026). My local set is far smaller and is not comparable with those results: its job is to check this project's contract.

`context-answer-v1` holds 18 sanitized cases: 12 positives, with required claims and sources, and 6 negatives. A deterministic fixture passed 18/18. That proves the evaluator tells a valid output from an invalid one; it does not prove that a generative model answers well.

| Arm evaluated | Result | Correct interpretation |
|---|---|---|
| Deterministic fixture | 18/18 | The gate works over constructed cases; it does not measure a model. |
| Generative Qwen through an external bridge | First batch rejected for carrying internal infrastructure; second batch returned no evaluable structured output. | **Inconclusive**; calling it an abstention or an answer failure would both be wrong. |
| Gemini through Antigravity | The initial reading gave 11/18 because it mixed exportable and `local_only` cases. The legitimate slice — 5 positives and 6 negatives — passed 11/11 when the same artifact was re-evaluated. | It validates only the permitted subset; it does not resolve the 7 local positives and does not compare providers. |
| Local provenance packet | 7/7 sources came out aligned after testing scope, fragment, manifest, and currency failures. | They are ready for human review; there is still no evaluated local answer. |

Going from 11/18 to 11/11 does not inflate a score: it repairs the evaluation universe. A source marked `local_only` does not become exportable because a secret scanner found no matches. Governance starts exactly when the denominator respects the permissions too.

The next rung is concrete: run an authorized local answer, keep the negatives, and have a person review every output. Until then, the evidence supports talking about an attribution gate; not about a reliable generative memory.

---

## Closing: a useful memory before a digital clone

In this project, "digital clone" is a rhetorical horizon, not a validated technical category. I will not use that name for a RAG with more documents in it, or for an avatar that answers with confidence. At a minimum I would reserve it for a system with temporal memory able to correct itself; revocable preferences and limits; evidence of authorship; behavior evaluated in new situations; and human control over what is kept, shared, or deleted. MemGPT and the generative agents of Park et al. offer influential architectures for handling context, memories, reflection, and planning, but they do not turn those functions into identity (Packer et al. 2023; Park et al. 2023).

The defensible route comes down to five gates:

1. **Provenance and admission.** Every source enters with a role, a scope, a sensitivity, a consent, and an allowed output. Reading is not promoting.
2. **Time and contradiction.** An update has to keep what came before, declare when it starts to apply, and fail closed against incompatible successors.
3. **Retrieval and answer.** The system has to find sufficient evidence, cite what it actually received, and abstain when it is missing.
4. **Authorship and agency.** No incoming mail authorizes inferences about style, values, or identity; those claims require self-authored material, an explicit opt-in, and review.
5. **Control and reversibility.** Any sensitive memory needs a veto, a per-scope purge, traceability, and a revocation that actually works.

The evidence in this third part supports describing `penta-agent` as a local prototype of governed memory: it keeps experience, records corrections, exposes a bounded public projection, and lets its own tests fail without disturbing production. That is more accurate — and more defensible — than calling it a digital clone.

The next step forward is not adding more nodes. It is closing the local answer evaluation and comparing alternatives — Graphiti, GraphRAG, or `deja-vu` — under the same cut, the same permissions, and observable output criteria. A memory worth trusting is not the one that boasts about remembering everything, but the one that can explain **where each claim came from, since when it holds, who is allowed to see it, and when it has to answer "I don't know"**.

---

## References

### Bibliography

Cormack, Gordon V., Charles L. A. Clarke, and Stefan Büttcher. 2009. "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods". In *Proceedings of the 32nd Annual International ACM SIGIR Conference on Research and Development in Information Retrieval*, 758–59. New York: Association for Computing Machinery. <https://doi.org/10.1145/1571941.1572114>.

Edge, Darren, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, and Jonathan Larson. 2024. "From Local to Global: A GraphRAG Approach to Query-Focused Summarization". arXiv, April 24, 2024; revised February 19, 2025. <https://arxiv.org/abs/2404.16130>.

Hu, Yuyang, Shichun Liu, Yanwei Yue, Guibin Zhang, Boyang Liu, Fangyi Zhu, Jiahang Lin, et al. 2025. "Memory in the Age of AI Agents". arXiv, December 15, 2025. <https://arxiv.org/abs/2512.13564>.

Lebo, Timothy, Satya Sahoo, and Deborah McGuinness, eds. 2013. *PROV-O: The PROV Ontology*. W3C Recommendation, April 30, 2013. <https://www.w3.org/TR/prov-o/>.

Nissenbaum, Helen. 2004. "Privacy as Contextual Integrity". *Washington Law Review* 79, no. 1: 119–58. <https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/>.

Packer, Charles, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. 2023. "MemGPT: Towards LLMs as Operating Systems". arXiv, October 12, 2023; revised February 12, 2024. <https://doi.org/10.48550/arXiv.2310.08560>.

Park, Joon Sung, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. 2023. "Generative Agents: Interactive Simulacra of Human Behavior". In *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*, article 2, 1–22. New York: Association for Computing Machinery. <https://doi.org/10.1145/3586183.3606763>.

Rasmussen, Preston, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. 2025. "Zep: A Temporal Knowledge Graph Architecture for Agent Memory". arXiv, January 20, 2025. <https://arxiv.org/abs/2501.13956>.

Wu, Di, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. 2024. "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory". arXiv, October 14, 2024; revised March 4, 2025. Accepted at ICLR 2025. <https://arxiv.org/abs/2410.10813>.

Wu, Di, Zixiang Ji, Asmi Kawatkar, Bryan Kwan, Jia-Chen Gu, Nanyun Peng, and Kai-Wei Chang. 2026. "LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues". Work in progress, arXiv, May 12, 2026. <https://arxiv.org/abs/2605.12493>.

Zhang, Yanzhao, Mingxin Li, Dingkun Long, Xin Zhang, Huan Lin, Baosong Yang, Pengjun Xie, et al. 2025. "Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models". arXiv, June 5, 2025. <https://arxiv.org/abs/2506.05176>.

### Software and technical documentation

GetZep. n.d. *Graphiti: A Framework for Building Temporal Knowledge Graphs*. GitHub repository. Accessed August 31, 2026. <https://github.com/getzep/graphiti>.

Hugging Face. n.d. *Sentence Transformers*. Technical documentation. Accessed August 31, 2026. <https://www.sbert.net/>.

Letta AI. n.d. *Letta Code*. GitHub repository. Accessed August 31, 2026. <https://github.com/letta-ai/letta-code>.

Mem0 AI. n.d. *Mem0: Universal Memory Layer for AI Agents*. GitHub repository. Accessed August 31, 2026. <https://github.com/mem0ai/mem0>.

Microsoft. n.d. *GraphRAG*. GitHub repository. Accessed August 31, 2026. <https://github.com/microsoft/graphrag>.

Qwen. n.d. *Qwen3-Embedding-0.6B*. Model card, Hugging Face. Accessed August 31, 2026. <https://huggingface.co/Qwen/Qwen3-Embedding-0.6B>.

Qwen. n.d. *Qwen3-Reranker-0.6B*. Model card, Hugging Face. Accessed August 31, 2026. <https://huggingface.co/Qwen/Qwen3-Reranker-0.6B>.

Shulcz, Vladislav. n.d. *deja-vu*. GitHub repository. Accessed August 31, 2026. <https://github.com/vshulcz/deja-vu>.

Vasturiano. n.d. *3d-force-graph*. GitHub repository. Accessed August 31, 2026. <https://github.com/vasturiano/3d-force-graph>.

Vectorize. n.d. *Hindsight: Agent Memory That Learns*. GitHub repository. Accessed August 31, 2026. <https://github.com/vectorize-io/hindsight>.

> **Conflicts of interest in the sources.** The model cards, the repositories, and several of the systems papers are written by their own developers or by organizations that sell related services; LongMemEval-V2, moreover, is still declared work in progress. They are used here to document architecture, declared functions, and maintenance status, not to accept claims of superiority. `penta-agent`'s own metrics are likewise evidence produced by the project itself, and they need reproducible artifacts and independent review before they can support general comparisons.
{: .notice--info}
