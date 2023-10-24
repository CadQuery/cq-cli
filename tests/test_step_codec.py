import tests.test_helpers as helpers


def test_step_codec():
    """
    Basic test of the STEP codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        "python",
        "src/cq_cli/cq_cli.py",
        "--codec",
        "step",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split("\n")[0].replace("\r", "") == "ISO-10303-21;"
