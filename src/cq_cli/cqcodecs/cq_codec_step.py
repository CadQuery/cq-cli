import os, tempfile
from cadquery import exporters
import cadquery as cq
import cq_cli.cqcodecs.codec_helpers as helpers


def convert(build_result, output_file=None, error_file=None, output_opts=None):
    # Create a temporary file to put the STL output into
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_step.step")

    # The exporters will add extra output that we do not want, so suppress it
    with helpers.suppress_stdout_stderr():
        # There should be a shape in the build results
        shape = build_result.results[0].shape

        # assembly or a single object?
        if type(shape).__name__ == "Assembly":
            # use assembly save method
            shape.save(temp_file)
        else:
            # Put the STEP output into the temp file
            exporters.export(shape, temp_file, exporters.ExportTypes.STEP)

    # Read the STEP output back in
    with open(temp_file, "r") as file:
        step_str = file.read()

    return step_str
