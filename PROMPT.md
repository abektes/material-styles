# mono-color experiment — lighthouse

The mono-color skill is designed to feed an AI image generator. This experiment
instead compiled its Recipe Manifest into a deterministic Python/PIL renderer
(`render_poster.py`), producing the same artifact twice with byte-identical
output (sha256 `79572965…f7d6`), proving the catalogs are complete enough to
drive a printer-like program, not just a prompt.

## Recipe Manifest

```yaml
subject: lighthouse
intent: poetic observation
exact_text: "the light rotates anyway"
text_language: English
representation: faithful reproduction (no source image; built from identifying anchors)
ratio: 3:4
carrier: none
substrate: substrate_neutral_white #FAFAF7
mode: complementary duotone
palette: palette_cobalt_terracotta
inks: Cobalt #2148B8 + Terracotta #C65F38
plate_roles: cobalt = structure (tower, sea, headline); terracotta = light (lamp, beam, reflection, date, aside)
layout: composition_editorial_cover
empty_paper: 54.8% (global gate 25-55 pass; family range 25-45 exceeded — see findings)
visual_tension: relaxed
focal_event: headline locked through the tower via a full-width paper channel
release_zone: upper-right pale field beside the beam fade
unresolved_edge: beam dots fade before the right frame
image_treatment: medium screening; ink pools solid at depth
type_hierarchy: type_literary (serif display 200px / grotesk micro 17px / mono data 15px = 11x jump)
disruption: headline channel cuts the tower
imperfection_seed: md5("lighthouse|the light rotates anyway|palette_cobalt_terracotta|composition_editorial_cover") = 1496745725
imperfections: imperfection_halftone_drift (7% dot jitter), imperfection_registration_drift (accent plate offset ~1.5mm)
```

## Compiled generation prompt (five paragraphs, per the Prompt Compiler)

1. Canvas and ink: 3:4 vertical poster on flat front-facing Neutral White `#FAFAF7`, chosen for a crisp contemporary cultural subject. Two-ink complementary duotone: Cobalt `#2148B8` as the dominant structural plate (tower mass, sea, headline, horizon rule; ~80% of printed area) and Terracotta `#C65F38` as the accent plate carrying light and annotation (lamp room, beam, water reflection, date, circled aside; ~20%). No third ink; overlap zones are butt-fit plate separations, not blends.

2. Original composition: editorial cover family, relaxed tension. One focal event: the headline locked into a full-width paper channel knocked through the lighthouse tower mid-page, so type and object form one collision lockup. Release zone: the upper-right quadrant, held quiet beside the beam's screened fade (the beam fades before the right frame — the one unresolved edge). Margins ~7%; ~55% visibly empty paper; one manual gesture only: a small circled aside "checked nightly" below the beam path; sea bleeds off the bottom edge, horizon rule bleeds both side edges.

3. Subject: a lighthouse built from identifying anchors — tapered striped tower, gallery slab, lantern room, one beam, sea horizon. Faithful representation through medium screening: cobalt halftone sea deepening from the horizon until ink pools solid at depth, where the coordinate microcopy is knocked out of the pooled ink as paper text; paper shows through the tower's stripe bands and the headline channel; terracotta reflection wedge continues the beam axis below the horizon, butt-fit against cobalt dots.

4. Typography and words: Literary role — lowercase serif display "the light / rotates / anyway" at ~11x scale over the microcopy, tight leading, natural line breaks, entering and crossing the object. Support voices: letterspaced grotesk kicker "FIELD NOTES — NORTH ATLANTIC", mono data strip "54.6°N 8.4°E — FL.W 5S" (knockout) and terracotta mono date "SEP 2026 — NO. 07". Handwriting appears only as the single circled aside, never as factual text.

5. Material and avoids: visible halftone dots at close range, legible at thumbnail scale; 7% halftone density drift; ~1.5mm registration drift on the accent plate only (visible at the lamp room). Exclude: any third color, gradients, full-color photography, digital color-wash monochrome, glossy mockups, 3D depth, lens blur, centered symmetry, retro aging, sepia, distressed borders, marketing copy, logos, QR codes.

## Measured result vs. catalog

| Metric | Catalog range | Measured |
|---|---|---|
| Empty paper (global gate) | 25–55% | 54.8% ✓ |
| Empty paper (editorial cover family) | 25–45% | 54.8% ✗ |
| Accent share of ink | 15–30% | 20.4% ✓ |
| Dominant plate share | 70–85% | 79.6% ✓ |
| Type scale jump (Literary) | 6:1–12:1 | ~11:1 ✓ |
| Imperfections (contemporary) | 0–2 | 2 ✓ |
| Determinism (same seed → same output) | required | byte-identical ✓ |
