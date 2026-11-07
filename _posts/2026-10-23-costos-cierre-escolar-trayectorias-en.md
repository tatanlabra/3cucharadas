---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extending my thesis in three spoonfuls (part III): what student trajectories show after a school closure"
subtitle: "In all 19 measurable cohorts, the point estimate of grade lag or exit from the register was higher among students who lost their school than among their peers. I cannot yet attribute that gap to the closure."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-11-06 09:00:00 -0300
categories: [data, education, public-policy]
tags: [education, school-closure, trajectories, causality, mineduc, administrative-data, duckdb, public-policy]
description: "Student trajectories and school closures in Chile: post-pilot results, causal limits, and minimum conditions for a responsible school transition."
excerpt: "Across every measurable cohort the progression gap is positive; in the primary window the missing-data bounds span both signs. The evidence can inform transitions, but cannot yet attribute harm or benefit to closure."
author: clabra
lang: en
ref: costos-cierre-escolar-trayectorias
permalink: /datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/
header:
  teaser: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/og-1200x630.webp
  og_image_alt: "Students and desks follow branching paths from a closed school towards different schools, as a metaphor for an uncertain educational transition."
  overlay_image: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/costos-cierre-escolar-trayectorias/teaser-mobile-640x360.webp
visual_id: costos-cierre-escolar-trayectorias
editorial_contract: societal-contribution-v1
table_contract: explicit-v1
math: true
toc: true
toc_sticky: true
comments: true
author_profile: true
distribution:
  social: true
  republish: []
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
---

When a school closes, finding another school on a map does not settle the public question. What matters is whether its students stayed enrolled, moved up to the expected grade, and sustained regular attendance. Above all, it matters to separate how much of any later setback comes from the closure itself and how much was already unfolding beforehand.
{: .text-justify}

To answer it, I reconstructed twenty years of school history across **79,709,054 enrolment records** and **73,873,835 performance records** from 2004 to 2025, following **78,972 student trajectories** in **1,141 regular schools** that closed between 2005 and 2024 against **734,472 controls** from schools that stayed open. The long window supports two readings that are worth holding together. First: across all **19 estimable annual cohorts** (2006–2024), the point estimate of the **share with no enrolment or enrolment below the expected grade one year later—what I call “progression failure or grade lag”—** rose more among students who lost their school than among their peers, and that gap is positive in all 19 (ranging from **+0.94 to +28.22 percentage points**, with a median of **+7.18**). Aggregating the full series weighted by exposed students (Callaway and Sant'Anna) yields a mean gap of **+9.11 percentage points** (95% confidence interval from **+5.34 to +12.88** and worst-case missing-data bounds from **+0.43 to +16.21 points**, which stay above zero), alongside **+6.29 points** under a random-effects model (**+4.49 to +8.09**, I² = 76.5%) and, under the same exposed-weighted scheme, **+1.38 points** in two-year persistent non-enrolment. Second: I still cannot attribute that gap to the closure on its own, because those schools were already institutionally more fragile and nearly half of their students were already switching schools before the event.
{: .text-justify}

Dividing the two decades into their **five institutional stages** reveals a structural pattern that a short window cannot show: closure volume is concentrated in the first half of the series, and the size of the progression gap attenuates thereafter. In **2005–2010** (LOCE regime and early SEP rollout; **521 closures** and **36,984 exposed students**), progression failure or grade lag rose **+12.15 percentage points**—the only regime where both the confidence interval (**+3.78 to +20.52**) and the worst-case missing-data bounds (**+3.49 to +18.83**) exclude zero at the same time—and two-year non-enrolment rose **+1.21 points**. In **2011–2015** (rollout of the General Education Law and the Quality Assurance System; **502 closures** and **31,512 exposed students**), the progression gap was **+7.82 points** and two-year persistent non-enrolment reached its series peak of **+1.85 points**: together, those first two stages account for **89.7% of regular closures** and **86.7% of exposed students** across the entire twenty-year series. The progression gap then falls to **+5.29 points** in **2016–2019** (gradual implementation of the Inclusion Law; **63 closures** and **6,190 exposed students**, with bounds from **−1.15 to 10.98 points**), **+2.70 points** in **2020–2022** (pandemic and flexible promotion; **33 closures** and **3,272 exposed students**), and **+2.59 points** in **2023–2024** (post-pandemic reactivation; **22 closures** and **1,014 exposed students**).
{: .text-justify}

Seen against that twenty-year series, the **2016–2019** subwindow—the cut I fixed as the primary window before examining the full series, whose figures come from the **post-pilot re-estimation**, that is, from re-estimating with the design already locked what an exploratory pilot had first probed—accounts for just **5.5% of supported closures** (63 of 1,141) and **7.8% of exposed students** (6,190 of 78,972), and because a few closures hold a large share of students, it weighs statistically as much as about **21 or 22 independent schools**. In that recent zoom, progression failure or grade lag rose **5.29 percentage points** more among exposed students than in the comparison group (conservative 95% confidence interval from **2.08 to 8.51 points**; the rate went from 2.2% to 15.8% when controls implied 10.6%), yet assumption-free missing-data bounds (Manski 2003[^manski2003]) span **−1.15 to 10.98 percentage points**. Because that range crosses zero, the 2016–2019 subwindow provides **partial, inconclusive evidence** on its own: it demonstrates neither harm, benefit, nor the absence of an effect, but serves as a demanding laboratory for stress-testing pre-trends, record coverage, and receiving-school quality without manufacturing the counterfactual of what would have happened to those same children and adolescents had their school stayed open.
{: .text-justify}

<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->
<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->

[Part I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) reconstructed the historical evidence and separated the findings that held up. [Part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) verified which schools closed in the recent decade and showed that the nearest school is rarely the main destination. This third instalment shifts from buildings to student trajectories in three steps: **what actually closed across twenty years**, **what happened next to students in the full series and its five stages**, and **how to protect a school transition in practice**.
{: .text-justify}

**Quick guide.** I call **G** the first year in which the school has no enrolment; **G−1** is its last open year and **G+1** the following one. For grade progression, “before” is measured two years before closure (G−2) and “after” at G+1. **pp** are percentage points; **RBD** is each school's code; **SEP**, the Preferential School Subsidy; **JEC**, the Full School Day; **RCID**, the closure rule I built from the data. **Manski bounds** (or missing-data bounds) are the range that would still be possible if every student without a record had fared either worst or best: when that range crosses zero, the missing records alone are enough to flip the sign of the result.
{: .notice--info .text-justify}

## Spoonful 1: what closed, and who was exposed across twenty years?

### Twenty years of closures under three successive sieves (RCID v1, 2005–2025)

In Chile, the legal closure of a school requires an exempt resolution from the regional education secretariat, but no complete public registry of those resolutions exists: I checked in Active Transparency (details in the methodological notes at the end). So I built an empirical, falsifiable rule, the **Data-Inferred School Closure Rule (RCID v1)**, which works like three successive sieves (**D0 ⊃ D1 ⊃ D2**) across twenty years of administrative data. The first (**D0**) detects enrolment that disappears; the second (**D1**) discards annexes and code changes; the third (**D2**) sets aside block transfers into a single school. Put simply, an entire class moving together into another building is not the same experience as families searching for places one by one.
{: .text-justify}

{: .table-caption}
**Table 1.** Hierarchy of the Data-Inferred School Closure Rule (RCID v1, D0 ⊃ D1 ⊃ D2) across all three instalments (2005–2025)

| Rule stratum | Historical window (2005–2015) | Recent window (2016–2025) | Longitudinal series (2005–2025) | What it purges and how it is used in Parts I, II, and III |
|---|---:|---:|---:|---|
| D0: raw administrative or activity exit | 1,635 | 346 | 1,981 | Enrolment cessation in t; contrasts with the 2,069 raw directory exits of 1992–2012 in Part I. |
| D1: strict closure of educational provision | 1,477 | 330 | 1,807 | Purges 158 historical annexes, sites, or RBD successors and 16 recent directory continuities (Part II baseline). |
| D2 = RCID v1 (conservative, includes right-censored 2025) | 1,382 | 296 | 1,678 | Further purges 95 historical absorptions and 34 recent concentrated absorptions or flow alerts (≥ 10 baseline and assigned students, ≥ 70% to the main destination, and HHI ≥ 0.50). |
| D2 = RCID v1 (clean with observed t+1 window) | 1,382 | 266 | 1,648 | Requires observing the full t+1 year (excludes the 30 right-censored 2025 episodes); main baseline for Part III. |
{: .table--compact .table--scroll}

As Table 1 shows, applying RCID v1 (D2) leaves **1,648 clean closures** with an observed post-closure year across 2005–2025—**1,382** in the 2005–2015 historical window and **266** in the 2016–2024 recent window—providing a consistent starting point that avoids conflating de facto mergers with dispersed closures. Not all of those closures can be followed through grade trajectories: only **1,177** had students in regular education (grades 1 to 8 of primary or 1 to 3 of secondary) and **1,141** found comparable controls (**78,972 exposed students** and **734,472 controls**). In the recent window, **145 of the 266** closures were schools offering only early-childhood education (69), only special education (57), only adult education (13), or only the final secondary grade (1), or were dominated by those offerings (5). Grade progression cannot be measured there, so this instalment speaks to regular schools, not to every closure.
{: .text-justify}

### A student flow is a signal, not an administrative act: the 2016–2025 cut

In the recent period (2016–2025), **346 episodes** appear in administrative records as schools with prior enrolment ceasing operation. After setting aside annexes, administrative changes, and likely continuities, [Part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) identified **330 strict closures** (D1) of educational provision. Tracking their students the following year reveals when nearly an entire student body moves together to a single receiving school: that pattern can reflect a merger, a code change, or simply an accessible nearby school, but student flow alone never replaces a formal administrative act.
{: .text-justify}

{: .table-caption}
**Table 2.** Diagnostic reading of the 346 episodes recorded as closures in the recent period (2016–2025)

| Status | Episodes | Supported interpretation |
|---|---:|---|
| No contradictory signal | 266 | The trajectory does not contradict a strict closure; it is not external corroboration. |
| Continuity candidate | 15 | Name, level or form of provision, or later activity warrants documentary review. |
| Unresolved alert | 35 | The category remains unchanged until independent evidence is available. |
| Incomplete follow-up | 30 | These closures occurred in 2025, so the following year is not yet observed. |
{: .table--compact .table--scroll}

Each of the 346 episodes appears once in Table 2. The **45 concentrated-destination alerts** come from a cross-cutting flow check that overlaps those categories and must not be added to them; without **independent institutional confirmations** (**zero** in this cut), the 330 strict closures remain the baseline reference for Part II, whereas this instalment builds on the D2 closures in Table 1.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-1-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/sample-flow-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/sample-flow-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-en-dark.svg' | relative_url }} 1600w" alt="Two lanes summarise support for the 2016 to 2019 post-pilot re-estimation. Of 64 historical episodes before support screening, 63 retain at least one comparable stratum and one is fully excluded. Of 6,581 exposed student-cohort observations, 391 are excluded and 6,190 remain. The support universe contains 82,753 control student-cohort observations; final samples differ by outcome." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 1</strong> — How the comparable sample is formed in the pre-registered zoom (2016–2019). Aggregate counts precede outcome-specific eligibility, and their units must not be added together. <span class="figure-source">Source: author’s calculations from the post-pilot re-estimation.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/sample-flow-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

Figure 1 distinguishes between closed schools (episodes) and “student-cohort” observations (each student counted within their closure cohort). All published information is strictly aggregated: to protect privacy, no names, addresses, or individual student or school codes are exposed.
{: .text-justify}

### Who the exposed students were

Before looking at what happened to them, it helps to know who they were. Table 3 summarises eight characteristics of children and adolescents and their origin schools, measured one year before closure (G−1); only the last row looks further back, from G−3, to capture prior school switching.
{: .text-justify}

{: .table-caption}
**Table 3.** Extended baseline characterisation of children and adolescents at G−1 (2016–2019 cohorts, 6,190 exposed and 82,753 controls)

| Baseline descriptor at G−1 | Exposed students | Comparison group | Gap (pp) | Substantive reading for identification |
|---|---:|---:|---:|---|
| Priority SEP student | 30.68% | 32.32% | −1.64 | Close balance in priority socioeconomic vulnerability after matching. |
| Total SEP eligibility (priority or preferential) | 54.51% | 55.58% | −1.07 | Similar composition on this binary vulnerability measure. |
| Effective SEP beneficiary | 37.63% | 48.58% | −10.95 | Consistent with the origin school's lower SEP agreement coverage (next row). |
| Origin school with SEP agreement | 45.17% | 55.23% | −10.06 | Closures cluster among providers with lower institutional SEP participation. |
| Origin school with Full School Day (JEC) | 53.97% | 72.51% | −18.54 | Lower full-day provision in schools that subsequently close. |
| Inter-municipality commuting (residence ≠ school municipality) | 38.59% | 29.99% | +8.60 | Higher share of children and adolescents already commuting outside their home municipality before closure. |
| Over-age ≥ 1 year relative to grade norm | 33.86% | 33.86% | 0.00 | Exact balance by construction of the G−1 matching strata. |
| At least one school switch between G−3 and G−1 | 47.04% | 30.52% | +16.52 | Nearly half of exposed students were already switching schools before closure. |
{: .table--compact .table--scroll}

The profile in Table 3 explains why caution is essential across both the long series and the recent cut: exposed students and their controls share the same age, the same prior grade lag (33.86%), and nearly identical individual eligibility for the Preferential School Subsidy (54.51% versus 55.58%, with **30.68%** priority students), yet they attended institutionally weaker schools—with lower SEP agreement coverage (−10.06 pp) and lower Full School Day coverage (−18.54 pp)—and nearly half (**47.04%** versus 30.52%) had already switched schools during the two preceding years. Part of the school disengagement and family mobility was already under way before closure. Moreover, I count as exposed only students still enrolled at G−1: if better-resourced families left before closure, the exposed group is already selected.
{: .text-justify}

## Spoonful 2: what happened after closure in the grand window and its five stages?

### The full 2005–2024 series and its five institutional stages

The empirical core of this instalment lies in the twenty annual cohorts from **2005 to 2024**. When schools close in different years, blending them into a simple average would mistakenly use recently closed schools as if they were stable controls for later closures. Modern **staggered difference-in-differences** estimators (Callaway and Sant'Anna 2021[^callaway2021]; Sun and Abraham 2021[^sun2021]; Roth et al. 2023[^roth2023]) avoid that distortion by comparing each annual cohort solely against schools that have not yet closed. Here I also compute missing-data bounds (Manski 2003[^manski2003]) and assess sensitivity to non-parallel pre-trends with a simplified version of the approach in Rambachan and Roth (2023[^rambachan2023]). Under the RCID v1 (D2) rule, the full series spans **20 annual cohorts**, **1,141 empirically supported episodes**, **78,972 exposed observations**, and **734,472 controls**. Of those 20 cohorts, 19 are estimable for progression and 17 for persistent non-enrolment: the cohorts at the edge of the 2004–2025 panel lack either the “before” year (G−2) or the second “after” year within the data. The year-by-year breakdown is available in the [open CSV for Figure 2]({{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}), and Table 4 summarises the five institutional periods, the annual range, and three distinct ways of pooling the two decades.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-2-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }} 1600w" alt="Three-panel infographic under the RCID v1 rule with 1,141 supported episodes between 2005 and 2024. Panel A displays the 19 estimable annual cohorts for progression failure or grade lag from 2006 to 2024: all 19 point estimates are positive, ranging from 0.94 to 28.22 percentage points, with a median of 7.18 and a Callaway and Sant'Anna student-weighted aggregate of +9.11 points (interval from 5.34 to 12.88 and Manski bounds from +0.43 to +16.21 points). Panel B shows attenuation across institutional regimes from 12.15 points in 2005–2010 and 7.82 in 2011–2015 to 5.29 in 2016–2019 (with missing-data bounds from minus 1.15 to 10.98 points), 2.70 in 2020–2022, and 2.59 in 2023–2024. Panel C shows G minus 1 baseline gaps after exact matching: individual SEP eligibility is balanced (−1.07 points), whereas exposed students face lower school SEP agreements (−10.06 points), lower full-day schooling (−18.54 points), lower valid record coverage (−19.24 points), and higher prior school switching (+16.52 points)." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 2</strong> — Full 2005–2024 series under the RCID v1 rule: annual estimates (2006–2024), attenuation across the five institutional stages, and baseline gaps among children and adolescents at G−1. <span class="figure-source">Source: author’s calculations from the 2004–2025 MINEDUC longitudinal panel.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

{: .table-caption}
**Table 4.** Summary of the full 2005–2024 series by institutional regime, annual range, and aggregation scheme (RCID v1)

| Institutional regime / Range / Aggregate | Supported episodes | Exposed (N) | Controls (N) | Progression failure or grade lag (pp) | 95% CI progression (pp) | Manski bounds progression (pp) | 2-year persistent non-enrolment (pp) | 95% CI non-enrolment (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Sub-aggregate 2005–2010 (LOCE regime and early SEP) | 521 | 36,984 | 334,062 | +12.15 | [+3.78, +20.52] | [+3.49, +18.83] | +1.21 | [+0.53, +1.90] |
| Sub-aggregate 2011–2015 (LGE and SAC rollout) | 502 | 31,512 | 260,740 | +7.82 | [+6.20, +9.41] | [−2.11, +16.18] | +1.85 | [+1.10, +2.59] |
| Sub-aggregate 2016–2019 (main window; bounds [−1.15, 10.98] pp) | 63 | 6,190 | 82,753 | +5.29 | [+2.08, +8.51] | [−1.15, +10.98] | +0.63 | [−0.77, +2.03] |
| Sub-aggregate 2020–2022 (COVID-19 pandemic and flexible promotion) | 33 | 3,272 | 42,457 | +2.70 | [−0.63, +6.03] | [+0.18, +4.95] | −0.28 | [−1.37, +0.81] |
| Sub-aggregate 2023–2024 (post-pandemic reactivation; 2024 censored at 2 years) | 22 | 1,014 | 14,460 | +2.59 | [−1.55, +6.73] | [−1.70, +6.07] | −0.93 | [−2.64, +0.78] |
| **Annual range (19 cohorts in progression; 17 in non-enrolment)** | **7 to 129** | **357 to 10,261** | **5,566 to 71,248** | **+0.94 to +28.22 (median: +7.18)** | **IQR: +3.15 to +9.62** | **—** | **−0.93 to +4.56 (median: +0.92)** | **IQR: +0.22 to +2.11** |
| **Full-series aggregate 2005–2024 (Callaway & Sant'Anna, exposed-weighted)** | **1,141** | **78,972** | **734,472** | **+9.11** | **[+5.34, +12.88]** | **[+0.43, +16.21]** | **+1.38** | **[+0.92, +1.85]** |
| **Full-series aggregate 2005–2024 (equal annual cohort weights)** | **1,141** | **78,972** | **734,472** | **+7.55** | **[+5.52, +9.57]** | **—** | **+1.03** | **[+0.56, +1.50]** |
| **Full-series aggregate 2005–2024 (random effects; I² = 76.5%, τ = 2.81 pp)** | **1,141** | **78,972** | **734,472** | **+6.29** | **[+4.49, +8.09]; prediction [+0.09, +12.49]** | **—** | **+0.79** | **[+0.16, +1.42]; prediction [−1.34, +2.92]** |
{: .table--compact .table--scroll}

The N columns in Table 4 refer to support; each estimate uses the subset with an observable outcome (for example, 4,815 exposed students for progression in 2016–2019). The Manski bounds do not include sampling error. The random-effects aggregate (Paule-Mandel, with a Hartung-Knapp interval) replaces the inverse-variance one in the previous version, which assumed a single effect common to all cohorts and, with 76.5% heterogeneity, produced an artificially narrow interval. Because cohorts share controls, even these intervals may be somewhat short.
{: .text-justify}

The twenty-year series and its five institutional divisions (Figure 2 and Table 4) deliver four main takeaways:
{: .text-justify}

- **Across the full series, all 19 estimable progression cohorts are positive, and the aggregate stays above zero under all three pooling schemes, though with substantial heterogeneity across periods:** weighting years by the number of affected students (Callaway and Sant'Anna) gives a mean difference of **+9.11 percentage points** ([+5.34, +12.88]), whose Manski bounds (**+0.43 to +16.21**) stay above zero, alongside **+1.38 points** ([+0.92, +1.85]) in two-year persistent non-enrolment. With equal weight for each annual cohort it is **+7.55 points** ([+5.52, +9.57]) in progression and **+1.03 points** ([+0.56, +1.50]) in non-enrolment. Under a random-effects model (I² = 76.5%, τ = 2.81 pp), the mean is **+6.29 points** ([+4.49, +8.09]), with a prediction interval of **+0.09 to +12.49 points** indicating where a new cohort's gap could fall.
- **2005–2010 (LOCE regime and early SEP) and 2011–2015 (LGE and SAC rollout) account for nearly nine in ten closures and the largest gaps:** in **2005–2010** (**521 episodes**, **36,984 exposed students**, and **334,062 controls**), progression failure rose **+12.15 percentage points** ([+3.78, +20.52]), and both its confidence interval and its Manski bounds (**+3.49 to +18.83**) exclude zero at the same time, while two-year non-enrolment rose **+1.21 points** ([+0.53, +1.90]). In **2011–2015** (**502 episodes**, **31,512 exposed students**, and **260,740 controls**), the progression gap was **+7.82 points** ([+6.20, +9.41]; bounds [−2.11, +16.18]) and two-year persistent non-enrolment reached its series-wide peak at **+1.85 percentage points** ([+1.10, +2.59]). Together, those first two stages encompass **1,023 of the 1,141 closures** (89.7%) and **68,496 of the 78,972 exposed students** (86.7%).
- **From 2016 onward, closure volume drops sharply and the progression gap attenuates across the three recent stages:** in **2016–2019** (gradual implementation of the Inclusion Law; **63 episodes** and **6,190 exposed students**), the gap falls to **+5.29 percentage points** ([+2.08, +8.51], with bounds from **−1.15 to 10.98 points**) and **+0.63 points** in non-enrolment. In **2020–2022** (COVID-19 pandemic and flexible promotion; **33 episodes** and **3,272 exposed students**), it compresses to **+2.70 points** ([−0.63, +6.03]; bounds [+0.18, +4.95]) and **−0.28 points** in non-enrolment. And in **2023–2024** (post-pandemic reactivation; **22 episodes** and **1,014 exposed students**), it stands at **+2.59 points** ([−1.55, +6.73]; bounds [−1.70, +6.07]) and **−0.93 points** in non-enrolment.
- **Attenuation across regimes is a robust descriptive fact, not the isolated effect of a single statute:** that decline coincides in time with the Preferential School Subsidy (SEP), the Quality Assurance System (SAC), and the Inclusion Law, but cannot be attributed directly to them because the kind of schools that close also changed, the way the directory recorded school status changed in 2015, flexible promotion in 2020–2022 mechanically reduces grade lag, and recent samples are much smaller.

### The pre-registered 2016–2019 zoom: partial evidence and two primary outcomes

Against that twenty-year backdrop, the **2016–2019** window takes on its proper meaning: it was the cut I pre-registered before estimating the long series because the official directory standardised operating status from 2015 onward, it allowed multi-year pre-trends inside a panel starting in 2004, and it avoided the 2020–2022 pandemic disruption. Yet because it captures only **63 of the 1,141 supported episodes** (5.5% of the series, of which **62 episodes** have an observable follow-up window for the two primary outcomes and **58** for attendance and marks), its estimates must be read as **partial evidence**.
{: .text-justify}

In this 2016–2019 zoom, the first primary outcome tracks the share of students with **no enrolment record for two consecutive years**: I do not call this “dropout” because disappearing from Chile’s administrative register does not clarify whether a student left schooling altogether, moved abroad, or entered an uncovered modality. Here the exposed group’s before-and-after change exceeds the comparison group’s by **+0.63 percentage points**, with a conservative 95% confidence interval from **−0.77 to 2.03 points** (across **3,666** exposed observations and **49,944** controls).
{: .text-justify}

The second primary outcome measures the share with **no enrolment or enrolment below the expected grade one year later**, summarised as **progression failure or grade lag**. In 2016–2019 the before-and-after gap rises by **+5.29 percentage points** among exposed students relative to controls (conservative interval from **2.08 to 8.51 points**, across **4,815** exposed observations and **65,538** controls). Yet the record is missing for **3.60%** of exposed students and **2.15%** of controls, and **Manski bounds** (Manski 2003[^manski2003]) span **−1.15 to 10.98 percentage points**—a no-optimism stress test that assigns the worst outcome to students without a record in one group and the best in the other, and then the reverse. On its own, this subperiod result is therefore **inconclusive**: among exposed students, progression failure rises from **2.2%** two years before closure to **15.8%** the year after versus **10.6%** implied by controls (**50%** above that counterfactual and, only if causal, about **255 students**), without separating register exit from grade repetition. Within this subwindow, the bounds exclude zero only in closures with at least 90% valid records in the prior year (38% of exposed students).
{: .text-justify}

{: .table-caption}
**Table 5.** Post-pilot re-estimation in the pre-registered zoom (2016–2019): observed differences, not causal effects

| Outcome | Estimated difference | Conservative 95% interval | Decisive condition |
|---|---:|---:|---|
| Persistent non-enrolment for two years | +0.63 pp | [−0.77, 2.03] | It is not dropout; the estimable pre-event trend rests on few episodes. |
| Progression failure or grade lag: no enrolment or below the expected grade one year later | +5.29 pp | [2.08, 8.51] | Missing-data bounds: [−1.15, 10.98] pp overall; [0.09, 7.84] pp in closures with ≥ 90% valid records at G−1 (38% of exposed students). No sampling error. |
| Attendance | −1.15 points | [−2.40, 0.10] | Exploratory and conditional; requires valid attendance and observable final pass/repeat status. |
| Average mark | −0.06 | [−0.14, 0.01] | Exploratory and conditional; only among students with observable performance. |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-3-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }} 1600w" alt="Inconclusive post-pilot re-estimation of two primary outcomes. Persistent non-enrolment is estimated at 0.63 percentage points, with a CI from minus 0.77 to 2.03; the different sample that includes receiver schools gives 0.71, from minus 0.69 to 2.12. Progression failure or grade lag is estimated at 5.29 points, from 2.08 to 8.51; the different receiver-school sample gives 5.09, from 1.94 to 8.23. Missing-data bounds span minus 1.15 to 10.98 points. These are not confirmed causal effects." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 3</strong> — Pre-registered 2016–2019 zoom: inconclusive post-pilot re-estimation, not causal effects. The progression interval does not cross zero, but its missing-data bounds do; overlap with the pilot and unobserved assumptions prevent a causal interpretation. <span class="figure-source">Source: author’s calculations from the post-pilot re-estimation.</span> <span class="figure-data">Accessible tabular data: <a href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-data.csv' | relative_url }}">estimates</a> and <a href="{{ '/assets/images/tesis-post3/missingness-bounds-data.csv' | relative_url }}">missing-data bounds</a>.</span></figcaption>
</figure>

Attendance and average marks in Table 5 are **exploratory and conditional**: they can be measured only among students with valid annual performance records in both periods. That leaves **3,871** exposed observations across **58 episodes**, **62.5%** of exposed support, against **63,591** of the **82,753** controls for attendance (63,596 for marks). In Figure 3, the alternative bar that keeps receiving schools inside the control group yields **+0.71 percentage points** in non-enrolment ([−0.69, 2.12], across 3,670 exposed and 59,613 controls) and **+5.09 points** in progression failure ([1.94, 8.23], across 4,822 exposed and 79,058 controls): changing which schools enter the control pool alters sample composition, but does not remove the **−1.15 to 10.98 point** bounds attached to the main +5.29 pp estimate.
{: .text-justify}

The effective sample size of this subwindow is best pictured as a **meeting room**. Even though 62 closed schools enter the 2016–2019 estimation, a handful of large closures account for a disproportionate share of students. Listening to those 62 closures is therefore less like hearing 62 independent voices at equal volume and more like hearing **21.1 effective episodes** for non-enrolment, **21.9** for progression, and just **17.7** for attendance and marks. Likewise, splitting urban and rural closures rests on even fewer rural episodes, so territorial recommendations must wait for road-network travel times and school-transport data.
{: .text-justify}

### Is like being compared with like? Pre-trends and record coverage

Across both the long series and the 2016–2019 zoom, the design uses **difference-in-differences**, which compares two films rather than two isolated snapshots: first it pairs each student from a school that will close with control students who are identical one year before closure (G−1) in calendar year, sex, age, region, provider type, rurality, education level, and grade, and then it measures how much the first group’s trajectory changed before and after the event relative to their matched peers. Put simply, I try to compare like with like across every characteristic recorded in the data, gauging closeness through the **standardised difference** (distance measured in units of spread where zero means equality).
{: .text-justify}

On what can be observed, the groups end up nearly identical in age, attendance, and marks, with standardised differences below 0.08. But exposed students have far fewer valid annual records in the year before closure: 76.8% versus 96.2%. At the same time, three pre-closure placebo tests in 2016–2019 give differences of +0.16, +0.30, and +0.40 points in progression: the interval around the +5.29-point estimate (with bounds from −1.15 to 10.98 points) stops excluding zero if post-closure bias reaches 2.07 points, about 2.54 times the 95% upper bound of the largest placebo (0.81 points), without combining that calculation with the missing-data bounds. And separating stayers enrolled in the same school between G−2 and G−1—3,556, or 77.5% of exposed students with a grade observed at G−2 and G−1 (70.6% of all exposed)—from late entrants (1,033), progression failure rises **+3.87 percentage points** ([+1.04, +6.69]) among stayers and **+9.58 points** ([+5.06, +14.10]) among late entrants: about three-quarters of the gap remains among students who had been in the school for at least two years.
{: .text-justify}

<aside class="notice--info" markdown="1">
**Methodological note — What changes with prior-year record coverage and how much bias would nullify the interval:** Manski's (2003[^manski2003]) worst-case bounds assume nothing about students without a record, so their width depends on how many are missing. Article 27 of Supreme Decree No. 315 requires the provider to submit promotion records before the regional secretariat rules on the closure; I do not observe that submission, only the share of students with a valid record in the panel. In 2016–2019 closures where that share reaches 90% (1,822 exposed students with an outcome), missingness nearly equalises across groups (2.31% versus 2.15%), the difference is +4.26 points, and the bounds run from +0.09 to +7.84 points; dropping only closures with fewer than half their records still leaves bounds from −0.90 to +12.18 points. Meanwhile, the 2.07-point post-closure bias threshold (2.54 times the 0.81-point 95% upper bound of the largest placebo) applies a linear, simplified version of the idea in Rambachan and Roth (2023[^rambachan2023]), not their formal estimator, and neither test simultaneously incorporates sampling error in the bounds.
</aside>

### What the literature adds—and what it does not

Much of the international evidence suggests that the impact of closing a school depends jointly on the transition process and on the quality of the receiving school: students often experience losses during the announcement and first post-closure year, followed by partial recovery when they transfer to higher-value-added schools, but lasting setbacks in attendance or secondary graduation when relocated into congested or similarly weak schools (Engberg et al. 2012[^engberg2012]; Brummet 2014[^brummet2014]; Beuchert et al. 2018[^beuchert2018]; Steinberg and MacDonald 2019[^steinberg2019]; Larsen 2020[^larsen2020]; Taghizadeh 2020[^taghizadeh2020]; Bross, Harris, and Liu 2023[^bross2023]; Kim 2024[^kim2024]), in line with the literature on school assignment and destination-school quality (Abdulkadiroğlu, Pathak, and Walters 2026[^abdulkadiroglu2026]). In Chile, Grau, Hojman, and Mizala (2018[^grau2018]) estimated increases in repetition and dropout in an earlier period, whereas Iocco (2024[^iocco2024]), in a preprint on planned closures, finds near-zero average score differences with heterogeneity by destination quality. Because of differences in period, treatment definition, and outcome, both the full 2005–2024 series (+9.11 points under Callaway and Sant'Anna; +6.29 under random effects) and the 2016–2019 estimate of 5.29 points—bounded between −1.15 and 10.98 points—complement rather than mechanically replicate or refute those studies.
{: .text-justify}

### Does the receiving school matter?

In my 2016–2019 panel I explored one piece of that mechanism. Among the 4,362 exposed students who enrolled in another school in the closure year (G), those who moved to a school with a higher prior promotion rate (at G−1) than their closed school (2,099) show a gap of +2.03 percentage points, versus +5.38 points among those who moved to a school with an equal or lower rate (2,263). The pattern points in the direction the literature suggests, but it is descriptive: families choose the destination, the sample leaves out students who did not re-enrol, and the difference between the two groups (−3.35 points) does not yet have an interval that separates it from chance.
{: .text-justify}

<aside class="notice--info" markdown="1">
**Methodological note — How I compared prior receiving-school quality ($$\Delta Q_i$$):** To avoid mechanical circularity, I defined each school's quality strictly from its historical pre-closure performance (at G−1, before receiving displaced students) and computed for each relocated student the difference between their receiving school and their origin school at G−1 in promotion rate, mean attendance, and mean mark. Because families choose the destination school, this contrast is descriptive heterogeneity, and the difference does not yet have its own interval.
</aside>

### Higher education: an open question

<!-- higher-education-agenda:start -->
For students who were in secondary education, the trajectory does not end with their last school enrolment: it still matters whether closure is related to timely entry into higher education, the type of institution, and the selectivity of the destination. That question is deferred to a later instalment. It requires official-provenance individual SIES microdata and, to distinguish test-taking, application, admission, and enrolment, a validated link to DEMRE data. Because those inputs are not accredited for this exercise, this post neither estimates nor suggests postsecondary effects. The future research agenda does not condition publication of the school-outcome results reported here.
{: .notice--info .text-justify}
<!-- higher-education-agenda:end -->

## Spoonful 3: how should a school transition be protected?

### Evidence can help before causality is resolved

Identification limits in the long series and an inconclusive causal estimate in the recent subwindow are not excuses to stand idle when a school closes. On the contrary, the longitudinal diagnostic shows exactly where students disappear from view and what operational guarantees must be required before, during, and after reorganising a school network.
{: .text-justify}

{: .table-caption}
**Table 6.** Minimum information for deciding and evaluating a transition

| Before a decision | During the transition | After the change |
|---|---|---|
| Distinguish school, site, level, merger, and identifier change. | Assign actual places and support to each student. | Follow enrolment, attendance, progression, grades, and wellbeing. |
| Record the announcement date and community participation. | Measure travel time, accessibility, and peer continuity. | Observe students and staff already in receiving schools as well. |
| Verify capacity, staffing, and prior destination quality. | Fund receiving-school load and pedagogical continuity. | Publish alerts, corrections, responsibilities, and deadlines. |
{: .table--compact .table--scroll}

Table 6 shifts the burden of proof against a concrete procedural gap: when the Library of the National Congress asked the Official Recognition Unit of the Metropolitan Regional Secretariat what the “student relocation certificate” (*constancia de reubicación de los alumnos*) required in the voluntary-closure checklist actually entailed, the authority clarified that this requirement—absent from both the statute and Supreme Decree No. 315 of 2010—consisted solely of “having informed students of alternatives for relocating their enrolment”, without verifying whether those nearby schools had actual vacancies or whether students effectively enrolled in them (Castro Paredes 2013[^castroparedes2013], p. 2n1). An authority cannot assume educational continuity merely because an exiting provider handed out a list of nearby schools or because part of the student body reappeared on an enrolment roll: it must verify beforehand that real vacancies, safe transport, support for priority students, and pedagogical support exist at the receiving schools, and track every displaced student by name for at least two years.
{: .text-justify}

## Closing: following trajectories changes the policy question

Part I reconstructed the historical foundations; Part II established which schools closed and what provision existed nearby; this third part followed **78,972 students across 1,141 regular closures** over twenty years. Looking at the full window (2005–2024) changes the perspective: all 19 estimable annual cohorts are positive, the Callaway and Sant'Anna aggregate reaches **+9.11 percentage points** (with Manski bounds from **+0.43 to +16.21 points** above zero; **+6.29 points** under random effects), and the five institutional stages show an attenuation from **+12.15 points** in 2005–2010 and **+7.82** in 2011–2015 to **+5.29 points** in the pre-registered 2016–2019 subwindow—which must always be read alongside its missing-data bounds of **−1.15 to 10.98 points**—**+2.70** in 2020–2022, and **+2.59** in 2023–2024, all conditioned by the higher prior institutional fragility and student mobility of closing schools.
{: .text-justify}

A result with causal limits does support precautionary safeguards today: do not treat proximity or a merely informative relocation notice as continuity, do not reorganise a network without verifying places and support, and follow every student through the transition. These safeguards are not estimated effects of those decisions. They are the minimum standard of public care while Exempt Resolutions terminating Official Recognition, announcement dates, receiving-school capacity, and complete evaluation and grade-promotion records are consolidated.
{: .text-justify}


<details markdown="1" class="post3-methods">
<summary>Methodological notes: closure rule, comparability, full series, and sources</summary>

### How a closure is defined: from documentary certainty to RCID v1

Under Chilean education law, no administrative instrument called a “closure act” (*acta de cierre*) decrees the end of a school. What legally formalises the termination or suspension of a school—through a final and enforceable decision (*acto firme y ejecutoriado*), meaning an official ruling against which no further appeals lie—is an **Exempt Resolution** (*Resolución Exenta*) issued by the respective Regional Ministerial Secretariat (SEREMI) of Education to extinguish or suspend its licence to operate (Official Recognition). That resolution operates under four legal figures: a one-year temporary recess, a tacit renunciation of Official Recognition if teaching does not resume after that recess, a total or partial voluntary renunciation of Official Recognition (**Articles 25 and 26 of Supreme Decree No. 315 of 2010 of MINEDUC**; Castro Paredes 2013[^castroparedes2013]), or the execution of a sanction revoking Official Recognition ordered by the Superintendency of Education (**Article 73(f) of [Law No. 20,529](https://www.bcn.cl/leychile/navegar?idNorma=1028635)**).
{: .text-justify}

Are those resolutions publicly available for every school in the country? To check empirically, I reviewed, in October 2026, the [Active Transparency Portal](https://www.portaltransparencia.cl/PortalPdT/directorio-de-organismos-regulados/?org=AJ001) of the Undersecretariat of Education (agency AJ001, section “Acts and resolutions affecting third parties”). Across the **12,509 administrative resolutions** and **4,735 sanction resolutions** published there, the pre-2018 historical repository is out of service, and between 2018 and 2025 the 16 regional secretariats record only **22 administrative resolutions** on school renunciation, recess, or closure—several of them declaring requests inadmissible for missing documentation or regularising “tacit closures” years after de facto cessation—and **21 unique sanction resolutions** revoking Official Recognition. Until that national registry is consolidated through a freedom-of-information request (**Law No. 20,285**), analysing twenty years of school history requires a transparent, falsifiable empirical rule—the **Data-Inferred School Closure Rule (RCID v1)** presented in Table 1 of the main text—that works like three successive sieves (D0 ⊃ D1 ⊃ D2):
{: .text-justify}

- **D0 (raw administrative exit):** the first sieve detects every school with positive enrolment in one year (t−1) that has no enrolment from t onward, does not reopen through 2025, and is recorded as closed in the official directory.
- **D1 (strict closure of provision):** the second sieve removes annexes or secondary sites and school database identifier (RBD) changes registered as successors from D0—that is, directory continuities.
- **D2 = RCID v1 (flow-purged data-inferred closure):** the third sieve sets aside concentrated transfers: schools with at least **10 baseline students** and **10** students tracked the following year, where a single receiving school takes at least **70%** of those relocated, with a destination concentration index (HHI) of at least **0.50** and the same main destination in t and t+1. These are de facto merger candidates that call for documentary review, not proof of a merger.

Figure 4 summarises the coverage of the territorial audit of the 346 episodes in Table 2: how many have enough prior history and how many flow alerts remain without institutional confirmation.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-4-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/territorial-audit-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/territorial-audit-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-en-dark.svg' | relative_url }} 1600w" alt="Of 346 episodes, 339 have a complete three-year pre-event window and 323 have five. The classification contains 266 with no contradictory signal, 15 continuity candidates, 35 unresolved alerts and 30 right-censored episodes. There are 45 post-event alerts and zero institutional confirmations; automated processing supports observation only." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 4</strong> — Coverage and limits of the territorial audit. Longitudinal follow-up and flow alerts cannot replace evidence on capacity, access, demography, or institutional decisions. <span class="figure-source">Source: author’s calculations from MINEDUC directories and the longitudinal audit.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/territorial-audit-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

### Comparability before closure

{: .table-caption}
**Table 7.** Observed similarity before closure in the weighted sample (2016–2019)

| Baseline characteristic | Exposed students | Comparison group | Reading |
|---|---:|---:|---|
| Mean age | 11.70 years | 11.70 years | Standardised difference: 0.000. |
| Mean attendance | 90.93% | 91.68% | Standardised difference: −0.079. |
| Mean mark | 5.62 | 5.67 | Standardised difference: −0.072. |
| Valid attendance and grade record | 76.8% | 96.2% | Coverage gap: −19.4 pp (observed share, unweighted). |
{: .table--compact .table--scroll}

Age is observed for the full sample and matches by construction, because it is part of the exact matching. Attendance and marks, by contrast, can be compared only among students with those records; coverage is 76.8% among exposed students and 96.2% in the comparison group (a −19.4 percentage-point gap; with controls reweighted to the matching, the gap is −19.2, the figure used in Figure 2). Here a direct link to the legal framework emerges: **Article 27(2) of Supreme Decree No. 315 of 2010** (and section nine of Superintendency of Education Circular No. 1 of 2013; Castro Paredes 2013[^castroparedes2013]) stipulates that the regional secretariat *may rule* on a recess or renunciation request only once the school provider delivers the **evaluation and grade-promotion records (*actas de evaluación y promoción escolar*) for all students**—that is, the official end-of-year sheet certifying marks, attendance, and grade promotion. Nearly one in four exposed students (23.2% versus 3.8% of controls) lacks that sheet in the year before closure. It is tempting to read a provider abandoning the process into that, but the pattern does not confirm it on its own. **17%** of students without a record are in 4 schools that delivered none, and **35%** are in 3 schools that delivered fewer than half. That is consistent with a disorderly administrative closure, like the “tacit closures” in Active Transparency. The remaining **48%** are scattered across schools that delivered most of their records, which fits mid-year transfers or withdrawals better. Neither explanation is proven, and Table 7 certifies neither random assignment nor full sociodemographic comparability.
{: .text-justify}

### Why the 2016–2019 zoom was pre-registered and how it fits into the 2005–2024 series

Focusing the pre-registered cut on **2016–2019** was not arbitrary: the operating-status register in the official school directory was standardised from 2015 onward, observing multi-year pre-trends inside a panel starting in 2004 pushes cohorts toward the mid-2010s, **2020–2022** was disrupted by COVID-19 closures and flexible promotion rules, and **2024–2025** does not yet have two complete post-closure years to measure persistent non-enrolment. A complete reading therefore combines both levels: Table 4 in the main text provides the historical scale across all twenty cohorts and five institutional regimes (where 89.7% of closures occurred between 2005 and 2015), whereas the 2016–2019 zoom documents the stress tests at maximum granularity.
{: .text-justify}

### Why I do not use an instrumental variable

Could that prior selection be overcome using an **instrumental variable**—that is, an external nudge akin to a lottery, such as the rollout of Local Public Education Services (SLEP), the School Admission System (SAE), or municipal demographic shocks? Not in this design: to be valid, an instrument must satisfy the **exclusion restriction**, meaning that external factor affects student progression *solely* because it triggered the school’s closure and through no other channel. Those reforms and demographic shifts simultaneously alter local resources, available seats, and everyday family school-switching decisions, violating that condition. Without a documented lottery or external administrative threshold that satisfies relevance and exclusion, forcing an instrumental model would only manufacture false precision. I therefore run no instrumental-variable regression in this version.
{: .text-justify}

### Three checks on pre-trends, record coverage, and receiving-school quality

Three additional checks on the microdata clarify the scope of the 2016–2019 window:
{: .text-justify}

1. **Sensitivity to prior trends (simplified linear version of Rambachan and Roth 2023) and stayers from G−2:** The three pre-closure placebos in progression are +0.16, +0.30, and +0.40 pp (largest placebo: 0.40 pp; 95% upper bound: 0.81 pp). In the +5.29 pp estimate (CI [2.08, 8.51]; bounds −1.15 to 10.98 pp), the interval margin to zero is 2.07 pp, equal to 2.54 times that 0.81 pp upper bound (without combining with the missing-data bounds). Among **stayers in the same school from G−2**—3,556, or 77.5% of exposed students with a grade observed at G−2 and G−1 (70.6% of all exposed)—progression failure rises **+3.87 pp** ([+1.04, +6.69]), versus **+9.58 pp** ([+5.06, +14.10]) among **late entrants between G−2 and G−1** (1,033): about three-quarters of the gap persists among stayers.
2. **Missing-data bounds by record coverage at G−1:** Outcomes are missing for 3.60% of exposed students and 2.15% of controls; the trimming share is (3.60 − 2.15)/(100 − 3.60) = 1.51%. With 90% or more valid records (1,822 exposed students with an outcome), the difference is +4.26 pp and the worst-case bounds run from +0.09 to +7.84 pp, so zero lies outside the range of possible mixtures (λ* = 1.0114 > 1); dropping the 7 closures with fewer than 50% of records leaves bounds of −0.90 to +12.18 pp; dropping the 4 closures with no records leaves −0.87 to +11.48 pp. None includes sampling error.
3. **Prior receiving-school quality ($$\Delta Q_i$$):** Among 4,362 exposed students enrolled in another school at G, those who moved to a school with a higher prior promotion rate at G−1 than their closed school (2,099) show +2.03 pp, versus +5.38 pp when the receiving school had an equal or lower rate (2,263). The descriptive difference is −3.35 pp, without its own interval; defining quality by mean attendance or by mean mark gives differences of −2.05 and −2.43 pp. The sample excludes students who did not enrol at G.

### Data sources and tools

The data come from MINEDUC open data: the [school directory](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/), [enrolment by student](https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/), and [performance by student](https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/). I processed them with [DuckDB](https://duckdb.org/) over [Apache Parquet/Arrow](https://arrow.apache.org/) files and estimated in Python with [pandas](https://pandas.pydata.org/), [SciPy](https://scipy.org/), and [statsmodels](https://www.statsmodels.org/stable/index.html), including the random-effects meta-analysis. The legal framework for SEP and the Inclusion Law is in Laws [No. 20,248](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=269001&idVersion=) and [No. 20,845](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=1078172&idParte=9605200&idVersion=2222-02-02).
{: .text-justify}

</details>

**Transparency and scope of the sources.** The original thesis and this extension series are my own work, as is my coauthorship of the [2014 working paper]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }})[^grau2014]; they therefore do not constitute an independent external replication, and they keep the historical reconstruction separate from the current re-estimation. I received no external funding and declare no conflicts of interest. My sole institutional affiliation is Chile’s Ministry of Social Development and Family, which did not fund, commission, or review this analysis; the views and conclusions are my sole responsibility. I used artificial-intelligence assistants to support reproducible programming, literature search, statistical validation, and editing; all methodological decisions and factual verifications are my own. The analysis code lives in a private thesis repository and is not yet public; the aggregate figures behind each chart are in the open CSV files that accompany it.
{: .notice--info .text-justify}

---

## References

[^abdulkadiroglu2026]: Abdulkadiroğlu, Atila, Parag A. Pathak, and Christopher R. Walters. 2026. [“Who Gets What in Education: Can School Matching Improve Student Achievement?”](https://doi.org/10.3386/w34936) NBER Working Paper 34936. [Scholar](https://scholar.google.com/scholar_lookup?title=Who+Gets+What+in+Education%3A+Can+School+Matching+Improve+Student+Achievement%3F&doi=10.3386%2Fw34936)

[^beuchert2018]: Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen, and Nina Smith. 2018. [“The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?”](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47. [Scholar](https://scholar.google.com/scholar_lookup?title=The+short-term+effects+of+school+consolidation+on+student+achievement%3A+Evidence+of+disruption%3F&doi=10.1016%2Fj.econedurev.2018.05.004)

[^bross2023]: Bross, Whitney, Douglas N. Harris, and Lihan Liu. 2023. [“The Effects of Performance-Based School Closure and Restart on Student Performance.”](https://doi.org/10.1016/j.econedurev.2023.102368) *Economics of Education Review* 94: 102368. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effects+of+performance-based+school+closure+and+restart+on+student+performance&doi=10.1016%2Fj.econedurev.2023.102368)

[^brummet2014]: Brummet, Quentin. 2014. [“The Effect of School Closings on Student Achievement.”](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–24. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effect+of+school+closings+on+student+achievement&doi=10.1016%2Fj.jpubeco.2014.06.010)

[^callaway2021]: Callaway, Brantly, and Pedro H. C. Sant'Anna. 2021. [“Difference-in-Differences with Multiple Time Periods.”](http://arxiv.org/pdf/1803.09015) *Journal of Econometrics* 225 (2): 200–230. [DOI](https://doi.org/10.1016/j.jeconom.2020.12.001) · [Scholar](https://scholar.google.com/scholar_lookup?title=Difference-in-Differences+with+multiple+time+periods&doi=10.1016%2Fj.jeconom.2020.12.001)

[^castroparedes2013]: Castro Paredes, Luis. 2013. [*Cierre voluntario de Establecimientos Educacionales*](https://obtienearchivo.bcn.cl/obtienearchivo?id=repositorio/10221/20674/5/Cierre%20voluntario%20de%20Establecimientos%20Educacionales_v2.pdf). Parliamentary Technical Advisory Report, Library of the National Congress of Chile (BCN), December 12, 2013.

[^engberg2012]: Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. [“Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?”](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203. [Scholar](https://scholar.google.com/scholar_lookup?title=Closing+schools+in+a+shrinking+district%3A+Do+student+outcomes+depend+on+which+schools+are+closed%3F&doi=10.1016%2Fj.jue.2011.10.001)

[^grau2014]: Grau, Nicolás, Daniel A. Hojman, Cristián Labra, and Alejandra Mizala. 2014. [“Destructive Creation: School Turnover and Educational Attainment.”]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}) Working Paper 396, Universidad de Chile.

[^grau2018]: Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. [“School Closure and Educational Attainment: Evidence from a Market-Based System.”](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf) *Economics of Education Review* 65: 1–17. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)

[^iocco2024]: Iocco, Maria Pia. 2024. [“Impact of Planned School Closures on Academic Performance: Evidence from Chile.”](https://doi.org/10.2139/ssrn.4808834) SSRN preprint. [Scholar](https://scholar.google.com/scholar_lookup?title=Impact+of+Planned+School+Closures+on+Academic+Performance%3A+Evidence+from+Chile&doi=10.2139%2Fssrn.4808834)

[^kim2024]: Kim, Jeonghyeok. 2024. [“The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes.”](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963. [Scholar](https://scholar.google.com/scholar_lookup?title=The+Long+Shadow+of+School+Closures%3A+Impacts+on+Students%27+Educational+and+Labor+Market+Outcomes&doi=10.26300%2FAX4M-3Z14)

[^larsen2020]: Larsen, Matthew F. 2020. [“Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment.”](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980. [Scholar](https://scholar.google.com/scholar_lookup?title=Does+closing+schools+close+doors%3F+The+effect+of+high+school+closings+on+achievement+and+attainment&doi=10.1016%2Fj.econedurev.2020.101980)

[^manski2003]: Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). New York: Springer. [Scholar](https://scholar.google.com/scholar_lookup?title=Partial+Identification+of+Probability+Distributions&doi=10.1007%2Fb97478)

[^rambachan2023]: Rambachan, Ashesh, and Jonathan Roth. 2023. [“A More Credible Approach to Parallel Trends.”](https://doi.org/10.1093/restud/rdad018) *The Review of Economic Studies* 90 (5): 2555–91. [Scholar](https://scholar.google.com/scholar_lookup?title=A+More+Credible+Approach+to+Parallel+Trends&doi=10.1093%2Frestud%2Frdad018)

[^roth2023]: Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–44. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)

[^steinberg2019]: Steinberg, Matthew P., and John M. MacDonald. 2019. [“The Effects of Closing Urban Schools on Students’ Academic and Behavioral Outcomes: Evidence from Philadelphia.”](https://doi.org/10.1016/j.econedurev.2018.12.005) *Economics of Education Review* 69: 25–60. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effects+of+closing+urban+schools+on+students%E2%80%99+academic+and+behavioral+outcomes%3A+Evidence+from+Philadelphia&doi=10.1016%2Fj.econedurev.2018.12.005)

[^sun2021]: Sun, Liyang, and Sarah Abraham. 2021. [“Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects.”](https://doi.org/10.1016/j.jeconom.2020.09.006) *Journal of Econometrics* 225 (2): 175–99. [Scholar](https://scholar.google.com/scholar_lookup?title=Estimating+dynamic+treatment+effects+in+event+studies+with+heterogeneous+treatment+effects&doi=10.1016%2Fj.jeconom.2020.09.006)

[^taghizadeh2020]: Taghizadeh, Jonas Larsson. 2020. [“Are Students in Receiving Schools Hurt by the Closing of Low-Performing Schools? Effects of School Closures on Receiving Schools in Sweden 2000–2016.”](https://doi.org/10.1016/j.econedurev.2020.102020) *Economics of Education Review* 78: 102020. [Scholar](https://scholar.google.com/scholar_lookup?title=Are+students+in+receiving+schools+hurt+by+the+closing+of+low-Performing+schools%3F+Effects+of+school+closures+on+receiving+schools+in+Sweden+2000%E2%80%932016&doi=10.1016%2Fj.econedurev.2020.102020)
