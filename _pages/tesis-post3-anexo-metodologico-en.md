---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Part III annex: definitions and traceability of school trajectories"
description: "Supplementary definitions, coverage, and limits of the comparison of school trajectories."
permalink: /datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/
ref: tesis-post3-anexo-metodologico
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

{% include thesis-series-nav.html current=3 %}

The [main article]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/' | relative_url }}) explains the question, comparison, and interpretative limits in each spoonful. This annex records technical decisions and coverage for readers who want to inspect them; it is not a prerequisite for the account. Every estimate in this revision is descriptive. An adjusted association does not establish a causal effect.

## What counts as an event

Year **G** marks a loss of provision inferred from records, not a legal determination that a school closed. The **2005–2015** classification uses disappearance without an observed reappearance through 2025 plus a review of pupil flows. The **2016–2024** classification also uses annual information on a school's status and identity. That documentary difference prevents me from treating the eras as one homogeneous exposure. The historical classification uses information from after G; it is not a rule that could have been applied in real time with the data then available.

Chilean evidence on school closure and educational mobility (Grau et al. 2018) and on nearby alternatives for vulnerable families (Elacqua et al. 2012) provides context, but it does not identify this series' contrast.

The broader D1 rule and the flow-screened D2 rule let me examine sensitivity to the event definition. In the historical inventory they identify the same episodes, so comparing them there is **not** a discriminating test. They differ in the modern era. A concentration of transfers is a reason to investigate continuity of provision, not institutional confirmation of a merger or closure.

## Population and comparison

The unit is a **pupil–cohort observation**, beginning with enrolment at the school of origin in G−1. One person may appear in more than one reference cohort, so pooled counts do not necessarily count distinct people. I exclude ambiguous baseline assignments and retain a coverage diagnosis for them.

| Decision | Main comparison |
|---|---|
| Matching characteristics | Event year, region, administrative school sector, rural or urban location, type of education, baseline grade, gender, and baseline age. |
| Minimum support by cell and outcome | At least one treated pupil and five controls, with one treated and two control schools. These are computational thresholds, not guarantees of identification. |
| Control selection | Eligibility is screened first; then a deterministic order caps controls at twenty per treated pupil. |
| Local exposure | Controls in the same municipality and education level are excluded; putting them back is a sensitivity. |
| Later events among controls | A control's own event within an outcome window excludes it. The rule uses the event inventory and calendar, not the pupil's outcome. |
| Weighting | Within each era, cells are weighted by treated pupils with a classifiable outcome. Equal cohort weights are a separate sensitivity. |
{: .table--compact .table--scroll}

When a comparable cell cannot be found, the population addressed by the contrast shrinks. I do not loosen matching rules after seeing a sign to recover a preferred result.

The literature does not establish a universal sign either: Engberg et al. (2012) describe an initial attendance loss among displaced pupils that disappears after their first year in a new school, and detect no adverse effects among pupils already at receiving schools in their setting; Brummet (2014) finds modest receiving-school effects; Beuchert et al. (2018) document short-term losses after Danish consolidations. None of those designs validates this comparison's matching rules.

## Two outcomes that cannot be substituted for one another

| Outcome | Starting population | Later observation | What it cannot establish |
|---|---|---|---|
| Lack of observed progression | First year of primary to second year of secondary school | In G+1, no linkable enrolment appears, or an interpretable grade is less than two grade levels above baseline. | It does not, on its own, separate actual delay, loss of coverage, and other routes. |
| Two years without observed enrolment | First year of primary to first year of secondary school | No valid record appears in either G+1 or G+2. | It does not establish that a pupil left education. |
{: .table--compact .table--scroll}

If there is enrolment but the grade is unknown or conflicting, progression remains **unknown**; it is not turned into either failure or absence. For the second outcome, any linkable enrolment in either year establishes presence. The 2024 cohort has follow-up for progression but not for a complete G+2 window. I record that boundary as incomplete follow-up.

## Uncertainty and missing information

The main contrast subtracts adjusted **post-event levels**; it is not a difference in differences. I calculate uncertainty with **9,999** positive school-level multiplier resamples. Each school receives the same random weight wherever it appears, and I recalculate levels and weights while retaining eligible pupils and cells. Clustering by school recognises shared circumstances among its pupils; it cannot remove selection or measurement bias.

The four pooled contrasts—two outcomes across two eras—use nominal **98.75%** intervals for that family. Annual intervals are **95%** and serve a descriptive purpose. Few schools, concentrated pupil weights, or further dependence between pupils call for warnings and sensitivities. An interval containing zero does not prove equivalence.

A **bound** answers another question. Assigning unknown grades alternately to progression and non-progression sets out the values compatible with that incomplete information while preserving the population specified for the bound. It is not a confidence interval. For actual education outside the panel, an absent administrative record cannot establish the true status either; the limits must reflect that additional uncertainty.

This is an application of partial identification (Manski 2003): the bounds depend on the stated extreme assignments, not on an inferred distribution of missing states.

## Complementary checks

The earlier indicator compares enrolment from G−2 to G−1. Its starting population differs from that of the main contrast, and its rates are unadjusted. It describes a pre-event difference, but neither identifies anticipation nor automatically corrects the later result.

{% assign reset_figure = site.data.tesis_reset_figures["post3-anticipation-persistent_nonenrollment_two_years-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset/anticipation" %}

{% assign reset_figure = site.data.tesis_reset_figures["post3-anticipation-persistent_nonenrollment_two_years-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset/anticipation" %}

The symmetric-cohort diagnosis compares baseline cohorts at G−4 and G−1 with equal relative horizons. It distinguishes a later gap from a difference in changes, but any causal reading needs further assumptions. Attendance and marks are analysed only among valid observed records; their units and observation rates are reported separately.

### How far the checks take us

These tests answer different questions. They must not be added or subtracted from one another. The bounds below retain the baseline population before excluding unknown information, so they need not contain point estimates calculated on classifiable outcomes. All numbers in this table are **percentage points**.

| Question and population | 2005–2015 | 2016–2024, or 2016–2023 where G+2 is needed | Permitted reading |
|---|---:|---:|---|
| Lack of progression with unknown grades, fixed baseline | +6.00 to +12.90 | +3.02 to +7.19 | Missing-information bounds, without their own statistical interval. |
| True non-schooling with schooling outside the panel unknown, fixed baseline | −2.82 to +4.76 | −1.76 to +2.89 | Both signs remain compatible; no record does not mean dropout. |
| Equal cohort weights: lack of progression | +10.09 | +5.06 | Point-only sensitivity, without its own interval. |
| Equal cohort weights: two years without a record | +2.08 | +0.88 | Point-only sensitivity, without its own interval. |
{: .table--compact .table--scroll}

The symmetric-cohort diagnosis needs a complete earlier cohort, so its historical series begins in **2008**, not 2005. In the following table, the first interval uses **9,999** school-level multipliers; the second allows school and pupil dependence through an asymptotic approximation. Both are nominally **95%** intervals. The weak-cluster precision warning applies to all four two-way intervals.

| Outcome and era | Difference between gaps | School interval | School-and-pupil interval |
|---|---:|---:|---:|
| Lack of progression, 2008–2015 | +4.36 | +2.07 to +8.60 | +0.90 to +7.81 |
| Lack of progression, 2016–2024 | +0.40 | −1.74 to +2.50 | −1.78 to +2.58 |
| Two years without a record, 2008–2015 | +0.45 | −0.30 to +1.23 | −0.31 to +1.20 |
| Two years without a record, 2016–2023 | +0.28 | −0.47 to +1.14 | −0.49 to +1.05 |
{: .table--compact .table--scroll}

The historical progression interval does not span zero, but that still does not turn the diagnosis into a causal effect. Earlier selection and assumptions about the generations remain unresolved. This table targets another estimand and, in the historical era, another window. Subtracting its figures from the primary contrasts cannot measure how much of the gap was “explained.”

Widening the event definition to D1 cannot discriminate between rules in the historical inventory: D1 and D2 flags coincide. In the modern era, full-sample contrasts change from **+4.98 to +1.88 points** for lack of progression and from **+1.13 to +0.33** for two years without a record. On common observations, D1 and D2 give **+4.96** and **+1.11 points**, respectively, under both rules. That equality follows mechanically from shared exposure and outcome. The full-sample difference mixes composition and support, without a joint interval. Results from local controls and three receiver-school filters are withheld to protect small groups. Withholding is not evidence of a null result or robustness; a receiver-school filter also selects a condition that follows the event.

### Attendance and marks among observed pupils

This comparison concerns changes between G−1 and G+1 **only for pupils with valid records in both years**. The complete-case rate is published in five-percentage-point bands: exact counts across correlated metrics and cohorts could reveal small groups. Among exposed pupils, the rate is **65–70%** in 2005–2015 and **70–75%** in 2016–2024; among controls it is **85–90%** and **90–95%**, respectively. This arm-specific selection prevents generalising the results to all baseline pupils.

| Conditional measure | 2005–2015, difference and 95% CI | 2016–2024, difference and 95% CI | Unit |
|---|---:|---:|---|
| Attendance | −0.31 [−0.73; +0.12] | −2.13 [−4.89; −0.08] | Attendance percentage points. |
| Mean mark | −0.092 [−0.114; −0.068] | −0.041 [−0.093; +0.014] | Mark points on the 1–7 scale. |
{: .table--compact .table--scroll}

The school-based intervals are exploratory and describe complete cases only. Attendance excluding zero values was calculated, but its estimates are withheld because a group is small; they are not replaced with zero. Windows before, overlapping, and after the pandemic provide exploratory context, without a formal comparison between periods or evidence of a pandemic effect.

## Versions and data protection

This is a retrospective reconstruction of data that were already analysed. The protocol and its amendments make decisions auditable, but they are not an independent preregistration. Earlier results remain in custody; I do not combine their figures with this revision.

Public downloads must contain only reviewed aggregates, without identifiers or small cells that could be reconstructed by subtracting one table from another. A privacy suppression retains its reason; it is neither a zero nor a lack of statistical support.

## References

- Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen, and Nina Smith. 2018. ["The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?"](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47. [Scholar](https://scholar.google.com/scholar_lookup?title=The+short-term+effects+of+school+consolidation+on+student+achievement%3A+Evidence+of+disruption%3F&doi=10.1016%2Fj.econedurev.2018.05.004)
- Brummet, Quentin. 2014. ["The Effect of School Closings on Student Achievement."](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–124. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effect+of+school+closings+on+student+achievement&doi=10.1016%2Fj.jpubeco.2014.06.010)
- Chilean Ministry of Education. n.d. "Student-level enrollment." Open Data Portal. <https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/>. Local extracts and transformations are documented in this revision’s protocol; the portal does not itself certify those files.
- Elacqua, Gregory, Matías Martínez, Humberto Santos, and Daniela Urbina. 2012. ["School Closures in Chile: Access to Quality Alternatives in a School Choice System."](http://www.scielo.cl/pdf/ede/v39n2/art05.pdf) *Estudios de Economía* 39 (2): 179–202. [DOI](https://doi.org/10.4067/S0718-52862012000200005) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closures+in+Chile%3A+Access+to+quality+alternatives+in+a+school+choice+system&doi=10.4067%2FS0718-52862012000200005)
- Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. ["Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?"](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203. [Scholar](https://scholar.google.com/scholar_lookup?title=Closing+schools+in+a+shrinking+district%3A+Do+student+outcomes+depend+on+which+schools+are+closed%3F&doi=10.1016%2Fj.jue.2011.10.001)
- Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. ["School Closure and Educational Attainment: Evidence from a Market-Based System."](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf) *Economics of Education Review* 65: 1–17. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)
- Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). Springer. [Scholar](https://scholar.google.com/scholar_lookup?title=Partial+Identification+of+Probability+Distributions&doi=10.1007%2Fb97478)
