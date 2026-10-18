# Réplica de la tesis (parte I) — paquete de difusión en Mastodon y Bluesky

Estado: **publicado y verificado el 2026-10-18** con `closeout --live`, tras la aprobación humana de la copia en el chat (borrador revisión 5, aprobaciones `true` en ambas redes). Verificación por API: texto, idioma, orden del hilo, tarjetas y facets en verde, sin checks en `false`.

| Red | Raíz ES | Respuesta EN |
|---|---|---|
| Mastodon | https://mastodon.social/@asiole/117459741937996739 | https://mastodon.social/@asiole/117459741991262476 |
| Bluesky | https://bsky.app/profile/labra.bsky.social/post/3my4neqrfdj2j | https://bsky.app/profile/labra.bsky.social/post/3my4net5a6z2y |

`social.json` contiene el texto base exacto que se publicó.

## Criterio editorial

- Tipo: auditoría de una réplica propia; audiencia profesional chilena de datos y política pública.
- Idea central: la historia general resistió, varias cifras no. Se declara que la auditoría es propia, no una réplica independiente, y que nada de lo publicado es causal.
- Sin cifras fuera del título y la descripción del post (2014 y 34); no se citan IHH, tasas ni coeficientes, para no descontextualizar su escala o sus límites.
- La raíz ES incluye la cápsula de audio solo con la URL de Spotify declarada en `audio.plataformas`; Mastodon añade la URL UTM del artículo y Bluesky conserva la tarjeta del artículo. La respuesta EN menciona que la cápsula es en español y no enlaza audio.
- Límites verificados por la CLI: Mastodon ES 493 de 500 (incluye la URL UTM); Bluesky ES 280 de 300.

## Respaldo en el post (`_posts/2026-08-29-replica-tesis-establecimientos-educacionales.md`)

| Afirmación de la copia | Dónde está |
|---|---|
| tesis de 2014 sobre entrada y salida de colegios | Subtítulo y apertura: «mi tesis de 2014 sobre entrada y salida de colegios» |
| audité 34 afirmaciones | `description` del front matter y sección «Cucharada 3» (34 juicios editoriales) |
| la historia general resistió, varias cifras no | Subtítulo: «La historia general resistió, varias cifras no» |
| auditoría propia, no independiente | Introducción: «La tesis es mía y la auditoría también: no es una réplica independiente» |
| nada es causal | Introducción: «Nada de lo que sigue es causal» |
| cápsula de audio en Spotify | `audio.plataformas` del front matter (URL idéntica) |
