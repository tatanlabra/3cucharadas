# Hero codera El Salvador para home

## Estado productivo

Fecha de cierre: 2026-06-27.

Este hero queda como plantilla productiva para portada de 3 Cucharadas: fondo negro, zona izquierda segura para texto y ciudad visible a la derecha con calles OSM blancas y nitidas. No usa raster satelital ni labels incrustados; la cartografia se compone desde geometria OSM local para controlar contraste, crop y peso visual.

## Archivos

Script reproducible:

```bash
python scripts/render_home_el_salvador_hero.py
```

Entrada:

```text
../catastros_sii/data/interim/osm_cache/el_salvador_overpass.json
```

Salidas:

```text
assets/images/home/el-salvador-codera-hero-2400x720.webp
assets/images/home/el-salvador-codera-hero-1600x524.webp
assets/images/home/el-salvador-codera-hero-mobile-1200x720.webp
```

Integracion (desde el 2026-10-17):

- `_pages/about.md` y `_pages/about-en.md` usan `header.overlay_image` con el asset `2400x720`, la clase `codera-hero` y sin leyenda: el mapa va solo con el título y la bajada de la página (la leyenda biográfica se retiró el 2026-10-18 a pedido de la persona usuaria).
- `assets/css/main.scss` define overrides responsivos para desktop, laptop y mobile bajo `.codera-hero`, siempre con `:not(.page__hero--latest)`.
- `index.html` ya no lo usa como hero (la portada abre con la última cucharada y la página 2 se titula con su número); lo conserva como imagen social con la variante `og-1200x630`.
- Contrato: `mapa-codera-acerca` en `docs/contracts/ux-transversal.yml`.

## Criterios visuales aceptados

- 40-45% izquierdo oscuro para texto del home.
- Ciudad desplazada a la derecha, con crop cercano sobre El Salvador.
- Calles principales en blanco muy claro y mayor grosor.
- Calles locales en blanco/gris fino, todavia legibles.
- Fondo negro codera con halo urbano sutil.
- Mobile no queda totalmente negro: usa asset propio `1200x720` y `background-position` ajustado.

## Como cambiar ciudad

1. Crear o apuntar un cache OSM local equivalente al usado por `OSM_CACHE`.
2. Ajustar `FOCUS_BBOX` al casco urbano que debe verse.
3. Cambiar nombres de salida en `SPECS` si el asset debe convivir con el actual.
4. Reejecutar:

```bash
python scripts/render_home_el_salvador_hero.py
identify assets/images/home/*hero*.webp
JEKYLL_ENV=production bundle exec jekyll build
```

5. Actualizar `index.html` y `assets/css/main.scss` para apuntar a los nuevos nombres.

## Validacion de cierre

La version productiva validada genero estos assets:

```text
1600x524 WEBP 28790B
2400x720 WEBP 47792B
1200x720 WEBP 32736B
```

Build validado:

```bash
JEKYLL_ENV=production bundle exec jekyll build
```

Resultado: build exitoso. Las advertencias observadas son de deprecacion Sass `@import` heredadas de Minimal Mistakes y no bloquean el hero.

Preview local usado para revision:

```text
http://127.0.0.1:4001/
```
