#!/usr/bin/env python3
"""
Single model test - run one stock with one model configuration
Usage: python single_model_test.py <model_name> <ticker>
"""

import sys
import os
from datetime import datetime
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import json
import time
from dotenv import load_dotenv

load_dotenv()

ANALYSIS_DATE = "2024-05-10"

def main():
    if len(sys.argv) < 3:
        print("Usage: python single_model_test.py <gpt-4o-mini|gpt-4o> <TICKER>")
        sys.exit(1)

    model_name = sys.argv[1]
    ticker = sys.argv[2]

    # Configure model
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = model_name
    config["quick_think_llm"] = model_name
    config["max_debate_rounds"] = 1

    print(f"Testing {ticker} with {model_name}")
    start_time = time.time()

    try:
        ta = TradingAgentsGraph(debug=False, config=config)
        final_state, final_decision = ta.propagate(ticker, ANALYSIS_DATE)

        result = {
            "model": model_name,
            "ticker": ticker,
            "decision": final_decision,
            "time": time.time() - start_time
        }

        print(json.dumps(result))

    except Exception as e:
        result = {
            "model": model_name,
            "ticker": ticker,
            "decision": "ERROR",
            "error": str(e),
            "time": time.time() - start_time
        }
        print(json.dumps(result), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
