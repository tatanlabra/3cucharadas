#!/usr/bin/env python3
"""Compatibility entry point: local commits never send Telegram messages."""

from __future__ import annotations

import argparse
import sys


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Deprecated: local commits no longer produce Telegram notifications.",
    )
    parser.add_argument("--repo-root", default=".", help=argparse.SUPPRESS)
    parser.add_argument("--dry-run", action="store_true", help=argparse.SUPPRESS)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    parse_args(argv)
    print("telegram-suppressed-local-commit")
    return 0


if __name__ == "__main__":
    sys.exit(main())
