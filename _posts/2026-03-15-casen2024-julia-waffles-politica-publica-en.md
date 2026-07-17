---
layout: single
title: "CASEN 2024 in 3 spoonfuls: without a fine-grained territorial reading, social policy moves blind"
date: 2026-03-15
categories: [datos, politica-publica, julia, casen]
tags: [casen2024, julia, expansion, sampling-design, waffle, dotplot, public-policy, bidat, territorial-gap]
description: "A reproducible analysis of CASEN 2024 in Julia: official validation against BIDAT data, national composition via waffle charts, and regional gaps in education, health and poverty for territorial prioritization."
author: clabra
lang: en
ref: casen2024-julia-waffles
permalink: /datos/politica-publica/julia/casen/casen2024-julia-waffles-politica-publica/
distribution:
  social: true
  republish: [dev, medium]
toc: true
toc_sticky: true
author_profile: true
header:
  teaser: /assets/images/teasers/teaser-casen-2024.webp
  og_image: /assets/images/casen2024-julia-waffles-politica-publica/waffle_trabajo_ingresos_pobreza.png

gallery_nacional:
  - url: /assets/images/casen2024-julia-waffles-politica-publica/waffle_educacion_educc.webp
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/waffle_educacion_educc.webp
    alt: "Chart 1: Distribution of the highest educational level attained in the adult population (≥18 years), Chile, CASEN 2024. A 100-cell waffle chart with proportions by largest remainder."
    title: "Chart 1 — Education: highest educational level attained (population ≥18 years, CASEN 2024)"
  - url: /assets/images/casen2024-julia-waffles-politica-publica/waffle_salud_s13.webp
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/waffle_salud_s13.webp
    alt: "Chart 2: Distribution of the health insurance system to which the population belongs, Chile, CASEN 2024. A waffle chart with 6 categories including FONASA, Isapre and others."
    title: "Chart 2 — Health: health insurance system (total population, CASEN 2024)"
  - url: /assets/images/casen2024-julia-waffles-politica-publica/waffle_trabajo_ingresos_pobreza.webp
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/waffle_trabajo_ingresos_pobreza.webp
    alt: "Chart 3: Income poverty status in Chile according to CASEN 2024: extreme poverty, non-extreme poverty and non-poverty. A 100-cell waffle chart."
    title: "Chart 3 — Income poverty: extreme, non-extreme and non-poverty (total population, CASEN 2024)"

gallery_regional:
  - url: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_educacion_educc.webp
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_educacion_educc.webp
    alt: "Chart 4: Dot plot of regional gaps in educational level by category, CASEN 2024. Each panel has its axis fitted to its own range; dashed vertical line = national reference and grey band = national 95% CI."
    title: "Chart 4 — Regional gaps in education: dot plot by category (axis fitted per panel, dashed line = national, band = 95% CI)"
  - url: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_salud_s13.webp
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_salud_s13.webp
    alt: "Chart 5: Dot plot of regional gaps in the health insurance system by category, CASEN 2024. Axis fitted per panel with national reference."
    title: "Chart 5 — Regional gaps in health: dot plot by category (axis fitted per panel, dashed line = national, band = 95% CI)"
  - url: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_trabajo_ingresos_pobreza.webp
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_trabajo_ingresos_pobreza.webp
    alt: "Chart 6: Dot plot of regional gaps in income poverty, CASEN 2024. Axis fitted per panel with national reference."
    title: "Chart 6 — Regional gaps in poverty: dot plot (axis fitted per panel, dashed line = national, band = 95% CI)"
---

In Chile, **La Araucanía records 13.0% extreme poverty; Magallanes, 4.2%**. That is 8.8 percentage points of difference — and if a public agency at the central or local level (regional governments / municipalities) designs its intervention using only the national average (6.9%), or disregarding regional differences, it could get the allocation of resources or the distribution of its components wrong.

This post documents a reproducible analysis of CASEN 2024 in [Julia](https://julialang.org), with cross-validation of official public figures against BIDAT and good traceability of the flow in the repo.

**Three findings to start with — statistically robust:**

- **Extreme poverty**: La Araucanía 13.0% 95% CI [11.8%, 14.1%] versus Magallanes 4.2% [3.1%, 5.2%] — a gap of **8.8 pp with non-overlapping CIs**.
- **FONASA coverage**: La Araucanía 91.1% [90.2%, 92.0%] versus Metropolitana 75.9% [75.0%, 76.7%] — a gap of **15.2 pp with non-overlapping CIs**.
- **Completed higher education**: Metropolitana 34.9% [34.0%, 35.7%] versus Maule 20.4% [19.2%, 21.6%] — a gap of **14.5 pp with non-overlapping CIs**.

The CIs are 95% and were computed by **Taylor linearization** ([wiki](https://en.wikipedia.org/wiki/Linearization)) for CASEN's complex sampling design (stratified two-stage, `expr` weights). That the CIs do not overlap implies these regional differences are statistically significant at the conventional level.

---

## Tolerance to contrast, or checking against official data

All results were checked against the official tables available in [BIDAT](https://bidat.gob.cl/url/695ff7271b10e).

{: .table-caption}
**Table 1** — Official validation results (BIDAT, CASEN 2024)

| Parameter | Value |
|-----------|-------|
| Validation status (national + regional, % + expanded) | **PASS** |
| Maximum tolerance in percentage points | 1×10⁻⁵ pp |
| Maximum tolerance in expanded values | 1×10⁻⁶ |
| Observed difference (pp) | 2.98×10⁻⁶ pp |
| Observed difference (expanded) | 0.0 |
| National rows compared | 16 |
| Regional rows compared | 256 |

The maximum observed difference is below 3 millionths of a percentage point and within the preset tolerance. **The results match the official tables within the predefined tolerances.**

---

## Spoonful 1: sampling design and expansion without shortcuts

CASEN 2024 has a **probabilistic stratified two-stage** design ([BIDAT methodological note](https://bidat.gob.cl/url/69b71c77197db)). For regional-level estimates, the correct factor is `expr`; for the municipal level `expc` is required — they are not interchangeable. This analysis uses `expr` and reports estimates by region with 95% CIs computed by **Taylor linearization** over the complex design (strata, PSU/UPM and weights/factors).

Population represented in this run (sum of `expr`): **20.13 million people** (a pending task is to assess the impact of the new 2024 Census instead of projections over the 2017 Census).

```julia
# CASEN 2024 sampling design specification
design = (
    weight = :expr,     # regional expansion factor
    strata = :estrato,  # sampling stratum
    psu    = :cod_upm,  # primary sampling unit (PSU)
    domain = :region,   # estimation domain
)
```

Coverage by analyzed dimension:

{: .table-caption}
**Table 2** — CASEN 2024 variables used and target population

| Dimension | CASEN variable | Target population |
|-----------|----------------|--------------------|
| Education | `educc`        | People ≥ 18 years |
| Health    | `s13`          | Total population   |
| Poverty   | `pobreza`      | Total population   |

### Weighted national results

The following percentages correspond to proportions weighted with `expr`, validated against official data in BIDAT. The difference from the official values is < 3×10⁻⁶ pp.

{: .table-caption}
**Table 3** — Weighted national distribution (CASEN 2024, main categories)

| Dimension | Category | % national |
|-----------|-----------|:----------:|
| Education | Complete secondary | 30.9% |
| Education | Complete higher education | 29.1% |
| Education | Incomplete higher education | 12.5% |
| Education | Incomplete secondary | 9.9% |
| Education | Incomplete primary | 8.4% |
| Education | Other | 7.7% |
| Education | No formal education | 1.5% |
| Health | Public system FONASA | 82.6% |
| Health | Isapre | 13.2% |
| Health | None (private out-of-pocket) | 2.0% |
| Health | Armed forces and police | 1.8% |
| Health | Does not know | 0.3% |
| Health | Other system | 0.2% |
| Poverty | Non-poverty | 82.7% |
| Poverty | Non-extreme poverty | 10.4% |
| Poverty | Extreme poverty | 6.9% |

---

## Spoonful 2: the technical flow in Julia

The pipeline runs end to end with `julia --project=. scripts/run_all.jl` (the orchestrator). The two most relevant pieces of code to reproduce and "audit" these results are the cell-allocation algorithm and the sampling-design specification, available in the [public repository](https://github.com/tatanlabra/casen24_julia_viz).

### Taylor linearization: SE and CI of the complex design

A Taylor estimator was implemented for proportions in domains (regions). The linearized variable for the proportion $\hat{p}_d$ in domain $d$ is:

$$z_j = \frac{1(j \in d)\,(1(\text{cat}_j = C) - \hat{p}_d)}{\hat{N}_d}$$

The variance is estimated with the stratified cluster-design formula:

```julia
# Taylor linearization variance (stratified, PSU)
# e_{hi} = sum of w_j * z_j over PSU i in stratum h
var_total = sum over strata h:
    (n_h / (n_h - 1)) * sum_i (e_{hi} - mean(e_h))^2

se    = sqrt(var_total)
ci_lo = clamp(p̂ - 1.96 * se, 0.0, 1.0)
ci_hi = clamp(p̂ + 1.96 * se, 0.0, 1.0)
```

All PSUs of the design are used (including those outside the domain, with $z_j = 0$), which is correct for random-domain estimation. The median regional 95% CI width is **1.66 pp**; the maximum is **5.76 pp** (small regions with low-prevalence categories).

> **Next entry, at some point 👀 — Jackknife and Bootstrap for CASEN as a contrast:** TSL is an optimal first-order approximation for means and proportions, but for non-linear statistics (Gini, medians, quantile ratios) it can under-estimate the variance. The [code repository](https://github.com/tatanlabra/casen24_julia_viz/blob/main/docs/ic-varianza-casen.md) includes the theory and the in-progress Julia code to contrast TSL with Jackknife (delete-1) and Bootstrap — a future entry in this series, which I have not reviewed in depth.

### Largest remainder: why it matters in a waffle chart

A 100-cell waffle chart requires the proportions to add up to exactly 100 whole cells. Direct rounding introduces accumulated errors that make the sum 99 or 101. This flow uses the **largest remainder** algorithm, which guarantees the exact sum by introducing a slight imprecision for the sake of the visualization (take it as a purely visual nicety):

```julia
"""
Allocate `n_cells` whole cells to proportions `p` using largest-remainder.
Guarantees that sum(cells) == n_cells exactly.
"""
function allocate_cells(p::AbstractVector{<:Real}, n_cells::Int = 100)
    raw    = p .* n_cells
    floors = floor.(Int, raw)
    remain = raw .- floors
    deficit = n_cells - sum(floors)
    # Assign remaining cells to the proportions with the largest remainder
    idx = sortperm(remain, rev=true)[1:deficit]
    floors[idx] .+= 1
    return floors
end
```

Validated with unit tests: `allocate_cells([0.5, 0.3, 0.2], 100) == [50, 30, 20]`.

### Reproducibility

```bash
# Requirements: Julia 1.10+
git clone <repo>
cd casen2024/julia_viz
julia --project=. -e "using Pkg; Pkg.instantiate()"
julia --project=. scripts/run_all.jl
```

The flow generates plenty of artifacts (CSV tables, PNG charts, audit logs for each input). The `Manifest.toml` file pins the exact versions of all dependencies (I used Julia 1.10).

---

## Spoonful 3: visual evidence

### National composition (Charts 1–3)

Each waffle represents 100 cells allocated by largest remainder over the weighted proportions.

{% include gallery id="gallery_nacional" layout="third" caption="**Charts 1–3** — National composition: education (population ≥18 years), health and poverty (total population). Source: CASEN 2024, own elaboration in Julia. Values are validated against BIDAT. Click to enlarge." %}

### Regional gaps (Charts 4–6)

Each panel uses an **axis fitted to the range of its own category** (not a shared global scale), which makes it possible to visualize differences that flatten out if all categories share the same axis. The **horizontal bars** are 95% CIs computed by Taylor linearization; the dashed vertical line marks the national estimate and the pale grey band its 95% CI.

{% include gallery id="gallery_regional" layout="third" caption="**Charts 4–6** — Regional gaps with 95% CIs (Taylor linearization, complex design): education, health and poverty. Bars = regional 95% CI; dashed line = national estimate; grey band = national 95% CI. Axis fitted per category. Click to enlarge." %}

### Gaps with 95% CIs — all statistically robust

{: .table-caption}
**Table 4** — Regional gaps with 95% CIs by Taylor linearization (CASEN 2024)

| Dimension | Category | Gap (pp) | Maximum | 95% CI | Minimum | 95% CI |
|-----------|-----------|:-----------:|--------|---------|--------|---------|
| Poverty | Non-poverty | **18.6 pp** | Magallanes 90.0% | [88.5%, 91.5%] | La Araucanía 71.4% | [69.8%, 73.0%] |
| Health | Isapre | **16.3 pp** | Metropolitana 20.6% | [19.8%, 21.5%] | Maule 4.3% | [3.7%, 5.0%] |
| Health | FONASA | **15.2 pp** | La Araucanía 91.1% | [90.2%, 92.0%] | Metropolitana 75.9% | [75.0%, 76.7%] |
| Education | Complete higher education | **14.5 pp** | Metropolitana 34.9% | [34.0%, 35.7%] | Maule 20.4% | [19.2%, 21.6%] |
| Poverty | Extreme poverty | **8.8 pp** | La Araucanía 13.0% | [11.8%, 14.1%] | Magallanes 4.2% | [3.1%, 5.2%] |

In every case the CIs do not overlap: the gaps are statistically significant at 5%. CIs computed by Taylor linearization over the complex design (strata, PSU/UPM, `expr`).

---

## Closing: three questions for those who use the survey

If you use CASEN 2024 for territorial characterization or other uses where regional-level variables matter, think twice before using a point estimate (without its confidence interval):

1. **Are your results validated against BIDAT and do they carry design-based CIs?** A difference greater than 1×10⁻⁵ pp from the official tables is not technical: it is a process issue. And without complex-design CIs, an 8 pp gap can look like evidence when it is noise in small regions.
2. **Are you using the correct expansion factor?** `expr` is the right one for regions; `expc` for municipalities. They are not interchangeable, and using the wrong one biases coverage estimates.
3. **Is your analysis reproducible?** A flow that cannot be audited cannot be defended before a technical counterpart, nor updated when CASEN 2026 is released.

The CIs incorporated here are complex-design (Taylor linearization), not simple asymptotic ones. They cover sampling variance but not non-response error or undercoverage. Causal inference between subpopulations requires additional design.
