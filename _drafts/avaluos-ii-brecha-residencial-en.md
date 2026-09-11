---
layout: single
title: "Property assessments II: what could the residential gap represent in property taxes?"
subtitle: "How much changes after discounting households counted in informal settlements, and the evidence needed to price the remainder"
date: 2026-09-09 20:00:00 -0400
categories: [datos, territorio]
tags: [catastro-sii, census-2024, property-tax, open-data, inequality]
author: clabra
lang: en
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: false
editorial_status: pending-tax-reconciliation
description: "A commune-level comparison of Chile's 2024 Census and 2026 first-half cadastral data, with an informal-settlement sensitivity."
excerpt: "Informal settlements explain an uneven part of the residential gap; substantial differences remain and require investigation."
header:
  teaser: /assets/images/avaluos-ii/gap-top15-en.png
math: true
toc: true
toc_sticky: true
comments: true
---

**Research draft: the monetary ranking remains pending reconciliation.** The chart compares the original gap with a sensitivity that subtracts census households in informal settlements. Neither bar shows lost revenue or establishes negligence by Chile's tax authority.
{: .notice--warning}

The [first property-assessment post](/en/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/) examined how changing a denominator changes the territorial story. This follow-up asks a harder question: when a commune has more census dwellings than residential cadastral records, how much of that difference might matter for property taxation?

The concern is legitimate: construction that meets the conditions for taxation should be recorded correctly. But subtracting two aggregate counts does not identify that construction, establish its tax obligation or reveal an unpaid peso. That distinction must survive the analysis.

## First spoonful: a difference that needs explaining

The comparison uses **all private dwellings in Chile's 2024 Census**, occupied and vacant, against **residential destination H records for the first half of 2026**. The cadastral source is a mirror extracted on 24 July 2026 and checked against official statistics. It is neither a direct SII download nor a September inventory. The [complete dataset](/catastro_sii_brecha/data/fiscal-gap/communes.json) preserves periods, extraction date and missing sources.

SII is Chile's tax authority. A *rol* is a cadastral identifier for a property; a *commune* is a local administrative area; CUT identifies communes in the official territorial classification. A dwelling is a census unit, while a household describes people living together. One building may contain many dwellings, and agricultural properties may contain homes excluded by a residential-H filter. Parent records and subdivisions create further mismatches.

Thus, **dwellings minus H records** diagnoses compatibility between two registers. It does not count homes without a cadastral identifier.

![Fifteen communes with the largest residual gap; each commune compares the original difference with the result after subtracting census households in informal settlements.](/assets/images/avaluos-ii/gap-top15-en.svg)

{% include avaluos-ii-top-en.html %}

Positive residuals after the sensitivity are sorted descending, with CUT as the tie-break. Bars start at zero. Antártica and Trehuaco have no source extract in this dataset and are excluded from this ranking; they remain explicitly missing in the complete table. Negative differences are retained too: they do not demonstrate that every property is correctly recorded.

## Informal settlements: what changes and what does not

[MINVU spatially linked its registry to the 2024 Census](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/vivienda-y-deficit/). In the 2024 snapshot it identified 1,373 settlements containing occupied dwellings, 81,993 dwellings and 77,399 households. The CNC 2026 layer used here contains 1,345 current polygons and a `HOGARESCEN` field: its numeric observations sum to 71,760 households, while 222 polygons are marked `S/I` or blank.

The sensitivity subtracts those observed households from each commune's gap under a strong assumption: **one census household in a settlement explains one dwelling that need not have a separate H record**. This is neither a dwelling-to-property linkage nor an observed correction. Where polygons lack a count, the calculation subtracts only known observations and labels the result partial.

| Commune | Original gap | Observed census households in settlements | Sensitivity residual | Share absorbed |
|---|---:|---:|---:|---:|
| Alto Hospicio | 15,368 | 9,136 | 6,232 | 59.4% |
| Antofagasta | 21,755 | 7,537 | 14,218 | 34.6% |
| Viña del Mar | 24,030 | 8,014 | 16,016 | 33.3% |
| Valparaíso | 32,533 | 2,572 | 29,961 | 7.9% |
| Puerto Montt | 29,036 | 632 | 28,404 | 2.2% |

Nationally, the sum of positive gaps falls from 1,588,449 to 1,516,689: 71,760 units, or 4.52%. The uneven effect is the central finding: settlements materially change some ranks but explain little of several leading gaps.

The Census also identifies dwellings considered irrecoverable because of type or materials. Applying the official algorithm to occupied private dwellings with residents yields 73,338. I do not subtract them: precarious materials do not establish irregular land tenure or absence of a cadastral record, and some dwellings may already fall inside the settlement polygons. Adding them would double-count an unknown overlap.

The historical anonymised settlement database is excluded too. It contains person and household observations associated with 2011–2021 surveys, including households that may have left the current registry. Treating it as a 2026 stock would mix periods and units; no individual row is published.

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

“Informal settlement” also does not mean “property the SII will never record.” [Law 17,235](https://www.bcn.cl/leychile/navegar?i=128563) taxes real property, and a cadastral identifier refers to a property rather than each dwelling; an occupation may lie within an existing parent property. Moreover, [article 16 of Law 20,234](https://www.bcn.cl/leychile/Navegar/imprimir?idNorma=268116&idParte=0) requires separate identifiers and assessments for sites in certain irregular subdivisions once they are regularised, works are accepted and deeds granted. Current informality does not establish permanent cadastral absence or a current tax obligation.

The audit found a concrete crosswalk error: the mirror's names were interchanged for codes belonging to Coyhaique, Aysén and Chile Chico. The corrected mapping updates dependent indicators; the [erratum preserves the previous and corrected values](/catastro_sii_brecha/data/fiscal-gap/method.md). Fixing that error changes the territorial story without identifying a single unpaid tax bill.

Institutional responsibilities also differ. The SII assesses properties and issues tax charges; the General Treasury, TGR, collects them. Charged and paid amounts are not interchangeable. Chile's [Common Municipal Fund redistributes property-tax resources](https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html), so a gross scenario associated with a commune would not automatically be revenue retained by its municipality.

A third post will examine the **Urban Construction Continuum (CCU)**: where the physical city grows, and whether that growth follows a pattern compatible with the discrepancies. Expansion must be distinguished from densification, and the CCU's dependence on census inputs must be checked. An extension can increase the assessment of an existing property without creating another cadastral record. Without administrative event dates, we cannot measure delay; without an enforceable obligation, we cannot measure lost tax resources.

[Explore the diagnostic in the existing viewer (Spanish)](/catastro_sii_brecha/#brecha-contribuciones) · [Download CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv) · [Method, sources and erratum (Spanish)](/catastro_sii_brecha/data/fiscal-gap/method.md).
