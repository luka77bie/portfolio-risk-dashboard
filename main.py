import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from src.data_loader import load_price_data


def calculate_portfolio_metrics(prices: pd.DataFrame, weights: np.ndarray) -> dict:
    """
    Calculate basic portfolio risk and return metrics.
    """

    returns = prices.pct_change().dropna()

    if returns.empty:
        raise ValueError("Not enough price data to calculate returns.")

    portfolio_returns = returns.dot(weights)
    cumulative_returns = (1 + portfolio_returns).cumprod()

    trading_days = 252

    annualised_return = portfolio_returns.mean() * trading_days
    annualised_volatility = portfolio_returns.std() * np.sqrt(trading_days)

    if annualised_volatility == 0:
        sharpe_ratio = np.nan
    else:
        sharpe_ratio = annualised_return / annualised_volatility

    running_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / running_max - 1
    maximum_drawdown = drawdown.min()

    return {
        "returns": returns,
        "portfolio_returns": portfolio_returns,
        "cumulative_returns": cumulative_returns,
        "annualised_return": annualised_return,
        "annualised_volatility": annualised_volatility,
        "sharpe_ratio": sharpe_ratio,
        "maximum_drawdown": maximum_drawdown,
    }


def plot_portfolio_performance(cumulative_returns: pd.Series) -> None:
    """
    Save a portfolio cumulative performance chart.
    """

    os.makedirs("outputs", exist_ok=True)

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_returns.index, cumulative_returns.values)
    plt.title("Portfolio Cumulative Performance")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("outputs/portfolio_performance.png")
    plt.close()


def main() -> None:
    tickers = ["AAPL", "MSFT"]
    weights = np.array([0.5, 0.5])

    start_date = "2024-01-01"
    end_date = "2024-12-31"

    prices = load_price_data(
        tickers=tickers,
        start_date=start_date,
        end_date=end_date,
        fallback_path="data/sample_prices.csv",
    )

    weights = weights[: len(prices.columns)]
    weights = weights / weights.sum()

    metrics = calculate_portfolio_metrics(prices, weights)

    print()
    print("Portfolio Risk Summary")
    print("----------------------")
    print(f"Assets: {', '.join(prices.columns)}")
    print(f"Annualised Return: {metrics['annualised_return']:.2%}")
    print(f"Annualised Volatility: {metrics['annualised_volatility']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Maximum Drawdown: {metrics['maximum_drawdown']:.2%}")

    plot_portfolio_performance(metrics["cumulative_returns"])

    print()
    print("Chart saved to outputs/portfolio_performance.png")


if __name__ == "__main__":
    main()
