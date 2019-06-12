"""
Implement the LSM methods in different forms.

Based on "Valuing American Options by Simulation: A Simple Least Squares
Approach" by Francis A. Longstaff and Eduardo S. Schwartz.
"""

import math
import numpy as np
from scipy import stats
import statsmodels.api as sm

import bsm
import gbm

# Paths as in the first example.
EXAMPLE_PATHS = np.reshape(np.ravel(np.transpose(np.matrix(
        """1.00 1.09 1.08 1.34;
           1.00 1.16 1.26 1.54;
           1.00 1.22 1.07 1.03;
           1.00 0.93 0.97 0.92;
           1.00 1.11 1.56 1.52;
           1.00 0.76 0.77 0.90;
           1.00 0.92 0.84 1.01;
           1.00 0.88 1.22 1.34"""))), (4, 8))

def lsm(paths, payoff_fun, regress_fun, discount_rate, T, strike):
    """Implement the LSM method."""
    number_of_steps, number_of_paths = np.shape(paths)
    intrinsic_value = payoff_fun(paths)
    realized_cash_flows = intrinsic_value[-1, :]
    cash_flows = [realized_cash_flows]
    ols_fits = []

    # The algorithm steps backwards, the range here is forwards, all i's below
    # are negated.
    for i in range(2, number_of_steps):
        # Regression is to take place on those paths for which the option is
        # currently in the money. The article shows that this improves
        # efficiency.
        current_intrinsic_values = intrinsic_value[-i, :]
        in_money = current_intrinsic_values > 0

        early_cash_flows = np.zeros(number_of_paths)
        if np.any(in_money):
            ols_fit = regress_fun(
                paths[-i, in_money] / strike,
                realized_cash_flows[in_money] / strike)
            ols_fits.append(ols_fit)

            # For the in the money paths, find those for which immediate
            # exercise has higher value than continuing the option.
            early_exercise = ols_fit.fittedvalues * strike < \
                    current_intrinsic_values[in_money]
            improvements = np.where(in_money)[0][early_exercise]
            early_cash_flows[improvements] = \
                    current_intrinsic_values[improvements]
        else:
            ols_fits.append([])

        # Add the new set of cash flows, zero out cash flows if the option was
        # exercised and use the undiscounted expected cash flows for regression
        # in the next step.
        (cash_flows, realized_cash_flows) = \
                add_cash_flows(cash_flows, early_cash_flows)

    # The option value give the estimated stopping policy is just the expected
    # value of the discounted cash flows.
    value = npv(cash_flows, discount_rate / (number_of_steps / T))
    return (value, cash_flows, ols_fits)

# Used as a polynomial basis in the regression.
def l_0(x):
    """The first Laguerre polynomial."""
    return np.exp(-x/2)
def l_1(x):
    """The second Laguerre polynomial."""
    return np.exp(-x/2) * (1 - x)
def l_2(x):
    """The third Laguerre polynomial."""
    return np.exp(-x/2) * (1 - 2 * x + x ** 2 / 2)

def american_put_payoff(strike):
    """Calculate the intrinsic values per path for an American Put."""
    def payoff_fun(values):
        return np.maximum(strike - values, 0.0)
    return payoff_fun

def regress_laguerre_2(stock_prices, cash_flows):
    """Perform the LSM regression."""
    mat_x = np.column_stack((
                np.ones(len(stock_prices)),
                l_0(stock_prices),
                l_1(stock_prices),
                l_2(stock_prices)))
    return sm.OLS(cash_flows, mat_x).fit()

def regress_linear(stock_prices, cash_flows):
    """Perform the LSM regression."""
    mat_x = np.column_stack((
                np.ones(len(stock_prices)),
                stock_prices,
                np.square(stock_prices)))
    return sm.OLS(cash_flows, mat_x).fit()

def add_cash_flows(cash_flows, early_cash_flows):
    """Add cash flows for period to an existing set of cash flows."""
    realized_cash_flows = np.copy(early_cash_flows)
    is_stopped = early_cash_flows > 0.0

    output = [early_cash_flows]
    for vec in cash_flows:
        # Zero out cash flows made if the option was exercised earlier and
        # create the Y vector for the regression.
        vec[is_stopped] = 0.0
        realized_cash_flows += vec
        output.append(vec)

    return (output, realized_cash_flows)

def npv(cash_flow_matrix, discount_rate):
    """Calculate the NPV of a set of cash flows given a discount factor."""
    discounted_cash_flows = np.zeros(np.shape(cash_flow_matrix[0]))
    discount_step = math.exp(-discount_rate)
    discount_rate = discount_step
    for cash_flows in cash_flow_matrix:
        discounted_cash_flows += cash_flows * discount_rate
        discount_rate *= discount_step

    value = sum(discounted_cash_flows) / np.shape(cash_flow_matrix)[1]
    standard_error = stats.sem(discounted_cash_flows)
    return (value, standard_error)


def price_table(
        number_of_paths, number_of_steps,
        strike=40, discount_rate=0.06
):  #pragma: no cover
    """Create a table of prices as Table 1 in the Longstaff Schwartz paper."""
    np.random.seed(42)
    output = {}
    for starting_stock_price in np.arange(36, 45, 2):
        for sigma in [0.2, 0.4]:
            for T in [1, 2]:
                key = ' '.join([str(starting_stock_price),
                                str(sigma), str(T)])
                output[key] = {}
                paths = gbm.simulate_gbm(
                    starting_stock_price, discount_rate, sigma,
                    number_of_paths, number_of_steps, T)

                output[key]['European Price'] = bsm.BSMOption(
                    starting_stock_price, strike, T, sigma,
                    discount_rate, 0).fair_value()[1]

                per_path_value = np.maximum(strike - paths[-1], 0) * \
                        math.exp(-discount_rate * T)
                output[key]['Simulated European Price'] = \
                        sum(per_path_value) / number_of_paths
                output[key]['Simulated European SE'] = stats.sem(per_path_value)

                lsm_result = lsm(
                    paths, american_put_payoff(strike), regress_laguerre_2,
                    discount_rate, T, strike)[0]
                output[key]['LSM American Price'] = lsm_result[0]
                output[key]['LSM American SE'] = lsm_result[1]

    return output
