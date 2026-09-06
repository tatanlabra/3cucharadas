# Cierre del piloto y variante de zoom centrado — 2026-09-06

> Registro histórico de la captura. Los entregables aprobados se archivaron fuera
> del sitio durante el saneamiento; ubicación, custodia y recuperación en
> [evidencia de saneamiento](evidence/site-health-20260906.md#archivo-de-videos).
> Los enlaces originales de este registro se resuelven restaurando el paquete.
> El fallo de Stringex descrito abajo corresponde al HEAD histórico, no al remoto corregido.

## TODO_STATE

- [x] Aprobación humana de la calidad/encuadre del piloto registrada, con observación de zoom.
- [x] Piloto MP4 preservado byte a byte; variante separada, sin modificar la web.
- [x] Zoom al centro, captura 4K nativa, MP4 1080p30 de diez segundos y controles técnicos.
- [x] Skill instalada en Codex; validación estructural, uso independiente y pruebas rojas/verdes.
- [x] Temporales del piloto retirados tras su aprobación; máster nuevo retenido.
- [x] Feedback positivo directo de la variante registrado en su manifiesto; no heredado del piloto.
- [x] Revalidación final: skill válida, regresión funcional y 300/300 hashes de frames correctos.
- [x] Skill versionada en penta-agent: `8c7f84c2bfeb63a5b1d397709e114c039358d701`.
- [!] Build completo del blog: falla por `stringex` no declarada en el bundle; pendiente externo al video, necesario antes de desplegar.
- [ghost] Push y subida/publicación externa: no solicitados para el cierre local.

## Entregables y evidencia

| Artefacto | Resultado |
|---|---|
| [Piloto aprobado](../assets/videos/multiagente-penta-agent-memoria-gobernada-grafo-linkedin-x.mp4) | 2,764,701 bytes; SHA256 `4d1b33173e0ca3eb52b3624f8b4d0cb3132c7e5af7484cd941ca1d43bc561c9e` |
| [Variante centrada](../assets/videos/multiagente-penta-agent-memoria-gobernada-grafo-zoom-centro.mp4) | 3,661,510 bytes; SHA256 `5aecef774b0a0adae3993b42bef2f5a7ec020bc49c309c352c55ae2321783efd` |
| [Manifiesto de la variante](../assets/videos/multiagente-penta-agent-memoria-gobernada-grafo-zoom-centro.json) | Fuente, entorno, receta, coordenadas de todos los nodos, hashes de frames y métricas |
| [Póster a 5 s](../assets/videos/multiagente-penta-agent-memoria-gobernada-grafo-zoom-centro-poster.jpg) | 1920×1080; extraído del MP4 entregado |
| [Hoja de contacto](../assets/videos/multiagente-penta-agent-memoria-gobernada-grafo-zoom-centro-contacto.jpg) | Diez muestras del MP4, revisadas visualmente |
| [Prueba independiente](evidence/captura-video-forward-test-20260906.md) | Otro agente utilizó la skill para crear preview y auditar el piloto, sin pistas sobre resultados |

Skill canónica: `penta-agent/skills/captura-video-difusion/SKILL.md` en la raíz del
workspace. Disponible mediante `~/.codex/skills/captura-video-difusion` y la
proyección local `.codex/skills` de penta-agent; sin cambiar otras configuraciones.
Invocación: «usa $captura-video-difusion para hacer el video de difusión».
El adaptador ejecutable está probado para este grafo; otras páginas requieren adaptación.

## Corrección y rúbrica fijada

El piloto acercaba la cámara sólo al 68 % de su distancia y apuntaba parcialmente
hacia `context:handoff`, nodo lateral. La variante apunta al centro (0,0,0) y pasa
de 3600 a 432 unidades (8.33×) con interpolación exponencial suave y retorno.
Los 975 nodos con coordenadas publicadas están centrados en el origen (error medio
por eje menor a 0.00001 unidades). Los otros 457 no tenían coordenadas persistidas:
ahora su simulación usa semilla fija y 180 pasos, y después se congelan los 1432.
No se alteran nodos, relaciones, rótulos ni el HTML canónico.

La explicación histórica que atribuía toda diferencia de replay a rasterización
era insuficiente: la comprobación anterior no cubría todos los nodos. La nueva
compara el hash del layout completo; no reduce su umbral para aceptar drift.

Se exige VMAF ≥97, SSIM ≥0.995 y PSNR ≥42 dB contra el mismo máster 1080p FFV1;
después se elige el menor archivo entre tres CRF. No es una búsqueda global.

| CRF | Bytes | VMAF | SSIM | PSNR dB | Resultado |
|---|---:|---:|---:|---:|---|
| 14 | 5,414,724 | 97.823944 | 0.999141 | 54.815520 | Pasa |
| 16 | 4,458,220 | 97.600786 | 0.998785 | 53.215841 | Pasa |
| 18 | 3,661,510 | 97.355207 | 0.998302 | 51.668153 | Seleccionado por menor peso |

## Verificación

HECHOS medidos: framebuffer WebGL y PNG 3840×2160; entrega H.264 High@4.1,
yuv420p BT.709 limited, 1920×1080, 30 fps constantes, 10.000 s, sin audio.
300 frames decodificados y únicos, sin repeticiones consecutivas, negros ni freezes;
timestamps CFR comprobados y átomo moov anterior a mdat. Pico móvil de un segundo:
5,335,832 bps. Cierre virtual del loop SSIM=1 y replay independiente SSIM=1,
delta de cámara=0 y hash de todos los nodos idéntico en este entorno.

Conversión explícita full RGB → limited YUV con matriz BT.709, además de etiquetas
y VUI. La igualdad de colores entre navegadores/GPU/plataformas distintas no se garantiza.

Fuente publicada descargada y fuente local coinciden: SHA256
`3a02db8eb78c02d8aa8ec5e2a5f885e14118e0a6ed1f333d46bd408cae7edfc3`.
Receta ejecutada: `scripts/capture_penta_rag_graph_video.mjs`, SHA256
`12d9f49d1e180bc5be4e5b20f3084f0ffc8f907a2b216f8b6f39bea037ad0584`.

Comprobaciones ejecutadas: `quick_validate.py` (PASS), `node --check` en los tres
scripts, self-test de hooks/layout/NaN, preview independiente con cinco poses,
auditoría del piloto y auditoría integral de la variante en el encoder.
`test-delivery.mjs` acepta el piloto, rechaza duración incorrecta y un MP4 congelado
con formato correcto, y vuelve a aceptar el piloto. Pruebas repetidas después del
refuerzo del launcher: PASS.

Incidentes: puerto/DNS restringidos por sandbox, recuperados mediante permisos
normales. Un subproceso Node restringido devolvió exit 0 sin ejecutar JS; el arnés
lo detectó y se validó fuera del sandbox. Se añadió rechazo explícito de evidencia
vacía al launcher. El selector MCP se ejecutó, pero su telemetría no estuvo disponible;
no se modificó infraestructura para habilitarla. Cambios concurrentes de otros agentes
en ambos repositorios fueron preservados; no se ejecutó una suite global ajena al alcance.

## Límites y limpieza

Revisión visual por muestras, no reproducción continua observada. El núcleo queda
visible; el panel derecho tapa una parte periférica al acercarse, y el panel izquierdo
conserva una superposición de la página original. No se prometen capacidades genéricas
perfectas por un único caso exitoso ni óptimo global por comparar tres candidatos.

El perfil está dentro de los límites oficiales consultados el 2026-09-06 de
[LinkedIn](https://www.linkedin.com/help/linkedin/answer/a7486279) y
[X](https://help.x.com/es/using-x/x-videos). Aceptación de subida y recodificación
por plataforma: NO VERIFICADAS; no se inició ninguna publicación.

Se eliminaron aproximadamente 925 MiB de temporales propios del piloto:
`/tmp/penta-rag-video-ce07IQ`, `/tmp/penta-rag-video-UJvoK4`,
`/tmp/penta-rag-video-Xoxkxl`, más los directorios vacíos
`/tmp/penta-rag-video-TQE6hB` y `/tmp/penta-rag-video-thhhw9`.
No tienen copia recuperable; los MP4 entregados permanecen intactos.
El nuevo máster, frames y candidatos siguen en `/tmp/penta-rag-video-LSb00a`.
La prueba independiente sigue en `/tmp/captura-video-forward-test-awSHAVJW`;
los controles negativos finales están en `/tmp/capture-delivery-test-VgDsj2`.

HANDOFF-TRACE: Codex principal -> persona usuaria, vía conversación, modelo no
registrado en la evidencia de captura, 2026-09-06. El feedback posterior a la variante
fue «muy buenos resultados, calidad y rapidez.»; el manifiesto registra esa aceptación
directa y ya no la presenta como pendiente. Esto no autoriza publicación externa.
Rollback visual: usar el MP4 del piloto; el visor canónico no fue editado ni desplegado.

## Remanente al cierre local

La skill y los videos están terminados para el caso probado. Los siguientes son
pasos posteriores u opcionales, no defectos pendientes de implementación:

| Acción | Estado y condición para retomarla |
|---|---|
| Build completo del blog | Bloqueado por la dependencia `stringex` fuera del bundle; resolver antes de promover este HEAD a publicación. Ver evidencia siguiente. |
| Push de los commits | No ejecutado; requiere encargo explícito. Antes, volver a validar el HEAD combinado y CI tras el push. |
| Publicación LinkedIn/X | No ejecutada; la subida real y la recodificación de la plataforma siguen sin verificar. |
| Archivar el máster intermedio | Opcional; los 300 PNG 4K y FFV1 siguen en `/tmp/penta-rag-video-LSb00a`, fuera de Git y sujetos a limpieza temporal. |
| Otras páginas | Ampliación futura: adaptar y validar un recorrido propio, sin extrapolar el éxito de este grafo. |
| Contador de preview | Mejora cosmética opcional: muestra índices de la secuencia de 300 aunque genera sólo cinco poses; documentado en la skill. |

Los MP4, póster, contacto, manifiestos y receta se conservan como entregables
durables del repositorio. El FFV1 intermedio es una referencia **1080p**; la fuente
4K son los PNG. No se incluye el scratch de cientos de MiB en los commits.
La regresión final sobre el MP4 centrado volvió a aceptar el válido, rechazar
duración incorrecta y clip congelado, y recuperar el verde; fixtures en
`/tmp/capture-delivery-test-zle6kI`. No se re-renderizó el video ni se alteró su SHA.

## Verificación adicional del cierre y commits

Skill: commit `8c7f84c2bfeb63a5b1d397709e114c039358d701`,
`feat(skills): incorpora captura de video HD para difusión` en penta-agent.
Incluye seis archivos de la skill y el symlink local de Codex; el enlace personal
instalado sigue resolviendo a esa fuente. El video, manifiestos y esta documentación
se agrupan en el commit de 3cucharadas que incorpora este archivo. Ambos commits
usan autor y committer `tatan <tatanlabra@gmail.com>`, sin coautoría de agentes.
No se incluyen cambios concurrentes ajenos en ninguno de los repositorios.

| Comprobación repetida al cierre | Resultado |
|---|---|
| `quick_validate.py` sobre la skill | PASS |
| `node --check` sobre los scripts y self-test de captura | PASS; hooks inválidos, drift y NaN rechazados |
| `test-delivery.mjs` sobre el MP4 centrado | PASS: válido → dos negativos rechazados → válido |
| Hash y tamaño de ambos MP4 frente a sus manifiestos | PASS; bytes del piloto y variante intactos |
| Feedback directo y SHA de receta | PASS; sólo cambió el estado documental de aprobación |
| Recibo de los PNG 4K conservados | PASS, 300/300 hashes verificados |
| Índice Git selectivo y whitespace | Revisado antes de cada commit; sin archivos ajenos |

### Fallo reproducible del build del blog, sin cambios de entorno persistentes

1. `bundle exec jekyll build --help` no inició Jekyll: `.bundle/config` apunta a
   `vendor/bundle`, donde no encuentra las gems. No se modificó esa configuración.
2. `BUNDLE_IGNORE_CONFIG=1 bundle check` pasó: el entorno global ya tiene las
   dependencias declaradas, por lo que no se instaló nada.
3. `BUNDLE_IGNORE_CONFIG=1 JEKYLL_ENV=production bundle exec jekyll build --disable-disk-cache --destination /tmp/captura-video-closeout-1C8FMw/site`
   llegó al render y terminó con exit 1: `stringex is not part of the bundle. Add it to your Gemfile.`
4. El mismo fallo se reprodujo con un único encabezado Kramdown y
   `transliterated_header_ids: true`. Como control aislado, `false` produjo HTML
   válido. **No se aplicó ese cambio al sitio**: podría modificar sus anchors.

La opción `transliterated_header_ids: true` ya está en `_config.yml:260` del HEAD
previo; `Gemfile` y `Gemfile.lock` no declaran `stringex` y no fueron editados por
esta sesión. La gem `stringex (1.5.1)` existe localmente, pero Bundler no permite
cargarla fuera del contrato declarado. Esto explica por qué un `bundle check`
verde no bastó para compilar. La solución de dependencias queda como tarea separada;
no se autorizaron nuevas dependencias de producción ni cambios de anchors.

No se ejecutó `verify_site_artifact.rb` sobre una salida incompleta ni se declaró
verde el build global. Después de resolver el bundle habrá que construir de nuevo
y validar también el presupuesto de tamaño del sitio con los nuevos assets.
La advertencia de Faraday sobre `faraday-retry` fue informativa; el error fatal
observado corresponde a `stringex`.

**Conclusión:** cierre local del video y la skill, verificados y versionados;
preparación del despliegue del blog pendiente por el fallo descrito. El resto del
worktree contiene trabajo concurrente ajeno: no se promete limpieza global.
