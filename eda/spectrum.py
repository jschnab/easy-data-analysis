#!/usr/bin/env python3

import os
import sys

from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import pandas as pd

from photochemistry.utils import linuxize_newlines

# CSV file parameters
WAVELENGTH_COL = "Wavelength (nm)"
ABSORB_COL = "Abs"
USE_COLS = list(range(2))
SKIP_HEADER = 1
SKIP_FOOTER = 37

# plotting parameters
COLOR = "black"
X_LABEL = "Wavelength (nm)"
Y_LABEL = "Absorbance (A.U.)"


def plot_spectrum(df):
    """
    Plot a spectrum from a pandas DataFrame.
    Assumes two columns named 'Wavelength (nm)' and 'Abs'.

    :param pandas.DataFrame df: contains the data to plot.
    """
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.plot(df[WAVELENGTH_COL], df[ABSORB_COL], c=COLOR)
    ax.set_xlim(300, 500)
    ax.set_ylim(0.1, 1.2)
    ax.set_xlabel(X_LABEL, fontsize=16)
    ax.set_ylabel(Y_LABEL, fontsize=16)
    for side in ["top", "right"]:
        ax.spines[side].set_visible(False)
    plt.show()


def run(input_name):
    with TemporaryDirectory() as temp_dir:
        output_name = os.path.join(temp_dir, "spectrum.csv")
        linuxize_newlines(input_name, output_name)
        df = pd.read_csv(
            output_name,
            usecols=USE_COLS,
            engine="python",
            skiprows=SKIP_HEADER,
            skipfooter=SKIP_FOOTER,
        )
        filtered = df[df[WAVELENGTH_COL] > 300]
        plot_spectrum(filtered)


def main():
    if len(sys.argv) < 2:
        print("Usage:", sys.argv[0], "<file name>")
        sys.exit(1)

    input_name = sys.argv[1]

    with TemporaryDirectory() as temp_dir:
        output_name = os.path.join(temp_dir, "spectrum.csv")
        linuxize_newlines(input_name, output_name)
        df = pd.read_csv(
            output_name,
            usecols=USE_COLS,
            engine="python",
            skiprows=SKIP_HEADER,
            skipfooter=SKIP_FOOTER,
        )
        filtered = df[df[WAVELENGTH_COL] > 300]
        plot_spectrum(filtered)


if __name__ == "__main__":
    main()
