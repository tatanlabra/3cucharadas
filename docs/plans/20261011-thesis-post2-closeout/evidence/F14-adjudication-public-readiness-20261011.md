# F14 — adjudicación R3 y preparación para revisión pública

- Fecha: `2026-10-11`.
- Alcance: hallazgos H-01 a H-13 de la R3 independiente de Claude, sobre Post II ES/EN y sus anexos.
- Veredicto del integrador: `READY_FOR_HUMAN_REVIEW`, no equivale a aprobación para publicar ni garantiza recepción pública.

| Hallazgo | Adjudicación | Evidencia o cambio |
|---|---|---|
| H-01 | Corregido | El denominador queda particionado como 12.116 filas oficiales: 12.038 funcionando y 78 autorizadas sin matrícula; 6.601 con y 5.515 sin candidato OSM. |
| H-02 | Corregido | Freeze científico revisión 6 y commits `e6a0bb7` y `38a31d7`: MR1 cruza cero y MR3 conserva signos e intervalos oficiales. |
| H-03 | Corregido | `PLAN_STATE` reconcilia PH-02/03/05/06/08/10/12/13, E-37 y D-15; el H1 real se observó rojo por hash obsoleto antes de actualizar el contrato. |
| H-04 | Corregido | El mapa interactivo limita trayectorias visibles a matrícula y transición inicial; el navegador prohíbe anécdotas escolares de SIMCE/admisión. |
| H-05 | Corregido en el alcance público | La prosa compara escuelas comparables y separa la mediana nacional amplia; no presenta como ejecutada una sensibilidad que aún no existe. |
| H-06 | Corregido | Entrada se define operacionalmente por matrícula positiva tras dos años claros, sin actividad previa observada ni sucesión; se declara el truncamiento temporal. |
| H-07 | Corregido | Se incorpora Grau, Hojman y Mizala (2018) como evidencia causal de resultados adversos, sin mezclar unidad, periodo ni diseño con los descriptivos del post. |
| H-08 | Corregido | Carruseles y tablas rotulan celdas descriptivas e IC95; `N` no se presenta como soporte inferencial exacto. |
| H-09 | Corregido | El anexo comparte permalink fuente y Polyglot genera `/datos/...` y `/en/datos/...`; build limpio eliminó la ruta EN duplicada anterior y H1 validó `hreflang`. |
| H-10 | Corregido | Hashes, freeze, suites, build, artefacto y matriz se recalculan sobre el snapshot final antes del commit. |
| H-11 | Corregido | Seis pares candidatos corresponden a cuatro cierres; no existe un par secundario elegible bajo la regla declarada. |
| H-12 | Corregido | Se definen DE, IC95, puntos porcentuales, regla schumpeteriana conjunta y umbrales exploratorios de concentración. |
| H-13 | Parcial no bloqueante | Se corrigieron nombres y rutas; el basemap remoto conserva fallback estático. La exposición tailnet requiere aceptación específica del riesgo antes de Telegram. |

## Juicio de optimalidad factible

- Restricciones duras: paridad ES/EN, trazabilidad, no causalidad, privacidad agregada, identidad Jekyll, rutas, accesibilidad y artefacto deben quedar verdes.
- Ideal sin restricciones: causalidad identificada, métricas reales de lectura y bundle cartográfico pequeño; no es alcanzable con la evidencia y el momento prepublicación actuales.
- Óptimo factible: paquete bilingüe listo para revisión humana local, con límites visibles, canarios observados en rojo y rollback por commit; no es todavía una publicación aprobada.
- Evidencia favorable: fuentes y anexos verdes, build de producción limpio, rutas canónicas, matriz visual y accesibilidad repetidas sobre el artefacto final.
- Evidencia contraria: 3.283 palabras ES y 3.235 EN superan la meta blanda; JS principal 985,42 kB y worker 477,73 kB sin comprimir; el mapa depende de teselas remotas antes del fallback.

## Hipótesis residuales y falsación

| Hipótesis abductiva | Evidencia discriminante | Condición de descarte |
|---|---|---|
| La extensión puede reducir lectura completa pese a aportar confianza. | Profundidad de scroll, tiempo activo y retroalimentación después de publicar. | No hay deterioro frente a posts comparables o lectores reportan que la trazabilidad compensa la longitud. |
| El bundle puede penalizar móviles lentos pese a carga diferida y fallback. | RUM móvil: LCP, interacción y tasa de fallback por red. | Percentiles móviles permanecen dentro de la meta del sitio y el fallback es excepcional. |
| El ajuste por tamaño podría ocultar parte de la diferencia MR1. | Sensibilidad preregistrada sin el control de tamaño. | La estimación permanece cercana a cero y su intervalo sigue cruzándolo. |

## Límite de la conclusión

- `READY_FOR_HUMAN_REVIEW` significa que no queda un defecto duro observado dentro del alcance local.
- El éxito público solo puede evaluarse con datos posteriores de recepción; no se infiere de gates, commits ni acuerdo entre agentes.

## Validación final

| Superficie | Resultado |
|---|---|
| Semántica, anexo, source y H1 | `exit 0`; el canario MR, hash y anécdota académica terminaron `EXPECTED_FAIL` con salida no cero. |
| TypeScript/Vitest/Vite | 136/136 pruebas, typecheck y build del mapa `exit 0`; permanece la advertencia de chunk mayor a 500 kB. |
| Jekyll y artefacto | Build de producción `exit 0`; 70.875.136 bytes y 1.512 entradas. |
| Matriz visual final | 24/24 páginas, 12/12 SVG y 2/2 fallbacks; 0 fallos después de aislar la inicialización del mapa de fuentes e imágenes previas. |
| Axe 4.12.1 | ES y EN: 37 reglas aprobadas, 0 violaciones y 0 inconclusos en `.page__content`. |
