---
layout: single
classes: [avaluos-ii-editorial]
title: "Property assessments II: where the residential gap warrants a tax review"
subtitle: "Informal settlements, construction materials and assessed values: from differences by commune to a property-level review"
date: 2026-09-11 00:00:00 -0300
categories: [datos, territorio]
tags: [catastro-sii, census-2024, property-tax, open-data, inequality]
author: clabra
lang: en
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: false
editorial_status: pending-tax-reconciliation
description: "Informal settlements, construction materials and residential assessments to identify where a Census–SII discrepancy warrants a tax review, with explicit assumptions and limitations."
excerpt: "A persistent discrepancy alongside high assessed values in registered properties warrants a cadastral review. Establishing omissions and their tax implications requires identifying the properties."
header:
  overlay_image: /assets/images/avaluos-ii/hero-catastro-residencial-v1-1942x809.webp
  overlay_filter: "linear-gradient(90deg, rgba(16,18,29,0.88), rgba(16,18,29,0.38))"
  show_overlay_excerpt: false
  caption: "AI-generated conceptual illustration; not an actual cadastral map."
  teaser: /assets/images/avaluos-ii/teaser-catastro-residencial-v1-1672x941.webp
  og_image: /assets/images/avaluos-ii/teaser-catastro-residencial-v1-1672x941.png
  og_image_alt: "Conceptual illustration of homes beneath a layer of incomplete property records."
math: true
toc: true
toc_sticky: true
comments: true
---

In the [first property-assessment post](/en/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/), changing the denominator changed the map. Now I am interested in a question that comes before calculating tax: **if the Census counts more dwellings than the SII's residential cadastral records, where should a review begin?**

The tax implications deserve closer attention when the discrepancy persists in communes whose registered properties have high assessed values. If a review found omitted properties comparable to them, the next step would be to establish whether registering them or updating their assessments creates a tax liability.

I examine that difference alongside informal settlements, construction materials and assessed values to guide the search. There are three steps: understand what we are subtracting, distinguish where a review might have tax implications, and specify the evidence needed to establish them.

**How to read the bars.** They guide a review; they do not count omitted properties or outstanding property-tax liabilities.
{: .notice--info}

## First spoonful: measure the difference without treating it as an omission

I compare **all private dwellings in the 2024 Census**, occupied and vacant, with **residential cadastral records—property-use code H—for the first half of 2026**. The first count concerns dwellings; the second concerns properties registered for tax purposes. SII is Chile's tax authority, and a commune is a local administrative area.

There is no one-to-one correspondence. A property may contain several dwellings, and a dwelling may be on an agricultural property excluded by the residential filter. The dates also differ. Dwellings minus records is therefore a **difference between counts**, not a count of “dwellings without a cadastral record.”

The bar is constructed in three steps:

| Step | Calculation | What it represents |
|---|---|---|
| Initial difference | Census dwellings minus residential cadastral records | The gap between the two counts |
| Informal-settlement scenario | Subtract the available household count, assuming one unit of the difference per household | The residual under that assumption |
| Construction-materials scenario | Apply the commune's share of dwellings with acceptable type and materials to the residual | A hypothetical composition of the residual |

### Informal settlements: how much the difference changes under an assumption

In Alto Hospicio, the initial difference is **15,368**. Subtracting the **9,136** households that the processing assigns to settlements with available data leaves **6,232** units: a **59.4%** reduction. In Puerto Montt, the same exercise reduces the difference by just **2.2%**.

| Commune | Initial difference | Households with data | Residual | Reduction |
|---|---:|---:|---:|---:|
| Alto Hospicio | 15,368 | 9,136 | 6,232 | 59.4% |
| Antofagasta | 21,755 | 7,537 | 14,218 | 34.6% |
| Viña del Mar | 24,030 | 8,014 | 16,016 | 33.3% |
| Valparaíso | 32,533 | 2,572 | 29,961 | 7.9% |
| Puerto Montt | 29,036 | 632 | 28,404 | 2.2% |

This deduction is a sensitivity test, not an established explanation. Several households may share a dwelling, the land may have a parent property record, and dates may differ. The layer also contains **222 polygons without a count**: missing data do not mean an absence of households. The interpretation of its `HOGARESCEN` field is detailed in the methodological notes.

The deduction does not represent a tax exemption either: it is an analytical assumption. The SII provides for [the assessment of buildings whose legal status has not been regularised][sii-no-regularizadas]; each property's circumstances must be checked.

In aggregate, the sum of positive differences across communes falls from **1,588,449 to 1,516,689**, a **4.52%** reduction. This is not the net national difference: communes with negative balances do not offset those with positive ones. The result shows that the assumption changes some communes substantially and others very little; it does not establish what share of the discrepancy informal settlements explain.

### Construction materials: describe a scenario, not assess property values

The second assumption asks how the residual would be distributed if it had the same composition as the dwellings observed in the commune. I use a criterion requiring **an acceptable dwelling type and acceptable wall, roof and floor materials simultaneously**, following the code in the [INE microdata manual, indicators viv04 and viv05, pp. 103–105][ine-manual].

In the processed data, **5,774,146 of 6,408,172** occupied private dwellings with residents present meet this criterion. The proportion is calculated for each commune, retaining incomplete observations in the denominator but outside the acceptable group.

For example, a residual of 9,000 units and an acceptable share of 80% would yield **7,200 units in that scenario and 1,800 in the remainder**. This has not located 7,200 dwellings: it has applied a known proportion to a difference of unknown composition.

The extrapolation has two limitations. Construction materials are observed in occupied dwellings with residents present, whereas the initial difference also includes vacant dwellings and those whose residents were absent. In addition, any dwellings missing from the cadastre could differ from those observed. **The “remainder” is not equivalent to irrecoverable dwellings either**: it includes both those that do not meet the criterion and incomplete observations.

I do not add another deduction for irrecoverable dwellings, because their overlap with informal settlements is unknown. Nor do I multiply this scenario by the share of records above the exemption threshold: we do not know the joint distribution of the two characteristics.

![Fifteen communes with the largest residual under the informal-settlement assumption. Each bar preserves the initial difference and separates the assumed deduction, the acceptable-type-and-materials scenario and the remainder.](/assets/images/avaluos-ii/gap-top15-en.svg)

{% include avaluos-ii-top-en.html %}

**How to read the chart.** The total length preserves the initial difference; its segments distinguish the assumed settlement deduction and the hypothetical composition of the residual. The fifteen communes are ranked by that residual, not by construction materials or assessed values. The tax-related selection in the second spoonful uses a different filter.

The [viewer lets you explore each commune and consult the complete table](/catastro_sii_brecha/#brecha-contribuciones). The [Valparaíso and Puerto Montt annex](/catastro_sii_brecha/#catastro-anexo) overlays properties, neighbourhood units and informal settlements: it helps reveal spatial relationships, but does not by itself identify omitted dwellings.

## Second spoonful: distinguish a large gap from a review with tax implications

The size of the difference alone does not establish its potential tax significance. For context, I examine the assessed values of **residential properties that are already registered**: their mean, median and the share above the general exemption threshold.

In the first half of 2026, that threshold was **60,030,710 Chilean pesos**, according to the [SII's official example][sii-ejemplo]. I compare each assessed value with the threshold for the same period. Exceeding it is not enough to establish an enforceable property-tax liability: applicable benefits and exemptions must also be checked.

A property's assessed value for tax purposes [is not its sale price][sii-comercial]. It takes account of both the land and the building and their characteristics. Therefore, **acceptable materials do not imply a high assessed value**: a dwelling with good construction materials on less valuable land may fall below the exemption threshold, while a more modest one on expensive land may exceed it. The SII explains the components of this valuation in its [guide to assessed values][sii-avaluo].

A few very high values can raise the mean. The median shows the centre of the distribution, while the share above the threshold indicates how widespread that condition is. These are complementary summaries of the same properties, not independent evidence of omission.

### An explicit filter: a positive residual and a median above the exemption threshold

In the dataset analysed, these **15 communes** meet both conditions. They are ranked by residual, from largest to smallest. **Construction materials are shown as a scenario, but do not determine the selection.**

| Commune | Residual | Acceptable scenario | Median assessed value, million Chilean pesos | Records above the threshold |
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

*The acceptable scenario combines dwelling type and materials, with results rounded to whole units. Assessed values and percentages refer exclusively to registered residential properties.*

Iquique combines a large residual with a median just above the threshold: **60.24 million Chilean pesos**. Its mean of **73.84 million** does not describe every property's circumstances. Lo Barnechea shows a different combination: a smaller residual of **2,300**, but a median of **290.03 million** and **85.6%** of records above the exemption threshold.

The contrast helps frame a question: **if omitted properties were found and were comparable to registered ones, what would registering them or updating their assessments imply?** It does not estimate how many would be found or how much tax they should owe.

Comparability is the hardest condition to establish. What is missing from a register may differ systematically from what entered it: smaller buildings, dwellings on agricultural properties or properties covered by a parent record. Applying the observed assessment profile to them could introduce bias if the absent properties have a different profile. This filter does not measure the proportional discrepancy or the cost of investigating each commune either; it is a starting point, not a demonstrably optimal prioritisation.

## Third spoonful: from a scenario for a commune to verification at property level

Comparing communes helps choose where to look. Establishing an omission with tax implications requires examining individual properties: **identify the building, establish its relationship to one or more cadastral records, and reconstruct the relevant dates**. The review must allow for both an omission and an explanation that rules it out.

| Possible explanation | What would need to be checked | What would weaken that explanation |
|---|---|---|
| Omitted property or building | Location, land and building information, property records and the cadastral file | The property is already correctly registered, including under another record or property-use category |
| Outdated assessed value | Built floor area and characteristics against cadastral details and their dates | The assessment already incorporates those characteristics |
| Differences in units or periods | Dwellings per property, parent records, agricultural uses, co-ownership and comparable dates | The discrepancy persists after reconciling units and periods |
| Source or processing error | Completeness of the extract, territorial identifiers and independent reproduction | The result is reproduced using independent sources and cross-checks |

**Registering a property and updating a building's assessment are different actions.** The SII has a [procedure for adding properties to the cadastre][sii-inclusion]. It also provides for changes to assessed values. An extension can increase the assessed value of an existing property without creating another record: the difference between dwellings and records cannot, by itself, detect every outdated cadastral assessment.

### What is missing before a scenario can be expressed in pesos

Constructing a scenario in pesos for a commune requires a compatible, reconciled measure of net residential property tax, together with explicit assumptions for applying it to the difference between registers. Quantifying liabilities that were actually omitted additionally requires identifying the properties and checking dates, benefits and exemptions.

The obstacle to the monetary scenario is specific: the extract's half-yearly field does not allow all components of net residential property tax to be separated. The official tables reviewed provide figures by commune and distinguish components, but include other non-agricultural property uses. **Dividing that total by residential records would produce an average drawn from incompatible populations.** The [source audit](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) records this unresolved issue.

Determining a tax liability, issuing a tax bill and collecting payment are different stages. The SII determines assessed values and issues property-tax bills; the [General Treasury of the Republic collects payment][tgr-impuestos]. Distribution through the [Municipal Common Fund][sii-fcm] also means that tax associated with a commune cannot be equated with revenue retained entirely by its municipality.

The [guide by Grote and Wen (2024, pp. 16–18)][fmi-guia] helps organise the problem: it distinguishes coverage, valuation and collection, and proposes cross-checking maps, field observations and records. It informs the design of a verification exercise; it does not supply a revenue coefficient that can be transferred to these communes.

## Closing: the difference needs an explanation

Communes where the difference persists and registered properties have high assessed values offer a starting point for cadastral review. If comparable omitted properties are confirmed, their tax implications must then be determined. If existing records, property-use categories or dates resolve the difference, the omission hypothesis becomes less compelling.

In the next instalment, I will explore the **Continuo de Construcciones Urbanas (CCU)** to examine the built footprint. Before attributing a discrepancy to administrative delay, its sources must be verified and the timing of each change reconstructed.

[Explore the analysis](/catastro_sii_brecha/#brecha-contribuciones) · [Download CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv).

<details markdown="1">
<summary>Methodological notes: sources, snapshots and unresolved limitations</summary>

**Provenance and coverage.** The cadastral mirror was downloaded on 24 July 2026 and corresponds to the first half of that year. It is neither a direct SII download nor a September snapshot. Antártica and Trehuaco have no extract and remain missing, rather than being treated as communes with no residential properties.

**Totals still awaiting reconciliation.** The cited [SII control by property-use category][sii-destino] reports 6,056,150 residential properties; the extract contains 6,054,808. The cited [MINVU housing-stock spreadsheets][minvu-parque] for the first half of 2026 report 6,057,949, including 1,342 in Trehuaco. The difference between the SII and the extract is 1,342, but between MINVU and the extract it reaches 3,141. Adding Trehuaco's 1,342 does not reconcile both controls: a difference of 1,799 properties remains against the MINVU total. This discrepancy is not attributed to an unproven cause, and totals are not silently replaced.

**Two informal-settlement snapshots.** The [MINVU report published on 8 July 2026][minvu-campamentos], using information referring to 2024, records 1,373 settlements, 81,993 occupied dwellings and 77,399 households. The CNC 2026 layer used in this processing contains 1,345 polygons and a total of 71,760 in the `HOGARESCEN` field, with 222 polygons missing that value. These are different populations and snapshots. Interpreting the field as census households is a provisional decision supported by its name and the available documentation, rather than by a dictionary specific to the layer. The deduction depends on it.

**Definition of construction materials.** The analysis uses the code in the INE manual, whose classification does not fully match its prose description: for acceptable materials, the latter allows some recoverable wall materials, whereas the code requires acceptable materials in all three components. The scenario combines that criterion with an acceptable dwelling type. Variants using complete materials responses and the broader non-irrecoverable category are retained; these are sensitivity analyses, not confidence intervals. The processing records 4,388 occupied dwellings with incomplete information.

**Processing corrections.** Territorial harmonisation was corrected for Coyhaique, Aysén and Chile Chico. The count of irrecoverable dwellings fell from 73,338 to 72,642—696 fewer—after first applying the official code's non-response exclusion. That correction does not change the dwellings–records difference or the settlement deduction. The historical anonymised 2011–2021 dataset is not used in the current calculation.

**Traceability.** The [method](/catastro_sii_brecha/data/fiscal-gap/method.md), [audit](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) and [data by commune](/catastro_sii_brecha/data/fiscal-gap/communes.json) document the processing. Only aggregates by commune are published.

</details>

## Sources and references

Grote, Martin, and Jean-François Wen. 2024. *How to Design and Implement Property Tax Reforms*. How to Note 2024/006. International Monetary Fund, September. [Full text][fmi-guia].

Instituto Nacional de Estadísticas (INE). 2025. *Manual de uso de microdatos censales: Censo de Población y Vivienda 2024*. Indicators viv04–viv06, pp. 103–106. [Manual][ine-manual].

Ministerio de Vivienda y Urbanismo (MINVU), Centro de Estudios de Ciudad y Territorio. 2026. *Caracterización de campamentos en Censo 2024*. Published on 8 July. See the general results and table 1, pp. 4–5. [Report][minvu-campamentos].

Servicio de Impuestos Internos (SII). “De avalúo fiscal a contribuciones: paso a paso,” example for the first half of 2026; “¿Qué es un avalúo fiscal?”; “¿El avalúo fiscal corresponde a una tasación comercial de la propiedad?”, updated 8 April 2026; “¿Cómo regularizo una propiedad que no tiene rol de avalúo?”, updated 7 April 2026; and “¿Para qué sirve el pago del impuesto territorial?”. [Calculation][sii-ejemplo], [assessed value][sii-avaluo], [distinction from market value][sii-comercial], [registration][sii-inclusion] and [municipal distribution][sii-fcm]. For buildings whose legal status has not been regularised, see the [documentation required for assessment][sii-no-regularizadas].

Tesorería General de la República (TGR). N.d. “Impuestos y tipos de impuestos.” TGR Help Centre. [Source][tgr-impuestos].

*The external sources above were accessed on 11 September 2026. Processing results and corrections should be read alongside the methodological notes.*

[ine-manual]: https://censo2024.ine.gob.cl/wp-content/uploads/2025/12/manual_uso_microdatos_censo2024.pdf
[minvu-campamentos]: https://catalogo.minvu.cl/cgi-bin/koha/opac-retrieve-file.pl?id=7e816aa9c26af8904eab01badfbfc6e6
[minvu-parque]: https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/
[sii-ejemplo]: https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf
[sii-comercial]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_8124.htm
[sii-avaluo]: https://www.sii.cl/destacados/impuesto_territorial/avaluo_fiscal.html
[sii-inclusion]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_1947.htm
[sii-fcm]: https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html
[sii-no-regularizadas]: https://www.sii.cl/servicios_online/1048-doctos_requeridos-2573.html
[sii-destino]: https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html
[tgr-impuestos]: https://ayuda.tgr.gob.cl/ayuda/impuestos/impuestos-y-tipos-de-impuestos
[fmi-guia]: https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf
