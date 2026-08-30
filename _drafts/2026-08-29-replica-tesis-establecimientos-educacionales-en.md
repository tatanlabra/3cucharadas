---
layout: single
title: "Replicating my own thesis in 3 spoonfuls: is the error from 2014, or is it mine today?"
subtitle: "I rebuilt the master's thesis I wrote on school entry and exit in Chile's voucher market, and put every table and figure next to its original"
date: 2026-08-29 09:30:00 -0400
categories: [datos, educacion, politica-publica]
tags: [replication, education, school-markets, voucher, mineduc, duration-analysis, vulnerability, audit]
description: "In 2026 I rebuilt my 2014 master's thesis on the entry and exit of schools in Chile, compared every table against the published one, and separated errors in the document from errors in my own replication."
excerpt: "When a rebuilt table does not match the printed one, the useful question is not which of the two is wrong, but whose error it is. Answering it means putting both side by side."
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

What follows is that first half. I rebuilt the eight tables and the figures, put them next to the published ones, and decided, cell by cell, whose difference each one was.
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
  <figcaption><strong>Figure 1</strong> — Total mobility by dependency: the 2014 original and my replication, which pools the twenty years so the balance reads in one glance. The totals on the right add up to 2,168 entries and 2,069 exits, the restricted universe behind the stylised facts. Panel labels are in Spanish, as in the source.</figcaption>
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

With a caveat that forces me to lower my voice: **the historical `do-file` was not executed**; what ran was a controlled reimplementation, and the artefact records it that way.
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
**Table 2** — The two cells whose asterisks do not add up

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

And a number I would rather not write: of the **30 revision proposals** this audit produced, only **12 today carry a traceable claim with its hash**. The other 18 are labelled proposal or unverified, and that is how they must be read. Anyone taking all 30 as findings has read this post backwards.
{: .text-justify}

## Spoonful 3: the five findings that change a reading

**1. My exit marker did not mark exits.** The variable `id_salida` correlates −0.977 with the calendar year: it falls from 1,676 flagged cases in 1992 to exactly 0 in 2012, while effective exits range between 42 and 290 with no trend (ρ = +0.382). It does not say «closed», it says «will close in some year within the window»: a school closing in 2011 is flagged in every prior year and in none after.
{: .text-justify}

It contaminates the three descriptive tables and the definition of the event in the duration model.
{: .text-justify}

**2. My duration variable measures observed tenure, not institutional age.** The panel starts in 1992 and schools that already existed enter left-truncated, which I did not declare; on top of that I imposed a linear shape on the baseline hazard. Measured year by year that slope is +0.018 percentage points a year with p = 0.27: I cannot tell it from zero. It is not a matter of form, because the baseline hazard is precisely what the model uses to separate the effect of time from that of the covariates.
{: .text-justify}

**3. The co-payment averages eight years of nominal pesos without deflating.** The crude entrant-exiter gap I published is \$8,133.6. Computed within each year and then weighted, it falls to \$7,124.2: **\$1,009.4, some 12.41 %, was temporal composition** and not a difference between schools. The finding survives, the magnitude does not. And there is something better underneath: the gap moves from \$8,085.69 in the first year of the series to \$3,821.18 in the last. **It converges to less than half**, and my pooled average erased exactly that.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh-en.webp' | relative_url }}" alt="On the left, the figure published in 2014 relating the municipal Herfindahl index to total mobility, with the horizontal axis running from 0 to 100. On the right, the 2026 replication of the same crosswalk on the canonical 0 to 10,000 axis, with a fitted line of negative slope." loading="lazy" decoding="async">
  <figcaption><strong>Figure 2</strong> — Municipal concentration and mobility. The original's axis stops at 100; the Herfindahl index is defined between 0 and 10,000, with 2,500 as the high-concentration threshold. The replication adds the line fitted over 336 municipalities.</figcaption>
</figure>

**4. The concentration index sits on a scale that is not its own, and its sign does not agree.** Put side by side, the original's axis stops at 100 and the Herfindahl index runs to 10,000. The municipality of Santiago, which I named explicitly, measures 157.1 against the 1,534 I published.
{: .text-justify}

With the scale corrected, more concentration goes descriptively with **less** mobility (negative slope, p = 0.009, 336 municipalities), while my municipal exits model reported a positive coefficient. And that model stacks three identification problems: contemporaneous regressors my own text declares jointly determined, a lagged dependent variable under random effects,[^nickell] and inference over 15 clusters.[^cameron] With so few groups, the standard error stops being trustworthy before the coefficient does.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" alt="Series with confidence intervals of the pupil-per-classroom-teacher ratio of schools that close, from seven years before the last flagged year to that year: it falls from 17.95 to 12.22, against a horizontal line at 20.3 for incumbent schools." loading="lazy" decoding="async">
  <figcaption><strong>Figure 3</strong> — The shadow of death, measured: pupils per classroom teacher in exiting schools, by year relative to the last flagged year, against incumbents. Axis labels are in Spanish, as generated.</figcaption>
</figure>

**5. The «shadow of death» was measurable and I only named it.** The pupil-per-teacher ratio of exiting schools falls monotonically from **17.95 to 12.22** over the seven prior years, against **20.31** for incumbents. This is not a sudden collapse: it is a seven-year hollowing out. That changes the policy reading, because deterioration with that shape is observable while it happens.
{: .text-justify}

With the caveat from finding 1: the axis measures years relative to the last flagged year, and that marker turned out not to mean what I thought it did.
{: .text-justify}

One debt left is not an error but an absence: the Schumpeterian frame organises my title, my abstract and my conclusion, but I never tested it. The reallocation decomposition separating improvement within incumbents from that coming from entry and exit —the standard in the very literature I was citing— is not in the document.[^griliches]
{: .text-justify}

## Closing: the second half runs to 2025

A second post will bring the recreation extended to 2025. The sources are already acquired —fourteen official MINEDUC collections, including the Official Directory 1992-2025— but I am not previewing figures: extending the window puts regime changes in the middle.
{: .text-justify}

What I take away is less technical than I expected. The two confirmed errors are asterisks and elementary arithmetic; the findings that move a conclusion came from looking at what my variables actually measured.
{: .text-justify}

And I would not have seen any of them arguing over numbers in prose: I saw them when I put the 2014 figure next to the 2026 one and the axes did not line up.
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
