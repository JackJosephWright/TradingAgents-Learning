==========================================================================
PHASE 4 CURRICULUM - PRACTICAL APPLICATION & EXPERIMENTATION
==========================================================================

Course: TradingAgents Multi-Agent System
Level: Advanced (Phases 1-3 Complete)
Duration: 8-20 hours (varies by path chosen)
Prerequisites: Understanding of memory systems, risk management, and architecture

This curriculum builds on your completed learning from Phases 1-3:
- ✅ Phase 1: Setup, first analyses, architecture basics
- ✅ Phase 2: Agent understanding, workflow comprehension
- ✅ Phase 3: Memory systems, risk management, advanced features

==========================================================================
PHASE 4 OVERVIEW
==========================================================================

**Goal**: Apply your knowledge through hands-on experimentation and build
practical trading analysis systems.

**Structure**: Choose your own adventure! Eight learning paths available,
ranging from quick wins to comprehensive projects.

**Recommended Starting Point**: Path A (Multi-Stock Portfolio Analysis)
- Immediate value demonstration
- Uses all knowledge from Phases 1-3
- Foundation for advanced paths
- 1-2 hours, moderate difficulty

**Learning Outcomes**:
By the end of Phase 4, you will be able to:
1. Run systematic analyses across multiple stocks
2. Optimize system configuration for your needs
3. Compare different LLM providers and their reasoning patterns
4. Build custom trading strategies with modified agents
5. Visualize and analyze agent debates
6. Deploy production-ready analysis pipelines
7. Create comprehensive portfolio management systems

==========================================================================
PATH A: MULTI-STOCK PORTFOLIO ANALYSIS ⭐⭐
==========================================================================

**Difficulty**: Moderate
**Duration**: 1-2 hours
**Status**: RECOMMENDED STARTING POINT

**Objective**:
Analyze 8-10 different stocks across various sectors to understand how
the agent system adapts to different companies, industries, and market
conditions. Build a diversified portfolio based on agent recommendations.

**What You'll Learn**:
- How agents adapt reasoning to different sectors
- Pattern recognition across similar companies
- Portfolio diversification principles
- Comparative analysis techniques
- Trading metrics application across sectors

**Prerequisites**:
- Completed Phases 1-3
- Working TradingAgents installation
- API keys configured

---

### STEP 1: Stock Selection (15 min)

Choose 8-10 stocks across different sectors:

**Suggested Portfolio Mix**:

1. **Technology (2-3 stocks)**
   - NVDA (NVIDIA) - AI/GPU leader
   - AAPL (Apple) - Consumer tech
   - MSFT (Microsoft) - Enterprise tech
   - GOOGL (Google) - Search/Cloud

2. **Finance (1-2 stocks)**
   - JPM (JP Morgan) - Traditional banking
   - V (Visa) - Payment processing

3. **Healthcare (1-2 stocks)**
   - JNJ (Johnson & Johnson) - Pharmaceuticals
   - UNH (UnitedHealth) - Healthcare services

4. **Consumer (1-2 stocks)**
   - KO (Coca-Cola) - Beverages
   - WMT (Walmart) - Retail

5. **Energy (1 stock)**
   - XOM (Exxon) - Traditional energy
   - TSLA (Tesla) - Alternative energy/EV

**Why This Mix**:
- Diverse industries test agent adaptability
- Mix of growth (tech) and value (consumer staples)
- Different volatility profiles (NVDA vs KO)
- Various market caps and risk profiles

---

### STEP 2: Create Analysis Script (20 min)

Create a new file: `multi_stock_analysis.py`

```python
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
        print(f"  ✅ {stock['ticker']:6} - Analysis time: {stock['analysis_time']:.1f}s")

    print(f"\nHOLD Recommendations ({len(hold_stocks)}):")
    for stock in hold_stocks:
        print(f"  ⏸️  {stock['ticker']:6} - Analysis time: {stock['analysis_time']:.1f}s")

    print(f"\nSELL/AVOID Recommendations ({len(sell_stocks)}):")
    for stock in sell_stocks:
        print(f"  ❌ {stock['ticker']:6} - Analysis time: {stock['analysis_time']:.1f}s")

    if error_stocks:
        print(f"\nErrors ({len(error_stocks)}):")
        for ticker in error_stocks:
            print(f"  ⚠️  {ticker}")

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

    print(f"\n✅ Results saved to: {filename}")

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
    print("✅ TradingAgents initialized\n")

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
```

**Key Features**:
- Analyzes multiple stocks systematically
- Tracks timing for each analysis
- Categorizes results by BUY/HOLD/SELL
- Calculates portfolio allocation
- Saves results to JSON for later analysis
- Includes error handling

---

### STEP 3: Run the Analysis (30-45 min)

```bash
cd /mnt/c/Users/iorda/OneDrive/Documents/GitHub/TradingAgents-Learning
source .venv/bin/activate  # or .venv/Scripts/activate on Windows
python multi_stock_analysis.py
```

**What to Observe**:
1. How agents adapt reasoning to different sectors
2. Which sectors get more BUY vs SELL signals
3. Timing differences (some stocks may take longer)
4. Error patterns (data availability issues)

**Expected Runtime**:
- ~4 minutes per stock × 10 stocks = ~40 minutes total
- With 10-second delays between stocks

---

### STEP 4: Analyze Results (20 min)

After the script completes, examine `portfolio_analysis_results.json`

**Questions to Answer**:

1. **Sector Patterns**:
   - Which sector had the most BUY signals?
   - Which had the most SELL signals?
   - Why might this be?

2. **Decision Distribution**:
   - What percentage were BUY/HOLD/SELL?
   - Is the system too conservative or aggressive?
   - How does this compare to your own market view?

3. **Reasoning Comparison**:
   - Look at investment plans for similar companies (AAPL vs MSFT)
   - How did agents differentiate between them?
   - What factors were emphasized for each sector?

4. **Risk Assessment**:
   - Did risky/safe/neutral analysts align across all stocks?
   - Or did risk perspectives vary by company?
   - Which stocks had the most debate/disagreement?

---

### STEP 5: Sector Comparison Analysis (15 min)

Create `analyze_sectors.py`:

```python
#!/usr/bin/env python3
"""
Analyze results by sector
"""

import json

SECTORS = {
    "Technology": ["NVDA", "AAPL", "MSFT", "GOOGL"],
    "Finance": ["JPM", "V"],
    "Healthcare": ["JNJ", "UNH"],
    "Consumer": ["KO", "WMT"],
    "Energy": ["XOM", "TSLA"]
}

def analyze_by_sector(results_file="portfolio_analysis_results.json"):
    with open(results_file, 'r') as f:
        data = json.load(f)

    results = data["individual_results"]

    print("="*70)
    print("SECTOR-BY-SECTOR ANALYSIS")
    print("="*70)

    for sector, tickers in SECTORS.items():
        print(f"\n{sector}:")
        print("-" * 40)

        sector_results = [r for r in results if r["ticker"] in tickers and r["success"]]

        if not sector_results:
            print("  No successful analyses")
            continue

        buy_count = sum(1 for r in sector_results if r["decision"] == "BUY")
        hold_count = sum(1 for r in sector_results if r["decision"] == "HOLD")
        sell_count = sum(1 for r in sector_results if r["decision"] == "SELL")

        total = len(sector_results)
        print(f"  Total analyzed: {total}")
        print(f"  BUY:  {buy_count}/{total} ({buy_count/total*100:.0f}%)")
        print(f"  HOLD: {hold_count}/{total} ({hold_count/total*100:.0f}%)")
        print(f"  SELL: {sell_count}/{total} ({sell_count/total*100:.0f}%)")

        # Show individual results
        for r in sector_results:
            print(f"    {r['ticker']:6} -> {r['decision']}")

if __name__ == "__main__":
    analyze_by_sector()
```

Run it:
```bash
python analyze_sectors.py
```

---

### STEP 6: Apply Trading Metrics Knowledge (20 min)

Now that you understand key trading metrics (from our earlier discussion),
manually review 2-3 of the decisions and validate them:

**Exercise**: Pick one BUY and one SELL recommendation

For each stock, manually check:

1. **Valuation Metrics**:
   - What's the current P/E ratio? (use Yahoo Finance or similar)
   - Is it overvalued or undervalued compared to sector?

2. **Technical Indicators** (from market_report in your results):
   - RSI: Is it in the 30-70 range (healthy) or overbought/oversold?
   - MACD: Is it aligned with the BUY/SELL decision?
   - Bollinger Bands: Is price near support or resistance?

3. **Momentum**:
   - Check recent price action (last 1-3 months)
   - Does the decision align with momentum?

4. **Fundamental Health**:
   - Revenue growth (from fundamentals_report)
   - Debt levels
   - Profitability

**Validation Questions**:
- Does the agent decision make sense given the metrics?
- What was the primary factor (technical, fundamental, news)?
- Would you personally agree with the decision?

---

### EXERCISES

**Exercise 1: Conservative Portfolio** (30 min)
Modify the script to only include defensive sectors:
- Consumer Staples: KO, PG, JNJ
- Utilities: NEE, DUK
- Healthcare: UNH, JNJ

Compare the BUY/SELL distribution to the full portfolio.
Hypothesis: More HOLD recommendations for defensive stocks?

**Exercise 2: Growth Portfolio** (30 min)
Create a high-growth portfolio:
- NVDA, TSLA, COIN, SQ, SHOP
- All volatile growth stocks

Question: Does the risk management system treat these differently?

**Exercise 3: Rerun on Different Date** (45 min)
Pick a different analysis date:
- Bull market: "2024-01-15"
- Bear market: "2022-06-15"
- Recent: current date

Compare results across time periods.

**Exercise 4: Manual Validation** (60 min)
For all BUY recommendations:
1. Research each stock independently
2. Check if you agree with the decision
3. Compare your reasoning to the agent's investment_plan
4. Document any disagreements

This develops your critical thinking about agent outputs.

---

### DELIVERABLES

By the end of Path A, you should have:

1. ✅ `multi_stock_analysis.py` - Working script
2. ✅ `portfolio_analysis_results.json` - Analysis output
3. ✅ `analyze_sectors.py` - Sector comparison tool
4. ✅ Written analysis answering the questions in Step 4
5. ✅ Manual validation of 2-3 key decisions
6. ✅ Optional: Exercise results and comparisons

---

### LEARNING OUTCOMES

After completing Path A, you will:
- ✅ Understand how agents adapt to different companies/sectors
- ✅ Know how to run systematic multi-stock analyses
- ✅ Be able to interpret and validate agent decisions
- ✅ Understand portfolio construction principles
- ✅ Have applied trading metrics knowledge practically
- ✅ Be ready for more advanced customization

---

### NEXT STEPS

After completing Path A, you can:
- Continue to **Path B** (Configuration Experimentation)
- Jump to **Path E** (Custom Strategy Development)
- Try **Path F** (Debate Analysis & Visualization)
- Or choose any other path based on your interests

==========================================================================
PATH B: CONFIGURATION EXPERIMENTATION ⭐⭐⭐
==========================================================================

**Difficulty**: Moderate-Advanced
**Duration**: 2-3 hours

**Objective**:
Systematically test different configuration options to understand their
impact on decision quality, speed, and cost. Find the optimal settings
for your use case.

**What You'll Learn**:
- How debate rounds affect decision quality
- Impact of different LLM models
- Data vendor performance comparison
- Cost vs quality tradeoffs
- Configuration optimization techniques

---

### EXPERIMENT 1: Debate Rounds Impact (45 min)

**Hypothesis**: More debate rounds = better decisions, but slower and more expensive

Create `test_debate_rounds.py`:

```python
#!/usr/bin/env python3
"""
Test impact of different debate round configurations
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import time
import json

TICKER = "NVDA"
DATE = "2024-05-10"
ROUNDS_TO_TEST = [1, 2, 3, 5]

def test_debate_rounds(rounds):
    """
    Test a specific debate round configuration
    """
    print(f"\n{'='*70}")
    print(f"Testing with {rounds} debate round(s)")
    print(f"{'='*70}\n")

    config = DEFAULT_CONFIG.copy()
    config["max_debate_rounds"] = rounds
    config["max_risk_discuss_rounds"] = rounds
    config["quick_think_llm"] = "gpt-4o-mini"
    config["deep_think_llm"] = "gpt-4o-mini"

    ta = TradingAgentsGraph(debug=False, config=config)

    start_time = time.time()
    final_state, final_decision = ta.propagate(TICKER, DATE)
    duration = time.time() - start_time

    # Extract debate depth from state
    invest_debate = final_state.get("investment_debate_state", {})
    risk_debate = final_state.get("risk_debate_state", {})

    bull_arguments = invest_debate.get("bull_history", [])
    bear_arguments = invest_debate.get("bear_history", [])

    result = {
        "rounds": rounds,
        "decision": final_decision,
        "duration": duration,
        "bull_arguments_count": len(bull_arguments),
        "bear_arguments_count": len(bear_arguments),
        "investment_plan": final_state.get("investment_plan", "")[:200],  # First 200 chars
        "estimated_cost": estimate_cost(rounds)
    }

    return result

def estimate_cost(rounds):
    """
    Rough cost estimation based on typical token usage
    """
    # Approximate:
    # - 4 analysts: 4k tokens each = 16k tokens
    # - Debate: 3k tokens per round × 2 sides = 6k per round
    # - Managers: 2 × 5k tokens = 10k tokens
    # - Risk debate: 3k tokens per round × 3 sides = 9k per round

    base_tokens = 16000 + 10000  # Analysts + managers
    debate_tokens = 6000 * rounds + 9000 * rounds
    total_tokens = base_tokens + debate_tokens

    # gpt-4o-mini pricing: $0.150 / 1M input tokens, $0.600 / 1M output tokens
    # Assume 80% input, 20% output
    input_tokens = total_tokens * 0.8
    output_tokens = total_tokens * 0.2

    cost = (input_tokens / 1_000_000 * 0.150) + (output_tokens / 1_000_000 * 0.600)
    return cost

def compare_results(all_results):
    """
    Compare results across different debate round settings
    """
    print(f"\n{'='*70}")
    print("DEBATE ROUNDS COMPARISON")
    print(f"{'='*70}\n")

    print(f"{'Rounds':<8} {'Decision':<10} {'Time (s)':<12} {'Cost ($)':<10} {'Arguments':<12}")
    print("-" * 70)

    for r in all_results:
        args = f"{r['bull_arguments_count']}B + {r['bear_arguments_count']}Be"
        print(f"{r['rounds']:<8} {r['decision']:<10} {r['duration']:<12.1f} ${r['estimated_cost']:<9.4f} {args:<12}")

    # Calculate value metrics
    print(f"\n{'='*70}")
    print("VALUE ANALYSIS")
    print(f"{'='*70}\n")

    baseline = all_results[0]
    for r in all_results[1:]:
        time_increase = ((r['duration'] - baseline['duration']) / baseline['duration']) * 100
        cost_increase = ((r['estimated_cost'] - baseline['estimated_cost']) / baseline['estimated_cost']) * 100
        decision_changed = "YES ⚠️" if r['decision'] != baseline['decision'] else "NO"

        print(f"{baseline['rounds']} round -> {r['rounds']} rounds:")
        print(f"  Time increase: {time_increase:+.1f}%")
        print(f"  Cost increase: {cost_increase:+.1f}%")
        print(f"  Decision changed: {decision_changed}")
        print()

def main():
    all_results = []

    for rounds in ROUNDS_TO_TEST:
        result = test_debate_rounds(rounds)
        all_results.append(result)

        # Save intermediate results
        with open(f"debate_rounds_test_{rounds}.json", 'w') as f:
            json.dump(result, f, indent=2)

    # Compare all results
    compare_results(all_results)

    # Save final comparison
    with open("debate_rounds_comparison.json", 'w') as f:
        json.dump(all_results, f, indent=2)

    print("\n✅ Results saved to debate_rounds_comparison.json")

if __name__ == "__main__":
    main()
```

**Run the experiment**:
```bash
python test_debate_rounds.py
```

**Analysis Questions**:
1. Did more rounds change the final decision?
2. What's the diminishing return point? (2 rounds vs 5 rounds)
3. Is the extra cost/time worth it?
4. Did argument quality improve with more rounds?

---

### EXPERIMENT 2: LLM Model Comparison (60 min)

**Hypothesis**: Better models = better decisions, but higher cost

Test different models:
- gpt-4o-mini (baseline, cheapest)
- gpt-4o (expensive, high quality)
- claude-sonnet-4 (if you have Anthropic API key)

Create `test_llm_models.py`:

```python
#!/usr/bin/env python3
"""
Compare different LLM models for decision quality
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import time

TICKER = "AAPL"
DATE = "2024-05-10"

MODELS_TO_TEST = [
    {
        "name": "All GPT-4o-mini",
        "quick": "gpt-4o-mini",
        "deep": "gpt-4o-mini",
        "cost_multiplier": 1.0
    },
    {
        "name": "Hybrid (mini + 4o)",
        "quick": "gpt-4o-mini",
        "deep": "gpt-4o",
        "cost_multiplier": 2.5
    },
    {
        "name": "All GPT-4o",
        "quick": "gpt-4o",
        "deep": "gpt-4o",
        "cost_multiplier": 15.0
    }
]

def test_model_config(model_config):
    """
    Test a specific LLM model configuration
    """
    print(f"\n{'='*70}")
    print(f"Testing: {model_config['name']}")
    print(f"  Quick-think: {model_config['quick']}")
    print(f"  Deep-think:  {model_config['deep']}")
    print(f"{'='*70}\n")

    config = DEFAULT_CONFIG.copy()
    config["quick_think_llm"] = model_config["quick"]
    config["deep_think_llm"] = model_config["deep"]
    config["max_debate_rounds"] = 1

    ta = TradingAgentsGraph(debug=False, config=config)

    start_time = time.time()
    final_state, final_decision = ta.propagate(TICKER, DATE)
    duration = time.time() - start_time

    return {
        "name": model_config["name"],
        "decision": final_decision,
        "duration": duration,
        "investment_plan": final_state.get("investment_plan", ""),
        "relative_cost": model_config["cost_multiplier"]
    }

def compare_models(results):
    """
    Compare model performance
    """
    print(f"\n{'='*70}")
    print("MODEL COMPARISON")
    print(f"{'='*70}\n")

    print(f"{'Model':<25} {'Decision':<10} {'Time (s)':<12} {'Rel. Cost':<10}")
    print("-" * 70)

    for r in results:
        print(f"{r['name']:<25} {r['decision']:<10} {r['duration']:<12.1f} {r['relative_cost']:<10.1f}x")

    # Show investment plan differences
    print(f"\n{'='*70}")
    print("INVESTMENT PLAN QUALITY (first 300 chars)")
    print(f"{'='*70}\n")

    for r in results:
        print(f"{r['name']}:")
        print(f"  {r['investment_plan'][:300]}...")
        print()

def main():
    results = []

    for model_config in MODELS_TO_TEST:
        result = test_model_config(model_config)
        results.append(result)

        # Wait between tests
        print("\nWaiting 10 seconds...")
        time.sleep(10)

    compare_models(results)

if __name__ == "__main__":
    main()
```

**Analysis Questions**:
1. Did expensive models produce different decisions?
2. Was the investment plan more detailed/sophisticated?
3. Which configuration offers the best value?
4. Is hybrid approach (cheap + expensive) optimal?

---

### EXPERIMENT 3: Data Vendor Comparison (45 min)

Test yfinance vs alpha_vantage for data quality:

```python
#!/usr/bin/env python3
"""
Compare data vendor performance
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

TICKER = "MSFT"
DATE = "2024-05-10"

VENDOR_CONFIGS = [
    {
        "name": "All yfinance",
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "yfinance",
        "news_data": "yfinance"
    },
    {
        "name": "All Alpha Vantage",
        "core_stock_apis": "alpha_vantage",
        "technical_indicators": "alpha_vantage",
        "fundamental_data": "alpha_vantage",
        "news_data": "alpha_vantage"
    },
    {
        "name": "Hybrid",
        "core_stock_apis": "yfinance",
        "technical_indicators": "yfinance",
        "fundamental_data": "alpha_vantage",
        "news_data": "alpha_vantage"
    }
]

def test_vendor_config(vendor_config):
    """
    Test a specific data vendor configuration
    """
    print(f"\n{'='*70}")
    print(f"Testing: {vendor_config['name']}")
    print(f"{'='*70}\n")

    config = DEFAULT_CONFIG.copy()
    config["data_vendors"] = {k: v for k, v in vendor_config.items() if k != "name"}
    config["quick_think_llm"] = "gpt-4o-mini"
    config["deep_think_llm"] = "gpt-4o-mini"

    ta = TradingAgentsGraph(debug=True, config=config)  # Debug=True to see data retrieval

    try:
        final_state, final_decision = ta.propagate(TICKER, DATE)

        # Check data completeness
        has_market = bool(final_state.get("market_report"))
        has_fundamentals = bool(final_state.get("fundamentals_report"))
        has_news = bool(final_state.get("news_report"))

        return {
            "name": vendor_config["name"],
            "decision": final_decision,
            "has_market_data": has_market,
            "has_fundamentals": has_fundamentals,
            "has_news": has_news,
            "success": True
        }
    except Exception as e:
        return {
            "name": vendor_config["name"],
            "error": str(e),
            "success": False
        }

def main():
    results = []

    for vendor_config in VENDOR_CONFIGS:
        result = test_vendor_config(vendor_config)
        results.append(result)

    # Compare
    print(f"\n{'='*70}")
    print("DATA VENDOR COMPARISON")
    print(f"{'='*70}\n")

    for r in results:
        if r["success"]:
            print(f"{r['name']}:")
            print(f"  Decision: {r['decision']}")
            print(f"  Market data: {'✅' if r['has_market_data'] else '❌'}")
            print(f"  Fundamentals: {'✅' if r['has_fundamentals'] else '❌'}")
            print(f"  News: {'✅' if r['has_news'] else '❌'}")
        else:
            print(f"{r['name']}: ❌ Error - {r['error']}")
        print()

if __name__ == "__main__":
    main()
```

**Analysis Questions**:
1. Which vendor had better data availability?
2. Did data source affect the decision?
3. Which vendor is more reliable?
4. What's the best hybrid configuration?

---

### OPTIMAL CONFIGURATION RECOMMENDATION (30 min)

Based on all experiments, document your recommended configuration:

Create `optimal_config.py`:

```python
"""
Optimal configuration based on experiments
"""

OPTIMAL_CONFIG = {
    # Based on your experiments
    "max_debate_rounds": 2,  # Sweet spot: quality vs speed
    "max_risk_discuss_rounds": 1,  # Risk debate needs less iteration

    # Two-tier LLM strategy
    "quick_think_llm": "gpt-4o-mini",  # 90% of calls
    "deep_think_llm": "gpt-4o-mini",  # For budget, or "gpt-4o" for quality

    # Data vendors
    "data_vendors": {
        "core_stock_apis": "yfinance",  # Fast, reliable
        "technical_indicators": "yfinance",  # Good coverage
        "fundamental_data": "alpha_vantage",  # More complete
        "news_data": "alpha_vantage"  # Better news coverage
    },

    # Justification
    "rationale": {
        "debate_rounds": "2 rounds provide 90% of quality at 150% of time",
        "llm_choice": "gpt-4o-mini for cost, gpt-4o for critical decisions only",
        "data_vendors": "Hybrid approach balances speed and data completeness"
    }
}

# Your specific values may differ based on your experiments!
```

---

### DELIVERABLES

By the end of Path B, you should have:

1. ✅ `test_debate_rounds.py` and results
2. ✅ `test_llm_models.py` and comparison
3. ✅ `test_data_vendors.py` and analysis
4. ✅ `optimal_config.py` with your recommendations
5. ✅ Written analysis of tradeoffs
6. ✅ Cost-benefit analysis for each configuration

---

### LEARNING OUTCOMES

After completing Path B, you will:
- ✅ Understand configuration impact on performance
- ✅ Know how to optimize for your use case
- ✅ Understand cost vs quality tradeoffs
- ✅ Be able to tune the system systematically
- ✅ Have evidence-based configuration recommendations

==========================================================================
PATH C: MULTI-LLM COMPARISON ⭐⭐⭐⭐
==========================================================================

**Difficulty**: Advanced
**Duration**: 2-3 hours
**Prerequisites**: API keys for multiple providers

**Objective**:
Compare reasoning patterns and decision quality across different LLM
providers (OpenAI, Anthropic, Google, Ollama local models).

**What You'll Learn**:
- How different models approach the same problem
- Provider-specific reasoning patterns
- Cost vs performance across providers
- When to use which model
- Local vs cloud model tradeoffs

**Note**: This path requires API keys for:
- OpenAI (you have)
- Anthropic Claude (optional)
- Google Gemini (optional)
- Or Ollama for local models

---

### SETUP: Multi-Provider Configuration (15 min)

1. Get API keys (if you don't have them):
   - Anthropic: https://console.anthropic.com/
   - Google AI: https://makersuite.google.com/app/apikey

2. Add to `.env`:
```bash
OPENAI_API_KEY=your_existing_key
ANTHROPIC_API_KEY=sk-ant-xxxxx
GOOGLE_API_KEY=AIzaSyxxxxx
```

3. Install Anthropic and Google SDKs (if not already):
```bash
pip install anthropic google-generativeai
```

---

### EXPERIMENT: Same Stock, Different Models (90 min)

Create `multi_llm_comparison.py`:

```python
#!/usr/bin/env python3
"""
Compare decision-making across different LLM providers
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import time
import json

TICKER = "NVDA"
DATE = "2024-05-10"

# Model configurations to test
MODELS = [
    {
        "name": "OpenAI GPT-4o-mini",
        "provider": "openai",
        "quick": "gpt-4o-mini",
        "deep": "gpt-4o-mini"
    },
    {
        "name": "OpenAI GPT-4o",
        "provider": "openai",
        "quick": "gpt-4o",
        "deep": "gpt-4o"
    },
    # Uncomment if you have Anthropic API key
    # {
    #     "name": "Anthropic Claude Sonnet",
    #     "provider": "anthropic",
    #     "quick": "claude-sonnet-4",
    #     "deep": "claude-sonnet-4"
    # },
    # Uncomment if you have Google API key
    # {
    #     "name": "Google Gemini Pro",
    #     "provider": "google",
    #     "quick": "gemini-1.5-pro",
    #     "deep": "gemini-1.5-pro"
    # }
]

def test_model(model_config):
    """
    Test analysis with a specific LLM
    """
    print(f"\n{'='*70}")
    print(f"Testing: {model_config['name']}")
    print(f"{'='*70}\n")

    config = DEFAULT_CONFIG.copy()
    config["llm_provider"] = model_config["provider"]
    config["quick_think_llm"] = model_config["quick"]
    config["deep_think_llm"] = model_config["deep"]
    config["max_debate_rounds"] = 1

    # Set backend URL based on provider
    if model_config["provider"] == "openai":
        config["backend_url"] = "https://api.openai.com/v1"
    elif model_config["provider"] == "anthropic":
        config["backend_url"] = "https://api.anthropic.com"
    elif model_config["provider"] == "google":
        config["backend_url"] = "https://generativelanguage.googleapis.com"

    try:
        ta = TradingAgentsGraph(debug=False, config=config)

        start_time = time.time()
        final_state, final_decision = ta.propagate(TICKER, DATE)
        duration = time.time() - start_time

        # Extract key reasoning
        investment_plan = final_state.get("investment_plan", "")
        final_risk_decision = final_state.get("final_decision", "")

        result = {
            "model": model_config["name"],
            "provider": model_config["provider"],
            "decision": final_decision,
            "duration": duration,
            "investment_plan": investment_plan,
            "risk_assessment": final_risk_decision,
            "success": True
        }

        # Save individual result
        filename = f"{model_config['provider']}_{model_config['quick']}_result.json"
        with open(filename, 'w') as f:
            json.dump(result, f, indent=2)

        return result

    except Exception as e:
        print(f"❌ Error with {model_config['name']}: {str(e)}")
        return {
            "model": model_config["name"],
            "error": str(e),
            "success": False
        }

def compare_reasoning(results):
    """
    Compare reasoning patterns across models
    """
    print(f"\n{'='*70}")
    print("MULTI-LLM COMPARISON RESULTS")
    print(f"{'='*70}\n")

    successful_results = [r for r in results if r["success"]]

    if not successful_results:
        print("❌ No successful analyses to compare")
        return

    # Decision summary
    print("DECISION SUMMARY:")
    print("-" * 70)
    for r in successful_results:
        print(f"{r['model']:<30} {r['decision']:<10} ({r['duration']:.1f}s)")

    # Check for consensus
    decisions = [r["decision"] for r in successful_results]
    unique_decisions = set(decisions)

    print(f"\n{'='*70}")
    print("CONSENSUS ANALYSIS:")
    print(f"{'='*70}\n")

    if len(unique_decisions) == 1:
        print(f"✅ UNANIMOUS: All models agree on {list(unique_decisions)[0]}")
    else:
        print(f"⚠️  DISAGREEMENT: Models gave {len(unique_decisions)} different decisions")
        for decision in unique_decisions:
            count = decisions.count(decision)
            models = [r["model"] for r in successful_results if r["decision"] == decision]
            print(f"  {decision}: {count}/{len(decisions)} - {', '.join(models)}")

    # Reasoning comparison
    print(f"\n{'='*70}")
    print("REASONING PATTERNS (first 300 chars of investment plan):")
    print(f"{'='*70}\n")

    for r in successful_results:
        print(f"{r['model']}:")
        print(f"  {r['investment_plan'][:300]}...")
        print()

def analyze_differences(results):
    """
    Deep analysis of reasoning differences
    """
    print(f"\n{'='*70}")
    print("DEEP REASONING ANALYSIS")
    print(f"{'='*70}\n")

    successful_results = [r for r in results if r["success"]]

    # Extract keywords from each investment plan
    for r in successful_results:
        plan = r["investment_plan"].lower()

        # Count mentions of key concepts
        concepts = {
            "ai/gpu": plan.count("ai") + plan.count("gpu") + plan.count("artificial intelligence"),
            "risk": plan.count("risk"),
            "growth": plan.count("growth"),
            "revenue": plan.count("revenue"),
            "competition": plan.count("competition") + plan.count("competitor"),
            "market": plan.count("market"),
        }

        print(f"{r['model']}:")
        print(f"  Key concept emphasis:")
        for concept, count in sorted(concepts.items(), key=lambda x: x[1], reverse=True):
            if count > 0:
                print(f"    {concept}: mentioned {count} times")
        print()

def main():
    print("="*70)
    print("MULTI-LLM COMPARISON EXPERIMENT")
    print("="*70)
    print(f"Stock: {TICKER}")
    print(f"Date: {DATE}")
    print(f"Models to test: {len(MODELS)}")
    print()

    results = []

    for i, model_config in enumerate(MODELS, 1):
        print(f"\n[{i}/{len(MODELS)}] Testing {model_config['name']}...")
        result = test_model(model_config)
        results.append(result)

        if i < len(MODELS):
            print("\nWaiting 15 seconds before next model...")
            time.sleep(15)

    # Compare results
    compare_reasoning(results)
    analyze_differences(results)

    # Save comparison
    with open("multi_llm_comparison.json", 'w') as f:
        json.dump(results, f, indent=2)

    print("\n✅ Full comparison saved to multi_llm_comparison.json")

if __name__ == "__main__":
    main()
```

**Run it**:
```bash
python multi_llm_comparison.py
```

---

### ANALYSIS QUESTIONS (30 min)

After running the comparison:

1. **Decision Consensus**:
   - Did all models reach the same decision?
   - If not, which models disagreed and why?
   - Is there a "majority vote" decision?

2. **Reasoning Style**:
   - Which model was most detailed?
   - Which was most concise?
   - Which emphasized technical vs fundamental analysis?

3. **Risk Assessment**:
   - Did risk perspectives differ across models?
   - Which model was most conservative/aggressive?

4. **Performance**:
   - Which model was fastest?
   - Which seemed most "thoughtful"?
   - Best cost/performance ratio?

5. **Consistency**:
   - Run the same analysis twice with each model
   - How consistent are decisions? (temperature = 0 should be very consistent)

---

### ADVANCED: Ensemble Decision Making (45 min)

Create `ensemble_decision.py`:

```python
#!/usr/bin/env python3
"""
Combine multiple LLM decisions into ensemble recommendation
"""

import json
from collections import Counter

def load_results(filename="multi_llm_comparison.json"):
    with open(filename, 'r') as f:
        return json.load(f)

def ensemble_decision(results):
    """
    Create ensemble decision from multiple models
    """
    successful_results = [r for r in results if r.get("success")]

    if not successful_results:
        return "ERROR", "No successful analyses"

    # Simple majority vote
    decisions = [r["decision"] for r in successful_results]
    vote_counts = Counter(decisions)
    majority_decision, majority_count = vote_counts.most_common(1)[0]

    total_votes = len(decisions)
    confidence = (majority_count / total_votes) * 100

    print("="*70)
    print("ENSEMBLE DECISION")
    print("="*70)
    print(f"\nVoting Results:")
    for decision, count in vote_counts.most_common():
        pct = (count / total_votes) * 100
        print(f"  {decision}: {count}/{total_votes} ({pct:.0f}%)")

    print(f"\nEnsemble Decision: {majority_decision}")
    print(f"Confidence: {confidence:.0f}%")

    if confidence == 100:
        print("✅ UNANIMOUS - Very high confidence")
    elif confidence >= 75:
        print("✅ STRONG CONSENSUS - High confidence")
    elif confidence >= 60:
        print("⚠️  WEAK CONSENSUS - Moderate confidence")
    else:
        print("❌ NO CONSENSUS - Low confidence, proceed with caution")

    return majority_decision, confidence

def weighted_ensemble(results):
    """
    Weighted ensemble based on model quality/cost
    """
    # Assign weights (adjust based on your preferences)
    model_weights = {
        "gpt-4o": 3.0,  # Highest quality
        "claude-sonnet-4": 2.5,
        "gpt-4o-mini": 1.0,  # Baseline
        "gemini-1.5-pro": 1.5
    }

    successful_results = [r for r in results if r.get("success")]

    decision_weights = {}
    total_weight = 0

    for r in successful_results:
        model_name = r.get("quick", "gpt-4o-mini")
        weight = model_weights.get(model_name, 1.0)

        decision = r["decision"]
        decision_weights[decision] = decision_weights.get(decision, 0) + weight
        total_weight += weight

    if not decision_weights:
        return "ERROR", 0

    # Find weighted majority
    best_decision = max(decision_weights, key=decision_weights.get)
    confidence = (decision_weights[best_decision] / total_weight) * 100

    print(f"\n{'='*70}")
    print("WEIGHTED ENSEMBLE (based on model quality)")
    print(f"{'='*70}\n")

    for decision, weight in sorted(decision_weights.items(), key=lambda x: x[1], reverse=True):
        pct = (weight / total_weight) * 100
        print(f"  {decision}: weight {weight:.1f}/{total_weight:.1f} ({pct:.0f}%)")

    print(f"\nWeighted Decision: {best_decision}")
    print(f"Weighted Confidence: {confidence:.0f}%")

    return best_decision, confidence

def main():
    results = load_results()

    # Simple majority
    ensemble_decision(results)

    # Weighted ensemble
    weighted_ensemble(results)

if __name__ == "__main__":
    main()
```

This creates a "wisdom of crowds" approach where multiple LLMs vote on
the decision, increasing robustness.

---

### DELIVERABLES

By the end of Path C, you should have:

1. ✅ `multi_llm_comparison.py` with results
2. ✅ `ensemble_decision.py` for combining decisions
3. ✅ Individual result files for each model
4. ✅ `multi_llm_comparison.json` with full comparison
5. ✅ Written analysis of reasoning patterns
6. ✅ Recommendations for which models to use when

---

### LEARNING OUTCOMES

After completing Path C, you will:
- ✅ Understand how different LLMs approach trading decisions
- ✅ Know provider-specific strengths and weaknesses
- ✅ Be able to implement ensemble decision-making
- ✅ Understand when to use which model
- ✅ Have evidence for cost/performance tradeoffs

==========================================================================
PATH D: HISTORICAL BACKTESTING CAMPAIGN ⭐⭐⭐
==========================================================================

**Difficulty**: Moderate-Advanced
**Duration**: 2-4 hours
**Note**: Currently blocked by yfinance cache issue (see Session 2 transcript)

**Objective**:
Systematically test the system on historical data to validate decision
quality and track learning improvements over time.

**What You'll Learn**:
- Backtesting methodology
- Performance metrics (accuracy, Sharpe ratio, max drawdown)
- How memory/learning improves decisions
- System limitations and failure modes

**Status**:
This path is partially blocked by a known issue with yfinance cache
corruption. Workaround: Delete cache before each run, or wait for fix.

---

### BACKGROUND: The Cache Issue

From Session 2 transcript:
- yfinance caches data in CSV files
- Cache files sometimes get corrupted (merged rows)
- This blocks multi-date backtesting
- Workaround: `rm -rf ~/.cache/py-yfinance-cache/` before each run
- Alternative: Use alpha_vantage as primary data vendor

---

### APPROACH 1: Single-Date Validation (60 min)

Instead of multi-date backtesting, validate on a single historical date
and then manually check actual performance.

Create `historical_validation.py`:

```python
#!/usr/bin/env python3
"""
Historical validation - single date with forward performance check
"""

from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import yfinance as yf
from datetime import datetime, timedelta

def analyze_and_validate(ticker, analysis_date, forward_periods=[7, 30, 90]):
    """
    Analyze stock on a specific date and check forward performance
    """
    print(f"\n{'='*70}")
    print(f"HISTORICAL VALIDATION: {ticker} on {analysis_date}")
    print(f"{'='*70}\n")

    # Run analysis
    config = DEFAULT_CONFIG.copy()
    config["quick_think_llm"] = "gpt-4o-mini"
    config["deep_think_llm"] = "gpt-4o-mini"

    ta = TradingAgentsGraph(debug=False, config=config)

    try:
        final_state, decision = ta.propagate(ticker, analysis_date)
        print(f"Agent Decision: {decision}")

        # Get historical prices to validate
        stock = yf.Ticker(ticker)

        # Parse analysis date
        analysis_dt = datetime.strptime(analysis_date, "%Y-%m-%d")

        # Get forward performance
        print(f"\nForward Performance:")
        print("-" * 40)

        hist = stock.history(start=analysis_date,
                            end=(analysis_dt + timedelta(days=max(forward_periods) + 10)).strftime("%Y-%m-%d"))

        if hist.empty:
            print("❌ No historical price data available")
            return None

        base_price = hist['Close'].iloc[0]

        for days in forward_periods:
            if len(hist) > days:
                future_price = hist['Close'].iloc[days]
                return_pct = ((future_price - base_price) / base_price) * 100

                # Evaluate decision
                if decision == "BUY" and return_pct > 5:
                    verdict = "✅ GOOD"
                elif decision == "SELL" and return_pct < -5:
                    verdict = "✅ GOOD"
                elif decision == "HOLD" and abs(return_pct) < 5:
                    verdict = "✅ GOOD"
                elif abs(return_pct) < 3:
                    verdict = "⚠️  NEUTRAL"
                else:
                    verdict = "❌ POOR"

                print(f"  {days:3d} days: {return_pct:+7.2f}% | {verdict}")

        return {
            "ticker": ticker,
            "date": analysis_date,
            "decision": decision,
            "base_price": base_price,
            "forward_returns": {
                days: ((hist['Close'].iloc[days] - base_price) / base_price) * 100
                for days in forward_periods if len(hist) > days
            }
        }

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

# Test cases - historical decisions we can validate
TEST_CASES = [
    ("NVDA", "2024-01-15"),  # Before big AI boom
    ("AAPL", "2024-05-10"),  # We analyzed this in Session 1
    ("TSLA", "2024-03-01"),  # Volatile stock test
    ("KO", "2024-02-15"),   # Defensive stock test
]

def main():
    results = []

    for ticker, date in TEST_CASES:
        result = analyze_and_validate(ticker, date)
        if result:
            results.append(result)

        print("\nWaiting 15 seconds...")
        time.sleep(15)

    # Summary
    print(f"\n{'='*70}")
    print("VALIDATION SUMMARY")
    print(f"{'='*70}\n")

    for r in results:
        print(f"{r['ticker']} ({r['date']}): {r['decision']}")
        for days, return_pct in r['forward_returns'].items():
            print(f"  {days} days: {return_pct:+.2f}%")
        print()

if __name__ == "__main__":
    main()
```

This approach validates decisions without needing multi-date backtesting.

---

### APPROACH 2: Weekly Analysis (if cache issue resolved)

If the cache issue gets fixed, here's the full backtesting approach:

Create `weekly_backtesting.py`:

```python
#!/usr/bin/env python3
"""
Weekly backtesting across multiple weeks
NOTE: Only run if cache corruption issue is resolved
"""

import pandas as pd
from datetime import datetime, timedelta
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG
import time

def generate_weekly_dates(start_date, end_date):
    """
    Generate list of dates (one per week)
    """
    dates = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    while current <= end:
        # Only include weekdays
        if current.weekday() < 5:  # Monday = 0, Friday = 4
            dates.append(current.strftime("%Y-%m-%d"))
        current += timedelta(days=7)

    return dates

def backtest_weekly(ticker, start_date, end_date):
    """
    Run weekly backtesting
    """
    print(f"Backtesting {ticker} from {start_date} to {end_date}")

    dates = generate_weekly_dates(start_date, end_date)
    print(f"Total weeks to analyze: {len(dates)}")

    # Initialize TradingAgents
    config = DEFAULT_CONFIG.copy()
    config["quick_think_llm"] = "gpt-4o-mini"
    config["deep_think_llm"] = "gpt-4o-mini"

    ta = TradingAgentsGraph(debug=False, config=config)

    results = []

    for i, date in enumerate(dates, 1):
        print(f"\n[{i}/{len(dates)}] Analyzing {date}...")

        try:
            # WORKAROUND: Clear cache before each run
            import os
            import shutil
            cache_path = os.path.expanduser("~/.cache/py-yfinance-cache/")
            if os.path.exists(cache_path):
                shutil.rmtree(cache_path)

            final_state, decision = ta.propagate(ticker, date)

            results.append({
                "date": date,
                "decision": decision,
                "success": True
            })

            print(f"  Decision: {decision}")

        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
            results.append({
                "date": date,
                "error": str(e),
                "success": False
            })

        # Wait between analyses
        if i < len(dates):
            time.sleep(15)

    return results

# Example usage (only run if cache issue resolved)
if __name__ == "__main__":
    # WARNING: This may fail due to cache corruption
    results = backtest_weekly("NVDA", "2024-01-01", "2024-03-31")

    # Analyze results
    successful = [r for r in results if r["success"]]
    print(f"\n✅ Successful analyses: {len(successful)}/{len(results)}")

    if successful:
        decisions = [r["decision"] for r in successful]
        print(f"BUY: {decisions.count('BUY')}")
        print(f"HOLD: {decisions.count('HOLD')}")
        print(f"SELL: {decisions.count('SELL')}")
```

---

### METRICS TO TRACK (30 min)

If you can run backtesting, calculate these metrics:

```python
def calculate_backtest_metrics(results, returns_data):
    """
    Calculate backtesting performance metrics
    """
    # 1. Accuracy: Did decision match forward return direction?
    correct = 0
    total = 0

    for r in results:
        if r["success"] and r["date"] in returns_data:
            forward_return = returns_data[r["date"]]
            decision = r["decision"]

            if (decision == "BUY" and forward_return > 0) or \
               (decision == "SELL" and forward_return < 0) or \
               (decision == "HOLD" and abs(forward_return) < 3):
                correct += 1
            total += 1

    accuracy = (correct / total * 100) if total > 0 else 0

    # 2. Return if we followed all BUY decisions
    buy_returns = [returns_data[r["date"]] for r in results
                   if r["success"] and r["decision"] == "BUY" and r["date"] in returns_data]

    avg_buy_return = sum(buy_returns) / len(buy_returns) if buy_returns else 0

    # 3. Max drawdown from SELL decisions we avoided
    sell_returns = [returns_data[r["date"]] for r in results
                    if r["success"] and r["decision"] == "SELL" and r["date"] in returns_data]

    avoided_losses = sum(r for r in sell_returns if r < 0)

    print("="*70)
    print("BACKTEST METRICS")
    print("="*70)
    print(f"Accuracy: {accuracy:.1f}%")
    print(f"Average BUY return: {avg_buy_return:+.2f}%")
    print(f"Avoided losses from SELL: {avoided_losses:+.2f}%")
```

---

### DELIVERABLES

By the end of Path D, you should have:

1. ✅ `historical_validation.py` with single-date validation
2. ✅ `weekly_backtesting.py` (if cache issue resolved)
3. ✅ Validation results for 4-5 historical decisions
4. ✅ Written analysis of decision quality
5. ✅ Metrics calculation (accuracy, returns, etc.)
6. ✅ Understanding of system limitations

---

### LEARNING OUTCOMES

After completing Path D, you will:
- ✅ Understand how to validate trading decisions historically
- ✅ Know key backtesting metrics (accuracy, returns, drawdown)
- ✅ Understand system failure modes and data limitations
- ✅ Be able to assess decision quality objectively
- ✅ Know how to work around technical limitations

==========================================================================
PATH E: CUSTOM STRATEGY DEVELOPMENT ⭐⭐⭐⭐⭐
==========================================================================

**Difficulty**: Advanced
**Duration**: 3-5 hours

**Objective**:
Build custom trading strategies by modifying agent prompts, adding new
indicators, or creating entirely new agent types.

**What You'll Learn**:
- Prompt engineering for trading agents
- How to add custom technical indicators
- Creating new analyst types
- Modifying debate behavior
- Advanced system customization

---

### PROJECT 1: Add Custom Technical Indicator (60 min)

**Goal**: Add Fibonacci retracement levels to Market Analyst

**Step 1**: Create the tool function

Create `tradingagents/tools/fibonacci_retracement.py`:

```python
"""
Fibonacci Retracement Levels Tool
"""

from langchain_core.tools import tool
import pandas as pd

@tool
def get_fibonacci_levels(ticker: str, date: str, lookback_days: int = 100) -> str:
    """
    Calculate Fibonacci retracement levels for a stock.

    Fibonacci levels (23.6%, 38.2%, 50%, 61.8%, 78.6%) help identify
    potential support and resistance levels.

    Args:
        ticker: Stock ticker symbol (e.g., "AAPL")
        date: Date in YYYY-MM-DD format
        lookback_days: Number of days to look back for high/low (default: 100)

    Returns:
        String with Fibonacci levels and current price position
    """
    from tradingagents.tools.data_vendors.vendor_router import VendorRouter

    try:
        vendor = VendorRouter()

        # Get price data
        prices = vendor.get_price_data(ticker, date, period=f"{lookback_days}d")

        if prices.empty:
            return f"No price data available for {ticker}"

        # Find swing high and swing low
        swing_high = prices['High'].max()
        swing_low = prices['Low'].min()
        diff = swing_high - swing_low

        # Calculate Fibonacci levels
        levels = {
            "0.0% (Low)": swing_low,
            "23.6%": swing_low + (diff * 0.236),
            "38.2%": swing_low + (diff * 0.382),
            "50.0%": swing_low + (diff * 0.500),
            "61.8%": swing_low + (diff * 0.618),
            "78.6%": swing_low + (diff * 0.786),
            "100.0% (High)": swing_high
        }

        # Current price
        current_price = prices['Close'].iloc[-1]

        # Find which level current price is near
        closest_level = min(levels.items(),
                          key=lambda x: abs(x[1] - current_price))

        result = f"Fibonacci Retracement Levels for {ticker}:\n"
        result += f"  Period: Last {lookback_days} days\n"
        result += f"  Swing High: ${swing_high:.2f}\n"
        result += f"  Swing Low:  ${swing_low:.2f}\n"
        result += f"  Current Price: ${current_price:.2f}\n\n"
        result += "Levels:\n"

        for level_name, level_price in levels.items():
            marker = " <-- Current" if level_name == closest_level[0] else ""
            result += f"  {level_name:15} ${level_price:7.2f}{marker}\n"

        # Interpretation
        if current_price > levels["61.8%"]:
            interpretation = "Price is in upper range - potential resistance ahead"
        elif current_price < levels["38.2%"]:
            interpretation = "Price is in lower range - potential support nearby"
        else:
            interpretation = "Price is in middle range - watch for breakout direction"

        result += f"\nInterpretation: {interpretation}"

        return result

    except Exception as e:
        return f"Error calculating Fibonacci levels: {str(e)}"
```

**Step 2**: Add to Market Analyst

Edit `tradingagents/agents/analysts/market_analyst.py`:

```python
# Add import at top
from tradingagents.tools.fibonacci_retracement import get_fibonacci_levels

# Find the tools list and add:
tools = [
    get_stock_data,
    get_indicators,
    get_fibonacci_levels,  # <-- ADD THIS
]

# Update system message to mention Fibonacci:
system_message = f"""You are a technical market analyst...
...
You have access to tools for price data, technical indicators,
and Fibonacci retracement levels.
...
"""
```

**Step 3**: Test it

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

config = DEFAULT_CONFIG.copy()
ta = TradingAgentsGraph(debug=True, config=config)

# Run analysis - watch for Fibonacci tool call in debug output
final_state, decision = ta.propagate("NVDA", "2024-05-10")
```

---

### PROJECT 2: Create a Macroeconomic Analyst (90 min)

**Goal**: Add a 5th analyst that considers macro conditions

**Step 1**: Create macro data tools

Create `tradingagents/tools/macro_indicators.py`:

```python
"""
Macroeconomic Indicators Tools
"""

from langchain_core.tools import tool
import requests

@tool
def get_interest_rates(date: str) -> str:
    """
    Get current Federal Reserve interest rates.

    Args:
        date: Date in YYYY-MM-DD format

    Returns:
        Current Fed Funds Rate and recent changes
    """
    # In real implementation, use FRED API or similar
    # For demo, return mock data

    return """Federal Reserve Interest Rates:

Current Fed Funds Rate: 5.25% - 5.50%
Previous Rate: 5.00% - 5.25%
Change: +0.25% (last meeting)

Recent History:
  - 2024 Q1: Held steady at 5.25-5.50%
  - 2023 Q4: Raised +0.25%
  - 2023 Q3: Raised +0.25%

Interpretation:
The Fed is maintaining a restrictive stance to combat inflation.
Higher rates increase borrowing costs and can pressure stock valuations,
especially for growth stocks.
"""

@tool
def get_inflation_data(date: str) -> str:
    """
    Get Consumer Price Index (CPI) inflation data.

    Args:
        date: Date in YYYY-MM-DD format

    Returns:
        Recent CPI data and trends
    """
    return """Consumer Price Index (CPI) Data:

Current CPI (YoY): 3.2%
Previous Month: 3.4%
Target: 2.0%

Breakdown:
  - Core CPI (ex-food & energy): 3.8%
  - Energy: -2.1%
  - Food: +2.4%
  - Housing: +5.9%

Trend: Inflation is declining but remains above Fed's target.
This suggests the Fed will maintain higher rates longer, which can
pressure stock valuations.
"""

@tool
def get_gdp_growth(date: str) -> str:
    """
    Get GDP growth data.

    Args:
        date: Date in YYYY-MM-DD format

    Returns:
        Recent GDP data and economic growth trends
    """
    return """GDP Growth Data:

Current Quarter: +2.1% (annualized)
Previous Quarter: +2.4%
Year Ago: +1.9%

Components:
  - Consumer Spending: +2.8%
  - Business Investment: +1.4%
  - Government Spending: -0.5%
  - Net Exports: +0.2%

Interpretation:
Economy showing moderate growth. Consumer spending remains strong
despite higher interest rates, suggesting resilience. However, business
investment is slowing, which could impact future growth.
"""
```

**Step 2**: Create Macroeconomic Analyst

Create `tradingagents/agents/analysts/macro_analyst.py`:

```python
"""
Macroeconomic Analyst Agent
Analyzes macroeconomic conditions and their impact on stocks
"""

from langchain_core.messages import HumanMessage
from tradingagents.tools.macro_indicators import (
    get_interest_rates,
    get_inflation_data,
    get_gdp_growth
)

def create_macro_analyst(llm):
    """
    Create macroeconomic analyst agent

    Args:
        llm: Language model for the analyst

    Returns:
        Agent node function
    """

    def macro_analyst_node(state):
        """
        Analyze macroeconomic conditions
        """
        company = state["company_of_interest"]
        date = state["trade_date"]

        system_message = f"""You are a macroeconomic analyst specializing in
understanding how broader economic conditions impact individual stocks.

Your role is to:
1. Assess current macroeconomic conditions (interest rates, inflation, GDP)
2. Analyze how these conditions affect {company} specifically
3. Consider sector-specific impacts (tech, finance, consumer, etc.)
4. Provide context for other analysts' findings

You have access to tools for:
- Federal Reserve interest rates
- Inflation (CPI) data
- GDP growth data

Provide a concise macro analysis report with:
- Current macro environment summary
- Impact on {company}'s sector
- Risks and opportunities from macro perspective
- Recommendation: MACRO_POSITIVE, MACRO_NEUTRAL, or MACRO_NEGATIVE

Be specific about HOW macro conditions affect this particular stock.
"""

        # Bind tools to LLM
        tools = [get_interest_rates, get_inflation_data, get_gdp_growth]
        llm_with_tools = llm.bind_tools(tools)

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"Analyze macroeconomic conditions for {company} on {date}"}
        ]

        # Agent loop (ReAct pattern)
        for _ in range(5):  # Max 5 iterations
            result = llm_with_tools.invoke(messages)
            messages.append(result)

            # Check if done (no more tool calls)
            if not result.tool_calls:
                break

            # Execute tool calls
            for tool_call in result.tool_calls:
                tool = next(t for t in tools if t.name == tool_call["name"])
                tool_result = tool.invoke(tool_call["args"])
                messages.append({
                    "role": "tool",
                    "content": tool_result,
                    "tool_call_id": tool_call["id"]
                })

        # Extract final report
        final_report = result.content

        return {
            "messages": [HumanMessage(content=final_report)],
            "macro_report": final_report
        }

    return macro_analyst_node
```

**Step 3**: Integrate into workflow

Edit `tradingagents/graph/setup.py`:

1. Import the new analyst:
```python
from tradingagents.agents.analysts.macro_analyst import create_macro_analyst
```

2. Add to graph:
```python
# In create_trading_graph function, after other analysts:
graph.add_node("macro_analyst", create_macro_analyst(llm_quick))
```

3. Add to workflow:
```python
# Add parallel edge from START
graph.add_edge(START, "macro_analyst")

# Add conditional edge to join with other analysts
# (This part requires more integration with the existing flow)
```

**Step 4**: Update AgentState

Edit `tradingagents/agents/utils/agent_states.py`:

```python
class AgentState(TypedDict):
    # ... existing fields ...
    macro_report: str  # <-- ADD THIS
```

**Step 5**: Test the new analyst

```python
from tradingagents.graph.trading_graph import TradingAgentsGraph

ta = TradingAgentsGraph(debug=True)
final_state, decision = ta.propagate("NVDA", "2024-05-10")

# Check macro_report in final_state
print("\n" + "="*70)
print("MACRO ANALYSIS:")
print("="*70)
print(final_state.get("macro_report", "No macro report"))
```

---

### PROJECT 3: Modify Bull/Bear Debate Behavior (60 min)

**Goal**: Make debates more aggressive/detailed

Edit `tradingagents/agents/researchers/bull_researcher.py`:

```python
# Find system message and modify:

system_message = f"""You are an AGGRESSIVE bull researcher who strongly
advocates for buying {company}.

Your debating style:
- Use STRONG, CONFIDENT language
- Challenge bear arguments directly and specifically
- Find 3-5 concrete reasons to buy
- Use data from analyst reports to support your case
- Counter every bear concern with a bull rebuttal
- Make your argument PERSUASIVE and COMPELLING

IMPORTANT RULES:
1. Each argument should cite specific data points
2. Address the bear's previous arguments point-by-point
3. Use phrases like "The data clearly shows...", "Bear argument ignores..."
4. Build momentum - each round should be MORE convincing than the last
5. End with a CLEAR, ACTION-ORIENTED recommendation

You are in a debate. Your goal is to WIN the debate, not just participate.
Make the research manager WANT to choose BUY.
"""
```

Similarly for `bear_researcher.py`:

```python
system_message = f"""You are a SKEPTICAL bear researcher who identifies
serious risks and reasons to avoid buying {company}.

Your debating style:
- Point out SPECIFIC risks that bulls overlook
- Use data to show vulnerabilities
- Challenge bull optimism with realistic concerns
- Find 3-5 concrete reasons to sell or avoid
- Counter every bull point with a risk analysis
- Make your case COMPELLING and data-driven

IMPORTANT RULES:
1. Each argument should cite specific risks or data points
2. Address the bull's previous arguments directly
3. Use phrases like "Bulls are overlooking...", "The data reveals..."
4. Escalate concerns - each round should reveal NEW risks
5. End with a CLEAR warning about the risks

You are in a debate. Your goal is to WIN by showing the risks clearly.
"""
```

Test to see if debates become more detailed and adversarial.

---

### PROJECT 4: Create a "Devil's Advocate" Node (90 min)

**Goal**: Add a node that challenges the final decision before it's made

Create `tradingagents/agents/devil_advocate.py`:

```python
"""
Devil's Advocate Agent
Challenges the proposed decision to ensure robustness
"""

def create_devil_advocate(llm):
    """
    Create devil's advocate agent that challenges decisions
    """

    def devil_advocate_node(state):
        """
        Challenge the proposed decision
        """
        company = state["company_of_interest"]
        decision = state.get("trader_investment_plan", "")
        investment_plan = state.get("investment_plan", "")

        # Extract the proposed action
        if "BUY" in decision.upper():
            action = "BUY"
        elif "SELL" in decision.upper():
            action = "SELL"
        else:
            action = "HOLD"

        system_message = f"""You are a devil's advocate whose job is to
challenge the proposed trading decision for {company}.

The team has proposed: {action}

Your role:
1. Identify 3-5 specific reasons why this decision could be WRONG
2. Point out what the team might be MISSING or OVERLOOKING
3. Challenge assumptions in the analysis
4. Highlight contradictions or weaknesses
5. Consider alternative scenarios where this decision fails

Be CRITICAL but CONSTRUCTIVE. Your goal is to stress-test the decision,
not just to be negative.

After your critique, provide:
- Overall Assessment: CHALLENGE SUCCESSFUL / DECISION HOLDS
- Confidence: LOW / MEDIUM / HIGH
- Recommendation: PROCEED / RECONSIDER / REVERSE

Be thorough and specific.
"""

        messages = [
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"""
Investment Plan:
{investment_plan}

Trader Decision:
{decision}

Challenge this decision. What could go wrong? What are we missing?
"""}
        ]

        result = llm.invoke(messages)
        critique = result.content

        print("\n" + "="*70)
        print("DEVIL'S ADVOCATE CRITIQUE:")
        print("="*70)
        print(critique)

        return {
            "messages": [HumanMessage(content=critique)],
            "devil_advocate_critique": critique
        }

    return devil_advocate_node
```

Add to workflow between trader and risk analysts to strengthen decision quality.

---

### EXERCISES

**Exercise 1**: Add Relative Strength Index (RSI) divergence detection
**Exercise 2**: Create a "Sector Analyst" that compares to sector peers
**Exercise 3**: Add "Whale Tracking" - monitor institutional holdings
**Exercise 4**: Create "Options Flow Analyst" for options market sentiment
**Exercise 5**: Build "Earnings Surprise" analyzer

---

### DELIVERABLES

By the end of Path E, you should have:

1. ✅ At least one custom technical indicator
2. ✅ One new analyst type (macro, sector, etc.)
3. ✅ Modified debate behavior
4. ✅ Optional: Devil's advocate or other custom node
5. ✅ Documentation of your changes
6. ✅ Test results comparing original vs custom system

---

### LEARNING OUTCOMES

After completing Path E, you will:
- ✅ Understand how to modify agent behavior through prompts
- ✅ Know how to add new tools and indicators
- ✅ Be able to create entirely new agent types
- ✅ Understand system architecture deeply
- ✅ Have built custom trading strategies
- ✅ Be prepared for advanced AI agent development

==========================================================================
PATH F: DEBATE ANALYSIS & VISUALIZATION ⭐⭐⭐
==========================================================================

**Difficulty**: Moderate-Advanced
**Duration**: 2-3 hours

**Objective**:
Analyze and visualize agent debates to understand decision dynamics,
identify patterns, and improve system transparency.

**What You'll Learn**:
- Debate extraction and parsing
- Visualization techniques for multi-agent systems
- Pattern recognition in arguments
- Decision flow analysis

**Note**: You already have `visualize_risk_debate.py` from Session 2!
This path extends that work.

---

### PROJECT 1: Investment Debate Visualizer (60 min)

Extend your existing visualizer to show investment debates:

Create `visualize_investment_debate.py`:

```python
#!/usr/bin/env python3
"""
Visualize Bull vs Bear investment debate
"""

import json
import sys

def load_decision_log(date):
    """Load the full decision log"""
    filename = f"full_states_log_{date}.json"
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Could not find {filename}")
        print("Run a decision first with the date you want to visualize")
        return None

def extract_investment_debate(states):
    """Extract bull and bear arguments from states"""

    bull_args = []
    bear_args = []
    final_decision = None

    for state in states:
        # Look for debate state
        debate_state = state.get("investment_debate_state", {})

        if "bull_history" in debate_state:
            bull_args = debate_state["bull_history"]
        if "bear_history" in debate_state:
            bear_args = debate_state["bear_history"]

        # Look for manager decision
        if "investment_plan" in state and state["investment_plan"]:
            final_decision = state["investment_plan"]

    return bull_args, bear_args, final_decision

def visualize_debate(bull_args, bear_args, final_decision):
    """Display the debate in a readable format"""

    print("="*70)
    print("BULL VS BEAR INVESTMENT DEBATE VISUALIZATION")
    print("="*70)

    max_rounds = max(len(bull_args), len(bear_args))

    for round_num in range(max_rounds):
        print(f"\n{'='*70}")
        print(f"ROUND {round_num + 1}")
        print(f"{'='*70}\n")

        # Bull argument
        if round_num < len(bull_args):
            print("🐂 BULL RESEARCHER:")
            print("-" * 70)
            print(bull_args[round_num])
            print()

        # Bear argument
        if round_num < len(bear_args):
            print("🐻 BEAR RESEARCHER:")
            print("-" * 70)
            print(bear_args[round_num])
            print()

    # Final decision
    if final_decision:
        print("\n" + "="*70)
        print("⚖️  RESEARCH MANAGER'S DECISION")
        print("="*70)
        print(final_decision)

    # Analysis
    print("\n" + "="*70)
    print("DEBATE ANALYSIS")
    print("="*70)

    print(f"Total rounds: {max_rounds}")
    print(f"Bull arguments: {len(bull_args)}")
    print(f"Bear arguments: {len(bear_args)}")

    # Count keywords in each side
    bull_text = " ".join(bull_args).lower()
    bear_text = " ".join(bear_args).lower()

    bull_keywords = {
        "growth": bull_text.count("growth"),
        "opportunity": bull_text.count("opportunity"),
        "positive": bull_text.count("positive"),
        "strong": bull_text.count("strong"),
        "buy": bull_text.count("buy")
    }

    bear_keywords = {
        "risk": bear_text.count("risk"),
        "concern": bear_text.count("concern"),
        "negative": bear_text.count("negative"),
        "weak": bear_text.count("weak"),
        "sell": bear_text.count("sell")
    }

    print("\nBull Emphasis:")
    for keyword, count in sorted(bull_keywords.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {keyword}: {count} mentions")

    print("\nBear Emphasis:")
    for keyword, count in sorted(bear_keywords.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {keyword}: {count} mentions")

def main():
    if len(sys.argv) < 2:
        print("Usage: python visualize_investment_debate.py <date>")
        print("Example: python visualize_investment_debate.py 2024-05-10")
        sys.exit(1)

    date = sys.argv[1]

    states = load_decision_log(date)
    if not states:
        sys.exit(1)

    bull_args, bear_args, final_decision = extract_investment_debate(states)

    if not bull_args and not bear_args:
        print("❌ No investment debate found in this log")
        sys.exit(1)

    visualize_debate(bull_args, bear_args, final_decision)

if __name__ == "__main__":
    main()
```

Usage:
```bash
python visualize_investment_debate.py 2024-05-10
```

---

### PROJECT 2: Debate Comparison Tool (45 min)

Compare debates across multiple stocks:

Create `compare_debates.py`:

```python
#!/usr/bin/env python3
"""
Compare debates across multiple stock analyses
"""

import json
import glob

def load_all_decisions():
    """Load all available decision logs"""
    files = glob.glob("full_states_log_*.json")

    decisions = []
    for filename in files:
        with open(filename, 'r') as f:
            data = json.load(f)

            # Extract key info
            if data and len(data) > 0:
                first_state = data[0]
                ticker = first_state.get("company_of_interest", "UNKNOWN")
                date = first_state.get("trade_date", "UNKNOWN")

                # Find final decision
                final_decision = "UNKNOWN"
                for state in reversed(data):
                    if "final_decision" in state and state["final_decision"]:
                        # Extract BUY/SELL/HOLD
                        decision_text = state["final_decision"]
                        if "BUY" in decision_text.upper():
                            final_decision = "BUY"
                        elif "SELL" in decision_text.upper():
                            final_decision = "SELL"
                        elif "HOLD" in decision_text.upper():
                            final_decision = "HOLD"
                        break

                # Extract debate length
                debate_state = {}
                for state in data:
                    if "investment_debate_state" in state:
                        debate_state = state["investment_debate_state"]
                        break

                bull_rounds = len(debate_state.get("bull_history", []))
                bear_rounds = len(debate_state.get("bear_history", []))

                decisions.append({
                    "ticker": ticker,
                    "date": date,
                    "decision": final_decision,
                    "bull_rounds": bull_rounds,
                    "bear_rounds": bear_rounds,
                    "filename": filename
                })

    return decisions

def compare_decisions(decisions):
    """Compare decisions across stocks"""

    print("="*70)
    print("MULTI-STOCK DEBATE COMPARISON")
    print("="*70)
    print(f"\nTotal analyses: {len(decisions)}\n")

    # Summary table
    print(f"{'Ticker':<8} {'Date':<12} {'Decision':<8} {'Bull Rounds':<12} {'Bear Rounds':<12}")
    print("-" * 70)

    for d in sorted(decisions, key=lambda x: x['ticker']):
        print(f"{d['ticker']:<8} {d['date']:<12} {d['decision']:<8} {d['bull_rounds']:<12} {d['bear_rounds']:<12}")

    # Statistics
    print("\n" + "="*70)
    print("STATISTICS")
    print("="*70)

    decision_counts = {}
    for d in decisions:
        decision_counts[d['decision']] = decision_counts.get(d['decision'], 0) + 1

    print("\nDecision Distribution:")
    for decision, count in sorted(decision_counts.items()):
        pct = (count / len(decisions)) * 100
        print(f"  {decision}: {count}/{len(decisions)} ({pct:.0f}%)")

    avg_bull_rounds = sum(d['bull_rounds'] for d in decisions) / len(decisions)
    avg_bear_rounds = sum(d['bear_rounds'] for d in decisions) / len(decisions)

    print(f"\nAverage debate rounds:")
    print(f"  Bull: {avg_bull_rounds:.1f}")
    print(f"  Bear: {avg_bear_rounds:.1f}")

def main():
    decisions = load_all_decisions()

    if not decisions:
        print("❌ No decision logs found")
        print("Run some analyses first!")
        return

    compare_decisions(decisions)

if __name__ == "__main__":
    main()
```

This shows patterns across all your analyses.

---

### PROJECT 3: Argument Strength Analyzer (60 min)

Use an LLM to rate argument quality:

Create `analyze_argument_strength.py`:

```python
#!/usr/bin/env python3
"""
Use LLM to analyze argument strength in debates
"""

import json
import sys
from openai import OpenAI
import os

def load_debate(date):
    """Load debate from decision log"""
    filename = f"full_states_log_{date}.json"
    with open(filename, 'r') as f:
        states = json.load(f)

    for state in states:
        if "investment_debate_state" in state:
            debate = state["investment_debate_state"]
            return debate.get("bull_history", []), debate.get("bear_history", [])

    return [], []

def rate_argument(argument, side):
    """
    Use GPT to rate argument quality
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""Rate the following {side} trading argument on these criteria:

1. Data-driven (uses specific numbers/metrics): 1-10
2. Logical coherence (reasoning makes sense): 1-10
3. Persuasiveness (compelling and convincing): 1-10
4. Specific (not vague or generic): 1-10
5. Addresses counterarguments: 1-10

Argument:
{argument}

Provide ratings as JSON:
{{
  "data_driven": X,
  "logical": X,
  "persuasive": X,
  "specific": X,
  "addresses_counter": X,
  "overall": X,
  "strengths": "brief description",
  "weaknesses": "brief description"
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    # Parse JSON from response
    result_text = response.choices[0].message.content
    # Extract JSON (might be wrapped in markdown)
    if "```json" in result_text:
        result_text = result_text.split("```json")[1].split("```")[0]
    elif "```" in result_text:
        result_text = result_text.split("```")[1].split("```")[0]

    return json.loads(result_text.strip())

def analyze_debate_quality(bull_args, bear_args):
    """
    Analyze quality of both sides
    """
    print("="*70)
    print("ARGUMENT QUALITY ANALYSIS")
    print("="*70)

    bull_ratings = []
    bear_ratings = []

    print("\nAnalyzing Bull Arguments...")
    for i, arg in enumerate(bull_args, 1):
        print(f"  Rating argument {i}/{len(bull_args)}...")
        rating = rate_argument(arg, "bull")
        rating["round"] = i
        bull_ratings.append(rating)

    print("\nAnalyzing Bear Arguments...")
    for i, arg in enumerate(bear_args, 1):
        print(f"  Rating argument {i}/{len(bear_args)}...")
        rating = rate_argument(arg, "bear")
        rating["round"] = i
        bear_ratings.append(rating)

    # Display results
    print("\n" + "="*70)
    print("BULL ARGUMENT RATINGS")
    print("="*70)

    for rating in bull_ratings:
        print(f"\nRound {rating['round']}:")
        print(f"  Data-driven: {rating['data_driven']}/10")
        print(f"  Logical: {rating['logical']}/10")
        print(f"  Persuasive: {rating['persuasive']}/10")
        print(f"  Specific: {rating['specific']}/10")
        print(f"  Addresses counter: {rating['addresses_counter']}/10")
        print(f"  Overall: {rating['overall']}/10")
        print(f"  Strengths: {rating['strengths']}")
        print(f"  Weaknesses: {rating['weaknesses']}")

    print("\n" + "="*70)
    print("BEAR ARGUMENT RATINGS")
    print("="*70)

    for rating in bear_ratings:
        print(f"\nRound {rating['round']}:")
        print(f"  Data-driven: {rating['data_driven']}/10")
        print(f"  Logical: {rating['logical']}/10")
        print(f"  Persuasive: {rating['persuasive']}/10")
        print(f"  Specific: {rating['specific']}/10")
        print(f"  Addresses counter: {rating['addresses_counter']}/10")
        print(f"  Overall: {rating['overall']}/10")
        print(f"  Strengths: {rating['strengths']}")
        print(f"  Weaknesses: {rating['weaknesses']}")

    # Overall comparison
    print("\n" + "="*70)
    print("OVERALL COMPARISON")
    print("="*70)

    if bull_ratings:
        bull_avg = sum(r['overall'] for r in bull_ratings) / len(bull_ratings)
        print(f"Bull average quality: {bull_avg:.1f}/10")

    if bear_ratings:
        bear_avg = sum(r['overall'] for r in bear_ratings) / len(bear_ratings)
        print(f"Bear average quality: {bear_avg:.1f}/10")

    if bull_ratings and bear_ratings:
        if bull_avg > bear_avg:
            print(f"\n✅ Bull arguments were stronger (by {bull_avg - bear_avg:.1f} points)")
        elif bear_avg > bull_avg:
            print(f"\n✅ Bear arguments were stronger (by {bear_avg - bull_avg:.1f} points)")
        else:
            print(f"\n⚖️  Arguments were equally strong")

def main():
    if len(sys.argv) < 2:
        print("Usage: python analyze_argument_strength.py <date>")
        sys.exit(1)

    date = sys.argv[1]

    bull_args, bear_args = load_debate(date)

    if not bull_args and not bear_args:
        print("❌ No debate found")
        sys.exit(1)

    analyze_debate_quality(bull_args, bear_args)

if __name__ == "__main__":
    main()
```

This uses GPT to objectively rate argument quality!

---

### DELIVERABLES

By the end of Path F, you should have:

1. ✅ `visualize_investment_debate.py` - Investment debate visualizer
2. ✅ `compare_debates.py` - Multi-stock comparison
3. ✅ `analyze_argument_strength.py` - LLM-based quality analysis
4. ✅ Extended `visualize_risk_debate.py` from Session 2
5. ✅ Analysis of debate patterns across multiple stocks
6. ✅ Insights on which arguments work best

---

### LEARNING OUTCOMES

After completing Path F, you will:
- ✅ Understand debate dynamics in detail
- ✅ Know how to extract and visualize agent interactions
- ✅ Be able to assess argument quality objectively
- ✅ Identify patterns in successful vs unsuccessful arguments
- ✅ Have tools for system transparency and explainability

==========================================================================
PATHS G & H: PRODUCTION & FINAL PROJECT
==========================================================================

**Note**: These paths are for advanced users ready to deploy or build
comprehensive systems. They require significant time and technical depth.

### PATH G: Production-Ready Pipeline ⭐⭐⭐⭐⭐

**Duration**: 4-6 hours

**Objective**: Deploy an automated trading analysis pipeline with:
- Scheduled daily/weekly analyses
- Email/Slack notifications
- Monitoring and logging
- Error handling and recovery
- Dashboard for results

**Topics**:
- Cron jobs or scheduled tasks
- Alert systems (email, Slack webhooks)
- Logging best practices
- Database for storing decisions
- Web dashboard (Flask or Streamlit)
- Docker containerization

**Deliverables**:
- Automated scheduling script
- Notification system
- Results dashboard
- Documentation for deployment
- Monitoring/alerting setup

---

### PATH H: Comprehensive Final Project ⭐⭐⭐⭐

**Duration**: 4-8 hours

**Objective**: Build a complete portfolio management system that combines
everything you've learned:

**Features**:
- Multi-stock portfolio analysis
- Automated rebalancing recommendations
- Risk assessment and position sizing
- Historical performance tracking
- Custom strategies and indicators
- Full documentation
- Unit tests
- Deployment-ready

**Components**:
1. Portfolio configuration and management
2. Automated analysis pipeline
3. Decision aggregation and weighting
4. Risk-adjusted allocation
5. Performance tracking and reporting
6. Web interface or API
7. Documentation and tests

This is a capstone project that demonstrates mastery of the system.

==========================================================================
RECOMMENDED LEARNING PATH
==========================================================================

Based on your completed Phases 1-3, here's the recommended order:

**Week 1 (4-6 hours)**:
✅ Already Complete: Phases 1-3

**Week 2 (2-3 hours)**:
1. **Path A**: Multi-Stock Portfolio Analysis
   - Quick wins, immediate value
   - Solidifies everything learned
   - 1-2 hours

2. **Path F**: Debate Analysis & Visualization (partial)
   - Extend your visualize_risk_debate.py
   - Add investment debate visualizer
   - 1 hour

**Week 3 (3-4 hours)**:
3. **Path B**: Configuration Experimentation
   - Optimize your setup
   - Understand tradeoffs
   - 2-3 hours

4. **Path D**: Historical Validation (partial)
   - Single-date validation approach
   - 1 hour

**Week 4 (3-5 hours)**:
5. **Path E**: Custom Strategy Development
   - Add your own indicators/analysts
   - 2-3 hours

6. **Path C**: Multi-LLM Comparison (optional, if you have API keys)
   - 2 hours

**Week 5+**:
7. **Path G or H**: Production deployment or final project
   - When you're ready for real application

==========================================================================
GETTING STARTED WITH YOUR NEXT SESSION
==========================================================================

**Immediate Next Step**: Path A - Multi-Stock Portfolio Analysis

**Why Start Here**:
1. Uses everything you've learned
2. Quick to complete (1-2 hours)
3. Immediate satisfying results
4. Foundation for advanced work
5. No additional setup needed

**How to Begin**:
1. Copy the `multi_stock_analysis.py` script from Path A above
2. Customize the PORTFOLIO dictionary with stocks you're interested in
3. Run it: `python multi_stock_analysis.py`
4. Analyze results
5. Complete the exercises

**Then**:
- Come back and choose your next path
- Or combine multiple paths based on your interests
- Or create your own custom path

==========================================================================
SUPPORT & TROUBLESHOOTING
==========================================================================

**Known Issues**:
1. yfinance cache corruption (see Session 2 transcript)
   - Workaround: Delete cache before each run
   - Alternative: Use alpha_vantage

2. Unicode encoding errors (already fixed in Session 1)

3. API rate limits
   - Add delays between analyses (10-15 seconds)
   - Use caching where possible

**Resources**:
- Session 1 & 2 transcripts for reference
- LEARNING_SESSION_SUMMARY.md (created in Session 2)
- RISK_MANAGEMENT_ANALYSIS.md (created in Session 2)
- Original LEARNING_PATH.md for architecture deep dives

**Questions?**:
Refer back to previous session transcripts or documentation files.

==========================================================================
FINAL NOTES
==========================================================================

You've completed a significant learning journey through Phases 1-3:
- ✅ Setup and basic understanding
- ✅ Architecture and agent comprehension
- ✅ Memory systems and learning
- ✅ Advanced risk management

You're now ready for **practical application and experimentation**.

**Remember**:
- This is a research and education framework
- Not for live trading without extensive validation
- Focus on learning and understanding
- Experiment freely and build confidently

**Have fun with Phase 4!** 🚀

==========================================================================
