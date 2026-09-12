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

Al terminar la validación local quedaba pendiente comprobar remotos, pipeline y contenido servido. Ese estado histórico queda resuelto por la comprobación productiva registrada abajo. No se envían solicitudes institucionales ni se habilita sindicación para el post.

## Cierre local final

Recibo `avaluos-ii-release-local-receipt-20260911.json`: artículo ES claro y EN nocturno, cero violaciones axe y 28 comprobaciones aprobadas por versión; panel monetario cero violaciones y 24 aprobadas. Contraste SVG/gradientes conserva comprobaciones incompletas. El tema nocturno se confirmó después de la auditoría, con texto rgb(229,234,241) y fondo rgb(32,40,56). Se corrigió un rojo real de 139 nodos a contraste 3,88:1 en tablas nocturnas. `role=group` elimina el nombre ARIA en contenedor genérico.

La revisión delegada probó q=0,25/0,5/0 y cambios de región, incluyendo Iquique al 25% ($9,1 y $1.077,2 millones), ausencia de elegibles y fallo intencional de JSON. No dejó sesiones ni rutas simuladas abiertas. El preview 4004 sigue disponible por solicitud del usuario. El control público previo devolvió 404 para el post nuevo.

## Producción comprobada

El 11-09-2026 a las 23:43:30 de Santiago, el [recibo productivo](avaluos-ii-release-production-receipt-20260911.json) registra tres páginas HTTP 200, contenido esperado y 58 recursos descargados desde las referencias del HTML efectivo, el manifiesto del visor y sus datos/figuras. Los 58 SHA-256 coinciden con el build revisado; cero errores y cero discrepancias. El HTML se valida por canonical, fórmulas y marcadores de contenido; sus hashes quedan registrados, sin exigir igualdad byte a byte entre builds con timestamps diferentes.

| Evidencia | Resultado |
|---|---|
| Artículo ES | https://3cucharadas.cl/datos/territorio/avaluos-ii-brecha-residencial/ — 404 previo → 200 con contenido esperado. |
| Artículo EN | https://3cucharadas.cl/en/datos/territorio/avaluos-ii-brecha-residencial/ — 200, canonical y ocho expresiones KaTeX. |
| Visor | https://3cucharadas.cl/catastro_sii_brecha/ — 200, panel monetario y SHA del dataset final. |
| GitLab Pages | [Pipeline 2842505278](https://gitlab.com/tatanlabra/3cucharadas/-/pipelines/2842505278), success para `9b5ddf83048e02397875c55eab4e9b33528675ca`; terminó a las 02:42:28 UTC del 12-09. |
| GitHub | [Redirector](https://github.com/tatanlabra/3cucharadas/actions/runs/34668294141) y [automatización de sindicación existente](https://github.com/tatanlabra/3cucharadas/actions/runs/34668294132), success. Avalúos II carece de opt-in de sindicación. |
| Seguridad de dependencias | `npm audit`: cero vulnerabilidades; API de alertas abiertas de GitHub: lista vacía. El aviso de tres moderadas durante el push correspondía al estado anterior. |
| Fuente y publicación | El commit analítico `93e3dba` permanece local; el blog publica exclusivamente los derivados agregados y activos revisados. |

El primer intento de push fue rechazado por la revisión automática por falta de evidencia del destino y del contenido saliente. Se verificó mediante API que el proyecto público GitLab `tatanlabra/3cucharadas` (57339918) tiene el dominio `3cucharadas.cl` verificado, que GitHub es el espejo configurado y que el envío era fast-forward. La inspección acotada de 140 archivos no detectó patrones privados ni fuentes individuales. Con esa evidencia adicional, la revisión automática aprobó el mismo push. No queda permiso pendiente ni se eludió el rechazo.

GitHub añadió después `d8184c7c`, un ajuste automático de saltos de línea en `_data/distribucion.yml`. La comparación YAML de ambas versiones dio igualdad semántica; se integró por fast-forward para conservar su autoría e historia. El commit de cierre sólo añade documentación excluida del build y usa `[skip ci]`; la evidencia productiva sigue vinculada al commit de implementación `9b5ddf83`, no a un supuesto segundo despliegue.

Reproducción del recibo: `python docs/avaluos-ii-release-public-check-20260911.py.txt /tmp/avaluos-production-recheck.json`, conservando o reconstruyendo el build aprobado en `/tmp/avaluos-release-production`. El script es una copia del comprobador usado, fijada a esta entrega; no constituye un verificador universal del sitio. Cambios posteriores en producción pueden invalidar la paridad y requieren otro recibo.

R1–R4 quedan completos para esta publicación. El neto observado, un enlace vivienda–rol que identifique omisiones y la ejecución futura del post III siguen fuera del resultado demostrado. La revisión móvil se realizó en viewport de 390 px; no se observó Safari/iPhone real. El URL público permite abrir el artículo desde el teléfono sin depender del preview local.
