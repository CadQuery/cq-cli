import os, tempfile
from cadquery import exporters
import cadquery as cq
import cq_cli.cqcodecs.codec_helpers as helpers


def convert(build_result, output_file=None, error_file=None, output_opts=None):
    # Create a temporary file to put the STL output into
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_threejs.json")

    # The exporters will add extra output that we do not want, so suppress it
    with helpers.suppress_stdout_stderr():
        # Put the STEP output into the temp file
        exporters.export(
            build_result.results[0].shape, temp_file, exporters.ExportTypes.TJS
        )

    # Read the STEP output back in
    with open(temp_file, "r") as file:
        tjs_str = file.read()

    return tjs_str
