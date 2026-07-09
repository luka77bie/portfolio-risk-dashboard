import time
from pathlib import Path
import pandas as pd
import yfinance as yf

def load_local_price_data(file_path="data/sample_prices.csv"):
    """
    Load local sample price data from CSV.
    The CSV file must contain:
    - Date column
    - One column per asset ticker
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Local price data file not found: {file_path}")

    prices = pd.read_csv(path, parse_dates=["Date"])
    prices = prices.set_index("Date")
    prices = prices.sort_index()
    prices = prices.dropna(how="all")

    if prices.empty:
        raise ValueError("Local price data is empty.")

    return prices

def download_price_data(tickers, start_date, end_date, max_retries=3, sleep_seconds=5):
    """
    Download adjusted close prices for a list of assets.
    This function uses yfinance as the primary data source.
    Free market data APIs may occasionally rate-limit requests.
    """
    last_error = None

    for attempt in range(1, max_retries + 1):
        try:
            data = yf.download(
                tickers,
                start=start_date,
                end=end_date,
                auto_adjust=True,
                progress=False,
                threads=False,
            )

            if data.empty:
                raise ValueError("Downloaded data is empty.")

            if isinstance(data.columns, pd.MultiIndex):
                prices = data["Close"]
            else:
                prices = data[["Close"]]
                prices.columns = tickers

            prices = prices.dropna(how="all")

            if prices.empty:
                raise ValueError("Price data is empty after cleaning.")

            return prices

        except Exception as error:
            last_error = error
            print(f"Download attempt {attempt}/{max_retries} failed: {error}")
            time.sleep(sleep_seconds)

    raise RuntimeError(
        "Failed to download market data after multiple attempts. "
        "This may be caused by API rate limits or network issues."
    ) from last_error

def get_price_data(
    tickers,
    start_date,
    end_date,
    use_local_fallback=True,
    local_file_path="data/sample_prices.csv",
):
    """
    Get price data from yfinance first, then fall back to local CSV if needed.
    """
    try:
        return download_price_data(tickers, start_date, end_date)
    except Exception as error:
        if not use_local_fallback:
            raise error

        print("\nMarket data download failed.")
        print("Falling back to local sample data.")
        print(f"Reason: {error}\n")

        prices = load_local_price_data(local_file_path)
        missing_tickers = [ticker for ticker in tickers if ticker not in prices.columns]
        if missing_tickers:
            raise ValueError(
                f"Local sample data does not contain requested tickers: {missing_tickers}"
            )

        return prices[tickers]

def calculate_returns(prices):
    """
    Calculate daily percentage returns.
    """
    returns = prices.pct_change().dropna()

    if returns.empty:
        raise ValueError(
            "Return data is empty. Check whether price data was loaded correctly."
        )

    return returns
