# cq-cli

[![tests](/actions/workflows/tests.yml/badge.svg)](/actions)

## Contents

* [Introduction](#introduction)
* [Getting Help](#getting-help)
* [Installation](#installation)
* [Usage](#usage)
* [Examples](#examples)
* [Contributing](#contributing)

## Introduction

***Please Note:*** cq-cli is in beta.

cq-cli is a Command Line Interface for executing CadQuery scripts and converting their output to another format. It uses a plugin system where "codecs" can be placed in the `cqcodecs` directory and will be automatically loaded and used if a user selects that codec from the command line.

Input and output files can be specified via arguments, but cq-cli also supports stdin, stdout, and stderr streams so that it can be used in a pipeline.

**Requires Python 3.11 or later.** Linux, macOS, and Windows are supported, though some features may behave differently on Windows.

## Getting Help

In addition to opening an issue on this repo, there is a [CadQuery Discord channel](https://discord.gg/qz3uAdF) and a [Google Group](https://groups.google.com/g/cadquery) where you can ask for help getting started with cq-cli.

## Installation

### uv (preferred) ⭐️

[uv](https://docs.astral.sh/uv/) is the recommended way to install and run cq-cli. It handles Python version management and virtual environments automatically.

```
uv venv --python 3.11
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync
```

Once complete, run cq-cli with:
```
cq-cli --help
```

### pip

It is strongly recommended to use a Python virtual environment when installing via pip.

cq-cli is not available on PyPI, so it must be installed from source using pip and git. git must be installed for this to work.

```
pip install git+https://github.com/CadQuery/cq-cli.git
```

Once the installation is complete, the CLI can be invoked as:
```
cq-cli --help
```
or:
```
python -m cq_cli.main --help
```

## Usage

```
cq-cli [-h] [--codec CODEC] [--infile INFILE] [--outfile OUTFILE]
       [--errfile ERRFILE] [--params PARAMS] [--outputopts OPTS]
       [--getparams GETPARAMS] [--validate VALIDATE] [--expression EXPRESSION]
```

Command line utility for converting CadQuery script output to various output formats.

| Argument | Description |
|---|---|
| `-h`, `--help` | Show help message and exit |
| `--codec CODEC` | The codec to use for conversion (e.g. `step`, `stl`, `svg`, `dxf`, `glb`, `gltf`, `threejs`). Can be omitted if `--outfile` has a recognised extension. Multiple codecs can be specified separated by `;` — must match the number of `--outfile` entries. |
| `--infile INFILE` | The input CadQuery script (`.py`) or FreeCAD file (`.fcstd`). Reads from stdin if omitted. |
| `--outfile OUTFILE` | File to write the converted output to. Prints to stdout if omitted. Multiple output files can be specified separated by `;`. |
| `--errfile ERRFILE` | File to write errors to. Prints to stderr if omitted. |
| `--params PARAMS` | Parameters to pass to the script. Accepts: a JSON file path, a JSON string (`{"width":10}`), or a colon/semicolon delimited string (`width:10;height:5;`). |
| `--outputopts OPTS` | Codec-specific options as a colon/semicolon delimited string. e.g. `width:100;height:200;` |
| `--getparams GETPARAMS` | Analyse the script and write parameter metadata as JSON. Pass a file path to write to a file, or `true` to print to stdout. |
| `--validate VALIDATE` | Set to `true` to validate the script without producing output. |
| `--expression EXPRESSION` | A Python expression to evaluate and render (e.g. `my_shape(x=5)`). Useful for rendering a specific part from a file that contains multiple functions. |

## Examples

1. Find out what codecs are available.
```
cq-cli --codec help
```
2. Validate a CadQuery script.
```
cq-cli --validate true --infile /input/path/script.py
```
3. Convert a CadQuery script to STEP format and output to stdout.
```
cq-cli --codec step --infile /input/path/script.py
```
4. Convert a CadQuery script to STEP format and write to a file.
```
cq-cli --codec step --infile /input/path/script.py --outfile /output/path/newfile.step
```
5. Convert a CadQuery script and write any errors to a separate file.
```
cq-cli --codec step --infile /input/path/script.py --errfile /error/path/error.txt
```
6. Convert a CadQuery script using stdin and stdout streams. This example counts the lines in the resulting STEP output.
```
cat /input/path/script.py | cq-cli --codec step | wc -l
```
7. Let cq-cli infer the codec from the output file extension.
```
cq-cli --infile /input/path/script.py --outfile /output/path/newfile.stl
```
8. Convert to multiple output formats in a single invocation.
```
cq-cli --infile /input/path/script.py --outfile /output/path/model.step;/output/path/model.stl
```
9. Convert a CadQuery script to SVG, passing output options to influence the resulting image.
```
cq-cli --codec svg --infile /input/path/script.py --outfile /output/path/newfile.svg --outputopts "width:100;height:100;marginLeft:12;marginTop:12;showAxes:False;projectionDir:(0.5,0.5,0.5);strokeWidth:0.25;strokeColor:(255,0,0);hiddenColor:(0,0,255);showHidden:True;"
```
10. Convert a CadQuery script to STL, adjusting mesh quality. Explanation of linear vs angular deflection can be found [here](https://dev.opencascade.org/doc/occt-7.1.0/overview/html/occt_user_guides__modeling_algos.html#occt_modalg_11_2).
```
cq-cli --codec stl --infile /input/path/script.py --outfile /output/path/script.stl --outputopts "linearDeflection:0.3;angularDeflection:0.3"
```
11. Extract parameter information from a script. Omit the file path to print JSON to stdout.
```
cq-cli --getparams /output/path/params.json --infile /input/path/script.py
```
12. Pass JSON parameter information from a file to the script.
```
cq-cli --codec stl --infile /input/path/script.py --outfile /output/path/output.stl --params /parameter/path/parameters.json
```
13. Pass JSON parameter data as a string on the command line.
```
cq-cli --codec stl --infile /input/path/script.py --params "{\"width\":10}"
```
14. Pass parameters as a colon/semicolon delimited string.
```
cq-cli --codec stl --infile /input/path/script.py --outfile test.stl --params "width:2;centered:True"
```
15. Render a specific function from a file using `--expression`.
```
cq-cli --codec step --infile /input/path/script.py --outfile /output/path/part.step --expression "my_part(x=5)"
```

## Contributing

### Development Setup

The recommended way to set up a development environment is with [uv](https://docs.astral.sh/uv/).

```
git clone https://github.com/CadQuery/cq-cli.git
cd cq-cli
uv venv --python 3.11
source .venv/bin/activate  # Windows: .venv\Scripts\activate
uv sync --extra dev
```

Alternatively, using pip:
```
git clone https://github.com/CadQuery/cq-cli.git
cd cq-cli
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e .[dev]
```

Run the test suite:
```
pytest -v --ignore=tests/test_freecad.py
```

### Adding a Codec

The codec plugin system is based on naming conventions so that cq-cli knows what codec options to accept from the user. When adding a codec, place it in the `cqcodecs` directory and follow the naming convention `cq_codec_[your codec name].py`. The `your codec name` part of the filename will automatically be used as the codec name specified by the user.

A good starting point is [cqcodecs/cq_codec_step.py](src/cq_cli/cqcodecs/cq_codec_step.py), which shows a simple codec implementation that relies on CadQuery to do the heavy lifting. At minimum, your codec needs a `convert` function that accepts a [CQGI BuildResult object](https://cadquery.readthedocs.io/en/latest/cqgi.html#cadquery.cqgi.BuildResult) and returns a string or bytes representing the converted model. If the codec writes the output file directly, return `None` and cq-cli will assume the output was written to disk.

### Adding a Codec Test

A test is required when adding a codec to cq-cli. Add a file named `test_[your codec name]_codec.py` in the `tests` directory. [tests/test_step_codec.py](tests/test_step_codec.py) is a good template.

### Exit Codes

| Code | Meaning |
|---|---|
| **0** | Operation completed successfully. |
| **1** | The CadQuery script could not be read from `--infile`. |
| **2** | Usage error — incorrect or insufficient arguments. |
| **3** | No valid codec was provided or could be inferred. |
| **100** | Error while running the CadQuery script (build error, possibly from OCCT). |
| **200** | Error while running the conversion codec. |

