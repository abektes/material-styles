"""Animated mono-color posters — seamless 3s loops, deterministic.

Each loop = the static poster + three motion layers, all print-logic:
1. accent-plate breathing: the accent ink is separated pixel-wise and
   re-stamped with an oscillating ~2px offset (misregistration, animated);
2. one native motion motif per poster (lanterns rise, wheel reflector orbits,
   ink pool ripples, water twinkles ...), seeded and periodic;
3. seeded grain tiles cycling (paper life).

Same seed -> same MP4. One-ink posters skip layer 1 (nothing to misregister).
"""
import hashlib
import math
import os
import random
import sys

import numpy as np
import imageio.v2 as imageio
from PIL import Image, ImageDraw, ImageFilter

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE + "/..")
os.chdir(_HERE + "/..")  # poster re-writes land in ./gallery, not animated/
import render_gallery as G  # noqa: E402

W, H = 1200, 1600
N_FRAMES = 90
FPS = 30
OUT = _HERE

# ---------------------------------------------------------------- helpers
def dist_arr(arr, c):
    return np.abs(arr - np.array(c, dtype=np.int16)).sum(axis=2)


def separate_accent(base, dom, acc, sub):
    """Split the accent ink into a movable plate. Returns (base_wo, plate_img,
    plate_mask) or (None, None, None) when separation is unsafe/empty.
    Pixels on or near dominant ink stay put (no holes punched in overprints)."""
    arr = np.asarray(base).astype(np.int16)
    d_dom, d_acc = dist_arr(arr, dom), dist_arr(arr, acc)
    d_sub, d_w = dist_arr(arr, sub), dist_arr(arr, (250, 250, 247))
    acc_mask = (d_acc + 25 < d_dom) & (d_sub > 40) & (d_w > 60)
    dom_mask = d_dom <= d_acc + 25
    near = np.asarray(Image.fromarray((dom_mask * 255).astype(np.uint8))
                      .filter(ImageFilter.MaxFilter(7))) > 128
    moving = acc_mask & ~near
    if moving.sum() < 500:
        return None, None, None
    mask = Image.fromarray((moving * 255).astype(np.uint8))
    wo = np.asarray(base).copy()
    wo[moving] = sub
    plate = Image.new("RGB", base.size, sub)
    plate.paste(base, (0, 0), mask)
    return Image.fromarray(wo), plate, mask


def seeded_grain(seed, n=4):
    rng = random.Random(seed)
    tiles = []
    for _ in range(n):
        b = rng.randbytes(W * H)
        g = Image.frombytes("L", (W, H), b)
        tiles.append(Image.merge("RGB", (g, g, g)))
    return tiles


def dot(d, x, y, r, c):
    d.ellipse([x - r, y - r, x + r, y + r], fill=c)


def ring(d, x, y, r, w, c):
    d.ellipse([x - r, y - r, x + r, y + r], outline=c, width=int(w))


def cross(d, x, y, r, w, c):
    ring(d, x, y, r, w, c)
    d.line([(x - r - 8, y), (x + r + 8, y)], fill=c, width=w)
    d.line([(x, y - r - 8), (x, y + r + 8)], fill=c, width=w)


def road_pt(pts, u):
    seg = max(0.0, min(0.999, u)) * (len(pts) - 1)
    j = min(int(seg), len(pts) - 2)
    lt = seg - j
    return (pts[j][0] + (pts[j + 1][0] - pts[j][0]) * lt,
            pts[j][1] + (pts[j + 1][1] - pts[j][1]) * lt,
            pts[j][2] + (pts[j + 1][2] - pts[j][2]) * lt)


ROAD = [(320, 1660, 330), (500, 1400, 255), (420, 1160, 195), (560, 980, 130),
        (500, 870, 72), (545, 800, 38)]

# ---------------------------------------------------------------- motifs
# Each motif: prep(seed) -> state ; draw(d, t, state). Periodic in t (period 1).


def m_fern(seed):
    rng = random.Random(seed)
    spores = [(rng.uniform(380, 980), rng.uniform(700, 1150),
               rng.uniform(30, 60), rng.uniform(-170, -120),
               rng.uniform(3, 5)) for _ in range(12)]
    leaves = [(rng.uniform(900, 1150), rng.uniform(300, 600),
               rng.uniform(-140, -90), rng.uniform(100, 150),
               rng.uniform(10, 18)) for _ in range(5)]

    def draw(d, t, s):
        for x0, y0, ax, ay, r in spores:
            k = (t + x0 / 1200 * 0.7) % 1.0
            dot(d, x0 + ax * k, y0 + ay * k, r * (1 - 0.4 * k), G.OXBLOOD)
        for x0, y0, ax, ay, r in leaves:
            k = (t + y0 / 1600 * 0.6) % 1.0
            x, y = x0 + ax * k, y0 + ay * k
            d.polygon([(x, y), (x + r * 0.8, y + r * 0.5), (x + r * 0.2, y + r)],
                      fill=G.mix(G.BG, G.BEIGE, 0.35))
    return draw, None


def m_market(seed):
    rng = random.Random(seed)
    lant = [(rng.uniform(120, 1080), rng.uniform(46, 62),
             rng.uniform(0, 1)) for _ in range(3)]

    def draw(d, t, s):
        for x0, r, ph in lant:
            k = (t + ph) % 1.0
            y = 1660 - k * 1500
            x = x0 + 14 * math.sin(2 * math.pi * (t * 2 + ph))
            d.ellipse([x - r - 9, y - r - 9, x + r + 9, y + r + 9], fill=G.WHITE)
            d.line([(x, y - r - 70), (x, y - r)], fill=G.TANGERINE, width=3)
            ring(d, x, y, r, 7, G.TANGERINE)
            d.rectangle([x - 7, y + r, x + 7, y + r + 20], fill=G.TANGERINE)
    return draw, None


def m_ride(seed):
    cx, cy, r = 880, 730, 444  # mid-rim of the baked wheel

    def draw(d, t, s):
        a = math.radians(72) + t * math.tau
        dot(d, cx + r * math.cos(a), cy + r * math.sin(a), 22, G.SORANGE)
        # marching dot along the baked route
        k = (t * 1.5) % 1.0
        x, y = 985 + k * 175, 650 - k * 380
        dot(d, x, y, 8 - 2 * k, G.SORANGE)
    return draw, None


def m_tea(seed):
    def draw(d, t, s):
        # ripples knocked out of the pooled table ink
        for k in range(3):
            p = (t + k / 3) % 1.0
            rx = 46 + p * 250
            box = [450 - rx, 1250 - rx * 0.30, 450 + rx, 1250 + rx * 0.30]
            col = G.mix(G.BEIGE, G.TERRA, 0.15 + 0.8 * p)
            d.arc(box, 190, 350, fill=col, width=max(2, int(6 - 4 * p)))
        # a drop falls from the spout, twice per loop
        for k in (0, 0.5):
            p = (t + k) % 0.5 / 0.5
            if p < 0.12:
                continue
            fp = (p - 0.12) / 0.88
            y = 700 + fp * fp * 520
            dot(d, 893, y, 7 - 2 * fp, G.TERRA)
    return draw, None


def m_gull(seed):
    def draw(d, t, s):
        # eye blink (twice per loop)
        b = (t * 2) % 1.0
        if 0.40 < b < 0.50:
            dot(d, 1090, 610, 34, G.WHITE)
            d.rectangle([1062, 604, 1118, 614], fill=G.CHARCOAL)
        # distant gulls drift across the gray field
        for i, y0 in enumerate((150, 235)):
            x = ((t * 200 + i * 640) % 1400) - 100
            for j in range(2):
                bx = x + j * 44
                d.arc([bx - 22, y0 - 20, bx + 22, y0 + 20], 180, 360,
                      fill=G.CHARCOAL, width=5)
    return draw, None


def m_sound(seed):
    cx, cy, r = 320, 840, 520  # carbon circle geometry from the poster

    def draw(d, t, s):
        over = tuple((a_ * b_) // 255 for a_, b_ in zip(G.EBLUE, G.CARBON))
        for ph, rr in ((0.0, 26), (math.pi, 16)):
            a = t * math.tau + ph
            # orbit radius breathes through the disc edge so the dot
            # genuinely enters the overprint zone (multiply color)
            ro = r + 190 * math.sin(2 * math.pi * t + ph)
            x, y = cx + ro * math.cos(a), cy + ro * math.sin(a)
            inside = math.hypot(x - cx, y - cy) < r - rr
            dot(d, x, y, rr, over if inside else G.EBLUE)
    return draw, None


def m_paper(seed):
    rng = random.Random(seed)
    marks = [(rng.uniform(140, 1100), rng.uniform(1380, 1520),
              rng.uniform(0, 1)) for _ in range(3)]

    def draw(d, t, s):
        for x0, y0, ph in marks:
            cross(d, x0 + 10 * math.sin(2 * math.pi * t + ph),
                  y0 + 8 * math.cos(2 * math.pi * t + ph), 13, 4, G.MINT)
    return draw, None


def m_pool(seed):
    rng = random.Random(seed)
    pts = []
    while len(pts) < 22:
        x, y = rng.uniform(100, 1100), rng.uniform(770, 1360)
        if 690 < x < 1080 and 1020 < y < 1360:
            continue  # keep the float zone clean
        pts.append((x, y, rng.uniform(0, 1)))

    def draw(d, t, s):
        for x, y, ph in pts:
            r = 2.5 + 3.5 * abs(math.sin(2 * math.pi * t + ph * 6.28))
            dot(d, x, y, r, G.WHITE)
    return draw, None


def m_moon(seed):
    rng = random.Random(seed)
    stars = [(rng.uniform(70, 480), rng.uniform(390, 790),
              rng.uniform(0, 1)) for _ in range(8)]

    def draw(d, t, s):
        pale = G.mix(G.AUB, G.BEIGE, 0.5)
        for x, y, ph in stars:
            r = 2 + 3 * abs(math.sin(2 * math.pi * t + ph * 6.28))
            dot(d, x, y, r, pale)
        # one shooting star per loop, upper left
        p = (t - 0.55) / 0.3
        if 0 <= p <= 1:
            e = p * p * (3 - 2 * p)
            x, y = 700 - 560 * e, 170 + 260 * e
            dot(d, x, y, 5, pale)
            d.line([(x, y), (x + 44, y - 20)], fill=pale, width=3)
    return draw, None


def m_walk(seed):
    def draw(d, t, s):
        # traffic dashes flowing down the road ribbon
        for k in range(5):
            u = (0.98 - (t * 0.45 + k * 0.09)) % 0.85 + 0.13
            x, y, w = road_pt(ROAD, u)
            dot(d, x, y, max(2.5, w * 0.09), G.WHITE)
        # sun shimmer ring
        r = 236 + 9 * math.sin(2 * math.pi * t)
        ring(d, 950, 300, r, 4, G.mix(G.ROYAL, G.WHITE, 0.55))
    return draw, None


MOTIFS = {"01-fern-archive": m_fern, "02-night-market": m_market,
          "03-midnight-ride": m_ride, "04-still-steaming": m_tea,
          "05-harbour-gull": m_gull, "06-sound-check": m_sound,
          "07-paper-keeps": m_paper, "08-the-pool": m_pool,
          "09-night-log": m_moon, "10-the-long-way": m_walk}

POSTER_FNS = [G.p01_fern, G.p02_market, G.p03_ride, G.p04_tea, G.p05_gull,
              G.p06_sound, G.p07_paper, G.p08_pool, G.p09_moons, G.p10_walk]

META = {  # slug -> (dom, acc|None, substrate)
    "01-fern-archive": (G.BG, G.OXBLOOD, G.BEIGE),
    "02-night-market": (G.TANGERINE, G.SLATE, G.WHITE),
    "03-midnight-ride": (G.ULTRA, G.SORANGE, G.WHITE),
    "04-still-steaming": (G.TERRA, None, G.BEIGE),
    "05-harbour-gull": (G.CHARCOAL, G.SRED, G.GRAY),
    "06-sound-check": (G.CARBON, G.EBLUE, G.WHITE),
    "07-paper-keeps": (G.CHARCOAL2, G.MINT, G.GRAY),
    "08-the-pool": (G.POWDER, G.SRED, G.WHITE),
    "09-night-log": (G.AUB, None, G.BEIGE),
    "10-the-long-way": (G.ROYAL, None, G.WHITE),
}


def stable_seed(slug):
    return int(hashlib.md5(("anim|" + slug).encode()).hexdigest()[:8], 16)


def render_one(slug, fn, dom, acc, sub):
    res = fn()
    base = Image.open(res["path"]).convert("RGB")
    seed = stable_seed(slug)
    draw_motif, _ = MOTIFS[slug](seed + 1)
    plate = None
    if acc is not None:
        wo, p_img, p_mask = separate_accent(base, dom, acc, sub)
        if wo is not None:
            plate = (wo, p_img, p_mask)
    grain = seeded_grain(seed + 2)

    def frame_gen():
        for i in range(N_FRAMES):
            t = i / N_FRAMES
            if plate:
                frame = plate[0].copy()
                ox = int(2.2 * math.cos(2 * math.pi * t))
                oy = int(2.2 * math.sin(2 * math.pi * t))
                frame.paste(plate[1], (ox, oy), plate[2])
            else:
                frame = base.copy()
            d = ImageDraw.Draw(frame)
            draw_motif(d, t, None)
            frame = Image.blend(frame, grain[i % 4], 0.035)
            yield frame

    return frame_gen


def main():
    import os
    os.makedirs(OUT, exist_ok=True)
    order = list(MOTIFS.keys())

    # pass 1: individual loops
    for slug, fn in zip(order, POSTER_FNS):
        dom, acc, sub = META[slug]
        gen = render_one(slug, fn, dom, acc, sub)
        path = f"{OUT}/{slug}-loop.mp4"
        w = imageio.get_writer(path, fps=FPS, codec="libx264",
                               pixelformat="yuv420p", macro_block_size=1,
                               ffmpeg_params=["-crf", "22"])
        for frame in gen():
            w.append_data(np.asarray(frame))
        w.close()
        print("wrote", path, flush=True)

    # pass 2: combined 5x2 animated contact sheet (thumbs cached small)
    TW, TH, GAP = 384, 512, 12
    sheet_w, sheet_h = 5 * TW + 4 * GAP, 2 * TH + GAP
    grids = []
    for slug, fn in zip(order, POSTER_FNS):
        dom, acc, sub = META[slug]
        gen = render_one(slug, fn, dom, acc, sub)
        grids.append([f.resize((TW // 2, TH // 2), Image.BILINEAR)
                      for f in gen()])
    w = imageio.get_writer(f"{OUT}/all-posters-loop.mp4", fps=FPS,
                           codec="libx264", pixelformat="yuv420p",
                           macro_block_size=1, ffmpeg_params=["-crf", "22"])
    for i in range(N_FRAMES):
        sheet = Image.new("RGB", (sheet_w, sheet_h), (250, 250, 247))
        for gi, frames in enumerate(grids):
            im = frames[i].resize((TW, TH), Image.BILINEAR)
            sheet.paste(im, (GAP + (gi % 5) * (TW + GAP),
                             GAP + (gi // 5) * (TH + GAP)))
        w.append_data(np.asarray(sheet))
    w.close()
    print("wrote all-posters-loop.mp4", flush=True)


if __name__ == "__main__":
    main()
