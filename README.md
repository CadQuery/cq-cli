# cq-cli

![tests](https://github.com/CadQuery/cq-cli/workflows/tests/badge.svg)

## Contents

* [Introduction](https://github.com/CadQuery/cq-cli#introduction)
* [Getting Help](https://github.com/CadQuery/cq-cli#getting_help)
* [Installation](https://github.com/CadQuery/cq-cli#installation)
* [Usage](https://github.com/CadQuery/cq-cli#usage)
* [Examples](https://github.com/CadQuery/cq-cli#examples)
* [Drawbacks](https://github.com/CadQuery/cq-cli#drawbacks)
* [Contributing](https://github.com/CadQuery/cq-cli#contributing)

## Introduction

***Please Note*** cq-cli is in alpha currently. Major features may be broken, and the application may change a lot before a full release.

cq-cli is a Command Line Interface for executing CadQuery scripts and converting their output to another format. It uses a plugin system where "codecs" can be placed in the cqcodecs directory and will be automatically loaded and used if a user selects that codec from the command line.

cq-cli is designed to be a batteries-included distribution, although this approach comes with some drawbacks as listed below. However, to have a CadQuery conversion utility that requires no installation and no Anaconda environment can be useful in certain cases.

It is possible to specify input and output files using arguments, but cq-cli also allows the use to the stdin, stdout and stderr streams so that it can be used in a pipeline.

Linux, MacOS and Windows are supported, but some features may be used differently or may not work the same in Windows.

## Getting Help

In addition to opening an issue on this repo, there is a [CadQuery Discord channel](https://discord.gg/qz3uAdF) and a [Google Group](https://groups.google.com/g/cadquery) that you can join to ask for help getting started with cq-cli.

## Installation

Download a binary distribution that is appropriate for your operating system from the [latest release](https://github.com/CadQuery/cq-cli/releases/tag/v0.1.0-alpha), extract the zip file, and make sure to put the cq-cli binary in the PATH. Then the CLI can be invoked as `cq-cli` (`cq-cli.exe` on Windows).

If installing on Windows, the [latest redistributable for Visual Studio](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads) will need to be installed.

If a development installation is desired, see the [Contributing](#contributing) section below.

## Usage

usage: cq-cli.py [-h] [--codec CODEC] [--infile INFILE] [--outfile OUTFILE] [--errfile ERRFILE] [--params PARAMS] [--validate VALIDATE]

Command line utility for converting CadQuery script output to various other output formats.

optional arguments:
* -h, --help Show this help message and exit
* --codec CODEC The codec to use when converting the CadQuery output. Must match the name of a codec file in the cqcodecs directory.
* --infile INFILE The input CadQuery script to convert.
* --outfile OUTFILE File to write the converted CadQuery output to. Prints to stdout if not specified.
* --errfile ERRFILE File to write any errors to. Prints to stderr if not specified.
* --params PARAMS A colon and semicolon delimited string (no spaces) of key/value pairs representing variables and their values in the CadQuery script. i.e. var1:10.0;var2:4.0;
* --validate VALIDATE Setting to true forces the CLI to only parse and validate the script and not produce converted output.

## Examples

1. Find out what codecs are available.
```
./cq-cli.py --codec help
```
2. Validate a CadQuery script.
```
./cq-cli.py --validate true --infile /input/path/script.py
```
3. Convert a CadQuery script to STEP format and output to stdout.
```
./cq-cli.py --codec step --infile /input/path/script.py
```
4. Convert a CadQuery script to STEP format and write to a file.
```
./cq-cli.py --codec step --infile /input/path/script.py --outfile /output/path/newfile.step
```
5. Convert a CadQuery script and write any errors to a separate file.
```
./cq-cli.py --codec step --infile /input/path/script.py -errfile /error/path/error.txt
```
6. Convert a CadQuery script using the stdin and stdout streams. This example counts the lines in the resulting STEP output as a trivial example.
```
cat /input/path/script.py | cq-cli.py --codec step | wc -l
```

## Drawbacks

* The file (and directory) size for cq-cli is very large. cq-cli uses pyinstaller to package the binaries for each platform, and must embed all needed dependencies. The OCP and OCCT library dependencies add a minimum of ~270 MB of data on top of the included Python distribution. It is possible that the pyinstaller spec file could be optimized. If you are interested in helping with this, please let us know by opening an issue.
* Startup times for the single binary are relatively slow. If startup and execution time is important to you, consider using the pyinstaller_dir.spec spec file with pyinstaller: `pyinstaller pyinstaller_dir.spec`.

## Contributing

If you want to help improve and expand cq-cli, the following steps should get you up and running with a development setup. There is a  [CadQuery Discord channel](https://discord.gg/qz3uAdF) and a [Google Group](https://groups.google.com/g/cadquery) that you can join to ask for help getting started.

### Anaconda Environment

A CadQuery Anaconda environment is required to run and build cq-cli via PyInstaller. For those unfamiliar (or uncomfortable) with Anaconda, it is probably best to start by installing Miniconda to a local directory and to avoid running `conda init`. After performing a local directory installation, an Anaconda environment can be activated via the [scripts,bin]/activate scripts. This will help avoid polluting and breaking the local Python installation.

Once the conda command is available, it is recommended that users build the environment from the latest master of the cadquery repo.
```
conda create -n cq-cli
conda activate cq-cli
conda install -c cadquery -c conda-forge cadquery=master
```

### Adding a Codec

The codec plugin system is based on naming conventions so that cq-cli knows what codec options to accept from the user. When adding a codec, make sure to place it in the `cqcodecs` directory and follow the naming convention `cq_codec_[your codec name].py`. The `your codec name` part of the filename will automatically be used as the codec name that the user specifies.

A good example to start with when creating your own codec would be `cqcodecs/cq_codec_step.py` as it shows a simple implementation of the codec that relies on CadQuery to do all the heavy lifting. At the very least, your codec needs to have a `convert` function that takes in a [CQGI BuildResult object](https://cadquery.readthedocs.io/en/latest/cqgi.html#cadquery.cqgi.BuildResult) and returns a string representing the converted model(s). As an alternative, cq-cli will pass the output file name, which makes it possible to write the output to the outfile path directly from the codec. If `None` is returned from the `convert` function, cq-cli will assume that the output was written directly to the output file by the codec.

For pyinstaller to know about the new dynamically loaded codec, it must be added to the `hiddenimports` array in both cq-cli_onfile_pyinstaller.spec and cq-cli_dir_pyinstaller.spec files. Leave the `.py` off of the name when adding to the array, for instance `codec.cq_codec_step` is the string used for the STEP codec. When only running a codec locally and not contributing it, this step is not required.

### Adding a Codec Test

A test is required when adding a codec to cq-cli, but is easy to add. Add a file named `test_[your codec name]_codec.py` in the tests directory, and add the test to it. `test_step_codec.py` would be a good template to base any new tests off of.

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
