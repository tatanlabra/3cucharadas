---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extending my thesis in three spoonfuls (part III): what student trajectories show after a school closure"
subtitle: "In all 19 cohorts, grade lag or exit from the register rose more among students who lost their school than among their peers. I cannot yet attribute that gap to the closure."
date: 2026-10-23 10:00:00 -0300
last_modified_at: 2026-10-31 18:00:00 -0300
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

To answer it, I followed **78,972 student trajectories** in **1,141 regular schools** that closed between 2005 and 2024, each against comparable students from schools that stayed open. The result supports two readings that are worth holding together. First: in the **19 cohorts** that can be measured, progression failure or grade lag among students who lost their school rose more than among their peers, and that gap is positive in all 19. Second: I still cannot attribute that gap to the closure, because those schools were already more fragile and their students more mobile.
{: .text-justify}

In the window I fixed before looking at the full series, 2016–2019, the **share with no enrolment or enrolment below the expected grade one year later—what I call “progression failure or grade lag”—rose 5.29 percentage points more among exposed students than in the comparison group**, with a conservative 95% confidence interval from **2.08 to 8.51 points**. Because next-year progression is not observed for every student, however, assumption-free missing-data bounds (Manski 2003) span **−1.15 to 10.98 percentage points**. Because that range crosses zero, the main-window result is **inconclusive**: on its own, it demonstrates neither harm, benefit, nor the absence of an effect. In scale: the rate went from 2.2% to 15.8% among exposed students, when their controls implied 10.6%.
{: .text-justify}

This exercise reports a **post-pilot re-estimation** across **79,709,054 enrolment records** and **73,873,835 performance records** from 2004 to 2025. Here is the paradox: in the primary window, all those millions of records weigh as much as about **21 or 22 independent schools**, because a few closures hold a large share of the students. That scale reveals individual trajectories that school-level averages hide, but it cannot manufacture the counterfactual—what would have happened to those same children and adolescents (NNA) had their school stayed open—required for a causal claim.
{: .text-justify}

<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->
<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->

[Part I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) reconstructed the historical evidence and separated the findings that held up. [Part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) verified which schools closed in the recent decade and showed that the nearest school is rarely the main destination. This third instalment shifts from buildings to student trajectories in three steps: **what actually closed**, **what happened next to students**, and **how to protect a school transition in practice**.
{: .text-justify}

**Update of 31 October 2026.** A self-audit, reviewed by two other models, led me to correct this instalment. I corrected the description of the closure rule (10-student and destination-concentration thresholds) and replaced a fixed-effect average with a random-effects one. I removed a pre-trend figure that had no reproducible support. I added the base rate, the universe that falls outside the analysis, and a more cautious reading of missing records, and I made explicit that sensitivity to prior trends remains pending. The main result does not change: it is still inconclusive.
{: .notice--warning .text-justify}

**Quick guide.** I call **G** the first year in which the school has no enrolment; **G−1** is its last open year and **G+1** the following one. For grade progression, “before” is measured two years before closure (G−2) and “after” at G+1. **pp** are percentage points; **RBD** is each school's code; **SEP**, the Preferential School Subsidy; **JEC**, the Full School Day; **RCID**, the closure rule I built from the data.
{: .notice--info .text-justify}

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

Each of the 346 episodes appears once in Table 1. The **45 concentrated-destination alerts** come from a cross-cutting flow check that overlaps those categories and must not be added to them; without **independent institutional confirmations** (**zero** in this cut), the 330 strict closures remain the baseline reference.
{: .text-justify}

### From documentary certainty to a rule built from the data

In Chile, the legal closure of a school requires an exempt resolution from the regional education secretariat, but no complete public registry of those resolutions exists: I checked in Active Transparency (details in the methodological notes at the end). So I built an empirical, falsifiable rule, the **Data-Inferred School Closure Rule (RCID v1)**, which works like three successive sieves. The first detects enrolment that disappears; the second discards annexes and code changes; the third sets aside block transfers into a single school. Put simply, an entire class moving together into another building is not the same experience as families searching for places one by one. Applying RCID v1 (D2) leaves **1,648 clean closures** with an observed post-closure year across 2005–2025 (**266** in the recent window), providing a consistent starting point that avoids conflating de facto mergers with dispersed closures.
{: .text-justify}




Not all of those closures can be followed through grade trajectories. Only **1,177** had students in regular education—grades 1 to 8 of primary or 1 to 3 of secondary—and **1,141** found comparable controls. In the recent window, **145 of the 266** closures were schools offering only early-childhood education (69), only special education (57), only adult education (13), or only the final secondary grade (1), or were dominated by those offerings (5). Grade progression cannot be measured there, so this instalment speaks to regular schools, not to every closure.
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

Figure 1 distinguishes between closed schools (episodes) and “student-cohort” observations (each student counted within their closure cohort). All published information is strictly aggregated: to protect privacy, no names, addresses, or individual student or school codes are exposed.
{: .text-justify}

### Who the exposed students were

Before looking at what happened to them, it helps to know who they were. Between three years and one year before closure (G−3 to G−1), Table 2 summarises eight characteristics of children and adolescents (NNA) and their origin schools.
{: .text-justify}

{: .table-caption}
**Table 2.** Extended baseline characterisation of children and adolescents (NNA) at G−1 (2016–2019 cohorts, 6,190 exposed and 82,753 controls)

| Baseline descriptor at G−1 | Exposed students | Comparison group | Gap (pp) | Substantive reading for identification |
|---|---:|---:|---:|---|
| Priority SEP student | 30.68% | 32.32% | −1.64 | Close balance in priority socioeconomic vulnerability after matching. |
| Total SEP eligibility (priority or preferential) | 54.51% | 55.58% | −1.07 | Similar composition on this binary vulnerability measure. |
| Effective SEP beneficiary | 37.63% | 48.58% | −10.95 | Explained almost entirely by the origin school's lower SEP agreement coverage (next row). |
| Origin school with SEP agreement | 45.17% | 55.23% | −10.06 | Closures cluster among providers with lower institutional SEP participation. |
| Origin school with Full School Day (JEC) | 53.97% | 72.51% | −18.54 | Lower full-day provision in schools that subsequently close. |
| Inter-municipality commuting (residence ≠ school municipality) | 38.59% | 29.99% | +8.60 | Higher share of NNA already commuting outside their home municipality before closure. |
| Over-age ≥ 1 year relative to grade norm | 33.86% | 33.86% | 0.00 | Exact balance by construction of the G−1 matching strata. |
| At least one school switch between G−3 and G−1 | 47.04% | 30.52% | +16.52 | Nearly half of exposed students were already switching schools before closure. |
{: .table--compact .table--scroll}

The profile in Table 2 explains why caution is essential: exposed students and their controls share the same age, the same prior grade lag (33.86%), and nearly identical individual eligibility for the Preferential School Subsidy (54.51% versus 55.58%, with **30.68%** priority students), yet they attended institutionally weaker schools—with lower SEP agreement coverage (−10.06 pp) and lower Full School Day coverage (−18.54 pp)—and nearly half (**47.04%** versus 30.52%) had already switched schools during the two preceding years. Part of the school wear and family mobility was already under way before closure.
{: .text-justify}

## Spoonful 2: what happened after closure?

### Two primary outcomes and an uncomfortable conclusion

To measure what happened after closure in the **2016–2019** primary window, I follow students from the **63 supported episodes** in Figure 1 (**62 episodes** have an observable follow-up window for the two primary outcomes and **58** for attendance and marks). The first primary outcome tracks the share of students with **no enrolment record for two consecutive years**: I do not call this “dropout” because disappearing from Chile’s administrative register does not clarify whether a student left schooling altogether, moved abroad, or entered an uncovered modality. Here the exposed group’s before-and-after change exceeds the comparison group’s by **+0.63 percentage points**, with a conservative 95% confidence interval from **−0.77 to 2.03 points** (across **3,666** exposed observations and **49,944** controls).
{: .text-justify}

The second primary outcome measures the share with **no enrolment or enrolment below the expected grade one year later**, summarised as **progression failure or grade lag**. Here the before-and-after gap rises by **+5.29 percentage points** among exposed students relative to controls (conservative interval from **2.08 to 8.51 points**, across **4,815** exposed observations and **65,538** controls), yet applying **Manski bounds** (Manski 2003) to students whose progression was not recorded spans **−1.15 to 10.98 percentage points**. Those bounds work like a no-optimism stress test: they assign the worst outcome to students without a record in one group and the best outcome in the other, and then the reverse. The record is missing for **3.6%** of exposed students and **2.2%** of controls. Because that span encompasses both a slight improvement and a nearly eleven-point setback, the point estimate alone cannot support a definitive causal claim. Even so, the gap reaches zero only when missing data come more than **90%** of the way toward the assignment most benign to closure.
{: .text-justify}

To put the figure in scale: among exposed students, progression failure or grade lag rises from **2.2%** two years before closure to **15.8%** the year after. Had they followed their controls' change, they would have reached **10.6%**. The gap therefore equals **50%** more than that counterfactual and, only if it were causal, about **255 students** in the 2016–2019 window. The indicator merges two different things—leaving the register and falling behind a grade—so that figure does not separate dropout from grade repetition.
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

Attendance and average marks in Table 3 are **exploratory and conditional**: they can be measured only among students with valid annual performance records in both periods. That leaves **3,871** exposed observations across **58 episodes**, **62.5%** of exposed support, against **63,591** of the **82,753** controls for attendance (63,596 for marks). In Figure 2, the alternative bar that keeps receiving schools inside the control group yields **+0.71 percentage points** in non-enrolment ([−0.69, 2.12], across 3,670 exposed and 59,613 controls) and **+5.09 points** in progression failure ([1.94, 8.23], across 4,822 exposed and 79,058 controls): changing which schools enter the control pool alters sample composition, but does not remove the **−1.15 to 10.98 point** bounds attached to the main +5.29 pp estimate.
{: .text-justify}

One further statistical limit is best pictured as a **meeting room**. Even though 62 closed schools enter the primary estimation, a handful of large closures account for a disproportionate share of students. Listening to those 62 closures is therefore less like hearing 62 independent voices at equal volume and more like hearing **21.1 effective episodes** for non-enrolment, **21.9** for progression, and just **17.7** for attendance and marks. Likewise, splitting urban and rural closures rests on even fewer rural episodes, so territorial recommendations must wait for road-network travel times and school-transport data.
{: .text-justify}

### Is like being compared with like?

The design uses **differences in differences**, which compares two films rather than two isolated snapshots: first it pairs each student from a school that will close with control students who are identical one year before closure (G−1) in calendar year, sex, age, region, provider type, rurality, education level, and grade, and then it measures how much the first group’s trajectory changed before and after the event relative to their matched peers. Put simply, I try to compare like with like across every characteristic recorded in the data, gauging closeness through the **standardised difference** (distance measured in units of spread where zero means equality).
{: .text-justify}

On what can be observed, the groups end up nearly identical in age, attendance, and marks, with standardised differences below 0.08. But exposed students have far fewer valid annual records in the year before closure: 76.8% versus 96.2%. The detail, and what that gap can and cannot mean, is in the methodological notes.
{: .text-justify}




### What does the full 2005–2024 series show?

Even so, what happens when all twenty annual cohorts are examined from 2005 to 2024? When schools close in different years, blending them into a simple average would mistakenly use recently closed schools as if they were stable controls for later closures. Modern **staggered difference-in-differences** estimators (Callaway and Sant'Anna 2021; Sun and Abraham 2021; Roth et al. 2023) avoid that distortion by comparing each annual cohort solely against schools that have not yet closed, Missing-data bounds (Manski 2003) are also computed here; formal sensitivity to non-parallel pre-trends (Rambachan and Roth 2023) remains pending. Under the RCID v1 (D2) rule, the full series spans **20 annual cohorts**, **1,141 empirically supported episodes**, **78,972 exposed observations**, and **734,472 controls**; the year-by-year breakdown is available in the [open CSV for Figure 3]({{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}), and Table 7 in the methodological notes summarises the five institutional periods, the annual range, and three distinct ways of averaging the series.
{: .text-justify}


<figure class="post3-figure data-visualization" id="fig-post3-4-en">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }} 1600w" alt="Three-panel infographic under the RCID v1 rule with 1,141 supported episodes between 2005 and 2024. Panel A displays the 19 estimable annual cohorts for progression failure or grade lag from 2006 to 2024: all 19 point estimates are positive, ranging from 0.94 to 28.22 percentage points, with a median of 7.18 and a Callaway and Sant'Anna student-weighted aggregate of +9.11 points (interval from 5.34 to 12.88 and Manski bounds from +0.43 to +16.21 points). Panel B shows attenuation across institutional regimes from 12.15 points in 2005–2010 and 7.82 in 2011–2015 to 5.29 in 2016–2019 (with missing-data bounds from minus 1.15 to 10.98 points), 2.70 in 2020–2022, and 2.59 in 2023–2024. Panel C shows G minus 1 baseline gaps after exact matching: individual SEP eligibility is balanced (−1.07 points), whereas exposed students face lower school SEP agreements (−10.06 points), lower full-day schooling (−18.54 points), lower valid record coverage (−19.24 points), and higher prior school switching (+16.52 points)." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 3</strong> — Full 2005–2024 series under the RCID v1 rule: annual estimates (2006–2024), attenuation across institutional regimes, and NNA baseline gaps at G−1. <span class="figure-source">Source: author’s calculations from the 2004–2025 MINEDUC longitudinal panel.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

The long series (Figure 3 and Table 7) yields three takeaways:
{: .text-justify}

- **The 2016–2019 window was fixed before the long series was examined, and it is not the window with the largest gap:** it was set in the primary estimation design, and the long series was estimated afterwards. The progression gap falls from **+12.15 percentage points** in 2005–2010 and **+7.82** in 2011–2015 to **+5.29** in 2016–2019 (bounds **−1.15 to 10.98**), **+2.70** in 2020–2022, and **+2.59** in 2023–2024. That decline coincides in time with the Preferential School Subsidy (SEP), the Quality Assurance System (SAC), and the Inclusion Law, but cannot be attributed to them: the kind of schools that close also changed, the directory began recording school status in 2015, flexible promotion in 2020–2022 mechanically reduces grade lag, and the samples shrink.
- **Across the full series, all 19 estimable progression cohorts are positive however they are averaged, though with substantial heterogeneity:** weighting years by the number of affected students (Callaway and Sant'Anna) gives a mean difference of **+9.11 points** ([+5.34, +12.88]), whose Manski bounds (**+0.43 to +16.21**) barely exclude zero. With equal weight for each year it is **+7.55 points** ([+5.52, +9.57]). A random-effects model, which allows the gap to vary across periods (I² = 76.5%), gives **+6.29 points** ([+4.49, +8.09]); its prediction interval, **+0.09 to +12.49**, indicates where a new cohort's gap could fall. By regime, the bounds exclude zero in 2005–2010 and 2020–2022 but include it in 2011–2015, 2016–2019, and 2023–2024.
- **Larger sample size does not replace a randomised trial:** in the primary window, three placebo tests before closure give differences of +0.16, +0.30, and +0.40 points in progression, all with intervals that include zero. That does not prove the trajectories were parallel, and the long series has no placebos of its own yet. Exposure is also measured one year before closure: students who left before the announcement are excluded, and with prior school switching of 47.04% that selection may matter. A strict causal reading requires measuring how much the conclusion would change without parallel trends (Rambachan and Roth 2023) and with exposure fixed two years earlier. Both analyses remain pending.


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


{: .table-caption}
**Table 4.** Minimum information for deciding and evaluating a transition

| Before a decision | During the transition | After the change |
|---|---|---|
| Distinguish school, site, level, merger, and identifier change. | Assign actual places and support to each student. | Follow enrolment, attendance, progression, grades, and wellbeing. |
| Record the announcement date and community participation. | Measure travel time, accessibility, and peer continuity. | Observe students and staff already in receiving schools as well. |
| Verify capacity, staffing, and prior destination quality. | Fund receiving-school load and pedagogical continuity. | Publish alerts, corrections, responsibilities, and deadlines. |
{: .table--compact .table--scroll}

Table 4 shifts the burden of proof against a concrete procedural gap: when the Library of the National Congress asked the Official Recognition Unit of the Metropolitan Regional Secretariat what the “student relocation certificate” (*constancia de reubicación de los alumnos*) required in the voluntary-closure checklist actually entailed, the authority clarified that this requirement—absent from both the statute and Supreme Decree No. 315 of 2010—consisted solely of “having informed students of alternatives for relocating their enrolment”, without verifying whether those nearby schools had actual vacancies or whether students effectively enrolled in them (Castro Paredes 2013, p. 2 and note 1). An authority cannot assume educational continuity merely because an exiting provider handed out a list of nearby schools or because part of the student body reappeared on an enrolment roll: it must verify beforehand that real vacancies, safe transport, support for priority students, and pedagogical support exist at the receiving schools, and track every displaced student by name for at least two years.
{: .text-justify}

## Closing: following trajectories changes the policy question

Part I reconstructed the historical foundations; Part II established which schools closed and what provision existed nearby; this third part followed students beyond the map. The headline result for the recent window—a **5.29 percentage-point** rise in progression failure or grade lag—must always be read alongside its missing-data bounds of **−1.15 to 10.98 points**, and the long-series gap (+9.11 points under Callaway and Sant'Anna; +6.29 under random effects) must be read alongside the higher prior mobility and institutional fragility of closing schools.
{: .text-justify}

An inconclusive result does support precautionary safeguards today: do not treat proximity or a merely informative relocation notice as continuity, do not reorganise a network without verifying places and support, and follow every student through the transition. These safeguards are not estimated effects of those decisions. They are the minimum standard of public care while Exempt Resolutions terminating Official Recognition, announcement dates, receiving-school capacity, and complete evaluation and grade-promotion records are consolidated.
{: .text-justify}


<details markdown="1" class="post3-methods">
<summary>Methodological notes: closure rule, comparability, full series, and sources</summary>

### How a closure is defined: from documentary certainty to RCID v1

Under Chilean education law, no administrative instrument called a “closure act” (*acta de cierre*) decrees the end of a school. What legally formalises the termination or suspension of a school—through a final and enforceable decision (*acto firme y ejecutoriado*), meaning an official ruling against which no further appeals lie—is an **Exempt Resolution** (*Resolución Exenta*) issued by the respective Regional Ministerial Secretariat (SEREMI) of Education to extinguish or suspend its licence to operate (Official Recognition). That resolution operates under four legal figures: a one-year temporary recess, a tacit renunciation of Official Recognition if teaching does not resume after that recess, a total or partial voluntary renunciation of Official Recognition (**Articles 25 and 26 of Supreme Decree No. 315 of 2010 of MINEDUC**; Castro Paredes 2013), or the execution of a sanction revoking Official Recognition ordered by the Superintendency of Education (**Article 73(f) of [Law No. 20,529](https://www.bcn.cl/leychile/navegar?idNorma=1028635)**).
{: .text-justify}

Are those resolutions publicly available for every school in the country? To check empirically, I reviewed, in October 2026, the [Active Transparency Portal](https://www.portaltransparencia.cl/PortalPdT/directorio-de-organismos-regulados/?org=AJ001) of the Undersecretariat of Education (agency AJ001, section “Acts and resolutions affecting third parties”). Across the **12,509 administrative resolutions** and **4,735 sanction resolutions** published there, the pre-2018 historical repository is out of service, and between 2018 and 2025 the 16 regional secretariats record only **22 administrative resolutions** on school renunciation, recess, or closure—several of them declaring requests inadmissible for missing documentation or regularising “tacit closures” years after de facto cessation—and **21 unique sanction resolutions** revoking Official Recognition. Until that national registry is consolidated through a freedom-of-information request (**Law No. 20,285**), analysing twenty years of school history requires a transparent, falsifiable empirical rule—the **Data-Inferred School Closure Rule (RCID v1)**—that works like three successive sieves (D0 ⊃ D1 ⊃ D2):
{: .text-justify}

- **D0 (raw administrative exit):** the first sieve detects every school with positive enrolment in one year (t−1) that has no enrolment from t onward, does not reopen through 2025, and is recorded as closed in the official directory.
- **D1 (strict closure of provision):** the second sieve removes annexes or secondary sites and school database identifier (RBD) changes registered as successors from D0—that is, directory continuities.
- **D2 = RCID v1 (flow-purged data-inferred closure):** the third sieve sets aside concentrated transfers: schools with at least **10 baseline students** and **10** students tracked the following year, where a single receiving school takes at least **70%** of those relocated, with a destination concentration index (HHI) of at least **0.50** and the same main destination in t and t+1. These are de facto merger candidates that call for documentary review, not proof of a merger.

{: .table-caption}
**Table 5.** Hierarchy of the Data-Inferred School Closure Rule (RCID v1, D0 ⊃ D1 ⊃ D2) across all three instalments (2005–2025)

| Rule stratum | Historical window (2005–2015) | Recent window (2016–2025) | Longitudinal series (2005–2025) | What it purges and how it is used in Parts I, II, and III |
|---|---:|---:|---:|---|
| D0: raw administrative or activity exit | 1,635 | 346 | 1,981 | Enrolment cessation in t; contrasts with the 2,069 raw directory exits of 1992–2012 in Part I. |
| D1: strict closure of educational provision | 1,477 | 330 | 1,807 | Purges 158 historical annexes, sites, or RBD successors and 16 recent directory continuities (Part II baseline). |
| D2 = RCID v1 (conservative, includes right-censored 2025) | 1,382 | 296 | 1,678 | Further purges 95 historical absorptions and 34 recent concentrated absorptions or flow alerts (≥ 10 baseline and assigned students, ≥ 70% to the main destination, and HHI ≥ 0.50). |
| D2 = RCID v1 (clean with observed t+1 window) | 1,382 | 266 | 1,648 | Requires observing the full t+1 year (excludes the 30 right-censored 2025 episodes); main baseline for Part III. |
{: .table--compact .table--scroll}

Figure 4 summarises the coverage of the territorial audit of the 346 episodes in Table 1: how many have enough prior history and how many flow alerts remain without institutional confirmation.
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

### Comparability before closure

{: .table-caption}
**Table 6.** Observed similarity before closure in the weighted sample (2016–2019)

| Baseline characteristic | Exposed students | Comparison group | Reading |
|---|---:|---:|---|
| Mean age | 11.70 years | 11.70 years | Standardised difference: 0.000. |
| Mean attendance | 90.93% | 91.68% | Standardised difference: −0.079. |
| Mean mark | 5.62 | 5.67 | Standardised difference: −0.072. |
| Valid attendance and grade record | 76.8% | 96.2% | Coverage gap: −19.4 pp (observed share, unweighted). |
{: .table--compact .table--scroll}

Age is observed for the full sample and matches by construction, because it is part of the exact matching. Attendance and marks, by contrast, can be compared only among students with those records; coverage is 76.8% among exposed students and 96.2% in the comparison group (a −19.4 percentage-point gap; with controls reweighted to the matching, the gap is −19.2, the figure used in Figure 3). Here a direct link to the legal framework emerges: **Article 27(2) of Supreme Decree No. 315 of 2010** (and section nine of Superintendency of Education Circular No. 1 of 2013; Castro Paredes 2013) stipulates that the regional secretariat *may rule* on a recess or renunciation request only once the school provider delivers the **evaluation and grade-promotion records (*actas de evaluación y promoción escolar*) for all students**—that is, the official end-of-year sheet certifying marks, attendance, and grade promotion. Nearly one in four exposed students (23.2% versus 3.8% of controls) lacks that sheet in the year before closure. It is tempting to read a provider abandoning the process into that, but the pattern does not confirm it on its own. **17%** of students without a record are in 4 schools that delivered none, and **35%** are in 3 schools that delivered fewer than half. That is consistent with a disorderly administrative closure, like the “tacit closures” in Active Transparency. The remaining **48%** are scattered across schools that delivered most of their records, which fits mid-year transfers or withdrawals better. Neither explanation is proven, and Table 6 certifies neither random assignment nor full sociodemographic comparability.
{: .text-justify}

### Why the primary window is 2016–2019

Focusing the primary cut on **2016–2019** was not arbitrary: the operating-status register in the official school directory was standardised from 2015 onward, observing multi-year pre-trends inside a panel starting in 2004 pushes cohorts toward the mid-2010s, **2020–2022** was disrupted by COVID-19 closures and flexible promotion rules, and **2024–2025** does not yet have two complete post-closure years to measure persistent non-enrolment.
{: .text-justify}

### The full series by regime

{: .table-caption}
**Table 7.** Summary of the full 2005–2024 series by institutional regime, annual range, and aggregation scheme (RCID v1)

| Institutional regime / Range / Aggregate | Supported episodes | Exposed (N) | Controls (N) | Progression failure or grade lag (pp) | 95% CI progression (pp) | 2-year persistent non-enrolment (pp) | 95% CI non-enrolment (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| Sub-aggregate 2005–2010 (LOCE regime and early SEP) | 521 | 36,984 | 334,062 | +12.15 | [+3.78, +20.52] | +1.21 | [+0.53, +1.90] |
| Sub-aggregate 2011–2015 (LGE and SAC rollout) | 502 | 31,512 | 260,740 | +7.82 | [+6.20, +9.41] | +1.85 | [+1.10, +2.59] |
| Sub-aggregate 2016–2019 (main window; bounds [−1.15, 10.98] pp) | 63 | 6,190 | 82,753 | +5.29 | [+2.08, +8.51] | +0.63 | [−0.77, +2.03] |
| Sub-aggregate 2020–2022 (COVID-19 pandemic and flexible promotion) | 33 | 3,272 | 42,457 | +2.70 | [−0.63, +6.03] | −0.28 | [−1.37, +0.81] |
| Sub-aggregate 2023–2024 (post-pandemic reactivation; 2024 censored at 2 years) | 22 | 1,014 | 14,460 | +2.59 | [−1.55, +6.73] | −0.93 | [−2.64, +0.78] |
| **Annual range (19 cohorts in progression; 17 in non-enrolment)** | **7 to 129** | **357 to 10,261** | **5,566 to 71,248** | **+0.94 to +28.22 (median: +7.18)** | **IQR: +3.15 to +9.62** | **−0.93 to +4.56 (median: +0.92)** | **IQR: +0.22 to +2.11** |
| **Full-series aggregate 2005–2024 (Callaway & Sant'Anna, exposed-weighted)** | **1,141** | **78,972** | **734,472** | **+9.11** | **[+5.34, +12.88]** | **+1.38** | **[+0.92, +1.85]** |
| **Full-series aggregate 2005–2024 (equal annual cohort weights)** | **1,141** | **78,972** | **734,472** | **+7.55** | **[+5.52, +9.57]** | **+1.03** | **[+0.56, +1.50]** |
| **Full-series aggregate 2005–2024 (random effects; I² = 76.5%, τ = 2.81 pp)** | **1,141** | **78,972** | **734,472** | **+6.29** | **[+4.49, +8.09]; prediction [+0.09, +12.49]** | **+0.79** | **[+0.16, +1.42]; prediction [−1.34, +2.92]** |
{: .table--compact .table--scroll}

The N columns in Table 7 refer to support; each estimate uses the subset with an observable outcome (for example, 4,815 exposed students for progression in 2016–2019). The random-effects aggregate (Paule-Mandel, with a Hartung-Knapp interval) replaces the inverse-variance one in the previous version, which assumed a single effect common to all cohorts and, with 76.5% heterogeneity, produced an artificially narrow interval. Because cohorts share controls, even these intervals may be somewhat short.
{: .text-justify}

### Why I do not use an instrumental variable

Could that prior selection be overcome using an **instrumental variable**—that is, an external nudge akin to a lottery, such as the rollout of Local Public Education Services (SLEP), the School Admission System (SAE), or municipal demographic shocks? Not in this design: to be valid, an instrument must satisfy the **exclusion restriction**, meaning that external factor affects student progression *solely* because it triggered the school’s closure and through no other channel. Those reforms and demographic shifts simultaneously alter local resources, available seats, and everyday family school-switching decisions, violating that condition. Without a documented lottery or external administrative threshold that satisfies relevance and exclusion, forcing an instrumental model would only manufacture false precision. No instrumental-variable regression is therefore run in this version.
{: .text-justify}

### Data sources and tools

The data come from MINEDUC open data: the [school directory](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/), [enrolment by student](https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/), and [performance by student](https://datosabiertos.mineduc.cl/rendimiento-por-estudiante-2/). I processed them with [DuckDB](https://duckdb.org/) over [Apache Parquet/Arrow](https://arrow.apache.org/) files and estimated in Python with [pandas](https://pandas.pydata.org/), [SciPy](https://scipy.org/), and [statsmodels](https://www.statsmodels.org/stable/index.html), including the random-effects meta-analysis. The legal framework for SEP and the Inclusion Law is in Laws [No. 20,248](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=269001&idVersion=) and [No. 20,845](https://www.bcn.cl/leychile/Navegar?idNorma=1078172&idParte=9605200&idVersion=2222-02-02).
{: .text-justify}

</details>

### Transparency and scope of the sources

The original thesis and this extension series are my own work, as is my coauthorship of the 2014 working paper; they therefore do not constitute an independent external replication, and they keep the historical reconstruction separate from the current re-estimation. I received no external funding and declare no conflicts of interest. My sole institutional affiliation is Chile’s Ministry of Social Development and Family, which did not fund, commission, or review this analysis; the views and conclusions are my sole responsibility. I used artificial-intelligence assistants to support reproducible programming, literature search, statistical validation, and editing; all methodological decisions and factual verifications are my own. The analysis code lives in a private thesis repository and is not yet public; the aggregate figures behind each chart are in the open CSV files that accompany it.
{: .text-justify}

---

## References

<div class="post-references" markdown="1">

Abdulkadiroğlu, Atila, Parag A. Pathak, and Christopher R. Walters. 2026. [“Who Gets What in Education: Can School Matching Improve Student Achievement?”](https://doi.org/10.3386/w34936) NBER Working Paper 34936.

Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen, and Nina Smith. 2018. [“The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?”](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47.

Bross, Whitney, Douglas N. Harris, and Lihan Liu. 2023. [“The Effects of Performance-Based School Closure and Restart on Student Performance.”](https://doi.org/10.1016/j.econedurev.2023.102368) *Economics of Education Review* 94: 102368.

Brummet, Quentin. 2014. [“The Effect of School Closings on Student Achievement.”](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–24.

Callaway, Brantly, and Pedro H. C. Sant'Anna. 2021. [“Difference-in-Differences with Multiple Time Periods.”](https://doi.org/10.1016/j.jeconom.2020.12.001) *Journal of Econometrics* 225 (2): 200–230.

Castro Paredes, Luis. 2013. [*Cierre voluntario de Establecimientos Educacionales*](https://obtienearchivo.bcn.cl/obtienearchivo?id=repositorio/10221/20674/5/Cierre%20voluntario%20de%20Establecimientos%20Educacionales_v2.pdf). Parliamentary Technical Advisory Report, Library of the National Congress of Chile (BCN), December 12, 2013.

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
