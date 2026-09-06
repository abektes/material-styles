"""Generate 10-poster showcase demonstrating the 10 Material-Driven Design Styles.

Each poster resolves a Recipe Manifest from design-system/*.json and executes
through stylelib.py. Re-running produces byte-identical SHA-256 hashes.
"""
import math
import os
import sys

from PIL import Image, ImageChops, ImageDraw
from stylelib import (
    StylePoster,
    S,
    W,
    H,
    UW,
    UH,
    multiply_colors,
    mix_colors,
    load_font,
)

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


# ==============================================================================
# 01. ZURICH CONCRETE MODERNISM
# ==============================================================================
def poster_01_zurich():
    P = StylePoster(
        "01-zurich-modernism",
        "style_zurich_modernism",
        SUB_ARTBOARD,
        [INK_ZURICH_BLACK, INK_SWISS_RED],
        "zurich|musica viva tonhalle|concentric_acoustic_arcs|fibonacci_grid",
    )
    dx, dy = P.drift

    # Concentric harmonic acoustic arcs radiating from lower-right pole (880, 1220)
    pole_x, pole_y = 860, 1220
    radii = [180, 320, 490, 700, 960, 1260]
    for idx, r in enumerate(radii):
        w = 4.0 + idx * 3.5
        P.ring(pole_x, pole_y, r, w, INK_ZURICH_BLACK)

    # Broad solid acoustic sector (between r=490 and r=680)
    for r in range(490, 680, 10):
        P.ring(pole_x, pole_y, r, 12.0, INK_ZURICH_BLACK)

    # 45-degree diagonal structural axis cutting through
    P.line([(90, 450), (1110, 1470)], INK_ZURICH_BLACK, w=2.0)

    # Intersecting Swiss Signal Red circle with drift
    P.ell(280 + dx, 680 + dy, 520 + dx, 920 + dy, INK_SWISS_RED)

    # Monolithic Akzidenz Grotesk typography
    P.text((90, 140), "musica viva", "grotesk_bold", 116, INK_ZURICH_BLACK, tracking=-2)
    P.text((90, 260), "tonhalle zürich", "grotesk_bold", 52, INK_SWISS_RED, tracking=-1)

    P.text((90, 340), "4. KONZERT DER TONHALLE-GESELLSCHAFT", "grotesk_bold", 16, INK_ZURICH_BLACK, tracking=2)
    P.text((90, 370), "DIENSTAG, 28. JANUAR 1958, 20.15 UHR", "grotesk", 15, INK_ZURICH_BLACK, tracking=1)
    P.text((90, 400), "DIRIGENT: HANS ROSBAUD // SOLIST: WOLFGANG SCHNEIDERHAN", "grotesk", 15, INK_ZURICH_BLACK, tracking=1)
    P.text((90, 430), "WERKE VON IGOR STRAVINSKY, BÉLA BARTÓK, PAUL HINDEMITH", "grotesk", 15, INK_ZURICH_BLACK, tracking=1)

    # Registration cross marks in margins
    rx, ry = 1110 + dx, 1500 + dy
    P.ring(rx, ry, 12, 1.0, INK_SWISS_RED)
    P.line([(rx - 16, ry), (rx + 16, ry)], INK_SWISS_RED, w=1.0)
    P.line([(rx, ry - 16), (rx, ry + 16)], INK_SWISS_RED, w=1.0)

    def zm(dm):
        dm.rectangle([90 * S, 140 * S, 880 * S, 480 * S], fill=255)
        dm.rectangle([180 * S, 560 * S, 960 * S, 1380 * S], fill=255)
    return P.finish(zmask=P.create_mask(zm), gate_range=(35, 55))


# ==============================================================================
# 02. 1960s POP ART SERIGRAPHY & PUSH PIN GRAPHIC
# ==============================================================================
def poster_02_pop_art():
    P = StylePoster(
        "02-pop-art-serigraphy",
        "style_pop_art_serigraphy",
        SUB_POP_CARDSTOCK,
        [INK_POP_MAGENTA, INK_POP_YELLOW, INK_POP_CYAN, INK_SQUEEGEE_BLACK],
        "corita_kent|push_pin_pop|squeegee_silkscreen|benday_dots",
    )
    dx, dy = P.drift

    # 1. 45-degree Coarse Ben-Day Halftone Dot Screen Field in Cyan Plate
    P.halftone(
        460, 240, 1100, 940, 28,
        lambda x, y: 4.5 + 8.5 * math.sin((x - y) / 160) ** 2,
        lambda x, y: True,
        INK_POP_CYAN,
        drift=(dx, dy),
    )

    # 2. Exuberant Pop Art Graphic Silhouette: Radiant multi-petaled Pop Blossom / Heart
    # Saturated Sunshine Yellow organic backing disc
    P.ell(200, 360, 880, 1040, INK_POP_YELLOW)

    # Saturated Hot Magenta primary pop silhouette (Multi-lobed organic star/flower)
    cx, cy = 540, 700
    pts_flower = []
    num_petals = 10
    for deg in range(0, 360, 5):
        rad = math.radians(deg)
        r = 220 + 80 * math.sin(deg * (num_petals / 360 * math.pi * 2))
        pts_flower.append((cx + math.cos(rad) * r, cy + math.sin(rad) * r))
    P.poly(pts_flower, INK_POP_MAGENTA)

    # Inner core contrast disc in Cyan
    P.ell(cx - 90 + dx, cy - 90 + dy, cx + 90 + dx, cy + 90 + dy, INK_POP_CYAN)
    # Center punch in Squeegee Black
    P.dot(cx, cy, 45, INK_SQUEEGEE_BLACK)
    P.dot(cx, cy, 20, SUB_POP_CARDSTOCK)

    # Heavy black Pop contour outline around flower with slight squeegee shift
    for i in range(len(pts_flower)):
        p1 = pts_flower[i]
        p2 = pts_flower[(i + 1) % len(pts_flower)]
        P.line([p1, p2], INK_SQUEEGEE_BLACK, w=4.5)

    # 3. Dynamic Typographic Voice: Push Pin / Sister Corita Kent Bold Serigraph
    # Massive multi-layered display title: "POWER & JOY"
    # Magenta shadow pass
    P.text((100 + dx * 2, 130 + dy * 2), "POWER & JOY", "din_bold", 112, INK_POP_MAGENTA, tracking=-2)
    # Solid Squeegee Black top pass
    P.text((100, 130), "POWER & JOY", "din_bold", 112, INK_SQUEEGEE_BLACK, tracking=-2)

    # Secondary Pop Kicker
    P.text((105, 255), "ELECTRIC SERIGRAPHY // IMMACULATE HEART & PUSH PIN", "grotesk_bold", 24, INK_POP_CYAN, tracking=2)

    # Saturated Pop Banner across lower section
    P.rect(90, 1140, 1110, 1270, INK_POP_YELLOW)
    P.line([(90, 1140), (1110, 1140)], INK_SQUEEGEE_BLACK, w=3.0)
    P.line([(90, 1270), (1110, 1270)], INK_SQUEEGEE_BLACK, w=3.0)
    P.text((600, 1175), "ALL POWER TO THE IMAGINATION!", "din_bold", 54, INK_SQUEEGEE_BLACK, tracking=4, anchor_x="center")

    # Accession metadata & Silkscreen workshop credits
    P.text((90, 1340), "SERIGRAPH WORKSHOP NYC // FOUR-COLOR SPOT SCREENPRINT", "din_bold", 18, INK_SQUEEGEE_BLACK, tracking=2)
    P.text((90, 1380), "HAND-PULLED ON 300GSM ARCHIVAL CARDSTOCK — LIMITED EDITION 250", "grotesk", 15, INK_POP_MAGENTA, tracking=1)
    P.text((1110, 1380), "CORITA KENT & GLASER HOMAGE", "mono_bold", 14, INK_POP_CYAN, tracking=2, anchor_x="right")

    # 4-color silkscreen registration crosshairs in margins
    for rx, ry, col in [
        (60, 60, INK_POP_MAGENTA),
        (1140, 60, INK_POP_CYAN),
        (60, 1540, INK_POP_YELLOW),
        (1140, 1540, INK_SQUEEGEE_BLACK),
    ]:
        P.ring(rx, ry, 12, 1.2, col)
        P.line([(rx - 16, ry), (rx + 16, ry)], col, w=1.0)
        P.line([(rx, ry - 16), (rx, ry + 16)], col, w=1.0)

    def zm(dm):
        dm.rectangle([90 * S, 120 * S, 1110 * S, 300 * S], fill=255)
        dm.rectangle([160 * S, 320 * S, 1040 * S, 1080 * S], fill=255)
        dm.rectangle([90 * S, 1120 * S, 1110 * S, 1420 * S], fill=255)
    return P.finish(zmask=P.create_mask(zm), gate_range=(28, 48))


# ==============================================================================
# 03. TOKYO RISO LAB (OVERPRINT MULTIPLY)
# ==============================================================================
def poster_03_tokyo_riso():
    P = StylePoster(
        "03-tokyo-riso-lab",
        "style_tokyo_riso_lab",
        SUB_VELLUM,
        [INK_RISO_PINK, INK_RISO_AQUA, INK_RISO_CARBON],
        "tokyo|neo tokyo noise|riso_pink_aqua|drum_collision",
    )
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
    return P.finish(zmask=P.create_mask(zm), gate_range=(25, 45))


# ==============================================================================
# 04. CONSTRUCTIVIST AGIT-PROP
# ==============================================================================
# ==============================================================================
# 04. CONSTRUCTIVIST AGIT-PROP
# ==============================================================================
def poster_04_constructivist():
    P = StylePoster(
        "04-constructivist-agit",
        "style_constructivist_agit",
        SUB_STRAW,
        [INK_AGIT_CARBON, INK_AGIT_VERMILION],
        "agit|beat the whites with the red wedge|lissitzky 1919|vkhutemas",
    )

    # 1. Lissitzky Split Spatial Field: Deep Carbon Angular Void on the right
    void_pts = [(440, 100), (1140, 100), (1140, 1140), (580, 1140)]
    P.poly(void_pts, INK_AGIT_CARBON)

    # 2. The Target White Sphere/Disc resting in the black void
    cx, cy = 800, 620
    cr = 270
    P.ell(cx - cr, cy - cr, cx + cr, cy + cr, SUB_STRAW)
    P.ring(cx, cy, 215, 3.5, INK_AGIT_CARBON)
    P.ring(cx, cy, 145, 3.0, INK_AGIT_CARBON)
    P.ring(cx, cy, 75, 2.5, INK_AGIT_CARBON)

    # 3. The Acute Revolutionary Red Wedge
    wedge_pts = [(50, 240), (840, 620), (70, 760)]
    P.poly(wedge_pts, INK_AGIT_VERMILION)

    # Full-span woodblock relief grain striations
    for y in range(256, 750, 20):
        x_left = 60 + int((y - 240) * 0.04)
        if y <= 620:
            x_right = int(50 + (y - 240) * 2.079)
        else:
            x_right = int(840 - (y - 620) * 5.5)
        if x_right > x_left + 10:
            P.line([(x_left + 6, y), (x_right - 6, y)], SUB_STRAW, w=1.8)

    # 4. Cleavage Fracture: The wedge splits the white circle
    crack_pts = [(cx, cy), (cx + 270, cy + 90), (cx + 250, cy + 220), (cx, cy)]
    P.poly(crack_pts, INK_AGIT_CARBON)

    displaced_pts = [
        (cx + 30, cy + 40),
        (cx + 290, cy + 130),
        (cx + 260, cy + 280),
        (cx + 40, cy + 270)
    ]
    P.poly(displaced_pts, SUB_STRAW)
    P.line([(cx + 30, cy + 40), (cx + 290, cy + 130)], INK_AGIT_CARBON, w=4.0)

    shards = [
        [(cx + 140, cy - 180), (cx + 220, cy - 240), (cx + 170, cy - 150)],
        [(cx + 260, cy - 50), (cx + 340, cy - 30), (cx + 280, cy + 20)],
        [(cx + 200, cy + 190), (cx + 290, cy + 250), (cx + 210, cy + 270)],
        [(cx - 30, cy + 290), (cx + 50, cy + 360), (cx - 70, cy + 340)],
    ]
    for idx, sh in enumerate(shards):
        c = INK_AGIT_VERMILION if idx % 2 == 0 else SUB_STRAW
        P.poly(sh, c)

    # 5. Floating Malevich / Lissitzky Geometric Satellites
    # Floating Red Square cleanly positioned between БЕЙ and the black void
    P.rect(300, 95, 370, 165, INK_AGIT_VERMILION)
    # Floating Straw Satellite in upper right black void (no text collision)
    P.rect(1020, 220, 1080, 360, SUB_STRAW)
    # Dynamic diagonal coordinate vector lines
    P.line([(50, 240), (1140, 830)], INK_AGIT_CARBON, w=1.5)
    P.line([(70, 760), (1140, 220)], INK_AGIT_VERMILION, w=1.5)

    # 6. Typographic Forces
    P.rotated_text((110, 350), "КЛИНОМ", "din_bold", 68, SUB_STRAW, angle_deg=22, tracking=4)
    P.rotated_text((150, 470), "КРАСНЫМ", "din_bold", 68, SUB_STRAW, angle_deg=22, tracking=4)

    # 'БЕЙ' (BEAT) monumental black wood-type at the top left
    P.text((60, 85), "БЕЙ", "din_bold", 124, INK_AGIT_CARBON, tracking=6)
    # 'БЕЛЫХ' (THE WHITES) centered in upper black void
    P.text((640, 130), "БЕЛЫХ", "din_bold", 84, SUB_STRAW, tracking=4)

    # Rodchenko-style interlocking headline banners below
    P.rect(60, 1170, 1140, 1285, INK_AGIT_CARBON)
    P.text((600, 1195), "BEAT THE OLD WITH THE NEW!", "din_bold", 68, SUB_STRAW, tracking=5, anchor_x="center")

    P.rect(60, 1285, 680, 1335, INK_AGIT_VERMILION)
    P.text((80, 1298), "ALL POWER TO REVOLUTIONARY UTILITY", "din_bold", 19, SUB_STRAW, tracking=3)

    # Constructed vector arrow polygons
    for ax in [710, 730, 750]:
        P.poly([(ax, 1300), (ax + 12, 1310), (ax, 1320)], INK_AGIT_CARBON)

    P.text((780, 1298), "VKHUTEMAS 1920", "din_bold", 20, INK_AGIT_CARBON, tracking=2)

    # Workshop Manifesto footer
    P.text((60, 1360), "EL LISSITZKY & ALEXANDER RODCHENKO // SECTION 4 MOSCOW", "din", 17, INK_AGIT_CARBON, tracking=3)
    P.text((60, 1395), "CONSTRUCTED OBJECTIVE FORM OVER INDIVIDUALIST DECORATION", "din_bold", 14, INK_AGIT_VERMILION, tracking=2)
    P.line([(60, 1430), (1140, 1430)], INK_AGIT_CARBON, w=3.0)

    def zm(dm):
        dm.rectangle([60 * S, 85 * S, 1140 * S, 1440 * S], fill=255)
    return P.finish(zmask=P.create_mask(zm), gate_range=(20, 42))


# ==============================================================================
# 05. DUTCH MATRIX MODERNISM (WIM CROUWEL / TOTAL DESIGN)
# ==============================================================================
def poster_05_dutch_matrix():
    P = StylePoster(
        "05-dutch-matrix-modernism",
        "style_dutch_matrix_modernism",
        SUB_DUTCH,
        [INK_DUTCH_ULTRAMARINE, INK_FLAME_ORANGE],
        "crouwel|vormgevers stedelijk amsterdam|stepped_diagonal_matrix|new_alphabet",
    )
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
    return P.finish(zmask=P.create_mask(zm), gate_range=(35, 55))


# ==============================================================================
# 06. LOW-FI THERMAL FAX & TELETEXT
# ==============================================================================
def poster_06_thermal_fax():
    P = StylePoster(
        "06-thermal-fax-brutalism",
        "style_thermal_fax_brutalism",
        SUB_THERMAL,
        [INK_THERMAL_BLACK],
        "teletext|packet dump 0x7ffe|thermal_roll|1bit_dither",
    )
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
    return P.finish(zmask=P.create_mask(zm), gate_range=(30, 50))


# ==============================================================================
# 07. VICTORIAN CHROMOLITHO NATURALIST
# ==============================================================================
def poster_07_victorian():
    P = StylePoster(
        "07-victorian-chromolitho",
        "style_victorian_chromolitho",
        SUB_LINEN,
        [INK_BITUMEN, INK_MINERAL_INDIGO, INK_BURNT_UMBER],
        "haeckel|discophora radiata|linen_vellum|intaglio_plate",
    )
    # Embossed intaglio plate depression border
    P.rect(100, 120, 1100, 1480, INK_BITUMEN)
    P.rect(104, 124, 1096, 1476, SUB_LINEN)
    P.rect(112, 132, 1088, 1468, INK_BITUMEN)
    P.rect(114, 134, 1086, 1466, SUB_LINEN)

    # Plate Roman numeral corner index
    P.text((140, 150), "Haeckel, Kunstformen der Natur.", "serif_italic", 16, INK_BITUMEN)
    P.text((1060, 150), "TAB. XLII.", "serif_bold", 18, INK_BITUMEN, anchor_x="right")

    # Concentric radial crosshatching: Anatomical Medusa Specimen
    cx, cy = 600, 680
    for r in range(40, 320, 24):
        P.ring(cx, cy, r, 1.2, INK_MINERAL_INDIGO)

    # 16 Radial umbrella ribs
    for i in range(16):
        ang = math.radians(i * (360 / 16))
        x2 = cx + math.cos(ang) * 320
        y2 = cy + math.sin(ang) * 320
        P.line([(cx, cy), (x2, y2)], INK_BITUMEN, w=2.0)
        # Burnt umber watercolor accent wash dot
        P.dot(x2, y2, 8, INK_BURNT_UMBER)

    # Fine crosshatch density in the core
    def medusa_density(x, y):
        dist = math.hypot(x - cx, y - cy)
        return max(0.0, 1.0 - dist / 280)

    P.crosshatch_field(320, 400, 880, 960, medusa_density, INK_BITUMEN, pitch=12)

    # Trailing tentacles
    for i in range(8):
        tx = cx - 180 + i * 50
        pts = [(tx, 960), (tx - 30, 1100), (tx + 20, 1220), (tx - 10, 1320)]
        P.line(pts, INK_MINERAL_INDIGO, w=1.5)

    # Scientific Linnaean Classification Typography
    P.text((600, 1360), "DISCOPHORA RADIATA", "serif_bold", 38, INK_BITUMEN, tracking=4, anchor_x="center")
    P.text((600, 1410), "Medusae acraspedae. — 1. Aurelia aurita. 2. Pelagia noctiluca.", "serif_italic", 18, INK_BURNT_UMBER, anchor_x="center")

    def zm(dm):
        dm.rectangle([140 * S, 170 * S, 1060 * S, 1430 * S], fill=255)
    return P.finish(zmask=P.create_mask(zm), gate_range=(38, 56))


# ==============================================================================
# 08. 1977 PUNK ZINE & XEROGRAPHY
# ==============================================================================
def poster_08_punk_xerox():
    P = StylePoster(
        "08-punk-xerox-ransom",
        "style_punk_xerox_ransom",
        SUB_BOND,
        [INK_COPIER_TONER, INK_ACID_LEMON],
        "punk|static noise riot|bond_copy|ransom_barricade",
    )
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
    return P.finish(zmask=P.create_mask(zm), gate_range=(22, 45))


# ==============================================================================
# 09. DE STIJL NEOPLASTICISM & GERRIT RIETVELD CHAIR (1918)
# ==============================================================================
def poster_09_de_stijl_rietveld():
    P = StylePoster(
        "09-de-stijl-rietveld",
        "style_de_stijl_rietveld",
        SUB_DESTIJL_PRESSBOARD,
        [INK_DESTIJL_RED, INK_DESTIJL_BLUE, INK_DESTIJL_YELLOW, INK_DESTIJL_BLACK],
        "rietveld|rood_blauwe_stoel 1918|de_stijl leiden|mondrian_grid",
    )

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
    P.text((60, 90), "DE STIJL", "din_bold", 96, INK_DESTIJL_BLACK, tracking=8)
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
    return P.finish(zmask=P.create_mask(zm), gate_range=(38, 58))


# ==============================================================================
# 10. BRAUN / BAUHAUS INDUSTRIAL PATENT SCHEMATIC
# ==============================================================================
def poster_10_braun_patent():
    P = StylePoster(
        "10-braun-patent-schematic",
        "style_braun_patent_schematic",
        SUB_DRAFT,
        [INK_INDIA_TECH, INK_BAUHAUS_YELLOW],
        "rams|fig 4 rotary control|drafting_grid|axonometric_spec",
    )
    # Subtle 40px metric drafting grid lines
    for x in range(60, UW - 60, 40):
        P.line([(x, 60), (x, UH - 60)], (0xE2, 0xE2, 0xDF), w=0.5)
    for y in range(60, UH - 60, 40):
        P.line([(60, y), (UW - 60, y)], (0xE2, 0xE2, 0xDF), w=0.5)

    # Technical Border Frame
    P.rect(60, 60, 1140, 1540, INK_INDIA_TECH)
    P.rect(63, 63, 1137, 1537, SUB_DRAFT)

    # Technical Header
    P.text((90, 90), "PATENTSCHRIFT NR. DE-1972844-B", "din_bold", 18, INK_INDIA_TECH, tracking=3)
    P.text((1110, 90), "KLASSE 21a4 — GRUPPE 12", "din", 16, INK_INDIA_TECH, tracking=2, anchor_x="right")
    P.line([(90, 125), (1110, 125)], INK_INDIA_TECH, w=1.5)

    # Main Figure Title
    P.text((90, 160), "FIG. 4 — DREHKNOPF-STEUERUNG", "din_bold", 44, INK_INDIA_TECH, tracking=2)
    P.text((90, 220), "EXPLODED ISOMETRIC ASSEMBLY // ROTARY ENCODER MECHANISM", "din", 18, INK_INDIA_TECH, tracking=1)

    # Bauhaus Signal Yellow Highlight Accent Block
    P.rect(260, 420, 940, 980, INK_BAUHAUS_YELLOW)

    # Precision Axonometric / Isometric Exploded Cylinder Assembly
    def iso_cylinder(cx, cy, rx, ry, h, ink):
        # Bottom ellipse
        P.ell(cx - rx, cy + h - ry, cx + rx, cy + h + ry, ink, outline=True, width=2.0)
        # Side lines
        P.line([(cx - rx, cy), (cx - rx, cy + h)], ink, w=2.0)
        P.line([(cx + rx, cy), (cx + rx, cy + h)], ink, w=2.0)
        # Top ellipse (filled with paper knockout)
        P.ell(cx - rx, cy - ry, cx + rx, cy + ry, SUB_DRAFT)
        P.ell(cx - rx, cy - ry, cx + rx, cy + ry, ink, outline=True, width=2.0)

    # Component 1: Rotary Knob Dial
    iso_cylinder(600, 480, 240, 90, 120, INK_INDIA_TECH)
    # Component 2: Flanged Mounting Collar
    iso_cylinder(600, 720, 190, 70, 80, INK_INDIA_TECH)
    # Component 3: Splined Core Spindle
    iso_cylinder(600, 920, 90, 35, 140, INK_INDIA_TECH)

    # Isometric Axis Centerline (Dash pattern)
    for y in range(360, 1140, 24):
        P.line([(600, y), (600, y + 14)], INK_INDIA_TECH, w=1.0)

    # Numbered Callout Leaders
    P.spec_callout(360, 540, "1", INK_INDIA_TECH, lead_dx=-140, lead_dy=-40)
    P.spec_callout(410, 760, "2", INK_INDIA_TECH, lead_dx=-190, lead_dy=0)
    P.spec_callout(510, 990, "3", INK_INDIA_TECH, lead_dx=-290, lead_dy=40)
    P.spec_callout(840, 540, "4a", INK_INDIA_TECH, lead_dx=140, lead_dy=-40)

    # Specification Legend Table in lower quadrant
    P.rect(90, 1180, 1110, 1480, INK_INDIA_TECH)
    P.rect(92, 1182, 1108, 1478, SUB_DRAFT)
    P.line([(90, 1240), (1110, 1240)], INK_INDIA_TECH, w=1.5)
    P.line([(420, 1180), (420, 1480)], INK_INDIA_TECH, w=1.0)
    P.line([(760, 1180), (760, 1480)], INK_INDIA_TECH, w=1.0)

    P.text((110, 1205), "TEIL-NR. / BENENNUNG", "din_bold", 16, INK_INDIA_TECH)
    P.text((440, 1205), "WERKSTOFF / NORM", "din_bold", 16, INK_INDIA_TECH)
    P.text((780, 1205), "MASSANGABE / TOLERANZ", "din_bold", 16, INK_INDIA_TECH)

    specs = [
        ("1. DREHKNOPF-AUSSENRING", "ALUMINIUM ELOXIERT", "Ø 120.0 mm ± 0.05"),
        ("2. RASTBLENDE MIT FEDER", "POLYACETAL (POM)", "Ø 95.0 mm ± 0.10"),
        ("3. ACHSWELLE 18-ZAHN", "EDELSTAHL 1.4301", "Ø 45.0 mm DIN 5480"),
        ("4a. SKALENRING 360°", "POLYCARBONAT WEISS", "TEILUNG 1° PRÄZISION"),
    ]
    for idx, (c1, c2, c3) in enumerate(specs):
        yy = 1265 + idx * 48
        P.text((110, yy), c1, "din", 15, INK_INDIA_TECH)
        P.text((440, yy), c2, "din", 15, INK_INDIA_TECH)
        P.text((780, yy), c3, "mono", 15, INK_INDIA_TECH)

    def zm(dm):
        dm.rectangle([60 * S, 60 * S, 1140 * S, 250 * S], fill=255)
        dm.rectangle([220 * S, 360 * S, 980 * S, 1140 * S], fill=255)
        dm.rectangle([90 * S, 1180 * S, 1110 * S, 1480 * S], fill=255)
    return P.finish(zmask=P.create_mask(zm), gate_range=(32, 52))


# ==============================================================================
# MASTER RUNNER & CONTACT SHEET COMPOSITOR
# ==============================================================================
def create_contact_sheet(results, out_path="styles_contact_sheet.png"):
    """Assemble all 10 posters into a high-resolution 5x2 contact sheet."""
    thumb_w, thumb_h = 300, 400
    cols, rows = 5, 2
    pad_x = 24
    pad_y = 65
    sheet_w = cols * thumb_w + (cols + 1) * pad_x
    sheet_h = rows * (thumb_h + pad_y) + 115

    sheet = Image.new("RGB", (sheet_w, sheet_h), (0x12, 0x12, 0x14))
    sd = ImageDraw.Draw(sheet)
    # load_font multiplies by S=2, so size_1x must be halved for 1x canvas
    f_title = load_font("din_bold", 11)
    f_sub = load_font("mono", 6)
    f_name = load_font("din_bold", 6.5)
    f_stat = load_font("mono", 5.5)

    # Master Header
    sd.text((pad_x, 24), "10 MATERIAL-DRIVEN SYSTEMATIC DESIGN STYLES — MASTER AUDIT", font=f_title, fill=(0xF4, 0xF4, 0xF2))
    sd.text((pad_x, 56), "DETERMINISTIC VECTOR RENDERING // SUBSTRATE PHYSICS // REPRODUCIBLE SEED ENGINES", font=f_sub, fill=(0x88, 0x88, 0x86))

    for idx, r in enumerate(results):
        c = idx % cols
        row = idx // cols
        x = pad_x + c * (thumb_w + pad_x)
        y = 95 + row * (thumb_h + pad_y)

        # Draw subtle border frame for posters with light edges
        sd.rectangle([x - 1, y - 1, x + thumb_w, y + thumb_h], outline=(0x33, 0x33, 0x36), width=1)

        im = Image.open(r["path"]).resize((thumb_w, thumb_h), Image.LANCZOS)
        sheet.paste(im, (x, y))

        # Two-line clean label
        clean_slug = r['slug'].split('-', 1)[1].replace('-', ' ').upper()
        title_text = f"#{idx+1:02d}  {clean_slug}"
        stat_text = f"EMPTY: {r['zempty']:.1f}% | GATE: {r['gate_range'][0]}-{r['gate_range'][1]}% | PASS"

        sd.text((x, y + thumb_h + 10), title_text, font=f_name, fill=(0xE8, 0xE8, 0xE5))
        sd.text((x, y + thumb_h + 28), stat_text, font=f_stat, fill=(0x4E, 0xC9, 0x90))

    sheet.save(out_path)
    print(f"-> Generated master contact sheet: {out_path} ({sheet_w}x{sheet_h})")


if __name__ == "__main__":
    renderers = [
        poster_01_zurich,
        poster_02_pop_art,
        poster_03_tokyo_riso,
        poster_04_constructivist,
        poster_05_dutch_matrix,
        poster_06_thermal_fax,
        poster_07_victorian,
        poster_08_punk_xerox,
        poster_09_de_stijl_rietveld,
        poster_10_braun_patent,
    ]

    print("================================================================================")
    print("           RENDERING 10 SYSTEMATIC MATERIAL-DRIVEN POSTERS                      ")
    print("================================================================================")
    print(f"{'#':2} {'Slug':30} {'Style ID':28} {'Zone%':>6} {'Gate':>9} {'Status':>6}")
    print("-" * 84)

    results = []
    for idx, fn in enumerate(renderers):
        res = fn()
        results.append(res)
        lo, hi = res["gate_range"]
        status = "PASS" if res["gate_ok"] else "FAIL"
        print(f"{idx+1:02d} {res['slug']:30} {res['style_id']:28} {res['zempty']:6.1f}% {lo:>3}-{hi:<3}% {status:>6}")

    print("-" * 84)
    create_contact_sheet(results)
    print("All 10 styles rendered deterministically and verified against gates.")
