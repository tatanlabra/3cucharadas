# Prueba independiente de uso real: captura-video-difusion

Estado: **success** para la petición acotada (previsualización y perfil técnico del MP4 existente).
Fecha: 2026-09-06. Agente: /root/forward_test_capture_skill.
Scratch retenido: `/tmp/captura-video-forward-test-awSHAVJW`.

## Alcance y resultado

- Se leyó y aplicó `penta-agent/skills/captura-video-difusion/SKILL.md`, con `references/penta-rag.md` y `references/calidad.md` completos.
- Se ejecutaron el launcher real, self-test, preview y auditoría del MP4 existente.
- La previsualización contiene cinco poses de una trayectoria de 10 s: 0, 2.5, 5, 7.5 y 9.9667 s.
- Se capturaron cinco PNG de escena, más cierre virtual y replay independiente; no se renderizaron 300 frames ni se generó otro MP4 final.
- No se editaron repositorios/configuración global, instalaron paquetes, publicaron piezas ni usaron cuentas. Todos los artefactos de esta prueba están en este scratch.
- El navegador y servidor terminaron con el proceso de captura, exit 0.

## Comandos y salidas

| Comando | Resultado |
|---|---|
| `node /home/ende/Descargas/programaciones/penta-agent/skills/captura-video-difusion/scripts/capture.mjs --help` | Exit 0; descubre `--scratch`, `--preview` y `--verify` |
| `node /home/ende/Descargas/programaciones/penta-agent/skills/captura-video-difusion/scripts/capture.mjs --self-test` | Exit 0; rechaza anchor ausente/duplicado, layout distinto y cámara NaN; estado válido y trayectoria pasan |
| `node /home/ende/Descargas/programaciones/penta-agent/skills/captura-video-difusion/scripts/capture.mjs --preview --scratch /tmp/captura-video-forward-test-awSHAVJW/preview` | Primer intento: exit 1, `listen EPERM` en 127.0.0.1; escalación normal: exit 0 |
| `node /home/ende/Descargas/programaciones/penta-agent/skills/captura-video-difusion/scripts/capture.mjs --verify /home/ende/Descargas/programaciones/activos/3cucharadas/assets/videos/multiagente-penta-agent-memoria-gobernada-grafo-linkedin-x.mp4` | Exit 0, `status: pass`; detalle en `existing-mp4-verify.json` |
| `curl --fail --location --max-time 30 --output /tmp/captura-video-forward-test-awSHAVJW/published-viewer.html https://3cucharadas.cl/assets/visualizations/penta-rag-knowledge-graph/index.html` | Sandbox: exit 6 DNS; escalación normal: exit 0, HTML descargado |
| `sha256sum /tmp/captura-video-forward-test-awSHAVJW/published-viewer.html /home/ende/Descargas/programaciones/activos/3cucharadas/assets/visualizations/penta-rag-knowledge-graph/index.html` | Ambos hashes idénticos: `3a02db8eb78c02d8aa8ec5e2a5f885e14118e0a6ed1f333d46bd408cae7edfc3` |

Los permisos normales fueron aceptados; no hubo rechazo de auto-review ni evasión del sandbox.
El intento adicional mediante la herramienta web no pudo abrir la URL (`not safe to open`); la comparación efectiva se hizo con la descarga pública autorizada.

## Evidencia de previsualización

| Medida | Valor observado |
|---|---|
| PNG de trayectoria | `frame-0000.png`, `frame-0075.png`, `frame-0150.png`, `frame-0225.png`, `frame-0299.png` |
| Buffer WebGL | 3840 × 2160 |
| Nodos fijados | 1432 |
| Replay de frame 0 | SSIM 1.000000 |
| Delta de estado entre sesiones | 0 |
| Trayectoria de receta | Orbita completa, foco (0,0,0), distancia 3600 → 432 → 3600 |
| Congelación | Coordenadas publicadas preservadas; faltantes resueltas con semilla/180 pasos; nodos fijos y partículas apagadas |

Evidencia persistida: `preview-approved.log`, `preview/capture-state.json`, `preview/resume-start-4k.png` y `preview/loop-close-4k.png`.

Se inspeccionaron visualmente los PNG 0, 75, 150 y 225, y la hoja de contacto que contiene también 299. El acercamiento alcanza el núcleo central; las vistas de cuarto y tres cuartos muestran caras diferentes del grupo, coherentes con la órbita.

El panel derecho tapa parte de un grupo periférico al máximo acercamiento. El panel izquierdo se superpone a una leyenda inferior, como aparece también en las muestras del MP4 existente. El núcleo pedido sigue visible y no se modificó la página para ocultar esas limitaciones. Esta revisión de muestras no demuestra la fluidez de todas las poses intermedias.

## MP4 existente

| Control | Resultado |
|---|---|
| SHA-256 | `4d1b33173e0ca3eb52b3624f8b4d0cb3132c7e5af7484cd941ca1d43bc561c9e` |
| Tamaño | 2,764,701 bytes |
| Códec / perfil | H.264 High, nivel 4.1 |
| Resolución / color | 1920 × 1080, yuv420p, BT.709 limited |
| Duración / frecuencia | 10.000000 s, 30 fps constantes |
| Audio | Ninguna pista |
| Decodificación | 300 frames, 300 únicos, máxima repetición consecutiva 1 |
| Intervalos negros / congelados | 0 / 0 |
| Faststart | Sí |
| Pico móvil de 1 s | 3,247,688 bps (3.247688 Mbps) |

Cumple los controles técnicos ejecutados por `--verify`. La prueba no recalculó VMAF/SSIM/PSNR contra un máster ni demuestra por sí sola la conversión histórica real de color. No se subió a una plataforma. La revisión visual del MP4 consistió en cinco muestras decodificadas, no en reproducción continua.

## Fricciones observadas

| Severidad | Hallazgo | Evidencia |
|---|---|---|
| Operativa, resuelta | La captura requiere escalación para abrir 127.0.0.1 bajo este sandbox; el flujo documenta la recuperación correctamente | `preview-first-attempt.log` frente a `preview-approved.log`; `references/penta-rag.md:15` |
| Menor | El progreso de `--preview` imprime `1/300`, `151/300`, `300/300` aunque sólo guarda cinco poses; puede inducir a creer que capturó 300 | `preview-approved.log`; `activos/3cucharadas/scripts/capture_penta_rag_graph_video.mjs:450` |
| Límite visual | Panel derecho oculta parte de grupo periférico a 5 s; panel izquierdo tapa parte de leyenda inferior | `preview/frames-4k/frame-0150.png` y hoja del MP4 existente |
| Observación de evidencia | Preview guarda estado y PNG; fuente, receta y SSIM quedan repartidos entre stdout/este informe, no en un manifiesto propio de preview | Listado real de `preview/`; no se esperaba manifiesto de MP4 porque no se solicitó video nuevo |

No se probaron URLs distintas del grafo, instalación portable sin repo vecino, render completo, codificación de candidatos, subida real ni fixtures adicionales de resolución/congelación incorrectas.

## Artefactos para revisión

- `preview-contact-sheet.jpg`: cinco poses nuevas, en orden de lectura; celda inferior derecha vacía.
- `preview/frames-4k/frame-0150.png`: máximo acercamiento al núcleo.
- `preview/frames-4k/frame-0000.png`: panorama inicial.
- `existing-mp4-contact-sheet.jpg`: cinco muestras del MP4 existente, orden idéntico.
- `existing-mp4-verify.json`: salida íntegra y hash del MP4 auditado.
- `published-viewer.html`: bytes de producción usados para comparación.
- `preview-first-attempt.log` y `preview-approved.log`: rojo por sandbox y recuperación verde.

## Identidad de la implementación observada

| Archivo | SHA-256 |
|---|---|
| Skill `SKILL.md` | `0b3230bcc60f8192f1250b556f095f584f209558cd447105ade80925c7c272d0` |
| Launcher `scripts/capture.mjs` | `b38033619ae08ce4c8d77242a892aaefb6cb88e3f067dc5f0604dd61d906f6ec` |
| Receta `capture_penta_rag_graph_video.mjs` | `12d9f49d1e180bc5be4e5b20f3084f0ffc8f907a2b216f8b6f39bea037ad0584` |

La consulta experiencial se abstuvo por ausencia de memoria pertinente. Se evitó registrar telemetría en el repo/configuración porque esta prueba tenía autorización de escritura únicamente en su scratch `/tmp`.
