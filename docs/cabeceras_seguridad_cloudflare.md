> **Estado histórico y registro de implementación.** Este documento conserva el
> diagnóstico de por qué GitLab Pages ignoraba `_headers`. La implementación y los
> procedimientos vigentes están en el
> [`runbook operativo`](runbook_cloudflare_headers.md).
>
> El 19 de julio de 2026 se implementaron y habilitaron las reglas de cabecera de
> respuesta de Cloudflare descritas abajo. No se instaló un Cloudflare Origin
> Certificate. La CSP sigue deliberadamente en modo **Report-Only**.

# Cabeceras de seguridad: diagnóstico histórico e implementación realizada

## Implementación realizada el 19 de julio de 2026

Se habilitaron tres **Response Header Transform Rules** en Cloudflare. Los registros
A, AAAA y `www` ya estaban en modo *Proxied* antes de este cambio.

| Regla activa | Filtro | Cabeceras configuradas con `Set static` |
|---|---|---|
| `seguridad-global` | `(http.host eq "3cucharadas.cl" or http.host eq "www.3cucharadas.cl")` | `X-Content-Type-Options: nosniff`; `X-Frame-Options: DENY`; `Referrer-Policy: strict-origin-when-cross-origin`; `Permissions-Policy: geolocation=(), microphone=(), camera=(), interest-cohort=()`; `Content-Security-Policy-Report-Only` con la CSP vigente. |
| `cache-assets-dist` | `(http.host eq "3cucharadas.cl" and starts_with(http.request.uri.path, "/assets/dist/"))` | `Cache-Control: public, max-age=31536000, immutable` |
| `cors-assets-data` | `(http.host eq "3cucharadas.cl" and starts_with(http.request.uri.path, "/assets/data/"))` | `Access-Control-Allow-Origin: *` |

Los filtros de las dos últimas reglas excluyen intencionalmente
`tiles.3cucharadas.cl`, que conserva sus cabeceras CORS condicionales y de `Range`
para PMTiles.

### Evidencia de verificación

- La respuesta principal entregó las cinco cabeceras de seguridad; `Permissions-Policy`
  apareció una sola vez con los cuatro directivos esperados.
- La CSP se entregó como `Content-Security-Policy-Report-Only`, sin pasar aún a modo
  bloqueante.
- `https://3cucharadas.cl/assets/data/catastro_sii/manifest.json` respondió `200` con
  `Access-Control-Allow-Origin: *`.
- `scripts/catastro_sii/verify_r2_cors.sh` pasó, incluido su control negativo; las
  solicitudes `Range` y CORS del subdominio `tiles` quedaron intactas.
- `cache-assets-dist` quedó activa. No había entonces un artefacto Vite publicado bajo
  `/assets/dist/` que respondiera `200` para confirmar la cabecera de caché final: la
  URL con el hash local respondió `404`.

### Pendiente deliberado

No se verificó desde el panel el modo SSL/TLS **Full (strict)** y no debe afirmarse
como configurado hasta revisarlo. HTTP ya redirige a HTTPS; **Always Use HTTPS** sigue
siendo una decisión opcional del panel. HSTS tampoco se activó: debe evaluarse sólo
después de un periodo estable. No se debe instalar un Origin Certificate como parte de
esta implementación.

## Diagnóstico

### Quién sirve el sitio

El siguiente era el registro del diagnóstico original; **no describe la configuración
actual**, ya que los registros del sitio estaban en modo *Proxied* antes de aplicar las
reglas de cabecera:

```
dig +short www.3cucharadas.cl CNAME  → tatanlabra.gitlab.io.
dig +short 3cucharadas.cl A          → 35.185.44.232   (Google Cloud, infra de GitLab)
dig +short 3cucharadas.cl NS         → remy/marge.ns.cloudflare.com
```

En ese momento, la conclusión anotada fue que Cloudflare estaba solo como **DNS (nube
gris)** y no proxyaba el apex. El contraste con un subdominio que sí proxyaba se
documentó así:

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

## Implementación Cloudflare: referencia histórica completada

Cloudflare fue elegido porque permite aplicar cabeceras en el borde sin cambiar el
repositorio ni depender de soporte inexistente de GitLab Pages para `_headers`.

La implementación se completó desde **Rules → Overview → Create rule → Response Header
Transform Rule**, utilizando `http.host` en vez del campo obsoleto `hostname` y `Set
static` en cada cabecera. Las expresiones, valores y evidencia final están registrados
en [la sección de implementación](#implementación-realizada-el-19-de-julio-de-2026).

La recomendación anterior de crear e instalar un **Cloudflare Origin Certificate** se
retiró: no formó parte de la implementación. La verificación del modo SSL/TLS y las
decisiones sobre Always Use HTTPS y HSTS se mantienen separadas en el
[runbook operativo](runbook_cloudflare_headers.md).

Para verificaciones posteriores, usar el runbook. En particular, una respuesta correcta
del documento principal contiene las cinco cabeceras y una sola
`Permissions-Policy`; el visor de PMTiles debe seguir respondiendo CORS y solicitudes
`Range` en `tiles.3cucharadas.cl`.

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
