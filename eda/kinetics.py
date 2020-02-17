#!/usr/bin/env python3

import os
import sys

from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from scipy.optimize import curve_fit

from eda.utils import linuxize_newlines

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
FIT_COLOR = "grey"
X_LABEL = "Time (min)"
Y_LABEL = "Absorbance (A.U.)"


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


def plot_kinetics(df, fitted=None):
    """
    Plot absorbance kinetics from a pandas DataFrame, and overlays
    provided fitted data, if provided.

    :param pandas.DataFrame df: contains the data to plot
    :param array-like fitted: fitted data to overlay
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.scatter(
        df[TIME_COL],
        df[ABSORB_COL],
        c=EXP_COLOR,
        label="Experimental",
        zorder=4,
    )
    if not fitted.empty:
        ax.plot(
            df[TIME_COL],
            fitted,
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
    plt.legend()
    plt.show()


def run(input_name, fit=None):
    with TemporaryDirectory() as temp_dir:
        output_name = os.path.join(temp_dir, "kinetics.csv")
        linuxize_newlines(input_name, output_name)
        df = pd.read_csv(
            output_name,
            usecols=USE_COLS,
            engine="python",
            skiprows=SKIP_HEADER,
            skipfooter=SKIP_FOOTER,
        )
        fitted = pd.Series()
        if fit:
            popt, perr, fitted = fit_data(
                df[TIME_COL],
                df[ABSORB_COL],
                exponential,
                initial_parameters=INIT_PARAMS,
            )
        plot_kinetics(df, fitted)


def main():
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "<file name>")
        sys.exit(1)

    input_name = sys.argv[1]

    with TemporaryDirectory() as temp_dir:
        output_name = os.path.join(temp_dir, "kinetics.csv")
        linuxize_newlines(input_name, output_name)
        df = pd.read_csv(
            output_name,
            usecols=USE_COLS,
            engine="python",
            skiprows=SKIP_HEADER,
            skipfooter=SKIP_FOOTER,
        )
        popt, perr, fitted = fit_data(
            df[TIME_COL],
            df[ABSORB_COL],
            exponential,
            initial_parameters=INIT_PARAMS,
        )
        plot_kinetics(df, fitted)


if __name__ == "__main__":
    main()
