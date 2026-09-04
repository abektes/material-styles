"""Render 10 mono-color gallery posters deterministically from catalog recipes.

Each poster resolves a Recipe Manifest (subject, palette, layout family, type
role, tension, imperfections) and draws it with monolib primitives. Same seed
always reproduces the same PNG. zmask= passes each poster's composed-content
silhouettes so the empty-paper gate measures composed zones, not dot pixels.
"""
import math

from PIL import Image, ImageChops
from monolib import (Poster, S, SUBSTRATES, mix, SERIF, SERIF_B, SANS, SANS_B,
                     MONO, MONO_B, W, H)

WHITE = SUBSTRATES["white"]
GRAY = SUBSTRATES["gray"]
BEIGE = SUBSTRATES["beige"]

BG = (0x00, 0x8A, 0x4B)      # Botanical Green
OXBLOOD = (0x8F, 0x34, 0x34)
TANGERINE = (0xE4, 0x6C, 0x2D)
SLATE = (0x47, 0x73, 0xA5)
ULTRA = (0x26, 0x3E, 0x99)   # Ultramarine
SORANGE = (0xE5, 0x5D, 0x2B)  # Safety Orange
TERRA = (0xC6, 0x5F, 0x38)
CHARCOAL = (0x30, 0x34, 0x3A)
SRED = (0xC8, 0x32, 0x32)
EBLUE = (0x17, 0x3A, 0xE3)   # Electric Blue
CARBON = (0x24, 0x23, 0x21)
MINT = (0x5E, 0xB7, 0x83)
CHARCOAL2 = (0x30, 0x2D, 0x2E)  # charcoal in the mint recipe
POWDER = (0x9E, 0xB8, 0xD3)
AUB = (0x63, 0x36, 0x5F)     # Aubergine
ROYAL = (0x20, 0x58, 0xD4)


def qbez(p0, p1, p2, t):
    x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
    y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
    return x, y


def qbez_tan(p0, p1, p2, t):
    dx = 2 * (1 - t) * (p1[0] - p0[0]) + 2 * t * (p2[0] - p1[0])
    dy = 2 * (1 - t) * (p1[1] - p0[1]) + 2 * t * (p2[1] - p1[1])
    n = math.hypot(dx, dy) or 1
    return dx / n, dy / n


def rot(vx, vy, ang):
    c, s = math.cos(ang), math.sin(ang)
    return vx * c - vy * s, vx * s + vy * c


# ---------------------------------------------------------------- 01 fern
def p01_fern():
    P = Poster("01-fern-archive", "beige", [BG, OXBLOOD],
               "fern|the archive of green|bg_oxblood|archival plate")
    dx, dy = P.drift
    P.text((110, 100), "FIELD ARCHIVE — SECTION G", SANS, 16, BG, tracking=6)
    P.text((108, 136), "the archive of green", SERIF, 92, BG)
    for a in [[(105, 295), (1095, 295)], [(105, 1185), (1095, 1185)],
              [(105, 295), (105, 1185)], [(1095, 295), (1095, 1185)]]:
        P.line(a, BG, 2)

    def frond(p0, p1, p2, n, L0, drop, ang_deg):
        prev = None
        leaf_pt = None
        for i in range(n + 1):
            t = i / n
            x, y = qbez(p0, p1, p2, t)
            if prev:
                P.line([prev, (x, y)], BG, 5)
            prev = (x, y)
            tx, ty = qbez_tan(p0, p1, p2, t)
            if i < n:
                for side in (-1, 1):
                    L = (L0 - drop * t) * (1 + P.rng.uniform(-0.08, 0.08))
                    if L < 24:
                        continue
                    dxx, dyy = rot(tx, ty, side * math.radians(ang_deg))
                    nx, ny = -dyy, dxx
                    hw = (9 + 11 * (L / L0)) * 1.15
                    tip = (x + dxx * L, y + dyy * L)
                    P.poly([(x + nx * hw, y + ny * hw), tip,
                            (x - nx * hw, y - ny * hw),
                            (x - dxx * 13, y - dyy * 13)], BG)
                    if n == 22 and i == 8 and side == 1:
                        leaf_pt = tip
        return leaf_pt

    lp = frond((660, 1160), (390, 730), (790, 360), 22, 215, 150, 64)
    frond((320, 1170), (200, 920), (470, 640), 16, 125, 85, 58)
    frond((900, 1170), (1010, 890), (760, 590), 16, 118, 80, 58)

    P.text((1088, 100), "PLATE 12 — PTERIDOPHYTA", MONO, 16, OXBLOOD,
           tracking=2, anchor_x="right")
    lx, ly = lp
    P.ring(lx + dx, ly + dy, 40, 2.5, OXBLOOD)
    P.line([(lx + 28 + dx, ly + 28 + dy), (lx + 84 + dx, ly + 84 + dy),
            (lx + 138 + dx, ly + 84 + dy)], OXBLOOD, 2)
    P.text((lx + 148 + dx, ly + 70 + dy), "sori, underside", SERIF, 23, OXBLOOD)
    cx = 108
    while cx < 300:
        P.rect(cx, 252, cx + 52, 258, BG)
        cx += 74

    P.text((110, 1214), "collected above the tide line — dried flat", MONO, 17, BG)
    for col in (110, 450, 790):
        P.greek(col, 1270, 300, 190, 8, BG, lw=6)

    zm = P.raw_layer(lambda dm: dm.rectangle([105 * S, 295 * S, 1095 * S, 1185 * S],
                                             fill=255))
    return P.finish(zmask=zm)


# ------------------------------------------------------------- 02 market
def p02_market():
    P = Poster("02-night-market", "white", [TANGERINE, SLATE],
               "night market|lanterns lit at dusk|tangerine_slate|object field")
    dx, dy = P.drift

    def lantern(cx, cy, r, outline=False):
        P.line([(cx, 0), (cx, cy - r + 6)], TANGERINE, 3)
        # thin paper contour separates this lantern from ones behind it
        P.ell(cx - r - 5, cy - r - 5, cx + r + 5, cy + r + 5, WHITE,
              outline=True, width=7)
        P.rect(cx - r * 0.16, cy - r - 10, cx + r * 0.16, cy - r + 6, TANGERINE)
        if outline:
            P.ell(cx - r, cy - r, cx + r, cy + r, TANGERINE, outline=True, width=11)
        else:
            P.ell(cx - r, cy - r, cx + r, cy + r, TANGERINE)
            for ddy, pad in ((-0.2 * r, 0.98 * r), (0.22 * r, 0.975 * r)):
                half = pad * r
                P.rect(cx - half, cy + ddy, cx + half, cy + ddy + 8, WHITE)
        P.rect(cx - 7, cy + r, cx + 7, cy + r + 24, TANGERINE)

    lant = [(980, 440, 412), (640, 310, 210), (340, 250, 150),
            (150, 500, 95), (730, 660, 120), (890, 800, 70),
            (280, 720, 56)]
    for cx, cy, r in lant:
        lantern(cx + dx, cy + dy, r)
    lantern(500 + dx, 580 + dy, 80, outline=True)

    P.rect(100, 80, 530, 114, WHITE)
    P.text((110, 90), "RIVERSIDE LANE — EVENINGS", SANS, 16, SLATE, tracking=6)
    P.text((108, 1150), "NIGHT", SANS_B, 200, SLATE, tracking=2)
    P.text((108, 1372), "MARKET", SANS_B, 200, SLATE, tracking=2)
    P.text((110, 1566), "lanterns lit at dusk", MONO, 16, SLATE)
    P.circled_note("smells like rain", 950, 1180, SERIF, 26, SLATE)

    def zm_fn(dm):
        for cx, cy, r in lant:
            dm.ellipse([(cx + dx - r) * S, (cy + dy - r) * S,
                        (cx + dx + r) * S, (cy + dy + r) * S], fill=255)
        dm.rectangle([108 * S, 1150 * S, 850 * S, 1365 * S], fill=255)
        dm.rectangle([108 * S, 1372 * S, 990 * S, 1590 * S], fill=255)
    return P.finish(zmask=P.raw_layer(zm_fn))


# --------------------------------------------------------------- 03 ride
def p03_ride():
    P = Poster("03-midnight-ride", "white", [ULTRA, SORANGE],
               "night ride|midnight ride|ultra_orange|ruled information")
    dx, dy = P.drift
    cx, cy, r = 880, 730, 470
    wheel = P.raw_layer(lambda dm: (
        dm.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
                   outline=255, width=46 * S),
        [dm.line([(cx + 60 * math.cos(math.radians(a)) * S,
                   cy + 60 * math.sin(math.radians(a)) * S),
                  (cx + (r - 26) * math.cos(math.radians(a)) * S,
                   cy + (r - 26) * math.sin(math.radians(a)) * S)],
                 fill=255, width=15 * S) for a in range(0, 360, 60)],
        dm.ellipse([(cx - 64) * S, (cy - 64) * S, (cx + 64) * S, (cy + 64) * S],
                   outline=255, width=16 * S)))
    P.stamp(wheel, ULTRA)
    P.dot(cx + (r - 26) * math.cos(math.radians(72)) + dx,
          cy + (r - 26) * math.sin(math.radians(72)) + dy, 22, SORANGE)

    P.text((100, 96), "PUBLIC RIDE — ALL WHEELS", SANS, 16, ULTRA, tracking=6)
    t1 = P.layer(lambda L: L.text(90, 340, "MIDNIGHT", SANS_B, 175))
    P.stamp(t1, ULTRA)
    P.stamp_where(t1, wheel, WHITE)
    t2 = P.layer(lambda L: L.text(90, 540, "RIDE", SANS_B, 175))
    P.stamp(t2, SORANGE, dx, dy)
    P.stamp_where(t2, wheel, mix(SORANGE, ULTRA, 0.35))
    P.text((1100, 110), "FRI — 22:00", MONO_B, 20, SORANGE, tracking=1,
           anchor_x="right")

    steps = 22
    for i in range(steps):
        t = i / steps
        x = cx + 90 + t * 210
        y = cy - 70 - t * t * 280
        P.dot(x + dx, y + dy, 9 - 2.6 * t, SORANGE)
    P.poly([(cx + 275 + dx, cy - 335 + dy), (cx + 325 + dx, cy - 255 + dy),
            (cx + 230 + dx, cy - 245 + dy)], SORANGE)

    for y in (1240, 1300, 1360):
        P.line([(100, y), (1100, y)], ULTRA, 2)
    for x in (460, 800):
        P.line([(x, 1240), (x, 1360)], ULTRA, 2)
    P.text((124, 1258), "DIST 40 KM", MONO, 19, ULTRA)
    P.text((484, 1258), "PACE BRISK", MONO, 19, ULTRA)
    P.text((824, 1258), "LIGHTS ON", MONO, 19, ULTRA)
    P.text((124, 1314), "start at the arch — ferry at dawn", MONO, 17, ULTRA)
    P.reg_mark(1120, 210, SORANGE)

    def zm_fn(dm):
        dm.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S], fill=255)
        dm.rectangle([90 * S, 340 * S, 1100 * S, 560 * S], fill=255)
        dm.rectangle([90 * S, 540 * S, 610 * S, 760 * S], fill=255)
        dm.rectangle([95 * S, 1230 * S, 1110 * S, 1370 * S], fill=255)
    return P.finish(zmask=P.raw_layer(zm_fn))


# ---------------------------------------------------------------- 04 tea
def p04_tea():
    P = Poster("04-still-steaming", "beige", [TERRA],
               "tea|still steaming|terracotta|editorial journal")
    dx, dy = P.drift
    TABLE = 1230
    pot = P.layer(lambda L: L.ell(90, 480, 810, 1230))
    P.stamp(pot, TERRA, dx, dy)
    P.poly([(640 + dx, 700 + dy), (880 + dx, 590 + dy), (905 + dx, 655 + dy),
            (675 + dx, 762 + dy)], TERRA)  # spout
    P.ring(82 + dx, 850 + dy, 102, 22, BEIGE)            # handle notch
    P.rect(330 + dx, 448 + dy, 570 + dx, 486 + dy, TERRA)  # lid
    P.ell(415 + dx, 404 + dy, 485 + dx, 450 + dy, TERRA)   # knob
    P.rect(0, TABLE + dy, 1200, 1600, TERRA)               # table ink pool
    P.rect(0, 1236 + dy, 1200, 1244 + dy, BEIGE)           # paper cut at the rim

    for i, base in enumerate((415, 468)):
        y = 400
        while y > 190:
            t = (400 - y) / 210
            x = base + 24 * math.sin(y * 0.022 + i * 2.6)
            r = (6 - 3 * t) * (1 + P.rng.uniform(-0.12, 0.12))
            P.dot(x + dx, y + dy, r, TERRA)
            y -= 21

    P.text((110, 100), "KITCHEN JOURNAL — NO. 3", SANS, 16, TERRA, tracking=6)
    P.greek(860, 150, 120, 360, 12, TERRA, lw=6)
    P.greek(1010, 150, 90, 360, 12, TERRA, lw=6)
    P.text((860, 540), "three cups before", MONO, 17, TERRA)
    P.text((860, 570), "the first word.", MONO, 17, TERRA)
    title = P.layer(lambda L: L.text(140, 640, "still steaming", SERIF, 150))
    P.stamp(title, mix(TERRA, BEIGE, 0.6), dx + 3, dy - 3)
    P.stamp(title, TERRA, dx, dy)
    P.stamp_where(title, pot, BEIGE)
    cx = 152
    while cx < 430:
        P.rect(cx + dx, 830 + dy, cx + 48 + dx, 836 + dy, TERRA)
        cx += 68
    # knocked-out caption inside the table pool
    P.text((140, 1390), "three cups before the first word.", MONO, 19, BEIGE)
    P.text((1100, 1390), "NO. 3", MONO, 19, BEIGE, anchor_x="right")

    def zm_fn(dm):
        dm.ellipse([90 * S, 480 * S, 810 * S, 1230 * S], fill=255)
        dm.rectangle([0, 1230 * S, 1200 * S, 1600 * S], fill=255)
        dm.rectangle([850 * S, 140 * S, 1120 * S, 600 * S], fill=255)
        dm.rectangle([380 * S, 190 * S, 520 * S, 480 * S], fill=255)
        dm.rectangle([810 * S, 640 * S, 1190 * S, 830 * S], fill=255)
    return P.finish(zmask=P.raw_layer(zm_fn))


# ---------------------------------------------------------------- 05 gull
def p05_gull():
    P = Poster("05-harbour-gull", "gray", [CHARCOAL, SRED],
               "gull|no rent|charcoal_red|image field")
    dx, dy = P.drift
    P.ell(400, 0, 1460, 1120, WHITE)  # white head plate on gray page
    crown_pts = [(930 + 530 * math.cos(math.radians(a)),
                  560 + 560 * math.sin(math.radians(a)))
                 for a in range(180, 361, 8)]
    crown = P.layer(lambda L: L.poly(crown_pts))
    P.stamp(crown, CHARCOAL, dx, dy)
    neck_pts = [(700, 950), (1240, 950), (1300, 1600), (650, 1600)]
    neck = P.layer(lambda L: L.poly(neck_pts))
    P.stamp(neck, CHARCOAL, dx, dy)
    wing_pts = [(0, 1600), (0, 1230), (390, 1140), (720, 1600)]
    wing = P.layer(lambda L: L.poly(wing_pts))
    P.stamp(wing, CHARCOAL, dx, dy)

    def neck_x(y):
        f = (y - 950) / 650
        return 700 - 50 * f, 1240 + 60 * f

    for y0, y1, col in ((1115, 1200, WHITE), (1312, 1434, SRED)):
        a0, b0 = neck_x(y0)
        a1, b1 = neck_x(y1)
        P.poly([(a0 + 10, y0), (b0 - 10, y0), (b1 - 10, y1), (a1 + 10, y1)], col)

    P.poly([(700 + dx, 620 + dy), (150 + dx, 710 + dy), (715 + dx, 775 + dy)], SRED)
    P.dot(665 + dx, 700 + dy, 7, WHITE)
    P.dot(1090, 610, 28, CHARCOAL)
    P.ring(1090, 610, 54, 8, SRED)

    P.text((110, 100), "FIELD OBSERVATIONS — HARBOUR WALL", MONO, 16, CHARCOAL,
           tracking=2)
    vt = P.layer(lambda L: L.text(300, 280, "NO RENT", SERIF_B, 128))
    P.stamp(vt, CHARCOAL)
    P.stamp_where(vt, crown, WHITE)
    P.circled_note("unbothered", 120, 980, SERIF, 30, SRED)
    P.dot(320, 1380, 46, SRED)
    P.text((60, 1544), "gull, adult, unimpressed", MONO, 15, WHITE)

    def zm_fn(dm):
        dm.ellipse([400 * S, 0, 1460 * S, 1120 * S], fill=255)
        dm.polygon([(x * S, y * S) for x, y in neck_pts], fill=255)
        dm.polygon([(x * S, y * S) for x, y in wing_pts], fill=255)
        dm.polygon([(700 * S, 620 * S), (150 * S, 710 * S), (715 * S, 775 * S)],
                   fill=255)
        dm.ellipse([290 * S, 1350 * S, 350 * S, 1410 * S], fill=255)
    return P.finish(extra=[WHITE], zmask=P.raw_layer(zm_fn))


# -------------------------------------------------------------- 06 sound
def p06_sound():
    P = Poster("06-sound-check", "white", [CARBON, EBLUE],
               "sound check|sound check|electric_carbon|overprint collage")
    dx, dy = P.drift
    circ = P.layer(lambda L: L.ell(-240, 240, 880, 1420))
    P.stamp(circ, CARBON)
    OVER = ((CARBON[0] * EBLUE[0]) // 255, (CARBON[1] * EBLUE[1]) // 255,
            (CARBON[2] * EBLUE[2]) // 255)
    band = P.raw_layer(lambda dm: dm.ellipse(
        [(140 + dx) * S, (320 + dy) * S, (1080 + dx) * S, (1260 + dy) * S],
        outline=255, width=52 * S))
    P.stamp(band, EBLUE, dx, dy)
    P.stamp_where(band, circ, OVER)

    t1 = P.layer(lambda L: L.text(80, 390, "SOUND", SANS_B, 300))
    t2 = P.layer(lambda L: L.text(80, 880, "CHECK", SANS_B, 300))
    for t in (t1, t2):
        P.stamp(t, EBLUE, dx, dy)
        P.stamp_where(t, circ, OVER)
        P.stamp_where(t, band, WHITE)

    P.text((90, 110), "BASEMENT SERIES — DOORS LATE", MONO, 17, EBLUE, tracking=2)
    P.text((90, 1550), "bring earplugs — we mean it", MONO, 17, EBLUE)

    ring_zone = P.raw_layer(lambda dm: dm.ellipse(
        [160 * S, 300 * S, 1120 * S, 1280 * S], fill=255))

    def zm_fn(dm):
        dm.ellipse([-240 * S, 240 * S, 880 * S, 1420 * S], fill=255)
        dm.rectangle([80 * S, 390 * S, 1160 * S, 740 * S], fill=255)
        dm.rectangle([80 * S, 880 * S, 1160 * S, 1230 * S], fill=255)
    zm = ImageChops.lighter(P.raw_layer(zm_fn), ring_zone)
    return P.finish(zmask=zm)


# -------------------------------------------------------------- 07 paper
def p07_paper():
    P = Poster("07-paper-keeps", "gray", [CHARCOAL2, MINT],
               "paper keeps things|paper keeps things|mint_charcoal|type declaration")
    dx, dy = P.drift
    P.text((110, 96), "NOTES ON KEEPING THINGS", MONO, 19, MINT, tracking=4)
    P.text((-90, 140), "PAPER", SERIF_B, 400, CHARCOAL2)
    P.text((-90, 570), "KEEPS", SERIF_B, 250, MINT)
    P.text((-90, 860), "THINGS", SERIF_B, 400, CHARCOAL2)
    cx = -60
    while cx < 700:
        P.rect(cx + dx, 1220 + dy, cx + 100 + dx, 1232 + dy, MINT)
        cx += 160
    P.text((110, 1550), "fold, crease, keep, pass on", MONO, 18, MINT)

    def zm_fn(dm):
        dm.rectangle([0, 150 * S, 1200 * S, 580 * S], fill=255)
        dm.rectangle([0, 580 * S, 1200 * S, 830 * S], fill=255)
        dm.rectangle([0, 870 * S, 1200 * S, 1300 * S], fill=255)
    return P.finish(zmask=P.raw_layer(zm_fn))


# ---------------------------------------------------------------- 08 pool
def p08_pool():
    P = Poster("08-the-pool", "white", [POWDER, SRED],
               "public pool|the pool is open|powder_red|editorial cover")
    dx, dy = P.drift
    P.text((100, 110), "THE POOL", SANS_B, 175, POWDER, tracking=8)
    P.text((100, 310), "IS OPEN", SANS_B, 175, SRED, tracking=8)
    P.text((100, 545), "cold water — warm concrete", SANS_B, 20, POWDER, tracking=2)
    P.text((100, 610), "shallow end to the left", MONO, 17, SRED)

    P.halftone(0, 710, 1200, 1600, 20, lambda x, y: 5 + 11 * (y - 710) / 890,
               lambda x, y: y > 710, POWDER, drift=(dx, dy))
    P.rect(0, 1400, 1200, 1600, POWDER)  # ink pools at depth
    for y, r, pit in ((980, 12.5, 30), (1250, 13.5, 36)):
        x = 110
        while x < 1090:
            P.dot(x + dx, y + dy, r, SRED)
            x += pit
    for x in (1120, 1185):
        P.rect(x - 8, 0, x + 8, 1020, POWDER)
    for y in (300, 470, 640, 810, 960):
        P.rect(1112, y, 1193, y + 16, POWDER)
    P.ring(880 + dx, 1190 + dy, 190, 100, SRED)

    steps = 26
    for i in range(steps):
        t = i / steps
        x = 470 + t * 360
        y = 565 + t * t * 440
        P.dot(x + dx, y + dy, 9, SRED)
    P.poly([(838 + dx, 1006 + dy), (806 + dx, 986 + dy), (856 + dx, 968 + dy)], SRED)

    def zm_fn(dm):
        dm.rectangle([95 * S, 115 * S, 1055 * S, 295 * S], fill=255)
        dm.rectangle([95 * S, 315 * S, 810 * S, 495 * S], fill=255)
        dm.rectangle([95 * S, 540 * S, 660 * S, 640 * S], fill=255)
        dm.rectangle([0, 710 * S, 1200 * S, 1600 * S], fill=255)
    return P.finish(zmask=P.raw_layer(zm_fn))


# ---------------------------------------------------------------- 09 moon
def p09_moons():
    P = Poster("09-night-log", "beige", [AUB],
               "moon phases|three moods of the same light|aubergine|specimen annotation")
    dx, dy = P.drift
    P.text((110, 88), "NIGHT LOG — ROOFTOP", SANS, 16, AUB, tracking=6)
    big_box = (360, -150, 1480, 990)
    inner_box = (660, -140, 1180, 880)
    cres = ImageChops.multiply(
        P.layer(lambda L: L.ell(*big_box)),
        ImageChops.invert(P.layer(lambda L: L.ell(*inner_box))))
    ghost = ImageChops.multiply(
        P.layer(lambda L: L.ell(big_box[0] + 24, big_box[1] - 14,
                                big_box[2] + 16, big_box[3] - 9)),
        ImageChops.invert(P.layer(lambda L: L.ell(inner_box[0] + 24, inner_box[1] - 14,
                                                  inner_box[2] + 16, inner_box[3] - 9))))
    P.stamp(ghost, mix(AUB, BEIGE, 0.62), dx, dy)
    P.stamp(cres, AUB, dx, dy)

    half = P.layer(lambda L: L.ell(120, 880, 600, 1360))
    P.stamp(half, AUB, dx, dy)
    cut = P.layer(lambda L: L.rect(360, 880, 600, 1360))
    P.knock(cut, dx, dy)

    P.ell(520, 1160, 860, 1500, AUB)
    for _ in range(8):
        a = P.rng.uniform(0, 2 * math.pi)
        rr = P.rng.uniform(15, 125)
        cx, cy = 690 + rr * math.cos(a), 1330 + rr * math.sin(a) * 0.9
        P.dot(cx, cy, P.rng.uniform(7, 15) * (1 + P.rng.uniform(-0.12, 0.12)), BEIGE)

    for _ in range(26):
        P.dot(P.rng.uniform(60, 460), P.rng.uniform(400, 800),
              P.rng.uniform(2, 4), AUB)

    tmask = P.layer(lambda L: [L.text(108, 124, "three moods", SERIF, 100),
                               L.text(108, 240, "of the same light", SERIF, 100)])
    P.stamp(tmask, AUB)
    P.stamp_where(tmask, cres, BEIGE)

    # ruled lunar-date strip
    for y in (1424, 1474, 1524, 1574):
        P.line([(100, y), (1100, y)], AUB, 2)
    P.text((124, 1436), "09 SEP — RISE 21:14  SET 06:02", MONO, 16, AUB)
    P.text((124, 1486), "17 SEP — LAST QUARTER", MONO, 16, AUB)
    P.text((124, 1536), "25 SEP — NEW, QUIET NIGHT", MONO, 16, AUB)
    P.text((900, 1240), "01 — FULL", MONO, 17, AUB)
    P.line([(893, 1252), (845, 1252)], AUB, 2)
    P.text((100, 892), "02 — HALF", MONO, 17, AUB)
    P.line([(225, 904), (262, 918)], AUB, 2)
    P.text((860, 990), "03 — CRESCENT, THE FAVOURITE", MONO, 17, AUB)

    def zm_fn(dm):
        dm.ellipse([big_box[0] * S, big_box[1] * S, big_box[2] * S, big_box[3] * S],
                   fill=255)
        dm.ellipse([inner_box[0] * S, inner_box[1] * S, inner_box[2] * S,
                    inner_box[3] * S], fill=0)
        dm.ellipse([120 * S, 880 * S, 600 * S, 1360 * S], fill=255)
        dm.ellipse([520 * S, 1160 * S, 860 * S, 1500 * S], fill=255)
        dm.rectangle([100 * S, 124 * S, 910 * S, 340 * S], fill=255)
        dm.rectangle([100 * S, 1424 * S, 1100 * S, 1574 * S], fill=255)
    return P.finish(zmask=P.raw_layer(zm_fn))


# ---------------------------------------------------------------- 10 walk
def p10_walk():
    P = Poster("10-the-long-way", "white", [ROYAL],
               "summer walk|walk until the town ends|royal blue|editorial cover")
    dx, dy = P.drift
    HORIZON = 800
    # pale sky haze above the horizon (release field)
    P.halftone(0, 560, 1200, 798, 26,
               lambda x, y: 1.5 + 3.5 * (y - 560) / 238,
               lambda x, y: True, ROYAL)
    P.line([(0, HORIZON), (1200, HORIZON)], ROYAL, 3)
    # screened sun
    SUN = (950, 300, 230)
    P.halftone(SUN[0] - SUN[2] - 30, SUN[1] - SUN[2] - 30,
               SUN[0] + SUN[2] + 30, SUN[1] + SUN[2] + 30, 20,
               lambda x, y: (13 * (1 - math.hypot(x - SUN[0], y - SUN[1]) / SUN[2])
                             if math.hypot(x - SUN[0], y - SUN[1]) < SUN[2] else 0),
               lambda x, y: math.hypot(x - SUN[0], y - SUN[1]) < SUN[2], ROYAL)
    for x, w, h in [(420, 48, 70), (486, 62, 100), (566, 40, 56), (620, 80, 118),
                    (716, 52, 78), (784, 36, 50)]:
        P.rect(x, HORIZON - h, x + w, HORIZON, ROYAL)

    pts = [(320, 1660, 330), (500, 1400, 255), (420, 1160, 195), (560, 980, 130),
           (500, 870, 72), (545, 800, 38)]
    road_img = Image.new("L", (W, H), 0)
    from PIL import ImageDraw as ID
    rd = ID.Draw(road_img)
    n_steps = 500
    for i in range(n_steps + 1):
        t = i / n_steps
        seg = t * (len(pts) - 1)
        j = min(int(seg), len(pts) - 2)
        lt = seg - j
        x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * lt
        y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * lt
        w = pts[j][2] + (pts[j + 1][2] - pts[j][2]) * lt
        rd.ellipse([(x - w) * S, (y - w) * S, (x + w) * S, (y + w) * S], fill=255)
    P.img.paste(ROYAL, (0, 0), road_img)
    for i in range(0, n_steps, 14):
        t = i / n_steps
        seg = t * (len(pts) - 1)
        j = min(int(seg), len(pts) - 2)
        lt = seg - j
        x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * lt
        y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * lt
        w = pts[j][2] + (pts[j + 1][2] - pts[j][2]) * lt
        P.dot(x, y, max(2, w * 0.07), WHITE)

    for t, label in ((0.32, "26"), (0.55, "11"), (0.78, "5"), (0.94, "0")):
        seg = t * (len(pts) - 1)
        j = min(int(seg), len(pts) - 2)
        lt = seg - j
        x = pts[j][0] + (pts[j + 1][0] - pts[j][0]) * lt
        y = pts[j][1] + (pts[j + 1][1] - pts[j][1]) * lt
        w = pts[j][2] + (pts[j + 1][2] - pts[j][2]) * lt
        if t > 0.4:
            P.text((x + w + 22, y - 12), label, MONO, 18, ROYAL)
        else:  # road-paint kilometre mark, knocked out of the ribbon
            P.text((x - w * 0.3, y - 14), label, MONO, 20, WHITE)

    def grass_ok(x, y):
        if y <= 1100:
            return False
        return not (90 < x < 1080 and 1270 < y < 1590)

    P.halftone(0, 1100, 1200, 1600, 25,
               lambda x, y: 4 + 9 * (y - 1100) / 500, grass_ok, ROYAL,
               drift=(dx, dy))

    P.text((110, 96), "SUNDAY — NO DESTINATION", SANS, 16, ROYAL, tracking=6)
    title = P.layer(lambda L: [L.text(110, 1280, "walk until", SERIF, 120),
                               L.text(110, 1440, "the town ends", SERIF, 120)])
    P.stamp(title, ROYAL, dx, dy)
    P.stamp_where(title, road_img, WHITE)

    def zm_fn(dm):
        dm.rectangle([0, 540 * S, 1200 * S, 800 * S], fill=255)   # sky haze band
        dm.ellipse([(SUN[0] - SUN[2]) * S, (SUN[1] - SUN[2]) * S,
                    (SUN[0] + SUN[2]) * S, (SUN[1] + SUN[2]) * S], fill=255)
        dm.rectangle([0, 1100 * S, 1200 * S, 1600 * S], fill=255)  # grass field
    zm = ImageChops.lighter(P.raw_layer(zm_fn), road_img)
    return P.finish(zmask=zm)


if __name__ == "__main__":
    targets = {
        "01-fern-archive": (40, 55), "02-night-market": (25, 50),
        "03-midnight-ride": (35, 55), "04-still-steaming": (35, 55),
        "05-harbour-gull": (20, 40), "06-sound-check": (20, 40),
        "07-paper-keeps": (20, 45), "08-the-pool": (25, 45),
        "09-night-log": (35, 55), "10-the-long-way": (25, 45),
    }
    rows = []
    for fn in (p01_fern, p02_market, p03_ride, p04_tea, p05_gull,
               p06_sound, p07_paper, p08_pool, p09_moons, p10_walk):
        rows.append(fn())
    print(f"{'slug':22} {'px%':>6} {'zone%':>6} {'family':>9} ok  {'ink shares':>10}  path")
    for r in rows:
        lo, hi = targets[r["slug"]]
        ok = "OK " if lo <= r["zempty"] <= hi else "OUT"
        sh = "/".join(f"{s:.0f}" for s in r["shares"])
        print(f"{r['slug']:22} {r['empty']:6.1f} {r['zempty']:6.1f} "
              f"{lo:>4}-{hi:<4} {ok}  {sh:>10}  {r['path']}")
