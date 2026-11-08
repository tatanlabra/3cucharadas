# Respuesta editorial ES al dictamen Claude r4

Estado: `APPROVE` de Claude r4 recibido; corregidos sus tres hallazgos menores y dos opcionales antes de la adaptación EN. Los cuatro archivos ES quedan congelados para revisión dirigida del delta. No se modificaron CSV ni JSON científicos. Dictamen original: `evidence/claude/result-r4.md`.

| Hallazgo r4 | Resolución y evidencia |
|---|---|
| Menor 1 · pruebas de III presentadas como pendientes | **Aceptado.** El encabezado y el párrafo del anexo IV aclaran que ambas sensibilidades ya se reportaron en el artículo y anexo III; la Tabla A1 las reúne por conveniencia, sin atribuirles nueva evidencia (`_pages/tesis-post4-anexo-metodologico.md:23-25,34-46`). |
| Menor 2 · «próxima entrega» | **Aceptado.** La prueba de trayectorias individuales queda pendiente como desafío 1 del artículo IV, que cierra la serie (`_pages/tesis-post4-anexo-metodologico.md:217`; `_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md:123-129`). |
| Menor 3 · subgrupo selectivo no estimado | **Aceptado.** El texto atribuye las estimaciones de rendición, selectividad y postulación a la muestra completa de la Tabla A5, sin inferir resultados para aspirantes con buenas notas (`_pages/tesis-post4-anexo-metodologico.md:205-215`). El +1,75 pp incluye cero y el +4,30 pp de postulación sigue como anomalía explicativa, no resiliencia demostrada. |
| Opcional 1 · orden de referencias | **Integrado.** `chernozhukov2018` precede a `cinellihazlett2020` en orden por clave, sin alterar definiciones (`_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md:143-145`). |
| Opcional 2 · tres valores de «mochila estudiantil» | **Integrado.** Se identifican DML PLR (−5,63 pp), R-Learner (−4,88 pp) y proyección FWL (−6,11 pp) como estimadores distintos con usos distintos; no se presentan como coeficiente único (`_pages/tesis-post4-anexo-metodologico.md:96,277-279,286`). |

## Verificación

- `ruby scripts/verify_thesis_post3.rb --lang es` → exit 0, `POST3_VALID lang=es`; persiste advertencia de custodia upstream `UNCOMMITTED_FILE_HASHES`.
- `ruby scripts/verify_thesis_post4.rb --lang es` → exit 0, `THESIS_POST4_VERIFIED lang=es fixture=none`.
- `python scripts/verify_thesis_editorial_delivery.py --check baseline` → exit 0, `EDITORIAL_DELIVERY_VALID check=baseline fixture=none`.
- `git diff --check --` sobre los cuatro ES → exit 0.
- Conteo visible anterior a `## Referencias`, conservando leyendas de figuras y retirando etiquetas HTML/Jekyll: III **2.572** palabras; IV **2.887** palabras. Los cuerpos, preámbulos y cierres de los artículos no cambiaron con este delta, salvo el orden bibliográfico.

HANDOFF-TRACE: Claude r4 → Codex editor ES vía Codex integrador; respuesta y cuatro archivos ES congelados → Codex integrador para revisión dirigida.

PLAN_STATE v2: F1 ES corregido y congelado; F2 dictamen `APPROVE` r4 con cinco observaciones resueltas; EN, PDF, QA integral y cierre local pendientes bajo coordinación del integrador.
