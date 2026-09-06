"""Style 12: 1980s Swiss Cyber New Wave (Wolfgang Weingart, April Greiman (Pacific Wave 1982))."""
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




class SwissCyberNewWaveStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_swiss_cyber_newwave",
        number=12,
        name="1980s Swiss Cyber New Wave",
        lineage="Wolfgang Weingart, April Greiman (Pacific Wave 1982)",
        substrate_hex="#F8F8FC",
        substrate_rgb=SUB_KROMEKOTE,
        inks=[INK_LASER_CYAN, INK_ACID_CHARTREUSE, INK_NEON_MAGENTA, INK_CYBER_BLACK],
        gate_range=(25, 45),
        description="Axonometric 3D wireframe cube, CMYK rosettes (15/45/75 deg), CRT scanlines, stepped tilted type",
        slug="12-swiss-cyber-newwave",
        default_content=PosterContent(
            headline="DOES IT MAKE SENSE?",
            subhead="HYBRID IMAGERY // PACIFIC WAVE 1982",
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
        headline = content.get_slot("headline", "DOES IT MAKE SENSE?")
        subhead = content.get_slot("subhead", "HYBRID IMAGERY // PACIFIC WAVE 1982")
        dx, dy = P.drift

        # 1. Saturated Acid Chartreuse Angular Ground Plane
        plane_pts = [(100, 360), (1100, 240), (1040, 980), (80, 1060)]
        P.poly(plane_pts, INK_ACID_CHARTREUSE)

        # 2. Offset CMYK Halftone Rosettes (Duxt multi-angle screening)
        P.cmyk_rosette_field(
            180, 380, 1000, 920, pitch=18,
            cmyk_fn=lambda x, y: (
                0.5 + 0.4 * math.sin(x / 90),
                0.4 + 0.5 * math.cos(y / 90),
                0.6,
                0.2 + 0.2 * math.sin((x + y) / 120)
            ),
            c_ink=INK_LASER_CYAN,
            m_ink=INK_NEON_MAGENTA,
            y_ink=INK_ACID_CHARTREUSE,
            k_ink=INK_CYBER_BLACK,
        )

        # 3. 72-dpi Bitmapped Mac 128k Floating Isometric Wireframe Cube
        cube_front = [(420, 520), (740, 520), (740, 840), (420, 840)]
        cube_top = [(420, 520), (560, 400), (880, 400), (740, 520)]
        cube_side = [(740, 520), (880, 400), (880, 720), (740, 840)]

        P.poly(cube_top, INK_LASER_CYAN)
        P.poly(cube_side, INK_NEON_MAGENTA)
        P.poly(cube_front, INK_CYBER_BLACK)

        for p_pts in [cube_front, cube_top, cube_side]:
            for i in range(len(p_pts)):
                P.line([p_pts[i], p_pts[(i + 1) % len(p_pts)]], SUB_KROMEKOTE, w=2.0)

        # 4. CRT Video Scanlines with Horizontal Jitter (Duxt scanlines)
        P.scanlines(80, 240, 1100, 1060, INK_CYBER_BLACK, period=6, depth=0.35, aberration=3, jitter=1.5)

        # 5. Weingart Spaced Typographic Hierarchy & New Wave Punctuation
        P.text((90, 120), headline, "din_bold", 88, INK_CYBER_BLACK, tracking=8)
        P.text((95, 220), "CALARTS // HYBRID IMAGERY // BASEL NEW WAVE 1986", "mono_bold", 20, INK_NEON_MAGENTA, tracking=3)

        # Floating punctuation cluster
        P.text((1020, 110), "?", "din_bold", 96, INK_LASER_CYAN)
        P.text((80, 1100), "*** // 72 DPI BITMAP VIDEO FRAME", "mono_bold", 18, INK_CYBER_BLACK, tracking=4)

        # Lower Technical Column Band
        P.rect(80, 1150, 1120, 1260, INK_CYBER_BLACK)
        P.text((110, 1185), "APRIL GREIMAN & WOLFGANG WEINGART", "din_bold", 36, INK_ACID_CHARTREUSE, tracking=3)
        P.text((110, 1225), "SPACE COLLAGE OVERPRINT // SYNTHETIC KROMEKOTE SHEET", "mono", 14, INK_LASER_CYAN, tracking=2)

        P.text((80, 1310), "DIGITAL COLLISION: POSTSCRIPT FONTS + VIDEO STILLS + CMYK FILM OFFSET", "din", 16, INK_CYBER_BLACK, tracking=2)
        P.text((80, 1345), "PRINTED IN LOS ANGELES // ISSUE #76 PACIFIC WAVE ARCHIVE", "mono", 14, INK_NEON_MAGENTA, tracking=1)

        def zm(dm):
            dm.rectangle([80 * S, 110 * S, 1120 * S, 1360 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(25, 45))


