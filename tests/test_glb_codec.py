import sys
import tests.test_helpers as helpers


def test_glb_codec():
    """
    Basic test of the GLB codec plugin.
    GLB files have a 4-byte magic header: 0x676C5446 ('glTF' in ASCII).
    """
    test_file = helpers.get_test_file_location("cube_assy.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "glb",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    assert out[:4] == b"glTF"
