#!/usr/bin/env python3
"""
Multi-Stock Portfolio Analysis
Analyzes multiple stocks and builds portfolio recommendations
"""

import os
from datetime import datetime
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import json
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Portfolio configuration
PORTFOLIO = {
    "Technology": ["NVDA", "AAPL", "MSFT"],
    "Finance": ["JPM", "V"],
    "Healthcare": ["JNJ", "UNH"],
    "Consumer": ["KO", "WMT"],
    "Energy": ["XOM"]
}

# Analysis configuration
ANALYSIS_DATE = "2024-05-10"  # Or use datetime.now().strftime("%Y-%m-%d")

def analyze_stock(ta, ticker, date):
    """
    Analyze a single stock and return key metrics
    """
    print(f"\n{'='*70}")
    print(f"ANALYZING: {ticker}")
    print(f"{'='*70}\n")

    start_time = time.time()

    try:
        # Run the full agent pipeline
        final_state, final_decision = ta.propagate(ticker, date)

        # Extract key information
        result = {
            "ticker": ticker,
            "date": date,
            "decision": final_decision,  # BUY/SELL/HOLD
            "analysis_time": time.time() - start_time,
            "success": True
        }

        # Try to extract additional metrics from reports
        if "market_report" in final_state:
            result["has_market_data"] = True
        if "fundamentals_report" in final_state:
            result["has_fundamentals"] = True
        if "investment_plan" in final_state:
            result["investment_plan"] = final_state["investment_plan"]
        if "final_decision" in final_state:
            result["risk_assessment"] = final_state["final_decision"]

        return result

    except Exception as e:
        print(f"ERROR analyzing {ticker}: {str(e)}")
        return {
            "ticker": ticker,
            "date": date,
            "decision": "ERROR",
            "error": str(e),
            "analysis_time": time.time() - start_time,
            "success": False
        }

def build_portfolio(results):
    """
    Build portfolio recommendations based on analysis results
    """
    print(f"\n{'='*70}")
    print("PORTFOLIO ANALYSIS SUMMARY")
    print(f"{'='*70}\n")

    buy_stocks = []
    hold_stocks = []
    sell_stocks = []
    error_stocks = []

    for result in results:
        if not result["success"]:
            error_stocks.append(result["ticker"])
            continue

        decision = result["decision"]
        if decision == "BUY":
            buy_stocks.append(result)
        elif decision == "HOLD":
            hold_stocks.append(result)
        elif decision == "SELL":
            sell_stocks.append(result)

    # Display results by category
    print(f"BUY Recommendations ({len(buy_stocks)}):")
    for stock in buy_stocks:
        print(f"  [BUY] {stock['ticker']:6} - Analysis time: {stock['analysis_time']:.1f}s")

    print(f"\nHOLD Recommendations ({len(hold_stocks)}):")
    for stock in hold_stocks:
        print(f"  [HOLD] {stock['ticker']:6} - Analysis time: {stock['analysis_time']:.1f}s")

    print(f"\nSELL/AVOID Recommendations ({len(sell_stocks)}):")
    for stock in sell_stocks:
        print(f"  [SELL] {stock['ticker']:6} - Analysis time: {stock['analysis_time']:.1f}s")

    if error_stocks:
        print(f"\nErrors ({len(error_stocks)}):")
        for ticker in error_stocks:
            print(f"  [ERROR] {ticker}")

    # Calculate portfolio metrics
    total_analyzed = len(results) - len(error_stocks)
    if total_analyzed > 0:
        buy_pct = (len(buy_stocks) / total_analyzed) * 100
        hold_pct = (len(hold_stocks) / total_analyzed) * 100
        sell_pct = (len(sell_stocks) / total_analyzed) * 100

        print(f"\n{'='*70}")
        print("PORTFOLIO METRICS")
        print(f"{'='*70}")
        print(f"Total Stocks Analyzed: {total_analyzed}")
        print(f"BUY signals:  {len(buy_stocks):2} ({buy_pct:5.1f}%)")
        print(f"HOLD signals: {len(hold_stocks):2} ({hold_pct:5.1f}%)")
        print(f"SELL signals: {len(sell_stocks):2} ({sell_pct:5.1f}%)")

        # Suggested allocation
        print(f"\n{'='*70}")
        print("SUGGESTED PORTFOLIO ALLOCATION")
        print(f"{'='*70}")

        if buy_stocks:
            allocation_per_stock = 100.0 / len(buy_stocks)
            print(f"\nBased on BUY signals, suggested equal-weight allocation:")
            for stock in buy_stocks:
                print(f"  {stock['ticker']:6}: {allocation_per_stock:5.1f}%")
        else:
            print("\nNo BUY signals - consider waiting or researching alternatives")

    return {
        "buy": buy_stocks,
        "hold": hold_stocks,
        "sell": sell_stocks,
        "errors": error_stocks
    }

def save_results(results, portfolio_summary, filename="portfolio_analysis_results.json"):
    """
    Save analysis results to JSON file
    """
    output = {
        "analysis_date": ANALYSIS_DATE,
        "timestamp": datetime.now().isoformat(),
        "individual_results": results,
        "portfolio_summary": portfolio_summary
    }

    with open(filename, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n[SUCCESS] Results saved to: {filename}")

def main():
    """
    Main execution function
    """
    print("="*70)
    print("MULTI-STOCK PORTFOLIO ANALYSIS")
    print("="*70)
    print(f"Analysis Date: {ANALYSIS_DATE}")

    # Flatten portfolio to list of tickers
    all_tickers = []
    for sector, tickers in PORTFOLIO.items():
        all_tickers.extend(tickers)

    print(f"Stocks to analyze: {len(all_tickers)}")
    print(f"Sectors covered: {len(PORTFOLIO)}")
    print()

    # Initialize TradingAgents
    print("Initializing TradingAgents...")
    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = "gpt-4o-mini"
    config["quick_think_llm"] = "gpt-4o-mini"
    config["max_debate_rounds"] = 1

    ta = TradingAgentsGraph(debug=False, config=config)
    print("[SUCCESS] TradingAgents initialized\n")

    # Analyze each stock
    results = []
    for i, ticker in enumerate(all_tickers, 1):
        print(f"\nProgress: {i}/{len(all_tickers)}")
        result = analyze_stock(ta, ticker, ANALYSIS_DATE)
        results.append(result)

        # Small delay to avoid rate limits
        if i < len(all_tickers):
            print("\nWaiting 10 seconds before next analysis...")
            time.sleep(10)

    # Build portfolio recommendations
    portfolio_summary = build_portfolio(results)

    # Save results
    save_results(results, portfolio_summary)

    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)

if __name__ == "__main__":
    main()
