# 3cucharadas-difusion

Herramienta local para preparar, revisar y publicar una cadena bilingue en
Mastodon y Bluesky. El blog en `https://3cucharadas.cl` sigue siendo la fuente
canonica; la GUI nunca recibe credenciales y publicar exige aprobacion humana.

## Instalacion reproducible

Desde este directorio:

```bash
conda env create -f environment.yml
conda activate 3cucharadas-difusion
```

No se modifica Python del sistema ni `~/.zshrc`. Para actualizar el entorno:

```bash
conda env update -n 3cucharadas-difusion -f environment.yml --prune
```

`environment.lock.yml` conserva las versiones resueltas y se usa para una
recreacion exacta de la linea base validada.

Preparar los secretos fuera del repositorio:

```bash
install -d -m 700 ~/.config/3cucharadas-difusion
cp config/secrets.env.example ~/.config/3cucharadas-difusion/secrets.env
chmod 600 ~/.config/3cucharadas-difusion/secrets.env
```

Usar un token de aplicacion Mastodon con alcance minimo `write:statuses` y una
App Password dedicada de Bluesky. Nunca usar la contrasena principal.

## Flujo CASEN

```bash
cucharadas-difusion doctor
cucharadas-difusion doctor --auth  # autentica ambas cuentas sin publicar
cucharadas-difusion prepare \
  _posts/2026-03-15-casen2024-julia-waffles-politica-publica.md \
  --provider auto
```

`prepare` verifica las dos URLs publicas, intenta Antigravity mediante
`agy-bridge`, luego DeepSeek mediante `ai-delegate cheap-code` y finalmente
Claude Code. Si todos fallan, abre un borrador vacio para escritura manual y
mantiene bloqueado el boton de publicacion.

La revision se sirve solo en `127.0.0.1`, usa un token efimero en el fragmento
de la URL y se abre con `xdg-open`. Un toast de KDE permite reabrirla. Cerrar el
navegador no borra el borrador:

```bash
cucharadas-difusion review casen2024-julia-waffles
```

Alternativas de terminal:

```bash
cucharadas-difusion preview casen2024-julia-waffles
cucharadas-difusion publish casen2024-julia-waffles        # dry-run
cucharadas-difusion publish casen2024-julia-waffles --live # confirmacion escrita
```

La GUI edita solo dos mensajes base, ES y EN. Las cuatro tarjetas se derivan de
ellos: Mastodon agrega su URL UTM y Bluesky conserva exactamente el mensaje base
con una tarjeta externa. Cualquier cambio editorial invalida las dos aprobaciones.

`publish --live` publica ES como raiz y EN como autorrespuesta. La interfaz
muestra progreso por cada pieza y luego consulta las APIs publicas para confirmar
hilo, idioma, tarjetas, imagenes y facets. El estado final exitoso es
`published_verified`; tambien puede repetirse esa comprobacion sin publicar:

```bash
cucharadas-difusion verify casen2024-julia-waffles
```

Bluesky recibe
facets UTF-8 para los hashtags y una tarjeta externa con la imagen OG existente;
la herramienta no genera imagenes. El ledger local
evita duplicados y permite continuar o revertir:

```bash
cucharadas-difusion resume casen2024-julia-waffles
cucharadas-difusion rollback casen2024-julia-waffles --network mastodon
```

Sin `--live`, ambos comandos son simulacros.

## Proveedores de copy

`PENTA_AGENT_ROOT` debe apuntar al repositorio canonico `penta-agent`. La
herramienta nunca invoca `agy` directamente. DeepSeek se usa solo si LiteLLM ya
esta listo en `127.0.0.1:4000`; la CLI no inicia Docker de forma silenciosa.

Para habilitarlo, usar el flujo documentado dentro de penta-agent:

```bash
cd "$PENTA_AGENT_ROOT/ai-sidecars/litellm"
docker compose config --no-env-resolution -q
docker compose up -d
curl -fsS http://127.0.0.1:4000/health/readiness
```

Los proveedores reciben solo titulo, descripcion, tags y URLs publicas. Sus
salidas son borradores, se validan y nunca pueden llamar a las APIs sociales.

## DEV, Medium y otros destinos

```bash
cucharadas-difusion destinations status casen2024-julia-waffles
cucharadas-difusion destinations checklist casen2024-julia-waffles
```

- DEV consume `/feed-dev-en.xml` como borradores; revisar y fijar la URL
  canonica de 3cucharadas antes de publicar.
- Medium se importa manualmente desde la URL inglesa limpia y se verifica el
  `canonical` resultante.
- JuliaBloggers queda en monitoreo. Planet Python, R-bloggers, OSGeo/OSM y
  EconAcademics se mantienen bloqueados hasta cumplir sus gates editoriales.

## Estado, depuracion y rollback

- Borradores: `~/.local/state/3cucharadas-difusion/drafts/`.
- Ledger append-only: `~/.local/state/3cucharadas-difusion/ledger.jsonl`.
- Secretos: `~/.config/3cucharadas-difusion/secrets.env`, modo `0600`.
- `Ctrl+C` detiene la GUI; `review <ref>` la reabre sin perder cambios.
- Un estado `partial` se inspecciona en el ledger y se retoma con `resume`.

## Pruebas

```bash
python -m pytest
JEKYLL_ENV=production bundle exec jekyll build --future
```

Las pruebas de red usan dobles; no escriben en Mastodon ni Bluesky.
