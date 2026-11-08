REVIEW_VERDICT: APPROVE

**Dictamen:** [Posts III–IV + anexos, ES] → los 2 materiales y 4 menores de r3 están resueltos y no veo regresiones materiales → verifiqué contra los cuatro archivos completos y el JSON público. Quedan 3 menores y 2 opcionales, ninguno bloqueante. No edité nada. Esta ronda es dirigida, no un segundo Goldfish.

## Resolución de r3

| Hallazgo r3 | Estado | Evidencia |
|---|---|---|
| MAT 1 · G1 no es el mismo grupo | Resuelto | Excerpt `IV:11`, cuerpo `IV:110`, cierre `IV:123`, alt y caption A2 (`anexo IV:165,168`) dicen que el quintil se recalcula y que no es una mejora de las mismas personas. |
| MAT 1 · CLAN completo en anexo | Resuelto | `anexo IV:191` coincide con el JSON (`full_student_and_school_g5_controls.any_he_two_year`): 91,24 % media, 51,79 % TP, notas 5,79 vs 5,20, asistencia 85,04 vs 93,35, estables 85,34 vs 58,89, rezago 6,31 vs 12,09. |
| MAT 2 · nota `chernozhukov2018` | Resuelto | Definida en `IV:145`; las 12 notas del principal IV están citadas y definidas, y lo mismo vale para III y ambos anexos. |
| MEN 1 · límite IP/CFT en aviso | Resuelto | `IV:51` yuxtapone el DiD −2,59 (p = 0,28). |
| MEN 2 · intervalo de −0,29 | Resuelto | `IV:47` trae `[−2,64; +2,06]`. |
| MEN 3 · cruces "A1/A4 del cuerpo" | Resuelto | `anexo III:173,209` dicen «de este anexo». |
| MEN 4 · `</details>` huérfano | Resuelto | No quedan en los anexos. |
| Opcionales | Integrados | Se añadió `{: .table-caption}` a A4 de III (`anexo III:94`) y la nota de multiplicidad (`anexo IV:193`). |

## Hallazgos nuevos (todos menores)

- **[MEN] `anexo IV:25,35` → el encuadre quedó obsoleto: dice que en la parte III «faltaban dos pruebas de sensibilidad», pero III ya las trae (`III:116`, `anexo III:141,219`) → reescribir como «pruebas ya reportadas en III; se reproducen aquí por conveniencia», o retirar el párrafo y remitir al anexo III.** Esta contradicción de referencias cruzadas heredaría el EN si no se corrige antes de F3.
- **[MEN] `anexo IV:217` → «Esa prueba queda pendiente para una próxima entrega», pero IV se presenta como «esta última entrega» (`IV:44`) y el desafío 1 la plantea como tarea abierta (`IV:127`) → cambiar a «queda pendiente (desafío 1 del artículo)».**
- **[MEN] `anexo IV:215` → «Quienes aspiran a carreras universitarias selectivas y llegan con buenas notas… presentan estimaciones ajustadas sin caída detectable» atribuye a un subgrupo lo que la tabla A5 estima para toda la muestra → reformular: «en la muestra completa, las estimaciones ajustadas de rendición y selectividad no muestran caída detectable».**

## Opcionales

- `IV:143,145` → `chernozhukov2018` va después de `cinellihazlett2020`; el resto de las referencias, y el anexo IV, siguen orden alfabético por clave. Intercambiar las dos líneas.
- `anexo IV:284,96,98` → «mochila estudiantil» aparece con −5,63 (PLR), −4,88 (R-Learner) y −6,11 (FWL). Una frase que explique que son estimadores distintos evitaría confusión.

## Criterios

| Criterio | Veredicto |
|---|---|
| 1. Preámbulo | Cumple. III define la brecha como diferencia de cambios (`III:58`) y IV separa tasa de diferencia de tasas. El límite IP/CFT ya figura. |
| 2. Hilo y extensión | Cumple. Con el conteo del editor, III = 2.572 y IV = 2.887, ambos dentro de rango (IV cerca del piso). No encontré ELI5 ni relleno. |
| 3. Anexos y límites | Cumple. Los límites decisivos están en el principal y el CLAN completo ya está en el anexo. |
| 4. Mismo hecho y límite | Cumple. No veo causalidad promovida desde no significación. El G1 de IP/CFT queda explícitamente «incluye cero». |
| 5. Cierre y referencias | Cumple con los 2 menores de arriba. Hay tres desafíos verificables por artículo y los anclas `#tabla-…`, `#fig-…` resuelven. |
| 6. Preámbulo, alt y cierre vs. tablas | Cumple. Contrasté contra el JSON los GATE IP/CFT (G1 −2,57; G2 −2,94 [−5,87; −0,01]; G3 −3,92; G5 −0,93) y la pendiente BLP 0,0177. |

## Fortalezas y contraejemplos

- **III:** separa Manski de la inferencia por intervalos. La descomposición D0/D1/D2 cuadra aritméticamente: 174 = 158 + 16, 129 = 95 + 34, 346 = 266 + 15 + 35 + 30, 145 = 69 + 57 + 13 + 1 + 5.
- **IV:** declara la sustitución IP/CFT→universidad como hipótesis rival, con prueba discriminante y condición de descarte (`IV:120`).
- **Contraejemplo a mi propia lectura:** con controles solo estudiantiles, el G5 también es negativo y significativo (−3,03 [−5,92; −0,14], `anexo IV:178`). Eso refuerza que «G1» no es un grupo especialmente dañado y el texto no lo sobrepromueve.

## Límites y riesgo residual

- **Verificado** contra el JSON: CLAN completo, GATE y BLP IP/CFT, 14,24 (`audit.json:125`). Verifiqué de forma aritmética: los p de 6 g.l., el 82,0 %, el 57,5 %, el 27 % y los conteos de las tablas de III.
- **No verificado:** la banda de recorte `[+3,79; +6,80]` (`anexo IV:49`), los manifiestos de figuras y el CSV de cada figura. No ejecuté builds ni verificadores.
- **Fuera de alcance:** las versiones EN.
- **Riesgo residual:** bajo. Los tres menores son de redacción en el anexo IV, sin tocar CSV ni JSON. Conviene corregirlos antes de que el adaptador EN consuma los anexos.

EDITORIAL_REVIEW_COMPLETE

HANDOFF-TRACE: Claude → Codex vía claude-bridge; revisión dirigida r4 completada.

MODEL-REPORT: Claude Sonnet 5.5 (`claude-sonnet-5-5`), Anthropic.

PLAN_STATE v2 (plan no cerrado; solo cambia F2):
```yaml
- id: "F2"
  glyph: "[~]"
  status: "active"
  step: "F2 · Claude · revisión dirigida r4 realizada; dictamen APPROVE (0 materiales; 3 menores en anexo IV, 2 opcionales); correcciones menores opcionales antes de F3"
  deps: ["ES"]
# Resto del estado recibido sin cambios. F3, EN, PDF, F4 y F5 siguen pendientes; el plan completo no está cerrado.
```
