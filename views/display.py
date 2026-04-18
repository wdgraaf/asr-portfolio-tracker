"""Handles all the printing and chart display using rich and matplotlib."""

from rich.console import Console
from rich.table import Table
import matplotlib.pyplot as plt

console = Console()


def show_portfolio_table(profit_loss_data):
    """Print the portfolio as a nice table."""
    table = Table(title="Your Portfolio")

    table.add_column("Ticker", style="cyan")
    table.add_column("Shares", justify="right")
    table.add_column("Buy Price", justify="right")
    table.add_column("Current Price", justify="right")
    table.add_column("Profit/Loss", justify="right")

    for row in profit_loss_data:
        pl = row["profit_loss"]
        pl_style = "green" if pl >= 0 else "red"
        table.add_row(
            row["ticker"],
            str(row["shares"]),
            f"${row['buy_price']:.2f}",
            f"${row['current_price']:.2f}",
            f"[{pl_style}]${pl:.2f}[/{pl_style}]",
        )

    console.print(table)


def show_total_value(total):
    """Print the total portfolio value."""
    console.print(f"\nTotal portfolio value: [bold green]${total:.2f}[/bold green]\n")


def show_simulation_chart(results):
    """Show a histogram of Monte Carlo simulation results."""
    plt.hist(results, bins=50, color="skyblue", edgecolor="black")
    plt.title("Monte Carlo Simulation - Future Portfolio Value")
    plt.xlabel("Portfolio Value ($)")
    plt.ylabel("Frequency")
    plt.show()


def show_message(text):
    """Print a simple message."""
    console.print(text)
