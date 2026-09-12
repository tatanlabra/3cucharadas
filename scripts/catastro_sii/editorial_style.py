"""Shared, offline Matplotlib style matching the viewer's ECharts tokens.

Fira Sans is already distributed by this site. Conversion from WOFF2 is a
local render cache, not a new font download or published font artifact.
"""
from contextlib import contextmanager
import hashlib
import os
from pathlib import Path
import tempfile

os.environ.setdefault('MPLCONFIGDIR', '/tmp/avaluos-ii-matplotlib')
import matplotlib
matplotlib.use('Agg')
from matplotlib import font_manager

ROOT = Path(__file__).resolve().parents[2]
THEMES = {
    'light': dict(surface='#ffffff', ink='#132033', muted='#445570', line='#d6dfea',
                  track='#7f91a8', residual='#00778a', material='#6755c4'),
    'dark': dict(surface='#10121d', ink='#f3f5f8', muted='#a9afbd', line='#2a3041',
                 track='#7f91a8', residual='#37e7ff', material='#b58cff'),
}


def contrast(foreground, background):
    def luminance(color):
        channels = [int(color[i:i+2], 16)/255 for i in (1, 3, 5)]
        linear = [x/12.92 if x <= .04045 else ((x+.055)/1.055)**2.4 for x in channels]
        return sum(x*w for x, w in zip(linear, (.2126, .7152, .0722)))
    low, high = sorted((luminance(foreground), luminance(background)))
    return (high+.05)/(low+.05)


def register_fonts():
    from fontTools.ttLib import TTFont
    for weight in ('Regular', 'Bold'):
        source = ROOT/f'assets/fonts/fira-sans/FiraSans-{weight}.woff2'
        digest = hashlib.sha256(source.read_bytes()).hexdigest()[:16]
        target = Path(tempfile.gettempdir())/f'avaluos-fira-{weight}-{digest}.ttf'
        if not target.exists():
            font = TTFont(source)
            font.flavor = None
            font.save(target)
        font_manager.fontManager.addfont(target)


@contextmanager
def editorial_style(theme='light'):
    colors = THEMES[theme]
    register_fonts()
    with matplotlib.rc_context({
        'font.family': 'Fira Sans', 'font.size': 11,
        'text.color': colors['ink'], 'axes.labelcolor': colors['muted'],
        'figure.facecolor': colors['surface'], 'axes.facecolor': colors['surface'],
        'savefig.facecolor': colors['surface'], 'svg.fonttype': 'none',
        'svg.hashsalt': 'avaluos-editorial-v1', 'axes.unicode_minus': False,
    }):
        yield colors


SVG_FONT_FAMILY = 'Cucharadas Figure'


def svg_text_by_weight(svg):
    """Return the actual SVG text characters for each rendered font weight."""
    import re
    import xml.etree.ElementTree as ET
    used = {400: set(), 700: set()}
    root = ET.fromstring(svg)
    for node in root.iter('{http://www.w3.org/2000/svg}text'):
        style = node.get('style', '')
        weight = 700 if re.search(r'font-weight:\s*(700|bold)\b', style) else 400
        used[weight].update(''.join(node.itertext()))
    if not any(used.values()):
        raise ValueError('Cannot embed fonts for an SVG without text')
    return used


def subset_woff2(characters, weight):
    """Subset local outlines; keep copyright/OFL metadata and rename the RFN.

    No local() fallback is emitted: devices must use the embedded subset.
    The subset has its own family name because Fira is a Reserved Font Name.
    """
    from io import BytesIO
    from fontTools import subset
    from fontTools.ttLib import TTFont
    style = {400: 'Regular', 700: 'Bold'}[weight]
    path = ROOT/f'assets/fonts/fira-sans/FiraSans-{style}.woff2'
    font = TTFont(path, recalcTimestamp=False)
    missing = {ord(c) for c in characters} - set(font.getBestCmap())
    if missing:
        raise ValueError(f'Font lacks required Unicode codepoints: {sorted(missing)}')
    options = subset.Options()
    options.name_IDs = ['*']  # retain authorship, copyright, license and source links
    options.name_legacy = True
    options.name_languages = ['*']
    options.layout_features = ['*']
    options.recalc_timestamp = False
    subsetter = subset.Subsetter(options=options)
    subsetter.populate(unicodes=sorted(ord(c) for c in characters))
    subsetter.subset(font)
    names = {
        1: SVG_FONT_FAMILY, 2: style, 3: f'{SVG_FONT_FAMILY}-{style}-subset-v1',
        4: f'{SVG_FONT_FAMILY} {style}', 6: f'CucharadasFigure-{style}',
        16: SVG_FONT_FAMILY, 17: style, 18: f'{SVG_FONT_FAMILY} {style}',
        21: SVG_FONT_FAMILY, 22: style,
    }
    for entry in font['name'].names:
        if entry.nameID in names:
            entry.string = names[entry.nameID].encode(entry.getEncoding())
    font.flavor = 'woff2'
    buffer = BytesIO()
    font.save(buffer, reorderTables=True)
    return buffer.getvalue()


def embed_svg_fonts(svg):
    """Keep SVG text selectable with self-contained, weight-specific WOFF2 fonts.

    Data URLs work inside SVG-as-image without an external font request:
    https://developer.mozilla.org/en-US/docs/Web/SVG/Guides/SVG_as_an_image
    License metadata preserved as described by the OFL web-font guidance:
    https://openfontlicense.org/webfonts-and-reserved-font-names/
    """
    import base64
    faces = []
    for weight, characters in svg_text_by_weight(svg).items():
        if not characters:
            continue
        encoded = base64.b64encode(subset_woff2(characters, weight)).decode('ascii')
        faces.append(f"@font-face{{font-family:'{SVG_FONT_FAMILY}';font-style:normal;"
                     f"font-weight:{weight};src:url(data:font/woff2;base64,{encoded}) format('woff2');}}")
    svg = svg.replace("font-family: 'Fira Sans'", f"font-family: '{SVG_FONT_FAMILY}'")
    marker = '<defs>'
    if marker not in svg:
        raise ValueError('SVG has no definitions element')
    return svg.replace(marker, marker+'\n<style type="text/css" id="embedded-editorial-fonts">'+''.join(faces)+'</style>', 1)
