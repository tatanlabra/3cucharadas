# DEV.to — depuración y publicación autorizadas

Fecha local: 2026-09-06, America/Santiago. Verificación pública: 2026-09-07 UTC.

## Autorización y alcance

La persona usuaria autorizó eliminar borradores inferiores y luego pidió publicar
los restantes. Esto amplía expresamente el límite anterior de mantenimiento sin
publicación; no autoriza modificar los dos artículos que ya estaban publicados.
La ejecución fue propia, sin delegación. `agent-browser` operó la sesión que la
persona usuaria autenticó; no se extrajeron claves ni cookies.

## Duplicado

Avalúo tenía dos borradores: 4584596 y 4584581. Sus contenidos completos del editor
eran idénticos, incluidos los metadatos: 31.816 caracteres en cada uno. El desempate
favoreció 4584596 porque ya estaba asociado al registro de distribución canónico.
Se confirmó que el formulario apuntaba a `/articles/4584581` y se eliminó sólo ese
duplicado. El panel pasó de ocho entradas/seis borradores a siete/cinco.

La copia privada `devto-cleanup/duplicates-before.json`, bajo el directorio durable
de evidencia de esta sesión, permite recuperar el contenido eliminado. Su SHA-256
es `6b3c27fc615f04ecd71a73c2dbb3863f93ea260da4701f945df94bfc49bb1624`.

## Publicaciones verificadas

| Artículo | ID | URL pública |
|---|---|---|
| Cuotas IA | 4235233 | https://dev.to/tatanlabra/ai-quotas-in-three-spoonfuls-a-hud-for-the-kde-panel-2db1 |
| Memoria II | 4584571 | https://dev.to/tatanlabra/multi-agent-work-in-three-spoonfuls-ii-auditable-memory-127a |
| Memoria III | 4582774 | https://dev.to/tatanlabra/multi-agent-work-in-three-spoonfuls-iii-a-memory-that-leaves-traces-3hfn |
| Avalúo | 4584596 | https://dev.to/tatanlabra/appraisal-and-vulnerability-in-3-spoonfuls-change-the-denominator-change-the-map-4j3e |
| Nushell | 4584688 | https://dev.to/tatanlabra/nushell-in-three-spoonfuls-when-does-a-structured-shell-actually-help-an-agent-520a |

El editor de estos artículos usa front matter y el botón `Save changes`. En cuatro
encabezados se cambió `published: false` a `published: true`; Nushell no declaraba
ese campo y se añadió explícitamente. Antes de cada cambio se comparó el contenido
actual completo contra el respaldo; cualquier diferencia habría detenido la edición.
La transformación aislada pasó dos fixtures válidos y rechazó encabezado ausente,
campo duplicado y estado ya publicado. No se alteraron cuerpos ni otros metadatos.

Los cinco previews renderizaron imágenes y secciones. Memoria II mostró una fórmula
y Avalúo tres, sin errores KaTeX ni etiquetas Jekyll sin interpretar. La primera
lectura de imágenes diferidas fue prematura; se corrigió el instrumento para esperar
la imagen cargada y el título visible del preview, sin modificar el contenido.

Los cinco endpoints públicos por usuario/slug devolvieron ID, canonical y fecha de
publicación; el cuerpo Markdown de cada respuesta coincide exactamente con el
respaldo excluyendo únicamente el encabezado. El panel final mostró **7 publicados,
0 borradores**. Los dos artículos publicados anteriormente no se editaron.

La consulta numérica de Cuotas IA devolvió 404 incluso después de guardar; su página
anónima devolvió HTTP 200 con `data-published=true`, y el endpoint público por slug
devolvió el artículo. No se asumió que el primer 404 demostrara falta de publicación.
DEV conserva para Cuotas IA `published_at=2026-07-26T15:38:43Z`; no se presenta esa
fecha histórica como una primera publicación realizada hoy. Las otras cuatro fechas
son 2026-09-07 UTC, todavía 2026-09-06 en Chile.

## Custodia y límites

`publication-before.json` conserva los cinco borradores exactos con permiso 0600;
`publication-result.json` registra los resultados públicos y la comparación de cuerpos.
Ambos están en `~/.local/state/3cucharadas/site-health/20260906/devto-cleanup/`.
El ledger local actualiza estados y reemplaza cuatro URLs temporales por las públicas.
La publicación no elimina la deuda de otros canales ni acredita por sí sola el cierre
de la auditoría técnica F4/F6. Una publicación externa no es totalmente reversible.
