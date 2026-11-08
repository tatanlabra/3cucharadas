---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extending my thesis in 3 spoonfuls (part III): tracking school trajectories after a school loses provision"
subtitle: "I find more recorded difficulties with grade progression and prolonged enrolment gaps; an earlier unadjusted indicator cautions against attributing them to the event."
date: 2026-10-23 10:00:00 -0300
categories: [data, education, public-policy]
tags: [education, school-closure, trajectories, mineduc, administrative-data, public-policy]
description: "School trajectories after a loss of provision in Chile: grade progression, recorded enrolment, uncertainty, and the limits of comparison."
excerpt: "I compare pupils from schools that lost provision with pupils from comparable schools, separating observed differences from what I cannot yet attribute to the event."
author: clabra
lang: en
ref: costos-cierre-escolar-trayectorias
permalink: /datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/
math: true
toc: true
toc_sticky: true
comments: true
author_profile: true
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
last_modified_at: 2026-11-07 23:40:00 -0300
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
distribution:
  social: false
  republish: []
  skip_reason: "Diffusion deferred by author."
published: true
f2_complete: true
publication_authorized: true
scientific_status: DESCRIPTIVE_ONLY
readiness: READY_FOR_PUBLICATION
---

<!-- SCIENTIFIC_STATUS: DESCRIPTIVE_ONLY; READINESS: READY_FOR_PUBLICATION; F2_COMPLETE: true; PUBLICATION_AUTHORIZED: true. -->
<!-- scientific-state: DESCRIPTIVE_ONLY -->
<!-- publication-readiness: READY_FOR_PUBLICATION -->

{% include thesis-series-nav.html current=3 %}

When a school stops offering the years it once taught, finding another place is only the beginning for a family. A child also needs to turn up in the school register again and move through the expected years of schooling. I followed those two signals in Chilean administrative records. Pupils from schools that lost provision fare worse on both measures than pupils from comparable schools in the historical and modern periods. An earlier unadjusted indicator, drawn from a different starting population, shows a difference before the event. What I observe is a gap; I cannot yet say how much of it the loss of provision produced. <!-- CLAIM: P3-01 -->

Related studies ask different questions about school closure. In Chile, Grau, Hojman, and Mizala (2018) study dropout and grade retention, while Elacqua and colleagues (2012) show that nearby quality alternatives can be scarce, particularly for rural or disadvantaged families. Elsewhere, Engberg and colleagues (2012) document an initial attendance disruption that fades, Brummet (2014) finds modest costs for receiving schools, and Beuchert and colleagues (2018) find short-run losses after consolidation. These studies motivate separate measures of progression, missing enrolment, and possible receiving schools; their treatments, populations, and designs do not identify an effect in this Chilean series.

The [methodological annex]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/' | relative_url }}) retains definitions, coverage, and technical checks; the three spoonfuls can be read without it.

I ask three connected questions. Did pupils progress to the expected year? Did they disappear from the enrolment records for two years? And how demanding is the comparison once I consider earlier differences and missing information? I use individual enrolment records from Chile's Ministry of Education and an operational classification of episodes in which a school lost provision, built from those records. I call the event year **G** and start with pupils enrolled at their school of origin in **G−1**. I compare pupils by event year, region, administrative school sector, urban or rural location, type of education, baseline grade, gender, and age, using characteristics recorded before the event. This avoids, for example, comparing a rural primary class directly with an urban secondary class. In the main comparison I exclude controls in the same municipality and education level to limit local exposure to the event; I later examined their inclusion, with figures withheld where related tables could reveal small groups. Matching on recorded characteristics does not make family, school, or local conditions identical. <!-- CLAIM: P3-02 -->

I keep **2005–2015** and **2016–2024** separate because the documentary rules for recognising a loss of provision differ. Combining them would imply one uniform exposure that the sources cannot establish. A school that changes code, or transfers most pupils to another site, calls for scrutiny: a disappearing identifier alone is not proof that educational provision disappeared. My classification is an operational research rule, not a legal determination about a school or a complete reconstruction of where every pupil studied next. The historical classification uses information from after G, so it could not have been applied in real time with the data then available. The starting register does not give every cohort the same length of follow-up, so I specify the denominator and observation window again for each question. <!-- CLAIM: P3-03 -->

**How to read the numbers.** A percentage point is the difference between two percentages: if one rate were 12% and another 10%, the gap would be 2 points, not a 2% relative increase. I obtain uncertainty intervals by resampling schools. Period summaries use **98.75%** intervals for the family of primary results; individual years use **95%** intervals. These ranges describe uncertainty under that procedure and its assumptions. They are not the probability that a fixed, already calculated interval contains the true value, and they do not automatically cover misclassified events, incomparable groups, or schooling outside the records. <!-- CLAIM: P3-04 -->
{: .notice--info}

## Spoonful 1: Did pupils progress to the expected grade?

This question matters even when a pupil remains enrolled. A change of school may coincide with an interruption, a different programme, or a delay. I began with pupils in regular education from the first year of primary school through the second year of secondary school whose baseline grade was interpretable one year before G. In **G+1**, I asked whether their recorded grade was at least two grade levels above that starting point: the grade expected **two academic years after the baseline** under regular progression. The measure does not directly observe learning. I record a lack of **observed** progression when I find no linkable enrolment or when a valid grade falls below that threshold. If a pupil has an enrolment record but its grade is ambiguous or cannot be mapped onto this scale, I mark progression as unknown rather than automatically counting failure; that uncertainty needs its own bound. <!-- CLAIM: P3-05 -->

Within groups comparable on earlier characteristics, I compare the chance of lacking observed progression between pupils from event schools and controls. This is an adjusted difference in **post-event levels**. It does not subtract an earlier change from a later one, as a difference-in-differences design would. For **2005–2015**, the pooled contrast was **+9.58 percentage points**, with an interval from **+6.83 to +15.87**; it drew on **61,597** treated pupil–cohort observations and **1,143,559** control observations with enough information for comparison. For **2016–2024**, it was **+4.98 points**, interval **+2.65 to +8.16**, from **9,242** treated and **181,532** control observations. A pupil–cohort observation need not be a unique person across the whole series. In each period the comparable event group has more difficulty progressing in the **register**. Neither estimate measures harm caused by losing the school. <!-- CLAIM: P3-06 --> <!-- CLAIM: P3-07 -->

The full annual series matters because a pooled number can hide variation. This definition yields **20 estimable annual cohorts**, from 2005 through 2024. Their intervals are **95%**; the estimates differ and some intervals include zero. For example, **2017** has **+1.96 points**, interval **−1.64 to +8.09**, whereas **2024** has **+1.90**, interval **−2.19 to +8.62**. I have not selected only the years that agree with the period summary. An annual interval crossing zero does not establish equal trajectories either: under the available data and procedure, that particular contrast cannot settle a single direction precisely. <!-- CLAIM: P3-08 -->

{% assign reset_figure = site.data.tesis_reset_figures["post3-grade_progression_or_lag-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset" %}

{% assign reset_figure = site.data.tesis_reset_figures["post3-grade_progression_or_lag-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset" %}

Being **enrolled** and having a **classifiable grade** are different. To check what missing grades can change, I fixed the starting population before excluding unknown grades and assigned those cases first to progression and then to lack of progression. The range compatible with those extreme assignments was **+6.00 to +12.90 percentage points** in 2005–2015 and **+3.02 to +7.19** in 2016–2024. These are **bounds** for incomplete information, not confidence intervals. They need not surround the earlier point estimates: they retain a different baseline population that includes unknown cases. Under this exercise the descriptive progression gap remains positive, while its cause remains unresolved. <!-- CLAIM: P3-09 -->

The first answer is therefore deliberately narrow. In years and groups with enough comparable data, pupils from schools that lost provision show more lack of **recorded** progression. I cannot yet separate the part due to the event from earlier differences, incomplete measurement, or a mixture of these. The next signal is simpler to define but easier to misread: what does it mean when a pupil stops appearing in the register?

## Spoonful 2: Who disappears from the enrolment records for two years?

For an education authority, losing a pupil's administrative trail is a practical warning: it becomes harder to check whether the pupil found a place and continued studying. To avoid treating ordinary school completion as an absence, I start here with pupils in the first year of primary school through the first year of secondary school. I define **two years without observed enrolment** as no positive, linkable school record in **either G+1 or G+2**, after enrolment at the school of origin. A valid record in either year makes this outcome negative. I again compare initially enrolled pupils at event schools with controls within sufficiently populated comparable groups, but the denominator now includes only baseline grades and cohorts with a complete two-year window. <!-- CLAIM: P3-10 -->

For **2005–2015**, the pooled difference was **+1.94 percentage points**, interval **+1.32 to +2.83**, with **58,960** treated observations and **1,087,452** controls. For **2016–2023**, it was **+1.13 points**, interval **+0.23 to +2.56**, with **7,879** and **155,145** observations respectively. The **2024** cohort is excluded from this outcome: its second later year falls beyond the available school panel. Calling that missing year zero would artificially depress the outcome. The modern window ends earlier than the progression window because follow-up is incomplete, not because the result for 2024 was favourable or unfavourable. <!-- CLAIM: P3-11 --> <!-- CLAIM: P3-12 -->

Scale helps here. A **1.94-point** difference is roughly two additional observations without enrolment per hundred initial observations **relative to the comparable group on the contrast's scale**. It is not a rate per school closure, and this figure does not by itself identify particular people. Nor is "not enrolled in this panel" the same as leaving education: individual linkage may fail, a source may be incomplete, a pupil may study outside the system covered, or another route may be unobserved. The database tells me where there is a record **within its coverage**, not the true educational status of each apparent absence. <!-- CLAIM: P3-13 -->

Annual variation again rules out a universal claim. In **2020**, the contrast is **−0.50 points**, interval **−1.56 to +1.55**; in **2023**, it is **−1.12**, interval **−1.60 to −0.40**. Both are counterexamples to saying that every modern cohort has a positive difference. The pooled modern figure summarizes a mixture of cohorts and weights, not a law governing each year. I also do not treat the negative 2023 contrast as evidence that a closure protected enrolment: selection, classification, and coverage remain unresolved. <!-- CLAIM: P3-14 -->

{% assign reset_figure = site.data.tesis_reset_figures["post3-persistent_nonenrollment_two_years-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset" %}

{% assign reset_figure = site.data.tesis_reset_figures["post3-persistent_nonenrollment_two_years-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset" %}

What can I say about a pupil **actually** being out of school? Holding the starting population fixed and allowing schooling states consistent with the missing information yields bounds from **−2.82 to +4.76 points** in 2005–2015 and **−1.76 to +2.89** in 2016–2023. Both signs remain possible. This exercise concerns **true non-schooling**, while the previous figures concern **absence from the observed register**: these are different outcomes. The bounds are not confidence intervals and cannot turn an administrative warning into a dropout count. <!-- CLAIM: P3-20 -->

{% assign reset_figure = site.data.tesis_reset_figures["post3-sensitivity-bounds"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset/sensitivity" %}

A sensible response to a missing record is to check the pupil's circumstances through administrative and human follow-up. That is a precaution, not a forecast of how many departures a closure caused. A better estimate of **real** absence would require validated linkage to other sources and an audit of records with invalid identifiers. The third spoonful poses a harder question for the comparison itself: were the groups already different?

## Spoonful 3: What changes when the comparison is made more demanding?

Earlier differences can change the reading. I measure enrolment continuity from **G−2 to G−1** in a different starting population from the primary comparison, without adjustment or an uncertainty interval. Its **37 observed outcome records cover 19 event cohorts (2006–2024)**, not 37 independent tests. In the **15 cohorts with both rates public**, continuity is lower at schools that later lose provision: descriptive differences calculated from rounded rates range from **0.1 to 8.2 percentage points**. One rate is withheld for privacy in four other cohorts. The published rates for the two outcomes match to one decimal place, although their control populations are not identical. This indicator neither quantifies nor corrects the primary contrast, and does not prove anticipation. <!-- CLAIM: P3-15 -->

That pattern challenges an assumption that the groups were interchangeable before the event. It cannot decide whether the gap reflects anticipation of a known loss of provision, pre-existing vulnerability, changing composition, or another process. Calling it anticipation would require evidence that the decision was known, or already affecting behaviour, before G. I therefore compared the gap for an earlier generation with the gap for the generation near the event, starting at G−4 and G−1 with equivalent follow-up. This is a **difference in differences**: a difference between two gaps. It might remove a stable disadvantage if its assumptions hold; it cannot automatically remove a disadvantage that changes over time (Roth et al. 2023). <!-- CLAIM: P3-16 -->

{% assign reset_figure = site.data.tesis_reset_figures["post3-anticipation-grade_progression_or_lag-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset/anticipation" %}

{% assign reset_figure = site.data.tesis_reset_figures["post3-anticipation-grade_progression_or_lag-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset/anticipation" %}

The four pooled results below are in percentage points, with 95% school-based intervals. The historical comparison begins in **2008** because it needs the earlier generation; I do not extend it artificially back to 2005. <!-- CLAIM: P3-16 -->

| Outcome | Era and cohorts | Difference between gaps | 95% school interval |
|---|---|---:|---:|
| Lack of observed progression | Historical, 2008–2015 | +4.36 | +2.07 to +8.60 |
| Lack of observed progression | Modern, 2016–2024 | +0.40 | −1.74 to +2.50 |
| Two years without observed enrolment | Historical, 2008–2015 | +0.45 | −0.30 to +1.23 |
| Two years without observed enrolment | Modern, 2016–2023 | +0.28 | −0.47 to +1.14 |
{: .table--compact .table--scroll}

**The question has changed, not just the number.** The primary results compare later levels; this table compares gaps across generations. Subtracting one from the other cannot tell me what share of presumed harm was explained. Three intervals span zero, leaving differences in either direction possible; this does not prove no effect. The historical progression interval stays above zero, but the earlier differences and comparison conditions still prevent a causal reading. <!-- CLAIM: P3-16 -->
{: .notice--info}

One pupil may appear in several cohorts, and one school in several years. To acknowledge both dependencies I also calculated diagnostic intervals grouped by **school and pupil**. In table order they are **+0.90 to +7.81**, **−1.78 to +2.58**, **−0.31 to +1.20**, and **−0.49 to +1.05 points**. They use an asymptotic method distinct from school resampling and retain a warning about weak-cluster precision. I do not choose whichever interval gives a preferred sign. Neither method establishes identification. <!-- CLAIM: P3-16 -->

{% assign reset_figure = site.data.tesis_reset_figures["post3-sensitivity-did"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset/sensitivity" %}

I also widened the operational definition of lost provision. In the modern era, the wider **D1** rule and the flow-refined **D2** rule change which pupils and schools enter the comparison. On their full samples, lack of progression goes from **+4.98 points under D2 to +1.88 under D1**; absence from the register goes from **+1.13 to +0.33**. On the common sample, however, both rules give exactly **+4.96** and **+1.11 points**, respectively. This equality follows from shared exposure and outcome for those observations; it is not independent confirmation. The full-sample gap reflects composition and support, and there is no joint interval here to establish a statistically supported change. In the historical era the two rules select the same events, so that check cannot discriminate between them. <!-- CLAIM: P3-17 -->

{% assign reset_figure = site.data.tesis_reset_figures["post3-sensitivity-d1-d2"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset/sensitivity" %}

Other checks place limits on what can be shown. The local-control comparisons and three of four receiver-school filters have been computed, but their figures are withheld to prevent small groups being reconstructed by subtracting related tables. A withheld estimate is neither zero nor evidence of robustness. Receiver-school filtering also selects a situation after the event; it cannot by itself explain the trajectory. Giving each cohort equal weight leaves positive point differences in all four main pooled combinations, but that sensitivity has no dedicated intervals. Exploratory windows before, overlapping, and after the pandemic neither identify a pandemic effect nor justify centring the account on a chosen subperiod. <!-- CLAIM: P3-17 --> <!-- CLAIM: P3-22 -->

### A secondary look at attendance and marks

I also compared changes in attendance and marks from G−1 to G+1, but only for pupils with valid records in both years. This selection matters: the share with both records lies in the **65–70%** band among historically exposed pupils, versus **85–90%** among controls; in the modern era it is **70–75%** versus **90–95%**. The bands reduce the risk of reconstructing small groups; they do not guarantee anonymity and are not confidence intervals. I cannot assume pupils missing from this comparison followed the same path. <!-- CLAIM: P3-21 -->

| Measure and unit | 2005–2015: difference in changes [95% CI] | 2016–2024: difference in changes [95% CI] |
|---|---:|---:|
| Attendance, percentage points | −0.31 [−0.73; +0.12] | −2.13 [−4.89; −0.08] |
| Mean mark, points on the 1–7 scale | −0.092 [−0.114; −0.068] | −0.041 [−0.093; +0.014] |
{: .table--compact .table--scroll}

These are exploratory results conditional on being observed, not general effects on learning. The attendance variants excluding zero values were also calculated, but their figures are withheld because a group is small; I do not use them to reinforce a direction. <!-- CLAIM: P3-21 -->

The third spoonful ends with a distinction: a later gap and a difference between changes answer different questions. The evidence calls for preserving both, explaining each sample's composition, and acknowledging figures that cannot be published. An effect claim would require a defensible account of how these pupils would have fared without the loss of provision; more subtraction alone cannot supply that account.

## What I learned, and what remains

I have answered three different questions. First, **recorded** grade progression is worse among pupils from event schools in comparable samples in each era, and missing-grade bounds preserve a positive difference for their fixed baseline population. Second, two-year gaps in the observed register are more frequent in the pooled results, but bounds for true non-schooling admit both signs. Third, enrolment continuity already differs before the event, and the diagnostic comparison between generations does not turn the later gap into harm caused by the event. The event definition also changes the composition of the comparison. <!-- CLAIM: P3-18 -->

The next challenges are to verify destinations and schooling outside the observed coverage, distinguish genuine loss of provision from administrative continuity, and build earlier comparisons that can sustain a causal interpretation. A transition policy can use these signals to check school places, travel, and continuity without calling them a count of harm caused. I will revise the conclusion if linked sources and better supported comparators change the results; retaining a sign under some sensitivities does not end the inquiry.

> **Correction note.** This revision reconstructs event classification, population, measured question, and uncertainty relative to the earlier edition. Its earlier figures answered a different comparison and are not comparable with these. <!-- CLAIM: P3-19 -->

## References

- Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen, and Nina Smith. 2018. ["The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?"](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47. [Scholar](https://scholar.google.com/scholar_lookup?title=The+short-term+effects+of+school+consolidation+on+student+achievement%3A+Evidence+of+disruption%3F&doi=10.1016%2Fj.econedurev.2018.05.004)
- Brummet, Quentin. 2014. ["The Effect of School Closings on Student Achievement."](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–124. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effect+of+school+closings+on+student+achievement&doi=10.1016%2Fj.jpubeco.2014.06.010)
- Chilean Ministry of Education. n.d. "Student-level enrollment." Open Data Portal. <https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/>. Local extracts and transformations are documented in this revision’s protocol; the portal does not itself certify those files.
- Elacqua, Gregory, Matías Martínez, Humberto Santos, and Daniela Urbina. 2012. ["School Closures in Chile: Access to Quality Alternatives in a School Choice System."](http://www.scielo.cl/pdf/ede/v39n2/art05.pdf) *Estudios de Economía* 39 (2): 179–202. [DOI](https://doi.org/10.4067/S0718-52862012000200005) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closures+in+Chile%3A+Access+to+quality+alternatives+in+a+school+choice+system&doi=10.4067%2FS0718-52862012000200005)
- Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. ["Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?"](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203. [Scholar](https://scholar.google.com/scholar_lookup?title=Closing+schools+in+a+shrinking+district%3A+Do+student+outcomes+depend+on+which+schools+are+closed%3F&doi=10.1016%2Fj.jue.2011.10.001)
- Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. ["School Closure and Educational Attainment: Evidence from a Market-Based System."](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf) *Economics of Education Review* 65: 1–17. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)
- Roth, Jonathan, Pedro H. C. Sant’Anna, Alyssa Bilinski, and John Poe. 2023. ["What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature."](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–2244. Methodological reference for assessing trends, not evidence of identification in these data. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)
