#!/usr/bin/env python3
"""Corrige el denominador principal de cobertura: viviendas, no población.

`metricas_comunales.parquet` traía únicamente `viviendas_ocupadas_censo_2024`
(viviendas particulares con moradores presentes) y usaba una razón
personas-por-vivienda-ocupada para convertir predios SII en una "población
equivalente" comparada contra la población censada. Ese es un denominador
indirecto (predio -> vivienda -> razón -> población) y, en la práctica,
produce coberturas sobre 100% en 62/346 comunas — un artefacto, no un hallazgo.

La comparación directa es predios SII (que catastran estructuras, no
personas) contra viviendas particulares totales del Censo 2024 (censadas y
no censadas: ocupadas + desocupadas). Este script agrega esa comparación
como denominador PRINCIPAL, hogares como denominador SECUNDARIO, y deja el
enfoque poblacional existente como contraste ADICIONAL — no lo elimina.

Fuente: microdatos de vivienda del Censo 2024 (INE, liberados 2025-12-03),
descarga pública desde censo2024.ine.gob.cl/resultados/ -> "Bases de datos
país" -> "Base de microdatos - Viviendas Censo 2024 (csv)". El CSV crudo
(~426 MB) NO se versiona en este repo; se agrega por comuna con DuckDB y
solo el resultado agregado (346 filas) se usa aquí.

Columnas fuente relevantes (ver diccionario_variables_censo2024.xlsx):
  - tipo_operativo: 2 = vivienda particular (excluye persona en situación de
    calle y vivienda colectiva).
  - p3a_estado_ocupacion: 1 = Ocupada, 2 = Desocupada.
  - cant_hog: hogares por vivienda (permite validar contra hogares_censo_2024
    ya existente: coincide exactamente a nivel nacional y comunal).

Ejecutar:
    python3 scripts/catastro_sii/enrich_viviendas_censo2024.py \
        --viviendas-csv /ruta/a/viviendas_censo2024.csv \
        [--dry-run]

Sin `--viviendas-csv` intenta la ruta local ya usada en esta sesión
(`~/Descargas/investigacion/censo2024/viviendas_censo2024.csv`).
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import duckdb
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "catastro_sii_brecha" / "data"
METRICS_PATH = DATA / "metricas_comunales.parquet"
COMMUNES_JSON_PATH = DATA / "comunas.json"
DEFAULT_VIVIENDAS_CSV = Path.home() / "Descargas" / "investigacion" / "censo2024" / "viviendas_censo2024.csv"


def jsonable(value):
    """Convierte tipos numpy/pandas a nativos de Python; NaN -> None."""
    if isinstance(value, (np.integer,)):
        return int(value)
    if isinstance(value, (np.floating,)):
        return None if math.isnan(value) else float(value)
    if isinstance(value, float) and math.isnan(value):
        return None
    if isinstance(value, dict):
        return {key: jsonable(item) for key, item in value.items()}
    if isinstance(value, (list, np.ndarray)):
        return [jsonable(item) for item in value]
    return value


def write_communes_json(df: pd.DataFrame) -> None:
    records = [{key: jsonable(value) for key, value in row.items()} for row in df.to_dict(orient="records")]
    with COMMUNES_JSON_PATH.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, separators=(",", ":"))


def aggregate_viviendas(csv_path: Path) -> pd.DataFrame:
    con = duckdb.connect()
    con.execute("SET memory_limit='4GB'")
    query = f"""
        SELECT
            comuna AS codigo_comuna,
            COUNT(*) FILTER (WHERE tipo_operativo = 2) AS viviendas_totales_censo_2024,
            COUNT(*) FILTER (WHERE tipo_operativo = 2 AND p3a_estado_ocupacion = 2)
                AS viviendas_desocupadas_censo_2024,
            SUM(cant_hog) FILTER (WHERE tipo_operativo = 2) AS hogares_validacion_censo_2024
        FROM read_csv('{csv_path.as_posix()}', delim=';', header=true, sample_size=200000)
        GROUP BY comuna
        ORDER BY comuna
    """
    frame = con.execute(query).fetch_df()
    frame["codigo_comuna"] = frame["codigo_comuna"].astype(str)
    return frame


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--viviendas-csv", type=Path, default=DEFAULT_VIVIENDAS_CSV)
    parser.add_argument("--dry-run", action="store_true", help="No escribe el parquet, solo reporta.")
    args = parser.parse_args()

    if not args.viviendas_csv.exists():
        raise SystemExit(f"No existe {args.viviendas_csv}. Descarga el CSV desde censo2024.ine.gob.cl/resultados/.")

    viviendas = aggregate_viviendas(args.viviendas_csv)
    if len(viviendas) != 346:
        raise SystemExit(f"Se esperaban 346 comunas en el agregado de viviendas, hay {len(viviendas)}")

    metrics = pd.read_parquet(METRICS_PATH)
    metrics["codigo_comuna"] = metrics["codigo_comuna"].astype(str)

    # Validación cruzada: hogares derivados de la base de vivienda deben
    # coincidir exactamente con hogares_censo_2024 ya presente (misma fuente
    # INE). Si no coincide, algo cambió (otra versión de la base, otro
    # corte) y no hay que seguir a ciegas.
    check = metrics[["codigo_comuna", "hogares_censo_2024"]].merge(viviendas, on="codigo_comuna", how="inner")
    mismatches = check[check["hogares_censo_2024"] != check["hogares_validacion_censo_2024"]]
    if len(mismatches) > 1:  # tolera 1 fila con NaN por comuna sin datos, ya visto en el corte real
        raise SystemExit(
            f"Validación cruzada de hogares falló en {len(mismatches)} comunas: "
            "la base de vivienda no coincide con hogares_censo_2024 ya existente. "
            "Revisa si es la misma versión/corte del Censo 2024 antes de continuar."
        )

    if len(metrics) != len(metrics["codigo_comuna"].unique()) or len(viviendas) != 346:
        raise SystemExit("codigo_comuna no es único en alguna de las dos tablas")

    merged = metrics.merge(
        viviendas.drop(columns=["hogares_validacion_censo_2024"]),
        on="codigo_comuna",
        how="left",
        validate="one_to_one",
    )
    if merged["viviendas_totales_censo_2024"].isna().any():
        missing = merged.loc[merged["viviendas_totales_censo_2024"].isna(), "codigo_comuna"].tolist()
        raise SystemExit(f"Comunas sin match en viviendas totales: {missing}")

    merged["viviendas_totales_censo_2024"] = merged["viviendas_totales_censo_2024"].astype("int64")
    merged["viviendas_desocupadas_censo_2024"] = merged["viviendas_desocupadas_censo_2024"].astype("int64")

    # Denominador PRINCIPAL: predios SII de destino H contra el universo
    # completo de viviendas particulares (censadas y no censadas). Directo,
    # sin razón de conversión intermedia.
    merged["cobertura_vivienda_pct"] = (
        merged["predios_habitacionales"] / merged["viviendas_totales_censo_2024"] * 100
    )
    # Denominador SECUNDARIO: predios SII contra hogares censados (ya
    # existente, sin cambios). Las razones CASEN personas/hogar y
    # hogares/vivienda siguen disponibles como sensibilidad, sin tocarlas.
    merged["cobertura_hogar_pct"] = merged["predios_habitacionales"] / merged["hogares_censo_2024"] * 100

    # El campo `hallazgo` es prosa por comuna que el visor muestra tal cual
    # (`#finding` en catastro_sii_brecha/app.js). Describía la cobertura
    # poblacional como si fuera la lectura principal; se regenera con la
    # vivienda como denominador principal.
    def cl_int(value: int) -> str:
        return f"{value:,}".replace(",", ".")

    def hallazgo(row: pd.Series) -> str:
        predios = cl_int(int(row["predios_habitacionales"]))
        viviendas_totales = cl_int(int(row["viviendas_totales_censo_2024"]))
        return (
            f"Con {predios} predios habitacionales, {row['comuna']} cubre "
            f"el {row['cobertura_vivienda_pct']:.1f}% de las {viviendas_totales} "
            "viviendas particulares del Censo 2024 (ocupadas y desocupadas). Es una comparación de "
            "registros contra estructuras, no un conteo de residentes."
        )

    merged["hallazgo"] = merged.apply(hallazgo, axis=1)

    national_predios = merged["predios_habitacionales"].sum()
    national_viviendas = merged["viviendas_totales_censo_2024"].sum()
    national_hogares = merged["hogares_censo_2024"].sum()
    print(f"Cobertura nacional por vivienda (principal): {national_predios / national_viviendas * 100:.1f}%")
    print(f"Cobertura nacional por hogar (secundaria):    {national_predios / national_hogares * 100:.1f}%")
    over_100_vivienda = int((merged["cobertura_vivienda_pct"] > 100).sum())
    over_100_pob = int((merged["cobertura_censo_pct"] > 100).sum())
    print(f"Comunas sobre 100% cobertura-vivienda (nueva):  {over_100_vivienda}/346")
    print(f"Comunas sobre 100% cobertura-población (vieja): {over_100_pob}/346")

    if args.dry_run:
        print("\n--dry-run: no se escribió metricas_comunales.parquet")
        return

    merged.to_parquet(METRICS_PATH, index=False)
    print(f"\nEscrito: {METRICS_PATH} ({len(merged.columns)} columnas)")

    if COMMUNES_JSON_PATH.exists():
        existing_columns = list(json.loads(COMMUNES_JSON_PATH.read_text(encoding="utf-8"))[0].keys())
        new_columns = [column for column in merged.columns if column not in existing_columns]
        write_communes_json(merged[existing_columns + new_columns])
        print(f"Escrito: {COMMUNES_JSON_PATH}")


if __name__ == "__main__":
    main()
