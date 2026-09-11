---
layout: single
title: "Property assessments II: where the residential gap warrants a tax review"
subtitle: "Informal settlements, construction materials and assessed values to identify where a closer review is warranted"
date: 2026-09-09 20:00:00 -0400
categories: [datos, territorio]
tags: [catastro-sii, census-2024, property-tax, open-data, inequality]
author: clabra
lang: en
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: false
editorial_status: pending-tax-reconciliation
description: "A reading of Chile's Census–SII gap using informal settlements, construction-material scenarios and residential assessments to guide cadastral review."
excerpt: "A persistent discrepancy alongside high assessed values in registered properties gives reasons to investigate. Identifying each property is still necessary before claiming missing tax charges."
header:
  teaser: /assets/images/avaluos-ii/gap-top15-en.png
math: true
toc: true
toc_sticky: true
comments: true
---

**How to read this analysis.** The bars help identify where to investigate. They combine an observed difference between registers with explicit scenarios; they do not yet count omitted properties or uncollected pesos.
{: .notice--info}

The [first property-assessment post](/en/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/) changed the denominator to examine the territory differently. This follow-up asks a public-administration question: **when census dwellings outnumber residential cadastral records, where should a review begin?**

The discrepancy becomes more relevant when it persists after considering informal settlements and coincides with high assessed values in properties that are already registered. If a review identifies omitted properties comparable to that stock and establishes an enforceable tax obligation, it could uncover charges that should have been issued. The sequence matters: first locate and verify the property; then determine its tax.

This exercise moves from a striking national number toward a reasoned territorial selection. The comparison can guide a review; each tax conclusion requires verification at property level.

## First spoonful: read the bar in three steps

The comparison uses **all private dwellings in Chile's 2024 Census**, occupied and vacant, and **residential cadastral records for the first half of 2026**, identified by destination code **H**. SII is Chile's tax authority; a *rol* identifies a property, and a *commune* is a local administrative area. These are different units: one property may contain several dwellings, while a dwelling may be within an agricultural property excluded by the residential filter. The subtraction therefore cannot be labelled “homes without a cadastral record.”

| Step | Calculation | What it shows |
|---|---|---|
| Initial difference | Census dwellings minus residential records | Where the two counts diverge most |
| Informal settlements | Subtract households with data in the MINVU layer, under a one-to-one assumption | How much the difference changes if those households are assigned to it |
| Construction materials | Apply the commune's share of dwellings with acceptable type and materials to the residual | How large that component would be if the residual resembled the observed housing stock |

**The full length preserves the initial difference.** The components show the assumed settlement deduction, the acceptable-materials scenario and the remainder. Communes are ranked by the residual after the settlement deduction; the materials component does not change that ordering.

![Fifteen communes with the largest residual after the informal-settlement assumption; each bar distinguishes the assumed deduction and a hypothetical materials composition of the remainder.](/assets/images/avaluos-ii/gap-top15-en.svg)

{% include avaluos-ii-top-en.html %}

The [viewer lets you select a commune, explore its bar and consult the complete table](/catastro_sii_brecha/#brecha-contribuciones). Its [Valparaíso and Puerto Montt map annex](/catastro_sii_brecha/#catastro-anexo) overlays residential properties, neighbourhood units and informal settlements to explore spatial relationships; the overlays alone do not identify unregistered dwellings.

### Informal settlements: a test that changes some communes substantially

Consider Alto Hospicio: its initial difference is 15,368, and the MINVU layer contains 9,136 census households in settlements with available counts. Subtraction leaves 6,232. This reduces the difference by 59.4%; **it has not located 9,136 homes without a record or established their tax status**.

| Commune | Initial difference | Settlement households with data | Scenario residual | Reduction |
|---|---:|---:|---:|---:|
| Alto Hospicio | 15,368 | 9,136 | 6,232 | 59.4% |
| Antofagasta | 21,755 | 7,537 | 14,218 | 34.6% |
| Viña del Mar | 24,030 | 8,014 | 16,016 | 33.3% |
| Valparaíso | 32,533 | 2,572 | 29,961 | 7.9% |
| Puerto Montt | 29,036 | 632 | 28,404 | 2.2% |

The national sum of positive differences falls from **1,588,449 to 1,516,689**, a **4.52%** reduction. The uneven effect is the finding: this assumption changes the reading of some communes substantially and leaves much of the difference in others.

[MINVU published a spatial link between its settlement registry and the 2024 Census](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/vivienda-y-deficit/): its 2024 snapshot contains 1,373 settlements, 81,993 occupied dwellings and 77,399 households. The CNC 2026 layer used here is a different snapshot: 1,345 polygons and 71,760 households in its census-count field, with 222 polygons missing that count. The registry changes over time; households and dwellings are also different units. Deductions in communes with missing counts are partial.

The assumption is deliberately simple: assign each counted settlement household to one unit of the difference. It can fail because households share a dwelling, land already has a parent property record, or dates differ. Living in an informal settlement does not establish an automatic tax exemption. The SII accepts evidence for reviewing unregularised buildings, and legislation provides separate property identifiers for sites in certain subdivisions after regularisation. [SII documentation requirements](https://www.sii.cl/servicios_online/1048-doctos_requeridos-2573.html), [Law 20,234, article 16](https://www.bcn.cl/leychile/Navegar/imprimir?idNorma=268116&idParte=0).

### Construction materials: looking beyond precarious housing

The Census distinguishes dwellings with **an acceptable dwelling type and acceptable wall, roof and floor materials simultaneously**. This is more restrictive than simply “not irrecoverable.” It describes construction components; it does not measure luxury, overall condition, floor area, legal status or assessed value. Classification follows the code in the [INE microdata manual, indicators viv04–viv06, pp. 103–106](https://censo2024.ine.gob.cl/wp-content/uploads/2025/12/manual_uso_microdatos_censo2024.pdf).

In the public data, **5,774,146 of 6,408,172 occupied private dwellings with residents meet this criterion**. To explore the residual's composition, we use each commune's proportion over all dwellings in that universe. Missing observations remain outside the acceptable group.

An illustrative example: if 9,000 units remained after the settlement assumption and 80% of the observed stock met the acceptable criterion, the bar would assign **7,200 to the acceptable scenario and 1,800 to the remainder**. This does not mean 7,200 acceptable dwellings without records have been found: it projects a known composition onto a difference whose contents remain unknown.

The extrapolation could overstate the share if actually omitted dwellings are more precarious than the observed stock; it could understate it if newer construction with acceptable materials predominates. The residual also includes occupied and vacant dwellings, while materials are observed in occupied dwellings with residents. The method retains alternatives using complete materials responses and the broader non-irrecoverable category to show dependence on those decisions. **We do not multiply material quality by the share of records above the tax threshold:** they come from different registers and their joint distribution is unknown.

We do not apply an additional deduction for irrecoverable housing, because its overlap with settlements is unknown. The historical 2011–2021 anonymised settlement database also remains outside the current calculation.

## Second spoonful: why the assessments of what we can observe matter

A large gap and a gap with potential tax relevance may occur in different places. To distinguish them, the viewer includes three references for each commune's **observed residential properties**: mean assessed value, median assessed value and the share above the general exemption amount.

The residential exemption amount was **CLP 60,030,710 in the first half of 2026**, matching the extract's period. Each property's assessment is compared with that value; no tax rate is applied to the commune-wide average. Exceeding it identifies a characteristic of the observed assessment, but other benefits or exemptions may affect the bill. [Official SII example for 2026H1](https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf).

These are not sale prices. The [SII explicitly distinguishes assessed values from market values](https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_8124.htm), and its methodology considers land, buildings, location, surface area and other attributes. A dwelling with acceptable materials on inexpensive land may remain below the exemption amount; modest construction on expensive land may exceed it. [How the fiscal assessment is formed](https://www.sii.cl/destacados/impuesto_territorial/avaluo_fiscal.html).

The mean summarises total value per record, but a few expensive properties can raise it. The median identifies the distribution's centre, while the share above the exemption amount shows how widespread that characteristic is. The three measures complement each other.

**The review criterion is conditional:** a persistent difference, a substantial acceptable-materials scenario, and a residential assessment distribution shifted above the exemption amount warrant closer territorial investigation. If omitted properties comparable to the registered stock are found, checking their inclusion and valuation becomes more relevant. This is a research priority, not an estimated probability of omission.

### Fifteen communes with two signals worth examining together

A transparent filter selects communes with **a positive residual and a median residential assessment above CLP 60,030,710**. These fifteen qualify, ordered by residual. This is a reproducible starting point, not a ranking of debt or evasion probability.

| Commune | Residual | Acceptable type-and-materials scenario | Median residential assessment, million CLP | Residential records above exemption amount |
|---|---:|---:|---:|---:|
| Iquique | 18,949 | 16,964 | 60.24 | 50.4% |
| Pucón | 13,707 | 12,205 | 63.71 | 53.4% |
| Puerto Varas | 8,693 | 7,997 | 61.61 | 51.1% |
| Pirque | 4,883 | 4,090 | 91.85 | 62.2% |
| Algarrobo | 3,201 | 2,876 | 79.72 | 71.1% |
| Santo Domingo | 2,765 | 2,516 | 112.00 | 75.9% |
| Lo Barnechea | 2,300 | 2,202 | 290.03 | 85.6% |
| Huechuraba | 2,297 | 2,118 | 69.73 | 52.5% |
| Concón | 2,005 | 1,888 | 91.82 | 73.3% |
| San Miguel | 1,984 | 1,927 | 63.62 | 55.2% |
| Zapallar | 1,948 | 1,723 | 182.98 | 75.0% |
| La Reina | 1,532 | 1,488 | 122.56 | 83.3% |
| Papudo | 1,213 | 1,092 | 69.05 | 58.1% |
| Providencia | 918 | 908 | 100.40 | 82.6% |
| Las Condes | 542 | 538 | 139.18 | 92.0% |

Scenario values are rounded to units, and assessments refer exclusively to registered properties. In Iquique, for example, the mean is CLP 73.84 million and the median CLP 60.24 million, barely above the exemption amount: a high average does not mean most of the stock lies far above the threshold.

Lo Barnechea illustrates another combination: a residual of 2,300, smaller than in the leading communes, alongside a median residential assessment of CLP 290.03 million and 85.6% of records above the exemption amount. Zapallar also combines a smaller residual with a high median. **These contrasts help identify where an omission could have greater tax relevance, if the properties eventually found are comparable to those already registered.** The difference's size and the assessment profile must be read together.

Selection bias is the main objection. What is missing from a register can differ systematically from what entered it: smaller dwellings, agricultural properties, parent records, recent construction or different tenure arrangements. Transferring a registered-stock mean, median or proportion to potentially absent properties requires similarity that has yet to be demonstrated.

### Why there is still no bar in pesos

The extract's semester field does not separate every component needed to obtain net residential property tax. Available official commune tables distinguish components but include other nonagricultural destinations alongside residential properties. Dividing that total by residential records would manufacture a residential average. The [source audit](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) documents this obstacle.

Potential charges, actual charges and payments are distinct stages. In Chile, the SII determines assessments and charges, while [the General Treasury, TGR, collects](https://ayuda.tgr.gob.cl/ayuda/impuestos/impuestos-y-tipos-de-impuestos); distribution through the Common Municipal Fund also prevents equating taxes associated with a commune with revenue entirely retained by its municipality. [SII: property taxes and distribution](https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html).

The literature helps organise this sequence. Grote and Wen distinguish coverage, valuation and collection in property-tax administration; their guide proposes comparing maps, field observations and registers to identify discrepancies. This supports property-level verification, not a coefficient that can be applied to Chile. [IMF guide, 2024, pp. 16–18](https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf).

## Third spoonful: which review would answer the question?

To strengthen the omitted-tax hypothesis, the next stage must link buildings to properties, review their tax status and reconstruct dates. The result may be a new registration, an update to an existing record, or confirmation that the record was already correct.

| Hypothesis | Discriminating evidence | What would weaken or reject it |
|---|---|---|
| Building or property absent from the cadastre | Identifiable location, land and building evidence, record searches and an inclusion file | The property is correctly recorded already, including under another identifier or destination |
| Outdated assessment in an existing record | Current area or attributes compared with cadastral detail and update dates | The assessment already incorporates those attributes, or the difference belongs to another period |
| Different units or dates | Links to parent records, agricultural properties, co-ownership and comparable time cuts | Individual linkage confirms equivalent units and dates and the difference persists |
| Source or crosswalk error | A complete official extract, reconciled territorial identifiers and an independent check | Independent sources reproduce the result under the same definitions |

The SII provides procedures for [including properties](https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_1947.htm) and modifying building assessments. Registration and updating are different responses: an extension can increase an existing property's assessment without creating another identifier.

There is experimental evidence that better taxpayer location can change collections: Dzansi and coauthors study a geospatial tool for delivering property-tax bills in Ghana. Their finding supports investigating the administrative mechanism; it does not supply a recovery rate for these Chilean communes. [NBER Working Paper 29923, 2025 revision](https://www.nber.org/system/files/working_papers/w29923/w29923.pdf).

There is also evidence against an automatic conclusion. In a historical country panel, D'Arcy, Nistotskaya and Olsson find no property-tax effect in their mechanism analysis. Improving a cadastre alone does not guarantee higher property-tax receipts. [Journal of Political Economy, 2024, section IV](https://www.journals.uchicago.edu/doi/full/10.1086/730551).

The inference worth retaining is specific: **where the discrepancy persists and observed properties have high assessments, a verifiable explanation and a review of possible registration or updating are warranted**. If existing records, destinations or dates resolve the difference, the tax hypothesis weakens. If omissions with enforceable obligations are identified, there will then be a basis to quantify missing charges and examine responsibility.

The next post will add the **Urban Construction Continuum (CCU)** to observe expansion and densification. The physical footprint can help locate change; measuring an SII delay also requires construction, notification and administrative-update dates, and checking how much the CCU depends on census inputs.

<details markdown="1">
<summary>Sources, time cuts and corrections that affect the reading</summary>

The cadastral mirror was downloaded on 24 July 2026 and refers to 2026H1; it is neither a direct SII download nor a September snapshot. Antártica and Trehuaco have no extract and remain missing. The national SII destination control reports 6,056,150 residential records; the extract contains 6,054,808. MINVU's 2026H1 spreadsheets report 6,057,949, including 1,342 in Trehuaco: these cuts are not silently combined. [SII by destination](https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html), [MINVU housing stock](https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/).

The review corrected the territorial crosswalk for Coyhaique, Aysén and Chile Chico. It also corrected the irrecoverable-housing indicator: the previous draft reported 73,338; applying the official code's missing-response exclusion first yields **72,642**, or 696 fewer. This correction changes neither the dwellings–records difference nor the settlement deduction. Acceptable materials follow the INE manual's code, which does not fully match its prose description; the decision and its sensitivity are documented.

The CNC layer does not include a dictionary for its `HOGARESCEN` field: interpreting it as census households relies on its name and MINVU documentation and must be reconsidered if an official definition differs. Materials information is incomplete for 4,388 occupied dwellings; the documented variants change their treatment and are not presented as confidence intervals.

The [reproducible method](/catastro_sii_brecha/data/fiscal-gap/method.md), [source audit](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) and [dataset](/catastro_sii_brecha/data/fiscal-gap/communes.json) preserve definitions, missing observations, rules and errata. Only commune aggregates are published.

</details>

## References behind the inference

- Grote, M., & Wen, J.-F. (2024). *How to Design and Implement Property Tax Reforms* (How to Note 2024/006). International Monetary Fund. [Full text](https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf).
- Dzansi, J., Jensen, A., Lagakos, D., & Telli, H. (2022; February 2025 revision). *Technology and Tax Capacity: Evidence from Local Governments in Ghana* (Working Paper 29923). National Bureau of Economic Research. [DOI](https://doi.org/10.3386/w29923).
- D'Arcy, M., Nistotskaya, M., & Olsson, O. (2024). Cadasters and economic growth: A long-run cross-country panel. *Journal of Political Economy, 132*(11), 3785–3826. [DOI](https://doi.org/10.1086/730551).

[Explore the diagnostic (Spanish)](/catastro_sii_brecha/#brecha-contribuciones) · [Download CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv) · [Method, sources and errata (Spanish)](/catastro_sii_brecha/data/fiscal-gap/method.md).
