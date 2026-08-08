#!/usr/bin/env python3
"""Comprobaciones sobre el CSS COMPILADO del artefacto.

Se lee `assets/css/main.css` ya compilado y comprimido, no el `.scss` fuente: lo
que importa es lo que el navegador aplica. Sass está en `style: compressed`, así
que las comprobaciones toleran espacios opcionales y no dependen del formato.

Motivos:

- Tipografía: `.page__content { font-size: 0.8rem }` daba 12,8 px de cuerpo en
  móvil, porque el tema escala la raíz a 16/18/20/22 px por breakpoint. El
  defecto era máximo justo en la pantalla más pequeña, y componía hacia abajo
  (tablas 10,8 px, thead 9,5 px).
- Táctil: los controles medían 27x25 px, muy por debajo de 44x44.
- Sin JS: si la lista se oculta por CSS y el botón depende de JavaScript, la
  navegación queda inalcanzable cuando el script no carga.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import report, require_artifact  # noqa: E402


def load_css(root: Path) -> str:
    path = root / "assets" / "css" / "main.css"
    if not path.exists():
        sys.exit(f"ERROR: no existe {path}. Construir el sitio primero.")
    return path.read_text("utf-8", errors="replace")


def has(css: str, pattern: str) -> bool:
    return re.search(pattern, css, re.I | re.S) is not None


def check_typography(css: str) -> int:
    problems = []

    if has(css, r"\.page__content\s*\{[^}]*font-size\s*:\s*0?\.8\s*rem"):
        problems.append(
            ".page__content sigue en 0.8rem (12,8 px en móvil): la regla no se corrigió"
        )

    # El cuerpo lleva su propia escala en px, desacoplada de la raíz. Se exige
    # suelo de 16 px —el mínimo que no obliga a hacer zoom en un móvil— y un techo
    # explícito para que la medida no se descontrole en pantallas anchas.
    clamp = re.search(
        r"\.page__content\s*\{[^}]*font-size\s*:\s*clamp\(\s*(\d+)px\s*,[^,]+,\s*(\d+)px\s*\)",
        css, re.I | re.S,
    )
    if not clamp:
        problems.append(".page__content no fija un clamp() en px con suelo y techo")
    else:
        floor, cap = int(clamp.group(1)), int(clamp.group(2))
        if floor < 16:
            problems.append(f"el suelo del cuerpo es {floor}px; se exige >= 16px")
        if cap > 20:
            problems.append(f"el techo del cuerpo es {cap}px; se exige <= 20px")

    # line-height >= 1.5 dentro de párrafos (WCAG 1.4.12).
    match = re.search(r"\.page__content\s*\{[^}]*line-height\s*:\s*([\d.]+)", css, re.I | re.S)
    if not match:
        problems.append(".page__content no declara line-height")
    elif float(match.group(1)) < 1.5:
        problems.append(
            f".page__content tiene line-height {match.group(1)}; WCAG 1.4.12 pide >= 1.5"
        )

    # La raíz gobierna TODA la interfaz, no sólo el cuerpo: neutralizar la
    # escalera del tema encogió cabecera, logo y botones. El cuerpo se corrige
    # aparte, y esta comprobación impide que la corrección vuelva a ese atajo.
    if re.search(r"(^|\})\s*html\s*\{[^}]*font-size\s*:\s*\d+(\.\d+)?%", css, re.I):
        problems.append(
            "se está sobrescribiendo la escalera de raíz del tema; eso reescala toda la interfaz"
        )

    # El encadenamiento de em que llevaba thead a 9,5 px.
    if has(css, r"thead\s+th\s*\{[^}]*font-size\s*:\s*0?\.88\s*em"):
        problems.append("thead th mantiene font-size: 0.88em, que compone hacia abajo")

    return report("cuerpo legible sin reescalar la interfaz", problems, 6)


def check_touch_targets(css: str) -> int:
    problems = []

    if not has(css, r"max\(\s*100%\s*,\s*44px\s*\)"):
        problems.append(
            "no se encontró el área táctil de 44 px (se esperaba max(100%, 44px) en un ::after)"
        )
    if not has(css, r"@media[^{]*pointer\s*:\s*coarse"):
        problems.append("no hay bloque @media (pointer: coarse) para separar los objetivos táctiles")
    if not has(css, r"\.masthead__controls"):
        problems.append("no existe la regla .masthead__controls")

    return report("objetivos táctiles >= 44 px", problems, 3)


def check_no_js_fallback(css: str) -> int:
    problems = []

    if not has(css, r"\.masthead__nav-list"):
        problems.append("no existe la regla .masthead__nav-list")
    if not has(css, r"\.masthead__nav-toggle"):
        problems.append("no existe la regla .masthead__nav-toggle")

    # El gancho CSS debe ser el propio atributo ARIA: así presentación y
    # accesibilidad no pueden divergir.
    if not has(css, r"aria-expanded"):
        problems.append("el panel no se abre con [aria-expanded=\"true\"]; ARIA y CSS pueden divergir")

    # Sin JS la lista debe seguir siendo visible y el botón desaparecer.
    if not has(css, r"\.no-js[^{]*\.masthead__nav-list"):
        problems.append("falta el fallback .no-js para .masthead__nav-list")
    if not has(css, r"\.no-js[^{]*\.masthead__nav-toggle\s*\{[^}]*display\s*:\s*none"):
        problems.append("falta ocultar .masthead__nav-toggle bajo .no-js")

    return report("navegación alcanzable sin JavaScript", problems, 5)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("artifact")
    parser.add_argument("--typography", action="store_true")
    parser.add_argument("--touch-targets", action="store_true")
    parser.add_argument("--no-js-fallback", action="store_true")
    args = parser.parse_args()

    css = load_css(require_artifact(args.artifact))
    modes = [
        (args.typography, check_typography),
        (args.touch_targets, check_touch_targets),
        (args.no_js_fallback, check_no_js_fallback),
    ]
    selected = [fn for flag, fn in modes if flag] or [fn for _, fn in modes]
    return max(fn(css) for fn in selected)


if __name__ == "__main__":
    sys.exit(main())
