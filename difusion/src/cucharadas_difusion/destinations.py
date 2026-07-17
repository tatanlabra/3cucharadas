from __future__ import annotations

from pathlib import Path
from typing import Any

from .posts import PostError, parse_post


def destination_status(repo: Path, ref: str) -> list[dict[str, Any]]:
    all_posts = []
    for path in sorted((repo / "_posts").glob("*.md")):
        try:
            all_posts.append(parse_post(path, repo))
        except PostError:
            continue
    pair = [post for post in all_posts if post.ref == ref]
    english = next((post for post in pair if post.lang == "en"), None)
    if english is None:
        raise PostError(f"No existe version EN para {ref}")
    republish = {str(item).lower() for item in english.distribution.get("republish", [])}

    def count_tag(tag: str, lang: str = "en") -> int:
        return sum(
            1
            for post in all_posts
            if post.lang == lang and tag.lower() in {item.lower() for item in post.tags}
        )

    return [
        {
            "destination": "dev",
            "status": "ready" if "dev" in republish else "blocked",
            "reason": "feed-dev-en.xml + revision humana" if "dev" in republish else "falta republish: dev",
        },
        {
            "destination": "medium",
            "status": "ready" if "medium" in republish else "blocked",
            "reason": "importar URL EN y verificar canonical" if "medium" in republish else "falta republish: medium",
        },
        {
            "destination": "juliabloggers",
            "status": "monitoring" if count_tag("julia") else "blocked",
            "reason": "feed enviado; esperar el siguiente ciclo semanal",
        },
        {
            "destination": "planet-python",
            "status": "ready" if count_tag("python") >= 2 else "blocked",
            "reason": f"{count_tag('python')}/2 posts Python EN",
        },
        {
            "destination": "r-bloggers",
            "status": "ready" if count_tag("r") >= 2 else "blocked",
            "reason": f"{count_tag('r')}/2 posts R EN; ademas requiere backlink",
        },
        {
            "destination": "osgeo-osm",
            "status": "ready" if count_tag("geo") + count_tag("openstreetmap") >= 2 else "blocked",
            "reason": f"{count_tag('geo') + count_tag('openstreetmap')}/2 posts geo/OSM EN",
        },
        {
            "destination": "econacademics",
            "status": "blocked",
            "reason": "requiere un post economico con referencia RePEc sustantiva",
        },
    ]


def destination_checklist(repo: Path, ref: str) -> str:
    rows = destination_status(repo, ref)
    lines = [f"# Checklist de destinos — {ref}", ""]
    for row in rows:
        mark = " " if row["status"] == "ready" else "x"
        lines.append(f"- [{mark}] {row['destination']}: {row['status']} — {row['reason']}")
    return "\n".join(lines) + "\n"
