# Redireccion historica de namespaces

Estos archivos **no son parte del build de 3cucharadas**. El sitio productivo
vive en `https://3cucharadas.cl` y el redirector oficial de GitHub Pages se
genera con `tools/build_github_redirector.py` hacia la rama `gh-pages-redirect`.

## Estado actual

El sitio ya no debe publicarse bajo `/3cucharadas/` en produccion. Si todavia
existen repos de namespace (`tatanlabra.gitlab.io` o `tatanlabra.github.io`),
deben redirigir al dominio canonical:

```text
https://3cucharadas.cl/
```

## Nota SEO

Los redirectores estaticos deben incluir canonical al dominio nuevo,
`robots: noindex, follow`, meta refresh y `window.location.replace`.

## Alcance de las paginas estaticas (decision del 2026-10-04)

`gh-pages-redirect` se genero el 2026-07-08 con 25 paginas, una por cada HTML del sitio de ese
momento, y no se regenera por cada post. Es a proposito:

- Las paginas por ruta solo hacen falta para las URL **historicas**, las que existieron bajo
  `tatanlabra.github.io/3cucharadas/` antes de la mudanza a `3cucharadas.cl` (2026-07-09).
- Lo posterior nunca se publico bajo `github.io`, asi que no hay enlaces que conservar. Si
  alguien pide una de esas rutas, el `404.html` de la rama quita el prefijo `/3cucharadas` y
  redirige con `location.replace` a la misma ruta en `3cucharadas.cl`.
- Medido el 2026-10-04: 40 URL en el sitemap y 25 paginas en la rama; un post posterior responde
  404 y redirige por JavaScript, uno historico responde 200 con meta refresh.

Lo unico que se pierde es un rastreador sin JavaScript, que ve el 404 en un post nuevo. Se
reabre si aparece trafico o enlaces hacia `github.io/3cucharadas/<post posterior>`; entonces
basta con regenerar con `tools/build_github_redirector.py` sobre un `_site` actual.
