import time
import json


def create_research_manager_balanced(llm, memory):
    """
    BALANCED VERSION: Gives equal weight to bull and bear arguments
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

        prompt = f"""As the portfolio manager and debate facilitator, your role is to objectively evaluate this debate and make a well-reasoned decision: Buy, Hold, or Sell.

IMPORTANT: Give EQUAL WEIGHT to both bull and bear arguments. Do not automatically favor caution or risk aversion. Evaluate the evidence objectively and let the data guide your decision.

Guidelines for your decision:
- If growth indicators are strong and risks are manageable → BUY
- If decline is likely or risks significantly outweigh opportunities → SELL
- If evidence is mixed or uncertain, or the stock is fairly valued → HOLD

Summarize the key points from both sides concisely, focusing on the most compelling evidence. Your recommendation must be clear and actionable, but it should reflect balanced judgment rather than defaulting to the bearish view.

Additionally, develop a detailed investment plan for the trader. This should include:

Your Recommendation: A balanced stance supported by objective evaluation of both bull and bear arguments.
Rationale: An explanation that acknowledges both perspectives and explains why the evidence tilts one direction.
Strategic Actions: Concrete steps for implementing the recommendation.

Take into account your past mistakes on similar situations. Be especially mindful of times when you were too cautious and missed opportunities, or too aggressive and ignored risks. Use these insights to refine your decision-making.

Here are your past reflections on mistakes:
"{past_memory_str}"

Here is the debate:
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
