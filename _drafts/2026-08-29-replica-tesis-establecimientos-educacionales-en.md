---
layout: single
title: "Replicating my own thesis in 3 spoonfuls: is the error from 2014, or is it mine today?"
subtitle: "I rebuilt the master's thesis I wrote on school entry and exit in Chile's voucher market, and built the machinery I needed in order not to be able to rule in my own favour"
date: 2026-08-29 09:30:00 -0400
categories: [datos, educacion, politica-publica]
tags: [replication, education, school-markets, voucher, mineduc, duration-analysis, vulnerability, audit]
description: "In 2026 I rebuilt my 2014 master's thesis on the entry and exit of schools in Chile and decided, cell by cell, whether each difference was right, wrong or unknown. Two columns cannot do that: it took a third —my own 2014 artefacts and the Stata engine re-executed— and a taxonomy that told four different kinds of not-knowing apart."
excerpt: "Auditing yourself is easy to say and hard to sustain: you hold the last word on every cell. This is the machinery I built to take it away from myself, and the three verdicts that ended up ruling against me."
author: clabra
lang: en
ref: replica-tesis-establecimientos-educacionales
permalink: /datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/
header:
  teaser: /assets/images/teasers/teaser-replica-tesis.webp
  og_image: /assets/images/replica-tesis-establecimientos/og-replica-tesis-1200x630-en.webp
  og_image_alt: "Side-by-side comparison of the market concentration and school mobility figure between the 2014 thesis and its 2026 replication"
math: true
toc: true
toc_sticky: true
comments: true
author_profile: true
---

In April 2014 I submitted a master's thesis on the entry and exit of schools in Chile between 1992 and 2012.[^tesis] I wanted to extend that series to 2025 and ran into the natural order of the problem: before extending my own work, I had to be able to reproduce it.
{: .text-justify}

What follows is that first half, and the problem turned out to be less technical than it looked. Rebuilding the eight tables and the figures was work; deciding **whose difference each one was** was the problem. Because the judge was me, over my own work, holding the last word on every cell.
{: .text-justify}

Auditing yourself has a trap that good intentions do not solve: when the reconstruction and the original disagree, the comfortable explanation is always available. So half of this work was not measuring but building the machinery that would stop me from ruling in my own favour: a third column to decide in my place, a taxonomy that told **right, wrong and unknown** apart instead of piling them together, and checks I broke on purpose to verify they could fail.
{: .text-justify}

Halfway through, twelve 2014 artefacts turned up —Stata outputs, sheets from my working spreadsheet, a chart embedded in the manuscript— and later I re-ran the original engine over the original data. That third column is what separates an agreement from a truth.
{: .text-justify}

**The thesis is mine and so is the audit**, so this is not an independent replication: I am reviewing decisions I made myself and that seemed reasonable at the time.
{: .text-justify}

The incentive runs both ways —indulgence toward my 2014 self, or severity to look rigorous— and the only thing holding it in check is one rule: I do not accept any discrepancy I cannot show. Hence a post with more side-by-side tables and figures than prose.
{: .text-justify}

A second conflict to declare. Grau, Hojman and Mizala published a 2018 article on school closure and educational attainment in the Chilean system.[^grau2018] As I recall, its acknowledgements mention my contribution at early stages; **I have not managed to verify that with the material in front of me**, so I record it as a recollection, not a fact.
{: .text-justify}

If it is accurate, it serves me as credential and as bias at once. Daniel Hojman, moreover, was my thesis advisor.
{: .text-justify}

## Reading contract

| Concept | What it means here | What it does not mean |
|---|---|---|
| **Replication** | Producing my figures, tables and estimates again from the data, with new code. | Recovering the 2014 run: environment, temporary files and the real order of my commands **were not recovered**. |
| **Discrepancy** | A rebuilt cell that does not match the printed one. | An error: it may sit in the document, in my replication, or in the chain joining them. |
| **Entry / exit** | A school appearing in, or dropping out of, the official register. | Opening or failure as a decision: I observe the flow, not the motive. |
| **IVE** | Chile's school vulnerability index: share of enrolment classified as vulnerable. | Household poverty, or an individual measure of any pupil. |
| **Producer** | The 2014 artefact that generated a figure: a Stata output, a sheet of my working spreadsheet, the chart embedded in the manuscript. | The run that created it: that is still lost. |
| **Re-execution** | Running the 2014 `do-file` again under Stata 17 MP over the original `.dta` files, and comparing against what was published. | The 2014 run: the actual order of my commands was never recovered. |
| **Measured ceiling** | How far a search that found nothing actually got: "2 of 20 coefficients across 142 documents", not "it did not turn up". | An excuse: it is the number that separates *searched and absent* from *never searched*. |
| **Traceable claim** | A statement tied to a verifiable artefact and its hash. | An opinion of mine. |

**Scope.** I work from the 2014 PDF, its LaTeX source and my `do-files`. Nothing below is causal: these are conditional associations within a panel, with no identification strategy behind them.
{: .small}

## Spoonful 1: what I rebuilt, and what the rebuilt things mean

Chile funds schooling with a per-pupil subsidy that follows the student, so three types of provider coexist: municipal, publicly funded private, and fee-paying private.
{: .text-justify}

That makes entry and exit measurable: if the money moves with enrolment, supply can reorganise itself without anyone decreeing it. My thesis set out to describe that reorganisation.
{: .text-justify}

The computing side is anecdotal and I dispatch it in two lines: the document no longer compiled —`utf8x` and `harvard` were withdrawn from LaTeX— and translating the code to Python forced me to check every estimate against Stata. What matters is what showed up once I looked at the objects.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad-en.webp' | relative_url }}" alt="On the left, the total mobility by administrative dependency figure published in 2014, with bars stacked by year from 1993 to 2012. On the right, the 2026 replication with the same flows pooled over the period: municipal 346 entries and 1,135 exits, publicly funded private 1,468 entries and 597 exits, fee-paying private 354 and 337." loading="lazy" decoding="async">
  <figcaption><strong>Figure 1</strong> — Total mobility by dependency: the 2014 original and my replication, which pools the twenty years so the balance reads in one glance. The totals on the right add up to 2,168 entries and 2,069 exits; the spreadsheet I built that figure with in 2014 says 2,160 and 2,065, which is exactly what got published. Panel labels are in Spanish, as in the source.</figcaption>
</figure>

Laid out that way, the flows say something the year-by-year stack was hiding: **the reallocation has a direction**. The municipal sector loses schools (346 entries against 1,135 exits) and the publicly funded private sector gains them (1,468 against 597), while fee-paying private roughly breaks even. This is not a market that grows: it is one that changes hands.
{: .text-justify}

The second object I rebuilt measures the share of vulnerable enrolment by dependency and closure status, in Greater Santiago. I put it against the published version at its totals row.
{: .text-justify}

{: .table-caption}
**Table 1** — Share of vulnerable enrolment, totals row: published in 2014 against my reconstruction

| Dependency | Status | Published | Rebuilt | Difference | N |
|---|---|---:|---:|---:|---:|
| Municipal | No closure | 78.3 | 78.347 | +0.047 | 2,815 |
| Municipal | Closing | 87.4 | 87.429 | +0.029 | 74 |
| Publicly funded private | No closure | 62.8 | 62.827 | +0.027 | 5,269 |
| Publicly funded private | Closing | 72.2 | 72.218 | +0.018 | 249 |
| Reported total | No closure | 68.4 | 68.386 | −0.014 | 8,246 |
| Reported total | Closing | 74.9 | 74.936 | +0.036 | 327 |

All 42 cells of the full table fall inside display tolerance, but the effective N I reproduce is not the published one: the row stays classified as a universe divergence, not as a match.
{: .small}

The substance of the table is more uncomfortable than its arithmetic: **the schools that close were serving, before closing, a systematically more vulnerable intake than those that stay open**, and that holds within each dependency, not only between them. Nine points in the municipal sector, almost ten in the publicly funded private one.
{: .text-justify}

That describes selection, not an effect: I do not observe what would have happened to those pupils without the closure.
{: .text-justify}

## Spoonful 2: an error of the past or an error of the present?

When a cell fails to match, what matters is whose error it is. Without an explicit criterion the discussion turns into a contest of opinions in which I always have the last word, which is exactly where an author auditing himself should not be.[^dewald]
{: .text-justify}

My criterion was to build an oracle. I reimplemented, under control and from a versioned snapshot of the code, the route that produces the descriptive tables, and ran it on Stata 17 against my Python version: **44 cells, maximum absolute difference of 3.6·10⁻¹²**.
{: .text-justify}

With a caveat that forced me to lower my voice: **the historical `do-file` was not executed**; what ran was a controlled reimplementation.
{: .text-justify}

A month later that caveat was half lifted. The 2014 run is still lost —environment, temporaries and the actual order of my commands— but I did re-estimate the final specification on the original engine, Stata 17 MP under my own licence, and something better than an oracle turned up: **the producer**.
{: .text-justify}

### Twelve artefacts of mine, found

Combing the source tree first surfaced five objects that produced the published numbers directly: the `outreg` output of the hierarchical model, two sheets of my working spreadsheet, a third with the SIMCE gap, and a chart embedded inside the manuscript with its series still in it. A second pass, this time crossing **every** document against **every** published figure, took the count to **twelve** artefacts serving as a third column —eleven certify some published figure and one turned out to measure something similar but different—. The search covered everything the tree keeps, and that matters as much as the find:
{: .text-justify}

{: .table-caption}
**Table 2** — Where the producer of each figure was searched for

| Corpus | Found | Read |
|---|---:|---:|
| Stata `.gph` graphs | 15 | 15 |
| `.doc` / `.docx` documents | 140 | 140 |
| `.xls` / `.xlsx` spreadsheets | 241 | 241 |
| Charts embedded in `.docx` | 290 | 290 |
| Sheets in the working workbook | 27 | 27 |

Five binary spreadsheets opened in no library and had to be decoded record by record; ninety-two documents came in the old Word format. Declaring coverage is what lets a «not found» read as data rather than as fatigue: there are two tables for which I **did** search the whole corpus and the producer **is not there**, and that is an answer, not a pending item.
{: .small}

That changes the question running through this post. Until here I was comparing **my reconstruction against the print**, and every discrepancy admitted the excuse that the reconstruction was the broken one. With the producer in view there is a third column —and in several cases my reconstruction looks more like my 2014 self's work than the text I published.
{: .text-justify}

Take the mobility figure: the shares in my spreadsheet sit **3.05 points** from the reconstruction and **13.41 points** from the printed text. My 2026 replication is 4.4 times closer to my own 2014 spreadsheet than my published document is.
{: .text-justify}

### The coefficient that did not come from my own output

My hierarchical model table publishes **0.003** for the lagged SIMCE mathematics score. The 2014 Stata output that produced that table prints **0.001**.
{: .text-justify}

It is not an engine difference: the other eleven coefficients of that same output match today's run to the fourth decimal, and between Stata and `statsmodels` the worst discrepancy across the fixed effects is 0.43 %. Nor is it an input problem: the SIMCE imputation the `do-file` declares is identical across both engines over 85,807 cells, with a maximum relative difference of 5.9·10⁻⁸ that comes from Stata storing in 32-bit `float`.
{: .text-justify}

I put the 0.003 through seven hypotheses of origin —another SIMCE specification among those the thesis itself pre-declares, another print precision, the imputed variable of the `do-file`, a transplant from another cell of the same table, the table's own decimal convention, the 2014 output itself, refitting on the original engine— and **all seven were refuted**. The estimate is 0.000533 on both engines, which rounds to 0.001 and not to 0.003.
{: .text-justify}

This is the finding that unsettles me most, because I cannot pin it on the translation to Python: the translation and the original agree, and the one that departs is the document.
{: .text-justify}

And it is not alone. In that same table the intercept variance is published as **0.001**; the output prints `lns1_1_2 = −3.160`, and $$e^{2\cdot(-3.160)}$$ gives **0.0018**, which rounds to 0.002. What makes this a finding rather than a suspicion are the **other two** variances in the same document, which do match: the residual gives 0.014010 against the published 0.01 and the slope 2.19·10⁻¹⁵ against 2.1·10⁻¹⁵. It is the two that agree that isolate the one that does not.
{: .text-justify}

### The table that publishes logarithms as variances

Combing the tree turned up a third output, `xtmixed_modelo_final.doc`, which reproduces **20 of the 21 values** of one of my hierarchical model's specifications. The document holds 24 numbers in total: there is no room for coincidence.
{: .text-justify}

And there sits the most conspicuous error I have found. The two rows the table labels as variances **are not variances**: they are the parameters Stata prints as the log of the standard deviation, copied without exponentiating. And they are crossed.
{: .text-justify}

{: .table-caption}
**Table 3** — The two variance rows of the hierarchical model, against the output that produced them

| Published row | Value | Standard error | Where it actually comes from | Actual variance |
|---|---:|---:|---|---:|
| Intercept variance | 3.82 | 0.002 | `lnsig_e`, which is the **residual** | 2,079.7 |
| Residual variance | 2.791 | 0.036 | `lns1_1_1`, which is the **intercept** | 265.6 |

The standard errors leave no room for interpretation: 0.002 sits beside 3.820 in the output and 0.036 beside 2.791, and in the table they appear paired the same way but under the opposite label.
{: .small}

In the same table, the publicly funded private coefficient was published as **1.4142** where the output prints **0.4142**. One digit.
{: .text-justify}

### The third column

Up to here this post compares **two** things: what I published in 2014 and what my reconstruction measures. With two columns, «they match» and «it is right» are indistinguishable —a reconstruction that inherits the original's error produces a perfect green— and green is exactly what nobody looks at twice.
{: .text-justify}

When my own artefacts appeared, a third column appeared with them, and with it a verdict that is **derived** rather than written:
{: .text-justify}

{: .table-caption}
**Table 4** — The 34 judgements over the document's 26 objects

| Do published and reconstruction match? | Which one is right? | Verdict | Judgements |
|---|---|---|---:|
| no | the reconstruction | error of the past | 10 |
| yes | both | correct match | 10 |
| no | **what was published** | **error of the present** | 3 |
| yes | **neither** | **inherited match** | 1 |
| no | neither | both wrong | 1 |
| — | *could not be settled* | (see Table 5) | 9 |

Twenty-five of the 34 have a third source. The deciding column comes from my own producer in 18 cases, from a Stata re-execution in 4, from an external disciplinary standard in 2, and from an internal contradiction in the text itself in 1.
{: .small}

### Four ways of not knowing, and only one is laziness

For months that last row read **thirteen unadjudicated**, and read that way they looked like thirteen identical holes. They were not, and confusing them was my error, not 2014's.
{: .text-justify}

Once I finally separated them, it turned out «I don't know» means four different things, and only one of them is work left undone:
{: .text-justify}

{: .table-caption}
**Table 5** — Why it was not settled, which is different from how many were not settled

| Reason | What it means | Judgements |
|---|---|---:|
| **Limit with a measured ceiling** | It was searched for, and the number saying how far the search got is on record. | 4 |
| **The claim is not numeric** | The text asserts a shape —«partly opposite paths»—, not a magnitude. | 3 |
| **Provenance verified** | The only claim about that panel is the code that produced it, and its hash checks out. | 2 |
| **Route declared and never run** | There is a written path and nobody walked it. This one *is* laziness. | **0** |

The distinction is not cosmetic. A limit with a ceiling says "searched across 142 documents, and the best candidate reproduces 2 of 20 coefficients"; without that number, "it did not turn up" is indistinguishable from "I never looked".
{: .small}

That last zero took three weeks and is the only thing in this post I let myself celebrate. It does not mean everything is settled: it means **nothing was left without saying why**.
{: .text-justify}

The inherited match is what justifies the whole apparatus, and it is the concentration index: the published figure says 1,534 and my reconstruction measures 1,517.5, a 1.3 % difference. **They match, and both are wrong**, because my reconstruction adopted my 2014 self's scale without asking where it came from.
{: .text-justify}

The duration model needed its own check, and that is where it got interesting. I model the probability that a school exits in year $$t$$ given that it was still open, with a complementary log-log link, the standard specification when the event is observed by periods rather than in continuous time:[^jenkins]
{: .text-justify}

$$
h(t \mid x) = 1 - \exp\!\left[-\exp\!\left(x'\beta + \gamma(t)\right)\right]
$$

On a synthetic case, Stata and `statsmodels` agree on the coefficients to $$1.0\cdot 10^{-7}$$ and on the log-likelihood to $$3.6\cdot 10^{-14}$$, but **their standard errors differ by up to 0.025**: Stata's match the observed-Hessian errors exactly and Python's default ones do not.
{: .text-justify}

The coefficients are the finding; the standard errors are the stars. The first matching does not guarantee the second. 🙂
{: .text-justify}

With the oracle working I could adjudicate the two significance errors. Neither survives rounding, because the deciding statistic is a ratio between two numbers printed in the same cell:
{: .text-justify}

$$
|z| = \frac{|\hat\beta|}{\operatorname{se}(\hat\beta)}
$$

{: .table-caption}
**Table 6** — The two cells whose asterisks do not add up

| Table and term | Published | Rebuilt | Published standard error | max \|z\| | Asterisks printed | Warranted |
|---|---:|---:|---:|---:|:--:|:--:|
| Table 6, spec. 1 — Closure dummy | −5.0907 | −5.090749 | 1.2147 | 4.19 | 1 | 2 |
| Table 8 — Intercept variance | 0.008 | 0.008745 | — | 2.43 | 2 | 1 |

The rebuilt coefficient matches to the sixth decimal: the discrepancy is in the star, not in the estimate.
{: .small}

The first one's confusion did not stay inside the table. The preceding paragraph reads that coefficient as insignificant and the following one reads it as significant, on the same page. It is a 2014 error and it is mine.
{: .text-justify}

There is a third kind I cannot assign to anyone. In my LaTeX source the «Observations» rows of the four regression tables are **empty** and N travels separately: I typeset those tables by hand instead of exporting them.
{: .text-justify}

That does not prove any figure is wrong —most match— but it cuts the chain between estimate and print: a discrepant cell may be a crooked transcription or a different input.
{: .text-justify}

The co-payment table carries an exact example of that broken chain. Its footnote publishes **N = 5,465**, which is the total of one panel; the means printed above it come from another, of **5,022**. Both numbers are mine and they travelled separately onto the same page.
{: .text-justify}

And a number I would rather not write: of the **30 revision proposals** this audit produced, only **12 today carry a traceable claim with its hash**. The other 18 are labelled proposal or unverified, and that is how they must be read. Anyone taking all 30 as findings has read this post backwards.
{: .text-justify}

## Spoonful 3: the findings that change a reading

**1. My exit marker did not mark exits.** The variable `id_salida` correlates −0.977 with the calendar year: it falls from 1,676 flagged cases in 1992 to exactly 0 in 2012, while effective exits range between 42 and 290 with no trend (ρ = +0.382). It does not say «closed», it says «will close in some year within the window»: a school closing in 2011 is flagged in every prior year and in none after.
{: .text-justify}

It contaminates the three descriptive tables and the definition of the event in the duration model.
{: .text-justify}

**2. My duration variable measures observed tenure, not institutional age.** The panel starts in 1992 and schools that already existed enter left-truncated, which I did not declare; on top of that I imposed a linear shape on the baseline hazard. Measured year by year that slope is +0.018 percentage points a year with p = 0.27: I cannot tell it from zero. It is not a matter of form, because the baseline hazard is precisely what the model uses to separate the effect of time from that of the covariates.
{: .text-justify}

**3. The co-payment averages eight years of nominal pesos without deflating.** Here the producer turned up too, and with it the universe: the 2014 working sheet prints 17,051.23 and 9,665.54 pesos, and exactly one of the ten panels reproduces it —to **0.00 and 0.005 pesos**, while the wide panel departs by 910.60 and 162.68. On that universe the crude entrant-exiter gap is \$7,385.7; computed within each year and then weighted, \$6,655.7: **\$730.0, some 9.88 %, was temporal composition** and not a difference between schools.
{: .text-justify}

The finding survives; the magnitude does not —and it is smaller than the one I had measured myself on the wide panel (\$1,009.4, 12.41 %), the panel the 2014 sheet rules out as the universe. Underneath there is something better: the gap moves from \$8,175.8 in 2004 to \$2,481.3 in 2011. **It falls to less than a third**, and my pooled average erased exactly that.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh-en.webp' | relative_url }}" alt="On the left, the figure published in 2014 relating the municipal Herfindahl index to total mobility, with the horizontal axis running from 0 to 100. On the right, the 2026 replication on the canonical 0 to 10,000 axis, measured with the variable the do-file labels as the index: a negative slope, p = 0.084 over 337 municipalities." loading="lazy" decoding="async">
  <figcaption><strong>Figure 2</strong> — Municipal concentration and mobility. The same index appears on three scales: the original's axis stops at 100, the text cites levels from 1,180 to 1,534, and the canonical definition runs from 0 to 10,000 with 2,500 as the high-concentration threshold. The replication is measured with `hhi_n_alumnos`, the variable the `do-file` itself labels as the index: the slope stays negative, but over 337 municipalities it is not distinguishable from zero at 5 % (p = 0.084).</figcaption>
</figure>

**4. The concentration index runs on a scale ten times its own, and I know why.** The Herfindahl index is defined between 0 and 10,000. The variable my own `do-file` labels «Herfindahl-Hirschman Index» reproduces the five levels I named explicitly with **1.34 % mean error** —Santiago gives 1,517.5 against the 1,534 published— but it does so multiplied by one hundred thousand: **ten times the canonical scale**. On the correct scale Santiago measures 151.7. This is not a decimal: read as I published it, **318 of 337 municipalities** would sit above the high-concentration threshold; on the canonical scale it is **66**. It changes which market gets called concentrated.
{: .text-justify}

The mechanism was in my spreadsheet. The index column runs from 1.1756 to **exactly 100**, and that maximum is no accident: it is the municipality with a single school, where the raw index equals 1. The column is the raw index **times one hundred**. Writing the text, I read it as if it were in thousands, and that is where the five published levels come from: the sheet times a thousand.
{: .text-justify}

That reading did not stay in the text. On another sheet of the same workbook I left the high-concentration threshold written as `=C2>2.5`, which on the spreadsheet's scale is 250 canonical points and not 2,500. It selects **330 of the 346 municipalities**; the real threshold selects **84**. A filter that passes 95 % of the cases is not filtering anything.
{: .text-justify}

Here I correct myself twice, and the second one stings. First, I measured concentration with **another column** of the panel, not the one the `do-file` labels as the index; the error gives itself away, because its ratio against the published values was almost constant —10.3, dispersion 0.03— the signature of comparing against something proportional but different.
{: .text-justify}

Second: with that column the descriptive contrast gave a negative and significant slope (p = 0.009, 336 municipalities). **Redone with the `do-file`'s own variable, the sign stays negative but the slope is no longer distinguishable from zero at 5 % (p = 0.084, 337 municipalities).** What still stands is that my municipal exits model reported a positive coefficient and the descriptive cloud does not back it; what falls is the force with which I asserted it.
{: .text-justify}

The direction survives a second check that depends on no regression at all: splitting municipalities at the canonical threshold, the concentrated ones average **1.66 %** annual mobility and the rest **2.01 %**. More concentration, less mobility. The sign is my reconstruction's and not my 2014 model's; what there still is not, is significance.
{: .text-justify}

And that model stacks three identification problems: contemporaneous regressors my own text declares jointly determined, a lagged dependent variable under random effects,[^nickell] and inference over 15 clusters.[^cameron] With so few groups, the standard error stops being trustworthy before the coefficient does.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" alt="Series with confidence intervals of the pupil-per-classroom-teacher ratio of schools that close, from seven years before the last flagged year to that year: it falls from 17.95 to 12.22, against a horizontal line at 20.3 for incumbent schools." loading="lazy" decoding="async">
  <figcaption><strong>Figure 3</strong> — The shadow of death, measured: pupils per classroom teacher in exiting schools, by year relative to the last flagged year, against incumbents. Axis labels are in Spanish, as generated.</figcaption>
</figure>

**5. The «shadow of death» was measurable and I only named it.** The pupil-per-teacher ratio of exiting schools falls monotonically from **17.95 to 12.22** over the seven prior years, against **20.31** for incumbents. This is not a sudden collapse: it is a seven-year hollowing out. That changes the policy reading, because deterioration with that shape is observable while it happens.
{: .text-justify}

With the caveat from finding 1: the axis measures years relative to the last flagged year, and that marker turned out not to mean what I thought it did.
{: .text-justify}

**6. And one where the error is mine today, not in 2014.** Among my workbook's sheets one turned up called `rad` —pupil-teacher ratio— with **48 numbers**. The table I published has **48 cells**, and all of them are there: same year, same dependency, same closure status. What was published and its producer are identical.
{: .text-justify}

The one that falls short is my 2026 reconstruction: it diverges in **41 of the 48 cells**, by 0.63 points on average and 3.49 at worst. For months I counted that discrepancy as a divergence with no owner; with the sheet beside it, the owner is me, now.
{: .text-justify}

**7. The sentence describes a split the figure does not make.** One of my figures shows mobility by region, and the text claims that intermediate and smaller cities —«under 15 thousand inhabitants»— concentrate **80 %** of the mobility of six regions. The two recipes that produce that figure were sitting in my `do-file` waiting for a join nobody had performed; run, they give **78.3 %**.
{: .text-justify}

A point and a half of difference was not the finding. The finding appeared when I applied the criterion the sentence actually states: using the school-age population per commune that the panel itself imports, the fifteen-thousand threshold leaves the share at **11 %**, not 80 %. Not even a threshold five times looser gets there: communes on the order of seventy-five thousand inhabitants give 68 %.
{: .text-justify}

The figure does not split by population: it splits by **regional capital**, which is what its own caption says. Under that split the share is 78.3 %, and it holds: seven different definitions of the universe —with and without teaching markers, presence only, adding relevance, and both ways of saying "non-capital"— all land between 77.98 % and 78.34 %. Separating the flows does move the number, and in both directions: entries 70.1 %, exits 84.3 %. The 80 % I published is neither.
{: .text-justify}

What I wrote described one criterion; what I plotted used another. Nobody would have caught it reading the text, because the number is *almost* right.
{: .text-justify}

**8. The denominator nobody had named.** Another claim of mine says that, of 346 communes, only **seven** exceed 5 % mobility over their stock. My 2014 spreadsheet said **ten**. For months I did not know which to believe, because "mobility over stock" does not say what quantity does the dividing.
{: .text-justify}

The answer was in the `do-file`, across four lines separated by twenty: the denominator is the count of schools **per commune and year**, averaged afterwards by commune. Run in Stata over the 2013 `.dta` files, the recipe gives **exactly seven**, and with room to spare: the seventh commune sits at 5.10 % and the eighth at 4.37 %. The seven does not depend on where the cut is placed.
{: .text-justify}

One minor discrepancy remains, which I declare rather than hide: the recipe yields **345** communes and my text cites 346.
{: .text-justify}

One debt left is not an error but an absence: the Schumpeterian frame organises my title, my abstract and my conclusion, but I never tested it. The reallocation decomposition separating improvement within incumbents from that coming from entry and exit —the standard in the very literature I was citing— is not in the document.[^griliches]
{: .text-justify}

## Where the audit landed

Twenty-six objects between tables and figure panels. Ten reproduce what was published; eleven diverge with a measured mechanism —a label, a universe, a scale, a rounding convention—; **none is left diverging without an explanation**; five admit no numerical test, and none of those five for want of work: three assert a shape with no magnitude to be measured against, and two have as their only claim the provenance of their code, already verified by hash.
{: .text-justify}

Behind those verdicts sit **51 hypotheses put to the test**, of which 40 were refuted and 9 survived. I record the refuted ones alongside the survivors on purpose: an audit that only publishes what it confirmed is not an audit, it is a selection.
{: .text-justify}

That per-object count, however, reads for more than it is, and it is worth saying why. **Convergence does not mean the same thing everywhere.** Of the nine prose claims that converge, only **three** do so at the precision they are printed at —half a unit of the last digit—. Four converge within the 15 % relative margin the text itself claims by writing «approximately», and two are inequalities: the text says «reaches» and the reconstruction satisfies it as a bound. Counting all nine as greens reads for more than it is.
{: .text-justify}

### The 2014 engine as judge

What settled the last judgements was not a new artefact: it was **running the original engine again**. Stata 17 MP, over the `.dta` files from 2013 and 2014 that survived, executing my `do-file`'s commands exactly as written —with the version prefix, because the `table` syntax of the time no longer exists—.
{: .text-justify}

That is a third column in its own right, and it settled four judgements. In two it confirmed what I published: the SIMCE gap for closing voucher schools comes out at 10.20 points with an interval excluding zero, and the seven communes are seven. In a third, the missing denominator. And in the fourth, what I least expected happened.
{: .text-justify}

### A judge that can also rule against me

At the end I put the 34 judgements through a rubric fixed in advance —a real third source, multiple agreement, a tolerance declared beforehand, a counterexample, contrary evidence— with explicit permission to lower a verdict already issued. It corrected **two**, and both were mine.
{: .text-justify}

The more uncomfortable of those two: I had declared that neither my 2014 model's sign nor my 2026 reconstruction's slope held up, and I had declared it leaning on a column that **my own registry describes as a different estimand** a few pages later. Redone with the definition that does reproduce what was published, the direction flips and the reconstruction lands on the right side. A judge that can only promote is not a judge.
{: .text-justify}

And the fourth re-execution case is of the same kind, but worse, because no rubric found it —arithmetic did. My reconstruction claimed the university-admission-test gap between closing and surviving voucher schools was **11.25 points**, against the 10 I published in 2014. I went back to it because the number felt large, and **no** recipe reproduces it: ten readings —ten panels across five universes, the mean of yearly gaps, the gap of medians, the absolute value of the exiting branch— all land between 8.15 and 10.40. The correct value is **10.40**.
{: .text-justify}

Corrected, the distance between my reconstruction and what I published eleven years ago drops from 1.25 points to 0.40. **The correction favours the 2014 document.** That is the kind of result you do not go looking for when auditing yourself, and precisely for that reason it is the one that has to be published.
{: .text-justify}

### A check that has never been seen red is not a check

None of the above is worth anything if the checks holding it up cannot fail. So the rule is to break them on purpose, verify they fail, restore them and verify they pass again, recording the concrete red case. There are **103 observed red cases** on record across 49 contracts; in this last round there were eleven.
{: .text-justify}

With a number I do not like and include anyway: of the project's **390 checks**, only **111 carry a recorded red case** —28 %—. The other 279 are declared as debt, not as green. A check without a red case is not a check: it is an intention.
{: .text-justify}

Two of those breaks taught more than the twenty-three that behaved. The first: **one check did not bite**. I added the Metropolitan Region —which under the same recipe gives 19.4 % where the six regions in the text give 78.3 %— to the region set of the mobility figure, and nothing went red. The check measured how much the result moved across definitions of the universe, but it did not pin down **which** the six regions were. A wrong set passed silently. I fixed it and broke it again; now it fails.
{: .text-justify}

The second came from earlier and is more uncomfortable: a check required that human review decisions remain pending. It went red exactly when the system was right —as the last one was resolved, a perfectly healthy queue failed—. A check being green does not say it is checking; sometimes it says it has never been given the chance to fail.
{: .text-justify}

## Closing: the second half runs to 2025

A second post will bring the recreation extended to 2025. The sources are already acquired —fourteen official MINEDUC collections, including the Official Directory 1992-2025— but I am not previewing figures: extending the window puts regime changes in the middle.
{: .text-justify}

What I take away is less technical than I expected. The confirmed errors are asterisks, scales and elementary arithmetic; the findings that move a conclusion came from looking at what my variables actually measured.
{: .text-justify}

And what surprised me most was not finding errors, but which side they turned up on. I started out assuming the reconstruction would be the weak link. Once my own 2014 artefacts appeared —the Stata output, the spreadsheet, the embedded chart— the reconstruction turned out to look more like them than the document I signed. Except in three cases, where the weak link is the reconstruction and now I know it.
{: .text-justify}

If I had to keep one thing out of all this, it would not be a finding but a habit: **decide the criterion before looking at the result, and write down what observation would knock it over**. It is uncomfortable to sustain and it is the only thing that stops auditing yourself from becoming an elegant way of agreeing with yourself. I held the last word on every cell of this document; the machinery exists to take it away from me.
{: .text-justify}

I am not closing this thinking the thesis was right or wrong. I am closing it knowing, cell by cell, **which of the two each one is** —and where it cannot be known, with the number saying how far I got looking. That is less heroic than a verdict and far more useful.
{: .text-justify}

There is a fourth kind of error I did not expect: the measuring instrument's own. The sweep that crosses documents against published figures got it wrong twice before it worked. First it asked for figures at coarser precisions than the printed one —looking for 20.7 rounded to an integer is looking for «21», which sits in any document with dates— and with that a codebook of 54 numbers «reproduced» the 48 cells of a table. Then it compared text instead of rounding, so the output that did produce a table fell outside its own table for printing 0.0087 where the table publishes 0.01.
{: .text-justify}

I caught both the same way: **measuring against a case I already knew**. If the sweep cannot find the producer I had already identified, I cannot believe it when it finds a new one. It is the same rule that holds up everything else.
{: .text-justify}

I would not have seen any of this arguing over numbers in prose: I saw it when I put the 2014 figure next to the 2026 one and the axes did not line up.
{: .text-justify}

---

## References

[^tesis]: Labra Olivares, Cristián A. *Patrones de entrada y salida de establecimientos educacionales en Chile (1992-2012)*, master's thesis, Universidad de Chile, 2014. Advisor: Daniel Hojman T.

[^grau2018]: Grau, Nicolás; Hojman, Daniel; Mizala, Alejandra. [School closure and educational attainment: Evidence from a market-based system](https://doi.org/10.1016/j.econedurev.2018.05.003), Economics of Education Review 2018.

[^dewald]: Dewald, William G.; Thursby, Jerry G.; Anderson, Richard G. Replication in Empirical Economics, American Economic Review 1986.

[^jenkins]: Jenkins, Stephen P. [Easy Estimation Methods for Discrete-Time Duration Models](https://doi.org/10.1111/j.1468-0084.1995.tb00031.x), Oxford Bulletin of Economics and Statistics 1995.

[^nickell]: Nickell, Stephen. [Biases in Dynamic Models with Fixed Effects](https://doi.org/10.2307/1911408), Econometrica 1981.

[^cameron]: Cameron, A. Colin; Miller, Douglas L. [A Practitioner's Guide to Cluster-Robust Inference](https://doi.org/10.3368/jhr.50.2.317), Journal of Human Resources 2015.

[^griliches]: Griliches, Zvi; Regev, Haim. [Firm Productivity in Israeli Industry 1979-1988](https://doi.org/10.1016/0304-4076(94)01601-U), Journal of Econometrics 1995.
