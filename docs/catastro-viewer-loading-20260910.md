# Carga del visor: evidencia local del 10-09-2026

## Alcance y decisión

Se conserva MapLibre y PMTiles. El selector SVG de Chile se monta con independencia
del motor y del fondo cartográfico. El motor solicitado y los JSON se descargan
en paralelo. Se conserva la carga diferida por proximidad a la sección; con
`saveData` se elimina el margen anticipado de 640 px. No se descarga una colección
completa de capas UV: sólo la comuna seleccionada.

La caché JSON vive únicamente en la página: comparte promesas y objetos ya
parseados, conserva la versión de la URL, aplica TTL de cinco minutos, LRU de
16 entradas y presupuesto de 8 MiB de contenido JSON serializado estimado.
Ese presupuesto no pretende medir el heap JavaScript. Los errores HTTP/JSON y
los timeouts se expulsan; las URL mutables usan revalidación HTTP (`no-cache`).
No se incorporan service workers, IndexedDB, localStorage ni persistencia nueva
de datos. El transporte PMTiles y su tratamiento de HTTP Range quedan intactos.

El selector legacy, el mapa y el gráfico introductorio comparten una sola
petición de filas comunales durante la página. El laboratorio conserva sus
fuentes propias: `insights-v1.json` y `explorador_comunal.json` tienen esquemas
distintos y no pueden sustituirse por `comunas.json`.

## Mediciones observadas

Navegador Chromium headless real mediante sesión aislada `perf-polish`, Jekyll
del host en `http://127.0.0.1:4004/catastro_sii_brecha/?vista=mapa#bivariate-card`.
El tiempo parte de la navegación. Frío significa proceso de navegador nuevo;
recarga significa misma sesión y caché HTTP disponible. No se simularon tiempos
de red en estas mediciones. Son observaciones individuales de un host compartido,
no percentiles, ensayo controlado ni medición de producción.

| Evento | Baseline frío | Final frío | Baseline recarga | Final recarga |
|---|---:|---:|---:|---:|
| Primer path del selector Chile | 2.342 ms | 900 ms | 1.099 ms | 592 ms |
| Canvas cartográfico en DOM | 1.791 ms | 1.614 ms | 841 ms | 949 ms |
| Controlador/estilo disponible | 2.342 ms* | 9.853 ms | 1.099 ms* | 980 ms |
| Fondo terminado, evento MapLibre `load` | 2.342 ms | 10.175 ms | 1.099 ms | 1.185 ms |
| Peticiones `comunas.json` | 2 | 1 | 2 | 1 |

\* El baseline habilitaba el controlador después del evento `load`; la versión
actual lo habilita con `style.load`, sin esperar todas las teselas externas.
Por ello esa fila no es un benchmark estrictamente equivalente.

Una petición de `comunas.json` transfirió 643.734 bytes en este servidor local.
Al compactar la diagramación apareció una segunda descarga desde el gráfico
introductorio; también se integró al mismo puente y la medición final vuelve
a una sola petición. El JSON del selector no cambió (759.295 bytes sin cabeceras).

La mejora consistente observada es que Chile aparece antes y deja de depender
del fondo, junto con la eliminación de descargas/parseos redundantes. **No se
demuestra una aceleración global del mapa:** el arranque final en frío fue más
lento. La petición del estilo remoto devolvió estado de Resource Timing 0 y
activó el fallback OSM; también hubo espera prolongada entre canvas y estilo.
No se atribuyen esos ocho segundos exclusivamente a la red: separar worker,
GPU, carga del host y origen remoto necesita una traza adicional. En producción
deben medirse percentiles y un origen cartográfico sano antes de prometer tiempos.

El presupuesto de JavaScript previo al selector deja de exigir el chunk de
MapLibre completo: el app inicial pasó de unos 1.046 KB a unos 28 KB, con el
motor separado de unos 1.024 KB. Se descarga igualmente cuando corresponde;
es división de la ruta crítica, no eliminación de ese coste.

## Pruebas negativas, recuperación y caché real

- Test inicial rojo: el módulo de caché aún no existía.
- Tests verdes: coalescencia concurrente, versiones de URL, TTL, expulsión LRU,
  límite de tamaño, errores HTTP/JSON, timeout, puente legacy y recuperación.
- Caldera → Copiapó → Caldera produjo una petición por comuna: Caldera 25.115
  bytes y 4,9 ms; Copiapó 33.358 bytes y 3,5 ms. Volver a Caldera no produjo
  descarga nueva; el resumen y la capa comparten el objeto parseado.
- La ruta `**/chunks/map-*.js` se abortó deliberadamente: quedaron 343 paths
  del selector disponibles y un mensaje con recuperación explícita.
- Se observó un rojo adicional: repetir el mismo import ES después de retirar
  el bloqueo no recuperaba el motor, porque el navegador retenía el fallo.
  Se corrigió a «Recargar visor» para import fallido. Restaurar la ruta y pulsar
  el botón recuperó canvas y estado nacional conservando la URL.
- Errores de datos y de inicialización del mapa mantienen reintentos en la
  página; los datos se abortan a los 15 s y la espera del estilo a los 20 s.
- Con WebGL2 deshabilitado mediante init script: 343 paths de Chile, mensaje
  accesible de degradación y cero peticiones del motor MapLibre.
- `aria-busy` distingue la carga del selector y de la capa UV; cambiar de comuna
  conserva nodos/foco del SVG y descarta resultados obsoletos por token.

## Reproducción y comprobaciones

Instrumentación: `scripts/catastro_sii/probe_loading.js`, utilizable mediante
`agent-browser --session <aislada> --init-script <ruta-absoluta> open <url>`.
Leer `window.__catastroPerf` y `performance.getEntriesByType('resource')`.
El observador mide presencia en DOM y eventos del controlador; no inspecciona
la calidad visual de cada tesela. Cerrar exclusivamente la sesión de prueba.

Comprobación focalizada ejecutada: Vitest, seis archivos, 36 tests verdes:
`data`, `map-parcel-lifecycle`, `legacy-territory`, `territorial-aggregates`,
`map-capability` y `coverage-teaser`. TypeScript y `git diff --check` verdes.
Vite construyó correctamente; mantiene el aviso conocido de chunk MapLibre
mayor de 500 KB. La validación integral corresponde al cierre de integración.

No se modificaron dependencias, publicación ni servidor. La sesión de navegador
`perf-polish` quedó cerrada y Jekyll 4004 permaneció activo.

## Ajuste posterior: altura estable al recorrer Chile

Se reprodujo el salto mediante hover real a 1.280 px: Teno, Maule dejaba el
grid y el mapa horizontal con 187,78 px; Quinta de Tilcoco, Libertador General
Bernardo O'Higgins los elevaba a 203,50 px. La diferencia de 15,72 px provenía
del párrafo de estado, que mezclaba nombre, disponibilidad UV y acción.

| Alternativa | Evaluación |
|---|---|
| Dos filas, nombre completo y acción separada | Elegida: didáctica, mantiene teclado y evita saltos con reserva proporcional de dos líneas para el nombre |
| Altura rígida para todo el panel | Innecesariamente amplia y frágil ante zoom o traducciones |
| Truncar nombres o usar sólo tooltip flotante | Oculta información territorial y debilita lectura móvil y accesibilidad |

El nombre y la región ocupan el primer bloque; «Haz clic para ver esta comuna»
ocupa siempre el segundo. El teclado muestra «Pulsa Enter…». Se elimina la
referencia UV redundante tanto del estado visual de hover como del tooltip
nativo; la disponibilidad sigue en el nombre accesible del control. La reserva
usa `em` y altura mínima: permite crecimiento natural ante texto ampliado y
no corta ni oculta nombres.

| Ancho | Comunas verificadas | Altura mínima del grid | Altura máxima del grid | Estado |
|---:|---:|---:|---:|---|
| 1.280 px | 343 | 223,656 px | 223,656 px | Sin salto ni overflow de página |
| 390 px | 343 | 404,156 px | 404,156 px | Sin salto ni overflow de página |
| 320 px | 343 | 444,469 px | 444,469 px | Sin salto; estado contenido en x34–286 |

Además de hover físico en etiquetas extremas, se disparó `pointerenter` en
cada uno de los 343 paths y se comparó el rectángulo del grid y del estado;
el estado permaneció en 69,469 px en los tres anchos. CSS y TypeScript verdes.
Captura inspeccionada: `/tmp/chile-hover-mobile-320.png`.

A 320 px se observó un overflow general independiente del selector: el enlace
de fuentes del laboratorio `.inline-link`, con `white-space: nowrap`, alcanzaba
x338. Se comunicó al integrador para corregir su bloque; no se mezcló esa
modificación con los selectores exclusivos del hover. La sesión de navegador
se cerró al terminar.

La integración detectó además dos fixtures desactualizados en
`tests/catastro_sii/accessibility.test.ts`: simulaban el contenedor como `{}` y
ejecutaban cualquier listener de MapLibre en el momento de registrarlo. Se
reprodujeron los dos fallos y se corrigió el doble para modelar `dataset`, ancho,
timers y emisión explícita de eventos. Dos regresiones nuevas comprueban que
`style.load` habilita controles sin anunciar el fondo terminado y que un estilo
ausente durante 20 s libera el mapa y rechaza la inicialización. Resultado:
11/11 tests de accesibilidad; 25/25 al combinar accesibilidad, caché y ciclo de
capas; TypeScript verde. No se modificó producción para eludir los fixtures.

## Ajuste posterior: rodillos en cascada al llegar a las cifras

Los rodillos pasan de 520–720 ms a 850–1.090 ms según la cantidad de dígitos.
Una cola compartida permite animar un único número a la vez en orden de lectura
(arriba–abajo, izquierda–derecha). Cada número conserva su valor final real desde
que llegan los datos; la cola retrasa sólo la decoración `aria-hidden`.

La observación permanece activa durante la cola y el efecto. El gatillo exige
55% de intersección con margen inferior negativo de 10%; no anticipa números
fuera de pantalla. Al salir del área observada se cancela el efecto o la espera.
Cambiar el valor invalida su registro anterior; una finalización tardía no puede
sobrescribir la nueva selección. Ocultar la pestaña o activar movimiento reducido
limpia el efecto y toda la cola. Sin IntersectionObserver se conserva texto
estático; no se instala un listener continuo de scroll.

Prueba roja observada antes del cambio: 5/9 casos fallaban por simultaneidad,
ausencia de cancelación al salir, gatillo temprano y fallback sin observador.
La versión nueva pasó 9/9, incluyendo orden, no solapamiento, valores inmediatos,
geometría obsoleta en cola, reemplazos rápidos, pestaña oculta y movimiento
reducido. TypeScript verde. Son cinco casos más que la suite previa de rodillos.

En navegador real y navegación limpia, la instrumentación registró cero llamadas
a WAAPI antes del scroll. Al entrar al bloque comenzaron, en orden, cobertura,
cobertura de hogares, población, predios, coordenadas, superficie y avalúo.
Las duraciones declaradas observadas fueron 850–1.060 ms en esos valores.
Una selección real de Atacama mostró como máximo un elemento `.number-rolling`
simultáneo, con el siguiente inicio posterior al cierre anterior. Los siete
efectos terminaron en unos 6,6 segundos y conservaron los valores de Atacama.

Un primer intento de scroll por etapas no registró efectos y la espera de 25 s
agotó su plazo; por eso se repitió desde navegación limpia instrumentando los
callbacks de IntersectionObserver y WAAPI. Esa repetición confirmó cero efectos
fuera del área visible y el ingreso secuencial al observar las siete cifras. El
efecto es descartable al salir y no se promete repetición para un valor idéntico.
La comprobación del navegador se cerró sin modificar datos fuente.
