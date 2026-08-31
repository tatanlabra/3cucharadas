#!/usr/bin/env python3
"""Genera la proyección pública 3D desde la memoria canónica de penta-agent.

Nodos    = lecciones (`strategy_key`) de `experience-lessons.yaml`.
Temas    = comunidades detectadas sobre el grafo semantico (modularidad) + etiqueta TF-IDF.
Aristas  = semanticas (k-NN coseno sobre centroides de embeddings en Qdrant)
           + estructurales (co-ocurrencia por tool/repo/transport).
Analitica= ranking de errores frecuentes y candidatos de mejora (fallos / obsoletas utiles).
Salida   = JSON del grafo + HTML autocontenido (vendor JS + datos inline).

Uso:
    # Reproduce el HTML publicado exclusivamente desde el JSON ya saneado.
    /opt/entornos/mamba312/bin/python scripts/penta_rag_graph/build_graph.py --check-public

    # Actualiza la proyección pública desde la memoria local y el índice derivado.
    /opt/entornos/mamba312/bin/python scripts/penta_rag_graph/build_graph.py --sanitize

El modo de render público no lee Qdrant, correo ni la memoria canónica. El modo
--sanitize sí los lee localmente, pero sólo escribe los dos artefactos públicos
saneados del sitio. Nunca escribe una exportación privada por omisión.
"""
from __future__ import annotations

import argparse
import colorsys
import json
import math
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import yaml

# --- Rutas y constantes -----------------------------------------------------
HERE = Path(__file__).resolve().parent
SITE_ROOT = HERE.parents[1]
WORKSPACE_ROOT = HERE.parents[3]
PENTA_AGENT_ROOT = WORKSPACE_ROOT / "penta-agent"
LESSONS = PENTA_AGENT_ROOT / "memory" / "experience-lessons.yaml"
EVENTS = PENTA_AGENT_ROOT / "memory" / "experience-events.jsonl"
VENDOR_JS = HERE / "vendor" / "3d-force-graph.min.js"
TEMPLATE = HERE / "rag-graph.template.html"
PUBLIC_GRAPH = SITE_ROOT / "assets" / "data" / "rag_knowledge_graph" / "public-graph.json"
PUBLIC_HTML = SITE_ROOT / "assets" / "visualizations" / "penta-rag-knowledge-graph" / "index.html"

COLLECTION = "penta_experience_v1"
QDRANT_URL = os.environ.get("PENTA_AGENT_QDRANT_URL", "http://localhost:6333").rstrip("/")

# helpers de clasificacion de la memoria (Fase A/B); import guardado
sys.path.insert(0, str(PENTA_AGENT_ROOT / "scripts"))
try:
    import experience_memory as _em  # type: ignore
except Exception:  # pragma: no cover
    _em = None

STATUS_COLOR = {
    "preferred": "#9ece6a", "viable": "#7aa2f7", "deprioritized": "#e0af68",
    "blocked": "#f7768e", "stale": "#565f89",
}
DEFAULT_COLOR = "#a9b1d6"
NO_CLUSTER_COLOR = "#3b4261"

SEMANTIC_K = 5           # vecinos por nodo
SEMANTIC_MIN_SIM = 0.62  # umbral base de similitud coseno
STRUCT_MAX_GROUP = 40    # cap de miembros por grupo estructural

# Capa editorial derivada: traduce trazas de ejecución a familias de trabajo
# reconocibles. No sustituye `strategy_key` ni pretende entender la intención
# humana; es una clasificación determinista, visible y revisable para que el
# visor no obligue a leer comandos antes de saber qué tipo de labor representa.
TASK_FAMILIES = (
    {
        "id": "coordination",
        "label": "Coordinar agentes y decisiones",
        "description": "Handoffs, contexto, delegación y reglas para que el trabajo continúe sin perder su razón.",
        "color": "#c678dd",
        "tokens": ("context", "handoff", "delegate", "delegat", "agy", "router", "queue", "workspace", "agent"),
    },
    {
        "id": "research",
        "label": "Investigar y analizar datos",
        "description": "Explorar fuentes, datos y evidencia para la tesis, documentos de trabajo o bibliografía.",
        "color": "#61afef",
        "tokens": ("tesis", "thesis", "pandas", "pyarrow", "parquet", "stata", "dataframe", "csv", "xlsx", "dta", "paper", "bibliog", "casen", "rsh", "dataset"),
    },
    {
        "id": "validation",
        "label": "Probar y verificar",
        "description": "Tests, gates y revisiones que distinguen una mejora comprobada de una apariencia de mejora.",
        "color": "#98c379",
        "tokens": ("pytest", "test", "validate", "verify", "check", "lint", "gate", "smoke", "regression", "falsifi"),
    },
    {
        "id": "versioning",
        "label": "Versionar y comparar cambios",
        "description": "Revisar diferencias, estados y trazabilidad de cambios antes de conservar o entregar una modificación.",
        "color": "#e5c07b",
        "tokens": ("git", "diff", "commit", "branch", "lazygit", "gitui", "status"),
    },
    {
        "id": "publishing",
        "label": "Editar y comunicar",
        "description": "Escribir, estructurar y preparar artefactos legibles: documentación, visualizaciones y publicaciones.",
        "color": "#e06c75",
        "tokens": ("write", "edit", "jekyll", "markdown", "draft", "post", "html", "css", "telegra", "linkedin", "rss"),
    },
    {
        "id": "operations",
        "label": "Operar herramientas y servicios",
        "description": "Usar infraestructura, modelos, índices y automatizaciones para que un flujo pueda ejecutarse de forma controlada.",
        "color": "#56b6c2",
        "tokens": ("docker", "systemd", "ssh", "qdrant", "server", "service", "network", "quota", "plasmoid", "kde", "remote", "ollama", "mcp"),
    },
    {
        "id": "inspection",
        "label": "Leer y rastrear evidencia",
        "description": "Localizar, abrir y contrastar archivos, resultados y antecedentes antes de intervenirlos.",
        "color": "#d19a66",
        "tokens": ("read", "cat", "sed", "rg", "grep", "find", "ls", "head", "tail", "open", "inspect", "pdf", "file"),
    },
    {
        "id": "execution",
        "label": "Ejecutar y automatizar",
        "description": "Pasos de shell o código que implementan una tarea después de revisar su contexto y sus límites.",
        "color": "#abb2bf",
        "tokens": (),
    },
)

# tokens sin valor tematico para etiquetar comunidades
STOP_TOKENS = {
    "path", "the", "and", "for", "with", "eof", "true", "false", "null", "none",
    "generic", "tmp", "var", "echo", "sp", "cd", "usr", "bin", "home", "ende",
    "programaciones", "penta", "agent", "http", "https", "www", "com", "org",
    "de", "la", "el", "en", "que", "los", "las", "del", "por", "con", "una",
}


# --- Qdrant (REST, stdlib) --------------------------------------------------
def qdrant_scroll_all() -> list[dict[str, Any]]:
    url = f"{QDRANT_URL}/collections/{COLLECTION}/points/scroll"
    points: list[dict[str, Any]] = []
    next_offset: Any = None
    while True:
        body: dict[str, Any] = {"limit": 512, "with_payload": True, "with_vector": True}
        if next_offset is not None:
            body["offset"] = next_offset
        req = urllib.request.Request(
            url, data=json.dumps(body).encode(), headers={"Content-Type": "application/json"}
        )
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read())
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            print(f"[warn] Qdrant no disponible ({exc}); sin aristas semanticas.", file=sys.stderr)
            return []
        result = data.get("result", {})
        batch = result.get("points", [])
        points.extend(batch)
        next_offset = result.get("next_page_offset")
        if not next_offset or not batch:
            break
    return points


def centroids_by_strategy(points: list[dict[str, Any]]) -> tuple[dict[str, np.ndarray], dict[str, Counter]]:
    vecs: dict[str, list[np.ndarray]] = defaultdict(list)
    agents: dict[str, Counter] = defaultdict(Counter)
    for p in points:
        payload = p.get("payload") or {}
        sk = payload.get("strategy_key")
        vec = p.get("vector")
        # Qdrant permite colecciones con un vector sin nombre (lista) o con
        # vectores nombrados. `penta_experience_v1` migró a `dense`/1024-dim;
        # mantener ambos contratos evita que el visor silenciosamente pierda
        # sus aristas semánticas al evolucionar el backend.
        if isinstance(vec, dict):
            vec = vec.get("dense")
        if not sk or not vec:
            continue
        vecs[sk].append(np.asarray(vec, dtype=np.float32))
        if payload.get("agent"):
            agents[sk][payload["agent"]] += 1
    centroids: dict[str, np.ndarray] = {}
    for sk, arr in vecs.items():
        c = np.mean(np.stack(arr), axis=0)
        n = np.linalg.norm(c)
        centroids[sk] = c / n if n > 0 else c
    return centroids, agents


# --- Nodos y aristas --------------------------------------------------------
def load_lessons() -> list[dict[str, Any]]:
    doc = yaml.safe_load(LESSONS.read_text(encoding="utf-8"))
    return doc.get("lessons", []) if isinstance(doc, dict) else []


def load_events() -> list[dict[str, Any]]:
    if not EVENTS.exists():
        return []
    out = []
    for line in EVENTS.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def norm_project(repo: str) -> str:
    """repo_scope (ruta) -> nombre de proyecto legible; colapsa dirs temporales."""
    if not repo:
        return ""
    base = os.path.basename(repo.rstrip("/"))
    # colapsa sufijos temporales aleatorios (p.ej. -gemini-validate.zOrUvL / .FW5MXV)
    if "." in base:
        head, _, suf = base.rpartition(".")
        looks_random = 4 <= len(suf) <= 8 and (any(c.isdigit() for c in suf) or
                       (any(c.isupper() for c in suf) and any(c.islower() for c in suf)))
        if head and looks_random and suf.lower() not in ("io", "com", "org", "net", "html", "json"):
            base = head
    base = re.sub(r"-(gemini|claude|codex)-validate$", "", base)
    base = re.sub(r"-roundtrip$", "", base)
    return base


# builtins de shell que NO son librerias/herramientas informativas
SHELL_BUILTINS = {"cd", "echo", "export", "source", "set", "true", "false", "sleep",
                  "pkill", "mkdir", "ln", "ls", "cp", "mv", "rm", "cat", "touch",
                  "cd;", "printf", "read", "eval", "exit", "unset", "test", "["}


# nombres que son subcarpetas de trabajo, no proyectos reales (se agrupan como "(varios)")
NON_PROJECTS = {"scratchpad", "reports", "vendor", "ui", "activos", "tmp", "memory", "tasks", ""}


def aggregate_projects(events, nodes):
    """Agrega metrica por proyecto (repo_scope) y adjunta proyecto dominante a cada nodo."""
    node_by_id = {n["id"]: n for n in nodes}
    strat_projects = defaultdict(Counter)     # strategy_key -> Counter(project)
    proj = defaultdict(lambda: {"events": 0, "successes": 0, "failures": 0,
                                "errors": Counter(), "failing": Counter(), "agents": Counter()})
    total_events = total_fail = 0
    for e in events:
        p = norm_project(e.get("repo_scope") or "")
        if p in NON_PROJECTS:
            p = "(varios)"
        sk = e.get("strategy_key")
        status = e.get("status")
        if sk:
            strat_projects[sk][p] += 1
        d = proj[p]
        d["events"] += 1
        total_events += 1
        if e.get("agent"):
            d["agents"][e["agent"]] += 1
        if status == "success":
            d["successes"] += 1
        elif status == "failure":
            d["failures"] += 1
            total_fail += 1
            ec = e.get("error_class") or "sin_clase"
            d["errors"][ec] += 1
            if sk:
                d["failing"][sk] += 1

    # adjunta proyecto dominante a nodos
    for n in nodes:
        pc = strat_projects.get(n["id"])
        if pc:
            n["project"] = pc.most_common(1)[0][0]
            n["projects"] = [p for p, _ in pc.most_common(4)]
        else:
            n["project"] = norm_project(n.get("repo") or "") or "(varios)"
            n["projects"] = [n["project"]]

    # paleta de proyectos (top por eventos)
    ranked = sorted(proj.items(), key=lambda kv: kv[1]["events"], reverse=True)
    palette = {}
    for i, (name, _) in enumerate(ranked):
        palette[name] = hsl_hex((0.12 + i * 0.61803398875) % 1.0, 0.5, 0.6)
    for n in nodes:
        n["projectColor"] = palette.get(n["project"], "#3b4261")

    projects_meta = []
    for name, d in ranked:
        tot = d["successes"] + d["failures"]
        projects_meta.append({
            "name": name, "events": d["events"],
            "successes": d["successes"], "failures": d["failures"],
            "fail_rate": round(d["failures"] / tot, 3) if tot else 0.0,
            "color": palette[name],
            "top_errors": [{"error_class": k, "count": v} for k, v in d["errors"].most_common(5)],
            "top_failing": [{"id": k, "count": v} for k, v in d["failing"].most_common(6)],
            "top_agent": d["agents"].most_common(1)[0][0] if d["agents"] else "",
        })
    coverage = {
        "total_events": total_events, "total_failures": total_fail,
        "fail_rate": round(total_fail / total_events, 4) if total_events else 0.0,
        "library_signal_recorded": False,
        "note": ("El RAG registra fallos por error_class y proyecto, pero NO clasifica "
                 "'mal uso de librería/función' (señal wrong_library_pattern sin datos). "
                 "Los fallos se concentran en delegación a CLIs externas y sandbox."),
    }
    return projects_meta, coverage


def build_nodes(lessons: list[dict[str, Any]], agents: dict[str, Counter]) -> list[dict[str, Any]]:
    nodes = []
    for les in lessons:
        sk = les.get("strategy_key")
        if not sk:
            continue
        ev = les.get("evidence") or {}
        succ = int(ev.get("successes") or 0)
        fail = int(ev.get("failures") or 0)
        status = les.get("status") or "viable"
        dominant_agent = agents.get(sk).most_common(1)[0][0] if agents.get(sk) else ""
        label = sk if len(sk) <= 64 else sk[:61] + "..."
        total = succ + fail
        nodes.append({
            "id": sk, "label": label, "status": status,
            "confidence": round(float(les.get("confidence") or 0.0), 3),
            "tool": les.get("tool_name") or "", "transport": les.get("transport") or "",
            "agent": dominant_agent, "repo": les.get("repo_scope") or "",
            "successes": succ, "failures": fail,
            "success_rate": round(succ / total, 3) if total else None,
            "last_success_at": (ev.get("last_success_at") or ""),
            "error_classes": ev.get("error_classes") or [],
            "val": round(math.log(total + 1) + 1.0, 3),
            "statusColor": STATUS_COLOR.get(status, DEFAULT_COLOR),
        })
    return nodes


def classify_task_family(node: dict[str, Any]) -> dict[str, str]:
    """Clasifica una traza por reglas públicas; conserva el identificador original."""
    haystack = " ".join(str(node.get(key) or "") for key in ("id", "tool", "transport", "repo")).lower()
    for family in TASK_FAMILIES:
        if any(re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", haystack) for token in family["tokens"]):
            return family
    return TASK_FAMILIES[-1]


def annotate_task_families(nodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Anota nodos y agrega un resumen entendible de tipos de trabajo."""
    family_by_id = {family["id"]: family for family in TASK_FAMILIES}
    totals: dict[str, dict[str, int]] = defaultdict(lambda: {"strategies": 0, "successes": 0, "failures": 0})
    for node in nodes:
        family = classify_task_family(node)
        node["task_family"] = family["id"]
        node["task_label"] = family["label"]
        node["task_description"] = family["description"]
        node["taskColor"] = family["color"]
        total = totals[family["id"]]
        total["strategies"] += 1
        total["successes"] += node["successes"]
        total["failures"] += node["failures"]

    ordered = []
    for family in TASK_FAMILIES:
        total = totals[family["id"]]
        if not total["strategies"]:
            continue
        observations = total["successes"] + total["failures"]
        ordered.append({
            "id": family["id"], "label": family["label"], "description": family["description"],
            "color": family["color"], **total,
            "success_rate": round(total["successes"] / observations, 3) if observations else None,
        })
    return ordered


def semantic_edges(nodes, centroids):
    ids = [n["id"] for n in nodes if n["id"] in centroids]
    if len(ids) < 2:
        return [], ids
    from sklearn.neighbors import NearestNeighbors
    mat = np.stack([centroids[i] for i in ids])
    k = min(SEMANTIC_K + 1, len(ids))
    nn = NearestNeighbors(n_neighbors=k, metric="cosine").fit(mat)
    dist, idx = nn.kneighbors(mat)
    seen, edges = set(), []
    for row, (drow, irow) in enumerate(zip(dist, idx)):
        for d, j in zip(drow, irow):
            if j == row:
                continue
            sim = 1.0 - float(d)
            if sim < SEMANTIC_MIN_SIM:
                continue
            a, b = ids[row], ids[j]
            key = (a, b) if a < b else (b, a)
            if key in seen:
                continue
            seen.add(key)
            edges.append({"source": a, "target": b, "kind": "semantic", "weight": round(sim, 3)})
    return edges, ids


def structural_edges(nodes):
    edges, seen = [], set()
    for attr in ("tool", "repo", "transport"):
        groups = defaultdict(list)
        for n in nodes:
            if n.get(attr):
                groups[n[attr]].append(n)
        for members in groups.values():
            if len(members) < 2:
                continue
            members = sorted(members, key=lambda n: n["confidence"], reverse=True)[:STRUCT_MAX_GROUP]
            hub = members[0]["id"]
            for m in members[1:]:
                key = (hub, m["id"], attr) if hub < m["id"] else (m["id"], hub, attr)
                if key in seen:
                    continue
                seen.add(key)
                edges.append({"source": hub, "target": m["id"], "kind": "structural", "attr": attr, "weight": 0.4})
    return edges


# --- Comunidades (temas) ----------------------------------------------------
def hsl_hex(h, s, l):
    r, g, b = colorsys.hls_to_rgb(h, l, s)
    return f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"


def tokenize(sk: str) -> list[str]:
    toks = re.split(r"[^a-z0-9]+", sk.lower())
    return [t for t in toks if len(t) >= 2 and t not in STOP_TOKENS and not t.isdigit()]


def detect_themes(nodes, sem_edges, sem_ids):
    """Detecta comunidades en el grafo semantico y las etiqueta con TF-IDF de tokens."""
    import networkx as nx
    from networkx.algorithms.community import greedy_modularity_communities

    node_by_id = {n["id"]: n for n in nodes}
    G = nx.Graph()
    G.add_nodes_from(sem_ids)
    for e in sem_edges:
        G.add_edge(e["source"], e["target"], weight=e["weight"])

    communities: list[set[str]] = []
    if G.number_of_edges() > 0:
        communities = [set(c) for c in greedy_modularity_communities(G, weight="weight")]
    # nodos sin arista semantica quedan como comunidad propia "sin conexion"
    covered = set().union(*communities) if communities else set()
    orphans = [n["id"] for n in nodes if n["id"] not in covered]

    # etiquetas TF-IDF: cada comunidad es un "documento" de tokens
    docs = []
    for comm in communities:
        c = Counter()
        for sk in comm:
            c.update(tokenize(sk))
        docs.append(c)
    dfreq = Counter()
    for c in docs:
        for tok in c:
            dfreq[tok] += 1
    ncom = max(len(docs), 1)

    clusters_meta = []
    cluster_of = {}
    # ordena comunidades por tamano (temas grandes primero)
    order = sorted(range(len(communities)), key=lambda i: len(communities[i]), reverse=True)
    for new_id, ci in enumerate(order):
        comm = communities[ci]
        c = docs[ci]
        scored = sorted(
            c.items(),
            key=lambda kv: kv[1] * math.log(1 + ncom / (dfreq[kv[0]] or 1)),
            reverse=True,
        )
        label_tokens = [t for t, _ in scored[:3]] or ["tema"]
        label = " · ".join(label_tokens)
        color = hsl_hex((new_id * 0.61803398875) % 1.0, 0.58, 0.62)
        members = [node_by_id[s] for s in comm]
        succ = sum(m["successes"] for m in members)
        fail = sum(m["failures"] for m in members)
        tools = Counter(m["tool"] for m in members if m["tool"])
        agents = Counter(m["agent"] for m in members if m["agent"])
        for s in comm:
            cluster_of[s] = new_id
            node_by_id[s]["cluster"] = new_id
            node_by_id[s]["clusterLabel"] = label
            node_by_id[s]["themeColor"] = color
        clusters_meta.append({
            "id": new_id, "label": label, "size": len(comm), "color": color,
            "successes": succ, "failures": fail,
            "success_rate": round(succ / (succ + fail), 3) if (succ + fail) else None,
            "top_tool": tools.most_common(1)[0][0] if tools else "",
            "top_agent": agents.most_common(1)[0][0] if agents else "",
            "keywords": label_tokens,
        })

    for s in orphans:
        node_by_id[s]["cluster"] = -1
        node_by_id[s]["clusterLabel"] = "sin conexión semántica"
        node_by_id[s]["themeColor"] = NO_CLUSTER_COLOR

    # marca aristas intra/inter-tema
    for e in sem_edges:
        cs, ct = cluster_of.get(e["source"]), cluster_of.get(e["target"])
        e["intra"] = bool(cs is not None and cs == ct)
    return clusters_meta


# --- Analitica: errores y mejora --------------------------------------------
def _error_signal(e):
    """(library, kind) de un evento: usa campos Fase A si existen, si no los deriva."""
    lib = e.get("error_library")
    kind = e.get("error_kind")
    if (not lib or not kind) and _em is not None:
        cmd = e.get("command") or ""
        try:
            if not kind:
                kind = _em.infer_error_kind(e.get("error_message_head"), e.get("exit_code"))
            if not lib:
                lib, _sym = _em.extract_error_library_and_symbol(e.get("error_message_head"), cmd, kind)
        except Exception:
            pass
    return (lib or ""), (kind or "")


def libraries_analytics(events, nodes):
    """Librerias/herramientas implicadas en FALLOS + adjunta libreria dominante a nodos."""
    node_by_id = {n["id"]: n for n in nodes}
    libs = defaultdict(lambda: {"failures": 0, "kinds": Counter(), "projects": Counter(), "strategies": Counter()})
    strat_lib = defaultdict(Counter)
    for e in events:
        if e.get("status") != "failure":
            continue
        lib, kind = _error_signal(e)
        if not lib or lib.lower() in SHELL_BUILTINS:
            continue
        p = norm_project(e.get("repo_scope") or "")
        sk = e.get("strategy_key")
        d = libs[lib]
        d["failures"] += 1
        if kind:
            d["kinds"][kind] += 1
        if p:
            d["projects"][p] += 1
        if sk:
            d["strategies"][sk] += 1
            strat_lib[sk][lib] += 1
    for n in nodes:
        lc = strat_lib.get(n["id"])
        n["error_library"] = lc.most_common(1)[0][0] if lc else ""
    ranked = sorted(libs.items(), key=lambda kv: kv[1]["failures"], reverse=True)
    libs_meta = [{
        "name": name, "failures": d["failures"],
        "top_kind": d["kinds"].most_common(1)[0][0] if d["kinds"] else "",
        "kinds": [{"kind": k, "count": v} for k, v in d["kinds"].most_common(4)],
        "projects": [{"name": k, "count": v} for k, v in d["projects"].most_common(4)],
        "strategies": [{"id": k, "count": v} for k, v in d["strategies"].most_common(5)],
    } for name, d in ranked]
    return libs_meta


def _parse_ts(s):
    try:
        return datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except (ValueError, TypeError):
        return None


def fix_edges(events, node_ids, window_min=60, lookahead=25):
    """Fase C: aristas fallo->correccion. Un fallo seguido (misma ventana/repo) de un exito
    del mismo strategy_key (reintento exitoso) o de otro que comparte ejecutable/herramienta."""
    seq = [e for e in events if e.get("strategy_key") and e.get("timestamp")]
    seq.sort(key=lambda e: e["timestamp"])
    edges, seen = [], set()
    recovered = set()
    for i, e in enumerate(seq):
        if e.get("status") != "failure":
            continue
        sk_f = e["strategy_key"]
        if sk_f not in node_ids:
            continue
        t_f = _parse_ts(e["timestamp"])
        repo_f = e.get("repo_scope")
        tool_f = (sk_f.split(":", 1)[0] if ":" in sk_f else sk_f)
        for j in range(i + 1, min(i + 1 + lookahead, len(seq))):
            s = seq[j]
            if s.get("status") != "success":
                continue
            if s.get("repo_scope") != repo_f:
                continue
            t_s = _parse_ts(s["timestamp"])
            if t_f and t_s and (t_s - t_f).total_seconds() > window_min * 60:
                break
            sk_s = s["strategy_key"]
            if sk_s not in node_ids:
                continue
            tool_s = (sk_s.split(":", 1)[0] if ":" in sk_s else sk_s)
            same = sk_s == sk_f
            if not same and tool_s != tool_f:
                continue
            recovered.add(sk_f)
            if same:
                break  # reintento del mismo: marca recuperado, sin auto-arista visual
            key = (sk_f, sk_s)
            if key in seen:
                break
            seen.add(key)
            edges.append({"source": sk_f, "target": sk_s, "kind": "fix", "weight": 0.9})
            break
    return edges, recovered


def analytics(nodes):
    # errores frecuentes: por cada error_class, cuantas estrategias y cuantos fallos acumulan
    err_strat = Counter()
    err_fail = Counter()
    for n in nodes:
        for ec in n["error_classes"]:
            err_strat[ec] += 1
            err_fail[ec] += n["failures"]
    errors = [
        {"error_class": ec, "strategies": err_strat[ec], "failures": err_fail[ec]}
        for ec, _ in err_strat.most_common(14)
    ]
    # candidatos de mejora: estrategias con fallos (ordena por fallos, luego menor success_rate)
    failing = sorted(
        [n for n in nodes if n["failures"] > 0],
        key=lambda n: (n["failures"], -(n["success_rate"] or 0)),
        reverse=True,
    )[:18]
    improve = [{
        "id": n["id"], "failures": n["failures"], "successes": n["successes"],
        "success_rate": n["success_rate"], "status": n["status"],
        "error_classes": n["error_classes"], "cluster": n.get("cluster", -1),
        "clusterLabel": n.get("clusterLabel", ""),
    } for n in failing]
    # obsoletas que antes servian (revalidar)
    stale_useful = sorted(
        [n for n in nodes if n["status"] == "stale" and n["successes"] > 0],
        key=lambda n: n["successes"], reverse=True,
    )[:14]
    revalidate = [{
        "id": n["id"], "successes": n["successes"], "last_success_at": n["last_success_at"],
        "cluster": n.get("cluster", -1), "clusterLabel": n.get("clusterLabel", ""),
    } for n in stale_useful]
    return {"errors": errors, "improve": improve, "revalidate": revalidate}


def seed_positions(nodes, centroids):
    ids = [n["id"] for n in nodes if n["id"] in centroids]
    if len(ids) < 3:
        return
    from sklearn.decomposition import PCA
    mat = np.stack([centroids[i] for i in ids])
    coords = PCA(n_components=3, random_state=0).fit_transform(mat)
    coords = coords / (np.abs(coords).max() + 1e-9) * 240.0
    pos = {i: coords[k] for k, i in enumerate(ids)}
    for n in nodes:
        p = pos.get(n["id"])
        if p is not None:
            n["x"], n["y"], n["z"] = float(p[0]), float(p[1]), float(p[2])


def sanitize_nodes(nodes):
    out = []
    for n in nodes:
        c = dict(n)
        repo = c.get("repo") or ""
        c["repo"] = os.path.basename(repo.rstrip("/")) if repo else ""
        out.append(c)
    return out


# --- Emision ----------------------------------------------------------------
def build_graph(sanitize=False):
    lessons = load_lessons()
    points = qdrant_scroll_all()
    centroids, agents = centroids_by_strategy(points)
    events = load_events()
    nodes = build_nodes(lessons, agents)
    task_families = annotate_task_families(nodes)
    sem, sem_ids = semantic_edges(nodes, centroids)
    struct = structural_edges(nodes)
    clusters = detect_themes(nodes, sem, sem_ids)
    projects_meta, coverage = aggregate_projects(events, nodes)
    node_ids = {n["id"] for n in nodes}
    libs_meta = libraries_analytics(events, nodes)
    fixes, recovered = fix_edges(events, node_ids)
    for n in nodes:
        n["recovered"] = n["id"] in recovered
    ana = analytics(nodes)
    seed_positions(nodes, centroids)
    if sanitize:
        nodes = sanitize_nodes(nodes)
    status_counts = Counter(n["status"] for n in nodes)
    return {
        "meta": {
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "collection": COLLECTION, "points_indexed": len(points),
            "nodes": len(nodes), "semantic_edges": len(sem), "structural_edges": len(struct),
            "status_counts": dict(status_counts), "sanitized": sanitize,
            "semantic_min_sim": SEMANTIC_MIN_SIM, "semantic_k": SEMANTIC_K,
            "themes": clusters, "task_families": task_families, "analytics": ana,
            "projects": projects_meta, "coverage": coverage,
            "libraries": libs_meta, "fix_edges": len(fixes),
        },
        "nodes": nodes, "links": sem + struct + fixes,
    }


def render_html(graph):
    template = TEMPLATE.read_text(encoding="utf-8")
    vendor = VENDOR_JS.read_text(encoding="utf-8")
    data_json = json.dumps(graph, ensure_ascii=False, separators=(",", ":"))
    return template.replace("/*__VENDOR_JS__*/", vendor).replace('"__GRAPH_DATA__"', data_json)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--sanitize", action="store_true", help="regenera JSON y HTML públicos desde fuentes locales")
    ap.add_argument("--json-only", action="store_true", help="con --sanitize, actualiza sólo el JSON público")
    ap.add_argument("--render-public", action="store_true", help="re-renderiza el HTML público desde el JSON ya saneado")
    ap.add_argument("--check-public", action="store_true", help="falla si HTML público no corresponde al JSON y la plantilla versionados")
    ap.add_argument("--public-json", type=Path, default=PUBLIC_GRAPH, help="JSON público de entrada/salida")
    ap.add_argument("--public-html", type=Path, default=PUBLIC_HTML, help="HTML público de entrada/salida")
    args = ap.parse_args()

    selected = sum((args.sanitize, args.render_public, args.check_public))
    if selected != 1:
        ap.error("elija exactamente una operación: --sanitize, --render-public o --check-public")

    if args.render_public or args.check_public:
        if not args.public_json.exists():
            ap.error(f"JSON público ausente: {args.public_json}")
        public_graph = json.loads(args.public_json.read_text(encoding="utf-8"))
        rendered = render_html(public_graph)
        meta = public_graph.get("meta", {})
        if args.check_public:
            if not args.public_html.exists():
                ap.error(f"HTML público ausente: {args.public_html}")
            current = args.public_html.read_text(encoding="utf-8")
            if current != rendered:
                print("[fail] el HTML público no corresponde al JSON, plantilla o vendor versionados", file=sys.stderr)
                return 1
            print(f"[ok] public HTML reproducible -> nodos={meta.get('nodes', 0)}")
            return 0
        args.public_html.parent.mkdir(parents=True, exist_ok=True)
        args.public_html.write_text(rendered, encoding="utf-8")
        print(f"[ok] public HTML re-rendered -> nodos={meta.get('nodes', 0)}")
        return 0

    pub = build_graph(sanitize=True)
    args.public_json.parent.mkdir(parents=True, exist_ok=True)
    args.public_json.write_text(json.dumps(pub, ensure_ascii=False, indent=2), encoding="utf-8")
    if not args.json_only:
        args.public_html.parent.mkdir(parents=True, exist_ok=True)
        args.public_html.write_text(render_html(pub), encoding="utf-8")
    print(f"[ok] public -> nodos={pub['meta']['nodes']} temas={len(pub['meta']['themes'])} (repos sin rutas)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
