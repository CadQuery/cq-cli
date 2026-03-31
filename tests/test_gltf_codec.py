import sys
import pytest
import tests.test_helpers as helpers


def test_gltf_codec():
    """
    Basic test of the GLTF codec plugin.
    """
    test_file = helpers.get_test_file_location("cube_assy.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "gltf",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split("\n")[0].replace("\r", "").startswith('{"accessors":')


def test_gltf_codec_is_valid_json():
    """
    Tests that the GLTF output is valid, parseable JSON.
    """
    test_file = helpers.get_test_file_location("cube_assy.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "gltf",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    import json

    data = json.loads(out.decode())
    assert "accessors" in data


def test_gltf_codec_to_file(tmp_path):
    """
    Tests that the GLTF codec writes a valid JSON file when --outfile is specified.
    """
    test_file = helpers.get_test_file_location("cube_assy.py")
    out_path = tmp_path / "out.gltf"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "gltf",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    import json

    data = json.loads(out_path.read_text())
    assert "accessors" in data


def test_gltf_codec_non_assembly_exits_with_error():
    """
    Tests that the GLTF codec on a non-assembly shape exits non-zero (raises ValueError).
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "gltf",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode != 0
