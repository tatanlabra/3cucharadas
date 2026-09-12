# Git hooks versionados

`.git/hooks/` no se versiona, así que los hooks vivos de este repo se guardan acá
y se instalan con un symlink o una copia.

| Hook | Qué hace | ¿Puede fallar el commit? |
|---|---|---|
| `post-commit` | Termina en silencio: un commit no confirma publicación | No |
| `post-commit-difusion` | Resuelve a qué destinos de difusión corresponde cada post tocado y deja la traza en `difusion/state/destinos/<ref>.json` | No |

## Instalar

`post-commit-difusion` no se instala como hook independiente: git sólo ejecuta un
archivo por evento. Instala la cadena versionada con:

```bash
scripts/install_git_hooks.sh
```

Ambos terminan en `exit 0` a propósito: un aviso o una traza que falla no debe
tumbar un commit que ya está hecho.

## Aviso de publicación verificada

Telegram se invoca explícitamente, nunca desde el hook. El emisor
`../notify_telegram_publication.py` exige build local del commit aislado, el
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
`republish`, `tags_min`, `verificado`), eso sí requiere extender `_evaluar()`.
