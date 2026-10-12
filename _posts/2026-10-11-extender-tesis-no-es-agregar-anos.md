---
layout: single
classes: [thesis-extension-post]
title: "Extender mi tesis en 3 cucharadas II: ¿mejora la educación cuando abren y cierran escuelas?"
subtitle: "Más evidencia sobre el recambio escolar, sus límites y las preguntas que deja para los sostenedores y los SLEP."
date: 2026-10-11 10:00:00 -0300
last_modified_at: 2026-10-12 09:10:31 -0300
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

En el [primer post]({{ '/datos/educacion/politica-publica/replica-tesis-establecimientos-educacionales/' | relative_url }}) volví sobre mi tesis de 2014 antes de extenderla. **Este análisis no identifica efectos causales.** Sobrevivieron dos hallazgos importantes para 1992–2012: hubo una reducción neta de establecimientos municipales y una expansión neta de particulares subvencionados; y, en el universo reconstruido del Gran Santiago, quienes después salían del registro atendían una matrícula más vulnerable. También encontré errores que cambiaban algunas interpretaciones. No bastaba con añadir años a las mismas tablas.

Esta segunda entrega retoma una pregunta pendiente: **¿qué significa que una escuela salga del sistema y otra entre?** Para quienes trabajan en educación, importa saber si ese movimiento amplía las oportunidades de aprender, reorganiza una oferta que ya no responde al territorio o interrumpe una trayectoria que necesitaba apoyo, no un traslado.

La intuición de que salen las escuelas de menor desempeño y llegan alternativas mejores merece examinarse. Pero no debe convertirse en la respuesta antes de mirar los datos. Con el análisis disponible **no pude establecer si el recambio observado mejora o empeora sistemáticamente los resultados educativos**. Eso no demuestra que sus efectos sean nulos: hay comparaciones imprecisas, otras sin información suficiente y, sobre todo, falta seguir a los estudiantes y construir el contrafactual —qué habría ocurrido sin el cierre o la apertura—.

Estos datos no identifican el efecto causal de abrir o cerrar escuelas. Sí permiten precisar los eventos, examinar sus trayectorias y terminar en el territorio: allí donde una apertura, una fusión o un cierre deja de ser una fila y cambia las alternativas de una comunidad.

## Seis respuestas antes del método

| Pregunta | Resultado | Qué podemos decir |
|---|---|---|
| ¿Cuántos cierres hubo? | **900 transiciones oficiales** entre 2015 y 2025; 330 son cierres estrictos con matrícula para este ejercicio. | `37.818` es el stock cerrado repetido año a año, no 37.818 cierres. |
| ¿Cierran las de peor rendimiento? | SIMCE `+0,029` DE, IC 95 % `[−0,095; +0,158]`; admisión no alcanza soporte. | Entre escuelas comparables, no aparece una desventaja relativa robusta de las que cierran. |
| ¿Las nuevas son mejores? | **`NOT_ESTIMABLE`**. | Falta soporte en las cohortes iniciales; no significa efecto cero, empate ni igualdad. |
| ¿La rotación mejoró el promedio? | SIMCE `−0,000105` DE; admisión `+0,000113` DE. | Los signos discrepan y son una descomposición contable, no efectos causales. |
| ¿Qué rol tienen los sostenedores y los SLEP? | Administran redes y transiciones bajo reglas distintas. | El panel describe eventos; no identifica el efecto de una modalidad de gestión. |
| ¿Existe una alternativa territorial? | Hay 38 cierres con una apertura compatible bajo la regla espacial. | Cercanía no demuestra cupos, acceso, destino ni sustitución. |

`DE` significa desviación estándar (una unidad relativa a la dispersión del puntaje). Un `IC 95 %` es un rango de incertidumbre del procedimiento. «Admisión núcleo» promedia lenguaje y matemática entre quienes rindieron ambas pruebas; no representa a todo cuarto medio.
{: .small}

## Cucharada 1: antes de evaluar un cierre, hay que saber qué cambió

### Una salida del registro no siempre es una escuela que desaparece

En la primera entrega, «entrada» y «salida» describían apariciones y desapariciones en los archivos. Para estudiar el período reciente necesito distinguirlas de los cambios administrativos y de la interrupción efectiva de la oferta educativa.

Un establecimiento puede cerrar; entrar en receso; fusionarse con otro; cambiar de identificador; perder una sede o dejar de impartir un nivel. También puede cambiar de sostenedor —la entidad responsable de administrarlo— sin dejar de funcionar. Ninguna de esas situaciones debería convertirse automáticamente en la misma clase de cierre.

El **RBD**, el identificador que utiliza el Ministerio de Educación para cada establecimiento, ayuda a seguir su historia, pero no la resuelve por sí solo. Un código que desaparece exige revisar qué ocurrió con la escuela, su sede y su oferta.

El panel sigue establecimientos durante el período reciente. Las transiciones oficiales comienzan cuando existen dos directorios consecutivos para observar el cambio de estado; El Salvador queda aparte como antecedente histórico. La unidad depende de la pregunta: el inventario cuenta eventos por RBD, la depuración reconstruye establecimientos y sedes, y las comparaciones usan establecimientos dentro de un segmento educativo.

**Ejercicio.** Separamos un cierre real de un cambio administrativo. Definimos como cierre oficial solo el paso desde un estado no cerrado al código `3`. Receso no es cierre; desaparecer del archivo queda como salida desconocida.

**Resultado.** Hay **900 cierres oficiales**: 684 desde actividad, 215 desde receso y uno desde autorización sin matrícula. De las 684 escuelas antes activas, 346 tenían estudiantes y 338 ya registraban matrícula cero. Cerrar una escuela vacía no equivale a desplazar una comunidad escolar.
{: .text-justify}

Pero esos 346 tampoco son automáticamente 346 escuelas que desaparecieron. Al reconstruir identidad y oferta, quedan **330 cierres estrictos de establecimiento-segmento**. Los otros 16 son cierres de sede o anexo, consolidaciones administrativas, reemplazos de RBD o casos no resueltos. Por ejemplo, los anexos London, Saint Gabriel y El Sembrador tienen candidatos a establecimiento principal que continúa activo. El vínculo es una inferencia desde directorios oficiales, no una equivalencia normativa confirmada; por eso se catalogan y se excluyen del estimando principal. Más adelante, el ejercicio territorial encuentra además cuatro candidatos a reemplazo en la misma sede: siguen dentro de los 330 cierres estrictos, pero se apartan solo de la comparación espacial.
{: .text-justify}

### No toda oferta cercana atiende la misma necesidad

La oferta también importa. Una sala cuna no compite por la misma población que una escuela básica o un liceo. Los códigos oficiales permiten separar educación inicial en sala cuna, nivel medio, transición y nivel heterogéneo; luego distinguimos básica y media. Desde aquí, «mercado» significa **comuna y segmento educativo exacto**, no toda institución que comparte territorio.
{: .text-justify}

Esa es una definición operativa, no una afirmación de que las familias eligen solo dentro de su comuna. También conviene distinguir establecimientos, matrícula y capacidad: una escuela con estudiantes no necesariamente tiene vacantes. Evaluar cobertura requiere saber qué niveles imparte, cuántos cupos puede ofrecer y si resulta accesible para quienes la necesitan.

Mientras tanto, el universo escolar se contrae. La población de 6 a 17 años proyectada por el [INE](https://www.ine.gob.cl/estadisticas-por-tema/demografia-y-poblacion/estimaciones-y-proyecciones-de-poblacion) pasa de **3.081.791 en 2025** a **1.366.155 en 2050**: `55,7 %` menos. Es población, no una predicción mecánica de matrícula o cierres; sí obliga a planificar capacidad, transporte y continuidad por territorio.
{: .text-justify}

### Dónde entran los SLEP y la desmunicipalización

Los SLEP agregan una capa institucional, no una explicación automática. Son sostenedores públicos y administran los establecimientos que han sido traspasados a su dependencia; no gobiernan toda la oferta de una comuna. La [Ley 21.040](https://www.bcn.cl/leychile/navegar?idNorma=1111237) regula ese traspaso y la Dirección de Educación Pública publica un [calendario por territorio](https://dep.gob.cl/calendario-de-traspaso/). Esas reglas no demuestran que una transición haya mejorado el aprendizaje. Además, un evento anterior al traspaso no puede atribuirse retrospectivamente al SLEP que hoy administra el territorio.
{: .text-justify}

La desmunicipalización plantea una pregunta distinta: **¿cambia la capacidad de sostener y mejorar una red cuando cambia su administración?** Un traspaso no debería contarse como desaparición municipal y creación de una escuela nueva si la misma comunidad continúa siendo atendida. Comparar sostenedores exigiría tasas con poblaciones expuestas y períodos equivalentes, no recuentos brutos. Este panel describe eventos; no identifica el efecto de una modalidad de gestión.

## Cucharada 2: ¿se van las que rinden peor y llegan alternativas mejores?

### La matrícula permite reconocer una trayectoria, no explicar su causa

**Objetivo.** Comprobar si las escuelas que cierran venían peor que alternativas comparables. Cada cierre se compara con establecimientos del mismo año, comuna, segmento educativo, dependencia, ruralidad y tamaño. SIMCE se estandariza por año, grado y asignatura; PSU, PDT y PAES, dentro de su propio proceso.

**Resultado.** La matrícula entrega la señal más clara: de los 684 cierres que venían de actividad, 665 tienen tres años completos y su mediana cae **`28 → 23 → 1`** estudiante.

Es una señal de vaciamiento anterior al cierre registrado. No significa que cada escuela haya seguido esa secuencia, ni explica si las familias se retiraron por dificultades educativas, por el anuncio de un cierre, por un traslado residencial o porque había menos niños en el territorio. Son explicaciones rivales por contrastar, no causas identificadas por esta trayectoria.

El desempeño tiene mucha menos cobertura:

| Trayectoria | Cierres con tres años | Cobertura sobre 684 | Medianas `t−3 → t−2 → t−1` |
|---|---:|---:|---|
| SIMCE | 76 | 11,1 % | `−0,232 → −0,235 → −0,083` |
| IVE-SINAE | 188 | 27,5 % | `0,882 → 0,910 → 0,946` |

IVE-SINAE es un índice agregado de vulnerabilidad escolar, no pobreza individual.
{: .small}

### Lo que dicen —y lo que no dicen— los puntajes

La tabla anterior describe el universo histórico amplio. La prueba estricta vuelve a filtrar anexos, cambios administrativos y segmentos distintos. De los 330 cierres elegibles, solo 97 tienen SIMCE y 46 admisión; después del emparejamiento exacto quedan **21 y 8**, respectivamente:

| Resultado | Estimación primaria | IC 95 % | Soporte |
|---|---:|---:|---:|
| SIMCE relativo | `+0,029` DE | `[−0,095; +0,158]` | 21 cierres |
| Puntaje de admisión (núcleo), entre quienes rinden | `−0,001` DE | `NOT_ESTIMABLE` | 8 cierres |

En palabras simples: entre escuelas comparables, SIMCE no muestra una diferencia precisa y admisión no alcanza el mínimo de diez cierres. Esto no dice que las escuelas que cierran estén sobre el promedio nacional: en el universo histórico amplio, la mediana SIMCE parte en `−0,232` DE. `NOT_ESTIMABLE` no significa cero, empate ni igualdad; significa que publicar un intervalo defendible exigiría fingir más información de la disponible.
{: .text-justify}

El mínimo de diez es una regla operativa retrospectiva, no una ley estadística que vuelva inválido cualquier estudio con nueve y válido cualquiera con diez. El límite se declara para no cambiarlo después de mirar los signos.

Las sensibilidades cuentan la misma historia. SIMCE ponderado da `+0,034` DE con un intervalo amplio `[−0,225; +0,289]`; las variantes de admisión siguen bajo el mínimo. Una especificación preliminar daba señal negativa, pero desaparece cuando dejamos de tratar anexos y mercados distintos como cierres comparables. Eso no prueba igualdad: muestra que la respuesta dependía de una definición demasiado laxa.
{: .text-justify}

### Un promedio puede cambiar sin que sepamos cuánto aprendieron los estudiantes

La contabilidad separa el cambio de quienes permanecen, la redistribución de matrícula y la contribución de entradas y salidas al indicador agregado. Un promedio podría subir porque deja de incluir a un grupo con puntajes bajos, sin que eso demuestre una mejora para ese grupo. También podría permanecer casi igual mientras unas comunidades ganan acceso y otras enfrentan traslados más difíciles.

### Este resultado no reemplaza lo que han encontrado otros estudios

[Grau, Hojman y Mizala](https://doi.org/10.1016/j.econedurev.2018.05.003), [Iocco](https://doi.org/10.2139/ssrn.4808834) y [Elacqua y colaboradores](https://doi.org/10.4067/S0718-52862012000200005) estudian consecuencias, receptores y alternativas con unidades y diseños distintos. No hay que obligarlos a entregar un único veredicto ni usarlos como validación automática de este ejercicio. Sí ayudan a precisar la pregunta: importa qué cierre ocurre, cómo se organiza la transición y qué alternativa efectiva encuentran los estudiantes.

## Cucharada 3: del promedio a la red educativa de cada territorio

### Qué pueden hacer los sostenedores con esta evidencia

La utilidad inmediata no es construir un ranking de escuelas que deberían cerrar. Es ordenar información antes de decidir si corresponde apoyar un establecimiento, ampliar su oferta, reorganizar una red o evaluar una fusión. Estas preguntas llevan a los mapas: no porque un mapa responda por sí solo, sino porque permite ver dónde una comparación agregada resulta insuficiente.

### Cómo leer los mapas sin convertir cercanía en reemplazo

**Objetivo.** Dar una forma territorial a la pregunta: cuando cierra una escuela estricta, ¿aparece cerca otra que atiende el mismo segmento? Buscamos una apertura dentro de 10 km y entre `t` y `t+2`. La ubicación del cierre corresponde a `t−1`; la ubicación de la entrada usa la **primera coordenada oficial válida entre el año de entrada y 2025**. Esta regla recupera registros tardíos sin fingir que la escuela estaba físicamente allí desde el primer año.

Aquí «entrada» es operacional: actividad con matrícula positiva después de al menos dos años despejados en el panel 2013–2025, sin episodio activo previo en esa ventana ni sucesión registrada. No demuestra que la escuela sea históricamente nueva; puede quedar historia anterior fuera del panel. Para los eventos recientes, además, la ventana posterior todavía puede estar incompleta.

Para mostrar variedad sin elegir el resultado más llamativo, tomamos primero **un caso por familia educativa preferida**; dentro de cada familia ordenamos por misma comuna, distancia, año y RBD. **Ni los valores ni la disponibilidad de resultados participan**. Las 9 trayectorias inestables se excluyen antes del emparejamiento y 259 entradas usan una coordenada informada con retraso; ambas cifras quedan visibles porque una ubicación tardía cambia qué significa «cerca».

**Resultado.** De 330 cierres estrictos, 320 tienen coordenada válida. Entre 414 aperturas, 389 tienen una coordenada elegible bajo la regla temporal. La guarda aparta seis pares candidatos, correspondientes a cuatro cierres, del mismo año y a no más de 100 metros, porque pueden ser reemplazos administrativos; exigir el mismo segmento excluye 420 combinaciones. Quedan **38 cierres emparejados con 29 aperturas únicas**. No hubo un par elegible de educación media. Los dos casos sistemáticos son descriptivos:

| Caso | Segmento | Cierre → apertura | Distancia | Qué permite ver |
|---|---|---|---:|---|
| Lo Barnechea | Transición inicial | 2016 → 2016 | 1,046 km | La apertura tiene su primera coordenada válida en 2019; observamos proximidad, no destino. |
| Lo Prado | Básica | 2016 → 2016 | 7,860 km | La apertura también se ubica con coordenada 2019 y queda fuera de la comuna del cierre. |

La selección no afirma que estos ejemplos sean representativos del país. Hace una cosa más modesta: muestra cómo cambian las preguntas cuando se conserva segmento, año de la coordenada y regla de identidad. Un enlace espacial es una hipótesis de proximidad, no una trayectoria estudiantil ni una prueba de sustitución.
{: .text-justify}

{% include thesis-post2-coordinate-audit-box.html %}

{% include thesis-extension-stylized-evidence.html %}

Los dos primeros botones pertenecen a la selección sistemática. El tercero juega otra partida: lo propuse porque crecí en El Salvador. Esa cercanía ayuda a formular preguntas, pero no convierte mi experiencia en explicación del cierre. Allí la Escuela N° 14 Óscar Yáñez Pastén (RBD 391) cerró al terminar 2013 y se fusionó con la Escuela N° 1 La Mina (RBD 390), en Diego Portales 1510. El [registro de la BCN](https://www.bcn.cl/laborparlamentaria/documento?id=636175) documenta que primero a sexto básico fueron derivados a la N° 1; el [reglamento institucional](https://fees.cl/wp-content/uploads/2019/12/Reglamento-de-convivencia-2019-2020.pdf) confirma su dirección e identidad.
{: .text-justify}

La matrícula conjunta de ambas escuelas cayó de **1.399 en 2004 a 977 en 2013** (`−30,2 %`). En 2014 la N° 1 pasó de 432 a 738 estudiantes, un salto compatible con la fusión documentada. La caída previa hace plausible una contracción demográfica, pero **no prueba que haya sido el motivo administrativo del cierre**; la intervención parlamentaria contemporánea discutió, de hecho, hacinamiento y adecuaciones posteriores.
{: .text-justify}

¿Había menos niños residentes? ¿Cambió la localización de los hogares vinculados a la minería? ¿Ganaron matrícula otras alternativas? ¿Se modificó la oferta de cursos? La serie vuelve pertinentes estas hipótesis; no permite escoger una por familiaridad con el lugar.

El visor usa un callejero OSM y coordenadas MINEDUC. En los dos casos sistemáticos la línea muestra cercanía, no destino; en El Salvador muestra la fusión documentada, no cada trayectoria individual.
{: .small}

Los ejemplos hacen visible la escala y el límite. En Lo Barnechea, el cierre y la entrada compatible están separados por 1,046 km y comparten comuna. En Lo Prado, la distancia es 7,860 km y no hay coincidencia comunal. En ambos casos el evento se registra en 2016, pero la coordenada de entrada aparece recién en 2019: el mapa es válido para contrastar los puntos oficiales seleccionados, no para reconstruir un recorrido ocurrido en 2016.
{: .text-justify}

Estos son hechos estilizados (patrones descriptivos útiles para formular preguntas), no experimentos. Los **paneles de salida y entrada son muestras separadas**; no seguimos estudiantes y no sabemos si la escuela nueva recibió a quienes salieron de la antigua.
{: .small}

Las figuras del carrusel usan **celdas descriptivas sin regularización** (sin el ajuste que estabiliza estimaciones ruidosas). La nota técnica usa otra cohorte, emparejamiento exacto y una regla mínima de soporte: **no son una segunda versión de la misma serie**.
{: .text-justify}

En el universo nacional, las nuevas tampoco entregan un final cómodo. El soporte exacto es `4/6/8` escuelas en SIMCE y `1/1/2` en admisión. Ninguna cohorte alcanza diez. La respuesta defendible es **`NOT_ESTIMABLE`**: esta base no permite decidir limpiamente si las entrantes son mejores o peores.
{: .text-justify}

La contabilidad de cada mercado separa el cambio de las escuelas que continúan, la reasignación de matrícula y la entrada o salida oficial. El recambio aporta `−0,000105` DE en SIMCE, con intervalo que cruza cero, y `+0,000113` en admisión, con intervalo positivo. Los signos no convergen y admisión observa solo rendidores. Como además las entradas no son estimables, **la consistencia schumpeteriana no queda apoyada**.
{: .text-justify}

## Lo que ya sabíamos y lo que agrega este ejercicio

[Iocco (2024)](https://doi.org/10.2139/ssrn.4808834) sigue estudiantes desplazados en Chile: encuentra efectos medios cercanos a cero y mejores resultados cuando la escuela receptora rinde más. Es un preprint; su cierre por desaparición prolongada del RBD puede mezclar cierres, fusiones o cambios de identificador. [Grau, Hojman y Mizala (2018)](https://doi.org/10.1016/j.econedurev.2018.05.003), en cambio, estiman para estudiantes afectados aumentos de `1,8–2,5` puntos porcentuales en deserción de enseñanza media y de `3,9–4,4` puntos en repitencia de quinto básico. Su unidad, periodo y diseño causal son distintos de nuestros descriptivos por escuela; por eso no se promedian ni se presentan como una contradicción automática.
{: .text-justify}

Aquí distinguimos evento, entidad, anexo y segmento; observamos renovación espacial y extendemos hasta 2025. Sin trayectorias individuales no identificamos destino, accesibilidad ni bienestar.
{: .text-justify}

### La pregunta que queda para una tercera entrega

La proyección demográfica nacional vuelve más importante esta discusión, pero no entrega un calendario de cierres. Antes de trasladarla a una comuna o localidad hay que estudiar población por edad, movilidad de los hogares, escolarización, capacidad y oferta por nivel. Un descenso nacional puede coexistir con barrios que necesitan escuelas nuevas.

Una tercera entrega podría construir escenarios territoriales para anticipar dónde apoyar, ampliar, reorganizar o resguardar capacidad educativa. Su producto útil no sería una lista de establecimientos destinados a cerrar.

## Qué puede usar la política pública

Este análisis sirve como **apoyo a la decisión**, no como una regla para cerrar, fusionar, abrir u ordenar escuelas en un ranking. La secuencia prudente es **observación → diagnóstico → decisión**. Saltar de una observación —por ejemplo, menor matrícula o una escuela cercana— directamente a un cierre confunde una señal con una causa y una causa con una solución.
{: .text-justify}

| Momento de la decisión | Señal que aporta este análisis | Evidencia adicional indispensable | Acción admisible y resguardo |
|---|---|---|---|
| Validar el evento | Distingue cierre, anexo, fusión, cambio de RBD y segmento. | Resoluciones, continuidad del principal y oferta por nivel. | Solicitar la corrección a quien mantiene el registro; no contar automáticamente una desaparición. |
| Diagnosticar matrícula decreciente | Muestra trayectoria, actividad y diferencias territoriales. | Población por edad, movilidad residencial, transferencias, competencia, capacidad y anuncios previos. | Activar diagnóstico y apoyo; no usar un umbral de matrícula como regla de cierre. |
| Planificar la transición o la red | Separa niveles y advierte que cercanía no equivale a sustitución. | Vacantes reales, accesibilidad y tiempos de viaje, destinos, apoyos, participación y continuidad pedagógica. | Preparar escenarios y un plan de transición; no presumir que la alternativa del directorio es utilizable. |
| Evaluar resultados | Define denominadores, muestras y límites de comparación. | Seguimiento de estudiantes y un contrafactual creíble. | Medir productos, resultados e impacto por separado; no atribuir aprendizaje, equidad o bienestar al cierre sin identificación causal. |

El alcance institucional también importa. Un SLEP planifica y gestiona **su propia red**, no los establecimientos de otros sostenedores. La [Ley 21.040, artículo 18, letras c y t](https://www.bcn.cl/leychile/navegar?idNorma=1111237), le encarga velar por una cobertura pública adecuada en su territorio —identificando zonas de expansión poblacional o de cobertura insuficiente— y por la continuidad de las trayectorias. MINEDUC puede observar brechas del sistema escolar; la Dirección de Educación Pública, las del Sistema de Educación Pública. El [Plan Anual Local 2026](https://dep.gob.cl/pal-2026/) planifica apoyo técnico, infraestructura y dotaciones a partir del número de cursos y la matrícula. Ninguna de esas funciones entrega autoridad sobre otros sostenedores, convierte este estudio en autorización administrativa ni demuestra que una modalidad de gestión sea superior.
{: .text-justify}

Hay dos errores de focalización que conviene vigilar. Un **falso positivo** señalaría como inviable una escuela cuya matrícula cae porque disminuye la población local, aunque siga siendo necesaria para asegurar acceso. Un **falso negativo** omitiría una transición riesgosa porque la matrícula agregada parece estable, aun cuando ciertos niveles, territorios o grupos hayan perdido una alternativa efectiva. El IVE-SINAE ayuda a describir composición agregada de la escuela; no identifica pobreza individual ni decide por sí solo dónde intervenir.
{: .text-justify}

Una teoría de cambio evaluable distingue cinco niveles. **Insumos:** registros de eventos válidos, demografía, capacidad, accesibilidad y destinos. **Actividades:** diagnosticar, apoyar, planificar transiciones y hacer seguimiento. **Productos:** evento clasificado, auditoría de capacidad y plan de transición. **Resultados intermedios:** continuidad, viaje, asistencia y retención. **Impactos:** aprendizaje y equidad. La cadena supone vacantes reales, traslados aceptables y participación de las comunidades; esos supuestos también deben probarse. **Este post propone la cadena para evaluarla; no acredita que ya funcione.**
{: .text-justify}

## Qué falta para hablar de causalidad

| Ruta | Qué permitiría responder | Prueba que puede hacerla fallar |
|---|---|---|
| Estudio de evento o diferencias en diferencias | Comparar trayectorias con un grupo creíble. | Tendencias previas incompatibles o anticipación del cierre. |
| Discontinuidad o variable instrumental | Aprovechar una regla que cambie la probabilidad de cierre. | Manipulación, primera etapa débil o exclusión inverosímil. |
| Seguimiento individual | Medir destino, transporte y resultados posteriores. | Pérdida selectiva o enlaces erróneos. |

<details class="technical-disclosure" markdown="1">
<summary>Nota técnica y controles de robustez</summary>

Esta sección conserva las cifras necesarias para auditar el ejercicio sin convertir el relato principal en un log de ejecución.

**Cobertura y deuda residual.** El registro de identidad reunió 14 alias oficiales y dos sucesiones temporales candidatas; estas últimas no tocan las 337 salidas del panel de riesgo, pero el registro no acredita que todas las recodificaciones posibles estén detectadas. La auditoría de selección muestra soporte desigual por dependencia, ruralidad y región, por lo que los resultados describen la muestra observada y no un efecto poblacional nacional. Los ejercicios SLEP reprodujeron patrones exploratorios, pero rechazaron el diseño causal porque no se sostuvo la equivalencia de las trayectorias previas y solo hubo entre tres y cuatro territorios tratados, según el desenlace. La literatura se usa como contexto: este post no reclama novedad exhaustiva.

**Mercados locales.** El estimando H1 compara la diferencia de riesgo entre los percentiles 75 y 25 de concentración en seis vecindarios espaciales con la misma diferencia bajo comuna. Es una sensibilidad de posición relativa, no el efecto de redibujar el mercado. Ninguna banda excluye cero: los techos son `0,273108` y `0,375248` puntos porcentuales. Los cortes de `0,25` y `0,5` son umbrales exploratorios del índice de concentración fijados por el autor, no reglas de política.

**Salidas y sensibilidad.** MR1-SIMCE estima `+0,029` DE `[−0,095; +0,158]` con 21 cierres. La variante `weighted_raw` da `+0,034` `[−0,225; +0,289]`. Admisión núcleo queda `NOT_ESTIMABLE` con ocho cierres en el resultado primario y sus sensibilidades. En modalidad humanista-científica hay siete; técnico-profesional tiene cero comparaciones con soporte estricto. Ciencias cubre solo a quienes eligieron y rindieron esa prueba.

La regresión a la media (un extremo tiende a acercarse al promedio al repetirse) produjo rebotes entre escuelas abiertas. Este diagnóstico no está emparejado, no aplica el shrinkage de MR1 ni asigna un evento de cierre. La vía administrativa de cierre de la Ley 20.529 es otro mecanismo rival.

**Entradas.** MR2 queda `NOT_ESTIMABLE` en ambos resultados: el soporte por cohorte es 4/6/8 en SIMCE y 1/1/2 en admisión, insuficiente para publicar estimaciones o intervalos. Promover signos sin soporte cambiaría la regla después de mirar. El protocolo es retrospectivo, no un registro previo prospectivo: registra diez desviaciones; planificó soportes mínimos 5, 10 y 20, pero solo ejecutó 10. Por eso esta publicación no presenta el umbral como una prueba de robustez ni usa puntos subsoportados para concluir.

**Descomposición.** Los mercados son comuna por segmento exacto. La rotación oficial suma entrada y salida: SIMCE `−0,000105` `[−0,000346; +0,000103]`; admisión `+0,000113` `[+0,000027; +0,000213]`. El componente `between` (reasignación entre incumbentes) es mayor: `+0,004777` en SIMCE y `+0,001858` en admisión. La identidad contable cierra con residuo máximo `6,66e−16`, bajo la tolerancia `1e−10`. Son identidades, no causas.

**Territorio y coordenadas.** El ejercicio espacial conserva 38 cierres emparejados con 29 aperturas únicas. La entrada se ubica en la primera coordenada oficial válida entre su año de entrada y 2025; 9 trayectorias inestables quedan fuera y 259 entradas tienen coordenada tardía. La auditoría nacional abarca 12.116 filas oficiales: 12.038 establecimientos funcionando y 78 autorizados sin matrícula, informados por separado. En ese total, 6.601 tienen al menos un candidato OSM, 5.515 no lo tienen y 126 filas fueron revisadas. Hay cero errores oficiales confirmados. OSM es una fuente secundaria; el producto público contiene agregados y no redistribuye la tabla combinada por establecimiento.

**Reproducibilidad.** Las cifras agregadas de esta ejecución son reproducibles; el snapshot científico está ligado a un ancla Git local y a un *freeze* verificable. Python preparó el CSV privado de entrada; R produjo los agregados, ejecutó 999 réplicas *bootstrap* (remuestreos para medir incertidumbre), y Python reconcilió las estimaciones puntuales de 112 celdas públicas agregadas. Ese acuerdo reduce errores de implementación, no confusión causal.

</details>

## Cierre: evaluar la transición, no celebrar el movimiento

Extender la tesis reveló que «cierre» escondía stocks, eventos, escuelas vacías, anexos y reemplazos de RBD; «mercado» mezclaba sala cuna, básica y media; «renovación» confundía cercanía con destino.
{: .text-justify}

La destrucción creadora escolar sigue siendo atractiva y por eso merece una prueba desagradablemente estricta. Hay señales, vacíos y presión demográfica; no permiso para celebrar.
{: .text-justify}

El mercado escolar chileno cambió de reglas y estructura en las décadas de 1980, 1990, 2000, 2010 y 2020. A este ritmo, la inteligencia artificial todavía corre detrás: al menos sus versiones vienen numeradas.
{: .text-justify}

### Transparencia y alcance de las fuentes

La tesis y su extensión son de mi autoría; no constituyen una réplica independiente. El Salvador fue seleccionado por mi vínculo biográfico con la localidad. Hacer explícitas ambas circunstancias permite reconocer posibles sesgos de confirmación y selección.

Este trabajo no recibió financiamiento de ninguna fuente. La persona autora declara no tener conflictos de interés; su única afiliación institucional es el Ministerio de Desarrollo Social y Familia de Chile, institución que no financió, encargó, supervisó ni revisó este trabajo, y cuyas posiciones no están representadas por sus conclusiones. Se utilizaron asistentes de inteligencia artificial para apoyar programación, control de calidad, revisión de prosa y revisión adversarial. Las decisiones metodológicas y editoriales, la verificación de fuentes y la responsabilidad por todas las afirmaciones y resultados corresponden exclusivamente a la persona autora.
{: .text-justify}

---

## Referencias

Chay, K. Y., McEwan, P. J., & Urquiola, M. (2005). [The central role of noise in evaluating interventions that use test scores to rank schools](https://doi.org/10.1257/0002828054825529). *American Economic Review, 95*(4), 1237–1258.

Elacqua, G., Martínez, M., Santos, H., & Urbina, D. R. (2012). [School closures in Chile: Access to quality alternatives in a school choice system](https://doi.org/10.4067/S0718-52862012000200005). *Estudios de Economía, 39*(2), 179–202.

Grau, N., Hojman, D., & Mizala, A. (2018). [School closure and educational attainment: Evidence from a market-based system](https://doi.org/10.1016/j.econedurev.2018.05.003). *Economics of Education Review, 65*, 1–17.

Hsieh, C.-T., & Urquiola, M. (2006). [The effects of generalized school choice on achievement and stratification](https://doi.org/10.1016/j.jpubeco.2005.11.002). *Journal of Public Economics, 90*(8–9), 1477–1503.

Iocco, M. P. (2024). [Impact of planned school closures on academic performance: Evidence from Chile](https://doi.org/10.2139/ssrn.4808834). *SSRN preprint*.

Paredes, R. D., & Fresard, M. (2018). [Voucher y cierre de escuelas en Chile](https://doi.org/10.38178/cep.vi151.62). *Estudios Públicos*, (151).

Quintero-Fragozo, C., Cortés, Y., & Sarrias, M. (2023). [Effects of spatial competition on public educational efficiency](https://doi.org/10.1080/02680939.2021.1966102). *Journal of Education Policy, 38*(1), 115–140.

Taghizadeh, J. L. (2020). [Effects of school closures on displaced students and future cohorts](https://doi.org/10.1016/j.labeco.2020.101910). *Labour Economics, 67*, 101910.
