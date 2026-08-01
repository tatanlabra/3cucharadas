---
layout: single
title: "Appraisal and vulnerability in 3 spoonfuls: change the denominator, change the map"
subtitle: "What happens when you spread the assessed value of 9.4 million parcels across neighbourhood units and then change the unit of comparison"
date: 2026-07-26 19:20:00 -0400
categories: [data, python, territory]
tags: [cadastre, property-tax, territorial-vulnerability, inequality, gini, theil, duckdb, python, geo, geospatial, open-data]
description: "A descriptive crosswalk between Chile's fiscal appraisal records and an official territorial vulnerability index. The stable finding is not a social paradox: it is how much the reading depends on the denominator, the universe, the geometry and the territorial scale."
excerpt: "A cadastre records parcels, not people. Changing the denominator changes the map; leaving it undeclared changes the story."
author: clabra
lang: en
ref: avaluo-vulnerabilidad-uv
permalink: /datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/
header:
  teaser: /assets/images/teasers/teaser-avaluo-vulnerabilidad.webp
  og_image: /assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-social-1200x630-en.webp
  og_image_alt: "Flow diagram from 10,343,893 original cadastral records to 9,401,277 unique parcels, of which 9,130,127 intersect at least one neighbourhood unit and 271,150 fall outside the mesh entirely."
math: true
distribution:
  social: true
  republish: []
toc: true
toc_sticky: true
comments: true
author_profile: true
classes: [avaluo-vulnerabilidad-post]
---

Most countries tax immovable property, and most of them argue about it badly. The argument usually skips the part that decides the answer: before any map is coloured, someone has to choose **what is added up, what it is divided by, over which territory it is aggregated, and which cases are left out**. Change any of those and the map can change while the underlying data stay identical.
{: .text-justify}

This post works through that problem with Chilean data, because Chile happens to publish the pieces needed to do it honestly: a national cadastre of every taxable property, and an official index that ranks small civic territories by socio-territorial vulnerability. The mechanics, though, are not Chilean. Any jurisdiction that assesses property for tax and then maps the result against a deprivation measure faces exactly the same four choices.
{: .text-justify}

The question fits in one small fraction:
{: .text-justify}

$$
\text{territorial indicator}
=
\frac{\text{the total you want to describe}}
{\text{the unit you compare it against}}
$$

Adding up the assessed value inside a territory answers how much administrative value was allocated there. Dividing that same total by households, by residents or by square metres answers different questions. None of them is «the correct one» by nature; the error appears when one is presented under another's name. The arithmetic is usually innocent. The narrative is not always.
{: .text-justify}

## Reading contract

I cross two Chilean administrative registers: the real-estate cadastre of the **Servicio de Impuestos Internos (SII)** —Chile's tax authority, roughly the counterpart of the IRS or HMRC— and the **Índice Global de Vulnerabilidad Socioterritorial (IGVUST)**, a socio-territorial vulnerability index published by the Ministry of Social Development and Family. The unit of analysis is the **neighbourhood unit**, not the parcel, the household or the person.
{: .text-justify}

A word on that unit, because it has no clean equivalent elsewhere and it drives half of what follows. A Chilean **unidad vecinal (UV)** is a civic territory drawn for neighbourhood organisation and local participation — closer to a British ward or an American neighbourhood association boundary than to a census tract. Crucially, **it was never designed to tile the country**. Large stretches of rural Chile belong to no UV at all. A census geography would cover everything by construction; this one does not, and pretending otherwise is the first way to get the map wrong.
{: .text-justify}

| Concept | What it means here | What it does not mean |
|---|---|---|
| **SII cadastre** | Administrative register of real estate and its characteristics. | A population census or a register of residents. |
| **Parcel** | Cadastral unit identified by municipality, block and parcel number. | A dwelling, a household, an owner or a person. |
| **Fiscal appraisal** | Administrative valuation used as the base of the property tax. | Sale price, income, or the wealth of whoever lives there. |
| **IGVUST** | A ranking of neighbourhood units by socio-territorial vulnerability. | An individual diagnosis or a causal mechanism. |
| **RSH** | Chile's *Registro Social de Hogares*, the means-testing registry that supplies the households and people used as denominators. In this processing it sums 15,978,644 people, close to 85% of the country's population. | A complete census, or a universe with even coverage across municipalities. |
| **Neighbourhood unit (UV)** | Territory defined for neighbourhood organisation and participation. | An exhaustive mesh covering all of Chile parcel by parcel. |
| **Denominator** | The magnitude the allocated appraisal is divided by. | Small print added afterwards: it defines the question. |

The RSH matters because it is the source of the households and people I use as denominators. Nationally it is broad —around 85% of the population— but it does not cover every municipality equally. In municipalities with low relative RSH enrolment, as can happen in the wealthiest districts of Santiago, an indicator «per RSH household» can inflate because the denominator is narrow, not because there is more appraised value. That is a coverage artefact, not a finding.
{: .text-justify}

Fiscal appraisal is also not market price: the SII builds it from the characteristics of the property and its homogeneous valuation zone, not from an observed transaction. It can be a useful territorial signal as long as it keeps its surname, **fiscal** — [Rosen's (1974)](https://doi.org/10.1086/260169) hedonic price theory explains why surroundings weigh on the valuation of a differentiated good such as housing, but this post observes neither transactions nor household wealth.
{: .text-justify}

One note on notation for readers used to the short scale: Chilean Spanish uses *billón* for 10¹². Throughout this English version I write **trillion** for that same quantity. Chilean pesos traded around 980 CLP per US dollar in July 2026, so the national total below —587.4 trillion CLP— is on the order of US$600 billion.
{: .small}

**Data cut:** 19 July 2026. **Editorial date:** 26 July 2026. All relationships are descriptive and depend on the UV mesh used.
{: .small}

## The question

I aggregated the fiscal appraisal of SII parcels to UV scale and compared it against the IGVUST national vulnerability ordering, holding the numerator fixed and changing the lens:
{: .text-justify}

| Measure | Question it answers |
|---|---|
| Total appraisal | How much fiscal appraisal was allocated to this UV? |
| Appraisal per RSH household | How much allocated appraisal corresponds to each registered household in the UV? |
| Appraisal per RSH person | How much corresponds to each registered person? |
| Appraisal per m² of parcel area | How much corresponds to each square metre of allocated parcel surface? |

The short answer: per household and per person there is almost no relationship with vulnerability. Per square metre a strong national relationship appears, but it dissolves when you look only at predominantly urban UVs. This is not a glamorous paradox between wealth and vulnerability. It is more sober, and therefore more useful: **the denominator, the universe and the scale are part of the result**.
{: .text-justify}

A warning before continuing: none of this says how much the people living there earn, what their house is worth on the market, or who owns it. Turning a territorial association into a statement about persons is precisely the ecological inference [Robinson (1950)](https://doi.org/10.2307/2087176) warned about more than seventy years ago.
{: .text-justify}

## Before the spoonfuls: why we tax what cannot move

The property tax has a less exotic logic than its public reputation suggests. Property is a visible base, immobile, and tied to the territory where services are delivered. In Chile, property tax revenue is municipal: part stays in the municipality of origin and part feeds the **Fondo Común Municipal**, an equalisation fund that redistributes resources for street lighting, green areas, infrastructure and social programmes ([SII, *Impuesto Territorial*](https://www.sii.cl/destacados/impuesto_territorial/index.html)). Without a cadastre, appraisals and parcel-level location, that architecture simply does not work.
{: .text-justify}

None of this is a Chilean peculiarity. Recurrent taxes on immovable property hold a relevant place in local finance across many countries. The comparison assembled by the World Bank shows collections close to 2%–3% of GDP in the United States, Canada and the United Kingdom, and significant shares of local revenue. These are not copies of the Chilean system, but they share the same intuition: part of the value that accumulates in a territory helps finance that territory ([World Bank, 2020](https://openknowledge.worldbank.org/handle/10986/34793)).
{: .text-justify}

The comparative evidence does not say that any property tax is fair by definition. It says something more uncomfortable: **design rules**. The OECD and the IMF highlight its immobile base, its revenue potential and its link to local services, but they recommend up-to-date valuations, moderate rates, and targeted or deferred relief for owners with low liquidity. The IMF itself uses the British *Council Tax* as an example of how overly compressed bands can produce a regressive outcome ([OECD, 2022](https://doi.org/10.1787/03dfe007-en); [IMF, 2024](https://doi.org/10.5089/9798400288753.061)). The instrument does not arrive progressive from the factory.
{: .text-justify}

There is, of course, a flashier route: delete a line from the bill and rebuild the cost on another spreadsheet. The sum can balance; the distribution need not. When an exemption stops looking at income or value and the compensation reproduces prior revenue, the tax does not disappear: it changes pocket, fund, or postcode. The accounting stays calm. The territory may not.
{: .text-justify}

Seen that way, the cadastre stops being a collection of tax rolls and becomes what it actually is: the infrastructure that lets you measure the base, divide it, and argue about who benefits from each rule. Now, the three spoonfuls.
{: .text-justify}

## Spoonful 1: building the numerator without closing the leak

The original extract holds **10,343,893 records**. A record is not the same as a unique parcel; administrative databases have echoes too. After deduplicating the cadastral key —municipality, block and parcel number— **9,401,277 parcels** remain. The goal is to distribute their appraised value across **6,891 UVs** before testing any denominator.
{: .text-justify}

Parcels and UVs are both polygons, but their boundaries do not coincide. A parcel can fall entirely inside one UV, straddle several, or touch none. I use areal apportionment by intersection area, a form of areal interpolation ([Goodchild, Anselin & Deichmann, 1993](https://doi.org/10.1068/a250383)):
{: .text-justify}

$$
f_{p,u} = \frac{\text{area}(p \cap u)}{\text{area}(p)}
\qquad
A_u = \sum_{p} a_p \cdot f_{p,u}
$$

where $$a_p$$ is the parcel's fiscal appraisal and $$A_u$$ the total allocated to the neighbourhood unit. If the parcel sits entirely inside one UV, it contributes everything; if it straddles the boundary in half, it contributes half.
{: .text-justify}

Two methodological decisions matter.
{: .text-justify}

**I use geometric area to apportion.** Among unique parcels, 10.7% have no usable declared surface and 2.8% have no geometry at all. Declared surface can serve for auditing or sensitivity checks, but it is not enough to place a parcel in space when there is no polygon. So I do not impute UV allocation from reported square metres alone. If a fallback is implemented later, it has to enter the analytical pipeline first, with an explicit location rule, and only then the post and the viewer. A pretty map is not a licence to invent geometry.
{: .text-justify}

**I do not renormalise.** If $$\sum_u f_{p,u} < 1$$, part of the parcel fell outside every UV. Redistributing that remainder among the UVs it did touch would produce a perfect sum —very convenient for the chart— and a worse measurement: it would hide the fact that the UV was never designed to tile Chile.
{: .text-justify}

The residual is concrete: **271,150 parcels**, **2.884%** of the deduplicated set, landed in no UV at all. The median municipal leakage is **0.644%**, but it is not homogeneous. In Antofagasta, 2,325 parcels outside any UV concentrate **32.6%** of the municipality's fiscal appraisal; in Tortel, Timaukel, San Gregorio, Laguna Blanca and Río Verde the leakage reaches 100%, because the UVs cover the settlement and the catalogued parcels lie outside that mesh.
{: .text-justify}

That bias gets declared, not swept under the rug. In municipalities with many parcels lacking polygons, or with heavy leakage outside the UV mesh, the crosswalk under-represents part of the cadastre. Public reading has to look at those indicators before interpreting any colour.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.webp' | relative_url }}" title="Figure 1 — From the original register to the spatial universe" aria-label="Open Figure 1 enlarged">
    <picture>
      <source srcset="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.svg' | relative_url }}" type="image/svg+xml">
      <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/sankey-pipeline-en.webp' | relative_url }}" alt="Flow diagram: 10,343,893 original records split into 942,616 duplicates and 9,401,277 unique parcels; of the latter, 9,130,127 touch at least one neighbourhood unit and 271,150 touch none." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 1</strong> — From the original register to the spatial universe. «Touches at least one UV» does not mean full allocation: a parcel can intersect a UV and still keep part of its surface outside the mesh. Source: own elaboration, data cut 19/07/2026. Click to enlarge.</figcaption>
</figure>

## Before the IGVUST: the size of the observed appraisal

Before crossing anything with vulnerability, it helps to know the order of magnitude. Across the 346 municipalities, allocated fiscal appraisal sums **587.4 trillion pesos** (≈US$600 billion). The Santiago Metropolitan Region concentrates **286.7 trillion** (**48.8%**); Valparaíso, **56.2 trillion** (**9.6%**); Biobío, **39.4 trillion** (**6.7%**). The concentration is not a detail: it sets the size of the numerator that later gets divided.
{: .text-justify}

{: .table-caption}
**Table 1** — Allocated fiscal appraisal before normalising

| Level | Territory | Allocated appraisal (trillion CLP) | National share |
|---|---|---:|---:|
| Region | Metropolitana | 286.7 | 48.8% |
| Region | Valparaíso | 56.2 | 9.6% |
| Region | Biobío | 39.4 | 6.7% |
| Region | La Araucanía | 28.2 | 4.8% |
| Region | Maule | 26.4 | 4.5% |
| Municipality | Las Condes | 38.2 | 6.5% |
| Municipality | Santiago | 27.1 | 4.6% |
| Municipality | Providencia | 16.3 | 2.8% |
| Municipality | Lo Barnechea | 16.0 | 2.7% |
| Municipality | Vitacura | 15.2 | 2.6% |

Shares are computed over the national allocated total of 587.4 trillion. The amounts for La Araucanía and Maule are derived from that published share, not from a separately measured figure. In municipalities with UV leakage or low relative coverage of the RSH denominator, this size should not be confused with a complete reading of the territory or its residents.
{: .small}

The five municipalities in the table add up to **112.8 trillion**: **19.2% of the entire allocated base of the country**, in five municipalities out of 346, all of them in the eastern districts of Santiago. That is the concentration that later disappears from view once you divide by households or by square metres. Antofagasta also ranks high (**15.1 trillion**), but with very high municipal UV leakage; that is exactly the kind of case where the total, the denominator and the universe have to be read together.
{: .text-justify}

The viewer carries this raw reading in the **Appraisals** tab of its denominator laboratory. First the numerator; then the story.
{: .text-justify}

## Spoonful 2: quartiles, bivariate map and denominators

The IGVUST ranks neighbourhood units by socio-territorial vulnerability. I keep its four official quartiles because they are that source's analytical contract — and note the direction, because it is easy to reverse: **`q1` is the most vulnerable quartile** and `q4` the least. On the appraisal axis, each UV is compared against the median of **its own region**, not against a fixed national cut: it lands below or above that regional median. The result is a 4×2 matrix —four IGVUST rows by two appraisal columns— which avoids two problems at once: a finer partition would make the bivariate map hard to read and, in regions with few UVs such as Arica y Parinacota, would suggest a precision the aggregated data do not deliver; and a fixed national cut would ignore that typical appraisal levels differ sharply between regions. A quartile indicates relative order, not distance.
{: .text-justify}

In the bivariate map the main reading uses **appraisal per m² of parcel area**. It is the clearest signal for drawing attention where high unit appraisal coincides with high territorial vulnerability. In the palette those cells are darker, with a transparent layer so as not to cover the basemap or turn the map into a chromatic alarm. The counterintuitive should draw attention; the obvious does not need a megaphone. The indicator remains descriptive and national; restricting to UVs with $$p_\text{urban} > 50$$ attenuates the per-m² association sharply.
{: .text-justify}

In the viewer, this crosswalk lives in an analytical map: UVs only, a graphic selector of Chile, hover with the unit's data, and a 4×2 legend. A single region-and-municipality search box governs the whole tour, and the selection you fix there carries into the tables and the territorial ranking where it applies. Inspecting parcel geometry is deliberately kept apart, as a documented annex: mixing it with the bivariate classification invites reading a cadastral boundary as if it were a result.
{: .text-justify}

### 1. Per household, the eye-catching cell is a lead

If you divide by RSH households, the most vulnerable quartile (`q1` IGVUST) contains 530 UVs in the highest quartile of appraisal per household. That number can look like a social contradiction. It is not one yet.
{: .text-justify}

{: .table-caption}
**Table 2** — Neighbourhood units by national vulnerability quartile and appraisal per household

| IGVUST quartile | Appraisal/household q1 | q2 | q3 | q4 |
|---|---:|---:|---:|---:|
| q1 · most vulnerable | 399 | 344 | 446 | **530** |
| q2 | 564 | 451 | 385 | 321 |
| q3 | 467 | 509 | 429 | 316 |
| q4 · least vulnerable | 293 | 419 | 463 | 546 |

The right word is **lead**, not conclusion. The ratio combines territorial appraisal with RSH households. If the denominator is small or the territory is large, the quotient rises without that demonstrating any greater wealth among the people who live there.
{: .text-justify}

### 2. The eye-catching quadrant has fewer households and far more area

The vulnerable UVs with the highest appraisal per household have a median of **120.5 households** and **78.2 km²**. The vulnerable ones with the lowest appraisal per household have **265 households** and **3.36 km²**. The ratio grows because the denominator shrinks while the territory expands. The spreadsheet does its job; interpretation has to do its own.
{: .text-justify}

{: .table-caption}
**Table 3** — Mechanism inside the most vulnerable quartile (`q1` IGVUST)

| Appraisal/household | UVs | Median households | Median area (km²) | Median appraisal/household (million CLP) |
|---|---:|---:|---:|---:|
| q1 | 399 | 265.0 | 3.36 | 10.2 |
| q2 | 344 | 368.5 | 15.21 | 26.2 |
| q3 | 446 | 274.5 | 45.59 | 57.6 |
| q4 | 530 | 120.5 | 78.22 | 185.6 |

The table does not invalidate the crosswalk. It delimits what it measures: fiscal appraisal allocated to a UV divided by RSH households, not the wellbeing of its residents.
{: .text-justify}

### 3. The association changes with normalisation

The next table uses two summaries between -1 and +1. **Pearson** summarises a linear relationship over the logarithm of positive appraisal; **Spearman** summarises whether the ordering of UVs changes monotonically. Near zero there is little linear or monotonic relationship. Neither column estimates a causal effect.
{: .text-justify}

{: .table-caption}
**Table 4** — Sensitivity of the association to the denominator

| Appraisal measure | Pearson | Spearman | UVs |
|---|---:|---:|---:|
| Total allocated | -0.371 | -0.382 | 6,857 |
| Per RSH household | -0.061 | -0.047 | 6,849 |
| Per RSH person | -0.079 | -0.072 | 6,849 |
| Per m² of allocated parcel area | -0.582 | -0.575 | 6,851 |
| Per m², predominantly urban UVs only | +0.079 | +0.081 | 3,221 |

Per household and per person, the association is close to nil. Per square metre, the national pattern looks strong. Restricting to predominantly urban UVs it flips to roughly +0.08. The prudent reading is that the national per-m² result contains a great deal of urban–rural contrast; not that a neighbourhood-level mechanism has been identified.
{: .text-justify}

The violins in Figure 2 show the full distribution. Their width indicates where more UVs concentrate; the internal lines show median and interquartile range. They are smoothed densities, not literal silhouettes of the territory.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores-en.webp' | relative_url }}" title="Figure 2 — Sensitivity to denominator and universe" aria-label="Open Figure 2 enlarged">
    <picture>
      <source srcset="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores-en.svg' | relative_url }}" type="image/svg+xml">
      <img src="{{ '/assets/images/avaluo-vulnerabilidad-unidad-vecinal/violin-denominadores-en.webp' | relative_url }}" alt="Three violin plots compare the distributions of appraisal per household, appraisal per square metre nationally, and appraisal per square metre in predominantly urban neighbourhood units, across the four national vulnerability quartiles." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figure 2</strong> — The same appraisal produces different distributions once the denominator and the universe change. The violins show estimated densities; their shape depends on the bandwidth and proves neither natural groupings nor causality. The internal lines summarise median and interquartile range. Source: own elaboration, data cut 19/07/2026. Click to enlarge.</figcaption>
</figure>

### 4. What is robust is the sensitivity

Among the **6,843 UVs** with an available quartile both per household and per m², only **1,362 (19.9%)** stay in the same quartile and **3,132 (45.8%)** move two or more. The parcels did not change. The question did.
{: .text-justify}

## Spoonful 3: scale and concentration

Among the **6,857 UVs with positive allocated appraisal**, the Gini coefficient is **0.7265**. It describes a highly concentrated territorial tax base; it is not a Gini of personal income or wealth.
{: .text-justify}

This matters beyond the statistical exercise. On a base this concentrated, any exemption also redistributes: it decides not only who stops paying, but which municipality, fund or tax will have to rebuild the amount. The benefit fits on one line; the full incidence usually needs another spreadsheet.
{: .text-justify}

The Gini summarises concentration but does not separate how much occurs within and between groups. That is what the **Theil** index is for, since it does decompose. With $$x_i$$ as the appraisal allocated to UV $$i$$, $$\mu$$ its mean and $$w_g$$ the share of group $$g$$ in total appraisal:
{: .text-justify}

$$
T = \frac{1}{n}\sum_{i=1}^{n} \frac{x_i}{\mu} \ln\!\left(\frac{x_i}{\mu}\right)
= \underbrace{\sum_{g} w_g T_g}_{\text{within}} + \underbrace{\sum_{g} w_g \ln\!\left(\frac{\mu_g}{\mu}\right)}_{\text{between}}
$$

Grouping by region, $$T = 1.2042$$ and 81.0% stays within regions. Regrouping by municipality, the between-group part reaches 56.9%. The municipality does not «reveal» segregation by magic: when you refine a partition, part of the inequality shifts from the within component to the between component by construction ([Shorrocks, 1984](https://doi.org/10.2307/1913511)).
{: .text-justify}

That is the modifiable areal unit problem, or MAUP ([Fotheringham & Wong, 1991](https://doi.org/10.1068/a231025)). The same parcels can produce different statistics depending on whether they are grouped into regions, municipalities or UVs. Scale does not decorate the result: it defines it. Which is why it matters what the UV actually is before using it as a container: if the unit does not correspond to a territory with its own meaning, the statistic it produces inherits that mismatch.
{: .text-justify}

Second brake: IGVUST quartiles order UVs, not people. The most vulnerable quartile gathers 25% of the units, but **2,032,893 of 15,978,644 RSH people (12.7%)**. A choropleth can over-represent dispersed rural territory even when its colours are perfectly computed.
{: .text-justify}

Third brake: the *assessment ratio* literature shows that fiscal valuation can depart systematically from market values, and that the pattern depends on institutional context. [Hodge, McMillen, Sands and Skidmore (2017)](https://doi.org/10.1111/1540-6229.12126) study that problem in another market; they do not prove the SII carries the same bias. What they do show is that using fiscal appraisal as a synonym for market price requires substantial adjustment factors — although, even so, territorial gradients and trends should not diverge that much.
{: .text-justify}

## Closing: gaps pay property tax too

The map does not dictate a tax policy. It does make it impossible to pretend the base is homogeneous, that every municipality starts from the same place, or that an exemption has no geography. The crosswalk identifies five gaps that must be closed before its colours can be used as strong evidence.
{: .text-justify}

**Gap 1: the denominator's universe.** The RSH covers around 85% of the country's population, but not with equal intensity across municipalities. Any indicator per RSH household or person has to declare that coverage and, where applicable, contrast it against census data. That contrast is exactly what the viewer opens with: before any crosswalk, it measures what fraction of the **private dwellings counted in the 2024 Census** is reached by the SII residential register, municipality by municipality. It is the same warning as this post, in its simplest form — declare the universe before dividing by it.
{: .text-justify}

**Gap 2: geometry and surface.** Apportionment requires polygons. Declared surface does not replace missing geometry without an additional spatial rule. Municipalities with many parcels lacking polygons need a warning before anyone interprets their colour.
{: .text-justify}

**Gap 3: leakage outside the UV mesh.** The UV does not cover the entire cadastral territory. If a municipality concentrates a lot of appraisal outside any UV, the crosswalk describes a subset, not its municipal total. The UV mesh needs local work to fit reality better.
{: .text-justify}

**Gap 4: urban–rural.** Appraisal per m² has a strong national signal, but it changes when the universe is restricted to urban UVs. The indicator needs a universe filter, not just an intense palette.
{: .text-justify}

**Gap 5: scale.** Region, municipality and UV are not enlarged versions of the same question. Changing the territorial unit changes the statistic.
{: .text-justify}

These gaps are not an automatic defence of every appraisal, rate or charge in force either. Relieving someone with little liquidity and a highly valued home is a real problem. Comparative evidence offers more precise instruments: income-based reductions, caps on the tax burden, deferrals until sale or inheritance, and transparent reassessments. There is no need to ask the cadastre to pretend the asset stopped existing.
{: .text-justify}

You can, of course, remove the obligation from one column and restore it with transfers from another. The relief stays visible; its financing moves. Before celebrating that the bill disappeared, it is worth checking the second spreadsheet and asking which territories end up paying for the courtesy.
{: .text-justify}

The viewer lets you explore these gaps from the general to the particular: the whole country, the municipality you choose, its neighbourhood units in the bivariate map, and a laboratory that zooms back out to test denominators, with an appraisals view, distributions, sensitivity checks and a municipal reading. An exemption does not stop being distributive because it is called a benefit: it also has a numerator, a denominator and a geography.
{: .text-justify}

<a class="btn btn--primary" href="{{ '/catastro_sii_brecha/' | relative_url }}">Explore the map and the denominator laboratory</a>

The viewer's interface is in Spanish, but its charts, tables and downloadable Parquet files are readable without it.
{: .small}

---

## Sources

**Property tax and international comparison**

- Servicio de Impuestos Internos (SII). *Impuesto Territorial*. Tax base, exemptions, reassessment and cadastral mapping. [sii.cl](https://www.sii.cl/destacados/impuesto_territorial/index.html).
- Servicio de Impuestos Internos (SII). *¿Para qué sirve el pago del impuesto territorial?* Municipal destination and the Fondo Común Municipal. [sii.cl](https://www.sii.cl/destacados/reavaluo/contribucionesreavaluo.html).
- OECD (2022). *Housing Taxation in OECD Countries*. OECD Tax Policy Studies, No. 29. [10.1787/03dfe007-en](https://doi.org/10.1787/03dfe007-en).
- Grote, M. & Wen, J.-F. (2024). *How to Design and Implement Property Tax Reforms*. IMF How-To Notes, 2024/006. [10.5089/9798400288753.061](https://doi.org/10.5089/9798400288753.061).
- World Bank (2020). *Property Tax Diagnostic Manual*. [Institutional repository](https://openknowledge.worldbank.org/handle/10986/34793).
- Senate of the Republic of Chile (15 July 2026). *Reconstrucción nacional: ¿cuáles fueron los aspectos centrales aprobados?* Legislative background to Bill No. 18.216-05, accessed 26 July 2026. [senado.cl](https://www.senado.cl/comunicaciones/noticias/reconstruccion-nacional-cuales-fueron-los-aspectos-centrales-aprobados).
- Cooperativa (22 July 2026). *Megarreforma: comisión mixta aprobó compensación a municipios por exención de contribuciones*. Formula approved by the joint committee and status of the bill, accessed 26 July 2026. [cooperativa.cl](https://www.cooperativa.cl/noticias/pais/politica/agenda-legislativa/megarreforma-comision-mixta-aprobo-compensacion-a-municipios-por/2026-07-22/171256.html).

**Method and theory**

- Sabatini, F., Cáceres, G. & Cerda, J. (2001). *Segregación residencial en las principales ciudades chilenas: Tendencias de las tres últimas décadas y posibles cursos de acción*. EURE, 27(82), 21-42. [10.4067/S0250-71612001008200002](https://doi.org/10.4067/S0250-71612001008200002).
- López-Morales, E., Sanhueza, C., Espinoza, S. & Órdenes, F. (2019). *Verticalización inmobiliaria y valorización de renta de suelo por infraestructura pública: un análisis econométrico del Gran Santiago, 2008-2011*. EURE, 45(136), 113-134. [10.4067/S0250-71612019000300113](https://doi.org/10.4067/S0250-71612019000300113).
- Rosen, S. (1974). *Hedonic Prices and Implicit Markets*. Journal of Political Economy, 82(1), 34-55. [10.1086/260169](https://doi.org/10.1086/260169).
- Goodchild, M. F., Anselin, L. & Deichmann, U. (1993). *A Framework for the Areal Interpolation of Socioeconomic Data*. Environment and Planning A, 25(3), 383-397. [10.1068/a250383](https://doi.org/10.1068/a250383).
- Robinson, W. S. (1950). *Ecological Correlations and the Behavior of Individuals*. American Sociological Review, 15(3), 351-357. [10.2307/2087176](https://doi.org/10.2307/2087176).
- Shorrocks, A. F. (1984). *Inequality Decomposition by Population Subgroups*. Econometrica, 52(6), 1369-1385. [10.2307/1913511](https://doi.org/10.2307/1913511).
- Fotheringham, A. S. & Wong, D. W. S. (1991). *The Modifiable Areal Unit Problem in Multivariate Statistical Analysis*. Environment and Planning A, 23(7), 1025-1044. [10.1068/a231025](https://doi.org/10.1068/a231025).
- Hodge, T. R., McMillen, D. P., Sands, G. & Skidmore, M. (2017). *Assessment Inequity in a Declining Housing Market: The Case of Detroit*. Real Estate Economics, 45(2), 237-258. [10.1111/1540-6229.12126](https://doi.org/10.1111/1540-6229.12126).
