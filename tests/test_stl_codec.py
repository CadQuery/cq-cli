import os
import tests.test_helpers as helpers


def test_stl_codec():
    """
    Basic test of the STL codec plugin.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        "python",
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
        "python",
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
        "python",
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
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split("\n")[0].replace("\r", "") == "solid "
