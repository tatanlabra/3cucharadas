# Incidente en primer canary Playwright de producto

El primer intento product-canary conservó8navegaciones inválidas: el nuevo arnés concatenaba el IIFE de embedded-vitals-init.js, terminado en `})()`, con el siguiente IIFE sin punto y coma. JavaScript lo interpretó como otra llamada al resultado undefined: el observador __PERF_MEASUREMENT__ y su snapshot no se instalaron. No son ausencias de LCP atribuibles al navegador.

La reproducción independiente ejecuta los dos scripts reales en un contexto VM mínimo: verify-init-separator.mjs observa TypeError y registered=false con el separador original, y registered=true sin error al introducir `;`. Evidencia init-separator-red-green.json. La prueba usa stubs de entorno para aislar sintaxis de ejecución; la recuperación del navegador se recoge separadamente en product-canary-recovery.

Se preservó el arnés fallido en product-canary/run-failed.mjs y su hash original en settings.json; el arnés activo formal-playwright/run.mjs usa separador explícito y captura pageerror. El intento fallido cerró4contextos/browsers y ambos servidores propios. No cambió ningún script de producto ni el arnés formal-first-person.
