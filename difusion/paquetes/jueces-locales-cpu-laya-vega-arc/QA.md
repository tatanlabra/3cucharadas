# QA — Paquete de difusión `jueces-locales-cpu-laya-vega-arc`

- [x] Paridad bilingüe ES/EN verificada con `ruby scripts/verify_draft_promotion.rb --production`.
- [x] Pack `heroes-v2` dedicado (`hero-1600x900.webp`, `hero-mobile-800x450.webp`, `teaser-1280x720.webp`, `teaser-mobile-640x360.webp`, `og-1200x630.webp`) verificado con `ruby scripts/verify_visual_assets.rb --strict` y `ruby scripts/verify_hero_disclosure.rb`.
- [x] Elegibilidad de destinos registrada en `difusion/state/destinos/jueces-locales-cpu-laya-vega-arc.json` (`mastodon-es`, `bluesky-es`, `linkedin-es`, `dev`, `medium`).
- [x] Coherencia numérica entre `_posts/2026-10-31-jueces-locales-cpu-laya-vega-arc*.md` y todas las piezas del paquete verificada con `ruby scripts/verify_difusion_coherente.rb jueces-locales-cpu-laya-vega-arc`.
- [x] Despliegue remoto (`git push origin main`) y comprobación de HTTP 200 en producción (`https://3cucharadas.cl/ia-herramientas/datos-codigo/jueces-locales-cpu-laya-vega-arc/` y `/en/...`).
- [x] Hilos ES/EN publicados y verificados con `scripts/post_push_difusion.sh jueces-locales-cpu-laya-vega-arc --live` (`published_verified`):
  - Mastodon ES: `https://mastodon.social/@asiole/117537301369480670`
  - Mastodon EN: `https://mastodon.social/@asiole/117537301419485275`
  - Bluesky ES: `https://bsky.app/profile/labra.bsky.social/post/3mz73kmfrps2i`
  - Bluesky EN: `https://bsky.app/profile/labra.bsky.social/post/3mz73knyw5y2o`
- [x] Reconciliación en `_data/distribucion.yml` y `ruby scripts/verify_distribution_done.rb --strict --social-only --ref jueces-locales-cpu-laya-vega-arc` en verde.
