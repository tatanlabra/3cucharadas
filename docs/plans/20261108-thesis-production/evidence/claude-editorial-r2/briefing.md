# Revisión editorial r2: ocho fuentes finales III–IV, ES/EN

Estado documental: LISTO. Origen Codex editor/integrador → Claude Code, CLI `claude-bridge`, modelo solicitado `sonnet`, 2026-11-08T02:22 UTC. Original del dictamen previo: `../claude-editorial-complete/result.md`; respuestas a B1–B7 y B8: `../figure-correction/editorial-r2-en.md` y `../figure-correction/editorial-r2-es3.md`. Snapshot congelado: `inputs-before.json` de este directorio.

PLAN_STATE v2: board `pb-20261108T003705315Z-fc127547`, rev16, D11 revisión editorial r2 activa. La revisión anterior fue `REQUEST_CHANGES` B1–B8; estas correcciones requieren juicio independiente antes del siguiente cierre. Otros ítems del plan, figuras/PDF y publicación, están fuera de tu unidad.

HANDOFF-TRACE: Codex → Claude Code vía `penta-agent/scripts/agent/claude-bridge` CLI, modelo solicitado `sonnet`, revisión de solo lectura.

## Unidad y límites duros

- Lee **completas las ocho fuentes** enumeradas en `inputs-before.json`: posts III/IV y sus anexos ES/EN. Revisa el texto final, no solo el diff. Incluye leyendas y textos alternativos dentro de Markdown; no inspecciones SVG, generadores, CSS ni gates.
- No edites archivos, no publiques, no actives otros agentes ni uses el consenso de revisores como evidencia. Confirma inventario 8/8 y, si calculas hashes, compáralos con el snapshot. Un recibo de transporte exitoso no equivale a aprobación editorial.
- Evalúa «el mismo hecho y el mismo límite» entre ES y EN: denominador, universo, especificación, intervalo, selección previa, datos faltantes y alcance causal deben viajar juntos. Distingue errores materiales de elecciones de estilo.
- Decisiones humanas: divulgación adulta, tres cucharadas por post, cuerpo principal conciso y anexo científico separado, cierre con recapitulación y tres desafíos, sin ELI5 ni promesas de daño o causalidad no identificados. No exijas estilo APA: Chicago/Deusto es guía editorial.

## Foco adversarial r2

| Punto anterior | Hecho/límite que debe sobrevivir |
|---|---|
| B1 | Las pruebas de tendencias y anclaje $$G-2$$ **ya estaban reportadas** en III; anexo IV solo las reúne. |
| B2 | DiD básica superior +1,21 pp es **inconcluso**; brazo $$G-5$$ puede contaminarse. No es ausencia probada de daño. |
| B3 | DiD de cohortes y DML tienen supuestos propios y pueden compartir sesgos; concordancia no garantiza identificación. |
| B4 | Reducción de 57,5 % al añadir historia individual es cambio entre modelos, **no fracción causal aislada**. |
| B5 | D1 \ D2 es prueba de composición: flujo ≥70 % compatible con continuidad administrativa, **sin confirmación documental** ni dirección/tamaño de sesgo causal establecido. G1 se define por orden del CATE predicho, no vulnerabilidad individual fija. |
| B6 | Anexos EN retiran analogías y etiquetas ELI5; método y límites permanecen. |
| B7 | No existe «Table 6» en post III EN; hecho de constancia de reubicación queda en prosa y notas legales. |
| B8 | Anexo III ES incorpora contraste por cohorte/agregación, 20 cohortes (19/17 estimables), cuatro lecturas y límites institucionales, antes omitidos. |

## Correcciones factuales adicionales

- `/home/ende/Descargas/programaciones/incubadora/tesis_mae_mejorada/research/post3/confirmatory_design_v3.yaml:1-29` registra `independent_preregistration: false` y piloto observado antes de especificar el corte 2016–2019. Los textos dicen «especificado después del piloto y antes de mirar la serie completa»; busca cualquier sello de prerregistro independiente aún positivo.
- `/home/ende/Descargas/programaciones/incubadora/tesis_mae_mejorada/research/post3/agy_full_series_v1/compute_full_series_2004_2025.py:432-433` excluye estudiantes expuestos alguna vez y escuelas con cierre registrado del universo de control. Los textos deben describir controles sin cierres registrados en el universo del pipeline, contrastes por cohorte y agregación. Callaway–Sant’Anna, Sun–Abraham y Roth son marco metodológico; **no** se atribuye implementación exacta del estimador CS. La fila +9,11 pp se llama «ponderado por expuestos»/«exposed-weighted».
- +1,85 pp de ausencia persistente es máximo entre **cinco regímenes**, no de los años individuales; la serie anual llega a +4,56 pp. −14,64 de celdas exactas y −13,24 de muestra modelada distinta no comparten denominador.
- III: +9,11 pp histórico y +5,29 pp 2016–2019 tienen universos distintos; las cotas recientes [−1,15; +10,98] incluyen cero; −3,35 pp de receptoras es descriptivo y sin intervalo propio.
- IV: la serie descriptiva cubre 2009–2022, los modelos se centran en 2016–2019; −0,29 es diferencia estimada, no tasa, con IC [−2,64; +2,06]. IP/CFT −2,09 depende del modelo, mientras DiD −2,59 tiene *p* = 0,28 y 12 tratados. Universidad +1,98 tiene intervalo que cruza cero: sustitución frente a pérdida neta sigue sin identificarse. G1 −12,26 y −0,26 pertenecen a quintiles **recalculados** entre especificaciones, no a los mismos alumnos seguidos.

## Salida requerida

Primera línea exacta `REVIEW_VERDICT: APPROVE` o `REVIEW_VERDICT: REQUEST_CHANGES`. Después: hallazgos en una línea por caso `[SEV] archivo:línea → problema → fix (evidencia)`; separa bloqueos de opcionales. Indica inventario 8/8, pruebas documentales, falsadores y límites de lo no inspeccionado. Si hay nueva discrepancia científica, identifica fuente/denominador/estimador en conflicto; no inventes recomputación. Cierra con `PLAN_STATE v2`, `HANDOFF-TRACE:` y `MODEL-REPORT:`. La revisión de figuras y el PDF quedan fuera de este dictamen.
