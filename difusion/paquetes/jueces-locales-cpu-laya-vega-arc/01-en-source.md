# Source (EN) — A three-judge committee on CPU: when voting improves a decision and when it only paralyzes it

Canonical URL: https://3cucharadas.cl/en/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/
Repository: https://github.com/tatanlabra/penta-agent

## Core summary

Inspired by the JEV Ultrafast architecture (`browser-use/jev-ultrafast`), I built a local 2-of-3 classifier committee (`simil-jev`) on my work laptop CPU (`Lenovo YOGA 730-15IKB`, `Intel Core i7-8550U` at `15 W`, `23.19 GiB` RAM, no discrete GPU) to resolve verification gates (`"Yes"`, `"No"`, `"Undefined"`) without calling a generative LLM.

Combining three open sub-billion-parameter decision engines—**Laya** (`0.4.11`), **VegaML** (`0.11.0` over `Qwen3.5-0.8B`), and **Arc Decide** (`0.4B` ONNX INT8)—exposed both a physical CPU bottleneck and a mathematical voting trap across a `240`-case benchmark (`80` calibration and `160` out-of-sample test cases: `60` `"Yes"`, `60` `"No"`, and `40` `"Undefined"`):

1. **The JEV precursor and the Olympic judges trap (Condorcet 1785; Dietterich 2000):**
   - Under Condorcet's jury theorem, majority voting reduces error only when each judge clears `50%` accuracy (`p > 0.5`) and errors are uncorrelated. In discrete three-class voting, opposite biases do not average out: they deadlock the quorum.
2. **The dual CPU bottleneck:**
   - Spawning three Python and PyTorch subprocesses sequentially on an `i7-8550U` took `~31.7 s` cold (`13.83 s` for Laya at `2.26 GiB`, `13.66 s` for VegaML at `4.93 GiB`, and `4.21 s` for Arc Decide at `0.59 GiB`).
   - Logically, Laya voted `"Yes"` on `125/160` cases (`73` false positives), VegaML voted `"No"` on `131/160` cases (`0/60` on `"Yes"`), and Arc Decide stayed silent on `148/160` cases (`12` `"Yes"` votes and `0` `"No"` votes).
3. **The `66.67%` selective accuracy paradox:**
   - When the 2-of-3 panel reached agreement, it hit `10` out of `15` (`66.67%` selective accuracy, after overfitting `14/14` on calibration), yet it only decided on `9.38%` of the test bank (`90.62%` abstention) and scored `0/60` on the `"No"` class. Its `28.75%` overall three-class accuracy (`46/160`, of which `36` were abstentions) barely beat a `0 ms` script that always answers `"Undefined"` (`25.00%`).
4. **The viable open alternative on CPU — `DeBERTa-v3-small-mnli-fever-anli` (ONNX INT8):**
   - Framing gate verification as three-class Natural Language Inference (NLI: `entailment`, `contradiction`, `neutral`) with `MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli` (`44M` backbone parameters, `142M` total, trained on `763,913` NLI pairs, `88.0%` on MNLI-m) compiled to dynamic `INT8` in `onnxruntime` resolves verdicts in `5` to `15 ms` using `~140 MiB` of RAM (`60` times lighter than the `8.36 GiB` footprint of the three judges).
