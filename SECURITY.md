# Política de seguridad

## Qué cubre este documento

El repositorio `3cucharadas`: el sitio publicado en <https://3cucharadas.cl> y el
visor del Catastro SII que vive dentro de él.

Infraestructura real, porque cambia dónde tiene sentido reportar:

| Pieza | Quién la opera |
|---|---|
| Producción (`3cucharadas.cl`) | **GitLab Pages**, publicado por el job `pages` de `.gitlab-ci.yml` |
| Borde (TLS, cabeceras de seguridad, caché) | **Cloudflare**, con Response Header Transform Rules — ver [`docs/security/`](docs/security/) |
| Teselas PMTiles (`tiles.3cucharadas.cl`) | Cloudflare R2 con CORS en allowlist |
| Espejo en GitHub | Copia pública + redirector de la URL histórica `tatanlabra.github.io/3cucharadas`. **No sirve el contenido principal.** |

Un hallazgo en el espejo de GitHub casi nunca afecta a producción. Uno en
`.gitlab-ci.yml` sí, siempre.

## Ramas mantenidas

| Rama | Estado |
|---|---|
| `main` | **Mantenida.** Es lo que se publica; no hay releases versionados ni ramas de soporte. |
| `gh-pages-redirect` | Mantenida solo como redirector estático en GitHub Pages. Sin contenido propio. |
| Cualquier otra | No mantenida. Los reportes se evalúan contra `main`. |

El sitio es de publicación continua: la corrección se hace en `main` y se
despliega en el siguiente pipeline. No hay backports.

## Cómo reportar

Por correo, a la dirección ya publicada en el `README.md` y en la página
[Acerca de](_pages/about.md): **tatanlabra@gmail.com**, con `[SECURITY]
3cucharadas` en el asunto.

Si el repositorio de GitHub tiene habilitado *Private vulnerability reporting*,
también sirve — llega al mismo destinatario y deja el hilo privado.

Ayuda mucho incluir:

- URL o ruta exacta del archivo afectado, y la rama o el commit.
- Qué se puede hacer con el fallo, no solo que existe.
- Pasos mínimos para reproducirlo.

## Qué no publicar en un issue

Los issues de GitLab y GitHub son públicos por defecto. **No abras uno** para:

- Una vulnerabilidad explotable antes de que esté corregida.
- Un exploit funcional, aunque sea "solo una prueba de concepto".
- Cualquier credencial, token o cookie de sesión — ni siquiera parcialmente
  redactada, porque el fragmento visible suele bastar para identificar la cuenta.
- Capturas de pantalla o volcados con datos personales de terceros.
- URLs firmadas o con parámetros de autenticación.

Si ya publicaste algo así por error: no lo borres en silencio. Avísalo por
correo, porque un secreto expuesto necesita rotación, y borrar el issue no
deshace lo que ya fue indexado o clonado.

## Qué esperar

Esto es un proyecto personal mantenido en tiempo libre. **No hay SLA y no se
promete uno.** Lo que sí se compromete:

- Un acuse de recibo cuando el reporte se lea, no cuando se resuelva.
- Una respuesta con veredicto —confirmado, no reproducible, aceptado como
  riesgo— antes de cerrar el hilo.
- Crédito público si lo quieres, y silencio si prefieres.

No hay recompensas económicas.

Divulgación coordinada: si el hallazgo es explotable, se agradece un plazo
razonable antes de publicarlo. Noventa días es un punto de partida sensato, y es
negociable en ambos sentidos según la gravedad real.

## Fuera de alcance

- Servicios de terceros embebidos (Disqus, Google Analytics 4, GoatCounter,
  Font Awesome vía cdnjs). Repórtalos a quien los opera; aquí solo se puede
  decidir si se siguen usando.
- Resultados de escáneres automáticos sin impacto demostrado, incluida la
  ausencia de una cabecera que no cambia nada explotable en un sitio estático.
- Que la CSP esté en `Content-Security-Policy-Report-Only`. Es una decisión
  deliberada y documentada en `_headers` y en
  [`docs/runbook_cloudflare_headers.md`](docs/runbook_cloudflare_headers.md):
  publicarla como bloqueante sin haber observado violaciones reales rompe el
  visor. Un reporte que demuestre una violación concreta sí es bienvenido.
- Ausencia de DNSSEC o de HSTS. Están evaluados y pendientes por decisión, no
  por descuido.
- Ingeniería social, phishing contra el autor, o ataques de denegación de
  servicio por volumen.

## Material relacionado

- [`docs/security/`](docs/security/) — índice, modelo de amenazas y
  procedimientos de reversión.
- [`_headers`](_headers) — la política de cabeceras como fuente única, con la
  advertencia de por qué GitLab Pages la ignora.
