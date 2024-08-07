import os, tempfile
import pytest
import tests.test_helpers as helpers
import json


def test_no_cli_arguments():
    """
    Runs the CLI with no arguments, which you should not do unless you want the usage message.
    """
    command = ["python", "src/cq_cli/main.py"]
    out, err, exitcode = helpers.cli_call(command)

    assert (
        out.decode()
        .split("\n")[0]
        .startswith("Please specify at least the validate option")
    )


def test_codec_and_infile_arguments_file_nonexistent():
    """
    Tests the CLI with only the codec and infile set, but with a non-existing file.
    """
    test_file = helpers.get_test_file_location("noexist.py")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert err.decode().startswith("infile does not exist.")


def test_codec_and_infile_arguments():
    """
    Test the CLI with only the codec and infile set, with a file that exists.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)
    assert "ISO-10303-21;" in out.decode()


def test_codec_infile_and_outfile_arguments():
    """
    Tests the CLI with the codec, infile and outfile set.
    """
    test_file = helpers.get_test_file_location("cube.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_4.step")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        temp_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, "r") as file:
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

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        temp_file,
        "--errfile",
        err_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the error back from the errfile
    with open(err_file, "r") as file:
        err_str = file.read()

    assert err_str == "Argument error: infile does not exist."


def test_no_codec_parameter():
    """
    Tests the CLI's ability to infer the codec from the outfile extension.
    """
    test_file = helpers.get_test_file_location("cube.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_12.step")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--infile",
        test_file,
        "--outfile",
        temp_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, "r") as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_no_codec_parameter_multiple_infiles():
    """
    Tests the CLI's ability to infer the codecs from multiple infile extensions.
    """
    test_file = helpers.get_test_file_location("cube.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file_step = os.path.join(temp_dir, "temp_test_13.step")
    temp_file_stl = os.path.join(temp_dir, "temp_test_13.stl")
    temp_paths = temp_file_step + ";" + temp_file_stl

    command = [
        "python",
        "src/cq_cli/main.py",
        "--infile",
        test_file,
        "--outfile",
        temp_paths,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile to make sure it has the correct content
    with open(temp_file_step, "r") as file:
        step_str = file.read()
    assert step_str.startswith("ISO-10303-21;")

    # Read the STL output back from the outfile to make sure it has the correct content
    with open(temp_file_stl, "r") as file:
        stl_str = file.read()
    assert stl_str.startswith("solid")

    assert exitcode == 0


def test_parameter_file():
    """
    Tests the CLI's ability to load JSON parameters from a file.
    """
    test_file = helpers.get_test_file_location("cube_params.py")
    params_file = helpers.get_test_file_location("cube_params.json")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_6.step")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        temp_file,
        "--params",
        params_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, "r") as file:
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

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        temp_file,
        "--params",
        '{"width":10}',
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, "r") as file:
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

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        temp_file,
        "--params",
        "width:10;",
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, "r") as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_parameter_analysis():
    """
    Tests the CLI's ability to extract parameters from a CadQuery script.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    command = [
        "python",
        "src/cq_cli/main.py",
        "--getparams",
        "true",
        "--infile",
        test_file,
    ]
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
    command = [
        "python",
        "src/cq_cli/main.py",
        "--getparams",
        temp_file,
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Run the script with baseline parameters
    command2 = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--params",
        temp_file,
    ]
    out2, err2, exitcode2 = helpers.cli_call(command2)

    assert err2.decode() == ""

    # Modify the parameters file
    with open(temp_file, "r") as file:
        json_str = file.read()
    json_dict = json.loads(json_str)
    json_dict[0]["initial"] = 10
    with open(temp_file, "w") as file:
        file.writelines(json.dumps(json_dict))

    # Run the command with the new parameters
    command3 = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--params",
        temp_file,
    ]
    out3, err3, exitcode3 = helpers.cli_call(command3)

    # Make sure that the file output changed
    assert out2.decode() != out3.decode()


def test_params_stl_output():
    """
    Test to specifically make sure that cq-cli will work with CadHub.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    # Get a temporary output file locations
    temp_dir = tempfile.gettempdir()
    output_file_path = os.path.join(temp_dir, "output.stl")
    default_output_file_path = os.path.join(temp_dir, "output_default.stl")
    customizer_file_path = os.path.join(temp_dir, "customizer.json")
    params_json_file_path = os.path.join(temp_dir, "params.json")

    # Fake out the params.json file that would be coming from the user's interaction with CadHub
    params_json = {}
    params_json["width"] = 10
    params_json["tag_name"] = "cube_default"
    params_json["centered"] = False
    with open(params_json_file_path, "w") as file:
        file.writelines(json.dumps(params_json))

    # Execute the script with the current parameters and save the new parameter metadata to the customizer file
    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--outfile",
        output_file_path,
        "--params",
        params_json_file_path,
        "--getparams",
        customizer_file_path,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Make sure there was no error
    assert err.decode() == ""

    # Make sure that the customizer.json file exists and has what we expect in it
    with open(customizer_file_path, "r") as file2:
        json_str = file2.read()
    json_dict = json.loads(json_str)
    assert json_dict[0]["initial"] == 1
    assert json_dict[1]["initial"] == "cube"
    assert json_dict[2]["initial"] == True

    # Write an STL using the default parameters so that we can compare it to what was generated with customized parameters
    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--outfile",
        default_output_file_path,
    ]
    out2, err2, exitcode2 = helpers.cli_call(command)

    # Compare the two files to make sure they are different
    with open(output_file_path, "r") as file3:
        stl_output_with_params = file3.read()
    with open(default_output_file_path, "r") as file4:
        default_stl = file4.read()
    assert stl_output_with_params != default_stl


def test_exit_codes():
    """
    Tests a few exit codes to make sure the correct ones are
    being returned.
    """

    # Test to make sure we get the correct exit code when no parameters are specified
    command = ["python", "src/cq_cli/main.py"]
    out, err, exitcode = helpers.cli_call(command)

    # Make sure that we got exit code 2
    assert exitcode == 2

    # We want to test a cube with fillets that are so large they cause a CAD kernel error
    test_input_file = helpers.get_test_file_location("impossible_cube.py")

    # Execute the script with the current parameters and save the new parameter metadata to the customizer file
    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_input_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Make sure that we got exit code 100 for a failed model build
    assert exitcode == 100


def test_expression_argument():
    """
    Tests the CLI with the the expression argument.
    """
    test_file = helpers.get_test_file_location("no_toplevel_objects.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_test_10.step")

    # Run cq-cli with --expression "cube()"
    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        temp_file,
        "--expression",
        "cube()",
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(temp_file, "r") as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")

    # Run cq-cli on the same model file, but don't specify an --expression. This
    # should fail because the file contains no top-level show_object() calls.
    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        temp_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # cq-cli invocation should fail
    assert exitcode == 200


def test_multiple_outfiles():
    """
    Tests the CLI with multiple output files specified.
    """
    test_file = helpers.get_test_file_location("cube.py")

    # Get a temporary output file location
    temp_dir = tempfile.gettempdir()
    temp_file_step = os.path.join(temp_dir, "temp_test_11.step")
    temp_file_stl = os.path.join(temp_dir, "temp_test_11.stl")
    temp_paths = temp_file_step + ";" + temp_file_stl

    command = [
        "python",
        "src/cq_cli/main.py",
        "--codec",
        "step;stl",
        "--infile",
        test_file,
        "--outfile",
        temp_paths,
    ]
    out, err, exitcode = helpers.cli_call(command)
    assert exitcode == 0
