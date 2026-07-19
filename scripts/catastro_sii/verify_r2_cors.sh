#!/usr/bin/env bash
set -euo pipefail

# Compara la política CORS declarada en r2-cors.json contra lo que el bucket R2
# responde de verdad. La política se aplica a mano en el dashboard de Cloudflare y
# ningún script la escribía, así que el archivo podía divergir del bucket sin que
# nada lo notara: exactamente lo que pasó con http://127.0.0.1:4001.
#
# No necesita credenciales. Sólo hace preflight OPTIONS contra un objeto público.
# Uso: verify_r2_cors.sh [ruta/r2-cors.json]

policy="${1:-$(dirname "$0")/r2-cors.json}"
: "${PUBLIC_TILES_BASE:=https://tiles.3cucharadas.cl/catastro-sii}"
: "${CORS_PROBE_OBJECT:=}"
# Origen que jamás debe estar permitido: detecta una política abierta de par en par.
: "${CORS_NEGATIVE_ORIGIN:=https://cors-canary.invalid}"

command -v curl >/dev/null || { printf '%s\n' 'Falta curl' >&2; exit 2; }
command -v jq >/dev/null || { printf '%s\n' 'Falta jq' >&2; exit 2; }
[[ -f "${policy}" ]] || { printf 'Política CORS ausente: %s\n' "${policy}" >&2; exit 2; }

if [[ -z "${CORS_PROBE_OBJECT}" ]]; then
  manifest="$(dirname "$0")/../../assets/data/catastro_sii/manifest.json"
  [[ -f "${manifest}" ]] || { printf 'Sin manifest para elegir objeto de prueba\n' >&2; exit 2; }
  CORS_PROBE_OBJECT="$(jq -er '.communes.url | strings' "${manifest}")" \
    || { printf 'Manifest sin capa comunal publicada\n' >&2; exit 2; }
fi

target="${PUBLIC_TILES_BASE%/}/${CORS_PROBE_OBJECT}"
failures=0

# Devuelve el Access-Control-Allow-Origin que R2 concede a un origen dado.
allow_origin_for() {
  local origin="$1" headers
  headers="$(curl --silent --show-error --max-time 20 --dump-header - --output /dev/null \
    -X OPTIONS \
    --header "Origin: ${origin}" \
    --header 'Access-Control-Request-Method: GET' \
    --header 'Access-Control-Request-Headers: range' \
    "${target}" 2>/dev/null || true)"
  printf '%s' "${headers}" \
    | tr -d '\r' \
    | awk 'BEGIN{IGNORECASE=1} /^access-control-allow-origin:/{print $2; exit}'
}

printf 'Verificando CORS declarado contra %s\n' "${target}"

while IFS= read -r origin; do
  [[ -n "${origin}" ]] || continue
  granted="$(allow_origin_for "${origin}")"
  if [[ "${granted}" == "${origin}" || "${granted}" == "*" ]]; then
    printf '  OK       %s\n' "${origin}"
  else
    printf '  DRIFT    %s declarado en la política pero el bucket responde %s\n' \
      "${origin}" "${granted:-sin Access-Control-Allow-Origin}" >&2
    failures=$((failures + 1))
  fi
done < <(jq -r '.[].AllowedOrigins[]? | strings' "${policy}")

# Control negativo: un origen no declarado no puede recibir permiso.
granted="$(allow_origin_for "${CORS_NEGATIVE_ORIGIN}")"
if [[ -n "${granted}" ]]; then
  printf '  ABIERTO  %s recibió %s: la política acepta orígenes no declarados\n' \
    "${CORS_NEGATIVE_ORIGIN}" "${granted}" >&2
  failures=$((failures + 1))
else
  printf '  OK       %s rechazado como corresponde\n' "${CORS_NEGATIVE_ORIGIN}"
fi

if (( failures > 0 )); then
  printf '\n%d discrepancia(s). Aplicar r2-cors.json en el dashboard de Cloudflare\n' "${failures}" >&2
  printf 'o retirar del archivo los orígenes que ya no se necesiten.\n' >&2
  exit 1
fi

printf '\nPolítica CORS del bucket coincide con %s\n' "${policy}"
