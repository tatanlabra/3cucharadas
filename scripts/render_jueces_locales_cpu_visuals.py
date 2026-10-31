#!/usr/bin/env python3
"""Sync CSV and manifest.json for the local CPU judges PoC post (1 D2 diagram + 1 CSV)."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
IMG_DIR = REPO_ROOT / "assets" / "images" / "jueces-locales-cpu"
DATA_DIR = REPO_ROOT / "assets" / "data" / "jueces-locales-cpu"

ROWS = [
    {
        "id": "laya_0_4_11",
        "label": "Laya 0.4.11 (PyTorch CPU)",
        "short_label": "Laya 0.4.11",
        "ram_gib": 2.26,
        "cold_s": 13.83,
        "warm_p95_ms": 366,
        "coverage_pct": 80.00,
        "selective_acc_pct": 41.41,
        "decided": "53/128",
        "yes_correct": 52,
        "no_correct": 1,
        "indef_correct": 13,
        "three_way_pct": 41.25,
        "false_positives": 73,
        "badge": "El que aprueba (Sí en 125/160)",
    },
    {
        "id": "vega_0_11_0",
        "label": "VegaML 0.11.0 (Qwen 0.8B CPU)",
        "short_label": "VegaML 0.11.0",
        "ram_gib": 4.93,
        "cold_s": 13.66,
        "warm_p95_ms": 1717,
        "coverage_pct": 78.13,
        "selective_acc_pct": 40.80,
        "decided": "51/125",
        "yes_correct": 0,
        "no_correct": 51,
        "indef_correct": 10,
        "three_way_pct": 38.13,
        "false_positives": 4,
        "badge": "El que rechaza (No en 131/160)",
    },
    {
        "id": "arc_0_4b_v0_2",
        "label": "Arc Decide 0.4B v0.2 (ONNX)",
        "short_label": "Arc 0.4B ONNX",
        "ram_gib": 0.59,
        "cold_s": 4.21,
        "warm_p95_ms": 950,
        "coverage_pct": 60.63,
        "selective_acc_pct": 47.42,
        "decided": "46/97",
        "yes_correct": 41,
        "no_correct": 5,
        "indef_correct": 22,
        "three_way_pct": 42.50,
        "false_positives": 49,
        "badge": "El silencioso en panel (12/160)",
    },
    {
        "id": "panel_2of3",
        "label": "Panel 2-de-3 (Laya + Vega + Arc)",
        "short_label": "Panel 2-de-3",
        "ram_gib": 4.93,
        "cold_s": 31.70,
        "warm_p95_ms": 3033,
        "coverage_pct": 9.38,
        "selective_acc_pct": 66.67,
        "decided": "10/15",
        "yes_correct": 10,
        "no_correct": 0,
        "indef_correct": 36,
        "three_way_pct": 28.75,
        "false_positives": 3,
        "badge": "9,38 % cobertura · 0/60 en No",
    },
    {
        "id": "always_indefinite",
        "label": 'Siempre "Indefinido" (baseline)',
        "short_label": "Siempre Indefinido",
        "ram_gib": 0.00,
        "cold_s": 0.00,
        "warm_p95_ms": 0,
        "coverage_pct": 0.00,
        "selective_acc_pct": 0.00,
        "decided": "0/0",
        "yes_correct": 0,
        "no_correct": 0,
        "indef_correct": 40,
        "three_way_pct": 25.00,
        "false_positives": 0,
        "badge": "25,00 % triclase callando siempre",
    },
]


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    for stale_svg in IMG_DIR.glob("jueces-locales-aciertos-clases-es-*.svg"):
        stale_svg.unlink(missing_ok=True)

    csv_path = DATA_DIR / "jueces-locales-panel-v2-summary.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(ROWS[0].keys()))
        writer.writeheader()
        writer.writerows(ROWS)

    d2_outputs = {
        "d2_desktop": IMG_DIR / "fig-d2-colapso-panel.svg",
        "d2_mobile": IMG_DIR / "fig-d2-colapso-panel-mobile.svg",
    }

    manifest = {
        "schema_version": 1,
        "contract": "DESIGN.md (3cucharadas Cuaderno de Evidencia)",
        "source_receipt": "penta-agent/reports/simil-jev-panel/receipts/panel-evaluation-v2.json",
        "csv": {
            "path": str(csv_path.relative_to(REPO_ROOT)),
            "sha256": sha256_file(csv_path),
        },
        "figures": {
            key: {
                "path": str(path.relative_to(REPO_ROOT)),
                "sha256": sha256_file(path),
            }
            for key, path in d2_outputs.items()
            if path.is_file()
        },
    }
    (DATA_DIR / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    img_manifest_path = IMG_DIR / "manifest.json"
    img_files = sorted(
        p for p in IMG_DIR.rglob("*") if p.is_file() and p != img_manifest_path
    )
    img_manifest = {
        "schema_version": 1,
        "contract": "DESIGN.md (3cucharadas Cuaderno de Evidencia)",
        "files": [
            {
                "path": str(p.relative_to(IMG_DIR)),
                "bytes": p.stat().st_size,
                "sha256": sha256_file(p),
            }
            for p in img_files
        ],
    }
    img_manifest_path.write_text(
        json.dumps(img_manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print("PASS synced CSV + D2 manifest.json (data + images)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
