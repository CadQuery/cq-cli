import pytest
import tests.test_helpers as helpers


def test_glb_codec():
    """
    Basic test of the GLB codec plugin.
    """
    test_file = helpers.get_test_file_location("cube_assy.py")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "glb",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().startswith("b'glTF")
