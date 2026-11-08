REVIEW_VERDICT: REQUEST_CHANGES

Hay 4 defectos materiales y 6 menores. Todos son de calibración o trazabilidad, ninguno de cifras. No edité nada; el modo plan solo permite lectura y la revisión es de solo lectura.

## Resultado Goldfish

| Criterio | Veredicto | Evidencia |
|---|---|---|
| 1. Preámbulo (motivación, conclusión, comparación, límite) | Cumple, con una reserva en III | IV lo hace bien. En III, la reserva es el hallazgo M1 |
| 2. Hilo y extensión | Cumple | IV ≈ 2.822 palabras (mi conteo, sin referencias ni HTML), cerca del mínimo de 2.800. Sin etiquetas ELI5. Las tres cucharadas encadenan pregunta, evidencia y transición |
| 3. Anexos sin esconder límites | Falla en 2 puntos | M3 y M4 |
| 4. Mismo hecho y mismo límite que la fuente | Falla en 2 puntos | M2 y M3. No hay causalidad promovida desde no significación |
| 5. Cierre y referencias | Cumple, con reserva | Recapitula. El tercer desafío de IV no es verificable (m3) |
| 6. Preámbulo, alt y cierre contra tablas | Falla en 1 punto | M2 |

Cifras que sí verifiqué contra anexos y CSV:
- **Parte III:** 89,7 % y 86,7 %; 62,5 %; 73 % de la brecha entre estables; 255 estudiantes; las cotas de 2016–2019.
- **Parte IV:** 82,0 %; 57,5 %; 27 %; la escalera de `selection-ladder-data.csv`; las filas de admisión; la serie 2009–2022.
- **Coherencia entre archivos:** sin contradicciones numéricas entre el artículo principal y sus anexos.

## Hallazgos materiales

**[MAT] M1 · `_posts/2026-10-23-…md:5,58` → «brecha» sin definir en el preámbulo.**
- El subtítulo dice que «la estimación puntual del rezago… fue mayor que la de sus pares». Eso se lee como una comparación de tasas.
- El estimando es una diferencia entre el cambio de expuestos y el cambio de controles. Esa definición recién aparece en la cucharada 2 (línea 84).
- Es justo la confusión tasa vs. diferencia de tasas del criterio 1.
- Ajuste: subtítulo con «el aumento del rezago… fue mayor que el de sus pares». En el aside, «brecha estimada (diferencia entre el cambio de expuestos y el de controles)».

**[MAT] M2 · `_posts/2026-11-04-…md:11,47,108,121` y alt de la fig. 1 → el −0,26 de G1 no tiene tabla ni CSV.**
- La conclusión «G1 pasa de −12,26 a −0,26 al añadir historia G−5» aparece en el extracto, el cierre y el alt.
- La tabla A4 del anexo solo tiene una fila de controles completos, para IP/CFT.
- `causal-ml-heterogeneity-paes-data.csv` no contiene −0,26, ni la pendiente BLP de acceso total con controles completos. Solo trae los GATE con controles estudiantiles y las filas PAES.
- Lo mismo vale para los GATE de IP/CFT con controles completos (G1 −2,57; G3 −3,92): no están en el CSV.
- No puedo verificar la cifra con las fuentes locales. La figura A2 (caption, anexo) admite que esa comparación «no aparece en el panel A».
- Ajuste: añadir a A4 la fila «Controles completos: Acceso ES 2 años» con G1, β₂ y p. Añadir esas filas al CSV. O, si el CSV no puede cambiar, anotar el origen del −0,26 en el anexo.

**[MAT] M3 · `_posts/2026-11-04-…md:106` → «resultado sólido» para el −2,09 de IP/CFT es sobrecalibrado.**
- En la misma comparación, el análogo de cohortes repetidas (anexo, tabla A3 y nota) es −2,59 pp, EE 2,29, p = 0,28, con 12 liceos tratados.
- El −2,09 usa error estándar agrupado (EE 0,72, p = 0,0037) sobre esos mismos pocos liceos.
- El principal solo dice, en la línea 96, que «ninguna diferencia entre regímenes se distingue de cero». No contrasta el −2,59 con el −2,09.
- Ajuste: reemplazar «sólido» por «la única señal que sobrevive al modelo completo». Añadir una oración con el −2,59 (p = 0,28) y los 12 liceos tratados. El anexo ya tiene todo.
- Relacionado, en el alt de la fig. 1: «caída significativa de −2,09». Cambiar por «estimada distinta de cero bajo el modelo».

**[MAT] M4 · `_posts/2026-11-04-…md:94` ↔ `_pages/tesis-post4-anexo-metodologico.md:237` → un límite que decide la lectura de básica superior está solo en el anexo.**
- El anexo advierte que la cohorte G−5 de 7.º Básico cursaba 3.º Medio en G−1, así que no es un brazo pre-tratado puro. El sesgo del DiD de básica va hacia cero.
- El principal presenta +1,21 y +1,02 como «incluyen pérdidas y ganancias plausibles» y no menciona ese sesgo.
- Ajuste: una oración en el principal, línea 94: «el diseño puede sesgar hacia cero esta estimación».

## Hallazgos menores

- **[MEN] `_posts/2026-11-04-…md:96` y anexo `:143`.** «Ninguna diferencia entre regímenes se distingue de cero» sugiere una prueba entre regímenes. Los p citados (0,28; 0,18; 0,12) son de cada régimen contra cero. Reformular. Y dar el IC o el p del −3,79 (EE 1,81 con 7 conglomerados), que si no se lee como significativo.
- **[MEN] Anexo IV `:28,33`.** «Versión simplificada de HonestDiD» en el título de la tabla A1 conserva el nombre pese a la salvedad del propio aside. Alinear con el anexo III: «versión lineal simplificada inspirada en Rambachan y Roth».
- **[MEN] Anexo IV `:44`.** «Los entrantes tardíos sufren un choque mayor» contradice el «no identifica su causa» de la fila 41. Cambiar por «muestran una brecha mayor».
- **[MEN] Anexo III `:138,216` ↔ anexo IV `:40`.** El «70,6 % del total» se asigna a 3.556 estables, pero 70,6 % de 6.581 son ≈ 4.645. 3.556 es el 77,5 % de 4.589 con curso observado. Separar los dos denominadores.
- **[MEN] Anexo IV `:63` ↔ principal `:96`.** El anexo habla de 19 liceos medios cerrados en 2016–2019. El DiD usa 12 conglomerados y el principal dice «12». Falta explicar la diferencia (soporte).
- **[MEN] Cierre IV `:123`.** El tercer desafío («reforzar la identificación…») no tiene criterio de aceptación observable. Precisar, por ejemplo, la sensibilidad Cinelli–Hazlett con un confusor de fuerza ≥ X, o más liceos tratados.

## Opcionales

- III: el aside combina el +9,11 de la serie con el límite de 2016–2019. Falta una frase de que las cotas de la serie (+0,43 a +16,21) excluyen cero. Hoy el lector puede creer que todo el titular es inconcluso.
- IV: el preámbulo usa «puntos» sin decir que es diferencia de tasas de ingreso (50,61 % vs 65,24 %). Lo dice la cucharada 1.

## Fortalezas y contraejemplos

- **Preámbulo de IV:** la separación −14,64 / −12,00 / muestras distintas y el «no sumar» de 82,0 % y 57,5 % están bien resueltos.
- **Parte III:** las cotas de Manski conviven con el IC en el mismo párrafo. El −3,35 de receptoras queda como descriptivo, sin intervalo propio. El 2016–2019 es «inconcluso por sí solo».
- **Parte IV:** la sustitución IP/CFT→universidad se enuncia como hipótesis rival, con prueba discriminante y condición de descarte.
- **Contraejemplo a M3:** el DML con validación cruzada por liceo sí es un diseño distinto del DiD de cohortes. Un −2,09 más preciso no es contradictorio per se. Lo exigible es declarar la discrepancia, no rebajar el hallazgo.

## Límites y riesgo residual

- No reestimé nada ni verifiqué `.csv` fuera de los cinco que cité. Los manifiestos de figuras y las versiones EN quedaron fuera de alcance.
- No ejecuté los verificadores de conteo de palabras. El 2.822 de IV es mi conteo aproximado; III queda en 2.553 según Codex y no lo repliqué.
- Riesgo residual tras corregir M1–M4: bajo. M2 es el único que puede obligar a tocar un CSV, y por tanto las figuras.

EDITORIAL_REVIEW_COMPLETE

HANDOFF-TRACE: Claude → Codex vía claude-bridge; revisión completada.

MODEL-REPORT: Claude Sonnet 5.5 (`claude-sonnet-5-5`), Anthropic.

PLAN_STATE v2 (F2 actualizado, plan no cerrado):
```yaml
- id: "F2"
  glyph: "[~]"
  status: "active"
  step: "F2 · Claude · revisión adversarial ES realizada; dictamen REQUEST_CHANGES (M1–M4 + 6 menores); correcciones pendientes del editor ES"
  deps: ["ES"]
- id: "CLAUDE_NET"
  glyph: "[x]"
  status: "done"
  verification: {kind: "observation", ref: "revisión completada por este canal; receipt r1 (EAI_AGAIN) preservado"}
# F0, B0, C0, ES, FIG, HERO, BOARD sin cambios. F1, SITE, LIVE_RED, ANNEX_TABLES siguen activos. F3, EN, PDF, F4, F5 siguen pendientes y dependen de F2.
```
