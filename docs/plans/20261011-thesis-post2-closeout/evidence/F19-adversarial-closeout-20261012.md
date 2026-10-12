# F19 — cierre adversarial y preview HTTPS

- Fecha: `2026-10-12`.
- Integrador: Codex.
- Par: Claude Opus 5.5, solo lectura.
- Veredicto final del par: `APPROVE`.
- Estado externo: H1 activo; commit de seguimiento, push, deploy y difusión no ejecutados.

## Hallazgos y adjudicación

| Hallazgo | Estado | Evidencia de cierre |
|---|---|---|
| Seis puntos MR2 subsoportados permanecían en la nota técnica | Corregido | ES/EN conservan `NOT_ESTIMABLE` y soporte 4/6/8 y 1/1/2 sin publicar los puntos; `mr2-points-technical` termina `EXPECTED_FAIL`, exit 1. |
| Dos SVG MR2 retirados seguían en el artefacto | Corregido | `verify_site_artifact.rb` se observó rojo por `Pruned asset is present`; `_config.yml` los excluye y el artefacto final pasa con 70.887.200 bytes y 1.510 entradas. |
| PH-10 apuntaba al calendario SAE | Corregido | `PLAN_STATE.yml` usa `slep_transfer_schedule.yaml`; el post enlaza la URL canónica DEP verificada HTTP 200. |
| El gate tipográfico aprobaba una colección vacía | Corregido | Mide `p`, `ul` y `ol`, exige al menos un bloque y los canarios vacío/ancho terminan `EXPECTED_FAIL`, exit 1. |
| El canario de scroll ejercitaba la rama de compatibilidad | Corregido | Ahora fija `initializationVisualShiftPx: 577` e `initializationScrollDeltaPx: 0`; termina `EXPECTED_FAIL`, exit 1. |
| El archivo vivo versionaba una IP Tailnet | Corregido con bloqueo residual | Cero literales en el árbol vivo; el commit histórico `3e62f95f` mantiene EXT bloqueado hasta preparar una historia pública limpia. |

## Verde final

| Gate | Resultado |
|---|---|
| Semántica y paridad | `PASS`, exit 0; freeze `15eee9b...`; advertencias blandas 4.401 palabras ES y 4.335 EN. |
| `PLAN_STATE` H1 | exit 0; 18 placeholders y 37 tareas emergentes. |
| Prepublicación H1 | exit 0. |
| Build Jekyll producción | exit 0; solo avisos Sass deprecados. |
| Artefacto | exit 0; 70.887.200 bytes y 1.510 entradas. |
| Matriz HTTPS | `PASS`, exit 0; 24/24 páginas, 12/12 SVG y 2/2 fallbacks. |
| Medida de escritorio | 62 bloques, máximo 720px, artículo 796px y overflow 0 a 1.440px. |
| Diff | `git diff --check` exit 0. |

## Custodia del tándem

- Sesión Claude reanudada: `813a3ef7-b1f7-47fc-be3e-5447f1dcc89e`.
- Briefing inicial: `penta-agent/.agents/queue/2026-10-12-post2-f19-rereview.md`, SHA-256 `a4c85ee588dfa334598697d93614f8102d1cd19c9401f0371bf39ecdd2b7c4fb`.
- Briefing estrecho: `penta-agent/.agents/queue/2026-10-12-post2-f19-narrow-rereview.md`, SHA-256 `769ab25e99fb50004e788e3f59bc510a9d1e52189045be1ec538da38f41a6421`.
- Respuesta final original: conservada en la sesión Claude indicada; comienza `Veredicto: APPROVE` y reporta `MODEL-REPORT` de `claude-opus-5-5`.
- Adjudicación del integrador: la observación baja de que faltaba `1992–2012` quedó refutada por la línea 42 actual de ambos posts; el período está presente y la paridad termina exit 0.

HANDOFF-TRACE: Claude REQUEST_CHANGES → Codex reparó los tres bloqueos → Claude reprodujo los cierres y emitió APPROVE → Codex adjudicó deuda no bloqueante → humano conserva H1 y toda autoridad externa.
