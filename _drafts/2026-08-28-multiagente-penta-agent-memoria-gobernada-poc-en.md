---
layout: single
title: "Multi-agent work in three spoonfuls III: a memory that leaves traces"
subtitle: "From auditable RAG to a governed knowledge base—and what still prevents calling it a digital clone"
date: 2026-08-28 00:00:00 -0400
categories: [ai, productivity, development, multi-agent]
tags: [multi-agent, rag, agent-memory, provenance, privacy, governance, knowledge-graph, threejs]
description: "Third penta-agent log: a 3D projection regenerated from real memory, boundaries between RAG, mail, and research, and a verifiable route—not a promise—toward a digital clone."
excerpt: "The RAG has already accumulated traces of work. The challenge is not drawing them: it is deciding which memory should persist, when it becomes outdated, and what evidence would be needed to responsibly discuss a digital clone."
author: clabra
lang: en
ref: multiagente-penta-agent-memoria-gobernada-poc
permalink: /en/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/
toc: true
toc_sticky: true
comments: true
author_profile: true
header:
  teaser: /assets/images/teasers/teaser-multiagentes-memoria.webp
  og_image: /assets/images/teasers/teaser-multiagentes-memoria.webp
  og_image_alt: "A 3D graph of strategies learned by a multi-agent system"
---

> **Entry status.** This is an executable, local draft. The visualization was generated on 29 August 2026 from a sanitized public projection: it contains no mail bodies, attachments, addresses, absolute paths, tokens, or credentials. It has not been published or pushed to a remote.
{: .notice--warning}

In the [second spoonful]({{ "/ia/productividad/desarrollo/multiagente-penta-agent-memoria/" | relative_url }}), the goal was narrower: establish that a memory could retrieve evidence and acknowledge when it could not. That part exists. What remained was to examine its consequence: as memory grows, it stops being only an index and becomes a responsibility for provenance, validity, access, and review.
{: .text-justify}

This third entry also corrects two mistakes of mine. The first version of this draft reduced the system to four decorative nodes. It was safe, but not informative: it turned a real knowledge base into an allegory. The second correction is less striking: a graph of commands can be faithful and still unreadable. Safety does not come from drawing less; it comes from applying verifiable limits to a projection that remains recognizably derived from evidence. The viewer below preserves strategies, relations, and failures, but begins with a human question: **what kind of work has been learned?**
{: .text-justify}

> **Reading convention.** **FACT** denotes a dated, reproducible local measurement; **INFERENCE** denotes a design decision drawn from those traces; **UNVERIFIED** denotes a capability deliberately not attributed to the system. This distinction is part of the demonstration: it prevents a number, an edge, or an infrastructure test from posing as evidence of understanding, answer fidelity, or identity.
{: .notice--info}

## Spoonful 1: what changed since II

RAG is not synonymous with agent memory, and memory is not identity. Recent literature distinguishes retrieval, memory, context management, and evaluation because they have different functions.[^memory-taxonomy] This entry uses that distinction to show progress without turning it into a promise of autonomy.
{: .text-justify}

The closing of II left four verifiable commitments, not a vague promise to “remember more.” III returns to them with an honesty rule: a piece counts as solved only when there is an artifact, a test, and a stated boundary. This is the short account before opening the viewer.
{: .text-justify}

| Open item at the end of II | What III implemented locally | Status that would be misleading to hide |
|---|---|---|
| Compare dense, lexical, and reranking retrieval without mistaking a local gain for production. | An isolated Qwen staging collection, with a frozen 319-context cut, preserved negatives, and tests for ranking, query instruction, and reranking. The next experiment accepts only an intent/document-family taxonomy bound to cut hashes and declared `source_only`. | The best run still has 2 partial cases: the strict gate remains red, there was no promotion, and independent human curation of that taxonomy is still missing. |
| Evaluate whether an answer uses retrieved sources and knows when to abstain. | `context-answer-v1`: 18 sanitized cases requiring claim coverage, retrieved citations, and negative abstention; the permitted external slice passed 11/11. | It is not an end-to-end generative-fidelity evaluation and does not replace human review of the 7 local cases. |
| Add validity without deleting history. | A sandbox preserves prior evidence, admits `supersedes` only from the later date, and rejects competing successors. | There is still no temporal reasoning connected to live memory or automatic contradiction adjudication. |
| Make growing memory visible without treating topology as truth. | A static 3D viewer regenerated from a sanitized projection, with work categories and a text alternative both in the post and inside the viewer when WebGL is unavailable. | The viewer does not query Qdrant, validate edges, or represent a mind or identity. |

III therefore does not announce a finished system. It shows what changed from evaluated retrieval to memory with boundaries, which checks can now fail, and where measurement, decision, or human authorization is still required.
{: .notice--primary}

| Layer | Local evidence as of 29 August 2026 | What it supports | What it still **does not** support |
|---|---|---|---|
| `penta-agent` experience memory | Public cut generated on 29 August: 16,955 derived-index points; 1,432 strategies, 3,949 relations, 12 communities, and 8 work types. | That operational traces, semantic neighbourhoods, and inspectable correction relations exist. | That every edge is causal truth, or that the system answers every question correctly. |
| Curated cross-agent context | 319 canonical contexts in `penta_context_v2`; in this entry’s local check the collection returned `green`, and remains derived from local records. | That a curated handoff or decision can be retrieved with provenance. | That all work history is curated, or that the index replaces the canonical record. |
| Dense embeddings without Ollama | Direct `Qwen3-Embedding-0.6B` staging: an explicit 319-context cut, 1024D on CPU, and 319/319 persisted in `penta_context_qwen3_staging`. A second pass with its ranking policy declared produced 38 passes, 2 partials, and 0 misses; all 8 negatives abstained. | That a reproducible, isolated, non-Ollama path exists to test and debug a retriever. | That Qwen improves the baseline, that the strict gate passed, or that it should be promoted. |
| Personal mail | Local aggregate pilot: 12,072 unique messages, 8,559 duplicates, years 2011–2026. The private report is not versioned. | That read-only inventory works within an authorized scope. | That mail is a public corpus, semantic database, or description of other people. |
| Local personal memory | A separate prototype with bounded mbox ingestion, SQLite/FTS, explicit scopes, purge, and synthetic evaluation. | That private material can be retrieved without mixing it into agent RAG. | That a generative workflow over sensitive mail or a personality model is authorized. |
| Thesis and research documents | Public snapshot of a derived index: 796 textual process artifacts, 533 links, and 7 leads; SQLite FTS5 and lexical TF-IDF, with no neural embeddings. It excludes historical sources, DTA, Parquet, PDF, and images. | That the research process can add verifiable traceability without exposing sources, text, paths, or microdata. | That the index proves historical execution, replication, substantive findings, or research data. |

There are two readings at once. The deductive one starts from a simple rule: if a source can be wrong, change, or be private, its origin and scope must travel with it. PROV-O formalizes the distinction between entity, activity, and agent; retrieving text is not enough—it matters what produced it and through which transformation.[^prov-o] The inductive reading starts from observed traces: the RAG already accumulates repeated strategies, communities, corrections, and failures. The graph does not invent those layers; it makes them inspectable.
{: .text-justify}

A real dependency also emerged that the old graph did not reveal. The historical viewer assumed a single vector; the current index uses the named `dense` vector. The first regeneration was degraded, with no semantic edges; a later run against the real index revealed the format incompatibility. After adapting the exporter and repeating the run, 3,658 semantic edges returned. This is not an implementation anecdote: a memory visualization is honest only when it can show when its data chain degraded, why, and when it was restored.
{: .text-justify}

### From technical trace to a human question

The index’s atomic unit remains an observed strategy—many are command-shaped because that is how actions were recorded. That is good for audit, but poor for explanation. So that the map can be read before knowing Bash, Python, or Qdrant, I added a visible, deterministic classification over those traces. It does not use a model to guess intent: it applies public rules to strategy, tool, transport, and project, while preserving the original technical identifier when a reader opens a detail card.
{: .text-justify}

| Derived work type | Strategies in this run | Example question it makes possible |
|---|---:|---|
| Coordinate agents and decisions | 399 | What was learned while leaving a handoff or delegating a task? |
| Research and analyse data | 396 | Which tactics recur while reviewing a thesis, data, or sources? |
| Read and trace evidence | 385 | Which antecedents were inspected before a decision? |
| Execute and automate | 118 | Which steps implemented a change after review? |
| Version and compare changes | 76 | Which controls were applied before retaining a modification? |
| Test and verify | 28 | What was checked rather than merely declared ready? |
| Operate tools and services | 18 | Which infrastructure enabled or blocked a workflow? |
| Edit and communicate | 12 | Which work turned technical evidence into documentation or publication? |

This layer is a pedagogical lens, not an ontology of the author or a new canonical truth. A strategy may participate in more than one task and is currently placed in the first family whose rules it meets. That simplification is declared so it can be corrected: it orients readers; it does not measure productivity or attribute human capacities to the system.
{: .text-justify}

### What this map measures—and what it does not

A semantic edge is proximity between centroids of indexed strategies; a structural edge derives from shared tools, repositories, or transports; a correction edge connects a failure to a related later strategy. These are three distinct signals. Node size summarizes observed evidence; initial colours group work types; panels can then switch to communities, projects, status, agent, and health. None of those signals demonstrates intent, human understanding, or a coherent biography.
{: .text-justify}

That caution matters because long-term memory evaluation is not limited to retrieving a sentence. LongMemEval separates extraction, multi-session reasoning, temporality, knowledge updating, and abstention.[^longmemeval] This project has evidence for retrieval and admission; it does not yet have a defensible evaluation of answer fidelity over mail, research material, or a representation of the author.
{: .text-justify}

## Spoonful 2: a knowledge base is not built with embeddings alone

The existing base has layers with different permissions and functions. The ledger and source files are canonical; Qdrant is a regenerable index; the viewer is a public projection; private adapters live outside Git. This is less flashy than saying “I have a digital brain,” but it prevents vector similarity from silently becoming a fact or identity.
{: .text-justify}

### The PoC is not a source blender

The diagram below makes explicit what a 3D graph must not imply: mail, thesis material, and RAG are not “more nodes” in a single bucket. At this stage, only curated working memory feeds cross-agent retrieval and the public projection. Mail retains a private, reversible, vetoable route; thesis and documents contribute only authorized traceability. The arrows describe allowed outputs, not automatic content transfers or inferences about people.
{: .text-justify}

<figure class="align-center">
  <a href="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources.svg' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources.svg' | relative_url }}" alt="Three governed sources: working RAG allows retrieval with provenance; personal mail allows only private reversible review; thesis and documents allow citations and verification status. A public boundary blocks mail bodies, attachments, addresses, absolute paths, microdata, and inferences about identity." loading="lazy" decoding="async">
  </a>
  <figcaption>Figure 1. The current integration is an architecture of permissions: the source determines its allowed output, not a promise of total memory.</figcaption>
</figure>

### The thesis enters as process traceability, not a corpus

This version’s concrete advance is not “putting the thesis into RAG.” It is a [public snapshot of the research index]({{ '/assets/data/memoria_gobernada/thesis-research-index-snapshot.json' | relative_url }}) generated from its derived manifest after its local contract was verified. The card releases only allowlisted metadata: **796** derived textual artifacts—316 audits, 244 reports, 133 contracts, 71 pseudocodes, and 32 inventory, replication, or documentation pieces—along with **533** process links and **7** leads that still require review. It does not release documents, titles, paths, individual hashes, query results, source files, or microdata.
{: .text-justify}

The distinction matters more than the count. Its retrieval layer is reproducible SQLite FTS5 plus lexical TF-IDF: it is not a neural embedding and does not claim understanding. Historical source data, DTA, Parquet, PDFs, and images are explicitly excluded; the card states that it is not evidence of historical execution, replication, or substantive findings. This is a useful way to add high-value knowledge: it can expose the research chain and its open gaps without turning data, drafts, or pending conclusions into public agent memory.
{: .text-justify}

| Upcoming problem | Existing asset | Library or project worth a serious trial | Criterion for adopting—or discarding—it |
|---|---|---|---|
| Recover coding episodes across agent harnesses | `penta-agent` handoffs, events, and curated context. | [`deja-vu`](https://github.com/vshulcz/deja-vu), which recalls locally written sessions from different coding agents through MCP. | It must improve a real historical lookup without replacing curated records with raw transcripts. |
| Keep explicit agent state | Evaluated RAG and curated context; not a general memory runtime. | [Letta](https://github.com/letta-ai/letta), an operational continuation of MemGPT.[^memgpt] | Compare its hierarchical memory with current contracts before adding another runtime. |
| Test dense embeddings without Ollama | `penta_context_v2` remains the baseline; `penta_context_qwen3_staging` is a separate derived collection. | [`Qwen3-Embedding-0.6B`](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B), executed through Sentence Transformers.[^qwen-embedding] | A `source_only`, hash-bound intent/family taxonomy must resolve the two partials without changing admission, negatives, `k`, or the active collection; then compare quality, CPU latency, and resources before considering a migration. |
| Extract memories from conversations or documents | Human curation and ingestion; private mail with a veto and scope. | [Mem0](https://github.com/mem0ai/mem0) and [Hindsight](https://github.com/vectorize-io/hindsight). | Measure precision, revocation, and false positives on synthetic data before any automatic mail extraction. |
| Represent validity, supersession, and contradiction | A sandbox tests explicit succession and fails closed on invalid temporal order or competing successors; there is no general temporal reasoner. | [Graphiti](https://github.com/getzep/graphiti) and Zep’s temporal architecture.[^graphiti] | Move from fixtures to thesis or project decisions while retaining source, validity, and human review. |
| Connect research documents, concepts, and citations | Allowlisted provenance snapshot of the derived index: 796 process artifacts, 533 links, and FTS5/TF-IDF retrieval, with no exported content. | [Microsoft GraphRAG](https://github.com/microsoft/graphrag) for a bounded scientific-corpus experiment.[^graphrag] | Compare cost, citation traceability, and retrieval against the current lexical baseline; do not ingest microdata, historical sources, or files without authorization. A local preflight already rejects corpus, scope, or budget without human approval. The repository is in maintenance mode and warns that indexing can be costly: here it would be a minimal comparative experiment, not a foundational dependency. |
| Visualize without inventing a topology | Local generator and vendored `3d-force-graph`. | [`3d-force-graph`](https://github.com/vasturiano/3d-force-graph), reused in this export. | Keep a text alternative and sanitized projection; do not turn visual distance into human affinity. |

This is the post’s methodological *mea culpa*: I had treated some of these libraries as bibliographic references when, for my research workflows, several deserve real comparative experiments. The priority is not installing everything. It is testing first what may reduce scientific friction without degrading traceability: GraphRAG for documents with verifiable citations, Graphiti for validity and contradiction, and `deja-vu` for recovering decisions distributed across coding sessions. Mem0 and Hindsight are riskier for mail and personal profile: they first need an evaluation set, visible revocation, and a legitimate-use question.
{: .text-justify}

The Qwen experiment also clarifies what “testing” means. No service was changed and the active collection was not rewritten: I created an isolated local environment, fixed its versions, downloaded the model only under an explicit signal, and targeted another collection. The cut keeps the 319 context identifiers and their digest—not their text—so a resumed run cannot silently mix in later records. The smoke test verified the direct model, 1,024 dimensions, and CPU execution. Reindexing completed 319/319 and bounded batching persists small groups; a test forces 17 records to verify a 16+1 write and that a missing frozen record stops the run.

The first result was deliberately uncomfortable: across 40 gold queries, there were 36 full passes, 3 partials, and one miss on a colloquial, typo-containing query about the delegation bridge; all 8 negatives abstained. Diagnosis showed that Qwen did retrieve the correct handoff as its second dense neighbour, but the `0.10` BM25 bonus—which only reorders already-admitted candidates—pushed it out of top-5 because of a generic sparse match.

I did not change production policy on that single observation. The Qwen variant declares a `0.00` BM25 bonus, staging-only; a red/green test reproduces the displacement and then restores the stronger dense neighbour. The second pass reused the same 319 points, without reindexing or touching `penta_context_v2`: it produced 38 passes, 2 partials, and no misses; Recall@5 rose to 0.9635 and MRR to 0.8396, while all 8 negative abstentions remained intact. Yet the two multi-source cadastre partials are enough for the strict evaluator to remain failing.

I also tested Qwen’s recommendation to declare a retrieval instruction, but did not turn a library recommendation into dogma. On exactly the same cut, a generic instruction to favour complete, citable sources fell to 33 passes, 3 partials, and 4 failures; negative abstentions fell from 8/8 to 6/8. That run reused all 319 vectors: it isolated the change to the query vector and falsified the hypothesis without touching documents or production. The native `query` prompt therefore remains the default, and a custom instruction exists only as an experimental parameter. The collection remains staging: it does not establish an improvement over the baseline and is not promoted. It must not be confused with the Qwen external bridge in the next section: that was a generative model outside the local boundary and its result was inconclusive; this is an embedding experiment with a bounded improvement and an open failure.[^qwen-embedding]
{: .notice--warning}

The next candidate was a local reranker from the same family, `Qwen3-Reranker-0.6B`: it receives only documents that already passed admission and reorders them; it cannot invent a source or turn a negative into a hit. On the fixed cut, it did retrieve the third document for the Spanish multi-source case and moved Recall@5 from 0.9635 to 0.9688, with MRR 0.9010 and all 8 abstentions preserved. Yet it remained at 38 passes, 2 partials, and 0 failures: that cadastre partial disappeared but one appeared in `penta-agent`/skills. Worse, median latency rose from 2.37 s to 15.83 s, with a 91.10 s maximum. This is an honest comparison, not an adoption: for now it only belongs in a local offline-analysis lane where that cost can be justified.[^qwen-reranker]
{: .text-justify}

A later read-only probe of the same isolated collection explains why I did not declare victory. For the two multi-source cadastre questions, the expected documents missing from top-5 were present among the candidates, at ranks 7 and 10 respectively. The model had not “forgotten” those sources; the retriever still cannot cover distinct document families within five places. Raising `k` until the result passes would change the evaluation question, not solve selection.

The next step does not add an opaque heuristic either: the staging contract already rejects a label that is not bound to the cut hash, query hash, and a closed-vocabulary family; it also rejects any label that declares use of the gold set. There are no independently curated human labels yet, so there is no new run to display and no partial case “solved.” The useful result is more modest: the next hypothesis can now fail without altering admission, negatives, `k`, or the active collection.
{: .notice--warning}

I then tested bounded `repo_scope` diversification: within a window of 20, it reorders only candidates that had already passed admission to make room for distinct provenance scopes. It kept the same 319 points, 8/8 abstentions, and zero failures; aggregate Recall@5 rose from 0.9635 to 0.9740 and the English multi-source case passed. Yet the strict result remained 38 passes and 2 partials: the Spanish case still left out the maps handoff and, in exchange, a partial appeared in `penta-agent` skills. This is useful precisely because it is not a victory: `repo_scope` is too coarse a proxy for a document family.

As a second control, I fused the base and reranker orders with reciprocal rank fusion (RRF), a classic rank-combination method.[^rrf] It neither added documents nor raised `k`: it reused the same 319 points and preserved all 8/8 abstentions. The result returned to **38/2**, with Recall@5=0.9635 and a 20.06 s median; neither cadastre partial was recovered. The sequence matters more than the algorithm’s name: RRF is a reasonable tool, but in this corpus it neither offsets the cost nor closes the contract. Both comparators remain offline, with no promotion. The next hypothesis needs curated lineage or document-intent metadata and an evaluation cut that proves an improvement does not merely move an error to another task.
{: .notice--info}

### Decision log: what the retriever actually learned

Every run below uses the same 319-context cut, 40 queries, and `k=5`; none changes documents, production, or the definition of success. This is not a leaderboard: it makes visible which hypothesis survived and which did not.

| Question tested | Isolated change | Observed result | Decision |
|---|---|---|---|
| Does the sparse bonus displace correct dense evidence? | BM25 from `0.10` to `0.00`, staging only. | From 36/3/1 to **38/2/0**; all 8/8 negatives still abstain. | Retained as an experimental starting point; not evidence of a production improvement. |
| Does a generic query instruction improve citability? | Explicit Qwen instruction. | **33/3/4** and 6/8 negative abstentions. | Rejected: coverage and abstention both regress. |
| Does a reranker recover complementary sources? | `Qwen3-Reranker-0.6B` over admitted candidates. | **38/2/0**; MRR 0.9010, but p50 15.83 s and one partial moves to skills. | Offline analysis only; no promotion. |
| Is repository scope the same as a document family? | `repo_scope` diversification. | **38/2/0**; Recall@5 0.9740, but the error moves. | Rejected: provenance is not document intent. |
| Does agreement between orders avoid that move? | Base + reranker RRF fusion. | **38/2/0**; p50 20.06 s; cadastre remains partial. | Rejected: it does not justify its cost or close the gate. |

{: .text-justify}

Mail makes the point. Being able to read a Thunderbird message does not authorize promoting it into durable memory, inferring preferences, or publishing it. Helen Nissenbaum’s contextual integrity names this distinction between access and appropriate information flow.[^nissenbaum] That is why mail appears here as a governed capability and reviewed aggregate, not as a shiny sphere in a public graph.
{: .text-justify}

## Spoonful 3: the graph that already exists

The visualization below was generated locally from a cut of experience memory and then sanitized for publication. The viewer does not call Qdrant or external services: it receives a static, regenerable, audited artifact. The full-screen link preserves the professional viewer; this page supplies context and limits. If the viewer opens in a browser without WebGL, it does not leave an empty canvas: it displays the derived metrics and the eight work families in its own textual alternative.
{: .text-justify}

The [public JSON export]({{ '/assets/data/rag_knowledge_graph/public-graph.json' | relative_url }}) accompanies the viewer so this run can be inspected reproducibly. Its generator, template, and vendored engine are also versioned with the site: before publication, the HTML must be reproduced exactly from that public JSON without rereading private sources. It is a reading projection, not the canonical memory.
{: .text-justify}

**Three-step guided reading.** First open the **Tasks** tab and choose, for example, “Research and analyse data”: the map then concentrates on tactics associated with that work. Then use **Proj** to distinguish where they occurred—thesis, `penta-agent`, or other repositories. Only at the end use **Errors** or diagnostic mode to inspect a concrete point of friction. The viewer should not demand that readers interpret a technical cloud before knowing the question it answers.
{: .notice--primary}

<section class="rag-knowledge-graph" aria-labelledby="rag-knowledge-graph-title">
  <div class="rag-knowledge-graph__header">
    <div>
      <p class="rag-knowledge-graph__eyebrow">Public projection · 2026-08-29</p>
      <h3 id="rag-knowledge-graph-title">penta-agent learned-work map</h3>
      <p>29 August cut: 1,432 strategies · 3,949 relations · 8 work types · 16,955 indexed points</p>
    </div>
    <a class="rag-knowledge-graph__open" href="{{ '/assets/visualizations/penta-rag-knowledge-graph/' | relative_url }}" target="_blank" rel="noopener">Open full viewer<span class="screen-reader-text"> in a new tab</span></a>
  </div>
  <iframe class="rag-knowledge-graph__frame" title="Navigable 3D map of penta-agent work types and strategies" src="{{ '/assets/visualizations/penta-rag-knowledge-graph/' | relative_url }}" loading="lazy" sandbox="allow-scripts" referrerpolicy="no-referrer"></iframe>
</section>

The viewer’s counts belong to that reproducible cut; they are not a live counter. Canonical memory and its indexes can change afterwards, so an update requires regenerating and sanitizing the projection, then reviewing the difference before replacing the public artifact.
{: .notice--info}

{: .table-caption}
**Table 1** — Text alternative and limits of the projection

| Visible component | Derivation | Correct reading |
|---|---|---|
| Work types | Deterministic rules over strategy, tool, transport, and project. | A didactic starting point for asking a question; not a psychological or exhaustive classification. |
| Strategy nodes | Experience lessons with observed evidence. | A recorded strategy, not a belief or author trait. |
| Semantic edges | Neighbourhood in the derived embedding index. | Operational similarity, not causality. |
| Structural and correction edges | Co-occurrence and temporal sequence of events. | A clue for inspecting recovery or failure; its provenance must be opened. |
| Communities, projects, and panels | Deterministic aggregates over the export. | A map for deciding what to ask and where to verify, not an automatic diagnosis. |
| Mail and thesis | **Not** content nodes. | Their capabilities, scopes, and metadata are described above; content remains private or under validation. |

The visual composition does not try to make all 3,949 relations legible at once. It starts from work types, lets readers isolate projects or errors, and keeps detail nodes behind interaction. That is the right trade-off between a real base—too large for an illustration—and public reading—too important for an opaque hairball.
{: .text-justify}

## The new gate: from a retrieved source to an attributed answer

Since post II, the retriever already had gold questions, ranking metrics, and negative controls. That was not enough for a final answer: a model can find the right document, cite another one, omit the decisive condition, or answer when it should abstain. I therefore separated those two contracts.
{: .text-justify}

The new local set has 18 sanitized cases: 12 questions with one or more required claims and 6 negatives. In a positive case, every claim must point to a source that retrieval actually returned; in a negative case, the output must abstain without attaching sources. The deterministic fixture passed 18/18, with claim coverage, citation validity, and negative abstention all at 1.0. That is evidence that the **gate** distinguishes a valid from an invalid contract—not evidence that a generative model already answers well.
{: .text-justify}

I also observed the first external red case. A sanitized batch sent through Qwen's isolated bridge was initially rejected because a retrieved excerpt contained internal infrastructure; that excerpt was filtered before any later export. On a second attempt Qwen did not return an evaluable structured block. The correct result is not to adjust the denominator or call an absence “abstention”: that arm remains **inconclusive**.
{: .notice--warning}

On August 29 I also ran Gemini through Antigravity, using the same isolated contract. Its global reading yielded 11/18: there were 12 external answers, but they were being checked against a set that also retained local questions. That exposed a design error, not a fair provider denominator. A later check of the canonical manifest found a seventh case: the RSH audit handoff is classified as `interno` and `local_only`. A clean secret-literal scan does not make it exportable. I retained the question and claim, but removed it from the external slice; I did not manufacture a public summary or force the retriever to return it.
{: .text-justify}

The legitimate external slice therefore contains 5 permitted positives and 6 negatives. Re-evaluating the exact same artifact, it had valid citations, required retrieved sources, and correct negative abstention in all 11 cases: **11/11**. The seven local positives are excluded from that benchmark, not solved or erased. This separates a source that must not leave local scope from generation that cites incorrectly; it still does not turn that narrow 11/11 into an overall result, a model comparison, or proof of reliable memory.
{: .text-justify}

The local circuit now has a first verifiable rung, but it is not an answer fabricated by a model. A provenance packet checks, without invoking a provider or querying Qdrant, that the local source exists, still contains the declared evidence fragment, matches the current provenance hash, and remains `local_only`. It was made to fail with a wrong scope, an absent fragment, an absent manifest, and a modified source; then, after selectively resynchronizing records that had changed, the current run left all 7 of 7 cases ready for human review. “Ready” means the local evidence is aligned for review, not that a model has already answered correctly.
{: .notice--warning}

The practical consequence is still less flashy than a leaderboard: an authorized local response must preserve the negatives and a person must review every answer. The provenance packet does not measure retrieval or generation; by itself it has no accuracy rate. Until then, neither Qwen nor Gemini justifies calling the memory reliable—much less a digital clone.
{: .text-justify}

## The route toward a digital clone is not closed

A digital clone is not “more context,” nor an avatar that answers confidently. It would require, at minimum, temporal memory that can correct itself, a revocable model of preferences and limits, evidence of authorship, and behavioural evaluation in new situations. Park et al.’s generative agents and MemGPT’s context architecture help frame the problem, but they do not establish that this system has those properties.[^park][^memgpt]
{: .text-justify}

The route I can defend today has five gates:
{: .text-justify}

1. **Provenance and admission.** Every new source enters with role, scope, sensitivity, consent, and an allowed output; reading is not promoting.
2. **Time and contradiction.** The sandbox now retains a prior decision, admits an explicit successor only from its date, and rejects competing successors. It is still not an integrated temporal reasoner: Graphiti is the serious comparator before carrying that rule into live memory.
3. **Retrieval and answer evaluation.** A local gate for citations, coverage, and abstention now exists over 18 sanitized cases. In parallel, Qwen completed an isolated 319-context cut. A declared ranking variant removed the initial miss and left 38 full passes and 2 partials out of 40 without losing negative abstentions; the strict gate still blocks promotion because of those multi-source partials. It is evidence of a gate that lets the system learn without fabricating a victory, not a demonstrated improvement over production. A first structured generative run separated absent evidence from attributed generation, but failed end-to-end because retrieval was incomplete. After testing scope, manifest, fragment, and freshness failures, the local provenance packet left all 7 of 7 sources ready for review; it prevents an answer from relying on old evidence, not a claim that a model answered well. Authorized retrieval and human review still remain.
4. **Authorship and agency.** A self-authored corpus, opt-in claims policy, and human review must precede any claim about style, values, or preferences. Incoming mail is not suitable for that purpose.
5. **Human control and reversibility.** Sensitive memory needs a veto, revocation, scope purge, and a trace of every transformation leading to a view or answer.

The conclusion is less spectacular and more useful: I have a multi-agent knowledge base that already leaves traces. It can retrieve context, retain corrections, show its topology, and keep private sources out of the display case. I do not yet have a digital clone. Naming that distance is part of the work; closing it requires comparative experiments, behavioural evidence, and human decisions that no graph can make for me.
{: .text-justify}

---

## References

[^memory-taxonomy]: Yuyang Hu et al., “Memory in the Age of AI Agents” (2025). <https://arxiv.org/abs/2512.13564>

[^prov-o]: W3C, “PROV-O: The PROV Ontology,” recommendation, 2013. <https://www.w3.org/TR/prov-o/>

[^longmemeval]: Di Wu et al., “LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory” (2024). <https://arxiv.org/abs/2410.10813>

[^memgpt]: Charles Packer et al., “MemGPT: Towards LLMs as Operating Systems” (2023). <https://doi.org/10.48550/arXiv.2310.08560>

[^graphiti]: Preston Rasmussen et al., “Zep: A Temporal Knowledge Graph Architecture for Agent Memory” (2025). <https://arxiv.org/abs/2501.13956>

[^graphrag]: Microsoft, “GraphRAG: modular graph-based Retrieval-Augmented Generation,” repository, accessed 30 August 2026. Its README declares maintenance mode, advises starting small, and warns of potentially costly indexing. <https://github.com/microsoft/graphrag>

[^qwen-embedding]: Yanzhao Zhang et al., “Qwen3 Embedding: Advancing Text Embedding and Reranking Through Foundation Models” (2025), arXiv:2506.05176. The [official Qwen3-Embedding-0.6B model card](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B) documents 1,024 dimensions, multilingual support, and query instructions.

[^qwen-reranker]: Qwen, [“Qwen3-Reranker-0.6B” model card](https://huggingface.co/Qwen/Qwen3-Reranker-0.6B), consulted 29 August 2026. It documents the Sentence Transformers `CrossEncoder` interface, multilingual support, and user-defined instructions; the figures above are this project’s fixed-cut local run, not a vendor benchmark.

[^rrf]: Gordon V. Cormack, Charles L. A. Clarke, and Stefan Büttcher, “Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods,” *Proceedings of the 32nd Annual ACM SIGIR Conference on Research and Development in Information Retrieval* (2009): 758–759. <https://doi.org/10.1145/1571941.1572114>

[^nissenbaum]: Helen Nissenbaum, “Privacy as Contextual Integrity,” *Washington Law Review* 79, no. 1 (2004): 119–158. <https://crypto.stanford.edu/portia/pubs/articles/N1500699020.html>

[^park]: Joon Sung Park et al., “Generative Agents: Interactive Simulacra of Human Behavior,” *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology* (2023): 1–22. <https://doi.org/10.1145/3586183.3606763>
