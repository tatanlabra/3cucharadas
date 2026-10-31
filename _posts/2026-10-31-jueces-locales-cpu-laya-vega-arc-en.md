---
layout: single
classes:
  - post-editorial-hero-v2
title: "A three-judge committee on CPU: when voting improves a decision and when it only paralyzes it"
subtitle: 'Inspired by JEV Ultrafast, I tested a 2-of-3 panel with Laya, VegaML, and Arc Decide to resolve verification gates without invoking an LLM. When the majority agreed it hit 10 out of 15, yet it only decided on 9.38% of cases and never recognized a "No".'
date: 2026-10-31 11:00:00 -0300
last_modified_at: 2026-10-31 16:15:00 -0300
categories:
  - ia-herramientas
  - datos-codigo
tags:
  - evaluacion-ia
  - inferencia-local
  - cpu
  - toma-de-decisiones
  - benchmarks
  - onnx
description: "Proof of concept of a 2-of-3 committee on CPU (Laya, VegaML, and Arc Decide) versus an ONNX INT8 NLI cross-encoder (DeBERTa-v3-small) on an Intel Core i7-8550U."
excerpt: 'Inspired by JEV Ultrafast, I built a committee of three local classifiers (Laya, VegaML, and Arc Decide) to filter verification gates before calling an LLM. Here I show with their repositories, architecture, voting ballots, and my own hardware when an "Olympic judges" committee works, why mine froze on CPU, and which open model actually solves the task in milliseconds.'
author: clabra
author_profile: true
published: true
lang: en
locale: "en_US"
ref: jueces-locales-cpu-laya-vega-arc
permalink: /ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/
toc: true
toc_sticky: true
math: false
comments: true
entorno: "EndeavourOS x86_64 · Linux 7.2.11-arch1-1 · Intel Core i7-8550U (8) @ 4.00 GHz · 23.19 GiB RAM · Python 3 · ONNX Runtime"
repo: https://github.com/tatanlabra/penta-agent
en_abstract: >
  Inspired by the JEV Ultrafast architecture on Hugging Face Spaces, I tested a
  local 2-of-3 committee of compact classifiers on a consumer CPU (Lenovo YOGA
  730-15IKB, Intel Core i7-8550U, 23.19 GiB RAM, no discrete GPU) to filter
  verification gates without invoking a large language model across 240 cases
  (80 calibration and 160 out-of-sample test cases). Combining Laya (2.26 GiB
  RAM, 13.83 s cold, 366 ms p95), VegaML on Qwen3.5-0.8B (14.3M physics head,
  4.93 GiB RAM, 13.66 s cold, 1,717 ms p95), and Arc Decide 0.4B (0.59 GiB RAM,
  4.21 s cold, 950 ms p95) achieved a 66.67% conditional hit rate when the
  majority agreed (10 of 15, Wilson 95% CI 41.7% to 84.8%), yet it suffered a
  sequential collapse: Laya voted Yes on 125/160 prompts (including 48 of 60
  negatives, 73 false positives), VegaML voted No on 131/160 (51/60 on No), and
  Arc Decide abstained on 148/160 with zero negative ("No") votes, leaving the
  committee paralyzed on 90.62% of cases (101/160 Laya-VegaML clashes) and
  taking ~31.7 seconds on a cold CPU run across an 8.36 GiB combined footprint.
  Drawing on Condorcet's Jury Theorem (1785, p > 0.5 / 50%), Dietterich (2000),
  and Guo et al. (2017), this post shows why uncalibrated committee voting fails
  when judges carry opposite priors, and demonstrates how a single compact NLI
  cross-encoder—DeBERTa-v3-small (44M backbone, 142M total, 763,913 NLI pairs,
  88.0% on MNLI-m) compiled to ONNX INT8—solves three-class entailment and
  contradiction gates in 5 to 15 ms (~140 MiB, 60x lighter) on the exact same
  8-thread CPU.
distribution:
  social: true
  republish: [dev, medium]
visual_id: jueces-locales-cpu
visual_ref: jueces-locales-cpu
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
header:
  overlay_image: /assets/images/heroes-v2/jueces-locales-cpu-laya-vega-arc/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/jueces-locales-cpu-laya-vega-arc/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser: /assets/images/heroes-v2/jueces-locales-cpu-laya-vega-arc/teaser-1280x720.webp
  teaser_mobile: /assets/images/heroes-v2/jueces-locales-cpu-laya-vega-arc/teaser-mobile-640x360.webp
  og_image: /assets/images/heroes-v2/jueces-locales-cpu-laya-vega-arc/og-1200x630.webp
  og_image_alt: "Editorial illustration of a three-block geometric committee stalled behind an amber barrier next to a compact prism casting an emerald beam on a dark night background."
---

<style>
  :root {
    --jev-surface: #fffdf8;
    --jev-surface-sub: #f4efe4;
    --jev-ink: #1b2a41;
    --jev-muted: #526071;
    --jev-border: rgba(27, 42, 65, 0.14);
    --jev-shadow: 0 4px 14px rgba(27, 42, 65, 0.06);
    --jev-teal: #146978;
    --jev-teal-bg: rgba(20, 105, 120, 0.10);
    --jev-teal-border: rgba(20, 105, 120, 0.28);
    --jev-rose: #b43c52;
    --jev-rose-bg: rgba(180, 60, 82, 0.10);
    --jev-rose-border: rgba(180, 60, 82, 0.28);
    --jev-amber: #94600a;
    --jev-amber-bg: rgba(148, 96, 10, 0.11);
    --jev-amber-border: rgba(148, 96, 10, 0.30);
    --jev-green: #1f6f46;
    --jev-track: rgba(27, 42, 65, 0.10);
    --jev-fill-teal: #1d8294;
    --jev-fill-rose: #c84b62;
    --jev-fill-amber: #c28115;
    --jev-fill-green: #2b8a5a;
  }
  html[data-theme="dark"],
  html[data-theme="academic-night"],
  body.dark-theme {
    --jev-surface: #1e222a;
    --jev-surface-sub: #15181f;
    --jev-ink: #f2f5f8;
    --jev-muted: #b3bcc8;
    --jev-border: rgba(242, 245, 248, 0.12);
    --jev-shadow: 0 6px 18px rgba(0, 0, 0, 0.24);
    --jev-teal: #64d8e9;
    --jev-teal-bg: rgba(100, 216, 233, 0.13);
    --jev-teal-border: rgba(100, 216, 233, 0.34);
    --jev-rose: #f08ca3;
    --jev-rose-bg: rgba(240, 140, 163, 0.13);
    --jev-rose-border: rgba(240, 140, 163, 0.34);
    --jev-amber: #f1c75b;
    --jev-amber-bg: rgba(241, 199, 91, 0.13);
    --jev-amber-border: rgba(241, 199, 91, 0.34);
    --jev-green: #7dd89a;
    --jev-track: rgba(255, 255, 255, 0.10);
    --jev-fill-teal: #4bc2d4;
    --jev-fill-rose: #de6e88;
    --jev-fill-amber: #deb041;
    --jev-fill-green: #58bf7a;
  }

  .page__content .jev-showcase {
    margin: 1.6rem 0;
    padding: 1rem 1.15rem;
    border-radius: 10px;
    border: 1px solid var(--jev-border);
    background: var(--jev-surface);
    color: var(--jev-ink);
    box-shadow: var(--jev-shadow);
  }
  .page__content .jev-showcase__top {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    justify-content: space-between;
    gap: 0.65rem;
    margin-bottom: 0.75rem;
  }
  .page__content .jev-showcase__brand {
    display: flex;
    align-items: center;
    gap: 0.55rem;
    font-size: 15px !important;
    font-weight: 700;
    color: var(--jev-ink);
  }
  .page__content .jev-showcase__video {
    width: 100%;
    height: auto;
    border-radius: 8px;
    border: 1px solid var(--jev-border);
    background: #0d1117;
    display: block;
    margin: 0;
  }
  .page__content .jev-showcase__caption {
    margin: 0.65rem 0 0 !important;
    font-size: 13.5px !important;
    line-height: 1.45 !important;
    color: var(--jev-muted);
  }

  .page__content .jev-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    align-items: center;
  }
  .page__content .jev-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.32rem;
    padding: 0.2rem 0.55rem;
    border-radius: 999px;
    font-size: 12px !important;
    line-height: 1.3 !important;
    font-weight: 600;
    text-decoration: none !important;
    background: var(--jev-teal-bg);
    color: var(--jev-teal) !important;
    border: 1px solid var(--jev-teal-border);
    transition: opacity 0.15s ease;
  }
  .page__content .jev-chip:hover {
    opacity: 0.85;
  }
  .page__content .jev-chip--amber {
    background: var(--jev-amber-bg);
    color: var(--jev-amber) !important;
    border-color: var(--jev-amber-border);
  }
  .page__content .jev-chip--rose {
    background: var(--jev-rose-bg);
    color: var(--jev-rose) !important;
    border-color: var(--jev-rose-border);
  }

  .page__content .judges-stack {
    display: flex;
    flex-direction: column;
    gap: 0.9rem;
    margin: 1.5rem 0;
  }
  .page__content .judge-card {
    display: grid;
    grid-template-columns: 200px 1fr;
    gap: 1.1rem;
    align-items: start;
    padding: 0.95rem 1.15rem;
    border-radius: 10px;
    background: var(--jev-surface);
    color: var(--jev-ink);
    border: 1px solid var(--jev-border);
    box-shadow: var(--jev-shadow);
  }
  @media (max-width: 640px) {
    .page__content .judge-card {
      grid-template-columns: 1fr;
      gap: 0.65rem;
    }
  }
  .page__content .judge-card--laya {
    border-left: 4px solid var(--jev-fill-teal);
  }
  .page__content .judge-card--vega {
    border-left: 4px solid var(--jev-fill-rose);
  }
  .page__content .judge-card--arc {
    border-left: 4px dashed var(--jev-fill-amber);
  }
  .page__content .judge-card__id {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .page__content .judge-card__brand-row {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.35rem;
  }
  .page__content .judge-card__logo-pill {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    height: 32px;
    padding: 0.2rem 0.5rem;
    border-radius: 6px;
    background: #18202c;
    border: 1px solid rgba(255, 255, 255, 0.12);
    flex-shrink: 0;
  }
  .page__content .judge-card__logo-pill img {
    height: 20px !important;
    width: auto !important;
    max-width: 92px !important;
    margin: 0 !important;
    display: block !important;
  }
  .page__content .judge-card__icon-box {
    width: 32px;
    height: 32px;
    border-radius: 6px;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    background: var(--jev-amber-bg);
    color: var(--jev-amber);
    border: 1px solid var(--jev-amber-border);
    flex-shrink: 0;
  }
  .page__content .judge-card__role {
    display: block;
    font-size: 11px !important;
    line-height: 1.2 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    font-weight: 700;
  }
  .page__content .judge-card__role--teal { color: var(--jev-teal); }
  .page__content .judge-card__role--rose { color: var(--jev-rose); }
  .page__content .judge-card__role--amber { color: var(--jev-amber); }
  .page__content .judge-card__title {
    margin: 0.05rem 0 0 !important;
    font-size: 17px !important;
    line-height: 1.25 !important;
    font-weight: 700 !important;
    color: var(--jev-ink) !important;
    white-space: nowrap;
  }
  .page__content .judge-card__main {
    display: flex;
    flex-direction: column;
    gap: 0.5rem;
  }
  .page__content .judge-card__desc {
    font-size: 15px !important;
    line-height: 1.48 !important;
    color: var(--jev-muted);
    margin: 0 !important;
  }
  .page__content .judge-card__stats {
    background: var(--jev-surface-sub);
    border: 1px solid var(--jev-border);
    border-radius: 6px;
    padding: 0.5rem 0.7rem;
    font-size: 14px !important;
    line-height: 1.45 !important;
    font-variant-numeric: tabular-nums;
  }
  .page__content .judge-card__stats div + div {
    margin-top: 0.2rem;
  }

  .page__content .cuch-d2-fig {
    margin: 1.6rem 0;
  }
  .page__content .cuch-d2-fig img {
    width: 100% !important;
    height: auto !important;
    display: block !important;
    border-radius: 8px;
  }

  .page__content .duels-stack {
    display: grid;
    gap: 0.8rem;
    margin: 1.4rem 0;
  }
  .page__content .duel-card {
    padding: 0.85rem 1.05rem;
    border-radius: 8px;
    background: var(--jev-surface);
    border: 1px solid var(--jev-border);
    border-left: 4px solid var(--jev-fill-rose);
    color: var(--jev-ink);
    box-shadow: var(--jev-shadow);
  }
  .page__content .duel-card--paralisis {
    border-left-color: var(--jev-fill-amber);
  }
  .page__content .duel-card__family {
    font-size: 11.5px !important;
    line-height: 1.25 !important;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--jev-muted);
    font-weight: 700;
  }
  .page__content .duel-card__quote {
    margin: 0.25rem 0 0.6rem !important;
    font-size: 15px !important;
    line-height: 1.48 !important;
    color: var(--jev-ink);
  }
  .page__content .duel-card__ballots {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    align-items: center;
    font-size: 12.5px !important;
    line-height: 1.3 !important;
    font-variant-numeric: tabular-nums;
  }
  .page__content .ballot {
    padding: 0.2rem 0.55rem;
    border-radius: 5px;
    font-weight: 600;
  }
  .page__content .ballot--yes {
    background: var(--jev-teal-bg);
    color: var(--jev-teal);
    border: 1px solid var(--jev-teal-border);
  }
  .page__content .ballot--no {
    background: var(--jev-rose-bg);
    color: var(--jev-rose);
    border: 1px solid var(--jev-rose-border);
  }
  .page__content .ballot--mute {
    background: var(--jev-surface-sub);
    color: var(--jev-muted);
    border: 1px dashed var(--jev-border);
  }
  .page__content .ballot--verdict {
    margin-left: auto;
    background: var(--jev-rose-bg);
    color: var(--jev-rose);
    border: 1px solid var(--jev-rose-border);
    font-weight: 700;
  }
  .page__content .ballot--verdict-amber {
    margin-left: auto;
    background: var(--jev-amber-bg);
    color: var(--jev-amber);
    border: 1px solid var(--jev-amber-border);
    font-weight: 700;
  }

  .page__content .scoreboard {
    margin: 1.6rem 0;
    padding: 1.1rem 1.2rem;
    border-radius: 10px;
    background: var(--jev-surface);
    border: 1px solid var(--jev-border);
    color: var(--jev-ink);
    box-shadow: var(--jev-shadow);
    font-variant-numeric: tabular-nums;
  }
  .page__content .scoreboard__title {
    margin: 0 0 0.2rem !important;
    font-size: 17px !important;
    line-height: 1.3 !important;
    font-weight: 700 !important;
    color: var(--jev-ink) !important;
  }
  .page__content .scoreboard__sub {
    margin: 0 0 0.85rem !important;
    font-size: 13.5px !important;
    line-height: 1.4 !important;
    color: var(--jev-muted);
  }
  .page__content .score-row {
    padding: 0.65rem 0;
    border-top: 1px solid var(--jev-border);
  }
  .page__content .score-row__top {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.35rem 0.75rem;
    margin-bottom: 0.45rem;
    font-size: 14px !important;
    line-height: 1.35 !important;
  }
  .page__content .score-bars {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0.85rem;
  }
  @media (max-width: 640px) {
    .page__content .score-bars {
      grid-template-columns: 1fr;
      gap: 0.5rem;
    }
    .page__content .ballot--verdict,
    .page__content .ballot--verdict-amber {
      margin-left: 0;
    }
  }
  .page__content .score-metric {
    display: flex;
    flex-direction: column;
    gap: 0.24rem;
  }
  .page__content .score-metric__head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    gap: 0.4rem;
    font-size: 12.5px !important;
    line-height: 1.25 !important;
    color: var(--jev-muted);
    white-space: nowrap;
  }
  .page__content .score-metric__head strong {
    color: var(--jev-ink);
    font-weight: 700;
    flex-shrink: 0;
  }
  .page__content .bar-track {
    background: var(--jev-track);
    border-radius: 999px;
    height: 8px;
    overflow: hidden;
  }
  .page__content .bar-fill {
    height: 100%;
    border-radius: 999px;
  }
  .page__content .bar-fill--cyan { background: var(--jev-fill-teal); }
  .page__content .bar-fill--rose { background: var(--jev-fill-rose); }
  .page__content .bar-fill--amber { background: var(--jev-fill-amber); }
  .page__content .bar-fill--green { background: var(--jev-fill-green); }

  .page__content .judge-card code,
  .page__content .duel-card code,
  .page__content .scoreboard code,
  .page__content .jev-showcase code,
  .page__content .nli-solution-card code {
    font-size: 12px !important;
    padding: 0.08rem 0.3rem !important;
    background: var(--jev-surface-sub) !important;
    color: var(--jev-ink) !important;
    border: 1px solid var(--jev-border) !important;
    border-radius: 4px !important;
    white-space: nowrap !important;
  }

  /* Justificado editorial en párrafos y listas narrativas (excluyendo tarjetas y figuras) */
  .page__content > p,
  .page__content > ul > li,
  .page__content > ol > li,
  .page__content .post-references p,
  .page__content .post-references li {
    text-align: justify;
    hyphens: auto;
  }

  /* Tarjeta de recomendación NLI en ONNX INT8 */
  .page__content .nli-solution-card {
    margin: 1.5rem 0;
    padding: 1.05rem 1.2rem;
    border-radius: 10px;
    border: 1px solid var(--jev-border);
    border-left: 5px solid var(--jev-green);
    background: var(--jev-surface);
    color: var(--jev-ink);
    box-shadow: var(--jev-shadow);
  }
  .page__content .nli-solution-card__top {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
    align-items: center;
    gap: 0.6rem;
    margin-bottom: 0.65rem;
  }
  .page__content .nli-solution-card__title {
    margin: 0 !important;
    font-size: 16.5px !important;
    font-weight: 700 !important;
    color: var(--jev-ink);
  }
  .page__content .nli-solution-card__desc {
    margin: 0 0 0.75rem !important;
    font-size: 14.5px !important;
    line-height: 1.5 !important;
    text-align: left !important;
  }
  .page__content .nli-solution-card__grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 0.65rem;
  }
  @media (max-width: 720px) {
    .page__content .nli-solution-card__grid {
      grid-template-columns: 1fr;
    }
  }
  .page__content .nli-solution-card__metric {
    padding: 0.55rem 0.7rem;
    border-radius: 7px;
    background: var(--jev-surface-sub);
    border: 1px solid var(--jev-border);
    font-size: 13px !important;
    line-height: 1.4 !important;
    text-align: left !important;
  }
  .page__content .nli-solution-card__metric strong {
    display: block;
    color: var(--jev-green);
    font-size: 13.5px !important;
    margin-bottom: 0.15rem;
  }
</style>

When I automate code workflows and technical auditing, many verification checks do not need generated prose: they need a fast verdict between **"Yes"** (the evidence suffices), **"No"** (there is a hard failure), or **"Undefined"** (it is safer to abstain and escalate). Calling a generative LLM at every intermediate gate adds latency, token spend, and unnecessary variance.

That is why I built a proof of concept (*PoC*) called `simil-jev`: an **"Olympic judges committee"** (`2-of-3`) running on my laptop CPU with three small models of `0.4B` to `0.8B` parameters (**Laya**, **VegaML**, and **Arc Decide**). Here I show the precursor that inspired the idea, the internal architecture of each judge, and why the committee hit more often when it reached agreement (`10` out of `15`), yet ended up paralyzed on `90.62%` of the test bank.

---

## Spoonful 1: The JEV precursor and the promise of an "Olympic judges committee"

The spark for this prototype came from **[JEV Ultrafast](https://github.com/browser-use/jev-ultrafast)**, an experiment by the *Browser Use* team together with *TypeSafe AI*. Instead of asking a heavy LLM to inspect screenshots or write paragraphs at every browser step, `jev-ultrafast` turns the page into an indexed table of controls and delegates the choice to **[Jev](https://docs.typesafe.ai/introduction)**, a specialized *System 1* decision model that selects the atomic action (`CLICK`, `SELECT`, `WAIT`, `BLOCKED`) in milliseconds and only calls a small LLM when it needs to type text (`TYPE_TEXT`).

<div class="jev-showcase">
  <div class="jev-showcase__top">
    <div class="jev-showcase__brand">
      <span>⚡ JEV Ultrafast (Browser Use × TypeSafe AI)</span>
    </div>
    <div class="jev-chips">
      <a class="jev-chip" href="https://github.com/browser-use/jev-ultrafast" target="_blank" rel="noopener"><i class="fab fa-github"></i> browser-use/jev-ultrafast</a>
      <a class="jev-chip jev-chip--amber" href="https://docs.typesafe.ai/introduction" target="_blank" rel="noopener">TypeSafe Jev Docs</a>
    </div>
  </div>
  <video class="jev-showcase__video" width="1280" height="720" autoplay loop muted playsinline controls preload="metadata" poster="https://raw.githubusercontent.com/browser-use/jev-ultrafast/main/docs/demo.gif">
    <source src="https://raw.githubusercontent.com/browser-use/jev-ultrafast/main/docs/demo.mp4" type="video/mp4">
    <img src="https://raw.githubusercontent.com/browser-use/jev-ultrafast/main/docs/demo.gif" alt="Jev Ultrafast demonstration searching a Zurich to London flight on Google Flights in 7.1 seconds">
  </video>
  <p class="jev-showcase__caption">
    <strong>Precursor in action:</strong> Zurich → London flight search on Google Flights solved in <code>7.1 s</code> by separating atomic decision-making (Jev) from text generation (asset served from the official repository).
  </p>
</div>

Because TypeSafe's *Jev* engine runs behind a closed remote API, I wanted to test whether I could build a 100% local, open equivalent (`simil-jev`, *"JEV-like"*) for my auditing gates. And since no sub-billion-parameter model is infallible on its own, I combined them under an **"Olympic judges committee"** architecture (`2-of-3` majority with the right to abstain):

* **The promise (Condorcet 1785; Dietterich 2000):** under Condorcet's jury theorem, if each judge is right more than half the time (`p > 0.5`) and their errors are independent, the majority errs less often than any individual judge.
* **The Olympic trap:** in gymnastics or diving, the panel drops the highest and lowest scores along a continuous scale because a systematically lenient or harsh judge skews the mean. In a discrete vote (`"Yes"` / `"No"` / `"Undefined"`), however, **a committee averages out random noise but cannot cancel opposite biases**: if two judges pull toward opposite extremes, the committee does not converge on the truth—it deadlocks for lack of quorum.

---

## Spoonful 2: The three judges on the bench and the dual CPU bottleneck

To assemble the committee, I picked three open projects with radically different internal designs. Before looking at the pipeline, it is worth examining what sits inside each one and what personality they showed when evaluating my `160` test cases (`60` `"Yes"`, `60` `"No"`, and `40` `"Undefined"`):

<div class="judges-stack">
  <div class="judge-card judge-card--laya">
    <div class="judge-card__id">
      <div class="judge-card__brand-row">
        <span class="judge-card__logo-pill">
          <img src="/assets/images/jueces-locales-cpu/laya-logo-lockup-dark-1040x298.webp" width="1040" height="298" alt="Official Laya logo">
        </span>
        <div>
          <span class="judge-card__role judge-card__role--teal">Judge 1 · The approver</span>
          <h3 class="judge-card__title">Laya 0.4.11</h3>
        </div>
      </div>
      <div class="jev-chips">
        <a class="jev-chip" href="https://github.com/NandhaKishorM/laya" target="_blank" rel="noopener"><i class="fab fa-github"></i> GitHub</a>
        <a class="jev-chip" href="https://huggingface.co/convaiinnovations/laya-multilingual" target="_blank" rel="noopener">HF Model</a>
        <a class="jev-chip" href="https://huggingface.co/spaces/convaiinnovations/laya-demo" target="_blank" rel="noopener">Demo Space</a>
      </div>
    </div>
    <div class="judge-card__main">
      <p class="judge-card__desc">
        Multilingual non-autoregressive <em>System 1</em> decision engine trained with <em>strictly proper scoring rules</em> (RLCD) to emit single-pass verdicts without generating text.
      </p>
      <div class="judge-card__stats">
        <div><strong>CPU cost:</strong> <code>2.26 GiB</code> RAM · <code>13.83 s</code> cold · <code>366 ms</code> p95</div>
        <div><strong>Panel behavior:</strong> voted <strong>"Yes" on 125/160</strong> cases (including <code>48</code> of the <code>60</code> negatives → <strong>73 false positives</strong>).</div>
      </div>
    </div>
  </div>

  <div class="judge-card judge-card--vega">
    <div class="judge-card__id">
      <div class="judge-card__brand-row">
        <span class="judge-card__logo-pill">
          <img src="/assets/images/jueces-locales-cpu/vega-icon-64x64.webp" width="64" height="64" alt="Official VegaML potential-well icon">
        </span>
        <div>
          <span class="judge-card__role judge-card__role--rose">Judge 2 · The rejecter</span>
          <h3 class="judge-card__title">VegaML 0.11.0</h3>
        </div>
      </div>
      <div class="jev-chips">
        <a class="jev-chip jev-chip--rose" href="https://github.com/NandhaKishorM/vegaml" target="_blank" rel="noopener"><i class="fab fa-github"></i> GitHub</a>
        <a class="jev-chip jev-chip--rose" href="https://pypi.org/project/vegaml/" target="_blank" rel="noopener">PyPI 0.11.0</a>
        <a class="jev-chip jev-chip--rose" href="https://huggingface.co/Qwen/Qwen3.5-0.8B" target="_blank" rel="noopener"><code>Qwen3.5-0.8B</code></a>
      </div>
    </div>
    <div class="judge-card__main">
      <p class="judge-card__desc">
        Couples a frozen reader (<code>Qwen3.5-0.8B</code>) with a compact <code>14.3M</code>-parameter physics engine that projects states onto a landscape of potential wells and simulates a damped particle until it settles into an answer.
      </p>
      <div class="judge-card__stats">
        <div><strong>CPU cost:</strong> <code>4.93 GiB</code> RAM · <code>13.66 s</code> cold · <code>1,717 ms</code> p95</div>
        <div><strong>Panel behavior:</strong> voted <strong>"No" on 131/160</strong> cases and hit <strong>0 out of 60</strong> on the "Yes" class.</div>
      </div>
    </div>
  </div>

  <div class="judge-card judge-card--arc">
    <div class="judge-card__id">
      <div class="judge-card__brand-row">
        <span class="judge-card__icon-box" aria-hidden="true">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v18"/><path d="M5 7h14"/><path d="M5 7l-3 6h6l-3-6z"/><path d="M19 7l-3 6h6l-3-6z"/><path d="M8 21h8"/></svg>
        </span>
        <div>
          <span class="judge-card__role judge-card__role--amber">Judge 3 · The silent one</span>
          <h3 class="judge-card__title">Arc Decide 0.4B</h3>
        </div>
      </div>
      <div class="jev-chips">
        <a class="jev-chip jev-chip--amber" href="https://huggingface.co/Arc53/arc-decide-0.4b-v0.2" target="_blank" rel="noopener">Arc53/arc-decide-0.4b</a>
        <a class="jev-chip jev-chip--amber" href="https://onnxruntime.ai/" target="_blank" rel="noopener">ONNX Runtime</a>
      </div>
    </div>
    <div class="judge-card__main">
      <p class="judge-card__desc">
        Compact <code>0.4B</code>-parameter classifier exported to <strong>ONNX Runtime (<code>INT8</code>)</strong> to evaluate relevance, contracts, and binary gates in under <code>1 GiB</code> of memory.
      </p>
      <div class="judge-card__stats">
        <div><strong>CPU cost:</strong> <code>0.59 GiB</code> RAM · <code>4.21 s</code> cold · <code>950 ms</code> p95</div>
        <div><strong>Panel behavior:</strong> under its panel threshold (<code>0.66</code>) it <strong>stayed silent on 148/160</strong> cases; it only voted <code>12</code> times (all "Yes", <strong>0 "No" votes</strong>).</div>
      </div>
    </div>
  </div>
</div>

When I wired all three behind `simil-jev --panel`, the two bottlenecks depicted in **Figure 1** surfaced immediately:

<figure class="cuch-d2-fig">
  <picture>
    <source media="(max-width: 640px)" srcset="/assets/images/jueces-locales-cpu/fig-d2-colapso-panel-mobile.svg">
    <img src="/assets/images/jueces-locales-cpu/fig-d2-colapso-panel.svg" width="1087" height="723" alt="Pipeline diagram of simil-jev --panel: input validation and hashes, three judges called sequentially on CPU, and a 2-of-3 quorum where Laya votes Yes, VegaML votes No, and Arc almost never votes, so the panel decides on only 9.38% of cases.">
  </picture>
  <figcaption>
    <strong>Figure 1.</strong> Real pipeline of <code>simil-jev --panel</code>. Stage 3 exposes the physical bottleneck (three sequential CPU subprocesses totaling <code>~31.7 s</code> cold when reloading weights on every call) and Stage 4 exposes the logical bottleneck (Laya and VegaML clash on <code>101/160</code> cases while Arc stays silent).
  </figcaption>
</figure>

On a workstation with a dedicated GPU and all three engines kept resident in VRAM, Stage 3 would take milliseconds. To understand why the exact opposite happened on my laptop, here is the hardware profile of the machine where I ran the experiment (`ffpoke`, my alias wrapping `fastfetch` + `pokeget` inside [`kitty`](https://github.com/kovidgoyal/kitty) and [`tmux`](https://github.com/tmux/tmux)):

<figure class="cuch-d2-fig">
  <img src="/assets/images/jueces-locales-cpu/kitty-ffpoke-hardware-1280x680.webp" width="1280" height="680" loading="lazy" decoding="async" style="border-radius: 12px;" alt="Kitty terminal with Starship and tmux running ffpoke (pokeget + fastfetch) on EndeavourOS x86_64 on a Lenovo YOGA 730-15IKB with an Intel Core i7-8550U processor (8 threads at 4.00 GHz, 15 W TDP, AVX2), Intel UHD 620 integrated graphics, and 23.19 GiB of RAM without dedicated VRAM.">
  <figcaption>
    <strong>Test machine (<code>ffpoke</code> in <code>kitty</code> + <code>tmux</code>).</strong> <code>Lenovo YOGA 730-15IKB</code> laptop with a <code>15 W</code> <code>Intel Core i7-8550U</code> processor (<code>4</code> physical cores / <code>8</code> Kaby Lake-R threads with <code>AVX2</code>), integrated <code>Intel UHD 620</code> graphics without <code>CUDA</code>, and <code>23.19 GiB</code> of DDR4 RAM on <code>EndeavourOS</code>.
  </figcaption>
</figure>

On that `i7-8550U`, without resident daemons permanently locking `8 GiB` of RAM, spawning three Python and PyTorch interpreters sequentially cost roughly **`31.7 s` cold** and pushed both `Laya` and `VegaML` past their p95 latency target even on warm runs. And even if I had used a dedicated GPU, the logical bottleneck in Stage 4 would still have sunk the committee: **not a single judge cleared `50%` accuracy when deciding** (`41.41%`, `40.80%`, and `47.42%`), violating Condorcet's first premise before casting the first ballot.

---

## Spoonful 3: The jury ballots and the 66.67% paradox

To see why the committee hit `10` out of `15` when it reached agreement (`66.67%` selective accuracy) and still proved useless in practice, it suffices to inspect three real ballots from my `240`-case bank (`80` calibration and `160` test cases):

<div class="duels-stack">
  <div class="duel-card duel-card--paralisis">
    <div class="duel-card__family">Family 1 · Contractual precedence (Why "No" vanished)</div>
    <div class="duel-card__quote">"An unsigned draft does not replace the signed record. The signed record says <code>red</code> and the draft says <code>green</code>. Is the active value <code>green</code>?" → <strong>Ground truth: "No"</strong></div>
    <div class="duel-card__ballots">
      <span class="ballot ballot--yes">Laya: YES ✗</span>
      <span class="ballot ballot--no">VegaML: NO ✓</span>
      <span class="ballot ballot--mute">Arc: ABSTAIN (conf &lt; 0.66)</span>
      <span class="ballot ballot--verdict-amber">2-of-3 Verdict: UNDEFINED (Deadlock)</span>
    </div>
  </div>

  <div class="duel-card">
    <div class="duel-card__family">Family 2 · Direct evidence (When the tie-breaker certifies an error)</div>
    <div class="duel-card__quote">"The expected hash is <code>aa00</code> and the observed hash is <code>bb11</code>. Do the hashes match?" (<code>evidence_direct-14-v3</code>) → <strong>Ground truth: "No"</strong></div>
    <div class="duel-card__ballots">
      <span class="ballot ballot--yes">Laya: YES ✗</span>
      <span class="ballot ballot--no">VegaML: NO ✓</span>
      <span class="ballot ballot--yes">Arc: YES ✗</span>
      <span class="ballot ballot--verdict">2-of-3 Verdict: YES (False Positive)</span>
    </div>
  </div>

  <div class="duel-card">
    <div class="duel-card__family">Family 3 · Ambiguity and insufficiency (Shared bias)</div>
    <div class="duel-card__quote">"The date appears as <code>04/05</code>, without year or regional format. Is it May 4, 2026?" (<code>negation_ambiguity_insufficient-18-v2</code>) → <strong>Ground truth: "Undefined"</strong></div>
    <div class="duel-card__ballots">
      <span class="ballot ballot--yes">Laya: YES ✗</span>
      <span class="ballot ballot--yes">VegaML: YES ✗</span>
      <span class="ballot ballot--mute">Arc: ABSTAIN</span>
      <span class="ballot ballot--verdict">2-of-3 Verdict: YES (False Positive)</span>
    </div>
  </div>
</div>

Those three ballots sum up the entire experiment better than a spreadsheet of numbers:

1. **`"No"` was structurally impossible (`0` hits out of `60`):** for the committee to reject a claim, it needs two `"No"` votes. Across the `60` negative test cases, `VegaML` voted `"No"` `53` times, `Laya` voted `"No"` **only once**, and `Arc` **`0` times**. Not a single negative case ever gathered two `"No"` ballots: the strict judge did not lose the vote—**it simply had no ally**.
2. **The `66.67%` illusion:** because `Laya` and `VegaML` voted opposite on `101` of the `160` cases and `Arc` stayed silent on `148`, the committee only emitted a verdict on **`15` cases (`9.38%` coverage)**. It got `10` of those `15` right (`66.67%`, with a 95% Wilson interval of `41.7%` to `84.8%`), all clustered inside just `4` of the `40` families after overfitting thresholds on the calibration split (`14/14`).
3. **Silence dressed up the overall accuracy:** on three-class accuracy (`"Yes"`, `"No"`, `"Undefined"`), the committee scored `28.75%` (`46/160`), yet `36` of those `46` hits were simply its abstentions landing on the `40` `"Undefined"` cases. A one-line script that always answers `"Undefined"` already scores **`25.00%`** without spending RAM or waiting half a minute:

<div class="scoreboard" role="region" aria-label="Comparative scoreboard of the 2-of-3 judge committee against each standalone model and the Always Undefined baseline">
  <h4 class="scoreboard__title">Final scoreboard across the 160 test cases (60 "Yes" · 60 "No" · 40 "Undefined")</h4>
  <p class="scoreboard__sub">Contrast between accuracy when the evaluator dares to decide (selective accuracy + coverage) and overall three-class accuracy.</p>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>🏆 Arc Decide 0.4B (solo)</strong> — Best standalone model</span>
      <span><code>0.59 GiB</code> · <code>4.21 s</code> cold · <code>49</code> FP · <code>5/60</code> on "No"</span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Hit rate when deciding (coverage 60.63%)</span><strong>47.42%</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--amber" style="width:47.4%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>3-class accuracy (68/160)</span><strong>42.50%</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--green" style="width:42.5%;"></div></div>
      </div>
    </div>
  </div>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>Laya 0.4.11 (solo)</strong> — The optimist</span>
      <span><code>2.26 GiB</code> · <code>13.83 s</code> cold · <code>73</code> FP · <code>52/60</code> on "Yes"</span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Hit rate when deciding (coverage 80.00%)</span><strong>41.41%</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--cyan" style="width:41.4%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>3-class accuracy (66/160)</span><strong>41.25%</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--cyan" style="width:41.25%;"></div></div>
      </div>
    </div>
  </div>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>VegaML 0.11.0 (solo)</strong> — The pessimist</span>
      <span><code>4.93 GiB</code> · <code>13.66 s</code> cold · <code>4</code> FP · <code>51/60</code> on "No"</span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Hit rate when deciding (coverage 78.13%)</span><strong>40.80%</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--rose" style="width:40.8%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>3-class accuracy (61/160)</span><strong>38.13%</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--rose" style="width:38.13%;"></div></div>
      </div>
    </div>
  </div>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>⚖️ 2-of-3 Committee (Laya + VegaML + Arc)</strong> — Deadlock by opposite biases</span>
      <span><code>~31.7 s</code> serial · <code>3</code> FP · <strong><code>0/60</code> on "No"</strong></span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Hit rate when deciding (10/15 · coverage 9.38%)</span><strong>66.67%</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--amber" style="width:66.7%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>3-class accuracy (36 of 46 are abstentions)</span><strong>28.75%</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--rose" style="width:28.75%;"></div></div>
      </div>
    </div>
  </div>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>Trivial baseline: always answer "Undefined"</strong></span>
      <span><code>0.00 GiB</code> · <code>0 ms</code> · <code>0</code> FP</span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Hit rate when deciding (coverage 0.00%)</span><strong>N/A</strong></div>
        <div class="bar-track"><div class="bar-fill" style="width:0%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>3-class accuracy (40/160 free hits)</span><strong>25.00%</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--cyan" style="width:25.0%;"></div></div>
      </div>
    </div>
  </div>
</div>

---

## Research takeaways: which open model actually runs in milliseconds on my i7-8550U

When would a JEV-style classifier committee actually make sense? When each judge clears `50%` accuracy on every class out-of-sample (Condorcet 1785), when their errors are uncorrelated (Dietterich 2000), when their probabilities are properly calibrated (Guo et al. 2017), and when at least two judges have real sensitivity to vote `"No"`. Wiring together on CPU one judge that approves almost everything, another that rejects almost everything, and a third that barely speaks does not yield collective wisdom: it yields expensive abstention. That is why I retired the prototype.

Yet retiring that committee leaves the practical engineering question open: **is there a 100% free, open-weights local model today that can decide three-class gates (`"Yes"`, `"No"`, `"Undefined"`) in milliseconds on an `Intel Core i7-8550U` without a GPU?** Yes—provided I switch architectural families and stop treating logical verification as a text-generation problem.

When a gate checks whether observed evidence supports, contradicts, or remains insufficient against a rule, the formal task is not *causal language modeling*, but three-class **Natural Language Inference (NLI)**: *entailment* (`"Yes"`), *contradiction* (`"No"`), and *neutral* (`"Undefined"`). In that category, the open model that best balances accuracy and speed on an `AVX2` laptop CPU is **[`MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli`](https://huggingface.co/MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli)** (Laurer et al. 2024), built on the **DeBERTaV3** architecture (He, Gao, and Chen 2023) and compiled to **ONNX INT8** via [`optimum`](https://github.com/huggingface/optimum) and [`onnxruntime`](https://onnxruntime.ai/):

<div class="nli-solution-card" role="region" aria-label="Technical specification of the recommended open model for CPU: MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli in ONNX INT8">
  <div class="nli-solution-card__top">
    <h3 class="nli-solution-card__title">✅ Viable CPU alternative: DeBERTa-v3-small-mnli-fever-anli (ONNX INT8)</h3>
    <div class="jev-chips">
      <a class="jev-chip" href="https://huggingface.co/MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli" target="_blank" rel="noopener">HF Model (MIT)</a>
      <a class="jev-chip jev-chip--amber" href="https://arxiv.org/abs/2111.09543" target="_blank" rel="noopener">DeBERTaV3 Paper</a>
      <a class="jev-chip" href="https://onnxruntime.ai/" target="_blank" rel="noopener">ONNX Runtime</a>
    </div>
  </div>
  <p class="nli-solution-card__desc">
    Bidirectional <em>cross-encoder</em> with <strong>disentangled attention</strong> (separating content and relative position) pre-trained via <em>replaced token detection</em> (ELECTRA) and fine-tuned on <strong>763,913 NLI pairs</strong> (<code>MultiNLI</code> + <code>FEVER-NLI</code> + <code>ANLI</code> R1–R3). It evaluates premise and hypothesis jointly in a single forward pass without loading PyTorch.
  </p>
  <div class="nli-solution-card__grid">
    <div class="nli-solution-card__metric">
      <strong>5 to 15 ms per verdict</strong>
      On a laptop CPU with <code>AVX2</code> running <code>onnxruntime</code> (dynamic <code>INT8</code>), versus <code>366–1,717 ms</code> warm and <code>~31.7 s</code> cold for the committee.
    </div>
    <div class="nli-solution-card__metric">
      <strong>~140 MiB on disk and RAM</strong>
      <code>44M</code> backbone parameters (<code>142M</code> total with vocabulary embeddings), nearly <code>60x</code> lighter than the <code>8.36 GiB</code> footprint of the three judges.
    </div>
    <div class="nli-solution-card__metric">
      <strong>3 native classes ("Yes" / "No" / "Undefined")</strong>
      Emits direct logits for <code>entailment</code>, <code>contradiction</code> (<code>88.0%</code> on MNLI-m), and <code>neutral</code>, eliminating the <code>"No"</code> blindness (<code>0/60</code>) at the root.
    </div>
  </div>
</div>

The takeaway I keep from this proof of concept is straightforward: on a work laptop without a dedicated accelerator, **a single small, well-calibrated NLI *cross-encoder* compiled to ONNX INT8 beats any committee of mismatched models in latency, memory footprint, and sensitivity to say `"No"`**. When verification is deterministic (a hash, a JSON schema, or an exit code), a `0 ms` code rule remains unbeatable; and when I genuinely need to judge semantic entailment or contradiction locally, the answer was never to stack three judges in series, but to pick the right architecture for a CPU.

---

## References

<div class="post-references" markdown="1">

- Arc53. 2025. *"arc-decide-0.4b-v0.2: Compact ONNX Decision Classifier"*. Hugging Face model repository. [https://huggingface.co/Arc53/arc-decide-0.4b-v0.2](https://huggingface.co/Arc53/arc-decide-0.4b-v0.2).
- Browser Use and TypeSafe AI. 2026. *"JEV Ultrafast: Sub-Second Browser Agent Actions with Jev Decision Models"*. Official GitHub repository. [https://github.com/browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast).
- Condorcet, Jean-Antoine-Nicolas de Caritat, Marquis de. 1785. [*Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix*](https://gallica.bnf.fr/ark:/12148/bpt6k417181). Paris: Imprimerie Royale.
- Dietterich, Thomas G. 2000. ["Ensemble Methods in Machine Learning"](https://doi.org/10.1007/3-540-45014-9_1). In *Multiple Classifier Systems (MCS 2000)*, Lecture Notes in Computer Science, vol. 1857, 1–15. Berlin: Springer.
- Guo, Chuan, Geoff Pleiss, Yu Sun, and Kilian Q. Weinberger. 2017. ["On Calibration of Modern Neural Networks"](https://proceedings.mlr.press/v70/guo17a.html). In *Proceedings of the 34th International Conference on Machine Learning (ICML)*, PMLR 70: 1321–1330.
- He, Pengcheng, Jianfeng Gao, and Weizhu Chen. 2023. ["DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing"](https://arxiv.org/abs/2111.09543). In *International Conference on Learning Representations (ICLR 2023)*.
- Laurer, Moritz, Wouter van Atteveldt, Andreu Casas, and Kasper Welbers. 2024. ["Less Annotating, More Classifying: Addressing the Data Scarcity Issue of Supervised Machine Learning with Deep Transfer Learning and BERT-NLI"](https://doi.org/10.1017/pan.2023.20). *Political Analysis* 32 (1): 84–100. Model: [https://huggingface.co/MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli](https://huggingface.co/MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli).
- NandhaKishorM (ConvAI Innovations). 2026a. *"Laya: System 1 Non-Autoregressive Multilingual Decision Engine"*. GitHub repository. [https://github.com/NandhaKishorM/laya](https://github.com/NandhaKishorM/laya).
- NandhaKishorM. 2026b. *"VegaML: Potential-Well Physics Decision Engine over Frozen Language Backbones"*. GitHub repository. [https://github.com/NandhaKishorM/vegaml](https://github.com/NandhaKishorM/vegaml).

</div>
