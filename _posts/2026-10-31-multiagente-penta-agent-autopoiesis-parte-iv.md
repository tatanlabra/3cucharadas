---
layout: single
classes:
  - post-editorial-hero-v2
  - post3-evidence
title: "Multiagentes en 3 cucharadas (parte IV): del tridente en consola a un circuito de autopoiesis"
subtitle: "Gobernanza de agentes, memoria híbrida en 70 milisegundos y un laboratorio que ensaya sus propias mejoras sin gastar cuota"
description: "Cuarta entrega de la serie multiagente en penta-agent: ruteo gobernado por cuota, memoria híbrida en 70 ms, herramientas MCP y un circuito de autopoiesis local en Harness2."
excerpt: "En la parte III armé un tridente de agentes en la terminal; meses después descubrí que coordinar llamadas no basta si el sistema olvida, gasta cuota a ciegas o se rompe en silencio. Aquí cuento cómo pasé a una arquitectura de autopoiesis gobernada y por qué un modelo de lenguaje suelto jamás podría lograrlo por sí solo."
date: 2026-10-31 12:00:00 -0300
last_modified_at: 2026-10-31 15:20:00 -0300
author: clabra
author_profile: true
comments: true
published: true
math: false
lang: es
ref: multiagente-penta-agent-autopoiesis-parte-iv
permalink: /ia/productividad/desarrollo/multiagente-penta-agent-autopoiesis-parte-iv/
categories: [ia, productividad, desarrollo, multiagente]
tags: [ia, agentes, cli, automatizacion, linux, arquitectura, memoria, autopoiesis]
distribution:
  social: true
  republish: []
repo: https://github.com/tatanlabra/penta-agent
entorno: "Arch Linux, KDE Plasma, kitty + tmux + Starship, servicios locales (Qdrant + FTS5 + Qwen3-Embedding-0.6B) y laboratorio determinista Harness2"
en_abstract: >
  Fourth entry in the penta-agent multi-agent series. Having three CLI agents
  talking in the terminal does not produce a system that learns: without
  governed memory, quota-aware routing, and falsifiable verification gates, each
  new session repeats past failures or burns quota blindly. Drawing on systems
  theory and autopoiesis (Maturana and Varela 1987; Luhmann 1995, 1998;
  Spencer-Brown 1969; Esposito 2017, 2024; Zönnchen, Dzhimova, and Socher 2025),
  this post shows why a standalone large language model lacks genuine re-entry
  and internal resistance, and how an engineered socio-technical harness supplies
  both across three layers: quota-governed agent routing with a live plan-board
  in kitty and tmux; a 70 ms hybrid memory coupling SQLite FTS5 with Qdrant
  dense vectors alongside modular skills and MCP servers; and a zero-token
  autopoiesis loop in Harness2 that converts real friction signals into holdout
  cases and rejects regressive candidates before human promotion.
toc: true
toc_sticky: true
visual_id: multiagente-penta-agent-autopoiesis-parte-iv
visual_ref: multiagente-penta-agent-autopoiesis-parte-iv
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
header:
  overlay_image: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/teaser-1280x720.webp
  teaser_mobile: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/teaser-mobile-640x360.webp
  og_image: /assets/images/heroes-v2/multiagente-penta-agent-autopoiesis-parte-iv/og-1200x630.webp
  og_image_alt: "Esfera de red con tres nodos agentes dentro de un anillo orbital Harness2 que filtra un pulso regresivo ante un umbral de resistencia interna y realimenta la estructura con el flujo verificado."
---

Después de medir los modelos en la [parte I]({{ '/ia/productividad/desarrollo/multiagente-penta-agent-modelos/' | relative_url }}), auditar la recuperación en la [parte II]({{ '/ia/productividad/desarrollo/multiagente-penta-agent-memoria/' | relative_url }}) y trazar la procedencia en la [parte III de esta serie]({{ '/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/' | relative_url }}), cerré el computador con una sensación de victoria: tenía un tridente de agentes funcionando desde la terminal en Arch Linux. Con un par de alias en `zsh`, podía invocar a [Claude Code](https://github.com/anthropics/claude-code) para razonar sobre arquitectura, pasarle un encargo a [Codex CLI](https://github.com/openai/codex) para editar código o pedirle una segunda opinión rápida a [Gemini CLI](https://github.com/google-gemini/gemini-cli) y Antigravity. Sobre el papel, la orquestación parecía resuelta.
{: .text-justify}

Sin embargo, después de usar ese esquema todos los días en proyectos reales dentro de [`penta-agent`](https://github.com/tatanlabra/penta-agent), choqué contra una pared silenciosa: **tener tres agentes conversando no equivale a tener un sistema que aprende**. Cada vez que abría una sesión nueva, el tridente sufría de amnesia parcial, repetía comandos que ya habían fallado la semana anterior, agotaba la cuota del proveedor más caro en tareas rutinarias o daba por "verificadas" pruebas que jamás habían tenido la posibilidad de fallar.
{: .text-justify}

Para entender qué me faltaba, me sirvió cambiar la pregunta. En un análisis reciente sobre inteligencia artificial desde la teoría de sistemas, Benedikt Zönnchen, Mariya Dzhimova y Gudrun Socher ([2025, 2–4](https://doi.org/10.3389/fcomm.2025.1585321)) proponen dejar de preguntarse si un modelo de lenguaje "piensa como un humano" y formular, en cambio, la pregunta de Humberto Maturana y Francisco Varela ([1987 [1984]](https://search.worldcat.org/title/12314331)) retomada por Niklas Luhmann ([1998, 60–69](https://search.worldcat.org/title/37906965)): **¿puede el sistema trazar su propia frontera con el entorno, observar sus propios fallos y sostenerse mediante sus propias operaciones?** Es decir, pasar de la noción difusa de "inteligencia" al mecanismo concreto de la **autopoiesis**.
{: .text-justify}

Como demuestran Zönnchen, Dzhimova y Socher ([2025, 8–10](https://doi.org/10.3389/fcomm.2025.1585321)), un modelo de lenguaje aislado en una ventana de chat **no es ni puede ser un sistema autopoiético productor de sentido (*sense-making*)**: carece de lo que George Spencer-Brown ([1969](https://archive.org/details/lawsofform00spen)) llamó *re-entry* —la capacidad de reintroducir la distinción entre el sistema y su entorno (autorreferencia vs. heterorreferencia) dentro de sus propias operaciones— porque solo calcula qué palabra es estadísticamente plausible después de otra, sin resistencia interna frente al error. Si quiero un sistema que mejore sin degradarse, tengo que construir alrededor de los modelos un **arnés socio-técnico** que acople la flexibilidad probabilística de las redes neuronales con el acoplamiento estricto y el código binario (`funciona / no funciona`, `work / fail`) de la tecnología determinista descrito por Luhmann ([1998, 517–525](https://search.worldcat.org/title/37906965)) y André Reichel ([2011, 105–118](https://doi.org/10.1504/IJISD.2011.043070)).
{: .text-justify}

### El punto de partida: lo que medí y descarté antes de dar este salto

Antes de entrar en las tres cucharadas de esta cuarta entrega, resumo el experimento que me obligó a adoptar esa disciplina. Cuando intenté dotar de memoria a largo plazo al sistema, la tentación obvia era instalar la arquitectura más sofisticada del momento: grafos temporales, extractores pesados o un juez neuronal de `8B` parámetros corriendo en CPU. En vez de dejarme llevar por la intuición, armé un benchmark reproducible sobre mis bitácoras reales —comparando alternativas abiertas como [GraphRAG](https://github.com/microsoft/graphrag), [Graphiti](https://github.com/getzep/graphiti), [Hindsight](https://github.com/vectorize-io/hindsight), [Letta](https://github.com/letta-ai/letta), [Mem0](https://github.com/mem0ai/mem0) y [deja-vu](https://github.com/vshulcz/deja-vu)— y fijé un contrato de falsación previo: cualquier candidato que superara los `0,10 s` de latencia `p95` o no mejorara al menos un `10 %` la recuperación quedaba descartado.
{: .text-justify}

| Qué puse a prueba en el laboratorio | Resultado medido | Decisión operativa |
|---|---|---|
| **Memoria híbrida (`v3.1`)** (índice léxico `FTS5` + vecinos semánticos en [Qdrant](https://github.com/qdrant/qdrant) con [`Qwen3-Embedding-0.6B`](https://github.com/QwenLM/Qwen3-Embedding)) | Latencia `p95 = 0,07 s` (`< 0,10 s`), `96 %` de acierto global y rescate de `1 de cada 3` consultas sin palabras exactas | **Promovida a producción** como motor de `experience-memory` y `recall-context` |
| **Grafo relacional en memoria (`v3.2`)** para expandir saltos entre entidades | Empate exacto en precisión con `v3.1`, pero casi el doble de latencia (`p95 = 0,13 s > 0,10 s`) | **Congelado en laboratorio**; la complejidad extra no pagó su costo |
| **Jueces neuronales (`4B` y `8B`) en CPU** para auditar respuestas en vivo | Entre `69 s` y `197 s` por veredicto, con timeouts de `180 s` en `2` de `3` corridas | **Descartados para el camino crítico**; poda de `36,3 GiB` en disco |
| **Chequeos deterministas + juez `0.6B` acotado** para validación local | Latencia de milisegundos, `0` llamadas remotas y `100 %` de reproducibilidad | **Adoptado como estándar** de puertas de control y evaluación |

**Tabla 1.** Síntesis del laboratorio previo de memoria y evaluación local en [`penta-agent`](https://github.com/tatanlabra/penta-agent): qué sobrevivió al umbral de `0,10 s` y por qué limpié `36,3 GiB` de modelos locales que no aportaban valor operativo.
{: .text-justify}

Con ese piso firme, organicé esta cuarta parte en tres cucharadas progresivas: en la **primera** muestro cómo pasé de lanzar agentes sueltos en consola a gobernarlos con presupuesto de cuota, puentes auditables y un tablero en vivo en [`kitty`](https://github.com/kovidgoyal/kitty) y [`tmux`](https://github.com/tmux/tmux); en la **segunda**, cómo funciona por dentro el sistema nervioso de memoria híbrida, herramientas [MCP](https://github.com/modelcontextprotocol/servers) y [skills](https://github.com/anthropics/skills); y en la **tercera**, cómo cerré el circuito de autopoiesis local con `Harness2` y dónde trazan hoy la frontera tanto mis métricas como la teoría de sistemas.
{: .text-justify}

---

## Cucharada 1: De invocar agentes a mano a gobernar agentes y modelos

Explicado en sencillo: cuando empecé a integrar los tres agentes yo actuaba como un director de tránsito que agitaba los brazos en medio de la esquina. Si quería que [Codex CLI](https://github.com/openai/codex) revisara un parche hecho por [Claude Code](https://github.com/anthropics/claude-code), copiaba rutas, abría otra pestaña y confiaba en que todo saliera bien. Eso sirve para hacer una demostración de cinco minutos, pero fracasa cuando una tarea dura dos horas y toca veinte archivos.
{: .text-justify}

### Ruteo con conciencia de cuota y fronteras de seguridad

Mi primera inferencia **deductiva** nació de una restricción dura: las suscripciones y APIs de modelos tienen límites de uso, ventanas de contexto distintas y fronteras de credenciales que no deben mezclarse. Por definición, si delego una tarea pesada a un agente cuya cuota está al `98 %`, la sesión va a morir a mitad de camino dejando el repositorio en un estado inconsistente.
{: .text-justify}

Por eso reemplacé la elección intuitiva de proveedor por una política explícita en `routing.yaml` y un centinela previo (`quota_status.sh`, gobernado por la skill `quota-guard`). Antes de lanzar cualquier encargo costoso, el sistema lee desde caché la presión real de cada carril sin gastar tokens:
{: .text-justify}

- **🔍 [Claude Code](https://github.com/anthropics/claude-code) (`Opus` / `Sonnet`):** asume el diseño arquitectónico, la edición delicada y la síntesis de largo aliento cuando su cuota está despejada (`exit 0`).
- **🛠️ [Codex CLI](https://github.com/openai/codex) (`gpt-5.4`):** entra como par de implementación, refactorización profunda, rescate de sesiones (`codex-rescue`) y verificación cruzada.
- **🌐 [Gemini CLI](https://github.com/google-gemini/gemini-cli) y Antigravity (`gemini-3-pro` / `flash`):** en sesión directa (`penta-agy`) actúa como integrador principal; cuando otro agente lo invoca desde afuera mediante `agy-bridge`, corre en un sandbox estricto sobre contexto público saneado como explorador, revisor o validador, sin heredar jamás llaves privadas ni archivos `.env`.

En lugar de llamar al binario crudo y depender de lo que escupa por pantalla, toda delegación cruzada pasa por `agy-bridge`. El puente exige declarar quién llama (`--caller`), en qué modo (`plan`, `review`, `patch`, `test` o `explain`) y con qué límite de tiempo (`--timeout`), dejando un recibo inmutable en `.agents/runs/<run_id>/` con `request.md`, `result.md`, `status.json` y `diff.patch`.
{: .text-justify}

### El tablero en vivo (`plan-board`) y las compuertas de decisión

Mi segunda inferencia fue **inductiva**: al revisar decenas de sesiones pasadas, noté que el mayor desperdicio de tiempo ocurría en dos extremos. O bien un agente me interrumpía cada dos minutos para pedirme permiso por pasos triviales y reversibles, o bien tomaba en silencio una decisión arquitectónica delicada y recién al final yo descubría que había ido por el camino equivocado.
{: .text-justify}

Para eliminar ambos extremos sin llenar este post de diagramas abstractos, prefiero mostrar directamente cómo luce hoy mi consola [`kitty`](https://github.com/kovidgoyal/kitty) —o alternativas minimalistas de Wayland como [`foot` en Codeberg](https://codeberg.org/dnkl/foot)— dividida en dos paneles con [`tmux`](https://github.com/tmux/tmux) mientras corre una tarea real:
{: .text-justify}

<figure class="align-center" style="width: 100%;">
  <video width="1280" height="800" style="width: 100%; height: auto; border-radius: 12px; display: block; cursor: pointer;" autoplay loop muted playsinline preload="metadata" onclick="this.paused ? this.play() : this.pause()" title="Haz clic o toca para pausar o reanudar la terminal" poster="{{ '/assets/images/multiagente-penta-agent-autopoiesis/kitty-tmux-plan-board-poster-1280x800.webp' | relative_url }}" aria-label="Demostración en consola Kitty dividida con tmux donde el panel superior ejecuta la delegación multiagente, pasa por un decision-gate y valida un gate falsable, mientras el panel inferior actualiza el plan-board en vivo hasta cerrar 4 de 4 pasos.">
    <source src="{{ '/assets/videos/kitty-tmux-plan-board-1280x800.webm' | relative_url }}" type="video/webm">
    Tu navegador no admite video WebM. Puedes <a href="{{ '/assets/videos/kitty-tmux-plan-board-1280x800.webm' | relative_url }}">abrir la demostración directamente</a>.
  </video>
  <figcaption><strong>Figura 1.</strong> Flujo diario en mi terminal <a href="https://github.com/kovidgoyal/kitty"><code>kitty</code></a> + <a href="https://github.com/tmux/tmux"><code>tmux</code></a> con prompt <a href="https://github.com/starship/starship"><code>Starship</code></a>: arriba corre la ejecución multiagente con <code>agy-bridge</code>, el freno de <code>decision-gate</code> y <code>pytest</code>; abajo, el monitor de <code>plan-board</code> (<code>watch.mjs</code>) actualiza en vivo el estado de cada paso (<code>[ ]</code> &rarr; <code>[~]</code> &rarr; <code>[!]</code> &rarr; <code>[x]</code>), las decisiones y la deriva.</figcaption>
</figure>

Lo que se ve en el panel inferior de la **Figura 1** es el contrato que cambió mi forma de trabajar:
{: .text-justify}

1. **Autonomía local con trazabilidad visual (`plan-board`):** todo paso reversible y dentro del alcance avanza sin pedirme permiso, pero debe reflejarse en tiempo real en la tabla inferior. Y ningún ítem puede cerrarse como verificado (`[x]`) si el agente no adjunta la referencia concreta de la prueba, comando u observación que lo respalda.
2. **Compuerta de decisión (`decision-gate`):** cuando aparece una bifurcación irreversible o de diseño (estado `[!]`), el agente detiene solo esa rama y me presenta la consulta con la **opción recomendada en primer lugar**, marcada como `(Recomendado)` y justificada con evidencia deductiva, inductiva y abductiva.
3. **Un gate que nunca se ha visto rojo no es un gate (`gates-falsables`):** antes de aceptar cualquier verificador nuevo, exijo correrlo contra un fallo sintético (`--fixture`) y comprobar que devuelve código de salida distinto de cero (`exit 1`). Si un test pasa siempre incluso cuando rompo el insumo a propósito, no es una red de seguridad: es teatro de cumplimiento.

---

## Cucharada 2: El sistema nervioso — memoria híbrida, skills y herramientas MCP

Si la primera cucharada ordena quién hace qué y bajo qué reglas, la segunda resuelve cómo recuerda el sistema lo que ya aprendió y cómo elige la herramienta exacta sin inflar la ventana de contexto.
{: .text-justify}

Aquí vuelve a ser clave el diagnóstico de Zönnchen, Dzhimova y Socher ([2025, 6–7, 9](https://doi.org/10.3389/fcomm.2025.1585321)): una red neuronal mantiene con la comunicación humana un **acoplamiento laxo** (*loose coupling*) que funciona como un *"sistema de fichas o Zettelkasten contingente"* (*"contingent index-card system [Zettelkasten]"*, pp. 7, 9) de asociaciones semánticas en un espacio vectorial, generando lo que Elena Esposito ([2017, 249–265](https://doi.org/10.1515/zfsoz-2017-1014); [2022](https://doi.org/10.7551/mitpress/14189.001.0001)) denomina *"doble contingencia virtual"* y *"comunicación artificial"*. Esa flexibilidad le permite conectar ideas formuladas con palabras muy distintas, pero también hace que sus salidas sean inherentemente probabilísticas y carezcan de decisión propia. Si quiero memoria confiable y ejecución precisa, debo acoplar ese *Zettelkasten* vectorial con índices exactos y scripts deterministas.
{: .text-justify}

### Memoria de experiencias (`experience-memory`): el *Zettelkasten* híbrido en `0,07 s`

Cuando empecé a guardar bitácoras, mi memoria era, en el fondo, un conjunto de archivos Markdown que yo leía o buscaba con [`ripgrep`](https://github.com/BurntSushi/ripgrep). El problema evidente es que si hace un mes resolví un bloqueo de pantalla en frío bajo el título `"Fallo de webview en autostart"` y hoy busco `"Panel que no carga al iniciar sesión"`, una búsqueda puramente léxica puede pasar de largo, mientras que una búsqueda puramente vectorial puede enterrar el nombre exacto de un script como `verify_boot_contract.sh`.
{: .text-justify}

La solución que validé en la **Tabla 1** combina ambos mundos detrás del servidor [MCP](https://github.com/modelcontextprotocol/servers) `experience-memory` y la skill `recall-context`:
{: .text-justify}

- **Carril léxico exacto (`SQLite FTS5`):** atrapa al instante nombres de banderas, códigos de error, rutas e invariantes (`INV-005`).
- **Carril semántico denso ([Qdrant](https://github.com/qdrant/qdrant) + [`Qwen3-Embedding-0.6B`](https://github.com/QwenLM/Qwen3-Embedding)):** indexa las decisiones arquitectónicas, handoffs y lecciones operativas (`penta_context_v2`) para recuperar vecinos conceptuales aunque no compartan ni una sola palabra clave.

Antes de diseñar una estrategia no trivial, el agente consulta `recall_experience` en `70 milisegundos` (`p95 = 0,07 s`). Así descubre qué comando funcionó antes, qué hipótesis ya fue refutada y qué trampa del entorno debe esquivar (por ejemplo, saber que en mi shell `cp`, `mv` y `rm` tienen alias interactivos `-i` que cuelgan un proceso sin TTY si no se invocan con `command mv -f`).
{: .text-justify}

### Skills como procedimientos vivos y selección proactiva de MCP

Para no saturar el prompt inicial con miles de líneas de instrucciones, adopté el patrón modular de [Anthropic Skills](https://github.com/anthropics/skills) enriquecido con contratos locales. En [`penta-agent`](https://github.com/tatanlabra/penta-agent) cada skill es un paquete autocontenido con cuatro piezas: un contrato corto en `SKILL.md` que define en qué casos se activa y **en qué casos no debe usarse**; documentación profunda bajo demanda en `references/` (por ejemplo, el corpus editorial extraído con [Docling](https://github.com/docling-project/docling) o las reglas de diagramación con [D2](https://github.com/terrastruct/d2)); ejecutables deterministas en `scripts/` (como las tuberías tipadas en [Nushell](https://github.com/nushell/nushell), la automatización visual con [Playwright](https://github.com/microsoft/playwright) o la integración con forjas vía [`glab` en GitLab](https://gitlab.com/gitlab-org/cli)); y un rastro de telemetría.
{: .text-justify}

Del mismo modo, la flota de servidores [MCP](https://github.com/modelcontextprotocol/servers) (`plan-board`, `experience-memory`, `ideas-rag`, `paper-search`, `bibliography-apa`, `PLAYWRIGHT_LOCAL`) está catalogada en `specs/mcp-capabilities.json`. Cuando entra una tarea, el triaje evalúa qué capacidades aportan evidencia real y registra tanto los aciertos como las abstenciones justificadas. Y cuando detecté que dos servidores antiguos (el de cuota y el de infraestructura remota SSH) eran más rápidos, transparentes y fáciles de auditar como scripts directos (`quota_status.sh` y `remote_exec.sh`), los di de baja como MCP y los convertí en skills ligeras. Menos demonios residentes, menor superficie de fallo.
{: .text-justify}

---

## Cucharada 3: El circuito de autopoiesis (`Harness2`) — cómo el sistema ensaya sus propias mejoras

Aquí llego al corazón de esta cuarta parte. Tener buenos agentes (Cucharada 1) y buena memoria con skills (Cucharada 2) todavía deja abierta una pregunta crítica: **¿qué pasa cuando una ruta de delegación envejece, una skill empieza a inducir errores o un ajuste en la memoria empeora la precisión en casos borde?** Si dependo únicamente de darme cuenta a ojo semanas después, el sistema se degrada por deriva silenciosa.
{: .text-justify}

### Por qué un LLM suelto no tiene *re-entry* ni resistencia interna

En su estudio sobre autopoiesis e inteligencia artificial, Zönnchen, Dzhimova y Socher ([2025, 8–9](https://doi.org/10.3389/fcomm.2025.1585321)) explican con precisión quirúrgica por qué no basta pedirle a un modelo que "reflexione sobre sus propios errores" mediante *chain-of-thought* (`CoT`). Cuando un modelo genera pasos intermedios como *"¿Es correcto este paso?"*, solo exhibe una **autorreferencialidad procesal** rudimentaria (*processual self-referentiality*, p. 8) —produciendo la continuación lingüística más plausible dentro de su distribución estadística—, pero carece de **autorreferencialidad reflexiva** (*reflective self-reference*) y de un *re-entry* genuino ([Spencer-Brown 1969](https://archive.org/details/lawsofform00spen)). Si un modelo se toma a sí mismo como única referencia sin un contraste externo, cae rápidamente en recursión infinita o colapso; si depende por completo de que un humano reentrene sus pesos desde afuera (`RLHF` o *fine-tuning* diferido), sigue siendo un artefacto *alopoiético* determinado desde el exterior ([Zönnchen, Dzhimova y Socher 2025, 4, 8–9](https://doi.org/10.3389/fcomm.2025.1585321)).
{: .text-justify}

Para salir de esa trampa, Zönnchen, Dzhimova y Socher ([2025, 7](https://doi.org/10.3389/fcomm.2025.1585321)) rescatan una formulación decisiva de Niklas Luhmann (1995) sobre cómo el constructivismo operativo reubica la "resistencia de la realidad" de Kant dentro de un sistema:
{: .text-justify}

> "Creo que no deberíamos abandonar la idea de resistencia [de Kant], sino que deberíamos reubicarla dentro del sistema. Es el resultado de resolver un conflicto interno: el resultado de las operaciones del sistema resistiendo a las operaciones del mismo sistema" (Luhmann 1995, citado en [Zönnchen, Dzhimova y Socher 2025, 7](https://doi.org/10.3389/fcomm.2025.1585321); traducción propia del original en inglés: *"I think we should not abandon [Kant's] idea of resistance, but we should relocate it into the system. It is the result of resolving an internal conflict—the result of the system's operations resisting the operations of the same system"*).

Esa frase describe, pieza por pieza, lo que construí en [`penta-agent`](https://github.com/tatanlabra/penta-agent) al adaptar e integrar el circuito proactivo de [**`Harness²`**](https://github.com/google-research/harness2) propuesto por Ruiyao Xu, Yanfei Chen, Zhongying CuiZhu et al. ([2026](https://arxiv.org/abs/2610.14224)): hacer que **las operaciones de verificación determinista del propio sistema resistan y filtren las propuestas de cambio generadas a partir de sus propias operaciones**.
{: .text-justify}

<details markdown="1">
<summary><strong>En sencillo (ELI5): ¿qué es el Harness² original de Google y cómo lo adapté a mi computador?</strong></summary>

Imagina que tus agentes de inteligencia artificial son cocineros muy creativos, pero el recetario que usan (sus reglas, su memoria y sus herramientas) a veces tiene pasos confusos que hacen que se les queme el arroz. El [`Harness²` original de Google Research](https://github.com/google-research/harness2) ([Xu et al. 2026](https://arxiv.org/abs/2610.14224)) propone un bucle genial llamado *Proponer–Probar–Componer*: en vez de cambiarle el cerebro al cocinero, pone a varios ayudantes a reescribir el recetario, les pide que cocinen platos de prueba en la nube y se queda con la receta ganadora. El problema para mi día a día era doble: la versión de fábrica está pensada para gastar cientos de llamadas pagadas a modelos en la nube (`Vertex AI`) y, además, cuando usa agentes de consola les apaga el cinturón de seguridad (`--dangerously-bypass-approvals-and-sandbox`) con internet abierto.
{: .text-justify}

Para adaptarlo a [`penta-agent`](https://github.com/tatanlabra/penta-agent) sin pagar un peso extra ni abrir agujeros de seguridad, tomé su motor de búsqueda recursiva (`commit 1cfe254e`) y lo encerré en una "cocina de juguete" completamente desconectada de internet (`unshare -Urn`), con carpeta temporal desechable y sin acceso a mis llaves ni a las CLIs de modelos (`model_calls = 0`). En lugar de inventar exámenes teóricos en la nube, mi envoltorio (`penta-harness2` y `local-cycle`) alimenta esa cocina con los tropiezos reales que sufrieron mis agentes durante la semana (`CSI`), exige que cualquier cambio de receta primero repruebe el examen cuando está roto (rojo) y luego apruebe todos los casos históricos sin romper nada (verde), y al final sincroniza la receta ganadora en una bandeja de espera para mis tres agentes (`Claude`, `Codex` y `Gemini/Antigravity`) con un botón de deshacer en un paso (`rollback-local`) por si yo no doy el visto bueno.
{: .text-justify}

</details>

<figure class="d2-responsive" style="width: 100%;">
  <picture style="display: block; width: 100%;">
    <source media="(max-width: 640px)" srcset="{{ '/assets/images/multiagente-penta-agent-autopoiesis/circuito-autopoiesis-h2-mobile.svg' | relative_url }}" type="image/svg+xml">
    <img src="{{ '/assets/images/multiagente-penta-agent-autopoiesis/circuito-autopoiesis-h2.svg' | relative_url }}" width="1001" height="954" style="width: 100%; height: auto; display: block; border-radius: 12px;" alt="Diagrama del circuito cerrado de autopoiesis local en Penta Agent con Harness2: las señales de fricción CSI alimentan el generador de casos y el ciclo local en los dominios de ruteo, memoria y skills; un juez determinista evalúa contra casos holdout con cero llamadas a modelos, descartando regresiones y conservando solo las mejoras verificadas para promoción humana.">
  </picture>
  <figcaption><strong>Figura 2.</strong> Circuito de autopoiesis gobernada en <code>penta-agent</code> + <code>Harness2</code>: reubicación de la resistencia interna (Luhmann 1995; Zönnchen, Dzhimova y Socher 2025) mediante evaluación <code>holdout</code> con <code>model_calls = 0</code> antes de cualquier promoción humana.</figcaption>
</figure>

### Cómo funciona el lazo cerrado en mis tres dominios (`routing`, `memory`, `skills`)

Como muestra la **Figura 2** (que se adapta en tres columnas por etapa para escritorio y en flujo vertical para móvil), el circuito opera en cuatro etapas estrictas:
{: .text-justify}

1. **Observación de fricciones reales (`CSI` — *Continuous Self-Improvement*):** mientras uso el sistema, un recolector registra señales objetivas de fricción: una tarea que tuvo que cambiar de agente por timeout, una consulta a `experience-memory` que devolvió pocos vecinos útiles o una skill donde el usuario tuvo que corregir un comando.
2. **Puente de evidencia a casos reproducibles (`--from-csi latest`):** el módulo `local_cycle.py` toma ese informe de fricción y lo traduce automáticamente en una especificación de prueba (`CaseSpec`) dentro de un entorno aislado, sin tocar mi configuración activa.
3. **Resistencia interna sin gastar tokens (`eval_harness` con `model_calls = 0`):** el arnés ejecuta la suite completa (`--profile autopoiesis-all`, que hoy cubre `9/9` casos base repartidos en `routing`, `memory` y `skills`) exigiendo dos condiciones duras: que todos los casos de control (`holdout`) pasen en verde (`holdout_passed = true`) y que el costo en llamadas a APIs externas sea exactamente cero (`model_calls = 0`).
4. **Decisión auditable (`KEEP` vs. `DISCARD`) y promoción humana:** si un candidato empeora un solo caso de `holdout` o no supera a la línea base, el juez determinista lo descarta (`DISCARD`). Solo cuando mejora el puntaje sin regresiones recibe un veredicto `KEEP` y deja un recibo firmado para que yo decida si lo promuevo al repositorio principal.

Para que no quede como una promesa teórica, en el siguiente mini-video muestro la corrida de `penta-harness2-shadow local-cycle --profile autopoiesis-all` en mi terminal [`kitty`](https://github.com/kovidgoyal/kitty) con [`tmux`](https://github.com/tmux/tmux), incluyendo qué ocurre cuando inyecto un candidato regresivo (`--fixture`) frente al candidato sano:
{: .text-justify}

<figure class="align-center" style="width: 100%;">
  <video width="1280" height="800" style="width: 100%; height: auto; border-radius: 12px; display: block; cursor: pointer;" autoplay loop muted playsinline preload="metadata" onclick="this.paused ? this.play() : this.pause()" title="Haz clic o toca para pausar o reanudar la terminal" poster="{{ '/assets/images/multiagente-penta-agent-autopoiesis/kitty-harness2-autopoiesis-poster-1280x800.webp' | relative_url }}" aria-label="Demostración en consola Kitty dividida con tmux ejecutando penta-harness2-shadow local-cycle con 9 de 9 casos en routing, memory y skills sin llamadas a modelo, aplicando resistencia interna para descartar un regresor y conservar el candidato sano.">
    <source src="{{ '/assets/videos/kitty-harness2-autopoiesis-1280x800.webm' | relative_url }}" type="video/webm">
    Tu navegador no admite video WebM. Puedes <a href="{{ '/assets/videos/kitty-harness2-autopoiesis-1280x800.webm' | relative_url }}">abrir la demostración directamente</a>.
  </video>
  <figcaption><strong>Figura 3.</strong> Ejecución en consola <a href="https://github.com/kovidgoyal/kitty"><code>kitty</code></a> + <a href="https://github.com/tmux/tmux"><code>tmux</code></a> del circuito de autopoiesis local (<code>local-cycle --profile autopoiesis-all</code>): evalúa los <code>9/9</code> casos en <code>routing</code>, <code>memory</code> y <code>skills</code> con <code>model_calls = 0</code>, aplica resistencia interna para rechazar el regresor (<code>DISCARD</code>) y conserva la mejora verificada (<code>KEEP +0,250</code>) con las <code>82</code> pruebas del arnés en verde.</figcaption>
</figure>

---

## Cierre: qué logra hoy mi arquitectura y dónde están sus límites

Al mirar el camino recorrido desde la [parte I]({{ '/ia/productividad/desarrollo/multiagente-penta-agent-modelos/' | relative_url }}), la [parte II]({{ '/ia/productividad/desarrollo/multiagente-penta-agent-memoria/' | relative_url }}) y la [parte III]({{ '/ia/productividad/desarrollo/multiagente-memoria-gobernada-poc/' | relative_url }}), la diferencia principal ya no está en qué modelo responde más bonito en un prompt aislado, sino en la estructura que sostiene al conjunto cuando yo no estoy mirando cada línea.
{: .text-justify}

Siguiendo la distinción rigurosa de Zönnchen, Dzhimova y Socher ([2025, 5, 9–10](https://doi.org/10.3389/fcomm.2025.1585321)) y de Elena Esposito ([2017](https://doi.org/10.1515/zfsoz-2017-1014); [2022](https://doi.org/10.7551/mitpress/14189.001.0001); [2024](https://www.residenzverlag.com/buch/kommunikation-mit-unverstaendlichen-maschinen)), sería un error epistémico afirmar que un modelo de lenguaje o un conjunto de scripts ha alcanzado por sí solo la autopoiesis biológica de una célula viva ([Maturana y Varela 1987 [1984]](https://search.worldcat.org/title/12314331)) o la producción reflexiva de sentido (*Sinn*) de una conciencia humana ([Luhmann 1998, 50–69](https://search.worldcat.org/title/37906965)). Como advierten los propios Zönnchen, Dzhimova y Socher ([2025, 5, 10](https://doi.org/10.3389/fcomm.2025.1585321)) al criticar el uso meramente metafórico del término en la literatura tecnológica, los modelos siguen siendo motores estadísticos que computan distribuciones sin estados mentales propios. Ahora bien —y esta es mi síntesis de ingeniería para el sistema socio-técnico completo—, cuando acoplo su capacidad de variación contingente con una memoria híbrida verificada, contratos de delegación estrictos, un arnés de resistencia interna binaria (`work / fail`; [Reichel 2011](https://doi.org/10.1504/IJISD.2011.043070)) que filtra sus propias propuestas antes de tocar producción y la supervisión deliberativa humana, obtengo en la práctica un circuito de **autopoiesis operativa gobernada**.
{: .text-justify}

Para cerrar con total transparencia, resumo en la **Tabla 2** qué está funcionando y medido hoy en mi máquina, hacia dónde apunta el siguiente paso y bajo qué condición objetiva descartaría cada componente si dejara de cumplir su promesa:
{: .text-justify}

| Pilar del sistema | Qué logra hoy (verificado en producción) | Qué pretende lograr y condición de descarte |
|---|---|---|
| **1. Ruteo de agentes y modelos** (`routing.yaml`, `quota-guard`, `agy-bridge`) | Rutea tareas entre [Claude Code](https://github.com/anthropics/claude-code), [Codex CLI](https://github.com/openai/codex) y [Gemini CLI](https://github.com/google-gemini/gemini-cli) / Antigravity según presión de cuota en caché; aísla handoffs en `.agents/runs/` con sandbox estricto y muestra el avance en vivo en `plan-board` (**Figura 1**). | **Meta:** reponderar prioridades de ruteo a partir de tasas históricas de éxito por dominio.<br>**Descarte:** si el puente añade fallos espurios o latencia burocrática mayor al ahorro de cuota. |
| **2. Memoria híbrida** (`experience-memory`, [Qdrant](https://github.com/qdrant/qdrant) + `FTS5`) | Resuelve consultas léxicas y semánticas en `p95 = 0,07 s` (`< 0,10 s`), rescata `33 %` de pares sin palabras exactas y ahorra `36,3 GiB` tras podar jueces CPU lentos (**Tabla 1**). | **Meta:** incorporar decaimiento automático de lecciones obsoletas cuando cambia un contrato.<br>**Descarte:** si la latencia `p95` supera `0,10 s` o el ruido semántico degrada la precisión top-3. |
| **3. Gobernanza de skills y MCP** (`mcp-fleet`, `gates-falsables`) | Mantiene paridad declarativa entre agentes (`24/24` chequeos en verde), mide uso y abstención de MCP y exige que todo gate nuevo falle primero ante un canario rojo (`--fixture -> exit 1`). | **Meta:** poda semiautomática de skills que acumulen fricción reiterada en telemetría `CSI`.<br>**Descarte:** si mantener los contratos de una skill cuesta más tiempo que ejecutar el comando directo. |
| **4. Autopoiesis local (`Harness2`)** (`local-cycle`, `eval_harness`) | Convierte fricciones reales `CSI` en `Casos` reproducibles y evalúa candidatos en `routing`, `memory` y `skills` (`9/9` casos, `82/82` tests) con `model_calls = 0`, aplicando resistencia interna (`KEEP` / `DISCARD`, **Figuras 2 y 3**). | **Meta:** ampliar el banco de casos reales extraídos de sesiones fallidas sin perder evaluación en milisegundos.<br>**Límite duro (`INV-004`):** prohibido el *auto-merge* ciego; la promoción final a producción requiere siempre revisión humana. |

**Tabla 2.** Balance entre los resultados verificados hoy en [`penta-agent`](https://github.com/tatanlabra/penta-agent), el horizonte de diseño y los umbrales de falsación que mantienen el sistema bajo control humano.
{: .text-justify}

Si algo me dejó claro construir esta cuarta etapa es que la madurez de un sistema multiagente no se mide por cuántas cosas nuevas le agrego cada semana, sino por cuánta complejidad innecesaria soy capaz de podar y cuántos errores propios es capaz de atajar el sistema antes de pedirme ayuda.
{: .text-justify}

---

## Referencias

<div class="post-references" markdown="1">

- Esposito, Elena. 2017. ["Artificial Communication? The Production of Contingency by Algorithms"](https://doi.org/10.1515/zfsoz-2017-1014). *Zeitschrift für Soziologie* 46 (4): 249–265. <https://doi.org/10.1515/zfsoz-2017-1014>.
- Esposito, Elena. 2022. [*Artificial Communication: How Algorithms Produce Social Intelligence*](https://doi.org/10.7551/mitpress/14189.001.0001). Cambridge, MA: The MIT Press. <https://doi.org/10.7551/mitpress/14189.001.0001>.
- Esposito, Elena. 2024. [*Kommunikation mit unverständlichen Maschinen*](https://www.residenzverlag.com/buch/kommunikation-mit-unverstaendlichen-maschinen). Salzburgo y Viena: Residenz Verlag (reseña académica verificable en <https://doi.org/10.21240/merz/2024.4.20>).
- Luhmann, Niklas. 1995. "Systems Theory and Postmodernism". Conferencia universitaria, Londres. Citado en [Zönnchen, Dzhimova y Socher (2025, 7)](https://doi.org/10.3389/fcomm.2025.1585321) (<https://doi.org/10.3389/fcomm.2025.1585321>).
- Luhmann, Niklas. 1998. [*Die Gesellschaft der Gesellschaft*](https://search.worldcat.org/title/37906965). Fráncfort del Meno: Suhrkamp Verlag. <https://search.worldcat.org/title/37906965>.
- Maturana, Humberto R. y Francisco J. Varela. 1987 [1984]. [*El árbol del conocimiento: las bases biológicas del entendimiento humano*](https://search.worldcat.org/title/12314331). Santiago de Chile: Editorial Universitaria (1.ª ed. chilena 1984; ed. internacional de 1987 citada en [Zönnchen, Dzhimova y Socher 2025, 3](https://doi.org/10.3389/fcomm.2025.1585321)). <https://search.worldcat.org/title/12314331>.
- Reichel, André. 2011. ["Technology as System: Towards an Autopoietic Theory of Technology"](https://doi.org/10.1504/IJISD.2011.043070). *International Journal of Innovation and Sustainable Development* 5 (2–3): 105–118. <https://doi.org/10.1504/IJISD.2011.043070>.
- Spencer-Brown, George. 1969. [*Laws of Form*](https://archive.org/details/lawsofform00spen). Londres: Allen & Unwin. <https://archive.org/details/lawsofform00spen>.
- Xu, Ruiyao, Yanfei Chen, Zhongying CuiZhu, Bhavana Dalvi Mishra, Yifei Ming, Han Yu, Rujun Han, Chen-Yu Lee y Tomas Pfister. 2026. ["Harness²: Recursive Agent Harnessing for an Open World"](https://arxiv.org/abs/2610.14224). *arXiv preprint* `arXiv:2610.14224` (código abierto en <https://github.com/google-research/harness2>). <https://arxiv.org/abs/2610.14224>.
- Zönnchen, Benedikt, Mariya Dzhimova y Gudrun Socher. 2025. ["From Intelligence to Autopoiesis: Rethinking Artificial Intelligence through Systems Theory"](https://doi.org/10.3389/fcomm.2025.1585321). *Frontiers in Communication* 10:1585321. <https://doi.org/10.3389/fcomm.2025.1585321>.

</div>

<style>
.post3-evidence .page__content > p,
.post3-evidence .page__content > ul > li,
.post3-evidence .page__content > ol > li,
.post3-evidence .page__content blockquote p {
  text-align: justify;
  hyphens: auto;
}
@media (max-width: 47.99em) {
  .post3-evidence .tabla-desliza {
    overflow-x: visible;
  }
  .post3-evidence .tabla-desliza table,
  .post3-evidence .tabla-desliza[data-perfil="narrativa"] table {
    width: 100% !important;
    max-width: 100% !important;
    min-width: 0 !important;
    table-layout: fixed;
    font-size: 13.5px;
    line-height: 1.35;
  }
  .post3-evidence .tabla-desliza table :is(th, td) {
    padding: 0.42rem 0.32rem;
    overflow-wrap: anywhere;
    word-break: normal;
  }
  .post3-evidence .tabla-desliza table code {
    font-size: 0.85em;
    word-break: break-word;
  }
}
</style>
