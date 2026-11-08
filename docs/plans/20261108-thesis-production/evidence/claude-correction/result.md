REVIEW_VERDICT: REQUEST_CHANGES

Hay un defecto geométrico de la misma clase que motivó la corrección: texto que toca o cruza el marco de los ejes. Está en la Figura 1 de IV, es visible en la captura y en el PDF, y ningún guard lo detecta. Es una corrección acotada. El resto del conjunto no tiene bloqueos adicionales dentro del alcance que revisé.

## Hallazgos

- **[ALTA] `352_post4_visuals.py:436-437,456` → el rótulo del peldaño 1 de Fig. 1 cruza el borde superior de cada panel.** El rótulo va en `y_pos[0]+2.12 = 13,32` con `va="center"`, y `ylim` termina en `13,5`. Con la fuente en 15 pt, la mitad de la altura del texto sobrepasa el marco. Se ve en `curated/iv-article-en-light-1440-fig-post4-1.png`, en `pdf-figure1-final.png` y en la captura móvil oscura. Corrección: subir el techo de `ylim` o bajar el rótulo, y comprobarlo en las cuatro variantes de tema e idioma. Evidencia: observación en tres capturas más el cálculo desde el código.
- **[ALTA, confianza media] `352_post4_visuals.py:810-812` → la etiqueta ámbar `−0,1` / `−0.1` ("Se matricula"/"Applies", panel B causal) llega al borde superior.** Va en `group_max+2,0 = 6,3` con `va="bottom"` y fuente de 15 pt, bajo un `ylim` superior de `7,5`. En la captura ES oscuro 1440 aparece pegada o cruzando el marco. No calculé el bbox; solo lo vi en la imagen, así que falta confirmarlo.
- **[ALTA] Cobertura de los dos guards → el marco de los ejes no es una marca registrada.** `_assert_visual_geometry` y `measureFigureGeometry` solo comparan etiquetas con barras, CI, puntos y líneas GATE. Espinas, rejilla y título quedan fuera. Corrección: registrar los cuatro bordes del `axes` como marcas en ambos guards y agregar un fixture negativo con un rótulo montado sobre el borde. Hoy el "64/64 PASS" es compatible con los dos defectos anteriores; que haya tres evidencias visuales de uno de ellos descarta que el verde pruebe legibilidad total.
- **[MEDIA] `fixture-svg-own-bar-overlap.json` → el fixture "barra propia" no discrimina.** Con la barra propia `causal-paes-bar-1-2` solo hay 1,93 px de solape vertical, contra un umbral de 1,5 px. Además dispara `causal-paes-bar-0-2`, una barra vecina, con 4,44×16,94 px. El fixture fallaría igual si la detección de barra propia estuviera rota. Corrección: mutar sobre una barra de altura apreciable. En el generador no hay mutante equivalente: son cuatro flags, y la cobertura de barra propia y vecina depende de `tests/test_post4_visual_geometry.py:36-52`, que no ejecuté.
- **[MEDIA] `352_post4_visuals.py:234,247,229-241` → queda una vía de excepción muerta y un docstring que miente.** El parámetro `allowed` sigue aceptándose y el docstring aún dice "bar labels may sit inside their own bars". Ningún llamador que vi lo usa (el grep solo lo encuentra en las líneas 234 y 247). Corrección: eliminarlos, para que la excepción que ocultó las 16 colisiones no pueda reintroducirse.
- **[MEDIA] Asociación de lectura, sin cruce → lectura frágil que dependen del color.**
  - En Fig. 1, cada CI queda debajo de su valor pero encima del título del peldaño siguiente. Por proximidad, ese título parece pertenecer al CI de arriba.
  - En el panel B causal, los valores ámbar flotan en un carril superior, lejos de barras casi nulas, y quedan pegados sobre los verdes.
  - En G1 móvil, `−12.3` y `−11.5` casi se tocan. No se intersectan, pero se leen como un par. Se distinguen solo por el color de la serie.
  - Corrección sugerida: separar los dos rótulos de G1 en vertical.
- **[BAJA] Guard del generador frente al de Playwright → no miden igual.** El del generador usa `box.overlaps` estricto y registra las marcas de cero de Fig. 1 (30 marcas). El de Playwright usa tolerancias de 2 px y 1,5 px, y registra solo `ci` y `point` (10+10). La medición de Playwright se hace con el SVG inyectado en el DOM, no desde `<img>`. No verifiqué si las fuentes incrustadas producen métricas idénticas.
- **[BAJA] Recibo funcional `post4-browser-*` → no vincula los SVG finales.** Su manifiesto es `45c26e…`; el actual de `assets/images/tesis-post4/manifest.json` es `fe602d8d…`. Esto coincide con lo que declararon. Como las correcciones de arriba cambiarán los SVG, hay que repetir también esa corrida.
- **[BAJA] Prosa IV ES (diff) → dos detalles menores.**
  - La serie 2009–2022 cita `−2,64` para 2016–2019 sin intervalo, en un párrafo cuyo propósito es mostrar incertidumbre.
  - El panorama longitudinal es visible desde el inicio solo como texto. La figura 2 está únicamente en el anexo.
- **[BAJA] `pdf-figure1-final.png` → espacio sobrante en el pie de figura.** Dice "(CSV) ." con un espacio antes del punto.

## Separación epistémica

- **HECHO**
  - Los 74 hashes de `inputs-before.json` coinciden (74/0 con diferencias).
  - El PDF final tiene SHA `b4e6df4e…`, igual al declarado.
  - Las 5 fixtures negativas están en `EXPECTED_FAIL` con `svg-label-geometry`.
  - `lang="es"` y `lang="en"` están presentes en `_site`, así que `hyphens:auto` aplica.
  - El chequeo de justificación evalúa todo `article p`.
  - Fig. 1 y el panel B causal muestran etiquetas tocando el marco, y el generador las posiciona en `y=13,32` y `y=6,3` (arriba).
- **DEDUCTIVO**
  - Una comprobación que no registra el marco ⊢ no puede acreditar la ausencia de cruces con el marco.
  - Un fixture que falla igual sin la capacidad probada ⊢ no la prueba.
- **INDUCTIVO**
  - Tres omisiones seguidas (colisión con barra vecina, barra propia, línea GATE) nacieron de marcas no registradas. El marco es la siguiente de esa serie.
- **ABDUCTIVO**
  - H1: el `ylim` se fijó sin margen para el texto agrandado por `_readable_text` (13–15 pt). H2: es una decisión de diseño intencional.
  - Evidencia discriminante: tras subir el `ylim`, el rótulo debe quedar dentro del marco en las cuatro variantes.
  - Descarte de H1: si con margen sigue tocando, la causa es otra.
- **NO VERIFICADO / ALCANCE**
  - No ejecuté Playwright ni el generador, ni pytest.
  - Vi 6 de 8 capturas curadas; no abrí `iv-article-es-academic-night-1440` ni `iv-article-es-light-320`.
  - Leí completos el generador (secciones relevantes), los detectores y el diff del post IV ES.
  - No revisé el post III, los anexos III/IV, la paridad numérica ES/EN, referencias ni los 494 enlaces. Declaro esa parte sin revisar.
  - Tampoco inspeccioné el CSS más allá del diff, ni verifiqué visualmente fondos locales del canvas SVG.

## Riesgos residuales tras corregir

- Justificación con `hyphens:auto` a 320 px puede formar espacios irregulares. No es verificable con el recibo.
- El detector sigue sin comparar pares sin rol (título, ticks, leyenda), tal como declararon.

PLAN_STATE v2: pb-20261108T003705315Z-fc127547 rev14. P4/D9: revisión adversarial entregada con REQUEST_CHANGES. Bloqueos: marco de ejes en Fig. 1 y panel B causal (los tres hallazgos [ALTA]). Pendientes: fixture de barra propia, limpieza de `allowed`, repetir recibo funcional. D9 sigue activo hasta registrar una aprobación sobre el conjunto corregido.

HANDOFF-TRACE: Claude Code → Codex; revisión adversarial de solo lectura. No edité, no hice commit, push ni difusión. No escribí el archivo de plan.

MODEL-REPORT: sonnet (claude-sonnet-5-5), revisión de solo lectura, sin subagentes.
