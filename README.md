# cq-cli

[![tests](https://github.com/CadQuery/cq-cli/actions/workflows/tests.yml/badge.svg)](https://github.com/CadQuery/cq-cli/actions)

## Contents

* [Introduction](https://github.com/CadQuery/cq-cli#introduction)
* [Getting Help](https://github.com/CadQuery/cq-cli#getting_help)
* [Installation](https://github.com/CadQuery/cq-cli#installation)
* [Usage](https://github.com/CadQuery/cq-cli#usage)
* [Examples](https://github.com/CadQuery/cq-cli#examples)
* [Drawbacks](https://github.com/CadQuery/cq-cli#drawbacks)
* [Contributing](https://github.com/CadQuery/cq-cli#contributing)

## Introduction

***Please Note*** cq-cli is in beta.

cq-cli is a Command Line Interface for executing CadQuery scripts and converting their output to another format. It uses a plugin system where "codecs" can be placed in the cqcodecs directory and will be automatically loaded and used if a user selects that codec from the command line.

It is possible to specify input and output files using arguments, but cq-cli also allows the use to the stdin, stdout and stderr streams so that it can be used in a pipeline.

Linux, MacOS and Windows are supported, but some features may be used differently or may not work the same in Windows.

## Getting Help

In addition to opening an issue on this repo, there is a [CadQuery Discord channel](https://discord.gg/qz3uAdF) and a [Google Group](https://groups.google.com/g/cadquery) that you can join to ask for help getting started with cq-cli.

## Installation (pip)

***Note:*** It probably goes without saying, but it is best to use a Python virtual environment when installing a Python package like cq-cli.

These instructions cover installing cq-cli using pip. If you want a stand-alone installation that does not require any of the Python infrastructure, read the Stand-Alone section below.

cq-cli is not available on PyPI, so it must be installed using pip and git. git must be installed for this process to work.

```
pip install git+https://github.com/CadQuery/cq-cli.git
```
Once the installation is complete, there will be two different ways to run the cq-cli command line interface.

```
cq-cli --help
```
or
```
python -m cq_cli.main --help
```

## Installation (Stand-Alone)

**Please note:** This method is not recommended now that cq-cli can be installed via pip, but it is still an option if it is not possible to use a Python virtual environment.

Download a binary distribution that is appropriate for your operating system from the [latest PyInstaller workflow run with a green checkmark](https://github.com/CadQuery/cq-cli/actions/workflows/pyinstaller.yml), extract the zip file, and make sure to put the cq-cli binary in the PATH. Then the CLI can be invoked as `cq-cli` (`cq-cli.exe` on Windows).

If installing on Windows, the [latest redistributable for Visual Studio](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) will need to be installed.


## Drawbacks of Stand-Alone Installation

* The file (and directory) size for cq-cli is very large. cq-cli uses pyinstaller to package the binaries for each platform, and must embed all needed dependencies. The OCP and OCCT library dependencies add a minimum of ~270 MB of data on top of the included Python distribution. It is possible that the pyinstaller spec file could be optimized. If you are interested in helping with this, please let us know by opening an issue.
* Startup times for the single binary are relatively slow. If startup and execution time is important to you, consider using the pyinstaller_dir.spec spec file with pyinstaller: `pyinstaller pyinstaller_dir.spec`.

## Usage

usage: cq-cli.py [-h] [--codec CODEC] [--infile INFILE] [--outfile OUTFILE] [--errfile ERRFILE] [--params PARAMS] [--outputopts OPTS] [--validate VALIDATE]

Command line utility for converting CadQuery script output to various other output formats.

optional arguments:
* `-h`, `--help` Show this help message and exit
* `--codec` CODEC The codec to use when converting the CadQuery output. Must match the name of a codec file in the cqcodecs directory.
* `--getparams` GETPARAMS 
* `--infile` INFILE The input CadQuery script to convert.
* `--outfile` OUTFILE File to write the converted CadQuery output to. Prints to stdout if not specified.
* `--errfile` ERRFILE File to write any errors to. Prints to stderr if not specified.
* `--params` PARAMS A colon and semicolon delimited string (no spaces) of key/value pairs representing variables and their values in the CadQuery script. i.e. var1:10.0;var2:4.0;
* `--outputopts` OPTS A colon and semicolon delimited string (no spaces) of key/value pairs representing options to pass to the selected codec.  i.e. width:100;height:200;
* `--validate` VALIDATE Setting to true forces the CLI to only parse and validate the script and not produce converted output.

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
cq-cli --codec step --infile /input/path/script.py -errfile /error/path/error.txt
```
6. Convert a CadQuery script using the stdin and stdout streams. This example counts the lines in the resulting STEP output as a trivial example.
```
cat /input/path/script.py | cq-cli.py --codec step | wc -l
```
7. Convert a CadQuery script to SVG, passing in output options to influence the resulting image.
```
cq-cli --codec svg --infile /input/path/script.py --outfile /output/path/newfile.svg --outputopts "width:100;height:100;marginLeft:12;marginTop:12;showAxes:False;projectionDir:(0.5,0.5,0.5);strokeWidth:0.25;strokeColor:(255,0,0);hiddenColor:(0,0,255);showHidden:True;"
```
8. Convert a CadQuery script to STL, passing in output options to change the quality of the resulting STL. Explanation of linear vs angular deflection can be found [here](https://dev.opencascade.org/doc/occt-7.1.0/overview/html/occt_user_guides__modeling_algos.html#occt_modalg_11_2).
```
cq-cli --codec stl --infile /input/path/script.py --outfile /output/path/script.stl --outputopts "linearDeflection:0.3;angularDeflection:0.3"
```
9. Extract parameter information from the input script. The outfile argument can also be left off to output the parameter JSON to stdout.
```
cq-cli --getparams /output/path/params.json --infile /input/path/script.py
```
10. Pass JSON parameter information from a file to be used in the script.
```
cq-cli --codec stl --infile /input/path/script.py --outfile /output/path/output.stl --params /parameter/path/parameters.json
```
11. Pass JSON parameter data as a string on the command line.
```
cq-cli --codec stl --infile /input/path/script.py --params "{\"width\":10}"
```
12. String parameters can be defined using single quotes (`'`) or escaped double quotes (`\"`).
```
cq-cli --codec stl --outfile test.stl --infile /input/path/script.py --outputopts "width:2;tag_name:'test';centered:True"
```
```
cq-cli --codec stl --outfile test.stl --infile /input/path/script.py --outputopts "width:2;tag_name:\"test\";centered:True"
```

## Contributing

If you want to help improve and expand cq-cli, the following steps should get you up and running with a development setup. There is a  [CadQuery Discord channel](https://discord.gg/qz3uAdF) and a [Google Group](https://groups.google.com/g/cadquery) that you can join to ask for help getting started.

1. Create a Python virtual environment and activate it. Attept to avoid the bleeding-edge version of Python as there may be problems.
2. Clone this repository: `git clone https://github.com/CadQuery/cq-cli.git`
3. cd into the repository directory: `cd cq-cli`
4. Do a local editable installation via pip: `pip install -e .`

### Adding a Codec

The codec plugin system is based on naming conventions so that cq-cli knows what codec options to accept from the user. When adding a codec, make sure to place it in the `cqcodecs` directory and follow the naming convention `cq_codec_[your codec name].py`. The `your codec name` part of the filename will automatically be used as the codec name that the user specifies.

A good example to start with when creating your own codec would be `cqcodecs/cq_codec_step.py` as it shows a simple implementation of the codec that relies on CadQuery to do all the heavy lifting. At the very least, your codec needs to have a `convert` function that takes in a [CQGI BuildResult object](https://cadquery.readthedocs.io/en/latest/cqgi.html#cadquery.cqgi.BuildResult) and returns a string representing the converted model(s). As an alternative, cq-cli will pass the output file name, which makes it possible to write the output to the outfile path directly from the codec. If `None` is returned from the `convert` function, cq-cli will assume that the output was written directly to the output file by the codec.

For pyinstaller to know about the new dynamically loaded codec, it must be added to the `hiddenimports` array in both cq-cli_onfile_pyinstaller.spec and cq-cli_dir_pyinstaller.spec files. Leave the `.py` off of the name when adding to the array, for instance `codec.cq_codec_step` is the string used for the STEP codec. When only running a codec locally and not contributing it, this step is not required.

### Adding a Codec Test

A test is required when adding a codec to cq-cli, but is easy to add. Add a file named `test_[your codec name]_codec.py` in the tests directory, and add the test to it. `test_step_codec.py` would be a good template to base any new tests off of.

### Exit Codes

Applications can return a non-zero exit code to let the user know what went wrong. Below is a listing of the exit codes for cq-cli and what they mean.

* **0:** Operation was successful with no errors detected.
* **1:** A CadQuery script could not be read from the given `infile`.
* **2:** There was a usage error with the parameters that were passed to cq-cli (too few parameters, not the correct ones, etc).
* **3:** A codec for converting the results of the CadQuery script was not provided.
* **100:** There was an unknown error while running the CadQuery script and obtaining a result (build error, possibly from OCCT).
* **200:** There was an unknown error while running a codec to convert the results of the CadQuery script.

### pyinstaller

If building cq-cli to run as a stand-alone app is required, there are two modes to build it in: `onefile` and `dir` (directory). onefile mode creates a single file for the app, which is easy to distribute but takes longer to start up run on each execution. dir mode creates a directory with numerous dependency files in it, including the cq-cli binary file, and starts up faster than the single file. However, the directory distribution can take up more than twice the disk space and can be messier to distribute. A PyInstaller spec file has been provided for both modes, and selecting between them only requires the addition of a command line argument. The commands to build in each type of mode are outlined below.

There are a few packages, including PyInstaller, must be installed via conda or pip before executing either of the `pyinstaller` commands below.
```
pip install pyinstaller
pip install path
```
The output for both of the commands will be in the `dist` directory. If the mode argument is left off, `onefile` is assumed.

#### pyinstaller onefile
```
pyinstaller cq-cli_pyinstaller.spec onefile
```

#### pyinstaller directory
```
pyinstaller cq-cli_pyinstaller.spec dir
```
