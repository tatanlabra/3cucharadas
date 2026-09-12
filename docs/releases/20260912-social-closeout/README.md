# Avalúos II: reparación y cierre social

Reparación `e77c03ea58dc4b2205cb3bc69f9cc170fa2d7822` subida a GitLab y GitHub.
[Pipeline #253](https://gitlab.com/tatanlabra/3cucharadas/-/pipelines/2843662335)
terminó en success: build y Pages aprobados. Evidencia en `remote-ci.json`.

El agente omitió Mastodon/Bluesky al declarar `distribution.social: false` en ES/EN
en `b4638115`, pese a la autorización de difusión. No fue un fallo de credenciales:
las cuentas autenticaron y ambas URLs del post respondieron HTTP 200.

El hook instalado solo resuelve destinos; no existe un emisor automático conectado
al push. El timer y CI auditan pendientes. Además, el catálogo ignoraba `social`
y su checklist mostraba `[x]` para elegibilidad. Eso facilitaba un cierre engañoso.

## Reparación

- Restaurado `social: true` ES/EN; excluir las redes exige una razón explícita incluso con otros canales.
- Verificación de política incorporada al perfil `source`, ejecutado antes del build en GitLab.
- Catálogo respeta la política; checklist y hook distinguen elegibilidad de publicación.
- `scripts/post_push_difusion.sh REF` enlaza política, envío, comprobación pública, reconciliación por ref y auditoría; simulacro por defecto.
- Reconciliación respeta el ledger solicitado, elimina eventos repetidos/revertidos, completa respuestas EN y valida YAML antes de sustituirlo.

El comando se ejecuta tras comprobar el despliegue y con autorización de envío.
No instala un envío incondicional al hacer commit/push ni publica otros canales.
Las URLs reconciliadas requieren el commit/push del registro.

## Evidencia observada

| Comprobación | Resultado | Evidencia |
|---|---|---|
| Regresión de política | Cuatro fallos antes; 13 pruebas/50 aserciones después | `policy-red.log`, `policy-green.log` |
| Regresión de elegibilidad | Dos fallos antes; suite Python completa: 38 pruebas aprobadas | `python-red.log`, `python-green.log` |
| Reconciliación | 5 pruebas/17 aserciones; ref aislado, repetición, rollback, respuesta EN, ledger inválido | `reconcile-green.log` |
| Salud del sitio | Perfil source aprobado | `source-health.log` |
| Build de producción local y gates del artefacto | Aprobados; avisos de deprecación Sass conservados | `jekyll-build.log`, `artifact.log`, `readiness.log` |
| Ausencia de duplicados antes del envío | Historial público cubierto desde 2026-09-11 sin coincidencias | `dedup-before.json` |
| Publicación | Ambas raíces ES y respuestas EN verificadas, tarjetas e imágenes presentes | `publication.json` |
| Repetición del cierre | Ambos envíos skipped; mismas URLs verificadas | `idempotence.json` |
| Auditoría social del post | Rojo sin URLs → verde con las cuatro URLs | `publication-before.log`, `publication-after.log` |

## Publicaciones

- Mastodon ES: https://mastodon.social/@asiole/117260311924206594
- Mastodon EN: https://mastodon.social/@asiole/117260311983076404
- Bluesky ES: https://bsky.app/profile/labra.bsky.social/post/3mve3cgiakl2y
- Bluesky EN: https://bsky.app/profile/labra.bsky.social/post/3mve3chsywl2t

Texto final en `difusion/paquetes/avaluos-ii-brecha-residencial/social.json`.
Se usaron hashtags y tarjeta con la portada del artículo. No se trasladaron
arrobas de X a otras redes sin confirmar la identidad de esas cuentas.

## Límites y pendientes ajenos a este cierre

`all-channels-pending.log` sigue rojo en modo estricto porque faltan las URLs
de LinkedIn/X en el registro. El autor confirmó haber publicado en X; eso no
equivale a una URL verificada y **no se debe reenviar**. Sus dos archivos locales
de copy se conservaron sin incluirlos en el commit de reparación.

La deuda de Medium/Nushell permanece fuera del alcance. Un Pages verde no la cierra.
La prueba de repetición garantiza el caso observado con ledger conservado; no
demuestra ausencia de duplicados ante pérdida del ledger o cualquier corte de red.
