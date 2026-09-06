"""Unified CLI suite for material-styles."""
import argparse
import sys
from typing import List

from material_styles.audit import audit_all, audit_style
from material_styles.core.content import PosterContent
from material_styles.registry import registry, render_poster
from material_styles.scaffold import scaffold_style


def cmd_list(args):
    """List all registered physical design styles."""
    styles = registry.list_styles()
    print("=" * 90)
    print(f"{'#':2} {'Style ID':30} {'Style Name':35} {'Gate':>9}")
    print("-" * 90)
    for s in styles:
        m = s.metadata
        lo, hi = m.gate_range
        print(f"{m.number:02d} {m.id:30} {m.name:35} {lo:>3}-{hi:<3}%")
    print("=" * 90)
    print(f"Total physical design styles: {len(styles)}")


def cmd_render(args):
    """Render a poster with optional custom content slots."""
    style = registry.get(args.style)
    if style is None:
        print(f"Error: Style '{args.style}' not found. Run 'material-styles list' to view available styles.", file=sys.stderr)
        sys.exit(1)

    print(f"Rendering Style #{style.metadata.number:02d}: {style.metadata.name}...")
    result = render_poster(
        style=style,
        headline=args.headline,
        subhead=args.subhead,
        footnote=args.footnote,
        accession_code=args.accession,
        seed=args.seed,
        output=args.output,
        outdir=args.outdir,
    )
    status = "PASS ✓" if result["gate_ok"] else "FAIL ✗"
    print(f"Saved: {result['path']}")
    print(f"Empty Paper: {result['zempty']:.1f}% (Gate: {result['gate_range'][0]}-{result['gate_range'][1]}%) [{status}]")


def cmd_audit(args):
    """Audit one or all styles for empty paper gates and byte-for-byte SHA-256 determinism."""
    if args.style:
        style = registry.get(args.style)
        if style is None:
            print(f"Error: Style '{args.style}' not found.", file=sys.stderr)
            sys.exit(1)
        res = audit_style(style, outdir=args.outdir)
        status = "PASS ✓" if res["gate_ok"] else "FAIL ✗"
        det = "MATCH ✓" if res["deterministic"] else "MISMATCH ✗"
        print(f"Style #{res['number']:02d} {res['name']}:")
        print(f"  Empty Paper: {res['zempty']:.1f}% | Gate: {res['gate_range'][0]}-{res['gate_range'][1]}% | {status}")
        print(f"  Dual-Pass SHA-256: {det} ({res['sha256'][:16]}...)")
        if not (res["gate_ok"] and res["deterministic"]):
            sys.exit(1)
    else:
        print("=" * 100)
        print("                        MATERIAL STYLES MASTER AUDIT                             ")
        print("=" * 100)
        print(f"{'#':2} {'Style ID':28} {'Zone%':>6} {'Gate':>9} {'Gate Status':>12} {'Dual-Pass SHA-256':>18}")
        print("-" * 100)
        results = audit_all(outdir=args.outdir)
        all_ok = True
        for r in results:
            g_stat = "PASS ✓" if r["gate_ok"] else "FAIL ✗"
            d_stat = "MATCH ✓" if r["deterministic"] else "MISMATCH ✗"
            lo, hi = r["gate_range"]
            print(f"{r['number']:02d} {r['style_id']:28} {r['zempty']:6.1f}% {lo:>3}-{hi:<3}% {g_stat:>12} {d_stat:>18}")
            if not (r["gate_ok"] and r["deterministic"]):
                all_ok = False
        print("=" * 100)
        if all_ok:
            print("All styles verified: 100% gate compliance & 100% SHA-256 reproducibility.")
        else:
            print("Warning: One or more styles failed gate audit or determinism verification.", file=sys.stderr)
            sys.exit(1)


def cmd_new_style(args):
    """Scaffold a new physical style module."""
    path = scaffold_style(
        name=args.name,
        style_id=args.id,
        lineage=args.lineage,
        number=args.number,
    )
    print(f"Successfully scaffolded new style:")
    print(f"  File: {path}")
    print(f"  To test: material-styles render --style {args.name} -o test.png")
    print(f"  To audit: material-styles audit {args.name}")


def cmd_gallery(args):
    """Batch render all styles and generate master contact sheet."""
    from render_styles_gallery import create_contact_sheet
    styles = registry.list_styles()
    print(f"Rendering all {len(styles)} styles...")
    results = []
    for s in styles:
        r = s.render(outdir=args.outdir)
        results.append(r)
    create_contact_sheet(results, out_path=args.contact_sheet)
    print("Gallery and contact sheet updated.")


def main(argv: List[str] = None):
    parser = argparse.ArgumentParser(
        prog="material-styles",
        description="Systematic Physical Design Systems & Generative Print Engine",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = subparsers.add_parser("list", help="List all registered design styles")
    p_list.set_defaults(func=cmd_list)

    # render
    p_render = subparsers.add_parser("render", help="Render a poster in a specific style")
    p_render.add_argument("--style", "-s", required=True, help="Style ID or number (e.g. 1 or 'style_pop_art_serigraphy')")
    p_render.add_argument("--headline", "-H", help="Custom headline / display text")
    p_render.add_argument("--subhead", "-S", help="Custom sub-headline text")
    p_render.add_argument("--footnote", help="Custom footnote / credits text")
    p_render.add_argument("--accession", help="Custom catalog / accession code")
    p_render.add_argument("--seed", type=int, help="Custom seed integer override")
    p_render.add_argument("--output", "-o", help="Output filepath")
    p_render.add_argument("--outdir", default="styles_gallery", help="Output directory")
    p_render.set_defaults(func=cmd_render)

    # audit
    p_audit = subparsers.add_parser("audit", help="Verify empty paper gates & SHA-256 determinism")
    p_audit.add_argument("style", nargs="?", help="Optional specific style ID or number to audit")
    p_audit.add_argument("--outdir", default="styles_gallery", help="Output directory")
    p_audit.set_defaults(func=cmd_audit)

    # new-style
    p_new = subparsers.add_parser("new-style", help="Scaffold a new physical style module")
    p_new.add_argument("name", help="Name of the new design style (e.g. 'Memphis Group 1981')")
    p_new.add_argument("--id", help="Explicit style ID (e.g. 'style_memphis_81')")
    p_new.add_argument("--lineage", help="Pioneering movement, school, or artist")
    p_new.add_argument("--number", type=int, help="Style number")
    p_new.set_defaults(func=cmd_new_style)

    # gallery
    p_gallery = subparsers.add_parser("gallery", help="Render all styles and generate contact sheet")
    p_gallery.add_argument("--outdir", default="styles_gallery", help="Directory for poster files")
    p_gallery.add_argument("--contact-sheet", default="styles_contact_sheet.png", help="Contact sheet output path")
    p_gallery.set_defaults(func=cmd_gallery)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
