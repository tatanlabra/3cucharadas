---
layout: single
title: "Código reproducible"
subtitle: "Flujo minimo"
date: 2025-08-11
categories: [informatics]
tags: [math]
toc: true
toc_sticky: true
comments: true
author_profile: true
math: true
---

R con R cigaRRO

## MathJax para matemáticas

Inline: $a^2+b^2=c^2$ y también $e^{i\pi}+1=0$.

Bloque:
$$
\int_{-\infty}^{\infty} e^{-x^2}\,dx=\sqrt{\pi}
$$

Bloque con $$...$$:
$$
\Pr\!\left(\left|\frac{\hat\beta}{\mathrm{SE}(\hat\beta)}\right| > z_{1-\alpha/2}\right)
$$


<!-- === PRUEBA DE NERD FONT E ÍCONOS ESPECIALES === -->

## Prueba Nerd Font (PUA)
<!-- Powerline: U+E0A0..E0B3 -->
**Powerline:** <span class="nf">      </span>

<!-- Devicons: U+E700..E7FF -->
**Devicons:** <span class="nf">    </span>

<!-- Seti UI: U+E600..E6FF -->
**Seti/UI:** <span class="nf">    </span>

<!-- Font Awesome PUA: U+F000.. -->
**Font Awesome:** <span class="nf">     </span>

<!-- Material Design Icons (algunas asignaciones extendidas) -->
**Material (MDI):** <span class="nf">󰀂 󰀘 󰙯 󰊤 󰇚</span>

---

## Prueba Unicode comunes (fallback del sistema)
**Flechas:** ← ↑ → ↓ ↔ ↕ ⇐ ⇒ ⇑ ⇓ ↩ ↪  
**Dibujo de cajas:** ─ ━ │ ┃ ┌ ┐ └ ┘ ├ ┤ ┬ ┴ ┼ ╔ ╗ ╚ ╝ ╠ ╣ ╦ ╩ ╬  
**Bloques:** ░ ▒ ▓ █ ▀ ▄ ▌ ▐  
**Moneda:** € £ ¥ ₩ ₿ ₹  
**Braille:** ⠁ ⠃ ⠉ ⠓ ⠟ ⠿  
**Matemática:** ∑ ∏ √ ∞ ≈ ≠ ≤ ≥ ∂ ∇ ∫  
**Emoji (color del sistema):** 😀 👍 🔥 🗂️ 🧭


## Bloque de Python

```python
import pandas as pd

def hello_world(name):
    """Saluda al usuario."""
    print(f"Hola, {name}!")
hello_world("Mundo")
```
## Bloque de Julia

```julia
using DataFrames

# Definir una función
function fibonacci(n)
    a, b = 0, 1
    for i = 1:n
        a, b = b, a + b
    end
    return a
end

println("El décimo número de Fibonacci es: ", fibonacci(10))
```

## Bloque de R

```r
# RNA-seq end-to-end con DESeq2, edgeR/voom y control de calidad
# Instalación (una sola vez):
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install(c(
  "DESeq2","edgeR","limma","apeglm","ashr","tximport","tximportData",
  "SummarizedExperiment","IHW","sva","Rsubread","AnnotationDbi"
), ask = FALSE, update = TRUE)
```

## Bloque de Bash

```bash
# Actualizar el sistema
sudo apt update && sudo apt upgrade -y

# Instalar un paquete
pip install numpy

# Listar archivos
ls -la
```

## Bloque de Stata

```stata
* Cargar datos de ejemplo
sysuse auto, clear

* Describir los datos
describe

* Generar un resumen estadístico
summarize mpg weight

* Correr una regresión lineal simple
regress mpg weight
```