"""Stores the user's assets and does basic calculations like total value."""


# This will hold the portfolio as a simple list of dicts
# Example: [{"ticker": "AAPL", "shares": 10, "buy_price": 150.0}, ...]
portfolio = []


def add_asset(ticker, shares, buy_price):
    """Add a new asset to the portfolio."""
    asset = {
        "ticker": ticker.upper(),
        "shares": shares,
        "buy_price": buy_price,
    }
    portfolio.append(asset)
    return asset


def remove_asset(ticker):
    """Remove an asset by ticker name."""
    global portfolio
    portfolio = [a for a in portfolio if a["ticker"] != ticker.upper()]


def get_portfolio():
    """Return the current portfolio list."""
    return portfolio


def calculate_total_value(current_prices):
    """Calculate the total portfolio value using current prices.

    current_prices is a dict like {"AAPL": 175.0, "MSFT": 400.0}
    """
    total = 0.0
    for asset in portfolio:
        ticker = asset["ticker"]
        if ticker in current_prices:
            total += asset["shares"] * current_prices[ticker]
    return total


def calculate_profit_loss(current_prices):
    """Calculate profit/loss for each asset."""
    results = []
    for asset in portfolio:
        ticker = asset["ticker"]
        if ticker in current_prices:
            current_value = asset["shares"] * current_prices[ticker]
            cost = asset["shares"] * asset["buy_price"]
            profit = current_value - cost
            results.append({
                "ticker": ticker,
                "shares": asset["shares"],
                "buy_price": asset["buy_price"],
                "current_price": current_prices[ticker],
                "profit_loss": profit,
            })
    return results
