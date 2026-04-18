"""Main menu loop. Connects the models to the views."""

from models import portfolio, price_service, simulation
from views import display


def show_menu():
    """Print the menu options."""
    print("\n=== Portfolio Tracker ===")
    print("1. Add asset")
    print("2. Remove asset")
    print("3. View portfolio")
    print("4. Run Monte Carlo simulation")
    print("5. Exit")
    print("========================")


def run():
    """Main loop that keeps the program running until the user quits."""
    display.show_message("[bold]Welcome to the Portfolio Tracker![/bold]")

    while True:
        show_menu()
        choice = input("Pick an option: ").strip()

        if choice == "1":
            ticker = input("Ticker (e.g. AAPL): ").strip()
            shares = float(input("Number of shares: "))
            buy_price = float(input("Buy price per share: "))
            portfolio.add_asset(ticker, shares, buy_price)
            display.show_message(f"[green]Added {ticker.upper()}![/green]")

        elif choice == "2":
            ticker = input("Ticker to remove: ").strip()
            portfolio.remove_asset(ticker)
            display.show_message(f"[yellow]Removed {ticker.upper()}.[/yellow]")

        elif choice == "3":
            assets = portfolio.get_portfolio()
            if not assets:
                display.show_message("[yellow]Portfolio is empty.[/yellow]")
                continue
            prices = price_service.get_prices_for_portfolio(assets)
            pl_data = portfolio.calculate_profit_loss(prices)
            display.show_portfolio_table(pl_data)
            total = portfolio.calculate_total_value(prices)
            display.show_total_value(total)

        elif choice == "4":
            assets = portfolio.get_portfolio()
            if not assets:
                display.show_message("[yellow]Portfolio is empty. Add assets first.[/yellow]")
                continue
            prices = price_service.get_prices_for_portfolio(assets)
            total = portfolio.calculate_total_value(prices)
            display.show_message("Running simulation...")
            results = simulation.run_monte_carlo(total)
            display.show_simulation_chart(results)

        elif choice == "5":
            display.show_message("[bold]Bye![/bold]")
            break

        else:
            display.show_message("[red]Invalid option, try again.[/red]")
