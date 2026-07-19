#!/usr/bin/env bash
# Validate a prospective R2 deployment locally. This script deliberately never
# contacts the bucket or public tile origin, and it never invokes rclone copy.
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cors_file="${script_dir}/r2-cors.json"
run_dir=""
errors=()

usage() {
  cat <<'EOF'
Uso: preflight_r2.sh --run-dir DIRECTORIO [--cors-file ARCHIVO]

Valida localmente la configuración de R2 y una corrida autorizada. No realiza
uploads, solicitudes HTTP ni llamadas a la red.
EOF
}

add_error() {
  errors+=("$1")
}

while [[ "$#" -gt 0 ]]; do
  case "$1" in
    --run-dir)
      [[ "$#" -ge 2 ]] || { usage >&2; exit 2; }
      run_dir="$2"
      shift 2
      ;;
    --cors-file)
      [[ "$#" -ge 2 ]] || { usage >&2; exit 2; }
      cors_file="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      printf 'Argumento no reconocido: %s\n' "$1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n "${run_dir}" ]] || add_error "Falta --run-dir con la corrida local que se desplegaría."

for variable in R2_REMOTE R2_BUCKET R2_PREFIX PUBLIC_TILES_BASE; do
  if [[ -z "${!variable:-}" ]]; then
    add_error "Falta variable de entorno ${variable}."
  fi
done

python_bin=""
if command -v python3 >/dev/null 2>&1; then
  python_bin="python3"
else
  add_error "No se encontró python3 para validar JSON local."
fi

if ! command -v rclone >/dev/null 2>&1; then
  add_error "No se encontró rclone en PATH."
elif [[ -n "${R2_REMOTE:-}" ]]; then
  # listremotes only reads the local rclone configuration. Do not use `lsd`,
  # `about`, or another command that could contact the configured remote.
  if ! configured_remotes="$(rclone listremotes 2>/dev/null)"; then
    add_error "No se pudo leer la configuración local de rclone."
  elif ! awk -v expected="${R2_REMOTE}:" '$0 == expected { found = 1 } END { exit !found }' <<<"${configured_remotes}"; then
    add_error "R2_REMOTE no existe en la configuración local de rclone."
  else
    # Read only the remote section's backend identity. Never print the config,
    # endpoint, access key, or secret access key.
    if ! config_file_output="$(rclone config file 2>/dev/null)"; then
      add_error "No se pudo ubicar la configuración local de rclone."
    else
      config_file="$(awk '
        /Configuration file is stored at:/ { next_path = 1; next }
        next_path && NF { print; exit }
      ' <<<"${config_file_output}")"
      if [[ -z "${config_file}" || ! -f "${config_file}" ]]; then
        add_error "No se encontró el archivo de configuración local de rclone."
      elif ! awk -v expected="${R2_REMOTE}" '
        /^\[[^]]+\]$/ {
          section = $0
          sub(/^\[/, "", section)
          sub(/\]$/, "", section)
          next
        }
        section == expected && /^[[:space:]]*type[[:space:]]*=/ {
          value = $0
          sub(/^[^=]*=[[:space:]]*/, "", value)
          backend = tolower(value)
        }
        section == expected && /^[[:space:]]*provider[[:space:]]*=/ {
          value = $0
          sub(/^[^=]*=[[:space:]]*/, "", value)
          provider = tolower(value)
        }
        END { exit !(backend == "s3" && provider == "cloudflare") }
      ' "${config_file}"; then
        add_error "R2_REMOTE debe ser un remoto rclone S3 con proveedor Cloudflare."
      fi
    fi
  fi
fi

if [[ -n "${python_bin}" ]]; then
  if ! cors_issues="$(${python_bin} - "${cors_file}" <<'PY'
import json
import sys
from pathlib import Path


def fail(message: str) -> None:
    print(message)
    raise SystemExit(1)


path = Path(sys.argv[1])
if not path.is_file():
    fail("r2-cors.json está ausente.")
try:
    document = json.loads(path.read_text(encoding="utf-8"))
except (OSError, json.JSONDecodeError):
    fail("r2-cors.json no contiene JSON válido.")

if not isinstance(document, list) or len(document) != 1 or not isinstance(document[0], dict):
    fail("r2-cors.json debe contener exactamente una política CORS.")

policy = document[0]
required_lists = {
    "AllowedOrigins": {"https://3cucharadas.cl", "https://www.3cucharadas.cl"},
    "AllowedMethods": {"GET", "HEAD"},
    "AllowedHeaders": {"Range", "If-None-Match"},
    "ExposeHeaders": {"Accept-Ranges", "Content-Length", "Content-Range", "ETag"},
}
for field, required in required_lists.items():
    value = policy.get(field)
    if not isinstance(value, list) or not all(isinstance(item, str) for item in value):
        fail(f"r2-cors.json requiere una lista de texto en {field}.")
    missing = required.difference(value)
    if missing:
        fail(f"r2-cors.json no declara todos los encabezados/orígenes requeridos en {field}.")

max_age = policy.get("MaxAgeSeconds")
if not isinstance(max_age, int) or isinstance(max_age, bool) or max_age <= 0:
    fail("r2-cors.json requiere MaxAgeSeconds positivo.")
PY
)"; then
    while IFS= read -r issue; do
      [[ -n "${issue}" ]] && add_error "CORS: ${issue}"
    done <<<"${cors_issues}"
  fi

  if [[ -n "${run_dir}" ]]; then
    if ! run_issues="$(${python_bin} - "${run_dir}" "${PUBLIC_TILES_BASE:-}" <<'PY'
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any


root = Path(sys.argv[1])
public_tiles_base = sys.argv[2].rstrip("/")
issues: list[str] = []


def issue(message: str) -> None:
    issues.append(message)


def read_object(path: Path, label: str) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        issue(f"{label} no contiene JSON válido.")
        return None
    if not isinstance(value, dict):
        issue(f"{label} debe ser un objeto JSON.")
        return None
    return value


def object_at(value: object, label: str) -> dict[str, Any] | None:
    if not isinstance(value, dict):
        issue(f"Manifest autorizado sin objeto {label}.")
        return None
    return value


def exact_string(value: object, expected: str, label: str) -> bool:
    if value != expected:
        issue(f"Manifest autorizado con {label} no permitido.")
        return False
    return True


if not root.is_dir():
    issue("--run-dir no es un directorio local legible.")
else:
    root = root.resolve()
    authorized = sorted(root.glob("tiles_manifest_*_authorized.json"))
    if len(authorized) != 1:
        issue("La corrida debe contener exactamente un tiles_manifest_*_authorized.json.")
    else:
        authorized_path = authorized[0]
        match = re.fullmatch(r"tiles_manifest_(\d{8}T\d{6}Z)_authorized\.json", authorized_path.name)
        if match is None:
            issue("El nombre del manifest autorizado no tiene una versión permitida.")
        else:
            version = match.group(1)
            source_path = root / f"tiles_manifest_{version}.json"
            required_assets = {
                f"chile_comunas_brechas_{version}.pmtiles",
                f"predios_region_03_{version}.pmtiles",
                f"basemap_chile_{version}.pmtiles",
                f"basemap_chile_{version}.style.json",
                f"territories_{version}.json",
                "fonts/Noto Sans Regular/0-255.pbf",
            }

            for relative in sorted(required_assets):
                asset = root / relative
                if not asset.is_file() or asset.is_symlink():
                    issue("Activo versionado requerido ausente o no regular.")
                elif asset.resolve().parent != root and root not in asset.resolve().parents:
                    issue("Activo versionado fuera de la corrida local.")
                elif asset.stat().st_size == 0:
                    issue("Activo versionado requerido está vacío.")

            for candidate in root.rglob("*"):
                if not candidate.is_file():
                    continue
                relative = candidate.relative_to(root).as_posix()
                is_tile_asset = (
                    relative.endswith(".pmtiles")
                    or relative.endswith(".pbf")
                    or relative.endswith(".style.json")
                )
                if is_tile_asset and relative not in required_assets:
                    issue("La corrida contiene un activo con nombre no permitido.")

            source = read_object(source_path, "Manifest fuente") if source_path.is_file() else None
            if source is None and not source_path.is_file():
                issue("Falta el manifest fuente auditado junto al autorizado.")
            manifest = read_object(authorized_path, "Manifest autorizado")
            if manifest is not None:
                exact_string(manifest.get("legal_publication_status"), "AUTHORIZED_VECTOR", "legal_publication_status")
                exact_string(manifest.get("build_scope"), "authorized-existing-artifact", "build_scope")
                exact_string(manifest.get("tiles_base"), public_tiles_base, "tiles_base")

                authorization = object_at(manifest.get("publication_authorization"), "publication_authorization")
                if authorization is not None:
                    exact_string(
                        authorization.get("kind"),
                        "project-owner-public-vector-confirmation",
                        "publication_authorization.kind",
                    )
                    exact_string(
                        authorization.get("source_manifest"),
                        source_path.name,
                        "publication_authorization.source_manifest",
                    )
                    if source_path.is_file():
                        expected_digest = hashlib.sha256(source_path.read_bytes()).hexdigest()
                        exact_string(
                            authorization.get("source_manifest_sha256"),
                            expected_digest,
                            "publication_authorization.source_manifest_sha256",
                        )

                results = object_at(manifest.get("results"), "results")
                if results is not None:
                    communes = object_at(results.get("communes"), "results.communes")
                    parcels = object_at(results.get("parcel_regions"), "results.parcel_regions")
                    pilot = object_at(parcels.get("03"), "results.parcel_regions.03") if parcels else None
                    if communes is not None:
                        exact_string(communes.get("url"), f"chile_comunas_brechas_{version}.pmtiles", "results.communes.url")
                        exact_string(communes.get("territories_file"), f"territories_{version}.json", "results.communes.territories_file")
                        if communes.get("available") is not True:
                            issue("Manifest autorizado no habilita la capa comunal.")
                    if pilot is not None:
                        exact_string(pilot.get("url"), f"predios_region_03_{version}.pmtiles", "results.parcel_regions.03.url")
                        exact_string(pilot.get("source_layer"), "predios", "results.parcel_regions.03.source_layer")
                        exact_string(
                            authorization.get("pilot_asset") if authorization else None,
                            f"predios_region_03_{version}.pmtiles",
                            "publication_authorization.pilot_asset",
                        )
                        if pilot.get("available") is not True or pilot.get("pilot") is not True:
                            issue("Manifest autorizado no habilita el piloto predial.")
                        for field in ("minzoom", "maxzoom", "feature_count", "bytes", "source_sha256"):
                            if field not in pilot:
                                issue("Manifest autorizado sin evidencia auditada del piloto predial.")

if issues:
    for item in dict.fromkeys(issues):
        print(item)
    raise SystemExit(1)
PY
)"; then
      while IFS= read -r issue; do
        [[ -n "${issue}" ]] && add_error "Corrida local: ${issue}"
      done <<<"${run_issues}"
    fi
  fi
fi

if [[ "${#errors[@]}" -gt 0 ]]; then
  printf '%s\n' 'Preflight R2 no superado:' >&2
  for error in "${errors[@]}"; do
    printf ' - %s\n' "${error}" >&2
  done
  exit 1
fi

printf '%s\n' 'Preflight R2 local superado: no se realizaron uploads ni solicitudes de red.'
