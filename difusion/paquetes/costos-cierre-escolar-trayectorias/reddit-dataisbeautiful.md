# Propuesta para r/dataisbeautiful (requiere verificar reglas vigentes desde sesión humana antes de enviar)

## Tipo de envío
- Imagen / Enlace con etiqueta `[OC]`: usar `assets/images/tesis-post3/cohort-series-infographic-en-light.png` (la versión en inglés de la Figura 3 rediseñada con geometría validada sin solapamientos) o enlace directo al artículo en inglés.

## Título propuesto
[OC] 20 years of school closures and student trajectories in Chile (79,709,054 enrolment records, 2005–2024): staggered DiD estimates, regime attenuation, and pre-closure baseline gaps

## Primer comentario obligatorio de nivel superior (requerido por la Regla 3 de r/dataisbeautiful)

**Data source:**
Nationwide longitudinal administrative microdata from Chile’s Ministry of Education (`MINEDUC`, *Centro de Estudios*), linking **79,709,054 enrolment records** and **73,873,835 annual academic performance records** from **2004 to 2025**.
- Full bilingual article and methodology: https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/
- Open tabular CSV data for this chart: https://3cucharadas.cl/assets/images/tesis-post3/cohort-series-infographic-data.csv

**Tools used:**
DuckDB and Python (`matplotlib` + DTCG design-token validator) for data processing, exact $G-1$ matching, staggered difference-in-differences estimation (**Callaway & Sant'Anna 2021**), **Manski (2003)** missing-data bounds, and automated bounding-box collision verification.

**What the three panels show (and what they do *not* prove):**
1. **Panel A (Annual cohorts, 2006–2024):** Under our Data-Inferred School Closure Rule (`RCID v1`, which filters out *de facto* mergers where a single school absorbs $\ge 70\%$ and $\ge 15$ relocated students, leaving **1,141 supported closure episodes**, **78,972 exposed observations**, and **734,472 controls**), all **19 estimable annual cohorts** for 1-year progression failure or grade lag are positive (ranging from **+0.94 pp** in 2021 to **+28.22 pp** in 2010; median **+7.18 pp**). The student-weighted Callaway & Sant'Anna aggregate is **+9.11 pp** (95% CI: **+5.34 to +12.88**; Manski bounds: **+0.43 to +16.21 pp**), and the inverse-variance weighted aggregate is **+5.14 pp** (**+4.34 to +5.95**).
2. **Panel B (Institutional regimes):** Rather than increasing over time, the post-closure progression gap attenuated across policy regimes—from **+12.15 pp** in **2005–2010** and **+7.82 pp** in **2011–2015** to **+5.29 pp** in our primary **2016–2019** window (95% CI: **2.08 to 8.51 pp**, but **inconclusive** on its own once worst-case Manski missing-data bounds of **−1.15 to 10.98 pp** are applied), **+2.70 pp** in **2020–2022**, and **+2.59 pp** in **2023–2024**.
3. **Panel C (Pre-closure baseline gaps at $G-1$):** Why we refuse to call this a pure causal effect of closure: while individual poverty eligibility (`SEP`) is balanced after exact matching (**−1.07 pp** gap; **30.68%** priority students), exposed students came from schools with fewer `SEP` agreements (**−10.06 pp**), less full-day schooling (**−18.54 pp**), lower valid baseline record coverage (**−19.24 pp** in the series / **−19.4 pp** in 2016–2019), and **+16.52 pp** higher prior school switching (**47.04%** of exposed students had already switched schools between $G-3$ and $G-1$, vs. **30.52%** of controls).
