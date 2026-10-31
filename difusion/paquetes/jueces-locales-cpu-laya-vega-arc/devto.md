---
title: "A three-judge committee on CPU: when voting improves a decision and when it only paralyzes it"
published: false
description: "Why a 2-of-3 local classifier committee (Laya, VegaML, Arc Decide) deadlocked on 90.62% of gates on an Intel i7-8550U, and how DeBERTa-v3-small in ONNX INT8 solves them in 5 to 15 ms."
tags: ai, machinelearning, onnx, linux
canonical_url: https://3cucharadas.cl/en/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/
---

When automating code workflows and technical auditing, many intermediate gates do not need generated prose: they need a fast verdict between **"Yes"** (evidence suffices), **"No"** (hard failure), or **"Undefined"** (abstain and escalate). Inspired by [JEV Ultrafast](https://github.com/browser-use/jev-ultrafast) (`7.1 s` end-to-end browser actions by separating atomic System 1 decisions from text generation), I built a local 2-of-3 committee (`simil-jev`) on my laptop CPU (`Lenovo YOGA 730-15IKB`, `Intel Core i7-8550U` at `15 W`, `23.19 GiB` RAM, no dGPU).

## 1. The three judges on the bench (`160` out-of-sample test cases)

I wired three open sub-billion-parameter engines behind `simil-jev --panel` and evaluated them on `240` cases (`80` calibration and `160` test cases: `60` `"Yes"`, `60` `"No"`, and `40` `"Undefined"`):

- **Laya `0.4.11` (The approver):** `2.26 GiB` RAM, `13.83 s` cold, `366 ms` p95. Voted `"Yes"` on `125/160` cases (including `48` of the `60` negatives → `73` false positives), achieving `41.41%` selective accuracy (`80.00%` coverage) and `41.25%` 3-class accuracy (`66/160`).
- **VegaML `0.11.0` on `Qwen3.5-0.8B` (The rejecter):** `4.93 GiB` RAM, `13.66 s` cold, `1,717 ms` p95 (`14.3M` physics head). Voted `"No"` on `131/160` cases (`0/60` on `"Yes"`, `51/60` on `"No"`), achieving `40.80%` selective accuracy (`78.13%` coverage) and `38.13%` 3-class accuracy (`61/160`).
- **Arc Decide `0.4B` ONNX INT8 (The silent one):** `0.59 GiB` RAM, `4.21 s` cold, `950 ms` p95. Under its panel threshold (`0.66`), it stayed silent on `148/160` cases and voted only `12` times (all `"Yes"`, `0` `"No"` votes). Standalone, it reached `47.42%` selective accuracy (`60.63%` coverage) and `42.50%` 3-class accuracy (`68/160`).

## 2. Why the 2-of-3 committee collapsed on CPU

1. **Zero recall on `"No"` (`0/60`):** VegaML voted `"No"` `53` times on the `60` negative cases, but Laya voted `"No"` only `1` time and Arc `0` times. No negative test case ever gathered two `"No"` ballots.
2. **The `66.67%` selective accuracy illusion:** Laya and VegaML clashed on `101/160` cases while Arc abstained on `148`. The panel decided on only `15` cases (`9.38%` coverage), hitting `10/15` (`66.67%`, Wilson 95% CI `41.7%` to `84.8%`) after overfitting `14/14` on calibration. Its `28.75%` 3-class accuracy (`46/160`, `36` of them abstentions) barely beat a `0 ms` script that always answers `"Undefined"` (`25.00%`, `40/160`), while costing `~31.7 s` cold in serial subprocesses.

## 3. What actually runs in `5` to `15 ms` on an `i7-8550U`: `DeBERTa-v3-small` in ONNX INT8

Gate verification against a rule is three-class Natural Language Inference (NLI: `entailment`, `contradiction`, `neutral`). Switching to [`MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli`](https://huggingface.co/MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli) (`44M` backbone parameters, `142M` total, fine-tuned on `763,913` NLI pairs, `88.0%` on MNLI-m) compiled to dynamic `INT8` in `onnxruntime` resolves each gate in **`5` to `15 ms`** on the same `AVX2` laptop CPU using **`~140 MiB`** of RAM (`60` times lighter than the `8.36 GiB` footprint of the three judges).

Read the full interactive article (with voting ballots, D2 pipeline diagrams, and the `kitty` + `ffpoke` hardware profile) at the canonical URL:
https://3cucharadas.cl/en/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/
