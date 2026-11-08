---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extending my thesis in 3 spoonfuls (part IV): higher education enrollment traced from students' school of origin"
subtitle: "The earlier and later school cohorts at schools that lost provision differ from controls; their difference in changes is descriptive, and total-access estimates are imprecise."
date: 2026-11-04 10:00:00 -0300
categories: [data, education, public-policy]
tags: [education, school-closure, higher-education, sies, administrative-data, public-policy]
description: "Higher-education enrolment, destinations, persistence, and qualifications after a loss of school provision: comparable cohorts and limits of inference."
excerpt: "I compare earlier and later cohorts from schools that lost provision and from control schools, distinguishing enrolment, destinations, persistence, and qualifications without treating the contrast as causal."
author: clabra
lang: en
ref: cierre-escolar-educacion-superior-causal-ml
permalink: /datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/
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
  teaser: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/og-1200x630.webp
  og_image_alt: "Nocturnal editorial illustration of student pathways departing from a closed high school and branching toward university campuses and vocational-technical institutes, representing the separation between pre-existing selection and causal effect."
  overlay_image: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/teaser-mobile-640x360.webp
visual_id: cierre-escolar-educacion-superior-causal-ml
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

{% include thesis-series-nav.html current=4 %}

The consequences of losing school provision may only become visible years later, when a cohort reaches higher education. A family wants to know more than whether a child found another school place: did the pupil later appear in further study, remain enrolled, or complete a qualification? I followed cohorts from Chilean secondary schools that lost provision and comparison schools through school records and the Higher Education Information Service (*Servicio de Información de Educación Superior*, SIES). Observed higher-education enrolment is lower at event schools **in both cohorts being compared**. After I subtract the changes in the two groups, the pooled contrasts for total access are negative, but their intervals include negative, zero, and positive values. That subtraction does not turn the contrast into an effect of closure. <!-- CLAIM: P4-01 -->

Earlier research explains why I look beyond school enrolment, without predicting an answer for Chile. Grau, Hojman, and Mizala (2018) study dropout and grade retention after Chilean closures, and Elacqua and colleagues (2012) show that nearby quality alternatives are not equally available to families. On later education, Larsen (2020) finds lower graduation and college attendance after Milwaukee high-school closures; Bross, Harris, and Liu (2023) find different outcomes by city and grade level when Louisiana schools close and restart as charters; and Kim (2024), in a Texas working paper, reports postsecondary consequences. These events, populations, and designs differ from the loss of provision studied here: they motivate the questions but cannot turn my contrasts into causal effects.

Part III of this series follows pupils' immediate school trajectories. Here I look further ahead without merging the two questions. I call the event year **G** and start with pupils enrolled at their school of origin in **G−1**. I calculate an expected school-completion year from each pupil's baseline grade and calendar year, assuming regular progression. I then search SIES for undergraduate enrolment in **the two years after expected school completion**. The clock follows that grade and calendar year, not each person's observed departure or graduation. Nor does this measure a person's first-ever entry into higher education: earlier SIES history was not checked to impose that condition. School delays and later study decisions can therefore both affect the measure. The denominator includes all eligible pupils in the initial school cohort with valid identification and complete follow-up, including those who never appear in SIES; it is not restricted to entrants. <!-- CLAIM: P4-02 -->

The series begins in **2009** because the earlier cohort requires school records from **G−5**, and those records begin in **2004**. I separate **2009–2015** from **2016–2024** because the historical and modern event rules draw on different evidence of lost provision. I do not pool them as a single experience. Modern access can be measured through 2024, but the mix of baseline grades changes near the panel's end: in 2023 and 2024 only the third year of secondary school has enough comparable data. Persistence reaches 2023, again with only that grade at the endpoint; for qualifications, 2019 contributes only the third grade of secondary school. Most excluded grades need longer follow-up. The second year of secondary school in 2023 does have a complete window, but lacks an eligible comparison. These boundaries follow data availability and comparability, not the sign of an estimate. Upper-primary comparisons need their own analysis and are not reported here as estimated results. Treating recent years as if they contained the same mix of baseline grades would mislead. The common-coverage sensitivity therefore requires years with eligible comparisons in the first, second, and third grades of secondary school; it is not a third-grade-only analysis. <!-- CLAIM: P4-03 -->

**How I read the comparisons.** A percentage point is the difference between two rates expressed as percentages. The **primary** intervals for total access are **97.5%** and those for destinations **98.75%**, reflecting separate families of comparisons; persistence and qualifications use **95%** intervals. I resample schools rather than isolated pupils because pupils in one school may share circumstances. An interval including zero leaves the direction unresolved under the procedure; it does not prove equality. Nor can any such interval, by itself, absorb a misclassified school, a missed individual link, or different trends that would have occurred without the event. <!-- CLAIM: P4-04 -->

The [methodological annex]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}) documents the calendar, definitions, coverage, and sensitivity checks; the three spoonfuls can be read on their own.

## Spoonful 1: How does the gap change between cohorts?

If enrolment at schools that later lose provision differs from that at control schools across school cohorts, looking only at the cohort closer to the event would overstate what I know about the event. I therefore compare **two cohorts in the same baseline grade** at each school: an earlier cohort enrolled **five years before** G, and a later cohort enrolled **one year before** G. I then compare their changes with those at schools matched on event year, region, administrative sector, urban or rural location, type of education, and baseline grade. Controls have no detected loss-of-provision event in the 2005–2024 inventory. That choice favours schools that survived the inventory and may bias the comparison. I retained controls in the same municipality to preserve local comparability and support, although displaced pupils might enrol there; excluding those controls remains a necessary check. These are different cohorts, **not the same people observed before and after**. <!-- CLAIM: P4-05 -->

**Earlier and later name school cohorts, not two sets of outcomes measured entirely before and after the event.** For an event in 2016, a pupil who was in the first year of secondary school in the earlier cohort in 2011 would be expected to finish school in 2014 and have an observed-access window in 2015–2016. Part of that window coincides with the event year. I have not verified that every pupil actually finished school before the event either. This is an illustration of the calendar, not an empirical observation. The comparison describes differences between cohorts; on its own, it does not show that the higher education gap was entirely measured before the loss of provision. <!-- CLAIM: P4-05 -->

The historical period shows why all four rates matter. In **2009–2015**, observed higher-education enrolment within the window was **45.87%** in the earlier cohort and **48.56%** in the later cohort at event schools. The corresponding control rates were **60.43%** and **65.43%**. The earlier cohort also shows a level disadvantage. The event-school increase was smaller than the control increase, and the pooled adjusted contrast was **−2.31 percentage points**, interval **−5.26 to +0.29**. The later cohort contributed **10,183** pupil–cohort observations from event schools and **1,208,182** controls; **73** event schools appeared across the two cohorts. Those pupil counts refer to the later cohort, not the total behind all four rates. Each comparable cell is weighted by its exposed pupils. The four published rates use those same weights, so subtracting their changes reconstructs the contrast, apart from rounding. <!-- CLAIM: P4-06 -->

In **2016–2024**, event-school rates were **55.93% earlier** and **55.01% later**, compared with **66.17%** and **67.68%** in controls. The pooled contrast was **−2.43 points**, interval **−5.67 to +1.27**, with **2,916** later-cohort observations at event schools, **806,153** controls, and **27** event schools across both cohorts. Precision is fragile: few event schools contribute, and some carry considerable weight. It has also not been verified that every control remained free of a similar event throughout observation. I cannot describe the difference between the two period estimates as a demonstrated trend: event rules, samples, and eligible baseline grades differ. <!-- CLAIM: P4-07 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-access-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-access-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

As a check on the timing definition, I also looked for enrolment only in the **first year after expected school completion**. The contrast is **−1.71 points** in 2009–2015, interval **−4.04 to +0.17**, and **−2.10** in 2016–2024, interval **−5.56 to +1.57**; these intervals are at 95%. This still does not establish anyone's first-ever entry or separate a school delay from a delay in continuing study. <!-- CLAIM: P4-18 -->

Subtracting changes removes a **fixed gap** only under demanding conditions. If the groups would have changed differently without the event, if controls received displaced pupils, or if event schools were already changing, the contrast does not identify the event's effect. A difference in changes needs a defensible account of the paths both groups would have taken without the event (Roth et al. 2023). There is a second, separate uncertainty: conservative national-capacity bounds for invalid identifiers are too wide to constrain direction, at **−80.95 to +74.03 points** historically and **−71.70 to +66.18** in the modern period. These are neither confidence intervals nor measured error rates for either group. They show why an apparently precise sample estimate cannot settle a separate linkage problem. <!-- CLAIM: P4-08 -->

### Does the choice of controls change the comparison?

I repeated the calculation with stable school characteristics, controls in a different municipality, years with all three baseline grades supported, and an additional adjustment for baseline age and gender. Across those four variants, the total-access point estimates remain negative in both eras, but these versions change the population or its weights; a matching sign does not prove equivalence.

A fixed-effects diagnostic gives **−2.47 points**, **95%** interval **−4.85 to −0.21**, for historical access, versus the primary **−2.31**, **97.5%** interval **−5.26 to +0.29**. It uses different weights, targets another estimand, and has a different confidence level; different zero crossings are not a test of the difference between estimators.

With **only controls that lose provision later**, historical access becomes **+0.73 points** under the school-exposure horizon and **+1.03** under the outcome horizon. Their 97.5% intervals are **−2.86 to +4.14** and **−2.96 to +4.68**. The later-cohort treated sample is smaller than in the primary estimate. The sign reversal alone does not establish bias in the primary estimate: the comparison changed. The figure retains the modern variants and their periods too, rather than selecting only results that agree. With future-event controls alone, the modern school-exposure comparison has support for events **2016–2019**; under the complete outcome horizon, support is limited to **2016–2018**: later years lack eligible controls for all four rates, and some grades also lack follow-up. The inventory retains years through 2024 as unsupported or censored states, never zeros. <!-- CLAIM: P4-19 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-sensitivity-comparison-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset/sensitivity" csv="post4-sensitivity-comparison-all.csv" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-sensitivity-comparison-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset/sensitivity" csv="post4-sensitivity-comparison-all.csv" %}

[Accessible comparison table]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-comparison-table-en.html' | relative_url }})

<details class="post3-methods">
<summary>View all 22 comparison contrasts and their intervals</summary>
<div class="tabla-desliza" role="region" tabindex="0" aria-label="Comparison sensitivities. Person counts are omitted to protect privacy.">
{% include tesis-reset-tables/post4-sensitivity-comparison-table-en.html %}
</div>
</details>

### Were the earlier-cohort outcomes entirely before the event?

I compared two still-earlier baseline cohorts, starting in G−6 and G−5. For modern access, that contrast is **−3.12 points**, **97.5%** interval **−5.24 to −0.68**. The historical counterpart is close to zero: **−0.35**, interval **−1.55 to +0.82**. The modern result shows a gap between earlier cohorts too, but some of their outcome windows reach the event year: it is not a clean test of wholly prior trends and does not attribute the gap to anticipation.

Requiring **both windows to end before G** removes pupils who began in the first year of secondary school: the contrast becomes **−2.28**, interval **−5.09 to +0.70**, for 2016–2024 events. Support and weights change, so subtracting these estimates does not measure contamination, and the interval crossing zero does not confirm parallel trends. The earlier G−7 versus G−6 comparison gives **−1.17**, interval **−3.15 to +1.13**, with access windows wholly before the event in this era. I retain both checks.

Historically, the late comparison covers **2010–2015**: in 2009 the first baseline grade lacks support and the second and third have incomplete windows. The early comparison covers **2011–2015**: all three grades are censored in 2009; in 2010 the first lacks support while the others are censored. School enrolment records begin in 2004 and SIES in 2007: moving cohorts to G−7/G−6 can leave a missing school baseline or an incomplete SIES window. The status of excluded years remains visible. For undergraduate qualifications, neither comparison has baseline grades for which both complete outcome windows end before the event: that diagnostic is not estimable under the fixed calendar. <!-- CLAIM: P4-20 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-sensitivity-calendar-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset/sensitivity" csv="post4-sensitivity-calendar-all.csv" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-sensitivity-calendar-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset/sensitivity" csv="post4-sensitivity-calendar-all.csv" %}

[Accessible calendar table]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-calendar-table-en.html' | relative_url }}) · [Accessible window matrix]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-calendar-window-matrix-en.html' | relative_url }})

<div class="tabla-desliza" role="region" tabindex="0" aria-label="A/B calendar. Person counts are omitted to protect privacy.">
{% include tesis-reset-tables/post4-sensitivity-calendar-table-en.html %}
</div>

<details class="post3-methods">
<summary>View complete outcome windows by baseline grade</summary>
<div class="tabla-desliza" role="region" tabindex="0" aria-label="Window ends relative to event year G; G is not strictly before the event. B requires both generations to end before G, plus observed support.">
{% include tesis-reset-tables/post4-sensitivity-calendar-window-matrix-en.html %}
</div>
</details>

The first answer describes relative changes. I see a level disadvantage in both cohorts, while the total-access intervals include negative, zero, and positive values. I cannot claim that the event reduced higher education enrolment or that it had no effect. Before asking about continuing in higher education, I need to distinguish **where the enrolment records lead** within the same window.

## Spoonful 2: Which destinations appear in the records?

"Higher education" can conceal quite different routes. I place every eligible pupil from the initial school cohort into one of four **mutually exclusive** categories in the same two-year window: university only; professional institute or technical training centre only (**IP/CFT**); both types; or no undergraduate enrolment found in the linked SIES extract. "None recorded" does not show that someone never studied, would not enter later, or valued one route less than another. For each destination I compare the change between event-school cohorts with the change between control cohorts. The four categories share the same initial denominator and together account for everyone in it. <!-- CLAIM: P4-09 -->

The table keeps all four destinations and their uncertainty. Each entry is the difference between the two groups' changes, in percentage points; intervals are **98.75%** within each period. Within each era, the categories share the eligible baseline cohort used for total access; **27** event schools contributed across both cohorts in the modern era. <!-- CLAIM: P4-10 --> <!-- CLAIM: P4-11 -->

| Destination recorded within two years | 2009–2015: contrast (interval) | 2016–2024: contrast (interval) |
|---|---:|---:|
| University only | −2.07 (−4.18 to −0.23) | +0.83 (−2.59 to +3.88) |
| IP/CFT only | −0.31 (−2.97 to +2.40) | −2.61 (−5.51 to +1.00) |
| Both types | +0.07 (−0.33 to +0.43) | −0.64 (−1.93 to +0.18) |
| None recorded | +2.31 (−0.61 to +5.58) | +2.43 (−1.68 to +6.05) |
{: .table--compact .table--scroll}

In the historical period, the university-only interval is wholly negative. I can describe that direction in the **descriptive contrast**, without attributing it to the event. In the modern period, every destination interval allows both signs and the comparison relies on few event schools; no single direction of redistribution is resolved. An interval spanning zero does not establish that destinations were equal. <!-- CLAIM: P4-10 --> <!-- CLAIM: P4-11 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-destinations-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-destinations-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

Differences between aggregate categories do not demonstrate that **individuals switched destinations**. A lower "IP/CFT only" contrast alongside a higher "none recorded" contrast cannot tell me that the same people exchanged one route for the other. I would need individual histories of options and timing, and a defensible causal comparison. Starting circumstances, attainment, and family resources may shape both school enrolment and later study. Adjustment for recorded characteristics cannot reveal everything unmeasured. "None recorded" is the arithmetic complement of two-year access, not independent evidence. Its intervals differ because the destination family uses **98.75%** and total access **97.5%**. The next question needs an even longer clock: who remains enrolled and who obtains a qualification?

## Spoonful 3: What do persistence and qualifications show?

An initial enrolment record is not a whole educational trajectory. I define **persistence** as SIES enrolment in at least **two of the three distinct years** beginning with the first year after expected school completion. The two years need **not be consecutive**. I define **qualification** as at least one recorded undergraduate award within **six inclusive calendar years** from that same first year. For both outcomes I compare the cohort changes at event schools with those at controls. I count every eligible pupil in the initial school cohort with complete follow-up, including those who never recorded higher-education entry. These are **not rates among entrants**. I exclude a cohort that has not yet had enough time rather than coding its unfinished window as zero. <!-- CLAIM: P4-12 -->

For persistence in **2009–2015**, the pooled contrast was **−3.13 points**, interval **−5.30 to −1.20**. In **2016–2023**, it was **−1.90**, interval **−5.01 to +1.31**. The modern series ends in 2023 because the next cohort lacks the complete three-year window. The historical contrast has a negative direction under this descriptive comparison. The modern contrast is less precise, rests on **26** event schools, and allows both an adverse and a favourable difference. I therefore cannot conclude that modern persistence was unchanged. <!-- CLAIM: P4-13 -->

For qualifications in **2009–2015**, the pooled contrast was **−1.47 points**, interval **−2.69 to −0.28**. In the modern period, only **2016–2019** has the stipulated horizon: the contrast there was **−2.28 points**, interval **−5.56 to +0.71**, with **16** event schools across both cohorts. Those mature years do not replace the modern access window through 2024. So few mature event schools sharply limit precision and any subgroup reading. These secondary-outcome intervals are **95%** and still do not incorporate uncertainty about linkage and classification. <!-- CLAIM: P4-14 -->

These outcomes also change with the calendar and comparator. For modern persistence, the late comparison between earlier cohorts is **−2.41 points**, **95%** interval **−4.50 to −0.07**, over 2016–2024; some outcome windows reach G, so this does not test wholly prior trends. With only controls whose event occurs after the outcome horizon, modern persistence is **−10.02 points**, interval **−19.51 to −0.81**, over 2016–2017 with **four event schools**; historical qualifications are **+4.05**, interval **−0.64 to +8.80**, over 2009–2014 with **27 event schools**. These descriptive contrasts use different samples and weights; they neither establish a difference from primary nor identify an effect of closure. Precision is especially weak with four event schools. <!-- CLAIM: P4-19 --> <!-- CLAIM: P4-20 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-followup-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-followup-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

### Two further checks that do not change the reading

Do these contrasts differ among groups? I compared groups defined by baseline grade, school administrative sector, rurality, and region before the event. Of **800 prespecified pairwise contrasts**, **388** could be estimated and **412** lacked support or were withheld for privacy. **34** have a Holm-adjusted p-value below 0.05: a signal under the fixed tests, not the probability that a hypothesis is true. The Holm (1979) adjustment operates within each outcome-by-era family, not across all 800 comparisons. The 34 are not independent discoveries: access and no-record outcomes are complements and duplicate some contrasts. I do not turn these exploratory results into a map of pupils "most affected" or into causal mechanisms. <!-- CLAIM: P4-21 -->

I also assessed whether **doubly robust difference in differences** for repeated cross sections (Sant’Anna and Zhao 2020) was estimable; it combines models for group composition and outcomes. Its name does not make it immune to every error. Before estimating its effects, support or model-fit requirements failed in some strata in both eras; all eight outcomes are not estimable under that specification in each era. I did not discard difficult strata to manufacture an estimate. The flexible machine-learning route and its individual-level heterogeneity diagnostics were **not run**; I do not call them impossible or reuse old predictions as confirmation. <!-- CLAIM: P4-15 -->


The third answer combines a signal with a boundary. Persistence and qualifications show historical descriptive differences, while recent cohorts offer fewer mature years and fewer event schools, with wide intervals. For a family, that does not guarantee or foreclose a route. For an institution, it argues for preserving verifiable longitudinal information before assigning later outcomes to an earlier school decision.

## What I learned, and what remains

The three spoonfuls lead from a gap between school cohorts to later records. First, both cohorts at event schools show a **level gap** in higher-education enrolment relative to controls, while the contrasts in changes for total access remain imprecise. Second, university, vocational and technical, mixed, and no-record destinations differ, but aggregates alone cannot show individual substitutions caused by the event. Third, persistence and qualifications require longer follow-up, and fewer schools support mature modern estimates. Exploratory subgroups do not turn these contrasts into causal profiles, and the DR-DiD feasibility failure supplies no further estimate. I have described what appears in the records and what each comparison can support. Causal identification remains open. <!-- CLAIM: P4-16 -->

The remaining challenges are to validate individual links, follow possible control events beyond the inventory, and support comparisons that preserve population and calendar. The computed sensitivities show why that matters: some keep the direction and others change sign along with the sample. None alone establishes what would have happened without the loss of provision. Recording places, transfers, and progress toward school completion is a prudent way to support pupils now. This analysis does not quantify how much later study changed **because of** losing school provision.

> **Correction note.** This reconstruction changes the population, follow-up calendar, measured question, and uncertainty assessment from the earlier edition. Its machine-learning estimates and figures concerned another comparison and must not be mixed with these results. <!-- CLAIM: P4-17 -->


## References

- Bross, Whitney, Douglas N. Harris, and Lihan Liu. 2023. ["The Effects of Performance-Based School Closure and Restart on Student Performance."](https://doi.org/10.1016/j.econedurev.2023.102368) *Economics of Education Review* 94: 102368. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effects+of+performance-based+school+closure+and+restart+on+student+performance&doi=10.1016%2Fj.econedurev.2023.102368)
- Chilean Ministry of Education. n.d. "Student-level enrollment." Open Data Portal. <https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/>. Local extracts and transformations are documented in this revision’s protocol; the portal does not itself certify those files.
- Elacqua, Gregory, Matías Martínez, Humberto Santos, and Daniela Urbina. 2012. ["School Closures in Chile: Access to Quality Alternatives in a School Choice System."](http://www.scielo.cl/pdf/ede/v39n2/art05.pdf) *Estudios de Economía* 39 (2): 179–202. [DOI](https://doi.org/10.4067/S0718-52862012000200005) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closures+in+Chile%3A+Access+to+quality+alternatives+in+a+school+choice+system&doi=10.4067%2FS0718-52862012000200005)
- Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. ["School Closure and Educational Attainment: Evidence from a Market-Based System."](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf) *Economics of Education Review* 65: 1–17. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)
- Higher Education Information Service (SIES). n.d. "Bases de datos de estudiantes matriculadas y matriculados en Educación Superior en Chile" and "Base de datos de estudiantes tituladas y titulados en Educación Superior en Chile". Mi Futuro, Chilean Ministry of Education. <https://www.mifuturo.cl/bases-de-datos-de-matriculados/>; <https://www.mifuturo.cl/bases-de-datos-titulados/>. Local enrollment and awards extracts are documented separately.
- Holm, Sture. 1979. "A Simple Sequentially Rejective Multiple Test Procedure." *Scandinavian Journal of Statistics* 6 (2): 65–70. <https://www.jstor.org/stable/4615733>.
- Kim, Jeonghyeok. 2024. ["The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes."](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963, Annenberg Institute at Brown University. Working paper, not a peer-reviewed journal article. [Scholar](https://scholar.google.com/scholar_lookup?title=The+Long+Shadow+of+School+Closures%3A+Impacts+on+Students%27+Educational+and+Labor+Market+Outcomes&doi=10.26300%2FAX4M-3Z14)
- Larsen, Matthew F. 2020. ["Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment."](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980. [Scholar](https://scholar.google.com/scholar_lookup?title=Does+closing+schools+close+doors%3F+The+effect+of+high+school+closings+on+achievement+and+attainment&doi=10.1016%2Fj.econedurev.2020.101980)
- Roth, Jonathan, Pedro H. C. Sant’Anna, Alyssa Bilinski, and John Poe. 2023. ["What's Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature."](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–2244. Methodological reference on parallel trends, not an empirical test of those trends here. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)
- Sant’Anna, Pedro H. C., and Jun Zhao. 2020. ["Doubly Robust Difference-in-Differences Estimators."](https://doi.org/10.1016/j.jeconom.2020.06.003) *Journal of Econometrics* 219 (1): 101–122. Reference for a method assessed for feasibility; it produced no effect estimate here. [Scholar](https://scholar.google.com/scholar_lookup?title=Doubly+robust+difference-in-differences+estimators&doi=10.1016%2Fj.jeconom.2020.06.003)
