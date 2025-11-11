#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration Experimentation Suite
Tests different agent configurations to reduce bearish bias
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
TEST_STOCKS = ["NVDA", "JPM", "WMT"]  # Stocks we know the actual outcomes for

# Known actual returns for validation
ACTUAL_RETURNS = {
    "NVDA": +109.36,  # Should be BUY
    "JPM": +62.90,    # Should be BUY
    "WMT": +70.24,    # Should be BUY
}

# Configuration variants to test
CONFIGURATIONS = [
    {
        "name": "Baseline",
        "description": "Current default configuration",
        "config_overrides": {},
        "prompt_modifications": None
    },
    {
        "name": "More Debate Rounds",
        "description": "Increase debate rounds to 2 for more thorough analysis",
        "config_overrides": {
            "max_debate_rounds": 2,
        },
        "prompt_modifications": None
    },
    {
        "name": "Pro-Growth Bias",
        "description": "Modify prompts to favor growth opportunities in bull markets",
        "config_overrides": {},
        "prompt_modifications": {
            "research_manager_addition": "\n\nIMPORTANT: We are currently in a strong bull market period. When evaluating the debate, give extra weight to growth potential and positive momentum indicators. Be cautious about being overly bearish in a rising market environment."
        }
    },
    {
        "name": "Balanced Decision",
        "description": "Explicitly instruct equal weighting of bull/bear arguments",
        "config_overrides": {},
        "prompt_modifications": {
            "research_manager_addition": "\n\nIMPORTANT: Give equal weight to both bull and bear arguments. Do not favor one side over the other unless the evidence is overwhelmingly one-sided. If uncertain, prefer HOLD over extreme positions."
        }
    },
    {
        "name": "High Conviction Only",
        "description": "Only recommend BUY/SELL with strong conviction, otherwise HOLD",
        "config_overrides": {},
        "prompt_modifications": {
            "research_manager_addition": "\n\nIMPORTANT: Only recommend BUY or SELL if you have HIGH CONVICTION based on the evidence. If the debate is close or uncertain, recommend HOLD. HOLD is a perfectly valid strategy."
        }
    },
]


def analyze_stock_with_config(ticker, date, config_variant, test_id):
    """
    Analyze a stock with a specific configuration variant
    """
    print(f"\n{'='*80}")
    print(f"Configuration: {config_variant['name']}")
    print(f"Stock: {ticker}")
    print(f"Date: {date}")
    print(f"{'='*80}\n")

    # Configure with overrides
    config = DEFAULT_CONFIG.copy()
    config.update(config_variant["config_overrides"])
    config["memory_prefix"] = f"test_{test_id}_{ticker}_{config_variant['name'].replace(' ', '_')}"

    start_time = time.time()

    try:
        # Initialize with this configuration
        ta = TradingAgentsGraph(debug=True, config=config)

        # Apply prompt modifications if specified
        if config_variant["prompt_modifications"]:
            # Note: Prompt modification would require deeper integration
            # For now, we'll test what we can with config changes
            pass

        # Run analysis
        final_state, final_decision = ta.propagate(ticker, date)

        analysis_time = time.time() - start_time

        # Grade the decision
        actual_return = ACTUAL_RETURNS[ticker]
        if actual_return > 20:  # Strong positive return
            correct_decision = "BUY"
        elif actual_return < -10:  # Negative return
            correct_decision = "SELL"
        else:
            correct_decision = "HOLD"

        is_correct = (final_decision == correct_decision)

        # Scoring
        if is_correct:
            grade = "A"
            score = 100
        elif final_decision == "HOLD" and correct_decision == "BUY":
            grade = "C"
            score = 50  # Too conservative but not wrong direction
        elif final_decision == "SELL" and correct_decision == "BUY":
            grade = "F"
            score = 0  # Wrong direction
        else:
            grade = "D"
            score = 25

        result = {
            "config_name": config_variant["name"],
            "ticker": ticker,
            "date": date,
            "decision": final_decision,
            "correct_decision": correct_decision,
            "actual_return": actual_return,
            "is_correct": is_correct,
            "grade": grade,
            "score": score,
            "analysis_time": analysis_time,
            "success": True
        }

        # Extract key insights
        if "investment_plan" in final_state:
            result["investment_plan"] = final_state["investment_plan"][:500]

        print(f"\n[RESULT] {config_variant['name']} -> {ticker}: {final_decision}")
        print(f"  Correct Decision: {correct_decision} | Grade: {grade}")
        print(f"  Actual Return: {actual_return:+.2f}%")
        print(f"  Time: {analysis_time:.1f}s")

        return result

    except Exception as e:
        print(f"[ERROR] {config_variant['name']} failed on {ticker}: {str(e)}")
        return {
            "config_name": config_variant["name"],
            "ticker": ticker,
            "date": date,
            "decision": "ERROR",
            "error": str(e),
            "analysis_time": time.time() - start_time,
            "success": False
        }


def run_configuration_experiments():
    """
    Main experiment runner
    """
    print("="*80)
    print("CONFIGURATION EXPERIMENTATION SUITE")
    print("="*80)
    print(f"\nAnalysis Date: {ANALYSIS_DATE}")
    print(f"Test Stocks: {', '.join(TEST_STOCKS)}")
    print(f"Configurations to Test: {len(CONFIGURATIONS)}")
    print()

    for config in CONFIGURATIONS:
        print(f"  - {config['name']}: {config['description']}")

    all_results = []
    test_id = int(time.time())
    print(f"\nTest ID: {test_id}")

    # Run experiments
    total_tests = len(TEST_STOCKS) * len(CONFIGURATIONS)
    current_test = 0

    for config_variant in CONFIGURATIONS:
        print(f"\n{'#'*80}")
        print(f"# TESTING CONFIGURATION: {config_variant['name']}")
        print(f"# {config_variant['description']}")
        print(f"{'#'*80}")

        config_results = []

        for ticker in TEST_STOCKS:
            current_test += 1
            print(f"\nProgress: {current_test}/{total_tests}")

            result = analyze_stock_with_config(ticker, ANALYSIS_DATE, config_variant, test_id)
            all_results.append(result)
            config_results.append(result)

            # Brief pause between tests
            print("\nWaiting 3 seconds before next test...")
            time.sleep(3)

        # Configuration summary
        successful = [r for r in config_results if r["success"]]
        if successful:
            avg_score = sum(r["score"] for r in successful) / len(successful)
            accuracy = sum(1 for r in successful if r["is_correct"]) / len(successful) * 100
            print(f"\n[CONFIG SUMMARY] {config_variant['name']}")
            print(f"  Accuracy: {accuracy:.1f}% ({sum(1 for r in successful if r['is_correct'])}/{len(successful)})")
            print(f"  Average Score: {avg_score:.1f}/100")

    # Build comprehensive summary
    print(f"\n{'='*80}")
    print("EXPERIMENT SUMMARY")
    print(f"{'='*80}\n")

    # Group by configuration
    by_config = {}
    for result in all_results:
        if result["success"]:
            config_name = result["config_name"]
            if config_name not in by_config:
                by_config[config_name] = []
            by_config[config_name].append(result)

    # Display comparison
    print("\nConfiguration Performance:\n")
    print(f"{'Configuration':<25} {'Accuracy':<12} {'Avg Score':<12} {'Decisions'}")
    print("-" * 80)

    config_rankings = []
    for config_name, results in by_config.items():
        accuracy = sum(1 for r in results if r["is_correct"]) / len(results) * 100
        avg_score = sum(r["score"] for r in results) / len(results)
        decisions = f"{sum(1 for r in results if r['decision']=='BUY')}B / " \
                   f"{sum(1 for r in results if r['decision']=='HOLD')}H / " \
                   f"{sum(1 for r in results if r['decision']=='SELL')}S"

        print(f"{config_name:<25} {accuracy:>6.1f}%      {avg_score:>6.1f}/100    {decisions}")

        config_rankings.append({
            "config_name": config_name,
            "accuracy": accuracy,
            "avg_score": avg_score,
            "decisions": decisions
        })

    # Rank configurations
    config_rankings.sort(key=lambda x: x["avg_score"], reverse=True)

    print(f"\n{'='*80}")
    print("BEST CONFIGURATIONS (Ranked by Score)")
    print(f"{'='*80}\n")

    for i, ranking in enumerate(config_rankings, 1):
        print(f"{i}. {ranking['config_name']}")
        print(f"   Accuracy: {ranking['accuracy']:.1f}% | Score: {ranking['avg_score']:.1f}/100")
        print(f"   Decisions: {ranking['decisions']}\n")

    # Save results
    output = {
        "analysis_date": ANALYSIS_DATE,
        "timestamp": datetime.now().isoformat(),
        "test_id": test_id,
        "configurations_tested": [c["name"] for c in CONFIGURATIONS],
        "stocks_tested": TEST_STOCKS,
        "actual_returns": ACTUAL_RETURNS,
        "all_results": all_results,
        "config_rankings": config_rankings,
    }

    output_file = "config_experiment_results.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"\n{'='*80}")
    print("EXPERIMENTS COMPLETE")
    print(f"{'='*80}")
    print(f"\nResults saved to: {output_file}")
    print(f"Total tests run: {len([r for r in all_results if r['success']])}")
    print(f"Total time: {sum(r['analysis_time'] for r in all_results if r['success']):.1f} seconds")

    # Recommendations
    print(f"\n{'='*80}")
    print("RECOMMENDATIONS")
    print(f"{'='*80}\n")

    best_config = config_rankings[0]
    print(f"Best Configuration: {best_config['config_name']}")
    print(f"  - Achieved {best_config['accuracy']:.1f}% accuracy")
    print(f"  - Average score: {best_config['avg_score']:.1f}/100")
    print(f"  - Decision distribution: {best_config['decisions']}")

    baseline = next((c for c in config_rankings if c["config_name"] == "Baseline"), None)
    if baseline and best_config["config_name"] != "Baseline":
        improvement = best_config["avg_score"] - baseline["avg_score"]
        print(f"\nImprovement over Baseline: +{improvement:.1f} points")


if __name__ == "__main__":
    run_configuration_experiments()
