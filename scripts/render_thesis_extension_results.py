#!/usr/bin/env python3
"""Construye la familia SVG bilingüe de resultados de la extensión de tesis.

El renderer copia la geometría de seis SVG científicos cerrados y transforma
solo sus textos. Los CSV se usan como anclas de proveniencia: no se reinterpretan
ni se copian al blog.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from xml.etree import ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[1]
SCIENTIFIC_ROOT = WORKSPACE / "incubadora/tesis_mae_mejorada"
OUTPUT_DIR = ROOT / "assets/images/extender-tesis-no-es-agregar-anos"
MANIFEST_PATH = OUTPUT_DIR / "resultados-manifest.json"

SVG_NS = "http://www.w3.org/2000/svg"
XLINK_NS = "http://www.w3.org/1999/xlink"
DC_NS = "http://purl.org/dc/elements/1.1/"
CC_NS = "http://creativecommons.org/ns#"
RDF_NS = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
for prefix, namespace in (
    ("", SVG_NS),
    ("xlink", XLINK_NS),
    ("dc", DC_NS),
    ("cc", CC_NS),
    ("rdf", RDF_NS),
):
    ET.register_namespace(prefix, namespace)

PRIVATE_PATTERN = re.compile(r"(?i)(?:/home/|Descargas/programaciones|\bRBD\b)")
SPANISH_RESIDUAL = re.compile(r"[áéíóúñ¿¡]", re.IGNORECASE)
NUMBER_PATTERN = re.compile(
    r"(?<![A-Za-z])(?:[+\-−±]?\d+(?:[.,]\d+)?(?:e[+\-−]?\d+)?(?:\s*%)?)"
)
INVARIANT_PATTERN = re.compile(r"^[\d\s+\-−±.,%\[\]<>/=·≥eEn]+$")
INVARIANT_TEXT = {"tesis_mae_mejorada", "kNN 10", "kNN 25", "kNN 50"}
LAYOUT_ADJUSTMENTS = [
    "v5: reduce the admissions result-row label to 10px to prevent left-edge clipping",
    "v7: shift the second vertical axis label +6 SVG units to prevent left-edge clipping",
    "v8: reduce the first score-row label to 8px to prevent left-edge clipping",
    "v8 EN: define academic (AC) and technical-vocational (TV) inside the SVG",
]


@dataclass(frozen=True)
class FigureSpec:
    key: str
    output_stem: str
    source_svg: str
    source_csv: str


SPECS = (
    FigureSpec(
        "v3",
        "resultados-v3-sensibilidad-mercados",
        "figures/release_visuals_h1_h3/v3_market_sensitivity.svg",
        "figures/release_visuals_h1_h3/v3_market_sensitivity.csv",
    ),
    FigureSpec(
        "v5",
        "resultados-v5-mr1",
        "figures/release_visuals_mr/v5_mr1_forest.svg",
        "figures/release_visuals_mr/v5_mr1_forest.csv",
    ),
    FigureSpec(
        "v6",
        "resultados-v6-mr2",
        "figures/release_visuals_mr/v6_mr2_support.svg",
        "figures/release_visuals_mr/v6_mr2_support.csv",
    ),
    FigureSpec(
        "v7",
        "resultados-v7-mr3",
        "figures/release_visuals_mr/v7_mr3_fhk.svg",
        "figures/release_visuals_mr/v7_mr3_fhk.csv",
    ),
    FigureSpec(
        "v8",
        "resultados-v8-mr4",
        "figures/release_visuals_mr/v8_mr4_modality.svg",
        "figures/release_visuals_mr/v8_mr4_modality.csv",
    ),
    FigureSpec(
        "v10",
        "resultados-v10-escalera-causal",
        "figures/release_visuals/v10_causal_ladder.svg",
        "figures/release_visuals/v10_causal_ladder.csv",
    ),
)

TRANSLATIONS = {
    # V3
    "V3 · Seis mercados, seis contrastes con incertidumbre": (
        "V3 · Six markets, six contrasts with uncertainty"
    ),
    "Gráfico de bosque con seis contrastes asociacionales de riesgo de cierre frente a "
    "comuna. Cada fila distingue el intervalo puntual, la banda simultánea y el punto "
    "estimado. Todas las bandas simultáneas incluyen cero. Su techo máximo es 0,273 "
    "puntos porcentuales: supera el umbral de sensibilidad de 0,25, pero queda bajo el "
    "umbral autoral de 0,5 puntos porcentuales.": (
        "Forest plot with six associational contrasts in closure risk relative to the "
        "municipality. Each row distinguishes the pointwise interval, simultaneous band, "
        "and point estimate. Every simultaneous band includes zero. Their maximum ceiling "
        "is 0.273 percentage points: above the 0.25 sensitivity threshold, but below the "
        "author's 0.5 percentage-point threshold."
    ),
    "Diferencia frente a comuna (puntos porcentuales)": (
        "Difference relative to municipality (percentage points)"
    ),
    "Radio 5 km": "5 km radius",
    "Radio 10 km": "10 km radius",
    "Radio 20 km": "20 km radius",
    "kNN 10": "kNN 10",
    "kNN 25": "kNN 25",
    "kNN 50": "kNN 50",
    "±0,25 pp · sensibilidad": "±0.25 pp · sensitivity",
    "±0,5 pp · umbral autoral": "±0.5 pp · author threshold",
    "Intervalo puntual 95 %": "Pointwise 95% interval",
    "Banda simultánea 95 %": "95% simultaneous band",
    "Estimación": "Estimate",
    "Contraste asociacional de riesgo de cierre frente a comuna · familia completa": (
        "Associational contrast in closure risk relative to municipality · full family"
    ),
    "Las seis bandas simultáneas incluyen 0. Techo: 0,273 pp; no descarta 0,25 pp, "
    "pero queda bajo 0,5 pp.": (
        "All six simultaneous bands include 0. Ceiling: 0.273 pp; it does not rule out "
        "0.25 pp, but remains below 0.5 pp."
    ),
    "Esto acota una asociación observada; no identifica un efecto causal.": (
        "This bounds an observed association; it does not identify a causal effect."
    ),
    # V5
    "V5 · MR1: los cierres no seleccionan inequívocamente peores resultados": (
        "V5 · MR1: closures do not unequivocally select lower-performing schools"
    ),
    "Bosque de estimaciones MR1 expresadas en desviaciones estándar. Los resultados "
    "primarios son 0,029 para SIMCE, cuyo intervalo cruza cero, y menos 0,001 para "
    "admisión, que no es estimable. Triángulos separados muestran la sensibilidad de "
    "pendiente preevento. A la derecha se muestra la pérdida desde 330 cierres hasta 21 "
    "y 8 casos con soporte estricto.": (
        "Forest plot of MR1 estimates in standard deviations. The primary results are "
        "0.029 for SIMCE, whose interval crosses zero, and minus 0.001 for admissions, "
        "which is not estimable. Separate triangles show the pre-event slope sensitivity. "
        "The right panel shows attrition from 330 closures to 21 and 8 cases with strict "
        "support."
    ),
    "Diferencia en DE e IC 95% cluster bootstrap": (
        "Difference in SD and 95% cluster-bootstrap CI"
    ),
    "SIMCE relativo": "Relative SIMCE",
    "Admisión · núcleo": "Admissions · core",
    "primario: +0.029  n=21": "primary: +0.029  n=21",
    "pendiente: +0.040  n=21": "slope: +0.040  n=21",
    "primario: n/e  n=8": "primary: n/e  n=8",
    "pendiente: n/e  n=8": "slope: n/e  n=8",
    "● Primario  △ Sensibilidad: pendiente preevento": (
        "● Primary  △ Sensitivity: pre-event slope"
    ),
    "Eventos / unidades": "Events / units",
    "Cierres": "Closures",
    "Con resultado": "With outcome",
    "Soporte estricto": "Strict support",
    "El N nacional no es el N estimable": "The national N is not the estimable N",
    "Unidad: desviaciones estándar (DE) · establecimiento que cierra menos comparables": (
        "Unit: standard deviations (SD) · closing school minus comparators"
    ),
    "SIMCE cruza cero; admisión queda no estimable con ocho cierres. × = punto "
    "descriptivo sin intervalo.": (
        "SIMCE crosses zero; admissions is not estimable with eight closures. "
        "× = descriptive point without an interval."
    ),
    # V6
    "V6 · MR2: cohortes tardías no rescatan la pregunta principal": (
        "V6 · MR2: later cohorts do not rescue the primary question"
    ),
    "Dos paneles para las cohortes uno a tres de nuevas escuelas. Las estimaciones de "
    "admisión carecen de intervalo y las tres cohortes quedan no estimables. SIMCE tampoco "
    "alcanza el umbral en ninguna cohorte. Un embudo separado muestra la caída desde 414 "
    "entradas a no más de 8 casos con soporte. Cada punto declara su n y una línea marca "
    "el mínimo de 10 unidades "
    "y 10 clusters. El veredicto global es no estimable.": (
        "Two panels cover cohorts one through three of new schools. Admissions estimates "
        "lack intervals and all three cohorts remain not estimable. SIMCE also fails to "
        "reach the threshold in every cohort. A separate funnel shows attrition from 414 "
        "entries to at most 8 supported cases. Each point reports its n, and a line marks "
        "the minimum of 10 "
        "units and 10 clusters. The global verdict is not estimable."
    ),
    "1ª": "1st",
    "2ª": "2nd",
    "3ª": "3rd",
    "Cohorte desde la entrada": "Cohort since entry",
    "Ventaja descriptiva e IC 95%": "Descriptive advantage and 95% CI",
    "× = punto descriptivo sin inferencia": "× = descriptive point without inference",
    "Entradas": "Entries",
    "Activas": "Active",
    "Soporte": "Support",
    "umbral: n≥10 y clusters≥10": "threshold: n≥10 and clusters≥10",
    "Soporte observado por cohorte": "Observed support by cohort",
    "SIMCE relativo · cohorte 1": "Relative SIMCE · cohort 1",
    "SIMCE relativo · cohorte 2": "Relative SIMCE · cohort 2",
    "SIMCE relativo · cohorte 3": "Relative SIMCE · cohort 3",
    "Admisión · núcleo · cohorte 1": "Admissions · core · cohort 1",
    "Admisión · núcleo · cohorte 2": "Admissions · core · cohort 2",
    "Admisión · núcleo · cohorte 3": "Admissions · core · cohort 3",
    "VEREDICTO GLOBAL · NOT_ESTIMABLE": "GLOBAL VERDICT · NOT_ESTIMABLE",
    "Umbral mínimo: 10 unidades y 10 clusters; la primera cohorte obligatoria queda "
    "bajo él.": (
        "Minimum threshold: 10 units and 10 clusters; required cohort one falls below it."
    ),
    # V7
    "V7 · MR3: la rotación oficial es pequeña dentro de la identidad FHK": (
        "V7 · MR3: official turnover is small within the FHK identity"
    ),
    "Dos cascadas descomponen el cambio de SIMCE relativo y admisión en componentes "
    "dentro, entre, cruce, entradas y salidas oficiales y cambios de observación. Las "
    "barras oficiales están tramadas y su total se informa aparte, sin sumarlo dos veces "
    "a la identidad. La rotación oficial es negativa e imprecisa en SIMCE, y positiva en "
    "admisión. La identidad FHK cierra con residual máximo 6,66 por diez a la menos 16 y "
    "no representa "
    "un efecto causal.": (
        "Two waterfalls decompose changes in relative SIMCE and admissions into within, "
        "between, cross, official entry and exit, and observed-sample entry and exit. "
        "Official bars are hatched and their total is reported separately, without "
        "double-counting it in the identity. Official turnover is negative and imprecise "
        "in SIMCE, and positive in admissions. The FHK identity closes with a maximum "
        "residual of 6.66 "
        "times ten to the minus 16 and does not represent a causal effect."
    ),
    "Dentro": "Within",
    "Entre": "Between",
    "Cruce": "Cross",
    "Entrada": "Entry",
    "oficial": "official",
    "Salida": "Exit",
    "Alta": "Entry",
    "observada": "observed",
    "Baja": "Exit",
    "Cambio": "Change",
    "total": "total",
    "Contribución": "Contribution",
    "SIMCE relativo · TOTAL OFICIAL = entrada + salida: -0.000105 [-0.000346, +0.000103]": (
        "Relative SIMCE · OFFICIAL TOTAL = entry + exit: -0.000105 [-0.000346, +0.000103]"
    ),
    "Admisión · núcleo · TOTAL OFICIAL = entrada + salida: +0.000113 [+0.000027, "
    "+0.000213]": (
        "Admissions · core · OFFICIAL TOTAL = entry + exit: +0.000113 [+0.000027, "
        "+0.000213]"
    ),
    "Identidad FHK verificada · residual máximo 6.66e-16 < 1e-10. El total oficial no "
    "se suma otra vez y no identifica causalidad.": (
        "Verified FHK identity · maximum residual 6.66e-16 < 1e-10. The official total "
        "is not added again and does not identify causality."
    ),
    # V8
    "V8 · MR4: modalidad, puntajes y participación no son intercambiables": (
        "V8 · MR4: track, scores, and participation are not interchangeable"
    ),
    "Tres paneles separan puntajes, participación y soporte por modalidad. En "
    "humanista-científica, las cinco estimaciones de selección de salida quedan no "
    "estimables con siete unidades. Las entradas tienen como máximo dos unidades con "
    "soporte. Técnico-profesional tiene cero comparaciones estrictamente soportadas en "
    "todas las medidas y permanece no estimable.": (
        "Three panels separate scores, participation, and support by track. In the "
        "academic track, all five exit-selection estimates are not estimable with seven "
        "units. Entry comparisons have at most two supported units. The technical-"
        "vocational track has zero strictly supported comparisons for every measure "
        "and remains not estimable."
    ),
    "Contraste e IC 95%": "Contrast and 95% CI",
    "Núcleo": "Core",
    "Ciencias": "Science",
    "Tres pruebas": "Three tests",
    "Puntajes · HC salida": "Scores · AC exit",
    "Aprobados": "Passed",
    "Inicial": "Initial",
    "Participación · HC salida": "Participation · AC exit",
    "3 pruebas": "3 tests",
    "Part. aprob.": "Part. passed",
    "Part. inicial": "Part. initial",
    "Soporte por modalidad": "Support by track",
    "Selección de salida HC, entradas HC y toda TP: no estimables": (
        "Academic (AC) exit selection, AC entry, and all "
        "technical-vocational (TV): not estimable"
    ),
    "TP tiene soporte estricto 0 en todas las medidas; no se publica un efecto "
    "inexistente.": (
        "TV has strict support of 0 for every measure; no nonexistent effect is reported."
    ),
    "HC salida": "AC exit",
    "HC entrada · máx.": "AC entry · max.",
    "TP · 0": "TV · 0",
    # V10
    "V10 · La causalidad no aparece al sumar controles": (
        "V10 · Causality does not appear by adding controls"
    ),
    "Escalera conceptual de tres niveles. Descripción y asociación condicional indican "
    "qué permiten y qué prohíben afirmar. La identificación causal aparece bloqueada: "
    "exige una regla o shock exógeno, pre-tendencias defendibles y efectos sobre "
    "estudiantes o mercados; añadir controles no autoriza ese salto.": (
        "Three-level conceptual ladder. Description and conditional association show "
        "what can and cannot be claimed. Causal identification remains blocked: it "
        "requires an exogenous rule or shock, defensible pre-trends, and effects on "
        "students or markets; adding controls does not authorize that jump."
    ),
    "1 · Descripción": "1 · Description",
    "PERMITE  Stocks, flujos, trayectorias y cobertura observada.": (
        "ALLOWS  Stocks, flows, trajectories, and observed coverage."
    ),
    "PROHÍBE  Atribuir los cambios a cierres o entradas.": (
        "PROHIBITS  Attributing changes to closures or entries."
    ),
    "FALTA  Una comparación contrafactual defendible.": (
        "MISSING  A defensible counterfactual comparison."
    ),
    "2 · Asociación condicional": "2 · Conditional association",
    "PERMITE  Contrastes ajustados dentro del soporte observado.": (
        "ALLOWS  Adjusted contrasts within observed support."
    ),
    "PROHÍBE  Leer coeficientes ajustados como efectos causales.": (
        "PROHIBITS  Reading adjusted coefficients as causal effects."
    ),
    "FALTA  Variación exógena y pre-tendencias defendibles.": (
        "MISSING  Exogenous variation and defensible pre-trends."
    ),
    "3 · Identificación causal · no alcanzada": "3 · Causal identification · not reached",
    "PERMITE  Solo con un diseño que sobreviva falsificaciones.": (
        "ALLOWS  Only with a design that survives falsification."
    ),
    "PROHÍBE  Afirmar que la destrucción creadora generó mejoras.": (
        "PROHIBITS  Claiming that creative destruction produced improvements."
    ),
    "FALTA  Regla o shock exógeno, pre-tendencias y efectos sobre estudiantes o "
    "mercados.": (
        "MISSING  An exogenous rule or shock, pre-trends, and effects on students or "
        "markets."
    ),
    "SALTO NO AUTORIZADO": "UNAUTHORIZED JUMP",
}


class RenderError(ValueError):
    """La familia bilingüe no satisface el contrato editorial."""


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _text_elements(root: ET.Element) -> list[ET.Element]:
    return [
        element
        for element in root.iter()
        if _local_name(element.tag) in {"text", "title", "desc"}
        and element.text
        and element.text.strip()
    ]


def _texts(root: ET.Element) -> list[str]:
    return [element.text.strip() for element in _text_elements(root) if element.text]


def _is_invariant(text: str) -> bool:
    return text in INVARIANT_TEXT or bool(INVARIANT_PATTERN.fullmatch(text))


def _translated(text: str) -> str:
    if text in TRANSLATIONS:
        return TRANSLATIONS[text]
    if _is_invariant(text):
        return text
    raise RenderError(f"texto fuente sin traducción exhaustiva: {text!r}")


def _number_fingerprint(texts: list[str]) -> Counter[str]:
    def normalise(value: str) -> str:
        return value.replace("−", "-").replace(",", ".").replace(" ", "")

    return Counter(
        normalise(match.group(0))
        for text in texts
        for match in NUMBER_PATTERN.finditer(text)
    )


def _parse(path: Path) -> ET.ElementTree:
    if not path.is_file() or path.is_symlink():
        raise RenderError(f"SVG ausente o inseguro: {path}")
    try:
        return ET.parse(path)
    except ET.ParseError as error:
        raise RenderError(f"SVG inválido: {path}: {error}") from error


def _assert_accessibility(root: ET.Element, label: str) -> None:
    if root.get("role") != "img" or "viewBox" not in root.attrib:
        raise RenderError(f"{label}: raíz SVG sin role=img o viewBox")
    labelled = root.get("aria-labelledby", "").split()
    direct = {
        child.get("id"): child
        for child in root
        if _local_name(child.tag) in {"title", "desc"} and child.get("id")
    }
    if len(labelled) != 2 or any(identifier not in direct for identifier in labelled):
        raise RenderError(f"{label}: aria-labelledby no enlaza title y desc")
    if {_local_name(direct[identifier].tag) for identifier in labelled} != {
        "title",
        "desc",
    }:
        raise RenderError(f"{label}: faltan title o desc accesibles")


def _write_tree(tree: ET.ElementTree, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile(
        dir=destination.parent,
        suffix=".svg",
        delete=False,
    ) as handle:
        temporary = Path(handle.name)
    try:
        tree.write(temporary, encoding="utf-8", xml_declaration=True)
        if (
            not destination.exists()
            or temporary.read_bytes() != destination.read_bytes()
        ):
            os.replace(temporary, destination)
        else:
            temporary.unlink()
    finally:
        if temporary.exists():
            temporary.unlink()


def _write_json(payload: dict[str, Any], destination: Path) -> None:
    content = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    destination.parent.mkdir(parents=True, exist_ok=True)
    if destination.exists() and destination.read_text(encoding="utf-8") == content:
        return
    with tempfile.NamedTemporaryFile(
        mode="w",
        encoding="utf-8",
        dir=destination.parent,
        suffix=".json",
        delete=False,
    ) as handle:
        handle.write(content)
        temporary = Path(handle.name)
    os.replace(temporary, destination)


def _apply_blog_layout(root: ET.Element, spec: FigureSpec) -> None:
    elements = _text_elements(root)
    if spec.key == "v5":
        candidates = [
            element
            for element in elements
            if element.text
            and element.text.strip() in {"Admisión · núcleo", "Admissions · core"}
            and "font-size: 11px" in element.get("style", "")
        ]
        if len(candidates) != 1:
            raise RenderError("v5: no se pudo aplicar el ajuste antirrecorte")
        label = candidates[0]
        label.set(
            "style",
            label.get("style", "").replace("font-size: 11px", "font-size: 10px", 1),
        )
    elif spec.key == "v7":
        candidates = [
            element
            for element in elements
            if element.text
            and element.text.strip() in {"Contribución", "Contribution"}
            and float(element.get("x", "999")) < 10
        ]
        if len(candidates) != 1 or candidates[0].get("y") is None:
            raise RenderError("v7: no se pudo aplicar el ajuste antirrecorte")
        label = candidates[0]
        new_x = float(label.get("x", "0")) + 6
        y = label.get("y", "0")
        label.set("x", f"{new_x:g}")
        label.set("transform", f"rotate(-90 {new_x:g} {y})")
    elif spec.key == "v8":
        candidates = [
            element
            for element in elements
            if element.text and element.text.strip() in {"Tres pruebas", "Three tests"}
        ]
        if len(candidates) != 1 or candidates[0].get("style") is None:
            raise RenderError("v8: no se pudo aplicar el ajuste antirrecorte")
        label = candidates[0]
        style = label.get("style", "")
        if "font-size: 9px" not in style:
            raise RenderError("v8: tamaño fuente de referencia inesperado")
        label.set("style", style.replace("font-size: 9px", "font-size: 8px", 1))


def _render_pair(spec: FigureSpec, output_dir: Path) -> dict[str, Any]:
    source_svg = SCIENTIFIC_ROOT / spec.source_svg
    source_csv = SCIENTIFIC_ROOT / spec.source_csv
    if not source_csv.is_file() or source_csv.is_symlink():
        raise RenderError(f"CSV fuente ausente o inseguro: {spec.source_csv}")
    source_tree = _parse(source_svg)
    source_texts = _texts(source_tree.getroot())
    expected_en = [_translated(text) for text in source_texts]
    if len(expected_en) != len(source_texts):
        raise RenderError(f"{spec.key}: traducción no biyectiva por posición")

    outputs: dict[str, Any] = {}
    for language in ("es", "en"):
        tree = _parse(source_svg)
        root = tree.getroot()
        _assert_accessibility(root, f"{spec.key}-{language}")
        elements = _text_elements(root)
        translated = 0
        for element, source_text in zip(elements, source_texts, strict=True):
            target = source_text if language == "es" else _translated(source_text)
            if target != source_text:
                translated += 1
            element.text = target
        _apply_blog_layout(root, spec)
        destination = output_dir / f"{spec.output_stem}-{language}.svg"
        _write_tree(tree, destination)
        outputs[language] = {
            "filename": destination.name,
            "sha256": sha256(destination),
            "bytes": destination.stat().st_size,
            "text_nodes": len(elements),
            "translated_nodes": translated,
        }
    return {
        "key": spec.key,
        "source_svg": spec.source_svg,
        "source_svg_sha256": sha256(source_svg),
        "source_csv": spec.source_csv,
        "source_csv_sha256": sha256(source_csv),
        "numeric_fingerprint": sorted(_number_fingerprint(source_texts).elements()),
        "outputs": outputs,
    }


def build_family(output_dir: Path = OUTPUT_DIR) -> dict[str, Any]:
    figures = [_render_pair(spec, output_dir) for spec in SPECS]
    manifest = {
        "schema_version": 1,
        "status": "BILINGUAL_THESIS_EXTENSION_RESULTS_READY",
        "generator": "scripts/render_thesis_extension_results.py",
        "generator_sha256": sha256(Path(__file__)),
        "source_policy": "closed_public_svg_geometry_plus_csv_hash",
        "blog_layout_adjustments": LAYOUT_ADJUSTMENTS,
        "languages": ["es", "en"],
        "figures": figures,
    }
    _write_json(manifest, output_dir / MANIFEST_PATH.name)
    validate_family(output_dir)
    return manifest


def _manifest(output_dir: Path) -> dict[str, Any]:
    path = output_dir / MANIFEST_PATH.name
    if not path.is_file() or path.is_symlink():
        raise RenderError("manifiesto ausente o inseguro")
    payload = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise RenderError("manifiesto no es un objeto")
    return payload


def _validate_pair(spec: FigureSpec, entry: dict[str, Any], output_dir: Path) -> None:
    source_svg = SCIENTIFIC_ROOT / spec.source_svg
    source_csv = SCIENTIFIC_ROOT / spec.source_csv
    if (
        entry.get("source_svg") != spec.source_svg
        or entry.get("source_csv") != spec.source_csv
    ):
        raise RenderError(f"{spec.key}: rutas lógicas de fuente alteradas")
    if entry.get("source_svg_sha256") != sha256(source_svg):
        raise RenderError(f"{spec.key}: drift del SVG científico")
    if entry.get("source_csv_sha256") != sha256(source_csv):
        raise RenderError(f"{spec.key}: drift del CSV científico")

    source_root = _parse(source_svg).getroot()
    source_texts = _texts(source_root)
    expected_en = [_translated(text) for text in source_texts]
    fingerprint = sorted(_number_fingerprint(source_texts).elements())
    if entry.get("numeric_fingerprint") != fingerprint:
        raise RenderError(f"{spec.key}: fingerprint numérico obsoleto")

    for language, expected_texts in (("es", source_texts), ("en", expected_en)):
        output = entry.get("outputs", {}).get(language, {})
        expected_name = f"{spec.output_stem}-{language}.svg"
        if output.get("filename") != expected_name:
            raise RenderError(f"{spec.key}-{language}: nombre de salida inesperado")
        path = output_dir / expected_name
        if not path.is_file() or path.is_symlink() or path.stat().st_size < 4_000:
            raise RenderError(f"{spec.key}-{language}: SVG ausente, inseguro o trivial")
        if (
            output.get("sha256") != sha256(path)
            or output.get("bytes") != path.stat().st_size
        ):
            raise RenderError(f"{spec.key}-{language}: hash o tamaño de salida cambió")
        root = _parse(path).getroot()
        _assert_accessibility(root, f"{spec.key}-{language}")
        texts = _texts(root)
        if _number_fingerprint(texts) != _number_fingerprint(source_texts):
            raise RenderError(f"{spec.key}-{language}: deriva numérica")
        serialized = path.read_text(encoding="utf-8")
        if PRIVATE_PATTERN.search(serialized):
            raise RenderError(
                f"{spec.key}-{language}: ruta privada o identificador prohibido"
            )
        if language == "en" and SPANISH_RESIDUAL.search("\n".join(texts)):
            raise RenderError(f"{spec.key}-en: residuo español")
        if (
            language == "en"
            and "NOT_ESTIMABLE" in "\n".join(source_texts)
            and Counter(text for text in texts if "NOT_ESTIMABLE" in text)
            != Counter(
                _translated(text) for text in source_texts if "NOT_ESTIMABLE" in text
            )
        ):
            raise RenderError(f"{spec.key}-en: NOT_ESTIMABLE fue traducido")
        if texts != expected_texts:
            raise RenderError(
                f"{spec.key}-{language}: texto no coincide con el contrato"
            )


def validate_family(output_dir: Path = OUTPUT_DIR) -> None:
    manifest = _manifest(output_dir)
    if (
        manifest.get("schema_version"),
        manifest.get("status"),
        manifest.get("languages"),
    ) != (1, "BILINGUAL_THESIS_EXTENSION_RESULTS_READY", ["es", "en"]):
        raise RenderError("cabecera de manifiesto inesperada")
    if manifest.get("generator") != "scripts/render_thesis_extension_results.py":
        raise RenderError("generador lógico inesperado")
    if manifest.get("blog_layout_adjustments") != LAYOUT_ADJUSTMENTS:
        raise RenderError("ajustes de diagramación inesperados")
    if manifest.get("generator_sha256") != sha256(Path(__file__)):
        raise RenderError("drift del generador")
    entries = manifest.get("figures", [])
    if [entry.get("key") for entry in entries] != [spec.key for spec in SPECS]:
        raise RenderError("inventario o orden de figuras inesperado")
    for spec, entry in zip(SPECS, entries, strict=True):
        _validate_pair(spec, entry, output_dir)
    serialized_manifest = json.dumps(manifest, ensure_ascii=False)
    if PRIVATE_PATTERN.search(serialized_manifest):
        raise RenderError("manifiesto contiene ruta privada o identificador prohibido")


def _refresh_output_hash(
    manifest: dict[str, Any], output_dir: Path, key: str, lang: str
) -> None:
    entry = next(row for row in manifest["figures"] if row["key"] == key)
    output = entry["outputs"][lang]
    path = output_dir / output["filename"]
    output["sha256"] = sha256(path)
    output["bytes"] = path.stat().st_size


def run_negative_probe(name: str) -> int:
    with tempfile.TemporaryDirectory(prefix="thesis-results-probe-") as raw:
        output_dir = Path(raw)
        manifest = build_family(output_dir)
        if name == "spanish-residual-en":
            entry = next(row for row in manifest["figures"] if row["key"] == "v5")
            path = output_dir / entry["outputs"]["en"]["filename"]
            tree = _parse(path)
            title = next(
                element
                for element in tree.getroot()
                if _local_name(element.tag) == "title"
            )
            title.text = f"{title.text} · descripción residual"
            _write_tree(tree, path)
            _refresh_output_hash(manifest, output_dir, "v5", "en")
        elif name == "number-drift":
            entry = next(row for row in manifest["figures"] if row["key"] == "v5")
            path = output_dir / entry["outputs"]["en"]["filename"]
            text = path.read_text(encoding="utf-8").replace("346", "347", 1)
            path.write_text(text, encoding="utf-8")
            _refresh_output_hash(manifest, output_dir, "v5", "en")
        elif name == "missing-accessibility":
            entry = next(row for row in manifest["figures"] if row["key"] == "v10")
            path = output_dir / entry["outputs"]["en"]["filename"]
            tree = _parse(path)
            tree.getroot().attrib.pop("role", None)
            _write_tree(tree, path)
            _refresh_output_hash(manifest, output_dir, "v10", "en")
        elif name == "stale-source-hash":
            manifest["figures"][0]["source_csv_sha256"] = "0" * 64
        elif name == "translated-not-estimable":
            entry = next(row for row in manifest["figures"] if row["key"] == "v6")
            path = output_dir / entry["outputs"]["en"]["filename"]
            text = path.read_text(encoding="utf-8").replace(
                "NOT_ESTIMABLE", "NOT ESTIMABLE"
            )
            path.write_text(text, encoding="utf-8")
            _refresh_output_hash(manifest, output_dir, "v6", "en")
        elif name == "private-path":
            entry = next(row for row in manifest["figures"] if row["key"] == "v10")
            path = output_dir / entry["outputs"]["en"]["filename"]
            text = path.read_text(encoding="utf-8").replace(
                "UNAUTHORIZED JUMP", "/home/private/UNAUTHORIZED JUMP", 1
            )
            path.write_text(text, encoding="utf-8")
            _refresh_output_hash(manifest, output_dir, "v10", "en")
        else:
            raise RenderError(f"canario desconocido: {name}")
        _write_json(manifest, output_dir / MANIFEST_PATH.name)
        try:
            validate_family(output_dir)
        except RenderError as error:
            print(f"NEGATIVE_PROBE_REJECTED {name}: {error}")
            return 2
    print(f"NEGATIVE_PROBE_ACCEPTED_UNEXPECTEDLY {name}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument(
        "--probe-negative",
        choices=(
            "spanish-residual-en",
            "number-drift",
            "missing-accessibility",
            "stale-source-hash",
            "translated-not-estimable",
            "private-path",
        ),
    )
    args = parser.parse_args()
    try:
        if args.probe_negative:
            return run_negative_probe(args.probe_negative)
        if args.check:
            validate_family()
            print("THESIS_EXTENSION_RESULTS_VALID figures=6 languages=2")
            return 0
        manifest = build_family()
        print(
            "THESIS_EXTENSION_RESULTS_BUILT "
            f"figures={len(manifest['figures'])} languages={len(manifest['languages'])}"
        )
        return 0
    except (OSError, ValueError, ET.ParseError, json.JSONDecodeError) as error:
        print(f"THESIS_EXTENSION_RESULTS_INVALID {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
