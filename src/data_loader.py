import yfinance as yf
import pandas as pd


def download_price_data(tickers, start_date, end_date):
    """
    Download adjusted close prices for a list of assets.
    """
    data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)

    if isinstance(data.columns, pd.MultiIndex):
        prices = data["Close"]
    else:
        prices = data[["Close"]]
        prices.columns = tickers

    return prices.dropna()


def calculate_returns(prices):
    """
    Calculate daily percentage returns.
    """
    return prices.pct_change().dropna()
