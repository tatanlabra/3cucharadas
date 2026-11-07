---
layout: single
classes: [thesis-recreation-post]
title: "Replicating my thesis in three spoonfuls (part I): what survived and what the evidence corrected"
subtitle: "I measured my 2014 thesis on school entry and exit again. The overall story survived, several numbers did not, and the working files helped explain why."
date: 2026-08-29 09:30:00 -0400
last_modified_at: 2026-11-06 09:00:00 -0300
categories: [data, education, public-policy]
tags: [replicability, education, school-market, voucher, mineduc, duration-analysis, vulnerability, audit]
description: "I rebuilt the results of my 2014 thesis on Chilean schools and audited 34 claims: what held, what was wrong then, and what still cannot be known."
excerpt: "The thesis did not emerge intact, but it did not collapse either. The producer files separated rebuilt results, 2014 errors, sensitivity analyses, and limits of the evidence."
author: clabra
lang: en
ref: replica-tesis-establecimientos-educacionales
permalink: /datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/
header:
  teaser: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/og-1200x630.webp
  og_image_alt: An archived thesis and reconstructed school models as a metaphor for a replication that corrects its original.
  overlay_image: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/teaser-mobile-640x360.webp
visual_id: replica-tesis-establecimientos
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

In April 2014 I defended and submitted my master's thesis on the entry and exit of Chilean schools between 1992 and 2012.[^tesis] Twelve years later I am trying to rebuild it and extend it through 2025.
{: .text-justify}

Over that interval, the rules changed: municipalisation in the 1980s; shared financing in the 1990s; the Preferential School Subsidy (SEP, its Spanish acronym) in the 2000s; Inclusion and New Public Education in the 2010s; and another state architecture in the 2020s.[^regimenes] The market changed, and so did the relationships that might explain school exits.
{: .text-justify}

Before adding thirteen years, I had to answer a smaller question: **which 2014 results could I produce again exactly?** In brief, 15 judgements were supported and 10 errors came from the 2014 document. None carried into the 2026 version I now use as a reference. Of the remaining 9, 1 was wrong on both sides, 1 was a misleading match, and 7 do not clearly show where the error lay.
{: .text-justify}

I did not want to turn this into a contest between tools: the story is not that Python defeated Stata or that my old MacBook lost to today's Lenovo. It is what survived the comparison, with more evidence and experience—and the inevitable bias of auditing myself. The thesis is mine and so is the audit: this is not an independent replication.
{: .text-justify}

Nothing below is causal. “Entry” and “exit” mean appearing in or disappearing from the administrative register, not observing the decision to open, close, or fail. “IVE” is aggregate school vulnerability, not poverty or individual vulnerability. And “rebuilt” means produced again from the available data and code, not recovering the exact 2014 session. RBD is each school's official identifier, and SIMCE is the national standardised learning assessment. Full series: **Part I** · [Part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) · [Part III]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/' | relative_url }}).
{: .small}

## Spoonful 1: what survived

The first conclusion held. Between 1992 and 2012, Chile did not merely have more or fewer schools; it experienced a **reallocation across sectors** (types of school administration). My reconstruction counts 2,168 entries and 2,069 exits. Municipal schools record 346 entries and 1,135 exits; subsidised private schools, 1,468 and 597; fee-paying private schools, 354 and 337.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp' | relative_url }}" title="Figure 1 — Mobility by sector" aria-label="Open Figure 1 enlarged">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp' | relative_url }}" alt="At left, the school-mobility figure published in 2014. At right, the 2026 reconstruction: municipal 346 entries and 1,135 exits, subsidised private 1,468 and 597, fee-paying private 354 and 337." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figure 1</strong> — Mobility by sector. The reconstruction totals 2,168 entries and 2,069 exits; my 2014 workbook, 2,160 and 2,065. The substantive pattern—municipal exit and subsidised-private entry—survives. Source: Labra Olivares (2014), master's thesis (left), and my 2026 recreation on the 1992–2012 school directory (right).</figcaption>
</figure>

The totals are not identical, but they tell the same story. In Table 1 for 2012, the aggregate share distance from the prior run in my 2014 working spreadsheet is 3.05 percentage points, whereas the sum of absolute differences in percentage points across the six shares between the published text and the spreadsheet reaches 13.41 percentage points (4.50 points in the municipal sector, 2.42 in free subsidised-private schools, and 4.27 in the high-fee bracket): the reconstruction resembles the file that produced the figure more closely than the document I signed.
{: .text-justify}

The second surviving conclusion is distributive. In Greater Santiago (Table 8), schools that later left the register served more vulnerable enrolments: 87.4% versus 78.3% among municipal schools, and 72.2% versus 62.8% among subsidised private schools. All 42 rebuilt cells are compatible with the published rounding margin, although the effective number of observations does not match the printed *N*. The magnitude survives; the exact universe does not.
{: .text-justify}

This describes selection (who belongs to each group), not effects. With data from 2002 to 2012, Paredes and Fresard associate lower enrolment with a greater probability of closure and study where pupils go afterwards.[^paredes2018] Núñez, Solís, and Soto examine two rural communities in southern Chile after the 2010 earthquake and show that how a school is closed matters to social cohesion.[^nunez2014] My data follow the same units over time, but they cannot establish those findings: they observe administrative flows, not motives, later trajectories, or community life.
{: .text-justify}

Several smaller results survived too: **10 of the 11 published fixed effects** (the model's average coefficients), the SIMCE gap among closing subsidised schools, seven municipalities above a mobility threshold, and the negative sign of the relation between concentration and mobility. Including the constant, there are 12 coefficients in the file, 11 effects in the table, and 10 matches.
{: .text-justify}

{: .table-caption}
**Table 1.** Audit balance and differences that change the interpretation

| Level | Result | Evidence | Verdict |
|---|---|---|---|
| Overall balance | 15 supported judgements; 10 errors in the 2014 document; 0 known errors in the 2026 reference output | Producer files and present-day reruns distinguish a published error from a reconstruction error. | The substantive account survives, with corrections. |
| Remaining limits | 1 error on both sides; 1 misleading match; 7 provenance or no-winner cases | The evidence explains why there is no valid comparison, even when it cannot name a winner. | No accuracy rate is forced. |
| Lagged SIMCE | 0.003 in the table; 0.001 in the producing output and two engines | 0.000533 rounds to 0.001. | 2014 transcription error. |
| Model variances | 3.82 and 2.791 | They were crossed log standard deviations, not variances. | 2014 interpretation error. |
| Municipal HHI | Santiago around 1,534 | The canonical scale gives around 152. | 2014 scale error. |
| Small cities | “Fewer than 15,000 inhabitants” account for about 80% | The capital/non-capital split gives 78.3%; the literal population threshold gives 11%. | The number and sentence refer to different partitions. |
| SIMCE gap | −4.3% among closing subsidised schools | The producer spreadsheet also gives −4.3%. | Producer value verified. |
| Mobility | Rates 6.3, 4.5, and 1.6 | Producer formulas recover every compared point. | Final match; causal interpretation remains unproven. |
| Between/within decomposition (Tables 3 and 7) | Enrolment and lagged SIMCE: between-school association (0.012131; *t* = 16.27), null within (−0.000048; *t* = −0.53). Pupils/teacher: mean gap of 5.90 and 6.23; additional fall of 0.216 and 0.148 per year, without inference | Table 7: pooled OLS with Mundlak means and RBD-clustered errors; replaces the random slope that collapsed (2.1 × 10⁻¹⁵). Table 3: descriptive decomposition. | The SIMCE–enrolment association reflects sorting across schools; prior contraction is descriptive. |
| Out-of-sample predictive alert (Table 10) | 2007–2008 training and 2009–2011 test: AUC = 0.8517; Brier = 0.008196 versus 0.008324 with no model | The top risk decile captures 43.7% of the 151 closures (69.5% in the top quintile); mean predicted risk of 0.60% versus 0.84% observed. | Ranks out-of-sample risk well; underpredicts its level and does not identify causes. |
{: .table--compact .table--scroll}

Counting by display answers a different question. Of 26 objects, twelve converge, ten have explained divergences, and four lack a numerical test; no divergence remains unexplained. I do not turn that inventory into an “accuracy rate”: an inequality, a rounding match, and literal equality are not the same test.
{: .small}

## Spoonful 2: who was wrong

A discrepancy between 2014 and 2026 does not identify who was wrong. It may come from transcription, code, sample, or estimand; with only “published” and “rebuilt,” each explanation can be invented after seeing the result.
{: .text-justify}

Clemens proposes a conservative rule: “follow-up studies should be considered robustness checks until proven to be replications” (p. 327).[^clemens2015] This matters: only after obtaining Reinhart and Rogoff’s working spreadsheet did Herndon, Ash, and Pollin isolate exclusion, coding, and weighting errors.[^herndon2013] Christensen and Miguel argue that open data and materials make credibility assessable.[^christensen2018] Hamermesh separates pure replication, which checks a published paper with its own data, from scientific replication, which tests the result on a different population, and notes that both are scarce in economics: an activity most economists applaud but few perform.[^hamermesh2007]
{: .text-justify}

I therefore added a third source: 2014 files that preserve traces of the calculation, including Stata output, spreadsheets, and charts, plus a new run where feasible. Before attributing a difference, I checked where each file came from, recorded the evidence, and fixed the comparison rule. The three sources stay separate so a technical repair cannot rewrite historical evidence. The third did not always favour the present.
{: .text-justify}

<figure class="recreation-pipeline-figure">
  <a href="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-en.svg' | relative_url }}" target="_blank" rel="noopener">
    <picture>
      <source media="(max-width: 47.99em)" srcset="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-en-mobile.svg' | relative_url }}">
      <img src="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-en.svg' | relative_url }}" alt="Three input classes—pieces and data, descriptive statistics, and associational econometrics—pass through one shared chain of custody, execution, comparison, and attribution before the result is classified and the causal boundary declared." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 2</strong> — Reconstruction and verification chain. If a check fails, the claim stops; an apparent match cannot replace missing evidence. Source: my own elaboration.</figcaption>
</figure>

The sequence matters for public policy. Change the definition of exit, the sample, or the comparison precision, and an administrative flow can resemble system decline. If a model runs without preserving the same ordered list of values, all I know is that it could run. The diagram condenses the boundary: **rerunnable does not mean rebuildable; rebuildable does not mean matching; matching does not mean correct; correct does not mean causal**.
{: .text-justify}

### Where my 2014 self was wrong

The cleanest case sits in the hierarchical model. The table reports **0.003** for lagged mathematics SIMCE; the Stata output that produced it prints **0.001**. Re-estimation gives 0.000533 in both Stata and Python, which rounds to 0.001. Seven alternative explanations were refuted. This was neither translation nor precision: it was transcription.
{: .text-justify}

In the same family of models (Table 6), two rows labelled as variances (measures of dispersion) were the log standard deviations printed by Stata, left untransformed and crossed in the original 2014 RTF table. The table reported 3.82 as the “intercept variance” and 2.791 as the “residual variance”; in fact, the between-municipality (random-intercept) variance is 265.6 and the residual variance is 2,079.7.[^fn3] Elsewhere, 0.4142 became 1.4142. Moreover, because three 2006 cross-sectional covariates lacked within-school time variation, the random-slope variance in the Greater Santiago model (Table 7, *N* = 14,704 observations across 2,640 schools) collapsed onto the numerical boundary (2.1 × 10⁻¹⁵). I re-estimated that specification with the Mundlak and Chamberlain decomposition, which separates each school's historical mean from its annual deviations, with RBD-clustered standard errors.[^mundlak1978][^chamberlain1982] Whereas the vulnerable pupil share comes from Table 8, the dependent variable in Table 7 is log enrolment, ln(enrolment). The positive association with lagged mathematics SIMCE comes from permanent differences *between* schools ($$\hat{\beta}_{\text{between}}$$ = 0.012131; *t* = 16.27); within the same school, annual SIMCE changes are not associated with enrolment changes ($$\hat{\beta}_{\text{within}}$$ = −0.000048; *t* = −0.53). I do not use the dynamic version for this separation: because it includes the school-level mean of lagged enrolment, it contains the dependent variable itself and introduces Nickell bias. Sometimes archaeology finds an underlying statistical mechanism; sometimes it finds a copy-and-paste error.
{: .text-justify}

The concentration index produced the error with the largest interpretive consequence for public policy. The Herfindahl–Hirschman index (HHI, a measure of how concentrated supply is) runs from 0 to 10,000 and uses 2,500 as the high-concentration threshold under the 2010 United States Merger Guidelines (the 2023 guidelines lowered it to 1,800). My spreadsheet stored the index times one hundred; the text read it as if it were times one thousand. Santiago therefore appeared around 1,534 when the canonical value was roughly 152.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" title="Figure 3 — Concentration and mobility" aria-label="Open Figure 3 enlarged">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" alt="At left, the 2014 concentration figure on an axis from 0 to 100. At right, the reconstruction on the canonical 0 to 10,000 scale, with a negative slope and p equal to 0.084." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figure 3</strong> — Concentration and mobility. The negative sign survives, but the slope is no longer distinguishable from zero at 5% (p = 0.084; under the model, the p-value summarises how incompatible the data are with a zero slope). In the rebuilt panel with data in both cross-sections, the published scale would label 318 of 337 municipalities highly concentrated; the canonical scale labels 66. Source: Labra Olivares (2014), master's thesis (left), and my 2026 recreation (right).</figcaption>
</figure>

In sheet hhi2 of TESIS.xlsx, the spreadsheet even preserved the threshold formula: “=C2>2.5”. On its scale that means 250 canonical points, not 2,500, and selects 330 of 346 municipalities in 2006 and 326 in 2016 (whereas the panel rebuilt for the figures covers 318 of 337 municipalities with data in both cross-sections). A filter that passes 95% of cases is not filtering very much.
{: .text-justify}

Another nearly correct result concealed a different definition. The text said that intermediate and small cities—fewer than 15,000 inhabitants—accounted for about 80% of mobility in six regions. The figure's recipe split regional capitals from the rest and yielded 78.3%. Applied literally, the population threshold yielded 11%. The number was close; the sentence described another partition.
{: .text-justify}

The most suggestive new finding was not quantified in the thesis. The pupil–teacher ratio among exiting schools falls from 17.95 to 12.22 over the previous seven years, against 20.31 among schools that remain in the register. To separate level and trend in Table 3, I compared municipal and subsidised-private schools between 2004 and 2011 (59,808 observations = 36,493 municipal + 23,315 subsidised-private). On average, schools that later exit operated with 5.90 fewer pupils per teacher in the municipal sector and 6.23 fewer in the subsidised-private sector. Their ratio also fell faster: 0.849 pupils per teacher per year versus 0.632 among staying municipal schools, and 0.565 versus 0.417 among subsidised-private schools. That additional difference, of 0.216 and 0.148 per year, is descriptive: I did not compute standard errors for the difference. Most of the decline is shared across the system; what distinguishes exiting schools is, above all, a smaller scale visible retrospectively across the previous seven years. The label is retrospective: it marks the entire prior history of a school that later disappears.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" title="Figure 4 — The shadow of death" aria-label="Open Figure 4 enlarged">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" alt="Series with confidence intervals for pupils per teacher among exiting schools: a fall from 17.95 to 12.22 over seven years, against 20.31 among incumbents." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figure 4</strong> — The “shadow of death”: fewer pupils per teacher during the seven years before exit. This is a descriptive pattern conditioned by the timing-marker problem, not a causal estimate. Source: my own elaboration with the 2026 recreation of the thesis data (1992–2012).</figcaption>
</figure>

That figure is relevant to public policy precisely because it does not promise what it cannot observe. A gradual deterioration raises questions about early warning, enrolment, staffing, and institutional response; it does not show that a particular intervention prevents closure or that closure causes the deterioration.
{: .text-justify}

<aside class="notice--info" markdown="1">
**Methodological note — How I separated between-school differences from within-school change (Mundlak–Chamberlain CRE):** A standard linear mixed model assumes that unobserved permanent school traits are uncorrelated with the explanatory variables; when that assumption fails, it blends differences *between* distinct schools with changes *within* the same school over time into a single number. To avoid that conflation in Table 7, I included each school's historical mean of every time-varying covariate ($$\bar{X}_i$$, the Mundlak 1978 and Chamberlain 1982 decomposition) and clustered standard errors by RBD.[^mundlak1978][^chamberlain1982] The coefficient on the annual deviation $$X_{it} - \bar{X}_i$$ then isolates variation *within* the school—although it remains exposed to time-varying factors and to the fact that non-tested intermediate SIMCE years were imputed via annual growth before lagging the series—whereas the coefficient on $$\bar{X}_i$$ captures structural sorting *between* distinct schools. In the dynamic specification ($$\hat{\beta}_{\text{between}}$$ = 0.000543, *t* = 7.26; $$\hat{\beta}_{\text{within}}$$ = 0.000174, *t* = 2.44), including the school-level mean of lagged enrolment introduces Nickell bias, so I lead with the static specification.
</aside>

## Spoonful 3: what is ready to be extended through 2025

**This was the test I needed before adding thirteen years: not that every 2014 number survived, but that I knew exactly what I was extending.** All the available code ran again, but it did not always produce the same result. Rerunnable means the code finishes; rebuildable, that it produces something comparable again; matching, that it passes a criterion fixed before looking at the result. Those are different claims.
{: .text-justify}

{% include evidence-carousel.html %}

When I reopened those nine cases with a different question—whether a common basis for comparison existed—three had one and matched, two had one and retained differences, and four lacked one. That second classification does not change their editorial verdict: the present rerun completed the recoverable routes and rebuilt the tables and figures, but it does not establish the effective 2014 session. The registry retains **50 technical hypotheses** and **34 editorial judgements**: the former test explanations; the latter classify published claims. Neither is an accuracy rate for the other.
{: .text-justify}

A comparison is informative only when both routes answer the same question: sample size, outcome definition, value order, and published precision are part of the result. A nearby number may hide a real discrepancy, while two identical numbers may inherit the same mistaken definition; what matters is the evidence that distinguishes a supported result from a coincidence.
{: .text-justify}

In the three matching cases, the tables or series retained a common basis and passed a rule fixed before comparison. In the two cases that remained different, rerunning the analysis did not erase the discrepancy; it located its starting point more precisely. Different tools reproduced the recoverable results, reducing the possibility that a finding depends on one particular program. Even so, that convergence supports the present calculation; on its own, it does not recreate the historical run.
{: .text-justify}

The other four cases teach a different lesson. When no common list of values, series, or sufficiently detailed output survives, comparing only the appearance of two figures would answer a new question. Calling them non-comparable is less dramatic than announcing a replication, but it protects the interpretation. The absence of a valid test does not make the original publication false or the reconstruction correct; it leaves an evidence debt that retrospective confidence cannot settle.
{: .text-justify}

This distinction matters beyond the thesis. An administration might use a rebuilt number to describe a historical period, formulate an alert, or justify an intervention. Those uses demand different support. A descriptive pattern can open a monitoring question; an alert needs out-of-sample validation and explicit error costs; an intervention needs a contrast that can approximate the counterfactual. If those uses are blurred, predictive accuracy or technical traceability ends up lending causal authority that the design never earned. In 2014 the discrete-time hazard model (*cloglog* on 2007–2011, Table 10: 30,484 school-year observations across 7,460 RBDs and 237 closures) had only been evaluated within the estimation sample. I now trained it on 2007–2008 transitions (12,495 rows and 86 closures) and evaluated it on 2009–2011 (17,989 rows and 151 closures), years not used to estimate it. It ranks risk well: the 10% of school-year records with the highest predicted risk concentrates 43.7% of closures (66 of 151) and the top 20% concentrates 69.5% (AUC = 0.8517; Hanley–McNeil reference interval of 0.81–0.89 on this single temporal split). Yet it misses the level: it predicted a mean risk of 0.60% when the observed rate was 0.84%, and its Brier score (0.008196) improves by only 1.5% on assigning every observation the observed base rate (0.008324). It is useful for ranking monitoring priorities, not for reading off absolute probabilities.
{: .text-justify}

<aside class="notice--info" markdown="1">
**Methodological note — Out-of-sample temporal validation (Table 10):** Evaluating a risk model on the same years used to estimate it usually overstates its accuracy, because the algorithm already “knows” which schools closed. I therefore estimated it on 2007–2008 and evaluated it on 2009–2011. Two metrics answer different questions. The AUC measures whether it ranks well: the probability that a record ending in closure receives a higher risk score than one that does not. The Brier score (0.008196) measures the mean squared error between predicted probability and actual closure; against the 0.84% school-year base rate in 2009–2011, any model sits close to zero, so it is benchmarked against assigning that base rate to all observations (0.008324). Covariates were standardised using 2007–2011 means and the estimation includes a ridge penalty; neither uses the 2009–2011 closures, though the former uses their covariates. Focusing diagnostics on the 10% or 20% of school-year records with the highest risk captures between two-fifths and seven-tenths of actual exits, without attributing causality.
</aside>

The extension through 2025 does not inherit every variable or interpretation, but defensible definitions and open questions. In 1992–2012 the aggregate directory only allowed counting raw RBD exits (2,069) without following pupils. From 2004 onward, longitudinal records support a **Data-Inferred School Closure Rule (RCID v1, its Spanish acronym)** with three nested levels. D0 gathers permanent closures with prior enrolment: 1,981 between 2005 and 2025. D1 deducts directory continuities, annexes, and replacements, leaving 1,807. D2 further deducts absorptions—when at least 70% of reassigned pupils move to a single stable receiving school in the closure year and the following year, with destination concentration HHI ≥ 5,000 on the 0–10,000 scale—and leaves **1,678 inferred closures** in its conservative version: 1,382 in 2005–2015 and 296 in 2016–2025. When a complete observed following year is also required, **1,648** remain (1,382 and 266 in 2016–2025). This is an empirical inference, not the documentary certainty of a resolution or closure certificate.
{: .text-justify}

I did not undertake this archaeology to acquit or condemn my 2014 work. Before constructing 2013–2025, I needed to separate what I could produce again, what was wrong, what was a sensitivity analysis (an alternative result under a different decision), and what could not be compared.
{: .text-justify}

What matters is not vindicating the original, but reaching [part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) with an auditable 1992–2012 base, known errors corrected, and visible limits. Now adding thirteen years makes sense: not to prolong a series, but to learn what changed with the rules and what it means for a school to enter or leave the register.
{: .text-justify}

## Closing: from replication to extension

The thesis ended up organised into four groups: results that survive, 2014 errors, a 2026 version with no known errors, and cases with no valid comparison. That separation shows what to retain and what not to carry into 1992–2025.
{: .text-justify}

The general direction of reallocation between 1992 and 2012 survives: municipal loss and subsidised-private expansion. Greater vulnerability among schools that later leave the register also survives, **only for the reconstructed Greater Santiago universe**. The scale of the concentration index, the literal reading of “fewer than 15,000 inhabitants”, two variances, several labels, and one key timing definition do not. Discrepancies found in the present route were corrected iteratively until the canonical output had no known errors; alternatives remain visible as sensitivity checks, not as the reconstruction.
{: .text-justify}

{: .table-caption}
**Table 2.** What public use survives, and where the evidence ends

| Result | Reasonable public use | What it does not authorise |
|---|---|---|
| Reallocation across sectors, 1992–2012 | Historical diagnosis of sectoral change | Causal attribution to a reform |
| Vulnerability in the reconstructed Greater Santiago universe | Questions about protection and educational continuity (separating the permanent between-school gap from within-school variation) | Generalisation to Chile or effects of closure |
| Pupil–teacher ratio and *cloglog* hazard before exit | Targeting preventive monitoring (out-of-sample AUC = 0.8517; 43.7% of closures in the top risk decile; ranks risk, but does not calibrate its level) | Presenting them as an automatic closure rule or causal effect |
| Corrected HHI | Describing concentration on the correct scale | Inferring the effect of competition on closure or mobility |
{: .table--compact .table--scroll}

The second part cannot add thirteen rows and pretend continuity. A school in the 1980s, one in the 1990s, one after SEP, one under Inclusion, and one transferred to a Local Education Service do not face the same market or the same state. A series can be calculated flawlessly and still answer another question. That is a particularly dangerous false signal of success in public policy.
{: .text-justify}

### From describing closure to identifying a policy

The reconstruction leaves a panel that can describe flows, recognise risk signals, and re-estimate associations. It does not observe why each school closed, what would have happened without a reform, or the individual trajectories of its pupils. More controls, fixed effects, sophisticated standard errors, or computing power can reduce some biases; **they do not create the missing counterfactual** (what would have happened without the reform or closure).
{: .text-justify}

[Part II]({{ '/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/' | relative_url }}) revisits these three questions without treating them as interchangeable:
{: .text-justify}

{: .table-caption}
**Table 3.** Causal routes and minimum conditions

<div class="causal-routes causal-routes--en" markdown="1">

| Route | Question and design | Minimum condition for interpretation |
|---|---|---|
| **Descriptive/predictive warning** | Model transitions among active, zero enrolment, recess, official closure, and absence from the register; estimate out-of-sample risk (in years or cases not used to fit the model). | Temporal validation, calibration (predicted risk should resemble observed frequency), decision thresholds, and a distributive audit. It can guide monitoring; it does not estimate effects. |
| **Staggered reform** | Evaluate changes associated with transfer to Local Education Services using difference-in-differences (comparing changes between affected and unaffected groups) and a cohort event study. | Verified dates and exposure; plausible parallel trends (similar pre-reform evolution), anticipation, composition, and spillovers. If rollout timing responded to risk, the design is not causal by decree. |
| **Consequences of closure** | Link pupil trajectories and compare continuity, distance, attendance, attainment, and dropout through an event study or matched difference-in-differences. | Cause of closure, genuinely comparable controls, and plausibly exogenous variation (not determined by the outcome); matching alone does not remove selection. |
{: .table--compact .table--scroll}

</div>

There is, however, a question that comes before econometric design. In a system where schools open and close, so-called **“creative destruction”** (replacing those that leave with new schools) may renew supply, displace lower-performing schools, or move pupils towards better alternatives. But the balance cannot be assessed only by observing which school disappears and which takes its place. Chilean evidence also points to costs of closure in grade repetition and dropout, as well as community effects that do not fit neatly into an enrolment count.[^grau2018][^nunez2014]
{: .text-justify}

That changes the public-policy question. The task is neither to prevent every closure nor to preserve every school. It is to determine **who absorbs the cost of transition**: which pupils must move, where they arrive, how much farther they travel, what happens to attendance, learning, and persistence, and what the community loses. Available seats are necessary; they do not exhaust those costs.
{: .text-justify}

Part II clarifies administrative events, examines institutional comparisons that cannot identify effects, and leaves individual follow-up pending; [Part III]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/' | relative_url }}) addresses it using student trajectories. That boundary matters because a longer dataset cannot replace the student trajectories that the 2014 thesis could barely observe.
{: .text-justify}

The open question is less comfortable than counting entries and exits: **when does creative destruction genuinely renew educational supply, and when does it merely shift its costs onto pupils, families, and territories with less capacity to absorb them?**
{: .text-justify}

An RBD—the school's official identifier—may disappear from the register. **A pupil's trajectory does not restart when that happens.**
{: .text-justify}

---

## References

[^tesis]: Labra Olivares, Cristián A. *Patrones de entrada y salida de establecimientos educacionales en Chile (1992-2012)*, master's thesis, Universidad de Chile, 2014. Advisor: Daniel Hojman T.

[^fn3]: In the Stata output for Table 6, the printed parameters are log standard deviations: the between-municipality (random-intercept) variance is 265.6—that is, e^(2 * 2.791)—and the residual variance is 2,079.7—that is, e^(2 * 3.82)—which were left unexponentiated and crossed in the original 2014 RTF table.

[^grau2018]: Grau, Nicolás; Hojman, Daniel; Labra, Cristián; Mizala, Alejandra. [Destructive Creation: School Turnover and Educational Attainment]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}), working paper SDT 396, Department of Economics, Universidad de Chile, 2014; Grau, Nicolás; Hojman, Daniel; Mizala, Alejandra. [School closure and educational attainment: Evidence from a market-based system](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf), *Economics of Education Review* 65, 1–17, 2018. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)

[^paredes2018]: Paredes, Ricardo D.; Fresard, Matías. Voucher y cierre de escuelas en Chile, *Estudios Públicos* 151, 7–27, 2018.

[^nunez2014]: Núñez, Carmen Gloria; Solís, Camila; Soto, Rodrigo. [¿Qué sucede en las comunidades cuando se cierra la escuela rural?](https://revistas.javeriana.edu.co/index.php/revPsycho/article/download/3602/8527), *Universitas Psychologica* 13(2), 615–625, 2014. [DOI](https://doi.org/10.11144/Javeriana.UPSY13-2.qscc) · [Scholar](https://scholar.google.com/scholar_lookup?title=%C2%BFQu%C3%A9+sucede+en+las+comunidades+cuando+se+cierra+la+escuela+rural%3F+Un+An%C3%A1lisis+Psicosocial+de+la+Pol%C3%ADtica+de+Cierre+de+las+Escuelas+Rurales+en+Chile&doi=10.11144%2FJaveriana.UPSY13-2.qscc)

[^regimenes]: Biblioteca del Congreso Nacional de Chile. [History of Decree-Law No. 3063](https://www.bcn.cl/historiadelaley/historia-de-la-ley/vista-expandida/8363/); [Law No. 19247](https://www.bcn.cl/leychile/navegar?idNorma=127911); [Law No. 20248](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=269001&idVersion=); [Law No. 20845](https://www.bcn.cl/leychile/Navegar?idNorma=1078172&idParte=9605200&idVersion=2222-02-02); [Law No. 21040](https://www.bcn.cl/leychile/Navegar?idNorma=1111237&idParte=9853075).

[^christensen2018]: Christensen, Garret; Miguel, Edward. [Transparency, Reproducibility, and the Credibility of Economics Research](https://doi.org/10.1257/jel.20171350), *Journal of Economic Literature* 56(3), 920–980, 2018. [Scholar](https://scholar.google.com/scholar_lookup?title=Transparency%2C+Reproducibility%2C+and+the+Credibility+of+Economics+Research&doi=10.1257%2Fjel.20171350)

[^clemens2015]: Clemens, Michael A. [The Meaning of Failed Replications: A Review and Proposal](https://doi.org/10.1111/joes.12139), *Journal of Economic Surveys* 31(1), 326–342, 2017 (online 2015). [Scholar](https://scholar.google.com/scholar_lookup?title=THE+MEANING+OF+FAILED+REPLICATIONS%3A+A+REVIEW+AND+PROPOSAL&doi=10.1111%2Fjoes.12139)

[^herndon2013]: Herndon, Thomas; Ash, Michael; Pollin, Robert. [Does high public debt consistently stifle economic growth?](https://doi.org/10.1093/cje/bet075), *Cambridge Journal of Economics* 38(2), 257–279, 2014 (online 2013). [Scholar](https://scholar.google.com/scholar_lookup?title=Does+high+public+debt+consistently+stifle+economic+growth%3F+A+critique+of+Reinhart+and+Rogoff&doi=10.1093%2Fcje%2Fbet075)

[^hamermesh2007]: Hamermesh, Daniel S. [Viewpoint: Replication in economics](https://doi.org/10.1111/j.1365-2966.2007.00428.x), *Canadian Journal of Economics* 40(3), 715–733, 2007. [Scholar](https://scholar.google.com/scholar_lookup?title=Viewpoint%3A+Replication+in+economics&doi=10.1111%2Fj.1365-2966.2007.00428.x)

[^mundlak1978]: Mundlak, Yair. [On the Pooling of Time Series and Cross Section Data](https://doi.org/10.2307/1913646), *Econometrica* 46(1), 69–85, 1978. [Scholar](https://scholar.google.com/scholar_lookup?title=On+the+Pooling+of+Time+Series+and+Cross+Section+Data&doi=10.2307%2F1913646)

[^chamberlain1982]: Chamberlain, Gary. [Multivariate Regression Models for Panel Data](https://doi.org/10.1016/0304-4076(82)90094-X), *Journal of Econometrics* 18(1), 5–46, 1982. [Scholar](https://scholar.google.com/scholar_lookup?title=Multivariate+Regression+Models+for+Panel+Data&doi=10.1016%2F0304-4076%2882%2990094-X)
