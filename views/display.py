"""Handles all the printing and chart display using rich and matplotlib."""

from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt
import numpy as np

console = Console()


def show_portfolio(assets, current_prices):
    """Print the portfolio with per-asset metrics and a total row."""
    table = Table(title="Your Portfolio")
    table.add_column("Ticker", style="cyan")
    table.add_column("Sector")
    table.add_column("Asset Class")
    table.add_column("Qty", justify="right")
    table.add_column("Buy Price", justify="right")
    table.add_column("Transaction Value", justify="right")
    table.add_column("Current Price", justify="right")
    table.add_column("Current Value", justify="right")
    table.add_column("P&L", justify="right")
    table.add_column("P&L %", justify="right")

    total_txn = 0.0
    total_current = 0.0

    for asset in assets:
        ticker = asset["ticker"]
        qty = asset["quantity"]
        buy_price = asset["purchase_price"]
        txn_value = qty * buy_price

        if ticker not in current_prices:
            table.add_row(
                ticker,
                asset["sector"],
                asset["asset_class"],
                f"{qty:g}",
                f"${buy_price:.2f}",
                f"${txn_value:,.2f}",
                "[dim]n/a[/dim]",
                "[dim]n/a[/dim]",
                "[dim]n/a[/dim]",
                "[dim]n/a[/dim]",
            )
            continue

        current_price = current_prices[ticker]
        current_value = qty * current_price
        pl = current_value - txn_value
        pl_pct = (pl / txn_value) * 100 if txn_value else 0.0
        pl_style = "green" if pl >= 0 else "red"

        total_txn += txn_value
        total_current += current_value

        table.add_row(
            ticker,
            asset["sector"],
            asset["asset_class"],
            f"{qty:g}",
            f"${buy_price:.2f}",
            f"${txn_value:,.2f}",
            f"${current_price:.2f}",
            f"${current_value:,.2f}",
            f"[{pl_style}]${pl:,.2f}[/{pl_style}]",
            f"[{pl_style}]{pl_pct:+.2f}%[/{pl_style}]",
        )

    total_pl = total_current - total_txn
    total_pl_pct = (total_pl / total_txn) * 100 if total_txn else 0.0
    total_style = "green" if total_pl >= 0 else "red"

    table.add_section()
    table.add_row(
        "[bold]TOTAL[/bold]",
        "",
        "",
        "",
        "",
        f"[bold]${total_txn:,.2f}[/bold]",
        "",
        f"[bold]${total_current:,.2f}[/bold]",
        f"[bold {total_style}]${total_pl:,.2f}[/bold {total_style}]",
        f"[bold {total_style}]{total_pl_pct:+.2f}%[/bold {total_style}]",
    )

    console.print(table)


def show_weights(weights_dict, title):
    """Print a Name | Weight (%) table for any grouping."""
    table = Table(title=title)
    table.add_column("Name", style="cyan")
    table.add_column("Weight (%)", justify="right")

    for name, weight in sorted(weights_dict.items(), key=lambda x: -x[1]):
        table.add_row(name, f"{weight:.2f}%")

    console.print(table)


def plot_prices(df, tickers):
    """Line chart of historical closing prices, one line per ticker."""
    for ticker in tickers:
        if ticker in df.columns:
            plt.plot(df.index, df[ticker], label=ticker)

    plt.title("Historical Closing Prices")
    plt.xlabel("Date")
    plt.ylabel("Price ($)")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()


def plot_simulation(results):
    """Histogram of Monte Carlo final values with percentile markers."""
    final_values = results["final_values"]
    percentiles = results["percentiles"]

    bins = np.logspace(np.log10(final_values.min()), np.log10(final_values.max()), 100)
    plt.hist(final_values, bins=bins, color="skyblue", edgecolor="black", alpha=0.75)

    for p, color in [(5, "red"), (50, "black"), (95, "green")]:
        value = percentiles[p]
        plt.axvline(value, color=color, linestyle="--", linewidth=1.5,
                    label=f"{p}th percentile: ${value:,.0f}")

    plt.title("Monte Carlo Simulation: 15 Year Projection")
    plt.xlabel("Portfolio Value ($)")
    plt.ylabel("Frequency")
    plt.legend()
    plt.xscale("log")
    plt.show()
