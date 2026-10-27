---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extending my thesis in three spoonfuls (part III): what student trajectories show after a school closure"
subtitle: "Following students makes the transition observable, but still cannot cleanly separate closure from trajectories that were already changing."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-10-26 23:20:00 -0300
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
**Table 2.** Observed similarity before closure in the weighted sample

| Baseline characteristic | Exposed students | Comparison group | Reading |
|---|---:|---:|---|
| Mean age | 11.70 years | 11.70 years | Standardised difference: 0.000. |
| Mean attendance | 90.93% | 91.68% | Standardised difference: −0.079. |
| Mean mark | 5.62 | 5.67 | Standardised difference: −0.072. |
| Valid attendance and grade record | 76.8% | 96.2% | Coverage gap: −19.4 pp. |
{: .table--compact .table--scroll}

The observed differences are small after weighting, but performance-record availability is not: records are missing far more often among exposed students. Age is observed for the full sample. Attendance and marks, by contrast, can be compared only among students with those records; coverage is 76.8% among exposed students and 96.2% in the comparison group. This gap warns that a relevant share of exposed students is less visible. The table therefore certifies neither random assignment nor full sociodemographic comparability: it shows similarity in what is observed while exposing record selection capable of changing the conclusion.
{: .text-justify}

Of the 63 episodes that retain general support in Figure 1, each outcome uses only the cohorts in which its follow-up window and annual record are observable: 62 episodes for the two primary outcomes and 58 for attendance and marks. The first outcome compares, before and after, the share of students with no enrolment record for two consecutive years. I do not call this dropout: absence from the school register does not, by itself, reveal the reason or destination. The exposed group’s change exceeds the comparison group’s by **+0.63 percentage points**, with a conservative 95% interval from **−0.77 to 2.03 points**. The estimate uses 3,666 exposed observations and 49,944 comparison observations from 62 closure episodes.
{: .text-justify}

The second outcome compares, before and after, the share with no enrolment or enrolment below the expected grade one year later, summarised as **progression failure or grade lag**. The exposed group’s change exceeds the comparison group’s by **+5.29 percentage points**, and its conservative interval runs from **2.08 to 8.51 points**. The estimate uses 4,815 exposed observations and 65,538 comparison observations in 62 closure episodes. But progression is not observed for everyone. Under extreme scenarios for those missing records, the bounds of **−1.15 to 10.98 percentage points** cross zero. That is the uncertainty that governs the public interpretation.
{: .text-justify}

{: .table-caption}
**Table 3.** Post-pilot re-estimation: observed differences, not causal effects

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
  <figcaption><strong>Figure 3</strong> — Coverage and limits of the territorial audit. Longitudinal follow-up and flow alerts cannot replace evidence on capacity, access, demography, or institutional decisions. <span class="figure-source">Source: author’s calculations from MINEDUC directories and the longitudinal audit.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/territorial-audit-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

{: .table-caption}
**Table 4.** Minimum information for deciding and evaluating a transition

| Before a decision | During the transition | After the change |
|---|---|---|
| Distinguish school, site, level, merger, and identifier change. | Assign actual places and support to each student. | Follow enrolment, attendance, progression, grades, and wellbeing. |
| Record the announcement date and community participation. | Measure travel time, accessibility, and peer continuity. | Observe students and staff already in receiving schools as well. |
| Verify capacity, staffing, and prior destination quality. | Fund receiving-school load and pedagogical continuity. | Publish alerts, corrections, responsibilities, and deadlines. |
{: .table--compact .table--scroll}

The table and Figure 3—where the 30 closures from 2025 with incomplete follow-up are labelled as right-censored because their subsequent year has not yet elapsed—shift the burden of proof. An authority should not assume continuity because another school is nearby or because several students reached the same destination. It should demonstrate that places, safe access, receiving resources, and sufficient support exist, then observe whether the transition worked for displaced students and for those already attending the receiving school.
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

Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. [“Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?”](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203.

Grau, Nicolás, Daniel A. Hojman, Cristián Labra, and Alejandra Mizala. 2014. [“Destructive Creation: School Turnover and Educational Attainment.”]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}) Working Paper 396, Universidad de Chile.

Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. [“School Closure and Educational Attainment: Evidence from a Market-Based System.”](https://doi.org/10.1016/j.econedurev.2018.05.003) *Economics of Education Review* 65: 1–17.

Iocco, Maria Pia. 2024. [“Impact of Planned School Closures on Academic Performance: Evidence from Chile.”](https://doi.org/10.2139/ssrn.4808834) SSRN preprint.

Kim, Jeonghyeok. 2024. [“The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes.”](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963.

Larsen, Matthew F. 2020. [“Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment.”](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980.

Steinberg, Matthew P., and John M. MacDonald. 2019. [“The Effects of Closing Urban Schools on Students’ Academic and Behavioral Outcomes: Evidence from Philadelphia.”](https://doi.org/10.1016/j.econedurev.2018.12.005) *Economics of Education Review* 69: 25–60.

Taghizadeh, Jonas Larsson. 2020. [“Are Students in Receiving Schools Hurt by the Closing of Low-Performing Schools? Effects of School Closures on Receiving Schools in Sweden 2000–2016.”](https://doi.org/10.1016/j.econedurev.2020.102020) *Economics of Education Review* 78: 102020.

</div>
