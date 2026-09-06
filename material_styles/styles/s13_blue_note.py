"""Style 13: 1950s Blue Note Hard Bop (Reid Miles, Francis Wolff (Blue Note Records 1958))."""
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




class BlueNoteHardBopStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_blue_note_hardbop",
        number=13,
        name="1950s Blue Note Hard Bop",
        lineage="Reid Miles, Francis Wolff (Blue Note Records 1958)",
        substrate_hex="#F7F5EE",
        substrate_rgb=SUB_ALBUM_JACKET,
        inks=[INK_VELVET_BLACK, INK_BLUE_NOTE_OCHRE],
        gate_range=(20, 42),
        description="Francis Wolff 45-degree photographic halftone saxophone crop, monumental condensed wood-type",
        slug="13-blue-note-hardbop",
        default_content=PosterContent(
            headline="SONNY ROLLINS",
            subhead="NEWK'S TIME // BLUE NOTE 4003",
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
        headline = content.get_slot("headline", "SONNY ROLLINS")
        subhead = content.get_slot("subhead", "NEWK'S TIME // BLUE NOTE 4003")
        dx, dy = P.drift

        # 1. Saturated Blue Note Ochre Header Block
        P.rect(80, 80, 1120, 290, INK_BLUE_NOTE_OCHRE)

        # 2. Severe Asymmetric Crop: Tenor Saxophone & Jazz Musician Silhouette on Right Side
        sax_body = [
            (640, 480), (740, 420), (840, 420), (960, 520), (1080, 680),
            (1120, 820), (1120, 1520), (560, 1520), (560, 1280), (620, 980),
            (600, 780), (640, 580)
        ]
        P.poly(sax_body, INK_VELVET_BLACK)

        # 45-degree photographic halftone grain field across the bell of the horn
        P.rotated_halftone(
            620, 600, 1100, 1300, 18, 45,
            lambda x, y: 0.15 + 0.65 * math.sin((x - y) / 120) ** 2,
            INK_VELVET_BLACK,
            shape="circle",
            drift=(dx, dy),
        )

        # Metallic highlights on horn
        P.line([(680, 680), (880, 860)], SUB_ALBUM_JACKET, w=3.5)
        P.line([(740, 780), (1020, 980)], INK_BLUE_NOTE_OCHRE, w=2.5)

        # 3. Typography
        P.text((110, 110), headline, "grotesk_bold", 96, INK_VELVET_BLACK, tracking=-2)
        P.text((115, 230), "WYNTON KELLY / DOUG WATKINS / PHILLY JOE JONES", "din_bold", 21, SUB_ALBUM_JACKET, tracking=2)

        P.text((110, 360), "NEWK'S", "din_bold", 136, INK_VELVET_BLACK, tracking=-3)
        P.text((110, 500), "TIME", "din_bold", 136, INK_VELVET_BLACK, tracking=-3)

        P.rect(880, 105, 1090, 175, INK_VELVET_BLACK)
        P.text((905, 118), "BLUE NOTE", "din_bold", 20, SUB_ALBUM_JACKET, tracking=2)
        P.text((905, 145), "BLP 4003", "din_bold", 20, INK_BLUE_NOTE_OCHRE, tracking=3)

        P.text((110, 680), "TUNE UP", "din_bold", 20, INK_BLUE_NOTE_OCHRE, tracking=2)
        P.text((110, 715), "ASIATIC RAES", "din_bold", 20, INK_VELVET_BLACK, tracking=2)
        P.text((110, 750), "WONDERFUL! WONDERFUL!", "din_bold", 20, INK_VELVET_BLACK, tracking=2)
        P.text((110, 785), "THE SURREY WITH THE FRINGE ON TOP", "din_bold", 20, INK_VELVET_BLACK, tracking=2)

        P.text((110, 1460), "BLUE NOTE RECORDS // 47 WEST 63RD ST. // NEW YORK 23", "din_bold", 17, INK_VELVET_BLACK, tracking=2)
        P.text((1090, 1460), "HIGH FIDELITY", "mono_bold", 15, SUB_ALBUM_JACKET, tracking=2, anchor_x="right")

        def zm(dm):
            dm.rectangle([80 * S, 80 * S, 1120 * S, 1480 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(20, 42))


