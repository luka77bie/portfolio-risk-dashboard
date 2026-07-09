import os
from typing import List

import pandas as pd


def load_price_data(
    tickers: List[str],
    start_date: str,
    end_date: str,
    fallback_path: str = "data/sample_prices.csv",
) -> pd.DataFrame:
    """
    Load historical price data.

    The function first attempts to download adjusted close prices from yfinance.
    If the download fails or returns empty data, it falls back to a local CSV file.

    Parameters
    ----------
    tickers : List[str]
        List of ticker symbols.
    start_date : str
        Start date in YYYY-MM-DD format.
    end_date : str
        End date in YYYY-MM-DD format.
    fallback_path : str
        Path to the local fallback CSV file.

    Returns
    -------
    pd.DataFrame
        Price data indexed by date.
    """

    try:
        import yfinance as yf

        print("Attempting to download market data from yfinance...")

        raw_data = yf.download(
            tickers,
            start=start_date,
            end=end_date,
            auto_adjust=True,
            progress=False,
        )

        if raw_data.empty:
            raise ValueError("yfinance returned empty data.")

        if isinstance(raw_data.columns, pd.MultiIndex):
            if "Close" in raw_data.columns.get_level_values(0):
                prices = raw_data["Close"]
            else:
                prices = raw_data["Adj Close"]
        else:
            prices = raw_data

        if isinstance(prices, pd.Series):
            prices = prices.to_frame(name=tickers[0])

        prices = prices.dropna(how="all")

        if prices.empty:
            raise ValueError("Downloaded price data is empty after cleaning.")

        print("Market data downloaded successfully.")
        return prices

    except Exception as error:
        print(f"Online data download failed: {error}")
        print(f"Loading fallback data from {fallback_path}...")

        if not os.path.exists(fallback_path):
            raise FileNotFoundError(
                f"Fallback file not found: {fallback_path}. "
                "Please create data/sample_prices.csv."
            )

        fallback_data = pd.read_csv(fallback_path, parse_dates=["Date"])
        fallback_data = fallback_data.set_index("Date")
        fallback_data = fallback_data.sort_index()

        available_columns = [ticker for ticker in tickers if ticker in fallback_data.columns]

        if not available_columns:
            raise ValueError(
                "None of the requested tickers are available in the fallback CSV file."
            )

        return fallback_data[available_columns]
