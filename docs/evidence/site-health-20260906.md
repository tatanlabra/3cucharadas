# Contrato de saneamiento — evidencia viva

## TODO_STATE v1

| Fase | Estado | Evidencia / siguiente gate |
|---|---|---|
| F0 Custodia | [x] | 1.325 archivos, bundle completo, restore y tres negativos rechazados |
| F1 Reconciliación | [~] | Base 75f80d72 + historia f91498b7; archivo externo verificado |
| F2 Entorno | [ ] | Bundler local, Node CI y diagnóstico Polyglot |
| F3 Dependencias/gates | [ ] | Locks, suite y artefactos |
| F4 Interfaz/rendimiento | [ ] | Baseline, candidatos, accesibilidad |
| F5 Consumidores/DEV | [ ] | Sólo borradores existentes, sin Telegram |
| F6 Producción | [ ] | Convergencia final, jobs y HTTP |

## Custodia y reconciliación

Respaldo privado: `3cucharadas/git-backups/site-health-20260906T221857Z` bajo
`XDG_STATE_HOME` (por defecto `~/.local/state`). Contiene `refs.bundle`, índice,
patch sin stage, estado NUL, snapshot íntegro y manifiesto SHA-256. La restauración
bare pasó `git fsck`; los 1.325 archivos restaurados coinciden. Los controles
manifest vacío, hash alterado y archivo ausente fallaron; el válido volvió a pasar.

Las 23 rutas pendientes se preservan íntegramente en ese snapshot. El baseline
remoto probado gobierna la candidata; no se reaplican versiones anteriores de sus
correcciones. Inventario original: `worktree-comparison.json` en la auditoría
`3cucharadas-audit-fgDYyv` y `status.z` en el respaldo durable.

| Rutas locales | Disposición y razón |
|---|---|
| scripts/notify_telegram_commit.py | Idéntica al remoto; absorbida |
| scripts/syndicate_devto.rb; scripts/jekyll_to_devto.rb; tests/test_jekyll_to_devto.rb | Versiones anteriores archivadas; remoto añade selección de borradores, rasterización, preflight y pruebas |
| scripts/verify_distribution_done.rb | Anterior archivada; remoto distingue plataforma/idioma y contratos ausentes |
| scripts/notify_telegram_publication.py; tests/test_notify_telegram_publication.py | Anteriores archivadas; remoto comprueba ambos espejos |
| .gitlab-ci.yml; .github/workflows/devto-syndication.yml | Anteriores archivadas; remoto conserva gates estrictos y modo de borradores existentes |
| scripts/install_git_hooks.sh; scripts/git-hooks/post-commit; scripts/git-hooks/README.md | Anteriores archivadas; remoto conserva instalación idempotente y commits silenciosos |
| difusion/README.md; difusion/config/destinos.yml; difusion/linkedin/multiagente-penta-agent-memoria-gobernada-targeting.md | Anteriores archivadas; baseline remoto preservado sin ejecutar canales |
| docs/distribucion.md; docs/publishing.md; systemd/user/difusion-cadencia.service | Anteriores archivadas; remoto documenta auditoría programada y ambos remotos |
| docs/flujo-difusion.md; docs/diagrams/flujo-difusion.d2; docs/diagrams/flujo-difusion.svg; docs/diagrams/flujo-difusion-mobile.d2; docs/diagrams/flujo-difusion-mobile.svg | Anteriores archivadas; se conserva la documentación remota consistente con sus scripts |

El commit de video queda en la ascendencia de la candidata mediante merge. Ningún
archivo pendiente se borra del checkout operativo antes de revalidar su snapshot.

## Archivo de videos

Decisión humana: archivo externo trazable de ambos videos aprobados, sin insertarlos
en posts ni publicarlos. Ubicación: `3cucharadas/source-masters/penta-rag-video-20260906`
bajo `XDG_STATE_HOME`. Nueve archivos copiados y verificados: seis entregables,
dos documentos históricos y la receta ejecutable. Su `manifest.json` contiene
paths, tamaños, hashes, commit de procedencia, responsable, función y retención.

| MP4 | SHA-256 |
|---|---|
| Piloto, 2.764.701 bytes | `4d1b33173e0ca3eb52b3624f8b4d0cb3132c7e5af7484cd941ca1d43bc561c9e` |
| Variante, 3.661.510 bytes | `5aecef774b0a0adae3993b42bef2f5a7ec020bc49c309c352c55ae2321783efd` |

Los seis entregables se retiran únicamente de la candidata publicable después de
verificar la copia. Se recuperan desde ese archivo, el respaldo F0 o el commit
`f91498b7`. Responsable: editorial-multiagente. Retención: hasta reemplazo explícito
y restauración comprobada. Los documentos de captura permanecen como historia;
sus enlaces originales se resuelven restaurando el paquete completo del archivo.

## Límites

Autorrevisión de Codex; no revisión entre proveedores. MCP selector evaluado, pero
el registro automático informó `MCP observation unavailable`. Ningún canal externo
se activa por esa selección. Deuda editorial y cobertura geoespacial se informan
separadas de salud técnica; no se cambian sus criterios para obtener verde.
