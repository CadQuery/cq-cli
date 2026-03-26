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


def test_glb_codec_to_file(tmp_path):
    """
    Tests that the GLB codec writes a valid binary file when --outfile is specified.
    """
    test_file = helpers.get_test_file_location("cube_assy.py")
    out_path = tmp_path / "out.glb"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "glb",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    content = out_path.read_bytes()
    assert content[:4] == b"glTF"


def test_glb_codec_non_assembly_exits_with_error():
    """
    Tests that the GLB codec on a non-assembly shape exits non-zero (raises ValueError).
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "glb",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode != 0
