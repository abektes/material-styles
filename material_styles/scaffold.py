"""Scaffolding tool for generating new physical style plugins."""
import os
import re
from typing import Optional

from material_styles.registry import registry


def to_camel_case(text: str) -> str:
    """Convert string to CamelCase class name."""
    words = re.findall(r"[A-Za-z0-9]+", text)
    return "".join(w.capitalize() for w in words)


def to_snake_case(text: str) -> str:
    """Convert string to snake_case identifier."""
    words = re.findall(r"[A-Za-z0-9]+", text.lower())
    return "_".join(words)


def scaffold_style(
    name: str,
    style_id: Optional[str] = None,
    lineage: Optional[str] = None,
    number: Optional[int] = None,
    substrate_hex: str = "#FAF8F5",
    target_dir: str = "material_styles/styles/custom",
) -> str:
    """Scaffold a new physical style module with complete boilerplate."""
    cls_name = to_camel_case(name) + "Style"
    slug = to_snake_case(name)
    sid = style_id or f"style_{slug}"
    lin = lineage or f"{name} (Movement)"

    if number is None:
        styles = registry.list_styles()
        max_num = max((s.metadata.number for s in styles), default=15)
        number = max_num + 1

    filename = f"s{number:02d}_{slug}.py"
    filepath = os.path.join(target_dir, filename)
    os.makedirs(target_dir, exist_ok=True)

    code = f'''"""Style {number:02d}: {name} ({lin})."""
from typing import Optional
from material_styles.core.content import PosterContent
from material_styles.core.poster import StylePoster, S
from material_styles.styles.base import BaseStyle, StyleMetadata

# Physical Substrate & Spot Inks
SUB_STOCK = (0xFA, 0xF8, 0xF5)
INK_PRIMARY = (0x18, 0x18, 0x1A)
INK_ACCENT = (0xE5, 0x39, 0x35)


class {cls_name}(BaseStyle):
    metadata = StyleMetadata(
        id="{sid}",
        number={number},
        name="{name}",
        lineage="{lin}",
        substrate_hex="{substrate_hex}",
        substrate_rgb=SUB_STOCK,
        inks=[INK_PRIMARY, INK_ACCENT],
        gate_range=(28, 50),
        description="Physical print mechanics and reproductive engine description.",
        default_content=PosterContent(
            headline="PROCLAMATION",
            subhead="{name.upper()}",
            footnote="SYSTEMATIC MATERIAL REPRODUCTION // LIMITED EDITION",
            accession_code="SPEC-{number:02d}",
        ),
    )

    def render(
        self,
        P: Optional[StylePoster] = None,
        content: Optional[PosterContent] = None,
        outdir: str = "styles_gallery",
    ) -> dict:
        if P is None:
            P = self.create_poster()
        content = content or self.metadata.default_content
        headline = content.get_slot("headline", "PROCLAMATION")
        subhead = content.get_slot("subhead", "{name.upper()}")
        footnote = content.get_slot("footnote", "SYSTEMATIC MATERIAL REPRODUCTION // LIMITED EDITION")
        accession = content.get_slot("accession_code", "SPEC-{number:02d}")

        dx, dy = P.drift

        # 1. Structural geometry & screening
        P.rect(120, 240, 1080, 1080, INK_PRIMARY)
        P.rotated_halftone(
            180, 300, 1020, 1020,
            pitch=16, angle_deg=45,
            density_fn=lambda x, y: 0.6,
            ink=INK_ACCENT, shape="circle"
        )

        # 2. Typographic hierarchy
        P.text((120, 140), headline, "grotesk_bold", 100, INK_PRIMARY, tracking=-2)
        P.text((120, 1140), subhead, "din_bold", 48, INK_ACCENT, tracking=1)
        P.text((120, 1220), footnote, "mono", 16, INK_PRIMARY, tracking=1)
        P.text((120, 1260), accession, "mono_bold", 18, INK_PRIMARY, tracking=2)

        # 3. Registration marks
        rx, ry = 1110 + dx, 1500 + dy
        P.ring(rx, ry, 12, 1.0, INK_ACCENT)
        P.line([(rx - 16, ry), (rx + 16, ry)], INK_ACCENT, w=1.0)
        P.line([(rx, ry - 16), (rx, ry + 16)], INK_ACCENT, w=1.0)

        # 4. Zone mask for empty paper gate verification
        def zm(dm):
            dm.rectangle([120 * S, 140 * S, 1080 * S, 1300 * S], fill=255)

        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=self.metadata.gate_range)
'''

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(code)

    return filepath
