"""Automated dual-pass SHA-256 determinism tests across all 15 physical styles."""
import pytest
from material_styles.audit import audit_style
from material_styles.registry import registry


@pytest.mark.parametrize("style_num", list(range(1, 16)))
def test_style_determinism(style_num, tmp_path):
    """Verify that two consecutive renders produce byte-for-byte identical SHA-256 hashes."""
    style = registry.get(style_num)
    assert style is not None, f"Style #{style_num} not found"

    outdir = str(tmp_path / f"style_{style_num}")
    res = audit_style(style, outdir=outdir)

    assert res["deterministic"] is True, (
        f"Style #{style_num} ({res['style_id']}) is NOT deterministic! "
        f"Dual-pass SHA-256 hashes did not match."
    )
