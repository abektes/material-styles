# Material Styles — 15 Systematic Physical Design Systems

A comprehensive generative and programmatic design architecture inspired by and expanding upon the [mono-color skill](https://github.com/yanliudesign/mono-color-skill).

Instead of treating design styles as arbitrary prompt adjectives ("ultra-detailed", "retro", "aesthetic"), this system models **physical reproduction physics**:
1. **Substrate Chemistry**: Paper stock weight, fiber tooth, and base RGB chemistry.
2. **Plate Separation**: Explicit plate roles, named pigments, opacity, and subtractive optical multiply.
3. **Reproduction Mechanics**: Rotated halftone screening, CMYK rosette angles, linocut relief, CRT scanlines, 1-bit Bayer matrix dithering, copperplate crosshatching, intaglio debossing, and contact photograms.
4. **Typographic Scale Jump**: Disciplined hierarchies with 5:1 to 18:1 display-to-support jumps.
5. **Controlled Analog Imperfections**: Deterministic seeded flaws (registration drift, baren ink starvation, toner drum scratches, thermal head burnouts, chemical tide lines).
6. **Mathematical Gates**: Strict programmatic bounds on empty paper percentage and plate ink distribution.

---

## 15-Style Verification Matrix

All 15 posters were generated with `render_styles_gallery.py` + `stylelib.py` (Python/PIL) and verified to be **100% byte-for-byte reproducible** (identical SHA-256 hashes across consecutive runs):

| # | File | Style Name | Substrate | Plate Chemistry | Reproductive Engine | Primary Type Voice | Zone% | Gate Range | Gate Status |
|---|------|------------|-----------|-----------------|---------------------|--------------------|:-----:|:----------:|:-----------:|
| **01** | `01-zurich-modernism.png` | Zurich Concrete Modernism | Coated Artboard `#F5F5F3` | Akzidenz Black `#111111` + Signal Red `#E53935` | Concentric Harmonic Acoustic Arcs + Fibonacci Grid | Akzidenz Grotesk Bold | 52.7% | 35–55% | **PASS ✓** |
| **02** | `02-pop-art-serigraphy.png` | 1960s Pop Art Serigraphy | Bleached Cardstock `#FAF8F5` | Pop Magenta `#E6007A` + Yellow `#FFDE00` + Cyan + Black | Multi-Angle Ben-Day Screens (15°/75°) + Double-Exposed Muse | Exuberant Push Pin Display Sans | 38.4% | 28–48% | **PASS ✓** |
| **03** | `03-tokyo-riso-lab.png` | Tokyo Riso Lab | Cream Vellum `#FCFAF2` | Fluo Pink `#FF4098` + Aqua `#00A4D3` + Carbon | 60-lpi Drum Screen + Optical Multiply | Condensed Bilingual Grotesk | 34.0% | 25–45% | **PASS ✓** |
| **04** | `04-constructivist-agit.png` | Constructivist Agit-Prop | Straw Newsprint `#EAE3D2` | Carbon Black `#1A1918` + Vermilion Red `#D72626` | Shouting Megaphone + Linocut Striations + Cyrillic Wood-Type (*КНИГИ*) | Monumental Wood Slab + Agit Banners | 24.6% | 20–42% | **PASS ✓** |
| **05** | `05-dutch-matrix-modernism.png`| Dutch Matrix Modernism | Cast-Coated Board `#F4F5F7` | Cobalt Ultramarine `#17369B` + Flame Orange `#F04D23`| 57° Isometric Stepped Diagonal Matrix Grid | Constructed Modular Sans (Crouwel) | 37.0% | 35–55% | **PASS ✓** |
| **06** | `06-thermal-fax-brutalism.png` | Low-Fi Thermal Fax & Teletext | Thermal Roll `#ECE8DC` | Single-Pass Thermal Black `#1C1B1A` | Pure 1-Bit Bayer Matrix Dithering | Fixed-Width Monospace OCR-A | 40.3% | 30–50% | **PASS ✓** |
| **07** | `07-victorian-chromolitho.png` | Victorian Chromolitho Naturalist | Linen Vellum `#F5EFE1` | Bitumen `#2C2523` + Indigo `#25405A` + Umber `#8A5636`| Intaglio Deboss + Fine Crosshatching | Engraved Copperplate Script + Latin Italic | 39.4% | 38–56% | **PASS ✓** |
| **08** | `08-punk-xerox-ransom.png` | 1977 Punk Zine & Xerography | Bond Copy `#EDECE8` | Electrostatic Toner `#181818` + Day-Glo Lemon | High-Contrast Blown-Out Photocopy | Skewed Ransom Cutout Newsprint Tiles | 30.7% | 22–45% | **PASS ✓** |
| **09** | `09-de-stijl-rietveld.png` | De Stijl Neoplasticism | Dutch Pressboard `#F5F3EB` | Primary Red `#D32F2F` + Blue `#19398A` + Yellow + Black| Axonometric Rietveld Chair + Mondrian Grid | Theo van Doesburg Modular Block Sans | 47.3% | 38–58% | **PASS ✓** |
| **10** | `10-braun-patent-schematic.png` | Braun Industrial Patent Schematic| Drafting Grid `#F8F8F6` | India Ink `#1C1D1F` + Bauhaus Yellow `#F5A623` | ISO Line Weights + Isometric Assembly | DIN 1451 Mittelschrift + Spec Tables | 42.3% | 32–52% | **PASS ✓** |
| **11** | `11-sosaku-hanga-woodcut.png` | Japanese Sōsaku-Hanga Woodcut | Echizen Washi `#F3EFE6` | Sumi Soot `#1E1C1A` + Cinnabar Vermilion `#C8382B` | Linocut Relief Crane + Baren Rubbing Starvation | Chiseled Block Woodcut + Hanko Seals | 38.4% | 30–50% | **PASS ✓** |
| **12** | `12-swiss-cyber-newwave.png` | 1980s Swiss Cyber New Wave | Kromekote Gloss `#F8F8FC` | Laser Cyan `#00E5FF` + Acid Chartreuse + Magenta + Dark | 3D Wireframe Cube + CMYK Rosettes + Scanlines | Tilted Stepped Univers + Geneva Mono | 32.2% | 25–45% | **PASS ✓** |
| **13** | `13-blue-note-hardbop.png` | 1950s Blue Note Hard Bop | LP Jacket Board `#F7F5EE` | Velvet Gravure Black `#101012` + Cadmium Ochre `#E09B19` | 45° Francis Wolff Halftone Saxophone Crop | Monumental Compressed Wood-Type Sans | 24.2% | 20–42% | **PASS ✓** |
| **14** | `14-bauhaus-typofoto.png` | Bauhaus Photogram & Typofoto | Darkroom Stock `#EDE8DF` | Silver Gelatin Black `#141416` + Bayer Red `#E02E1B` | Camereless Optical Photogram + Red Focal Ray | Herbert Bayer Universal Lowercase Type | 35.2% | 35–55% | **PASS ✓** |
| **15** | `15-polish-surrealism.png` | Polish Poster School Surrealism | Warsaw Offset `#EBE3D0` | Poison Olive `#4D592B` + Crimson Rust + Charcoal | Visceral Biological Paper-Cut Contour + Concentric Rings| Hand-Brushed Lithographic Tusche Script | 36.4% | 28–48% | **PASS ✓** |

---

## Machine-Readable System Catalogs

All design rules are centralized under `design-system/`:
- [`design-system/styles.json`](design-system/styles.json): Definitions, lineages, and gates for all 15 styles.
- [`design-system/colors.json`](design-system/colors.json): 15 physical substrates and 37 spot pigments with precise RGB/hex chemistry.
- [`design-system/compositions.json`](design-system/compositions.json): 15 composition geometry rules and spatial bounds.
- [`design-system/typography.json`](design-system/typography.json): Typographic roles, leading, tracking, and scale jump limits.
- [`design-system/imperfections.json`](design-system/imperfections.json): Seeded analog reproduction flaws (plate drift, burnout lines, drum scratches, baren swirls).
- [`design-system/rhythm.json`](design-system/rhythm.json): Visual tension classifications and focal events.

---

## Files in this Repository

- `SKILL.md`: Complete agent skill document enabling any LLM/agent to resolve recipe manifests and generate 5-paragraph production prompts.
- `stylelib.py`: Core Python/PIL rendering engine implementing optical overprint multiply, rotated halftones, CMYK rosettes, linocut relief, scanlines, and Bayer dithering.
- `render_styles_gallery.py`: Executable gallery generator for all 15 posters with programmatic gate auditing and master contact sheet compositor.
- `styles_gallery/*.png`: The 15 high-resolution posters (1200×1600).
- `styles_contact_sheet.png`: High-resolution visual contact sheet showing all 15 styles side-by-side in a 3×5 grid (1644×1510).
