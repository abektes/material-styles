"""Base class and metadata contract for all systematic material styles."""
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Tuple, List, Optional

from material_styles.core.content import PosterContent
from material_styles.core.poster import StylePoster, S


@dataclass
class StyleMetadata:
    id: str
    number: int
    name: str
    lineage: str
    substrate_hex: str
    substrate_rgb: Tuple[int, int, int]
    inks: List[Tuple[int, int, int]]
    gate_range: Tuple[int, int]
    description: str
    slug: Optional[str] = None
    default_content: PosterContent = field(default_factory=PosterContent)


class BaseStyle(ABC):
    """Abstract base class for all pluggable physical design styles."""

    metadata: StyleMetadata

    @abstractmethod
    def render(
        self,
        P: StylePoster,
        content: Optional[PosterContent] = None,
        outdir: str = "styles_gallery",
    ) -> dict:
        """Render the poster onto canvas P and return the gate result dict."""
        raise NotImplementedError

    def get_zone_mask(self, P: StylePoster):
        """Optional zone mask for calculating empty paper percentage."""
        return None

    def create_poster(self, slug: Optional[str] = None) -> StylePoster:
        """Instantiate a StylePoster canvas pre-configured with this style's substrate."""
        s = slug or self.metadata.slug or f"{self.metadata.number:02d}-{self.metadata.id.replace('style_', '').replace('_', '-')}"
        recipe = f"{self.metadata.id}|{self.metadata.substrate_hex}"
        return StylePoster(
            slug=s,
            style_id=self.metadata.id,
            substrate_rgb=self.metadata.substrate_rgb,
            inks=self.metadata.inks,
            recipe=recipe,
        )
