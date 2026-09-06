# Paleta nocturna: comparación leve del 6 de septiembre de 2026

Se aplica la candidata teal al cuerpo editorial: fondo de cabeceras de tabla
`#243b3b` y divisor de `h2` `#345d5d`. El texto mantiene `#f4f4f4`.
Evaluación local por el subagente de paleta; sin commit ni publicación.

## Fuente y alcance

- Tema real: `minimal-mistakes-jekyll` 4.28.1 (`Gemfile.lock:106`), skin `contrast` (`_config.yml:6`).
- Nocturno propio `academic-night`, inspirado explícitamente en Carbon Gray 100 (`assets/css/main.scss:282`); el acento existente es teal `#3ddbd9`.
- Activación por `data-theme`, con persistencia en `3cucharadas-theme` (`assets/js/theme-toggle.js:4`); el alias histórico `tokyo-night` se normaliza.
- Dos tokens nuevos (`assets/css/main.scss:310`), divisor editorial (`assets/css/main.scss:470`) y cabeceras de tabla (`assets/css/main.scss:1424`).
- Migración local de dos `mix()` a `color.mix()` (`assets/css/main.scss:2467`), con `@use "sass:color"` antes de reglas CSS (`assets/css/main.scss:6`).
- No cambian párrafos, tipografía, dimensiones, celdas, botones, foco, contenido, gradientes ni animaciones.

## Rúbrica fijada para las tres variantes

Contraste de texto normal ≥4,5:1 y grande ≥3:1, acento visible pero tenue en
cabeceras, identidad conservada, tema claro equivalente, teclado/foco preservados
y ausencia de nuevo desborde de documento. La preferencia estética queda subordinada
a esos requisitos. No se evalúa velocidad ni se afirma optimalidad global.

| Variante | Fondo cabecera / divisor h2 | Contraste cabecera | Juicio visual |
|---|---|---|---|
| Baseline | `#393939` / `#bfbfbf` | 10,50:1 | Legible; cabeceras y navegación repiten gris neutro |
| Teal, seleccionada | `#243b3b` / `#345d5d` | 10,83:1 | Introduce matiz tenue y continúa el turquesa de interacción existente |
| Ciruela, conservada como alternativa | `#3c303c` / `#624d61` | 11,36:1 | Legible y tenue; introduce otra familia cromática en el cuerpo |

La ciruela tiene algo más de contraste: se prefiere teal por continuidad cromática,
puesto que ambas superan ampliamente el mínimo. Es un juicio de diseño acotado,
no evidencia de preferencia de lectores. Ideal: validación perceptual con lectores;
óptimo factible aquí: una intervención de dos selectores, reversible y comprobada.

## Evidencia ejecutada

- Baseline proporcionado: `/tmp/3cucharadas-audit-fgDYyv/site-production`.
- Página: `/datos/python/territorio/avaluo-vulnerabilidad-unidad-vecinal/`, seis tablas; muestra medida de 23 cabeceras, 129 celdas, 9 títulos h2 y 67 párrafos.
- Navegador: `agent-browser`, sesión exclusiva `night-palette-20260906`, viewports 1280×900 y 390×900; puertos locales exclusivos 4187 y 4188.
- Comparación controlada: `/tmp/3c-health-palette-NuNzLO/compare.cjs`, `comparison.json` y `judgments.json`; baseline y dos candidatas con idéntico contenido y encuadre.
- Build real: `BUNDLE_PATH=vendor/bundle BUNDLE_FROZEN=true JEKYLL_ENV=production bundle exec jekyll build --disable-disk-cache --destination /tmp/3c-health-palette-NuNzLO/site`, exit 0; registro `build.log`.
- Validación del CSS compilado frente al baseline: `verify-final.cjs` y `final-verification.json`; exit 0, estilos claros medidos idénticos, cabeceras y divisores nuevos activos en ambas resoluciones.
- Tema claro: cabeceras blancas sobre rojo `#b71c1c`, 6,57:1 antes/después; cuerpo crema conservado.
- Texto nocturno de cuerpo y h2: `#f4f4f4` sobre `#161616`, 16,45:1; texto secundario `#c6c6c6`, 10,59:1.
- Divisor teal sobre fondo: 2,47:1; línea decorativa, sin información exclusiva ni función de control. La jerarquía continúa expresada por el título y su tamaño/peso.
- Teclado: primeras diez pulsaciones Tab con mismo elemento, etiqueta, foco visible, contorno y offset; `baseline-keyboard.json` idéntico a `final-keyboard.json`; Enter en el botón conmuta claro y vuelve a nocturno.
- Foco del conmutador: `#3ddbd9`, 3 px y offset 2 px; 11,26:1 sobre cabecera `#0f0f0f`, sin modificación.
- Sin desborde de documento: `documentElement.scrollWidth` ≤1280/390; las tablas anchas conservan su desplazamiento horizontal existente.
- Control negativo de contraste: `#3c3c3c` sobre `#393939` devuelve 1,047:1 y falla el umbral; las tres variantes reales lo superan.
- `git diff --check` sin errores; build conserva advertencias de `@import`, fuera de la migración puntual de `mix()`.

## Capturas inspeccionadas

Todas en `/tmp/3c-health-palette-NuNzLO/`; las capturas nocturnas enumeradas,
el tema claro final y el foco se revisaron con `view_image`. Son evidencia
efímera local, sin cargar imágenes al repositorio.

| Variante | Escritorio | Móvil |
|---|---|---|
| Baseline | `baseline-academic-night-1280.png` | `baseline-academic-night-390.png` |
| Teal | `teal-academic-night-1280.png` | `teal-academic-night-390.png` |
| Ciruela | `plum-academic-night-1280.png` | `plum-academic-night-390.png` |
| Compilado final | `final-compiled-academic-night-1280.png` | `final-compiled-academic-night-390.png` |
| Tema claro final | `final-compiled-light-1280.png` | `final-compiled-light-390.png` |

Foco real: `final-keyboard-focus.png`. Se conservan además las capturas claras
de todas las variantes y sus hojas CSS de comparación.

## Incidentes, contraejemplos y límites

- El sandbox impidió inicialmente abrir el puerto local; el preview funcionó con la escalación acotada al servidor local.
- Las primeras comparaciones dieron falsas diferencias claras y de foco por transiciones CSS heredadas de 200–750 ms; las mediciones válidas esperan su término y fijan scroll instantáneo.
- Una espera por promesas de animación agotó el tiempo CDP; se sustituyó por espera diagnóstica de 1000 ms. La conmutación final usa el botón real para mantener sincronizadas sus etiquetas.
- La sesión permitió únicamente recursos de `127.0.0.1`; recursos externos, incluidos iconos de Font Awesome, no aparecen en las capturas. Esta limitación afecta por igual al baseline y a la candidata.
- El servidor local registró `ConnectionResetError` cuando el navegador interrumpió una descarga MP4 al navegar; no se evaluó reproducción de video en este subencargo.
- El contraste es un HECHO calculado desde estilos computados; la continuidad estética es una INFERENCIA; preferencia de lectores y rendimiento son NO VERIFICADOS.
- Se revisó un post representativo en dos anchos y un navegador; no es una auditoría WCAG integral del sitio ni una validación de lectores de pantalla.
- Autorrevisión con rúbrica de `improvement-judge` y cierre de `auditoria-critica`; riesgo residual bajo para el alcance CSS, sin afirmar independencia de autor y juez.
- Reversión: quitar los dos tokens y regla h2, y devolver la cabecera a `var(--night-layer-strong)`; la migración equivalente `color.mix()` puede conservarse.
- Cierre operativo: sesión de navegador propia y ambos servidores locales cerrados; los servidores terminaron con exit 0 tras interrupción controlada.

| Estado | Resultado |
|---|---|
| Implementado | Paleta teal leve, migración Sass puntual, build y comparación visual/contraste/teclado |
| Parcial | — |
| No implementado | Publicación y validación global del sitio, fuera de este subencargo |
