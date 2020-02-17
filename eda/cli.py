#!/usr/bin/env python3

import sys

from argparse import ArgumentParser

from eda import kinetics
from eda import spectrum


class CliParser:
    def __init__(self):
        parser = ArgumentParser(
            description="Tools for easy scientific data analysis",
            usage="pchem <command> <subcommand> [parameters]",
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
            usage="pchem plot <subcommand> [parameters]",
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
            description="Plot an absorbance spectrum",
            usage="pchem plot spectrum [-h] file",
        )
        parser.add_argument(
            "file",
            help="CSV file storing data to plot",
        )
        args = parser.parse_args(sys.argv[3:])
        spectrum.run(
            input_name=args.file,
        )

    def kinetics(self):
        parser = ArgumentParser(
            description="Plot an absorbance kinetics curve",
            usage="pchem plot kinetics [-h] [-f] file",
        )
        parser.add_argument(
            "file",
            help="CSV file storing data to plot",
        )
        parser.add_argument(
            "-f",
            "--fit",
            action="store_true",
            help="Fit the data using exponential decay",
        )
        args = parser.parse_args(sys.argv[3:])
        kinetics.run(
            input_name=args.file,
            fit=args.fit,
        )


def main():
    CliParser()


if __name__ == "__main__":
    main()
