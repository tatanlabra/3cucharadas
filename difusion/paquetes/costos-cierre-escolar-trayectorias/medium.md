# Instrucciones de publicación en Medium
# 1. Usar "Import a story" con la URL canónica en inglés:
#    https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/
#    o pegar el cuerpo de abajo y fijar manualmente el Canonical Link en Advanced Settings hacia esa misma URL.
# 2. Subtítulo sugerido: Linking 79.7 million enrolment records in Chile shows why a nearby school on a map is not educational continuity—and why missing-data bounds matter.
# 3. Tags sugeridos: Education Policy, Causal Inference, Data Science, Econometrics, Public Policy

# When a School Closes, What Actually Happens to Its Students?

When a school shuts down, the administrative response usually begins and ends with a map. If another school with empty desks sits a mile away, planners tend to assume the problem is solved.

Maps, however, track buildings rather than children. They do not tell us whether displaced students stayed enrolled the following year, advanced to the expected grade, or quietly dropped out of the administrative record. More importantly, a map cannot answer the hardest question in education policy: when students struggle after a school closure, how much of that setback was caused by the closure itself, and how much was already unfolding inside a fragile school before the doors closed?

In the third instalment of my [*Extending My Thesis in Three Spoonfuls*](https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/) series, I shifted the unit of analysis from school buildings to individual student trajectories across twenty years of nationwide administrative microdata from Chile’s Ministry of Education (`MINEDUC`), linking **79,709,054 enrolment records** and **73,873,835 annual performance records** from 2004 to 2025.

What emerged is a lesson in why honest bounds matter more than tidy point estimates.

---

## First: Not Every “Closed” School Actually Closed

Before measuring what happens to students after a closure, you have to make sure the school genuinely closed. In massive administrative directories, school identifiers—called `RBD` (*Rol Base de Datos*) in Chile—often vanish because of paperwork changes, annex consolidations, or *de facto* mergers where an entire student body walks into a new building together.

Across the full 2005–2025 panel, **1,981 schools** recorded positive enrolment one year and zero the next (**D0**). Filtering out subsequent reopenings and administrative continuities leaves **1,807 strict closures** (**D1**, including **330** in the 2016–2025 decade).

To separate genuine student dispersion from reorganisations where classmates move together, we introduced the **Data-Inferred School Closure Rule (`RCID v1`, D2)**: a school exit counts as a dispersed data-inferred closure only if it had at least 5 trackable students prior to closure and no single receiving school absorbed **70% or more** (and at least **15 students**) of its displaced pupils. That rule leaves **1,678 closures** across twenty years (**1,648** with a fully observed post-closure year).

---

## Second: A +5.29 Percentage-Point Gap—and Why Missing Records Make It Inconclusive

In our primary recent window (**2016–2019**), **63 closures** retain exact matching support (**6,190** exposed student-cohort observations matched one year prior to closure against **82,753** controls of the same calendar year, sex, region, school ownership type, rurality, education level, and starting grade).

Across the **62 episodes** with complete follow-up windows, we tracked two primary outcomes:
1. **Two-year persistent non-enrolment:** We avoid calling this “dropout” because disappearing from national school rolls does not by itself distinguish school abandonment from emigration or unrecorded modalities. The before-and-after change among exposed students exceeded controls by **+0.63 percentage points** (conservative 95% confidence interval: **−0.77 to 2.03 points**, across **3,666** exposed and **49,944** control observations).
2. **Progression failure or grade lag (one year later):** Defined as having no enrolment record or being enrolled below the expected grade the following year. Here the before-and-after change was **+5.29 percentage points** higher among exposed students than among controls, with a conservative 95% confidence interval from **2.08 to 8.51 points** (across **4,815** exposed and **65,538** control observations).

If we stopped at the confidence interval, the headline would write itself.

But progression is not observed for every student. And in baseline records one year before closure (*G*−1), valid attendance and grade records were available for **96.2%** of control students, compared with only **76.8%** of exposed students—a **−19.4 percentage-point** visibility gap. When we compute assumption-free **Manski (2003) bounds** for the missing progression records, the plausible range runs from **−1.15 to 10.98 percentage points**. Because those bounds cross zero, the 2016–2019 result is **inconclusive**.

There is also a concentration problem that standard sample sizes hide. Think of those 62 closed schools as a **meeting room**: because a few large closures account for a disproportionate share of students, listening to the student-weighted average is less like hearing 62 independent voices and more like hearing **21.9 effective episodes** for progression (**21.1** for non-enrolment, and just **17.7** for exploratory attendance and grade marks).

---

## Third: Comparing Like with Like Reveals Pre-Existing Fragility

Why were records already missing more often in schools that were about to close? To find out, we audited extended baseline descriptors for all **6,190** exposed and **82,753** control observations between *G*−3 and *G*−1.

On individual demographics and poverty, exact matching worked: both groups averaged **11.70 years** of age, had identical baseline grade lag (**33.86%**), and had virtually the same share of low-income priority students under Chile’s Preferential School Subsidy (`SEP`: **30.68%** among exposed vs. **32.32%** among controls; **54.51%** vs. **55.58%** total `SEP` eligibility).

On institutional stability, however, the two groups lived in different worlds:
- Exposed students attended schools with **−10.06 percentage points** lower `SEP` agreement participation (**45.17%** vs. **55.23%**) and **−18.54 percentage points** lower Full School Day (`JEC`) coverage (**53.97%** vs. **72.51%**).
- **47.04%** of exposed students had already switched schools at least once during the two years *before* closure (*G*−3 to *G*−1), compared with **30.52%** of controls (**+16.52 percentage points**).

Nearly half of displaced students were already experiencing school instability before their school closed.

---

## Fourth: What the Full 20-Year Staggered Series (2005–2024) Shows

Was the 2016–2019 window an outlier? Using **Callaway and Sant'Anna (2021)** staggered difference-in-differences across all **20 annual cohorts from 2005 to 2024** under `RCID v1` (**1,141** supported closures, **78,972** exposed observations, and **734,472** controls), we found the exact opposite:
- Across Chile’s successive institutional regimes, the post-closure progression gap attenuated steadily: from **+12.15 percentage points** in **2005–2010** (521 closures) and **+7.82 points** in **2011–2015** (502 closures) to **+5.29 points** in **2016–2019** (63 closures; bounds **−1.15 to 10.98 pp**), **+2.70 points** during the **2020–2022** pandemic, and **+2.59 points** in **2023–2024**.
- All **19 estimable annual progression cohorts (2006–2024)** are positive (ranging from **+0.94** to **+28.22 points**, median **+7.18**).
- The full-series Callaway and Sant'Anna exposed-weighted aggregate is **+9.11 percentage points** (95% CI: **+5.34 to +12.88**), with Manski bounds of **+0.43 to +16.21 points** that do not cross zero, while inverse-variance precision weighting (*I*² = 76.48%) yields **+5.14 points** (**+4.34 to +5.95**).

Even so, because closing schools already suffered from higher prior turnover and a **−1.49 point** pre-trend gap at *G*−2 in the long series (**Rambachan and Roth 2023**), and because policy reforms like Local Public Education Services (`SLEP`) or centralized admissions (`SAE`) directly affect seats and resources (failing the instrumental-variable exclusion restriction, so no instrumental-variable regression is run in this version), observational scale cannot substitute for a randomised design.

---

## Protecting Transitions Before Causality Is Settled

An inconclusive bound is not a license for administrative complacency—it shifts the burden of proof. Before closing or consolidating a school, authorities should verify real receiving-school seats, active `SEP` subsidies, Full School Day provision, and safe transport travel times, and then track every displaced student by name for at least two years. Those precautionary safeguards are not estimated causal effects; they are the baseline duty of care owed to students when a school closes.

*Read the full bilingual article, interactive light/dark SVG figures, and open CSV datasets at [3cucharadas.cl](https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/).*
