"""Core rendering engine primitives, canvas, and typography."""
from material_styles.core.content import PosterContent
from material_styles.core.primitives import (
    seed_of,
    multiply_colors,
    mix_colors,
    in_poly,
)
from material_styles.core.typography import (
    FONT_CANDIDATES,
    load_font,
    auto_fit_text,
    wrap_text_to_box,
)
from material_styles.core.poster import StylePoster, S, UW, UH, W, H

__all__ = [
    "PosterContent",
    "seed_of",
    "multiply_colors",
    "mix_colors",
    "in_poly",
    "FONT_CANDIDATES",
    "load_font",
    "auto_fit_text",
    "wrap_text_to_box",
    "StylePoster",
    "S",
    "UW",
    "UH",
    "W",
    "H",
]
