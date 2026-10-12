# F23 — E46: custodia científica y hoja de ruta causal

Fecha: 2026-10-12. Estado: E46 implementado y revisado con caveats; sin autorización de publicación ni de inferencia causal.

## PLAN_STATE v2

```yaml
version: 2
plan_id: thesis-post2-closeout-20261011
task_id: E-46
state: peer_reviewed_done
peer_verdict: ACCEPT_WITH_CAVEATS
research_commit: 8a71aadb7017ef02833c961c463e97098cfa6d21
blog_commit: 8c1b0e11f7b8d3e17d360ba91ee29772b96d4567
causal_claim_authorized: false
external_actions_authorized: false
```

## Custodia

| Superficie | Evidencia |
|---|---|
| Investigación | Rama `release/thesis-post-ii-science-20261012`, commit `8a71aadb7017ef02833c961c463e97098cfa6d21`, worktree limpio y sin upstream. |
| Blog | Rama `release/thesis-post-ii-public-clean-20261012`, commit revisado `8c1b0e11f7b8d3e17d360ba91ee29772b96d4567`. |
| Primera rerevisión | `archivo/handoffs/.originals/response.EB0Fwn.txt`, SHA-256 `d30c71bba73ce71b291a0af2292992fa544a19ccf4354e396e19c3b7761fa51a`, veredicto `REQUEST_CHANGES`. |
| Briefing final | `archivo/handoffs/.originals/20261012T190902Z_INBOX_codex-a-claude.md.source`, SHA-256 `fd2978d38d281b4936bc75a496d5d363ce436b0ae362db4d8ce779e114129861`. |
| Respuesta final | `archivo/handoffs/.originals/response.Ojjhcr.txt`, SHA-256 `254f3e62c93f240c273c0672910420f4d401869e768b66c86c2118381e6b53bc`, veredicto `ACCEPT_WITH_CAVEATS`. |

HANDOFF-TRACE: Codex → Claude Opus por CLI local → REQUEST_CHANGES → reparación N1/M1/M3 y B1–B3 → rerevisión read-only → ACCEPT_WITH_CAVEATS → Codex integra; DEC-REL-007 y toda acción externa siguen bloqueadas.

## Rojo → verde falsado

| Criterio | Rojo observado | Verde observado |
|---|---|---|
| N1, AP-035 | `254 --validate` fallaba por un hash de freeze obsoleto. | `254 --validate` y `316 --validate` salen 0 sin builder; alterar AP-035, un byte del freeze, la topología Git o agregar un commit hijo produce exit 2. |
| M1, lenguaje causal | SRF-014 podía afirmar causalidad y conservar `NOT_CAUSAL`; el freeze lo aceptaba exit 0. | Igualdad exacta con el diccionario canónico; cinco mutaciones semánticas son rechazadas y el control pasa. |
| M3, aislamiento visual | 44 pruebas salían verdes mientras reescribían doce archivos versionados y dejaban 316 rojo. | 67 pruebas corren en `tmp_path_factory`, salen 0 y no cambian status ni mtimes de la raíz. |
| B1, decisión humana | E-38 aparecía cerrada aunque DEC-REL-007 seguía `pending/selected:null`. | E-38 queda `implemented_pending_human_decision`; E-39 depende de su implementación, no de una aprobación inexistente. |
| B2, sensibilidad SAE | Las filas 2019 parecían una sensibilidad distinta aunque no retiraban controles ese año. | Las dos filas explicitan que son idénticas a la principal en 2019. |
| B3, caso autor | `uses_outcomes:false` ocultaba que El Salvador fue propuesto conociendo el evento. | YAML, renderer, metadatos SVG y gate declaran `selected_on_event:true` y ausencia de outcomes medidos. |

## Caveats que no se convierten en cierre ficticio

| Caveat | Estado y límite |
|---|---|
| Portabilidad visual M3b | Dos corridas locales son deterministas, pero siete PNG, un SVG y cinco derivados no reproducen los bytes históricos en este host; el freeze los acopla transitivamente mediante audits con hashes. |
| Restaurabilidad F4 | Nueve insumos públicos preexistentes siguen fuera de Git; el freeze conserva `restorability: NOT_ESTABLISHED`. Los validadores focales pasan en un clon sin esos insumos. |
| Validador 313 | Tres fallos no focales son idénticos en base y candidato por deriva entre schema 5 y expectativas antiguas; candidato menos base es el conjunto vacío. |
| Topología Git | Un futuro commit humano, merge o upstream cambia la observación congelada; el recibo debe regenerarse después de esa acción, no antes. |

## Qué hipótesis se prueban hoy

| Línea | Hipótesis o estimando | Estado inferencial |
|---|---|---|
| H1, mercados | Si una definición espacial cambia el contraste ajustado P75–P25 de riesgo respecto de comuna. | Confirmatoria asociacional sobre posición relativa; no es una dosis común ni un efecto causal de la frontera (`publication/spatial_dynamics_spec.yaml:95-133`). |
| H2, vulnerabilidad | Si el contraste de riesgo asociado a competencia varía entre P25 y P75 de vulnerabilidad escolar. | Exploratoria; el soporte por celda no alcanza para una familia confirmatoria (`publication/spatial_dynamics_spec.yaml:134-155`). |
| H3, trayectorias | Si matrícula, desempeño y composición entre t-3 y t-1 difieren entre escuelas que cierran desde actividad y las que siguen activas. | Descriptiva; no acredita anticipación causal (`publication/spatial_dynamics_spec.yaml:156-163`). |
| SLEP | ATT por cohorte sobre tasa de cierre público y log de matrícula después del traspaso efectivo. | Diseño rechazado: fallan ambas equivalencias previas y solo hay 3–4 territorios tratados (`audit/article_post2_research_closeout.json:359-386`). |
| SAE | ATT del despliegue temprano sobre HHI comuna-grado y log de establecimientos efectivos. | Gates observables aprobados, pero efecto inconcluso: las 4 celdas cambian de signo al excluir alguna de 5 regiones tratadas (`audit/article_post2_research_closeout.json:43-139`). |

E46 prueba que estas afirmaciones y límites son portables y falsables. No prueba que H1–H3, SLEP o SAE identifiquen causalidad.

## Escenarios de éxito causal

| Escenario | Qué tendría que ocurrir | Condición de descarte |
|---|---|---|
| Efecto robusto | Estimando y ventana preespecificados, soporte suficiente, equivalencia previa, ausencia plausible de anticipación/spillovers, dirección y magnitud estables, e inferencia válida para pocos conglomerados. | Falla cualquier gate duro o el signo depende de una unidad tratada. |
| Equivalencia práctica | El intervalo completo queda dentro de una ROPE/MDE de relevancia pública fijada antes de estimar. | `p > 0,05` sin precisión no cuenta como ausencia de efecto. |
| Heterogeneidad o mecanismo | Interacción preespecificada y soportada, con mecanismo intermedio medido y multiplicidad controlada. | La interacción aparece solo después de mirar resultados o queda sin soporte por celda. |
| No identificación honesta | El diseño se rechaza o queda inconcluso con el motivo cuantificado, como hoy en SLEP/SAE. | Es éxito de integridad científica, no evidencia causal ni permiso para afirmar efecto nulo. |

La meta no es “encontrar efectos”, porque ese criterio incentiva búsqueda ex post. La meta es identificar o acotar efectos de magnitud relevante bajo un diseño que pueda ponerse en rojo.

## Ambición óptima factible

| Prioridad | Diseño propuesto | Gates mínimos antes de estimar |
|---|---|---|
| SAE-1 | Triple diferencia región × grado de entrada × cohorte/año, incluyendo 2019 solo si el contraste de grados no tratados es creíble. | Outcomes por grado, tendencias diferenciales previas, test explícito de spillover intrarregional, soporte por celda y especificación congelada. |
| SAE-2 | Cadena de mecanismos: postulaciones, asignaciones, flujos entre escuelas y composición; luego concentración, cierres y aprendizaje. | Trazabilidad temporal, denominadores estables, no usar outcomes posteriores para seleccionar mecanismos y control de multiplicidad. |
| SAE-3 | Inferencia para cinco regiones tratadas: leave-one-region-out, wild cluster/bootstrap apropiado, randomization inference solo si existe una asignación conocida, y sensibilidad a tendencias. | No usar permutaciones que supongan aleatorización inexistente; declarar MDE/ROPE antes de reestimar. |
| SLEP-1 | Ampliar cohortes y postratamientos del calendario efectivo reconciliado; separar anuncio y traspaso como tiempos de evento. | Más conglomerados tratados, equivalencia previa conjunta, soporte no tratado y diagnóstico de anticipación/spillovers. |
| SLEP-2 | ATT escalonado como principal; synthetic DiD o control sintético solo como robustez cuando exista buen ajuste y donantes no contaminados. | Si pretrends, soporte o ajuste donante siguen fallando, mantener `DESIGN_REJECTED_NOT_IDENTIFIABLE`. |
| Política | Definir actor, unidad de intervención, horizonte, outcome primario y magnitud mínima útil antes del análisis. | Ningún resultado escolar agregado autoriza cierre automático ni inferencia individual. |

## Deducción, inducción y abducción

- **Deducción:** con 0 de 4 celdas SAE de signo estable y ambas equivalencias SLEP fallidas, los resultados actuales no sostienen una conclusión causal direccional.
- **Inducción:** la fragilidad SAE se repite en dos outcomes y dos años, por lo que no parece una anomalía aislada de una celda.
- **Abducción:** heterogeneidad regional, contaminación entre grados o calendario incompleto explican mejor la inestabilidad que un efecto común bien determinado; se descartan si cohortes adicionales no contaminadas preservan signo y magnitud.
- **Contrafactual:** aun con estimaciones significativas, un resultado que desaparece al excluir una región o al mover la ventana no sería suficientemente robusto para orientar política.

## Cierre

| Estado | Resultado |
|---|---|
| Implementado | E46 portable, recibos exactos, N1/M1/M3 falsados, B1–B3 alineados y revisión Claude `ACCEPT_WITH_CAVEATS`. |
| Parcial | Portabilidad visual, restaurabilidad F4, validador 313 y diseños causales SAE/SLEP permanecen explícitamente abiertos. |
| No implementado | Aprobación humana, DEC-REL-007, push, despliegue, paridad pública, difusión y nuevas estimaciones causales. |
