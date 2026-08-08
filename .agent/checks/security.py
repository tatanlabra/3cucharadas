#!/usr/bin/env python3
"""Controles de seguridad verificables sobre el código fuente del repositorio.

Estos comprobadores fijan cuatro correcciones concretas para que no se pierdan
en una edición futura. No pretenden ser un escáner general.

Contexto: el plan de seguridad original asumía GitHub Pages como producción. La
realidad verificada es GitLab Pages (`.gitlab-ci.yml`, job `pages`, artefacto
`public/`); GitHub es espejo y redirector. Esa corrección de premisa cambia las
prioridades: el riesgo de cadena de suministro más grave estaba en el pipeline
de GitLab, no en los workflows de GitHub.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _common import report  # noqa: E402

REPO = Path(__file__).resolve().parents[2]

# `curl … | bash`, `wget … | sh`, con o sin sudo. El pipe es lo que importa.
PIPE_TO_SHELL = re.compile(
    r"(curl|wget)\b[^\n|]*\|\s*(sudo\s+)?(ba)?sh\b",
    re.I,
)
SHA40 = re.compile(r"^[0-9a-f]{40}$")
USES = re.compile(r"^\s*-?\s*uses\s*:\s*(\S+)", re.M)
WRITE_PERM = re.compile(r"^\s*(contents|packages|id-token|deployments)\s*:\s*write", re.M)


def check_pipeline() -> int:
    """Riesgo P0: ejecución de código remoto no pinneado, como root, en el job
    que construye el artefacto publicado. Un compromiso del proveedor inyecta
    código arbitrario directamente en producción."""
    path = REPO / ".gitlab-ci.yml"
    if not path.exists():
        print("FAIL pipeline: no existe .gitlab-ci.yml")
        return 1

    problems = []
    for number, line in enumerate(path.read_text("utf-8").splitlines(), 1):
        if line.lstrip().startswith("#"):
            continue
        if PIPE_TO_SHELL.search(line):
            problems.append(f".gitlab-ci.yml:{number} canaliza una descarga remota a un shell")

    return report("pipeline sin ejecución remota sin verificar", problems, 1)


def check_liquid_escaping() -> int:
    """Los feeds RSS remotos se descargan durante el build y se hornean en el
    HTML publicado. Un `href` sin escapar acepta `javascript:` o `data:`, y
    `rel="noopener noreferrer"` NO mitiga esquemas de URL.

    Se comprueba el contexto de ATRIBUTO, que es donde vive el riesgo real. En
    texto, `{{ news.articles.size }}` es un entero y `{{ article.published |
    date: … }}` es una fecha ya formateada: marcarlos sería ruido que empuja a
    escapar cosas inertes y a desconfiar del comprobador.
    """
    # Datos que llegan de un feed remoto durante el build.
    REMOTE = re.compile(r"\{\{-?\s*(article|entry|item|news)\.[^}]*\}\}", re.I)
    # Atributo HTML cuyo valor contiene al menos una interpolación.
    ATTR = re.compile(r"""([\w:-]+)\s*=\s*"([^"]*\{\{[^"]*)"|([\w:-]+)\s*=\s*'([^']*\{\{[^']*)'""")
    SAFE = re.compile(r"\|\s*(escape|escape_once|uri_escape|url_encode|cgi_escape|strip_html)\b")
    # Atributos que el navegador interpreta como URL navegable o ejecutable.
    URL_ATTRS = {"href", "src", "action", "formaction", "poster", "cite", "data", "srcset",
                 "background", "ping", "style"}

    problems = []
    checked = 0

    for path in sorted((REPO / "_includes").rglob("*.html")):
        text = path.read_text("utf-8", errors="replace")
        if not REMOTE.search(text):
            continue
        checked += 1
        rel = path.relative_to(REPO)
        for number, line in enumerate(text.splitlines(), 1):
            for match in ATTR.finditer(line):
                attribute = (match.group(1) or match.group(3) or "").lower()
                value = match.group(2) or match.group(4) or ""
                for expression in REMOTE.finditer(value):
                    if SAFE.search(expression.group(0)):
                        continue
                    severity = "URL" if attribute in URL_ATTRS else "atributo"
                    problems.append(
                        f"{rel}:{number} dato remoto sin escapar en {severity} "
                        f"'{attribute}': {expression.group(0).strip()}"
                    )

    return report("interpolaciones Liquid escapadas", problems, checked)


def check_actions_pinned() -> int:
    """Un workflow con permisos de escritura y un secreto es la única superficie
    del repo capaz de modificar la rama. Ahí el pinning a SHA no es opcional."""
    workflows = sorted((REPO / ".github" / "workflows").glob("*.yml"))
    if not workflows:
        print("OK   pinning de acciones: no hay workflows de GitHub")
        return 0

    problems = []
    for path in workflows:
        text = path.read_text("utf-8")
        if not WRITE_PERM.search(text):
            continue  # solo se exige a los que pueden escribir
        rel = path.relative_to(REPO)
        for match in USES.finditer(text):
            ref = match.group(1)
            if "@" not in ref:
                problems.append(f"{rel}: '{ref}' sin referencia fijada")
                continue
            version = ref.rsplit("@", 1)[1].strip("\"'")
            if not SHA40.match(version):
                problems.append(f"{rel}: '{ref}' usa una etiqueta móvil, no un SHA de 40 caracteres")

    return report("acciones con permiso de escritura pinneadas a SHA", problems, len(workflows))


def check_dependabot() -> int:
    """Sin actualización automática, el pinning exacto de npm convierte el drift
    de dependencias en silencioso."""
    path = REPO / ".github" / "dependabot.yml"
    if not path.exists():
        print("FAIL dependabot: no existe .github/dependabot.yml")
        return 1

    try:
        import yaml
    except ImportError:
        print("FAIL dependabot: falta PyYAML para validar el archivo")
        return 1

    data = yaml.safe_load(path.read_text("utf-8")) or {}
    declared = {u.get("package-ecosystem") for u in (data.get("updates") or [])}

    expected = {"github-actions"}
    if (REPO / "Gemfile").exists():
        expected.add("bundler")
    if (REPO / "package.json").exists():
        expected.add("npm")

    problems = [f"falta el ecosistema '{eco}', que sí está presente en el repo" for eco in sorted(expected - declared)]
    return report("dependabot cubre los ecosistemas presentes", problems, len(expected))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pipeline", action="store_true")
    parser.add_argument("--liquid-escaping", action="store_true")
    parser.add_argument("--actions-pinned", action="store_true")
    parser.add_argument("--dependabot", action="store_true")
    args = parser.parse_args()

    modes = [
        (args.pipeline, check_pipeline),
        (args.liquid_escaping, check_liquid_escaping),
        (args.actions_pinned, check_actions_pinned),
        (args.dependabot, check_dependabot),
    ]
    selected = [fn for flag, fn in modes if flag] or [fn for _, fn in modes]
    return max(fn() for fn in selected)


if __name__ == "__main__":
    sys.exit(main())
