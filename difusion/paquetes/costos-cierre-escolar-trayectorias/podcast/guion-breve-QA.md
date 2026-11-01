# QA del guión breve para NotebookLM: Post III, centrado en la serie completa

- **Guión:** `guion-breve.md` (mismo directorio).
- **Fuente que manda:** `_posts/2026-10-23-costos-cierre-escolar-trayectorias.md`, ruta relativa al repo `activos/3cucharadas`; se abrevia como `post` en las tablas, así que `post:206` es la línea 206 de ese archivo.
- **Fecha:** 2026-11-01. Etapa: borrador listo para enviar; la escucha humana queda pendiente hasta que exista el audio.
- **Extensión:** `wc -w` sobre el archivo completo da 2.426 palabras, encabezados incluidos. El límite era 2.500.
- **Comprobación de las líneas:** un script comprobó que cada cita aparece literalmente en la línea indicada del post (103 patrones del guión, 0 ausentes tras corregir un número de línea propio; las 53 citas de esta tabla, 0 ausentes tras corregir una).
- **Texto hablado:** sin dígitos en los diálogos (`rg '[0-9]'` solo encuentra encabezados), y sin enlaces ni códigos EV.

## 1. Cifras y afirmaciones cuantitativas

| # | Tal como se pronuncia | Valor | Post ES (`archivo:línea`) | Cita breve del post |
|---:|---|---|---|---|
| 1 | "diecinueve de diecinueve", "diecinueve cohortes anuales medibles" | 19 de 19 | `post:5` | "En 19 de 19 cohortes, el rezago o la salida del registro … creció más que el de sus pares" |
| 2 | "setenta y ocho mil novecientas setenta y dos trayectorias estudiantiles" | 78.972 | `post:46` | "seguí **78.972 trayectorias estudiantiles**" |
| 3 | "mil ciento cuarenta y una escuelas regulares que cerraron entre dos mil cinco y dos mil veinticuatro" | 1.141; 2005–2024 | `post:46` | "en **1.141 escuelas regulares** que cerraron entre 2005 y 2024" |
| 4 | "setecientas treinta y cuatro mil cuatrocientas setenta y dos observaciones de control" | 734.472 | `post:188` | "**78.972 observaciones expuestas** y **734.472 controles**" |
| 5 | "tres coladores" | 3 | `post:90` | "funciona como tres coladores sucesivos" |
| 6 | "de dos mil cinco a dos mil veinticinco, quedan mil seiscientos cuarenta y ocho cierres limpios" | 1.648; 2005–2025 | `post:90` | "deja **1.648 cierres limpios** con ventana posterior observada en toda la serie 2005–2025" |
| 7 | "mil ciento setenta y siete tenían estudiantes de educación regular" | 1.177 | `post:96` | "Solo **1.177** tenían estudiantes de educación regular" |
| 8 | "mil ciento cuarenta y uno encontraron controles comparables" | 1.141 | `post:96` | "y **1.141** encontraron controles comparables" |
| 9 | "empareja a cada alumno, un año antes del cierre" | G−1 | `post:177` | "estudiantes de control idénticos un año antes del cierre (G−1)" |
| 10 | "veinte cohortes anuales, de dos mil cinco a dos mil veinticuatro"; "mirar los veinte años" | 20; 2005–2024 | `post:188` | "las veinte cohortes anuales entre 2005 y 2024" |
| 11 | "diecinueve permiten estimar la progresión, de dos mil seis a dos mil veinticuatro" | 19; 2006–2024 | `post:196` | "las 19 cohortes anuales estimables … entre 2006 y 2024: las 19 son positivas" |
| 12 | "de cero coma noventa y cuatro puntos porcentuales a veintiocho coma veintidós" | +0,94 a +28,22 pp | `post:327` | "+0,94 a +28,22 (mediana: +7,18)" |
| 13 | "una mediana de siete coma dieciocho puntos" | +7,18 pp | `post:327` | "(mediana: +7,18)" |
| 14 | "de casi uno a veintiocho" (redondeo del conductor) | 0,94 y 28,22 | `post:327` | mismo rango que el #12 |
| 15 | "de tres maneras" | 3 agregados | `post:188` | "tres formas distintas de promediar la serie" |
| 16 | "nueve coma once puntos, con un intervalo de cinco coma treinta y cuatro a doce coma ochenta y ocho" | +9,11 [+5,34; +12,88] | `post:206` | "la diferencia media es de **+9,11 puntos** ([+5,34; +12,88])" |
| 17 | "siete coma cincuenta y cinco, entre cinco coma cincuenta y dos y nueve coma cincuenta y siete" | +7,55 [+5,52; +9,57] | `post:206` | "Con el mismo peso para cada año, es de **+7,55 puntos** ([+5,52; +9,57])" |
| 18 | "seis coma veintinueve puntos, con un intervalo de confianza de cuatro coma cuarenta y nueve a ocho coma cero nueve" | +6,29 [+4,49; +8,09] | `post:206` | "da **+6,29 puntos** ([+4,49; +8,09])" |
| 19 | "Nueve, siete y medio, seis y pico" (redondeo del conductor) | 9,11; 7,55; 6,29 | `post:206` | mismas cifras que los #16 a #18 |
| 20 | "actualización del treinta y uno de octubre" | 2026-10-31 | `post:61` | "Actualización del 31 de octubre de 2026 … reemplacé un promedio de efecto fijo por uno de efectos aleatorios" |
| 21 | "una heterogeneidad de setenta y seis coma cinco por ciento" | I² = 76,5 % | `post:333` | "con una heterogeneidad de 76,5 % produce un intervalo artificialmente estrecho" |
| 22 | "va de cero coma cero nueve a doce coma cuarenta y nueve puntos"; "más de doce puntos" | [+0,09; +12,49] | `post:206` | "su intervalo de predicción, **+0,09 a +12,49**, indica dónde podría caer la brecha de una cohorte nueva" |
| 23 | "las cotas van de cero coma cuarenta y tres a dieciséis coma veintiún puntos" | [+0,43; +16,21] | `post:206` | "sus cotas de Manski (**+0,43 a +16,21**) apenas excluyen el cero" |
| 24 | "no aparecer dos años seguidos" | 2 años | `post:139` | "**sin matrícula durante dos años seguidos**" |
| 25 | "cero coma setenta y nueve puntos, entre cero coma dieciséis y uno coma cuarenta y dos" | +0,79 [+0,16; +1,42] | `post:330` | fila de efectos aleatorios, columna de no matrícula: "**+0,79** \| **[+0,16; +1,42]**" |
| 26 | "de menos uno coma treinta y cuatro a dos coma noventa y dos" | [−1,34; +2,92] | `post:330` | "predicción [−1,34; +2,92]" |
| 27 | "En dos mil cinco a dos mil diez era de doce coma quince puntos" | +12,15 pp | `post:205` | "**+12,15 puntos porcentuales** en 2005–2010" |
| 28 | "en dos mil once a dos mil quince, siete coma ochenta y dos" | +7,82 | `post:205` | "**+7,82** en 2011–2015" |
| 29 | "en dos mil dieciséis a dos mil diecinueve, cinco coma veintinueve" | +5,29 | `post:205` | "**+5,29** en 2016–2019" |
| 30 | "en dos mil veinte a dos mil veintidós, dos coma setenta" | +2,70 | `post:205` | "**+2,70** en 2020–2022" |
| 31 | "en dos mil veintitrés y dos mil veinticuatro, dos coma cincuenta y nueve" | +2,59 | `post:205` | "**+2,59** en 2023–2024" |
| 32 | "en dos mil quince cambió la forma de registrar el estado de los colegios" | 2015 | `post:205` | "la forma de registrar el estado de los colegios en 2015" |
| 33 | "ventana principal, de dos mil dieciséis a dos mil diecinueve" | 2016–2019 | `post:49` | "En la ventana que fijé antes de mirar la serie completa, 2016–2019" |
| 34 | "sesenta y tres escuelas con soporte comparable" | 63 | `post:139` | "los **63 episodios con soporte comparable**" |
| 35 | "pesan como unas veintiuna o veintidós escuelas independientes" | 21 o 22 | `post:52` | "pesan como unas **21 o 22 escuelas independientes**" |
| 36 | "La serie completa reúne mil ciento cuarenta y una" | 1.141 | `post:188` | "**1.141 episodios con soporte empírico**" |
| 37 | "cinco coma veintinueve puntos, con intervalo de dos coma cero ocho a ocho coma cincuenta y uno" | +5,29 [2,08; 8,51] | `post:49` | "subió 5,29 puntos porcentuales más … de **2,08 a 8,51 puntos**" |
| 38 | "de menos uno coma quince a diez coma noventa y ocho" | [−1,15; 10,98] | `post:49` | "el rango posible va de **−1,15 a 10,98 puntos porcentuales**" |
| 39 | "en más de un noventa por ciento al escenario más benigno" | > 90 % | `post:142` | "la brecha solo llega a cero cuando los datos faltantes se acercan en más de un **90 %** a la asignación más benigna" |
| 40 | "diez coma cero seis puntos menos de convenio de la Subvención Escolar Preferencial" | −10,06 pp | `post:132` | "con menos convenio SEP (−10,06 pp)" |
| 41 | "dieciocho coma cincuenta y cuatro puntos menos de Jornada Escolar Completa" | −18,54 pp | `post:132` | "menos Jornada Escolar Completa (−18,54 pp)" |
| 42 | "el cuarenta y siete coma cero cuatro por ciento … frente al treinta coma cincuenta y dos por ciento" | 47,04 % frente a 30,52 % | `post:132` | "casi la mitad (**47,04 %** frente a 30,52 %) ya había cambiado de colegio en los dos años previos" |
| 43 | "Casi la mitad de los chavales" | 47,04 % | `post:132` | "casi la mitad" |
| 44 | "en los dos años previos" | G−3 a G−1 | `post:132` | "en los dos años previos" |
| 45 | "tres pruebas placebo … cero coma dieciséis, cero coma treinta y cero coma cuarenta puntos" | +0,16; +0,30; +0,40 | `post:207` | "tres pruebas placebo anteriores al cierre dan diferencias de +0,16, +0,30 y +0,40 puntos" |
| 46 | "La exposición se mide un año antes del cierre" | G−1 | `post:207` | "la exposición se mide un año antes del cierre" |
| 47 | "Dos análisis … fijar la exposición dos años antes del cierre" | 2 análisis; G−2 | `post:207` | "con la exposición fijada dos años antes. Ambos análisis siguen pendientes" |
| 48 | "durante al menos dos años" | ≥ 2 años | `post:243` | "monitorear nominalmente … durante al menos dos años" |
| 49 | "la tercera parte de la serie", "la tercera entrega" | parte III | `post:4`, `post:58` | "(parte III)"; "Esta tercera entrega" |

No hubo que eliminar ninguna cifra del guión: todas tienen su línea. Se descartaron antes de escribir dos cifras que aparecen en el guión anterior y ya no corresponden al post: la pretendencia de −1,49 puntos, que la actualización retiró (`post:61`: "Retiré una cifra de pretendencia que no tenía respaldo reproducible"), y el 76,8 % atribuido a la cobertura del grupo de comparación en asistencia, que el post no presenta así.

## 2. Afirmaciones no numéricas y su estado epistémico

| Afirmación del guión | Estado | Respaldo |
|---|---|---|
| El autor todavía no puede atribuir la brecha al cierre | Hecho: lo dice el post | `post:5`, `post:46` |
| La "falla de progresión o rezago" junta salir del registro y quedar atrasado, y no distingue deserción de repitencia | Hecho | `post:49`, `post:145` |
| El diseño de diferencias en diferencias "compara dos películas"; el emparejamiento usa año, sexo, edad, región, dependencia, ruralidad, nivel y curso | Hecho | `post:177` |
| Los estimadores escalonados comparan cada cohorte solo contra escuelas que aún no han cerrado | Hecho | `post:188` |
| "El signo no depende de cómo promedies" | Hecho: "se promedien como se promedien" | `post:206` |
| El modelo de efectos aleatorios es "el más moderado" de los tres | Deducción: 6,29 < 7,55 < 9,11 | `post:206` |
| Se usa el modelo de efectos aleatorios como referencia para conversar | Decisión editorial del guión, no jerarquía del post; el guión dice que el artículo reporta las tres | `post:61`, `post:206`, `post:333` |
| El intervalo de predicción indica dónde podría caer la brecha de una cohorte nueva | Hecho | `post:206` |
| "Si las próximas cohortes se parecen a estas" | Cautela interpretativa del guión, sin cifra; acota la lectura del intervalo de predicción | — |
| Las cotas de Manski funcionan como una "prueba de esfuerzo sin optimismo" | Hecho | `post:142` |
| En no matrícula persistente "la señal es más débil" | Interpretación sobre cifras del post: estimación menor y un intervalo de predicción que incluye el cero | `post:330` |
| La atenuación por régimen coincide con la SEP, el SAC y la Ley de Inclusión, pero no se les puede atribuir | Hecho; el guión la presenta como hecho y su causa como pregunta abierta | `post:205` |
| La ventana 2016–2019 se fijó antes de ver la serie y no es la que más brecha muestra | Hecho | `post:205` |
| "Mirar los veinte años evita que la conclusión dependa de haber elegido un período" | Interpretación del guión, apoyada en el hecho anterior | `post:205` |
| La ventana principal no demuestra daño, beneficio ni ausencia de efecto | Hecho | `post:49` |
| Escuelas de origen institucionalmente más frágiles; parte del desgaste ya estaba en marcha | Hecho | `post:132` |
| La serie larga no tiene placebos propios; queda fuera quien se fue antes del anuncio; los intervalos pueden quedar cortos | Hecho | `post:207`, `post:333` |
| Siguen pendientes la sensibilidad de Rambachan y Roth y la exposición fijada dos años antes | Hecho | `post:207` |
| Un resultado inconcluso no justifica la pasividad; resguardos antes, durante y después | Hecho | `post:229`, `post:238`–`post:240`, `post:243` |
| Los resguardos no son efectos estimados; son el estándar mínimo de cuidado público | Hecho | `post:251` |
| Una lista de colegios cercanos entregada por el sostenedor no equivale a continuidad | Hecho | `post:243`, `post:251` |
| **Conclusión de política del autor:** es crítico evaluar los lugares donde ocurrirán los próximos cierres o fusiones, para diseñar los planes de mitigación y de acompañamiento de estudiantes y familias, y la transición demográfica | **Recomendación del autor por encargo del 2026-11-01. No aparece literal en el post.** El guión la presenta como recomendación y pregunta pendiente, sin cifras ni lugares | Apoyos en el post: `post:172` (sin recomendaciones territoriales hasta incorporar tiempos de viaje), `post:229` y `post:251` (reorganizar una red escolar), `post:291` (los datos no sustituyen evidencia sobre demografía), `post:338` (las caídas demográficas comunales alteran recursos, vacantes y decisiones de las familias) |
| "El artículo no trae proyecciones de natalidad ni de matrícula" | Hecho verificado por búsqueda: `rg -i 'demogr\|natalidad'` sobre el post solo encuentra `post:291`, `post:307` ("sociodemográfica", sobre comparabilidad) y `post:338`; ninguna trae proyecciones | — |
| Autoría de Cristián Labra | Deducción: el autor declara su coautoría del documento de 2014 y la referencia lo nombra | `post:215`, `post:371` |

## 3. Pendiente después de generar el audio

- [ ] Que las cifras del eje global se oigan bien: +6,29 [4,49; 8,09], la predicción [0,09; 12,49], 19 de 19, 1.141 escuelas y 78.972 trayectorias.
- [ ] Que NotebookLM no presente la brecha como un efecto causal ni atribuya la atenuación a la SEP, el SAC o la Ley de Inclusión.
- [ ] Que la recomendación final suene como recomendación del autor, sin proyecciones ni comunas inventadas.
- [ ] Que los acentos salgan distintos (A `es-ES`, B `es-CL`), o anotarlo si no.
