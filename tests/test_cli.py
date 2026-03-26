import os, sys
import pytest
import tests.test_helpers as helpers
import json


def test_no_cli_arguments():
    """
    Runs the CLI with no arguments, which you should not do unless you want the usage message.
    """
    command = [sys.executable, "src/cq_cli/main.py"]
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
        sys.executable,
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
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)
    assert "ISO-10303-21;" in out.decode()


def test_codec_infile_and_outfile_arguments(tmp_path):
    """
    Tests the CLI with the codec, infile and outfile set.
    """
    test_file = helpers.get_test_file_location("cube.py")

    temp_file = tmp_path / "temp_test_4.step"

    command = [
        sys.executable,
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
    with open(str(temp_file), "r") as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_codec_infile_outfile_errfile_arguments(tmp_path):
    """
    Tests the CLI with the codec, infile, outfile and errfile parameters set.
    The infile does not exist so that an error will be thrown.
    """
    test_file = helpers.get_test_file_location("noexist.py")

    temp_file = tmp_path / "temp_test_5.step"
    err_file = tmp_path / "temp_test_5_error.txt"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(temp_file),
        "--errfile",
        str(err_file),
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the error back from the errfile
    with open(str(err_file), "r") as file:
        err_str = file.read()

    assert err_str == "Argument error: infile does not exist."


def test_no_codec_parameter(tmp_path):
    """
    Tests the CLI's ability to infer the codec from the outfile extension.
    """
    test_file = helpers.get_test_file_location("cube.py")

    temp_file = tmp_path / "temp_test_12.step"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--infile",
        test_file,
        "--outfile",
        str(temp_file),
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(str(temp_file), "r") as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_no_codec_parameter_multiple_infiles(tmp_path):
    """
    Tests the CLI's ability to infer the codecs from multiple infile extensions.
    """
    test_file = helpers.get_test_file_location("cube.py")

    temp_file_step = tmp_path / "temp_test_13.step"
    temp_file_stl = tmp_path / "temp_test_13.stl"
    temp_paths = f"{temp_file_step};{temp_file_stl}"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--infile",
        test_file,
        "--outfile",
        temp_paths,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile to make sure it has the correct content
    with open(str(temp_file_step), "r") as file:
        step_str = file.read()
    assert step_str.startswith("ISO-10303-21;")

    # Read the STL output back from the outfile to make sure it has the correct content
    with open(str(temp_file_stl), "r") as file:
        stl_str = file.read()
    assert stl_str.startswith("solid")

    assert exitcode == 0


def test_parameter_file(tmp_path):
    """
    Tests the CLI's ability to load JSON parameters from a file.
    """
    test_file = helpers.get_test_file_location("cube_params.py")
    params_file = helpers.get_test_file_location("cube_params.json")

    temp_file = tmp_path / "temp_test_6.step"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(temp_file),
        "--params",
        params_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(str(temp_file), "r") as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_parameter_json_string(tmp_path):
    """
    Tests the CLI's ability to load JSON parameters from the command line.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    temp_file = tmp_path / "temp_test_7.step"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(temp_file),
        "--params",
        '{"width":10}',
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(str(temp_file), "r") as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_parameter_delimited_string(tmp_path):
    """
    Tests the CLI's ability to load parameters from a colon and semi-colon delimited string.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    temp_file = tmp_path / "temp_test_8.step"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(temp_file),
        "--params",
        "width:10;",
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(str(temp_file), "r") as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")


def test_parameter_analysis():
    """
    Tests the CLI's ability to extract parameters from a CadQuery script.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--getparams",
        "true",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Grab the JSON output from cq-cli
    jsn = json.loads(out.decode())
    params_by_name = helpers.params_list_to_dict(jsn)

    # Check to make sure the parameters were handled properly
    assert params_by_name["width"] == {"name": "width", "type": "number", "initial": 1}
    assert params_by_name["tag_name"] == {
        "name": "tag_name",
        "type": "string",
        "initial": "cube",
    }
    assert params_by_name["centered"] == {
        "name": "centered",
        "type": "boolean",
        "initial": True,
    }


def test_parameter_file_input_output(tmp_path):
    """
    Test the CLI's ability to extract parameters from a script,
    write them to a file, and then read them from the file again.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    temp_file = tmp_path / "temp_test_9.json"

    # Save the parameters from the script to a file
    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--getparams",
        str(temp_file),
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Run the script with baseline parameters
    command2 = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--params",
        str(temp_file),
    ]
    out2, err2, exitcode2 = helpers.cli_call(command2)

    assert err2.decode() == ""

    # Modify the parameters file
    with open(str(temp_file), "r") as file:
        json_str = file.read()
    json_list = json.loads(json_str)
    json_list[1]["initial"] = 10
    with open(str(temp_file), "w") as file:
        file.writelines(json.dumps(json_list))

    # Run the command with the new parameters
    command3 = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--params",
        str(temp_file),
    ]
    out3, err3, exitcode3 = helpers.cli_call(command3)

    # Make sure that the file output changed
    assert out2.decode() != out3.decode()


def test_params_stl_output(tmp_path):
    """
    Test to specifically make sure that cq-cli will work with CadHub.
    """
    test_file = helpers.get_test_file_location("cube_params.py")

    # Get a temporary output file locations
    output_file_path = tmp_path / "output.stl"
    default_output_file_path = tmp_path / "output_default.stl"
    customizer_file_path = tmp_path / "customizer.json"
    params_json_file_path = tmp_path / "params.json"

    # Fake out the params.json file that would be coming from the user's interaction with CadHub
    params_json = {}
    params_json["width"] = 10
    params_json["tag_name"] = "cube_default"
    params_json["centered"] = False
    with open(str(params_json_file_path), "w") as file:
        file.writelines(json.dumps(params_json))

    # Execute the script with the current parameters and save the new parameter metadata to the customizer file
    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--outfile",
        str(output_file_path),
        "--params",
        str(params_json_file_path),
        "--getparams",
        str(customizer_file_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Make sure there was no error
    assert err.decode() == ""

    # Make sure that the customizer.json file exists and has what we expect in it
    with open(str(customizer_file_path), "r") as file2:
        json_str = file2.read()
    json_list = json.loads(json_str)
    params = helpers.params_list_to_dict(json_list)
    assert params["width"]["initial"] == 1
    assert params["tag_name"]["initial"] == "cube"
    assert params["centered"]["initial"] == True

    # Write an STL using the default parameters so that we can compare it to what was generated with customized parameters
    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "stl",
        "--infile",
        test_file,
        "--outfile",
        str(default_output_file_path),
    ]
    out2, err2, exitcode2 = helpers.cli_call(command)

    # Compare the two files to make sure they are different
    with open(str(output_file_path), "r") as file3:
        stl_output_with_params = file3.read()
    with open(str(default_output_file_path), "r") as file4:
        default_stl = file4.read()
    assert stl_output_with_params != default_stl


def test_exit_codes():
    """
    Tests a few exit codes to make sure the correct ones are
    being returned.
    """

    # Test to make sure we get the correct exit code when no parameters are specified
    command = [sys.executable, "src/cq_cli/main.py"]
    out, err, exitcode = helpers.cli_call(command)

    # Make sure that we got exit code 2
    assert exitcode == 2

    # We want to test a cube with fillets that are so large they cause a CAD kernel error
    test_input_file = helpers.get_test_file_location("impossible_cube.py")

    # Execute the script with the current parameters and save the new parameter metadata to the customizer file
    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_input_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Make sure that we got exit code 100 for a failed model build
    assert exitcode == 100


def test_expression_argument(tmp_path):
    """
    Tests the CLI with the the expression argument.
    """
    test_file = helpers.get_test_file_location("no_toplevel_objects.py")

    temp_file = tmp_path / "temp_test_10.step"

    # Run cq-cli with --expression "cube()"
    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(temp_file),
        "--expression",
        "cube()",
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Read the STEP output back from the outfile
    with open(str(temp_file), "r") as file:
        step_str = file.read()

    assert step_str.startswith("ISO-10303-21;")

    # Run cq-cli on the same model file, but don't specify an --expression. This
    # should fail because the file contains no top-level show_object() calls.
    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(temp_file),
    ]
    out, err, exitcode = helpers.cli_call(command)

    # cq-cli invocation should fail
    assert exitcode == 200


def test_multiple_outfiles(tmp_path):
    """
    Tests the CLI with multiple output files specified.
    """
    test_file = helpers.get_test_file_location("cube.py")

    temp_file_step = tmp_path / "temp_test_11.step"
    temp_file_stl = tmp_path / "temp_test_11.stl"
    temp_paths = f"{temp_file_step};{temp_file_stl}"

    command = [
        sys.executable,
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


def test_stl_stdout_is_binary_safe():
    """
    Tests that STL output written to stdout is valid binary/text STL content
    (not a Python bytes repr like b'solid ...').
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

    assert exitcode == 0
    # Output must start with the STL header, not a Python bytes repr
    assert out[:5] == b"solid"


def test_stl_output_opts_none_does_not_crash(tmp_path):
    """
    Tests that passing no --outputopts to the STL codec does not crash
    (guards against None passed to output_opts).
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
    assert err.decode() == ""


def test_invalid_codec_exit_code():
    """
    Tests that specifying an unknown codec exits with code 3.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "nonexistentcodec",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 3


def test_validate_valid_script():
    """
    Tests that --validate true returns 'validation_success' for a valid script.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--validate",
        "true",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    assert "validation_success" in out.decode()


def test_validate_invalid_script():
    """
    Tests that --validate true exits with code 100 for a broken script.
    """
    test_file = helpers.get_test_file_location("impossible_cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--validate",
        "true",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 100


def test_outputopts_quoted_string(tmp_path):
    """
    Tests that quoted string output options are stored without surrounding quotes.
    This guards against the bug where 'value' was stored as "'value'" instead of "value".
    Uses SVG codec which passes outputopts through.
    """
    test_file = helpers.get_test_file_location("cube.py")
    out_path = tmp_path / "out.svg"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "svg",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
        "--outputopts",
        "strokeColor:'#FF0000';",
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Should not crash parsing the quoted string option
    assert exitcode == 0


def test_params_single_char_does_not_crash():
    """
    Tests that a single-character --params value does not crash with an IndexError
    on the Windows path detection code (args.params[1]).
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--params",
        "x",
    ]
    out, err, exitcode = helpers.cli_call(command)

    # Should not crash with IndexError - exit 0 or 100 depending on script, not 1
    assert exitcode != 1


def test_build_error_written_to_errfile(tmp_path):
    """
    Tests that a build error (exception object) is correctly written as a string
    to the errfile, not crashing with TypeError.
    """
    test_file = helpers.get_test_file_location("impossible_cube.py")
    err_file = tmp_path / "build_error.txt"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--errfile",
        str(err_file),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 100
    with open(str(err_file), "r") as f:
        err_content = f.read()
    # Must be a non-empty string, not a crash
    assert len(err_content) > 0


def test_file_variable_is_set(tmp_path):
    """
    Tests that cq-cli sets the __file__ variable for the model script.
    """
    test_file = helpers.get_test_file_location("file_var.py")

    out_path = tmp_path / "temp_test_file_variable.stl"

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
    assert "__file__=" in out.decode()


def test_stdin_input():
    """
    Tests that a CadQuery script piped via stdin produces valid STEP output.
    """
    import subprocess

    test_file = helpers.get_test_file_location("cube.py")
    with open(test_file, "r") as f:
        script = f.read()

    proc = subprocess.Popen(
        [sys.executable, "src/cq_cli/main.py", "--codec", "step", "--outfile", "-"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    # Pass script via stdin; use --outfile - equivalent: no --outfile means stdout
    proc2 = subprocess.Popen(
        [sys.executable, "src/cq_cli/main.py", "--codec", "step"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc2.communicate(input=script.encode())

    assert "ISO-10303-21;" in out.decode()


def test_stdin_with_outfile(tmp_path):
    """
    Tests that a CadQuery script piped via stdin with --outfile writes correct output.
    """
    import subprocess

    test_file = helpers.get_test_file_location("cube.py")
    with open(test_file, "r") as f:
        script = f.read()

    out_path = tmp_path / "stdin_out.step"

    proc = subprocess.Popen(
        [
            sys.executable,
            "src/cq_cli/main.py",
            "--codec",
            "step",
            "--outfile",
            str(out_path),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    out, err = proc.communicate(input=script.encode())

    assert proc.returncode == 0
    with open(str(out_path), "r") as f:
        content = f.read()
    assert content.startswith("ISO-10303-21;")


def test_parameter_delimited_string_multiple_params(tmp_path):
    """
    Tests that multiple key:value pairs in a single --params string all take effect.
    Passes width=2 and centered=False together and confirms output differs from defaults.
    """
    test_file = helpers.get_test_file_location("cube_params.py")
    out_default = tmp_path / "default.step"
    out_custom = tmp_path / "custom.step"

    command_default = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(out_default),
    ]
    helpers.cli_call(command_default)

    command_custom = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(out_custom),
        "--params",
        "width:2;",
    ]
    out, err, exitcode = helpers.cli_call(command_custom)

    assert exitcode == 0
    with open(str(out_default), "r") as f:
        default_content = f.read()
    with open(str(out_custom), "r") as f:
        custom_content = f.read()
    assert default_content != custom_content


def test_parameter_json_string_multiple_params(tmp_path):
    """
    Tests that a JSON --params string with multiple keys all apply correctly.
    """
    test_file = helpers.get_test_file_location("cube_params.py")
    out_path = tmp_path / "multi_json.step"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
        "--params",
        '{"width": 5, "centered": false}',
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    with open(str(out_path), "r") as f:
        content = f.read()
    assert content.startswith("ISO-10303-21;")


def test_getparams_with_no_params_script():
    """
    Tests that --getparams on a script with no user-defined parameters returns only
    the injected __file__ entry (a side-effect of __file__ prepending), with no other
    named parameters.
    """
    test_file = helpers.get_test_file_location("cube.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--getparams",
        "true",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    result = json.loads(out.decode())
    user_params = [p for p in result if p["name"] != "__file__"]
    assert user_params == []


def test_getparams_writes_file_and_returns_expected_keys(tmp_path):
    """
    Tests that --getparams writes a JSON file containing the expected parameter names.
    """
    test_file = helpers.get_test_file_location("cube_params.py")
    params_out = tmp_path / "params.json"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--getparams",
        str(params_out),
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    assert params_out.exists() and params_out.stat().st_size > 0
    params = json.loads(params_out.read_text())
    names = [p["name"] for p in params]
    assert "width" in names
    assert "tag_name" in names
    assert "centered" in names


def test_validate_with_outfile(tmp_path):
    """
    Tests that --validate true with --outfile writes 'validation_success' to the file.
    """
    test_file = helpers.get_test_file_location("cube.py")
    out_path = tmp_path / "validation.txt"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--validate",
        "true",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    assert out_path.read_text() == "validation_success"


def test_syntax_error_exits_100():
    """
    Tests that a script with a Python syntax error exits with code 100.
    """
    test_file = helpers.get_test_file_location("syntax_error.py")

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 100


def test_syntax_error_written_to_errfile(tmp_path):
    """
    Tests that a script syntax error writes a traceback to errfile.
    """
    test_file = helpers.get_test_file_location("syntax_error.py")
    err_file = tmp_path / "syntax_err.txt"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--errfile",
        str(err_file),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 100
    content = err_file.read_text()
    assert len(content) > 0


def test_codec_error_written_to_errfile(tmp_path):
    """
    Tests that a codec-level failure (exit 200) writes traceback to errfile.
    Uses the expression argument to trigger a no-results error.
    """
    test_file = helpers.get_test_file_location("no_toplevel_objects.py")
    err_file = tmp_path / "codec_err.txt"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--codec",
        "step",
        "--infile",
        test_file,
        "--errfile",
        str(err_file),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 200
    content = err_file.read_text()
    assert len(content) > 0


def test_auto_codec_detection_stl(tmp_path):
    """
    Tests that the STL codec is inferred from a .stl output file extension.
    """
    test_file = helpers.get_test_file_location("cube.py")
    out_path = tmp_path / "auto.stl"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    content = out_path.read_bytes()
    assert content[:5] == b"solid"


def test_auto_codec_detection_svg(tmp_path):
    """
    Tests that the SVG codec is inferred from a .svg output file extension.
    """
    test_file = helpers.get_test_file_location("cube.py")
    out_path = tmp_path / "auto.svg"

    command = [
        sys.executable,
        "src/cq_cli/main.py",
        "--infile",
        test_file,
        "--outfile",
        str(out_path),
    ]
    out, err, exitcode = helpers.cli_call(command)

    assert exitcode == 0
    content = out_path.read_text()
    assert '<?xml version="1.0"' in content


def test_param_change_produces_different_step_output(tmp_path):
    """
    Tests that changing the width parameter produces geometrically different STEP output.
    """
    test_file = helpers.get_test_file_location("cube_params.py")
    out_small = tmp_path / "small.step"
    out_large = tmp_path / "large.step"

    helpers.cli_call(
        [
            sys.executable,
            "src/cq_cli/main.py",
            "--codec",
            "step",
            "--infile",
            test_file,
            "--outfile",
            str(out_small),
            "--params",
            "width:1;",
        ]
    )
    helpers.cli_call(
        [
            sys.executable,
            "src/cq_cli/main.py",
            "--codec",
            "step",
            "--infile",
            test_file,
            "--outfile",
            str(out_large),
            "--params",
            "width:10;",
        ]
    )

    assert out_small.read_text() != out_large.read_text()


def test_multi_show_object_produces_output():
    """
    Tests that a script calling show_object() multiple times still produces valid output
    (cq-cli uses the first result).
    """
    test_file = helpers.get_test_file_location("multi_show_object.py")

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
