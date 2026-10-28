---
title: "Auditing Staggered DiD at 80M-Row Scale: Data-Inferred School Closures, Effective Clusters, and Manski Bounds"
published: false
description: "How we audited 20 years of student trajectories in Chile (79.7M enrolment rows) using DuckDB, exact G-1 matching, Callaway & Sant'Anna staggered DiD, and Manski missing-data bounds."
tags: datascience, econometrics, duckdb, python
canonical_url: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/
---

When working with nationwide administrative panels—in our case, **79,709,054 enrolment records** and **73,873,835 annual academic performance records** from Chile’s Ministry of Education (`MINEDUC`, 2004–2025)—the biggest threat to credible inference is rarely compute speed. With DuckDB and Parquet marts, joining **79,709,054** rows takes seconds.

The real danger is **silent methodological overconfidence**: treating raw directory exits as real closures, trusting nominal cluster counts when cluster sizes are skewed, or reporting a tight 95% confidence interval when outcome missingness can flip the sign of the estimate.

In [Part III of my thesis extension series on *3 Cucharadas*](https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/), we built a reproducible validation pipeline for student trajectories after school closures. Here are the four engineering and econometric guardrails that changed our conclusions.

---

## 1. Filtering *De Facto* Mergers with a Data-Inferred Closure Rule (`RCID v1`)

In panel data, a school identifier (`RBD`) dropping from positive enrolment in year $t-1$ to zero in year $t$ (**D0**: **1,981** episodes across 2005–2025) does not mean students were dispersed. Even after removing reopenings and site continuities (**D1**: **1,807** strict closures, including **330** in 2016–2025), student-flow matrices reveal cases where a single receiving school absorbs almost the entire cohort.

We formalised the **Data-Inferred School Closure Rule (`RCID v1`, D2)** as a deterministic SQL/DuckDB filter over student transition graphs:

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
  WHERE n_tracked_t1 >= 5
    AND (CAST(n_transferred AS DOUBLE) / n_tracked_t1) >= 0.70
    AND n_transferred >= 15
)
SELECT d1.*
FROM strict_closures_d1 AS d1
LEFT JOIN concentrated_absorptions AS ca
  USING (closure_cohort_year, origin_rbd)
WHERE d1.n_tracked_prev >= 5
  AND ca.origin_rbd IS NULL;
```

Applying `RCID v1` purges 95 historical and 34 recent concentrated absorptions ($\ge 70\%$ share and $\ge 15$ students), leaving **1,678** closures across 2005–2025 (**1,648** with a complete $t+1$ window observed).

---

## 2. Why Confidence Intervals Aren't Enough: Arm-Adversarial Manski Bounds

In our primary recent window (**2016–2019**, **63** supported closures, **6,190** exposed student-cohort observations matched exactly at $G-1$ against **82,753** controls), we estimated two primary difference-in-differences outcomes across **62 episodes**:
- **2-year persistent non-enrolment:** **+0.63 percentage points** (95% CI: **[−0.77, 2.03]**, $N_{\text{treated}} = 3,666$, $N_{\text{control}} = 49,944$).
- **1-year progression failure or grade lag** (no enrolment or enrolled below the expected grade at $t+1$): **+5.29 percentage points** (95% CI: **[2.08, 8.51]**, $N_{\text{treated}} = 4,815$, $N_{\text{control}} = 65,538$).

A naive pipeline would ship `+5.29 pp (p < 0.01)` as a confirmed harm.

However, baseline valid performance-record coverage at $G-1$ already shows a **−19.4 percentage-point** gap (**76.8%** among exposed students vs. **96.2%** among controls), and next-year progression status is not observed for every student in the support set. When we compute worst-case **Manski (2003) bounds** for the missing progression records, the bound interval spans **[−1.15, 10.98] percentage points**.

In our Ruby release gate (`verify_thesis_post3.rb`), we enforce a hard invariant: **every single mention of `5.29` in prose, tables, or `<figure>` alt text must appear in the same local window as both `−1.15` and `10.98`**:

```ruby
def verify_progression_pairing(lang, body, progression_pattern)
  lower = lang == "es" ? /(?:[−-]1,15|menos\s+1,15)/i : /(?:[−-]1\.15|minus\s+1\.15)/i
  upper = lang == "es" ? /10,98/i : /10\.98/i
  blocks = semantic_blocks(body).select { |block| block.match?(progression_pattern) }
  paired = blocks.all? do |block|
    claims = positions(block, progression_pattern)
    lows = positions(block, lower)
    highs = positions(block, upper)
    claims.all? do |claim|
      lows.any? { |pos| (claim - pos).abs <= 420 } &&
        highs.any? { |pos| (claim - pos).abs <= 420 }
    end
  end
  raise ThesisPost3Error, "unpaired progression claim (#{lang})" unless paired
end
```

---

## 3. Effective Treated Clusters vs. Nominal Episode Counts

With 62 treated closure episodes, standard cluster-robust inference looks comfortable at first glance. But school closures have highly skewed enrolment sizes. Computing the **effective number of treated clusters** ($G_{\text{eff}} = (\sum w_g)^2 / \sum w_g^2$) drops the independent information to:
- **21.1 effective episodes** for persistent non-enrolment,
- **21.9 effective episodes** for progression failure or lag,
- **17.7 effective episodes** for exploratory attendance (**−1.15 points**, **[−2.40, 0.10]**) and average marks (**−0.06**, **[−0.14, 0.01]**, observed across **58** episodes and **3,871** exposed students).

---

## 4. Scaling to 20 Staggered Cohorts (2005–2024) and Checking Pre-Existing Mobility

Rather than relying on a two-way fixed-effects regression that mixes already-treated cohorts into the control group with negative weights, we estimated each of the **20 annual closure cohorts ($G = 2005\dots 2024$)** separately against clean not-yet-treated controls (**Callaway & Sant'Anna 2021**), covering **1,141 supported episodes**, **78,972 exposed observations**, and **734,472 controls**:

| Regime / Aggregation | Supported Episodes | Exposed ($N$) | Controls ($N$) | Progression Failure / Lag (pp) | 95% CI (pp) |
|---|---:|---:|---:|---:|---:|
| **2005–2010** (LOCE / early SEP) | 521 | 36,984 | 334,062 | **+12.15** | [+3.78, +20.52] |
| **2011–2015** (LGE / SAC rollout) | 502 | 31,512 | 260,740 | **+7.82** | [+6.20, +9.41] |
| **2016–2019** (Main window; bounds [−1.15, 10.98]) | 63 | 6,190 | 82,753 | **+5.29** | [+2.08, +8.51] |
| **2020–2022** (COVID-19 pandemic) | 33 | 3,272 | 42,457 | **+2.70** | [−0.63, +6.03] |
| **2023–2024** (Post-pandemic) | 22 | 1,014 | 14,460 | **+2.59** | [−1.55, +6.73] |
| **Callaway & Sant'Anna (exposed-weighted)** | **1,141** | **78,972** | **734,472** | **+9.11** | **[+5.34, +12.88]** (Manski: [+0.43, +16.21]) |
| **Equal annual cohort weights** | **1,141** | **78,972** | **734,472** | **+7.55** | **[+5.52, +9.57]** |
| **Inverse-variance precision ($I^2 = 76.48\%$)** | **1,141** | **78,972** | **734,472** | **+5.14** | **[+4.34, +5.95]** |

Even when all 19 estimable annual progression cohorts are positive, extended $G-1$ profiling shows why observational DiD cannot be promoted to a randomized trial: while individual poverty eligibility (`SEP`) is balanced (**30.68%** priority students vs. **32.32%**), exposed students came from schools with fewer `SEP` agreements (**−10.06 pp**), less full-day schooling (**−18.54 pp**), and **47.04%** had already switched schools between $G-3$ and $G-1$ (vs. **30.52%** of controls).

All tabular CSV fallbacks, DTCG visual tokens, and bilingual reports are available at [3cucharadas.cl](https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/).
