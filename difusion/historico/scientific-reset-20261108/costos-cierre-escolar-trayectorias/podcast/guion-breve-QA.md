# QA del guion breve para NotebookLM: Post III, centrado en la serie completa

- **Guion:** `guion-breve.md` (mismo directorio).
- **Fuente que manda:** post canónico `costos-cierre-escolar-trayectorias` (<https://3cucharadas.cl/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/>).
- **Fecha:** 1 de noviembre de 2026 (QA revisada el 7 de noviembre de 2026 contra el post reestructurado). Etapa: publicado; audio generado y verificado por escucha humana el 1 de noviembre. El guion está congelado: es el insumo del episodio emitido.
- **Extensión:** `wc -w` sobre el archivo completo da dos mil cuatrocientas veintiséis palabras, encabezados incluidos, bajo el tope de dos mil quinientas.
- **Comprobación de las citas:** cada cifra pronunciada aparece en el post canónico vigente, salvo las tres afirmaciones registradas en la sección 3 como divergencias con la versión del 6 de noviembre.
- **Texto hablado:** sin dígitos en los diálogos (`rg '^\*\*[AB]:\*\*.*[0-9]'` no devuelve líneas), y sin enlaces ni códigos de evidencia.

## 1. Cifras y afirmaciones cuantitativas

| Tal como se pronuncia | Valor | Sección en el post ES | Cita breve del post |
|---|---|---|---|
| "diecinueve de diecinueve", "diecinueve cohortes anuales medibles" | 19 de 19 | Subtítulo y Apertura | "En las 19 cohortes medibles, la estimación puntual del rezago o la salida del registro de quienes perdieron su escuela fue mayor que la de sus pares" |
| "setenta y ocho mil novecientas setenta y dos trayectorias estudiantiles" | 78.972 | Apertura | "seguí **78.972 trayectorias estudiantiles**" |
| "mil ciento cuarenta y una escuelas regulares que cerraron entre dos mil cinco y dos mil veinticuatro" | 1.141; 2005–2024 | Apertura | "en **1.141 escuelas regulares** que cerraron entre 2005 y 2024" |
| "setecientas treinta y cuatro mil cuatrocientas setenta y dos observaciones de control" | 734.472 | Apertura y Cucharada 2 | "**78.972 observaciones expuestas** y **734.472 controles**" |
| "tres coladores" | 3 | Cucharada 1 | "funciona como tres coladores sucesivos" |
| "de dos mil cinco a dos mil veinticinco, quedan mil seiscientos cuarenta y ocho cierres limpios" | 1.648; 2005–2025 | Cucharada 1, Tabla 1 | "deja **1.648 cierres limpios** con ventana posterior observada en toda la serie 2005–2025" |
| "mil ciento setenta y siete tenían estudiantes de educación regular" | 1.177 | Cucharada 1 | "solo **1.177** tenían estudiantes de educación regular" |
| "mil ciento cuarenta y uno encontraron controles comparables" | 1.141 | Cucharada 1 | "y **1.141** encontraron controles comparables" |
| "empareja a cada alumno, un año antes del cierre" | G−1 | Cucharada 2 | "estudiantes de control idénticos un año antes del cierre (G−1)" |
| "veinte cohortes anuales, de dos mil cinco a dos mil veinticuatro"; "mirar los veinte años" | 20; 2005–2024 | Cucharada 2 | "las veinte cohortes anuales entre **2005 y 2024**" |
| "diecinueve permiten estimar la progresión, de dos mil seis a dos mil veinticuatro" | 19; 2006–2024 | Cucharada 2, Figura 2 | "las 19 cohortes anuales estimables de falla de progresión o rezago entre 2006 y 2024: las 19 son positivas" |
| "de cero coma noventa y cuatro puntos porcentuales a veintiocho coma veintidós" | +0,94 a +28,22 pp | Apertura y Tabla 4 | "+0,94 a +28,22 (mediana: +7,18)" |
| "una mediana de siete coma dieciocho puntos" | +7,18 pp | Apertura y Tabla 4 | "(mediana: +7,18)" |
| "de tres maneras" | 3 agregados | Cucharada 2 | "tres formas distintas de agregar las dos décadas" |
| "nueve coma once puntos, con un intervalo de cinco coma treinta y cuatro a doce coma ochenta y ocho" | +9,11 [+5,34; +12,88] | Apertura y Tabla 4 | "la brecha media es de **+9,11 puntos porcentuales** (intervalo de confianza del 95 % de **+5,34 a +12,88**)" |
| "siete coma cincuenta y cinco, entre cinco coma cincuenta y dos y nueve coma cincuenta y siete" | +7,55 [+5,52; +9,57] | Cucharada 2, Tabla 4 | "Con pesos iguales por cohorte anual es de **+7,55 puntos** ([+5,52; +9,57])" |
| "seis coma veintinueve puntos, con un intervalo de confianza de cuatro coma cuarenta y nueve a ocho coma cero nueve" | +6,29 [+4,49; +8,09] | Apertura y Tabla 4 | "la media es de **+6,29 puntos** ([+4,49; +8,09])" |
| "una heterogeneidad de setenta y seis coma cinco por ciento" | I² = 76,5 % | Cucharada 2, Tabla 4 | "con una heterogeneidad de 76,5 % produce un intervalo artificialmente estrecho" |
| "va de cero coma cero nueve a doce coma cuarenta y nueve puntos" | [+0,09; +12,49] | Cucharada 2, Tabla 4 | "con un intervalo de predicción de **+0,09 a +12,49 puntos**" |
| "las cotas van de cero coma cuarenta y tres a dieciséis coma veintiún puntos" | [+0,43; +16,21] | Apertura y Tabla 4 | "sus cotas de Manski (**+0,43 a +16,21**) se mantienen sobre cero" |
| "no aparecer dos años seguidos" | 2 años | Cucharada 2 | "**sin matrícula durante dos años seguidos**" |
| "cero coma setenta y nueve puntos, entre cero coma dieciséis y uno coma cuarenta y dos" | +0,79 [+0,16; +1,42] | Cucharada 2, Tabla 4 | "fila de efectos aleatorios, columna de no matrícula: **+0,79** \| **[+0,16; +1,42]**" |
| "de menos uno coma treinta y cuatro a dos coma noventa y dos" | [−1,34; +2,92] | Cucharada 2, Tabla 4 | "predicción [−1,34; +2,92]" |
| "En dos mil cinco a dos mil diez era de doce coma quince puntos" | +12,15 pp | Apertura y Tabla 4 | "en **2005–2010** ... la falla de progresión subió **+12,15 puntos porcentuales**" |
| "en dos mil once a dos mil quince, siete coma ochenta y dos" | +7,82 | Apertura y Tabla 4 | "En **2011–2015** ... la brecha de progresión fue de **+7,82 puntos**" |
| "en dos mil dieciséis a dos mil diecinueve, cinco coma veintinueve" | +5,29 | Apertura y Tabla 4 | "baja a **+5,29 puntos porcentuales** en **2016–2019** (con cotas de **−1,15 a 10,98 puntos**)" |
| "en dos mil veinte a dos mil veintidós, dos coma setenta" | +2,70 | Apertura y Tabla 4 | "a **+2,70 puntos** en **2020–2022**" |
| "en dos mil veintitrés y dos mil veinticuatro, dos coma cincuenta y nueve" | +2,59 | Apertura y Tabla 4 | "y a **+2,59 puntos** en **2023–2024**" |
| "en dos mil quince cambió la forma de registrar el estado de los colegios" | 2015 | Cucharada 2 | "la forma de registrar el estado de los colegios en 2015" |
| "ventana principal, de dos mil dieciséis a dos mil diecinueve" | 2016–2019 | Apertura | "la subventana **2016–2019** —el corte que fijé como ventana principal antes de mirar la serie completa" |
| "sesenta y tres escuelas con soporte comparable" | 63 | Apertura y Cucharada 2 | "**63 de los 1.141 episodios con soporte**" |
| "pesan como unas veintiuna o veintidós escuelas independientes" | 21 o 22 | Apertura | "pesa estadísticamente como unas **21 o 22 escuelas independientes**" |
| "cinco coma veintinueve puntos, con intervalo de dos coma cero ocho a ocho coma cincuenta y uno" | +5,29 [2,08; 8,51] | Apertura y Cucharada 2 | "subió **5,29 puntos porcentuales** ... de **2,08 a 8,51 puntos**" |
| "de menos uno coma quince a diez coma noventa y ocho" | [−1,15; 10,98] | Apertura y Cucharada 2 | "van de **−1,15 a 10,98 puntos porcentuales**" |
| "diez coma cero seis puntos menos de convenio de la Subvención Escolar Preferencial" | −10,06 pp | Cucharada 1, Tabla 3 | "con menos convenio SEP (−10,06 pp)" |
| "dieciocho coma cincuenta y cuatro puntos menos de Jornada Escolar Completa" | −18,54 pp | Cucharada 1, Tabla 3 | "menos Jornada Escolar Completa (−18,54 pp)" |
| "el cuarenta y siete coma cero cuatro por ciento … frente al treinta coma cincuenta y dos por ciento" | 47,04 % frente a 30,52 % | Cucharada 1, Tabla 3 | "casi la mitad (**47,04 %** frente a 30,52 %) ya había cambiado de colegio en los dos años previos" |
| "tres pruebas placebo … cero coma dieciséis, cero coma treinta y cero coma cuarenta puntos" | +0,16; +0,30; +0,40 | Cucharada 2 y Apéndice | "tres pruebas placebo anteriores al cierre en 2016–2019 dan diferencias de +0,16, +0,30 y +0,40 puntos" |
| "La exposición se mide un año antes del cierre" | G−1 | Cucharada 1 | "solo cuento como expuestos a quienes seguían matriculados en G−1" |
| "durante al menos dos años" | ≥ 2 años | Cucharada 3 | "monitorear nominalmente qué pasa con cada estudiante durante al menos dos años" |
| "la tercera parte de la serie", "la tercera entrega" | parte III | Título y Apertura | "(parte III)"; "Esta tercera entrega" |

## 2. Afirmaciones no numéricas y su estado epistémico

| Afirmación del guion | Estado | Respaldo en el post |
|---|---|---|
| El autor todavía no puede atribuir la brecha al cierre por sí solo | Hecho | Subtítulo y Apertura |
| La "falla de progresión o rezago" junta salir del registro y quedar atrasado, y no distingue deserción de repitencia | Hecho | Apertura y Cucharada 2 |
| El diseño de diferencias en diferencias "compara dos películas"; el emparejamiento usa año, sexo, edad, región, dependencia, ruralidad, nivel y curso | Hecho | Cucharada 2 |
| Los estimadores escalonados comparan cada cohorte solo contra escuelas que aún no han cerrado | Hecho | Cucharada 2 |
| El intervalo de predicción indica dónde podría caer la brecha de una cohorte nueva | Hecho | Cucharada 2 |
| Las cotas de Manski funcionan como una "prueba de esfuerzo sin optimismo" | Hecho | Cucharada 2 |
| La atenuación por régimen coincide con la SEP, el SAC y la Ley de Inclusión, pero no se les puede atribuir de forma directa | Hecho | Cucharada 2 |
| La ventana 2016–2019 se fijó antes de ver la serie y por sí sola es evidencia parcial e inconclusa | Hecho | Apertura y Cucharada 2 |
| Escuelas de origen institucionalmente más frágiles; parte del desgaste ya estaba en marcha | Hecho | Cucharada 1 |
| Un resultado inconcluso no justifica la pasividad; resguardos antes, durante y después | Hecho | Cucharada 3 y Cierre |
| Los resguardos prudenciales no son efectos estimados de esas decisiones; son el estándar mínimo de cuidado público | Hecho | Cucharada 3 y Cierre |
| Una lista de colegios cercanos entregada por el sostenedor no equivale a continuidad educativa | Hecho | Cucharada 3 y Cierre |
| El modelo de efectos aleatorios es "el más moderado" de los tres | Deducción: 6,29 < 7,55 < 9,11 | Cucharada 2, Tabla 4 |
| Se usa el modelo de efectos aleatorios como referencia para conversar | Decisión editorial del guion, no jerarquía del post; el guion dice que el artículo reporta las tres | Cucharada 2 |
| La serie larga no tiene placebos propios; queda fuera quien se fue antes del anuncio; los intervalos pueden quedar cortos | Hecho | Cucharada 1 y Cucharada 2 |

## 3. Divergencias con el post reestructurado el 6 de noviembre de 2026

El guion se escribió y grabó contra la versión del post del 1 de noviembre. Tres pasajes ya no tienen respaldo literal en la versión vigente; se registran y no se corrigen, porque el audio ya está emitido.

| Pasaje del guion | Estado hoy | Qué dice el post vigente |
|---|---|---|
| "Dos análisis que el artículo deja pendientes: … Rambachan y Roth, y fijar la exposición dos años antes del cierre" | Desactualizado | Ambos están hechos: umbral de 2,54 veces el tope previo de 0,81 pp; +3,87 pp [+1,04; +6,69] en estables desde G−2 y +9,58 pp [+5,06; +14,10] en entrantes tardíos (Cucharada 2 y Apéndice) |
| "la brecha solo llega a cero si los datos faltantes se acercan en más de un noventa por ciento al escenario más benigno" | Sin respaldo literal | La condición vigente es que las cotas excluyen el cero solo en cierres con al menos 90 % de actas válidas en G−1 (38 % de los expuestos) |
| "la que el autor incorporó en su actualización del treinta y uno de octubre" | Sin respaldo literal | El post ya no lleva esa nota de actualización fechada; la justificación (I² = 76,5 % e intervalo artificialmente estrecho) sí sigue en la Cucharada 2 |

## 4. Verificación tras generación del audio (1 de noviembre de 2026)

- [x] Las cifras del eje global se pronuncian con fidelidad (+6,29 [4,49; 8,09], predicción [0,09; 12,49], 19 de 19, 1.141 escuelas y 78.972 trayectorias).
- [x] El audio no presenta la brecha como un efecto causal demostrado ni atribuye la atenuación a la SEP, el SAC o la Ley de Inclusión.
- [x] La recomendación final se expresa como estándar prudencial, sin proyecciones ni comunas inventadas.
