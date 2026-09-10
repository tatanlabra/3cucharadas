#!/usr/bin/env bash
# Purga la cache de borde de Cloudflare para los activos que cambiaron.
#
# Por que hace falta: Cloudflare guarda su propia copia de cada fichero durante
# `max-age` (14400 s = 4 h en este sitio). Mientras viva, todo visitante recibe esos
# bytes aunque el origen ya tenga otros. Un fichero con nombre NUEVO no sufre esto
# --Cloudflare no tenia copia--; el problema es solo sobrescribir conservando el nombre,
# que es lo que hacen las piezas marcadas `nombre_legacy` en _data/visuales/.
#
# Y una trampa que cuesta una purga entera: purgar ANTES de que el despliegue termine
# hace que Cloudflare vuelva a traer el fichero VIEJO del origen y lo cachee otras 4 h.
# Por eso este script comprueba primero que el origen ya sirve los bytes nuevos, y se
# niega a purgar si no.
#
# Uso:
#   scripts/purge_cloudflare_cache.sh --changed              # lo que toco el ultimo commit
#   scripts/purge_cloudflare_cache.sh --since origin/main    # todo lo pendiente de publicar
#   scripts/purge_cloudflare_cache.sh --range A..B           # un rango explicito
#   scripts/purge_cloudflare_cache.sh assets/images/a.png    # rutas explicitas
#   scripts/purge_cloudflare_cache.sh --changed --dry-run
#
# Codigos de salida:
#   0  purga verificada en el borde (o --dry-run correcto)
#   1  el despliegue no llego, la API rechazo, o el borde sigue viejo / no concluyente
#   2  error de uso
#   3  el selector no encontro ningun activo (ver --allow-empty)
#
# Por que el 3 existe: un selector que no encuentra nada imprimia "Nada que purgar" y
# salia 0. Medido el 2026-09-09: los activos del post del HUD habian cambiado en
# 50a16c15, dos commits antes de HEAD, y `--changed` --que mira solo HEAD~1..HEAD--
# informaba exito habiendo purgado nada. Un exito que no hizo nada es peor que un fallo.
set -euo pipefail

SITE="https://3cucharadas.cl"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}/3cucharadas/secrets.env"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY=0
ALLOW_EMPTY=0
SELECTOR=""
declare -a PATHS=()

# Activos modificados (M) en un rango. Un fichero anadido (A) no necesita purga:
# su URL es nueva y Cloudflare no tenia copia.
collect_range() {
  local range="$1"
  while IFS= read -r f; do
    [ -n "$f" ] && PATHS+=("$f")
  done < <(git -C "$ROOT" diff --name-only --diff-filter=M "$range" -- 'assets/**' || true)
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --dry-run)     DRY=1 ;;
    --allow-empty) ALLOW_EMPTY=1 ;;
    --changed)     SELECTOR="HEAD~1..HEAD"; collect_range "HEAD~1..HEAD" ;;
    --since)
      [ "$#" -ge 2 ] || { echo "--since necesita una referencia (ej: origin/main)" >&2; exit 2; }
      git -C "$ROOT" rev-parse --verify --quiet "$2" >/dev/null \
        || { echo "referencia desconocida: $2" >&2; exit 2; }
      SELECTOR="$2..HEAD"; collect_range "$2..HEAD"; shift ;;
    --range)
      [ "$#" -ge 2 ] || { echo "--range necesita A..B" >&2; exit 2; }
      case "$2" in *..*) ;; *) echo "--range espera la forma A..B, no: $2" >&2; exit 2 ;; esac
      SELECTOR="$2"; collect_range "$2"; shift ;;
    -*) echo "opcion desconocida: $1" >&2; exit 2 ;;
    *)  PATHS+=("$1") ;;
  esac
  shift
done

if [ "${#PATHS[@]}" -eq 0 ]; then
  if [ -n "$SELECTOR" ]; then
    echo "El selector '$SELECTOR' no encontro ningun activo modificado bajo assets/." >&2
    echo "Si los activos cambiaron en un commit anterior, usa --since <ref> o rutas explicitas." >&2
  else
    echo "No se indico ningun activo. Usa --changed, --since <ref>, --range A..B o rutas." >&2
  fi
  [ "$ALLOW_EMPTY" -eq 1 ] && { echo "(--allow-empty: se acepta como exito)"; exit 0; }
  exit 3
fi

echo "Comprobando que el origen ya sirve los bytes nuevos..."
declare -a URLS=()
stale=0
for rel in "${PATHS[@]}"; do
  local_size=$(stat -c%s "$ROOT/$rel" 2>/dev/null || echo 0)
  [ "$local_size" -eq 0 ] && { echo "  ?  $rel (no existe en el arbol; se omite)"; continue; }
  # El parametro aleatorio evita la clave de cache y llega al origen de verdad.
  served=$(curl -sS --max-time 45 -o /dev/null -w '%{size_download}' \
    "$SITE/$rel?purgecheck=$RANDOM$RANDOM" || echo 0)
  if [ "$served" = "$local_size" ]; then
    echo "  OK $rel ($local_size B)"
    URLS+=("$SITE/$rel")
  else
    echo "  NO $rel: el origen da $served B y el arbol $local_size B" >&2
    stale=1
  fi
done

if [ "$stale" -ne 0 ]; then
  echo "El despliegue todavia no llego. Purgar ahora recachearia lo viejo otras 4 h." >&2
  exit 1
fi
[ "${#URLS[@]}" -eq 0 ] && { echo "Ningun activo comprobable en el origen." >&2; exit 3; }

if [ "$DRY" -eq 1 ]; then
  printf 'Se purgaria:\n'; printf '  %s\n' "${URLS[@]}"; exit 0
fi

# La credencial se carga aqui y no al principio: --dry-run tiene que poder correr sin
# ella, que es justo cuando se quiere mirar antes de tocar nada. El token NUNCA va como
# literal en la linea de comandos, porque los hooks de memoria y el transcript registran
# los comandos; se lee del fichero, que va en 0600.
if [ -z "${CLOUDFLARE_PURGE_TOKEN:-}" ]; then
  [ -r "$CONF" ] || { echo "Falta $CONF (o la variable CLOUDFLARE_PURGE_TOKEN)." >&2; exit 1; }
  set -a
  # shellcheck disable=SC1090
  . "$CONF"
  set +a
fi
: "${CLOUDFLARE_PURGE_TOKEN:?falta CLOUDFLARE_PURGE_TOKEN}"
: "${CLOUDFLARE_ZONE_ID:?falta CLOUDFLARE_ZONE_ID}"

payload=$(printf '%s\n' "${URLS[@]}" | jq -R . | jq -s '{files: .}')
resp=$(curl -sS --max-time 60 -X POST \
  "https://api.cloudflare.com/client/v4/zones/$CLOUDFLARE_ZONE_ID/purge_cache" \
  -H "Authorization: Bearer $CLOUDFLARE_PURGE_TOKEN" \
  -H 'Content-Type: application/json' \
  --data "$payload")

if [ "$(printf '%s' "$resp" | jq -r .success)" != "true" ]; then
  printf '%s' "$resp" | jq -c '{success, errors}' >&2
  exit 1
fi
echo "Purga aceptada por la API."

# Aceptada no es hecha: se comprueba contra el borde, que es lo que ve un visitante.
#
# Todo lo que sigue va con `|| true` y sin `rg`, por dos razones medidas el 2026-09-09:
# (1) con `set -euo pipefail`, un `grep`/`rg` que no encuentra la cabecera sale 1, pipefail
#     lo propaga y la asignacion MATA el script --con la purga ya gastada y sin verificar--
#     sin imprimir nada. Pasa de verdad cuando la respuesta es chunked, un 304 o una pagina
#     de error, que son justo los casos en los que hay que mirar.
# (2) `rg` no existe en la imagen ruby:3.3; `grep` esta en cualquier parte.
echo "Verificando en el borde..."
sleep 5
bad=0
unknown=0
for url in "${URLS[@]}"; do
  rel="${url#"$SITE"/}"
  local_size=$(stat -c%s "$ROOT/$rel" 2>/dev/null || echo 0)
  hdr=$(curl -sSI --max-time 45 "$url" || true)
  code=$(printf '%s' "$hdr" | grep -iE '^HTTP/' | tail -1 | awk '{print $2}' || true)
  served=$(printf '%s' "$hdr" | grep -i '^content-length:' | tr -dc '0-9' || true)
  status=$(printf '%s' "$hdr" | grep -i '^cf-cache-status:' | tr -d '\r' | awk '{print $2}' || true)
  if [ -z "$served" ]; then
    echo "  NO CONCLUYENTE $rel  http=${code:-?}  cf=${status:-?}  (sin content-length)" >&2
    unknown=1
  elif [ "$served" = "$local_size" ]; then
    echo "  OK $rel  $served B  cf=${status:-?}"
  else
    echo "  PENDIENTE $rel  borde=$served B  arbol=$local_size B  cf=${status:-?}" >&2
    bad=1
  fi
done
if [ "$bad" -ne 0 ]; then
  echo "Alguna URL sigue vieja; reintenta en unos segundos." >&2; exit 1
fi
if [ "$unknown" -ne 0 ]; then
  echo "La purga fue aceptada, pero el borde no permitio comprobarla. Verificalo a mano." >&2
  exit 1
fi
echo "Listo."
