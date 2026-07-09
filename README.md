# Portfolio Risk Dashboard

A lightweight Python-based portfolio risk dashboard that downloads historical market data, calculates basic portfolio risk metrics, and visualises cumulative portfolio performance.

This project demonstrates Python, financial data processing, portfolio risk analysis, and a robust data pipeline with local CSV fallback support.

## Project Overview

The dashboard calculates and displays key risk indicators for a simple equity portfolio.

Current features include:

- Historical price data loading
- Automatic fallback to local sample data if online data download fails
- Daily return calculation
- Portfolio cumulative return calculation
- Annualised return
- Annualised volatility
- Sharpe ratio
- Maximum drawdown
- Portfolio performance chart generation

The project is intentionally kept simple and modular so that it can be extended later with more advanced quantitative finance methods.

## Why This Project

Financial data pipelines often fail when relying only on live API access. This project therefore uses a more robust structure:

1. First, the program attempts to download market data using `yfinance`.
2. If the download fails, the program automatically falls back to a local CSV file.
3. This ensures that `python3 main.py` can still run successfully even when the online data source is unavailable.

This makes the project more reliable for GitHub review, portfolio demonstration, and local testing.

## Project Structure

```text
portfolio-risk-dashboard/
│
├── main.py
├── requirements.txt
├── README.md
│
├── src/
│   ├── __init__.py
│   └── data_loader.py
│
├── data/
│   └── sample_prices.csv
│
└── outputs/
    └── portfolio_performance.png
```

## Technologies Used

- Python 3
- pandas
- numpy
- matplotlib
- yfinance

## Installation

Clone the repository:

```bash
git clone https://github.com/your-username/portfolio-risk-dashboard.git
cd portfolio-risk-dashboard
```

Install dependencies:

```bash
pip3 install -r requirements.txt
```

If you are using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## How to Run

Run the main script:

```bash
python3 main.py
```

If the program runs successfully, it will print a portfolio risk summary in the terminal and generate a performance chart.

Example output:

```text
Portfolio Risk Summary
----------------------
Annualised Return: ...
Annualised Volatility: ...
Sharpe Ratio: ...
Maximum Drawdown: ...
```

The output chart will be saved to:

```text
outputs/portfolio_performance.png
```

## Data Pipeline

The data loading logic is handled in:

```text
src/data_loader.py
```

The system follows this logic:

```text
Try to download historical prices from yfinance
        ↓
If successful, use downloaded market data
        ↓
If unsuccessful, load data/sample_prices.csv
        ↓
Calculate returns and portfolio risk metrics
```

This fallback design makes the project more stable than a script that depends only on live API access.

## Risk Metrics

### Annualised Return

Annualised return estimates the portfolio's yearly return based on average daily returns.

### Annualised Volatility

Annualised volatility measures the standard deviation of portfolio returns on a yearly basis.

### Sharpe Ratio

The Sharpe ratio measures return per unit of risk.

In this project, the basic Sharpe ratio is calculated without a risk-free rate assumption.

### Maximum Drawdown

Maximum drawdown measures the largest peak-to-trough decline in portfolio value.

It is useful for understanding downside risk.

## Example Portfolio

The default example portfolio uses:

```text
AAPL
MSFT
```

The weights are set inside `main.py`.

These tickers can be modified to test different portfolios.

## Local Sample Data

The project includes a local fallback dataset:

```text
data/sample_prices.csv
```

This file allows the project to run even if `yfinance` cannot download data due to network issues, API rate limits, or temporary service problems.

## Future Improvements

Possible extensions include:

- Add more assets and dynamic portfolio weights
- Add Value at Risk
- Add Conditional Value at Risk
- Add rolling volatility
- Add correlation matrix
- Add benchmark comparison
- Add Streamlit dashboard interface
- Add portfolio optimisation
- Add unit tests
- Add GitHub Actions workflow for automated testing

## Limitations

This project is for educational and portfolio demonstration purposes only.

It is not financial advice and should not be used as a production trading or investment system.

The risk metrics are simplified and do not account for transaction costs, taxes, liquidity constraints, market impact, or changing risk-free rates.

## Author

Jiacheng Bie

## License

This project is open for educational use.
