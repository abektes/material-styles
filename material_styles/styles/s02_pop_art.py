"""Style 02: 1960s Pop Art Serigraphy (Sister Corita Kent, Andy Warhol, Milton Glaser (Push Pin 1968))."""
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




class PopArtSerigraphyStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_pop_art_serigraphy",
        number=2,
        name="1960s Pop Art Serigraphy",
        lineage="Sister Corita Kent, Andy Warhol, Milton Glaser (Push Pin 1968)",
        substrate_hex="#FAF8F5",
        substrate_rgb=SUB_POP_CARDSTOCK,
        inks=[INK_POP_MAGENTA, INK_POP_YELLOW, INK_POP_CYAN, INK_SQUEEGEE_BLACK],
        gate_range=(28, 48),
        description="Multi-angle Ben-Day screens (15/75 deg), double-exposed muse silhouette, drop-shadow wood-type",
        slug="02-pop-art-serigraphy",
        default_content=PosterContent(
            headline="LOVE & REVOLT",
            subhead="DAMN EVERYTHING BUT THE CIRCUS!",
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
        headline = content.get_slot("headline", "LOVE & REVOLT")
        subhead = content.get_slot("subhead", "DAMN EVERYTHING BUT THE CIRCUS!")
        dx, dy = P.drift

        # 1. Radiant Yellow Screen Block (Saturated Pop ground)
        P.rect(120, 240, 1080, 1080, INK_POP_YELLOW)

        # 2. Multi-Angle Ben-Day Screens (Duxt screening engine: Cyan 15 deg, Magenta 75 deg)
        # Cyan plate screened at 15 degrees
        P.rotated_halftone(
            140, 260, 1060, 1060, 22, 15,
            lambda x, y: 0.15 + 0.70 * math.sin((x + y) / 180) ** 2,
            INK_POP_CYAN,
            shape="circle",
            drift=(dx, dy),
        )
        # Magenta plate screened at 75 degrees
        P.rotated_halftone(
            140, 260, 1060, 1060, 22, 75,
            lambda x, y: 0.20 + 0.65 * math.cos((x - y) / 210) ** 2,
            INK_POP_MAGENTA,
            shape="circle",
            drift=(-dx, -dy),
        )

        # 3. High-Contrast Pop Portrait / Profile Silhouette in Squeegee Black
        head_profile = [
            (380, 1080), (380, 880), (410, 840), (420, 780), (460, 740),
            (510, 710), (560, 690), (540, 640), (580, 600), (620, 580),
            (660, 550), (700, 510), (730, 460), (770, 480), (810, 520),
            (840, 580), (850, 660), (840, 740), (800, 820), (780, 880),
            (800, 960), (820, 1080)
        ]
        # Squeegee offset shadow in Cyan
        P.poly([(p[0] + dx * 3, p[1] + dy * 3) for p in head_profile], INK_POP_CYAN)
        # Primary Squeegee Black silhouette
        P.poly(head_profile, INK_SQUEEGEE_BLACK)

        # Electric Pop Magenta Lips accent
        lips_pts = [(620, 740), (670, 725), (710, 740), (670, 765)]
        P.poly(lips_pts, INK_POP_MAGENTA)
        P.line(lips_pts, INK_SQUEEGEE_BLACK, w=2.5)

        # Eye accent with Pop Cyan iris
        P.ell(650, 610, 710, 650, SUB_POP_CARDSTOCK)
        P.dot(680, 630, 14, INK_POP_CYAN)
        P.dot(680, 630, 6, INK_SQUEEGEE_BLACK)

        # 4. Squeegee ink drags along edge of screen frame
        for sy in range(240, 1080, 45):
            P.line([(120, sy), (120 + ((sy * 13) % 40), sy)], INK_SQUEEGEE_BLACK, w=3.0)
            P.line([(1080 - ((sy * 17) % 35), sy), (1080, sy)], INK_POP_MAGENTA, w=2.5)

        # 5. Monumental Corita Kent / Push Pin Typography
        # Massive title: headline
        P.text((120 + dx * 2, 110 + dy * 2), headline, "din_bold", 112, INK_POP_MAGENTA, tracking=-2)
        P.text((120, 110), headline, "din_bold", 112, INK_SQUEEGEE_BLACK, tracking=-2)

        # Kicker banner
        P.text((125, 215), "ELECTRIC SERIGRAPHY // IMMACULATE HEART & PUSH PIN NYC", "grotesk_bold", 21, INK_POP_CYAN, tracking=2)

        # Lower proclaim banner
        P.rect(120, 1140, 1080, 1260, INK_POP_YELLOW)
        P.line([(120, 1140), (1080, 1140)], INK_SQUEEGEE_BLACK, w=3.0)
        P.line([(120, 1260), (1080, 1260)], INK_SQUEEGEE_BLACK, w=3.0)
        P.text((600, 1175), subhead, "din_bold", 48, INK_SQUEEGEE_BLACK, tracking=4, anchor_x="center")

        # Accession metadata & Silkscreen workshop credits
        P.text((120, 1330), "CORITA KENT & ANDY WARHOL HOMAGE // SCREENPRINT ON 300GSM BRISTOL", "din_bold", 17, INK_SQUEEGEE_BLACK, tracking=2)
        P.text((120, 1370), "LIMITED EDITION 250 // HAND-PULLED SQUEEGEE OFFSET", "grotesk", 15, INK_POP_MAGENTA, tracking=1)
        P.text((1080, 1370), "SERIGRAPH LAB NYC", "mono_bold", 14, INK_POP_CYAN, tracking=2, anchor_x="right")

        # Corner registration marks
        for rx, ry, col in [(60, 60, INK_POP_MAGENTA), (1140, 60, INK_POP_CYAN), (60, 1540, INK_POP_YELLOW), (1140, 1540, INK_SQUEEGEE_BLACK)]:
            P.ring(rx, ry, 12, 1.2, col)
            P.line([(rx - 16, ry), (rx + 16, ry)], col, w=1.0)
            P.line([(rx, ry - 16), (rx, ry + 16)], col, w=1.0)

        def zm(dm):
            dm.rectangle([120 * S, 110 * S, 1080 * S, 240 * S], fill=255)
            dm.rectangle([120 * S, 240 * S, 1080 * S, 1080 * S], fill=255)
            dm.rectangle([120 * S, 1140 * S, 1080 * S, 1400 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(28, 48))


