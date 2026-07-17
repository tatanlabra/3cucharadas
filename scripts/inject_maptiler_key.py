#!/usr/bin/env python3
"""Inject the public MapTiler key only into an already-built static artifact."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--maplibre-script", default="")
    parser.add_argument("--maplibre-css", default="")
    args = parser.parse_args()
    key = os.environ.get("MAPTILER_PUBLIC_KEY", "")
    payload = {
        "maptilerKey": key,
        "maplibreScript": args.maplibre_script,
        "maplibreCss": args.maplibre_css,
        "styleUrl": "https://api.maptiler.com/maps/dataviz-dark/style.json?key={key}",
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("window.CATASTRO_MAP_CONFIG = " + json.dumps(payload) + ";\n", encoding="utf-8")
    print(f"MapTiler configured: {bool(key)}")


if __name__ == "__main__":
    main()
