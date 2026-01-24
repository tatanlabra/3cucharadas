---
layout: single
title: "RNA-seq con R: guía práctica con fórmulas, ligaduras y código reproducible"
subtitle: "Flujo completo: conteos, normalización, NB-GLM, voom y control de FDR en Bioconductor"
date: 2025-11-08
categories: [r, bioinformatics, biology]
tags: [rna-seq, deseq2, edger, limma, reproducibilidad, math]
toc: true
toc_sticky: true
comments: true
author_profile: true
math: true
---

# RNA-seq con R: guía práctica con fórmulas, ligaduras y código reproducible

> **Objetivo.** Documentar un flujo de trabajo de RNA-seq de extremo a extremo en R/Bioconductor con énfasis en diseño, normalización, modelado NB-GLM, *voom*, control del error tipo I (FDR) y reducción de sesgos por *batch*. Incluye tipografía con flechas y símbolos: →, ⇄, ⇒, ∝, ≤, ≥, ±, ≈, ⟂.  
> **Nota de formato:** en este post las fórmulas usan **solo** bloques `$$ … $$`.

---

## 1. Diseño experimental y potencia

### 1.1 Variables clave
- Factores biológicos: condición (tratamiento vs control), tiempo, sexo, tejido.
- Factores técnicos: lote (*batch*), librería, *lane*, *kit*, laboratorio.
- Réplicas: preferir **n ≥ 3** por grupo; priorizar réplicas sobre mayor profundidad cuando el objetivo es DE.

### 1.2 Profundidad y longitud de lectura
- Regla práctica a nivel de **gen**: ~15–30 M lecturas SE por muestra; más réplicas suele superar el beneficio de más profundidad para DE.

### 1.3 Poder estadístico aproximado
Definiciones:
$$
g \text{ = gen},\quad \sigma_g^2 \text{ = varianza en log-CPM},\quad \Delta_g=\log_2(\mathrm{FC}).
$$

Aproximación de Wald a dos colas:
$$
\text{Poder} \approx \Pr\!\left(\left|\frac{\Delta_g}{\sqrt{\frac{\sigma_g^2}{n_1}+\frac{\sigma_g^2}{n_2}}}\right| > z_{1-\alpha/2}\right).
$$

---

## 2. Flujo de trabajo general

**QC → alineación/cuantiﬁcación → conteo → normalización → modelado → interpretación.**

1) **QC** con FastQC y *dashboard* con MultiQC.  
2) **Alineación** por genoma (STAR) **o** **cuantificación** por transcriptoma (Salmon).  
3) **Conteo** por *featureCounts* (genes/exones).  
4) **Normalización**: factores de tamaño (DESeq2, RLE), TMM (edgeR), *voom* (limma).  
5) **Modelado**: NB-GLM (DESeq2/edgeR) o LM con pesos (*voom* + limma).  
6) **Múltiples pruebas**: Benjamini–Hochberg (FDR).  
7) **Batch**: ComBat / SVA cuando aplique.

---

## 3. QC previo

### 3.1 FastQC → MultiQC
- Módulos clave: calidad por base, contenido GC, *adapter content*, *overrepresented seqs*, *duplication levels*, *k-mer content*. Consolidar con *MultiQC*.

---

## 4. Alineación vs cuantificación “ligera”

### 4.1 STAR (alineación al genoma)
- Rápido y sensible; detecta *splicing* canónico y quimérico.

### 4.2 Salmon (cuantificación por transcriptoma)
- *Quasi-mapping* sesgo-consciente; integra estimación de incertidumbre.

### 4.3 Elección práctica
- **Genes** y diseños con intrones → STAR + featureCounts.  
- **Transcritos/isoformas** o *pilot* rápido → Salmon + tximport.

---

## 5. Conteo por gen
$$
\mathrm{counts}_{g,i} \;=\; \sum_{r \in \mathcal{R}_i} \mathbf{1}\!\left[r \hookrightarrow g\right],
$$
donde \(\mathcal{R}_i\) son lecturas de la muestra \(i\). Implementación eficiente: *featureCounts*.

---

## 6. Unidades de expresión

### 6.1 CPM, RPKM/FPKM, TPM
$$
\mathrm{CPM}_{g,i} = \frac{10^6 \, C_{g,i}}{\sum_h C_{h,i}},\qquad
\mathrm{RPKM}_{g,i} = \frac{10^9 \, C_{g,i}}{L_g \sum_h C_{h,i}},
$$
$$
\mathrm{TPM}_{g,i} = \frac{\frac{C_{g,i}}{L_g}}{\sum_h \frac{C_{h,i}}{L_h}} \times 10^6.
$$

Para DE con NB-GLM, usar **cuentas crudas** + factores de tamaño; TPM/FPKM útiles para comparaciones **intra-muestra**.

---

## 7. Normalización

### 7.1 DESeq2 (median-ratio / RLE)
Definiciones y factor de tamaño:
$$
\tilde{K}_{g,i}=\frac{K_{g,i}}{\operatorname{geom}\big(\{K_{g,\cdot}\}\big)},\qquad
s_i=\operatorname{mediana}_{g \in G}\ \tilde{K}_{g,i}.
$$

### 7.2 edgeR (TMM)
$$
\log_2 \mathrm{FC}_{g}^{(i,\mathrm{ref})}=\log_2\!\frac{K_{g,i}/N_i}{K_{g,\mathrm{ref}}/N_{\mathrm{ref}}},\qquad
\mathrm{TMM}_i=\operatorname{trimmed\_mean}\!\big(\log_2 \mathrm{FC}_{g}^{(i,\mathrm{ref})}\big).
$$

### 7.3 *voom* (limma)
$$
w_{g,i}=\frac{1}{\widehat{\sigma}^2\!\big(\log_2(\mathrm{CPM}_{g,i})\big)}.
$$

---

## 8. Modelo estadístico

### 8.1 NB-GLM (DESeq2/edgeR)
$$
K_{g,i}\sim \mathrm{NB}(\mu_{g,i},\alpha_g),\qquad
\log \mu_{g,i}=\log s_i+\mathbf{x}_i^{\top}\boldsymbol{\beta}_g.
$$

### 8.2 Reducción de sesgo en log-FC
Aplicar *shrinkage* de log-FC con **apeglm** o **ashr** cuando la información es baja.

### 8.3 Corrección por múltiples pruebas
BH a FDR \(q\):
$$
p_{(k)} \le \frac{k}{m}\,q \;\Rightarrow\; \text{rechazar } H_{(1)},\dots,H_{(k)}.
$$

---

## 9. Efectos de *batch* y covariables
- Incluir lote en el diseño: `~ batch + condition`.  
- Si *batch* desequilibrado, considerar **ComBat**.  
- Si *batch* latente, estimar con **SVA**.

---

## 10. Integración a nivel de transcrito
$$
\widehat{K}^{\mathrm{gene}} \;=\; \sum_{t \in g} \mathrm{length\text{-}scaled\ counts}_t.
$$
Importar con **tximport** para inferencia a nivel de gen y menor sesgo por longitud.

---

## 11. Pipeline en R: reproducible y ejecutable

> **Requisitos**: R ≥ 4.3, Bioconductor ≥ 3.18. Directorio con `counts.tsv` (genes × muestras), `coldata.csv` (muestras × metadatos) y, opcionalmente, `tx2gene.csv` si se usa *tximport*.

```r
# RNA-seq end-to-end con DESeq2, edgeR/voom y control de calidad
# Instalación (una sola vez):
if (!requireNamespace("BiocManager", quietly = TRUE)) install.packages("BiocManager")
BiocManager::install(c(
  "DESeq2","edgeR","limma","apeglm","ashr","tximport","tximportData",
  "SummarizedExperiment","IHW","sva","Rsubread","AnnotationDbi"
), ask = FALSE, update = TRUE)

suppressPackageStartupMessages({
  library(DESeq2); library(edgeR); library(limma)
  library(apeglm); library(ashr); library(tximport)
  library(SummarizedExperiment); library(sva)
})

set.seed(1234)  # reproducibilidad

# 1) Entrada
counts   <- read.table("counts.tsv", header = TRUE, row.names = 1, sep = "\t", check.names = FALSE)
coldata  <- read.csv("coldata.csv", row.names = 1)
stopifnot(all(colnames(counts) == rownames(coldata)))

# 2) Filtros mínimos
keep <- rowSums(counts >= 10) >= 3
counts <- counts[keep, ]

# 3) DESeq2 NB-GLM
dds <- DESeqDataSetFromMatrix(countData = counts, colData = coldata, design = ~ batch + condition)
dds <- DESeq(dds, minReplicatesForReplace = 7)
# Transformaciones para QC
vsd <- vst(dds, blind = TRUE)
rld <- rlog(dds, blind = TRUE)

# 4) Contraste principal
res <- results(dds, contrast = c("condition","treated","control"), alpha = 0.05, independentFiltering = TRUE)
# Shrinkage de LFC
res_shr <- lfcShrink(dds, coef = "condition_treated_vs_control", type = "apeglm")
res_tbl <- as.data.frame(res_shr[order(res_shr$padj), ])
write.csv(res_tbl, "DE_deseq2_apeglm.csv", row.names = TRUE)

# 5) BH-FDR y umbrales
sig <- subset(res_tbl, padj < 0.05 & abs(log2FoldChange) >= 1)
write.csv(sig, "DE_sig_LFC1_FDR5.csv", row.names = TRUE)

# 6) Alternativa: limma-voom
dge <- DGEList(counts = counts)
dge <- calcNormFactors(dge, method = "TMM")
design <- model.matrix(~ batch + condition, data = coldata)
v <- voom(dge, design = design, plot = FALSE)
fit <- lmFit(v, design); fit <- eBayes(fit, trend = TRUE)
voom_res <- topTable(fit, coef = "conditiontreated", n = Inf, adjust.method = "BH")
write.csv(voom_res, "DE_voom.csv")

# 7) Batch opcional con ComBat (sobre expresión log)
expr <- assay(vsd)
combat_expr <- ComBat(dat = expr, batch = coldata$batch, mod = model.matrix(~ condition, coldata))
# PCA rápido post-batch
pca <- prcomp(t(combat_expr))
write.csv(pca$x[,1:3], "PCA_post_ComBat.csv")

# 8) Resumen rápido
cat(sprintf("Genes evaluados: %d\nDESeq2 FDR<0.05: %d\nvoom FDR<0.05: %d\n",
            nrow(res_tbl), sum(res_tbl$padj < 0.05, na.rm=TRUE),
            sum(voom_res$adj.P.Val < 0.05, na.rm=TRUE)))
```
