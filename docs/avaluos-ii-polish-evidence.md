# Avalúos II: revisión local del 10 de septiembre de 2026

Preparación local, sin push ni publicación. Contrato: `avaluos-ii-polish-contract.yaml`.
Baselines: blog `e986f238`, análisis `32c6fa3`. Los datos crudos se conservaron.

## Resultado analítico y editorial

El criterio estricto combina tipo de vivienda aceptable y materiales aceptables
en paredes, techo y piso. Hay 5.774.146 casos entre 6.408.172 viviendas particulares
ocupadas con moradores presentes. La proporción de cada comuna se transfiere al
residuo sólo como escenario: 1.318.681,81 equivalentes aceptables y 198.007,19 de
otras condiciones reconstruyen el residuo de 1.516.689; el descuento supuesto
de campamentos suma 71.760 y la diferencia positiva inicial 1.588.449.

La precedencia de no respuesta del código INE corrige 73.338 a 72.642 viviendas
irrecuperables; no modifica la brecha ni el descuento de campamentos. Tres casos
adversariales reprodujeron el error. Build, auditoría de fuentes y 53 pruebas
analíticas posteriores aprobaron. El JSON, CSV y Parquet públicos concilian.

Se incorporan mediana, media y proporción de avalúos habitacionales observados
sobre $60.030.710, umbral oficial del período 2026S1. Los dos borradores muestran
las 15 comunas con residuo positivo y mediana superior a ese valor. No se traslada
la distribución de avalúos a las viviendas sin enlace ni se cruza como probabilidad
con materialidad. El neto tributario habitacional sigue sin conciliar:
`fiscal_status=blocked_components`; los escenarios monetarios permanecen nulos.

Fuentes, alcance de lectura y contraevidencia: `avaluos-ii-editorial-evidence.md`.
La hipótesis útil es prioridad para revisión predial; se refuta para cada caso si
ya está correctamente registrado, pertenece a otro universo o carece de obligación
exigible. Geometrías yuxtapuestas tampoco demuestran un inmueble omitido.

## Interfaz y rendimiento medidos

| Elemento | Antes | Después | Alcance |
|---|---:|---:|---|
| Grilla de indicadores a 390 px | 1.241,5 px | 663 px | Misma información, sin desborde |
| Grilla de indicadores a 1440 px | 495,28 px | 382 px | Misma información |
| Primer selector Chile, frío | 2.342 ms | 900 ms | Una observación local por versión |
| Selector Chile, recarga | 1.099 ms | 592 ms | Misma sesión con caché HTTP |
| Peticiones de comunas | 2 | 1 | Datos y parseo compartidos |
| Mapa completo, frío | 2.342 ms | 10.175 ms | Resultado peor; no demuestra aceleración global |
| Texto secundario claro sobre blanco | 6,27:1 | 7,56:1 | Contraste de los tokens usados |
| Hover Teno/Quinta de Tilcoco, 1280 px | 187,78/203,50 px | 223,656/223,656 px | 343 etiquetas verificadas |

Los detalles de carga, caché, fallos de motor y WebGL y recuperación están en
`catastro-viewer-loading-20260910.md`. No se atribuye la espera del mapa a una sola
causa: falta separar origen remoto, worker, GPU y carga del host.

Se conserva ECharts porque ya sostiene los gráficos SVG del visor y comparte
tema, tooltip y accesibilidad; añadir React u otro motor no retira su coste.
La paleta clara se revisó de nuevo por preferencia explícita del usuario: colores
luminosos próximos al modo nocturno, con contornos contrastantes, etiquetas y
patrones. La afirmación inicial de contraste >=3 para cada relleno ya no describe
esa segunda paleta; el criterio pasa a la identificación de bordes y texto.

QA observada: tooltip de Valparaíso con todos los componentes y advertencia;
clic selecciona comuna 5101 y actualiza mediana, promedio y proporción. Con
`prefers-reduced-motion`, el valor final está presente y no aparecen carretes.
Con peticiones de scripts externos bloqueadas, la tabla conserva 346 filas y
el SVG estático permanece accesible; el gráfico puede desplazarse horizontalmente.
El fondo de ese SVG cambia con el tema. No equivale a certificar todos los casos
de JavaScript deshabilitado en cada navegador.

Axe no detectó infracciones en la sección de brecha ni en los indicadores medidos;
quedaron contrastes inconclusos sobre SVG y gradientes, revisados mediante capturas
y cálculo de tokens. Esta comprobación acotada no certifica accesibilidad del sitio
completo. El desborde adicional a 320 px provenía de enlaces con `nowrap`, corregido
permitiendo salto de línea; pendiente comprobación del build definitivo.

## Validación y reapertura por peticiones adicionales

La primera validación integral falló en dos fixtures de accesibilidad sin `dataset`.
La recuperación añadió un DOM simulado fiel y eventos explícitos; se verifican
`style.load` independiente de `load` y limpieza ante timeout del estilo. La segunda
validación integral pasó: 127 pruebas TS; 52 pruebas Python ejecutadas, de las cuales
45 aprobaron y 7 se omitieron por dependencias geoespaciales; TypeScript, CSS, Vite,
Jekyll y verificación del artefacto aprobados. Los omitidos no cuentan como aprobados.

Después el usuario pidió cascada de cifras más lenta, nueva paleta y dos mapas.
Estos cambios reabren su validación: el cierre definitivo y sus pruebas se registran
abajo al terminar, sin presentar el resultado anterior como prueba del código nuevo.

## Cierre de código y verificación, 11 de septiembre

La cascada final tiene nueve pruebas específicas verdes: una cifra a la vez,
850–1.090 ms, umbral visible 55% y margen inferior negativo. El navegador confirmó
orden de lectura, máximo una animación concurrente y limpieza al salir; sin
IntersectionObserver queda estática. Los valores exactos nunca esperan la cola.

La paleta final clara usa turquesa `#56BDB9`, azul grisáceo `#99ABC2` y ámbar
`#EFB35F`; contorno `#40566E`. El oscuro conserva sus tres tonos y usa contorno
`#61758F`. Las etiquetas son independientes del relleno y se mantienen los patrones.
No se presenta esta preferencia visual como una optimalidad universal.

Los mapas finales de Valparaíso y Puerto Montt tienen PNG de 1800×1350 en ambos
temas y previews WebP de 900/1800 px. Cada preview móvil pesa 97–98 KB; cada PNG,
1–1,2 MB. Navegación nueva comprobó cero peticiones de mapas antes del anexo, sólo
dos WebP claros al entrar y descarga de variantes oscuras al cambiar tema.
Se conserva PNG para ampliación. El recorte de Puerto Montt prioriza ciudad y
periferia; Alerce aparece sólo en el contexto de unidades vecinales.

La plantilla Matplotlib fue recuperada de la sesión del 24-07-2026; renderer,
insumos y caso negativo están documentados en el repositorio analítico,
`v5_brecha/docs/avaluos-ii-annex-maps.md`. Un CUT top2 alterado sólo en memoria
se rechazó antes de crear salida. Un SHA de PNG alterado en una copia temporal
de `maps-audit.json` también se rechazó; el conjunto real recuperó verde.
El manifiesto público contiene únicamente procedencia y conteos agregados.

La última integral pasó 132 pruebas TS, 45 Python y 7 omitidas. Las 53 pruebas
analíticas y el renderer geoespacial se comprobaron separadamente. Los borradores
ES/EN se construyeron con `--drafts --unpublished`; se verificaron cifras clave,
tablas, gráficos y enlaces al anexo. `verify_site_artifact.rb` aprobó también
ese build, y el registro visual estricto terminó sin avisos.

El anexo quedó con fondo uniforme y margen de llegada bajo la navegación fija:
axe en claro informó cero infracciones y cero inconclusos. En el resto del alcance
permanecen los contrastes SVG/gradientes inconclusos descritos antes; no se extrapola
la comprobación del anexo a una certificación global. A 320 px no hay desborde.
El visor renderizado contiene una sola definición del código H.

Comandos de reproducción: `scripts/catastro_sii/validate_build.sh` con Node de
`.nvmrc`, `python3 scripts/catastro_sii/project_fiscal_gap.py`,
`python3 scripts/catastro_sii/verify_fiscal_gap.py`,
`ruby scripts/verify_visual_assets.rb --strict` y build Jekyll con borradores.
Las capturas de esta revisión están en `/tmp/polish-*`; los resultados resumidos
y los scripts de medición quedan versionados. Código registrado localmente en
`6986f7dc` (blog) y `b8eeb59` (análisis), con árboles limpios después de esos commits.
El preview respondió HTTP 200 y los hashes de CSS, app.js y site-ui.js servidos
coincidieron con los citados por su HTML. Este cierre documental no cambia código.
No se realizó push ni publicación; Jekyll 4004 permanece activo.

## Revisión integral y eliminación de omisiones, 11 de septiembre

La revisión del alcance completo reabre F9_2 y su dependiente F9_5 como parciales:
la caché y el selector tienen resultados favorables, pero no acreditan una mejora
global del mapa. El tablero `avaluos-ii-todo.md` incluye también F3/F4 fiscales,
launcher, servidor y protocolo CCU. Los cortes de pruebas anteriores permanecen
arriba como historia, no como resultados vigentes de esta continuación.

Se ejecutaron localmente las seis pruebas de geometría y luego la suite Python
completa: **52 aprobadas, cero fallos y cero omisiones, 2,453 s**. Log íntegro:
`avaluos-ii-python-complete-20260911.txt`. Incluye la extracción PMTiles con archivo
sintético, dos payloads seleccionados y hash de la fuente sin cambios. No se
alteraron pruebas para evitar omisiones ni se reconstruyeron PMTiles nacionales.

Entorno mantenido: `/opt/entornos/catastros-sii-predial/bin/python`, Python 3.12.13,
GeoPandas 1.1.4, Shapely 2.1.2, pandas 3.0.5 y PyArrow 25.0.0. PMTiles 3.7.0 se
descargó de PyPI como rueda pura, sin dependencias ni instalación, a `/tmp`.
SHA-256: `d1a7a7a166ce3c5c8756cc2c8e4b0aa55e3d854fbd4517c963de16c39b631b14`.
La descarga inicial dentro del sandbox falló por DNS; la descarga de red autorizada
funcionó. No se modificó el entorno global ni el entorno predial.

Reproducción desde la raíz del blog; el primer comando requiere acceso a PyPI:

```sh
python -m pip download --no-cache-dir --no-deps --only-binary=:all: --dest /tmp/avaluos-pmtiles-qa-20260911 pmtiles==3.7.0
PROJ_DATA=/usr/share/proj PYTHONPATH=/tmp/avaluos-pmtiles-qa-20260911/pmtiles-3.7.0-py3-none-any.whl /opt/entornos/catastros-sii-predial/bin/python -m unittest discover -s tests/catastro_sii -v
```

`validate_build.sh` conserva su selección normal de `python3`; ese intérprete
puede volver a omitir pruebas si carece de las dependencias. La ejecución anterior
es la comprobación complementaria completa, no un cambio del entorno de CI.
Las 132 TS y 53 analíticas aprobadas corresponden al código integrado de la
sección anterior; una actualización documental no justifica repetirlas.

## Petición posterior: duración final de medio segundo

El usuario pidió el 11-09 reducir la animación a la mitad. Se conservó la cola,
activación próxima al viewport, orden, accesibilidad y cancelación; los rodillos
pasaron de 850–1.090 ms a **425–545 ms**. La prueba existente con un máximo de
550 ms falló primero con 970 ms en el ejemplo de cinco dígitos. Tras el cambio,
las nueve pruebas de la animación aprobaron; `node --check` también.
La ejecución Vitest completa posterior aprobó 135 pruebas en 19 archivos,
incluidos los 17 archivos de Catastro y dos de memoria gobernada.

Se actualizó la huella de `site-ui.js` en el HTML. Una lectura real del servidor
4004 confirmó HTTP 200, duración nueva y coincidencia entre huella anunciada y
bytes servidos: `1a40049e0112a00a5757a33ec6a706d272236092c8ec0c385fd1a8f51673c2b3`.
La reconstrucción automática retiró el overlay efímero del mapa, tal como se
había documentado; se repone después de los cambios de archivos de esta tanda.
