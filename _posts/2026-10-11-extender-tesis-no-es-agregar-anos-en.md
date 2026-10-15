---
layout: single
classes: [thesis-extension-post]
title: "Extending my thesis in three spoonfuls (part II): does education improve when schools open and close?"
subtitle: "More evidence on school turnover, its limits, and the questions it leaves for providers and Local Education Services."
date: 2026-10-11 10:00:00 -0300
last_modified_at: 2026-10-14 18:30:00 -0300
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

In [part I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) I returned to my 2014 thesis before extending it. **This analysis does not identify causal effects.** Two important findings survived for 1992–2012: a net reduction in municipal schools and a net expansion of subsidised private schools; and, in the reconstructed Greater Santiago universe, establishments that later disappeared from the records served a more vulnerable enrolment. I also found errors that changed some interpretations. Adding years to the same tables was not enough.

The two instalments do not use a single window or estimate the same quantities. Part I audits 1992–2012. This instalment uses directories from 2015 to 2025 to observe transitions from 2016 to 2025, and a 2013–2025 panel to detect entries. It does not re-estimate the sectoral reallocation, vulnerability gap, or pupil–teacher ratio from part I.

| What I set out to do at the end of part I | What I did here | Status |
|---|---|---|
| Build a predictive warning system | I classified events and described enrolment before closure. | Pending: temporal validation, calibration, and distributional audit. |
| Evaluate SLEP transfers with difference-in-differences or an event study | I tested a synthetic-control design; no comparison passed the support rule. I added an exploratory diagnostic. | Design changed; no causal estimate. |
| Follow individual trajectories | I reviewed the literature and territorial alternatives but did not link students. | Pending. |
| Not proposed in part I: examine SAE | I added an exploratory triple difference. | New analysis; it does not identify the policy effect. |

This second instalment returns to an open question: **what does it mean for one school to leave the system and another to enter?** For people working in education, what matters is whether that movement expands opportunities to learn, reorganises provision that no longer fits the territory, or interrupts a trajectory that needed support rather than a transfer.

The intuition that lower-performing schools leave and better alternatives arrive deserves examination. But it must not become the answer before looking at the data. With the available analysis, **I could not establish whether the observed turnover systematically improves or worsens educational outcomes**. This does not prove that its effects are zero: some comparisons are imprecise, others lack enough information, and above all we do not follow students or construct the counterfactual—what would have happened without the closure or opening.

Within that limit, the data do let us clarify events, inspect their trajectories, and end in the territory: where an opening, merger, or closure stops being a row and changes a community's alternatives.

## Six answers before methods

| Question | Result | What we can say |
|---|---|---|
| How many closures occurred? | **900 official transitions** from 2016 to 2025, using 2015 as the baseline; 330 are strict closures with enrolment for this exercise. | `37,818` is the cumulative count of closed establishments repeated over years, not 37,818 closures. |
| Do the lowest-performing schools close? | Among 21 of 330 strict closures, SIMCE is `+0.029` SD, 95% CI `[−0.095, +0.158]`; admissions has only 8 cases. | The contrast does not describe all closures: 97 had SIMCE and only 21 exact support. In the broad historical universe, the median starts at `−0.232` SD. |
| Are new schools better? | **Not estimable under the adopted rule (minimum 10 cases).** | Initial cohorts do not have enough cases; this does not mean a zero effect, a tie, or equality. |
| Did turnover improve the average? | SIMCE `−0.000105` SD; admissions `+0.000113` SD. | The signs disagree and these are accounting contributions, not causal effects. |
| What is the role of providers and SLEPs? | They manage networks and transitions under different rules. | The panel describes events; it does not identify the effect of a management model. |
| Is there a territorial alternative? | The spatial rule finds 38 closures with a compatible opening. | Proximity does not establish capacity, access, destination, or substitution. |

`SD` means standard deviation (a unit relative to score dispersion). A `95% CI` is the procedure's uncertainty range. “Admissions core” averages language and mathematics among students who took both tests; it does not represent every final-year student.
{: .small}

## Spoonful 1: before evaluating a closure, establish what changed

### Leaving the register does not always mean a school disappeared

In the first instalment, “entry” and “exit” described appearances and disappearances in the files. To study the recent period, I need to separate those from administrative changes and an actual interruption in education provision.

An establishment may close, enter recess, merge with another, change identifier, lose a site, or stop serving a level. It may also change provider—the entity responsible for managing it—without ceasing to operate. None of those situations should automatically become the same kind of closure.

The **RBD**, MINEDUC's identifier for each establishment, helps track its history but does not resolve it on its own. A code that disappears requires checking what happened to the school, its site, and its provision.

The panel follows establishments over the recent period. The directories begin in 2015, so the first observable transition is in 2016. The El Salvador case dates from 2013 and appears later as a separate historical case. The unit depends on the question: the inventory counts RBD events, identity work reconstructs establishments and sites, and comparisons use establishments within an education segment.

**Exercise.** I separate an actual closure from an administrative change. I define an official closure only as a transition from a non-closed status into code `3`. Recess is not closure; disappearance from the file remains an exit of unknown cause.

**Result.** There are **900 official closures**: 684 after activity, 215 after recess, and one after authorisation without enrolment. Of the 684 previously active schools, 346 had students and 338 already recorded zero enrolment. Closing an empty school is not the same as displacing a school community.
{: .text-justify}

Yet those 346 cases are not automatically 346 schools that disappeared. After reconstructing identity and provision, **330 strict school-segment closures** remain. The other 16 are site or annex closures, administrative consolidations, RBD replacements, or unresolved cases. The London, Saint Gabriel, and El Sembrador annexes, for example, have candidate parent schools that remain active. That link is inferred from official directories, not confirmed legal equivalence, so we catalogue it and exclude it from the primary estimand. Later, the territorial exercise finds four further same-site replacement candidates: they remain among the 330 strict closures and are removed only from the spatial comparison.
{: .text-justify}

### Nearby provision does not necessarily serve the same need

Provision matters too. A nursery does not compete for the same population as a primary school or a secondary school. Official codes let us separate early childhood education into nursery, middle, transition, and mixed levels; I then distinguish primary and secondary education. From here on, a “market” means **commune and exact education segment**, not every institution in the same territory.
{: .text-justify}

That is an operational definition, not a claim that families choose only within their commune. We must also distinguish establishments, enrolment, and capacity: a school with students does not necessarily have vacancies. Assessing coverage requires knowing which levels it serves, how many places it can offer, and whether it is accessible to those who need it.

According to the [INE projection based on the 2024 Census](https://www.ine.gob.cl/estadisticas-por-tema/demografia-y-poblacion/estimaciones-y-proyecciones-de-poblacion), the population aged 6–17 falls from **3,081,791 in 2025** to **1,366,155 in 2050**, a `55.7%` decline. The figure excludes early childhood education and describes population, not enrolment or closures; it does require territorial planning of capacity, transport, and continuity.
{: .text-justify}

### Where SLEPs and de-municipalisation fit

SLEPs add an institutional layer, not an automatic explanation. They are public providers and manage establishments transferred to them; they do not govern every school in a commune. [Law 21,040](https://www.bcn.cl/leychile/navegar?idNorma=1111237) regulates those transfers, and the Directorate of Public Education publishes a [territory-by-territory schedule](https://dep.gob.cl/calendario-de-traspaso/). Those rules do not show that a transition improved learning. Nor can an event before a transfer be attributed retrospectively to the SLEP that now manages the territory.
{: .text-justify}

De-municipalisation raises a different question: **does a network's capacity to sustain and improve provision change when its administration changes?** A transfer should not count as a municipal disappearance and a new school if the same community continues to be served. Comparing providers would require rates over equivalent exposed populations and periods, not raw counts. This panel describes events; it does not identify the effect of a management model.

## Spoonful 2: do the lower-performing schools leave and better alternatives arrive?

### Enrolment reveals a trajectory, not its cause

**Objective.** Test whether closing schools had been performing worse than comparable alternatives. Each closure is compared with institutions in the same year, commune, education segment, sector, rurality, and size band. SIMCE is standardised by year, grade, and subject; PSU, PDT, and PAES within their own process.

**Result.** Enrolment provides the clearest signal: of the 684 closures that followed activity, 665 have three complete years and their median falls from **`28 → 23 → 1`** student.

This is a sign of emptying before the recorded closure. It does not mean every school followed that sequence, nor does it explain whether families left because of education difficulties, a closure announcement, residential movement, or fewer children in the territory. These are rival explanations to test, not causes identified by this trajectory.

Achievement has much thinner coverage:

| Trajectory | Closures with three years | Coverage of 684 | Medians `t−3 → t−2 → t−1` |
|---|---:|---:|---|
| SIMCE | 76 | 11.1% | `−0.232 → −0.235 → −0.083` |
| IVE-SINAE | 188 | 27.5% | `0.882 → 0.910 → 0.946` |

IVE-SINAE is an aggregate school-vulnerability index, not individual poverty.
{: .small}

### What scores do—and do not—tell us

The table above describes the broad historical universe. The strict test filters out annexes, administrative changes, and different segments again. Of 330 eligible closures, only 97 have SIMCE and 46 have admissions data; exact matching leaves **21 and 8**, respectively:

| Outcome | Primary estimate | 95% CI | Support |
|---|---:|---:|---:|
| Relative SIMCE | `+0.029` SD | `[−0.095, +0.158]` | 21 closures |
| Admissions score (core), among test takers | `−0.001` SD | Not estimable | 8 closures |

Among comparable schools, SIMCE shows no precise difference, and admissions does not meet the minimum of ten closures. This does not mean that closing schools are above the national average: in the broad historical universe, the SIMCE median starts at `−0.232` SD. In technical artifacts, `NOT_ESTIMABLE` does not mean zero, a tie, or equality; it means that publishing a defensible interval would require pretending the data contain more information than they do.
{: .text-justify}

The `−4.3%` in part I and the `+0.029` in this instalment are not the same contrast. The first is a percentage gap relative to the commune mean in grade 4 mathematics for closing subsidised private schools across nine years from 1999 to 2011. The second uses annual standard deviations, recent strict closures, the mean from `t−3` to `t−1`, and exact controls. Period, unit, universe, and estimand all change; the signs are not directly comparable.
{: .small}

The minimum of ten is a retrospective operational rule, not a statistical law that makes any study with nine cases invalid and any study with ten valid. Stating the limit prevents changing it after seeing the signs.

The sensitivity checks tell the same story. Weighted SIMCE is `+0.034` SD with a wide interval `[−0.225, +0.289]`; admissions variants remain below the threshold. A preliminary specification produced a negative signal, but it disappears once annexes and different markets are no longer treated as comparable closures. That does not prove equality: it shows that the answer depended on an overly loose definition.
{: .text-justify}

### An average can change without telling us how much students learned

The accounting separates change within continuing schools, enrolment reallocation, and the contribution of entries and exits to an aggregate indicator. An average might rise because it no longer includes a group with low scores, without showing that the group improved. It might also remain almost unchanged while some communities gain access and others face harder journeys.

## Spoonful 3: from the average to each territory's education network

### What providers can do with this evidence

The immediate use is not a ranking of schools that should close. It is to organise information before deciding whether to support an establishment, expand its provision, reorganise a network, or assess a merger. These questions lead to maps—not because a map answers them on its own, but because it reveals where an aggregate comparison is insufficient.

### How to read the maps without turning proximity into replacement

**Objective.** Give the question a territorial form: when a strict closure occurs, does another school serving the same segment appear nearby? I search within 10 km and from `t` to `t+2`. Closure location is measured at `t−1`; entry location uses the **first valid official coordinate between the entry year and 2025**. This rule recovers late records without pretending that the school was physically there from its first year.

Here “entry” is operational: activity with positive enrolment after at least two clear years in the 2013–2025 panel, with no prior active episode in that window and no registered succession. It does not prove that the school is historically new; earlier history may lie outside the panel. For recent events, the later observation window may also remain incomplete.

To show variety without choosing the most striking result, I first take **one case from each preferred education family**; within each family I order by same commune, distance, year, and RBD. **Neither outcome values nor outcome availability enter the selection.** The 9 unstable trajectories are excluded before matching, and 259 entries use a coordinate reported with a lag; both counts remain visible because a late location changes what “nearby” means.

**Result.** Of 330 strict closures, 320 have valid coordinates. Among 414 openings, 389 have an eligible coordinate under the temporal rule. The guard removes six candidate pairs, corresponding to four closures, in the same year and no more than 100 metres away because they may be administrative replacements; requiring the same segment excludes 420 combinations. This leaves **38 matched closures and 29 unique openings**. No eligible secondary-education pair remained. The two systematic cases are descriptive:

| Case | Segment | Closure → opening | Distance | What it reveals |
|---|---|---|---:|---|
| Lo Barnechea | Early transition | 2016 → 2016 | 1.046 km | The entrant's first valid coordinate is from 2019; proximity is observed, not destination. |
| Lo Prado | Primary | 2016 → 2016 | 7.860 km | The entrant is also located with a 2019 coordinate and is outside the closure's commune. |

The selection does not claim that these examples represent the country. It does something more modest: it shows how the questions change when segment, coordinate year, and identity rules are preserved. A spatial link is a proximity hypothesis, not a student trajectory or evidence of substitution.
{: .text-justify}

{% include thesis-post2-coordinate-audit-box.html %}

{% include thesis-extension-stylized-evidence.html %}

The first two buttons belong to the systematic selection. The third is different: I proposed it because I grew up in El Salvador. That familiarity helps frame questions but does not turn my experience into an explanation of the closure. School No. 14 Óscar Yáñez Pastén (RBD 391) closed at the end of 2013 and merged with School No. 1 La Mina (RBD 390), at 1510 Diego Portales. The [BCN record](https://www.bcn.cl/laborparlamentaria/documento?id=636175) documents that grades one through six were transferred to School No. 1; its [institutional regulations](https://fees.cl/wp-content/uploads/2019/12/Reglamento-de-convivencia-2019-2020.pdf) confirm its address and identity.
{: .text-justify}

Combined enrolment fell from **1,399 in 2004 to 977 in 2013** (`−30.2%`). In 2014 School No. 1 rose from 432 to 738 students, a jump consistent with the documented merger. The preceding decline makes demographic contraction plausible, but **does not prove it was the administrative motive for closure**; the contemporary parliamentary intervention instead discussed overcrowding and subsequent adaptations.
{: .text-justify}

Were there fewer resident children? Did the location of mining-linked households change? Did other alternatives gain enrolment? Did the range of grades change? The series makes these hypotheses worth investigating; it does not let us choose one because the place is familiar.

The viewer uses an OSM street map and MINEDUC coordinates. In the two systematic cases the line shows proximity, not destination; in El Salvador it shows the documented merger, not individual student trajectories.
{: .small}

In both cases, the opening's coordinate first appears in 2019. The map compares the selected official points; it does not reconstruct a journey made in 2016.
{: .text-justify}

These are stylised facts (descriptive patterns useful for asking questions), not experiments. The **exit and entry panels are separate samples**; I do not follow students and cannot know whether the new school received those who left the old one.
{: .small}

The carousel trajectories use **descriptive cells without regularisation** (without the adjustment that stabilises noisy estimates). The technical note uses a different cohort, exact matching, and a minimum-support rule: they are **not a second version of the same series**.
{: .text-justify}

For new schools there is no conclusive answer either. Exact support is `4/6/8` schools in SIMCE and `1/1/2` in admissions. No cohort reaches ten cases. The result is therefore **not estimable under the adopted rule**: this dataset cannot determine whether entrants perform better or worse.
{: .text-justify}

Market accounting separates change within continuing schools, enrolment reallocation, and official entry or exit. Turnover contributes `−0.000105` SD in SIMCE, with an interval crossing zero, and `+0.000113` in admissions, with a positive interval. The signs differ, and admissions observes only test takers. Since entry is also not estimable, these results **do not support the creative-destruction hypothesis**.
{: .text-justify}

### How this result relates to earlier studies

[Iocco (2024)](https://doi.org/10.2139/ssrn.4808834) follows displaced students in Chile: it reports average effects near zero and better outcomes when the receiving school performs better. It is a preprint; prolonged RBD disappearance may mix closures, mergers, or identifier changes. [Grau, Hojman, and Mizala (2018)](https://doi.org/10.1016/j.econedurev.2018.05.003), by contrast, estimate increases of `1.8–2.5` percentage points in high-school dropout and `3.9–4.4` points in fifth-grade retention among affected students. [Elacqua and colleagues](https://doi.org/10.4067/S0718-52862012000200005) examine the alternatives available to pupils affected by a closure. Their units, periods, and designs differ from this school-level descriptive analysis, so the estimates are neither averaged nor presented as an automatic contradiction.
{: .text-justify}

Here I distinguish event, entity, annex, and segment; observe spatial renewal; and extend through 2025. Without individual trajectories I do not identify destination, accessibility, or welfare.
{: .text-justify}

### What happened when I looked for effects of SAE and SLEPs

I also attempted two causal analyses: one for transfers to Local Public Education Services (SLEPs) and another for the staggered introduction of the School Admission System (SAE). Both could fail; the first was blocked before estimating an effect.
{: .text-justify}

| Analysis | Hypothesis tested | Observed result | What blocks a causal reading |
|---|---|---|---|
| Synthetic SLEP design | Transfer changes enrolment or provision relative to territories with comparable pre-transfer trajectories. | **None of the 25** territory-horizon combinations met the support rule fixed in the analysis specification. | No admissible synthetic comparison existed. For later schedule changes, the Evaluation Council's [*2025 Annual Report*, pp. 35–36](https://educacionpublica.gob.cl/wp-content/uploads/2026/03/Informe-Anual-2025-Consejo-Evaluador-del-Sistema-de-Educacion-Publica.pdf#page=35), documents case-by-case adjustments based on installation progress, sustainability, and complexity; it does not identify the schedule for the cohorts analysed here. |
| Exploratory SLEP analysis | Baseline conditions predict earlier transfer, and proximity across networks may contaminate comparisons. | Three baseline conditions showed no predictive ability distinguishable from chance: cross-validated AUC `0.53`, permutation `p=0.22`. In 53 of 70 territories there is at least one other SLEP relative to which 20% or more of its schools are within 20 km, as-the-crow-flies, of a school in that SLEP. | Failing to detect observed selection does not show that the schedule was random; the geometry shows potential interference rather than an observed spillover. |
| SAE triple difference | In 2018, concentration changes in two of the entry grades—grades 1 and 7—relative to deferred grades, differently in four regions entering that year and ten control regions. | HHI `+0.0035` `[−0.0104, +0.0174]`; log effective number of schools `−0.0042` `[−0.0265, +0.0181]`. | With the primary equal commune-grade weighting, 4 of 4 pre-period equivalence checks pass; with equal historical-region weights, both outcomes fail in 2016–2017, the immediately preceding period. There are only four treated regions, and cross-grade effects are not ruled out. |

These results do not allow me to conclude that SLEPs and SAE had no effects. For SLEPs, the causal design was rejected before an effect was estimated. For SAE, both 95% intervals—delete-one-region jackknife over 14 historical regions—include zero and values of both signs. With only four treated regions, nominal 95% coverage is approximate, and without identification the intervals do not bound the policy effect. The data let me diagnose the design's limits; they do not let me evaluate either policy.
{: .text-justify}

For SLEPs, a future evaluation would be more causally informative if the criteria setting the order of entry were documented before transfer, more treated territories accumulated, and interference, student destinations, accessibility, and outcomes were measured. For SAE, whose rollout is complete, extending the window requires pooling later cohorts with fewer not-yet-treated regions or constructing a different contrast, for example from a defensible assignment rule. These conditions would strengthen, not guarantee, a causal reading of **these designs**; until they are met, their results are exploratory signals, not impacts.
{: .text-justify}

## What public policy can use

This analysis provides **decision support**, not a rule for closing, merging, opening, or ranking schools. The prudent sequence is **observation → diagnosis → decision**. Falling enrolment or a nearby school justify diagnosis; they are not enough to decide on closure.
{: .text-justify}

| Decision stage | Signal supplied by this analysis | Indispensable additional evidence | Permissible action and safeguard |
|---|---|---|---|
| Validate the event | Distinguishes closure, annex, merger, RBD change, and education segment. | Resolutions, continuity of the parent school, and provision by level. | Ask the register's custodian to correct it; do not automatically count a disappearance. |
| Diagnose falling enrolment | Shows trajectories, operating status, and territorial differences. | Population by age, residential mobility, transfers, competition, capacity, and prior announcements. | Trigger diagnosis and support; do not use an enrolment threshold as a closure rule. |
| Plan a transition or network | Separates levels and warns that proximity is not substitution. | Actual vacancies, accessibility and travel time, destinations, support, participation, and pedagogical continuity. | Prepare scenarios and a transition plan; do not presume that a directory alternative is usable. |
| Evaluate results | Defines denominators, samples, and comparison limits. | Student follow-up and a credible counterfactual. | Measure outputs, outcomes, and impact separately; do not attribute learning, equity, or welfare to closure without causal identification. |

Institutional scope matters too. A SLEP plans and manages **its own network**, not establishments run by other providers. [Law 21,040, Article 18(c) and (t)](https://www.bcn.cl/leychile/navegar?idNorma=1111237) requires each SLEP to develop public provision, safeguard coverage—including areas of population growth or insufficient coverage—and ensure continuity of educational pathways. Paragraph (t) adds monitoring and support for retention and re-engagement. MINEDUC is the governing authority for the education system; the Directorate of Public Education coordinates and strategically steers the Public Education System. The [2026 Annual Local Plan](https://dep.gob.cl/pal-2026/) plans technical support, infrastructure, and staffing on the basis of course numbers and enrolment. None of these functions grants authority over other providers, turns the study into administrative authorisation, or establishes that one governance model performs better than another.
{: .text-justify}

Two targeting errors deserve attention. A **false positive** would flag a school as unviable because enrolment is falling with the local population even though it remains necessary for access. A **false negative** would miss a risky transition because aggregate enrolment looks stable even as particular levels, territories, or groups lose an effective option. IVE-SINAE helps describe aggregate school composition; it does not identify individual poverty or decide by itself where to intervene.
{: .text-justify}

An evaluable theory of change distinguishes five levels. **Inputs:** valid event records, demographics, capacity, accessibility, and destinations. **Activities:** diagnosis, support, transition planning, and follow-up. **Outputs:** a classified event, a capacity audit, and a transition plan. **Intermediate outcomes:** continuity, travel, attendance, and retention. **Impacts:** learning and equity. The chain assumes actual vacancies, acceptable transfers, and community participation; those assumptions also need testing. **This post proposes the chain for evaluation; it does not establish that it already works.**
{: .text-justify}

## What is missing for causal inference

| Route | What it could answer | Test that could make it fail |
|---|---|---|
| Staggered SLEP rollout | Compare early and late transfers if timing does not depend on potential outcomes. | Timing linked to readiness, inadequate pre-treatment support, or interference across territories. |
| SAE triple difference | Compare entry and deferred grades across early and control regions. | Too few treated clusters, placebos that depend on weighting, or cross-grade effects. |
| Event study or difference-in-differences | Compare trajectories with a credible control group. | Incompatible pre-trends or anticipation of closure. |
| Discontinuity or instrumental variable | Exploit a rule that changes closure probability. | Manipulation, weak first stage, or implausible exclusion. |
| Individual follow-up | Measure destination, transport, and later outcomes. | Selective attrition or incorrect links. |

### The question left for a third instalment

The national demographic projection makes this discussion more important, but it does not provide a closure calendar. Before applying it to a commune or locality, we need population by age, household mobility, school participation, capacity, and provision by level. A national decline can coexist with neighbourhoods that need new schools.

A third instalment could build territorial scenarios to anticipate where to support, expand, reorganise, or preserve education capacity. Its useful product would not be a list of establishments destined to close.

<details class="technical-disclosure" markdown="1">
<summary>Technical note and robustness checks</summary>

This section preserves the figures needed to audit the exercise without turning the main story into an execution log.

**Coverage and residual debt.** The identity registry assembled 14 official aliases and two candidate temporal successions; the latter touch none of the 337 exits in the risk panel, but the registry does not establish that every possible recoding has been detected. The selection audit shows uneven support across provider type, rurality, and region, so the results describe the observed sample rather than a national population effect. For SLEPs, none of the 25 territory-horizon combinations passed synthetic support: the rule fixed in the analysis specification required at least 10 eligible and 3 effective donors, a maximum weight of `0.50`, pre-treatment RMSPE no greater than `0.25` SD, last-pre-period errors no greater than 5% for enrolment and 2% for schools, and at least two admissible territories per cell and five overall. The follow-up diagnostic uses 2015 public enrolment, active public schools, and students per school to distinguish 26 territories transferred by 31 December 2025 from 44 not yet transferred, using ridge logistic regression, five-fold cross-validation, and 1,999 permutations. The exact AUC was `0.5341` with permutation `p=0.2195`: it showed no predictive ability distinguishable from chance and does not establish random assignment. High overlap is pairwise: relative to at least one other SLEP, 20% or more of the territory's schools are within 20 km, as-the-crow-flies, of a school in that SLEP; it does not require contiguous territories. For SAE, all four primary placebos fell within the fixed margins, but the historical-region sensitivity passed only two of four and the post contrast uses just four treated regions. The literature provides context: this post makes no exhaustive novelty claim.

**SAE.** The 2017–2018 triple difference compares two of the entry grades, grades 1 and 7, with grades 2–6 and 8, across four regions entering in 2018 and ten not-yet-treated rollout regions. The [official MINEDUC guide](https://www.mineduc.cl/wp-content/uploads/sites/19/2018/01/guia-informativa.pdf) confirms the sequence: Magallanes entered for the 2017 school year, followed by Tarapacá, Coquimbo, O’Higgins, and Los Lagos for 2018. Magallanes is excluded; Ñuble is pooled with Biobío because that was the geography receiving the assignment. Inference uses a delete-one-region jackknife over 14 historical clusters. The intervals are unadjusted; the Holm-adjusted p-value is `1.0` for both outcomes. HHI and `log(1/HHI)`, the log effective number of schools, are two scales of the same index. They cover all observed regular basic-education enrolment by commune-grade and all provider types, not only SAE applicants; an applicant-level effect would therefore be diluted by students who did not apply, and the outcomes are not independent signals. HHI is `+0.003513` `[−0.010368, +0.017395]`; the log effective number is `−0.004192` `[−0.026491, +0.018106]`, approximately `−0.4%` `[−2.6%, +1.8%]` in the effective number. As a descriptive reference, the 2017 commune-grade mean HHI was `0.1913` and the arithmetic mean effective number was `12.48`. The pre-period margins fixed in the specification—`±0.02` for HHI and `±0.05` for the log—exceed even the bounds of the 2018 intervals: passing them cannot rule out pre-trend deviations as large as any effect those intervals allow. An independent R oracle reproduces twelve cells within `1e−10`. This is an exploratory DDD: the p-values are descriptive, not randomisation inference.

**Local markets.** The H1 estimand compares the risk difference between the 75th and 25th percentiles of concentration across six spatial neighbourhoods with the same difference under the commune. It is a relative-position sensitivity, not the effect of redrawing a market. No band excludes zero: the upper bounds of the contrasts are `0.273108` and `0.375248` percentage points. The main practical-relevance threshold was `0.5` percentage points, with sensitivities at `0.25` and `1.0`; I set them before estimating H1. They are neither concentration-index thresholds nor policy rules.

**Exits and sensitivity.** MR1-SIMCE is `+0.029` SD `[−0.095, +0.158]` with 21 closures. The `weighted_raw` variant gives `+0.034` `[−0.225, +0.289]`. Core admissions is `NOT_ESTIMABLE` with eight closures in both the primary result and its sensitivities. The academic track has seven; the technical-vocational track has zero comparisons with strict support. Science covers only students who chose and took that test.

Regression to the mean means an extreme tends to move closer to the average when remeasured; this occurred among open schools. This diagnostic is unmatched, does not apply MR1 shrinkage, and assigns no closure event. The administrative closure route under Law 20.529 is another rival mechanism.

**Entrants.** MR2 remains `NOT_ESTIMABLE` in both outcomes: cohort support is 4/6/8 for SIMCE and 1/1/2 for admissions, insufficient to publish estimates or intervals. Promoting unsupported signs would change the rule after looking. The protocol is retrospective, not a prospective preregistration: it records ten deviations; minimum supports of 5, 10, and 20 were planned, but only 10 was run. This publication therefore does not present the threshold as a robustness test or use under-supported points to draw a conclusion.

**Decomposition.** Markets are commune by exact segment. Official turnover combines entry and exit: SIMCE `−0.000105` `[−0.000346, +0.000103]`; admissions `+0.000113` `[+0.000027, +0.000213]`. The between component (reallocation among incumbents) is larger: `+0.004777` in SIMCE and `+0.001858` in admissions. The accounting identity closes with a maximum residual of `6.66e−16`, below the `1e−10` tolerance. These are identities, not causes.

**Territory and coordinates.** The spatial exercise retains 38 matched closures and 29 unique openings. Each entry uses the first valid official coordinate between its entry year and 2025; 9 unstable trajectories are excluded and 259 entries have a delayed coordinate. The national audit covers 12,116 official rows: 12,038 operating establishments and 78 authorised without enrolment, reported separately. Of that total, 6,601 have at least one OSM candidate, 5,515 do not, and 126 rows were reviewed. There are zero confirmed official errors. OSM is a secondary source; the public product contains aggregates and does not redistribute the combined establishment-level table.

**Reproducibility.** The aggregate figures from this run are reproducible; the scientific snapshot is tied to a local Git anchor and a verifiable freeze. Python prepared the private input CSV; R produced the aggregates, ran 999 bootstrap replications (resamples used to measure uncertainty), and Python reconciled the point estimates in 112 public aggregate cells. That agreement reduces implementation error, not causal confusion.

</details>

## Closing: evaluate the transition, do not celebrate movement

Extending the thesis revealed that “closure” concealed stocks, events, empty schools, annexes, and RBD replacements; “market” mixed nurseries, primary schools, and secondary schools; “renewal” confused proximity with destination.
{: .text-justify}

The creative-destruction hypothesis is attractive; that is why it requires a strict test. There are signals, gaps, and demographic pressure, but no evidence for celebrating turnover.
{: .text-justify}

The movement exists. What remains unknown is who gains continuity and who ultimately pays for the transition.
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
