# Entrega editorial III–IV — cierre local

Estado: **COMPLETE local**. Ejecución integral: seis criterios aprobados, cero fallos y cero omisiones. Recibo: [integral-closure.json](evidence/integral-closure.json).

## Resultado editorial

- Dos artículos y dos anexos por idioma: ocho páginas ES/EN. Los artículos presentan motivación, hallazgo, comparación y límite al inicio; tres cucharadas; recapitulación y tres desafíos verificables al cierre.
- III ES: 2.572 palabras editoriales; IV ES: 2.887. III EN: 2.707; IV EN: 2.904. Con el contador reproducible de los gates, el cuerpo ES se reduce 57,8 % y 68,3 %, respectivamente; el detalle conservado pasa a anexos independientes.
- Sin etiquetas ELI5. Navegación de las cuatro entregas, TOC, tablas desplazables, variantes móviles y claro/oscuro; prosa con alineación natural acotada a III/IV.
- Hero IV nuevo con cinco variantes y procedencia; 48 variantes de figuras IV regeneradas. Los ocho CSV conservan sus hashes iniciales.
- PDF IV compuesto desde artículo y anexo: 22 páginas, tres figuras y seis tablas. [Manifiesto](../../../../../incubadora/tesis_mae_mejorada/outputs/post4_delivery/post4_borrador_educacion_superior_causal_ml.manifest.json).

## Revisión y correcciones

Claude Sonnet 5.5 revisó ES independientemente: REQUEST_CHANGES inicial; APPROVE completo r4 y confirmación dirigida r5 después de ajustes menores. Las respuestas originales y el transporte están en `evidence/claude/`; `decision.json` vincula las fuentes aprobadas. EN se adaptó después de esa aprobación.

Se corrigieron especialmente la diferencia entre tasa y estimación, el carácter descriptivo de receptoras, la incertidumbre reciente por faltantes, los quintiles G1 recalculados y la diferencia entre contracción IP/CFT y pérdida neta. No se reestimaron modelos.

La comprobación de navegador rechazó inicialmente una leyenda inglesa que omitía el límite jurídico D1/D2; la inspección manual detectó además un texto alternativo que afirmaba efecto nulo. Se cotejaron siete pares de descripciones/leyendas con ES y se corrigieron cuatro campos. El fallo original está preservado en `evidence/browser-post4-before-en-caption-fix.json`.

## Evidencia de aceptación

La ejecución final aprobó 64 combinaciones de ocho páginas, cuatro tamaños y dos temas, más lectura sin JavaScript e impresión; los 494 enlaces locales resuelven. La evidencia final de cada criterio y su caso negativo está en `evidence/contract/`. Los ensayos previos al último ajuste EN se conservan en `evidence/contract-pre-en-caption-fix/` y no sustituyen la aceptación final.

- Build de producción: `evidence/build-final.log`.
- Identidad de artículos y ocho CSV: `evidence/baseline.json` y criterio AC-F0.
- Revisión ES vigente: AC-F2 y `evidence/claude/decision.json`.
- PDF y tres imágenes embebidas: `evidence/pdf-delivery.json`; caso negativo adicional de imagen obsoleta en `evidence/pdf-image-probes.json`.
- Casos reales de anexo ausente y desbordamiento: `evidence/site-technical-final.json` (ejecución ES anterior al último ajuste EN, preservada) y AC-F4-red (build final).
- Casos de citas ausentes, HTML huérfano, deriva científica y paridad: suites Ruby III 3 pruebas/393 aserciones; IV 3/61. Fixtures de navegador III 2/58 e IV 2/30.
- Renderizador PDF: 11 pruebas, Ruff, qpdf, pdfinfo y pypdf aprobados.

## Límites de la entrega

- Local, sin commit, push, publicación ni envío. HEAD del blog permanece `a97b1c8fd37e41e9349dbfd5b0c6e988a053c9a4`; tesis, `4d91f3cc40c59ac7e10def1881d8da1a74a541bc`.
- Post III conserva la advertencia `UNCOMMITTED_FILE_HASHES`: el gate acredita correspondencia con archivos locales, no una nueva custodia científica mediante commit upstream.
- Las ecuaciones del PDF usan notación Unicode lineal; no son ecuaciones OfficeMath nativas. La versión web conserva su notación matemática.
- La corrección editorial sigue Chicago-Deusto/CMOS y las excepciones documentadas del blog; no certifica cumplimiento exhaustivo del manual ni identificación causal.
- El preview local en `http://127.0.0.1:4004/` no representa el sitio público.

## Tablero y equipo

Plan `pb-20261107T230204755Z-19e1bf67`: ventana Kitty independiente, visibilidad confirmada por el usuario. Se eliminó `NO_COLOR=1` heredado para habilitar colores y énfasis. El estado persistido se exporta a `evidence/plan-state.yaml`.

Trabajo dividido entre editor ES, adaptador EN, implementador de sitio y productor de figuras/PDF; máximo tres trabajadores simultáneos. Codex integró y verificó; Claude realizó la revisión adversarial ES mediante el puente canónico.

HANDOFF-TRACE: Codex integrador y agentes de implementación → usuario; entrega local para lectura y revisión, sin acciones externas.

## Tabla de cierre

| Estado | Detalle |
|---|---|
| Implementado | Plan editorial completo, verificación integral 6/6 y tablero cerrado con evidencia. |
| Parcial | — |
| No implementado | — dentro del alcance local autorizado; publicación y envío no forman parte de esta entrega. |
