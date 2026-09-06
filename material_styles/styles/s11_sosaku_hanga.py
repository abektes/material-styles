"""Style 11: Japanese Sōsaku-Hanga Woodcut (Shikō Munakata, Kōshirō Onchi (Sōsaku-Hanga 1950s))."""
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




class SosakuHangaStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_sosaku_hanga",
        number=11,
        name="Japanese Sōsaku-Hanga Woodcut",
        lineage="Shikō Munakata, Kōshirō Onchi (Sōsaku-Hanga 1950s)",
        substrate_hex="#F3EFE6",
        substrate_rgb=SUB_WASHI,
        inks=[INK_SUMI, INK_CINNABAR, INK_AOMORI_INDIGO],
        gate_range=(30, 50),
        description="Hand-carved linocut/woodcut relief crane, baren rubbing ink starvation, carved hanko seals",
        slug="11-sosaku-hanga-woodcut",
        default_content=PosterContent(
            headline="SŌSAKU-HANGA",
            subhead="CREATIVE PRINTS // CRANE AT DAWN",
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
        headline = content.get_slot("headline", "SŌSAKU-HANGA")
        subhead = content.get_slot("subhead", "CREATIVE PRINTS // CRANE AT DAWN")
        dx, dy = P.drift

        # 1. Radiant Cinnabar Vermilion Solar Disc in background
        P.ell(320, 240, 880, 800, INK_CINNABAR)

        # 2. Dynamic Soaring Crane / Spirit Bird Woodblock Silhouette
        bird_body = [
            (600, 480), (680, 420), (740, 380), (820, 360), (780, 420),
            (720, 480), (840, 520), (960, 560), (880, 600), (760, 620),
            (700, 680), (720, 760), (660, 840), (580, 920), (520, 860),
            (480, 760), (420, 680), (320, 640), (220, 620), (340, 560),
            (460, 540), (520, 500)
        ]
        P.poly(bird_body, INK_SUMI)
        # Hand-carved linocut relief feather gouges
        P.linocut_relief(bird_body, INK_SUMI, SUB_WASHI, num_gouges=10)

        # Indigo pine bough silhouette in foreground
        pine_pts = [
            (120, 1080), (240, 980), (380, 940), (460, 980), (340, 1020),
            (260, 1050), (120, 1080)
        ]
        P.poly(pine_pts, INK_AOMORI_INDIGO)

        # 3. Baren Circular Impression Textures (Uneven woodblock hand-rubbing)
        for br in [140, 280, 420, 560]:
            P.ring(600 + dx, 520 + dy, br, 1.5, INK_SUMI)

        # 4. Red Artist Hanko Seals (Cinnabar Vermilion Stamping)
        P.rect(940, 960, 1040, 1060, INK_CINNABAR)
        P.rect(948, 968, 1032, 1052, SUB_WASHI)
        P.line([(960, 985), (1020, 985)], INK_CINNABAR, w=2.5)
        P.line([(960, 1035), (1020, 1035)], INK_CINNABAR, w=2.5)
        P.line([(990, 975), (990, 1045)], INK_CINNABAR, w=2.5)
        P.text((962, 995), "MUNA", "din_bold", 18, INK_CINNABAR, tracking=2)

        P.ell(955, 1080, 1025, 1140, INK_CINNABAR)
        P.text((968, 1098), "KATA", "mono_bold", 14, SUB_WASHI, tracking=1)

        # 5. Woodcut Calligraphic Display Typography
        P.text((120, 110), headline, "din_bold", 104, INK_SUMI, tracking=4)
        P.text((125, 220), "AOMORI WOODCUT ARCHIVE // SHIKŌ MUNAKATA & ONCHI", "din_bold", 21, INK_CINNABAR, tracking=3)

        # Woodcut vertical index strip
        P.rect(120, 360, 180, 680, INK_SUMI)
        P.text((135, 380), "P", "din_bold", 32, SUB_WASHI)
        P.text((135, 430), "R", "din_bold", 32, SUB_WASHI)
        P.text((135, 480), "I", "din_bold", 32, SUB_WASHI)
        P.text((135, 530), "N", "din_bold", 32, SUB_WASHI)
        P.text((135, 580), "T", "din_bold", 32, SUB_WASHI)
        P.text((135, 630), "S", "din_bold", 32, SUB_WASHI)

        # Lower Exhibition Imprint
        P.line([(120, 1200), (1080, 1200)], INK_SUMI, w=3.0)
        P.text((120, 1230), "SHIKŌ MUNAKATA & KŌSHIRŌ ONCHI // WOODCUT PRINTS 1935-1958", "din_bold", 22, INK_SUMI, tracking=2)
        P.text((120, 1270), "HAND-PULLED ON RAW KOZO FIBER ECHIZEN WASHI WITH SUMI AND CINNABAR", "grotesk", 15, INK_AOMORI_INDIGO, tracking=1)
        P.text((120, 1310), "NATIONAL MUSEUM OF MODERN ART TOKYO // FOLK CRAFT PAVILION", "grotesk", 15, INK_SUMI, tracking=1)
        P.line([(120, 1350), (1080, 1350)], INK_CINNABAR, w=1.5)

        def zm(dm):
            dm.rectangle([120 * S, 120 * S, 1080 * S, 1350 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(30, 50))


