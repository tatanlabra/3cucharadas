# QA — Cápsula de audio NotebookLM (`costos-cierre-escolar-trayectorias`)

- **Estado actual:** **Paquete local preparado y verificado contra el post canónico v3.2** (`etapa: preparado`). Pendiente la generación manual del audio en la interfaz de NotebookLM y la escucha humana antes de ensamblar cortinas o publicar en Spotify.
- **Fecha de preparación:** 2026-10-28

---

## 1. Registro de evidencia del guion y de la fuente editorial

| ID | Afirmación en `01-fuente.md` y `guion.md` | Respaldo en `_posts/2026-10-23-costos-cierre-escolar-trayectorias.md` | Sección / Localizador | Naturaleza |
|---|---|---|---|---|
| `EV-01` | Base longitudinal 2004–2025 con 79.709.054 registros de matrícula y 73.873.835 de rendimiento | «79.709.054 registros de matrícula y 73.873.835 de rendimiento entre 2004 y 2025» | Apertura, párrafo 3 | Resultado descriptivo |
| `EV-02` | Diagnóstico de 346 episodios recientes (330 cierres estrictos): 266 sin señal contradictoria, 15 continuidades candidatas, 35 alertas no resueltas, 30 con seguimiento incompleto (2025); 45 alertas de flujo y 0 confirmaciones institucionales | Tabla 1 y párrafo posterior | Cucharada 1, §1 | Resultado diagnóstico |
| `EV-03` | Regla `RCID v1` (D0 ⊃ D1 ⊃ D2): 1.981 salidas brutas (D0), 1.807 cierres estrictos (D1), 1.678 `RCID v1` conservador y 1.648 `RCID v1` limpio con t+1 observado (depura absorciones ≥ 70 % y ≥ 15 alumnos) | Tabla 2 y lista previa | Cucharada 1, §2 | Definición y resultado |
| `EV-04` | Soporte 2016–2019: de 64 episodios, 63 conservan soporte; 6.190 observaciones expuestas (de 6.581) y 82.753 controles | Figura 1 (`sample-flow`) | Cucharada 1, Figura 1 | Resultado descriptivo |
| `EV-05` | Resultados primarios 2016–2019 (62 episodios): no matrícula persistente 2 años = +0,63 pp ([−0,77; 2,03], 3.666 expuestos y 49.944 controles); falla de progresión o rezago = +5,29 pp ([2,08; 8,51], 4.815 expuestos y 65.538 controles), con cotas de Manski [−1,15; 10,98] pp que cruzan cero (inconcluso) | Apertura y Cucharada 2, §1, Tabla 3 y Figura 2 | Apertura / Cucharada 2 | Resultado primario y límite |
| `EV-06` | Resultados secundarios exploratorios y condicionados (58 episodios, 3.871 expuestos, cobertura 62,5 % vs 76,8 %): asistencia −1,15 puntos ([−2,40; 0,10]) y notas −0,06 ([−0,14; 0,01]) | Tabla 3 y párrafo posterior | Cucharada 2, §1 | Resultado exploratorio |
| `EV-07` | Episodios efectivos («sala de reuniones»): 62 episodios nominales equivalen a 21,1 efectivos en no matrícula, 21,9 en progresión y 17,7 en asistencia y notas | Párrafo sobre episodios efectivos | Cucharada 2, §1 | Límite estadístico |
| `EV-08` | Balance previo G−1 y radiografía NNA: edad 11,70 años (100 % observada), brecha de acta válida −19,4 pp (76,8 % vs 96,2 %); elegibilidad SEP equilibrada (30,68 % prioritarios, 54,51 % total), pero menor convenio SEP (−10,06 pp), menor JEC (−18,54 pp) y alta rotación previa G−3 a G−1 (47,04 % vs 30,52 %, +16,52 pp) | Tablas 4 y 5 y párrafos explicativos | Cucharada 2, §2 | Resultado e interpretación |
| `EV-09` | Serie completa 2005–2024 bajo `RCID v1` (20 cohortes, 1.141 episodios con soporte, 78.972 expuestos y 734.472 controles): atenuación por régimen desde +12,15 pp (2005–2010) y +7,82 pp (2011–2015) a +5,29 pp (2016–2019, cotas [−1,15; 10,98]), +2,70 pp (2020–2022) y +2,59 pp (2023–2024); 19 cohortes positivas en progresión (+0,94 a +28,22 pp, mediana +7,18 pp); agregado Callaway y Sant'Anna +9,11 pp ([+5,34; +12,88], cotas de Manski [+0,43; +16,21] pp) y varianza inversa +5,14 pp ([+4,34; +5,95]) | Tabla 6, Figura 3 y viñetas posteriores | Cucharada 2, §3 | Resultado longitudinal |
| `EV-10` | Rechazo de variables instrumentales (SLEP, SAE, caídas de matrícula) por violar la restricción de exclusión; no se ejecuta regresión instrumental en esta versión | Párrafo final de Cucharada 2, §3 | Cucharada 2, §3 | Límite de identificación |
| `EV-11` | Cápsula histórica (*Destructive Creation*, 2014): +1,46 pp (682.217), +1,74 pp (2.361) y +1,08 pp (906.629); tablas 5, 6, 7, 8 y 14 no comparables; y agenda de educación superior diferida (requiere SIES y DEMRE) | Cápsula histórica y bloque `higher-education-agenda` | Cucharada 2, §4–§5 | Límite histórico y de alcance |
| `EV-12` | Resguardos prudenciales antes, durante y después de una transición escolar (no son efectos estimados de esas decisiones) | Figura 4, Tabla 7 y Cierre | Cucharada 3 y Cierre | Recomendación prudencial |

---

## 2. Verificación documental del paquete (comprobado hoy)

- [x] `01-fuente.md` está limpia de front matter, Liquid y HTML accesorio, y conserva todas las cifras con sus denominadores, intervalos y cotas de datos faltantes.
- [x]Cada mención de `+5,29` va acompañada de sus cotas de datos faltantes (`−1,15 a 10,98 puntos porcentuales`) y de la calificación de resultado inconcluso en la ventana principal.
- [x] `personalizacion.txt` declara conversación de dos hablantes en español (A conductor `es-ES`, B experta `es-CL`), formato Deep Dive de longitud media, los tres movimientos y las exclusiones obligatorias, en 1.248 caracteres (bajo el límite de la interfaz de NotebookLM).
- [x] `guion.md` contiene aproximadamente 2.950 palabras pronunciables (dentro del presupuesto orientativo de 2.700–3.400 palabras para ~20 minutos), sin etiquetas de evidencia dentro del diálogo hablado, atribuyendo los hallazgos «al artículo» y nunca en primera persona.
- [x] No se incluyen identificadores individuales (`MRUN`), códigos `RBD` específicos ni rutas privadas.

---

## 3. Verificación de audio y escucha humana (pendiente tras generación manual en NotebookLM)

- [ ] Descargar el máster desde NotebookLM a `${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/renders/costos-cierre-escolar-trayectorias/capsula-es-master-estereo.m4a` y registrar `sha256` en `origen.yaml`.
- [ ] Medir duración con `ffprobe` (verificar contra la ventana `600–1800 s`) y sonoridad con `ffmpeg -af loudnorm`.
- [ ] Ensamblar con cortinas de inicio y cierre (`source-masters/podcast-cortinas/ensamblar.py`) a −16 LUFS.
- [ ] **Escucha humana obligatoria:**
  - [ ] Comprobar que las cifras pronunciadas coinciden con el post (`+5,29 pp` con cotas `−1,15 a 10,98 pp`, `+0,63 pp`, `1.648` cierres `RCID v1`, `+9,11 pp` y `+5,14 pp` en la serie 2005–2024, `47,04 %` de rotación previa).
  - [ ] Comprobar que el audio mantiene el carácter inconcluso de la ventana principal y no atribuye causalidad ni efectos en educación superior.
  - [ ] Verificar si NotebookLM respetó la distinción de acentos (`es-ES` en A y `es-CL` en B) o informar si salieron con el mismo acento.
  - [ ] Confirmar ausencia de cortes abruptos o lectura de instrucciones.
