# Avalúos II — avance consolidado

Corte: 11-09-2026. Preparación y commits locales; push, publicación y envío de solicitudes excluidos. Este tablero deriva del [contrato principal](../../catastros_sii/v5_brecha/docs/avaluos-ii-contract.md), [F8](../../catastros_sii/v5_brecha/docs/avaluos-ii-campamentos-contract.yaml), [F9](avaluos-ii-polish-contract.yaml), [F10 editorial](avaluos-ii-editorial-consolidation-contract.yaml) y [F11 visual](avaluos-ii-visual-editorial-contract.yaml). La serie emparejada completa cierra la comprobación local del mapa útil; el ranking monetario sigue dependiendo de datos tributarios compatibles.

## Resumen

| Estado | Resultado |
|---|---|
| Implementado | Visor y ajustes visuales; campamentos/materialidad; post diagnóstico ES/EN con fecha y portadas; mapa útil frío −20,43% en ensayo local; pruebas y auditoría finales aprobadas. |
| Parcial | Ranking en pesos y cierre fiscal del post: falta neto habitacional comunal compatible con 2026S1; acceso desde iPhone pendiente de activar y comprobar el túnel de Termius. |
| No implementado | Push, publicación y envío de solicitud institucional, excluidos de la autorización; ejecución futura del post III CCU. |

## Detalle por requisito

`[x]` comprobado; `[~]` parcial; `[ghost]` depende del insumo indicado; `[ ]` no ejecutado. No se calcula porcentaje de progreso: los requisitos tienen pesos y dependencias diferentes.

| Pedido / tarea | Estado | Criterio y evidencia | Continuación necesaria |
|---|---|---|---|
| F0–F1: recuperar contexto, fijar alcance y procedencia | [x] | Contrato principal, manifiestos y corrección territorial con rechazo observado | Conservar fuentes y decisiones |
| F2: comparación censal con destino habitacional | [x] | 346 comunas, 344 cubiertas; 6.054.808 roles administrativos, incluidos los carentes de geometría; 53 pruebas analíticas | No convertir faltantes en cero |
| F3a: motor de escenarios y controles | [x] | Pruebas de unidades, componentes, ceros y rechazo de neto no certificado; artefactos monetarios permanecen nulos | Activarlo sólo con datos compatibles |
| F3b: neto habitacional comunal 2026S1 | [ghost] | Cero valores disponibles en las 346 comunas; solicitud y vías investigadas documentadas | Obtener suma neta y cantidad del mismo universo, período y componentes; medianas requieren distribución o estadístico oficial |
| F3c: ranking en pesos y sensibilidad monetaria | [ghost] | El contrato prohíbe sustituir el neto por DC mezclado o por una tasa aplicada al avalúo medio | Depende de F3b; conciliar y generar escenarios antes de ordenar |
| F4: post II ES/EN | [~] | Borradores construidos y cifras conciliadas; diagnóstico físico y prioridad de revisión documentados | Incorporar resultado fiscal de F3 sin presentarlo como deuda ni negligencia probada |
| F5: visor único y tabla accesible | [x] | Diagnóstico integrado, selección comunal y tabla completa; 132 pruebas TS y QA móvil/escritorio | La rama monetaria depende de F3 |
| F6: validación local | [x] | 132 TS, 53 analíticas y 52 Python del visor aprobadas; cero omisiones en la ejecución Python complementaria; builds y verificadores verdes | Evidencia y comandos en F9; no equivale a certificar todo navegador o producción |
| F7: diseño de post III CCU | [x] | Protocolo C0–C7 de expansión, densificación, tiempos y falsación | Ejecución del cruce y post III fuera del alcance aprobado |
| F8: campamentos y otras condiciones habitacionales | [x] | Sensibilidad CNC y clasificación censal reproducibles; 222 polígonos sin conteo conservan ese estado | Sin enlace vivienda–rol ni descuento observado de todos los asentamientos informales |
| F9_1: barra de composición habitacional | [x] | Escenario estricto 1.318.681,81 equivalentes aceptables; suma de componentes conserva el residuo; tres casos adversariales corrigieron materialidad | Transferencia de composición asumida, no calidad observada de inmuebles omitidos |
| F9_2a: caché, carga visible y selector | [x] | Peticiones comunales 2→1; caché acotada, reintento y pruebas de fallos; selector disponible sin WebGL | Conservar recuperación y límites de memoria |
| F9_2b: rapidez del mapa completo | [x] | [Serie emparejada](catastro-paired-loading-20260911-focus.md): mapa útil frío 2.002,20→1.593,10 ms, recarga 1.668,10→1.077,45 ms; mismo encuadre/capas; diez mediciones válidas | Ensayo local acotado; dos exclusiones por foco conservadas; primer load frío mejora sólo 6,72% |
| F9_3: relato, bibliografía y contraste de hipótesis | [x] | Fuentes primarias y contraevidencia ES/EN; altas tasaciones motivan revisión, sin identificar obligación de los casos ausentes | Cierre fiscal del artículo continúa en F4 |
| F9_4a: diagramación, contraste y temas | [x] | Indicadores a 390 px: 1.241,5→663 px; a 1440 px: 495,28→382 px; 320 px sin desborde | QA acotada, no certificación global |
| F9_4b: casino en cascada, duración final medio segundo | [x] | Última petición del 11-09: 425–545 ms, exactamente la mitad del ajuste previo; una cifra a la vez, activación cerca del viewport; nueve pruebas verdes | Valor exacto accesible inmediato; reduced-motion estático |
| F9_4c: nueva paleta próxima al modo nocturno | [x] | Turquesa, azul grisáceo y ámbar luminosos; contornos, etiquetas y patrones; QA claro/oscuro | Preferencia implementada, sin afirmar optimalidad estética universal |
| F9_6: hover Chile estable | [x] | 343 etiquetas sin variar altura a 1280 y 390 px; instrucción separada, sin texto UV redundante | Nombres completos y teclado conservados |
| F9_7: terminología didáctica | [x] | Una definición del código H por página; después roles/predios habitacionales | Claves técnicas permanecen intactas |
| F9_8: dos mapas con campamentos | [x] | Valparaíso y Puerto Montt; plantilla histórica, tres capas, PNG claro/oscuro y WebP; hashes y rechazos adversariales | Recortes y faltantes declarados; imágenes no prueban omisiones prediales |
| F9_5: integración y preparación local | [x] | [Cierre final](avaluos-ii-final-closeout-20260911.md): gate con Node fijado, 135 TS entre dos suites, 52 Python sin omisiones, 53 analíticas; verificación de datos/assets y mapa útil aprobados | Cierre local F9; no cierra F3/F4 ni certifica producción |
| F9_E1: alerta de desarrollo Vitest | [x] | 4.1.10→4.1.11; auditoría npm 2 alertas→0; producción conserva los hashes de sus 16 archivos Catastro | Sólo familia Vitest; avisos conocidos de Sass y tamaño MapLibre permanecen |
| Launcher de desarrollo: sólo pacman | [x] | `~/.config/kitty/sessions/desarrollo.session:9`; autostart apunta a esa sesión | Otro launcher independiente conserva sus aplicaciones |
| Servidor solicitado en 4004 | [x] | Se confirmó su término desde el host y se restauró; ES/EN y portada visibles; siete enlaces cartográficos conservados al regenerar | Configuración efímera fuera del repo; no se publica el overlay local |
| Preview desde iPhone mediante Termius | [~] | Servidor y páginas HTTP 200 comprobados desde el PC; instrucciones y enlaces del túnel local entregados; [alcance y evidencia](avaluos-ii-final-closeout-20260911.md#continuación-acceso-desde-iphone) | Activar el reenvío local en el iPhone y comprobar que abre post y visor; conexión SSH por sí sola no prueba ese acceso |
| F10: nueva base, traducción y fecha | [x] | [Evidencia editorial](avaluos-ii-editorial-consolidation-evidence.md); original intacto, 20 filas y 80 valores ES/EN equivalentes, 12 referencias, fecha 11-09-2026; builds y QA móvil/escritorio | El escenario monetario original sigue dependiendo de F3 |
| F11: hero y teaser generados directamente | [x] | Dos outputs inspeccionados; WebP conserva píxeles y reduce 29,07 % / 27,02 % de bytes; integración ES/EN, descripciones sociales y caption legible | 1,45–1,50 MB por WebP; no representa entrega móvil óptima |
| F11: diagnóstico delegado de imagegen | [x] | [Auditoría](avaluos-ii-imagegen-diagnosis-20260911.md): generación y edición local comprobadas, rúbrica previa y tarjeta real revisada | La corrección de la skill global no formaba parte de la auditoría; sin ranking experimental entre proveedores |
| Solicitud institucional | [ ] | Texto concreto preparado, no enviado | El envío requiere autorización explícita; no hay respuesta institucional pendiente |
| Push y publicación | [ ] | Borradores `published: false`; sin push realizado | Excluidos expresamente |

## Evidencia y reproducción

- [Pruebas, comportamiento y límites F9](avaluos-ii-polish-evidence.md), incluidos comandos del entorno geoespacial local.
- [Ensayo cartográfico emparejado completo](catastro-paired-loading-20260911-focus.md): diez observaciones válidas, dos cebados y dos exclusiones; once pruebas del evaluador. [Primer intento incompleto](catastro-paired-loading-20260911.md) conservado como antecedente.
- [Cierre integral y seguridad de dependencias](avaluos-ii-final-closeout-20260911.md): pruebas, comandos, errores previos, recuperación y límites vigentes.
- [Consolidación y arte editorial](avaluos-ii-editorial-consolidation-evidence.md), [prompts reutilizables](avaluos-ii-imagegen-prompts-20260911.md) y [diagnóstico de imagegen](avaluos-ii-imagegen-diagnosis-20260911.md).
- [Carga: mediciones y diagnóstico](catastro-viewer-loading-20260910.md): serie posterior, fallo CORS del preview, overlay local y espera de frames; conservar también el resultado histórico.
- [Investigación tributaria complementaria](../../catastros_sii/v5_brecha/docs/avaluos-ii-fiscal-source-followup-20260911.md) y [solicitud preparada](../../catastros_sii/v5_brecha/docs/avaluos-ii-solicitud-datos.md).
- [Protocolo CCU C0–C7](../../catastros_sii/v5_brecha/docs/avaluos-iii-ccu-protocol.md): diseño completo, ejecución futura.

La comprobación posterior al pedido de acceso móvil mantiene cero valores netos y cero escenarios monetarios no nulos en las 346 comunas: 344 estados `blocked_components` y dos `missing_source`. Se pidió una ruta local o URL del insumo compatible; no se pidió ni se autorizó cambiar el estimando. La solicitud institucional continúa sin enviar y no hay un proceso de obtención de datos confirmado en ejecución.

Un estado se reabre si una prueba falla, cambia el artefacto sin validar o una observación contradice el criterio. La falta de neto fiscal no se resuelve cambiando el estimando ni las etiquetas de los gráficos. Rollback: revertir sólo cambios propios y regenerar derivados; conservar fuentes, evidencia y trabajo concurrente.
