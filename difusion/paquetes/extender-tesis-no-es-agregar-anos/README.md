# Extender mi tesis (parte II) — paquete de difusión (`extender-tesis-no-es-agregar-anos`)

Estado de redes cortas: **publicado y verificado el 2026-10-18** con `closeout --live`, tras la aprobación humana de la copia en el chat (borrador revisión 3, aprobaciones `true` en ambas redes). Verificación por API: texto, idioma, orden del hilo, tarjetas y facets en verde, sin checks en `false`.

| Red | Raíz ES | Respuesta EN |
|---|---|---|
| Mastodon | https://mastodon.social/@asiole/117459743632695677 | https://mastodon.social/@asiole/117459743663387977 |
| Bluesky | https://bsky.app/profile/labra.bsky.social/post/3my4nfiis7r2y | https://bsky.app/profile/labra.bsky.social/post/3my4nfktld42u |

`social.json` contiene el texto base exacto que se publicó.

## Archivos del paquete completo (12 artefactos + `social.json` + `podcast/`)

- `00-metadata.yaml`: metadatos canónicos, evidencia dura y estado por canal.
- `01-en-source.md`: fuente transcreada maestra al inglés.
- `social.json` y `social-corto.md`: copias para Mastodon y Bluesky (ES/EN, publicadas el 2026-10-18).
- `linkedin.md` y `x.md`: copias nativas para LinkedIn y X.
- `medium.md` y `devto.md`: adaptaciones diferenciadas con enlace canónico.
- `hn.txt`: título y comentario técnico inicial para Hacker News.
- `reddit-dataisbeautiful.md` y `reddit-hilos.md`: borradores para `r/dataisbeautiful`, `r/PublicPolicy` y `r/econometrics`.
- `QA.md`: lista de control verificada.
- `podcast/`: guion y metadatos de la cápsula de audio en Spotify (episodio `7ho9naqSgAotsTfcsBmOwc`, compartido con la parte I; es el único ID verificado en `podcast/origen.yaml`).

## Edición adversarial del 2026-11-07

- Mejoras econométricas destacadas en todas las piezas largas: M4 (encogimiento de Bayes empírico de Morris 1983 con soporte regional), M5 (permutación exacta de Fisher y *wild cluster bootstrap* de Webb en SAE; *Synthetic DiD* en SLEP) y M6 (logit condicional de McFadden sobre destinos de reubicación).
- Correcciones: ID de Spotify inventado en `linkedin.md` (sustituido por el verificado), rutas de imagen inexistentes en `reddit-dataisbeautiful.md`, voz autoral en singular en `devto.md` y `medium.md`, hilo de `x.md` dentro del límite.
- Pendiente humano: reejecutar los dos gates listados en `QA.md` antes de cualquier envío.

## Criterio editorial

- Contrato epistémico del Post II: no identifica efectos causales de los cierres sobre los estudiantes ni ofrece una regla automática para decidir qué escuelas cerrar.
- Paridad numérica estricta verificada con `scripts/verify_difusion_coherente.rb extender-tesis-no-es-agregar-anos`.
- Frases prohibidas y `affirmed_promotions` de `scripts/verify_thesis_extension_post_ii.rb` aplicadas a ES y EN: sin coincidencias.
