#!/usr/bin/env python3
"""Render bilingual, governance-controlled SVG evidence for thesis extension Post II.

The renderer consumes allow-listed public CSV exports produced by the scientific
repository. It emits deterministic SVGs, a Jekyll data file, and a hash manifest;
it never reads student microdata or the private matched-pair output.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import math
import re
import sys
import textwrap
from collections.abc import Iterable, Mapping, Sequence
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
INPUT_DIR = (
    WORKSPACE
    / "incubadora/tesis_mae_mejorada/figures/post2_stylized_evidence"
)
OUTPUT_DIR = ROOT / "assets/images/extender-tesis-no-es-agregar-anos"
DATA_PATH = ROOT / "_data/thesis_extension_stylized.yml"
MANIFEST_PATH = OUTPUT_DIR / "estilizada-manifest.json"
MAP_DATA_PATH = ROOT / "assets/data/thesis-extension-post2/cases.json"
AVALUOS_THEME_PATH = ROOT / "assets/src/catastro_sii/chart-theme.ts"
AUTHOR_CASE_PATH = (
    WORKSPACE
    / "incubadora/tesis_mae_mejorada/research/article_post2/el_salvador_author_case.yaml"
)

INPUTS = {
    "demography": INPUT_DIR / "demographic_pressure.csv",
    "spatial": INPUT_DIR / "spatial_case_summary.csv",
    "trajectory": INPUT_DIR / "comparable_trajectory.csv",
    "case_trajectory": INPUT_DIR / "case_trajectory.csv",
    "school_points": INPUT_DIR / "spatial_school_points.csv",
    "school_links": INPUT_DIR / "spatial_school_links.csv",
}

COLORS = {
    "navy": "#10121d",
    "navy_2": "#171b2a",
    "navy_3": "#22283b",
    "ink": "#f4f7fb",
    "muted": "#b8c2d6",
    "grid": "#48516a",
    "cyan": "#37e7ff",
    "lime": "#b8ff3c",
    "magenta": "#ff4fd8",
    "amber": "#ffd166",
}
AVALUOS_SHARED_ACCENTS = ("cyan", "lime", "magenta", "amber")

EXPECTED_HEADERS = {
    "demography": {
        "year",
        "population_age_6_17",
        "index_2025_100",
        "change_from_2025_percent",
        "series_status",
    },
    "spatial": {
        "case",
        "commune",
        "paired_closures",
        "nearby_entries",
        "event_period",
        "closure_year",
        "entry_year",
        "closure_rbd",
        "entry_rbd",
        "entry_coordinate_year",
        "location_lag_years",
        "median_distance_km",
        "distance_band",
        "same_commune_pairs",
        "education_segment",
        "segment_family",
        "outcome_completeness",
        "selection_rank",
    },
    "trajectory": {
        "branch",
        "outcome",
        "relative_year",
        "status",
        "estimate",
        "ci95_low",
        "ci95_high",
        "units",
        "median_comparators",
        "regimes",
    },
    "case_trajectory": {
        "case",
        "commune",
        "branch",
        "outcome",
        "relative_year",
        "status",
        "estimate",
        "units",
        "minimum_units",
        "regimes",
    },
    "school_points": {
        "case",
        "commune",
        "role",
        "rbd",
        "school_name",
        "event_year",
        "coordinate_year",
        "location_lag_years",
        "latitude",
        "longitude",
        "official_source_url",
        "market_segment",
    },
    "school_links": {
        "case",
        "commune",
        "closure_rbd",
        "entry_rbd",
        "closure_year",
        "entry_year",
        "entry_coordinate_year",
        "location_lag_years",
        "distance_km",
        "market_segment",
    },
}

FORBIDDEN_HEADERS = re.compile(
    r"(?i)^(?:student_id|student_name|person_id|run|rut|mrun|dvrut|idalumno|rut_sostenedor|phone|email|private_path)$"
)
PRIVATE_TEXT = re.compile(
    r"(?i)(?:/home/|Descargas/programaciones|\b(?:student_id|person_id|run|rut|mrun|dvrut|idalumno)\b)"
)
SAFE_SLUG = re.compile(r"[^a-z0-9]+")


TEXT = {
    "es": {
        "demographic_title": "Menos población en edad escolar: una presión que ya viene en camino",
        "demographic_desc": (
            "Serie nacional de población de 6 a 17 años, índice 2025 igual a 100. "
            "Las estimaciones terminan en 2024 y las proyecciones comienzan en 2025."
        ),
        "estimate": "Estimación 2013–2024",
        "projection": "Proyección 2025–2050",
        "index_axis": "Índice (2025 = 100)",
        "projection_boundary": "Comienza la proyección",
        "demographic_callout": "−55,7 %",
        "demographic_callout_detail": "población de 6–17 años entre 2025 y 2050",
        "not_enrolment": "Es población, no una proyección de matrícula.",
        "trajectory_simce_title": "SIMCE: el soporte es desigual entre años",
        "trajectory_simce_desc": (
            "Trayectorias nacionales de SIMCE relativo. Salidas y entradas están en paneles "
            "independientes; cada punto muestra unidades y, cuando es estimable, intervalo "
            "de confianza de 95 por ciento."
        ),
        "trajectory_admission_title": "Admisión: las entradas no alcanzan soporte inferencial",
        "trajectory_admission_desc": (
            "Trayectorias nacionales de pruebas de admisión, estandarizadas dentro de cada "
            "régimen. Las cruces son celdas descriptivas sin soporte inferencial suficiente."
        ),
        "exit_panel": "Antes de la salida",
        "entry_panel": "Después de la entrada",
        "simce": "SIMCE relativo",
        "admission": "Admisión · núcleo",
        "sd_axis": "Diferencia estandarizada (DE)",
        "estimated": "Celda descriptiva con IC 95 %",
        "not_estimable": "NOT_ESTIMABLE · solo descriptivo",
        "units": "unidades",
        "changing_support": "El soporte cambia entre años; no es un estudio de evento causal.",
        "comparison_direction": "Punto = establecimiento que sale o entra menos sus comparables.",
        "map_title": "Cierres con origen en {commune} y entradas compatibles cercanas",
        "map_desc": (
            "Mapa de establecimientos con coordenadas oficiales para {commune}. Las equis son cierres y los signos "
            "más son aperturas compatibles; las líneas muestran el emparejamiento de proximidad, no destinos."
        ),
        "schematic": "COORDENADAS OFICIALES · SIN TRAYECTORIAS DE ESTUDIANTES",
        "closure_group": "cierres emparejados",
        "compatible_pairs": "pares compatibles",
        "unique_entries": "entradas únicas cercanas",
        "median_distance": "distancia mediana",
        "same_commune": "pares en la misma comuna",
        "period": "periodo",
        "selection": (
            "Selección mecánica por familia, misma comuna, distancia, año y RBD; "
            "sin usar resultados."
        ),
        "pair_legend": "+ apertura compatible",
        "closure_legend": "× cierre oficial",
        "outcome_strip": "Indicadores comunales publicables",
        "suppressed": "N bajo umbral",
        "published": "publicado",
        "local_caveat": (
            "Las celdas pequeñas se ocultan. Una entrada cercana no se interpreta como "
            "receptora de estudiantes."
        ),
        "demographic_source": (
            "Fuente: INE, estimaciones y proyecciones de población 1992–2070, base 2024."
        ),
        "trajectory_source": (
            "Fuente: MINEDUC, directorios, matrícula y resultados; elaboración propia."
        ),
        "map_source": (
            "Fuente: Directorio oficial MINEDUC; emparejamiento propio, no destino estudiantil."
        ),
        "radius_pairs": "{count} pares",
    },
    "en": {
        "demographic_title": "A smaller school-age population: pressure already in motion",
        "demographic_desc": (
            "National population aged 6–17, indexed to 2025 equals 100. Estimates end in "
            "2024 and projections begin in 2025."
        ),
        "estimate": "Estimate 2013–2024",
        "projection": "Projection 2025–2050",
        "index_axis": "Index (2025 = 100)",
        "projection_boundary": "Projection begins",
        "demographic_callout": "−55.7%",
        "demographic_callout_detail": "population aged 6–17 between 2025 and 2050",
        "not_enrolment": "This is population, not an enrolment projection.",
        "trajectory_simce_title": "SIMCE: support is uneven across years",
        "trajectory_simce_desc": (
            "National relative-SIMCE trajectories. Exits and entries are shown in separate "
            "panels; each point reports units and, when estimable, a 95 percent confidence interval."
        ),
        "trajectory_admission_title": "Admissions: entrants lack inferential support",
        "trajectory_admission_desc": (
            "National admissions-test trajectories, standardised within each regime. "
            "Crosses mark descriptive cells without enough support for inference."
        ),
        "exit_panel": "Before exit",
        "entry_panel": "After entry",
        "simce": "Relative SIMCE",
        "admission": "Admissions · core",
        "sd_axis": "Standardised difference (SD)",
        "estimated": "Descriptive cell with 95% CI",
        "not_estimable": "NOT_ESTIMABLE · descriptive only",
        "units": "units",
        "changing_support": "Support changes across years; this is not a causal event study.",
        "comparison_direction": "Point = exiting or entering school minus its comparators.",
        "map_title": "Closures anchored in {commune} and nearby compatible entries",
        "map_desc": (
            "School map using official coordinates for {commune}. Crosses are closures and plus signs are "
            "compatible openings; lines show the proximity match, not student destinations."
        ),
        "schematic": "OFFICIAL COORDINATES · NO STUDENT TRAJECTORIES",
        "closure_group": "paired closures",
        "compatible_pairs": "compatible pairs",
        "unique_entries": "unique nearby entries",
        "median_distance": "median distance",
        "same_commune": "same-commune pairs",
        "period": "period",
        "selection": (
            "Mechanical selection by family, same-commune status, distance, year, "
            "and RBD; outcomes are not used."
        ),
        "pair_legend": "+ compatible opening",
        "closure_legend": "× official closure",
        "outcome_strip": "Publishable commune-level indicators",
        "suppressed": "N below threshold",
        "published": "published",
        "local_caveat": (
            "Small cells are withheld. A nearby entrant is not interpreted as receiving students."
        ),
        "demographic_source": (
            "Source: INE, 1992–2070 population estimates and projections, 2024 base."
        ),
        "trajectory_source": (
            "Source: MINEDUC directories, enrolment and outcomes; author calculations."
        ),
        "map_source": (
            "Source: official MINEDUC directory; author match, not student destination."
        ),
        "radius_pairs": "{count} pairs",
    },
}


def esc(value: Any) -> str:
    return html.escape(str(value), quote=True)


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def sha256_path(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def slug(value: str) -> str:
    replacements = str.maketrans("áéíóúñ", "aeioun")
    return SAFE_SLUG.sub("-", value.lower().translate(replacements)).strip("-")


def fmt_decimal(value: float, digits: int, lang: str, signed: bool = False) -> str:
    rendered = f"{value:+.{digits}f}" if signed else f"{value:.{digits}f}"
    if lang == "es":
        rendered = rendered.replace(".", ",")
    return rendered.replace("-", "−")


def display_period(value: str) -> str:
    start, separator, end = value.partition("–")
    return start if separator and start == end else value


def read_rows(key: str) -> list[dict[str, str]]:
    path = INPUTS[key]
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        headers = set(reader.fieldnames or [])
        if headers != EXPECTED_HEADERS[key]:
            raise ValueError(f"cabeceras inesperadas en {path.name}: {sorted(headers)}")
        if any(FORBIDDEN_HEADERS.search(field) for field in headers):
            raise ValueError(f"cabecera institucional prohibida en {path.name}")
        rows = list(reader)
    if not rows:
        raise ValueError(f"entrada vacía: {path}")
    return rows


def load_data() -> dict[str, list[dict[str, str]]]:
    theme_text = AVALUOS_THEME_PATH.read_text(encoding="utf-8")
    missing_accents = [
        COLORS[name] for name in AVALUOS_SHARED_ACCENTS if COLORS[name] not in theme_text
    ]
    if missing_accents:
        raise ValueError(
            "la paleta dejó de coincidir con el visor de Avalúos: "
            + ", ".join(missing_accents)
        )
    data = {key: read_rows(key) for key in INPUTS}
    validate_data(data)
    return data


def load_author_case() -> dict[str, Any]:
    raw = yaml.safe_load(AUTHOR_CASE_PATH.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise TypeError("el expediente de El Salvador no es un objeto YAML")
    validate_author_case(raw)
    return raw


def haversine_km(left: Mapping[str, Any], right: Mapping[str, Any]) -> float:
    radius = 6371.0088
    lat1 = math.radians(float(left["latitude"]))
    lat2 = math.radians(float(right["latitude"]))
    delta_lat = lat2 - lat1
    delta_lon = math.radians(float(right["longitude"]) - float(left["longitude"]))
    value = (
        math.sin(delta_lat / 2) ** 2
        + math.cos(lat1) * math.cos(lat2) * math.sin(delta_lon / 2) ** 2
    )
    return 2 * radius * math.asin(math.sqrt(value))


def validate_author_case(case: Mapping[str, Any]) -> None:
    if case.get("status") != "documented_descriptive_case":
        raise ValueError("El Salvador dejó de ser un caso descriptivo documentado")
    selection = case["selection"]
    if selection.get("systematic_sample_member") is not False or selection.get("uses_outcomes") is not False:
        raise ValueError("El Salvador contaminó la selección sistemática")
    event = case["event"]
    if event.get("type") != "documented_closure_and_merger" or int(event.get("school_year", 0)) != 2014:
        raise ValueError("cronología o tipo de evento de El Salvador derivó")
    closure = case["schools"]["closure"]
    receiver = case["schools"]["receiver"]
    if int(closure["rbd"]) != 391 or int(receiver["rbd"]) != 390:
        raise ValueError("identidad RBD de El Salvador derivó")
    if int(receiver["coordinate_reference_year"]) != 2020 or "Diego Portales 1510" not in receiver["address"]:
        raise ValueError("la coordenada receptora no conserva su contraste documental")
    for school in (closure, receiver):
        if not (-60 <= float(school["latitude"]) <= -10 and -112 <= float(school["longitude"]) <= -60):
            raise ValueError("coordenada de El Salvador fuera de Chile")
    observed_distance = haversine_km(closure, receiver)
    if abs(observed_distance - float(case["schools"]["geodesic_distance_km"])) > 0.002:
        raise ValueError("distancia de El Salvador no coincide con las coordenadas")
    rows = {int(row["year"]): row for row in case["enrollment"]["rows"]}
    required = {
        2004: (818, 581, 1399),
        2013: (545, 432, 977),
        2014: (0, 738, 738),
        2025: (0, 445, 445),
    }
    for year, values in required.items():
        row = rows.get(year, {})
        observed = (
            int(row.get("closure_rbd_391", -1)),
            int(row.get("receiver_rbd_390", -1)),
            int(row.get("combined", -1)),
        )
        if observed != values:
            raise ValueError(f"matrícula de El Salvador derivó en {year}")
    summaries = case["enrollment"]["summaries"]
    if abs(float(summaries["combined_change_2004_2013_percent"]) + 30.164403) > 0.000001:
        raise ValueError("variación 2004-2013 de El Salvador derivó")
    source_ids = {row["id"] for row in case["documentary_sources"]}
    if not {"bcn_2014", "fees_regulation_2019", "fees_bulletin_2020", "mineduc_open_data"}.issubset(source_ids):
        raise ValueError("fuentes documentales de El Salvador incompletas")
    not_verified = " ".join(case["epistemic_register"]["not_verified"]).lower()
    if "razón administrativa" not in not_verified or "cada estudiante" not in not_verified:
        raise ValueError("límites epistémicos de El Salvador incompletos")


def validate_data(data: Mapping[str, Sequence[Mapping[str, str]]]) -> None:
    demography = data["demography"]
    years = [int(row["year"]) for row in demography]
    if years != sorted(years) or 2013 not in years or 2025 not in years or 2050 not in years:
        raise ValueError("la serie demográfica no cubre ordenadamente 2013, 2025 y 2050")
    if any(
        row["series_status"] not in {"ESTIMATE", "PROJECTION"}
        or (int(row["year"]) <= 2024) != (row["series_status"] == "ESTIMATE")
        for row in demography
    ):
        raise ValueError("frontera estimación/proyección inválida")

    spatial = data["spatial"]
    if len(spatial) != 2 or [int(row["selection_rank"]) for row in spatial] != [1, 2]:
        raise ValueError("se esperaban dos casos comunales con ranking 1–2")
    if any(int(row["paired_closures"]) != 1 or int(row["nearby_entries"]) != 1 for row in spatial):
        raise ValueError("cada caso debe representar un cierre y una apertura estrictos")
    if [row["segment_family"] for row in spatial] != ["initial", "basic"]:
        raise ValueError("los casos sistemáticos no siguen el orden inicial y básica")

    points = data["school_points"]
    links = data["school_links"]
    if len(points) != 4 or len(links) != 2:
        raise ValueError("la geografía pública no contiene cuatro puntos y dos pares estrictos")
    case_keys = {(row["case"], row["commune"]) for row in spatial}
    if {(row["case"], row["commune"]) for row in points} != case_keys:
        raise ValueError("los puntos institucionales no calzan con los casos comunales")
    if {(row["case"], row["commune"]) for row in links} != case_keys:
        raise ValueError("los enlaces institucionales no calzan con los casos comunales")
    point_keys = {
        (row["case"], row["role"], int(row["rbd"])) for row in points
    }
    if any(row["role"] not in {"closure", "entry"} for row in points):
        raise ValueError("rol institucional desconocido")
    if any(
        int(row["coordinate_year"]) - int(row["event_year"])
        != int(row["location_lag_years"])
        for row in points
        if row["role"] == "entry"
    ):
        raise ValueError("rezago de coordenada de entrada inconsistente")
    if any(
        not (-60 <= float(row["latitude"]) <= -10)
        or not (-112 <= float(row["longitude"]) <= -60)
        or not row["official_source_url"].startswith("https://datosabiertos.mineduc.cl/")
        for row in points
    ):
        raise ValueError("punto institucional sin coordenada o procedencia oficial válida")
    for row in links:
        case = row["case"]
        if (case, "closure", int(row["closure_rbd"])) not in point_keys:
            raise ValueError("enlace sin establecimiento de cierre")
        if (case, "entry", int(row["entry_rbd"])) not in point_keys:
            raise ValueError("enlace sin establecimiento de entrada")
    segment_by_case = {row["case"]: row["education_segment"] for row in spatial}
    if any(point["market_segment"] != segment_by_case[point["case"]] for point in points):
        raise ValueError("punto institucional fuera del segmento exacto del caso")
    if any(link["market_segment"] != segment_by_case[link["case"]] for link in links):
        raise ValueError("enlace institucional fuera del segmento exacto del caso")

    trajectory = data["trajectory"]
    expected = {
        (branch, outcome, year)
        for branch, years_for_branch in (("exit", (-3, -2, -1)), ("entry", (0, 1, 2)))
        for outcome in ("simce_relative", "admission_core")
        for year in years_for_branch
    }
    observed = {
        (row["branch"], row["outcome"], int(row["relative_year"]))
        for row in trajectory
    }
    if observed != expected:
        raise ValueError("la trayectoria nacional no contiene las doce celdas esperadas")
    for row in trajectory:
        if row["status"] not in {"ESTIMATED", "NOT_ESTIMABLE"}:
            raise ValueError("estado de trayectoria desconocido")
        has_interval = bool(row["ci95_low"] and row["ci95_high"])
        if has_interval != (row["status"] == "ESTIMATED"):
            raise ValueError("intervalo incompatible con estado de estimación")

    cases = data["case_trajectory"]
    if {(row["case"], row["commune"]) for row in cases} != case_keys:
        raise ValueError("las trayectorias comunales no calzan con los casos espaciales")
    if any(row["status"] not in {"PUBLISHED", "SUPPRESSED_SMALL_N"} for row in cases):
        raise ValueError("estado comunal desconocido")


def svg_shell(title: str, desc: str, body: str, *, height: int = 720) -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{height}" viewBox="0 0 1200 {height}" role="img" aria-labelledby="figure-title figure-desc">
  <title id="figure-title">{esc(title)}</title>
  <desc id="figure-desc">{esc(desc)}</desc>
  <defs>
    <pattern id="projection-hatch" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(35)">
      <line x1="0" y1="0" x2="0" y2="12" stroke="{COLORS['lime']}" stroke-width="3" opacity="0.24"/>
    </pattern>
    <filter id="soft-shadow" x="-20%" y="-20%" width="140%" height="140%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#000000" flood-opacity="0.28"/>
    </filter>
  </defs>
  <style>
    text {{ font-family: Inter, "Inter var", system-ui, sans-serif; }}
    .title {{ fill: {COLORS['ink']}; font-size: 32px; font-weight: 760; letter-spacing: -0.4px; }}
    .subtitle {{ fill: {COLORS['muted']}; font-size: 16px; }}
    .label {{ fill: {COLORS['ink']}; font-size: 16px; }}
    .small {{ fill: {COLORS['muted']}; font-size: 14px; }}
    .tiny {{ fill: {COLORS['muted']}; font-size: 12px; }}
    .number {{ fill: {COLORS['ink']}; font-size: 22px; font-weight: 760; font-variant-numeric: tabular-nums; }}
    .kicker {{ fill: {COLORS['cyan']}; font-size: 13px; font-weight: 750; letter-spacing: 1.4px; }}
    .map-title {{ fill: {COLORS['ink']}; font-size: 40px; font-weight: 780; letter-spacing: -0.5px; }}
    .map-label {{ fill: {COLORS['muted']}; font-size: 18px; }}
    .map-small {{ fill: {COLORS['muted']}; font-size: 16px; }}
    .map-value {{ fill: {COLORS['ink']}; font-size: 34px; font-weight: 780; font-variant-numeric: tabular-nums; }}
  </style>
  <rect width="1200" height="{height}" rx="24" fill="{COLORS['navy']}"/>
{body}
</svg>
'''


def text_block(lines: Iterable[str], x: float, y: float, css_class: str, gap: int = 22) -> str:
    tspans = "".join(
        f'<tspan x="{x}" y="{y + index * gap}">{esc(line)}</tspan>'
        for index, line in enumerate(lines)
    )
    return f'  <text class="{css_class}">{tspans}</text>\n'


def wrapped(value: str, width: int = 112) -> list[str]:
    return textwrap.wrap(value, width=width, break_long_words=False, break_on_hyphens=False)


def polyline(points: Sequence[tuple[float, float]]) -> str:
    return " ".join(f"{x:.2f},{y:.2f}" for x, y in points)


def render_demography(rows: Sequence[Mapping[str, str]], lang: str) -> str:
    copy = TEXT[lang]
    selected = [row for row in rows if 2013 <= int(row["year"]) <= 2050]
    x0, x1, y0, y1 = 112.0, 1128.0, 190.0, 570.0
    min_index, max_index = 40.0, 105.0

    def xy(row: Mapping[str, str]) -> tuple[float, float]:
        year = int(row["year"])
        index = float(row["index_2025_100"])
        x = x0 + (year - 2013) / (2050 - 2013) * (x1 - x0)
        y = y1 - (index - min_index) / (max_index - min_index) * (y1 - y0)
        return x, y

    estimate = [row for row in selected if row["series_status"] == "ESTIMATE"]
    projection = [next(row for row in selected if int(row["year"]) == 2024)] + [
        row for row in selected if row["series_status"] == "PROJECTION"
    ]
    body = [
        '  <text class="kicker" x="72" y="64">POST II · PRESIÓN DEMOGRÁFICA</text>',
        f'  <text class="title" x="72" y="110">{esc(copy["demographic_title"])}</text>',
        text_block(wrapped(copy["demographic_desc"]), 72, 140, "subtitle").rstrip(),
        f'  <rect x="72" y="164" width="1092" height="438" rx="18" fill="{COLORS["navy_2"]}" stroke="{COLORS["grid"]}"/>',
    ]
    for tick in (40, 60, 80, 100):
        y = y1 - (tick - min_index) / (max_index - min_index) * (y1 - y0)
        body.extend(
            [
                f'  <line x1="{x0}" y1="{y:.2f}" x2="{x1}" y2="{y:.2f}" stroke="{COLORS["grid"]}" stroke-width="1"/>',
                f'  <text class="small" x="98" y="{y + 5:.2f}" text-anchor="end">{tick}</text>',
            ]
        )
    for year in (2013, 2020, 2025, 2030, 2040, 2050):
        x = x0 + (year - 2013) / (2050 - 2013) * (x1 - x0)
        body.append(
            f'  <text class="small" x="{x:.2f}" y="594" text-anchor="middle">{year}</text>'
        )
    x_2025 = x0 + (2025 - 2013) / (2050 - 2013) * (x1 - x0)
    body.extend(
        [
            f'  <rect x="{x_2025:.2f}" y="190" width="{x1 - x_2025:.2f}" height="380" fill="url(#projection-hatch)"/>',
            f'  <line x1="{x_2025:.2f}" y1="180" x2="{x_2025:.2f}" y2="575" stroke="{COLORS["amber"]}" stroke-width="2" stroke-dasharray="7 7"/>',
            f'  <text class="tiny" x="{x_2025 - 10:.2f}" y="558" text-anchor="end" fill="{COLORS["amber"]}">{esc(copy["projection_boundary"])}</text>',
            f'  <polyline points="{polyline([xy(row) for row in estimate])}" fill="none" stroke="{COLORS["cyan"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>',
            f'  <polyline points="{polyline([xy(row) for row in projection])}" fill="none" stroke="{COLORS["lime"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="11 9"/>',
        ]
    )
    by_year = {int(row["year"]): row for row in selected}
    for year in (2025, 2030, 2035, 2050):
        row = by_year[year]
        x, y = xy(row)
        population = int(row["population_age_6_17"])
        millions = fmt_decimal(population / 1_000_000, 2, lang)
        suffix = "millones" if lang == "es" else "million"
        anchor = "end" if year == 2050 else "middle"
        dx = -8 if year == 2050 else 0
        body.extend(
            [
                f'  <circle cx="{x:.2f}" cy="{y:.2f}" r="7" fill="{COLORS["navy"]}" stroke="{COLORS["lime"]}" stroke-width="4"/>',
                f'  <text class="small" x="{x + dx:.2f}" y="{y - 16:.2f}" text-anchor="{anchor}" fill="{COLORS["ink"]}">{year} · {millions} {suffix}</text>',
            ]
        )
    body.extend(
        [
            f'  <rect x="746" y="226" width="350" height="102" rx="14" fill="{COLORS["navy_3"]}" stroke="{COLORS["magenta"]}" filter="url(#soft-shadow)"/>',
            f'  <text x="770" y="270" fill="{COLORS["magenta"]}" font-size="34" font-weight="780">{esc(copy["demographic_callout"])}</text>',
            f'  <text class="small" x="770" y="300">{esc(copy["demographic_callout_detail"])}</text>',
            f'  <line x1="84" y1="630" x2="130" y2="630" stroke="{COLORS["cyan"]}" stroke-width="5"/>',
            f'  <text class="small" x="140" y="635">{esc(copy["estimate"])}</text>',
            f'  <line x1="350" y1="630" x2="396" y2="630" stroke="{COLORS["lime"]}" stroke-width="5" stroke-dasharray="10 8"/>',
            f'  <text class="small" x="406" y="635">{esc(copy["projection"])}</text>',
            f'  <text class="small" x="1128" y="635" text-anchor="end">{esc(copy["not_enrolment"])}</text>',
            f'  <text class="tiny" x="72" y="680">{esc(copy["demographic_source"])}</text>',
        ]
    )
    return svg_shell(copy["demographic_title"], copy["demographic_desc"], "\n".join(body))


def render_trajectory(
    rows: Sequence[Mapping[str, str]], lang: str, outcome: str
) -> str:
    copy = TEXT[lang]
    outcome_key = "simce" if outcome == "simce_relative" else "admission"
    title = copy[f"trajectory_{outcome_key}_title"]
    desc = copy[f"trajectory_{outcome_key}_desc"]
    subset = [row for row in rows if row["outcome"] == outcome]
    y_min, y_max = -1.0, 0.4
    panel_specs = (
        ("exit", copy["exit_panel"], (-3, -2, -1), 72.0, COLORS["magenta"]),
        ("entry", copy["entry_panel"], (0, 1, 2), 626.0, COLORS["lime"]),
    )
    body = [
        f'  <text class="kicker" x="72" y="64">POST II · {esc(copy[outcome_key].upper())}</text>',
        f'  <text class="title" x="72" y="110">{esc(title)}</text>',
        text_block(wrapped(desc), 72, 140, "subtitle").rstrip(),
    ]

    def y_position(value: float) -> float:
        return 520.0 - (value - y_min) / (y_max - y_min) * 300.0

    for branch, panel_title, years, panel_x, color in panel_specs:
        width = 502.0
        body.extend(
            [
                f'  <rect x="{panel_x}" y="186" width="{width}" height="408" rx="18" fill="{COLORS["navy_2"]}" stroke="{COLORS["grid"]}"/>',
                f'  <text class="label" x="{panel_x + 24}" y="210" font-weight="720">{esc(panel_title)}</text>',
            ]
        )
        for tick in (-1.0, -0.5, 0.0):
            y = y_position(tick)
            body.append(
                f'  <line x1="{panel_x + 72}" y1="{y:.2f}" x2="{panel_x + width - 28}" y2="{y:.2f}" stroke="{COLORS["grid"]}" stroke-width="{2 if tick == 0 else 1}" {"stroke-dasharray=\"5 6\"" if tick == 0 else ""}/>'
            )
            body.append(
                f'  <text class="tiny" x="{panel_x + 60}" y="{y + 4:.2f}" text-anchor="end">{fmt_decimal(tick, 1, lang)}</text>'
            )
        panel_rows = {
            int(row["relative_year"]): row for row in subset if row["branch"] == branch
        }
        points = []
        for index, year in enumerate(years):
            row = panel_rows[year]
            x = panel_x + 116 + index * 160
            estimate = float(row["estimate"])
            y = y_position(estimate)
            year_label = f"t−{abs(year)}" if year < 0 else f"t+{year}" if year > 0 else "t0"
            points.append((x, y))
            if row["status"] == "ESTIMATED":
                low_y = y_position(float(row["ci95_low"]))
                high_y = y_position(float(row["ci95_high"]))
                body.extend(
                    [
                        f'  <line x1="{x}" y1="{low_y:.2f}" x2="{x}" y2="{high_y:.2f}" stroke="{color}" stroke-width="5"/>',
                        f'  <line x1="{x - 11}" y1="{low_y:.2f}" x2="{x + 11}" y2="{low_y:.2f}" stroke="{color}" stroke-width="4"/>',
                        f'  <line x1="{x - 11}" y1="{high_y:.2f}" x2="{x + 11}" y2="{high_y:.2f}" stroke="{color}" stroke-width="4"/>',
                        f'  <circle cx="{x}" cy="{y:.2f}" r="9" fill="{COLORS["navy"]}" stroke="{color}" stroke-width="5"/>',
                    ]
                )
            else:
                body.extend(
                    [
                        f'  <rect x="{x - 12}" y="{y - 12:.2f}" width="24" height="24" rx="4" fill="none" stroke="{COLORS["amber"]}" stroke-width="3"/>',
                        f'  <line x1="{x - 8}" y1="{y - 8:.2f}" x2="{x + 8}" y2="{y + 8:.2f}" stroke="{COLORS["amber"]}" stroke-width="3"/>',
                        f'  <line x1="{x + 8}" y1="{y - 8:.2f}" x2="{x - 8}" y2="{y + 8:.2f}" stroke="{COLORS["amber"]}" stroke-width="3"/>',
                    ]
                )
            body.extend(
                [
                    f'  <text class="small" x="{x}" y="542" text-anchor="middle">{year_label}</text>',
                    f'  <text x="{x}" y="562" text-anchor="middle" fill="{COLORS["muted"]}" font-size="11">N={int(row["units"])}</text>',
                    f'  <text x="{x}" y="579" text-anchor="middle" fill="{COLORS["muted"]}" font-size="11">{esc(row["regimes"])}</text>',
                    f'  <text x="{x}" y="{max(236, y - 19):.2f}" text-anchor="middle" fill="{color if row["status"] == "ESTIMATED" else COLORS["amber"]}" font-size="13" font-weight="700">{fmt_decimal(estimate, 2, lang, signed=True)}</text>',
                ]
            )
        body.append(
            f'  <polyline points="{polyline(points)}" fill="none" stroke="{color}" stroke-width="2" stroke-dasharray="4 8" opacity="0.55"/>'
        )
    body.extend(
        [
            f'  <circle cx="88" cy="620" r="7" fill="{COLORS["navy"]}" stroke="{COLORS["cyan"]}" stroke-width="4"/>',
            f'  <text class="small" x="106" y="625">{esc(copy["estimated"])}</text>',
            f'  <rect x="360" y="612" width="16" height="16" rx="3" fill="none" stroke="{COLORS["amber"]}" stroke-width="2"/>',
            f'  <line x1="363" y1="615" x2="373" y2="625" stroke="{COLORS["amber"]}" stroke-width="2"/>',
            f'  <line x1="373" y1="615" x2="363" y2="625" stroke="{COLORS["amber"]}" stroke-width="2"/>',
            f'  <text class="small" x="387" y="625">{esc(copy["not_estimable"])}</text>',
            f'  <text class="small" x="1128" y="625" text-anchor="end">{esc(copy["changing_support"])}</text>',
            f'  <text class="small" x="72" y="654">{esc(copy["comparison_direction"])}</text>',
            f'  <text class="tiny" x="72" y="680">{esc(copy["trajectory_source"])}</text>',
        ]
    )
    return svg_shell(title, desc, "\n".join(body))


def marker(x: float, y: float, color: str) -> str:
    return "\n".join(
        [
            f'  <circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="{COLORS["navy"]}" stroke="{color}" stroke-width="3"/>',
            f'  <line x1="{x - 6:.1f}" y1="{y:.1f}" x2="{x + 6:.1f}" y2="{y:.1f}" stroke="{color}" stroke-width="3"/>',
            f'  <line x1="{x:.1f}" y1="{y - 6:.1f}" x2="{x:.1f}" y2="{y + 6:.1f}" stroke="{color}" stroke-width="3"/>',
        ]
    )


def render_map_legacy(
    row: Mapping[str, str],
    case_rows: Sequence[Mapping[str, str]],
    lang: str,
) -> str:
    copy = TEXT[lang]
    commune = row["commune"]
    title = copy["map_title"].format(commune=commune)
    desc = copy["map_desc"].format(commune=commune)
    center_x, center_y = 338.0, 358.0
    bands = (
        (int(row["within_2km"]), 78.0, -70.0, "0–2 km"),
        (int(row["from_2_to_5km"]), 150.0, 135.0, "2–5 km"),
        (int(row["from_5_to_10km"]), 222.0, 0.0, "5–10 km"),
    )
    body = [
        f'  <text class="kicker" x="72" y="60">{esc(copy["schematic"])}</text>',
        f'  <text class="title" x="72" y="106">{esc(title)}</text>',
        f'  <text class="subtitle" x="72" y="136">{esc(copy["selection"])}</text>',
        f'  <rect x="72" y="164" width="552" height="418" rx="18" fill="{COLORS["navy_2"]}" stroke="{COLORS["grid"]}"/>',
        f'  <rect x="648" y="164" width="480" height="244" rx="18" fill="{COLORS["navy_2"]}" stroke="{COLORS["grid"]}"/>',
    ]
    for radius, label in ((78, "2 km"), (150, "5 km"), (222, "10 km")):
        body.extend(
            [
                f'  <circle cx="{center_x}" cy="{center_y}" r="{radius}" fill="none" stroke="{COLORS["cyan"]}" stroke-width="2" stroke-dasharray="7 8" opacity="0.65"/>',
                f'  <text class="tiny" x="{center_x + radius - 7}" y="{center_y + 2}" text-anchor="end" fill="{COLORS["cyan"]}">{label}</text>',
            ]
        )
    body.extend(
        [
            f'  <rect x="{center_x - 32}" y="{center_y - 32}" width="64" height="64" rx="10" fill="{COLORS["navy"]}" stroke="{COLORS["magenta"]}" stroke-width="5"/>',
            f'  <line x1="{center_x - 18}" y1="{center_y - 18}" x2="{center_x + 18}" y2="{center_y + 18}" stroke="{COLORS["magenta"]}" stroke-width="5"/>',
            f'  <line x1="{center_x + 18}" y1="{center_y - 18}" x2="{center_x - 18}" y2="{center_y + 18}" stroke="{COLORS["magenta"]}" stroke-width="5"/>',
            f'  <text class="number" x="{center_x}" y="{center_y + 61}" text-anchor="middle">{int(row["paired_closures"])} {esc(copy["closure_group"])}</text>',
        ]
    )
    for band_index, (count, radius, base_angle, label) in enumerate(bands):
        for index in range(count):
            angle = math.radians(base_angle + (index - (count - 1) / 2) * 20)
            marker_x = center_x + radius * math.cos(angle)
            marker_y = center_y + radius * math.sin(angle)
            body.append(marker(marker_x, marker_y, COLORS["lime"]))
        label_y = 200 + band_index * 34
        body.append(
            f'  <text class="small" x="92" y="{label_y}">{label} · {esc(copy["radius_pairs"].format(count=count))}</text>'
        )
    metrics = (
        (copy["unique_entries"], str(int(row["nearby_entries"])), COLORS["lime"]),
        (copy["median_distance"], f'{fmt_decimal(float(row["median_distance_km"]), 1, lang)} km', COLORS["cyan"]),
        (copy["same_commune"], str(int(row["same_commune_pairs"])), COLORS["magenta"]),
        (copy["period"], display_period(row["event_period"]), COLORS["amber"]),
    )
    for index, (label, value, color) in enumerate(metrics):
        x = 676 + (index % 2) * 218
        y = 206 + (index // 2) * 96
        body.extend(
            [
                f'  <text class="small" x="{x}" y="{y}">{esc(label)}</text>',
                f'  <text x="{x}" y="{y + 35}" fill="{color}" font-size="28" font-weight="780">{esc(value)}</text>',
            ]
        )
    body.extend(
        [
            f'  <text class="tiny" x="92" y="552">{esc(copy["pair_legend"])}</text>',
            f'  <text class="tiny" x="338" y="552">{esc(copy["closure_legend"])}</text>',
            f'  <rect x="648" y="432" width="480" height="150" rx="18" fill="{COLORS["navy_2"]}" stroke="{COLORS["grid"]}"/>',
            f'  <text class="label" x="676" y="466" font-weight="720">{esc(copy["outcome_strip"])}</text>',
        ]
    )
    years = (-2, -1, 0, 1, 2)
    labels = ("t−2", "t−1", "t0", "t+1", "t+2")
    simce_by_year = {
        int(item["relative_year"]): item
        for item in case_rows
        if item["outcome"] == "simce_relative"
    }
    published_labels: list[str] = []
    for index, (year, year_label) in enumerate(zip(years, labels, strict=True)):
        item = simce_by_year[year]
        x = 692 + index * 83
        body.append(
            f'  <text class="tiny" x="{x}" y="496" text-anchor="middle">{year_label}</text>'
        )
        if item["status"] == "PUBLISHED":
            estimate = fmt_decimal(float(item["estimate"]), 3, lang, signed=True)
            published_labels.append(f"{year_label}: {estimate} · N={int(float(item['units']))}")
            body.extend(
                [
                    f'  <circle cx="{x}" cy="520" r="9" fill="{COLORS["lime"]}"/>',
                ]
            )
        else:
            body.extend(
                [
                    f'  <rect x="{x - 8}" y="512" width="16" height="16" rx="3" fill="none" stroke="{COLORS["amber"]}" stroke-width="2"/>',
                ]
            )
    outcome_note = " · ".join(published_labels)
    if outcome_note:
        body.append(
            f'  <text class="tiny" x="676" y="564" fill="{COLORS["lime"]}">{esc(outcome_note)}</text>'
        )
        body.append(
            f'  <text class="tiny" x="1104" y="564" text-anchor="end">□ = {esc(copy["suppressed"])}</text>'
        )
    else:
        body.append(
            f'  <text class="tiny" x="890" y="564" text-anchor="middle">□ = {esc(copy["suppressed"])}</text>'
        )
    body.extend(
        [
            f'  <text class="small" x="72" y="626">{esc(copy["local_caveat"])}</text>',
            f'  <text class="tiny" x="72" y="676">{esc(copy["map_source"])}</text>',
        ]
    )
    return svg_shell(title, desc, "\n".join(body))


def labeled_map_points(
    points: Sequence[Mapping[str, str]], lang: str
) -> list[tuple[Mapping[str, str], str]]:
    role_order = {"closure": 0, "entry": 1}
    ordered = sorted(
        points,
        key=lambda point: (
            role_order[point["role"]],
            int(point["event_year"]),
            int(point["rbd"]),
        ),
    )
    counters = {"closure": 0, "entry": 0}
    prefixes = {"closure": "C", "entry": "A" if lang == "es" else "O"}
    result: list[tuple[Mapping[str, str], str]] = []
    for point in ordered:
        counters[point["role"]] += 1
        result.append((point, f"{prefixes[point['role']]}{counters[point['role']]}") )
    return result


def render_map(
    row: Mapping[str, str],
    points: Sequence[Mapping[str, str]],
    links: Sequence[Mapping[str, str]],
    lang: str,
) -> str:
    """Render official school points and deterministic proximity links."""

    copy = TEXT[lang]
    commune = row["commune"]
    title = copy["map_title"].format(commune=commune)
    desc = copy["map_desc"].format(commune=commune)
    if not points or not links:
        raise ValueError(f"caso cartográfico sin puntos o enlaces: {commune}")
    x0, x1, y0, y1 = 78.0, 716.0, 160.0, 618.0
    lons = [float(point["longitude"]) for point in points]
    lats = [float(point["latitude"]) for point in points]
    lon_pad = max((max(lons) - min(lons)) * 0.1, 0.004)
    lat_pad = max((max(lats) - min(lats)) * 0.1, 0.004)
    lon_min, lon_max = min(lons) - lon_pad, max(lons) + lon_pad
    lat_min, lat_max = min(lats) - lat_pad, max(lats) + lat_pad

    def xy(point: Mapping[str, str]) -> tuple[float, float]:
        x = x0 + (float(point["longitude"]) - lon_min) / (lon_max - lon_min) * (x1 - x0)
        y = y1 - (float(point["latitude"]) - lat_min) / (lat_max - lat_min) * (y1 - y0)
        return x, y

    labeled_points = labeled_map_points(points, lang)
    ordered = [point for point, _label in labeled_points]
    labels = {
        (point["role"], int(point["rbd"])): label
        for point, label in labeled_points
    }
    by_key = {(point["role"], int(point["rbd"])): point for point in points}
    case_label = "CASO COMUNAL" if lang == "es" else "COMMUNE CASE"
    directory_label = "DIRECTORIO OFICIAL MINEDUC" if lang == "es" else "OFFICIAL MINEDUC DIRECTORY"
    school_label = "ESTABLECIMIENTOS" if lang == "es" else "SCHOOLS"
    body = [
        f'  <rect x="0" y="0" width="12" height="720" fill="{COLORS["cyan"]}"/>',
        f'  <text class="kicker" x="54" y="46">{case_label} · {int(row["selection_rank"]):02d}</text>',
        f'  <text class="map-title" x="54" y="91">{esc(commune)}</text>',
        f'  <text class="map-small" x="1146" y="54" text-anchor="end" fill="{COLORS["lime"]}">{esc(directory_label)}</text>',
        f'  <line x1="54" y1="110" x2="1146" y2="110" stroke="{COLORS["grid"]}" stroke-width="2"/>',
        f'  <rect x="54" y="136" width="684" height="510" fill="{COLORS["navy_2"]}" stroke="{COLORS["grid"]}"/>',
        f'  <rect x="766" y="136" width="380" height="510" fill="{COLORS["navy_2"]}" stroke="{COLORS["grid"]}"/>',
        f'  <text class="tiny" x="786" y="160" fill="{COLORS["cyan"]}">{school_label}</text>',
    ]
    for index in range(5):
        x = x0 + index / 4 * (x1 - x0)
        lon = lon_min + index / 4 * (lon_max - lon_min)
        body.extend(
            [
                f'  <line x1="{x:.2f}" y1="{y0}" x2="{x:.2f}" y2="{y1}" stroke="{COLORS["grid"]}" opacity="0.42"/>',
                f'  <text class="tiny" x="{x:.2f}" y="638" text-anchor="middle">{lon:.3f}°</text>',
            ]
        )
    for index in range(5):
        y = y0 + index / 4 * (y1 - y0)
        lat = lat_max - index / 4 * (lat_max - lat_min)
        body.extend(
            [
                f'  <line x1="{x0}" y1="{y:.2f}" x2="{x1}" y2="{y:.2f}" stroke="{COLORS["grid"]}" opacity="0.42"/>',
                f'  <text class="tiny" x="68" y="{y + 4:.2f}" text-anchor="end">{lat:.3f}°</text>',
            ]
        )
    body.extend(
        [
            f'  <text class="tiny" x="700" y="156" text-anchor="end" fill="{COLORS["cyan"]}">N ↑</text>',
            f'  <text class="tiny" x="82" y="156">{esc(copy["schematic"])}</text>',
        ]
    )
    for link in links:
        closure = by_key[("closure", int(link["closure_rbd"]))]
        entry = by_key[("entry", int(link["entry_rbd"]))]
        cx, cy = xy(closure)
        ex, ey = xy(entry)
        body.append(
            f'  <line x1="{cx:.2f}" y1="{cy:.2f}" x2="{ex:.2f}" y2="{ey:.2f}" stroke="{COLORS["cyan"]}" stroke-width="2" stroke-dasharray="7 7" opacity="0.38"><title>{esc(labels[("closure", int(link["closure_rbd"]))])} → {esc(labels[("entry", int(link["entry_rbd"]))])} · {float(link["distance_km"]):.1f} km</title></line>'
        )
    label_positions: dict[tuple[str, int], tuple[float, float]] = {}
    occupied: list[tuple[float, float, float, float]] = []
    candidates = ((18, -10), (18, 24), (-38, -10), (-38, 24), (-8, -25), (-8, 38))
    for point in ordered:
        point_x, point_y = xy(point)
        key = (point["role"], int(point["rbd"]))
        label = labels[key]
        width = 8 + len(label) * 7
        selected_position: tuple[float, float] | None = None
        for offset_x, offset_y in candidates:
            label_x = min(max(point_x + offset_x, x0 + 4), x1 - width - 4)
            label_y = min(max(point_y + offset_y, y0 + 16), y1 - 4)
            box = (label_x, label_y - 12, label_x + width, label_y + 2)
            if all(
                box[2] + 3 <= other[0]
                or box[0] >= other[2] + 3
                or box[3] + 3 <= other[1]
                or box[1] >= other[3] + 3
                for other in occupied
            ):
                selected_position = (label_x, label_y)
                occupied.append(box)
                break
        if selected_position is None:
            raise ValueError(f"no hay posición sin colisión para {label} en {commune}")
        label_positions[key] = selected_position

    for point in ordered:
        x, y = xy(point)
        role = point["role"]
        color = COLORS["magenta"] if role == "closure" else COLORS["lime"]
        label = labels[(role, int(point["rbd"]))]
        label_x, label_y = label_positions[(role, int(point["rbd"]))]
        body.append(
            f'  <g><title>{esc(label)} · RBD {int(point["rbd"])} · {esc(point["school_name"])} · {int(point["event_year"])}</title>'
        )
        body.append(
            f'    <circle cx="{x:.2f}" cy="{y:.2f}" r="13" fill="{COLORS["navy"]}" stroke="{color}" stroke-width="3"/>'
        )
        if role == "closure":
            body.extend(
                [
                    f'    <line x1="{x - 6:.2f}" y1="{y - 6:.2f}" x2="{x + 6:.2f}" y2="{y + 6:.2f}" stroke="{color}" stroke-width="3"/>',
                    f'    <line x1="{x + 6:.2f}" y1="{y - 6:.2f}" x2="{x - 6:.2f}" y2="{y + 6:.2f}" stroke="{color}" stroke-width="3"/>',
                ]
            )
        else:
            body.extend(
                [
                    f'    <line x1="{x - 7:.2f}" y1="{y:.2f}" x2="{x + 7:.2f}" y2="{y:.2f}" stroke="{color}" stroke-width="3"/>',
                    f'    <line x1="{x:.2f}" y1="{y - 7:.2f}" x2="{x:.2f}" y2="{y + 7:.2f}" stroke="{color}" stroke-width="3"/>',
                ]
            )
        body.extend(
            [
                f'    <line x1="{x:.2f}" y1="{y:.2f}" x2="{label_x:.2f}" y2="{label_y - 5:.2f}" stroke="{color}" stroke-width="1" opacity="0.8"/>',
                f'    <text x="{label_x:.2f}" y="{label_y:.2f}" fill="{color}" font-size="11" font-weight="780">{esc(label)}</text></g>',
            ]
        )

    for index, point in enumerate(ordered):
        role = point["role"]
        color = COLORS["magenta"] if role == "closure" else COLORS["lime"]
        label = labels[(role, int(point["rbd"]))]
        y = 184 + index * 38
        name = str(point["school_name"])
        short_name = name if len(name) <= 35 else f"{name[:33].rstrip()}…"
        body.extend(
            [
                f'  <text x="786" y="{y}" fill="{color}" font-size="12" font-weight="780">{esc(label)}</text>',
                f'  <text class="tiny" x="818" y="{y}">RBD {int(point["rbd"])} · {int(point["event_year"])}</text>',
                f'  <text x="818" y="{y + 16}" fill="{COLORS["ink"]}" font-size="11">{esc(short_name)}</text>',
            ]
        )
    body.extend(
        [
            f'  <text class="tiny" x="54" y="680"><tspan fill="{COLORS["magenta"]}">{esc(copy["closure_legend"])}</tspan><tspan dx="24" fill="{COLORS["lime"]}">{esc(copy["pair_legend"])}</tspan></text>',
            f'  <text class="tiny" x="1146" y="680" text-anchor="end">{esc(copy["map_source"])}</text>',
        ]
    )
    return svg_shell(title, desc, "\n".join(body))


def render_author_case_map(case: Mapping[str, Any], lang: str) -> str:
    title = (
        "El Salvador: cierre y fusión documentados"
        if lang == "es"
        else "El Salvador: a documented closure and merger"
    )
    desc = (
        "Esquema de la Escuela N° 14 y la Escuela N° 1, separadas por 0,449 kilómetros, con matrícula agregada antes y después de la fusión."
        if lang == "es"
        else "Diagram of School No. 14 and School No. 1, 0.449 kilometres apart, with aggregate enrolment before and after the merger."
    )
    copy = {
        "es": {
            "eyebrow": "CASO DEL AUTOR · FUERA DE LA SELECCIÓN SISTEMÁTICA",
            "closure": "Escuela N° 14 · RBD 391",
            "closure_detail": "Óscar Yáñez Pastén · cerró al terminar 2013",
            "receiver": "Escuela N° 1 · RBD 390",
            "receiver_detail": "La Mina · Diego Portales 1510 · receptora documentada",
            "relationship": "fusión documentada · 0,449 km",
            "legend": "× cierre · R escuela receptora",
            "m1": "1.399",
            "l1": "matrículas conjuntas · 2004",
            "m2": "977",
            "l2": "matrículas conjuntas · 2013",
            "m3": "−30,2 %",
            "l3": "cambio conjunto · 2004–2013",
            "m4": "738",
            "l4": "matrículas Escuela N° 1 · 2014",
            "note": "La caída previa es compatible con contracción demográfica; no prueba el motivo administrativo del cierre.",
            "source": "BCN 2014 · FEES · Directorio y matrícula MINEDUC",
        },
        "en": {
            "eyebrow": "AUTHOR CASE · OUTSIDE THE SYSTEMATIC SELECTION",
            "closure": "School No. 14 · RBD 391",
            "closure_detail": "Óscar Yáñez Pastén · closed at the end of 2013",
            "receiver": "School No. 1 · RBD 390",
            "receiver_detail": "La Mina · 1510 Diego Portales · documented receiver",
            "relationship": "documented merger · 0.449 km",
            "legend": "× closure · R receiving school",
            "m1": "1,399",
            "l1": "combined enrolment · 2004",
            "m2": "977",
            "l2": "combined enrolment · 2013",
            "m3": "−30.2%",
            "l3": "combined change · 2004–2013",
            "m4": "738",
            "l4": "School No. 1 enrolment · 2014",
            "note": "The preceding decline is consistent with demographic contraction; it does not prove the administrative motive for closure.",
            "source": "BCN 2014 · FEES · MINEDUC directory and enrolment",
        },
    }[lang]
    cards = [
        (copy["m1"], copy["l1"], 152),
        (copy["m2"], copy["l2"], 262),
        (copy["m3"], copy["l3"], 372),
        (copy["m4"], copy["l4"], 482),
    ]
    metadata = json.dumps(
        {
            "case_id": case["case_id"],
            "status": case["status"],
            "systematic_sample_member": case["selection"]["systematic_sample_member"],
            "closure_rbd": case["schools"]["closure"]["rbd"],
            "receiver_rbd": case["schools"]["receiver"]["rbd"],
            "receiver_coordinate_year": case["schools"]["receiver"]["coordinate_reference_year"],
            "coordinate_caveat": case["schools"]["coordinate_caveat"],
            "sources": [row["url"] for row in case["documentary_sources"]],
            "not_verified": case["epistemic_register"]["not_verified"],
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    card_svg = "\n".join(
        f'''  <g><rect x="770" y="{y}" width="374" height="88" rx="12" fill="#fffaf0" stroke="#a9b9c9"/>
    <text x="794" y="{y + 37}" class="metric">{esc(metric)}</text>
    <text x="794" y="{y + 63}" class="label">{esc(label)}</text></g>'''
        for metric, label, y in cards
    )
    svg_id = f"el-salvador-{lang}"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="720" viewBox="0 0 1200 720" role="img" aria-labelledby="{svg_id}-title {svg_id}-desc">
  <title id="{svg_id}-title">{esc(title)}</title>
  <desc id="{svg_id}-desc">{esc(desc)}</desc>
  <metadata>{esc(metadata)}</metadata>
  <defs>
    <pattern id="rules-{lang}" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M0 27.5H28" stroke="#94c5df" stroke-opacity=".25"/></pattern>
    <style>
      text {{ font-family: "Fira Sans", "Inter", "Aptos", sans-serif; fill: #26354c; }}
      .eyebrow {{ font-size: 13px; font-weight: 800; letter-spacing: 1.5px; fill: #096b83; }}
      .title {{ font-size: 29px; font-weight: 800; }}
      .school {{ font-size: 17px; font-weight: 800; }}
      .detail {{ font-size: 13px; fill: #566477; }}
      .metric {{ font-size: 27px; font-weight: 800; fill: #096b83; }}
      .label {{ font-size: 13px; fill: #566477; }}
      .note {{ font-size: 14px; font-weight: 650; }}
      .source {{ font-size: 11px; fill: #566477; }}
      .receiver-marker {{ font-size: 21px; font-weight: 850; fill: #096b83; }}
    </style>
  </defs>
  <rect width="1200" height="720" fill="#fbf5e8"/>
  <rect width="1200" height="720" fill="url(#rules-{lang})"/>
  <line x1="46" y1="0" x2="46" y2="720" stroke="#c74e5c" stroke-opacity=".42"/>
  <text x="76" y="48" class="eyebrow">{esc(copy["eyebrow"])}</text>
  <text x="76" y="84" class="title">{esc(title)}</text>
  <rect x="58" y="122" width="682" height="448" rx="16" fill="#eef3ef" stroke="#a9b9c9"/>
  <path d="M202 422 C315 360 420 303 574 244" fill="none" stroke="#16738a" stroke-width="4" stroke-dasharray="10 9"/>
  <text x="328" y="318" class="detail">{esc(copy["relationship"])}</text>
  <circle cx="202" cy="422" r="22" fill="#fffaf0" stroke="#b74765" stroke-width="5"/>
  <path d="M191 411l22 22M213 411l-22 22" stroke="#b74765" stroke-width="5"/>
  <text x="88" y="474" class="school">{esc(copy["closure"])}</text>
  <text x="88" y="498" class="detail">{esc(copy["closure_detail"])}</text>
  <rect x="552" y="222" width="44" height="44" rx="8" fill="#fffaf0" stroke="#096b83" stroke-width="5"/>
  <text x="574" y="252" text-anchor="middle" class="receiver-marker">R</text>
  <text x="466" y="184" class="school">{esc(copy["receiver"])}</text>
  <text x="410" y="208" class="detail">{esc(copy["receiver_detail"])}</text>
  <text x="80" y="528" class="detail">{esc(copy["legend"])}</text>
  <text x="80" y="552" class="source">{esc(desc)}</text>
{card_svg}
  <rect x="58" y="600" width="1086" height="58" rx="10" fill="#fffaf0" stroke="#b74765" stroke-width="2"/>
  <text x="82" y="626" class="note">{esc(copy["note"])}</text>
  <text x="82" y="647" class="source">{esc(copy["source"])}</text>
</svg>
'''


def asset_path(name: str) -> str:
    return f"/assets/images/extender-tesis-no-es-agregar-anos/{name}"


def render_map_data(
    data: Mapping[str, Sequence[Mapping[str, str]]],
    author_case: Mapping[str, Any],
) -> bytes:
    cases: list[dict[str, Any]] = []
    for summary in data["spatial"]:
        case_key = summary["case"]
        points = [
            {
                "role": point["role"],
                "rbd": int(point["rbd"]),
                "name": point["school_name"],
                "event_year": int(point["event_year"]),
                "coordinate_year": int(point["coordinate_year"]),
                "location_lag_years": int(point["location_lag_years"]),
                "latitude": float(point["latitude"]),
                "longitude": float(point["longitude"]),
                "market_segment": point["market_segment"],
                "source_url": point["official_source_url"],
            }
            for point in data["school_points"]
            if point["case"] == case_key
        ]
        links = [
            {
                "closure_rbd": int(link["closure_rbd"]),
                "entry_rbd": int(link["entry_rbd"]),
                "closure_year": int(link["closure_year"]),
                "entry_year": int(link["entry_year"]),
                "entry_coordinate_year": int(link["entry_coordinate_year"]),
                "location_lag_years": int(link["location_lag_years"]),
                "distance_km": float(link["distance_km"]),
                "market_segment": link["market_segment"],
            }
            for link in data["school_links"]
            if link["case"] == case_key
        ]
        trajectories = []
        for row in data["case_trajectory"]:
            if row["case"] != case_key:
                continue
            estimate = row["estimate"].strip()
            trajectories.append(
                {
                    "branch": row["branch"],
                    "outcome": row["outcome"],
                    "relative_year": int(row["relative_year"]),
                    "status": row["status"],
                    "estimate": float(estimate) if estimate else None,
                    "units": int(row["units"]),
                    "minimum_units": int(row["minimum_units"]),
                    "regime": row["regimes"],
                }
            )
        family_labels = {
            "initial": ("educación inicial", "pre-primary"),
            "basic": ("educación básica", "primary"),
            "secondary": ("educación media", "secondary"),
        }
        family_es, family_en = family_labels.get(
            summary["segment_family"],
            (summary["segment_family"], summary["segment_family"]),
        )
        selection_note_es = (
            f"Ejemplo de la familia {family_es}; dentro de ella se "
            "ordenó por misma comuna, distancia, año y RBD. Ni valores ni disponibilidad "
            "de resultados participaron"
        )
        selection_note_en = (
            f"Example from the {family_en} family; within-family ordering "
            "used same-commune status, distance, year, and RBD. Neither outcome values nor "
            "outcome availability were used"
        )
        cases.append(
            {
                "id": slug(summary["commune"]),
                "case": case_key,
                "case_kind": "systematic",
                "selection_rank": int(summary["selection_rank"]),
                "selection_note_es": selection_note_es,
                "selection_note_en": selection_note_en,
                "commune": summary["commune"],
                "event_period": display_period(summary["event_period"]),
                "education_segment": summary["education_segment"],
                "segment_family": summary["segment_family"],
                "distance_km": float(summary["median_distance_km"]),
                "distance_band": summary["distance_band"],
                "same_commune": bool(int(summary["same_commune_pairs"])),
                "poster_es": asset_path(
                    f"estilizada-mapa-{slug(summary['commune'])}-es.svg"
                ),
                "poster_en": asset_path(
                    f"estilizada-mapa-{slug(summary['commune'])}-en.svg"
                ),
                "points": points,
                "links": links,
                "trajectories": trajectories,
            }
        )
    schools = author_case["schools"]
    closure = schools["closure"]
    receiver = schools["receiver"]
    enrolment = {int(row["year"]): row for row in author_case["enrollment"]["rows"]}
    mineduc_url = next(
        row["url"]
        for row in author_case["documentary_sources"]
        if row["id"] == "mineduc_open_data"
    )
    cases.append(
        {
            "id": "el-salvador",
            "case": "author-el-salvador",
            "case_kind": "author_documented",
            "selection_rank": None,
            "selection_note_es": "Caso propuesto por el autor; fuera de la selección sistemática",
            "selection_note_en": "Author-proposed case; outside the systematic selection",
            "commune": "El Salvador",
            "event_period": "2013–2014",
            "education_segment": "basic",
            "segment_family": "basic",
            "distance_km": float(schools["geodesic_distance_km"]),
            "distance_band": "under_1_km",
            "same_commune": True,
            "poster_es": asset_path("estilizada-mapa-el-salvador-es.svg"),
            "poster_en": asset_path("estilizada-mapa-el-salvador-en.svg"),
            "points": [
                {
                    "role": "closure",
                    "rbd": int(closure["rbd"]),
                    "name": closure["official_name"],
                    "event_year": 2014,
                    "coordinate_year": int(closure["coordinate_reference_year"]),
                    "location_lag_years": int(closure["coordinate_reference_year"]) - 2014,
                    "latitude": float(closure["latitude"]),
                    "longitude": float(closure["longitude"]),
                    "market_segment": "basic",
                    "source_url": mineduc_url,
                },
                {
                    "role": "receiver",
                    "rbd": int(receiver["rbd"]),
                    "name": receiver["official_name"],
                    "event_year": 2014,
                    "coordinate_year": int(receiver["coordinate_reference_year"]),
                    "location_lag_years": int(receiver["coordinate_reference_year"]) - 2014,
                    "latitude": float(receiver["latitude"]),
                    "longitude": float(receiver["longitude"]),
                    "market_segment": "basic",
                    "source_url": mineduc_url,
                },
            ],
            "links": [
                {
                    "closure_rbd": int(closure["rbd"]),
                    "receiver_rbd": int(receiver["rbd"]),
                    "closure_year": 2014,
                    "receiver_year": 2014,
                    "distance_km": float(schools["geodesic_distance_km"]),
                    "relationship": "documented_merger",
                    "market_segment": "basic",
                }
            ],
            "trajectories": [
                {
                    "branch": "combined",
                    "outcome": "enrollment_total",
                    "calendar_year": 2004,
                    "relative_year": -10,
                    "status": "DESCRIPTIVE",
                    "estimate": int(enrolment[2004]["combined"]),
                    "units": 2,
                    "minimum_units": 1,
                    "regime": "MINEDUC",
                },
                {
                    "branch": "combined",
                    "outcome": "enrollment_total",
                    "calendar_year": 2013,
                    "relative_year": -1,
                    "status": "DESCRIPTIVE",
                    "estimate": int(enrolment[2013]["combined"]),
                    "units": 2,
                    "minimum_units": 1,
                    "regime": "MINEDUC",
                },
                {
                    "branch": "receiver",
                    "outcome": "enrollment_total",
                    "calendar_year": 2014,
                    "relative_year": 0,
                    "status": "DESCRIPTIVE",
                    "estimate": int(enrolment[2014]["receiver_rbd_390"]),
                    "units": 1,
                    "minimum_units": 1,
                    "regime": "MINEDUC",
                },
                {
                    "branch": "receiver",
                    "outcome": "enrollment_total",
                    "calendar_year": 2025,
                    "relative_year": 11,
                    "status": "DESCRIPTIVE",
                    "estimate": int(enrolment[2025]["receiver_rbd_390"]),
                    "units": 1,
                    "minimum_units": 1,
                    "regime": "MINEDUC",
                },
            ],
        }
    )
    payload = {
        "schema_version": 3,
        "generated_by": "scripts/render_thesis_extension_stylized.py",
        "basemap_manifest": "/assets/data/catastro_sii/manifest.json",
        "selection_rule": (
            "first one strict entity-segment pair per preferred education family; within "
            "each family, ranked by same-commune status, distance, year, and stable "
            "identifiers; neither outcome values nor outcome availability were used"
        ),
        "cases": cases,
    }
    return (
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True, allow_nan=False)
        + "\n"
    ).encode()


def render_yaml(
    data: Mapping[str, Sequence[Mapping[str, str]]],
    asset_names: Sequence[str],
    author_case: Mapping[str, Any],
) -> str:
    by_year = {int(row["year"]): row for row in data["demography"]}
    spatial = data["spatial"]
    school_points = data["school_points"]
    trajectory = data["trajectory"]
    locale_copy = {
        "es": {
            "id": "thesis-extension-stylized-es",
            "eyebrow": "Visor de evidencia · Chile 2013–2025",
            "title": "Dos casos seleccionados, una fusión y una cautela",
            "intro": "Empiece por los casos territoriales. Después contraste la presión demográfica y las trayectorias nacionales sin confundir cercanía con destino ni descripción con causalidad.",
            "open": "Abrir SVG en HD",
            "enlarge": "Ampliar figura",
            "instructions": "Elija una lámina o use las flechas. Toque la figura para ampliarla.",
            "status_template": "Figura %current% de %total%",
            "controls_label": "Controles del carrusel de evidencia estilizada",
            "previous": "Figura anterior",
            "next": "Figura siguiente",
            "go_to": "Ir a la figura",
            "of": "de",
            "figure": "Figura",
            "map_case": "Caso comunal",
            "demographic_case": "Demografía",
            "trajectory_case": "Trayectoria nacional",
            "admission_tab": "Admisión",
            "demographic_heading": "La población en edad escolar se contrae",
            "demographic_caption": "La población de 6 a 17 años pasa de 3,08 millones en 2025 a 1,37 millones en 2050: una caída proyectada de 55,7 %. No es una predicción de matrícula ni de cierres.",
            "maps_heading": "Dos ejemplos sistemáticos y una fusión documentada",
            "maps_intro": (
                "Primero elegimos un caso por familia educativa preferida; dentro de cada "
                "familia ordenamos por misma comuna, distancia, año y RBD. Ni los valores "
                "ni la disponibilidad de resultados participan. Cada mapa muestra cercanía, "
                "no destino de estudiantes."
            ),
            "schools_heading": "Ver establecimientos y fuente pública",
            "closure_role": "Cierre",
            "entry_role": "Apertura compatible",
            "receiver_role": "Escuela receptora",
            "school_source": "Directorio oficial de establecimientos MINEDUC",
            "author_case_label": "Caso del autor · fuera de la selección sistemática",
            "author_case_title": "El Salvador: una escuela cerró y otra recibió de 1° a 6° básico",
            "author_case_intro": "La Escuela N° 14 Óscar Yáñez Pastén cerró al terminar 2013 y se fusionó con la Escuela N° 1 La Mina. La BCN documentó el traslado de primero a sexto básico.",
            "author_case_caveat": "La matrícula conjunta cayó 30,2 % entre 2004 y 2013. La tendencia es compatible con contracción demográfica, pero no prueba el motivo administrativo del cierre.",
            "author_case_coordinate": "El mapa usa la coordenada oficial 2020 de la Escuela N° 1, coherente con Diego Portales 1510; los directorios anteriores la ubicaban erróneamente en Diego de Almagro.",
            "author_case_alt": "Mapa esquemático de la Escuela N° 14 cerrada y la Escuela N° 1 receptora en El Salvador, con cifras agregadas de matrícula.",
            "author_case_open": "Abrir evidencia estática en HD",
            "author_case_sources": "Fuentes del caso",
            "trajectories_heading": "Resultados académicos con el soporte a la vista",
            "trajectories_intro": "Las salidas y las entradas viven en paneles distintos. N cuenta celdas descriptivas, no el soporte inferencial exacto; las cruces no estimables no son ceros.",
            "method_heading": "Ver los datos detrás de las figuras",
            "data_tables_label": "Valores seleccionados detrás de las figuras",
            "year": "Año",
            "population": "Población 6–17",
            "index": "Índice 2025=100",
            "commune": "Comuna",
            "closures": "Cierres emparejados",
            "entries": "Entradas únicas",
            "same_commune": "Pares en la misma comuna",
            "period": "Periodo",
            "distance": "Distancia del par",
            "branch": "Rama",
            "outcome": "Resultado",
            "relative_year": "Año relativo",
            "estimate": "Estimación",
            "interval": "IC 95 %",
            "n": "N",
            "status": "Estado",
            "regime": "Régimen",
            "exit": "Salida",
            "entry": "Entrada",
            "simce_relative": "SIMCE relativo",
            "admission_core": "Admisión · núcleo",
            "not_estimable": "No estimable",
            "estimated": "Celda descriptiva",
            "segment_labels": {
                "initial": "educación inicial",
                "basic": "educación básica",
                "secondary": "educación media",
            },
        },
        "en": {
            "id": "thesis-extension-stylized-en",
            "eyebrow": "Evidence viewer · Chile 2013–2025",
            "title": "Two selected cases, one merger, and one caution",
            "intro": "Start with the territorial cases. Then compare demographic pressure and national trajectories without confusing proximity with destination or description with causality.",
            "open": "Open HD SVG",
            "enlarge": "Enlarge figure",
            "instructions": "Choose a panel or use the arrows. Tap the figure to enlarge it.",
            "status_template": "Figure %current% of %total%",
            "controls_label": "Stylised-evidence carousel controls",
            "previous": "Previous figure",
            "next": "Next figure",
            "go_to": "Go to figure",
            "of": "of",
            "figure": "Figure",
            "map_case": "Commune case",
            "demographic_case": "Demography",
            "trajectory_case": "National trajectory",
            "admission_tab": "Admissions",
            "demographic_heading": "The school-age population is shrinking",
            "demographic_caption": "The population aged 6–17 falls from 3.08 million in 2025 to 1.37 million in 2050, a projected 55.7% decline. This is not a forecast of enrolment or closures.",
            "maps_heading": "Two systematic examples and one documented merger",
            "maps_intro": (
                "We first choose one case from each preferred education family; within each "
                "family, we order by same-commune status, distance, year, and RBD. Neither "
                "outcome values nor outcome availability are used. Each map shows proximity, "
                "not student destinations."
            ),
            "schools_heading": "View schools and public source",
            "closure_role": "Closure",
            "entry_role": "Compatible opening",
            "receiver_role": "Receiving school",
            "school_source": "Official MINEDUC school directory",
            "author_case_label": "Author case · outside the systematic selection",
            "author_case_title": "El Salvador: one school closed and another received grades 1–6",
            "author_case_intro": "School No. 14 Óscar Yáñez Pastén closed at the end of 2013 and merged with School No. 1 La Mina. The BCN record documents the transfer of grades one through six.",
            "author_case_caveat": "Combined enrolment fell 30.2% between 2004 and 2013. The trend is consistent with demographic contraction, but it does not prove the administrative motive for closure.",
            "author_case_coordinate": "The map uses School No. 1's official 2020 coordinate, consistent with 1510 Diego Portales; earlier directories incorrectly placed it in Diego de Almagro.",
            "author_case_alt": "Schematic map of closed School No. 14 and receiving School No. 1 in El Salvador, with aggregate enrolment figures.",
            "author_case_open": "Open static evidence in HD",
            "author_case_sources": "Case sources",
            "trajectories_heading": "Academic outcomes with support in view",
            "trajectories_intro": "Exits and entries remain in separate panels. N counts descriptive cells, not exact inferential support; non-estimable crosses are not zeroes.",
            "method_heading": "View the data behind the figures",
            "data_tables_label": "Selected values behind the figures",
            "year": "Year",
            "population": "Population aged 6–17",
            "index": "Index 2025=100",
            "commune": "Commune",
            "closures": "Paired closures",
            "entries": "Unique entries",
            "same_commune": "Same-commune pairs",
            "period": "Period",
            "distance": "Pair distance",
            "branch": "Branch",
            "outcome": "Outcome",
            "relative_year": "Relative year",
            "estimate": "Estimate",
            "interval": "95% CI",
            "n": "N",
            "status": "Status",
            "regime": "Regime",
            "exit": "Exit",
            "entry": "Entry",
            "simce_relative": "Relative SIMCE",
            "admission_core": "Admissions · core",
            "not_estimable": "Not estimable",
            "estimated": "Descriptive cell",
            "segment_labels": {
                "initial": "early childhood",
                "basic": "primary",
                "secondary": "secondary",
            },
        },
    }

    lines = [
        "schema_version: 3",
        "generated_by: scripts/render_thesis_extension_stylized.py",
        "data_governance:",
        "  official_institution_locations: true",
        "  public_school_registry_rows: true",
        "  student_microdata: false",
        "  personal_identifiers: false",
        "  third_party_restricted_rows: false",
        "  map_geometry: official_point_coordinates",
        "assets:",
    ]
    for name in sorted(asset_names):
        lines.append(f"  - {asset_path(name)}")
    lines.append("locales:")
    for lang in ("es", "en"):
        copy = locale_copy[lang]
        lines.extend(
            [
                f"  {lang}:",
                f"    id: {copy['id']}",
                f"    eyebrow: {json.dumps(copy['eyebrow'], ensure_ascii=False)}",
                f"    title: {json.dumps(copy['title'], ensure_ascii=False)}",
                f"    intro: {json.dumps(copy['intro'], ensure_ascii=False)}",
                f"    open_full_size: {json.dumps(copy['open'], ensure_ascii=False)}",
                f"    enlarge: {json.dumps(copy['enlarge'], ensure_ascii=False)}",
                f"    instructions: {json.dumps(copy['instructions'], ensure_ascii=False)}",
                f"    status_template: {json.dumps(copy['status_template'], ensure_ascii=False)}",
                f"    controls_label: {json.dumps(copy['controls_label'], ensure_ascii=False)}",
                f"    previous: {json.dumps(copy['previous'], ensure_ascii=False)}",
                f"    next: {json.dumps(copy['next'], ensure_ascii=False)}",
                f"    go_to: {json.dumps(copy['go_to'], ensure_ascii=False)}",
                f"    of: {json.dumps(copy['of'], ensure_ascii=False)}",
                f"    figure_label: {json.dumps(copy['figure'], ensure_ascii=False)}",
                f"    map_case: {json.dumps(copy['map_case'], ensure_ascii=False)}",
                f"    demographic_case: {json.dumps(copy['demographic_case'], ensure_ascii=False)}",
                f"    trajectory_case: {json.dumps(copy['trajectory_case'], ensure_ascii=False)}",
                f"    schools_heading: {json.dumps(copy['schools_heading'], ensure_ascii=False)}",
                f"    closure_role: {json.dumps(copy['closure_role'], ensure_ascii=False)}",
                f"    entry_role: {json.dumps(copy['entry_role'], ensure_ascii=False)}",
                f"    receiver_role: {json.dumps(copy['receiver_role'], ensure_ascii=False)}",
                f"    school_source: {json.dumps(copy['school_source'], ensure_ascii=False)}",
                "    trajectory_tabs:",
                "      simce: \"SIMCE\"",
                f"      admission: {json.dumps(copy['admission_tab'], ensure_ascii=False)}",
                "    demographic:",
                f"      heading: {json.dumps(copy['demographic_heading'], ensure_ascii=False)}",
                f"      asset: {asset_path(f'estilizada-demografia-{lang}.svg')}",
                f"      alt: {json.dumps(TEXT[lang]['demographic_desc'], ensure_ascii=False)}",
                f"      caption: {json.dumps(copy['demographic_caption'], ensure_ascii=False)}",
                "      rows:",
            ]
        )
        for year in (2025, 2030, 2035, 2050):
            row = by_year[year]
            lines.extend(
                [
                    f"        - year: {year}",
                    f"          population: {int(row['population_age_6_17'])}",
                    f"          index: {float(row['index_2025_100']):.3f}",
                ]
            )
        sources = {row["id"]: row for row in author_case["documentary_sources"]}
        author_schools = author_case["schools"]
        author_summary = author_case["enrollment"]["summaries"]
        author_rows = {int(row["year"]): row for row in author_case["enrollment"]["rows"]}
        lines.extend(
            [
                "    authored_case:",
                f"      label: {json.dumps(copy['author_case_label'], ensure_ascii=False)}",
                f"      title: {json.dumps(copy['author_case_title'], ensure_ascii=False)}",
                f"      intro: {json.dumps(copy['author_case_intro'], ensure_ascii=False)}",
                f"      caveat: {json.dumps(copy['author_case_caveat'], ensure_ascii=False)}",
                f"      coordinate_caveat: {json.dumps(copy['author_case_coordinate'], ensure_ascii=False)}",
                "      commune: El Salvador",
                "      segment_family: basic",
                "      event_period: 2013–2014",
                f"      asset: {asset_path(f'estilizada-mapa-el-salvador-{lang}.svg')}",
                f"      alt: {json.dumps(copy['author_case_alt'], ensure_ascii=False)}",
                f"      open_label: {json.dumps(copy['author_case_open'], ensure_ascii=False)}",
                f"      distance_km: {float(author_schools['geodesic_distance_km']):.3f}",
                f"      combined_2004: {int(author_summary['combined_2004'])}",
                f"      combined_2004_display: {json.dumps('1.399' if lang == 'es' else '1,399')}",
                f"      combined_2013: {int(author_summary['combined_2013'])}",
                "      combined_2013_display: \"977\"",
                f"      combined_change_percent: {float(author_summary['combined_change_2004_2013_percent']):.1f}",
                f"      receiver_2014: {int(author_rows[2014]['receiver_rbd_390'])}",
                "      receiver_2014_display: \"738\"",
                f"      receiver_2025: {int(author_rows[2025]['receiver_rbd_390'])}",
                "      schools:",
                "        - role: closure",
                "          rbd: 391",
                f"          name: {json.dumps(author_schools['closure']['official_name'], ensure_ascii=False)}",
                "          event_year: 2014",
                "        - role: receiver",
                "          rbd: 390",
                f"          name: {json.dumps(author_schools['receiver']['official_name'], ensure_ascii=False)}",
                "          event_year: 2014",
                f"      sources_heading: {json.dumps(copy['author_case_sources'], ensure_ascii=False)}",
                "      sources:",
                f"        - label: {json.dumps('BCN, 1 de abril de 2014' if lang == 'es' else 'BCN, 1 April 2014', ensure_ascii=False)}",
                f"          url: {json.dumps(sources['bcn_2014']['url'])}",
                f"        - label: {json.dumps('FEES, reglamento institucional' if lang == 'es' else 'FEES institutional regulations', ensure_ascii=False)}",
                f"          url: {json.dumps(sources['fees_regulation_2019']['url'])}",
                f"        - label: {json.dumps('Datos abiertos MINEDUC' if lang == 'es' else 'MINEDUC open data', ensure_ascii=False)}",
                f"          url: {json.dumps(sources['mineduc_open_data']['url'])}",
            ]
        )
        lines.extend(
            [
                "    maps:",
                f"      heading: {json.dumps(copy['maps_heading'], ensure_ascii=False)}",
                f"      intro: {json.dumps(copy['maps_intro'], ensure_ascii=False)}",
                "      items:",
            ]
        )
        for row in spatial:
            file_name = f"estilizada-mapa-{slug(row['commune'])}-{lang}.svg"
            alt = TEXT[lang]["map_desc"].format(commune=row["commune"])
            closures = int(row["paired_closures"])
            entries = int(row["nearby_entries"])
            if lang == "es":
                closure_label = "cierre" if closures == 1 else "cierres"
                entry_label = "apertura única" if entries == 1 else "aperturas únicas"
                caption = f"{closures} {closure_label} y {entries} {entry_label}; distancia "
            else:
                closure_label = "closure" if closures == 1 else "closures"
                entry_label = "unique opening" if entries == 1 else "unique openings"
                caption = f"{closures} {closure_label} and {entries} {entry_label}; distance "
            caption += f"{fmt_decimal(float(row['median_distance_km']), 3, lang)} km"
            case_points = [
                point
                for point in school_points
                if point["case"] == row["case"] and point["commune"] == row["commune"]
            ]
            lines.extend(
                [
                    f"        - commune: {json.dumps(row['commune'], ensure_ascii=False)}",
                    f"          asset: {asset_path(file_name)}",
                    f"          alt: {json.dumps(alt, ensure_ascii=False)}",
                    f"          caption: {json.dumps(caption, ensure_ascii=False)}",
                    f"          paired_closures: {int(row['paired_closures'])}",
                    f"          nearby_entries: {int(row['nearby_entries'])}",
                    f"          same_commune_pairs: {int(row['same_commune_pairs'])}",
                    f"          event_period: {json.dumps(display_period(row['event_period']), ensure_ascii=False)}",
                    f"          median_distance_km: {float(row['median_distance_km']):.3f}",
                    f"          education_segment: {json.dumps(row['education_segment'])}",
                    f"          segment_family: {json.dumps(copy['segment_labels'][row['segment_family']], ensure_ascii=False)}",
                    "          schools:",
                ]
            )
            for point, label in labeled_map_points(case_points, lang):
                role_label = copy["closure_role"] if point["role"] == "closure" else copy["entry_role"]
                lines.extend(
                    [
                        f"            - marker: {json.dumps(label)}",
                        f"              role: {json.dumps(role_label, ensure_ascii=False)}",
                        f"              rbd: {int(point['rbd'])}",
                        f"              name: {json.dumps(point['school_name'], ensure_ascii=False)}",
                        f"              event_year: {int(point['event_year'])}",
                    ]
                )
        lines.extend(
            [
                "    trajectories:",
                f"      heading: {json.dumps(copy['trajectories_heading'], ensure_ascii=False)}",
                f"      intro: {json.dumps(copy['trajectories_intro'], ensure_ascii=False)}",
                "      items:",
            ]
        )
        for outcome in ("simce_relative", "admission_core"):
            outcome_key = "simce" if outcome == "simce_relative" else "admission"
            title = TEXT[lang][f"trajectory_{outcome_key}_title"]
            desc = TEXT[lang][f"trajectory_{outcome_key}_desc"]
            lines.extend(
                [
                    f"        - outcome: {outcome}",
                    f"          title: {json.dumps(title, ensure_ascii=False)}",
                    f"          asset: {asset_path(f'estilizada-trayectoria-{outcome_key}-{lang}.svg')}",
                    f"          alt: {json.dumps(desc, ensure_ascii=False)}",
                ]
            )
        lines.extend(
            [
                "      rows:",
            ]
        )
        for row in sorted(
            trajectory,
            key=lambda item: (
                0 if item["branch"] == "exit" else 1,
                item["outcome"],
                int(item["relative_year"]),
            ),
        ):
            interval = (
                f"[{float(row['ci95_low']):.3f}, {float(row['ci95_high']):.3f}]"
                if row["ci95_low"]
                else "—"
            )
            lines.extend(
                [
                    f"        - branch: {json.dumps(copy[row['branch']], ensure_ascii=False)}",
                    f"          outcome: {json.dumps(copy[row['outcome']], ensure_ascii=False)}",
                    f"          relative_year: {int(row['relative_year'])}",
                    f"          estimate: {float(row['estimate']):.3f}",
                    f"          interval: {json.dumps(interval, ensure_ascii=False)}",
                    f"          units: {int(row['units'])}",
                    f"          status: {json.dumps(copy['estimated'] if row['status'] == 'ESTIMATED' else copy['not_estimable'], ensure_ascii=False)}",
                    f"          regime: {json.dumps(row['regimes'], ensure_ascii=False)}",
                ]
            )
        lines.extend(
            [
                "    table_labels:",
                f"      method_heading: {json.dumps(copy['method_heading'], ensure_ascii=False)}",
                f"      data_tables_label: {json.dumps(copy['data_tables_label'], ensure_ascii=False)}",
                f"      year: {json.dumps(copy['year'], ensure_ascii=False)}",
                f"      population: {json.dumps(copy['population'], ensure_ascii=False)}",
                f"      index: {json.dumps(copy['index'], ensure_ascii=False)}",
                f"      commune: {json.dumps(copy['commune'], ensure_ascii=False)}",
                f"      closures: {json.dumps(copy['closures'], ensure_ascii=False)}",
                f"      entries: {json.dumps(copy['entries'], ensure_ascii=False)}",
                f"      same_commune: {json.dumps(copy['same_commune'], ensure_ascii=False)}",
                f"      period: {json.dumps(copy['period'], ensure_ascii=False)}",
                f"      distance: {json.dumps(copy['distance'], ensure_ascii=False)}",
                f"      branch: {json.dumps(copy['branch'], ensure_ascii=False)}",
                f"      outcome: {json.dumps(copy['outcome'], ensure_ascii=False)}",
                f"      relative_year: {json.dumps(copy['relative_year'], ensure_ascii=False)}",
                f"      estimate: {json.dumps(copy['estimate'], ensure_ascii=False)}",
                f"      interval: {json.dumps(copy['interval'], ensure_ascii=False)}",
                f"      n: {json.dumps(copy['n'], ensure_ascii=False)}",
                f"      status: {json.dumps(copy['status'], ensure_ascii=False)}",
                f"      regime: {json.dumps(copy['regime'], ensure_ascii=False)}",
            ]
        )
    return "\n".join(lines) + "\n"


def build_outputs(
    data: Mapping[str, Sequence[Mapping[str, str]]],
    author_case: Mapping[str, Any],
) -> dict[Path, bytes]:
    outputs: dict[Path, bytes] = {}
    asset_names: list[str] = []
    for lang in ("es", "en"):
        name = f"estilizada-mapa-el-salvador-{lang}.svg"
        outputs[OUTPUT_DIR / name] = render_author_case_map(author_case, lang).encode()
        asset_names.append(name)
        name = f"estilizada-demografia-{lang}.svg"
        outputs[OUTPUT_DIR / name] = render_demography(data["demography"], lang).encode()
        asset_names.append(name)
        for outcome in ("simce_relative", "admission_core"):
            outcome_key = "simce" if outcome == "simce_relative" else "admission"
            name = f"estilizada-trayectoria-{outcome_key}-{lang}.svg"
            outputs[OUTPUT_DIR / name] = render_trajectory(
                data["trajectory"], lang, outcome
            ).encode()
            asset_names.append(name)
        for row in data["spatial"]:
            name = f"estilizada-mapa-{slug(row['commune'])}-{lang}.svg"
            matching_points = [
                item
                for item in data["school_points"]
                if item["case"] == row["case"] and item["commune"] == row["commune"]
            ]
            matching_links = [
                item
                for item in data["school_links"]
                if item["case"] == row["case"] and item["commune"] == row["commune"]
            ]
            outputs[OUTPUT_DIR / name] = render_map(
                row, matching_points, matching_links, lang
            ).encode()
            asset_names.append(name)
    yaml_bytes = render_yaml(data, asset_names, author_case).encode()
    outputs[DATA_PATH] = yaml_bytes
    outputs[MAP_DATA_PATH] = render_map_data(data, author_case)
    manifest = {
        "schema_version": 2,
        "generated_by": "scripts/render_thesis_extension_stylized.py",
        "generator": {
            "path": "scripts/render_thesis_extension_stylized.py",
            "sha256": sha256_path(Path(__file__)),
        },
        "data_governance": {
            "official_institution_locations": True,
            "public_school_registry_rows": True,
            "student_microdata": False,
            "personal_identifiers": False,
            "third_party_restricted_rows": False,
            "map_geometry": "official_point_coordinates",
        },
        "visual_lineage": {
            "reference": "assets/src/catastro_sii/chart-theme.ts",
            "reference_sha256": sha256_path(AVALUOS_THEME_PATH),
            "shared_accents": {
                name: COLORS[name] for name in AVALUOS_SHARED_ACCENTS
            },
            "adaptation": "official_school_point_map",
        },
        "inputs": {
            str(path.relative_to(WORKSPACE)): sha256_path(path)
            for path in (*INPUTS.values(), AUTHOR_CASE_PATH)
        },
        "outputs": {
            str(path.relative_to(ROOT)): {
                "sha256": sha256_bytes(content),
                "bytes": len(content),
            }
            for path, content in sorted(outputs.items(), key=lambda item: str(item[0]))
        },
    }
    outputs[MANIFEST_PATH] = (
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode()
    return outputs


def validate_output(path: Path, content: bytes) -> None:
    text = content.decode("utf-8")
    if PRIVATE_TEXT.search(text):
        raise ValueError(f"texto potencialmente privado en {path}")
    if path.suffix == ".svg":
        requirements = (
            'role="img"',
            "aria-labelledby=",
            "<title",
            "<desc",
            "viewBox=",
            "Inter",
        )
        if any(token not in text for token in requirements):
            raise ValueError(f"SVG sin semántica accesible: {path}")
        if len(content) < 4_000:
            raise ValueError(f"SVG trivial: {path}")


def write_outputs(outputs: Mapping[Path, bytes]) -> None:
    for path, content in outputs.items():
        validate_output(path, content)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)


def check_outputs(outputs: Mapping[Path, bytes]) -> None:
    failures = []
    for path, expected in outputs.items():
        validate_output(path, expected)
        if not path.is_file():
            failures.append(f"ausente: {path.relative_to(ROOT)}")
        elif path.read_bytes() != expected:
            failures.append(f"deriva: {path.relative_to(ROOT)}")
    if failures:
        raise ValueError("; ".join(failures))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--check", action="store_true", help="verify generated outputs without writing"
    )
    args = parser.parse_args()
    try:
        outputs = build_outputs(load_data(), load_author_case())
        if args.check:
            check_outputs(outputs)
            print("THESIS_EXTENSION_STYLIZED_VALID")
        else:
            write_outputs(outputs)
            print(f"THESIS_EXTENSION_STYLIZED_WRITTEN count={len(outputs)}")
    except (OSError, TypeError, ValueError, KeyError) as error:
        print(f"THESIS_EXTENSION_STYLIZED_ERROR {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
