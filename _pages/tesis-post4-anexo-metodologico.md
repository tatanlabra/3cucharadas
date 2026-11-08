---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Anexo de la parte IV: cohortes escolares y registros de educación superior"
description: "Calendarios, denominadores, soporte y trazabilidad de la comparación de educación superior."
permalink: /datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/
ref: tesis-post4-anexo-metodologico
lang: es
author: clabra
author_profile: true
math: true
toc: true
toc_sticky: true
table_contract: explicit-v1
last_modified_at: 2026-11-07 23:40:00 -0300
published: true
f2_complete: true
publication_authorized: true
scientific_status: DESCRIPTIVE_ONLY
readiness: READY_FOR_PUBLICATION
---

<!-- SCIENTIFIC_STATUS: DESCRIPTIVE_ONLY; READINESS: READY_FOR_PUBLICATION; F2_COMPLETE: true; PUBLICATION_AUTHORIZED: true. -->
<!-- scientific-state: DESCRIPTIVE_ONLY -->
<!-- publication-readiness: READY_FOR_PUBLICATION -->

{% include thesis-series-nav.html current=4 %}

El [artículo principal]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/' | relative_url }}) presenta las tres preguntas y los límites que cambian su interpretación. Este anexo documenta el calendario, los denominadores y la trazabilidad. El diseño compara generaciones escolares; no sigue el mismo grupo de personas antes y después ni identifica efectos individuales.

## Dos generaciones y un calendario común

Llamo **G** al año del evento y **g** al curso inicial de enseñanza media: primero, segundo o tercero. La generación anterior estaba matriculada en G−5; la posterior, en G−1. Si **B** es el año basal, para cada generación calculo el primer año posterior al egreso escolar esperado como **B+5−g**, suponiendo avance regular:

| Generación | Año basal | Primer año posterior al egreso esperado |
|---|---|---|
| Anterior | G−5 | G−g |
| Posterior | G−1 | G+4−g |
{: .table--compact .table--scroll}

Por ejemplo, primero medio en 2015 conduce a cuarto medio en 2018 y al primer año posterior en 2019. La ventana de acceso observado comprende 2019 y 2020. La etiqueta generación anterior tampoco garantiza que su resultado sea estrictamente anterior a G: con G=2016 y primero medio basal en 2011, el acceso se observa en 2015–2016, la persistencia en 2015–2017 y la titulación en 2015–2020. Esas ventanas pueden coincidir con el evento o prolongarse después de él. El calendario esperado no se recalcula según el egreso efectivo de cada estudiante: por eso la medida combina posibles atrasos escolares con lo que ocurre al pasar a educación superior.

Se consideran todos los años de evento candidatos entre 2009 y 2024 y se verifica el seguimiento por curso y desenlace. La serie empieza en 2009 porque la generación G−5 necesita registros escolares desde 2004, además de cobertura posterior de educación superior. Las eras histórica y moderna se presentan separadas porque usan información distinta para clasificar la pérdida de oferta; no se estima un agregado único que presuponga equivalencia entre ambas.

Versiones accesibles de las figuras: [Tabla accesible del calendario]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-calendar-table-es.html' | relative_url }}) y [Matriz accesible de ventanas por grado]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-calendar-window-matrix-es.html' | relative_url }}).

## Qué se cuenta en cada resultado

El denominador es la cohorte escolar basal elegible, con identificación válida y seguimiento completo, dentro de las celdas comparables. No se restringe a quienes ingresaron a educación superior. Los conteos exactos de estudiantes se muestran solo para el acceso primario agregado de dos años en cada era y corresponden a la **generación posterior**; los conteos de escuelas abarcan ambas generaciones. Los demás contrastes omiten conteos de personas por privacidad combinada.

| Resultado | Registro requerido desde el primer año posterior al egreso esperado |
|---|---|
| Acceso observado | Al menos una matrícula de pregrado SIES durante dos años. No acredita primera entrada de la persona. |
| Destinos | En esos mismos dos años: solo universidad, solo instituto profesional o centro de formación técnica, ambos tipos, o ninguno. Un tipo desconocido se trata como información incompleta. |
| Persistencia registrada | Matrícula en al menos dos años distintos de una ventana de tres; no necesariamente consecutivos. |
| Titulación observada | Al menos un título de pregrado durante seis años calendario, incluidos los extremos. |
{: .table--compact .table--scroll}

SIES corresponde al Servicio de Información de Educación Superior. El extracto de matrícula utilizado cubre 2007–2026; el de títulos, 2007–2025. Son fuentes fechadas, susceptibles de revisión: verificar sus archivos y conteos no prueba que toda trayectoria nacional esté cubierta ni que cada enlace individual sea correcto.

El seguimiento moderno permite agregar acceso para 2016–2024, persistencia para 2016–2023 y titulación para 2016–2019. La composición por curso cambia en los extremos: no basta tener el año de evento para disponer de la misma ventana de seguimiento. **Seguimiento incompleto**, **falta de comparadores** y **supresión por privacidad** son estados diferentes; ninguno se reemplaza por cero.

## Cómo se construye el contraste

El pareo principal exige el mismo año de evento, región, dependencia, ruralidad, código de enseñanza y curso basal. Cada celda necesita las cuatro combinaciones: escuelas con evento y de comparación, en las generaciones anterior y posterior. Los controles principales no tienen un evento D1 observado en el inventario 2005–2024. Esto selecciona escuelas supervivientes durante ese inventario y puede sesgar la comparación; conservar controles de la misma comuna favorece soporte local, pero permite posibles desplazamientos hacia ellos.

Dentro de cada celda se calcula cuánto cambia la tasa entre generaciones en las escuelas con evento y se resta el cambio de los controles. Después se agregan las celdas con pesos de estudiantes tratados de la generación posterior. Las cuatro tasas descriptivas presentadas para el acceso primario agregado usan esos mismos pesos: su diferencia de cambios reconstruye el contraste salvo redondeo. Restar cambios no garantiza que ambos grupos hubieran seguido tendencias paralelas sin el evento (Roth et al. 2023).

## Incertidumbre, medición y límites

El remuestreo por escuelas usa 9.999 multiplicadores positivos y recalcula el estimador. Los intervalos primarios agregados son del 97,5 % para acceso en las dos eras, del 98,75 % para la familia de destinos y del 95 % para seguimiento. La heterogeneidad aplica el procedimiento de Holm (1979) dentro de familias predefinidas. Estos ajustes responden a familias distintas; no corresponde comparar la significación de dos filas como prueba de que sus efectos difieren.

La concentración en pocas escuelas limita la precisión, aunque haya muchos estudiantes. El número de estudiantes no reemplaza al de unidades escolares independientes. El diagnóstico de varianza por escuela y estudiante repetido mantiene el punto y arroja cocientes de varianza de **0,99861 a 1,00519** frente al agrupamiento escolar CR0 en los 16 resultados agregados. No corrige la fragilidad de pocos liceos; los ocho resultados modernos agregados llevan la bandera de precisión escolar débil.

Un identificador de estudiante inválido en el registro escolar o una asignación basal ambigua excluyen a la persona del estimando de identificación válida y deben quedar contados en la auditoría. Un identificador válido sin registro SIES puede representar ausencia **en el extracto**, pero no prueba que no hubo educación superior real. Las cotas de enlace utilizan capacidad agregada de registros con identificadores inválidos: no son tasas medidas de error de los grupos. Si resultan demasiado amplias para discriminar direcciones, se informa esa falta de información.

## Resultados y cobertura de los ocho desenlaces

La tabla usa **puntos porcentuales** y muestra las dos taxonomías por separado. Los intervalos de acceso de dos años son del 97,5 %; los de cuatro destinos, del 98,75 %; los de matrícula del año exacto, persistencia y titulación, del 95 %. No se deben comparar sus cruces con cero como una prueba de diferencia entre desenlaces.

| Desenlace | 2009–2015: contraste [intervalo] | 2016–2024: contraste [intervalo] |
|---|---:|---:|
| Matrícula observada en dos años | −2,31 [−5,26; +0,29] | −2,43 [−5,67; +1,27] |
| Matrícula en el año nominal exacto | −1,71 [−4,04; +0,17] | −2,10 [−5,56; +1,57] |
| Solo universidad en dos años | −2,07 [−4,18; −0,23] | +0,83 [−2,59; +3,88] |
| Solo IP/CFT en dos años | −0,31 [−2,97; +2,40] | −2,61 [−5,51; +1,00] |
| Ambos tipos en dos años | +0,07 [−0,33; +0,43] | −0,64 [−1,93; +0,18] |
| Ningún registro superior en dos años | +2,31 [−0,61; +5,58] | +2,43 [−1,68; +6,05] |
| Matrícula en al menos dos de tres años | −3,13 [−5,30; −1,20] | −1,90 [−5,01; +1,31] |
| Título de pregrado en seis años | −1,47 [−2,69; −0,28] | −2,28 [−5,56; +0,71] |
{: .table--compact .table--scroll}

La columna moderna indica la **taxonomía**, no que cada desenlace reúna todos los años 2016–2024: persistencia agrega cierres hasta 2023 y título hasta 2019. Para acceso de dos años, 2023 y 2024 aportan solo tercero medio. La variante de años comunes retiene únicamente años con soporte en **primero, segundo y tercero medio simultáneamente**: 2010–2015 y 2016–2022 para acceso, 2016–2021 para persistencia moderna y 2016–2017 para título moderno. Esa variante no es una estimación separada de "solo tercero" ni sustituye la serie completa.

Las cuatro categorías de destino comparten denominador y son exhaustivas; "ningún registro" es el complemento de acceso en dos años, no una confirmación independiente. Los intervalos históricos de solo universidad, persistencia y título son negativos en sus respectivos niveles de confianza; todos los modernos incluyen cero. La interpretación sigue siendo descriptiva: los intervalos no incorporan errores de clasificación, tendencias distintas ni enlaces incompletos. Las cotas conservadoras de capacidad de enlace para acceso abarcan **−80,95 a +74,03** puntos en la era histórica y **−71,70 a +66,18** en la moderna. Son demasiado amplias para defender un signo con esa información; no representan errores observados por brazo.

[Tabla accesible de comparaciones]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-comparison-table-es.html' | relative_url }}).

## Sensibilidades ejecutadas y límites de cada una

| Comparación predefinida | Resultado observado | Límite |
|---|---|---|
| Atributos escolares estables, controles de otra comuna y años con tres grados | Los 16 agregados por variante están estimados; acceso conserva punto negativo en ambas taxonomías. | Cambian población o comparador; coincidencia de signo no demuestra equivalencia ni ausencia de interferencia. |
| Estandarización de edad y género basales | Los 16 agregados están estimados; acceso moderno pasa de −2,43 a −1,59 puntos. | Exige soporte de las categorías presentes entre tratados; no atribuir la diferencia a un mecanismo individual. |
| Efectos fijos como diagnóstico | Los 16 agregados están estimados; acceso histórico −2,47 puntos [IC del 95 %: −4,85; −0,21], mientras el primario es −2,31 [IC del 97,5 %: −5,26; +0,29]. | El coeficiente usa otros pesos y responde otro estimando; los niveles de confianza también difieren. Dos intervalos con cruces distintos no son prueba formal entre ellos. |
| Controles sin D1 observado más D1 futuro, con dos horizontes | Los 16 agregados de cada horizonte están estimados y el acceso queda cercano al primario. | En **180 filas elegibles variante × desenlace × G × grado** de las dos variantes combinadas (76 y 104), no aportó ningún control D1 futuro; ahí la semejanza no prueba robustez frente a ese comparador. |
| Solo controles D1 futuro, con dos horizontes | 15/16 agregados bajo horizonte de desenlace y 16/16 bajo exposición escolar; el título moderno con horizonte de desenlace pierde soporte. | Cambian muestra y comparador; en varios resultados modernos hay menos de diez escuelas tratadas. La proyección preparada omite sus tasas por brazo y conteos exactos de personas; los puntos describen muestras distintas y mantienen precisión escolar débil. |
| Varianza de dos vías escuela×estudiante | Los 16 puntos agregados son idénticos al primario; el cociente de varianza escolar es 0,99861–1,00519. | La aproximación CR0 no resuelve pocos clústeres tratados ni identifica efectos. |
| Generaciones anteriores A y estrictamente previas B | A conserva las generaciones G−6/G−5 y G−7/G−6, aunque algunas ventanas llegan a G; B las mantiene y exige que **ambas** ventanas terminen antes de G. En acceso moderno G−6/G−5, A −3,12 [−5,24; −0,68] y B −2,28 [−5,09; +0,70] puntos. | B excluye primero medio y recalcula soporte/pesos; el cambio no mide sesgo por anticipación. Para título, las **96 filas de cobertura** de B (48 por variante, correspondientes a 48 combinaciones G × grado) llevan `NOT_ESTIMABLE_TEMPORAL_OVERLAP`, nunca cero. |
| Heterogeneidad por grado, dependencia, ruralidad y región | Se fijaron 800 pares: 388 estimables y 412 sin soporte o protegidos por privacidad. En 34, el p Holm es menor que 0,05. | Holm opera dentro de cada familia desenlace×era de 65 o 35 pruebas, no sobre las 800 juntas; acceso y ausencia duplican señales. No identifica perfiles causales ni autoriza publicar celdas subgrupales. |
{: .table--compact .table--scroll}

La persistencia moderna ilustra por qué importa conservar desenlaces además de acceso: en el placebo tardío A da **−2,41 puntos** [IC 95 %: **−4,50; −0,07**] para 2016–2024, aunque algunas ventanas alcanzan G. Con controles solo futuros bajo el horizonte del desenlace da **−10,02** [**−19,51; −0,81**] para 2016–2017 con **cuatro liceos tratados**; la titulación histórica de ese comparador da **+4,05** [**−0,64; +8,80**] para 2009–2014 con **27 liceos**. Cambian cohortes, pesos y comparadores; estos intervalos nominales del 95 % no prueban diferencias frente al primario, anticipación ni efectos causales. Cuatro liceos implican precisión escolar particularmente débil.

El inventario exhaustivo registra **4.992** estados de cobertura (`variante × desenlace × G × grado`), **2.200** estados de resultados de sensibilidades, **144** claves primarias y los **800** pares de heterogeneidad. La reconciliación conjunta pasó; una fila puede estar estimada sin intervalo anual, suprimida, censurada, sin soporte o excluida por ventana estricta. Ninguno de estos estados equivale a cero. La revisión combinada detectó restas posibles entre variantes y retiró conteos cruzables de la proyección preparada; un piso por fila aislada no bastaría.

La comprobación de factibilidad del estimador DR-DiD para cortes repetidos de Sant’Anna y Zhao (2020), previa al cálculo de efectos, examinó los 152 estratos históricos y los 72 modernos. Fallaron 39 y 29, respectivamente, por separación del modelo de pertenencia al grupo o porque alguna predicción requería combinaciones de características que el ajuste no podía sostener. Bajo la regla fijada, no se descartan esos estratos para estimar otra población: los ocho desenlaces de cada era quedan `NOT_ESTIMABLE_DRDID_DESIGN`. Es falta de estimabilidad con esta especificación, no un efecto nulo ni una evaluación de todos los métodos posibles. BLP/GATE/CLAN está `NOT_RUN_METHOD_NOT_IMPLEMENTED`: trabajo no ejecutado, distinto de una barrera empírica demostrada.

## Reproducibilidad y revisión retrospectiva

El protocolo fija decisiones para una reconstrucción auditable de datos ya estudiados; no constituye un prerregistro independiente. Se conservan código, hashes de archivos, cobertura y recibos de ejecución. El primario y las sensibilidades tienen recibos de producción; la conciliación de todas las claves pasó. La reproducción independiente de ambos agregados pasó. Esta concordancia numérica no valida por sí sola los supuestos causales ni la cobertura completa de las fuentes.

La revisión de privacidad combinada descartó la exportación íntegra de los agregados privados. La proyección preparada para difusión conserva cuatro tasas y conteos exactos de estudiantes solo para el acceso primario agregado de dos años en ambas eras; en los demás resultados conserva contrastes, intervalos, estados y conteos de escuelas, y retira tasas por brazo y conteos de personas. También conserva los motivos de ausencia y supresión. Estas exclusiones reducen las reconstrucciones por resta detectadas entre resultados, tablas y figuras de esta edición; no garantizan protección frente a todas las combinaciones posibles con información externa. Las cifras anteriores permanecen bajo custodia histórica y no se presentan como resultados de esta comparación.

## Referencias

- Holm, Sture. 1979. "A Simple Sequentially Rejective Multiple Test Procedure." *Scandinavian Journal of Statistics* 6 (2): 65–70. <https://www.jstor.org/stable/4615733>.
- Ministerio de Educación de Chile. s. f. "Matrícula por estudiante." Portal de Datos Abiertos. <https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/>. Los cortes y transformaciones locales de esta revisión constan en su protocolo; el portal no certifica por sí solo esos archivos.
- Roth, Jonathan, Pedro H. C. Sant’Anna, Alyssa Bilinski y John Poe. 2023. ["What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature."](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–2244. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)
- Sant’Anna, Pedro H. C. y Jun Zhao. 2020. ["Doubly Robust Difference-in-Differences Estimators."](https://doi.org/10.1016/j.jeconom.2020.06.003) *Journal of Econometrics* 219 (1): 101–122. Referencia del método evaluado por factibilidad; no se estimó aquí su efecto. [Scholar](https://scholar.google.com/scholar_lookup?title=Doubly+robust+difference-in-differences+estimators&doi=10.1016%2Fj.jeconom.2020.06.003)
- Servicio de Información de Educación Superior (SIES). s. f. "Bases de datos de estudiantes matriculadas y matriculados en Educación Superior en Chile" y "Base de datos de estudiantes tituladas y titulados en Educación Superior en Chile". Mi Futuro, Ministerio de Educación de Chile. <https://www.mifuturo.cl/bases-de-datos-de-matriculados/>; <https://www.mifuturo.cl/bases-de-datos-titulados/>. Los cortes locales de matrícula y titulación usados aquí están documentados por separado.
