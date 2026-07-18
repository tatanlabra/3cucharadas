# Plan de integración ejecutable

## Objetivo y criterio de éxito

Entregar un visor Vite/TypeScript aislado que preserve la página existente, cargue una
capa comunal PMTiles al iniciar y cargue a demanda sólo el PMTiles regional de Atacama
después de seleccionar Caldera o Diego de Almagro. Éxito significa: build reproducible,
URL compartible, métricas preservadas, atributos sensibles bloqueados, cero descarga
predial inicial y ningún upload mientras el gate legal esté pendiente.

## Implementación incremental

1. Añadir Vite, TypeScript, MapLibre y PMTiles con versiones fijas; la página actual
   consume el bundle mediante manifest, sin introducir JavaScript global del tema.
2. Crear un manifest público versionado y catálogo de regiones/comunas compatible con
   los datos actuales. Si falta el PMTiles nacional, el visor conserva el fallback de
   celdas y comunica el estado.
3. Montar MapLibre de forma diferida, con protocolo PMTiles y un estilo base que apunta
   a un PMTiles Protomaps/OSM autoalojado. No se consulta OSM público.
4. Habilitar el piloto Atacama únicamente tras región/comuna válida. El source predial
   se elimina al cambiar de región y se filtra por comuna al seleccionarla.
5. Preparar scripts remotos reproducibles: inventario, extracto público, validación,
   Tippecanoe, validación PMTiles, presupuesto de teselas, upload R2 y rollback.
6. Ejecutar tests unitarios, build Vite, build Jekyll y smoke browser. La promoción y
   el upload quedan explícitamente fuera hasta contar con autorización legal, R2 y
   toolchain en `stata01`.

## Supuestos y riesgos

- El mapa base y los PMTiles se servirán finalmente desde `tiles.3cucharadas.cl`;
  hasta entonces se usa un manifest de staging sin activar la capa predial.
- Los límites comunales deben provenir de una fuente pública autorizada. No se derivan
  de los polígonos prediales SII.
- No se generalizará a otras regiones con artefactos prediales hasta que Atacama pase
  controles funcionales, cartográficos y de p95 de teselas.

## Reversión

La página anterior se puede recuperar con `git revert` del commit de integración. Los
PMTiles se versionan por fecha y el manifest puede volver a la versión anterior sin
modificar la fuente maestra.
