# Propuesta para r/dataisbeautiful (requiere verificar reglas vigentes desde sesión humana antes de enviar)

## Tipo de envío
- Imagen / Enlace con etiqueta `[OC]`: usar `assets/images/tesis-post4/selection-ladder-en-light.png` o enlace directo al artículo en inglés.

## Título propuesto
[OC] Do school closures close the door to higher education? Selection vs. causal effect across 20 years of school and SIES higher-education records in Chile (2007–2026)

## Primer comentario obligatorio de nivel superior (requerido por la Regla 3 de r/dataisbeautiful)

**Data source:**
Nationwide longitudinal administrative microdata from Chile’s Ministry of Education (`MINEDUC`, *Centro de Estudios* and `SIES`), linking **79,709,054** school enrollment records and **73,873,835** academic performance records (`2004–2025`), **20** annual SIES higher-education enrollment rosters (`2007–2026`), **19** SIES graduation rosters (`2007–2025`), and **6** open-access PAES/PDT centralized university admission cycles (`2021–2026`).
- Full bilingual article and methodology: https://3cucharadas.cl/en/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/
- Open tabular CSV data for the three figures:
  - https://3cucharadas.cl/assets/data/tesis-post4/selection-ladder-data.csv
  - https://3cucharadas.cl/assets/data/tesis-post4/longitudinal-regimes-data.csv
  - https://3cucharadas.cl/assets/data/tesis-post4/causal-ml-heterogeneity-paes-data.csv

**Tools used:**
DuckDB, Apache Parquet, and Python (`scikit-learn`, `interpret` Explainable Boosting Machine, and `matplotlib`) for repeated-cohort difference-in-differences (`G−1` vs. `G−5`), Double/Debiased Machine Learning (`DML PLR`, **Chernozhukov et al. 2018**), Hájek Doubly Robust `DR-ATT`, and an `Orthogonal R-Learner` (**Nie & Wager 2021**) with **Chernozhukov et al. (2025)** `BLP / GATE / CLAN` heterogeneity tests and **Cinelli & Hazlett (2020)** omitted-variable sensitivity.

**What the three-rung selection ladder shows (`N = 62,153` in the primary `2016–2019` window with complete `G−5` school history):**
1. **Rung 1 (Demographic baseline at G−1):** Comparing displaced secondary students (`1.°` to `3.° Medio`) only against peers of the same sex, age, grade, region, rurality, and provider type yields an apparent drop of **−13.24 pp** (`SE 2.94 pp`) in `DML PLR` (**−14.64 pp** in exact cells).
2. **Rung 2 (+ Student's prior academic backpack at G−1 and G−2):** Adding pre-closure GPA (`NEM`), attendance, prior repetition, and school stability cuts the gap by **57.5%** to **−5.63 pp** (`SE 2.12 pp`).
3. **Rung 3 (+ School's prior baseline at G−5, four years before closure):** In repeated-cohort DiD (`G−1` vs. `G−5`), **82.0%** of the raw gap (**−12.00 pp**) was already present four years before closure, reducing the DiD estimate to **−2.64 pp** (`SE 2.22 pp`) and the full `DML PLR` estimate to **−0.29 pp** (`SE 1.20 pp`; `EBM`: **−0.91 pp**; Hájek `DR-ATT`: **+0.19 pp**). However, entry into vocational-technical higher education (`IP/CFT`) contracts by **−2.09 pp** (`SE 0.72 pp`, `95% CI [−3.50, −0.68]`, `p = 0.0037`) in the full `DML` model, **−2.59 pp** in `2016–2019` DiD, and **−4.33 pp** during the `2020–2022` pandemic closures.
