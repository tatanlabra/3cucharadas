## Versión en español (principal)

Probé si darle Nushell a un agente mejoraba realmente su trabajo. El resultado no fue “sí” ni “no”.

En 380 ejecuciones apareció una frontera bastante más útil:

El corpus afinado mejoró de 23/30 a 30/30 aciertos, pero la mediana de tiempo subió de 6,2 a 9,5 segundos y la salida de 152 a 368 tokens.

En el holdout, la mejora fue de 10/15 a 14/15, aunque Nushell solo se activó 4/15 veces. Y en un caso agregado basado en la recreación de mi tesis, ambos brazos acertaron todo: cambiar la ruta no cambió el resultado.

Mi regla quedó más estrecha que al empezar: Nushell merece una prueba cuando hay datos estructurados, varias transformaciones y un riesgo concreto de error silencioso. Para lo demás suele existir una herramienta más simple.

El post incluye el visor en R, los límites del experimento y el paquete reproducible. Me interesa comparar otras estrategias: ¿qué problema resolvieron, contra qué línea base y cómo comprobaron la mejora?

Método, datos y código: https://3cucharadas.cl/ia/productividad/desarrollo/nushell-coprocesador-estructurado/?utm_source=linkedin&utm_medium=social&utm_campaign=nushell-coprocesador-estructurado

#Nushell #AIAgents #Reproducibility
Documento: `nushell-coprocesador-estructurado-carrusel.pdf`
Título sugerido del documento: `Cuándo Nushell ayuda a un agente — evidencia de 380 ejecuciones`
Texto alternativo sugerido: `Carrusel de seis láminas que resume una comparación de 380 ejecuciones con y sin una ruta selectiva hacia Nushell: diseño, mejoras observadas, costes, caso real agregado y regla final.`

---

## English version (optional)

I tested whether giving a coding agent a selective Nushell route actually improved its work. The result was not a shell ranking.

Across 380 runs, the tuned positive corpus improved from 23/30 to 30/30 correct answers, while median time rose from 6.2 to 9.5 seconds and median output from 152 to 368 tokens.

The holdout improved from 10/15 to 14/15, but Nushell activated in only 4/15 treatment runs. In an aggregate case based on a reconstruction of my master's thesis, both arms were correct throughout: the route changed, the relevant outcome did not.

The rule I kept is narrow: test Nushell when structured input, several transformations, and a concrete risk of silent parsing failure occur together. Otherwise, prefer the simpler tool.

Method, data, limitations, and reproducible case: https://3cucharadas.cl/en/ia/productividad/desarrollo/nushell-coprocesador-estructurado/?utm_source=linkedin&utm_medium=social&utm_campaign=nushell-coprocesador-estructurado

#Nushell #AIAgents #Reproducibility
