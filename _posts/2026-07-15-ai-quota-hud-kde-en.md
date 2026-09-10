---
layout: single
classes: [ai-quota-hud-post]
title: "AI quotas in three spoonfuls: a HUD for the KDE panel"
subtitle: "Claude, Codex, Gemini, and DeepSeek, before one of them declares itself out of service"
date: 2026-07-15 00:00:00 +0000
categories: [ai, productivity, development, kde]
tags: [kde, plasma, plasmoid, qml, python, systemd, mcp, claude-code, codex, gemini, deepseek, arch-linux, quota, rate-limit, local-first]
description: "A local KDE Plasma 6 widget that shows the available quota for Claude, Codex, Gemini, and DeepSeek. How it works and what happened when Codex changed its usage windows."
excerpt: "Five agents, five ways of measuring quota, and one widget to know which of them can still finish the job."
author: clabra
lang: en
ref: ai-quota-hud-kde
permalink: /ia/productividad/ai-quota-hud-kde/
distribution:
  social: true
  republish: [dev, medium]
sindicar: true
valor_seo: bajo
devto_tags: [ai, claude, deepseek, kde]
devto_video_url: https://youtu.be/OuRMIQEURes
toc: true
toc_sticky: true
comments: true
author_profile: true
header:
  teaser: /assets/images/teasers/teaser-ai-quota-hud.webp
  og_image: /assets/images/ai-quota-hud/popup-og-en-1200x938.webp
  og_image_alt: "AI Quota HUD detailed view with five quota donuts"
---

I currently use Claude Code, Codex, Gemini (through `agy` on the command line), and DeepSeek on Arch Linux with KDE Plasma 6. For me, as for many others, the problem has become knowing which one still has quota—especially when a task already carries a lot of context, reviewed files, and an hour of iteration.
{: .text-justify}

That is how I ended up building a viewer, or HUD, for the KDE panel: five indicators showing how much room each agent has left and when its quota should reset. No extra tab, no separate dashboard, and—most importantly—no surprise when the quota runs out while I am wrapping up a task or a `git rebase` 😱.
{: .text-justify}

## First spoonful: the token-week

Each provider invented its own way of measuring how much we can use it.
{: .text-justify}

Claude speaks in windows of hours and days. Codex reports the windows available for the plan. Gemini requires a local estimate of requests. Copilot counts premium requests against a calendar cutoff. DeepSeek, by contrast, speaks in monetary balance.
{: .text-justify}

Five agents, five clocks, and no shared unit.
{: .text-justify}

The industry has achieved something rather peculiar: turning **token-hours** and **token-weeks** into real planning units. It is no longer enough to ask how long a task will take. I also have to calculate whether the agent can finish it before leaving me to do things the old-fashioned way :).
{: .text-justify}

On the panel I reduced it to five rings, or donuts. A nearly full one means the agent still has room. A nearly empty one means it is probably time to thank it for its service and try the next one.
{: .text-justify}

{% include figure class="ai-quota-hud__donuts" popup=true image_path="/assets/images/ai-quota-hud/bar.png" alt="Compact AI Quota HUD bar on the KDE Plasma panel, with five circular indicators." caption="**Figure 1** — Compact AI Quota HUD view on the KDE Plasma panel. The five rings summarize the available margin by agent. The coloured arc is what remains free, and the outer white marks count the days until reset. Source: own screenshot with synthetic data." %}

Hovering over one donut shows that agent in detail: its windows and their reset times.
{: .text-justify}

{% include figure popup=true image_path="/assets/images/ai-quota-hud/tooltip-en-1260x930.png" alt="AI Quota HUD hover panel showing the four Antigravity and Gemini quota windows, each with its free percentage and reset time." caption="**Figure 2** — The hover panel shows the windows of the agent under the cursor without leaving the active task. Antigravity carries two independent weekly quotas on separate clocks: one for Google models and one for third-party ones. The badge says where each figure comes from: OFFICIAL if the provider reports it, LOCAL if it is a local count. Source: own screenshot with synthetic data." %}

Clicking opens the detailed view, with the five agents on top and the windows of whichever one is selected below.
{: .text-justify}

{% include figure popup=true image_path="/assets/images/ai-quota-hud/popup-en-1920x1500.png" alt="AI Quota HUD detailed view: a row of five selectors with each agent's free percentage and, below, Claude's four windows with percentage, provenance and reset time." caption="**Figure 3** — The detailed view. On top, the five agents with their tightest margin; below, the windows of whichever one is selected. Each line says how much is left, when it renews, and where the figure comes from. Source: own screenshot with synthetic data." %}

<figure class="ai-quota-hud__video">
  <video autoplay loop muted playsinline controls preload="metadata" poster="/assets/images/ai-quota-hud/popup-en-1920x1500.png" aria-label="AI Quota HUD demonstration: KDE panel, hover panel, and detailed view.">
    <source src="/assets/videos/ai-quota-hud-kde.webm" type="video/webm">
    Your browser does not support WebM video. You can <a href="/assets/videos/ai-quota-hud-kde.webm">open the demonstration directly</a>.
  </video>
  <figcaption><strong>Figure 4</strong> — The walkthrough from the KDE panel to the detailed view. The recording is from July and shows the earlier design, with four agents and no selector row; figures 1 to 3 show the current state. The values are synthetic and do not represent personal quotas. Source: own screen recording.</figcaption>
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

## Update, 8 September 2026

The HUD changed enough that the July screenshots no longer represented it.
Figures 1 to 3 above show the current state; the recording in figure 4 is still
from July and is kept because the walkthrough —panel, hover panel, detailed
view— has not changed, even though the design has.
{: .text-justify}

What is different:
{: .text-justify}

- **Five agents instead of four.** Copilot was added; it counts premium requests against a calendar cutoff. The post said "four" in seven places and has been corrected.
- **A different hover panel.** It used to squeeze all five agents into one cramped list. It now shows the detail of the agent under the cursor, with a badge per line saying whether the figure is reported by the provider (`OFFICIAL`) or counted locally (`LOCAL`).
- **A different click view.** The five agents moved into a row of selectors showing their tightest margin, with the windows of the selected one below. Previously it was five simultaneous columns that did not fit.
- **Slightly thicker strokes and larger logos.** The quota arc went from 0.055 to 0.060 of the diameter and the logos grew by 3 %, measured at runtime. The central aperture was recovered by tightening the gap between rings, because widening the stroke was shrinking it.
- **The interface is translated.** Source strings moved to English and Spanish lives in a `gettext` catalogue, so the widget speaks the language of the desktop.

And two things that surfaced precisely while preparing these screenshots, which
matter more than the screenshots themselves:
{: .text-justify}

- Dates rendered in English on a Spanish desktop. `Qt.formatDate` with a hand-written format uses the C locale, not the system one: with everything else already translated, it still said "Sat 12 Sep" where "sáb 12 sept" belonged. Measured with `QLocale("es_CL")` on the same date.
- Four labels were written in Spanish by the collector and reached the screen without passing through the catalogue, so on an English desktop they read in Spanish among translated strings.

The screenshots are generated by a script in the repository, not by hand, and
that is where the three new figures come from:
{: .text-justify}

```bash
scripts/capture_previews.sh build/previews en 3
```

It renders the three views without opening a window, with the same component the
tests verify, at whatever scale is asked for —3× for these. The data comes from
`ai-quota-monitor sample`, which writes a synthetic report into a temporary
directory: the real cache is neither read nor touched, and every line of the
render is labelled as synthetic. That is why the figures do not show my quotas,
and why they can be regenerated identically. It does need a GPU, though, and the
update below explains why.
{: .text-justify}

## Update, 9 September 2026

Figures 1 to 3 were regenerated for a specific reason: **the logos came out
black**. The widget on the panel was always fine; what was wrong was the
screenshot script.
{: .text-justify}

The Kirigami component that recolours a monochrome SVG does it with a GPU
material, and the software renderer has no equivalent for that material: it draws
the silhouette and skips the colour. The script rendered in software, so four of
the five logos showed up black —Codex, white— and in the popup they were nearly
invisible, dark on dark. The fifth, Gemini, looked right because it was never
meant to be tinted: it keeps the blue of its own file.
{: .text-justify}

What interests me most about this failure is why all 93 tests stayed green. A black
silhouette has exactly the same width, the same height and the same aperture as a
tinted one, so no geometric invariant could see it: the absence of a colour check
*was* the reason it went unnoticed. And it had been written down in the repository
since 6 September —«software rendering alone did not show SVG mask colours
faithfully»— two days before a commit switched the flow to offscreen and shipped the
defect.
{: .text-justify}

Measured: the bar had 1452 opaque pixels of pure black and 299 of pure white; the
popup, 2597 and 6. It now has zero of each, and the four masked logos appear in their
accent colour. There is a new test that looks at the pixel colour inside the central
disc of every donut and requires the dominant colour to be that provider's accent,
with Gemini as the negative control: if Gemini matched both, the measurement would be
looking at the ring rather than the logo. It skips explicitly when the machine has no
GPU, and it never passes by measuring nothing.
{: .text-justify}

A twist I did not expect: of the three ways to render on the GPU, the two obvious ones
require mapping a window, and **a locked screen stops presenting it**. The same
commands that worked in the afternoon hung an hour later with the session locked,
waiting for a frame nobody was going to paint. The one that works opens no window at
all. And switching platforms brought another surprise: the new one derived the DPI
from the real monitor instead of using 96, and with that the tooltip grew 24 pixels
without a single line of code changing. The DPI is now pinned, so the geometry does not
depend on the monitor of whichever machine takes the screenshot.
{: .text-justify}

The logos also grew by 5.3 %, which is all the margin left: the corner of their box now
touches the circumference of the central hole. The check that guaranteed that
containment had been disabled by a silent ceiling that clamped any value above 1
without warning —a value of 1.10 came out green—; removing it put the check back in
service.
{: .text-justify}

{% include figure popup=true image_path="/assets/images/ai-quota-hud/xkcd-303-compiling.png" alt="xkcd 303, Compiling: two programmers play while waiting for compilation to finish." caption="**Figure 5** — *Compiling*, [xkcd no. 303](https://xkcd.com/303/), by Randall Munroe. The old excuse was that the code was compiling; now I can say the quota resets next week. Licensed under [CC BY-NC 2.5](https://creativecommons.org/licenses/by-nc/2.5/)." %}
