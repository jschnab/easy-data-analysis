#!/usr/bin/env python3

import sys

from argparse import ArgumentParser

from eda import kinetics
from eda import spectrum


class CliParser:
    def __init__(self):
        parser = ArgumentParser(
            description=(
                "Tools for easy scientific data analysis. Please visit "
                "https://github.com/jschnab/easy-data-analysis.git for "
                "detailed information and a tutorial."
            ),
            usage="eda <command> <subcommand> [parameters, ...]",
        )
        parser.add_argument(
            "command",
            help="Valid commands are {plot}",
        )
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print(f"unrecognized command '{args.command}'")
            parser.print_help()
            sys.exit(1)
        # use dispatch pattern to invoke command with same name
        getattr(self, args.command)()

    def plot(self):
        parser = ArgumentParser(
            description="Draw a plot from data stored in a CSV file",
            usage="eda plot <subcommand> [parameters, ...]",
        )
        parser.add_argument(
            "subcommand",
            help=(
                "Valid subcommands are {spectrum,kinetics}"
            ),
        )
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.subcommand):
            print(f"unrecognized subcommand '{args.subcommand}'")
            parser.print_help()
            sys.exit(1)
        getattr(self, args.subcommand)()

    def spectrum(self):
        parser = ArgumentParser(
            description=(
                f"Plot an absorbance spectrum. "
                "You can plot one or several files using -f followed by "
                "space-separated file names"
            ),
            usage="eda plot spectrum [-h] [-f]",
        )
        parser.add_argument(
            "-f",
            "--file",
            nargs="+",
            help="CSV files storing data to plot",
        )
        parser.add_argument(
            "-l",
            "--label",
            nargs="*",
            help="Specify the plot legend labels to use for each file",
        )
        parser.add_argument(
            "--fig-size",
            nargs=2,
            type=float,
            help="Specify figure size (inches)",
        )
        parser.add_argument(
            "--xcolumn",
            nargs="?",
            help="Specify the name of the column containing x-axis values",
        )
        parser.add_argument(
            "--ycolumn",
            nargs="?",
            help="Specify the name of the column containing y-axis values",
        )
        parser.add_argument(
            "--xlabel",
            nargs="?",
            help="Specify the label of the plot's x-axis",
        )
        parser.add_argument(
            "--ylabel",
            nargs="?",
            help="Specify the label of the plot's y-axis",
        )
        parser.add_argument(
            "--xlimit",
            nargs=2,
            type=float,
            help="Specify the lower and upper limits of the plot's x-axis",
        )
        parser.add_argument(
            "--ylimit",
            nargs=2,
            type=float,
            help="Specify the lower and upper limits of the plot's y-axis",
        )
        parser.add_argument(
            "--skip-header",
            nargs="?",
            type=int,
            help=(
                "Specify the number of rows to skip at the beginning of the "
                "CSV file"
            ),
            dest="skip_header",
        )
        args = parser.parse_args(sys.argv[3:])
        spectrum.run(
            input_files=args.file,
            labels=args.label,
            fig_size=args.fig_size,
            x_col=args.xcolumn,
            y_col=args.ycolumn,
            x_lab=args.xlabel,
            y_lab=args.ylabel,
            x_lim=args.xlimit,
            y_lim=args.ylimit,
            skip_header=args.skip_header,
        )

    def kinetics(self):
        parser = ArgumentParser(
            description=(
                "Plot an absorbance kinetics curve. "
                "You can plot one or several files using -f followed by "
                "space-separated file names"
            ),
            usage="eda plot kinetics [-h] [-f] [-m]",
        )
        parser.add_argument(
            "-f",
            "--file",
            nargs="+",
            help="CSV files storing data to plot",
        )
        parser.add_argument(
            "-m",
            "--model",
            action="store_true",
            help="Model the data using exponential decay",
        )
        parser.add_argument(
            "-l",
            "--label",
            nargs="*",
            help="Specify the plot legend labels to use for each file",
        )
        args = parser.parse_args(sys.argv[3:])
        kinetics.run(
            input_files=args.file,
            model=args.model,
            labels=args.label,
        )


def main():
    CliParser()


if __name__ == "__main__":
    main()
