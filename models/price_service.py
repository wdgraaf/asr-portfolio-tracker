"""Fetches current stock prices using the yfinance library."""

import yfinance as yf


def get_current_price(ticker):
    """Get the current price for a single ticker."""
    stock = yf.Ticker(ticker)
    data = stock.history(period="1d")
    if data.empty:
        return None
    return round(data["Close"].iloc[-1], 2)


def get_prices_for_portfolio(portfolio):
    """Get current prices for all tickers in the portfolio.

    Returns a dict like {"AAPL": 175.0, "MSFT": 400.0}
    """
    prices = {}
    for asset in portfolio:
        ticker = asset["ticker"]
        price = get_current_price(ticker)
        if price is not None:
            prices[ticker] = price
    return prices
