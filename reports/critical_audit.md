# Auditoría crítica de cierre

Audiencia: mantenedor/a que decide si construir, alojar o promover el piloto.

## Claims revisados

| Clasificación | Cantidad | Resultado |
| --- | ---: | --- |
| HECHO | 8 | Diagnóstico de repo, fuentes piloto, build local, tests y estado remoto comprobados en esta ejecución. |
| INFERENCIA | 3 | La DPA 2023 permite el cruce comunal; el estilo Protomaps será compatible con el extracto elegido; el piloto quedará dentro de presupuesto. |
| NO VERIFICADO | 4 | Autorización vectorial SII, instalación/fuentes en stata01, R2/CORS/Range y tamaño p95 de teselas. |
| ESPECULACIÓN | 0 | No se promueve ninguna afirmación de desempeño o disponibilidad sin medición. |

## Hallazgos

1. **Alta — promoción predial bloqueada.** No hay autorización vectorial explícita.
   El gate `LEGAL_PUBLICATION_STATUS=PENDING` y los scripts abortan publicación/upload;
   mantenerlo así hasta una revisión humana documentada.
2. **Alta — infraestructura remota ausente.** `stata01` respondió sin el proyecto ni
   Tippecanoe/PMTiles/GDAL, y no se encontró la fuente allí. No presentar los scripts
   como un procesamiento ejecutado: son un runbook reproducible pendiente.
3. **Media — DPA y basemap por verificar.** La DPA 2023 es una fuente institucional
   candidata, pero el archivo concreto, hash, licencia operativa y cruce de códigos aún
   no se descargaron. El estilo debe probarse contra el esquema de capas del PMTiles
   Protomaps seleccionado antes de producción.
4. **Media — rendimiento sin evidencia predial.** El bundle cartográfico carga de modo
   diferido (267,49 KB gzip), pero no hay p95 de teselas, memoria móvil ni Range real.
5. **Baja — sesgo de automatización/publicación.** Que la capa tenga pocos atributos
   no convierte el polígono en inocuo ni autorizado. La advertencia de cartografía
   referencial y la revisión legal siguen siendo necesarias.

## Conflictos y límites

No se observaron credenciales, claves R2 ni atributos prediales sensibles en el
artefacto web. Esta auditoría no reemplaza autorización de SII, una evaluación jurídica
ni pruebas con un bucket R2 real.

## Veredicto

**Aprobado con observaciones para integración y staging sin vectores prediales.**
**No aprobado para publicar PMTiles SII** hasta resolver los cuatro ítems `NO VERIFICADO`
y documentar la evidencia en los reportes de tiles y de publicación.
