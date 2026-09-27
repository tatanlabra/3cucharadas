---
layout: single
title: "Replicating my thesis in three spoonfuls I: what survived and what the evidence corrected"
subtitle: "I measured my 2014 thesis on school entry and exit again: most of the story survived, several numbers did not, and the producer files made it possible to decide why"
date: 2026-08-29 09:30:00 -0400
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
math: true
toc: true
toc_sticky: true
comments: true
author_profile: true
distribution:
  social: false
  republish: []
  skip_reason: "Post-publication distribution paused by editorial decision when the post was published."
ai_disclosure:
  level: some_ai
  components:
    text: unknown
    hero: generated
---

In April 2014 I defended and submitted my master's thesis on the entry and exit of Chilean schools between 1992 and 2012.[^tesis] Twelve years later I am trying to rebuild it and extend it through 2025.
{: .text-justify}

Over that interval, the rules changed: municipalisation in the 1980s; shared financing in the 1990s; the Preferential School Subsidy in the 2000s; Inclusion and New Public Education in the 2010s; and another state architecture in the 2020s.[^regimenes] The market mutated very quickly, and so did the relationships that might explain school exits. AI at least publishes release notes; Chile's school system does not always do so.
{: .text-justify}

Before adding thirteen years, I had to answer a smaller question: **which 2014 results could I produce again exactly?** In brief, fifteen judgements were correctly supported, ten errors belonged to the 2014 document, none remains as a known error in the canonical 2026 output, one was wrong on both sides, another was a misleading match, and seven delimit the evidence without clearly assigning an error.
{: .text-justify}

I wanted to pit the tools against each other, but the story is not that Python defeated Stata or that my old MacBook lost to today's Lenovo. It is what survived the comparison, with more evidence and experience—and the inevitable bias of auditing myself. The thesis is mine and so is the audit: this is not an independent replication.
{: .text-justify}

Nothing below is causal. “Entry” and “exit” mean appearing in or disappearing from the administrative register, not observing the decision to open, close, or fail. “IVE” is aggregate school vulnerability, not poverty or individual vulnerability. And “rebuilt” means produced again from the available data and code, not recovering the exact 2014 session.
{: .small}

## Spoonful 1: what survived

The first conclusion held. Between 1992 and 2012, Chile did not merely have more or fewer schools; it experienced a **reallocation across sectors** (types of school administration). My reconstruction counts 2,168 entries and 2,069 exits. Municipal schools record 346 entries and 1,135 exits; subsidised private schools, 1,468 and 597; fee-paying private schools, 354 and 337.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp' | relative_url }}" title="Figure 1 — Mobility by sector" aria-label="Open Figure 1 enlarged">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp' | relative_url }}" alt="At left, the school-mobility figure published in 2014. At right, the 2026 reconstruction: municipal 346 entries and 1,135 exits, subsidised private 1,468 and 597, fee-paying private 354 and 337." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figure 1</strong> — Mobility by sector. The reconstruction totals 2,168 entries and 2,069 exits; my 2014 workbook, 2,160 and 2,065. The substantive pattern—municipal exit and subsidised-private entry—survives.</figcaption>
</figure>

The totals are not identical, but they tell the same story. My 2014 working spreadsheet is 3.05 percentage points from the reconstruction and 13.41 from the published prose: the reconstruction resembles the file that produced the figure more closely than the document I signed.
{: .text-justify}

The second surviving conclusion is distributive. In Greater Santiago, schools that later closed served more vulnerable enrolments: 87.4% versus 78.3% among municipal schools, and 72.2% versus 62.8% among subsidised private schools. All 42 rebuilt cells fall within the display tolerance (the margin allowed by published rounding), although the effective number of observations does not match the printed N. The magnitude survives; the exact universe does not.
{: .text-justify}

This describes selection (who belongs to each group), not effects. With data from 2002 to 2012, Paredes and Fresard associate lower enrolment by grade with a greater probability of closure and study where pupils go afterwards.[^paredes2018] Núñez, Solís, and Soto examine two rural communities in southern Chile after the 2010 earthquake and show that how a school is closed matters to social cohesion.[^nunez2014] My panel (data that follow the same units over time) cannot establish those findings: it observes administrative flows, not motives, later trajectories, or community life.
{: .text-justify}

Several smaller results survived too: **10 of the 11 published fixed effects** (the model's average coefficients), the SIMCE gap among closing subsidised schools, seven municipalities above a mobility threshold, and the negative sign of the relation between concentration and mobility. Including the constant, there are 12 coefficients in the file, 11 effects in the table, and 10 matches.
{: .text-justify}

{: .table-caption}
**Table 1** — What happened to the 34 audited judgements

| Outcome | Judgements | Interpretation |
|---|---:|---|
| Correct match | 15 | Published and rebuilt evidence support the same claim, backed by a third source. |
| 2014 error | 10 | The producer or rerun backs the reconstruction and refutes the publication. |
| Known error in the 2026 output | 0 | Divergent routes remain sensitivity analyses and did not enter the canonical output. |
| Wrong on both sides | 1 | Neither document nor reconstruction represents the estimand (the exact quantity being measured) well. |
| Misleading match | 1 | Both sides agree because they inherit the same wrong definition. |
| Limit, non-numeric claim, or provenance | 7 | The evidence cannot name a winner, but it can say why. |

Counting by display answers a different question. Of 26 objects, twelve converge, ten have explained divergences, and four lack a numerical test; no divergence remains unexplained. I do not turn that inventory into an “accuracy rate”: an inequality, a rounding match, and literal equality are not the same test.
{: .small}

## Spoonful 2: who was wrong

A discrepancy between 2014 and 2026 does not identify who was wrong. It may come from transcription, code, sample, or estimand; with only “published” and “rebuilt,” each explanation can be invented after seeing the result.
{: .text-justify}

Clemens sets a conservative burden: “follow-up studies should be considered robustness checks until proven to be replications” (p. 4).[^clemens2015] This matters: Herndon, Ash, and Pollin isolated exclusion, coding, and weighting errors with Reinhart and Rogoff’s working spreadsheet.[^herndon2013] Christensen and Miguel argue that open data and materials make credibility assessable.[^christensen2018]
{: .text-justify}

I added a third column: 2014 artefacts (files that preserve a trace of the calculation)—Stata output, spreadsheets, and charts—and, where feasible, a rerun. The diagram operationalises the burden: custody, execution receipt, prior comparison, and attribution. The three inputs stay separate so a repair cannot rewrite historical evidence. The third column did not always favour the present.
{: .text-justify}

<figure class="recreation-pipeline-figure">
  <a href="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-en.svg' | relative_url }}" target="_blank" rel="noopener">
    <picture>
      <source media="(max-width: 47.99em)" srcset="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-en-mobile.svg' | relative_url }}">
      <img src="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-en.svg' | relative_url }}" alt="Three input classes—pieces and data, descriptive statistics, and associational econometrics—pass through one shared chain of custody, execution, comparison, and attribution before the result is classified and the causal boundary declared." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 2.</strong> The anti-drift pipeline (a workflow that prevents silent changes). A failed gate (a control that must pass before proceeding) stops the claim; an apparent match does not fill the gap. Reproducible D2 sources: <a href="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-en.d2' | relative_url }}">desktop</a> and <a href="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-en-mobile.d2' | relative_url }}">mobile</a>.</figcaption>
</figure>

The sequence matters for public policy. Change the definition of exit, the sample, or the comparison precision, and an administrative flow can resemble system decline; run a model without preserving the same vector (the same ordered list of values), and green certifies execution only. The awkward rule is: **rerunnable does not mean rebuildable; rebuildable does not mean matching; matching does not mean correct; correct does not mean causal**.
{: .text-justify}

### Where my 2014 self was wrong

The cleanest case sits in the hierarchical model. The table reports **0.003** for lagged mathematics SIMCE; the Stata output that produced it prints **0.001**. Re-estimation gives 0.000533 in both Stata and Python, which rounds to 0.001. Seven alternative explanations were refuted. This was neither translation nor precision: it was transcription.
{: .text-justify}

In the same family of models, two rows labelled as variances (measures of dispersion) were the log standard deviations printed by Stata, left untransformed and crossed. The table reported 3.82 as the “intercept variance” and 2.791 as the “residual variance”; the corresponding variances were 2,079.7 and 265.6. Elsewhere, 0.4142 became 1.4142. Sometimes archaeology finds a sophisticated mechanism; sometimes it finds a copy-and-paste error.
{: .text-justify}

The concentration index produced the error with the largest interpretive consequence for public policy. The Herfindahl–Hirschman index (HHI, a measure of how concentrated supply is) runs from 0 to 10,000 and uses 2,500 as the high-concentration threshold. My spreadsheet stored the index times one hundred; the text read it as if it were times one thousand. Santiago therefore appeared around 1,534 when the canonical value was roughly 152.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" title="Figure 3 — Concentration and mobility" aria-label="Open Figure 3 enlarged">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" alt="At left, the 2014 concentration figure on an axis from 0 to 100. At right, the reconstruction on the canonical 0 to 10,000 scale, with a negative slope and p equal to 0.084." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figure 3</strong> — Concentration and mobility. The negative sign survives, but the slope is no longer distinguishable from zero at 5% (p = 0.084; under the model, the p-value summarises how incompatible the data are with a zero slope). The published scale would label 318 of 337 municipalities highly concentrated; the canonical scale labels 66.</figcaption>
</figure>

The spreadsheet even preserved the threshold formula: `=C2>2.5`. On its scale that means 250 canonical points, not 2,500, and selects 330 of 346 municipalities. A filter that passes 95% of cases is not filtering very much.
{: .text-justify}

Another nearly correct result concealed a different definition. The text said that intermediate and small cities—fewer than 15,000 inhabitants—accounted for about 80% of mobility in six regions. The figure's recipe split regional capitals from the rest and yielded 78.3%. Applied literally, the population threshold yielded 11%. The number was close; the sentence described another partition.
{: .text-justify}

### Summary of key findings

{: .table-caption}
**Table 2** — Differences that change the interpretation, and whose error they were

| Object | Published in 2014 | New evidence | Verdict |
|---|---|---|---|
| Lagged SIMCE, hierarchical model | 0.003 | Output and two engines: 0.001 | 2014 error |
| Model variances | 3.82 and 2.791 | They were crossed log standard deviations | 2014 error |
| Subsidised-private coefficient | 1.4142 | Output: 0.4142 | 2014 error |
| Municipal HHI | Santiago ≈ 1,534 | Canonical scale ≈ 152 | 2014 error |
| “Fewer than 15,000 inhabitants” | ≈ 80% | Capital/non-capital: 78.3%; population: 11% | 2014 error |
| Pupils per teacher | 48 cells | `rad`: 48/48; alternative calculation separated | Producer vector verified |
| SIMCE gap, closing subsidised schools | −4.3 | Producer sheet: −4.3 | Producer value verified |
| Gross mobility and rates | 6.3; 4.5; 1.6 | Producer formulas: 80/80 and 40/40 points | Correct final match |
| Net mobility | Entries − exits | Workbook and embedded chart: 80/80 points | Correct final match; causal interpretation unproven |
| PSU gap | ≈ 10 | Final result: 10.40, not 11.25 | Correct final match |

The most suggestive new finding was not quantified in the thesis. The pupil–teacher ratio among exiting schools falls from 17.95 to 12.22 over the previous seven years, against 20.31 among incumbents (schools that remain in the register). This does not look like an instantaneous collapse but a prolonged thinning-out visible retrospectively across the previous seven years. The label is retrospective: it marks the entire prior history of a school that later disappears.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" title="Figure 4 — The shadow of death" aria-label="Open Figure 4 enlarged">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" alt="Series with confidence intervals for pupils per classroom teacher among exiting schools: a fall from 17.95 to 12.22 over seven years, against 20.31 among incumbents." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figure 4</strong> — The “shadow of death”: fewer pupils per teacher during the seven years before exit. This is a descriptive pattern conditioned by the timing-marker problem, not a causal estimate.</figcaption>
</figure>

That figure is relevant to public policy precisely because it does not promise what it cannot observe. A gradual deterioration raises questions about early warning, enrolment, staffing, and institutional response; it does not show that a particular intervention prevents closure or that closure causes the deterioration.
{: .text-justify}

## Spoonful 3: what is ready to be extended through 2025

**This was the test I needed before adding thirteen years: not that every 2014 number survived, but that I knew exactly what I was extending.** Every available computational route ran again; that did not make every result equal. Three distinctions make sense of that result. Rerunnable means the route finishes; rebuildable, that it produces a comparable object again; matching, that it passes a pre-specified criterion (fixed before looking at the result). Those are different claims.[^comparison]
{: .text-justify}

{% include evidence-carousel.html %}

{: .table-caption}
**Table 3** — What happened when I reopened the nine doubtful cases

| Outcome | Cases | What it permits me to say |
|---|---:|---|
| Match | 3 | Table 4 reproduces 12/12 cells; Figures 3 and 4 reproduce 40/40 and 80/80 points. |
| Mismatch | 2 | Tables 5 and 8 fail their pre-specified criterion. |
| Not comparable by design | 4 | The route ran, but no common series or vector survives; pixel distance would answer another question. |

Table 5 recovers N=30,484 and `duracion3`, but only 10 of 20 coefficients and 11 of 20 standard errors equal the printed rounding. Table 6 retains 35 of 41 magnitudes; Table 7, 10 of 11 fixed effects, except 0.003 versus 0.001. In Table 8, only 4 of 12 match under rounding; eight appear truncated (decimals cut off rather than rounded). “Close” and “equal at published precision” are not synonyms.
{: .text-justify}

Python rebuilt the tables and figures; a fresh run invoked Stata 17 through `stata-mp` and completed 14 active routes, including the governed recovery of `do_058`, `do_059`, and `do_060`.[^stata17][^harvest] The result is a **traceable present-day rerun**, not historical equivalence: it shows that the chain can be traversed today, not that this was the 2014 session.
{: .text-justify}

I also keep two inventories separate. The registry tested **50 hypotheses**: **37 were refuted, 11 sustained, 1 partial, and 1 refuted for eleven of fourteen terms**. The editorial balance contains **34 judgements**. Hypotheses count explanations tested; judgements count published claims and objects. Neither is an accuracy rate for the other.
{: .text-justify}

I did not undertake this archaeology to acquit or condemn my 2014 work. Before constructing 2013–2025, I needed to separate what I could produce again, what was wrong, what was a sensitivity analysis (an alternative result under a different decision), and what could not be compared. I also wanted to subject a thesis that took considerable effort to complete to today's tools. Its failure to emerge intact makes the exercise more useful.

What matters is not vindicating the original, but reaching Post II with an auditable 1992–2012 base, corrected known errors, and visible limits. Now adding thirteen years makes sense: not to prolong a series, but to learn what changed with the rules and what it means for a school to enter or leave the system.
{: .text-justify}

## Closing, preparing for 2025

The thesis ended up divided into results that survive, 2014 errors, a canonical 2026 output with no known errors, and cases with no valid comparison. That partition shows what to retain and what not to carry into 1992–2025.
{: .text-justify}

The general direction of reallocation between 1992 and 2012 survives: municipal loss and subsidised-private expansion. Greater vulnerability among schools that later close also survives, **only for the reconstructed Greater Santiago universe**. The scale of the concentration index, the literal reading of “fewer than 15,000 inhabitants”, two variances, several labels, and one key timing definition do not. Discrepancies found in the present route were iterated until the canonical output had no known errors; alternatives remain visible as sensitivity checks, not as the reconstruction.
{: .text-justify}

{: .table-caption}
**Table 4** — What public use survives, and where the evidence ends

| Result | Reasonable public use | What it does not authorise |
|---|---|---|
| Reallocation across sectors, 1992–2012 | Historical diagnosis of sectoral change | Causal attribution to a reform |
| Vulnerability in the reconstructed Greater Santiago universe | Questions about protection and educational continuity | Generalisation to Chile or effects of closure |
| Pupil–teacher ratio before exit | Retrospective hypothesis for designing a warning system | Presenting it as a current classifier or validated alert |
| Corrected HHI | Describing concentration on the correct scale | Inferring the effect of competition on closure or mobility |

The second part cannot add thirteen rows and pretend continuity. A school in the 1980s, one in the 1990s, one after SEP, one under Inclusion, and one transferred to a Local Education Service do not face the same market or the same state. A series can execute flawlessly and answer another question: public policy's most elegant false green.
{: .text-justify}

### From describing closure to identifying a policy

The reconstruction leaves a panel that can describe flows, recognise risk signals, and re-estimate associations. It does not observe why each school closed, what would have happened without a reform, or the individual trajectories of its pupils. More controls, fixed effects, sophisticated standard errors, or compute can reduce some biases; **they do not create the missing counterfactual** (what would have happened without the reform or closure).
{: .text-justify}

For the extension through 2025 to produce useful social-policy evidence, the second post will have to distinguish three routes rather than sell them as interchangeable:

<div class="causal-routes causal-routes--en" markdown="1">

| Route | Question and design | Gate it must pass |
|---|---|---|
| **Descriptive/predictive warning** | Model transitions among active, zero enrolment, recess, official closure, and absence from the register; estimate out-of-sample risk (in years or cases not used to fit the model). | Temporal validation, calibration (predicted risk should resemble observed frequency), decision thresholds, and a distributive audit. It can guide monitoring; it does not estimate effects. |
| **Staggered reform** | Evaluate changes associated with transfer to Local Education Services using difference-in-differences (comparing changes between affected and unaffected groups) and a cohort event study. | Verified dates and exposure; plausible parallel trends (similar pre-reform evolution), anticipation, composition, and spillovers. If rollout timing responded to risk, the design is not causal by decree. |
| **Consequences of closure** | Link pupil trajectories and compare continuity, distance, attendance, attainment, and dropout through an event study or matched difference-in-differences. | Cause of closure, genuinely comparable controls, and plausibly exogenous variation (not determined by the outcome); matching alone does not remove selection. |

</div>

There is, however, a question that comes before econometric design. In a system where providers enter and exit, so-called **“creative destruction”** (replacing those that leave with new providers) may renew supply, displace lower-performing schools, or move pupils towards better alternatives. But the balance cannot be assessed only by observing which school disappears and which takes its place. Chilean evidence also points to costs of closure in grade repetition and dropout, as well as community effects that do not fit neatly into an enrolment count.[^grau2018][^nunez2014]
{: .text-justify}

That changes the public-policy question. The objective is neither to prevent every closure nor to assume that preserving every school is always preferable. It is to determine **who absorbs the cost of transition**: which pupils must move, where they arrive, how much farther they travel, what happens to attendance, learning, and persistence, and what a community loses when an institution that organised part of local life disappears. Available seats are necessary; they do not necessarily exhaust those costs.
{: .text-justify}

That is where I want to take Post II: extend a base whose construction and failures I now understand, distinguish institutional changes from changes in the register, and observe individual trajectories that the 2014 thesis could barely see. They matter in themselves and for what each pupil contributes to their surroundings.
{: .text-justify}

The open question is less comfortable than counting entries and exits: **when does creative destruction genuinely renew educational supply, and when does it merely shift its costs onto pupils, families, and territories with less capacity to absorb them?**
{: .text-justify}

The final irony is that the school market changed rules faster than AI and left worse release notes. An RBD (the school's official identifier, or database registration number) may disappear from the register. **A pupil's trajectory does not restart when that happens.**
{: .text-justify}

---

## References

[^tesis]: Labra Olivares, Cristián A. *Patrones de entrada y salida de establecimientos educacionales en Chile (1992-2012)*, master's thesis, Universidad de Chile, 2014. Advisor: Daniel Hojman T.

[^grau2018]: Grau, N.; Hojman, D.; Labra, C.; Mizala, A. [*Destructive Creation: School Turnover and Educational Attainment*]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}), working paper 396, 2014; Grau, Hojman, and Mizala, [*School closure and educational attainment*](https://doi.org/10.1016/j.econedurev.2018.05.003), 2018.

[^paredes2018]: Paredes, Ricardo D.; Fresard, Matías. *Voucher y cierre de escuelas en Chile*, *Estudios Públicos* 151, 7–27, 2018.

[^nunez2014]: Núñez, Carmen Gloria; Solís, Camila; Soto, Rodrigo. [¿Qué sucede en las comunidades cuando se cierra la escuela rural?](https://doi.org/10.11144/Javeriana.UPSY13-2.qscc), *Universitas Psychologica* 13(2), 615–625, 2014.

[^regimenes]: Biblioteca del Congreso Nacional de Chile. [History of Law No. 3,063](https://www.bcn.cl/historiadelaley/historia-de-la-ley/vista-expandida/8363/); [Law No. 19,247](https://www.bcn.cl/leychile/navegar?idNorma=127911); [Law No. 20,248](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=269001&idVersion=); [Law No. 20,845](https://www.bcn.cl/leychile/Navegar?idNorma=1078172&idParte=9605200&idVersion=2222-02-02); [Law No. 21,040](https://www.bcn.cl/leychile/Navegar?idNorma=1111237&idParte=9853075).

[^christensen2018]: Christensen, Garret; Miguel, Edward. [Transparency, Reproducibility, and the Credibility of Economics Research](https://doi.org/10.1257/jel.20171350), *Journal of Economic Literature* 56(3), 920–980, 2018.

[^clemens2015]: Clemens, Michael A. [The Meaning of Failed Replications: A Review and Proposal](https://doi.org/10.1111/joes.12139), *Journal of Economic Surveys* 31(1), 326–342, 2015.

[^herndon2013]: Herndon, Thomas; Ash, Michael; Pollin, Robert. [Does high public debt consistently stifle economic growth?](https://doi.org/10.1093/cje/bet075), *Cambridge Journal of Economics* 38(2), 257–279, 2013.

[^hamermesh2007]: Hamermesh, Daniel S. [Viewpoint: Replication in economics](https://doi.org/10.1111/j.1365-2966.2007.00428.x), *Canadian Journal of Economics* 40(3), 715–733, 2007.

[^stata17]: Technical receipt pinned at commit `0e9e02d4316d120336d6c2af26434beb5d4b24e0`: 15/15 roles with zero `r(NNN)`, Stata 17 with `c(MP)=1`, `c(flavor)=IC` reported separately, and four historical roots intact.

[^comparison]: Terminal comparison pinned at `tesis_mae_mejorada@a8ee6ac`: nine reopened cases, four inferential families, and separate thresholds for tables, raster images, and equivalence.

[^harvest]: Output harvest pinned at `tesis_mae_mejorada@cd6d19b`: directed reruns of `do_058`, `do_059`, and `do_060`, four validated data products, and separate limits for smoke tests and graphs that were never exported.
