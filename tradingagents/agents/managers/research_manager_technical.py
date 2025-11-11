import time
import json


def create_research_manager_technical(llm, memory):
    """
    TECHNICAL-FOCUSED VERSION: Emphasizes deterministic technical indicators over subjective debate
    Decision-making is rules-based and data-driven to reduce inconsistency
    """
    def research_manager_node(state) -> dict:
        history = state["investment_debate_state"].get("history", "")
        market_research_report = state["market_report"]
        sentiment_report = state["sentiment_report"]
        news_report = state["news_report"]
        fundamentals_report = state["fundamentals_report"]

        investment_debate_state = state["investment_debate_state"]

        curr_situation = f"{market_research_report}\n\n{sentiment_report}\n\n{news_report}\n\n{fundamentals_report}"
        past_memories = memory.get_memories(curr_situation, n_matches=2)

        past_memory_str = ""
        for i, rec in enumerate(past_memories, 1):
            past_memory_str += rec["recommendation"] + "\n\n"

        prompt = f"""As a quantitative portfolio manager, your role is to make data-driven investment decisions based PRIMARILY on technical indicators and objective financial metrics. Subjective narratives and debate arguments should carry LESS weight than hard data.

DECISION FRAMEWORK (Apply in this order):

**Step 1: Technical Indicator Analysis (PRIMARY - 60% weight)**
Extract and analyze these key indicators from the market research report:
- MACD: Positive + rising = bullish | Negative + falling = bearish
- RSI: >70 = overbought (caution) | <30 = oversold (opportunity) | 40-60 = neutral
- Moving Averages: Price above 50-day & 200-day SMA = bullish trend
- Volume: Increasing on up days = confirmation | Decreasing = weakening
- Momentum: Consistent upward momentum = bullish

Technical Signal Summary:
- If 4+ indicators bullish → Strong BUY signal
- If 3-4 indicators bullish, 0-1 bearish → BUY signal
- If 2-3 mixed signals → HOLD signal
- If 3+ indicators bearish → SELL signal

**Step 2: Fundamental Health Check (SECONDARY - 25% weight)**
- Revenue growth: >10% YoY = positive | <0% = negative
- Profit margins: Improving = positive | Declining = negative
- Debt levels: D/E <1.5 = healthy | >2.5 = concerning
- Cash flow: Positive & growing = healthy

**Step 3: Sentiment & News Context (TERTIARY - 15% weight)**
- Only use sentiment/news to confirm or slightly adjust technical signals
- Do NOT override strong technical signals based solely on narrative

**Decision Rules:**
1. If technical indicators give clear signal (4+ agree) → Follow that signal
2. If technical indicators mixed but fundamentals strong → Lean BUY or HOLD
3. If technical indicators mixed but fundamentals weak → Lean SELL or HOLD
4. ALWAYS prioritize objective data over subjective debate arguments
5. When uncertain between BUY/HOLD, check: Is trend clearly up? → BUY. Mixed? → HOLD.
6. When uncertain between SELL/HOLD, check: Is trend clearly down? → SELL. Mixed? → HOLD.

**Bull vs Bear Debate:**
Review the debate arguments ONLY to extract any additional technical insights or data points. Do NOT let persuasive rhetoric override your quantitative analysis.

Debate Summary:
{history}

Past lessons learned:
{past_memory_str}

**YOUR TASK:**
1. Extract technical indicators from market research
2. Count bullish vs bearish signals
3. Check fundamental health
4. Apply decision rules above
5. Make clear recommendation: BUY, HOLD, or SELL

Your recommendation should be PRIMARILY driven by technical indicators. Be consistent and rules-based. Include:
- Recommendation: BUY/HOLD/SELL with confidence level (high/medium/low)
- Technical Indicator Summary: List key indicators and their signals
- Rationale: Explain which rules led to your decision
- Strategic Actions: Concrete next steps"""

        response = llm.invoke(prompt)

        new_investment_debate_state = {
            "judge_decision": response.content,
            "history": investment_debate_state.get("history", ""),
            "bear_history": investment_debate_state.get("bear_history", ""),
            "bull_history": investment_debate_state.get("bull_history", ""),
            "current_response": response.content,
            "count": investment_debate_state["count"],
        }

        return {
            "investment_debate_state": new_investment_debate_state,
            "investment_plan": response.content,
        }

    return research_manager_node
