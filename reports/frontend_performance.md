# Presupuesto de frontend

Build local validado el 2026-07-18 con Node 24.18.0, Vite 7.0.0, MapLibre GL JS 5.6.0
y PMTiles 3.2.0.

| Recurso | Transferencia gzip | Cuándo carga |
| --- | ---: | --- |
| Entrada Vite y estilo local | 1,01 KB JS + 0,27 KB CSS | Al visitar la página. |
| App MapLibre/PMTiles | 267,49 KB JS + 9,97 KB CSS | Sólo cuando el visor entra a 320 px del viewport. |
| Capa comunal PMTiles | No disponible aún | Al iniciar el mapa, después de publicar manifest y R2. |
| PMTiles predial Atacama | No disponible aún | Sólo tras región/comuna piloto y activación explícita. |

El chunk cartográfico supera el aviso de 500 KB sin comprimir de Vite, pero está
separado de la entrada inicial y no se solicita antes de acercarse al mapa. El
presupuesto de datos no se declara aprobado hasta medir teselas reales en el piloto.
