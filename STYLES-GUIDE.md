# Material Styles — 10 Systematic Physical Design Systems

A comprehensive generative and programmatic design architecture inspired by and expanding upon the [mono-color skill](https://github.com/yanliudesign/mono-color-skill).

Instead of treating design styles as arbitrary prompt adjectives ("ultra-detailed", "retro", "aesthetic"), this system models **physical reproduction physics**:
1. **Substrate Chemistry**: Paper stock weight, fiber tooth, and base RGB chemistry.
2. **Plate Separation**: Explicit plate roles, named pigments, opacity, and subtractive optical multiply.
3. **Reproduction Mechanics**: Halftone screening, 1-bit Bayer matrix dithering, copperplate crosshatching, intaglio debossing, contact photograms.
4. **Typographic Scale Jump**: Disciplined hierarchies with 5:1 to 16:1 display-to-support jumps.
5. **Controlled Analog Imperfections**: Deterministic seeded flaws (registration drift, toner drum scratches, thermal head burnouts, chemical tide lines).
6. **Mathematical Gates**: Strict programmatic bounds on empty paper percentage and plate ink distribution.

---

## 10-Style Verification Matrix

All 10 posters were generated with `render_styles_gallery.py` + `stylelib.py` (Python/PIL) and verified to be **100% byte-for-byte reproducible** (identical SHA-256 hashes across consecutive runs):

| # | File | Style Name | Substrate | Plate Chemistry | Reproductive Engine | Primary Type Voice | Zone% | Gate Range | Gate Status |
|---|------|------------|-----------|-----------------|---------------------|--------------------|:-----:|:----------:|:-----------:|
| **01** | `01-zurich-modernism.png` | Zurich Concrete Modernism | Coated Artboard `#F5F5F3` | Akzidenz Black `#111111` + Signal Red `#E53935` | Concentric Harmonic Acoustic Arcs + Fibonacci Grid | Akzidenz Grotesk Bold | 52.7% | 35–55% | **PASS ✓** |
| **02** | `02-pop-art-serigraphy.png` | 1960s Pop Art Serigraphy | Bleached Cardstock `#FAF8F5` | Pop Magenta `#E6007A` + Yellow `#FFDE00` + Cyan + Black | 45° Ben-Day Screen + Saturated Organic Silhouette | Exuberant Push Pin Display Sans | 39.6% | 28–48% | **PASS ✓** |
| **03** | `03-tokyo-riso-lab.png` | Tokyo Riso Lab | Cream Vellum `#FCFAF2` | Fluo Pink `#FF4098` + Aqua `#00A4D3` + Carbon | 60-lpi Drum Screen + Optical Multiply | Condensed Bilingual Grotesk | 34.0% | 25–45% | **PASS ✓** |
| **04** | `04-constructivist-agit.png` | Constructivist Agit-Prop | Straw Newsprint `#EAE3D2` | Carbon Black `#1A1918` + Vermilion `#D72626` | Acute Wedge + Shattered Target Disc & Barricade | Monumental Wood Slab + Cyrillic Banners | 23.7% | 20–42% | **PASS ✓** |
| **05** | `05-dutch-matrix-modernism.png`| Dutch Matrix Modernism | Cast-Coated Board `#F4F5F7` | Cobalt Ultramarine `#17369B` + Flame Orange `#F04D23`| 57° Isometric Stepped Diagonal Matrix Grid | Constructed Modular Sans (Crouwel) | 37.0% | 35–55% | **PASS ✓** |
| **06** | `06-thermal-fax-brutalism.png` | Low-Fi Thermal Fax & Teletext | Thermal Roll `#ECE8DC` | Single-Pass Thermal Black `#1C1B1A` | Pure 1-Bit Bayer Matrix Dithering | Fixed-Width Monospace OCR-A | 40.3% | 30–50% | **PASS ✓** |
| **07** | `07-victorian-chromolitho.png` | Victorian Chromolitho Naturalist | Linen Vellum `#F5EFE1` | Bitumen `#2C2523` + Indigo `#25405A` + Umber `#8A5636`| Intaglio Deboss + Fine Crosshatching | Engraved Copperplate Script + Latin Italic | 39.4% | 38–56% | **PASS ✓** |
| **08** | `08-punk-xerox-ransom.png` | 1977 Punk Zine & Xerography | Bond Copy `#EDECE8` | Electrostatic Toner `#181818` + Day-Glo Lemon | High-Contrast Blown-Out Photocopy | Skewed Ransom Cutout Newsprint Tiles | 30.7% | 22–45% | **PASS ✓** |
| **09** | `09-de-stijl-rietveld.png` | De Stijl Neoplasticism | Dutch Pressboard `#F5F3EB` | Primary Red `#D32F2F` + Blue `#19398A` + Yellow + Black| Axonometric Rietveld Chair + Mondrian Grid | Theo van Doesburg Modular Block Sans | 47.3% | 38–58% | **PASS ✓** |
| **10** | `10-braun-patent-schematic.png` | Braun Industrial Patent Schematic| Drafting Grid `#F8F8F6` | India Ink `#1C1D1F` + Bauhaus Yellow `#F5A623` | ISO Line Weights + Isometric Assembly | DIN 1451 Mittelschrift + Spec Tables | 42.3% | 32–52% | **PASS ✓** |

---

## Machine-Readable System Catalogs

All design rules are centralized under `design-system/`:
- [`design-system/styles.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/styles.json): Definitions, lineages, and gates for all 10 styles.
- [`design-system/colors.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/colors.json): 10 physical substrates and 23 spot pigments with precise RGB/hex chemistry.
- [`design-system/compositions.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/compositions.json): 10 composition geometry rules and spatial bounds.
- [`design-system/typography.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/typography.json): Typographic roles, leading, tracking, and scale jump limits.
- [`design-system/imperfections.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/imperfections.json): Seeded analog reproduction flaws (plate drift, burnout lines, drum scratches, baren swirls).
- [`design-system/rhythm.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/rhythm.json): Visual tension classifications and focal events.

---

## Files in this Repository

- `SKILL.md`: Complete agent skill document enabling any LLM/agent to resolve recipe manifests and generate 5-paragraph production prompts.
- `stylelib.py`: Core Python/PIL rendering engine implementing optical overprint multiply, 1-bit dithering, crosshatching, and font abstraction.
- `render_styles_gallery.py`: Executable gallery generator for all 10 posters with programmatic gate auditing.
- `styles_gallery/*.png`: The 10 high-resolution posters (1200x1600).
- `styles_contact_sheet.png`: High-resolution visual contact sheet showing all 10 styles side-by-side.
