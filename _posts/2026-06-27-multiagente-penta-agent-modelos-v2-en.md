---
layout: single
title: "Multi-agent work in three spoonfuls: what worked for me and what did not"
subtitle: "A practical note on Codex, Claude, Gemini/Antigravity, Copilot, MCP, skills, and handoffs in my daily workflow"
date: 2026-06-27 00:00:00 +0000
categories: [ai, productivity, development, multi-agent]
tags: [multi-agent, agentic-coding, context-engineering, codex, claude-code, gemini, antigravity, copilot, litellm, deepseek, zai, mcp, skills, agents-md, vscode, arch-linux]
description: "A situated experience with penta-agent: what has helped me coordinate agents for memos, regulation, statistics, home automation, self-hosting, and local security, without selling it as a universal recipe."
author: clabra
lang: en
ref: multiagente-penta-agent-modelos
permalink: /ia/productividad/desarrollo/multiagente-penta-agent-modelos/
toc: true
toc_sticky: true
comments: true
author_profile: true
---

This started as a practical annoyance: long tasks interrupted by quota limits, conversations that became too heavy, and reviews that required copying context across windows in clumsy and inefficient ways. To deal with that, I built a multi-agent workflow in VS Code, on Arch Linux. I first called it tri-agent; after a couple of months it became `penta-agent`, a still imperfect way of coordinating agents, roles, permissions, and traces in my own workflow.
{: .text-justify}

It is not a new idea, and it is not a promise of full autonomy. In fact, maintaining it takes work. But it is a local work contract that orders who executes, who reviews, when MCP is used, when Gemini/Antigravity enters, when Copilot remains only support, which skills are loaded, and what evidence or artifact should exist at the end.
{: .text-justify}

I am writing from my own cases: memos, regulatory review, spreadsheets, statistical models, scripts for a home server, system timers, self-hosted cloud, router security, backups, this blog, and everyday maintenance. In those cases, having some agentic governance has helped me. Maybe it is also a false sense of digital sovereignty. I am not immune to that.
{: .text-justify}

The thesis is simple: a multi-agent system without roles, permissions, and traces may look sophisticated, but in practice it can feel too much like a meeting without minutes.
{: .text-justify}

**Three ideas to start with:**

- **Codex has worked for me as the main executor**: it reads files, applies patches, runs validations, and can close diffs with evidence. It is not infallible, so it should not be the only validator on critical changes.
- **Claude has worked for me as a strong reviewer, especially with Opus**: architecture, regulation, statistical assumptions, and argumentative risks. I use it as a brake and as support for the main executor.
- **Gemini/Antigravity, Copilot, and LiteLLM with DeepSeek and Z.ai work better when bounded**: exploration, validation, canary work, or small tasks. When they start deciding with too little context, the workflow gets worse.

## Spoonful 1: the problem was not using agents, it was losing continuity

In a long task, the cost of a pause is not only the time without an answer. The expensive part is losing continuity: what was being tested, what file changed, which hypothesis failed, which validation remained pending, and which context should no longer be dragged along.
{: .text-justify}

My first mistake was treating each model or agent as a symmetric second opinion. That does not scale. In a memo or a regulatory review, I ended up with useful comments that were hard to reconcile.
{: .text-justify}

The fix was more boring and more useful: separate roles. Not because it is the right way for everyone, but because in my workflow it lowers the cost of returning to a task without having to recap everything from scratch.
{: .text-justify}

I read provider convergence from there. Codex documents configuration, sandboxing, permissions, MCP, `AGENTS.md`, skills, and subagents; GitHub Copilot supports repository instructions; Gemini Code Assist describes an agent mode with tools, MCP, and approval of changes; and Claude Code exposes hooks such as `PreToolUse`, `PostToolUse`, and `SessionStart`.[^openai-config][^github-instructions][^gemini-agent][^claude-hooks]
{: .text-justify}

{: .table-caption}
**Table 2** — Current roles in `penta-agent`

| Component | Actual role | Limit I impose |
|---|---|---|
| ChatGPT/Codex | Local technical orchestrator, planner, and executor | It should not self-validate as the only source of truth on critical changes |
| Claude | Reviewer, auditor, and co-planner | It should not take operational control by default |
| Gemini/Antigravity | Explorer, validator, and fallback | It should not enter the critical path unless explicitly promoted |
| Copilot | Canary and IDE/GitHub-native support | It should not be treated as an independent architectural arbiter |
| LiteLLM sidecar | Cheap, narrow delegation | I do not use it for architecture, security, or final decisions; today I use it in bounded ways with DeepSeek and Z.ai |
| Human | Closure, privacy, and acceptance | Final judgment is not delegated when risk is involved |

The local architecture makes that explicit. In `routing.yaml`, the `penta_agent_ops` rule keeps Codex as `primary`, Claude as `reviewer`, Gemini as validator/fallback, and the human as checkpoint:

```yaml
id: penta_agent_ops
planner: codex
primary: codex
reviewer: claude
escalate_to: human
validator_chain: [gemini]
fallback_chain: [gemini]
planning:
  proactive_skills: [handoff-protocol, recall-context]
  mcp_policy:
    mode: conditional
    allowed_paths: [claude_to_codex_mcp, gemini_to_codex_mcp]
  provider_roles:
    planning_sidecars:
      canary: copilot
```

The key detail is `mcp_policy.mode: conditional`. Not everything goes through MCP. Not everything deserves a handoff. Not everything deserves a second provider. After some iterations, I made evaluation proactive, as with skills, but invocation still needs a signal. Early on, skills were not activated when I wanted them to be, and handoffs were scarce.
{: .text-justify}

---

## Spoonful 2: the repository as a work contract

The piece that helped me most was not a model. It was a startup rule: if a task touches multi-agent work, MCP, Claude, Gemini, Copilot, routing, handoffs, or `penta-agent`, first read the local canon.
{: .text-justify}

In my case, that canon lives in files such as:

- `router/routing.yaml`
- `shared-references/arquitectura-multiagente.md`
- `playbooks/puente-mcp-codex.md`
- `.mcp.json`

This prevents a common vice: generic probing of CLIs, models, and commands before understanding the project's contract. For small things, it may not matter. For a regulatory review, a statistical run, or a local security change, it does. Drift burns tokens and sometimes leaves the task stranded in the wrong place.
{: .text-justify}

A useful `AGENTS.md` does not need to be a novel. Long instructions consume context. I think it should mostly prevent bad practices:

```markdown
# Workspace multi-agent rules

If the user mentions multi-agent work, MCP, Claude, Gemini,
Copilot, routing, handoff, or penta-agent:

1. Use `penta-agent/` as the source of truth.
2. Read routing, architecture, MCP bridge, and MCP config first.
3. Do not probe generic CLIs before reading the canon.
4. Delegate to Antigravity only through `scripts/agent/agy-bridge`.
5. Do not send secrets, `.env`, keys, or credentials to external providers.
```

Recent literature seems to move in a similar direction, with a healthy warning. Galster et al. describe these artifacts as versionable mechanisms for configuring agentic tools and observe that `AGENTS.md` is emerging as an interoperable standard.[^galster-config] Arabat and Sayagh propose treating them as instructions-as-code, not as side notes.[^instructions-code] On the other hand, Gloaguen et al. warn that context files can reduce success and increase cost when they add unnecessary requirements.[^agents-md-eval] My experience is that the balance must be tuned constantly.
{: .text-justify}

### Skills: procedures, not endless prompts

Skills have helped me when they act as reusable procedures with clear activation rules, limits, and references. A publishing skill, for example, should not say "write nicely." It should say verifiable things:

```yaml
name: jekyll-post
description: Jekyll posts with front matter, drafts/posts workflow, build checks, and reproducible publication.
```

```markdown
- Prepare correct front matter and validate the build.
- Keep claims dated and traceable.
- Review front matter and the editorial guide.
```

The minimum question for a skill is: when does it activate, what must it not do, which files must it read, and what output makes it possible to verify that it did the job well. That fits Anthropic's progressive-loading model: metadata first, instructions when the skill activates, and resources or scripts only if needed.[^claude-skills] It also fits SkillJuror, which shows that skill organization changes how agents search for and apply knowledge, although the benefit depends on whether resources are actionable.[^skilljuror]
{: .text-justify}

The security warning matters too: `SKILL.md` is not passive documentation.[^skill-supply-chain] If a skill brings scripts, ambiguous instructions, or manipulable metadata, it is closer to installing software than to pasting an innocent prompt.
{: .text-justify}

### MCP: a bridge, but I still do not squeeze it fully

The real MCP surface in `penta-agent` is deliberately small:

```json
{
  "mcpServers": {
    "codex": {
      "type": "stdio",
      "command": "scripts/codex_mcp.sh",
      "args": ["mcp-server"],
      "env": {}
    }
  }
}
```

The idea is not that every agent connects to every other agent. The preferred path is **Claude/Gemini to Codex** when they need filesystem access, commands, tests, or local edits. Codex to Claude or Antigravity uses controlled CLI/file handoffs. I do not assume a bidirectional bridge or a universal `filesystem` MCP baseline.
{: .text-justify}

That is also a security decision. MCP's official security guidance lists risks such as confused deputy, token passthrough, SSRF, session hijacking, and local server compromise.[^mcp-security] Recent work on tool poisoning in MCP argues that the critical problem is often on the client side: malicious metadata, low parameter visibility, and implicit trust.[^mcp-threat] I still do not get all the value from MCP, but I prefer it narrow.
{: .text-justify}

### Handoffs: the antidote to "I told them"

A handoff is not saying "let Claude review it." A useful handoff leaves a minimal trace:

```text
HANDOFF-TRACE: codex asks claude for support (model: sonnet) via CLI
MODEL-REPORT: {"agent":"codex","provider":"openai","model":"__default__","source":"self_report"}
MODEL-REPORT: {"agent":"claude","provider":"anthropic","model":"sonnet","source":"self_report"}
```

And it separates the basics:

```yaml
metadata:
  from: codex
  to: claude
  via: CLI
  skill: handoff-protocol

essential_context:
  - what was done
  - what was rejected
  - what remains to validate

task_for_receiver:
  - review claims
  - detect risks
  - do not modify files

verification:
  - tests run
  - sources checked
  - final decision
```

This feels bureaucratic until something fails. When it fails, the trace helps answer whether the problem was insufficient context, wrong model, bad route, ambiguous output, quota, permissions, sandboxing, or a poorly written instruction. OpenAI proposes a similar logic in its agent improvement loop: use traces, feedback, and evals to modify the harness, not only to ask the model to "do better."[^openai-loop] This has also helped me use `recall-context`: with a good trace, previous work is much easier to recover across agents.
{: .text-justify}

---

## Spoonful 3: what I learned by making it fail

My own error list is more useful than a list of tools. I hope this post reads more like a logbook than a showcase. It will probably age quickly, but perhaps it will be useful to someone else.
{: .text-justify}

{: .table-caption}
**Table 3** — My mistakes and current controls

| Mistake | What it looked like | Current control |
|---|---|---|
| Treating models as equivalent | Any provider could comment on anything | Explicit roles: primary, reviewer, explorer, validator, canary |
| Automatic fan-out | I asked for second opinions out of habit | Always evaluate, invoke only with enough signal |
| Fragile model IDs | A rename broke scripts or examples | Use `__default__`, aliases, and discovery |
| Declaring a sidecar ready too early | The proxy started, but the provider failed by quota or balance | Separate "proxy is alive" from "provider is usable" |
| Overlong context files | The agent followed irrelevant rules and explored too much | Minimal, actionable, dated instructions |
| MCP as a universal solution | More servers, more implicit trust | Conditional MCP, consent, sandboxing, and minimal permissions |
| Vector memory as source of truth | Drift risk from dimensions or derived indexes | JSONL as source; Qdrant/FastEmbed as rebuildable indexes |
| Copilot as a strong second provider | It did not always add independent judgment | Use it as canary/support, not as arbiter |

Memory deserves a paragraph. In `penta-agent`, operational memory lives in append-only files such as `experience-events.jsonl`, `experience-lessons.yaml`, and `interaction-metrics.jsonl`. Qdrant and FastEmbed help retrieve experiences, but they are derivatives. If embeddings change or a dimension mismatch appears, the index is rebuilt from JSONL. After fighting that kind of drift, I do not want the source of truth to be fragile.
{: .text-justify}

The LiteLLM sidecar follows the same philosophy. It is useful for cheap, narrow delegation to aliases such as `cheap`, `cheap-code`, or `cheap-reasoner`, but not for architecture, security, or final decisions. The real provider smoke test matters more than a healthy container. If DeepSeek returns `Insufficient Balance`, the system is not ready; we have only learned that Docker can turn on a light.
{: .text-justify}

---

## Closing: an optimization loop

My stack should not be read as a universal template. It is not one. What may be useful is the logic behind it: small contracts so the work does not depend on human memory or on the enthusiasm of the moment. I published a sanitized public version of the stack at [`tatanlabra/penta-agent`](https://github.com/tatanlabra/penta-agent). It is not a dump of my local environment: I removed runtime memory, private paths, logs, `.env` files, credentials, internal IPs, and anything that could reveal personal configuration. Anyone cloning it should treat it as a template and review the placeholders in `AGENTS.md`, `.mcp.json`, `router/routing.yaml`, `scripts/agent/agy-bridge`, and `skills/` before using it.
{: .text-justify}

`penta-agent` has helped me not because it has many agents, but because it has brakes: roles, routes, skills, permissions, handoffs, rebuildable memory, and validation. That does not make it universal or superior. It makes it auditable for my problems. _Vibe coding_ names the first feeling of flow well: ask, watch code appear, correct, continue. But when the workflow matures, the question changes: how efficient, elegant, and verifiable is the solution you get?
{: .text-justify}

---

## Technical References

[^openai-config]: OpenAI Developers, "Configuration Reference -- Codex," accessed June 21, 2026. It documents configuration, permissions, sandboxing, MCP, `AGENTS.md`, skills, and subagents in Codex. <https://developers.openai.com/codex/config-reference>

[^openai-loop]: OpenAI Cookbook, "Build an Agent Improvement Loop with Traces, Evals, and Codex," accessed June 21, 2026. It uses traces, feedback, evals, and harness configuration to improve agents. <https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop>

[^claude-hooks]: Anthropic, "Hooks reference -- Claude Code Docs," accessed June 21, 2026. It describes hooks as lifecycle control points, including `PreToolUse`, `PostToolUse`, and `SessionStart`. <https://code.claude.com/docs/en/hooks>

[^claude-skills]: Anthropic, "Agent Skills -- Claude API Docs," accessed June 21, 2026. It describes skills as modular capabilities with instructions, metadata, scripts, and references loaded in stages. <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>

[^github-instructions]: GitHub Docs, "Adding repository custom instructions for GitHub Copilot," accessed June 21, 2026. It documents repository instructions and formats associated with Copilot. <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions>

[^gemini-agent]: Google Developers, "Use the Gemini Code Assist agent mode," accessed June 21, 2026. It describes agent mode in the IDE, tool use, MCP, and action approval. <https://developers.google.com/gemini-code-assist/docs/use-agentic-chat-pair-programmer>

[^galster-config]: Matthias Galster et al., "Configuring Agentic AI Coding Tools: An Exploratory Study," arXiv:2602.14690, 2026. It analyzes mechanisms such as context files, skills, subagents, hooks, settings, and MCP. <https://arxiv.org/abs/2602.14690>

[^agents-md-eval]: Thibaud Gloaguen et al., "Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?," arXiv:2602.11988, 2026. It reports that context files can reduce success and increase cost when they add unnecessary requirements. <https://arxiv.org/abs/2602.11988>

[^instructions-code]: Ali Arabat and Mohammed Sayagh, "Toward Instructions-as-Code: Understanding the Impact of Instruction Files on Agentic Pull Requests," arXiv:2606.13449, 2026. It analyzes agentic pull requests and concludes that instructions do not automatically improve performance. <https://arxiv.org/abs/2606.13449>

[^skilljuror]: Zhiyu Chen et al., "SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior," arXiv:2606.11543, 2026. It evaluates skill organization and progressive loading. <https://arxiv.org/abs/2606.11543>

[^skill-supply-chain]: Shoumik Saha, Kazem Faghih, and Soheil Feizi, "Under the Hood of SKILL.md: Semantic Supply-chain Attacks on AI Agent Skill Registry," arXiv:2605.11418, 2026. It warns that `SKILL.md` metadata and instructions can manipulate skill discovery, selection, and governance. <https://arxiv.org/abs/2605.11418>

[^mcp-security]: Model Context Protocol, "Security Best Practices," accessed June 21, 2026. It lists risks and mitigations for MCP implementations. <https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices>

[^mcp-threat]: Charoes Huang, Xin Huang, Ngoc Phu Tran, and Amin Milani Fard, "Model Context Protocol Threat Modeling and Analyzing Vulnerabilities to Prompt Injection with Tool Poisoning," arXiv:2603.22489, 2026. It applies STRIDE/DREAD to MCP and highlights tool poisoning as a critical client-side vulnerability. <https://arxiv.org/abs/2603.22489>

---
