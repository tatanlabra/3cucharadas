# Auditoría e implementación editorial — partes III y IV

## Diagnóstico
Los artículos mezclaban relato, inventario de fuentes, especificaciones y pruebas de sensibilidad. Las explicaciones introductorias repetidas interrumpían la secuencia de preguntas; algunos titulares expresaban más certeza que las tablas y notas que los acompañaban.

La extensión se trató como un problema de jerarquía editorial: conservar las conclusiones y sus límites en la lectura principal, y ofrecer el detalle verificable en páginas de anexo con navegación de retorno. El contrato aprobado fija presupuestos distintos para artículo, preámbulo y cierre.

## Arquitectura implementada
| Superficie | Función |
|---|---|
| Preámbulo | Situación que motiva la pregunta; hallazgo, comparación crítica y límite en un único aviso de tres párrafos |
| Tres cucharadas | Pregunta concreta, evidencia necesaria, interpretación y transición hacia la siguiente pregunta |
| Cierre | Recapitulación, implicación prudencial y tres desafíos observables |
| Anexo de cada parte | Tablas, figuras complementarias, especificaciones, sensibilidad y procedencia |
| Navegación | Cuatro entregas, ubicación actual y enlaces contextuales entre argumento y evidencia |
| Presentación | TOC, tablas desplazables, foco de teclado, figuras claro/oscuro y variantes móviles; alineación natural |

### Parte III
El hilo pasa de delimitar los cierres y la población observable a comparar las trayectorias y evaluar qué decisiones permiten sus límites. El agregado histórico y la ventana 2016–2019 no se intercambian. La diferencia entre receptoras permanece descriptiva y sin intervalo propio.

### Parte IV
La primera cucharada pregunta cuánta desventaja existía antes del cierre; la segunda examina qué cambia al considerar esa historia; la tercera distingue acceso total, canal técnico-profesional y heterogeneidad dependiente de la especificación. El cierre conserva la alternativa de sustitución hacia universidades.

## Criterio de estilo
Se usó el corpus local ya extraído con Docling y la guía [style-manual-corpus.md](../../style-manual-corpus.md): Chicago-Deusto para español y CMOS 18 para inglés, con las excepciones editoriales documentadas del blog. Párrafos con una unidad de sentido, sujetos explícitos, paralelismo, encabezados informativos y transiciones que nombran la pregunta pendiente.

Los presupuestos de extensión, los anexos separados y la alineación natural son decisiones del blog. No se atribuyen a Chicago. La revisión no cambia el sistema de referencias ni certifica una auditoría exhaustiva de todo el manual.

## Revisión independiente
La primera revisión sustantiva de Claude Sonnet 5.5 produjo REQUEST_CHANGES. Confirmó la mejora del hilo y detectó problemas de definición del estimando, trazabilidad de G1 y visibilidad de límites de identificación. Respuesta original y transporte: evidence/claude/.

El integrador contrasta los hallazgos con las fuentes antes de incorporarlos: un consenso entre agentes no reemplaza la evidencia. Claude aprobó la revisión completa ES en r4 y confirmó su vigencia tras cinco ajustes menores en r5. El dictamen y los seis hashes de fuentes quedan en evidence/claude/decision.json. Esta aprobación excluye EN, PDF y navegador, que se verifican por separado.

## Extensión medida en español

Con el mismo contador de los verificadores, retirando referencias, marcas HTML y el anexo plegable anterior: III pasa de 6.318 a 2.664 unidades de palabra (−57,8 %); IV, de 9.549 a 3.024 (−68,3 %). El detalle metodológico se conserva en anexos separados. Este contador separa números y signos, por lo que difiere del conteo editorial por espacios (2.572 y 2.887). Evidencia y método: evidence/editorial-length-es.json.

## Verificación y límites
- Identidad de los cuatro artículos y hashes de los ocho CSV contra baseline.
- Verificadores científicos sobre la unión artículo/anexo, con errores provocados y salidas originales.
- Comprobación de las ocho rutas, temas claro/oscuro, tamaños de pantalla, referencias, tablas, teclado, impresión y lectura sin JavaScript.
- Enlaces y fragmentos internos sobre el artefacto renderizado.
- PDF IV compuesto desde el artículo y su anexo; hashes de ambos insumos y del PDF.
- No se reestiman modelos ni se certifica identificación causal. La entrega local no equivale a publicación ni a custodia científica en un nuevo commit.

## Estado vivo
El estado de aceptación está en [contract.md](contract.md) y en el tablero `pb-20261107T230204755Z-19e1bf67`. Este informe describe el criterio editorial; el cierre, las mediciones finales y las limitaciones pendientes se registran en el acta de entrega.
