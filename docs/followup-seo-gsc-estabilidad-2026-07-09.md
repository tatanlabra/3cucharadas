# Follow-up SEO, estabilidad y Google Search Console

Fecha de control: 2026-07-09.

Arquitectura objetivo:

- Produccion: GitLab Pages.
- Dominio canonico: `https://3cucharadas.cl/`.
- Variante `www`: redirecciona o resuelve hacia `https://3cucharadas.cl/`.
- GitHub: espejo/respaldo del codigo y redirector desde la URL historica.
- URL historica: `https://tatanlabra.github.io/3cucharadas/`.
- GitHub Pages: no debe publicar el sitio duplicado; debe publicar solo el redirector.

## 1. Revision de pendiente

### Estado local

- Rama actual: `post-publicacion-dominio-propio`.
- Arbol local: limpio al cierre de la revision previa.
- Cambios locales ya comiteados:
  - `c4729a85 fix(seo): estabilizar canonical y 404`
  - `ed5d5678 ci(pages): estabilizar redirector github`
  - `67f82ff6 chore(drafts): retirar borrador bayes obsoleto`
  - `7de469af draft(posts): agregar borrador predial v44`
  - `668b3207 chore(assets): conservar imagen fuente rss governance`
- Redirector GitHub local actualizado en rama `gh-pages-redirect`:
  - `c4e4bcc4 chore(pages): actualizar redirector github`

### Estado publico verificado

Control HTTP/DNS repetido contra servicios publicos a las `2026-07-09 02:49 UTC`:

- `https://3cucharadas.cl/`: `HTTP/2 200`.
- `http://3cucharadas.cl/`: `301` hacia `https://3cucharadas.cl/`.
- `https://www.3cucharadas.cl/`: `308` hacia `https://3cucharadas.cl/`.
- `https://3cucharadas.cl/robots.txt`: `HTTP/2 200`.
- `https://3cucharadas.cl/sitemap.xml`: `HTTP/2 200`.
- `https://3cucharadas.cl/feed.xml`: `HTTP/2 200`.
- DNS:
  - `NS 3cucharadas.cl`: Cloudflare (`remy`, `marge`).
  - `A 3cucharadas.cl`: `35.185.44.232`.
  - `AAAA 3cucharadas.cl`: `2600:1901:0:7b8a::`.
  - `CNAME www.3cucharadas.cl`: `tatanlabra.gitlab.io.`

Pendiente critico detectado:

- `https://tatanlabra.github.io/3cucharadas/` sigue sirviendo el redirector antiguo:
  - `robots`: `noindex, follow, noarchive`.
  - texto antiguo sin tilde: `El sitio se traslado...`.
- Localmente ya existe el redirector corregido con `index, follow`; falta publicarlo en GitHub Pages.

## 2. Diagnostico deductivo

Si la arquitectura final es dominio propio canonico en GitLab Pages, entonces los invariantes tecnicos son:

- `_config.yml` debe mantener `url: "https://3cucharadas.cl"` y `baseurl: ""`.
- `robots.txt`, `sitemap.xml`, `feed.xml`, canonicals, Open Graph, Twitter cards y JSON-LD deben emitir URLs absolutas bajo `https://3cucharadas.cl/`.
- Todas las variantes de host y esquema deben converger al canonico:
  - `http://3cucharadas.cl/*` -> `https://3cucharadas.cl/*`.
  - `https://www.3cucharadas.cl/*` -> `https://3cucharadas.cl/*`.
- La URL historica de GitHub Pages debe transferir senales hacia el dominio nuevo y no convertirse en sitio duplicado.
- Search Console debe verificar el dominio nuevo y mantener observacion temporal de las propiedades antiguas para confirmar transferencia gradual.

Derivacion para Google:

- Google recomienda verificar tanto las propiedades antiguas como las nuevas durante una mudanza de URL y mantener redirecciones activas por un periodo largo.
- Las redirecciones permanentes son una senal fuerte para seleccionar la URL canonica; si el hosting no permite 301 por ruta, el redirector HTML debe reforzar la transferencia con `rel=canonical`, `index, follow`, sitemap canonico y enlaces visibles al destino.
- El sitemap nuevo debe listar solo URLs canonicas del dominio nuevo.

## 3. Diagnostico inductivo

Lo observado en vivo sugiere:

- GitLab Pages ya esta resolviendo bien el dominio canonico, HTTP->HTTPS y `www`->apex.
- Los archivos tecnicos basicos (`robots.txt`, `sitemap.xml`, `feed.xml`) estan disponibles publicamente.
- El mayor riesgo SEO actual no esta en GitLab, sino en GitHub Pages: la URL historica aun publica un redirector con `noindex`.
- Mientras GitHub Pages no reciba el redirector nuevo, Search Console puede ver una combinacion suboptima: la URL antigua existe, apunta al destino, pero pide no indexar el origen en vez de ayudar a consolidar la mudanza.
- La comprobacion local de build no sustituye la comprobacion publica: GitHub Pages puede seguir sirviendo contenido anterior aunque la rama local ya este corregida.

## 4. Plan de accion priorizado

### Fase 0 - Publicar lo ya preparado

Objetivo: alinear el estado publico con el estado local.

1. Publicar `gh-pages-redirect` en GitHub.
2. Confirmar que el workflow `github-pages-redirector.yml` corre y despliega un unico artifact.
3. Repetir `curl` sobre:
   - `https://tatanlabra.github.io/3cucharadas/`
   - `https://tatanlabra.github.io/3cucharadas/mlops/bayes-hiperparametros/`
4. Confirmar en el HTML publico:
   - `robots` contiene `index, follow`.
   - `canonical` apunta a `https://3cucharadas.cl/...`.
   - El texto visible usa `se traslado` corregido como `se trasladó` si corresponde al build publico.

Pendiente manual/remoto: requiere autorizacion explicita de push remoto.

### Fase 1 - Agregar y verificar el dominio en Search Console

Ruta manual: `https://search.google.com/search-console`.

Pasos recomendados:

1. Elegir `Agregar propiedad`.
2. Seleccionar `Dominio`.
3. Ingresar exactamente `3cucharadas.cl`.
4. Copiar el registro TXT que entrega Google.
5. En Cloudflare, abrir el dominio `3cucharadas.cl` y crear un registro:
   - Tipo: `TXT`.
   - Nombre: `@` o `3cucharadas.cl`, segun interfaz.
   - Contenido: token TXT entregado por Search Console.
   - Proxy: no aplica para TXT.
6. Esperar propagacion DNS y presionar `Verificar`.
7. Mantener el TXT despues de verificar.

Propiedades URL-prefix utiles, ademas de la propiedad de dominio:

- `https://3cucharadas.cl/`: para inspeccion puntual y reportes por prefijo canonico.
- `https://www.3cucharadas.cl/`: para comprobar que Google ve la redireccion a apex.
- `https://tatanlabra.github.io/3cucharadas/`: para monitorear la URL historica, si Search Console permite verificarla.

### Fase 2 - Sitemap e inspeccion inicial

En la propiedad `3cucharadas.cl`:

1. Ir a `Sitemaps`.
2. Enviar `https://3cucharadas.cl/sitemap.xml`.
3. Confirmar que Search Console lo marca como leido.
4. Usar `Inspeccion de URL` con:
   - `https://3cucharadas.cl/`
   - `https://3cucharadas.cl/feed.xml`
   - 3 a 5 posts historicos con trafico o valor editorial.
5. Solicitar indexacion solo para las URLs canonicas clave, no masivamente.

### Fase 3 - Cambio de direccion

Evaluacion:

- La herramienta `Cambio de direccion` de Search Console esta pensada para mudanzas de sitio entre propiedades verificadas.
- Puede ser limitada o no aplicable para un subpath de GitHub Pages (`/3cucharadas/`) hacia dominio propio.
- No forzarla si Search Console no valida la propiedad origen o no acepta ese patron.

Si la herramienta lo permite:

1. Abrir la propiedad antigua.
2. Usar `Configuracion` -> `Cambio de direccion`.
3. Seleccionar `https://3cucharadas.cl/`.
4. Verificar que los checks de redireccion pasen.

Si no lo permite:

- Mantener redirector GitHub limpio.
- Mantener sitemap canonico nuevo.
- Seguir reportes de indexacion y rendimiento por 3 a 6 meses.

### Fase 4 - Estabilidad tecnica recurrente

Cadencia semanal durante el primer mes:

```bash
JEKYLL_ENV=production bundle exec jekyll build
curl -sSIL https://3cucharadas.cl/
curl -sSIL http://3cucharadas.cl/
curl -sSIL https://www.3cucharadas.cl/
curl -sSIL https://3cucharadas.cl/sitemap.xml
curl -sSIL https://3cucharadas.cl/feed.xml
curl -sSL https://tatanlabra.github.io/3cucharadas/ | rg 'robots|canonical|3cucharadas.cl'
```

Checks de Search Console:

- `Paginas`: errores nuevos, excluidas por canonical inesperado, soft 404, redirect error.
- `Sitemaps`: URLs descubiertas y fecha de ultima lectura.
- `Rendimiento`: impresiones y clicks por pagina, consulta y pais.
- `Crawl stats`: subidas bruscas de errores o respuestas no 200.
- `HTTPS`: confirmar que no hay problemas de certificado.

### Fase 5 - Mejoras SEO de alto retorno

Prioridad alta:

- Revisar que cada post con trafico tenga `title`, `description`/excerpt y `image` adecuados.
- Normalizar imagenes sociales a formato estable cuando el post lo amerite, idealmente 1200x630 para Open Graph.
- Validar datos estructurados con Rich Results Test para home y 3 a 5 posts representativos.
- Revisar que las paginas `/en/...` tengan canonical y metadatos propios, no apuntando por accidente a la version en espanol si no corresponde.
- Auditar links internos antiguos que todavia apunten a `tatanlabra.github.io/3cucharadas`.

Prioridad media:

- Crear un tablero mensual manual con:
  - top consultas por impresiones.
  - top paginas por clicks.
  - CTR bajo con posicion media alta.
  - paginas nuevas sin impresiones despues de 14 dias.
- Mejorar snippets de posts con alta impresion y bajo CTR.
- Medir Core Web Vitals/PageSpeed para home y posts con imagenes pesadas.

Prioridad baja:

- Evaluar WebSub/ping de feed si el consumo RSS lo justifica.
- Crear sitemap o listado editorial especial solo si existe una necesidad real de descubrimiento; no duplicar URLs ya cubiertas por `jekyll-sitemap`.

## 5. Criterios de exito

El cambio se considera estabilizado cuando:

- GitHub Pages publico muestra el redirector corregido, no el antiguo.
- Search Console verifica `3cucharadas.cl` como propiedad de dominio.
- `https://3cucharadas.cl/sitemap.xml` aparece leido sin errores.
- Home y posts clave figuran como canonicos seleccionados por Google bajo `https://3cucharadas.cl/`.
- Las impresiones de URLs antiguas bajan gradualmente y las del dominio nuevo suben o se estabilizan.
- No aparecen errores recurrentes de 404, redirect loop, duplicate without user-selected canonical o alternate page with proper canonical para URLs que deberian indexarse.

## 6. Fuentes operativas

- Google Search Central: Site move with URL changes: `https://developers.google.com/search/docs/crawling-indexing/site-move-with-url-changes`
- Google Search Central: Redirects and Google Search: `https://developers.google.com/search/docs/crawling-indexing/301-redirects`
- Google Search Central: How to specify a canonical URL: `https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls`
- Google Search Central: Build and submit a sitemap: `https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap`
- Search Console Help: Verify your site ownership: `https://support.google.com/webmasters/answer/9008080`
- Search Console Help: Change of Address tool: `https://support.google.com/webmasters/answer/9370220`
