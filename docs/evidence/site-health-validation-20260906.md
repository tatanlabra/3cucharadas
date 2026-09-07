# Saneamiento — validación suplementaria del contrato original

## Dictamen local

Se cotejó el cierre provisional con el [plan aprobado](../contracts/site-health-approved-plan.md),
sin reducirlo a las pruebas ya ejecutadas. F4 se reabrió porque un ensayo exploratorio
y un resultado axe con revisión pendiente no satisfacían el contrato completo.
La implementación y esta revisión son propias; sólo la paleta nocturna original
fue delegada al subagente expresamente autorizado. No se afirma perfección ni
óptimo global. F6 requiere todavía evidencia de la nueva release en producción.

## F2: diagnóstico y anchors

`tests/test_polyglot_doctor.rb`: cinco tests, 38 aserciones. El control negativo
simula la ausencia real de `stringex` en un proceso Ruby y rompe la transliteración
Kramdown; su recuperación genera los anchors ASCII esperados. El Markdown GFM
efectivamente usado por el sitio conserva anchors Unicode: no se cambió ese
comportamiento para hacer coincidir una expectativa errónea del primer fixture.
Los builds mínimos ES/EN con y sin hook doctor producen HTML idéntico.

## F4: matriz e interacción

La candidata se construyó con el perfil `local`: producción, future y drafts,
tipos, pruebas y verificadores de artefactos. El recorrido final empleó Chromium
151.0.7922.77 y axe 4.12.1, con 22 combinaciones: portada ES/EN, Avalúo y post III
por dos anchos y dos temas; grafo por dos anchos; Catastro por dos anchos y dos temas.
Anchos 390/1280, alto 900. Cero violaciones automáticas, errores JavaScript,
recursos propios HTTP >=400, imágenes propias rotas o overflow del documento.

El instrumento inicialmente consultaba contraste durante transiciones de tema
y recorridos smooth-scroll interrumpidos. Se conservaron esos resultados y se
corrigió la espera: tema seleccionado antes de cargar cada contexto independiente,
recorrido instantáneo verificable y todas las secciones visibles con opacidad 1.
No se cambió CSS para esconder un fallo del instrumento. Las pruebas independientes
de Tab, Enter y cambio de tema siguen siendo la evidencia de interacción real.

Catastro normal: Caldera, 17 UV clasificadas, 13 filas en la ficha; selector, limpieza,
ArrowRight en pestañas y Enter en tema funcionan a ambos anchos. La geometría local
usa respuestas HTTP Range 206: esto no se confunde con una prueba del almacenamiento
geográfico remoto. Grafo: filtro «Probar y verificar», reinicio y pestaña Proyectos
operativos por teclado. Home/posts: foco, tema, imágenes diferidas y fragmentos
internos comprobados en los recorridos preservados.

Con WebGL anulado deliberadamente, Catastro mantiene cinco filas básicas y las
actualiza al seleccionar otra comuna; limpiar la selección elimina el contenido
anterior. Antes la ficha quedaba desfasada esperando el mapa. El renderizador completo
sigue añadiendo sus 13 filas al cargar. El grafo muestra ocho familias y cuatro
métricas, cero canvas y ningún panel `#insights` superpuesto a su alternativa textual.

## Revisión de todos los incompletos

La exportación conserva los nodos completos, sin el límite de diez ejemplos por
regla del resumen CLI. Se revisaron 1.590 ocurrencias de contraste y cuatro de video;
son ocurrencias repetidas por ancho/tema, no otros tantos problemas distintos.

| Grupo | Ocurrencias | Evidencia y resolución |
|---|---:|---|
| Portadas: separadores decorativos | 96 | Separadores `aria-hidden`, sin información exclusiva; no se consideran texto informativo |
| Portadas: texto sobre fotografía | 32 | Captura original y fondo sin texto; contraste mínimo en el área de los glifos 17,031 móvil y 19,267 escritorio |
| Avalúo: tablas y KaTeX | 410 | Estilos completos de cada nodo y ancestros; límites conservadores incluyendo sombras de scroll: >=9,507 claro y >=16,453 nocturno |
| Post III: tablas | 24 | Mismos límites, con sus propios nodos y fondos capturados; sin remitir sólo al estilo de otro post |
| Grafo: texto sobre canvas/panel | 92 | Cuatro colores observados, panel real de opacidad 0,9 y caso adverso canvas blanco; mínimos 4,577 / 7,874 / 5,047 / 4,804; instrucción de navegación con fondo opaco |
| Catastro: fondos y degradados | 936 | Cadenas CSS completas y composición conservadora por canales; 924 ocurrencias informativas >=4,5; 12 iconos redundantes con etiquetas adyacentes se clasifican decorativos |
| Video de Avalúo | 4 | ffprobe: sólo H.264, 39,533 s, ninguna pista de audio; recorrido ilustrativo descrito en párrafo, aria-label y figcaption; no hay diálogo que subtitular |

Las cotas CSS no modelan pseudo-elementos del hero: éste se revisó aparte con
capturas de fondo bajo los glifos, con mínimo 8,690 en escritorio y 9,037 móvil.
Los iconos decorativos de descarga/documento/método conservan textos adyacentes
completos; no se eximen controles ni etiquetas informativas por tener `aria-hidden`.
En grafo, la medición de píxeles final complementa la cota adversa (>=6,028).

La revisión encontró fallos reales que el verde automático no resolvía: el degradado
claro de títulos usaba colores brillantes sobre tarjetas claras y el gris de etiquetas
medía 4,406:1 sobre píxeles (237,242,249). Se conservaron las capturas anteriores y se
corrigió sólo la variante clara con tokens de texto existentes y `--muted: #52617a`.
El gradiente del hero y el modo nocturno no se alteraron por ese ajuste. Las nuevas
cotas mínimas son 4,969 para degradados claros y 4,708 para texto secundario claro.

Otros fallos observados y recuperados: pista del hero con token incorrecto, diccionario
4,49:1, pestañas inactivas 4,32:1, dos grupos nombrados sin rol y atribución cartográfica
sin señal visual adicional al color. Los tests estáticos y de semántica conservaron
controles negativos; el grafo se regeneró sólo desde su JSON público sin cambiar datos.

## Rendimiento: candidato descartado

Una candidata: precargar Fira Sans Regular y Bold. Siete pares alternados y un par
de calentamiento excluido; mismo HTML inmutable, RSS, assets y reloj de build.
Caché desactivada y vaciada por muestra, almacenamiento de origen limpiado, viewport
390×900, red 40 ms / 1,5 MB/s, CPU ×4, misma máquina y versión del navegador.

LCP mediano: **684 → 1.152 ms**, cero de siete pares mejores; empeora 68,42%.
CLS: 0,353835 → 0,308684. Se descarta: no cumple mejora >=10% y >=5/7 pares.
No se retiene ningún preload ni se presenta menor CLS como compensación del fallo
principal. El harness rechaza muestras vacías/incompletas, insuficiente ganancia y
regresión secundaria; acepta su fixture de recuperación. El CLS del baseline sigue
siendo una limitación medida, no una afirmación de rendimiento óptimo.

## F5: mantenimiento tras publicación

La [publicación posterior expresamente autorizada](devto-publication-20260906.md)
dejó siete artículos publicados y ningún borrador. Un test del CLI real reprodujo
que `--existing-drafts-only` fallaba por inventario de borradores vacío. Se añadió
un no-op sólo cuando cada canonical elegible tiene exactamente un ID válido y estado
publicado en un inventario autenticado completo. Vacío, duplicidad y 429 siguen
fallando. Dos ejecuciones repetidas válidas hacen cero escrituras, sin tocar ledger
ni crear una custodia vacía engañosa: dos tests, 32 aserciones. La guarda anterior
de actualizaciones conserva sus cuatro tests y 23 aserciones.

## Evidencia y límites

Scratch de ejecución: `/tmp/3c-health-validation-20260906/`; informes completos de
navegador en `/tmp/playwright-local-mcp.q6GZZa/`. Deben copiarse a la custodia durable
de esta sesión antes del cierre F6, con manifiesto de hashes y sin secretos.
Las pruebas no certifican lectores de pantalla, Safari 16 ni Firefox 104; se conservan
sus targets de build. Siete tests geoespaciales siguen siendo la excepción acordada,
no cobertura ejecutada. Ningún dato canónico ni post se reescribió en este suplemento.
