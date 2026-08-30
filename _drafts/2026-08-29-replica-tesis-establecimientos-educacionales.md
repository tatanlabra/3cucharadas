---
layout: single
title: "Replicar mi propia tesis en 3 cucharadas: ¿el error es de 2014 o es mío de hoy?"
subtitle: "Volví a levantar la tesis de magíster que escribí sobre entrada y salida de colegios en el mercado escolar chileno, y puse cada cuadro y cada figura frente a su original"
date: 2026-08-29 09:30:00 -0400
categories: [datos, educacion, politica-publica]
tags: [replicabilidad, educacion, mercado-escolar, voucher, mineduc, analisis-de-duracion, vulnerabilidad, auditoria]
description: "Reconstruí en 2026 mi tesis de magíster de 2014 sobre entrada y salida de establecimientos educacionales en Chile, comparé cada cuadro contra el publicado y separé los errores del documento de los errores de mi propia réplica."
excerpt: "Cuando un cuadro reconstruido no coincide con el impreso, la pregunta útil no es cuál de los dos está mal, sino de quién es el error. Y para responderla hay que poner los dos al lado."
author: clabra
lang: es
ref: replica-tesis-establecimientos-educacionales
permalink: /datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/
header:
  teaser: /assets/images/teasers/teaser-replica-tesis.webp
  og_image: /assets/images/replica-tesis-establecimientos/og-replica-tesis-1200x630.webp
  og_image_alt: "Comparación cara a cara de la figura de concentración de mercado y movilidad escolar entre la tesis de 2014 y su réplica de 2026"
math: true
toc: true
toc_sticky: true
comments: true
author_profile: true
---

En abril de 2014 entregué una tesis de magíster sobre entrada y salida de establecimientos educacionales en Chile entre 1992 y 2012.[^tesis] Quería extender esa serie hasta 2025 y me topé con el orden natural del problema: antes de extender mi trabajo, tenía que poder reproducirlo.
{: .text-justify}

Lo que cuento acá es esa primera mitad. Reconstruí los ocho cuadros y las figuras, los puse frente a los publicados y fui decidiendo, celda por celda, de quién era cada diferencia.
{: .text-justify}

**La tesis es mía y la auditoría también**, así que esto no es una réplica independiente: estoy revisando decisiones que tomé yo y que en su momento me parecieron razonables.
{: .text-justify}

El incentivo corre en dos direcciones —indulgencia con mi yo de 2014, o severidad para aparentar rigor—, y lo único que lo contiene es una regla: no doy por buena ninguna divergencia que no pueda mostrar. De ahí que este post tenga más cuadros y figuras lado a lado que prosa.
{: .text-justify}

Declaro un segundo conflicto. Grau, Hojman y Mizala publicaron en 2018 un artículo sobre cierre de establecimientos y logro educativo en el sistema chileno.[^grau2018] Según recuerdo, sus agradecimientos mencionan mi contribución en etapas tempranas; **no he logrado verificarlo con el material que tengo a la vista**, así que lo dejo como recuerdo y no como hecho.
{: .text-justify}

Si es efectivo, me sirve de credencial y de sesgo al mismo tiempo. Daniel Hojman, además, fue mi profesor guía.
{: .text-justify}

## Contrato de lectura

| Concepto | Qué significa acá | Qué no significa |
|---|---|---|
| **Réplica** | Volver a producir mis figuras, cuadros y estimaciones desde los datos, con código nuevo. | Recuperar la ejecución de 2014: entorno, temporales y orden real de mis comandos **no se recuperaron**. |
| **Divergencia** | Una celda reconstruida que no coincide con la impresa. | Un error: puede estar en el documento, en mi réplica o en la cadena que las une. |
| **Entrada / salida** | Que un establecimiento aparezca o deje de aparecer en el registro oficial. | Apertura o quiebre como decisión: no observo el motivo, solo el flujo. |
| **IVE** | Índice de vulnerabilidad escolar: porcentaje de la matrícula clasificada como vulnerable. | Pobreza medida en el hogar ni indicador individual del alumno. |
| **Claim trazable** | Afirmación amarrada a un artefacto verificable y a su hash. | Opinión mía. |

**Alcance.** Trabajo con el PDF de 2014, su fuente LaTeX y mis `do-files`. Nada de lo que sigue es causal: son asociaciones condicionales dentro de un panel, sin estrategia de identificación detrás.
{: .small}

## Cucharada 1: qué recreé, y qué significa lo recreado

Chile financia la educación escolar con una subvención por alumno que sigue al estudiante, y así conviven tres dependencias: municipal, particular subvencionada y particular pagada.
{: .text-justify}

Eso vuelve medible la entrada y la salida: si el dinero se mueve con la matrícula, la oferta puede reorganizarse sin que nadie lo decrete. Mi tesis quería describir esa reorganización.
{: .text-justify}

La parte informática es anecdótica y la despacho en dos líneas: el documento ya no compilaba —`utf8x` y `harvard` fueron retirados de LaTeX— y traducir el código a Python obligó a contrastar cada estimación contra Stata. Importa lo que apareció al mirar los objetos.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp' | relative_url }}" alt="A la izquierda, la figura de movilidad total por dependencia administrativa publicada en 2014, con barras apiladas por año entre 1993 y 2012. A la derecha, la réplica de 2026 con los mismos flujos agregados en el período: municipal 346 entradas y 1.135 salidas, particular subvencionado 1.468 entradas y 597 salidas, particular pagado 354 y 337." loading="lazy" decoding="async">
  <figcaption><strong>Figura 1</strong> — Movilidad total por dependencia: el original de 2014 y mi réplica, que agrega los veinte años para que el saldo se lea de una vez. Los totales de la derecha suman 2.168 entradas y 2.069 salidas, el universo restringido que sostiene los hechos estilizados.</figcaption>
</figure>

Puestos así, los flujos dicen algo que la lámina apilada por año escondía: **la reasignación tiene dirección**. El sector municipal pierde establecimientos (346 entradas contra 1.135 salidas) y el particular subvencionado los gana (1.468 contra 597), mientras el particular pagado queda casi en tablas. No es un mercado que crezca: es uno que cambia de manos.
{: .text-justify}

El segundo objeto que recreé mide el porcentaje de matrícula vulnerable por dependencia y situación de cierre, en el Gran Santiago. Lo pongo contra el publicado en su fila de totales.
{: .text-justify}

{: .table-caption}
**Tabla 1** — Porcentaje de matrícula vulnerable, fila Total: publicado en 2014 frente a mi reconstrucción

| Dependencia | Situación | Publicado | Reconstruido | Diferencia | N |
|---|---|---:|---:|---:|---:|
| Municipal | Sin cierre | 78,3 | 78,347 | +0,047 | 2.815 |
| Municipal | Con cierre | 87,4 | 87,429 | +0,029 | 74 |
| Particular subvencionado | Sin cierre | 62,8 | 62,827 | +0,027 | 5.269 |
| Particular subvencionado | Con cierre | 72,2 | 72,218 | +0,018 | 249 |
| Total reportado | Sin cierre | 68,4 | 68,386 | −0,014 | 8.246 |
| Total reportado | Con cierre | 74,9 | 74,936 | +0,036 | 327 |

Las 42 celdas del cuadro caen dentro de la tolerancia de despliegue, pero el N efectivo que reproduzco no es el publicado: la fila queda clasificada como divergencia de universo, no como coincidencia.
{: .small}

El fondo del cuadro es más incómodo que su aritmética: **los establecimientos que cierran atendían, antes de cerrar, a una matrícula sistemáticamente más vulnerable que los que siguen abiertos**, y eso ocurre dentro de cada dependencia, no solo entre ellas. Nueve puntos en el sector municipal, casi diez en el particular subvencionado.
{: .text-justify}

Describe una selección, no un efecto: no observo qué habría pasado con esos alumnos sin el cierre.
{: .text-justify}

## Cucharada 2: ¿error del pasado o error del presente?

Cuando una celda no calza, lo que importa es de quién es el error. Sin criterio explícito la discusión se vuelve una pelea de opiniones donde yo tengo la última palabra, que es justo donde un autor que se audita no debería estar.[^dewald]
{: .text-justify}

Mi criterio fue construir un oráculo. Reimplementé de forma controlada, desde una foto versionada del código, la ruta que produce los cuadros descriptivos, y la corrí en Stata 17 contra mi versión en Python: **44 celdas, diferencia máxima absoluta de 3,6·10⁻¹²**.
{: .text-justify}

Con una advertencia que me obliga a bajar el tono: **el `do-file` histórico no se ejecutó**; lo que corrió fue una reimplementación controlada, y así queda registrado en el artefacto.
{: .text-justify}

El modelo de duración necesitó su propio contraste, y ahí apareció lo interesante. Modelo la probabilidad de que un establecimiento salga en el año $$t$$ dado que seguía abierto, con enlace log-log complementario, la especificación estándar cuando el evento se observa por períodos y no en tiempo continuo:[^jenkins]
{: .text-justify}

$$
h(t \mid x) = 1 - \exp\!\left[-\exp\!\left(x'\beta + \gamma(t)\right)\right]
$$

Sobre un caso sintético, Stata y `statsmodels` coinciden en los coeficientes hasta $$1{,}0\cdot 10^{-7}$$ y en la log-verosimilitud hasta $$3{,}6\cdot 10^{-14}$$, pero **sus errores estándar difieren hasta 0,025**: los de Stata coinciden exactamente con los de la Hessiana observada y los del default de Python no.
{: .text-justify}

Los coeficientes son el hallazgo; los errores estándar son las estrellas. Que lo primero calce no garantiza lo segundo. 🙂
{: .text-justify}

Con el oráculo funcionando pude adjudicar los dos errores de significancia. Ninguno sobrevive al redondeo, porque el estadístico que decide es un cociente entre dos números impresos en la misma celda:
{: .text-justify}

$$
|z| = \frac{|\hat\beta|}{\operatorname{ee}(\hat\beta)}
$$

{: .table-caption}
**Tabla 2** — Las dos celdas cuyos asteriscos no cuadran

| Cuadro y término | Publicado | Reconstruido | Error estándar publicado | \|z\| máximo | Asteriscos publicados | Corresponden |
|---|---:|---:|---:|---:|:--:|:--:|
| Cuadro 6, esp. 1 — Dummy cierre | −5,0907 | −5,090749 | 1,2147 | 4,19 | 1 | 2 |
| Cuadro 8 — Varianza del intercepto | 0,008 | 0,008745 | — | 2,43 | 2 | 1 |

El coeficiente reconstruido coincide hasta el sexto decimal: la divergencia está en la estrella, no en la estimación.
{: .small}

La confusión del primero no se quedó en la tabla. El párrafo anterior lee ese coeficiente como no significativo y el siguiente lo lee como significativo, en la misma página. Es un error de 2014 y es mío.
{: .text-justify}

Hay un tercer tipo que no puedo adjudicar a nadie. En mi fuente LaTeX las filas «Observaciones» de los cuatro cuadros de regresión están **vacías** y el N viaja aparte: compuse esas tablas a mano en vez de exportarlas.
{: .text-justify}

Eso no prueba que haya cifras mal —la mayoría calza—, pero corta la cadena entre la estimación y lo impreso: una celda discrepante puede ser tanto una transcripción torcida como un insumo distinto.
{: .text-justify}

Y un número que preferiría no escribir: de las **30 propuestas de revisión** que produjo esta auditoría, solo **12 tienen hoy un claim trazable con su hash**. Las otras 18 están rotuladas como propuesta o no verificado, y así hay que leerlas. Quien se lleve las 30 como hallazgos habrá leído este post al revés.
{: .text-justify}

## Cucharada 3: los cinco hallazgos que cambian una lectura

**1. Mi marcador de salida no marcaba salidas.** La variable `id_salida` correlaciona −0,977 con el año calendario: cae de 1.676 casos marcados en 1992 a exactamente 0 en 2012, mientras las salidas efectivas oscilan entre 42 y 290 sin tendencia (ρ = +0,382). No dice «cerró», dice «cerrará en algún año dentro de la ventana»: un establecimiento que cierra en 2011 queda marcado en todos los años anteriores y en ninguno posterior.
{: .text-justify}

Contamina los tres cuadros descriptivos y la definición del evento en el modelo de duración.
{: .text-justify}

**2. Mi variable de duración mide antigüedad observada, no edad institucional.** El panel empieza en 1992 y los establecimientos que ya existían entran truncados por la izquierda, cosa que no declaré; encima le impuse al riesgo base una forma lineal. Medida año a año esa pendiente es de +0,018 puntos porcentuales anuales con p = 0,27: no la distingo de cero. No es un detalle de forma, porque el riesgo base es justo lo que el modelo usa para separar el efecto del tiempo del de las covariables.
{: .text-justify}

**3. El copago promedia ocho años de pesos nominales sin deflactar.** La brecha cruda entre entrantes y salientes que publiqué es de \$8.133,6. Calculada dentro de cada año y luego ponderada, cae a \$7.124,2: **\$1.009,4, un 12,41 %, era composición temporal** y no diferencia entre establecimientos. El hallazgo sobrevive, la magnitud no. Y hay algo mejor debajo: la brecha pasa de \$8.085,69 en el primer año de la serie a \$3.821,18 en el último. **Converge a menos de la mitad**, y mi promedio agrupado borraba justamente eso.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" alt="A la izquierda, la figura publicada en 2014 que relaciona el índice de Herfindahl comunal con la movilidad total, con el eje horizontal entre 0 y 100. A la derecha, la réplica de 2026 con el mismo cruce sobre el eje canónico de 0 a 10.000, con la recta ajustada de pendiente negativa." loading="lazy" decoding="async">
  <figcaption><strong>Figura 2</strong> — Concentración comunal y movilidad. El eje del original llega a 100; el índice de Herfindahl se define entre 0 y 10.000, con 2.500 como umbral de alta concentración. La réplica agrega la recta ajustada sobre 336 comunas.</figcaption>
</figure>

**4. El índice de concentración está en una escala que no es la suya, y su signo no concuerda.** Puestas las figuras al lado, el eje del original llega a 100 y el del índice de Herfindahl llega a 10.000. La comuna de Santiago, que cité por nombre, mide 157,1 contra el 1.534 que publiqué.
{: .text-justify}

Con la escala corregida, más concentración va descriptivamente con **menos** movilidad (pendiente negativa, p = 0,009, 336 comunas), mientras mi modelo de salidas comunales reportaba un coeficiente positivo. Y ese modelo acumula tres problemas de identificación: regresores contemporáneos que mi propio texto declara determinados conjuntamente, dependiente rezagada bajo efectos aleatorios[^nickell] e inferencia sobre 15 conglomerados.[^cameron] Con tan pocos grupos, el error estándar deja de ser confiable antes que el coeficiente.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" alt="Serie con intervalos de confianza de la razón alumnos por docente de aula de los establecimientos que cierran, desde siete años antes del último año marcado hasta ese año: cae de 17,95 a 12,22, frente a una línea horizontal en 20,3 que representa a los establecimientos incumbentes." loading="lazy" decoding="async">
  <figcaption><strong>Figura 3</strong> — La sombra de la muerte, medida: alumnos por docente de aula de los establecimientos que salen, por año respecto del último año marcado, contra los incumbentes.</figcaption>
</figure>

**5. La «sombra de la muerte» era medible y solo la nombré.** La razón de alumnos por docente de los establecimientos que salen cae de forma monótona de **17,95 a 12,22** en los siete años previos, contra **20,31** de los incumbentes. No es un colapso repentino: es un vaciamiento de siete años. Eso cambia la lectura de política, porque un deterioro con esa forma es observable mientras ocurre.
{: .text-justify}

Con la salvedad del hallazgo 1: el eje mide años respecto del último año marcado, y ese marcador es el que resultó no significar lo que yo creía.
{: .text-justify}

Queda una deuda que no es un error sino una ausencia: el marco schumpeteriano organiza mi título, mi resumen y mi conclusión, pero nunca lo contrasté. La descomposición de reasignación que separa la mejora dentro de los incumbentes de la que viene de entradas y salidas —el estándar de la literatura que yo mismo citaba— no está en el documento.[^griliches]
{: .text-justify}

## Cierre: la segunda mitad va hasta 2025

Un segundo post traerá la recreación ampliada hasta 2025. Las fuentes ya están adquiridas —catorce colecciones oficiales del MINEDUC, incluido el Directorio Oficial 1992-2025—, pero no adelanto cifras: extender la ventana mete cambios de régimen en el medio.
{: .text-justify}

Lo que me llevo es menos técnico de lo que esperaba. Los dos errores confirmados son asteriscos y aritmética elemental; los hallazgos que mueven una conclusión salieron de mirar qué medían mis variables.
{: .text-justify}

Y ninguno lo habría visto discutiendo cifras en prosa: los vi cuando puse la figura de 2014 al lado de la de 2026 y los ejes no coincidían.
{: .text-justify}

---

## Referencias

[^tesis]: Labra Olivares, Cristián A. *Patrones de entrada y salida de establecimientos educacionales en Chile (1992-2012)*, tesis de magíster, Universidad de Chile, 2014. Profesor guía: Daniel Hojman T.

[^grau2018]: Grau, Nicolás; Hojman, Daniel; Mizala, Alejandra. [School closure and educational attainment: Evidence from a market-based system](https://doi.org/10.1016/j.econedurev.2018.05.003), Economics of Education Review 2018.

[^dewald]: Dewald, William G.; Thursby, Jerry G.; Anderson, Richard G. Replication in Empirical Economics, American Economic Review 1986.

[^jenkins]: Jenkins, Stephen P. [Easy Estimation Methods for Discrete-Time Duration Models](https://doi.org/10.1111/j.1468-0084.1995.tb00031.x), Oxford Bulletin of Economics and Statistics 1995.

[^nickell]: Nickell, Stephen. [Biases in Dynamic Models with Fixed Effects](https://doi.org/10.2307/1911408), Econometrica 1981.

[^cameron]: Cameron, A. Colin; Miller, Douglas L. [A Practitioner's Guide to Cluster-Robust Inference](https://doi.org/10.3368/jhr.50.2.317), Journal of Human Resources 2015.

[^griliches]: Griliches, Zvi; Regev, Haim. [Firm Productivity in Israeli Industry 1979-1988](https://doi.org/10.1016/0304-4076(94)01601-U), Journal of Econometrics 1995.
