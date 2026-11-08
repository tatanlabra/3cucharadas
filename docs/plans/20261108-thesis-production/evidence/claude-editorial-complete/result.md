REVIEW_VERDICT: REQUEST_CHANGES

Los cuerpos de los posts III y IV cumplen el criterio. Los bloqueos están en el anexo IV EN, que no se sincronizó con el ES reescrito, en el post III EN y en el anexo III ES. No edité las fuentes. Escribí el informe completo en el único archivo permitido en modo plan, `/home/ende/.claude/plans/revisi-n-editorial-completa-crispy-quilt.md`.

**Inventario:** leí las 8 rutas completas. Los sha256 actuales coinciden 8/8 con `inputs-before.json`.

## Bloqueos
- **[B1] `_pages/tesis-post4-anexo-metodologico-en.md:26`:** dice que los dos controles de la parte III (tendencias previas y anclaje en G−2) «remained pending». ES:25 y el anexo III (ES:141, ES:219) ya los reportan. Corrección: alinear a ES:25.
- **[B2] EN IV anexo :253:** lee +1,21 como «absence of detectable harm». Contradice ES:245 («inconclusa, no ausencia demostrada») y el post EN:101 («neither proves equality»). Corrección: alinear a ES:245.
- **[B3] EN IV anexo :85-88:** presenta «two independent identification strategies… the other holds up». ES:81 dice que su concordancia no garantiza identificación y que pueden compartir sesgos. Corrección: alinear a ES:81 y quitar «belt and suspenders».
- **[B4] EN IV anexo :101:** afirma en negrita «57.5% … was prior student trajectory». ES:96 dice «no es una fracción causal aislada». Corrección: alinear a ES:96.
- **[B5] EN IV anexo :148, :152, :179, :196:** usa «smoking-gun», «were predominantly administrative reorganizations», «severely biasing any causal inference» y «striking». El ES equivalente (ES:142, ES:146, ES:171, ES:189) dice «compatible con… pendiente de confirmación documental». Corrección: alinear al ES.
- **[B6] Etiquetas ELI5, contrarias a la decisión de prosa adulta.** Están en EN IV anexo :29, :31, :67, :85, :88, :157 («in plain language», «Two cars», «identical twin», «oven-and-freezer paradox») y en EN III anexo :26 y :156 («Put simply»). El ES IV ya está sobrio. Corrección: reescribirlas como el ES.
- **[B7] `_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md:128`:** párrafo huérfano «Table 6 shifts the burden…». No existe Tabla 6, duplica el contenido de :132 y ES:136 ya lo condensó. Corrección: borrar :128.
- **[B8] `_pages/tesis-post3-anexo-metodologico.md:92-96`:** el ES salta de «Serie, sensibilidad y receptoras» directo a la Tabla A4. Faltan la sección EN:97-99 (método escalonado, cohortes 20/19/17 y citas Callaway/Sun/Roth) y los cuatro puntos EN:121-126. Esos puntos incluyen que la atenuación entre regímenes no es el efecto de una ley y que la promoción flexible reduce el rezago de forma mecánica. Corrección: trasladarlos al ES.

## Observaciones opcionales
- **«Pre-registrado»:** aparece en la figura 2 del post III (:111) y en ambos anexos III, pero el cuerpo dice «fijado antes de mirar la serie completa» (:101). No hay sello verificable. Convendría suavizar o citar fecha o commit.
- **Banda de recorte:** el anexo IV (ES:49, EN:51) cita «[+3,79; +6,80]» como de la parte III. El anexo III solo trae el 1,51 % y λ*.
- **Brechas mezcladas:** el anexo IV (ES:73-75, EN:77-79) llama «trece o catorce puntos» a −13,24 y −14,64. Son muestras distintas, y el post IV:66 pide no combinarlas.
- **«Series-wide peak +1.85»:** en EN III anexo :124 es incorrecto, porque el rango anual llega a +4,56. Es el máximo entre regímenes.
- **Recorte de 1,51 %:** en anexo III ES:220 y EN:239, con los insumos redondeados da 1,50 %.
- **Duplicado:** en ES IV anexo :200, «al combinar: combina».
- **Anclas:** `tabla-post4-a1`, `a3`, `a4` y `a6` existen en EN y no en ES.
- **Fechas:** `last_modified_at` de EN III y IV (11-06) es más antiguo que el ES (11-07), señal de EN sin sincronizar.
- **Paridad menor en IV:** el aside EN:47 trae el IC de IP/CFT y el ES no. EN:113 y EN:137 no tienen par ES. EN:129 no recapitula la serie.
- **Audio en EN III:** el post EN no tiene bloque `audio` ni `ai_disclosure.audio`. Confirmar que es intencional.

## Verificado
- **Invariantes del encargo:** los cuatro posts cumplen los de III y los de IV. Incluyen el CI 2016–2019 [−7,54; +2,25] (ES:62, EN:63). Permalinks y `ref` son idénticos entre ES y EN.
- **Aritmética interna:** correcta (tablas A1–A4, DiD = brecha menos brecha G−5, 82,0 %, 57,5 %, 89,7 % y 86,7 %, ≈255 estudiantes).
- **Cotejo con datos:** el JSON de IV contiene 0,6583; 0,0177; −2,73/+2,21; −12,26; −11,48; −2,57; −3,92; 1,75; 4,3; 6,16; 2,33; 0,0037; −2,09; −0,29; −0,91; 0,19; 1,98; −2,59; −3,79; −5,63; −13,24. El cotejo con los CSV fue parcial por redondeo y no es concluyente.

## Límites
- No revisé figuras, SVG, generadores ni gates, ni corrí build. `_site` es de las 19:00, anterior a las ediciones de 20:30–21:00.
- No recomputé ciencia y no cotejé los CSV de forma exhaustiva.
- No usé consenso entre agentes como evidencia.
- Ninguna de las dos aprobaciones (texto y figuras) está dada todavía. El texto queda en REQUEST_CHANGES y las figuras son de otra unidad.

PLAN_STATE v2: pb-20261108T003705315Z-fc127547 — texto REQUEST_CHANGES (B1–B8); figuras fuera de esta unidad.
HANDOFF-TRACE: Codex → Claude Code vía claude-bridge CLI, sonnet → veredicto devuelto al integrador (Codex).
MODEL-REPORT: claude-sonnet-5-5 (alias sonnet), solo lectura, 8/8 fuentes, sin delegar.
