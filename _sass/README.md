# Sass del sitio

`minimal-mistakes.scss` y `minimal-mistakes/` vienen de la gema Minimal Mistakes 4.28.1
(MIT, © Michael Rose; aviso en `minimal-mistakes/_copyright.scss`), copiados al repo y
modificados en la capa 2C de la auditoría UX del 2026-10-17
(`archivo/handoffs/2026-10-17_AUDITORIA_ux-ui-3cucharadas.md`, §19):

- sistema de módulos de Sass (`@use`/`@forward`): ningún `@import`;
- funciones de los módulos `sass:*` en vez de las globales, y sin división con `/`;
- sin Susy: sus 21 llamadas `span()`/`gutter()` se reemplazaron por los valores que ya
  producían;
- sin la librería breakpoint: `_breakpoint.scss` emite las mismas media queries en `em`;
- sin Magnific Popup (el lightbox es `<dialog>` en `assets/js/site-core.js`); su único
  estilo global, el reset de `button::-moz-focus-inner`, vive en `_button-reset.scss`;
- solo el skin `contrast` (el de `_config.yml`): sus variables encabezan `_variables.scss`
  y sus reglas quedan en `skins/_contrast.scss`.

`assets/css/main.scss` lo configura con `@use "minimal-mistakes" as * with (...)`.
`scripts/verify_sass_strict.rb` lo compila sin silenciar avisos y reprueba ante cualquiera.
