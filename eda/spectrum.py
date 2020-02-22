import logging
import sys
import yaml

from os import path as ospath
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import pandas as pd

from eda.utils import (
    format_newlines,
    get_linesep,
    get_end_of_data,
    get_number_lines,
    log_errors,
)

logging.basicConfig(
    filename=f"{str(Path.home())}/.edalog",
    format="%(asctime)s - %(levelname)s: %(message)s",
    level=logging.DEBUG,
)

# CSV file parameters
WAVELENGTH_COL = "Wavelength (nm)"
ABSORB_COL = "Abs"
USE_COLS = list(range(2))
SKIP_HEADER = 1

# plotting parameters
FIG_SIZE = (7, 5)
COLORS = ["black", "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
X_LABEL = "Wavelength (nm)"
Y_LABEL = "Absorbance (A.U.)"
X_LIM = None
Y_LIM = None
LEGEND_LOC = "lower left"


@log_errors
def plot_spectrum(
    dfs,
    labels,
    fig_size,
    x_col,
    y_col,
    x_lab,
    y_lab,
    x_lim,
    y_lim,
    legend_loc,
    title,
):
    """
    Plot a spectrum from a pandas DataFrame.
    Assumes two columns named 'Wavelength (nm)' and 'Abs'.

    :param list[pandas.DataFrame] dfs: list of dataframes which contain the
                                       data to plot.
    :param list[str] labels: name of each curve in the plot
    """
    fig, ax = plt.subplots(figsize=fig_size)
    for i, df in enumerate(dfs):
        ax.plot(
            df[x_col],
            df[y_col],
            c=COLORS[i],
            label=labels[i],
        )
    if x_lim:
        ax.set_xlim(*x_lim)
    if y_lim:
        ax.set_ylim(*y_lim)
    ax.set_xlabel(x_lab, fontsize=16)
    ax.set_ylabel(y_lab, fontsize=16)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    ax.set_title(title, fontsize=18)
    plt.legend(loc=legend_loc)
    plt.show()


@log_errors
def run(input_files, **kwargs):
    """
    Convert CSV files line endings and plot spectra on the same graph.

    :param list[str] input_files: list of file paths to process
    :param list[str] labels: labels of the plot legend, optional (defaults
                             to file names
    """
    config_file = ospath.join(str(Path.home()), ".edaconf")
    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)["plot"]["spectrum"]
    kwargs = {k: v for k, v in kwargs.items() if v is not None}
    if not kwargs.get("labels"):
        kwargs["labels"] = [
            ospath.split(ospath.abspath(infile))[-1]
            for infile in input_files
        ]
    if len(kwargs["labels"]) != len(input_files):
        print(
            "Error: there should be as many labels as files, "
            f"got {len(input_files)} file(s) but {len(kwargs['labels'])} "
            "label(s)"
        )
        sys.exit(1)
    dfs = []
    with TemporaryDirectory() as temp_dir:
        for infile in input_files:
            output_path = ospath.join(temp_dir, "formatted.csv")
            linesep = get_linesep(infile)
            format_newlines(infile, len(linesep), output_path)
            n_lines = get_number_lines(output_path)
            end_of_data = get_end_of_data(output_path)
            skip_footer = n_lines - end_of_data
            df = pd.read_csv(
                output_path,
                usecols=kwargs.get("use_cols", config["use_cols"]),
                engine="python",
                skiprows=kwargs.get("skip_header", config["skip_header"]),
                skipfooter=skip_footer,
            )
            dfs.append(df)
        plot_spectrum(
            dfs=dfs,
            labels=kwargs["labels"],
            fig_size=kwargs.get("fig_size", config["figure_size"]),
            x_col=kwargs.get("x_col", config["xcolumn"]),
            y_col=kwargs.get("y_col", config["ycolumn"]),
            x_lab=kwargs.get("x_lab", config["xlabel"]),
            y_lab=kwargs.get("y_lab", config["ylabel"]),
            x_lim=kwargs.get("x_lim", config["xlimit"]),
            y_lim=kwargs.get("y_lim", config["ylimit"]),
            legend_loc=kwargs.get("legend_loc", config["legend_location"]),
            title=kwargs.get("title", config["title"]),
        )
