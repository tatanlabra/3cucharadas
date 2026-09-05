#!/usr/bin/env python3
"""Generate English D2-map SVGs from the reviewed Spanish masters."""

from __future__ import annotations

from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets" / "images" / "structured-shell"

JOBS = {
    "fig-d2-familias-shell.svg": {
        "output": "fig-d2-shell-families-en.svg",
        "replacements": {
            "D2: Familias de shell y el lugar de Nushell": "D2: Shell families and where Nushell fits",
            "Mapa conceptual. Las shells de texto sh, Bash y zsh transportan texto por sus tuberías. Fish es una shell interactiva no POSIX. Nushell transporta registros, columnas y fechas como valores tipados. PowerShell transporta objetos del ecosistema .NET. El post compara solamente la ruta selectiva entre zsh y Nushell y no clasifica a las demás shells.": "Conceptual map. Text shells sh, Bash, and zsh carry text through pipelines. Fish is an interactive non-POSIX shell. Nushell carries records, columns, and dates as typed values. PowerShell carries objects from the .NET ecosystem. The post compares only selective routing between zsh and Nushell; it does not rank the other shells.",
            "D2 · ORIENTACIÓN, NO RANKING": "D2 · ORIENTATION, NOT A RANKING",
            "No todas las shells transportan lo mismo": "Shells do not all carry the same data",
            "El nombre «shell» no basta para decidir qué herramienta conviene usar.": "The word ‘shell’ alone does not tell you which tool fits.",
            "TUBERÍAS DE TEXTO": "TEXT PIPELINES",
            "Los programas se pasan texto entre sí.": "Programs exchange text with each other.",
            "Orquestación habitual de comandos.": "Standard command orchestration.",
            "INTERACTIVA": "INTERACTIVE",
            "Prioriza la experiencia interactiva.": "Focuses on interactive use.",
            "No es POSIX; recibe salida textual de CLI.": "Non-POSIX; consumes CLI text output.",
            "SHELL ESTRUCTURADA": "STRUCTURED SHELL",
            "Registros, columnas, números y fechas.": "Records, columns, numbers, and dates.",
            "La estructura cambia la operación.": "Structure changes the operation.",
            "OBJETOS .NET": ".NET OBJECTS",
            "Encadena objetos tipados de .NET.": "Pipes typed .NET objects.",
            "Otra familia estructurada, fuera de esta prueba.": "Another structured family, outside this test.",
            "LA PREGUNTA OPERATIVA DEL POST": "THE POST’S OPERATING QUESTION",
            "¿Hay registros, columnas, fechas o agrupaciones que aprovechar?": "Can the task exploit records, columns, dates, or grouping?",
            "No: conserva una CLI nativa o una utilidad acotada.": "No: keep the native CLI or a focused utility.",
            "Si el volumen o el análisis crecen: DuckDB, Python, Polars o R.": "If scale or analysis grows: DuckDB, Python, Polars, or R.",
            "Alcance: este experimento compara una ruta zsh → Nushell en Linux;": "Scope: this experiment tests selective zsh → Nushell routing on Linux;",
            "no mide cuál shell es «mejor» en general.": "it does not rank shells overall.",
            "Las utilidades y los motores de datos no son shells: ocupan otras capas de la decisión.": "Utilities and data engines are not shells: they sit at other decision layers.",
        },
    },
    "fig-d2-familias-shell-mobile.svg": {
        "output": "fig-d2-shell-families-mobile-en.svg",
        "replacements": {
            "D2: Familias de shell y el lugar de Nushell": "D2: Shell families and where Nushell fits",
            "Versión móvil del mapa conceptual. Las shells de texto sh, Bash y zsh transportan texto. Fish prioriza la interacción y no es POSIX. Nushell transporta valores tipados. PowerShell transporta objetos .NET. El post compara solamente zsh con una ruta selectiva de Nushell.": "Mobile version of the conceptual map. Text shells sh, Bash, and zsh carry text. Fish prioritises interactive use and is not POSIX. Nushell carries typed values. PowerShell carries .NET objects. The post compares only zsh with a selective Nushell route.",
            "D2 · ORIENTACIÓN, NO RANKING": "D2 · ORIENTATION, NOT A RANKING",
            "No todas las shells": "Shells do not all carry",
            "transportan lo mismo": "the same data",
            "El nombre «shell» no basta para decidir": "The word ‘shell’ alone does not tell you",
            "qué herramienta conviene usar.": "which tool fits.",
            "TUBERÍAS DE TEXTO": "TEXT PIPELINES",
            "Los programas se pasan texto": "Programs exchange text",
            "entre sí.": "with each other.",
            "Orquestación habitual de comandos.": "Standard command orchestration.",
            "INTERACTIVA": "INTERACTIVE",
            "Prioriza la experiencia": "Focuses on interactive use;",
            "interactiva; no es POSIX.": "it is not POSIX.",
            "Recibe salida textual de CLI.": "Consumes CLI text output.",
            "SHELL ESTRUCTURADA": "STRUCTURED SHELL",
            "Registros, columnas, números": "Records, columns, numbers,",
            "y fechas como valores tipados.": "and dates as typed values.",
            "La estructura cambia la operación.": "Structure changes the operation.",
            "OBJETOS .NET": ".NET OBJECTS",
            "Encadena objetos tipados": "Pipes typed objects",
            "del ecosistema .NET.": "from the .NET ecosystem.",
            "Fuera de esta prueba zsh → Nushell.": "Outside this zsh → Nushell test.",
            "LA PREGUNTA OPERATIVA": "THE OPERATING QUESTION",
            "¿Hay registros, columnas o fechas": "Can the task exploit records, columns,",
            "que aprovechar?": "dates, or grouping?",
            "No: conserva la herramienta nativa.": "No: keep the native tool.",
            "Si crece: DuckDB, Python, Polars o R.": "If it grows: DuckDB, Python, Polars, or R.",
            "Alcance: ruta zsh → Nushell en Linux.": "Scope: zsh → Nushell routing on Linux.",
            "No decide qué shell es «mejor» en general.": "It does not rank shells overall.",
            "Utilidades y motores de datos ocupan otras capas.": "Utilities and data engines sit at other layers.",
        },
    },
}


def render(source_name: str, job: dict[str, object]) -> None:
    source = ASSETS / source_name
    output = ASSETS / str(job["output"])
    content = source.read_text(encoding="utf-8")
    for old, new in dict(job["replacements"]).items():
        count = content.count(old)
        if count != 1:
            raise SystemExit(f"{source_name}: expected one occurrence of {old!r}, found {count}")
        content = content.replace(old, new)
    if "/home/" in content or "file:" in content:
        raise SystemExit(f"{source_name}: local path leaked into generated SVG")
    output.write_text(content, encoding="utf-8")
    print(f"PASS {source.name} -> {output.name}")


def main() -> None:
    for source_name, job in JOBS.items():
        render(source_name, job)


if __name__ == "__main__":
    main()
