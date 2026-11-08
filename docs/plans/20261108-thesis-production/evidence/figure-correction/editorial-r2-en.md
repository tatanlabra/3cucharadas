# Respuesta editorial EN a Claude: B1–B7

Estado: B1–B7 corregidos en las fuentes EN bajo ownership editorial. El artículo IV EN no requirió cambios en esta ronda: el dictamen consideró conformes ambos cuerpos principales, salvo el párrafo huérfano de III. B8 corresponde al anexo III ES y tiene otro escritor. No modifiqué CSV, JSON, SVG, valores, identidades de tablas, títulos, fechas, referencias ni permalinks. El dictamen original está en `docs/plans/20261108-thesis-production/evidence/claude-editorial-complete/result.md`.

| Hallazgo | Resolución y evidencia |
|---|---|
| B1 · sensibilidades III supuestamente pendientes | El anexo IV EN dice que el artículo y anexo III ya reportan tendencias no paralelas y anclaje $$G-2$$; las reúne como referencia (`_pages/tesis-post4-anexo-metodologico-en.md:24-32`). |
| B2 · +1.21 pp como ausencia de daño | El contraste de básica superior se declara inconcluso: el brazo $$G-5$$ podría haber sido afectado y atenuar una caída; no demuestra beneficio ni ausencia de daño (`_pages/tesis-post4-anexo-metodologico-en.md:253`). |
| B3 · estrategias independientes que se sostienen mutuamente | El aviso presenta dos ajustes con supuestos propios y admite sesgos compartidos por omisión o comparabilidad; elimina la promesa «belt and suspenders» (`_pages/tesis-post4-anexo-metodologico-en.md:85-88`). |
| B4 · 57.5% como fracción causal | Único cambio a celda interpretativa de Tabla A2: −13.24 a −5.63 pp se explica como reducción al añadir historia individual, no fracción causal aislada; cifras, fila y estructura intactas (`_pages/tesis-post4-anexo-metodologico-en.md:101,111`). Excepción semántica autorizada por el integrador. |
| B5 · validación concluyente, reorganización confirmada y sesgo causal cuantificado | La prueba se llama de composición; el flujo ≥70% es compatible con continuidad administrativa, pendiente de confirmación documental. La mezcla D1/D2 altera la composición, sin establecer dirección ni tamaño de sesgo causal. La lectura de heterogeneidad evita «striking» y G1 se define por efecto condicional predicho (`_pages/tesis-post4-anexo-metodologico-en.md:148-152,157,179,196`). |
| B6 · etiquetas y analogías ELI5 | Retiré «in plain language», automóviles, gemelos, cinturón/tirantes y horno/congelador del anexo IV; también «Put simply» y la analogía de dos películas del anexo III. Los métodos conservan sus supuestos y límites (`_pages/tesis-post4-anexo-metodologico-en.md:29-32,67,73-88,157`; `_pages/tesis-post3-anexo-metodologico-en.md:26,156`). |
| B7 · Table 6 inexistente | Eliminé el párrafo huérfano del artículo III EN; su hecho documental y límite permanecen en el párrafo de la constancia de reubicación y en las notas legales (`_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md:128-132`). |

## Correcciones factuales de paridad

- El corte 2016–2019 se describe como especificado **después del piloto y antes de mirar la serie completa**, sin prerregistro independiente, conforme al contrato de diseño; se corrigen prosa, leyendas y encabezados EN III (`_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md:92,103`; `_pages/tesis-post3-anexo-metodologico-en.md:67,128-138,226-228`).
- El +1.85 pp de no matrícula persistente se llama máximo **entre los cinco regímenes**, no de los años individuales; el máximo anual llega a +4.56 pp (`_pages/tesis-post3-anexo-metodologico-en.md:124`).
- El pipeline compara cohortes con escuelas sin cierres registrados en su universo, luego agrega los contrastes; Callaway, Sun y Roth son marco metodológico, no sello de implementación exacta. Etiqueta A4, alt de figura 1 y prosa EN usan «exposed-weighted» sin atribución incorrecta (`_posts/2026-10-23-costos-cierre-escolar-trayectorias-en.md:76,84`; `_pages/tesis-post3-anexo-metodologico-en.md:99,114,123,166`). La etiqueta de Tabla A4 se ajustó por la misma corrección factual ya realizada en ES, sin cambiar valores ni estructura.
- El anexo IV EN separa la brecha de celdas exactas −14.64 de la muestra modelada distinta −13.24, atribuye las estimaciones PAES/PDT a la muestra completa y aclara que −5.63 (DML PLR), −4.88 (R-Learner) y −6.11 (FWL) son estimadores distintos (`_pages/tesis-post4-anexo-metodologico-en.md:77-82,222-224,285-287`).

## Verificación

- `ruby scripts/verify_thesis_post3.rb --lang en` → exit 0, `POST3_VALID lang=en`; aviso upstream conocido: `UNCOMMITTED_FILE_HASHES`.
- `ruby scripts/verify_thesis_post4.rb --lang en` → exit 0, `THESIS_POST4_VERIFIED lang=en fixture=none`.
- `python scripts/verify_thesis_editorial_delivery.py --check baseline` → exit 0, `EDITORIAL_DELIVERY_VALID check=baseline fixture=none`.
- `git diff --check --` sobre las cuatro rutas EN → exit 0.

HANDOFF-TRACE: Claude Code → Codex integrador → Codex editor EN; B1–B7 resueltos para revisión dirigida congelada, B8 ES III bajo escritor separado.

PLAN_STATE v2: corrección editorial EN ejecutada; revisión independiente dirigida, PDF, QA integral y cierre local pendientes bajo coordinación del integrador.
