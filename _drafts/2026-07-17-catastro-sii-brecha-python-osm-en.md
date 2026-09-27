---
layout: single
# Retirado de publicación: se reescribe antes de volver a salir.
published: false
title: "A cadastre is not a census: measuring residential coverage with Python and OSM"
subtitle: "H records, Parquet, neon cells, and one rule against inventing residents"
date: 2026-07-17 15:00:00 -0400
categories: [data, python, openstreetmap]
tags: [python, openstreetmap, osm, maplibre, parquet, sii-cadastre, census-2024, open-data, geodata]
description: "A Python + OpenStreetMap viewer comparing the residential-equivalent coverage of Chile's SII cadastre against the 2024 Census."
excerpt: "Nearly six million H records are not nearly six million households. That distinction now has a viewer."
author: clabra
lang: en
ref: catastro-sii-brecha-python-osm
permalink: /datos/python/openstreetmap/catastro-sii-brecha/
header:
  teaser: /assets/images/heroes-v2/catastro-sii-brecha-python-osm/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/catastro-sii-brecha-python-osm/og-1200x630.webp
  og_image_alt: Homes, parcels and luminous households as a metaphor for the difference between a cadastre and a census.
  overlay_image: /assets/images/heroes-v2/catastro-sii-brecha-python-osm/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/catastro-sii-brecha-python-osm/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/catastro-sii-brecha-python-osm/teaser-mobile-640x360.webp
visual_id: catastro-sii-brecha-python-osm
distribution:
  social: true
  republish: [dev]
toc: true
toc_sticky: true
comments: true
author_profile: true
ai_disclosure:
  level: some_ai
  components:
    text: unknown
    hero: generated
---

Chile's SII cadastre is excellent for looking at territory. It is also easy to misuse: N property records becomes N households becomes N residents. It does not.
{: .text-justify}

I built the [SII residential coverage gap viewer](/catastro_sii_brecha/). It starts from residential-destination (`H`) records and asks a narrower question: what share of a commune's 2024 Census population would those records cover if they followed that commune's people-per-occupied-dwelling ratio?
{: .text-justify}

It does not locate residents. It does not explain informality, vacancy, classification errors, or undercount. It measures equivalent register coverage. The limitation is the feature.
{: .text-justify}

## One auditable equation

```python
population_equivalent = H_records * (census_population_2024 / occupied_dwellings_with_residents)
coverage = population_equivalent / census_population_2024
```

The primary comparison uses the 2024 Census. A separate historical context compares the same equivalent population with INE's 2024 projection based on the 2017 Census; it is not presented as a 2024-Census-based projection.
{: .text-justify}

CASEN 2024 is kept as a sensitivity only. The survey supports a weighted communal arithmetic, but the Chilean social development ministry does not recommend commune-level representative estimates. It does not rank communes, colour the map, or write the headline.
{: .text-justify}

## Python for data, OSM for a map that stays honest

The pipeline is Python-first: columnar reads from the canonical SII cut, official Census and INE inputs normalized to Zstandard-compressed Parquet, and a reproducible commune-level table. A browser is not an HPC cluster, so it does not ingest six million records on first load.
{: .text-justify}

Valid H coordinates become aggregated Web Mercator density cells. That gives a neon concentration layer over a dark OpenStreetMap base without claiming that each glow is a particular home. The initial load contains 346 commune indicators; cells are requested only after a commune is selected.
{: .text-justify}

The crosswalk is part of the result. The SII cut splits Santiago into three extracts while the Census has one commune; Trehuaco and Antarctica have no SII extract in this cut. The build documents those facts instead of silently imputing records.
{: .text-justify}

The viewer includes a public Parquet download and [methodology page](/catastro_sii_brecha/metodologia.html). The useful first question is not “how many people live there?” but “how much of the population can this register represent under stated rules?” Everything else needs evidence after that.
{: .text-justify}
