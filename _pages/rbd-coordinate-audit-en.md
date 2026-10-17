---
layout: single
classes: [thesis-extension-post, thesis-coordinate-audit-annex]
title: "National audit of MINEDUC–OSM school coordinates"
subtitle: "Method, aggregate results and limitations of the check used in Post II."
date: 2026-10-11 19:10:00 -0300
last_modified_at: 2026-10-17 17:15:00 -0300
categories: [data, education, methods]
tags: [education, mineduc, openstreetmap, coordinates, data-quality]
description: "Reproducible technical annex for the aggregate audit of Chilean school coordinates using OpenStreetMap signals."
excerpt: "A geographic quality audit distinguishes official coordinates, OSM candidates and unresolved cases without automatically correcting the institutional source."
author: clabra
lang: en
ref: auditoria-coordenadas-rbd
permalink: /datos/educacion/auditoria-coordenadas-rbd/
header:
  teaser: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/og-1200x630.webp
  og_image_alt: "Overlaid school points and boundaries as a metaphor for a coordinate audit."
distribution:
  social: false
---

This annex documents the geographic check used in Post II. The comparison **does not identify the causal effect** of opening or closing schools, nor does it turn OpenStreetMap (OSM) into automatic ground truth. Its narrower purpose is to detect signals that deserve review before distances are measured.

[Leer este anexo técnico en español](/datos/educacion/auditoria-coordenadas-rbd/).

## Universe and sources

- The main universe contains **12,038 operating establishments** in the 2025 MINEDUC Official Directory, covering every administrative type and region.
- Another **78 establishments authorised without enrolment** are reported separately. Both statuses make up the **12,116 official rows audited**; they are not mixed when describing the main universe of operating establishments.
- The contrast uses **18,588 candidate education features** from the OSM snapshot dated 27 August 2026.
- Commune boundaries come from the 2023 DPA: 345 valid geometries; the Antarctic commune (CUT 12202) is not evaluable because the official file does not contain its polygon.

The official unit is the establishment by directory year. OSM contributes mapped objects: a point can represent an entrance, building, campus or internal polygon centroid. Proximity therefore does not establish identity.

## Matching rules

| Level | Rule | Permitted result |
|---|---|---|
| A | An OSM reference explicitly identifies the same RBD | Highest-confidence candidate |
| B | Exact normalised name, same commune and one unique candidate | Strong candidate |
| C | Name similarity of at least 0.90, same commune and an additional signal | Mandatory review |
| D | Spatial proximity only | Diagnostic; never a match on its own |

Ties retain every alternative. Matching does not use enrolment, SIMCE, admission or any other education outcome, and it never imputes or overwrites a MINEDUC coordinate.

## Aggregate results

| Indicator | Count |
|---|---:|
| Official rows with at least one A–C candidate | 6,601 |
| Official rows without an OSM candidate | 5,515 |
| Ambiguous matches retained | 237 |
| Valid official coordinates | 11,864 |
| Missing official coordinates | 250 |
| Apparently swapped latitude and longitude | 2 |
| Commune mismatch signals | 48 |
| Cases inside the 250 m commune buffer | 31 |
| Shared-campus candidates | 207 |
| Candidate temporal jumps | 750 |
| Sample rows adjudicated by rules | 126 |
| Confirmed official errors | **0** |

Among establishments with a candidate and a calculable distance, cumulative counts are 5,230 within 100 m; 5,745 within 250 m; 6,013 within 500 m; 6,184 within 1 km; 6,324 within 2 km; and 6,465 within 5 km. These thresholds prioritise review; they are not a truth scale.

Two OSM links declare a possible MINEDUC source. They remain a shared-source risk and do not count as independent corroboration.

## Adjudication and interpretation

A stratified sample using seed `20261011`, plus mandatory rows, assembled 126 compatible or divergent explicit references, name matches and duplicate candidates. Rules then adjudicated them. The repository **does not document an independent human review of all 126 rows**, so calling them “manually reviewed” would be inaccurate. The automated outcome was deliberately conservative: **no signal was promoted to a confirmed official error**.

- An invalid coordinate is observable in the official snapshot, but OSM alone does not establish the correct point.
- A point outside its commune can reflect a border, entrance, move or error; the 250 m buffer prevents cartographic precision from becoming an administrative conclusion.
- Two RBDs separated by 10 m or less may share a campus.
- A move of at least 1 km between years can reflect relocation, merger, correction or error.
- Absence from OSM means no contrast is available, not that MINEDUC is validated.

## Public surface, licensing and reproducibility

The national audit publishes aggregates only, grouped by region, signal, confidence and distance band. The combined national establishment-level table is not published: the MINEDUC portal did not display a licence alongside the files during this review, and that absence is not treated as permission to redistribute them.

- [Download the aggregate JSON summary](/assets/data/thesis-extension-post2/coordinate-audit-summary.json).
- Official source: [MINEDUC directory of education establishments](https://datosabiertos.mineduc.cl/directorio-de-establecimientos-educacionales/).
- Cartography: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), under the [ODbL](https://opendatacommons.org/licenses/odbl/1-0/).

The national JSON fixes hashes for the aggregate sources and OSM snapshot. It contains no names, individual RBDs, addresses, coordinates or personal identifiers.

## Audit of the El Salvador case

The 2025 national audit was insufficient to validate the case shown in the viewer because RBD 391 was closed and lay outside that universe. I therefore ran a scoped check for the two El Salvador establishments, keeping the official observations and OSM candidates separate.

| Contrast result | Cases |
|---|---:|
| Official points retained | 2 |
| OSM candidates retained for comparison | 2 |
| Rejected homonyms | 1 |
| Confirmed official errors | **0** |
{: .table--compact .table--scroll}

School No. 14 (RBD 391) remains an **unresolved discrepancy**: the 2008–2011 MINEDUC directories list 500 Diego Portales and the homonymous OSM feature is compatible with that site, but it was created in 2022 and states no RBD. The candidate lies **825.551 m** from the official 2015 point. Measured from that candidate, School No. 1 is **1.272025 km** away; using both official coordinates, it is **0.448903 km** away. The viewer retains both observations and does not claim that OSM corrected MINEDUC.

- [Download the El Salvador contrast GeoJSON](/assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.geojson).
- [Download its reproducibility manifest](/assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.manifest.json).

This scoped file contains RBDs, names and coordinates already displayed in Post II, plus OSM identifiers and links. It contains no student data or personal identifiers.

## What can be concluded

The audit supports the claim that the territorial measurement has reproducible checks and that some signals require review. It does not establish that OSM corrected MINEDUC, that a discrepancy is an institutional error, or that proximity between establishments proves substitution, quality or causality.
