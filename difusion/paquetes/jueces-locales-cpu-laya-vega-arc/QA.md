# QA — Paquete de difusión `jueces-locales-cpu-laya-vega-arc`

- [x] Paridad bilingüe ES/EN verificada con `ruby scripts/verify_draft_promotion.rb --production`.
- [x] Pack `heroes-v2` dedicado (`hero-1600x900.webp`, `hero-mobile-800x450.webp`, `teaser-1280x720.webp`, `teaser-mobile-640x360.webp`, `og-1200x630.webp`) verificado con `ruby scripts/verify_visual_assets.rb --strict` y `ruby scripts/verify_hero_disclosure.rb`.
- [x] Elegibilidad de destinos registrada en `difusion/state/destinos/jueces-locales-cpu-laya-vega-arc.json` (`mastodon-es`, `bluesky-es`, `linkedin-es`, `dev`, `medium`).
- [x] Coherencia numérica entre `_posts/2026-10-31-jueces-locales-cpu-laya-vega-arc*.md` y todas las piezas del paquete verificada con `ruby scripts/verify_difusion_coherente.rb jueces-locales-cpu-laya-vega-arc`.
- [ ] Despliegue remoto (`git push origin main`) y comprobación de HTTP 200 en producción antes de ejecutar `scripts/post_push_difusion.sh jueces-locales-cpu-laya-vega-arc --live`.
