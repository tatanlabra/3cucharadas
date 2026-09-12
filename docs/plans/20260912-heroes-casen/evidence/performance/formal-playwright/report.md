# Formal Playwright, mismo Chrome151 — RED

| Grupo | Referencia ms | Candidato ms | Cambio | Resultado |
|---|---:|---:|---:|---|
| Avalúos cold |1068|964|−9,74%|PASS|
| Avalúos warm |244|344|+40,98%|RED|
| CASEN cold |984|1140|+15,85%|RED|
| CASEN warm |200|236|+18,00%|RED|

40/40 LCP y FCP presentes; CLS máximo0,053783<=0,1; todos los LCP individuales<=2500ms. Cinco pares AB/BA por página y cold/warm; ninguna muestra excluida. El gate canónico validó binding y estructura y salió1 al detectar Avalúos warm>10%; summary.json conserva los tres grupos que incumplen.

Recogida terminada exit0. Receipt liga144fuentes,1248archivos del build candidato, settings, scripts y observaciones.20sesiones cerradas y servidores4041/4042cerrados;4004intacto. La fuente congelada sigue238221099b11ca45bc387d65fe90450397084927173ef75e808dfa36bc848b2a.

Los diez intervalos CPU10s varían22,5–54,6%; no se seleccionaron muestras por carga. Avalúos warm CPUmediana referencia30,3%/candidato48,3%; esto es confusión observada y no permite declarar que el100% de la regresión sea coste del producto.

La tanda previa formal-first-person sigue preservada con sus8ausentes. El intento inicial de este canary tuvo un defecto de concatenación de scripts, conservado y explicado en ../presentation-diagnosis/harness-incident.md; el canary recuperado entregó8/8 antes de lanzar esta tanda.

## Diagnóstico sin cambios de producto

CASEN cambió su candidato LCP de párrafo(~100914px²) a imagen(~534240px²), consistentemente5/5 por grupo. Eso explica que el objeto medido sea distinto, no exime del contrato. Hero nuevo74.248bytes y responseEnd mediana55,3ms cold/64,1ms warm: no hay evidencia de descarga tardía como único cuello. Avalúos hero156.080→161.742bytes, descarga warm mediana35,7→34,7ms; comprimir5.662bytes extra no tiene evidencia suficiente para explicar100ms.

main.css117.711→119.679bytes; transferencia warm mediana Aval20,6→21,1ms y CASEN25,6→27,2ms. La descarga CSS no explica por sí sola las diferencias, pero coste de estilo/layout/composición no está aislado. CASEN candidato solicita FiraSans-Medium155.208bytes adicional por título500, ausente en referencia; plausible coste que requiere canary propio. font-display ya es swap. FiraCode Nerd1.138.228bytes es deuda compartida, no prueba de regresión nueva.

CASEN cold fuentes finalizan alrededor941–964ms referencia frente1064–1100ms candidato; LCP984→1140. Correlación temporal compatible con trabajo de fuentes/layout, pero document.fonts.ready ocurre después del LCP y no demuestra bloqueo causal. Avalúos warm longtasks totales medianos221→264ms; CASEN warm256→252ms. Una atribución causal exclusiva a JavaScript tampoco sale de esas sumas.

Hipótesis prioritaria propuesta por root: índice Lunr síncrono en footer; lunr-store207.700→215.304bytes y el constructor recorre todo store. Prototipo interceptado en /tmp y canary acotado aparte podrán comparar la misma página con solo ese trabajo diferido. No hay optimización aprobada ni nuevo formal en este reporte.

Datos completos y contraejemplos por recurso: resource-diagnosis.json; raw startTime,paintTime,presentationTime,callbackAt,longtasks,fonts,CPU: runs.json. Los diagnósticos no sustituyen standardLCP.
