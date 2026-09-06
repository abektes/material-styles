"""Cross-platform typography management, font resolution, and auto-fitting."""
import os
from PIL import ImageFont

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


def load_font(category: str, size_1x: float, scale: int = 2):
    """Resolve font for category and scale by supersample factor scale."""
    size_px = int(size_1x * scale)
    paths = FONT_CANDIDATES.get(category, FONT_CANDIDATES["grotesk"])
    for p in paths:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size_px)
            except Exception:
                continue
    return ImageFont.load_default()


def auto_fit_text(
    draw,
    text: str,
    category: str,
    max_width_1x: float,
    max_size_1x: float = 120,
    min_size_1x: float = 18,
    tracking: float = 0,
    scale: int = 2,
) -> float:
    """Calculate the largest font size (in 1x coords) that fits within max_width_1x."""
    max_width_px = max_width_1x * scale
    curr_size = max_size_1x

    while curr_size > min_size_1x:
        f = load_font(category, curr_size, scale=scale)
        # Measure text with tracking
        total_w = 0
        for ch in text:
            bbox = draw.textbbox((0, 0), ch, font=f)
            ch_w = bbox[2] - bbox[0]
            total_w += ch_w + tracking * scale
        if total_w <= max_width_px:
            return curr_size
        curr_size -= 2

    return min_size_1x


def wrap_text_to_box(
    text: str,
    max_chars_per_line: int = 24,
) -> list:
    """Break text into lines if longer than max_chars_per_line."""
    words = text.split()
    lines = []
    curr = []
    curr_len = 0
    for w in words:
        if curr_len + len(w) + 1 > max_chars_per_line and curr:
            lines.append(" ".join(curr))
            curr = [w]
            curr_len = len(w)
        else:
            curr.append(w)
            curr_len += len(w) + 1
    if curr:
        lines.append(" ".join(curr))
    return lines
