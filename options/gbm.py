"""Simulate Geometric Brownian Motion."""
import numpy as np

def simulate_gbm(start_value, mu, sigma, number_of_paths, number_of_steps, T):
    """Simulate number_of_paths GBM's"""
    if T <= 0:
        raise ValueError('T must be positive.')
    if number_of_paths % 2 == 1:
        raise ValueError('Number of paths needs to be even.')
    dt = T / number_of_steps
    sqrt_dt = np.sqrt(dt)
    drift = (mu - 0.5 * sigma ** 2) * dt

    output = [np.full(number_of_paths, start_value)]
    for i in range(1, number_of_steps + 1):
        # Create random standard normals antithetically.
        normals = np.random.standard_normal(number_of_paths // 2)
        normals = np.concatenate((normals, -normals))

        output.append(output[i - 1] * \
                np.exp(drift + sigma * sqrt_dt * normals))

    return np.array(output)
