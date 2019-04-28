"""Option calculations using binomial stock_trees."""
from collections import namedtuple
import math
import utils

Option = namedtuple('Option', ['S', 'K', 'price_fun'])

def binom_option(
        option: Option,
        discount_rate: float,
        dividend_yield: float,
        sigma: float,
        N: int,
        steps: int
):
    """Calculate the value of an European option."""
    dt = N / steps
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u

    cc_rate = math.exp(discount_rate * dt) # Continuously compounded rate.
    u_minus_d = u - d
    q_u = (math.exp((discount_rate - dividend_yield) * dt) - d) / u_minus_d
    q_d = 1 - q_u
    print("u: {}, d: {}".format(u, d))
    print("q_u: {}, q_d: {}".format(q_u, q_d))
    print("exp((discount_rate - dividend_yield) * dt): {}".format(cc_rate))

    stock_tree = utils.Tree(steps)
    stock_tree.set_node(0, 0, option.S)
    for i in range(1, steps):
        stock_tree.set_node(i, 0, stock_tree.get_node(i - 1, 0) * u)
        for j in range(1, i + 1):
            stock_tree.set_node(i, j, stock_tree.get_node(i - 1, j - 1) * d)
    last_level = stock_tree.get_level(steps)

    value_tree = utils.Tree(steps)
    for i in range(0, len(last_level)):
        value_tree.set_node(
            steps - 1, i,
            option.price_fun(stock_tree.get_node(steps - 1, i), option.K))

    for i in range(steps - 2, -1, -1):
        for j in range(1, i + 2):
            v_t = (1 / cc_rate) * (
                q_u * value_tree.get_node(i + 1, j - 1) +
                q_d * value_tree.get_node(i + 1, j))
            value_tree.set_node(i, j - 1, v_t)

    return (stock_tree, value_tree)
