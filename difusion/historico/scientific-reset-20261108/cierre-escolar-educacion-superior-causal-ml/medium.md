# Medium Import Draft — Do School Closures Close the Door to Higher Education?

> **Canonical URL (must be set in Medium Advanced Settings before publishing):**
> `https://3cucharadas.cl/en/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/`

When a high school shuts down, the immediate policy debate revolves around finding nearby seats for displaced students by the start of the next school year. Yet for teenagers in the middle of secondary education, a deeper question looms: what happens years later when it is time to cross into higher education?

Across 20 years of linked administrative records in Chile (`79,709,054` school enrollments and `73,873,835` academic performance records linked to **20** annual SIES higher-education rosters from `2007` to `2026`, **19** graduation rosters from `2007` to `2025`, and **6** centralized university admission cycles from `2021` to `2026`), a naive comparison suggests a large penalty. Displaced secondary students (`1.°` to `3.° Medio`) enter higher education within two years of theoretical graduation at a rate **−13.24 percentage points** (`SE 2.94 pp`) lower in Double/Debiased Machine Learning (**−14.64 pp** in exact demographic cells) than peers of the same sex, age, grade, region, rurality, and school type.

## Climbing the Selection Ladder (`N = 62,153`)

Why is that raw gap misleading? Because schools do not close at random, and students who remain in a school until its final year carry a distinct prior trajectory:
1. **Adding the student's prior academic backpack (`G−1` and `G−2`):** Controlling for pre-closure GPA (`NEM`), attendance, prior repetition, and mobility cuts the gap by **57.5%**, down to **−5.63 pp** (`SE 2.12 pp`).
2. **Adding the school's own pre-closure baseline (`G−5`):** Comparing the closing cohort (`G−1`) against an earlier cohort (`G−5`) from the exact same school four years before closure reveals that **82.0%** of the apparent gap (**−12.00 pp**) was already present four years before the school closed. Once both student and school history are controlled for, the overall secondary effect narrows to **−2.64 pp** (`SE 2.22 pp`) in repeated-cohort difference-in-differences and **−0.29 pp** (`SE 1.20 pp`) in full `DML PLR` (**−0.91 pp** with Explainable Boosting Machines; **+0.19 pp** with Hájek `DR-ATT`).

## The Vocational-Technical Bridge (`IP/CFT`) and Vulnerable Students (`G1`)

Look beneath the overall average, however, and a specific channel contracts:
- **Vocational-technical higher education (`IP/CFT`) drops by −2.09 pp** (`SE 0.72 pp`, `95% CI [−3.50, −0.68]`, `p = 0.0037`) even after controlling for full student and `G−5` school history (the regime-level DiD point estimates, **−2.59 pp** in `2016–2019` and **−4.33 pp** during the `2020–2022` pandemic closures, point the same way but are imprecise with so few closing high schools per regime), while university entry moves **+1.98 pp** (`[−0.22, +4.19]`). Whether that pattern reflects a net loss of vocational-technical transitions or partial upward substitution into universities when displaced students enter academically stronger receiving high schools is a key mechanism question examined in the full piece.
- **Concentration in the most vulnerable quintile (`G1`):** Using an `Orthogonal R-Learner` (`BLP / GATE / CLAN`), the quintile with the largest predicted harm (`G1`: **99.5%** secondary students, **77.2%** vocational track, **87.1%** prior attendance) suffers a **−12.26 pp** drop in higher-education entry (**−8.02 pp** in `IP/CFT` and **−11.48 pp** in 2-year persistence) when only individual history is controlled for—a gap absorbed (**−0.26 pp**) once `G−5` school fragility is accounted for.

Read the complete bilingual analysis with interactive light/dark figures and open CSV datasets at [3cucharadas.cl](https://3cucharadas.cl/en/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/?utm_source=medium&utm_medium=syndication&utm_campaign=tesis_post4).
