"""Automated gate verification tests across all 15 physical styles."""
import pytest
from material_styles.registry import registry


@pytest.mark.parametrize("style_num", list(range(1, 16)))
def test_style_gate_compliance(style_num, tmp_path):
    """Verify that every style renders and passes its designated empty paper gate."""
    style = registry.get(style_num)
    assert style is not None, f"Style #{style_num} not found in registry"

    res = style.render(outdir=str(tmp_path))
    assert res["gate_ok"] is True, (
        f"Style #{style_num} ({res['style_id']}) failed empty paper gate! "
        f"Empty: {res['zempty']:.1f}%, Gate: {res['gate_range'][0]}-{res['gate_range'][1]}%"
    )
