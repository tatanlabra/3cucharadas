---
title: "Auditing My 2014 Econometrics Thesis: Producer Provenance, Mundlak CRE vs. Mixed Models, and Out-of-Sample Hazard Validation"
published: false
description: "What happens when you re-run a 12-year-old school-turnover thesis in Stata and Python: separating transcription bugs, HHI scale errors, collapsed random slopes, and out-of-sample Brier skill."
tags: datascience, python, econometrics, reproducibility
canonical_url: https://3cucharadas.cl/en/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/
---

Twelve years after defending my 2014 master's thesis on school entry and exit in Chile (`1992–2012`), I set out to extend the panel through 2025. Before appending thirteen years of new administrative records, I built a verification pipeline to audit **34** published editorial judgements and **50** technical hypotheses across **26** display objects (**12** convergences, **10** explained divergences, **4** without a numerical test, and **0** unexplained divergences).

In [Part I of the series on *3 Cucharadas*](https://3cucharadas.cl/en/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/), separating three distinct artefacts—the published 2014 PDF, the surviving 2014 producer files (Stata logs and Excel workbooks), and new 2026 executions—showed that **15** judgements held up, **10** errors came from the 2014 document, and **0** known errors remain in the 2026 reference output (with **9** remaining cases: **1** wrong on both sides, **1** misleading match, and **7** provenance/no-winner cases).

Here are the four technical lessons that matter for anyone auditing legacy econometric code.

---

## 1. The Four-Stage Verification Boundary

A script that finishes without throwing an exception proves very little. The verification pipeline enforces a strict four-stage hierarchy:
> **Rerunnable ≠ Rebuildable ≠ Matching ≠ Correct ≠ Causal**

For example, in the 1992–2012 school directory, my 2026 reconstruction counts **2,168** entries and **2,069** exits (municipal: **346** entries and **1,135** exits; subsidised-private: **1,468** and **597**; fee-paying private: **354** and **337**), whereas my 2014 workbook had **2,160** and **2,065**. In the 2012 cross-section, the rebuilt shares sit **3.05** percentage points from the prior spreadsheet run, while the published 2014 prose drifted **13.41** percentage points from its own spreadsheet (**4.50** points in municipal, **2.42** in free subsidised-private, and **4.27** in high-fee schools). Without the intermediate producer file, that discrepancy would have been misattributed to the modern code.

---

## 2. Silent Mixed-Model Failures: Collapsed Random Slopes vs. Mundlak–Chamberlain `CRE`

In Greater Santiago (`Table 7`, **14,704** school-year observations across **2,640** schools), the 2014 thesis estimated a linear mixed model for `ln(enrolment)` with random slopes. Auditing the producer log revealed two specification defects:
1. The random-slope variance had collapsed onto the numerical boundary (`2.1 × 10⁻¹⁵`), while two other hierarchical model rows in `Table 6` (**3.82** and a crossed log standard deviation) had been copied directly from Stata's untransformed log standard deviations instead of exponentiating them into the true random-intercept variance (**265.6**) and residual variance (**2,079.7**)—alongside a transcription typo turning **0.000533** (**0.001**) into **0.003** and **0.4142** into **1.4142**.
2. Standard random effects assume unobserved school traits are uncorrelated with covariates, conflating cross-sectional sorting *between* schools with longitudinal change *within* a school.

Replacing the degenerate random-slope specification with pooled OLS using the **Mundlak (1978) and Chamberlain (1982) Correlated Random Effects (`CRE`)** decomposition (including school-level historical means alongside annual deviations, with school `RBD`-clustered standard errors) splits the coefficient cleanly:
- **Between-school sorting:** `0.012131` (`t = 16.27`). Schools with higher historical mathematics `SIMCE` scores are structurally larger.
- **Within-school change:** `−0.000048` (`t = −0.53`). When a school improves its `SIMCE` score from one year to the next, its enrolment does not detectably increase (and the point estimate even flips sign). In the dynamic specification with lagged enrolment (`0.000543`, `t = 7.26` between; `0.000174`, `t = 2.44` within), short-panel Nickell bias applies.

---

## 3. Unit-Scale Bugs in Market Concentration (`HHI`) and Pre-Exit Contraction

In `TESIS.xlsx`, the Herfindahl–Hirschman Index (`HHI`, canonical scale **0** to **10,000**, with high-concentration thresholds at **2,500** in 2010 and **1,800** in 2023) was stored multiplied by **100** instead of **10,000**, and the thesis text read it as multiplied by one thousand:
- Santiago was reported around **1,534** instead of its canonical value of **152**.
- A threshold formula `=C2>2.5` (**250** canonical points instead of **2,500**) flagged **330** of **346** municipalities in 2006 and **326** in 2016 (**95%**); across **337** panel municipalities, the buggy scale labels **318** as highly concentrated versus **66** on the canonical scale (slope `p = 0.084`).

Conversely, a new descriptive decomposition on **59,808** municipal (**36,493**) and subsidised-private (**23,315**) observations from 2004–2011 quantified the seven-year “shadow of death” prior to exit: the pupil–teacher ratio of exiting schools drops from **17.95** to **12.22** (versus **20.31** among staying schools), operating with **5.90** and **6.23** fewer pupils per teacher on average and falling faster by **0.216** (**0.849** vs **0.632**) and **0.148** (**0.565** vs **0.417**) pupils per teacher per year.

---

## 4. Out-of-Sample Hazard Validation (`AUC` vs. Brier Skill) and `RCID v1`

In 2014, the discrete-time hazard model (`cloglog` on 2007–2011, `Table 10`: **30,484** school-year observations across **7,460** `RBD`s and **237** closures) was evaluated only in-sample. Splitting the panel temporally—training on 2007–2008 (**12,495** rows, **86** closures) and testing out-of-sample on 2009–2011 (**17,989** rows, **151** closures)—shows why `AUC` alone can mislead policy users:
- **Ranking (`AUC = 0.8517`, interval `0.81–0.89`):** The top **10%** risk decile captures **43.7%** of closures (**66** of **151**), and the top **20%** quintile captures **69.5%**.
- **Calibration (`Brier = 0.008196` vs. `0.008324` base-rate model):** Because the closure rate rose between training and test periods, mean predicted risk (**0.60%**) underpredicts the observed rate (**0.84%**), yielding a Brier skill improvement of just **1.5%**.

To prepare the 2005–2025 extension, I also replaced raw `RBD` directory exits with the three-sieve **Data-Inferred School Closure Rule (`RCID v1`)**: **D0** (**1,981** permanent exits with prior enrolment) $\supset$ **D1** (**1,807** strict closures after removing annexes/continuities) $\supset$ **D2** (**1,678** conservative inferred closures after removing block absorptions where a single stable receiver takes $\ge 70\%$ of reassigned pupils with destination `HHI` $\ge 5,000$: **1,382** in 2005–2015 and **296** in 2016–2025; or **1,648** clean closures with complete $t+1$ follow-up: **1,382** and **266**, excluding **30** right-censored 2025 closures).

Scope note: this is a self-audit with the original producer files, not an independent replication, and none of the associations above are causal. Full bilingual write-up and interactive SVG diagrams at [3cucharadas.cl](https://3cucharadas.cl/en/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/).
