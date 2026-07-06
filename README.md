# ¡Hola! Soy Cristián Labra Olivares (tatan)

Economista y servidor público desde 2012, con un fuerte interés en el uso de datos, estadística y programación para la formulación de políticas sociales. Mi objetivo es plasmar por acá mis intereses y colaborar.

### Sobre este espacio

Este lugar nace de la necesidad de **compartir, aprender y colaborar**. Aquí encontrarás contenido sobre:

-   Políticas sociales y diseño basado en evidencia.
-   Visualización de datos y programación aplicada.
-   Ética pública, software libre y cooperación.

### Herramientas

Trabajo principalmente con **Stata**, **R**, **Python**, **SQL**, **Julia** y sistemas **Linux**.

### Contacto

Si quieres comentar, criticar o colaborar, puedes encontrarme en:

-   **Email:** [tatanlabra@gmail.com](mailto:tatanlabra@gmail.com)
-   **X (Twitter):** [@tatanlabra](https://x.com/tatanlabra)
-   **Mastodon:** [@asiole@mastodon.social](https://mastodon.social/@asiole)
-   **Bluesky:** [@labra.bsky.social](https://bsky.app/profile/labra.bsky.social)

---

**Gracias por pasar por aquí** 🙌

## Publicacion

Sitio productivo: https://3cucharadas.cl

Este repositorio se publica productivamente mediante GitLab Pages. GitHub se
conserva como espejo publico y como redirector de la URL historica
`https://tatanlabra.github.io/3cucharadas/`, no como hosting productivo del
contenido principal.

## Operación RSS diaria (server-side)

- El widget RSS se genera durante el build de GitLab CI: `.gitlab-ci.yml`
  ejecuta `scripts/fetch_news.py` antes de `jekyll build`.
- GitHub Pages no publica una copia del sitio real; solo sirve redirectores
  estaticos desde la rama `gh-pages-redirect`.
- No hay commits automáticos diarios de `_data/feedly_news.json`; el JSON es artefacto de build.

### Configuración requerida en GitLab UI

1. Ir a `Build > Pipeline schedules` en el proyecto `tatanlabra/3cucharadas`.
2. Crear schedule diario con cron: `0 9 * * *` (UTC).
3. Seleccionar branch objetivo: `main`.
4. Guardar y ejecutar una corrida manual inicial para validar que el job `build_site` publique el widget actualizado.
