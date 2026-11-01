# Guion para NotebookLM — Extender mi tesis en 3 cucharadas (parte III), versión breve centrada en la serie completa

- **Personajes sintéticos:**
  - **A (conductor, español de España, `es-ES`):** conduce, pide definiciones simples, plantea las dudas metodológicas y cuida el ritmo.
  - **B (experta, español de Chile, `es-CL`):** explica los datos, el método y sus límites, atribuyendo siempre el análisis al artículo de `tres cucharadas punto ce ele`.
- **Duración estimada:** entre catorce y quince minutos. Cada cifra está respaldada en `guion-breve-QA.md`; ninguna referencia de evidencia se lee en voz alta.

---

## Apertura (0:00 – 0:45)

**A:** Cuando cierra un colegio, desde un despacho la respuesta suele ser rápida: se mira el mapa y al lado hay otra escuela con pupitres libres. Pero el mapa enseña edificios, no lo que les pasó a los chavales al año siguiente.

**B:** Eso es lo que mira la tercera parte de la serie publicada en tres cucharadas punto ce ele. Y el dato que abre la conversación es este: diecinueve de diecinueve. En las diecinueve cohortes anuales medibles, el rezago o la salida del registro de quienes perdieron su escuela creció más que el de sus pares. Aun así, el autor escribe que todavía no puede atribuir esa brecha al cierre.

---

## Movimiento 1: Qué se mide y sobre quién (0:45 – 3:15)

**A:** Diecinueve de diecinueve. Antes de entusiasmarnos, ¿de cuántos estudiantes y de cuántas escuelas estamos hablando?

**B:** De setenta y ocho mil novecientas setenta y dos trayectorias estudiantiles, en mil ciento cuarenta y una escuelas regulares que cerraron entre dos mil cinco y dos mil veinticuatro. Y frente a ellas, setecientas treinta y cuatro mil cuatrocientas setenta y dos observaciones de control: estudiantes comparables de escuelas que seguían abiertas.

**A:** ¿Y cómo sabe el artículo que una escuela cerró de verdad?

**B:** Con una regla propia, la Regla de Cierre Escolar Inferido desde los Datos, o RCID versión uno, que funciona como tres coladores: detecta la matrícula que desaparece, descarta anexos y cambios de código, y aparta los traslados en bloque a un solo colegio receptor. No es lo mismo que un curso entero se mude junto a otro edificio a que cada familia tenga que buscar cupo por su cuenta. En toda la serie, de dos mil cinco a dos mil veinticinco, quedan mil seiscientos cuarenta y ocho cierres limpios.

**A:** ¿Y entran todos al análisis?

**B:** No. Solo mil ciento setenta y siete tenían estudiantes de educación regular, de básica o de media, y mil ciento cuarenta y uno encontraron controles comparables. Ojo con eso: el estudio habla de escuelas regulares, no de todo cierre. En escuelas solo de párvulos, de educación especial o de adultos no se puede medir el paso de curso.

**A:** Vale. ¿Y qué se mide exactamente?

**B:** El indicador central es lo que el artículo llama "falla de progresión o rezago": la proporción de estudiantes que al año siguiente no aparecen matriculados o están en un curso inferior al esperado. Y hay que ser honestos con lo que junta: salir del registro y quedar atrasado de curso. Esa cifra no distingue deserción de repitencia.

**A:** ¿Y cómo se compara a unos con otros?

**B:** Con diferencias en diferencias, que compara dos películas en vez de dos fotografías. El diseño empareja a cada alumno, un año antes del cierre, con controles del mismo año, sexo, edad, región, dependencia, ruralidad, nivel y curso, y luego mide cuánto cambió su trayectoria frente al cambio de sus pares. Para la serie completa, además, usa estimadores escalonados, que comparan cada cohorte solo contra escuelas que todavía no han cerrado. Así no se usa como control a un colegio que cierra al año siguiente.

---

## Movimiento 2: El efecto global de la ventana completa, 2005–2024 (3:15 – 8:00)

**A:** Vamos al corazón: veinte cohortes anuales, de dos mil cinco a dos mil veinticuatro. ¿Qué sale?

**B:** Primero, la foto año a año. De las veinte, diecinueve permiten estimar la progresión, de dos mil seis a dos mil veinticuatro. Las diecinueve brechas son positivas. Van de cero coma noventa y cuatro puntos porcentuales a veintiocho coma veintidós, con una mediana de siete coma dieciocho puntos.

**A:** Un rango enorme, de casi uno a veintiocho. ¿Cómo se resume eso en una sola cifra?

**B:** El artículo lo hace de tres maneras, y eso es lo interesante: el signo no depende de cómo promedies. Si das más peso a los años con más alumnos afectados, con el estimador de Callaway y Sant'Anna, la brecha media es de nueve coma once puntos, con un intervalo de cinco coma treinta y cuatro a doce coma ochenta y ocho. Si das el mismo peso a cada año, es de siete coma cincuenta y cinco, entre cinco coma cincuenta y dos y nueve coma cincuenta y siete. Y con un modelo de efectos aleatorios, que admite que la brecha varía entre épocas, es de seis coma veintinueve puntos, con un intervalo de confianza de cuatro coma cuarenta y nueve a ocho coma cero nueve.

**A:** Nueve, siete y medio, seis y pico. ¿Con cuál me quedo?

**B:** El artículo reporta las tres. Como referencia conviene la de efectos aleatorios, por dos razones: es la más moderada, y es la que el autor incorporó en su actualización del treinta y uno de octubre: antes usaba un promedio que suponía un efecto común a todas las cohortes, pero con una heterogeneidad de setenta y seis coma cinco por ciento ese supuesto produce un intervalo artificialmente estrecho.

**A:** ¿Y el intervalo de predicción? Porque eso suena a otra cosa.

**B:** Es otra cosa, y para política pública quizá es lo más útil. El intervalo de confianza dice dónde está el promedio. El de predicción indica dónde podría caer la brecha de una cohorte nueva. Y va de cero coma cero nueve a doce coma cuarenta y nueve puntos. Su extremo inferior queda apenas sobre cero.

**A:** O sea, que para una próxima tanda de cierres, con estos datos, lo esperable es una brecha positiva, que podría ser casi nula o de más de doce puntos.

**B:** Esa es la lectura de los números, si las próximas cohortes se parecen a estas. Pero falta una pieza: no todos los estudiantes tienen su avance registrado al año siguiente. Para esos datos faltantes, el artículo aplica cotas de Manski, que funcionan como una prueba de esfuerzo sin optimismo: a los alumnos sin dato les asignan el peor desenlace en un grupo y el mejor en el otro, y luego al revés. Sobre el agregado de Callaway y Sant'Anna de toda la serie, las cotas van de cero coma cuarenta y tres a dieciséis coma veintiún puntos. Apenas excluyen el cero, pero lo excluyen.

**A:** ¿Y la salida persistente del registro? La de no aparecer dos años seguidos.

**B:** Ahí la señal es más débil. Con efectos aleatorios, la no matrícula persistente da cero coma setenta y nueve puntos, entre cero coma dieciséis y uno coma cuarenta y dos, y su intervalo de predicción, de menos uno coma treinta y cuatro a dos coma noventa y dos, sí incluye el cero.

**A:** ¿Y por épocas? ¿La brecha es estable?

**B:** No, se atenúa. En dos mil cinco a dos mil diez era de doce coma quince puntos; en dos mil once a dos mil quince, siete coma ochenta y dos; en dos mil dieciséis a dos mil diecinueve, cinco coma veintinueve; en dos mil veinte a dos mil veintidós, dos coma setenta; y en dos mil veintitrés y dos mil veinticuatro, dos coma cincuenta y nueve.

**A:** Una escalera descendente. La tentación es decir: llegaron la Subvención Escolar Preferencial, el Sistema de Aseguramiento de la Calidad y la Ley de Inclusión, y funcionaron.

**B:** Y el artículo dice explícitamente que no se les puede atribuir. La caída coincide en el tiempo con esas políticas, pero también cambió el tipo de escuelas que cierran, en dos mil quince cambió la forma de registrar el estado de los colegios, la promoción flexible de la pandemia reduce el rezago de forma mecánica y las muestras se achican. La escalera es un hecho; su causa, no.

---

## Movimiento 3: Por qué la serie completa pesa más que la ventana reciente, y qué la limita (8:00 – 11:45)

**A:** Ahora, el artículo tiene una ventana principal, de dos mil dieciséis a dos mil diecinueve, cuyo resultado es inconcluso. ¿Por qué hoy ponemos el foco en la serie completa?

**B:** Hay tres hechos del artículo que lo justifican. El primero es de tamaño: la ventana principal tiene sesenta y tres escuelas con soporte comparable y, como unas pocas concentran gran parte del alumnado, sus millones de registros pesan como unas veintiuna o veintidós escuelas independientes. La serie completa reúne mil ciento cuarenta y una. El segundo: esa ventana se fijó antes de mirar la serie larga y no es la que más brecha muestra; mirar los veinte años evita que la conclusión dependa de haber elegido un período. El tercero: en la ventana principal la brecha es de cinco coma veintinueve puntos, con intervalo de dos coma cero ocho a ocho coma cincuenta y uno, pero sus cotas por datos faltantes van de menos uno coma quince a diez coma noventa y ocho. Cruzan el cero, y por eso esa ventana, sola, es inconclusa.

**A:** ¿Inconclusa quiere decir que no pasa nada?

**B:** No. Quiere decir que no demuestra por sí sola daño, beneficio ni ausencia de efecto. Y la brecha solo llega a cero si los datos faltantes se acercan en más de un noventa por ciento al escenario más benigno para el cierre.

**A:** Entonces la serie completa es la lectura de fondo. ¿Ya podemos decir que cerrar una escuela causa rezago?

**B:** Todavía no, y el autor es muy claro. Para dimensionar el fenómeno, la serie completa es la lectura de conjunto; para atribuirlo al cierre, faltan piezas. La primera es quiénes eran estos niños, niñas y adolescentes. En la ventana principal, el emparejamiento deja a los dos grupos con la misma edad, el mismo rezago previo y casi la misma vulnerabilidad individual. Pero los expuestos iban a escuelas institucionalmente más frágiles: diez coma cero seis puntos menos de convenio de la Subvención Escolar Preferencial y dieciocho coma cincuenta y cuatro puntos menos de Jornada Escolar Completa. Y el cuarenta y siete coma cero cuatro por ciento ya había cambiado de colegio en los dos años previos, frente al treinta coma cincuenta y dos por ciento de los controles.

**A:** Casi la mitad de los chavales ya venía dando tumbos antes del cierre.

**B:** Exacto: parte del desgaste ya estaba en marcha. Y hay más límites. En la ventana principal, tres pruebas placebo anteriores al cierre dan cero coma dieciséis, cero coma treinta y cero coma cuarenta puntos, todas con intervalos que incluyen el cero; pero eso no prueba que las trayectorias fueran paralelas, y la serie larga todavía no tiene placebos propios. La exposición se mide un año antes del cierre, así que quien se fue antes del anuncio queda fuera, y con tanta rotación esa selección puede pesar. Y como las cohortes comparten controles, incluso los intervalos de efectos aleatorios pueden quedar algo cortos.

**A:** ¿Qué haría falta para cerrar la pregunta causal?

**B:** Dos análisis que el artículo deja pendientes: medir cuánto cambiaría la conclusión sin tendencias paralelas, con el enfoque de Rambachan y Roth, y fijar la exposición dos años antes del cierre. Mientras tanto, la frase justa es la del subtítulo: en diecinueve de diecinueve cohortes, el rezago o la salida del registro de quienes perdieron su escuela creció más que el de sus pares, y todavía no se puede atribuir esa brecha al cierre.

---

## Cierre: dónde va a ocurrir y cómo acompañar (11:45 – 14:30)

**A:** Vamos a lo práctico. Si alguien en un ministerio, un servicio local o un municipio escucha "todavía no es causal" y concluye que no hay nada que hacer…

**B:** Habría entendido todo al revés. El artículo dice que un resultado inconcluso no justifica quedarse de brazos cruzados: el diagnóstico muestra dónde se pierde el rastro de los estudiantes y qué garantías exigir antes, durante y después de reorganizar una red escolar. Antes, verificar capacidad, dotación y calidad de los destinos. Durante, vacantes reales y apoyos para cada estudiante, tiempos de viaje y financiamiento para la escuela receptora. Después, seguir matrícula, asistencia, progresión, notas y bienestar durante al menos dos años, también en las receptoras.

**A:** Y aclara que eso no son efectos estimados.

**B:** Son el estándar mínimo de cuidado público. Una lista de colegios cercanos entregada por el sostenedor no equivale a continuidad educativa.

**A:** Pero la serie completa deja una pregunta encima de la mesa. Si la brecha aparece cohorte tras cohorte, ¿dónde van a ocurrir los próximos cierres?

**B:** Y esa es la conclusión de política que el autor quiere dejar dicha: es crítico evaluar los lugares donde esto va a ocurrir, es decir, dónde se concentrarán los próximos cierres o fusiones, para diseñar a tiempo los planes de mitigación del impacto y de acompañamiento de estudiantes y familias, y para diseñar la transición demográfica del sistema escolar. Ojo: el artículo no trae proyecciones de natalidad ni de matrícula, así que no vamos a inventar cifras ni nombrar comunas. Lo que sí dice es que las caídas demográficas comunales alteran a la vez los recursos, las vacantes y las decisiones de las familias, que sus datos no sustituyen evidencia sobre capacidad, acceso o demografía, y que su exploración entre zonas urbanas y rurales todavía no permite recomendaciones territoriales sin incorporar tiempos de viaje por red vial y transporte escolar. Por eso la pregunta de dónde es la tarea pendiente, y la que decide si la próxima transición se planifica o se improvisa.

**A:** Me quedo con eso. El mapa enseña edificios. La serie completa enseña que, cohorte tras cohorte, el rezago o la salida del registro de quienes pierden su escuela crece más que el de sus pares, aunque todavía no sepamos cuánto se debe al cierre. Y saber dónde ocurrirán los próximos cierres es lo que hay que responder antes de cerrar.

**B:** Las tablas, las figuras y los datos abiertos de cada gráfico están en el artículo, en tres cucharadas punto ce ele.

**A:** Os invitamos a leerlo completo. Esta conversación se elaboró con voces sintéticas a partir de la tercera entrega de la serie "Extender mi tesis en tres cucharadas", escrita por Cristián Labra. Hasta la próxima.
