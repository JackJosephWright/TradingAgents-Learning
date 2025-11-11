#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Technical-Focused Variant Testing
Tests technical-weighted decision making with reduced LLM debate
"""

import os
import sys
import shutil

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("="*80, flush=True)
print("TECHNICAL-FOCUSED VARIANT TEST", flush=True)
print("="*80, flush=True)

from datetime import datetime
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import json
import time
from dotenv import load_dotenv

print("\n[INIT] Loading environment...", flush=True)
load_dotenv()

# Test parameters
ANALYSIS_DATE = "2024-05-10"
TEST_STOCKS = ["WMT", "NVDA", "JPM"]  # All 3 stocks from our analysis

# Known outcomes
ACTUAL_RETURNS = {
    "NVDA": +109.36,  # Should be BUY
    "JPM": +62.90,    # Should be BUY
    "WMT": +70.24,    # Should be BUY
}

print(f"\n[CONFIG] Testing {len(TEST_STOCKS)} stocks", flush=True)
print(f"[CONFIG] Focus: Technical indicators > LLM debate", flush=True)
print(f"[CONFIG] Expected: All BUY decisions\n", flush=True)

# Back up original
print("[SETUP] Backing up original research_manager.py...", flush=True)
original_file = "tradingagents/agents/managers/research_manager.py"
backup_file = "research_manager_tech_backup.py"
shutil.copy2(original_file, backup_file)
print("[SETUP] Backup complete\n", flush=True)

results = []

try:
    # Swap to technical variant
    print("="*80, flush=True)
    print("SWAPPING TO TECHNICAL-FOCUSED RESEARCH MANAGER", flush=True)
    print("="*80, flush=True)

    shutil.copy2("tradingagents/agents/managers/research_manager_technical.py", original_file)
    print("[SETUP] Technical variant installed\n", flush=True)

    # Reload modules
    print("[SETUP] Reloading modules...", flush=True)
    import importlib
    import tradingagents.agents.managers.research_manager
    importlib.reload(tradingagents.agents.managers.research_manager)
    import tradingagents.agents
    importlib.reload(tradingagents.agents)
    print("[SETUP] Reload complete\n", flush=True)

    # Test each stock
    for i, ticker in enumerate(TEST_STOCKS, 1):
        print("="*80, flush=True)
        print(f"TEST {i}/{len(TEST_STOCKS)}: {ticker}", flush=True)
        print("="*80, flush=True)

        actual_return = ACTUAL_RETURNS[ticker]
        correct_decision = "BUY" if actual_return > 20 else "SELL" if actual_return < -10 else "HOLD"

        print(f"[INFO] Stock: {ticker}", flush=True)
        print(f"[INFO] Actual return: {actual_return:+.2f}%", flush=True)
        print(f"[INFO] Expected decision: {correct_decision}\n", flush=True)

        # Configure with reduced debate
        config = DEFAULT_CONFIG.copy()
        config["memory_prefix"] = f"tech_test_{int(time.time())}_{ticker}"
        config["max_debate_rounds"] = 1  # Keep 1 round for context, but technical analysis dominates

        print(f"[TEST] Initializing technical-focused analysis...", flush=True)
        start = time.time()

        ta = TradingAgentsGraph(debug=False, config=config)

        print(f"[TEST] Running analysis on {ticker}...", flush=True)
        final_state, decision = ta.propagate(ticker, ANALYSIS_DATE)

        exec_time = time.time() - start

        # Grade the decision
        is_correct = (decision == correct_decision)
        if is_correct:
            grade, score = "A", 100
        elif decision == "HOLD" and correct_decision == "BUY":
            grade, score = "C", 50
        elif decision == "SELL" and correct_decision == "BUY":
            grade, score = "F", 0
        else:
            grade, score = "D", 25

        result = {
            "ticker": ticker,
            "decision": decision,
            "correct_decision": correct_decision,
            "actual_return": actual_return,
            "is_correct": is_correct,
            "grade": grade,
            "score": score,
            "time": exec_time
        }
        results.append(result)

        # Display result
        status = "CORRECT" if is_correct else "WRONG"
        symbol = "+" if is_correct else "X"

        print(f"\n[RESULT] {ticker}: {decision} (expected {correct_decision})", flush=True)
        print(f"[RESULT] Status: {status} ({symbol}) | Grade: {grade} | Score: {score}/100", flush=True)
        print(f"[RESULT] Time: {exec_time:.1f}s\n", flush=True)

        if i < len(TEST_STOCKS):
            print(f"Waiting 3 seconds before next test...\n", flush=True)
            time.sleep(3)

finally:
    # Restore original
    print("="*80, flush=True)
    print("[CLEANUP] Restoring original research_manager.py...", flush=True)
    shutil.copy2(backup_file, original_file)
    os.remove(backup_file)
    print("[CLEANUP] Restoration complete", flush=True)

# Summary
print("\n" + "="*80, flush=True)
print("TECHNICAL-FOCUSED VARIANT RESULTS", flush=True)
print("="*80, flush=True)

total_tests = len(results)
correct_tests = sum(1 for r in results if r["is_correct"])
accuracy = (correct_tests / total_tests * 100) if total_tests > 0 else 0
avg_score = sum(r["score"] for r in results) / total_tests if total_tests > 0 else 0

print(f"\nAccuracy: {accuracy:.1f}% ({correct_tests}/{total_tests})", flush=True)
print(f"Average Score: {avg_score:.1f}/100", flush=True)
print(f"\nDetailed Results:\n", flush=True)

for result in results:
    symbol = "+" if result["is_correct"] else "X"
    print(f"  {result['ticker']:<6} {result['decision']:>6} (expected {result['correct_decision']})  "
          f"Grade: {result['grade']}  {symbol:>3}", flush=True)

# Compare to known baseline
print(f"\n" + "-"*80, flush=True)
print("COMPARISON TO BASELINE:", flush=True)
print(f"-"*80, flush=True)
print("\nPath C (Original, LLM-debate heavy):", flush=True)
print("  NVDA: SELL (X)  |  JPM: HOLD (X)  |  WMT: SELL (X)  |  Accuracy: 0%", flush=True)
print("\nPath B (Original, today's run):", flush=True)
print("  WMT: BUY (+)  |  Accuracy: 100% (but only 1 stock)", flush=True)
print("\nCurrent (Technical-focused):", flush=True)
results_line = "  " + "  |  ".join([f"{r['ticker']}: {r['decision']} ({'+'  if r['is_correct'] else 'X'})"
                                     for r in results])
print(f"{results_line}  |  Accuracy: {accuracy:.0f}%", flush=True)

# Analysis
print(f"\n" + "="*80, flush=True)
print("ANALYSIS", flush=True)
print("="*80, flush=True)

if accuracy == 100:
    print("\n[SUCCESS] Technical-focused variant achieved 100% accuracy!", flush=True)
    print("Technical indicators provide more consistent, correct decisions.", flush=True)
elif accuracy >= 67:
    print(f"\n[GOOD] Technical variant achieved {accuracy:.0f}% accuracy - significant improvement!", flush=True)
    print("Technical focus reduces inconsistency compared to debate-heavy approach.", flush=True)
elif accuracy >= 33:
    print(f"\n[MIXED] Technical variant achieved {accuracy:.0f}% accuracy - some improvement.", flush=True)
    print("Technical indicators help but may need further tuning.", flush=True)
else:
    print(f"\n[POOR] Technical variant only achieved {accuracy:.0f}% accuracy.", flush=True)
    print("Technical weighting alone may not solve the consistency problem.", flush=True)

# Save results
output = {
    "timestamp": datetime.now().isoformat(),
    "variant": "Technical-Focused",
    "accuracy": accuracy,
    "avg_score": avg_score,
    "results": results,
    "comparison": {
        "path_c_accuracy": 0.0,
        "path_b_accuracy": 100.0,  # WMT only
        "current_accuracy": accuracy
    }
}

output_file = "technical_variant_results.json"
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"\n[SAVE] Results saved to: {output_file}", flush=True)

print("\n" + "="*80, flush=True)
print("TEST COMPLETE", flush=True)
print("="*80, flush=True)

# Recommendations
if accuracy == 100:
    print("\nRECOMMENDATION: Adopt technical-focused approach for production use!", flush=True)
elif accuracy >= 67:
    print("\nRECOMMENDATION: Technical focus shows promise - consider hybrid approach.", flush=True)
else:
    print("\nRECOMMENDATION: May need additional strategies beyond technical weighting.", flush=True)
