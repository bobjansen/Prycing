"""
Functionality to capture the Black-Scholes-Merton model

Formula's from: https://en.wikipedia.org/wiki/Greeks_(finance)
"""


import math
from dataclasses import dataclass
from enum import IntEnum
from scipy.stats import norm
import scipy.optimize as spOpt


class OptionSide(IntEnum):
    """The side of an option, either call or put."""
    Call = 0
    Put = 1


def find_implied_vol(
        price: float,
        side: OptionSide,
        spot: float,
        strike: float,
        tau: float,
        discount_rate: float,
        dividend_yield: float
):
    """Find the implied vol from price and parameters."""
    def price_from_vol(sigma):
        opt = BSMOption(spot, strike, tau, sigma,
                        discount_rate, dividend_yield)
        return opt.fair_value()[side] - price

    if price_from_vol(0) > 0:
        raise ValueError('Assuming 0 volatility gives price higher than given.')
    # The default method 'brentq' should suffice for this purpose.
    return spOpt.root_scalar(price_from_vol, bracket=(0, 2))


@dataclass(frozen=True)
class BSMOption():
    """
    An option under the Black-Scholes-Merton (BSM) model.

    Sigma, discount_rate and dividend_yield are expressed as fraction, tau is
    in years.
    """
    spot: float
    strike: float
    tau: float
    sigma: float
    discount_rate: float
    dividend_yield: float

    def fair_value(self):
        """Calculates the fair value under the BSM-model."""
        # If the volatility is zero, the option price is equal to its intrinsic
        # value at maturity.
        if self.sigma == 0:
            discounted_stock = self._dividend_discount() * self.spot
            discounted_strike = self._discount() * self.strike
            intrinsic_value = discounted_stock - discounted_strike
            return(max(intrinsic_value, 0), max(-intrinsic_value, 0))
        return (self.spot * self._call_delta() - \
                     self._discount() * self.strike * norm.cdf(self._d2()),
                self._discount() * self.strike * norm.cdf(-self._d2()) - \
                     self.spot * -self._put_delta())

    def delta(self):
        """Calculates the delta under the BSM-model."""
        return (self._call_delta(), self._put_delta())

    def vega(self):
        """Calculates the vega under the BSM-model."""
        return self.spot * self._dividend_discount() * norm.pdf(self._d1()) * \
                self.tau

    def _call_delta(self):
        return self._dividend_discount() * norm.cdf(self._d1())

    def _put_delta(self):
        return -self._dividend_discount() * norm.cdf(-self._d1())

    def _d1(self):
        numerator = self._log_moneyness() + self._q_drift() * self.tau
        return numerator / self._scaled_vol()

    def _d2(self):
        return self._d1() - self._scaled_vol()

    def _q_drift(self):
        return self.discount_rate - self.dividend_yield + self.sigma ** 2 / 2

    def _scaled_vol(self):
        return self.sigma * math.sqrt(self.tau)

    def _log_moneyness(self):
        return math.log(self.spot / self.strike)

    def _dividend_discount(self):
        return math.exp(-self.dividend_yield * self.tau)

    def _discount(self):
        return math.exp(-self.discount_rate * self.tau)
