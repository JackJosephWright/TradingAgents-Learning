# TradingAgents Learning Path

A structured guide for understanding the TradingAgents framework, from beginner to advanced.

## Learning Approach

This repository is designed for **collaborative learning**. Whether you're new to programming or exploring AI trading systems, this path will help you understand how multi-agent LLM systems work.

## Prerequisites Check

Before starting, verify you understand:
- ✅ Basic Python (functions, classes, dictionaries)
- ✅ Command line basics (cd, ls, running scripts)
- ✅ What APIs are (making requests, getting responses)
- ⚠️ Nice to have: Git basics, virtual environments

**If you're missing these**, that's okay! Reference these as you learn:
- [Python Basics (10 min)](https://www.learnpython.org/)
- [Command Line Crash Course (20 min)](https://developer.mozilla.org/en-US/docs/Learn/Tools_and_testing/Understanding_client-side_tools/Command_line)
- [API Fundamentals (15 min)](https://www.freecodecamp.org/news/what-is-an-api-in-english-please-b880a3214a82/)

---

## Phase 1: Getting Started (Day 1-2)

**Goal**: Get the system running and make your first trading decision

### Step 1: Install and Run (30 min)
1. Follow [INSTALLATION_GUIDE.md](INSTALLATION_GUIDE.md)
2. Get API keys (OpenAI + Alpha Vantage)
3. Run `python main.py`
4. Watch the agents work!

**Success criteria**: You see output from multiple agents and get a final trading recommendation.

### Step 2: Understand What Just Happened (30 min)
Read the terminal output carefully. You should see:
- 4 analyst agents gathering data
- Bull vs Bear debate
- Research manager's decision
- Trader's final recommendation
- Risk analysis team's evaluation

**Exercise**: Run the same command again with a different stock ticker:
```bash
# Edit main.py to change "NVDA" to "AAPL"
python main.py
```

Notice how the agents' reasoning changes based on the company.

### Step 3: Read the Big Picture (1 hour)
Read these sections from [TRADINGAGENTS_DEEP_DIVE.md](../TRADINGAGENTS_DEEP_DIVE.md):
1. Section 1: Overview and Philosophy
2. Section 2: System Architecture
3. Section 4: The Two-Tier LLM Strategy

**Don't worry if you don't understand everything!** Just get familiar with the concepts.

---

## Phase 2: Understanding the Agents (Day 3-5)

**Goal**: Understand how each agent works and what they do

### Step 4: The Four Analysts (2 hours)

Read and experiment with each analyst:

#### Market Analyst
**File**: `tradingagents/agents/analysts/market_analyst.py`

**What it does**: Analyzes price history, technical indicators, trends

**Exercise**:
1. Read lines 1-40 (imports and system message)
2. Find the tools it uses (search for `tools = [...]`)
3. Run the system with debug=True to see its tool calls

**Key concept**: ReAct pattern (Reason → Act → Observe)

#### Sentiment Analyst
**File**: `tradingagents/agents/analysts/sentiment_analyst.py`

**What it does**: Scrapes and analyzes social media sentiment

**Exercise**:
1. Identify what data sources it uses
2. Look at how it formats its report
3. Notice the Markdown table at the end

#### News Analyst
**File**: `tradingagents/agents/analysts/news_analyst.py`

**What it does**: Fetches recent news and analyzes impact

**Exercise**:
1. See how it retrieves news via Alpha Vantage
2. Look at its prompting strategy
3. Compare news analysis for different companies

#### Fundamentals Analyst
**File**: `tradingagents/agents/analysts/fundamentals_analyst.py`

**What it does**: Analyzes financial statements, ratios, company health

**Exercise**:
1. Find the 4 fundamental tools it has access to
2. See how it compares metrics to industry standards
3. Read its system message to understand its role

**Phase 2 Checkpoint**: You should be able to explain what each analyst does in 1-2 sentences.

---

## Phase 3: The Debate System (Day 6-8)

**Goal**: Understand how agents argue and reach decisions

### Step 5: Bull vs Bear Debate (2 hours)

**Files to study**:
- `tradingagents/agents/researchers/bull_researcher.py`
- `tradingagents/agents/researchers/bear_researcher.py`

**What they do**: Argue for buying vs selling based on analyst reports

**Exercise**:
1. Read both files side by side
2. Notice how they access the 4 analyst reports
3. See how they build on each other's arguments
4. Look at the "history" in the debate state

**Key concept**: Debate state (`InvestDebateState` in `agent_states.py`)

**Experiment**:
```python
# In main.py, increase debate rounds
config["max_debate_rounds"] = 3  # Default: 1

# Run and compare output quality
python main.py
```

More debate rounds = more back-and-forth = better reasoning (but slower & more expensive)

### Step 6: The Research Manager (1 hour)

**File**: `tradingagents/agents/managers/research_manager.py`

**What it does**: Judges the bull/bear debate and makes investment decision

**Exercise**:
1. Read the prompt given to the manager (lines 22-38)
2. Notice how it accesses past memories
3. See how it creates the `investment_plan`
4. Look at what gets returned to the state

**Key concept**: Managers use "deep-thinking" LLMs (o4-mini or gpt-4o) for critical decisions

---

## Phase 4: The Trader & Risk Team (Day 9-11)

**Goal**: Understand final decision-making and risk management

### Step 7: The Trader Agent (1 hour)

**File**: `tradingagents/agents/trader/trader.py`

**What it does**: Takes investment plan and makes specific BUY/SELL/HOLD decision

**Exercise**:
1. See how it receives the investment plan
2. Read the system message (lines 32-33)
3. Notice the final output format: `FINAL TRANSACTION PROPOSAL: **BUY/HOLD/SELL**`
4. Look at how past memories influence decisions

**Key concept**: The trader is the first point where a concrete action is proposed

### Step 8: Risk Management Team (2 hours)

**Files to study**:
- `tradingagents/agents/risk_analysts/risky_analyst.py`
- `tradingagents/agents/risk_analysts/safe_analyst.py`
- `tradingagents/agents/risk_analysts/neutral_analyst.py`
- `tradingagents/agents/managers/risk_manager.py`

**What they do**: Evaluate the trader's proposal from different risk perspectives

**Exercise**:
1. Read each risk analyst's perspective
2. Notice how they consider different risk factors
3. See how the risk manager synthesizes their views
4. Look at the final decision format

**Experiment**:
```python
# Try with a volatile vs stable stock
python main.py  # NVDA (volatile tech stock)
# Change to KO (stable consumer stock)
python main.py
```

Compare how risk assessment differs.

---

## Phase 5: Data Flow & Architecture (Day 12-14)

**Goal**: Understand how data flows through the system

### Step 9: The Agent State (1 hour)

**File**: `tradingagents/agents/utils/agent_states.py`

**What it does**: Defines the shared state that all agents read/write

**Exercise**:
1. Read the `AgentState` class
2. Identify each field and what it stores
3. Notice `InvestDebateState` and `RiskDebateState`
4. See how annotations work (`Annotated[str, "description"]`)

**Key concept**: State management in LangGraph

### Step 10: The Trading Graph (2 hours)

**File**: `tradingagents/graph/trading_graph.py`

**What it does**: Main orchestrator that initializes LLMs and runs the pipeline

**Exercise**:
1. Read the `__init__` method (lines 35-90)
2. See how LLMs are initialized for OpenAI, Anthropic, Google, Ollama
3. Look at the tool node creation
4. Find the memory system initialization (5 memory systems!)
5. Study the `propagate()` method

**Key concept**: The "graph" in LangGraph is the workflow definition

### Step 11: The Workflow Setup (2 hours)

**File**: `tradingagents/graph/setup.py`

**What it does**: Defines the actual workflow (which agent runs when)

**Exercise**:
1. Find `create_trading_graph()` function
2. Trace the workflow from START to END
3. See how debate routing works (`continue_debate_check`)
4. Notice the conditional edges

**Visualization exercise**:
Draw the workflow on paper:
```
START → Analysts (4x parallel) → Bull/Bear Debate → Manager → Trader → Risk Debate → Risk Manager → END
```

---

## Phase 6: Data Vendors & Tools (Day 15-17)

**Goal**: Understand how agents get external data

### Step 12: Data Vendor Abstraction (1.5 hours)

**File**: `tradingagents/tools/data_vendors/abstract_data_vendor.py`

**What it does**: Defines the interface for all data sources

**Exercise**:
1. Read the abstract class
2. Identify all the methods (get_price_data, get_news, etc.)
3. See which are @abstractmethod (must be implemented)

### Step 13: Specific Data Vendors (2 hours)

**Files**:
- `tradingagents/tools/data_vendors/yfinance_vendor.py`
- `tradingagents/tools/data_vendors/alpha_vantage_vendor.py`

**Exercise**:
1. See how yfinance implements the interface
2. Notice error handling and rate limiting
3. Look at Alpha Vantage's API key usage
4. Compare implementation differences

**Experiment**:
```python
# In default_config.py, change data vendors
config["data_vendors"] = {
    "core_stock_apis": "alpha_vantage",  # Instead of yfinance
    # ... rest of config
}
```

### Step 14: Tool Functions (1.5 hours)

**Files in**: `tradingagents/tools/`

**Exercise**:
1. Read `get_stock_price.py`
2. See how it's decorated (`@tool`)
3. Notice the docstring (LLM reads this!)
4. Look at how it calls the data vendor

**Key concept**: Tools are functions that agents can call. The LLM decides WHEN to call them.

---

## Phase 7: Memory & Learning (Day 18-20)

**Goal**: Understand how the system learns from past decisions

### Step 15: The Memory System (2 hours)

**File**: `tradingagents/agents/utils/memory.py`

**What it does**: Stores and retrieves past trading decisions

**Exercise**:
1. Read the `Memory` class initialization
2. See how it uses ChromaDB (vector database)
3. Look at `add_memory()` - what gets stored?
4. Study `get_memories()` - how are memories retrieved?

**Key concept**: Semantic search using embeddings

**Experiment**:
```python
# After running a few decisions, check memory
import chromadb
client = chromadb.Client()
collections = client.list_collections()
print(collections)
```

### Step 16: Reflection System (1.5 hours)

**Files**:
- Look for memory usage in analyst files
- See how managers query past memories
- Notice the reflection prompts

**Exercise**:
1. Find where memories are queried (search for `memory.get_memories`)
2. See what context is used for retrieval
3. Notice how past recommendations influence current decisions

**Experiment**: Run the same stock analysis twice a few days apart. See if decisions change based on learned patterns.

---

## Phase 8: Advanced Topics (Day 21-25)

**Goal**: Deep dive into advanced features and customization

### Step 17: LLM Configuration (2 hours)

**Files**:
- `tradingagents/default_config.py`
- `tradingagents/graph/trading_graph.py` (LLM init section)

**Topics to explore**:
1. Two-tier LLM strategy
2. Provider abstraction (OpenAI, Anthropic, Google, Ollama)
3. Tool binding with LangChain
4. Temperature and token settings

**Experiment**:
```python
config = {
    "quick_think_llm": "gpt-4o-mini",
    "deep_think_llm": "gpt-4o",
    "temperature": 0.7,  # Add this
}
```

### Step 18: Prompt Engineering (2 hours)

**Exercise**: Review all system messages across agent files

**Key patterns to notice**:
1. Role definition ("You are a...")
2. Context provision (analyst reports, history)
3. Output format specification (tables, bullet points)
4. Constraints ("must end with...", "be concise")

**Experiment**: Modify a system message to change agent behavior:
```python
# In market_analyst.py, adjust the system message
system_message = """You are a VERY CONSERVATIVE market analyst..."""
```

### Step 19: Debugging & Logging (1.5 hours)

**Exercise**:
1. Run with `debug=True`
2. Read the verbose output
3. Trace a single agent call from prompt to response
4. Add your own print statements to track state changes

**Useful debugging**:
```python
# Add to any node function
def my_node(state):
    print(f"DEBUG: Current state keys: {state.keys()}")
    print(f"DEBUG: Market report length: {len(state['market_report'])}")
    # ... rest of function
```

### Step 20: Custom Agents (2 hours)

**Challenge**: Create your own analyst!

**Example**: Macroeconomic Analyst

```python
# tradingagents/agents/analysts/macro_analyst.py
def create_macro_analyst(llm):
    def macro_analyst_node(state):
        tools = [
            get_interest_rates,
            get_gdp_data,
            get_inflation,
        ]

        system_message = """You are a macroeconomic analyst..."""

        # ... implement similar to other analysts

        return {
            "messages": [result],
            "macro_report": report,
        }

    return macro_analyst_node
```

**Exercise**:
1. Define what data your agent needs
2. Create or use existing tools
3. Write the system message
4. Add to the workflow in `setup.py`

---

## Phase 9: Local LLM Setup (Day 26-28)

**Goal**: Run TradingAgents with local models

Follow [RTX3500_SETUP.md](RTX3500_SETUP.md) in detail.

**Steps**:
1. Install Ollama (30 min)
2. Download Llama 3.3 8B (20 min)
3. Configure hybrid setup (30 min)
4. Test and compare to cloud (1-2 hours)
5. Benchmark performance (1 hour)

**Exercise**: Run the same analysis with 3 configs:
1. Full cloud (GPT-4o-mini)
2. Hybrid (Llama 3.3 local + GPT-4o-mini cloud)
3. Full local (Llama 3.3 for everything)

Compare:
- Decision time
- Decision quality
- Cost
- GPU usage

---

## Phase 10: Advanced Projects (Ongoing)

**Goal**: Build on what you've learned

### Project Ideas

#### Project 1: Multi-Stock Portfolio Analysis
Extend the system to analyze multiple stocks and suggest portfolio allocation:
```python
tickers = ["NVDA", "AAPL", "GOOGL", "MSFT", "TSLA"]
decisions = {}
for ticker in tickers:
    _, decision = ta.propagate(ticker, date)
    decisions[ticker] = decision

# Create portfolio allocation agent
portfolio = create_portfolio(decisions)
```

#### Project 2: Backtesting Framework
Test the system on historical data:
```python
dates = pd.date_range('2024-01-01', '2024-12-31', freq='W')
results = []
for date in dates:
    decision = ta.propagate("NVDA", date.strftime("%Y-%m-%d"))
    results.append((date, decision))

# Calculate returns, Sharpe ratio, max drawdown
analyze_backtest(results)
```

#### Project 3: Custom Data Vendor
Add a new data source (e.g., Twitter API):
```python
class TwitterVendor(AbstractDataVendor):
    def get_sentiment_data(self, ticker, date):
        # Implement Twitter scraping
        pass
```

#### Project 4: Fine-Tuned Model
Train a model on financial data:
```bash
# Collect financial news corpus
# Fine-tune Llama 3.3 8B
# Compare to base model performance
```

#### Project 5: Web Interface
Build a UI with Chainlit (already partially supported):
```bash
chainlit run tradingagents/chainlit_app.py
```

---

## Troubleshooting Your Learning

### "I'm stuck on Phase X"
- Re-read the previous phase
- Check the INSTALLATION_GUIDE.md troubleshooting section
- Run the code with `debug=True`
- Add print statements to see intermediate values

### "The code is too complex"
- Start by reading just the docstrings
- Focus on one file at a time
- Draw diagrams to visualize flow
- Discuss with your learning partner

### "I don't understand LangChain/LangGraph"
These are complex frameworks. Recommended resources:
- [LangChain Docs](https://python.langchain.com/)
- [LangGraph Tutorial](https://langchain-ai.github.io/langgraph/tutorials/introduction/)
- Focus on: Chains, Tools, Agents, State Graphs

### "I don't understand embeddings/vector databases"
ChromaDB is used for semantic memory. Resources:
- [Embeddings Explained (10 min video)](https://www.youtube.com/watch?v=5MaWmXwxFNQ)
- [ChromaDB Docs](https://docs.trychroma.com/)

---

## Knowledge Checkpoints

### Checkpoint 1 (After Phase 3)
You should be able to:
- [ ] Run TradingAgents with any stock ticker
- [ ] Explain what each of the 4 analysts does
- [ ] Describe the bull vs bear debate process
- [ ] Identify where decisions are made

### Checkpoint 2 (After Phase 6)
You should be able to:
- [ ] Trace data flow from tool call to agent response
- [ ] Explain the state management system
- [ ] Modify the workflow to add a new step
- [ ] Change data vendors in the config

### Checkpoint 3 (After Phase 9)
You should be able to:
- [ ] Run the system with local LLMs
- [ ] Compare cloud vs local performance
- [ ] Explain the hybrid approach benefits
- [ ] Troubleshoot GPU/VRAM issues

### Final Checkpoint
You should be able to:
- [ ] Build a custom analyst agent
- [ ] Implement a new data vendor
- [ ] Modify prompts to change behavior
- [ ] Explain the entire system architecture to someone else

---

## Learning with a Friend

Since you mentioned working with a friend learning programming:

### Study Together Activities
1. **Code walkthroughs**: Take turns explaining files
2. **Pair debugging**: Debug issues together
3. **Compare outputs**: Run same analysis, discuss differences
4. **Build together**: Create a custom agent as a team
5. **Teaching moments**: Explain concepts you understand to each other

### Division of Labor
- **Person A**: Focus on analysts and data flow
- **Person B**: Focus on debate system and managers
- **Together**: Integrate understanding at each checkpoint

### Collaboration Exercises
1. One person modifies a prompt, other tests impact
2. One sets up local LLM, other tests with cloud
3. Compare notes on cost analysis decisions
4. Build custom agents and integrate them

---

## Next Steps After This Path

Once you've completed this learning path:

1. **Contribute**: Open issues, submit PRs to improve the codebase
2. **Experiment**: Test novel agent configurations
3. **Research**: Read academic papers on multi-agent systems
4. **Build**: Create your own trading strategies
5. **Share**: Document your learnings for others

**Remember**: This is a research and educational framework. DO NOT use it for live trading without extensive validation and risk management.

---

## Additional Resources

### Essential Reading
- Original TradingAgents paper (if available)
- [TRADINGAGENTS_DEEP_DIVE.md](../TRADINGAGENTS_DEEP_DIVE.md)
- LangGraph documentation
- ReAct paper: "Synergizing Reasoning and Acting in Language Models"

### Community
- [LangChain Discord](https://discord.gg/langchain)
- [r/algotrading](https://www.reddit.com/r/algotrading/)
- [r/MachineLearning](https://www.reddit.com/r/MachineLearning/)

### Tools
- [LangSmith](https://smith.langchain.com/) - Debug LangChain applications
- [Weights & Biases](https://wandb.ai/) - Track experiments
- [Jupyter Notebooks](https://jupyter.org/) - Interactive exploration

---

## Conclusion

Learning TradingAgents is a journey through modern AI systems, multi-agent architectures, prompt engineering, and financial analysis. Take your time, experiment freely, and most importantly, enjoy the learning process!

Remember: The goal isn't just to run the code, but to **understand** how it works so you can build your own intelligent systems.

Good luck! 🚀
