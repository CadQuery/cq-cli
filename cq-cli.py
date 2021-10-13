#!/usr/bin/env python3
import os
import sys
import argparse
import cadquery as cq
from cadquery import cqgi
import fileinput
import traceback
import json
from cqcodecs import loader

def build_and_parse(script_str, params, errfile):
    """
    Uses CQGI to parse and build a script, substituting in parameters if any were supplied.
    """
        # We need to do a broad try/catch to let the user know if something higher-level fails
    try:
        # Do the CQGI handling of the script here and, if successful, pass the build result to the codec
        cqModel = cqgi.parse(script_str)
        build_result = cqModel.build(params)

        # Handle the case of the build not being successful, otherwise pass the codec the build result
        if not build_result.success:
            # Re-throw the exception so that it will be caught and formatted correctly
            raise(build_result.exception)
        else:
            return build_result
    except Exception:
        out_tb = traceback.format_exc()

        # If there was an error file specified write to that, otherwise send it to stderr
        if errfile != None:
            with open(errfile, 'w') as file:
                file.write(str(out_tb))
        else:
            print(str(out_tb), file=sys.stderr)

    # Return None here to prevent a failed build from slipping through
    return None

def get_script_from_infile(infile, outfile, errfile):
    """
    Gets the CadQuery script from the infile location.
    """
    script_str = None

    # See whether to ingest a file or accept text from stdin
    if infile == None:
        # Do not output to stdout if that is where our conversion output is going
        if outfile != None:
            print("No input file specified, assuming stdin.")
    else:
        # Make sure the infile exists
        if not os.path.isfile(infile):
            if errfile == None:
                print("infile does not exist.", file=sys.stderr)
            else:
                with open(errfile, 'w') as file:
                    file.write("Argument error: infile does not exist.")

            return

    # If there was an infile specified, read the contents of it, otherwise read from stdin
    if infile == None:
        # Grab the string from stdin
        script_str = sys.stdin.read()
    else:
        with open(infile, 'r') as file:
            script_str = file.read()

    return script_str


def set_pythonpath_for_infile(infile):
    """
    Sets the PYTHONPATH environment variable to include the location of the infile.
    """

    # If the infile is none we are reading from stdin and there is nothing to set
    if infile == None:
        return

    # Make sure that any user-created modules are found
    sys.path.append(os.path.abspath(os.path.join(infile, os.pardir)))


def get_params_from_file(param_json_path, errfile):
    """
    Loads JSON parameters in a file into a Python dictionary.
    """
    param_dict = None

    # Make sure that the file exists
    if os.path.isfile(param_json_path):
        # Read the contents of the file
        with open(param_json_path, 'r') as file:
            params_json = file.read()
            param_dict_array = json.loads(params_json)

            # Load the array of parameters into the single JSON structure CQGI is expecting
            param_dict = {}

            # Account for parameters either being in an array or in a dict of their own
            if type(param_dict_array) == list:
                for p in param_dict_array:
                    param_dict[p["name"]] = p["initial"]
            elif type(param_dict_array) == dict:
                for key in param_dict_array:
                    param_dict[key] = param_dict_array[key]
    else:
        if errfile == None:
            print("Parameter file does not exist, default parameters will be used. ", file=sys.stderr)
        else:
            with open(errfile, 'w') as file:
                file.write("Argument error: Parameter file does not exist, default parameters will be used.")

    return param_dict


def main():
    infile = None
    outfile = None
    errfile = None
    codec = None
    codec_module = None
    params = {}
    output_opts = {}

    # Find the codecs that have been added.
    loaded_codecs = loader.load_codecs()

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Command line utility for converting CadQuery script output to various other output formats.')
    parser.add_argument('--codec', dest='codec', help='The codec to use when converting the CadQuery output. Must match the name of a codec file in the cqcodecs directory.')
    parser.add_argument('--getparams', dest='getparams', help='Analyzes the script and returns a JSON string with the parameter information.')
    parser.add_argument('--infile', dest='infile', help='The input CadQuery script to convert.')
    parser.add_argument('--outfile', dest='outfile', help='File to write the converted CadQuery output to. Prints to stdout if not specified.')
    parser.add_argument('--errfile', dest='errfile', help='File to write any errors to. Prints to stderr if not specified.')
    parser.add_argument('--params', dest='params', help='A colon and semicolon delimited string (no spaces) of key/value pairs representing variables and their values in the CadQuery script.  i.e. var1:10.0;var2:4.0;')
    parser.add_argument('--outputopts', dest='opts', help='A colon and semicolon delimited string (no spaces) of key/value pairs representing options to pass to the selected codec.  i.e. width:100;height:200;')
    parser.add_argument('--validate', dest='validate', help='Setting to true forces the CLI to only parse and validate the script and not produce converted output.')

    args = parser.parse_args()

    # Make sure that the user has at least specified the validate or codec arguments
    if args.validate == None and args.getparams == None and args.codec == None:
        parser.print_help(sys.stderr)
        return

    #
    # Outfile handing
    #
    # See whether to output to a file or stdout
    if args.outfile != None:
        outfile = args.outfile

    #
    # Errfile handling
    #
    # See whether to output errors to a file or stderr
    if args.errfile != None:
        errfile = args.errfile

    #
    # Validation handling
    #
    # If the user wants to validate, do that and exit
    if args.validate == 'true':
        script_str = get_script_from_infile(args.infile, outfile, errfile)

        if script_str == None: return

        # Set the PYTHONPATH variable to the current directory to allow module loading
        set_pythonpath_for_infile(args.infile)

        build_result = build_and_parse(script_str, params, errfile)

        # Double-check that the build was a success
        if build_result != None and build_result.success:
            # Let the user know that the validation was a success
            if outfile != None:
                with open(outfile, 'w') as file:
                    file.write('validation_success')
            else:
                print('validation_success')

        return

    #
    # Parameter analysis
    #
    # Analyzes the parameters that are available in the script.
    #
    if args.getparams != None:
        # Array of dictionaries that holds the parameter data
        params = []

        # Load the script string
        script_str = get_script_from_infile(args.infile, outfile, errfile)
        if script_str == None: return

        # Set the PYTHONPATH variable to the current directory to allow module loading
        set_pythonpath_for_infile(args.infile)

        # A representation of the CQ script with all the metadata attached
        cq_model = None
        try:
            cq_model = cqgi.parse(script_str)
        except Exception as err:
            print("Script error: " + str(err), file=sys.stderr)

        # Allows us to present parameters to users later that they can alter
        parameters = cq_model.metadata.parameters

        # Step through all the parameters and add them to the array of dictionaries
        for param in parameters.values():
            new_dict = {}

            # Return the data type of the parameter, trying to match conventions set by other platforms
            if param.varType.__name__ == "NumberParameterType":
                new_dict["type"] = "number"
            elif param.varType.__name__ == "StringParameterType":
                new_dict["type"] = "string"
            elif param.varType.__name__ == "BooleanParameterType":
                new_dict["type"] = "boolean"

            # Save the name of the parameter
            new_dict["name"] = param.name

            # If there is a description, save it
            if param.desc:
                new_dict["caption"] = param.desc

            # If there is an initial value, save it
            if param.default_value:
                new_dict["initial"] = param.default_value

            # If there are values set for valid values via describe_parameter(), add those
            if param.valid_values:
                new_dict["min"] = param.valid_values[0]
                new_dict["max"] = param.valid_values[-1]
                new_dict["step"] = new_dict["max"] - new_dict["min"]

                # Ensure that the step is larger than 0
                if new_dict["step"] <= 0:
                    new_dict["step"] = 1

            params.append(new_dict)

        # Write the converted output to the appropriate place based on the command line arguments
        if args.getparams == 'true':
            print(json.dumps(params))
        else:
            with open(args.getparams, 'w') as file:
                file.write(json.dumps(params))

        # Check to see if the user only cared about getting the params
        if args.codec == None:
            return

    #
    # Codec handling
    #
    # Save the requested codec for later
    codec = args.codec

    # If the user has not supplied a codec, they need to be validating the script
    if (codec == 'help' or codec == None) and (args.validate == None or args.validate == 'false'):
        print("Please specify a codec. You have the following to choose from:")
        for key in loaded_codecs:
            print(key.replace('cq_codec_', ''))
        return

    for key in loaded_codecs:
        # Check to make sure that the requested codec exists
        if codec in key:
            codec_module = loaded_codecs[key]

    #
    # Infile handling
    #
    infile = args.infile

    # Grab the script input from a file path or stdin
    script_str = get_script_from_infile(infile, outfile, errfile)

    if script_str == None: return

    # Set the PYTHONPATH variable to the current directory to allow module loading
    set_pythonpath_for_infile(args.infile)

    #
    # Parameter handling
    #
    # Check whether any parameters were passed
    if args.params != None:
        # We have been passed a directory
        if args.params.startswith('/') or args.params.startswith('.') or args.params.startswith('..') or args.params.startswith('~') or args.params[1] == ':':
            # Load the parameters dictionary from the file
            file_params = get_params_from_file(args.params, errfile)

            # Make sure we got parameters back before we try to pass it to CQGI
            if file_params != None:
                params = file_params
        elif args.params.startswith("{"):
            # Convert the JSON string passed from the user to a Python dictionary
            params = json.loads(args.params)
        else:
            # Convert the string of parameters into a params dictionary
            groups = args.params.split(';')
            for group in groups:
                param_parts = group.split(':')
                # Protect against a trailing semi-colon
                if len(param_parts) == 2:
                    params[param_parts[0]] = param_parts[1]

    #
    # Output options handling
    #
    # Check whether any output options were passed
    if args.opts != None:
        # Convert the string of options into a output_opts dictionary
        groups = args.opts.split(';')
        for group in groups:
            opt_parts = group.split(':')
            # Protect against a trailing semi-colon
            if len(opt_parts) == 2:
                op1 = opt_parts[1]

                # Handle the option data types properly
                if op1 == "True" or op1 == "False":
                    op = opt_parts[1] == "True"
                elif op1[:1] == "(":
                    op = tuple(map(float, opt_parts[1].replace("(", "").replace(")", "").split(',')))
                elif "." in op1:
                    op = float(opt_parts[1])
                else:
                    op = int(opt_parts[1])

                output_opts[opt_parts[0]] = op

    #
    # Parse and build the script.
    #
    build_result = None
    try:
        build_result = build_and_parse(script_str, params, errfile)

        # If None was returned, it means the build failed and the exception has already been reported
        if build_result == None:
            return
    except Exception as err:
        # Write the file to the appropriate place based on what the user specified
        if errfile == None:
            print("build_and_parse error: " + str(err), file=sys.stderr)
        else:
            with open(errfile, 'w') as file:
                file.write(err)
        return

    #
    # Final build
    #
    # Build, parse and let the selected codec convert the CQ output
    try:
        # Use the codec plugin to do the conversion
        converted = codec_module.convert(build_result, outfile, errfile, output_opts)

        # If converted is None, assume that the output was written to file directly by the codec
        if converted != None:
            # Write the converted output to the appropriate place based on the command line arguments
            if outfile == None:
                print(converted)
            else:
                with open(outfile, 'w') as file:
                    file.write(converted)

    except Exception:
        out_tb = traceback.format_exc()

        # Send the error to wherever the user requested
        if errfile == None:
            print("Conversion codec error: " + str(out_tb), file=sys.stderr)
        else:
            with open(errfile, 'w') as file:
                file.write(str(out_tb))

if __name__ == "__main__":
    main()
