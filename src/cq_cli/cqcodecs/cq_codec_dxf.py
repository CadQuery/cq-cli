import os, tempfile
from cadquery import exporters
import cq_cli.cqcodecs.codec_helpers as helpers


def convert(build_result, output_file=None, error_file=None, output_opts=None):
    # Create a temporary file to put the STL output into
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_dxf.dxf")

    # The exporters will add extra output that we do not want, so suppress it
    with helpers.suppress_stdout_stderr():
        # Put the DXF output into the temp file
        exporters.export(
            build_result.results[0].shape,
            temp_file,
            exporters.ExportTypes.DXF,
            opt=output_opts,
        )

    # Read the DXF output back in
    with open(temp_file, "r") as file:
        dxf_str = file.read()

    return dxf_str
