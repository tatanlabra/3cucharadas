# Propuesta para r/dataisbeautiful (requiere verificar reglas vigentes desde sesión humana antes de enviar)

## Tipo de envío
- Imagen / Enlace con etiqueta `[OC]`: usar `assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp` o `assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp` o enlace directo al artículo en inglés.

## Título propuesto
[OC] Auditing my 2014 thesis on school entry and exit in Chile (1992–2012): 2,168 entries, 2,069 exits, the 7-year "shadow of death" before closure, and what failed replication

## Primer comentario obligatorio de nivel superior (requerido por la Regla 3 de r/dataisbeautiful)

**Data source:**
Chilean Ministry of Education (`MINEDUC`) historical school directories (`1992–2012` and longitudinal extension `2004–2025`), audited against the original 2014 master's thesis producer files (`Stata` logs and `Excel` workbooks).
- Full bilingual article and methodology: https://3cucharadas.cl/en/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/

**Tools used:**
Stata and Python (`pandas`, `statsmodels`, `scikit-learn`, `matplotlib`) for forensic replication, **Mundlak (1978) and Chamberlain (1982)** correlated random effects (`CRE`) decomposition, out-of-sample discrete-time hazard (`cloglog`) validation, and the **Data-Inferred School Closure Rule (`RCID v1`)**.

**Key findings from auditing 34 thesis judgements and 50 technical hypotheses:**
1. **Audit balance:** **15** judgements held up, **10** errors came from the 2014 document (including a transcription error printing **0.003** instead of **0.001** from **0.000533**, two rows of untransformed log standard deviations where true random-intercept and residual variances were **265.6** and **2,079.7**, and a tenfold `HHI` scale bug putting Santiago at **1,534** instead of **152**), and **0** known errors remain in the 2026 reference output.
2. **Between-school sorting vs. within-school change (`N = 14,704` across `2,640` schools in Greater Santiago):** Replacing a collapsed random-slope mixed model (`2.1 × 10⁻¹⁵`) with a **Mundlak–Chamberlain `CRE`** decomposition shows that the positive association between lagged mathematics `SIMCE` and log enrolment is entirely between schools (`0.012131`, `t = 16.27`), while within-school annual changes flip sign and are indistinguishable from zero (`−0.000048`, `t = −0.53`).
3. **Seven-year “shadow of death” (`59,808` observations, 2004–2011) and out-of-sample risk ranking (`30,484` observations, 2007–2011):** Exiting schools see their pupil–teacher ratio drop from **17.95** to **12.22** over the seven years before exit (versus **20.31** among stayers). Trained on 2007–2008 (**12,495** rows, **86** closures) and tested on 2009–2011 (**17,989** rows, **151** closures), the `cloglog` hazard model achieves **AUC = 0.8517** (**43.7%** of closures in the top **10%** risk decile, **69.5%** in the top **20%** quintile), though Brier skill improves by only **1.5%** (**0.008196** vs **0.008324**) due to base-rate drift (**0.60%** predicted vs **0.84%** observed).
