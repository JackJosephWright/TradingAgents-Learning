#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rolling Time Windows Backtest - Full Year 2024
Tests technical-focused variant across 12 months with 10 stocks per month
Measures performance at 1-month, 3-month, and 6-month holding periods
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
print("ROLLING TIME WINDOWS BACKTEST - 2024", flush=True)
print("=" * 80, flush=True)

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import yfinance as yf

print("\n[INIT] Loading environment...", flush=True)
load_dotenv()

# Stock universe: 10 stocks per month, sector-diverse
MONTHLY_STOCKS = {
    "2024-01": ["AAPL", "JPM", "JNJ", "WMT", "BA", "XOM", "META", "NEE", "PLD", "LIN"],
    "2024-02": ["MSFT", "BAC", "UNH", "COST", "CAT", "CVX", "DIS", "DUK", "AMT", "APD"],
    "2024-03": ["GOOGL", "WFC", "PFE", "HD", "HON", "COP", "NFLX", "SO", "CCI", "SHW"],
    "2024-04": ["NVDA", "GS", "ABBV", "MCD", "UNP", "SLB", "CMCSA", "D", "EQIX", "ECL"],
    "2024-05": ["AMD", "MS", "MRK", "NKE", "UPS", "EOG", "T", "AEP", "PSA", "NEM"],
    "2024-06": ["INTC", "C", "LLY", "SBUX", "LMT", "MPC", "VZ", "EXC", "DLR", "FCX"],
    "2024-07": ["CSCO", "BLK", "TMO", "TGT", "GE", "PSX", "TMUS", "SRE", "O", "NUE"],
    "2024-08": ["ORCL", "AXP", "ABT", "LOW", "MMM", "VLO", "CHTR", "PEG", "AVB", "DOW"],
    "2024-09": ["CRM", "USB", "AMGN", "DG", "RTX", "OXY", "PARA", "XEL", "EQR", "ALB"],
    "2024-10": ["ADBE", "PNC", "CVS", "ROST", "DE", "HAL", "WBD", "ED", "VTR", "VMC"],
    "2024-11": ["QCOM", "TFC", "GILD", "KO", "FDX", "BKR", "FOXA", "ES", "WELL", "PPG"],
    "2024-12": ["AVGO", "SCHW", "BMY", "PEP", "NSC", "WMB", "NXST", "FE", "MAA", "IFF"]
}

# Analysis dates (15th of each month)
ANALYSIS_DATES = [
    "2024-01-15", "2024-02-15", "2024-03-15", "2024-04-15",
    "2024-05-15", "2024-06-15", "2024-07-15", "2024-08-15",
    "2024-09-15", "2024-10-15", "2024-11-15", "2024-12-15"
]

# Holding periods and thresholds (1-MONTH ONLY)
# Short-term trading: 5% monthly target
HOLDING_PERIODS = {
    "1mo": {"days": 30, "buy_threshold": 5, "sell_threshold": -3}
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

            # Don't try to fetch future dates
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

    # Determine correct decision based on actual return
    if actual_return >= buy_threshold:
        correct_decision = "BUY"
    elif actual_return <= sell_threshold:
        correct_decision = "SELL"
    else:
        correct_decision = "HOLD"

    # Check if agent's decision matches
    is_correct = (decision == correct_decision)

    # Assign grade and score
    if is_correct:
        grade, score = "A", 100
    elif decision == "HOLD":
        if correct_decision == "BUY":
            grade, score = "C", 50  # Missed opportunity
        else:  # correct_decision == "SELL"
            grade, score = "C", 50  # Avoided loss
    elif decision == "BUY" and correct_decision == "SELL":
        grade, score = "F", 0  # Bought a loser
    elif decision == "SELL" and correct_decision == "BUY":
        grade, score = "F", 0  # Sold a winner
    else:
        grade, score = "D", 25

    return is_correct, score, grade


def analyze_stock_on_date(ticker, analysis_date, month_key):
    """Analyze a single stock on a specific date"""
    print(f"\n  [{ticker}] Starting analysis for {analysis_date}...", flush=True)

    # Configure with unique memory prefix
    config = DEFAULT_CONFIG.copy()
    config["memory_prefix"] = f"backtest_{month_key}_{ticker}_{int(time.time())}"
    config["max_debate_rounds"] = 1

    start_time = time.time()

    try:
        # Run analysis
        ta = TradingAgentsGraph(debug=False, config=config)
        final_state, decision = ta.propagate(ticker, analysis_date)

        analysis_time = time.time() - start_time

        print(f"  [{ticker}] Decision: {decision} (took {analysis_time:.1f}s)", flush=True)
        print(f"  [{ticker}] Calculating returns...", flush=True)

        # Calculate returns for all holding periods
        returns = calculate_returns(ticker, analysis_date)

        if returns is None:
            print(f"  [{ticker}] FAILED - could not calculate returns", flush=True)
            return None

        # Grade decision for each holding period
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


def run_backtest():
    """Main backtest runner"""
    print("\n[CONFIG] Test Parameters:", flush=True)
    print(f"  Months: {len(ANALYSIS_DATES)}", flush=True)
    print(f"  Stocks per month: 10", flush=True)
    print(f"  Total decisions: {len(ANALYSIS_DATES) * 10}", flush=True)
    print(f"  Holding periods: 1-month, 3-month, 6-month", flush=True)
    print(f"  Estimated time: ~10 hours\n", flush=True)

    all_results = []
    monthly_summaries = []

    for month_idx, analysis_date in enumerate(ANALYSIS_DATES, 1):
        month_key = analysis_date[:7]  # "2024-01"
        stocks = MONTHLY_STOCKS[month_key]

        print("=" * 80, flush=True)
        print(f"MONTH {month_idx}/12: {analysis_date} ({month_key})", flush=True)
        print(f"Stocks: {', '.join(stocks)}", flush=True)
        print("=" * 80, flush=True)

        month_results = []
        month_start_time = time.time()

        for stock_idx, ticker in enumerate(stocks, 1):
            print(f"\n[{month_idx}/{len(ANALYSIS_DATES)}] Stock {stock_idx}/10: {ticker}", flush=True)

            result = analyze_stock_on_date(ticker, analysis_date, month_key)

            if result:
                month_results.append(result)
                all_results.append(result)

            # Brief pause between stocks
            if stock_idx < len(stocks):
                print(f"\n  Waiting 2 seconds before next stock...", flush=True)
                time.sleep(2)

        month_time = time.time() - month_start_time

        # Monthly summary
        print(f"\n[MONTH SUMMARY] {month_key}", flush=True)
        print(f"  Completed: {len(month_results)}/10 stocks", flush=True)
        print(f"  Time: {month_time/60:.1f} minutes", flush=True)

        if month_results:
            for period in ["1mo", "3mo", "6mo"]:
                grades = [r["grades"][period] for r in month_results
                         if period in r["grades"] and r["grades"][period] is not None]

                if grades:
                    accuracy = sum(1 for g in grades if g["is_correct"]) / len(grades) * 100
                    avg_score = sum(g["score"] for g in grades) / len(grades)
                    print(f"  {period}: {accuracy:.1f}% accuracy | Avg score: {avg_score:.1f}/100 | ({len(grades)} valid)", flush=True)

        monthly_summaries.append({
            "month": month_key,
            "analysis_date": analysis_date,
            "stocks_completed": len(month_results),
            "time_minutes": round(month_time / 60, 2)
        })

        # Save progress after each month
        save_progress(all_results, monthly_summaries)

        print(f"\n  Waiting 5 seconds before next month...\n", flush=True)
        time.sleep(5)

    # Final analysis
    print("\n" + "=" * 80, flush=True)
    print("BACKTEST COMPLETE - FINAL RESULTS", flush=True)
    print("=" * 80, flush=True)

    generate_final_report(all_results, monthly_summaries)


def save_progress(all_results, monthly_summaries):
    """Save progress to JSON file"""
    output = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "Rolling Time Windows Backtest",
        "total_stocks_analyzed": len(all_results),
        "months_completed": len(monthly_summaries),
        "results": all_results,
        "monthly_summaries": monthly_summaries
    }

    with open("rolling_windows_progress.json", 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=2)

    print(f"  [SAVED] Progress saved to rolling_windows_progress.json", flush=True)


def generate_final_report(all_results, monthly_summaries):
    """Generate comprehensive final report"""

    # Calculate overall metrics for each holding period
    period_stats = {}

    for period in ["1mo", "3mo", "6mo"]:
        valid_grades = []
        for result in all_results:
            if period in result["grades"] and result["grades"][period] is not None:
                valid_grades.append(result["grades"][period])

        if valid_grades:
            accuracy = sum(1 for g in valid_grades if g["is_correct"]) / len(valid_grades) * 100
            avg_score = sum(g["score"] for g in valid_grades) / len(valid_grades)

            # Calculate average return by decision type
            buy_returns = [g["actual_return"] for r in all_results
                          if r["decision"] == "BUY" and period in r["grades"]
                          and r["grades"][period] is not None]
            hold_returns = [g["actual_return"] for r in all_results
                           if r["decision"] == "HOLD" and period in r["grades"]
                           and r["grades"][period] is not None]
            sell_returns = [g["actual_return"] for r in all_results
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

    # Print summary
    print(f"\nTotal Stocks Analyzed: {len(all_results)}", flush=True)
    print(f"Months Completed: {len(monthly_summaries)}/12", flush=True)
    print("\n" + "-" * 80, flush=True)
    print("PERFORMANCE BY HOLDING PERIOD", flush=True)
    print("-" * 80, flush=True)

    for period, stats in period_stats.items():
        print(f"\n{period.upper()} HOLDING PERIOD:", flush=True)
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

    # Save final report
    final_output = {
        "timestamp": datetime.now().isoformat(),
        "test_type": "Rolling Time Windows Backtest - 2024",
        "total_stocks": len(all_results),
        "months_completed": len(monthly_summaries),
        "period_statistics": period_stats,
        "all_results": all_results,
        "monthly_summaries": monthly_summaries
    }

    with open("rolling_windows_final_report.json", 'w', encoding='utf-8') as f:
        json.dump(final_output, f, indent=2)

    print(f"\n[COMPLETE] Final report saved to: rolling_windows_final_report.json", flush=True)
    print("=" * 80, flush=True)


if __name__ == "__main__":
    run_backtest()
