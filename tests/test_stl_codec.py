import os
import sys
import tests.test_helpers as helpers


def test_stl_codec():
    """
    Basic test of the STL codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split("\n")[0].replace("\r", "") == "solid "


def test_stl_codec_quality():
    """
    Test of the STL codec plugin's ability to adjust the quality of the resulting STL.
    """
    test_file = helpers.get_test_file_location("sphere.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Keep track of the number of lines for each STL as an approximate measure of quality
    high_detail = len(out.decode().split("\n"))

    # Attempt to adjust the quality of the resulting STL
    command2 = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--outputopts",
        "linearDeflection:0.3;angularDeflection:0.3",
    ]
    out2, err2, exitcode2 = helpers.cli_call(command2)

    # Keep track of the number of lines in the STL as an approximate measure of quality
    low_detail = len(out2.decode().split("\n"))

    assert low_detail < high_detail


def test_stl_codec_with_assembly():
    """
    Test of the STL codec plugin with a CadQuery assembly.
    """
    test_file = helpers.get_test_file_location("cube_assy.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split("\n")[0].replace("\r", "") == "solid "


def test_stl_codec_to_file(tmp_path):
    """
    Tests that the STL codec writes a valid file when --outfile is specified.
    """
    test_file = helpers.get_test_file_location("cube.py")
    out_path = tmp_path / "out.stl"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    content = out_path.read_bytes()
    assert content[:5] == b"solid"


def test_stl_codec_quality_file_size(tmp_path):
    """
    Tests that lower deflection values produce a larger file than higher values.
    Uses file size rather than line count, which is robust to binary/text mode.
    """
    test_file = helpers.get_test_file_location("sphere.py")
    out_high = tmp_path / "high_detail.stl"
    out_low = tmp_path / "low_detail.stl"

    helpers.cli_call(
        [
            sys.executable,
            "src/cq_cli/main.py",
            "--codec",
            "stl",
            "--infile",
            test_file,
            "--outfile",
            str(out_high),
        ]
    )
    helpers.cli_call(
        [
            sys.executable,
            "src/cq_cli/main.py",
            "--codec",
            "stl",
            "--infile",
            test_file,
            "--outfile",
            str(out_low),
            "--outputopts",
            "linearDeflection:0.5;angularDeflection:0.5",
        ]
    )

    assert out_high.stat().st_size > out_low.stat().st_size


def test_stl_codec_assembly_to_file(tmp_path):
    """
    Tests that an assembly exported to an STL file produces valid content.
    """
    test_file = helpers.get_test_file_location("cube_assy.py")
    out_path = tmp_path / "assy.stl"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    content = out_path.read_bytes()
    assert content[:5] == b"solid"


def test_stl_codec_binary():
    """
    Tests exporting to binary stl format.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--outputopts",
        "binary:True",
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert out[:5] != b"solid"
