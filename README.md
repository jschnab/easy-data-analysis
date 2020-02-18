# easy-data-analysis: plotting and statistical analysis tools for scientific research

## Overview

This package provides tools to analyze scientific research data, with a focus on plotting and statistical analysis.

## Compatibility and Installation

This package is written in Python 3.6 and was tested on Linux and MacOS 13. It depends on the following libraries:
* matplotlib 3.1.3
* numpy 1.18.4
* pandas 0.25.3
* scipy 1.4.1

Installing these libraries is easily done with `pip`, simply run in a terminal:
```
pip install --upgrade <library>
```

`easy-data-analysis` is packaged and available through [PyPI](https://pypi.org), you can install it by running in a terminal:
```
pip install --upgrade easy-data-analysis
```

## Usage

At the moment `easy-data-analysis` is accessible through a command line interface, type this in your terminal for more information:
```
eda --help
```

Currently, the only available command is `plot` and give access to subommands `spectrum` and `kinetics`.

### `spectrum` subcommand

This subcommand plots absorption spectra from CSV files, run:
```
eda plot spectrum [arguments]
```

Arguments include:
* `-f` or `--file` specify names of files to process
* `-l` or `--label` specify labels on data for the plot legend

For example:
```
eda plot spectrum -f file1.csv file2.csv -l experiment1 experiment2
```

For more information:
```
eda plot spectrum -h
```

### `kinetics` subcommand

This subcommand plots absorption kinetics curves from CSV files, run:
```
eda plot kinetics [arguments]
```

Arguments include:
* `-f` or `--file` specify names of files to process
* `-l` or `--label` specify labels on data for the plot legend
* `-m` or `--model` is a flag indicating an exponential model should be fitted on the data

For example:
```
eda plot kinetics -f file1.csv file2.csv -l experiment1 experiment2 -m
```

For more information:
```
eda plot kinetics -h
```
