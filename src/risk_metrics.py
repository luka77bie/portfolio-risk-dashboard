import numpy as np


def annualized_return(daily_returns, trading_days=252):
    """
    Calculate annualized return from daily returns.
    """
    cumulative_return = (1 + daily_returns).prod()
    n_days = len(daily_returns)
    return cumulative_return ** (trading_days / n_days) - 1


def annualized_volatility(daily_returns, trading_days=252):
    """
    Calculate annualized volatility.
    """
    return daily_returns.std() * np.sqrt(trading_days)


def sharpe_ratio(daily_returns, risk_free_rate=0.02, trading_days=252):
    """
    Calculate annualized Sharpe ratio.
    """
    ann_return = annualized_return(daily_returns, trading_days)
    ann_vol = annualized_volatility(daily_returns, trading_days)

    if ann_vol == 0:
        return np.nan

    return (ann_return - risk_free_rate) / ann_vol


def max_drawdown(daily_returns):
    """
    Calculate maximum drawdown.
    """
    cumulative = (1 + daily_returns).cumprod()
    running_max = cumulative.cummax()
    drawdown = cumulative / running_max - 1
    return drawdown.min()


def historical_var(daily_returns, confidence_level=0.95):
    """
    Calculate historical Value at Risk.
    """
    return np.percentile(daily_returns, (1 - confidence_level) * 100)


def historical_cvar(daily_returns, confidence_level=0.95):
    """
    Calculate historical Conditional Value at Risk.
    """
    var = historical_var(daily_returns, confidence_level)
    return daily_returns[daily_returns <= var].mean()
