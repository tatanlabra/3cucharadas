# Avalúos II: cierre del modelo y publicación

Autorización explícita del 11-09-2026: publicar tras terminar pasos y revisiones. Código analítico conservado en commit `93e3dba`; fuente individual permanece local. Dataset agregado final SHA-256 `c21b29389e3a3f0c3d90d7383ac5d19c41851a67d308261a6db841d70e6badfc`.

## Resultado y límites

Modelo general por predio bajo reglas SII 2026S1; incluye resultados cero y agrega luego por CUT. Contribución observada neta permanece sin certificar. Ranking de 15 comunas con residuo positivo y avalúo mediano sobre exención; escenarios mediana/promedio, q=0/0,25/0,5/1. La materialidad no vuelve a multiplicar el dinero. La transferencia a nuevos predios comparables es una hipótesis; ni deuda ni negligencia quedan demostradas.

Revisión alternativa NumPy por ramas y tasas racionales sobre los 6.054.808 roles y 344 comunas: medias, medianas, proporción positiva y productos coinciden con tolerancia menor de 0,000001 CLP por estadístico. El crosswalk sigue siendo el canónico, no una validación territorial independiente. Revisión entre agentes Codex, sin independencia de proveedor. Antártica y Trehuaco siguen sin fuente.

## Verificaciones y fallos conservados

| Comprobación | Evidencia |
|---|---|
| Modelo analítico | 78 pruebas en el cierre analítico; 25 del modelo repetidas tras aclarar metadatos. Mutante de tasa ×10 produce 7 fallos; versión canónica recupera verde. |
| Integración TypeScript | 136 pruebas; tipado, CSS y Vite aprobados. Cuatro pruebas nuevas rechazaron el dataset anterior sin modelo. |
| Integración Python | 56 pruebas, sin omisiones, con entorno predial y PMTiles fijado. Cuatro pruebas cruzadas rechazan nulos convertidos en cero, sensibilidad incorrecta y unidad incompatible. |
| Tabla accesible | La nueva tabla cambió el inventario esperado 9→10; rojo observado y actualizado con identificación explícita del nuevo host. |
| Datos y proyecciones | Parquet, JSON, CSV, tablas ES/EN y metadatos conciliados; clave SHA en la petición para evitar servir un dataset anterior desde caché. |
| Mapas previos | 20.068 valores físicos exactos; cinco fuentes y cuatro PNG con hashes intactos. Variación de suma flotante en cuatro campos de Galvarino <0,000001 CLP, sin cambiar cifras mostradas. |
| Inventario de assets | Primer gate detectó ocho imágenes grandes sin dueño y luego JSON agregado >1MB; propiedad y retención registradas. PNG monetarios incorporan dimensiones verificables; SVG omite dimensiones no verificables por ese gate. |
| Publicación | Borradores construidos antes de mover; ES/EN en _posts con fecha 11-09-2026. Build productivo y gate de enlaces de 20 posts aprobados. |

## Revisión visual y recuperación

La revisión detectó ambas variantes de figura visibles en modo claro, por precedencia CSS; se corrigió la especificidad. El selector adopta tipografía, superficie, contraste y foco del visor. Altura del gráfico se adapta al número de comunas. La tabla dinámica refleja q y región; referencia nacional permanece estática y explícita. Estado sin datos y fallo de descarga conservan tabla/fallback e informan la indisponibilidad.

Axe detectó nombres repetidos en regiones de tablas del post. El plugin ahora añade un ordinal por tabla. Se reinició sólo el preview 4004 para cargar el plugin Ruby; se conservan sus siete enlaces de mapas locales. Las comprobaciones de contraste sobre SVG y gradientes pueden quedar incompletas: no equivalen a una certificación WCAG ni a probar Safari real.

Los logs versionados normalizan espacios finales sin ocultar fallos. Los avisos conocidos de Sass @import y tamaño del módulo cartográfico permanecen. Las pruebas de rendimiento anteriores corresponden a su experimento fechado; no se presentan como una nueva medición de esta entrega.

## Despliegue

Pendiente de comprobar remotos, pipeline y contenido servido. El cierre R4 requiere evidencia HTTP y hashes de los activos referenciados por el HTML público, además del estado de CI. No se envían solicitudes institucionales ni se habilita sindicación para el post.

## Cierre local final

Recibo `avaluos-ii-release-local-receipt-20260911.json`: artículo ES claro y EN nocturno, cero violaciones axe y 28 comprobaciones aprobadas por versión; panel monetario cero violaciones y 24 aprobadas. Contraste SVG/gradientes conserva comprobaciones incompletas. El tema nocturno se confirmó después de la auditoría, con texto rgb(229,234,241) y fondo rgb(32,40,56). Se corrigió un rojo real de 139 nodos a contraste 3,88:1 en tablas nocturnas. `role=group` elimina el nombre ARIA en contenedor genérico.

La revisión delegada probó q=0,25/0,5/0 y cambios de región, incluyendo Iquique al 25% ($9,1 y $1.077,2 millones), ausencia de elegibles y fallo intencional de JSON. No dejó sesiones ni rutas simuladas abiertas. El preview 4004 sigue disponible por solicitud del usuario. El control público previo devolvió 404 para el post nuevo.
