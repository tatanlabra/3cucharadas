# Diagnóstico adicional: pintura, fuentes y carga

| Hecho observado | Evidencia |
|---|---|
| Observers registrados antes de pintura | Baseline 60,7 ms y candidato 206,6 ms; FCP 1324/4536 ms. Observer nativo y observer adicional reportaron LCP consistente. Sin errores capturados. |
| Página visible y enfocada | Foco a 62,5/212,6 ms; sin pérdida posterior registrada; opacity 1 y visibility visible en HTML/body/héroe/h1. |
| LCP reapareció en repetición mínima | Baseline 1556 ms; candidato 4536 ms. Los missing del piloto permanecen sin reemplazo. |
| Fuentes y screenshot | Fonts ready después de DCL a 2103,7/6283,9 ms; LCP ocurrió antes. Await posterior fue inmediato. Screenshot posterior no cambió LCP/FCP. |
| Hero recibido mucho antes de LCP | Baseline1600:156080B, request140 ms/end168,6 ms, LCP1556 ms; candidato1600:161742B, request502,9 ms/end536,1 ms, LCP4536 ms. |
| Intervalos de render amplios | rAF candidato pasó de559,7 a4209,6 ms; el temporizador nominal5s se ejecutó a5429 ms. Estas observaciones muestran demora de scheduling, sin identificar su causa única. |
| CPU durante la sesión | /proc/stat: baseline81,66% y candidato99,13% de ocupación agregada. Deltas incluyen preparación y lectura, no exclusivamente render. |
| Competencia de CPU posterior | En seguimiento1,13s después: llama-server2,55cores, awk, Brave y bundle activos. No se extrapola esa atribución exacta al intervalo previo. |

## Disposición epistemológica

- Hipótesis provisional preferida: contención/scheduling del host o del renderer explica parte de la latencia variable y podría contribuir a pintura ausente antes del corte. La respaldan CPU agregada casi saturada, pausas entre frames y recursos entregados mucho antes de LCP.
- Evidencia contraria y límites: no se reprodujeron los dos missing; CPU por proceso se midió después, no durante esas dos navegaciones originales. El diagnóstico agregó observers y un rAF de observación, de modo que tampoco es un experimento causal idéntico al piloto.
- Prueba discriminante pendiente: cinco parejas conservadas bajo ventana coordinada, CPU10s antes de cada pareja y deltas durante cada navegación. Rechazar la explicación por contención si missing/demoras persisten de forma consistente con CPU baja y frames normales; estudiar entonces captura/renderer y obtención de métricas. No relajar2500ms ni10%.
- Registro tardío, página oculta o falta de foco quedan debilitados por esta repetición, pero no demostrados imposibles en el piloto anterior, que no instrumentó todos esos eventos.
- Espera de fuentes no bloqueó el LCP en esta repetición: LCP precedió fonts.ready. Esto no descarta efectos de las fuentes sobre otro rendimiento.
- No se modifica ni excluye el héroe CASEN del LCP: su mayor superficie como nuevo elemento LCP es un cambio real de contenido.

## Decode e instrumentación futura

- La duración original de decodificación no está disponible en Resource Timing. El intervalo responseEnd→LCP NO se presenta como decode. Se conserva null para esa duración.
- El probe posterior decode() usó por error `.page__hero-image`, mientras el candidato usa `.page__hero-media img`; su motivo “CSS background” no describe al candidato. No hubo medición decode válida y no se sustituyó por cero. El baseline sí utiliza fondo CSS.
- El arnés formal registra LCP raw loadTime/renderTime, observer registration, foco, visibilidad, fonts.ready, longtasks y waterfall. No incorpora el bucle rAF del diagnóstico ni llama vitals (que recarga).
- Dos capturas inspeccionadas: ambos héroes/títulos visibles. Servidores4041/4042 son propios;4004 permanece ajeno e intacto.
