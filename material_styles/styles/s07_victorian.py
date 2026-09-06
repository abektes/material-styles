"""Style 07: Victorian Chromolitho Naturalist (Ernst Haeckel (Kunstformen der Natur), Linnaean Plates)."""
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




class VictorianChromolithoStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_victorian_chromolitho",
        number=7,
        name="Victorian Chromolitho Naturalist",
        lineage="Ernst Haeckel (Kunstformen der Natur), Linnaean Plates",
        substrate_hex="#F5EFE1",
        substrate_rgb=SUB_LINEN,
        inks=[INK_BITUMEN, INK_MINERAL_INDIGO, INK_BURNT_UMBER],
        gate_range=(38, 56),
        description="Intaglio debossed plate border, fine copperplate crosshatching, engraved script + Latin binomials",
        slug="07-victorian-chromolitho",
        default_content=PosterContent(
            headline="DISOMPHALIA DISCOPHORA",
            subhead="TAB. VII. RADIOLARIA ACANTHOMETRA",
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
        headline = content.get_slot("headline", "DISOMPHALIA DISCOPHORA")
        subhead = content.get_slot("subhead", "TAB. VII. RADIOLARIA ACANTHOMETRA")
        # Embossed intaglio plate depression border
        P.rect(100, 120, 1100, 1480, INK_BITUMEN)
        P.rect(104, 124, 1096, 1476, SUB_LINEN)
        P.rect(112, 132, 1088, 1468, INK_BITUMEN)
        P.rect(114, 134, 1086, 1466, SUB_LINEN)

        # Plate Roman numeral corner index
        P.text((140, 150), "Haeckel, Kunstformen der Natur.", "serif_italic", 16, INK_BITUMEN)
        P.text((1060, 150), "TAB. XLII.", "serif_bold", 18, INK_BITUMEN, anchor_x="right")

        # Concentric radial crosshatching: Anatomical Medusa Specimen
        cx, cy = 600, 680
        for r in range(40, 320, 24):
            P.ring(cx, cy, r, 1.2, INK_MINERAL_INDIGO)

        # 16 Radial umbrella ribs
        for i in range(16):
            ang = math.radians(i * (360 / 16))
            x2 = cx + math.cos(ang) * 320
            y2 = cy + math.sin(ang) * 320
            P.line([(cx, cy), (x2, y2)], INK_BITUMEN, w=2.0)
            # Burnt umber watercolor accent wash dot
            P.dot(x2, y2, 8, INK_BURNT_UMBER)

        # Fine crosshatch density in the core
        def medusa_density(x, y):
            dist = math.hypot(x - cx, y - cy)
            return max(0.0, 1.0 - dist / 280)

        P.crosshatch_field(320, 400, 880, 960, medusa_density, INK_BITUMEN, pitch=12)

        # Trailing tentacles
        for i in range(8):
            tx = cx - 180 + i * 50
            pts = [(tx, 960), (tx - 30, 1100), (tx + 20, 1220), (tx - 10, 1320)]
            P.line(pts, INK_MINERAL_INDIGO, w=1.5)

        # Scientific Linnaean Classification Typography
        P.text((600, 1360), "DISCOPHORA RADIATA", "serif_bold", 38, INK_BITUMEN, tracking=4, anchor_x="center")
        P.text((600, 1410), "Medusae acraspedae. — 1. Aurelia aurita. 2. Pelagia noctiluca.", "serif_italic", 18, INK_BURNT_UMBER, anchor_x="center")

        def zm(dm):
            dm.rectangle([140 * S, 170 * S, 1060 * S, 1430 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(38, 56))


