import os
import subprocess


def get_test_file_location(file_name):
    """
    Combines the testdata directory path with a filename for a test.
    """
    test_data_dir = os.path.join(os.path.dirname(__file__), "testdata")

    return os.path.join(test_data_dir, file_name)


def cli_call(command):
    """
    Makes the operating system process calls to test the CLI properly.
    """
    proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = proc.communicate()
    return out, err, proc.returncode


def params_list_to_dict(param_list):
    """
    Converts a list of params into a dictionary of those params keyed by name.
    """
    d = {}
    for entry in param_list:
        d[entry["name"]] = entry
    return d
