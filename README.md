# CodeAlpha Internship – Task 2: Stock Portfolio Tracker

A menu-driven Python application that tracks a stock portfolio using manually defined stock prices. It calculates total investment, current estimated value, profit/loss, returns, and stock allocation.

## Features

- Add multiple stock purchases (purchase lots are stored separately).
- Hardcoded dictionary containing 20 sample stock symbols and prices.
- Calculate total investment and current estimated portfolio value.
- Calculate profit/loss and percentage return.
- View portfolio summary and allocation breakdown.
- Update or remove portfolio entries.
- Search holdings by stock symbol.
- Save and automatically reload portfolio data using JSON.
- Export portfolio reports to CSV and TXT.
- Input validation and file error handling.
- Uses only Python's standard library.

## Requirements

- Python 3.8 or newer
- No third-party packages required

## Run the project

Open a terminal in this folder and run:

```bash
python stock_portfolio_tracker.py
```

On some Windows installations, use:

```powershell
py stock_portfolio_tracker.py
```

## How to use

1. Run the Python file.
2. Select **2** to view the supported symbols and sample prices.
3. Select **1** to add a stock.
4. Enter the stock symbol, quantity, and your purchase price per share.
5. Select **3** to view your holdings and portfolio value.
6. Select **4** to view the summary and allocation.
7. Use options **8** and **9** to export CSV and TXT reports.
8. Select **0** to save and exit.

## Supported sample symbols

AAPL, TSLA, GOOGL, MSFT, AMZN, NVDA, META, NFLX, ORCL, IBM, INTC, AMD, DIS, KO, PEP, UBER, PYPL, ADBE, CRM, COST.

Prices are defined in the `STOCK_PRICES` dictionary at the top of `stock_portfolio_tracker.py`. Edit the values manually whenever you want to simulate a different market price.

## Calculation logic

- **Total investment** = Quantity × Purchase price per share
- **Current value** = Quantity × Hardcoded current sample price
- **Profit/Loss** = Current value − Total investment
- **Return (%)** = (Profit/Loss ÷ Total investment) × 100

## Files created while using the application

| File | Purpose |
|---|---|
| `portfolio_data.json` | Saves portfolio entries for the next run |
| `portfolio_report.csv` | Spreadsheet-friendly report |
| `portfolio_report.txt` | Readable text report |

These files are generated in the same folder when the relevant operations are used.

## Example

Suppose you buy 5 shares of AAPL at $170 each. The hardcoded sample price is $180.

- Total investment = 5 × 170 = **$850**
- Current value = 5 × 180 = **$900**
- Profit = 900 − 850 = **$50**
- Return = (50 ÷ 850) × 100 = **5.88%**

