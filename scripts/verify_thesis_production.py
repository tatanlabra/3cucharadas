#!/usr/bin/env python3
"""Observe actual remote refs, deployment jobs, pages and public asset bytes."""
import argparse
import concurrent.futures
import hashlib
import json
import subprocess
import sys
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SITE = "https://3cucharadas.cl"
SLUGS = ("costos-cierre-escolar-trayectorias", "cierre-escolar-educacion-superior-causal-ml")


def command(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True, timeout=90).strip()


def fetch(path):
    request = urllib.request.Request(SITE + path, headers={"User-Agent": "3cucharadas-release-verification/1"})
    with urllib.request.urlopen(request, timeout=45) as response:
        return response.read()


def digest(value):
    return hashlib.sha256(value).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--artifact-root", type=Path, required=True)
    parser.add_argument("--receipt", type=Path, required=True)
    parser.add_argument("--expected-sha")
    args = parser.parse_args()
    expected = args.expected_sha or command("git", "rev-parse", "HEAD")
    report = {"expected_sha": expected, "remote_refs": {}, "pages": [], "assets": [], "failures": []}
    try:
        for name, url in (("gitlab", "git@gitlab.com:tatanlabra/3cucharadas.git"),
                          ("github", "https://github.com/tatanlabra/3cucharadas.git")):
            actual = command("git", "ls-remote", url, "refs/heads/main").split()[0]
            report["remote_refs"][name] = actual
            if actual != expected:
                report["failures"].append(f"{name}: remote SHA differs")
        if report["failures"]:
            raise ValueError("Remote commit mismatch; deployment verification cannot proceed")
        pipelines = json.loads(command("glab", "api", f"projects/57339918/pipelines?sha={expected}&per_page=20"))
        if not pipelines:
            raise ValueError("No pipeline for expected SHA")
        pipeline = max(pipelines, key=lambda row: row["id"])
        report["pipeline"] = pipeline
        jobs = json.loads(command("glab", "api", f"projects/57339918/pipelines/{pipeline['id']}/jobs?per_page=100"))
        report["jobs"] = [{key: row[key] for key in ("id", "name", "status", "web_url")} for row in jobs]
        if pipeline["status"] != "success":
            report["failures"].append("Pipeline is not successful")
        for required in ("build_site", "pages"):
            if not any(row["name"] == required and row["status"] == "success" for row in jobs):
                report["failures"].append(f"Missing successful {required} job")
        assets = set()
        for part in (3, 4):
            folder = Path(f"assets/images/tesis-post{part}")
            manifest = json.loads((ROOT / folder / "manifest.json").read_text())
            if not manifest.get("files"):
                raise ValueError(f"Empty manifest {folder}")
            assets.add(str(folder / "manifest.json"))
            assets.update(str(folder / row["path"]) for row in manifest["files"])
        assets.update(str(path.relative_to(ROOT)) for path in
                      (ROOT / "assets/images/heroes-v2/cierre-escolar-educacion-superior-causal-ml").glob("*.webp"))
        for lang in ("", "/en"):
            for slug in SLUGS:
                for suffix in ("", "anexo-metodologico/"):
                    route = f"{lang}/datos/educacion/politica-publica/{slug}/{suffix}"
                    local = args.artifact_root / route.lstrip("/") / "index.html"
                    public = BeautifulSoup(fetch(route), "html.parser")
                    built = BeautifulSoup(local.read_bytes(), "html.parser")
                    public_body, built_body = public.select_one(".page__content"), built.select_one(".page__content")
                    equal = public_body is not None and built_body is not None and str(public_body) == str(built_body)
                    report["pages"].append({"route": route, "article_dom_equal": equal})
                    if not equal:
                        report["failures"].append(f"Public article DOM differs: {route}")
        def check_asset(path):
            body = fetch("/" + path)
            local_hash = digest((ROOT / path).read_bytes())
            return {"path": path, "public_sha256": digest(body), "local_sha256": local_hash,
                    "equal": digest(body) == local_hash}
        with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
            report["assets"] = list(pool.map(check_asset, sorted(assets)))
        report["failures"].extend(f"Stale public asset: {row['path']}" for row in report["assets"] if not row["equal"])
        if len(report["pages"]) != 8 or len(report["assets"]) < 130:
            report["failures"].append("Incomplete verification coverage")
    except Exception as error:
        report["failures"].append(str(error))
    report["status"] = "FAIL" if report["failures"] else "PASS"
    args.receipt.parent.mkdir(parents=True, exist_ok=True)
    args.receipt.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"status": report["status"], "pages": len(report["pages"]),
                      "assets": len(report["assets"]), "failures": report["failures"]}))
    return 1 if report["failures"] else 0


if __name__ == "__main__":
    sys.exit(main())
