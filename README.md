# easy-data-analysis: plotting and statistical analysis tools for scientific research

## Overview

This package provides tools to analyze scientific research data, with a focus on plotting and statistical analysis. It is written in Python and was tested on Linux and MacOS.

## Compatibility

This package is written in Python 3.6 and was tested on Linux and MacOS 13. It depends on the following libraries:
* matplotlib 3.1.3
* numpy 1.18.4
* pandas 0.25.3
* scipy 1.4.1

## Installation

If you are new to installation of Python and its packages, a [tutorial](https://packaging.python.org/tutorials/installing-packages/) is on the Python's website.

Installing Python libraries is most easily done with `pip`, simply run in a terminal:
```
pip install --upgrade <library>
```

`easy-data-analysis` is packaged and available through [PyPI](https://pypi.org), you can install it by running in a terminal:
```
pip install --upgrade easy-data-analysis
```

Source distributions are also available here on GitHub, download the source and install it by running:
```
pip install <path>
```

## Command Line Interface

`easy-data-analysis` is accessible through a command line interface which follows this syntax:
```
eda <command> <subcommand> [arguments ...]
```

Type this in your terminal for more information:
```
eda --help
```

### `configure` command

```
eda configure <subcommand>
```

`configure` manages the default arguments of all commands, i.e. the behaviour of commands when you do not provide optional arguments.
Available subcommands:
* `spectrum`: configure `eda plot spectrum`
* `kinetics`: configure `eda plot kinetics`
* `default`: rollback to the original configuration (the one provided when you install this package)

When you enter the configuration mode, instructions will be displayed before you are prompted for input. The name of the parameter is displayed followed by its current value between ( parentheses ).
You have three possible actions (validate any of them by pressing <Enter>):
* keep the current value: leave the input field empty
* modify the current value: type your input (if a list is expected, use space to separate values)
* enter a void value (no value): enter 'none' (without quotes)

### `plot` command

```
eda plot <subcommand> [arguments ...]
```

`plot` reads a CSV file and plots the data according to one of the following subcommands:
* `spectrum`
* `kinetics`

#### `spectrum` subcommand

This subcommand plots absorption spectra.
```
eda plot spectrum [arguments ...]
```
File names are positional arguments, they should be passed before optional argument. Optional arguments include:
* `-l` or `--label` specify labels on data for the plot legend
* `--figure-size` specify width and height in inches
* `--xcolumn` name of the column containing x-axis values
* `--ycolumn` name of the column containing y-axis values
* `--xlabel` label on the plot's x-axis
* `--ylabel` label on the plot's y-axis
* `--xlimit` specify left and right values for x-axis limits
* `--ylimit` specify bottom and top values for y-axis limits
* `--skip-header` number of rows to skip at the beginning of the file
* `--legend-location` run `eda plot spectrum -h` for more information
* `--title` specify the title of the plot

For example:
```
eda plot spectrum file1.csv file2.csv -l experiment1 experiment2
```

For more information:
```
eda plot spectrum -h
```

#### `kinetics` subcommand

This subcommand plots absorption kinetics curves. It can also plot an exponential model curve fitted on the data. Parameters of the model will be printed on the console.
```
eda plot kinetics [arguments ...]
```

File names are positional arguments and should be passed before optional arguments. Optional arguments include:
* `-l` or `--label` specify labels on data for the plot legend
* `-m` or `--model` is a flag indicating an exponential model should be fitted on the data
* `--figure-size` specify width and height in inches
* `--xcolumn` name of the column containing x-axis values
* `--ycolumn` name of the column containing y-axis values
* `--xlabel` label on the plot's x-axis
* `--ylabel` label on the plot's y-axis
* `--xlimit` specify left and right values for x-axis limits
* `--ylimit` specify bottom and top values for y-axis limits
* `--skip-header` number of rows to skip at the beginning of the file
* `--legend-location` run `eda plot spectrum -h` for more information
* `--title` specify the title of the plot

For example:
```
eda plot kinetics file1.csv file2.csv -l experiment1 experiment2 -m
```

For more information:
```
eda plot kinetics -h
```
