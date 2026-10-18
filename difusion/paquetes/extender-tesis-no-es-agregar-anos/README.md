# Extender mi tesis (parte II) — paquete de difusión social

Estado: **publicado y verificado el 2026-10-18** con `closeout --live`, tras la aprobación humana de la copia en el chat (borrador revisión 3, aprobaciones `true` en ambas redes). Verificación por API: texto, idioma, orden del hilo, tarjetas y facets en verde, sin checks en `false`.

| Red | Raíz ES | Respuesta EN |
|---|---|---|
| Mastodon | https://mastodon.social/@asiole/117459743632695677 | https://mastodon.social/@asiole/117459743663387977 |
| Bluesky | https://bsky.app/profile/labra.bsky.social/post/3my4nfiis7r2y | https://bsky.app/profile/labra.bsky.social/post/3my4nfktld42u |

`social.json` contiene el texto base exacto que se publicó.

`social.json` contiene el texto base del borrador (`base_copy`): raíz ES y respuesta EN. Mastodon agrega la URL UTM del artículo al final; Bluesky usa la tarjeta OG del artículo. El borrador operativo y su ledger viven en el state dir XDG, fuera del repositorio. Se generó con `--provider manual`, se editó por la API de storage con revisión esperada (revisión 2) y la aprobación humana lo llevó a la revisión 3.

## Criterio editorial

- Contrato epistémico del Post II: no identifica efectos causales de los cierres ni ofrece una regla para decidir qué escuelas cerrar. La copia solo dice lo que el post dice en su apertura y cierre.
- Sin cifras: la CLI solo admite números presentes en título, descripción o URL del post, y las cifras del cuerpo (900, 330, 38, etc.) quedan fuera a propósito para que ninguna se lea sin su denominador.
- Sin casos individuales: El Salvador no se menciona; Lo Prado, Lo Barnechea y «parte III» están retirados del post.
- Sin enlace a la cápsula de audio: el episodio se titula «¿Cerrar escuelas en los próximos años? ¿cuáles cerrar?…» y la tarjeta de Spotify desplazaría a la del artículo en Mastodon, mostrando esa pregunta como encabezado. Si se quisiera añadir, solo la raíz ES y con la URL declarada en `audio.plataformas`.
- La respuesta EN no menciona audio.

## Respaldo de cada afirmación (Post II, `_posts/2026-10-11-extender-tesis-no-es-agregar-anos.md`)

| Afirmación de la copia | Sección del post |
|---|---|
| «cierres y aperturas de escuelas en Chile» | `description` del front matter: «examina cierres y aperturas escolares en Chile» |
| «Los registros precisan el recambio» | `excerpt`: «Los registros permiten precisar el recambio» |
| «no permiten saber si mejoró o empeoró los resultados educativos» | Apertura, `claim-causal-boundary`: «no identifica si el recambio mejora o empeora los resultados educativos» |
| «qué continuidad recibió la comunidad y quién absorbió los costos» | Apertura: «qué continuidad recibió la comunidad y quién absorbió sus costos»; Cierre, `claim-open-question`: «quién conserva continuidad y quién termina pagando la transición» |

## Controles

- Frases prohibidas y `affirmed_promotions` de `scripts/verify_thesis_extension_post_ii.rb` aplicadas a ES y EN: sin coincidencias.
- Validación de la CLI: Bluesky 276 (ES) y 281 (EN) caracteres sobre 300; Mastodon 467 y 475 sobre 500 contando la URL completa.
