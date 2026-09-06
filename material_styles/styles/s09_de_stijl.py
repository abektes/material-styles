"""Style 09: De Stijl Neoplasticism (Gerrit Rietveld (Rood-blauwe stoel 1918), Theo van Doesburg)."""
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




class DeStijlRietveldStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_de_stijl_rietveld",
        number=9,
        name="De Stijl Neoplasticism",
        lineage="Gerrit Rietveld (Rood-blauwe stoel 1918), Theo van Doesburg",
        substrate_hex="#F5F3EB",
        substrate_rgb=SUB_DESTIJL_PRESSBOARD,
        inks=[INK_DESTIJL_RED, INK_DESTIJL_BLUE, INK_DESTIJL_YELLOW, INK_DESTIJL_BLACK],
        gate_range=(38, 58),
        description="Axonometric 3D Rietveld chair projection with primary yellow end-caps, Mondrian Cartesian planes",
        slug="09-de-stijl-rietveld",
        default_content=PosterContent(
            headline="DE STIJL",
            subhead="MAANDBLAD VOOR NIEUWE KUNST",
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
        headline = content.get_slot("headline", "DE STIJL")
        subhead = content.get_slot("subhead", "MAANDBLAD VOOR NIEUWE KUNST")

        # 1. Asymmetrical Orthogonal Mondrian Cartesian Grid (Heavy black structural lines)
        # Vertical grid lines
        P.line([(180, 60), (180, 1540)], INK_DESTIJL_BLACK, w=6.0)
        P.line([(960, 60), (960, 1540)], INK_DESTIJL_BLACK, w=5.0)
        # Horizontal grid lines
        P.line([(60, 270), (1140, 270)], INK_DESTIJL_BLACK, w=6.0)
        P.line([(60, 1120), (1140, 1120)], INK_DESTIJL_BLACK, w=5.0)
        P.line([(180, 1360), (1140, 1360)], INK_DESTIJL_BLACK, w=4.0)

        # Pure primary Mondrian color blocks locked into grid perimeters
        # Top-right Primary Chrome Yellow block
        P.rect(960, 60, 1140, 270, INK_DESTIJL_YELLOW)
        # Bottom-left Primary Cobalt Blue vertical bar
        P.rect(60, 1120, 180, 1540, INK_DESTIJL_BLUE)
        # Small top-left Primary Cadmium Red square
        P.rect(120, 210, 180, 270, INK_DESTIJL_RED)

        # 2. Axonometric 3D Spatial Projection of the Gerrit Rietveld Red and Blue Chair (1918)
        ox, oy = 560, 680

        # A. RECLINING BACKREST PLANE: Monumental tilted plane in Primary Cadmium Red
        back_pts = [
            (ox - 120, oy - 290),
            (ox + 160, oy - 290),
            (ox + 80, oy + 120),
            (ox - 200, oy + 120),
        ]
        P.poly(back_pts, INK_DESTIJL_RED)
        for i in range(4):
            P.line([back_pts[i], back_pts[(i + 1) % 4]], INK_DESTIJL_BLACK, w=3.0)

        # B. CANTILEVERED HORIZONTAL SEAT PLANE in Primary Cobalt Blue
        seat_pts = [
            (ox - 160, oy - 20),
            (ox + 180, oy - 20),
            (ox + 120, oy + 130),
            (ox - 220, oy + 130),
        ]
        P.poly(seat_pts, INK_DESTIJL_BLUE)
        for i in range(4):
            P.line([seat_pts[i], seat_pts[(i + 1) % 4]], INK_DESTIJL_BLACK, w=3.0)

        # C. BLACK STRUCTURAL TIMBER RAILS & SIGNATURE YELLOW END-CAPS
        rails = [
            # Left front vertical leg
            ((ox - 190, oy + 260), (ox - 190, oy - 60)),
            # Right front vertical leg
            ((ox + 150, oy + 260), (ox + 150, oy - 60)),
            # Left rear vertical leg
            ((ox - 130, oy + 180), (ox - 130, oy - 180)),
            # Right rear vertical leg
            ((ox + 210, oy + 180), (ox + 210, oy - 180)),
            # Left horizontal armrest rail
            ((ox - 250, oy - 60), (ox - 90, oy - 60)),
            # Right horizontal armrest rail
            ((ox + 90, oy - 60), (ox + 270, oy - 60)),
            # Seat support transverse crossbars
            ((ox - 230, oy + 110), (ox + 230, oy + 110)),
            ((ox - 210, oy + 40), (ox + 210, oy + 40)),
            # Base floor runners
            ((ox - 230, oy + 240), (ox - 70, oy + 240)),
            ((ox + 70, oy + 240), (ox + 230, oy + 240)),
        ]

        for p1, p2 in rails:
            # Draw thick black timber lath
            P.line([p1, p2], INK_DESTIJL_BLACK, w=7.0)
            # Rietveld's signature detail: radiant Primary Yellow square end-caps!
            for pt in [p1, p2]:
                hx, hy = pt
                P.rect(hx - 6, hy - 6, hx + 6, hy + 6, INK_DESTIJL_YELLOW)
                P.rect(hx - 6, hy - 6, hx + 6, hy + 6, INK_DESTIJL_BLACK, outline=True, width=1.0)

        # 3. Theo van Doesburg Constructed Typographic Voice (Strictly Orthogonal)
        # De Stijl monumental masthead
        P.text((60, 90), headline, "din_bold", 96, INK_DESTIJL_BLACK, tracking=8)
        P.text((60, 205), "MAANDBLAD VOOR NIEUWE KUNST, WETENSCHAP EN KULTUUR", "din", 16, INK_DESTIJL_BLACK, tracking=3)
        P.text((60, 235), "REDACTIE: THEO VAN DOESBURG // LEIDEN — JAARGANG 2", "din_bold", 15, INK_DESTIJL_RED, tracking=2)

        # Lower architectural specification column
        P.text((220, 1160), "GERRIT TH. RIETVELD", "din_bold", 42, INK_DESTIJL_BLACK, tracking=4)
        P.text((220, 1220), "ROOD-BLAUWE STOEL (1918)", "din_bold", 28, INK_DESTIJL_BLUE, tracking=2)
        P.text((220, 1270), "BEUKENHOUT // PRIMAIRE LAK // AFMETINGEN: 86 x 66 x 83 CM", "mono", 15, INK_DESTIJL_BLACK, tracking=1)
        P.text((220, 1305), "RUIMTELIJKE BEELDING IN PURE CONSTRUCTIE EN ELEMENTAIRE KLEUR", "din", 15, INK_DESTIJL_BLACK, tracking=1)

        # Vertical 90-degree rotated margin text along the left coordinate strip
        P.vtext((70, 480), "UTRECHT — LEIDEN — ANTWERPEN — WEIMAR", "din_bold", 15, INK_DESTIJL_BLACK)

        # Spec sheet numbering
        P.text((1110, 1390), "CAT. NO. 1918/01", "mono_bold", 15, INK_DESTIJL_BLACK, tracking=2, anchor_x="right")
        P.text((1110, 1420), "NEOPLASTICISME", "din_bold", 16, INK_DESTIJL_RED, tracking=3, anchor_x="right")

        def zm(dm):
            dm.rectangle([60 * S, 90 * S, 1140 * S, 270 * S], fill=255)
            dm.rectangle([250 * S, 340 * S, 870 * S, 1020 * S], fill=255)
            dm.rectangle([60 * S, 1120 * S, 1140 * S, 1480 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(38, 58))


