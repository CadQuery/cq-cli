import os, tempfile
import cq_cli.cqcodecs.codec_helpers as helpers


def convert(build_result, output_file=None, error_file=None, output_opts=None):
    # Create a temporary file to put the STL output into
    temp_dir = tempfile.gettempdir()
    temp_file = os.path.join(temp_dir, "temp_glb.glb")

    # The exporters will add extra output that we do not want, so suppress it
    with helpers.suppress_stdout_stderr():
        # Put the GLB output into the temp file
        # Check to see if we are dealing with an assembly or a single object
        if type(build_result.first_result.shape).__name__ == "Assembly":
            build_result.first_result.shape.save(temp_file, binary=True)
        else:
            raise ValueError(
                "GLB export is only available for CadQuery assemblies at this time"
            )

    # Read the GLB output back in
    with open(temp_file, "rb") as file:
        glb_data = file.read()

    return glb_data
