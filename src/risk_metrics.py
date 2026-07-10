import numpy as np
import pandas as pd


def calculate_daily_returns(prices: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate daily percentage returns from price data.
    """
    returns = prices.pct_change().dropna()

    if returns.empty:
        raise ValueError("Not enough price data to calculate returns.")

    return returns


def calculate_portfolio_returns(
    asset_returns: pd.DataFrame,
    weights: np.ndarray,
) -> pd.Series:
    """
    Calculate portfolio daily returns as weighted asset returns.
    """
    weights = np.asarray(weights, dtype=float)

    if len(weights) != asset_returns.shape[1]:
        raise ValueError("Number of weights must match number of assets.")

    if weights.sum() == 0:
        raise ValueError("Portfolio weights cannot sum to zero.")

    weights = weights / weights.sum()

    return asset_returns.dot(weights)


def calculate_cumulative_returns(portfolio_returns: pd.Series) -> pd.Series:
    """
    Calculate cumulative portfolio returns.
    """
    return (1 + portfolio_returns).cumprod()


def annualised_return(portfolio_returns: pd.Series, trading_days: int = 252) -> float:
    """
    Estimate annualised return using average daily return.
    """
    return portfolio_returns.mean() * trading_days


def annualised_volatility(portfolio_returns: pd.Series, trading_days: int = 252) -> float:
    """
    Estimate annualised volatility using daily return standard deviation.
    """
    return portfolio_returns.std() * np.sqrt(trading_days)


def sharpe_ratio(
    portfolio_returns: pd.Series,
    risk_free_rate: float = 0.0,
    trading_days: int = 252,
) -> float:
    """
    Calculate simplified annualised Sharpe ratio.

    risk_free_rate is expressed as an annual rate.
    """
    ann_return = annualised_return(portfolio_returns, trading_days)
    ann_vol = annualised_volatility(portfolio_returns, trading_days)

    if ann_vol == 0:
        return np.nan

    return (ann_return - risk_free_rate) / ann_vol


def drawdown_series(portfolio_returns: pd.Series) -> pd.Series:
    """
    Calculate drawdown series from portfolio returns.
    """
    cumulative_returns = calculate_cumulative_returns(portfolio_returns)
    running_max = cumulative_returns.cummax()
    drawdown = cumulative_returns / running_max - 1

    return drawdown


def maximum_drawdown(portfolio_returns: pd.Series) -> float:
    """
    Calculate maximum drawdown.
    """
    return drawdown_series(portfolio_returns).min()


def historical_var(portfolio_returns: pd.Series, confidence_level: float = 0.95) -> float:
    """
    Calculate Historical Value at Risk as a return quantile.

    Negative values represent portfolio losses.
    """
    return np.percentile(portfolio_returns, (1 - confidence_level) * 100)


def historical_cvar(portfolio_returns: pd.Series, confidence_level: float = 0.95) -> float:
    """
    Calculate Historical Conditional Value at Risk.

    CVaR is the average return below the VaR threshold.
    Negative values represent average tail losses.
    """
    var = historical_var(portfolio_returns, confidence_level)
    tail_losses = portfolio_returns[portfolio_returns <= var]

    if tail_losses.empty:
        return np.nan

    return tail_losses.mean()


def calculate_summary_metrics(
    prices: pd.DataFrame,
    weights: np.ndarray,
    risk_free_rate: float = 0.0,
    confidence_level: float = 0.95,
) -> dict:
    """
    Calculate portfolio return, risk, tail-risk, and drawdown metrics.
    """
    asset_returns = calculate_daily_returns(prices)
    portfolio_returns = calculate_portfolio_returns(asset_returns, weights)
    cumulative_returns = calculate_cumulative_returns(portfolio_returns)
    drawdowns = drawdown_series(portfolio_returns)

    metrics = {
        "asset_returns": asset_returns,
        "portfolio_returns": portfolio_returns,
        "cumulative_returns": cumulative_returns,
        "drawdowns": drawdowns,
        "annualised_return": annualised_return(portfolio_returns),
        "annualised_volatility": annualised_volatility(portfolio_returns),
        "sharpe_ratio": sharpe_ratio(portfolio_returns, risk_free_rate),
        "maximum_drawdown": maximum_drawdown(portfolio_returns),
        "historical_var": historical_var(portfolio_returns, confidence_level),
        "historical_cvar": historical_cvar(portfolio_returns, confidence_level),
    }

    return metrics
