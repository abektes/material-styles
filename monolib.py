"""Shared deterministic rendering primitives for the mono-color gallery.

All layout coordinates are in 1x space (1200x1600); everything is scaled by
S internally for supersampling. Inks are exact catalog hexes; imperfections
( registration drift, halftone drift, density jitter ) are seeded per recipe.
"""
import hashlib
import random
import warnings

from PIL import Image, ImageChops, ImageDraw, ImageFont

warnings.filterwarnings("ignore")

S = 2
W, H = 1200 * S, 1600 * S
UW, UH = 1200, 1600
FONT_DIR = "/usr/share/fonts/truetype/dejavu/"

SUBSTRATES = {
    "white": (0xFA, 0xFA, 0xF7),
    "gray": (0xE9, 0xE9, 0xE5),
    "beige": (0xF5, 0xF1, 0xE8),
}


def mix(c1, c2, t):
    return tuple(int(a + (b - a) * t) for a, b in zip(c1, c2))


def seed_of(recipe):
    return int(hashlib.md5(recipe.encode()).hexdigest()[:8], 16)


class Poster:
    def __init__(self, slug, substrate, inks, recipe):
        self.slug = slug
        self.sub = SUBSTRATES[substrate]
        self.inks = inks  # [dominant] or [dominant, accent]
        self.seed = seed_of(recipe)
        self.rng = random.Random(self.seed)
        self.img = Image.new("RGB", (W, H), self.sub)
        self.d = ImageDraw.Draw(self.img)
        m = self.rng.randint(0, 359)
        import math
        self.drift = (int(math.cos(math.radians(m)) * 3), int(math.sin(math.radians(m)) * 3))

    # ---------- geometry ----------
    def sc(self, *vals):
        return [v * S for v in vals]

    def poly(self, pts, ink):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=ink)

    def rect(self, x0, y0, x1, y1, ink):
        self.d.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=ink)

    def ell(self, x0, y0, x1, y1, ink, outline=False, width=1):
        box = [x0 * S, y0 * S, x1 * S, y1 * S]
        if outline:
            self.d.ellipse(box, outline=ink, width=int(width * S))
        else:
            self.d.ellipse(box, fill=ink)

    def dot(self, x, y, r, ink):
        if r * S < 0.5:
            return
        self.d.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=ink)

    def ring(self, cx, cy, r, w, ink):
        self.d.ellipse([(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
                       outline=ink, width=int(w * S))

    def line(self, pts, ink, w):
        self.d.line([(x * S, y * S) for x, y in pts], fill=ink, width=int(w * S))

    # ---------- masks ----------
    def raw_layer(self, fn):
        """fn receives a full-res ImageDraw on an L mask; draw with *S coords."""
        m = Image.new("L", (W, H), 0)
        fn(ImageDraw.Draw(m))
        return m

    def layer(self, fn):
        m = Image.new("L", (W, H), 0)
        dm = ImageDraw.Draw(m)
        class L:
            @staticmethod
            def poly(pts):
                dm.polygon([(x * S, y * S) for x, y in pts], fill=255)
            @staticmethod
            def rect(x0, y0, x1, y1):
                dm.rectangle([x0 * S, y0 * S, x1 * S, y1 * S], fill=255)
            @staticmethod
            def ell(x0, y0, x1, y1):
                dm.ellipse([x0 * S, y0 * S, x1 * S, y1 * S], fill=255)
            @staticmethod
            def text(x, y, s, fname, size):
                dm.text((x * S, y * S), s, font=font(fname, size), fill=255)
        fn(L)
        return m

    def stamp(self, mask, ink, ox=0, oy=0):
        self.img.paste(ink, (int(ox * S), int(oy * S)), mask)

    def stamp_where(self, mask, cond_mask, ink):
        """Paste ink only where mask AND cond_mask."""
        self.img.paste(ink, (0, 0), ImageChops.multiply(mask, cond_mask))

    def knock(self, mask, ox=0, oy=0):
        self.stamp(mask, self.sub, ox, oy)

    # ---------- halftone ----------
    def halftone(self, x0, y0, x1, y1, pitch, r_fn, region_fn, ink,
                 jitter=0.07, drift=(0, 0)):
        pitch *= S
        row = 0
        yy = y0 * S
        while yy < y1 * S:
            off = (pitch // 2) if row % 2 else 0
            row += 1
            xx = x0 * S + off
            while xx < x1 * S:
                if region_fn(xx / S, yy / S):
                    r = r_fn(xx / S, yy / S)
                    if r and r > 0:
                        r *= 1 + self.rng.uniform(-jitter, jitter)
                        self.dot(xx / S + drift[0], yy / S + drift[1], r, ink)
                xx += pitch
            yy += pitch

    # ---------- type ----------
    def text(self, xy, s, fname, size, ink, tracking=0, anchor_x="left"):
        f = font(fname, size)
        wpx = self.text_w(s, fname, size, tracking)
        x = xy[0] if anchor_x == "left" else (xy[0] - wpx if anchor_x == "right" else xy[0] - wpx / 2)
        x = int(x)
        if tracking:
            cx = x * S
            for ch in s:
                self.d.text((cx, xy[1] * S), ch, font=f, fill=ink)
                cx += self.d.textlength(ch, font=f) + tracking * S
        else:
            self.d.text((x * S, xy[1] * S), s, font=f, fill=ink)

    def text_w(self, s, fname, size, tracking=0):
        f = font(fname, size)
        w = sum(self.d.textlength(ch, font=f) for ch in s)
        return (w + tracking * S * max(0, len(s) - 1)) / S

    def vtext(self, xy, s, fname, size, ink):
        """90-degree rotated (bottom-to-top) text with top-left at xy."""
        f = font(fname, size)
        tmp = Image.new("L", (int(self.d.textlength(s, font=f)) + 40 * S, int(f.size) + 40 * S), 0)
        ImageDraw.Draw(tmp).text((20 * S, 20 * S), s, font=f, fill=255)
        tmp = tmp.rotate(90, expand=True)
        self.img.paste(ink, (int(xy[0] * S), int(xy[1] * S)), tmp)

    def greek(self, x, y, w, h, lines, ink, lw=6, lh=None):
        """Greeked text-block texture: rows of bars with word gaps."""
        lh = lh or (lw * 2.1)
        row = y
        n = 0
        while row < y + h and n < lines:
            cx = x
            while cx < x + w - lw * 2:
                word = self.rng.uniform(2.2, 5.2) * lw
                if cx + word > x + w:
                    break
                self.rect(cx, row, cx + word, row + lw, ink)
                cx += word + lw * self.rng.uniform(0.9, 1.6)
            row += lh
            n += 1

    def circled_note(self, text, x, y, fname, size, ink, pad=14, rot=3):
        f = font(fname, size)
        tw = self.text_w(text, fname, size)
        self.d.text((x * S, y * S), text, font=f, fill=ink)
        lw_, lh_ = int((tw + 2 * pad) * S), int((size * 1.6 + 2 * pad) * S)
        loop = Image.new("L", (lw_, lh_), 0)
        ImageDraw.Draw(loop).ellipse([3 * S, 3 * S, lw_ - 3 * S, lh_ - 3 * S],
                                     outline=255, width=3 * S)
        loop = loop.rotate(rot, expand=True, resample=Image.BICUBIC)
        self.img.paste(ink, (int((x - pad) * S) + self.drift[0],
                             int((y - size * 0.45 - pad) * S) + self.drift[1]), loop)

    def reg_mark(self, cx, cy, ink, r=16):
        self.ring(cx, cy, r, 2.2, ink)
        self.line([(cx - r - 8, cy), (cx + r + 8, cy)], ink, 2.2)
        self.line([(cx, cy - r - 8), (cx, cy + r + 8)], ink, 2.2)

    # ---------- output ----------
    def finish(self, outdir="gallery", extra=(), zmask=None):
        """Report pixel-based and silhouette-based empty-paper percentages.

        zmask: full-res L mask of the composed content silhouettes (object
        zones, type bands); zone_empty = canvas minus composed zones."""
        import os
        os.makedirs(outdir, exist_ok=True)
        final = self.img.resize((UW, UH), Image.LANCZOS)
        path = f"{outdir}/{self.slug}.png"
        final.save(path)
        small = final.resize((300, 400))
        data = list(small.getdata())
        counts = [0] * len(self.inks)
        inked = 0
        for p in data:
            if sum(abs(p[i] - self.sub[i]) for i in range(3)) > 36:
                if any(sum(abs(p[i] - e[i]) for i in range(3)) <= 36 for e in extra):
                    continue
                inked += 1
                dists = [sum(abs(p[i] - ink[i]) for i in range(3)) for ink in self.inks]
                counts[dists.index(min(dists))] += 1
        empty = 100 * (400 * 300 - inked) / (400 * 300)
        shares = [100 * c / max(1, inked) for c in counts]
        zempty = None
        if zmask is not None:
            zm = zmask.resize((300, 400))
            occupied = sum(1 for v in zm.getdata() if v >= 128)
            zempty = 100 * (400 * 300 - occupied) / (400 * 300)
        return {"slug": self.slug, "empty": empty, "zempty": zempty,
                "shares": shares, "path": path}


def font(fname, size_1x):
    return ImageFont.truetype(FONT_DIR + fname, int(size_1x * S))


SERIF = "DejaVuSerif.ttf"
SERIF_B = "DejaVuSerif-Bold.ttf"
SANS = "DejaVuSans.ttf"
SANS_B = "DejaVuSans-Bold.ttf"
MONO = "DejaVuSansMono.ttf"
MONO_B = "DejaVuSansMono-Bold.ttf"
