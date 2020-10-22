import tests.test_helpers as helpers

def test_step_codec():
    """
    Basic test of the STEP codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = ["python", "cq-cli.py", "--codec", "step", "--infile", test_file]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split('\n')[9].replace('\r', '') == "ISO-10303-21;"