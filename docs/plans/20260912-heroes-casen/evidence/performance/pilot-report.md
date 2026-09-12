# Piloto local de rendimiento Q1 — diagnóstico

| Página / condición | LCP baseline → candidato | Lectura diagnóstica |
|---|---|---|
| Avalúos II / frío | ausente → ausente | LCP no entregado dentro de ventana de 5 s; no se imputa cero. |
| Avalúos II / caliente | 3928 → 3636 ms | −7,43%; ambos superan 2500 ms. |
| CASEN largo / frío | 984 → 2024 ms | +105,69%; supera margen de regresión del 10%. |
| CASEN largo / caliente | 364 → 716 ms | +96,70%; supera margen de regresión del 10%. |

- Una pareja por página y condición: ocho navegaciones, seis LCP observados y dos ausentes. No constituye las cinco parejas formales ni acepta el candidato final.
- CLS por ventana máximo observado: baseline 0,01454; candidato 0,02305. Los ocho CLS observados son menores que 0,1; `cls-availability.json` los separa de LCP ausente.
- En CASEN el elemento LCP cambia de párrafo del baseline a la imagen hero candidata. El cambio de elemento es observado; una pareja no establece regresión estable ni atribuye causalidad.
- La carga del host al iniciar navegaciones osciló entre 8,45 y 9,66 (load average de un minuto, ocho hilos disponibles). Se conserva por navegación; no se atribuye la latencia a esa carga sin comprobación discriminante.

## Condiciones y límites

- Chrome for Testing 151.0.7922.77, agent-browser 0.33.2, headless Linux del host; 1440×1000 CSS, DPR 1, tema claro, sin throttling de CPU ni red. No representa teléfono ni conexión real de usuarios.
- Servidor canónico idéntico `scripts/catastro_sii/serve_range_static.mjs`, puertos 4041 y 4042, overlay explícito vacío. Cabeceras reales `Cache-Control: no-store` verificadas.
- Frío: proceso/sesión aislada nueva por página/build/pareja, sin perfil/restauración. No se vació caché de disco del sistema operativo. Caliente: segunda navegación mediante reload del mismo navegador, sin afirmar hit de caché HTTP.
- Baseline `/tmp/3c-heroes-baseline-site`; candidato de piloto `/tmp/3c-heroes-cardfix-site`. El candidato final todavía no está integrado. HTML y recursos efectivamente solicitados tienen SHA en settings/runs.
- Orden contrabalanceado AB en Avalúos y BA en CASEN; en cada build frío y luego caliente. Ventana fija de 5000 ms desde init, captura real 5029–5100 ms aprox., sin interacción ni scroll.
- Solo localhost permitido mediante allowed-domains; peticiones externas bloqueadas. Esto es un ensayo local controlado, no tráfico público ni publicación.

## Medidor y errores preservados

- Se inspeccionó el script de vitals embebido en el binario instalado y se extrajo exactamente a `embedded-vitals-init.js`, con hash del binario y del script en settings. Usa PerformanceObserver buffered para LCP y suma de layout-shift sin interacción para CLS bruto.
- `measurement-init.js` recoge entradas completas y congela métricas a los cinco segundos. El arnés añade CLS por ventana (separación máxima de 1 s entre entradas y duración máxima de 5 s) y conserva también la suma bruta. Las entradas y fuentes están disponibles para revisar el cálculo.
- La guía instalada anuncia `addinitscript`, pero el parser devolvió Unknown command antes de navegar. Se conservó el fallo y doctor; se recuperó con los flags soportados `--init-script`.
- `agent-browser vitals` sin URL recarga la página: el control comparó performance.timeOrigin antes/después y rechazó tres muestras registradas, dejando el intento interrumpido en `pilot/`. Ninguna se usó en el resultado diagnóstico. La continuación interrumpida permanece en el log.
- El piloto válido usa agent-browser como navegador y eval como lectura del observer previamente instalado; no llama al comando vitals. Verifica URL, tamaño, visibilidad, h1, estado de carga y timeOrigin inalterado.
- Los controles deterministas observados rechazan regresión, exceso absoluto y dato ausente, y verifican recuperación verde/ventanas CLS (`measurement-controls.json`). Validan predicados, no sustituyen evidencia de rendimiento.

## Reproducción

1. Servir ambos builds con el mismo script canónico y overlay vacío, en 4041/4042.
2. Ejecutar `python3 run_performance.py --candidate-root <build-final-congelado> --pairs 5 --label formal --output <directorio-nuevo>`; conservar scripts init junto al arnés.
3. Revisar faltantes y medianas por página y condición, no mezclar frío/caliente. Exigir candidato mediana LCP ≤2500 ms y ≤110% baseline; CLS ≤0,1. No ocultar baseline fuera de umbral.
4. Cerrar sesiones y servidores propios. Para revertir el arnés, retirar únicamente estos archivos de evidencia o /tmp; no modifica producto.

Las sesiones de medida y la sesión de prueba fueron cerradas por nombre. Servidores propios 4041/4042 cerrados. Pendiente candidato final del agente raíz y autorización operativa para las cinco parejas ya previstas; no se iniciaron anticipadamente.
