"""
Backtesting with Memory & Reflection - Agents Learn Over Time!

This script:
1. Runs trading decisions across multiple dates
2. Calculates actual returns for each decision
3. Reflects on mistakes/successes
4. Stores lessons in memory
5. Shows how agents improve with experience
"""
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
from dotenv import load_dotenv
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

# Load environment variables
load_dotenv()

# Create config
config = DEFAULT_CONFIG.copy()
config["deep_think_llm"] = "gpt-4o-mini"
config["quick_think_llm"] = "gpt-4o-mini"
config["max_debate_rounds"] = 1

config["data_vendors"] = {
    "core_stock_apis": "yfinance",
    "technical_indicators": "yfinance",
    "fundamental_data": "alpha_vantage",
    "news_data": "alpha_vantage",
}

print("=" * 80)
print("BACKTESTING WITH MEMORY & REFLECTION")
print("=" * 80)
print("\nThis demonstration shows how agents LEARN from past decisions.")
print("Watch as they improve their decision-making over time!\n")

# Define test dates (weekly intervals)
test_dates = [
    "2024-04-15",  # Week 1
    "2024-04-22",  # Week 2
    "2024-04-29",  # Week 3
    "2024-05-06",  # Week 4
    "2024-05-13",  # Week 5
]

# Initialize the trading agents graph
print("Initializing TradingAgentsGraph with memory enabled...")
ta = TradingAgentsGraph(debug=False, config=config)  # debug=False for cleaner output
print("[OK] Agents initialized with fresh memory\n")

# Track results
results = []

# Fetch historical data for return calculation
ticker = yf.Ticker("AAPL")
historical_data = ticker.history(start="2024-04-01", end="2024-06-01")

print("=" * 80)
print("RUNNING SEQUENTIAL BACKTESTING WITH LEARNING")
print("=" * 80)

for i, decision_date in enumerate(test_dates, 1):
    print(f"\n{'='*80}")
    print(f"RUN #{i}: {decision_date}")
    print(f"{'='*80}")

    # Get decision from agents
    print(f"\n[Step 1] Agents analyzing AAPL on {decision_date}...")
    _, decision = ta.propagate("AAPL", decision_date)

    print(f"[Step 2] Decision: {decision}")

    # Calculate actual returns (hold for 1 week)
    try:
        # Get price on decision date
        decision_dt = pd.to_datetime(decision_date).tz_localize(historical_data.index.tz)
        decision_price_data = historical_data[historical_data.index >= decision_dt].iloc[0]
        decision_price = decision_price_data['Close']

        # Get price 1 week later
        week_later = decision_dt + timedelta(days=7)
        week_later_data = historical_data[historical_data.index >= week_later].iloc[0]
        week_later_price = week_later_data['Close']

        # Calculate returns
        price_change = week_later_price - decision_price
        returns_pct = (price_change / decision_price) * 100

        # Interpret decision quality
        if decision == "BUY" and returns_pct > 0:
            outcome = "CORRECT"
            returns_value = abs(returns_pct) * 100  # Positive value for good decisions
        elif decision == "SELL" and returns_pct < 0:
            outcome = "CORRECT"
            returns_value = abs(returns_pct) * 100  # Positive value for good decisions
        elif decision == "HOLD":
            outcome = "NEUTRAL"
            returns_value = 0  # Neutral for HOLD
        else:
            outcome = "INCORRECT"
            returns_value = -abs(returns_pct) * 100  # Negative value for bad decisions

        print(f"\n[Step 3] Actual Market Performance:")
        print(f"  Price on {decision_date}: ${decision_price:.2f}")
        print(f"  Price 1 week later: ${week_later_price:.2f}")
        print(f"  Returns: {returns_pct:+.2f}%")
        print(f"  Decision Quality: {outcome}")

        # Reflect and remember
        print(f"\n[Step 4] Agents reflecting on their decision...")
        print(f"  Teaching agents: returns_value = {returns_value:.2f}")
        ta.reflect_and_remember(returns_value)
        print(f"  [OK] Lessons stored in memory for future decisions")

        # Store results
        results.append({
            'run': i,
            'date': decision_date,
            'decision': decision,
            'entry_price': decision_price,
            'exit_price': week_later_price,
            'returns_pct': returns_pct,
            'outcome': outcome,
            'learning_value': returns_value
        })

    except Exception as e:
        print(f"\n[ERROR] Could not calculate returns: {e}")
        results.append({
            'run': i,
            'date': decision_date,
            'decision': decision,
            'entry_price': None,
            'exit_price': None,
            'returns_pct': None,
            'outcome': 'ERROR',
            'learning_value': 0
        })

print(f"\n{'='*80}")
print("BACKTESTING COMPLETE - ANALYZING LEARNING PATTERNS")
print(f"{'='*80}\n")

# Create results DataFrame
df = pd.DataFrame(results)

print("SUMMARY OF ALL DECISIONS:")
print("-" * 80)
print(df.to_string(index=False))

print(f"\n{'='*80}")
print("LEARNING ANALYSIS")
print(f"{'='*80}\n")

# Count decision types
decision_counts = df['decision'].value_counts()
print("Decision Distribution:")
for decision, count in decision_counts.items():
    print(f"  {decision}: {count} times")

# Count outcomes
outcome_counts = df['outcome'].value_counts()
print(f"\nOutcome Distribution:")
for outcome, count in outcome_counts.items():
    print(f"  {outcome}: {count} times")

# Calculate accuracy
correct = len(df[df['outcome'] == 'CORRECT'])
total = len(df[df['outcome'].isin(['CORRECT', 'INCORRECT'])])
if total > 0:
    accuracy = (correct / total) * 100
    print(f"\nDecision Accuracy: {correct}/{total} = {accuracy:.1f}%")

# Check for learning improvement
if len(df) >= 3:
    first_half = df.iloc[:len(df)//2]
    second_half = df.iloc[len(df)//2:]

    first_correct = len(first_half[first_half['outcome'] == 'CORRECT'])
    first_total = len(first_half[first_half['outcome'].isin(['CORRECT', 'INCORRECT'])])

    second_correct = len(second_half[second_half['outcome'] == 'CORRECT'])
    second_total = len(second_half[second_half['outcome'].isin(['CORRECT', 'INCORRECT'])])

    if first_total > 0 and second_total > 0:
        first_accuracy = (first_correct / first_total) * 100
        second_accuracy = (second_correct / second_total) * 100

        print(f"\nLEARNING TREND:")
        print(f"  Early decisions (runs 1-{len(first_half)}): {first_accuracy:.1f}% accuracy")
        print(f"  Later decisions (runs {len(first_half)+1}-{len(df)}): {second_accuracy:.1f}% accuracy")

        if second_accuracy > first_accuracy:
            print(f"  📈 IMPROVEMENT: +{second_accuracy - first_accuracy:.1f}% (agents are learning!)")
        elif second_accuracy < first_accuracy:
            print(f"  📉 DECLINE: {second_accuracy - first_accuracy:.1f}% (may need more data)")
        else:
            print(f"  ➡️ STABLE: No change in accuracy")

print(f"\n{'='*80}")
print("MEMORY SYSTEM STATUS")
print(f"{'='*80}")
print("\nAgents now have memories from these experiences:")
print(f"  - Bull Researcher: Learned from {len(results)} situations")
print(f"  - Bear Researcher: Learned from {len(results)} situations")
print(f"  - Trader: Learned from {len(results)} situations")
print(f"  - Investment Judge: Learned from {len(results)} situations")
print(f"  - Risk Manager: Learned from {len(results)} situations")
print("\nNext time agents encounter similar market conditions,")
print("they will retrieve these memories and make better decisions!")

print(f"\n{'='*80}")
print("DEMONSTRATION COMPLETE")
print(f"{'='*80}\n")
