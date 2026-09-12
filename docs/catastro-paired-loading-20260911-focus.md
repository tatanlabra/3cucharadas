# Continuación del ensayo: fijar el navegador

Registro previo a una segunda serie completa, 11-09-2026. Se conservan protocolo, resultados y veredicto del intento anterior. Esta continuación no modifica el visor ni relaja las condiciones de aceptación.

## Diagnóstico y alternativas

Hecho anterior: tres observaciones quedaron ocultas durante la carga y no completaron una serie comparable. Su perfil efectivo no quedó registrado; no se puede afirmar que fueran navegadores con ventana ni atribuir causalmente el incidente a ese modo.

Una sonda actual en navegador explícitamente headless confirmó `HeadlessChrome/151.0.0.0` con motor Chrome 151.0.7922.77. La primera navegación permaneció visible, con foco tras los primeros 18 ms y 343 comunas. Las dos visitas posteriores con la misma URL no crearon documentos nuevos: son lecturas repetidas del mismo documento, no tres navegaciones independientes. No se cuentan como mediciones de rendimiento ni como prueba de fiabilidad.

`Browser.getBrowserCommandLine` fue rechazado porque el proceso no tiene `--enable-automation`; se registró esa limitación y se consultó `Browser.getVersion`, sin cambiar flags globales ni emular resultados. La sonda vive separada del ensayo.

| Alternativa | Decisión y límite |
|---|---|
| Fijar headless explícito y registrar versión por observación | Aplicada a ambos candidatos; elimina una dependencia de configuración sin falsear eventos de foco; falta observar la serie |
| Emular foco o ignorar páginas ocultas | Descartada: alteraría la precondición que explica el sesgo anterior |
| Repetir hasta conseguir un resultado favorable | Descartada: mantengo orden, tamaño, reemplazos máximos y umbrales previos |

Hipótesis provisional: controlar el modo de arranque permite completar una serie con foco estable. La evidencia discriminante son las trazas de visibilidad y foco de los doce pasos; se descarta si reaparece la pérdida de foco con este perfil. No demuestra la causa del intento anterior.

## Serie declarada

El protocolo de continuación copia literalmente los umbrales, número de observaciones, orden, viewport, caché, tolerancias geométricas y reglas de fallos del original. Añade únicamente el modo headless explícito y registro del motor. Las revisiones siguen siendo e986f238 y 6b46731e; el código cartográfico actual coincide con esta última, aunque el blog tiene commits editoriales posteriores.

Se prepararon las mismas dos copias aisladas con el script existente y se proyectaron al Jekyll 4004 ya activo, sin reiniciarlo. Durante la serie no se modificará fuente del sitio; el recibo FREEZE es un compromiso operativo del agente principal, no una aprobación humana simulada. Se conserva cada observación, incluso si el criterio falla.

## Intento con modo explícito

La primera carga fría baseline completó el mapa útil en 2.027,4 ms, con foco válido y sin errores. La siguiente sesión falló antes de navegar con `Could not configure browser: Failed to connect: No such file or directory`. El runner acababa de cerrar y volver a abrir `perf-paired-cold`; la desaparición del socket durante esa reutilización es compatible con una carrera de cierre. No se atribuye una duración cartográfica al intento que no navegó.

Se conservan resultado, error y hash del runner en `catastro-paired-loading-20260911-attempt2.json`. El arreglo usa un identificador único para cada proceso frío y otro por versión para las recargas; no se añade una espera arbitraria. El runner también rechaza sobrescribir un archivo de resultados existente. Estos cambios no tocan el evaluador ni el visor. La hipótesis de carrera se descarta si falla igualmente el arranque con nombres nuevos.

La siguiente serie empieza completa en otro directorio y conserva el intento abortado. No se decide repetir a partir de sus tiempos: faltan nueve observaciones por un fallo de infraestructura anterior a la navegación.

## Resultado de la serie completa

La tercera serie terminó con diez observaciones válidas —tres frías y dos recargas por versión—, dos cebados y dos exclusiones por foco, conservadas en [attempt3.json](catastro-paired-loading-20260911-attempt3.json). No se agotó el límite previo de reemplazos; no hubo fallos cartográficos, HTTP ni de equivalencia. Las doce navegaciones previstas completaron su paso; el total de intentos fue catorce por los reemplazos. Las exclusiones fueron `candidate-cold1-attempt1` (10.039,6 ms) y `baseline-cold3-attempt1` (10.483,4 ms).

| Mediana en ms | Baseline | Actual | Cambio |
|---|---:|---:|---:|
| Mapa útil, frío | 2.002,20 | 1.593,10 | −20,43 % |
| Mapa útil, recarga | 1.668,10 | 1.077,45 | −35,41 % |
| Selector, frío | 1.548,30 | 980,10 | −36,70 % |
| Selector, recarga | 1.207,75 | 523,60 | −56,65 % |
| Primer evento `load`, frío | 1.525,70 | 1.423,10 | −6,72 % |
| Primer evento `load`, recarga | 1.196,90 | 960,60 | −19,74 % |

El criterio principal y las tres salvaguardas del protocolo dan **PASS**. Las cámaras finales coinciden: centro [−71,1; −39,38558098137152], zoom 2,680030782531039 y lienzo 750 × 558; iguales hashes de estilo inicial, manifiesto y fuentes/capas finales. El motor observado en las catorce visitas fue Chrome 151.0.7922.77 headless.

La pérdida de foco **reapareció incluso en headless**: queda refutada la expectativa de que fijar ese modo bastaría para evitarla. La serie pudo completarse dentro de los reemplazos predeclarados, pero no queda resuelta su causa. Los identificadores únicos evitaron el fallo de socket durante esta serie; una serie sin ese fallo es evidencia acotada, no prueba universal de su causa o ausencia futura.

### Qué mide el criterio y qué no

El contrato resumido decía «MapLibre load», pero el protocolo original, fijado antes de las mediciones y conservado en `ecc5800a`, ya distinguía el mapa útil como medida principal: el evento `load` de la versión anterior ocurre con centro [−71,1; −36,7] y zoom 3,1, antes de ajustar Chile. En la versión nueva ocurre durante la transición. Esas cámaras no son equivalentes; compararlas como final de carga mezclaría estados visuales distintos.

Se sincroniza ahora la redacción del contrato con esa definición previa: primer `idle` con `loaded`, teselas listas, cámara inmóvil y 343 comunas. No se cambian umbrales tras los resultados. El evento `load` se conserva como secundario y **su reducción fría de 6,72 % no satisface por sí sola el umbral del 10 %**. La mejora demostrada del 20,43 % corresponde al estado final comparable.

El alcance es un ensayo local controlado de dos revisiones, con cinco observaciones válidas por revisión, sin significación estadística inferida. No certifica percentiles de producción, redes móviles, todos los dispositivos ni la respuesta de proveedores externos. La estabilidad de foco tampoco se presenta como resuelta.

### Runtime y reproducción

La sonda y el ensayo inicial usaron Node 26.8.2 del host. Para comprobar el `.nvmrc` del proyecto, se obtuvieron temporalmente Node 26.8.1 y su SHA-256 oficial `3e301118d7df53d563b7e96c1617545f26e2f76f9724be668d6cab65c15dda5d`. Las dos variantes se reconstruyeron con 26.8.1 y **todos sus artefactos coinciden byte a byte** con los medidos. El código ejecutado en Chrome no cambia; el gate integral se ejecuta con el runtime fijado. No se instaló Node globalmente.

```sh
PATH=/tmp/node-v26.8.1-linux-x64/bin:$PATH python scripts/catastro_sii/prepare_loading_benchmark.py --root /tmp/catastro-paired-pinned-20260911
node scripts/catastro_sii/benchmark_loading.mjs --run /tmp/catastro-paired-focus-20260911/series3 /tmp/catastro-paired-focus-20260911/series3/freeze.txt docs/catastro-paired-loading-20260911-protocol2.json
node --test --test-isolation=none tests/catastro_sii/benchmark-loading.test.mjs
```

Para repetir hay que elegir directorios nuevos, preparar/proyectar los builds y registrar un nuevo FREEZE antes de navegar. La orden de ensayo rechaza resultados previos: se observó el rechazo con el directorio del intento 2 y se confirmó su SHA-256 intacto. Las once pruebas del evaluador mantienen los casos negativos de timeout, HTTP, estados ausentes, foco y umbrales.

Al terminar se cerraron las sesiones exclusivas y se retiró solamente el enlace `__catastro_benchmark`; el Jekyll 4004 y sus siete enlaces cartográficos permanecen. Los JSON, protocolo y errores anteriores quedan versionados.
