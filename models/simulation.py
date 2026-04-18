"""Runs a simple Monte Carlo simulation to estimate future portfolio value."""

import numpy as np


def run_monte_carlo(current_value, days=252, simulations=1000, mean_return=0.0005, std_dev=0.02):
    """Run a basic Monte Carlo simulation.

    Parameters:
        current_value: starting portfolio value
        days: how many trading days to simulate (252 = 1 year)
        simulations: how many times to run it
        mean_return: average daily return
        std_dev: daily standard deviation

    Returns a list of final values (one per simulation).
    """
    results = []
    for i in range(simulations):
        value = current_value
        for day in range(days):
            daily_change = np.random.normal(mean_return, std_dev)
            value = value * (1 + daily_change)
        results.append(value)
    return results
