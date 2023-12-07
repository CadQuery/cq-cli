import os, tempfile
from cadquery import exporters
import cq_cli.cqcodecs.codec_helpers as helpers


def convert(build_result, output_file=None, error_file=None, output_opts=None):
    # Create a temporary file to put the STL output into
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_svg.svg")

    # The exporters will add extra output that we do not want, so suppress it
    with helpers.suppress_stdout_stderr():
        # There should be a shape in the build results
        result = build_result.results[0].shape

        # If the build result is an assembly, we have to make it a compound before trying to export it as SVG
        if type(result).__name__ == "Assembly":
            result = result.toCompound()

        # Put the STEP output into the temp file
        exporters.export(
            result, temp_file, exporters.ExportTypes.SVG, opt=output_opts,
        )

    # Read the STEP output back in
    with open(temp_file, "r") as file:
        step_str = file.read()

    return step_str
