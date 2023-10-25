import pytest
import tests.test_helpers as helpers


def test_gltf_codec():
    """
    Basic test of the GLTF codec plugin.
    """
    test_file = helpers.get_test_file_location("cube_assy.py")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "gltf",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split("\n")[0].replace("\r", "").startswith('{"accessors":')
