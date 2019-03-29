"""Option calculations using binomial stock_trees."""
from collections import namedtuple
import math
import utils

Option = namedtuple('Option', ['S', 'K', 'price_fun'])

#pylint: disable-msg=too-many-arguments
def binom_option(option, r, q, sigma, N, steps):
    """Calculate the value of an European option."""
    dt = N / steps
    u = math.exp(sigma * math.sqrt(dt))
    d = 1 / u

    cc_rate = math.exp(r * dt) # Continuously compounded rate.
    u_minus_d = u - d
    q_u = (math.exp((r - q) * dt) - d) / u_minus_d
    q_d = 1 - q_u
    print("u: {}, d: {}".format(u, d))
    print("q_u: {}, q_d: {}, exp((r - q) * dt): {}".format(q_u, q_d, cc_rate))

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

    #for i in range(steps - 1, -1, -1):
    #    for j in range(1, i):
    #        phi_u = portfolio_tree.get_node(i + 1, j - 1)
    #        phi_d = portfolio_tree.get_node(i + 1, j)
    #        x = (discount_factor_per_level * u * phi_d - d * phi_u) / u_minus_d
    #        y = ((1 / stock_tree.get_node(i, j)) * phi_u - phi_d) / u_minus_d
