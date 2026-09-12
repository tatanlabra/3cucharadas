# Cinco parejas formales: aceptación de rendimiento no alcanzada

| Página / condición | Mediana LCP baseline → candidato | Resultado |
|---|---|---|
| Avalúos II / frío | no estimada | Hay LCP ausentes; no se eliminan muestras para calcular una mediana favorable. |
| Avalúos II / caliente | 520 → 3832 ms | +636,92%; falla 2500 ms y margen 10%. |
| CASEN largo / frío | no estimada | Hay LCP ausentes; aceptación no concluyente en este grupo. |
| CASEN largo / caliente | 632 → 364 ms | −42,41%; pasa este grupo. |

- Colección 40/40, cinco parejas por página y condición. 32 LCP observados y ocho ausentes; no se imputaron ceros ni se descartaron valores lentos. Se conserva cada entrada y el checkpoint posterior a fonts.ready.
- CLS observado 40/40; máximo baseline 0.01454101 y candidato 0.03823597, ambos ≤0,1. summary.json conserva el resultado del colector, que marca null en grupos incompletos por LCP; observed-metrics-summary.json separa los CLS conocidos.
- Diez ventanas de CPU de 10 s antes de parejas y deltas por navegación. Ocupación agregada durante navegación entre 26.28% y 93.39%; cpu-pair-comparison.json registra diferencias por pareja sin excluir nada ni convertir diferencias de carga en prueba causal.
- Mismo Chrome 151 headless, 1440×1000, DPR 1, tema claro, CPU/red sin throttling, localhost permitido y servidor canónico con no-store. Frío=navegador nuevo; caliente=reload mismo navegador, sin afirmar hit de caché HTTP. No se vació caché del sistema operativo.
- Fuente de 144 archivos y copia del build de 1248 archivos verificadas antes/después; hashes del arnés e init coinciden con settings. Figuras/política nuevas están en el candidato medido; builds antiguos del piloto no se aceptan como finales.

## Hallazgo de presentación

- Avalúos candidato caliente, pareja 1: paintTime 134,3 ms pero presentationTime/startTime 4036 ms; fonts.ready 409,1 ms; CPU 38,2%. Se conserva el LCP estándar de 4036 ms.
- Avalúos candidato frío, pareja 1: observer a 36,8 ms, foco a 38,6 ms, fonts.ready 1058,4 ms, visible y sin entradas paint a 5 s; CPU 38,0%. El checkpoint posterior tampoco obtuvo LCP.
- Estos casos debilitan la hipótesis de que la saturación global de CPU o la espera de fuentes expliquen por sí solas la anomalía. La separación entre pintura y presentación apunta provisionalmente al compositor/presentación o al entorno headless; no demuestra un defecto de Chromium ni una causa única.
- No se cambia el umbral ni se reemplaza LCP por paintTime. Root inició un canary separado para discriminar esa hipótesis; sus resultados no forman parte de estas 40 navegaciones ni eliminan el rojo.

El runner terminó con 0 porque completó la colección. Esa salida no acredita aceptación: el receipt permanece partial y el gate debe recomputar desde runs.json. Veinte sesiones propias y servidores 4041/4042 cerrados; 4004 intacto. No hubo cambios de producto.
