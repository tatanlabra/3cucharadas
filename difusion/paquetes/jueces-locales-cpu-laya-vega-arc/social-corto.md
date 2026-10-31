# Copias para redes cortas (Mastodon y Bluesky)

El texto base exacto (raíz ES y respuesta EN) está registrado en `social.json` para ser consumido por el pipeline de `cucharadas-difusion` una vez que exista aprobación humana posterior al despliegue.

## Raíz ES (279 caracteres sin URL; Mastodon añade la URL con UTM al final, Bluesky usa tarjeta OG)
Probé en mi i7-8550U un comité 2-de-3 de clasificadores locales (Laya, VegaML y Arc Decide) para filtrar compuertas sin llamar a un LLM: acertó 10/15 al decidir (66,67 %), pero calló en el 90,62 % y acertó 0/60 en "No". Con DeBERTa-v3-small ONNX INT8 baja a 5-15 ms y 140 MiB. #IA

## Respuesta EN (278 caracteres)
I tested a 2-of-3 committee of local classifiers (Laya, VegaML, Arc Decide) on my i7-8550U CPU to filter gates without an LLM: it hit 10/15 when deciding (66.67%), yet abstained on 90.62% and hit 0/60 on "No". Switching to DeBERTa-v3-small ONNX INT8 takes 5-15 ms in 140 MiB. #AI
