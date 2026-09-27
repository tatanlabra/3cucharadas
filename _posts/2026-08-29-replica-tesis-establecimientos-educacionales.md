---
layout: single
title: "Replicar mi tesis en 3 cucharadas I: qué sobrevivió y qué corrigió la evidencia"
subtitle: "Volví a medir mi tesis de 2014 sobre entrada y salida de colegios: la mayor parte de la historia resistió, varias cifras no y los archivos productores permitieron decidir por qué"
date: 2026-08-29 09:30:00 -0400
categories: [datos, educacion, politica-publica]
tags: [replicabilidad, educacion, mercado-escolar, voucher, mineduc, analisis-de-duracion, vulnerabilidad, auditoria]
description: "Recreé los resultados de mi tesis de 2014 sobre establecimientos educacionales en Chile y audité 34 afirmaciones: qué se sostuvo, qué estaba mal entonces y qué todavía no puede saberse."
excerpt: "La tesis no salió intacta, pero tampoco se derrumbó. Los archivos productores permitieron separar resultados recreados, errores de 2014, sensibilidades y límites de la evidencia."
author: clabra
lang: es
ref: replica-tesis-establecimientos-educacionales
permalink: /datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/
header:
  teaser: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/og-1200x630.webp
  og_image_alt: Tesis archivada y modelos escolares reconstruidos como metáfora de una réplica que corrige su original.
  overlay_image: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/replica-tesis-establecimientos-educacionales/teaser-mobile-640x360.webp
visual_id: replica-tesis-establecimientos
math: true
toc: true
toc_sticky: true
comments: true
author_profile: true
distribution:
  social: false
  republish: []
  skip_reason: "Difusión posterior pausada por decisión editorial al publicar el post."
ai_disclosure:
  level: some_ai
  components:
    text: unknown
    hero: generated
---

En abril de 2014 defendí y entregué mi tesis de magíster sobre entrada y salida de establecimientos educacionales en Chile entre 1992 y 2012.[^tesis] Doce años después estoy tratando de recrearla y extenderla hasta 2025.
{: .text-justify}

En ese intervalo cambiaron las reglas: municipalización en los ochenta; financiamiento compartido en los noventa; Subvención Escolar Preferencial en los dos mil; Inclusión y Nueva Educación Pública en los diez; y otra arquitectura estatal en los veinte.[^regimenes] El mercado mutó muy rápido: cambiaron también las relaciones que podrían explicar los cierres. La IA al menos publica notas de versión; el sistema escolar chileno no siempre.
{: .text-justify}

Antes de añadir trece años había que contestar una pregunta más modesta: **¿qué resultados de 2014 podía volver a producir con exactitud?** En síntesis: quince juicios quedaron correctamente respaldados; diez errores estaban en 2014; ninguno permanece como error conocido en la salida canónica de 2026; uno fallaba a ambos lados; otro era una coincidencia engañosa; y siete no permiten adjudicar un error claro.
{: .text-justify}

Quise enfrentar herramientas, pero la historia no es que Python derrotara a Stata ni que mi antiguo MacBook perdiera ante el Lenovo actual. Es qué sobrevivió al contraste, con más evidencia y experiencia —y el sesgo inevitable de auditarse a uno mismo. La tesis es mía y la auditoría también: no es una réplica independiente.
{: .text-justify}

Nada de lo que sigue es causal. «Entrada» y «salida» significan aparecer o desaparecer del registro, no observar la decisión de abrir, cerrar o quebrar. «IVE» es vulnerabilidad escolar agregada, no pobreza ni vulnerabilidad individual. Y «recreado» significa producido otra vez desde los datos y el código disponible, no haber recuperado la sesión exacta de 2014.
{: .small}

## Cucharada 1: qué sobrevivió

La primera conclusión sí resistió: entre 1992 y 2012 no hubo simplemente más o menos colegios; hubo una **reasignación entre dependencias** (tipos de administración escolar). Mi reconstrucción suma 2.168 entradas y 2.069 salidas. El sector municipal registra 346 entradas y 1.135 salidas; el particular subvencionado, 1.468 y 597; el particular pagado, 354 y 337.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp' | relative_url }}" title="Figura 1 — Movilidad por dependencia" aria-label="Abrir la Figura 1 ampliada">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-movilidad.webp' | relative_url }}" alt="A la izquierda, la figura de movilidad total por dependencia administrativa publicada en 2014. A la derecha, la réplica de 2026: municipal 346 entradas y 1.135 salidas, particular subvencionado 1.468 y 597, particular pagado 354 y 337." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figura 1</strong> — Movilidad por dependencia. La reconstrucción totaliza 2.168 entradas y 2.069 salidas; la planilla de 2014, 2.160 y 2.065. El patrón —salida municipal y entrada subvencionada— sobrevive.</figcaption>
</figure>

Los totales no son idénticos, pero cuentan la misma historia. Mi planilla de 2014 está a 3,05 puntos porcentuales de la reconstrucción y a 13,41 del texto publicado: la recreación se parece más al archivo productor que a la prosa que firmé.
{: .text-justify}

La segunda conclusión que resistió es distributiva. En el Gran Santiago, los establecimientos que después cierran atendían una matrícula más vulnerable: 87,4 % frente a 78,3 % en municipales y 72,2 % frente a 62,8 % en particulares subvencionados. Las 42 celdas reconstruidas caen dentro de la tolerancia de despliegue (margen compatible con el redondeo publicado), aunque el número efectivo de observaciones no coincide con el impreso. La magnitud sobrevive; el universo exacto, no.
{: .text-justify}

Esto describe selección (quiénes integran cada grupo), no efectos. Con datos de 2002 a 2012, Paredes y Fresard asocian menor matrícula con mayor probabilidad de cierre y estudian el destino posterior de los alumnos.[^paredes2018] Núñez, Solís y Soto examinan dos comunidades rurales del sur tras el terremoto de 2010 y muestran que el modo de cerrar una escuela importa para la cohesión social.[^nunez2014] Mi panel (datos que siguen las mismas unidades en el tiempo) no puede sostener esas conclusiones: observa flujos administrativos, no motivos, trayectorias ni vida comunitaria.
{: .text-justify}

También sobrevivieron varios resultados más pequeños: **10 de los 11 efectos fijos publicados** (coeficientes promedio del modelo), la brecha SIMCE de los subvencionados que cierran, siete comunas sobre un umbral de movilidad y el signo negativo entre concentración y movilidad. Con la constante, son 12 coeficientes en el archivo, 11 efectos en el cuadro y 10 coincidencias.
{: .text-justify}

{: .table-caption}
**Tabla 1** — Qué ocurrió con los 34 juicios auditados

| Resultado | Juicios | Lectura |
|---|---:|---|
| Calce correcto | 15 | Publicado y reconstruido sostienen la misma afirmación y una tercera fuente la respalda. |
| Error de 2014 | 10 | El productor o la reejecución respalda la reconstrucción y refuta lo publicado. |
| Error conocido en la salida 2026 | 0 | Las rutas discrepantes quedaron como sensibilidades y no entraron a la salida canónica. |
| Error a ambos lados | 1 | Ni el documento ni la reconstrucción representan bien el estimando (la cantidad que se quería medir). |
| Coincidencia engañosa | 1 | Ambos lados coinciden porque heredan la misma definición equivocada. |
| Límite, afirmación no numérica o procedencia | 7 | La evidencia no autoriza un ganador, pero sí permite decir por qué. |

El recuento por figura responde otra pregunta. De 26 objetos, hay doce convergencias, diez divergencias explicadas y cuatro sin prueba numérica; no queda ninguna divergencia inexplicada. No convierto ese inventario en «porcentaje de acierto»: una desigualdad, un redondeo y una igualdad literal no son la misma prueba.
{: .small}

## Cucharada 2: quién se equivocó

Una discrepancia entre 2014 y 2026 no identifica por sí sola al equivocado. Puede nacer en una transcripción, el código, la muestra o un cambio del estimando; con solo «publicado» y «reconstruido», esas explicaciones se inventan después de conocer el resultado.
{: .text-justify}

Clemens fija una carga conservadora: “follow-up studies should be considered robustness checks until proven to be replications” (p. 4).[^clemens2015] En castellano: un seguimiento es una prueba de robustez hasta demostrar que es una réplica. No es semántica: Herndon, Ash y Pollin solo aislaron exclusiones, errores de código y ponderaciones al obtener la planilla de trabajo de Reinhart y Rogoff.[^herndon2013] Para Christensen y Miguel, abrir datos y materiales permite someter la credibilidad de la evidencia a examen.[^christensen2018]
{: .text-justify}

Por eso añadí una tercera columna: artefactos de 2014 (archivos que dejaron huella del cálculo), como salidas de Stata, planillas y gráficos, y, cuando fue posible, una nueva ejecución. El diagrama exige custodia, recibo, comparación previa y atribución. Las tres entradas permanecen separadas para que una reparación técnica no reescriba la evidencia histórica. La tercera columna no siempre favoreció al presente.
{: .text-justify}

<figure class="recreation-pipeline-figure">
  <a href="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-es.svg' | relative_url }}" target="_blank" rel="noopener">
    <picture>
      <source media="(max-width: 47.99em)" srcset="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-es-mobile.svg' | relative_url }}">
      <img src="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-es.svg' | relative_url }}" alt="Tres clases de insumos —piezas y datos, estadística descriptiva y econometría asociacional— atraviesan una cadena compartida de custodia, ejecución, comparación y atribución antes de clasificar el resultado y declarar la frontera causal." loading="lazy" decoding="async">
    </picture>
  </a>
  <figcaption><strong>Figura 2.</strong> Pipeline anticorrimiento (cadena de trabajo que evita cambios silenciosos). Un gate fallido (control que debe aprobarse para seguir) detiene la afirmación; un calce aparente no rellena el vacío. Fuentes D2 reproducibles: <a href="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-es.d2' | relative_url }}">escritorio</a> y <a href="{{ '/assets/images/replica-tesis-establecimientos/pipeline-recreacion-es-mobile.d2' | relative_url }}">móvil</a>.</figcaption>
</figure>

La secuencia importa para política pública. Si cambia la definición de salida, la muestra o la precisión, un flujo administrativo puede parecer una caída del sistema; si el modelo corre sin conservar el mismo vector (la misma lista ordenada de valores), el verde solo acredita ejecución. La regla incómoda es esta: **reejecutable no significa recreable; recreable no significa coincidente; coincidente no significa correcto; correcto no significa causal**.
{: .text-justify}

### Donde me equivoqué en 2014

El caso más limpio está en el modelo jerárquico. El cuadro publica **0,003** para el rezago del SIMCE de matemáticas; la salida de Stata que produjo la tabla imprime **0,001**. Una reestimación da 0,000533 en Stata y Python, que redondea a 0,001. Siete explicaciones alternativas quedaron refutadas. No fue traducción ni precisión: fue transcripción.
{: .text-justify}

En la misma familia de modelos, dos filas rotuladas como varianzas (medidas de dispersión) eran los logaritmos de desviaciones estándar que Stata imprime, sin transformar y además cruzados. El cuadro publicó 3,82 como «varianza del intercepto» y 2,791 como «varianza residual»; las varianzas correspondientes eran 2.079,7 y 265,6. En otra celda, 0,4142 se convirtió en 1,4142. A veces la arqueología encuentra un mecanismo sofisticado; otras, un triste error de copia y pega.
{: .text-justify}

El índice de concentración produjo el error con mayor consecuencia interpretativa para la política pública. El Herfindahl-Hirschman (IHH, una medida de cuán concentrada está la oferta) va de 0 a 10.000 y usa 2.500 como umbral de alta concentración. Mi planilla guardó el índice por cien; el texto lo leyó como si estuviera por mil. Así, Santiago aparece con 1.534 cuando la escala correcta es aproximadamente 152.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" title="Figura 3 — Concentración y movilidad" aria-label="Abrir la Figura 3 ampliada">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/cara-a-cara-ihh.webp' | relative_url }}" alt="A la izquierda, la figura publicada en 2014 con un índice de concentración entre 0 y 100. A la derecha, la recreación sobre la escala canónica de 0 a 10.000, con pendiente negativa y p igual a 0,084." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figura 3</strong> — Concentración y movilidad. El signo negativo sobrevive, pero la pendiente deja de distinguirse de cero al 5 % (p = 0,084; el valor p resume, bajo el modelo, cuán incompatibles son los datos con una pendiente nula). La escala publicada habría clasificado 318 de 337 comunas como altamente concentradas; la canónica clasifica 66.</figcaption>
</figure>

La planilla incluso dejó escrita la fórmula del umbral: `=C2>2.5`. En su escala eso equivale a 250 puntos canónicos, no 2.500, y selecciona 330 de 346 comunas. Un filtro que aprueba al 95 % de los casos no está filtrando mucho.
{: .text-justify}

Otro resultado casi correcto escondía una definición distinta. El texto decía que ciudades intermedias y menores de 15.000 habitantes concentraban cerca del 80 % de la movilidad de seis regiones. La receta de la figura separaba capitales regionales del resto y daba 78,3 %. Aplicado literalmente, el umbral de población daba 11 %. El número estaba cerca; la frase describía otra partición.
{: .text-justify}

### Resumen de hallazgos clave

{: .table-caption}
**Tabla 2** — Diferencias que cambian la lectura, y de quién fue el error

| Objeto | Publicado en 2014 | Evidencia nueva | Veredicto |
|---|---|---|---|
| Rezago SIMCE, modelo jerárquico | 0,003 | Salida y dos motores: 0,001 | Error de 2014 |
| Varianzas del modelo | 3,82 y 2,791 | Eran log-desviaciones cruzadas | Error de 2014 |
| Coeficiente subvencionado | 1,4142 | Salida: 0,4142 | Error de 2014 |
| IHH comunal | Santiago ≈ 1.534 | Escala canónica ≈ 152 | Error de 2014 |
| «Menos de 15 mil habitantes» | ≈ 80 % | Capital/no capital: 78,3 %; población: 11 % | Error de 2014 |
| Alumnos por docente | 48 celdas | Hoja `rad`: 48/48; cálculo alternativo separado | Vector productor verificado |
| Brecha SIMCE, subvencionados que cierran | −4,3 | Hoja productora: −4,3 | Valor productor verificado |
| Movilidad bruta y tasas | 6,3; 4,5; 1,6 | Fórmulas productoras: 80/80 y 40/40 puntos | Calce final correcto |
| Movilidad neta | Entradas − salidas | Planilla y gráfico incrustado: 80/80 puntos | Calce final correcto; interpretación causal no probada |
| Brecha PSU | ≈ 10 | Resultado final: 10,40, no 11,25 | Calce final correcto |

El hallazgo nuevo más sugerente no estaba cuantificado en la tesis. La razón alumnos por docente de los establecimientos que salen cae de 17,95 a 12,22 durante los siete años previos, frente a 20,31 entre incumbentes (los que permanecen en el registro). No parece un derrumbe instantáneo sino un vaciamiento prolongado, visible retrospectivamente durante los siete años previos. La etiqueta es retrospectiva: marca toda la historia previa de un establecimiento que después desaparece.
{: .text-justify}

<figure class="align-center">
  <a class="image-popup" href="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" title="Figura 4 — La sombra de la muerte" aria-label="Abrir la Figura 4 ampliada">
    <img src="{{ '/assets/images/replica-tesis-establecimientos/sombra-de-la-muerte.webp' | relative_url }}" alt="Serie con intervalos de confianza de la razón alumnos por docente de establecimientos que salen: cae de 17,95 a 12,22 durante los siete años previos, frente a 20,31 entre incumbentes." loading="lazy" decoding="async">
  </a>
  <figcaption><strong>Figura 4</strong> — La «sombra de la muerte»: menos alumnos por docente durante los siete años anteriores a la salida. Es un patrón descriptivo condicionado por el problema del marcador temporal, no una estimación causal.</figcaption>
</figure>

Esa figura es útil para política pública precisamente porque no promete lo que no observa. Un deterioro gradual abre preguntas sobre alertas tempranas, matrícula, dotación y respuesta institucional; no demuestra que una intervención específica evite el cierre ni que el cierre cause el deterioro.
{: .text-justify}

## Cucharada 3: qué quedó listo para extender hasta 2025

**Esta era la prueba que necesitaba antes de sumar trece años: no que cada cifra de 2014 sobreviviera, sino saber exactamente qué estaba extendiendo.** Todo el itinerario computacional disponible volvió a ejecutarse; eso no hizo que todos los resultados fueran iguales. Para entenderlo había que separar tres cosas. Reejecutable significa que la ruta termina; recreable, que vuelve a producir un objeto comparable; coincidente, que supera el criterio preespecificado (fijado antes de mirar el resultado). Son afirmaciones distintas.[^comparison]
{: .text-justify}

{% include evidence-carousel.html %}

{: .table-caption}
**Tabla 3** — Qué ocurrió al reabrir los nueve casos dudosos

| Resultado | Casos | Qué permite decir |
|---|---:|---|
| Coincidencia | 3 | El Cuadro 4 reproduce 12/12 celdas; las Figuras 3 y 4 reproducen 40/40 y 80/80 puntos. |
| Diferencia | 2 | Los Cuadros 5 y 8 no superan su criterio preespecificado. |
| No comparable por diseño | 4 | La ruta corrió, pero falta una serie o vector común; comparar píxeles contestaría otra pregunta. |

El Cuadro 5 recupera N=30.484 y `duracion3`, pero sólo 10 de 20 coeficientes y 11 de 20 errores estándar igualan el redondeo impreso. El Cuadro 6 conserva 35 de 41 magnitudes; el 7, 10 de 11 efectos fijos, salvo 0,003 frente a 0,001. En el 8, sólo 4 de 12 coinciden bajo redondeo; ocho parecen truncadas (decimales cortados sin redondear). «Cerca» no es «igual a la precisión publicada».
{: .text-justify}

Python reconstruyó tablas y gráficos; una corrida fresca invocó Stata 17 mediante `stata-mp` y completó 14 rutas activas, incluida la recuperación gobernada de `do_058`, `do_059` y `do_060`.[^stata17][^harvest] El resultado es una **reejecución actual trazable**, no equivalencia histórica: prueba que la cadena puede recorrerse hoy, no que esta fuera la sesión de 2014.
{: .text-justify}

También separo dos inventarios que es fácil confundir. El registro probó **50 hipótesis**: **37 quedaron refutadas, 11 sostenidas, 1 parcial y 1 refutada para once de catorce términos**. El balance editorial contiene **34 juicios**. Las hipótesis cuentan explicaciones sometidas a contraste; los juicios cuentan afirmaciones y objetos publicados. Ninguno es una tasa de acierto del otro.
{: .text-justify}

No hice esta arqueología para absolver o condenar mi trabajo de 2014. Antes de construir 2013–2025 necesitaba separar qué podía producir de nuevo, qué estaba mal, qué era una sensibilidad (un resultado alternativo bajo otra decisión) y qué no podía compararse. También quise someter a herramientas actuales una tesis que costó sacar a flote. Que no haya salido intacta hace el ejercicio más útil.

Lo importante no es reivindicar el original, sino llegar al Post II con una base 1992–2012 auditable, errores conocidos corregidos y límites visibles. Ahora sí tiene sentido añadir trece años: no para prolongar una serie, sino para averiguar qué cambió con las reglas y qué significa que un establecimiento entre o salga del sistema.
{: .text-justify}

## Cierre, preparando para 2025

La tesis quedó dividida en resultados que sobreviven, errores de 2014, una salida canónica de 2026 sin errores conocidos y casos sin comparación válida. Esa partición muestra qué conservar y qué no llevar a 1992–2025.
{: .text-justify}

Sobrevive la reasignación de 1992–2012: pérdida municipal y expansión subvencionada. También sobrevive, **solo para el universo reconstruido del Gran Santiago**, la mayor vulnerabilidad de quienes después cierran. No sobreviven la escala del IHH, la lectura de «menos de 15 mil habitantes», dos varianzas, varios rótulos ni una definición temporal clave. Las discrepancias de la ruta actual se corrigieron hasta dejar una salida canónica de 2026 sin errores conocidos; las alternativas siguen visibles como sensibilidades, no como recreación.
{: .text-justify}

{: .table-caption}
**Tabla 4** — Qué uso público resiste y dónde termina la evidencia

| Resultado | Uso público razonable | Lo que no autoriza |
|---|---|---|
| Reasignación entre dependencias, 1992–2012 | Diagnóstico histórico del cambio sectorial | Atribuirlo causalmente a una reforma |
| Vulnerabilidad en el Gran Santiago reconstruido | Preguntar por protección y continuidad educativa | Generalizar a Chile o atribuir efectos del cierre |
| Razón alumnos/docente antes de la salida | Hipótesis retrospectiva para diseñar una alerta | Presentarla como clasificador actual o alerta validada |
| IHH corregido | Describir concentración en la escala correcta | Inferir el efecto de la competencia sobre cierres o movilidad |

La segunda parte no podrá añadir trece filas y fingir continuidad. Un establecimiento de los ochenta, uno de los noventa, uno posterior a la SEP, uno bajo Inclusión y uno traspasado a un Servicio Local no enfrentan el mismo mercado ni el mismo Estado. Una serie puede ejecutar impecablemente y contestar otra pregunta: el falso verde más elegante de la política pública.
{: .text-justify}

### De describir el cierre a identificar una política

La recreación deja un panel capaz de describir flujos, reconocer señales de riesgo y reestimar asociaciones. No observa por qué cerró cada establecimiento, qué habría ocurrido sin una reforma ni la trayectoria individual de sus alumnos. Añadir controles, efectos fijos, errores estándar más sofisticados o más cómputo puede reducir algunos sesgos; **no crea el contrafactual que falta** (qué habría ocurrido sin la reforma o el cierre).
{: .text-justify}

Para que la extensión a 2025 produzca evidencia de política social útil, el segundo post deberá distinguir tres rutas y no venderlas como intercambiables:

<div class="causal-routes causal-routes--es" markdown="1">

| Ruta | Pregunta y diseño | Gate que debe pasar |
|---|---|---|
| **Alerta descriptiva/predictiva** | Modelar transiciones entre activo, matrícula cero, receso, cierre oficial y ausencia del registro; estimar riesgo fuera de muestra (en años o casos no usados para ajustar el modelo). | Validación temporal, calibración (que el riesgo predicho se parezca a la frecuencia observada), umbrales de decisión y auditoría distributiva. Puede orientar monitoreo; no estima efectos. |
| **Reforma escalonada** | Evaluar cambios asociados al traspaso a Servicios Locales con diferencias en diferencias (comparar cambios entre grupos afectados y no afectados) y estudio de eventos por cohortes. | Fechas y exposición verificadas; tendencias paralelas (evolución previa semejante), anticipación, composición y derrames plausibles. Si el calendario respondió al riesgo, el diseño no es causal por decreto. |
| **Consecuencias del cierre** | Vincular trayectorias de estudiantes y comparar continuidad, distancia, asistencia, logro y abandono mediante estudio de eventos o diferencias en diferencias emparejadas. | Causa del cierre, controles realmente comparables y variación plausiblemente exógena (no determinada por el resultado); emparejar por sí solo no elimina la selección. |

</div>

Hay, sin embargo, una pregunta anterior al diseño econométrico. En un sistema con entrada y salida de proveedores, la llamada **«destrucción creativa»** (reemplazo de quienes salen por nuevos oferentes) puede renovar la oferta, desplazar establecimientos de menor desempeño o llevar estudiantes hacia alternativas mejores. Pero el balance no puede hacerse mirando solo qué establecimiento desaparece y cuál ocupa su lugar. En Chile existe también evidencia de costos del cierre sobre repitencia y abandono, y de efectos comunitarios que difícilmente caben en una cuenta de matrícula.[^grau2018][^nunez2014]
{: .text-justify}

Eso cambia la pregunta de política pública. No se trata de impedir cualquier cierre ni de conservar todo establecimiento. Se trata de saber **quién absorbe el costo de la transición**: quién debe cambiarse, adónde llega, cuánto más se desplaza, qué ocurre con su asistencia, aprendizaje y permanencia, y qué pierde la comunidad. Que existan cupos es necesario; no agota esos costos.
{: .text-justify}

Ahí quiero llevar el Post II: extender una base cuya construcción y fallas ahora conozco, distinguir cambios institucionales de cambios de registro y observar trayectorias individuales que la tesis de 2014 casi no podía ver. Importan por sí mismas y por lo que cada estudiante aporta a su entorno.
{: .text-justify}

La pregunta que queda abierta no es contar nuevamente entradas y salidas, sino **¿cuándo la destrucción creativa renueva efectivamente la oferta educativa y cuándo solo desplaza sus costos hacia estudiantes, familias y territorios con menor capacidad para absorberlos?**
{: .text-justify}

La ironía final es que el mercado escolar cambió de reglas más rápido que la IA y dejó peores notas de versión. Un RBD (identificador oficial del establecimiento, rol de base de datos) puede desaparecer del registro. **La trayectoria de un estudiante no se reinicia cuando eso ocurre.**
{: .text-justify}

---

## Referencias

[^tesis]: Labra Olivares, Cristián A. *Patrones de entrada y salida de establecimientos educacionales en Chile (1992-2012)*, tesis de magíster, Universidad de Chile, 2014. Profesor guía: Daniel Hojman T.

[^grau2018]: Grau, N.; Hojman, D.; Labra, C.; Mizala, A. [*Destructive Creation: School Turnover and Educational Attainment*]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}), DT 396, 2014; Grau, Hojman y Mizala, [*School closure and educational attainment*](https://doi.org/10.1016/j.econedurev.2018.05.003), 2018.

[^paredes2018]: Paredes, Ricardo D.; Fresard, Matías. *Voucher y cierre de escuelas en Chile*, *Estudios Públicos* 151, 7–27, 2018.

[^nunez2014]: Núñez, Carmen Gloria; Solís, Camila; Soto, Rodrigo. [¿Qué sucede en las comunidades cuando se cierra la escuela rural?](https://doi.org/10.11144/Javeriana.UPSY13-2.qscc), *Universitas Psychologica* 13(2), 615–625, 2014.

[^regimenes]: Biblioteca del Congreso Nacional de Chile. [Historia de la Ley N.º 3.063](https://www.bcn.cl/historiadelaley/historia-de-la-ley/vista-expandida/8363/); [Ley N.º 19.247](https://www.bcn.cl/leychile/navegar?idNorma=127911); [Ley N.º 20.248](https://www.bcn.cl/leychile/Navegar/index_html?idNorma=269001&idVersion=); [Ley N.º 20.845](https://www.bcn.cl/leychile/Navegar?idNorma=1078172&idParte=9605200&idVersion=2222-02-02); [Ley N.º 21.040](https://www.bcn.cl/leychile/Navegar?idNorma=1111237&idParte=9853075).

[^christensen2018]: Christensen, Garret; Miguel, Edward. [Transparency, Reproducibility, and the Credibility of Economics Research](https://doi.org/10.1257/jel.20171350), *Journal of Economic Literature* 56(3), 920–980, 2018.

[^clemens2015]: Clemens, Michael A. [The Meaning of Failed Replications: A Review and Proposal](https://doi.org/10.1111/joes.12139), *Journal of Economic Surveys* 31(1), 326–342, 2015.

[^herndon2013]: Herndon, Thomas; Ash, Michael; Pollin, Robert. [Does high public debt consistently stifle economic growth?](https://doi.org/10.1093/cje/bet075), *Cambridge Journal of Economics* 38(2), 257–279, 2013.

[^hamermesh2007]: Hamermesh, Daniel S. [Viewpoint: Replication in economics](https://doi.org/10.1111/j.1365-2966.2007.00428.x), *Canadian Journal of Economics* 40(3), 715–733, 2007.

[^stata17]: Recibo técnico fijado en el commit `0e9e02d4316d120336d6c2af26434beb5d4b24e0`: 15/15 roles con cero `r(NNN)`, Stata 17 con `c(MP)=1`, `c(flavor)=IC` informado por separado y cuatro raíces históricas intactas.

[^comparison]: Comparación terminal fijada en `tesis_mae_mejorada@a8ee6ac`: nueve casos reabiertos, cuatro familias inferenciales y umbrales separados para tablas, raster y equivalencia.

[^harvest]: Cosecha de salidas fijada en `tesis_mae_mejorada@cd6d19b`: reejecución dirigida de `do_058`, `do_059` y `do_060`, cuatro productos de datos validados y límites separados para smoke tests y gráficos no exportados.
