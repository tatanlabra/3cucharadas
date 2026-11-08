**REVIEW_VERDICT: REQUEST_CHANGES.** Las 17 comprobaciones de r2 quedan en 14 resueltas y 3 sin resolver, todas del lado ES. No encontré regresiones nuevas de cifras o de límites. Plan mode estaba activo, así que no edité ninguna fuente. El veredicto va en esta respuesta.

## Matriz de cierre r2

Contra la lista r2 son 6 bloqueos, 6 medios y 5 bajos: 17 en total.

| ID | Hallazgo r2 | Estado | Evidencia actual |
|---|---|---|---|
| B1 | «+9,11 en Callaway–Sant'Anna» | **Resuelto** | ES anexo III `:161` «+9,11 puntos ponderados por expuestos». `:96` y EN `:99,:166` no atribuyen estimador. `rg` solo devuelve citas bibliográficas. |
| B2 | «antes de mirar la serie completa» (ES post) | **Resuelto** | ES post III `:101` «después de observar un piloto… antes de ejecutar la reestimación v3… no fue un prerregistro independiente». EN post `:92`. |
| B3 | Seis puntos con redacciones distintas | **Resuelto** | ES anexo `:126,:221`, EN anexo `:130,:228` y EN post `:92,:103` coinciden. 0 coincidencias de «before examining» y «antes de mirar». YAML `:2` dice `specified_after_pilot_before_full_v3_execution`. |
| B4 | Universo de controles / estimador | **Resuelto** | ES post `:86`, ES anexo `:96`, EN post `:76`, EN anexo `:99`. Script `compute_full_series_2004_2025.py:432-433` excluye con `NOT EXISTS ever_treated_students` y `NOT EXISTS all_closure_schools`. |
| B5 | IV D1−D2 como validación | **Resuelto** | ES post `:105`, ES anexo `:148`, EN post `:106`, EN anexo `:152`. Los cuatro dicen «compatible con», no «valida», sin dirección ni tamaño del sesgo. |
| B6 | Aserción legal sin ancla | **Resuelto** | EN post `:130` la atribuye a la nota Castro Paredes; ya no enlaza al anexo. ES post `:136` solo dice «contexto administrativo». Abrí el PDF: lo respaldan `pdftotext` líneas 86–99 y 184–191. Ver F6. |
| M1 | Título A1 EN «simplified version of HonestDiD» | **Resuelto** | EN anexo IV `:37` «simplified linear version inspired by Rambachan and Roth». |
| M2 | ES `:66` sin cláusula de intercambiabilidad | **Resuelto** | ES anexo IV `:66` «no garantiza comparabilidad en características no observadas». |
| M3 | EN «robust descriptive fact» | **Resuelto** | EN anexo III `:126` «descriptive, not the isolated effect of a single statute». |
| M4 | ES sin frase de no observables | **Resuelto** | ES anexo III `:151`. |
| M5 | Banda de recorte [+3,79; +6,80] sin origen | **Sin resolver en ES** | EN anexo IV `:51` cita la ruta completa y dice que no se muestra en el artículo ni en el anexo III. ES anexo IV `:50` no. Ver F2. |
| M6 | Denominador ES III | **Resuelto** | ES post III `:75` «no necesariamente personas distintas». |
| L1 | Alt de `longitudinal-regimes` | **Sin resolver en ES** | EN `:123` incluye punto estimado, p = 0,28 y 12 conglomerados. ES `:119` no. Ver F1. |
| L2 | «dos películas» y «sala de reuniones» | **Resuelto** | 0 coincidencias en los 8 archivos. |
| L3 | Comentario `scientific-state` G1 | **Resuelto** | EN `:56` explícito. ES `:56` dice «depende de la especificación y no identifica daño confirmado». Ver F4. |
| L4 | Cláusula de prioridad, A4 y «significativa» | **Resuelto** | ES post IV `:134`, EN `:138`. A4 con p nominal en ES `:185,:196` y EN `:191,:200`. |
| L5 | `last_modified_at` EN anterior a ES | **Resuelto** | EN ≥ ES en los cuatro pares: III post 23:40 vs 20:30, III anexo 23:40 vs 21:00, IV post y anexo 23:40 en ambos idiomas. |

## Hallazgos pendientes

- **[MED] F1 · `_pages/tesis-post4-anexo-metodologico.md:119`** → el alt dice «−2,64… concentrado en IP/CFT con −2,59» sin p = 0,28, sin 12 conglomerados y sin «estimación puntual, no efecto demostrado». EN `:123` sí los trae. Fix: copiar el alt EN. En `:119` y `:147` también corregir «el estimación» → «la estimación».
- **[MED] F2 · `_pages/tesis-post4-anexo-metodologico.md:50`** → cita `full_63_episodes.lee_monotonic_bounds_pp` sin `post_iii_upgrades → m2_stratified_manski_and_lee_bounds`, y no dice que es una salida técnica ausente del artículo y del anexo III. Fix: copiar la cláusula de EN `:51`. Verifiqué con `jq` que la ruta existe y vale `[3.79,6.8]`, así que las cifras no cambian.
- **[BAJO] F3 · `_pages/tesis-post4-anexo-metodologico.md:47`** → «bajo el criterio de Rambachan y Roth» sobreatribuye el criterio formal. EN `:48` dice «separate criterion… not a full HonestDiD analysis». Fix: «bajo esta versión lineal simplificada inspirada en…, que no es un análisis HonestDiD completo».
- **[BAJO] F4 · `_posts/2026-11-04-…causal-ml.md:56`** → no dice «reordenado» ni «grupo fijo». EN `:56` sí. Fix: alinear con EN.
- **[BAJO] F5 · EN `_posts/…trayectorias-en.md:76` y `_pages/tesis-post3-anexo-metodologico-en.md:99`** → omiten «excluí a estudiantes expuestos alguna vez», que sí está en ES `:86` y `:96` y en el script `:432`. EN anexo `:40` tampoco trae «no necesariamente personas distintas», que sí está en ES anexo `:39` y EN post `:64`.
- **[BAJO] F6 · EN `_posts/…trayectorias-en.md:130` vs ES `:136`** → el PDF respalda el hecho, pero lo atribuye a consultas con la SEREMI RM y dice que «no está contenida en ningún texto legal». EN lo presenta como «legal commentary reports». Fix: «reports, citing consultations with the Metropolitan Region secretariat, that…». ES queda más débil que EN, aceptable pero asimétrico.

## Hechos, inferencia y alcance

- **HECHO:** las cifras núcleo coinciden en ES y EN. En III: +5,29 con cotas [−1,15; +10,98], +9,11 como agregado aparte y −3,35 sin intervalo propio. En IV: −14,64 vs −13,24, 82,0 % solo de la brecha cruda de celda, 57,5 % de la secuencia del modelo, −0,29 [−2,64; +2,06], −2,09 vs −2,59 (p = 0,28), G1 −12,26 vs −0,26 como quintiles recalculados, y sustitución vs exclusión neta no identificada.
- **INFERENCIA (deductiva):** F1 y F2 son diferencias de paridad entre idiomas, no errores numéricos.
- **Límite:** no evalué si el SVG de `longitudinal-regimes` repite «concentrado» en su `<desc>`. Revisen ese archivo al corregir F1.
- **No inspeccionado:** SVG/PNG, CSV, JSON salvo la ruta de recorte, generadores, CSS, gates, PDF de salida, front matter salvo `last_modified_at`. No recomputé cifras desde datos.
- **SHA y ediciones:** 8/8 SHA-256 idénticos a `inputs-before.json`, antes y después. No edité fuentes. Dejé una copia temporal del PDF de la BCN en `/tmp/castro-r3.*` y hashes en `/tmp/r3-*.txt`.

PLAN_STATE v2: tablero `pb-20261108T003705315Z-fc127547`, D11 revisión r3 = `REQUEST_CHANGES` (14 de 17 resueltos; 2 medios y 1 bajo de r2 sin resolver en ES, más 3 bajos de paridad nuevos). Siguiente paso: Codex corrige F1 y F2, y opcionalmente F3–F6. Después viene una verificación acotada con `rg` de esas líneas. No se publica ni se hace push.

HANDOFF-TRACE: Claude Code (`claude-bridge`, `sonnet` solicitado) → Codex integrador, revisión dirigida r3 de solo lectura. Sin ediciones, sin publicación, sin otros agentes.

MODEL-REPORT: Sonnet 5.5 (`claude-sonnet-5-5`), sin subagentes. Lectura completa de las 8 fuentes y de la lista r2. Verificado con `sha256sum` 8/8 antes y después, `rg`, `jq` sobre el JSON, lectura de `confirmatory_design_v3.yaml` y del script, y `pdftotext` sobre el PDF de Castro Paredes.
