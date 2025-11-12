"""
Intraday data tools for day trading analysis.
Uses Alpaca API for minute-level data.
"""

from langchain_core.tools import tool
from typing import Annotated


@tool
def get_intraday_data(
    symbol: Annotated[str, "ticker symbol of the company"],
    date: Annotated[str, "Trading date in yyyy-mm-dd format"],
    timeframe: Annotated[str, "Timeframe: 1Min, 5Min, 15Min, 30Min, 1Hour"] = "5Min",
) -> str:
    """
    Retrieve intraday stock price data for a given ticker on a specific trading day.
    Returns OHLCV data at the specified timeframe (e.g., 5-minute bars).

    Args:
        symbol (str): Ticker symbol, e.g., AAPL, TSLA
        date (str): Trading date in yyyy-mm-dd format
        timeframe (str): Bar timeframe - "1Min", "5Min", "15Min", "30Min", "1Hour"

    Returns:
        str: Formatted DataFrame with timestamp, open, high, low, close, volume
    """
    from tradingagents.dataflows.alpaca_intraday import get_alpaca_intraday_bars

    try:
        df = get_alpaca_intraday_bars(symbol, timeframe=timeframe, date=date)

        if df.empty:
            return f"No intraday data available for {symbol} on {date}"

        # Return formatted string representation
        return df.to_csv(index=False)

    except Exception as e:
        return f"Error fetching intraday data: {str(e)}"


@tool
def get_intraday_indicators(
    symbol: Annotated[str, "ticker symbol of the company"],
    date: Annotated[str, "Trading date in yyyy-mm-dd format"],
    timeframe: Annotated[str, "Timeframe: 1Min, 5Min, 15Min, 30Min, 1Hour"] = "5Min",
) -> str:
    """
    Calculate day trading indicators on intraday data.
    Includes: VWAP, EMA-9, EMA-21, RSI, ATR.

    Args:
        symbol (str): Ticker symbol, e.g., AAPL, TSLA
        date (str): Trading date in yyyy-mm-dd format
        timeframe (str): Bar timeframe - "1Min", "5Min", "15Min", "30Min", "1Hour"

    Returns:
        str: Formatted DataFrame with indicators
    """
    from tradingagents.dataflows.alpaca_intraday import (
        get_alpaca_intraday_bars,
        calculate_intraday_indicators
    )

    try:
        df = get_alpaca_intraday_bars(symbol, timeframe=timeframe, date=date)

        if df.empty:
            return f"No intraday data available for {symbol} on {date}"

        # Calculate indicators
        df = calculate_intraday_indicators(df)

        # Return relevant columns
        output_cols = [
            'timestamp', 'close', 'volume', 'vwap',
            'ema_9', 'ema_21', 'rsi', 'atr'
        ]

        return df[output_cols].to_csv(index=False)

    except Exception as e:
        return f"Error calculating intraday indicators: {str(e)}"


@tool
def get_latest_quote(
    symbol: Annotated[str, "ticker symbol of the company"],
) -> str:
    """
    Get the latest real-time quote for a ticker.
    Returns current bid, ask, and sizes.

    Args:
        symbol (str): Ticker symbol, e.g., AAPL, TSLA

    Returns:
        str: Latest quote information
    """
    from tradingagents.dataflows.alpaca_intraday import get_alpaca_latest_quote

    try:
        quote = get_alpaca_latest_quote(symbol)

        if not quote:
            return f"No quote available for {symbol}"

        return (
            f"Latest Quote for {symbol}:\n"
            f"  Bid: ${quote['bid']:.2f} (Size: {quote['bid_size']})\n"
            f"  Ask: ${quote['ask']:.2f} (Size: {quote['ask_size']})\n"
            f"  Spread: ${quote['ask'] - quote['bid']:.2f} "
            f"({(quote['ask'] - quote['bid']) / quote['bid'] * 100:.2f}%)\n"
            f"  Time: {quote['timestamp']}"
        )

    except Exception as e:
        return f"Error fetching latest quote: {str(e)}"
