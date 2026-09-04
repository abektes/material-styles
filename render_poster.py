#!/usr/bin/env python3
"""Deterministic mono-color renderer experiment.

Implements the mono-color skill's Recipe Manifest as code instead of an
image-generation prompt. All values come from design-system/*.json:
- palette_cobalt_terracotta  (#2148B8 + #C65F38) on substrate_neutral_white (#FAFAF7)
- composition_editorial_cover, tension_relaxed
- type_literary display + grotesk micro + mono data
- 2 contemporary imperfections: halftone drift 7%, registration drift ~1.5mm
- stable seed = md5(subject|text|palette|layout)
"""
import hashlib
import random
import sys

from PIL import Image, ImageDraw, ImageFont

S = 2                       # supersample factor
W, H = 1200 * S, 1600 * S   # 3:4 vertical poster

SUBSTRATE = (0xFA, 0xFA, 0xF7)
COBALT = (0x21, 0x48, 0xB8)
TERRA = (0xC6, 0x5F, 0x38)

RECIPE = "lighthouse|the light rotates anyway|palette_cobalt_terracotta|composition_editorial_cover"
SEED = int(hashlib.md5(RECIPE.encode()).hexdigest()[:8], 16)
rng = random.Random(SEED)

DRIFT = (10, 6)  # registration drift (~1.5mm at print scale), accent plate only
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size_1x):
    return ImageFont.truetype(FONT_DIR + name, int(size_1x * S))


def in_poly(x, y, poly):
    """Ray-casting point-in-polygon on supersampled coords."""
    inside = False
    n = len(poly)
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        if (y1 > y) != (y2 > y):
            xin = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
            if x < xin:
                inside = not inside
    return inside


img = Image.new("RGB", (W, H), SUBSTRATE)
d = ImageDraw.Draw(img)

# ---------------- plate geometry ----------------

# light path on the water: terracotta wedge under the tower, fading with depth
refl_poly = [(575 * S, 1186 * S), (625 * S, 1186 * S), (700 * S, 1230 * S), (500 * S, 1230 * S)]
# beam: solid core trapezoid + screened tail continuing the same edges
beam_core = [(620 * S, 196 * S), (980 * S, 25 * S), (980 * S, 495 * S), (620 * S, 246 * S)]
beam_tail = [(980 * S, 25 * S), (1100 * S, -15 * S), (1100 * S, 480 * S), (980 * S, 495 * S)]

# ---------------- cobalt plate: structure (no drift) ----------------

# sea: halftone gradient deepening from the horizon, ink pooling solid below 1265;
# dots inside the reflection wedge are skipped so the accent plate butt-fits
PITCH = 23 * S
row = 0
for y in range(int(1185 * S), int(1235 * S), PITCH):
    t = (y / S - 1180) / 55
    r = (5.5 + 13 * t ** 1.15) * S
    off = (PITCH // 2) if row % 2 else 0
    row += 1
    for x in range(off, W, PITCH):
        if in_poly(x, y, refl_poly):
            continue
        rr = r * (1 + rng.uniform(-0.07, 0.07))
        d.ellipse([x - rr, y - rr, x + rr, y + rr], fill=COBALT)
d.rectangle([0, 1240 * S, W, H], fill=COBALT)

# pale halftone field, upper-left quiet texture fading before the headline
row = 0
for y in range(int(150 * S), int(500 * S), 20 * S):
    off = (10 * S) if row % 2 else 0
    row += 1
    for x in range(int(84 * S) + off, int(500 * S), 20 * S):
        dist = ((x - 84 * S) ** 2 + (y - 150 * S) ** 2) ** 0.5 / S
        if dist > 420:
            continue
        r = 5 * max(0.0, 1 - dist / 420) ** 0.9 * S
        r *= 1 + rng.uniform(-0.07, 0.07)
        if r < 0.5 * S:
            continue
        d.ellipse([x - r, y - r, x + r, y + r], fill=COBALT)

# horizon rule bleeding both side edges
d.line([0, 1180 * S, W, 1180 * S], fill=COBALT, width=3 * S)


def tower_edges(y1x):
    t = (y1x - 274) / (1210 - 274)
    return 490 - 205 * t, 710 + 205 * t


# tower mass
tower_poly = [(280 * S, 1210 * S), (920 * S, 1210 * S), (710 * S, 274 * S), (490 * S, 274 * S)]
tower_mask = Image.new("L", (W, H), 0)
tm = ImageDraw.Draw(tower_mask)
tm.polygon(tower_poly, fill=255)
img.paste(COBALT, (0, 0), tower_mask)

# headline channel: paper knocked through the full tower width, carrying the type
l0, r0 = tower_edges(530)
l1, r1 = tower_edges(1115)
d.polygon([(l0 * S, 530 * S), (r0 * S, 530 * S), (r1 * S, 1115 * S), (l1 * S, 1115 * S)],
          fill=SUBSTRATE)

# paper stripe bands above the channel (plate knockouts)
for y0, y1 in [(345, 400), (480, 535)]:
    a0, b0 = tower_edges(y0)
    a1, b1 = tower_edges(y1)
    d.polygon([(a0 * S, y0 * S), (b0 * S, y0 * S), (b1 * S, y1 * S), (a1 * S, y1 * S)],
              fill=SUBSTRATE)

# gallery slab and dome
d.rectangle([460 * S, 250 * S, 740 * S, 276 * S], fill=COBALT)
d.ellipse([555 * S, 128 * S, 645 * S, 196 * S], fill=COBALT)
d.rectangle([597 * S, 96 * S, 603 * S, 132 * S], fill=COBALT)

# headline, Literary serif, tight leading, locked into the channel across the tower
display = font("DejaVuSerif.ttf", 200)
for i, line in enumerate(["the light", "rotates", "anyway"]):
    d.text((168 * S, (535 + i * 200) * S), line, font=display, fill=COBALT)

# microcopy + data strip
micro = font("DejaVuSans.ttf", 17)
mono = font("DejaVuSansMono.ttf", 15)


def tracked(xy, text, fnt, fill, tr_1x):
    x, y = xy[0] * S, xy[1] * S
    for ch in text:
        d.text((x, y), ch, font=fnt, fill=fill)
        x += d.textlength(ch, font=fnt) + tr_1x * S


tracked((84, 96), "FIELD NOTES — NORTH ATLANTIC", micro, COBALT, 6)
# coordinates knocked out of the pooled ink; date sits on the accent plate above it
d.text((84 * S, 1462 * S), "54.6°N 8.4°E — FL.W 5S", font=mono, fill=SUBSTRATE)
d.text((1116 * S - d.textlength("SEP 2026 — NO. 07", font=mono), 1126 * S),
       "SEP 2026 — NO. 07", font=mono, fill=TERRA)

# ---------------- terracotta plate: light + annotation (with drift) ----------------

dx, dy = DRIFT

# lamp room solid, paper mullions
d.rectangle([(545 + dx / 2) * S, (170 + dy / 2) * S,
             (655 + dx / 2) * S, (252 + dy / 2) * S], fill=TERRA)
for mx in (583, 609):
    d.rectangle([(mx + dx / 2) * S, (170 + dy / 2) * S,
                 (mx + 8 + dx / 2) * S, (252 + dy / 2) * S], fill=SUBSTRATE)

# beam: solid core + screened tail fading before the right frame (unresolved edge)
d.polygon([(x + dx, y + dy) for x, y in beam_core], fill=TERRA)
BP = 20 * S
row = 0
for y in range(int(60 * S), int(470 * S), BP):
    off = (BP // 2) if row % 2 else 0
    row += 1
    for x in range(int(995 * S) + off, int(1095 * S), BP):
        t = (x / S - 980) / 120
        r = 13 * max(0.0, 1 - t) * S
        r *= 1 + rng.uniform(-0.07, 0.07)
        if r < 0.6 * S or not in_poly(x, y, [(px + dx, py + dy) for px, py in beam_tail]):
            continue
        d.ellipse([x - r, y - r, x + r, y + r], fill=TERRA)

# light path reflected on the sea, fading with depth
row = 0
for y in range(int(1196 * S), int(1225 * S), 21 * S):
    t = (y / S - 1186) / 42
    r = (11 - 7 * t) * S
    off = (21 * S // 2) if row % 2 else 0
    row += 1
    for x in range(int(505 * S) + off, int(695 * S), 21 * S):
        if not in_poly(x, y, refl_poly):
            continue
        rr = r * (1 + rng.uniform(-0.07, 0.07))
        d.ellipse([x - rr + dx, y - rr + dy, x + rr + dx, y + rr + dy], fill=TERRA)

# one manual gesture: a circled aside in the quiet zone below the beam
note = font("DejaVuSerif.ttf", 27)
d.text((920 * S, 545 * S), "checked nightly", font=note, fill=TERRA)
loop = Image.new("L", (300 * S, 110 * S), 0)
ld = ImageDraw.Draw(loop)
ld.ellipse([6 * S, 6 * S, 294 * S, 104 * S], outline=255, width=3 * S)
loop = loop.rotate(3, expand=True, resample=Image.BICUBIC)
img.paste(TERRA, (int(880 * S) + dx, int(512 * S) + dy), loop)

# ---------------- output + metrics ----------------

final = img.resize((1200, 1600), Image.LANCZOS)
out = sys.argv[1] if len(sys.argv) > 1 else "lighthouse-monocolor.png"
final.save(out)

small = final.resize((300, 400))
data = list(small.getdata())
inked = cob = ter = 0
for p in data:
    if abs(p[0] - SUBSTRATE[0]) + abs(p[1] - SUBSTRATE[1]) + abs(p[2] - SUBSTRATE[2]) > 36:
        inked += 1
        dc = sum(abs(p[i] - COBALT[i]) for i in range(3))
        dt = sum(abs(p[i] - TERRA[i]) for i in range(3))
        if dc < dt:
            cob += 1
        else:
            ter += 1
total = len(data)
print(f"seed={SEED}")
print(f"empty_paper={100 * (total - inked) / total:.1f}%  (gate 25-55, family 25-45)")
print(f"accent_share_of_ink={100 * ter / max(1, inked):.1f}%  (target 15-30)")
print(f"dominant_share_of_ink={100 * cob / max(1, inked):.1f}%")
