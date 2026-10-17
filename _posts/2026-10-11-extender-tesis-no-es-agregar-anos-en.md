---
layout: single
classes: [thesis-extension-post]
title: "Extending my thesis in three spoonfuls (part II): does education improve when schools open and close?"
subtitle: "More evidence on school turnover, its limits, and the questions it leaves for providers and Local Public Education Services."
date: 2026-10-11 10:00:00 -0300
last_modified_at: 2026-10-17 13:40:00 -0300
categories: [data, education, public-policy]
tags: [education, school-markets, school-closure, mineduc, administrative-data, replication, simce, admissions, slep, territory]
description: "An extension of my thesis examines school closures and openings in Chile: what administrative records show and what is still needed to assess quality, coverage, and continuity."
excerpt: "A school closing and another opening is not enough to know whether education improved. The records clarify turnover; its effects also require looking at students, providers, and territory."
author: clabra
lang: en
ref: extender-tesis-no-es-agregar-anos
permalink: /datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/
header:
  teaser: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/og-1200x630.webp
  og_image_alt: "Schools in different states and overlapping contours as a metaphor for closures and changes in education provision."
  overlay_image: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/teaser-mobile-640x360.webp
visual_id: extender-tesis-no-es-agregar-anos
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
  skip_reason: "Distribution paused until the public URL is verified and specific authorisation is received."
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
---

In [part I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) I confirmed a tension that still matters: in a system of closures and openings, moving provision does not by itself tell us whether opportunities to learn improved. This part asks what happens when one school leaves and another enters.

<span id="claim-causal-boundary"></span>**This analysis does not identify whether turnover improves or worsens educational outcomes.** That is not an elegant way of saying that the effect is zero. Some comparisons are imprecise; others lack enough comparable cases; and the records neither follow each student nor reconstruct what would have happened without the closure or opening.

Part I audited 1992–2012. Here I use directories from 2015 to 2025 to observe transitions from 2016 to 2025, and a 2013–2025 panel to detect entries. The period and questions differ; I do not re-estimate Part I's results.

Three results organise the account. First, the register contains **900 official closures**, but the stricter definition leaves **330 closures with enrolment** for comparison. Second, median enrolment falls sharply before closure, although that path does not reveal its cause. Third, only **38 closures** have a nearby opening in the same segment under the territorial criterion; proximity does not establish available places, accessibility, or student destination.

The contribution is a public question: **what continuity did the community receive, and who bore its costs?**

## Spoonful 1: before evaluating a closure, establish what changed

### Leaving the register does not always mean a school disappeared

In the first instalment, “entry” and “exit” described appearances and disappearances in the files. To study the recent period, I need to separate those from administrative changes and an actual interruption in education provision.

An establishment may close, enter recess, merge with another, change identifier, lose a site, or stop serving a level. It may also change provider—the entity responsible for managing it—without ceasing to operate. None of those situations should automatically become the same kind of closure.

The **RBD**, MINEDUC's identifier for each establishment, helps track its history but does not resolve it on its own. A code that disappears requires checking what happened to the school, its site, and its provision.

The panel follows establishments over the recent period. The directories begin in 2015, so the first observable transition is in 2016. The El Salvador case dates from 2013 and appears later as a separate historical case. The unit depends on the question: the inventory counts RBD events, identity work reconstructs establishments and sites, and comparisons use establishments within an education segment.

**Exercise.** I separate an actual closure from an administrative change. I define an official closure only as a transition from a non-closed status into code `3`. Recess is not closure; disappearance from the file remains an exit of unknown cause.

<span id="claim-event-count"></span>**Result.** There are **900 official closures**: 684 after activity, 215 after recess, and one after authorisation without enrolment. Of the 684 previously active schools, 346 had students and 338 already recorded zero enrolment. Closing an empty school is not the same as displacing a school community.
{: .text-justify}

Yet those 346 cases are not automatically 346 schools that disappeared. After reconstructing identity and provision, **330 strict closures of a school in the level it served** remain. The other 16 are site or annex closures, administrative consolidations, RBD replacements, or unresolved cases. Those links are inferred from official directories and excluded from the primary comparison; four further same-site replacement candidates are removed only from the spatial exercise.
{: .text-justify}

### Nearby provision does not necessarily serve the same need

Provision matters too. A nursery does not compete for the same population as a primary school or a secondary school. Official codes let us separate early childhood education into nursery, middle, transition, and mixed levels; I then distinguish primary and secondary education. From here on, a “market” means **commune and exact education segment**, not every institution in the same territory.
{: .text-justify}

That is an operational definition, not a claim that families choose only within their commune. We must also distinguish establishments, enrolment, and capacity: a school with students does not necessarily have vacancies. Assessing coverage requires knowing which levels it serves, how many places it can offer, and whether it is accessible to those who need it.

<span id="claim-demography"></span>According to the [INE projection based on the 2024 Census](https://www.ine.gob.cl/estadisticas-por-tema/demografia-y-poblacion/estimaciones-y-proyecciones-de-poblacion), the population aged 6–17 falls from **3,081,791 in 2025** to **1,366,155 in 2050**, a `55.7%` decline. The figure excludes early childhood education and describes population, not enrolment or closures; it does require territorial planning of capacity, transport, and continuity.
{: .text-justify}

### Where SLEPs and de-municipalisation fit

SLEPs are public providers of establishments transferred to them; they do not govern every school in a commune. [Law 21,040](https://www.bcn.cl/leychile/navegar?idNorma=1111237) regulates the transfer, and the Directorate of Public Education publishes its [territorial schedule](https://dep.gob.cl/calendario-de-traspaso/). A transfer is not the disappearance of a school when the same community remains served, nor can an earlier event be attributed to today's SLEP. Comparing administrations requires equivalent exposed populations and periods: this panel describes events; it does not identify the effect of a management model.

## Spoonful 2: do the lower-performing schools leave and better alternatives arrive?

### Enrolment reveals a trajectory, not its cause

The comparison asks whether closing schools had been performing worse than similar alternatives. Each closure is compared with institutions in the same year, commune, education segment, sector, rurality, and size band. SIMCE is standardised by year, grade, and subject; PSU, PDT, and PAES within their own process.

<span id="claim-enrolment-path"></span>Enrolment provides the clearest signal: of the 684 closures that followed activity, 665 have three complete years. **The medians for those three years fall `28 → 23 → 1` student.**

The sequence describes three snapshots of the group, not every school's trajectory. Nor does it show whether families left because of education difficulties, a closure announcement, residential movement, or fewer children in the territory. These are rival explanations to test, not causes identified by the medians.

Achievement has much thinner coverage:

| Trajectory | Closures with three years | Coverage of 684 | Medians `t−3 → t−2 → t−1` |
|---|---:|---:|---|
| SIMCE | 76 | 11.1% | `−0.232 → −0.235 → −0.083` |
| IVE-SINAE | 188 | 27.5% | `0.882 → 0.910 → 0.946` |
{: .table--compact .table--numeric .table--scroll}

IVE-SINAE is an aggregate school-vulnerability index, not individual poverty.
{: .small}

### What scores do—and do not—tell us

<span id="claim-outcomes"></span>The table above describes the broad historical universe. The strict test filters out annexes, administrative changes, and different segments again. Of 330 eligible closures, only 97 have SIMCE and 46 have admissions data; exact matching leaves **21 and 8**, respectively:

| Outcome | Primary estimate | 95% CI | Support |
|---|---:|---:|---:|
| Relative SIMCE | `+0.029` SD | `[−0.095, +0.158]` | 21 closures |
| Admissions score (core), among test takers | `−0.001` SD | Not estimable | 8 closures |
{: .table--compact .table--scroll}

Among comparable schools, SIMCE shows no precise difference, and admissions does not meet the minimum of ten closures. This does not mean that closing schools are above the national average: in the broad historical universe, the SIMCE median starts at `−0.232` SD. In technical artefacts, `NOT_ESTIMABLE` does not mean zero, a tie, or equality; it means that publishing a defensible interval would require pretending the data contain more information than they do.
{: .text-justify}

The `−4.3%` in part I and the `+0.029` in this instalment are not the same contrast. The first is a percentage gap relative to the commune mean in grade 4 mathematics for closing subsidised private schools across nine years from 1999 to 2011. The second uses annual standard deviations, recent strict closures, the mean from `t−3` to `t−1`, and exact controls. Period, unit, universe, and estimand all change; the signs are not directly comparable.
{: .small}

The minimum of ten is a retrospective rule to prevent adapting the threshold to the observed signs; it is not a universal statistical law.

Sensitivity does not change the conclusion: weighted SIMCE is `+0.034` SD `[−0.225, +0.289]`, and admissions remains below the minimum. The preliminary signal disappears after separating annexes and markets; it does not prove equality, but dependence on a loose definition.
{: .text-justify}

### An average can change without telling us how much students learned

The accounting separates continuation, reallocation, and entry or exit. An average can rise after excluding a low-scoring group without that group improving, or remain stable while access and journeys change.

## Spoonful 3: from the average to each territory's education network

### What providers can do with this evidence

The immediate use is not a ranking of schools that should close. It is to organise information before deciding whether to support an establishment, expand its provision, reorganise a network, or assess a merger. These questions lead to maps—not because a map answers them on its own, but because it reveals where an aggregate comparison is insufficient.

### How to read the maps without turning proximity into replacement

The territorial comparison asks whether another school serving the same segment appears nearby after a strict closure. I search within 10 km and from `t` to `t+2`. Closure location is measured at `t−1`; entry location uses the **first valid official coordinate between the entry year and 2025**. This criterion recovers late records without pretending that the school was physically there from its first year.

Here “entry” is operational: activity with positive enrolment after at least two clear years in the 2013–2025 panel, with no prior active episode in that window and no registered succession. It does not prove that the school is historically new; earlier history may lie outside the panel. For recent events, the later observation window may also remain incomplete.

To show variety without choosing the most striking result, I take **one case from each education family defined in advance**, ordered by commune, distance, year, and RBD. **Neither outcome values nor outcome availability enter the selection.** Nine unstable trajectories are excluded before matching, and 259 entries use a coordinate reported with a lag.

<span id="claim-territorial"></span>Of 330 strict closures, 320 have valid coordinates. Among 414 openings, 389 have an eligible coordinate under the temporal criterion. Six candidate pairs, corresponding to four closures, are excluded in the same year and no more than 100 metres away because they may be administrative replacements; requiring the same segment excludes another 420 combinations. This leaves **38 matched closures and 29 unique openings**. No eligible secondary-education pair remained. The two systematic cases are descriptive:

| Case | Segment | Closure → opening | Distance | What it reveals |
|---|---|---|---:|---|
| Lo Barnechea | Early transition | 2016 → 2016 | 1.046 km | The entrant's first valid coordinate is from 2019; proximity is observed, not destination. |
| Lo Prado | Primary | 2016 → 2016 | 7.860 km | The entrant is also located with a 2019 coordinate and is outside the closure's commune. |
{: .table--compact .table--scroll}

The selection does not claim that these examples represent the country. It does something more modest: it shows how the questions change when segment, coordinate year, and identity rules are preserved. A spatial link is a proximity hypothesis, not a student trajectory or evidence of substitution.
{: .text-justify}

{% include thesis-extension-stylized-evidence.html %}

<span id="claim-el-salvador"></span>I included the third case because I grew up in El Salvador; that familiarity guides questions, not explanations. School No. 14 (RBD 391) closed at the end of 2013 and merged with School No. 1 (RBD 390). The 2008–2011 directories place the former at **500 Diego Portales**; [institutional regulations](https://fees.cl/wp-content/uploads/2019/12/Reglamento-de-convivencia-2019-2020.pdf) place the latter at **1510 Diego Portales**. The [BCN](https://www.bcn.cl/laborparlamentaria/documento?id=636175) documents the transfer of grades one through six.
{: .text-justify}

School No. 14's 2015 MINEDUC point differs by 826 m from the homonymous OSM feature. The viewer uses the latter as a **historical candidate**, not a correction: it was created in 2022, states no RBD, and the [contrast GeoJSON](/assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.geojson) retains both. This places School No. 1 **about 1.3 km** away; the official points yielded 0.45 km.
{: .text-justify}

Combined enrolment fell from **1,399 in 2004 to 977 in 2013** (`−30.2%`). In 2014 School No. 1 rose from 432 to 738 students, a jump consistent with the documented merger. The preceding decline makes demographic contraction plausible, but **does not prove it was the administrative motive for closure**; the contemporary parliamentary intervention also discussed overcrowding and subsequent adaptations.
{: .text-justify}

Were there fewer children, did mining-linked households move, or did other provision grow? The series raises these questions; familiarity cannot answer them.

The viewer uses an OSM street map, MINEDUC coordinates and, for School No. 14, an adjudicated historical candidate that retains the official point for comparison. In the systematic cases, the line represents proximity, not destination; in El Salvador it represents the documented merger, not individual student trajectories. These are stylised facts for asking questions, not experiments. The exit and entry panels are separate samples.
{: .small}

<span id="claim-new-schools"></span>For new schools there is no conclusive answer either. Comparable cases by cohort number `4/6/8` in SIMCE and `1/1/2` in admissions. No cohort reaches ten cases. The result is therefore **not estimable under the adopted criterion**: this dataset cannot determine whether entrants perform better or worse.
{: .text-justify}

<span id="claim-decomposition"></span>Market accounting separates change within continuing schools, enrolment reallocation, and official entry or exit. Turnover contributes `−0.000105` SD in SIMCE, with a 95% CI of `[−0.000346, +0.000103]`, and `+0.000113` in admissions, with a 95% CI of `[+0.000027, +0.000213]`. The admissions interval is above zero among test takers; the SIMCE interval crosses zero. These are accounting identities, not causes, and they **do not provide causal support for the creative-destruction hypothesis**.
{: .text-justify}

### How this result relates to earlier studies

[Iocco (2024)](https://doi.org/10.2139/ssrn.4808834) follows displaced students in Chile: it reports average effects near zero and better outcomes when the receiving school performs better. It is a preprint; prolonged RBD disappearance may mix closures, mergers, or identifier changes. [Grau, Hojman, and Mizala (2018)](https://doi.org/10.1016/j.econedurev.2018.05.003), by contrast, estimate increases of `1.8–2.5` percentage points in high-school dropout and `3.9–4.4` points in fifth-grade retention among affected students. [Elacqua and colleagues](https://doi.org/10.4067/S0718-52862012000200005) examine the alternatives available to pupils affected by a closure. Their units, periods, and designs differ from this school-level descriptive analysis, so the estimates are neither averaged nor presented as an automatic contradiction.
{: .text-justify}

Here I distinguish event, entity, annex, and segment; observe spatial renewal; and extend through 2025. Without individual trajectories I do not identify destination, accessibility, or welfare.
{: .text-justify}

### What we know about SAE and SLEPs

<span id="claim-slep-sae"></span>The staggered schedules of Local Public Education Services (SLEPs) and the School Admission System (SAE) appear to offer causal comparisons. In these data, however, neither meets sufficient conditions for attributing an effect.
{: .text-justify}

| Analysis | Hypothesis tested | Observed result | What blocks a causal reading |
|---|---|---|---|
| Synthetic SLEP design | Transfer changes enrolment or provision relative to territories with comparable pre-transfer trajectories. | **None of the 25** territory-horizon combinations met the comparability criterion fixed in the analysis specification. | No admissible synthetic comparison existed. For later schedule changes, the Evaluation Council's [*2025 Annual Report*, pp. 35–36](https://educacionpublica.gob.cl/wp-content/uploads/2026/03/Informe-Anual-2025-Consejo-Evaluador-del-Sistema-de-Educacion-Publica.pdf#page=35), documents case-by-case adjustments based on installation progress, sustainability, and complexity; it does not identify the schedule for the cohorts analysed here. |
| Exploratory SLEP analysis | Baseline conditions predict earlier transfer, and proximity across networks may contaminate comparisons. | Three baseline conditions showed no predictive ability distinguishable from chance: cross-validated AUC `0.53`, permutation `p=0.22`. In 53 of 70 territories there is at least one other SLEP relative to which 20% or more of its schools are within 20 km, as-the-crow-flies, of a school in that SLEP. | Failing to detect observed selection does not show that the schedule was random; the geometry shows potential interference rather than an observed spillover. |
| SAE triple difference | In 2018, concentration changes in two of the entry grades—grades 1 and 7—relative to deferred grades, differently in four regions entering that year and ten control regions. | HHI `+0.0035` `[−0.0104, +0.0174]`; log effective number of schools `−0.0042` `[−0.0265, +0.0181]`. | With the primary equal commune-grade weighting, 4 of 4 pre-period equivalence checks pass; with equal historical-region weights, both outcomes fail in 2016–2017, the immediately preceding period. There are only four treated regions, and cross-grade effects are not ruled out. |
{: .table--compact .table--scroll}

These results do not allow me to conclude that SLEPs and SAE had no effects. For SLEPs, no comparison met the conditions required to estimate one. For SAE, both 95% intervals—delete-one-region jackknife over 14 historical regions—include zero and values of both signs. With only four treated regions, nominal 95% coverage is approximate, and without identification the intervals do not bound the policy effect. The data let me diagnose the design's limits; they do not let me evaluate either policy.
{: .text-justify}

For SLEPs, a future evaluation would be more causally informative if the criteria setting the order of entry were documented before transfer, more treated territories accumulated, and interference, student destinations, accessibility, and outcomes were measured. For SAE, whose rollout is complete, extending the window requires pooling later cohorts with fewer not-yet-treated regions or constructing a different contrast, for example from a defensible assignment rule. These conditions would strengthen, not guarantee, a causal reading of **these designs**; until they are met, their results are exploratory signals, not impacts.
{: .text-justify}

## What public policy can use

<span id="claim-policy-use"></span>This analysis provides **decision support**, not a rule for closing, merging, opening, or ranking schools. The prudent sequence is **observation → diagnosis → decision**. Falling enrolment or a nearby school justify diagnosis; they are not enough to decide on closure.
{: .text-justify}

| Decision stage | Signal supplied by this analysis | Indispensable additional evidence | Prudent use |
|---|---|---|---|
| Validate the event | Distinguishes closure, annex, merger, RBD change, and education segment. | Resolutions, continuity of the parent school, and provision by level. | Ask the register's custodian to correct it; do not automatically count a disappearance. |
| Diagnose falling enrolment | Shows trajectories, operating status, and territorial differences. | Population by age, residential mobility, transfers, competition, capacity, and prior announcements. | Trigger diagnosis and support; do not use an enrolment threshold as a closure rule. |
| Plan a transition or network | Separates levels and warns that proximity is not substitution. | Actual vacancies, accessibility and travel time, destinations, support, participation, and pedagogical continuity. | Prepare scenarios and a transition plan; do not presume that a directory alternative is usable. |
| Evaluate results | Defines denominators, samples, and comparison limits. | Student follow-up and a credible counterfactual. | Measure outputs, outcomes, and impact separately; do not attribute learning, equity, or welfare to closure without causal identification. |
{: .table--compact .table--scroll}

Institutional scope matters too. A SLEP plans and manages **its own network**, not establishments run by other providers. [Law 21,040, Article 18(c) and (t)](https://www.bcn.cl/leychile/navegar?idNorma=1111237) requires each SLEP to develop public provision, safeguard coverage—including areas of population growth or insufficient coverage—and ensure continuity of educational pathways. Paragraph (t) adds monitoring and support for retention and re-engagement. MINEDUC is the governing authority for the education system; the Directorate of Public Education coordinates and strategically steers the Public Education System. The [2026 Annual Local Plan](https://dep.gob.cl/pal-2026/) plans technical support, infrastructure, and staffing on the basis of course numbers and enrolment. None of these functions grants authority over other providers, turns the study into administrative authorisation, or establishes that one governance model performs better than another.
{: .text-justify}

Two errors matter. A **false positive** would deem unviable a school still needed for access; a **false negative** would miss a risky transition because aggregate enrolment looks stable. IVE-SINAE describes aggregate school composition; it neither identifies individual poverty nor decides where to intervene.
{: .text-justify}

The theory of change links **inputs**—valid events, demographics, capacity, and destinations—to diagnosis and support, transition plans, continuity, attendance, and retention, then learning and equity. It assumes actual vacancies, transfers that preserve access, and community participation. **This post proposes the chain for evaluation; it does not establish that it works.**
{: .text-justify}

## What would need to happen for causal inference

A causal result requires more than adding years. For closures, we need to follow students, know their destinations, and compare their trajectories with a credible group before families anticipate the change. For SLEPs, we need to document why each territory transferred when it did, accumulate more treated units, and measure interference across nearby networks. For SAE, a longer window does not by itself solve the small number of treated clusters or placebos that depend on weighting: a different contrast must rest on a defensible assignment rule.

Each route can fail. Incompatible pre-trends invalidate an event study; a discontinuity requires a rule that cannot be manipulated; an instrumental variable needs a clear first stage and credible exclusion; and individual follow-up can be biased when links fail selectively. Stating these conditions before estimation is part of the result, not a formality.

Demographic change makes territorial scenarios for support, expansion, reorganisation, and protection of capacity more urgent. It does not provide a closure calendar: national decline can coexist with neighbourhoods that need new schools. A future article should combine local demography, provision by level, vacancies, travel times, and student trajectories. Its useful product would not be a list of establishments destined to close.

<details class="technical-disclosure" markdown="1">
<summary>Technical note and robustness checks</summary>

This section preserves the figures needed to audit the exercise without turning the main story into an execution log.

**Coverage.** The identity registry assembled 14 official aliases and two candidate temporal successions; it does not establish that every possible recoding has been detected. The sample varies across provider type, rurality, and region, so the results describe observed cases rather than a national population effect.

**SLEPs.** None of the 25 territory-horizon combinations met the defined minimum of ten eligible donors, three effective donors, and the pre-treatment fit checks. The exploratory diagnostic distinguishes 26 territories transferred by 31 December 2025 from 44 not yet transferred. Using three baseline conditions, AUC was `0.5341` and permutation `p=0.2195` over 1,999 draws: prediction was not distinguishable from chance, but this does not establish random assignment. In 53 of 70 territories, at least 20% of schools lie within 20 km of a school in another SLEP; that geometry is compatible with interference, not evidence of a spillover effect.

**SAE.** The 2017–2018 triple difference compares grades 1 and 7 with deferred grades, across four regions entering in 2018 and ten not yet treated. The [MINEDUC guide](https://www.mineduc.cl/wp-content/uploads/sites/19/2018/01/guia-informativa.pdf) confirms that sequence. Inference uses a delete-one-region jackknife over 14 historical regions. HHI is `+0.003513` `[−0.010368, +0.017395]`; the log effective number is `−0.004192` `[−0.026491, +0.018106]`. All four primary placebos meet the defined margin, but historical-region weighting passes only two of four. With four treated regions, sensitive checks, and possible cross-grade effects, the comparison remains exploratory.

**Results and sensitivity (MR1 and MR2).** SIMCE is `+0.029` SD `[−0.095, +0.158]` with 21 closures; the weighted variant is `+0.034` `[−0.225, +0.289]`. Admissions is `NOT_ESTIMABLE` with eight closures. Entrants are also `NOT_ESTIMABLE`: comparable cases by cohort are 4/6/8 in SIMCE and 1/1/2 in admissions. The minimum of ten was set in a retrospective protocol; it is reported as a limitation, not a universal law.

**Decomposition and markets.** Official turnover contributes `−0.000105` `[−0.000346, +0.000103]` in SIMCE and `+0.000113` `[+0.000027, +0.000213]` in admissions. The accounting residual is below `1e−10`; arithmetic closure does not turn the components into causes. The H1 spatial sensitivity compares relative concentration positions under six neighbourhood definitions with the commune definition: no band excludes zero, and its thresholds are not policy rules.

**Territory and reproducibility.** The spatial exercise retains 38 closures and 29 unique openings; it excludes nine unstable trajectories and records 259 entries with delayed coordinates. The national audit distinguishes 12,038 operating establishments from 78 authorised without enrolment. OSM is a secondary source, and the public product retains aggregates only. R produced the aggregates and 999 bootstrap replications; Python reconciled 112 public cells within `1e−10`. Agreement across implementations reduces calculation error; it does not solve causal identification.

</details>

## Closing: evaluate the transition, do not celebrate movement

Extending the thesis revealed that “closure” concealed stocks, events, empty schools, annexes, and RBD replacements; “market” mixed nurseries, primary schools, and secondary schools; “renewal” confused proximity with destination.
{: .text-justify}

The creative-destruction hypothesis is attractive; that is why it requires a strict test. There are signals, gaps, and demographic pressure, but **this analysis provides no evidence for celebrating turnover**.
{: .text-justify}

<span id="claim-open-question"></span>The observed administrative turnover exists. What remains unknown is who retains continuity and who ultimately pays for the transition.
{: .text-justify}

### Transparency and scope of the sources

The thesis and its extension are my own work; they are not an independent replication. I was also a co-author of [*Destructive Creation* (Working Paper 396, 2014)]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}), a predecessor to the Grau, Hojman, and Mizala (2018) article cited here. El Salvador was selected because of my biographical connection to the town. Making these relationships explicit helps recognise possible confirmation and selection bias.

I received no funding for this work and declare no conflicts of interest. My sole institutional affiliation is Chile's Ministry of Social Development and Family, which did not fund, commission, supervise, or review this work; its positions are not represented by these conclusions. I used artificial-intelligence assistants to support programming, quality control, prose review, and adversarial review. The methodological and editorial decisions, source verification, and responsibility for every claim and result are mine.
{: .text-justify}

---

## References

<div class="post-references" markdown="1">

Chay, K. Y., McEwan, P. J., & Urquiola, M. (2005). [The central role of noise in evaluating interventions that use test scores to rank schools](https://doi.org/10.1257/0002828054825529). *American Economic Review, 95*(4), 1237–1258.

Elacqua, G., Martínez, M., Santos, H., & Urbina, D. R. (2012). [School closures in Chile: Access to quality alternatives in a school choice system](https://doi.org/10.4067/S0718-52862012000200005). *Estudios de Economía, 39*(2), 179–202.

Grau, N., Hojman, D., & Mizala, A. (2018). [School closure and educational attainment: Evidence from a market-based system](https://doi.org/10.1016/j.econedurev.2018.05.003). *Economics of Education Review, 65*, 1–17.

Hsieh, C.-T., & Urquiola, M. (2006). [The effects of generalized school choice on achievement and stratification](https://doi.org/10.1016/j.jpubeco.2005.11.002). *Journal of Public Economics, 90*(8–9), 1477–1503.

Iocco, M. P. (2024). [Impact of planned school closures on academic performance: Evidence from Chile](https://doi.org/10.2139/ssrn.4808834). *SSRN preprint*.

Paredes, R. D., & Fresard, M. (2018). [Voucher y cierre de escuelas en Chile](https://doi.org/10.38178/cep.vi151.62). *Estudios Públicos*, (151).

Quintero-Fragozo, C., Cortés, Y., & Sarrias, M. (2023). [Effects of spatial competition on public educational efficiency](https://doi.org/10.1080/02680939.2021.1966102). *Journal of Education Policy, 38*(1), 115–140.

Taghizadeh, J. L. (2020). [Effects of school closures on displaced students and future cohorts](https://doi.org/10.1016/j.labeco.2020.101910). *Labour Economics, 67*, 101910.

</div>
