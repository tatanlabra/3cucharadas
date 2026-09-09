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
#   scripts/purge_cloudflare_cache.sh --changed            # lo que toco el ultimo commit
#   scripts/purge_cloudflare_cache.sh assets/images/a.png  # rutas explicitas
#   scripts/purge_cloudflare_cache.sh --changed --dry-run
set -euo pipefail

SITE="https://3cucharadas.cl"
CONF="${XDG_CONFIG_HOME:-$HOME/.config}/3cucharadas/secrets.env"
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DRY=0
declare -a PATHS=()

for arg in "$@"; do
  case "$arg" in
    --dry-run) DRY=1 ;;
    --changed)
      # Solo activos versionados que el ultimo commit modifico. Un fichero anadido
      # (A) no necesita purga: su URL es nueva.
      while IFS= read -r f; do
        [ -n "$f" ] && PATHS+=("$f")
      done < <(git -C "$ROOT" diff --name-only --diff-filter=M HEAD~1 HEAD -- 'assets/**' || true)
      ;;
    -*) echo "opcion desconocida: $arg" >&2; exit 2 ;;
    *)  PATHS+=("$arg") ;;
  esac
done

if [ "${#PATHS[@]}" -eq 0 ]; then
  echo "Nada que purgar: ningun activo modificado (los anadidos no lo necesitan)."
  exit 0
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
[ "${#URLS[@]}" -eq 0 ] && { echo "Nada que purgar."; exit 0; }

if [ "$DRY" -eq 1 ]; then
  printf 'Se purgaria:\n'; printf '  %s\n' "${URLS[@]}"; exit 0
fi

# La credencial se carga aqui y no al principio: --dry-run tiene que poder correr sin
# ella, que es justo cuando se quiere mirar antes de tocar nada. El token NUNCA va como
# literal en la linea de comandos, porque los hooks de memoria y el transcript registran
# los comandos; se lee del fichero, que va en 0600.
if [ -z "${CLOUDFLARE_PURGE_TOKEN:-}" ]; then
  [ -r "$CONF" ] || { echo "Falta $CONF (o la variable CLOUDFLARE_PURGE_TOKEN)." >&2; exit 1; }
  # shellcheck disable=SC1090
  set -a; . "$CONF"; set +a
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
echo "Verificando en el borde..."
sleep 5
bad=0
for url in "${URLS[@]}"; do
  rel="${url#$SITE/}"
  local_size=$(stat -c%s "$ROOT/$rel")
  hdr=$(curl -sSI --max-time 45 "$url")
  served=$(printf '%s' "$hdr" | rg -i '^content-length:' | tr -dc '0-9')
  status=$(printf '%s' "$hdr" | rg -i '^cf-cache-status:' | tr -d '\r' | awk '{print $2}')
  if [ "$served" = "$local_size" ]; then
    echo "  OK $rel  $served B  cf=$status"
  else
    echo "  PENDIENTE $rel  borde=$served B  arbol=$local_size B  cf=$status" >&2
    bad=1
  fi
done
[ "$bad" -eq 0 ] || { echo "Alguna URL sigue vieja; reintenta en unos segundos." >&2; exit 1; }
echo "Listo."
