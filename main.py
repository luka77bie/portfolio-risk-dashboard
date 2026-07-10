import numpy as np

from src.data_loader import load_price_data
from src.risk_metrics import calculate_summary_metrics
from src.visualization import (
    plot_portfolio_performance,
    plot_drawdown,
    plot_correlation_matrix,
    plot_return_distribution,
)


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

    metrics = calculate_summary_metrics(
        prices=prices,
        weights=weights,
        risk_free_rate=0.0,
        confidence_level=0.95,
    )

    print()
    print("Portfolio Risk Summary")
    print("----------------------")
    print(f"Assets: {', '.join(prices.columns)}")
    print(f"Start Date: {prices.index.min().date()}")
    print(f"End Date: {prices.index.max().date()}")
    print(f"Number of Observations: {len(prices)}")
    print("----------------------")
    print(f"Annualised Return: {metrics['annualised_return']:.2%}")
    print(f"Annualised Volatility: {metrics['annualised_volatility']:.2%}")
    print(f"Sharpe Ratio: {metrics['sharpe_ratio']:.2f}")
    print(f"Maximum Drawdown: {metrics['maximum_drawdown']:.2%}")
    print(f"95% Historical VaR: {metrics['historical_var']:.2%}")
    print(f"95% Historical CVaR: {metrics['historical_cvar']:.2%}")

    plot_portfolio_performance(metrics["cumulative_returns"])
    plot_drawdown(metrics["drawdowns"])
    plot_correlation_matrix(metrics["asset_returns"])
    plot_return_distribution(metrics["portfolio_returns"])

    print()
    print("Charts saved to outputs/:")
    print("- outputs/portfolio_performance.png")
    print("- outputs/drawdown.png")
    print("- outputs/correlation_matrix.png")
    print("- outputs/return_distribution.png")


if __name__ == "__main__":
    main()
