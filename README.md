# a.s.r. Portfolio Tracker

CLI tool for tracking and simulating an investment portfolio.

## Features

- Add and remove assets (ticker, sector, asset class, quantity, purchase price)
- View current portfolio value and P/L using live prices from Yahoo Finance
- Break down portfolio weights by asset, sector, or asset class
- Plot historical price charts for one or more tickers
- Run a Monte Carlo simulation (geometric Brownian motion) to project future portfolio value
- Portfolio is persisted to `data/portfolio.json`

## Installation

```bash
git clone https://github.com/wdgraaf/asr-portfolio-tracker.git
cd asr-portfolio-tracker

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

python main.py
```

## Usage

Once started, the CLI shows a menu:

1. **Add asset** — enter ticker, sector, asset class, quantity, and purchase price.
2. **Remove asset** — remove an asset by ticker.
3. **View portfolio** — table with current prices, market value, and unrealised P/L.
4. **View weights** — portfolio weights grouped by asset, sector, or asset class.
5. **Price history & chart** — plot historical prices for one or more tickers over a chosen period (1mo, 6mo, 1y, 5y).
6. **Run simulation** — 15-year Monte Carlo projection using drift and volatility estimated from 2 years of daily returns.
0. **Exit**

## Project Structure

```
asr-portfolio-tracker/
├── main.py                      # Entry point
├── requirements.txt
├── controllers/                 # Controller
│   └── cli_controller.py        #   Menu loop, wires models and views
├── models/                      # Model
│   ├── portfolio.py             #   Portfolio state and persistence
│   ├── price_service.py         #   yfinance wrapper (live + historical)
│   └── simulation.py            #   Monte Carlo / GBM simulation
├── views/                       # View
│   └── display.py               #   Rich tables and matplotlib charts
└── data/
    └── portfolio.json           # Saved portfolio
```

## Tech Stack

- **Python 3.10+**
- **yfinance** — market data
- **pandas** — price data handling
- **numpy** — simulation and vector math
- **matplotlib** — price and simulation charts
- **rich** — formatted terminal tables
