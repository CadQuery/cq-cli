import tests.test_helpers as helpers


def test_threejs_codec():
    """
    Basic test of the TJS (Three.js) codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "threejs",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)
    print("Output New: " + str(out.decode()))
    print("Error: " + str(err))
    assert (
        out.decode().split("\n")[5].replace("\r", "") == '        "vertices"      : 24,'
    )
    assert (
        out.decode().split("\n")[6].replace("\r", "") == '        "faces"         : 12,'
    )
