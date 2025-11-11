#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
LLM Model Comparison: GPT-4o-mini vs GPT-4o
Tests how different AI models make trading decisions on the same stocks
"""

import os
import sys
from datetime import datetime
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import json
import time
from dotenv import load_dotenv

# Fix Unicode encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')

# Load environment variables
load_dotenv()

# Test configuration
ANALYSIS_DATE = "2024-05-10"
TEST_STOCKS = ["NVDA", "JPM", "WMT"]  # Stocks where 4o-mini struggled

# Models to compare
MODELS_TO_TEST = [
    {
        "name": "GPT-4o-mini",
        "deep_think_llm": "gpt-4o-mini",
        "quick_think_llm": "gpt-4o-mini",
        "description": "Fast & cost-effective model"
    },
    {
        "name": "GPT-4o",
        "deep_think_llm": "gpt-4o",
        "quick_think_llm": "gpt-4o",
        "description": "Full-power model with better reasoning"
    }
]

def analyze_stock_with_model(ticker, date, model_config, test_id):
    """
    Analyze a stock with a specific model configuration
    """
    print(f"\n{'='*70}")
    print(f"Model: {model_config['name']}")
    print(f"Stock: {ticker}")
    print(f"Date: {date}")
    print(f"{'='*70}\n")

    # Configure model with unique memory prefix to avoid collection conflicts
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = model_config["deep_think_llm"]
    config["quick_think_llm"] = model_config["quick_think_llm"]
    config["max_debate_rounds"] = 1
    config["memory_prefix"] = f"test_{test_id}_{ticker}_{model_config['name'].replace('-', '_').replace(' ', '_')}"

    start_time = time.time()

    try:
        # Initialize with this model with unique memory collections
        ta = TradingAgentsGraph(debug=True, config=config)

        # Run analysis
        final_state, final_decision = ta.propagate(ticker, date)

        analysis_time = time.time() - start_time

        result = {
            "model": model_config["name"],
            "ticker": ticker,
            "date": date,
            "decision": final_decision,
            "analysis_time": analysis_time,
            "success": True
        }

        # Extract key insights
        if "investment_plan" in final_state:
            result["investment_plan"] = final_state["investment_plan"]
        if "market_report" in final_state:
            result["market_report"] = final_state["market_report"][:500]

        print(f"\n[RESULT] {model_config['name']} -> {ticker}: {final_decision}")
        print(f"[TIME] {analysis_time:.1f} seconds")

        return result

    except Exception as e:
        print(f"[ERROR] {model_config['name']} failed on {ticker}: {str(e)}")
        return {
            "model": model_config["name"],
            "ticker": ticker,
            "date": date,
            "decision": "ERROR",
            "error": str(e),
            "analysis_time": time.time() - start_time,
            "success": False
        }

def compare_models():
    """
    Main comparison function
    """
    print("="*70)
    print("LLM MODEL COMPARISON")
    print("="*70)
    print(f"\nAnalysis Date: {ANALYSIS_DATE}")
    print(f"Test Stocks: {', '.join(TEST_STOCKS)}")
    print(f"Models: {len(MODELS_TO_TEST)}")
    print()

    for model_config in MODELS_TO_TEST:
        print(f"  - {model_config['name']}: {model_config['description']}")

    all_results = []

    # Generate unique test ID for this comparison run
    test_id = int(time.time())
    print(f"\nTest ID: {test_id}")

    # Test each stock with each model
    for ticker in TEST_STOCKS:
        print(f"\n{'#'*70}")
        print(f"# TESTING STOCK: {ticker}")
        print(f"{'#'*70}")

        for model_config in MODELS_TO_TEST:
            result = analyze_stock_with_model(ticker, ANALYSIS_DATE, model_config, test_id)
            all_results.append(result)

            # Brief pause between tests
            print("\nWaiting 5 seconds before next test...")
            time.sleep(5)

    # Build comparison summary
    print(f"\n{'='*70}")
    print("COMPARISON SUMMARY")
    print(f"{'='*70}\n")

    # Group by ticker
    by_ticker = {}
    for result in all_results:
        if result["success"]:
            ticker = result["ticker"]
            if ticker not in by_ticker:
                by_ticker[ticker] = []
            by_ticker[ticker].append(result)

    # Display comparison
    for ticker, results in by_ticker.items():
        print(f"\n{ticker}:")
        for result in results:
            print(f"  {result['model']:15} -> {result['decision']:6}  ({result['analysis_time']:.1f}s)")

    # Check agreement
    print(f"\n{'='*70}")
    print("DECISION AGREEMENT ANALYSIS")
    print(f"{'='*70}\n")

    agreements = 0
    disagreements = 0

    for ticker, results in by_ticker.items():
        if len(results) == 2:
            decision1 = results[0]["decision"]
            decision2 = results[1]["decision"]

            if decision1 == decision2:
                agreements += 1
                print(f"[AGREE] {ticker}: AGREE ({decision1})")
            else:
                disagreements += 1
                print(f"[DISAGREE] {ticker}: DISAGREE ({results[0]['model']} says {decision1}, {results[1]['model']} says {decision2})")

    total = agreements + disagreements
    if total > 0:
        agreement_rate = (agreements / total) * 100
        print(f"\nAgreement Rate: {agreement_rate:.1f}% ({agreements}/{total})")
    else:
        print("\n[ERROR] No valid comparisons")

    # Save results
    output = {
        "analysis_date": ANALYSIS_DATE,
        "timestamp": datetime.now().isoformat(),
        "models_tested": [m["name"] for m in MODELS_TO_TEST],
        "stocks_tested": TEST_STOCKS,
        "results": all_results,
        "summary": {
            "by_ticker": by_ticker,
            "agreements": agreements,
            "disagreements": disagreements,
            "agreement_rate": agreement_rate if total > 0 else 0
        }
    }

    output_file = "llm_comparison_results.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n{'='*70}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"\nResults saved to: {output_file}")
    print(f"Total time: {sum(r['analysis_time'] for r in all_results if r['success']):.1f} seconds")

    # Next steps
    print(f"\nNext Steps:")
    print(f"  1. Review detailed decisions in {output_file}")
    print(f"  2. Compare reasoning quality between models")
    print(f"  3. Validate decisions against historical data")
    print(f"  4. Analyze cost vs. quality tradeoffs")

if __name__ == "__main__":
    compare_models()
