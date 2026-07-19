from __future__ import annotations

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = ROOT / "scripts" / "catastro_sii" / "protomaps-basemap-style.template.json"
PLACEHOLDER = "__BASEMAP_PM_TILES__"


def luminance(hex_color: str) -> float:
    """Luminancia relativa aproximada (0 negro, 1 blanco)."""
    value = hex_color.lstrip("#")
    if len(value) == 3:
        value = "".join(character * 2 for character in value)
    red, green, blue = (int(value[index:index + 2], 16) / 255 for index in (0, 2, 4))
    return 0.2126 * red + 0.7152 * green + 0.0722 * blue


class BasemapStyleTemplateTests(unittest.TestCase):
    """La paleta clara se validó a ojo y vivía sólo en una ruta ignorada por Git.

    La plantilla versionada seguía produciendo el neón oscuro, así que regenerar el
    basemap revertía el diseño aprobado sin que nada avisara. Estas pruebas fijan el
    contrato: la plantilla es la única fuente del estilo y produce la paleta clara.
    """

    def setUp(self) -> None:
        self.raw = TEMPLATE.read_text(encoding="utf-8")
        self.style = json.loads(self.raw)

    def test_template_keeps_the_tile_placeholder(self) -> None:
        self.assertEqual(self.raw.count(PLACEHOLDER), 1)

    def test_background_is_light(self) -> None:
        background = next(
            layer for layer in self.style["layers"] if layer["id"] == "background"
        )
        color = background["paint"]["background-color"]
        self.assertGreater(
            luminance(color), 0.7,
            f"El fondo del basemap dejó de ser claro: {color}",
        )

    def test_no_neon_saturation_survives(self) -> None:
        """El neón rechazado se reconoce por colores muy saturados y brillantes."""
        offenders = []
        for layer in self.style["layers"]:
            for key, value in (layer.get("paint") or {}).items():
                if not (isinstance(value, str) and value.startswith("#") and "color" in key):
                    continue
                raw = value.lstrip("#")
                if len(raw) == 3:
                    raw = "".join(character * 2 for character in raw)
                channels = [int(raw[index:index + 2], 16) for index in (0, 2, 4)]
                spread = max(channels) - min(channels)
                if spread > 120 and max(channels) > 200:
                    offenders.append(f"{layer['id']}.{key}={value}")
        self.assertEqual(offenders, [], f"Colores neón en la plantilla: {offenders}")

    def test_style_declares_the_self_hosted_glyphs(self) -> None:
        self.assertIn("glyphs", self.style)


if __name__ == "__main__":
    unittest.main()
