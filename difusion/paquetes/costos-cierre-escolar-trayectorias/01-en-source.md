# What Happens to Students When a School Closes? Twenty Years of Administrative Trajectories, Missing-Data Bounds, and Staggered DiD in Chile

*Originally published on [3 Cucharadas](https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/) (in [Spanish](https://3cucharadas.cl/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/) and [English](https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/)) as the third instalment of the “Extending My Thesis in Three Spoonfuls” series.*

When a school closes, policy discussions often stop at the map: if another school with open seats sits a mile away, the transition is assumed to be covered. Yet buildings on a map do not tell us whether displaced students stayed enrolled the following year, progressed to the expected grade, or absorbed a hidden disruption. Above all, a map cannot separate what happened *because* of the closure from trajectories that were already fraying before the school shut its doors.

In this third instalment, we move from school-level maps to individual student trajectories across twenty years of nationwide administrative records from Chile’s Ministry of Education (`MINEDUC`), linking **79,709,054 enrolment records** and **73,873,835 annual academic performance records** between 2004 and 2025.

The headline finding is an exercise in epistemic honesty:
- In our primary recent window (**2016–2019 closures**), the before-and-after increase in **progression failure or grade lag**—defined as having no enrolment record or being enrolled below the expected grade one year later—was **+5.29 percentage points** larger among exposed students than among exactly matched comparison students (conservative 95% confidence interval: **2.08 to 8.51 points**, across **4,815** exposed observations and **65,538** controls in **62** closure episodes).
- However, next-year grade progression is not observed for every student. Once we compute assumption-free **Manski (2003) bounds** for those missing records, the plausible interval spans **−1.15 to 10.98 percentage points**. Because that range crosses zero, the main-window estimate is **inconclusive**: on its own, it proves neither harm, benefit, nor a null effect.
- When we expand the lens to all **20 annual closure cohorts from 2005 to 2024** (**1,141** supported closure episodes, **78,972** exposed student-cohort observations, and **734,472** controls), all **19 estimable progression cohorts (2006–2024)** are positive, yielding a **Callaway and Sant'Anna (2021)** student-weighted aggregate of **+9.11 percentage points** (95% CI: **+5.34 to +12.88**; Manski bounds: **+0.43 to +16.21 points**, which do not cross zero) and an inverse-variance precision-weighted aggregate of **+5.14 points** (**+4.34 to +5.95**). Yet extended baseline profiling shows that **47.04%** of exposed students had already switched schools at least once during the two years *before* closure (versus **30.52%** of controls). Even across twenty years, an adjusted difference-in-differences gap captures a mix of closure disruption and pre-existing institutional fragility, not a randomised experiment.

---

## 1. Separating Paper Exits from Real Dispersions: The Data-Inferred School Closure Rule (`RCID v1`)

In massive administrative panels covering thousands of schools over two decades, researchers rarely have a physical legal dossier for every school exit. Sometimes a school’s administrative identifier—known in Chile as its `RBD` (*Rol Base de Datos*)—disappears from the directory because of an annex consolidation, a site relocation, or a *de facto* merger where the entire student body moves together to a single receiving school.

In the recent decade (**2016–2025**), **346 episodes** appear as schools with prior enrolment dropping to zero. Part II’s strict school-level rules pared that list to **330 strict closures**: **266** episodes show no contradictory student-flow signal, **15** are continuity candidates, **35** have unresolved flow alerts, and **30** are right-censored 2025 closures whose post-closure year (2026) has not yet elapsed (with **45** cross-cutting concentrated-flow alerts and **0** external institutional confirmations in this phase).

To ensure complete consistency across all three instalments (2005–2025), we formalise a falsifiable three-tier hierarchy—the **Data-Inferred School Closure Rule (`RCID v1`, D0 ⊃ D1 ⊃ D2)**:

| Rule stratum | Historical window (2005–2015) | Recent window (2016–2025) | Full longitudinal series (2005–2025) | Operational definition |
|---|---:|---:|---:|---|
| **D0:** Raw administrative exit | 1,635 | 346 | 1,981 | Positive enrolment in *t*−1, zero in *t*, and no subsequent teaching activity. |
| **D1:** Strict closure of educational provision | 1,477 | 330 | 1,807 | Purges subsequent reopenings, `RBD` code changes on the same site, and annexes. |
| **D2 = `RCID v1` (conservative)** | 1,382 | 296 | 1,678 | Requires ≥ 5 trackable students in *t*−1 and removes concentrated absorptions where a single receiver absorbs ≥ 70% of relocated students and ≥ 15 pupils in *t*. |
| **D2 = `RCID v1` (clean, observed *t*+1)** | 1,382 | 266 | 1,648 | Further requires observing the full *t*+1 year (excluding the 30 right-censored 2025 closures). |

Separating **D1** and **D2** prevents *de facto* mergers—where classmates move together into a single receiving building—from diluting the analysis of genuine closures that force families to search for seats one by one.

---

## 2. The 2016–2019 Post-Pilot Re-Estimation and the “Meeting Room” Problem

In the **2016–2019** primary window, **63** of **64** historical episodes retain comparable support (**6,190** exposed student-cohort observations out of **6,581**, matched against a support universe of **82,753** control observations). Across the **62 episodes** with observable follow-up for primary outcomes:

| Outcome | Estimated difference | Conservative 95% CI | Key analytical condition |
|---|---:|---:|---|
| **Persistent non-enrolment for two years** | **+0.63 pp** | [−0.77, 2.03] | 3,666 exposed vs. 49,944 controls; not labelled “dropout” because register absence does not reveal cause or emigration. |
| **Progression failure or grade lag (1 year later)** | **+5.29 pp** | [2.08, 8.51] | 4,815 exposed vs. 65,538 controls; **Manski missing-data bounds: [−1.15, 10.98] pp**. |
| **Attendance** | **−1.15 points** | [−2.40, 0.10] | **Exploratory and conditional** (58 episodes, 3,871 exposed vs. 63,591 controls; 62.5% vs. 76.8% valid-record coverage). |
| **Average mark (1.0–7.0 scale)** | **−0.06** | [−0.14, 0.01] | **Exploratory and conditional** (58 episodes, 3,871 exposed vs. 63,596 controls; observed performance records only). |

Including receiving schools inside an alternative comparison sample yields **+0.71 percentage points** for two-year non-enrolment ([−0.69, 2.12], across 3,670 exposed and 59,613 controls) and **+5.09 points** for progression failure ([1.94, 8.23], across 4,822 exposed and 79,058 controls). Changing the control pool shifts the sample, but does not eliminate the **−1.15 to 10.98 point** missing-data bounds.

Moreover, nominal school counts overstate effective sample size. Picture a **meeting room** with 62 closed schools where a handful of large closures account for most displaced students. Weighted by students, those 62 closures carry the independent information of only **21.1 effective episodes** for non-enrolment, **21.9** for progression, and **17.7** for attendance and marks.

---

## 3. Are We Comparing Like with Like? Pre-Closure Asymmetries at *G*−1

Our difference-in-differences specification matches exposed and control students exactly one year before closure (*G*−1) on calendar year, sex, region, school ownership type, rurality, education level, and starting grade. On standard baseline observables, the weighted groups look nearly identical: mean age is **11.70 years** in both groups, mean attendance is **90.93%** versus **91.68%**, and mean grade point average is **5.62** versus **5.67**. Yet valid performance-record coverage at *G*−1 is **76.8%** among exposed students versus **96.2%** among controls—a **−19.4 percentage-point** visibility gap before closure even occurs.

When we audit eight extended child-and-adolescent (`NNA`) and institutional descriptors between *G*−3 and *G*−1 across all **6,190** exposed and **82,753** control observations, a sharp contrast emerges:
- **Individual socioeconomic vulnerability is balanced:** priority low-income students under Chile’s Preferential School Subsidy (`SEP`, *Subvención Escolar Preferencial*) make up **30.68%** of exposed students versus **32.32%** of controls (−1.64 pp), total `SEP` eligibility is **54.51%** versus **55.58%** (−1.07 pp), and baseline over-age status (≥ 1 year above grade norm) is exactly **33.86%** in both groups.
- **Institutional provision and prior trajectory stability are not:** exposed students attended schools with lower effective `SEP` beneficiary coverage (**37.63%** vs. **48.58%**, −10.95 pp), fewer signed school-level `SEP` agreements (**45.17%** vs. **55.23%**, −10.06 pp), substantially lower Full School Day (`JEC`, *Jornada Escolar Completa*) provision (**53.97%** vs. **72.51%**, −18.54 pp), higher inter-municipality commuting (**38.59%** vs. **29.99%**, +8.60 pp), and far higher prior school switching: **47.04%** of exposed students had already changed schools at least once between *G*−3 and *G*−1, compared with **30.52%** of controls (**+16.52 pp**).

---

## 4. Why 2016–2019, and What Does the Full 2005–2024 Series Show?

The 2016–2019 window was selected as the primary specification for four technical reasons: official closure status (`ESTADO_ESTAB`) was standardised in 2015, multi-year pre-trends inside a panel starting in 2004 push cohorts toward the mid-2010s, **2020–2022** was distorted by COVID-19 school lockdowns and flexible promotion rules, and **2024–2025** is right-censored for two-year follow-up.

To verify that 2016–2019 was not cherry-picked, we estimate all **20 annual closure cohorts from 2005 to 2024** under `RCID v1` against clean not-yet-treated controls following **Callaway and Sant'Anna (2021)**, **Sun and Abraham (2021)**, and **Roth et al. (2023)**:

| Institutional regime / Range / Aggregate | Supported episodes | Exposed (*N*) | Controls (*N*) | Progression failure or lag (pp) | 95% CI progression (pp) | 2-year non-enrolment (pp) | 95% CI non-enrolment (pp) |
|---|---:|---:|---:|---:|---:|---:|---:|
| **2005–2010** (LOCE regime & early SEP) | 521 | 36,984 | 334,062 | **+12.15** | [+3.78, +20.52] | **+1.21** | [+0.53, +1.90] |
| **2011–2015** (LGE & SAC quality rollout) | 502 | 31,512 | 260,740 | **+7.82** | [+6.20, +9.41] | **+1.85** | [+1.10, +2.59] |
| **2016–2019** (main window; bounds [−1.15, 10.98] pp) | 63 | 6,190 | 82,753 | **+5.29** | [+2.08, +8.51] | **+0.63** | [−0.77, +2.03] |
| **2020–2022** (COVID-19 pandemic shock) | 33 | 3,272 | 42,457 | **+2.70** | [−0.63, +6.03] | **−0.28** | [−1.37, +0.81] |
| **2023–2024** (post-pandemic; 2024 censored at 2 yr) | 22 | 1,014 | 14,460 | **+2.59** | [−1.55, +6.73] | **−0.93** | [−2.64, +0.78] |
| **Annual range** (19 prog. / 17 non-enrol. cohorts) | 7 to 129 | 357 to 10,261 | 5,566 to 71,248 | **+0.94 to +28.22** (med: +7.18) | [+3.15, +9.62] (IQR) | **−0.93 to +4.56** (med: +0.92) | [+0.22, +2.11] (IQR) |
| **Full series 2005–2024 (Callaway & Sant'Anna)** | **1,141** | **78,972** | **734,472** | **+9.11** | **[+5.34, +12.88]** | **+1.38** | **[+0.92, +1.85]** |
| **Full series 2005–2024 (equal cohort weights)** | **1,141** | **78,972** | **734,472** | **+7.55** | **[+5.52, +9.57]** | **+1.03** | **[+0.56, +1.50]** |
| **Full series 2005–2024 (inverse-variance; *I*² = 76.48%)** | **1,141** | **78,972** | **734,472** | **+5.14** | **[+4.34, +5.95]** | **+0.54** | **[+0.29, +0.79]** |

Three patterns stand out:
1. **Monotonic attenuation across institutional regimes:** rather than inflating the effect, the 2016–2019 window reflects a long-run decline in the post-closure progression gap from **+12.15 pp** (2005–2010) and **+7.82 pp** (2011–2015) to **+5.29 pp** (2016–2019, with bounds **−1.15 to 10.98 pp**), as targeted school subsidies (`SEP`), quality assurance (`SAC`), and the Inclusion Law expanded.
2. **Consistent positive sign across all 19 estimable cohorts:** in the full series, the exposed-weighted Callaway and Sant'Anna aggregate reaches **+9.11 pp** and its Manski bounds (**[+0.43, +16.21] pp**) remain strictly positive, while inverse-variance weighting converges to **+5.14 pp**.
3. **Why neither staggered DiD nor Instrumental Variables turns observational data into a trial:** given pre-existing student mobility (**47.04%**) and a modest mean pre-trend deviation at *G*−2 of **−1.49 points** in the long series, causal claims remain sensitive to departures from parallel trends (**Rambachan and Roth 2023**). Moreover, candidate instruments such as Local Public Education Services (`SLEP`), the centralised School Admission System (`SAE`), or demographic shocks directly affect school resources, seat availability, and student sorting—violating the exclusion restriction. No instrumental-variable regression is therefore run in this version. Higher-education entry likewise remains deferred until individual microdata from `SIES` (Higher Education Information Service) and `DEMRE` (university admissions testing) are accredited.

---

## 5. Precautionary Safeguards for School Transitions

An inconclusive causal bound in the recent window does not justify policy passivity—it shifts the burden of proof onto educational authorities before, during, and after any closure:
- **Before deciding:** distinguish true closures from mergers or `RBD` code changes, record announcement dates, and verify real seat capacity, active `SEP` agreements, and Full School Day (`JEC`) provision in receiving schools.
- **During the transition:** guarantee nominal seat assignments, safe transport based on network travel time rather than straight-line distance, peer-group continuity, and receiving-school funding.
- **After the change:** track enrolment, attendance, grade progression, and valid performance records for every displaced student—and for incumbent students in receiving schools—for at least two years.

These precautionary safeguards are not estimated causal effects of those interventions; they are the minimum standard of public care required when a school closes.
