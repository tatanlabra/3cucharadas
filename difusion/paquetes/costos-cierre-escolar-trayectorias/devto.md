---
title: "Auditing Staggered DiD at 80M-Row Scale: 20 Years of School Closures, Institutional Regimes, and Manski Bounds"
published: false
description: "How we audited 20 years of student trajectories in Chile (79.7M enrolment rows, 2005–2024) using DuckDB, Callaway & Sant'Anna staggered DiD, Manski bounds, and pre-trend stress tests."
tags: datascience, econometrics, duckdb, python
canonical_url: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/
---

When working with nationwide administrative panels—in our case, **79,709,054 enrolment records** and **73,873,835 annual academic performance records** from Chile’s Ministry of Education (`MINEDUC`, 2004–2025)—the biggest threat to credible inference is rarely compute speed. With DuckDB over Parquet marts, the longitudinal join is not the bottleneck.

The real danger is **silent methodological overconfidence**: treating raw directory exits as real closures, relying on a narrow recent window without checking the long historical series, or reporting a tight 95% confidence interval when outcome missingness can flip the sign of the estimate.

In [Part III of my thesis extension series on *3 Cucharadas*](https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/), I built a reproducible validation pipeline across **20 annual closure cohorts (`2005–2024`)**. Here are the engineering and econometric guardrails that shaped the conclusions.

---

## 1. Filtering *De Facto* Mergers Across 20 Years with `RCID v1`

In panel data, a school identifier (`RBD`) dropping from positive enrolment in year $t-1$ to zero in year $t$ (**D0**: **1,981** episodes across 2005–2025; **1,635** historical and **346** recent) does not mean students were dispersed. Even after removing annexes, secondary sites, and registered RBD successors (**D1**: **1,807** strict closures, purging **158** historical and **16** recent continuities to leave **1,477** in 2005–2015 and **330** in 2016–2025), student-flow matrices reveal cases where a single receiving school absorbs almost the entire cohort.

I formalised the **Data-Inferred School Closure Rule (`RCID v1`, D2)** as a deterministic DuckDB filter over student transition graphs (conceptual sketch; the production query also checks the stable main destination in $t+1$ and the destination `HHI`):

```sql
-- Conceptual DuckDB filter for RCID v1 (stratum D2)
WITH destination_shares AS (
  SELECT
    closure_cohort_year,
    origin_rbd,
    dest_rbd,
    COUNT(DISTINCT mrun) AS n_transferred,
    SUM(COUNT(DISTINCT mrun)) OVER (PARTITION BY closure_cohort_year, origin_rbd) AS n_tracked_t1
  FROM student_transitions_d1
  WHERE dest_rbd IS NOT NULL
  GROUP BY 1, 2, 3
),
concentrated_absorptions AS (
  SELECT DISTINCT closure_cohort_year, origin_rbd
  FROM destination_shares
  WHERE n_tracked_t1 >= 10
    AND (CAST(n_transferred AS DOUBLE) / n_tracked_t1) >= 0.70
)
SELECT d1.*
FROM strict_closures_d1 AS d1
LEFT JOIN concentrated_absorptions AS ca
  USING (closure_cohort_year, origin_rbd)
WHERE d1.n_tracked_prev >= 10
  AND ca.origin_rbd IS NULL;
```

Applying `RCID v1` purges **95** historical and **34** recent concentrated absorptions ($\ge 10$ baseline and assigned students, $\ge 70\%$ share to a single main destination in $t$ and $t+1$, and destination $\text{HHI} \ge 0.50$), leaving **1,678** conservative `D2` closures and **1,648** clean `D2` closures with a complete observed $t+1$ window (**1,382** in 2005–2015 and **266** in 2016–2024, excluding **30** right-censored 2025 closures). Of those **1,648** closures, **1,177** offered regular primary/secondary grades and **1,141** had exact matching support (**78,972** exposed student-cohort observations vs. **734,472** controls).

---

## 2. Leading with the 20-Year Staggered Series (2005–2024) and Five Institutional Regimes

Rather than relying on a two-way fixed-effects regression that mixes already-treated cohorts into the control group with negative weights, I estimated each of the **20 annual closure cohorts ($G = 2005\dots 2024$)** separately against clean not-yet-treated controls matched exactly at $G-1$ (**Callaway & Sant'Anna 2021**; **Sun & Abraham 2021**):

| Regime / Aggregation | Supported Episodes | Exposed ($N$) | Controls ($N$) | Progression Failure / Lag (pp) | 95% CI (pp) | Manski Bounds (pp) | 2-Yr Non-Enrolment (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **2005–2010** (LOCE / early SEP) | 521 | 36,984 | 334,062 | **+12.15** | [+3.78, +20.52] | [+3.49, +18.83] | **+1.21** [+0.53, +1.90] |
| **2011–2015** (LGE / SAC rollout) | 502 | 31,512 | 260,740 | **+7.82** | [+6.20, +9.41] | [−2.11, +16.18] | **+1.85** [+1.10, +2.59] |
| **2016–2019** (Nested zoom; bounds [−1.15, 10.98]) | 63 | 6,190 | 82,753 | **+5.29** | [+2.08, +8.51] | [−1.15, +10.98] | **+0.63** [−0.77, +2.03] |
| **2020–2022** (COVID-19 pandemic) | 33 | 3,272 | 42,457 | **+2.70** | [−0.63, +6.03] | [+0.18, +4.95] | **−0.28** [−1.37, +0.81] |
| **2023–2024** (Post-pandemic) | 22 | 1,014 | 14,460 | **+2.59** | [−1.55, +6.73] | [−1.70, +6.07] | **−0.93** [−2.64, +0.78] |
| **Callaway & Sant'Anna (exposed-weighted)** | **1,141** | **78,972** | **734,472** | **+9.11** | **[+5.34, +12.88]** | **[+0.43, +16.21]** | **+1.38** **[+0.92, +1.85]** |
| **Equal annual cohort weights** | **1,141** | **78,972** | **734,472** | **+7.55** | **[+5.52, +9.57]** | — | **+1.03** **[+0.56, +1.50]** |
| **Random effects ($I^2 = 76.5\%$, $\tau = 2.81$ pp)** | **1,141** | **78,972** | **734,472** | **+6.29** | **[+4.49, +8.09]** | Pred: [+0.09, +12.49] | **+0.79** **[+0.16, +1.42]** |

All **19 estimable annual progression cohorts (`2006–2024`)** are positive (ranging from **+0.94** to **+28.22 pp**, median **+7.18 pp**, IQR **+3.15 to +9.62**), and the first two institutional stages (`2005–2010` and `2011–2015`) concentrate **89.7%** of supported closures and **86.7%** of exposed observations.

---

## 3. Why the Nested 2016–2019 Zoom Requires Manski Bounds—and When Those Bounds Exclude Zero

In the nested **2016–2019** pre-registered zoom (**63** supported closures = **5.5%** of the series; **6,190** exposed of **78,972** in the series; **62** episodes with primary follow-up; **21.9** effective episodes for progression, **21.1** for non-enrolment, and **17.7** for attendance/marks), **1-year progression failure or grade lag** rises by **+5.29 percentage points** (95% CI: **[2.08, 8.51]**, $N_{\text{treated}} = 4,815$, $N_{\text{control}} = 65,538$).

However, baseline valid performance-record coverage at $G-1$ already shows a **−19.4 percentage-point** gap (**76.8%** among exposed students vs. **96.2%** among controls; **−19.24 pp** once controls are reweighted to the match), and next-year progression status is missing for **3.60%** of exposed students vs. **2.15%** of controls. Computing worst-case **Manski (2003) bounds** across the whole `2016–2019` subwindow yields **[−1.15, 10.98] percentage points**, which crosses zero and makes the overall subwindow estimate **inconclusive on its own**.

In the Ruby release gate (`verify_thesis_post3.rb`), I enforce a hard invariant: **every single mention of `5.29` in prose, tables, or `<figure>` alt text must appear in the same semantic block, within a fixed character window, as both `−1.15` and `10.98`**. This is the function as it ships in the repository:

```ruby
def verify_progression_pairing(lang, body, progression_pattern)
  lower = lang == "es" ? /(?:[−-]1,15|menos\s+1,15)/i : /(?:[−-]1\.15|minus\s+1\.15)/i
  upper = lang == "es" ? /10,98/i : /10\.98/i
  total = body.scan(progression_pattern).length
  blocks = semantic_blocks(body).select { |block| block.match?(progression_pattern) }
  represented = blocks.sum { |block| block.scan(progression_pattern).length }
  paired = blocks.all? do |block|
    claims = positions(block, progression_pattern)
    lows = positions(block, lower)
    highs = positions(block, upper)
    claims.all? do |claim|
      lows.any? { |position| (claim - position).abs <= 420 } &&
        highs.any? { |position| (claim - position).abs <= 420 }
    end
  end
  unless total.positive? && represented == total && paired
    raise ThesisPost3Error, "cada mención de progresión debe conservar sus dos cotas #{lang}"
  end
end
```

The `represented == total` check matters: a mention of the estimate that falls outside every semantic block (for example inside a stray HTML comment) would otherwise escape the pairing test, and a gate that cannot fail is not a gate.

When I restrict the `2016–2019` zoom to closures that complied with the **≥ 90% valid prior-year record benchmark** (**1,822** exposed students with an outcome, **38%** of exposed support), missingness equalises (**2.31%** vs. **2.15%**), the estimate is **+4.26 pp**, and the worst-case **Manski bounds tighten to [+0.09, +7.84] pp**—strictly above zero (threshold **λ* = 1.0114**).

---

## 4. Pre-Trend Sensitivity (`Rambachan & Roth 2023`), Stayers vs. Late Entrants, and Destination Quality ($\Delta Q_i$)

Three additional diagnostics stress-test the `2016–2019` mechanism window:
- **Pre-trend placebos & breakdown margin:** Three pre-closure placebos give **+0.16**, **+0.30**, and **+0.40 pp** (largest 95% upper bound **0.81 pp**). Under a linear **Rambachan & Roth (2023)** sensitivity check, post-closure bias would need to reach **2.07 pp** (**2.54** times the **0.81 pp** placebo upper bound) to push the confidence interval around **+5.29 pp** (bounds **[−1.15, 10.98] pp**) across zero.
- **Continuous stayers vs. late entrants:** Prior mobility was common: **47.04%** of exposed students had switched schools between $G-3$ and $G-1$ (vs. **30.52%** of controls, **+16.52 pp**). In the descriptive universe, **70.58%** of **6,581** exposed observations were stable from $G-2$. The separate supported progression sample includes **3,556** continuous stayers and **1,033** late entrants. Progression failure rises **+3.87 pp** (**[+1.04, +6.69]**) among stayers and **+9.58 pp** (**[+5.06, +14.10]**) among late entrants—about three-quarters of the point gap remains even among stable students.
- **Receiving-school historical promotion quality ($\Delta Q_i$ at $G-1$):** Among **4,362** exposed students who re-enrolled in another school in the closure year ($G$), transferring to a school with a higher prior promotion rate (**2,099** students) yields a **+2.03 pp** gap, versus **+5.38 pp** when transferring to a school with an equal or lower prior rate (**2,263** students; descriptive difference **−3.35 pp**, with no confidence interval of its own yet, and families choose the destination, so this is heterogeneity, not a dose-response effect).

All tabular CSV fallbacks, DTCG visual tokens, and bilingual reports are available at [3cucharadas.cl](https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/).
