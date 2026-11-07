---
title: "Why Extending an Administrative Panel Is Not Just Appending Rows: Schema Drift, Empirical Bayes Shrinkage, and Few-Cluster Inference"
published: false
description: "How we audited 2013–2025 school turnover in Chile using RCID v1 student-flow sieves, Morris (1983) Empirical Bayes shrinkage, McFadden (1974) conditional logit, and Synthetic DiD / Webb WCB."
tags: datascience, econometrics, python, publicpolicy
canonical_url: https://3cucharadas.cl/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/
---

When extending a longitudinal dataset by a decade, the most dangerous failure mode is silent schema and estimand drift: running the old code on new years and treating the output as a continuous series.

In [Part II of my school-turnover series on *3 Cucharadas*](https://3cucharadas.cl/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/), I extended my Chilean school panel (`2013–2025` for entries and `2015–2025` directories for `2016–2025` transitions). Here are the four data-engineering and econometric hurdles that prevented naive causal claims.

---

## 1. Event Sieves (`D0 ⊃ D1 ⊃ D2`): Why 900 Official Closures Become 266 Clean Events

In raw administrative directories, **900** transitions into closed status (code 3) occur between 2016 and 2025: **684** from active operation, **215** from temporary recess, and **1** from authorisation without enrolment.
- **Empty shells:** Of the **684** previously active schools, **346** had enrolled pupils and **338** already had zero enrolment.
- **Directory continuities (`D1`):** Reconstructing school identity, annexes, and education segments removes **16** annex closures, consolidations, or identifier (`RBD`) replacements, leaving **330** strict closures.
- **Student-flow block absorptions (`RCID v1`, `D2`):** Linking annual student rosters flags **34** episodes with at least **10** baseline and assigned students where $\ge 70\%$ move together to a single stable receiving school with destination `HHI` $\ge 0.50$. Removing those *de facto* mergers leaves **296** conservative `RCID v1` closures and **266** clean closures with a fully observed $t+1$ window (excluding **30** right-censored 2025 closures).

---

## 2. Small-School Missingness and Morris (1983) Parametric Empirical Bayes Shrinkage

Across **665** active closures with three complete prior years, median enrolment contracts from **28 → 23 → 1** student before closure (**44 → 34 → 0** in `D1`, **39 → 31 → 0** in conservative `D2`, and **36 → 27 → 0** in clean `D2`). Because exiting schools are tiny, test-score coverage is sparse: only **76** closures (**11.1%** of **684**) have three complete years of `SIMCE` (medians **−0.232 → −0.235 → −0.083** SD) and **188** have `IVE-SINAE` (**0.882 → 0.910 → 0.946**).

Among the **330** strict closures, only **97** have `SIMCE` and **46** have university admissions (`PSU/PDT/PAES`). Requiring exact 6-way commune matching (year, commune, segment, sector, rurality, and size band) discards **76** of **97** `SIMCE` closures and **38** of **46** admissions closures, leaving just **21** (**+0.029** SD, 95% CI **[−0.095, +0.158]**; **17** under `D2` at **+0.017** SD) and **8** (**−0.001** SD; **5** under `D2` at **−0.057** SD, below the minimum threshold of **10** closures).

To recover common support without ignoring small-sample noise, I relaxed commune blocking to the regional level and applied **Morris (1983) Parametric Empirical Bayes shrinkage**, pulling noisy small-school gaps toward the regional mean in proportion to their sampling variance relative to structural variance $\hat{\tau}^2$:
- **`SIMCE` extended support:** Recovers **95 of 97** closures (**97.9%**), yielding **+0.0061** SD (95% CI **[−0.1467, +0.1715]**, vs. **−0.0751** SD unshrunken).
- **Admissions extended support:** Recovers **44 of 46** closures (**95.7%**), yielding **−0.0420** SD (95% CI **[−0.1352, +0.0616]**, vs. **−0.0987** SD unshrunken).

I gained support (**97.9%** and **95.7%**), not precision: both intervals cross zero (**−0.15** to **+0.17** SD in `SIMCE`), and because the shrinkage weights larger, less noisy closures more heavily, the sign flip from the unshrunken gap is partly a reweighting, not just less noise. Meanwhile, market-level accounting decomposition shows turnover contributes **−0.000105** SD in `SIMCE` (**[−0.000346, +0.000103]**) and **+0.000113** SD in admissions (**[+0.000027, +0.000213]**).

---

## 3. Spatial Proximity vs. McFadden (1974) Conditional Discrete Choice (`N = 9,093`)

In spatial buffers (**10 km**, $t$ to $t+2$), out of **330** strict closures (**320** geocoded) and **414** openings (**389** geocoded), only **38** closures link to **29** unique openings in the same education segment.

Tracking **9,093** individual student transfers across **101** clean `D2` closures against all active schools serving the same level within **15 km** via a **McFadden (1974) conditional logit** (clustered by closure) shows where students actually relocate:
- Median distance is **1.83 km** (mean **2.89 km**), and **73.4%** stay in the same commune.
- Each additional kilometre cuts relative destination odds by one-third (`−0.4029` per km, `OR = 0.668`, `z = −5.34`), staying in the same commune more than triples the odds (`z = +5.24`), keeping the same sector more than doubles them (`z = +4.77`), larger log enrolment strongly attracts transfers (`z = +8.08`), and receiving-school `SIMCE` shows no positive pull (`−0.2311`, `OR = 0.794`, `z = −1.71`; mean realised `SIMCE` change **−0.035** SD).

---

## 4. Few-Cluster and Convex-Hull Diagnostics for `SLEP` and `SAE`

1. **`SLEP` de-municipalisation (`Arkhangelsky et al. 2021` Synthetic DiD):** Across **25** territory-horizon pairs, treated networks exceed the convex simplex of donor communes. **Synthetic DiD** yields **−0.0004** (**[−0.0526, +0.0966]**) in log public enrolment and **+0.0041** (**[−0.0289, +0.0431]**) in log active public schools (pre-transfer `RMSPE` **0.0140** vs. **0.0134**; baseline cross-validated `AUC = 0.5341`, permutation `p = 0.2195`).
2. **`SAE` centralised admissions (`Webb 2023` 6-point Wild Cluster Bootstrap + Fisher Permutation):** With only **4** treated regions out of **14**, asymptotic standard errors fail. Evaluating all $\binom{14}{4} = 1,001$ exact Fisher regional permutations and **Webb (2023) 6-point wild cluster bootstrap (`WCB`)** under equal regional weighting gives `HHI` **+0.0053** (Fisher `p = 0.7133`, `WCB` CI **[−0.0160, +0.0267]**; commune-grade weighted **+0.0035**, **[−0.0104, +0.0174]**) and log effective schools **−0.0142** (Fisher `p = 0.6703`, `WCB` CI **[−0.0580, +0.0292]**; commune-grade weighted **−0.0042**, **[−0.0265, +0.0181]**), while pre-treatment placebos fail under regional weighting.

Full bilingual article and coordinate audit at [3cucharadas.cl](https://3cucharadas.cl/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/).
