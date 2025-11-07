#!/usr/bin/env python3
"""
Historical Validation: JPM HOLD Decision from May 10, 2024
Check actual forward performance to evaluate if HOLD was the right call
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Decision parameters
DECISION_DATE = "2024-05-10"
DECISION = "HOLD"
TICKER = "JPM"

# Forward performance periods
PERIODS = {
    "1 week": 7,
    "2 weeks": 14,
    "1 month": 30,
    "2 months": 60,
    "3 months": 90,
    "6 months": 180
}

def get_forward_performance():
    """
    Get JPM's actual performance after the decision date
    """
    print("="*70)
    print("JPM HOLD DECISION - HISTORICAL VALIDATION")
    print("="*70)
    print(f"\nDecision Date: {DECISION_DATE}")
    print(f"Agent Decision: {DECISION}")
    print(f"Today's Date: {datetime.now().strftime('%Y-%m-%d')}")

    print("\n" + "-"*70)
    print("AGENT'S RATIONALE:")
    print("-"*70)
    print("• Strong fundamentals: 8.8% revenue growth, $49.55B net income")
    print("• Positive technical indicators: bullish MACD, 50-day SMA support")
    print("• Concerns: Economic slowdown, fintech competition, high PEG ratio")
    print("• Strategy: Hold position, monitor economic indicators & earnings")

    print("\n" + "="*70)
    print("FORWARD PERFORMANCE ANALYSIS")
    print("="*70)

    # Download JPM data
    ticker = yf.Ticker(TICKER)

    # Get data from decision date to now
    decision_dt = datetime.strptime(DECISION_DATE, "%Y-%m-%d")
    end_date = datetime.now()

    # Download historical data
    hist = ticker.history(start=DECISION_DATE, end=end_date.strftime("%Y-%m-%d"))

    if hist.empty:
        print("\n[ERROR] No historical data available")
        return

    base_price = hist['Close'].iloc[0]
    print(f"\nBase Price (May 10, 2024): ${base_price:.2f}")

    # Check each forward period
    results = []

    for period_name, days in PERIODS.items():
        target_date = decision_dt + timedelta(days=days)

        # Find closest trading day to target
        closest_date = None
        closest_price = None

        for date, row in hist.iterrows():
            if date.date() >= target_date.date():
                closest_date = date
                closest_price = row['Close']
                break

        if closest_price is not None:
            return_pct = ((closest_price - base_price) / base_price) * 100
            profit_loss = closest_price - base_price

            # Determine if HOLD was appropriate
            if return_pct > 20:
                verdict = "[SHOULD HAVE BOUGHT]"
            elif return_pct > 10:
                verdict = "[STRONG OPPORTUNITY MISSED]"
            elif return_pct > 5:
                verdict = "[MODERATE GAIN MISSED]"
            elif return_pct > -5:
                verdict = "[HOLD WAS REASONABLE]"
            else:
                verdict = "[HOLD WAS GOOD (AVOIDED LOSS)]"

            results.append({
                'period': period_name,
                'date': closest_date.strftime('%Y-%m-%d'),
                'price': closest_price,
                'return_pct': return_pct,
                'profit_loss': profit_loss,
                'verdict': verdict
            })

            print(f"\n{period_name:12} ({closest_date.strftime('%Y-%m-%d')}):")
            print(f"  Price: ${closest_price:.2f}")
            print(f"  Return: {return_pct:+.2f}%")
            print(f"  P/L: ${profit_loss:+.2f}")
            print(f"  Assessment: {verdict}")

    # Get current price
    current_price = hist['Close'].iloc[-1]
    current_date = hist.index[-1].strftime('%Y-%m-%d')
    total_return = ((current_price - base_price) / base_price) * 100

    print("\n" + "="*70)
    print("CURRENT STATUS")
    print("="*70)
    print(f"Current Price ({current_date}): ${current_price:.2f}")
    print(f"Total Return: {total_return:+.2f}%")
    print(f"Total P/L: ${current_price - base_price:+.2f}")

    # Evaluate HOLD decision quality
    print("\n" + "="*70)
    print("DECISION VALIDATION")
    print("="*70)

    # For HOLD, we evaluate if it should have been BUY or SELL instead
    if total_return > 30:
        overall = "[POOR CALL - SHOULD HAVE BEEN BUY]"
        rating = "1/5 stars"
        grade = "F"
        explanation = "Stock had exceptional gains. Agent was far too conservative."
    elif total_return > 20:
        overall = "[SUBOPTIMAL - SHOULD HAVE BEEN BUY]"
        rating = "2/5 stars"
        grade = "D"
        explanation = "Strong gains missed. Agent underestimated opportunity."
    elif total_return > 10:
        overall = "[ACCEPTABLE BUT MISSED OPPORTUNITY]"
        rating = "3/5 stars"
        grade = "C"
        explanation = "Decent gains available. HOLD was safe but not optimal."
    elif total_return > 5:
        overall = "[REASONABLE DECISION]"
        rating = "4/5 stars"
        grade = "B"
        explanation = "Moderate gains. HOLD was appropriate given risks."
    elif total_return > -5:
        overall = "[GOOD CALL]"
        rating = "4.5/5 stars"
        grade = "A-"
        explanation = "Minimal movement. HOLD was the right conservative choice."
    else:
        overall = "[EXCELLENT CALL]"
        rating = "5/5 stars"
        grade = "A+"
        explanation = "Stock declined. HOLD protected capital effectively."

    print(f"\nAgent's HOLD Decision: {overall}")
    print(f"Decision Quality: {rating}")
    print(f"Grade: {grade}")
    print(f"\nAnalysis: {explanation}")

    if total_return > 10:
        print(f"\n[OPPORTUNITY COST] Investors who BOUGHT on {DECISION_DATE} would be up {total_return:.2f}%")
        print(f"The agent's conservative stance meant missing significant gains.")
    elif total_return < -5:
        print(f"\n[PROTECTED CAPITAL] The HOLD decision avoided a {total_return:.2f}% loss")
        print(f"Agent's caution was justified!")
    else:
        print(f"\n[NEUTRAL OUTCOME] HOLD was reasonable given {total_return:+.2f}% movement")

    # Risk/Reward Analysis
    print("\n" + "="*70)
    print("RISK/REWARD ANALYSIS")
    print("="*70)

    peak_price = hist['High'].max()
    peak_date = hist['High'].idxmax().strftime('%Y-%m-%d')
    peak_return = ((peak_price - base_price) / base_price) * 100

    trough_price = hist['Low'].min()
    trough_date = hist['Low'].idxmin().strftime('%Y-%m-%d')
    trough_return = ((trough_price - base_price) / base_price) * 100

    print(f"\nHighest Price: ${peak_price:.2f} (on {peak_date})")
    print(f"Peak Return: {peak_return:+.2f}%")

    print(f"\nLowest Price: ${trough_price:.2f} (on {trough_date})")
    print(f"Trough Return: {trough_return:+.2f}%")

    print(f"\nPrice Range: ${trough_price:.2f} - ${peak_price:.2f}")
    print(f"Volatility Range: {trough_return:+.2f}% to {peak_return:+.2f}%")

    # Volatility
    volatility = hist['Close'].pct_change().std() * 100
    print(f"\nAverage Daily Volatility: {volatility:.2f}%")

    if volatility > 2.5:
        vol_assessment = "[HIGH VOLATILITY] - HOLD was prudent risk management"
    elif volatility > 1.5:
        vol_assessment = "[MODERATE VOLATILITY] - HOLD was defensible"
    else:
        vol_assessment = "[LOW VOLATILITY] - Could have confidently BOUGHT"

    print(f"Volatility Assessment: {vol_assessment}")

    # Risk-adjusted return (Sharpe-like ratio)
    risk_adjusted = total_return / volatility if volatility > 0 else 0
    print(f"\nRisk-Adjusted Return: {risk_adjusted:.2f}")

    if risk_adjusted > 10:
        print("  [EXCELLENT RISK/REWARD] - Definitely should have bought!")
    elif risk_adjusted > 5:
        print("  [GOOD RISK/REWARD] - BUY would have been better")
    elif risk_adjusted > 2:
        print("  [FAIR RISK/REWARD] - HOLD was reasonable")
    else:
        print("  [POOR RISK/REWARD] - HOLD was smart")

    # Compare to agent's concerns
    print("\n" + "="*70)
    print("VALIDATION OF AGENT'S CONCERNS")
    print("="*70)

    print("\nAgent was worried about:")
    print("1. Economic slowdown and tariffs")
    print("2. Fintech competition")
    print("3. High PEG ratio (overvaluation)")

    if total_return > 20:
        print(f"\nVERDICT: Agent's concerns were OVERBLOWN")
        print(f"JPM rose {total_return:.2f}% despite these headwinds.")
        print(f"The fundamentals were stronger than the agent realized.")
    elif total_return > 10:
        print(f"\nVERDICT: Agent's concerns were VALID but OVERSTATED")
        print(f"JPM still gained {total_return:.2f}%, showing resilience.")
        print(f"A more balanced view would have supported a BUY.")
    else:
        print(f"\nVERDICT: Agent's concerns were JUSTIFIED")
        print(f"The {total_return:.2f}% movement validates the cautious stance.")

    # Final summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\nAgent Decision: {DECISION}")
    print(f"Actual Return: {total_return:+.2f}%")
    print(f"Decision Grade: {grade}")
    print(f"\nShould agent have decided differently?")

    if total_return > 20:
        print("  YES - Should have been BUY")
        print(f"  Agent's growth bias toward tech (NVDA) may have blinded it")
        print(f"  to this value opportunity in traditional finance.")
        print(f"\n  KEY LESSON: Don't overlook steady performers with strong fundamentals!")
    elif total_return > 10:
        print("  PROBABLY - BUY would have been better")
        print(f"  Agent was too risk-averse given JPM's strong fundamentals.")
        print(f"\n  KEY LESSON: Balance risk concerns with opportunity assessment.")
    else:
        print("  NO - HOLD was appropriate")
        print(f"  Agent correctly assessed the risk/reward balance.")

if __name__ == "__main__":
    get_forward_performance()
