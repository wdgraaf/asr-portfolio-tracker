"""Main menu loop. Connects the models to the views."""

from models.portfolio import Portfolio
from models import price_service, simulation
from views import display


MENU = """
=== a.s.r. Portfolio Tracker ===
1. Add asset
2. Remove asset
3. View portfolio
4. View weights
5. Price history & chart
6. Run simulation
0. Exit
"""


def _prompt_float(label: str) -> float | None:
    raw = input(label).strip()
    try:
        return float(raw)
    except ValueError:
        print("Invalid input, try again")
        return None


def _add_asset(portfolio: Portfolio) -> None:
    ticker = input("Ticker (e.g. AAPL): ").strip()
    if not ticker:
        print("Invalid input, try again")
        return
    sector = input("Sector (e.g. Technology): ").strip()
    asset_class = input("Asset class (e.g. Equity): ").strip()
    quantity = _prompt_float("Quantity: ")
    if quantity is None:
        return
    purchase_price = _prompt_float("Purchase price per unit: ")
    if purchase_price is None:
        return
    portfolio.add_asset(ticker, sector, asset_class, quantity, purchase_price)
    print(f"Added {ticker.upper()}.")


def _remove_asset(portfolio: Portfolio) -> None:
    ticker = input("Ticker to remove: ").strip()
    if not ticker:
        print("Invalid input, try again")
        return
    portfolio.remove_asset(ticker)
    print(f"Removed {ticker.upper()}.")


def _view_portfolio(portfolio: Portfolio) -> None:
    assets = portfolio.get_assets()
    if not assets:
        print("Portfolio is empty.")
        return
    tickers = [a["ticker"] for a in assets]
    prices = price_service.get_current_prices(tickers)
    display.show_portfolio(assets, prices)


def _view_weights(portfolio: Portfolio) -> None:
    assets = portfolio.get_assets()
    if not assets:
        print("Portfolio is empty.")
        return

    print("\nGroup by:")
    print("  1. Asset")
    print("  2. Sector")
    print("  3. Asset class")
    sub = input("Pick an option: ").strip()

    field_map = {
        "1": ("ticker", "Weights by Asset"),
        "2": ("sector", "Weights by Sector"),
        "3": ("asset_class", "Weights by Asset Class"),
    }
    if sub not in field_map:
        print("Invalid input, try again")
        return

    field, title = field_map[sub]
    tickers = [a["ticker"] for a in assets]
    prices = price_service.get_current_prices(tickers)
    weights = portfolio.get_weights_by(field, prices)
    if not weights:
        print("No priced assets to show weights for.")
        return
    display.show_weights(weights, title)


def _price_history() -> None:
    raw = input("Tickers (comma-separated, e.g. AAPL,MSFT): ").strip()
    tickers = [t.strip().upper() for t in raw.split(",") if t.strip()]
    if not tickers:
        print("Invalid input, try again")
        return
    period = input("Period (e.g. 1mo, 6mo, 1y, 5y) [1y]: ").strip() or "1y"
    df = price_service.get_historical_prices(tickers, period=period)
    if df.empty:
        print("No price data returned.")
        return
    display.plot_prices(df, tickers)


def _run_simulation(portfolio: Portfolio) -> None:
    assets = portfolio.get_assets()
    if not assets:
        print("Portfolio is empty. Add assets first.")
        return
    tickers = [a["ticker"] for a in assets]
    prices = price_service.get_current_prices(tickers)
    print("Running simulation...")
    results = simulation.run_simulation(assets, prices)
    display.plot_simulation(results)


def run() -> None:
    """Main loop that keeps the program running until the user quits."""
    portfolio = Portfolio()
    actions = {
        "1": lambda: _add_asset(portfolio),
        "2": lambda: _remove_asset(portfolio),
        "3": lambda: _view_portfolio(portfolio),
        "4": lambda: _view_weights(portfolio),
        "5": _price_history,
        "6": lambda: _run_simulation(portfolio),
    }

    while True:
        print(MENU)
        try:
            choice = input("Pick an option: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break

        if choice == "0":
            print("Bye!")
            break

        action = actions.get(choice)
        if action is None:
            print("Invalid input, try again")
            continue

        try:
            action()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        except Exception as e:
            print(f"Something went wrong ({e}), try again")
