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
