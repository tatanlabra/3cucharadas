---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extending my thesis in three spoonfuls (part III): what student trajectories show after a school closure"
subtitle: "Following students makes the transition observable, but still cannot cleanly separate closure from trajectories that were already changing."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-10-27 04:00:00 -0300
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

When a school closes, finding another school on a map does not settle the policy question. We need to know whether its students remained enrolled, progressed to the next grade, and sustained their attendance. We also need to distinguish what happened after closure from what would have happened had the school remained open.
{: .text-justify}

The latest comparison estimates that the before-and-after change in the **observed share with no enrolment or enrolment below the expected grade one year later—summarised as “progression failure or grade lag”—was 5.29 percentage points larger among exposed students than in the comparison group**. The conservative 95% confidence interval—the range of uncertainty produced by the procedure—runs from **2.08 to 8.51 points**. Once scenarios for missing progression records are included, however, the bounds range from **−1.15 to 10.98 percentage points**. That range spans both signs. The result is therefore **inconclusive**: it demonstrates neither harm, benefit, nor the absence of an effect.
{: .text-justify}

This exercise presents a **post-pilot re-estimation**; it is not an independent confirmation. The database links **79,709,054 enrolment records** and **73,873,835 performance records** from 2004 to 2025. Its scale makes trajectories visible and exposes problems that school-level aggregates conceal, but it cannot create the counterfactual—what would have happened without closure—required for a causal claim.
{: .text-justify}

<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->
<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->

[Part I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) reconstructed the historical evidence and separated the results that survived from those that needed correction. [Part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) verified what closed in the recent period and showed that a nearby school is not necessarily the students’ destination.
{: .text-justify}

This third part changes the unit of analysis: from schools and maps to student trajectories. It compares exposed students with others who have similar observable characteristics, estimates school outcomes, and turns the limits of the evidence into concrete requirements for a transition. Three questions organise the account: what closed, what happened next, and what public policy should require.
{: .text-justify}

## Spoonful 1: what closed, and who was exposed?

### A student flow is a signal, not an administrative act

The starting point is 346 episodes administratively recorded as closures of schools that had previously enrolled students. Part II’s strict definition retains 330 exits of educational provision and sets aside annexes, possible continuities, and administrative changes. The follow-up considers students enrolled in the preceding year and observes their subsequent records whenever the time window allows it.
{: .text-justify}

Students’ destinations help review that classification. A highly concentrated transfer to another school may be consistent with a merger, institutional continuity, an accessible alternative, or coincident family choices. The flow proves none of these explanations. Changing an episode’s identity requires a directory, a formal act by the provider, or another independent institutional source.
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

The table classifies each of the 346 episodes once under the reporting rule. The **45 concentrated-destination alerts** are a different cut and overlap those categories; they must not be added to them. Nor did they produce automatic changes: this phase has **zero independent institutional confirmations**, and the 330 strict closures remain the reference set.
{: .text-justify}

### From documentary certainty to the Data-Inferred School Closure Rule (RCID v1)

Confirming a legal-administrative closure requires reviewing official records, recognition decrees, and provider filings. When analysing twenty years of massive panels without a physical dossier for every school, however, we must make transparent a falsifiable, reproducible empirical rule that separates raw directory exits from a genuine cessation of educational provision with student displacement. That is the **Data-Inferred School Closure Rule (`RCID v1`)**, applied uniformly across all three instalments of this series through three nested strata (D0 ⊃ D1 ⊃ D2):
{: .text-justify}

- **D0 (raw administrative or activity exit):** the school records positive enrolment in t−1, drops to zero enrolment in t, and records no teaching activity in t+1 or subsequent years (or appears with a closed status in the official directory).
- **D1 (strict closure of educational provision):** subset of D0 that purges school-level false closures—subsequent reopenings, RBD code changes with site continuity, partial annexes or branches, and candidate administrative continuities.
- **D2 = RCID v1 (data-inferred closure purged by student flow):** subset of D1 that requires observing at least 5 trackable students in t−1 and removes concentrated absorptions or de facto mergers in which a single receiving school absorbs at least **70%** of relocated students and at least **15 students** in t (with a clean t+1 variant when the post-closure window is fully observed).

{: .table-caption}
**Table 2.** Hierarchy of the Data-Inferred School Closure Rule (`RCID v1`, D0 ⊃ D1 ⊃ D2) across all three instalments (2005–2025)

| Rule stratum | Historical window (2005–2015) | Recent window (2016–2025) | Longitudinal series (2005–2025) | What it purges and how it is used in Parts I, II, and III |
|---|---:|---:|---:|---|
| D0: raw administrative or activity exit | 1,635 | 346 | 1,981 | Enrolment cessation in t; contrasts with the 2,069 raw directory exits of 1992–2012 in Part I. |
| D1: strict closure of educational provision | 1,477 | 330 | 1,807 | Purges 158 historical reopenings or continuities and 16 recent candidate continuities or annexes (Part II baseline). |
| D2 = RCID v1 (conservative, includes right-censored 2025) | 1,382 | 296 | 1,678 | Further purges 95 historical absorptions and 34 recent concentrated absorptions or flow alerts (≥ 70% and ≥ 15 students). |
| D2 = RCID v1 (clean with observed t+1 window) | 1,382 | 266 | 1,648 | Requires observing the full t+1 year (excludes the 30 right-censored 2025 episodes); main baseline for Part III. |
{: .table--compact .table--scroll}

Separating D1 and D2 avoids conflating a full reorganisation or single-receiver absorption with forced student dispersion. In Part II, moving from the 330 strict closures (D1) to the 296 under `RCID v1` (D2) lowers median pre-closure enrolment from 44 to 39 students in t−2 and from 34 to 31 in t−1 (36 and 27 in the clean 266-closure variant) and leaves the adjusted SIMCE difference at +0.017 standard deviations (17 supported closures, 95% interval crossing zero). In this Part III, the primary specification excludes concentrated-flow alerts (operating on the clean D2 stratum) and explicitly contrasts sensitivity to including or excluding receiving schools.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-1-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/sample-flow-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/sample-flow-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/sample-flow-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/sample-flow-en-dark.svg' | relative_url }} 1600w" alt="Two lanes summarise support for the 2016 to 2019 post-pilot re-estimation. Of 64 historical episodes before support screening, 63 retain at least one comparable stratum and one is fully excluded. Of 6,581 exposed student-cohort observations, 391 are excluded and 6,190 remain. The support universe contains 82,753 comparison student-cohort observations; final samples differ by outcome." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 1</strong> — How the comparable sample is formed for the post-pilot re-estimation. Aggregate counts precede outcome-specific eligibility, and their units must not be added together. <span class="figure-source">Source: author’s calculations from the v3.1 post-pilot re-estimation.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/sample-flow-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

The figure separates the universe, episodes, and observations. A “student-cohort observation” counts one student within one closure cohort; it is not necessarily a different person throughout the full dataset. This distinction prevents apparent scale from being mistaken for more independent cases than the analysis actually contains.
{: .text-justify}

The audit does not turn student flows into a list of schools to close or merge either. Public outputs remain aggregated: they contain no identifiers, names, addresses, coordinates, or candidate lists. If a future review corrects a Part II episode, it should make the source and version supporting the change visible.
{: .text-justify}

## Spoonful 2: what happened after closure?

### Two primary outcomes and an uncomfortable conclusion

The re-estimation focuses on closures from 2016 to 2019 and compares trajectories before and after each episode. Identity alerts and receiving schools are excluded from the main comparison. The uncertainty calculation recognises that students from the same closure share conditions; an additional check accounts for the same student appearing more than once in the records.
{: .text-justify}

### Are we comparing like with like?

The design uses differences in differences: it measures how much each group changed, then subtracts those changes. Before that double subtraction, it groups students with the same year, sex, region, provider type, rurality, education level, and starting grade. Put simply, it tries to compare like with like using the characteristics we can observe. That helps, but it cannot reveal characteristics that never entered the data, such as household income, parental education, special educational needs, or the closure-announcement date.
{: .text-justify}

{: .table-caption}
**Table 3.** Observed similarity before closure in the weighted sample

| Baseline characteristic | Exposed students | Comparison group | Reading |
|---|---:|---:|---|
| Mean age | 11.70 years | 11.70 years | Standardised difference: 0.000. |
| Mean attendance | 90.93% | 91.68% | Standardised difference: −0.079. |
| Mean mark | 5.62 | 5.67 | Standardised difference: −0.072. |
| Valid attendance and grade record | 76.8% | 96.2% | Coverage gap: −19.4 pp. |
{: .table--compact .table--scroll}

The observed differences are small after weighting, but performance-record availability is not: records are missing far more often among exposed students. Age is observed for the full sample. Attendance and marks, by contrast, can be compared only among students with those records; coverage is 76.8% among exposed students and 96.2% in the comparison group. This gap warns that a relevant share of exposed students is less visible. The table therefore certifies neither random assignment nor full sociodemographic comparability: it shows similarity in what is observed while exposing record selection capable of changing the conclusion.
{: .text-justify}

To audit more deeply whether exact matching at G−1 compares truly equivalent trajectories, we incorporate eleven additional baseline descriptors of children and adolescents (NNA) and their prior institutional environment from Preferential School Subsidy (SEP), directory, enrolment, and performance records between G−3 and G−1. The diagnostic reveals two simultaneous sides: while individual socioeconomic eligibility (`PRIORITARIO_ALU` and `PREFERENTE_ALU`) and over-age status are nearly balanced after stratifying by level and grade, effective school SEP participation, Full School Day (JEC) provision, inter-municipality commuting, and prior school mobility exhibit structural asymmetries that basic demographic matching does not remove.
{: .text-justify}

{: .table-caption}
**Table 4.** Extended baseline characterisation of children and adolescents (NNA) at G−1 (2016–2019 cohorts, 6,190 exposed and 82,753 controls)

| Baseline descriptor at G−1 | Exposed students | Comparison group | Gap (pp) | Substantive reading for identification |
|---|---:|---:|---:|---|
| Priority SEP student (`PRIORITARIO_ALU`) | 30.68% | 32.32% | −1.64 | Close balance in priority socioeconomic vulnerability after stratification. |
| Preferential SEP student (`PREFERENTE_ALU`) | 23.83% | 23.26% | +0.57 | Similarity in the second tier of SEP eligibility. |
| Total SEP eligibility (priority or preferential) | 54.51% | 55.58% | −1.07 | Individual eligible socioeconomic composition is comparable at G−1. |
| Effective SEP beneficiary (`BEN_SEP`) | 37.63% | 48.58% | −10.95 | Despite equal eligibility, exposed students receive lower effective SEP coverage. |
| Origin school with SEP agreement (`CONVENIO_SEP`) | 45.17% | 55.23% | −10.06 | Closures cluster among providers with lower institutional SEP participation. |
| Origin school with Full School Day (JEC) | 53.97% | 72.51% | −18.54 | Prior supply asymmetry: lower full-day provision before closure. |
| Inter-municipality commuting (residence ≠ school municipality) | 38.59% | 29.99% | +8.60 | Higher share of students already commuting across municipalities before closure. |
| Over-age ≥ 1 year relative to grade norm | 33.86% | 33.86% | 0.00 | Exact balance induced by matching on age, level, and grade at G−1. |
| Severe over-age ≥ 2 years relative to grade | 8.32% | 8.32% | 0.00 | No baseline difference in accumulated lag of two or more years. |
| Chronic absenteeism (< 85% among valid records) | 13.99% | 11.14% | +2.85 | Greater prior attendance fragility among students with valid records at G−1. |
| Prior grade repetition at G−1 (among valid records) | 5.49% | 4.48% | +1.01 | Slightly higher non-promotion in the year immediately preceding closure. |
| School switch between G−2 and G−1 | 26.57% | 16.53% | +10.04 | Over a quarter of exposed students were already switching schools before closure. |
| At least one school switch between G−3 and G−1 | 47.04% | 30.52% | +16.52 | Nearly half of exposed students experienced prior mobility: a signal of pre-existing fragility. |
{: .table--compact .table--scroll}

This extended profile reinforces why an adjusted difference must not be read mechanically as a pure effect of closure: although exposed NNA and their controls share the same age, the same prior accumulated grade lag, and a nearly identical share of priority and preferential students (54.51% versus 55.58%), exposed students attended schools with lower SEP agreement coverage (−10.06 pp) and Full School Day coverage (−18.54 pp), and nearly half (47.04% versus 30.52%) had already switched schools at least once between G−3 and G−1. Part of the trajectories was already under strain before the school left the register.
{: .text-justify}

Of the 63 episodes that retain general support in Figure 1, each outcome uses only the cohorts in which its follow-up window and annual record are observable: 62 episodes for the two primary outcomes and 58 for attendance and marks. The first outcome compares, before and after, the share of students with no enrolment record for two consecutive years. I do not call this dropout: absence from the school register does not, by itself, reveal the reason or destination. The exposed group’s change exceeds the comparison group’s by **+0.63 percentage points**, with a conservative 95% interval from **−0.77 to 2.03 points**. The estimate uses 3,666 exposed observations and 49,944 comparison observations from 62 closure episodes.
{: .text-justify}

The second outcome compares, before and after, the share with no enrolment or enrolment below the expected grade one year later, summarised as **progression failure or grade lag**. The exposed group’s change exceeds the comparison group’s by **+5.29 percentage points**, and its conservative interval runs from **2.08 to 8.51 points**. The estimate uses 4,815 exposed observations and 65,538 comparison observations in 62 closure episodes. But progression is not observed for everyone. Under extreme scenarios for those missing records, the bounds of **−1.15 to 10.98 percentage points** cross zero. That is the uncertainty that governs the public interpretation.
{: .text-justify}

{: .table-caption}
**Table 5.** Post-pilot re-estimation: observed differences, not causal effects

| Outcome | Estimated difference | Conservative 95% interval | Decisive condition |
|---|---:|---:|---|
| Persistent non-enrolment for two years | +0.63 pp | [−0.77, 2.03] | It is not dropout; the estimable pre-event trend rests on few episodes. |
| Progression failure or grade lag: no enrolment or below the expected grade one year later | +5.29 pp | [2.08, 8.51] | Missing-data bounds: [−1.15, 10.98] pp. |
| Attendance | −1.15 points | [−2.40, 0.10] | Exploratory; requires valid attendance and observable final pass/repeat status. |
| Average mark | −0.06 | [−0.14, 0.01] | Exploratory; only among students with observable performance. |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-2-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }} 1600w" alt="Inconclusive post-pilot re-estimation of two primary outcomes. Persistent non-enrolment is estimated at 0.63 percentage points, with an interval from minus 0.77 to 2.03; the different sample including receiver schools gives 0.71, from minus 0.69 to 2.12. Progression failure or grade lag is estimated at 5.29 points, from 2.08 to 8.51; the different receiver-school sample gives 5.09, from 1.94 to 8.23. Missing-data bounds span minus 1.15 to 10.98 points. These are not confirmed causal effects." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 2</strong> — Inconclusive post-pilot re-estimation, not causal effects. The progression interval does not cross zero, but its missing-data bounds do; overlap with the pilot and unobserved assumptions prevent a causal interpretation. <span class="figure-source">Source: author’s calculations from the v3.1 post-pilot re-estimation.</span> <span class="figure-data">Accessible tabular data: <a href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-data.csv' | relative_url }}">estimates</a> and <a href="{{ '/assets/images/tesis-post3/missingness-bounds-data.csv' | relative_url }}">missing-data bounds</a>.</span></figcaption>
</figure>

Attendance and average marks add context; they do not change the main conclusion. They are observed only when a valid annual record exists; for attendance, the value must also be between 1 and 100 and final status must be pass or repeat in both periods. That requirement narrows the analytical sample to **3,871 exposed observations** across **58 episodes** (compared with 63,591 comparison observations for attendance and 63,596 for marks), covering **62.5%** of exposed support versus **76.8%** in the comparison group. These rows are therefore **exploratory and conditional**; they do not describe the full exposed population. Missing-data bounds were calculated only for progression and do not incorporate sampling uncertainty. No equivalent bounds were estimated for attendance or average marks, so their uncertainty from selection remains unresolved.
{: .text-justify}

The 62 episodes behind the two primary outcomes yield 61 nominal degrees of freedom, but their contributions are unequal. After accounting for that concentration, they amount to approximately **21.1 effective episodes** for non-enrolment and **21.9** for progression; across the 58 episodes with valid performance records, attendance and grades fall to **17.7**. Clustered intervals and the *wild cluster* check better protect uncertainty, but they cannot create independent episodes or repair selection and the missing counterfactual.
{: .text-justify}

“Effective episodes” can be understood as a meeting room. Although 62 schools are present, a few contribute a disproportionate share of students and speak more loudly in the average. The conversation is therefore less like hearing 62 independent voices and more like hearing about 21 at a balanced volume. The calculation neither removes schools nor changes the estimate; it shows how much independent information supports the interval. The exploratory outcomes rest on an even smaller base, which is another reason not to turn attendance or marks into causal headlines.
{: .text-justify}

Nor is it enough for the groups to resemble one another in the available columns. The double difference would be causal only if both groups would have followed comparable trajectories without closure. That alternative path is unobserved. Baseline similarity, clustered intervals, and sensitivity checks reduce specific rival explanations, but they cannot rule out an anticipated decision, prior deterioration, or selective record loss as explanations for part of the difference.
{: .text-justify}

The result remains inconclusive. The analysis rules were set after observing the pilot, there is no announcement date with which to separate anticipation from operation, and some pre-event tests rest on few episodes. In Figure 2, the bar that includes receiving schools within the comparison group yields **+0.71 percentage points** for non-enrolment ([−0.69, 2.12]) and **+5.09 points** for progression failure or grade lag ([1.94, 8.23]), on different samples (3,670 exposed observations versus 59,613 controls, and 4,822 versus 79,058): variants that include receiving schools or local markets change sample composition and are neither mechanical versions of the same comparison nor a substitute for the missing-data bounds of **−1.15 to 10.98 points**.
{: .text-justify}

What evidence could change this reading? A stronger evaluation would need to set the analysis before observing its results, confirm each closure through an institutional source, and measure the same outcome before and after the episode. It would also have to show that conclusions survive alternative receiving-school definitions, dependence across students and episodes, and loss to follow-up. Conversely, claiming that there is no cost would require defining in advance what difference is socially negligible and estimating it precisely enough; a confidence interval that includes zero does not accomplish that task.
{: .text-justify}

The urban–rural split remains exploratory. The rural sample is much smaller, and comparing several groups at once increases the chance of highlighting a fortuitous difference. Before turning that signal into a territorial recommendation, the analysis needs more episodes, network travel times, and transport data, because the same distance can imply very different access conditions.
{: .text-justify}

### Why was 2016–2019 chosen, and what does the full 2005–2024 series show?

A legitimate question when reading the primary specification is why the estimation focused on the **2016–2019** cohorts rather than every available year between **2004 and 2025**. The original choice was neither arbitrary nor driven by searching for a particular sign: it followed from four simultaneous administrative-data constraints. First, the official school-status field (`ESTADO_ESTAB`) entered the MINEDUC directory only in the 2015 snapshot, making **2016** the first cohort in which the contemporaneous transition to closed status is observed directly year over year. Second, requiring up to nine years of pre-event history (G−9 to G−1) inside a panel starting in 2004 mechanically pushes cohorts with a full pre-event horizon toward the mid-2010s. Third, the **2020–2022** cohorts coincide with pandemic lockdowns and exceptional promotion rules during COVID-19. Fourth, the **2024–2025** cohorts are right-censored for observing two-year persistent non-enrolment (G+1 requires at least two post-closure years).
{: .text-justify}

Even so, modern staggered difference-in-differences methodology for multiple time periods (Callaway and Sant'Anna 2021; Sun and Abraham 2021; Roth et al. 2023) shows that we can and should estimate each annual cohort G = 2005…2024 separately against clean not-yet-treated controls—avoiding the negative weights of traditional two-way fixed-effects regressions—and then report the annual ranges, institutional-regime sub-aggregates, and series-wide aggregates under explicit weighting schemes. Combining historical closure records from the 2015 and 2025 directories with the `RCID v1` (D2) rule, we reconstruct all **20 annual closure cohorts from 2005 to 2024**, encompassing **1,141 empirically supported episodes**, **78,972 exposed student-cohort observations**, and **734,472 comparison observations** in exactly matched strata.
{: .text-justify}

{: .table-caption}
**Table 6.** Annual cohort estimates (G = 2005–2024), ranges, regime sub-aggregates, and full-series aggregates

| Cohort / Regime / Aggregate | Supported episodes | Exposed (N) | Controls (N) | Progression failure or grade lag (pp) | 95% CI progression (pp) | 2-year persistent non-enrolment (pp) | 95% CI non-enrolment (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cohort 2005 (initial boundary; no pre-trend at G−2) | 46 | 1,981 | 48,273 | +3.99 | [−1.38, +9.36] | +2.62 | [−0.09, +5.33] |
| Cohort 2006 (pre-SEP regime) | 60 | 2,666 | 51,310 | +7.37 | [+3.16, +11.57] | +2.71 | [+0.11, +5.32] |
| Cohort 2007 (pre-SEP regime) | 65 | 3,747 | 50,114 | +5.22 | [+2.29, +8.15] | +2.18 | [+0.45, +3.92] |
| Cohort 2008 (SEP launch) | 59 | 3,164 | 53,788 | +5.07 | [+1.71, +8.43] | +1.93 | [−0.20, +4.05] |
| Cohort 2009 (early SEP implementation) | 63 | 3,633 | 47,492 | +7.19 | [+2.82, +11.56] | +0.92 | [−0.87, +2.71] |
| Cohort 2010 (27F earthquake and network adjustment) | 88 | 4,864 | 62,719 | +5.46 | [+2.15, +8.77] | −0.41 | [−1.29, +0.46] |
| Cohort 2011 (student movement and voucher adjustment) | 98 | 6,809 | 69,927 | +4.16 | [+2.14, +6.19] | +0.62 | [−0.68, +1.91] |
| Cohort 2012 (SAC quality system rollout) | 115 | 7,674 | 67,272 | +5.41 | [+2.72, +8.09] | +0.39 | [−0.30, +1.08] |
| Cohort 2013 (SAC regime) | 109 | 5,190 | 53,681 | +7.94 | [+5.42, +10.46] | +1.45 | [−0.01, +2.91] |
| Cohort 2014 (run-up to the Inclusion Law) | 100 | 5,260 | 57,152 | +3.91 | [+1.76, +6.05] | +0.82 | [−0.02, +1.66] |
| Cohort 2015 (Law No. 20,845 Inclusion enacted) | 105 | 7,018 | 51,073 | +7.62 | [+5.02, +10.23] | +1.62 | [+0.53, +2.71] |
| Cohort 2016 (main post-pilot window) | 17 | 1,074 | 13,798 | +3.27 | [−3.51, +10.05] | −0.29 | [−1.44, +0.86] |
| Cohort 2017 (main post-pilot window) | 14 | 540 | 12,690 | +4.79 | [−2.61, +12.18] | +0.12 | [−3.19, +3.43] |
| Cohort 2018 (main post-pilot window) | 14 | 1,842 | 19,729 | +5.78 | [+2.37, +9.19] | +1.33 | [−1.84, +4.50] |
| Cohort 2019 (main post-pilot window) | 17 | 1,359 | 19,321 | +6.44 | [−0.68, +13.57] | +0.62 | [−1.89, +3.12] |
| Cohort 2020 (COVID-19 pandemic; in-person closure) | 40 | 7,839 | 20,694 | +10.64 | [−6.81, +28.09] | +1.00 | [−1.07, +3.06] |
| Cohort 2021 (COVID-19 pandemic; flexible promotion) | 18 | 661 | 8,590 | −1.18 | [−8.45, +6.08] | +2.18 | [−1.38, +5.73] |
| Cohort 2022 (post-pandemic in-person return) | 12 | 509 | 6,530 | +22.55 | [−4.07, +49.17] | +2.23 | [−2.41, +6.87] |
| Cohort 2023 (post-pandemic with complete window) | 18 | 932 | 9,546 | +15.72 | [+2.70, +28.74] | +1.52 | [−1.47, +4.51] |
| Cohort 2024 (1-year progression observed; 2-year censored in 2025) | 78 | 12,208 | 10,773 | +19.92 | [−3.83, +43.66] | 0.00 | [0.00, 0.00] |
| **Annual range (minimum to maximum; IQR P25–P75)** | **12 to 115** | **509 to 12,208** | **6,530 to 69,927** | **−1.18 to +22.55 (IQR: +4.63 to +7.70)** | **[−8.45, +49.17]** | **−0.41 to +2.71 (IQR: +0.62 to +2.05)** | **[−3.19, +6.87]** |
| **Sub-aggregate 2006–2010 (pre-SEP and early SEP)** | **335** | **18,074** | **265,423** | **+5.97** | **[+4.32, +7.62]** | **+1.24** | **[+0.47, +2.01]** |
| **Sub-aggregate 2011–2015 (SAC and Inclusion run-up)** | **527** | **31,951** | **299,105** | **+5.75** | **[+4.64, +6.85]** | **+0.90** | **[+0.44, +1.36]** |
| **Sub-aggregate 2016–2019 (main window; bounds [−1.15, 10.98] pp)** | **62** | **4,815** | **65,538** | **+5.29** | **[+2.08, +8.51]** | **+0.63** | **[−0.77, +2.03]** |
| **Sub-aggregate 2020–2022 (COVID-19 pandemic shock)** | **70** | **9,009** | **35,814** | **+10.44** | **[−4.85, +25.74]** | **+1.16** | **[−0.68, +3.01]** |
| **Sub-aggregate 2023–2024 (post-pandemic reactivation)** | **96** | **13,140** | **20,319** | **+19.62** | **[−2.46, +41.70]** | **+1.52** | **[−1.47, +4.51]** |
| **Full-series aggregate 2005–2024 (Callaway & Sant'Anna, exposed-weighted)** | **1,141** | **78,972** | **734,472** | **+9.11** | **[+5.34, +12.88]** | **+1.09** | **[+0.65, +1.53]** |
| **Full-series aggregate 2005–2024 (equal annual cohort weights)** | **1,141** | **78,972** | **734,472** | **+7.55** | **[+5.52, +9.57]** | **+1.24** | **[+0.75, +1.73]** |
| **Full-series aggregate 2005–2024 (inverse-variance precision; I² = 76.48%)** | **1,141** | **78,972** | **734,472** | **+5.14** | **[+4.34, +5.95]** | **+0.67** | **[+0.33, +1.00]** |
{: .table--compact .table--scroll}

<figure class="post3-figure data-visualization" id="fig-post3-4-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }} 1600w" alt="Infographic of the 2005 to 2024 staggered series under the RCID v1 rule with 1,677 closures between 2005 and 2024 and 1,141 supported episodes. Across the 20 annual cohorts, progression failure or grade lag ranges from minus 1.18 to plus 22.55 percentage points, with 5.29 points in the 2016 to 2019 window and missing-data bounds from minus 1.15 to 10.98 points. The exposed-weighted Callaway and Sant'Anna aggregate is +9.11 points, with an interval from 5.34 to 12.88 and Manski bounds from +0.43 to +16.21 points." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 3</strong> — Full 2005–2024 series audit by annual cohort, regime sub-aggregates, Callaway and Sant'Anna staggered aggregation, and extended NNA baseline characterisation at G−1. In the last cohort row of Table 6, the 2024 cohort records 0.00 in the two-year column only as a right-censored cell marker (requires 2026). <span class="figure-source">Source: author’s calculations from the 2004–2025 panel and the audited v1 full-series artifact.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

Table 6 and Figure 3 dispel any suspicion that the **2016–2019** window was opportunistically selected and reveal three first-order regularities. First, across **2006 to 2019**—fourteen consecutive pre-pandemic cohorts—the adjusted difference in progression failure or grade lag is consistently positive and remarkably stable across institutional regimes: **+5.97 percentage points** in **2006–2010** ([+4.32, +7.62]), **+5.75 points** in **2011–2015** ([+4.64, +6.85]), and **+5.29 percentage points** in **2016–2019** ([+2.08, +8.51], with missing-data bounds from **−1.15 to 10.98 points**). In fact, the 2016–2019 window has a **more conservative** point estimate than the two preceding five-year periods, but wider sampling uncertainty because fewer closures occurred per year (62 episodes versus 335 and 527). Second, across the full **2005–2024** series, the exposed-weighted Callaway and Sant'Anna staggered aggregate reaches **+9.11 percentage points** ([+5.34, +12.88]) and its Manski missing-data bounds (**[+0.43, +16.21] points**) **do not cross zero**, whereas inverse-variance precision weighting—which downweights the high dispersion of the pandemic and post-pandemic years (I² = 76.48%)—converges to **+5.14 points** ([+4.34, +5.95]). Third, for two-year persistent non-enrolment (19 evaluable cohorts from 2005 to 2023, with 66,764 exposed and 723,699 controls), the exposed-weighted aggregate is **+1.09 percentage points** ([+0.65, +1.53]), consistent with the historical order of magnitude. Even so, as Table 4’s NNA characterisation and a mean pre-trend difference at G−2 of −1.49 points ([−2.27, −0.71]) in the long series show, these aggregated differences describe an **adjusted before-and-after gap** in the presence of pre-existing fragility and mobility, not a randomised experiment.
{: .text-justify}

### What the literature adds—and what it does not

The directed review used here did not find a universal sign. The studies it includes report initial disruption, later recovery, persistent losses for some groups, and better outcomes when the destination offers stronger conditions (Engberg et al. 2012; Brummet 2014; Beuchert et al. 2018; Steinberg and MacDonald 2019). In receiving schools, moreover, a decline in school-level averages may reflect a change in student composition rather than harm to incumbent pupils (Taghizadeh 2020), while limited seats in effective schools constrain how much reassignment can improve achievement (Abdulkadiroğlu, Pathak, and Walters 2026). At the secondary level, some studies find risks to graduation or postsecondary access even when test scores recover (Larsen 2020; Bross, Harris, and Liu 2023; Kim 2024).
{: .text-justify}

Chile does not support a mechanical transfer of findings either. Grau, Hojman, and Mizala (2018) estimate increases in grade repetition and dropout for a different period and design; Iocco (2024), in a preprint, finds an average achievement result close to zero with heterogeneity by destination. Differences in outcome, cohort, treatment, and method prevent the 5.29-point estimate—whose missing-data bounds run from −1.15 to 10.98 points—from being read as either a replication or a refutation of those studies.
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

An inconclusive result does not require passivity. It already identifies what information is missing before a school network is reorganised and what should be followed afterwards. Falling enrolment may open a diagnosis; on its own, it recommends neither a merger nor a closure.
{: .text-justify}

<figure class="post3-figure data-visualization" id="fig-post3-3-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/territorial-audit-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/territorial-audit-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/territorial-audit-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/territorial-audit-en-dark.svg' | relative_url }} 1600w" alt="Of 346 episodes, 339 have a complete three-year pre-event window and 323 have five. The classification contains 266 with no contradictory signal, 15 continuity candidates, 35 unresolved alerts, and 30 episodes without complete later follow-up. There are 45 post-event alerts and zero institutional confirmations; automated processing supports observation only." loading="lazy" decoding="async">
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

The table and Figure 4—where the 30 closures from 2025 with incomplete follow-up are labelled as right-censored because their subsequent year has not yet elapsed—shift the burden of proof. An authority should not assume continuity because another school is nearby or because several students reached the same destination. It should demonstrate that places, safe access, receiving resources, and sufficient support exist, then observe whether the transition worked for displaced students and for those already attending the receiving school.
{: .text-justify}

Local Public Education Services (SLEP) and the School Admission System (SAE) are not automatic causal instruments either. They may modify coordination, destinations, or receiving load, but they also directly affect resources, vacancies, and trajectories; this breaks the requirement that an instrument operate only through closure. Falling enrolment, school size, and local shocks fail for similar reasons: they may predict closure while also affecting outcomes. Without a documented administrative rule or lottery that satisfies relevance, exclusion, monotonicity, no anticipation, and limited interference, an instrumental-variable estimate would create apparent precision rather than identification. No instrumental-variable regression is therefore run in this version.
{: .text-justify}

## Closing: following trajectories changes the policy question

Part I reconstructed what we knew; Part II established which schools closed and what provision appeared nearby. This third part follows students and shows why the map was insufficient: destination is not continuity, and observed continuity is not a counterfactual.
{: .text-justify}

The most visible result—a change 5.29 percentage points larger among exposed students than in the comparison group—must remain beside its bounds of **−1.15 to 10.98 points**. Separating them would create a certainty the analysis does not possess. This instalment makes a more demanding contribution: turning massive administrative records into verifiable questions that can protect transitions without fabricating a causal answer.
{: .text-justify}

An inconclusive result does support precautionary safeguards today: do not treat proximity as continuity, do not reorganise a network without verifying places and support, and follow every student through the transition. These safeguards are not estimated effects of those decisions. They also require publishing what is missing and correcting the decision if alerts show that the destination was not prepared.
{: .text-justify}

The next analytical step is not to search across models until an attractive number appears. It is to obtain announcement dates, institutional evidence, receiving-school capacity and accessibility, less selective observation, and an independent evaluation. Only then can the cost of closure be better distinguished from the deterioration that preceded it and the conditions students encountered at their destinations.
{: .text-justify}

### Transparency and scope of the sources

The thesis and this extension are my own work; they are not an independent replication. I also coauthored the 2014 working paper. That relationship may favour inherited hypotheses, so the historical reconstruction and the current reanalysis remain separate and any discrepancies must stay visible.
{: .text-justify}

I received no funding for this work and declare no conflicts of interest. My sole institutional affiliation is Chile’s Ministry of Social Development and Family, which did not fund, commission, supervise, or review this work; its positions are not represented by these conclusions. I used artificial-intelligence assistants to support programming, literature search, quality control, prose review, and adversarial review. The methodological and editorial decisions, source verification, and responsibility for the claims and results are mine.
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

Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://doi.org/10.1016/j.jeconom.2023.03.008) *Journal of Econometrics* 235 (2): 2218–44.

Steinberg, Matthew P., and John M. MacDonald. 2019. [“The Effects of Closing Urban Schools on Students’ Academic and Behavioral Outcomes: Evidence from Philadelphia.”](https://doi.org/10.1016/j.econedurev.2018.12.005) *Economics of Education Review* 69: 25–60.

Sun, Liyang, and Sarah Abraham. 2021. [“Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects.”](https://doi.org/10.1016/j.jeconom.2020.09.006) *Journal of Econometrics* 225 (2): 175–99.

Taghizadeh, Jonas Larsson. 2020. [“Are Students in Receiving Schools Hurt by the Closing of Low-Performing Schools? Effects of School Closures on Receiving Schools in Sweden 2000–2016.”](https://doi.org/10.1016/j.econedurev.2020.102020) *Economics of Education Review* 78: 102020.

</div>
