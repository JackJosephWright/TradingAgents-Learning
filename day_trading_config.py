"""
Day Trading Configuration
Optimized for fast intraday decisions with Alpaca data.
"""

import os
from tradingagents.default_config import DEFAULT_CONFIG

# Create day trading config based on defaults
DAY_TRADING_CONFIG = DEFAULT_CONFIG.copy()

# Update for day trading
DAY_TRADING_CONFIG.update({
    # LLM settings - Use fast model for everything
    "llm_provider": "openai",
    "deep_think_llm": "gpt-4o-mini",  # Faster than o4-mini
    "quick_think_llm": "gpt-4o-mini",  # Same model for consistency
    "backend_url": "https://api.openai.com/v1",

    # NO DEBATE for speed (bull/bear debate takes too long)
    "max_debate_rounds": 0,  # Skip debate entirely
    "max_risk_discuss_rounds": 1,  # Single risk check only

    # Data vendors - Alpaca for intraday, yfinance as backup
    "data_vendors": {
        "core_stock_apis": "alpaca",  # Use Alpaca for intraday
        "technical_indicators": "alpaca",  # Intraday indicators
        "fundamental_data": "yfinance",  # Not used, but keep for compatibility
        "news_data": "yfinance",  # Pre-market news only
    },

    # Memory prefix
    "memory_prefix": "day_trading",
})

# Analysts to use (NO FUNDAMENTALS for day trading)
DAY_TRADING_ANALYSTS = [
    "market",  # Technical analysis on intraday charts
    # "social",  # Optional: Skip for speed
    # "news",    # Optional: Only useful pre-market
    # "fundamentals" is REMOVED - not relevant for day trading
]

# Intraday holding periods and thresholds
INTRADAY_PERIODS = {
    "30min": {
        "minutes": 30,
        "buy_threshold": 0.3,   # 0.3% gain target
        "sell_threshold": -0.2  # 0.2% max loss
    },
    "1hr": {
        "minutes": 60,
        "buy_threshold": 0.5,   # 0.5% gain target
        "sell_threshold": -0.3  # 0.3% max loss
    },
    "2hr": {
        "minutes": 120,
        "buy_threshold": 0.8,   # 0.8% gain target
        "sell_threshold": -0.5  # 0.5% max loss
    },
    "4hr": {
        "minutes": 240,
        "buy_threshold": 1.2,   # 1.2% gain target
        "sell_threshold": -0.8  # 0.8% max loss
    }
}

# Trading session times (ET)
MARKET_OPEN = "09:30"
MARKET_CLOSE = "16:00"
PRE_MARKET_START = "04:00"
AFTER_HOURS_END = "20:00"

# Day trading rules
DAY_TRADING_RULES = {
    "timeframe": "5Min",  # 5-minute candles (most common for day trading)
    "min_volume": 1000000,  # Minimum daily volume (liquidity)
    "max_spread_pct": 0.1,  # Max 0.1% bid-ask spread
    "no_overnight": True,  # Close all positions by market close
    "avoid_first_15min": True,  # Skip 9:30-9:45 (high volatility)
    "avoid_last_15min": True,  # Skip 3:45-4:00 (closing volatility)
}

# High-volume stocks suitable for day trading
DAY_TRADING_STOCKS = [
    "SPY",   # S&P 500 ETF (highest volume)
    "QQQ",   # NASDAQ ETF
    "AAPL",  # Apple
    "TSLA",  # Tesla
    "NVDA",  # NVIDIA
    "AMD",   # AMD
    "AMZN",  # Amazon
    "MSFT",  # Microsoft
    "META",  # Meta
    "GOOGL", # Google
]

# Performance tracking
PERFORMANCE_METRICS = [
    "win_rate",          # % of profitable trades
    "avg_gain",          # Average gain per winning trade
    "avg_loss",          # Average loss per losing trade
    "profit_factor",     # Total gains / Total losses
    "sharpe_ratio",      # Risk-adjusted return
    "max_drawdown",      # Largest peak-to-trough decline
    "trades_per_day",    # Trading frequency
]


def print_config_summary():
    """Print day trading configuration summary"""
    print("=" * 80)
    print("DAY TRADING CONFIGURATION")
    print("=" * 80)
    print(f"\nLLM Settings:")
    print(f"  Deep Think: {DAY_TRADING_CONFIG['deep_think_llm']}")
    print(f"  Quick Think: {DAY_TRADING_CONFIG['quick_think_llm']}")
    print(f"\nDebate Settings:")
    print(f"  Max Debate Rounds: {DAY_TRADING_CONFIG['max_debate_rounds']} (DISABLED)")
    print(f"  Max Risk Rounds: {DAY_TRADING_CONFIG['max_risk_discuss_rounds']}")
    print(f"\nAnalysts Enabled:")
    for analyst in DAY_TRADING_ANALYSTS:
        print(f"  - {analyst.capitalize()}")
    print(f"\nData Sources:")
    for category, vendor in DAY_TRADING_CONFIG['data_vendors'].items():
        print(f"  {category}: {vendor}")
    print(f"\nHolding Periods:")
    for period, config in INTRADAY_PERIODS.items():
        print(f"  {period}: BUY >= {config['buy_threshold']}%, SELL <= {config['sell_threshold']}%")
    print(f"\nTrading Rules:")
    print(f"  Timeframe: {DAY_TRADING_RULES['timeframe']}")
    print(f"  Min Volume: {DAY_TRADING_RULES['min_volume']:,}")
    print(f"  No Overnight: {DAY_TRADING_RULES['no_overnight']}")
    print(f"  Avoid First 15min: {DAY_TRADING_RULES['avoid_first_15min']}")
    print(f"  Avoid Last 15min: {DAY_TRADING_RULES['avoid_last_15min']}")
    print("=" * 80)


if __name__ == "__main__":
    print_config_summary()
