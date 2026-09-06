"""Style 05: Dutch Matrix Modernism (Wim Crouwel (Total Design, Stedelijk Catalogus 1968))."""
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




class DutchMatrixModernismStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_dutch_matrix_modernism",
        number=5,
        name="Dutch Matrix Modernism",
        lineage="Wim Crouwel (Total Design, Stedelijk Catalogus 1968)",
        substrate_hex="#F4F5F7",
        substrate_rgb=SUB_DUTCH,
        inks=[INK_DUTCH_ULTRAMARINE, INK_FLAME_ORANGE],
        gate_range=(35, 55),
        description="57-degree isometric stepped matrix, constructed modular block sans, 3-column metadata",
        slug="05-dutch-matrix-modernism",
        default_content=PosterContent(
            headline="VORMGEVERS",
            subhead="STEDELIJK MUSEUM AMSTERDAM",
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
        headline = content.get_slot("headline", "VORMGEVERS")
        subhead = content.get_slot("subhead", "STEDELIJK MUSEUM AMSTERDAM")
        dx, dy = P.drift

        # 1. Monolithic constructed display title (Crouwel lowercase / grotesk_bold)
        P.text((90, 130), "vormgevers", "grotesk_bold", 118, INK_DUTCH_ULTRAMARINE, tracking=-3)
        P.text((90, 255), "stedelijk museum amsterdam", "grotesk_bold", 42, INK_FLAME_ORANGE, tracking=-1)

        # 2. Strict Isometric 57-degree / 45-degree Stepped Diagonal Matrix Staircase
        # Main ultramarine stepped diagonal block mass
        step_w = 420
        step_h = 44
        start_x, start_y = 120, 360
        num_steps = 12

        for i in range(num_steps):
            sx = start_x + i * 42
            sy = start_y + i * 48
            # Stepped bar in cobalt ultramarine
            P.rect(sx, sy, sx + step_w, sy + step_h, INK_DUTCH_ULTRAMARINE)
            # Inner fine matrix rule
            if i % 2 == 0:
                P.line([(sx + 10, sy + step_h // 2), (sx + step_w - 10, sy + step_h // 2)], SUB_DUTCH, w=1.0)

        # Intersecting Flame Orange modular accent block (Counter-step)
        orange_x = start_x + 5 * 42 + 240 + dx
        orange_y = start_y + 3 * 48 + dy
        P.rect(orange_x, orange_y, orange_x + 220, orange_y + 260, INK_FLAME_ORANGE)

        # Knockout numeral / matrix code inside orange block
        P.text((orange_x + 20, orange_y + 30), "68", "grotesk_bold", 96, SUB_DUTCH, tracking=-2)
        P.text((orange_x + 24, orange_y + 160), "CATALOGUS 448", "din_bold", 16, SUB_DUTCH, tracking=2)
        P.text((orange_x + 24, orange_y + 195), "TOTAL DESIGN", "din", 14, SUB_DUTCH, tracking=2)

        # 3. Coordinate System Matrix Grid Ticks (16x24 grid indicators)
        for col in range(6):
            gx = 680 + col * 75
            P.line([(gx, 360), (gx, 372)], INK_DUTCH_ULTRAMARINE, w=1.0)
            P.text((gx - 4, 380), f"{col+1:02d}", "mono", 11, INK_DUTCH_ULTRAMARINE)

        # Matrix dot array in open coordinate field
        for r in range(4):
            for c in range(5):
                P.dot(680 + c * 75 + 10, 440 + r * 50, 2.5, INK_DUTCH_ULTRAMARINE)

        # 4. Tabular Metadata Columns (Rigid 3-column architectural layout)
        col1_x = 90
        col2_x = 440
        col3_x = 790
        base_y = 1080

        # Column 1: Exhibition dates & venues
        P.text((col1_x, base_y), "DATA EN LOCATIE", "din_bold", 15, INK_FLAME_ORANGE, tracking=2)
        P.text((col1_x, base_y + 32), "19 OKTOBER — 24 NOVEMBER 1968", "grotesk_bold", 18, INK_DUTCH_ULTRAMARINE, tracking=0)
        P.text((col1_x, base_y + 64), "PAVILJOEN VOOR VORMGEVING", "grotesk", 15, INK_DUTCH_ULTRAMARINE, tracking=0)
        P.text((col1_x, base_y + 90), "PAULUS POTTERSTRAAT 13, AMSTERDAM", "grotesk", 14, INK_DUTCH_ULTRAMARINE, tracking=0)

        # Column 2: Participants & curation
        P.text((col2_x, base_y), "DEELNEMENDE ONTWERPERS", "din_bold", 15, INK_FLAME_ORANGE, tracking=2)
        P.text((col2_x, base_y + 32), "FRISO KRAMER // BENNO PREMSELA", "grotesk_bold", 18, INK_DUTCH_ULTRAMARINE, tracking=0)
        P.text((col2_x, base_y + 64), "WIM CROUWEL // KHO LIANG IE", "grotesk", 15, INK_DUTCH_ULTRAMARINE, tracking=0)
        P.text((col2_x, base_y + 90), "JAN VAN DER VOO // TOTAL DESIGN", "grotesk", 14, INK_DUTCH_ULTRAMARINE, tracking=0)

        # Column 3: Systematic print specifications
        P.text((col3_x, base_y), "SPECIFICATIES / COÖRDINATEN", "din_bold", 15, INK_FLAME_ORANGE, tracking=2)
        P.text((col3_x, base_y + 32), "GRID: 57° ISOMETRISCH MATRIX", "mono_bold", 16, INK_DUTCH_ULTRAMARINE, tracking=1)
        P.text((col3_x, base_y + 64), "DRUK: OFFSET ROTATIE LITHO", "mono", 14, INK_DUTCH_ULTRAMARINE, tracking=1)
        P.text((col3_x, base_y + 90), "KLEUR: PMS 072 C + 021 C", "mono", 14, INK_DUTCH_ULTRAMARINE, tracking=1)

        # 5. Lithographic Step Wedge Calibration Bar at Bottom
        wedge_y = 1440
        for b in range(16):
            bx = 90 + b * 45
            c = INK_DUTCH_ULTRAMARINE if b % 2 == 0 else INK_FLAME_ORANGE
            P.rect(bx, wedge_y, bx + 40, wedge_y + 12, c)
        P.text((90, 1468), "STEDELIJK MUSEUM DRUKWERK // SYSTEEM WIM CROUWEL // TOTAL DESIGN 1968", "mono", 12, INK_DUTCH_ULTRAMARINE, tracking=1)

        def zm(dm):
            dm.rectangle([90 * S, 130 * S, 1110 * S, 330 * S], fill=255)
            dm.rectangle([120 * S, 360 * S, 1020 * S, 980 * S], fill=255)
            dm.rectangle([90 * S, 1060 * S, 1110 * S, 1490 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(35, 55))


