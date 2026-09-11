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

## Auditoría adicional del 11-09-2026: tiempos, CORS y planificación de frames

Se repitió la medición sobre los mismos assets locales del commit `b293b365`,
Chromium headless 151, mediante tres procesos nuevos y dos navegaciones con el
tercer proceso reutilizado. Viewport fijo 1.280 × 900, misma URL y sonda. La caché
del sistema operativo, la carga del host y los servicios externos no se reiniciaron.
Frío designa un proceso nuevo; tibio no garantiza que cada recurso salga de caché:
`comunas.json` se transfirió una vez por navegación también en las recargas.

| Navegación | Selector SVG | Canvas | Controlador/estilo | Fondo `load` |
|---|---:|---:|---:|---:|
| Fría 1 | 1.777 ms | 2.830 ms | 2.855 ms | 3.188 ms |
| Fría 2 | 1.312 ms | 1.851 ms | 1.879 ms | 2.376 ms |
| Fría 3 | 1.785 ms | 2.340 ms | 2.359 ms | 2.846 ms |
| Tibia 1 | 410 ms | 672 ms | 727 ms | 881 ms |
| Tibia 2 | 481 ms | 797 ms | 831 ms | 1.006 ms |
| Control frío 1.280 × 577, sin profiler | 1.476 ms | 2.005 ms | 2.025 ms | 2.421 ms |

Las seis navegaciones conservaron 343 paths y una petición de `comunas.json`.
La mediana fría del fondo fue 2.846 ms. El máximo evento completo de las trazas
frías fue un `RunTask` de 508,6 ms; no apareció el tramo de ocho segundos en esta
serie. Esto contradice una regresión sostenida de diez segundos, pero no demuestra
aceleración frente al baseline original: aquel fue una observación aislada, sin
control equivalente de viewport, foco, origen y estado de caché.

### Fallo de estilo identificado, sin atribución especulativa a la red

La petición a
`https://tiles.3cucharadas.cl/catastro-sii/basemap_chile_20260719T124804Z.style.json`
falló en el navegador local con `net::ERR_FAILED`; CDP precisó
`corsErrorStatus.corsError = MissingAllowOriginHeader`. Su espera fue de 250 a
964 ms, insuficiente para explicar el tramo histórico de ocho segundos.

El manifest local respondía 404; el visor usaba entonces el manifest público.
La política versionada `scripts/catastro_sii/r2-cors.json` permite producción y
`localhost:4001/5173`, pero no `127.0.0.1:4004`. Un GET real del mismo activo con
`Origin: https://3cucharadas.cl` respondió 200 y `Access-Control-Allow-Origin`
correcto; con el origen del preview respondió 200 sin esa cabecera. La evidencia
corresponde a una incompatibilidad del preview con CORS, no a un activo público
caído ni a un fallo demostrado del recorrido de producción.

Se activó el respaldo raster OSM. En el control CDP las doce teselas respondieron
200, `fromDiskCache: false`; el mapa visible mostró base y etiquetas completas.
`transferSize = 0` en Resource Timing para esos recursos externos no prueba caché.
La serie anterior mide este respaldo, no la cartografía vectorial de producción.

### Overlay local existente y control discriminante

`verify_local_preview_manifest.py` validó los activos ya presentes en
`~/.local/state/3cucharadas/catastro_sii/local`. Se proyectaron **sólo siete
archivos requeridos**, mediante symlinks bajo
`/tmp/3cucharadas-jekyll-4004/assets/data/catastro_sii/local`: manifest, índice
territorial, tres PMTiles, estilo y fuente Noto Sans. Referencian 653.730.830 bytes
existentes; no se duplicó ese contenido ni se descargaron datos. El destino es
efímero, separado del artefacto público. No se editó el manifest versionado, el
estado canónico, CORS remoto ni código de MapLibre.

Jekyll 4004 sirvió el PMTiles con `206 Partial Content`,
`Content-Range: bytes 0-15/600873308` y 16 bytes con cabecera `PMTiles`. El estilo y
la fuente locales respondieron 200. No se abrió otro servidor ni se reinició éste.

| Control vectorial, 1.280 × 577 | Selector | Canvas | Estilo | Fondo | Primera pintura |
|---|---:|---:|---:|---:|---:|
| Proceso nuevo, foco no preparado | 823 ms | 947 ms | 9.573 ms | 9.984 ms | 9.712 ms |
| Proceso nuevo, target en primer plano y diez frames previos | 1.062 ms | 1.213 ms | 1.246 ms | 1.874 ms | 560 ms |

La primera corrida reprodujo la espera larga y la aisló: el estilo había terminado
su fetch a 827 ms y el worker respondió a 1.005 ms, pero un callback de
`requestAnimationFrame` esperó **8.617 ms**. El primer request PMTiles llegó después,
a 9.568 ms. El mayor long task observado fue 78 ms; no hubo llamada WebGL
instrumentada de más de 50 ms. MapLibre `Style.loadJSON` difiere `_load` mediante
`browser.frameAsync`; el controlador depende de ese frame antes de `style.load`.

En el segundo proceso se ejecutó `Page.bringToFront` antes de navegar y se
observaron diez frames separados por unos 16,7 ms. `hasFocus()` fue verdadero
antes y después de esa navegación; era falso al medir la primera. El retardo
desapareció. **Hipótesis favorecida:** la planificación/foco del navegador de
pruebas interfiere con el primer frame. Es una explicación provisional: una sola
pareja y dos preparaciones conjuntas no prueban que `bringToFront` sea la única
causa. Se descarta como explicación suficiente si el retardo reaparece con target
visible, enfocado y frames regulares durante todo el intervalo. El listener CDP
de estados de foco no sobrevivió a la navegación de la CLI; no se afirma que
se observó continuamente esa condición. No se aplicó ningún parche especulativo.

El overlay vectorial y OSM tienen estilo, encuadre y capas diferentes; comparar
sus tiempos como una mejora del código sería inválido. La captura final del
overlay muestra cartografía vectorial legible, con base y topónimos. El criterio
de cierre global permanece pendiente: mismo estilo, capas, viewport, foco y
estado HTTP; al menos tres navegaciones por versión; mediana de `load` menor y
sin regresión del selector. No hay evidencia de optimalidad global.

### Reproducibilidad, archivos y reversión

Los resultados completos están en `catastro-map-loading-20260911.json` y
`catastro-map-loading-20260911-overlay.json`; los errores CDP acotados, en
`catastro-map-loading-20260911-network.json`. El índice `...-traces.json` conserva
conteos, hashes y máximos; las trazas completas son temporales en `/tmp`.
Las sondas `...-probe.js`, `...-network.mjs` y `...-foreground.mjs` son diagnósticos
fuera del bundle. Worker Resource Timing produjo duraciones negativas en algunas
capturas: se conservaron como anomalía y no se usaron para atribuir tiempos.

Desde la raíz del repositorio, para una navegación fría reproducible:

```sh
agent-browser --session perf-polish --init-script "$PWD/docs/catastro-map-loading-20260911-probe.js" open about:blank
agent-browser --session perf-polish set viewport 1280 900
agent-browser --session perf-polish profiler start --categories 'devtools.timeline,v8.execute,blink.user_timing,loading,gpu,disabled-by-default-devtools.timeline'
agent-browser --session perf-polish open 'http://127.0.0.1:4004/catastro_sii_brecha/?vista=mapa#bivariate-card'
agent-browser --session perf-polish eval 'window.__mapTrace'
agent-browser --session perf-polish profiler stop /tmp/catastro-reproduction.trace.json
agent-browser --session perf-polish close
```

Leer los hitos cuando aparezca `basemap-load`; para tibio conservar el proceso.
Para el control de foco, obtener `agent-browser ... get cdp-url` en `about:blank`
y pasar ese endpoint local a `node docs/catastro-map-loading-20260911-foreground.mjs`
antes de navegar. La sonda introduce coste de observación y no mide percentiles
de usuarios reales.

El comando efectivo del servidor observado fue:

```sh
vendor/bundle/ruby/3.4.0/bin/jekyll serve --drafts --unpublished --host 127.0.0.1 --port 4004 --destination /tmp/3cucharadas-jekyll-4004
```

El overlay se conserva para la revisión solicitada. Un rebuild puede retirarlo:
la configuración canónica sólo conserva `.git` y `.svn`. Para una futura sesión
persistente basta un archivo YAML **local, fuera del repositorio**, por ejemplo
`/tmp/3cucharadas-preview-4004.yml`, con `keep_files` que incluya esas dos rutas y
`assets/data/catastro_sii/local`, y pasar ambos archivos a `--config`. No se creó
ese archivo ni se reinició ahora. La proyección puede recrearse enlazando sólo
los siete archivos declarados; quitar sus symlinks y directorios vacíos revierte
el preview sin tocar los originales. Nunca trasladar el overlay a un build de
publicación. Se cerró únicamente la sesión `perf-polish`; Jekyll 4004 permanece.
