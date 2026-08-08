# Reversión de los cambios de endurecimiento

Cada cambio se revierte por separado. El orden importa poco: no hay dependencias
entre ellos. Lo que sí importa es no revertir a ciegas — cada sección dice qué
riesgo se vuelve a aceptar.

Nada de lo que sigue toca cuentas, DNS, Cloudflare ni NIC Chile. La reversión del
borde tiene su propio procedimiento en
[`../runbook_cloudflare_headers.md`](../runbook_cloudflare_headers.md), sección
"Rollback".

## Antes de revertir cualquier cosa

```bash
python3 .agent/checks/security.py --pipeline
python3 .agent/checks/security.py --liquid-escaping
python3 .agent/checks/security.py --actions-pinned
python3 .agent/checks/security.py --dependabot
```

Los cuatro comprobadores fallarán después de revertir lo que corresponda. Eso es
lo esperado, y es la señal de que el pipeline de CI también fallará: los
comprobadores existen para que la reversión sea deliberada y no accidental.

---

## 1. `.gitlab-ci.yml` — imagen por digest

**Síntoma que justificaría revertir:** el runner no encuentra el digest (imagen
purgada del registry) y el job falla en el `pull` antes de ejecutar nada.

**Reversión mínima y preferida** — no volver a la etiqueta flotante, sino
resolver el digest vigente:

```bash
TOKEN=$(curl -fsSL "https://auth.docker.io/token?service=registry.docker.io&scope=repository:library/ruby:pull" | jq -r .token)
curl -fsSL -o /dev/null -D - -H "Authorization: Bearer $TOKEN" \
  -H "Accept: application/vnd.oci.image.index.v1+json, application/vnd.docker.distribution.manifest.list.v2+json" \
  https://registry-1.docker.io/v2/library/ruby/manifests/3.3 | grep -i docker-content-digest
```

Reemplazar el digest en la línea `image:` y volver a correr el pipeline.

**Reversión total** (`image: ruby:3.3`): se vuelve a aceptar que el mismo commit
construya con una base distinta cada semana. El build deja de ser reproducible.

## 2. `.gitlab-ci.yml` — Node por tarball verificado

**Síntoma que justificaría revertir:** `sha256sum -c` falla. **Esto no es un
motivo para revertir**, es el control funcionando. Antes de tocar nada,
comprobar contra la fuente:

```bash
curl -fsSL https://nodejs.org/dist/v24.18.0/SHASUMS256.txt | grep linux-x64.tar.xz
```

- Si coincide con `NODE_SHA256_X64` y el job sigue fallando: problema de
  descarga, no de integridad. Reintentar.
- Si **no** coincide: no actualizar el valor por inercia. Un tarball publicado
  que cambia de hash es exactamente el escenario que este control detecta.
  Investigar antes de subir el número.

**Para subir de versión de Node** (procedimiento normal, no reversión):

1. Actualizar `.nvmrc` y `engines.node` en `package.json`.
2. Actualizar `NODE_VERSION`, `NODE_SHA256_X64` y `NODE_SHA256_ARM64` en
   `.gitlab-ci.yml` con los valores de `https://nodejs.org/dist/v<X.Y.Z>/SHASUMS256.txt`.
3. Correr `npm ci && npm run check:catastro && npm run test:catastro && npm run build:catastro`.

**Reversión total** (volver a `curl … | bash -` de NodeSource): se reintroduce
ejecución de código remoto como root dentro del job que publica producción. Es el
riesgo P0 del modelo de amenazas. No hacerlo sin una razón escrita.

## 3. `_includes/news-widget.html` y `scripts/fetch_news.py` — allowlist de esquema

**Síntoma que justificaría revisar:** un titular aparece sin enlace, renderizado
como `<span class="news-widget__link">` en vez de `<a>`.

Eso significa que el feed entregó una URL que no empieza por `http://` ni
`https://`. Diagnóstico antes de tocar el código:

```bash
jq -r '.articles[] | "\(.source_label)\t\(.link)"' _data/feedly_news.json
```

Si el enlace vacío corresponde a un feed que emite URLs relativas, la corrección
correcta es resolverlas contra la base del feed en `scripts/fetch_news.py`, **no**
ampliar la allowlist.

**Reversión total** (volver a `href="{{ article.link }}"`): se vuelve a aceptar
que un feed ajeno hornee `javascript:` o `data:text/html;…` en el HTML publicado.

## 4. Acciones pinneadas a SHA

**Síntoma que justificaría revertir:** un workflow falla con "unable to resolve
action … repository not found" tras un cambio del upstream.

**Reversión mínima y preferida** — re-resolver el SHA, no volver a la etiqueta:

```bash
gh api repos/actions/checkout/commits/v4 --jq '.sha'
gh api repos/actions/configure-pages/commits/v5 --jq '.sha'
gh api repos/actions/upload-pages-artifact/commits/v5 --jq '.sha'
gh api repos/actions/deploy-pages/commits/v5 --jq '.sha'
gh api repos/actions/setup-python/commits/v5 --jq '.sha'
```

Sustituir el SHA y mantener el comentario `# vX.Y.Z` al día.

**Reversión total** (volver a `@v4` / `@v5`): `devto-syndication.yml` vuelve a
ejecutar código movible con `contents: write` y `DEV_TO_API_KEY`;
`github-pages-redirector.yml`, con `pages: write` e `id-token: write`.

## 5. `.github/dependabot.yml`

Revertir es borrar el archivo. No rompe nada: Dependabot deja de abrir PRs.

Si el problema es el ruido y no el mecanismo, bajar
`open-pull-requests-limit` o cambiar `interval: "weekly"` por `"monthly"` es
preferible a eliminarlo.

## 6. `SECURITY.md` y `docs/security/`

Documentación pura. Borrarlos no cambia el comportamiento del sitio ni del
pipeline. `docs/` está en `exclude:` de `_config.yml`, así que nada de esto se
publica.

Lo único con efecto externo es `SECURITY.md` en la raíz: GitHub y GitLab lo
muestran en la pestaña de seguridad del repositorio. Borrarlo retira el canal de
reporte publicado sin retirar la dirección de correo, que sigue en `README.md` y
en `_pages/about.md`.
