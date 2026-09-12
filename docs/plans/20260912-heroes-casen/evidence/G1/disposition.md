# G1 — revisión documental opcional

## Resultado de Gemini/Antigravity

**Rechazado como evidencia documental**, aunque el bridge registró `success` y código 0. La revisión atribuye al cuestionario categorías y páginas refutadas por la fuente oficial descargada. Sus salidas originales y el rechazo estructurado se conservan sin reemplazar el estado de transporte por un veredicto editorial inventado.

| Hallazgo | Evidencia discriminante | Disposición |
|---|---|---|
| P1: categorías de v9 inventadas | Cuestionario, página79, enumera1..11; las categorías3 y4 son tenencia propia compartida pagada/pagándose, respectivamente. | No usar sus etiquetas ni el denominador1..4. |
| P1: v28 mal descrito y porcentaje de pérdida no observado | Cuestionario, página83: condición p10=2 y clasificación de hogar principal; el instrumento no acredita una pérdida de80%+. | Conservar la cautela sobre filtro condicional, verificada separadamente; rechazar página11 y cifra. |
| P2: representatividad comunal suavizada y página imposible | Nota oficial, páginas2–3: expc no hace representativos los resultados; PDF de6páginas. | No sustituir representatividad de diseño por un umbral de precisión. |
| P2: afirmación universal de verificación | Resultado dice que verificó todo y no tuvo riesgos; carece de traza de recuperación y contradice los instrumentos. | Acuerdo y código0 no acreditan verificación. |

Los archivos `sources/manifest.json`, `sources/questionnaire-p79.txt`, `sources/questionnaire-p83.txt` y `sources/use-note-p2-3.txt` permiten reproducir el contraejemplo contra los PDF conservados. Los índices PDF son78 y82; los números impresos son79 y83.

## Contraste local independiente del proveedor

Hechos verificados: las categorías anteriores y el filtro v28 se comprobaron con la fuente pública oficial; la nota limita la representatividad territorial. El archivo público actual de Forem declara los cuatro valores globales del nivel de IA. El desglose texto/hero es una decisión editorial del sitio, no un esquema de componentes impuesto por esa enumeración de Forem.

Deducción acotada: el indicador v9=3/4 describe hogares que declaran tenencia propia de un sitio compartido, no toda co-localización residencial ni un conteo de viviendas por sitio. Una proporción de hogares no identifica automáticamente el parámetro de viviendas de una identidad algebraica. Estas observaciones no sustituyen la auditoría científica del estimador, los pesos ni su implementación.

Condición de descarte del rechazo: aportar una versión oficial identificada que contenga las categorías o páginas discrepantes, con recuperación verificable y explicación de la diferencia de versión. La mera repetición del argumento por otro modelo no cumple esa condición.

## Fallback Qwen Code / DeepSeek

El fallback fue autorizado por el usuario. Se mantuvo el briefing público, sin microdatos ni acceso al repositorio canónico. El primer intento de ejecución restringida quedó sin respuesta, con errores repetidos de backend sandbox; se interrumpió con código130. Sus archivos se conservan junto a `interruption.json`, separado de un estado del bridge que no llegó a producirse.

El segundo intento usa el mismo bridge, modelo y modo con ejecución escalada. El harness encontró Docker y descargó automáticamente su imagen `ghcr.io/qwenlm/qwen-code:0.21.6`; su digest se conserva en stderr. Este efecto del arranque se registra expresamente: no fue una instalación manual ni se modificó la configuración. La afirmación antigua del bridge de que no había backend no describía este entorno escalado.

`qwen-configured-provider.json` conserva únicamente campos públicos permitidos de la ruta: harness Qwen Code, modelo solicitado deepseek-v4-pro, proveedor configurado DeepSeek y endpoint público. Esta evidencia de configuración se separa del autorreporte del modelo y no se presenta como autenticación criptográfica de identidad.

Resultado del segundo intento: **fallo de transporte y contenido suplementario parcial recuperado**. El CLI terminó en0 pero el bridge terminó en1 porque `stdout.json` tiene exactamente65536bytes y acaba dentro de una cadena JSON. El prefijo contiene27objetos JSON completos; el último mensaje de asistente conserva el informe final y su `QWEN_RESULT partial`. La recuperación no repara ni cambia el estado oficial del bridge.

El proveedor declara de forma explícita que **no verificó el texto de los PDF CASEN**: su contenedor carece de `pdftotext` y el intento de shell fue denegado. Sí recuperó Forem y documentó la enumeración global. La afirmación adicional de que el orden del enum demuestra un valor por defecto remoto queda sin adoptar: esa enumeración por sí sola no demuestra el default de almacenamiento. La fuente local de U1 fija su propio default explícito.

Para SVG, el informe reconoce que MDN no afirma literalmente la selectabilidad y que la página de propiedades de texto de Matplotlib no sustenta esa afirmación. Este matiz útil queda como crítica suplementaria, sin convertirla en una revisión externa aprobada.

**Estado final G1: partial_optional; count_as_approved_external_review=false.** No hay tercer intento. No bloquea D2 ni autoriza cierre científico. El rechazo Gemini, los estados originales, la recuperación por prefijo completo y los límites están en los JSON de esta carpeta.


## Saneamiento del paquete de commit

Los streams `stdout.json` y `complete-prefix-objects.json` del segundo intento Qwen fueron excluidos del conjunto versionable porque contenían conversación serializada y metadata local de inicialización. Se conservaron íntegros fuera de ese conjunto y se verificó SHA-256 antes y después de copiar. Los dos digests originales y tamaños permanecen en `qwen-20260912T105710Z-263862/sanitized-review-evidence.json` y `recovery.json`; no se presentan como archivos disponibles en este paquete.

La exportación allowlist conserva identidad pública, proveedor configurado, estado, recuentos y hashes. No contiene mensajes ni eventos de inicialización. El informe final documental recuperado y los errores de transporte se mantienen como evidencia parcial; Gemini sigue rechazado y G1 sigue `partial_optional`, sin revisión externa aprobada. La frontera de 65536 bytes continúa siendo una observación y no una causa probada.
