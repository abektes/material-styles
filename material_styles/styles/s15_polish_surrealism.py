"""Style 15: Polish Poster School Surrealism (Jan Lenica (Wozzeck 1964), Henryk Tomaszewski)."""
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




class PolishSurrealismStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_polish_surrealism",
        number=15,
        name="Polish Poster School Surrealism",
        lineage="Jan Lenica (Wozzeck 1964), Henryk Tomaszewski",
        substrate_hex="#EBE3D0",
        substrate_rgb=SUB_POLISH_OFFSET,
        inks=[INK_POISON_OLIVE, INK_CRIMSON_RUST, INK_GOUACHE_CHARCOAL],
        gate_range=(28, 48),
        description="Visceral biological paper-cut silhouette, concentric hypnotic color rings, expressive brush lettering",
        slug="15-polish-surrealism",
        default_content=PosterContent(
            headline="WOZZECK",
            subhead="TEATR WIELKI W WARSZAWIE",
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
        headline = content.get_slot("headline", "WOZZECK")
        subhead = content.get_slot("subhead", "TEATR WIELKI W WARSZAWIE")
        dx, dy = P.drift

        # 1. Expressive Poison Olive Biological Contour Background
        P.ell(180, 260, 1020, 1100, INK_POISON_OLIVE)

        # 2. Concentric Grotesque Anatomical Rings (Jan Lenica Wozzeck motif)
        for r in [380, 320, 260, 200, 140, 80]:
            col = INK_CRIMSON_RUST if (r // 60) % 2 == 0 else INK_GOUACHE_CHARCOAL
            P.ring(600, 680, r, 24.0, col)

        # Center screaming core
        P.ell(520, 600, 680, 760, INK_GOUACHE_CHARCOAL)
        P.ell(550, 630, 650, 730, SUB_POLISH_OFFSET)
        P.dot(600, 680, 25, INK_CRIMSON_RUST)

        # Hand-carved organic relief lines across the surrealist head
        head_poly = [
            (220, 1060), (280, 840), (220, 640), (320, 420), (520, 280),
            (680, 280), (880, 420), (980, 640), (920, 840), (980, 1060)
        ]
        for i in range(len(head_poly)):
            P.line([head_poly[i], head_poly[(i + 1) % len(head_poly)]], INK_GOUACHE_CHARCOAL, w=6.0)

        # 3. Raw Painterly Brush Display Lettering
        P.text((600, 110), headline, "din_bold", 124, INK_GOUACHE_CHARCOAL, tracking=4, anchor_x="center")
        P.text((600, 220), "OPERA W 3 AKTACH // ALBAN BERG", "din_bold", 26, INK_CRIMSON_RUST, tracking=3, anchor_x="center")

        # Lower Theatrical Imprint
        P.rect(120, 1160, 1080, 1270, INK_GOUACHE_CHARCOAL)
        P.text((600, 1185), subhead, "din_bold", 48, SUB_POLISH_OFFSET, tracking=5, anchor_x="center")

        P.text((120, 1310), "REŻYSERIA: JAN LENICA // KIEROWNICTWO MUZYCZNE: BOHDAN WODICZKO", "din_bold", 17, INK_GOUACHE_CHARCOAL, tracking=1)
        P.text((120, 1345), "POLISH POSTER SCHOOL ARCHIVE // WARSZAWA 1964 // WYDAWNICTWO ARTYSTYCZNO-GRAFICZNE", "grotesk", 14, INK_POISON_OLIVE, tracking=1)
        P.line([(120, 1380), (1080, 1380)], INK_CRIMSON_RUST, w=2.5)

        def zm(dm):
            dm.rectangle([120 * S, 110 * S, 1080 * S, 1380 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(28, 48))


