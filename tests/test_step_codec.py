import sys
import tests.test_helpers as helpers


def test_step_codec():
    """
    Basic test of the STEP codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert "ISO-10303-21;" in out.decode()


def test_step_codec_with_assembly():
    """
    Tests that the STEP codec correctly handles a CadQuery Assembly,
    exercising the assembly.save() code path instead of exporters.export().
    """
    test_file = helpers.get_test_file_location("cube_assy.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    assert "ISO-10303-21;" in out.decode()


def test_step_codec_to_file(tmp_path):
    """
    Tests that the STEP codec writes a valid file when --outfile is specified.
    """
    test_file = helpers.get_test_file_location("cube.py")
    out_path = tmp_path / "out.step"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    content = out_path.read_text()
    assert content.startswith("ISO-10303-21;")


def test_step_codec_contains_geometry():
    """
    Tests that the STEP output contains geometry data, not just the header.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    content = out.decode()
    assert "CLOSED_SHELL" in content
