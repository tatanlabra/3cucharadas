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

When a school closes, finding another building is only the beginning. A family needs to know whether a place really exists, whether the journey is manageable, and whether its child remains enrolled and moves up a grade. In [part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) I showed why the nearest school seldom tells us where displaced pupils actually go. Here I follow their school trajectories after closure. My question is harder: what changed relative to comparable pupils, and how much of that difference was already taking shape beforehand?

<aside class="notice--primary" markdown="1">
**Finding.** The estimated gap in progression failure or grade lag was positive in all 19 measurable annual cohorts. Weighted by exposed pupils, the historical aggregate was **+9.11 percentage points**; its missing-data bounds also stayed above zero, although they do not incorporate sampling uncertainty.

**Comparison.** I followed **78,972 exposed student-cohort observations** associated with **1,141 supported regular-school closures**, against **734,472 control observations**.

**Limit.** Earlier school fragility prevents me from attributing the entire gap to closure. For the recent 2016–2019 window, missing-data bounds run from **−1.15 to +10.98 points** and span zero.
</aside>

I reconstructed this history from Chilean Ministry of Education (MINEDUC) enrolment and performance records for 2004–2025. First I separate closures from possible administrative continuities. Then I compare school trajectories. Finally I ask what a public authority could check before, during, and after a transition. The [methodological annex]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}) keeps the full tables, definitions, sensitivity analyses, and sources available.

<!-- scientific-state: POST_PILOT_REESTIMATION_V3; result: INCONCLUSIVE -->
<!-- publication-readiness: READY_SCHOOL_OUTCOMES_HE_DEFERRED -->

{% include thesis-series-nav.html current=3 %}

## Spoonful 1: what closed, and who was exposed?

A school may disappear under its official code without its pupils losing the same educational provision. A site may acquire another identifier, or a whole school may move together. Counting such cases as scattered closures would change the later comparison. I therefore built the Data-Inferred School Closure Rule, **RCID v1**, as three successive filters. D0 detects administrative exits; D1 sets aside annexes and code continuities; D2 sets aside unusually concentrated transfers to one destination. A student flow is a signal to investigate, not a legal decision or proof of a merger. <span id="fig-post3-1"></span>The [exact criteria and coverage diagram]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#fig-post3-1) remain in the annex.

D2 leaves **1,648 clean closures** with a subsequent year observed in 2005–2025. Measuring grade progression requires a narrower population: **1,177** closures involved regular-education pupils in observable grades, and **1,141** had comparable controls. Those are the source of **78,972 exposed student-cohort observations** and **734,472 control observations**. These counts are observations in cohorts, not necessarily different people. Schools offering only early-years, special or adult education, or the final secondary grade cannot answer this particular progression question. Their exclusion does not imply that closure carries no cost there. The [D0/D1/D2 breakdown]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a1) traces each step.

Nor were the two groups identical before closure. In 2016–2019, **47.04%** of exposed pupils had changed schools at least once between G−3 and G−1, compared with **30.52%** of controls. Schools that would close were less likely to have an SEP agreement or a full school day. Matching brought age and prior grade lag close to balance, but it cannot erase every earlier difference. A later gap may reflect both closure and deterioration already underway. If more advantaged families left before the final open year, the observed group also starts out selected. The [full baseline table]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a3) reports coverage as well as characteristics.

The recent years illustrate why classification is more than tidying a spreadsheet. Between 2016 and 2025, **346 episodes** showed an exit after prior enrolment. D1 retained **330 strict exits of educational provision**, while D2 separated highly concentrated student flows before I measured outcomes. There were **45 concentrated-destination alerts** overlapping other categories, without independent institutional confirmation in that cut. I did not add them up as another class of closure or turn a flow into a regional education authority's decision. A later continuity document could reclassify a case and change the population. The [diagnostic reading of all 346 episodes]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a2) makes that uncertainty visible.

Once this population is defined, the next question is no longer how many school codes disappeared. It is what became of the pupils enrolled before their school stopped operating.

## Spoonful 2: what happened after closure?

I call **G** the first year without enrolment at the school of origin, and **G−1** its last open year. For progression, I compare the grade observed two years before closure (G−2) with the grade expected one year afterwards (G+1). I call no enrolment or enrolment below that expected grade **progression failure or grade lag**. The measure combines situations that the register cannot always distinguish; absence from it is not automatically school dropout. I compare changes among exposed pupils and controls, closure cohort by closure cohort. The [regime tables and specifications]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a4) show the underlying comparisons.

The follow-up draws on **79,709,054 enrolment** and **73,873,835 performance records** from 2004 to 2025. To avoid comparing a newly closed school with one already affected, I formed controls from schools still open and estimated differences by closure year[^callaway2021][^sun2021][^roth2023]. I then summarised cohorts under stated weights. This improves the time comparison, but still assumes something about the paths pupils would have followed without closure and about whose outcomes are missing. I read confidence intervals, missing-data bounds, and prior characteristics together; they are not independent proofs of one cause.

Figure 1 presents the whole series. Across **19 estimable progression cohorts**, every point estimate was positive. The exposed-weighted mean was **+9.11 percentage points** (95% confidence interval **+5.34 to +12.88**; worst-case missing-data bounds **+0.43 to +16.21**). Giving every cohort equal weight yields **+7.55 points**; a random-effects model yields **+6.29**, with high heterogeneity (**I² = 76.5%**). These are alternative summaries of gaps, not three independent effects. Exposed-weighted persistent non-enrolment over two years rose by **+1.38 points**. Follow-up differs across the 20 closure cohorts: 19 support progression estimates and 17 support persistent non-enrolment, because of the panel's edges.

<figure class="post3-figure data-visualization" id="fig-post3-2">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/cohort-series-infographic-en-dark.svg' | relative_url }} 1600w" alt="Three-panel infographic under the RCID v1 rule with 1,141 supported episodes between 2005 and 2024. Panel A displays the 19 estimable annual cohorts for progression failure or grade lag from 2006 to 2024: all 19 point estimates are positive, ranging from 0.94 to 28.22 percentage points, with a median of 7.18 and a Callaway and Sant'Anna student-weighted aggregate of +9.11 points (interval from 5.34 to 12.88 and Manski bounds from +0.43 to +16.21 points). Panel B shows attenuation across institutional regimes from 12.15 points in 2005–2010 and 7.82 in 2011–2015 to 5.29 in 2016–2019 (with missing-data bounds from minus 1.15 to 10.98 points), 2.70 in 2020–2022, and 2.59 in 2023–2024. Panel C shows G minus 1 baseline gaps after exact matching: individual SEP eligibility is similar (−1.07 points), whereas exposed students face lower school SEP agreements (−10.06 points), lower full-day schooling (−18.54 points), lower valid record coverage (−19.24 points), and higher prior school switching (+16.52 points)." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 1</strong> — Full 2005–2024 series under the RCID v1 rule: annual estimates (2006–2024), attenuation across the five institutional stages, and baseline gaps among children and adolescents at G−1. <span class="figure-source">Source: author’s calculations from the 2004–2025 MINEDUC longitudinal panel.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post3/cohort-series-infographic-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

A long view changes how the recent window reads. In **2005–2010**, **521 supported closures** and **36,984 exposed observations** yielded a progression gap of **+12.15 points**, with confidence interval **+3.78 to +20.52** and bounds **+3.49 to +18.83**. In **2011–2015**, **502 closures** and **31,512 exposed observations** yielded **+7.82 points**, with bounds **−2.11 to +16.18**. Together those periods account for **89.7%** of supported regular closures and **86.7%** of exposed observations. Later point estimates decline to **+2.70** in 2020–2022 and **+2.59** in 2023–2024. These are descriptions of different periods. They do not isolate the effect of the SEP policy, the Inclusion Law, or the pandemic. Which schools closed, record coverage, promotion rules, and sample sizes changed too.

I fixed **2016–2019** as the primary recent window before examining the complete series: the directory was standardised from 2015, earlier years were observable, and the period preceded the pandemic. It contributes **63 of 1,141 supported episodes** and **6,190 of 78,972 exposed observations**. The narrower window allows more demanding measurement and sensitivity checks; it cannot stand in for two decades. Persistent non-enrolment over two years was **+0.63 points** relative to controls (conservative interval **−0.77 to +2.03**). That interval spans zero, and the measure cannot tell where a pupil absent from the register is studying. Figure 2 shows both primary outcomes; the [detailed table]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a5) retains denominators and exploratory results.

Progression failure or grade lag in the same window was **+5.29 percentage points** (conservative interval **+2.08 to +8.51**). Yet assumption-free bounds for missing outcomes[^manski2003] run from **−1.15 to +10.98 points**. Because they include zero, the recent result is **inconclusive on its own**, despite the positive point estimate. Outcome data are missing for **3.60%** of exposed pupils and **2.15%** of controls. Among closures with at least 90% valid records, the bounds narrow to **+0.09 to +7.84**; that selected subset covers only **38%** of exposed observations with an outcome, and the bounds exclude sampling uncertainty. Choosing schools by coverage may introduce further differences. It does not change the conclusion for the full set.

<figure class="post3-figure data-visualization" id="fig-post3-3">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post3/post-pilot-reestimation-en-dark.svg' | relative_url }} 1600w" alt="Inconclusive post-pilot re-estimation of two primary outcomes. Persistent non-enrolment is estimated at 0.63 percentage points, with a CI from minus 0.77 to 2.03; the different sample that includes receiver schools gives 0.71, from minus 0.69 to 2.12. Progression failure or grade lag is estimated at 5.29 points, from 2.08 to 8.51; the different receiver-school sample gives 5.09, from 1.94 to 8.23. Missing-data bounds span minus 1.15 to 10.98 points. These are not confirmed causal effects." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 2</strong> — Pre-registered 2016–2019 zoom: inconclusive post-pilot re-estimation, not causal effects. The progression interval does not cross zero, but its missing-data bounds do; overlap with the pilot and unobserved assumptions prevent a causal interpretation. <span class="figure-source">Source: author’s calculations from the post-pilot re-estimation.</span> <span class="figure-data">Accessible tabular data: <a href="{{ '/assets/images/tesis-post3/post-pilot-reestimation-data.csv' | relative_url }}">estimates</a> and <a href="{{ '/assets/images/tesis-post3/missingness-bounds-data.csv' | relative_url }}">missing-data bounds</a>.</span></figcaption>
</figure>

The effective size of the recent comparison also matters. Although **62 closures** have an observable window for both primary outcomes, a few account for many pupils. Under that imbalance, the information is equivalent to about **21.1 effective episodes** for non-enrolment and **21.9** for progression; attendance and grades fall to **17.7**. Those secondary differences are exploratory because they require valid reports in both periods: only **3,871 exposed observations**, or **62.5%** of supported exposed observations, have them. A precise estimate among pupils with reports need not represent those without them. The annex preserves [coverage, comparability, and secondary outcomes]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tabla-post3-a6).

Neither pre-trend checks nor sample adjustments resolve missing outcomes. Three pre-closure placebos in 2016–2019 were **+0.16, +0.30, and +0.40 points**. A simplified linear sensitivity check finds that **2.07 points** of later bias would bring the conventional interval to zero. This is a different test from missing-data bounds; the two cannot simply be added. Among pupils enrolled since G−2, the progression gap was **+3.87 points**; among late entrants it was **+9.58**. That contrast warns of earlier selection, although neither group supplies a perfect counterfactual. The [assumptions and sensitivity calculations]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#tendencias-y-datos-faltantes) are available in the annex.

I also examined **4,362 exposed observations** that reappeared enrolled at a receiving school in G. If the destination's earlier pass rate exceeded that of the school of origin, the progression gap was **+2.03 points**; at destinations with an equal or lower pass rate, **+5.38**. Their **−3.35-point difference** is descriptive and has **no confidence interval of its own**. Families choose destinations and the comparison excludes those who did not reappear. It does not estimate the effect of assigning a higher-quality school. The [receiving-school comparison]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#calidad-de-la-receptora) states the prior-quality definition.

The historical figure and recent close-up answer related questions with different degrees of support. One exposes a widespread, highly varied gap; the other shows exactly how missing outcomes and selection constrain attribution. That distinction leads to the practical question: what safeguards should be checked even while the exact causal size remains unsettled?

## Spoonful 3: how can a school transition be protected?

An observed gap with uncertain causal attribution can identify where a public procedure must produce evidence. It cannot show that a particular intervention would reduce the gap. Before closure, an authority needs to establish whether provision really ends or continues under another code, site, or level; when the change was announced; and how many genuine, accessible, suitable places exist. During the move, travel, support, and teaching continuity matter. Afterwards, enrolment, attendance, grade, and wellbeing need tracking at receiving schools. The table lists information to require, not effects already estimated.

{: .table-caption}
**Table 1.** Minimum information for deciding and evaluating a transition

| Before a decision | During the transition | After the change |
|---|---|---|
| Distinguish school, site, level, merger, and identifier change. | Assign actual places and support to each student. | Follow enrolment, attendance, progression, grades, and wellbeing. |
| Record the announcement date and community participation. | Measure travel time, accessibility, and peer continuity. | Observe students and staff already in receiving schools as well. |
| Verify capacity, staffing, and prior destination quality. | Fund receiving-school load and pedagogical continuity. | Publish alerts, corrections, responsibilities, and deadlines. |
{: .table--compact .table--scroll}

Table 6 shifts the burden of proof against a concrete procedural gap: when the Library of the National Congress asked the Official Recognition Unit of the Metropolitan Regional Secretariat what the “student relocation certificate” (*constancia de reubicación de los alumnos*) required in the voluntary-closure checklist actually entailed, the authority clarified that this requirement—absent from both the statute and Supreme Decree No. 315 of 2010—consisted solely of “having informed students of alternatives for relocating their enrolment”, without verifying whether those nearby schools had actual vacancies or whether students effectively enrolled in them (Castro Paredes 2013[^castroparedes2013], p. 2n1). An authority cannot assume educational continuity merely because an exiting provider handed out a list of nearby schools or because part of the student body reappeared on an enrolment roll: it must verify beforehand that real vacancies, safe transport, support for priority students, and pedagogical support exist at the receiving schools, and track every displaced student by name for at least two years.

I would make that proposal evaluable. Before a decision, I would record a baseline for pupils and receiving schools, announcement dates, available places, and journey times. During reassignment, I would record support actually delivered, continuity in grade, and further school changes. Afterwards, I would follow the whole cohort, including pupils absent from the regular register, under explicit privacy and coverage rules. This separates delivery from outcomes: the existence of a place does not establish acceptance, a subsequent enrolment does not establish progression, and a change after closure does not by itself identify its cause.

A certificate listing alternatives is not a guaranteed place. Administrative documentation[^castroparedes2013] discussed in the [legal notes]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#certeza-documental-y-regla-empirica) shows that informing families of relocation options could satisfy a formal requirement without confirming vacancies or actual arrival. I therefore recommend confirming places, transport, and support before reorganisation, then tracking each displaced pupil for at least two years with privacy safeguards. These **precautionary safeguards are not estimated effects of those decisions**. Their effectiveness would require recording implementation and comparing outcomes. Map proximity alone says little about journey time, admission, or destination quality.

This article does not estimate higher education outcomes. [Part IV]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/' | relative_url }}) extends that question using SIES and PAES/PDT records. <span id="fig-post3-4"></span>The [territorial audit figure]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}#fig-post3-4) preserves classification evidence. The longer horizon does not replace immediate school follow-up: enrolment may continue today while options change later, or later differences may reflect disadvantages already present before closure.

## Closing: following trajectories changes the decision

The inquiry began with a distinction: a school disappearing from a directory may signal lost provision or continuity under a different form. After filtering those episodes, I followed **78,972 exposed student-cohort observations** across **1,141 supported regular-school closures**. In the long series, progression failure or grade lag has a positive estimated gap in 19 measurable cohorts, reaching **+9.11 percentage points** under exposed weighting; its size differs across periods. In the primary recent window, 2016–2019, the estimate is **+5.29 points**, but missing-data bounds from **−1.15 to +10.98** span zero. Prior school fragility and pupil mobility still prevent me from calling the whole gap an effect of closure.

That uncertainty does not remove the practical need to verify continuity. Checking places, travel, and support and following pupils into their destination schools is a precautionary response to incomplete records. I have not measured the effectiveness of that response here. Three observable tasks would move this diagnosis towards an evaluable decision:

1. **Document what closed.** Collect formal decisions and announcement dates so legal closures, pauses, and reorganisations can be distinguished.
2. **Complete the trajectories.** Recover missing reports and outcomes, and assess sampling uncertainty, trends, and selection together for the recent window.
3. **Measure the transition.** Record places, journey times, support, and receiving-school outcomes, including pupils who never reappear as enrolled.

[Part IV]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/' | relative_url }}) follows postsecondary paths under the same discipline: separate what is observed from what can be attributed.

## References

[^callaway2021]: Callaway, Brantly, and Pedro H. C. Sant'Anna. 2021. [“Difference-in-Differences with Multiple Time Periods.”](http://arxiv.org/pdf/1803.09015) *Journal of Econometrics* 225 (2): 200–230. [DOI](https://doi.org/10.1016/j.jeconom.2020.12.001) · [Scholar](https://scholar.google.com/scholar_lookup?title=Difference-in-Differences+with+multiple+time+periods&doi=10.1016%2Fj.jeconom.2020.12.001)

[^castroparedes2013]: Castro Paredes, Luis. 2013. [*Cierre voluntario de Establecimientos Educacionales*](https://obtienearchivo.bcn.cl/obtienearchivo?id=repositorio/10221/20674/5/Cierre%20voluntario%20de%20Establecimientos%20Educacionales_v2.pdf). Parliamentary Technical Advisory Report, Library of the National Congress of Chile (BCN), December 12, 2013.

[^manski2003]: Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). New York: Springer. [Scholar](https://scholar.google.com/scholar_lookup?title=Partial+Identification+of+Probability+Distributions&doi=10.1007%2Fb97478)

[^roth2023]: Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–44. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)

[^sun2021]: Sun, Liyang, and Sarah Abraham. 2021. [“Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects.”](https://doi.org/10.1016/j.jeconom.2020.09.006) *Journal of Econometrics* 225 (2): 175–99. [Scholar](https://scholar.google.com/scholar_lookup?title=Estimating+dynamic+treatment+effects+in+event+studies+with+heterogeneous+treatment+effects&doi=10.1016%2Fj.jeconom.2020.09.006)
