# LinkedIn — Paquete nativo (ES principal + variante EN)

> Nota operativa: en LinkedIn el enlace canónico va incluido directamente en el cuerpo (no usar el «truco del primer comentario»).

---

## Versión nativa en español (principal)

Cuando cierra una escuela, la discusión suele terminar al mirar un mapa: si hay otro establecimiento con cupos a un par de kilómetros, se da por resuelta la transición.

Pero un mapa muestra edificios, no trayectorias estudiantiles.

Acabo de publicar en **3 Cucharadas** la parte III de la serie *«Extender mi tesis en 3 cucharadas»*, donde pasamos de los directorios y mapas a seguir trayectorias individuales sobre veinte años de datos administrativos del MINEDUC (**79.709.054** registros de matrícula y **73.873.835** de rendimiento entre 2004 y 2025):

🔗 https://3cucharadas.cl/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=linkedin&utm_medium=social&utm_campaign=tesis_post3

Cuatro aprendizajes que deja el análisis:

1️⃣ **No toda baja administrativa es una dispersión estudiantil (`RCID v1`).**
De **1.981** salidas brutas de directorio entre 2005 y 2025 (**1.807** cierres estrictos de oferta), el seguimiento de flujos permite apartar las absorciones concentradas o fusiones de facto donde un solo colegio recibe al menos el 70 % de los alumnos trasladados (y ≥ 15 estudiantes). Eso deja **1.648 cierres limpios** con ventana posterior observada (**266** en la década reciente).

2️⃣ **Un intervalo de confianza positivo puede volverse inconcluso al transparentar los datos faltantes.**
En la ventana principal reciente (**2016–2019**, 62 episodios), la falla de progresión o rezago al año siguiente aumenta en **+5,29 puntos porcentuales** más entre los estudiantes expuestos que en su grupo de comparación emparejado (IC 95 %: **2,08 a 8,51 puntos**; en no matrícula por dos años la diferencia es **+0,63 puntos**, IC **[−0,77; 2,03]**). Sin embargo, al aplicar cotas de Manski (2003) sin supuestos optimistas para los registros faltantes, el rango posible va de **−1,15 a 10,98 puntos porcentuales**. Como cruza cero, el resultado de esa ventana es formalmente **inconcluso**. Además, por la concentración de alumnos en pocos cierres grandes, 62 escuelas equivalen a solo **21,9 episodios efectivos** en progresión (**21,1** en no matrícula y **17,7** en asistencia y notas exploratorias).

3️⃣ **Comparar «peras con peras» en G−1 revela fragilidad institucional y rotación previa.**
Tras emparejar exactamente por año, sexo, región, dependencia, ruralidad, nivel y curso un año antes del cierre, la edad (**11,70 años**) y la elegibilidad individual para la Subvención Escolar Preferencial (**30,68 %** de alumnos prioritarios y **54,51 %** elegibles totales) quedan equilibradas. Pero los niños expuestos venían de escuelas con menos convenio SEP (**−10,06 pp**), menos Jornada Escolar Completa (**−18,54 pp**), menor cobertura de actas previas (**−19,4 pp**) y casi la mitad (**47,04 %** frente a **30,52 %** en los controles) ya había cambiado de colegio al menos una vez en los dos años anteriores al cierre.

4️⃣ **La serie completa 2005–2024 muestra atenuación entre regímenes, pero no reemplaza un experimento.**
Al estimar las **20 cohortes anuales (2005–2024, 1.141 episodios con soporte, 78.972 expuestos y 734.472 controles)** con diferencias en diferencias escalonadas (Callaway y Sant'Anna 2021), la brecha de progresión baja progresivamente desde **+12,15 pp** (2005–2010) y **+7,82 pp** (2011–2015) hasta **+5,29 pp** (2016–2019, cotas **[−1,15; 10,98]**), **+2,70 pp** (2020–2022) y **+2,59 pp** (2023–2024), con un agregado ponderado de **+9,11 pp** (cotas de Manski **[+0,43; +16,21] pp**) y **+5,14 pp** por varianza inversa. Aun así, por la movilidad previa no es una prueba experimental, y esto cambia la pregunta de política pública: antes de cerrar o reorganizar una escuela, la autoridad debe acreditar vacantes reales, transporte seguro, convenio SEP y seguimiento nominal por al menos dos años como resguardos prudenciales.

En el post encontrarán las 7 tablas, las 4 visualizaciones interactivas y los CSV abiertos con toda la serie.

#Educación #PolíticaPública #DatosAbiertos #InferenciaCausal #Chile #Econometría

---

## English variant

When a school closes, policy discussions often stop at the map: if another school sits a mile away, the transition is assumed to be covered.

In Part III of my *“Extending My Thesis in Three Spoonfuls”* series on **3 Cucharadas**, we move from school maps to individual student trajectories across 20 years of Chilean administrative records (**79,709,054** enrolment rows and **73,873,835** performance rows, 2004–2025):

🔗 https://3cucharadas.cl/en/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/?utm_source=linkedin&utm_medium=social&utm_campaign=tesis_post3_en

Key takeaways:
• **Paper exits vs. real student dispersion (`RCID v1`):** Filtering out *de facto* mergers (where a single school absorbs ≥70% and ≥15 relocated students) narrows 1,981 raw exits and 1,807 strict closures to **1,648 clean closures** with observed post-closure windows.
• **Why missing-data bounds matter:** In our primary 2016–2019 window, 1-year progression failure or grade lag rises by **+5.29 pp** (95% CI: **2.08 to 8.51 pp**; 2-year non-enrolment is **+0.63 pp**, CI **[−0.77, 2.03]**). Once we apply assumption-free **Manski (2003) bounds** for missing records, however, the interval spans **−1.15 to 10.98 pp**—making the main-window estimate formally **inconclusive**.
• **Pre-existing fragility at G−1:** While exact matching balances age (**11.70 years**) and individual poverty eligibility (**30.68%** priority students), **47.04%** of exposed students had already switched schools between G−3 and G−1 (vs. **30.52%** of controls).
• **20-year staggered DiD (2005–2024):** Across **1,141 supported closures** (**78,972** exposed, **734,472** controls), the progression gap attenuated from **+12.15 pp** (2005–2010) and **+7.82 pp** (2011–2015) to **+5.29 pp** (2016–2019; bounds **[−1.15, 10.98]**), with a Callaway & Sant'Anna aggregate of **+9.11 pp** (Manski bounds **[+0.43, +16.21] pp**) and **+5.14 pp** under inverse-variance weighting.

#EducationPolicy #CausalInference #Econometrics #OpenData #PublicPolicy
