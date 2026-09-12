# Comparación emparejada de carga cartográfica

Estado inicial: preparación terminada; ninguna observación ejecutada antes del
aviso `FREEZE` del integrador. Revisiones `e986f238` y `6b46731e`, protocolo fijado
en `catastro-paired-loading-20260911-protocol.json` antes de navegar.

## Comparabilidad y criterio previo

La versión anterior espera `load` antes de aplicar el encuadre de Chile; la nueva
aplica ese encuadre tras `style.load`. Comparar sólo el primer `load` puede medir
dos cámaras diferentes. La medida principal será el primer `idle` con 343 paths
del selector, `map.loaded()`, `areTilesLoaded()` y cámara inmóvil. El `load`
histórico se conserva como medida secundaria.

Ambas copias conservan sus propios HTML, CSS, JS y lógica. Una regla de fixture
idéntica fija el lienzo en 750 × 558 px dentro de viewport 1.280 × 577. Se usa el
mismo overlay vectorial, datos, estilo, tema y configuración de movimiento. Las
cámaras finales deben coincidir dentro de 0,0001 grados para el centro, 0,0001
para zoom, 0,1 grados para bearing/pitch y un píxel para dimensiones. Fuentes,
capas, manifest y estilo inicial deben tener identidad comprobable.

El umbral permanece: mediana fría al menos 10% menor; ninguna mediana de selector
o carga tibia empeora más de 10%. Son tres procesos nuevos y dos recargas por
versión, con orden alternado declarado. No es un ensayo estadístico ni permite
afirmar optimalidad global; el área estandarizada limita la conclusión al fixture.

Antes de navegar se pone el target en primer plano y se observan diez frames
regulares. El documento medido registra foco/visibilidad cada 50 ms y en eventos.
Se excluye por pérdida de foco según el criterio previo, nunca por duración.
Las exclusiones conservan todos sus tiempos y tienen máximo dos reemplazos por
versión/modo. Timeout de 30 s, error, geometría/estilo distinto o conteo incorrecto
son fallos observados; no se descartan para mejorar resultados.

## Preparación aislada y reproducción

No había bundle anterior conservado. Se extrajeron archivos concretos mediante
`git archive`, sin cambiar el checkout, y se compartió `node_modules` existente:
ambos lockfiles son idénticos. Vite construyó las dos versiones sin instalar
nada. En cada copia se añadió el mismo observador de MapLibre y se ajustó sólo
la base del cargador a su ruta temporal; no se alteró la cámara ni la carga.
`catastro-paired-loading-20260911-preparation.json` registra hashes de entradas
y artefactos. El aviso de chunk mayor de 500 KB permanece en ambos builds.

```sh
python3 scripts/catastro_sii/prepare_loading_benchmark.py --root /tmp/catastro-paired-final-20260911
python3 scripts/catastro_sii/prepare_loading_benchmark.py --root /tmp/catastro-paired-final-20260911 --project-only /tmp/3cucharadas-jekyll-4004
node scripts/catastro_sii/benchmark_loading.mjs --run /tmp/catastro-paired-final-20260911 /tmp/catastro-paired-final-20260911/freeze.txt
```

La primera orden rechaza sobrescribir copias existentes; para reproducir el
build completo se debe elegir otra raíz temporal. La proyección usa sólo el
servidor Jekyll existente en 4004 y enlaza datos compartidos. Se ejecutará tras
reconstrucción y `FREEZE`, porque Jekyll puede eliminar esas rutas efímeras.
El recibo `freeze.txt` contendrá el mensaje real del integrador; su existencia
no sustituye autorización ni valida resultados.

Sesiones exclusivas del ensayo: `perf-paired-cold`, `perf-paired-baseline` y
`perf-paired-candidate`; se cierran individualmente. Las dos sesiones tibias
permiten alternar versiones conservando cachés independientes. Las recargas
usan `Page.reload`, y se verifica un nuevo `performance.timeOrigin` para impedir
que una navegación de fragmento reutilice accidentalmente la observación anterior.

## Pruebas del evaluador, antes de los datos reales

Ocho pruebas focalizadas verdes con
`node --test --test-isolation=none tests/catastro_sii/benchmark-loading.test.mjs`.
Se observaron veredictos negativos para colección vacía, mejora insuficiente de
9%, mediana con corridas lentas, regresión tibia mayor de 10%, cámara/estilo
distintos, HTTP 404, timeout y pérdida de foco. El fixture equivalente con mejora
de 20% devuelve verde. Estos son controles sintéticos del evaluador, no evidencia
de rendimiento de ninguna versión. Node syntax checks, compilación Python y
`git diff --check` verdes.

## Primer intento tras FREEZE: serie incompleta por foco

Se conservan cinco observaciones en `catastro-paired-loading-20260911-attempt1.json`.
No se completó la serie ni se cambiaron umbrales o reglas de exclusión.

| Observación | Foco válido | Selector | Mapa útil | Tratamiento previo |
|---|---|---:|---:|---|
| Baseline fría 1, intento 1 | No | 9.852 ms | 10.302 ms | Excluida por documento oculto/desenfocado |
| Baseline fría 1, intento 2 | Sí | 1.702 ms | 2.178 ms | Conservada |
| Actual fría 1, intento 1 | Sí | 1.593 ms | 2.216 ms | Conservada |
| Actual fría 2, intento 1 | No | 811 ms | 10.060 ms | Excluida por documento oculto/desenfocado |
| Actual fría 2, intento 2 | No | 796 ms | 10.087 ms | Excluida por documento oculto/desenfocado |

El tercer intento de actual/fría2 se detuvo antes de navegar porque no cumplió
la preparación de foco/diez frames. No hay una sexta observación. Se mantienen
las cinco mediciones, incluso las lentas excluidas. No se observó error de mapa
y las cámaras finales fueron idénticas: centro `[-71.1,-39.38558098137152]`, zoom
`2.680030782531039`, bearing/pitch cero y lienzo 750 × 558. Estilo, manifest y
fuentes/capas coincidieron en las observaciones completas.

En las tres observaciones excluidas se registró un evento `blur`, seguido de
`visibilitychange` a oculto, entre 59 y 79 ms desde navegación; `style.load`
quedó pendiente hasta que la página volvió a visible alrededor de 9,4–9,6 s.
Los eventos cartográficos siguieron sin foco. En las dos observaciones válidas,
todos los hitos permanecieron visibles y enfocados. Esta evidencia identifica
una interferencia de visibilidad en el ensayo; no permite atribuir esos ocho
segundos al código de una versión. La pareja válida, por sí sola, tampoco
demuestra la mejora: 2.216/2.178 = 1,018, con muestra insuficiente.

El integrador detectó durante el ensayo que el evaluador revisaba fallos duros
después de excluir por foco y aceptaba igualdad entre hashes de objetos ausentes.
Se corrigió exclusivamente el evaluador: timeout/HTTP/runtime y estilo/manifest
ausentes bloquean aunque la observación se excluya de tiempos. Once pruebas
focalizadas pasan, incluidas esas dos condiciones negativas. Los datos originales
y el veredicto inicial se conservan; todos se reevaluaron uniformemente con la
corrección. El resultado sigue siendo **no cumple**, por serie incompleta; no se
presenta como una regresión establecida ni como una mejora demostrada.

Ese corte dejó F9_2 parcial. La [continuación con serie completa](catastro-paired-loading-20260911-focus.md) conserva este intento, registra dos fallos operativos, completa la comparación bajo las reglas previas y distingue el mapa útil del primer evento `load`.
