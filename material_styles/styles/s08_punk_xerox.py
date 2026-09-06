"""Style 08: 1977 Punk Zine & Xerography (Jamie Reid (Sex Pistols), 1977 London/NYC Fanzines)."""
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




class PunkXeroxRansomStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_punk_xerox_ransom",
        number=8,
        name="1977 Punk Zine & Xerography",
        lineage="Jamie Reid (Sex Pistols), 1977 London/NYC Fanzines",
        substrate_hex="#EDECE8",
        substrate_rgb=SUB_BOND,
        inks=[INK_COPIER_TONER, INK_ACID_LEMON],
        gate_range=(22, 45),
        description="High-contrast blown-out photocopy, torn newsprint ransom blocks, toner drum streaks",
        slug="08-punk-xerox-ransom",
        default_content=PosterContent(
            headline="ANARCHY IN THE U.K.",
            subhead="LIVE AT THE 100 CLUB // OXFORD ST",
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
        headline = content.get_slot("headline", "ANARCHY IN THE U.K.")
        subhead = content.get_slot("subhead", "LIVE AT THE 100 CLUB // OXFORD ST")
        # Day-Glo fluorescent yellow backing sticker band
        P.rect(80, 180, 1120, 360, INK_ACID_LEMON)

        # Ransom Cutout Headline: Individual tilted paper letter tiles!
        P.ransom_word((100, 210), "STATIC", 110, INK_COPIER_TONER, SUB_BOND, jitter_deg=5)
        P.ransom_word((120, 420), "NOISE", 120, INK_COPIER_TONER, SUB_BOND, jitter_deg=6)
        P.ransom_word((620, 420), "RIOT", 120, INK_ACID_LEMON, INK_COPIER_TONER, jitter_deg=6)

        # Blown-out high-contrast electrostatic toner portrait mass
        P.rect(100, 640, 1100, 1160, INK_COPIER_TONER)
        # Sharp cutout rips in toner mass exposing paper
        P.poly([(140, 660), (480, 680), (320, 940)], SUB_BOND)
        P.poly([(720, 720), (1060, 680), (980, 1100)], SUB_BOND)
        P.ell(440, 780, 760, 1100, SUB_BOND)
        P.ell(480, 820, 720, 1060, INK_COPIER_TONER)

        # Photocopier drum longitudinal scratch (Toner flaw)
        P.line([(340, 20), (340, 1580)], INK_COPIER_TONER, w=1.0)
        P.line([(342, 40), (342, 1560)], INK_COPIER_TONER, w=1.0)

        # Spliced typewritten manifesto columns
        P.rect(100, 1220, 1100, 1460, INK_COPIER_TONER)
        P.text((130, 1250), "NO FUTURE FANZINE // ISSUE NO. 07 // PRICE 20P", "mono_bold", 22, INK_ACID_LEMON, tracking=3)
        P.text((130, 1300), "LIVE AT THE VORTEX CLUB — FRIDAY NIGHT 10PM", "mono", 18, SUB_BOND, tracking=2)
        P.text((130, 1340), "FEATURING: THE SCREAMING CLOCK + RAW POWER DUO", "mono", 18, SUB_BOND, tracking=2)
        P.text((130, 1390), "DISTRIBUTED HAND-TO-HAND ONLY // DO IT YOURSELF", "mono_bold", 18, INK_ACID_LEMON, tracking=3)

        def zm(dm):
            dm.rectangle([80 * S, 180 * S, 1120 * S, 1460 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(22, 45))


