"""Automated tests verifying material-styles CLI subcommands."""
import os
from material_styles.cli import main
from material_styles.registry import registry
from material_styles.scaffold import scaffold_style


def test_cli_list(capsys):
    """Test 'material-styles list' outputs all 15 styles."""
    main(["list"])
    captured = capsys.readouterr()
    assert "Total physical design styles: 15" in captured.out
    assert "style_zurich_modernism" in captured.out
    assert "style_polish_surrealism" in captured.out


def test_cli_render_custom_text(tmp_path):
    """Test 'material-styles render' with custom headline and subhead."""
    out_file = str(tmp_path / "custom_poster.png")
    main([
        "render",
        "--style", "1",
        "--headline", "TEST HEADLINE",
        "--subhead", "TEST SUBHEAD",
        "-o", out_file,
    ])
    assert os.path.exists(out_file)
    assert os.path.getsize(out_file) > 10000


def test_cli_audit_single(capsys):
    """Test 'material-styles audit 1' passes."""
    main(["audit", "1"])
    captured = capsys.readouterr()
    assert "PASS ✓" in captured.out
    assert "MATCH ✓" in captured.out


def test_cli_scaffold(tmp_path):
    """Test 'material-styles new-style' scaffolds a valid file."""
    custom_dir = str(tmp_path / "custom_styles")
    scaffold_path = scaffold_style(
        name="Constructivist Bauhaus 1923",
        target_dir=custom_dir,
    )
    assert os.path.exists(scaffold_path)
    with open(scaffold_path) as f:
        code = f.read()
    assert "ConstructivistBauhaus1923Style" in code
    assert "BaseStyle" in code
