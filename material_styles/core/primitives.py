"""Color mathematics, seed derivation, and polygon geometry primitives."""
import hashlib


def seed_of(key_string: str) -> int:
    """Derive stable 32-bit integer seed from recipe string."""
    return int(hashlib.md5(key_string.encode("utf-8")).hexdigest()[:8], 16)


def multiply_colors(c1, c2):
    """Subtractive optical multiply of two ink pigments."""
    return (
        int((c1[0] * c2[0]) / 255),
        int((c1[1] * c2[1]) / 255),
        int((c1[2] * c2[2]) / 255),
    )


def mix_colors(c1, c2, t: float):
    """Linear interpolation between two RGB colors."""
    return (
        int(c1[0] + (c2[0] - c1[0]) * t),
        int(c1[1] + (c2[1] - c1[1]) * t),
        int(c1[2] + (c2[2] - c1[2]) * t),
    )


def in_poly(x: float, y: float, poly) -> bool:
    """Ray-casting point-in-polygon test in supersampled coords."""
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
