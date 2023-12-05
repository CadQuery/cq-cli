import tests.test_helpers as helpers


def test_svg_codec():
    """
    Basic test of the SVG codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        "python",
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
        "python",
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
