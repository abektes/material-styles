"""Style 10: Braun Industrial Patent Schematic (Dieter Rams, Bauhaus Industrial Drawing Office)."""
import math
from typing import Optional

from PIL import Image, ImageChops, ImageDraw

from material_styles.core.content import PosterContent
from material_styles.core.poster import StylePoster, S, UW, UH, W, H
from material_styles.core.primitives import multiply_colors, mix_colors
from material_styles.core.typography import load_font
from material_styles.styles.base import BaseStyle, StyleMetadata

# ----------------- Substrates & Inks -----------------
SUB_ARTBOARD = (0xF5, 0xF5, 0xF3)          # 01 Zurich
SUB_POP_CARDSTOCK = (0xFA, 0xF8, 0xF5)     # 02 Pop Serigraphy
SUB_VELLUM = (0xFC, 0xFA, 0xF2)            # 03 Tokyo Riso
SUB_STRAW = (0xEA, 0xE3, 0xD2)             # 04 Agit-Prop
SUB_DUTCH = (0xF4, 0xF5, 0xF7)             # 05 Dutch Matrix
SUB_THERMAL = (0xEC, 0xE8, 0xDC)           # 06 Thermal Fax
SUB_LINEN = (0xF5, 0xEF, 0xE1)             # 07 Victorian
SUB_BOND = (0xED, 0xEC, 0xE8)              # 08 Punk Xerox
SUB_DESTIJL_PRESSBOARD = (0xF5, 0xF3, 0xEB)# 09 De Stijl
SUB_DRAFT = (0xF8, 0xF8, 0xF6)             # 10 Patent
SUB_WASHI = (0xF6, 0xF2, 0xE8)             # 11 Sosaku Hanga
SUB_KROMEKOTE = (0xFB, 0xFB, 0xFD)         # 12 Swiss Cyber
SUB_ALBUM_JACKET = (0xF4, 0xF1, 0xEA)      # 13 Blue Note
SUB_BROMO_CHLORIDE = (0xEF, 0xEC, 0xE4)    # 14 Bauhaus Typofoto
SUB_POLISH_OFFSET = (0xF3, 0xEF, 0xEA)     # 15 Polish Surrealism

INK_ZURICH_BLACK = (0x11, 0x11, 0x11)
INK_SWISS_RED = (0xE5, 0x39, 0x35)
INK_POP_MAGENTA = (0xE6, 0x00, 0x7A)
INK_POP_YELLOW = (0xFF, 0xDE, 0x00)
INK_POP_CYAN = (0x00, 0x9F, 0xE3)
INK_SQUEEGEE_BLACK = (0x18, 0x18, 0x1A)
INK_RISO_PINK = (0xFF, 0x40, 0x98)
INK_RISO_AQUA = (0x00, 0xA4, 0xD3)
INK_RISO_CARBON = (0x2B, 0x2A, 0x29)
INK_AGIT_CARBON = (0x1A, 0x19, 0x18)
INK_AGIT_VERMILION = (0xD7, 0x26, 0x26)
INK_DUTCH_ULTRAMARINE = (0x17, 0x36, 0x9B)
INK_FLAME_ORANGE = (0xF0, 0x4D, 0x23)
INK_THERMAL_BLACK = (0x1C, 0x1B, 0x1A)
INK_BITUMEN = (0x2C, 0x25, 0x23)
INK_MINERAL_INDIGO = (0x25, 0x40, 0x5A)
INK_BURNT_UMBER = (0x8A, 0x56, 0x36)
INK_COPIER_TONER = (0x18, 0x18, 0x18)
INK_ACID_LEMON = (0xE6, 0xFF, 0x00)
INK_DESTIJL_RED = (0xD3, 0x2F, 0x2F)
INK_DESTIJL_BLUE = (0x19, 0x39, 0x8A)
INK_DESTIJL_YELLOW = (0xF9, 0xC8, 0x0E)
INK_DESTIJL_BLACK = (0x14, 0x14, 0x14)
INK_INDIA_TECH = (0x1C, 0x1D, 0x1F)
INK_BAUHAUS_YELLOW = (0xF5, 0xA6, 0x23)
INK_SUMI = (0x1A, 0x18, 0x16)
INK_CINNABAR = (0xD9, 0x38, 0x1E)
INK_AOMORI_INDIGO = (0x26, 0x4E, 0x5A)
INK_LASER_CYAN = (0x00, 0xF0, 0xFF)
INK_ACID_CHARTREUSE = (0xD4, 0xFF, 0x00)
INK_NEON_MAGENTA = (0xFF, 0x00, 0x55)
INK_CYBER_BLACK = (0x0C, 0x0C, 0x0E)
INK_VELVET_BLACK = (0x16, 0x16, 0x16)
INK_BLUE_NOTE_OCHRE = (0xE5, 0x95, 0x00)
INK_EMULSION_BLACK = (0x12, 0x11, 0x10)
INK_BAUHAUS_RED = (0xD6, 0x28, 0x28)
INK_GOUACHE_CHARCOAL = (0x1C, 0x1B, 0x1A)
INK_POISON_OLIVE = (0x4D, 0x6A, 0x34)
INK_CRIMSON_RUST = (0xA6, 0x2B, 0x2B)




class BraunPatentSchematicStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_braun_patent_schematic",
        number=10,
        name="Braun Industrial Patent Schematic",
        lineage="Dieter Rams, Bauhaus Industrial Drawing Office",
        substrate_hex="#F8F8F6",
        substrate_rgb=SUB_DRAFT,
        inks=[INK_INDIA_TECH, INK_BAUHAUS_YELLOW],
        gate_range=(32, 52),
        description="ISO line-weight hierarchy (0.5/0.25mm), exploded isometric assembly, dimension witness lines",
        slug="10-braun-patent-schematic",
        default_content=PosterContent(
            headline="ELEKTRISCHER RASIERAPPARAT",
            subhead="BRAUN AG FRANKFURT AM MAIN // MODELL SI 2",
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
        headline = content.get_slot("headline", "ELEKTRISCHER RASIERAPPARAT")
        subhead = content.get_slot("subhead", "BRAUN AG FRANKFURT AM MAIN // MODELL SI 2")
        # Subtle 40px metric drafting grid lines
        for x in range(60, UW - 60, 40):
            P.line([(x, 60), (x, UH - 60)], (0xE2, 0xE2, 0xDF), w=0.5)
        for y in range(60, UH - 60, 40):
            P.line([(60, y), (UW - 60, y)], (0xE2, 0xE2, 0xDF), w=0.5)

        # Technical Border Frame
        P.rect(60, 60, 1140, 1540, INK_INDIA_TECH)
        P.rect(63, 63, 1137, 1537, SUB_DRAFT)

        # Technical Header
        P.text((90, 90), "PATENTSCHRIFT NR. DE-1972844-B", "din_bold", 18, INK_INDIA_TECH, tracking=3)
        P.text((1110, 90), "KLASSE 21a4 — GRUPPE 12", "din", 16, INK_INDIA_TECH, tracking=2, anchor_x="right")
        P.line([(90, 125), (1110, 125)], INK_INDIA_TECH, w=1.5)

        # Main Figure Title
        P.text((90, 160), "FIG. 4 — DREHKNOPF-STEUERUNG", "din_bold", 44, INK_INDIA_TECH, tracking=2)
        P.text((90, 220), "EXPLODED ISOMETRIC ASSEMBLY // ROTARY ENCODER MECHANISM", "din", 18, INK_INDIA_TECH, tracking=1)

        # Bauhaus Signal Yellow Highlight Accent Block
        P.rect(260, 420, 940, 980, INK_BAUHAUS_YELLOW)

        # Precision Axonometric / Isometric Exploded Cylinder Assembly
        def iso_cylinder(cx, cy, rx, ry, h, ink):
            # Bottom ellipse
            P.ell(cx - rx, cy + h - ry, cx + rx, cy + h + ry, ink, outline=True, width=2.0)
            # Side lines
            P.line([(cx - rx, cy), (cx - rx, cy + h)], ink, w=2.0)
            P.line([(cx + rx, cy), (cx + rx, cy + h)], ink, w=2.0)
            # Top ellipse (filled with paper knockout)
            P.ell(cx - rx, cy - ry, cx + rx, cy + ry, SUB_DRAFT)
            P.ell(cx - rx, cy - ry, cx + rx, cy + ry, ink, outline=True, width=2.0)

        # Component 1: Rotary Knob Dial
        iso_cylinder(600, 480, 240, 90, 120, INK_INDIA_TECH)
        # Component 2: Flanged Mounting Collar
        iso_cylinder(600, 720, 190, 70, 80, INK_INDIA_TECH)
        # Component 3: Splined Core Spindle
        iso_cylinder(600, 920, 90, 35, 140, INK_INDIA_TECH)

        # Isometric Axis Centerline (Dash pattern)
        for y in range(360, 1140, 24):
            P.line([(600, y), (600, y + 14)], INK_INDIA_TECH, w=1.0)

        # Numbered Callout Leaders
        P.spec_callout(360, 540, "1", INK_INDIA_TECH, lead_dx=-140, lead_dy=-40)
        P.spec_callout(410, 760, "2", INK_INDIA_TECH, lead_dx=-190, lead_dy=0)
        P.spec_callout(510, 990, "3", INK_INDIA_TECH, lead_dx=-290, lead_dy=40)
        P.spec_callout(840, 540, "4a", INK_INDIA_TECH, lead_dx=140, lead_dy=-40)

        # Specification Legend Table in lower quadrant
        P.rect(90, 1180, 1110, 1480, INK_INDIA_TECH)
        P.rect(92, 1182, 1108, 1478, SUB_DRAFT)
        P.line([(90, 1240), (1110, 1240)], INK_INDIA_TECH, w=1.5)
        P.line([(420, 1180), (420, 1480)], INK_INDIA_TECH, w=1.0)
        P.line([(760, 1180), (760, 1480)], INK_INDIA_TECH, w=1.0)

        P.text((110, 1205), "TEIL-NR. / BENENNUNG", "din_bold", 16, INK_INDIA_TECH)
        P.text((440, 1205), "WERKSTOFF / NORM", "din_bold", 16, INK_INDIA_TECH)
        P.text((780, 1205), "MASSANGABE / TOLERANZ", "din_bold", 16, INK_INDIA_TECH)

        specs = [
            ("1. DREHKNOPF-AUSSENRING", "ALUMINIUM ELOXIERT", "Ø 120.0 mm ± 0.05"),
            ("2. RASTBLENDE MIT FEDER", "POLYACETAL (POM)", "Ø 95.0 mm ± 0.10"),
            ("3. ACHSWELLE 18-ZAHN", "EDELSTAHL 1.4301", "Ø 45.0 mm DIN 5480"),
            ("4a. SKALENRING 360°", "POLYCARBONAT WEISS", "TEILUNG 1° PRÄZISION"),
        ]
        for idx, (c1, c2, c3) in enumerate(specs):
            yy = 1265 + idx * 48
            P.text((110, yy), c1, "din", 15, INK_INDIA_TECH)
            P.text((440, yy), c2, "din", 15, INK_INDIA_TECH)
            P.text((780, yy), c3, "mono", 15, INK_INDIA_TECH)

        def zm(dm):
            dm.rectangle([60 * S, 60 * S, 1140 * S, 250 * S], fill=255)
            dm.rectangle([220 * S, 360 * S, 980 * S, 1140 * S], fill=255)
            dm.rectangle([90 * S, 1180 * S, 1110 * S, 1480 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(32, 52))


