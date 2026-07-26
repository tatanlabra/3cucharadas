#!/usr/bin/env python3
"""Capitales comunales (ciudad/pueblo cabecera) para las 346 comunas del visor Catastro SII.

Produce ``catastro_sii_brecha/data/capitales_comunales.parquet`` con el centro
y zoom sugerido para encuadrar la capital comunal (no el centroide del
polígono comunal) al seleccionar una comuna en el visor. La lista de 346
comunas y sus llaves de unión (``codigo_comuna``, ``comuna``, ``region``) se
toman tal cual de ``catastro_sii_brecha/data/metricas_comunales.parquet``: no
se derivan códigos ni nombres propios.

Fuentes de coordenadas, en orden de preferencia:
  1. Wikidata (SPARQL, https://query.wikidata.org/sparql): comunas de Chile
     (instancia de Q1840161) con su propiedad ``capital`` (P36) y las
     coordenadas (P625) de esa localidad. Es la fuente estructurada primaria;
     el resultado crudo se cachea en ``.cache/wikidata_comunas_raw.json`` para
     no repetir la consulta en corridas siguientes.
  2. Nominatim/OSM (https://nominatim.openstreetmap.org/search) para las
     comunas sin capital+coordenada en Wikidata. Se respeta 1 req/seg y un
     User-Agent identificable; cada respuesta se cachea en
     ``.cache/nominatim_capitales.json`` por texto de consulta exacto.

Si ninguna de las dos fuentes resuelve una comuna, la fila queda con
``lon``/``lat`` nulos y ``fuente = "sin_resolver"`` — no se inventan ni
estiman coordenadas de memoria.

Ejecutar sin argumentos; es determinista dado el mismo estado de las fuentes
(y de la caché local, si existe):

    python3 scripts/catastro_sii/build_capitales_comunales.py
"""
from __future__ import annotations

import json
import re
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "catastro_sii_brecha" / "data"
CACHE_DIR = DATA / ".cache"
COMMUNES_PARQUET = DATA / "metricas_comunales.parquet"
OUTPUT = DATA / "capitales_comunales.parquet"

WIKIDATA_CACHE = CACHE_DIR / "wikidata_comunas_raw.json"
NOMINATIM_CACHE = CACHE_DIR / "nominatim_capitales.json"

WIKIDATA_ENDPOINT = "https://query.wikidata.org/sparql"
NOMINATIM_ENDPOINT = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "3cucharadas-catastro-sii-capitales/1.0 (contacto: tatanlabra@gmail.com)"

DEFAULT_ZOOM = 13.0
NOMINATIM_RATE_LIMIT_S = 1.1
HTTP_TIMEOUT_S = 30

# Q1840161 = "comuna de Chile" en Wikidata.
WIKIDATA_QUERY = """
SELECT ?comuna ?comunaLabel ?regionLabel ?capital ?capitalLabel ?coord WHERE {
  ?comuna wdt:P31 wd:Q1840161 .
  OPTIONAL { ?comuna wdt:P131 ?region . }
  OPTIONAL {
    ?comuna wdt:P36 ?capital .
    OPTIONAL { ?capital wdt:P625 ?coord . }
  }
  SERVICE wikibase:label { bd:serviceParam wikibase:language "es". }
}
"""

# Chile continental + insular. Isla de Pascua (Rapa Nui) es un caso real fuera
# de la caja continental y se valida aparte, no se descarta como error.
CHILE_MAINLAND_BBOX = {"lon": (-76.0, -66.0), "lat": (-56.0, -17.0)}
RAPA_NUI_BBOX = {"lon": (-110.0, -108.5), "lat": (-27.5, -26.5)}


def normalize_name(value: str) -> str:
    """Clave de comparación: minúsculas, sin tildes/apóstrofes, espacios colapsados."""
    decomposed = unicodedata.normalize("NFKD", value)
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    stripped = re.sub(r"[^a-zA-Z0-9]+", " ", stripped)
    return re.sub(r"\s+", " ", stripped).strip().lower()


def http_get_json(url: str, params: dict, headers: dict) -> dict:
    query = urllib.parse.urlencode(params)
    request = urllib.request.Request(f"{url}?{query}", headers=headers)
    with urllib.request.urlopen(request, timeout=HTTP_TIMEOUT_S) as response:
        return json.loads(response.read().decode("utf-8"))


def fetch_wikidata_raw() -> dict:
    if WIKIDATA_CACHE.exists():
        return json.loads(WIKIDATA_CACHE.read_text())
    headers = {"Accept": "application/sparql-results+json", "User-Agent": USER_AGENT}
    data = http_get_json(WIKIDATA_ENDPOINT, {"query": WIKIDATA_QUERY}, headers)
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    WIKIDATA_CACHE.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    return data


def parse_point_wkt(wkt: str) -> tuple[float, float] | None:
    match = re.match(r"Point\(([-0-9.]+)\s+([-0-9.]+)\)", wkt)
    if not match:
        return None
    lon, lat = float(match.group(1)), float(match.group(2))
    return lon, lat


def build_wikidata_index(raw: dict) -> dict[str, dict]:
    """QID -> mejor registro (label, región(es), capital, lon, lat) visto en las filas."""
    index: dict[str, dict] = {}
    for row in raw["results"]["bindings"]:
        qid = row["comuna"]["value"]
        entry = index.setdefault(
            qid,
            {
                "comuna_label": row.get("comunaLabel", {}).get("value"),
                "region_labels": set(),
                "capital_label": None,
                "lon": None,
                "lat": None,
            },
        )
        if "regionLabel" in row:
            entry["region_labels"].add(row["regionLabel"]["value"])
        if "coord" in row and entry["lon"] is None:
            point = parse_point_wkt(row["coord"]["value"])
            if point is not None:
                entry["lon"], entry["lat"] = point
                entry["capital_label"] = row.get("capitalLabel", {}).get("value")
        elif entry["capital_label"] is None and "capitalLabel" in row:
            entry["capital_label"] = row["capitalLabel"]["value"]
    return index


def build_name_lookup(index: dict[str, dict]) -> dict[str, list[dict]]:
    lookup: dict[str, list[dict]] = {}
    for entry in index.values():
        if not entry["comuna_label"]:
            continue
        key = normalize_name(entry["comuna_label"])
        lookup.setdefault(key, []).append(entry)
    return lookup


def load_nominatim_cache() -> dict:
    if NOMINATIM_CACHE.exists():
        return json.loads(NOMINATIM_CACHE.read_text())
    return {}


def save_nominatim_cache(cache: dict) -> None:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    NOMINATIM_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=2))


def query_nominatim(query_text: str, cache: dict) -> list[dict] | None:
    if query_text in cache:
        return cache[query_text]
    headers = {"User-Agent": USER_AGENT}
    try:
        results = http_get_json(
            NOMINATIM_ENDPOINT,
            {
                "q": query_text,
                "format": "json",
                "limit": 5,
                "countrycodes": "cl",
                "addressdetails": 0,
            },
            headers,
        )
    except (urllib.error.URLError, TimeoutError, ValueError) as exc:
        print(f"  [nominatim] error para {query_text!r}: {exc}")
        results = None
    cache[query_text] = results
    time.sleep(NOMINATIM_RATE_LIMIT_S)
    return results


def nominatim_result_tier(result: dict) -> int:
    """Prioridad de tipo de resultado: valores más bajos son mejores.

    0: localidad tipo ciudad/pueblo/municipio (el propio asentamiento).
    1: límite administrativo (para comunas urbanas de conurbación sin un
       "pueblo cabecera" distinto de la propia comuna, p.ej. El Bosque en
       el Gran Santiago, el límite administrativo es el mejor proxy).
    2: aldea (village).
    3: caserío (hamlet) u otro lugar poblado menor.
    4: cualquier otra cosa (calles, estaciones, etc.), última opción.
    """
    cls, typ = result.get("class"), result.get("type")
    if cls == "place" and typ in {"city", "town", "municipality"}:
        return 0
    if cls == "boundary" and typ == "administrative":
        return 1
    if cls == "place" and typ == "village":
        return 2
    if cls == "place" and typ == "hamlet":
        return 3
    if cls == "place" and typ == "suburb":
        return 2
    return 4


NOISE_TIER = 4


def pick_best_nominatim_result(results: list[dict] | None) -> dict | None:
    if not results:
        return None
    candidates = sorted(
        results,
        key=lambda r: (nominatim_result_tier(r), -float(r.get("importance") or 0)),
    )
    return candidates[0] if candidates else None


def within_chile(lon: float, lat: float) -> bool:
    mainland = (
        CHILE_MAINLAND_BBOX["lon"][0] <= lon <= CHILE_MAINLAND_BBOX["lon"][1]
        and CHILE_MAINLAND_BBOX["lat"][0] <= lat <= CHILE_MAINLAND_BBOX["lat"][1]
    )
    rapa_nui = (
        RAPA_NUI_BBOX["lon"][0] <= lon <= RAPA_NUI_BBOX["lon"][1]
        and RAPA_NUI_BBOX["lat"][0] <= lat <= RAPA_NUI_BBOX["lat"][1]
    )
    return mainland or rapa_nui


def main() -> None:
    communes = pd.read_parquet(COMMUNES_PARQUET)[["codigo_comuna", "comuna", "region"]].copy()
    assert communes["codigo_comuna"].is_unique, "codigo_comuna no es único en metricas_comunales.parquet"

    wikidata_raw = fetch_wikidata_raw()
    wikidata_index = build_wikidata_index(wikidata_raw)
    name_lookup = build_name_lookup(wikidata_index)

    nominatim_cache = load_nominatim_cache()

    rows = []
    unresolved: list[str] = []
    capital_diff: list[tuple[str, str, str]] = []
    out_of_bbox: list[tuple[str, str, float, float]] = []

    for record in communes.itertuples(index=False):
        codigo, comuna, region = record.codigo_comuna, record.comuna, record.region
        key = normalize_name(comuna)
        candidates = name_lookup.get(key, [])

        capital_comunal = None
        lon = lat = None
        fuente = None

        if candidates:
            with_coord = [c for c in candidates if c["lon"] is not None]
            chosen = with_coord[0] if with_coord else candidates[0]
            if chosen["lon"] is not None:
                capital_comunal = chosen["capital_label"] or comuna
                lon, lat = chosen["lon"], chosen["lat"]
                fuente = "wikidata"

        if lon is None:
            # Sin capital+coordenada en Wikidata: probamos Nominatim asumiendo
            # que, como en la enorme mayoría de las comunas chilenas, la
            # capital comparte nombre con la comuna. Si la consulta con región
            # sólo devuelve ruido (p.ej. una estación de bomberos homónima),
            # reintentamos con una consulta más simple sin el nombre de región,
            # que a veces confunde el parser de Nominatim.
            best = None
            for query_text in (f"{comuna}, {region}, Chile", f"{comuna}, Chile"):
                results = query_nominatim(query_text, nominatim_cache)
                candidate = pick_best_nominatim_result(results)
                if candidate is not None and nominatim_result_tier(candidate) < NOISE_TIER:
                    best = candidate
                    break
                best = best or candidate
            if best is not None:
                capital_comunal = comuna
                lon, lat = float(best["lon"]), float(best["lat"])
                fuente = "osm_nominatim"

        if lon is None:
            unresolved.append(f"{codigo} {comuna} ({region})")
            fuente = "sin_resolver"

        if capital_comunal and normalize_name(capital_comunal) != normalize_name(comuna):
            capital_diff.append((codigo, comuna, capital_comunal))

        if lon is not None and not within_chile(lon, lat):
            out_of_bbox.append((codigo, comuna, lon, lat))

        rows.append(
            {
                "codigo_comuna": codigo,
                "comuna": comuna,
                "region": region,
                "capital_comunal": capital_comunal,
                "lon": lon,
                "lat": lat,
                "zoom_sugerido": DEFAULT_ZOOM,
                "fuente": fuente,
            }
        )

    save_nominatim_cache(nominatim_cache)

    out = pd.DataFrame(rows)
    out.to_parquet(OUTPUT, index=False)

    total = len(out)
    resolved = out["lon"].notna().sum()
    by_source = out["fuente"].value_counts().to_dict()

    print(f"Filas totales: {total} (esperado 346)")
    print(f"Con coordenada resuelta: {resolved}/{total}")
    print(f"Por fuente: {by_source}")
    if unresolved:
        print(f"\nSin resolver ({len(unresolved)}):")
        for line in unresolved:
            print(f"  - {line}")
    if out_of_bbox:
        print(f"\nFuera de la caja de cordura Chile/Rapa Nui ({len(out_of_bbox)}):")
        for codigo, comuna, lon, lat in out_of_bbox:
            print(f"  - {codigo} {comuna}: lon={lon} lat={lat}")
    if capital_diff:
        print(f"\nCapital comunal distinta del nombre de la comuna ({len(capital_diff)}):")
        for codigo, comuna, capital in sorted(capital_diff, key=lambda t: t[1]):
            print(f"  - {codigo} {comuna} -> {capital}")

    print(f"\nEscrito: {OUTPUT}")


if __name__ == "__main__":
    main()
