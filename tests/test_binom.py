"Test the binomial tree code."""
import unittest

from Prycing.options.binom import Option, binom_option

#pylint: disable-msg=attribute-defined-outside-init
class TestFairValue(unittest.TestCase):
    """Test fair values calculated using binomial tree."""
    def setUp(self):
        call_pay_off = lambda S, K: max(S - K, 0)
        put_pay_off = lambda S, K: max(K - S, 0)
        self.put_option1 = Option(36, 40, put_pay_off)
        self.call_option1 = Option(36, 40, call_pay_off)

    def test_put_fair_value(self):
        """Test fair value calculated for puts."""
        self.assertAlmostEqual(
            binom_option(self.put_option1, 0.06, 0, 0.2, 1, 500)[1].get_node(0, 0),
            3.844, places=2)
        self.assertAlmostEqual(
            binom_option(self.put_option1, 0.06, 0, 0.2, 2, 500)[1].get_node(0, 0),
            3.763, places=2)
        self.assertAlmostEqual(
            binom_option(self.put_option1, 0.06, 0, 0.4, 1, 500)[1].get_node(0, 0),
            6.711, places=2)
        self.assertAlmostEqual(
            binom_option(self.put_option1, 0.06, 0, 0.4, 2, 500)[1].get_node(0, 0),
            7.700, places=2)

    def test_call_fair_value(self):
        """Test fair value calculated for puts."""
        self.assertAlmostEqual(
            binom_option(self.call_option1, 0.06, 0, 0.2, 1, 500)[1].get_node(0, 0),
            2.174, places=2)
        self.assertAlmostEqual(
            binom_option(self.call_option1, 0.06, 0, 0.2, 2, 1000)[1].get_node(0, 0),
            4.286, places=2)
        self.assertAlmostEqual(
            binom_option(self.call_option1, 0.06, 0, 0.4, 1, 1000)[1].get_node(0, 0),
            5.041, places=2)
        self.assertAlmostEqual(
            binom_option(self.call_option1, 0.06, 0, 0.4, 2, 1000)[1].get_node(0, 0),
            8.223, places=2)
