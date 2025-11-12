"""
Alpaca API integration for intraday trading data.
Provides minute-level bars for day trading analysis.
"""

import os
import pandas as pd
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()


def get_alpaca_intraday_bars(
    ticker: str,
    timeframe: str = "5Min",
    date: str = None,
    limit: int = 390  # Full trading day (6.5 hours * 60 minutes / timeframe)
):
    """
    Fetch intraday bars from Alpaca API.

    Args:
        ticker: Stock ticker symbol
        timeframe: Bar timeframe - "1Min", "5Min", "15Min", "30Min", "1Hour"
        date: Trading date in YYYY-MM-DD format (defaults to today)
        limit: Number of bars to fetch (default 390 = full day for 1min bars)

    Returns:
        DataFrame with columns: timestamp, open, high, low, close, volume
    """
    try:
        from alpaca.data.historical import StockHistoricalDataClient
        from alpaca.data.requests import StockBarsRequest
        from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
    except ImportError:
        raise ImportError(
            "Alpaca SDK not installed. Install with: pip install alpaca-py"
        )

    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        raise ValueError(
            "Alpaca API keys not found. Set ALPACA_API_KEY and ALPACA_SECRET_KEY in .env"
        )

    # Initialize client (paper trading by default)
    client = StockHistoricalDataClient(api_key, secret_key)

    # Parse timeframe
    timeframe_map = {
        "1Min": TimeFrame(1, TimeFrameUnit.Minute),
        "5Min": TimeFrame(5, TimeFrameUnit.Minute),
        "15Min": TimeFrame(15, TimeFrameUnit.Minute),
        "30Min": TimeFrame(30, TimeFrameUnit.Minute),
        "1Hour": TimeFrame(1, TimeFrameUnit.Hour),
    }

    if timeframe not in timeframe_map:
        raise ValueError(
            f"Invalid timeframe. Choose from: {list(timeframe_map.keys())}"
        )

    tf = timeframe_map[timeframe]

    # Set date range
    if date:
        target_date = datetime.strptime(date, "%Y-%m-%d")
    else:
        target_date = datetime.now()

    # Alpaca requires start and end times
    # Market hours: 9:30 AM - 4:00 PM ET
    start = target_date.replace(hour=9, minute=30, second=0, microsecond=0)
    end = target_date.replace(hour=16, minute=0, second=0, microsecond=0)

    # Create request
    request_params = StockBarsRequest(
        symbol_or_symbols=ticker,
        timeframe=tf,
        start=start,
        end=end,
        limit=limit
    )

    # Fetch data
    bars = client.get_stock_bars(request_params)

    # Convert to DataFrame
    if ticker in bars.data:
        df = bars.df

        # Reset index to make timestamp a column
        df = df.reset_index()

        # Rename columns to match existing format
        df = df.rename(columns={
            'symbol': 'ticker',
            'timestamp': 'timestamp',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'volume': 'volume'
        })

        # Convert timestamp to string format
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')

        return df[['timestamp', 'open', 'high', 'low', 'close', 'volume']]
    else:
        return pd.DataFrame()


def get_alpaca_latest_quote(ticker: str):
    """
    Get the latest quote for a ticker.
    Useful for real-time trading decisions.

    Args:
        ticker: Stock ticker symbol

    Returns:
        dict with bid, ask, bid_size, ask_size, timestamp
    """
    try:
        from alpaca.data.historical import StockHistoricalDataClient
        from alpaca.data.requests import StockLatestQuoteRequest
    except ImportError:
        raise ImportError(
            "Alpaca SDK not installed. Install with: pip install alpaca-py"
        )

    api_key = os.getenv("ALPACA_API_KEY")
    secret_key = os.getenv("ALPACA_SECRET_KEY")

    if not api_key or not secret_key:
        raise ValueError(
            "Alpaca API keys not found. Set ALPACA_API_KEY and ALPACA_SECRET_KEY in .env"
        )

    client = StockHistoricalDataClient(api_key, secret_key)

    request_params = StockLatestQuoteRequest(symbol_or_symbols=ticker)
    latest_quote = client.get_stock_latest_quote(request_params)

    if ticker in latest_quote:
        quote = latest_quote[ticker]
        return {
            "bid": quote.bid_price,
            "ask": quote.ask_price,
            "bid_size": quote.bid_size,
            "ask_size": quote.ask_size,
            "timestamp": quote.timestamp.strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        return {}


def calculate_vwap(df: pd.DataFrame):
    """
    Calculate Volume Weighted Average Price (VWAP).
    Critical indicator for day trading.

    Args:
        df: DataFrame with columns: high, low, close, volume

    Returns:
        Series with VWAP values
    """
    typical_price = (df['high'] + df['low'] + df['close']) / 3
    return (typical_price * df['volume']).cumsum() / df['volume'].cumsum()


def calculate_intraday_indicators(df: pd.DataFrame):
    """
    Calculate day trading indicators on intraday data.

    Args:
        df: DataFrame with OHLCV data

    Returns:
        DataFrame with added indicator columns
    """
    # VWAP
    df['vwap'] = calculate_vwap(df)

    # EMAs (faster than SMAs for intraday)
    df['ema_9'] = df['close'].ewm(span=9, adjust=False).mean()
    df['ema_21'] = df['close'].ewm(span=21, adjust=False).mean()

    # RSI
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['rsi'] = 100 - (100 / (1 + rs))

    # ATR (for stop-loss)
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift())
    low_close = abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    true_range = ranges.max(axis=1)
    df['atr'] = true_range.rolling(14).mean()

    return df


# Example usage
if __name__ == "__main__":
    # Test the integration
    ticker = "AAPL"
    date = "2024-03-15"

    print(f"Fetching 5-minute bars for {ticker} on {date}...")
    df = get_alpaca_intraday_bars(ticker, timeframe="5Min", date=date)

    if not df.empty:
        print(f"\nFetched {len(df)} bars")
        print(f"\nFirst few rows:")
        print(df.head())

        print(f"\nCalculating indicators...")
        df = calculate_intraday_indicators(df)
        print(df[['timestamp', 'close', 'vwap', 'ema_9', 'ema_21', 'rsi']].tail())
    else:
        print("No data returned. Check your API keys and date.")
