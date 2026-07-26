#!/usr/bin/env python3
"""Agregados territoriales livianos para el visor Catastro SII.

Produce ``catastro_sii_brecha/data/agregados_territoriales.json`` a partir de
los shards UV publicados y de las métricas comunales agregadas. No escribe ni
expone registros prediales individuales ni geometrías.

Convención: medianas y cuartiles se calculan sobre UV con ``avm2 > 0``, sin
ponderar por superficie, hogares ni población.
"""
from __future__ import annotations

import argparse
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "catastro_sii_brecha" / "data"
UV_DIR = DATA / "uv"
COMMUNES_JSON = DATA / "comunas.json"
EXPLORER_JSON = DATA / "explorador_comunal.json"
INSIGHTS_JSON = DATA / "insights-v1.json"
OUTPUT = DATA / "agregados_territoriales.json"

SCHEMA_VERSION = 1
UNUSABLE_UV_FEATURES = [
    {"uv_rsh": 43018092, "codigo_comuna": "04301", "comuna": "Ovalle", "region": "Coquimbo"},
    {"uv_rsh": 101054603, "codigo_comuna": "10105", "comuna": "Frutillar", "region": "Los Lagos"},
    {"uv_rsh": 162037323, "codigo_comuna": "16203", "comuna": "Coelemu", "region": "Ñuble"},
]


def input_files() -> list[Path]:
    return [COMMUNES_JSON, EXPLORER_JSON, INSIGHTS_JSON, *sorted(UV_DIR.glob("*.json"))]


def generated_at_from_inputs() -> str:
    latest = max(path.stat().st_mtime for path in input_files())
    return datetime.fromtimestamp(latest, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def data_code(value: Any) -> str:
    text = str(value).strip()
    if not text.isdigit():
        raise ValueError(f"codigo comunal invalido: {value!r}")
    return text[1:] if len(text) == 5 and text.startswith("0") else text


def shared_code(value: Any) -> str:
    return data_code(value).zfill(5)


def finite_number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)) and value == value and value not in (float("inf"), float("-inf")):
        return float(value)
    return None


def quantile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    ordered = sorted(values)
    if len(ordered) == 1:
        return round(ordered[0], 2)
    position = q * (len(ordered) - 1)
    low = int(position)
    high = min(low + 1, len(ordered) - 1)
    weight = position - low
    return round(ordered[low] * (1 - weight) + ordered[high] * weight, 2)


def describe(values: list[float]) -> dict[str, float | int | None]:
    return {
        "n_uv_validas": len(values),
        "avm2_mediana": quantile(values, 0.5),
        "avm2_p25": quantile(values, 0.25),
        "avm2_p75": quantile(values, 0.75),
        "avm2_p90": quantile(values, 0.90),
        "avm2_min": round(min(values), 2) if values else None,
        "avm2_max": round(max(values), 2) if values else None,
    }


def quartile_of(value: float | None, cuts: list[float]) -> int | None:
    if value is None:
        return None
    if value <= cuts[0]:
        return 1
    if value <= cuts[1]:
        return 2
    if value <= cuts[2]:
        return 3
    return 4


def explorer_series() -> dict[str, dict[str, float | None]]:
    payload = json.loads(EXPLORER_JSON.read_text(encoding="utf-8"))
    codes = payload["codigo"]
    series = payload["series"]
    wanted = {
        "avaluo_total_mmm",
        "superficie_km2",
        "predios",
        "hogares",
        "poblacion_censo",
        "pct_urbano",
        "vulnerabilidad_media",
        "p90_p50",
        "gini_avaluo",
    }
    rows: dict[str, dict[str, float | None]] = {}
    for index, code in enumerate(codes):
        rows[shared_code(code)] = {
            key: finite_number(values[index])
            for key, values in series.items()
            if key in wanted
        }
    return rows


def insights_uv_universe() -> int:
    payload = json.loads(INSIGHTS_JSON.read_text(encoding="utf-8"))
    value = payload.get("universe", {}).get("uv")
    if not isinstance(value, int):
        raise ValueError("insights-v1.json no declara universe.uv entero")
    return value


def uv_rows(code: str) -> list[dict[str, float]]:
    shard = UV_DIR / f"{data_code(code)}.json"
    if not shard.exists():
        shard = UV_DIR / f"{shared_code(code)}.json"
    payload = json.loads(shard.read_text(encoding="utf-8")) if shard.exists() else {"features": []}
    rows: list[dict[str, float]] = []
    for feature in payload.get("features", []):
        props = (feature or {}).get("properties") or {}
        avm2 = finite_number(props.get("avm2"))
        row = {
            "avm2": avm2,
            "av": finite_number(props.get("av")) or 0.0,
            "hog": finite_number(props.get("hog")) or 0.0,
            "pob": finite_number(props.get("pob")) or 0.0,
            "urb": finite_number(props.get("urb")) or 0.0,
        }
        rows.append(row)
    return rows


def aggregate() -> dict[str, Any]:
    communes = json.loads(COMMUNES_JSON.read_text(encoding="utf-8"))
    explorer = explorer_series()

    commune_values: dict[str, list[float]] = {}
    commune_extra: dict[str, dict[str, float | int | None]] = {}
    region_values: dict[str, list[float]] = {}
    region_communes: dict[str, list[str]] = {}
    all_values: list[float] = []

    for row in communes:
        code = shared_code(row["codigo_comuna"])
        region = str(row["region"])
        uv = uv_rows(code)
        valid = [item["avm2"] for item in uv if item["avm2"] is not None and item["avm2"] > 0]
        commune_values[code] = valid
        if valid:
            region_values.setdefault(region, []).extend(valid)
            all_values.extend(valid)
        region_communes.setdefault(region, []).append(code)
        explorer_row = explorer.get(code, {})
        avaluo_total = explorer_row.get("avaluo_total_mmm")
        superficie = explorer_row.get("superficie_km2")
        commune_extra[code] = {
            "n_uv": len(uv),
            "avaluo_total_clp": round(avaluo_total * 1_000_000_000, 2) if avaluo_total is not None else None,
            "superficie_total_m2": round(superficie * 1_000_000, 2) if superficie is not None else None,
            "predios_enrolados": round(explorer_row["predios"], 2) if explorer_row.get("predios") is not None else None,
            "hogares_rsh": round(explorer_row["hogares"], 2) if explorer_row.get("hogares") is not None else None,
            "poblacion_censo": round(explorer_row["poblacion_censo"], 2) if explorer_row.get("poblacion_censo") is not None else None,
            "pct_urbano": round(explorer_row["pct_urbano"], 2) if explorer_row.get("pct_urbano") is not None else None,
            "vulnerabilidad_media": round(explorer_row["vulnerabilidad_media"], 4) if explorer_row.get("vulnerabilidad_media") is not None else None,
            "p90_p50": round(explorer_row["p90_p50"], 4) if explorer_row.get("p90_p50") is not None else None,
            "gini_avaluo": round(explorer_row["gini_avaluo"], 4) if explorer_row.get("gini_avaluo") is not None else None,
        }

    commune_medians = {code: quantile(values, 0.5) for code, values in commune_values.items()}
    median_list = sorted(value for value in commune_medians.values() if value is not None)
    commune_cuts = [quantile(median_list, q) or 0.0 for q in (0.25, 0.5, 0.75)]
    region_medians = {region: quantile(values, 0.5) for region, values in region_values.items()}

    communes_out: dict[str, dict[str, Any]] = {}
    for row in communes:
        code = shared_code(row["codigo_comuna"])
        region = str(row["region"])
        median = commune_medians[code]
        region_median = region_medians.get(region)
        communes_out[code] = {
            "codigo_comuna": code,
            "codigo_comuna_dato": data_code(code),
            "comuna": row["comuna"],
            "region": region,
            **commune_extra[code],
            **describe(commune_values[code]),
            "cuartil_nacional_avm2": quartile_of(median, commune_cuts),
            "mediana_regional_avm2": region_median,
            "sobre_mediana_regional": bool(median > region_median) if median is not None and region_median is not None else None,
        }

    regions_out: dict[str, dict[str, Any]] = {}
    for region in sorted(region_communes):
        codes = region_communes[region]
        values = region_values.get(region, [])
        regions_out[region] = {
            "region": region,
            "n_comunas": len(codes),
            "n_comunas_con_avm2": sum(1 for code in codes if commune_medians[code] is not None),
            "n_uv": sum(int(commune_extra[code]["n_uv"] or 0) for code in codes),
            **describe(values),
            "avaluo_total_clp": round(sum(float(commune_extra[code]["avaluo_total_clp"] or 0) for code in codes), 2),
            "superficie_total_m2": round(sum(float(commune_extra[code]["superficie_total_m2"] or 0) for code in codes), 2),
            "predios_enrolados": round(sum(float(commune_extra[code]["predios_enrolados"] or 0) for code in codes), 2),
        }

    missing_codes = sorted(code for code, median in commune_medians.items() if median is None)
    published_uv = sum(int(item["n_uv"] or 0) for item in commune_extra.values())
    insights_uv = insights_uv_universe()
    return {
        "schema_version": SCHEMA_VERSION,
        "generated_at": generated_at_from_inputs(),
        "method": {
            "unidad": "unidad vecinal (UV)",
            "fuente_etiquetas": "catastro_sii_brecha/data/comunas.json",
            "fuente_series": "catastro_sii_brecha/data/explorador_comunal.json",
            "mediana": "mediana de avm2 sobre UV con avm2 > 0, sin ponderar",
            "cuartiles_comunales": "cuartiles nacionales calculados sobre la mediana comunal de avm2",
            "corte_bivariado": "avm2 de la UV comparado contra la mediana de su región",
            "moneda": "CLP por m2, valor directo",
        },
        "technical_notes": {
            "uv_universe_reconciliation": {
                "insights_v1_uv": insights_uv,
                "published_uv_features": published_uv,
                "difference": insights_uv - published_uv,
                "reason": "insights-v1 usa el universo tabular uv_avaluo.parquet; el visor usa shards GeoJSON navegables y excluye UV cuya geometría fue marcada como no usable por el generador cartográfico.",
                "not_navigable_uv": UNUSABLE_UV_FEATURES,
            }
        },
        "national": {
            "n_comunas": len(communes_out),
            "n_regiones": len(regions_out),
            "n_uv": published_uv,
            "n_comunas_con_avm2": len(communes_out) - len(missing_codes),
            "comunas_sin_avm2": missing_codes,
            **describe(all_values),
            "cortes_cuartil_comunal": commune_cuts,
            "avaluo_total_clp": round(sum(float(item["avaluo_total_clp"] or 0) for item in commune_extra.values()), 2),
            "superficie_total_m2": round(sum(float(item["superficie_total_m2"] or 0) for item in commune_extra.values()), 2),
            "predios_enrolados": round(sum(float(item["predios_enrolados"] or 0) for item in commune_extra.values()), 2),
        },
        "regions": regions_out,
        "communes": communes_out,
    }


def assert_contract(payload: dict[str, Any]) -> None:
    forbidden = {"predio", "pred_uid", "rol", "rut", "run", "direccion", "geometry", "coordinates", "avaluo_fiscal_clp"}
    rendered = json.dumps(payload, ensure_ascii=False)
    for key in forbidden:
        if f'"{key}"' in rendered:
            raise AssertionError(f"campo individual prohibido en salida: {key}")
    national = payload["national"]
    if national["n_comunas"] != 346:
        raise AssertionError(f"se esperaban 346 comunas, no {national['n_comunas']}")
    if national["n_regiones"] != 16:
        raise AssertionError(f"se esperaban 16 regiones, no {national['n_regiones']}")
    if national["n_comunas_con_avm2"] != 340:
        raise AssertionError(f"se esperaban 340 comunas con avm2, no {national['n_comunas_con_avm2']}")
    if len(national["comunas_sin_avm2"]) != 6:
        raise AssertionError("se esperaban seis comunas preservadas sin avm2 positivo")
    note = payload["technical_notes"]["uv_universe_reconciliation"]
    if note["difference"] != len(UNUSABLE_UV_FEATURES):
        raise AssertionError(
            "la diferencia entre insights-v1 y shards UV publicados ya no coincide "
            "con las UV no navegables documentadas"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="no escribe; sólo informa")
    args = parser.parse_args()

    payload = aggregate()
    assert_contract(payload)
    rendered = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    national = payload["national"]
    print(
        f"comunas: {national['n_comunas']} · regiones: {national['n_regiones']} · "
        f"comunas con avm2: {national['n_comunas_con_avm2']}"
    )
    print(
        f"UV: {national['n_uv']} · UV con avm2: {national['n_uv_validas']} · "
        f"mediana nacional: ${national['avm2_mediana']:,.0f}/m2"
    )
    print(f"comunas sin avm2 positivo: {', '.join(national['comunas_sin_avm2'])}")

    if args.check:
        previous = OUTPUT.read_text(encoding="utf-8") if OUTPUT.exists() else ""
        print("sin cambios" if previous == rendered else "CAMBIA (ejecuta sin --check)")
        return 0

    OUTPUT.write_text(rendered, encoding="utf-8")
    print(f"escrito: {OUTPUT.relative_to(ROOT)} ({len(rendered) / 1024:.1f} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
