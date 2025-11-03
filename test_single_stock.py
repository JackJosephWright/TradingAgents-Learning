#!/usr/bin/env python3
"""
Single Stock Test - Verify system works
"""

import sys
import os
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)

# Load environment variables
load_dotenv()

print("="*70, flush=True)
print("SINGLE STOCK TEST", flush=True)
print("="*70, flush=True)

TICKER = "NVDA"
DATE = "2024-05-10"

print(f"\nTicker: {TICKER}", flush=True)
print(f"Date: {DATE}", flush=True)

print("\nInitializing TradingAgents...", flush=True)
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"
config["quick_think_llm"] = "gpt-4o-mini"
config["max_debate_rounds"] = 1

ta = TradingAgentsGraph(debug=False, config=config)
print("[SUCCESS] Initialized!", flush=True)

print(f"\nAnalyzing {TICKER}...", flush=True)
print("(This will take ~4 minutes)\n", flush=True)

try:
    final_state, decision = ta.propagate(TICKER, DATE)

    print(f"\n{'='*70}", flush=True)
    print(f"RESULT: {decision}", flush=True)
    print(f"{'='*70}", flush=True)

    print("\n[SUCCESS] Analysis complete!", flush=True)

except Exception as e:
    print(f"\n[ERROR] {str(e)}", flush=True)
