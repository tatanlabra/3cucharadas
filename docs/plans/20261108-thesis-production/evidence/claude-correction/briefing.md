# Revisión adversarial: corrección integral III–IV

Estado documental: LISTO PARA REVISIÓN. Fuentes congeladas y vinculadas en inputs-before.json; timestamp 2026-11-08T01:59:00Z.
Origen: Codex integrador. Destino: Claude Code, modelo sonnet según routing canónico. Vía: claude-bridge CLI, review de solo lectura.
PLAN_STATE v2: pb-20261108T003705315Z-fc127547 rev14; P1/D7/D8/D10 verificados localmente, P4 activo, D9 activo para revisión y nueva publicación. P0/P2/P3 acreditan entrega anterior 1959f659, no aprueban corrección nueva.
HANDOFF-TRACE: Codex → Claude Code vía claude-bridge CLI; revisión adversarial sonnet.

## Decisiones humanas vinculantes
- Restaurar párrafos justificados en posts y anexos III/IV ES/EN.
- Corregir figura 1 IV estrecha y textos que cruzan barras; todas las figuras deben resultar legibles.
- Detectar errores geométricos tanto en generación como en Playwright, con negativos reales.
- Panorama longitudinal 2009–2022 visible desde inicio; 2016–2019 identificado como subventana, sin extrapolar modelos.
- Revisar adversarialmente TODO el conjunto antes de push inmediato autorizado. Difusión permanece pendiente.
- Preservar identidad, cifras, CSV/JSON científicos, intervalos y límites inferenciales.

## Contexto y alcance de revisión
El verde anterior midió contraste CSS y tamaño, no cruces texto/texto o texto/marcas. El usuario detectó una omisión real. No aceptar contraste o salida0 como sustituto de legibilidad. El CSS limitaba figura1 a620px aunque contenido permite732–796px en escritorio. Diseño interno también requiere reparación. Revisión ES previa r4/r5 fue APPROVE, pero nuevos cambios invalidan su frescura; se conserva como histórica.

Lee fuentes completas en /home/ende/Descargas/programaciones/activos/3cucharadas:
- _posts/2026-10-23-costos-cierre-escolar-trayectorias.md y -en.md
- _posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md y -en.md
- _pages/tesis-post3-anexo-metodologico.md y -en.md
- _pages/tesis-post4-anexo-metodologico.md y -en.md
- assets/css/main.scss y scripts/verify_thesis_series_browser.mjs, scripts/verify_thesis_visual_quality.mjs, scripts/verify_draft_promotion.rb (cambios acotados identificados al congelar).
Generador en /home/ende/Descargas/programaciones/incubadora/tesis_mae_mejorada/scripts/352_post4_visuals.py; sus pruebas y figuras SVG/PNG/CSV/manifiesto.

## Qué exigir
1. Relato adulto claro, motivación y método crítico explícitos, hallazgo con límite, recapitulación y desafíos. Chicago-Deusto/CMOS como guía; no inventar que exige decisiones del blog.
2. Serie2009–2022 y subventana2016–2019 distinguidas; ninguna inferencia nueva no sustentada. Comparaciones de grupos/estimadores no se convierten en cambios de las mismas personas.
3. Justificación DOM real; tablas, leyendas y listas conservan legibilidad.
4. Figuras: leer capturas reales y SVG, comprobar que etiquetas/intervalos no chocan, no quedan fuera y no se comprimen. Distinguir etiquetas intencionales dentro de barras de cruces accidentales. No aprobar por consenso de agentes.
5. Guard de generación y Playwright: verificar cobertura, casos negativos, falso verde/falso rojo y límites del detector. Rechazar criterios decorativos, colecciones vacías, umbral ajustado para aprobar o errores ocultos.
6. Preservación de datos, paridad ES/EN, referencias, PDF regenerado, recursos locales y públicos. Estado de deploy final aún pendiente; no exigirlo antes de review.

## Salida requerida
- `REVIEW_VERDICT: APPROVE` o `REVIEW_VERDICT: REQUEST_CHANGES` inequívoco.
- Hallazgos `[SEV] archivo:línea → problema → corrección (evidencia)`.
- Separar observación, inferencia y límites no verificados. No afirmar haber ejecutado Playwright si solo leíste recibos/capturas.
- Incluir `PLAN_STATE v2`, `HANDOFF-TRACE:` y `MODEL-REPORT:` al cierre. Solo lectura; sin editar, commit, push ni difusión.

## Hallazgo discriminante que debe revisar
Primera matriz geométrica: 48/64 PASS y 16 vistas de anexos rojas por colisiones reales entre valores y barras vecinas de la misma categoría. El generador tenía una excepción demasiado amplia (`for other in range(2/3)`) que ocultaba estas colisiones. La corrección debe restringir excepciones a la barra propia y rediseñar ubicación de valores. Inspecciona las excepciones y las falsaciones de colisión contra barra VECINA de la MISMA categoría. No aceptar relajar el detector como arreglo. Recibo rojo preservado en `evidence/figure-correction/visual-local.json`.

## Límites que debe contrastar
El detector Playwright compara textos con IDs QA contra todos los demás textos SVG y las marcas CI/punto/barra asignadas. No compara pares sin rol (título/tick/leyenda entre sí), trazos no etiquetados ni semántica. Capturas reales y el guard del generador complementan esa cobertura; no permiten afirmar inspección exhaustiva de cada píxel. La comparación de contraste SVG usa canvas raíz; verificar visualmente fondos locales.

Segunda corrida, aún rechazada: `visual-local-corrected.json` conserva 16 fallos de contraste causados por `+4,3`/`+4.3` blanco sobre barra propia demasiado estrecha. Root lo identificó visualmente y el check de contraste lo rechazó (1:1 contra canvas). Ver `diagnostic-paes-clipped-label.png` y `diagnostic.md`. La corrección final coloca valores fuera de todas las barras y elimina también la excepción de barra propia. Revisar el cuarto fixture `svg-own-bar-overlap` además de los tres anteriores.

Tercer hallazgo visual antes de congelar: etiqueta ámbar −11,5 en G1 atravesada por la línea cian del panel GATE. El detector anterior no incluía segmentos GATE. Exigir corrección de posición, comprobación de trayectorias reales (no solo rectángulo envolvente de toda la polilínea) y falsación específica. Auditar legibilidad de las tres familias y cobertura declarada frente a esta evidencia.

## Evidencia final y comandos de comprobación
Todo lo siguiente relativo al blog, salvo indicación absoluta:
- Snapshot de 74 archivos: `docs/plans/20261108-thesis-production/evidence/claude-correction/inputs-before.json`; comprueba hashes si detectas cambios.
- QA final: `docs/plans/20261108-thesis-production/evidence/figure-correction/visual-local-final.json` (64/64 PASS; contraste texto5,73, SVG4,67; mínimo SVG10,28px en conjunto; Fig1móvil12,50px).
- Cinco negativos reales: `fixture-svg-value-overlap.json`, `fixture-svg-longitudinal-overlap.json`, `fixture-svg-causal-overlap.json`, `fixture-svg-own-bar-overlap.json`, `fixture-svg-gate-line-overlap.json` dentro del mismo directorio. Baseline limpio y mutante rechazado exit1.
- Capturas de las tres familias: ocho PNG en `docs/plans/20261108-thesis-production/evidence/figure-correction/curated/`. ABRIR las imágenes, especialmente causal EN claro320 y ES oscuro1440. Observación visual aún a juzgar: −12,3 y −11,5 en G1 cercanos en móvil aunque no se intersectan; evalúa si la asociación/lectura es clara o requiere ajuste.
- PDF final local: `/home/ende/Descargas/programaciones/incubadora/tesis_mae_mejorada/outputs/post4_delivery/post4_borrador_educacion_superior_causal_ml.pdf`; 23 páginas,3 figuras,6 tablas, SHA b4e6df4ed77f2d222bb465936a8f265c5c0a626f88aac1f18b5620b041cf8b51. Figura1 en página5,ancho14,02cm. Raster de página5 `docs/plans/20261108-thesis-production/evidence/figure-correction/pdf-figure1-final.png`.
- Funcional `post3-browser-*` y `post4-browser-*`:64/64, justificación completa, Fig1ratio1, noJS8/8,print8/8. Su manifiesto IV corresponde a primera corrección geométrica, por lo que la matriz visual final es quien vincula las últimas figuras; fuentes/CSS funcionales iguales. No afirmar binding funcional de los últimos SVG a partir de ese recibo anterior.
- Fuente/reference/build final pasan; `source-final.json`, `build-final.log`. Linksrenderizados8rutas/494enlaces.
- Generador: `PYTHONDONTWRITEBYTECODE=1 /opt/entornos/mamba312/bin/python /home/ende/Descargas/programaciones/incubadora/tesis_mae_mejorada/tests/verify_post4_visual_geometry.py`;24rendersenmemoria. Mutantes flags`--inject-selection-overlap`, `--inject-longitudinal-overlap`, `--inject-causal-overlap`, `--inject-causal-gate-overlap` salen1soloerror específico;setup3/superviviente2.
- `python3 scripts/verify_thesis_editorial_delivery.py --check baseline` y `--check pdf` pasan. `--check review` aún apunta a revisión histórica y debe fallar stale hasta registrar tu respuesta aprobatoria; no es hallazgo del producto.

Tu tarea es revisar TODO el conjunto (o declarar inequívocamente alcance no revisado), no solo los últimos SVG. No editar ni publicar. No llamar a subagentes de edición. Si puedes completar con estas fuentes y capturas, evita nuevas rondas redundantes. Devuelve un veredicto argumentado con bloqueos concretos y riesgos residuales.
