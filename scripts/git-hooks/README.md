# Git hooks versionados

`.git/hooks/` no se versiona, así que los hooks vivos de este repo se guardan acá
y se instalan con un symlink o una copia.

| Hook | Qué hace | ¿Puede fallar el commit? |
|---|---|---|
| `post-commit` | Avisa por Telegram del commit | No |
| `post-commit-difusion` | Resuelve a qué destinos de difusión corresponde cada post tocado y deja la traza en `difusion/state/destinos/<ref>.json` | No |

## Instalar

```bash
ln -sf ../../scripts/git-hooks/post-commit .git/hooks/post-commit
```

`post-commit-difusion` no se instala como hook independiente: git sólo ejecuta un
archivo por evento. Para tener los dos, encadénalos desde un `post-commit`
propio:

```bash
cat > .git/hooks/post-commit <<'SH'
#!/usr/bin/env bash
root="$(git rev-parse --show-toplevel)"
"$root/scripts/git-hooks/post-commit" || true
"$root/scripts/git-hooks/post-commit-difusion" || true
exit 0
SH
chmod +x .git/hooks/post-commit
```

Ambos terminan en `exit 0` a propósito: un aviso o una traza que falla no debe
tumbar un commit que ya está hecho.

## Difusión: por qué resuelve y no publica

`post-commit-difusion` calcula qué destinos corresponden al artículo y lo escribe.
**No publica.** Publicar sigue siendo:

```bash
cucharadas-difusion publish --ref <ref>     # dry-run por defecto
```

que pasa por revisión humana. Un hook que publicara al commitear pondría el
contenido en público antes de que nadie lo hubiera leído, y el rollback siempre
es posterior al daño.

## Cómo se decide un destino

El catálogo está en `difusion/config/destinos.yml`. Cada destino declara el
**idioma** que consume y el **público** al que habla, más condiciones
verificables. La resolución cruza eso con lo que el post declara de verdad.

Tres estados:

- `listo` — se cumplen todas las condiciones.
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
`republish`, `tags_min`, `verificado`), eso sí requiere extender `_evaluar()`.
