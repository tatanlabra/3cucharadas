#!/usr/bin/env bash
# Verify the deployed Catastro SII tile manifest without credentials or writes.
#
# This is deliberately a post-upload/release guard.  The public manifest must
# match the local candidate, and every enabled PMTiles asset must still support
# browser Range requests from the production origin.  It does not upload,
# promote, rewrite, or delete anything.
set -euo pipefail

readonly SITE_ORIGIN="https://3cucharadas.cl"
readonly DEFAULT_MANIFEST_URL="${SITE_ORIGIN}/assets/data/catastro_sii/manifest.json"
readonly EXPECTED_COMMUNES=345

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
repo_root="$(cd "${script_dir}/../.." && pwd)"
manifest_url="${DEFAULT_MANIFEST_URL}"
local_manifest="${repo_root}/assets/data/catastro_sii/manifest.json"
local_territories="${repo_root}/assets/data/catastro_sii/territories.json"
tiles_base_override=""
curl_bin="${CURL_BIN:-curl}"
temporary_dir=""

usage() {
  cat <<'EOF'
Uso: verify_public_tiles.sh [opciones]

Verifica, sin mutar estado, que el manifest Catastro SII publicado coincide con
el candidato local, conserva 345 comunas y sirve cada PMTiles habilitado con un
GET Range/CORS apto para https://3cucharadas.cl.

Opciones:
  --manifest-url URL       URL HTTPS del manifest público.
                         Por defecto: https://3cucharadas.cl/assets/data/catastro_sii/manifest.json
  --local-manifest PATH    Manifest local que se espera publicar.
  --local-territories PATH Índice local de bounding boxes de las comunas.
  --tiles-base URL         Comprueba explícitamente el origen de tiles declarado.
  --curl-bin PATH          Binario curl (permite un doble en pruebas; sin red).
  -h, --help               Muestra esta ayuda.
EOF
}

fail() {
  printf 'ERROR: %s\n' "$*" >&2
  exit 1
}

cleanup() {
  [[ -n "${temporary_dir}" ]] && rm -rf -- "${temporary_dir}"
}
trap cleanup EXIT

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --manifest-url)
      [[ "$#" -ge 2 ]] || fail 'Falta valor para --manifest-url'
      manifest_url="$2"
      shift 2
      ;;
    --local-manifest)
      [[ "$#" -ge 2 ]] || fail 'Falta valor para --local-manifest'
      local_manifest="$2"
      shift 2
      ;;
    --local-territories)
      [[ "$#" -ge 2 ]] || fail 'Falta valor para --local-territories'
      local_territories="$2"
      shift 2
      ;;
    --tiles-base)
      [[ "$#" -ge 2 ]] || fail 'Falta valor para --tiles-base'
      tiles_base_override="$2"
      shift 2
      ;;
    --curl-bin)
      [[ "$#" -ge 2 ]] || fail 'Falta valor para --curl-bin'
      curl_bin="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "Opción desconocida: $1"
      ;;
  esac
done

command -v "${curl_bin}" >/dev/null 2>&1 || fail "No se encontró curl: ${curl_bin}"
command -v jq >/dev/null 2>&1 || fail 'Falta jq'
command -v rg >/dev/null 2>&1 || fail 'Falta rg'
[[ "${manifest_url}" == https://* ]] || fail "El manifest público debe usar HTTPS: ${manifest_url}"
[[ -f "${local_manifest}" ]] || fail "Manifest local ausente: ${local_manifest}"
[[ -f "${local_territories}" ]] || fail "Índice local de comunas ausente: ${local_territories}"

temporary_dir="$(mktemp -d "${TMPDIR:-/tmp}/catastro-public-verify.XXXXXX")"
public_manifest="${temporary_dir}/manifest.public.json"
public_territories="${temporary_dir}/territories.public.json"
local_manifest_canonical="${temporary_dir}/manifest.local.canonical.json"
public_manifest_canonical="${temporary_dir}/manifest.public.canonical.json"
local_territories_canonical="${temporary_dir}/territories.local.canonical.json"
public_territories_canonical="${temporary_dir}/territories.public.canonical.json"
public_style="${temporary_dir}/basemap.style.public.json"

fetch_json() {
  local url="$1"
  local output="$2"
  "${curl_bin}" --fail --silent --show-error --location --output "${output}" "${url}"
}

canonical_json() {
  local source="$1"
  local output="$2"
  jq -eS . "${source}" > "${output}"
}

declared_communes_count() {
  local source="$1"
  jq -er '
    .communes
    | if type == "object" then length else error("communes debe ser objeto") end
  ' "${source}"
}

verify_territories() {
  local source="$1"
  local label="$2"
  local count
  count="$(declared_communes_count "${source}")" || fail "Índice territorial ${label} inválido"
  [[ "${count}" -eq "${EXPECTED_COMMUNES}" ]] || {
    fail "Índice territorial ${label}: se esperaban ${EXPECTED_COMMUNES} comunas y hay ${count}"
  }
  jq -e '.communes | has("12202") | not' "${source}" >/dev/null \
    || fail "Índice territorial ${label}: no puede incluir la exclusión declarada 12202"
}

resolve_manifest_asset_url() {
  local path="$1"
  local remainder origin directory
  case "${path}" in
    https://*)
      printf '%s\n' "${path}"
      ;;
    /*)
      remainder="${manifest_url#https://}"
      origin="https://${remainder%%/*}"
      printf '%s%s\n' "${origin}" "${path}"
      ;;
    *)
      directory="${manifest_url%/*}"
      printf '%s/%s\n' "${directory}" "${path}"
      ;;
  esac
}

require_versioned_name() {
  local name="$1"
  local expression="$2"
  local label="$3"
  [[ "${name}" =~ ${expression} ]] \
    || fail "${label} no referencia un PMTiles versionado permitido: ${name}"
}

range_cors_check() {
  local label="$1"
  local url="$2"
  local headers="${temporary_dir}/${label//[^A-Za-z0-9]/_}.headers"

  if ! "${curl_bin}" --fail --silent --show-error --location \
      --dump-header "${headers}" --output /dev/null \
      --header "Origin: ${SITE_ORIGIN}" --range 0-126 "${url}"; then
    fail "${label}: el GET Range público falló: ${url}"
  fi
  rg -qi '^HTTP/[0-9.]+ 206' "${headers}" \
    || fail "${label}: el GET Range no respondió 206"
  rg -qi '^accept-ranges:[[:space:]]*bytes' "${headers}" \
    || fail "${label}: falta Accept-Ranges: bytes"
  rg -qi '^content-range:[[:space:]]*bytes[[:space:]]+0-126/[0-9]+' "${headers}" \
    || fail "${label}: falta Content-Range para bytes 0-126"
  rg -qi "^access-control-allow-origin:[[:space:]]*${SITE_ORIGIN}" "${headers}" \
    || fail "${label}: CORS no permite ${SITE_ORIGIN}"
  rg -qi '^access-control-expose-headers:.*accept-ranges' "${headers}" \
    || fail "${label}: CORS no expone Accept-Ranges"
  rg -qi '^access-control-expose-headers:.*content-range' "${headers}" \
    || fail "${label}: CORS no expone Content-Range"
  printf 'PASS %s Range/CORS: %s\n' "${label}" "${url}"
}

cors_get_check() {
  local label="$1"
  local url="$2"
  local headers="${temporary_dir}/${label//[^A-Za-z0-9]/_}.headers"

  if ! "${curl_bin}" --fail --silent --show-error --location \
      --dump-header "${headers}" --output /dev/null \
      --header "Origin: ${SITE_ORIGIN}" "${url}"; then
    fail "${label}: el GET público falló: ${url}"
  fi
  rg -qi '^HTTP/[0-9.]+ 200' "${headers}" \
    || fail "${label}: el GET público no respondió 200"
  rg -qi "^access-control-allow-origin:[[:space:]]*${SITE_ORIGIN}" "${headers}" \
    || fail "${label}: CORS no permite ${SITE_ORIGIN}"
  printf 'PASS %s GET/CORS: %s\n' "${label}" "${url}"
}

fetch_json "${manifest_url}" "${public_manifest}" \
  || fail "No se pudo obtener el manifest público: ${manifest_url}"
canonical_json "${local_manifest}" "${local_manifest_canonical}" \
  || fail "Manifest local JSON inválido: ${local_manifest}"
canonical_json "${public_manifest}" "${public_manifest_canonical}" \
  || fail "Manifest público JSON inválido: ${manifest_url}"
cmp -s "${local_manifest_canonical}" "${public_manifest_canonical}" \
  || fail 'El manifest público no coincide semánticamente con el manifest local candidato'

status="$(jq -er '.legal_publication_status | strings' "${public_manifest}")" \
  || fail 'Manifest público sin legal_publication_status válido'
case "${status}" in
  PENDING)
    fail 'El manifest público sigue PENDING; no es un release verificable'
    ;;
  AUTHORIZED_VECTOR|AUTHORIZED_RASTER_ONLY)
    ;;
  *)
    fail "Estado de publicación no permitido en producción: ${status}"
    ;;
esac

tiles_base="$(jq -er '.tiles_base | strings | rtrimstr("/")' "${public_manifest}")" \
  || fail 'Manifest público sin tiles_base'
[[ "${tiles_base}" == https://* ]] || fail "tiles_base debe usar HTTPS: ${tiles_base}"
if [[ -n "${tiles_base_override}" ]]; then
  [[ "${tiles_base_override%/}" == "${tiles_base}" ]] \
    || fail "--tiles-base no coincide con el manifest público: ${tiles_base_override} != ${tiles_base}"
fi

communes_available="$(jq -er '.communes.available' "${public_manifest}")" \
  || fail 'Manifest público sin communes.available'
[[ "${communes_available}" == true ]] \
  || fail 'El manifest público no declara disponible la capa comunal nacional'
[[ "$(jq -er '.communes.source_layer | strings' "${public_manifest}")" == 'comunas' ]] \
  || fail 'La capa comunal no declara source_layer=comunas'
jq -e '.communes.excluded_communes | type == "array" and index("12202") != null' "${public_manifest}" >/dev/null \
  || fail 'La capa comunal debe declarar la exclusión 12202'

basemap_name="$(jq -er '.basemap.url | strings' "${public_manifest}")" \
  || fail 'Manifest público sin URL de basemap'
style_name="$(jq -er '.basemap.style_url | strings' "${public_manifest}")" \
  || fail 'Manifest público sin URL de estilo de basemap'
communes_name="$(jq -er '.communes.url | strings' "${public_manifest}")" \
  || fail 'Manifest público sin URL de capa comunal'
pilot_name="$(jq -er '.parcel_regions["03"].url | strings' "${public_manifest}")" \
  || fail 'Manifest público sin URL de piloto Atacama'
require_versioned_name "${basemap_name}" '^basemap_chile_[0-9]{8}(T[0-9]{6}Z)?[.]pmtiles$' 'Basemap'
require_versioned_name "${style_name}" '^basemap_chile_[0-9]{8}(T[0-9]{6}Z)?[.]style[.]json$' 'Estilo de basemap'
require_versioned_name "${communes_name}" '^chile_comunas_brechas_[0-9]{8}(T[0-9]{6}Z)?[.]pmtiles$' 'Capa comunal'
require_versioned_name "${pilot_name}" '^predios_region_03_[0-9]{8}(T[0-9]{6}Z)?[.]pmtiles$' 'Piloto Atacama'

[[ "$(jq -er '.basemap.available' "${public_manifest}")" == true ]] \
  || fail 'El manifest público no declara disponible el basemap autoalojado'

unexpected_regions="$(jq -r '.parcel_regions | keys[] | select(. != "03")' "${public_manifest}")"
[[ -z "${unexpected_regions}" ]] \
  || fail "Manifest público expone una región predial no autorizada: ${unexpected_regions}"
pilot_available="$(jq -er '.parcel_regions["03"].available' "${public_manifest}")" \
  || fail 'Manifest público sin parcel_regions.03.available'
if [[ "${pilot_available}" == true ]]; then
  [[ "${status}" == 'AUTHORIZED_VECTOR' ]] \
    || fail 'El piloto Atacama expuesto exige AUTHORIZED_VECTOR'
  [[ "$(jq -er '.parcel_regions["03"].pilot' "${public_manifest}")" == true ]] \
    || fail 'La región 03 expuesta debe declararse como piloto'
  [[ "$(jq -er '.parcel_regions["03"].source_layer | strings' "${public_manifest}")" == 'predios' ]] \
    || fail 'El piloto Atacama no declara source_layer=predios'
elif [[ "${status}" == 'AUTHORIZED_RASTER_ONLY' ]]; then
  :
elif [[ "${pilot_available}" != false ]]; then
  fail 'parcel_regions.03.available debe ser booleano'
fi

territories_path="$(jq -er '.communes.territories_url | strings' "${public_manifest}")" \
  || fail 'Manifest público sin territories_url comunal'
public_territories_url="$(resolve_manifest_asset_url "${territories_path}")"
[[ "${public_territories_url}" == https://* ]] \
  || fail "territories_url debe resolver a HTTPS: ${public_territories_url}"
fetch_json "${public_territories_url}" "${public_territories}" \
  || fail "No se pudo obtener el índice territorial público: ${public_territories_url}"
verify_territories "${local_territories}" 'local'
verify_territories "${public_territories}" 'público'
canonical_json "${local_territories}" "${local_territories_canonical}" \
  || fail "Índice territorial local JSON inválido: ${local_territories}"
canonical_json "${public_territories}" "${public_territories_canonical}" \
  || fail "Índice territorial público JSON inválido: ${public_territories_url}"
cmp -s "${local_territories_canonical}" "${public_territories_canonical}" \
  || fail 'El índice territorial público no coincide con el candidato local'

style_url="${tiles_base}/${style_name}"
fetch_json "${style_url}" "${public_style}" \
  || fail "No se pudo obtener el estilo público: ${style_url}"
jq -e --arg basemap "${basemap_name}" --arg glyphs 'fonts/{fontstack}/{range}.pbf' '
  .version == 8
  and .glyphs == $glyphs
  and .sources.protomaps.type == "vector"
  and .sources.protomaps.url == $basemap
' "${public_style}" >/dev/null \
  || fail 'El estilo público no referencia el basemap y fuente versionados esperados'

range_cors_check 'basemap' "${tiles_base}/${basemap_name}"
cors_get_check 'estilo-basemap' "${style_url}"
cors_get_check 'fuente-noto' "${tiles_base}/fonts/Noto%20Sans%20Regular/0-255.pbf"
range_cors_check 'comunas' "${tiles_base}/${communes_name}"
[[ "${pilot_available}" == true ]] \
  && range_cors_check 'Atacama' "${tiles_base}/${pilot_name}"

printf 'PASS manifest público, %s comunas y PMTiles habilitados verificados.\n' "${EXPECTED_COMMUNES}"
