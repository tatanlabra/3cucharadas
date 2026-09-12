---
layout: single
classes: [avaluos-ii-editorial]
title: "Property assessments in 3 spoonfuls II: where to review the residential gap"
subtitle: "Informal settlements, construction materials and assessed values: from differences by commune to a property-level review"
date: 2026-09-11 00:00:00 -0300
categories: [datos, territorio]
tags: [catastro-sii, census-2024, property-tax, open-data, inequality]
author: clabra
lang: en
ref: avaluos-ii-brecha-residencial
permalink: /datos/territorio/avaluos-ii-brecha-residencial/
published: true
editorial_status: hypothetical-property-tax-scenario
description: "The Census–SII gap, informal settlements and residential assessments: theoretical tax scenarios in Chilean pesos to guide property-level review, with explicit assumptions."
excerpt: "A persistent discrepancy alongside high assessed values in registered properties warrants a cadastral review. Establishing omissions and their tax implications requires identifying the properties."
header:
  overlay_image: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/hero-1600x900.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/og-1200x630.webp
  og_image_alt: Residential city at night and conceptual cadastral polygons to reconcile.
  overlay_image_mobile: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/hero-mobile-800x450.webp
  teaser_mobile: /assets/images/heroes-v2/avaluos-ii-brecha-residencial/teaser-mobile-640x360.webp
math: true
toc: true
toc_sticky: true
comments: true
visual_id: avaluos-ii
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
---

In the [first property-assessment post](/en/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/), changing the denominator changed the map. Now I am interested in a question that comes before calculating tax: **if the Census counts more dwellings than the SII's residential cadastral records, where should a review begin?**

The tax implications deserve closer attention when the discrepancy persists in communes whose registered properties have high assessed values. If a review found omitted properties comparable to them, the next step would be to establish whether registering them or updating their assessments creates a tax liability.

I examine that difference alongside informal settlements, construction materials and assessed values to guide the search. There are three steps: understand what we are subtracting, gauge its possible tax significance through scenarios in pesos, and specify the evidence needed to establish it.

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

<figure style="width:100%">
  <div role="region" aria-label="Fifteen communes with the largest residual under the informal-settlement assumption. Each bar preserves the initial difference and separates the assumed deduction, the acceptable-type-and-materials scenario and the remainder." tabindex="0" style="max-width:100%;overflow-x:auto;border:1px solid currentColor;border-radius:.4rem">
    <img class="avaluos-ii-monetary-light" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/gap-top15-en.svg" alt="Fifteen communes with the largest residual under the informal-settlement assumption. Each bar preserves the initial difference and separates the assumed deduction, the acceptable-type-and-materials scenario and the remainder." loading="lazy">
    <img class="avaluos-ii-monetary-dark" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/gap-top15-en-dark.svg" alt="Fifteen communes with the largest residual under the informal-settlement assumption. Each bar preserves the initial difference and separates the assumed deduction, the acceptable-type-and-materials scenario and the remainder." loading="lazy">
  </div>
  <figcaption>Scenarios for the composition of the difference; these are not identified omitted dwellings. Scroll horizontally or open the SVG to zoom; values appear in the following table. <a href="/assets/images/avaluos-ii/gap-top15-en.svg">SVG</a> · <a href="/assets/images/avaluos-ii/gap-top15-en-dark.svg">SVG dark</a>.</figcaption>
</figure>

{% include avaluos-ii-top-en.html %}

**How to read the chart.** The total length preserves the initial difference; its segments distinguish the assumed settlement deduction and the hypothetical composition of the residual. The fifteen communes are ranked by that residual, not by construction materials or assessed values. The tax-related selection in the second spoonful uses a different filter.

The [viewer lets you explore each commune and consult the complete table](/catastro_sii_brecha/#brecha-contribuciones). The [Valparaíso and Puerto Montt annex](/catastro_sii_brecha/#catastro-anexo) overlays properties, neighbourhood units and informal settlements: it helps reveal spatial relationships, but does not by itself identify omitted dwellings.

### Several dwellings on one site: another explanation worth testing

Two dwellings can share a plot and be covered by one property-tax record. The Census would then count two dwellings without a property necessarily being absent from the tax register. This mechanism may contribute to the difference; measuring its contribution requires linking **dwellings, sites and property records**. The public dictionary examined and the [Census microdata manual, pp. 17–20][ine-manual], link dwellings, households and people, but do not provide a shared site or property-record identifier for this reconciliation. Several households within one dwelling are not the same as several dwellings on one site.

CASEN 2024 provides a narrower signal. Categories 3 and 4 of its tenure question identify households reporting **an owned site shared with other dwellings**, either fully paid or being paid for. They do not ask how many dwellings occupy the site. I calculate their share among **all households with valid answers**, including renters and other tenure arrangements, using one household head per household. The principal-household question is conditional; applying it as a filter to the entire dataset would incorrectly remove households in single-household dwellings. See the [official questionnaire, pp. 79 and 83][casen-cuestionario].

The national result is **1.09% of households**, with an approximate 95% interval of **0.97% to 1.21%**. It comes from 78,654 sampled households, with no missing answers to this question. National and regional estimates use `expr` and Taylor linearization with strata and clusters; the interval expresses sampling uncertainty, rather than every possible measurement error. The [official CASEN data-use note][casen-nota] distinguishes these domains from descriptive use at commune level.

<figure style="width:100%">
  <div role="region" aria-label="Share of households reporting an owned shared site: Chile and 16 regions with approximate intervals; Valparaíso and Viña del Mar as exploratory cases without confidence intervals." tabindex="0" style="max-width:100%;overflow-x:auto;border:1px solid currentColor;border-radius:.4rem">
    <img class="avaluos-ii-monetary-light" width="1152" height="1286" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/casen-shared-site-en.svg" alt="Share of households reporting an owned shared site: Chile and 16 regions with approximate intervals; Valparaíso and Viña del Mar as exploratory cases without confidence intervals." loading="lazy">
    <img class="avaluos-ii-monetary-dark" width="1152" height="1286" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/casen-shared-site-en-dark.svg" alt="Share of households reporting an owned shared site: Chile and 16 regions with approximate intervals; Valparaíso and Viña del Mar as exploratory cases without confidence intervals." loading="lazy">
  </div>
  <figcaption>CASEN 2024. Percentages describe households, not dwellings per site. The two commune cases are not representative. Scroll horizontally or open the SVG to zoom; values appear in the following table. <a href="/assets/images/avaluos-ii/casen-shared-site-en.svg">SVG</a> · <a href="/assets/images/avaluos-ii/casen-shared-site-en-dark.svg">SVG dark</a>.</figcaption>
</figure>

{% include casen-shared-site-table.html lang='en' %}

Valparaíso and Viña del Mar show **9.27% and 8.60%**, respectively, in the commune calculation weighted by `expc`. These are exploratory signals: I selected the two communes after observing their discrepancy, and these results **are not representative estimates for each commune**. A commune weight does not confer that property. The table retains sample sizes and missingness; the eleven communes outside the sample are recorded as missing data, never zero.

The deduction is limited but useful: dwelling and property-record counts may differ even with an accurate register. The observed pattern in these two communes makes shared sites worth investigating. The hypothesis is that they explain part of the discrepancy, alongside informal settlements, agricultural land uses, timing and possible omissions. A representative sample linking dwellings to sites and property records would discriminate between these explanations; the hypothesis would weaken as a material explanation if this linkage showed a small contribution against a criterion set before measurement.

**I do not subtract this percentage from the bars or monetary scenarios.** It describes household tenure, not the share of excess dwellings in a count. It also misses other ways of sharing sites and may overlap with informal settlements. Subtracting it now would introduce apparent precision and could count the same explanation twice.
{: .notice--info}

<details markdown="1">
<summary>Why the CASEN percentage cannot directly become dwellings per site</summary>

In a purely hypothetical example, if a share $$p_v$$ of **dwellings** belonged to sites with exactly two dwellings and all remaining dwellings occupied individual sites, there would be $$V(1-p_v/2)$$ sites. The property-records/sites ratio would be $$R_2=R_1/(1-p_v/2)$$, where $$R_1=\text{property records}/V$$. For example, an assumed $$p_v=0.20$$ would mean 90 sites for every 100 dwellings. The CASEN **household** share is not that parameter: the formula illustrates the mechanism but does not estimate a fiscal adjustment.

</details>

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

The contrast helps frame a question: **if omitted properties were found and were comparable to registered ones, what order of magnitude would the associated tax have?** I construct two scenarios to address that question; neither estimates how many properties would be found.

Comparability is the hardest condition to establish. What is missing from a register may differ systematically from what entered it: smaller buildings, dwellings on agricultural properties or properties covered by a parent record. Applying the observed assessment profile to them could introduce bias if the absent properties have a different profile. This filter does not measure the proportional discrepancy or the cost of investigating each commune either; it is a starting point, not a demonstrably optimal prioritisation.

### Giving the problem a scale: two theoretical tax scenarios

First, I calculate, **property by property**, the general tax that would result from applying the first-half 2026 brackets to each assessed value. I then calculate the mean and median of those results within each commune, **including zeros below the exemption threshold**. Applying a rate to the mean assessed value would not necessarily give the same result: exemptions and brackets change the calculation.

The model uses the parameters in the [SII's official example][sii-ejemplo]: an exemption threshold of **CLP 60,030,710**, a bracket change at **CLP 214,395,361**, and annual rates of **0.893% and 1.042%**, respectively. It is a **theoretical annual-equivalent general property tax**, holding that half-year's parameters fixed. It excludes refuse charges, surtaxes and individual benefits; it does not reproduce actual tax bills or collections for the whole of 2026.

I then multiply the residual under the informal-settlement assumption by each statistic:

| Scenario | Calculation | Interpretation |
|---|---|---|
| Using the median | Residual × median theoretical tax per property | Applies the central value of the modelled tax to each unit |
| Using the mean | Residual × mean theoretical tax per property | Applies the average, which is sensitive to high assessments |

**These are two references for scale, not a confidence interval or guaranteed lower and upper bounds.** The median is not a minimum tax: if more than half the properties fall below the exemption threshold, it can be zero while the mean is positive. The same fifteen communes selected above are retained here and ranked by the scenario using the mean.

<figure style="width:100%">
  <div role="region" aria-label="Theoretical annual-equivalent general property-tax scenarios for the fifteen communes with a positive residual and a median assessment above the exemption threshold; comparison of mean and median." tabindex="0" style="max-width:100%;overflow-x:auto;border:1px solid currentColor;border-radius:.4rem">
    <img class="avaluos-ii-monetary-light" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/monetary-top15-en.svg" alt="Theoretical annual-equivalent general property-tax scenarios for the fifteen communes with a positive residual and a median assessment above the exemption threshold; comparison of mean and median." loading="lazy">
    <img class="avaluos-ii-monetary-dark" width="1152" height="1027" style="width:100%;min-width:1000px;max-width:none;height:auto" src="/assets/images/avaluos-ii/monetary-top15-en-dark.svg" alt="Theoretical annual-equivalent general property-tax scenarios for the fifteen communes with a positive residual and a median assessment above the exemption threshold; comparison of mean and median." loading="lazy">
  </div>
  <figcaption>Million Chilean pesos, assuming that each residual unit corresponded to a new comparable property. Amounts are hypothetical; they are neither established tax debt nor revenue retained by municipalities. Scroll horizontally or open the SVG to zoom; values appear in the following table. <a href="/assets/images/avaluos-ii/monetary-top15-en.svg">SVG</a> · <a href="/assets/images/avaluos-ii/monetary-top15-en-dark.svg">SVG dark</a>.</figcaption>
</figure>

{% include avaluos-ii-monetary-en.html %}

Iquique illustrates why both references are useful. With **18,949** residual units, the scenario using the median reaches **CLP 36 million** in annual-equivalent tax; using the mean, it reaches **CLP 4,309 million**. The difference is large: the median assessment barely exceeds the exemption threshold and yields theoretical tax of about **CLP 1,912 per property**, while the mean includes the contribution of higher assessments. Showing only one statistic would hide that difference in the profile.

In Lo Barnechea, **2,300** residual units produce **CLP 4,983 million using the median and CLP 6,669 million using the mean**. Under this model, it leads the monetary ranking despite having a much smaller physical gap than Iquique. This has not discovered missing revenue: it shows the scale of tax if new comparable properties were confirmed. The contrast makes the case for reviewing communes where an unresolved discrepancy coincides with high assessed values more concrete.

The full comparison assumes **one new comparable property for every residual unit**: I call this assumption $$q=1$$. The viewer allows it to be reduced to $$q=0.5$$ or $$q=0.25$$, halving or quartering the amounts. This factor represents the hypothetical share of the residual that would result in new comparable properties; **it is not an estimated probability, a collection rate or the share of properties paying tax**. Tax zeros are already included in both statistics. No additional construction-materials deduction is applied.

## Third spoonful: from a scenario for a commune to verification at property level

Comparing communes helps choose where to look. Establishing an omission with tax implications requires examining individual properties: **identify the building, establish its relationship to one or more cadastral records, and reconstruct the relevant dates**. The review must allow for both an omission and an explanation that rules it out.

| Possible explanation | What would need to be checked | What would weaken that explanation |
|---|---|---|
| Omitted property or building | Location, land and building information, property records and the cadastral file | The property is already correctly registered, including under another record or property-use category |
| Outdated assessed value | Built floor area and characteristics against cadastral details and their dates | The assessment already incorporates those characteristics |
| Differences in units or periods | Dwellings per property, parent records, agricultural uses, co-ownership and comparable dates | The discrepancy persists after reconciling units and periods |
| Source or processing error | Completeness of the extract, territorial identifiers and independent reproduction | The result is reproduced using independent sources and cross-checks |

**Registering a property and updating a building's assessment are different actions.** The SII has a [procedure for adding properties to the cadastre][sii-inclusion]. It also provides for changes to assessed values. An extension can increase the assessed value of an existing property without creating another record: the difference between dwellings and records cannot, by itself, detect every outdated cadastral assessment.

### What is missing before a scenario becomes an established liability

The scenarios above give the assumption a scale, but quantifying liabilities that were actually omitted requires identifying the properties, checking their dates and assessed values, and applying the relevant benefits and exemptions. Compatible, reconciled tax-billing data are also needed to compare theoretical tax with actual bills.

The [SII cadastral dictionary][sii-estructura] defines the available half-yearly field as a contribution **including refuse charges**. It is not used as net tax. The official commune-level tables reviewed distinguish components but include other non-agricultural uses: **dividing that total by residential records would produce an average drawn from incompatible populations**. The [source audit](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) retains this limitation; the rule-based calculation neither reconciles nor removes it.

Determining a tax liability, issuing a tax bill and collecting payment are different stages. The SII determines assessed values and issues property-tax bills; the [General Treasury of the Republic collects payment][tgr-impuestos]. Distribution through the [Municipal Common Fund][sii-fcm] also means that tax associated with a commune cannot be equated with revenue retained entirely by its municipality.

The [guide by Grote and Wen (2024, pp. 16–18)][fmi-guia] helps organise the problem: it distinguishes coverage, valuation and collection, and proposes cross-checking maps, field observations and records. It informs the design of a verification exercise; it does not supply a revenue coefficient that can be transferred to these communes.

<aside class="notice--info" markdown="1">
**Behind the analysis: Python and reproducible geomatics**

Python connects cadastral, census and territorial aggregates; Parquet stores columnar tables, and Matplotlib produces these figures in SVG and PNG with typography and palettes for both reading modes. Each chart comes from a verifiable table: the image helps readers see the pattern, while the table exposes the values. The viewer retains ECharts for interactive exploration and map layers for examining territory.

For CASEN, R opens the original dataset and passes the required columns to Python through an in-memory pipe. Python computes estimates and design variance; algebraic fixtures and a bounded comparison with Julia check the implementation. Separating extraction, computation, presentation and checks makes similar work easier to carry into larger computing workflows. **This execution is local: it is neither a benchmark nor a demonstrated HPC-cluster run.** The [method and provenance](/catastro_sii_brecha/data/casen-shared-site/method.md) document what was actually done.
</aside>

## Closing: the difference needs an explanation

Communes where the difference persists and registered properties have high assessed values offer a starting point for cadastral review. The scenarios in pesos show why a smaller gap may deserve tax-related attention. If comparable omitted properties are confirmed, their tax implications must be determined; if existing records, property-use categories or dates resolve the difference, the omission hypothesis becomes less compelling. The result warrants investigation but does not establish negligence or a failure to collect tax by any agency.

In the next instalment, I will explore the **Continuo de Construcciones Urbanas (CCU)** to examine the built footprint. Before attributing a discrepancy to administrative delay, its sources must be verified and the timing of each change reconstructed.

[Explore the analysis](/catastro_sii_brecha/#brecha-contribuciones) · [Download CSV](/catastro_sii_brecha/data/fiscal-gap/communes.csv).

<details markdown="1">
<summary>Methodological notes: sources, snapshots and unresolved limitations</summary>

**Provenance and coverage.** The cadastral mirror was downloaded on 24 July 2026 and corresponds to the first half of that year. It is neither a direct SII download nor a September snapshot. Antártica and Trehuaco have no extract and remain missing, rather than being treated as communes with no residential properties.

**Totals still awaiting reconciliation.** The cited [SII control by property-use category][sii-destino] reports 6,056,150 residential properties; the extract contains 6,054,808. The cited [MINVU housing-stock spreadsheets][minvu-parque] for the first half of 2026 report 6,057,949, including 1,342 in Trehuaco. The difference between the SII and the extract is 1,342, but between MINVU and the extract it reaches 3,141. Adding Trehuaco's 1,342 does not reconcile both controls: a difference of 1,799 properties remains against the MINVU total. This discrepancy is not attributed to an unproven cause, and totals are not silently replaced.

**Two informal-settlement snapshots.** The [MINVU report published on 8 July 2026][minvu-campamentos], using information referring to 2024, records 1,373 settlements, 81,993 occupied dwellings and 77,399 households. The CNC 2026 layer used in this processing contains 1,345 polygons and a total of 71,760 in the `HOGARESCEN` field, with 222 polygons missing that value. These are different populations and snapshots. Interpreting the field as census households is a provisional decision supported by its name and the available documentation, rather than by a dictionary specific to the layer. The deduction depends on it.

**Definition of construction materials.** The analysis uses the code in the INE manual, whose classification does not fully match its prose description: for acceptable materials, the latter allows some recoverable wall materials, whereas the code requires acceptable materials in all three components. The scenario combines that criterion with an acceptable dwelling type. Variants using complete materials responses and the broader non-irrecoverable category are retained; these are sensitivity analyses, not confidence intervals. The processing records 4,388 occupied dwellings with incomplete information.

**Monetary formula and unit.** For an assessed value $$A$$, exemption threshold $$E=60\,030\,710$$ and bracket change $$T=214\,395\,361$$, the calculation is:

$$
\begin{aligned}
g(A)={}&0.00893\max(\min(A,T)-E,0)\\
       &+0.01042\max(A-T,0).
\end{aligned}
$$

Results are aggregated by commune, including zeros, before multiplying each statistic by the positive residual and by $$q$$. Tax is not applied to the mean assessment, properties with zero theoretical tax are not filtered out, and a rate that is already annual is not annualised again. The individual exempt assessment in the extract does not replace the general exemption threshold in this model. The calculation therefore does not represent individual benefits or seek to reconstruct each property's tax bill. The mean and median describe registered properties; extrapolating them to the residual requires the comparability assumption.

**Processing corrections.** Territorial harmonisation was corrected for Coyhaique, Aysén and Chile Chico. The count of irrecoverable dwellings fell from 73,338 to 72,642—696 fewer—after first applying the official code's non-response exclusion. That correction does not change the dwellings–records difference or the settlement deduction. The historical anonymised 2011–2021 dataset is not used in the current calculation.

**Traceability.** The [method](/catastro_sii_brecha/data/fiscal-gap/method.md), [audit](/catastro_sii_brecha/data/fiscal-gap/source-audit.json) and [data by commune](/catastro_sii_brecha/data/fiscal-gap/communes.json) document the processing. Only aggregates by commune are published.

</details>

## Sources and references

Ministerio de Desarrollo Social y Familia. 2026. *CASEN 2024: questionnaire and data-use note*. Tenure and principal household, pp. 79 and 83 of the [questionnaire][casen-cuestionario]; expansion factors and domains in the [data-use note][casen-nota]. Accessed September 12, 2026.

Grote, Martin, and Jean-François Wen. 2024. *How to Design and Implement Property Tax Reforms*. How to Note 2024/006. International Monetary Fund, September. [Full text][fmi-guia].

Instituto Nacional de Estadísticas (INE). 2025. *Manual de uso de microdatos censales: Censo de Población y Vivienda 2024*. Indicators viv04–viv06, pp. 103–106. [Manual][ine-manual].

Ministerio de Vivienda y Urbanismo (MINVU), Centro de Estudios de Ciudad y Territorio. 2026. *Caracterización de campamentos en Censo 2024*. Published on 8 July. See the general results and table 1, pp. 4–5. [Report][minvu-campamentos].

Servicio de Impuestos Internos (SII). “De avalúo fiscal a contribuciones: paso a paso,” example for the first half of 2026; “¿Qué es un avalúo fiscal?”; “¿El avalúo fiscal corresponde a una tasación comercial de la propiedad?”, updated 8 April 2026; “¿Cómo regularizo una propiedad que no tiene rol de avalúo?”, updated 7 April 2026; and “¿Para qué sirve el pago del impuesto territorial?”. [Calculation][sii-ejemplo], [assessed value][sii-avaluo], [distinction from market value][sii-comercial], [registration][sii-inclusion] and [municipal distribution][sii-fcm]. For buildings whose legal status has not been regularised, see the [documentation required for assessment][sii-no-regularizadas].

Servicio de Impuestos Internos (SII). N.d. *Estructura de archivo para Detalle Catastral de Bienes Raíces*. Basic information for non-agricultural properties, fields 5–8 and the property-use table, p. 1. [Dictionary][sii-estructura].

Tesorería General de la República (TGR). N.d. “Impuestos y tipos de impuestos.” TGR Help Centre. [Source][tgr-impuestos].

*The external sources above were accessed on 11 September 2026. Processing results and corrections should be read alongside the methodological notes.*

[ine-manual]: https://censo2024.ine.gob.cl/wp-content/uploads/2025/12/manual_uso_microdatos_censo2024.pdf
[minvu-campamentos]: https://catalogo.minvu.cl/cgi-bin/koha/opac-retrieve-file.pl?id=7e816aa9c26af8904eab01badfbfc6e6
[minvu-parque]: https://centrodeestudios.minvu.gob.cl/repositorio/categoria/parque-habitacional/
[sii-ejemplo]: https://www.sii.cl/destacados/impuesto_territorial/Ej_Casa.pdf
[sii-estructura]: https://www.sii.cl/bbrr/descargas/estructura_detalle_catastral.pdf
[sii-comercial]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_8124.htm
[sii-avaluo]: https://www.sii.cl/destacados/impuesto_territorial/avaluo_fiscal.html
[sii-inclusion]: https://www.sii.cl/preguntas_frecuentes/aval_contrib_bbrr/001_165_1947.htm
[sii-fcm]: https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html
[sii-no-regularizadas]: https://www.sii.cl/servicios_online/1048-doctos_requeridos-2573.html
[sii-destino]: https://www.sii.cl/sobre_el_sii/estadisticas/ebbrrn_bbrr_por_destino.html
[tgr-impuestos]: https://ayuda.tgr.gob.cl/ayuda/impuestos/impuestos-y-tipos-de-impuestos
[fmi-guia]: https://www.imf.org/-/media/files/publications/howtonotes/2024/english/htnea2024006.pdf

[casen-cuestionario]: https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf
[casen-nota]: https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf
