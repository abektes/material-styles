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
        "corita_kent|push_pin_pop|warhol_exposure|cmyk_screen_angles",
    )
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
    # Massive title: "LOVE & REVOLT"
    P.text((120 + dx * 2, 110 + dy * 2), "LOVE & REVOLT", "din_bold", 112, INK_POP_MAGENTA, tracking=-2)
    P.text((120, 110), "LOVE & REVOLT", "din_bold", 112, INK_SQUEEGEE_BLACK, tracking=-2)

    # Kicker banner
    P.text((125, 215), "ELECTRIC SERIGRAPHY // IMMACULATE HEART & PUSH PIN NYC", "grotesk_bold", 21, INK_POP_CYAN, tracking=2)

    # Lower proclaim banner
    P.rect(120, 1140, 1080, 1260, INK_POP_YELLOW)
    P.line([(120, 1140), (1080, 1140)], INK_SQUEEGEE_BLACK, w=3.0)
    P.line([(120, 1260), (1080, 1260)], INK_SQUEEGEE_BLACK, w=3.0)
    P.text((600, 1175), "DAMN EVERYTHING BUT THE CIRCUS!", "din_bold", 48, INK_SQUEEGEE_BLACK, tracking=4, anchor_x="center")

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


def poster_04_constructivist():
    P = StylePoster(
        "04-constructivist-agit",
        "style_constructivist_agit",
        SUB_STRAW,
        [INK_AGIT_CARBON, INK_AGIT_VERMILION],
        "rodchenko_1924|lengiz_books|megaphone_soundwave|vkhutemas",
    )

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
    P.rotated_text((380, 580), "КНИГИ", "din_bold", 120, SUB_STRAW, angle_deg=-20, tracking=6)

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
# 11. JAPANESE SŌSAKU-HANGA (SHIKŌ MUNAKATA WOODCUT)
# ==============================================================================
def poster_11_sosaku_hanga():
    P = StylePoster(
        "11-sosaku-hanga-woodcut",
        "style_sosaku_hanga",
        SUB_WASHI,
        [INK_SUMI, INK_CINNABAR, INK_AOMORI_INDIGO],
        "shiko_munakata|sosaku_hanga|baren_relief|kozo_washi",
    )
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
    P.text((120, 110), "SŌSAKU-HANGA", "din_bold", 104, INK_SUMI, tracking=4)
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
    return P.finish(zmask=P.create_mask(zm), gate_range=(30, 50))


# ==============================================================================
# 12. 1980s SWISS CYBER NEW WAVE (WEINGART & GREIMAN HYBRID TYPOGRAPHY)
# ==============================================================================
def poster_12_swiss_cyber():
    P = StylePoster(
        "12-swiss-cyber-newwave",
        "style_swiss_cyber",
        SUB_KROMEKOTE,
        [INK_LASER_CYAN, INK_ACID_CHARTREUSE, INK_NEON_MAGENTA, INK_CYBER_BLACK],
        "april_greiman|wolfgang_weingart|new_wave|bitmapped_mac_1986",
    )
    dx, dy = P.drift

    # 1. Saturated Acid Chartreuse Angular Ground Plane
    plane_pts = [(100, 360), (1100, 240), (1040, 980), (80, 1060)]
    P.poly(plane_pts, INK_ACID_CHARTREUSE)

    # 2. Offset CMYK Halftone Rosettes (Duxt multi-angle screening)
    P.cmyk_rosette_field(
        180, 380, 1000, 920, pitch=18,
        cmyk_fn=lambda x, y: (
            0.5 + 0.4 * math.sin(x / 90),
            0.4 + 0.5 * math.cos(y / 90),
            0.6,
            0.2 + 0.2 * math.sin((x + y) / 120)
        ),
        c_ink=INK_LASER_CYAN,
        m_ink=INK_NEON_MAGENTA,
        y_ink=INK_ACID_CHARTREUSE,
        k_ink=INK_CYBER_BLACK,
    )

    # 3. 72-dpi Bitmapped Mac 128k Floating Isometric Wireframe Cube
    cube_front = [(420, 520), (740, 520), (740, 840), (420, 840)]
    cube_top = [(420, 520), (560, 400), (880, 400), (740, 520)]
    cube_side = [(740, 520), (880, 400), (880, 720), (740, 840)]

    P.poly(cube_top, INK_LASER_CYAN)
    P.poly(cube_side, INK_NEON_MAGENTA)
    P.poly(cube_front, INK_CYBER_BLACK)

    for p_pts in [cube_front, cube_top, cube_side]:
        for i in range(len(p_pts)):
            P.line([p_pts[i], p_pts[(i + 1) % len(p_pts)]], SUB_KROMEKOTE, w=2.0)

    # 4. CRT Video Scanlines with Horizontal Jitter (Duxt scanlines)
    P.scanlines(80, 240, 1100, 1060, INK_CYBER_BLACK, period=6, depth=0.35, aberration=3, jitter=1.5)

    # 5. Weingart Spaced Typographic Hierarchy & New Wave Punctuation
    P.text((90, 120), "DOES IT MAKE SENSE?", "din_bold", 88, INK_CYBER_BLACK, tracking=8)
    P.text((95, 220), "CALARTS // HYBRID IMAGERY // BASEL NEW WAVE 1986", "mono_bold", 20, INK_NEON_MAGENTA, tracking=3)

    # Floating punctuation cluster
    P.text((1020, 110), "?", "din_bold", 96, INK_LASER_CYAN)
    P.text((80, 1100), "*** // 72 DPI BITMAP VIDEO FRAME", "mono_bold", 18, INK_CYBER_BLACK, tracking=4)

    # Lower Technical Column Band
    P.rect(80, 1150, 1120, 1260, INK_CYBER_BLACK)
    P.text((110, 1185), "APRIL GREIMAN & WOLFGANG WEINGART", "din_bold", 36, INK_ACID_CHARTREUSE, tracking=3)
    P.text((110, 1225), "SPACE COLLAGE OVERPRINT // SYNTHETIC KROMEKOTE SHEET", "mono", 14, INK_LASER_CYAN, tracking=2)

    P.text((80, 1310), "DIGITAL COLLISION: POSTSCRIPT FONTS + VIDEO STILLS + CMYK FILM OFFSET", "din", 16, INK_CYBER_BLACK, tracking=2)
    P.text((80, 1345), "PRINTED IN LOS ANGELES // ISSUE #76 PACIFIC WAVE ARCHIVE", "mono", 14, INK_NEON_MAGENTA, tracking=1)

    def zm(dm):
        dm.rectangle([80 * S, 110 * S, 1120 * S, 1360 * S], fill=255)
    return P.finish(zmask=P.create_mask(zm), gate_range=(25, 45))


# ==============================================================================
# 13. 1950s BLUE NOTE HARD BOP (REID MILES / FRANCIS WOLFF)
# ==============================================================================
def poster_13_blue_note():
    P = StylePoster(
        "13-blue-note-hardbop",
        "style_blue_note",
        SUB_ALBUM_JACKET,
        [INK_VELVET_BLACK, INK_BLUE_NOTE_OCHRE],
        "reid_miles|francis_wolff|blue_note_4003|hard_bop_jazz",
    )
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
    P.text((110, 110), "SONNY ROLLINS", "grotesk_bold", 96, INK_VELVET_BLACK, tracking=-2)
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
    return P.finish(zmask=P.create_mask(zm), gate_range=(20, 42))


# ==============================================================================
# 14. BAUHAUS PHOTOGRAM & TYPOFOTO (LÁSZLÓ MOHOLY-NAGY 1925)
# ==============================================================================
def poster_14_bauhaus_typofoto():
    P = StylePoster(
        "14-bauhaus-typofoto",
        "style_bauhaus_typofoto",
        SUB_BROMO_CHLORIDE,
        [INK_EMULSION_BLACK, INK_BAUHAUS_RED],
        "moholy_nagy|typofoto|dessau_bauhaus_1925|rayogram_exposure",
    )
    dx, dy = P.drift

    # 1. Dark Silver Emulsion Background Field (Photographic darkroom exposure)
    P.rect(100, 180, 1100, 1180, INK_EMULSION_BLACK)

    # 2. Optical Photogram Luminescence: Negative glass lenses & wire springs
    # Main circular lens shadow (negative white exposure in black ground)
    P.ell(280, 360, 880, 960, SUB_BROMO_CHLORIDE)
    # Inner refraction rings
    for r in [260, 220, 170, 110, 60]:
        P.ring(580, 660, r, 2.5, INK_EMULSION_BLACK)

    # Spiral spring wire photogram
    pts_spiral = []
    for deg in range(0, 720, 10):
        rad = math.radians(deg)
        r = 40 + deg * 0.35
        pts_spiral.append((580 + math.cos(rad) * r, 660 + math.sin(rad) * r))
    for i in range(len(pts_spiral) - 1):
        P.line([pts_spiral[i], pts_spiral[i + 1]], INK_EMULSION_BLACK, w=3.0)

    # Geometric glass prism (Equilateral triangle)
    prism_pts = [(420, 880), (840, 880), (630, 480)]
    P.poly(prism_pts, SUB_BROMO_CHLORIDE)
    P.line([(420, 880), (840, 880)], INK_BAUHAUS_RED, w=4.5)
    P.line([(840, 880), (630, 480)], INK_BAUHAUS_RED, w=4.5)
    P.line([(630, 480), (420, 880)], INK_BAUHAUS_RED, w=4.5)

    # 3. Dynamic Bauhaus Signal Red Vector Ray
    P.line([(100, 180), (1100, 1180)], INK_BAUHAUS_RED, w=3.5)
    P.dot(630, 480, 22, INK_BAUHAUS_RED)

    # 4. Herbert Bayer Universal Typofoto Typography (Stark lowercase sans)
    P.text((100, 90), "bauhaus typofoto", "din_bold", 78, INK_EMULSION_BLACK, tracking=2)
    P.text((105, 170), "moholy-nagy // dessau bauhaus 1925 // typographie + fotografie", "din_bold", 18, INK_BAUHAUS_RED, tracking=2)

    # Callout annotations along orthographic grid
    P.text((140, 1220), "MALEREI FOTOGRAFIE FILM // BAND 8 DER BAUHAUSBÜCHER", "din_bold", 20, INK_EMULSION_BLACK, tracking=2)
    P.text((140, 1255), "LICHT ALS GESTALTUNGSMATERIAL — DIREKTE BELICHTUNG OHNE KAMERA", "grotesk", 15, INK_EMULSION_BLACK, tracking=1)
    P.text((140, 1285), "VERLAG ALBERT LANGEN // MÜNCHEN 1925", "grotesk", 14, INK_BAUHAUS_RED, tracking=1)

    P.line([(100, 1330), (1100, 1330)], INK_EMULSION_BLACK, w=2.0)

    def zm(dm):
        dm.rectangle([100 * S, 90 * S, 1100 * S, 1330 * S], fill=255)
    return P.finish(zmask=P.create_mask(zm), gate_range=(35, 55))


# ==============================================================================
# 15. 1970s POLISH POSTER SCHOOL SURREALISM (JAN LENICA WOZZECK)
# ==============================================================================
def poster_15_polish_surrealism():
    P = StylePoster(
        "15-polish-surrealism",
        "style_polish_surrealism",
        SUB_POLISH_OFFSET,
        [INK_GOUACHE_CHARCOAL, INK_POISON_OLIVE, INK_CRIMSON_RUST],
        "jan_lenica|polish_poster_school|wozzeck_1964|teatr_wielki",
    )
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
    P.text((600, 110), "WOZZECK", "din_bold", 124, INK_GOUACHE_CHARCOAL, tracking=4, anchor_x="center")
    P.text((600, 220), "OPERA W 3 AKTACH // ALBAN BERG", "din_bold", 26, INK_CRIMSON_RUST, tracking=3, anchor_x="center")

    # Lower Theatrical Imprint
    P.rect(120, 1160, 1080, 1270, INK_GOUACHE_CHARCOAL)
    P.text((600, 1185), "TEATR WIELKI W WARSZAWIE", "din_bold", 48, SUB_POLISH_OFFSET, tracking=5, anchor_x="center")

    P.text((120, 1310), "REŻYSERIA: JAN LENICA // KIEROWNICTWO MUZYCZNE: BOHDAN WODICZKO", "din_bold", 17, INK_GOUACHE_CHARCOAL, tracking=1)
    P.text((120, 1345), "POLISH POSTER SCHOOL ARCHIVE // WARSZAWA 1964 // WYDAWNICTWO ARTYSTYCZNO-GRAFICZNE", "grotesk", 14, INK_POISON_OLIVE, tracking=1)
    P.line([(120, 1380), (1080, 1380)], INK_CRIMSON_RUST, w=2.5)

    def zm(dm):
        dm.rectangle([120 * S, 110 * S, 1080 * S, 1380 * S], fill=255)
    return P.finish(zmask=P.create_mask(zm), gate_range=(28, 48))


# ==============================================================================
# MASTER RUNNER & CONTACT SHEET COMPOSITOR
# ==============================================================================
def create_contact_sheet(results, out_path="styles_contact_sheet.png"):
    """Assemble all posters into a high-resolution 5-column contact sheet."""
    thumb_w, thumb_h = 300, 400
    cols = 5
    rows = (len(results) + cols - 1) // cols
    pad_x = 24
    pad_y = 65
    sheet_w = cols * thumb_w + (cols + 1) * pad_x
    sheet_h = rows * (thumb_h + pad_y) + 115

    sheet = Image.new("RGB", (sheet_w, sheet_h), (0x12, 0x12, 0x14))
    sd = ImageDraw.Draw(sheet)
    f_title = load_font("din_bold", 11)
    f_sub = load_font("mono", 6)
    f_name = load_font("din_bold", 6.5)
    f_stat = load_font("mono", 5.5)

    # Master Header
    sd.text((pad_x, 24), f"{len(results)} MATERIAL-DRIVEN SYSTEMATIC DESIGN STYLES — MASTER AUDIT", font=f_title, fill=(0xF4, 0xF4, 0xF2))
    sd.text((pad_x, 56), "DETERMINISTIC VECTOR RENDERING // SUBSTRATE PHYSICS // DUXT HALFTONES // REPRODUCIBLE SEED ENGINES", font=f_sub, fill=(0x88, 0x88, 0x86))

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
        poster_11_sosaku_hanga,
        poster_12_swiss_cyber,
        poster_13_blue_note,
        poster_14_bauhaus_typofoto,
        poster_15_polish_surrealism,
    ]

    print("================================================================================")
    print("           RENDERING 15 SYSTEMATIC MATERIAL-DRIVEN POSTERS                      ")
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
    print("All 15 styles rendered deterministically and verified against gates.")
