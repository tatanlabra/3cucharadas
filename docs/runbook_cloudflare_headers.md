# Runbook: cabeceras de seguridad en `3cucharadas.cl` vía Cloudflare

Ejecución manual en el panel. Rutas de UI verificadas en julio de 2026.

**Estado de partida medido:**
```
curl -sS -I -4 https://3cucharadas.cl/
→ HTTP/2 200 · única cabecera de política: permissions-policy: interest-cohort=()
→ gitlab-lb: haproxy-pages-04-lb-gprd   (confirma GitLab Pages, sin proxy)
```

---

## Las dos trampas que hay que entender antes de empezar

### 1. `tiles.3cucharadas.cl` NO sirve CORS con comodín

Medido contra un objeto real:

```
curl -sS -I -H "Origin: https://3cucharadas.cl" -H "Range: bytes=0-99" \
  https://tiles.3cucharadas.cl/catastro-sii/basemap_chile_20260718T212932Z.pmtiles

HTTP/2 206
access-control-allow-origin: https://3cucharadas.cl        ← allowlist, NO "*"
access-control-expose-headers: Accept-Ranges,Content-Length,Content-Range,ETag
```

Con `Origin: https://example.com` no devuelve **ninguna** cabecera `access-control-*`.

Las Transform Rules de zona **alcanzan también a los dominios personalizados de R2**. Un
`Set` de `Access-Control-Allow-Origin: *` sobre `tiles` lo volvería incondicional, y pisar
`access-control-expose-headers` **rompe PMTiles**: el visor necesita leer `Content-Range` y
`Accept-Ranges` para las Range requests.

**Por eso las tres reglas llevan filtro `http.host` explícito. No lo quites.**

### 2. El AAAA es el punto crítico

`tatanlabra.gitlab.io` resuelve a las mismas A **y** AAAA que el apex: el registro IPv6 es
GitLab Pages real y sirve el sitio.

Si proxeas solo el A, el tráfico IPv6 va directo a GitLab y **se salta todas las reglas**.
Como los clientes dual-stack prefieren IPv6 (Happy Eyeballs, RFC 8305), la mayoría de
visitantes no recibiría ninguna cabecera — mientras tu propio `curl -4` muestra todo verde.
Es un falso positivo peligroso.

---

## Paso 1 — Baseline

```bash
curl -sS -I -4 https://3cucharadas.cl/ | tee /tmp/baseline-apex.txt
dig +short 3cucharadas.cl A AAAA | tee /tmp/baseline-dns.txt
bash scripts/catastro_sii/verify_r2_cors.sh
```

El repo ya trae `verify_r2_cors.sh`, que hace preflight `OPTIONS` con control negativo.
**Es el test de regresión de `tiles`** — úsalo tras cada paso. Debe terminar sin `DRIFT`.

## Paso 2 — Modo SSL y Universal SSL

**`SSL/TLS → Overview → Configure` → `Full (strict)`.**

**Por qué `Flexible` rompería el sitio**, con evidencia: el origen 301-redirige HTTP a HTTPS.

```
curl -sS -I http://3cucharadas.cl/  →  HTTP/1.1 301 · location: https://3cucharadas.cl/
```

Con `Flexible`, Cloudflare habla HTTP al origen → GitLab responde 301 → el navegador pide
HTTPS → Cloudflare vuelve a hablar HTTP → 301 otra vez. **Bucle infinito,
`ERR_TOO_MANY_REDIRECTS`.**

`Full` sin strict tampoco: no valida el certificado del origen.

### Bloqueo antes de continuar

**`SSL/TLS → Edge Certificates`**: confirma que existe un **Universal SSL en estado Active**
cuyos hosts incluyan `3cucharadas.cl` y `www.3cucharadas.cl`.

El certificado de `tiles` cubre solo `tiles` (`CN=89c2f30d.sni.cloudflaressl.com`), no sirve
para el apex. **Si Universal SSL no está Active, detente**: proxear sin certificado de edge
da error TLS a todos los visitantes. La emisión tarda de minutos a ~24 h.

## Paso 3 — Activar el proxy (A **y** AAAA)

**`DNS → Records`**:

| Registro | Acción |
|---|---|
| `3cucharadas.cl` **A** → `35.185.44.232` | nube a **naranja (Proxied)** |
| `3cucharadas.cl` **AAAA** → `2600:1901:0:7b8a::` | nube a **naranja** — *no omitir* |
| `www.3cucharadas.cl` CNAME | nube a **naranja** (hoy responde 308 al apex, y ese redirect también viaja sin cabeceras si queda gris) |

Alternativa válida si no quieres IPv6: **borrar** el AAAA. Proxearlo es mejor.

### Verificación

```bash
dig +short 3cucharadas.cl A      # → 104.x / 172.67.x (Cloudflare), no 35.185.44.232
dig +short 3cucharadas.cl AAAA   # → 2606:4700::/32 (Cloudflare), NO 2600:1901:...
curl -sS -I -4 https://3cucharadas.cl/ | grep -iE 'http/|server|cf-ray'
```

Deben aparecer `server: cloudflare` y `cf-ray:`.

> **`curl -6` no sirve como verificación en esta máquina**: no tiene tránsito IPv6 (solo una
> ULA `fdce:…` sin ruta por defecto; `curl -6 https://ipv6.google.com` también falla). Un
> fallo ahí es un falso negativo. El discriminador real es el `dig +short AAAA` de arriba,
> que corre sobre IPv4. Para prueba end-to-end usa `https://internet.nl`.

Regresión de tiles: `bash scripts/catastro_sii/verify_r2_cors.sh` → sin `DRIFT`.

## Paso 4 — Transform Rules

**`Rules → Overview → Create rule → Response Header Transform Rule`**

*(La ruta cambió: ya no es `Rules → Transform Rules`.)*

Plan Free: 10 reglas activas. Usamos 3. El campo de host es **`http.host`**, no `hostname`.

### Set vs Add

GitLab.com inyecta `permissions-policy: interest-cohort=()` a nivel de instancia. Con **Add**
la respuesta llevaría **dos** `Permissions-Policy` y los navegadores no las fusionan de forma
predecible. **Usa `Set` en las cinco.**

### Regla 1 — `seguridad-global`

Expresión (pestaña *Edit expression*):
```
(http.host eq "3cucharadas.cl" or http.host eq "www.3cucharadas.cl")
```

| Header | Value |
|---|---|
| `X-Content-Type-Options` | `nosniff` |
| `X-Frame-Options` | `DENY` |
| `Referrer-Policy` | `strict-origin-when-cross-origin` |
| `Permissions-Policy` | `geolocation=(), microphone=(), camera=(), interest-cohort=()` |

Y `Content-Security-Policy-Report-Only` (una sola línea, 710 caracteres):

```
default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; script-src 'self' 'unsafe-inline' https://www.googletagmanager.com https://*.disqus.com https://*.disquscdn.com; style-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://*.disquscdn.com; font-src 'self' data: https://cdnjs.cloudflare.com; img-src 'self' data: blob: https://*.disquscdn.com https://referrer.disqus.com https://*.google-analytics.com https://*.googletagmanager.com; connect-src 'self' https://tiles.3cucharadas.cl https://*.google-analytics.com https://*.analytics.google.com https://*.googletagmanager.com https://*.disqus.com; worker-src 'self' blob:; frame-src https://disqus.com; form-action 'self'
```

### Regla 2 — `cache-assets-dist`
```
(http.host eq "3cucharadas.cl" and starts_with(http.request.uri.path, "/assets/dist/"))
```
→ `Cache-Control` = `public, max-age=31536000, immutable`

### Regla 3 — `cors-assets-data`
```
(http.host eq "3cucharadas.cl" and starts_with(http.request.uri.path, "/assets/data/"))
```
→ `Access-Control-Allow-Origin` = `*`

Aquí `*` es correcto: son agregados comunales públicos servidos desde Pages. **El filtro
`http.host` es lo que impide que esta regla toque `tiles`.**

### Verificación

```bash
curl -sS -I -4 https://3cucharadas.cl/ | grep -iE 'x-content-type|x-frame|referrer-policy|permissions-policy|content-security'
curl -sS -I -4 https://3cucharadas.cl/ | grep -ci '^permissions-policy:'   # DEBE ser 1
```
Si sale `2`, usaste **Add** en vez de **Set**.

```bash
# tiles INTACTO — la verificación que más importa
curl -sS -I -H "Origin: https://3cucharadas.cl" -H "Range: bytes=0-99" \
  https://tiles.3cucharadas.cl/catastro-sii/basemap_chile_20260718T212932Z.pmtiles \
  | grep -iE 'http/|access-control|content-range'
```
Debe seguir dando `206`, `access-control-allow-origin: https://3cucharadas.cl` y
`access-control-expose-headers`. Si cambió a `*`, o desapareció `expose-headers`, o aparece
`x-frame-options` → una regla se filtró al host equivocado.

Cierra abriendo el visor en el navegador: las teselas deben cargar sin errores CORS.

## Paso 5 — Always Use HTTPS (opcional, al final)

`SSL/TLS → Edge Certificates → Always Use HTTPS` → On.

HSTS solo tras varias semanas estables: con `max-age` largo es difícil de revertir.

---

## El certificado: recomendación

**No instales el Cloudflare Origin Certificate por ahora.**

Tu origen ya presenta un certificado **público y válido**, y `Full (strict)` lo acepta sin
problema:

```
issuer=Google Trust Services, CN=WE1
subject=CN=3cucharadas.cl
notAfter=Oct 3 2026
```

El Origin Certificate existe para orígenes **sin** certificado válido. Instalarlo aquí
significa perder la renovación automática de GitLab y quedarte con uno que **solo Cloudflare
reconoce** — y, sobre todo, **es la única puerta de un solo sentido de todo el
procedimiento**: con él instalado no puedes volver las nubes a gris sin dejar el sitio con
error TLS para todos.

Todos los demás pasos son reversibles en segundos.

**El riesgo que sí existe** es que el proxy interfiera con la renovación ACME. Margen real:
los certificados vencen el **3 de octubre de 2026** y GitLab renueva ~30 días antes, o sea
alrededor del **3 de septiembre**. Hay ~6 semanas.

**Plan:** activa el proxy sin tocar el certificado, y **antes del 3 de septiembre** verifica:

```bash
echo | openssl s_client -connect 3cucharadas.cl:443 -servername 3cucharadas.cl 2>/dev/null \
  | openssl x509 -noout -dates
```

Si el `notAfter` no se movió, entonces sí: crea el Origin Certificate y sigue el
procedimiento de instalación (con la raíz Origin CA incluida, separada por línea en blanco;
sin ella GitLab devuelve `526`). Ruta: `Deploy → Pages` → lápiz junto al dominio → desactivar
Let's Encrypt automático.

Mitigación alternativa: una Configuration Rule que exima
`starts_with(http.request.uri.path, "/.well-known/acme-challenge/")` de caché y de Always Use
HTTPS.

---

## Rollback

**Nivel 1 — cabeceras mal.** `Rules → Overview` → toggle **Off** en la regla culpable.
Segundos. Cubre casi todo.

**Nivel 2 — el visor se rompió.** Desactiva las 3 reglas y corre `verify_r2_cors.sh`. Si
sigue roto no eran las reglas: `Caching → Configuration → Purge Everything` (los assets
cacheados conservan cabeceras viejas).

**Nivel 3 — el sitio no responde tras proxear.** Diagnostica antes de revertir:

| Síntoma | Causa | Arreglo |
|---|---|---|
| `521` | Cloudflare no alcanza el origen | Revisa que A/AAAA apunten a GitLab |
| `525` / `526` | Fallo TLS al origen | Modo SSL, o falta la raíz Origin CA |
| `ERR_TOO_MANY_REDIRECTS` | **SSL en Flexible** | Cambia a Full (strict), no revertir DNS |
| Error de certificado | Universal SSL no activo | Espera la emisión |

**Nivel 4 — revertir el proxy.** Si no instalaste el Origin Certificate: nubes a gris y
listo. Si lo instalaste, primero reactiva Let's Encrypt en GitLab, **espera** a que emita
(verifica con `openssl s_client` que el issuer sea Let's Encrypt) y recién entonces pon las
nubes en gris.

---

## Qué NO tocar

| Registro | Motivo |
|---|---|
| `_gitlab-pages-verification-code` TXT (**los dos**) | GitLab revalida la propiedad periódicamente. Borrar cualquiera **desactiva el dominio**. Son dos porque cubren apex y `www`. |
| TXT `google-site-verification=...` | Se pierde el acceso a Search Console y el histórico SEO. |
| `tiles.3cucharadas.cl` (tipo **R2**) | Binding nativo, ya proxeado, con su propio certificado y su propia política CORS en `R2 → 3cucharadas-tiles → Settings → CORS Policy`, versionada en `scripts/catastro_sii/r2-cors.json`. |
| `_headers` del repo | Es la fuente documental única de la política. Si cambias una cabecera en Cloudflare, **actualízalo también** o divergirán. |

---

## Orden y reversibilidad

```
1. Baseline                          → curl + verify_r2_cors.sh
2. Full (strict) + Universal SSL     [reversible: total]
3. Proxy A + AAAA + www              [reversible: total]  ← verifica AQUÍ a fondo
4. Transform Rules ×3                [reversible: total]
5. Always Use HTTPS (opcional)       [reversible: total]
— Origin Certificate: NO por ahora   [única puerta de un solo sentido]
```

## Verificación final

```bash
echo "== cabeceras =="
curl -sS -I -4 https://3cucharadas.cl/ | grep -iE 'x-content-type|x-frame|referrer-policy|permissions-policy|content-security|cf-ray'
echo "== permissions-policy (debe ser 1) =="
curl -sS -I -4 https://3cucharadas.cl/ | grep -ci '^permissions-policy:'
echo "== AAAA proxeado (debe ser 2606:4700:...) =="
dig +short 3cucharadas.cl AAAA
echo "== tiles intacto =="
curl -sS -I -H "Origin: https://3cucharadas.cl" -H "Range: bytes=0-99" \
  https://tiles.3cucharadas.cl/catastro-sii/basemap_chile_20260718T212932Z.pmtiles \
  | grep -iE 'http/|access-control|content-range'
```
