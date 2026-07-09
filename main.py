from src.data_loader import download_price_data, calculate_returns
from src.portfolio import calculate_portfolio_returns
from src.risk_metrics import (
    annualized_return,
    annualized_volatility,
    sharpe_ratio,
    max_drawdown,
    historical_var,
    historical_cvar,
)
from src.visualization import (
    plot_equity_curve,
    plot_drawdown,
    plot_correlation_matrix,
)


def main():
    tickers = ["AAPL", "MSFT", "NVDA", "JPM"]
    weights = [0.25, 0.25, 0.25, 0.25]

    start_date = "2020-01-01"
    end_date = "2025-01-01"

    prices = download_price_data(tickers, start_date, end_date)
    asset_returns = calculate_returns(prices)
    portfolio_returns = calculate_portfolio_returns(asset_returns, weights)

    print("Portfolio Risk Summary")
    print("-" * 40)
    print(f"Annualized Return: {annualized_return(portfolio_returns):.2%}")
    print(f"Annualized Volatility: {annualized_volatility(portfolio_returns):.2%}")
    print(f"Sharpe Ratio: {sharpe_ratio(portfolio_returns):.2f}")
    print(f"Maximum Drawdown: {max_drawdown(portfolio_returns):.2%}")
    print(f"95% Historical VaR: {historical_var(portfolio_returns):.2%}")
    print(f"95% Historical CVaR: {historical_cvar(portfolio_returns):.2%}")

    plot_equity_curve(portfolio_returns)
    plot_drawdown(portfolio_returns)
    plot_correlation_matrix(asset_returns)


if __name__ == "__main__":
    main()
