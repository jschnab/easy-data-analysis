import logging
import os
import sys

from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import pandas as pd

from eda.utils import (
    linuxize_newlines,
    get_number_lines,
    get_end_of_data,
    log_errors,
)

HOME = str(Path.home())

logging.basicConfig(
    filename=f"{HOME}/eda_errors.log",
    format="%(asctime)s - %(levelname)s: %(message)s",
    level=logging.DEBUG,
)

# CSV file parameters
WAVELENGTH_COL = "Wavelength (nm)"
ABSORB_COL = "Abs"
USE_COLS = list(range(2))
SKIP_HEADER = 1

# plotting parameters
COLORS = ["black", "C0", "C1", "C2", "C3", "C4", "C5", "C6", "C7", "C8", "C9"]
X_LABEL = "Wavelength (nm)"
Y_LABEL = "Absorbance (A.U.)"
LEGEND_LOC = "lower left"


@log_errors
def plot_spectrum(dfs, labels):
    """
    Plot a spectrum from a pandas DataFrame.
    Assumes two columns named 'Wavelength (nm)' and 'Abs'.

    :param list[pandas.DataFrame] dfs: list of dataframes which contain the
                                       data to plot.
    :param list[str] labels: name of each curve in the plot
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, df in enumerate(dfs):
        ax.plot(
            df[WAVELENGTH_COL],
            df[ABSORB_COL],
            c=COLORS[i],
            label=labels[i],
        )
    ax.set_xlim(300, 500)
    ax.set_xlabel(X_LABEL, fontsize=16)
    ax.set_ylabel(Y_LABEL, fontsize=16)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    plt.legend(loc=LEGEND_LOC)
    plt.show()


@log_errors
def run(input_files, labels=None):
    """
    Convert CSV files line endings and plot spectra on the same graph.

    :param list[str] input_files: list of file paths to process
    :param list[str] labels: labels of the plot legend, optional (defaults
                             to file names
    """
    if not labels:
        labels = [
            os.path.split(os.path.abspath(infile))[-1]
            for infile in input_files
        ]
    if len(labels) != len(input_files):
        print(
            "Error: there should be as many labels as files, "
            f"got {len(input_files)} file(s) but {len(labels)} label(s)"
        )
        sys.exit(1)
    dfs = []
    with TemporaryDirectory() as temp_dir:
        for infile in input_files:
            output_path = os.path.join(temp_dir, "linuxized.csv")
            linuxize_newlines(infile, output_path)
            n_lines = get_number_lines(output_path)
            end_of_data = get_end_of_data(output_path)
            skip_footer = n_lines - end_of_data
            df = pd.read_csv(
                output_path,
                usecols=USE_COLS,
                engine="python",
                skiprows=SKIP_HEADER,
                skipfooter=skip_footer,
            )
            filtered = df[df[WAVELENGTH_COL] > 300]
            dfs.append(filtered)
        plot_spectrum(dfs, labels)
