import tests.test_helpers as helpers


def test_static_freecad_file():
    """
    Basic test of the FreeCAD (FCStd) codec plugin.
    """
    test_file = helpers.get_test_file_location("shelf.FCStd")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert "ISO-10303-21;" in out.decode()


def test_parametric_freecad_file():
    """
    Basic test of the FreeCAD (FCStd) codec plugin.
    """
    test_file = helpers.get_test_file_location("shelf.FCStd")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--params",
        "internal_rail_spacing:152.4;",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert "ISO-10303-21;" in out.decode()
