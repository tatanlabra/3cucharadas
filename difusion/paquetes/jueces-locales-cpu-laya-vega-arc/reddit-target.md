TÍTULO PROVISIONAL:
I benchmarked a 2-of-3 committee of sub-1B local classifiers (Laya, VegaML, Arc Decide) on a laptop CPU (i7-8550U): why opposite priors caused 90.62% deadlock (0/60 on "No"), and the NLI cross-encoder I plan to test next

URL PROPUESTA:
https://3cucharadas.cl/en/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/

PRIMER COMENTARIO PROPUESTO:
Inspired by JEV Ultrafast (`7.1 s` browser tasks by separating atomic System 1 decisions from LLM text generation), I tested whether a 2-of-3 committee of open sub-billion-parameter classifiers (`simil-jev`) could resolve 3-class verification gates (`"Yes"`, `"No"`, `"Undefined"`) on my laptop CPU (`Lenovo YOGA 730-15IKB`, `Intel Core i7-8550U` at `15 W`, `23.19 GiB` RAM, no dGPU).

Key results across `240` cases (`80` calibration and `160` out-of-sample test cases: `60` `"Yes"`, `60` `"No"`, `40` `"Undefined"`):
- **The three judges standalone:** Laya `0.4.11` (`2.26 GiB`, `13.83 s` cold, `366 ms` p95) voted `"Yes"` on `125/160` cases (`73` FP, `41.25%` 3-class accuracy). VegaML `0.11.0` (`4.93 GiB`, `13.66 s` cold, `1,717 ms` p95, `14.3M` physics head over `Qwen3.5-0.8B`) voted `"No"` on `131/160` cases (`0/60` on `"Yes"`, `38.13%` 3-class accuracy). Arc Decide `0.4B` (`0.59 GiB`, `4.21 s` cold, `950 ms` p95) abstained under its `0.66` panel threshold on `148/160` cases (`12` `"Yes"` votes, `0` `"No"` votes; `42.50%` standalone 3-class accuracy).
- **Why the 2-of-3 panel collapsed:** Laya and VegaML clashed on `101/160` cases while Arc stayed silent, so the committee only decided on `15` cases (`9.38%` coverage, `10/15` = `66.67%` selective accuracy, Wilson 95% CI `41.7%` to `84.8%`, after overfitting `14/14` on calibration) and scored `0/60` on `"No"` (`28.75%` 3-class accuracy, where `36` of `46` hits were abstentions, vs `25.00%` for a `0 ms` `"Always Undefined"` baseline).
- **What I plan to test next (not measured):** Framing the gate as 3-class NLI (`entailment`, `contradiction`, `neutral`), the candidate is `cross-encoder/nli-deberta-v3-small` (DeBERTaV3, `44M` backbone parameters, `142M` total, fine-tuned on SNLI + MultiNLI; its repository ships an ONNX INT8 build for `AVX2` CPUs). I have not run it on this bank, so I have no latency, RAM, or accuracy numbers for it yet; whether it fixes the missing `"No"` votes is the open question. Suggestions for a fair comparison against the trio (~7.8 GiB of RAM combined) are welcome.

Code repository: https://github.com/tatanlabra/penta-agent

RECORDATORIO DE CONDUCTA:
- Destino previsto: r/LocalLLaMA. Antes de enviar, revisar en una sesión humana las reglas de autopromoción y los flairs del sub; si no admite enlaces propios, descartar el canal.
- Si preguntan por la alternativa NLI: no está medida en este banco; no citar latencia, RAM ni exactitud propias para ella.
- No solicitar votos ni publicar otra pieza propia en Reddit el mismo día.
