---
layout: single
classes:
  - post-editorial-hero-v2
title: "Un comité de tres jueces pequeños en CPU: cuándo votar mejora una decisión y cuándo solo la paraliza"
subtitle: 'Inspirado en JEV Ultrafast, probé un panel 2-de-3 con Laya, VegaML y Arc Decide para decidir gates sin invocar a un LLM. Cuando hubo acuerdo acertó 10 de 15, pero solo decidió en el 9,38 % de los casos y nunca reconoció un "No".'
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
description: "Prueba de concepto de un comité 2-de-3 en CPU (Laya, VegaML y Arc Decide) frente a un cross-encoder NLI en ONNX INT8 (DeBERTa-v3-small) sobre un Intel i7-8550U."
excerpt: 'Inspirado en JEV Ultrafast, armé un comité de tres clasificadores locales (Laya, VegaML y Arc Decide) para filtrar decisiones antes de llamar a un LLM. Aquí muestro con sus repositorios, arquitectura, papeletas de votación y mi propio hardware cuándo un comité tipo "jueces olímpicos" funciona, por qué el mío quedó paralizado en CPU y qué modelo libre sí resuelve la tarea en milisegundos.'
author: clabra
author_profile: true
published: true
lang: es
locale: "es_CL"
ref: jueces-locales-cpu-laya-vega-arc
permalink: /ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/
toc: true
toc_sticky: true
math: false
comments: true
entorno: "EndeavourOS x86_64 · Linux 7.2.11-arch1-1 · Intel Core i7-8550U (8) @ 4,00 GHz · 23,19 GiB RAM · Python 3 · ONNX Runtime"
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
  republish: []
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
  og_image_alt: "Ilustración editorial de un comité de tres bloques geométricos bloqueados tras una barrera ámbar frente a un prisma compacto con haz esmeralda sobre fondo nocturno."
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

Cuando automatizo flujos de código y auditoría técnica, muchas validaciones no piden redactar texto: piden decidir rápido entre **"Sí"** (la evidencia alcanza), **"No"** (hay un fallo duro) o **"Indefinido"** (conviene abstenerse y escalar). Llamar a un LLM generativo en cada compuerta intermedia suma latencia, gasto de tokens y variabilidad innecesaria.

Por eso armé una prueba de concepto (*PoC*) llamada `simil-jev`: un **"comité de jueces olímpicos"** (`2-de-3`) corriendo en la CPU de mi portátil con tres modelos pequeños de `0,4B` a `0,8B` parámetros (**Laya**, **VegaML** y **Arc Decide**). Aquí muestro el precursor que inspiró la idea, la arquitectura de cada juez y por qué el comité acertó más cuando lograba acuerdo (`10` de `15`), pero terminó paralizado en el `90,62 %` de los casos.

---

## Cucharada 1: El precursor JEV y la promesa del "comité de jueces olímpicos"

La chispa de este prototipo vino de **[JEV Ultrafast](https://github.com/browser-use/jev-ultrafast)**, un experimento del equipo de *Browser Use* junto a *TypeSafe AI*. En vez de pedirle a un LLM pesado que mire capturas de pantalla o redacte párrafos en cada paso del navegador, `jev-ultrafast` convierte la página en una tabla indexada de controles y delega la elección en **[Jev](https://docs.typesafe.ai/introduction)**, un modelo especializado de decisión (*System 1*) que escoge la acción atómica (`CLICK`, `SELECT`, `WAIT`, `BLOCKED`) en milisegundos y solo llama a un LLM pequeño cuando necesita escribir texto (`TYPE_TEXT`).

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
    <img src="https://raw.githubusercontent.com/browser-use/jev-ultrafast/main/docs/demo.gif" alt="Demostración de Jev Ultrafast buscando un vuelo Zúrich a Londres en Google Flights en 7,1 segundos">
  </video>
  <p class="jev-showcase__caption">
    <strong>Precursor en acción:</strong> búsqueda Zúrich → Londres en Google Flights resuelta en <code>7,1 s</code> separando decisión atómica (Jev) de generación de texto (activo servido desde el repositorio oficial).
  </p>
</div>

Como el motor *Jev* de TypeSafe opera detrás de una API remota y cerrada, quise comprobar si podía construir un equivalente 100 % local y abierto (`simil-jev`, *"símil de JEV"*) para mis compuertas de auditoría. Y como ningún modelo de menos de mil millones de parámetros es infalible por sí solo, decidí combinarlos bajo una arquitectura de **"comité de jueces olímpicos"** (`2-de-3` con derecho a abstención):

* **La promesa (Condorcet 1785; Dietterich 2000):** según el teorema del jurado de Condorcet, si cada juez acierta más de la mitad de las veces (`p > 0,5`) y sus errores son independientes, la mayoría se equivoca menos que cualquier juez individual.
* **La trampa olímpica:** en gimnasia o clavados el panel descarta las notas extremas sobre una escala continua, porque un juez sistemáticamente generoso o severo distorsiona el promedio. En un voto binario (`"Sí"` / `"No"` / `"Indefinido"`), en cambio, **un comité promedia ruido pero no corrige sesgos**: si dos jueces tiran hacia extremos opuestos, el comité no converge en la verdad, sino en la parálisis por falta de quórum.

---

## Cucharada 2: Los tres jueces en el banquillo y el doble cuello de botella en CPU

Para armar el comité seleccioné tres proyectos abiertos con arquitecturas radicalmente distintas entre sí. Antes de mirar el pipeline, vale la pena conocer qué hay dentro de cada uno y qué personalidad mostraron al evaluar mis `160` casos de prueba (`60` `"Sí"`, `60` `"No"` y `40` `"Indefinidos"`):

<div class="judges-stack">
  <div class="judge-card judge-card--laya">
    <div class="judge-card__id">
      <div class="judge-card__brand-row">
        <span class="judge-card__logo-pill">
          <img src="/assets/images/jueces-locales-cpu/laya-logo-lockup-dark-1040x298.webp" width="1040" height="298" alt="Logo oficial de Laya">
        </span>
        <div>
          <span class="judge-card__role judge-card__role--teal">Juez 1 · El que aprueba</span>
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
        Motor de decisión <em>System 1</em> no autorregresivo multilingüe entrenado con <em>strictly proper scoring rules</em> (RLCD) para emitir fallos en una sola pasada sin generar texto.
      </p>
      <div class="judge-card__stats">
        <div><strong>Costo CPU:</strong> <code>2,26 GiB</code> RAM · <code>13,83 s</code> frío · <code>366 ms</code> p95</div>
        <div><strong>Conducta en el panel:</strong> votó <strong>"Sí" en 125/160</strong> casos (incluidos <code>48</code> de los <code>60</code> negativos → <strong>73 falsos positivos</strong>).</div>
      </div>
    </div>
  </div>

  <div class="judge-card judge-card--vega">
    <div class="judge-card__id">
      <div class="judge-card__brand-row">
        <span class="judge-card__logo-pill">
          <img src="/assets/images/jueces-locales-cpu/vega-icon-64x64.webp" width="64" height="64" alt="Ícono oficial del pozo físico de VegaML">
        </span>
        <div>
          <span class="judge-card__role judge-card__role--rose">Juez 2 · El que rechaza</span>
          <h3 class="judge-card__title">VegaML 0.11.0</h3>
        </div>
      </div>
      <div class="jev-chips">
        <a class="jev-chip jev-chip--rose" href="https://github.com/NandhaKishorM/vegaml" target="_blank" rel="noopener"><i class="fab fa-github"></i> GitHub</a>
        <a class="jev-chip jev-chip--rose" href="https://pypi.org/project/vegaml/" target="_blank" rel="noopener">PyPI 0.11.0</a>
        <a class="jev-chip jev-chip--rose" href="https://huggingface.co/Qwen/Qwen3.5-0.8B" target="_blank" rel="noopener"><code>Qwen</code> 0,8B</a>
      </div>
    </div>
    <div class="judge-card__main">
      <p class="judge-card__desc">
        Combina un lector congelado (<code>Qwen</code> de <code>0,8B</code>) con un pequeño motor físico de <code>14,3M</code> de parámetros que proyecta estados en un paisaje de valles y simula una partícula con fricción hasta caer en una respuesta.
      </p>
      <div class="judge-card__stats">
        <div><strong>Costo CPU:</strong> <code>4,93 GiB</code> RAM · <code>13,66 s</code> frío · <code>1.717 ms</code> p95</div>
        <div><strong>Conducta en el panel:</strong> votó <strong>"No" en 131/160</strong> casos y acertó <strong>0 de 60</strong> en la clase "Sí".</div>
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
          <span class="judge-card__role judge-card__role--amber">Juez 3 · El silencioso</span>
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
        Clasificador compacto de <code>0,4B</code> parámetros exportado a <strong>ONNX Runtime (<code>INT8</code>)</strong> para evaluar relevancia, contratos y compuertas binarias en menos de <code>1 GiB</code> de memoria.
      </p>
      <div class="judge-card__stats">
        <div><strong>Costo CPU:</strong> <code>0,59 GiB</code> RAM · <code>4,21 s</code> frío · <code>950 ms</code> p95</div>
        <div><strong>Conducta en el panel:</strong> con su umbral de panel (<code>0,66</code>) <strong>calló en 148/160</strong> casos; solo votó <code>12</code> veces (todas "Sí", <strong>0 votos "No"</strong>).</div>
      </div>
    </div>
  </div>
</div>

Cuando conecté los tres bajo el comando `simil-jev --panel`, aparecieron de golpe los dos cuellos de botella que retrata la **Figura 1**:

<figure class="cuch-d2-fig">
  <picture>
    <source media="(max-width: 640px)" srcset="/assets/images/jueces-locales-cpu/fig-d2-colapso-panel-mobile.svg">
    <img src="/assets/images/jueces-locales-cpu/fig-d2-colapso-panel.svg" width="1087" height="723" alt="Diagrama del pipeline de simil-jev --panel: validación de entrada y hashes, tres jueces llamados en serie en CPU y un quórum 2-de-3 donde Laya vota Sí, VegaML vota No y Arc casi nunca vota, por lo que el panel decide solo en el 9,38 % de los casos.">
  </picture>
  <figcaption>
    <strong>Figura 1.</strong> Pipeline real de <code>simil-jev --panel</code>. En la etapa 3 está el cuello físico (tres subprocesos en serie en CPU que suman <code>~31,7 s</code> en frío al recargar pesos en cada consulta) y en la etapa 4 el cuello lógico (Laya y VegaML chocan en <code>101/160</code> casos mientras Arc permanece mudo).
  </figcaption>
</figure>

En una estación con GPU dedicada y los tres motores residentes en VRAM, la etapa 3 tomaría milisegundos. Para dimensionar por qué en mi máquina ocurrió lo contrario, basta mirar la radiografía del equipo donde corrí el experimento (`ffpoke`, mi alias sobre `fastfetch` + `pokeget` en [`kitty`](https://github.com/kovidgoyal/kitty) y [`tmux`](https://github.com/tmux/tmux)):

<figure class="cuch-d2-fig">
  <img src="/assets/images/jueces-locales-cpu/kitty-ffpoke-hardware-1280x680.webp" width="1280" height="680" loading="lazy" decoding="async" style="border-radius: 12px;" alt="Consola Kitty con Starship y tmux ejecutando ffpoke (pokeget + fastfetch) en EndeavourOS x86_64 sobre un Lenovo YOGA 730-15IKB con procesador Intel Core i7-8550U (8 hilos a 4,00 GHz, 15 W TDP, AVX2), gráfica integrada Intel UHD 620 y 23,19 GiB de RAM sin VRAM dedicada.">
  <figcaption>
    <strong>Máquina de prueba (<code>ffpoke</code> en <code>kitty</code> + <code>tmux</code>).</strong> Portátil <code>Lenovo YOGA 730-15IKB</code> con procesador <code>Intel Core i7-8550U</code> de <code>15 W</code> (<code>4</code> núcleos físicos / <code>8</code> hilos Kaby Lake-R con <code>AVX2</code>), gráfica integrada <code>Intel UHD 620</code> sin <code>CUDA</code> y <code>23,19 GiB</code> de RAM DDR4 sobre <code>EndeavourOS</code>.
  </figcaption>
</figure>

En ese `i7-8550U`, sin demonios residentes que secuestren `8 GiB` permanentes de RAM, levantar tres intérpretes de Python y PyTorch en serie costó unos **`31,7 s` en frío** y dejó a `Laya` y `VegaML` fuera de su meta de latencia p95 incluso en caliente. Y aun si hubiera tenido una GPU dedicada, el cuello lógico de la etapa 4 habría hundido igual al comité: **ningún juez superaba el `50 %` de acierto al decidir** (`41,41 %`, `40,80 %` y `47,42 %`), violando la primera condición de Condorcet antes de emitir el primer voto.

---

## Cucharada 3: Las papeletas del jurado y la paradoja del 66,67 %

Para ver por qué el comité acertó `10` de `15` cuando lograba acuerdo (`66,67 %` de exactitud selectiva) y aun así resultó inútil, basta abrir tres papeletas reales de mi banco de `240` casos (`80` de calibración y `160` de prueba):

<div class="duels-stack">
  <div class="duel-card duel-card--paralisis">
    <div class="duel-card__family">Familia 1 · Precedencia contractual (Por qué desapareció el "No")</div>
    <div class="duel-card__quote">"Un borrador sin firma no reemplaza el dato firmado. El firmado dice <code>rojo</code> y el borrador, <code>verde</code>. ¿El valor vigente es <code>verde</code>?" → <strong>Respuesta correcta: "No"</strong></div>
    <div class="duel-card__ballots">
      <span class="ballot ballot--yes">Laya: SÍ ✗</span>
      <span class="ballot ballot--no">VegaML: NO ✓</span>
      <span class="ballot ballot--mute">Arc: ABSTENCIÓN (conf &lt; 0,66)</span>
      <span class="ballot ballot--verdict-amber">Fallo 2-de-3: INDEFINIDO (Bloqueo)</span>
    </div>
  </div>

  <div class="duel-card">
    <div class="duel-card__family">Familia 2 · Evidencia directa (Cuando el desempate certifica un error)</div>
    <div class="duel-card__quote">"El hash esperado es <code>aa00</code> y el observado <code>bb11</code>. ¿Coinciden los hashes?" (<code>evidence_direct-14-v3</code>) → <strong>Respuesta correcta: "No"</strong></div>
    <div class="duel-card__ballots">
      <span class="ballot ballot--yes">Laya: SÍ ✗</span>
      <span class="ballot ballot--no">VegaML: NO ✓</span>
      <span class="ballot ballot--yes">Arc: SÍ ✗</span>
      <span class="ballot ballot--verdict">Fallo 2-de-3: SÍ (Falso Positivo)</span>
    </div>
  </div>

  <div class="duel-card">
    <div class="duel-card__family">Familia 3 · Ambigüedad e insuficiencia (Sesgo compartido)</div>
    <div class="duel-card__quote">"La fecha aparece como <code>04/05</code>, sin año ni convención regional. ¿Es el 4 de mayo de 2026?" (<code>negation_ambiguity_insufficient-18-v2</code>) → <strong>Respuesta correcta: "Indefinido"</strong></div>
    <div class="duel-card__ballots">
      <span class="ballot ballot--yes">Laya: SÍ ✗</span>
      <span class="ballot ballot--yes">VegaML: SÍ ✗</span>
      <span class="ballot ballot--mute">Arc: ABSTENCIÓN</span>
      <span class="ballot ballot--verdict">Fallo 2-de-3: SÍ (Falso Positivo)</span>
    </div>
  </div>
</div>

Esas tres papeletas resumen todo el experimento mejor que una sábana de números:

1. **El `"No"` era estructuralmente imposible (`0` aciertos de `60`):** para que el comité rechace algo necesita dos votos `"No"`. En los `60` casos negativos de prueba, `VegaML` votó `"No"` `53` veces, `Laya` apenas **`1` vez** y `Arc` **`0` veces**. Ningún caso negativo reunió jamás dos votos `"No"`: el juez severo no perdió la votación, **se quedó sin aliado**.
2. **La ilusión del `66,67 %`:** como `Laya` y `VegaML` votaron opuesto en `101` de los `160` casos y `Arc` permaneció callado en `148`, el comité solo emitió veredicto en **`15` casos (`9,38 %` de cobertura)**. Acertó `10` de esos `15` (`66,67 %`, con un intervalo de Wilson al 95 % de `41,7 %` a `84,8 %`), pero concentrados en apenas `4` de las `40` familias tras haber sobreajustado umbrales en calibración (`14/14`).
3. **Callar vestía de acierto la métrica global:** en exactitud de tres clases (`"Sí"`, `"No"`, `"Indefinido"`), el comité marcó `28,75 %` (`46/160`), pero `36` de esos `46` aciertos fueron simplemente sus abstenciones cayendo sobre los `40` casos `"Indefinidos"`. Un script vacío que responda siempre `"Indefinido"` ya obtiene **`25,00 %`** sin gastar RAM ni esperar medio minuto:

<div class="scoreboard" role="region" aria-label="Marcador comparativo del comité de jueces frente a cada modelo individual y el baseline Siempre Indefinido">
  <h4 class="scoreboard__title">Marcador final en los 160 casos de prueba (60 "Sí" · 60 "No" · 40 "Indefinidos")</h4>
  <p class="scoreboard__sub">Contraste entre el acierto cuando el evaluador se atreve a decidir (exactitud selectiva + cobertura) y la exactitud global de tres clases.</p>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>🏆 Arc Decide 0.4B (solo)</strong> — El mejor individual</span>
      <span><code>0,59 GiB</code> · <code>4,21 s</code> frío · <code>49</code> FP · <code>5/60</code> en "No"</span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Acierto al decidir (cobertura 60,63 %)</span><strong>47,42 %</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--amber" style="width:47.4%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>Exactitud 3-clases (68/160)</span><strong>42,50 %</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--green" style="width:42.5%;"></div></div>
      </div>
    </div>
  </div>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>Laya 0.4.11 (solo)</strong> — El optimista</span>
      <span><code>2,26 GiB</code> · <code>13,83 s</code> frío · <code>73</code> FP · <code>52/60</code> en "Sí"</span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Acierto al decidir (cobertura 80,00 %)</span><strong>41,41 %</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--cyan" style="width:41.4%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>Exactitud 3-clases (66/160)</span><strong>41,25 %</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--cyan" style="width:41.25%;"></div></div>
      </div>
    </div>
  </div>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>VegaML 0.11.0 (solo)</strong> — El pesimista</span>
      <span><code>4,93 GiB</code> · <code>13,66 s</code> frío · <code>4</code> FP · <code>51/60</code> en "No"</span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Acierto al decidir (cobertura 78,13 %)</span><strong>40,80 %</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--rose" style="width:40.8%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>Exactitud 3-clases (61/160)</span><strong>38,13 %</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--rose" style="width:38.13%;"></div></div>
      </div>
    </div>
  </div>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>⚖️ Comité 2-de-3 (Laya + VegaML + Arc)</strong> — Parálisis por sesgos opuestos</span>
      <span><code>~31,7 s</code> en serie · <code>3</code> FP · <strong><code>0/60</code> en "No"</strong></span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Acierto al decidir (10/15 · cobertura 9,38 %)</span><strong>66,67 %</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--amber" style="width:66.7%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>Exactitud 3-clases (36 de 46 son abstenciones)</span><strong>28,75 %</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--rose" style="width:28.75%;"></div></div>
      </div>
    </div>
  </div>

  <div class="score-row">
    <div class="score-row__top">
      <span><strong>Baseline trivial: responder siempre "Indefinido"</strong></span>
      <span><code>0,00 GiB</code> · <code>0 ms</code> · <code>0</code> FP</span>
    </div>
    <div class="score-bars">
      <div class="score-metric">
        <div class="score-metric__head"><span>Acierto al decidir (cobertura 0,00 %)</span><strong>no aplica</strong></div>
        <div class="bar-track"><div class="bar-fill" style="width:0%;"></div></div>
      </div>
      <div class="score-metric">
        <div class="score-metric__head"><span>Exactitud 3-clases (40/160 aciertos gratis)</span><strong>25,00 %</strong></div>
        <div class="bar-track"><div class="bar-fill bar-fill--cyan" style="width:25.0%;"></div></div>
      </div>
    </div>
  </div>
</div>

---

## Cierre de investigación: qué modelo libre sí corre en milisegundos en mi i7-8550U

¿Cuándo tendría sentido armar un comité de clasificadores tipo JEV? Cuando cada juez supere el `50 %` de acierto en cada clase sobre datos fuera de muestra (Condorcet 1785), cuando sus errores estén desacoplados (Dietterich 2000), cuando sus probabilidades estén calibradas (Guo et al. 2017) y cuando al menos dos jueces tengan sensibilidad real para votar `"No"`. Juntar en CPU a un juez que aprueba casi todo, otro que rechaza casi todo y un tercero que casi no habla no produce sabiduría colectiva: produce abstención cara. Por eso retiré el prototipo.

Pero retirar ese comité deja abierta la pregunta práctica: **¿existe hoy un modelo local, 100 % libre y gratuito, que sí pueda decidir compuertas de tres clases (`"Sí"`, `"No"`, `"Indefinido"`) en milisegundos sobre un `Intel Core i7-8550U` sin GPU?** Sí existe, siempre que cambie de familia arquitectónica y deje de tratar una verificación lógica como si fuera un problema de generación de texto.

Cuando una compuerta evalúa si una evidencia observada respalda, contradice o resulta insuficiente frente a una regla, el problema formal no es *causal language modeling*, sino **inferencia de lenguaje natural (*Natural Language Inference*, NLI)** de tres clases: *entailment* (`"Sí"`), *contradiction* (`"No"`) y *neutral* (`"Indefinido"`). En esa categoría, el modelo abierto que mejor equilibra precisión y velocidad en una CPU portátil con `AVX2` es **[`MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli`](https://huggingface.co/MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli)** (Laurer et al. 2024), basado en la arquitectura **DeBERTaV3** (He, Gao y Chen 2023) y compilado a **ONNX INT8** mediante [`optimum`](https://github.com/huggingface/optimum) y [`onnxruntime`](https://onnxruntime.ai/):

<div class="nli-solution-card" role="region" aria-label="Ficha técnica del modelo libre recomendado para CPU: MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli en ONNX INT8">
  <div class="nli-solution-card__top">
    <h3 class="nli-solution-card__title">✅ Alternativa viable en CPU: DeBERTa-v3-small-mnli-fever-anli (ONNX INT8)</h3>
    <div class="jev-chips">
      <a class="jev-chip" href="https://huggingface.co/MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli" target="_blank" rel="noopener">HF Model (MIT)</a>
      <a class="jev-chip jev-chip--amber" href="https://arxiv.org/abs/2111.09543" target="_blank" rel="noopener">Paper DeBERTaV3</a>
      <a class="jev-chip" href="https://onnxruntime.ai/" target="_blank" rel="noopener">ONNX Runtime</a>
    </div>
  </div>
  <p class="nli-solution-card__desc">
    <em>Cross-encoder</em> bidireccional con <strong>atención desenredada</strong> (<em>disentangled attention</em>, que separa contenido y posición relativa) entrenado mediante <em>replaced token detection</em> (ELECTRA) y ajustado sobre <strong>763.913 pares NLI</strong> (<code>MultiNLI</code> + <code>FEVER-NLI</code> + <code>ANLI</code> R1–R3). Evalúa premisa e hipótesis juntas en una sola pasada hacia adelante sin cargar PyTorch.
  </p>
  <div class="nli-solution-card__grid">
    <div class="nli-solution-card__metric">
      <strong>5 a 15 ms por veredicto</strong>
      En un procesador portátil con <code>AVX2</code> sobre <code>onnxruntime</code> (<code>INT8</code> dinámico), frente a los <code>366–1.717 ms</code> en caliente y <code>~31,7 s</code> en frío del comité.
    </div>
    <div class="nli-solution-card__metric">
      <strong>~140 MiB en disco y RAM</strong>
      <code>44M</code> de parámetros en el <em>backbone</em> (<code>142M</code> totales con vocabulario), casi <code>60 veces</code> más liviano que los <code>8,36 GiB</code> que ocupaban los tres jueces.
    </div>
    <div class="nli-solution-card__metric">
      <strong>3 clases nativas ("Sí" / "No" / "Indefinido")</strong>
      Emite logits directos para <code>entailment</code>, <code>contradiction</code> (<code>88,0 %</code> en MNLI-m) y <code>neutral</code>, eliminando de raíz la ceguera al <code>"No"</code> (<code>0/60</code>).
    </div>
  </div>
</div>

La lección que me llevo de esta prueba de concepto es simple: en un portátil de trabajo sin aceleradora dedicada, **un único *cross-encoder* NLI pequeño, bien calibrado y compilado a ONNX INT8 supera en velocidad, huella de memoria y sensibilidad para decir `"No"` a cualquier comité de modelos mal acoplados**. Cuando la verificación es determinista (un hash, un esquema JSON o un código de salida), una regla de código en `0 ms` sigue siendo imbatible; y cuando realmente hace falta juzgar implicación o contradicción semántica en local, la respuesta no estaba en sumar tres jueces en serie, sino en elegir la arquitectura correcta para una CPU.

---

## Referencias

<div class="post-references" markdown="1">

- Arc53. 2025. *"arc-decide-0.4b-v0.2: Compact ONNX Decision Classifier"*. Repositorio de modelo en Hugging Face. [https://huggingface.co/Arc53/arc-decide-0.4b-v0.2](https://huggingface.co/Arc53/arc-decide-0.4b-v0.2).
- Browser Use y TypeSafe AI. 2026. *"JEV Ultrafast: Sub-Second Browser Agent Actions with Jev Decision Models"*. Repositorio oficial en GitHub. [https://github.com/browser-use/jev-ultrafast](https://github.com/browser-use/jev-ultrafast).
- Condorcet, Jean-Antoine-Nicolas de Caritat, Marqués de. 1785. [*Essai sur l'application de l'analyse à la probabilité des décisions rendues à la pluralité des voix*](https://gallica.bnf.fr/ark:/12148/bpt6k417181). París: Imprimerie Royale.
- Dietterich, Thomas G. 2000. ["Ensemble Methods in Machine Learning"](https://doi.org/10.1007/3-540-45014-9_1). En *Multiple Classifier Systems (MCS 2000)*, Lecture Notes in Computer Science, vol. 1857, 1–15. Berlín: Springer.
- Guo, Chuan, Geoff Pleiss, Yu Sun y Kilian Q. Weinberger. 2017. ["On Calibration of Modern Neural Networks"](https://proceedings.mlr.press/v70/guo17a.html). En *Proceedings of the 34th International Conference on Machine Learning (ICML)*, PMLR 70: 1321–1330.
- He, Pengcheng, Jianfeng Gao y Weizhu Chen. 2023. ["DeBERTaV3: Improving DeBERTa using ELECTRA-Style Pre-Training with Gradient-Disentangled Embedding Sharing"](https://arxiv.org/abs/2111.09543). En *International Conference on Learning Representations (ICLR 2023)*.
- Laurer, Moritz, Wouter van Atteveldt, Andreu Casas y Kasper Welbers. 2024. ["Less Annotating, More Classifying: Addressing the Data Scarcity Issue of Supervised Machine Learning with Deep Transfer Learning and BERT-NLI"](https://doi.org/10.1017/pan.2023.20). *Political Analysis* 32 (1): 84–100. Modelo: [https://huggingface.co/MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli](https://huggingface.co/MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli).
- NandhaKishorM (ConvAI Innovations). 2026a. *"Laya: System 1 Non-Autoregressive Multilingual Decision Engine"*. Repositorio en GitHub. [https://github.com/NandhaKishorM/laya](https://github.com/NandhaKishorM/laya).
- NandhaKishorM. 2026b. *"VegaML: Potential-Well Physics Decision Engine over Frozen Language Backbones"*. Repositorio en GitHub. [https://github.com/NandhaKishorM/vegaml](https://github.com/NandhaKishorM/vegaml).

</div>
