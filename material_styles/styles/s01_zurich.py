"""01. Zurich Concrete Modernism (Josef Müller-Brockmann, Max Bill 1958)."""
from typing import Optional
from material_styles.core.content import PosterContent
from material_styles.core.poster import StylePoster, S, UW, UH, W, H
from material_styles.styles.base import BaseStyle, StyleMetadata

SUB_ARTBOARD = (0xF5, 0xF5, 0xF3)
INK_ZURICH_BLACK = (0x11, 0x11, 0x11)
INK_SWISS_RED = (0xE5, 0x39, 0x35)


class ZurichModernismStyle(BaseStyle):
    metadata = StyleMetadata(
        id="style_zurich_modernism",
        number=1,
        name="Zurich Concrete Modernism",
        lineage="Josef Müller-Brockmann, Max Bill (Zürich Concrete 1958)",
        substrate_hex="#F5F5F3",
        substrate_rgb=SUB_ARTBOARD,
        inks=[INK_ZURICH_BLACK, INK_SWISS_RED],
        gate_range=(35, 55),
        description="Concentric harmonic acoustic arcs, 45-degree diagonal axes, Akzidenz-Grotesk",
        slug="01-zurich-modernism",
        default_content=PosterContent(
            headline="musica viva",
            subhead="tonhalle zürich",
            accession_code="4. KONZERT DER TONHALLE-GESELLSCHAFT",
            footnote="DIRIGENT: HANS ROSBAUD // SOLIST: WOLFGANG SCHNEIDERHAN",
        ),
    )

    def render(
        self,
        P: Optional[StylePoster] = None,
        content: Optional[PosterContent] = None,
        outdir: str = "styles_gallery",
    ) -> dict:
        if P is None:
            P = self.create_poster()
        content = content or self.metadata.default_content
        headline = content.get_slot("headline", "musica viva")
        subhead = content.get_slot("subhead", "tonhalle zürich")
        accession = content.get_slot("accession_code", "4. KONZERT DER TONHALLE-GESELLSCHAFT")
        footnote = content.get_slot("footnote", "DIRIGENT: HANS ROSBAUD // SOLIST: WOLFGANG SCHNEIDERHAN")

        dx, dy = P.drift

        # Concentric harmonic acoustic arcs radiating from lower-right pole (860, 1220)
        pole_x, pole_y = 860, 1220
        radii = [180, 320, 490, 700, 960, 1260]
        for idx, r in enumerate(radii):
            w = 4.0 + idx * 3.5
            P.ring(pole_x, pole_y, r, w, INK_ZURICH_BLACK)

        # Broad solid acoustic sector (between r=490 and r=680)
        for r in range(490, 680, 10):
            P.ring(pole_x, pole_y, r, 12.0, INK_ZURICH_BLACK)

        # 45-degree diagonal structural axis cutting through
        P.line([(90, 450), (1110, 1470)], INK_ZURICH_BLACK, w=2.0)

        # Intersecting Swiss Signal Red circle with drift
        P.ell(280 + dx, 680 + dy, 520 + dx, 920 + dy, INK_SWISS_RED)

        # Monolithic Akzidenz Grotesk typography
        P.text((90, 140), headline, "grotesk_bold", 116, INK_ZURICH_BLACK, tracking=-2)
        P.text((90, 260), subhead, "grotesk_bold", 52, INK_SWISS_RED, tracking=-1)

        P.text((90, 340), accession, "grotesk_bold", 16, INK_ZURICH_BLACK, tracking=2)
        P.text((90, 370), "DIENSTAG, 28. JANUAR 1958, 20.15 UHR", "grotesk", 15, INK_ZURICH_BLACK, tracking=1)
        P.text((90, 400), footnote, "grotesk", 15, INK_ZURICH_BLACK, tracking=1)
        P.text((90, 430), "WERKE VON IGOR STRAVINSKY, BÉLA BARTÓK, PAUL HINDEMITH", "grotesk", 15, INK_ZURICH_BLACK, tracking=1)

        # Registration cross marks in margins
        rx, ry = 1110 + dx, 1500 + dy
        P.ring(rx, ry, 12, 1.0, INK_SWISS_RED)
        P.line([(rx - 16, ry), (rx + 16, ry)], INK_SWISS_RED, w=1.0)
        P.line([(rx, ry - 16), (rx, ry + 16)], INK_SWISS_RED, w=1.0)

        def zm(dm):
            dm.rectangle([90 * S, 140 * S, 880 * S, 480 * S], fill=255)
            dm.rectangle([180 * S, 560 * S, 960 * S, 1380 * S], fill=255)

        return P.finish(outdir=outdir, zmask=P.create_mask(zm), gate_range=self.metadata.gate_range)
