# Redirección del root → /3cucharadas/

Estos archivos **no son parte del build de 3cucharadas**. Sirven para que la raíz de los
dominios de GitHub/GitLab Pages de usuario redirija al proyecto.

## Por qué

El sitio vive en un subdirectorio:
- `https://tatanlabra.gitlab.io/3cucharadas/`
- `https://tatanlabra.github.io/3cucharadas/`

La raíz (`https://tatanlabra.gitlab.io/` y `https://tatanlabra.github.io/`) la sirven repos
**separados** llamados como el namespace. Hay que poner una redirección en cada uno.

## GitLab (`tatanlabra.gitlab.io`)

1. Crear/usar el repo `tatanlabra.gitlab.io`.
2. Publicar en su Pages tanto `index.html` (meta-refresh, fallback universal) como
   `_redirects` (301 server-side, preferido por SEO).
3. Con `_redirects`, GitLab responde un 301 real de `/` a `/3cucharadas/`.

## GitHub (`tatanlabra.github.io`)

1. Crear/usar el repo `tatanlabra.github.io`.
2. Commitear `index.html` en la raíz (GitHub Pages no soporta `_redirects`; el meta-refresh
   + `window.location.replace` es la vía portátil).
3. Activar Pages sobre `main`.

## Nota SEO

`index.html` lleva `rel=canonical` a `/3cucharadas/` y `robots: noindex, follow` para que la
raíz no compita en el índice y transfiera la navegación al sitio real.
