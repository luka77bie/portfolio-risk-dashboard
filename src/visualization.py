import os

import matplotlib.pyplot as plt
import pandas as pd


def ensure_output_dir(output_dir: str = "outputs") -> None:
    """
    Create output directory if it does not exist.
    """
    os.makedirs(output_dir, exist_ok=True)


def plot_portfolio_performance(
    cumulative_returns: pd.Series,
    save_path: str = "outputs/portfolio_performance.png",
) -> None:
    """
    Save cumulative portfolio performance chart.
    """
    ensure_output_dir()

    plt.figure(figsize=(10, 6))
    plt.plot(cumulative_returns.index, cumulative_returns.values)
    plt.title("Portfolio Cumulative Performance")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_drawdown(
    drawdowns: pd.Series,
    save_path: str = "outputs/drawdown.png",
) -> None:
    """
    Save portfolio drawdown chart.
    """
    ensure_output_dir()

    plt.figure(figsize=(10, 6))
    plt.plot(drawdowns.index, drawdowns.values)
    plt.title("Portfolio Drawdown")
    plt.xlabel("Date")
    plt.ylabel("Drawdown")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_correlation_matrix(
    asset_returns: pd.DataFrame,
    save_path: str = "outputs/correlation_matrix.png",
) -> None:
    """
    Save asset return correlation matrix.
    """
    ensure_output_dir()

    corr = asset_returns.corr()

    plt.figure(figsize=(8, 6))
    plt.imshow(corr)
    plt.colorbar(label="Correlation")
    plt.xticks(range(len(corr.columns)), corr.columns, rotation=45)
    plt.yticks(range(len(corr.columns)), corr.columns)
    plt.title("Asset Return Correlation Matrix")

    for i in range(len(corr.columns)):
        for j in range(len(corr.columns)):
            plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")

    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()


def plot_return_distribution(
    portfolio_returns: pd.Series,
    save_path: str = "outputs/return_distribution.png",
) -> None:
    """
    Save portfolio daily return distribution histogram.
    """
    ensure_output_dir()

    plt.figure(figsize=(10, 6))
    plt.hist(portfolio_returns.values, bins=30)
    plt.title("Portfolio Daily Return Distribution")
    plt.xlabel("Daily Return")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.close()
