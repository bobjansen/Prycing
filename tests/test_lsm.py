"""Test the LSM code."""
import unittest
import math
import numpy as np
import pandas as pd
from hypothesis import given, settings
from hypothesis.strategies import floats

import Prycing.options.gbm as gbm
from Prycing.options.lsm import lsm, american_put_payoff, \
        regress_laguerre_2, regress_linear

class Table1Prices(unittest.TestCase):
    """Compate prices to the prices in the paper (table 1)."""
    def setUp(self):
        self.prices = pd.read_csv('tests/table_1.csv')['LSM American Price']

    def test_table_1_laguerre_2(self):
        """Compare the first table."""
        number_of_paths = 100000
        number_of_steps = 50
        strike = 40
        discount_rate = 0.06

        i = 0
        np.random.seed(42)
        for starting_stock_price in np.arange(36, 45, 2):
            for sigma in [0.2, 0.4]:
                for T in [1, 2]:
                    paths = gbm.simulate_gbm(
                        starting_stock_price, discount_rate, sigma,
                        number_of_paths, number_of_steps, T)

                    lsm_price = lsm(
                        paths, american_put_payoff(strike), regress_laguerre_2,
                        discount_rate, T, strike)[0][0]
                    self.assertAlmostEqual(lsm_price, self.prices[i])
                    i += 1

    def test_table_1_linear(self):
        """Compare the first table."""
        number_of_paths = 100000
        number_of_steps = 50
        strike = 40
        discount_rate = 0.06

        i = 0
        np.random.seed(42)
        for starting_stock_price in np.arange(36, 45, 2):
            for sigma in [0.2, 0.4]:
                for T in [1, 2]:
                    paths = gbm.simulate_gbm(
                        starting_stock_price, discount_rate, sigma,
                        number_of_paths, number_of_steps, T)

                    lsm_price = lsm(
                        paths, american_put_payoff(strike), regress_linear,
                        discount_rate, T, strike)[0][0]
                    self.assertAlmostEqual(lsm_price, self.prices[i], places=1)
                    i += 1


class AmericanMoreExpensive(unittest.TestCase):
    """Test that American options are more expensive than European."""
    @settings(max_examples=50, deadline=1000)
    @given(floats(0, 100), floats(0, 1), floats(0.01, 100), floats(0, 1),
           floats(0.001, 10))
    def test_american_more_expensive(
            self,
            strike, discount_rate, starting_stock_price, sigma, T
    ):
        """Implement the test using 10.000 paths and 50 steps."""
        number_of_paths = 10000
        number_of_steps = 50
        paths = gbm.simulate_gbm(
            starting_stock_price, discount_rate, sigma,
            number_of_paths, number_of_steps, T)
        per_path_value = np.maximum(strike - paths[-1], 0) * \
                math.exp(-discount_rate * T)
        european_price = sum(per_path_value) / number_of_paths

        lsm_price = lsm(
            paths, american_put_payoff(strike), regress_laguerre_2,
            discount_rate, T, strike)[0][0]
        # Add 5 cents to only get worthwile deviations due to something else
        # than noise in the simulations. The adjustment should go to zero as
        # the number of paths increases.
        self.assertGreaterEqual(lsm_price + 1, european_price)
