import numpy as np


def calculate_portfolio_returns(asset_returns, weights):
    """
    Calculate portfolio daily returns from asset returns and portfolio weights.
    """
    weights = np.array(weights)

    if len(weights) != asset_returns.shape[1]:
        raise ValueError("Number of weights must match number of assets.")

    if not np.isclose(weights.sum(), 1.0):
        raise ValueError("Portfolio weights must sum to 1.")

    return asset_returns @ weights
