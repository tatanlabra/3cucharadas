#!/usr/bin/env python3
"""Verify identity, review freshness or local PDF custody for the III–IV revision."""
import argparse
import hashlib
import json
import sys
from pathlib import Path
from urllib.parse import unquote, urljoin, urlparse
import yaml

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "docs/plans/20261107-thesis-editorial-iii-iv/evidence"
ES_SOURCES = {
    "_posts/2026-10-23-costos-cierre-escolar-trayectorias.md",
    "_posts/2026-11-04-cierre-escolar-educacion-superior-causal-ml.md",
    "_pages/tesis-post3-anexo-metodologico.md",
    "_pages/tesis-post4-anexo-metodologico.md",
}
PDF_SOURCES = {name for name in ES_SOURCES if "post4" in name or "causal-ml" in name}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def metadata(path):
    return yaml.safe_load(path.read_text().split("---", 2)[1])


def require(ok, message):
    if not ok:
        raise AssertionError(message)


def verify_links(artifact_root, broken_anchor=False):
    from bs4 import BeautifulSoup

    require(artifact_root.is_dir(), "Rendered artifact missing")
    cache = {}
    checked = 0
    mutated = False
    for name in sorted(ES_SOURCES):
        for lang in ("es", "en"):
            source = ROOT / (name if lang == "es" else name.replace(".md", "-en.md"))
            route = ("/en" if lang == "en" else "") + metadata(source)["permalink"]
            page = artifact_root / route.lstrip("/") / "index.html"
            soup = BeautifulSoup(page.read_text(), "html.parser")
            article = soup.select_one(".page__content")
            require(article is not None, f"Article content missing: {route}")
            for anchor in article.select("a[href]"):
                href = anchor["href"]
                target = urlparse(urljoin("https://3cucharadas.cl" + route, href))
                if target.scheme not in ("http", "https") or target.hostname not in ("3cucharadas.cl", "www.3cucharadas.cl"):
                    continue
                path = artifact_root / unquote(target.path).lstrip("/")
                require(path.resolve().is_relative_to(artifact_root), f"Link escapes artifact: {href}")
                if path.is_dir():
                    path = path / "index.html"
                require(path.is_file(), f"Broken local link: {route} -> {href}")
                fragment = unquote(target.fragment)
                if path.suffix == ".html":
                    if broken_anchor and not mutated:
                        fragment = "editorial-nonexistent-anchor-probe"
                        mutated = True
                    if fragment:
                        if path not in cache:
                            doc = BeautifulSoup(path.read_text(), "html.parser")
                            cache[path] = {tag["id"] for tag in doc.select("[id]")}
                        require(fragment in cache[path], f"Broken anchor: {route} -> {target.path}#{fragment}")
                checked += 1
    require(checked > 0, "No local links inspected")
    print(f"EDITORIAL_LINKS_VALID pages=8 local_links={checked}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", required=True, choices=("baseline", "review", "pdf", "links"))
    parser.add_argument("--fixture", choices=("identity-drift", "review-stale", "pdf-stale", "pdf-image-stale", "broken-anchor"))
    parser.add_argument("--artifact-root", type=Path)
    args = parser.parse_args()
    expected_fixture = {"baseline": "identity-drift", "review": "review-stale", "pdf": "pdf-stale", "links": "broken-anchor"}[args.check]
    if args.fixture and args.fixture != expected_fixture and not (args.check == "pdf" and args.fixture == "pdf-image-stale"):
        parser.error("Fixture does not exercise the requested check")
    if args.check == "links":
        if not args.artifact_root:
            parser.error("--artifact-root is required for links")
        verify_links(args.artifact_root.resolve(), bool(args.fixture))
    elif args.check == "baseline":
        baseline = json.loads((EVIDENCE / "baseline.json").read_text())
        require(len(baseline["posts"]) == 4, "Baseline must contain four original posts")
        for index, (name, original) in enumerate(baseline["posts"].items()):
            actual = metadata(ROOT / name)
            if args.fixture and index == 0:
                actual["ref"] = "unapproved-identity"
            for field, expected in original["identity"].items():
                require(str(actual.get(field)) == expected, f"Identity changed: {name}:{field}")
        for name, expected in baseline["data_sha256"].items():
            require(digest(ROOT / name) == expected, f"Measured data changed: {name}")
    elif args.check == "review":
        decision = json.loads((EVIDENCE / "claude/decision.json").read_text())
        require(decision["verdict"] == "APPROVE", "Review has unresolved changes")
        require(ES_SOURCES <= decision["inputs"].keys(), "Review must cover both ES posts and annexes")
        for index, (name, expected) in enumerate(decision["inputs"].items()):
            observed = digest(ROOT / name)
            if args.fixture and index == 0:
                observed = "0" * 64
            require(observed == expected, f"Stale review: {name}")
        result = ROOT / decision["original_response"]
        require(digest(result) == decision["original_sha256"], "Original review response changed")
        require("REVIEW_VERDICT: APPROVE" in result.read_text(), "Original reviewer did not approve")
    else:
        receipt = json.loads((EVIDENCE / "pdf-delivery.json").read_text())
        require(receipt["figures"] == 3 and receipt["tables"] == 6, "PDF evidence inventory is incomplete")
        require(receipt["pages"] > 0, "Empty PDF")
        require(PDF_SOURCES <= receipt["inputs"].keys(), "PDF must bind both article and annex")
        require(len(receipt["images"]) == 3, "PDF must bind three embedded images")
        for name, expected in receipt["images"].items():
            if args.fixture == "pdf-image-stale":
                expected = "0" * 64
            require(name.startswith("assets/images/tesis-post4/"), "Unexpected PDF image source")
            require(digest(ROOT / name) == expected, f"Stale PDF figure: {name}")
        for index, (name, expected) in enumerate(receipt["inputs"].items()):
            observed = digest(ROOT / name)
            if args.fixture and index == 0:
                observed = "0" * 64
            require(observed == expected, f"Stale PDF source: {name}")
        pdf = Path(receipt["pdf_path"])
        require(pdf.read_bytes().startswith(b"%PDF-"), "Not a PDF")
        require(digest(pdf) == receipt["pdf_sha256"], "PDF bytes changed")
    print(f"EDITORIAL_DELIVERY_VALID check={args.check} fixture={args.fixture or 'none'}")


if __name__ == "__main__":
    try:
        main()
    except AssertionError as error:
        print(f"EDITORIAL_DELIVERY_REJECTED: {error}", file=sys.stderr)
        sys.exit(1)
    except (OSError, ValueError, KeyError) as error:
        print(f"EDITORIAL_DELIVERY_UNVERIFIED: {error}", file=sys.stderr)
        sys.exit(3)
