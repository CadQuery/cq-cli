import os, tempfile
from cadquery import exporters
import cadquery as cq
import cq_cli.cqcodecs.codec_helpers as helpers


def convert(build_result, output_file=None, error_file=None, output_opts=None):
    # Create a temporary file to put the STL output into
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_stl.stl")

    linearDeflection = 0.1
    angularDeflection = 0.1

    # If the user has provided the deflection settings, use them
    if "linearDeflection" in output_opts:
        linearDeflection = output_opts["linearDeflection"]
    if "angularDeflection" in output_opts:
        angularDeflection = output_opts["angularDeflection"]

    # The exporters will add extra output that we do not want, so suppress it
    with helpers.suppress_stdout_stderr():
        # There should be a shape in the build results
        result = build_result.results[0].shape

        # If the build result is an assembly, we have to make it a compound before trying to export it as SVG
        if type(result).__name__ == "Assembly":
            result = result.toCompound()
        else:
            result = result.val()

        # Put the STL output into the temp file
        result.exportStl(temp_file, linearDeflection, angularDeflection, True)

    # Read the STL output back in
    with open(temp_file, "r") as file:
        stl_str = file.read()

    return stl_str
