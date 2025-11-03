#!/usr/bin/env python3
"""
Historical Validation: NVDA BUY Decision from May 10, 2024
Check actual forward performance to validate agent decision
"""

import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

# Decision parameters
DECISION_DATE = "2024-05-10"
DECISION = "BUY"
PRICE_ON_DECISION_DATE = 88.71  # Closing price on May 10, 2024
RECOMMENDED_ENTRY = (75, 85)  # Agent's recommended range

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
    Get NVDA's actual performance after the decision date
    """
    print("="*70)
    print("NVDA BUY DECISION - HISTORICAL VALIDATION")
    print("="*70)
    print(f"\nDecision Date: {DECISION_DATE}")
    print(f"Agent Decision: {DECISION}")
    print(f"Price on Decision Date: ${PRICE_ON_DECISION_DATE:.2f}")
    print(f"Recommended Entry Range: ${RECOMMENDED_ENTRY[0]}-${RECOMMENDED_ENTRY[1]}")
    print(f"Today's Date: {datetime.now().strftime('%Y-%m-%d')}")
    print("\n" + "="*70)
    print("FORWARD PERFORMANCE ANALYSIS")
    print("="*70)

    # Download NVDA data
    ticker = yf.Ticker("NVDA")

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

            # Determine if decision was good
            if return_pct > 10:
                verdict = "[EXCELLENT]"
            elif return_pct > 5:
                verdict = "[GOOD]"
            elif return_pct > 0:
                verdict = "[POSITIVE]"
            elif return_pct > -5:
                verdict = "[SLIGHT LOSS]"
            else:
                verdict = "[POOR]"

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
            print(f"  Verdict: {verdict}")

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

    # Overall verdict
    print("\n" + "="*70)
    print("DECISION VALIDATION")
    print("="*70)

    if total_return > 20:
        overall = "[EXCELLENT CALL]"
        rating = "5/5 stars"
    elif total_return > 10:
        overall = "[GOOD CALL]"
        rating = "4/5 stars"
    elif total_return > 0:
        overall = "[CORRECT DIRECTION]"
        rating = "3/5 stars"
    else:
        overall = "[POOR CALL]"
        rating = "1-2/5 stars"

    print(f"\nAgent's BUY Decision: {overall}")
    print(f"Decision Quality: {rating}")

    if total_return > 0:
        print(f"\n[SUCCESS] The BUY decision was CORRECT!")
        print(f"Investors who bought on {DECISION_DATE} would be up {total_return:.2f}%")
    else:
        print(f"\n[FAILURE] The BUY decision was INCORRECT")
        print(f"Investors who bought on {DECISION_DATE} would be down {total_return:.2f}%")

    # Check if recommended entry point was hit
    print("\n" + "="*70)
    print("ENTRY POINT ANALYSIS")
    print("="*70)
    print(f"\nAgent recommended waiting for: ${RECOMMENDED_ENTRY[0]}-${RECOMMENDED_ENTRY[1]} range")
    print(f"Actual price on decision date: ${base_price:.2f}")

    # Check if price dipped to recommended range
    low_after_decision = hist['Low'].min()
    low_date = hist['Low'].idxmin().strftime('%Y-%m-%d')

    print(f"\nLowest price after decision: ${low_after_decision:.2f} (on {low_date})")

    if low_after_decision <= RECOMMENDED_ENTRY[1]:
        print(f"[INFO] Price DID dip to recommended range!")
        print(f"       Patient investors could have entered at ${low_after_decision:.2f}")

        # Calculate return from better entry
        better_entry_return = ((current_price - low_after_decision) / low_after_decision) * 100
        print(f"       Return from optimal entry: {better_entry_return:+.2f}%")
        print(f"       vs. Return from May 10: {total_return:+.2f}%")
        print(f"       Difference: {better_entry_return - total_return:+.2f}% better!")
    else:
        print(f"[INFO] Price did NOT dip to recommended range")
        print(f"       Waiting would have meant missing the move!")

    # Peak price analysis
    peak_price = hist['High'].max()
    peak_date = hist['High'].idxmax().strftime('%Y-%m-%d')
    peak_return = ((peak_price - base_price) / base_price) * 100

    print(f"\nHighest price reached: ${peak_price:.2f} (on {peak_date})")
    print(f"Peak return: {peak_return:+.2f}%")

    # Summary statistics
    print("\n" + "="*70)
    print("RISK/REWARD SUMMARY")
    print("="*70)

    max_gain = peak_return
    max_loss = ((hist['Low'].min() - base_price) / base_price) * 100

    print(f"\nMaximum Gain (Peak): {max_gain:+.2f}%")
    print(f"Maximum Loss (Trough): {max_loss:+.2f}%")
    print(f"Risk/Reward Ratio: {abs(max_gain/max_loss):.2f}:1")
    print(f"Current Position: {total_return:+.2f}%")

    # Volatility
    volatility = hist['Close'].pct_change().std() * 100
    print(f"\nAverage Daily Volatility: {volatility:.2f}%")

    if volatility > 3:
        print("  [HIGH VOLATILITY] - Requires strong conviction")
    elif volatility > 2:
        print("  [MODERATE VOLATILITY] - Normal for growth tech")
    else:
        print("  [LOW VOLATILITY] - Relatively stable")

if __name__ == "__main__":
    get_forward_performance()
