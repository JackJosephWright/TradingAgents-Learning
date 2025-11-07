#!/usr/bin/env python3
"""
Historical Validation: KO SELL Decision from May 10, 2024
Check actual forward performance to evaluate if SELL was the right call
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Decision parameters
DECISION_DATE = "2024-05-10"
DECISION = "SELL"
TICKER = "KO"

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
    Get KO's actual performance after the decision date
    """
    print("="*70)
    print("KO SELL DECISION - HISTORICAL VALIDATION")
    print("="*70)
    print(f"\nDecision Date: {DECISION_DATE}")
    print(f"Agent Decision: {DECISION}")
    print(f"Today's Date: {datetime.now().strftime('%Y-%m-%d')}")

    print("\n" + "-"*70)
    print("AGENT'S RATIONALE:")
    print("-"*70)
    print("• Market saturation: Declining demand for sugary drinks")
    print("• High debt-to-equity ratio: 2.32 (financial leverage concerns)")
    print("• Competition: Health-conscious brands threatening market share")
    print("• Overbought: RSI 75.96 suggests vulnerability to correction")
    print("• Strategy: Sell immediately, reallocate to better opportunities")

    print("\n" + "="*70)
    print("FORWARD PERFORMANCE ANALYSIS")
    print("="*70)

    # Download KO data
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

            # Determine if SELL was appropriate
            if return_pct < -10:
                verdict = "[EXCELLENT CALL - AVOIDED LOSS]"
            elif return_pct < -5:
                verdict = "[GOOD CALL - PROTECTED CAPITAL]"
            elif return_pct < 0:
                verdict = "[CORRECT DIRECTION]"
            elif return_pct < 5:
                verdict = "[NEUTRAL - SMALL OPPORTUNITY COST]"
            elif return_pct < 10:
                verdict = "[WRONG - MISSED MODERATE GAINS]"
            else:
                verdict = "[POOR CALL - MISSED SIGNIFICANT GAINS]"

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
    print(f"Total P/L (if held): ${current_price - base_price:+.2f}")

    # Evaluate SELL decision quality
    print("\n" + "="*70)
    print("DECISION VALIDATION")
    print("="*70)

    # For SELL, we check if the stock went down (validating the decision)
    if total_return < -20:
        overall = "[EXCELLENT CALL]"
        rating = "5/5 stars"
        grade = "A+"
        explanation = "Stock crashed. Agent correctly identified major risk."
    elif total_return < -10:
        overall = "[VERY GOOD CALL]"
        rating = "4.5/5 stars"
        grade = "A"
        explanation = "Significant decline avoided. Agent's bearish view was right."
    elif total_return < -5:
        overall = "[GOOD CALL]"
        rating = "4/5 stars"
        grade = "B+"
        explanation = "Stock declined. SELL was justified."
    elif total_return < 0:
        overall = "[CORRECT DIRECTION]"
        rating = "3.5/5 stars"
        grade = "B"
        explanation = "Small decline. SELL was reasonable but not critical."
    elif total_return < 5:
        overall = "[NEUTRAL - SMALL OPPORTUNITY COST]"
        rating = "3/5 stars"
        grade = "C"
        explanation = "Minimal gains missed. Not a big mistake but not optimal."
    elif total_return < 15:
        overall = "[WRONG CALL - MISSED GAINS]"
        rating = "2/5 stars"
        grade = "D"
        explanation = "Stock had decent gains. Agent was wrong to recommend SELL."
    else:
        overall = "[POOR CALL - MAJOR OPPORTUNITY MISSED]"
        rating = "1/5 stars"
        grade = "F"
        explanation = "Stock performed well. Agent completely misjudged this opportunity."

    print(f"\nAgent's SELL Decision: {overall}")
    print(f"Decision Quality: {rating}")
    print(f"Grade: {grade}")
    print(f"\nAnalysis: {explanation}")

    if total_return > 5:
        print(f"\n[OPPORTUNITY COST] Investors who HELD or BOUGHT would be up {total_return:.2f}%")
        print(f"The agent's bearish stance was incorrect.")
        print(f"\nOpportunity cost: ${current_price - base_price:.2f} per share")
    elif total_return < 0:
        print(f"\n[PROTECTED CAPITAL] The SELL decision avoided a {total_return:.2f}% loss")
        print(f"Agent correctly identified the downside risk!")
    else:
        print(f"\n[MINIMAL IMPACT] With only {total_return:+.2f}% movement, SELL had little impact")

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

    if volatility > 2:
        vol_assessment = "[HIGH VOLATILITY] - SELL was prudent for risk-averse"
    elif volatility > 1.5:
        vol_assessment = "[MODERATE VOLATILITY] - SELL was defensible"
    else:
        vol_assessment = "[LOW VOLATILITY] - Stable stock, SELL was questionable"

    print(f"Volatility Assessment: {vol_assessment}")

    # Compare to agent's concerns
    print("\n" + "="*70)
    print("VALIDATION OF AGENT'S CONCERNS")
    print("="*70)

    print("\nAgent was worried about:")
    print("1. Market saturation and declining sugary drink demand")
    print("2. High debt-to-equity ratio (2.32)")
    print("3. Health-conscious competition")
    print("4. Overbought RSI (75.96)")

    if total_return < -5:
        print(f"\nVERDICT: Agent's concerns were CORRECT")
        print(f"KO fell {total_return:.2f}%, validating the bearish thesis.")
    elif total_return < 0:
        print(f"\nVERDICT: Agent's concerns had SOME MERIT")
        print(f"KO did decline slightly ({total_return:.2f}%).")
        print(f"SELL was reasonable but not critical.")
    elif total_return < 10:
        print(f"\nVERDICT: Agent's concerns were OVERSTATED")
        print(f"KO gained {total_return:.2f}% despite the identified risks.")
        print(f"The company's defensive characteristics and dividend were undervalued.")
    else:
        print(f"\nVERDICT: Agent's concerns were WRONG")
        print(f"KO gained {total_return:.2f}%, showing its resilience.")
        print(f"Agent failed to recognize KO's stability and value as a defensive stock.")

    # Defensive stock analysis
    print("\n" + "="*70)
    print("DEFENSIVE STOCK CHARACTERISTICS")
    print("="*70)

    print("\nCoca-Cola is typically considered a 'defensive' stock:")
    print("• Stable cash flows from global brand recognition")
    print("• Consistent dividend payments (2.92% yield mentioned)")
    print("• Less volatile than growth stocks")
    print("• Performs relatively well in economic downturns")

    if volatility < 1.5 and total_return > 0:
        print(f"\nANALYSIS: KO exhibited classic defensive characteristics")
        print(f"  - Low volatility: {volatility:.2f}%")
        print(f"  - Positive return: {total_return:.2f}%")
        print(f"  - Agent may have UNDERVALUED defensive qualities")
        print(f"\nKEY LESSON: Don't dismiss defensive stocks during bull markets!")
        print(f"They provide stability and steady returns, even if not explosive growth.")

    # Final summary
    print("\n" + "="*70)
    print("SUMMARY")
    print("="*70)
    print(f"\nAgent Decision: {DECISION}")
    print(f"Actual Return: {total_return:+.2f}%")
    print(f"Decision Grade: {grade}")
    print(f"\nShould agent have decided differently?")

    if total_return < -5:
        print("  NO - SELL was correct")
        print(f"  Agent successfully identified a declining stock.")
    elif total_return < 0:
        print("  DEBATABLE - SELL was reasonable")
        print(f"  Small decline suggests caution was warranted, but not critical.")
    elif total_return < 10:
        print("  YES - Should have been HOLD or BUY")
        print(f"  Agent was too bearish on a stable, dividend-paying defensive stock.")
        print(f"\n  KEY LESSON: Defensive stocks serve a portfolio purpose!")
        print(f"  Not every stock needs explosive growth. Stability has value.")
    else:
        print("  YES - Should have been BUY")
        print(f"  Agent completely misjudged KO's opportunity.")
        print(f"  Growth bias may have caused agent to undervalue stable performers.")

    # Agent bias assessment
    if total_return > 5:
        print("\n" + "="*70)
        print("AGENT BIAS DETECTION")
        print("="*70)
        print("\nPOSSIBLE GROWTH BIAS DETECTED:")
        print(f"• Agent recommended BUY on NVDA (high-growth tech)")
        print(f"• Agent recommended SELL on KO (stable consumer defensive)")
        print(f"• KO still delivered {total_return:.2f}% with low volatility")
        print(f"\nImplication: Agent may be overweighting growth potential")
        print(f"and underweighting stability and risk-adjusted returns.")

if __name__ == "__main__":
    get_forward_performance()
