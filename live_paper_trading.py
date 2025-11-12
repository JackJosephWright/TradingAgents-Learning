#!/usr/bin/env python3
"""
Live Paper Trading with Alpaca
Runs TradingAgents in real-time during market hours (9:30 AM - 1:30 PM ET)
Uses Alpaca Paper Trading API to execute actual trades
"""

import os
import sys
import time
import json
from datetime import datetime, timedelta
from pytz import timezone
from dotenv import load_dotenv

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("=" * 80)
print("LIVE PAPER TRADING - ALPACA + TRADINGAGENTS")
print("=" * 80)

# Load environment
load_dotenv()

# Import Alpaca
try:
    from alpaca.trading.client import TradingClient
    from alpaca.trading.requests import MarketOrderRequest, GetOrdersRequest
    from alpaca.trading.enums import OrderSide, TimeInForce, QueryOrderStatus
except ImportError:
    print("[ERROR] Alpaca SDK not installed. Run: pip install alpaca-py")
    sys.exit(1)

# Import our trading system
from day_trading_config import (
    DAY_TRADING_CONFIG,
    DAY_TRADING_ANALYSTS,
    DAY_TRADING_STOCKS
)
from tradingagents.graph.trading_graph import TradingAgentsGraph

# Eastern Time Zone
ET = timezone('US/Eastern')

# Trading Configuration
TRADING_CONFIG = {
    "start_time": "09:30",  # Market open
    "end_time": "13:30",    # End trading at 1:30 PM
    "decision_interval_minutes": 30,  # Make decisions every 30 minutes
    "stocks_to_trade": ["AAPL", "TSLA", "SPY"],  # High liquidity stocks
    "position_size_usd": 1000,  # $1000 per position
    "max_positions": 3,  # Max 3 concurrent positions
}


class LivePaperTrader:
    """Manages live paper trading with Alpaca"""

    def __init__(self):
        # Initialize Alpaca client
        api_key = os.getenv("ALPACA_API_KEY")
        secret_key = os.getenv("ALPACA_SECRET_KEY")

        if not api_key or not secret_key:
            raise ValueError("Alpaca API keys not found in .env")

        self.client = TradingClient(api_key, secret_key, paper=True)

        # Initialize TradingAgents
        self.ta = TradingAgentsGraph(
            selected_analysts=DAY_TRADING_ANALYSTS,
            debug=False,
            config=DAY_TRADING_CONFIG
        )

        # Track trades
        self.trades_log = []
        self.active_positions = {}

        print("\n[INIT] Alpaca Paper Trading Client initialized")
        self.print_account_info()

    def print_account_info(self):
        """Print account balance and buying power"""
        account = self.client.get_account()
        print(f"\n[ACCOUNT] Paper Trading Account:")
        print(f"  Cash: ${float(account.cash):,.2f}")
        print(f"  Buying Power: ${float(account.buying_power):,.2f}")
        print(f"  Portfolio Value: ${float(account.portfolio_value):,.2f}")

    def is_market_open(self):
        """Check if market is currently open"""
        clock = self.client.get_clock()
        return clock.is_open

    def get_current_price(self, symbol):
        """Get current price for a symbol"""
        try:
            from alpaca.data.historical import StockHistoricalDataClient
            from alpaca.data.requests import StockLatestQuoteRequest

            data_client = StockHistoricalDataClient(
                os.getenv("ALPACA_API_KEY"),
                os.getenv("ALPACA_SECRET_KEY")
            )

            request = StockLatestQuoteRequest(symbol_or_symbols=symbol)
            quote = data_client.get_stock_latest_quote(request)

            if symbol in quote:
                return float(quote[symbol].ask_price)
            return None
        except Exception as e:
            print(f"  [ERROR] Failed to get price for {symbol}: {e}")
            return None

    def get_position(self, symbol):
        """Get current position for a symbol"""
        try:
            position = self.client.get_open_position(symbol)
            return {
                "symbol": symbol,
                "qty": int(position.qty),
                "avg_entry_price": float(position.avg_entry_price),
                "current_price": float(position.current_price),
                "unrealized_pl": float(position.unrealized_pl),
                "unrealized_plpc": float(position.unrealized_plpc) * 100
            }
        except:
            return None

    def place_order(self, symbol, side, qty):
        """Place a market order"""
        try:
            order_data = MarketOrderRequest(
                symbol=symbol,
                qty=qty,
                side=OrderSide.BUY if side == "BUY" else OrderSide.SELL,
                time_in_force=TimeInForce.DAY
            )

            order = self.client.submit_order(order_data)
            print(f"  [ORDER] {side} {qty} shares of {symbol} - Order ID: {order.id}")
            return order
        except Exception as e:
            print(f"  [ERROR] Failed to place order: {e}")
            return None

    def make_trading_decision(self, symbol):
        """Use TradingAgents to make a trading decision"""
        print(f"\n  [{symbol}] Analyzing with TradingAgents...")

        try:
            # Use today's date
            today = datetime.now(ET).strftime("%Y-%m-%d")

            start_time = time.time()
            final_state, decision = self.ta.propagate(symbol, today)
            elapsed = time.time() - start_time

            print(f"  [{symbol}] Decision: {decision} (took {elapsed:.1f}s)")

            return decision
        except Exception as e:
            print(f"  [{symbol}] FAILED: {e}")
            return "HOLD"

    def execute_decision(self, symbol, decision):
        """Execute a trading decision"""
        current_position = self.get_position(symbol)
        current_price = self.get_current_price(symbol)

        if not current_price:
            print(f"  [{symbol}] Cannot get price, skipping")
            return

        print(f"  [{symbol}] Current price: ${current_price:.2f}")

        # Calculate position size
        position_value = TRADING_CONFIG["position_size_usd"]
        qty = int(position_value / current_price)

        if qty < 1:
            print(f"  [{symbol}] Position size too small, skipping")
            return

        # Execute based on decision
        if decision == "BUY" and not current_position:
            # Check if we can open new position
            if len(self.active_positions) >= TRADING_CONFIG["max_positions"]:
                print(f"  [{symbol}] Max positions reached, skipping BUY")
                return

            print(f"  [{symbol}] BUYING {qty} shares at ${current_price:.2f}")
            order = self.place_order(symbol, "BUY", qty)

            if order:
                self.active_positions[symbol] = {
                    "entry_time": datetime.now(ET),
                    "entry_price": current_price,
                    "qty": qty,
                    "decision": decision
                }

                self.trades_log.append({
                    "timestamp": datetime.now(ET).isoformat(),
                    "symbol": symbol,
                    "action": "BUY",
                    "qty": qty,
                    "price": current_price,
                    "decision": decision
                })

        elif decision == "SELL" and current_position:
            print(f"  [{symbol}] SELLING {current_position['qty']} shares at ${current_price:.2f}")
            print(f"  [{symbol}] P&L: {current_position['unrealized_plpc']:+.2f}%")

            order = self.place_order(symbol, "SELL", current_position['qty'])

            if order:
                if symbol in self.active_positions:
                    entry_info = self.active_positions.pop(symbol)

                    self.trades_log.append({
                        "timestamp": datetime.now(ET).isoformat(),
                        "symbol": symbol,
                        "action": "SELL",
                        "qty": current_position['qty'],
                        "price": current_price,
                        "entry_price": entry_info.get("entry_price"),
                        "pl_pct": current_position['unrealized_plpc'],
                        "decision": decision
                    })

        elif decision == "HOLD":
            if current_position:
                print(f"  [{symbol}] HOLDING position - P&L: {current_position['unrealized_plpc']:+.2f}%")
            else:
                print(f"  [{symbol}] HOLD - No action")

        else:
            print(f"  [{symbol}] No action for decision: {decision}")

    def close_all_positions(self):
        """Close all open positions at end of trading session"""
        print("\n[CLOSE] Closing all open positions...")

        try:
            positions = self.client.get_all_positions()

            for position in positions:
                symbol = position.symbol
                qty = int(position.qty)
                current_price = float(position.current_price)
                pl_pct = float(position.unrealized_plpc) * 100

                print(f"  [{symbol}] Closing {qty} shares at ${current_price:.2f} (P&L: {pl_pct:+.2f}%)")
                self.place_order(symbol, "SELL", qty)

                self.trades_log.append({
                    "timestamp": datetime.now(ET).isoformat(),
                    "symbol": symbol,
                    "action": "CLOSE",
                    "qty": qty,
                    "price": current_price,
                    "pl_pct": pl_pct,
                    "reason": "End of session"
                })

        except Exception as e:
            print(f"  [ERROR] Failed to close positions: {e}")

        self.active_positions = {}

    def print_session_summary(self):
        """Print summary of trading session"""
        print("\n" + "=" * 80)
        print("SESSION SUMMARY")
        print("=" * 80)

        self.print_account_info()

        if self.trades_log:
            print(f"\nTotal Trades: {len(self.trades_log)}")

            buys = [t for t in self.trades_log if t["action"] == "BUY"]
            sells = [t for t in self.trades_log if t["action"] in ["SELL", "CLOSE"]]

            print(f"  BUY orders: {len(buys)}")
            print(f"  SELL orders: {len(sells)}")

            if sells:
                completed_trades = [t for t in sells if "pl_pct" in t]
                if completed_trades:
                    avg_pl = sum(t["pl_pct"] for t in completed_trades) / len(completed_trades)
                    print(f"  Average P&L: {avg_pl:+.2f}%")

                    winners = [t for t in completed_trades if t["pl_pct"] > 0]
                    print(f"  Win Rate: {len(winners)}/{len(completed_trades)} ({len(winners)/len(completed_trades)*100:.1f}%)")

            # Save log
            log_filename = f"paper_trading_log_{datetime.now(ET).strftime('%Y%m%d')}.json"
            with open(log_filename, 'w') as f:
                json.dump(self.trades_log, f, indent=2)
            print(f"\n[SAVED] Trade log: {log_filename}")
        else:
            print("\nNo trades executed")

        print("=" * 80)

    def run_trading_session(self):
        """Run the trading session from 9:30 AM to 1:30 PM"""
        print(f"\n[START] Trading Session Configuration:")
        print(f"  Start: {TRADING_CONFIG['start_time']} ET")
        print(f"  End: {TRADING_CONFIG['end_time']} ET")
        print(f"  Decision Interval: {TRADING_CONFIG['decision_interval_minutes']} minutes")
        print(f"  Stocks: {', '.join(TRADING_CONFIG['stocks_to_trade'])}")
        print(f"  Position Size: ${TRADING_CONFIG['position_size_usd']}")
        print(f"  Max Positions: {TRADING_CONFIG['max_positions']}")

        # Wait for market to open
        while not self.is_market_open():
            now = datetime.now(ET)
            print(f"\n[WAIT] Market not open yet. Current time: {now.strftime('%I:%M:%S %p')} ET")
            print("  Checking again in 60 seconds...")
            time.sleep(60)

        print("\n[OPEN] Market is open! Starting trading...")

        # Main trading loop
        decision_count = 0

        while True:
            now = datetime.now(ET)
            current_time = now.strftime("%H:%M")

            # Check if we should stop
            if current_time >= TRADING_CONFIG["end_time"]:
                print(f"\n[STOP] Reached end time: {current_time} ET")
                break

            # Check if market is still open
            if not self.is_market_open():
                print(f"\n[STOP] Market closed at {current_time} ET")
                break

            # Make trading decisions
            decision_count += 1
            print(f"\n{'=' * 80}")
            print(f"DECISION ROUND #{decision_count} - {now.strftime('%I:%M:%S %p')} ET")
            print(f"{'=' * 80}")

            for symbol in TRADING_CONFIG["stocks_to_trade"]:
                decision = self.make_trading_decision(symbol)
                self.execute_decision(symbol, decision)

            # Wait for next decision interval
            next_decision = now + timedelta(minutes=TRADING_CONFIG["decision_interval_minutes"])
            wait_seconds = (next_decision - datetime.now(ET)).total_seconds()

            if wait_seconds > 0:
                print(f"\n[WAIT] Next decision at {next_decision.strftime('%I:%M %p')} ET")
                print(f"  Waiting {wait_seconds/60:.1f} minutes...")
                time.sleep(wait_seconds)

        # Close all positions at end of session
        self.close_all_positions()

        # Print summary
        self.print_session_summary()


if __name__ == "__main__":
    try:
        trader = LivePaperTrader()
        trader.run_trading_session()
    except KeyboardInterrupt:
        print("\n\n[STOP] Interrupted by user")
        if 'trader' in locals():
            trader.close_all_positions()
            trader.print_session_summary()
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        import traceback
        traceback.print_exc()
