#!/usr/bin/env python3
"""Project reviewed SII/CASEN aggregates into the removable Avalúos II extension.

The projector never copies source microdata or internal paths.  It validates the
aggregate files against their provenance, publishes only commune/national tables,
and renders the two bilingual includes used by the existing posts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any, Iterable


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_SII_DIR = ROOT.parent / "catastros_sii/v5_brecha/artifacts/avaluos_ii_extension"
DEFAULT_OUTPUT_DIR = ROOT / "assets/data/avaluos-ii-extension"
DEFAULT_INCLUDE_DIR = ROOT / "_includes"

SII_COLUMNS = (
    "series",
    "territory_code",
    "roles",
    "primary_h",
    "positive_h_line_roles",
    "non_h_with_h_line",
    "excluded_common",
    "excluded_matrix",
    "unresolved",
    "eligible_non_h_h",
    "agricultural_p_only",
    "primary_h_without_positive_h_line",
)
SII_DESTINATION_COLUMNS = ("series", "territory_code", "destination", "roles")
CASEN_SOURCE_COLUMNS = (
    "scope",
    "territory_code",
    "name",
    "household_share",
    "weighted_households_shared",
    "weighted_households_shared_se",
    "weighted_households_shared_ci95_low",
    "weighted_households_shared_ci95_high",
    "household_total_ci_status",
    "weighted_persons_shared",
    "weighted_persons_shared_se",
    "weighted_persons_shared_ci95_low",
    "weighted_persons_shared_ci95_high",
    "person_total_ci_status",
    "n_households_sample",
    "n_shared_households_sample",
    "n_shared_persons_sample",
    "no_sample",
)
CASEN_PUBLIC_COLUMNS = (
    "scope",
    "territory_code",
    "territory_name",
    "weight",
    "expanded_households",
    "expanded_residents",
    "sample_households",
    "sample_residents",
)
SII_CASES = (("CL", "Chile"), ("5101", "Valparaíso"), ("10101", "Puerto Montt"))
CASEN_CASES = (("CL", "Chile"), ("5101", "Valparaíso"), ("5109", "Viña del Mar"))
EXPANDED_COMPARISON_COLUMNS = (
    "scope", "territory_code", "name", "region", "fiscal_source_available", "direct_source_available",
    "census_private_dwellings_2024", "fiscal_baseline_primary_h_roles_2026s1", "direct_primary_h_roles_2026s1",
    "direct_vs_fiscal_primary_h_change", "eligible_nonprincipal_residential_roles_2026s1",
    "expanded_residential_roles_2026s1", "signed_difference_before_expansion", "positive_difference_before_expansion",
    "signed_difference_after_expansion", "positive_difference_after_expansion", "signed_difference_reduction",
    "positive_difference_reduction",
)
EXPANDED_SUMMARY_COLUMNS = (
    "scope", "territory_code", "name", "communes_total", "fiscal_source_communes_observed",
    "direct_source_communes_observed", "direct_source_communes_missing", "census_private_dwellings_full_universe_2024",
    "census_private_dwellings_direct_coverage_2024", "fiscal_baseline_primary_h_roles_total",
    "direct_primary_h_roles_total", "source_total_change_including_coverage", "eligible_nonprincipal_residential_roles_total",
    "expanded_residential_roles_total", "net_signed_difference_before_expansion", "net_signed_difference_after_expansion",
    "net_signed_difference_reduction", "sum_positive_difference_before_expansion", "sum_positive_difference_after_expansion",
    "sum_positive_difference_reduction",
)
PUBLIC_FILES = (
    "sii-communes.csv",
    "sii-destination-breakdown.csv",
    "casen-quantities.csv",
    "expanded-comparison.csv",
    "expanded-national-summary.csv",
    "method.md",
    "audit.json",
    "provenance.json",
)
POSTS = (
    ROOT / "_posts/2026-09-11-avaluos-ii-brecha-residencial.md",
    ROOT / "_posts/2026-09-11-avaluos-ii-brecha-residencial-en.md",
)
PROTECTED_REFERENCE_PATTERN = re.compile(
    r"/(?:assets/images/avaluos-ii|catastro_sii_brecha)/[^\s\"'<>)]*"
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def front_matter(text: str) -> str:
    require(text.startswith("---\n"), "post lacks front matter")
    end = text.find("\n---\n", 4)
    require(end >= 0, "post front matter is not closed")
    return text[: end + 5]


def baseline_post(repo_ref: str, relative: str) -> str:
    result = subprocess.run(
        ["git", "show", f"{repo_ref}:{relative}"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def read_json(path: Path) -> dict[str, Any]:
    data = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(data, dict), f"{path.name}: expected a JSON object")
    return data


def read_csv_exact(path: Path, columns: tuple[str, ...]) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as source:
        reader = csv.DictReader(source)
        require(tuple(reader.fieldnames or ()) == columns, f"{path.name}: unexpected columns")
        rows = list(reader)
    require(bool(rows), f"{path.name}: empty aggregate")
    return rows


def nonnegative_integer(row: dict[str, str], field: str, label: str) -> int:
    raw = row[field]
    require(raw != "" and raw.isdigit(), f"{label}.{field}: expected a non-negative integer")
    return int(raw)


def check_bound_hash(provenance: dict[str, Any], path: Path) -> None:
    outputs = provenance.get("outputs_sha256")
    require(isinstance(outputs, dict), "provenance: outputs_sha256 is missing")
    require(outputs.get(path.name) == sha256(path), f"{path.name}: provenance hash mismatch")


def extract_urls(value: Any) -> list[str]:
    found: set[str] = set()

    def visit(item: Any) -> None:
        if isinstance(item, str) and item.startswith(("https://", "http://")):
            found.add(item)
        elif isinstance(item, dict):
            for nested in item.values():
                visit(nested)
        elif isinstance(item, list):
            for nested in item:
                visit(nested)

    visit(value)
    return sorted(found)


def validate_sii(source_dir: Path) -> dict[str, Any]:
    communes_path = source_dir / "sii-communes.csv"
    destinations_path = source_dir / "sii-destination-breakdown.csv"
    audit_path = source_dir / "sii-audit.json"
    provenance_path = source_dir / "sii-provenance.json"
    rows = read_csv_exact(communes_path, SII_COLUMNS)
    destination_rows = read_csv_exact(destinations_path, SII_DESTINATION_COLUMNS)
    audit = read_json(audit_path)
    provenance = read_json(provenance_path)

    for path in (communes_path, destinations_path, audit_path):
        check_bound_hash(provenance, path)
    require(provenance.get("raw_rows_exported") is False, "SII provenance must reject raw-row export")
    require(provenance.get("applied_to_original_gap") is False, "SII result must not alter the original gap")
    require(audit.get("source_unchanged") is True, "SII source changed during extraction")
    require(audit.get("role_keys_unique") is True, "SII role keys are not unique")
    require(audit.get("unit", "").startswith("administrative role"), "SII unit is not an administrative role")

    indexed: dict[tuple[str, str], dict[str, Any]] = {}
    totals: dict[str, dict[str, int]] = {"A": {}, "N": {}}
    numeric_fields = SII_COLUMNS[2:]
    for row in rows:
        series = row["series"]
        code = row["territory_code"]
        require(series in totals, f"SII: unexpected series {series!r}")
        require(code.isdigit(), f"SII: invalid territory code {code!r}")
        key = (series, code)
        require(key not in indexed, f"SII: duplicate aggregate {key}")
        parsed = {field: nonnegative_integer(row, field, f"SII[{series},{code}]") for field in numeric_fields}
        require(
            parsed["non_h_with_h_line"]
            == parsed["excluded_common"]
            + parsed["excluded_matrix"]
            + parsed["unresolved"]
            + parsed["eligible_non_h_h"],
            f"SII[{series},{code}]: exclusion identity failed",
        )
        require(
            parsed["positive_h_line_roles"]
            == parsed["primary_h"]
            - parsed["primary_h_without_positive_h_line"]
            + parsed["non_h_with_h_line"],
            f"SII[{series},{code}]: H-line identity failed",
        )
        indexed[key] = {"series": series, "territory_code": code, **parsed}
        for field, value in parsed.items():
            totals[series][field] = totals[series].get(field, 0) + value

    audited_totals = audit.get("totals_by_series")
    require(isinstance(audited_totals, dict), "SII audit: totals_by_series is missing")
    for series in ("A", "N"):
        require(totals[series] == audited_totals.get(series), f"SII {series}: commune totals disagree with audit")
    require(totals["A"]["primary_h"] == 0, "SII A: primary H must remain separate")
    require(totals["N"]["unresolved"] == 0, "SII N: unresolved candidate roles cannot be published")

    destination_totals: dict[tuple[str, str], int] = {}
    seen_destination_keys: set[tuple[str, str, str]] = set()
    for row in destination_rows:
        series, code, destination = row["series"], row["territory_code"], row["destination"]
        require(series in totals and code.isdigit(), "SII destination: invalid series or territory")
        require(destination not in {"", "H", "K"}, "SII destination: invalid eligible destination")
        destination_key = (series, code, destination)
        require(destination_key not in seen_destination_keys, f"SII destination: duplicate {destination_key}")
        seen_destination_keys.add(destination_key)
        destination_totals[(series, code)] = destination_totals.get((series, code), 0) + nonnegative_integer(
            row, "roles", f"SII destination[{series},{code},{destination}]"
        )
    for key, row in indexed.items():
        require(
            destination_totals.get(key, 0) == row["eligible_non_h_h"],
            f"SII destination: breakdown does not sum to eligible roles for {key}",
        )

    selected: list[dict[str, Any]] = []
    for code, name in SII_CASES:
        row = totals["N"] if code == "CL" else indexed.get(("N", code))
        require(row is not None, f"SII: missing selected territory {code}")
        selected.append({"territory_code": code, "territory_name": name, **row})

    return {
        "communes_path": communes_path,
        "destinations_path": destinations_path,
        "audit_path": audit_path,
        "provenance_path": provenance_path,
        "audit": audit,
        "provenance": provenance,
        "totals": totals,
        "selected": selected,
        "row_count": len(rows),
        "destination_row_count": len(destination_rows),
    }


def casen_hash_binding(provenance: dict[str, Any], path: Path) -> None:
    outputs = provenance.get("outputs_sha256")
    if isinstance(outputs, dict) and path.name in outputs:
        require(outputs[path.name] == sha256(path), f"{path.name}: CASEN provenance hash mismatch")
        return
    for key in ("source_csv_sha256", "aggregate_csv_sha256", "source_sha256"):
        if provenance.get(key) == sha256(path):
            return
    raise ValueError(f"{path.name}: CASEN provenance does not bind the aggregate")


def validate_expanded(source_dir: Path, sii: dict[str, Any]) -> dict[str, Any]:
    comparison_path = source_dir / "expanded-comparison.csv"
    summary_path = source_dir / "expanded-national-summary.csv"
    audit_path = source_dir / "expanded-audit.json"
    provenance_path = source_dir / "expanded-provenance.json"
    rows = read_csv_exact(comparison_path, EXPANDED_COMPARISON_COLUMNS)
    summaries = read_csv_exact(summary_path, EXPANDED_SUMMARY_COLUMNS)
    provenance = read_json(provenance_path)
    audit = read_json(audit_path)
    for path in (comparison_path, summary_path, audit_path):
        check_bound_hash(provenance, path)
    require(len(summaries) == 1 and summaries[0]["territory_code"] == "CL", "expanded summary: expected Chile row")
    indexed = {row["territory_code"]: row for row in rows}
    require(len(indexed) == len(rows), "expanded comparison: duplicate territory")
    selected = [summaries[0], indexed["5101"], indexed["10101"]]
    national = summaries[0]
    require(int(national["direct_primary_h_roles_total"]) == sii["totals"]["N"]["primary_h"], "expanded summary: direct H mismatch")
    require(int(national["eligible_nonprincipal_residential_roles_total"]) == sii["totals"]["N"]["eligible_non_h_h"], "expanded summary: eligible mismatch")
    require(int(national["expanded_residential_roles_total"]) == int(national["direct_primary_h_roles_total"]) + int(national["eligible_nonprincipal_residential_roles_total"]), "expanded summary: union identity failed")
    require(int(national["net_signed_difference_reduction"]) == int(national["eligible_nonprincipal_residential_roles_total"]), "expanded summary: net reduction identity failed")
    require(provenance.get("raw_rows_exported") is False, "expanded provenance must reject raw-row export")
    return {"comparison_path": comparison_path, "summary_path": summary_path, "audit_path": audit_path,
            "provenance_path": provenance_path, "provenance": provenance, "audit": audit, "selected": selected}


def validate_casen(source_dir: Path) -> dict[str, Any]:
    csv_path = source_dir / "casen-counts.csv"
    audit_path = source_dir / "casen-counts-audit.json"
    provenance_path = source_dir / "casen-counts-provenance.json"
    rows = read_csv_exact(csv_path, CASEN_SOURCE_COLUMNS)
    audit = read_json(audit_path)
    provenance = read_json(provenance_path)
    casen_hash_binding(provenance, csv_path)
    check_bound_hash(provenance, audit_path)
    require(provenance.get("raw_data_exported") is False, "CASEN provenance must reject raw-data export")
    require(provenance.get("sources_unchanged_after_run") is True, "CASEN sources changed during extraction")
    baseline = provenance.get("baseline", {})
    require(baseline.get("household_rates_preserved") is True, "CASEN household rates were not preserved")
    require(audit.get("privacy", {}).get("raw_observations_exported") is False, "CASEN audit reports raw observations")
    require(audit.get("privacy", {}).get("identifiers_exported") is False, "CASEN audit reports identifiers")
    require(audit.get("inference", {}).get("national_region_weight") == "expr", "CASEN national/regional weight changed")
    require(audit.get("inference", {}).get("commune_weight") == "expc", "CASEN commune weight changed")
    require(audit.get("inference", {}).get("communes") == "descriptive, nonrepresentative, no CI, no ranking", "CASEN commune interpretation changed")

    indexed: dict[str, dict[str, Any]] = {}
    for row in rows:
        code = row["territory_code"]
        require(code not in indexed, f"CASEN: duplicate territory {code}")
        require(row["scope"] in {"national", "region", "commune"}, f"CASEN[{code}]: invalid scope")
        indexed[code] = row

    expected_codes = {code for code, _ in CASEN_CASES}
    require(expected_codes.issubset(indexed), "CASEN: missing Chile, Valparaíso or Viña del Mar")
    coverage = audit.get("coverage", {})
    require(len(rows) == coverage.get("national", 0) + coverage.get("regions", 0) + coverage.get("commune_universe", 0), "CASEN: coverage disagrees with CSV")
    require(indexed["CL"]["scope"] == "national", "CASEN: Chile must use the national domain")
    for code in ("5101", "5109"):
        require(indexed[code]["scope"] == "commune", f"CASEN[{code}]: expected descriptive commune domain")

    expected_rates = {"CL": 0.01087822201092484, "5101": 0.09268113577023498, "5109": 0.0859948617877048}
    selected = []
    for code, default_name in CASEN_CASES:
        row = indexed[code]
        require(row["name"] != "", f"CASEN[{code}]: missing territory name")
        require(row["no_sample"] == "False", f"CASEN[{code}]: selected territory has no sample")
        require(abs(float(row["household_share"]) - expected_rates[code]) < 1e-12, f"CASEN[{code}]: published household rate changed")
        parsed = {
            "expanded_households": nonnegative_integer(row, "weighted_households_shared", f"CASEN[{code}]"),
            "expanded_residents": nonnegative_integer(row, "weighted_persons_shared", f"CASEN[{code}]"),
            "sample_households": nonnegative_integer(row, "n_shared_households_sample", f"CASEN[{code}]"),
            "sample_residents": nonnegative_integer(row, "n_shared_persons_sample", f"CASEN[{code}]"),
        }
        require(parsed["expanded_residents"] >= parsed["expanded_households"], f"CASEN[{code}]: residents must belong to selected households")
        require(parsed["sample_residents"] >= parsed["sample_households"], f"CASEN[{code}]: sample residents must belong to selected households")
        selected.append(
            {
                "scope": row["scope"],
                "territory_code": code,
                "territory_name": row["name"] or default_name,
                "weight": "expr" if row["scope"] in {"national", "region"} else "expc",
                **parsed,
            }
        )
    return {
        "csv_path": csv_path,
        "audit_path": audit_path,
        "provenance_path": provenance_path,
        "audit": audit,
        "provenance": provenance,
        "selected": selected,
        "row_count": len(rows),
    }


def number(value: int, lang: str) -> str:
    formatted = f"{value:,}"
    return formatted.replace(",", ".") if lang == "es" else formatted


def scroll_table(caption: str, headers: list[str], rows: Iterable[tuple[str, list[str]]]) -> str:
    lines = [
        '<div class="avaluos-ii-table" role="region" tabindex="0" style="max-width:100%;overflow-x:auto" '
        f'aria-label="{html.escape(caption, quote=True)}">',
        '<div style="width:max-content;min-width:100%">',
        f"<table><caption>{html.escape(caption)}</caption><thead><tr>"
        + "".join(f'<th scope="col">{html.escape(label)}</th>' for label in headers)
        + "</tr></thead><tbody>",
    ]
    for name, cells in rows:
        lines.append(
            f'<tr><th scope="row">{html.escape(name)}</th>'
            + "".join(f"<td>{html.escape(value)}</td>" for value in cells)
            + "</tr>"
        )
    lines.append("</tbody></table></div></div>")
    return "\n".join(lines)


def casen_table(rows: list[dict[str, Any]], lang: str) -> str:
    es = lang == "es"
    caption = (
        "Hogares con v9=3/4 y residentes en esos hogares; Chile usa expr y las comunas usan expc de forma descriptiva."
        if es
        else "Households with v9=3/4 and their residents; Chile uses expr and communes use expc descriptively."
    )
    headers = (
        ["Territorio", "Hogares expandidos (estimación)", "Residentes expandidos (estimación)", "Hogares muestrales del grupo", "Residentes muestrales del grupo"]
        if es
        else ["Territory", "Expanded households (estimate)", "Expanded residents (estimate)", "Selected sample households", "Selected sample residents"]
    )
    body = [
        (
            row["territory_name"],
            [
                number(row["expanded_households"], lang),
                number(row["expanded_residents"], lang),
                number(row["sample_households"], lang),
                number(row["sample_residents"], lang),
            ],
        )
        for row in rows
    ]
    return scroll_table(caption, headers, body)


def sii_table(rows: list[dict[str, Any]], lang: str) -> str:
    es = lang == "es"
    caption = (
        "Descarga SII 2026S1: roles no agrícolas y evidencia de líneas H; Valparaíso y Puerto Montt fueron elegidos antes de observar estos resultados."
        if es
        else "SII 2026H1 download: non-agricultural records and H-line evidence; Valparaíso and Puerto Montt were selected before these results were examined."
    )
    headers = (
        ["Ámbito", "Roles N", "Destino principal H", "No H con línea H", "Bien común o matriz", "Grupo elegible", "Principal H sin línea H válida"]
        if es
        else ["Area", "N records", "Primary use H", "Non-H with H line", "Common or parent record", "Eligible group", "Primary H without valid H line"]
    )
    body = []
    for row in rows:
        cells = [
            number(row["roles"], lang),
            number(row["primary_h"], lang),
            number(row["non_h_with_h_line"], lang),
            number(row["excluded_common"] + row["excluded_matrix"], lang),
            number(row["eligible_non_h_h"], lang),
            number(row["primary_h_without_positive_h_line"], lang),
        ]
        body.append((row["territory_name"], cells))
    return scroll_table(caption, headers, body)


def expanded_table(expanded: dict[str, Any], lang: str) -> str:
    es = lang == "es"
    headers = (["Ámbito", "Viviendas Censo", "H principal directo", "Extra no H", "Unión no agrícola", "Diferencia antes → después"]
               if es else ["Area", "Census dwellings", "Direct primary H", "Extra non-H", "Non-agricultural union", "Difference before → after"])
    body = []
    for row in expanded["selected"]:
        national = row["scope"] == "national"
        get = lambda national_key, commune_key: int(row[national_key if national else commune_key])
        cells = [
            number(get("census_private_dwellings_full_universe_2024", "census_private_dwellings_2024"), lang),
            number(get("direct_primary_h_roles_total", "direct_primary_h_roles_2026s1"), lang),
            number(get("eligible_nonprincipal_residential_roles_total", "eligible_nonprincipal_residential_roles_2026s1"), lang),
            number(get("expanded_residential_roles_total", "expanded_residential_roles_2026s1"), lang),
            f'{number(get("net_signed_difference_before_expansion", "signed_difference_before_expansion"), lang)} → {number(get("net_signed_difference_after_expansion", "signed_difference_after_expansion"), lang)}',
        ]
        body.append((row["name"], cells))
    caption = ("Comparación ampliada dentro de la serie no agrícola de la descarga directa; Chile es diferencia nacional neta."
               if es else "Expanded comparison within the direct download's non-agricultural series; Chile is the national net difference.")
    return scroll_table(caption, headers, body)


def render_include(sii: dict[str, Any], casen: dict[str, Any], expanded: dict[str, Any], lang: str) -> str:
    es = lang == "es"
    n = sii["totals"]["N"]
    a = sii["totals"]["A"]
    national = expanded["selected"][0]
    if es:
        parts = [
            "{% if include.section == 'casen' %}",
            "<h3>Cuántos hogares y residentes describe la señal CASEN</h3>",
            "<p>Las categorías 3 y 4 de <code>v9</code> se observan en la respuesta del hogar, tomada una sola vez desde el registro de su jefatura, pero las cantidades expandidas siguientes describen <strong>hogares completos y residentes de esos hogares</strong>. No cuentan personas que hayan declarado esa categoría de sitio de manera independiente. Chile usa <code>expr</code>; Valparaíso y Viña del Mar usan <code>expc</code> como descripciones comunales sin representatividad estadística.</p>",
            casen_table(casen["selected"], lang),
            '<p>La señal es compatible con varias viviendas en un sitio, pero CASEN no enlaza el sitio declarado con un rol SII. Por eso no demuestra que el SII sea incapaz de registrar esas construcciones. <a href="/assets/data/avaluos-ii-extension/casen-quantities.csv">Descargar las cantidades agregadas</a>. Se mantienen sin cambios el 1,09 % nacional, el 9,27 % de Valparaíso, el 8,60 % de Viña del Mar y los intervalos ya publicados.</p>',
            "{% else %}",
            "<p>La descarga nacional directa del SII permite mirar las líneas de construcción dentro de cada rol. Un rol cuyo destino principal es comercial u otro código puede contener una línea de destino H. Por eso, filtrar solo por destino principal H puede dejar fuera <strong>uso residencial registrado dentro de roles no H</strong>. Las líneas captan presencia de uso H, pero no cuántas viviendas censales representa: este cruce cuenta roles administrativos y no demuestra viviendas omitidas.</p>",
            expanded_table(expanded, lang),
            f'<p>En el total no agrícola, {number(n["non_h_with_h_line"], lang)} roles no H contienen al menos una línea H válida. Tras excluir {number(n["excluded_common"], lang)} bienes comunes y {number(n["excluded_matrix"], lang)} matrices referenciadas, quedan <strong>{number(n["eligible_non_h_h"], lang)} roles distintos</strong>. Como no se superponen con los {number(n["primary_h"], lang)} roles H del mismo archivo, su unión amplía el recuento no agrícola con evidencia residencial a <strong>{number(n["primary_h"] + n["eligible_non_h_h"], lang)}</strong> y reduce en {number(n["eligible_non_h_h"], lang)} la diferencia nacional aritmética frente al Censo. Esto no convierte cada rol en una vivienda ni equivale a sumar las brechas comunales positivas.</p>',
            f'<p>El total de destino principal H de la descarga directa es {number(n["primary_h"], lang)}: supera en 3.141 los 6.054.808 del espejo de julio usado en el análisis original y coincide con el control MINVU citado. La coincidencia agregada no es una conciliación individual completa, por lo que no sustituye las cifras, barras ni escenarios originales.</p>',
            f'<p>En este nuevo corte, la suma de diferencias comunales positivas pasa de {number(int(national["sum_positive_difference_before_expansion"]), lang)} a {number(int(national["sum_positive_difference_after_expansion"]), lang)}: cae {number(int(national["sum_positive_difference_reduction"]), lang)}, menos que la diferencia nacional neta porque algunas comunas ya tenían saldo no positivo y otras cruzan el cero. Frente al espejo de julio, el aumento total del recuento de roles es 79.634: 3.141 por fuente y cobertura más 76.493 por ampliar el filtro; no es un efecto puro del filtro.</p>',
            f'<p>La serie agrícola se mantiene aparte: registra {number(a["eligible_non_h_h"], lang)} roles con línea H y {number(a["agricultural_p_only"], lang)} con construcción P —casa patronal— pero sin H. Son roles, no viviendas, y no se suman al grupo no agrícola.</p>',
            '<details markdown="1"><summary>Método de la ampliación y límites de comparación</summary>',
            sii_table(sii["selected"], lang),
            '<p><strong>SII.</strong> Una línea H válida requiere ordinal y superficie positivos. Varias líneas del mismo rol cuentan una sola vez. Se excluye el rol K o referenciado como bien común y luego el rol matriz referenciado; la unidad individual miembro de una copropiedad permanece. Los destinos desconocidos o vacíos no se imputan. También se conservan los roles principales H sin línea H válida: la ausencia de esa línea no prueba ausencia residencial.</p>',
            '<p><strong>CASEN.</strong> Las cantidades se agregan a partir de una respuesta por hogar, tomada desde el registro de jefatura cuando <code>v9=3/4</code>; los residentes son quienes pertenecen a esos hogares. No se filtra por la condición de hogar principal (<code>v28</code>), que solo se pregunta en viviendas con más de un hogar. Las estimaciones nacional y regional usan <code>expr</code>. Los dos casos comunales usan <code>expc</code> solo con propósito descriptivo.</p>',
            '<p><strong>Qué puede combinarse.</strong> Dentro de la misma descarga SII sí se unen los roles principales H y los roles distintos no H con línea H válida. La serie agrícola también cuenta roles, pero se informa aparte porque queda fuera del universo no agrícola elegido. Los hogares CASEN y de campamentos sí son unidades distintas y su solapamiento no está controlado; no se suman a esa unión. La sensibilidad 2024S2 y los escenarios fiscales originales permanecen intactos.</p>',
            '<p><a href="/assets/data/avaluos-ii-extension/method.md">Método completo</a> · <a href="/assets/data/avaluos-ii-extension/provenance.json">Procedencia y SHA-256</a> · <a href="/assets/data/avaluos-ii-extension/expanded-comparison.csv">Comparación comunal ampliada</a> · <a href="/assets/data/avaluos-ii-extension/expanded-national-summary.csv">Resumen nacional</a> · <a href="/assets/data/avaluos-ii-extension/sii-destination-breakdown.csv">Desglose por destino principal del grupo elegible</a></p>',
            "</details>",
            "{% endif %}",
        ]
    else:
        parts = [
            "{% if include.section == 'casen' %}",
            "<h3>How many households and residents the CASEN signal describes</h3>",
            "<p>Categories 3 and 4 of <code>v9</code> are observed in the household response, taken once from its head's record, but the expanded quantities below describe <strong>whole households and the residents of those households</strong>. They do not count people who independently reported that site category. Chile uses <code>expr</code>; Valparaíso and Viña del Mar use <code>expc</code> as descriptive commune results without statistical representativeness.</p>",
            casen_table(casen["selected"], lang),
            '<p>The signal is compatible with several dwellings on one site, but CASEN does not link the reported site to an SII property record. It therefore does not establish that the SII is unable to record those buildings. <a href="/assets/data/avaluos-ii-extension/casen-quantities.csv">Download the aggregate quantities</a>. The published national 1.09%, Valparaíso 9.27%, Viña del Mar 8.60% and their existing intervals remain unchanged.</p>',
            "{% else %}",
            "<p>The direct national SII download makes it possible to inspect construction lines within each property record. A record whose primary use is commercial or another code may contain a construction line with use H. Filtering only on primary use H can therefore leave out <strong>residential use already recorded within non-H records</strong>. The lines capture the presence of use H, but not how many census dwellings it represents: this cross-check counts administrative records and does not establish omitted dwellings.</p>",
            expanded_table(expanded, lang),
            f'<p>Across the non-agricultural series, {number(n["non_h_with_h_line"], lang)} non-H records contain at least one valid H line. After excluding {number(n["excluded_common"], lang)} common-property records and {number(n["excluded_matrix"], lang)} referenced parent records, <strong>{number(n["eligible_non_h_h"], lang)} distinct records</strong> remain. Because they do not overlap the {number(n["primary_h"], lang)} primary-H records in the same file, their union expands the non-agricultural count with residential evidence to <strong>{number(n["primary_h"] + n["eligible_non_h_h"], lang)}</strong> and reduces the national arithmetic difference with the Census by {number(n["eligible_non_h_h"], lang)}. This does not turn each record into a dwelling and is not the sum of positive commune gaps.</p>',
            f'<p>The direct download contains {number(n["primary_h"], lang)} records with primary use H: 3,141 more than the July mirror\'s 6,054,808 used in the original analysis, and the same aggregate as the cited MINVU control. Aggregate agreement is not a complete record-level reconciliation, so it does not replace the original figures, bars or scenarios.</p>',
            f'<p>In this new cut, the sum of positive commune differences falls from {number(int(national["sum_positive_difference_before_expansion"]), lang)} to {number(int(national["sum_positive_difference_after_expansion"]), lang)}: a reduction of {number(int(national["sum_positive_difference_reduction"]), lang)}, smaller than the national net reduction because some communes already had non-positive balances and others cross zero. Relative to the July mirror, the total increase in the record count is 79,634: 3,141 from source and coverage plus 76,493 from expanding the filter; it is not a pure filter effect.</p>',
            f'<p>The agricultural series remains separate: it records {number(a["eligible_non_h_h"], lang)} roles with an H line and {number(a["agricultural_p_only"], lang)} with a P construction—a farmhouse—but no H. These are property records, not dwellings, and are not added to the non-agricultural group.</p>',
            '<details markdown="1"><summary>Extension method and comparison limits</summary>',
            sii_table(sii["selected"], lang),
            '<p><strong>SII.</strong> A valid H line requires a positive ordinal and area. Multiple lines in one record count once. A K record or a record referenced as common property is excluded first, followed by a referenced parent record; the individual condominium member remains. Unknown or empty uses are not imputed. Primary-H records without a valid H line also remain classified as H: the missing line does not establish absence of residential use.</p>',
            "<p><strong>CASEN.</strong> Quantities are aggregated from one household response, taken from its head's record when <code>v9=3/4</code>; residents are the people belonging to those households. They are not filtered by main-household status (<code>v28</code>), which is asked only in dwellings with more than one household. National and regional estimates use <code>expr</code>. The two commune cases use <code>expc</code> for descriptive purposes only.</p>",
            '<p><strong>What can be combined.</strong> Within the same SII download, primary-H records and distinct non-H records with a valid H line can be joined. The agricultural series also counts property records, but it is reported separately because it lies outside the chosen non-agricultural universe. CASEN and informal-settlement households are different units and their overlap is uncontrolled; they are not added to that union. The original 2024H2 sensitivity and fiscal scenarios remain intact.</p>',
            '<p><a href="/assets/data/avaluos-ii-extension/method.md">Full method</a> · <a href="/assets/data/avaluos-ii-extension/provenance.json">Provenance and SHA-256</a> · <a href="/assets/data/avaluos-ii-extension/expanded-comparison.csv">Expanded commune comparison</a> · <a href="/assets/data/avaluos-ii-extension/expanded-national-summary.csv">National summary</a> · <a href="/assets/data/avaluos-ii-extension/sii-destination-breakdown.csv">Primary-use breakdown of the eligible group</a></p>',
            "</details>",
            "{% endif %}",
        ]
    return "\n".join(parts) + "\n"


def render_method(sii: dict[str, Any], casen: dict[str, Any], expanded: dict[str, Any]) -> str:
    n = sii["totals"]["N"]
    a = sii["totals"]["A"]
    return f"""# Avalúos II: ampliación explicativa

## Alcance

Esta ampliación agrega cantidades CASEN y evidencia agregada de usos mixtos SII. Presenta por separado una comparación ampliada entre el Censo y grupos disjuntos de roles de la misma descarga directa. No modifica el espejo de julio, el visor, las cifras, figuras, sensibilidad 2024S2 ni los escenarios fiscales del análisis original, y no suma hogares CASEN o de campamentos a esa comparación.

## SII: fuente, unidad y clasificación

La fuente es la descarga nacional directa `BRORGA2441_NAC_2026_1.zip`, primer semestre de 2026. Una fila A/N representa un rol administrativo y las filas AL/NL describen líneas de terreno o construcción. Una línea residencial observable exige ordinal positivo, superficie positiva y destino H; varias líneas H del mismo rol cuentan una vez.

El grupo inicial contiene roles con destino principal distinto de H y al menos una línea H válida. Se excluye primero el rol con destino K o referenciado como bien común, y luego el rol matriz referenciado. Una unidad individual que referencia esos roles no se excluye automáticamente. El código K está documentado como bien común en la [guía oficial SII de 2013](https://www.sii.cl/portales/reavaluo_no_agricola/2013/guia_para_calcular_avaluo.pdf), aunque el PDF breve vigente lo omite. Los destinos vacíos o desconocidos no se imputan. Los {number(n['primary_h_without_positive_h_line'], 'es')} roles no agrícolas con destino principal H sin una línea H válida conservan su clasificación principal.

La serie N contiene {number(n['roles'], 'es')} roles y {number(n['primary_h'], 'es')} con destino principal H. Entre los roles no H, {number(n['non_h_with_h_line'], 'es')} tienen una línea H válida; tras las exclusiones quedan {number(n['eligible_non_h_h'], 'es')}. Como ambos grupos son disjuntos dentro del mismo archivo, forman {number(n['primary_h'] + n['eligible_non_h_h'], 'es')} roles no agrícolas con evidencia residencial. La serie A se informa aparte: {number(a['eligible_non_h_h'], 'es')} roles con H y {number(a['agricultural_p_only'], 'es')} con P sin H. Estos resultados cuentan roles, no viviendas, hogares, personas, construcciones omitidas, deuda ni recaudación.

El total H principal de la descarga directa supera en 3.141 al espejo de julio y coincide con el control MINVU citado en el post. Es una concordancia agregada, no una conciliación individual completa; por eso no sustituye el denominador histórico.

## CASEN: cantidades y dominio

Las cantidades corresponden a una respuesta por hogar tomada desde el registro de jefatura cuando `v9=3/4`: sitio propio compartido con otras viviendas, pagado o pagándose. Los residentes son todas las personas pertenecientes a esos hogares, no personas que hayan respondido esa categoría de manera independiente. No se filtra por la condición de hogar principal (`v28`), que solo se pregunta en viviendas con más de un hogar. Chile usa `expr`; Valparaíso y Viña del Mar usan `expc` como descripciones comunales sin representatividad estadística. Los tamaños muestrales de hogares y residentes se publican en unidades separadas.

## Límite de combinación

Los roles principales H y los roles distintos no H con línea H válida sí se unen dentro de la misma descarga SII. La serie agrícola también cuenta roles, pero se informa aparte porque queda fuera del universo no agrícola elegido. Los hogares CASEN y de campamentos usan otra unidad y no tienen un identificador que permita controlar el solapamiento, por lo que no se suman ni se restan de esa unión. El aporte de esos mecanismos a la diferencia requeriría un enlace vivienda–sitio–rol con fechas compatibles.

## Archivos públicos

- `sii-communes.csv`: agregados por comuna y serie.
- `sii-destination-breakdown.csv`: desglose agregado del grupo elegible por destino principal.
- `casen-quantities.csv`: Chile, Valparaíso y Viña del Mar, con cantidades y muestras.
- `expanded-comparison.csv`: comparación comunal completa entre el filtro H directo y la unión ampliada.
- `expanded-national-summary.csv`: diferencia nacional neta y suma de diferencias positivas, antes y después de ampliar.
- `audit.json`: identidades y cobertura verificadas por el proyector.
- `provenance.json`: nombres, SHA-256 y URL disponibles; no incluye rutas internas.
"""


def write_csv(path: Path, rows: list[dict[str, Any]], columns: tuple[str, ...]) -> None:
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows({column: row[column] for column in columns} for row in rows)


def source_receipt(label: str, source: dict[str, Any]) -> dict[str, Any]:
    provenance = source["provenance"]
    files = []
    for key in ("csv_path", "communes_path", "destinations_path", "comparison_path", "summary_path", "audit_path", "provenance_path"):
        path = source.get(key)
        if isinstance(path, Path):
            files.append({"filename": path.name, "sha256": sha256(path)})
    archive_name = provenance.get("source_filename")
    archive_sha = provenance.get("source_sha256")
    if isinstance(archive_name, str) and isinstance(archive_sha, str):
        files.append({"filename": Path(archive_name).name, "sha256": archive_sha})
    upstream_sources = provenance.get("sources", [])
    if isinstance(upstream_sources, list):
        for item in upstream_sources:
            if not isinstance(item, dict):
                continue
            filename, digest = item.get("filename"), item.get("sha256")
            if isinstance(filename, str) and isinstance(digest, str):
                files.append({"filename": Path(filename).name, "sha256": digest})
    unique_files = {(item["filename"], item["sha256"]): item for item in files}
    return {"label": label, "files": list(unique_files.values()), "urls": extract_urls(provenance)}


def project(sii_dir: Path, casen_dir: Path, output_dir: Path, include_dir: Path) -> dict[str, Any]:
    source_paths = (
        sii_dir / "sii-communes.csv",
        sii_dir / "sii-destination-breakdown.csv",
        sii_dir / "sii-audit.json",
        sii_dir / "sii-provenance.json",
        casen_dir / "casen-counts.csv",
        casen_dir / "casen-counts-audit.json",
        casen_dir / "casen-counts-provenance.json",
        sii_dir / "expanded-comparison.csv",
        sii_dir / "expanded-national-summary.csv",
        sii_dir / "expanded-audit.json",
        sii_dir / "expanded-provenance.json",
    )
    source_digests = {path: sha256(path) for path in source_paths}
    sii = validate_sii(sii_dir)
    casen = validate_casen(casen_dir)
    expanded = validate_expanded(sii_dir, sii)
    output_dir.parent.mkdir(parents=True, exist_ok=True)
    include_dir.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="avaluos-ii-extension-", dir=output_dir.parent) as temporary:
        stage = Path(temporary)
        (stage / "sii-communes.csv").write_bytes(sii["communes_path"].read_bytes())
        (stage / "sii-destination-breakdown.csv").write_bytes(sii["destinations_path"].read_bytes())
        write_csv(stage / "casen-quantities.csv", casen["selected"], CASEN_PUBLIC_COLUMNS)
        (stage / "expanded-comparison.csv").write_bytes(expanded["comparison_path"].read_bytes())
        (stage / "expanded-national-summary.csv").write_bytes(expanded["summary_path"].read_bytes())
        (stage / "method.md").write_text(render_method(sii, casen, expanded), encoding="utf-8")

        audit = {
            "schema_version": 1,
            "scope": "explanatory_extension_only",
            "original_analysis_modified": False,
            "sii": {
                "unit": "administrative role; not a dwelling, household, person or unregistered building",
                "commune_series_rows": sii["row_count"],
                "destination_rows": sii["destination_row_count"],
                "role_keys_unique": sii["audit"]["role_keys_unique"],
                "source_unchanged": sii["audit"]["source_unchanged"],
                "unresolved_candidate_roles": sii["totals"]["A"]["unresolved"] + sii["totals"]["N"]["unresolved"],
                "unknown_construction_destinations": sii["audit"].get("unknown_construction_destinations", []),
                "construction_without_positive_area": sii["audit"].get("construction_without_positive_area"),
                "primary_h_without_positive_h_line": sii["totals"]["N"]["primary_h_without_positive_h_line"],
            },
            "casen": {
                "unit": "households selected by household-head v9 response; residents belonging to those households",
                "rows": casen["row_count"],
                "national_weight": "expr",
                "commune_weight": "expc",
                "commune_representativeness": False,
            },
            "combination": "disjoint_direct_sii_role_groups_joined; other units kept separate",
            "raw_rows_exported": False,
        }
        (stage / "audit.json").write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        rendered_includes: dict[str, Path] = {}
        for lang in ("es", "en"):
            path = stage / f"avaluos-ii-extension-{lang}.html"
            path.write_text(render_include(sii, casen, expanded, lang), encoding="utf-8")
            rendered_includes[lang] = path

        provenance = {
            "schema_version": 1,
            "publication_snapshot": "2026-09-13",
            "sources": [source_receipt("sii", sii), source_receipt("expanded_comparison", expanded), source_receipt("casen", casen)],
            "documentation_urls": [
                "https://www4.sii.cl/sismunInternet6/descargaArchivo",
                "https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Cuestionario_Casen_2024.pdf",
                "https://observatorio.ministeriodesarrollosocial.gob.cl/storage/docs/casen/2024/Nota_uso_bases_de_datos_Casen_2024.pdf",
            ],
            "outputs_sha256": {
                path.name: sha256(path)
                for path in sorted(stage.iterdir())
                if path.is_file() and path.name != "provenance.json"
            },
            "includes_sha256": {path.name: sha256(path) for path in rendered_includes.values()},
            "projector": {"filename": Path(__file__).name, "sha256": sha256(Path(__file__))},
            "private_paths_exported": False,
            "raw_rows_exported": False,
        }
        raw_provenance = json.dumps(provenance, ensure_ascii=False, indent=2) + "\n"
        require("/home/" not in raw_provenance, "public provenance contains an internal path")
        (stage / "provenance.json").write_text(raw_provenance, encoding="utf-8")

        require(
            source_digests == {path: sha256(path) for path in source_paths},
            "source aggregates changed during projection; no output was replaced",
        )

        output_dir.mkdir(parents=True, exist_ok=True)
        for name in PUBLIC_FILES:
            os.replace(stage / name, output_dir / name)
        for lang, source in rendered_includes.items():
            os.replace(source, include_dir / f"avaluos-ii-extension-{lang}.html")

    return {
        "output_dir": str(output_dir),
        "public_files": list(PUBLIC_FILES),
        "includes": [f"avaluos-ii-extension-{lang}.html" for lang in ("es", "en")],
        "sii_eligible_non_h_h": sii["totals"]["N"]["eligible_non_h_h"],
        "casen_territories": [row["territory_code"] for row in casen["selected"]],
        "raw_rows_exported": False,
    }


def check_projection(output_dir: Path, include_dir: Path, baseline_path: Path) -> dict[str, Any]:
    provenance_path = output_dir / "provenance.json"
    provenance = read_json(provenance_path)
    require(provenance.get("private_paths_exported") is False, "projection reports internal paths")
    require(provenance.get("raw_rows_exported") is False, "projection reports raw rows")
    raw_public = "\n".join((output_dir / name).read_text(encoding="utf-8") for name in PUBLIC_FILES)
    require("/home/" not in raw_public, "public extension contains an internal path")

    expected_outputs = provenance.get("outputs_sha256")
    require(isinstance(expected_outputs, dict), "projected provenance lacks output hashes")
    for filename, expected in expected_outputs.items():
        path = include_dir / filename if filename.startswith("avaluos-ii-extension-") else output_dir / filename
        require(path.is_file(), f"projected output is missing: {filename}")
        require(sha256(path) == expected, f"projected output hash mismatch: {filename}")
    require(
        provenance.get("projector", {}).get("sha256") == sha256(Path(__file__)),
        "projector changed after projection",
    )

    public_casen = read_csv_exact(output_dir / "casen-quantities.csv", CASEN_PUBLIC_COLUMNS)
    require([row["territory_code"] for row in public_casen] == ["CL", "5101", "5109"], "public CASEN selection changed")
    read_csv_exact(output_dir / "sii-communes.csv", SII_COLUMNS)
    read_csv_exact(output_dir / "sii-destination-breakdown.csv", SII_DESTINATION_COLUMNS)
    read_csv_exact(output_dir / "expanded-comparison.csv", EXPANDED_COMPARISON_COLUMNS)
    read_csv_exact(output_dir / "expanded-national-summary.csv", EXPANDED_SUMMARY_COLUMNS)

    baseline = read_json(baseline_path)
    blog_head = baseline.get("blog_head")
    require(isinstance(blog_head, str) and blog_head, "baseline lacks blog_head")
    post_hashes = {}
    for post in POSTS:
        text = post.read_text(encoding="utf-8")
        include_name = "avaluos-ii-extension-en.html" if post.name.endswith("-en.md") else "avaluos-ii-extension-es.html"
        relative = str(post.relative_to(ROOT))
        original = baseline_post(blog_head, relative)
        require(front_matter(text) == front_matter(original), f"{post.name}: protected front matter changed")
        require(
            sorted(PROTECTED_REFERENCE_PATTERN.findall(text)) == sorted(PROTECTED_REFERENCE_PATTERN.findall(original)),
            f"{post.name}: protected figure or viewer references changed",
        )
        require(f"{{% include {include_name} section='sii' %}}" in text, f"{post.name}: SII extension include missing")
        require(f"{{% include {include_name} section='casen' %}}" in text, f"{post.name}: CASEN extension include missing")
        post_hashes[relative] = sha256(post)

    return {
        "status": "passed",
        "projector_sha256": sha256(Path(__file__)),
        "posts_sha256": post_hashes,
        "includes_sha256": provenance["includes_sha256"],
        "public_data_sha256": {
            name: sha256(output_dir / name)
            for name in PUBLIC_FILES
        },
        "baseline_sha256": sha256(baseline_path),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sii-dir", type=Path, default=DEFAULT_SII_DIR)
    parser.add_argument("--casen-dir", type=Path)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    parser.add_argument("--include-dir", type=Path, default=DEFAULT_INCLUDE_DIR)
    parser.add_argument("--baseline", type=Path, default=DEFAULT_SII_DIR / "baseline.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        result = check_projection(args.output_dir, args.include_dir, args.baseline)
    else:
        require(args.casen_dir is not None, "--casen-dir is required unless --check is used")
        result = project(args.sii_dir, args.casen_dir, args.output_dir, args.include_dir)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
