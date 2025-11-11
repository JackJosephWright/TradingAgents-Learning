import time
import json


def create_research_manager_growth(llm, memory):
    """
    PRO-GROWTH VERSION: Favors growth opportunities in bull markets
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

        prompt = f"""As the portfolio manager and debate facilitator, your role is to evaluate this debate with a growth-oriented mindset appropriate for bull market conditions.

MARKET CONTEXT: We are in a bull market environment where growth stocks and momentum tend to be rewarded. While acknowledging risks is important, do not let fear of potential downsides cause you to miss significant opportunities.

Guidelines for decision-making:
- Strong growth potential + manageable risks = BUY (favor growth when reasonable)
- Declining fundamentals + significant headwinds = SELL
- Mixed signals or fairly valued = HOLD
- When uncertain between BUY and HOLD, lean toward capturing upside in a rising market

Evaluate both the bull and bear arguments, but give additional weight to:
1. Growth potential and revenue momentum
2. Competitive advantages and market position
3. Positive technical indicators and momentum
4. Historical pattern that rising tides lift most boats

Be cautious of overweighting speculative risks that may never materialize. In bull markets, excessive caution often means missing opportunities.

Develop a detailed investment plan including:

Your Recommendation: A growth-focused stance that balances opportunity with prudent risk management.
Rationale: Explain why growth potential justifies the risks, or why risks truly outweigh opportunities.
Strategic Actions: Concrete steps for implementation.

Learn from past mistakes, especially times when excessive caution caused you to miss strong performers. Balance risk awareness with opportunity recognition.

Past reflections on mistakes:
"{past_memory_str}"

Debate History:
{history}"""
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
