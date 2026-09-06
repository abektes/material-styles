"""Dynamic style registry discovering built-in and community styles."""
import importlib
import inspect
import os
import pkgutil
from typing import Dict, List, Optional, Union

from material_styles.core.content import PosterContent
from material_styles.core.poster import StylePoster
from material_styles.styles.base import BaseStyle


class StyleRegistry:
    """Registry managing all active built-in and custom physical design styles."""

    def __init__(self):
        self._by_id: Dict[str, BaseStyle] = {}
        self._by_number: Dict[int, BaseStyle] = {}
        self._loaded = False

    def register(self, style: BaseStyle):
        """Register a style instance."""
        meta = style.metadata
        self._by_id[meta.id] = style
        self._by_number[meta.number] = style

    def get(self, key: Union[int, str]) -> Optional[BaseStyle]:
        """Look up a style by integer number (e.g. 1 or '01') or ID string."""
        self.ensure_loaded()
        if isinstance(key, int):
            return self._by_number.get(key)
        if isinstance(key, str):
            if key.isdigit():
                return self._by_number.get(int(key))
            # Try exact id match
            if key in self._by_id:
                return self._by_id[key]
            # Try with or without style_ prefix
            prefixed = f"style_{key}" if not key.startswith("style_") else key
            if prefixed in self._by_id:
                return self._by_id[prefixed]
            for s in self._by_id.values():
                if key.lower() in s.metadata.name.lower():
                    return s
        return None

    def list_styles(self) -> List[BaseStyle]:
        """Return all registered styles ordered by number."""
        self.ensure_loaded()
        return sorted(self._by_id.values(), key=lambda s: s.metadata.number)

    def ensure_loaded(self):
        """Lazy load built-in and custom styles if not already loaded."""
        if not self._loaded:
            self._load_builtins()
            self._load_custom()
            self._loaded = True

    def _load_builtins(self):
        import material_styles.styles as styles_pkg
        for _, modname, _ in pkgutil.iter_modules(styles_pkg.__path__):
            if modname.startswith("s") and "_" in modname:
                try:
                    mod = importlib.import_module(f"material_styles.styles.{modname}")
                    for _, cls in inspect.getmembers(mod, inspect.isclass):
                        if issubclass(cls, BaseStyle) and cls is not BaseStyle:
                            self.register(cls())
                except Exception as e:
                    print(f"Warning: Failed to load style module {modname}: {e}")

    def _load_custom(self):
        try:
            import material_styles.styles.custom as custom_pkg
            for _, modname, _ in pkgutil.iter_modules(custom_pkg.__path__):
                try:
                    mod = importlib.import_module(f"material_styles.styles.custom.{modname}")
                    for _, cls in inspect.getmembers(mod, inspect.isclass):
                        if issubclass(cls, BaseStyle) and cls is not BaseStyle:
                            self.register(cls())
                except Exception as e:
                    print(f"Warning: Failed to load custom style module {modname}: {e}")
        except Exception:
            pass


# Global singleton registry
registry = StyleRegistry()


def get_style(key: Union[int, str]) -> Optional[BaseStyle]:
    return registry.get(key)


def list_styles() -> List[BaseStyle]:
    return registry.list_styles()


def render_poster(
    style: Union[int, str, BaseStyle],
    headline: Optional[str] = None,
    subhead: Optional[str] = None,
    footnote: Optional[str] = None,
    accession_code: Optional[str] = None,
    seed: Optional[int] = None,
    output: Optional[str] = None,
    outdir: str = "styles_gallery",
    slug: Optional[str] = None,
) -> dict:
    """Render a poster dynamically using a style and optional custom content slots."""
    if isinstance(style, (int, str)):
        resolved_style = registry.get(style)
        if resolved_style is None:
            raise ValueError(f"Unknown style: {style}")
    else:
        resolved_style = style

    content = PosterContent(
        headline=headline,
        subhead=subhead,
        footnote=footnote,
        accession_code=accession_code,
        seed=seed,
    )
    poster = resolved_style.create_poster(slug=slug)
    result = resolved_style.render(poster, content=content, outdir=outdir)

    if output:
        from PIL import Image
        img = Image.open(result["path"])
        img.save(output)
        result["path"] = output

    return result
