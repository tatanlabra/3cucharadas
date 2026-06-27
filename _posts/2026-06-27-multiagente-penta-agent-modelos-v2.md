---
layout: single
title: "Multiagentes en 3 cucharadas: lo que me funcionó y lo que no"
subtitle: "Una bitácora práctica sobre Codex, Claude, Gemini/Antigravity, Copilot, MCP, skills y handoffs en mi flujo diario"
date: 2026-06-27 00:00:00 +0000
categories: [ia, productividad, desarrollo, multiagente]
tags: [multiagente, agentic-coding, context-engineering, codex, claude-code, gemini, antigravity, copilot, litellm, deepseek, zai, mcp, skills, agents-md, vscode, arch-linux]
description: "Una experiencia situada con penta-agent: qué me ha servido para coordinar agentes en minutas, normativa, estadística, automatización doméstica, nube propia y seguridad local, sin venderlo como receta universal."
author: clabra
lang: es
ref: multiagente-penta-agent-modelos
permalink: /ia/productividad/desarrollo/multiagente-penta-agent-modelos/
toc: true
toc_sticky: true
comments: true
author_profile: true
---

Esto empezó como una molestia práctica: tareas largas que se cortaban por cuota, conversaciones que quedaban demasiado cargadas y revisiones que exigían copiar contexto entre ventanas de forma incómoda e ineficiente. Para resolverlo armé un multiagente en VS Code, sobre Arch Linux, y llamé primero tri-agent y luego de un par de meses ya es `penta-agent`, una forma todavía imperfecta de coordinar agentes, roles, permisos y trazas dentro de mi flujo.
{: .text-justify}

No es algo nuevo ni una promesa de autonomía total, de hecho mantenerlo da harta pega. Pero, es un contrato local de trabajo que ordena quién ejecuta, quién revisa, cuándo se usa MCP, cuándo entra Gemini/Antigravity, cuándo Copilot queda como apoyo, qué skills se cargan y qué evidencia o producto queda al cierre.
{: .text-justify}

Lo cuento desde casos de uso concretos míos: minutas, revisión normativa, de planillas, modelos estadísticos, scripts de automatización en server de la casa, timers de sistema, nube propia, seguridad del router, backups, blog y mantenimiento cotidiano. En todos esos casos me ha servido tener algo de “gobernanza" agéntica. Quizás una falsa sensación de soberanía digital también.
{: .text-justify}

La tesis es simple: un sistema multiagente sin roles, permisos ni trazas puede parecer sofisticado, pero en la práctica se parece demasiado a una reunión sin acta.
{: .text-justify}

**Tres ideas para comenzar:**

- **Codex me ha funcionado como ejecutor principal**: lee archivos, aplica parches, corre validaciones y puede cerrar diffs con evidencia. No es infalible, por eso no debería autovalidarse en cambios críticos.
- **Claude me ha servido como revisor fuerte (sobre todo con Opus)**: revisa arquitectura, normativa, supuestos estadísticos y riesgos argumentales. Lo uso como freno, y apoyo al ejecutor principal.
- **Gemini/Antigravity, Copilot y LiteLLM (con DeepSeek y Z.ai) sirven mejor acotados**: exploración, validación, canary o tareas pequeñas. Cuando empiezan a decidir con poco contexto, el flujo empeora.

## Cucharada 1: el problema no era usar agentes, era no perder continuidad

En una tarea larga, el costo de una pausa no es solo el tiempo sin respuesta. Lo más caro es perder continuidad: qué se estaba probando, qué archivo cambió, qué hipótesis falló, qué validación quedó pendiente y qué contexto ya no conviene seguir arrastrando.
{: .text-justify}

Mi primer error fue tratar cada modelo/agente como una “segunda opinión” o validación simétrica. Eso no escala. En una minuta o una revisión normativa, terminaba con comentarios útiles pero difíciles de reconciliar.
{: .text-justify}

La solución fue más aburrida y más útil: separar roles. No porque sea “la” forma correcta para todo el mundo, sino porque en mi flujo baja el costo de volver a una tarea, sin recapitular era alto.
{: .text-justify}

Me sirve leer la convergencia de proveedores desde ahí. Codex documenta configuración, sandbox, permisos, MCP, `AGENTS.md`, skills y subagentes; GitHub Copilot admite instrucciones de repositorio; Gemini Code Assist describe un agent mode con herramientas, MCP y aprobación de cambios; y Claude Code permite hooks en puntos como `PreToolUse`, `PostToolUse` y `SessionStart`.[^openai-config][^github-instructions][^gemini-agent][^claude-hooks]
{: .text-justify}

{: .table-caption}
**Tabla 2** — Roles actuales en `penta-agent`

| Componente | Rol real | Límite que le impongo |
|---|---|---|
| ChatGPT/Codex | Orquestador técnico local, planner y ejecutor | No autovalidarse como única fuente de verdad en cambios críticos |
| Claude | Reviewer, auditor y co-planificador | No tomar control operativo por defecto |
| Gemini/Antigravity | Explorer, validator y fallback | No entrar al critical path salvo decisión explícita |
| Copilot | Canary y soporte IDE/GitHub-native | No tratarlo como árbitro arquitectónico independiente |
| LiteLLM sidecar | Delegación barata y estrecha | No usarlo para arquitectura, seguridad ni decisiones finales; hoy lo uso acotado con DeepSeek y Z.ai |
| Humano | Cierre, privacidad y aceptación | No delegar criterio final cuando hay riesgo |

La arquitectura local lo vuelve explícito. En `routing.yaml`, la regla `penta_agent_ops` mantiene a Codex como `primary`, a Claude como `reviewer`, a Gemini como validador/fallback y al humano como checkpoint:

```yaml
id: penta_agent_ops
planner: codex
primary: codex
reviewer: claude
escalate_to: humano
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

El detalle clave es `mcp_policy.mode: conditional`. No todo se manda por MCP. No todo merece handoff. No todo merece un segundo proveedor. La evaluación luego de algunas iteraciones la hice proactiva, al igual que con los skills, que los activadores fuesen bien explicitos. Al principio no se activaban cuando querían o los handoffs eran escasos.
{: .text-justify}

---

## Cucharada 2: el repositorio como contrato de trabajo

La pieza que más me ayudó no fue un modelo. Fue una regla de arranque: si una tarea toca multiagente, MCP, Claude, Gemini, Copilot, routing, handoffs o `penta-agent`, primero se lee el canon local.
{: .text-justify}

En mi caso, ese canon vive en archivos como:

- `router/routing.yaml`
- `shared-references/arquitectura-multiagente.md`
- `playbooks/puente-mcp-codex.md`
- `.mcp.json`

Esto evita un vicio frecuente: hacer uso genérico de CLIs, modelos y comandos antes de entender el "contrato" u objetivo del proyecto. En cosas chicas puede no importar. En una revisión normativa, una corrida estadística o un ajuste de seguridad local, sí importa, ya que la deriva gasta tokens como loco, y a veces termina varado en cualquier lugar.
{: .text-justify}

Un `AGENTS.md` útil no necesita ser una novela, gasta contexto, tiene que evitar malas prácticas creo yo:

```markdown
# Reglas multiagente del workspace

Si el usuario menciona trabajo multiagente, MCP, Claude, Gemini,
Copilot, routing, handoff o penta-agent:

1. Usar `penta-agent/` como source of truth.
2. Leer primero routing, arquitectura, puente MCP y configuración MCP.
3. No hacer probing genérico de CLIs antes de leer el canon.
4. Delegar a Antigravity solo mediante `scripts/agent/agy-bridge`.
5. No entregar secretos, `.env`, llaves ni credenciales a proveedores externos.
```

La literatura reciente pareciera ir en una dirección parecida, pero con una advertencia sana. Galster et al. describen estos artefactos como mecanismos versionables para configurar herramientas agenticas y observan que `AGENTS.md` emerge como estándar interoperable.[^galster-config] Arabat y Sayagh proponen mirarlos como “instructions-as-code”, no como notas al margen.[^instructions-code] Por otro lado, Gloaguen et al. advierten que los context files pueden reducir éxito y aumentar costo cuando agregan requisitos innecesarios.[^agents-md-eval] En mi experiencia, hay que buscar bien el equilibrio y estar dispuesto a tunear de forma constante.
{: .text-justify}

### Skills: procedimientos, no prompts eternos

Las skills me han servido cuando actúan como procedimientos reutilizables con activación clara, límites y referencias. Una skill de publicación, por ejemplo, no debería decir “escribe bonito”; debería decir cosas verificables:

```yaml
name: jekyll-post
description: Posts Jekyll con front matter, drafts/posts, build y publicacion reproducible.
```

```markdown
- Preparar front matter correcto y validar build.
- Mantener claims fechados y trazables.
- Revisar front matter y guía editorial.
```

La pregunta mínima para una skill es: cuándo se activa, qué no debe hacer, qué archivos debe leer y qué salida permite verificar que hizo bien su trabajo. Eso calza con la carga progresiva descrita por Anthropic: metadata primero, instrucciones cuando la skill se activa, y recursos o scripts solo si hacen falta.[^claude-skills] También calza con SkillJuror, que muestra que la organización de una skill cambia cómo los agentes buscan y aplican conocimiento, aunque el beneficio depende de que los recursos sean accionables.[^skilljuror]
{: .text-justify}

La advertencia de seguridad es igualmente importante: `SKILL.md` no es documentación pasiva.[^skill-supply-chain] Si una skill trae scripts, instrucciones ambiguas o metadata manipulable, se parece más a instalar software que a pegar un prompt inocente.
{: .text-justify}

### MCP: puente, pero aún no le saco el jugo

El MCP real de `penta-agent` es deliberadamente pequeño:

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

La idea no es que todos los agentes se conecten con todos. El camino preferido es **Claude/Gemini hacia Codex** cuando necesitan filesystem, comandos, tests o edición local. Codex hacia Claude o Antigravity usa CLI/handoff controlado. No asumo bridge bidireccional ni `filesystem` MCP universal.
{: .text-justify}

Esto también es una decisión de seguridad. La documentación oficial de MCP enumera riesgos como confused deputy, token passthrough, SSRF, secuestro de sesión y compromiso de servidores locales.[^mcp-security] La investigación reciente sobre tool poisoning en MCP insiste en que el problema crítico muchas veces está del lado cliente: metadata maliciosa, baja visibilidad de parámetros y confianza implícita.[^mcp-threat]. Aún no le saco todo el provecho.
{: .text-justify}

### Handoffs: el antídoto contra “yo le avisé”

Un handoff no es decir “que lo revise Claude”. Un handoff útil debe dejar rastro mínimo:

```text
HANDOFF-TRACE: codex le solicita apoyo a claude (model: sonnet) via CLI
MODEL-REPORT: {"agent":"codex","provider":"openai","model":"__default__","source":"self_report"}
MODEL-REPORT: {"agent":"claude","provider":"anthropic","model":"sonnet","source":"self_report"}
```

Y debe separar lo básico:

```yaml
metadata:
  from: codex
  to: claude
  via: CLI
  skill: handoff-protocol

contexto_esencial:
  - que se hizo
  - que se descarto
  - que falta validar

tarea_para_receptor:
  - revisar claims
  - detectar riesgos
  - no modificar archivos

verificacion:
  - pruebas corridas
  - fuentes consultadas
  - decision final
```

Esto parece burocracia hasta que algo falla. Cuando falla, la traza permite saber si el problema fue contexto insuficiente, modelo inadecuado, mala ruta, salida ambigua, cuota, permisos, sandbox o una instrucción mal escrita. OpenAI propone una lógica semejante en su loop de mejora de agentes: usar trazas, feedback y evaluaciones para modificar el arnés, no solo para pedirle al modelo que “lo haga mejor”.[^openai-loop] Esto me ha servido para usar la skill recall-context luego, ya que con una buena traza recupero trabajo previo de forma bien eficiente entre agentes.
{: .text-justify}

---

## Cucharada 3: lo que aprendí haciendo que fallara

La lista de errores propios vale más que la lista de herramientas. Este post más que vitrina, ojalá sirva de bitácora y probablemente añeje pronto, pero ojalá le sirva a más de alguien.
{: .text-justify}

{: .table-caption}
**Tabla 3** — Errores propios y controles actuales

| Error | Cómo se veía | Control actual |
|---|---|---|
| Tratar modelos como equivalentes | Cualquier proveedor podía opinar de cualquier cosa | Roles explícitos: primary, reviewer, explorer, validator, canary |
| Fan-out automático | Pedía segundas opiniones por costumbre | Evaluar siempre, invocar solo con señal suficiente |
| Model IDs frágiles | Un rename rompía scripts o ejemplos | Usar `__default__`, aliases y discovery diaria |
| Sidecar declarado listo demasiado pronto | El proxy arrancaba, pero el proveedor fallaba por saldo/cuota | Separar “proxy vivo” de “proveedor usable” |
| Context files demasiado largos | El agente obedecía reglas irrelevantes y exploraba de más | Instrucciones mínimas, accionables y fechadas |
| MCP como solución universal | Más servidores, más confianza implícita | MCP condicional, consentimiento, sandbox y mínimos permisos |
| Memoria vectorial como fuente de verdad | Riesgo de drift por dimensiones o índices derivados | JSONL como fuente; Qdrant/FastEmbed como índice reconstruible |
| Copilot como segundo proveedor fuerte | No siempre aporta independencia real | Usarlo como canary/support, no como árbitro |

La parte de memoria merece un párrafo. En `penta-agent`, la memoria operativa vive en archivos append-only como `experience-events.jsonl`, `experience-lessons.yaml` e `interaction-metrics.jsonl`. Qdrant y FastEmbed ayudan a recuperar experiencias, pero son derivados. Si cambia el embedding o aparece una dimensión incompatible, se reconstruye el índice desde JSONL. Después de pelear con ese tipo de drift, no quiero que la fuente de verdad sea frágil.
{: .text-justify}

El sidecar de LiteLLM sigue la misma filosofía. Sirve para delegar tareas baratas y acotadas a aliases como `cheap`, `cheap-code` o `cheap-reasoner`, pero no para arquitectura, seguridad ni decisiones finales. Además, el smoke real de proveedor importa más que el contenedor sano. Si DeepSeek responde `Insufficient Balance`, el sistema no está listo; solo aprendimos que Docker sabe prender una luz.
{: .text-justify}

---

## Cierre: bucle de optimización

No conviene mirar mi stack como si fuera plantilla universal, no lo es. Lo que sí puede servir es tomar elementos de la lógica: contratos pequeños para no depender de memoria humana ni de entusiasmo del momento. Dejé una versión pública y sanitizada del stack en [`tatanlabra/penta-agent`](https://github.com/tatanlabra/penta-agent). No es un volcado de mi entorno local: quité memoria runtime, rutas privadas, logs, `.env`, credenciales, IPs internas y cualquier cosa que pudiera revelar configuración personal. Quien lo clone debería tratarlo como plantilla y revisar los placeholders de `AGENTS.md`, `.mcp.json`, `router/routing.yaml`, `scripts/agent/agy-bridge` y `skills/` antes de usarlo.
{: .text-justify}

`penta-agent` me ha servido no porque tenga muchos agentes, sino porque tiene frenos: roles, rutas, skills, permisos, handoffs, memoria reconstruible y validación. Eso no lo vuelve universal ni superior. Lo vuelve auditable para mis problemas. El _vibe coding_ nombra bien la primera sensación de fluidez: pedir, ver aparecer código, corregir y seguir. Pero cuando el flujo madura, la pregunta cambia: qué tan eficiente, elegante y verificable es la solución que obtienes.
{: .text-justify}

---

## Referencias técnicas

[^openai-config]: OpenAI Developers, “Configuration Reference — Codex”, consultado el 21 de junio de 2026. Documenta configuración, permisos, sandbox, MCP, `AGENTS.md`, skills y subagentes en Codex. <https://developers.openai.com/codex/config-reference>

[^openai-loop]: OpenAI Cookbook, “Build an Agent Improvement Loop with Traces, Evals, and Codex”, consultado el 21 de junio de 2026. Usa trazas, feedback, evaluaciones y configuración del harness para mejorar agentes. <https://developers.openai.com/cookbook/examples/agents_sdk/agent_improvement_loop>

[^claude-hooks]: Anthropic, “Hooks reference — Claude Code Docs”, consultado el 21 de junio de 2026. Describe hooks como puntos de control del ciclo de vida, incluidos `PreToolUse`, `PostToolUse` y `SessionStart`. <https://code.claude.com/docs/en/hooks>

[^claude-skills]: Anthropic, “Agent Skills — Claude API Docs”, consultado el 21 de junio de 2026. Describe skills como capacidades modulares con instrucciones, metadata, scripts y referencias, cargadas por etapas. <https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview>

[^github-instructions]: GitHub Docs, “Adding repository custom instructions for GitHub Copilot”, consultado el 21 de junio de 2026. Documenta instrucciones de repositorio y formatos asociados a Copilot. <https://docs.github.com/en/copilot/how-tos/copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions>

[^gemini-agent]: Google Developers, “Use the Gemini Code Assist agent mode”, consultado el 21 de junio de 2026. Describe agent mode en IDE, uso de herramientas, MCP y aprobación de acciones. <https://developers.google.com/gemini-code-assist/docs/use-agentic-chat-pair-programmer>

[^galster-config]: Matthias Galster et al., “Configuring Agentic AI Coding Tools: An Exploratory Study”, arXiv:2602.14690, 2026. Analiza mecanismos como context files, skills, subagentes, hooks, settings y MCP. <https://arxiv.org/abs/2602.14690>

[^agents-md-eval]: Thibaud Gloaguen et al., “Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?”, arXiv:2602.11988, 2026. Reporta que context files pueden reducir éxito y elevar costo cuando agregan requisitos innecesarios. <https://arxiv.org/abs/2602.11988>

[^instructions-code]: Ali Arabat y Mohammed Sayagh, “Toward Instructions-as-Code: Understanding the Impact of Instruction Files on Agentic Pull Requests”, arXiv:2606.13449, 2026. Analiza pull requests agenticos y concluye que las instrucciones no mejoran automáticamente el desempeño. <https://arxiv.org/abs/2606.13449>

[^skilljuror]: Zhiyu Chen et al., “SkillJuror: Measuring How Agent Skill Organization Changes Runtime Behavior”, arXiv:2606.11543, 2026. Evalúa organización de skills y carga progresiva. <https://arxiv.org/abs/2606.11543>

[^skill-supply-chain]: Shoumik Saha, Kazem Faghih y Soheil Feizi, “Under the Hood of SKILL.md: Semantic Supply-chain Attacks on AI Agent Skill Registry”, arXiv:2605.11418, 2026. Advierte que la metadata e instrucciones de `SKILL.md` pueden manipular descubrimiento, selección y gobernanza de skills. <https://arxiv.org/abs/2605.11418>

[^mcp-security]: Model Context Protocol, “Security Best Practices”, consultado el 21 de junio de 2026. Enumera riesgos y mitigaciones para implementaciones MCP. <https://modelcontextprotocol.io/docs/tutorials/security/security_best_practices>

[^mcp-threat]: Charoes Huang, Xin Huang, Ngoc Phu Tran y Amin Milani Fard, “Model Context Protocol Threat Modeling and Analyzing Vulnerabilities to Prompt Injection with Tool Poisoning”, arXiv:2603.22489, 2026. Aplica STRIDE/DREAD a MCP y destaca tool poisoning como vulnerabilidad crítica del lado cliente. <https://arxiv.org/abs/2603.22489>

---
