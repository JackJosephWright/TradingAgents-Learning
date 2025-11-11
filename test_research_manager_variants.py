#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Research Manager Variant Testing
Tests original vs balanced vs pro-growth research managers
"""

import os
import sys
import shutil
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

load_dotenv()

# Test configuration
ANALYSIS_DATE = "2024-05-10"
TEST_STOCKS = ["NVDA", "JPM", "WMT"]

# Known outcomes
ACTUAL_RETURNS = {
    "NVDA": +109.36,  # Should be BUY
    "JPM": +62.90,    # Should be BUY
    "WMT": +70.24,    # Should be BUY
}

RESEARCH_MANAGER_VARIANTS = [
    {
        "name": "Original",
        "file": "tradingagents/agents/managers/research_manager.py",
        "backup": "research_manager_original_backup.py",
        "description": "Default research manager (bearish bias suspected)"
    },
    {
        "name": "Balanced",
        "file": "tradingagents/agents/managers/research_manager.py",
        "source": "tradingagents/agents/managers/research_manager_balanced.py",
        "backup": "research_manager_balanced_test.py",
        "description": "Equal weight to bull/bear arguments"
    },
    {
        "name": "Pro-Growth",
        "file": "tradingagents/agents/managers/research_manager.py",
        "source": "tradingagents/agents/managers/research_manager_growth.py",
        "backup": "research_manager_growth_test.py",
        "description": "Favors growth opportunities in bull markets"
    }
]


def swap_research_manager(variant):
    """
    Temporarily swap the research_manager.py file
    """
    target_file = variant["file"]

    # Back up original if this is the first variant
    if variant["name"] == "Original":
        # Just note that we're using the original
        print(f"[SETUP] Using original research_manager.py")
        return True

    # For other variants, copy the new version over
    if "source" in variant:
        try:
            shutil.copy2(variant["source"], target_file)
            print(f"[SETUP] Swapped in {variant['name']} research manager")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to swap research manager: {e}")
            return False

    return False


def restore_original_research_manager():
    """
    Restore the original research_manager.py
    """
    # We'll manually restore at the end
    pass


def analyze_with_variant(ticker, date, variant, test_id):
    """
    Analyze a stock with a specific research manager variant
    """
    print(f"\n{'='*80}")
    print(f"Variant: {variant['name']}")
    print(f"Stock: {ticker}")
    print(f"{'='*80}\n")

    # Configure
    config = DEFAULT_CONFIG.copy()
    config["memory_prefix"] = f"variant_test_{test_id}_{ticker}_{variant['name'].replace(' ', '_').replace('-', '_')}"
    config["max_debate_rounds"] = 1

    start_time = time.time()

    try:
        # Need to reload the module to pick up changes
        import importlib
        import tradingagents.agents.managers.research_manager
        importlib.reload(tradingagents.agents.managers.research_manager)

        # Also reload the agents init to pick up the change
        import tradingagents.agents
        importlib.reload(tradingagents.agents)

        # Initialize trading graph
        ta = TradingAgentsGraph(debug=False, config=config)

        # Run analysis
        final_state, final_decision = ta.propagate(ticker, date)

        analysis_time = time.time() - start_time

        # Grade the decision
        actual_return = ACTUAL_RETURNS[ticker]
        correct_decision = "BUY" if actual_return > 20 else "SELL" if actual_return < -10 else "HOLD"
        is_correct = (final_decision == correct_decision)

        # Scoring
        if is_correct:
            grade, score = "A", 100
        elif final_decision == "HOLD" and correct_decision == "BUY":
            grade, score = "C", 50
        elif final_decision == "SELL" and correct_decision == "BUY":
            grade, score = "F", 0
        else:
            grade, score = "D", 25

        result = {
            "variant": variant["name"],
            "ticker": ticker,
            "decision": final_decision,
            "correct_decision": correct_decision,
            "actual_return": actual_return,
            "is_correct": is_correct,
            "grade": grade,
            "score": score,
            "analysis_time": analysis_time,
            "success": True
        }

        print(f"\n[RESULT] {variant['name']} -> {ticker}: {final_decision}")
        print(f"  Expected: {correct_decision} | Grade: {grade} | Score: {score}/100")
        print(f"  Actual Return: {actual_return:+.2f}%")
        print(f"  Time: {analysis_time:.1f}s")

        return result

    except Exception as e:
        print(f"[ERROR] {variant['name']} failed on {ticker}: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            "variant": variant["name"],
            "ticker": ticker,
            "decision": "ERROR",
            "error": str(e),
            "analysis_time": time.time() - start_time,
            "success": False
        }


def run_variant_tests():
    """
    Main test runner
    """
    print("="*80)
    print("RESEARCH MANAGER VARIANT TESTING")
    print("="*80)
    print(f"\nTest Stocks: {', '.join(TEST_STOCKS)}")
    print(f"Variants: {len(RESEARCH_MANAGER_VARIANTS)}\n")

    for variant in RESEARCH_MANAGER_VARIANTS:
        print(f"  - {variant['name']}: {variant['description']}")

    all_results = []
    test_id = int(time.time())

    # Back up original file
    original_file = "tradingagents/agents/managers/research_manager.py"
    backup_file = "research_manager_original.py.backup"

    print(f"\n[SETUP] Backing up original research_manager.py")
    shutil.copy2(original_file, backup_file)

    try:
        for variant in RESEARCH_MANAGER_VARIANTS:
            print(f"\n{'#'*80}")
            print(f"# TESTING VARIANT: {variant['name']}")
            print(f"# {variant['description']}")
            print(f"{'#'*80}")

            # Swap in this variant
            if not swap_research_manager(variant):
                print(f"[SKIP] Could not set up {variant['name']}, skipping")
                continue

            variant_results = []

            for ticker in TEST_STOCKS:
                result = analyze_with_variant(ticker, ANALYSIS_DATE, variant, test_id)
                all_results.append(result)
                variant_results.append(result)

                # Brief pause
                print("\nWaiting 3 seconds...")
                time.sleep(3)

            # Variant summary
            successful = [r for r in variant_results if r["success"]]
            if successful:
                avg_score = sum(r["score"] for r in successful) / len(successful)
                accuracy = sum(1 for r in successful if r["is_correct"]) / len(successful) * 100
                print(f"\n[VARIANT SUMMARY] {variant['name']}")
                print(f"  Accuracy: {accuracy:.1f}% ({sum(1 for r in successful if r['is_correct'])}/{len(successful)})")
                print(f"  Average Score: {avg_score:.1f}/100")

    finally:
        # Restore original
        print(f"\n[CLEANUP] Restoring original research_manager.py")
        shutil.copy2(backup_file, original_file)
        os.remove(backup_file)

    # Final summary
    print(f"\n{'='*80}")
    print("FINAL RESULTS")
    print(f"{'='*80}\n")

    # Group by variant
    by_variant = {}
    for result in all_results:
        if result["success"]:
            variant_name = result["variant"]
            if variant_name not in by_variant:
                by_variant[variant_name] = []
            by_variant[variant_name].append(result)

    # Display comparison
    print(f"{'Variant':<15} {'Accuracy':<12} {'Avg Score':<12} {'Decisions'}")
    print("-" * 70)

    variant_rankings = []
    for variant_name, results in by_variant.items():
        accuracy = sum(1 for r in results if r["is_correct"]) / len(results) * 100
        avg_score = sum(r["score"] for r in results) / len(results)
        decisions = f"{sum(1 for r in results if r['decision']=='BUY')}B / " \
                   f"{sum(1 for r in results if r['decision']=='HOLD')}H / " \
                   f"{sum(1 for r in results if r['decision']=='SELL')}S"

        print(f"{variant_name:<15} {accuracy:>6.1f}%      {avg_score:>6.1f}/100    {decisions}")

        variant_rankings.append({
            "variant": variant_name,
            "accuracy": accuracy,
            "avg_score": avg_score,
            "decisions": decisions,
            "results": results
        })

    # Rank variants
    variant_rankings.sort(key=lambda x: x["avg_score"], reverse=True)

    print(f"\n{'='*80}")
    print("BEST VARIANT")
    print(f"{'='*80}\n")

    best = variant_rankings[0]
    print(f"🏆 {best['variant']}")
    print(f"   Accuracy: {best['accuracy']:.1f}%")
    print(f"   Score: {best['avg_score']:.1f}/100")
    print(f"   Decisions: {best['decisions']}")

    # Compare to original
    original = next((v for v in variant_rankings if v["variant"] == "Original"), None)
    if original and best["variant"] != "Original":
        improvement = best["avg_score"] - original["avg_score"]
        print(f"\n   Improvement over Original: +{improvement:.1f} points")

    # Save results
    output = {
        "timestamp": datetime.now().isoformat(),
        "test_id": test_id,
        "all_results": all_results,
        "variant_rankings": variant_rankings
    }

    output_file = "research_manager_variant_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"\n{'='*80}")
    print(f"Results saved to: {output_file}")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    run_variant_tests()
