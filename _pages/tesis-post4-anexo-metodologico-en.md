---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Part IV methodological annex: higher education and causal machine learning"
description: "Sources, tables, supplementary figures, and specifications for part IV of the thesis extension series."
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
---

{% include thesis-series-nav.html current=4 %}

This annex retains the study populations, detailed tables, supplementary figures, specifications, and sources behind the [main article]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/' | relative_url }}). Table numbers beginning with A belong to this annex, while figure IDs remain stable for existing links. Every estimate depends on the population, outcome, and assumptions of its comparison.

## Data linkage and support

### Two school-outcome checks revisited here

Before turning to universities and technical institutes, I return to [part III]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/' | relative_url }}). There I showed that, after a school closure in 2016–2019, **progression failure or grade lag** (no enrolment or enrolment below the expected grade one year later) rose by **+5.29 percentage points** (+2.08 to +8.51 pp, with Manski 2003[^manski2003] partial-identification bounds of −1.15 to +10.98 pp). That article and its annex already report two sensitivity checks motivated by the staggered difference-in-differences literature (Callaway and Sant'Anna 2021[^callaway2021]; Roth et al. 2023[^roth2023]). I bring them together here for reference: one examines deviations from **parallel trends**; the other anchors the exposed cohort **two years before closure ($$G-2$$)** rather than one year before ($$G-1$$).

<aside class="notice--info" markdown="1">
**Two sensitivity checks on part III**

- **Non-parallel trends (simplified linear version inspired by Rambachan and Roth 2023[^rambachan2023]):** I compare the largest pre-closure deviation observed between $$G-4$$ and $$G-2$$ with the post-closure bias required for the conventional confidence interval to include zero. The multiplier $$M^*$$ summarises that ratio. This is not the output of the formal HonestDiD procedure and does not incorporate bounds for missing outcomes.
- **Anchoring at $$G-2$$ rather than $$G-1$$:** I separate pupils already enrolled at the school two years before closure from those who entered in its final open year. Differences between the groups inform prior selection; they do not isolate a causal effect of mobility.
</aside>

{: .table-caption}
<span id="tabla-post4-a1"></span>
**Table A1.** Retrospective closure of part III: robustness to non-parallel trends (simplified linear version inspired by Rambachan and Roth) and anchoring two years before closure ($$G-2$$, 2016–2019 window)

| Retrospective test on school outcomes (2016–2019) | Grade progression failure or lag | Persistent 2-year non-enrolment | Scope of the comparison |
|---|---:|---:|---|
| Baseline estimate at $$G-1$$ (part III) | +5.29 pp [+2.08; +8.51] | +0.63 pp [−0.77; +2.03] | Starting point for 4,815 and 3,666 exposed pupils. |
| Largest observed pre-closure drift between cohorts | 0.40 pp (95% bound: 0.81 pp) | 0.41 pp (95% bound: 0.74 pp) | The largest prior point deviation was below half a point. |
| Later bias that would bring the 95% interval to zero | 2.54 × prior bound (0.81 pp) = 5.21 × prior point drift (0.40 pp) | The interval already spanned zero | In this separate test, later bias of 2.54 times the prior bound would make the conventional interval include zero; it does not resolve missing outcomes. |
| Pupils stable since two years earlier ($$G-2$$; 70.58% of the descriptive population of 6,581 exposed) | +3.87 pp [+1.04; +6.69] | +0.07 pp [−1.44; +1.58] | The progression estimate uses 3,556 supported stable treated pupils versus 4,815 treated pupils in a separate baseline sample; full-sample bounds still cross zero. |
| Late entrants in the final year ($$G-2 \to G-1$$, 26.55% of the descriptive population of 6,581 exposed) | +9.58 pp [+5.06; +14.10] | +2.62 pp [−0.29; +5.52] | This supported subsample has 1,033 late treated pupils; the between-group contrast does not identify its cause. |
{: .table--compact .table--scroll}

Table A1 sharpens two checks from part III without resolving missing-data bounds. The simplified pre-trend test suggests that, under its separate criterion, a later trend deviation of up to **2.54 times** the upper prior bound would leave the conventional progression interval excluding zero[^rambachan2023]. It is not a full HonestDiD analysis or a cure for missing outcomes. Among pupils stable since $$G-2$$, the estimated gap is **+3.87 pp** rather than +5.29 pp, a **1.42-point** reduction (27%); late entrants show **+9.58 pp**. The supported samples contain 3,556 stable and 1,033 late treated pupils. In the initial descriptive population of 6,581 exposed, 70.58% were stable, 26.55% entered in $$G-1$$, and the remaining 2.87% had no $$G-2$$ record at that school because they attended its entry grade. The recent full-population missing-data bounds still cross zero. The question is whether any difference persists at higher-education entry and how much preceded closure.

<aside class="notice--info" markdown="1">
**Methodological note — How the econometric upgrades across parts I, II, and III connect to this series finale:** Updating all four installments under a unified empirical standard ties the entire research arc together: in **part I** (1992–2012), the Mundlak–Chamberlain decomposition separates the permanent smaller scale of exiting schools (−5.90 and −6.23 pupils per teacher) from their internal pre-closure contraction (−0.216 and −0.148 per year), while the out-of-sample discrete-time hazard reaches an AUC of 0.8517 (capturing 43.7% of closures in the top risk decile). In **part II** (2013–2025), Empirical Bayes shrinkage across 97.9% of closures with SIMCE (95 recovered closures; +0.0061 SD) and 95.7% with admissions (44 recovered closures; −0.0420 SD) does not support gains after accounting for selection, and McFadden's conditional logit across 9,093 individual transfers shows that families reallocate by physical proximity (median 1.83 km, $$\hat{\beta}_{\text{dist}}$$ = −0.4029 per km) and municipal boundaries (OR = 3.397) rather than destination SIMCE scores (OR = 0.794, not significant; mean realized change of −0.035 SD). Finally, in **part III** (2005–2025), the approximate Lee monotonic trimming band ([+3.79; +6.80 pp]) in the [public econometric-audit JSON]({{ '/assets/data/tesis-post4/trilogy_econometric_upgrades_v1.json' | relative_url }}) at the post_iii_upgrades → m2_stratified_manski_and_lee_bounds → full_63_episodes → lee_monotonic_bounds_pp path (a Part III technical output not displayed in its article or annex), Manski bounds in closures with at least 90% valid school reports ([+0.09; +7.84 pp]), and the descriptive −3.35 pp difference between receiving-school groups are partial sensitivity checks. That difference has no interval of its own, and family choice precludes attributing it to receiving-school quality.
</aside>

### How I rebuilt the bridge to SIES and PAES without breaking privacy or license rules

To follow every student from their school desk into higher education, I assembled and audited three families of official administrative records totaling **57 microdata packages** linked through MINEDUC's masked individual identifier (MRUN, an encrypted national ID that enables longitudinal research without ever exposing a person's RUT or name):

- **SIES Higher Education Enrollment (2007–2026, 20 complete years):** from 971,644 enrollment records in 2007 to 1,448,106 in 2026, with valid MRUN coverage exceeding 99.7% across the analytical window, distinguishing each year whether the student enrolled in a **University**, a **Professional Institute (IP)**, or a **Technical Training Center (CFT)**.
- **SIES Higher Education Graduates (2007–2025, 19 complete years):** from 107,018 annual graduation records in 2007 to 307,988 in 2025, which makes it possible to verify actual degree completion for cohorts with a sufficient observation horizon.
- **PAES/PDT University Admission Tests (2021–2026, 6 annual cycles):** legacy DEMRE files for 2014–2020 carry a contractual clause that forbids individual-level cross-linkage without explicit written authorization from DEMRE; in strict compliance with that restriction, **I did not use any DEMRE 2014–2020 file**. Instead, I used exclusively the registration, score, application, and centralized enrollment microdata for the **2021 to 2026** admission cycles published directly by MINEDUC's Open Data portal under an **open CC-BY license**, which explicitly authorizes verifiable scientific reuse.

<aside class="notice--info" markdown="1">
**Methodological note — Why I audited the code on real data and why I compare against clean open schools:** Connecting these real administrative rosters to the computer module prepared at the close of part III uncovered **three technical lessons** worth sharing because they illustrate why data science should never trust code tested only on simulations:

1. **A database table-binding bug:** an internal subquery omitted the origin-school key when filtering receiving schools, causing execution to halt the moment real data arrived.
2. **A computational bottleneck:** the legacy query grouped roughly 35 million student-year records in candidate grades before filtering relevant schools and parsed twenty compressed CSV files line by line. Converting the SIES and PAES sources into a fast columnar storage format (Apache Parquet) cut total execution time from hours to **under 25 seconds**.
3. **Why future closing schools provide no supported exact-match comparison:** Among 2016–2019 closures, **19 regular secondary schools** were eligible; **12 other secondary schools** closed in 2021–2025 as potential future controls. The exact DiD estimate retains **12 treated secondary-school clusters** with support and follow-up; these are not the 12 future controls, and I do not assign an unverified reason to each excluded eligible school. Requiring exact matches on **8 dimensions** (year, grade, sex, age, region, governance, rurality, and vocational track), at least two schools and five pupils in each of four arms leaves **0 comparable cells** (0% retention; without matching, the comparison gives +4.37 pp, with the opposite sign). Matching instead against **clean schools that remained open** in those same cells, while excluding receiving schools and directly affected local markets, yields **188 exact cells and 2,223 treated secondary pupils** (273 cells and 2,953 treated in the broader check) and **123 cells with 935 treated upper-elementary pupils**. This supports the stated comparison; it does not guarantee exchangeability on unobserved characteristics.
</aside>


## Cohort comparisons and models

### Separating prior student and school histories in the closure comparison

I now turn to the core empirical question. For every student enrolled between **seventh and eleventh grade** in the year before their school closed ($$G-1$$), I computed their **expected higher-education entry year ($$t_0$$)** by adding the years remaining to graduate from twelfth grade on time (for instance, a student in 11th Grade, 3.º Medio, in 2017 whose school closed at the end of that year was expected to complete 12th Grade in 2018 and enter higher education in $$t_0$$ = 2019, or at latest in $$t_0 + 1$$ = 2020). Measuring the **two-year entry window ($$t_0$$ or $$t_0 + 1$$)** is essential in Chile, where many young people work for a year, retake the admission exam, or defer enrollment by twelve months without abandoning higher education.

In exact cells for the primary **2016–2019** closure window, secondary pupils (1.º a 3.º Medio) from closing schools entered higher education at **50.61%**, versus **65.24%** in comparable open schools: a raw gap of **−14.64 percentage points**. A separate DML sample adjusted only for demographics and school structure gives **−13.24 pp**. These estimates use different denominators and cannot be combined as one sample.

Before attributing either gap to closure, two prior histories need examination:

1. **What were pupils’ grades and attendance before their high school closed?** Individual academic history at $$G-1$$ and $$G-2$$ includes grade-point average (used in NEM), attendance, prior repetitions, and whether pupils had remained at the school since $$G-2$$ or entered in $$G-1$$.
2. **How did an earlier cohort from the same high school fare?** The $$G-5$$ cohort attended four years before the exposed cohort, while the school was still open. Its higher-education entry rate measures a prior school-level disadvantage. A gap already present then cannot be attributed to a later closure, although it does not by itself identify the closure effect.

<aside class="notice--info" markdown="1">
**Two complementary adjustments, each with its own assumptions.** I compare cohorts from the same school and adjust individual characteristics with Double Machine Learning. Agreement between these approaches does not guarantee identification: both can share bias from omitted variables or insufficient comparability:

- **Repeated-cohort difference-in-differences ($$G-1$$ vs. $$G-5$$ within exact cells):** A pupil cannot first enter higher education twice. I therefore compare the cohort exposed to closure at $$G-1$$ with a cohort from the **same high school** at $$G-5$$ that attended four years earlier and, in secondary grades, graduated before closure. I subtract the analogous cohort change in controls matched on region, rurality, governance, grade, sex, and age. A fixed historical disadvantage of the closing school would cancel by subtraction. The contrast assumes that, without closure, the difference between $$G-5$$ and $$G-1$$ cohorts would have been the same in closing and control schools. Closing schools were already shrinking (part I), so that assumption may fail; one prior period cannot test it here. The Table A1 sensitivity check concerns school outcomes from part III, not higher education.
- **Double/Debiased Machine Learning with school-grouped cross-fitting:** I also adjust flexibly for nonlinear differences in prior grades, attendance, age-for-grade, and mobility using Double/Debiased Machine Learning (Chernozhukov et al. 2018[^chernozhukov2018]; Chernozhukov et al. 2024[^chernozhukov2024]). Boosted trees (HGB) and an interpretable additive model (EBM) predict higher-education entry from observed pre-closure student and school characteristics; a second model predicts attendance at a closing school from those characteristics. I then compare residual variation not predicted by those covariates. With **5-fold cross-fitting grouped by school**, models train on 80% of schools and predict for the held-out 20%. This reduces within-school memorisation but cannot remove unobserved confounding.
</aside>


Figure 1 in the main article and Table A2 in this annex show how estimates change as prior student and school histories enter the comparison. The steps use distinct samples and assumptions; none alone identifies a closure effect:

{: .table-caption}
<span id="tabla-post4-a2"></span>
**Table A2.** Ladder of adjusted comparisons for 2-year higher-education entry (2016–2019 closures; DML model with *N* = 62,153 students with complete $$G-5$$ history: 38,525 in Secondary and 23,628 in Upper Elementary; rung 3a: exact DiD with 2,223 treated across 188 cells in Secondary and 935 across 123 cells in Upper Elementary)

| Level at closure ($$G-1$$) | Identification ladder rung | Primary estimator | 2-year HE entry effect (pp) | Clustered standard error (pp) | 95% confidence interval (pp) | What this rung purges and how to interpret it |
|---|---|---|---:|---:|---|---|
| Secondary (1.º a 3.º Medio, *N* = 38,525) | 1. $$G-1$$ gap with demographic and territorial controls only | DML PLR (HGB) | −13.24 | 2.94 | [−19.00; −7.48] | Compares students in the same grade, region, governance, rurality, and vocational track, but mixes closure with prior fragility. |
| Secondary (1.º a 3.º Medio) | 2. + Prior individual academic history ($$G-1$$ and $$G-2$$) | DML PLR (HGB) | −5.63 | 2.12 | [−9.78; −1.47] | Adjusts for GPA (NEM), prior attendance, grade repetitions, and $$G-2$$ stability: the estimate falls by 57.5% (−7.61 of −13.24 pp) after adding prior individual history; this is not an isolated causal share. |
| Secondary (1.º a 3.º Medio) | 3a. Repeated-cohort difference-in-differences ($$G-1$$ vs. $$G-5$$) | Exact DiD + *Wild Bootstrap* | −2.64 | 2.22 | [−7.54; +2.25] | Subtracts the gap that the same high school already exhibited four years before the exposed cohort ($$G-5$$: −12.00 pp; 12 clusters). **82.0% of the raw cell gap (−12.00 of −14.64 pp) already existed in $$G-5$$**. |
| Secondary (1.º a 3.º Medio) | 3b. Full model: student history ($$G-1$$/$$G-2$$) + school history ($$G-5$$) | DML PLR (HGB / EBM) | −0.29 | 1.20 | [−2.64; +2.06] | In additive EBM: −0.91 pp (SE 1.03); in Hájek doubly robust: +0.19 pp (SE 1.34). The estimated average is near zero; its interval does not establish equality. |
| Secondary (1.º a 3.º Medio) | 3c. Full model disaggregated for vocational-technical higher education (IP/CFT) | R-Learner, BLP $$\beta_1$$ on the full-DML residuals | −2.09 | 0.72 | [−3.50; −0.68] | Unlike university entry (+1.98 pp, [−0.22; +4.19]), **the conditional estimate for IP/CFT is −2.09 pp (*p* = 0.0037)**. The two channels sum to roughly the −0.29 pp overall-entry effect, so substitution toward universities remains an open question (third spoonful). |
| Upper Elementary (7.º a 8.º Básico, *N* = 23,628) | 1. $$G-1$$ gap with demographic and territorial controls only | DML PLR (HGB) | −4.06 | 1.73 | [−7.44; −0.67] | Moderate initial gap when closure takes place four or five years before high-school graduation. |
| Upper Elementary (7.º a 8.º Básico) | 2. + Student prior academic history ($$G-1$$ and $$G-2$$) | DML PLR (HGB) | −1.51 | 1.67 | [−4.78; +1.76] | Accounting for seventh- or eighth-grade GPA and attendance suffices to render the gap statistically indistinguishable from zero. |
| Upper Elementary (7.º a 8.º Básico) | 3a. Repeated-cohort difference-in-differences ($$G-1$$ vs. $$G-5$$) | Exact DiD + *Wild Bootstrap* | +1.21 | 2.06 | [−3.39; +5.81] | The estimate relies on 11 clusters; its interval includes both plausible losses and gains. |
| Upper Elementary (7.º a 8.º Básico) | 3b. Full model: student history ($$G-1$$/$$G-2$$) + school history ($$G-5$$) | DML PLR (HGB / EBM) | +1.02 | 1.76 | [−2.44; +4.47] | In additive EBM: +0.86 pp (SE 1.81); in Hájek doubly robust: +1.32 pp (SE 1.74). No average fall is detected under this adjustment; the interval includes negative and positive values. |
{: .table--compact .table--scroll}

Table A2 shows why the comparison population matters. The raw exact-cell gap and the modelled steps use different samples; their estimates cannot be added or treated as a single decomposition. Adding pupil history changes the modelled estimate from −13.24 to −5.63 points, a 57.5% reduction within that model. The earlier cohort's −12.00-point gap is 82.0% of the −14.64-point raw gap within the same exact cells. Pupil and school histories overlap, so neither percentage is a separately identified causal share. Combining both histories yields −0.29 points for total entry, with an interval spanning zero; alternative models yield −0.91 and +0.19. The IP/CFT estimate of −2.09 comes from a separate channel outcome under the full residual adjustment. Its interpretation remains conditional on the design, support, and unmeasured factors.

Do the estimates differ for secondary pupils who had attended the school since two years before closure and those who entered only in its final year? I also tested this with the full Double ML model. Among stable pupils from $$G-2$$ (**29,683 pupils, 1,974 treated**), the initial **−13.23-point** gap becomes **−1.50 points** (school-clustered SE **1.59**) after adjusting individual and school histories. Among late entrants in $$G-1$$ (**8,842 pupils, 1,264 treated**), the initial **−7.70-point** gap becomes **+1.50 points** (SE **2.02**). Both adjusted total-entry estimates are near zero, but their standard errors do not establish equality. These supported subgroups are distinct from the descriptive school-outcome population in part III.

### Fourteen years of history (2009–2022): Pre-Tuition-Free, Tuition-Free/Inclusion, and Pandemic regimes

Did the same pattern hold fifteen years ago, before Chile introduced tuition-free higher education (*Gratuidad*, launched in 2016 for universities and subsequently expanded to eligible non-profit CFTs and IPs) or during the COVID-19 pandemic? Because the individual SIES rosters span 2007 through 2026, I can estimate the exact repeated-cohort design ($$G-1$$ vs. $$G-5$$) across **14 annual cohorts of school closures between 2009 and 2022**, grouped into three institutional policy regimes (regimes are defined by the closure year; the higher-education entry years of each group extend into the following regime):

<figure class="post3-figure data-visualization" id="fig-post4-2">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" width="1600" height="850" src="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post4/longitudinal-regimes-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post4/longitudinal-regimes-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post4/longitudinal-regimes-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post4/longitudinal-regimes-en-dark.svg' | relative_url }} 1600w" alt="Two-panel chart on 14 years of school closures and higher education between 2009 and 2022. Panel A shows regime-specific secondary DiD point estimates, not confirmed changes between regimes: in 2009–2015 (Pre-Tuition-Free) the effect is plus 0.55 percentage points; in 2016–2019 (Tuition-Free and Inclusion) it is minus 2.64 points, with an IP/CFT point estimate of minus 2.59 points (12 treated school clusters; p = 0.28) while university stands at minus 0.34; in 2020–2022 (Pandemic) it is minus 3.79 points, with IP/CFT and two-year persistence point estimates of minus 4.33 and minus 4.72 points, each imprecise. Panel B compares higher-education entry rates across screened D2 closures (50.6%), clean controls (65.2%), and excluded block transfers D1 minus D2 (71.6% in secondary and 81.1% in elementary)." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure A1</strong> — 14-year longitudinal series (2009–2022): difference-in-differences effects by policy regime on overall, university, vocational-technical (IP/CFT), and persistent enrollment (panel A), and a composition comparison between screened D2 episodes and excluded block transfers (D1 \ D2, panel B); the figure does not verify the legal status of any individual episode. <span class="figure-source">Source: author's calculations from MINEDUC–SIES panel 2007–2026.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post4/longitudinal-regimes-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>.</span></figcaption>
</figure>

{: .table-caption}
<span id="tabla-post4-a3"></span>
**Table A3.** Longitudinal 2009–2022 series of higher-education effects by policy regime and exposure level (clean closure rule D2)

| Public policy regime | Level in $$G-1$$ | Exposed in $$G-1$$ (N) | Raw gap in $$G-1$$ (pp) | Prior gap in $$G-5$$ (pp) | DiD 2-yr HE entry (pp) | DiD 2-yr University (pp) | DiD 2-yr IP/CFT (pp) | DiD 2-yr Persistence (pp) | DiD Graduation by 2025 (pp; censored if t0 ≥ 2019) |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 2009–2015 (Pre-Gratuidad / LGE-SAC) | Secondary | 10,934 | −14.79 | −15.35 | +0.55 (SE 1.29) | +0.35 | +0.22 | +0.08 | +0.28 |
| 2009–2015 (Pre-Gratuidad / LGE-SAC) | Upper Elementary | 7,061 | −9.13 | −7.67 | −1.47 (SE 0.86) | −1.15 | −0.37 | −1.50 | +0.17 |
| 2016–2019 (Gratuidad & Inclusion) | Secondary | 2,223 | −14.64 | −12.00 | −2.64 (SE 2.22) | −0.34 | −2.59 | −1.72 | +4.43† |
| 2016–2019 (Gratuidad & Inclusion) | Upper Elementary | 935 | −2.38 | −3.59 | +1.21 (SE 2.06) | +2.43 | −0.45 | +1.92 | +1.84† |
| 2020–2022 (COVID-19 Pandemic) | Secondary | 678 | −5.62 | −1.83 | −3.79 (SE 1.81) | −0.24 | −4.33 | −4.72 | −0.04† |
| 2020–2022 (COVID-19 Pandemic) | Upper Elementary (4 clusters; descriptive) | 156 | −1.56 | −3.69 | +2.13 (SE 6.22) | +7.09 | −5.17 | −3.11 | −3.92† |
| **Cumulative series 2009–2022 (clean D2)** | **Secondary** | **13,835** | **−14.32** | **−14.15** | **−0.17 (SE 1.10)** | **+0.21** | **−0.46** | **−0.44** | **—** |
| **Excluded D1 \ D2 (block transfers ≥ 70%)** | **Secondary** | **2,282** | **+4.06** | **+6.64** | **−2.58** | — | — | — | — |
| **Excluded D1 \ D2 (block transfers ≥ 70%)** | **Upper Elementary** | **1,434** | **+7.28** | **+7.06** | **+0.22** | — | — | — | — |
{: .table--compact .table--scroll}

*Note:* LGE = General Education Law (2009); SAC = Quality Assurance System (2011). Treated clusters by row: 39 and 77 in 2009–2015; 12 and 11 in 2016–2019; 7 and 4 in 2020–2022; 58 in the cumulative series. † Right-censored: not interpreted.

Figure A1 and Table A3 support three descriptive observations:

1. **Among 2009–2015 closures (10,934 exposed secondary pupils), the prior gap exceeded the later observed gap:** four years before the exposed cohort ($$G-5$$), those high schools were already −15.35 pp below their controls, compared with a later gap of −14.79 pp. The difference-in-differences estimate for entry was **+0.55 pp** (−2.07 to +3.18 pp). Cumulative graduation by 2025 likewise shows no difference distinguishable from zero (+0.28 pp in secondary and +0.17 pp in upper elementary).
2. **From 2016 onward, the IP/CFT point estimate turns negative, but each regime-specific test against zero is imprecise:** the DiD estimate for IP/CFT entry moves from +0.22 pp in 2009–2015 closures to −2.59 pp in 2016–2019 (SE 2.29; *p* = 0.28; 12 clusters) and −4.33 pp in 2020–2022 (SE 2.88; *p* = 0.18; 7 clusters). University entry stays near zero (−0.34 and −0.24 pp), while second-year persistence is estimated at −4.72 pp in the pandemic (SE 2.60; *p* = 0.12). The series is compatible with erosion of the vocational-technical channel, but 7 to 12 treated high schools per regime do not distinguish these individual estimates from zero or establish differences between regimes. A hypothesis to test is that losing in-person guidance networks matters more for pupils headed to an IP or CFT.
3. **A composition check compatible with the clean-closure rule (panel B of Figure A1):** The student-flow rule (D2) from parts II and III sets aside possible administrative continuities (D1 \ D2) when a school code disappears but **70% or more of its pupils move together** to one receiving school. These may include mergers, code changes, or whole-campus moves; the flow alone does not verify which occurred. Among the **2,282 secondary** and **1,434 upper-elementary** pupils excluded by this rule, higher-education entry was **71.60%** in secondary (**+4.06 pp** against controls) and **81.10%** in upper elementary (**+7.28 pp**). This concentrated flow is compatible with administrative reorganisations among high-performing schools, pending documentary confirmation. A directory-only definition (D1) would mix these episodes with D2 closures, where the secondary entry rate was **50.61%**, and change the composition of the estimates; it does not establish the direction or size of causal bias.


## Heterogeneity and admissions

### Estimating heterogeneity with the Orthogonal R-Learner (BLP, GATE, and CLAN)

A near-zero estimated average for total entry can coexist with differences by pathway or pupil profile. I test whether the predicted ranking persists outside the schools used to train it and whether it survives adjustment for the school's prior history.

<aside class="notice--info" markdown="1">
**Orthogonal R-Learner, BLP, GATE, and CLAN.** To examine differences between profiles without searching arbitrary subgroups, I use the Orthogonal R-Learner[^niewager2021][^wager2024], informed by generalized random forests[^athey2019], with BLP, GATE, and CLAN summaries[^cddf2018][^chernozhukov2024]. That inference framework was developed for experiments with known propensities; here propensities are estimated by cross-validation. Separating training from validation helps, but the analysis still depends on overlap and no residual confounding.

1. **Predicted conditional effect (CATE).** A second regularised model learns variation by pupil characteristics in G−1 and G−2, using five folds grouped by school. I exclude school size and identifiers from the moderators to reduce memorisation of closed schools; this cannot remove unobserved confounding.
2. **BLP ranking test.** A weighted regression with school-clustered errors estimates an average coefficient ($$\beta_1$$) and a heterogeneity slope ($$\beta_2$$). A slope compatible with zero does not support ranking profiles. A positive slope with *p* < 0.05 supports ranking under this design and its assumptions; it does not validate an effect for each pupil.
3. **GATE and CLAN.** I sort pupils into equal-sized quintiles of the predicted conditional effect, from G1 at the lower end to G5 at the higher end. GATE estimates an average contrast within each quintile; CLAN compares the observed characteristics of G1 and G5. The model redefines those quintiles when its controls change.
</aside>

<figure class="post3-figure data-visualization" id="fig-post4-3">
  <a class="image-popup post3-theme-link" href="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light.svg' | relative_url }}" data-light-href="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light.svg' | relative_url }}" data-dark-href="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-dark.svg' | relative_url }}">
    <picture class="post3-theme-picture">
      <source class="post3-theme-source" media="(max-width: 47.99em)" srcset="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light-mobile.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light-mobile.svg' | relative_url }}" data-dark-srcset="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-dark-mobile.svg' | relative_url }}">
      <img class="post3-theme-image" width="1600" height="850" src="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light.svg' | relative_url }}" srcset="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light.svg' | relative_url }} 1600w" sizes="(max-width: 47.99em) 100vw, 1000px" data-light-src="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light.svg' | relative_url }}" data-dark-src="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-dark.svg' | relative_url }}" data-light-srcset="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-light.svg' | relative_url }} 1600w" data-dark-srcset="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-dark-mobile.svg' | relative_url }} 768w, {{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-en-dark.svg' | relative_url }} 1600w" alt="Two panels. A: quintiles of the predicted conditional effect with student controls; G1, the quintile with the lowest predicted effect, records −12.26 points for total entry. Adding G−5 school history re-estimates the quintiles: the new G1 has different composition and records −0.26; this is not follow-up of a fixed group and is not plotted. B: raw gaps and adjusted estimates for PAES/PDT test-taking, applications, enrolment, and selectivity in 2021–2026; adjusted estimates establish neither equality nor a mechanism." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure A2</strong> — Quintiles of predicted conditional effects with student controls (panel A), and observed PAES/PDT admissions stages in 2021–2026 (panel B). Panel A shows −12.26 points in G1 under student controls. With G−5 school history, a re-estimated G1 records −0.26 points, a result not shown in the panel. The quintiles are not fixed groups. <span class="figure-source">Source: my calculations from the MINEDUC–SIES–PAES linkage, 2004–2026.</span> <span class="figure-data"><a href="{{ '/assets/images/tesis-post4/causal-ml-heterogeneity-paes-data.csv' | relative_url }}">Accessible tabular data (CSV)</a>; <a href="{{ '/assets/data/tesis-post4/post4_higher_education_causal_ml_v1.json' | relative_url }}">full results with school history (JSON)</a>.</span></figcaption>
</figure>

Figure A2 and Table A4 distinguish two specifications that should not be conflated:

{: .table-caption}
<span id="tabla-post4-a4"></span>
**Table A4.** Estimated heterogeneity associated with school closure via Orthogonal R-Learner (BLP test, GATE quintiles, and CLAN profile, *N* = 62,153)

| Specification and postsecondary outcome | BLP heterogeneity slope ($$\hat{\beta}_2$$) | *p*-value ($$\hat{\beta}_2$$) | GATE G1 (lowest predicted effect, pp) | GATE G3 (middle quintile, pp) | GATE G5 (highest predicted effect, pp) | Who sits in the critical G1 quintile versus G5 (CLAN) |
|---|---:|---:|---:|---:|---:|---|
| Student controls: **2-year HE entry** | +0.634 (SE 0.282) | **0.0243** | **−12.26** [−17.79; −6.74] | −3.31 | −3.03 [−5.92; −0.14] | G1 has 99.5% secondary students (vs. 13.8% in G5), 77.2% in vocational track (vs. 0.3%), and lower attendance (87.1% vs. 93.1%). |
| Student controls: **2-year IP/CFT entry** | +0.800 (SE 0.237) | **0.0007** | **−8.02** [−12.42; −3.63] | +1.54 | +0.73 [−1.71; +3.18] | G1 concentrates vocational-technical secondary students (77.2%), higher post-closure grade lag (11.5% vs. 4.8%), and lower attendance. |
| Student controls: **2-year persistence** | +0.580 (SE 0.258) | **0.0247** | **−11.48** [−17.87; −5.10] | −5.09 | −5.49 [−9.06; −1.92] | The G1 estimate here uses individual-history controls; it must be reconsidered with full school history. |
| Student controls: **2-year University entry** | −0.530 (SE 0.431) | 0.2191 | +0.21 [−4.40; +4.82] | −6.96 | −4.10 [−8.45; +0.24] | No statistically significant systematic heterogeneity is detected in the university channel (*p* = 0.2191). |
| Full controls (+ $$G-5$$ school history): **2-year IP/CFT entry** | +0.425 (SE 0.179) | **0.0177** | **−2.57** [−5.68; +0.54] | −3.92 | −0.93 [−2.86; +0.99] | The BLP slope has nominal *p* = 0.0177 without a documented multiplicity adjustment; G2 and G3 point estimates are −2.94 and −3.92 pp, respectively. |
{: .table--compact .table--scroll}

Table A4 supports two levels of reading. With individual-history controls at $$G-1$$ and $$G-2$$, the BLP ranking test supports heterogeneity under this design in total higher-education entry ($$\hat{\beta}_2$$ = +0.634, *p* = 0.0243), second-year persistence ($$\hat{\beta}_2$$ = +0.580, *p* = 0.0247), and IP/CFT entry ($$\hat{\beta}_2$$ = +0.800, *p* = 0.0007). Once I also account for the origin school's $$G-5$$ entry rate, total-entry heterogeneity is no longer distinguishable from zero: a newly ranked G1 has an estimate of −0.26 pp. This is compatible with earlier school disadvantage contributing to the first signal; it does not identify how any fixed pupils changed. For IP/CFT, the full model still estimates a mean difference of −2.09 pp (*p* = 0.0037) and a heterogeneity slope of +0.425 (*p* = 0.0177), with group estimates of −2.57 pp in G1, −2.94 pp in G2, and −3.92 pp in G3. The ordering is not monotone: G1's interval includes zero, while G3 has the largest point decline.

Who belongs to the 20% of pupils with the lowest predicted conditional effect (G1) under student-only controls? CLAN describes their observed characteristics: **99.49%** attended **secondary school** at closure (versus 13.75% in G5, where upper-elementary pupils predominate); **77.17%** were in the **vocational-technical track** (versus 0.28%). Their prior $$G-1$$ marks averaged 5.33 versus 5.63, and attendance was **87.13%** versus **93.07%**. Their schools’ $$G-5$$ cohort entered higher education at 57.17% versus 66.63%, and immediate post-closure lag or exit was **8.98%** versus **6.21%**. G1 also had fewer prior repetitions (1.71% versus 15.09%) and more pupils stable since $$G-2$$ (77.12% versus 64.87%). This is a group profile, not proof that each pupil was harmed.

Adding $$G-5$$ school history forms new quintiles. In the newly ranked G1, **91.24%** attended secondary school (versus **37.07%** in the new G5) and **51.79%** were on the vocational track (versus **2.74%**). Prior marks averaged **5.79** versus **5.20**, and attendance **85.04%** versus **93.35%**. The shares stable since $$G-2$$ were **85.34%** versus **58.89%**, while prior grade repetition was **1.87%** versus **12.33%**. The schools' historical higher-education entry rates were **63.25%** versus **64.93%**, and later school lag or exit from the register was **6.31%** versus **12.09%**. This CLAN profile describes a different composition. The public JSON contains no transition matrix linking G1 membership across specifications, so I cannot read the change in estimates as an improvement for the same people.

The public JSON reports nominal *p*-values across several outcomes and specifications without documenting a multiplicity adjustment. I treat the heterogeneity tests as exploratory signals requiring independent confirmation.

### What happens with the PAES/PDT admission test and entry into the most selective programs?

One piece of the puzzle remains: does school closure affect the probability of sitting for the national admission exam (PDT in 2021–2022 and PAES since 2023), submitting a centralized application, enrolling through that system, or entering the **top 20% most selective degree programs in the country**?

<aside class="notice--info" markdown="1">
**Programme selectivity adjusted with Empirical Bayes.** Small programmes can look unusually selective because of a few high scores in one year. Using official PAES/PDT enrolment microdata for 2021–2026, I combine each programme-year's mean admission score with the system-wide mean, weighting that adjustment by the number enrolled. The resulting index reduces small-sample noise before classifying entrants to the top 20% of programmes by adjusted selectivity. This is a descriptive ranking of programmes, not a causal effect of school closure.
</aside>

{: .table-caption}
<span id="tabla-post4-a5"></span>
**Table A5.** Centralized PAES/PDT admission and Empirical Bayes selectivity (2016–2019 closures in cohorts with expected entry $$t_0$$ in 2021–2025, *N* = 29,218 students across 2,079 schools)

| Outcome in the centralized admission system (2021–2026) | Exposed mean (%) | Control mean (%) | Raw gap (pp) | DML with student history $$G-1$$/$$G-2$$ (pp) | Full DML with $$G-5$$ school history (pp) | Substantive reading of the selective university channel |
|---|---:|---:|---:|---:|---:|---|
| 1. Sits for admission test (PAES or PDT) in $$t_0$$ or $$t_0 + 1$$ | 61.27% | 72.25% | −10.98 | −3.09 (SE 2.73) [−8.44; +2.25] | +0.75 (SE 1.73) [−2.65; +4.15] | The 11-point raw gap in test-taking ceases to be distinguishable from zero once student and school prior trajectories are controlled for. |
| 2. Applies through the centralized admission system | 41.63% | 48.38% | −6.75 | −0.15 (SE 2.67) [−5.39; +5.09] | +4.30 (SE 1.66) [+1.05; +7.55] | Holding academic history and depressed $$G-5$$ school history constant, the point estimate turns positive, possibly reflecting over-adjustment against a very low historical baseline. |
| 3. Enrolls via centralized PAES/PDT admission | 33.28% | 40.74% | −7.46 | −1.44 (SE 2.63) [−6.60; +3.72] | +2.87 (SE 1.68) [−0.43; +6.17] | No fall distinguishable from zero is detected in centralised enrolment under this adjustment; its interval permits losses and gains. |
| 4. Enrolls in a top 20% selectivity program (Empirical Bayes) | 12.14% | 14.68% | −2.54 | −0.62 (SE 1.52) [−3.60; +2.36] | +1.75 (SE 1.46) [−1.12; +4.62] | The adjusted estimate is not distinguishable from zero; its interval still permits losses and gains. |
{: .table--compact .table--scroll}

Table A5 separates test-taking, application, centralised enrolment, and entry into selective programmes. In its full sample, adjusted estimates for test-taking and top-20% selectivity do not show a decline distinguishable from zero. Under the full model, the +1.75-point selectivity estimate includes zero; the +4.30-point application estimate is positive but has no established explanation. It could reflect over-adjustment against a low historical baseline, so I treat it as an anomaly to investigate rather than resilience caused by closure. These outcomes do not establish a pathway mechanism.

The full-model IP/CFT estimate is −2.09 points while university entry is estimated at +1.98, with an interval that includes zero. Aggregate arithmetic cannot show whether the same pupils substituted university for IP/CFT or lost higher-education access altogether. Testing mutually exclusive individual paths to IP/CFT, university, both over time, or neither remains open (challenge 1 in the main article). Guidance, placement agreements, and vocational continuity are possible mechanisms, but these records do not measure them directly.

## Specifications, sensitivity, and sources

<span id="cohortes-y-horizonte"></span>
### 1. Cohort definition, postsecondary horizon, and the clean closure rule (RCID v1)

The analytical universe starts from school closure episodes identified between **2005 and 2024** across MINEDUC's longitudinal panel (2004–2025, 79,709,054 enrollment records and 73,873,835 performance records). Following the hierarchy established in part III ($$D_0 \supset D_1 \supset D_2$$), I distinguish:

- **$$D_0$$ (1,981 raw exits 2005–2025):** any school with positive enrollment in $$t-1$$ that records zero enrollment from $$t$$ onward and does not reopen.
- **$$D_1$$ (1,807 strict directory closures):** purges annexes, secondary campuses, and direct administrative code (RBD) continuities.
- **$$D_2$$ or RCID v1 (1,678 closures in the conservative version and 1,648 clean closures with observed $$t+1$$ window):** further purges **concentrated student-flow absorptions** (schools with at least 10 students where a single receiving school absorbs 70% or more of the displaced cohort with concentration index HHI of at least 0.50 and the same modal destination in $$t$$ and $$t+1$$). In terms of the Rubin Causal Model (Imbens and Rubin 2015[^imbensrubin2015]), this filtering mitigates both sources of violation of the stable unit treatment value assumption (SUTVA): (i) *hidden versions of treatment* (separating genuine closures from block campus relocations $$D_1 \setminus D_2$$) and (ii) *interference* in the control group (excluding receiving schools and local municipality-level markets directly exposed to closure).

To evaluate trajectories into higher education across the full theory-of-change causal chain (Gertler et al. 2017[^gertler2017]), I focus on students enrolled in the year prior to closure ($$G-1$$) in **upper elementary (7.º or 8.º Básico, teaching code 110)** or **regular secondary education (1.º a 3.º Medio, academic code 310, vocational-technical codes 410–810, and artistic code 910)**, and exclude cells whose expected entry year $$t_0$$ falls outside 2007–2025 (so that $$t_0 + 1$$ is contained within 2007–2026). Let $$g_i$$ (from 7 to 11) denote the ordinal grade attended by student $$i$$ in year $$G - 1$$. Their **expected on-time twelfth-grade graduation year** is $$(G - 1) + (12 - g_i)$$, and their **expected on-time higher-education entry year ($$t_0$$)** is defined by:

$$
t_0(i) = G + (12 - g_i)
$$

For example, for a student in 3.º Medio ($$g_i$$ = 11) in $$G - 1$$, their expected entry year is $$t_0 = G + 1$$; for a student in 7.º Básico ($$g_i$$ = 7) in $$G - 1$$, it is $$t_0 = G + 5$$. On this individual clock aligned by origin grade, I define six postsecondary outcomes in the SIES individual rosters (2007–2026): (1) **on-time entry in $$t_0$$**; (2) **two-year window entry ($$t_0$$ or $$t_0 + 1$$)**, the primary outcome because it captures students who defer enrollment by one year; (3) **university entry in $$t_0$$ or $$t_0 + 1$$**; (4) **entry into a Professional Institute (IP) or Technical Training Center (CFT) in $$t_0$$ or $$t_0 + 1$$**; (5) **two-year consecutive persistence** (being enrolled in higher education both in the initial entry year and in the immediately following year); and (6) **cumulative graduation through 2025** in the official SIES Graduation rosters (2007–2025), right-censored when $$t_0 \ge 2019$$.

### 2. Repeated-cohort econometric specification ($$G-1$$ vs. $$G-5$$) and cluster-robust inference

In the repeated-cohort difference-in-differences design within exact cells, each cell $$c$$ is defined by the exact combination of: closure episode year $$G$$, origin level and grade $$g_i$$, academic versus vocational-technical track, school region, governance type, and rurality. Following the principle of never conditioning on post-treatment *bad controls* (Angrist and Pischke 2009[^angristpischke2009]; Huntington-Klein 2025[^huntingtonklein2025]), all controls are fixed strictly at $$G-1$$, $$G-2$$, and $$G-5$$, excluding intermediate post-closure variables ($$G$$ or $$G+1$$) that would block part of the causal channel. Within each cell $$c$$, I observe four arms: students from the closing school in the exposed cohort ($$G-1$$, post-treated arm) and in an earlier cohort from the **same school** four years before the exposed cohort ($$G-5$$, pre-treated arm: in secondary school it graduates in $$G-2$$ if enrolled in 1.º Medio, in $$G-3$$ if in 2.º Medio, and in $$G-4$$ if in 3.º Medio; in upper elementary, the $$G-5$$ cohort of 8.º Básico attends 4.º Medio in $$G-1$$ and that of 7.º Básico only reaches 3.º Medio in $$G-1$$), compared against the $$G-1$$ and $$G-5$$ cohorts of clean never-treated schools (excluding receiving schools and local municipality-level markets directly exposed to closure). The estimator weighted by the number of exposed students in $$G-1$$ ($$N_{1\text{post}(c)}$$) is:

$$
\hat{\Delta}_{\text{DiD}} = \sum_{c} w_c \left[ \left(\bar{Y}_{\text{trat}(G-1)c} - \bar{Y}_{\text{trat}(G-5)c}\right) - \left(\bar{Y}_{\text{ctrl}(G-1)c} - \bar{Y}_{\text{ctrl}(G-5)c}\right) \right]
$$

with weights $$w_c = N_{1\text{post}(c)} / \sum_{k} N_{1\text{post}(k)}$$. Variance is estimated by clustering at the origin school/episode level. Because the 2016–2019 design rests on 12 treated clusters in secondary and 11 in upper elementary (7 and 4 in pandemic closures), I complement analytical inference with a six-point Webb *wild cluster bootstrap* (MacKinnon and Webb 2017[^mackinnonwebb2017]; Cameron, Gelbach, and Miller 2008[^cameron2008]) and a Student $$t$$ distribution with degrees of freedom equal to the number of treated clusters minus one (Angrist and Pischke 2009[^angristpischke2009]; that number is not the closure year $$G$$ of the school clock), reporting the more conservative interval. The pandemic upper-elementary row (4 clusters) is purely descriptive. One caveat specific to upper elementary: in schools offering both elementary and secondary grades, the $$G-5$$ cohort of 7.º Básico was attending 3.º Medio in the school's final year, so it is not a pure pre-treated arm; if closure also affected it, the upper-elementary DiD could attenuate a decline toward zero. I therefore read its +1.21 pp as inconclusive, neither a demonstrated benefit nor evidence of no harm. In the retrospective evaluation of non-parallel trends inspired by Rambachan and Roth (2023[^rambachan2023]) on part III (table A1), alongside the ratios relative to the prior 95% bound (2.54 times) and the prior point drift (5.21 times), if the post-closure slope change is instead bounded by the largest pre-closure slope change (0.15 pp per year), the interval withstands up to 14.24 times that change; these thresholds are a simplified single-post-period version rather than the output of the formal procedure.

<span id="especificaciones-causal-ml"></span>
### 3. Causal Machine Learning specification (DML PLR, Hájek DR-ATT, and Orthogonal R-Learner)

To adjust flexibly for both prior individual academic history ($$X_{\text{acad}}$$: grade-point average in $$G-1$$ and $$G-2$$, attendance rate in $$G-1$$ and $$G-2$$, prior grade repetitions, and $$G-2$$ stayer indicator) and school history ($$X_{\text{school}}$$: overall, university, and vocational-technical entry rates of the $$G-5$$ cohort from the same school), I estimate two complementary **Double/Debiased Machine Learning** models (Chernozhukov et al. 2018[^chernozhukov2018]; Chernozhukov et al. 2024[^chernozhukov2024]; Ding 2024[^ding2024]) using **5-fold cross-fitting grouped by origin school**:

1. **Robinson Partially Linear Model (DML PLR):** For each of the five folds $$k$$ (from 1 to 5), I train on the remaining four folds an outcome predictor $$\hat{g}_{-k}(X_i)$$ via histogram-boosted trees (*HistGradientBoostingRegressor*) and, in parallel, an interpretable generalized additive model (*ExplainableBoostingRegressor*, EBM *glassbox*), alongside a regularized propensity model $$\hat{m}_{-k}(X_i)$$ bounded in [0.01; 0.85] (Imbens and Rubin 2015[^imbensrubin2015]; Ding 2024[^ding2024]); clipping does not create overlap, it only limits extreme weights (with a minimum observed propensity of 0.0100 in the steps with student and school controls). Using out-of-fold residuals $$\tilde{u}_i = Y_i - \hat{g}_{-k(i)}(X_i)$$ and $$\tilde{v}_i = D_i - \hat{m}_{-k(i)}(X_i)$$, the Neyman-orthogonal estimator is:

   $$
   \hat{\theta}_{\text{PLR}} = \left(\sum_{i=1}^{N} \tilde{v}_i \tilde{u}_i\right) / \left(\sum_{i=1}^{N} \tilde{v}_i^2\right)
   $$

   with school-clustered standard errors derived from the orthogonal influence function $$\psi_i$$. Under heterogeneous effects, $$\hat{\theta}_{\text{PLR}}$$ is an average of conditional effects weighted by conditional treatment variance given $$X$$, not the average effect on the treated; for that reason I also report the Hájek DR-ATT.
2. **Hájek-normalized Doubly Robust Average Treatment Effect on the Treated (DR-ATT):** Combines the counterfactual outcome predictor trained strictly on controls $$\hat{g}_{0(-k)}(X_i)$$ with renormalized inverse-probability weights (Ding 2024[^ding2024]):

   $$
   w_{c(i)} = \left[(1 - D_i) \hat{m}_{-k}(X_i) / \left(1 - \hat{m}_{-k}(X_i)\right)\right] / \left[\sum_{j=1}^{N} (1 - D_j) \hat{m}_{-k}(X_j) / \left(1 - \hat{m}_{-k}(X_j)\right)\right]
   $$

   This estimator remains consistent if either the outcome model *or* the propensity model is correctly specified.
3. **Heterogeneity via Orthogonal R-Learner and BLP / GATE / CLAN tests:** In the second stage, I estimate the conditional treatment effect function $$\hat{\tau}(Z_i)$$ by minimizing Robinson's weighted squared loss $$\sum_i \tilde{v}_i^2 \left[ (\tilde{u}_i / \tilde{v}_i) - \tau(Z_i) \right]^2$$ with school-clustered cross-fitting over the individual moderator vector $$Z_i$$ (secondary versus elementary level, ordinal grade, vocational-technical track, GPA, attendance, prior repetitions, and $$G-2$$ stayer status). Using out-of-fold predictions $$S_i = \hat{\tau}_{-k(i)}(Z_i)$$, the orthogonal Best Linear Predictor (BLP) calibration regression:

   $$
   \tilde{u}_i = \beta_1 \tilde{v}_i + \beta_2 \tilde{v}_i \left(S_i - \bar{S}\right) + \varepsilon_i
   $$

   delivers the formal heterogeneity test ($$H_0: \beta_2 = 0$$), while projecting onto indicators for the five quintiles of $$S_i$$ yields group average effects (GATE G1 to G5).

<span id="confusion-omitida"></span>
### 4. Formal omitted-variable sensitivity analysis of Cinelli and Hazlett (2020)

What if an unobserved family factor absent from MINEDUC registries—such as household income, parental education, or home support—explained part of the IP/CFT estimate or the differences across pupils? I apply the formal omitted-variable bias sensitivity framework of **Cinelli and Hazlett (2020[^cinellihazlett2020])**, which computes the **Robustness Value ($$\text{RV}$$)**—the percentage of residual variance in both treatment and outcome that an unobserved confounder would need to explain to drive the point estimate to zero—and bounds the maximum bias if an omitted confounder were as strong as observed covariates such as GPA, attendance, or $$G-5$$ school history. Its analytical bounds apply to the linear Frisch–Waugh–Lovell partialling-out projection ($$\hat{\theta}_{\text{FWL}}$$). Table A6 therefore reports both the nonlinear R-Learner coefficient ($$\hat{\beta}_1$$) and the linear FWL reference coefficient $$\hat{\theta}_{\text{FWL}}$$ used for sensitivity ranges.

The prior-individual-history adjustment does not yield one interchangeable coefficient: Table A2 reports **−5.63 pp** from DML PLR; Table A6 reports **−4.88 pp** from the R-Learner and **−6.11 pp** from the linear FWL projection used for omitted-variable sensitivity. They are different estimators serving different reporting purposes.

{: .table-caption}
<span id="tabla-post4-a6"></span>
**Table A6.** Omitted-variable sensitivity analysis of Cinelli and Hazlett (2020) for overall entry and the vocational-technical channel (IP/CFT, *N* = 62,153)

| Evaluated specification and outcome ($$\hat{\beta}_1$$ R-Learner / linear $$\hat{\theta}_{\text{FWL}}$$) | Partial $$R^2$$ ($$Y \sim D$$ given $$X$$) | Robustness Value $$\text{RV}_q$$ (*q* = 1) | Robustness Value $$\text{RV}_\alpha$$ ($$\alpha$$ = 0.05) | Bound if confounder were 1× as strong as GPA ($$\text{gpa}_{G-1}$$) | Bound if 1× as strong as attendance ($$\text{att}_{G-1}$$) | Bound if 1× as strong as $$G-5$$ school history |
|---|---:|---:|---:|---:|---:|---:|
| Student history ($$G-1$$/$$G-2$$): **2-year HE entry** (−4.88 pp / $$\hat{\theta}_{\text{FWL}}$$ = −6.11 pp) | 0.00548 | 7.16% | 3.36% | ±0.14 pp [−6.25; −5.97] | ±0.10 pp [−6.21; −6.01] | — |
| Student history ($$G-1$$/$$G-2$$): **2-year persistence** (−5.02 pp / $$\hat{\theta}_{\text{FWL}}$$ = −6.52 pp) | 0.00489 | 6.77% | 2.95% | ±0.13 pp [−6.66; −6.39] | ±0.09 pp [−6.62; −6.43] | — |
| Full model (+ $$G-5$$ history): **2-year IP/CFT entry** (−2.09 pp / $$\hat{\theta}_{\text{FWL}}$$ = −2.24 pp) | 0.00403 | 6.16% | 2.33% | ±0.01 pp [−2.25; −2.23] | ±0.16 pp [−2.39; −2.08] | ±0.26 pp [−2.50; −1.98] |
{: .table--compact .table--scroll}

Table A6 measures omitted-confounder sensitivity for the linear FWL projection of IP/CFT entry (−2.24 pp), alongside the R-Learner BLP estimate (−2.09 pp); the 95% threshold uses a school-clustered standard error. An omitted factor would need to explain **6.16%** of residual variation in both closure and IP/CFT entry to move the projected point estimate to zero, or **2.33%** for its confidence interval to include zero. Marks and attendance are weak benchmarks here: after other covariates, their partial $$R^2$$ values with treatment are 0.00000 and 0.00043. The more demanding benchmark is the school's $$G-5$$ history (partial $$R^2$$ of 0.00915). A factor of that strength would move the point estimate by ±0.26 pp (±0.52 pp at twice that strength), to [−2.50, −1.98] pp ([−2.76, −1.72] pp at twice that strength). These are shifts of a point estimate, not confidence intervals. In this projection, the **2.33%** threshold for the confidence interval exceeds the school's observed partial association with closure (**0.915%**); the **6.16%** point-null threshold is higher still. The hypothetical family factor is unobserved, so this comparison cannot show that the finding survives every form of omitted confounding.

<span id="fuentes-y-custodia"></span>
### 5. Official sources, cryptographic receipts, and reproducible tools

All calculations derive from official sources verified via SHA-256 cryptographic checksums recorded in the project's custody receipts: (1) [SIES Higher Education Enrollment 2007–2026](https://datosabiertos.mineduc.cl/matricula-en-educacion-superior/) (20 annual CSV/RAR files); (2) [SIES Higher Education Graduates 2007–2025](https://datosabiertos.mineduc.cl/titulados-en-educacion-superior/) (19 annual files); (3) [PAES/PDT University Admission Tests 2021–2026](https://datosabiertos.mineduc.cl/pruebas-de-admision-a-la-educacion-superior/) (18 registration, score, application, and enrollment packages under CC-BY license); and (4) MINEDUC School Directory, Enrollment, and Student Performance registries (2004–2025). Large-scale data processing ran on [DuckDB](https://duckdb.org/) over columnar [Apache Parquet](https://parquet.apache.org/) stores, and econometric and *Causal Machine Learning* estimation was implemented in Python (numpy, pandas, scipy, scikit-learn, and interpret for ExplainableBoostingRegressor). Aggregated tabular data for all three figures are publicly available in CSV format without any individual or school identifier.


**Transparency and scope of the sources.** The original thesis and this extension series are my own work, as is my co-authorship of the [2014 working paper]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }})[^grau2014]; they therefore do not constitute an independent external replication and keep the historical reconstruction separate from current estimates. I received no external funding and declare no conflicts of interest. My sole institutional affiliation is the Ministry of Social Development and Family of Chile, which did not fund, commission, or review this analysis; all views and conclusions are my sole responsibility. I used artificial intelligence assistants to support reproducible programming, document ingestion, statistical validation, and editing; all methodological decisions and factual verifications are my own. In strict compliance with data governance (ADR-188), no DEMRE 2014–2020 file subject to individual-linkage restrictions was used, relying exclusively on open SIES 2007–2026 and MINEDUC PAES/PDT 2021–2026 (CC-BY) databases.
{: .notice--info}


## References

[^angristpischke2009]: Angrist, Joshua D., and Jörn-Steffen Pischke. 2009. [*Mostly Harmless Econometrics: An Empiricist's Companion*](https://doi.org/10.1515/9781400829828). Princeton, NJ: Princeton University Press. [Scholar](https://scholar.google.com/scholar_lookup?title=Mostly+Harmless+Econometrics&doi=10.1515%2F9781400829828)

[^athey2019]: Athey, Susan, Julie Tibshirani, and Stefan Wager. 2019. [“Generalized Random Forests.”](https://arxiv.org/pdf/1610.01271) *The Annals of Statistics* 47 (2): 1148–78. [DOI](https://doi.org/10.1214/18-AOS1709) · [Scholar](https://scholar.google.com/scholar_lookup?title=Generalized+random+forests&doi=10.1214%2F18-AOS1709)

[^callaway2021]: Callaway, Brantly, and Pedro H. C. Sant'Anna. 2021. [“Difference-in-Differences with Multiple Time Periods.”](http://arxiv.org/pdf/1803.09015) *Journal of Econometrics* 225 (2): 200–230. [DOI](https://doi.org/10.1016/j.jeconom.2020.12.001) · [Scholar](https://scholar.google.com/scholar_lookup?title=Difference-in-Differences+with+multiple+time+periods&doi=10.1016%2Fj.jeconom.2020.12.001)

[^cameron2008]: Cameron, A. Colin, Jonah B. Gelbach, and Douglas L. Miller. 2008. [“Bootstrap-Based Improvements for Inference with Clustered Errors.”](http://www.nber.org/papers/t0344.pdf) *The Review of Economics and Statistics* 90 (3): 414–27. [DOI](https://doi.org/10.1162/rest.90.3.414) · [Scholar](https://scholar.google.com/scholar_lookup?title=Bootstrap-Based+Improvements+for+Inference+with+Clustered+Errors&doi=10.1162%2Frest.90.3.414)

[^cddf2018]: Chernozhukov, Victor, Mert Demirer, Esther Duflo, and Iván Fernández-Val. 2018. [“Generic Machine Learning Inference on Heterogeneous Treatment Effects in Randomized Experiments, with an Application to Immunization in India.”](http://www.nber.org/papers/w24678.pdf) NBER Working Paper 24678 (published in *Econometrica* 93 (1): 1–41, 2025). [DOI](https://doi.org/10.3386/w24678) · [Scholar](https://scholar.google.com/scholar_lookup?title=Generic+Machine+Learning+Inference+on+Heterogeneous+Treatment+Effects+in+Randomized+Experiments%2C+with+an+Application+to+Immunization+in+India&doi=10.3386%2Fw24678)

[^chernozhukov2018]: Chernozhukov, Victor, Denis Chetverikov, Mert Demirer, Esther Duflo, Christian Hansen, Whitney Newey, and James Robins. 2018. [“Double/Debiased Machine Learning for Treatment and Structural Parameters.”](https://doi.org/10.1111/ectj.12097) *The Econometrics Journal* 21 (1): C1–C68. [Scholar](https://scholar.google.com/scholar_lookup?title=Double%2Fdebiased+machine+learning+for+treatment+and+structural+parameters&doi=10.1111%2Fectj.12097)

[^chernozhukov2024]: Chernozhukov, Victor, Christian Hansen, Nathan Kallus, Martin Spindler, and Vasilis Syrgkanis. 2024. [*Applied Causal Inference Powered by ML and AI*](https://arxiv.org/pdf/2403.02467). CausalML-book.org. [DOI](https://doi.org/10.48550/arXiv.2403.02467) · [Scholar](https://scholar.google.com/scholar_lookup?title=Applied+Causal+Inference+Powered+by+ML+and+AI&doi=10.48550%2FarXiv.2403.02467)

[^cinellihazlett2020]: Cinelli, Carlos, and Chad Hazlett. 2020. [“Making Sense of Sensitivity: Extending Omitted Variable Bias.”](https://doi.org/10.1111/rssb.12348) *Journal of the Royal Statistical Society: Series B (Statistical Methodology)* 82 (1): 39–67. [Scholar](https://scholar.google.com/scholar_lookup?title=Making+Sense+of+Sensitivity%3A+Extending+Omitted+Variable+Bias&doi=10.1111%2Frssb.12348)

[^ding2024]: Ding, Peng. 2024. [*A First Course in Causal Inference*](https://api.taylorfrancis.com/content/books/mono/download?identifierName=doi&identifierValue=10.1201/9781003484080&type=googlepdf). Boca Raton, FL: Chapman & Hall/CRC. [DOI](https://doi.org/10.1201/9781003484080) · [Scholar](https://scholar.google.com/scholar_lookup?title=A+First+Course+in+Causal+Inference&doi=10.1201%2F9781003484080)

[^gertler2017]: Gertler, Paul J., Sebastian Martinez, Patrick Premand, Laura B. Rawlings, and Christel M. J. Vermeersch. 2017. [*La evaluación de impacto en la práctica (Impact Evaluation in Practice)*](https://doi.org/10.1596/978-1-4648-0888-3). 2nd ed. Washington, DC: World Bank and Inter-American Development Bank. [Scholar](https://scholar.google.com/scholar_lookup?title=La+evaluaci%C3%B3n+de+impacto+en+la+pr%C3%A1ctica%2C+Segunda+edici%C3%B3n&doi=10.1596%2F978-1-4648-0888-3)

[^grau2014]: Grau, Nicolás, Daniel A. Hojman, Cristián Labra, and Alejandra Mizala. 2014. [“Destructive Creation: School Turnover and Educational Attainment.”]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}) Working Paper 396, [Department of Economics, University of Chile](https://econ.uchile.cl/es/publicacion/destructive-creation-school-turnover-and-educational-attainment).

[^huntingtonklein2025]: Huntington-Klein, Nick. 2025. [*The Effect: An Introduction to Research Design and Causality*](https://theeffectbook.net/). 2nd ed. Boca Raton, FL: Chapman & Hall/CRC.

[^imbensrubin2015]: Imbens, Guido W., and Donald B. Rubin. 2015. [*Causal Inference for Statistics, Social, and Biomedical Sciences: An Introduction*](https://doi.org/10.1017/CBO9781139025751). New York: Cambridge University Press. [Scholar](https://scholar.google.com/scholar_lookup?title=Causal+Inference+for+Statistics%2C+Social%2C+and+Biomedical+Sciences&doi=10.1017%2FCBO9781139025751)

[^mackinnonwebb2017]: MacKinnon, James G., and Matthew D. Webb. 2017. [“Wild Bootstrap Inference for Wildly Different Cluster Sizes.”](https://doi.org/10.1002/jae.2508) *Journal of Applied Econometrics* 32 (2): 233–54. [Scholar](https://scholar.google.com/scholar_lookup?title=Wild+Bootstrap+Inference+for+Wildly+Different+Cluster+Sizes&doi=10.1002%2Fjae.2508)

[^manski2003]: Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). New York: Springer. [Scholar](https://scholar.google.com/scholar_lookup?title=Partial+Identification+of+Probability+Distributions&doi=10.1007%2Fb97478)

[^niewager2021]: Nie, Xinkun, and Stefan Wager. 2021. [“Quasi-Oracle Estimation of Heterogeneous Treatment Effects.”](https://arxiv.org/pdf/1712.04912) *Biometrika* 108 (2): 299–319. [DOI](https://doi.org/10.1093/biomet/asaa076) · [Scholar](https://scholar.google.com/scholar_lookup?title=Quasi-oracle+estimation+of+heterogeneous+treatment+effects&doi=10.1093%2Fbiomet%2Fasaa076)

[^rambachan2023]: Rambachan, Ashesh, and Jonathan Roth. 2023. [“A More Credible Approach to Parallel Trends.”](https://doi.org/10.1093/restud/rdad018) *The Review of Economic Studies* 90 (5): 2555–91. [Scholar](https://scholar.google.com/scholar_lookup?title=A+More+Credible+Approach+to+Parallel+Trends&doi=10.1093%2Frestud%2Frdad018)

[^roth2023]: Roth, Jonathan, Pedro H. C. Sant'Anna, Alyssa Bilinski, and John Poe. 2023. [“What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature.”](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–44. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)

[^wager2024]: Wager, Stefan. 2024. [*Causal Inference: A Statistical Learning Approach*](https://web.stanford.edu/~swager/causal_inf_book.pdf). Stanford University monograph.
