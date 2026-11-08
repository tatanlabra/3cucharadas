---
layout: single
classes: [thesis-extension-post, post3-evidence]
title: "Extender mi tesis en 3 cucharadas (parte IV): matrícula superior después de la escuela de origen"
subtitle: "Las generaciones anterior y posterior de liceos con pérdida de oferta difieren de sus controles; el contraste de cambios es descriptivo e impreciso para acceso total."
date: 2026-11-04 10:00:00 -0300
categories: [datos, educacion, politica-publica]
tags: [educacion, cierre-escolar, educacion-superior, sies, datos-administrativos, politica-publica]
description: "Matrícula superior, destinos, persistencia y titulación tras pérdida de oferta escolar: cohortes comparables, ventanas maduras y límites causales."
excerpt: "Comparo generaciones de liceos con pérdida de oferta y controles. Distingo matrícula observada, destino, persistencia y titulación, sin llamar causal al contraste."
author: clabra
lang: es
ref: cierre-escolar-educacion-superior-causal-ml
permalink: /datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/
math: true
toc: true
toc_sticky: true
comments: true
author_profile: true
ai_disclosure:
  level: some_ai
  components:
    text: assisted
    hero: generated
last_modified_at: 2026-11-07 23:40:00 -0300
header:
  teaser: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/teaser-1280x720.webp
  og_image: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/og-1200x630.webp
  og_image_alt: "Ilustración nocturna de trayectorias estudiantiles que parten desde un liceo cerrado y se bifurcan hacia campus universitarios e institutos técnico-profesionales, representando la separación entre selección previa y efecto causal."
  overlay_image: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/hero-1600x900.webp
  overlay_image_mobile: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/hero-mobile-800x450.webp
  overlay_filter: linear-gradient(90deg, rgba(9,11,24,0.94) 0%, rgba(9,11,24,0.68) 42%, rgba(9,11,24,0.12) 72%, rgba(9,11,24,0.08) 100%)
  show_overlay_excerpt: false
  teaser_mobile: /assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml/teaser-mobile-640x360.webp
visual_id: cierre-escolar-educacion-superior-causal-ml
editorial_contract: societal-contribution-v1
table_contract: explicit-v1
distribution:
  social: false
  republish: []
  skip_reason: "Diffusion deferred by author."
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

Perder una escuela puede afectar una trayectoria mucho después de conseguir otra vacante. Seguí a generaciones de liceos en registros escolares y del Servicio de Información de Educación Superior (SIES) para preguntar por matrícula, destinos y continuidad de estudios. Encontré menor matrícula superior en el grupo de liceos con pérdida de oferta en **ambas generaciones comparadas**. Al comparar sus cambios con los de controles, los intervalos de acceso total abarcan diferencias negativas y positivas. **La evidencia describe brechas; todavía no permite atribuirlas al cierre.** <!-- CLAIM: P4-01 -->

La literatura explica por qué conviene mirar más allá de la matrícula escolar, sin anticipar una respuesta para Chile. Grau, Hojman y Mizala (2018) estudian deserción y repitencia tras cierres chilenos, y Elacqua y colaboradores (2012) muestran que no todas las familias tienen alternativas cercanas de calidad. Para educación posterior, Larsen (2020) encuentra pérdidas de graduación y asistencia universitaria tras cierres de liceos en Milwaukee; Bross, Harris y Liu (2023) encuentran resultados distintos según ciudad y nivel al cerrar y reabrir escuelas como *charter* en Luisiana; Kim (2024), en un documento de trabajo sobre Texas, observa consecuencias postsecundarias. Son eventos, poblaciones y diseños diferentes de esta pérdida de oferta: motivan las preguntas, pero no convierten mis contrastes en efectos causales.

La parte III examina la trayectoria escolar inmediata. Llamo **G** al año del evento y parto de estudiantes matriculados en **G−1** en su escuela de origen. Calculo cuándo terminarían la media si avanzaran regularmente. Busco matrícula SIES de pregrado en **los dos años siguientes a ese egreso esperado**. No verifico el egreso efectivo ni la primera entrada de la vida a educación superior: la medida puede mezclar demoras escolares y decisiones posteriores. El denominador incluye al grupo inicial con identificador y seguimiento válidos, también a quienes nunca aparecen en SIES. <!-- CLAIM: P4-02 -->

La serie empieza en **2009** porque la generación anterior requiere matrícula escolar de **G−5** y los registros empiezan en **2004**. Separo eventos **2009–2015** y **2016–2024** porque las fuentes y reglas para reconocer pérdida de oferta cambian entre eras. Tampoco todos los años contienen los mismos grados: para acceso, 2023 y 2024 solo aportan tercero medio; para persistencia y titulación, ese mismo grado es el único que aporta en sus extremos modernos de 2023 y 2019. Las exclusiones responden a seguimiento incompleto o falta de una comparación elegible —segundo medio de 2023 tiene ventana completa, pero no comparador suficiente—. Por eso probé además años con soporte en los **tres grados de media**, sin sustituir la serie completa. Básica superior requiere otro análisis y no se presenta como resultado estimado aquí. <!-- CLAIM: P4-03 -->

**Cómo leo las comparaciones.** La unidad visible es el punto porcentual, la resta entre dos tasas expresadas en %. Los intervalos **primarios** de acceso total se fijaron al **97,5 %** y los de destinos al **98,75 %** para contemplar su familia de comparaciones; los de persistencia y titulación se presentan al **95 %**. Se obtuvieron remuestreando escuelas, no estudiantes aislados, porque estudiantes del mismo liceo pueden compartir condiciones. Un intervalo que cruza cero deja abierta la dirección del contraste bajo el método; no prueba igualdad. Y ningún intervalo incorpora, por sí solo, una escuela mal clasificada, un enlace perdido o tendencias que habrían sido distintas aun sin cierre. <!-- CLAIM: P4-04 -->

El [anexo metodológico]({{ '/datos/educacion/politica-publica/cierre-escolar-educacion-superior-causal-ml/anexo-metodologico/' | relative_url }}) documenta el calendario, las definiciones, la cobertura y las sensibilidades; las tres cucharadas se entienden sin abrirlo.

## Cucharada 1: ¿cómo cambia la brecha entre generaciones?

Si las tasas de educación superior de los liceos con evento difieren de las de control entre generaciones escolares, mirar solo la generación cercana al evento exageraría lo que sabemos de él. Por eso contrasté **dos generaciones del mismo grado** en cada liceo: la anterior matriculada **cinco años antes** del evento y la posterior **un año antes**. Luego comparé esos cambios dentro de grupos del mismo año, región, dependencia administrativa, condición urbana o rural, tipo de enseñanza y curso. Los controles son liceos sin pérdida de oferta detectada en el inventario 2005–2024; esa elección favorece escuelas que sobrevivieron y puede sesgar la comparación. Conservé controles de la misma comuna para mantener comparabilidad local y suficientes casos, aunque podrían recibir estudiantes desplazados. Por eso también se requiere comprobar qué sucede al excluirlos. Son generaciones distintas: no sigo a las mismas personas en ambos períodos. <!-- CLAIM: P4-05 -->

**Anterior y posterior nombran generaciones escolares, no dos mediciones tomadas enteramente antes y después del evento.** Para un evento en 2016, la generación anterior de primero medio parte en 2011, terminaría la media en 2014 y tiene ventana de acceso en 2015–2016. Parte de su resultado coincide, por tanto, con el año del evento. Tampoco verifiqué que cada estudiante hubiera egresado efectivamente antes de ese año. Esta comparación describe diferencias entre generaciones; por sí sola no demuestra que la brecha de educación superior estuviera íntegramente medida antes del cierre. <!-- CLAIM: P4-05 -->

La era histórica ilustra por qué importa mirar las cuatro tasas. En **2009–2015**, la matrícula superior observada dentro de la ventana era **45,87 %** en la generación anterior y **48,56 %** en la posterior de liceos con evento; en controles, era **60,43 %** y **65,43 %**, respectivamente. La generación anterior también muestra una desventaja de nivel. El cambio del grupo con evento fue menor que el de control y el contraste ajustado agregado fue **−2,31 puntos porcentuales**, intervalo **−5,26 a +0,29**. La generación cercana al evento aportó **10.183** observaciones estudiante-cohorte de liceos con evento y **1.208.182** de control; el cálculo reunió **73** escuelas con evento entre ambas generaciones. Estos recuentos de estudiantes no son el total de las cuatro tasas. Cada grupo comparable pesa según sus estudiantes expuestos. Las cuatro tasas usan esos mismos pesos: restar sus cambios permite reconstruir aproximadamente el contraste, con pequeñas diferencias por redondeo. <!-- CLAIM: P4-06 -->

En **2016–2024**, las tasas fueron **55,93 % en la generación anterior** y **55,01 % en la posterior** de liceos con evento, frente a **66,17 %** y **67,68 %** en controles. El contraste agregado fue **−2,43 puntos**, intervalo **−5,67 a +1,27**, con **2.916** observaciones de la generación cercana al evento en liceos con evento, **806.153** de control y **27** liceos con evento entre ambas generaciones. La precisión es frágil: hay pocos liceos con evento y algunos concentran mucho peso. Tampoco está verificado que todos los controles hayan seguido sin un evento similar durante todo el período observado. No interpreto la diferencia entre los dos períodos como una evolución demostrada: las reglas de clasificación, muestras y grados incluidos difieren. <!-- CLAIM: P4-07 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-access-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-access-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

Como comprobación del horizonte, también busqué matrícula solo en el **primer año posterior al egreso esperado**. El contraste es **−1,71 puntos** en 2009–2015, intervalo **−4,04 a +0,17**, y **−2,10** en 2016–2024, intervalo **−5,56 a +1,57**; estos intervalos son del 95 %. Tampoco identifican primera entrada individual ni separan una demora escolar de una demora en continuar estudios. <!-- CLAIM: P4-18 -->

La resta de cambios descontaría una brecha estable bajo condiciones exigentes. No resuelve que las escuelas tengan tendencias distintas, que un control reciba estudiantes desplazados o que falten enlaces. Las cotas por capacidad nacional de identificadores inválidos ilustran este último problema: **−80,95 a +74,03 puntos** en la era histórica y **−71,70 a +66,18** en la moderna. Son límites conservadores, no intervalos de confianza ni tasas medidas de error por grupo. Su amplitud impide defender una dirección solo con esa información de enlace. Tampoco bastaría restar las tasas si las trayectorias sin evento hubieran sido distintas (Roth et al. 2023). <!-- CLAIM: P4-08 -->

### ¿Depende la comparación de quién sirve como control?

Repetí el análisis con atributos escolares estables, controles de otra comuna, años con los tres grados comparables y ajuste adicional por edad y género basales. En esas cuatro variantes, los puntos de acceso total permanecen negativos en ambas eras, pero cambian la población o sus pesos; esa coincidencia no prueba equivalencia.

Como diagnóstico de efectos fijos, el acceso histórico es **−2,47 puntos**, intervalo del **95 %** **−4,85 a −0,21**, frente al primario **−2,31**, intervalo del **97,5 %** **−5,26 a +0,29**: usa otros pesos y otro estimando, además de otro nivel de confianza; sus cruces de cero no prueban una diferencia entre estimadores.

Al usar **solo controles con pérdida de oferta futura**, el acceso histórico pasa a **+0,73 puntos** con el horizonte de exposición escolar y **+1,03** con el horizonte del desenlace; sus intervalos del 97,5 % son **−2,86 a +4,14** y **−2,96 a +4,68**. La muestra tratada es menor que en el primario. La inversión del punto no demuestra por sí sola sesgo del primario: cambió la comparación. La figura conserva también las variantes modernas y sus períodos, sin escoger solo las que coinciden. Con controles futuros únicamente, la comparación moderna con horizonte de exposición escolar tiene soporte para eventos **2016–2019**; con horizonte completo del desenlace, el soporte se limita a **2016–2018**: después faltan controles elegibles para las cuatro tasas, y ciertos grados carecen además de seguimiento. El inventario conserva años hasta 2024 como estados sin soporte o censurados; no se los convierte en cero. <!-- CLAIM: P4-19 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-sensitivity-comparison-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset/sensitivity" csv="post4-sensitivity-comparison-all.csv" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-sensitivity-comparison-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset/sensitivity" csv="post4-sensitivity-comparison-all.csv" %}

[Tabla accesible de comparaciones]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-comparison-table-es.html' | relative_url }})

<details class="post3-methods">
<summary>Ver los 22 contrastes de comparación y sus intervalos</summary>
<div class="tabla-desliza" role="region" tabindex="0" aria-label="Sensibilidades de comparación. Se omiten conteos de personas para proteger la privacidad.">
{% include tesis-reset-tables/post4-sensitivity-comparison-table-es.html %}
</div>
</details>

### ¿Los resultados de generaciones anteriores son realmente previos?

Volví a comparar dos generaciones anteriores, con puntos de partida G−6 y G−5. En acceso moderno, el contraste es **−3,12 puntos**, intervalo del **97,5 %** **−5,24 a −0,68**. El análogo histórico queda cerca de cero: **−0,35**, intervalo **−1,55 a +0,82**. El resultado moderno muestra una brecha también entre generaciones anteriores, pero algunas de sus ventanas alcanzan el año del evento: no es una prueba limpia de tendencias enteramente previas ni permite atribuir esa brecha a anticipación.

Al exigir que **ambas ventanas terminen antes de G**, quedan fuera estudiantes que partían en primero medio: el contraste es **−2,28**, intervalo **−5,09 a +0,70**, para eventos 2016–2024. Cambian soporte y pesos; restar ambas cifras no mide contaminación, y que el intervalo cruce cero tampoco confirma tendencias paralelas. La comparación aún más temprana, G−7 frente a G−6, da **−1,17**, intervalo **−3,15 a +1,13**, con ventanas de acceso enteramente previas en esa era. Conservo ambas pruebas.

En la era histórica, la comparación tardía queda en **2010–2015**: en 2009 primero medio no tiene soporte y segundo y tercero no completan la ventana. La temprana queda en **2011–2015**: en 2009 los tres grados están censurados y en 2010 primero carece de soporte mientras segundo y tercero están censurados. La matrícula escolar comienza en 2004 y SIES en 2007: desplazar las generaciones a G−7/G−6 puede dejar sin año basal escolar y sin ventana SIES completa. Se retienen los estados de los años excluidos. Para titulación, ninguna de las dos comparaciones anteriores ofrece grados cuyas dos ventanas completas terminen antes del evento: ese diagnóstico no es estimable bajo el calendario fijado. <!-- CLAIM: P4-20 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-sensitivity-calendar-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset/sensitivity" csv="post4-sensitivity-calendar-all.csv" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-sensitivity-calendar-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset/sensitivity" csv="post4-sensitivity-calendar-all.csv" %}

[Tabla accesible del calendario]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-calendar-table-es.html' | relative_url }}) · [Matriz accesible de ventanas]({{ '/assets/images/tesis-post4/scientific-reset/sensitivity/post4-sensitivity-calendar-window-matrix-es.html' | relative_url }})

<div class="tabla-desliza" role="region" tabindex="0" aria-label="Calendario A/B. Se omiten conteos de personas para proteger la privacidad.">
{% include tesis-reset-tables/post4-sensitivity-calendar-table-es.html %}
</div>

<details class="post3-methods">
<summary>Ver las ventanas completas por desenlace y grado</summary>
<div class="tabla-desliza" role="region" tabindex="0" aria-label="Finales de ventanas relativos al año G del evento; G no es estrictamente previo. B exige que ambas generaciones terminen antes de G, además de soporte observado.">
{% include tesis-reset-tables/post4-sensitivity-calendar-window-matrix-es.html %}
</div>
</details>

La primera respuesta es, entonces, una descripción de cambios relativos: observo una desventaja en ambas generaciones y contrastes de acceso total cuyos intervalos incluyen valores negativos, cero y valores positivos. No puedo decir que el cierre "cerró la puerta" ni que no tuvo efecto. Antes de discutir continuidad de estudios conviene mirar **qué tipo de matrícula superior** aparece en la misma ventana.

## Cucharada 2: ¿a qué destinos llegaron los registros?

Decir "educación superior" puede ocultar trayectorias distintas. Clasifiqué a cada estudiante del grupo inicial en cuatro destinos **mutuamente excluyentes** dentro de la misma ventana de dos años: solo universidad, solo instituto profesional o centro de formación técnica (**IP/CFT**), ambos tipos, o ninguno registrado en el extracto SIES. "Ninguno" significa que no encuentro matrícula de pregrado enlazable en esa ventana; no prueba que la persona nunca estudió, que no ingresará más tarde ni que una vía tenga menor valor. Para cada destino comparé el cambio entre generaciones de liceos con evento con el cambio de los controles. Las cuatro categorías comparten el mismo grupo inicial y sus proporciones suman el total. <!-- CLAIM: P4-09 -->

La tabla conserva los cuatro destinos y sus rangos de incertidumbre. Cada cifra es la diferencia entre el cambio del grupo con evento y el de controles, en puntos porcentuales; los intervalos son del **98,75 %** y se leen dentro de su propio período. Las categorías comparten por era la cohorte basal elegible del acceso total; en la era moderna contribuyen **27** liceos con evento entre ambas generaciones. <!-- CLAIM: P4-10 --> <!-- CLAIM: P4-11 -->

| Destino observado en dos años | 2009–2015: contraste (intervalo) | 2016–2024: contraste (intervalo) |
|---|---:|---:|
| Solo universidad | −2,07 (−4,18 a −0,23) | +0,83 (−2,59 a +3,88) |
| Solo IP/CFT | −0,31 (−2,97 a +2,40) | −2,61 (−5,51 a +1,00) |
| Ambos tipos | +0,07 (−0,33 a +0,43) | −0,64 (−1,93 a +0,18) |
| Ninguno registrado | +2,31 (−0,61 a +5,58) | +2,43 (−1,68 a +6,05) |
{: .table--compact .table--scroll}

En el período histórico, solo universidad tiene un intervalo completamente negativo: describo esa dirección en el contraste, sin atribuirla al evento. En el moderno, todos los intervalos admiten ambos signos y la comparación depende de pocos liceos; no hay una redistribución con dirección inequívoca. Un intervalo que abarca cero no prueba que los destinos fueran iguales. <!-- CLAIM: P4-10 --> <!-- CLAIM: P4-11 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-destinations-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-destinations-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

Una diferencia en categorías no equivale a una sustitución individual demostrada. Que un agregado muestre menos "solo IP/CFT" y otro más "ninguno" no permite afirmar que las mismas personas cambiaron un destino por otro. Haría falta una reconstrucción individual de opciones y calendarios, además de una comparación causal defendible. Las características iniciales, el rendimiento y los recursos familiares pueden influir tanto en la escuela como en la educación superior; ajustar variables conocidas no revela todo lo que no se midió. "Ningún registro" es el complemento aritmético del acceso en dos años, no una señal independiente; sus intervalos difieren porque la familia de destinos usa **98,75 %** y el acceso total **97,5 %**. La siguiente pregunta exige aún más tiempo: ¿quién permanece matriculado y quién alcanza un título?

## Cucharada 3: ¿qué muestran persistencia y titulación?

El acceso inicial observado no agota una trayectoria. Definí **persistencia** como matrícula SIES en por lo menos **dos de los tres años** que comienzan en el primer año posterior al egreso escolar esperado. Los dos años no tienen que ser consecutivos. Definí **titulación** como al menos un título de pregrado registrado dentro de **seis años calendarios inclusivos** desde el primer año posterior al egreso esperado. En ambos casos comparé el cambio entre generaciones de liceos con evento con el cambio de los controles y conté a todos los estudiantes del grupo inicial con seguimiento completo, incluidos quienes nunca registraron acceso. Por eso estas **no son tasas entre ingresantes**. Una generación demasiado reciente queda fuera en vez de convertirse en cero. <!-- CLAIM: P4-12 -->

Para persistencia en **2009–2015**, el contraste agregado fue **−3,13 puntos**, intervalo **−5,30 a −1,20**; en **2016–2023**, **−1,90**, intervalo **−5,01 a +1,31**. La muestra moderna termina en 2023 porque la cohorte siguiente no completa la ventana de tres años. El resultado histórico señala una diferencia direccional en el contraste descriptivo; el moderno es más incierto y se basa en **26** liceos tratados, con precisión débil. No concluyo que la persistencia moderna no cambió: el intervalo admite tanto una diferencia adversa como una favorable en la escala estimada. <!-- CLAIM: P4-13 -->

Para titulación en **2009–2015**, el contraste agregado fue **−1,47 puntos**, intervalo **−2,69 a −0,28**. En la era moderna, solo **2016–2019** dispone del horizonte fijado: allí el contraste fue **−2,28 puntos**, intervalo **−5,56 a +0,71**, con **16** liceos con evento entre ambas generaciones. Esos últimos años no sustituyen la ventana moderna de acceso hasta 2024. La escasez de escuelas tratadas maduras limita especialmente la precisión y cualquier lectura por subgrupo. Los intervalos son del 95 % para estos desenlaces secundarios y tampoco incorporan la incertidumbre de enlaces y clasificación. <!-- CLAIM: P4-14 -->

Las sensibilidades de estos desenlaces también cambian con el calendario y el comparador. Para persistencia moderna, la comparación tardía entre generaciones anteriores arroja **−2,41 puntos**, intervalo del **95 %** **−4,50 a −0,07**, en 2016–2024; algunas ventanas alcanzan G, de modo que no prueba tendencias enteramente previas. Con solo controles cuyo evento ocurre después del horizonte del desenlace, la persistencia moderna es **−10,02 puntos**, intervalo **−19,51 a −0,81**, en 2016–2017 con **cuatro liceos con evento**; la titulación histórica es **+4,05**, intervalo **−0,64 a +8,80**, en 2009–2014 con **27 liceos**. Son contrastes descriptivos con muestras y pesos distintos; no prueban una diferencia frente al primario ni un efecto del cierre. El resultado de cuatro liceos tiene precisión escolar especialmente débil. <!-- CLAIM: P4-19 --> <!-- CLAIM: P4-20 -->

{% assign reset_figure = site.data.tesis_reset_figures["post4-followup-historical"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

{% assign reset_figure = site.data.tesis_reset_figures["post4-followup-modern"] %}
{% include thesis-reset-figure.html figure=reset_figure base="/assets/images/tesis-post4/scientific-reset" %}

### Otras dos pruebas que no cambian la lectura

¿Son iguales los contrastes en todos los grupos? Comparé subgrupos definidos por grado, dependencia, ruralidad y región antes del evento. De **800 contrastes predefinidos**, **388** pudieron estimarse y **412** quedaron sin soporte o reservados. **34** presentan un valor p ajustado menor que 0,05: una señal bajo las pruebas fijadas, no una probabilidad de que la hipótesis sea verdadera. Usé el ajuste de **Holm** (1979), que vuelve más exigente encontrar diferencias al probar varias comparaciones, dentro de cada familia de desenlace y era; no controla conjuntamente las 800 pruebas. Los 34 no son descubrimientos independientes: acceso y ausencia de registro son complementos y repiten algunos contrastes. No convierto esos resultados exploratorios en un mapa de estudiantes "más afectados" ni en mecanismos causales. <!-- CLAIM: P4-21 -->

También evalué la factibilidad de diferencias en diferencias **doblemente robustas** de cortes repetidos (Sant’Anna y Zhao 2020), un método que combina modelos de composición y resultados. El nombre no significa que resista cualquier error. Antes de calcular efectos, fallaron requisitos de soporte o ajuste en parte de los estratos de ambas eras; los ocho desenlaces quedaron no estimables con esa especificación en cada era. No eliminé los estratos difíciles para fabricar una cifra. La ruta de aprendizaje automático flexible y sus diagnósticos de heterogeneidad individual no se ejecutaron; no los declaro imposibles ni reutilizo predicciones antiguas como confirmación. <!-- CLAIM: P4-15 -->


La tercera respuesta combina una señal y una frontera: hay diferencias descriptivas en seguimiento y titulación histórica, pero las cohortes recientes aportan menos años maduros y menos escuelas, y sus intervalos son amplios. Para una familia no significa que una opción esté garantizada o cerrada; para una institución significa que debe conservar información longitudinal verificable antes de atribuir resultados a una decisión escolar.

## Lo que aprendí y lo que falta

Las tres cucharadas responden preguntas encadenadas. Primero, ambas generaciones muestran una desventaja de nivel en matrícula superior en los liceos con evento; la diferencia entre sus cambios y los del grupo de comparación es imprecisa. Segundo, los destinos universitario, técnico-profesional, mixto y sin registro muestran patrones distintos, pero ninguno revela por sí solo sustituciones individuales causadas por el evento. Tercero, persistencia y titulación exigen más años de seguimiento y, en las cohortes modernas maduras, menos escuelas sostienen los resultados. Los subgrupos exploratorios no convierten esos contrastes en perfiles causales y la factibilidad fallida de DR-DiD no aporta una estimación adicional. He descrito lo que aparece en los registros y el alcance de cada comparación; la identificación causal sigue abierta. <!-- CLAIM: P4-16 -->

Los desafíos siguientes son validar enlaces individuales, seguir posibles eventos de los controles más allá del inventario y sustentar comparaciones que preserven población y calendario. Las sensibilidades ya calculadas muestran por qué importa: algunas mantienen la dirección y otras cambian el signo junto con la muestra. Ninguna decide por sí sola qué habría pasado sin pérdida de oferta. Para mejorar la transición educativa, es prudente documentar vacante, traslado y seguimiento hacia el egreso; este análisis todavía no cuantifica cuánto de la trayectoria cambió **por** el cierre.

> **Nota de corrección.** Esta revisión cambia la población, el calendario de seguimiento, la pregunta medida y la incertidumbre respecto de la edición anterior. Sus estimaciones de aprendizaje automático y sus figuras respondían a otra comparación; no se deben mezclar con estos resultados. <!-- CLAIM: P4-17 -->


## Referencias

- Bross, Whitney, Douglas N. Harris y Lihan Liu. 2023. ["The Effects of Performance-Based School Closure and Restart on Student Performance."](https://doi.org/10.1016/j.econedurev.2023.102368) *Economics of Education Review* 94: 102368. [Scholar](https://scholar.google.com/scholar_lookup?title=The+effects+of+performance-based+school+closure+and+restart+on+student+performance&doi=10.1016%2Fj.econedurev.2023.102368)
- Elacqua, Gregory, Matías Martínez, Humberto Santos y Daniela Urbina. 2012. ["School Closures in Chile: Access to Quality Alternatives in a School Choice System."](http://www.scielo.cl/pdf/ede/v39n2/art05.pdf) *Estudios de Economía* 39 (2): 179–202. [DOI](https://doi.org/10.4067/S0718-52862012000200005) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closures+in+Chile%3A+Access+to+quality+alternatives+in+a+school+choice+system&doi=10.4067%2FS0718-52862012000200005)
- Grau, Nicolás, Daniel A. Hojman y Alejandra Mizala. 2018. ["School Closure and Educational Attainment: Evidence from a Market-Based System."](http://www.econ.uchile.cl/uploads/publicacion/b5a96b0864935586496a4959e10220c588993d2b.pdf) *Economics of Education Review* 65: 1–17. [DOI](https://doi.org/10.1016/j.econedurev.2018.05.003) · [Scholar](https://scholar.google.com/scholar_lookup?title=School+closure+and+educational+attainment%3A+Evidence+from+a+market-based+system&doi=10.1016%2Fj.econedurev.2018.05.003)
- Holm, Sture. 1979. "A Simple Sequentially Rejective Multiple Test Procedure." *Scandinavian Journal of Statistics* 6 (2): 65–70. <https://www.jstor.org/stable/4615733>.
- Kim, Jeonghyeok. 2024. ["The Long Shadow of School Closures: Impacts on Students’ Educational and Labor Market Outcomes."](https://doi.org/10.26300/AX4M-3Z14) EdWorkingPaper 24-963, Annenberg Institute at Brown University. Documento de trabajo, no artículo revisado por pares. [Scholar](https://scholar.google.com/scholar_lookup?title=The+Long+Shadow+of+School+Closures%3A+Impacts+on+Students%27+Educational+and+Labor+Market+Outcomes&doi=10.26300%2FAX4M-3Z14)
- Larsen, Matthew F. 2020. ["Does Closing Schools Close Doors? The Effect of High School Closings on Achievement and Attainment."](https://doi.org/10.1016/j.econedurev.2020.101980) *Economics of Education Review* 76: 101980. [Scholar](https://scholar.google.com/scholar_lookup?title=Does+closing+schools+close+doors%3F+The+effect+of+high+school+closings+on+achievement+and+attainment&doi=10.1016%2Fj.econedurev.2020.101980)
- Ministerio de Educación de Chile. s. f. "Matrícula por estudiante." Portal de Datos Abiertos. <https://datosabiertos.mineduc.cl/matricula-por-estudiante-2/>. Los cortes y transformaciones locales de esta revisión constan en su protocolo; el portal no certifica por sí solo esos archivos.
- Roth, Jonathan, Pedro H. C. Sant’Anna, Alyssa Bilinski y John Poe. 2023. ["What’s Trending in Difference-in-Differences? A Synthesis of the Recent Econometrics Literature."](https://arxiv.org/pdf/2201.01194) *Journal of Econometrics* 235 (2): 2218–2244. Referencia metodológica para tendencias paralelas, no prueba empírica de ellas en esta serie. [DOI](https://doi.org/10.1016/j.jeconom.2023.03.008) · [Scholar](https://scholar.google.com/scholar_lookup?title=What%E2%80%99s+trending+in+difference-in-differences%3F+A+synthesis+of+the+recent+econometrics+literature&doi=10.1016%2Fj.jeconom.2023.03.008)
- Sant’Anna, Pedro H. C. y Jun Zhao. 2020. ["Doubly Robust Difference-in-Differences Estimators."](https://doi.org/10.1016/j.jeconom.2020.06.003) *Journal of Econometrics* 219 (1): 101–122. Referencia del método cuya estimabilidad se examinó; no produjo efecto estimado aquí. [Scholar](https://scholar.google.com/scholar_lookup?title=Doubly+robust+difference-in-differences+estimators&doi=10.1016%2Fj.jeconom.2020.06.003)
- Servicio de Información de Educación Superior (SIES). s. f. "Bases de datos de estudiantes matriculadas y matriculados en Educación Superior en Chile" y "Base de datos de estudiantes tituladas y titulados en Educación Superior en Chile". Mi Futuro, Ministerio de Educación de Chile. <https://www.mifuturo.cl/bases-de-datos-de-matriculados/>; <https://www.mifuturo.cl/bases-de-datos-titulados/>. Los cortes locales de matrícula y titulación usados aquí están documentados por separado.
