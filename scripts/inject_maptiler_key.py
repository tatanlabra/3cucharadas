#!/usr/bin/env python3
"""Keep the legacy configuration inert after the self-hosted PMTiles migration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    payload = {"legacyMapDisabled": True}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("window.CATASTRO_MAP_CONFIG = " + json.dumps(payload) + ";\n", encoding="utf-8")
    print("Legacy map configuration left disabled; Vite loads the local MapLibre bundle.")


if __name__ == "__main__":
    main()
