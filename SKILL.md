---
name: material-styles
description: Generate original, physically grounded editorial posters, prints, and visual systems across 10 systematic design styles (Zurich Concrete Modernism, 1960s Pop Art Serigraphy, Tokyo Riso Lab, Constructivist Agit-Prop, Dutch Matrix Modernism, Low-Fi Thermal Fax, Victorian Chromolitho Naturalist, 1977 Punk Xerox, De Stijl Neoplasticism, Braun Industrial Patent). Models substrate chemistry, spot plate separations, mechanical screening, typographic scale jumps, and seeded analog imperfections. Use whenever creating authentic print posters, album art, editorial layouts, zines, packaging, or generative Python vector scripts.
---

# Material Styles: 10 Systematic Physical Design Systems

Turn any subject, phrase, music album, technical brief, or visual concept into an original editorial artifact grounded in authentic physical printing mechanics:

$$\text{Substrate Chemistry} + \text{Plate Separations} + \text{Reproduction Engine} + \text{Typographic Hierarchy} + \text{Seeded Imperfections}$$

Never output generic digital styling, flat RGB color washes, or superficial "retro" filter effects. Every composition must follow the physical laws and machine-readable catalogs in `design-system/`.

---

## The 10 Design Directions

| # | Style ID | Primary Lineage | Substrate | Spot Pigments & Inks | Reproductive System | Empty Paper Gate |
|---|----------|-----------------|-----------|----------------------|---------------------|:----------------:|
| **01** | `style_zurich_modernism` | Josef Müller-Brockmann, Max Bill (*Zürich Concrete 1958*) | Coated Artboard `#F5F5F3` | Pitch Black `#111111` + Signal Red `#E53935` | Concentric harmonic acoustic arcs, 45° dynamic diagonal axes, Akzidenz-Grotesk | **35–55%** |
| **02** | `style_pop_art_serigraphy` | Sister Corita Kent, Milton Glaser (*Push Pin Studios 1968*) | Bleached Cardstock `#FAF8F5` | Pop Magenta `#E6007A`, Yellow `#FFDE00`, Cyan `#009FE3`, Black | 45° Ben-Day screen halftone field, exuberant organic floral silhouettes, hand-pulled misregistration | **28–48%** |
| **03** | `style_tokyo_riso_lab` | Japanese Under-Press, Multichrome Risograph | Cream High-Bulk Vellum `#FCFAF2` | Fluo Pink `#FF4098`, Aqua `#00A4D3`, Carbon Black | 60-lpi coarse drum screens, subtractive optical multiply overprints, 2mm misregistration drift | **25–45%** |
| **04** | `style_constructivist_agit` | El Lissitzky (*Red Wedge 1919*), Alexander Rodchenko (*VKHUTEMAS*) | Straw Newsprint `#EAE3D2` | Carbon Black `#1A1918` + Vermilion Red `#D72626` | Split black/straw spatial field, acute piercing wedge, cleaved disc fracture, woodblock relief striations, Cyrillic wood-type | **20–42%** |
| **05** | `style_dutch_matrix_modernism` | Wim Crouwel (*Total Design*, *Stedelijk Catalogus 1968*) | Cast-Coated Board `#F4F5F7` | Cobalt Ultramarine `#17369B` + Flame Orange `#F04D23` | 57° isometric stepped matrix, constructed modular block sans, 3-column architectural metadata | **35–55%** |
| **06** | `style_thermal_fax_brutalism` | Subculture Teletext, POS Thermal Roll | Thermal Receipt Roll `#ECE8DC` | Single-Pass Thermal Black `#1C1B1A` | Pure 1-bit Bayer matrix dithering (no gray pixels), OCR-A monospace, telemetry data burst, burnout line | **30–50%** |
| **07** | `style_victorian_chromolitho` | Ernst Haeckel (*Kunstformen der Natur*), Linnaean Plates | Linen Vellum `#F5EFE1` | Bitumen `#2C2523`, Indigo `#25405A`, Burnt Umber `#8A5636` | Intaglio debossed plate border, fine copperplate crosshatching, engraved script + Latin binomials | **38–56%** |
| **08** | `style_punk_xerox_ransom` | Jamie Reid (*Sex Pistols*), 1977 London/NYC Fanzines | Bond Copy `#EDECE8` | Electrostatic Toner `#181818` + Day-Glo Lemon `#FFE800` | High-contrast blown-out photocopy, torn newsprint ransom blocks, cut-and-paste tape mask, toner drum streaks | **22–45%** |
| **09** | `style_de_stijl_rietveld` | Gerrit Rietveld (*Rood-blauwe stoel 1918*), Theo van Doesburg | Unbleached Dutch Pressboard `#F5F3EB` | Primary Cadmium Red `#D32F2F`, Blue `#19398A`, Yellow `#F9C80E`, Black | Axonometric 3D Rietveld chair projection with primary yellow end-caps, Mondrian Cartesian planes, modular sans | **38–58%** |
| **10** | `style_braun_patent_schematic` | Dieter Rams, Bauhaus Industrial Drawing Office | Metric Drafting Grid `#F8F8F6` | Technical India Ink `#1C1D1F` + Signal Yellow `#F5A623` | ISO line-weight hierarchy (0.5/0.25mm), exploded isometric assembly, dimension witness lines, DIN spec tables | **32–52%** |

---

## Agent Decision Matrix: Style Selection Guide

When a user provides a topic, subject, or brief without naming a style, map their intent using this matrix:

| User Intent or Subject Domain | Recommended Style | Why |
|--------------------------------|-------------------|-----|
| **Classical Music, Acoustic Performance, Avant-Garde Sound, Architecture** | `style_zurich_modernism` | Harmonic concentric arcs model sound propagation and mathematical resonance. |
| **Joyful Proclamations, Youth Culture, Psychedelia, Pop Art, Optimism** | `style_pop_art_serigraphy` | Saturated flat pigments, vibrant Ben-Day halftones, and organic silhouettes create immediate graphic joy. |
| **Underground Electronic Music, Tokyo Indie, Nightlife, Multichrome Prints** | `style_tokyo_riso_lab` | Overprinting fluorescent pink and aqua creates vibrant purple optical intersections. |
| **Revolutionary Politics, Manifestos, Urgent Proclamations, Avant-Garde Agit** | `style_constructivist_agit` | Acute diagonal force vectors and fractured geometric tension deliver unstoppable polemic impact. |
| **Corporate Identity Systems, Typography Lectures, Exhibition Catalogs, Logic** | `style_dutch_matrix_modernism` | Rigid isometric grid discipline and modular letterforms convey rigorous systemic intelligence. |
| **Hacker Subculture, Telemetry, Ambient Noise, Cryptography, Terminal Output** | `style_thermal_fax_brutalism` | 1-bit Bayer matrix dithering and thermal paper artifacts embody raw computational transmission. |
| **Botanical Specimens, Zoology, Oceanography, Historical Archives, Natural History** | `style_victorian_chromolitho` | Copperplate intaglio hatching and Latin nomenclature deliver timeless scientific reverence. |
| **Punk Rock, DIY Zines, Counter-Culture, Underground Protests, Noise Gigs** | `style_punk_xerox_ransom` | High-contrast electrostatic toner grit and torn paper ransom typography express direct street resistance. |
| **Modernist Furniture, Interior Design, De Stijl Art, Structural Purity** | `style_de_stijl_rietveld` | The primary triad and axonometric Rietveld timber chair embody pure spatial neoplasticism. |
| **Industrial Hardware, Patents, Consumer Electronics, Engineering Manuals** | `style_braun_patent_schematic` | Exploded isometric assemblies and DIN callouts communicate German functionalist precision. |

---

## The Universal Recipe Manifest

Before generating an image prompt or running a rendering script, resolve the input into this deterministic YAML manifest:

```yaml
style_id: style_pop_art_serigraphy
subject: "A blooming wild poppy flower celebrating urban renewal"
intent: "Civic proclamation celebrating creative liberation"
exact_text: "POWER & JOY"
text_language: "English"
representation: "Saturated flat silkscreen silhouette with optical Ben-Day screening"
ratio: "3:4 vertical poster"
substrate:
  id: sub_bleached_cardstock
  hex: "#FAF8F5"
  finish: "Smooth heavy bleached printmaking cardstock, uncoated tooth"
palette:
  id: palette_pop_serigraphy
  dominant:
    name: "Pop Squeegee Black"
    hex: "#18181A"
    role: "Display lettering and deep silhouette accent"
  accents:
    - name: "Hot Pop Magenta"
      hex: "#E6007A"
      role: "Inner floral blossom and background glow"
    - name: "Sunshine Pop Yellow"
      hex: "#FFDE00"
      role: "Central disc, radiant petals, and slogan banner"
    - name: "Pop Cerulean Cyan"
      hex: "#009FE3"
      role: "Coarse 45-degree Ben-Day screen halftone field"
composition:
  family: comp_pop_collision
  grid: "Asymmetrical poster grid with 2-inch bottom proclamation banner"
  empty_paper_percent: 39
  visual_tension: "vibrant_collision"
  focal_event: "Radiant multi-petaled organic flower silhouette colliding with Ben-Day screen"
  release_zone: "Unprinted bleached cardstock margins at upper corners and top margin"
typography:
  display_voice: "Exuberant Push Pin heavy display sans with two-color drop shadow"
  support_voice: "Condensed sans-serif banner text and technical workshop imprint"
  scale_jump: "8:1 ratio between display headline and footer notes"
imperfections:
  - "Hand-pulled silkscreen registration drift: 1.5mm cyan plate shift"
  - "Margin silkscreen registration target crosshairs at four corners"
```

---

## Output Mode A: The 5-Paragraph Production Prompt

When compiling a prompt for AI image generators (Midjourney v6, Flux 1.1 Pro, Imagen 3, SDXL), compile the Recipe Manifest into exactly **5 structured paragraphs**:

### Paragraph Structure
1. **Substrate & Ink Chemistry**: Explicit physical paper substrate (tooth, weight, base hex `#XXXXXX`) and exact spot color separations. Prohibit digital RGB washes.
2. **Composition & Spatial Tension**: Geometry, grid system, alignment anchors, empty paper percentage gate, release zone location, and the single focal event.
3. **Subject Reproduction Mechanics**: The exact physical reproductive engine (e.g. 45° Ben-Day screen, 1-bit Bayer matrix dither, relief woodblock striations, copperplate crosshatching, axonometric orthographic projection).
4. **Typographic Hierarchy & Voices**: Exact headline text (in quotes), line breaks, casing, support voices, scale jump ratio, and structural baseline alignment.
5. **Physical Imperfections & Exclusions**: Seeded analog imperfections (registration drift, plate bite, toner grit). End with an explicit negative exclusion block.

### Example Production Prompt: Style 04 (Constructivist Agit-Prop)
> A museum-grade Russian Constructivist agit-prop editorial poster printed on heavy, unbleached straw newsprint substrate (#EAE3D2) with visible natural wood fibers and a matte press finish. Two-color physical spot printing ink separation using dense letterpress Carbon Black (#1A1918) and high-saturation revolutionary Vermilion Red (#D72626). No digital color gradations or smooth computer gradients.
>
> Asymmetric spatial tension dividing the 3:4 vertical composition: the right side features a towering, deep carbon black angular geometric void, while the left field remains open straw newsprint with 24% empty paper space. A massive acute Vermilion Red triangle wedge pierces from the left edge deep into the heart of a large off-white circular target disc situated inside the black void.
>
> The red wedge is detailed with authentic woodblock relief striations running horizontally across its entire span. The lower-right sector of the white target disc is violently cleaved and displaced downwards into the black void, surrounded by floating sharp polygonal debris shards. Pure graphic vector execution with razor-sharp plate edges.
>
> Monumental Russian constructivist typography: the word 'БЕЙ' set in massive black letterpress wood-type at the top left beside a solid red square; 'БЕЛЫХ' printed in bold straw paper lettering centered inside the upper black void; and 'КЛИНОМ КРАСНЫМ' set inside the red wedge angled along its 22-degree diagonal axis. Bottom section features interlocking Rodchenko-style horizontal banners: 'BEAT THE OLD WITH THE NEW!' in reverse knockout type on a black bar, with 'ALL POWER TO REVOLUTIONARY UTILITY' below on a vermilion bar, accompanied by solid triangle arrow indicators and 'VKHUTEMAS 1920'.
>
> Seeded printing imperfections: subtle woodcut ink squash along the wedge contours and faint letterpress roller bite into the straw paper. Explicit exclusions: no 3D rendering, no glossy lighting, no digital drop shadows, no soft airbrushing, no photo realism, no distressed grunge filters, no generic modern decorative clutter.

---

## Output Mode B: Deterministic Code Rendering (`stylelib.py`)

When generating deterministic, programmatic vector/raster artwork, use the project's built-in rendering engine [`stylelib.py`](file:///Users/ahmetbektes/WDesignspace/mono-color/stylelib.py).

### Quick Code Blueprint
```python
from stylelib import StylePoster, load_font

# 1. Initialize poster with physical substrate chemistry
P = StylePoster("style_pop_art_serigraphy", "poster_pop_demo", sub_hex="#FAF8F5")
S = P.scale  # Supersampling factor (S=2 for 2400x3200 internal render)

# 2. Add graphic elements with spot pigments
# Draw Ben-Day screen halftone field
P.halftone_field(650, 140, 1100, 590, (0x00, 0x9F, 0xE3), dot_pitch=14, max_r=5.5)

# Draw organic silhouette
P.poly(flower_polygon_points, fill=(0xFF, 0xDE, 0x00))

# 3. Add typographic hierarchy
P.text((90, 140), "POWER & JOY", "grotesk_bold", 108, (0x18, 0x18, 0x1A), tracking=-2)
P.text((90, 1260), "ALL POWER TO THE IMAGINATION!", "din_bold", 24, (0x18, 0x18, 0x1A), tracking=4)

# 4. Define zone mask and finish with numeric empty paper gating
def zm(dm):
    dm.rectangle([60 * S, 60 * S, 1140 * S, 1540 * S], fill=255)

result = P.finish(zmask=P.create_mask(zm), gate_range=(28, 48))
assert result["gate_ok"], f"Empty paper gate failed: {result['zempty']:.1f}%"
```

---

## Machine-Readable System Catalog Links

All design rules, palettes, and gates are strictly defined in `design-system/`:
- [`design-system/styles.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/styles.json): All 10 styles, historic lineages, and empty paper gates.
- [`design-system/colors.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/colors.json): Substrate chemistry (RGB, tooth, weight) and spot pigments.
- [`design-system/compositions.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/compositions.json): Geometry layouts, axes, and grid rules.
- [`design-system/typography.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/typography.json): Letterform skeletons, tracking, and scale jumps.
- [`design-system/imperfections.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/imperfections.json): Seeded physical flaws and registration parameters.
- [`design-system/rhythm.json`](file:///Users/ahmetbektes/WDesignspace/mono-color/design-system/rhythm.json): Visual tension, focal events, and quiet release zones.
