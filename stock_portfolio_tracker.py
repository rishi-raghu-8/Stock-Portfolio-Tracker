"""
CodeAlpha Internship - Task 2: Stock Portfolio Tracker
Author: Rishi R 
Description:
A menu-driven stock portfolio tracker using manually defined stock prices.
No external packages or live market API are required.
"""

import csv
import json
import os
from datetime import datetime

APP_NAME = "CODEALPHA STOCK PORTFOLIO TRACKER"
VERSION = "1.0.0"
DATA_FILE = "portfolio_data.json"
CSV_FILE = "portfolio_report.csv"
TXT_FILE = "portfolio_report.txt"

# Manually defined sample prices (USD). Update these values when required.
STOCK_PRICES = {
    "AAPL": 180.00,
    "TSLA": 250.00,
    "GOOGL": 140.00,
    "MSFT": 420.00,
    "AMZN": 175.00,
    "NVDA": 120.00,
    "META": 500.00,
    "NFLX": 610.00,
    "ORCL": 125.00,
    "IBM": 190.00,
    "INTC": 32.00,
    "AMD": 155.00,
    "DIS": 100.00,
    "KO": 62.00,
    "PEP": 170.00,
    "UBER": 75.00,
    "PYPL": 65.00,
    "ADBE": 520.00,
    "CRM": 270.00,
    "COST": 850.00,
}


def line(char="=", width=76):
    print(char * width)


def heading(title):
    print()
    line()
    print(title.center(76))
    line()


def money(value):
    return f"${value:,.2f}"


def pause():
    input("\nPress Enter to continue...")


def get_positive_number(prompt, allow_zero=False):
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
            if value < 0 or (value == 0 and not allow_zero):
                print("Please enter a valid positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Enter a number, for example 10 or 10.5.")


def get_stock_symbol():
    while True:
        symbol = input("Enter stock symbol: ").strip().upper()
        if not symbol:
            print("Stock symbol cannot be empty.")
        elif symbol not in STOCK_PRICES:
            print("Symbol not found in the manually maintained price list.")
            print("Use option 2 to view available stocks.")
        else:
            return symbol


def show_available_stocks():
    heading("AVAILABLE STOCKS AND MANUALLY DEFINED PRICES")
    print(f"{'SYMBOL':<14}{'PRICE':>20}")
    line("-")
    for symbol, price in sorted(STOCK_PRICES.items()):
        print(f"{symbol:<14}{money(price):>20}")
    line("-")
    print("Note: These are sample hardcoded prices, not live market prices.")


def calculate_position(position):
    quantity = position["quantity"]
    current_price = STOCK_PRICES[position["symbol"]]
    purchase_price = position["purchase_price"]
    invested = quantity * purchase_price
    current_value = quantity * current_price
    profit_loss = current_value - invested
    return invested, current_value, profit_loss


def load_portfolio():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
        if not isinstance(data, list):
            raise ValueError("Portfolio data must be a list.")
        valid = []
        for item in data:
            symbol = str(item["symbol"]).upper()
            quantity = float(item["quantity"])
            purchase_price = float(item["purchase_price"])
            if symbol in STOCK_PRICES and quantity > 0 and purchase_price > 0:
                valid.append({
                    "symbol": symbol,
                    "quantity": quantity,
                    "purchase_price": purchase_price,
                })
        return valid
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError) as error:
        print(f"Warning: Could not load saved portfolio: {error}")
        return []


def save_portfolio(portfolio):
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(portfolio, file, indent=4)
        print(f"Portfolio saved successfully to {DATA_FILE}.")
    except OSError as error:
        print(f"Could not save portfolio: {error}")


def add_stock(portfolio):
    heading("ADD STOCK TO PORTFOLIO")
    show_available_stocks()
    symbol = get_stock_symbol()
    quantity = get_positive_number("Enter quantity to buy: ")
    purchase_price = get_positive_number(
        f"Enter your purchase price per share (current sample price: "
        f"{money(STOCK_PRICES[symbol])}): "
    )

    # Keep each purchase as a separate lot so purchase prices remain accurate.
    portfolio.append({
        "symbol": symbol,
        "quantity": quantity,
        "purchase_price": purchase_price,
    })
    save_portfolio(portfolio)
    print(f"\n{quantity:g} shares of {symbol} added successfully.")
    print(f"Current estimated value: {money(quantity * STOCK_PRICES[symbol])}")


def view_portfolio(portfolio):
    heading("YOUR STOCK PORTFOLIO")
    if not portfolio:
        print("Your portfolio is empty. Add a stock to get started.")
        return

    headers = (
        f"{'NO.':<5}{'SYMBOL':<10}{'QUANTITY':>12}"
        f"{'BUY PRICE':>15}{'MARKET PRICE':>16}{'CURRENT VALUE':>18}"
    )
    print(headers)
    line("-")
    total_invested = total_value = total_pl = 0.0

    for index, position in enumerate(portfolio, 1):
        invested, value, pl = calculate_position(position)
        total_invested += invested
        total_value += value
        total_pl += pl
        print(
            f"{index:<5}{position['symbol']:<10}"
            f"{position['quantity']:>12.2f}"
            f"{money(position['purchase_price']):>15}"
            f"{money(STOCK_PRICES[position['symbol']]):>16}"
            f"{money(value):>18}"
        )

    line("-")
    print(f"Total purchase investment : {money(total_invested)}")
    print(f"Current portfolio value   : {money(total_value)}")
    print(f"Overall profit / loss     : {money(total_pl)} "
          f"({'PROFIT' if total_pl >= 0 else 'LOSS'})")
    if total_invested:
        print(f"Overall return            : {(total_pl / total_invested) * 100:.2f}%")


def portfolio_summary(portfolio):
    heading("PORTFOLIO SUMMARY")
    if not portfolio:
        print("No portfolio data available.")
        return

    total_invested = 0.0
    total_value = 0.0
    stock_totals = {}

    for position in portfolio:
        invested, value, _ = calculate_position(position)
        total_invested += invested
        total_value += value
        symbol = position["symbol"]
        stock_totals[symbol] = stock_totals.get(symbol, 0.0) + value

    pl = total_value - total_invested
    print(f"Number of purchase lots : {len(portfolio)}")
    print(f"Unique stocks           : {len(stock_totals)}")
    print(f"Total amount invested   : {money(total_invested)}")
    print(f"Current market value    : {money(total_value)}")
    print(f"Total profit / loss     : {money(pl)}")
    print(f"Return percentage       : {(pl / total_invested * 100):.2f}%"
          if total_invested else "Return percentage       : N/A")

    print("\nSTOCK ALLOCATION")
    line("-")
    for symbol, value in sorted(stock_totals.items(), key=lambda item: item[1], reverse=True):
        percentage = value / total_value * 100 if total_value else 0
        bar = "#" * int(percentage / 2)
        print(f"{symbol:<8} {percentage:>6.2f}%  {bar}")
    line("-")


def update_stock(portfolio):
    heading("UPDATE A PORTFOLIO ENTRY")
    if not portfolio:
        print("Portfolio is empty.")
        return
    view_portfolio(portfolio)
    try:
        index = int(input("\nEnter entry number to update: "))
        if not 1 <= index <= len(portfolio):
            print("Invalid entry number.")
            return
    except ValueError:
        print("Please enter a valid whole number.")
        return

    position = portfolio[index - 1]
    print(f"Selected: {position['symbol']} | Quantity: {position['quantity']}")
    print("1. Update quantity")
    print("2. Update purchase price")
    print("3. Update both")
    choice = input("Choose: ").strip()

    if choice in ("1", "3"):
        position["quantity"] = get_positive_number("New quantity: ")
    if choice in ("2", "3"):
        position["purchase_price"] = get_positive_number("New purchase price: ")
    if choice not in ("1", "2", "3"):
        print("Invalid choice. No changes made.")
        return

    save_portfolio(portfolio)
    print("Portfolio entry updated.")


def remove_stock(portfolio):
    heading("REMOVE A PORTFOLIO ENTRY")
    if not portfolio:
        print("Portfolio is empty.")
        return
    view_portfolio(portfolio)
    try:
        index = int(input("\nEnter entry number to remove: "))
        if not 1 <= index <= len(portfolio):
            print("Invalid entry number.")
            return
    except ValueError:
        print("Please enter a valid whole number.")
        return

    removed = portfolio.pop(index - 1)
    save_portfolio(portfolio)
    print(f"Removed {removed['symbol']} from the portfolio.")


def export_csv(portfolio):
    heading("EXPORT PORTFOLIO TO CSV")
    if not portfolio:
        print("Nothing to export. Your portfolio is empty.")
        return
    fields = [
        "symbol", "quantity", "purchase_price", "current_price",
        "total_investment", "current_value", "profit_loss", "return_percent"
    ]
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fields)
            writer.writeheader()
            for position in portfolio:
                invested, value, pl = calculate_position(position)
                writer.writerow({
                    "symbol": position["symbol"],
                    "quantity": position["quantity"],
                    "purchase_price": position["purchase_price"],
                    "current_price": STOCK_PRICES[position["symbol"]],
                    "total_investment": round(invested, 2),
                    "current_value": round(value, 2),
                    "profit_loss": round(pl, 2),
                    "return_percent": round(pl / invested * 100, 2) if invested else 0,
                })
        print(f"CSV report exported successfully: {CSV_FILE}")
    except OSError as error:
        print(f"CSV export failed: {error}")


def export_txt(portfolio):
    heading("EXPORT PORTFOLIO TO TEXT REPORT")
    if not portfolio:
        print("Nothing to export. Your portfolio is empty.")
        return
    total_invested = sum(calculate_position(p)[0] for p in portfolio)
    total_value = sum(calculate_position(p)[1] for p in portfolio)
    total_pl = total_value - total_invested

    try:
        with open(TXT_FILE, "w", encoding="utf-8") as file:
            file.write(APP_NAME + "\n")
            file.write("=" * 76 + "\n")
            file.write(f"Generated: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}\n\n")
            file.write(f"{'STOCK':<10}{'QUANTITY':>12}{'BUY PRICE':>15}"
                       f"{'MARKET PRICE':>16}{'CURRENT VALUE':>18}\n")
            file.write("-" * 76 + "\n")
            for position in portfolio:
                _, value, _ = calculate_position(position)
                file.write(
                    f"{position['symbol']:<10}{position['quantity']:>12.2f}"
                    f"{money(position['purchase_price']):>15}"
                    f"{money(STOCK_PRICES[position['symbol']]):>16}"
                    f"{money(value):>18}\n"
                )
            file.write("\n")
            file.write(f"Total investment: {money(total_invested)}\n")
            file.write(f"Current value:    {money(total_value)}\n")
            file.write(f"Profit / Loss:    {money(total_pl)}\n")
            file.write("\nDISCLAIMER: Prices are manually defined sample values, not live quotes.\n")
        print(f"Text report exported successfully: {TXT_FILE}")
    except OSError as error:
        print(f"Text export failed: {error}")


def search_stock(portfolio):
    heading("SEARCH STOCK IN PORTFOLIO")
    symbol = input("Enter stock symbol to search: ").strip().upper()
    matches = [p for p in portfolio if p["symbol"] == symbol]
    if not matches:
        print(f"No portfolio entries found for {symbol}.")
        return
    total_quantity = sum(p["quantity"] for p in matches)
    total_invested = sum(p["quantity"] * p["purchase_price"] for p in matches)
    current_value = total_quantity * STOCK_PRICES[symbol]
    print(f"Stock symbol          : {symbol}")
    print(f"Purchase lots         : {len(matches)}")
    print(f"Total quantity        : {total_quantity:g}")
    print(f"Average purchase price: {money(total_invested / total_quantity)}")
    print(f"Current sample price  : {money(STOCK_PRICES[symbol])}")
    print(f"Total investment      : {money(total_invested)}")
    print(f"Current value         : {money(current_value)}")
    print(f"Profit / Loss         : {money(current_value - total_invested)}")


def clear_portfolio(portfolio):
    heading("CLEAR PORTFOLIO")
    if not portfolio:
        print("Portfolio is already empty.")
        return
    confirm = input("This will remove all saved portfolio entries. Type YES to confirm: ")
    if confirm.strip().upper() == "YES":
        portfolio.clear()
        save_portfolio(portfolio)
        print("All portfolio entries have been removed.")
    else:
        print("Clear operation cancelled.")


def show_menu():
    heading(APP_NAME)
    print(f"Version {VERSION} | Python standard library only")
    print("\n1.  Add stock")
    print("2.  View available stocks and prices")
    print("3.  View portfolio")
    print("4.  Portfolio summary and allocation")
    print("5.  Update portfolio entry")
    print("6.  Remove portfolio entry")
    print("7.  Search portfolio by stock symbol")
    print("8.  Export portfolio to CSV")
    print("9.  Export portfolio to TXT")
    print("10. Save portfolio")
    print("11. Clear portfolio")
    print("0.  Exit")
    line("-")


def main():
    portfolio = load_portfolio()
    print(f"\nWelcome to {APP_NAME}!")
    print(f"Loaded {len(portfolio)} saved portfolio entr{'y' if len(portfolio) == 1 else 'ies'}.")

    actions = {
        "1": lambda: add_stock(portfolio),
        "2": show_available_stocks,
        "3": lambda: view_portfolio(portfolio),
        "4": lambda: portfolio_summary(portfolio),
        "5": lambda: update_stock(portfolio),
        "6": lambda: remove_stock(portfolio),
        "7": lambda: search_stock(portfolio),
        "8": lambda: export_csv(portfolio),
        "9": lambda: export_txt(portfolio),
        "10": lambda: save_portfolio(portfolio),
        "11": lambda: clear_portfolio(portfolio),
    }

    while True:
        show_menu()
        choice = input("Enter your choice: ").strip()
        if choice == "0":
            save_portfolio(portfolio)
            print("\nThank you for using the Stock Portfolio Tracker!")
            print("Remember: this educational project does not provide financial advice.")
            break
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Invalid option. Please choose a number from 0 to 11.")
        pause()


if __name__ == "__main__":
    main()
