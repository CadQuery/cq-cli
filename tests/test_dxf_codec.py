import tests.test_helpers as helpers


def test_dxf_codec():
    """
    Basic test of the DXF codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "dxf",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split("\n")[1].replace("\r", "") == "SECTION"
