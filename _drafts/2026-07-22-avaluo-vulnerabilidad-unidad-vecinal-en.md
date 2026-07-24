---
layout: single
title: "One cadastre, four stories: why the denominator changes the map"
subtitle: "From fiscal appraisal to territorial vulnerability: a guide to reading 9.4 million parcels without confusing value, households, and area"
date: 2026-07-22 10:00:00 -0400
categories: [data, python, territory]
tags: [sii-cadastre, igvust, neighbourhood-unit, inequality, gini, theil, duckdb, geospatial, open-data]
description: "A plain-language introduction to crossing SII fiscal appraisal and IGVUST by neighbourhood unit. The stable finding is not a paradox between value and vulnerability, but how the reading changes with the denominator, scale, and universe."
excerpt: "A cadastre records parcels, not people. Before comparing it with territorial vulnerability, one must decide what is added, what divides it, and which territory remains outside."
author: clabra
lang: en
ref: avaluo-vulnerabilidad-uv
permalink: /datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/
header:
  teaser: /assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-teaser-640-en.webp
  og_image: /assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-social-1200x630-en.webp
math: true
distribution:
  social: true
  republish: []
toc: true
toc_sticky: true
comments: true
author_profile: true
---

A data map looks like an answer, but several decisions come before the colours: **what is counted, what divides it, over which territory it is aggregated, and which cases remain outside**. Change any of those decisions and the map may also change even when the source data stay exactly the same.
{: .text-justify}

The idea fits in one fraction:
{: .text-justify}

$$
\text{territorial indicator}
=
\frac{\text{total to be described}}
{\text{unit used for comparison}}
$$

The total fiscal appraisal in a territory answers how much administrative value was accumulated there. Dividing that same total by households, people, or square metres answers different questions. None is automatically “the right one”; the error begins when they are treated as interchangeable.
{: .text-justify}

## Before the results: a minimal mental map

This post crosses two Chilean administrative records. The first is the Internal Revenue Service's (SII) real-estate cadastre. The second is the Ministry of Social Development and Family's Global Territorial Vulnerability Index (IGVUST). Readers need no prior knowledge of either, but seven concepts must remain separate.
{: .text-justify}

| Concept | What it means here | What it does not mean |
|---|---|---|
| **Cadastre** | Administrative register of real estate and its characteristics. | Population census or register of resident owners. |
| **Parcel** | Cadastral unit identified by municipality, block, and parcel number. | Dwelling, household, or person. |
| **Fiscal appraisal** | Administrative valuation used as the territorial-tax base. | Sale price, income, or household wealth. |
| **IGVUST** | Ranking of neighbourhood units by territorial vulnerability. | Individual diagnosis or causal explanation of vulnerability. |
| **Social Registry of Households (RSH)** | Source of the household and person counts used as denominators. | Population census or income measurement in this analysis. |
| **Neighbourhood unit** | Territory defined for neighbourhood organisation and participation. | Exhaustive mesh required to cover every square metre of Chile. |
| **Universe and denominator** | Cases included and the quantity dividing the total. | Fine print added after the result: they are part of the question. |

Fiscal appraisal is not market price. But neither is it arbitrary: Chile's SII builds it from area, construction material, destination, and **homogeneous area**, a zone of similar unit values. It can therefore serve as a territorial signal, provided it keeps its surname: **fiscal**.
{: .text-justify}

This connects with [Rosen's (1974)](https://doi.org/10.1086/260169) hedonic-price theory: the value of a differentiated good incorporates its own attributes and those of its surroundings. There is a decisive difference here. I observe neither transaction prices nor household assets; I observe an administrative valuation for tax purposes. I will not turn one into the other.
{: .text-justify}

## The question: keep the numerator fixed and change the lens

I aggregated parcel fiscal appraisal at neighbourhood-unit scale and compared it with IGVUST's national vulnerability order. The **unit of analysis** is the neighbourhood unit, not the parcel or person. The descriptive question is: how does the pattern between appraisal and vulnerability change when the same total is expressed in four ways?
{: .text-justify}

| Measure | Question it answers |
|---|---|
| Total appraisal | How much fiscal appraisal was allocated to this unit? |
| Appraisal per RSH household | How much allocated appraisal corresponds per registered household? |
| Appraisal per RSH person | How much corresponds per registered person? |
| Appraisal per parcel m² | How much appraisal corresponds per allocated parcel area? |

The short answer is that the pattern depends heavily on that lens. Per household and per person, there is almost no relationship. Per square metre, a strong national relationship appears. Looking only at predominantly urban units, it fades. The finding is not that one map “disproves” another; it is that **denominator, universe, and scale are part of the result**.
{: .text-justify}

This analysis cannot reveal how much residents earn, what a dwelling would sell for, or who lives in a parcel. Confusing an association between territories with characteristics of their residents would be an improper ecological inference ([Robinson, 1950](https://doi.org/10.2307/2087176)).
{: .text-justify}

**Data cut:** 19 July 2026. **Editorial date:** 22 July 2026. Every relationship below is descriptive and conditional on the neighbourhood-unit mesh used.
{: .small}

## Spoonful 1: building a common numerator without forcing the map

The original cut contains **10,343,893 records**, but a record is not the same thing as a unique parcel. Deduplicating the cadastral key —municipality, block, and parcel number— leaves **9,401,277 parcels**. The objective is to allocate their appraisal across 6,891 neighbourhood units before testing any denominator.
{: .text-justify}

Parcels and units are both polygons, but their borders do not match: a parcel can fall fully inside one unit, cross several, or touch none. The rule is intersection-area apportionment, a form of areal interpolation ([Goodchild, Anselin & Deichmann, 1993](https://doi.org/10.1068/a250383)). For parcel $$p$$ and neighbourhood unit $$u$$:
{: .text-justify}

$$
f_{p,u} = \frac{\text{area}(p \cap u)}{\text{area}(p)}
\qquad
A_u = \sum_{p} a_p \cdot f_{p,u}
$$

where $$a_p$$ is the parcel's fiscal appraisal. If it lies fully inside one unit, it contributes all of it; if it crosses a boundary halfway, it contributes half.
{: .text-justify}

Two decisions are part of the result.
{: .text-justify}

**I use geometric area, not declared area.** Among the 9,401,277 unique parcels, 10.7% have no usable declared surface and 2.8% have no geometry. Replacing an available measurement with an assumption merely to retain an intuitive column name would be backwards.
{: .text-justify}

**I do not renormalize.** If $$\sum_u f_{p,u} < 1$$, part of a parcel lies outside every neighbourhood unit. Redistributing that remainder among the units it does touch would produce a perfect sum and a worse datum: it would hide that neighbourhood units were not designed to tessellate Chile.
{: .text-justify}

The remainder is concrete: **271,150 parcels**, **2.884%** of the deduplicated total, do not fall in any unit. The median municipal leakage is 0.644%, but it is not uniform. In Antofagasta, 2,325 parcels outside units account for 32.6% of municipal fiscal appraisal; in Tortel, Timaukel, San Gregorio, Laguna Blanca, and Río Verde leakage reaches 100% because the units cover the settlement while cadastral parcels lie outside it.
{: .text-justify}

Law 19.418 defines the neighbourhood unit as an arena for neighbourhood organisation and participation, not as an exhaustive parcel mesh. Fiscal appraisal in territory with no unit is not an error the method should hide: it lies outside this crosswalk's universe and is reported as such.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.webp' | relative_url }}" title="Figure 1 — From the original records to the spatial universe" aria-label="Open an enlarged version of Figure 1">
    <picture>
      <source srcset="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.svg' | relative_url }}" type="image/svg+xml">
      <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.webp' | relative_url }}" alt="Flow diagram: 10,343,893 original records split into 942,616 duplicates and 9,401,277 unique parcels; among the unique parcels, 9,130,127 touch at least one neighbourhood unit and 271,150 touch none." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 1</strong> — From the original records to the spatial universe. “Touches at least one unit” does not mean complete allocation: a parcel can intersect a unit while retaining part of its area outside the mesh. Source: own analysis, cut 19 July 2026. Click to enlarge.</figcaption>
</figure>

## Spoonful 2: four facts once the denominator is visible

Before reading the tables, it helps to understand **quartiles**. I ordered the units from lowest to highest and split them into four groups containing approximately the same number of units. A quartile indicates relative position, not distance: being in `q4` does not mean having four times the value of `q1`. In IGVUST, `q1` is the **most vulnerable** group; for appraisal, `q1` is the lowest-value group and `q4` the highest.
{: .text-justify}

### 1. One cell attracts attention, but it does not yet tell a social story

I first divided allocated appraisal by the RSH households in each unit and ordered both variables into national quartiles. IGVUST quartile 1 is the **most** vulnerable. Within that row, the combination with the highest appraisal per household (`qa4`) contains 530 units: more than the 399 in the lowest-appraisal-per-household quartile.
{: .text-justify}

{: .table-caption}
**Table 1** — Neighbourhood units by national quartile of vulnerability and appraisal per household

| IGVUST quartile | Appraisal/household q1 | q2 | q3 | q4 |
|---|---:|---:|---:|---:|
| q1 · most vulnerable | 399 | 344 | 446 | **530** |
| q2 | 564 | 451 | 385 | 321 |
| q3 | 467 | 509 | 429 | 316 |
| q4 · least vulnerable | 293 | 419 | 463 | 546 |

This picture could be sold as a contradiction: highly vulnerable units where the cadastre records high appraisal per household. The right word is **clue**, not conclusion. The quartile combines a territorial numerator with a household count; that division must be opened before assigning it social meaning.
{: .text-justify}

### 2. The striking quadrant has fewer households and much more land

The vulnerable units in the highest appraisal-per-household quartile have a median of 120.5 households and 78.2 km². Those in the lowest appraisal-per-household quartile have 265 households and 3.36 km². The ratio rises because the denominator shrinks and the territory becomes huge; this table does not show that its residents are wealthier.
{: .text-justify}

{: .table-caption}
**Table 2** — Mechanism in the most vulnerable quartile (`q1` IGVUST)

| Appraisal/household | Units | Median households | Median area (km²) | Median appraisal/household (million CLP) |
|---|---:|---:|---:|---:|
| q1 | 399 | 265.0 | 3.36 | 10.2 |
| q2 | 344 | 368.5 | 15.21 | 26.2 |
| q3 | 446 | 274.5 | 45.59 | 57.6 |
| q4 | 530 | 120.5 | 78.22 | 185.6 |

The table does not invalidate the crosswalk. It establishes what it measures: fiscal appraisal allocated to a neighbourhood unit divided by RSH households, not the well-being of its residents.
{: .text-justify}

### 3. The sign changes with the statistical question

The next table uses two summaries that range from −1 to +1. **Pearson** looks for a linear relationship —here using the logarithm of positive appraisal— while **Spearman** asks whether the ordering of units changes monotonically, using ranks. Values near zero indicate little linear or monotonic relationship, respectively. A negative sign means that, in that universe and with that ratio, greater vulnerability is descriptively associated with lower appraisal. Neither column estimates a causal effect or includes an uncertainty interval.
{: .text-justify}

{: .table-caption}
**Table 3** — Sensitivity of the association to the denominator

| Appraisal measure | Pearson | Spearman | Units |
|---|---:|---:|---:|
| Allocated total | −0.371 | −0.382 | 6,857 |
| Per RSH household | −0.061 | −0.047 | 6,849 |
| Per RSH person | −0.079 | −0.072 | 6,849 |
| Per allocated parcel m² | −0.582 | −0.575 | 6,851 |
| Per m², only `p_urbano > 50` | +0.079 | +0.081 | 3,221 |

Per household and per person, the association is almost null under both estimators. Per square metre, the national pattern seems strong. But when restricted to predominantly urban units it changes to approximately +0.08. The cautious reading is that the national per-m² result largely contains the urban-rural contrast; it does not identify a neighbourhood mechanism.
{: .text-justify}

The violins in Figure 2 reveal something a correlation compresses too far: the full distribution. Their width shows where more units are concentrated; internal lines show the median and interquartile range. These are smoothed densities, not literal silhouettes of territory.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores-en.webp' | relative_url }}" title="Figure 2 — Sensitivity to the denominator and universe" aria-label="Open an enlarged version of Figure 2">
    <picture>
      <source srcset="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores-en.svg' | relative_url }}" type="image/svg+xml">
      <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores-en.webp' | relative_url }}" alt="Three violin plots compare distributions of appraisal per household, appraisal per square metre nationally, and appraisal per square metre in predominantly urban neighbourhood units, across the four national vulnerability quartiles." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 2</strong> — The same appraisal produces different distributions when the denominator and universe change. Violins show estimated densities; their shape depends on bandwidth and proves neither natural groups nor causality. Internal lines summarize the median and interquartile range. Source: own analysis, cut 19 July 2026. Click to enlarge.</figcaption>
</figure>

### 4. The robust result is sensitivity, not the winning colour

The same numerator —apportioned fiscal appraisal— yields four different stories when the comparison unit changes. That is not a software bug or a curiosity solved by choosing the prettiest map. It is the central methodological result: before saying “value” against “vulnerability,” one must declare whether the measure is total, households, people, or area, and which universe was left outside.
{: .text-justify}

Reclassification makes this tangible. Among the **6,843 units** with quartiles available both per household and per m², only **1,362 (19.9%)** remain in the same quartile, while **3,132 (45.8%)** move by two or more. The parcels did not change; the question used to summarise them did.
{: .text-justify}

## Spoonful 3: what changes when the scale changes

Among the **6,857 neighbourhood units with positive allocated appraisal**, the Gini coefficient is **0.7265**. Gini equals 0 when every unit receives exactly the same amount and approaches 1 as concentration increases. Here it describes a highly concentrated territorial tax base; it is not a Gini of individual income or wealth.
{: .text-justify}

Gini summarises concentration but does not cleanly separate how much occurs within and between groups. The **Theil index** does. With $$x_i$$ as the appraisal allocated to unit $$i$$, $$\mu$$ as its mean, and $$w_g$$ as group $$g$$'s share of total appraisal:
{: .text-justify}

$$
T = \frac{1}{n}\sum_{i=1}^{n} \frac{x_i}{\mu} \ln\!\left(\frac{x_i}{\mu}\right)
= \underbrace{\sum_{g} w_g T_g}_{\text{within}} + \underbrace{\sum_{g} w_g \ln\!\left(\frac{\mu_g}{\mu}\right)}_{\text{between}}
$$

Grouped by region, $$T = 1.2042$$ and 81.0% remains within regions. Regrouped by municipality, the between-group share reaches 56.9%. It would be easy to conclude that the municipal scale “reveals” segregation. It does not on its own: municipalities are nested within regions, and refining a partition shifts inequality from within to between by construction ([Shorrocks, 1984](https://doi.org/10.2307/1913511)).
{: .text-justify}

It still teaches something useful: the **modifiable areal unit problem**, or MAUP ([Fotheringham & Wong, 1991](https://doi.org/10.1068/a231025)). Put simply, the same points or polygons can produce different statistics when grouped into regions, municipalities, or neighbourhood units. Scale is not a presentation detail; it changes both the question and the accounting of inequality.
{: .text-justify}

Second brake: IGVUST quartiles rank units, not people. The most-vulnerable quartile contains 25% of units but **2,032,893 of 15,978,644 RSH people (12.7%)**. A choropleth can overrepresent dispersed rural territory even if every colour is calculated correctly.
{: .text-justify}

Third brake: assessment-ratio research shows that fiscal valuation can systematically depart from market values and that the pattern depends on institutional context. [Hodge, McMillen, Sands and Skidmore (2017)](https://doi.org/10.1111/1540-6229.12126) study that problem in another market; they do not prove that Chile's SII has the same bias. What they do rule out is treating fiscal appraisal as market price or claiming from this crosswalk how much it understates real inequality.
{: .text-justify}

## The potato: how to read any map like this

The general conclusion does not depend on memorising one correlation. It depends on keeping three questions beside every territorial figure.
{: .text-justify}

**One: what was left outside?** The 2.884% outside neighbourhood units appears only because I did not force allocation to close. It marks a territorial limit of the indicator, not unmeasured people or a geometry error.
{: .text-justify}

**Two: what divided the total?** Per household, per person, and per square metre answer different questions. The denominator is not fine print; the most stable result is precisely that sensitivity.
{: .text-justify}

**Three: what is the observed unit?** A neighbourhood-unit map does not turn fiscal appraisal into personal wealth or a territorial ranking into a causal explanation. Scale, universe, and allocation rule have to travel with every number.
{: .text-justify}

<a class="btn btn--primary" href="{{ '/catastro_sii_brecha/?vista=distribuciones&normalizacion=m2' | relative_url }}">Explore the map and denominator lab</a>

---

## Sources

**Method and theory**

- Rosen, S. (1974). *Hedonic Prices and Implicit Markets*. Journal of Political Economy, 82(1), 34–55. [10.1086/260169](https://doi.org/10.1086/260169).
- Goodchild, M. F., Anselin, L. & Deichmann, U. (1993). *A Framework for the Areal Interpolation of Socioeconomic Data*. Environment and Planning A, 25(3), 383–397. [10.1068/a250383](https://doi.org/10.1068/a250383).
- Robinson, W. S. (1950). *Ecological Correlations and the Behavior of Individuals*. American Sociological Review, 15(3), 351–357. [10.2307/2087176](https://doi.org/10.2307/2087176).
- Shorrocks, A. F. (1984). *Inequality Decomposition by Population Subgroups*. Econometrica, 52(6), 1369–1385. [10.2307/1913511](https://doi.org/10.2307/1913511).
- Fotheringham, A. S. & Wong, D. W. S. (1991). *The Modifiable Areal Unit Problem in Multivariate Statistical Analysis*. Environment and Planning A, 23(7), 1025–1044. [10.1068/a231025](https://doi.org/10.1068/a231025).
- Hodge, T. R., McMillen, D. P., Sands, G. & Skidmore, M. (2017). *Assessment Inequity in a Declining Housing Market: The Case of Detroit*. Real Estate Economics, 45(2), 237–258. [10.1111/1540-6229.12126](https://doi.org/10.1111/1540-6229.12126).

**Data and territorial rules**

- Chilean Internal Revenue Service — [real-estate appraisal query](https://zeus.sii.cl/avalu_cgi/br/brch10.sh), first-semester 2026 cut; own aggregation, with no individual parcel attributes in the web product.
- Ministry of Social Development and Family — [IGVUST results report](https://bid-ckan-dataset.ministeriodesarrollosocial.gob.cl/dataset/ce0a80ce-e7e8-4014-a00b-23f00d93d8f1/resource/6c71d287-d441-4641-8a5a-3c48b0fd2d31/download/informe-de-resultados-igvust.pdf); June 2026 attributes and March 2026 neighbourhood-unit geometry in this processing.
- Chilean National Statistics Institute — [2024 Population and Housing Census](https://censo2024.ine.gob.cl/estadisticas/).
- [DFL No. 58 setting the text of Law No. 19.418](https://www.bcn.cl/leychile/Navegar?idNorma=70040) — definition and determination of neighbourhood units.
- [DFL No. 1 of 1998, Law No. 17.235 on Territorial Tax](https://www.bcn.cl/leychile/Navegar?buscar=17235&idNorma=128563) — fiscal-appraisal and territorial-tax framework.

Sources accessed 22 July 2026. Combining the 202603 geometry with the 202606 attributes produces 6,891 units in this processing; the official report enumerates 6,887. I document the four-unit difference between universes without attributing it to an error in either source. The tables come from the reproducible `qa/normalization_sensitivity.json` gate; the claim matrix documents the principal figures together with their universe, denominator, and limit.
{: .small}
