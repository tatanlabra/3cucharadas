# Medium Import Draft — I Audited My 2014 Master's Thesis Twelve Years Later: What Survived and What My Own Files Corrected

> **Canonical URL (must be set in Medium Advanced Settings before publishing):**
> `https://3cucharadas.cl/en/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/`

In April 2014, I defended my master's thesis on the entry and exit of schools in Chile between 1992 and 2012. Twelve years later, I wanted to extend that study through 2025.

Before adding thirteen years of new school openings, closures, and regulatory reforms, I forced myself to answer a humbling preliminary question: **how much of my 2014 thesis could I actually reproduce today?**

When you only compare a published PDF against a modern script, any discrepancy invites post-hoc excuses. So I brought in a third witness: the surviving 2014 producer files—original Stata logs, working spreadsheets, and chart formulas—alongside new re-estimations in Stata and Python. Across **34** editorial judgements and **50** technical hypotheses (and **26** display objects: **12** convergences, **10** explained divergences, **4** without a numerical test, and **0** unexplained divergences), **15** judgements held up, **10** errors came from the 2014 document, and **0** known errors remain in the 2026 reference version (with **9** remaining cases: **1** wrong on both sides, **1** misleading match, and **7** where provenance cannot crown a winner).

---

## 1. The Big Picture Survived—and Resembled the Spreadsheet More Than My Prose

Between 1992 and 2012, Chile's school system did not simply grow or shrink; it experienced a massive reallocation across administrative sectors. My 2026 reconstruction counts **2,168** entries and **2,069** exits (compared with **2,160** and **2,065** in my 2014 spreadsheet): municipal public schools registered **346** entries and **1,135** exits, subsidised private voucher schools registered **1,468** entries and **597** exits, and fee-paying private schools registered **354** entries and **337** exits.

Curiously, in the 2012 cross-section, my 2026 reconstruction sits just **3.05** percentage points away from the prior run stored inside my 2014 spreadsheet, whereas the text I signed in 2014 drifted **13.41** percentage points from that same spreadsheet (**4.50** points in municipal, **2.42** in free subsidised-private, and **4.27** in high-fee schools).

Distributive sorting in Greater Santiago also held up: schools that later left the register served more vulnerable student populations (`IVE`), at **87.4%** versus **78.3%** in municipal schools and **72.2%** versus **62.8%** in subsidised private schools (**42** rebuilt cells match within rounding, along with **10** of **11** fixed effects, a **−4.3%** `SIMCE` test-score gap among closing subsidised schools, and mobility rates of **6.3**, **4.5**, and **1.6**).

---

## 2. Four Instructive Mistakes from 2014

1. **Copy-paste and log-variance errors:** In Table 6, lagged mathematics `SIMCE` was printed as **0.003**, even though the producing Stata output printed **0.001** (**0.000533** in Stata and Python). Worse, two rows labelled as variances (**3.82** and a crossed log standard deviation) were actually untransformed log standard deviations from Stata: the true between-municipality variance is **265.6** and the residual variance is **2,079.7** (and another cell turned **0.4142** into **1.4142**).
2. **When a mixed model blends sorting with change (Mundlak 1978 & Chamberlain 1982):** In Greater Santiago (`Table 7`, **14,704** observations across **2,640** schools), my 2014 random-slope variance collapsed onto the numerical boundary (`2.1 × 10⁻¹⁵`), fusing permanent differences between schools with annual changes within the same school. Re-estimating `ln(enrolment)` with the **Mundlak (1978) and Chamberlain (1982)** correlated random effects decomposition separates the two: the positive link with lagged mathematics `SIMCE` is entirely a **between-school** selection effect (`0.012131`, `t = 16.27`), while **within** a given school, annual `SIMCE` improvements have no detectable effect on next year's enrolment and even flip sign (`−0.000048`, `t = −0.53`; dynamic contrast: `0.000543`, `t = 7.26` between and `0.000174`, `t = 2.44` within).
3. **A tenfold scale error in market concentration (`HHI`):** On the canonical **0** to **10,000** Herfindahl–Hirschman scale (where US Merger Guidelines set high concentration at **2,500** in 2010 and **1,800** in 2023), my spreadsheet stored values multiplied by **100** and my text read them as multiplied by one thousand—putting Santiago at **1,534** instead of **152**, and using a formula `> 2.5` (**250** canonical points) that labelled **330** of **346** municipalities in 2006 (**95%**) as concentrated (**318** of **337** panel municipalities on the buggy scale vs **66** on the canonical scale; slope `p = 0.084`). And a claim that cities under **15,000** inhabitants accounted for **80%** of mobility actually reflected a non-capital split (**78.3%**), whereas the literal population threshold gave **11%**.
4. **The seven-year “shadow of death”:** Across **59,808** observations (**36,493** municipal and **23,315** subsidised-private, 2004–2011), exiting schools saw their pupil–teacher ratio fall from **17.95** to **12.22** over the seven years prior to exit (versus **20.31** among stayers), operating with **5.90** and **6.23** fewer pupils per teacher and contracting faster by **0.216** (**0.849** vs **0.632**) and **0.148** (**0.565** vs **0.417**) per year.

---

## 3. Out-of-Sample Risk Ranking and Preparing the 2025 Extension

When I tested the thesis's discrete-time hazard model (`cloglog`, **30,484** observations across **7,460** schools and **237** closures) out of sample—training on 2007–2008 (**12,495** rows, **86** closures) and evaluating on 2009–2011 (**17,989** rows, **151** closures)—it ranked closure risk well (**AUC = 0.8517**, interval **0.81–0.89**; **43.7%** of closures in the top **10%** risk decile, **66** of **151**, and **69.5%** in the top **20%** quintile), but underpredicted the level (**0.60%** predicted vs **0.84%** observed; Brier score **0.008196** vs **0.008324**, a **1.5%** skill gain).

Finally, using student-level records from 2004 onward, I built the **Data-Inferred School Closure Rule (`RCID v1`, 2005–2025)**: narrowing **1,981** raw permanent exits (**D0**) to **1,807** strict closures (**D1**) and **1,678** conservative inferred closures after removing block absorptions where $\ge 70\%$ of reassigned students move to a single stable school with destination `HHI` $\ge 5,000$ (**1,382** in 2005–2015 and **296** in 2016–2025; or **1,648** clean closures with observed $t+1$, setting aside **30** right-censored 2025 closures).

One caveat before the link: auditing my own thesis is not an independent replication, and none of these associations are causal. Read the full bilingual article and interactive verification chain at [3cucharadas.cl](https://3cucharadas.cl/en/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/?utm_source=medium&utm_medium=syndication&utm_campaign=tesis_post1).
