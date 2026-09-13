# Flujo: de un post publicado a una cápsula de audio

Fecha de revisión: 2026-09-13.

Una **cápsula** es una conversación de dos voces sintéticas sobre un post ya publicado, generada
con NotebookLM y servida desde el propio artículo. No sustituye al post ni añade evidencia: es otra
puerta de entrada al mismo contenido. Donde discrepen, manda el post.

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

### 4. Máster fuera, re-encode dentro

El archivo descargado va a `${XDG_STATE_HOME:-$HOME/.local/state}/3cucharadas/renders/<ref>/`,
según `docs/gobernanza-repositorio.md`. Lo que entra al repositorio es el re-encode mono:

```bash
ffmpeg -i <master> -ac 1 -c:a aac -b:a 64k -movflags +faststart \
  assets/audio/<ref>/capsula-<idioma>-<duración>s.m4a
```

Son voces: el canal estéreo no porta información. Medido en los dos episodios: 31,8 MB → 8,25 MB y
52,0 MB → 13,5 MB, un 74 % menos en ambos, sin pérdida audible. La duración va en el nombre por la
misma razón por la que las imágenes llevan sus dimensiones — si el episodio se regenera, cambia la
ruta y no hay que purgar la caché de Cloudflare. Un reemplazo que conserve la duración exacta **sí**
exige purga.

### 5. Declarar el archivo en el contrato del repositorio

`docs/contracts/repo-governance.yaml`, dentro de `owned_large_files`, con `owner`, `role` y
`retention` no vacíos:

```yaml
  assets/audio/<ref>/capsula-es-<duración>s.m4a:
    owner: editorial-<ref>
    role: capsula-de-audio-publicada-referenciada-por-el-post
    retention: mantener-mientras-el-post-la-enlace
```

Sin esta entrada, `scripts/verify_repo_governance.rb --strict` reprueba con `unowned_large_file` y
tumba el pipeline entero: el umbral es 1 MB. El gate inventaría con `git ls-files`, así que hay que
hacer `git add` del binario **antes** de correrlo — si no, pasa en verde sin haber comprobado nada.

### 6. Encender el bloque en el post

```yaml
audio:
  archivo: /assets/audio/<ref>/capsula-es-<duración>s.m4a
  tipo: audio/mp4
  duracion_s: 989
  bytes: 8253516
  fecha: "2026-09-13"
  generador: NotebookLM (Google)
  voces: 2
  idioma: es
ai_disclosure:
  components:
    audio: generated
```

`_includes/capsula-audio.html` lo renderiza solo; lo invoca `_layouts/single.html` justo antes de
`{{ content }}`. Solo `archivo` es obligatoria y hace de guard: sin ella no se renderiza nada.
Ausente `transcripcion`, el bloque declara la pendencia en vez de callarla.

**No declarar el audio en `_data/visuales/`.** `verify_visual_assets.rb` no lee dimensiones de un
archivo de audio, devolvería `nil`, y el aviso V2 es fatal en `--strict`.

### 7. Gates

Sin tubería, o midiendo con `$pipestatus[1]` — en zsh, `cmd | tail; echo $?` informa del `tail`:

```bash
ruby scripts/verify_repo_governance.rb --strict     # 0
bundle exec jekyll build -d public
ruby scripts/verify_site_artifact.rb public         # 0
ruby scripts/verify_site_health.rb --profile source # 0
```

Y una comprobación que ningún gate hace por ti, porque un `archivo:` mal escrito no rompe nada:

```bash
grep -c 'class="notice capsula-audio"' public/<permalink>/index.html   # 1, no 0
```

### 8. Después del deploy, medir el MIME una vez

```bash
curl -sS -I -4 https://3cucharadas.cl/assets/audio/<ref>/capsula-es-<duración>s.m4a \
  | grep -iE 'content-type|accept-ranges'
```

Se espera `audio/mp4` (o `audio/x-m4a`) y `accept-ranges: bytes`. Sin Range no hay forma de saltar
dentro de un audio que dura media hora. Si GitLab Pages devolviera `application/octet-stream`, con
`x-content-type-options: nosniff` activo el reproductor puede quedarse mudo en Safari: la salida es
renombrar el archivo a `.mp4` —mismo contenedor, misma pista AAC— y actualizar la entrada del
contrato. Producción ya sirve `video/mp4` con `accept-ranges: bytes` para
`assets/videos/catastro-sii-visor.mp4`, medido el 2026-09-13.

## Enlaces

- Plantilla del prompt: `penta-agent/skills/publicacion-externa/references/notebooklm-podcast.md`
- Mapa de difusión: `docs/flujo-difusion.md`
- Custodia de binarios: `docs/gobernanza-repositorio.md`
- Purga de caché: `docs/purga-cache-cloudflare.md`
