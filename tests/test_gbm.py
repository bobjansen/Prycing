"""Test the failure modes of the GBM code."""
import unittest

from Prycing.options.gbm import simulate_gbm

class TestGBMFailure(unittest.TestCase):
    """Test failure of simulate_gbm()."""
    def test_zero_time(self):
        """Test T = 0 gives an error."""
        self.assertRaises(
            ValueError,
            simulate_gbm, 5, 0.01, 0.2, 1000, 50, 0)

    def test_odd_paths(self):
        """Test T = 0 gives an error."""
        self.assertRaises(
            ValueError,
            simulate_gbm, 5, 0.01, 0.2, 1001, 50, 1)
