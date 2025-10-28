# TradingAgents - Learning Edition 🎓

> **A collaborative learning repository** for understanding multi-agent LLM trading systems.
>
> This is an educational fork of [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents) with extensive documentation, guides, and optimizations for learning with an RTX 3500 GPU.

[![Original Repo](https://img.shields.io/badge/Original-TauricResearch%2FTradingAgents-blue)](https://github.com/TauricResearch/TradingAgents)
[![arXiv](https://img.shields.io/badge/arXiv-2412.20138-B31B1B?logo=arxiv)](https://arxiv.org/abs/2412.20138)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

---

## 🎯 What Is This Repository?

This is a **learning-focused fork** of TradingAgents - a sophisticated multi-agent LLM framework that simulates professional trading firms. We've added:

✅ **Comprehensive deep-dive documentation** (16 sections covering architecture, agents, workflows)
✅ **Beginner-friendly installation guide** with troubleshooting for dependency hell
✅ **RTX 3500 GPU setup guide** for local LLMs (Ollama + Llama 3.3)
✅ **Cost analysis** comparing cloud vs local approaches
✅ **Structured learning path** for progressive understanding (10 phases, 20 steps)
✅ **Simplified requirements** that actually install without issues

**Perfect for**:
- 🎓 Students learning about multi-agent AI systems
- 💻 Developers exploring LLM orchestration with LangGraph
- 📊 Researchers studying financial AI applications
- 🤝 Friends learning programming together

---

## 🚀 Quick Start (5 Minutes)

### 1. Clone This Repository
```bash
git clone https://github.com/YOUR_USERNAME/TradingAgents-Learning.git
cd TradingAgents-Learning
```

### 2. Set Up Python Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies (The Easy Way)
```bash
pip install -r requirements-minimal.txt
```
⏱️ Takes 2-5 minutes (vs 40+ min with full requirements.txt)

### 4. Configure API Keys
```bash
cp .env.example .env
# Edit .env with your keys:
# - OpenAI API: https://platform.openai.com
# - Alpha Vantage (free): https://www.alphavantage.co/support/#api-key
```

### 5. Run Your First Analysis
```bash
python main.py
```

You'll see 10+ AI agents analyze NVDA stock and make a trading decision!

---

## 📚 Learning Resources

We've created extensive documentation to help you understand every aspect of the system:

### 📖 Start Here
- **[LEARNING_PATH.md](docs/LEARNING_PATH.md)** - 10-phase structured learning guide (start here!)
- **[INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)** - Detailed setup with troubleshooting

### 🔍 Deep Dives
- **[TRADINGAGENTS_DEEP_DIVE.md](TRADINGAGENTS_DEEP_DIVE.md)** - 16-section architecture analysis
- **[RTX3500_SETUP.md](docs/RTX3500_SETUP.md)** - Local LLM setup for your GPU
- **[COST_ANALYSIS.md](docs/COST_ANALYSIS.md)** - Cloud vs local cost comparison

### 📊 Learning Path Overview

| Phase | Focus | Time | Outcome |
|-------|-------|------|---------|
| 1 | Getting Started | 2 hours | Run first analysis |
| 2 | Understanding Agents | 4 hours | Know what each agent does |
| 3 | Debate System | 4 hours | Understand bull/bear debates |
| 4 | Trader & Risk | 4 hours | Final decision making |
| 5 | Data Flow | 4 hours | Trace complete pipeline |
| 6 | Data Vendors | 4 hours | External data integration |
| 7 | Memory & Learning | 4 hours | How agents learn |
| 8 | Advanced Topics | 6 hours | Prompts, debugging, custom agents |
| 9 | Local LLM Setup | 4 hours | Run on your RTX 3500 |
| 10 | Projects | Ongoing | Build your own systems |

**Total**: ~36 hours to comprehensive understanding

---

## 🏗️ System Architecture

TradingAgents mimics a real trading firm with specialized roles:

```
┌─────────────────────────────────────────────────────────────┐
│                     ANALYST TEAM (4 agents)                 │
├─────────────────────────────────────────────────────────────┤
│  Market Analyst  │  Sentiment  │   News    │ Fundamentals  │
│  (Technical)     │  (Social)   │  (Macro)  │  (Financial)  │
└────────┬─────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                 RESEARCH TEAM (Bull vs Bear)                │
├─────────────────────────────────────────────────────────────┤
│         Bull Researcher  ⚔️  Bear Researcher                │
│              (Debate for 1-3 rounds)                        │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                    RESEARCH MANAGER                         │
│            (Judges debate, creates plan)                    │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                       TRADER AGENT                          │
│              (Proposes BUY/SELL/HOLD)                       │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│            RISK MANAGEMENT TEAM (3 analysts)                │
├─────────────────────────────────────────────────────────────┤
│      Risky Analyst │ Safe Analyst │ Neutral Analyst         │
└────────┬────────────────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│                      RISK MANAGER                           │
│                (Final decision & execution)                 │
└─────────────────────────────────────────────────────────────┘
```

**Total LLM calls per decision**: 12-20 (depending on debate rounds)
**Decision time**: 2-5 minutes (cloud) or 4-7 minutes (local RTX 3500)

---

## 💰 Cost Comparison

| Configuration | Per Decision | Monthly (30) | Best For |
|---------------|--------------|--------------|----------|
| **GPT-4o-mini (Cloud)** | $0.02 | $0.60 | **Beginners** (recommended) |
| **Hybrid (RTX 3500)** | $0.01 | $0.30 | Learning local deployment |
| **Full Local (RTX 3500)** | $0.00 | $0.00 | High volume testing |
| GPT-4o (Cloud) | $0.35 | $10.50 | Premium quality |

See [COST_ANALYSIS.md](docs/COST_ANALYSIS.md) for detailed breakdown.

---

## 🖥️ Hardware Requirements

### Cloud-Only (Easiest)
- Any computer with internet
- No GPU needed
- $5-20/year in API costs

### Hybrid (Recommended for Learning)
- **RTX 3500 Ada (12GB VRAM)** ✅ Your current GPU!
- Runs quick-thinking agents locally
- Managers use cloud API
- 50% cost savings

### Full Local (Advanced)
- RTX 4090 (24GB) or better recommended
- RTX 3500 works but slower
- Complete privacy, $0 API costs

---

## 🛠️ Installation Issues?

### Problem: Pip Install Stuck Forever
**Symptom**: `pip install -r requirements.txt` runs for 40+ minutes

**Solution**: Use our minimal requirements
```bash
pip install -r requirements-minimal.txt
```

### Other Issues
See [INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) for comprehensive troubleshooting.

---

## 📝 Usage Examples

### Basic Usage
```python
from tradingagents.graph.trading_graph import TradingAgentsGraph
from tradingagents.default_config import DEFAULT_CONFIG

ta = TradingAgentsGraph(debug=True, config=DEFAULT_CONFIG.copy())
_, decision = ta.propagate("NVDA", "2024-05-10")
print(decision)
```

### Hybrid Configuration (RTX 3500)
```python
config = DEFAULT_CONFIG.copy()
config["llm_provider"] = "ollama"
config["quick_think_llm"] = "llama3.3:8b"  # LOCAL on RTX 3500
config["deep_think_llm"] = "gpt-4o-mini"   # CLOUD for managers
config["backend_url"] = "http://localhost:11434"

ta = TradingAgentsGraph(debug=True, config=config)
_, decision = ta.propagate("AAPL", "2024-05-10")
```

### Custom Configuration
```python
config = DEFAULT_CONFIG.copy()
config["max_debate_rounds"] = 3  # More debate = better quality
config["max_risk_discuss_rounds"] = 2

config["data_vendors"] = {
    "core_stock_apis": "yfinance",
    "technical_indicators": "yfinance",
    "fundamental_data": "alpha_vantage",
    "news_data": "alpha_vantage",
}

ta = TradingAgentsGraph(debug=True, config=config)
```

---

## 🎓 Learning with a Friend

Since this is designed for collaborative learning:

### Recommended Approach
1. **Person A**: Focus on analyst agents & data flow
2. **Person B**: Focus on debate system & managers
3. **Together**: Meet at each checkpoint to discuss

### Study Activities
- Take turns explaining files to each other
- Pair debugging sessions
- Compare outputs from different configurations
- Build a custom agent together
- Share what you learned in your own words

See [LEARNING_PATH.md](docs/LEARNING_PATH.md) for detailed collaboration exercises.

---

## 🔬 What You'll Learn

By working through this repository, you'll understand:

✅ **Multi-agent systems** - How specialized AI agents collaborate
✅ **LangGraph** - Workflow orchestration for LLM applications
✅ **ReAct prompting** - Reason + Act paradigm for tool-using agents
✅ **Function calling** - How LLMs use external tools/APIs
✅ **Debate mechanisms** - Adversarial agents improving decisions
✅ **Memory systems** - Vector databases for learning from past decisions
✅ **Local LLMs** - Running Llama/Qwen on your own hardware
✅ **Cost optimization** - Hybrid cloud/local architectures
✅ **Prompt engineering** - Crafting effective agent instructions

---

## 🚨 Important Disclaimers

⚠️ **This is for EDUCATION and RESEARCH ONLY**

- DO NOT use for live trading without extensive validation
- Past performance does not guarantee future results
- This is NOT financial advice
- Trading involves significant risk of loss
- Agent decisions are non-deterministic and can vary

See [Tauric AI Disclaimer](https://tauric.ai/disclaimer/) for full details.

---

## 📦 What's Included

```
TradingAgents-Learning/
├── README.md                        # This file (beginner-friendly)
├── TRADINGAGENTS_DEEP_DIVE.md      # 16-section architecture guide
├── requirements-minimal.txt         # Simplified dependencies
├── requirements.txt                 # Full dependencies (advanced)
├── docs/
│   ├── INSTALLATION_GUIDE.md       # Detailed setup & troubleshooting
│   ├── RTX3500_SETUP.md            # Local LLM guide for your GPU
│   ├── COST_ANALYSIS.md            # Cloud vs local cost comparison
│   └── LEARNING_PATH.md            # Structured 10-phase curriculum
├── tradingagents/
│   ├── agents/                     # All agent implementations
│   │   ├── analysts/               # 4 analyst agents
│   │   ├── researchers/            # Bull/bear debate agents
│   │   ├── trader/                 # Trading decision agent
│   │   ├── risk_analysts/          # 3 risk analysts
│   │   └── managers/               # Research & risk managers
│   ├── graph/                      # LangGraph workflow
│   ├── tools/                      # Data vendor integrations
│   └── default_config.py           # Configuration settings
├── main.py                         # Simple usage example
└── cli/                            # Interactive CLI interface
```

---

## 🤝 Contributing

Found a bug? Have a suggestion? Want to add more documentation?

We welcome contributions! This is a learning repository - help make it better for others.

**Ideas for contributions**:
- Additional troubleshooting guides
- More detailed code comments
- Example projects and tutorials
- Performance benchmarks
- Alternative model configurations
- Documentation improvements

---

## 🙏 Acknowledgments

This repository builds on the excellent work by:

- **[TauricResearch](https://github.com/TauricResearch)** - Original TradingAgents framework
- **Authors**: Yijia Xiao, Edward Sun, Di Luo, Wei Wang
- **Paper**: [TradingAgents: Multi-Agents LLM Financial Trading Framework (arXiv:2412.20138)](https://arxiv.org/abs/2412.20138)

Special thanks to:
- **Alpha Vantage** for free API access and increased rate limits for TradingAgents
- **LangChain team** for LangGraph framework
- **Ollama** for making local LLM deployment easy

---

## 📄 Citation

If you use this for research or learning, please cite the original work:

```bibtex
@misc{xiao2025tradingagentsmultiagentsllmfinancial,
      title={TradingAgents: Multi-Agents LLM Financial Trading Framework},
      author={Yijia Xiao and Edward Sun and Di Luo and Wei Wang},
      year={2025},
      eprint={2412.20138},
      archivePrefix={arXiv},
      primaryClass={q-fin.TR},
      url={https://arxiv.org/abs/2412.20138},
}
```

---

## 📬 Questions or Issues?

- **Installation problems?** Check [INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)
- **Learning questions?** Follow [LEARNING_PATH.md](docs/LEARNING_PATH.md)
- **GPU setup?** See [RTX3500_SETUP.md](docs/RTX3500_SETUP.md)
- **Cost concerns?** Read [COST_ANALYSIS.md](docs/COST_ANALYSIS.md)
- **General questions?** Open an issue on GitHub

---

## 🎯 Next Steps

Ready to start learning?

1. ✅ **Install** using the Quick Start above
2. 📖 **Read** [LEARNING_PATH.md](docs/LEARNING_PATH.md)
3. 🏃 **Run** your first analysis
4. 🔍 **Explore** [TRADINGAGENTS_DEEP_DIVE.md](TRADINGAGENTS_DEEP_DIVE.md)
5. 🎓 **Learn** progressively through all 10 phases
6. 🚀 **Build** your own custom agents

**Good luck on your learning journey!** 🚀

---

<div align="center">

**Original Repository**: [TauricResearch/TradingAgents](https://github.com/TauricResearch/TradingAgents)

Made with ❤️ for learners and educators

</div>
