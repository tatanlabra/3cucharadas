from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

import yaml

from .posts import PostError, parse_post

CATALOGO = Path(__file__).resolve().parents[2] / "config" / "destinos.yml"

LISTO = "listo"
BLOQUEADO = "bloqueado"
PENDIENTE = "pendiente-verificar"


def cargar_catalogo(path: Path | None = None) -> list[dict[str, Any]]:
    """Lee el catálogo declarativo de destinos.

    Antes esta lista estaba hardcodeada acá y sólo contemplaba destinos en
    inglés. Vive en YAML para que agregar un destino no exija tocar código y
    para que idioma y público queden declarados de forma auditable.
    """
    ruta = path or CATALOGO
    if not ruta.exists():
        raise PostError(f"No existe el catálogo de destinos: {ruta}")
    data = yaml.safe_load(ruta.read_text(encoding="utf-8")) or {}
    destinos = data.get("destinos")
    if not isinstance(destinos, list) or not destinos:
        raise PostError(f"Catálogo de destinos vacío o mal formado: {ruta}")
    return destinos


def _cargar_posts(repo: Path) -> list[Any]:
    posts = []
    for path in sorted((repo / "_posts").glob("*.md")):
        try:
            posts.append(parse_post(path, repo))
        except PostError:
            continue
    return posts


def _contar_tag(posts: list[Any], tag: str, lang: str) -> int:
    return sum(
        1
        for post in posts
        if post.lang == lang and tag.lower() in {item.lower() for item in post.tags}
    )


def _evaluar(
    destino: dict[str, Any],
    pareja: dict[str, Any],
    todos: list[Any],
) -> tuple[str, str]:
    requiere = destino.get("requiere") or {}
    faltas: list[str] = []

    lang_post = requiere.get("lang_post")
    if lang_post and lang_post not in pareja:
        # Un post sólo en español no es un error: simplemente no alcanza los
        # destinos anglófonos. Antes esto lanzaba excepción y dejaba el artículo
        # sin evaluar en ningún destino, ni siquiera los que sí le correspondían.
        return BLOQUEADO, f"no hay versión {lang_post}"

    republish = requiere.get("republish")
    if republish:
        post = pareja.get(lang_post or "en")
        declarados = {str(x).lower() for x in (post.distribution.get("republish") or [])}
        if str(republish).lower() not in declarados:
            faltas.append(f"falta republish: {republish}")

    for tag, minimo in (requiere.get("tags_min") or {}).items():
        n = _contar_tag(todos, tag, lang_post or "en")
        if n < int(minimo):
            faltas.append(f"{n}/{minimo} posts {lang_post or 'en'} con tag `{tag}`")

    if faltas:
        return BLOQUEADO, "; ".join(faltas)
    if requiere.get("verificado") is False:
        return PENDIENTE, "faltan por confirmar las reglas de envío del destino"
    return LISTO, str(destino.get("nota", "")).strip()


def destination_status(
    repo: Path, ref: str, catalogo: Path | None = None
) -> list[dict[str, Any]]:
    todos = _cargar_posts(repo)
    pareja = {post.lang: post for post in todos if post.ref == ref}
    if not pareja:
        raise PostError(f"No existe ningún post con ref {ref}")

    filas = []
    for destino in cargar_catalogo(catalogo):
        estado, razon = _evaluar(destino, pareja, todos)
        filas.append(
            {
                "destination": destino["id"],
                "lang": destino.get("lang"),
                "audiencia": destino.get("audiencia", []),
                "modo": destino.get("modo"),
                "status": estado,
                "reason": razon,
                "activos": destino.get("activos", []),
            }
        )
    return filas


def destination_checklist(repo: Path, ref: str, catalogo: Path | None = None) -> str:
    filas = destination_status(repo, ref, catalogo)
    idiomas = sorted({str(f["lang"]) for f in filas})
    lineas = [f"# Checklist de destinos — {ref}", ""]
    for idioma in idiomas:
        lineas.append(f"## {idioma}")
        lineas.append("")
        for fila in (f for f in filas if f["lang"] == idioma):
            marca = "x" if fila["status"] == LISTO else " "
            publico = ", ".join(fila["audiencia"]) or "—"
            lineas.append(
                f"- [{marca}] **{fila['destination']}** ({fila['modo']}, público: {publico})"
                f" — {fila['status']}: {fila['reason']}"
            )
            for activo in fila["activos"]:
                lineas.append(f"      · activo: `{activo}`")
        lineas.append("")
    return "\n".join(lineas).rstrip() + "\n"


def registrar_resolucion(
    repo: Path, ref: str, catalogo: Path | None = None
) -> Path:
    """Deja por escrito qué destinos corresponden a este artículo y por qué.

    El hook no publica: resuelve y registra. El archivo resultante es la
    trazabilidad de por qué un artículo fue o no a cada canal.
    """
    filas = destination_status(repo, ref, catalogo)
    destino_dir = repo / "difusion" / "state" / "destinos"
    destino_dir.mkdir(parents=True, exist_ok=True)
    salida = destino_dir / f"{ref}.json"
    salida.write_text(
        json.dumps(
            {
                "ref": ref,
                "resuelto_en": datetime.now(UTC).isoformat(timespec="seconds"),
                "listos": [f["destination"] for f in filas if f["status"] == LISTO],
                "destinos": filas,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return salida
