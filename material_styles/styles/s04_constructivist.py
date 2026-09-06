"""Style 04: Constructivist Agit-Prop (Alexander Rodchenko (Lengiz 1924), El Lissitzky (VKHUTEMAS))."""
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




class ConstructivistAgitStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_constructivist_agit",
        number=4,
        name="Constructivist Agit-Prop",
        lineage="Alexander Rodchenko (Lengiz 1924), El Lissitzky (VKHUTEMAS)",
        substrate_hex="#EAE3D2",
        substrate_rgb=SUB_STRAW,
        inks=[INK_AGIT_CARBON, INK_AGIT_VERMILION],
        gate_range=(20, 42),
        description="Shouting megaphone silhouette, linocut relief striations, perspective Cyrillic wood-type",
        slug="04-constructivist-agit",
        default_content=PosterContent(
            headline="КНИГИ",
            subhead="ПО ВСЕМ ОТРАСЛЯМ ЗНАНИЯ",
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
        headline = content.get_slot("headline", "КНИГИ")
        subhead = content.get_slot("subhead", "ПО ВСЕМ ОТРАСЛЯМ ЗНАНИЯ")

        # 1. Shouting Face Silhouette at Left (homage to Lilya Brik in Lengiz poster)
        shouter_pts = [
            (60, 1120), (60, 620), (140, 580), (190, 540), (240, 510),
            (280, 540), (270, 610), (220, 640),
            # Mouth open wide shouting into cone
            (250, 670), (180, 710), (250, 750),
            # Jaw and neck
            (220, 790), (180, 840), (190, 940), (220, 1040), (240, 1120)
        ]
        P.poly(shouter_pts, INK_AGIT_CARBON)
        # Woodblock relief gouges on shouter
        P.linocut_relief(shouter_pts, INK_AGIT_CARBON, SUB_STRAW, num_gouges=6)

        # 2. Diagonal Sonic Megaphone Expansion Cone (Radiating from mouth across page)
        # Primary Vermilion Red outer expansion cone
        cone_vermilion = [(250, 670), (1140, 140), (1140, 1080), (250, 750)]
        P.poly(cone_vermilion, INK_AGIT_VERMILION)

        # Secondary Carbon Black inner soundwave sector
        cone_black = [(340, 680), (1140, 360), (1140, 880), (340, 740)]
        P.poly(cone_black, INK_AGIT_CARBON)

        # Central straw soundwave core
        cone_straw = [(480, 690), (1140, 520), (1140, 720), (480, 730)]
        P.poly(cone_straw, SUB_STRAW)

        # 3. Concentric Soundwave Arc Ribs across the megaphone
        for r in [220, 380, 560, 760, 960]:
            P.ring(250, 710, r, 3.5, SUB_STRAW)

        # 4. Diagonal Structural Girders & Tension Cables
        P.line([(60, 240), (1140, 140)], INK_AGIT_CARBON, w=3.0)
        P.line([(250, 670), (1140, 140)], INK_AGIT_CARBON, w=4.5)
        P.line([(250, 750), (1140, 1080)], INK_AGIT_CARBON, w=4.5)
        P.line([(60, 1120), (1140, 1080)], INK_AGIT_CARBON, w=3.0)

        # 5. Monumental Perspective Cyrillic Wood-Type
        # 'КНИГИ' (BOOKS) bursting from the mouth of the cone
        P.rotated_text((380, 580), headline, "din_bold", 120, SUB_STRAW, angle_deg=-20, tracking=6)

        # 'ПО ВСЕМ ОТРАСЛЯМ' (ON ALL BRANCHES)
        P.rotated_text((480, 480), "ПО ВСЕМ ОТРАСЛЯМ", "din_bold", 38, INK_AGIT_CARBON, angle_deg=-20, tracking=4)

        # 'ЗНАНИЯ' (OF KNOWLEDGE) monumental vermilion callout in upper void
        P.text((580, 80), "ЗНАНИЯ!", "din_bold", 96, INK_AGIT_VERMILION, tracking=6)

        # 6. Rodchenko Industrial Barricades at Bottom
        P.rect(60, 1160, 1140, 1270, INK_AGIT_CARBON)
        P.text((600, 1185), "ГОСИЗДАТ // ЛЕНГИЗ 1924", "din_bold", 62, SUB_STRAW, tracking=6, anchor_x="center")

        P.rect(60, 1270, 740, 1320, INK_AGIT_VERMILION)
        P.text((80, 1285), "ПРОИЗВОДСТВЕННОЕ ИСКУССТВО // РОДЧЕНКО", "din_bold", 18, SUB_STRAW, tracking=3)

        for ax in [770, 790, 810]:
            P.poly([(ax, 1285), (ax + 12, 1295), (ax, 1305)], INK_AGIT_CARBON)

        P.text((840, 1285), "ВХУТЕМАС 1924", "din_bold", 19, INK_AGIT_CARBON, tracking=2)

        P.text((60, 1350), "LILYA BRIK & ALEXANDER RODCHENKO // BOOKS ON ALL SUBJECTS", "din", 16, INK_AGIT_CARBON, tracking=2)
        P.text((60, 1385), "AGITATIONAL STATE PUBLISHING HOUSE MOSCOW // LENINGRAD", "din_bold", 14, INK_AGIT_VERMILION, tracking=2)
        P.line([(60, 1420), (1140, 1420)], INK_AGIT_CARBON, w=3.0)

        def zm(dm):
            dm.rectangle([60 * S, 80 * S, 1140 * S, 1420 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(20, 42))


