#!/usr/bin/env python3
"""Verifica una publicación propia en redes y la registra en _data/distribucion.yml.

Dos usos:
  registrar_publicacion.py <ref> <enlace> [--lang es|en] [--fecha AAAA-MM-DD] [--dry-run]
  registrar_publicacion.py <ref> --descubrir [--dry-run]

Con un enlace (LinkedIn, X, Reddit, Spotify, Mastodon o Bluesky): lo resuelve (lnkd.in, t.co),
le quita los parámetros de rastreo, comprueba que la publicación exista y sea del autor, y la
agrega a las publicaciones del `ref`. Con --descubrir busca sola, en las API públicas de
Mastodon y Bluesky, los posts del autor que enlazan el artículo y registra los que falten.

Qué se puede comprobar sin sesión (medido el 2026-11-01):
  - Mastodon y Bluesky: API pública; se descubren solos.
  - LinkedIn: la página pública del post responde 200 sin sesión; el autor se lee del slug.
    El perfil, en cambio, responde 999 (antibots): no se pueden descubrir posts.
  - X: oEmbed público (publish.x.com) devuelve el autor; el timeline exige API de pago.
  - Spotify: la página del episodio responde 200 con User-Agent de navegador.
  - Reddit: bloquea la lectura automática; el enlace se registra como declarado por el autor.
Los perfiles del autor salen de `social.links` en _config.yml. No se usa un navegador con la
sesión de la persona: en LinkedIn, X y Reddit eso infringe sus términos y arriesga la cuenta.

Vinculación (2026-11-01): en Mastodon, Bluesky, X y LinkedIn, además del autor, se comprueba que
el post enlace el artículo del `ref` o su episodio (bloque `audio:` del post). Los acortadores se
resuelven: t.co responde 301 si no se envía un User-Agent de navegador, y lnkd.in muestra una
página intermedia con el destino en `external_url_click`. Sin ese vínculo, el registro se rechaza
salvo con --sin-vinculo. Descubrir posts en X o LinkedIn sin sesión no es posible: xcancel (Nitter)
responde 451, el puente de X de RSS-Bridge responde 500, los buscadores no indexan los posts del día
y AUR no tiene herramientas que funcionen sin cuenta.
"""
from __future__ import annotations

import argparse
import datetime as dt
import html
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "_data" / "distribucion.yml"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
TRACKING = re.compile(r"^(utm_\w+|rcm|si|trk|trackingId|s|t|ref_src|ref_url|share_id|context)$")


class Rechazo(Exception):
    pass


def fetch(url: str, *, ua: bool = True, timeout: int = 20) -> tuple[int, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA} if ua else {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status, resp.geturl(), resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as exc:
        return exc.code, url, ""


def limpiar(url: str) -> str:
    parts = urllib.parse.urlsplit(url)
    query = [(k, v) for k, v in urllib.parse.parse_qsl(parts.query) if not TRACKING.match(k)]
    return urllib.parse.urlunsplit((parts.scheme, parts.netloc, parts.path, urllib.parse.urlencode(query), ""))


def perfiles() -> dict[str, str]:
    config = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8"))
    links = (config.get("social") or {}).get("links") or []
    out = {}
    for link in links:
        if m := re.match(r"https://www\.linkedin\.com/in/([^/]+)/?", link):
            out["linkedin"] = m.group(1).lower()
        elif m := re.match(r"https://x\.com/([^/]+)/?", link):
            out["x"] = m.group(1).lower()
        elif m := re.match(r"https://(mastodon\.[^/]+)/@([^/]+)/?", link):
            out["mastodon"] = f"{m.group(2).lower()}@{m.group(1)}"
        elif m := re.match(r"https://bsky\.app/profile/([^/]+)/?", link):
            out["bluesky"] = m.group(1).lower()
    return out


def verificar(url: str, yo: dict[str, str]) -> tuple[str, str, str]:
    """Devuelve (plataforma, url_normalizada, cómo se verificó) o lanza Rechazo."""
    host = urllib.parse.urlsplit(url).netloc.lower()
    if host in {"lnkd.in", "t.co"}:
        status, url, _ = fetch(url)
        if status != 200:
            raise Rechazo(f"el enlace corto respondió {status}")
        host = urllib.parse.urlsplit(url).netloc.lower()
    url = limpiar(url)
    path = urllib.parse.urlsplit(url).path

    if host.endswith("linkedin.com"):
        m = re.match(r"/posts/([^/_]+)_", path)
        if not m:
            raise Rechazo(f"no es la URL de un post de LinkedIn: {path}")
        if m.group(1).lower() != yo.get("linkedin"):
            raise Rechazo(f"el post es de `{m.group(1)}`, no de `{yo.get('linkedin')}`")
        status, _, page = fetch(url)
        if status != 200 or "authwall" in page.lower():
            raise Rechazo(f"la página pública del post respondió {status}")
        return "linkedin", url, "página pública 200 y autor en el slug"

    if host in {"x.com", "www.x.com", "twitter.com", "www.twitter.com", "mobile.twitter.com"}:
        m = re.match(r"/([^/]+)/status/(\d+)", path)
        if not m:
            raise Rechazo(f"no es la URL de un post de X: {path}")
        canon = f"https://x.com/{m.group(1)}/status/{m.group(2)}"
        status, _, body = fetch("https://publish.x.com/oembed?omit_script=true&url=" + urllib.parse.quote(canon, safe=""))
        if status != 200:
            raise Rechazo(f"oEmbed de X respondió {status}: el post no existe o no es público")
        autor = json.loads(body).get("author_url", "").rstrip("/").rsplit("/", 1)[-1].lower()
        if autor != yo.get("x"):
            raise Rechazo(f"el post es de @{autor}, no de @{yo.get('x')}")
        return "x", canon, "oEmbed público 200 con el autor"

    if host.endswith("reddit.com") or host == "redd.it":
        m = re.match(r"/r/([^/]+)/comments/([a-z0-9]+)", path)
        if not m:
            raise Rechazo(f"no es la URL de un hilo de Reddit: {path}")
        canon = f"https://www.reddit.com/r/{m.group(1)}/comments/{m.group(2)}/"
        return "reddit", canon, f"r/{m.group(1)}; declarado por el autor (Reddit bloquea la verificación automática)"

    if host == "open.spotify.com":
        if not re.fullmatch(r"/episode/[A-Za-z0-9]{22}", path):
            raise Rechazo(f"no es la URL de un episodio de Spotify: {path}")
        status, _, _ = fetch(url)
        if status != 200:
            raise Rechazo(f"Spotify respondió {status}")
        return "spotify", url, "episodio 200 con User-Agent de navegador"

    if host.startswith("mastodon."):
        m = re.match(r"/@([^/]+)/(\d+)", path)
        if not m:
            raise Rechazo(f"no es la URL de un post de Mastodon: {path}")
        status, _, body = fetch(f"https://{host}/api/v1/statuses/{m.group(2)}", ua=False)
        if status != 200:
            raise Rechazo(f"la API de Mastodon respondió {status}")
        acct = json.loads(body)["account"]["acct"].lower()
        if f"{acct}@{host}" != yo.get("mastodon") and acct != yo.get("mastodon"):
            raise Rechazo(f"el post es de {acct}, no de {yo.get('mastodon')}")
        return "mastodon", url, "API pública 200 con el autor"

    if host == "bsky.app":
        m = re.match(r"/profile/([^/]+)/post/([a-z0-9]+)", path)
        if not m:
            raise Rechazo(f"no es la URL de un post de Bluesky: {path}")
        if m.group(1).lower() != yo.get("bluesky"):
            raise Rechazo(f"el post es de {m.group(1)}, no de {yo.get('bluesky')}")
        uri = urllib.parse.quote(f"at://{m.group(1)}/app.bsky.feed.post/{m.group(2)}", safe="")
        status, _, _ = fetch(f"https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?depth=0&uri={uri}", ua=False)
        if status != 200:
            raise Rechazo(f"la API de Bluesky respondió {status}")
        return "bluesky", url, "API pública 200 con el autor"

    raise Rechazo(f"plataforma no reconocida: {host}")


def objetivos(ref: str) -> tuple[str, set[str]]:
    """Marca del artículo (`/<ref>/`) y URLs de episodio declaradas en el bloque audio: del post."""
    episodios = set()
    for post in (ROOT / "_posts").glob("*.md"):
        texto = post.read_text(encoding="utf-8")
        if not re.search(rf"^ref:\s*{re.escape(ref)}\s*$", texto, re.M):
            continue
        front = yaml.safe_load(texto.split("\n---\n", 1)[0].lstrip("-\n")) or {}
        for plataforma in ((front.get("audio") or {}).get("plataformas") or []):
            if "/episode/" in str(plataforma.get("url", "")):
                episodios.add(str(plataforma["url"]).split("?")[0])
    return f"/{ref}/", episodios


def resolver(url: str) -> str:
    host = urllib.parse.urlsplit(url).netloc.lower()
    if host == "t.co":
        return fetch(url, ua=False)[1]  # sin User-Agent de navegador, t.co responde 301
    if host == "lnkd.in":
        _, _, page = fetch(url)
        m = re.search(r'data-tracking-control-name="external_url_click"[^>]*href="([^"]+)"', page)
        return html.unescape(m.group(1)) if m else url
    return url


def enlaces(plataforma: str, url: str) -> list[str]:
    """URLs a las que apunta el post, con los acortadores ya resueltos."""
    path = urllib.parse.urlsplit(url).path
    crudos: list[str] = []
    if plataforma == "mastodon":
        host = urllib.parse.urlsplit(url).netloc
        _, _, body = fetch(f"https://{host}/api/v1/statuses/{path.rstrip('/').rsplit('/', 1)[-1]}", ua=False)
        st = json.loads(body)
        crudos = re.findall(r'href="([^"]+)"', st.get("content", "")) + [((st.get("card") or {}).get("url") or "")]
    elif plataforma == "bluesky":
        actor, rkey = re.match(r"/profile/([^/]+)/post/([a-z0-9]+)", path).groups()
        uri = urllib.parse.quote(f"at://{actor}/app.bsky.feed.post/{rkey}", safe="")
        _, _, body = fetch(f"https://public.api.bsky.app/xrpc/app.bsky.feed.getPostThread?depth=0&uri={uri}", ua=False)
        post = json.loads(body)["thread"]["post"]
        for facet in post["record"].get("facets") or []:
            crudos += [f.get("uri", "") for f in facet.get("features", [])]
        crudos.append(((post.get("embed") or {}).get("external") or {}).get("uri", ""))
    elif plataforma == "x":
        _, _, body = fetch("https://publish.x.com/oembed?omit_script=true&url=" + urllib.parse.quote(url, safe=""))
        crudos = re.findall(r"https://t\.co/[A-Za-z0-9]+", json.loads(body).get("html", ""))
    elif plataforma == "linkedin":
        _, _, page = fetch(url)
        for bloque in re.findall(r'<script type="application/ld\+json">(.*?)</script>', page, re.S):
            try:
                datos = json.loads(bloque)
            except json.JSONDecodeError:
                continue
            if isinstance(datos, dict):
                crudos += re.findall(r"https?://\S+", str(datos.get("articleBody") or ""))
    return [resolver(u) for u in dict.fromkeys(c for c in crudos if c)]


def vinculo(ref: str, urls: list[str]) -> list[str]:
    marca, episodios = objetivos(ref)
    out = []
    if any(marca in u and "3cucharadas.cl" in u for u in urls):
        out.append("artículo")
    if any(u.split("?")[0] in episodios for u in urls):
        out.append("episodio")
    return out


def bloque_ref(texto: str, ref: str) -> tuple[int, int]:
    inicio = texto.find(f"\n- slug: {ref}\n")
    if inicio < 0:
        raise Rechazo(f"{ref} no tiene entrada en _data/distribucion.yml")
    fin = texto.find("\n- slug: ", inicio + 1)
    return inicio + 1, (fin + 1 if fin >= 0 else len(texto))


def nota_yaml(texto: str) -> str:
    """Escalar entre comillas dobles, cortado bajo 80 columnas.

    Sin comillas, un «: » dentro de la nota rompe el YAML (pasó con «r/PublicPolicy; …»).
    Un string JSON es un escalar YAML válido entre comillas dobles, y sus saltos de línea
    se pliegan a un espacio al leerlo.
    """
    lineas, actual = [], "    nota:"
    for palabra in json.dumps(" ".join(texto.split()), ensure_ascii=False).split(" "):
        if len(actual) + 1 + len(palabra) > 78 and actual.strip() != "nota:":
            lineas.append(actual)
            actual = "     "
        actual += " " + palabra
    return "\n".join(lineas + [actual]) + "\n"


def registrar(ref: str, plataforma: str, url: str, como: str, lang: str, fecha: str, dry: bool) -> str:
    texto = DATA.read_text(encoding="utf-8")
    if url in texto:
        return f"YA_REGISTRADO {plataforma} {url}"
    ini, fin = bloque_ref(texto, ref)
    bloque = texto[ini:fin]
    campo = "url_publicada_en" if lang == "en" else "url_publicada"
    entrada = re.search(rf"^  - plataforma: {plataforma}\n(?:    .*\n|      .*\n)*", bloque, re.M)
    if lang == "en" and entrada and "url_publicada_en:" not in entrada.group(0) and plataforma != "reddit":
        # Mismo canal, versión en inglés: va en la misma entrada, como en Mastodon y Bluesky.
        linea = re.search(r"^    url_publicada: .*\n", entrada.group(0), re.M)
        if not linea:
            raise Rechazo(f"la entrada {plataforma} de {ref} no tiene url_publicada")
        pos = ini + entrada.start() + linea.end()
        nuevo = texto[:pos] + f"    url_publicada_en: {url}\n" + texto[pos:]
    else:
        item = (f"  - plataforma: {plataforma}\n    fecha: '{fecha}'\n    {campo}: {url}\n"
                f"    estado: publicado\n" + nota_yaml(f"Verificado con registrar_publicacion.py: {como}."))
        cuerpo = bloque if bloque.endswith("\n") else bloque + "\n"
        nuevo = texto[:ini] + cuerpo + item + texto[fin:]
    try:
        datos = yaml.safe_load(nuevo)
    except yaml.YAMLError as exc:
        raise Rechazo(f"el YAML resultante no es válido; no se escribe ({exc.problem})") from None
    pubs = next(e for e in datos if e.get("slug") == ref)["publicaciones"]
    if not any(p.get(campo) == url for p in pubs):
        raise Rechazo("el YAML resultante no contiene la publicación: no se escribe")
    if not dry:
        DATA.write_text(nuevo, encoding="utf-8")
    return f"{'SIMULADO' if dry else 'REGISTRADO'} {plataforma}/{lang} {url}"


def descubrir(ref: str, yo: dict[str, str]) -> list[tuple[str, str, str]]:
    """(plataforma, url, lang) de los posts del autor que enlazan el artículo."""
    hallados = []
    acct, inst = yo["mastodon"].split("@")
    _, _, body = fetch(f"https://{inst}/api/v1/accounts/lookup?acct={acct}", ua=False)
    cuenta = json.loads(body)["id"]
    _, _, body = fetch(f"https://{inst}/api/v1/accounts/{cuenta}/statuses?limit=40", ua=False)
    for st in json.loads(body):
        blob = json.dumps(st, ensure_ascii=False)
        if f"/{ref}/" in blob:
            hallados.append(("mastodon", st["url"], "en" if f"/en/" in blob.split(ref)[0][-120:] else "es"))
    actor = yo["bluesky"]
    _, _, body = fetch(f"https://public.api.bsky.app/xrpc/app.bsky.feed.getAuthorFeed?limit=50&actor={actor}", ua=False)
    for item in json.loads(body).get("feed", []):
        post = item["post"]
        blob = json.dumps(post["record"], ensure_ascii=False)
        if f"/{ref}/" in blob:
            rkey = post["uri"].rsplit("/", 1)[-1]
            hallados.append(("bluesky", f"https://bsky.app/profile/{actor}/post/{rkey}",
                             "en" if f"/en/" in blob.split(ref)[0][-120:] else "es"))
    return hallados


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("ref")
    ap.add_argument("enlace", nargs="?")
    ap.add_argument("--lang", choices=["es", "en"], default="es")
    ap.add_argument("--fecha", default=dt.date.today().isoformat())
    ap.add_argument("--descubrir", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--sin-vinculo", action="store_true", help="registrar aunque el post no enlace el artículo ni el episodio")
    args = ap.parse_args(argv)
    if bool(args.enlace) == args.descubrir:
        ap.error("pasar un enlace o --descubrir, no ambos")
    yo = perfiles()
    try:
        if args.descubrir:
            hallados = descubrir(args.ref, yo)
            if not hallados:
                print(f"SIN_HALLAZGOS {args.ref} en Mastodon y Bluesky")
            for plataforma, url, lang in hallados:
                print(registrar(args.ref, plataforma, url, "descubierto en la API pública", lang, args.fecha, args.dry_run))
            return 0
        plataforma, url, como = verificar(args.enlace, yo)
        if plataforma in {"mastodon", "bluesky", "x", "linkedin"}:
            urls = enlaces(plataforma, url)
            vinc = vinculo(args.ref, urls)
            if not vinc and not args.sin_vinculo:
                raise Rechazo(f"el post no enlaza el artículo ni el episodio de {args.ref} (enlaces: {urls or 'ninguno'})")
            como += f"; enlaza {', '.join(vinc) or 'nada del ref (--sin-vinculo)'}"
        print(registrar(args.ref, plataforma, url, como, args.lang, args.fecha, args.dry_run))
        return 0
    except Rechazo as exc:
        print(f"RECHAZADO: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
