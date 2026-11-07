# Transcreated English Source — Part II: Extending a Panel Is Not Just Adding Years (What School Turnover in Chile Still Cannot Tell Us)

> Canonical URL: `https://3cucharadas.cl/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/`

When one school closes and another opens nearby, do opportunities to learn improve, or does only the administrative register change?

In Part I of this series, I audited my 2014 master's thesis on school entry and exit in Chile (`1992–2012`). In Part II, I extend the lens to recent school directories (`2015–2025` to observe transitions between `2016` and `2025`, and a `2013–2025` panel to detect entries). **This analysis does not identify whether school turnover improves or worsens educational outcomes.** Some aggregate comparisons are imprecise, others lack sufficient common support, and even when annual student rosters reveal where displaced students go the next year, administrative records alone cannot reconstruct what would have happened without the closure or opening.

What extending the panel does show is why appending years to a historical specification is a trap: schema definitions change, raw administrative exits mix empty shells and paperwork consolidations with real community displacements, and standard quasi-experimental designs for recent reforms fail support and small-cluster diagnostics.

---

## 1. Deconstructing “Closure”: From 900 Official Exits to 266 Clean Dispersed Closures (`RCID v1`)

In Chile's Ministry of Education (`MINEDUC`) directories, each school is tracked by its `RBD` (*Rol Base de Datos*) identifier. Between 2016 and 2025, **900** official closures (transitions to operating status code 3) appear in the register: **684** from active operation, **215** from temporary recess, and **1** from authorisation without enrolment.
- Among the **684** previously active schools, **346** had enrolled students and **338** already recorded zero enrolment. Closing an empty registration code is not displacing a school community.
- Reconstructing school identity, annexes, and exact education segments (`D1`) leaves **330** strict closures, removing **16** site/annex closures, administrative consolidations, or `RBD` replacements.
- Applying the **Data-Inferred School Closure Rule (`RCID v1`, level `D2`)** across longitudinal student rosters—which sets aside episodes with at least **10** baseline and assigned students where at least **70%** move to a single stable receiving school in `t` and `t+1` with destination concentration `HHI ≥ 0.50`—purges **34** block-absorption alerts, leaving **296** closures under conservative `RCID v1` and **266** clean closures with a complete observed `t+1` horizon (after setting aside **30** right-censored 2025 closures).

Meanwhile, demographic pressure is reshaping the planning horizon: according to Chile's National Statistics Institute (`INE`, based on the 2024 Census), the population aged 6 to 17 is projected to fall from **3,081,791** in 2025 to **1,366,155** in 2050—a **55.7%** contraction.

---

## 2. Pre-Closure Contraction, Test-Score Missingness, and Empirical Bayes Shrinkage (Morris 1983)

Across the **665** active closures with three complete prior years, median enrolment contracts sharply over the three years before closure: **28 → 23 → 1** student (and in the evaluated subset: **44 → 34 → 0** under `D1`, **39 → 31 → 0** under conservative `D2`, and **36 → 27 → 0** under clean `D2`).

Test scores and vulnerability indices suffer from severe selection and missingness:
- Only **76** closures (**11.1%** of the **684** active exits) have three complete years of standardised `SIMCE` test scores (medians moving from **−0.232** to **−0.235** to **−0.083** standard deviations), and **188** have the aggregate school vulnerability index `IVE-SINAE` (**0.882 → 0.910 → 0.946**).
- Among the **330** strict closures, only **97** have `SIMCE` and **46** have university admissions (`PSU/PDT/PAES`) data. Under exact commune matching (year, commune, segment, sector, rurality, and size band), common support drops to **21** closures in `SIMCE` (**+0.029** SD, 95% CI **[−0.095, +0.158]**; weighted **+0.034** SD **[−0.225, +0.289]**; **17** closures under `D2` at **+0.017** SD) and **8** closures in admissions (**−0.001** SD; **5** closures under `D2` at **−0.057** SD, below the retrospective minimum of **10** closures).
- **Morris (1983) Parametric Empirical Bayes Shrinkage:** Relaxing commune blocking to the regional level (region, year, segment, sector, and rurality) and shrinking noisy small-school gaps toward the regional mean recovers **95 of 97** closures (**97.9%**) in `SIMCE` (**+0.0061** SD, 95% CI **[−0.1467, +0.1715]**, versus **−0.0751** SD unshrunken) and **44 of 46** (**95.7%**) in admissions (**−0.0420** SD, 95% CI **[−0.1352, +0.0616]**, versus **−0.0987** SD unshrunken). Both intervals span zero (**−0.15** to **+0.17** SD in `SIMCE`).
- In market-level accounting decompositions, net entry and exit contributes **−0.000105** SD in `SIMCE` (**[−0.000346, +0.000103]**) and **+0.000113** SD in admissions (**[+0.000027, +0.000213]**)—practically nil and non-causal.

---

## 3. Spatial Proximity vs. Real Student Relocations (McFadden 1974 Conditional Logit)

Does a nearby opening replace a closed school? Among **330** strict closures (**320** with valid coordinates) and **414** openings (**389** with eligible coordinates), only **38** closures link within **10 km** (`t` to `t+2`) to **29** unique openings serving the exact same education segment. (In the historical case of El Salvador, School No. **14**, `RBD` **391** at **500** Diego Portales, closed at the end of 2013 and merged with School No. **1**, `RBD` **390** at **1510** Diego Portales after combined enrolment fell from **1,399** in 2004 to **977** in 2013, **−30.2%**, with School No. 1 jumping from **432** to **738** students in 2014.)

To see where displaced students actually go, I linked longitudinal rosters from clean `D2` closures to all active schools serving the same level within a **15 km** radius (**9,093** individual student transfers with coordinates across **101** closures) and estimated a **McFadden (1974) conditional logit** discrete-choice model with closure-clustered standard errors:
- Median relocation distance is **1.83 km** (mean **2.89 km**), **73.4%** of students stay in their home commune, and the mean realised `SIMCE` change is **−0.035** SD.
- Each additional kilometre reduces relative destination odds by one-third (`−0.4029` per km, `OR = 0.668`, `z = −5.34`); staying in the same commune more than triples the odds (`z = +5.24`); remaining in the same administrative sector more than doubles them (`z = +4.77`); larger enrolment attracts transfers (`z = +8.08`); and receiving-school `SIMCE` score shows no positive pull (`−0.2311`, `OR = 0.794`, `z = −1.71`).

---

## 4. Why Staggered Reform Evaluations (`SLEP` and `SAE`) Fail Identification Gateways

Two major recent reforms—the transfer of municipal schools to Local Public Education Services (`SLEP`, Law **21,040**) and the centralised School Admission System (`SAE`)—look like natural staggered difference-in-differences designs, yet both fail diagnostic gates:
- **`SLEP` (Synthetic DiD, Arkhangelsky et al. 2021):** None of the **25** territory-horizon combinations had an admissible pure synthetic control within the donor convex simplex. Under **Synthetic Difference-in-Differences**, the mean change is **−0.0004** (95% range **[−0.0526, +0.0966]**) in log public enrolment and **+0.0041** (**[−0.0289, +0.0431]**) in log active public schools (pre-transfer `RMSPE` **0.0140** vs **0.0134**; baseline cross-validated `AUC = 0.5341`, permutation `p = 0.2195`).
- **`SAE` (Exact Fisher Permutation & Webb 2023 Wild Cluster Bootstrap):** With only **4** treated regions and **10** control regions (**14** historical regions), equal commune-grade weighting yields `HHI` **+0.0035** (**[−0.0104, +0.0174]**) and log effective schools **−0.0042** (**[−0.0265, +0.0181]**). Under equal historical-region weighting, `HHI` is **+0.0053** with **exact Fisher permutation** across all **1,001** possible regional assignments giving `p = 0.7133` and **Webb (2023) 6-point wild cluster bootstrap (`WCB`)** 95% CI **[−0.0160, +0.0267]**, while log effective schools is **−0.0142** (Fisher `p = 0.6703`; `WCB` CI **[−0.0580, +0.0292]**) and pre-treatment placebos fail under regional weighting.

Full bilingual article, interactive maps, and methodology: https://3cucharadas.cl/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/
