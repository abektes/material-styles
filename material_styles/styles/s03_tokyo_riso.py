"""Style 03: Tokyo Riso Lab (Japanese Under-Press, Multichrome Risograph)."""
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




class TokyoRisoLabStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_tokyo_riso_lab",
        number=3,
        name="Tokyo Riso Lab",
        lineage="Japanese Under-Press, Multichrome Risograph",
        substrate_hex="#FCFAF2",
        substrate_rgb=SUB_VELLUM,
        inks=[INK_RISO_PINK, INK_RISO_AQUA, INK_RISO_CARBON],
        gate_range=(25, 45),
        description="60-lpi drum screens, subtractive optical multiply overprints, 2mm registration drift",
        slug="03-tokyo-riso-lab",
        default_content=PosterContent(
            headline="SHIBUYA UNDERGROUND",
            subhead="EXPERIMENTAL NOISE & MODULAR ELECTRONICS",
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
        headline = content.get_slot("headline", "SHIBUYA UNDERGROUND")
        subhead = content.get_slot("subhead", "EXPERIMENTAL NOISE & MODULAR ELECTRONICS")
        # Mask 1: Fluorescent Pink plate (large geometric arch + circle)
        def draw_p1(dm):
            dm.rectangle([140 * S, 320 * S, 720 * S, 1180 * S], fill=255)
            dm.ellipse([260 * S, 200 * S, 600 * S, 540 * S], fill=255)
        mask_pink = P.create_mask(draw_p1)

        # Mask 2: Aqua plate with intentional 2.5mm registration drift (shifted diagonal circle + bar)
        dx, dy = P.drift
        def draw_p2(dm):
            dm.ellipse([440 * S, 480 * S, 1020 * S, 1060 * S], fill=255)
            dm.rectangle([200 * S, 960 * S, 1060 * S, 1120 * S], fill=255)
        mask_aqua = P.create_mask(draw_p2)

        # Physical subtractive optical multiply: Pink + Aqua = Deep Violet Overprint!
        P.overprint_multiply(mask_pink, INK_RISO_PINK, mask_aqua, INK_RISO_AQUA, ox2=dx, oy2=dy)

        # 60-lpi coarse drum halftone pattern on upper right quadrant
        P.halftone(
            660, 160, 1080, 480, 24,
            lambda x, y: 3.5 + 8.0 * math.sin((x + y) / 140) ** 2,
            lambda x, y: True,
            INK_RISO_PINK,
            drift=(dx, dy),
        )

        # Black typography and bilingual stamp lines (Flat carbon plate)
        P.text((120, 140), "SHINJUKU UNDERGROUND SOUND EXPERIMENT", "din", 16, INK_RISO_CARBON, tracking=4)
        P.text((120, 180), "NEO TOKYO NOISE", "din_bold", 96, INK_RISO_CARBON, tracking=-1)
        P.vtext((1060, 320), "新宿音響実験室 — 限定版", "grotesk_bold", 24, INK_RISO_CARBON)

        # Riso workshop accession stamp
        P.rect(120, 1380, 420, 1460, INK_RISO_CARBON)
        P.text((140, 1405), "RISO LAB DRUM 03 / VOL. 18", "mono_bold", 18, SUB_VELLUM, tracking=1)
        P.text((1080, 1430), "EDITION: 120 / 300 COPIES", "mono", 15, INK_RISO_CARBON, tracking=2, anchor_x="right")

        def zm(dm):
            dm.rectangle([120 * S, 140 * S, 1080 * S, 1460 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(25, 45))


