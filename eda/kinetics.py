import logging
import sys
import yaml

from collections import OrderedDict
from os import path as ospath
from pathlib import Path
from tempfile import TemporaryDirectory

import matplotlib.pyplot as plt
import pandas as pd

from eda.models import (
    test_exponential_models,
    fit_data_catch_error,
    fit_with_expression,
    get_model_info,
    print_params,
)
from eda.utils import (
    get_end_of_data,
    get_linesep,
    get_number_lines,
    format_newlines,
    log_errors,
)

logging.basicConfig(
    filename=f"{str(Path.home())}/.edalog",
    format="%(asctime)s - %(levelname)s: %(message)s",
    level=logging.DEBUG,
)

# plotting parameters
EXP_COLOR = "black"
MARKERS = ["o", "v", "^", "s", "D", "*", "P", "X", "<", ">"]
FIT_COLOR = "grey"


@log_errors
def plot_kinetics(
    input_data,
    models,
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
    Plot absorbance kinetics from a pandas DataFrame, and overlays
    provided fitted data, if provided.

    :param list[pandas.DataFrame] input: dataframes containing the data to plot
    :param list[pandas.DataFrame] models: dataframes containing fitted data
                                          to overlay
    :param list[str] labels: name of each curve in the plot
    """
    fig, ax = plt.subplots(figsize=fig_size)
    for i, df in enumerate(input_data):
        ax.scatter(
            df[x_col],
            df[y_col],
            c=EXP_COLOR,
            marker=MARKERS[i],
            label=labels[i],
            zorder=4,
        )
        if not models[i].empty:
            ax.plot(
                models[i].x,
                models[i].y,
                c=FIT_COLOR,
                label="Fitted",
                zorder=0,
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
    # remove duplicated legend
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), loc=legend_loc)
    plt.show()


@log_errors
def run(input_files, **kwargs):
    """
    Convert CSV files line endings and plot absorbance kinetics one the
    same graph.

    :param list[str] input_files: list of file paths to process
    :param list[str] labels: labels of the plot legend, optional
                             (defaults to file names)
    :param bool model: whether to model the data and plot the fitted
                       curve or not, optional
    """
    config_file = ospath.join(str(Path.home()), ".edaconf")
    with open(config_file) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)["plot"]["kinetics"]

    kwargs = {k: v for k, v in kwargs.items() if v is not None}

    # get labels and check their number
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

    with TemporaryDirectory() as temp_dir:

        input_data = []
        models = []

        for infile, label in zip(input_files, kwargs["labels"]):
            # make sure the file has correct newlines
            output_path = ospath.join(temp_dir, "formatted.csv")
            linesep = get_linesep(infile)
            format_newlines(infile, len(linesep), output_path)

            # determine at which row data ends
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
            input_data.append(df)

            # will be replaced by fitted data if we fit
            fitted = pd.DataFrame()

            # fit data
            if kwargs.get("fit", config["fit"]):

                # use an arbitrary user-input model
                if kwargs.get("expression"):
                    model, popt, perr, fitted, r = fit_with_expression(
                        df[kwargs.get("x_col", config["xcolumn"])],
                        df[kwargs.get("y_col", config["ycolumn"])],
                        kwargs.get("expression"),
                        kwargs.get("init_params"),
                    )

                # use a hard-encoded model
                else:
                    model = kwargs.get("model", config["model"])
                    if not model:
                        raise ValueError(
                            "No model was selected. Please pass a model as an "
                            "argument to `eda plot kinetics` or configure the "
                            "default model")

                    if model == "exp":
                        model, popt, perr, fitted, r = test_exponential_models(
                            df[kwargs.get("x_col", config["xcolumn"])],
                            df[kwargs.get("y_col", config["ycolumn"])],
                            kwargs.get(
                                "init_params",
                                config["init_params"]["exp1"]),
                            kwargs.get(
                                "init_params",
                                config["init_params"]["exp2"]),
                        )

                    else:
                        popt, perr, fitted, r = fit_data_catch_error(
                            df[kwargs.get("x_col", config["xcolumn"])],
                            df[kwargs.get("y_col", config["ycolumn"])],
                            get_model_info(model)["function"],
                            kwargs.get(
                                "init_params",
                                config["init_params"][model]),
                        )

                # print calculated model parameters
                print()
                print_params(
                    label,
                    model,
                    popt,
                    perr,
                    r,
                    kwargs.get("time_unit", config["time_unit"]),
                )

            # add fitted data to the list
            models.append(fitted)

        plot_kinetics(
            input_data,
            models,
            kwargs["labels"],
            fig_size=kwargs.get("fig_size", config["figure_size"]),
            x_col=kwargs.get("x_col", config["xcolumn"]),
            y_col=kwargs.get("y_col", config["ycolumn"]),
            x_lab=kwargs.get("x_lab", config["xlabel"]),
            y_lab=kwargs.get("y_lab", config["ylabel"]),
            x_lim=kwargs.get("x_lim", config["xlimit"]),
            y_lim=kwargs.get("y_lim", config["ylimit"]),
            legend_loc=kwargs.get("legend_loc", config["legend_location"]),
            title=kwargs.get("title"),
        )
