"""Style 06: Low-Fi Thermal Fax & Teletext (Subculture Teletext, POS Thermal Roll)."""
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




class ThermalFaxBrutalismStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_thermal_fax_brutalism",
        number=6,
        name="Low-Fi Thermal Fax & Teletext",
        lineage="Subculture Teletext, POS Thermal Roll",
        substrate_hex="#ECE8DC",
        substrate_rgb=SUB_THERMAL,
        inks=[INK_THERMAL_BLACK],
        gate_range=(30, 50),
        description="Pure 1-bit Bayer matrix dithering, OCR-A monospace, telemetry data burst, burnout line",
        slug="06-thermal-fax-brutalism",
        default_content=PosterContent(
            headline="TERMINAL NODE 0x7F",
            subhead="PACKET TELEMETRY RECEPTION STREAM",
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
        headline = content.get_slot("headline", "TERMINAL NODE 0x7F")
        subhead = content.get_slot("subhead", "PACKET TELEMETRY RECEPTION STREAM")
        # Serrated top tear-edge
        for x in range(0, UW, 16):
            P.poly([(x, 0), (x + 8, 12), (x + 16, 0)], INK_THERMAL_BLACK)

        # Monospace Terminal Header
        P.rect(60, 60, 1140, 110, INK_THERMAL_BLACK)
        P.text((80, 75), "BBS TELETEXT NODE // SYSTEM TELEMETRY DUMP // 2400 BAUD", "mono_bold", 18, SUB_THERMAL, tracking=2)

        # ASCII Box Border
        P.line([(60, 130), (1140, 130)], INK_THERMAL_BLACK, w=2.0)
        P.line([(60, 1500), (1140, 1500)], INK_THERMAL_BLACK, w=2.0)

        # Primary Display Headline
        P.text((80, 160), "BUFFER OVERRUN", "mono_bold", 84, INK_THERMAL_BLACK, tracking=4)
        P.text((80, 270), "STATUS: 0x7FFE FAULT IN MEMORY STACK", "mono", 22, INK_THERMAL_BLACK, tracking=2)

        # Pure 1-bit Bayer Algorithmic Matrix Dithering Field
        def grad_field(x, y):
            # Radial wave pattern dithered strictly into 1-bit binary dots
            dist = math.hypot(x - 600, y - 680)
            val = 0.5 + 0.48 * math.sin(dist / 32)
            return max(0.0, min(1.0, val))

        P.dither_1bit_field(80, 360, 1120, 1000, grad_field, INK_THERMAL_BLACK, step=4)

        # Telemetry hex data rows
        hex_lines = [
            "0000: 4E 45 4F 5F 54 4F 4B 59 4F 20 54 45 52 4D 49 4E  NEO_TOKYO TERMIN",
            "0010: 41 4C 20 56 45 52 20 34 2E 30 20 42 55 49 4C 44  AL VER 4.0 BUILD",
            "0020: 78 37 46 46 45 20 4F 56 45 52 46 4C 4F 57 20 4F  x7FFE OVERFLOW O",
            "0030: 4B 20 41 4C 4C 20 43 4C 45 41 52 20 4E 4F 20 57  K ALL CLEAR NO W",
        ]
        for idx, line in enumerate(hex_lines):
            P.text((80, 1050 + idx * 36), line, "mono", 18, INK_THERMAL_BLACK, tracking=1)

        # Thermal Print Head Burnout Line (1px continuous white dropout at x=780)
        P.rect(780, 40, 782, 1540, SUB_THERMAL)

        # Receipt bottom cut footer
        P.text((80, 1450), "=== END OF TRANSMISSION ===", "mono_bold", 18, INK_THERMAL_BLACK, tracking=6)

        def zm(dm):
            dm.rectangle([60 * S, 60 * S, 1140 * S, 120 * S], fill=255)
            dm.rectangle([80 * S, 150 * S, 1100 * S, 320 * S], fill=255)
            dm.rectangle([80 * S, 360 * S, 1120 * S, 1000 * S], fill=255)
            dm.rectangle([80 * S, 1040 * S, 1120 * S, 1220 * S], fill=255)
            dm.rectangle([80 * S, 1430 * S, 1120 * S, 1480 * S], fill=255)
        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=(30, 50))


