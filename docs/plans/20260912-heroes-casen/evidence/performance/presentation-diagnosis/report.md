# Diagnóstico de presentación, 2026-09-12

Estado: diagnóstico local; no aceptación de rendimiento del producto. Se conservaron los 40 resultados formales previos, incluidos ocho LCP ausentes y la regresión warm de Avalúos. Ningún producto, dato o arnés formal editado. Los únicos procesos propios fueron canaries aislados y servidor4044, ya cerrados;4004 y sesiones ajenas intactos.

## Hechos observados

| Ensayo | LCP estándar inmediato, ms | Control retrasado3s, ms | Lectura limitada |
|---|---|---|---|
| agent-browser0.33.2, Chrome151 headless, polling inicial | cold ausente; warm4056; paint41.8 | cold ausente; warm4108 | El HTML mínimo reproduce la anomalía sin app, fuentes web ni longtasks |
| agent-browser0.33.2, Chrome151 headed inicial | cold ausente; warm4836; paint28.5 | cold3088; warm3060 | Headed por sí solo no corrige; cold late registró INP120 sin input automatizado, no es evidencia limpia de aceptación |
| agent-browser headless, espera pasiva inicial | cold68; warm52 | No ensayado | Recuperación temporal, luego contradicha |
| agent-browser headless, screenshot diagnóstico | cold84; warm56 | No ensayado | Captura es intervención; no se usa para aceptación |
| agent-browser repetición ABBA, cold | polling96; pasiva ausente; pasiva80; polling88 | No ensayado | Refuta que eliminar polling sea suficiente o que polling sea condición necesaria |
| Playwright local, Chromium152.0.7977.8 fijado | cold56; warm36 | cold3032; warm3028 | Cuatro observaciones completas, control negativo visible |
| Playwright local, mismo Chrome151.0.7922.77 | cold60; warm48 | cold3040; warm3032 | Cuatro observaciones completas sin cambiar versión del navegador |

Todos los valores usan el último PerformanceObserver de largest-contentful-paint.startTime en una ventana congelada a5000ms. Nunca se imputó un ausente ni se sustituyó por paintTime. Todas las páginas declararon visible/focused. El modo headed se corrobora por UA runtime Chrome/151 frente a HeadlessChrome/151 sin override de UA; DISPLAY y WAYLAND_DISPLAY estaban definidos. Esto no prueba presentación física continua ni excluye interacción humana; no se logró vincular argv del proceso a cada sesión, por lo que los flags observados de otros Chrome no acreditan el lanzamiento canary.

El HTML fast tiene únicamente estilo inline y h1; late agrega un h1 mayor con setTimeout3000. El servidor stdlib tuvo revalidaciones304 warm y favicon404: estos canaries no son equivalentes a la política no-store formal y no son medición de los builds. Los canaries Playwright usan la librería fijada de penta-agent/tools/playwright-local-mcp y su executablePath; también se ejecutó el binario exacto Chrome151 de agent-browser. El uso directo del módulo Node fue el fallback expresamente solicitado por root, sin instalación. No se lanzó el servidor MCP porque el experimento requería un único proceso Node y contexto explícito.

## Hipótesis comparadas y falsación

| Hipótesis | Evidencia discriminante actual | Condición de descarte o próximo control |
|---|---|---|
| La app o nueva imagen es condición necesaria del fallo | Refutada por missing y4056ms en h1 mínimo sin recursos externos | Ya descartada como explicación necesaria; una regresión adicional del producto aún puede coexistir |
| wait--fn impide presentar y espera pasiva basta | Refutada por pasiva missing y polling88–96ms en ABBA | Ya descartada en esa forma fuerte; no se excluyen otras diferencias del driver |
| Solo nuevo headless causa el problema | Debilitada: headed también missing/4836; runtime UA cambia | No basta cambiar --headed; probar backend de presentación requeriría trazas de compositor y vínculo exacto de proceso |
| Pipeline de presentación/feedback o combinación driver/configuración/entorno intermitente | Favorecida provisionalmente por paint41.8 frente a presentación4056 sin longtasks, ambos modos; PW con mismo151 no reproduce en4navegaciones | Descartar una causa exclusiva de agent-browser si PW mismo151 reproduce en ensayos alternados; distinguir raster real de feedback con traza compositor/Viz y CPU por hilo |
| CPU/GPU/raster del host introduce retraso real | No excluida: CPU media no descarta un hilo saturado, GPU o bloqueo de presentación; no medimos CPU de estos canaries | Razonar causalmente exige cargas comparables, trazas y ensayos alternados; no basta el promedio38% ni paintTime temprano |
| Retraso de entrega de callbacks JS explica toda la brecha | Debilitada: formal callback llega~2ms después de presentationTime, no~4s después de timestamp temprano; h1 mínimo sin longtasks | Una traza que muestre presentación temprana y callback tardío la rehabilitaría; actual API no lo demuestra |

## Fuentes primarias consultadas

- [MDN paintTime](https://developer.mozilla.org/en-US/docs/Web/API/LargestContentfulPaint/paintTime): inicio de pintura tras fase de rendering, no promesa de píxeles presentados.
- [MDN presentationTime](https://developer.mozilla.org/en-US/docs/Web/API/LargestContentfulPaint/presentationTime): momento de presentación según implementación.
- [Agent-browser0.33.2 chrome.rs](https://github.com/vercel-labs/agent-browser/blob/v0.33.2/cli/src/native/cdp/chrome.rs): build_chrome_args usa headless=new, disable-backgrounding-occluded-windows y enable-unsafe-swiftshader; no implica que todo rendering sea software ni acredita argv efectivo de nuestras sesiones.
- [Agent-browser0.33.2 actions.rs](https://github.com/vercel-labs/agent-browser/blob/v0.33.2/cli/src/native/actions.rs): wait--fn delega a poll_until_true; sesión informa motor/hash, no configura un reemplazo de LCP.
- [Playwright browsers](https://playwright.dev/docs/browsers#chromium-new-headless-mode): headless shell y Chrome completo son implementaciones diferentes; por eso se incluyó mismoChrome151.
- [CDP HeadlessExperimental](https://chromedevtools.github.io/devtools-protocol/tot/HeadlessExperimental/): beginFrame requiere target con BeginFrameControl; no se aplicó a un target ordinario ni se presume soportado.

## Recomendación y límites

1. Mantener el resultado formal previo como rojo/incompleto con evidencia preservada.
2. Probar un par baseline/candidate congelados con Playwright local y mismoChrome151: observers simples pre-navegación, sin captura/rAF/input, espera pasiva y ventana5000ms, timeOrigin único, scope loopback, viewport1440×1000 DPR1, media light, no-store idéntico, CPU y hashes. Esta pareja aún no se ejecutó aquí.
3. Si no hay missing y el control rápido/tardío funciona antes y después, congelar contrato de medición revisado y ejecutar los cinco pares completos AB/BA por página y temperatura para ambos builds. Conservar <=2500ms y <=10% y el CLS exigido; no seleccionar muestras por resultado o carga.
4. Si vuelve a fallar el canary con mismo151, detener aceptación y recoger una traza acotada compositor/Viz de fast canary; screenshot/framepump siguen siendo intervenciones diagnósticas, no optimización del producto.

No se demuestra una causa exclusiva ni optimalidad del setup con8navegaciones. La comparación Playwright cambia launchflags, driver e instrumentación y ocurrió después, por lo que aún existe confusión temporal. Las capturas fueron inspeccionadas: h1 negro legible sobre fondo blanco; no prueban cuándo se presentó por primera vez.

## Reproducción acotada

Desde la raíz del blog, en una terminal propia: `python3 -m http.server 4044 --bind 127.0.0.1 --directory docs/plans/20260912-heroes-casen/evidence/performance/presentation-diagnosis`.
En otra: `node docs/plans/20260912-heroes-casen/evidence/performance/presentation-diagnosis/playwright_canary.mjs` (8navegaciones,~45s, cierra sus contextos/browsers).
Control rojo: `python3 docs/plans/20260912-heroes-casen/evidence/performance/presentation-diagnosis/check_canary.py late` dio exit1.
Recuperación verde: mismo comando con `fast` dio exit0. No usar la salida verde para aprobar los builds.
Cerrar únicamente el servidor4044 propio con Ctrl-C. No cerrar servicios ajenos.
