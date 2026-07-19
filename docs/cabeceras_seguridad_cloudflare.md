# Cabeceras de seguridad: por qué `_headers` no basta y cómo aplicarlas

Estado: **el sitio se publica hoy sin política de seguridad.** El archivo `_headers`
existe, se despliega y el servidor lo ignora. Este documento explica por qué y deja los
pasos exactos para resolverlo.

## Diagnóstico

### Quién sirve el sitio

**GitLab Pages, sin proxy delante.** Verificado:

```
dig +short www.3cucharadas.cl CNAME  → tatanlabra.gitlab.io.
dig +short 3cucharadas.cl A          → 35.185.44.232   (Google Cloud, infra de GitLab)
dig +short 3cucharadas.cl NS         → remy/marge.ns.cloudflare.com
```

Cloudflare está solo como **DNS (nube gris)**, no proxea el apex. El contraste con un
subdominio que sí proxean lo confirma:

| | `3cucharadas.cl` | `tiles.3cucharadas.cl` |
|---|---|---|
| IP | `35.185.44.232` (GCP) | anycast Cloudflare |
| `server:` | ausente | `cloudflare` |
| `cf-ray:` | ausente | presente |

Nota: la ausencia de `server:` **no** indica proxy — el daemon de GitLab Pages
simplemente no la emite. Emite `x-request-id` y `vary: Origin`, ambos presentes.

GitHub Pages queda descartado: el workflow `github-pages-redirector.yml` publica sin
`CNAME`, o sea vive en `tatanlabra.github.io`, no en el dominio.

### Causa raíz

**GitLab Pages nunca ha soportado `_headers`.** No es un problema de formato ni de
ubicación. Verificado sobre el código fuente de `gitlab-org/gitlab-pages`:

- `rg '_headers'` sobre todo el árbol → **cero resultados**
- `_redirects`, en cambio, tiene parser completo en `internal/redirects/redirects.go`
- `internal/customheaders/customheaders.go` son 13 líneas que solo copian cabeceras
  desde `config.General.CustomHeaders`, poblado por el flag CLI `-header`, es decir
  `gitlab_pages['headers']` en `gitlab.rb`: **configuración de instancia, solo admin**.
  No existe ninguna ruta desde el artefacto publicado.
- [Issue #50](https://gitlab.com/gitlab-org/gitlab-pages/-/issues/50), "A way to
  customize some headers", **abierta desde marzo de 2017**.

Esto explica con precisión lo observado: la única cabecera que llega es
`permissions-policy: interest-cohort=()`, que GitLab.com pone a nivel de instancia. Por
eso aparece el opt-out de FLoC pero no el `geolocation=(), microphone=(), camera=()` que
declara nuestro archivo.

**Corrección a un supuesto previo:** la creencia de que GitLab Pages soporta `_headers`
desde la versión 16.7 es incorrecta; probablemente se confundió con `_redirects`, que sí
tiene soporte real estilo Netlify.

## Solución: Cloudflare Transform Rules

Es el camino natural porque la zona ya está en Cloudflare y ya proxean
`tiles.3cucharadas.cl`. **No requiere ningún cambio en el repositorio.**

### 1. Activar el proxy

Cloudflare → **DNS**: pasar el registro A de `3cucharadas.cl` (`35.185.44.232`) de gris
a **naranja (Proxied)**. Idem el CNAME de `www`.

Cloudflare → **SSL/TLS → Overview**: modo **Full (strict)**.

### 2. Resolver el certificado antes de nada

El sitio usa el certificado Let's Encrypt que GitLab Pages provisiona solo. Con el proxy
activo, la renovación ACME `http-01` puede fallar y el sitio caería al vencer.

**Recomendado**: SSL/TLS → Origin Server → crear un **Cloudflare Origin Certificate**
(15 años), subirlo en GitLab → Settings → Pages → dominio → Certificate, y desactivar el
toggle de Let's Encrypt automático.

*No* quitar el registro TXT de verificación del dominio en GitLab.

### 3. Transform Rules

Cloudflare → **Rules → Transform Rules → Modify Response Header → Create rule**.

**Regla 1 — seguridad global.** Expresión: `hostname eq "3cucharadas.cl"`.
Acción **Set** para cada una (⚠️ *Set*, no *Add*: el origen ya manda su propia
`permissions-policy` y *Add* dejaría dos cabeceras en conflicto):

| Cabecera | Valor |
|---|---|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=(), interest-cohort=()` |
| `Content-Security-Policy-Report-Only` | *(ver `_headers` en la raíz del repo; es la fuente única del valor)* |

**Regla 2 — artefactos Vite con hash.** Expresión:
`starts_with(http.request.uri.path, "/assets/dist/")`
→ `Cache-Control: public, max-age=31536000, immutable`

**Regla 3 — datos abiertos.** Expresión:
`starts_with(http.request.uri.path, "/assets/data/")`
→ `Access-Control-Allow-Origin: *`

El plan Free alcanza: Transform Rules están en todos los planes, con 10 reglas activas.
Ninguna de estas cabeceras está en la lista restringida de Cloudflare (que solo bloquea
`cf-*`, `x-cf-*`, `server`, `eh-cache-tag`, `eh-cdn-cache-control`).

### 4. Verificar

```bash
curl -sI https://3cucharadas.cl/ | grep -iE 'x-content-type|x-frame|referrer-policy|permissions-policy|content-security'
```
Deben aparecer las cinco. La `permissions-policy` debe salir **una sola vez** y con los
cuatro directivos — si aparece dos veces, se usó *Add* en lugar de *Set*.

## Lo que NO sirve

**`<meta http-equiv>`** es incompatible con la estrategia actual. Cobertura real:

| Cabecera | ¿vía meta? |
|---|---|
| `Content-Security-Policy-Report-Only` | **imposible**, no existe en meta |
| CSP enforcing | parcial: `frame-ancestors`, `report-uri` y `sandbox` se ignoran |
| `Referrer-Policy` | sí, pero con `<meta name="referrer">` |
| `X-Content-Type-Options` | no |
| `X-Frame-Options` | no |
| `Permissions-Policy` | no |

Como el proyecto usa CSP en **Report-Only** deliberadamente —por GA4, Disqus y el visor
Catastro— la vía meta no puede expresar la política que necesitamos.

## Alternativa si se descarta Cloudflare

Migrar el hosting a **Cloudflare Pages**, que sí soporta `_headers` nativo con el mismo
archivo sin cambios, publicando con `wrangler pages deploy public` desde el job `pages`
del CI existente. Es más invasivo y no se recomienda mientras la opción de Transform
Rules no toque el repositorio.
