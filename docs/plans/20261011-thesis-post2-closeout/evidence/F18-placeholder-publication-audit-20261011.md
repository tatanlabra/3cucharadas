# F18 — auditoría de placeholders y acabado editorial

- Fecha: 2026-10-11.
- Alcance: Post II ES/EN, evidencia congelada, visuales y medida tipográfica.
- Regla: investigar y adjudicar cada placeholder; una deuda no ejecutada se divulga y no se convierte en robustez.

| ID | Adjudicación | Evidencia y efecto editorial |
|---|---|---|
| PH-01 | Cerrado | `audit/post2_stylized_evidence.json`; período, evento y establecimiento-segmento conciliados. |
| PH-02 | Cerrado con riesgo residual | `audit/school_identity_registry_v1.json` y `audit/school_identity_outcome_sensitivity_v1.json`; dos sucesiones candidatas no tocan los 337 cierres del panel, sin afirmar cobertura exhaustiva. |
| PH-03 | Cerrado por resultado negativo | `audit/slep_identification_v2.json` y `audit/slep_discovery_v3.json`; diseño causal rechazado y atribución causal retirada. |
| PH-04 | Cerrado | `audit/article_school_market_event_support.json`; denominadores separados, sin sumar universos distintos. |
| PH-05 | Cerrado con límite | `reports/253_article_selection_support.md`, `reports/255_article_selection_support_strata.md` y `reports/257_article_selection_positivity.md`; soporte desigual y sin generalización poblacional. |
| PH-06 | Cerrado como deuda visible | `audit/article_school_market_renewal_estimation.json`, DEV-MR-003; 5/10/20 no fue ejecutado, por lo que el post retira la pretensión de robustez del umbral 10. |
| PH-07 | Cerrado | `audit/scientific_release_freeze.json`; `NOT_ESTIMABLE` no se interpreta como cero ni empate. |
| PH-08 | Cerrado | `audit/article_school_market_renewal_estimation.json`; signos e intervalos MR3 reconciliados. |
| PH-09 | Cerrado para el blog | `audit/article_r007_openalex_chain.json`; la revisión no es exhaustiva y el claim de novedad se retiró. R-007 sigue abierto solo para el artículo. |
| PH-10 | Cerrado | `research/article_post2/slep_transfer_schedule.yaml`, Ley 21.040 y calendario DEP; traspasos fechados y sin atribución retroactiva. |
| PH-11 | Cerrado | `audit/school_coordinate_osm_audit_v1.json`; auditoría agregada con atribución OSM y sin redistribuir microdatos combinados. |
| PH-12 | Cerrado con límite | `audit/post2_stylized_evidence.json`; ventanas, 259 coordenadas tardías, 9 trayectorias excluidas y regla de selección visibles. |
| PH-13 | Cerrado | `assets/data/thesis-extension-post2/cases.json`; nombres, roles, años y distancias conciliados. |
| PH-14 | Cerrado con límite | `research/article_post2/el_salvador_author_case.yaml`; fusión y traslado de cursos documentados; motivo y destinos individuales retirados. |
| PH-15 | Cerrado | `audit/post2_stylized_evidence.json`; proyección INE 6–17, base 2024, sin traducirla en matrícula o cierres. |
| PH-16 | Revisado y excluido | Post III conserva contrato propio futuro; no se anticipan cierres ni escenarios desde Post II. |
| PH-17 | Cerrado para el claim publicado | `audit/scientific_release_freeze.json`; 999 réplicas, 112 celdas y residual reproducibles; las sensibilidades no ejecutadas quedan enumeradas y no sostienen el veredicto. |
| PH-18 | Cerrado por decisión humana | Declaraciones ES/EN de financiamiento, afiliación e IA incorporadas literalmente con paridad. |

## Correcciones de publicación

- Se separó la procedencia de figuras: demografía usa INE base 2024; trayectorias y mapas usan sus fuentes MINEDUC correspondientes.
- La columna narrativa se limita a `72ch` desde `64em`; mapas, tablas, figuras y nota técnica conservan el ancho ampliado.
- El panel lateral del mapa gana ancho, la selección ocupa dos columnas y se evita la partición artificial de encabezados.
- El canario `prose-measure` produjo `EXPECTED_FAIL` con exit 1 antes del gate verde.

## Frontera

- No se completaron artificialmente las sensibilidades 5/10/20, IPW, bounds, washouts alternativos ni la revisión exhaustiva R-007.
- Esas ausencias impiden claims de robustez exhaustiva, causalidad y novedad; no impiden el relato descriptivo acotado.
- No hubo commit, push, despliegue ni difusión en F18.
