import tests.test_helpers as helpers

def test_stl_codec():
    """
    Basic test of the STL codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = ["python", "cq-cli.py", "--codec", "stl", "--infile", test_file]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split('\n')[0].replace('\r', '') == "solid "