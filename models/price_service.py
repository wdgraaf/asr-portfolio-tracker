"""Fetches current and historical stock prices using yfinance."""

import pandas as pd
import yfinance as yf


def get_current_prices(tickers: list[str]) -> dict[str, float]:
    """Fetch the latest close price for each ticker."""
    prices: dict[str, float] = {}
    try:
        for ticker in tickers:
            try:
                data = yf.Ticker(ticker).history(period="1d")
                if data.empty:
                    print(f"Warning: no data for {ticker}, skipping.")
                    continue
                prices[ticker] = round(float(data["Close"].iloc[-1]), 2)
            except Exception as e:
                print(f"Warning: could not fetch {ticker} ({e}), skipping.")
    except Exception as e:
        print(f"Error fetching current prices: {e}")
    return prices


def get_historical_prices(tickers: list[str], period: str = "1y") -> pd.DataFrame:
    """Return closing prices for each ticker over the given period."""
    try:
        data = yf.download(
            tickers, period=period, progress=False, auto_adjust=False
        )
        if data.empty:
            return pd.DataFrame()
        close = data["Close"] if "Close" in data.columns.get_level_values(0) else data
        if isinstance(close, pd.Series):
            close = close.to_frame(name=tickers[0])
        return close.dropna(how="all")
    except Exception as e:
        print(f"Error fetching historical prices: {e}")
        return pd.DataFrame()
