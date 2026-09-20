# Flujo de difusión después de cerrar un post

Fecha de revisión: 2026-09-06.

<picture>
  <source media="(max-width: 640px)" srcset="diagrams/flujo-difusion-mobile.svg">
  <img src="diagrams/flujo-difusion.svg" alt="El commit local resuelve destinos; el push abre ramas en GitLab para el sitio canónico y en GitHub para el redirector y los borradores DEV.to; publicar en plataformas externas conserva revisión humana.">
</picture>

La fuente mantenible está en `docs/diagrams/flujo-difusion.d2`; la variante
vertical está en `docs/diagrams/flujo-difusion-mobile.d2`.

Un derivado queda fuera de este mapa porque no se dispara con el push ni con un workflow: la
**cápsula de audio** de un post, que se genera a mano en NotebookLM y se sirve desde el propio
artículo. Su procedimiento está en `docs/flujo-podcast.md`.

| Evento | Qué se dispara | Dependencias que deciden | Resultado |
|---|---|---|---|
| `git commit` que toca `_posts/*.md` | Cadena local `post-commit` → `post-commit-difusion` | Hook instalado, `difusion/src`, Python y `ref` en el post | Escribe `difusion/state/destinos/<ref>.json`; no publica y nunca bloquea el commit |
| `git push origin main` | Push al `main` de GitLab y GitHub | Dos push URLs configuradas; autenticación en ambos servicios | Envía el mismo SHA, pero los pushes no son atómicos |
| Push a GitLab `main` o pipeline programado | `build_site` y luego `pages` | Assets, coherencia de difusión, transformación DEV.to, Jekyll y validadores verdes | Publica el sitio canónico en `https://3cucharadas.cl` |
| Pipeline programado de GitLab | `distribution_audit`, después de `pages` | Contratos `distribution` y artefactos registrados por plataforma e idioma | Hace visible toda la deuda histórica sin bloquear el despliegue ya completado |
| Push a GitHub `main` | Workflow del redirector | Rama `gh-pages-redirect` y permisos Pages/OIDC | Publica solo el redirector de GitHub Pages |
| Push a GitHub con un post EN, transformador, sindicador, test o workflow DEV.to modificado | Workflow `devto-syndication.yml` | Tests verdes, `DEV_TO_API_KEY`, `republish: [dev]`, `permalink` y guarda de 21 días para creaciones | Con secreto crea un borrador o actualiza un artículo; sin secreto termina sin tocar DEV.to |
| Respuesta DEV.to 2xx | Actualización del registro y commit del bot | `contents: write` y datos válidos de la API | Guarda id/URL en `_data/distribucion.yml`; ese commit nace solo en GitHub y debe integrarse antes del próximo push dual |
| 09:30 local cada día | `difusion-cadencia.timer` | Timer habilitado, repositorio accesible y `_data/distribucion.yml` actualizado | Vigila Mastodon y Bluesky por idioma, DEV D4 y Medium D10; un vencimiento de hasta 30 días dispara toast |
| Orden humana explícita | DEV.to, Medium, LinkedIn o `cucharadas-difusion publish --live` | Revisión del borrador, autenticación y reglas del destino | Publicación externa verificable; el borrador DEV.to por sí solo no cierra D4 |

## Estado observado (histórico al 2026-09-06)

- El timer está habilitado y activo; la corrida del 2026-09-06 falló y activó `OnFailure`.
- El rojo accionable contiene cinco artefactos del post de Nushell: Mastodon y Bluesky en ES y EN, más DEV.to.
- El timer reporta además ocho artefactos históricos fuera de su ventana accionable de 30 días. Las respuestas EN de CASEN y AI Quota se reconciliaron el 2026-09-06 contra las APIs públicas de ambas redes.
- `distribution_audit` ejecuta la auditoría completa en pipelines programados después de Pages; el timer local conserva la ventana de 30 días.
- El catálogo declaraba DEV como feed; el mecanismo efectivo crea borradores por API y deja la publicación como acción manual.
- El supuesto 404 del post III provenía de un `_site` reutilizado y obsoleto: el enlace `/en/en/...` estaba en una tarjeta relacionada generada el 2026-08-31, no en el Markdown fuente. Un build limpio en destino vacío validó los 18 posts.
- Las comprobaciones locales de enlaces deben construir en un directorio temporal vacío; reutilizar `_site` mezcla páginas viejas con el commit actual y produce diagnósticos falsos.
- Telegram no se dispara desde el commit: el aviso explícito exige build, ambos remotos, CI y URL pública, y vive en un commit separado del cambio funcional.

## Cierre posdespliegue de Mastodon y Bluesky

El hook de commit solo registra elegibilidad y el timer solo audita pendientes.
No existe un hook Git nativo `post-push`: un push por sí solo no envía a estas redes.
Después de verificar Pages, el operador que tenga autorización de envío ejecuta
`scripts/post_push_difusion.sh REF --live` sobre el borrador revisado. Sin `--live`
es un simulacro. El comando enlaza envío, verificación pública, reconciliación por
ref y auditoría estricta de las cuatro URLs ES/EN. El registro resultante se
incluye en el siguiente commit/push; ningún `[x]` de elegibilidad lo sustituye.

Avalúos II se omitió al declarar incorrectamente `social: false` en ambas versiones.
Se restauró `true`; excluir estas redes exige ahora una razón explícita aun cuando
se declaren LinkedIn/X. El perfil `source` verifica esa política antes de Pages.
La evidencia de reparación y envío está en
[`releases/20260912-social-closeout/`](releases/20260912-social-closeout/).

## Runbook reproducible para un lanzamiento social

Este es el único orden autorizado para Mastodon y Bluesky. El hook resuelve
elegibilidad; no convierte un commit ni un push en autorización o en envío.

| Carril | Alcance automático | Decisión o verificación humana que permanece |
|---|---|---|
| Mastodon y Bluesky | Preparación, envío explícito y verificación por API | Autorizar el envío y revisar la copia antes de `--live` |
| DEV.to | Crear o actualizar un borrador cuando el workflow tiene secreto | Publicar el borrador y comprobar el canónico |
| Medium, LinkedIn y X | Ninguno | Preparar, publicar, verificar y reconciliar la URL pública |
| Feeds y directorios | Resolver elegibilidad y monitorear la deuda | Enviar o insistir y comprobar la inclusión externa |

| Fase | Operador / script | Evidencia de salida | No hacer |
|---|---|---|---|
| 1. Declarar | Editar las dos versiones del post y `distribution` | `social: true` en ES/EN; `ref` idéntico; `slug` en `_data/distribucion.yml` igual al último segmento del permalink | Cambiar título, fecha o permalink para abrir una campaña |
| 2. Resolver | `post-commit-difusion` o `destinations status REF` | Checklist `listo`, `bloqueado` o `pendiente-verificar` por destino | Leer `listo` como publicación |
| 3. Validar y desplegar | Suite de difusión, build limpio, commit selectivo, push y Pages | Tests, artefacto, SHA y URL canónica pública | Enviar mientras el sitio o su OG todavía no están disponibles |
| 4. Preparar y revisar | `cucharadas-difusion prepare`/`review` y paquete local | Borrador válido, texto final y aprobación de ambas redes | Publicar un borrador vacío, sin revisión o con datos no trazables |
| 5. Enviar y verificar | `scripts/post_push_difusion.sh REF --live --confirm "PUBLICAR REF"` | Cuatro piezas ES/EN, tarjetas, URLs públicas y ledger XDG | Repetir a mano un envío parcial; el comando lo reanuda de forma idempotente |
| 6. Reconciliar | El cierre ejecuta `reconciliar_distribucion.rb --aplicar` | URLs raíz ES y respuesta EN en `_data/distribucion.yml`; gate social estricto verde para el ref | Declarar éxito si las URLs siguen solo en el ledger ignorado |
| 7. Versionar el cierre | Commit selectivo y push dual del ledger reconciliado | SHA idéntico en remotos y registro versionado | Asumir que el push original contiene las URLs sociales |

### Preflight mínimo

```bash
cd /home/ende/Descargas/programaciones/activos/3cucharadas
PYTHONPATH=difusion/src /opt/entornos/3cucharadas-difusion/bin/python -m pytest difusion/tests -q
JEKYLL_ENV=production bundle exec jekyll build -d "$(mktemp -d /tmp/3c-difusion.XXXXXX)"
PYTHONPATH=difusion/src /opt/entornos/3cucharadas-difusion/bin/python -m cucharadas_difusion.cli --repo . destinations status REF
curl -fsS -A 'Mozilla/5.0' -o /dev/null -w '%{http_code}\n' 'https://open.spotify.com/episode/<ID>'
```

El envío real requiere una orden humana vigente y una revisión local previa. El
comando de cierre no publica DEV.to, Medium, LinkedIn, X ni otro `ref`; solo
Mastodon y Bluesky del `REF` solicitado.

### Cápsulas de audio

La cápsula se declara en `audio.plataformas` del post y se aloja fuera del sitio.
Una raíz de Bluesky puede incluir una URL secundaria únicamente si es una de esas
URLs declaradas; el publicador crea su facet enlazable y conserva la tarjeta OG
del artículo. Mastodon añade además el enlace UTM al artículo. La versión EN no
debe presentar una cápsula ES como si fuera audio en inglés: puede mencionarla
como tal o enlazar solo el artículo.

La copy final, las URLs de la cápsula y la condición de aprobación quedan en
`difusion/paquetes/<ref>/`; el borrador operativo y su ledger viven fuera del
repositorio. Ninguno reemplaza al otro: el paquete permite revisión, el ledger
previene duplicados y `_data/distribucion.yml` conserva la evidencia versionada.
Spotify puede responder 403 a consultas sin User-Agent para episodios recientes;
el 200 con un User-Agent de navegador es una precondición del lanzamiento, no una
consecuencia de haber escrito `audio:`.

### Límites del hook y del ledger

`post-commit-difusion` usa el Python disponible en `PATH`, nunca bloquea un
commit y escribe una caché ignorada en `difusion/state/`. No acredita que la
resolución corresponda al SHA desplegado, especialmente si el worktree tenía
cambios sin commit. Antes de `--live`, se resuelve otra vez con el intérprete
fijado del preflight sobre la revisión aprobada; se conserva el JSON solo como
ayuda de diagnóstico.

El ledger XDG es la única protección local contra reenvíos. No ejecutar dos
cierres simultáneos ni reemplazarlo; si falta, está corrupto o cambió de equipo,
primero se comparan las APIs públicas, el ledger y `_data/distribucion.yml`.
Un rollback remoto vigente todavía requiere retirar manualmente sus URLs del
registro versionado, commit y push: la reconciliación actual añade publicaciones
vigentes, pero no borra evidencia histórica ya versionada.

### Recuperación

| Situación | Acción segura | Criterio de salida |
|---|---|---|
| `partial` | Repetir `scripts/post_push_difusion.sh REF --live --confirm "PUBLICAR REF"` | La red ya emitida queda `skipped`; solo se completa la faltante |
| `published_unverified` | Ejecutar `cucharadas-difusion verify REF` sin volver a publicar | Tarjetas, idioma, orden y facets comprobados desde APIs públicas |
| Publicación externa informada sin URL | Conservar copy y buscar URL; no reenviar | URL o recibo comprobable en el ledger y luego reconciliado |
| Cambio del post después del borrador | Preparar y revisar de nuevo | Metadatos del borrador coinciden con el post actual |

## Cómo leer los gates sin mezclar estados

| Evidencia | Qué demuestra | Qué no demuestra |
|---|---|---|
| Pipeline verde sobre un SHA | Ese árbol versionado construyó y pasó sus gates | Que el checkout enlazado al timer tenga el mismo SHA o contenido |
| `verify_distribution_done.rb` | Deuda completa registrada por plataforma e idioma | Que una publicación externa sin registrar no exista |
| `verify_distribution_done.rb --ventana 30` | Pendientes accionables recientes para el aviso diario | Que la deuda histórica esté saldada |
| DEV `GET /api/articles/:id` con HTTP 200 | El artículo está publicado y accesible | El estado de otros IDs privados |
| DEV `GET /api/articles/:id` con HTTP 404 | El ID no está disponible públicamente | Si sigue como borrador o fue eliminado |

Un `404` de DEV exige una consulta autenticada a `articles/me/unpublished` antes de
afirmar que el borrador todavía existe. El secreto del workflow no se extrae para
hacer esa comprobación: se usa desde GitHub Actions o desde una sesión local que ya
tenga `DEV_TO_API_KEY`, sin imprimirlo.

El timer ejecuta los archivos del `WorkingDirectory` configurado en systemd, no el
árbol que esté verde en el remoto. Antes de interpretar su salida se comparan
`git rev-parse HEAD`, `git status --short` y el SHA remoto. Si el checkout está
atrasado o contiene cambios divergentes, se reproduce el gate en un worktree limpio.

El verificador del artefacto presupone que Vite ya produjo sus manifests. La secuencia
local equivalente a CI es `npm ci`, checks/tests Node, ambos builds Vite, build Jekyll
en destino vacío y, recién entonces, `verify_site_artifact.rb` y
`verify_distribution_readiness.rb`. `Vite manifest is missing` después de ejecutar
solo Jekyll prueba una precondición omitida, no un defecto del artefacto completo.

## Transformación Jekyll a DEV.to

- Convierte `relative_url` y atributos HTML relativos a URLs absolutas bajo `https://3cucharadas.cl`.
- Resuelve `site.url`, `site.baseurl`, `page.url`, `page.title` y `page.description`; elimina otras salidas Jekyll con aviso.
- Conserva solo una allowlist explícita de tags Forem, incluidos `katex`, `embed`, `link` y `youtube`.
- Convierte matemáticas `$$ ... $$` a bloques `{% katex %}` y elimina extensiones Kramdown.
- Expande `include gallery` desde el front matter y conserva todas sus imágenes con URL absoluta.
- Genera front matter DEV.to con `published: false`, `canonical_url`, portada, hasta cuatro tags y `ai_disclosure_level: some_ai`; en el editor Markdown básico la publicación humana cambia `published` a `true`.
- Falla antes de la API si queda `relative_url`, `site.*`, `page.*`, una salida `{{ ... }}`, Kramdown o un tag Liquid no permitido fuera de código.
- `ruby scripts/syndicate_devto.rb --export-dir DIR` escribe los siete Markdown derivados exactos sin requerir clave ni llamar a la API.
- Antes de un `PUT`, consulta los artículos publicados y no publicados: el front matter refleja el estado remoto y el atributo JSON `published` se omite, por lo que una actualización no publica ni despublica por accidente.
- `ruby scripts/syndicate_devto.rb --existing-drafts-only` actualiza todos los borradores que coinciden por `canonical_url`, no crea artículos y no toca los ya publicados.

Contratos externos: [guía oficial del editor DEV](https://dev.to/p/editor_guide) y [API v1 de Forem](https://developers.forem.com/api/).
