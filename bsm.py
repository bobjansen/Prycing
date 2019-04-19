"""
Functionality to capture the Black-Scholes-Merton model

Formula's from:
https://en.wikipedia.org/wiki/Greeks_(finance)#First-order_Greeks
"""


import math
from enum import IntEnum
from scipy.stats import norm
import scipy.optimize as spOpt


class OptionSide(IntEnum):
    """The side of an option, either call or put."""
    Call = 0
    Put = 1


def find_implied_vol(price, side, S, K, tau, r, q):
    """Find the implied vol from price and parameters."""
    def price_from_vol(sigma):
        opt = BSMOption(S, K, tau, sigma, r, q)
        return opt.fair_value()[side] - price

    if price_from_vol(0) > 0:
        raise ValueError('Assuming 0 volatility gives price higher than given.')
    # The default method 'brentq' should suffice for this purpose.
    return spOpt.root_scalar(price_from_vol, bracket=(0, 2))


class BSMOption():
    """
    An option under the Black-Scholes-Merton (BSM) model.
    """
    def __init__(self, S_, K_, tau_, sigma_, r_, q_):
        self.S = S_
        self.K = K_
        self.tau = tau_
        self.sigma = sigma_
        self.r = r_
        self.q = q_

    def fair_value(self):
        """Calculates the fair value under the BSM-model."""
        # If the volatility is zero, the option price is equal to its intrinsic
        # value.
        if self.sigma == 0:
            return(max(self.S - self.K, 0), max(self.K - self.S, 0))
        return (self.S * self._call_delta() - \
                     self._discount() * self.K * norm.cdf(self._d2()),
                self._discount() * self.K * norm.cdf(-self._d2()) - \
                     self.S * self._dividend_discount() * norm.cdf(-self._d1()))

    def delta(self):
        """Calculates the delta under the BSM-model."""
        return (self._call_delta(), self._put_delta())

    def vega(self):
        """Calculates the vega under the BSM-model."""
        return self.S * self._dividend_discount() * norm.pdf(self._d1()) * \
                self.tau

    def _call_delta(self):
        return self._dividend_discount() * norm.cdf(self._d1())

    def _put_delta(self):
        return -self._dividend_discount() * norm.cdf(-self._d1())

    def _d1(self):
        numerator = self._log_monenyness() + self._q_drift() * self.tau
        return numerator / self._scaled_vol()

    def _d2(self):
        return self._d1() - self._scaled_vol()

    def _q_drift(self):
        return self.r - self.q + self.sigma ** 2 / 2

    def _scaled_vol(self):
        return self.sigma * math.sqrt(self.tau)

    def _log_monenyness(self):
        return math.log(self.S / self.K)

    def _dividend_discount(self):
        return math.exp(-self.q * self.tau)

    def _discount(self):
        return math.exp(-self.r * self.tau)
