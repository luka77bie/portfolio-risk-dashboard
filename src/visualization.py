import os
import matplotlib.pyplot as plt


def ensure_output_dir(output_dir="outputs"):
    """
    Create output directory if it does not exist.
    """
    os.makedirs(output_dir, exist_ok=True)


def plot_equity_curve(portfolio_returns, save_path="outputs/equity_curve.png"):
    """
    Plot and save cumulative portfolio return.
    """
    ensure_output_dir()
    equity_curve = (1 + portfolio_returns).cumprod()

    plt.figure(figsize=(10, 5))
    plt.plot(equity_curve)
    plt.title("Portfolio Equity Curve")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.grid(True)
    plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.close()


def plot_drawdown(portfolio_returns, save_path="outputs/drawdown.png"):
    """
    Plot and save portfolio drawdown.
    """
    ensure_output_dir()
    equity_curve = (1 + portfolio_returns).cumprod()
    running_max = equity_curve.cummax()
    drawdown = equity_curve / running_max - 1

    plt.figure(figsize=(10, 5))
    plt.plot(drawdown)
    plt.title("Portfolio Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.close()


def plot_correlation_matrix(asset_returns, save_path="outputs/correlation_matrix.png"):
    """
    Plot and save asset return correlation matrix.
    """
    ensure_output_dir()
    corr = asset_returns.corr()

    plt.figure(figsize=(8, 6))
    plt.imshow(corr)
    plt.colorbar()
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Asset Return Correlation Matrix")
    plt.savefig(save_path, bbox_inches="tight", dpi=150)
    plt.close()