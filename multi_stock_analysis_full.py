#!/usr/bin/env python3
"""
Multi-Stock Portfolio Analysis - FULL (10 stocks)
Analyzes 10 stocks across 5 sectors to evaluate agent performance
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

# Full 10-stock portfolio across 5 sectors
PORTFOLIO = {
    "Technology": ["NVDA", "AAPL", "MSFT"],
    "Finance": ["JPM", "V"],
    "Consumer": ["KO", "WMT"],
    "Healthcare": ["JNJ", "UNH"],
    "Energy": ["XOM"]
}

# Analysis configuration
ANALYSIS_DATE = "2024-05-10"

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
            "decision": final_decision,
            "analysis_time": time.time() - start_time,
            "success": True
        }

        # Try to extract additional metrics from reports
        if "market_report" in final_state:
            result["has_market_data"] = True
            result["market_report"] = final_state["market_report"][:500]  # First 500 chars
        if "fundamentals_report" in final_state:
            result["has_fundamentals"] = True
        if "investment_plan" in final_state:
            result["investment_plan"] = final_state["investment_plan"]
        if "final_decision" in final_state:
            result["risk_assessment"] = final_state["final_decision"]

        print(f"\n[RESULT] {ticker}: {final_decision}")
        print(f"[TIME] Analysis completed in {result['analysis_time']:.1f} seconds")

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

def main():
    """
    Main execution function
    """
    print(f"\n{'='*70}")
    print("TRADINGAGENTS - FULL 10-STOCK PORTFOLIO ANALYSIS")
    print(f"{'='*70}\n")
    print(f"Analysis Date: {ANALYSIS_DATE}")
    print(f"Total Stocks: 10")
    print(f"Sectors: {len(PORTFOLIO)}")
    print(f"\nPortfolio Composition:")
    for sector, stocks in PORTFOLIO.items():
        print(f"  {sector:15}: {', '.join(stocks)}")

    # Initialize TradingAgents
    print(f"\n{'='*70}")
    print("INITIALIZING TRADING AGENTS")
    print(f"{'='*70}\n")

    config = DEFAULT_CONFIG.copy()
    config["deep_think_llm"] = "gpt-4o-mini"
    config["quick_think_llm"] = "gpt-4o-mini"
    config["max_debate_rounds"] = 1

    ta = TradingAgentsGraph(debug=False, config=config)
    print("Trading agents initialized successfully!")

    # Analyze each stock
    print(f"\n{'='*70}")
    print("STARTING PORTFOLIO ANALYSIS")
    print(f"{'='*70}")

    all_results = []
    stock_count = 0
    total_stocks = sum(len(stocks) for stocks in PORTFOLIO.values())

    for sector, tickers in PORTFOLIO.items():
        print(f"\n{'#'*70}")
        print(f"# SECTOR: {sector.upper()}")
        print(f"{'#'*70}")

        for ticker in tickers:
            stock_count += 1
            print(f"\n[PROGRESS] Analyzing stock {stock_count}/{total_stocks}: {ticker}")

            result = analyze_stock(ta, ticker, ANALYSIS_DATE)
            result["sector"] = sector
            all_results.append(result)

            # Brief pause between stocks to avoid rate limits
            if stock_count < total_stocks:
                print("\nWaiting 2 seconds before next analysis...")
                time.sleep(2)

    # Build portfolio summary
    summary = build_portfolio(all_results)

    # Save results to JSON
    output = {
        "analysis_date": ANALYSIS_DATE,
        "timestamp": datetime.now().isoformat(),
        "individual_results": all_results,
        "portfolio_summary": summary
    }

    output_file = "portfolio_analysis_full.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\n{'='*70}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*70}")
    print(f"\nResults saved to: {output_file}")
    print(f"Total analysis time: {sum(r['analysis_time'] for r in all_results):.1f} seconds")
    print(f"\nNext steps:")
    print(f"  1. Run: python analyze_sectors.py (for sector comparison)")
    print(f"  2. Validate individual decisions")
    print(f"  3. Compare with actual historical performance")

if __name__ == "__main__":
    main()
