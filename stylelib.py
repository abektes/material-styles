"""Unified deterministic rendering engine for the 10 Material-Driven Design Styles.

Grounded in printing physics, substrate chemistry, plate separations, mechanical
screening, strict typographic hierarchy, and seeded analog imperfections.
All coordinates in 1x space (1200x1600); internally supersampled at S=2.
Deterministic: identical recipe and seed produces byte-identical output.
"""
import hashlib
import math
import os
import random
import warnings

from PIL import Image, ImageChops, ImageDraw, ImageFont, ImageFilter

warnings.filterwarnings("ignore")

S = 2                       # supersample scale factor
UW, UH = 1200, 1600         # 1x output dimensions
W, H = UW * S, UH * S       # 2x supersampled dimensions

FONT_CANDIDATES = {
    "grotesk_bold": [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "grotesk": [
        "/System/Library/Fonts/Helvetica.ttc",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "din_bold": [
        "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf",
        "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    ],
    "din": [
        "/System/Library/Fonts/Supplemental/DIN Alternate Bold.ttf",
        "/System/Library/Fonts/Supplemental/DIN Condensed Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ],
    "serif": [
        "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf",
    ],
    "serif_bold": [
        "/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
    ],
    "serif_italic": [
        "/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Italic.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Italic.ttf",
    ],
    "mono": [
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/System/Library/Fonts/Supplemental/Courier New Bold.ttf",
        "/System/Library/Fonts/Monaco.dfont",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
    ],
    "mono_bold": [
        "/System/Library/Fonts/Supplemental/Courier New Bold.ttf",
        "/System/Library/Fonts/Supplemental/Courier New.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf",
    ],
}


def load_font(category, size_1x):
    """Resolve font for category and scale by supersample factor S."""
    size_px = int(size_1x * S)
    paths = FONT_CANDIDATES.get(category, FONT_CANDIDATES["grotesk"])
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size_px)
            except Exception:
                continue
    return ImageFont.load_default()


def seed_of(key_string):
    """Derive stable 32-bit integer seed from recipe string."""
    return int(hashlib.md5(key_string.encode("utf-8")).hexdigest()[:8], 16)


def multiply_colors(c1, c2):
    """Subtractive optical multiply of two ink pigments."""
    return (
        int((c1[0] * c2[0]) / 255),
        int((c1[1] * c2[1]) / 255),
        int((c1[2] * c2[2]) / 255),
    )


def mix_colors(c1, c2, t):
    """Linear interpolation between two RGB colors."""
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


class StylePoster:
    """Master poster canvas implementing physics-based plate rendering."""

    def __init__(self, slug, style_id, substrate_rgb, inks, recipe):
        self.slug = slug
        self.style_id = style_id
        self.sub = substrate_rgb
        self.inks = inks  # list of primary ink RGB tuples
        self.recipe = recipe
        self.seed = seed_of(recipe)
        self.rng = random.Random(self.seed)
        self.img = Image.new("RGB", (W, H), self.sub)
        self.d = ImageDraw.Draw(self.img)

        # Seeded registration drift (~0.5 - 2.5 mm in 1x space)
        angle = self.rng.uniform(0, 2 * math.pi)
        drift_dist = self.rng.uniform(2.0, 5.0)
        self.drift = (
            int(math.cos(angle) * drift_dist),
            int(math.sin(angle) * drift_dist),
        )

    # ---------------- Geometry primitives ----------------
    def poly(self, pts, ink):
        self.d.polygon([(x * S, y * S) for x, y in pts], fill=ink)

    def rect(self, x0, y0, x1, y1, ink, outline=False, width=1):
        box = [x0 * S, y0 * S, x1 * S, y1 * S]
        if outline:
            self.d.rectangle(box, outline=ink, width=int(width * S))
        else:
            self.d.rectangle(box, fill=ink)

    def ell(self, x0, y0, x1, y1, ink, outline=False, width=1):
        box = [x0 * S, y0 * S, x1 * S, y1 * S]
        if outline:
            self.d.ellipse(box, outline=ink, width=int(width * S))
        else:
            self.d.ellipse(box, fill=ink)

    def dot(self, x, y, r, ink):
        if r * S < 0.4:
            return
        self.d.ellipse(
            [(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=ink
        )

    def ring(self, cx, cy, r, w, ink):
        self.d.ellipse(
            [(cx - r) * S, (cy - r) * S, (cx + r) * S, (cy + r) * S],
            outline=ink,
            width=int(w * S),
        )

    def line(self, pts, ink, w=1):
        self.d.line([(x * S, y * S) for x, y in pts], fill=ink, width=int(w * S))

    # ---------------- Mask & Layer operations ----------------
    def create_mask(self, draw_fn):
        """Create an 8-bit grayscale L mask at full resolution."""
        m = Image.new("L", (W, H), 0)
        dm = ImageDraw.Draw(m)
        draw_fn(dm)
        return m

    def stamp(self, mask, ink, ox=0, oy=0):
        """Paste ink through an L mask with optional offset."""
        self.img.paste(ink, (int(ox * S), int(oy * S)), mask)

    def knock(self, mask, ox=0, oy=0):
        """Knock out paper substrate through an L mask."""
        self.stamp(mask, self.sub, ox, oy)

    def overprint_multiply(self, mask_plate1, ink1, mask_plate2, ink2, ox2=0, oy2=0):
        """Physical subtractive optical multiply of two overlapping plates."""
        # 1. Stamp plate 1
        self.stamp(mask_plate1, ink1)

        # 2. Shift plate 2 for registration drift
        shifted_mask2 = Image.new("L", (W, H), 0)
        shifted_mask2.paste(mask_plate2, (int(ox2 * S), int(oy2 * S)))

        # 3. Plate 2 alone (where plate 1 is NOT present)
        p1_inv = ImageChops.invert(mask_plate1)
        p2_alone = ImageChops.multiply(shifted_mask2, p1_inv)
        self.stamp(p2_alone, ink2)

        # 4. Overlap intersection: subtractive multiply ink
        overlap_mask = ImageChops.multiply(mask_plate1, shifted_mask2)
        mult_ink = multiply_colors(ink1, ink2)
        self.stamp(overlap_mask, mult_ink)

    # ---------------- Halftone screening ----------------
    def halftone(
        self,
        x0,
        y0,
        x1,
        y1,
        pitch,
        r_fn,
        region_fn,
        ink,
        jitter=0.07,
        drift=(0, 0),
    ):
        """Screened halftone dots with seeded density jitter and plate drift."""
        pitch_s = pitch * S
        row = 0
        yy = y0 * S
        while yy < y1 * S:
            off = (pitch_s // 2) if row % 2 else 0
            row += 1
            xx = x0 * S + off
            while xx < x1 * S:
                orig_x, orig_y = xx / S, yy / S
                if region_fn(orig_x, orig_y):
                    r = r_fn(orig_x, orig_y)
                    if r and r > 0:
                        r *= 1 + self.rng.uniform(-jitter, jitter)
                        self.dot(orig_x + drift[0], orig_y + drift[1], r, ink)
                xx += pitch_s
            yy += pitch_s

    # ---------------- 1-Bit Algorithmic Dithering (Thermal Fax) ----------------
    def dither_1bit_field(self, x0, y0, x1, y1, grad_fn, ink, step=2):
        """Deterministic 4x4 Bayer ordered matrix 1-bit dithering."""
        bayer4 = [
            [0, 8, 2, 10],
            [12, 4, 14, 6],
            [3, 11, 1, 9],
            [15, 7, 13, 5],
        ]
        for y in range(int(y0), int(y1), step):
            by = (y // step) % 4
            for x in range(int(x0), int(x1), step):
                bx = (x // step) % 4
                threshold = (bayer4[by][bx] + 0.5) / 16.0
                intensity = grad_fn(x, y)  # 0.0 (paper) to 1.0 (ink)
                if intensity > threshold:
                    self.rect(x, y, x + step, y + step, ink)

    # ---------------- Copperplate crosshatch (Linnaean Naturalist) ----------------
    def crosshatch_field(self, x0, y0, x1, y1, density_fn, ink, pitch=6):
        """Fine intaglio crosshatch lines modulated by density function."""
        # Layer 1: 45 degree hatch
        y = y0 - (x1 - x0)
        while y < y1 + (x1 - x0):
            # Sample density along line
            cy = max(y0, min(y1, y + (x1 - x0) / 2))
            cx = (x0 + x1) / 2
            d = density_fn(cx, cy)
            if d > 0.15:
                w = 1.0 if d < 0.6 else 2.0
                self.line([(x0, y), (x1, y + (x1 - x0))], ink, w)
            y += pitch

        # Layer 2: -45 degree cross-hatch for deep shadows
        y = y0 - (x1 - x0)
        while y < y1 + (x1 - x0):
            cy = max(y0, min(y1, y + (x1 - x0) / 2))
            cx = (x0 + x1) / 2
            d = density_fn(cx, cy)
            if d > 0.55:
                self.line([(x1, y), (x0, y + (x1 - x0))], ink, 1.0)
            y += pitch

    # ---------------- Typography helpers ----------------
    def text_w(self, s, category, size_1x, tracking=0):
        f = load_font(category, size_1x)
        w = sum(self.d.textlength(ch, font=f) for ch in s)
        return (w + tracking * S * max(0, len(s) - 1)) / S

    def text(
        self,
        xy,
        s,
        category,
        size_1x,
        ink,
        tracking=0,
        anchor_x="left",
    ):
        f = load_font(category, size_1x)
        wpx = self.text_w(s, category, size_1x, tracking)
        x = (
            xy[0]
            if anchor_x == "left"
            else (xy[0] - wpx if anchor_x == "right" else xy[0] - wpx / 2)
        )
        x = int(x)
        y = int(xy[1])
        if tracking:
            cx = x * S
            for ch in s:
                self.d.text((cx, y * S), ch, font=f, fill=ink)
                cx += self.d.textlength(ch, font=f) + tracking * S
        else:
            self.d.text((x * S, y * S), s, font=f, fill=ink)

    def vtext(self, xy, s, category, size_1x, ink):
        """Vertical 90-degree rotated text (reading upwards)."""
        f = load_font(category, size_1x)
        tw = int(self.d.textlength(s, font=f)) + 30 * S
        th = int(size_1x * 1.5 * S) + 30 * S
        tmp = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(tmp).text((15 * S, 15 * S), s, font=f, fill=255)
        rot = tmp.rotate(90, expand=True, resample=Image.BICUBIC)
        self.img.paste(ink, (int(xy[0] * S), int(xy[1] * S)), rot)

    def rotated_text(self, xy, s, category, size_1x, ink, angle_deg, tracking=0):
        """Render text rotated by arbitrary angle (e.g. 45-degree Constructivist wedge)."""
        f = load_font(category, size_1x)
        tw = int(self.text_w(s, category, size_1x, tracking) * S) + 60 * S
        th = int(size_1x * 1.8 * S) + 60 * S
        tmp = Image.new("L", (tw, th), 0)
        dt = ImageDraw.Draw(tmp)
        if tracking:
            cx = 30 * S
            for ch in s:
                dt.text((cx, 30 * S), ch, font=f, fill=255)
                cx += dt.textlength(ch, font=f) + tracking * S
        else:
            dt.text((30 * S, 30 * S), s, font=f, fill=255)
        rot = tmp.rotate(angle_deg, expand=True, resample=Image.BICUBIC)
        self.img.paste(ink, (int(xy[0] * S), int(xy[1] * S)), rot)

    def ransom_word(self, xy, word, size_1x, bg_ink, text_ink, jitter_deg=4):
        """Punk fanzine cutout letter tile: glued newsprint box with character jitter."""
        x = xy[0]
        y = xy[1]
        for ch in word:
            rot = self.rng.uniform(-jitter_deg, jitter_deg)
            cat = self.rng.choice(["din_bold", "grotesk_bold", "serif_bold", "mono_bold"])
            f = load_font(cat, size_1x)
            ch_w = self.d.textlength(ch, font=f) / S
            tile_w = int(ch_w + 12)
            tile_h = int(size_1x * 1.3)
            # Create tile mask
            tile = Image.new("RGB", (int(tile_w * S), int(tile_h * S)), bg_ink)
            td = ImageDraw.Draw(tile)
            td.text((int(6 * S), int(4 * S)), ch, font=f, fill=text_ink)
            # Slight rotation
            tile_rot = tile.rotate(rot, expand=True, resample=Image.BICUBIC)
            # Paper cutout drop shadow
            shadow_mask = Image.new("L", tile_rot.size, 160)
            self.img.paste((20, 20, 20), (int((x + 2) * S), int((y + 3) * S)), shadow_mask)
            self.img.paste(tile_rot, (int(x * S), int(y * S)))
            x += tile_w + 4

    def cinnabar_seal(self, cx, cy, size_1x, text_kanji, seal_ink):
        """Wabi-Sabi vermilion cinnabar signature seal stamp (*shuniku*)."""
        hs = size_1x / 2
        # Slight organic irregularity
        pts = [
            (cx - hs, cy - hs),
            (cx + hs, cy - hs),
            (cx + hs, cy + hs),
            (cx - hs, cy + hs),
        ]
        self.d.rounded_rectangle(
            [(p[0] * S, p[1] * S) for p in [(cx - hs, cy - hs), (cx + hs, cy + hs)]],
            radius=int(4 * S),
            fill=seal_ink,
        )
        f = load_font("serif_bold", size_1x * 0.45)
        # Inverted paper characters inside seal
        self.d.text((int((cx - hs * 0.55) * S), int((cy - hs * 0.6) * S)), text_kanji[:1], font=f, fill=self.sub)
        if len(text_kanji) > 1:
            self.d.text((int((cx - hs * 0.55) * S), int((cy) * S)), text_kanji[1:2], font=f, fill=self.sub)

    def spec_callout(self, pt_x, pt_y, num_str, ink, radius=16, lead_dx=50, lead_dy=-40):
        """Technical drawing dimension callout circle with leader line.

        Leader terminates precisely on the circle circumference without cutting
        through the callout ring or numeral. Numeral is centered via textbbox.
        """
        # Adapt radius for multi-character labels (e.g. '4a')
        if len(num_str) > 1 and radius < 18:
            radius = 18

        ex = pt_x + lead_dx
        ey = pt_y + lead_dy

        # Unit vector from target point on object to callout circle center
        dx = ex - pt_x
        dy = ey - pt_y
        dist = math.hypot(dx, dy)
        if dist < 1:
            dist = 1
        ux = dx / dist
        uy = dy / dist

        # Contact point on circle perimeter facing the target point
        contact_x = ex - ux * radius
        contact_y = ey - uy * radius

        # Draw leader line terminating exactly on circumference
        self.line([(pt_x, pt_y), (contact_x, contact_y)], ink, w=1.5)

        # Terminal dot on object surface
        self.dot(pt_x, pt_y, 2.5, ink)

        # Fill circle with substrate background so background grid/linework is masked
        self.ell(ex - radius, ey - radius, ex + radius, ey + radius, self.sub)

        # Callout outline ring
        self.ring(ex, ey, radius, 1.8, ink)

        # Centered numeral using exact text bounding box
        f = load_font("din_bold", radius * 1.1)
        bbox = self.d.textbbox((0, 0), num_str, font=f)
        tcx = (bbox[0] + bbox[2]) / 2.0
        tcy = (bbox[1] + bbox[3]) / 2.0
        self.d.text(
            (int(ex * S - tcx), int(ey * S - tcy)),
            num_str,
            font=f,
            fill=ink,
        )

    # ---------------- Metrics and output ----------------
    def finish(self, outdir="styles_gallery", zmask=None, gate_range=(30, 55)):
        """Generate final image, compute pixel/zone empty paper, and verify gates."""
        os.makedirs(outdir, exist_ok=True)
        final = self.img.resize((UW, UH), Image.LANCZOS)
        out_path = f"{outdir}/{self.slug}.png"
        final.save(out_path)

        # Quantitative metric audit
        small = final.resize((300, 400))
        pixels = list(small.getdata())
        inked = 0
        counts = [0] * len(self.inks)
        for p in pixels:
            # Distance from substrate
            dist_sub = sum(abs(p[i] - self.sub[i]) for i in range(3))
            if dist_sub > 32:
                inked += 1
                if self.inks:
                    dists = [sum(abs(p[i] - ink[i]) for i in range(3)) for ink in self.inks]
                    counts[dists.index(min(dists))] += 1

        total = len(pixels)
        empty_pct = 100.0 * (total - inked) / total
        shares = [100.0 * c / max(1, inked) for c in counts]

        zempty_pct = None
        if zmask is not None:
            zm = zmask.resize((300, 400))
            occupied = sum(1 for v in zm.getdata() if v >= 120)
            zempty_pct = 100.0 * (total - occupied) / total

        lo, hi = gate_range
        check_val = zempty_pct if zempty_pct is not None else empty_pct
        gate_ok = lo <= check_val <= hi

        return {
            "slug": self.slug,
            "style_id": self.style_id,
            "empty": empty_pct,
            "zempty": zempty_pct,
            "shares": shares,
            "gate_ok": gate_ok,
            "gate_range": gate_range,
            "path": out_path,
        }
