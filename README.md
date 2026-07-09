# Portfolio Risk Dashboard

A Python-based portfolio risk analytics tool for evaluating historical performance, downside risk, drawdown, and asset correlation of a multi-asset portfolio.

## Motivation

Portfolio construction is not only about expected return. A professional investment workflow should also consider volatility, downside risk, tail loss, maximum drawdown, and asset correlation.

This project implements a lightweight risk dashboard to analyze these dimensions using historical market data.

## Features

- Historical price data download
- Daily return calculation
- Portfolio return aggregation
- Annualized return
- Annualized volatility
- Sharpe ratio
- Historical Value at Risk
- Conditional Value at Risk
- Maximum drawdown
- Equity curve visualization
- Drawdown visualization
- Correlation matrix visualization

## Methodology

The portfolio return is calculated as a weighted sum of individual asset returns:

`portfolio_return = sum(weight_i * asset_return_i)`

where `weight_i` is the portfolio weight of asset `i`, and `asset_return_i` is the daily return of asset `i`.

Historical VaR is estimated from the empirical distribution of portfolio returns. CVaR is calculated as the average portfolio return below the VaR threshold.

## Example Portfolio

```python
tickers = ["AAPL", "MSFT"]
weights = [0.5, 0.5]

## Example Outputs

### Equity Curve

![Equity Curve](outputs/equity_curve.png)

### Drawdown

![Drawdown](outputs/drawdown.png)

### Correlation Matrix

![Correlation Matrix](outputs/correlation_matrix.png)
