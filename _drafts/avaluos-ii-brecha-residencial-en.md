---
layout: single
title: "Property assessments II: what could the residential gap represent in property taxes?"
subtitle: "Chile's largest differences between census dwellings and residential cadastral records, and the evidence needed to price them"
date: 2026-09-09 20:00:00 -0400
categories: [datos, territorio]
tags: [catastro-sii, census-2024, property-tax, open-data, inequality]
author: clabra
lang: en
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: false
editorial_status: pending-tax-reconciliation
description: "A commune-level comparison of Chile's 2024 Census and 2026 first-half cadastral data. Physical differences do not identify unpaid taxes."
excerpt: "A difference between registers can flag a problem. Converting it into money requires evidence about the units and the tax obligation."
header:
  teaser: /assets/images/avaluos-ii/gap-top15-en.png
math: true
toc: true
toc_sticky: true
comments: true
---

**Research draft: the monetary ranking remains pending reconciliation.** The available chart ranks physical differences. It does not show lost revenue or establish negligence by Chile's tax authority.
{: .notice--warning}

The [first property-assessment post](/en/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/) examined how changing a denominator changes the territorial story. This follow-up asks a harder question: when a commune has more census dwellings than residential cadastral records, how much of that difference might matter for property taxation?

The concern is legitimate: construction that meets the conditions for taxation should be recorded correctly. But subtracting two aggregate counts does not identify that construction, establish its tax obligation or reveal an unpaid peso. That distinction must survive the analysis.

## First spoonful: a difference that needs explaining

The comparison uses **all private dwellings in Chile's 2024 Census**, occupied and vacant, against **residential destination H records for the first half of 2026**. The cadastral source is a mirror extracted on 24 July 2026 and checked against official statistics. It is neither a direct SII download nor a September inventory. The [complete dataset](/catastro_sii_brecha/data/fiscal-gap/communes.json) preserves periods, extraction date and missing sources.

SII is Chile's tax authority. A *rol* is a cadastral identifier for a property; a *commune* is a local administrative area; CUT identifies communes in the official territorial classification. A dwelling is a census unit, while a household describes people living together. One building may contain many dwellings, and agricultural properties may contain homes excluded by a residential-H filter. Parent records and subdivisions create further mismatches.

Thus, **dwellings minus H records** diagnoses compatibility between two registers. It does not count homes without a cadastral identifier.

![Fifteen communes with the largest positive difference between private census dwellings and H records; physical diagnostic, not a tax ranking.](/assets/images/avaluos-ii/gap-top15-en.svg)

{% include avaluos-ii-top-en.html %}

Positive differences are sorted descending, with CUT as the tie-break. Bars start at zero. Antártica and Trehuaco have no source extract in this dataset and are excluded from this ranking; they remain explicitly missing in the complete table. Negative differences are retained too: they do not demonstrate that every property is correctly recorded.

The [INE defines the census universe](https://censo2024.ine.gob.cl/resultados/), while the [SII classifies properties by destination](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html). Construction, classification and administrative updates may change between the two dates. This is not a measure of growth from 2024 to 2026, because the units also differ.

The [official MINVU 2026 first-half spreadsheets](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/) provide an additional check: Trehuaco has 1,342 residential records and Antártica has zero. However, their national total is 6,057,949, exceeding the SII table by 1,799. Across communes covered by the mirror, those 1,799 additional records are distributed over 208 communes. The [full reconciliation](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) preserves both sources; it does not silently replace the chart's snapshot. A later revision is a hypothesis, not an enrollment date or evidence of unpaid tax.

## Second spoonful: translating the question into pesos

The proposed scenario is:

$$
B_c(q)=\max(V_{c,2024}-H_{c,2026H1},0)\;q\;\overline{T}_{c,annual\ equivalent}
$$

The mean will cover **all residential H records, including zeros**. It requires verified net tax for one semester, doubled to express an annual equivalent under that semester's conditions. This is not an observed annual tax bill or collected revenue. Monetary units are Chilean pesos (CLP), with no exchange-rate conversion.

q takes values 0, 0.25, 0.5 and 1. It asks what a hypothetical fraction of the difference would represent if assigned the average tax of the observed residential stock. **q = 1 is neither an estimated omission probability nor a demonstrated upper bound.** Properties actually omitted could have a different tax distribution. A common positive q rescales every bar without changing the order; commune-specific assumptions can change it.

The median across all records may be zero when zeros predominate. It will therefore accompany the mean, the positive share, and the mean and median among positive records. Multiplying an all-record mean by the positive share would discount zeros twice. Positive share times positive-case median is a separate typical-case scenario, not an expected value.

The current obstacle is specific: the [historical cadastral product definition](https://www.sii.cl/documentos/resoluciones/2010/2010-5.pdf) includes refuse charges and surtaxes in the semester field. The available extract does not separate these components. It also does not reconcile exactly with the national control. The [method and audit](/catastro_sii_brecha/data/fiscal-gap/method.md) document the discrepancy and the sources examined.

The [current SII commune CSV files](https://www.sii.cl/sobre_el_sii/estadisticas/estadisticas_bienes_raices_por_comuna.html) do provide tax components for the first half of 2026. Their net tax, however, covers all nonagricultural destinations, including commerce and offices. Dividing that amount by residential records would not yield a residential mean.

Renaming the column, taxing an average assessment or scaling the values to match a national total would not resolve this. Exemptions, progressive rates and benefits prevent those substitutions. We need commune-level residential net-tax totals and H counts for the same semester; medians require a distribution or official summary statistics. **There is currently no publishable ranking of communes by monetary gap.**

## Third spoonful: what would establish responsibility?

| Provisional explanation | Evidence that would distinguish it |
|---|---|
| Delayed cadastral updating | An identifiable property, construction date, enforceable obligation and later registration or update |
| Homes recorded under another unit or destination | Documentary and spatial links to existing parent, agricultural or other records |
| Incompatible dates or classifications | Comparable-period reconstruction and an audit of each register's rules |
| Extract or crosswalk error | Official-source recovery and corrected keys, omissions or duplicates |
| Census or mapping error | Independent evidence contradicting the census count, location or classification |

Each explanation has a possible rejection condition. The delay hypothesis weakens if the record already existed or no tax was due. The mirror-error hypothesis weakens if an independently reconciled official extract confirms the observation. Unit mismatch weakens when an individual linkage establishes a one-to-one correspondence. None of those checks is accomplished by the commune-level subtraction.

The audit found a concrete crosswalk error: the mirror's names were interchanged for codes belonging to Coyhaique, Aysén and Chile Chico. The corrected mapping updates dependent indicators; the [erratum preserves the previous and corrected values](/catastro_sii_brecha/data/fiscal-gap/method.md). Fixing that error changes the territorial story without identifying a single unpaid tax bill.

Institutional responsibilities also differ. The SII assesses properties and issues tax charges; the General Treasury, TGR, collects them. Charged and paid amounts are not interchangeable. Chile's [Common Municipal Fund redistributes property-tax resources](https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html), so a gross scenario associated with a commune would not automatically be revenue retained by its municipality.

A third post will examine the **Urban Construction Continuum (CCU)**: where the physical city grows, and whether that growth follows a pattern compatible with the discrepancies. Expansion must be distinguished from densification, and the CCU's dependence on census inputs must be checked. An extension can increase the assessment of an existing property without creating another cadastral record. Without administrative event dates, we cannot measure delay; without an enforceable obligation, we cannot measure lost tax resources.

[Explore the diagnostic in the existing viewer (Spanish)](/catastro_sii_brecha/#brecha-contribuciones) · [Download CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv) · [Method, sources and erratum (Spanish)](/catastro_sii_brecha/data/fiscal-gap/method.md).
