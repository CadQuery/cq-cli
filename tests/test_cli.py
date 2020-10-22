import os, tempfile
import pytest
import tests.test_helpers as helpers

def test_no_cli_arguments():
    """
    Runs the CLI with no arguments, which you should not do unless you want the usage message.
    """
    command = ["python", "cq-cli.py"]
    out, err, exitcode = helpers.cli_call(command)

    assert err.decode().split('\n')[0].startswith("usage")

def test_codec_and_infile_arguments_file_nonexistent():
    """
    Tests the CLI with only the codec and infile set, but with a non-existing file.
    """
    test_file = helpers.get_test_file_location("noexist.py")

    command = ["python", "cq-cli.py", "--codec", "step", "--infile", test_file]
    out, err, exitcode = helpers.cli_call(command)

    assert err.decode().startswith("infile does not exist.")

def test_codec_and_infile_arguments():
    """
    Test the CLI with only the codec and infile set, with a file that exists.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = ["python", "cq-cli.py", "--codec", "step", "--infile", test_file]
    out, err, exitcode = helpers.cli_call(command)

    assert out.decode().split('\n')[9].replace('\r', '') == "ISO-10303-21;"

def test_codec_infile_and_outfile_arguments():
    """
    Tests the CLI with the codec, infile and outfile set.
    """
    test_file = helpers.get_test_file_location("cube.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_4.step")

    command = ["python", "cq-cli.py", "--codec", "step", "--infile", test_file, '--outfile', temp_file]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, 'r') as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")

def test_codec_infile_outfile_errfile_arguments():
    """
    Tests the CLI with the codec, infile, outfile and errfile parameters set.
    The infile does not exist so that an error will be thrown.
    """
    test_file = helpers.get_test_file_location("noexist.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_5.step")
    err_file = os.path.join(temp_dir, "temp_test_5_error.txt")

    command = ["python", "cq-cli.py", "--codec", "step", "--infile", test_file, '--outfile', temp_file, '--errfile', err_file]
    out, err, exitcode = helpers.cli_call(command)

    # Read the error back from the errfile
    with open(err_file, 'r') as file:
        err_str = file.read()

    assert err_str == "Argument error: infile does not exist."