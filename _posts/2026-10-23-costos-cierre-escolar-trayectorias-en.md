---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extending my thesis in three spoonfuls (part III): what student trajectories show after a school closure"
subtitle: "Following students makes the transition observable, but still cannot cleanly separate closure from trajectories that were already changing."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-10-28 04:00:00 -0300
categories: [data, education, public-policy]
tags: [education, school-closure, trajectories, causality, mineduc, administrative-data, duckdb, public-policy]
description: "Student trajectories and school closures in Chile: post-pilot results, causal limits, and minimum conditions for a responsible school transition."
excerpt: "The comparison finds a difference in grade progression, but the missing-data bounds span both signs. The evidence can inform transitions, but cannot yet attribute harm or benefit to closure."
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
math: false
toc: true
toc_sticky: true
comments: true
author_profile: true
distribution:
  social: false
  republish: []
  skip_reason: "Local candidate: distribution is enabled only after human editorial approval and canonical publication."
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
---

When a school closes, finding another school on a map does not settle the public question. What matters is whether its students stayed enrolled, moved up to the expected grade, and sustained regular attendance. Above all, we need to separate how much of any later setback comes from the closure itself and how much was already unfolding beforehand.
{: .text-justify}

The primary comparison estimates that the before-and-after change in the **observed share with no enrolment or enrolment below the expected grade one year later—summarised as “progression failure or grade lag”—was 5.29 percentage points larger among exposed students than in the comparison group**, with a conservative 95% confidence interval from **2.08 to 8.51 points**. Because next-year progression is not observed for every student, however, assumption-free missing-data bounds (Manski 2003) span **−1.15 to 10.98 percentage points**. Because that range crosses zero, the main-window result is **inconclusive**: on its own, it demonstrates neither harm, benefit, nor the absence of an effect.
{: .text-justify}

This exercise reports a **post-pilot re-estimation** across **79,709,054 enrolment records** and **73,873,835 performance records** from 2004 to 2025. That scale reveals individual trajectories that school-level averages hide, but it cannot manufacture the counterfactual—what would have happened to those same children and adolescents (NNA) had their school stayed open—required for a causal claim.
{: .text-justify}

<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->
<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->

[Part I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) reconstructed the historical evidence and separated the findings that held up. [Part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) verified which schools closed in the recent decade and showed that the nearest school is rarely the main destination. This third instalment shifts from buildings to student trajectories in three steps: **what actually closed**, **what happened next to students**, and **how to protect a school transition in practice**.
{: .text-justify}

## Spoonful 1: what closed, and who was exposed?

### A student flow is a signal, not an administrative act

In the recent period (2016–2025), **346 episodes** appear in administrative records as schools with prior enrolment ceasing operation. After setting aside annexes, administrative changes, and likely continuities, [Part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) identified **330 strict closures** of educational provision. Tracking their students the following year reveals when nearly an entire student body moves together to a single receiving school: that pattern can reflect a merger, a code change, or simply an accessible nearby school, but student flow alone never replaces a formal administrative act.
{: .text-justify}

{: .table-caption}
**Table 1.** Diagnostic reading of the 346 episodes recorded as closures

| Status | Episodes | Supported interpretation |
|---|---:|---|
| No contradictory signal | 266 | The trajectory does not contradict a strict closure; it is not external corroboration. |
| Continuity candidate | 15 | Name, level or form of provision, or later activity warrants documentary review. |
| Unresolved alert | 35 | The category remains unchanged until independent evidence is available. |
| Incomplete follow-up | 30 | These closures occurred in 2025, so the following year is not yet observed. |
{: .table--compact .table--scroll}

Each of the 346 episodes appears once in Table 1. The **45 concentrated-destination alerts** come from a cross-cutting flow check that overlaps those categories and must not be added to them; this phase has **zero independent institutional confirmations**, so the 330 strict closures remain the baseline reference.
{: .text-justify}

### From documentary certainty to the Data-Inferred School Closure Rule (RCID v1)

Across twenty years of massive panels without a physical paper file for every school, we need an explicit, falsifiable rule that separates a raw directory exit from a genuine closure that disperses students. That is the **Data-Inferred School Closure Rule (`RCID v1`)**, structured into three nested strata (D0 ⊃ D1 ⊃ D2):
{: .text-justify}

- **D0 (raw administrative exit):** positive enrolment in t−1, zero enrolment in t, and no subsequent teaching activity.
- **D1 (strict closure of provision):** purges reopenings, database-identifier (RBD) changes on the same site, and administrative continuities from D0.
- **D2 = RCID v1 (flow-purged data-inferred closure):** requires at least 5 trackable students in t−1 and sets aside concentrated absorptions in which a single receiving school absorbs at least **70%** of relocated students and at least **15 students** in t.

{: .table-caption}
**Table 2.** Hierarchy of the Data-Inferred School Closure Rule (`RCID v1`, D0 ⊃ D1 ⊃ D2) across all three instalments (2005–2025)

| Rule stratum | Historical window (2005–2015) | Recent window (2016–2025) | Longitudinal series (2005–2025) | What it purges and how it is used in Parts I, II, and III |
|---|---:|---:|---:|---|
| D0: raw administrative or activity exit | 1,635 | 346 | 1,981 | Enrolment cessation in t; contrasts with the 2,069 raw directory exits of 1992–2012 in Part I. |
| D1: strict closure of educational provision | 1,477 | 330 | 1,807 | Purges 158 historical reopenings or continuities and 16 recent candidate continuities or annexes (Part II baseline). |
| D2 = RCID v1 (conservative, includes right-censored 2025) | 1,382 | 296 | 1,678 | Further purges 95 historical absorptions and 34 recent concentrated absorptions or flow alerts (≥ 70% and ≥ 15 students). |
| D2 = RCID v1 (clean with observed t+1 window) | 1,382 | 266 | 1,648 | Requires observing the full t+1 year (excludes the 30 right-censored 2025 episodes); main baseline for Part III. |
{: .table--compact .table--scroll}

Put simply, an entire class moving together into another building is not the same experience as families searching for places one by one. Applying `RCID v1` (D2) leaves **1,648 clean closures** with an observed post-closure year across 2005–2025 (**266** in the recent window), providing a consistent foundation that avoids conflating de facto mergers with dispersed closures.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-1-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/sample-flow-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/sample-flow-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-en-dark.svg' | relative_url }} 1600w" alt="Two lanes summarise support for the 2016 to 2019 post-pilot re-estimation. Of 64 historical episodes before support screening, 63 retain at least one comparable stratum and one is fully excluded. Of 6,581 exposed student-cohort observations, 391 are excluded and 6,190 remain. The support universe contains 82,753 control student-cohort observations; final samples differ by outcome." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 1</strong> — How the comparable sample is formed for the post-pilot re-estimation (2016–2019). Aggregate counts precede outcome-specific eligibility, and their units must not be added together. <span class="figure-source">Source: author’s calculations from the post-pilot re-estimation.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/sample-flow-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

Figure 1 distinguishes between school episodes and “student-cohort” observations (one student counted within one closure cohort). All public outputs remain strictly aggregated: no names, addresses, or school or individual identifiers are exposed.
{: .text-justify}

## Spoonful 2: what happened after closure?

### Two primary outcomes and an uncomfortable conclusion

To measure what happened after closure in the **2016–2019** primary window, we follow students from the **63 supported episodes** in Figure 1 (**62 episodes** have an observable follow-up window for the two primary outcomes and **58** for attendance and marks). The first primary outcome tracks the share of students with **no enrolment record for two consecutive years**: we do not call this “dropout” because absence from Chile’s administrative register does not by itself reveal the reason or destination. Here the exposed group’s before-and-after change exceeds the comparison group’s by **+0.63 percentage points**, with a conservative 95% confidence interval from **−0.77 to 2.03 points** (across **3,666** exposed observations and **49,944** controls).
{: .text-justify}

The second primary outcome measures the share with **no enrolment or enrolment below the expected grade one year later**, summarised as **progression failure or grade lag**. Here the before-and-after gap rises by **+5.29 percentage points** among exposed students relative to controls (conservative interval from **2.08 to 8.51 points**, across **4,815** exposed observations and **65,538** controls). The catch lies in the students whose progression record is missing: when we compute assumption-free Manski bounds for those missing records, the possible range spans **−1.15 to 10.98 percentage points**. Because that interval encompasses both a slight improvement and a nearly eleven-point setback, the point estimate cannot support a definitive causal claim.
{: .text-justify}

{: .table-caption}
**Table 3.** Post-pilot re-estimation (2016–2019): observed differences, not causal effects

| Outcome | Estimated difference | Conservative 95% interval | Decisive condition |
|---|---:|---:|---|
| Persistent non-enrolment for two years | +0.63 pp | [−0.77, 2.03] | It is not dropout; the estimable pre-event trend rests on few episodes. |
| Progression failure or grade lag: no enrolment or below the expected grade one year later | +5.29 pp | [2.08, 8.51] | Missing-data bounds: [−1.15, 10.98] pp. |
| Attendance | −1.15 points | [−2.40, 0.10] | Exploratory and conditional; requires valid attendance and observable final pass/repeat status. |
| Average mark | −0.06 | [−0.14, 0.01] | Exploratory and conditional; only among students with observable performance. |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-2-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }} 1600w" alt="Inconclusive post-pilot re-estimation of two primary outcomes. Persistent non-enrolment is estimated at 0.63 percentage points, with a CI from minus 0.77 to 2.03; the different sample that includes receiver schools gives 0.71, from minus 0.69 to 2.12. Progression failure or grade lag is estimated at 5.29 points, from 2.08 to 8.51; the different receiver-school sample gives 5.09, from 1.94 to 8.23. Missing-data bounds span minus 1.15 to 10.98 points. These are not confirmed causal effects." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 2</strong> — Inconclusive post-pilot re-estimation, not causal effects. The progression interval does not cross zero, but its missing-data bounds do; overlap with the pilot and unobserved assumptions prevent a causal interpretation. <span class="figure-source">Source: author’s calculations from the post-pilot re-estimation.</span> <span class="figure-data">Accessible tabular data: <a href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-data.csv' | relative_url }}">estimates</a> and <a href="{{ '/assets/images/tesis-post3/missingness-bounds-data.csv' | relative_url }}">missing-data bounds</a>.</span></figcaption>
</figure>

Attendance and average marks in Table 3 are **exploratory and conditional**: they can be measured only among students with valid annual performance records in both periods (**3,871** exposed observations across **58 episodes**, covering **62.5%** of exposed support versus **76.8%** of controls, with **63,591** and **63,596** comparison observations). In Figure 2, the alternative bar that keeps receiving schools inside the control group yields **+0.71 percentage points** in non-enrolment ([−0.69, 2.12], across 3,670 exposed and 59,613 controls) and **+5.09 points** in progression failure ([1.94, 8.23], across 4,822 exposed and 79,058 controls): changing which schools enter the control pool alters sample composition, but does not remove the **−1.15 to 10.98 point** bounds attached to the main +5.29 pp estimate.
{: .text-justify}

One further statistical limit is best pictured as a **meeting room**. Even though 62 closed schools enter the primary estimation, a handful of large closures account for a disproportionate share of students. Listening to those 62 closures is therefore less like hearing 62 independent voices at equal volume and more like hearing **21.1 effective episodes** for non-enrolment, **21.9** for progression, and just **17.7** for attendance and marks. Likewise, splitting urban and rural closures rests on even fewer rural episodes, so territorial recommendations must wait for road-network travel times and school-transport data.
{: .text-justify}

### Are we comparing like with like?

The design uses **differences in differences**: it measures how much the exposed group changed before and after closure and subtracts the change among control students matched exactly one year before the event (G−1) on year, sex, region, provider type, rurality, education level, and starting grade. Put simply, we try to compare like with like across every characteristic recorded in the data.
{: .text-justify}

{: .table-caption}
**Table 4.** Observed similarity before closure in the weighted sample (2016–2019)

| Baseline characteristic | Exposed students | Comparison group | Reading |
|---|---:|---:|---|
| Mean age | 11.70 years | 11.70 years | Standardised difference: 0.000. |
| Mean attendance | 90.93% | 91.68% | Standardised difference: −0.079. |
| Mean mark | 5.62 | 5.67 | Standardised difference: −0.072. |
| Valid attendance and grade record | 76.8% | 96.2% | Coverage gap: −19.4 pp. |
{: .table--compact .table--scroll}

Age is observed for the full sample. Attendance and marks, by contrast, can be compared only among students with those records; coverage is 76.8% among exposed students and 96.2% in the comparison group (a −19.4 percentage-point gap). Table 4 therefore certifies neither random assignment nor full sociodemographic comparability: it shows balance in observed averages alongside selective record loss among students whose school is about to close.
{: .text-justify}

What happens when we broaden the lens to social vulnerability and prior schooling history between G−3 and G−1? Table 5 summarises eight key descriptors of children and adolescents (NNA) and their origin schools.
{: .text-justify}

{: .table-caption}
**Table 5.** Extended baseline characterisation of children and adolescents (NNA) at G−1 (2016–2019 cohorts, 6,190 exposed and 82,753 controls)

| Baseline descriptor at G−1 | Exposed students | Comparison group | Gap (pp) | Substantive reading for identification |
|---|---:|---:|---:|---|
| Priority SEP student (`PRIORITARIO_ALU`) | 30.68% | 32.32% | −1.64 | Close balance in priority socioeconomic vulnerability after matching. |
| Total SEP eligibility (priority or preferential) | 54.51% | 55.58% | −1.07 | Individual eligible socioeconomic composition is comparable at G−1. |
| Effective SEP beneficiary (`BEN_SEP`) | 37.63% | 48.58% | −10.95 | Despite equal individual eligibility, exposed students receive lower effective SEP coverage. |
| Origin school with SEP agreement (`CONVENIO_SEP`) | 45.17% | 55.23% | −10.06 | Closures cluster among providers with lower institutional SEP participation. |
| Origin school with Full School Day (JEC) | 53.97% | 72.51% | −18.54 | Lower full-day provision in schools that subsequently close. |
| Inter-municipality commuting (residence ≠ school municipality) | 38.59% | 29.99% | +8.60 | Higher share of NNA already commuting outside their home municipality before closure. |
| Over-age ≥ 1 year relative to grade norm | 33.86% | 33.86% | 0.00 | Exact balance by construction of the G−1 matching strata. |
| At least one school switch between G−3 and G−1 | 47.04% | 30.52% | +16.52 | Nearly half of exposed students were already switching schools before closure. |
{: .table--compact .table--scroll}

The profile in Table 5 explains why caution is essential: exposed students and their controls share the same age, the same prior grade lag (33.86%), and nearly identical individual eligibility for the Preferential School Subsidy (54.51% versus 55.58%, with **30.68%** priority students), yet they attended institutionally weaker schools—with lower SEP agreement coverage (−10.06 pp) and lower Full School Day coverage (−18.54 pp)—and nearly half (**47.04%** versus 30.52%) had already switched schools during the two preceding years. Part of the strain and mobility preceded closure.
{: .text-justify}

### Why was 2016–2019 chosen, and what does the full 2005–2024 series show?

Focusing the primary cut on **2016–2019** was not arbitrary: the official directory status field (`ESTADO_ESTAB`) was standardised from 2015 onward, observing multi-year pre-trends inside a panel starting in 2004 pushes cohorts toward the mid-2010s, **2020–2022** was disrupted by COVID-19 closures and flexible promotion rules, and **2024–2025** is right-censored for two-year non-enrolment.
{: .text-justify}

Even so, using modern staggered difference-in-differences estimators for multiple time periods (Callaway and Sant'Anna 2021; Sun and Abraham 2021; Roth et al. 2023) together with formal sensitivity bounds (Manski 2003; Rambachan and Roth 2023), we estimate all **20 annual closure cohorts from 2005 to 2024** under `RCID v1` (D2) against not-yet-treated controls. The full series spans **1,141 empirically supported episodes**, **78,972 exposed observations**, and **734,472 controls**; the cohort-by-cohort series is available in the [open CSV for Figure 3]({{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}), while Table 6 summarises the five institutional regimes, the annual range, and the three series-wide aggregates.
{: .text-justify}

{: .table-caption}
**Table 6.** Summary of the full 2005–2024 series by institutional regime, annual range, and aggregation scheme (`RCID v1`)

| Institutional regime / Range / Aggregate | Supported episodes | Exposed (N) | Controls (N) | Progression failure or grade lag (pp) | 95% CI progression (pp) | 2-year persistent non-enrolment (pp) | 95% CI non-enrolment (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sub-aggregate 2005–2010 (LOCE regime and early SEP) | 521 | 36,984 | 334,062 | +12.15 | [+3.78, +20.52] | +1.21 | [+0.53, +1.90] |
| Sub-aggregate 2011–2015 (LGE and SAC rollout) | 502 | 31,512 | 260,740 | +7.82 | [+6.20, +9.41] | +1.85 | [+1.10, +2.59] |
| Sub-aggregate 2016–2019 (main window; bounds [−1.15, 10.98] pp) | 63 | 6,190 | 82,753 | +5.29 | [+2.08, +8.51] | +0.63 | [−0.77, +2.03] |
| Sub-aggregate 2020–2022 (COVID-19 pandemic and flexible promotion) | 33 | 3,272 | 42,457 | +2.70 | [−0.63, +6.03] | −0.28 | [−1.37, +0.81] |
| Sub-aggregate 2023–2024 (post-pandemic reactivation; 2024 censored at 2 years) | 22 | 1,014 | 14,460 | +2.59 | [−1.55, +6.73] | −0.93 | [−2.64, +0.78] |
| **Annual range (19 cohorts in progression; 17 in non-enrolment)** | **7 to 129** | **357 to 10,261** | **5,566 to 71,248** | **+0.94 to +28.22 (median: +7.18)** | **[+3.15, +9.62] (IQR)** | **−0.93 to +4.56 (median: +0.92)** | **[+0.22, +2.11] (IQR)** |
| **Full-series aggregate 2005–2024 (Callaway & Sant'Anna, exposed-weighted)** | **1,141** | **78,972** | **734,472** | **+9.11** | **[+5.34, +12.88]** | **+1.38** | **[+0.92, +1.85]** |
| **Full-series aggregate 2005–2024 (equal annual cohort weights)** | **1,141** | **78,972** | **734,472** | **+7.55** | **[+5.52, +9.57]** | **+1.03** | **[+0.56, +1.50]** |
| **Full-series aggregate 2005–2024 (inverse-variance precision; I² = 76.48%)** | **1,141** | **78,972** | **734,472** | **+5.14** | **[+4.34, +5.95]** | **+0.54** | **[+0.29, +0.79]** |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-4-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }} 1600w" alt="Three-panel infographic under the RCID v1 rule with 1,141 supported episodes between 2005 and 2024. Panel A displays the 19 estimable annual cohorts for progression failure or grade lag from 2006 to 2024: all 19 point estimates are positive, ranging from 0.94 to 28.22 percentage points, with a median of 7.18 and a Callaway and Sant'Anna student-weighted aggregate of +9.11 points (interval from 5.34 to 12.88 and Manski bounds from +0.43 to +16.21 points). Panel B shows attenuation across institutional regimes from 12.15 points in 2005–2010 and 7.82 in 2011–2015 to 5.29 in 2016–2019 (with missing-data bounds from minus 1.15 to 10.98 points), 2.70 in 2020–2022, and 2.59 in 2023–2024. Panel C shows G minus 1 baseline gaps after exact matching: individual SEP eligibility is balanced (−1.07 points), whereas exposed students face lower school SEP agreements (−10.06 points), lower full-day schooling (−18.54 points), lower valid record coverage (−19.24 points), and higher prior school switching (+16.52 points)." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 3</strong> — Full 2005–2024 series audit under <code>RCID v1</code>: annual estimates (2006–2024), attenuation across institutional regimes, and NNA baseline gaps at G−1. <span class="figure-source">Source: author’s calculations from the 2004–2025 panel and the audited v1 full-series artifact.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

The long series in Table 6 and Figure 3 yields three clear takeaways:
{: .text-justify}

- **The 2016–2019 window was not cherry-picked to inflate the result:** on the contrary, the progression gap attenuates monotonically as the Preferential School Subsidy (SEP), the Quality Assurance System (SAC), and the Inclusion Law rolled out—falling from **+12.15 percentage points** in 2005–2010 and **+7.82 points** in 2011–2015 to **+5.29 percentage points** in 2016–2019 (with its **−1.15 to 10.98 point** bounds), **+2.70 points** in 2020–2022, and **+2.59 points** in 2023–2024.
- **Across the full series, all 19 estimable progression cohorts are positive:** the exposed-weighted Callaway and Sant'Anna aggregate reaches **+9.11 percentage points** ([+5.34, +12.88]) and its Manski bounds (**+0.43 to +16.21 points**) do not cross zero, while inverse-variance weighting—which downweights cross-cohort dispersion (I² = 76.48%)—converges to **+5.14 points** ([+4.34, +5.95]).
- **Larger sample size does not replace a randomised trial:** given the high prior school switching at G−1 (47.04%) and a modest mean pre-trend deviation at G−2 of −1.49 points across the long series, any strict causal reading must account for how sensitive conclusions are to plausible departures from parallel trends (Rambachan and Roth 2023).

Could we overcome that endogeneity with an instrumental variable, such as the rollout of Local Public Education Services (SLEP), the School Admission System (SAE), or municipal demographic shocks? Not in this setting: those reforms and enrolment drops directly alter resources, available seats, and family school-switching decisions, violating the exclusion restriction (that an instrument affect student outcomes only through closure). Without a documented lottery or external administrative threshold that satisfies relevance and exclusion, forcing an instrumental model would manufacture false precision. No instrumental-variable regression is therefore run in this version.
{: .text-justify}

### What the literature adds—and what it does not

International evidence agrees that the impact of closing a school depends jointly on the transition process and on the quality of the receiving school: students often experience disruption during the announcement and first post-closure year, followed by partial recovery when they transfer to higher-value-added schools, but lasting setbacks in attendance or secondary graduation when relocated into congested or similarly weak schools (Engberg et al. 2012; Brummet 2014; Beuchert et al. 2018; Steinberg and MacDonald 2019; Larsen 2020; Taghizadeh 2020; Bross, Harris, and Liu 2023; Kim 2024; Abdulkadiroğlu, Pathak, and Walters 2026). In Chile, Grau, Hojman, and Mizala (2018) estimated increases in repetition and dropout in an earlier period, whereas Iocco (2024), in a preprint on planned closures, finds near-zero average score differences with heterogeneity by destination quality. Because of differences in period, treatment definition, and outcome, the 5.29-point estimate—bounded between −1.15 and 10.98 points—complements rather than mechanically replicates or refutes those studies.
{: .text-justify}

**Historical reconstruction capsule.** The closest Chilean antecedent is [*Destructive Creation* (Working Paper 396, 2014)]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}), which I coauthored. Its Table 7 reported a **+1.46 percentage-point** difference in absence from the official register for at least two years, among 682,217 students. Table 8 reported +1.74 points in a restricted comparison of 2,361 students, and Table 14 reported +1.08 points in an expanded sample of 906,629. These are published marginal effects from probit models, not results from the current re-estimation. Causal Tables 5, 6, 7, 8, and 14 remain **not comparable**: the original estimation file, exact analytical input, and full transformation rule were not recovered, and the equation and notes disagree about fixed effects. The figures therefore describe the paper, but do not now confirm or correct its execution.
{: .notice--info .text-justify}

### Higher education: an open question

<!-- higher-education-agenda:start -->
For students who were in secondary education, the trajectory does not end with their last school enrolment: it still matters whether closure is related to timely entry into higher education, the type of institution, and the selectivity of the destination. That question is deferred to a later instalment. It requires official-provenance individual SIES microdata and, to distinguish test-taking, application, admission, and enrolment, a validated link to DEMRE data. Because those inputs are not accredited for this exercise, this post neither estimates nor suggests postsecondary effects. The future research agenda does not condition publication of the school-outcome results reported here.
{: .notice--info .text-justify}
<!-- higher-education-agenda:end -->

## Spoonful 3: how should a school transition be protected?

### Evidence can help before causality is resolved

An inconclusive causal estimate in the recent window is not an excuse to stand idle when a school closes. On the contrary, the longitudinal diagnostic shows exactly where students disappear from view and what operational guarantees must be required before, during, and after reorganising a school network.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-3-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/territorial-audit-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/territorial-audit-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-en-dark.svg' | relative_url }} 1600w" alt="Of 346 episodes, 339 have a complete three-year pre-event window and 323 have five. The classification contains 266 with no contradictory signal, 15 continuity candidates, 35 unresolved alerts and 30 right-censored episodes. There are 45 post-event alerts and zero institutional confirmations; automated processing supports observation only." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 4</strong> — Coverage and limits of the territorial audit. Longitudinal follow-up and flow alerts cannot replace evidence on capacity, access, demography, or institutional decisions. <span class="figure-source">Source: author’s calculations from MINEDUC directories and the longitudinal audit.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/territorial-audit-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

{: .table-caption}
**Table 7.** Minimum information for deciding and evaluating a transition

| Before a decision | During the transition | After the change |
|---|---|---|
| Distinguish school, site, level, merger, and identifier change. | Assign actual places and support to each student. | Follow enrolment, attendance, progression, grades, and wellbeing. |
| Record the announcement date and community participation. | Measure travel time, accessibility, and peer continuity. | Observe students and staff already in receiving schools as well. |
| Verify capacity, staffing, and prior destination quality. | Fund receiving-school load and pedagogical continuity. | Publish alerts, corrections, responsibilities, and deadlines. |
{: .table--compact .table--scroll}

Figure 4 and Table 7 shift the burden of proof: an authority cannot assume educational continuity merely because another school stands a few kilometres away or because a group of pupils reappeared on an enrolment roll. It must verify beforehand that real vacancies, safe transport, active SEP agreements, and pedagogical support exist at the receiving schools, and track every displaced student by name for at least two years.
{: .text-justify}

## Closing: following trajectories changes the policy question

Part I reconstructed the historical foundations; Part II established which schools closed and what provision existed nearby; this third part followed student trajectories and showed why the map was not enough. The headline result for the recent window—a **5.29 percentage-point** rise in progression failure or grade lag—must always be read alongside its missing-data bounds of **−1.15 to 10.98 points**, and the long-series gap (+9.11 points under Callaway and Sant'Anna; +5.14 points under inverse-variance weighting) must be read alongside the higher prior mobility and institutional fragility of closing schools.
{: .text-justify}

An inconclusive result does support precautionary safeguards today: do not treat proximity as continuity, do not reorganise a network without verifying places and support, and follow every student through the transition. These safeguards are not estimated effects of those decisions. They are the minimum standard of public care while better data are built on announcement dates, receiving-school capacity, and complete performance records.
{: .text-justify}

### Transparency and scope of the sources

The original thesis and this extension series are my own work, as is my coauthorship of the 2014 working paper; they therefore do not constitute an independent external replication, and they keep the historical reconstruction separate from the current re-estimation. I received no external funding and declare no conflicts of interest. My sole institutional affiliation is Chile’s Ministry of Social Development and Family, which did not fund, commission, or review this analysis; the views and conclusions are my sole responsibility. I used artificial-intelligence assistants to support reproducible programming, literature search, statistical validation, and editing; all methodological decisions and factual verifications are my own.
{: .text-justify}

---

## References

<div class="post-references" markdown="1">

Abdulkadiroğlu, Atila, Parag A. Pathak, and Christopher R. Walters. 2026. [“Who Gets What in Education: Can School Matching Improve Student Achievement?”](https://doi.org/10.3386/w34936) NBER Working Paper 34936.

Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen, and Nina Smith. 2018. [“The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?”](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47.

Bross, Whitney, Douglas N. Harris, and Lihan Liu. 2023. [“The Effects of Performance-Based School Closure and Restart on Student Performance.”](https://doi.org/10.1016/j.econedurev.2023.102368) *Economics of Education Review* 94: 102368.

Brummet, Quentin. 2014. [“The Effect of School Closings on Student Achievement.”](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–24.

Callaway, Brantly, and Pedro H. C. Sant'Anna. 2021. [“Difference-in-Differences with Multiple Time Periods.”](https://doi.org/10.1016/j.jeconom.2020.12.001) *Journal of Econometrics* 225 (2): 200–230.

Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. [“Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?”](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203.

Grau, Nicolás, Daniel A. Hojman, Cristián Labra, and Alejandra Mizala. 2014. [“Destructive Creation: School Turnover and Educational Attainment.”]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}) Working Paper 396, Universidad de Chile.

Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. [“School Closure and Educational Attainment: Evidence from a Market-Based System.”](https://doi.org/10.1016/j.econedurev.2018.05.003) *Economics of Education Review* 65: 1–17.

Iocco, Maria Pia. 2024. [“Impact of Planned School Closures on Academic Performance: Evidence from Chile.”](https://doi.org/10.2139/ssrn.4808834) SSRN preprint.

Kim, Jeonghyeok. 2024. [“The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes.”](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963.

Larsen, Matthew F. 2020. [“Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment.”](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980.

Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). New York: Springer.

Rambachan, Ashesh, and Jonathan Roth. 2023. [“A More Credible Approach to Parallel Trends.”](https://doi.org/10.1093/restud/rdad018) *The Review of Economic Studies* 90 (5): 2555–91.

Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://doi.org/10.1016/j.jeconom.2023.03.008) *Journal of Econometrics* 235 (2): 2218–44.

Steinberg, Matthew P., and John M. MacDonald. 2019. [“The Effects of Closing Urban Schools on Students’ Academic and Behavioral Outcomes: Evidence from Philadelphia.”](https://doi.org/10.1016/j.econedurev.2018.12.005) *Economics of Education Review* 69: 25–60.

Sun, Liyang, and Sarah Abraham. 2021. [“Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects.”](https://doi.org/10.1016/j.jeconom.2020.09.006) *Journal of Econometrics* 225 (2): 175–99.

Taghizadeh, Jonas Larsson. 2020. [“Are Students in Receiving Schools Hurt by the Closing of Low-Performing Schools? Effects of School Closures on Receiving Schools in Sweden 2000–2016.”](https://doi.org/10.1016/j.econedurev.2020.102020) *Economics of Education Review* 78: 102020.

</div>
