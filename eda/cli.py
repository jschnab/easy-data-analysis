#!/usr/bin/env python3

import sys

from argparse import ArgumentParser
from os import path as ospath
from pathlib import Path
from shutil import copyfile

from eda import kinetics
from eda import spectrum
from eda.configure import ConfigurationManager


class CliParser:
    def __init__(self):
        parser = ArgumentParser(
            description=(
                "Tools for easy scientific data analysis. Please visit "
                "https://github.com/jschnab/easy-data-analysis.git for "
                "detailed information and a tutorial."
            ),
            usage="eda <command> <subcommand> [parameters ...]",
        )
        parser.add_argument(
            "command",
            help="Valid commands are {configure,plot}",
        )
        args = parser.parse_args(sys.argv[1:2])
        if not hasattr(self, args.command):
            print(f"unrecognized command '{args.command}'")
            parser.print_help()
            sys.exit(1)
        # create the configuration file if it does not exist
        home = str(Path.home())
        self.config_user = ospath.join(home, ".edaconf")
        if not ospath.exists(self.config_user):
            here = ospath.abspath(ospath.dirname(__file__))
            self.config_default = ospath.join(here, "config_default.yaml")
            copyfile(self.config_default, self.config_user)
        # use dispatch pattern to invoke command with same name
        getattr(self, args.command)()

    def configure(self):
        parser = ArgumentParser(
            description=("Configure default parameters"),
            usage="eda configure <subcommand>",
        )
        parser.add_argument(
            "subcommand",
            help=(
                "Valid subcommands are {default,kinetics,spectrum}. Use "
                "'default' to rollback to default configuration, 'kinetics' "
                "or 'spectrum' to configure corresponding 'eda plot' "
                "subcommands."
            ),
        )
        args = parser.parse_args(sys.argv[2:3])
        config = ConfigurationManager()
        if not hasattr(config, args.subcommand):
            print(f"unrecognized subcommand '{args.subcommand}'")
            parser.print_help()
            sys.exit(1)
        getattr(config, args.subcommand)(args.subcommand)

    def plot(self):
        parser = ArgumentParser(
            description="Draw a plot from data stored in a CSV file",
            usage="eda plot <subcommand> [parameters ...]",
        )
        parser.add_argument(
            "subcommand",
            help=("Valid subcommands are {kinetics,spectrum}"),
        )
        args = parser.parse_args(sys.argv[2:3])
        if not hasattr(self, args.subcommand):
            print(f"unrecognized subcommand '{args.subcommand}'")
            parser.print_help()
            sys.exit(1)
        getattr(self, args.subcommand)()

    def spectrum(self):
        parser = ArgumentParser(
            description=("Plot an absorbance spectrum"),
            usage=(
                "eda plot spectrum file [file ...] [-h] [-l] [--figure-size] "
                "[--xcolumn] [--ycolumn] [--xlabel] [--ylabel] [--xlimit] "
                "[--ylimit] [--skip-header] [--legend-location] [--title]"
            ),
        )
        parser.add_argument(
            "file",
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
            "--figure-size",
            nargs=2,
            type=float,
            help="Specify figure size (inches)",
            dest="fig_size",
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
        parser.add_argument(
            "--legend-location",
            nargs="?",
            type=str,
            help="Specify the position of the legend on the plot",
            choices=[
                "best",
                "upper right",
                "upper left",
                "lower right",
                "lower left",
            ],
            dest="legend_loc",
        )
        parser.add_argument(
            "--title",
            nargs="?",
            type=str,
            help="Specify the title of the plot",
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
            legend_loc=args.legend_loc,
            title=args.title,
        )

    def kinetics(self):
        parser = ArgumentParser(
            description=(
                "Plot an absorbance kinetics curve"),
            usage=(
                "eda plot spectrum file [file ...] [-h] [-f] [-m] [-l] "
                "[--figure-size] [--xcolumn] [--ycolumn] [--xlabel] [--ylabel]"
                " [--xlimit] [--ylimit] [--skip-header] [--legend-location] "
                "[--title] [--time-unit] [--init-params]"
            ),
        )
        parser.add_argument(
            "file",
            nargs="+",
            help="CSV files storing data to plot",
        )
        parser.add_argument(
            "-f",
            "--fit",
            action="store_true",
            help=(
                "Fit the data using a model, specify model with the '-f' or "
                "'--fit' argument)"
            ),
        )
        parser.add_argument(
            "-m",
            "--model",
            choices=["linear", "exp1", "exp2", "exp"],
            help=(
                "Specify the model to use when fitting data, choose 'linear' "
                "(linear model), 'exp1' (first-order exponential), 'exp2' "
                "(second-order exponential), or 'exp' (select the best fit "
                "between 'exp1' and 'exp2')"
            ),
        )
        parser.add_argument(
            "--init-params",
            nargs="+",
            type=float,
            help=(
                "The initial parameters to use when fitting data (make sure "
                "the number of parameters is appropriate for the selected "
                "model)"
            ),
        )
        parser.add_argument(
            "-l",
            "--label",
            nargs="*",
            help="Specify the plot legend labels to use for each file",
        )
        parser.add_argument(
            "--figure-size",
            nargs=2,
            type=float,
            help="Specify figure size (inches)",
            dest="fig_size",
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
        parser.add_argument(
            "--legend-location",
            nargs="?",
            type=str,
            help="Specify the position of the legend on the plot",
            choices=[
                "best",
                "upper right",
                "upper left",
                "lower right",
                "lower left",
            ],
            dest="legend_loc",
        )
        parser.add_argument(
            "--title",
            nargs="?",
            type=str,
            help="Title of the plot",
        )
        parser.add_argument(
            "--time-unit",
            choices=["minute", "second"],
            help="Time unit of the kinetics experiment",
        )
        args = parser.parse_args(sys.argv[3:])
        kinetics.run(
            input_files=args.file,
            fit=args.fit,
            model=args.model,
            init_params=args.init_params,
            labels=args.label,
            fig_size=args.fig_size,
            x_col=args.xcolumn,
            y_col=args.ycolumn,
            x_lab=args.xlabel,
            y_lab=args.ylabel,
            x_lim=args.xlimit,
            y_lim=args.ylimit,
            skip_header=args.skip_header,
            legend_loc=args.legend_loc,
            title=args.title,
            time_unit=args.time_unit,
        )


def main():
    CliParser()


if __name__ == "__main__":
    main()
