# QA — Paquete de difusión `multiagente-penta-agent-autopoiesis-parte-iv`

- [x] Paridad bilingüe ES/EN verificada con `ruby scripts/verify_post_publication_readiness.rb --production`.
- [x] Pack `heroes-v2` dedicado (`hero-1600x900.webp`, `hero-mobile-800x450.webp`, `teaser-1280x720.webp`, `teaser-mobile-640x360.webp`, `og-1200x630.webp`) verificado con `ruby scripts/verify_visual_assets.rb --strict` y `ruby scripts/verify_hero_disclosure.rb _site`.
- [x] Elegibilidad de destinos registrada en `difusion/state/destinos/multiagente-penta-agent-autopoiesis-parte-iv.json` (`mastodon-es`, `bluesky-es`, `linkedin-es`, `dev`, `medium`).
- [x] Coherencia numérica entre `_posts/2026-10-31-multiagente-penta-agent-autopoiesis-parte-iv*.md` y todas las piezas del paquete verificada con `ruby scripts/verify_difusion_coherente.rb multiagente-penta-agent-autopoiesis-parte-iv`.
- [ ] Despliegue remoto (`git push origin main`) y comprobación de HTTP 200 en producción antes de ejecutar `scripts/post_push_difusion.sh multiagente-penta-agent-autopoiesis-parte-iv --live`.
