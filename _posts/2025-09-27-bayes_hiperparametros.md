---
layout: single
title: "Hiperparámetros con Bayes en H2O: guía práctica y reproducible"
subtitle: "Cómo orquestar Bayesian Optimization con modelos de H2O (GBM/XGBoost) en Python y R"
date: 2025-09-27
categories: [mlops, hpo, h2o]
tags: [bayesian-optimization, h2o, gbm, xgboost, skopt, reproducibilidad]
toc: true
toc_sticky: true
comments: true
author_profile: true
---

> **TL;DR**  
> Bayesian Optimization (BO) minimiza el **número de entrenamientos** para encontrar buenos hiperparámetros, modelando la función objetivo con un **surrogate** (p. ej., proceso gaussiano) y eligiendo el siguiente punto con una **función de adquisición** (p. ej., Expected Improvement). Aquí te muestro cómo **integrar BO con H2O** sin plugins comerciales, usando *scikit-optimize* en Python y *ParBayesianOptimization* en R.

---

## 1) ¿Por qué Bayes para H2O?

- **Menos evaluaciones** que grid/random search para espacios medianos-grandes.  
- Explora con “curiosidad informada” (trade-off explotación/exploración).  
- Funciona bien con **métricas ruidosas** (k-fold CV) y **espacios mixtos** (enteros, reales, categorías).

> **Idea clave**: minimizamos una función objetivo \( f(\theta) \) (p. ej., \(-\mathrm{AUC}\) o \(\mathrm{logloss}\)) sobre hiperparámetros \(\theta\). BO aprende una distribución sobre \(f\) y selecciona la próxima \(\theta\) maximizando la adquisición.

\[
\theta^\* = \arg\min_{\theta \in \Theta} \; f(\theta)
\qquad\text{con}\qquad
\theta_{t+1} = \arg\max_{\theta} \mathrm{EI}(\theta \mid \mathcal{D}_t)
\]

---

## 2) Setup y reproducibilidad

### Requisitos mínimos

- **Python ≥ 3.11**: `h2o`, `scikit-optimize`, `pandas`, `numpy`.
- **R ≥ 4.3** (opcional): `h2o`, `ParBayesianOptimization`.

```bash
# Python (entorno de proyecto)
python -m venv .venv && source .venv/bin/activate
python -m pip install -U pip
pip install h2o scikit-optimize pandas numpy
