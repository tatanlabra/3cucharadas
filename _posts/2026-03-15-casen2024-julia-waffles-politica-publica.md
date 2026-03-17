---
layout: single
title: "CASEN 2024 en 3 cucharadas: sin lectura territorial a baja escala, la política social avanza a ciegas"
date: 2026-03-15
categories: [datos, politica-publica, julia, casen]
tags: [casen2024, julia, expansion, diseno-muestral, waffle, dotplot, politica-publica, bidat, brecha-territorial]
description: "Análisis reproducible de CASEN 2024 en Julia: validación oficial con datos en el BIDAT, composición nacional por waffle chart y brechas regionales en educación, salud y pobreza para priorización territorial."
author: "3 Cucharadas"
toc: true
toc_sticky: true
author_profile: true
header:
  og_image: /assets/images/casen2024-julia-waffles-politica-publica/waffle_trabajo_ingresos_pobreza.png

gallery_nacional:
  - url: /assets/images/casen2024-julia-waffles-politica-publica/waffle_educacion_educc.png
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/waffle_educacion_educc.png
    alt: "Gráfico 1: Distribución del nivel educacional alcanzado en la población adulta (≥18 años), Chile, CASEN 2024. Waffle chart de 100 celdas con proporciones por largest remainder."
    title: "Gráfico 1 — Educación: nivel educacional alcanzado (población ≥18 años, CASEN 2024)"
  - url: /assets/images/casen2024-julia-waffles-politica-publica/waffle_salud_s13.png
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/waffle_salud_s13.png
    alt: "Gráfico 2: Distribución del sistema previsional de salud al que pertenece la población, Chile, CASEN 2024. Waffle chart con 6 categorías incluyendo FONASA, Isapre y otros."
    title: "Gráfico 2 — Salud: sistema previsional de salud (población total, CASEN 2024)"
  - url: /assets/images/casen2024-julia-waffles-politica-publica/waffle_trabajo_ingresos_pobreza.png
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/waffle_trabajo_ingresos_pobreza.png
    alt: "Gráfico 3: Situación de pobreza por ingresos en Chile según CASEN 2024: pobreza extrema, pobreza no extrema y no pobreza. Waffle chart de 100 celdas."
    title: "Gráfico 3 — Pobreza por ingresos: extrema, no extrema y no pobreza (población total, CASEN 2024)"

gallery_regional:
  - url: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_educacion_educc.png
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_educacion_educc.png
    alt: "Gráfico 4: Dot plot de brechas regionales en nivel educacional por categoría, CASEN 2024. Cada panel tiene eje ajustado a su rango; punto vacío indica referencia nacional."
    title: "Gráfico 4 — Brechas regionales en educación: dot plot por categoría (eje ajustado por panel, punto vacío = referencia nacional)"
  - url: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_salud_s13.png
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_salud_s13.png
    alt: "Gráfico 5: Dot plot de brechas regionales en sistema previsional de salud por categoría, CASEN 2024. Eje ajustado por panel con referencia nacional."
    title: "Gráfico 5 — Brechas regionales en salud: dot plot por categoría (eje ajustado por panel, punto vacío = referencia nacional)"
  - url: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_trabajo_ingresos_pobreza.png
    image_path: /assets/images/casen2024-julia-waffles-politica-publica/regional_dotplot_trabajo_ingresos_pobreza.png
    alt: "Gráfico 6: Dot plot de brechas regionales en pobreza por ingresos, CASEN 2024. Eje ajustado por panel con referencia nacional."
    title: "Gráfico 6 — Brechas regionales en pobreza: dot plot (eje ajustado por panel, punto vacío = referencia nacional)"
---

En Chile, **La Araucanía registra 13.0% de pobreza extrema; Magallanes, 4.2%**. Son 8.8 puntos porcentuales de diferencia — y si un servicio público de nivel central o local (GOREs/Municipios) diseñan su intervención usando solo el promedio nacional (6.9%), o despreciando las diferencias regionales, podrían equivocarse en asignar recursos o distribuir sus componentes.

Este post documenta un análisis reproducible de CASEN 2024 en [Julia](https://julialang.org), con validación cruzada de cifras oficiales públicas en BIDAT y buena trazabilidad  del flujo en la repo.

**Tres hallazgos para comenzar — estadísticamente robustos:**

- **Pobreza extrema**: La Araucanía 13.0% IC 95 % [11.8%, 14.1%] versus Magallanes 4.2% [3.1%, 5.2%] — brecha de **8.8 pp con CIs no superpuestos**.
- **Cobertura FONASA**: La Araucanía 91.1% [90.2%, 92.0%] versus Metropolitana 75.9% [75.0%, 76.7%] — brecha de **15.2 pp con CIs no superpuestos**.
- **Educación superior completa**: Metropolitana 34.9% [34.0%, 35.7%] versus Maule 20.4% [19.2%, 21.6%] — brecha de **14.5 pp con CIs no superpuestos**.

Los IC son del 95 % y fueron calculados por **Taylor linearization** ([wiki](https://en.wikipedia.org/wiki/Linearization)) para el diseño muestral complejo de CASEN (estratificado bietápico, ponderadores `expr`). Que los CIs no se superpongan implica que estas diferencias regionales son estadísticamente significativas al nivel convencional.

---

## Tolerancia al contraste o cotejo con datos oficiales

Todos los resultados fueron contrastados contra las tablas oficiales disponibles en [BIDAT](https://bidat.gob.cl/url/695ff7271b10e).

{: .table-caption}
**Tabla 1** — Resultados de validación oficial (BIDAT, CASEN 2024)

| Parámetro | Valor |
|-----------|-------|
| Estado validación (nacional + regional, % + expandidos) | **PASA** |
| Tolerancia máxima en puntos porcentuales | 1×10⁻⁵ pp |
| Tolerancia máxima en valores expandidos | 1×10⁻⁶ |
| Diferencia observada (pp) | 2.98×10⁻⁶ pp |
| Diferencia observada (expandido) | 0.0 |
| Filas comparadas nacional | 16 |
| Filas comparadas regional | 256 |

La diferencia máxima observada es inferior a 3 millonésimas de punto porcentual, tolerable 😀. **Los resultados son numéricamente idénticos a los oficiales.**

---

## Cucharada 1: diseño muestral y expansión sin atajos

CASEN 2024 tiene diseño **estratificado bietápico probabilístico** ([nota metodológica BIDAT](https://bidat.gob.cl/url/69b71c77197db)). Para estimaciones a nivel regional, el factor correcto es `expr`; para nivel comunal se requiere `expc` — no son intercambiables. Este análisis usa `expr` y reporta estimaciones por región con IC 95 % calculados por **Taylor linearization** sobre el diseño complejo (estratos, UPM/PSU y pesos/factores).

Población representada en esta ejecución (suma de `expr`): **20.13 millones de personas** (un trabajo pendiente es evaluar el impacto de nuevo Censo 2024 en lugar de proyecciones sobre Censo 2017).

```julia
# Especificación del diseño muestral CASEN 2024
design = (
    weight = :expr,     # factor de expansión regional
    strata = :estrato,  # estrato de muestreo
    psu    = :cod_upm,  # unidad primaria de muestreo (UPM)
    domain = :region,   # dominio de estimación
)
```

Cobertura por dimensión analizada:

{: .table-caption}
**Tabla 2** — Variables CASEN 2024 utilizadas y población objetivo

| Dimensión | Variable CASEN | Población objetivo |
|-----------|----------------|--------------------|
| Educación | `educc`        | Personas ≥ 18 años |
| Salud     | `s13`          | Población total    |
| Pobreza   | `pobreza`      | Población total    |

### Resultados nacionales ponderados

Los porcentajes siguientes corresponden a proporciones ponderadas con `expr`, validadas contra datos oficiales en BIDAT. La diferencia con los valores oficiales es < 3×10⁻⁶ pp.

{: .table-caption}
**Tabla 3** — Distribución nacional ponderada (CASEN 2024, principales categorías)

| Dimensión | Categoría | % nacional |
|-----------|-----------|:----------:|
| Educación | Media Completa | 30.9% |
| Educación | Superior Completa | 29.1% |
| Educación | Superior Incompleta | 12.5% |
| Educación | Media Incompleta | 9.9% |
| Educación | Básica Incompleta | 8.4% |
| Educación | Otros | 7.7% |
| Educación | Sin Educ. Formal | 1.5% |
| Salud | Sistema Público FONASA | 82.6% |
| Salud | Isapre | 13.2% |
| Salud | Ninguno (particular) | 2.0% |
| Salud | FF.AA. y del Orden | 1.8% |
| Salud | No sabe | 0.3% |
| Salud | Otro sistema | 0.2% |
| Pobreza | No pobreza | 82.7% |
| Pobreza | Pobreza no extrema | 10.4% |
| Pobreza | Pobreza extrema | 6.9% |

---

## Cucharada 2: el flujo técnico en Julia

El pipeline corre de punta a punta con `julia --project=. scripts/run_all.jl` (orquestador). Las dos piezas de código más relevantes para reproducir y "auditar" estos resultados son el algoritmo de asignación de celdas y la especificación del diseño muestral (ambos en el repositorio de gitlab/github).

### Taylor linearization: SE e IC del diseño complejo

Se implementó el estimador de Taylor para proporciones en dominios (regiones). La variable linearizada para la proporción $\hat{p}_d$ en dominio $d$ es:

$$z_j = \frac{1(j \in d)\,(1(\text{cat}_j = C) - \hat{p}_d)}{\hat{N}_d}$$

La varianza se estima con la fórmula del diseño estratificado por conglomerados:

```julia
# Varianza Taylor linearization (estratificado, PSU)
# e_{hi} = suma de w_j * z_j por PSU i en estrato h
var_total = sum over strata h:
    (n_h / (n_h - 1)) * sum_i (e_{hi} - mean(e_h))^2

se    = sqrt(var_total)
ci_lo = clamp(p̂ - 1.96 * se, 0.0, 1.0)
ci_hi = clamp(p̂ + 1.96 * se, 0.0, 1.0)
```

Se usan todos los PSU del diseño (incluidos los fuera del dominio, con $z_j = 0$), lo que es correcto para estimación de dominio aleatorio. El SE mediano regional es **1.66 pp** de ancho de IC; el máximo es **5.76 pp** (regiones pequeñas con categorías de baja prevalencia).

> **Próxima entrada, en algún momento 👀 — Jackknife y Bootstrap para CASEN como contraste:** TSL es una aproximación de primer orden óptima para medias y proporciones, pero para estadísticos no lineales (Gini, medianas, razones de cuantiles) puede sub-estimar la varianza. El [repositorio de código](https://github.com/tatanlabra/casen24_julia_viz/blob/main/docs/ic-varianza-casen.md) incluye la teoría y el código Julia en desarrollo para contrastar TSL con Jackknife (delete-1) y Bootstrap — entrada futura de esta serie, no lo he revisado en profundidad.

### Resto Mayor o "Largest remainder": por qué importa en un waffle chart

Un waffle chart de 100 celdas exige que las proporciones sumen exactamente 100 enteros. El redondeo directo introduce errores acumulados que hacen que la suma sea 99 o 101. Este flujo usa el algoritmo de **largest remainder**, que garantiza la suma exacta introduciendo una imprecisión en post de la visualización (tomenlo como una choreza visual solamente):

```julia
"""
Asigna `n_cells` celdas enteras a proporciones `p` usando largest-remainder.
Garantiza que sum(cells) == n_cells exactamente.
"""
function allocate_cells(p::AbstractVector{<:Real}, n_cells::Int = 100)
    raw    = p .* n_cells
    floors = floor.(Int, raw)
    remain = raw .- floors
    deficit = n_cells - sum(floors)
    # Asigna celdas restantes a las proporciones con mayor remainder
    idx = sortperm(remain, rev=true)[1:deficit]
    floors[idx] .+= 1
    return floors
end
```

Validado con tests unitarios: `allocate_cells([0.5, 0.3, 0.2], 100) == [50, 30, 20]`.

### Reproducibilidad

```bash
# Requisitos: Julia 1.10+
git clone <repo>
cd casen2024/julia_viz
julia --project=. -e "using Pkg; Pkg.instantiate()"
julia --project=. scripts/run_all.jl
```

El flujo genera hartos elementos (tablas CSV, gráficos PNG, logs de auditoría de cada insumo). El archivo `Manifest.toml` fija las versiones exactas de todas las dependencias (ocupé Julia 1.10).

---

## Cucharada 3: evidencia visual

### Composición nacional (Gráficos 1–3)

Cada waffle representa 100 celdas asignadas por "largest remainder" sobre las proporciones ponderadas.

{% include gallery id="gallery_nacional" layout="third" caption="**Gráficos 1–3** — Composición nacional: educación (población ≥18 años), salud y pobreza (población total). Fuente: CASEN 2024, elaboración propia en Julia. Los valores están validados contra BIDAT. Clic para ampliar." %}

### Brechas regionales (Gráficos 4–6)

Cada panel usa un **eje ajustado al rango de su propia categoría** (no escala global compartida), lo que permite visualizar diferencias que se aplanan si todas las categorías comparten el mismo eje. Las **barras horizontales** son IC 95 % calculados por Taylor linearization. El punto vacío (○) marca la referencia nacional en cada panel (con su CI).

{% include gallery id="gallery_regional" layout="third" caption="**Gráficos 4–6** — Brechas regionales con IC 95 % (Taylor linearization, diseño complejo): educación, salud y pobreza. Barras = IC 95 %; punto vacío (○) = referencia nacional. Eje ajustado por categoría. Clic para ampliar." %}

### Brechas con IC 95 % — todas estadísticamente robustas

{: .table-caption}
**Tabla 4** — Brechas regionales con IC 95 % por Taylor linearization (CASEN 2024)

| Dimensión | Categoría | Brecha (pp) | Máximo | IC 95 % | Mínimo | IC 95 % |
|-----------|-----------|:-----------:|--------|---------|--------|---------|
| Pobreza | No pobreza | **18.6 pp** | Magallanes 90.0% | [88.5%, 91.5%] | La Araucanía 71.4% | [69.8%, 73.0%] |
| Salud | Isapre | **16.3 pp** | Metropolitana 20.6% | [19.8%, 21.5%] | Maule 4.3% | [3.7%, 5.0%] |
| Salud | FONASA | **15.2 pp** | La Araucanía 91.1% | [90.2%, 92.0%] | Metropolitana 75.9% | [75.0%, 76.7%] |
| Educación | Superior Completa | **14.5 pp** | Metropolitana 34.9% | [34.0%, 35.7%] | Maule 20.4% | [19.2%, 21.6%] |
| Pobreza | Pobreza extrema | **8.8 pp** | La Araucanía 13.0% | [11.8%, 14.1%] | Magallanes 4.2% | [3.1%, 5.2%] |

En todos los casos los IC no se superponen: las brechas son estadísticamente significativas al 5 %. IC calculados por Taylor linearization sobre diseño complejo (estratos, UPM/PSU, `expr`).

---

## Cierre: tres preguntas para quienes usan la encuesta

Si usas CASEN 2024 para caracterización territorial u otros usos donde variables a nivel regional son relevantes, piensalo dos veces antes de usar un dato puntual (sin su intervalo de confianza):

1. **¿Tus resultados están validados contra BIDAT y tienen IC de diseño?** Una diferencia de más de 1×10⁻⁵ pp respecto a las tablas oficiales no es técnica: es de proceso. Y sin IC de diseño complejo, una brecha de 8 pp puede parecer evidencia cuando es ruido en regiones pequeñas.
2. **¿Estás usando el factor de expansión correcto?** `expr` es el apropiado para región; `expc` para comuna. No son intercambiables y usar el incorrecto sesga las estimaciones de cobertura.
3. **¿Tu análisis es reproducible?** Un flujo que no puede ser auditado no puede ser defendido frente a una contraparte técnica ni actualizado cuando salga CASEN 2026.

Los IC aquí incorporados son de diseño complejo (Taylor linearization), no asintóticos simples. Cubren la varianza de muestreo pero no el error de no respuesta ni la subcobertura. Para inferencia causal entre subpoblaciones se requiere diseño adicional.
