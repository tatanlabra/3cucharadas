# Gobernanza del repositorio

## Decisión operativa

| Clase | Ubicación | Retención |
| --- | --- | --- |
| Fuentes Jekyll, código y activos publicados | repositorio Git | mientras una página, build o pieza publicada los consuma |
| Worktrees paralelos | `/home/ende/Descargas/programaciones/.worktrees/3cucharadas/` | hasta integrar o descartar explícitamente su rama |
| PMTiles de revisión | `${CATASTRO_SII_LOCAL_ROOT:-${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/catastro_sii/local}` | hasta reemplazar la corrida y verificar su SHA-256 |
| Renders de difusión | `${THREE_CUCHARADAS_RENDER_ROOT:-${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/renders}` | hasta publicación o reemplazo comprobado |
| Másters no publicados | `${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/source-masters/` | conservar con manifiesto; no son entrada del build |
| Builds y dependencias instaladas | checkout local, ignorados | efímeros y reconstruibles desde locks |
| Respaldo de refs | `${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/git-backups/` | conservar antes de retirar ramas o ejecutar GC |

El vídeo `assets/videos/catastro-sii-visor.mp4`, los activos RAG y las piezas sociales
de avalúo permanecen versionados: el sitio o sus paquetes publicados los consumen. Una
migración futura debe probar URL, MIME, caché y reproducción antes de retirarlos.

## Gate

```bash
ruby scripts/verify_repo_governance.rb --strict
ruby scripts/verify_repo_governance.rb --strict-local
```

El primer comando gobierna contenido versionado, objetos grandes con dueño, anchura,
profundidad y worktrees anidados. El segundo suma los derivados locales y sirve para
cerrar una limpieza. Ambos emiten JSON con bytes y entradas medidos; no existe un
presupuesto arbitrario para el tamaño total del checkout.

Los umbrales de `docs/contracts/repo-governance.yaml` reflejan restricciones externas:
GitHub recomienda objetos de hasta 1 MB, bloquea objetos de 100 MB, recomienda `.git`
menor a 10 GB, ancho menor a 3.000 entradas y profundidad menor a 50; GitLab.com limita
el repositorio a 10 GB, cada push a 5 GiB y Pages a 1.000 MiB. La push rule específica del
proyecto respondió `404` el 2026-09-06, por lo que no se inventa un máximo adicional.

Fuentes oficiales:

- https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits
- https://docs.gitlab.com/user/gitlab_com/
- https://docs.gitlab.com/user/project/repository/push_rules/

## Medición precisa

| Superficie | Medición |
| --- | --- |
| Snapshot versionado | suma de `git ls-files` y tamaño real de cada entrada |
| Base Git comprimida | `git count-objects -vH` y API remota con `statistics=true` |
| Sitio publicable | `ruby scripts/verify_site_artifact.rb public` después de build limpio |
| Residuos locales | `verify_repo_governance.rb --strict-local` por ruta, bytes y entradas |
| Ramas recuperables | `git bundle verify` más listado de heads y SHA-256 del bundle |

Línea base del 2026-09-06: GitLab reportó `repository_size=126059736`, GitHub
`size=122803 KiB`, el artefacto limpio midió 59.873.791 bytes y 1.121 archivos. La
limpieza retiró 975.604.859 bytes de 24 directorios derivados, sin contar los 716 MB
movidos a estado externo. El checkout compartido bajó de 2.076.205.056 a 221.651.909
bytes; el estado externo total, incluido el bundle de refs, quedó en 844.784.666 bytes.

Las ramas `publish/nushell-20260829` y `publish/nushell-v2-20260905` conservan tres y
un commits únicos frente a `main`; por eso sus worktrees se reubicaron y no se
retiraron. El bundle verificado contiene 262 heads y mide 125.179.276 bytes.

## Rollback

| Cambio | Reversión |
| --- | --- |
| Worktree movido | `git worktree move <ruta-externa> <ruta-anterior>` tras comprobar que el destino no existe |
| PMTiles externos | definir `CATASTRO_SII_LOCAL_ROOT` o mover la raíz de vuelta y comparar su manifiesto SHA-256 |
| Renders externos | definir `THREE_CUCHARADAS_RENDER_ROOT`; regenerar desde HTML/CSS si se pierden |
| Build o caché eliminada | `npm ci`, `npm run build:catastro`, `bundle install` y `jekyll build` desde locks |
| Ref retirada en el futuro | verificar el bundle y recrear la ref desde el hash registrado antes de cualquier GC |
