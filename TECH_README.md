# CadQuery CLI (cq-cli) - Project Overview

`cq-cli` is a Command Line Interface for executing CadQuery scripts and converting their output to various formats (STEP, STL, DXF, SVG, GLB, GLTF, ThreeJS). It is designed to be used in automation pipelines and supports stdin/stdout streams.

## Architecture

The project is built around the **CadQuery Gateway Interface (CQGI)**.
- **Entry Point:** `src/cq_cli/main.py` handles argument parsing, script loading, and coordination between CQGI and codecs.
- **Plugin System:** Codecs are dynamically loaded from `src/cq_cli/cqcodecs/` by `loader.py`. Any file matching `cq_codec_*.py` is treated as a codec.
- **FreeCAD Support:** Integrates `cadquery_freecad_import_plugin` to handle `.fcstd` files.

## Tech Stack
- **Language:** Python 3.9+
- **Core Library:** [CadQuery](https://github.com/CadQuery/cadquery)
- **Environment Management:** `uv` (preferred)
- **Build Tool:** PyInstaller (for standalone binaries)
- **Testing:** `pytest`

## Key Commands

### Development
- **Install Dependencies:** `uv sync`
- **Run CLI (Development):** `python -m cq_cli.main --help`
- **Run Tests:** `pytest`
- **Linting:** `black` (v19.10b0 specified in `pyproject.toml`)

### Usage Examples
- **Convert to STEP:** `cq-cli --codec step --infile model.py --outfile model.step`
- **Auto-detect Codec:** `cq-cli --infile model.py --outfile model.stl`
- **Extract Parameters:** `cq-cli --getparams true --infile model.py`
- **Pass Parameters:** `cq-cli --params "width:10;height:20" --infile model.py`
- **Evaluate Expression:** `cq-cli --expression "my_part(10)" --infile models.py`

### Building
- **PyInstaller (One-file):** `pyinstaller cq-cli_pyinstaller.spec onefile`
- **PyInstaller (Directory):** `pyinstaller cq-cli_pyinstaller.spec dir`

## Development Conventions

### Adding a New Codec
1. Create `src/cq_cli/cqcodecs/cq_codec_[name].py`.
2. Implement a `convert` function:
   ```python
   def convert(build_result, outfile, errfile, output_opts):
       # build_result is a cqgi.BuildResult
       # Return string/bytes for writing to outfile (or stdout)
       # Return None if the codec writes directly to outfile
   ```
3. Add the new codec to `hiddenimports` in `cq-cli_pyinstaller.spec` for standalone builds.
4. Add a test in `tests/test_[name]_codec.py`.

### Exit Codes
- **0:** Success
- **1:** Input file read error
- **2:** Usage/Argument error
- **3:** Missing/Invalid codec
- **100:** CadQuery build error (script execution failure)
- **200:** Codec conversion error

## Testing
Tests are located in the `tests/` directory and use `pytest`. Many tests rely on `tests/test_helpers.py` for CLI invocation and `tests/testdata/` for sample scripts.
