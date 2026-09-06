"""Audit runner verifying empty paper gates and dual-pass byte-for-byte determinism."""
import hashlib
from typing import Dict, List, Optional, Union

from material_styles.registry import registry
from material_styles.styles.base import BaseStyle


def compute_sha256(filepath: str) -> str:
    """Compute SHA-256 hash of a file."""
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(65536):
            h.update(chunk)
    return h.hexdigest()


def audit_style(style_or_id: Union[BaseStyle, str, int], outdir: str = "styles_gallery") -> dict:
    """Audit an individual style for gate pass and deterministic dual-pass SHA-256."""
    if isinstance(style_or_id, (str, int)):
        style = registry.get(style_or_id)
        if style is None:
            raise ValueError(f"Unknown style: {style_or_id}")
    else:
        style = style_or_id

    # Pass 1
    res1 = style.render(outdir=outdir)
    hash1 = compute_sha256(res1["path"])

    # Pass 2
    res2 = style.render(outdir=outdir)
    hash2 = compute_sha256(res2["path"])

    deterministic = (hash1 == hash2)
    gate_ok = res1["gate_ok"]
    zempty = res1.get("zempty") or res1.get("empty")

    return {
        "number": style.metadata.number,
        "style_id": style.metadata.id,
        "name": style.metadata.name,
        "slug": res1["slug"],
        "path": res1["path"],
        "zempty": zempty,
        "gate_range": res1["gate_range"],
        "gate_ok": gate_ok,
        "deterministic": deterministic,
        "sha256": hash1,
    }


def audit_all(outdir: str = "styles_gallery") -> List[dict]:
    """Audit all registered styles and return results."""
    styles = registry.list_styles()
    results = []
    for s in styles:
        res = audit_style(s, outdir=outdir)
        results.append(res)
    return results
