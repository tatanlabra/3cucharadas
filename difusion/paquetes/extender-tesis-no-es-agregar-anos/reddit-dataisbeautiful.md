# Propuesta para r/dataisbeautiful (requiere verificar reglas vigentes desde sesión humana antes de enviar)

## Tipo de envío
- Imagen / Enlace con etiqueta `[OC]`: el Post II no tiene exportación raster (solo SVG en `assets/images/extender-tesis-no-es-agregar-anos/`). Antes de enviar, rasterizar a PNG `resultados-v10-escalera-causal-en.svg` o `estilizada-trayectoria-simce-en.svg` (versión EN), o enviar como enlace directo al artículo en inglés.

## Título propuesto
[OC] Extending a school-turnover panel in Chile (2015–2025): from 900 official closures to 266 clean student-dispersal exits, 9,093 student relocations (median 1.83 km), and why staggered reform evaluations fail diagnostic gates

## Primer comentario obligatorio de nivel superior (requerido por la Regla 3 de r/dataisbeautiful)

**Data source:**
Chilean Ministry of Education (`MINEDUC`) official school directories, student enrolment rosters, `SIMCE` standardised assessments, and university admission records (`2013–2025`, plus `INE` 2024 Census demographic projections `2025–2050`).
- Full bilingual article and methodology: https://3cucharadas.cl/en/datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/

**Tools used:**
Python (`pandas`, `statsmodels`, `scipy`, `matplotlib`) for longitudinal student-roster linkage, the **Data-Inferred School Closure Rule (`RCID v1`)**, **Morris (1983)** parametric Empirical Bayes shrinkage, **McFadden (1974)** conditional logit discrete-choice modelling (`15 km` choice sets), **Synthetic Difference-in-Differences (Arkhangelsky et al. 2021)**, **exact Fisher permutation (`1,001` regional assignments)**, and **Webb (2023) 6-point wild cluster bootstrap (`WCB`)**.

**Key findings from the 2015–2025 extension:**
1. **Deconstructing 900 official closures (`RCID v1`):** Between 2016 and 2025, **900** official closures appear (**684** from active operation, **215** from recess, **1** without enrolment), but **338** already had zero students (`346` had active enrolment). Filtering out **16** annex/code replacements leaves **330** strict closures (`D1`), and removing **34** block-absorption transfers (`≥ 70%` of students moving to a single school with destination `HHI ≥ 0.50`) leaves **296** conservative `D2` closures and **266** clean `D2` closures with a full `t+1` window (**30** right-censored in 2025).
2. **`SIMCE` missingness & Morris (1983) Empirical Bayes shrinkage:** Only **76** closures (**11.1%** of **684**) have three prior years of `SIMCE`. Among the **330** strict closures, only **97** have `SIMCE` and **46** have admissions data; exact commune matching retains just **21** (`+0.029` SD, 95% CI **[−0.095, +0.158]**) and **8** closures. Regional **Empirical Bayes shrinkage** recovers **95 of 97** (**97.9%**) in `SIMCE` (`+0.0061` SD, **[−0.1467, +0.1715]** vs. `−0.0751` unshrunken) and **44 of 46** (**95.7%**) in admissions (`−0.0420` SD, **[−0.1352, +0.0616]**).
3. **Where displaced students actually go (`9,093` transfers across `101` closures):** Median transfer distance is **1.83 km** (mean **2.89 km**), **73.4%** stay in their home commune, and the mean `SIMCE` change is **−0.035** SD. In **McFadden (1974) conditional logit**, each kilometre lowers relative destination odds by one-third (`−0.4029`, `OR = 0.668`, `z = −5.34`) while destination `SIMCE` shows no positive pull (`−0.2311`, `OR = 0.794`, `z = −1.71`).
