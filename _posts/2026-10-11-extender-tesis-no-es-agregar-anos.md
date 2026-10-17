---
layout: single
classes: [thesis-extension-post]
title: "Extender mi tesis en 3 cucharadas (parte II): ¿mejora la educación cuando abren y cierran escuelas?"
subtitle: "Más evidencia sobre el recambio escolar, sus límites y las preguntas que deja para los sostenedores y los SLEP."
date: 2026-10-11 10:00:00 -0300
last_modified_at: 2026-10-17 13:40:00 -0300
categories: [datos, educacion, politica-publica]
tags: [educacion, mercado-escolar, cierre-escolar, mineduc, datos-administrativos, replicabilidad, simce, admision, slep, territorio]
description: "Una extensión de mi tesis examina cierres y aperturas escolares en Chile: qué muestran los registros y qué falta para evaluar calidad, cobertura y continuidad educativa."
excerpt: "Que una escuela cierre y otra abra no basta para saber si la educación mejoró. Los registros permiten precisar el recambio; sus efectos exigen mirar también a los estudiantes, los sostenedores y el territorio."
author: clabra
lang: es
ref: extender-tesis-no-es-agregar-anos
permalink: /datos/educacion/politica-publica/extender-tesis-no-es-agregar-anos/
header:
  teaser: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/og-1200x630.webp
  og_image_alt: "Escuelas en distintos estados y contornos superpuestos como metáfora de cierres y cambios en la oferta educativa."
  overlay_image: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/extender-tesis-no-es-agregar-anos/teaser-mobile-640x360.webp
visual_id: extender-tesis-no-es-agregar-anos
editorial_contract: societal-contribution-v1
table_contract: explicit-v1
math: false
toc: true
toc_sticky: true
comments: true
author_profile: true
distribution:
  social: false
  republish: []
  skip_reason: "Difusión pausada hasta verificar la URL pública y recibir autorización específica."
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
---

La [parte I]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) confirmó una tensión: ante cierres y aperturas, mover la oferta no dice si mejoraron las oportunidades de aprender. Esta parte pregunta qué ocurre cuando una escuela sale y otra entra.

<span id="claim-causal-boundary"></span>**Este análisis no identifica si el recambio mejora o empeora los resultados educativos.** No es una forma elegante de decir que el efecto sea cero. Algunas comparaciones son imprecisas; otras no reúnen casos comparables suficientes; y los registros no permiten seguir a cada estudiante ni reconstruir qué habría ocurrido sin el cierre o la apertura.

La parte I auditó 1992–2012. Aquí uso directorios de 2015 a 2025 para observar transiciones entre 2016 y 2025, y un panel 2013–2025 para detectar entradas. El período y las preguntas son distintos; no vuelvo a estimar los resultados de la parte I.

El registro contiene **900 cierres oficiales**, pero la definición estricta deja **330 cierres con matrícula**; las medianas caen antes del cierre sin revelar su causa; y, bajo el criterio territorial, solo **38 cierres** tienen una apertura cercana del mismo segmento. La cercanía no acredita cupos, accesibilidad ni destino. El aporte es una pregunta pública: **qué continuidad recibió la comunidad y quién absorbió sus costos**.

## Cucharada 1: antes de evaluar un cierre, hay que saber qué cambió

### Una salida del registro no siempre es una escuela que desaparece

En la primera entrega, «entrada» y «salida» describían apariciones y desapariciones en los archivos. Para estudiar el período reciente necesito distinguirlas de los cambios administrativos y de la interrupción efectiva de la oferta educativa.

Un establecimiento puede cerrar; entrar en receso; fusionarse con otro; cambiar de identificador; perder una sede o dejar de impartir un nivel. También puede cambiar de sostenedor —la entidad responsable de administrarlo— sin dejar de funcionar. Ninguna de esas situaciones debería convertirse automáticamente en la misma clase de cierre.

El **RBD**, identificador oficial del establecimiento, ayuda a seguir su historia, pero un código que desaparece exige revisar la escuela, la sede y la oferta. Los directorios comienzan en 2015 y la primera transición observable es de 2016. El caso de El Salvador, de 2013, se presenta aparte. El inventario cuenta eventos por RBD; las comparaciones reconstruyen establecimientos dentro de un segmento educativo.

**Ejercicio.** Separé un cierre real de un cambio administrativo. Definí como cierre oficial solo el paso desde un estado no cerrado al código `3`. Receso no es cierre; si un RBD desaparece del archivo, lo clasifico como salida desconocida.

<span id="claim-event-count"></span>**Resultado.** Hay **900 cierres oficiales**: 684 desde actividad, 215 desde receso y uno desde autorización sin matrícula. De las 684 escuelas antes activas, 346 tenían estudiantes y 338 ya registraban matrícula cero. Cerrar una escuela vacía no equivale a desplazar una comunidad escolar.
{: .text-justify}

Pero esos 346 tampoco son automáticamente 346 escuelas que desaparecieron. Al reconstruir identidad y oferta, quedan **330 cierres estrictos del establecimiento en el nivel que atendía**. Los otros 16 son cierres de sede o anexo, consolidaciones administrativas, reemplazos de RBD o casos no resueltos. Esos vínculos se infieren desde directorios oficiales y se excluyen de la comparación principal; otros cuatro candidatos a reemplazo en la misma sede se apartan solo del ejercicio espacial.
{: .text-justify}

### No toda oferta cercana atiende la misma necesidad

Una sala cuna no atiende la misma población que una escuela básica o un liceo. Separo educación inicial —sala cuna, nivel medio, transición y heterogéneo—, básica y media. Desde aquí, «mercado» significa **comuna y segmento educativo exacto**. Es una definición operativa, no una afirmación sobre dónde eligen las familias. Cobertura, además, exige distinguir matrícula de vacantes y accesibilidad.

<span id="claim-demography"></span>Según la proyección del [INE con base en el Censo 2024](https://www.ine.gob.cl/estadisticas-por-tema/demografia-y-poblacion/estimaciones-y-proyecciones-de-poblacion), la población de 6 a 17 años pasa de **3.081.791 en 2025** a **1.366.155 en 2050**: `55,7 %` menos. La cifra no incluye la educación parvularia y describe población, no matrícula ni cierres; sí obliga a planificar capacidad, transporte y continuidad por territorio.
{: .text-justify}

### Dónde entran los SLEP y la desmunicipalización

Los SLEP son sostenedores públicos de los establecimientos traspasados a su dependencia; no gobiernan toda la oferta comunal. La [Ley 21.040](https://www.bcn.cl/leychile/navegar?idNorma=1111237) regula el traspaso y la Dirección de Educación Pública publica su [calendario territorial](https://dep.gob.cl/calendario-de-traspaso/). Un traspaso no es la desaparición de una escuela si la comunidad continúa atendida, ni un evento anterior puede atribuirse al SLEP actual. Comparar administraciones exige poblaciones expuestas y períodos equivalentes: este panel describe eventos, no identifica el efecto de una modalidad de gestión.

## Cucharada 2: ¿se van las que rinden peor y llegan alternativas mejores?

### La matrícula permite reconocer una trayectoria, no explicar su causa

La comparación pregunta si las escuelas que cierran venían peor que alternativas similares. Cada cierre se contrasta con establecimientos del mismo año, comuna, segmento educativo, dependencia, ruralidad y tamaño. SIMCE se estandariza por año, grado y asignatura; PSU, PDT y PAES, dentro de su propio proceso.

<span id="claim-enrolment-path"></span>La matrícula entrega la señal más clara: de los 684 cierres que venían de actividad, 665 tienen tres años completos. **Las medianas de los tres años caen `28 → 23 → 1` estudiante.**

La secuencia describe tres cortes del conjunto, no la trayectoria de cada escuela. Tampoco permite saber si las familias se retiraron por dificultades educativas, por el anuncio de un cierre, por un traslado residencial o porque había menos niños en el territorio. Son explicaciones rivales por contrastar, no causas identificadas por estas medianas.

El desempeño tiene mucha menos cobertura:

| Trayectoria | Cierres con tres años | Cobertura sobre 684 | Medianas `t−3 → t−2 → t−1` |
|---|---:|---:|---|
| SIMCE | 76 | 11,1 % | `−0,232 → −0,235 → −0,083` |
| IVE-SINAE | 188 | 27,5 % | `0,882 → 0,910 → 0,946` |
{: .table--compact .table--numeric .table--scroll}

IVE-SINAE es un índice agregado de vulnerabilidad escolar, no pobreza individual.
{: .small}

### Lo que dicen —y lo que no dicen— los puntajes

<span id="claim-outcomes"></span>La tabla anterior describe el universo histórico amplio. La prueba estricta vuelve a filtrar anexos, cambios administrativos y segmentos distintos. De los 330 cierres elegibles, solo 97 tienen SIMCE y 46 admisión; después del emparejamiento exacto quedan **21 y 8**, respectivamente:

| Resultado | Estimación primaria | IC 95 % | Soporte |
|---|---:|---:|---:|
| SIMCE relativo | `+0,029` DE | `[−0,095; +0,158]` | 21 cierres |
| Puntaje núcleo de admisión, entre quienes rinden | `−0,001` DE | No estimable | 8 cierres |
{: .table--compact .table--scroll}

Entre escuelas comparables, SIMCE no muestra una diferencia precisa y admisión no alcanza el mínimo de diez cierres. Esto no dice que las escuelas que cierran estén sobre el promedio nacional: en el universo histórico amplio, la mediana SIMCE parte en `−0,232` DE. En los artefactos técnicos, `NOT_ESTIMABLE` no significa cero, empate ni igualdad; significa que publicar un intervalo defendible exigiría fingir más información de la disponible.
{: .text-justify}

El `−4,3 %` de la parte I, para particulares subvencionados que cierran, y el `+0,029` reciente no son comparables. El primero es la brecha respecto del promedio comunal en matemática de 4° básico para nueve años entre 1999 y 2011; el segundo usa desviaciones estándar anuales, cierres estrictos, la media entre `t−3` y `t−1` y controles exactos. Cambian período, unidad, universo y estimando; tampoco son comparables los signos.
{: .small}

El mínimo de diez es una regla retrospectiva para no ajustar el umbral a los signos observados; no es una ley estadística universal.

La sensibilidad no cambia la conclusión: SIMCE ponderado da `+0,034` DE `[−0,225; +0,289]` y admisión sigue bajo el mínimo. La señal preliminar desaparece al separar anexos y mercados; no prueba igualdad, sino dependencia de una definición laxa.
{: .text-justify}

### Un promedio puede cambiar sin que sepamos cuánto aprendieron los estudiantes

La contabilidad separa permanencia, redistribución y entradas o salidas. Un promedio puede subir al excluir un grupo con puntajes bajos sin que ese grupo mejore, o permanecer estable mientras cambian el acceso y los traslados.

## Cucharada 3: del promedio a la red educativa de cada territorio

### Qué pueden hacer los sostenedores con esta evidencia

La utilidad inmediata no es construir un ranking de escuelas que deberían cerrar. Es ordenar información antes de decidir si corresponde apoyar un establecimiento, ampliar su oferta, reorganizar una red o evaluar una fusión. Estas preguntas llevan a los mapas: no porque un mapa responda por sí solo, sino porque permite ver dónde una comparación agregada resulta insuficiente.

### Cómo leer los mapas sin convertir cercanía en reemplazo

La comparación territorial pregunta: ante un cierre estricto, ¿aparece cerca otra escuela que atiende el mismo segmento? Busqué una apertura dentro de 10 km y entre `t` y `t+2`. La ubicación del cierre corresponde a `t−1`; la ubicación de la entrada usa la **primera coordenada oficial válida entre el año de entrada y 2025**. Este criterio recupera registros tardíos sin fingir que la escuela estaba físicamente allí desde el primer año.

Uso «entrada» en un sentido operativo: actividad con matrícula positiva después de al menos dos años previos sin actividad registrada en el panel 2013–2025, sin episodio activo anterior en esa ventana ni sucesión registrada. No demuestra que la escuela sea históricamente nueva; puede quedar historia anterior fuera del panel. Para los eventos recientes, además, la ventana posterior todavía puede estar incompleta.

Para mostrar variedad sin elegir el resultado más llamativo, seleccioné **un caso por cada grupo educativo definido de antemano** y ordené por comuna, distancia, año y RBD. **Ni los valores ni la disponibilidad de resultados participaron en la selección**. Nueve trayectorias inestables se excluyen antes del emparejamiento y 259 entradas usan una coordenada informada con retraso.

<span id="claim-territorial"></span>De 330 cierres estrictos, 320 tienen coordenada válida. Entre 414 aperturas, 389 tienen una coordenada elegible bajo el criterio temporal. Se excluyen seis pares candidatos, correspondientes a cuatro cierres, del mismo año y a no más de 100 metros porque pueden ser reemplazos administrativos; exigir el mismo segmento excluye otras 420 combinaciones. Quedan **38 cierres emparejados con 29 aperturas únicas**. No hubo un par elegible de educación media. Los dos casos sistemáticos son descriptivos:

| Caso | Segmento | Cierre → apertura | Distancia | Qué permite ver |
|---|---|---|---:|---|
| Lo Barnechea | Transición inicial | 2016 → 2016 | 1,046 km | La apertura tiene su primera coordenada válida en 2019; muestra proximidad, no destino. |
| Lo Prado | Básica | 2016 → 2016 | 7,860 km | La apertura también se ubica con coordenada 2019 y queda fuera de la comuna del cierre. |
{: .table--compact .table--scroll}

La selección no afirma que estos ejemplos sean representativos del país. Hace una cosa más modesta: muestra cómo cambian las preguntas cuando se conserva segmento, año de la coordenada y regla de identidad. Un enlace espacial es una hipótesis de proximidad, no una trayectoria estudiantil ni una prueba de sustitución.
{: .text-justify}

{% include thesis-extension-stylized-evidence.html %}

<span id="claim-el-salvador"></span>Crecí en El Salvador; esa cercanía orienta preguntas, no explica el cierre. La Escuela N° 14 (RBD 391) cerró al terminar 2013 y se fusionó con la N° 1 (RBD 390). Los directorios 2008–2011 ubican la primera en **Diego Portales 500**; el [reglamento institucional](https://fees.cl/wp-content/uploads/2019/12/Reglamento-de-convivencia-2019-2020.pdf), la segunda en **Diego Portales 1510**. La [BCN](https://www.bcn.cl/laborparlamentaria/documento?id=636175) documenta el traspaso de primero a sexto básico.
{: .text-justify}

El punto MINEDUC 2015 de la N° 14 difiere 826 m del objeto OSM homónimo. El visor usa este último como **candidato histórico**, no como corrección: fue creado en 2022, no declara RBD y el [GeoJSON de contraste](/assets/data/thesis-extension-post2/viewer-coordinate-audit-v1.geojson) conserva ambos. Así, la distancia a la N° 1 es **aproximadamente 1,3 km**; con los puntos oficiales era 0,45 km.
{: .text-justify}

La matrícula conjunta de ambas escuelas cayó de **1.399 en 2004 a 977 en 2013** (`−30,2 %`). En 2014 la N° 1 pasó de 432 a 738 estudiantes, un salto compatible con la fusión documentada. La caída previa hace plausible una contracción demográfica, pero **no prueba que haya sido el motivo administrativo del cierre**; la intervención parlamentaria contemporánea también discutió hacinamiento y adecuaciones posteriores.
{: .text-justify}

¿Había menos niños, se desplazaron hogares mineros o creció otra oferta? La serie abre esas preguntas; no permite resolverlas por familiaridad.

El visor usa un mapa de calles OSM, coordenadas MINEDUC y, para la N° 14, un candidato histórico adjudicado que conserva el punto oficial como contraste. En los casos sistemáticos, la línea representa proximidad, no destino; en El Salvador representa la fusión documentada, no cada trayectoria individual. Son hechos estilizados para formular preguntas, no experimentos. Los paneles de salida y entrada son muestras separadas.
{: .small}

<span id="claim-new-schools"></span>Para las escuelas nuevas tampoco hay una respuesta concluyente. Los casos comparables por cohorte son `4/6/8` en SIMCE y `1/1/2` en admisión. Ninguna cohorte alcanza diez casos. Por eso el resultado es **no estimable bajo el criterio adoptado**: la base no permite determinar si rinden mejor o peor.
{: .text-justify}

<span id="claim-decomposition"></span>La contabilidad de cada mercado separa el cambio de las escuelas que continúan, la reasignación de matrícula y la entrada o salida oficial. El recambio aporta `−0,000105` DE en SIMCE, con IC 95 % `[−0,000346; +0,000103]`, y `+0,000113` en admisión, con IC 95 % `[+0,000027; +0,000213]`. El intervalo de admisión queda sobre cero entre quienes rinden; el de SIMCE cruza cero. Son identidades contables, no causas, y **no permiten respaldar causalmente la hipótesis de destrucción creativa**.
{: .text-justify}

### Cómo conversa este resultado con estudios anteriores

[Iocco (2024)](https://doi.org/10.2139/ssrn.4808834) sigue estudiantes desplazados en Chile: encuentra efectos medios cercanos a cero y mejores resultados cuando la escuela receptora rinde más. Es un preprint; su cierre por desaparición prolongada del RBD puede mezclar cierres, fusiones o cambios de identificador. [Grau, Hojman y Mizala (2018)](https://doi.org/10.1016/j.econedurev.2018.05.003), en cambio, estiman para estudiantes afectados aumentos de `1,8–2,5` puntos porcentuales en deserción de enseñanza media y de `3,9–4,4` puntos en repitencia de quinto básico. [Elacqua y colaboradores](https://doi.org/10.4067/S0718-52862012000200005) estudian las alternativas disponibles para quienes enfrentan un cierre. Sus unidades, períodos y diseños son distintos de este análisis descriptivo por escuela; por eso no se promedian ni se presentan como una contradicción automática.
{: .text-justify}

Este ejercicio distingue evento, entidad, anexo y segmento, observa la renovación espacial y extiende el panel hasta 2025. Sin trayectorias individuales no identifica destino, accesibilidad ni bienestar.
{: .text-justify}

### Qué sabemos sobre SAE y SLEP

<span id="claim-slep-sae"></span>Los calendarios escalonados de los Servicios Locales de Educación Pública (SLEP) y del Sistema de Admisión Escolar (SAE) parecen ofrecer comparaciones causales. En estos datos, sin embargo, ninguna de las dos cumple condiciones suficientes para atribuir un efecto.
{: .text-justify}

| Análisis | Hipótesis puesta a prueba | Resultado observado | Qué bloquea una lectura causal |
|---|---|---|---|
| SLEP sintético | El traspaso cambia matrícula u oferta respecto de territorios con trayectoria previa comparable. | **Ninguna de las 25** combinaciones territorio-horizonte cumplió el criterio de comparabilidad fijado en la especificación. | No hubo comparaciones sintéticas admisibles. Para cambios de calendario posteriores, el [*Informe Anual 2025* del Consejo Evaluador, pp. 35–36](https://educacionpublica.gob.cl/wp-content/uploads/2026/03/Informe-Anual-2025-Consejo-Evaluador-del-Sistema-de-Educacion-Publica.pdf#page=35), documenta ajustes caso a caso por avance de instalación, sostenibilidad y complejidad; no identifica el calendario de las cohortes aquí analizadas. |
| SLEP exploratorio | Condiciones basales predicen qué territorios se traspasan antes y la cercanía entre redes puede contaminar comparaciones. | Tres condiciones basales no mostraron capacidad predictiva distinguible del azar: AUC con validación cruzada `0,53`, `p=0,22` de permutación. En 53 de 70 territorios existe al menos otro SLEP respecto del cual 20 % o más de sus escuelas queda, en distancia lineal, a 20 km o menos de alguna escuela de ese SLEP. | No detectar selección observada no demuestra que el calendario sea aleatorio; la geometría muestra interferencia potencial, no un efecto derrame observado. |
| SAE, triple diferencia | En 2018 cambia la concentración en dos de los grados de entrada —1° y 7° básico— frente a grados aún diferidos, de forma distinta en cuatro regiones que ingresaron ese año que en diez regiones de control. | HHI `+0,0035` `[−0,0104; +0,0174]`; log del número efectivo de escuelas `−0,0042` `[−0,0265; +0,0181]`. | Con la ponderación principal, igual por comuna-grado, pasan 4 de 4 equivalencias previas; con peso igual por región histórica fallan ambos resultados en 2016–2017, el período inmediatamente anterior. Solo hay cuatro regiones tratadas y no se descartan efectos entre grados. |
{: .table--compact .table--scroll}

Estos resultados no permiten concluir que los SLEP y el SAE no tuvieron efectos. En SLEP, ninguna comparación cumplió las condiciones necesarias para estimarlos. En SAE, ambos intervalos de 95 % —*jackknife* eliminando una de 14 regiones históricas a la vez— incluyen cero y valores de ambos signos. Con solo cuatro regiones tratadas, la cobertura nominal de 95 % es aproximada y, sin identificación, no acota el efecto de la política. La base permite diagnosticar los límites del diseño, no evaluar ninguna de las dos políticas.
{: .text-justify}

En SLEP, una próxima evaluación sería causalmente más informativa si documentara antes del traspaso los criterios que fijan el orden de ingreso, acumulara más territorios tratados y midiera interferencia, destinos estudiantiles, accesibilidad y resultados. En SAE, cuyo despliegue ya terminó, ampliar la ventana obliga a combinar cohortes posteriores con menos regiones aún no tratadas o a construir otro contraste, por ejemplo a partir de una regla de asignación defendible. Estas condiciones fortalecerían, sin garantizar, una lectura causal de **estos diseños**; mientras no se cumplan, sus resultados son señales exploratorias, no impactos.
{: .text-justify}

## Qué puede usar la política pública

<span id="claim-policy-use"></span>Este análisis sirve como **apoyo a la decisión**, no como una regla para cerrar, fusionar, abrir u ordenar escuelas en un ranking. La secuencia prudente es **observación → diagnóstico → decisión**. Una baja de matrícula o la cercanía de otra escuela justifican un diagnóstico; no bastan para decidir un cierre.
{: .text-justify}

| Momento de la decisión | Señal que aporta este análisis | Evidencia adicional indispensable | Uso prudente |
|---|---|---|---|
| Validar el evento | Distingue cierre, anexo, fusión, cambio de RBD y segmento. | Resoluciones, continuidad del principal y oferta por nivel. | Solicitar la corrección a quien mantiene el registro; no contar automáticamente una desaparición. |
| Diagnosticar matrícula decreciente | Muestra trayectoria, actividad y diferencias territoriales. | Población por edad, movilidad residencial, transferencias, competencia, capacidad y anuncios previos. | Activar diagnóstico y apoyo; no usar un umbral de matrícula como regla de cierre. |
| Planificar la transición o la red | Separa niveles y advierte que cercanía no equivale a sustitución. | Vacantes reales, accesibilidad y tiempos de viaje, destinos, apoyos, participación y continuidad pedagógica. | Preparar escenarios y un plan de transición; no presumir que la alternativa del directorio es utilizable. |
| Evaluar resultados | Define denominadores, muestras y límites de comparación. | Seguimiento de estudiantes y un contrafactual creíble. | Medir productos, resultados e impacto por separado; no atribuir aprendizaje, equidad o bienestar al cierre sin identificación causal. |
{: .table--compact .table--scroll}

Un SLEP planifica y gestiona **su propia red**, no los establecimientos de otros sostenedores. La [Ley 21.040, artículo 18, letras c y t](https://www.bcn.cl/leychile/navegar?idNorma=1111237) le encarga desarrollar la oferta pública, velar por cobertura y continuidad, y apoyar permanencia y revinculación. MINEDUC ejerce la rectoría; la Dirección de Educación Pública conduce estratégicamente el sistema. El [Plan Anual Local 2026](https://dep.gob.cl/pal-2026/) organiza apoyo, infraestructura y dotaciones según cursos y matrícula. Nada de ello entrega autoridad sobre otros sostenedores ni demuestra la superioridad de una modalidad de gestión.
{: .text-justify}

Dos errores importan. Un **falso positivo** declararía inviable una escuela que aún asegura acceso; un **falso negativo** omitiría una transición riesgosa porque la matrícula agregada parece estable. IVE-SINAE describe composición escolar agregada; no identifica pobreza individual ni decide dónde intervenir.
{: .text-justify}

La teoría de cambio enlaza **insumos** —eventos válidos, demografía, capacidad y destinos— con diagnóstico y apoyo, planes de transición, continuidad, asistencia y retención, hasta aprendizaje y equidad. Supone vacantes reales, traslados sin deterioro de acceso y participación comunitaria. **Este post propone evaluar esa cadena; no acredita que funcione.**
{: .text-justify}

## Qué tendría que ocurrir para hablar de causalidad

Un resultado causal exige algo más ambicioso que acumular años. Para los cierres, hace falta seguir a los estudiantes, conocer sus destinos y comparar sus trayectorias con las de un grupo creíble antes de que las familias anticipen el cambio. Para SLEP, se necesita documentar por qué cada territorio fue traspasado en cierta fecha, disponer de más unidades tratadas y medir la interferencia entre redes cercanas. Para SAE, una ventana más larga no resuelve por sí sola los pocos conglomerados tratados ni los placebos sensibles a la ponderación: se requiere otro contraste, apoyado en una regla de asignación defendible.

Cada ruta puede fallar. Tendencias previas incompatibles invalidan un estudio de eventos; una discontinuidad exige una regla no manipulable; una variable instrumental requiere una primera etapa clara y una exclusión creíble; y el seguimiento individual puede sesgarse si los enlaces fallan de forma selectiva. Declarar estas condiciones antes de estimar es parte del resultado, no una formalidad.

La proyección demográfica vuelve urgente construir escenarios territoriales de apoyo, expansión, reorganización y resguardo de capacidad. No entrega un calendario de cierres: un descenso nacional puede coexistir con barrios que necesitan escuelas nuevas. Un futuro artículo debería unir demografía local, oferta por nivel, vacantes, tiempos de viaje y trayectorias estudiantiles. Su producto útil no sería una lista de establecimientos destinados a cerrar.

<details class="technical-disclosure" markdown="1">
<summary>Nota técnica y controles de robustez</summary>

Esta sección conserva las cifras necesarias para auditar el ejercicio sin convertir el relato principal en un registro de ejecución.

**Cobertura.** El registro de identidad reunió 14 alias oficiales y dos sucesiones temporales candidatas; no acredita que toda recodificación posible esté detectada. La muestra varía por dependencia, ruralidad y región, de modo que los resultados describen los casos observados y no un efecto poblacional nacional.

**SLEP.** Ninguna de las 25 combinaciones territorio-horizonte reunió al menos diez territorios elegibles, tres donantes efectivos y los ajustes pretratamiento definidos. El diagnóstico exploratorio distingue 26 territorios traspasados al 31 de diciembre de 2025 y 44 aún no traspasados. Con tres condiciones basales, la AUC fue `0,5341` y el valor `p=0,2195` en 1.999 permutaciones: no se detectó una predicción distinta del azar, pero eso tampoco demuestra asignación aleatoria. En 53 de 70 territorios, al menos 20 % de sus escuelas queda a 20 km o menos de una escuela de otro SLEP; es geometría compatible con interferencia, no evidencia de un efecto derrame.

**SAE.** La triple diferencia 2017–2018 compara 1° y 7° básico con grados diferidos, entre cuatro regiones que ingresaron en 2018 y diez aún no tratadas. La [guía de MINEDUC](https://www.mineduc.cl/wp-content/uploads/sites/19/2018/01/guia-informativa.pdf) confirma esa secuencia. La inferencia usa *jackknife* sobre 14 regiones históricas. HHI da `+0,003513` `[−0,010368; +0,017395]`; el log del número efectivo de escuelas, `−0,004192` `[−0,026491; +0,018106]`. Los cuatro placebos principales cumplen el margen definido, pero la ponderación histórica solo aprueba dos de cuatro. Con cuatro regiones tratadas, resultados sensibles y posibles efectos entre grados, la comparación sigue siendo exploratoria.

**Resultados y sensibilidad (MR1 y MR2).** SIMCE da `+0,029` DE `[−0,095; +0,158]` con 21 cierres; la variante ponderada da `+0,034` `[−0,225; +0,289]`. Admisión queda `NOT_ESTIMABLE` con ocho cierres. Las entradas también quedan `NOT_ESTIMABLE`: los casos comparables por cohorte son 4/6/8 en SIMCE y 1/1/2 en admisión. El mínimo de diez se fijó en un protocolo retrospectivo; se declara como una limitación y no como una ley universal.

**Descomposición y mercados.** La rotación oficial aporta `−0,000105` `[−0,000346; +0,000103]` en SIMCE y `+0,000113` `[+0,000027; +0,000213]` en admisión. El residuo de la identidad contable es menor que `1e−10`; ese cierre aritmético no convierte los componentes en causas. La sensibilidad espacial H1 compara posiciones relativas de concentración bajo seis vecindarios con la definición comunal: ninguna banda excluye cero y sus umbrales no son reglas de política.

**Territorio y reproducibilidad.** El ejercicio conserva 38 cierres y 29 aperturas únicas; excluye nueve trayectorias inestables y registra 259 entradas con coordenada tardía. La auditoría nacional distingue 12.038 establecimientos funcionando y 78 autorizados sin matrícula. OSM es una fuente secundaria y el producto público conserva solo agregados. R produjo los agregados y 999 réplicas *bootstrap*; Python reconcilió 112 celdas públicas con una diferencia menor que `1e−10`. El acuerdo entre implementaciones reduce errores de cálculo, no resuelve la identificación causal.

</details>

## Cierre: evaluar la transición, no celebrar el movimiento

Extender la tesis reveló que «cierre» escondía recuentos acumulados, eventos, escuelas vacías, anexos y reemplazos de RBD; «mercado» mezclaba sala cuna, básica y media; «renovación» confundía cercanía con destino.
{: .text-justify}

La hipótesis de destrucción creativa es atractiva; por eso hay que exigirle una prueba estricta. Hoy hay señales, vacíos y presión demográfica, pero **este análisis no aporta evidencia para celebrar el recambio**.
{: .text-justify}

<span id="claim-open-question"></span>La rotación administrativa observada existe. Lo que todavía falta saber es quién conserva continuidad y quién termina pagando la transición.
{: .text-justify}

### Transparencia y alcance de las fuentes

La tesis y su extensión son de mi autoría; no constituyen una réplica independiente. También fui coautor de [*Destructive Creation* (DT 396, 2014)]({{ '/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf' | relative_url }}), antecedente del artículo de Grau, Hojman y Mizala (2018) citado aquí. El Salvador fue seleccionado por mi vínculo biográfico con la localidad. Hacer explícitas estas relaciones permite reconocer posibles sesgos de confirmación y selección.

No recibí financiamiento para este trabajo y declaro no tener conflictos de interés. Mi única afiliación institucional es el Ministerio de Desarrollo Social y Familia de Chile, que no financió, encargó, supervisó ni revisó este trabajo; sus posiciones no están representadas por estas conclusiones. Utilicé asistentes de inteligencia artificial para apoyar programación, control de calidad, revisión de prosa y revisión adversarial. Las decisiones metodológicas y editoriales, la verificación de fuentes y la responsabilidad por todas las afirmaciones y resultados son mías.
{: .text-justify}

---

## Referencias

<div class="post-references" markdown="1">

Chay, K. Y., McEwan, P. J., & Urquiola, M. (2005). [The central role of noise in evaluating interventions that use test scores to rank schools](https://doi.org/10.1257/0002828054825529). *American Economic Review, 95*(4), 1237–1258.

Elacqua, G., Martínez, M., Santos, H., & Urbina, D. R. (2012). [School closures in Chile: Access to quality alternatives in a school choice system](https://doi.org/10.4067/S0718-52862012000200005). *Estudios de Economía, 39*(2), 179–202.

Grau, N., Hojman, D., & Mizala, A. (2018). [School closure and educational attainment: Evidence from a market-based system](https://doi.org/10.1016/j.econedurev.2018.05.003). *Economics of Education Review, 65*, 1–17.

Hsieh, C.-T., & Urquiola, M. (2006). [The effects of generalized school choice on achievement and stratification](https://doi.org/10.1016/j.jpubeco.2005.11.002). *Journal of Public Economics, 90*(8–9), 1477–1503.

Iocco, M. P. (2024). [Impact of planned school closures on academic performance: Evidence from Chile](https://doi.org/10.2139/ssrn.4808834). *SSRN preprint*.

Paredes, R. D., & Fresard, M. (2018). [Voucher y cierre de escuelas en Chile](https://doi.org/10.38178/cep.vi151.62). *Estudios Públicos*, (151).

Quintero-Fragozo, C., Cortés, Y., & Sarrias, M. (2023). [Effects of spatial competition on public educational efficiency](https://doi.org/10.1080/02680939.2021.1966102). *Journal of Education Policy, 38*(1), 115–140.

Taghizadeh, J. L. (2020). [Effects of school closures on displaced students and future cohorts](https://doi.org/10.1016/j.labeco.2020.101910). *Labour Economics, 67*, 101910.

</div>
