---
layout: single
classes: [thesis-extension-post]
title: "Extending my thesis in three spoonfuls (part II): what school turnover still cannot tell us"
subtitle: "What the records show about school turnover, what they cannot establish, and what continuity planning requires."
date: 2026-10-11 10:00:00 -0300
last_modified_at: 2026-10-17 17:15:00 -0300
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
  social: true
  republish: []
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
---

In [part I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) I left one question open: when one school leaves and another enters, do opportunities to learn improve, or does only the register change?
{: .text-justify}

<span id="claim-causal-boundary"></span>**This analysis does not identify whether turnover improves or worsens educational outcomes.** That is not an elegant way of saying that the effect is zero. Some comparisons are imprecise; others lack enough comparable cases; and the records neither follow each student nor reconstruct what would have happened without the closure or opening.
{: .text-justify}

Part I audited 1992–2012. Here I use directories from 2015 to 2025 to observe transitions from 2016 to 2025, and a 2013–2025 panel to detect entries. The period and questions differ; I do not re-estimate Part I's results.
{: .text-justify}

Three results organise the account. First, the register contains **900 official closures**, but the stricter definition leaves **330 closures with enrolment** for comparison. Second, median enrolment falls sharply before closure, although that path does not reveal its cause. Third, only **38 closures** have a nearby opening in the same segment under the territorial criterion; proximity does not establish available places, accessibility, or student destination.
{: .text-justify}

The contribution is a public question: **what continuity did the community receive, and who bore its costs?**
{: .text-justify}

## Spoonful 1: before evaluating turnover, establish what actually changed

### Leaving the register does not always mean a school disappeared

In the first instalment, “entry” and “exit” described appearances and disappearances in the files. To study the recent period, I need to separate those from administrative changes and an actual interruption in education provision.
{: .text-justify}

An establishment may close, enter recess, merge with another, change identifier, lose a site, or stop serving a level. It may also change provider—the entity responsible for managing it—without ceasing to operate. None of those situations should automatically become the same kind of closure.
{: .text-justify}

The **RBD**, MINEDUC's identifier for each establishment, helps track its history but does not resolve it on its own. A code that disappears requires checking what happened to the school, its site, and its provision.
{: .text-justify}

The panel follows establishments over the recent period. The directories begin in 2015, so the first observable transition is in 2016. The El Salvador case dates from 2013 and appears later as a separate historical case. The unit depends on the question: the inventory counts RBD events, identity work reconstructs establishments and sites, and comparisons use establishments within an education segment.
{: .text-justify}

**Exercise.** I separate an actual closure from an administrative change. I define an official closure only as a transition from a non-closed status into code `3`. Recess is not closure; disappearance from the file remains an exit of unknown cause.
{: .text-justify}

<span id="claim-event-count"></span>**Result.** There are **900 official closures**: 684 after activity, 215 after recess, and one after authorisation without enrolment. Of the 684 previously active schools, 346 had students and 338 already recorded zero enrolment. Closing an empty school is not the same as displacing a school community.
{: .text-justify}

Yet those 346 cases are not automatically 346 schools that disappeared. After reconstructing identity and provision, **330 strict closures of a school in the level it served** remain. The other 16 are site or annex closures, administrative consolidations, RBD replacements, or unresolved cases. Those links are inferred from official directories and excluded from the primary comparison; four further same-site replacement candidates are removed only from the spatial exercise.
{: .text-justify}

### Nearby provision does not necessarily serve the same need

Provision matters too. A nursery does not compete for the same population as a primary school or a secondary school. Official codes let us separate early childhood education into nursery, middle, transition, and mixed levels; I then distinguish primary and secondary education. From here on, a “market” means **commune and exact education segment**, not every institution in the same territory.
{: .text-justify}

That is an operational definition, not a claim that families choose only within their commune. We must also distinguish establishments, enrolment, and capacity: a school with students does not necessarily have vacancies. Assessing coverage requires knowing which levels it serves, how many places it can offer, and whether it is accessible to those who need it.
{: .text-justify}

<span id="claim-demography"></span>According to the [INE projection based on the 2024 Census](https://www.ine.gob.cl/estadisticas-por-tema/demografia-y-poblacion/estimaciones-y-proyecciones-de-poblacion), the population aged 6–17 falls from **3,081,791 in 2025** to **1,366,155 in 2050**, a `55.7%` decline. The figure excludes early childhood education and describes population, not enrolment or closures; it does require territorial planning of capacity, transport, and continuity.
{: .text-justify}

### Where SLEPs and de-municipalisation fit

SLEPs are public providers of establishments transferred to them; they do not govern every school in a commune. [Law 21,040](https://www.bcn.cl/leychile/navegar?idNorma=1111237) regulates the transfer, and the Directorate of Public Education publishes its [territorial schedule](https://dep.gob.cl/calendario-de-traspaso/). A transfer is not the disappearance of a school when the same community remains served, nor can an earlier event be attributed to today's SLEP. Comparing administrations requires equivalent exposed populations and periods: this panel describes events; it does not identify the effect of a management model.
{: .text-justify}

## Spoonful 2: do the lower-performing schools leave and better alternatives arrive?

### Enrolment reveals a trajectory, not its cause

The comparison asks whether closing schools had been performing worse than similar alternatives. Each closure is compared with institutions in the same year, commune, education segment, sector, rurality, and size band. SIMCE is standardised by year, grade, and subject; PSU, PDT, and PAES within their own process.
{: .text-justify}

<span id="claim-enrolment-path"></span>Enrolment provides the clearest signal: of the 684 closures that followed activity, 665 have three complete years. **The medians for those three years fall `28 → 23 → 1` student.**
{: .text-justify}

The sequence describes three snapshots of the group, not every school's trajectory. Nor does it show whether families left because of education difficulties, a closure announcement, residential movement, or fewer children in the territory. These are rival explanations to test, not causes identified by the medians. SIMCE has three complete years for 76 closures and moves from `−0.232` to `−0.083` standard deviations; IVE-SINAE covers 188 and rises from `0.882` to `0.946`. The latter is an aggregate school-vulnerability index, not individual poverty.
{: .text-justify}

### What scores do—and do not—tell us

<span id="claim-outcomes"></span>The strict test filters out annexes, administrative changes, and different segments again. Of 330 eligible closures, only 97 have SIMCE and 46 have admissions data; exact matching leaves **21 and 8**, respectively.
{: .text-justify}

{: .table-caption}
**Table 1.** Observed signals and the limit of each comparison

| Signal | Support | Result | Limit |
|---|---:|---:|---|
| Enrolment before closure | 665 closures | Medians `28 → 23 → 1` | Describes prior emptying; does not identify its cause. |
| SIMCE before closure | 76 closures | Medians `−0.232 → −0.235 → −0.083` SD | 11.1% coverage of the 684 closures from active status. |
| IVE-SINAE before closure | 188 closures | Medians `0.882 → 0.910 → 0.946` | Aggregate school composition, not individual vulnerability. |
| SIMCE among comparable schools | 21 closures | `+0.029` SD; 95% CI `[−0.095, +0.158]` | The interval includes differences in either direction. |
| Admissions among test takers | 8 closures | `−0.001` SD; interval not estimable | Below the retrospective minimum of ten closures. |
{: .table--compact .table--scroll}

Among comparable schools, SIMCE shows no precise difference, and admissions does not meet the minimum of ten closures. This does not mean that closing schools are above the national average: in the broad historical universe, the SIMCE median starts at `−0.232` SD. In the technical results, “not estimable” does not mean zero, a tie, or equality; it means that publishing a defensible interval would require pretending the data contain more information than they do.
{: .text-justify}

The `−4.3%` in part I and the `+0.029` in this instalment are not the same contrast. The first is a percentage gap relative to the commune mean in grade 4 mathematics for closing subsidised private schools across nine years from 1999 to 2011. The second uses annual standard deviations, recent strict closures, the mean from `t−3` to `t−1`, and exact controls. Period, unit, universe, and estimand all change; the signs are not directly comparable.
{: .small}

The minimum of ten is a retrospective rule to prevent adapting the threshold to the observed signs; it is not a universal statistical law. Sensitivity does not change the conclusion: weighted SIMCE is `+0.034` SD `[−0.225, +0.289]`, and admissions remains below the minimum. Groups selected for an extreme score also tend to move toward the average at a later measurement; without an appropriate comparison, a before-and-after change can therefore confuse improvement with [regression to the mean](https://doi.org/10.1257/0002828054825529).
{: .text-justify}

### An average can change without telling us how much students learned

The accounting separates continuation, reallocation, and entry or exit. An average can rise after excluding a low-scoring group without that group improving, or remain stable while access and journeys change.
{: .text-justify}

## Spoonful 3: from the average to each territory's education network

### What providers can do with this evidence

The immediate use is not a ranking of schools that should close. It is to organise information before deciding whether to support an establishment, expand its provision, reorganise a network, or assess a merger. These questions lead to maps—not because a map answers them on its own, but because it reveals where an aggregate comparison is insufficient.
{: .text-justify}

### How to read the maps without turning proximity into replacement

The territorial comparison asks whether another school serving the same segment appears nearby after a strict closure. I search within 10 km and from `t` to `t+2`. Closure location is measured at `t−1`; entry location uses the **first valid official coordinate between the entry year and 2025**. This criterion recovers late records without pretending that the school was physically there from its first year.
{: .text-justify}

Here “entry” is operational: activity with positive enrolment after at least two clear years in the 2013–2025 panel, with no prior active episode in that window and no registered succession. It does not prove that the school is historically new; earlier history may lie outside the panel. For recent events, the later observation window may also remain incomplete.
{: .text-justify}

<span id="claim-territorial"></span>Of 330 strict closures, 320 have valid coordinates. Among 414 openings, 389 have an eligible coordinate under the temporal rule. After excluding possible administrative replacements, different segments, and nine unstable trajectories, **38 closures remain linked by proximity to 29 unique openings**. This national result helps size the phenomenon; it does not show that the openings received the displaced students or offered an accessible substitute.
{: .text-justify}

<span id="claim-el-salvador"></span>I use El Salvador as the territorial example because I grew up there. That familiarity guides questions and may introduce selection bias; it neither explains the closure nor makes the case nationally representative. School No. 14 (RBD 391) closed at the end of 2013 and merged with School No. 1 (RBD 390). The 2008–2011 directories place the former at **500 Diego Portales**; [institutional regulations](https://fees.cl/wp-content/uploads/2019/12/Reglamento-de-convivencia-2019-2020.pdf) place the latter at **1510 Diego Portales**. The [BCN](https://www.bcn.cl/laborparlamentaria/documento?id=636175) documents the transfer of grades one through six.
{: .text-justify}

Combined enrolment fell from **1,399 in 2004 to 977 in 2013** (`−30.2%`). In 2014 School No. 1 rose from 432 to 738 students, a jump consistent with the documented merger. The preceding decline makes demographic contraction plausible, but **does not prove it was the administrative motive for closure**; the contemporary parliamentary intervention also discussed overcrowding and subsequent adaptations.
{: .text-justify}

{% include thesis-extension-stylized-evidence.html %}

The map contrasts the official MINEDUC coordinate with an OpenStreetMap historical candidate for School No. 14; it does not replace one source with the other. The line represents the documented merger between establishments, not each student's route. Were there fewer children, did mining-linked households move, or did other provision grow? The series raises those questions; familiarity cannot answer them. The [coordinate audit]({{ '/datos/educacion/auditoria-coordenadas-rbd/' | relative_url }}) preserves the GeoJSON and manifest for the contrast.
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

{: .table-caption}
**Table 2.** SLEP and SAE designs: hypothesis, result, and failed test

| Analysis | Hypothesis tested | Observed result | Failed test |
|---|---|---|---|
| SLEP | Transfer changes enrolment or provision relative to territories with comparable pre-transfer trajectories. | None of the 25 territory-horizon combinations had an admissible synthetic comparison. The baseline diagnostic showed no predictive ability distinguishable from chance: cross-validated AUC `0.5341`, permutation `p=0.2195`. | Comparable support is absent; failure to detect observed selection does not make the schedule random, and proximity across networks permits interference. |
| SAE | Entry in 2018 changes concentration in grades 1 and 7 relative to deferred grades, differently in four treated and ten control regions. | HHI `+0.0035` `[−0.0104, +0.0174]`; log effective number `−0.0042` `[−0.0265, +0.0181]`. | Only four regions are treated, and the immediately preceding placebos fail under the alternative historical-region weighting. |
{: .table--compact .table--scroll}

These results do not allow me to conclude that SLEPs and SAE had no effects. For SLEPs, the Evaluation Council's [*2025 Annual Report*, pp. 35–36](https://educacionpublica.gob.cl/wp-content/uploads/2026/03/Informe-Anual-2025-Consejo-Evaluador-del-Sistema-de-Educacion-Publica.pdf#page=35) documents later case-by-case schedule adjustments, but it does not identify how the order of the cohorts analysed here was set. For SAE, both intervals—delete-one-region jackknife over 14 historical regions—include zero and values of either sign. With only four treated regions, nominal 95% coverage is approximate, and without identification those intervals do not bound the policy effect. The data show why these designs do not sustain a causal reading; they do not evaluate either policy's impact.
{: .text-justify}

A future SLEP evaluation would need to document entry criteria before transfer, accumulate more treated territories, and measure interference, destinations, accessibility, and outcomes. For SAE, adding years does not by itself repair the small number of treated clusters: a different contrast grounded in a defensible assignment rule is needed. Until those conditions are met, these findings diagnose the designs; they are not impacts.
{: .text-justify}

## What public policy can use

<span id="claim-policy-use"></span>This analysis provides **decision support**, not a rule for closing, merging, opening, or ranking schools. The prudent sequence is **observation → diagnosis → decision**. Falling enrolment or a nearby school justify diagnosis; they are not enough to decide on closure.
{: .text-justify}

The event must first be validated: closure, annex, merger, RBD change, and loss of a level are not interchangeable. Diagnosis then needs demography, residential mobility, capacity, transfers, and prior announcements. If the network is reorganised, the plan must verify actual vacancies, travel times, accessibility, support, and pedagogical continuity. Only then does evaluation with student follow-up and a credible counterfactual become meaningful.
{: .text-justify}

A SLEP plans and manages **its own network**, not establishments run by other providers. [Law 21,040, Article 18(c) and (t)](https://www.bcn.cl/leychile/navegar?idNorma=1111237) requires it to develop public provision, safeguard coverage and continuity, and support retention and re-engagement. MINEDUC is the governing authority; the Directorate of Public Education provides strategic direction for the system. The [2026 Annual Local Plan](https://dep.gob.cl/pal-2026/) organises support, infrastructure, and staffing according to course numbers and enrolment. None of this grants authority over other providers or establishes that one governance model performs better than another.
{: .text-justify}

[Law 20,529, Articles 10 and 12](https://www.bcn.cl/leychile/navegar?idNorma=1028635&idParte=9173209) assigns the Education Quality Agency the tasks of evaluating and guiding the system and states that performance evaluation should strengthen institutional capacity, guide improvement plans, and promote continuous improvement. [Article 31 of the same law](https://www.bcn.cl/leychile/navegar?idNorma=1028635) provides for loss of official recognition after four years in the Insufficient Performance category. This analysis did not verify that pathway's full operational status, chronology, or applicable certificates, and it attributes none of the observed closures to it. A descriptive signal in this post may trigger diagnosis and support; on its own it neither establishes that procedure nor constitutes a closure order.
{: .text-justify}

Two errors matter. A **false positive** would deem unviable a school still needed for access; a **false negative** would miss a risky transition because aggregate enrolment looks stable. IVE-SINAE describes aggregate school composition; it neither identifies individual poverty nor decides where to intervene.
{: .text-justify}

The theory of change links **inputs**—valid events, demographics, capacity, and destinations—to diagnosis and support, transition plans, continuity, attendance, and retention, then learning and equity. It assumes actual vacancies, transfers that preserve access, and community participation. **This post proposes the chain for evaluation; it does not establish that it works.**
{: .text-justify}

Teaching capacity belongs in that chain. Lower enrolment may create opportunities to reorganise classes and reinforce support, but it also creates frictions: hard-to-replace specialisms, commuting time, the loss of established teams, and labour tensions. Counting places without checking staffing, continuity of pedagogical relationships, and working conditions can shift the cost of reorganisation onto students and workers.
{: .text-justify}

## What would need to happen for causal inference

A causal result requires more than adding years. For closures, we need to follow students, know their destinations, and compare their trajectories with a credible group before families anticipate the change. For SLEPs, we need to document why each territory transferred when it did, accumulate more treated units, and measure interference across nearby networks. For SAE, a longer window does not by itself solve the small number of treated clusters or placebos that depend on weighting: a different contrast must rest on a defensible assignment rule.
{: .text-justify}

Each route can fail. Incompatible pre-trends invalidate an event study; a discontinuity requires a rule that cannot be manipulated; an instrumental variable needs a clear first stage and credible exclusion; and individual follow-up can be biased when links fail selectively. Stating these conditions before estimation is part of the result, not a formality.
{: .text-justify}

Demographic change makes territorial scenarios for support, expansion, reorganisation, and protection of capacity more urgent. It does not provide a closure calendar: national decline can coexist with neighbourhoods that need new schools. A future article should combine local demography, provision by level, vacancies, travel times, and student trajectories. Its useful product would not be a list of establishments destined to close.
{: .text-justify}

### Scope and reproducibility

Coverage changes with the question: 665 closures have complete enrolment trajectories, 76 have SIMCE, 188 have IVE-SINAE, and only 21 remain in the strict SIMCE comparison. Admissions describes students who reached the end of secondary education and sat an admissions test, not all pupils. Each result must be read with its own denominator; these are not one national cohort.
{: .text-justify}

Independent routes produced the principal aggregates and agreed within the specified precision. That agreement reduces calculation risk, but it does not establish the historical session, compensate for missing data, or create causal identification. Public artefacts preserve figures, sources, rules, and limits; restricted data remain outside the repository.
{: .text-justify}

## Closing: evaluate the transition, do not celebrate movement

Extending the thesis revealed that “closure” concealed stocks, events, empty schools, annexes, and RBD replacements; “market” mixed nurseries, primary schools, and secondary schools; “renewal” confused proximity with destination.
{: .text-justify}

The creative-destruction hypothesis is attractive; that is why it requires a strict test. There are signals, gaps, and demographic pressure, but **this analysis provides no evidence for celebrating turnover**.
{: .text-justify}

<span id="claim-open-question"></span>The observed administrative turnover exists. What remains unknown is who retains continuity and who ultimately pays for the transition.
{: .text-justify}

### Transparency and scope of the sources

The thesis and its extension are my own work; they are not an independent replication. I was also a co-author of [*Destructive Creation* (Working Paper 396, 2014)]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}), a predecessor to the Grau, Hojman, and Mizala (2018) article cited here. El Salvador was selected because of my biographical connection to the town. Making these relationships explicit helps recognise possible confirmation and selection bias.
{: .text-justify}

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
