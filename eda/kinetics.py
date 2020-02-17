import os
import sys

from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.optimize import curve_fit

from eda.utils import linuxize_newlines, get_number_lines, get_end_of_data

# curve fitting initial parameters
INIT_PARAMS = [-1, -1, 1]

# CSV file parameters
TIME_COL = "Time (min)"
ABSORB_COL = "Abs"
USE_COLS = list(range(2))
SKIP_HEADER = 1
SKIP_FOOTER = 27

# plotting parameters
EXP_COLOR = "black"
MARKERS = ["o", "v", "^", "s", "D", "*", "P", "X", "<", ">"]
FIT_COLOR = "grey"
X_LABEL = "Time (min)"
Y_LABEL = "Absorbance (A.U.)"
LEGEND_LOC = "lower right"


def exponential(x, a, k, b):
    """
    Defines a general exponential function.
    """
    return a * np.exp(k * x) + b


def fit_data(x, y, func, initial_parameters=None):
    """
    Fit experimental data with a function.

    :param array-like x: independent variable data
    :param array-like y: dependent variable data
    :param callable func: function to fit on the data
    :param array-like initial_parameters: start curve fitting with these
                                          parameters
    :return: optimal parameters, parameters standard error, fitted data
    """
    popt, pcov = curve_fit(func, x, y, initial_parameters)
    perr = np.sqrt(np.diag(pcov))
    fitted = func(x, *popt)
    return popt, perr, fitted


def plot_kinetics(dfs, models=None, labels=None):
    """
    Plot absorbance kinetics from a pandas DataFrame, and overlays
    provided fitted data, if provided.

    :param list[pandas.DataFrame] dfs: list of dataframes containing
                                       the data to plot
    :param list[array-like] models: list of fitted data to overlay
    :param list[str] labels: name of each curve in the plot
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    for i, df in enumerate(dfs):
        ax.scatter(
            df[TIME_COL],
            df[ABSORB_COL],
            c=EXP_COLOR,
            marker=MARKERS[i],
            label=labels[i],
            zorder=4,
        )
        if not models[i].empty:
            ax.plot(
                df[TIME_COL],
                models[i],
                c=FIT_COLOR,
                label="Fitted",
                zorder=0,
            )
    ax.set_xlim(-0.5, 7.5)
    ax.set_ylim(0.2, 1.2)
    ax.set_xlabel(X_LABEL, fontsize=16)
    ax.set_ylabel(Y_LABEL, fontsize=16)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    plt.legend(loc=LEGEND_LOC)
    plt.show()


def run(input_files, labels=None, model=None):
    """
    Convert CSV files line endings and plot absorbance kinetics one the
    same graph.

    :param list[str] input_files: list of file paths to process
    :param list[str] labels: labels of the plot legend, optional
                             (defaults to file names)
    :param bool model: whether to model the data and plot the fitted
                       curve or not, optional
    """
    if not labels:
        labels = [
            os.path.split(os.path.abspath(infile))[-1]
            for infile in input_files
        ]
    dfs = []
    models = []
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
            dfs.append(df)
            fitted = pd.Series()
            if model:
                popt, perr, fitted = fit_data(
                    df[TIME_COL],
                    df[ABSORB_COL],
                    exponential,
                    initial_parameters=INIT_PARAMS,
                )
            models.append(fitted)
        plot_kinetics(dfs, models, labels)
