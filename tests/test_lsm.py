"""Test the LSM code."""
import unittest
import numpy as np
import pandas as pd
from hypothesis import given
from hypothesis.strategies import floats

import Prycing.options.gbm as gbm
from Prycing.options.lsm import simulate_and_price, lsm, american_put_payoff, \
        regress_laguerre_2

class Table1Prices(unittest.TestCase):
    """Compate prices to the prices in the paper (table 1)."""
    def setUp(self):
        self.prices = pd.read_csv('tests/table_1.csv')['LSM American Price']

    def test_table_1(self):
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
                    i = i + 1


class AmericanMoreExpensive(unittest.TestCase):
    """Test that American options are more expensive than European."""
    @given(floats(0, 100), floats(0, 1), floats(0, 100), floats(0, 1),
           floats(0.001, 10))
    def test_american_more_expensive(
            self,
            strike, discount_rate, starting_stock_price, sigma, T
    ):
        """Implement the test using 1000 paths and 25 steps."""
        prices = simulate_and_price(
            1000, 25,
            strike, discount_rate, starting_stock_price, sigma, T)
        # Add a cent to only get worthwile deviations due to something else
        # than noise in the simulations.
        self.assertGreaterEqual(prices[1] + 0.01, prices[0])
