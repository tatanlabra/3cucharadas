# Avalúos II — avance consolidado

Corte: 11-09-2026. El usuario autorizó publicar al terminar los pasos y revisiones. El [contrato de salida](avaluos-ii-release-contract.yaml) incorpora escenarios tributarios normativos calculados por predio. Los contratos anteriores documentan el diagnóstico y sus límites: el neto observado permanece desconocido; el modelo adicional no lo sustituye.

## Resumen

| Estado | Resultado |
|---|---|
| Implementado | Publicación ES/EN y visor con escenarios monetarios: CI aprobado, tres páginas HTTP 200 y 58 recursos públicos con hashes coincidentes; contrato R1–R4 completo. |
| Parcial | Acceso al preview desde iPhone no observado directamente; el post y visor ya tienen URL público. El neto observado sigue sin fuente compatible. |
| No implementado | Solicitud institucional y ejecución futura del post III CCU, fuera de esta publicación. |

## Detalle por requisito

`[x]` comprobado; `[~]` parcial; `[ghost]` depende del insumo indicado; `[ ]` no ejecutado. No se calcula porcentaje de progreso: los requisitos tienen pesos y dependencias diferentes.

| Pedido / tarea | Estado | Criterio y evidencia | Continuación necesaria |
|---|---|---|---|
| F0–F1: recuperar contexto, fijar alcance y procedencia | [x] | Contrato principal, manifiestos y corrección territorial con rechazo observado | Conservar fuentes y decisiones |
| F2: comparación censal con destino habitacional | [x] | 346 comunas, 344 cubiertas; 6.054.808 roles administrativos, incluidos los carentes de geometría; 53 pruebas analíticas | No convertir faltantes en cero |
| F3a: motor de escenarios y controles | [x] | Pruebas de unidades, componentes, ceros y rechazo de neto no certificado; campos históricos de neto observado permanecen nulos | Activar esa rama sólo con datos compatibles; modelo normativo independiente en F3c |
| F3b: neto habitacional comunal 2026S1 | [ghost] | Cero valores disponibles en las 346 comunas; solicitud y vías investigadas documentadas | Obtener suma neta y cantidad del mismo universo, período y componentes; medianas requieren distribución o estadístico oficial |
| F3c: ranking en pesos y sensibilidad monetaria | [x] | Modelo general por predio, media/mediana con ceros, q=0/0,25/0,5/1; 15 comunas priorizadas; controles independientes contra 6.054.808 registros | Son escenarios normativos, no giro neto observado ni deuda |
| F4: post II ES/EN | [x] | Escenarios y contraste Iquique–Lo Barnechea integrados; artículos en _posts con fecha 11-09-2026; 13 referencias equivalentes | R4 completo; URLs públicos comprobados |
| F5: visor único y tabla accesible | [x] | Diagnóstico integrado, selección comunal y tabla completa; 136 pruebas TS y QA móvil/escritorio; tabla monetaria acompaña q y región | Mantener separado el neto observado del escenario normativo |
| F6: validación local | [x] | 136 TS, 78 analíticas y 56 Python del visor aprobadas; 25 del modelo repetidas tras aclarar metadatos; builds y verificadores verdes | Evidencia final en el recibo de salida; no certifica todo navegador |
| F7: diseño de post III CCU | [x] | Protocolo C0–C7 de expansión, densificación, tiempos y falsación | Ejecución del cruce y post III fuera del alcance aprobado |
| F8: campamentos y otras condiciones habitacionales | [x] | Sensibilidad CNC y clasificación censal reproducibles; 222 polígonos sin conteo conservan ese estado | Sin enlace vivienda–rol ni descuento observado de todos los asentamientos informales |
| F9_1: barra de composición habitacional | [x] | Escenario estricto 1.318.681,81 equivalentes aceptables; suma de componentes conserva el residuo; tres casos adversariales corrigieron materialidad | Transferencia de composición asumida, no calidad observada de inmuebles omitidos |
| F9_2a: caché, carga visible y selector | [x] | Peticiones comunales 2→1; caché acotada, reintento y pruebas de fallos; selector disponible sin WebGL | Conservar recuperación y límites de memoria |
| F9_2b: rapidez del mapa completo | [x] | [Serie emparejada](catastro-paired-loading-20260911-focus.md): mapa útil frío 2.002,20→1.593,10 ms, recarga 1.668,10→1.077,45 ms; mismo encuadre/capas; diez mediciones válidas | Ensayo local acotado; dos exclusiones por foco conservadas; primer load frío mejora sólo 6,72% |
| F9_3: relato, bibliografía y contraste de hipótesis | [x] | Fuentes primarias y contraevidencia ES/EN; altas tasaciones motivan revisión, sin identificar obligación de los casos ausentes | Relato monetario final integrado en F4 y publicado en R4 |
| F9_4a: diagramación, contraste y temas | [x] | Indicadores a 390 px: 1.241,5→663 px; a 1440 px: 495,28→382 px; 320 px sin desborde | QA acotada, no certificación global |
| F9_4b: casino en cascada, duración final medio segundo | [x] | Última petición del 11-09: 425–545 ms, exactamente la mitad del ajuste previo; una cifra a la vez, activación cerca del viewport; nueve pruebas verdes | Valor exacto accesible inmediato; reduced-motion estático |
| F9_4c: nueva paleta próxima al modo nocturno | [x] | Turquesa, azul grisáceo y ámbar luminosos; contornos, etiquetas y patrones; QA claro/oscuro | Preferencia implementada, sin afirmar optimalidad estética universal |
| F9_6: hover Chile estable | [x] | 343 etiquetas sin variar altura a 1280 y 390 px; instrucción separada, sin texto UV redundante | Nombres completos y teclado conservados |
| F9_7: terminología didáctica | [x] | Una definición del código H por página; después roles/predios habitacionales | Claves técnicas permanecen intactas |
| F9_8: dos mapas con campamentos | [x] | Valparaíso y Puerto Montt; plantilla histórica, tres capas, PNG claro/oscuro y WebP; hashes y rechazos adversariales | Recortes y faltantes declarados; imágenes no prueban omisiones prediales |
| F9_5: integración y preparación local | [x] | [Cierre final](avaluos-ii-final-closeout-20260911.md): gate con Node fijado, 135 TS entre dos suites, 52 Python sin omisiones, 53 analíticas; verificación de datos/assets y mapa útil aprobados | Evidencia histórica F9; F3c/F4/R4 se cierran en el contrato de salida |
| F9_E1: alerta de desarrollo Vitest | [x] | 4.1.10→4.1.11; auditoría npm 2 alertas→0; producción conserva los hashes de sus 16 archivos Catastro | Sólo familia Vitest; avisos conocidos de Sass y tamaño MapLibre permanecen |
| Launcher de desarrollo: sólo pacman | [x] | `~/.config/kitty/sessions/desarrollo.session:9`; autostart apunta a esa sesión | Otro launcher independiente conserva sus aplicaciones |
| Servidor solicitado en 4004 | [x] | Se confirmó su término desde el host y se restauró; ES/EN y portada visibles; siete enlaces cartográficos conservados al regenerar | Configuración efímera fuera del repo; no se publica el overlay local |
| Preview desde iPhone mediante Termius | [~] | Servidor y páginas HTTP 200 comprobados desde el PC; instrucciones y enlaces del túnel local entregados; [alcance y evidencia](avaluos-ii-final-closeout-20260911.md#continuación-acceso-desde-iphone) | Activar el reenvío local en el iPhone y comprobar que abre post y visor; conexión SSH por sí sola no prueba ese acceso |
| F10: nueva base, traducción y fecha | [x] | [Evidencia editorial](avaluos-ii-editorial-consolidation-evidence.md); original intacto, 20 filas y 80 valores ES/EN equivalentes, 12 referencias en esa revisión, fecha 11-09-2026; builds y QA móvil/escritorio | Revisión monetaria posterior conserva valores y añade la referencia oficial número 13 |
| F11: hero y teaser generados directamente | [!] | La primera ejecución comprobó la herramienta, pero la revisión humana del 12-09 rechazó su dirección gris/teal | Sustituida por F12; conservar como incidente y antecedente, no como baseline estético |
| F11: diagnóstico delegado de imagegen | [x] | [Auditoría](avaluos-ii-imagegen-diagnosis-20260911.md): generación y edición local comprobadas, rúbrica previa y tarjeta real revisada | La corrección de la skill global no formaba parte de la auditoría; sin ranking experimental entre proveedores |
| F12: convención de título y sistema visual | [x] | Recall y corpus confirman «tema en 3 cucharadas II» y Tokyo Night; títulos ES/EN, cuatro formatos, pipeline 2842837117 y [hashes públicos](avaluos-ii-title-visual-production-receipt-20260912.json) verificados | Axe deja inconcluso el contraste sobre gradientes; no se probó Safari ni un iPhone físico |
| Solicitud institucional | [ ] | Texto concreto preparado, no enviado | El envío requiere autorización explícita; no hay respuesta institucional pendiente |
| Push y publicación | [x] | Commit de implementación 9b5ddf83 enviado a GitLab y GitHub; pipeline 2842505278 aprobado; tres páginas y 58 recursos verificados | Recibo productivo y contrato R4 completos; conservar el ajuste automático posterior del espejo |

## Evidencia y reproducción

- [Cierre productivo R1–R4](avaluos-ii-release-evidence-20260911.md) y [recibo público](avaluos-ii-release-production-receipt-20260911.json): CI, URLs, hashes y límites de la publicación.

- [Pruebas, comportamiento y límites F9](avaluos-ii-polish-evidence.md), incluidos comandos del entorno geoespacial local.
- [Ensayo cartográfico emparejado completo](catastro-paired-loading-20260911-focus.md): diez observaciones válidas, dos cebados y dos exclusiones; once pruebas del evaluador. [Primer intento incompleto](catastro-paired-loading-20260911.md) conservado como antecedente.
- [Cierre integral y seguridad de dependencias](avaluos-ii-final-closeout-20260911.md): pruebas, comandos, errores previos, recuperación y límites vigentes.
- [Consolidación y arte editorial](avaluos-ii-editorial-consolidation-evidence.md), [prompts reutilizables](avaluos-ii-imagegen-prompts-20260911.md) y [diagnóstico de imagegen](avaluos-ii-imagegen-diagnosis-20260911.md).
- [Carga: mediciones y diagnóstico](catastro-viewer-loading-20260910.md): serie posterior, fallo CORS del preview, overlay local y espera de frames; conservar también el resultado histórico.
- [Investigación tributaria complementaria](../../catastros_sii/v5_brecha/docs/avaluos-ii-fiscal-source-followup-20260911.md) y [solicitud preparada](../../catastros_sii/v5_brecha/docs/avaluos-ii-solicitud-datos.md).
- [Protocolo CCU C0–C7](../../catastros_sii/v5_brecha/docs/avaluos-iii-ccu-protocol.md): diseño completo, ejecución futura.

La recuperación posterior identificó los catastros NFS y comprobó la copia local protegida 2026S1. La revisión añade una conversión normativa por predio, manteniendo nulos los campos de giro neto observado. No se emplea el DC mezclado como impuesto ni una tasa sobre el avalúo medio. La solicitud institucional sigue preparada sin enviar.

Un estado se reabre si una prueba falla, cambia el artefacto sin validar o una observación contradice el criterio. La publicación fue autorizada después del cierre local previo; la investigación de obligaciones reales sigue siendo una tarea distinta. Rollback: revertir sólo cambios propios y regenerar derivados; conservar fuentes, evidencia y trabajo concurrente.
