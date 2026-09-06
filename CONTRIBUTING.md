# Contributing New Design Directions to Material Styles

`material-styles` is designed as an extensible, community-driven physical design engine. Anyone can contribute a new systematic design style—whether from design history, printmaking movements, architectural manifestos, or underground subcultures.

---

## 5-Step Guide to Adding a New Style

### 1. Scaffold Your Style
Use the built-in scaffolding CLI to create the boilerplate:
```bash
material-styles new-style "Memphis Group 1981" --id style_memphis_81
```
This generates a new file in `material_styles/styles/custom/s16_memphis_group_1981.py`.

### 2. Configure Physical Substrate & Spot Pigments
In your new file, define real paper substrate and spot ink RGB values:
```python
# Uncoated high-bulk paper or synthetic plastic laminate
SUB_LAMINATE = (0xFA, 0xFA, 0xF5)

# High-voltage Postmodern spot inks
INK_ELECTRIC_TEAL = (0x00, 0xD2, 0xC4)
INK_SQUIGGLE_CORAL = (0xFF, 0x6B, 0x6B)
INK_LEOPARD_BLACK = (0x1C, 0x1B, 0x1E)
```

### 3. Implement Print Mechanics & Parametric Slots
Use the core engine primitives in `self.render()`:
- `P.rotated_halftone(...)`: Angled Ben-Day screening (e.g. 15°, 45°, 75°).
- `P.cmyk_rosette_field(...)`: Subtractive 4-plate offset lithography.
- `P.linocut_relief(...)`: Hand-carved woodblock knife gouging.
- `P.scanlines(...)`: CRT raster and photocopier horizontal pass jitter.
- `P.dither_1bit_field(...)`: Bayer matrix 1-bit thermal dithering.
- `P.draw_axono_box(...)`: 3D isometric & axonometric assemblies.

Support parametric text slots using `content.get_slot()` with authentic historic fallbacks:
```python
headline = content.get_slot("headline", "ETTORE SOTTSASS")
subhead = content.get_slot("subhead", "MILANO SALONE 1981")
```

### 4. Define Empty Paper Gate & Zone Mask
Set realistic empty paper bounds in `metadata.gate_range`:
```python
gate_range = (30, 50)  # e.g., 30% to 50% must remain unprinted paper
```

Define the graphic zone mask inside `render()`:
```python
def zm(dm):
    dm.rectangle([120 * S, 140 * S, 1080 * S, 1300 * S], fill=255)
return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=self.metadata.gate_range)
```

### 5. Audit & Verify
Run the audit tool to ensure:
1. Empty paper percentage falls strictly within the gate range.
2. Two consecutive renders produce 100% identical SHA-256 hashes.

```bash
# Audit your style
material-styles audit style_memphis_81

# Run full test suite
pytest tests/ -v
```

Once all tests pass, submit your Pull Request!
EOF
