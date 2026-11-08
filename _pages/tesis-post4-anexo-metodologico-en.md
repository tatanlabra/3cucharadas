---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Part IV annex: school cohorts and higher education records"
description: "Calendars, denominators, support, and provenance for the higher-education comparison."
permalink: /datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/
ref: tesis-post4-anexo-metodologico
lang: en
author: clabra
author_profile: true
math: true
toc: true
toc_sticky: true
table_contract: explicit-v1
last_modified_at: 2026-11-07 23:40:00 -0300
published: true
f2_complete: true
publication_authorized: true
scientific_status: DESCRIPTIVE_ONLY
readiness: READY_FOR_PUBLICATION
---

<!-- SCIENTIFIC_STATUS: DESCRIPTIVE_ONLY; READINESS: READY_FOR_PUBLICATION; F2_COMPLETE: true; PUBLICATION_AUTHORIZED: true. -->
<!-- scientific-state: DESCRIPTIVE_ONLY -->
<!-- publication-readiness: READY_FOR_PUBLICATION -->

{% include thesis-series-nav.html current=4 %}

The [main article]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/' | relative_url }}) sets out the three questions and the limits that change their interpretation. This annex records the calendar, denominators, and provenance. The design compares school cohorts; it does **not** follow the same people before and after, or identify individual effects.

## Two cohorts and a common calendar

I call the event calendar year **G** and the baseline secondary-school grade **g**, taking the values one, two, or three. The earlier cohort was enrolled in calendar year G−5; the later cohort in G−1. If **B** is the baseline calendar year, the first year **after expected school completion** is **B+5−g**, assuming regular progression:

| Cohort | Baseline calendar year | First year after expected completion |
|---|---|---|
| Earlier | G−5 | G−g |
| Later | G−1 | G+4−g |
{: .table--compact .table--scroll}

For example, a pupil in the first year of secondary school in 2015 would reach the fourth year in 2018 under regular progression. The first year after expected completion is 2019, so the observed-access window covers 2019 and 2020. The label **earlier cohort** does not mean that all its outcomes precede G. In an illustrative event year **G=2016**, a first-year secondary pupil in the earlier cohort starts in **2011**. That pupil's access window is **2015–2016**, persistence window **2015–2017**, and qualification window **2015–2020**. These calendar windows can coincide with the event or extend beyond it; they are not empirical observations of a particular pupil. I do not reset the clock to each pupil's actual school-leaving date. The measure therefore combines possible school delays with later transitions into higher education.

I consider candidate event years from **2009 through 2024** and check follow-up by baseline grade and outcome. The series begins in 2009 because a G−5 cohort needs school records from 2004 as well as later higher-education coverage. I present historical and modern eras separately because the evidence used to classify lost provision differs; no single pooled estimate presumes that they represent equivalent exposures.

Accessible versions of the figures: [Accessible calendar table]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-calendar-table-en.html' | relative_url }}) and [Accessible window matrix by grade]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-calendar-window-matrix-en.html' | relative_url }}).

## What each outcome counts

The denominator is the eligible **baseline school cohort**, with a valid identifier and complete follow-up in comparable cells. It is not restricted to higher-education entrants. Exact pupil counts appear only for pooled primary two-year access in each era and refer to the **later cohort**; school counts cover **both cohorts**. Other contrasts omit person counts after combined privacy review.

| Outcome | Record required from the first year after expected school completion |
|---|---|
| Observed access | At least one SIES undergraduate enrolment in a two-year window. This does not establish a person's first-ever entry. |
| Destinations | In the same two years: university only, professional institute or technical training centre only, both types, or none recorded. An unknown institution type is incomplete information. |
| Recorded persistence | Enrolment in at least two distinct years of a three-year window; the years need not be consecutive. |
| Observed qualification | At least one undergraduate award within six inclusive calendar years. |
{: .table--compact .table--scroll}

SIES is Chile's Higher Education Information Service (*Servicio de Información de Educación Superior*). The enrolment extract used here covers **2007–2026**; the awards extract covers **2007–2025**. These are dated sources that can be revised. Checking their files and counts does not prove that every national trajectory is covered or that every individual link is correct.

Modern follow-up supports pooled access for **2016–2024**, persistence for **2016–2023**, and qualifications for **2016–2019**. The mix of baseline grades changes at the endpoints. The presence of an event year alone does not supply a complete window for every outcome. **Incomplete follow-up**, **lack of comparable controls**, and **privacy suppression** are different states; none is replaced with zero.

## How the contrast is built

The main matching rule requires the same event year, region, administrative school sector, rural or urban location, type of education, and baseline grade. A cell needs all four combinations: event and comparison schools in both earlier and later cohorts. Main controls have no observed D1 event in the 2005–2024 inventory. This selects schools that survived that inventory and may bias the comparison. Keeping controls in the same municipality improves local support but allows possible transfers into those schools.

Within each cell, I calculate the change in the outcome rate between cohorts at event schools and subtract the change at controls. I then pool cells using the number of treated pupils in the later cohort as weights. The four displayed descriptive rates for pooled primary access use those **same weights**: taking their difference in changes reconstructs the point contrast, apart from rounding. Subtracting changes does not guarantee that the two groups would have followed parallel trends without the event (Roth et al. 2023).

## Uncertainty, measurement, and limits

The school-level resampling uses **9,999** positive multipliers and recalculates the estimator. Primary pooled intervals are **97.5%** for total access across the two eras, **98.75%** for the destination family, and **95%** for persistence and qualifications. The heterogeneity analysis uses the Holm (1979) procedure within prespecified families. These adjustments concern different families; comparing which of two rows is "significant" is not a test of whether their effects differ.

Concentration in a few schools limits precision even when there are many pupils. A large student count does not replace independent school units. The two-way school-and-student variance diagnostic keeps the point estimates fixed and yields variance ratios of **0.99861 to 1.00519** relative to school-clustered CR0 for the 16 pooled estimates. It does not repair a small number of event-school clusters: all eight modern pooled primary results carry a weak-school-precision flag.

An invalid student identifier in the school records or ambiguous baseline assignment excludes a person from the valid-identification estimand and must be counted in the audit. A valid identifier with no SIES record may mean absence **from the extract**, not necessarily absence from higher education. Linkage bounds use the aggregate capacity of records with invalid identifiers; they are not measured group-specific error rates. When they are too wide to distinguish directions, that lack of information must be reported.

## Results and coverage for all eight outcomes

The table reports **percentage points** and keeps the two event taxonomies separate. Two-year access intervals are at 97.5%; the four destinations at 98.75%; exact-year enrolment, persistence, and qualifications at 95%. Comparing whether two intervals cross zero is not a test of the difference between those outcomes.

| Outcome | 2009–2015: contrast [interval] | 2016–2024: contrast [interval] |
|---|---:|---:|
| Enrolment observed within two years | −2.31 [−5.26; +0.29] | −2.43 [−5.67; +1.27] |
| Enrolment in the exact nominal year | −1.71 [−4.04; +0.17] | −2.10 [−5.56; +1.57] |
| University only within two years | −2.07 [−4.18; −0.23] | +0.83 [−2.59; +3.88] |
| IP/CFT only within two years | −0.31 [−2.97; +2.40] | −2.61 [−5.51; +1.00] |
| Both types within two years | +0.07 [−0.33; +0.43] | −0.64 [−1.93; +0.18] |
| No higher-education record within two years | +2.31 [−0.61; +5.58] | +2.43 [−1.68; +6.05] |
| Enrolment in at least two of three years | −3.13 [−5.30; −1.20] | −1.90 [−5.01; +1.31] |
| Undergraduate award within six years | −1.47 [−2.69; −0.28] | −2.28 [−5.56; +0.71] |
{: .table--compact .table--scroll}

The modern column identifies a **taxonomy**, not a claim that every outcome pools all years from 2016 to 2024: persistence includes event years only through 2023 and qualifications only through 2019. For two-year access, 2023 and 2024 contribute only the third baseline grade. The common-year sensitivity keeps only event years with support in **all three secondary-school grades at once**: 2010–2015 and 2016–2022 for access, 2016–2021 for modern persistence, and 2016–2017 for modern qualifications. It is not a separate third-grade-only estimate and does not replace the full series.

The four destination categories share a denominator and are exhaustive. No record is the complement of two-year access, not independent confirmation. Historical intervals for university only, persistence, and qualifications are negative at their respective confidence levels; every modern pooled primary interval includes zero. Interpretation remains descriptive: intervals do not cover misclassification, divergent trends, or incomplete linkage. Conservative invalid-identifier capacity bounds for access run from **−80.95 to +74.03** historical points and **−71.70 to +66.18** modern points. They are too wide to defend a direction from linkage information; they are not measured arm-specific error rates.

[Accessible comparison table]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-comparison-table-en.html' | relative_url }}).

## Completed sensitivities and their limits

| Prespecified comparison | Observed result | Limit |
|---|---|---|
| Stable school characteristics, controls from another municipality, and years with three supported grades | All 16 pooled rows per variant are estimated; access points remain negative in both taxonomies. | Population or comparator changes; matching signs do not prove equivalence or no interference. |
| Baseline age and gender standardisation | All 16 pooled rows are estimated; modern access changes from −2.43 to −1.59 points. | Requires support for categories present among treated pupils; this difference does not identify an individual mechanism. |
| Fixed-effects diagnostic | All 16 pooled rows are estimated; historical access is −2.47 points [95% CI: −4.85; −0.21] versus primary −2.31 [97.5% CI: −5.26; +0.29]. | The coefficient uses different weights and answers a different estimand; the confidence levels also differ. Different zero crossings are not a formal difference test. |
| Never-observed-D1 plus future-D1 controls, with two horizons | All 16 pooled rows per horizon are estimated; access remains close to primary. | In **180 eligible variant × outcome × G × grade rows** across the two combined variants (76 and 104), no future-D1 control contributes. Agreement there does not test that comparator. |
| Future-D1 controls only, with two horizons | 15/16 pooled rows under the outcome horizon and 16/16 under school exposure; modern qualifications lose support under the outcome horizon. | Sample and comparator change; several modern outcomes have fewer than ten treated schools. The projection prepared for release omits their arm rates and exact person counts; the points describe different samples and retain weak school-level precision. |
| Two-way school-and-student variance | The 16 pooled point estimates equal primary; variance ratios to school CR0 are 0.99861–1.00519. | CR0 does not solve few treated clusters or identify effects. |
| Earlier cohorts A and strictly pre-event B | A keeps G−6/G−5 and G−7/G−6 even where outcome windows reach G; B keeps those cohorts but requires **both** windows to end before G. For modern access G−6/G−5, A is −3.12 [−5.24; −0.68] and B is −2.28 [−5.09; +0.70] points. | B drops the first baseline grade and recalculates support and weights; the difference is not an estimate of anticipation bias. For qualifications, all **96 B coverage rows** (48 per variant, corresponding to 48 G-by-grade combinations) are `NOT_ESTIMABLE_TEMPORAL_OVERLAP`, not zero. |
| Heterogeneity by grade, sector, rurality, and region | 800 pairs were fixed: 388 estimable, 412 unsupported or withheld for privacy; 34 have Holm p below 0.05. | Holm acts within each outcome-by-era family of 65 or 35 tests, not across all 800. Access and no-record results duplicate signals; no causal profile or subgroup release follows. |
{: .table--compact .table--scroll}

Modern persistence shows why I retain outcomes beyond access: the late A placebo is **−2.41 points** [95% CI: **−4.50; −0.07**] over 2016–2024, although some windows reach G. With future-only controls under the outcome horizon it is **−10.02** [**−19.51; −0.81**] over 2016–2017 with **four event schools**; historical qualifications with that comparator are **+4.05** [**−0.64; +8.80**] over 2009–2014 with **27 event schools**. Cohorts, weights, and comparators change. These nominal 95% intervals do not test differences from primary, anticipation, or causal effects. School-level precision is especially weak with four event schools.

The exhaustive inventory records **4,992** coverage statuses (`variant × outcome × G × grade`), **2,200** sensitivity result statuses, **144** primary keys, and all **800** heterogeneity pairs. Their joint key reconciliation passed. A row can have a point without a valid annual interval, be suppressed, censored, unsupported, or excluded by the strict calendar. None of those statuses means zero. The combined review found possible subtraction across variants and removed cross-reconstructible counts from the prepared projection; a threshold on each row alone would not suffice.

The pre-outcome feasibility check for the repeated-cross-section DR-DiD estimator of Sant’Anna and Zhao (2020) examined **152 historical** and **72 modern** strata. It found **39** and **29** failures, respectively: either the group-membership model separated groups or a prediction needed a combination of characteristics unsupported by the fitted model. Under the fixed rule, I do not discard those strata to estimate a different population. All **eight outcomes in each era** have status `NOT_ESTIMABLE_DRDID_DESIGN`. This is non-estimability under this specification, not a zero effect or a judgment on all possible methods. BLP/GATE/CLAN is `NOT_RUN_METHOD_NOT_IMPLEMENTED`: work not executed, distinct from a demonstrated empirical barrier.

## Reproducibility and retrospective review

The protocol fixes decisions for an auditable reconstruction of previously studied data. It is not an independent preregistration. I retain code, file hashes, coverage, and execution receipts. Primary and sensitivity production have receipts, and the joint key reconciliation passed. Independent reproduction of both aggregates passed. Numerical agreement does not by itself validate causal assumptions or complete source coverage.

The combined privacy review ruled out full export of the private aggregates. The projection prepared for release retains four rates and exact pupil counts only for pooled primary two-year access in each era. For other results it retains contrasts, intervals, statuses, and school counts, while removing arm rates and person counts. Reasons for missing data and suppression remain visible. These exclusions reduce reconstruction by subtraction detected among this edition’s results, tables, and figures; they do not guarantee protection against every possible combination with external information. Earlier-edition figures remain in historical custody and are not presented as results of this comparison.

## References

- Chilean Ministry of Education. n.d. "Student-level enrollment." Open Data Portal. <https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/>. Local extracts and transformations are documented in this revision’s protocol; the portal does not itself certify those files.
- Higher Education Information Service (SIES). n.d. "Bases de datos de estudiantes matriculadas y matriculados en Educación Superior en Chile" and "Base de datos de estudiantes tituladas y titulados en Educación Superior en Chile". Mi Futuro, Chilean Ministry of Education. <https://www.mifuturo.cl/bases-de-datos-de-matriculados/>; <https://www.mifuturo.cl/bases-de-datos-titulados/>. Local enrollment and awards extracts are documented separately.
- Holm, Sture. 1979. "A Simple Sequentially Rejective Multiple Test Procedure." *Scandinavian Journal of Statistics* 6 (2): 65–70. <https://www.jstor.org/stable/4615733>.
- Roth, Jonathan, Pedro H. C. Sant’Anna, Alyssa Bilinski, and John Poe. 2023. ["What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature."](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–2244. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)
- Sant’Anna, Pedro H. C., and Jun Zhao. 2020. ["Doubly Robust Difference-in-Differences Estimators."](https://doi.org/10.1016/j.jeconom.2020.06.003) *Journal of Econometrics* 219 (1): 101–122. A reference for the method checked for feasibility; it yielded no effect estimate here. [Scholar](https://scholar.google.com/scholar_lookup?title=Doubly+robust+difference-in-differences+estimators&doi=10.1016%2Fj.jeconom.2020.06.003)
