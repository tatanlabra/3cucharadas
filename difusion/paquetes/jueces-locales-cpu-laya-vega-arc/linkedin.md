# LinkedIn — ES nativo + variante EN

## Cuerpo principal (ES)

Cuando automatizo auditorías de código y contratos de datos, muchas compuertas intermedias no necesitan generar prosa: necesitan decidir rápido entre "Sí" (la evidencia alcanza), "No" (hay un fallo duro) o "Indefinido" (conviene abstenerse y escalar). Inspirado en la arquitectura de JEV Ultrafast, armé en mi portátil (Lenovo YOGA 730-15IKB con un Intel Core i7-8550U de 15 W y 23,19 GiB de RAM sin GPU dedicada) un comité "2-de-3" con tres motores abiertos pequeños: Laya (0.4.11), VegaML (0.11.0 sobre Qwen3.5-0.8B) y Arc Decide (0.4B en ONNX INT8).

Sobre un banco de 240 casos (80 de calibración y 160 de prueba fuera de muestra: 60 "Sí", 60 "No" y 40 "Indefinidos"), el resultado dejó una lección empírica difícil de ignorar:

- **La trampa de los "jueces olímpicos" en voto discreto (Condorcet 1785; Dietterich 2000):** cuando dos modelos tienen sesgos opuestos, la mayoría simple no los corrige, los bloquea. Laya votó "Sí" en 125 de 160 casos (con 73 falsos positivos), VegaML votó "No" en 131 de 160 (0 aciertos de 60 en "Sí") y Arc Decide calló en 148 de 160 casos (0 votos "No").
- **La ilusión del 66,67 %:** cuando el comité logró acuerdo acertó 10 de 15 casos (66,67 %), pero solo decidió en el 9,38 % del banco (90,62 % de parálisis), acertó 0 de 60 en la clase "No" y tardó ~31,7 s en frío al levantar procesos en serie. Su exactitud global de tres clases (28,75 %, con 36 de 46 aciertos por abstención) apenas superó el 25,00 % de un script vacío que responde siempre "Indefinido" en 0 ms.
- **Qué propongo medir ahora (hipótesis, no resultado):** una compuerta que pregunta si la evidencia respalda, contradice o no alcanza frente a una regla es, formalmente, inferencia de lenguaje natural (NLI de 3 clases: entailment, contradiction y neutral). El candidato es un único cross-encoder bidireccional abierto, `cross-encoder/nli-deberta-v3-small` (DeBERTaV3 ajustado sobre SNLI y MultiNLI, con una versión ONNX INT8 para CPU en su repositorio). Todavía no lo corrí en este banco: su latencia, su memoria y, sobre todo, si logra decir "No" donde el comité marcó 0 de 60, están por medir.

Artículo completo con las papeletas de votación, diagramas de arquitectura, mi consola con `ffpoke` y referencias en:
https://3cucharadas.cl/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/?utm_source=linkedin&utm_medium=social&utm_campaign=jueces_locales_cpu

---

## English variant (LinkedIn EN)

When automating code audits and data contracts, many intermediate verification gates do not need generated prose: they need a fast verdict between "Yes", "No", or "Undefined". Inspired by JEV Ultrafast, I tested a local 2-of-3 classifier committee on my laptop CPU (Lenovo YOGA 730-15IKB, Intel Core i7-8550U at 15 W, 23.19 GiB RAM, no discrete GPU) combining Laya (0.4.11), VegaML (0.11.0 on Qwen3.5-0.8B), and Arc Decide (0.4B ONNX INT8).

Across 240 cases (80 calibration and 160 out-of-sample test cases), the benchmark exposed both a physical bottleneck and a voting trap:

- **Opposite biases deadlock a discrete quorum (Condorcet 1785; Dietterich 2000):** Laya voted "Yes" on 125/160 cases (73 false positives), VegaML voted "No" on 131/160 (0/60 on "Yes"), and Arc Decide abstained on 148/160 (0 "No" votes).
- **The 66.67% selective accuracy paradox:** when the 2-of-3 panel agreed it hit 10 out of 15 (66.67%), yet it only decided on 9.38% of cases, hit 0/60 on "No", and took ~31.7 s cold on CPU. Its 28.75% 3-class accuracy (46/160, 36 of them abstentions) barely beat a 0 ms script that always returns "Undefined" (25.00%).
- **What I propose to measure next (a hypothesis, not a result):** framing the gate as 3-class Natural Language Inference (NLI), the candidate is a single open cross-encoder, `cross-encoder/nli-deberta-v3-small` (DeBERTaV3 fine-tuned on SNLI and MultiNLI, with an ONNX INT8 build for CPUs in its repository). I have not run it on this bank yet: its latency, its memory use, and above all whether it can say "No" where the committee scored 0/60 are still to be measured.

Full article and hardware breakdown:
https://3cucharadas.cl/en/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/?utm_source=linkedin&utm_medium=social&utm_campaign=jueces_locales_cpu
