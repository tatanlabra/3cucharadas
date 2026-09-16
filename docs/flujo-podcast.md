# Flujo: de un post publicado a una cápsula de audio

Fecha de revisión: 2026-09-13.

Una **cápsula** es una conversación de dos voces sintéticas sobre un post ya publicado, generada
con NotebookLM, publicada como episodio de podcast y enlazada desde el artículo. No sustituye al
post ni añade evidencia: es otra puerta de entrada al mismo contenido. Donde discrepen, manda el
post.

**Desde el 2026-09-15 el sitio no aloja el audio.** Las escuchas ocurren en Spotify y Apple, donde
cuentan para el programa, y el artefacto de Pages deja de crecer 10,9 MB por episodio — a 24
episodios eran 261 MB, el 25 % del límite.

## Por qué este documento existe

Tres cosas de este flujo no se deducen leyendo el código, y las tres cuestan una sesión si se
ignoran.

**El audio se genera a mano, y eso no es una carencia que haya que rodear.** NotebookLM no expone
API de cuenta personal para Audio Overviews. El paso manual —abrir el cuaderno, elegir formato,
pegar la personalización, descargar— es parte del procedimiento. No hay que automatizarlo con
cookies exportadas ni con un navegador teledirigido.

**El producto no obedece la duración que le pidas, y la ventana ya se movió una vez.** El primer
episodio se generó con un prompt que exigía entre 300 y 480 segundos y salió de **989 s (16:29)**,
más del doble del máximo; con esa medición la ventana se fijó en 600–1200 s. El segundo episodio
salió de **1616 s (26:56)** y volvió a caer fuera. Se aplicó la regla en vez de recortar el audio:
la ventana es ahora **600–1800 s**. Escribir un número de minutos en el campo de personalización no
acorta nada, y dos mediciones separadas por diez minutos son poca base — un tercer episodio puede
volver a moverla.

**Los acentos se piden, no se obtienen.** La interfaz no tiene selector de acento por hablante. La
petición de un conductor con español de España y una experta con español de Chile va en el texto de
personalización, y si sale un solo acento hay que anotarlo en el QA del episodio, no declararlo
cumplido. La única comprobación posible es escuchar.

## Pasos

### 1. Preparar el paquete

Plantilla: `penta-agent/skills/publicacion-externa/references/notebooklm-podcast.md`. Produce la
fuente editorial, el texto de personalización y el guion de referencia en
`difusion/paquetes/<ref>/podcast/`. Ese directorio se versiona y está excluido del build
(`_config.yml`).

### 2. Generar el audio en NotebookLM

Cuaderno aislado, **solo** la fuente editorial como origen. Formato **Deep Dive** («Análisis en
profundidad»), longitud **media** —ni *Shorter* ni *Longer*—, español, dos presentadores. Pegar la
personalización. Descargar el `.m4a`.

### 3. Escuchar

Antes de tocar el repositorio. Los cinco puntos están en el `QA.md` de la plantilla: acentos
distintos, roles sostenidos, cifras coincidentes con el post, ausencia de cortes, y que no se lean
instrucciones en voz alta.

### 4. El máster se custodia; nada entra al repositorio

El archivo descargado va a `${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/renders/<ref>/`, según
`docs/gobernanza-repositorio.md`, y ahí se queda. **No hay re-encode ni binario versionado**: el
episodio se sube tal cual a Spotify for Creators, que acepta el máster estéreo.

Al no haber copia en el repositorio, esa carpeta es la única copia propia y no tiene respaldo
remoto. Conviene que entre en `git-bundle-backup` o en Borg.

### 5. Subir el episodio a Spotify for Creators

**Manual, y no hay alternativa**: Spotify for Creators no expone API de publicación, y un show
alojado ahí no puede migrar a un feed externo que uno controle —lo que cerraría el círculo y haría
de cada episodio un `git push`—. New episode → Select a file. Se puede programar la fecha.

La descripción sigue el molde del primer episodio: pregunta gancho, qué hace el episodio y su
resultado defendible, declaración de IA y voces sintéticas, enlace al artículo, y la firma
«3 Cucharadas — Directo al grano.».

**Al comprobar la URL del episodio, usar `-A` con un User-Agent de navegador.** Medido el
2026-09-15: `curl` a secas devuelve **403** sobre un episodio recién publicado y parece roto; con UA
devuelve 200. Un episodio antiguo responde 200 en ambos casos, así que la protección anti-bot
aplica a los recientes.

Apple lo recoge del feed solo. El feed tarda en regenerarse: hay que esperar a que muestre el
episodio antes de registrar nada.

### 6. Encender el bloque en el post

```yaml
audio:
  duracion_s: 1616
  fecha: "2026-09-15"
  generador: NotebookLM (Google)
  voces: 2
  idioma: es
  plataformas:
    - nombre: Spotify
      url: https://open.spotify.com/episode/<ID>
    - nombre: Apple Podcasts
      url: https://podcasts.apple.com/cl/podcast/id<ID-DEL-PROGRAMA>
ai_disclosure:
  components:
    audio: generated
```

Y las mismas URL en `_data/distribucion.yml`, que es donde se registra la publicación.

`_includes/capsula-audio.html` lo renderiza solo; lo invoca `_layouts/single.html` justo antes de
`{{ content }}`. **Solo `plataformas` es obligatoria y hace de guard**: sin al menos una URL no se
renderiza nada, que es exactamente lo que debe pasar mientras el episodio no esté publicado fuera.
Se comprueba `.size > 0` porque en Liquid un array vacío es *truthy*.

`ai_disclosure.components.audio: generated` se mantiene aunque el archivo viva en Spotify: describe
quién produjo la pieza, no dónde se aloja. Importa más que antes, porque la declaración no viaja con
el episodio — Spotify no dice que las voces sean sintéticas.

### 7. Gates

Sin tubería, o midiendo con `$pipestatus[1]` — en zsh, `cmd | tail; echo $?` informa del `tail`:

```bash
ruby scripts/verify_repo_governance.rb --strict     # 0
bundle exec jekyll build -d public
ruby scripts/verify_site_artifact.rb public         # 0
ruby scripts/verify_site_health.rb --profile source # 0
```

Y una comprobación que ningún gate hace por ti, porque unas `plataformas` mal escritas no rompen
nada — el guard simplemente no renderiza el bloque, en silencio:

```bash
grep -c 'class="notice capsula-audio"' public/<permalink>/index.html   # 1, no 0
```

El silencio es deliberado mientras el episodio no esté publicado; deja de serlo en cuanto lo está.
Por eso esta línea es parte del criterio de cierre, no un extra.

### 8. Después del deploy, comprobar los enlaces

```bash
curl -sS -o /dev/null -L -A 'Mozilla/5.0' -w '%{http_code}\n' "<url de Spotify>"   # 200
curl -sS -o /dev/null -L -w '%{http_code}\n' "<url de Apple>"                      # 200
```

Ya no hay archivo propio que medir: la comprobación de rango que antes ocupaba este paso quedó como
medición histórica al final del documento.

### 9. Distribuir a Apple Podcasts (una sola vez por programa)

**No hay que construir ningún feed.** Spotify for Creators genera el RSS al publicar el primer
episodio; está en Settings → Availability → **RSS Distribution** y hay que **habilitarlo** para que
sirva fuera de Spotify. Al hacerlo, el correo del feed se vuelve público: conviene que sea una
dirección de contacto.

Después, en **podcastsconnect.apple.com** con un Apple ID normal —no hace falta cuenta de
desarrollador—: botón **+** → **New Show** → **Add a show with an RSS feed** → pegar la URL del
feed → **Add**. Apple valida y muestra vista previa; si algo falla, avisa antes de dejar seguir.
Luego **Content Rights**, contacto, **Availability** (países, Distribution, **Transcripts**, Show
Release, **Show Claiming**) y **Save** → **Publish**. Aprobación: de horas a un par de días, y no se
vuelve a enviar nada nunca más: cada episodio nuevo entra por el feed.

Dos ajustes que conviene no dejar por defecto: **activar Transcripts**, porque Apple genera
transcripción automática y eso cubre en parte la brecha que el bloque del post declara; y
**restringir Show Claiming**, para que nadie más pueda reclamar el programa.

#### La URL de Apple que se publica no es la que Apple enseña

Medido el 2026-09-13 y cuesta una sesión si se ignora: el slug que muestra Apple lleva el título
completo **con guion largo** (`3-cucharadas-—-datos-...`), y esa URL responde **404**. La canónica
omite el guion largo. La forma que hay que registrar en el repositorio es la corta,
`https://podcasts.apple.com/<pais>/podcast/id<ID>`, que responde 200 y redirige sola a la canónica.
Comprobado en las tiendas `cl` y `us`.

Corolario del mismo día: `https://itunes.apple.com/lookup?id=<ID>` puede devolver `resultCount: 0`
durante horas después de que la página pública ya sirva 200. Ese endpoint consulta el índice de
búsqueda, que va por detrás del catálogo: un cero ahí **no** significa que el programa no exista.

#### Artwork

Apple exige entre **1400×1400 y 3000×3000**, JPG o PNG, RGB. Se sirve desde el feed, así que la
portada se cambia en Spotify, no aquí. Circula un tope de 512 KB de peso que no está en
documentación oficial de Apple; por si acaso, conviene quedar por debajo.

Y una advertencia medida sobre cómo llegar a ese tamaño, en
`~/.local/state/3cucharadas/source-masters/podcast-portada/MANIFIESTO.md`: la herramienta `image_gen`
de Codex —que fue la que generó estas portadas— **no expone parámetro de tamaño** y siempre entrega
~1,57 MP, o sea 1254×1254 en cuadrado. Regenerar con imagen de referencia conserva la composición
pero re-sintetiza los píxeles y sale **14× menos fiel** que ampliar el original con
`waifu2x-ncnn-vulkan -n -1 -s 4` seguido de Lanczos (0,222 frente a 3,167 de diferencia media por
píxel). Para subir de resolución una portada que ya existe, ampliar gana a regenerar.

## Enlaces

- Plantilla del prompt: `penta-agent/skills/publicacion-externa/references/notebooklm-podcast.md`
- Mapa de difusión: `docs/flujo-difusion.md`
- Custodia de binarios: `docs/gobernanza-repositorio.md`
- Purga de caché: `docs/purga-cache-cloudflare.md`
- Portadas y su manifiesto: `~/.local/state/3cucharadas/source-masters/podcast-portada/`

## Mediciones que dejaron de aplicar

Vigentes mientras el sitio alojó el archivo, del 2026-09-13 al 2026-09-15. Se conservan porque
volverían a aplicar si alguna vez se re-alojara un medio propio.

**La extensión del archivo publicado decide si se puede saltar dentro del audio, y `.m4a` no
sirve.** Medido el 2026-09-13 sobre producción, con los dos episodios ya desplegados. Cloudflare
respondía `cf-cache-status: DYNAMIC` a los dos `.m4a` —no está entre las extensiones que cachea— y
en ese modo **no propaga las peticiones de rango**: un `Range: bytes=0-99` devolvía `200` con los
8,3 MB completos en vez de `206`. El contraste que aísla la causa: `assets/videos/catastro-sii-visor.mp4`
y un `.pdf` de `assets/docs`, ambos `cf-cache-status: MISS`, sí devuelven `206` con su
`content-range`. Sin rango no hay forma de adelantar ni retroceder, y cada reproducción descarga el
episodio entero. La salida es la extensión: **`.mp4`**, que es el mismo contenedor MP4 con la misma
pista AAC —renombrar, no recodificar: el sha256 no cambia— y sí entra en la lista de Cloudflare. El
MIME nunca fue el problema: GitLab Pages servía `audio/mp4` correctamente también para `.m4a`.

El contraste citado usaba `assets/videos/catastro-sii-visor.mp4`, que **también se retiró** el
2026-09-15: esa URL ya no existe, así que la medición no es reproducible tal cual, aunque la
conclusión —la extensión decide si Cloudflare cachea, y sin caché no hay rango— sigue en pie.
