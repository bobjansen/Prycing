"""Test the LSM code."""
import unittest
from hypothesis import given
from hypothesis.strategies import floats

from Prycing.options.lsm import simulate_and_price

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
