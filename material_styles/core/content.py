"""Parametric content slots for material-driven design systems."""
from dataclasses import dataclass, field
from typing import Optional, Dict, Any


@dataclass
class PosterContent:
    """Semantic content slots for poster rendering.

    Styles define authentic historic fallbacks when slots are left empty.
    """
    headline: Optional[str] = None
    subhead: Optional[str] = None
    footnote: Optional[str] = None
    accession_code: Optional[str] = None
    seed: Optional[int] = None
    extra: Dict[str, Any] = field(default_factory=dict)

    def get_slot(self, slot_name: str, fallback: str) -> str:
        """Get a slot string or return the historic default fallback."""
        val = getattr(self, slot_name, None)
        if val is not None and str(val).strip() != "":
            return str(val).strip()
        return fallback
