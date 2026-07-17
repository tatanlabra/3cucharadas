---
layout: single
classes: [ai-quota-hud-post]
title: "AI quotas in three spoonfuls: a HUD for the KDE panel"
subtitle: "Claude, Codex, Gemini, and DeepSeek, before one of them declares itself out of service"
date: 2026-07-15 00:00:00 +0000
categories: [ai, productivity, development, kde]
tags: [kde, plasma, plasmoid, qml, python, systemd, mcp, claude-code, codex, gemini, deepseek, arch-linux, quota, rate-limit, local-first]
description: "A local KDE Plasma 6 widget that shows the available quota for Claude, Codex, Gemini, and DeepSeek. How it works and what happened when Codex changed its usage windows."
excerpt: "Four agents, four ways of measuring quota, and one widget to know which of them can still finish the job."
author: clabra
lang: en
ref: ai-quota-hud-kde
permalink: /ia/productividad/ai-quota-hud-kde/
distribution:
  social: true
  republish: [dev, medium]
toc: true
toc_sticky: true
comments: true
author_profile: true
header:
  teaser: /assets/images/teasers/teaser-ai-quota-hud.webp
  og_image: /assets/images/ai-quota-hud/popup-hidpi.png
  og_image_alt: "AI Quota HUD popup with four quota donuts"
---

I currently use Claude Code, Codex, Gemini (through `agy` on the command line), and DeepSeek on Arch Linux with KDE Plasma 6. For me, as for many others, the problem has become knowing which one still has quota—especially when a task already carries a lot of context, reviewed files, and an hour of iteration.
{: .text-justify}

That is how I ended up building a viewer, or HUD, for the KDE panel: four indicators showing how much room each agent has left and when its quota should reset. No extra tab, no separate dashboard, and—most importantly—no surprise when the quota runs out while I am wrapping up a task or a `git rebase` 😱.
{: .text-justify}

## First spoonful: the token-week

Each provider invented its own way of measuring how much we can use it.
{: .text-justify}

Claude speaks in windows of hours and days. Codex reports the windows available for the plan. Gemini requires a local estimate of requests. DeepSeek, by contrast, speaks in monetary balance.
{: .text-justify}

Four agents, four clocks, and no shared unit.
{: .text-justify}

The industry has achieved something rather peculiar: turning **token-hours** and **token-weeks** into real planning units. It is no longer enough to ask how long a task will take. I also have to calculate whether the agent can finish it before leaving me to do things the old-fashioned way :).
{: .text-justify}

On the panel I reduced it to four rings, or donuts. A nearly full one means the agent still has room. A nearly empty one means it is probably time to thank it for its service and try the next one.
{: .text-justify}

{% include figure class="ai-quota-hud__donuts" popup=true image_path="/assets/images/ai-quota-hud/bar.png" alt="Compact AI Quota HUD bar on the KDE Plasma panel, with four circular indicators." caption="**Figure 1** — Compact AI Quota HUD view on the KDE Plasma panel. The four rings summarize the available margin by agent. Source: own screenshot with demonstration data." %}

Hovering over it shows the details of each window and its reset time:
{: .text-justify}

{% include figure popup=true image_path="/assets/images/ai-quota-hud/tooltip.png" alt="AI Quota HUD tooltip with quota and reset information by agent." caption="**Figure 2** — The tooltip shows windows and reset times without leaving the active task. Source: own screenshot with demonstration data." %}

Opening the widget shows the complete detail for all four agents:
{: .text-justify}

<figure class="ai-quota-hud__video">
  <video autoplay loop muted playsinline controls preload="metadata" poster="/assets/images/ai-quota-hud/popup-hidpi.png" aria-label="AI Quota HUD demonstration: KDE panel, tooltip, and popup with four quota indicators.">
    <source src="/assets/videos/ai-quota-hud-kde.webm" type="video/webm">
    Your browser does not support WebM video. You can <a href="/assets/videos/ai-quota-hud-kde.webm">open the demonstration directly</a>.
  </video>
  <figcaption><strong>Figure 3</strong> — AI Quota HUD demonstration from the KDE panel to the detailed view. Panel, tooltip, and popup read one local source; the values shown are demonstration data and do not represent personal quotas. Source: own screen recording.</figcaption>
</figure>

## Second spoonful: the data decides, not the order

The first version worked well for weeks. Codex returned two windows: a short five-hour one and a weekly one.
{: .text-justify}

My code interpreted them by position:
{: .text-justify}

1. The first window, or outer ring, was the five-hour one.
2. The second was the weekly one.

It was simple—until Codex changed the schema.
{: .text-justify}

One day the widget showed 5% available in the supposed “5h” window, but with a reset scheduled six days later. Even for a technology company, five hours lasting almost a week seemed like too much innovation.
{: .text-justify}

The raw response contained a single window:
{: .text-justify}

```text
604800 seconds
```

That is seven days.
{: .text-justify}

Codex had stopped reporting the short window, but my code still called whatever appeared first “5h.” At the same time, the old weekly window remained frozen in the cache because the “keep the last good value” logic could not distinguish between a failed query and a window that had ceased to exist. 👻
{: .text-justify}

The correction had two parts.
{: .text-justify}

First, each window stopped being identified by its position and began to be identified by its actual duration. A short duration is a session; an extended duration is a weekly window or equivalent.
{: .text-justify}

Second, the monitor now distinguishes between:
{: .text-justify}

- **a query that failed**, in which case it temporarily preserves the previous value and marks it as cached;
- **a valid query that no longer contains a window**, in which case it removes that window from the current state.

The interface also stopped assuming that every agent has the same structure. If two windows arrive, it draws a double donut. If one arrives, it draws a single ring. The data defines the interface, not the other way around.
{: .text-justify}

The lesson is small but fairly general: **if the provider supplies the duration, that is the identity of the data; its position in an array is only a temporary coincidence.**
{: .text-justify}

## Third spoonful: local, useful, and not very universal

This project is not meant to be a cross-platform application.
{: .text-justify}

I built it for an environment very much like mine:
{: .text-justify}

- Arch Linux;
- KDE Plasma 6;
- `systemd --user`;
- Python;
- Bash;
- QML;
- the local sessions and credentials of the tools I already use.

It can probably be adapted to other distributions running Plasma 6. I do not promise that it will work unchanged on GNOME, Plasma 5, Windows, or macOS. Nor did I abstract every possible authentication method. It is a tool for my own desktop that I decided to organize and publish, not an attempt to solve every possible combination of operating systems, providers, and plans.
{: .text-justify}

Inside, the path is short:
{: .text-justify}

```text
                 systemd --user timer
                          │
                     every five minutes
                          ▼
 helpers/*.sh ──► Python monitor ──► status.json
                                           │
                            ┌──────────────┴──────────────┐
                            ▼                             ▼
                    QML widget                      MCP server
              panel · tooltip · popup       checks before delegation
```

The *helpers* are the only component that touches credentials. They return sanitized JSON, without authentication tokens or conversation content.
{: .text-justify}

The Python monitor queries, validates, and merges the information. If it encounters a `timeout`, an expired credential, or a `429` error, it preserves the last known value and marks it as cached.
{: .text-justify}

The `systemd` timer runs the update every five minutes. The widget does not query providers directly; it only reads a local file with `0600` permissions. That way I avoid triggering a *rate limit* by checking the *rate limit* too often, which would be an especially elegant way of closing the loop. 🫠
{: .text-justify}

The same `status.json` can be read by an MCP server. This lets an agent ask which provider still has quota before delegating a task. The desktop bar and the orchestrator receive exactly the same state.
{: .text-justify}

## Closing

The repository is published under the MIT license. It is designed for KDE Plasma 6, does not require `sudo`, and installs into the user's local paths:
{: .text-justify}

```bash
git clone https://github.com/tatanlabra/ai-quota-kde.git
cd ai-quota-kde
scripts/install-user.sh
ai-quota-monitor doctor
```

[View the repository on GitHub](https://github.com/tatanlabra/ai-quota-kde){: .btn .btn--primary}

It does not create more quota, negotiate better plans, or eliminate the token-week. It only prevents me from discovering halfway through a task that the chosen agent has gone off in search of additional quota 🤑.
{: .text-justify}

It is a small spoonful of sovereignty over my own workflow: knowing how much remains, when it resets, and who should get the next handoff.
{: .text-justify}

{% include figure popup=true image_path="/assets/images/ai-quota-hud/xkcd-303-compiling.png" alt="xkcd 303, Compiling: two programmers play while waiting for compilation to finish." caption="**Figure 4** — *Compiling*, [xkcd no. 303](https://xkcd.com/303/), by Randall Munroe. The old excuse was that the code was compiling; now I can say the quota resets next week. Licensed under [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)." %}
