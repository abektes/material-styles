"""MONO-COLOR — deterministic motion showreel.

Story: a phantom print shop runs one job through the machine. Paper loads,
the ink catalog stamps in, ten plates flash-cut through (each poster with its
own kinetic phrase and motion motif), the full run tiles into a gallery wall,
and the job ends on a slate: same seed, same pixels. Every frame is drawn in
code with PIL and encoded with ffmpeg — no generative imagery, no randomness
beyond seeded grain tiles.
"""
import hashlib
import math
import os

import numpy as np
import imageio.v2 as imageio
import imageio_ffmpeg
from PIL import Image, ImageChops, ImageDraw, ImageFont

W, H = 1920, 1080
FPS = 30
FD = "/usr/share/fonts/truetype/dejavu/"
GAL = "../gallery"

SUBS = {
    "white": (0xFA, 0xFA, 0xF7),
    "gray": (0xE9, 0xE9, 0xE5),
    "beige": (0xF5, 0xF1, 0xE8),
}
INKS = {
    "BG": (0x00, 0x8A, 0x4B), "OXBLOOD": (0x8F, 0x34, 0x34),
    "TANGERINE": (0xE4, 0x6C, 0x2D), "SLATE": (0x47, 0x73, 0xA5),
    "ULTRA": (0x26, 0x3E, 0x99), "SORANGE": (0xE5, 0x5D, 0x2B),
    "TERRA": (0xC6, 0x5F, 0x38), "CHARCOAL": (0x30, 0x34, 0x3A),
    "SRED": (0xC8, 0x32, 0x32), "EBLUE": (0x17, 0x3A, 0xE3),
    "CARBON": (0x24, 0x23, 0x21), "MINT": (0x5E, 0xB7, 0x83),
    "CHARCOAL2": (0x30, 0x2D, 0x2E), "POWDER": (0x9E, 0xB8, 0xD3),
    "AUB": (0x63, 0x36, 0x5F), "ROYAL": (0x20, 0x58, 0xD4),
    "PAPER": (0xFA, 0xFA, 0xF7),
}

# ---------------------------------------------------------------- easing
def clamp01(v):
    return 0.0 if v < 0 else (1.0 if v > 1 else v)


def lerp(a, b, t):
    return a + (b - a) * t


def e_out_expo(t):
    t = clamp01(t)
    return 1.0 if t >= 1 else 1 - math.pow(2, -10 * t)


def e_out_cubic(t):
    t = clamp01(t)
    return 1 - math.pow(1 - t, 3)


def e_in_out_quint(t):
    t = clamp01(t)
    return 16 * t ** 5 if t < 0.5 else 1 - math.pow(-2 * t + 2, 5) / 2


def e_out_back(t, s=1.70158):
    t = clamp01(t)
    return 1 + (s + 1) * math.pow(t - 1, 3) + s * math.pow(t - 1, 2)


def mix(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


_FONTS = {}


def F(name, size):
    key = (name, size)
    if key not in _FONTS:
        _FONTS[key] = ImageFont.truetype(FD + name, size)
    return _FONTS[key]


SERIF, SERIF_B = "DejaVuSerif.ttf", "DejaVuSerif-Bold.ttf"
SANS, SANS_B = "DejaVuSans.ttf", "DejaVuSans-Bold.ttf"
MONO = "DejaVuSansMono.ttf"

# ---------------------------------------------------------------- posters
PW, PH = 750, 1000
POSTERS = [
    # file, dom, accent|None, substrate, phrase lines, font, size, kicker, motif
    ("01-fern-archive.png", "BG", "OXBLOOD", "beige",
     ["the archive", "of green"], SERIF, 118, "PLATE 12 — PTERIDOPHYTA", "leaflets"),
    ("02-night-market.png", "TANGERINE", "SLATE", "white",
     ["NIGHT", "MARKET"], SANS_B, 150, "RIVERSIDE LANE — EVENINGS", "lanterns"),
    ("03-midnight-ride.png", "ULTRA", "SORANGE", "white",
     ["MIDNIGHT", "RIDE"], SANS_B, 150, "FRI — 22:00 · DIST 40 KM", "wheel"),
    ("04-still-steaming.png", "TERRA", None, "beige",
     ["still", "steaming"], SERIF, 130, "KITCHEN JOURNAL — NO. 3", "steam"),
    ("05-harbour-gull.png", "CHARCOAL", "SRED", "gray",
     ["NO", "RENT"], SERIF_B, 165, "FIELD OBSERVATIONS — HARBOUR WALL", "beak"),
    ("06-sound-check.png", "CARBON", "EBLUE", "white",
     ["SOUND", "CHECK"], SANS_B, 150, "BASEMENT SERIES — DOORS LATE", "overprint"),
    ("07-paper-keeps.png", "CHARCOAL2", "MINT", "gray",
     ["paper", "keeps", "things"], SERIF_B, 120, "NOTES ON KEEPING THINGS", "marquee"),
    ("08-the-pool.png", "POWDER", "SRED", "white",
     ["THE POOL", "IS OPEN"], SANS_B, 138, "COLD WATER — WARM CONCRETE", "pool"),
    ("09-night-log.png", "AUB", None, "beige",
     ["three moods", "of the same light"], SERIF, 92, "NIGHT LOG — ROOFTOP", "moon"),
    ("10-the-long-way.png", "ROYAL", None, "white",
     ["walk until", "the town ends"], SERIF, 118, "SUNDAY — NO DESTINATION", "road"),
]


def load_posters():
    out = []
    for p in POSTERS:
        im = Image.open(os.path.join(GAL, p[0])).convert("RGB").resize((PW, PH),
                                                                      Image.LANCZOS)
        out.append((im,) + p)
    return out


# ---------------------------------------------------------------- type
def tracked(d, xy, s, fname, size, fill, tr=0, anchor="left"):
    f = F(fname, size)
    total = sum(d.textlength(ch, font=f) for ch in s) + tr * max(0, len(s) - 1)
    x, y = xy
    if anchor == "right":
        x -= total
    elif anchor == "center":
        x -= total / 2
    for ch in s:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + tr
    return total


def kinetic(img, x, y, s, fname, size, fill, t, hold=0.55):
    """Word reveal: left-to-right clip wipe with a small y settle."""
    f = F(fname, size)
    rev = e_out_expo((t) / hold)
    if rev <= 0:
        return 0
    w = int(text_w(ImageDraw.Draw(img), s, fname, size)) + 2
    tmp = Image.new("L", (w + 4, size + 40), 0)
    ImageDraw.Draw(tmp).text((0, 0), s, font=f, fill=255)
    cw = max(1, int(w * rev))
    tmp = tmp.crop((0, 0, cw, size + 40))
    solid = Image.new("RGB", tmp.size, fill)
    yy = int(y - 14 * (1 - rev))
    img.paste(solid, (int(x), yy), tmp)
    return w


def text_w(d, s, fname, size, tr=0):
    f = F(fname, size)
    return sum(d.textlength(ch, font=f) for ch in s) + tr * max(0, len(s) - 1)


# ---------------------------------------------------------------- grain
def make_grain(n=4):
    tiles = []
    for _ in range(n):
        b = os.urandom(W * H)
        g = Image.frombytes("L", (W, H), b)
        tiles.append(Image.merge("RGB", (g, g, g)))
    return tiles


GRAIN = None


def add_grain(frame, i):
    frame = Image.blend(frame, GRAIN[i % len(GRAIN)], 0.045)
    return frame


# ---------------------------------------------------------------- overlays
def reg_mark(d, cx, cy, ink, r=16, w=2.2):
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=ink, width=int(w * 2))
    d.line([(cx - r - 10, cy), (cx + r + 10, cy)], fill=ink, width=4)
    d.line([(cx, cy - r - 10), (cx, cy + r + 10)], fill=ink, width=4)


def overlays(img, d, chapter_idx, t, ticket, dark=False, show_reg=True):
    base = SUBS["white"] if dark else INKS["CHARCOAL"]
    off = mix(base, INKS["CHARCOAL2"] if dark else SUBS["white"], 0.55)
    tracked(d, (70, 44), ticket, MONO, 22, base, 4)
    # plate counter
    if chapter_idx is not None:
        label = f"PLATE {chapter_idx + 1:02d}/10"
    else:
        label = "— /10"
    tracked(d, (W - 70, 44), label, MONO, 22, base, 4, anchor="right")
    for i in range(10):
        x = W - 70 - text_w(d, label, MONO, 22, 4) - 150 + i * 12
        on = chapter_idx is not None and i <= chapter_idx
        d.rectangle([x, 48, x + 8, 56], fill=base if on else off)
    # drifting registration mark (misregistration motif)
    if show_reg and chapter_idx is not None:
        dx = 3 * math.sin(chapter_idx * 1.7 + t * 6.283)
        dy = 3 * math.cos(chapter_idx * 2.3 + t * 6.283)
        reg_mark(d, W - 84 + dx, H - 76 + dy, base)


# ---------------------------------------------------------------- shots
def shot_open(img, d, t):
    sub = SUBS["white"]
    # registration cross draws on
    a = e_out_cubic(t / 0.18)
    reg_mark(d, W / 2, H / 2, INKS["CHARCOAL"], r=26 * a + 2, w=2.4)
    # title stamps
    if t > 0.16:
        s = 1.14 - 0.14 * e_out_expo((t - 0.16) / 0.3)
        f = F(SERIF_B, int(200 * s))
        d.text((W / 2 - f.getlength("TWO INKS.") / 2, 400), "TWO INKS.",
               font=f, fill=INKS["CHARCOAL2"])
    if t > 0.30:
        s = 1.14 - 0.14 * e_out_expo((t - 0.30) / 0.3)
        f = F(SERIF_B, int(200 * s))
        d.text((W / 2 - f.getlength("ONE SHEET.") / 2, 620), "ONE SHEET.",
               font=f, fill=INKS["SRED"])
    # substrate swatch bars wipe through the bottom
    if t > 0.5:
        p = e_in_out_quint((t - 0.5) / 0.35)
        bw = 300
        x0 = W / 2 - 1.5 * bw
        for i, (name, hexv) in enumerate([("WHITE", "#FAFAF7"), ("GRAY", "#E9E9E5"),
                                          ("BEIGE", "#F5F1E8")]):
            x = x0 + i * bw + (1 - p) * (W if i % 2 else -W)
            d.rectangle([x, 940, x + bw - 14, 1010], fill=SUBS[name.lower()],
                        outline=INKS["CHARCOAL"], width=2)
            tracked(d, (x + 18, 1022), f"{name} {hexv}", MONO, 18, INKS["CHARCOAL"], 2)
    if t > 0.85:
        kinetic(img, W / 2 - text_w(d, "A DETERMINISTIC PRINT SYSTEM", MONO, 24, 6) / 2,
                190, "A DETERMINISTIC PRINT SYSTEM", MONO, 24, INKS["CHARCOAL"],
                (t - 0.85) / 0.1, hold=1.0)


CATALOG = ["BG", "OXBLOOD", "TANGERINE", "SLATE", "ULTRA", "SORANGE", "TERRA",
           "CHARCOAL", "SRED", "EBLUE", "CARBON", "MINT", "POWDER", "AUB", "ROYAL"]


def shot_catalog(img, d, t):
    n = len(CATALOG)
    bw = (W - 240) / n
    # bars stagger in
    for i, name in enumerate(CATALOG):
        lt = clamp01((t - i * 0.018) / 0.3)
        if lt <= 0:
            continue
        h = 280 * e_out_back(lt)
        x = 120 + i * bw
        d.rectangle([x + 8, 780 - h, x + bw - 10, 780], fill=INKS[name])
        if lt > 0.8:
            c = INKS[name]
            tracked(d, (x + 12, 800), "#%02X%02X%02X" % c, MONO, 15,
                    INKS["CHARCOAL"], 0)
    # ruler line ticks across the top
    p = e_in_out_quint(clamp01(t / 0.35))
    d.line([(120, 280), (120 + (W - 240) * p, 280)], fill=INKS["CHARCOAL"], width=3)
    for i in range(n):
        if i / n < p:
            x = 120 + i * bw + bw / 2
            d.line([(x, 268), (x, 292)], fill=INKS["CHARCOAL"], width=3)
    if t > 0.45:
        kinetic(img, 120, 330, "10 POSTERS · 9 LAYOUTS · 3 SUBSTRATES · ≤ 2 INKS",
                MONO, 30, INKS["CHARCOAL"], (t - 0.45) / 0.12, hold=0.7)
    if t > 0.6:
        kinetic(img, 120, 392, "EVERY FRAME RENDERED IN CODE", SERIF, 60,
                INKS["CHARCOAL2"], (t - 0.6) / 0.12, hold=0.7)


# ---------------------------------------------------------------- motifs
def motif(img, d, kind, dom, acc, sub, t, area):
    ax, ay, aw, ah = area  # type-side area
    domc, subc = INKS[dom], SUBS[sub]
    if kind == "leaflets":
        for i in range(16):
            sp = 0.5 + (i * 37 % 10) / 10
            x = ax + aw + 260 - (t * 900 * sp + i * 130) % (aw + 560)
            y = ay - 120 + ((t * 520 * sp + i * 97) % (ah + 300))
            s_ = 14 + (i * 53 % 22)
            ang = math.radians(60 + (i * 31 % 60))
            dx, dy = math.cos(ang), math.sin(ang)
            d.polygon([(x - dx * s_, y - dy * s_), (x + dy * s_ * .4, y - dx * s_ * .4),
                       (x - dy * s_ * .4, y + dx * s_ * .4)],
                      fill=mix(domc, subc, 0.25 + 0.3 * (i % 3) / 3))
    elif kind == "lanterns":
        for i in range(5):
            r = 26 + (i * 29 % 26)
            prog = (t * 0.9 + i * 0.19) % 1.0
            x = ax + 60 + i * (aw - 140) / 4 + 14 * math.sin(t * 12 + i)
            y = ay + ah + 60 - prog * (ah + 200)
            c = INKS["TANGERINE"] if i % 2 == 0 else mix(INKS["SLATE"], subc, 0.15)
            d.line([(x, y - r - 90), (x, y - r)], fill=c, width=3)
            d.ellipse([x - r, y - r, x + r, y + r], outline=c, width=6)
            d.ellipse([x - r * .45, y - r * .45, x + r * .45, y + r * .45], fill=c)
    elif kind == "wheel":
        cx, cy = ax + aw * 0.72, ay + ah - 240
        r, ang0 = 200, t * math.tau * 0.9
        for i in range(6):
            a = ang0 + i * math.tau / 6
            d.line([(cx + 40 * math.cos(a), cy + 40 * math.sin(a)),
                    (cx + (r - 14) * math.cos(a), cy + (r - 14) * math.sin(a))],
                   fill=domc, width=13)
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=domc, width=16)
        d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], outline=domc, width=10)
        a = ang0 + math.radians(72)
        d.ellipse([cx + (r - 12) * math.cos(a) - 18, cy + (r - 12) * math.sin(a) - 18,
                   cx + (r - 12) * math.cos(a) + 18, cy + (r - 12) * math.sin(a) + 18],
                  fill=INKS["SORANGE"])
    elif kind == "steam":
        for i in range(2):
            x0 = ax + aw * 0.6 + i * 70
            for k in range(11):
                p = (t * 2.2 + k * 0.09 + i * 0.5) % 1.0
                y = ay + ah * 0.62 - p * ah * 0.62
                x = x0 + 26 * math.sin(p * 9 + i * 2.4)
                r = 11 * (1 - p * 0.7)
                d.ellipse([x - r, y - r, x + r, y + r],
                          fill=mix(domc, subc, 0.15 + 0.4 * p))
    elif kind == "beak":
        p = e_in_out_quint(clamp01((t - 0.25) / 0.5))
        x = ax - 500 + p * (aw + 700)
        d.polygon([(x, ay + ah * 0.55), (x - 300, ay + ah * 0.62),
                   (x - 20, ay + ah * 0.70)], fill=INKS["SRED"])
        blink = 1 if (t * 10) % 1 > 0.12 else 0.25
        cx, cy = ax + aw * 0.78, ay + ah * 0.30
        d.ellipse([cx - 26, cy - 26, cx + 26, cy + 26], fill=domc)
        if blink:
            d.ellipse([cx - 44, cy - 44, cx + 44, cy + 44], outline=INKS["SRED"],
                      width=7)
    elif kind == "overprint":
        cx, cy = ax + aw * 0.7, ay + ah * 0.55
        off = 70 * math.sin(t * math.tau)
        m1 = Image.new("L", img.size, 0)
        ImageDraw.Draw(m1).ellipse([cx - 130, cy - 130, cx + 130, cy + 130],
                                   outline=255, width=34)
        m2 = Image.new("L", img.size, 0)
        ImageDraw.Draw(m2).ellipse([cx - 130 + off, cy - 130, cx + 130 + off,
                                    cy + 130], outline=255, width=34)
        both = ImageChops.multiply(m1, m2)
        img.paste(INKS["EBLUE"], (0, 0), m1)
        img.paste(INKS["CARBON"], (0, 0), m2)
        over = tuple((a * b) // 255 for a, b in zip(INKS["EBLUE"], INKS["CARBON"]))
        img.paste(over, (0, 0), both)
        d.ellipse([cx - 54 + off / 2, cy - 54, cx + 54 + off / 2, cy + 54],
                  fill=INKS["EBLUE"])
    elif kind == "marquee":
        word = "PAPER KEEPS THINGS · "
        f = F(SERIF_B, 190)
        w1 = int(f.getlength(word))
        x = -(int(t * w1 * 1.2) % w1)
        col = mix(INKS["CHARCOAL2"], subc, 0.82)
        d.text((x, ay + 60), word, font=f, fill=col)
        d.text((x + w1, ay + 60), word, font=f, fill=col)
        yy = ay + 400
        xx = ax
        while xx < ax + aw:
            d.rectangle([xx, yy, xx + 90, yy + 12], fill=INKS["MINT"])
            xx += 150
    elif kind == "pool":
        for row, (y0, sp) in enumerate(((ay + ah * 0.28, 120), (ay + ah * 0.45, -90))):
            off = (t * sp) % 46
            x = ax - 46 + off if sp > 0 else ax + aw - off
            while ax - 46 < x < ax + aw + 46:
                d.ellipse([x - 11, y0 - 11, x + 11, y0 + 11], fill=INKS["SRED"])
                x += 46 if sp > 0 else -46
        cx = ax + aw * 0.72
        cy = ay + ah * 0.62 + 14 * math.sin(t * math.tau)
        d.ellipse([cx - 110, cy - 110, cx + 110, cy + 110], outline=INKS["SRED"],
                  width=52)
    elif kind == "moon":
        cx, cy = ax + aw * 0.75, ay + 430
        R = 120
        d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=domc)
        a = t * math.tau * 0.8
        ox, oy = 60 * math.cos(a), 60 * math.sin(a)
        d.ellipse([cx - R * 0.82 + ox, cy - R * 0.82 + oy,
                   cx + R * 0.82 + ox, cy + R * 0.82 + oy], fill=subc)
        for i in range(9):
            sx = ax + 30 + (i * 173 % int(aw - 40))
            sy = ay + 30 + (i * 97 % 220)
            r = 3 + 2 * abs(math.sin(t * math.tau * (1 + i * 0.3) + i))
            d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=mix(domc, subc, 0.35))
    elif kind == "road":
        x0, y0 = ax + aw * 0.9, ay + ah * 0.15
        for i in range(14):
            p = ((i / 14) + t * 0.55) % 1.0
            x = x0 - p * aw * 1.0
            y = y0 + p * ah * 0.7
            d.rectangle([x - 5, y, x + 5, y + 26], fill=mix(domc, subc, 0.15))
        km = int(round(26 * (1 - clamp01(t * 1.25))))
        d.text((ax + 40, ay + ah * 0.72), f"{km:02d} KM TO TOWN", font=F(MONO, 44),
               fill=domc)


# ---------------------------------------------------------------- chapters
def draw_chapter(img, d, post, idx, t):
    base, fname, dom, acc, sub, lines, tfont, tsize, kicker, motif_kind = post
    subc = SUBS[sub]
    domc = INKS[dom]
    accc = INKS[acc] if acc else mix(domc, subc, 0.45)

    side_right = idx % 2 == 0  # poster on the right for even idx
    # poster stamps in
    tin = clamp01(t / 0.38)
    scale = 1.16 - 0.16 * e_out_expo(tin)
    pw, ph = int(PW * scale), int(PH * scale)
    pimg = base.resize((pw, ph), Image.BILINEAR)
    px = (W - pw - 150) if side_right else (150 + (PW - pw) // 2)
    px = int((W - pw) * (0.78 if side_right else 0.22))
    py = int((H - ph) / 2 + 10)
    img.paste(pimg, (px, py))

    # type block on the other side
    ax = 110 if side_right else W - 110 - 640
    area = (int(ax), 210, 640, 660)
    # motif layer sits under the type so phrases always stay readable
    if t > 0.22:
        motif(img, d, motif_kind, dom, acc, sub, t, area)
    y = 250
    for i, line in enumerate(lines):
        kinetic(img, ax, y, line, tfont, tsize, domc if i % 2 == 0 else accc,
                t - 0.10 - i * 0.10, hold=0.5)
        y += int(tsize * 1.02)
    # kicker + hex chips
    if t > 0.34:
        kinetic(img, ax, y + 26, kicker, MONO, 24, INKS["CHARCOAL"],
                t - 0.34, hold=0.4)
        chx = ax
        for i, c in enumerate([domc] + ([accc] if acc else [])):
            d.rectangle([chx, y + 84, chx + 44, y + 128], outline=INKS["CHARCOAL"],
                        width=2)
            d.rectangle([chx + 4, y + 88, chx + 40, y + 124], fill=c)
            tracked(d, (chx, y + 140), "#%02X%02X%02X" % c, MONO, 16,
                    INKS["CHARCOAL"], 0)
            chx += 150
    # giant chapter numeral, half-cropped at the frame edge
    f = F(SERIF_B, 560)
    nx = (W - 36) if side_right else 36
    d.text((nx - (0 if side_right else int(f.getlength(f"{idx+1:02d}"))), 540),
           f"{idx+1:02d}", font=f, fill=mix(domc, subc, 0.80))


# ---------------------------------------------------------------- wall
def load_thumbs():
    out = []
    for p in POSTERS:
        out.append(Image.open(os.path.join(GAL, p[0])).convert("RGB")
                   .resize((330, 440), Image.LANCZOS))
    return out


def shot_wall(img, d, t, thumbs):
    cols, rows = 5, 2
    tw, th = 330, 440
    gx, gy = 26, 26
    x0 = (W - cols * tw - (cols - 1) * gx) / 2
    y0 = (H - rows * th - (rows - 1) * gy) / 2 + 14
    import random as _r
    rng = _r.Random(7)
    for i, th_img in enumerate(thumbs):
        lt = clamp01((t - 0.04 - i * 0.045) / 0.42)
        if lt <= 0:
            continue
        e = e_out_back(lt)
        gxpos = x0 + (i % cols) * (tw + gx)
        gypos = y0 + (i // cols) * (th + gy)
        sx = gxpos + (rng.uniform(-1, 1)) * 900 * (1 - e)
        sy = gypos + (rng.uniform(-1, 1)) * 1200 * (1 - e)
        img.paste(th_img, (int(sx), int(sy)))
    if t > 0.55:
        kinetic(img, W / 2 - text_w(d, "THE FULL RUN — EVERY PLATE, ONE JOB",
                                    MONO, 26, 6) / 2, 96,
                "THE FULL RUN — EVERY PLATE, ONE JOB", MONO, 26,
                INKS["CHARCOAL"], (t - 0.55) / 0.1, hold=0.8)


# ---------------------------------------------------------------- outro
SEEDS = [hashlib.md5(s.encode()).hexdigest()[:8] for s in
         ["fern|the archive of green", "night market|lanterns lit at dusk",
          "night ride|midnight ride", "tea|still steaming", "gull|no rent",
          "sound check|sound check", "paper keeps things|paper keeps things",
          "public pool|the pool is open", "moon phases|three moods",
          "summer walk|walk until the town ends"]]


def shot_outro(img, d, t):
    bgc = INKS["CHARCOAL2"]
    paperc, mint = SUBS["white"], INKS["MINT"]
    # giant title with a mint channel sweeping through it (lighthouse callback)
    f = F(SERIF_B, 250)
    word = "MONO-COLOR"
    wt = f.getlength(word)
    x = (W - wt) / 2
    y = 280
    d.text((x, y), word, font=f, fill=paperc)
    band_y = -140 + t * (H + 400)
    d.rectangle([0, band_y, W, band_y + 96], fill=bgc)
    tmp = Image.new("L", img.size, 0)
    ImageDraw.Draw(tmp).text((x, y), word, font=f, fill=255)
    band = Image.new("L", img.size, 0)
    ImageDraw.Draw(band).rectangle([0, band_y, W, band_y + 96], fill=255)
    minttext = Image.new("RGB", img.size, mint)
    img.paste(minttext, (0, 0), ImageChops.multiply(tmp, band))
    if t > 0.25:
        kinetic(img, 120, 700, "same seed → same pixels", SERIF, 72, mint,
                (t - 0.25) / 0.1, hold=0.5)
        kinetic(img, 120, 800, "sha256-verified · byte-identical on every run",
                MONO, 26, paperc, (t - 0.4) / 0.1, hold=0.6)
        kinetic(img, 120, 850, "rendered in code — pillow + ffmpeg, no generative imagery",
                MONO, 26, paperc, (t - 0.5) / 0.1, hold=0.6)
    # scrolling seed ticker
    tick = " · ".join(s for s in SEEDS) + " · "
    ft = F(MONO, 22)
    w1 = int(ft.getlength(tick))
    off = int(t * 260) % w1
    col = mix(paperc, bgc, 0.55)
    for xx in (-off, -off + w1, -off + 2 * w1):
        d.text((xx, 960), tick, font=ft, fill=col)
    if t > 0.7:
        tracked(d, (W - 120, 890), "REEL 01 — 2026", MONO, 24, mint, 4,
                anchor="right")
    reg_mark(d, 960, 160, mint)


# ---------------------------------------------------------------- main
def render(out_path="mono-color-reel.mp4"):
    global GRAIN
    GRAIN = make_grain()
    posters = load_posters()
    thumbs = load_thumbs()

    chapters = [(f"ch{i:02d}", 87, (lambda p=pt, k=i: (lambda img, d, t:
                        draw_chapter(img, d, p, k, t)))(), False, True)
                for i, pt in enumerate(posters)]
    shots = [("open", 100, shot_open, False, True),
             ("catalog", 108, shot_catalog, False, True),
             *chapters,
             ("wall", 130, lambda img, d, t: shot_wall(img, d, t, thumbs),
              False, False),
             ("outro", 118, shot_outro, True, False)]

    writer = imageio.get_writer(out_path, fps=FPS, codec="libx264",
                                pixelformat="yuv420p", macro_block_size=1,
                                ffmpeg_params=["-crf", "18"])
    WIPE = 7
    prev_final = None
    chapter_idx = None
    gi = 0
    for name, n, fn, dark, show_reg in shots:
        if name.startswith("ch"):
            chapter_idx = int(name[2:])
        else:
            chapter_idx = None
        ticket = ("GALLERY PASS — ALL PLATES" if name == "wall"
                  else "END SLATE — JOB COMPLETE" if name == "outro"
                  else "MONO-COLOR — DETERMINISTIC PRINT SYSTEM")
        for i in range(n):
            t = i / (n - 1)
            if prev_final is not None and i == 0:
                img = Image.new("RGB", (W, H), INKS["CHARCOAL2"])  # plate flash
                d = ImageDraw.Draw(img)
            elif prev_final is not None and 0 < i < WIPE:
                p = e_in_out_quint((i - 1) / (WIPE - 1))
                x = min(int(p * (W + 120)), W)
                scene = Image.new("RGB", (W, H), SUBS["white"])
                fn(scene, ImageDraw.Draw(scene), t)
                img = prev_final.copy()
                img.paste(scene.crop((0, 0, x, H)), (0, 0))
                d = ImageDraw.Draw(img)
                if x < W:
                    d.rectangle([x - 14, 0, x, H], fill=INKS["CHARCOAL2"])
            else:
                img = Image.new("RGB", (W, H),
                                INKS["CHARCOAL2"] if name == "outro"
                                else SUBS["white"])
                d = ImageDraw.Draw(img)
                fn(img, d, t)
            overlays(img, d, chapter_idx, t, ticket, dark, show_reg)
            img = add_grain(img, gi)
            gi += 1
            writer.append_data(np.asarray(img))
        prev_final = img.copy()
    writer.close()
    print("wrote", out_path)


if __name__ == "__main__":
    render()
