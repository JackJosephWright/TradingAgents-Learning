# Day Trading Setup Guide

## What Changed?

We've streamlined TradingAgents for **day trading** with these key modifications:

### ✂️ Removed
- **Fundamentals Analyst** - Not relevant for intraday trading
- **Bull/Bear Debate System** - Too slow for day trading (set `max_debate_rounds = 0`)
- **Social Media Analyst** - Optional, removed for speed

### ➕ Added
- **Alpaca API Integration** - Intraday minute-level data
- **VWAP Indicator** - Critical for day trading
- **Intraday Technical Indicators** - EMA-9/21, RSI, ATR on 5-min charts
- **Day Trading Configuration** - Optimized thresholds and timeframes

### ⚡ Speed Improvements
- Before: ~4 minutes per decision (with debate)
- After: ~30-60 seconds per decision
- **~4-8x faster**

---

## Quick Start

### 1. Get Alpaca API Keys (Free)

1. Sign up at https://alpaca.markets
2. Go to Dashboard → Paper Trading → View API Keys
3. Copy your API Key and Secret Key

### 2. Update .env File

```bash
# Add these lines to your .env file:
ALPACA_API_KEY=your_api_key_here
ALPACA_SECRET_KEY=your_secret_key_here
```

### 3. Install Alpaca SDK

```bash
cd /mnt/c/Users/iorda/OneDrive/Documents/GitHub/TradingAgents-Learning
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install alpaca-py
```

### 4. Run Test Script

```bash
python test_day_trading.py
```

This will:
- Test Alpaca API connection
- Fetch 5-minute bars for AAPL
- Calculate intraday indicators (VWAP, EMA, RSI, ATR)
- Run TradingAgents with simplified config

---

## Day Trading Configuration

The new `day_trading_config.py` includes:

### Analysts (Simplified)
```python
DAY_TRADING_ANALYSTS = [
    "market",  # Technical analysis only
    # "social" - REMOVED for speed
    # "news" - REMOVED (not relevant intraday)
    # "fundamentals" - REMOVED (not relevant intraday)
]
```

### No Debate
```python
"max_debate_rounds": 0,  # Skip bull/bear debate
"max_risk_discuss_rounds": 1,  # Single risk check
```

### Intraday Holding Periods
```python
INTRADAY_PERIODS = {
    "30min": {"buy_threshold": 0.3%, "sell_threshold": -0.2%},
    "1hr":   {"buy_threshold": 0.5%, "sell_threshold": -0.3%},
    "2hr":   {"buy_threshold": 0.8%, "sell_threshold": -0.5%},
    "4hr":   {"buy_threshold": 1.2%, "sell_threshold": -0.8%}
}
```

### Day Trading Rules
```python
{
    "timeframe": "5Min",  # 5-minute candles
    "min_volume": 1000000,  # Only liquid stocks
    "no_overnight": True,  # Close by 4 PM
    "avoid_first_15min": True,  # Skip 9:30-9:45
    "avoid_last_15min": True,  # Skip 3:45-4:00
}
```

---

## New Files

### Core Files
- `day_trading_config.py` - Configuration for day trading
- `test_day_trading.py` - Test script
- `tradingagents/dataflows/alpaca_intraday.py` - Alpaca API integration
- `tradingagents/agents/utils/intraday_tools.py` - Intraday data tools

### Updated Files
- `.env.example` - Added Alpaca keys template
- This guide (`DAY_TRADING_SETUP.md`)

---

## Architecture

### Before (Weekly Trading)
```
Market → Social → News → Fundamentals
  ↓
Bull ↔ Bear (1-3 debate rounds)
  ↓
Research Manager
  ↓
Trader
  ↓
Risk Team (Risky → Safe → Neutral)
  ↓
Risk Manager → Decision

Time: ~4 minutes
```

### After (Day Trading)
```
Market Analyst
  ↓
(NO DEBATE)
  ↓
Research Manager
  ↓
Trader
  ↓
Risk Team (Single round)
  ↓
Risk Manager → Decision

Time: ~30-60 seconds
```

---

## Usage Example

### Basic Test
```python
from day_trading_config import DAY_TRADING_CONFIG, DAY_TRADING_ANALYSTS
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Initialize with day trading config
ta = TradingAgentsGraph(
    selected_analysts=DAY_TRADING_ANALYSTS,  # Only market
    debug=False,
    config=DAY_TRADING_CONFIG
)

# Analyze a stock
final_state, decision = ta.propagate("AAPL", "2024-03-15")
print(f"Decision: {decision}")
```

### Fetch Intraday Data
```python
from tradingagents.dataflows.alpaca_intraday import (
    get_alpaca_intraday_bars,
    calculate_intraday_indicators
)

# Get 5-minute bars
df = get_alpaca_intraday_bars("AAPL", timeframe="5Min", date="2024-03-15")

# Calculate indicators
df = calculate_intraday_indicators(df)

# Check signals
latest = df.iloc[-1]
print(f"Close: ${latest['close']:.2f}")
print(f"VWAP: ${latest['vwap']:.2f}")
print(f"RSI: {latest['rsi']:.1f}")
```

---

## Next Steps

### 1. Test Current Setup ✓
```bash
python test_day_trading.py
```

### 2. Create Intraday Backtest
Modify `test_rolling_windows_pilot.py` to:
- Use intraday data instead of daily
- Test 1 full trading day (9:30 AM - 4:00 PM)
- Make decisions every 30 minutes or 1 hour
- Measure: win rate, avg gain/loss, Sharpe ratio

### 3. Integrate Intraday into Market Analyst
Update `tradingagents/agents/analysts/market_analyst.py` to:
- Accept intraday data
- Use VWAP instead of daily SMAs
- Focus on 9-EMA, 21-EMA, RSI-14

### 4. Run Full Pilot
- Test 10 trading days
- High-volume stocks (SPY, AAPL, TSLA, NVDA)
- Compare 30min, 1hr, 2hr holding periods
- Target: >55% accuracy

---

## Day Trading Best Practices

### Stocks to Trade
Focus on high-volume, liquid stocks:
- **SPY** - S&P 500 ETF (highest volume)
- **QQQ** - NASDAQ ETF
- **AAPL, MSFT, NVDA, TSLA** - Tech megacaps
- **AMD, META, GOOGL, AMZN** - High volatility

### Time Windows
- **Avoid 9:30-9:45 AM** - Opening volatility
- **Best: 10:00 AM - 3:30 PM** - Stable trends
- **Avoid 3:45-4:00 PM** - Closing volatility

### Risk Management
- **Max 0.5-1% risk per trade**
- **Use ATR for stop-loss** - 1-2x ATR
- **Close all positions by 4:00 PM** - No overnight risk
- **Max 3-5 trades per day** - Avoid overtrading

---

## Troubleshooting

### "Alpaca API keys not found"
- Add `ALPACA_API_KEY` and `ALPACA_SECRET_KEY` to `.env`
- Make sure there are no spaces around the `=` sign

### "No data returned"
- Check if date is a weekday (markets closed on weekends)
- Ensure date is not today (use yesterday or earlier)
- Verify API keys are correct

### "Module 'alpaca' not found"
```bash
pip install alpaca-py
```

### Still too slow?
- Verify `max_debate_rounds: 0`
- Check only "market" in `selected_analysts`
- Use `gpt-4o-mini` for all LLMs (not `o4-mini`)

---

## Performance Goals

| Metric | Target | Notes |
|--------|--------|-------|
| Win Rate | >55% | % of profitable trades |
| Avg Gain | >0.5% | Per winning trade |
| Avg Loss | <0.3% | Per losing trade |
| Profit Factor | >2.0 | Total gains / Total losses |
| Decision Time | <60s | Fast enough for intraday |
| Trades/Day | 3-5 | Avoid overtrading |

---

## Questions?

Open an issue or check the main README for contact info.

Good luck day trading! 📈
