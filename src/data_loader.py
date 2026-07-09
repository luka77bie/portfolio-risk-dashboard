cat > src/data_loader.py << 'EOF'
import time
from pathlib import Path
from io import StringIO

import pandas as pd
import yfinance as yf
import requests


def load_local_price_data(file_path="data/sample_prices.csv"):
    """
    Load local sample price data from CSV.
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

    print("Data source: local CSV")
    return prices


def download_price_data_yfinance(tickers, start_date, end_date, max_retries=3, sleep_seconds=5):
    """
    Download adjusted close prices using yfinance.
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

            print("Data source: yfinance")
            return prices

        except Exception as error:
            last_error = error
            print(f"yfinance attempt {attempt}/{max_retries} failed: {error}")
            time.sleep(sleep_seconds)

    raise RuntimeError("yfinance failed after multiple attempts.") from last_error


def download_single_ticker_stooq(ticker, start_date, end_date):
    """
    Download daily close price for one US ticker from Stooq.
    Example: AAPL -> aapl.us
    """
    stooq_ticker = f"{ticker.lower()}.us"

    start = pd.to_datetime(start_date).strftime("%Y%m%d")
    end = pd.to_datetime(end_date).strftime("%Y%m%d")

    url = (
        "https://stooq.com/q/d/l/"
        f"?s={stooq_ticker}&d1={start}&d2={end}&i=d"
    )

    response = requests.get(url, timeout=15)

    if response.status_code != 200:
        raise RuntimeError(f"Stooq request failed for {ticker}: HTTP {response.status_code}")

    data = pd.read_csv(StringIO(response.text))

    if data.empty or "Close" not in data.columns:
        raise ValueError(f"Stooq returned empty or invalid data for {ticker}")

    data["Date"] = pd.to_datetime(data["Date"])
    data = data.set_index("Date").sort_index()

    return data["Close"].rename(ticker)


def download_price_data_stooq(tickers, start_date, end_date):
    """
    Download price data from Stooq as secondary online data source.
    """
    series_list = []

    for ticker in tickers:
        series = download_single_ticker_stooq(ticker, start_date, end_date)
        series_list.append(series)

    prices = pd.concat(series_list, axis=1)
    prices = prices.dropna(how="all")

    if prices.empty:
        raise ValueError("Stooq price data is empty.")

    print("Data source: Stooq")
    return prices


def get_price_data(
    tickers,
    start_date,
    end_date,
    use_local_fallback=True,
    local_file_path="data/sample_prices.csv",
):
    """
    Multi-source price data pipeline.

    Priority:
    1. yfinance
    2. Stooq
    3. local CSV fallback
    """
    try:
        return download_price_data_yfinance(tickers, start_date, end_date)

    except Exception as yfinance_error:
        print("\nyfinance download failed.")
        print(f"Reason: {yfinance_error}\n")

    try:
        return download_price_data_stooq(tickers, start_date, end_date)

    except Exception as stooq_error:
        print("\nStooq download failed.")
        print(f"Reason: {stooq_error}\n")

    if not use_local_fallback:
        raise RuntimeError("All online data sources failed and local fallback is disabled.")

    print("Falling back to local sample data.\n")

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
EOF
