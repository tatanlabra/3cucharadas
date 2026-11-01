# Git hooks versionados

`.git/hooks/` no se versiona, así que los hooks vivos de este repo se guardan acá
y se instalan con un symlink o una copia.

| Hook | Qué hace | ¿Puede fallar el commit/push? |
|---|---|---|
| `pre-commit` | Ejecuta `scripts/verify_draft_promotion.rb` (`verify_post_publication_readiness.rb`) y `scripts/verify_visual_assets.rb --strict` cuando el commit toca `_posts/*.md`, `_drafts/*.md` o `_data/visuales/*.yml`, validando atribución (`author: clabra` + `author_profile: true`), paridad bilingüe ES/EN (`ref`), justificado (`{: .text-justify}`), referencias, videos/imágenes y manifiesto visual (`V1`–`V13`) | **Sí**, el commit |
| `post-commit` | Termina en silencio: un commit no confirma publicación | No |
| `post-commit-difusion` | Resuelve a qué destinos de difusión corresponde cada post tocado y deja la traza en `difusion/state/destinos/<ref>.json` | No |
| `pre-push` | Escanea con `gitleaks` los commits que salen y ejecuta `scripts/verify_draft_promotion.rb` sobre cualquier post tocado en `_posts/*.md` o `_drafts/*.md`, deteniendo el push antes de GitLab y de GitHub si falta atribución (`author: clabra`), metadatos, justificado, referencias o si hay violaciones editoriales (`mathjax: true`, `« »`, 1.ª persona plural) | **Sí**, el push |

## Instalar

`post-commit-difusion` no se instala como hook independiente: git sólo ejecuta un
archivo por evento. Instala la cadena versionada con:

```bash
scripts/install_git_hooks.sh
```

Ambos terminan en `exit 0` a propósito: un aviso o una traza que falla no debe
tumbar un commit que ya está hecho.

`pre-push` es lo contrario y falla a propósito: `origin` empuja primero a GitLab
(producción, público) y después a GitHub, y el push no es atómico, así que el bloqueo
de pushes de GitHub llega cuando GitLab ya publicó el commit. El hook es el único punto
común a los dos. Requiere `gitleaks` (`sudo pacman -S --needed gitleaks`); si falta,
detiene el push. Saltarlo con `git push --no-verify` es una decisión humana.
`.git/hooks` es común a todos los worktrees del repo, así que aplica a todos.

## Aviso de publicación verificada

Telegram se invoca explícitamente, nunca desde el hook. El emisor
`../notify_telegram_publication.py` instala el lockfile sin scripts de instalación
y recompila los bundles Vite antes del build Jekyll del commit aislado; exige el
mismo SHA en GitLab y GitHub, CI exitoso de GitLab y contenido esperado en la URL pública. Si
un gate no pasa, sale con error y no envía ningún mensaje.

## Difusión: por qué resuelve y no publica

`post-commit-difusion` calcula qué destinos corresponden al artículo y lo escribe.
**No publica.** Publicar sigue siendo:

```bash
scripts/post_push_difusion.sh <ref>     # dry-run por defecto; --live exige autorización
```

que pasa por revisión humana. Un hook que publicara al commitear pondría el
contenido en público antes de que nadie lo hubiera leído, y el rollback siempre
es posterior al daño.

## Cómo se decide un destino

El catálogo está en `difusion/config/destinos.yml`. Cada destino declara el
**idioma** que consume y el **público** al que habla, más condiciones
verificables. La resolución cruza eso con lo que el post declara de verdad.

Tres estados:

- `listo` — elegible; no acredita borrador, aprobación ni publicación. El checklist mantiene `[ ]`.
- `bloqueado` — falta algo concreto, y el motivo lo dice (`falta republish: dev`,
  `1/2 posts en con tag geo`).
- `pendiente-verificar` — el destino existe pero **no se han confirmado sus
  reglas de envío**. Nunca pasa a `listo` solo. Es a propósito: declarar listo un
  agregador sin confirmar su política de autopromoción es cómo se termina
  spameando una comunidad.

### La trampa de los sinónimos

Varios destinos se desbloquean por umbral de etiqueta (`{python: 2}` significa
dos posts en inglés etiquetados `python`). Las etiquetas se comparan literalmente:
**`geospatial` no cuenta para un destino que espera `geo`**. Este hook existe en
buena parte para que ese error se vea al commitear y no meses después, al
preguntarse por qué un artículo nunca llegó a OSGeo.

## Añadir un destino

Editar `difusion/config/destinos.yml`. No hay que tocar código: `destinations.py`
lee el YAML. Si el destino necesita una condición que hoy no existe (`lang_post`,
`republish`, `tags_min`, `tags_any`, `verificado`), eso sí requiere extender `_evaluar()`.

### Elegir la comunidad correcta (`tags_any`)

`tags_min` mide historial: sirve para agregadores que piden varios posts del tema.
Una comunidad como un subreddit no pide historial, sino que el artículo sea de su
tema. Para eso está `tags_any`: el post evaluado tiene que llevar al menos una de
las etiquetas, en el idioma del destino. Así el hook nombra `reddit-publicpolicy-en`
y `reddit-latinoamerica-es` para el Post III de la tesis, que lleva `public-policy`
y `politica-publica`, y ninguno de los dos para un post técnico. Desde el
2026-11-01 el hook muestra todo destino `listo` o `pendiente-verificar`, no solo
Mastodon y Bluesky. Por eso `econacademics` y `comunidades-datos-gis-es` también
filtran por tema: sin ese filtro, aparecían pendientes en todos los posts.

## Canales sin API: lo aprendido con el Post III (2026-11-01)

El hook nombra el destino; la publicación en estos canales la hace una persona.
Lo que sigue se verificó al difundir el Post III de la tesis.

| Canal | Qué funciona | Qué no |
|---|---|---|
| Reddit (`modo: prefill`) | `scripts/reddit_prefill_urls.py <ref> --open` abre el formulario de old.reddit con título y texto prellenados (`/r/<sub>/submit?selftext=true&title=…&text=…`), en el navegador habitual y con la sesión de la persona, que revisa la barra lateral y envía | La API y los navegadores automatizados reciben «blocked by network security». Ir más lento no lo evita: Reddit detecta el navegador automatizado, no el ritmo. Esquivarlo arriesga la cuenta. El script solo prellena posts de texto: r/dataisbeautiful (envío de enlace con primer comentario de fuentes) va a mano |
| LinkedIn | Publicación de tipo documento con el PDF del carrusel y un copy corto con gancho; los enlaces van en el cuerpo. La lámina final puede llevar dos enlaces (post y podcast), que `render-linkedin-carousel.sh` repone en el PDF como anotaciones `/Link` | El visor de LinkedIn puede no hacer clicables los enlaces del PDF; las fuentes no coinciden. Por eso cada mitad de la lámina muestra también su dirección |
| Podcast (Spotify) | La URL `open.spotify.com/episode/<ID>` sale del botón Compartir o de la página pública del programa renderizada con `agent-browser` | El RSS de Spotify for Creators no la trae (su enlace es de creators.spotify.com) y tarda en listar un episodio que Spotify ya muestra. Detalle en `docs/flujo-podcast.md` |

El gate `verify_difusion_coherente.rb` también lee el HTML del carrusel y las notas
de cada paquete. Cualquier cifra que no esté en el post lo reprueba: un «79 mil»
redondeado, una fecha dentro de una nota o una entidad numérica como `&#8599;`.
Hay que copiar las cifras exactas del post y escribir los símbolos como caracteres
literales.

## Push a dos remotos y el bot de DEV.to

`origin` empuja primero a GitLab y después a GitHub, y el push no es atómico. El bot
de GitHub Actions que registra la sindicación de DEV.to commitea en `main` de GitHub
y reescribe `_data/distribucion.yml` con su propio ancho de línea: vuelve a cortar
las `nota:` largas en torno a 80 columnas, sin partir palabras ni rutas (medido el
2026-11-01: una línea quedó de 85 caracteres y otra, con una ruta, de 127). Si eso
ocurre entre dos pushes, GitLab acepta el siguiente y GitHub lo rechaza. Se resuelve
como en `81444990` y `d4c38ba3`: `git fetch` de GitHub, un merge `--no-ff` firmado
por tatan (`merge: integra el reformateo YAML del bot…`) y un push que avanza en los
dos remotos. Nunca con `--force`. Escribir notas cortas reduce el riesgo, pero no lo
elimina: el bot vuelve a fluir el texto a su manera. Lo que sí evita la sorpresa es
hacer `git ls-remote` a los dos remotos después de cada push.
