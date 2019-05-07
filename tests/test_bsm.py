"""Test the BSM code."""
import unittest
from hypothesis import given
from hypothesis.strategies import floats

from Prycing.options.bsm import BSMOption, find_implied_vol, OptionSide

class TestPutCallEquality(unittest.TestCase):
    """Test that C(S, K) == P(K, S) if rates are zero."""
    @given(floats(0, 10), floats(0, 10), floats(0, 10), floats(0, 10))
    def test_put_call_equality(
            self,
            spot,
            strike,
            time_to_maturity,
            sigma
        ):
        """Implement the test using hypothesis."""
        option1 = BSMOption(spot, strike, time_to_maturity, sigma, 0, 0)
        option2 = BSMOption(strike, spot, time_to_maturity, sigma, 0, 0)
        fair_value1 = option1.fair_value()
        fair_value2 = option2.fair_value()
        self.assertAlmostEqual(fair_value1[0], fair_value2[1])
        self.assertAlmostEqual(fair_value1[1], fair_value2[0])

#pylint: disable-msg=attribute-defined-outside-init
#pylint: disable-msg=too-many-instance-attributes
class TestFairValue(unittest.TestCase):
    """Test the pricing functionality of the BSM module."""
    def setUp(self):
        """Setup the test class."""
        self.option1 = BSMOption(36, 40, 1, 0.2, 0.06, 0)
        self.option2 = BSMOption(36, 40, 2, 0.2, 0.06, 0)
        self.option3 = BSMOption(36, 40, 1, 0.4, 0.06, 0)
        self.option4 = BSMOption(36, 40, 2, 0.4, 0.06, 0)

        self.option5 = BSMOption(38, 40, 1, 0.2, 0.06, 0)
        self.option6 = BSMOption(38, 40, 2, 0.2, 0.06, 0)
        self.option7 = BSMOption(38, 40, 1, 0.4, 0.06, 0)
        self.option8 = BSMOption(38, 40, 2, 0.4, 0.06, 0)

        self.option9 = BSMOption(40, 40, 1, 0.2, 0.06, 0)
        self.option10 = BSMOption(40, 40, 2, 0.2, 0.06, 0)
        self.option11 = BSMOption(40, 40, 1, 0.4, 0.06, 0)
        self.option12 = BSMOption(40, 40, 2, 0.4, 0.06, 0)

        self.option13 = BSMOption(42, 40, 1, 0.2, 0.06, 0)
        self.option14 = BSMOption(42, 40, 2, 0.2, 0.06, 0)
        self.option15 = BSMOption(42, 40, 1, 0.4, 0.06, 0)
        self.option16 = BSMOption(42, 40, 2, 0.4, 0.06, 0)

        self.option17 = BSMOption(44, 40, 1, 0.2, 0.06, 0)
        self.option18 = BSMOption(44, 40, 2, 0.2, 0.06, 0)
        self.option19 = BSMOption(44, 40, 1, 0.4, 0.06, 0)
        self.option20 = BSMOption(44, 40, 2, 0.4, 0.06, 0)

    def test_put_fair_value(self):
        """Test the fair values of puts. Values taken from LSM paper."""
        self.assertAlmostEqual(self.option1.fair_value()[1], 3.844, places=3)
        self.assertAlmostEqual(self.option2.fair_value()[1], 3.763, places=3)
        self.assertAlmostEqual(self.option3.fair_value()[1], 6.711, places=3)
        self.assertAlmostEqual(self.option4.fair_value()[1], 7.700, places=3)

        self.assertAlmostEqual(self.option5.fair_value()[1], 2.852, places=3)
        self.assertAlmostEqual(self.option6.fair_value()[1], 2.991, places=3)
        self.assertAlmostEqual(self.option7.fair_value()[1], 5.834, places=3)
        self.assertAlmostEqual(self.option8.fair_value()[1], 6.979, places=3)

        self.assertAlmostEqual(self.option9.fair_value()[1], 2.066, places=3)
        self.assertAlmostEqual(self.option10.fair_value()[1], 2.356, places=3)
        self.assertAlmostEqual(self.option11.fair_value()[1], 5.060, places=3)
        self.assertAlmostEqual(self.option12.fair_value()[1], 6.326, places=3)

        self.assertAlmostEqual(self.option13.fair_value()[1], 1.465, places=3)
        self.assertAlmostEqual(self.option14.fair_value()[1], 1.841, places=3)
        self.assertAlmostEqual(self.option15.fair_value()[1], 4.379, places=3)
        self.assertAlmostEqual(self.option16.fair_value()[1], 5.736, places=3)

        self.assertAlmostEqual(self.option17.fair_value()[1], 1.017, places=3)
        self.assertAlmostEqual(self.option18.fair_value()[1], 1.429, places=3)
        self.assertAlmostEqual(self.option19.fair_value()[1], 3.783, places=3)
        self.assertAlmostEqual(self.option20.fair_value()[1], 5.202, places=3)

    def test_call_fair_value(self):
        """Test the fair values of puts. Values taken from my implementation."""
        self.assertAlmostEqual(self.option1.fair_value()[0], 2.174, places=3)
        self.assertAlmostEqual(self.option2.fair_value()[0], 4.286, places=3)
        self.assertAlmostEqual(self.option3.fair_value()[0], 5.041, places=3)
        self.assertAlmostEqual(self.option4.fair_value()[0], 8.223, places=3)

        self.assertAlmostEqual(self.option5.fair_value()[0], 3.181, places=3)
        self.assertAlmostEqual(self.option6.fair_value()[0], 5.514, places=3)
        self.assertAlmostEqual(self.option7.fair_value()[0], 6.164, places=3)
        self.assertAlmostEqual(self.option8.fair_value()[0], 9.502, places=3)

        self.assertAlmostEqual(self.option9.fair_value()[0], 4.396, places=3)
        self.assertAlmostEqual(self.option10.fair_value()[0], 6.879, places=3)
        self.assertAlmostEqual(self.option11.fair_value()[0], 7.389, places=3)
        self.assertAlmostEqual(self.option12.fair_value()[0], 10.849, places=3)

        self.assertAlmostEqual(self.option13.fair_value()[0], 5.794, places=3)
        self.assertAlmostEqual(self.option14.fair_value()[0], 8.365, places=3)
        self.assertAlmostEqual(self.option15.fair_value()[0], 8.708, places=3)
        self.assertAlmostEqual(self.option16.fair_value()[0], 12.259, places=3)

        self.assertAlmostEqual(self.option17.fair_value()[0], 7.346, places=3)
        self.assertAlmostEqual(self.option18.fair_value()[0], 9.952, places=3)
        self.assertAlmostEqual(self.option19.fair_value()[0], 10.112, places=3)
        self.assertAlmostEqual(self.option20.fair_value()[0], 13.725, places=3)

class TestFindImpiedVol(unittest.TestCase):
    """Test the implied volatility finder."""
    def test_find_implied_vol(self):
        """Setup the test class."""
        self.assertAlmostEqual(
            find_implied_vol(2.174, OptionSide.Call, 36, 40, 1, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(4.286, OptionSide.Call, 36, 40, 2, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(5.041, OptionSide.Call, 36, 40, 1, 0.06, 0).root,
            0.4, places=4)
        self.assertAlmostEqual(
            find_implied_vol(8.223, OptionSide.Call, 36, 40, 2, 0.06, 0).root,
            0.4, places=4)

        self.assertAlmostEqual(
            find_implied_vol(3.181, OptionSide.Call, 38, 40, 1, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(5.514, OptionSide.Call, 38, 40, 2, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(6.164, OptionSide.Call, 38, 40, 1, 0.06, 0).root,
            0.4, places=4)
        self.assertAlmostEqual(
            find_implied_vol(9.502, OptionSide.Call, 38, 40, 2, 0.06, 0).root,
            0.4, places=4)

        self.assertAlmostEqual(
            find_implied_vol(4.396, OptionSide.Call, 40, 40, 1, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(6.879, OptionSide.Call, 40, 40, 2, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(7.389, OptionSide.Call, 40, 40, 1, 0.06, 0).root,
            0.4, places=4)
        self.assertAlmostEqual(
            find_implied_vol(10.849, OptionSide.Call, 40, 40, 2, 0.06, 0).root,
            0.4, places=4)

        self.assertAlmostEqual(
            find_implied_vol(5.794, OptionSide.Call, 42, 40, 1, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(8.365, OptionSide.Call, 42, 40, 2, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(8.708, OptionSide.Call, 42, 40, 1, 0.06, 0).root,
            0.4, places=4)
        self.assertAlmostEqual(
            find_implied_vol(12.259, OptionSide.Call, 42, 40, 2, 0.06, 0).root,
            0.4, places=4)

        self.assertAlmostEqual(
            find_implied_vol(7.346, OptionSide.Call, 44, 40, 1, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(9.952, OptionSide.Call, 44, 40, 2, 0.06, 0).root,
            0.2, places=4)
        self.assertAlmostEqual(
            find_implied_vol(10.112, OptionSide.Call, 44, 40, 1, 0.06, 0).root,
            0.4, places=4)
        self.assertAlmostEqual(
            find_implied_vol(13.725, OptionSide.Call, 44, 40, 2, 0.06, 0).root,
            0.4, places=4)
