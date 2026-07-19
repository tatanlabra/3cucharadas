---
layout: single
title: "CASEN 2024 en 3 cucharadas: sin lectura regional, la política social decide a ciegas"
date: 2026-07-14
categories: [datos, politica-publica, julia]
tags: [casen2024, julia, expansion, diseno-muestral, waffle, dotplot, politica-publica]
description: "Validación oficial BIDAT + lectura regional en Julia: una base para priorización territorial con evidencia trazable."
author: "Equipo 3 Cucharadas"
toc: true
toc_sticky: true
author_profile: true
---

Cuando una política social se define solo con promedios nacionales, el riesgo no es técnico: es político. Este post defiende una tesis simple y exigente: **sin contraste oficial y sin lectura regional, CASEN se usa por debajo de su estándar público**.

Fuente oficial de contraste: https://bidat.gob.cl/details/ficha/dataset/base-de-datos-casen-2024

## Gate de validación oficial (antes de interpretar)

- Estado validación estricta (nacional + regional, porcentajes + expandidos): **PASS**.
- Tolerancia usada (pp): `1.0e-5`
- Tolerancia usada (expandido): `1.0e-6`
- Máx diferencia en porcentajes (pp): `2.9795683218480917e-6`
- Máx diferencia en expandidos: `0.0`
- Traducción sustantiva: esa diferencia máxima equivale aproximadamente a **1 persona** sobre la población expandida total.

## Cucharada 1: diseño muestral y expansión sin atajos

Con factor de expansión `expr`, la suma de ponderadores representa población objetivo.
En esta ejecución: **2.0131682e7 personas** (aprox. **20.13 millones**).

Definición operacional de muestra compleja en el flujo (snippet corto):

```julia
# Especificación mínima del diseño muestral CASEN 2024
design = (
    weight = :expr,
    strata = :estrato,
    psu    = :cod_upm,
    domain = :region,
)
```

Cobertura por indicador: educación=`edad >= 18`, salud=`población total`, pobreza=`población total`.

## Cucharada 2: qué decisiones soporta y cuáles aún no

**Sí soporta (esta versión):**
- priorización territorial inicial,
- identificación de brechas descriptivas robustas,
- comunicación ejecutiva con trazabilidad oficial.

**No soporta todavía (sin SE/IC):**
- ranking fino de regiones con pretensión inferencial,
- comparación estadística formal entre subpoblaciones,
- evaluación de impacto causal.

Snippet ilustrativo de chart regional (mínimo y gráfico):

```julia
using DataFrames, CairoMakie

sub = table_policy_region[
    (table_policy_region.dimension .== "pobreza") .&
    (table_policy_region.category .== "Pobreza extrema"), :
]
sort!(sub, :share, rev=true)

fig = Figure(size=(900, 420))
ax = Axis(fig[1, 1], xlabel="% población", ylabel="Región")
scatter!(ax, sub.share .* 100, 1:nrow(sub))
```

## Cucharada 3: evidencia visual nacional y regional

### 3.1 Resultados nacionales (composición)

![Waffle nacional educación]({{ "/assets/images/casen2024-julia-waffles-politica-publica/waffle_educacion_educc.png" | relative_url }})

![Waffle nacional salud]({{ "/assets/images/casen2024-julia-waffles-politica-publica/waffle_salud_s13.png" | relative_url }})

![Waffle nacional pobreza]({{ "/assets/images/casen2024-julia-waffles-politica-publica/waffle_trabajo_ingresos_pobreza.png" | relative_url }})

### 3.2 Resultados regionales (small multiples de dot plot)

Cada panel usa eje regional ajustado a su categoría y agrega referencia nacional, para visibilizar diferencias que se pierden en escalas globales.

![Dot plot regional educación]({{ "/assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_educacion_educc.png" | relative_url }})

- En **Media Completa**, la brecha territorial es de **11.1 pp**: máximo en **Antofagasta** (37.3%) y mínimo en **Aysén** (26.2%).
- En **Superior Completa**, la brecha territorial es de **14.5 pp**: máximo en **Metropolitana** (34.9%) y mínimo en **Maule** (20.4%).

![Dot plot regional salud]({{ "/assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_salud_s13.png" | relative_url }})

- En **Sistema Público FONASA**, la brecha territorial es de **15.2 pp**: máximo en **La Araucanía** (91.1%) y mínimo en **Metropolitana** (75.9%).
- En **Isapre**, la brecha territorial es de **16.3 pp**: máximo en **Metropolitana** (20.6%) y mínimo en **Maule** (4.3%).

![Dot plot regional pobreza]({{ "/assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_trabajo_ingresos_pobreza.png" | relative_url }})

- En **No pobreza**, la brecha territorial es de **18.7 pp**: máximo en **Magallanes** (90.1%) y mínimo en **La Araucanía** (71.4%).
- En **Pobreza extrema**, la brecha territorial es de **8.8 pp**: máximo en **La Araucanía** (13.0%) y mínimo en **Magallanes** (4.2%).

## Cierre: recomendación accionable

Si una institución pública ya usa CASEN para asignación territorial, este flujo debería ser estándar mínimo: **validación oficial + lectura regional explícita + trazabilidad reproducible**.

La mejora pendiente es clara: incorporar SE/IC de diseño para pasar de brechas descriptivas robustas a decisiones comparativas con inferencia formal.
