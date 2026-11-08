---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extending my thesis in 3 spoonfuls (part IV): do school closures close the door to higher education?"
subtitle: "Much of the higher-education entry gap preceded closure. With pupil and school history, the estimated difference in total entry is near zero; the full model estimates an IP/CFT contraction that the cohort comparison cannot distinguish from zero."
date: 2026-11-04 10:00:00 -0300
last_modified_at: 2026-11-07 23:40:00 -0300
categories: [data, education, public-policy]
tags: [education, school-closure, higher-education, sies, paes, causal-ml, double-ml, difference-in-differences, econometrics, duckdb, public-policy, education-policy]
description: "School closure and higher-education entry in Chile: prior gaps, adjusted estimates, IP/CFT pathways, and causal limits (2007–2026)."
excerpt: "The raw 2016–2019 entry gap was −14.64 points; an earlier cohort at the same schools already showed −12.00. In a different sample, the full model estimated −0.29 for total entry and −2.09 for IP/CFT. The −12.26 and −0.26 estimates refer to G1 quintiles redefined by different models, not recovery among the same pupils."
author: clabra
lang: en
ref: cierre-escolar-educacion-superior-causal-ml
permalink: /datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/
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
    audio: unknown
---

When a secondary school closes, finding another school place does not settle a pupil's later trajectory. Years later, entering and remaining in higher education become important questions. [Part III]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/' | relative_url }}) followed immediate school trajectories. This instalment examines **14 closure cohorts, from 2009 to 2022**. Within that broader picture, the detailed **2016–2019** analysis asks how much disadvantage preceded closure.

<aside class="notice--primary" markdown="1">
**Finding for 2016–2019.** With individual and school histories included, the estimated difference in total higher-education entry is **−0.29 percentage points** (interval **−2.64 to +2.06**). The conditional estimate for professional institutes and technical training centres (IP/CFT) is **−2.09 points** (interval **−3.50 to −0.68**).

**Comparison.** In exact cells for 2016–2019, the raw entry-rate gap was **−14.64 points**. An earlier cohort at the same schools already showed a **−12.00-point** gap.

**Limit.** These comparisons use different samples and estimators. The repeated-cohort difference-in-differences estimate for IP/CFT is **−2.59 points** (*p* = **0.28**) with 12 treated secondary schools and does not distinguish that decline from zero. Individual destinations and family circumstances remain incompletely observed.
</aside>

Linking MINEDUC, SIES and openly licensed PAES/PDT records, I start with differences across periods, then examine 2016–2019 using pupils' prior trajectories and an earlier cohort at the same school. Models for that window do not automatically represent all 14 cohorts. The [methodological annex]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}) retains the detailed estimates, figures, sources, and specifications.

<!-- Legacy pipeline identifier retained for gate compatibility; G1 is re-ranked by specification, and harm to a fixed group is not established. -->
<!-- scientific-state: POST4_HIGHER_EDUCATION_CAUSAL_ML_V1; result: SELECTION_DOMINATES_AVERAGE_IPCFT_AND_G1_VULNERABLE_HARMED -->
<!-- publication-readiness: READY_INDIVIDUAL_SIES_AND_PAES_VERIFIED -->

{% include thesis-series-nav.html current=4 %}

## Spoonful 1: how much disadvantage was there already?

Looking across **14 closure cohorts from 2009 to 2022** tests how much the reading depends on period. For secondary pupils, estimated total entry in **2009–2015** was **+0.55 points** (interval **−2.07 to +3.18**); in **2016–2019**, **−2.64** (interval **−7.54 to +2.25**); and in **2020–2022**, **−3.79** (standard error **1.81**, interval **−8.22 to +0.64**). The later regimes involve far fewer treated secondary schools: **12** in 2016–2019 and **7** during the pandemic. Point estimates for IP/CFT turn negative from 2016, but each regime-specific test against zero is imprecise. I have not directly tested differences between regimes, nor identified the effect of any one reform. The annex keeps the [longitudinal figure and regime table]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#fig-post4-2), including educational level, persistence, and graduation censoring.

That overview comes before the detailed analysis: **2016–2019 is one window within the series, not a substitute for it**. For that window, the documented specifications compare the later gap with individual and school histories. Their results retain that temporal scope.

For secondary-school closures in **2016–2019**, direct comparison within exact cells finds higher-education entry among **50.61%** of exposed pupils and **65.24%** of controls: a **−14.64-percentage-point** gap. It is an observed difference, not a closure effect. The first step in a separate modelled sample adjusts for demographics and school administration and yields **−13.24 points**. I do not combine the rates and the model coefficient as though they shared a denominator. Their value is the question they raise: did the two groups have comparable prospects before anything closed?

The data say no. Four years earlier than the exposed cohort, another cohort at the same schools, while they were still open, entered higher education at a rate **12.00 points** below its controls in the exact cells (**51.78%** versus **63.78%**). That pre-existing gap is **82.0% of the −14.64-point raw cell gap**. It is not 82.0% of every model result. Separately, adding pupils' prior grades, attendance, repetition, and mobility to the model that began at −13.24 changes its estimate to **−5.63 points**. Pupil history and school history overlap: summing those reductions would count some disadvantage twice.

International research documents short-run disruption after school closures and shows why receiving schools matter[^engberg2012][^brummet2014][^grau2018][^beuchert2018][^bross2023][^abdulkadiroglu2026]. Evidence on entry to higher education years later is thinner, and findings across countries or periods cannot simply be substituted for Chile's[^larsen2020][^kim2024]. The initial Chilean comparison cannot support the headline that closure itself destroyed 14 points of access. The earlier school cohort reveals substantial selection before closure. To ask whether an additional difference remains, I need a comparison across cohorts rather than two final rates.

I linked the school panel to SIES enrolment and graduation and openly licensed PAES/PDT admissions records using a masked individual identifier. These data distinguish university entry from IP/CFT entry. They do not explain why each person chooses, postpones, or abandons a route. The [provenance, licensing, and coverage]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#fuentes-y-custodia) are documented separately.

An earlier cohort is not the observed alternative future of the same young people. It consists of other pupils who attended the same school before the exposed cohort. Its value is to show that the institution had an access disadvantage well before the closure episode. Matching schools by region or governance alone is insufficient if pupils differ in marks, attendance, and movement between schools. Such histories can predict both a school's future exit and later higher-education entry. The records cover some of that history; household income and family decisions remain incomplete. Thus 82.0% is a descriptive ratio between two gaps in the same exact cells, not a definitively explained causal fraction.

This changes the policy question. A large raw gap demands attention to the vulnerability of displaced pupils, but attributing all of it to the final closure could direct help at the wrong moment. I need to learn whether a further difference appears when I compare cohorts at the same school and pupils with similar earlier trajectories. That is the second spoonful.

## Spoonful 2: what changes once I account for that history?

My clock starts with the school's last open year, **G−1**. For a pupil in grades **7 through 11** (Chile's 7.º Básico through 3.º Medio), I calculated when they would have finished the final secondary year without repeating and checked higher-education enrolment in that year or the next. A two-year window allows some delay without immediately calling it dropout. I separated total entry, university, IP/CFT, second-year persistence, and graduation when enough time had elapsed. A recent cohort may not yet have had time to graduate; that censoring is not a negative outcome. The annex states the [cohort definitions and horizons]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#cohortes-y-horizonte).

Before using the linkage, I checked classification and support on the actual records. Likely whole-school transfers are excluded by the D2 rule from part III; combining them with dispersed closures would change the population. Nor could I compare 2016–2019 closures only with schools that would close later under eight exact conditions: **zero cells** retained the four required arms. I therefore used clean, still-open control schools with explicit matching and sensitivity checks. <span id="fig-post4-2"></span>The annex shows [excluded continuities]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#fig-post4-2) and this support failure. Zero valid cells does not mean zero effect.

The repeated-cohort strategy compares two cohorts from the same secondary school: one cohort encountered the closure, and another attended years earlier. I subtract the corresponding change in control schools from each comparison. This removes enduring disadvantage that a post-closure comparison cannot see. The central assumption is that, without closure, the change between cohorts would have been comparable in treated and control schools[^roth2023]. A reform, changing family composition, or a local shock that hits future closing schools differently could break it. The G−5 history addresses an important rival explanation; it does not turn closure into random assignment.

For secondary pupils, the repeated-cohort difference-in-differences estimate is **−2.64 points**, interval **−7.54 to +2.25**: this support cannot distinguish a fall from zero. The flexible model that includes both individual and school history yields **−0.29 points**, interval **−2.64 to +2.06**. An additive model and a doubly robust estimator give **−0.91** and **+0.19 points**, respectively. These comparisons lie near zero under their populations and assumptions. They do not prove that there was no effect anywhere. The figure shows each step and its sample, while the [full analytic table]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#tabla-post4-a2) retains outcomes and uncertainty.

<figure class="post3-figure data-visualization" id="fig-post4-1">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post4/selection-ladder-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post4/selection-ladder-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post4/selection-ladder-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post4/selection-ladder-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post4/selection-ladder-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post4/selection-ladder-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" width="1600" height="850" src="{{ '/assets/images/tesis-post4/selection-ladder-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post4/selection-ladder-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post4/selection-ladder-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post4/selection-ladder-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post4/selection-ladder-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post4/selection-ladder-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post4/selection-ladder-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post4/selection-ladder-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post4/selection-ladder-en-dark.svg' | relative_url }} 1600w" alt="Adjusted-comparison ladder for 2016–2019 school closures in secondary and upper elementary education. In secondary education, the initial gap adjusted for demographics alone is minus 13.24 percentage points; adding pupils' prior academic history changes it to minus 5.63 points; a repeated-cohort difference-in-differences comparison against G minus 5 gives minus 2.64 points; and full Double ML with G minus 5 school history estimates minus 0.29 points for total entry and a difference of minus 2.09 points for professional institutes and technical training centres, distinguishable from zero under that model. In upper elementary education, the estimates +1.21 and +1.02 points have intervals that include zero." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 1</strong> — Comparison ladder for 2016–2019 closures: the −13.24-point secondary-school gap belongs to the first modelled step; later steps adjust individual (G−1/G−2) and school (G−5) histories under their own samples and assumptions. For upper elementary pupils, intervals around +1.21 and +1.02 include zero. <span class="figure-source">Source: my calculations from the longitudinal MINEDUC–SIES linkage, 2004–2026.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post4/selection-ladder-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

The flexible Double Machine Learning model uses cross-validation by school[^chernozhukov2018]. It learns how marks, attendance, age for grade, and earlier trajectories relate to outcomes in some schools and predicts in others. This separation limits memorisation of a particular closing school. It cannot recover unrecorded family income, parental support, or application decisions. I report a partially linear and a doubly robust estimate because their weights and assumptions differ. Their proximity supports some stability of the average across models, while common support and omitted-confounder sensitivity still matter. The [technical specification]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#especificaciones-causal-ml) sets out the estimators and school-level uncertainty.

Among pupils in **grades 7 or 8**, the corresponding 2016–2019 difference-in-differences estimate is **+1.21 points** (interval **−3.39 to +5.81**) and the full model gives **+1.02** (interval **−2.44 to +4.47**). Both ranges include plausible losses and gains; neither proves equality. The G−5 cohort in grade 7 might still have attended the school at closure. If so, the supposedly earlier reference could also have been exposed and a negative difference attenuated. More years of schooling remained after a move at that age, but time alone does not establish protection. This distinction by age helps specify whom follow-up must cover.

Graduation demands another timing caveat. SIES data for that outcome run to 2025, so someone whose expected entry was in 2019 or later may not have completed a full course. A censored graduation number cannot be compared across regimes as though follow-up were equal. Group sizes also change: the pandemic row for grades 7–8 relies on **four treated school clusters** and is descriptive. Keeping these warnings beside the series prevents an isolated numerical contrast becoming a policy story that the data cannot distinguish.

The same series offers a composition check compatible with the rule excluding likely block transfers. The D1-minus-D2 cases have much higher postsecondary entry rates than the clean-closure group. Combining them would alter sample composition and the comparison itself. That difference does not validate the rule on its own, verify the legal status of any episode, or establish the direction or size of causal bias. The next step searches for differences within the filtered population.

Comparable trends are especially uncertain when each regime contains few treated secondary schools. Confidence bands express some of that imprecision but cannot observe every reason a school weakened before closure. A near-zero estimate under the full model rules out sufficiently large average falls incompatible with its interval under that model. It does not establish that every cohort, pathway, or pupil was unharmed. I therefore change outcome in the final spoonful and ask where a signal remains.

## Spoonful 3: what can I say about vocational and technical entry?

An estimated average close to zero for total entry can conceal shifts between routes. In the full model with G−5 school history, the estimate for **IP/CFT** is **−2.09 percentage points** (standard error **0.72**, *p* = **0.0037**, interval **−3.50 to −0.68**). The university estimate under the same specification is **+1.98 points**, interval **−0.22 to +4.19**. The surviving signal is a **conditional estimated contraction in the IP/CFT channel**. In contrast, the 2016–2019 repeated-cohort comparison estimates **−2.59 points** for IP/CFT (standard error **2.29**, *p* = **0.28**, **12 treated schools**); its uncertainty includes zero. I cannot tell how much of the IP/CFT change is a net loss of higher-education entry and how much is substitution towards university. A balance of average rates does not follow the same person between destinations.

The measured outcome is enrolment within two years of expected entry. It cannot reveal whether a change of pathway was chosen, forced by available places, or delayed. I would need mutually exclusive individual histories for that. The distinction matters for support: recovering a lost place, helping someone switch course, and supporting a deliberate choice are different tasks. The table in the annex keeps [separate institutional outcomes]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#tabla-post4-a2) rather than treating one fall as a complete destination map.

I explored whether pupils' pre-closure characteristics predict different estimated responses, using school-level cross-validation to avoid memorising one institution. With individual controls in the R-Learner[^niewager2021], the quintile **G1 with the lowest predicted effect** records **−12.26 points** in total entry and **−11.48** in second-year persistence. It contains **99.5%** secondary pupils and **77.2%** on the vocational track. When I add G−5 school history, the model sorts pupils again: the **new G1** contains **91.2%** secondary pupils and **51.8%** on the vocational track, and records **−0.26 points** in total entry (interval **−2.73 to +2.21**). The BLP test no longer distinguishes heterogeneity in total entry from zero (*p* = **0.6583**). These are **re-estimated quintiles with different composition**, not a measured recovery for the same people. <span id="fig-post4-3"></span>The annex preserves the [profile figure]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#fig-post4-3) and [full results JSON]({{ '/assets/data/tesis-post4/post4_higher_education_causal_ml_v1.json' | relative_url }}).

A predictive ranking does not automatically become a personal causal effect. G1 through G5 are quintiles of a score learnt by the model, not administrative groups defined before the study. A BLP test asks whether that score orders systematic differences outside training; GATE averages and CLAN profiles then describe where a signal appears. In this observational setting, propensity and outcomes are modelled, while common support, unmeasured factors, and small numbers of treated school clusters remain consequential. That is why I present the outcome by channel before using profiles to guide attention.

For IP/CFT, the slope of heterogeneity in the full model remains positive (**0.425; p = 0.0177**). Its G1 estimate is **−2.57 points**, interval **−5.68 to +0.54**, which includes zero; the largest point decline occurs in G3, **−3.92 points**. Quintiles do not form a monotone gradient. I cannot describe G1 after full adjustment as the identified worst-hit group. Lower attendance and vocational enrolment are useful prompts for follow-up, not proof of the mechanism behind the channel difference.

PAES/PDT admissions records let me inspect another route. After adjusting individual and school history, estimated entry to the most selective **20% of programmes** is **+1.75 points** (interval **−1.12 to +4.62**), indistinguishable from zero. Centralised application is estimated at **+4.30 points** (interval **+1.05 to +7.55**), an anomaly that might reflect over-adjustment against a historically low starting point. I do not interpret it as resilience caused by closure. The [admissions table]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#tabla-post4-a5) separates test-taking, application, enrolment, and programme selectivity.

A formal omitted-variable analysis[^cinellihazlett2020] sizes, but cannot close, another objection. In the linear projection associated with the IP/CFT result, a hidden factor explaining **6.16%** of residual variation in both closure and enrolment would move the point estimate to zero; at **2.33%**, its 95% interval would include zero. Marks and attendance are weak benchmarks here because they barely predict closure after the other controls. The school's G−5 history is a more demanding benchmark; an unmeasured family factor could behave differently. The [parameters and bounds]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}#confusion-omitida) are reported without presenting a threshold as a causal guarantee.

One hypothesis is that closure interrupts guidance, practical-placement agreements, or specialism continuity relevant to IP/CFT. I have not measured those networks directly. A rival explanation is substitution: some who would have entered IP/CFT may instead enrol at university. A discriminating check needs **mutually exclusive individual trajectories**: IP/CFT, university, both at different times, or neither. If most of the IP/CFT decline appears at university, I would reject net access loss as the general explanation; if it appears outside all higher education, that explanation becomes more plausible. Omitted-confounder sensitivity remains another condition on either reading.

## Closing: separate selection, pathway, and mechanism

Here the first spoonful showed that a large raw access gap had an important precedent in schools and pupils before closure. The second compared cohorts and adjustments: under the full model, the estimated difference in total entry approaches zero without proving equality. The third found a **−2.09-point** estimated contraction in IP/CFT entry. The lowest predicted-effect quintile records **−12.26** with individual controls and **−0.26 points** with school history, but it is re-estimated under each specification; the figures do not track a fixed group. The total-entry heterogeneity test ceases to distinguish a pattern from zero.

I propose careful follow-up for vocational-track pupils moving between secondary schools: continuity of specialisms, guidance, support, and postsecondary destinations. That is a precaution in response to a localised signal, not evidence that such a protocol works or proof of net access loss. Three observable tasks remain:

1. **Trace destinations.** Distinguish IP/CFT, university, both, and neither in individual enrolment histories to separate substitution from net loss.
2. **Measure mechanisms.** Record guidance, placement agreements, and recognition of prior learning before and after closure; these remain hypotheses.
3. **Test robustness.** Add family background and more schools in each period, recalculate confidence intervals, and compare the IP/CFT linear-projection robustness value with its present **2.33%** threshold.

If substitution predominates, support should focus on choice and continuity. If exclusion predominates, restoring access is the priority.

## References

[^abdulkadiroglu2026]: Abdulkadiroğlu, Atila, Parag A. Pathak, and Christopher R. Walters. 2026. [“Who Gets What in Education: Can School Matching Improve Student Achievement?”](https://doi.org/10.3386/w34936) NBER Working Paper 34936. [Scholar](https://scholar.google.com/scholar_lookup?title=Who+Gets+What+in+Education%3A+Can+School+Matching+Improve+Student+Achievement%3F&doi=10.3386%2Fw34936)

[^beuchert2018]: Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen, and Nina Smith. 2018. [“The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?”](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47. [Scholar](https://scholar.google.com/scholar_lookup?title=The+short-term+effects+of+school+consolidation+on+student+achievement%3A+Evidence+of+disruption%3F&doi=10.1016%2Fj.econedurev.2018.05.004)

[^bross2023]: Bross, Whitney, Douglas N. Harris, and Lihan Liu. 2023. [“The Effects of Performance-Based School Closure and Restart on Student Performance.”](https://doi.org/10.1016/j.econedurev.2023.102368) *Economics of Education Review* 94: 102368. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effects+of+performance-based+school+closure+and+restart+on+student+performance&doi=10.1016%2Fj.econedurev.2023.102368)

[^brummet2014]: Brummet, Quentin. 2014. [“The Effect of School Closings on Student Achievement.”](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–24. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effect+of+school+closings+on+student+achievement&doi=10.1016%2Fj.jpubeco.2014.06.010)

[^chernozhukov2018]: Chernozhukov, Victor, Denis Chetverikov, Mert Demirer, Esther Duflo, Christian Hansen, Whitney Newey, and James Robins. 2018. [“Double/Debiased Machine Learning for Treatment and Structural Parameters.”](https://doi.org/10.1111/ectj.12097) *The Econometrics Journal* 21 (1): C1–C68. [Scholar](https://scholar.google.com/scholar_lookup?title=Double%2Fdebiased+machine+learning+for+treatment+and+structural+parameters&doi=10.1111%2Fectj.12097)

[^cinellihazlett2020]: Cinelli, Carlos, and Chad Hazlett. 2020. [“Making Sense of Sensitivity: Extending Omitted Variable Bias.”](https://doi.org/10.1111/rssb.12348) *Journal of the Royal Statistical Society: Series B (Statistical Methodology)* 82 (1): 39–67. [Scholar](https://scholar.google.com/scholar_lookup?title=Making+Sense+of+Sensitivity%3A+Extending+Omitted+Variable+Bias&doi=10.1111%2Frssb.12348)

[^engberg2012]: Engberg, John, Brian Gill, Gema Zamarro, and Ron Zimmer. 2012. [“Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?”](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203. [Scholar](https://scholar.google.com/scholar_lookup?title=Closing+schools+in+a+shrinking+district%3A+Do+student+outcomes+depend+on+which+schools+are+closed%3F&doi=10.1016%2Fj.jue.2011.10.001)

[^grau2018]: Grau, Nicolás, Daniel A. Hojman, and Alejandra Mizala. 2018. [“School Closure and Educational Attainment: Evidence from a Market-Based System.”](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf) *Economics of Education Review* 65: 1–17. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)

[^kim2024]: Kim, Jeonghyeok. 2024. [“The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes.”](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963. [Scholar](https://scholar.google.com/scholar_lookup?title=The+Long+Shadow+of+School+Closures%3A+Impacts+on+Students%27+Educational+and+Labor+Market+Outcomes&doi=10.26300%2FAX4M-3Z14)

[^larsen2020]: Larsen, Matthew F. 2020. [“Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment.”](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980. [Scholar](https://scholar.google.com/scholar_lookup?title=Does+closing+schools+close+doors%3F+The+effect+of+high+school+closings+on+achievement+and+attainment&doi=10.1016%2Fj.econedurev.2020.101980)

[^niewager2021]: Nie, Xinkun, and Stefan Wager. 2021. [“Quasi-Oracle Estimation of Heterogeneous Treatment Effects.”](https://arxiv.org/pdf/1712.04912) *Biometrika* 108 (2): 299–319. [DOI](https://doi.org/10.1093/biomet/asaa076) · [Scholar](https://scholar.google.com/scholar_lookup?title=Quasi-oracle+estimation+of+heterogeneous+treatment+effects&doi=10.1093%2Fbiomet%2Fasaa076)

[^roth2023]: Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–44. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)
