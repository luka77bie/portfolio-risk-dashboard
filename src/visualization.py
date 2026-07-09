import matplotlib.pyplot as plt


def plot_equity_curve(portfolio_returns):
    """
    Plot cumulative portfolio return.
    """
    equity_curve = (1 + portfolio_returns).cumprod()

    plt.figure(figsize=(10, 5))
    plt.plot(equity_curve)
    plt.title("Portfolio Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.grid(True)
    plt.show()


def plot_drawdown(portfolio_returns):
    """
    Plot portfolio drawdown.
    """
    equity_curve = (1 + portfolio_returns).cumprod()
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1

    plt.figure(figsize=(10, 5))
    plt.plot(drawdown)
    plt.title("Portfolio Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.show()


def plot_correlation_matrix(asset_returns):
    """
    Plot correlation matrix of asset returns.
    """
    corr = asset_returns.corr()

    plt.figure(figsize=(8, 6))
    plt.imshow(corr)
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Asset Return Correlation Matrix")
    plt.show()
