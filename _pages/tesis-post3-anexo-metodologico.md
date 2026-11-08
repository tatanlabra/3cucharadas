---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Anexo de la parte III: definiciones y trazabilidad de las trayectorias escolares"
description: "Especificación complementaria, cobertura y límites de la comparación de trayectorias escolares."
permalink: /datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/anexo-metodologico/
ref: tesis-post3-anexo-metodologico
lang: es
author: clabra
author_profile: true
math: true
toc: true
toc_sticky: true
table_contract: explicit-v1
last_modified_at: 2026-11-07 21:00:00 -0300
published: true
f2_complete: true
publication_authorized: true
scientific_status: DESCRIPTIVE_ONLY
readiness: READY_FOR_PUBLICATION
---

<!-- SCIENTIFIC_STATUS: DESCRIPTIVE_ONLY; READINESS: READY_FOR_PUBLICATION; F2_COMPLETE: true; PUBLICATION_AUTHORIZED: true. -->

{% include thesis-series-nav.html current=3 %}

El [artículo principal]({{ '/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/' | relative_url }}) explica la pregunta, la comparación y sus límites en cada cucharada. Este anexo permite revisar las decisiones técnicas y la cobertura sin convertirlas en requisitos para entender el relato. Todas las estimaciones de esta revisión son descriptivas: una asociación ajustada no acredita un efecto causal.

## Qué representa un evento

El año **G** identifica una pérdida de oferta inferida de registros, no una resolución jurídica de cierre. La clasificación de 2005–2015 utiliza desaparición sin reaparición observada hasta 2025 y revisión de flujos; la de 2016–2024 incorpora además información anual de estado e identidad del establecimiento. Esa diferencia documental impide interpretar ambas eras como una sola exposición homogénea. La clasificación histórica utiliza información posterior a G; no es una regla que hubiera podido aplicarse en tiempo real con los datos disponibles entonces.

La evidencia chilena sobre cierre y movilidad escolar (Grau et al. 2018) y sobre alternativas cercanas para familias vulnerables (Elacqua et al. 2012) aporta contexto, pero no identifica el contraste de esta serie.

La regla más amplia, D1, y la depurada por flujos, D2, permiten examinar la sensibilidad a la definición. En el inventario histórico entregan los mismos episodios: compararlas allí no constituye una prueba discriminante. En la era moderna sí difieren. Una concentración de traslados es una señal para revisar continuidad de oferta, no corroboración institucional de una fusión o un cierre.

## Población y comparación

La unidad es una observación **estudiante–cohorte**, con matrícula inicial en la escuela de origen en G−1. Una persona puede aparecer en más de una cohorte de referencia; por eso los conteos acumulados no son necesariamente personas distintas. Se excluyen asignaciones basales ambiguas y se conserva su diagnóstico de cobertura.

| Decisión | Comparación principal |
|---|---|
| Características de pareo | Año del evento, región, dependencia, ruralidad, código de enseñanza, curso, género y edad basales. |
| Soporte mínimo por celda y desenlace | Al menos un estudiante tratado y cinco controles, con una escuela tratada y dos de control. Son umbrales computacionales, no garantías de identificación. |
| Selección de controles | Primero se depura la elegibilidad; después se aplica un máximo de veinte controles por tratado con orden determinista. |
| Exposición local | Se excluyen controles de la misma comuna y nivel educativo; se examina su reincorporación como sensibilidad. |
| Cierres posteriores | Un evento propio del control dentro de la ventana del desenlace lo excluye; la regla depende del inventario y del calendario, no del resultado del estudiante. |
| Ponderación | Dentro de cada era, las celdas pesan según estudiantes tratados con desenlace clasificable. Los pesos iguales por cohorte son una sensibilidad distinta. |
{: .table--compact .table--scroll}

No encontrar una celda comparable reduce la población a la que responde el contraste. No se amplían las reglas de pareo después de mirar el signo para recuperar resultados preferidos.

La literatura tampoco fija un signo universal: Engberg et al. (2012) describen una diferencia negativa inicial de asistencia entre estudiantes desplazados que desaparece tras el primer año en su nueva escuela, y no detectan efectos adversos entre estudiantes de escuelas receptoras en su contexto; Brummet (2014) encuentra efectos receptores modestos; Beuchert et al. (2018) documentan pérdidas de corto plazo tras consolidaciones danesas. Ninguno de esos diseños valida el pareo de este ejercicio.

## Dos desenlaces que no son intercambiables

| Desenlace | Población inicial | Observación posterior | Qué no demuestra |
|---|---|---|---|
| Ausencia de progresión observada | Primero básico a segundo medio | En G+1 no aparece matrícula enlazable, o el grado interpretable es menor al basal más dos cursos. | No distingue por sí solo atraso efectivo, salida de cobertura y otras trayectorias. |
| Dos años sin matrícula observada | Primero básico a primero medio | No aparece registro válido en ninguno de G+1 y G+2. | No acredita abandono escolar. |
{: .table--compact .table--scroll}

Si existe matrícula pero el grado es desconocido o discordante, la progresión queda desconocida: no se convierte en fracaso ni en ausencia. Para el segundo desenlace, cualquier matrícula enlazable en cualquiera de los dos años acredita presencia. La cohorte 2024 tiene seguimiento para progresión, pero no para completar G+2; esa frontera se registra como seguimiento incompleto.

## Incertidumbre y datos que faltan

El contraste principal resta niveles posteriores ajustados; no es una diferencia en diferencias. La incertidumbre se calcula con 9.999 remuestreos por multiplicadores escolares positivos. Cada escuela recibe el mismo peso aleatorio en todas sus apariciones; se recalculan niveles y ponderaciones conservando estudiantes y celdas elegibles. Agrupar por escuela reconoce que estudiantes de un mismo establecimiento comparten circunstancias; no elimina sesgos de selección o medición.

Los cuatro contrastes agregados —dos desenlaces por dos eras— usan intervalos nominales del 98,75 %, ajustados por esa familia. Los intervalos anuales son del 95 % y cumplen una función descriptiva. Pocos establecimientos, concentración del alumnado o dependencia adicional entre estudiantes exigen advertencias y sensibilidades; un intervalo que contiene cero no prueba equivalencia.

Una **cota** responde otra pregunta. Asignar a los grados desconocidos avance o falta de avance delimita qué valores son compatibles con esa información incompleta, manteniendo la población definida para la cota. No es un intervalo de confianza. Para escolarización real fuera del panel, la ausencia administrativa tampoco identifica el estado verdadero: los límites deben reconocer esa incertidumbre adicional.

Esta es una aplicación de identificación parcial (Manski 2003): las cotas dependen de las asignaciones extremas declaradas, no de una distribución inferida de los estados faltantes.

## Comprobaciones complementarias

El indicador previo compara matrícula de G−2 a G−1. Su población inicial es distinta de la del contraste principal y sus tasas no están ajustadas: describe una señal previa, no identifica anticipación ni corrige automáticamente el resultado posterior.

{% assign reset_figure = site.data.tesis_reset_figures["post3-anticipation-persistent_nonenrollment_two_years-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset/anticipation" %}

{% assign reset_figure = site.data.tesis_reset_figures["post3-anticipation-persistent_nonenrollment_two_years-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post3/scientific-reset/anticipation" %}

El diagnóstico de cohortes simétricas compara generaciones basales G−4 y G−1 con iguales horizontes relativos. Distingue una brecha posterior de una diferencia entre cambios, pero requiere supuestos adicionales para cualquier lectura causal. Asistencia y notas se analizan únicamente entre registros válidos observados; sus unidades y tasas de observación se informan por separado.

### Hasta dónde llevan las comprobaciones

Estas pruebas responden preguntas distintas y no se deben sumar ni restar entre sí. Los límites siguientes mantienen la población basal antes de excluir información desconocida; por eso no tienen por qué encerrar los puntos estimados en la muestra con desenlace clasificable. "Puntos" significa **puntos porcentuales**, salvo en la tabla de notas.

| Pregunta y población | 2005–2015 | 2016–2024, o 2016–2023 si requiere G+2 | Lectura permitida |
|---|---:|---:|---|
| Falta de progresión con grado desconocido, población basal fija | +6,00 a +12,90 | +3,02 a +7,19 | Cotas de información faltante, sin intervalo estadístico propio. |
| No escolarización real con matrícula fuera del panel desconocida, población basal fija | −2,82 a +4,76 | −1,76 a +2,89 | Ambos signos siguen siendo compatibles; "sin registro" no equivale a abandono. |
| Igual peso por cohorte: falta de progresión | +10,09 | +5,06 | Sensibilidad puntual, sin intervalo propio. |
| Igual peso por cohorte: dos años sin registro | +2,08 | +0,88 | Sensibilidad puntual, sin intervalo propio. |
{: .table--compact .table--scroll}

El diagnóstico entre generaciones simétricas necesita observar una cohorte anterior completa: por ello comienza en **2008**, no en 2005, en la era histórica. En la tabla siguiente, el primer intervalo procede de 9.999 multiplicadores por escuela; el segundo incorpora dependencia por escuela y estudiante mediante una aproximación asintótica. Ambos son nominalmente del 95 %. La advertencia de precisión débil para el segundo se conserva en las cuatro filas.

| Desenlace y era | Diferencia entre brechas | Intervalo escolar | Intervalo escuela y estudiante |
|---|---:|---:|---:|
| Falta de progresión, 2008–2015 | +4,36 | +2,07 a +8,60 | +0,90 a +7,81 |
| Falta de progresión, 2016–2024 | +0,40 | −1,74 a +2,50 | −1,78 a +2,58 |
| Dos años sin registro, 2008–2015 | +0,45 | −0,30 a +1,23 | −0,31 a +1,20 |
| Dos años sin registro, 2016–2023 | +0,28 | −0,47 a +1,14 | −0,49 a +1,05 |
{: .table--compact .table--scroll}

El primer intervalo histórico de progresión no cruza cero; eso tampoco convierte el ejercicio en un efecto causal. La selección previa ya observada y los supuestos entre generaciones siguen abiertos. Las cifras de esta tabla tienen otro estimando y, en la era histórica, otra ventana: restarlas a los contrastes principales no cuantifica cuánto de la brecha fue "explicado".

La ampliación D1 de la clasificación de eventos no discrimina nada en el inventario histórico: sus banderas coinciden con D2. En la era moderna, los contrastes completos pasan de **+4,98 a +1,88 puntos** para falta de progresión y de **+1,13 a +0,33** para dos años sin registro. Con las observaciones comunes, D1 y D2 dan respectivamente **+4,96** y **+1,11 puntos** en ambos métodos: comparten exposición y desenlace, de modo que la igualdad es mecánica. La diferencia entre muestras completas mezcla composición y soporte y carece de intervalo conjunto. Los resultados de controles locales y tres filtros de escuelas receptoras quedan reservados por privacidad de grupos pequeños; su reserva no implica resultado nulo ni robustez. El filtro de escuela receptora selecciona una condición posterior al evento.

### Asistencia y notas entre estudiantes observados

Aquí la pregunta es el cambio entre G−1 y G+1 de quienes tienen **ambos** registros válidos. La tasa de casos completos se publica en bandas de cinco puntos porcentuales porque los conteos precisos correlacionados entre métricas y cohortes permitirían reconstruir grupos pequeños. Entre tratados, esa tasa es **65–70 %** en 2005–2015 y **70–75 %** en 2016–2024; entre controles, **85–90 %** y **90–95 %**, respectivamente. La selección entre brazos impide generalizar estos resultados a todos los estudiantes basales.

| Medida condicionada a observación | 2005–2015, diferencia e IC 95 % | 2016–2024, diferencia e IC 95 % | Unidad |
|---|---:|---:|---|
| Asistencia | −0,31 [−0,73; +0,12] | −2,13 [−4,89; −0,08] | Puntos porcentuales de asistencia. |
| Nota promedio | −0,092 [−0,114; −0,068] | −0,041 [−0,093; +0,014] | Puntos de nota en escala 1–7. |
{: .table--compact .table--scroll}

Los intervalos escolares son exploratorios y describen solo casos completos. El análisis de asistencia que excluye ceros se calculó, pero sus estimaciones se suprimen por un grupo pequeño; no se reemplazan por cero. Las ventanas anterior, coincidente y posterior a la pandemia son contexto exploratorio, sin contraste formal entre periodos ni prueba de un efecto pandémico.

## Versiones y resguardo

Esta reconstrucción es retrospectiva: ya existían análisis de la misma población. El protocolo y sus enmiendas permiten auditar decisiones, pero no constituyen un prerregistro independiente. Se conservan los resultados anteriores bajo custodia; no se mezclan sus cifras con esta revisión.

Las descargas públicas deben contener solo agregados revisados, sin identificadores y sin celdas pequeñas reconstruibles mediante diferencias entre tablas. Una supresión por privacidad conserva su motivo; no equivale a un cero ni a ausencia de soporte estadístico.

## Referencias

- Beuchert, Louise, Maria Knoth Humlum, Helena Skyt Nielsen y Nina Smith. 2018. ["The Short-Term Effects of School Consolidation on Student Achievement: Evidence of Disruption?"](https://doi.org/10.1016/j.econedurev.2018.05.004) *Economics of Education Review* 65: 31–47. [Scholar](https://scholar.google.com/scholar_lookup?title=The+short-term+effects+of+school+consolidation+on+student+achievement%3A+Evidence+of+disruption%3F&doi=10.1016%2Fj.econedurev.2018.05.004)
- Brummet, Quentin. 2014. ["The Effect of School Closings on Student Achievement."](https://doi.org/10.1016/j.jpubeco.2014.06.010) *Journal of Public Economics* 119: 108–124. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effect+of+school+closings+on+student+achievement&doi=10.1016%2Fj.jpubeco.2014.06.010)
- Elacqua, Gregory, Matías Martínez, Humberto Santos y Daniela Urbina. 2012. ["School Closures in Chile: Access to Quality Alternatives in a School Choice System."](http://www.scielo.cl/pdf/ede/v39n2/art05.pdf) *Estudios de Economía* 39 (2): 179–202. [DOI](https://doi.org/10.4067/S0718-52862012000200005) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closures+in+Chile%3A+Access+to+quality+alternatives+in+a+school+choice+system&doi=10.4067%2FS0718-52862012000200005)
- Engberg, John, Brian Gill, Gema Zamarro y Ron Zimmer. 2012. ["Closing Schools in a Shrinking District: Do Student Outcomes Depend on Which Schools Are Closed?"](https://doi.org/10.1016/j.jue.2011.10.001) *Journal of Urban Economics* 71 (2): 189–203. [Scholar](https://scholar.google.com/scholar_lookup?title=Closing+schools+in+a+shrinking+district%3A+Do+student+outcomes+depend+on+which+schools+are+closed%3F&doi=10.1016%2Fj.jue.2011.10.001)
- Grau, Nicolás, Daniel A. Hojman y Alejandra Mizala. 2018. ["School Closure and Educational Attainment: Evidence from a Market-Based System."](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf) *Economics of Education Review* 65: 1–17. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)
- Manski, Charles F. 2003. [*Partial Identification of Probability Distributions*](https://doi.org/10.1007/b97478). Springer. [Scholar](https://scholar.google.com/scholar_lookup?title=Partial+Identification+of+Probability+Distributions&doi=10.1007%2Fb97478)
- Ministerio de Educación de Chile. s. f. "Matrícula por estudiante." Portal de Datos Abiertos. <https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/>. Los cortes y transformaciones locales de esta revisión constan en su protocolo; el portal no certifica por sí solo esos archivos.
