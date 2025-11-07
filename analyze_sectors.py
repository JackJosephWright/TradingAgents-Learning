#!/usr/bin/env python3
"""
Sector Comparison Analysis
Compares performance across different sectors in portfolio
"""

import json
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

def load_portfolio_results(filename="portfolio_analysis_full.json"):
    """
    Load portfolio analysis results from JSON file
    """
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        print(f"[ERROR] Could not find {filename}")
        print("Please run multi_stock_analysis_full.py first")
        return None

def get_sector_mapping():
    """
    Define sector for each stock
    """
    return {
        "NVDA": "Technology",
        "JPM": "Finance",
        "KO": "Consumer",
        "AAPL": "Technology",
        "MSFT": "Technology",
        "V": "Finance",
        "JNJ": "Healthcare",
        "UNH": "Healthcare",
        "WMT": "Consumer",
        "XOM": "Energy"
    }

def get_historical_performance(ticker, start_date, end_date=None):
    """
    Get actual historical performance for a stock
    """
    if end_date is None:
        end_date = datetime.now().strftime("%Y-%m-%d")

    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(start=start_date, end=end_date)

        if hist.empty:
            return None

        start_price = hist['Close'].iloc[0]
        end_price = hist['Close'].iloc[-1]
        return_pct = ((end_price - start_price) / start_price) * 100

        return {
            "start_price": start_price,
            "end_price": end_price,
            "return_pct": return_pct,
            "max_price": hist['High'].max(),
            "min_price": hist['Low'].min(),
            "volatility": hist['Close'].pct_change().std() * 100
        }
    except Exception as e:
        print(f"[ERROR] Could not get data for {ticker}: {e}")
        return None

def analyze_sectors(portfolio_data):
    """
    Main sector analysis function
    """
    print("="*70)
    print("SECTOR COMPARISON ANALYSIS")
    print("="*70)

    if not portfolio_data:
        return

    results = portfolio_data.get("individual_results", [])
    analysis_date = portfolio_data.get("analysis_date", "2024-05-10")

    sector_map = get_sector_mapping()

    # Group results by sector
    sectors = {}
    for result in results:
        if not result.get("success"):
            continue

        ticker = result["ticker"]
        sector = sector_map.get(ticker, "Unknown")

        if sector not in sectors:
            sectors[sector] = []

        sectors[sector].append(result)

    print(f"\nAnalysis Date: {analysis_date}")
    print(f"Sectors Analyzed: {len(sectors)}")
    print(f"Total Stocks: {sum(len(stocks) for stocks in sectors.values())}")

    # Analyze each sector
    print("\n" + "="*70)
    print("SECTOR-BY-SECTOR BREAKDOWN")
    print("="*70)

    sector_summaries = {}

    for sector, stocks in sorted(sectors.items()):
        print(f"\n{sector.upper()} SECTOR")
        print("-" * 70)

        buy_count = sum(1 for s in stocks if s["decision"] == "BUY")
        hold_count = sum(1 for s in stocks if s["decision"] == "HOLD")
        sell_count = sum(1 for s in stocks if s["decision"] == "SELL")

        print(f"Stocks analyzed: {len(stocks)}")
        print(f"  BUY:  {buy_count}")
        print(f"  HOLD: {hold_count}")
        print(f"  SELL: {sell_count}")

        # Get historical performance
        print(f"\nHistorical Performance (from {analysis_date} to today):")

        sector_performance = []
        for stock in stocks:
            ticker = stock["ticker"]
            decision = stock["decision"]

            perf = get_historical_performance(ticker, analysis_date)
            if perf:
                sector_performance.append({
                    "ticker": ticker,
                    "decision": decision,
                    "return": perf["return_pct"],
                    "volatility": perf["volatility"]
                })

                print(f"  {ticker:6} ({decision:4}): {perf['return_pct']:+7.2f}% return, "
                      f"{perf['volatility']:.2f}% volatility")

        # Calculate sector averages
        if sector_performance:
            avg_return = sum(s["return"] for s in sector_performance) / len(sector_performance)
            avg_volatility = sum(s["volatility"] for s in sector_performance) / len(sector_performance)

            print(f"\n  Sector Average Return: {avg_return:+.2f}%")
            print(f"  Sector Average Volatility: {avg_volatility:.2f}%")

            # Check decision accuracy
            correct_decisions = 0
            for sp in sector_performance:
                if sp["decision"] == "BUY" and sp["return"] > 0:
                    correct_decisions += 1
                elif sp["decision"] == "SELL" and sp["return"] < 0:
                    correct_decisions += 1
                elif sp["decision"] == "HOLD" and -5 < sp["return"] < 10:
                    correct_decisions += 1

            accuracy = (correct_decisions / len(sector_performance)) * 100
            print(f"  Decision Accuracy: {accuracy:.1f}%")

            sector_summaries[sector] = {
                "stocks": len(stocks),
                "buy": buy_count,
                "hold": hold_count,
                "sell": sell_count,
                "avg_return": avg_return,
                "avg_volatility": avg_volatility,
                "accuracy": accuracy,
                "performance": sector_performance
            }

    # Cross-sector comparison
    print("\n" + "="*70)
    print("CROSS-SECTOR COMPARISON")
    print("="*70)

    if sector_summaries:
        print("\nSector Rankings by Return:")
        sorted_by_return = sorted(sector_summaries.items(),
                                  key=lambda x: x[1]["avg_return"],
                                  reverse=True)

        for i, (sector, summary) in enumerate(sorted_by_return, 1):
            print(f"{i}. {sector:15} {summary['avg_return']:+7.2f}% avg return")

        print("\nSector Rankings by Decision Accuracy:")
        sorted_by_accuracy = sorted(sector_summaries.items(),
                                    key=lambda x: x[1]["accuracy"],
                                    reverse=True)

        for i, (sector, summary) in enumerate(sorted_by_accuracy, 1):
            print(f"{i}. {sector:15} {summary['accuracy']:6.1f}% accuracy")

        print("\nRisk-Adjusted Performance (Return / Volatility):")
        risk_adjusted = []
        for sector, summary in sector_summaries.items():
            if summary["avg_volatility"] > 0:
                sharpe = summary["avg_return"] / summary["avg_volatility"]
                risk_adjusted.append((sector, sharpe))

        risk_adjusted.sort(key=lambda x: x[1], reverse=True)
        for i, (sector, sharpe) in enumerate(risk_adjusted, 1):
            print(f"{i}. {sector:15} {sharpe:6.2f} ratio")

    # Investment recommendations
    print("\n" + "="*70)
    print("SECTOR INVESTMENT RECOMMENDATIONS")
    print("="*70)

    for sector, summary in sorted(sector_summaries.items()):
        print(f"\n{sector.upper()}:")

        # Determine recommendation based on multiple factors
        score = 0
        factors = []

        # Factor 1: Average return
        if summary["avg_return"] > 50:
            score += 3
            factors.append(f"  [+] Exceptional returns ({summary['avg_return']:+.1f}%)")
        elif summary["avg_return"] > 20:
            score += 2
            factors.append(f"  [+] Strong returns ({summary['avg_return']:+.1f}%)")
        elif summary["avg_return"] > 0:
            score += 1
            factors.append(f"  [+] Positive returns ({summary['avg_return']:+.1f}%)")
        else:
            score -= 1
            factors.append(f"  [-] Negative returns ({summary['avg_return']:+.1f}%)")

        # Factor 2: Decision accuracy
        if summary["accuracy"] >= 80:
            score += 2
            factors.append(f"  [+] High accuracy ({summary['accuracy']:.0f}%)")
        elif summary["accuracy"] >= 60:
            score += 1
            factors.append(f"  [+] Good accuracy ({summary['accuracy']:.0f}%)")
        else:
            score -= 1
            factors.append(f"  [-] Low accuracy ({summary['accuracy']:.0f}%)")

        # Factor 3: BUY signals
        if summary["buy"] > 0:
            score += 1
            factors.append(f"  [+] {summary['buy']} BUY signal(s)")

        # Factor 4: Volatility
        if summary["avg_volatility"] > 3:
            factors.append(f"  [!] High volatility ({summary['avg_volatility']:.1f}%)")
        elif summary["avg_volatility"] < 2:
            factors.append(f"  [+] Low volatility ({summary['avg_volatility']:.1f}%)")

        # Print factors
        for factor in factors:
            print(factor)

        # Overall recommendation
        print(f"\n  Overall Score: {score}/6")
        if score >= 5:
            print(f"  Recommendation: [STRONG BUY] - Excellent sector opportunity")
        elif score >= 3:
            print(f"  Recommendation: [BUY] - Good sector for allocation")
        elif score >= 1:
            print(f"  Recommendation: [HOLD] - Consider existing positions")
        else:
            print(f"  Recommendation: [AVOID] - Look for better opportunities")

    # Summary
    print("\n" + "="*70)
    print("PORTFOLIO ALLOCATION SUGGESTION")
    print("="*70)

    # Find sectors with BUY signals
    buy_sectors = [(s, sum["buy"]) for s, sum in sector_summaries.items() if sum["buy"] > 0]

    if buy_sectors:
        print("\nRecommended Sector Allocation (equal-weight by BUY signals):")
        total_buys = sum(count for _, count in buy_sectors)

        for sector, buy_count in sorted(buy_sectors, key=lambda x: x[1], reverse=True):
            allocation = (buy_count / total_buys) * 100
            print(f"  {sector:15} {allocation:5.1f}%  ({buy_count} stock(s))")
    else:
        print("\nNo BUY signals detected across sectors")
        print("Recommendation: Stay in cash or look for opportunities in other markets")

    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)

    # Generate key insights
    if sector_summaries:
        best_sector = max(sector_summaries.items(), key=lambda x: x[1]["avg_return"])
        worst_sector = min(sector_summaries.items(), key=lambda x: x[1]["avg_return"])
        most_accurate = max(sector_summaries.items(), key=lambda x: x[1]["accuracy"])

        print(f"\n1. Best Performing Sector: {best_sector[0]}")
        print(f"   Return: {best_sector[1]['avg_return']:+.2f}%")

        print(f"\n2. Worst Performing Sector: {worst_sector[0]}")
        print(f"   Return: {worst_sector[1]['avg_return']:+.2f}%")

        print(f"\n3. Most Accurate Predictions: {most_accurate[0]}")
        print(f"   Accuracy: {most_accurate[1]['accuracy']:.1f}%")

        # Diversification insight
        sectors_with_buys = sum(1 for s in sector_summaries.values() if s["buy"] > 0)
        print(f"\n4. Diversification Opportunity: {sectors_with_buys}/{len(sector_summaries)} sectors have BUY signals")

        if sectors_with_buys >= 3:
            print("   [GOOD] Good sector diversification available")
        elif sectors_with_buys >= 2:
            print("   [MODERATE] Some diversification possible")
        else:
            print("   [LIMITED] Limited diversification - consider broader search")

if __name__ == "__main__":
    portfolio_data = load_portfolio_results()
    if portfolio_data:
        analyze_sectors(portfolio_data)

        print("\n" + "="*70)
        print("ANALYSIS COMPLETE")
        print("="*70)
        print("\nThis analysis shows:")
        print("  - Which sectors performed best historically")
        print("  - How accurate the agent's decisions were per sector")
        print("  - Risk-adjusted performance across sectors")
        print("  - Recommended sector allocation strategy")
    else:
        print("\n[INFO] Run 'python multi_stock_analysis_quick.py' first to generate data")
