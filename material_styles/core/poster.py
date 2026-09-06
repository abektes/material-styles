"""Core StylePoster canvas implementing physical substrate and reproduction mechanics."""
import math
import os
import random
from PIL import Image, ImageChops, ImageDraw

from material_styles.core.primitives import (
    seed_of,
    multiply_colors,
    mix_colors,
    in_poly,
)
from material_styles.core.typography import load_font

S = 2                       # supersample scale factor
UW, UH = 1200, 1600         # 1x output dimensions
W, H = UW * S, UH * S       # 2x supersampled dimensions


class StylePoster:
    """Master poster canvas implementing physics-based plate rendering."""

    def __init__(self, slug, style_id, substrate_rgb, inks, recipe, scale=S):
        self.slug = slug
        self.style_id = style_id
        self.scale = scale
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

    # ---------------- 3D Axonometric helper ----------------
    def draw_axono_box(
        self,
        ox,
        oy,
        dx,
        dy,
        dz,
        top_fill=None,
        left_fill=None,
        right_fill=None,
        outline_ink=None,
        width=1.5,
    ):
        """Draw an axonometric 3D cube/box at (ox, oy)."""
        # Axonometric isometric projection:
        # X goes down-left (cos 30, sin 30)
        # Y goes down-right (cos 30, sin 30)
        # Z goes straight up
        cos30 = 0.866025
        sin30 = 0.5

        def prj(x, y, z):
            px = ox + (y - x) * cos30
            py = oy + (x + y) * sin30 - z
            return (px, py)

        p000 = prj(0, 0, 0)
        p100 = prj(dx, 0, 0)
        p110 = prj(dx, dy, 0)
        p010 = prj(0, dy, 0)
        p001 = prj(0, 0, dz)
        p101 = prj(dx, 0, dz)
        p111 = prj(dx, dy, dz)
        p011 = prj(0, dy, dz)

        top_poly = [p001, p101, p111, p011]
        left_poly = [p000, p100, p101, p001]
        right_poly = [p100, p110, p111, p101]

        if top_fill:
            self.poly(top_poly, top_fill)
        if left_fill:
            self.poly(left_poly, left_fill)
        if right_fill:
            self.poly(right_poly, right_fill)

        if outline_ink:
            edges = [
                (p000, p100), (p100, p110), (p110, p010), (p010, p000),
                (p001, p101), (p101, p111), (p111, p011), (p011, p001),
                (p000, p001), (p100, p101), (p110, p111), (p010, p011),
            ]
            for e0, e1 in edges:
                self.line([e0, e1], outline_ink, w=width)

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
        self.stamp(mask_plate1, ink1)

        shifted_mask2 = Image.new("L", (W, H), 0)
        shifted_mask2.paste(mask_plate2, (int(ox2 * S), int(oy2 * S)))

        p1_inv = ImageChops.invert(mask_plate1)
        p2_alone = ImageChops.multiply(shifted_mask2, p1_inv)
        self.stamp(p2_alone, ink2)

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

    def rotated_halftone(
        self,
        x0,
        y0,
        x1,
        y1,
        pitch,
        angle_deg,
        density_fn,
        ink,
        shape="circle",
        max_r=None,
        jitter=0.04,
        drift=(0, 0),
    ):
        """Rotated halftone screen at arbitrary angle (15, 45, 75 degrees)."""
        rad = math.radians(angle_deg)
        cos_a = math.cos(rad)
        sin_a = math.sin(rad)
        cx = (x0 + x1) / 2.0
        cy = (y0 + y1) / 2.0
        diag = math.hypot(x1 - x0, y1 - y0)
        u_min, u_max = -diag / 2.0, diag / 2.0
        v_min, v_max = -diag / 2.0, diag / 2.0

        if max_r is None:
            max_r = pitch * 0.58

        u = u_min
        while u <= u_max:
            v = v_min
            while v <= v_max:
                px = cx + u * cos_a - v * sin_a + drift[0]
                py = cy + u * sin_a + v * cos_a + drift[1]
                if x0 <= px <= x1 and y0 <= py <= y1:
                    density = density_fn(px, py)
                    if density > 0.03:
                        r = max_r * math.sqrt(min(1.0, density))
                        if jitter > 0:
                            r *= 1.0 + self.rng.uniform(-jitter, jitter)
                        if shape == "circle":
                            self.dot(px, py, r, ink)
                        elif shape == "square":
                            self.rect(px - r, py - r, px + r, py + r, ink)
                        elif shape == "diamond":
                            pts = [(px, py - r * 1.2), (px + r * 1.2, py), (px, py + r * 1.2), (px - r * 1.2, py)]
                            self.poly(pts, ink)
                        elif shape == "cross":
                            th = max(1.0, r * 0.4)
                            self.rect(px - r, py - th, px + r, py + th, ink)
                            self.rect(px - th, py - r, px + th, py + r, ink)
                        elif shape == "line":
                            self.line([(px - pitch * 0.45, py), (px + pitch * 0.45, py)], ink, w=max(1.0, r * 1.5))
                v += pitch
            u += pitch

    def cmyk_rosette_field(
        self,
        x0,
        y0,
        x1,
        y1,
        pitch=14,
        cmyk_fn=None,
        c_ink=(0x00, 0x9F, 0xE3),
        m_ink=(0xE6, 0x00, 0x7A),
        y_ink=(0xFF, 0xDE, 0x00),
        k_ink=(0x18, 0x18, 0x1A),
    ):
        """Authentic 4-color offset lithography halftone rosette field (CMYK angles)."""
        if cmyk_fn is None:
            return
        self.rotated_halftone(x0, y0, x1, y1, pitch, 0, lambda x, y: cmyk_fn(x, y)[2], y_ink, shape="circle")
        self.rotated_halftone(x0, y0, x1, y1, pitch, 15, lambda x, y: cmyk_fn(x, y)[0], c_ink, shape="circle")
        self.rotated_halftone(x0, y0, x1, y1, pitch, 75, lambda x, y: cmyk_fn(x, y)[1], m_ink, shape="circle")
        self.rotated_halftone(x0, y0, x1, y1, pitch, 45, lambda x, y: cmyk_fn(x, y)[3], k_ink, shape="circle")

    # ---------------- Linocut Relief ----------------
    def linocut_relief(self, poly_pts, ink, bg_ink, num_gouges=8, seed=42):
        """Simulates hand-carved relief woodblock gouges inside a solid polygon."""
        self.poly(poly_pts, ink)
        xs = [p[0] for p in poly_pts]
        ys = [p[1] for p in poly_pts]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)

        step_y = (max_y - min_y) / (num_gouges + 1)
        for i in range(1, num_gouges + 1):
            gy = min_y + i * step_y + ((i * 17) % 7) - 3
            gx0 = min_x + 15 + ((i * 23) % 25)
            gx1 = max_x - 15 - ((i * 31) % 25)
            if gx1 > gx0 + 30:
                w = 1.5 if i % 2 == 0 else 2.5
                pts = [
                    (gx0, gy),
                    ((gx0 + gx1) * 0.4, gy + ((i * 13) % 9) - 4),
                    ((gx0 + gx1) * 0.7, gy - ((i * 11) % 7) + 3),
                    (gx1, gy),
                ]
                self.line(pts, bg_ink, w=w)

    # ---------------- Scanlines ----------------
    def scanlines(self, x0, y0, x1, y1, ink, period=4, depth=0.4, aberration=2, jitter=1.0):
        """Draws alternating scanline rows with slight horizontal jitter."""
        for y in range(int(y0), int(y1), period):
            jit = int((self.rng.random() - 0.5) * 2 * jitter)
            self.line([(x0 + jit - aberration, y), (x1 + jit + aberration, y)], ink, w=1.0)

    # ---------------- 1-Bit Algorithmic Dithering ----------------
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
                intensity = grad_fn(x, y)
                if intensity > threshold:
                    self.rect(x, y, x + step, y + step, ink)

    # ---------------- Crosshatch ----------------
    def crosshatch_field(self, x0, y0, x1, y1, density_fn, ink, pitch=6):
        """Fine intaglio crosshatch lines modulated by density function."""
        y = y0 - (x1 - x0)
        while y < y1 + (x1 - x0):
            cy = max(y0, min(y1, y + (x1 - x0) / 2))
            cx = (x0 + x1) / 2
            d = density_fn(cx, cy)
            if d > 0.15:
                w = 1.0 if d < 0.6 else 2.0
                self.line([(x0, y), (x1, y + (x1 - x0))], ink, w)
            y += pitch

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
        f = load_font(category, size_1x, scale=S)
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
        f = load_font(category, size_1x, scale=S)
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
        f = load_font(category, size_1x, scale=S)
        tw = int(self.d.textlength(s, font=f)) + 30 * S
        th = int(size_1x * 1.5 * S) + 30 * S
        tmp = Image.new("L", (tw, th), 0)
        ImageDraw.Draw(tmp).text((15 * S, 15 * S), s, font=f, fill=255)
        rot = tmp.rotate(90, expand=True, resample=Image.BICUBIC)
        self.img.paste(ink, (int(xy[0] * S), int(xy[1] * S)), rot)

    def rotated_text(self, xy, s, category, size_1x, ink, angle_deg, tracking=0):
        """Render text rotated by arbitrary angle."""
        f = load_font(category, size_1x, scale=S)
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
        """Punk fanzine cutout letter tile."""
        x = xy[0]
        y = xy[1]
        for ch in word:
            rot = self.rng.uniform(-jitter_deg, jitter_deg)
            cat = self.rng.choice(["din_bold", "grotesk_bold", "serif_bold", "mono_bold"])
            f = load_font(cat, size_1x, scale=S)
            ch_w = self.d.textlength(ch, font=f) / S
            tile_w = int(ch_w + 12)
            tile_h = int(size_1x * 1.3)
            tile = Image.new("RGB", (int(tile_w * S), int(tile_h * S)), bg_ink)
            td = ImageDraw.Draw(tile)
            td.text((int(6 * S), int(4 * S)), ch, font=f, fill=text_ink)
            tile_rot = tile.rotate(rot, expand=True, resample=Image.BICUBIC)
            shadow_mask = Image.new("L", tile_rot.size, 160)
            self.img.paste((20, 20, 20), (int((x + 2) * S), int((y + 3) * S)), shadow_mask)
            self.img.paste(tile_rot, (int(x * S), int(y * S)))
            x += tile_w + 4

    def cinnabar_seal(self, cx, cy, size_1x, text_kanji, seal_ink):
        """Wabi-Sabi vermilion cinnabar signature seal stamp (*shuniku*)."""
        hs = size_1x / 2
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
        f = load_font("serif_bold", size_1x * 0.45, scale=S)
        self.d.text((int((cx - hs * 0.55) * S), int((cy - hs * 0.6) * S)), text_kanji[:1], font=f, fill=self.sub)
        if len(text_kanji) > 1:
            self.d.text((int((cx - hs * 0.55) * S), int((cy) * S)), text_kanji[1:2], font=f, fill=self.sub)

    def spec_callout(self, pt_x, pt_y, num_str, ink, radius=16, lead_dx=50, lead_dy=-40):
        """Technical drawing dimension callout circle with leader line."""
        if len(num_str) > 1 and radius < 18:
            radius = 18

        ex = pt_x + lead_dx
        ey = pt_y + lead_dy

        dx = ex - pt_x
        dy = ey - pt_y
        dist = math.hypot(dx, dy)
        if dist < 1:
            dist = 1
        ux = dx / dist
        uy = dy / dist

        contact_x = ex - ux * radius
        contact_y = ey - uy * radius

        self.line([(pt_x, pt_y), (contact_x, contact_y)], ink, w=1.5)
        self.dot(pt_x, pt_y, 2.5, ink)
        self.ell(ex - radius, ey - radius, ex + radius, ey + radius, self.sub)
        self.ring(ex, ey, radius, 1.8, ink)

        f = load_font("din_bold", radius * 1.1, scale=S)
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

        small = final.resize((300, 400))
        get_d = getattr(small, "get_flattened_data", small.getdata)
        pixels = list(get_d())
        inked = 0
        counts = [0] * len(self.inks)
        for p in pixels:
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
            get_zm = getattr(zm, "get_flattened_data", zm.getdata)
            occupied = sum(1 for v in get_zm() if v >= 120)
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
