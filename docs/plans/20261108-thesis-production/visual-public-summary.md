> Revisión anterior, superada por observación humana: 64/64 solo acreditaba los checks entonces implementados. No medía cruces de rótulos con marcas; no aprueba la corrección actual.

# QA visual pública: posts III y IV

**Estado del despliegue 1959f659, anterior a la corrección editorial y geométrica solicitada después:** matriz pública `visual-production-public-final.json` y copia `visual-production-public.json`: **64/64 combinaciones PASS**. Este resultado no acredita los cambios de justificación ni el rediseño posterior de la figura 1; requieren build, QA y despliegue nuevos. La primera matriz pública se conserva en `visual-public-before-abort-classification.json`: 63/64 filas pasaron; el único fallo clasificó dos abortos de SVG móviles **inactivos** en escritorio como errores de red. Las figuras activas terminaron cargadas, sin errores de imagen ni de variante. El detector corregido separa esos abortos transitorios y sigue fallando ante recursos activos rotos.

## Cobertura y evidencia

- Ocho rutas públicas: artículo y anexo III/IV en español e inglés; temas claro y oscuro; anchos de 320, 390, 768 y 1.440 px.
- Matriz final: 64 filas, 0 fallos, 16.088 muestras de texto directo, contraste CSS mínimo 5,73:1, contraste SVG mínimo 4,67:1 y texto SVG renderizado mínimo 10,28 px. `uncertainBackgrounds=0`, 0 imágenes incompletas y 0 abortos transitorios observados.
- Primera matriz: 64 filas, 96 capturas, mismos mínimos visuales; una fila falló por los abortos inactivos descritos arriba. La ejecución final del contrato no solicitó nuevas capturas: las cuatro muestras conservadas provienen de esa primera matriz sobre el mismo despliegue público.
- Falsación de contraste sobre DOM público: `visual-public-falsification.json`; base sin fallos, mutante blanco sobre blanco con ratio 1:1, salida 1 (`EXPECTED_FAIL`).
- Falsación de recurso activo sobre red pública: `visual-public-active-svg-falsification.json`; base sin fallos, SVG móvil activo interceptado, imagen incompleta y salida 1 (`EXPECTED_FAIL`).
- Cuatro capturas públicas representativas: `visual-public-iii-article-es-dark-mobile.png`, `visual-public-iii-annex-en-light-figure-mobile.png`, `visual-public-iv-article-en-light-desktop.png` y `visual-public-iv-annex-es-dark-figure-mobile.png`. Inspección visual: títulos, leyendas y figuras legibles en esas cuatro muestras; no se observó recorte.

## Límites del alcance

- `.page__title` de los cuatro artículos sí tiene texto directo y entra al muestreo CSS. El cálculo usa el fondo CSS sólido del hero; no calcula el contraste por píxel frente a la imagen y su sombra degradada. Las capturas representativas complementan esa medición, sin certificar todos los píxeles del bitmap.
- El contraste de cada etiqueta SVG se compara con el canvas raíz `patch_1`. Los fondos locales de paneles y leyendas no se resuelven por etiqueta; por eso el mínimo SVG informado no es una certificación completa de cada subpanel.
- El contraste CSS compone colores declarados del texto y los ancestros. `uncertainBackgrounds=0` significa que el detector no halló fondos CSS ambiguos en las muestras; no prueba que toda combinación visual de un bitmap sea accesible.
- Las cuatro capturas inspeccionadas son una muestra; la matriz automatizada cubre todas las 64 combinaciones y verifica además carga de imágenes, fuente efectiva, desbordes, consola y red.

La difusión externa sigue fuera de este QA.

## Corrección posterior en curso

Playwright midió la figura 1 IV en el preview previo al cambio: ancho de imagen 288/358/620/620 px frente a columna de 288/358/732/796 px a viewport de 320/390/768/1.440 px. El límite `--measure: 62ch` explicaba el ancho fijo de 620 px en tablet y escritorio. El CSS nuevo usa toda la columna disponible y el SVG fue regenerado.

El build corregido local pasó el gate funcional III 32/32 e IV 32/32; las 64 filas mostraron todos sus párrafos justificados y la razón de ancho de la figura 1 fue 1 en las 16 variantes del artículo IV. NoJS y print pasaron 8/8 cada uno. Los dos guardias nuevos se vieron en rojo mediante DOM real (`post3-unjustified-red.json`, `post4-narrow-figure-red.json`), ambos con salida 1. Recibos en `evidence/figure-correction/`. La matriz visual nueva y la comprobación pública después del próximo despliegue son independientes y siguen pendientes aquí.
