# Modelo de amenazas — 3cucharadas

Ordenado por **impacto sobre el HTML que recibe un visitante de
`https://3cucharadas.cl`**, no por lo llamativo del hallazgo. El criterio importa
porque el plan original ordenaba al revés: ponía GitHub Actions arriba dando por
hecho que GitHub publicaba producción, cuando quien publica es GitLab.

Fecha de este ordenamiento: 2026-08-07. Alcance: el repositorio y su cadena de
publicación. La configuración de Cloudflare y de NIC Chile se documenta en
[`../runbook_cloudflare_headers.md`](../runbook_cloudflare_headers.md).

## Cómo llega el código a producción

```
commit en main
   └─ push a origin (dos URLs: GitLab + GitHub)
        ├─ GitLab CI  → build_site → jekyll build -d public → job pages → 3cucharadas.cl
        │                  ↑ aquí entra TODO lo externo: imagen base, Node, gemas,
        │                    paquetes npm y los feeds RSS de terceros
        └─ GitHub      → espejo público + redirector estático (gh-pages-redirect)
                           ↑ no toca el contenido de 3cucharadas.cl
```

Todo lo que se ejecute dentro de `build_site` puede escribir en `public/`. Esa es
la frontera de confianza real.

---

## P0 — Ejecución remota sin verificar dentro del job que publica

**Estado: corregido.**

`.gitlab-ci.yml` instalaba Node con:

```
curl -fsSL https://deb.nodesource.com/setup_24.x | bash -
```

Un script remoto ejecutado **como root** dentro del job que produce el artefacto
publicado, sin fijar ni verificar nada. El atacante no necesita tocar el
repositorio: le basta comprometer NodeSource, o la ruta de red hasta él, para
inyectar código en `public/` y desde ahí en el navegador de cada visitante. No
queda rastro en ningún diff, porque el repositorio no cambia.

Agravante: `image: ruby:3.3` era una etiqueta flotante, así que ni siquiera la
base era la misma entre dos builds del mismo commit. Un build no reproducible no
se puede auditar después del hecho.

Corrección aplicada:

- Imagen base fijada por digest: `ruby:3.3@sha256:81c61dc…`.
- Node instalado desde el tarball oficial de `nodejs.org` y verificado contra un
  SHA256 **declarado en `.gitlab-ci.yml`**, no descargado junto al archivo. Esa
  distinción es el punto: verificar contra el `SHASUMS256.txt` bajado en el mismo
  momento no demuestra nada, porque quien pueda alterar el tarball puede alterar
  la lista. El valor fijado en el repositorio sí es revisable en un diff.
- Si el checksum no coincide, `sha256sum -c` falla y el job se detiene antes de
  construir.

**Deuda que esto crea:** un digest fijo no recibe parches. Hay que refrescarlo a
mano cuando se quieran actualizaciones de Debian o de Ruby, y Dependabot no cubre
imágenes de GitLab CI. Se acepta a conciencia: una base predecible que se
actualiza cuando alguien lo decide es preferible a una base que cambia sola.
Revisar junto con el bump de `.nvmrc`.

**Residual:** el runner compartido de GitLab.com sigue siendo infraestructura de
un tercero, y `npm ci` y `bundle install` siguen descargando de registries
públicos. Los lockfiles (`package-lock.json`, `Gemfile.lock`) fijan versiones y
hashes; el registry sigue siendo confianza depositada.

---

## P1 — Contenido de terceros horneado en el HTML publicado

**Estado: corregido en dos capas.**

`scripts/fetch_news.py` descarga feeds RSS ajenos **durante el build de CI** y
`_includes/news-widget.html` los renderiza. Todos los campos del widget pasaban
por `| escape` menos uno: el `href`.

```liquid
<a href="{{ article.link }}" target="_blank" rel="noopener noreferrer">
```

`article.link` sale de `entry.get("link", …)`, es decir, de texto controlado por
el feed. Un feed hostil o comprometido podía emitir `javascript:` o
`data:text/html;…` y quedaba horneado en el HTML publicado.
`rel="noopener noreferrer"` **no mitiga esto**: limita el acceso a
`window.opener` y el `Referer`, no filtra esquemas de URL.

Corrección:

1. **En la ingesta** (`scripts/fetch_news.py`, `_safe_link`): allowlist de
   esquema http/https. Se recortan control chars de los extremos y se eliminan
   tab, LF y CR **antes** de mirar el prefijo, porque el parser de URL del
   navegador hace exactamente eso: `"java\nscript:"` se navega como
   `javascript:`, pero un `startswith` ingenuo lo deja pasar. Si no hay URL
   aceptable, se devuelve `""`.
2. **En la plantilla** (`_includes/news-widget.html`): la misma allowlist en
   Liquid, más `| escape` sobre el valor emitido para que no pueda cerrar el
   atributo. Si no pasa, se conserva el titular como texto plano en un `<span>`.

La segunda capa no es redundancia decorativa: `_data/feedly_news.json` puede
venir de un commit anterior o de una ejecución del script previa a esta
corrección, y la plantilla es lo último que toca el dato antes de publicarlo.

---

## P1 — Drift silencioso de dependencias

**Estado: corregido, con una salvedad operativa.**

`package.json` fija versiones exactas y `package-lock.json` está versionado. Ese
pinning es correcto, pero sin nadie que avise convierte el atraso en algo
invisible: los gates del repositorio comprueban que el build funcione, no que las
dependencias estén al día.

Se añadió `.github/dependabot.yml` con `bundler`, `npm` y `github-actions`,
semanal.

**Salvedad:** `origin` tiene dos URLs de push (GitLab + GitHub), o sea GitHub es
un espejo alimentado desde la máquina local. Dependabot solo abre PRs en GitHub.
Fusionar uno allí deja `main` de GitHub por delante de GitLab y el siguiente push
local se rechaza por non-fast-forward. **Los PRs de Dependabot son un aviso, no
el camino de integración**: hay que aplicar el bump en local, correr los gates y
empujar a ambos remotos.

---

## P2 — GitHub Actions con permisos de escritura

**Estado: pinneado. No toca producción.**

Esto estaba en lo alto del plan v1.0 por la premisa equivocada de hosting. Sigue
importando —el repositorio es público y un workflow comprometido puede alterarlo—
pero el sitio que ve un visitante no depende de ello.

| Workflow | Permisos | Superficie |
|---|---|---|
| `devto-syndication.yml` | `contents: write` + `secrets.DEV_TO_API_KEY`, dispara en push a `main`, hace `git push` de vuelta | La peor del repositorio en GitHub |
| `github-pages-redirector.yml` | `pages: write` + `id-token: write` | Controla el redirector y puede pedir un token OIDC a nombre del repositorio |
| `fetch-news.yml` | `contents: read`, manual | Baja |

Las cinco referencias a acciones pasaron de etiqueta móvil a SHA de commit de 40
caracteres, resueltos contra el upstream real (`gh api
repos/<owner>/<repo>/commits/<tag>`), con la versión humana en un comentario al
lado. Una etiqueta como `@v4` se puede reapuntar por quien controle el
repositorio de la acción; un SHA no.

**Residual:** el secreto `DEV_TO_API_KEY` sigue existiendo y el workflow sigue
disparando automáticamente en push. Reducirlo es cuestión de política de cuenta
(entornos protegidos, revisión obligatoria), no de este archivo.

---

## P2 — Superficie de cliente del visor Catastro SII

**Estado: verificado, sin acción.** Se deja registrado para que una auditoría
futura no vuelva a gastar el mismo tiempo.

- Los dos `innerHTML = ""` de `catastro_sii_brecha/app.js` (líneas 262 y 334)
  vacían un `<select>` y lo repueblan con `createElement` + `textContent`. No son
  sinks explotables.
- Los parámetros de URL se validan con allowlist cerrada y expresiones regulares
  en `assets/src/catastro_sii/state.ts`; `preview.ts` además exige host local
  para el modo preview.
- MapLibre y PMTiles están autoalojados, sin claves de API.
- El CORS de R2 es una allowlist estricta, no un comodín.
- Font Awesome se carga con `integrity` + `crossorigin`.
- Disqus es click-to-load.
- Cero secretos versionados. Los dos únicos archivos de datos versionados son
  agregados comunales públicos por diseño.

---

## P3 — Borde: cabeceras, TLS y CSP

**Estado: implementado en Cloudflare, con pendientes deliberados.**

`_headers` es **inerte** en GitLab Pages. No es un problema de formato: GitLab
Pages nunca ha soportado ese archivo (cero referencias en el código de
`gitlab-org/gitlab-pages`, frente a un parser completo para `_redirects`; issue
#50 abierta desde 2017). El archivo se conserva como fuente única de la política;
quien la aplica son las Response Header Transform Rules de Cloudflare, activas
desde 2026-07-19.

Pendientes por decisión, no por olvido: HSTS, DNSSEC, verificación desde el panel
del modo SSL/TLS Full (strict), y la promoción de la CSP de `Report-Only` a
bloqueante. El detalle, con los `curl` medidos, está en
[`../runbook_cloudflare_headers.md`](../runbook_cloudflare_headers.md) y en
[`../cabeceras_seguridad_cloudflare.md`](../cabeceras_seguridad_cloudflare.md).

---

## P3 — Deriva de configuración

Ninguno es explotable hoy. Se documentan porque el costo de arreglarlos sube con
el tiempo y porque un inventario incompleto es lo que produce auditorías que
repiten trabajo.

| Deriva | Dónde | Por qué importa |
|---|---|---|
| Shortname de Disqus `https-tatanlabra-gitlab-io-3cucharadas` | `_config.yml:38` | Apunta al dominio antiguo `tatanlabra.gitlab.io`. Los hilos quedan asociados a una identidad que ya no es la del sitio; migrar el shortname después de acumular más comentarios es más caro |
| reCAPTCHA muerto | `_includes/comments.html:98` | `{% if site.reCaptcha.siteKey %}` — la clave no existe en `_config.yml`, así que la rama nunca se activa. Es código de Minimal Mistakes que carga `google.com/recaptcha/api.js` si alguien define esa clave sin querer |
| Staticman muerto | `_includes/comments.html:135` | Postea a `api.staticman.net` con `site.repository` y `site.staticman.branch`; ninguna de las dos existe en la configuración. Inalcanzable mientras `comments.provider` sea `disqus` |
| GoatCounter sin SRI y con URL protocol-relative | `_includes/analytics-providers/goatcounter.html:4` | `src="//gc.zgo.at/count.js"` sin `integrity` ni `crossorigin`, mientras Font Awesome sí los lleva (`_includes/head.html:45-46`). La inconsistencia es el hallazgo: o se exige SRI a los scripts de terceros o no. GoatCounter no publica hashes estables para ese archivo, así que aplicar SRI implica fijar una versión concreta |

Los cuatro están fuera del alcance de esta fase: viven en archivos que edita otro
trabajo en paralelo.
