# QA — Cápsula de audio NotebookLM (`costos-cierre-escolar-trayectorias`)

- **Estado actual:** **Paquete local sincronizado con el post canónico reestructurado (ventana macro 2005–2024 primero y zoom anidado 2016–2019 con mejoras econométricas M1–M3)** y episodio publicado en Spotify y Apple Podcasts (`etapa: publicado`).
- **Fecha de actualización:** 7 de noviembre de 2026 (revisión editorial adversarial; `01-fuente.md` y `personalizacion.txt` resincronizados; `guion.md`, `guion-breve.md` y `origen.yaml` intactos por ser el insumo y la procedencia del audio ya publicado)

---

## 1. Registro de evidencia del guion y de la fuente editorial

| ID | Afirmación en `01-fuente.md` y `guion.md` | Respaldo en el post canónico (`costos-cierre-escolar-trayectorias`) | Sección / Localizador | Naturaleza |
|---|---|---|---|---|
| `EV-01` | Base longitudinal 2004–2025 con 79.709.054 registros de matrícula y 73.873.835 de rendimiento | «79.709.054 registros de matrícula y 73.873.835 de rendimiento entre 2004 y 2025» | Apertura | Resultado descriptivo |
| `EV-02` | Serie completa 2005–2024 bajo `RCID v1` (20 cohortes, 1.141 episodios con soporte, 78.972 expuestos y 734.472 controles): 19 cohortes positivas en progresión (+0,94 a +28,22 pp, mediana +7,18 pp); Callaway y Sant'Anna +9,11 pp ([+5,34; +12,88], cotas de Manski [+0,43; +16,21] pp) y +1,38 pp en no matrícula; pesos iguales +7,55 pp ([+5,52; +9,57]); efectos aleatorios (I² = 76,5 %, τ = 2,81 pp) +6,29 pp ([+4,49; +8,09], predicción [+0,09; +12,49]) y +0,79 pp en no matrícula | Apertura, Cucharada 2 §1, Tabla 4 y Figura 2 | Apertura / Cucharada 2 | Resultado longitudinal principal |
| `EV-03` | Atenuación por etapas institucionales: 2005–2010 (521 cierres, 36.984 expuestos, +12,15 pp, cotas [+3,49; +18,83]) y 2011–2015 (502 cierres, 31.512 expuestos, +7,82 pp, no matrícula +1,85 pp) concentran el 89,7 % de los cierres (1.023) y el 86,7 % de los expuestos (68.496), bajando a +5,29 pp en 2016–2019 (63 cierres, 6.190 expuestos, cotas [−1,15; +10,98]), +2,70 pp en 2020–2022 (33 cierres, 3.272 expuestos) y +2,59 pp en 2023–2024 (22 cierres, 1.014 expuestos) | Apertura y Cucharada 2, Tabla 4 | Apertura / Cucharada 2 | Resultado por régimen |
| `EV-04` | Regla `RCID v1` (D0 ⊃ D1 ⊃ D2): 1.981 salidas brutas (D0), 1.807 cierres estrictos (D1), 1.678 `RCID v1` conservador y 1.648 `RCID v1` limpio con t+1 observado (1.382 en 2005–2015 y 266 en 2016–2024; depura traslados concentrados con ≥ 10 estudiantes, ≥ 70 % a un destino y HHI ≥ 0,50); 1.177 regulares y 1.141 con soporte | Cucharada 1, Tabla 1 | Cucharada 1 | Definición y resultado |
| `EV-05` | Diagnóstico de 346 episodios recientes (330 cierres estrictos): 266 sin señal contradictoria, 15 continuidades candidatas, 35 alertas no resueltas, 30 con seguimiento incompleto (2025); 45 alertas de flujo, 0 confirmaciones institucionales, y catastro en Transparencia Activa (12.509 resoluciones administrativas y 4.735 sancionatorias; 22 y 21 únicas en 2018–2025) | Cucharada 1, Tabla 2 y Notas metodológicas | Cucharada 1 / Apéndice | Resultado diagnóstico |
| `EV-06` | Radiografía NNA en G−1 (6.190 expuestos y 82.753 controles): edad 11,70 años (100 % observada), sobreedad 33,86 %, prioritarios SEP 30,68 % vs 32,32 % (−1,64 pp), elegibilidad SEP 54,51 % vs 55,58 % (−1,07 pp), pero menor convenio SEP (−10,06 pp), menor JEC (−18,54 pp), brecha de acta válida −19,4 pp (76,8 % vs 96,2 %) y mayor rotación previa entre G−3 y G−1 (47,04 % vs 30,52 %, +16,52 pp) | Cucharada 1, Tabla 3 y Apéndice Tabla 7 | Cucharada 1 / Apéndice | Resultado e interpretación |
| `EV-07` | Subventana anidada 2016–2019 (5,5 % de los cierres y 7,8 % de los expuestos; 62 episodios primarios; 21,1, 21,9 y 17,7 episodios efectivos): no matrícula +0,63 pp ([−0,77; 2,03], 3.666 expuestos y 49.944 controles); falla de progresión +5,29 pp ([2,08; 8,51], 4.815 expuestos y 65.538 controles) con cotas de Manski [−1,15; 10,98] pp (inconcluso); asistencia −1,15 ([−2,40; 0,10]) y notas −0,06 ([−0,14; 0,01]) sobre 58 episodios y 3.871 expuestos (62,5 % vs 76,8 %) | Cucharada 2, Tabla 5 y Figura 3 | Cucharada 2 | Resultado primario y exploratorio |
| `EV-08` | Mejoras econométricas M1–M3 en 2016–2019: (M1) placebos +0,16, +0,30 y +0,40 pp (tope 0,81 pp; umbral 2,07 pp = 2,54 veces el tope previo) y estables desde G−2 (+3,87 pp en 3.556 estables vs +9,58 pp en 1.033 entrantes tardíos); (M2) cierres con ≥ 90 % de actas bajo el DS n.º 315 (1.822 expuestos, +4,26 pp y cotas [+0,09; +7,84] pp que excluyen cero); (M3) escuela receptora con mayor aprobación previa en G−1 (+2,03 pp en 2.099 alumnos vs +5,38 pp en 2.263, diferencia descriptiva −3,35 pp) | Cucharada 2 y Apéndice metodológico | Cucharada 2 / Apéndice | Verificaciones econométricas M1–M3 |
| `EV-09` | Rechazo de variables instrumentales (SLEP, SAE, demografía comunal) por violar la restricción de exclusión; agenda de educación superior diferida a la parte IV (SIES y DEMRE); y resguardos prudenciales antes, durante y después de la transición | Cucharada 2, Cucharada 3, Tabla 6 y Cierre | Cucharada 2 / Cucharada 3 | Límite de identificación y recomendación prudencial |

---

## 2. Verificación documental del paquete

- [x] `01-fuente.md` está limpia de front matter, Liquid y HTML accesorio, abre con la ventana macro `2005–2024` y sus cinco etapas institucionales, e integra el zoom `2016–2019` con las tres verificaciones econométricas (M1: Rambachan y Roth simplificado y estables desde G−2; M2: cotas de Manski por entrega de actas; M3: calidad previa de la receptora), presentadas con su nombre descriptivo y no solo con la etiqueta.
- [x] Cada mención de `+5,29` va acompañada de sus cotas de datos faltantes (`−1,15 a 10,98 puntos porcentuales`) y de la calificación de resultado inconcluso en la subventana reciente.
- [x] `personalizacion.txt` mide cuatrocientos ochenta caracteres (`wc -m`, tope de cuatrocientos noventa), en español de Chile sin anglicismos, con el orden macro → etapas → zoom `2016–2019` (M1–M3) → resguardos, y con las cinco etapas correctamente delimitadas (2020–2022 y 2023–2024 por separado).
- [x] `guion.md` y `guion-breve.md` atribuyen los hallazgos al artículo, sin dígitos en los diálogos hablados (`rg '^\*\*[AB]:\*\*.*[0-9]'` no devuelve líneas) ni identificadores individuales (`MRUN`) o códigos `RBD` específicos.
- [x] `origen.yaml` conserva intactos los enlaces publicados en Spotify y Apple Podcasts.
- [x] Coherencia numérica: `ruby scripts/verify_difusion_coherente.rb costos-cierre-escolar-trayectorias` sale 0 (corrido vía Codex en sandbox de solo lectura el 7 de noviembre de 2026). Ese gate no desciende a `podcast/` (su glob recorre solo la raíz del paquete y `difusion/linkedin/`), así que se corrió además una réplica en Python de su extracción numérica sobre los siete `.md`/`.txt` de `podcast/`: cero cifras huérfanas en cada archivo.

---

## 3. Divergencias entre el audio publicado y el post actualizado (registradas, no corregidas)

El episodio se generó el 1 de noviembre de 2026 a partir de `guion-breve.md`, antes de la reestructuración del post del 6 de noviembre. Los guiones no se tocan porque son el insumo del audio emitido; lo que diverge se deja escrito aquí para que nadie lo tome por fidelidad.

| Lo que dice el audio (`guion-breve.md`) | Lo que dice hoy el post | Lectura |
|---|---|---|
| «Dos análisis que el artículo deja pendientes: ... Rambachan y Roth, y fijar la exposición dos años antes del cierre» | Ambos están resueltos (M1): umbral de 2,54 veces el tope previo de 0,81 pp y +3,87 pp en estables desde G−2 frente a +9,58 pp en entrantes tardíos | El audio quedó desactualizado en este punto; `01-fuente.md` ya incorpora M1 |
| «la brecha solo llega a cero si los datos faltantes se acercan en más de un noventa por ciento al escenario más benigno» | Esa frase ya no está en el post; la condición vigente es que las cotas excluyen el cero solo en cierres con al menos 90 % de actas válidas en G−1 (38 % de los expuestos) | Afirmación huérfana en la versión actual del post |
| «la que el autor incorporó en su actualización del treinta y uno de octubre» | El post ya no lleva esa nota de actualización fechada | Referencia histórica, sin respaldo literal hoy |
| Cierre sobre «dónde van a ocurrir los próximos cierres» y transición demográfica | El post no trae proyecciones; el guion ya lo advertía y no inventa cifras | Énfasis editorial del autor, no hallazgo del post |

Si se regenera el episodio, cargar `01-fuente.md` actualizada y pegar `personalizacion.txt`; el `guion-breve.md` publicado no debe reutilizarse sin incorporar M1–M3.
