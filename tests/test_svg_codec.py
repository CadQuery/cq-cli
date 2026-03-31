import sys
import tests.test_helpers as helpers


def test_svg_codec():
    """
    Basic test of the SVG codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "svg",
        "--infile",
        test_file,
        "--outputopts",
        "width:100;height:100;marginLeft:12;marginTop:12;showAxes:False;projectionDir:(0.5,0.5,0.5);strokeWidth:0.25;strokeColor:(255,0,0);hiddenColor:(0,0,255);showHidden:True;",
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert (
        out.decode().split("\n")[0].replace("\r", "")
        == '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
    )


def test_svg_codec_with_assembly():
    """
    Test of the SVG codec plugin with a CadQuery assembly.
    """
    test_file = helpers.get_test_file_location("cube_assy.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "svg",
        "--infile",
        test_file,
        "--outputopts",
        "width:100;height:100;marginLeft:12;marginTop:12;showAxes:False;projectionDir:(0.5,0.5,0.5);strokeWidth:0.25;strokeColor:(255,0,0);hiddenColor:(0,0,255);showHidden:True;",
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert (
        out.decode().split("\n")[0].replace("\r", "")
        == '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'
    )


def test_svg_codec_default_opts():
    """
    Tests that the SVG codec works with no --outputopts (no crash on None opts).
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "svg",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    assert '<?xml version="1.0"' in out.decode()


def test_svg_codec_to_file(tmp_path):
    """
    Tests that the SVG codec writes a valid file when --outfile is specified.
    """
    test_file = helpers.get_test_file_location("cube.py")
    out_path = tmp_path / "out.svg"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "svg",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    content = out_path.read_text()
    assert '<?xml version="1.0"' in content


def test_svg_codec_contains_path_elements():
    """
    Tests that the SVG output contains at least one <path> element,
    confirming actual geometry was rendered (not just an empty SVG wrapper).
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "svg",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    assert "<path" in out.decode()
