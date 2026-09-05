# Auditoría crítica — paquete de difusión Nushell

Fecha: 2026-09-05
Objeto: adaptaciones de `devto.md`, `medium.md`, `hn.txt`, `reddit-target.md`, `linkedin.md`, `social-corto.md` y carrusel LinkedIn.

## Tesis y decisión

- Tesis: Nushell merece una ruta selectiva cuando coinciden datos estructurados, varias transformaciones y riesgo concreto de fallo silencioso; la evidencia no sostiene una superioridad general.
- Decisión: aprobar el paquete para revisión humana por canal, no para publicación automática.
- Audiencia: profesionales de agentes de código, herramientas de línea de comandos y reproducibilidad.

## Inventario epistémico

| Clase | Cantidad | Alcance |
|---|---:|---|
| HECHO | 16 | Diseño, resultados, costes, activaciones, fallos observados, entorno y caso agregado; contrastados con el post canónico. |
| INFERENCIA | 2 | Regla de enrutamiento retenida y clasificación del envío de Hacker News como normal. |
| ESPECULACIÓN | 0 | — |
| NO VERIFICADO | 3 | Reglas actuales de r/nushell, render final dentro de plataformas y elegibilidad de cuentas. |

## Hallazgos

| Severidad | Hallazgo | Resolución |
|---|---|---|
| Media | Las repeticiones no son familias independientes y parte del corpus fue usada durante el ajuste. | El límite aparece en las piezas largas y se evita presentar una tasa generalizable. |
| Media | El PDF de LinkedIn es rasterizado y no etiquetado. | Se declara el límite y se exige texto alternativo general; queda pendiente una variante con capa de texto si se requiere accesibilidad interna. |
| Media | Las reglas de r/nushell no pudieron verificarse porque la consulta pública respondió 403. | Reddit permanece bloqueado hasta revisión humana de las reglas visibles. |
| Baja | `devto.md` incluía un ejemplo con cifras de filas que no procedían del texto canónico vigente. | Se eliminó el ejemplo numérico y se conservó solo la descripción del contrato JSON. |

## Sesgos y conflicto de interés

- Confirmación y selección: el diseño inicial favorecía encontrar valor en la skill; el microbenchmark adverso, el holdout y el caso de indiferencia actúan como contraevidencia.
- Publicación: se preservan resultados negativos y costes, no solo los aciertos favorables.
- Automatización: ningún borrador ni validación local se trata como evidencia de publicación o render final en plataforma.
- Conflicto reputacional: el mismo proyecto implementó la skill y produjo las mediciones; las piezas largas lo declaran.

## Contraargumento más fuerte

- El estudio puede estar midiendo una política y sus errores de integración en una sola máquina, con pocas familias, más que una ventaja propia de Nushell.
- La conclusión se restringe por ello a una regla operacional falsable; no se atribuye causalidad general a la shell.

## Veredicto

- Aprobado con observaciones para revisión humana por canal.
- Riesgo residual: medio antes de la carga en cada plataforma; bajo para la coherencia factual del paquete local.
- Bloqueos: Reddit sin reglas verificadas y cualquier envío externo sin autorización explícita.
