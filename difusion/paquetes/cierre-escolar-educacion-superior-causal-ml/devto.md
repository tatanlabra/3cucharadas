---
title: "Causal ML over 20 Years of Linked School and Higher-Education Microdata in DuckDB: Selection vs. School Closure Effects"
published: false
description: "How I linked 79,709,054 school enrollment records and 20 annual SIES higher-education rosters in DuckDB/Parquet to run repeated-cohort DiD, Double ML, and an Orthogonal R-Learner."
tags: datascience, python, duckdb, machinelearning
canonical_url: https://3cucharadas.cl/en/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/
---

In Part IV of my school-closure research series on [3cucharadas.cl](https://3cucharadas.cl/en/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/), I needed to link **79,709,054** annual school enrollment records and **73,873,835** performance records (`2004–2025`) with **20** annual SIES Higher Education Enrollment rosters (`2007–2026`), **19** graduation rosters (`2007–2025`), and **6** centralized university admission cycles (`PAES/PDT`, `2021–2026`).

## 1. Columnar Ingestion (`DuckDB` + `Apache Parquet ZSTD`)

Consolidating the 57 official microdata packages (CSV inside RAR archives, each verified by SHA-256 receipt) into Apache Parquet tables brought the full longitudinal cross across 20 years of masked individual identifiers (`MRUN`) from hours to under 25 seconds on a single local workstation. The first run on real data also surfaced a join bug (a subquery dropping the origin school code) that simulated data had never triggered.

## 2. Identification Ladder (`G−1` vs. `G−5`) and Orthogonal ML (`N = 62,153`)

Using 5-fold school-clustered cross-fitting (`GroupKFold(5)` by school `RBD`) so students from the same school never split across train and test folds:
- **Rung 1 (Demographic baseline at `G−1`):** **−13.24 pp** (`SE 2.94 pp`) in `DML PLR` (**−14.64 pp** in exact cells).
- **Rung 2 (+ Student `G−1`/`G−2` academic backpack):** **−5.63 pp** (`SE 2.12 pp`), a **57.5%** reduction.
- **Rung 3 (+ School `G−5` baseline four years before closure):** **−2.64 pp** (`SE 2.22 pp`) in repeated-cohort DiD (**82.0%** of the raw gap existed at `G−5`: **−12.00 pp**) and **−0.29 pp** (`SE 1.20 pp`) in full `DML PLR` (**−0.91 pp** with `EBM`; **+0.19 pp** with Hájek `DR-ATT`).
- **Vocational-technical contraction (`IP/CFT`):** **−2.09 pp** (`SE 0.72 pp`, `95% CI [−3.50, −0.68]`, `p = 0.0037`) in full `DML`; the regime-level DiD point estimates (**−2.59 pp** in `2016–2019`, `p = 0.28`; **−4.33 pp** in `2020–2022` pandemic closures, `p = 0.18`) go the same way but are imprecise with **12** and **7** treated clusters. University entry moves **+1.98 pp** (`[−0.22, +4.19]`), so substitution toward universities is an open rival reading (`Cinelli–Hazlett` `RV_q1 = 6.16%`, `RV_alpha05 = 2.33%`).
- **`Orthogonal R-Learner` (`BLP / GATE / CLAN`):** `BLP` slope `β₂ = +0.634` (`p = 0.0243`) for overall entry and `β₂ = +0.800` (`p = 0.0007`) for `IP/CFT` (`β₂ = +0.425`, `p = 0.0177` with `G−5` controls); vulnerable quintile `G1` drops **−12.26 pp** before `G−5` controls and **−0.26 pp** after.

Full article, interactive charts, and downloadable CSVs: https://3cucharadas.cl/en/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/
