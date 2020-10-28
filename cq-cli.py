#!/usr/bin/env python3
import os
import sys
import argparse
import cadquery as cq
from cadquery import cqgi
import fileinput
import traceback
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

def main():
    infile = None
    outfile = None
    errfile = None
    codec = None
    codec_module = None
    params = {}

    # Find the codecs that have been added.
    loaded_codecs = loader.load_codecs()

    # Parse the command line arguments
    parser = argparse.ArgumentParser(description='Command line utility for converting CadQuery script output to various other output formats.')
    parser.add_argument('--codec', dest='codec', help='The codec to use when converting the CadQuery output. Must match the name of a codec file in the cqcodecs directory.')
    parser.add_argument('--infile', dest='infile', help='The input CadQuery script to convert.')
    parser.add_argument('--outfile', dest='outfile', help='File to write the converted CadQuery output to. Prints to stdout if not specified.')
    parser.add_argument('--errfile', dest='errfile', help='File to write any errors to. Prints to stderr if not specified.')
    parser.add_argument('--params', dest='params', help='A colon and semicolon delimited string (no spaces) of key/value pairs representing variables and their values in the CadQuery script.  i.e. var1:10.0;var2:4.0;')
    parser.add_argument('--validate', dest='validate', help='Setting to true forces the CLI to only parse and validate the script and not produce converted output.')

    args = parser.parse_args()

    # Make sure that the user has at least specified the validate or codec arguments
    if args.validate == None and args.codec == None:
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

    #
    # Parameter handling
    #
    # Check whether any parameters were passed
    if args.params != None:
        # Convert the string of parameters into a params dictionary
        groups = args.params.split(';')
        for group in groups:
            param_parts = group.split(':')
            params[param_parts[0]] = param_parts[1]

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
        converted = codec_module.convert(build_result, outfile, errfile)

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