import logging
import warnings

from pathlib import Path

import numpy as np
import pandas as pd

from scipy import stats
from scipy.optimize import curve_fit

from eda.utils import log_errors, send_warnings_to_log

logging.basicConfig(
    filename=f"{str(Path.home())}/.edalog",
    format="%(asctime)s - %(levelname)s: %(message)s",
    level=logging.DEBUG,
)

INITIAL_PARAMS_FIRST_ORDER_DECAY = [-1, -1]
INITIAL_PARAMS_SECOND_ORDER_DECAY = [0, 0, 0, 0]
BOUNDS = (-2, 2)
METHOD = "trf"
LOSS = "linear"
FTOL = 1e-6
MAX_NFEV = 1600


@log_errors
def first_order_exponential(x, a, k):
    """
    Defines a first-order exponential function.
    """
    return a * np.exp(k * x)


@log_errors
def second_order_exponential(x, a1, a2, k1, k2):
    """
    Defines a second-order exponential function.
    """
    return a1 * np.exp(k1 * x) + a2 * np.exp(k2 * x)


@log_errors
def linear(x, a, b):
    """
    Defines a linear function.
    """
    return a * x + b


@log_errors
def get_model_info(model_name):
    """
    Return information about a model given its name.

    :param str model_name: model name
    :return dict: model information
    """
    model_info = {
        "exp1": {
            "function": first_order_exponential,
            "equation": "y = a * exp(k * x)",
            "params": ["a", "k"],
        },
        "exp2": {
            "function": second_order_exponential,
            "equation": "y = a1 * exp(k1 * x) + a2 * exp(k2 * x)",
            "params": ["a1", "a2", "k1", "k2"],
        },
        "linear": {
            "function": linear,
            "equation": "y = a * x + b",
            "params": ["a", "b"],
        },
    }
    return model_info[model_name]


@log_errors
def get_t_half(k, unit="minutes"):
    """
    Calculate the t1/2 constant of an exponential function, and return
    its value in seconds.

    :param float k: exponential parameter of the function
    :param str unit: time unit of the data used to obtain k (optional,
                     default is minutes)
    :return float: t1/2 constant
    """
    multi = {"minutes": 60, "seconds": 1}
    return np.log(2) / abs(k) * multi[unit]


@log_errors
def fit_data(
    x,
    y,
    func,
    initial_parameters=INITIAL_PARAMS_FIRST_ORDER_DECAY,
    bounds=BOUNDS,
    method=METHOD,
    ftol=1e-8,
):
    """
    Fit experimental data with a function.

    :param array-like x: independent variable data
    :param array-like y: dependent variable data
    :param callable func: function to fit on the data
    :param array-like initial_parameters: start curve fitting with these
                                          parameters
    :return: optimal parameters, parameters standard error, fitted data
    """
    with warnings.catch_warnings():
        warnings.showwarning = send_warnings_to_log
        popt, pcov = curve_fit(
            func,
            x,
            y,
            p0=initial_parameters,
            bounds=bounds,
            method=method,
            ftol=ftol,
            loss=LOSS,
        )
    perr = np.sqrt(np.diag(pcov))
    rsq = get_r_sq_adj(y, func(x, *popt), len(popt))
    x_fitted = np.linspace(min(x), max(x), 10000)
    fitted = pd.DataFrame({
        "x": x_fitted,
        "y": func(x_fitted, *popt),
    })
    return popt, perr, fitted, rsq


@log_errors
def get_r_sq_adj(y, fitted, n_params):
    """
    Calculate the adjusted R-squared value of the model.

    :param numpy.array y: dependent variable
    :param numpy.array fitted: values fitted by the model
    :param int n_params: number of parameters of the model
    :return float: adjusted R-squared value
    """
    y_mean = y.mean()
    # total sum of squares
    syy = ((y - y_mean) ** 2).sum()
    # residual sum of squares
    resid_ss = ((y - fitted) ** 2).sum()
    # total mean square
    total_ms = syy / (n_params - 1)
    # residual mean square
    resid_ms = resid_ss / (len(y) - n_params)
    return (total_ms - resid_ms) / total_ms


@log_errors
def get_r_sq(y, fitted, n_params):
    """
    Calculate the R-squared value (non-adjusted) of the model.

    :param numpy.array y: dependent variable
    :param numpy.array fitted: values fitted by the model
    :param int n_params: number of parameters of the model
    :return float: adjusted R-squared value
    """
    y_mean = y.mean()
    # total sum of squares
    syy = ((y - y_mean) ** 2).sum()
    # residual sum of squares
    resid_ss = ((y - fitted) ** 2).sum()
    # regression sum of squares
    reg_ss = syy - resid_ss
    return reg_ss / syy


@log_errors
def compare_exponential_models(x, y):
    """
    Compare first- and second-order exponential models to fit the data
    and return results corresponding to the best model.

    The p-value is from testing if the second-order exponential is a better
    fit than the first-order exponential

    :param array-like x: independent variable data
    :param array-like y: dependent variable data
    :return: model name, optimal parameters, parameters standard error,
             fitted data, p-value
    """
    popt1, perr1, fitted1, rsq1 = fit_data(
        x,
        y,
        first_order_exponential,
        initial_parameters=INITIAL_PARAMS_FIRST_ORDER_DECAY,
        bounds=(-2, 2),
        method=METHOD,
    )
    popt2, perr2, fitted2, rsq2 = fit_data(
        x,
        y,
        second_order_exponential,
        initial_parameters=INITIAL_PARAMS_SECOND_ORDER_DECAY,
        bounds=PARAM_BOUNDS,
        method=METHOD,
        loss=LOSS,
        ftol=FTOL,
    )

    y_mean = y.mean()
    syy = ((y - y_mean) ** 2).sum()

    # ANOVA first-order exponential
    y_hat1 = np.array(first_order_exponential(x, *popt1))
    resid_ss1 = ((y - y_hat1) ** 2).sum()
    reg_ss1 = syy - resid_ss1
    total_ms1 = syy / (len(y) - 1)
    reg_ms1 = reg_ss1 / (len(popt1) - 1)
    resid_ms1 = resid_ss1 / (len(y) - len(popt1))

    # ANOVA second-order exponential
    y_hat2 = np.array(second_order_exponential(x, *popt2))
    resid_ss2 = ((y - y_hat2) ** 2).sum()
    reg_ss2 = syy - resid_ss2
    total_ms2 = syy / (len(y) - 1)
    reg_ms2 = reg_ss2 / (len(popt2) - 1)
    resid_ms2 = resid_ss2 / (len(y) - len(popt2))

    # test if second-order is better fit than first-order
    vr = (reg_ss2 - reg_ss1) / resid_ms2
    p_val = 1 - stats.f.cdf(vr, len(popt2) - 1, len(y) - len(popt2))

    if p_val < 0.05:
        return "second_exp", popt2, perr2, fitted2, rsq2
    else:
        return "first_exp", popt1, perr1, fitted1, rsq1


@log_errors
def print_params(label, name, popt, errors, rsq):
    """
    Displays model parameters on the console.

    :param str label: label to identify the data
    :param str name: name of the model
    :param tuple[float] popt: optimal parameters values from fitting
    :param tuple[float] errors: standard error of optimal parameters
    :param float r: adjusted R-square
    """
    params = get_model_info(name)["params"]
    print(f"{label}")
    print(f"{get_model_info(name)['equation']}")
    print("-" * 30)
    print("{0:10}{1:>10}{2:>10}".format("Parameter", "Value", "Std Err"))
    print("-" * 30)
    for i in range(len(params)):
        print(f"{params[i]:10}{popt[i]:+10.4f}{errors[i]:10.4f}")
    print("{0:10}{1:10.5f}".format("R-square", rsq))
    if name == "exp1":
        t = get_t_half(popt[1])
        print("{0:10}{1:10.2f}".format("t1 (sec)", t))
    if name == "exp2":
        t1 = get_t_half(popt[2])
        t2 = get_t_half(popt[3])
        print("{0:10}{1:10.2f}".format("t1 (sec)", t1))
        print("{0:10}{1:10.2f}".format("t2 (sec)", t2))
