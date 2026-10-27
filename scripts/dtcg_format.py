"""Valida tokens DTCG 2025.10 con el schema oficial vendorizado y semántica sRGB."""

from __future__ import annotations

import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

from jsonschema import FormatChecker
from jsonschema.validators import validator_for
from referencing import Registry, Resource
from referencing.exceptions import NoSuchResource

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_DIR = ROOT / "assets/data/tesis-post3/dtcg/2025.10"
PROVENANCE = ROOT / "assets/data/tesis-post3/dtcg/PROVENANCE.json"
SCHEMA_URL = "https://www.designtokens.org/schemas/2025.10/format.json"
EXTENSION_NAMESPACE = "org.3cucharadas"
HEX = re.compile(r"#[0-9a-fA-F]{6}\Z")
MODES = ("light", "dark")
COLORS = ("canvas", "surface", "ink", "muted", "grid", "accent", "focus", "positive", "negative", "warning")
SERIES = ("one", "two", "three", "four", "five", "six")


class DTCGError(ValueError):
    """El documento no satisface el schema oficial o la semántica local."""


def _offline_retrieve(uri: str) -> Resource:
    raise NoSuchResource(ref=uri)


def _schema_validator() -> Any:
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    files = provenance["files"]
    if not files or "format.json" not in files:
        raise DTCGError("provenance DTCG incompleta")
    store: dict[str, Any] = {}
    base = provenance["schema_base_url"].rstrip("/")
    for relative, expected_hash in files.items():
        path = SCHEMA_DIR / relative
        raw = path.read_bytes()
        if hashlib.sha256(raw).hexdigest() != expected_hash:
            raise DTCGError(f"schema DTCG alterado: {relative}")
        store[f"{base}/{relative}"] = json.loads(raw)
    schema = store[SCHEMA_URL]
    validator_class = validator_for(schema)
    validator_class.check_schema(schema)
    registry = Registry(retrieve=_offline_retrieve).with_resources(
        (uri, Resource.from_contents(document)) for uri, document in store.items()
    )
    return validator_class(schema, registry=registry, format_checker=FormatChecker())


def color_hex(node: dict[str, Any], label: str = "color") -> str:
    if not isinstance(node, dict) or node.get("$type") != "color":
        raise DTCGError(f"{label}: token sin $type=color")
    value = node.get("$value")
    if not isinstance(value, dict) or value.get("colorSpace") != "srgb":
        raise DTCGError(f"{label}: se requiere objeto color sRGB")
    hex_value = value.get("hex")
    components = value.get("components")
    alpha = value.get("alpha")
    if not isinstance(hex_value, str) or not HEX.fullmatch(hex_value):
        raise DTCGError(f"{label}: hex inválido")
    if not isinstance(components, list) or len(components) != 3:
        raise DTCGError(f"{label}: components requiere tres canales")
    if type(alpha) not in (int, float) or alpha != 1:
        raise DTCGError(f"{label}: alpha opaco requerido")
    for index, channel in enumerate(components):
        if type(channel) not in (int, float) or not math.isfinite(channel) or not 0 <= channel <= 1:
            raise DTCGError(f"{label}: components[{index}] inválido")
        expected = int(hex_value[1 + 2 * index:3 + 2 * index], 16) / 255
        if not math.isclose(channel, expected, rel_tol=0, abs_tol=5e-13):
            raise DTCGError(f"{label}: components[{index}] difiere de hex")
    return hex_value.lower()


def metadata(tokens: dict[str, Any]) -> dict[str, Any]:
    if "meta" in tokens:
        raise DTCGError("meta raíz no está permitido; usar $extensions")
    extension = tokens.get("$extensions", {}).get(EXTENSION_NAMESPACE)
    if not isinstance(extension, dict) or extension.get("runtimeRemoteDependencies") != []:
        raise DTCGError("$extensions.org.3cucharadas.runtimeRemoteDependencies debe ser []")
    return extension


def validate_document(tokens: dict[str, Any]) -> None:
    if not isinstance(tokens, dict):
        raise DTCGError("la raíz debe ser objeto")
    if tokens.get("$schema") != SCHEMA_URL:
        raise DTCGError("$schema debe fijar DTCG 2025.10")
    validator = _schema_validator()
    errors = sorted(validator.iter_errors(tokens), key=lambda error: tuple(map(str, error.absolute_path)))
    if errors:
        error = errors[0]
        location = ".".join(map(str, error.absolute_path)) or "$root"
        raise DTCGError(f"schema DTCG 2025.10: {location}: {error.message}")
    metadata(tokens)
    try:
        for mode in MODES:
            palette = tokens["color"][mode]
            for name in COLORS:
                color_hex(palette[name], f"color.{mode}.{name}")
            for name in SERIES:
                color_hex(palette["series"][name], f"color.{mode}.series.{name}")
    except (KeyError, TypeError) as error:
        raise DTCGError(f"paleta incompleta: {error}") from error


def schema_sha256() -> str:
    return hashlib.sha256((SCHEMA_DIR / "format.json").read_bytes()).hexdigest()
