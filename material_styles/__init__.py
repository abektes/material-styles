"""Material Styles: 15 Systematic Physical Design Systems & Generative Print Engine."""
from material_styles.core.content import PosterContent
from material_styles.core.poster import StylePoster
from material_styles.styles.base import BaseStyle, StyleMetadata
from material_styles.registry import registry, get_style, list_styles, render_poster
from material_styles.audit import audit_style, audit_all
from material_styles.scaffold import scaffold_style

__version__ = "0.2.0"
__all__ = [
    "PosterContent",
    "StylePoster",
    "BaseStyle",
    "StyleMetadata",
    "registry",
    "get_style",
    "list_styles",
    "render_poster",
    "audit_style",
    "audit_all",
    "scaffold_style",
]
