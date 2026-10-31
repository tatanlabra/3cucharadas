TÍTULO PROVISIONAL:
I benchmarked a 2-of-3 committee of sub-1B local classifiers (Laya, VegaML, Arc Decide) on a laptop CPU (i7-8550U): why opposite priors caused 90.62% deadlock (0/60 on "No") and why DeBERTa-v3-small in ONNX INT8 solved it in 5 to 15 ms

URL PROPUESTA:
https://3cucharadas.cl/en/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/

PRIMER COMENTARIO PROPUESTO:
Inspired by JEV Ultrafast (`7.1 s` browser tasks by separating atomic System 1 decisions from LLM text generation), I tested whether a 2-of-3 committee of open sub-billion-parameter classifiers (`simil-jev`) could resolve 3-class verification gates (`"Yes"`, `"No"`, `"Undefined"`) on my laptop CPU (`Lenovo YOGA 730-15IKB`, `Intel Core i7-8550U` at `15 W`, `23.19 GiB` RAM, no dGPU).

Key results across `240` cases (`80` calibration and `160` out-of-sample test cases: `60` `"Yes"`, `60` `"No"`, `40` `"Undefined"`):
- **The three judges standalone:** Laya `0.4.11` (`2.26 GiB`, `13.83 s` cold, `366 ms` p95) voted `"Yes"` on `125/160` cases (`73` FP, `41.25%` 3-class accuracy). VegaML `0.11.0` (`4.93 GiB`, `13.66 s` cold, `1,717 ms` p95, `14.3M` physics head over `Qwen3.5-0.8B`) voted `"No"` on `131/160` cases (`0/60` on `"Yes"`, `38.13%` 3-class accuracy). Arc Decide `0.4B` (`0.59 GiB`, `4.21 s` cold, `950 ms` p95) abstained under its `0.66` panel threshold on `148/160` cases (`12` `"Yes"` votes, `0` `"No"` votes; `42.50%` standalone 3-class accuracy).
- **Why the 2-of-3 panel collapsed:** Laya and VegaML clashed on `101/160` cases while Arc stayed silent, so the committee only decided on `15` cases (`9.38%` coverage, `10/15` = `66.67%` selective accuracy after overfitting `14/14` on calibration) and scored `0/60` on `"No"` (`28.75%` 3-class accuracy, where `36` of `46` hits were abstentions, vs `25.00%` for a `0 ms` `"Always Undefined"` baseline).
- **The viable CPU alternative:** Framing the gate as 3-class NLI (`entailment`, `contradiction`, `neutral`) with `MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli` (`44M` backbone parameters, `142M` total, fine-tuned on `763,913` NLI pairs, `88.0%` on MNLI-m) compiled to dynamic `INT8` in `onnxruntime` runs in `5` to `15 ms` per verdict using `~140 MiB` of RAM (`60` times lighter than the `8.36 GiB` trio).

Code repository: https://github.com/tatanlabra/penta-agent
