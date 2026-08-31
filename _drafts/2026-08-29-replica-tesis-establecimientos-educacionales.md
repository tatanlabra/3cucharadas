---
layout: single
title: "Replicar mi propia tesis en 3 cucharadas: ¿el error es de 2014 o es mío de hoy?"
subtitle: "Volví a levantar la tesis de magíster que escribí sobre entrada y salida de colegios en el mercado escolar chileno, y puse cada cuadro y cada figura frente a su original"
date: 2026-08-29 09:30:00 -0400
categories: [datos, educacion, politica-publica]
tags: [replicabilidad, educacion, mercado-escolar, voucher, mineduc, analisis-de-duracion, vulnerabilidad, auditoria]
description: "Reconstruí en 2026 mi tesis de magíster de 2014 sobre entrada y salida de establecimientos educacionales en Chile, comparé cada cuadro contra el publicado y, cuando aparecieron mis propios artefactos de 2014, contra ellos: 26 displays, 43 hipótesis contrastadas y ninguna divergencia sin explicar."
excerpt: "Cuando un cuadro reconstruido no coincide con el impreso, la pregunta útil no es cuál de los dos está mal, sino de quién es el error. Y para responderla hay que poner los dos al lado —y, cuando aparece, el artefacto que los produjo."
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

Lo que cuento acá es esa primera mitad. Reconstruí los ocho cuadros y las figuras, los puse frente a los publicados y fui decidiendo, celda por celda, de quién era cada diferencia. A mitad de camino aparecieron cinco artefactos de 2014 —la salida de Stata, hojas de mi planilla, un gráfico incrustado en el manuscrito— y la comparación pasó a tener tres columnas en vez de dos.
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
| **Productor** | El artefacto de 2014 que generó una cifra: una salida de Stata, una hoja de mi planilla de trabajo, el gráfico incrustado en el manuscrito. | La ejecución que lo creó: esa sigue perdida. |
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
  <figcaption><strong>Figura 1</strong> — Movilidad total por dependencia: el original de 2014 y mi réplica, que agrega los veinte años para que el saldo se lea de una vez. Los totales de la derecha suman 2.168 entradas y 2.069 salidas; la planilla con la que armé esa figura en 2014 dice 2.160 y 2.065, que es exactamente lo publicado.</figcaption>
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

Con una advertencia que me obligaba a bajar el tono: **el `do-file` histórico no se ejecutó**; lo que corrió fue una reimplementación controlada.
{: .text-justify}

Esa advertencia quedó a medias un mes después. La ejecución de 2014 sigue perdida —entorno, temporales y orden real de mis comandos—, pero volví a estimar la especificación final con el motor original, Stata 17 MP sobre mi propia licencia, y apareció algo mejor que un oráculo: **el productor**.
{: .text-justify}

### Cinco artefactos míos, encontrados

Rastreando el árbol de fuentes aparecieron cinco objetos que produjeron directamente lo publicado: la salida de `outreg` del modelo jerárquico, dos hojas de mi planilla de trabajo, una tercera con la brecha SIMCE, y un gráfico incrustado dentro del manuscrito con su serie adentro. La búsqueda cubrió todo lo que el árbol conserva, y eso importa tanto como el hallazgo:
{: .text-justify}

{: .table-caption}
**Tabla 2** — Dónde se buscó el productor de cada figura

| Corpus | Encontrados | Leídos |
|---|---:|---:|
| Gráficos `.gph` de Stata | 15 | 15 |
| Documentos `.doc` / `.docx` | 140 | 140 |
| Planillas `.xls` / `.xlsx` | 241 | 241 |
| Gráficos incrustados en `.docx` | 290 | 290 |

Cinco planillas binarias no las abría ninguna librería y hubo que decodificarlas registro a registro; noventa y dos documentos venían en el formato viejo de Word. Declarar la cobertura es lo que permite leer un «no aparece» como dato y no como cansancio.
{: .small}

Eso cambia la pregunta de todo el post. Hasta acá comparaba **mi reconstrucción contra lo impreso**, y cada divergencia admitía la excusa de que la equivocada era la reconstrucción. Con el productor a la vista hay una tercera columna —y en varios casos mi reconstrucción se parece más al trabajo de mi yo de 2014 que el texto que publiqué.
{: .text-justify}

En la figura de movilidad, sin ir más lejos: las participaciones de mi planilla quedan a **3,05 puntos** de la reconstrucción y a **13,41 puntos** del texto impreso. Mi réplica de 2026 está 4,4 veces más cerca de mi planilla de 2014 que mi propio documento publicado.
{: .text-justify}

### El coeficiente que no salió de mi salida

Mi cuadro del modelo jerárquico publica **0,003** para el rezago del puntaje SIMCE de matemáticas. La salida de Stata de 2014 que produjo esa tabla imprime **0,001**.
{: .text-justify}

No es una diferencia de motor: los otros once coeficientes de esa misma salida coinciden con la corrida de hoy hasta el cuarto decimal, y entre Stata y `statsmodels` la peor discrepancia sobre los efectos fijos es 0,43 %. Tampoco es un problema del insumo: la imputación de SIMCE que el `do-file` declara es idéntica entre ambos motores sobre 85.807 celdas, con una diferencia relativa máxima de 5,9·10⁻⁸ que viene de que Stata guarda en `float` de 32 bits.
{: .text-justify}

Sometí el 0,003 a siete hipótesis de origen —otra especificación de SIMCE de las que la propia tesis predeclara, otra precisión de impresión, la variable imputada del `do-file`, un trasplante desde otra celda de la misma tabla, la convención de decimales del cuadro, la propia salida de 2014, el reajuste con el motor original— y **las siete quedaron refutadas**. La estimación da 0,000533 en los dos motores, que redondea a 0,001 y no a 0,003.
{: .text-justify}

Es el hallazgo que más me incomoda, porque no puedo atribuirlo a la traducción a Python: la traducción y el original coinciden, y el que se aparta es el documento.
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
**Tabla 3** — Las dos celdas cuyos asteriscos no cuadran

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

El cuadro de copago trae un ejemplo exacto de esa cadena rota. Su nota al pie publica **N = 5.465**, que es el total de un panel; sus medias impresas salen de otro, de **5.022**. Las dos cifras son mías y viajaron por separado hasta la misma página.
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

**3. El copago promedia ocho años de pesos nominales sin deflactar.** Acá el productor también apareció, y con él el universo: la hoja de trabajo de 2014 imprime 17.051,23 y 9.665,54 pesos, y uno solo de los diez paneles la reproduce —a **0,00 y 0,005 pesos**, mientras el panel amplio se separa en 910,60 y 162,68—. Sobre ese universo la brecha cruda entre entrantes y salientes es \$7.385,7; calculada dentro de cada año y luego ponderada, \$6.655,7: **\$730,0, un 9,88 %, era composición temporal** y no diferencia entre establecimientos.
{: .text-justify}

El hallazgo sobrevive; la magnitud, no —y es más chica que la que yo mismo había medido antes sobre el panel amplio (\$1.009,4, 12,41 %), el que la hoja de 2014 descarta como universo—. Debajo hay algo mejor: la brecha pasa de \$8.175,8 en 2004 a \$2.481,3 en 2011. **Cae a menos de un tercio**, y mi promedio agrupado borraba justamente eso.
{: .text-justify}

<figure class="align-center">
  <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" alt="A la izquierda, la figura publicada en 2014 que relaciona el índice de Herfindahl comunal con la movilidad total, con el eje horizontal entre 0 y 100. A la derecha, la réplica de 2026 sobre el eje canónico de 0 a 10.000, medida con la variable que el do-file rotula como el índice: recta de pendiente negativa, p = 0,084 sobre 337 comunas." loading="lazy" decoding="async">
  <figcaption><strong>Figura 2</strong> — Concentración comunal y movilidad. El mismo índice aparece en tres escalas: el eje del original llega a 100, el texto cita niveles de 1.180 a 1.534, y la definición canónica va de 0 a 10.000 con 2.500 como umbral de alta concentración. La réplica está medida con `hhi_n_alumnos`, la variable que el propio `do-file` rotula como el índice: la pendiente sigue siendo negativa, pero sobre 337 comunas no se distingue de cero al 5 % (p = 0,084).</figcaption>
</figure>

**4. El índice de concentración corre en una escala diez veces la suya.** El índice de Herfindahl se define entre 0 y 10.000. La variable que mi propio `do-file` rotula «Índice de Herfindahl-Hirschman» reproduce los cinco niveles que cité por nombre con **1,34 % de error medio** —Santiago da 1.517,5 contra el 1.534 publicado—, pero lo hace multiplicada por cien mil: **diez veces la escala canónica**. En la escala correcta Santiago mide 151,7. No es un decimal: leído como lo publiqué, **318 de 337 comunas** quedarían sobre el umbral de alta concentración; en la escala canónica son **66**. Cambia qué mercado se llama concentrado.
{: .text-justify}

Acá me corrijo dos veces a mí mismo, y la segunda duele más. Primero medí la concentración con **otra columna** del panel, no con la que el `do-file` rotula como el índice; el error se delata solo, porque su razón contra lo publicado era casi constante —10,3, con dispersión 0,03—, señal de estar comparando contra algo proporcional pero distinto.
{: .text-justify}

Segundo: con esa columna el contraste descriptivo daba pendiente negativa y significativa (p = 0,009, 336 comunas). **Rehecho con la variable del `do-file`, el signo sigue siendo negativo pero la pendiente ya no se distingue de cero al 5 % (p = 0,084, 337 comunas).** Lo que queda en pie es que mi modelo de salidas comunales reportaba un coeficiente positivo y la nube descriptiva no lo acompaña; lo que se cae es la fuerza con que yo lo afirmaba.
{: .text-justify}

Y ese modelo acumula tres problemas de identificación: regresores contemporáneos que mi propio texto declara determinados conjuntamente, dependiente rezagada bajo efectos aleatorios[^nickell] e inferencia sobre 15 conglomerados.[^cameron] Con tan pocos grupos, el error estándar deja de ser confiable antes que el coeficiente.
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

## Dónde quedó la auditoría

Veintiséis objetos entre cuadros y paneles de figura. Diez reproducen lo publicado; diez divergen con un mecanismo medido —una etiqueta, un universo, una escala, una convención de redondeo—; **ninguno queda divergiendo sin explicación**; seis no admiten prueba numérica, porque son afirmaciones estructurales o les falta un dato que el panel no conserva.
{: .text-justify}

{: .table-caption}
**Tabla 4** — Estado de los veintiséis displays

| Veredicto | Displays |
|---|---:|
| Reproducen lo publicado | 10 |
| Divergen con mecanismo medido | 10 |
| Divergen sin explicar | 0 |
| Sin prueba numérica posible | 6 |
| **Total** | **26** |

Detrás de esos veredictos hay **43 hipótesis sometidas a contraste**, de las que 34 quedaron refutadas y 7 sobrevivieron. Registro las refutadas junto a las que sobrevivieron a propósito: una auditoría que solo publica lo que confirmó no es una auditoría, es una selección.
{: .text-justify}

## Cierre: la segunda mitad va hasta 2025

Un segundo post traerá la recreación ampliada hasta 2025. Las fuentes ya están adquiridas —catorce colecciones oficiales del MINEDUC, incluido el Directorio Oficial 1992-2025—, pero no adelanto cifras: extender la ventana mete cambios de régimen en el medio.
{: .text-justify}

Lo que me llevo es menos técnico de lo que esperaba. Los errores confirmados son asteriscos, escalas y aritmética elemental; los hallazgos que mueven una conclusión salieron de mirar qué medían mis variables.
{: .text-justify}

Y lo que más me sorprendió no fue encontrar errores, sino de qué lado aparecieron. Empecé asumiendo que la reconstrucción iba a ser el eslabón débil. Cuando aparecieron mis propios artefactos de 2014 —la salida de Stata, la planilla, el gráfico incrustado— resultó que la reconstrucción se parecía más a ellos que el documento que firmé.
{: .text-justify}

Ninguno de estos lo habría visto discutiendo cifras en prosa: los vi cuando puse la figura de 2014 al lado de la de 2026 y los ejes no coincidían.
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
