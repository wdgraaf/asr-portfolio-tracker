"""Runs a simple Monte Carlo simulation to estimate future portfolio value."""

import numpy as np
import yfinance as yf


TRADING_DAYS = 252
DEFAULT_MU = 0.07
DEFAULT_SIGMA = 0.20
MIN_RETURN_OBSERVATIONS = 30


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


def _estimate_params(ticker: str) -> tuple[float, float]:
    """Fetch 2 years of daily returns and return annualised (mu, sigma)."""
    try:
        data = yf.Ticker(ticker).history(period="2y")
        if data.empty or len(data) < MIN_RETURN_OBSERVATIONS + 1:
            return DEFAULT_MU, DEFAULT_SIGMA
        returns = data["Close"].pct_change().dropna().to_numpy()
        if len(returns) < MIN_RETURN_OBSERVATIONS:
            return DEFAULT_MU, DEFAULT_SIGMA
        mu = float(returns.mean()) * TRADING_DAYS
        sigma = float(returns.std(ddof=1)) * np.sqrt(TRADING_DAYS)
        return mu, sigma
    except Exception as e:
        print(f"Warning: could not estimate params for {ticker} ({e}), using defaults.")
        return DEFAULT_MU, DEFAULT_SIGMA


def run_simulation(
    assets: list[dict],
    current_prices: dict[str, float],
    years: int = 15,
    n_simulations: int = 100_000,
) -> dict:
    """Run a vectorised geometric Brownian motion simulation per asset.

    For each asset, pulls 2 years of daily returns from yfinance to estimate
    annualised drift and volatility, then draws n_simulations terminal values
    using S_T = S_0 * exp((mu - 0.5*sigma^2)*T + sigma*sqrt(T)*Z) and sums
    across assets to get portfolio totals.
    """
    priced_assets = [a for a in assets if a["ticker"] in current_prices]
    if not priced_assets:
        zeros = np.zeros(n_simulations)
        return {
            "final_values": zeros,
            "percentiles": {p: 0.0 for p in (5, 25, 50, 75, 95)},
            "mean": 0.0,
            "initial_value": 0.0,
        }

    T = float(years)
    sqrt_T = np.sqrt(T)
    totals = np.zeros(n_simulations)
    initial_value = 0.0

    for asset in priced_assets:
        ticker = asset["ticker"]
        s0 = asset["quantity"] * current_prices[ticker]
        initial_value += s0

        mu, sigma = _estimate_params(ticker)
        z = np.random.standard_normal(n_simulations)
        terminal = s0 * np.exp((mu - 0.5 * sigma**2) * T + sigma * sqrt_T * z)
        totals += terminal

    percentiles = {
        p: float(np.percentile(totals, p)) for p in (5, 25, 50, 75, 95)
    }

    return {
        "final_values": totals,
        "percentiles": percentiles,
        "mean": float(totals.mean()),
        "initial_value": initial_value,
    }
