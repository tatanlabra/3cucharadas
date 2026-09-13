# Avalúos II: cierre de publicación del 13 de septiembre de 2026

Revisión desplegada: `48403c8dea3c1f8ff705742f5fa50fae2b111376`. Análisis reproducible: `9d4eb179bef0305af8ebbe3bdff75baf0e213c93` en catastros_sii (repositorio local sin remoto).

[Pipeline GitLab aprobado](https://gitlab.com/tatanlabra/3cucharadas/-/pipelines/2844735033). Los recibos `public-parity.json` y `public-data-parity.json` comparan las URLs normales realmente servidas, sin parámetros para eludir caché: siete páginas, 58 assets referenciados y ocho descargas. El artefacto ZIP pasó CRC. El texto del artículo ES/EN coincide con el aprobado.

La revisión conserva 781 archivos protegidos y 16 bindings de contenido/evidencia. El perfil source pasa sus 25 controles. La auditoría encontró y corrigió un hash/claim social obsoleto y la pérdida de cobertura de seis piezas legacy; la nueva prueba falló antes del arreglo y pasó después. Los dos commits locales anteriores se incluyen con esos correctivos.

GitHub recibe el espejo con `[skip actions]` para no ejecutar sindicación social. El commit posterior de este recibo solo afecta `docs/` y `difusion/`, excluidos del sitio, y usa `[skip ci]`: no se presenta como un segundo despliegue. `main` local y ambos remotos deben apuntar a ese cierre documental.

Quedan preservados fuera del commit 77 archivos de otros trabajos (CSS/borrador/figuras Multiagentes IV y loops/README de difusión). No se borran ramas ni worktrees ajenos. La deuda de Medium/Nushell que dejó rojo el pipeline programado anterior y la deuda histórica de rendimiento AC-Q6 siguen identificadas; no son un fallo del nuevo build ni se dan por resueltas. Los detalles, correcciones de entorno y límites están en `publication.json`.

Rollback: revertir los commits de contenido en un nuevo commit, validar y desplegar. No hacer force-push ni restaurar el árbol de trabajo sobre cambios ajenos.
