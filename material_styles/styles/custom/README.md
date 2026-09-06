# Custom Community Styles

Drop any new style Python module here (e.g. `s16_memphis_81.py`).
The dynamic style registry will automatically discover, validate, and register any subclass of `BaseStyle` found in this directory.

### Quick Start
To scaffold a new style with full boilerplate, run:
```bash
material-styles new-style "Memphis Group 1981" --id style_memphis_81
```

Or inherit from `BaseStyle` manually:
```python
from material_styles.styles.base import BaseStyle, StyleMetadata
from material_styles.core.content import PosterContent
from material_styles.core.poster import StylePoster

class MyCustomStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_my_custom",
        number=16,
        name="My Custom Physical Style",
        lineage="Movement / Pioneer (Year)",
        substrate_hex="#FAF8F5",
        substrate_rgb=(250, 248, 245),
        inks=[(24, 24, 26), (229, 57, 53)],
        gate_range=(30, 50),
        description="Physical print mechanics and reproductive engine description",
        default_content=PosterContent(headline="DEFAULT HEADLINE", subhead="DEFAULT SUBHEAD"),
    )

    def render(self, P=None, content=None, outdir="styles_gallery"):
        if P is None:
            P = self.create_poster()
        content = content or self.metadata.default_content
        headline = content.get_slot("headline", "DEFAULT HEADLINE")
        # Draw physical plates & geometry...
        return P.finish(outdir=outdir, gate_range=self.metadata.gate_range)
```
