#!/usr/bin/env python3

import sys

from argparse import ArgumentParser

from eda import kinetics
from eda import spectrum


class CliParser:
    def __init__(self):
        parser = ArgumentParser(
            description="Tools for easy scientific data analysis",
            usage="eda <command> <subcommand> [parameters]",
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
            usage="eda plot <subcommand> [parameters]",
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
        args = parser.parse_args(sys.argv[3:])
        spectrum.run(
            input_files=args.file,
            labels=args.label,
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
