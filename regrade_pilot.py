#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Quick Re-grade: Apply moderate thresholds to existing pilot data
"""

import json

# New moderate thresholds
HOLDING_PERIODS = {
    "1mo": {"days": 30, "buy_threshold": 5, "sell_threshold": -3},
    "3mo": {"days": 90, "buy_threshold": 10, "sell_threshold": -7},
    "6mo": {"days": 180, "buy_threshold": 20, "sell_threshold": -12}
}

def grade_decision(decision, actual_return, period_info):
    """Grade a decision based on actual return and holding period thresholds"""
    if actual_return is None:
        return None, None, "N/A"

    buy_threshold = period_info["buy_threshold"]
    sell_threshold = period_info["sell_threshold"]

    if actual_return >= buy_threshold:
        correct_decision = "BUY"
    elif actual_return <= sell_threshold:
        correct_decision = "SELL"
    else:
        correct_decision = "HOLD"

    is_correct = (decision == correct_decision)

    if is_correct:
        grade, score = "A", 100
    elif decision == "HOLD":
        if correct_decision == "BUY":
            grade, score = "C", 50
        else:
            grade, score = "C", 50
    elif decision == "BUY" and correct_decision == "SELL":
        grade, score = "F", 0
    elif decision == "SELL" and correct_decision == "BUY":
        grade, score = "F", 0
    else:
        grade, score = "D", 25

    return is_correct, score, grade

# Load existing results
with open("pilot_test_progress.json", 'r') as f:
    data = json.load(f)

results = data["results"]

# Re-grade all results
for result in results:
    ticker = result["ticker"]
    decision = result["decision"]

    for period_name, return_value in result["returns"].items():
        if return_value is not None:
            period_info = HOLDING_PERIODS[period_name]
            is_correct, score, grade = grade_decision(decision, return_value, period_info)

            result["grades"][period_name] = {
                "is_correct": is_correct,
                "score": score,
                "grade": grade,
                "actual_return": return_value
            }

# Calculate new statistics
print("=" * 80)
print("RE-GRADED PILOT TEST RESULTS (MODERATE THRESHOLDS)")
print("=" * 80)
print(f"\nThresholds:")
print(f"  1-month: BUY >= 5%, SELL <= -3%")
print(f"  3-month: BUY >= 10%, SELL <= -7%")
print(f"  6-month: BUY >= 20%, SELL <= -12%")
print()

period_stats = {}

for period in ["1mo", "3mo", "6mo"]:
    valid_grades = []
    for result in results:
        if period in result["grades"] and result["grades"][period] is not None:
            valid_grades.append(result["grades"][period])

    if valid_grades:
        accuracy = sum(1 for g in valid_grades if g["is_correct"]) / len(valid_grades) * 100
        avg_score = sum(g["score"] for g in valid_grades) / len(valid_grades)

        # Count decisions
        buy_count = sum(1 for r in results if r["decision"] == "BUY")
        hold_count = sum(1 for r in results if r["decision"] == "HOLD")
        sell_count = sum(1 for r in results if r["decision"] == "SELL")

        # Calculate average returns by decision type
        buy_returns = [r["grades"][period]["actual_return"] for r in results
                      if r["decision"] == "BUY" and period in r["grades"]
                      and r["grades"][period] is not None]
        hold_returns = [r["grades"][period]["actual_return"] for r in results
                       if r["decision"] == "HOLD" and period in r["grades"]
                       and r["grades"][period] is not None]
        sell_returns = [r["grades"][period]["actual_return"] for r in results
                       if r["decision"] == "SELL" and period in r["grades"]
                       and r["grades"][period] is not None]

        period_stats[period] = {
            "total_valid": len(valid_grades),
            "accuracy": round(accuracy, 2),
            "avg_score": round(avg_score, 2),
            "buy_count": buy_count,
            "hold_count": hold_count,
            "sell_count": sell_count,
            "buy_correct": sum(1 for r in results if r["decision"] == "BUY" and period in r["grades"]
                              and r["grades"][period] is not None and r["grades"][period]["is_correct"]),
            "hold_correct": sum(1 for r in results if r["decision"] == "HOLD" and period in r["grades"]
                               and r["grades"][period] is not None and r["grades"][period]["is_correct"]),
            "sell_correct": sum(1 for r in results if r["decision"] == "SELL" and period in r["grades"]
                               and r["grades"][period] is not None and r["grades"][period]["is_correct"]),
            "avg_buy_return": round(sum(buy_returns) / len(buy_returns), 2) if buy_returns else None,
            "avg_hold_return": round(sum(hold_returns) / len(hold_returns), 2) if hold_returns else None,
            "avg_sell_return": round(sum(sell_returns) / len(sell_returns), 2) if sell_returns else None
        }

print("-" * 80)
print("PERFORMANCE BY HOLDING PERIOD")
print("-" * 80)

for period, stats in period_stats.items():
    print(f"\n{period.upper()} HOLDING PERIOD:")
    print(f"  Valid Measurements: {stats['total_valid']}")
    print(f"  Accuracy: {stats['accuracy']:.1f}%")
    print(f"  Average Score: {stats['avg_score']:.1f}/100")
    print(f"  Decisions: {stats['buy_count']} BUY | {stats['hold_count']} HOLD | {stats['sell_count']} SELL")
    print(f"  Decision Accuracy: BUY {stats['buy_correct']}/{stats['buy_count']} | HOLD {stats['hold_correct']}/{stats['hold_count']} | SELL {stats['sell_correct']}/{stats['sell_count']}")
    if stats['avg_buy_return']:
        print(f"  Avg BUY return: {stats['avg_buy_return']:+.2f}%")
    if stats['avg_hold_return']:
        print(f"  Avg HOLD return: {stats['avg_hold_return']:+.2f}%")
    if stats['avg_sell_return']:
        print(f"  Avg SELL return: {stats['avg_sell_return']:+.2f}%")

overall_accuracy = sum(s["accuracy"] for s in period_stats.values()) / len(period_stats)

print("\n" + "=" * 80)
print("OVERALL SUMMARY")
print("=" * 80)
print(f"\nOverall Accuracy: {overall_accuracy:.1f}%")
print(f"Total Predictions: {len(results) * 3} (20 stocks × 3 periods)")

print("\n" + "-" * 80)
print("COMPARISON TO AGGRESSIVE THRESHOLDS")
print("-" * 80)
print(f"  Aggressive (10%/20%/30%): 28.3% accuracy")
print(f"  Moderate (5%/10%/20%):    {overall_accuracy:.1f}% accuracy")
print(f"  Improvement: {overall_accuracy - 28.3:+.1f} percentage points")

print("\n" + "=" * 80)
if overall_accuracy >= 60:
    print("RECOMMENDATION: PROCEED WITH FULL 12-MONTH BACKTEST")
    print("Accuracy meets 60% threshold for full test")
elif overall_accuracy >= 50:
    print("RECOMMENDATION: CONSIDER PROCEEDING WITH CAUTION")
    print("Accuracy is close to acceptable levels")
else:
    print("RECOMMENDATION: REVIEW DECISION FRAMEWORK")
    print("Accuracy still below acceptable threshold")
print("=" * 80)

# Save re-graded results
output = {
    "timestamp": data["timestamp"],
    "test_type": "Pilot Test - Rolling Windows (2 months) - RE-GRADED MODERATE",
    "thresholds": HOLDING_PERIODS,
    "total_stocks_analyzed": len(results),
    "overall_accuracy": round(overall_accuracy, 2),
    "period_statistics": period_stats,
    "results": results,
    "monthly_summaries": data["monthly_summaries"]
}

with open("pilot_test_regraded_moderate.json", 'w', encoding='utf-8') as f:
    json.dump(output, f, indent=2)

print(f"\n[SAVED] Re-graded results saved to: pilot_test_regraded_moderate.json")
