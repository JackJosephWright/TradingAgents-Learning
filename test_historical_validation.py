"""
Historical validation: Did the HOLD decision make sense?
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

print("=" * 80)
print("HISTORICAL VALIDATION: AAPL Trading Decision on 2024-05-10")
print("=" * 80)

# The agents' decision was made on 2024-05-10
decision_date = "2024-05-10"
decision_price_date = "2024-05-09"  # Last trading day before decision

# Get data for 6 months after the decision
start_date = "2024-05-01"
end_date = "2024-11-10"  # 6 months later

print(f"\n1. AGENT DECISION SUMMARY (2024-05-10):")
print("-" * 80)
print("Decision: HOLD")
print("Rationale:")
print("  - Strong bullish momentum (MACD 3.09, 10 EMA 178.03)")
print("  - BUT approaching overbought (RSI 64.14)")
print("  - Mixed news sentiment (0.08 to 0.36)")
print("  - Concerns: market saturation, legal challenges, union issues")
print("\nKey Technical Levels on 2024-05-10:")
print("  - Price: ~$183.25 (close on 2024-05-09)")
print("  - 50 SMA: 171.28 (support)")
print("  - 200 SMA: 179.38 (support)")
print("  - Bollinger Upper: 185.72 (resistance)")

print(f"\n2. FETCHING ACTUAL HISTORICAL DATA:")
print("-" * 80)

try:
    # Fetch data
    ticker = yf.Ticker("AAPL")
    data = ticker.history(start=start_date, end=end_date)

    if data.empty:
        print("[ERROR] No data retrieved")
    else:
        # Get the decision date price
        decision_price = data.loc[data.index.date == pd.to_datetime(decision_price_date).date()]['Close'].values[0]

        print(f"[OK] Retrieved {len(data)} days of data")
        print(f"Decision date price (2024-05-09 close): ${decision_price:.2f}")

        # Calculate what happened at key timeframes
        timeframes = {
            "1 week later (2024-05-17)": 7,
            "1 month later (2024-06-10)": 31,
            "3 months later (2024-08-10)": 92,
            "6 months later (2024-11-10)": 184
        }

        print(f"\n3. PRICE PERFORMANCE AFTER HOLD DECISION:")
        print("-" * 80)

        results = []
        for label, days_offset in timeframes.items():
            try:
                target_date = pd.to_datetime(decision_price_date) + timedelta(days=days_offset)
                # Make target_date timezone-aware to match data.index
                if data.index.tz is not None:
                    target_date = target_date.tz_localize(data.index.tz)
                # Find closest trading day
                closest_data = data[data.index >= target_date].iloc[0]
                target_price = closest_data['Close']
                target_actual_date = closest_data.name.strftime('%Y-%m-%d')

                change_dollars = target_price - decision_price
                change_percent = (change_dollars / decision_price) * 100

                results.append({
                    'timeframe': label,
                    'date': target_actual_date,
                    'price': target_price,
                    'change_pct': change_percent
                })

                status = "GAIN" if change_percent > 0 else "LOSS"
                print(f"{label:30s} [{target_actual_date}]")
                print(f"  Price: ${target_price:.2f} ({status}: {change_percent:+.2f}%)")

            except IndexError:
                print(f"{label:30s} [Data not available]")

        print(f"\n4. WHAT IF SCENARIOS:")
        print("-" * 80)

        # Calculate best/worst case scenarios
        max_price = data['Close'].max()
        min_price = data['Close'].min()
        max_date = data['Close'].idxmax().strftime('%Y-%m-%d')
        min_date = data['Close'].idxmin().strftime('%Y-%m-%d')

        max_gain = ((max_price - decision_price) / decision_price) * 100
        max_loss = ((min_price - decision_price) / decision_price) * 100

        print(f"Best case (if BOUGHT on 2024-05-09):")
        print(f"  Peak: ${max_price:.2f} on {max_date} (+{max_gain:.2f}%)")

        print(f"\nWorst case (if BOUGHT on 2024-05-09):")
        print(f"  Low: ${min_price:.2f} on {min_date} ({max_loss:.2f}%)")

        print(f"\nIf SOLD on 2024-05-09 (agents' Phase 1 decision):")
        print(f"  Opportunity cost: Would have missed {max_gain:.2f}% gain at peak")

        print(f"\n5. DECISION QUALITY ASSESSMENT:")
        print("-" * 80)

        # Get the 6-month performance
        six_month_result = next((r for r in results if '6 months' in r['timeframe']), None)

        if six_month_result:
            six_month_return = six_month_result['change_pct']

            print(f"6-month return: {six_month_return:+.2f}%")

            if six_month_return > 10:
                print("\n[ANALYSIS] HOLD was SUBOPTIMAL")
                print("  - Strong gains suggest BUY would have been better")
                print("  - However, HOLD protected against downside while")
                print("    still allowing participation if held long-term")
            elif six_month_return > 0:
                print("\n[ANALYSIS] HOLD was REASONABLE")
                print("  - Modest gains suggest the caution was justified")
                print("  - Avoiding overbought entry protected against volatility")
            elif six_month_return > -10:
                print("\n[ANALYSIS] HOLD was GOOD")
                print("  - Slight losses validate the cautious stance")
                print("  - Agents correctly identified overbought conditions")
            else:
                print("\n[ANALYSIS] HOLD was EXCELLENT")
                print("  - Significant losses avoided by not buying")
                print("  - Agents correctly anticipated correction")

            print(f"\nCompared to Phase 1 SELL decision:")
            if six_month_return > 0:
                print(f"  - Phase 1 (SELL) would have missed +{six_month_return:.2f}% gains")
                print(f"  - Phase 2 (HOLD) was MUCH BETTER - kept position")
            else:
                print(f"  - Phase 1 (SELL) would have avoided {six_month_return:.2f}% losses")
                print(f"  - But HOLD wasn't wrong - it provided flexibility")

        print(f"\n6. VOLATILITY ANALYSIS:")
        print("-" * 80)

        # Calculate volatility metrics
        data['Daily_Return'] = data['Close'].pct_change()
        volatility = data['Daily_Return'].std() * 100

        print(f"Daily volatility (std dev): {volatility:.2f}%")

        # Count significant moves
        big_up_days = len(data[data['Daily_Return'] > 0.03])
        big_down_days = len(data[data['Daily_Return'] < -0.03])

        print(f"Days with >3% gains: {big_up_days}")
        print(f"Days with >3% losses: {big_down_days}")

        if big_down_days > big_up_days:
            print("\nValidation: More down days than up days supports HOLD caution")
        else:
            print("\nValidation: More up days suggests BUY could have worked")

        print(f"\n7. AGENT PREDICTION ACCURACY:")
        print("-" * 80)

        # Check if the RSI overbought warning was accurate
        print("Agent predicted concerns:")
        print("  [X] RSI approaching overbought (64.14)")

        if min_price < decision_price * 0.95:
            print("      -> CORRECT: Stock did pull back >5%")
        else:
            print("      -> INCORRECT: No significant pullback occurred")

        print("  [X] Market saturation concerns")
        if six_month_return and six_month_return < 5:
            print("      -> VALIDATED: Limited growth supports saturation thesis")
        else:
            print("      -> REFUTED: Strong growth contradicts saturation")

        print("\n" + "=" * 80)
        print("VALIDATION COMPLETE")
        print("=" * 80)

except Exception as e:
    print(f"[ERROR] {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
