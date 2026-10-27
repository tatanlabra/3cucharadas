# Documento sombra editorial — Post III

Este documento acompaña la edición; no forma parte del relato público ni sustituye los artefactos científicos canónicos.

## Contribución de la serie

| Entrega | Unidad | Pregunta | Aporte | Límite que hereda la siguiente |
|---|---|---|---|---|
| I | Establecimientos, 1992–2012 | ¿Qué resultados de la tesis pueden reconstruirse? | Audita 34 afirmaciones y separa resultados reproducibles, errores y discrepancias. | Entradas y salidas administrativas no muestran trayectorias individuales. |
| II | Eventos recientes y territorio | ¿Qué cerró y apareció una alternativa comparable cerca? | Distingue 900 cierres oficiales, 330 estrictos y 38 con apertura cercana del mismo segmento. | Cercanía no demuestra destino, cupos ni continuidad. |
| III | Trayectorias estudiantiles | ¿Qué ocurrió después y qué debe proteger una transición? | Estima resultados escolares, hace visible la selección de registros y traduce límites en condiciones de política. | Estado `INCONCLUSIVE`: el contrafactual, el anuncio y la pérdida selectiva siguen abiertos. |

## Registro de afirmaciones y límites

| Afirmación pública | Fuente congelada | Límite inseparable |
|---|---|---|
| 79.709.054 matrículas y 73.873.835 registros de rendimiento, 2004–2025 | `post3_database_release_v2.json` | Volumen no crea identificación causal. |
| No matrícula persistente: +0,63 pp, IC 95 % [−0,77; 2,03] | `post3_modern_causal_v3_1.json` | Ausencia del registro no equivale a deserción. |
| No promoción o rezago: +5,29 pp, IC 95 % [2,08; 8,51] | `post3_modern_causal_v3_1.json` | Toda mención conserva cotas por faltantes [−1,15; 10,98] pp. |
| Comparabilidad observada: edad 11,70/11,70; asistencia 90,93/91,68; notas 5,62/5,67 | `post3_school_comparability_v1.json` | Brecha de cobertura de rendimiento: −19,4 pp; no certifica aleatorización. |
| 62 cierres equivalen a 21,1 y 21,9 clústeres efectivos en resultados primarios | `post3_identification_alternatives_v1.json` | Es una heurística de información independiente, no una promoción causal. |
| Asistencia y notas son exploratorias y condicionadas | `post3_modern_causal_v3_1.json` | No tienen cotas equivalentes de datos faltantes. |
| Cinco tablas HMG permanecen no comparables | `post3_hmg_replication_status.json` y especificación histórica | Las cifras publicadas no confirman ni corrigen una ejecución no recuperada. |

El recibo autocontenido que proyecta estos campos y sus hashes está en `docs/contracts/evidence/post3-scientific-release-v3_1.json`. Declara `upstream_custody: UNCOMMITTED_FILE_HASHES`: acredita la relación entre el post y la proyección congelada, pero no reemplaza la custodia de los artefactos científicos en un commit upstream. El verificador funciona en un checkout autónomo; si se define `POST3_RESEARCH_ROOT`, además exige igualdad byte a byte con los artefactos fuente.

## Decisiones editoriales

| Decisión | Razón | Pérdida aceptada | Condición de revisión |
|---|---|---|---|
| Publicar resultados escolares ahora | El cierre escolar tiene evidencia suficiente para una lectura `INCONCLUSIVE` útil en política. | No responde aún por trayectorias postsecundarias. | Nuevos microdatos oficiales y enlace validado SIES/DEMRE. |
| Dejar educación superior como agenda breve | No hay insumos acreditados para estimar ni sugerir efectos. | Se elimina el contrato metodológico extenso del cuerpo. | Una entrega posterior tendrá diseño y verificador propios. |
| Mantener diferencias en diferencias como exploratoria | Hay comparación antes/después y grupos observables parecidos. | No se atribuye causalidad. | Anuncios, eventos confirmados, medición previa estable y diseño independiente. |
| No estimar variable instrumental | SLEP, SAE, matrícula y shocks tienen canales directos hacia los resultados. | No se ofrece una cifra de aparente precisión. | Regla o sorteo documentado que satisfaga relevancia, exclusión, anticipación e interferencia. |
| Conservar la cápsula HMG | Permite contrastar el antecedente sin simular una réplica exacta. | Ocupa espacio editorial. | Recuperación del insumo, código y transformaciones originales. |

## Contrato de paridad ES/EN

- Misma fecha, `ref`, permalink, tres figuras, cuatro tablas, universos, cifras y estado epistémico.
- Español chileno profesional; inglés institucional con ortografía británica.
- La traducción conserva la intención y el límite, no una sintaxis palabra por palabra.
- La versión española debe contener entre 3.000 y 3.500 palabras visibles antes de referencias.

## Cortes realizados

- Se reemplazaron cinco párrafos de educación superior por una agenda de una sola unidad semántica.
- Se reforzó el tránsito I→II→III en la apertura y el cierre.
- Se explicó comparabilidad, clústeres efectivos y resultado inconcluso con analogías breves.
- Se conservaron las tres figuras, cuatro tablas, cápsula HMG, literatura y transparencia.
- Se eliminaron formulaciones de bitácora o de bloqueo editorial del post público.

## Falsación editorial

- El gate debe fallar si aparece un marcador científico/editorial contradictorio o duplicado.
- El gate debe fallar si cualquier `5,29`/`5.29` —con o sin signo, y también redondeado a `5,3`/`5.3`— queda sin ambas cotas en el mismo bloque semántico y a no más de 420 caracteres.
- El gate debe fallar si reaparece el bloqueo SIES, una cifra postsecundaria o una promoción causal en cuerpo o metadatos.
- El gate debe fallar si el post vuelve a `_drafts`, si ES/EN divergen en cifras de tablas o figuras, o si faltan figuras/tablas/referencias.
- El gate de navegador solo puede aprobar con `--artifact-root`, igualdad byte a byte entre HTML servido y artefacto, CSS ligado al mismo build y conteos críticos iguales a las fuentes actuales.

HANDOFF-TRACE: Codex integrador → Claude Sonnet, revisión adversarial read-only `REQUEST_CHANGES` → Codex integrador; falsos verdes de cotas, paridad numérica y artefacto servido corregidos y re-falsados localmente.
