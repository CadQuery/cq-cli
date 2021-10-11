import os, tempfile
import pytest
import tests.test_helpers as helpers
import json

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


def test_parameter_file():
    """
    Tests the CLI's ability to load JSON parameters from a file.
    """
    test_file = helpers.get_test_file_location("cube_params.py")
    params_file = helpers.get_test_file_location("cube_params.json")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_6.step")

    command = ["python", "cq-cli.py", "--codec", "step", "--infile", test_file, '--outfile', temp_file, '--params', params_file]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, 'r') as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_parameter_json_string():
    """
    Tests the CLI's ability to load JSON parameters from the command line.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_7.step")

    command = ["python", "cq-cli.py", "--codec", "step", "--infile", test_file, '--outfile', temp_file, '--params', "{\"width\":10}"]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, 'r') as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_parameter_delimited_string():
    """
    Tests the CLI's ability to load parameters from a colon and semi-colon delimited string.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_8.step")

    command = ["python", "cq-cli.py", "--codec", "step", "--infile", test_file, '--outfile', temp_file, '--params', "width:10;"]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, 'r') as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_parameter_analysis():
    """
    Tests the CLI's ability to extract parameters from a CadQuery script.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    command = ["python", "cq-cli.py", "--getparams", "true", "--infile", test_file]
    out, err, exitcode = helpers.cli_call(command)

    # Grab the JSON output from cq-cli
    jsn = json.loads(out.decode())

    # Check to make sure the first parameter was handled properly
    assert jsn[0]["type"] == "number"
    assert jsn[0]["name"] == "width"
    assert jsn[0]["initial"] == 1

    # Check to make sure the second parameter was handled properly
    assert jsn[1]["type"] == "string"
    assert jsn[1]["name"] == "tag_name"
    assert jsn[1]["initial"] == "cube"

    # Check to make sure the third parameter was handled properly
    assert jsn[2]["type"] == "boolean"
    assert jsn[2]["name"] == "centered"
    assert jsn[2]["initial"] == True


def test_parameter_file_input_output():
    """
    Test the CLI's ability to extract parameters from a script,
    write them to a file, and then read them from the file again.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_9.json")

    # Save the parameters from the script to a file
    command = ["python", "cq-cli.py", "--getparams", "true", "--infile", test_file, '--outfile', temp_file ]
    out, err, exitcode = helpers.cli_call(command)

    # Run the script with baseline parameters
    command2 = ["python", "cq-cli.py", "--codec", "stl", "--infile", test_file, '--params', temp_file]
    out2, err2, exitcode2 = helpers.cli_call(command2)

    # Modify the parameters file
    with open(temp_file, 'r') as file:
        json_str = file.read()
    json_dict = json.loads(json_str)
    json_dict[0]['initial'] = 10
    with open(temp_file, "w") as file:
        file.writelines(json.dumps(json_dict))

    # Run the command with the new parameters
    command3 = ["python", "cq-cli.py", "--codec", "stl", "--infile", test_file, '--params', temp_file]
    out3, err3, exitcode3 = helpers.cli_call(command3)

    # Make sure that the file output changed
    assert out2.decode() != out3.decode()
