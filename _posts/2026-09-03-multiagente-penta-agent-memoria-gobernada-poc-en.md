---
layout: single
title: "Multi-agent work in three spoonfuls III: a memory that leaves traces"
subtitle: "From auditable RAG to a more governed memory: it still is not a digital clone"
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
  # Solo en la version EN: `_plugins/julia_feed.rb:60` exige `lang: en` ademas del
  # canal, y `syndicate_devto.rb` lee esta misma clave. La transcreacion de hoy lo
  # copio del ES --que lleva `[]` porque el espanol no se sindica-- y con eso el
  # post salio del feed sin que nada avisara: paso de 4 items a 3.
  republish: [dev, medium]
repo: https://github.com/tatanlabra/penta-agent
entorno: "Arch Linux, KDE Plasma, local services (Qdrant and Sentence Transformers over loopback, systemd timers), Qdrant with the named `dense` vector"
en_abstract: >
  Third log of a local multi-agent setup. The previous entry made its shared
  memory measurable; this one asks a harder question: what should persist, what
  should expire, and what must never leave its scope. Four sources are kept apart
  by contract rather than merged — curated operational memory, a private and
  reversible personal-mail pilot, authorized process metadata from a thesis
  project, and the sanitized public projection built from them. A frozen
  319-context staging collection, embedded with Qwen3-Embedding-0.6B, was used to
  test several retrieval changes against 40 queries, eight of them written to
  check that the system also knows when *not* to retrieve. The best configuration
  reached 38 complete cases, 2 partial and no outright failures. A reranker
  ordered results slightly better and was rejected anyway, because response time
  grew too much. The more useful finding was that the two remaining cases do not
  need more power, they need better metadata. The viewer is a static, regenerable
  export — a map of recorded work, not a mind — and the illustration beside it is
  a brain loaded to 20%, which is roughly where this stands. What this does not
  show is equally explicit: retrieval quality is not answer fidelity, and none of
  it amounts to a digital clone.
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

> **Status of the demo.** The viewer was regenerated on August 29, 2026 from a sanitized public projection (with the non-public bits stripped out 😀): the artifact contains no mail bodies, attachments, addresses, absolute paths, tokens, credentials, or microdata.
{: .notice--warning}

## Preamble: remembering is not enough

In the [second part]({{ "/ia/productividad/desarrollo/multiagente-penta-agent-memoria/" | relative_url }}) I went after a bounded problem: getting `penta-agent`'s memory to retrieve evidence and to recognize when it had found none. The question in this third part is more practical, and it comes out of the system having been in use for a while: **what happens to a memory as it grows and turns blurry, or even contradictory?**

An index can pile up fragments without any trouble, and there are plenty of tools that already do that well. A more useful memory, in my judgment, has to carry provenance, currency, permissions, contradictions, and deletion criteria. It also has to tell finding a source apart from using it correctly. Recent literature insists on separating RAG — retrieval-augmented generation — context management, and agent memory, because they do different jobs and call for different evaluations [^hu-2025].

What follows has three movements: what changed since part II; which experiments survived a more serious evaluation; and how to show a memory without passing it off as a mind.

---
## Spoonful 1: from retrieving fragments to governing evidence

In part II the problem was **retrieving well**: finding the relevant context and recognizing when there was not enough evidence. A useful memory does not only retrieve information; it also has to know **where it came from, whether it still holds, where it can be used, and what is allowed to be done with it**.

RAG mostly solves retrieval. The memory layer adds rules for keeping, updating, relating, or discarding evidence. None of those functions amounts, on its own, to identity. To describe provenance I use concepts compatible with PROV-O — entities, activities, and agents — while currency, sensitivity, and permissions need rules of their own [^lebo-2013].

### What changed since part II

| Open item from II                                              | What exists now                                                                                       | What is still open                                                                        |
| -------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| Compare dense retrieval, lexical retrieval, and reranking.     | A frozen cut of 319 contexts and 40 queries evaluated at `k=5`.                                        | The best configuration gets 38 complete cases and 2 partials; the strict gate stays shut.            |
| Check that an answer uses its sources and knows how to abstain. | The `context-answer-v1` contract, with 12 positive and 6 negative cases, all sanitized.                | The end-to-end evaluation with a local model and the reserved human review are unfinished. |
| Add currency without erasing history.                          | The proof of concept admits `supersedes` only toward later versions and rejects competing successors.  | There is still no temporal reasoner wired into live memory.                                |
| Show growth without turning the graph into truth.              | A 3D viewer, regenerable from sanitized JSON and accompanied by a text alternative.                    | The viewer neither validates relations nor represents a mind.                              |

The difference may look small, but it changes the question. Knowing **which fragment sits close to a query** is no longer enough; what matters as well is **what kind of evidence it is and under what conditions it can be reused**.

### What memory actually exists

The PoC brings several layers together, but does not treat them as equivalent:

* **`penta-agent` experience:** 16,955 indexed points and 1,432 strategies make it possible to explore actions, corrections, and failures. Semantic closeness proves neither causality nor truth.
* **Curated context:** 319 canonical records make it possible to retrieve *handoffs* and decisions with their provenance. The index helps to find them, but does not replace the original record.
* **Research process:** a projection with 796 derived artifacts and 533 links makes it possible to inspect the work trajectory without publishing documents or microdata.
* **Personal mail:** the local inventory holds 12,072 unique messages between 2011 and 2026. It serves to test reading and deduplication within an authorized scope; it is not a public corpus and not a personality model.
* **Experimental personal memory:** a separate prototype tests retrieval through `mbox`, SQLite/FTS, scopes, and purge. There is still no authorization to generate answers out of sensitive mail.

This separation heads off a frequent temptation: confusing **having technical access to a source** with **being authorized to turn it into reusable memory**.

### A useful failure

The pipeline itself supplied an example of why provenance matters. The historical exporter expected a plain vector, while the current index stored the named `dense` vector. The first regeneration produced a degraded graph, with no semantic edges. A run against the real index caught the incompatibility and, once the exporter was fixed, 3,658 edges came back.

The lesson matters more than the number: **an auditable visualization has to be able to show when its data chain degraded, why it happened, and how it was put back together**. It is a real use case.

### From command to task

The 1,432 recorded strategies are still the basic unit of this memory. Many of them started life as commands, so I added a deterministic classification to make them more readable: coordinating agents (399), researching and analyzing (396), tracing evidence (385), executing or automating (118), versioning changes (76), verifying (28), operating infrastructure (18), and communicating results (12).

A strategy could belong to several categories, but today it lands in the first matching rule. **It is a lens for walking through the memory, not a description of the person behind it.** There is plenty of room to improve this with other visualizations; if you know of one, I would be grateful for the tip.

---

## Spoonful 2: governing sources before blending them

The architecture starts from a simple separation. The **canonical record** (the *ledger*) and the source files hold the evidence; Qdrant keeps indexes that can be destroyed and regenerated; the viewer publishes a sanitized projection; and the private adapters stay outside Git. The index is there to find things. It has no authority to turn a vector match, on its own, into a durable fact.

### An architecture of permissions, not a blender

Mail, thesis material (from the master's degree), and operational memory may all be technically readable by the same system, but that does not make them interchangeable. In this PoC, only the previously curated context may feed cross-agent retrieval and the public projection. Mail stays in a private, reversible, revocable circuit; the thesis contributes authorized process metadata and nothing else.

The distinction matters: **having technical access to a piece of data does not settle whether reusing it for any purpose is legitimate**. Contextual integrity theory poses exactly this problem: privacy depends not only on the data, but also on the context, the actors, and the norms that govern its circulation [^nissenbaum-2004].

<figure class="align-center">

  <a href="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources.svg' | relative_url }}" target="_blank" rel="noopener">

<img src="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/governed-sources.svg' | relative_url }}" alt="Three governed sources: operational memory allows retrieval with provenance; personal mail allows only private, reversible review; master's thesis material and documents allow citations and verification status. With a boundary that blocks publishing mail bodies, attachments, addresses, absolute paths, microdata, and inferences about identity." loading="lazy" decoding="async">

  </a>

  <figcaption>Figure 1. The current integration is an architecture of permissions: each source determines which outputs are permitted.</figcaption>

</figure>

The thesis is a good example. What enters the public system is a [snapshot of the research index]({{ '/assets/data/memoria_gobernada/thesis-research-index-snapshot.json' | relative_url }}), not the corpus. The August 29 cut holds 796 derived textual artifacts — 316 audits, 244 reports, 133 contracts, 71 pseudocode files, and 32 inventory, replication, or documentation pieces — plus 533 links and 7 open leads. It leaves out the source documents, DTA, Parquet, PDF, images, paths, full texts, and microdata. The search is deliberately lexical: FTS5 and TF-IDF help to find artifacts, but they make no claim to understand the research.

There is a detail more interesting than the figures. The published snapshot is still faithful to the cut it declares: its fingerprint matches the manifest of that moment. The corpus, however, kept growing and reached 817 documents, twenty-one more. Since the index was not regenerated, the currency gate is red: `check-research-index` returns `2`, because `document_count` and `source_fingerprint` no longer match the current state.

That does not invalidate the snapshot; it **dates** it. Its correct status is "valid for the August 29 cut, but not current with respect to today's corpus". A gate that had stayed green after the corpus grew would have been worse than a failed gate: it would have certified a currency that does not exist. This is the formal record of the memory's growth and potential divergence.
{: .notice--warning}

### Reuse before reinventing

None of this requires building every memory component from scratch. In fact, a good sign of maturity would be being able to **delete my own code** when an existing tool solves the same problem better without degrading privacy, provenance, or reversibility.

To recover decisions scattered across coding sessions, `deja-vu` already indexes the local histories of many agents and exposes them through a CLI and MCP. It is a natural candidate to contrast against my own *handoffs* and events before writing yet another equivalent layer.

For more structured persistent memory there are more ambitious approaches. MemGPT introduced the idea of managing distinct memory tiers as a way of extending an agent's effective context [^packer-2023]; Letta's current line carries that principle into editable memory blocks and external memory. Mem0 automates the extraction, consolidation, and retrieval of information from conversations [^chhikara-2025], while Hindsight distinguishes the operations of **retaining, recalling, and reflecting**, taking in semantic, lexical, temporal, and graph-based retrieval [^latimer-2025].

The **currency** problem deserves an experiment of its own. Graphiti, the open component described in Zep's architecture, explicitly models relations that change over time and keeps historical information instead of silently replacing it [^rasmussen-2025]. That comes far closer to the problem I am trying to solve with `supersedes` than piling on more temporal rules of my own.

For document collections, Microsoft GraphRAG offers another useful idea: build a graph derived from the corpus and summarize communities to answer global questions that a conventional RAG handles worse [^edge-2024]. I would not use it yet as a replacement for the thesis index. First it would have to show, over a bounded scientific subset, that the added complexity and cost improve something the lexical baseline cannot resolve.

Visualization, finally, is a practically solved problem: `3d-force-graph` already provides a three-dimensional layout built on Three.js and force algorithms. The relevant part of this PoC is not writing another graphics engine, but controlling **which graph the browser receives** and remembering that visual distance proves neither conceptual proximity, nor causality, nor human affinity.

The common rule is simple: **test components, do not collect them**. That a library can remember more does not mean it should receive more data.

There is also a conflict of interest worth making explicit. Mem0, Hindsight, Zep/Graphiti, and Letta are described in large part by their own teams. Their papers and repositories are appropriate sources for learning the architectures they propose, but their comparative results are not independent validation of superiority. I use them here as designs that deserve a contrast, not as winners of a competition — and my own stack is not superior either. If anything, mine is rather experimental, built for my own purposes.

### A retrieval experiment that could fail

I tested `Qwen3-Embedding-0.6B` on an isolated copy of 319 contexts, without touching production. The evaluation used 40 queries, eight of them designed to check that the system also knew how **not to retrieve evidence when it should not**.

The best configuration got **38 complete cases, 2 partials, and no outright miss** within the top five positions. From there I tried several possible improvements:

* dropping the BM25 lexical boost held the best result;
* adding a generic instruction to the *embedding* made both retrieval and abstention worse;
* `Qwen3-Reranker-0.6B` ordered the results somewhat better, but pushed response time up too far;
* diversifying by repository and fusing rankings did not resolve the two partial cases either.

The experiment left a conclusion more useful than finding a new model: **the two open cases do not seem to need more power, but better metadata**. Both of them require retrieving documents from different families within only five results.

So the next test will be to add explicit information about **lineage and document intent**, without using the correct answers to build those labels. Arbitrarily raising `k` or piling on more models would only have moved the problem elsewhere.

Until those two cases are resolved reproducibly, the collection stays in `staging`. In this system, **remembering that an improvement has not been demonstrated yet is also part of the memory**.

## Spoonful 3: a map that does not pass itself off as a mind

Once what may enter the memory is sorted out, another question remains: **how do you show it without mistaking a representation for reality?**

The viewer answers with a precaution: it queries neither Qdrant (the database where the vectors are indexed) nor any private source when someone opens the site — it **receives a sanitized JSON** (a data file from which the information that must not be published has been removed), generated from a specific cut of the memory.

That way the graph can be rebuilt and audited without touching the original sources again. The [public JSON export]({{ '/assets/data/rag_knowledge_graph/public-graph.json' | relative_url }}) even lets you inspect directly what information the browser receives.

### Seeing the network without attributing more to it than it says

The August 29 cut holds **1,432 strategies, 3,949 relations, and eight task families**, derived from 16,955 indexed points.

The image below **is not that network**: it is an illustration, and the percentage is the joke. The real network is explored in the full viewer, which lets you select tasks, projects, and errors.

<figure class="align-center">

  <a href="{{ '/assets/visualizations/penta-rag-knowledge-graph/index.html' | relative_url }}" target="_blank" rel="noopener">
    <img src="{{ '/assets/images/multiagente-penta-agent-memoria-gobernada/cerebro-20-por-ciento-1600x1000.webp' | relative_url }}"
         alt="Illustration: half the silhouette of a brain, made of points and edges, coming apart toward the right into loose points, with a loading bar stopped at 20%."
         loading="lazy"
         decoding="async">
  </a>

  <figcaption>
    Figure 2. An illustration, not a projection of the data: the digital-clone metaphor loaded to 20%. The network hints at itself where there is density and comes apart where there is none, which is exactly what an index knows how to do. The real projection, with its nodes and edges, is in the viewer.
  </figcaption>

</figure>

[**Open the interactive viewer in a new tab →**]({{ '/assets/visualizations/penta-rag-knowledge-graph/index.html' | relative_url }})
{: .text-center}

It is worth reading with some precautions. A **node** (a point in the graph) stands for a recorded strategy. An **edge** (a line between two nodes) stands for some derived relation: semantic similarity, a shared tool, or a correction, for instance. A **community** (a group of nodes that appears especially well connected) helps you get your bearings inside the network.

None of those relations proves, on its own, causality, truth, or a trait of the person who used the system. Mail and private documents do not appear as content nodes either.

The numbers belong, moreover, to a dated cut. Updating the memory does not silently change the graph: the projection has to be regenerated, sanitized again, and its differences reviewed before it is published anew.

**The viewer is not the memory. It is barely a map built from one of its projections.**

### Retrieving a source is not enough either

Finding the right document is only half the problem. The system also has to **use the right source, respect its scope, and abstain when the evidence falls short**.

To test that layer I built `context-answer-v1`, a small set of 18 cases: 12 with sufficient evidence and 6 in which the right answer was to claim no more than what was available. The deterministic test passed all 18 cases and confirmed that the gate works; it still does not prove that a generative model answers well on its own.

The tests with external models also left a practical rule. Only the sources authorized to leave the machine should be evaluated outside it. The exportable subset passed 11/11 cases; another seven sources stayed `local_only` and require an evaluation inside the local environment.

The conclusion is simple: **retrieving is not enough; every answer has to carry provenance, permissions, and the ability to abstain**. Until that local evaluation and its human review are complete, I can talk about a governed and attributable memory, but not yet about a reliable generative memory.

---

## Closing: a useful memory before a digital clone

The "digital clone" is still some way off; today it is a distant horizon. What is missing, at a minimum: a temporal memory able to correct itself, revocable preferences and limits, evidence of authorship, behavior evaluated in new situations, and "human" or higher control over what is kept, shared, or deleted. MemGPT[^packer-2023] and the generative agents of Park et al.[^park-2023] offer influential architectures for handling context, memories, reflection, and planning, but they do not turn those functions into identity (Packer et al. 2023; Park et al. 2023).

In this third part, `penta-agent` is a local prototype of governed memory: it keeps experience, records corrections, exposes a bounded public projection, and lets its own tests fail without disturbing production.

The next step forward is not adding more nodes. It is closing the local answer evaluation and comparing alternatives — Graphiti, GraphRAG, or `deja-vu` — under the same cut, the same permissions, and observable output criteria. I am very much open to your comments and usage experience; I think one practical point of comparison would serve me better than going on testing the many tools that appear day after day.

---

## References

### Further reading

Works that guided this piece and that this version no longer cites in the body.
They are kept because losing track of what was read is worse than declaring it.

Cormack, Gordon V., Charles L. A. Clarke, and Stefan Büttcher. 2009. "Reciprocal Rank Fusion Outperforms Condorcet and Individual Rank Learning Methods". In *Proceedings of the 32nd Annual International ACM SIGIR Conference on Research and Development in Information Retrieval*, 758–59. New York: Association for Computing Machinery. <https://doi.org/10.1145/1571941.1572114>.

Wu, Di, Hongwei Wang, Wenhao Yu, Yuwei Zhang, Kai-Wei Chang, and Dong Yu. 2024. "LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory". arXiv, October 14, 2024; revised March 4, 2025. Accepted at ICLR 2025. <https://arxiv.org/abs/2410.10813>.

Wu, Di, Zixiang Ji, Asmi Kawatkar, Bryan Kwan, Jia-Chen Gu, Nanyun Peng, and Kai-Wei Chang. 2026. "LongMemEval-V2: Evaluating Long-Term Agent Memory Toward Experienced Colleagues". Work in progress, arXiv, May 12, 2026. <https://arxiv.org/abs/2605.06304>.

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

> **Conflicts of interest in the sources.** The model cards, the repositories, and several of the systems papers are written by their own developers or by organizations that offer related services; LongMemEval-V2, moreover, is still declared work in progress. They are used here to document architecture, declared functions, and maintenance status, not to accept claims of superiority. `penta-agent`'s own metrics are likewise evidence produced by the project itself, and they require reproducible artifacts and independent review before they can support general comparisons.
{: .notice--info}

[^chhikara-2025]: Chhikara, Prateek, Dev Khant, Saket Aryan, Taranjeet Singh, and Deshraj Yadav. 2025. "Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory". arXiv, April 28, 2025. <https://arxiv.org/abs/2504.19413>.

[^edge-2024]: Edge, Darren, Ha Trinh, Newman Cheng, Joshua Bradley, Alex Chao, Apurva Mody, Steven Truitt, Dasha Metropolitansky, Robert Osazuwa Ness, and Jonathan Larson. 2024. "From Local to Global: A GraphRAG Approach to Query-Focused Summarization". arXiv, April 24, 2024; revised February 19, 2025. <https://arxiv.org/abs/2404.16130>.

[^hu-2025]: Hu, Yuyang, Shichun Liu, Yanwei Yue, Guibin Zhang, Boyang Liu, Fangyi Zhu, Jiahang Lin, et al. 2025. "Memory in the Age of AI Agents". arXiv, December 15, 2025. <https://arxiv.org/abs/2512.13564>.

[^latimer-2025]: Latimer, Chris, Nicoló Boschi, Andrew Neeser, Chris Bartholomew, Gaurav Srivastava, Xuan Wang, and Naren Ramakrishnan. 2025. "Hindsight Is 20/20: Building Agent Memory That Retains, Recalls, and Reflects". arXiv, December 16, 2025. <https://arxiv.org/abs/2512.12818>.

[^lebo-2013]: Lebo, Timothy, Satya Sahoo, and Deborah McGuinness, eds. 2013. *PROV-O: The PROV Ontology*. W3C Recommendation, April 30, 2013. <https://www.w3.org/TR/prov-o/>.

[^nissenbaum-2004]: Nissenbaum, Helen. 2004. "Privacy as Contextual Integrity". *Washington Law Review* 79, no. 1: 119–58. <https://digitalcommons.law.uw.edu/wlr/vol79/iss1/10/>.

[^packer-2023]: Packer, Charles, Sarah Wooders, Kevin Lin, Vivian Fang, Shishir G. Patil, Ion Stoica, and Joseph E. Gonzalez. 2023. "MemGPT: Towards LLMs as Operating Systems". arXiv, October 12, 2023; revised February 12, 2024. <https://doi.org/10.48550/arXiv.2310.08560>.

[^park-2023]: Park, Joon Sung, Joseph C. O'Brien, Carrie J. Cai, Meredith Ringel Morris, Percy Liang, and Michael S. Bernstein. 2023. "Generative Agents: Interactive Simulacra of Human Behavior". In *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology*, article 2, 1–22. New York: Association for Computing Machinery. <https://doi.org/10.1145/3586183.3606763>.

[^rasmussen-2025]: Rasmussen, Preston, Pavlo Paliychuk, Travis Beauvais, Jack Ryan, and Daniel Chalef. 2025. "Zep: A Temporal Knowledge Graph Architecture for Agent Memory". arXiv, January 20, 2025. <https://arxiv.org/abs/2501.13956>.
