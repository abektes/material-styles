# mono-color gallery — 10 deterministic examples

Ten posters generated with the [mono-color skill](https://github.com/yanliudesign/mono-color-skill)'s
design system, rendered as code instead of AI image prompts. Each poster resolves a
full Recipe Manifest from the skill's `design-system/*.json` catalogs and is drawn by
`render_gallery.py` + `monolib.py` (Python/PIL, no randomness beyond the seeded
imperfections). **Re-running the script reproduces every PNG byte-for-byte** (verified:
two consecutive runs produce identical SHA-256 hashes for all ten files).

The skill's numeric gates were checked programmatically for every poster: empty paper
(measured as canvas minus composed-content silhouettes) within the global 25–55% band
*and* its composition family's dominance band, accent-ink share 15–30% of printed ink,
dominant plate 70–85%, and the family's type scale ratio. `zone%` below is the
silhouette-based empty-paper measure; `px%` is raw non-substrate pixels, reported for
reference. A visual QA pass (three independent reviewers) passed all ten.

| # | file | subject / phrase | family | mode · inks | type | zone% | family band |
|---|------|------------------|--------|-------------|------|-------|-------------|
| 01 | `01-fern-archive.png` | fern · "the archive of green" | archival plate | duotone · Botanical Green `#008A4B` + Oxblood `#8F3434` on Pale Beige | Literary serif + mono plate data | 54.1 | 40–55 ✓ |
| 02 | `02-night-market.png` | night market · "lanterns lit at dusk" | object field | duotone · Tangerine `#E46C2D` + Slate Blue `#4773A5` on White | Cultural Grotesk + mono | 49.8 | 25–50 ✓ |
| 03 | `03-midnight-ride.png` | night ride · "MIDNIGHT RIDE" | ruled information | duotone · Ultramarine `#263E99` + Safety Orange `#E55D2B` on White | Condensed Civic + mono facts | 51.6 | 35–55 ✓ |
| 04 | `04-still-steaming.png` | tea · "still steaming" | editorial journal | **pure one-ink** · Terracotta `#C65F38` on Pale Beige | Literary serif + mono | 42.2 | 35–55 ✓ |
| 05 | `05-harbour-gull.png` | harbour gull · "NO RENT" | image field | duotone · Charcoal `#30343A` + Signal Red `#C83232` on Cool Gray | Rotated-free serif display + mono | 34.0 | 20–40 ✓ |
| 06 | `06-sound-check.png` | sound check · "SOUND CHECK" | overprint collage | **overprint duotone** · Electric Blue `#173AE3` × Carbon `#242321` on White | Cultural Grotesk interlocked caps | 39.0 | 20–40 ✓ |
| 07 | `07-paper-keeps.png` | keeping things · "PAPER KEEPS THINGS" | type-led declaration | duotone · Mint `#5EB783` + Charcoal `#302D2E` on Cool Gray | Typographic Object serif, page-filling | 30.2 | 20–45 ✓ |
| 08 | `08-the-pool.png` | public pool · "THE POOL IS OPEN" | editorial cover | duotone · Powder Blue `#9EB8D3` + Signal Red `#C83232` on White | wide grotesk + mono | 25.6 | 25–45 ✓ |
| 09 | `09-night-log.png` | moon phases · "three moods of the same light" | specimen annotation | **pure one-ink** · Aubergine `#63365F` on Pale Beige | Literary serif + mono labels | 54.5 | 35–55 ✓ |
| 10 | `10-the-long-way.png` | summer walk · "walk until the town ends" | editorial cover | **pure one-ink** · Royal Blue `#2058D4` on White | Literary serif + mono km marks | 39.2 | 25–45 ✓ |

Across the set: all 9 layout families (image field ×2), 12 of the catalog's palettes,
4 type roles, both one-ink and all four two-ink modes' plate logic, all three
substrates, and 0–2 controlled imperfections per poster (stable md5 seed per recipe;
registration drift on accent plates, halftone/density jitter, pale second impressions
in one-ink work).

## Print-logic features demonstrated

- **Plate knockouts** — headline channels cut through the fern plate frame (01),
  the lighthouse-style channel (04), white type where SOUND CHECK crosses the blue ring (06),
  title knocked out where the road passes under it (10).
- **Paper as a shape** — the gull's white head is exposed substrate on the gray page (05);
  stripe bands and mullions are paper, not white ink.
- **Halftone reproduction** — screened seas, pools, suns, steam and sky haze with
  cataloged 7% dot jitter; ink density pooling to solid at depth.
- **Overprint physics** — 06's overlap zone is the multiply of the two inks, not a third color.
- **Registration drift** — accent plates offset ~1.5 mm (02, 03, 08); in one-ink posters
  drift appears only as a pale second impression of the same ink (04 title, 09 crescent).

## Files

- `gallery/*.png` — the ten posters (1200×1600, 3:4)
- `contact-sheet.png` — all ten at thumbnail scale
- `render_gallery.py` — the ten recipes; `python render_gallery.py` regenerates everything
- `monolib.py` — rendering engine (poster canvas, plates, masks, halftone, type, gestures, metrics)
- `render_poster.py`, `lighthouse-monocolor.png`, `PROMPT.md` — the original single-poster experiment

Known limitation: DejaVu fonts stand in for the editorial serif/grotesk/mono voices
(no font files in this environment); the catalogs' type *roles* are followed, the exact
letterforms are not.
