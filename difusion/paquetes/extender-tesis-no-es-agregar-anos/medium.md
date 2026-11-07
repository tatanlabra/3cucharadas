# Medium Import Draft — Why Extending a Research Panel Is Not Just Adding Years: What School Turnover in Chile Still Cannot Tell Us

> **Canonical URL (must be set in Medium Advanced Settings before publishing):**
> `https://3cucharadas.cl/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/`

When a school closes and another opens in the same city, it is tempting to tell a simple story of “creative destruction”: low-performing schools exit, better alternatives enter, and the system renews itself.

In Part II of my [*Extending My Thesis in Three Spoonfuls*](https://3cucharadas.cl/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/) series, I extended my 2014 thesis on Chilean schools across recent administrative directories (`2015–2025` for transitions between `2016` and `2025`, and `2013–2025` for entries). The central takeaway is methodological and public: **the administrative records clarify what changed in the school network, but they do not show that turnover improved educational outcomes.**

Meanwhile, demographic projections from Chile's National Statistics Institute (`INE`, 2024 Census) indicate that the school-age population (6 to 17) will fall from **3,081,791** in 2025 to **1,366,155** in 2050—a **55.7%** decline that makes transition planning unavoidable.

---

## 1. Not Every Vanishing Code Is a Closed School

Between 2016 and 2025, **900** official closures appear in Ministry of Education (`MINEDUC`) files: **684** from active schools, **215** from recess, and **1** without enrolment. Yet **338** of the **684** previously active schools already had zero students, leaving **346** with enrolled pupils.

After filtering out **16** annex closures, consolidations, and identifier (`RBD`) replacements, **330** strict closures (`D1`) remain. And when I track student flows using the **Data-Inferred School Closure Rule (`RCID v1`, `D2`)**—which removes **34** block absorptions where at least **70%** of $\ge 10$ students move together to a single stable receiving school with destination concentration `HHI` $\ge 0.50$—I am left with **296** conservative inferred closures and **266** clean dispersed closures with a complete post-closure year (setting aside **30** right-censored 2025 closures).

---

## 2. Empty Desks Before Closure, Missing Test Scores, and Empirical Bayes Shrinkage

Across **665** closures with three complete prior years, median enrolment falls **28 → 23 → 1** student before closure (**44 → 34 → 0** in `D1`, **39 → 31 → 0** in conservative `D2`, and **36 → 27 → 0** in clean `D2`).

Because closing schools are small and shrinking, only **76** (**11.1%** of **684**) have three complete years of standardised `SIMCE` test scores (medians **−0.232 → −0.235 → −0.083** SD) and **188** have school vulnerability `IVE-SINAE` (**0.882 → 0.910 → 0.946**). Among **330** strict closures, only **97** have `SIMCE` and **46** have university admissions (`PSU/PDT/PAES`). Exact commune matching leaves just **21** closures in `SIMCE` (**+0.029** SD, **[−0.095, +0.158]**; weighted **+0.034** SD **[−0.225, +0.289]**; **17** under `D2` at **+0.017** SD) and **8** in admissions (**−0.001** SD; **5** under `D2` at **−0.057** SD, below our minimum of **10** closures).

By relaxing blocking to the region and applying **Morris (1983) empirical Bayes shrinkage**, I recover **95 of 97** `SIMCE` closures (**97.9%**, **+0.0061** SD, **[−0.1467, +0.1715]**, vs **−0.0751** SD unshrunken) and **44 of 46** admissions closures (**95.7%**, **−0.0420** SD, **[−0.1352, +0.0616]**, vs **−0.0987** SD unshrunken). Both intervals span zero (**−0.15** to **+0.17** SD in `SIMCE`), and market-level turnover decompositions are virtually zero (**−0.000105** SD in `SIMCE`, **[−0.000346, +0.000103]**, and **+0.000113** SD in admissions, **[+0.000027, +0.000213]**).

---

## 3. Proximity on a Map Is Not Where Students Actually Go

Out of **330** strict closures (**320** geocoded) and **414** openings (**389** geocoded), only **38** closures have a new school serving the same education segment within **10 km** (`t` to `t+2`, across **29** unique openings; new-school cohorts have only **4/6/8** comparable cases in `SIMCE` and **1/1/2** in admissions). In my hometown of El Salvador, School No. **14** (`RBD` **391** at **500** Diego Portales) closed in 2013 and merged into School No. **1** (`RBD` **390** at **1510** Diego Portales) after combined enrolment fell **−30.2%** from **1,399** in 2004 to **977** in 2013 (with School No. 1 rising from **432** to **738** pupils in 2014).

Following **9,093** individual student transfers across **101** clean `D2` closures within a **15 km** choice set via a **McFadden (1974) conditional logit** shows that displaced students move a median of **1.83 km** (mean **2.89 km**), **73.4%** stay in the same commune, and destinations are driven by distance (`−0.4029` per km, `OR = 0.668`, `z = −5.34`), commune borders (`z = +5.24`), same sector (`z = +4.77`), and school size (`z = +8.08`)—not higher `SIMCE` scores (`−0.2311`, `OR = 0.794`, `z = −1.71`; mean realised change **−0.035** SD).

Finally, testing two flagship institutional reforms shows why observational schedules are not automatic natural experiments: across **25** Local Public Education Service (`SLEP`) territory-horizon pairs, **Synthetic DiD (Arkhangelsky et al. 2021)** yields **−0.0004** (**[−0.0526, +0.0966]**) in log public enrolment and **+0.0041** (**[−0.0289, +0.0431]**) in log active schools without pure synthetic support (`RMSPE` **0.0140** vs **0.0134**; diagnostic `AUC = 0.5341`, `p = 0.2195`), while for the School Admission System (`SAE`, **4** treated regions out of **14**), **exact Fisher permutation** (**1,001** assignments, `p = 0.7133` for `HHI` **+0.0053** and `p = 0.6703` for log effective schools **−0.0142**) and **Webb (2023) 6-point wild cluster bootstrap** (**[−0.0160, +0.0267]** and **[−0.0580, +0.0292]**; commune-grade weighted **+0.0035** **[−0.0104, +0.0174]** and **−0.0042** **[−0.0265, +0.0181]**) span zero and fail regional pre-trend placebos.

Read the complete bilingual analysis and interactive maps at [3cucharadas.cl](https://3cucharadas.cl/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/?utm_source=medium&utm_medium=syndication&utm_campaign=tesis_post2).
