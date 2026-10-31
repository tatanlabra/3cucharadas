# LinkedIn — ES nativo + variante EN

## Cuerpo principal (ES)

Cuando automatizo auditorías de código y contratos de datos, muchas compuertas intermedias no necesitan generar prosa: necesitan decidir rápido entre "Sí" (la evidencia alcanza), "No" (hay un fallo duro) o "Indefinido" (conviene abstenerse y escalar). Inspirado en la arquitectura de JEV Ultrafast, armé en mi portátil (Lenovo YOGA 730-15IKB con un Intel Core i7-8550U de 15 W y 23,19 GiB de RAM sin GPU dedicada) un comité "2-de-3" con tres motores abiertos pequeños: Laya (0.4.11), VegaML (0.11.0 sobre Qwen3.5-0.8B) y Arc Decide (0.4B en ONNX INT8).

Sobre un banco de 240 casos (80 de calibración y 160 de prueba fuera de muestra: 60 "Sí", 60 "No" y 40 "Indefinidos"), el resultado dejó una lección empírica difícil de ignorar:

- **La trampa de los "jueces olímpicos" en voto discreto (Condorcet 1785; Dietterich 2000):** cuando dos modelos tienen sesgos opuestos, la mayoría simple no los corrige, los bloquea. Laya votó "Sí" en 125 de 160 casos (con 73 falsos positivos), VegaML votó "No" en 131 de 160 (0 aciertos de 60 en "Sí") y Arc Decide calló en 148 de 160 casos (0 votos "No").
- **La ilusión del 66,67 %:** cuando el comité logró acuerdo acertó 10 de 15 casos (66,67 %), pero solo decidió en el 9,38 % del banco (90,62 % de parálisis), acertó 0 de 60 en la clase "No" y tardó ~31,7 s en frío al levantar procesos en serie. Su exactitud global de tres clases (28,75 %, con 36 de 46 aciertos por abstención) apenas superó el 25,00 % de un script vacío que responde siempre "Indefinido" en 0 ms.
- **Qué modelo libre sí funciona en CPU:** al reformular la compuerta como inferencia de lenguaje natural (NLI de 3 clases: entailment, contradiction y neutral), un único cross-encoder bidireccional —`MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli`, entrenado sobre 763.913 pares NLI y compilado a ONNX INT8— resuelve cada veredicto en 5 a 15 ms sobre el mismo i7-8550U ocupando ~140 MiB de RAM (casi 60 veces menos que los 8,36 GiB del comité).

Artículo completo con las papeletas de votación, diagramas de arquitectura, mi consola con `ffpoke` y referencias en:
https://3cucharadas.cl/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/?utm_source=linkedin&utm_medium=social&utm_campaign=jueces_locales_cpu

---

## English variant (LinkedIn EN)

When automating code audits and data contracts, many intermediate verification gates do not need generated prose: they need a fast verdict between "Yes", "No", or "Undefined". Inspired by JEV Ultrafast, I tested a local 2-of-3 classifier committee on my laptop CPU (Lenovo YOGA 730-15IKB, Intel Core i7-8550U at 15 W, 23.19 GiB RAM, no discrete GPU) combining Laya (0.4.11), VegaML (0.11.0 on Qwen3.5-0.8B), and Arc Decide (0.4B ONNX INT8).

Across 240 cases (80 calibration and 160 out-of-sample test cases), the benchmark exposed both a physical bottleneck and a voting trap:

- **Opposite biases deadlock a discrete quorum (Condorcet 1785; Dietterich 2000):** Laya voted "Yes" on 125/160 cases (73 false positives), VegaML voted "No" on 131/160 (0/60 on "Yes"), and Arc Decide abstained on 148/160 (0 "No" votes).
- **The 66.67% selective accuracy paradox:** when the 2-of-3 panel agreed it hit 10 out of 15 (66.67%), yet it only decided on 9.38% of cases, hit 0/60 on "No", and took ~31.7 s cold on CPU. Its 28.75% 3-class accuracy (46/160, 36 of them abstentions) barely beat a 0 ms script that always returns "Undefined" (25.00%).
- **What actually works on a laptop CPU:** framing the gate as 3-class Natural Language Inference (NLI) with `MoritzLaurer/DeBERTa-v3-small-mnli-fever-anli` (fine-tuned on 763,913 NLI pairs and compiled to ONNX INT8) resolves verdicts in 5 to 15 ms using ~140 MiB of RAM (nearly 60x lighter than the 8.36 GiB footprint of the three judges).

Full article and hardware breakdown:
https://3cucharadas.cl/en/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/?utm_source=linkedin&utm_medium=social&utm_campaign=jueces_locales_cpu
