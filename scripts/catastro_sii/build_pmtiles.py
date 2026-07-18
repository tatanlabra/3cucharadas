#!/usr/bin/env python3
"""Build audited PMTiles without mutating the canonical SII GeoParquet.

The script intentionally has two products.  A communal layer joins public aggregate
metrics to an approved boundary source.  The parcel pilot reads only the canonical
Caldera and Diego de Almagro GeoParquet files, retains destination H geometries,
constructs a new allowlisted GeoDataFrame, and feeds FlatGeobuf to Tippecanoe.

`--publishable` is a safety boundary: parcel output cannot be marked publishable
unless LEGAL_PUBLICATION_STATUS is AUTHORIZED_VECTOR.  Private validation artefacts
remain possible with the default PENDING status but must not be uploaded to R2.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import UTC, datetime
from math import ceil
from pathlib import Path
from typing import Any, Iterable

import geopandas as gpd
import pandas as pd


LEGAL_VALUES = {"AUTHORIZED_VECTOR", "AUTHORIZED_RASTER_ONLY", "PENDING", "REJECTED"}
PILOT_SOURCES = {
    "03102": "caldera_3202.parquet",
    "03202": "diego_de_almagro_3102.parquet",
}
PUBLIC_PARCEL_FIELDS = {
    "cod_region",
    "cod_comuna",
    "destino_clase",
    "calidad_geometrica",
    "version_datos",
    "geometry",
}
FORBIDDEN_FIELD_FRAGMENTS = (
    "direccion", "address", "rol", "propiet", "run", "folio", "cliente", "interno",
    "avaluo", "valor", "sup_", "superficie", "predio", "manzana", "utm", "match",
)
TILE_BUDGET_BYTES = {
    "p50": 150 * 1024,
    "p95": 500 * 1024,
    "max": 1024 * 1024,
}


@dataclass(frozen=True)
class BuildResult:
    path: Path
    layer: str
    minzoom: int
    maxzoom: int
    feature_count: int
    bytes_written: int
    source_sha256: dict[str, str]
    territories_file: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


def run(command: list[str], *, capture: bool = False) -> subprocess.CompletedProcess[str]:
    print("+", " ".join(command), flush=True)
    return subprocess.run(command, check=True, text=True, capture_output=capture)


def require_programs(*programs: str) -> None:
    missing = [program for program in programs if shutil.which(program) is None]
    if missing:
        raise RuntimeError(f"Herramientas requeridas ausentes: {', '.join(missing)}")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_code(value: object) -> str:
    text = str(value).strip()
    if text.endswith(".0"):
        text = text[:-2]
    if not text.isdigit() or len(text) not in (4, 5):
        raise ValueError(f"Código comunal inválido: {value!r}")
    return text.zfill(5)


def ensure_valid_geometries(frame: gpd.GeoDataFrame, label: str) -> None:
    if frame.empty:
        raise RuntimeError(f"{label}: no contiene entidades publicables")
    missing = int(frame.geometry.isna().sum())
    empty = int(frame.geometry.is_empty.sum())
    invalid = int((~frame.geometry.is_valid).sum())
    if missing or empty or invalid:
        raise RuntimeError(
            f"{label}: geometrías no publicables (nulas={missing}, vacías={empty}, inválidas={invalid}). "
            "La fuente maestra no se repara ni se altera; revisar el reporte de origen."
        )


def ensure_public_parcel_schema(frame: gpd.GeoDataFrame) -> None:
    columns = set(frame.columns)
    if columns != PUBLIC_PARCEL_FIELDS:
        raise RuntimeError(f"Esquema público predial inesperado: {sorted(columns)}")
    leaked = [column for column in columns if any(fragment in column.lower() for fragment in FORBIDDEN_FIELD_FRAGMENTS)]
    if leaked:
        raise RuntimeError(f"Atributos prohibidos en salida predial: {leaked}")


def select_public_residential_geometries(
    raw: gpd.GeoDataFrame,
    label: str,
) -> tuple[gpd.GeoDataFrame, dict[str, int]]:
    """Create a read-only public selection and account for unrenderable records.

    Empty and null source geometries cannot be encoded as vector tiles. They are
    excluded from the derivative only and counted in the build manifest; the
    canonical GeoParquet is never repaired, rewritten, or otherwise mutated.
    Non-empty invalid geometries remain a hard failure because silently dropping
    them would conceal a material source-quality issue.
    """
    residential = raw.loc[
        raw["dc_cod_destino"].fillna("").astype(str).str.strip().eq("H"),
        ["geometry"],
    ].copy()
    missing = residential.geometry.isna()
    empty = ~missing & residential.geometry.is_empty
    invalid = ~missing & ~empty & ~residential.geometry.is_valid
    if int(invalid.sum()):
        raise RuntimeError(
            f"{label}: geometrías residenciales inválidas no vacías={int(invalid.sum())}; "
            "la fuente maestra no se repara ni se altera."
        )
    usable = residential.loc[~missing & ~empty].copy()
    ensure_valid_geometries(usable, label)
    return usable, {
        "residential_input": int(len(residential)),
        "excluded_null_geometries": int(missing.sum()),
        "excluded_empty_geometries": int(empty.sum()),
    }


def public_parcel_frame(
    geometries: gpd.GeoDataFrame,
    commune_code: str,
    version: str,
    crs: Any,
) -> gpd.GeoDataFrame:
    """Build the allowlisted derivative while preserving the selected row index."""
    return gpd.GeoDataFrame(
        {
            "cod_region": "03",
            "cod_comuna": commune_code,
            "destino_clase": "Residencial",
            "calidad_geometrica": "Referencial",
            "version_datos": version,
        },
        index=geometries.index,
        geometry=geometries.geometry,
        crs=crs,
    ).to_crs(4326)


def write_fgb(frame: gpd.GeoDataFrame, path: Path, layer: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    frame.to_file(path, layer=layer, driver="FlatGeobuf", index=False)


def tippecanoe(
    source: Path,
    output: Path,
    layer: str,
    minzoom: int,
    maxzoom: int,
    fields: Iterable[str],
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    command = [
        "tippecanoe", "--force", "--output", str(output), "--layer", layer,
        "--minimum-zoom", str(minzoom), "--maximum-zoom", str(maxzoom),
        "--projection=EPSG:4326", "--simplify-only-low-zooms",
        "--no-simplification-of-shared-nodes", "--no-tiny-polygon-reduction-at-maximum-zoom",
        "--extend-zooms-if-still-dropping",
    ]
    for field in fields:
        command.extend(["--include", field])
    command.append(str(source))
    run(command)


def validate_pmtiles(path: Path, expected_layer: str, report: Path) -> None:
    # conda-forge's Python PMTiles package exposes pmtiles-show rather than the
    # unrelated Go CLI named pmtiles. Keep the build tied to the installed tool.
    result = run(["pmtiles-show", str(path)], capture=True)
    if expected_layer not in result.stdout:
        raise RuntimeError(f"{path.name}: PMTiles no declara la capa {expected_layer!r}")
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(result.stdout, encoding="utf-8")


def nearest_rank(values: list[int], percentile: float) -> int:
    if not values:
        raise RuntimeError("PMTiles sin teselas direccionables")
    if not 0 < percentile <= 1:
        raise ValueError(f"Percentil inválido: {percentile}")
    return values[ceil(percentile * len(values)) - 1]


def validate_tile_budget(path: Path, report: Path) -> dict[str, int]:
    """Measure stored tile payloads before a private result can be persisted."""
    from pmtiles.reader import MmapSource, all_tiles

    with path.open("rb") as handle:
        sizes = sorted(len(payload) for _, payload in all_tiles(MmapSource(handle)))
    summary = {
        "tile_count": len(sizes),
        "p50_bytes": nearest_rank(sizes, 0.50),
        "p95_bytes": nearest_rank(sizes, 0.95),
        "max_bytes": sizes[-1],
    }
    if (
        summary["p50_bytes"] >= TILE_BUDGET_BYTES["p50"]
        or summary["p95_bytes"] >= TILE_BUDGET_BYTES["p95"]
        or summary["max_bytes"] >= TILE_BUDGET_BYTES["max"]
    ):
        raise RuntimeError(
            f"{path.name}: excede presupuesto de teselas "
            f"(p50={summary['p50_bytes']}, p95={summary['p95_bytes']}, max={summary['max_bytes']})"
        )
    report.parent.mkdir(parents=True, exist_ok=True)
    report.write_text(
        json.dumps({"budget_bytes": TILE_BUDGET_BYTES, **summary}, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def build_communes(
    boundaries_path: Path,
    code_field: str,
    metrics_path: Path,
    output_dir: Path,
    version: str,
    excluded_commune_codes: set[str],
) -> BuildResult:
    boundaries = gpd.read_file(boundaries_path)
    if code_field not in boundaries.columns:
        raise RuntimeError(f"La capa comunal no contiene la columna de código {code_field!r}")
    ensure_valid_geometries(boundaries, "capa comunal")
    metrics = pd.read_json(metrics_path)
    if "codigo_comuna" not in metrics.columns or len(metrics) != 346:
        raise RuntimeError("Las métricas comunales deben tener codigo_comuna y exactamente 346 filas")
    metrics = metrics.copy()
    metrics["cod_comuna"] = metrics["codigo_comuna"].map(canonical_code)
    if metrics["cod_comuna"].duplicated().any():
        raise RuntimeError("Métricas comunales con código duplicado")
    boundaries = boundaries.copy()
    boundaries["cod_comuna"] = boundaries[code_field].map(canonical_code)
    boundary_codes = set(boundaries["cod_comuna"])
    metric_codes = set(metrics["cod_comuna"])
    missing_metrics_geometry = metric_codes - boundary_codes
    missing_boundary_metrics = boundary_codes - metric_codes
    if missing_boundary_metrics:
        raise RuntimeError(f"Límites comunales sin métricas: {sorted(missing_boundary_metrics)}")
    if missing_metrics_geometry != excluded_commune_codes:
        raise RuntimeError(
            "La diferencia entre métricas y DPA debe coincidir exactamente con las exclusiones declaradas: "
            f"observada={sorted(missing_metrics_geometry)} declarada={sorted(excluded_commune_codes)}"
        )
    if len(boundaries) + len(missing_metrics_geometry) != len(metrics):
        raise RuntimeError("Conteo comunal inconsistente entre DPA y métricas")
    public_metrics = metrics.loc[:, [
        "cod_comuna", "comuna", "region", "poblacion_censo_2024", "predios_habitacionales",
        "cobertura_censo_pct", "brecha_equivalente_censo", "cobertura_coordenadas_pct",
    ]]
    output = boundaries.loc[:, ["cod_comuna", "geometry"]].merge(public_metrics, on="cod_comuna", how="left", validate="one_to_one")
    output["cod_region"] = output["cod_comuna"].str.slice(0, 2)
    output["version_datos"] = version
    missing_metrics = int(output["comuna"].isna().sum())
    if missing_metrics:
        raise RuntimeError(f"{missing_metrics} límites comunales no pudieron cruzarse con métricas")
    communal = gpd.GeoDataFrame(output, geometry="geometry", crs=boundaries.crs).to_crs(4326)
    ensure_valid_geometries(communal, "capa comunal pública")
    fgb = output_dir / "interim" / f"chile_comunas_brechas_{version}.fgb"
    write_fgb(communal, fgb, "comunas")
    pmtiles = output_dir / f"chile_comunas_brechas_{version}.pmtiles"
    fields = [column for column in communal.columns if column != "geometry"]
    tippecanoe(fgb, pmtiles, "comunas", 4, 12, fields)
    validate_pmtiles(pmtiles, "comunas", output_dir / "reports" / f"communes_{version}_pmtiles_show.txt")
    tile_budget = validate_tile_budget(pmtiles, output_dir / "reports" / f"communes_{version}_tile_budget.json")
    territories_path = output_dir / f"territories_{version}.json"
    territories = {
        "schema_version": 1,
        "communes": {
            row.cod_comuna: {"bounds": [round(float(value), 7) for value in row.geometry.bounds]}
            for row in communal.itertuples(index=False)
        },
    }
    territories_path.write_text(json.dumps(territories, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return BuildResult(
        pmtiles, "comunas", 4, 12, len(communal), pmtiles.stat().st_size,
        {boundaries_path.name: sha256(boundaries_path)}, territories_path.name,
        {"excluded_communes": sorted(missing_metrics_geometry), "tile_budget": tile_budget},
    )


def build_atacama_pilot(source_dir: Path, output_dir: Path, version: str) -> BuildResult:
    parts: list[gpd.GeoDataFrame] = []
    fingerprints: dict[str, str] = {}
    geometry_exclusions: dict[str, dict[str, int]] = {}
    for commune_code, filename in PILOT_SOURCES.items():
        source = source_dir / filename
        if not source.is_file():
            raise FileNotFoundError(f"Fuente piloto ausente: {source}")
        raw = gpd.read_parquet(source, columns=["dc_cod_destino", "geometry"])
        residential, counts = select_public_residential_geometries(raw, filename)
        public = public_parcel_frame(residential, commune_code, version, raw.crs)
        ensure_public_parcel_schema(public)
        parts.append(public)
        fingerprints[filename] = sha256(source)
        geometry_exclusions[filename] = counts
    combined = gpd.GeoDataFrame(pd.concat(parts, ignore_index=True), geometry="geometry", crs=4326)
    ensure_valid_geometries(combined, "piloto Atacama")
    ensure_public_parcel_schema(combined)
    fgb = output_dir / "interim" / f"predios_region_03_{version}.fgb"
    write_fgb(combined, fgb, "predios")
    pmtiles = output_dir / f"predios_region_03_{version}.pmtiles"
    tippecanoe(fgb, pmtiles, "predios", 13, 18, sorted(PUBLIC_PARCEL_FIELDS - {"geometry"}))
    validate_pmtiles(pmtiles, "predios", output_dir / "reports" / f"atacama_{version}_pmtiles_show.txt")
    tile_budget = validate_tile_budget(pmtiles, output_dir / "reports" / f"atacama_{version}_tile_budget.json")
    return BuildResult(
        pmtiles, "predios", 13, 18, len(combined), pmtiles.stat().st_size,
        fingerprints, metadata={
            "source_geometry_exclusions": geometry_exclusions,
            "tile_budget": tile_budget,
        },
    )


def result_dict(result: BuildResult, *, available: bool, pilot: bool = False, communes: list[str] | None = None) -> dict[str, Any]:
    return {
        "available": available,
        "pilot": pilot,
        "url": result.path.name,
        "source_layer": result.layer,
        "minzoom": result.minzoom,
        "maxzoom": result.maxzoom,
        "feature_count": result.feature_count,
        "bytes": result.bytes_written,
        "source_sha256": result.source_sha256,
        "communes": communes or [],
        **({"territories_file": result.territories_file} if result.territories_file else {}),
        **result.metadata,
    }


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument("--output-dir", type=Path, required=True)
    command.add_argument("--version", default=datetime.now(UTC).strftime("%Y%m%d"))
    command.add_argument("--tiles-base", default=os.environ.get("PUBLIC_TILES_BASE", "https://tiles.3cucharadas.cl/catastro-sii"))
    command.add_argument("--legal-status", default=os.environ.get("LEGAL_PUBLICATION_STATUS", "PENDING"))
    command.add_argument("--publishable", action="store_true", help="Marca el piloto predial apto para upload; exige autorización vectorial.")
    command.add_argument("--build-communes", action="store_true")
    command.add_argument("--comunas-source", type=Path)
    command.add_argument("--comunas-code-field", default=os.environ.get("COMUNAS_SOURCE_CODE_FIELD", "cod_comuna"))
    command.add_argument("--metrics-source", type=Path)
    command.add_argument("--build-atacama-pilot", action="store_true")
    command.add_argument("--predios-source-dir", type=Path)
    command.add_argument(
        "--excluded-commune-code", action="append", default=[],
        help="Código comunal presente en métricas pero sin geometría DPA autorizada; debe declararse explícitamente.",
    )
    return command


def main() -> int:
    args = parser().parse_args()
    legal = args.legal_status.upper()
    if legal not in LEGAL_VALUES:
        raise RuntimeError(f"LEGAL_PUBLICATION_STATUS inválido: {legal}")
    if args.publishable and legal != "AUTHORIZED_VECTOR":
        raise RuntimeError("La publicación vectorial exige LEGAL_PUBLICATION_STATUS=AUTHORIZED_VECTOR")
    if not args.build_communes and not args.build_atacama_pilot:
        raise RuntimeError("Indica --build-communes, --build-atacama-pilot o ambos")
    require_programs("tippecanoe", "pmtiles-show")
    if args.build_communes and (args.comunas_source is None or args.metrics_source is None):
        raise RuntimeError("La capa comunal requiere --comunas-source y --metrics-source")
    if args.build_atacama_pilot and args.predios_source_dir is None:
        raise RuntimeError("El piloto requiere --predios-source-dir")

    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, Any] = {}
    if args.build_communes:
        excluded = {canonical_code(code) for code in args.excluded_commune_code}
        communal = build_communes(
            args.comunas_source.resolve(), args.comunas_code_field, args.metrics_source.resolve(),
            output_dir, args.version, excluded,
        )
        results["communes"] = result_dict(communal, available=True)
    if args.build_atacama_pilot:
        pilot = build_atacama_pilot(args.predios_source_dir.resolve(), output_dir, args.version)
        results["parcel_regions"] = {"03": result_dict(pilot, available=args.publishable, pilot=True, communes=sorted(PILOT_SOURCES))}

    manifest = {
        "schema_version": 1,
        "generated_at": datetime.now(UTC).isoformat(),
        "legal_publication_status": legal,
        "tiles_base": args.tiles_base.rstrip("/"),
        "build_scope": "publishable" if args.publishable else "private-validation",
        "source_geometry": "Canonical GeoParquet was read-only; null/empty geometries are counted and excluded only from the derivative, while invalid geometries are rejected and never repaired in place.",
        "results": results,
    }
    (output_dir / f"tiles_manifest_{args.version}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (RuntimeError, subprocess.CalledProcessError, FileNotFoundError, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        raise SystemExit(1)
