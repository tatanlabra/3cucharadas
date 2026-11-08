# Paridad editorial EN III–IV

PLAN_STATE v2: `pb-20261108T003705315Z-fc127547` — P0/P1 activos; P2–P4 pendientes del integrador.
HANDOFF-TRACE: Codex integrador → adaptador EN vía collaboration; fuentes ES aprobadas → cuatro fuentes EN bajo ownership exclusivo → integrador y editorial crítica.

## Alcance y correcciones

| Fuente EN | Corrección frente a ES aprobado | Límite preservado |
|---|---|---|
| `_pages/tesis-post3-anexo-metodologico-en.md` | La distribución histórica usa 89,7 % de 1.141 cierres y 86,7 % de 78.972 observaciones. La permanencia desde G−2 usa 70,58 % de las 6.581 observaciones expuestas descriptivas; las muestras estimables, distintas, son 3.556 estables y 1.033 entrantes tardíos. | No se convierte una proporción descriptiva en denominador de la muestra estimable ni en fracción causal atribuible a permanecer. |
| `_pages/tesis-post4-anexo-metodologico-en.md` | Se restituyeron la reducción de 1,42 puntos, los subgrupos de 29.683 y 8.842 alumnos con sus estimaciones/errores, el perfil CLAN G1 reestimado completo y el benchmark 0,915 %. Se quitaron dos números de una analogía inglesa ajena al ES y la etiqueta legal “DS No. 315” que no corresponde al pasaje homólogo. | Quintiles reestimados tienen distinta composición; el JSON público no identifica transiciones de individuos. Errores de subgrupos no prueban igualdad; benchmark observado no descarta toda confusión omitida. |
| Ambos posts EN | Cotejados junto con sus anexos en el corpus canónico ES/EN; no requirieron cambios nuevos en esta ronda de paridad. | Se conservan cifras, intervalos, comparaciones y restricciones inferenciales del ES aprobado. |

## Verificación observada

| Comando | Resultado |
|---|---|
| `ruby scripts/verify_thesis_post3.rb` | Exit 0: `POST3_VALID lang=both`; advertencia histórica `UNCOMMITTED_FILE_HASHES`. |
| `ruby scripts/verify_thesis_post4.rb` | Exit 0: `THESIS_POST4_VERIFIED lang=both fixture=none`. |
| `git diff --check` | Exit 0. |
| `ruby scripts/verify_difusion_coherente.rb --all-declared --root .` | Exit 0 tras la corrección separada de tres piezas de difusión III por editorial crítica: `PASS: coherencia numérica; 9 ref(s) explícitas`. Cobertura III: 280 cifras; IV: 425 cifras, en corpus post+anexo ES/EN. |

El gate de difusión comprueba coherencia numérica; la revisión humana de esas piezas sigue pendiente. Desde este ownership no se alteraron fuentes ES, datos, verificadores ni piezas de difusión. Fuentes EN congeladas para build y revisión del integrador; sin commit ni push desde este ownership.
