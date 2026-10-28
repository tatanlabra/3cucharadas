# Fuente editorial para NotebookLM — Extender mi tesis en 3 cucharadas (parte III): qué muestran las trayectorias después del cierre de una escuela

- **Artículo de origen:** Extender mi tesis en 3 cucharadas (parte III): qué muestran las trayectorias después del cierre de una escuela
- **Autor:** Cristián Labra (`3cucharadas.cl`)
- **URL canónica:** `https://3cucharadas.cl/datos/educacion/politica-publica/costos-cierre-escolar-trayectorias/`
- **Fecha de referencia:** 28 de octubre de 2026

---

## 1. Tesis central y alcance epistémico

Cuando una escuela cierra, la pregunta de política pública no se responde encontrando otro colegio cercano en el mapa: importa saber si sus estudiantes continuaron matriculados, avanzaron al curso esperado y sostuvieron su asistencia, y sobre todo distinguir qué parte de las dificultades posteriores proviene del cierre y qué parte venía acumulándose antes.

El artículo presenta una reestimación posterior al piloto (versión 3.1) sobre veinte años de registros administrativos del Ministerio de Educación de Chile (MINEDUC) entre 2004 y 2025, enlazando 79.709.054 registros de matrícula y 73.873.835 registros de rendimiento anual.

Su conclusión central es deliberadamente exigente:
1. En la ventana principal reciente (cohortes 2016 a 2019), la proporción de estudiantes sin matrícula o bajo el curso esperado al año siguiente —llamada «falla de progresión o rezago»— aumentó en **+5,29 puntos porcentuales** más entre los estudiantes expuestos que en su grupo de comparación emparejado (intervalo de confianza conservador del 95 %: **2,08 a 8,51 puntos**).
2. Sin embargo, como la progresión al año siguiente no se observa para todos los alumnos, al calcular cotas sin supuestos optimistas para los datos faltantes (cotas de Manski), el rango posible va de **−1,15 a 10,98 puntos porcentuales**. Como ese rango cruza cero, el resultado de la ventana principal es **inconcluso**: no demuestra por sí solo daño, beneficio ni ausencia de efecto.
3. En cambio, al reconstruir las veinte cohortes anuales completas entre 2005 y 2024 bajo la Regla de Cierre Escolar Inferido desde los Datos (`RCID v1`, 1.141 episodios con soporte, 78.972 observaciones expuestas y 734.472 controles), las 19 cohortes evaluables de progresión muestran diferencias positivas, con un agregado escalonado de Callaway y Sant'Anna de **+9,11 puntos porcentuales** (intervalo: **+5,34 a +12,88**; cotas de Manski: **+0,43 a +16,21 puntos**, que no cruzan cero) y un agregado por varianza inversa de **+5,14 puntos** (**+4,34 a +5,95**). Aun así, la caracterización previa de los niños, niñas y adolescentes (NNA) revela que casi la mitad de los alumnos expuestos ya venía rotando de colegio antes del cierre (**47,04 %** frente a **30,52 %** en los controles), por lo que la brecha mide una diferencia ajustada antes-después en presencia de fragilidad preexistente, no un experimento aleatorio.

---

## 2. Movimiento 1 — ¿Qué cerró realmente? De la salida administrativa a la regla RCID v1

En la ventana reciente (2016–2025) existen **346 episodios** donde un establecimiento con matrícula dejó de operar. Al depurar anexos, cambios administrativos y continuidades probables, la parte II de la serie identificó **330 cierres estrictos** de oferta educativa. El diagnóstico longitudinal clasifica esos 346 episodios en cuatro estados mutuamente excluyentes:
- **266 episodios sin señal contradictoria:** la trayectoria estudiantil no contradice el cierre estricto.
- **15 continuidades candidatas:** cambios de nombre, nivel o actividad posterior que ameritan revisión documental.
- **35 alertas no resueltas:** se mantiene la categoría mientras no exista fuente institucional independiente.
- **30 episodios con seguimiento incompleto:** son cierres de 2025 cuyo año posterior (2026) aún está censurado a la derecha.

De manera transversal existen **45 alertas por destino concentrado** y **cero confirmaciones institucionales independientes** en esta fase.

Para estudiar veinte años de paneles masivos sin expediente físico por escuela, el artículo define la **Regla de Cierre Escolar Inferido desde los Datos (`RCID v1`)**, estructurada en tres niveles anidados (D0 ⊃ D1 ⊃ D2):
- **D0 (salida administrativa bruta):** matrícula positiva en t−1, caída a cero en t y sin actividad docente posterior (**1.635** en 2005–2015; **346** en 2016–2025; **1.981** en total).
- **D1 (cierre estricto de oferta educativa):** depura reaperturas posteriores y cambios de código RBD con continuidad de local (**1.477** en 2005–2015; **330** en 2016–2025; **1.807** en total).
- **D2 = RCID v1 (cierre inferido depurado por flujo estudiantil):** exige al menos 5 estudiantes seguibles en t−1 y descarta las absorciones concentradas o fusiones de facto donde un único establecimiento receptor concentra al menos el **70 %** de los trasladados y al menos **15 alumnos** en t (**1.382** en 2005–2015; **296** en 2016–2025; **1.678** en total, o **1.648** en la variante limpia con t+1 observado al excluir los 30 episodios de 2025).

En simple: no es equivalente que un curso entero se mude junto a otro edificio a que cada familia deba buscar matrícula por separado. En la ventana 2016–2019, de **64 episodios** históricos antes del filtro de soporte, **63** conservan al menos un estrato comparable (**6.190** observaciones estudiante-cohorte expuestas de **6.581** iniciales, frente a un universo de soporte de **82.753** observaciones de control).

---

## 3. Movimiento 2 — ¿Qué ocurrió después del cierre? Resultados 2016–2019, radiografía NNA y serie larga 2005–2024

### 3.1. Dos resultados primarios y dos exploratorios en 2016–2019
Sobre los **62 episodios** con seguimiento observable para los resultados primarios:
1. **No matrícula persistente por dos años:** el artículo evita llamarla «deserción» porque la ausencia del registro administrativo no informa el motivo ni si el estudiante salió del país o pasó a otra modalidad no capturada. La diferencia antes-después es de **+0,63 puntos porcentuales** (intervalo conservador del 95 %: **−0,77 a 2,03 puntos**, sobre **3.666** observaciones expuestas y **49.944** controles).
2. **Falla de progresión o rezago (sin matrícula o bajo el curso esperado al año siguiente):** la diferencia antes-después es de **+5,29 puntos porcentuales** (intervalo conservador: **2,08 a 8,51 puntos**, sobre **4.815** observaciones expuestas y **65.538** controles), pero sus cotas por datos faltantes van de **−1,15 a 10,98 puntos porcentuales**.
3. **Asistencia y promedio de notas (exploratorios y condicionados):** solo pueden medirse entre quienes tienen acta válida en ambos períodos (**3.871** observaciones expuestas en **58 episodios**, que cubren apenas el **62,5 %** del soporte expuesto frente al **76,8 %** de los controles). La diferencia es de **−1,15 puntos** en asistencia (**−2,40 a 0,10**) y **−0,06** en promedio de notas (**−0,14 a 0,01**).

Si se incluyen las escuelas receptoras dentro del grupo de comparación (en una muestra distinta), la no matrícula se estima en **+0,71 puntos** (**−0,69 a 2,12**) y la falla de progresión en **+5,09 puntos** (**1,94 a 8,23**), sin eliminar las cotas de **−1,15 a 10,98 puntos**.

### 3.2. La analogía de la sala de reuniones: episodios efectivos
Aunque hay 62 escuelas cerradas en la estimación principal, unas pocas concentran una fracción desproporcionada de los alumnos. Escuchar esos 62 cierres se parece menos a escuchar 62 voces independientes al mismo volumen y más a escuchar unas **21,1 voces o episodios efectivos** en no matrícula, **21,9** en progresión y apenas **17,7** en asistencia y notas.

### 3.3. ¿Estamos comparando peras con peras? Balance basal y radiografía NNA en G−1
El método de diferencias en diferencias empareja exactamente un año antes del cierre (G−1) por año, sexo, región, dependencia, ruralidad, nivel educativo y curso inicial.
- En el balance tradicional, la edad promedio es idéntica (**11,70 años** en ambos grupos; se observa en el 100 % de la muestra), y entre quienes tienen acta previa la asistencia (**90,93 %** frente a **91,68 %**) y las notas (**5,62** frente a **5,67**) son muy similares. Pero la disponibilidad de acta válida en G−1 presenta una brecha severa: **76,8 %** en expuestos frente a **96,2 %** en controles (**−19,4 puntos porcentuales**). Por eso la tabla no certifica aleatorización ni comparabilidad sociodemográfica completa.
- Al incorporar descriptores adicionales de NNA entre G−3 y G−1 (sobre 6.190 expuestos y 82.753 controles), aparece una dualidad reveladora:
  - La vulnerabilidad socioeconómica individual elegible para la Subvención Escolar Preferencial (SEP) está equilibrada: **30,68 %** de estudiantes prioritarios en expuestos frente a **32,32 %** en controles (brecha de **−1,64 puntos**), y **54,51 %** frente a **55,58 %** en elegibilidad SEP total (**−1,07 puntos**), con idéntica sobreedad (**33,86 %**).
  - En cambio, los expuestos asistían a colegios con menor cobertura efectiva de beneficiarios SEP (**37,63 %** frente a **48,58 %**, brecha de **−10,95 puntos**), menor convenio SEP del establecimiento (**45,17 %** frente a **55,23 %**, **−10,06 puntos**), mucha menor Jornada Escolar Completa (**53,97 %** frente a **72,51 %**, **−18,54 puntos**), mayor conmutación entre comunas (**38,59 %** frente a **29,99 %**, **+8,60 puntos**) y mucha mayor rotación escolar previa: el **47,04 %** de los alumnos expuestos ya había cambiado de escuela al menos una vez entre G−3 y G−1, frente al **30,52 %** de los controles (**+16,52 puntos**).

### 3.4. ¿Por qué 2016–2019 y qué muestra la serie completa 2005–2024?
La ventana 2016–2019 se eligió como corte principal por cuatro razones técnicas: el estado oficial de cierre (`ESTADO_ESTAB`) entró al directorio en 2015; exigir historia previa larga dentro de un panel que parte en 2004 empuja hacia mediados de los años 2010; 2020–2022 estuvo alterado por la pandemia de COVID-19 y la promoción flexible; y 2024–2025 está censurado para medir dos años posteriores.

Al estimar las **20 cohortes anuales entre 2005 y 2024** por separado frente a controles aún no tratados bajo `RCID v1` (**1.141 episodios con soporte**, **78.972 expuestos** y **734.472 controles**):
- **Atenuación progresiva por régimen institucional en falla de progresión:**
  1. **2005–2010 (régimen LOCE e inicio SEP, 521 episodios):** **+12,15 puntos porcentuales** (IC 95 %: **+3,78 a +20,52**); no matrícula de 2 años: **+1,21 puntos** (**+0,53 a +1,90**).
  2. **2011–2015 (puesta en marcha LGE y SAC, 502 episodios):** **+7,82 puntos** (**+6,20 a +9,41**); no matrícula de 2 años: **+1,85 puntos** (**+1,10 a +2,59**).
  3. **2016–2019 (ventana principal e inicio Ley de Inclusión, 63 episodios):** **+5,29 puntos** (**+2,08 a +8,51**, con cotas por datos faltantes de **−1,15 a 10,98 puntos**); no matrícula de 2 años: **+0,63 puntos** (**−0,77 a +2,03**).
  4. **2020–2022 (pandemia COVID-19, 33 episodios):** **+2,70 puntos** (**−0,63 a +6,03**); no matrícula de 2 años: **−0,28 puntos** (**−1,37 a +0,81**).
  5. **2023–2024 (post-pandemia, 22 episodios):** **+2,59 puntos** (**−1,55 a +6,73**); no matrícula de 2 años: **−0,93 puntos** (**−2,64 a +0,78**, con 2024 censurado en el horizonte de dos años).
- **Rango anual y agregados de toda la serie:** las **19 cohortes estimables de progresión (2006–2024)** son todas positivas, variando entre **+0,94 puntos** (en 2021) y **+28,22 puntos** (en 2010), con mediana de **+7,18 puntos** y rango intercuartílico de **+3,15 a +9,62 puntos**. El agregado ponderado por expuestos de Callaway y Sant'Anna es **+9,11 puntos porcentuales** (**+5,34 a +12,88**), con cotas de Manski de **+0,43 a +16,21 puntos** (y **+1,38 puntos** en no matrícula de dos años); con pesos iguales por cohorte anual es **+7,55 puntos** (**+5,52 a +9,57**); y por varianza inversa (I² = 76,48 %) es **+5,14 puntos** (**+4,34 a +5,95**).

### 3.5. Por qué no se usa una variable instrumental (SLEP o SAE) y cápsula histórica
Los Servicios Locales de Educación Pública (SLEP), el Sistema de Admisión Escolar (SAE) o las caídas demográficas comunales no cumplen la restricción de exclusión de una variable instrumental: afectan directamente recursos, vacantes y trayectorias estudiantiles, no solo la probabilidad de cierre. Por eso no se ejecuta una regresión instrumental en esta versión.

Respecto del antecedente chileno [*Destructive Creation* (Documento de Trabajo 396, 2014)](https://3cucharadas.cl/assets/docs/doc_trabajo_destruccion_labra_mizala_hojman_grau.pdf), del que el autor fue coautor, sus tablas reportaron efectos marginales probit de **+1,46 puntos porcentuales** (sobre **682.217** estudiantes en la tabla 7), **+1,74 puntos** (**2.361** estudiantes en la tabla 8) y **+1,08 puntos** (**906.629** estudiantes en la tabla 14) en ausencia del registro por dos años. Las tablas causales 5, 6, 7, 8 y 14 siguen **no comparables** porque no se recuperaron el script ni el insumo analítico exacto y la ecuación discrepa de las notas sobre los efectos fijos; las cifras describen lo publicado sin confirmar ni corregir su ejecución.

La pregunta sobre ingreso oportuno a la **educación superior** queda diferida para una entrega posterior que cuente con microdatos individuales acreditados del SIES y enlace validado con DEMRE; no se estiman ni sugieren efectos postsecundarios en esta parte.

---

## 4. Movimiento 3 — ¿Cómo se protege una transición escolar? Resguardos prudenciales

Que la ventana reciente sea causalmente inconclusa no justifica pasividad: invierte la carga de la prueba hacia la autoridad educativa y el sostenedor antes, durante y después del cierre:
- **Antes de decidir:** distinguir si se trata de un establecimiento, sede, fusión o cambio de código RBD; registrar la fecha de anuncio y participación de la comunidad; y verificar capacidad, convenio SEP, Jornada Escolar Completa y calidad previa de los colegios receptores.
- **Durante la transición:** asignar vacantes reales y apoyos nominales a cada estudiante; medir tiempos de viaje, transporte seguro y continuidad de compañeros de curso; y financiar la mayor carga de las escuelas receptoras.
- **Después del cambio:** seguir nominalmente matrícula, asistencia, progresión, notas y bienestar por al menos dos años, observando tanto a los estudiantes desplazados como a quienes ya asistían a las escuelas receptoras, y publicar alertas con plazos de corrección.

Estos **resguardos prudenciales** no son efectos estimados de esas decisiones: son el estándar mínimo de responsabilidad pública para no confundir cercanía en el mapa con continuidad educativa real.
