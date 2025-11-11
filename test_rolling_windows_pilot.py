#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PILOT TEST: Weekly Day Trading Backtest - 8 Weeks in Jan-Feb 2024
Tests technical-focused variant with WEEKLY holding periods (7 days)
Validates day trading approach before running full backtest
"""

import os
import sys
import json
import time
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv

# Force unbuffered output
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("=" * 80, flush=True)
print("PILOT TEST: ROLLING WINDOWS BACKTEST (2 MONTHS)", flush=True)
print("=" * 80, flush=True)

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import yfinance as yf

print("\n[INIT] Loading environment...", flush=True)
load_dotenv()

# PILOT: 8 weeks in Jan-Feb 2024 (day trading approach)
WEEKLY_STOCKS = {
    "2024-01-08": ["AAPL", "JPM", "WMT"],  # Week 1
    "2024-01-15": ["MSFT", "BAC", "COST"],  # Week 2
    "2024-01-22": ["NVDA", "META", "JNJ"],  # Week 3
    "2024-01-29": ["GOOGL", "XOM", "BA"],  # Week 4
    "2024-02-05": ["AMZN", "CVX", "UNH"],  # Week 5
    "2024-02-12": ["TSLA", "DIS", "CAT"],  # Week 6
    "2024-02-19": ["AMD", "NEE", "PLD"],  # Week 7
    "2024-02-26": ["NFLX", "LIN", "DUK"]   # Week 8
}

ANALYSIS_DATES = [
    "2024-01-08", "2024-01-15", "2024-01-22", "2024-01-29",
    "2024-02-05", "2024-02-12", "2024-02-19", "2024-02-26"
]

# Holding period: 1 WEEK (7 days) - Day Trading
# Weekly target: 2% gain, -1.5% stop-loss
HOLDING_PERIODS = {
    "1wk": {"days": 7, "buy_threshold": 2, "sell_threshold": -1.5}
}


def get_price_on_date(ticker, date_str):
    """Fetch closing price for a ticker on a specific date"""
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        start_date = (date_obj - timedelta(days=5)).strftime("%Y-%m-%d")
        end_date = (date_obj + timedelta(days=5)).strftime("%Y-%m-%d")

        # Use yfinance directly
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)

        if not df.empty:
            # Find closest date to target
            df_dates = df.index.strftime("%Y-%m-%d").tolist()
            closest_date = None
            for d in sorted(df_dates):
                if d >= date_str:
                    closest_date = d
                    break
            if not closest_date:
                closest_date = df_dates[-1]

            if closest_date:
                price_row = df[df.index.strftime("%Y-%m-%d") == closest_date]
                if not price_row.empty:
                    return float(price_row['Close'].values[0])
    except Exception as e:
        print(f"    [ERROR] Failed to get price for {ticker} on {date_str}: {e}", flush=True)

    return None


def calculate_returns(ticker, analysis_date):
    """Calculate returns for all holding periods"""
    returns = {}
    analysis_price = get_price_on_date(ticker, analysis_date)

    if not analysis_price:
        print(f"    [SKIP] Could not get analysis date price for {ticker}", flush=True)
        return None

    for period_name, period_info in HOLDING_PERIODS.items():
        try:
            analysis_dt = datetime.strptime(analysis_date, "%Y-%m-%d")
            future_dt = analysis_dt + timedelta(days=period_info["days"])
            future_date = future_dt.strftime("%Y-%m-%d")

            if future_dt > datetime.now():
                print(f"    [SKIP] {period_name} end date {future_date} is in the future", flush=True)
                returns[period_name] = None
                continue

            future_price = get_price_on_date(ticker, future_date)

            if future_price:
                return_pct = ((future_price - analysis_price) / analysis_price) * 100
                returns[period_name] = round(return_pct, 2)
            else:
                returns[period_name] = None

        except Exception as e:
            print(f"    [ERROR] Failed to calculate {period_name} return for {ticker}: {e}", flush=True)
            returns[period_name] = None

    return returns


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


def analyze_stock_on_date(ticker, analysis_date, week_key):
    """Analyze a single stock on a specific date"""
    print(f"\n  [{ticker}] Starting analysis for {analysis_date}...", flush=True)

    config = DEFAULT_CONFIG.copy()
    config["memory_prefix"] = f"pilot_weekly_{week_key}_{ticker}_{int(time.time())}"
    config["max_debate_rounds"] = 1

    start_time = time.time()

    try:
        ta = TradingAgentsGraph(debug=False, config=config)
        final_state, decision = ta.propagate(ticker, analysis_date)

        analysis_time = time.time() - start_time

        print(f"  [{ticker}] Decision: {decision} (took {analysis_time:.1f}s)", flush=True)
        print(f"  [{ticker}] Calculating returns...", flush=True)

        returns = calculate_returns(ticker, analysis_date)

        if returns is None:
            print(f"  [{ticker}] FAILED - could not calculate returns", flush=True)
            return None

        results = {
            "ticker": ticker,
            "analysis_date": analysis_date,
            "decision": decision,
            "analysis_time": round(analysis_time, 2),
            "returns": returns,
            "grades": {}
        }

        for period_name, return_value in returns.items():
            if return_value is not None:
                period_info = HOLDING_PERIODS[period_name]
                is_correct, score, grade = grade_decision(decision, return_value, period_info)

                results["grades"][period_name] = {
                    "is_correct": is_correct,
                    "score": score,
                    "grade": grade,
                    "actual_return": return_value
                }

                status = "CORRECT" if is_correct else "WRONG"
                print(f"  [{ticker}] {period_name}: {return_value:+.2f}% | Grade: {grade} ({status})", flush=True)
            else:
                results["grades"][period_name] = None
                print(f"  [{ticker}] {period_name}: No data", flush=True)

        return results

    except Exception as e:
        print(f"  [{ticker}] FAILED with error: {e}", flush=True)
        import traceback
        traceback.print_exc()
        return None


def run_pilot():
    """Run pilot test"""
    print("\n[CONFIG] Pilot Test Parameters:", flush=True)
    print(f"  Weeks: {len(ANALYSIS_DATES)} (Jan-Feb 2024)", flush=True)
    print(f"  Stocks per week: 3", flush=True)
    print(f"  Total decisions: {len(ANALYSIS_DATES) * 3}", flush=True)
    print(f"  Holding period: 1-WEEK (7 days) - Day Trading", flush=True)
    print(f"  Decision framework: BALANCED (requires 4-5 indicators)", flush=True)
    print(f"  Threshold: BUY >= 2%, SELL <= -1.5%", flush=True)
    print(f"  Estimated time: ~45 minutes\n", flush=True)

    all_results = []
    weekly_summaries = []

    for week_idx, analysis_date in enumerate(ANALYSIS_DATES, 1):
        week_key = analysis_date
        stocks = WEEKLY_STOCKS[week_key]

        print("=" * 80, flush=True)
        print(f"WEEK {week_idx}/8: {analysis_date}", flush=True)
        print(f"Stocks: {', '.join(stocks)}", flush=True)
        print("=" * 80, flush=True)

        week_results = []
        week_start_time = time.time()

        for stock_idx, ticker in enumerate(stocks, 1):
            print(f"\n[{week_idx}/8] Stock {stock_idx}/3: {ticker}", flush=True)

            result = analyze_stock_on_date(ticker, analysis_date, week_key)

            if result:
                week_results.append(result)
                all_results.append(result)

            if stock_idx < len(stocks):
                print(f"\n  Waiting 2 seconds before next stock...", flush=True)
                time.sleep(2)

        week_time = time.time() - week_start_time

        # Weekly summary
        print(f"\n[WEEK SUMMARY] {week_key}", flush=True)
        print(f"  Completed: {len(week_results)}/3 stocks", flush=True)
        print(f"  Time: {week_time/60:.1f} minutes", flush=True)

        if week_results:
            for period in ["1wk"]:
                grades = [r["grades"][period] for r in week_results
                         if period in r["grades"] and r["grades"][period] is not None]

                if grades:
                    accuracy = sum(1 for g in grades if g["is_correct"]) / len(grades) * 100
                    avg_score = sum(g["score"] for g in grades) / len(grades)
                    print(f"  {period}: {accuracy:.1f}% accuracy | Avg score: {avg_score:.1f}/100 | ({len(grades)} valid)", flush=True)

        weekly_summaries.append({
            "week": week_key,
            "analysis_date": analysis_date,
            "stocks_completed": len(week_results),
            "time_minutes": round(week_time / 60, 2)
        })

        # Save progress
        save_progress(all_results, weekly_summaries)

        if week_idx < len(ANALYSIS_DATES):
            print(f"\n  Waiting 5 seconds before next week...\n", flush=True)
            time.sleep(5)

    # Final report
    print("\n" + "=" * 80, flush=True)
    print("PILOT TEST COMPLETE - RESULTS", flush=True)
    print("=" * 80, flush=True)

    generate_final_report(all_results, weekly_summaries)


def save_progress(all_results, weekly_summaries):
    """Save progress to JSON file"""
    output = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "Pilot Test - Weekly Day Trading (8 weeks)",
        "total_stocks_analyzed": len(all_results),
        "weeks_completed": len(weekly_summaries),
        "results": all_results,
        "weekly_summaries": weekly_summaries
    }

    with open("pilot_weekly_progress.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"  [SAVED] Progress saved to pilot_weekly_progress.json", flush=True)


def generate_final_report(all_results, weekly_summaries):
    """Generate final pilot test report"""
    period_stats = {}

    for period in ["1wk"]:
        valid_grades = []
        for result in all_results:
            if period in result["grades"] and result["grades"][period] is not None:
                valid_grades.append(result["grades"][period])

        if valid_grades:
            accuracy = sum(1 for g in valid_grades if g["is_correct"]) / len(valid_grades) * 100
            avg_score = sum(g["score"] for g in valid_grades) / len(valid_grades)

            buy_returns = [r["grades"][period]["actual_return"] for r in all_results
                          if r["decision"] == "BUY" and period in r["grades"]
                          and r["grades"][period] is not None]
            hold_returns = [r["grades"][period]["actual_return"] for r in all_results
                           if r["decision"] == "HOLD" and period in r["grades"]
                           and r["grades"][period] is not None]
            sell_returns = [r["grades"][period]["actual_return"] for r in all_results
                           if r["decision"] == "SELL" and period in r["grades"]
                           and r["grades"][period] is not None]

            period_stats[period] = {
                "total_valid": len(valid_grades),
                "accuracy": round(accuracy, 2),
                "avg_score": round(avg_score, 2),
                "buy_count": sum(1 for r in all_results if r["decision"] == "BUY"),
                "hold_count": sum(1 for r in all_results if r["decision"] == "HOLD"),
                "sell_count": sum(1 for r in all_results if r["decision"] == "SELL"),
                "avg_buy_return": round(sum(buy_returns) / len(buy_returns), 2) if buy_returns else None,
                "avg_hold_return": round(sum(hold_returns) / len(hold_returns), 2) if hold_returns else None,
                "avg_sell_return": round(sum(sell_returns) / len(sell_returns), 2) if sell_returns else None
            }

    print(f"\nTotal Stocks Analyzed: {len(all_results)}", flush=True)
    print(f"Weeks Completed: {len(weekly_summaries)}/8", flush=True)
    print("\n" + "-" * 80, flush=True)
    print("PERFORMANCE BY HOLDING PERIOD", flush=True)
    print("-" * 80, flush=True)

    for period, stats in period_stats.items():
        print(f"\n{period.upper()} HOLDING PERIOD (7 days):", flush=True)
        print(f"  Valid Measurements: {stats['total_valid']}", flush=True)
        print(f"  Accuracy: {stats['accuracy']:.1f}%", flush=True)
        print(f"  Average Score: {stats['avg_score']:.1f}/100", flush=True)
        print(f"  Decisions: {stats['buy_count']} BUY | {stats['hold_count']} HOLD | {stats['sell_count']} SELL", flush=True)
        if stats['avg_buy_return']:
            print(f"  Avg BUY return: {stats['avg_buy_return']:+.2f}%", flush=True)
        if stats['avg_hold_return']:
            print(f"  Avg HOLD return: {stats['avg_hold_return']:+.2f}%", flush=True)
        if stats['avg_sell_return']:
            print(f"  Avg SELL return: {stats['avg_sell_return']:+.2f}%", flush=True)

    final_output = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "Pilot Test - Weekly Day Trading (8 weeks Jan-Feb 2024)",
        "total_stocks": len(all_results),
        "weeks_completed": len(weekly_summaries),
        "period_statistics": period_stats,
        "all_results": all_results,
        "weekly_summaries": weekly_summaries
    }

    with open("pilot_weekly_final_report.json", 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)

    print(f"\n[COMPLETE] Pilot test report saved to: pilot_weekly_final_report.json", flush=True)

    # Recommendation
    print("\n" + "=" * 80, flush=True)
    print("PILOT TEST RECOMMENDATION", flush=True)
    print("=" * 80, flush=True)

    overall_accuracy = sum(s["accuracy"] for s in period_stats.values()) / len(period_stats)

    print(f"\nOverall Accuracy: {overall_accuracy:.1f}%", flush=True)

    if overall_accuracy >= 60:
        print("\n[PROCEED] Accuracy is acceptable. Ready to run extended weekly backtest.", flush=True)
        print("  Consider running longer weekly test with more data points.", flush=True)
    else:
        print("\n[CAUTION] Accuracy below 60%. Review results before extended backtest.", flush=True)
        print("  Consider adjusting thresholds or decision framework.", flush=True)

    print("=" * 80, flush=True)


if __name__ == "__main__":
    run_pilot()
