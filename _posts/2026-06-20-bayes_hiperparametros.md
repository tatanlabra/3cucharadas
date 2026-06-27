---
layout: single
title: "Hiperparámetros con Bayes en 3 cucharadas: menos grilla, más memoria estadística"
subtitle: "Optimización bayesiana en Python para modelos de vulnerabilidad y valor esperado de compra"
date: 2026-06-20
categories: [mlops, hpo, python, h2o]
tags: [bayesian-optimization, hyperparameter-optimization, h2o, xgboost, ebm, rsh, ecommerce, aucpr, reproducibilidad]
description: "Guía directa para usar optimización bayesiana como estrategia de búsqueda de hiperparámetros en modelos predictivos: un caso público tipo RSH con EBM y un caso privado tipo ecommerce con H2O XGBoost."
author: clabra
lang: es
ref: bayes-hiperparametros
permalink: /mlops/bayes-hiperparametros/
toc: true
toc_sticky: true
comments: true
author_profile: true
---

Imaginemos un modelo tabular con 10 valores de <span class="text-nowrap">learn_rate</span>, 8 de <span class="text-nowrap">max_depth</span>, 5 de <span class="text-nowrap">sample_rate</span> y 5 de <span class="text-nowrap">col_sample_rate</span>. Una grilla cartesiana entrenaría **2.000 modelos**. Con validación cruzada de 5 folds, la cuenta operativa sube a **10.000 ajustes internos**. En una máquina con RAM, VRAM o CPU acotadas, eso no es necesariamente más rigor: puede ser solo una forma cara de ignorar lo aprendido en las evaluaciones anteriores.
{: .text-justify}

Este post propone usar optimización bayesiana (BO) como una capa externa de decisión en Python. No gana siempre. Gana cuando el problema se parece a esto: función objetivo cara, espacio de búsqueda acotado, métrica razonablemente estable y presupuesto limitado.
{: .text-justify}


**Tres ideas para comenzar:**

- **BO no asume que el hiperparámetro tenga una distribución particular.** En el caso clásico con procesos gaussianos, lo que se modela probabilísticamente es la función objetivo evaluada en distintos puntos del espacio de hiperparámetros.
- **Random search sigue siendo un baseline serio.** Bergstra y Bengio mostraron que puede ser mucho más eficiente que la grilla cuando no todos los hiperparámetros importan por igual. BO parte desde ahí y agrega memoria estadística.
- **Optimizar hiperparámetros no arregla una mala función objetivo.** En RSH, por ejemplo, se podría modelar una circularidad (lo que llaman ahora "fuga de información" 🌊). En ecommerce, sin ser mi campo (bienvenidos comentarios) sería confundir propensión con causalidad. En ambos casos, BO puede encontrar más rápido una solución si el diseño predictivo está bien planteado.

---

## Tolerancia al contraste o cotejo con evidencia

Este post no compara resultados empíricos todavía (segunda patita), pero he probado su funcionamiento en productivo con un par de casos, por lo que viene desde lo empírico con datos reales y trazabilidad completa (SAT: Sistema de Alerta Temprana de Deserción Escolar, y Modelo de Subtramos de vulnerabilidad en RSH, tramos dentro del 40% más vulnerable con EBM).
{: .text-justify}

{: .table-caption}
**Tabla 1** — Evidencia mínima para sostener el enfoque

| Punto                                                                                               | Evidencia                                                                                                                                                                                                                                                                                                                                                                                                 | Implicancia práctica                                                                                                                                                                                                                     |
| --------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| H2O resuelve bien el entrenamiento, pero no trae BO como búsqueda nativa estándar                   | [H2O Grid Search](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/grid-search.html) documenta grillas cartesianas y aleatorias.                                                                                                                                                                                                                                                                            | Si queremos una búsqueda secuencial informada, H2O puede quedar como motor de entrenamiento y Python como capa de optimización externa. La separación es limpia: H2O entrena; Optuna, SMAC, BoTorch o `skopt` deciden el próximo punto.  |
| Para este post, Optuna es una opción más práctica que `gp_minimize`                                 | [Optuna](https://optuna.org/) está diseñado como framework de HPO, con estudios, trials, persistencia, samplers y pruners. Además, su [`GPSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html) ajusta un proceso gaussiano sobre la función objetivo.                                                                                           | En un flujo H2O + Python, Optuna permite registrar cada corrida, reanudar experimentos y comparar samplers. `gp_minimize` sirve para explicar BO con pocas líneas, pero Optuna es más defendible como herramienta de trabajo.            |
| La normalidad no está en el hiperparámetro, sino en el modelo probabilístico de la función objetivo | En BO con procesos gaussianos, lo que se modela es la función $f(\theta)$, por ejemplo, la AUC obtenida al entrenar con cierto conjunto de hiperparámetros. Véase [`skopt.gp_minimize`](https://scikit-optimize.github.io/stable/modules/generated/skopt.gp_minimize.html) y [`Optuna GPSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html). | No corresponde decir que “el hiperparámetro sigue una normal”. Lo correcto es decir que, dadas las evaluaciones ya observadas, BO construye una distribución predictiva sobre el desempeño esperado de nuevas configuraciones.           |
| Random search no es ingenuo: es un baseline fuerte cuando pocos hiperparámetros importan de verdad  | [Bergstra y Bengio (2012)](https://jmlr.org/papers/v13/bergstra12a.html) muestran que random search puede ser más eficiente que una grilla cuando solo algunas dimensiones concentran la variación relevante.                                                                                                                                                                                             | La comparación justa no es BO versus grilla enorme, sino BO versus random search con el mismo presupuesto de evaluaciones. Si BO no supera ese baseline, el espacio de búsqueda o el surrogate probablemente no están aportando.         |
| HPO exige diseño experimental, no solo una librería                                                 | [Bischl et al. (2023)](https://arxiv.org/abs/2107.05847) ordenan el problema de HPO como una decisión experimental: espacio de búsqueda, presupuesto, remuestreo, métrica, riesgo de sobreajuste y validación externa.                                                                                                                                                                                    | La optimización debe fijar antes el presupuesto de trials, la métrica objetivo y la separación train/validation/test. En RSH y ecommerce, repetir tuning contra la misma validación puede sobreajustar tanto como ajustar mal el modelo. |
| BO puede ahorrar evaluaciones, pero depende del surrogate y de la función de adquisición            | [SMAC3, Lindauer et al. (2022)](https://www.jmlr.org/papers/v23/21-0888.html) muestra un enfoque robusto de optimización bayesiana para configuraciones de algoritmos; [BoTorch, Balandat et al. (2020)](https://arxiv.org/abs/1910.06403) ofrece un marco más flexible para adquisición, restricciones y optimización avanzada.                                                                          | “Usar Bayes” no basta. En espacios mixtos, condicionales o con muchas categorías, TPE/SMAC puede ser más práctico que un GP simple; en problemas avanzados, BoTorch es más potente, pero también más exigente.                           |
| Expected Improvement es útil, pero no debe tratarse como receta cerrada                             | [Ament et al. (2023)](https://arxiv.org/abs/2310.20708) revisan problemas numéricos de EI y proponen logEI; otros trabajos recientes muestran que la adquisición puede comportarse mal con ruido, mala inicialización o superficies difíciles.                                                                                                                                                            | En validaciones ruidosas, como CV, validación temporal o muestras pequeñas, conviene fijar semillas, repetir folds o usar métricas menos inestables. La adquisición decide dónde mirar después, no garantiza verdad estadística.         |
| LLM + BO es una línea interesante, no un reemplazo de la validación                                 | [LLAMBO, Liu et al. (2024)](https://arxiv.org/abs/2402.03921), y trabajos sobre priors o modelos preentrenados para BO, como [HyperBO, Wang et al. (2021)](https://arxiv.org/abs/2109.08215), apuntan a usar conocimiento previo para proponer mejores espacios o puntos iniciales.                                                                                                                       | Un modelo de razonamiento puede ayudar a definir rangos, descartar configuraciones absurdas o proponer warm starts. Pero no reemplaza holdout, validación temporal, auditoría de leakage ni análisis sustantivo del target.              |


---

## Cucharada 1: dos problemas de ranking, no dos juguetes predictivos

Quiero usar dos ejemplos con igual peso. Uno viene del mundo público: ordenar hogares por vulnerabilidad relativa usando una muestra pública del RSH (sobre lectura territorial de datos sociales en Chile escribí antes en [CASEN 2024 en 3 cucharadas]({{ "/datos/politica-publica/julia/casen/casen2024-julia-waffles-politica-publica/" | relative_url }})). El otro viene del mundo privado: ordenar clientes, sesiones o contactos según el valor esperado de una acción comercial en ecommerce.
{: .text-justify}

No son problemas equivalentes en lo sustantivo. El primero tiene consecuencias de legitimidad pública; el segundo, de eficiencia comercial. Pero ambos comparten una misma pregunta estadística: si lo importante es ordenar bien los casos, ¿cómo buscamos hiperparámetros que mejoren ese orden sin gastar cómputo en combinaciones poco informativas?
{: .text-justify}

{: .table-caption}
**Tabla 2**: Dos ejercicios equivalentes para pensar HPO como problema de ranking

| Dimensión                  | RSH, muestra pública                                                                                                                                                                                                                                                                                                        | Ecommerce, estilo Shopify                                                                                                                                                                                                                                                                                |
| -------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Unidad de análisis         | Hogar                                                                                                                                                                                                                                                                                                                       | Cliente, sesión, cliente-campaña o cliente-producto                                                                                                                                                                                                                                                      |
| Pregunta sustantiva        | ¿Qué hogares presentan mayor probabilidad relativa de vulnerabilidad, usando señales indirectas y no el ingreso como predictor?                                                                                                                                                                                             | ¿Qué clientes o sesiones deberían priorizarse porque concentran mayor probabilidad de compra, margen esperado o respuesta incremental a una acción comercial?                                                                                                                                            |
| Fuente                     | Muestra pública, aleatoria y anonimizada del RSH disponible en [BIDAT](https://bidat.gob.cl/details/ficha/dataset/registro-social-de-hogares-muestra-diciembre-2025)                                                                                                                                                        | Tabla propia de navegación, transacciones y campañas: sesiones, carritos, compras, margen, descuentos, recurrencia, stock, canales y dispositivos                                                                                                                                                        |
| Target razonable           | Una señal de vulnerabilidad construida fuera del set de predictores. Puede ser binaria, ordinal o continua: pertenencia a un grupo de alta vulnerabilidad, transición posterior a mayor vulnerabilidad, índice externo de privación o tramo de referencia usado solo como etiqueta, no como predictor.                      | Dos opciones distintas: propensión a comprar o valor esperado, si no hay experimento; uplift causal, si existe asignación aleatoria, grupo de control o diseño cuasi experimental defendible.                                                                                                            |
| Qué se excluye             | Ingreso directo y variables que sean copias operacionales del ingreso o del target. La idea no es reconstruir mecánicamente la CSE, sino evaluar cuánto ordenamiento se puede recuperar desde señales indirectas de vulnerabilidad.                                                                                         | Variables posteriores a la intervención: apertura de campaña si se predice antes de enviarla, descuento efectivamente usado si se quiere decidir a quién ofrecerlo, compra observada dentro de la ventana objetivo, o cualquier variable contaminada por el resultado.                                   |
| Modelo propuesto           | **EBM** con `interpretML`, porque permite revisar funciones parciales, monotonicidades plausibles, saltos extraños y efectos de interacción sin perder completamente el control interpretativo.                                                                                                                             | **H2O XGBoost**, porque es fuerte en tabular, maneja no linealidades e interacciones, escala bien y permite tratar el ecommerce como un problema operativo de ranking o valor esperado.                                                                                                                  |
| Predictores plausibles     | Tamaño del hogar, composición etaria, presencia de niños, personas mayores o dependientes, escolaridad, ocupación, situación laboral, tenencia de vivienda, materialidad, hacinamiento, allegamiento, ruralidad, comuna o territorio agregado, acceso a servicios, discapacidad y otras señales socioeconómicas indirectas. | Recencia, frecuencia, monto, margen, sesiones recientes, tiempo desde última compra, categorías visitadas, abandono de carrito, profundidad de navegación, sensibilidad histórica a descuentos, canal, device, fuente de adquisición, stock, estacionalidad, devoluciones y respuesta previa a campañas. |
| Qué significa ordenar bien | Que, al comparar dos hogares, el hogar más vulnerable según la señal de referencia tienda a recibir un score mayor. En la parte alta del ranking, debería concentrar hogares con mayor vulnerabilidad observada, sin depender de ingreso directo.                                                                           | Que el top k seleccionado concentre más compra, margen o efecto incremental que una priorización aleatoria o que una regla simple de negocio. Si hay experimento, importa el efecto incremental; si no lo hay, solo puede hablarse de propensión o valor esperado.                                       |
| Métricas principales       | AUC si el target es binario y el ranking global importa; AUCPR si la alta vulnerabilidad es minoritaria; NDCG@k o lift@k si importa el tramo superior; Kendall o Spearman si el target es ordinal; Brier y curvas de calibración si el score se interpretará como probabilidad.                                             | Para propensión: AUCPR, lift@k, gain@k y profit@k. Para valor esperado: RMSE, MAE, pinball loss o error ponderado por margen. Para uplift causal: uplift@k, Qini y ganancia incremental estimada en holdout experimental.                                                                                |
| Riesgo principal           | Circularidad, fuga de información y falsa legitimidad. Un modelo puede ordenar muy bien porque aprendió variables que son casi equivalentes al ingreso o al propio target. Eso sería buen desempeño aparente, pero mala evidencia.                                                                                          | Confundir propensión con causalidad. Los mejores compradores no son necesariamente los más persuadibles. Un cupón enviado a quien habría comprado igual puede aumentar conversiones observadas y, al mismo tiempo, destruir margen incremental.                                                          |

### Caso RSH: ranking de vulnerabilidad sin usar ingreso directo

El ejercicio RSH no debería formularse como “predecir pobreza” ni como “replicar la CSE”. Eso cerraría demasiado rápido la discusión y aumentaría el riesgo de circularidad. Lo más limpio es formularlo como un problema de **ranking supervisado de vulnerabilidad relativa**.
{: .text-justify}

La función objetivo no busca solo acertar clases, sino mejorar la probabilidad de que el orden entre hogares sea correcto. Si el hogar $i$ es más vulnerable que el hogar $j$, el modelo debería asignar $s_i > s_j$. Ese score puede calibrarse como probabilidad, pero su primer uso analítico es ordinal: ordenar hogares con la mayor estabilidad posible.
{: .text-justify}

Una forma simple de escribirlo es:
{: .text-justify}

$$
s_i = f_\theta(X_i), \quad X_i \not\ni ingreso
$$

donde $s_i$ es el score de vulnerabilidad del hogar, $X_i$ contiene señales indirectas y $\theta$ representa los hiperparámetros del modelo. El ingreso directo queda fuera de $X_i$. También deberían quedar fuera las variables que sean una copia administrativa demasiado cercana del target.
{: .text-justify}

En un EBM, el score tiene una ventaja importante: puede descomponerse en efectos por variable e interacciones acotadas.
{: .text-justify}

$$
g(E[y_i]) = \beta_0 + \sum_k f_k(x_{ik}) + \sum_{k<l} f_{kl}(x_{ik}, x_{il})
$$

Esa forma no vuelve al modelo “justo” por sí misma, pero permite auditarlo mejor. Si el score aumenta de manera brusca en un punto absurdo de escolaridad, materialidad o composición del hogar, la forma funcional queda a la vista. En este caso, la interpretabilidad no es estética: es parte de la defensa metodológica del ranking.
{: .text-justify}

Para HPO, un hiperparámetro ilustrativo es <span class="text-nowrap">max_bins</span>. Controla cuán finamente se discretizan las variables continuas antes de aprender efectos. Con pocos bins, el modelo puede suavizar demasiado y perder diferencias reales. Con demasiados bins, puede capturar ruido, producir saltos artificiales y empeorar la estabilidad del orden.
{: .text-justify}

La comparación correcta no es “grilla versus Bayes” en abstracto. La comparación relevante es esta:
{: .text-justify}

| Estrategia    | Qué haría con <span class="text-nowrap">max_bins</span>                                                        | Problema                                                                                                          |
| ------------- | ------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------- |
| Grilla        | Probaría valores fijos, por ejemplo 32, 64, 128, 256, 512 y 1024.               | Ordenada, pero rígida. Si el buen rango está entre dos valores o depende de otro hiperparámetro, puede mirar mal. |
| Random search | Probaría valores aleatorios dentro de un rango.                                 | Es un baseline fuerte, pero no aprende explícitamente de los resultados anteriores.                               |
| BO            | Usa los resultados ya observados para decidir el siguiente valor de <span class="text-nowrap">max_bins</span>. | No garantiza el óptimo, pero puede ahorrar evaluaciones si la superficie tiene estructura aprovechable.           |

Un movimiento bivariado más realista sería optimizar <span class="text-nowrap">max_bins</span> junto con <span class="text-nowrap">interactions</span>. La intuición es clara: más granularidad en variables principales puede exigir más cautela con interacciones. Si se aumentan ambas sin control, el ranking puede mejorar en validación interna y empeorar fuera de muestra.
{: .text-justify}

$$
\theta = (\mathrm{max\_bins},\ \mathrm{interactions})
$$

La métrica objetivo principal sería **Kendall’s tau-b**, porque el propósito del modelo no es solo clasificar hogares vulnerables, sino preservar correctamente la prelación entre ellos: que hogares con mayor vulnerabilidad de referencia reciban sistemáticamente scores más altos que hogares menos vulnerables. AUCPR puede reportarse como métrica complementaria si la alta vulnerabilidad se define como evento minoritario; NDCG@k, si interesa auditar especialmente el tramo superior del ranking; y Brier/calibración, solo si el score será interpretado como probabilidad. En una versión más exigente, además del desempeño global, exigiría estabilidad por subgrupos y territorio: un ranking que ordena bien solo en la región o tipo de hogar dominante no está listo para discusión pública sería según mi opinión.
{: .text-justify}


### Caso ecommerce: lift operativo sin confundirlo con causalidad

En ecommerce hay que separar tres modelos que suelen mezclarse:
{: .text-justify}

1. **Propensión**: probabilidad de compra futura.
2. **Valor esperado**: compra esperada ponderada por monto, margen o probabilidad de conversión.
3. **Uplift causal**: incremento atribuible a una acción, por ejemplo enviar un cupón, mostrar un banner o activar una recomendación.

Si no hay experimento, y aquí entro en territorio desconocido para mi conocimiento, yo no prometería causalidad. Haría un modelo de propensión o de valor esperado y lo evaluaría como ranking comercial. Si hay experimento A/B o grupo de control válido, entonces sí se puede hablar de uplift más real: la pregunta pasa a ser quién compra más porque fue tratado, no simplemente quién iba a comprar de todos modos.
{: .text-justify}

Usaría H2O XGBoost con dos variantes:
{: .text-justify}

| Escenario       | Target                                                           | Métrica                                                                       |
| --------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| Sin experimento | Compra futura, margen futuro o valor esperado en 7, 14 o 30 días | AUCPR, lift@k, gain@k, profit@k, RMSE o MAE si el target es monto             |
| Con experimento | Diferencia incremental atribuible al tratamiento                 | uplift@k, Qini, ganancia incremental y validación contra holdout experimental |

En el caso observacional, un score útil podría ser:
{: .text-justify}

$$
score_i = \hat{p}_i(\text{compra}) \times \widehat{margen}_i
$$

Eso no mide causalidad, pero puede servir para priorizar acciones si el objetivo es eficiencia comercial. Si el costo del contacto o del descuento es conocido, conviene optimizar ganancia esperada:
{: .text-justify}

$$
profit_i = \hat{p}_i(\text{compra}) \times \widehat{margen}_i - costo_i
$$

En H2O XGBoost, un hiperparámetro ilustrativo es <span class="text-nowrap">max_depth</span>. Controla la profundidad máxima de cada árbol. Con árboles muy superficiales, el modelo puede perder interacciones relevantes: por ejemplo, clientes recurrentes, con abandono reciente de carrito, alta sensibilidad a descuentos y stock disponible. Con árboles demasiado profundos, puede memorizar ruido de campañas, estacionalidad o eventos puntuales.
{: .text-justify}

| Estrategia    | Qué haría con <span class="text-nowrap">max_depth</span>                                                                                          | Problema                                                                                                      |
| ------------- | ------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------- |
| Grilla        | Probaría profundidades fijas, por ejemplo 2, 4, 6, 8, 10 y 12.                                                     | Simple, pero se vuelve costosa al combinarse con <span class="text-nowrap">learn_rate</span>, <span class="text-nowrap">min_rows</span>, <span class="text-nowrap">sample_rate</span> y <span class="text-nowrap">col_sample_rate</span>. |
| Random search | Probaría profundidades aleatorias y combinaciones al azar de otros hiperparámetros.                                | Buen baseline, especialmente si pocas dimensiones importan de verdad.                                         |
| BO            | Aprende desde los trials previos qué zonas producen mejor lift@k, profit@k o AUCPR, y decide dónde probar después. | Depende de que la métrica sea estable y de que la validación represente el uso real del modelo.               |

El movimiento bivariado natural es <span class="text-nowrap">max_depth</span> con <span class="text-nowrap">min_rows</span> o <span class="text-nowrap">learn_rate</span>.
{: .text-justify}

$$
\theta = (\mathrm{max\_depth},\; \mathrm{min\_rows})
$$

La intuición: si se permiten árboles más profundos, puede ser necesario exigir más observaciones mínimas por hoja para evitar reglas demasiado específicas. Otra dupla frecuente es <span class="text-nowrap">max_depth</span> con <span class="text-nowrap">learn_rate</span>: árboles más complejos con tasas de aprendizaje altas pueden sobreajustar rápido; tasas más bajas pueden necesitar más árboles y más tiempo.
{: .text-justify}

Ahí BO tiene sentido práctico. No porque “Bayes sea mejor” por definición, sino porque una grilla cartesiana crece rápido. Si se prueban 8 valores de profundidad, 8 de <span class="text-nowrap">min_rows</span>, 6 de <span class="text-nowrap">learn_rate</span>, 5 de <span class="text-nowrap">sample_rate</span> y 5 de <span class="text-nowrap">col_sample_rate</span>, ya son 9.600 combinaciones antes de pensar en validación cruzada o ventanas temporales. Random search reduce el costo; BO intenta reducirlo aprendiendo de cada evaluación.
{: .text-justify}

La idea de fondo para ambos ejemplos es la misma:
{: .text-justify}

$$
\theta^* = \arg\max_{\theta \in \Theta} M(f_\theta, D_{valid})
$$

donde $M$ puede ser AUCPR, NDCG@k, lift@k, profit@k, Qini o una combinación penalizada por inestabilidad. BO no asume que los hiperparámetros tengan distribución normal. En su versión con procesos gaussianos, modela probabilísticamente la función objetivo: qué desempeño cabe esperar para una configuración todavía no evaluada, dado lo que ya se observó.
{: .text-justify}

La decisión metodológica queda así: random search es el baseline mínimo; BO entra cuando cada entrenamiento cuesta, cuando el espacio de búsqueda es razonable y cuando la métrica de validación representa el uso real del modelo. Si esas tres condiciones no se cumplen, BO puede producir una optimización elegante sobre una pregunta mal planteada.
{: .text-justify}

## Cucharada 2: el experimento antes que el algoritmo

La optimización de hiperparámetros, creo yo, parte fijando como evaluaremos el éxito. En estos dos ejemplos, el contrato de éxito tendría seis piezas:
{: .text-justify}

{: .table-caption}
**Tabla 3**: Contrato mínimo antes de hacer HPO

| Decisión          | Qué debe quedar fijo                                                         | Por qué importa                                                                            |
| ----------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------ |
| Unidad            | Hogar, cliente, sesión o cliente-campaña                                     | Si la unidad cambia, cambia el target, la validación y la interpretación del score.        |
| Target            | Señal de vulnerabilidad, compra futura, margen esperado o efecto incremental | No se optimiza lo mismo si el target es ordinal, binario, monetario o causal.              |
| Métrica principal | Una métrica alineada con la decisión                                         | La métrica debe representar el uso real del ranking, no solo verse bien en un leaderboard. |
| Split             | Validación fuera de muestra, idealmente temporal cuando corresponde          | El tuning contra una validación débil produce confianza artificial.                        |
| Presupuesto       | Número máximo de entrenamientos                                              | HPO es una decisión bajo restricción de cómputo, no una búsqueda infinita.                 |
| Baseline          | Regla simple y random search                                                 | BO debe justificar su complejidad contra alternativas razonables.                          |

La parte estadística clave es que la métrica observada no es la métrica verdadera. Cada trial entrega una estimación ruidosa del desempeño:
{: .text-justify}

$$
\widehat{M}(\theta) = M(\theta) + \varepsilon
$$

Ese ruido aparece por splits, folds, prevalencia del evento, tamaño muestral, cambios temporales, subgrupos pequeños y variación propia del entrenamiento. En RSH puede verse como inestabilidad por territorio o tipo de hogar. En ecommerce puede verse como estacionalidad, campañas simultáneas, cambios de stock, descuentos o ventanas de validación poco representativas.
{: .text-justify}

Por eso, en lugar de optimizar solo una métrica limpia, conviene optimizar una métrica penalizada:
{: .text-justify}

$$
J(\theta) = M(\theta) - \lambda_1 \cdot \text{inestabilidad} - \lambda_2 \cdot \text{complejidad}
$$

La intuición es simple. Una configuración no debería ganar solo porque sube marginalmente la métrica principal. Debería ganar porque mejora el ranking (particularmente en RSH/SIVUST, donde el orden es lo crítico), se sostiene fuera de muestra y no introduce una complejidad difícil de defender.
{: .text-justify}

En el caso RSH, esa función podría premiar Kendall’s tau-b y castigar inestabilidad por territorio, composición del hogar o subgrupos relevantes. En ecommerce, podría premiar profit@k o lift@k y castigar volatilidad temporal, exceso de profundidad o dependencia de una campaña puntual.
{: .text-justify}

El espacio de búsqueda también debe pensarse, no solo declararse. Una grilla amplia puede parecer neutral, pero en realidad contiene supuestos. Decidir que <span class="text-nowrap">max_depth</span> va de 2 a 20, o que <span class="text-nowrap">max_bins</span> puede llegar a 4096, no es inocente. Amplía el espacio, encarece la búsqueda y permite configuraciones que quizá nunca deberían competir.
{: .text-justify}

Una regla práctica:
{: .text-justify}

{: .table-caption}
**Tabla 4**: Cómo pensaría el espacio de búsqueda

| Tipo de hiperparámetro   | Tratamiento razonable                         | Ejemplo                                                         |
| ------------------------ | --------------------------------------------- | --------------------------------------------------------------- |
| Enteros de complejidad   | Rangos acotados y sustantivamente defendibles | <span class="text-nowrap">max_depth</span>, <span class="text-nowrap">max_bins</span>, <span class="text-nowrap">interactions</span>                         |
| Tasas o regularización   | Escala logarítmica                            | <span class="text-nowrap">learn_rate</span>, penalizaciones, regularización                    |
| Muestreo                 | Rangos conservadores                          | <span class="text-nowrap">sample_rate</span>, <span class="text-nowrap">col_sample_rate</span>                                |
| Parámetros condicionales | Activarlos solo si corresponde                | Interacciones solo si el modelo base ya es estable              |
| Costo computacional      | Registrar tiempo por trial                    | Un punto levemente mejor puede no justificar triplicar el costo |

Aquí entra BO, pero con un rol acotado. No define el target, no corrige fugas/circularidad ("leakage" 🕶️) y no decide qué error es aceptable. La secuencia práctica sería esta:
{: .text-justify}

1. correr una regla simple;
2. correr random search con un presupuesto fijo;
3. correr BO con el mismo presupuesto;
4. comparar no solo la mejor métrica, sino la curva de aprendizaje;
5. revisar estabilidad en test;
6. publicar también los trials fallidos.

La curva de aprendizaje importa mucho. Si BO supera a random search recién después de 300 trials, pero el presupuesto real era 30, no aportó. Si random search alcanza un resultado similar con menor complejidad, también es evidencia. La pregunta no es qué método tiene mejor reputación, sino cuál entrega mejor decisión con el presupuesto disponible.
{: .text-justify}

Para este post, usaría **Optuna** como orquestador principal. No porque sea “más bayesiano” en abstracto, sino porque permite registrar estudios, reanudar trials, comparar samplers y guardar resultados (originalmente probé con otras librerías en SAT sin éxito, terminaba usando artefactor como pickle para suplir cosas que no tenía la librería). El motor de entrenamiento puede ser H2O XGBoost, EBM u otro modelo tabular; Optuna solo necesita una función objetivo que devuelva una métrica.
{: .text-justify}

También distinguiría tres niveles de búsqueda:
{: .text-justify}

{: .table-caption}
**Tabla 5**: Tres niveles de búsqueda posibles

| Nivel      | Estrategia                    | Uso razonable                                                                      |
| ---------- | ----------------------------- | ---------------------------------------------------------------------------------- |
| Base       | Random search                 | Baseline técnico mínimo. Si BO no lo supera, no hay mucho que defender.            |
| Intermedio | TPE o GP vía Optuna           | Buen equilibrio entre practicidad, trazabilidad y búsqueda secuencial.             |
| Avanzado   | SMAC, BoTorch o multiobjetivo | Al parecer es útil si hay restricciones, objetivos múltiples o espacios condicionales complejos (NO LO HE PROBADO). |

No sobredefendería el proceso gaussiano. Para explicar BO es útil, pero en espacios mixtos, discretos o condicionales, TPE o SMAC parecen ser más prácticos. En problemas pequeños y relativamente suaves, GP tiene sentido. En problemas grandes, con categorías, condicionalidad o ruido, conviene comparar. En resumen, hay que medir cuánto cuesta cada evaluación y qué inestabilidad no estamos dispuestos a aceptar.
{: .text-justify}

---

## Cucharada 3: Alternativas y cierre

En lugar de BO o en su complemento, el uso de LLM puede entrar como una capa. Primero, antes del tuning, para proponer espacios de búsqueda razonables, detectar hiperparámetros mal escalados y sugerir restricciones. Segundo, durante el tuning, para leer trials fallidos y proponer ajustes al espacio. Tercero, después del tuning, para revisar consistencia: pérdida de información, variables sospechosas, métricas que no calzan con la decisión o explicaciones demasiado frágiles (HAY QUE EXPERIMENTAR).
{: .text-justify}

El flujo más interesante sería híbrido:
{: .text-justify}

$$
\text{conocimiento de dominio}
\rightarrow
\text{espacio de búsqueda}
\rightarrow
\text{random search}
\rightarrow
\text{BO}
\rightarrow
\text{auditoría}
\rightarrow
\text{rediseño}
$$

Y, en paralelo:
{: .text-justify}

$$
\text{LLM}
\rightarrow
\text{mejores hipótesis de búsqueda}
\rightarrow
\text{menos trials absurdos}
$$

La gracia no es reemplazar Bayes por LLM ni LLM por Bayes. La gracia es que cada parte haga lo que sabe hacer mejor. El LLM puede ayudar a pensar, resumir, criticar y proponer. BO puede asignar mejor el presupuesto de evaluación. La validación, en cambio, sigue siendo el tribunal.
{: .text-justify}

---

## Cierre: una invitación a probar con datos reales

La pregunta que me interesa dejar abierta no es si BO es “mejor” que random search. Esa pregunta, así formulada, es demasiado amplia. La pregunta útil es más concreta:
{: .text-justify}

**con 30 entrenamientos disponibles, ¿qué estrategia entrega el ranking más estable, defendible y útil?**

En RSH, eso significa probar si un modelo transparente puede ordenar vulnerabilidad relativa sin usar ingreso directo (por ausencia o fragilidad del dato directo), con auditoría por territorio y tipo de hogar. En ecommerce, significa probar si un modelo tabular optimizado mejora una regla simple de negocio en profit@k, lift@k o ganancia incremental, respetando ventanas temporales.
{: .text-justify}

Considerar un set de estrategias:
{: .text-justify}

| Estrategia    | Pregunta que responde                                           |
| ------------- | --------------------------------------------------------------- |
| Regla simple  | ¿Cuánto aporta realmente el modelo?                             |
| Random search | ¿Cuánto se gana con una búsqueda barata y honesta?              |
| BO            | ¿Cuánto se gana aprendiendo del historial de trials?            |
| LLM + BO      | ¿Cuánto se gana si el espacio de búsqueda parte mejor diseñado? |

Si alguien trabaja en política pública, me gustaría saber qué señales indirectas usan para ordenar sus modelos sin caer en circularidad. Si alguien trabaja en ecommerce u otra industria, cómo definen métricas cuando no hay experimento y cómo separan propensión de efecto incremental. Y si alguien ya usa LLM para diseñar búsquedas de hiperparámetros, feliz de leerlo 🤩.
{: .text-justify}

La optimización de hiperparámetros no es el centro del problema. El centro es la decisión que viene después del ranking. En política pública, una mala prelación puede dañar legitimidad. En industrias, puede destruir margen. En ambos casos, ordenar bien importa más que declarar ganador a un algoritmo.
{: .text-justify}

## Referencias

* Ament, Sebastian; Daulton, Samuel; Eriksson, David; Balandat, Maximilian; Bakshy, Eytan. [Unexpected Improvements to Expected Improvement for Bayesian Optimization](https://arxiv.org/abs/2310.20708), NeurIPS 2023.
* Balandat, Maximilian et al. [BoTorch: A Framework for Efficient Monte-Carlo Bayesian Optimization](https://arxiv.org/abs/1910.06403), NeurIPS 2020.
* Bergstra, James; Bengio, Yoshua. [Random Search for Hyper-Parameter Optimization](https://jmlr.org/papers/v13/bergstra12a.html), JMLR 2012.
* Bischl, Bernd et al. [Hyperparameter Optimization: Foundations, Algorithms, Best Practices and Open Challenges](https://doi.org/10.1002/widm.1484), WIREs Data Mining and Knowledge Discovery, 2023. Versión abierta en [arXiv](https://arxiv.org/abs/2107.05847).
* Caruana, Rich et al. [Intelligible Models for HealthCare: Predicting Pneumonia Risk and Hospital 30-day Readmission](https://www.microsoft.com/en-us/research/wp-content/uploads/2017/06/KDD2015FinalDraftIntelligibleModels4HealthCare_igt143e-caruanaA.pdf), KDD 2015.
* H2O.ai. [Grid (Hyperparameter) Search](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/grid-search.html), documentación oficial.
* H2O.ai. [XGBoost](https://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/xgboost.html), documentación oficial.
* InterpretML. [Explainable Boosting Machine](https://interpret.ml/docs/ebm.html) y [Hyperparameters](https://interpret.ml/docs/hyperparameters.html), documentación oficial.
* Lindauer, Marius; Eggensperger, Katharina; Feurer, Matthias; Biedenkapp, André; Deng, Difan; Benjamins, Carolin; Ruhkopf, Tim; Sass, René; Hutter, Frank. [SMAC3: A Versatile Bayesian Optimization Package for Hyperparameter Optimization](https://www.jmlr.org/papers/v23/21-0888.html), JMLR 2022.
* Liu, Tennison; Astorga, Nicolás; Seedat, Nabeel; van der Schaar, Mihaela. [Large Language Models to Enhance Bayesian Optimization](https://arxiv.org/abs/2402.03921), 2024.
* Ministerio de Desarrollo Social y Familia, BIDAT. [Registro Social de Hogares, Muestra diciembre 2025](https://bidat.gob.cl/details/ficha/dataset/registro-social-de-hogares-muestra-diciembre-2025), publicado el 30 de enero de 2026.
* Optuna. [Optuna: A Hyperparameter Optimization Framework](https://optuna.org/) y [`GPSampler`](https://optuna.readthedocs.io/en/stable/reference/samplers/generated/optuna.samplers.GPSampler.html), documentación oficial.
* Scikit-Optimize. [`gp_minimize`](https://scikit-optimize.github.io/stable/modules/generated/skopt.gp_minimize.html), documentación oficial.
* Villagrán Prieto, Nicolás; Garrido-Merchán, Eduardo C. [Default Machine Learning Hyperparameters Do Not Provide Informative Initialization for Bayesian Optimization](https://arxiv.org/abs/2602.08774), 2026, preprint.
* Zhou, Han; Ma, Xingchen; Blaschko, Matthew B. [A Corrected Expected Improvement Acquisition Function Under Noisy Observations](https://arxiv.org/abs/2310.05166), 2023.
